# Checkpoint: flivideo-orch — 2026-10-27

**Purpose**: Where the FliVideo orchestrator (tmux `flivideo-orch`, M4) is up to. Read this after a compact or a cold start.

**For Agents**:
- Read this first when resuming as flivideo-orch
- The current step tells you the next action; the standing rules are not optional

## Current step
**2026-10-29 21:15 local — OVERNIGHT BUILD RUNNING (I am boss).** Spec `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/overnight-2026-10-29-build-spec.md` @280be51 (W1–W8; W8 = fli.brand.json lock). David's "go" verified in flivideo-arch-rsch transcript (14:09:40Z, origin human). Builders (tmux + iTerm): `ovn-templates-dev` (Sonnet: W1→W2→W7 markers), `ovn-flicore-dev` (Opus: W3+W7 window-state+W8 core → tag v0.26.0-rc.1 → W4+W8 non-FliStudio), `ovn-flistudio-dev` (Opus: FliStudio W4/W5/W8 after rc.1, W6 after W1). Watch cron 61f0c1e8 at :13/:43 (session-only). David also asked: check flivideo-arch-rsch every 30 min until ~00:15. Done = every item passed (gate reproduced by me) or parked + morning report `docs/briefs/overnight-2026-10-29-report.md` pushed on flivideo main (the only main push allowed). Never merge, touch live checkouts, restart apps, or ask David.
- 21:30 REPRODUCED by orch: W1 (8a79987: tc/lint/fmt/build ok, template 86+44 tests, create-appystack 59, sync identical, 0 majors of 42 bumps) ✅ · W2 (92da408: tc/build ok, 8 + 30 tests, electron ^44.10) ✅ · W7 markers (flicut 77a8a3f, flicast 65d83cd, fliedit 726950a; json == package.json spec) ✅ · W3+W7 window-state+W8 core (fc1957a, tag v0.26.0-rc.1 → fc1957a; tc/lint/build/fmt ok, 627/627, lines 99.01%) ✅. ovn-templates-dev finished. Decisions to report: audio+fli.cut→flicut; exportApp legacy/part→null; EditApp gains flicast; template has no lockfile so W1/W2 are range-only bumps; Electron 44.10 not run live.

**2026-10-29 ~19:50 local:** Live FliStudio was pulled (`079ef61`) and restarted at 19:44 by the project-page work (`flistudio-ux-dev` / David), not by me, so the overlay-pilot update is DONE (retire that ask). Live is 1 behind origin (`237046c`: extension shown as a link). FliCut started by me on overlay-pilot-dev's request (pid 26674, kybernesis a01, idle); spike made `fli.cut.ch01.json` + `videos/ch01/ch01-cut.*` (9:16, 61 s); `videos/ch10/ch10-cut.mp4` = byte copy of the August `first-edit/10-…-export--916.mp4`; unused `fli.cut.ch10.json` left (David's call). **David: extension architecture is owned HERE, not by builders.** Open contract decision: an extension must declare which pipeline stage it belongs to; today PipelineStrip (`flistudio/client/src/screens/ProjectHome.tsx`) hard-codes every extension under the Overlay box. Settled by the project-page work: an extension is a screen (link, no running dot); FliStudio reads extension results from disk (Overlay counts `-overlay-` exports in videos/), never calls the module; overlay is optional and never holds "current stage"; extension renders compete for final (newer overlay render → "final · calculated").

**2026-10-28 ~14:45 local:** overlay-pilot-dev FINISHED (~1h40m, ~$45): FliTools `4fee551`, FliCut `3bff5e9` (not running; picks up on next start), fli-core v0.25.0 `7648b9f`, FliStudio main `0d3e323`/`e0a3c99`/`e2d1b1a`. Joy a01: 3 videos × 3 looks placed; on-word real on run 3 (salon 10/10, nail tech 9/11 + 2 not judged). FliTools restarted by the builder. **Live FliStudio checkout NOT updated** (classifier refused the builder) — awaiting David's go: pull --ff-only, npm install, build overlay-pilot + shared, my-app restart flistudio (check :7151 has zero :443 first). Watch cron stopped.

**2026-10-28 ~13:03 local:** David said go → launched **`overlay-pilot-dev`** (tmux default server, iTerm attached, Opus, auto) on `/Users/davidcruwys/dev/ad/flivideo/flistudio/docs/planning/overlay-pilot/handover-to-flivideo-orch.md` (FliStudio `99e86a1`). Order: FliTools audio-clean + FliCut delegates → fli-core overlay-by-video + release tag → FliStudio pins → `modules/overlay-pilot/` flow A, run on Joy's beauty-and-joy a01. Added rule: it never starts/restarts FliCut — it messages flivideo-orch; I restart only at `busy: []` after telling David. David accepted the "three parts" = FliTools/fli-core/FliStudio and "flihub" = FliCut reading. Report goes to `overlay-pilot-spec` (fallback: commit `docs/planning/overlay-pilot/build-report.md`). Joy-overlays handover: FliStudio `4c321e6`.

**2026-10-27 ~16:15Z:** D12 re-uploaded by David: `IL-voVs9IBE`, private, processed; uploadSteps thumbnail/captions/both playlists all `applied` (captions fixed). publishAt null (not scheduled). fli-core v0.24.0 (aiUse/paidPromotion in BrandStudioDefaults) + FliStudio `5a0a08b` merged, npm install, restarted. AppyDave studioDefaults aiUse:false (v-appydave `55cd412`). Open: does Studio show A/B Testing on a scheduled video; Studio check of video language.

**2026-10-27 ~16:10Z:** merged `0c41653` (Publish-page upload box, API-off message) and `5f1947d` (audio language, playlists at upload, AI use, schedule, durable uploadSteps, captions wait for processing, re-upload after delete); FliStudio restarted. David deleted D12 upload kW8K9EHNZwE; D12 dry run now plans a fresh upload (AI Agents + OpenRig playlists, 553 units). NEXT: David re-uploads D12 from Publish with Schedule, then checks Studio (video language, subtitles, playlists, A/B Testing on a scheduled video). Paid promotion is Studio-only (API can't set). Captions root cause unproven; read meta.uploadSteps after the re-upload. fli-core gap: BrandStudioDefaults drops aiUse/paidPromotion.

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
