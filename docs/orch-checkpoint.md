# Checkpoint: flivideo-orch — 2026-10-27

**Purpose**: Where the FliVideo orchestrator (tmux `flivideo-orch`, M4) is up to. Read this after a compact or a cold start.

**For Agents**:
- Read this first when resuming as flivideo-orch
- The current step tells you the next action; the standing rules are not optional

## Current step
**Merge `fc50-waits` into FliCut main** — built and pushed. Hold for David's "go", because it restarts his FliCut window.

## Progress
### Done
- [x] FR-174 FliHub card buttons (flihub `9e6917e`: Rename · Discard blue primary on the right, Rename · Keep amber)
- [x] D12 brief B1–B6 + `edit.render` (flivideo `307422a`; FliStudio `9ae0ee8`; FliCut `ebae9bb`, `06f1422`, `1771ab4`)
- [x] FC-49 open-a-cut (FliStudio `a5b87f7`, FliCut `fc590a0`), merged and restarted
- [x] FC-50 investigation (FliCut backlog `b0be94b`): stall = D12 is all-HEVC + densest-bitrate stretch 7:30–8:23.7, not B1 and not player code
- [x] Restart safety in app-registry `75e5e37` (my-app stop/restart refuse while busy unless `--force`), merged
- [x] flicut skill updated in appydave-plugins `df8f17e`
- [x] D12 disk question: only ONE export exists, `/Users/davidcruwys/dev/video-projects/v-appydave/d12-openrig-agent-teams/videos/openrig-agent-teams/openrig-agent-teams-audio-a100.mp4` (169 MB, 08:26). The second export overwrote the first in place; nothing went to the Trash
- [x] Disk-drop diagnosis: swap. VM volume was 20.4 GB, 17.9 GB of swap used on 24 GB RAM, 17 Claude processes. Not temp files (`/private/tmp` was 2.1 GB), no APFS snapshots

### In progress
- [ ] Merge `fc50-waits` ← YOU ARE HERE
  - Branch: worktree `/Users/davidcruwys/dev/ad/flivideo/flicut-worktrees/fc50-waits`, pushed. Commits `99ad95f` (restart safety R1–R6 + length fix) and `7bc5a4a` (FC-50 parts 1+4 + dev-shot), on top of main `b0be94b`
  - Gates: typecheck clean, 608 tests pass, api:check current
  - Steps on David's go:
    1. `bin/flicut status --json` must show `busy: []`
    2. `cd /Users/davidcruwys/dev/ad/flivideo/flicut && git merge --ff-only fc50-waits && git push`
    3. `bin/flicut restart` (never `my-app restart flicut`), then confirm one listener on 7121 with `lsof -nP -iTCP:7121 -sTCP:LISTEN`
    4. Confirm R2 reopens the D12 cut
    5. Remove the worktrees `restart-safety` and `fc50-waits`, and delete those branches local and remote
    6. Add the restart-safety verbs to the flicut skill (`/Users/davidcruwys/dev/ad/appydave-plugins/flivideo/skills/flicut/SKILL.md`): `busy`, `job.rerun`, `cut.dismiss`, `cuts.engine`/`accept-engine`, `player.stats`, `edit.get length`
    7. Tell the Roamy session ("M4 Mini session audit and Kokoro voiceover") it is live and to re-render: old renders run ~24 s long and the SRT drifts

### Pending — awaiting David's decision
- R5: run live FliCut from a promoted release worktree (`flicut-live`) with an `app:promote` step that refuses while busy
- FC-50 part 2 (HEVC proxy) and part 3 (playhead out of the store). Research first; no design ahead of it
- FliHub DiscardModal default (currently "Keep the rest"; recommended leaving it)
- FR-174 player buttons + autoplay; Teletubby auto-stage on `write_script`
- PreToolUse hook false positive ("appytron-upgrade silently overwrites…") blocks harmless Bash. Lives in David's settings and needs his yes. Workaround: put commands in scratch script files
- Adding `"busy": "bash scripts/app.sh busy"` to FliCut's control block in `~/.config/appydave/apps.json` (David's config; mention only)

### Not yet seen in a real window
- FC-49 screens, the "Proposals changed" bar, how FliStudio shows a refused stop (exit 5). My screencaptures come back black, so David must look

### Low priority / banked
- `scripts/dev-probe.sh` and `dev-probe-cdp.sh` still `pkill -f` (flagged, not fixed)
- Pre-existing failing checks: FliStudio e2e 390px, `verify_mirror.py`, FliHub 12 lint errors, FliCut prettier. Flaky tests: `requestLogger`, `hear-it`, `fc37-inputs`
- Banked, not authorised: FR-173, FR-165, FR-175, FR-176, FC-48; YouTube login untangle (`/Users/davidcruwys/dev/ad/flivideo/docs/briefs/youtube-logins-untangle-2026-10-22.md`)
- Reach reports: re-pull every couple of weeks: `bin/flistudio youtube.reporting.pull --brand appydavelabs --as agent:flivideo-orch --json`

## Before starting the next step
- Never restart FliCut unless `/api/status` shows `busy: []`, and tell David first. A restart on 26 Oct killed Roamy's render `62e1f45462dbb54a`
- Don't change the D12 edit `openrig-agent-teams`; no exporting or publishing D12; never delete or archive takes
- Workers stay in worktrees, never on live checkouts; no pattern kills (`pkill -f`, `killall`)
- FliStudio restart is ours (`/Users/davidcruwys/dev/ad/apps/app-registry/bin/my-app restart flistudio`); never restart FliHub by hand

## Ruled out this window
- `my-app restart flicut`: orphaned PID 9578 and killed a render. Use FliCut's own `bin/flicut restart`
- "FC-50 stall is the B1 filler maths or the player": ruled out. It is HEVC density under load
- "The 300 ms view-state save is new and causes the stall": not new (Aug/Sept), and no disk write during play
- "D12 really runs 19:35": wrong. `buildPlan` doubled frames at 1,025 joins (+23.8 s); 19:11 is true
- "Two exports = two files on disk": wrong. Overwritten in place
- "Disk drop = temp folders or system clones (the Roamy cause)": not on the M4 today. It was swap growth
