# Brief: FliEdit drivable audit + assembly spike — 2026-10-31

**Worker:** `fliedit-drivable-dev` · **Worktree:** `/Users/davidcruwys/dev/ad/flivideo/fliedit-worktrees/drivable-audit` (branch `drivable-audit`, from main `d0cb909`)
**Reports to:** flivideo-orch (SendMessage `flivideo-orch`). Never park waiting on David — route questions to orch.
**Priority:** #5 — runs in parallel from the start, but must never delay items 1–4 (Overlay chin bug,
StoryPilot, B-roll Pilot spec, FliHub button). If you contend for a shared resource (CPU-heavy renders,
a port), yield. **Must be usable today**; David uses it tomorrow or the day after.

## Source
- Captain's Log B676 (Plaud, wins on intent) + B677 §7, §9 D7, §10 Q6, §11 step 1.

## Why
FliCut is sequential only. FliEdit must **assemble a layered video** (A-roll + overlay/B-roll) so an AI can
drive the edit of this weekend's three videos (Overlay Pilot, StoryPilot, B-roll Pilot). FliEdit was built in
a day or two on autopilot and has never been used in anger.

## Steps
1. **Audit** against `dev-team:drivable` (JSON-RPC door, capability list, agent principal, busy state).
   Also load `flivideo:fliedit` and `appytron:appytron-conventions` if `appytron.json` exists.
   Output: a short table — capability · drivable today? · gap.
2. **Spike:** prove a **two-layer assembly** (A-roll + one overlay or still) over JSON-RPC from an existing
   clip, end to end to an output file. Answer B677 Q6: can every asset type be supplied drivably?
3. Fix the gaps that block step 2 and the real first input: **A-roll talking heads David records today**
   (no B-roll exists yet). Smallest changes first.
4. Run `test:integration` (port 7171) and the Electron build — both have never been run; report honestly.
5. Commit on `drivable-audit`.

## Done
Audit table + spike output file path + gate output sent to flivideo-orch. orch merges.
**You do not merge to main.**

## Never
- Never touch David's `fli.edit.*` files or the D12 edit `openrig-agent-teams`.
- Never delete/move video files or takes; write outputs to a scratch output folder.
- Never test against live ports 7150/7151/7111/7121/7161/5173/5101.
- Never `pkill -f electron` or any pattern kill.
