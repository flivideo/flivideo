# Brief: Overlay Pilot chin bug — 2026-10-31

**Worker:** `overlay-chin-dev` · **Worktree:** `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/overlay-chin` (branch `overlay-chin`, from main `ce8fd25`)
**Reports to:** flivideo-orch (SendMessage `flivideo-orch`). Never park waiting on David — route questions to orch.
**Priority:** #1 of David's Saturday plan. Small. David records the Overlay Pilot video today.

## Source
- Captain's Log B676 (Plaud voice, wins on intent) + B677 §2, §9 D1–D2, §10 Q1–Q2 — `$CAPTAINS_LOG_URL` / captains-log MCP `capture_get`.

## The bug
On Joy's videos some overlays cover her chin. Presenter tracking (a box around the head so overlays avoid it)
**already exists**: the AppyDave presenter-tracking work (~3–4 weeks ago) and the original Joy overlay
scripts both use it. **Never rebuild it.** Find it, find out why Overlay Pilot does not use it (not wired /
wrong coordinates / per-style), and wire it in.

Code: `modules/overlay-pilot` (hits already in `server/looks.ts`, `grammar/rules.json`); planning in
`docs/planning/overlay-pilot`. Skill: `flivideo:overlay-pilot`. Also search `video-editor:overlay-*` skills
and the Joy overlay scripts for the existing tracker.

## Steps, in order
1. **First establish whether re-running a style overwrites the previous output.** Report the answer.
2. If it overwrites: add the smallest variant/version so a re-run writes beside the original.
3. Wire presenter tracking in.
4. Re-run on **Joy's three existing videos WITHOUT overwriting the originals** — old and new viewable side by side.
5. Gates: typecheck, tests, lint per `appystack:appystack-conventions`. Commit on `overlay-chin`.

## Done
Branch committed, gates green, three new renders beside three untouched originals, and a message to
flivideo-orch with: overwrite answer, root cause, file paths of old + new for each video, gate output.
orch merges and restarts FliStudio — **you do not merge to main and do not restart anything.**

## Never
- Never test against live ports 7150/7151; use the worktree's own ports.
- Never delete, move or overwrite any existing render or take.
- Never `pkill`/`killall` with patterns.
