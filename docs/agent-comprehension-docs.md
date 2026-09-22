# Agent comprehension docs — the technique

**What this is**: the repeatable way we document how a Fli app works *internally*, derived from its code and the docs it
already has, so an agent opening the repo knows how it works. Written 2026-09-22 (David + Claude, FliStudio session);
first run on FliStudio, FliHub, FliCut, FliCast and fli-core in parallel, one session per repo.

**Audience**: the agents that work in the repo. Humans get SYSTEM.md and the README as a by-product.

> **Step 1 on a TypeScript repo** (TS + zod extractor added 2026-09-22, dev-team 0.3.0; piloted on fli-core and
> FliStudio, both committed and verifying). Run `npm install` in the repo first — the extractor parses with the repo's
> own `typescript` and refuses (exit 3) rather than guess. `S` = the schema-mirror skill's `scripts/` dir
> (`/Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/schema-mirror/scripts`):
>
> ```bash
> python3 $S/detect_stack.py .                                                   # typescript/zod must show [OK ]
> python3 $S/extract_typescript.py . -o docs/schema-mirror.json                  # one run covers TS and zod
> python3 $S/render_mirror.py docs/schema-mirror.json -o docs/schema-mirror.md
> python3 $S/verify_mirror.py docs/schema-mirror.json                            # must exit 0
> ```
>
> Then read the page's **Cannot be mirrored** table before trusting it: schemas built by helpers (`scanned(...)`,
> `zoneScan(...)`, `callResult(...)`) and bases imported from `@flivideo/core` are named gaps, not absences — an app's
> mirror links to core's schemas by name and fli-core's own mirror holds their shape. A repo's incidental Python
> scripts are listed there as not covered; never commit a separate "mirror" of them as if it were the app.

---

## The three steps — in this order

| # | Skill | Produces (in the target repo) | Why this position |
|---|---|---|---|
| 1 | `/dev-team:schema-mirror` | `docs/schema-mirror.md` + `docs/schema-mirror.json` | The **facts**: schemas, types, enums, closed sets, each anchored to `file:line`, derived not typed. Has a verify mode, so drift becomes an exit code |
| 2 | `/dev-team:system-context` | `docs/SYSTEM.md` + `docs/AGENT-NOTES.md`, and the `@docs/AGENT-NOTES.md` line in `CLAUDE.md` | The **explanation**: how it works, why, pitfalls. Builds on step 1 — link to the mirror, never retype a schema |
| 3 | `/dev-team:craft-readme` | `README.md` (refresh, not rewrite from zero) | The **front door**, last, so it can point into 1 and 2 without duplicating them |

**Why order matters**: the mirror is checkable, the narrative is not. Putting the checkable layer first means the narrative
cites facts instead of restating them, and a later `verify_mirror.py` run catches the day the code moves.

---

## Rules for every run

- **Docs only.** Change nothing under `src/`, `server/`, `client/`, `shared/` or any code path. No refactors, no fixes —
  a bug you find goes in the report as a finding, not a commit.
- **Ground every claim in this repo's code or docs.** Label anything not read directly from code `[inferred]`. Never
  invent a path, port, command or version — if you cannot find it, say so.
- **The Fli family shares contracts** (`@flivideo/core` / repo `/Users/davidcruwys/dev/ad/flivideo/fli-core`, the
  `fli.studio.json` identity file, the `fli.<app>…json` decision files). **Cite them; do not restate them.** Say what
  *this* app reads and writes, and point at fli-core for the shape.
- **Existing docs are input, not truth.** Where a doc and the code disagree, the code wins and the disagreement goes in
  the report. Do not delete an existing doc: if the new docs supersede one (e.g. an old `CONTEXT.md`), add a one-line
  pointer at its top to the new file instead.
- **Never touch live data**: `/Users/davidcruwys/dev/video-projects/`, `~/.config/appydave`, `~/.fli`, any app store.
- **Do not start, stop or restart any running app or dev server.**
- **Commit and push to `main`** in the target repo when done (docs only, conventional message). No branches, no PRs.

---

## Per-repo notes

| Repo | Path | Run | Note |
|---|---|---|---|
| FliStudio | `/Users/davidcruwys/dev/ad/flivideo/flistudio` | steps 1–3 | The agent door describes itself (`flistudio list`, `GET /api/capabilities`) — AGENT-NOTES points there, does not copy the capability list |
| FliHub | `/Users/davidcruwys/dev/ad/flivideo/flihub` | steps 1–3 | Has an older-generator `CONTEXT.md` + `context.globs.json`. New docs supersede `CONTEXT.md`: pointer line at its top, do not delete |
| FliCut | `/Users/davidcruwys/dev/ad/flivideo/flicut` | steps 1–3 | Nothing exists yet beyond README + CLAUDE.md |
| FliCast | `/Users/davidcruwys/dev/ad/flivideo/flicast` | step 1, then **refresh** 2 and 3 | Already has `docs/SYSTEM.md` + `docs/AGENT-NOTES.md` from `system-context` (2026-09-16). Refresh against the code, keep what is still true |
| fli-core | `/Users/davidcruwys/dev/ad/flivideo/fli-core` | **step 1 only** | It *is* the shared contract; the other apps' docs cite its mirror |
| FliStack | `/Users/davidcruwys/dev/ad/flivideo/flistack` | not run | Docs-only, no app code yet (Phase II not started). Run when it has code |

---

## Done when

1. The step outputs above exist in the repo, and `python3 <schema-mirror skill>/scripts/verify_mirror.py docs/schema-mirror.json`
   exits 0.
2. `CLAUDE.md` carries the `@docs/AGENT-NOTES.md` line (steps 2 repos only).
3. Committed and pushed to `main`.
4. The session's final message is the **report**: files written (absolute paths), commit hash, doc-vs-code disagreements
   found, bugs noticed (not fixed), and what it could not verify.

## Re-running later

Step 1's verify mode is the cheap check: run it after any schema change; exit 1 means regenerate the mirror and re-read
AGENT-NOTES for anything the change invalidated. Full re-run of 2 and 3 only when the app's shape has changed.
