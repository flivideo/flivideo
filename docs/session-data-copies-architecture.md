# Session data copies: one way for every Fli app to read a Claude session

**Purpose**: Names the cross-cutting problem behind Story Pilot's "dock extract". A Claude Code session lives as a `.jsonl`
on the one machine that ran it, but videos, stories and reviews need its words on other machines. This note says what
exists today, what the open decisions are, and which other systems have the same need. It is a design note, not a go.

**For Agents**:
- Read before building anything that reads, copies or links a Claude session from a Fli app or extension.
- Don't add a second session-copy mechanism. Extend this one, or raise it here first.
- The storage decision (where copies live and whether they go into git) is **open and David's** (see §4).

*Status 2026-11-04: banked as architecture. David: "this is really the unified way that FliStudio and its subsidiary
extensions and applications deal with sessions with data copies… if you focused it on this one area, we would have
scattered systems all over the place." The git question is "hot", to be talked through today; it is not a yes.*

## 1 · The problem

```
 M4  ──  d13 sessions (.jsonl)          Roamy ── d14, d19 sessions (.jsonl)
          │                                         │
          └── Story Pilot on the M4 can read ──┐    └── Story Pilot on the M4 CANNOT read
                                               ▼
                                   "not on this machine"
```

A session transcript is large (10–40 MB), private, and stays on the machine that ran it. Any app that wants to use it
for something else (a story, a review, a recap) either works on that machine only or needs a copy.

## 2 · What exists today (Story Pilot W1, flistudio `188a202`)

- **Dock extract:** `modules/storypilot/scripts/dock_extract.py` runs on the machine holding the transcript. It writes
  `resources/sessions/<id>.turns.json` into the video project: David's turns only, with skill bodies, `isMeta` messages,
  pastes, tool results and image placeholders removed. Each turn has an index and timestamp anchor, plus
  `{session_id, machine, path, bytes, sha256, extractedAt, by}`.
- **Read order:** extract → the live transcript → "not on this machine (run the extract there)".
- **Staleness:** a size or mtime change on the transcript marks the extract out of date.
- **Paging:** `story.source.read` has `offset`/`limit`. No silent cut.

It works, but it is **Story-Pilot-shaped**: the filter, the file location and the verb all live in one module.

## 3 · What a unified version would own

| Concern | Today (Story Pilot) | Unified (proposal) |
|---|---|---|
| Turn filter (whose words are whose) | `storypilot/server/sessions.ts` | one shared library, used by every reader |
| Extract format | `<id>.turns.json` | one versioned schema, maybe with an optional Claude-side summary layer |
| Where copies live | the video project's `resources/sessions/` | **open (§4)** |
| How copies travel | not yet decided (git was proposed) | **open (§4)** |
| Refresh | by hand, per machine | a verb any app can call, run on the owning machine |
| Finding a session by id | each tool resolves its own | one resolver (the chaperone skill already has `resolve_session.py`) |

## 4 · Open decisions (David's)

1. **Where do copies live?** In the project folder, in a central store (say, beside Captain's Log on the M2), or both?
2. **How do they travel?** Through a git commit to the private project repo (v-appydave), a Syncthing or Dropbox folder,
   or fetched live over Tailscale from the owning machine.
3. **What goes in a copy?** David's words only (today), or both sides of the session plus a summary?
4. **Privacy:** sessions can contain pasted secrets. Any copy path needs a scrub step before it leaves the machine.

## 5 · Other systems with the same need (candidates to check, not yet verified)

| System | Why it might need session copies |
|---|---|
| Captain's Log | captures already link to sessions by id; a reader there hits the same "wrong machine" wall |
| `sesh` skills (session-recall, session-archaeology, session-rescue) | each reads and filters transcripts its own way |
| AngelEye (session inspector) | a fleet view of sessions; has known cross-machine sync gaps |
| Story Pilot Prep | the angle and evidence come from sessions |
| Teletubby | scripts may come from a story built out of sessions |
| AppyRig / OpenRig | rig seats are sessions; their history is per machine |

Next step when David picks it up: confirm each row by reading that system's session code, then write one brief.
Backlog entry: `docs/backlog.md` → "Session data copies".
