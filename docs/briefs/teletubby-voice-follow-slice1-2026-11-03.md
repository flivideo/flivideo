---
created: 2026-11-03
timestamp: 2026-11-03T20:25+07:00
---
# Brief: Teletubby voice-follow SLICE 1 — port Textream's matcher + a replay harness on real takes (2026-11-03)

**From:** `flivideo-orch`. **To:** `voice-follow-dev` (**M2**, cwd `/Users/davidcruwys/dev/ad/flivideo/teletubby`). Report to `flivideo-orch`.
**Go:** David's "yes", relayed by `flivideo-roamy` ~20:15 — **slice 1 only**. This answers `teletubby/CLAUDE.md:284`'s
"ask first" for slice 1; later slices need a new ask. **Machine: M2** — code, standing ruling.

## Read first
`/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/textream-vs-teletubby-harvest.md` (esp. §voice-following, option
(a), "The smallest first slice"). Textream source: `~/dev/upstream/repos/textream` @ `2c02f3e` (MIT, © 2026 Fatih Kadir Akin).
Teletubby: its `CLAUDE.md`, `docs/AGENT-NOTES.md`, `src/core`. Skill `flivideo:teletubby`.

## Setup
Worktree off origin/main: `git -C ~/dev/ad/flivideo/teletubby fetch origin && git -C ~/dev/ad/flivideo/teletubby worktree add ~/dev/ad/flivideo/teletubby-worktrees/voice-follow -b voice-follow origin/main`, `npm install`.

## Do
1. Port Textream's `PromptMatcher` to `src/core/voice-follow.ts` (pure TypeScript, no I/O), with an MIT header + attribution
   (copyright line, licence text or pointer, source path + commit). Port its 2 tests to vitest. Keep the semantics: forward-only,
   2-of-3 agreement before stepping, manual-jump handling.
2. **Replay harness** (`scripts/` or `src/core/…replay` + a CLI entry): input = a recorded take's **word-timed FliTools
   transcript** + the **script** it was read from; feed words at real timing; output per beat: when the aligner would have
   stepped vs **when David actually pressed ↓**, with offsets (s) and a match rate.
3. **Find real data** (read-only): takes recorded with Teletubby where both a word-timed transcript and a record of David's ↓
   presses exist. Look in Teletubby's own logs/state, FliStudio/fli-core facts logs, and the video projects
   (`/Users/davidcruwys/dev/video-projects/v-appydave/*`, `v-aitldr/*`) — copy into scratch, never edit project files. **If no
   ↓-press record exists anywhere, STOP before inventing one** and report what data exists and what proxy you propose (e.g. the
   beat/paragraph boundaries from the script vs transcript word times) — orch will decide.
4. Run it on **at least 3 real takes**. Report per take: beats, aligner steps, matched within ±1 s / ±2 s, median and worst
   offset, false/early steps, misses.

## Gate
`npm run typecheck`, `npm test` green; the 2 ported tests + harness unit tests. Commit on `voice-follow`, push the branch. Do
not merge. Write results to `teletubby/docs/voice-follow-slice1-results-2026-11-03.md`.

## Out of scope
Mic, Speech permission, Swift helper, any UI, any change to how Teletubby scrolls today. Keep the M2 light.
STOP and report to `flivideo-orch`: the per-take table, the overall verdict (promising / not), commits, and the data source used.
