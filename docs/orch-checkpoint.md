# Checkpoint: flivideo-orch — 2026-10-27

**Purpose**: Where the FliVideo orchestrator (tmux `flivideo-orch`, M4) is up to. Read this after a compact or a cold start.

**For Agents**:
- Read this first when resuming as flivideo-orch
- The current step tells you the next action; the standing rules are not optional

## Current step
**2026-10-27 late:** Live test PASSED: David uploaded `fIuXHsVPDMs` private to AppyDave from the z99 panel (processed/succeeded per upload-status), then deleted it in Studio. Fix `1ffa162` (studioPayload null defaults) merged. David enabled YouTube Data API v3 in project 229911379755. z99 project folder moved to macOS Trash (David empties). Running: builder `publish-upload-box` worktree (upload box on Publish page + accessNotConfigured → not-set-up message). Merge + restart only when no upload is running. Unknown still: Unlisted lock test result; whether captions landed.

**2026-10-27 15:20Z:** yt-publish MERGED (FliStudio main `43bb6e6`, schema mirror regenerated, worktree + branch removed), FliStudio restarted (7150/7151 up). appydave re-signed by David (AppyCast Brand Account = main channel; scopes analytics + readonly + force-ssl; guard passes). Test project `/Users/davidcruwys/dev/video-projects/v-appydave/z99-youtube-upload-test` (synthetic 36 s testsrc clip + SRT + yellow thumb, 3 chapters, agent-proposed Launch pieces). WAITING: David approves 6 Launch pieces at http://localhost:7150/b/appydave/p/z99-youtube-upload-test?zone=launch&video=upload-test, then Check → Upload in step 1, then Studio check (try Unlisted = private-lock test), then delete the video in Studio. Watch: long uploads may exceed the 5-min request timeout.

**2026-10-27 late:** yt-publish `67c573c` built (create-only, allowlist, 36 tests verified by me). Now running: (a) same builder adds the Upload panel in UploadWizard step 1 (human route; dry-run preview → confirm → private upload → Studio-only list → Mark published); (b) schema-mirror extractor fix in `/Users/davidcruwys/dev/ad/appydave-plugins-worktrees/schema-mirror-ts-fix` (mirror stale since FliStudio `3ea915d`, 10-13). Then: merge both on David's go, restart FliStudio, set up a throwaway test project with decided Launch, David maps Brand Accounts + re-signs `appydave --publish`, dry run, David uploads.

**Builder running: FliStudio YouTube publish** (worktree `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/yt-publish`, branch `yt-publish`, spec `flistudio/docs/briefs/youtube-publish-api-spec-2026-10-27.md` @ `1207f91`). Fake-Google tests only; no real Google calls. **David's ruling 2026-10-27: broad sign-in (`youtube.force-ssl` + readonly + analytics), code create-only: one private `videos.insert` + `thumbnails.set` + `captions.insert` on the just-created id only; endpoint allowlist; real run human-only; no update/delete/playlist/comment code. Editing later as its own job (FliStudio-uploaded only, snapshot-before-change). Delete never.** On return: check gates, report to David, merge only on his go. Live test (private throwaway on AppyDave) waits on David mapping the AppyDave Brand Accounts + `npm run research:auth -- --brand appydave --publish`.

Previous: `fc50-waits` merged 2026-10-27 (FliCut main `7bc5a4a`).

## Progress
### Done
- [x] FR-174 FliHub card buttons (flihub `9e6917e`)
- [x] D12 brief B1–B6 + `edit.render` (flivideo `307422a`; FliStudio `9ae0ee8`; FliCut `ebae9bb`, `06f1422`, `1771ab4`)
- [x] FC-49 open-a-cut (FliStudio `a5b87f7`, FliCut `fc590a0`)
- [x] FC-50 investigation (FliCut `b0be94b`): HEVC density at 7:30–8:23.7
- [x] Restart safety in app-registry `75e5e37`
- [x] **Merged `fc50-waits` → FliCut main `7bc5a4a`** (restart safety R1–R4, R6, length fix, FC-50 parts 1+4). FliCut was NOT running at merge time, so no restart was done. Worktrees + branches `restart-safety`, `fc50-waits` removed local and remote
- [x] flicut skill: new verbs added (appydave-plugins `5c8b1ea`)
- [x] Roamy session ("M4 Mini session audit and Kokoro voiceover") told to re-render D12 (msg sent, not confirmed read)
- [x] D12 disk question + disk-drop diagnosis (swap) — see brains `mac-os/`

### Verified 2026-10-27 (David's screenshot + API)
- [x] FliCut reopened on the D12 cut by itself (R2); one listener on 7121 (PID 11618); `busy` idle
- [x] `cuts.engine`: from 2 → to 2, pending false, so no "Proposals changed" bar is expected. The bar itself is still unseen (it only shows when the engine moves)
- [x] `edit.get` length: kept 1146.75 s (19:07, matches the window), renders 1148.76 s (19:09), 25 fps. Summary says 134 cuts; the window says 128 (not investigated)

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
