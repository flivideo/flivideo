#!/usr/bin/env python3
"""
Repair D10 (appydave/d10-ai-powered-video-cuts) after the 07:03:17.106Z "mark published" click.

What the click did (fli-core markPublished, called from server/src/capabilities/publish.ts markPublished):
every `chosen` piece of the video went `published` and got `changed = {at: 07:03:17.106Z, by: human:ui}`.

This script, per piece:
  A. undoes the stamp on every non-video resource the click touched: status published -> chosen, `changed` back to
     its `added` stamp (what it was before the click: these decisions were never touched after they were made);
  B. for the pieces that have a NEWER proposal David has not decided (social x/linkedin/facebook, description,
     chapters, pinned-comment), turns the old decision back into a plain `candidate` (what FliStudio itself does to a
     replaced decision), so nothing is approved and each piece shows its newest proposal with its open gate.
The video (r_0d0c094673) stays published with its YouTube link. Gates are only checked, never written.

Dry run by default. `--apply` writes fli.resources.json (atomically; refuses if the file changed while running).
Take a backup first. Stop nothing: FliStudio rereads the file on change.
"""
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone

PROJECT = "/Users/davidcruwys/dev/video-projects/v-appydave/d10-ai-powered-video-cuts"
RESOURCES = os.path.join(PROJECT, "fli.resources.json")
GATES = os.path.join(PROJECT, "fli.studio.gates.json")
STAMP_AT = "2026-10-13T07:03:17.106Z"
STAMP_BY = "human:ui"
VIDEO_ID = "r_0d0c094673"
REPAIR_BY = "script:repair-d10"

# Step A: everything the click restamped, besides the video.
STAMPED = {
    "r_73254858d5": "keywords",
    "r_dcf9ecb568": "chapters",
    "r_1b8f74f645": "description",
    "r_6c94e9e5b9": "end-screen",
    "r_c278becd38": "pinned-comment",
    "r_dee88c3e66": "studio-settings",
    "r_438ec652c2": "social-x",
    "r_a85b824e87": "social-linkedin",
    "r_5eae10c51e": "social-facebook",
}
# Step B: old decision -> (newer undecided proposal, its open gate).
SUPERSEDED = {
    "r_438ec652c2": ("r_b2a4bbbf63", "g_8334a98162"),
    "r_a85b824e87": ("r_03fbe6e76e", "g_8334a98162"),
    "r_5eae10c51e": ("r_8a753bd163", "g_8334a98162"),
    "r_dcf9ecb568": ("r_1230b2ad6b", "g_5d77cb9e3e"),
    "r_1b8f74f645": ("r_f39377bfce", "g_2ffa66960a"),
    "r_c278becd38": ("r_1e56d58e3d", "g_8e4ceab4a5"),
}


def main() -> int:
    apply = "--apply" in sys.argv[1:]
    raw = open(RESOURCES, "rb").read()
    digest = hashlib.sha256(raw).hexdigest()
    data = json.loads(raw)
    gates = {g["id"]: g for g in json.load(open(GATES))["gates"]}
    by_id = {r["id"]: r for r in data["resources"]}
    now = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    problems, changes = [], []

    video = by_id.get(VIDEO_ID)
    if not video or video.get("status") != "published":
        problems.append(f"{VIDEO_ID} (video) is not published; this repair is for the state after the click.")

    for rid, kind in STAMPED.items():
        r = by_id.get(rid)
        if r is None:
            problems.append(f"{rid} ({kind}) is missing.")
            continue
        ch = r.get("changed", {})
        if r.get("kind") != kind or r.get("status") != "published" or ch.get("at") != STAMP_AT or ch.get("by") != STAMP_BY:
            problems.append(
                f"{rid} ({kind}) is not as the click left it (status {r.get('status')}, changed {ch.get('at')} by {ch.get('by')}); left alone."
            )
            continue
        if (r.get("meta") or {}).get("posted"):
            problems.append(f"{rid} ({kind}) is ticked posted; left alone.")
            continue
        if rid in SUPERSEDED:
            pid, gid = SUPERSEDED[rid]
            p, g = by_id.get(pid), gates.get(gid)
            ok = (
                p is not None
                and p.get("kind") == kind
                and p.get("status") == "candidate"
                and (p.get("meta") or {}).get("proposal") is True
                and p["added"]["at"] > r["added"]["at"]
                and g is not None
                and g.get("status") == "open"
            )
            if not ok:
                problems.append(f"{rid} ({kind}): proposal {pid} / gate {gid} not as expected; left alone.")
                continue
            r["status"] = "candidate"
            r["changed"] = {"at": now, "by": REPAIR_BY}
            changes.append(
                f"{rid} {kind:16} published -> candidate  (no longer approved; newest proposal {pid} waits, gate {gid} open)"
            )
        else:
            r["status"] = "chosen"
            r["changed"] = dict(r["added"])
            changes.append(
                f"{rid} {kind:16} published -> chosen     (changed restored to {r['added']['at']} by {r['added']['by']})"
            )

    print(f"{'APPLY' if apply else 'DRY RUN'}: {RESOURCES}")
    for c in changes:
        print("  change  " + c)
    for p in problems:
        print("  skip    " + p)
    print(f"  keep    {VIDEO_ID} video published (YouTube link stays); gates untouched")
    if not apply:
        print("Nothing written. Re-run with --apply after taking a backup.")
        return 0
    if problems:
        print("Refusing to write: fix or explain the skips first.")
        return 1
    if hashlib.sha256(open(RESOURCES, "rb").read()).hexdigest() != digest:
        print("Refusing to write: fli.resources.json changed while this ran. Run again.")
        return 1
    fd, tmp = tempfile.mkstemp(dir=PROJECT, prefix=".fli.resources.", suffix=".tmp")
    with os.fdopen(fd, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, RESOURCES)
    print(f"Wrote {len(changes)} changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
