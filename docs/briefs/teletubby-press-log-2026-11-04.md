---
created: 2026-11-04
timestamp: 2026-11-04T10:20+07:00
---
# Brief: Teletubby ↓-press log (the test data voice-follow needs) (2026-11-04)

**From:** `flivideo-orch`. **To:** `tubby-presslog-dev` (**M2**). Report to `flivideo-orch` and STOP.
**Go:** David, 2026-11-04 ~10:15 ("yes" to the press log). **Machine: M2** — code, standing ruling. Orch re-gates on the M4
(where David records), merges, restarts Teletubby.

## Why
Voice-follow slice 1 (`teletubby/docs/voice-follow-slice1-results-2026-11-03.md`) can't be judged: nothing records when David
presses ↓ (or otherwise steps) while reading. With a log, any take read from a Teletubby script becomes ground truth: replay the
take's word-timed transcript through the aligner and compare its steps with David's presses.

## Do
1. On every position change while presenting (↓/↑ step, jump, any key/remote/Stream Deck path that moves the script), append
   one JSON line: `{t: ISO wall clock with ms, mono: monotonic ms since session start, kind: step|back|jump|start|stop,
   from, to, paragraphId?, scriptId, scriptVersion/hash}`. Also log session start/stop (script id, version) so a take can be
   lined up with its recording by wall clock.
2. Where: beside the script's other state, one file per session (e.g. `<project>/…/teletubby/press-logs/<scriptId>-<ISO>.jsonl`
   — follow where Teletubby already writes project data; say where you chose and why). Append-only; never blocks the UI; a write
   failure is logged, not shown.
3. Always on (no setting), it's tiny. Note in Teletubby's CLAUDE.md / AGENT-NOTES.md and the `flivideo:teletubby` skill where the
   logs are and that `scripts/voice-follow-replay.mjs` should accept a press log as the comparison source (add that: per paragraph,
   aligner step vs press time, offsets, ±1 s / ±2 s, median, worst, early, misses). Bump the flivideo plugin version
   (`git pull` appydave-plugins first; commit only the skill + plugin.json).
4. Tests: unit for the log writer (every kind, append-only, failure tolerated) and the replay's press-log mode on a fixture.

## Setup / gate
Worktree: `git -C ~/dev/ad/flivideo/teletubby fetch origin && git -C ~/dev/ad/flivideo/teletubby worktree add ~/dev/ad/flivideo/teletubby-worktrees/press-log -b press-log origin/main`; `npm install`.
`npm run typecheck`, `npm test` green. Don't touch voice-follow matching (slice 2 is separate). No mic, no Speech permission.
Push branch `press-log`; report: sha(s), where logs land, test counts before → after, the replay command with a press log.
