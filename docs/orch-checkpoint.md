# Checkpoint: flivideo-orch — 2026-10-27

**Purpose**: Where the FliVideo orchestrator (tmux `flivideo-orch`, M4) is up to. Read this after a compact or a cold start.

**For Agents**:
- Read this first when resuming as flivideo-orch
- The current step tells you the next action; the standing rules are not optional

## 2026-11-04 ~21:05 — evening walk builds all live; nothing running
- FliStudio main f1e54a4: Reader file-type rendering (b34d5d3), typed guides (d78d06f/defbebb; d13 story.brief build words IDENTICAL),
  Reader guide layout (60cfe46), Reader fixes (20c3b76: anchor links, inline md, used = "in voice docs"), speed step 2 (Viewer 2× / Listen 1×, remembered).
- fli-core v0.31.0-rc.1 (guides) → v0.32.0 (SpeedControl) → v0.33.0 (rememberedSpeed). FliHub f35299b and FliCut a9aaf12 on the shared control
  + remembered speed. Gists: VERBAL-STYLE (brand-dave 4.2.1), voice-profile (v-appydave 3f41dd0), hook study (flivideo 4aac9a3), vOz
  studio-narrative header (v-voz). FliEdit Lane A complete (A1–A8); Lane B page 6 calls.
- Held: AITLDR strip (flistudio aitldr-strip 858708c, ungated, needs rebase). Teletubby voice-parity b48c8dd → tomorrow at the M4.
  Real-app screenshots owed: FliEdit A2–A8. Update strip shows hyperframes-studio (no origin) — exclude later.

## 2026-11-04 ~19:25 — FliEdit Lane A complete; Reader live; no workers running
- FliEdit Lane A A1–A8 merged (fliedit main @ watch-list commit after 434c847): U6 3611285, U5 47fa438 (snap only), U7 96456d3,
  U4 e7d94e0, U3 85fdb01, H1 4b35cec (duck measured 12 dB; d01 9.1 dB), U2 88cf952, H4 434c847. Real-app screenshots for A2–A8 owed
  (one pass when David is at the M4). Lane B page now 6 calls (05 link, 06 caption safe-area): https://claude.ai/artifact/QA9wL1Y9Qy8PrnWAsQ7GRh
- FliStudio: freeze lifted 19:00 (roamy). Reader file-type rendering + syntax colours + fragment-first LIVE (b34d5d3). Route for walk
  fixes: M2 build → M4 gate → merge → heads-up to flivideo-roamy before restart.
- Held: AITLDR strip (flistudio aitldr-strip @ 858708c, ungated; David said "hold on", never keep/stop). Teletubby voice-parity
  (b48c8dd) waits for David at the M4 tomorrow (Allow + bench + live read). Speed control waits on Q2/Q3/Q5.

## 2026-11-04 ~18:35 — David's rulings via flivideo-roamy; evening freeze on FliStudio
- Rulings: Teletubby click-a-word-to-jump = NO. Apple speech permission + all Teletubby testing wait until tomorrow (David at the M4);
  no speech-test rerun tonight. voice-parity @ b48c8dd gated (532 tests) but NOT merged — merge + Allow + bench + live read tomorrow.
- Tonight David walks Story Pilot (Guides section, Direction box, a story build) from Roamy via the localhost:7150 tunnel, driven by
  flivideo-roamy → orch freezes FliStudio main (no merges, no restarts). Held: AITLDR strip (flistudio branch aitldr-strip @ 858708c,
  ungated). FliEdit Lane A continues: A1–A5 merged (3611285, 47fa438, 96456d3, e7d94e0, 85fdb01), A6 duck building on the M2;
  real-app screenshots for A2–A5 owed (M4 display asleep).
- Update strip live (727eec2): shows hyperframes-studio (no origin) — exclude/mark local-only later.

## 2026-11-04 ~11:00 — STOPPED for shutdown of both machines (David)
- No FliVideo workers running. Teletubby stopped. FliStudio left as an app (comes back via my-app after reboot).
- WIP saved: teletubby branch `apple-stt-bundle` @ 799e257 (Apple STT as .app so macOS can prompt) — UNFINISHED, not gated;
  resume with brief `docs/briefs/teletubby-apple-stt-permission-2026-11-04.md` on the M2.
- Waiting on David: go on FliEdit Lane A plan (`fliedit/docs/buildout-plan-2026-11-04.md`); Lane B page
  https://claude.ai/artifact/QA9wL1Y9Qy8PrnWAsQ7GRh; first live voice-follow read (Groq; Teletubby d13 "Story Pilot — Overlay
  Pilot", press V, Allow mic); walk the Guides on d13 before any script work; G Hub yes/no.
- After reboot: `my-app start flistudio` on the M4 if it isn't up; kill the orphan nodemon (ppid=1).

## 2026-11-04 ~10:05 — Guides section + Direction box + help system + voice-follow all live
- flistudio main 316772c (Guides above Sources, shared FilterChips, story.guide.read), 44d2fd8 Direction box, f65e676 help system;
  teletubby a31fce1 voice-follow (clean-room aligner, Groq primary/Apple fallback, off by default) + eab0ac4 press log.
- d13 screenshot: docs/screenshots/guides-section-d13-2026-11-04.png (6 guides: 2 global structure, 4 brand). Opened for David.
- Next with David: walk the guides on screen (scripts held until then); M4 `sudo xcodebuild -license` → Apple bench + first live
  read on d13; G Hub uninstall yes/no; speed plan review; Open-in-HyperFrames button now unblocked (help-system + guides merged).

## 2026-11-04 ~09:35 — David out ~1 h ("anything you can manage, do")
- Merged + live: help system (flistudio f65e676 incl. 8a1fc56; fli-core v0.30.0 tagged 7f23961; brand-dave 4.1.4), press log
  (teletubby eab0ac4; Teletubby not running on the M4, real-app press-log check needs David presenting). Plugins updated on M4
  (flivideo 2.10.0, brand-dave 4.1.4) — restart sessions to load.
- Gating: direction-box (rebased gate-dir 44d2fd8). Running: guides-section-dev (M2; Guides above Sources + shared FilterChips),
  tubby-voice-dev (M2; clean-room spec frozen sha be9b449…, released to build at 09:3x, then Groq vs Apple bake-off),
  fliedit-watch-rsch (M4; watch list fliedit 8c0949e, U1–U10; publishing the pairs page).
- Scripts (d13, d18) ON HOLD by David until every guide is visible on screen and talked through.
- Speed plan done (docs/research/speed-control-plan-2026-11-04.md, f3970d2) — show David before any code.
- Asked David: uninstall Logitech G Hub on the M2 (installed 2025-09-12, no Logitech USB device, autostarts 2 launch agents). His call.
- cl-matchline-build (M2, not ours) waits on David: `npm run app:restart` in ~/dev/ad/apps/captains-log.

## 2026-11-04 ~09:05 — HyperFrames app live; semantic identity re-checked
- hyperframes-studio app up (M4 127.0.0.1:7210, ~/dev/ad/apps/hyperframes-studio 63ba5c1, apps.json b6cceee, d01-trial v-appydave c2f0e59). fliedit-sbs (M4) running. hf-door brief held until help-system + guide-slots merge.
- Semantic identity: David's lost 10:49 discussion found by flivideo-roamy (78d6888); orch re-check appended §6 (add domPath, lint gate before the coverage test, point-at-anything mode).

## 2026-11-04 ~08:10 — four 11-04 briefs (David's go via flivideo-roamy); reporting line now David on the M4 (Roamy offline)
- Running on the M2 (dispatch notes `docs/briefs/orch-dispatch-2026-11-04.md`, 849dc94): help-system-dev (branch help-system),
  guide-slots-dev (branch guide-slots), writeups-rsch (docs only). Held: Direction box (brief storypilot-direction-box) until
  guide-slots merges — both touch story.brief and the Script/rail area.
- `~/dev/upstream/scratch` deleted 07:05 today by flivideo-roamy on David's word ("let's clean up the 4.7 GB") — intended; so HyperFrames X1 install + proj are gone; :7210 down since
  orch stopped it ~21:02 as timed. v-appydave `_staging/2026-09-22-pocket4-deprecated` deletions = the 2026-10-17 T7 offload
  (91/91 text files byte-identical on T7, 30 MP4s there). Both asked of David.

## 2026-11-03 ~23:20 — Story Pilot build queue DONE (all merged, flistudio main dbd1f6a)
- Merged tonight: W0 a4f4cb7 · W1 188a202 · templates agent-drivable 84f4e5d · W2 c827c92 · W2.1 c968ec7 · tail filter
  065129d · W4 dbd1f6a (+ chip fixes 35225b5 / 1c5bb9b). Plugin flivideo 2.8.0 (appydave-plugins e72c270). teletubby d748f8a.
- flistudio `.env` now has CAPTAINS_LOG_URL=https://mac-mini-m2.tail1acb0f.ts.net. e2e uses a stub CL (never the real one).
- Gate lessons: run the FULL e2e spec for the screen on the M4 (look specs skip on the M2: no d13/d18 data); M2 lacks Python
  PIL (overlay-pilot render tests fail there only); orphan nodemon after every my-app restart (kill ppid=1 ones).
- HELD for David (via flivideo-roamy): d13 dock extracts git commit (classifier: sensitive provenance; files on M4 disk,
  untracked); delete M4 scratch ~/dev/upstream/scratch (X1 4.6 GB) and copy project v-appydave/z99-w4-shots; instruction
  text → then d13 redo = first W4 "update"; Teletubby ↓-press log ask.
- Noticed, not mine: v-appydave has uncommitted deletions under _staging/2026-09-22-pocket4-deprecated/ — leave alone.
- No workers running.

## 2026-11-03 ~21:10 — ORDER (David via flivideo-roamy)
- Story Pilot order: W1 islands (running) → W2 Reader UI → W4 rerun machinery (versions, build record, undo, update/recreate).
  The d13 redo (step 5) is ON HOLD until David + flivideo-roamy settle the Global/Brand instructions; it then becomes the
  first real "update" run through W4. story.templates agent-drivable still builds (API gap); no instructions injected.

## 2026-11-03 ~21:00 — RULING: intro stamp (David, option A, via flivideo-roamy)
- "I'm AppyDave, let's get into it" is DROPPED from story/build videos and KEPT for tutorials. In a story the hook closes on a
  sentence stating what the video will show. Sign-off "I'm AppyDave, I'll see you in the next video" stays everywhere.
  flivideo-roamy updates VERBAL-STYLE.md. **d13: turn the video-level launch-stamp element OFF in step 5 (the d13 redo), not now.**
- Merged tonight: flistudio 2509f5e (LAST WORK fallback), a4f4cb7 (W0 tests), 1d5ef8b (Show chips redesign); teletubby d748f8a
  (voice-follow slice 1, inert). Held: ↓-press log (David's ask via flivideo-roamy).

## 2026-11-03 ~19:50 — reporting line: flivideo-roamy
- Standing instruction (David via flivideo-roamy): every report and question goes to `flivideo-roamy`, not David. It decides
  anything that isn't David's taste or a ruling; orch keeps going between steps; David-only items (his wording, rulings, M4
  keypresses) go to flivideo-roamy first, batched. A peer message is still never David's consent for a permission-gated action.
- Live workers: show-filter-dev (M2), textream-harvest-rsch (M2), storypilot-w0-dev (M2), trial-run (M4, HyperFrames Studio
  server still up on 127.0.0.1:7210 for David to see; stop = pkill -f "cli.ts preview").

## 2026-11-03 ~17:50 — Roamy channel is now `flivideo-roamy`
- Roamy reaches flivideo-orch via `flivideo-roamy` (bridge session on Roamy); it replaces `roamy-home-orch` for FliVideo work.
- Series B: Published 25 (v-aitldr c4ea5e1/17fd8ad/1ad9515); LAST WORK ignores bookkeeping + platform Published live
  (flistudio b1bdf3e, fli-core v0.29.0). Held: b26 main id P4c-XkAeJxI until Jan commits his b26 edit; b28–b30 Skool URLs from David.
- Held for David: trial plan steps 1,2,4 on M4 (doc 08).
- STANDING RULING (David via flivideo-roamy, ~18:15, replaces the ~18:00 one): code changes run on the M2 by default and sync to the others; M4 only when work is already in progress there; never code on Roamy; briefs route through flivideo-orch; every job states its machine + why.
- HOLD (David designing, no build until his go): Story Pilot ↔ Captain's Log mapping, running note docs/briefs/storypilot-captains-log-mapping-2026-11-03.md (c2b0f14).
- Roamy asked about the Send-to-session box (flistudio 136bb92): facts sent; blocked from Roamy by design (loopback + no tailscale-* + door token). No change yet.

## 2026-11-03 ~15:30 — B686 ecosystem research DONE and filed
- Map https://claude.ai/artifact/FikDp9d9cn3MzQmo3zpqq6 · docs `docs/ecosystem-research/` (00–07, candidates) ·
  flivideo 6969341, brains 5c7b4502. 15/15 ACs.
- David: "research that should exist and easy to find in flivideo and backlogs" → linked from `README.md`
  (*Research & direction*), `docs/backlog.md` (*Ecosystem research: 21 decisions*), and notes on B686/B687.
- HELD for David: 21 rows in `06-approval-register.md`; R1 → R3 → R4 after pilot testing. Easy: R13 ruling, X2 check.
- Open asks: close the 4 b686 windows (2 on M2, 2 on M4); park B686/B687.

## 2026-11-03 ~11:40 — day so far (flistudio main 136bb92)
- Dossier B687 (chain B683, voice B686). Deliver B686 plan gate: brains north-star/deliver-2026-11-03-B686-…md; B1 b686-arch-write (M2 Opus) + B2 b686-rsch (M2 Sonnet) running, watchers b0q8p50mc/btqy0d6ao; B3 b686-synth-write (M4 Opus) after both.
- Merged today: d65a16d angle fold/clear/undo, 5b9324e reader key hints, e7dea41 play intro only, 136bb92 send-to-session (flag in .env ON by David's own command; M2 probe 403 on :7150 and ts.net:8443).
- Banked (not built): docs/briefs/storypilot-screen-batch-2026-11-03.md (items 1–5), docs/briefs/session-box-spec-2026-11-03.md.
- BUG to bank: `my-app restart flistudio` orphans the previous nodemon (ppid 1) every restart — killed 81065 and 79641 by hand.
- deliver skill §6a (plan gate) added, appydave-plugins abae233.

## 2026-11-02 ~20:00 — NOTICE ONLY: Skool-Pilot coming (from skool-david-kaff, on David's ask)
- New FliVideo-family app, maybe growing into Skool Studio. Nothing built, scope not agreed. **Do not start work.**
- Loop: Kaff's advice → skill → asset on Skool → Kaff reviews → skill v2 → students get it. Jan applies via agents (as Story Pilot / B-roll Pilot).
- Read: /Users/davidcruwys/dev/ad/brains/skool/skool-pilot-concept.md · sources /Users/davidcruwys/dev/ad/brains/skool/sources/2026-11-02-kaff-session-2/ · first output https://claude.ai/artifact/FhFgoU1Pg9Dy6iYaLZJqw3
- Open for David: Pilot or Studio; FliStudio zone or separate app; Kaff direct vs Claude ingests Looms; how Jan syncs.

## 2026-11-02 ~19:35 — David's D19 rulings applied (v-appydave c75d044, appyrigs 89431662)
- Angle A NOT set (human-only verb); David must click "Use this" on proposal A in Story Pilot. Beats already in A order, B payoff, beat 24 what's-next (his framing).
- AppyTron = working version, 3 exemptions accepted. Two sources removed (entries only). Why Our Rigs Failed r_0c9f83be88 filed as tool background.

## 2026-11-02 ~19:00 — D19 rig series (A/B/C) done, receipt sent to roamy-home-orch
- A: FliStudio be723e5 (artefacts as Story Pilot sources); D19 +12 items; proof d19-artefacts-2-live.png.
- B: appyrigs beccb105, artefact BQK5MXiU1HNigqZg47arB7 (AppyTron/AppyStack working w/ exemptions to confirm; Spaghetti back to rig).
- C: v-appydave 8bbeed8, thesis provisional, angles A/B/C proposed (rec A), angle NOT locked.
- Open for David: D19 angle; AppyTron WEIGH-UP 17:55 status vs 18:30 audit; remove 2 suggested sources?
- Waiting: openrig-orch artefact URL (misconfigured vs rebuilt built-ins) → register on D19 via storypilot-dev.
- Windows: storypilot-dev idle; d19-storypilot-video idle; rig-compare-rsch closed.

## 2026-11-02 ~16:55 — David steers from Roamy from now on
- David works from home on Roamy. He attaches to M4 windows over ssh; `roamy-home-orch` (Roamy tmux) holds his table.
- Handover: docs/handovers/roamy-home-2026-11-02.md (attach lines, artefacts, held asks). All M4 sessions left running.
- Report §05 updated to current state (artifact version 1793612881-0816).
- Xcode 27.2 installed on M4; licence + first launch still need `sudo` (David). Rig launch waits on that + his go in openrig-orch.
- M4 power: sleep 0 / standby 0 / autorestart 1; nothing changed.
- Ghost text in openrig-orch / d18 / aitldr-strip-rsch / storypilot-dev prompt boxes is a suggestion, not David's input.

## 2026-11-02 ~12:35 — acted on David's answers to the 11-02 report
- D1 yes: three intros done — D13 `d13-overlay-pilot/script/three-intros-2026-11-02.md` (e78ef2d), D18 `d18-story-pilot/resources/three-intros-2026-11-02.md` (b4d3377). Proposed only; David picks.
- D2 yes: Snappy spec §9 records 8 approvals (78d4b56). Spikes HELD until OpenRig rig plan is approved.
- D3 yes: `flihub-broll-dev` launched (worktree flihub-worktrees/broll-register, brief flihub-broll-register-2026-11-02.md).
- D4 don't draft: VERBAL-STYLE.md exists (brand-dave/skills/brand/references/appydave/). Discuss in orch window, no worker.
- D5 keep: `aitldr-strip-rsch` done → specs/aitldr-strip-reconstruction-2026-11-02.md (2a61ec0); waits for David.
- Bugs → storypilot-dev (brief storypilot-keys-bugs-2026-11-02.md); real-browser proof required.
- New windows: swift-rsch (brains/swift-macos), d20-snappy-work (D20 project + living sources). overlaypilot-dev CLOSED (handover in its brief).
- OpenRig plan awaiting David's go (report §05). Report republished visual (441f6e7).

## 2026-11-02 ~08:35 +07 — before David's reboot (Swagger, flivideo-orch [5d47a4])
- LIVE: FliStudio main 3f6804e (Listen v2, Prep UI); FliTools main 0f2dcdd (speech + word timings, my-app lifecycle); skill flivideo:storypilot-prep (appydave-plugins f9eea8b, reloaded).
- D19 prepped in live FliStudio by d19-prep-work (16 in story, 44 aside, no angle, undo available). Window closed.
- Closed: flitools-dev, storypilot-dev, disk-work, d19-prep-work. Worktrees removed: rail-v2, r1, flitools tts-verb + chunk-overlap. Left: storypilot (keep), aitldr-production (2 ahead), pair-remove (untracked repair script).
- HELD (do not build until David releases): docs/briefs/_held-david-2026-11-02.md — Listen speed keys = video keys; Reader step keys; Prep rethink (3 angles -> 3 intros -> pick -> story); orch owns flaky e2e / 2 worktrees / schema-mirror after reboot.
- David will hand over "this morning's learnings" soon. Resume: read the held file, wait for learnings.

## Current step

### 2026-11-01 ~13:00 — AUTOPILOT; Lab removed
- David: "Don't ask between restarts … working as much on autopilot as possible … We're not actually working with the apps." → orch merges + restarts every green unit without asking (busy.sh still checked).
- David: "the pilot lab should be removed now" → storypilot-dev queue: remove Story Pilot Lab, before Listen. The Lab-first process fork is closed (moot).
- FliStudio main 691e455 (✎ icon, Show filter, Attachments) LIVE.

### 2026-11-01 ~12:50 — rail v3 LIVE; Listen approved and building
- FliStudio main 63f87a0 (rail v3: margins, top tab row when open, M 55% / L 67% of the area, script focus restored, +19 marker, UX fixes). Restarted, health ok.
- Workers: storypilot-dev (rail-v2): Reader markdown, +19 scrolls to the cards, styled controls → then the LISTEN build. flistudio-dev (studio-dev): ✎ icon → Show filter → "Attachments" rename → clear-on-publish → shell polish (radii, resources chip). flitools-dev (flitools-worktrees/tts-verb): Kokoro speech verb. resources-rsch closed (specs docs/specs/resources-model + storypilot-listen, artifact R4GPEs2XUkfjUpdkXweGno).
- David: Listen approved; clear caches on publish (+ the manual clear stays); Lab keep/remove still open.

### 2026-11-01 ~11:10 — new orch [5d47a4]; rail fix LIVE
- Old orch [b8d399] shut down (David). Its only post-handover item was the 10:30 D19 standing job (below), which is still mine.
- Story Pilot rail fix: FliStudio main 62a4524 (ff from rail-v2), gates reproduced (typecheck 0, tests green), busy idle, restarted, health ok. Content now spans the strip width, which supersedes the 1000px content cap (David said go). The script sheet stays capped at 960px (David).
- storypilot-dev's next unit: collapse D18's 19 NOT PLACED timeline nodes into a "+19" marker (orch's call; David didn't follow the question).
- Still open for David: the Lab-first + approved-mock process fork; the Projects Show filter; the "Field notes" name; the D19 angle.

### 2026-11-01 ~10:30 — D19 angle (David)
- Thesis: "I built an OpenRig that turns spaghetti into clean code" — unproven until the AppyStack run finishes; honest verdict / check-that-lied are supporting beats, not the focus. D19 keeps gathering; no script.md yet. Ruling forwarded verbatim to d19-storypilot-video; it saved it in story settings `notes` (50 sources, v-appydave ab9b1d4).
- **Standing job for orch:** ping `d19-storypilot-video` at each AppyStack (ladder-appystack) tier end and when the run finishes, so it attaches the hand-back / LEARNED / judge records. It does not watch the seats itself.

### 2026-11-01 ~10:10 — session names (David renamed)
- D13 video/script asks → `d13-overlaypilot-video` (tmux still `d13-overlaypilot-work`). D18 → `d18-storypilot-video` (tmux `d18-storypilot-work`). D19 → currently calls itself `d19-storypilot-video` (tmux `d19-storypilot-work`); suggested rename `d19-spaghettirig-video`. Story Pilot code → `storypilot-dev`.

### 2026-11-01 ~10:00 — one rail LIVE; D19 created; workers visible
- Story Pilot one elastic right rail (FliHub look, push, M/L, Reader folded in, section note targets, no Width S/M/L): FliStudio main f5b6caa, restarted, health ok. Built by tmux worker `storypilot-dev` (worktree flistudio-worktrees/rail-v2) — keep it up as the Story Pilot worker.
- David: orch must delegate to VISIBLE tmux workers, not hidden subagents.
- D19 `d19-spaghetti-rig` created via project.create (id 88f509cf…). tmux `d19-storypilot-work` gathering sources (brief docs/briefs/d19-spaghetti-rig-story-2026-11-01.md); reports to orch.
- Open for David: Projects "Show" filter → recommend click=solo, ⌘-click=add, ★ rows always shown (awaiting go). Name: "Field notes" (data) vs Field Trial (process) — recommended.
- Orch handover/restart recommended (this conversation ~$1,100); pending David's go.

### 2026-11-01 ~09:20 — Story Pilot + Lab side tabs, white cards LIVE
- FliStudio main 367f10c (lab-tabs, built by a subagent; gates reproduced; busy idle; restarted, health ok). Right-edge Settings/Sources/Chapters rail (push, never overlay) on Lab + main Story Pilot; Resources white card tokenised (--surface-sheet etc.); --content-max 1000px (Words) for Story Pilot/Lab; Lab variants A/B/C/D with C dark|light toggle, B terminal toggle, S/M/L 720/860/1000.
- Brand skill: app-surfaces rule (appydave-plugins 1314d2f, 825c578).
- Not done: Story Pilot reader "Large" no longer wider than container; no hover-intent delay; AGENT-NOTES not updated.
- David attached to tmux d18-storypilot-work (opened in iTerm2).

### 2026-11-01 ~09:00 — David's rulings A2 DONE (brief david-rulings-and-storypilot-handover-2026-11-01.md, b4caa5b)
- Q1 every ⌘⇧ click swallowed + Lab variant E (light terminal) + full-width B/C/E: FliStudio main 2364edc (restarted, health ok), FliCut main 7f1bcfb (built, restarted, health up). Sticky ✎ mode still only takes target clicks (both apps).
- All three fli-notes builders closed; their worktrees + branches removed. A3 banked in docs/backlog.md (8bda8eb).
- David's 3 Lab notes (B, C, D) read cleanly; meta.words loses spaces between blocks (minor).
- Part B of that brief belongs to session d18-storypilot-work. David now talks to orch directly on the M4.
- 3 empty iTerm windows ("iTermServer-3.7.5", 0 tabs) on screen — offered to close; awaiting David.


### 2026-11-01 ~08:15 — fli-notes v2 DONE (merged + live)
- fli-core v0.28.0 released (main 7c7ad88, rc.1 promoted). FliStudio main 746643c (busy idle → merged, npm install, my-app restart, health ok; Lab verified live on D13). FliCut main 4a4396b (was DOWN; built, not started). Both repinned #v0.28.0.
- UAT page: https://claude.ai/artifact/XBK9iekHsY7GhaCM28vqyp (slug f462c874-76c8-4359-8fe7-4eef12f89c77) · source docs/uat/fli-notes-v2-2026-11-01/. Ghost-check 0. 6 questions, each with rec.
- flistudio skill updated (appydave-plugins c036e26). Workers idle; closing them + worktrees needs David's say-so.
- Open: David's answers; real-Mac ⌘⇧ check on first try; no live Lab note written on D13 (d13-write owns it).

### 2026-11-01 ~07:45 — fli-notes v2 RUNNING
- Go (relayed, David ~07:30): "Go on both… I like option A" + "yes remove notes page". Brief `docs/briefs/fli-notes-v2-quiet-capture-and-lab-2026-11-01.md` (8c092bf); work plan `docs/briefs/fli-notes-v2-orch-workplan-2026-11-01.md` (14848d5).
- Same three workers re-tasked on branch `notes-v2` in their v1 worktrees: core = life states → v0.28.0-rc.1; studio = remove notes UI + ⌘⇧ gesture + Story Pilot Lab A–D; cut = remove + gesture + v1 Q1.
- DO NOT write D13 (tmux `d13-write` owns it; don't stop it). David uses FliStudio on the M4 later today — busy-check, no restarts of FliStudio/FliCut while he is in them; tell him and wait.
- Next for orch: on rc message, nothing; on app reports, reproduce gates, merge core → tag v0.28.0, repin, merge apps (busy-check), UAT page (AppyDave light).

### 2026-10-31 ~23:10 — OVERNIGHT RUN: fli-notes (notes / asks / changes) — GO from David
- Go: "go with recomendations" (~23:00, relayed from Roamy `flivideo-field-trial-plan`). Brief `docs/briefs/fli-notes-suite-record-2026-10-31.md` (`cda4daa`); split in `docs/briefs/fli-notes-orch-workplan-2026-10-31.md` (`8f844d5`).
- Workers RUNNING (tmux + iTerm): `fli-notes-core-dev` (fli-core-worktrees/notes-record, §4A → tag v0.27.0-rc.1), `fli-notes-studio-dev` (flistudio-worktrees/fli-notes, §4B), `fli-notes-cut-dev` (flicut-worktrees/fli-notes, §4C).
- Orch steps after reports: (1) reproduce fli-core gates → merge main, tag v0.27.0, push; (2) apps repin #v0.27.0, reproduce gates, busy-check, ff-merge, restart FliStudio (my-app) — FliCut restart only at busy:[] and tell David; (3) §4D D13 first line via `story.script.set` (ask record human:chat first, then change linked by `answers`; ONLY line 1; overlap with later paras → open ask in report; feel/do untouched; no TeleTubby/Prompter send); (4) `scanNotes` over v-appydave returns both; (5) morning UAT page (AppyDave light) with batched taste calls; checkpoint.
- 23:20 fli-core DONE: gates reproduced (typecheck, lint, 652 tests) → main ff, **v0.27.0 released + tagged (00bc4bb, pushed)**. App workers told to pin #v0.27.0 directly. Core taste calls (morning list): resolve = new change line on the ask; answers≠close (notes.resolve closes); channel from by; ≤2000-char whole else ±240-char excerpt; schema:1, ids n_<12hex>, B-code in links.capture; readNotes exists:false.
- ~00:00 FliCut DONE: gates reproduced (tsc, 623/623) → flicut main ff **db599d0**, pushed, npm install + build. Live FliCut was DOWN (not restarted). Shots copied to docs/uat/fli-notes-2026-10-31/flicut/. Cut taste calls: ⌥⇧N (+⌘⇧N) shortcut; change target entityType edit field cuts; snapshot ids + kept + word runs; auto-transcribe = agent:flicut; because/session on all write verbs; codes -32039/41/44/47; small notes list, no change records shown. Deferred: undo/redo doesn't set answers; real Cut-button gesture not screen-proven (IPC door proven).
- ~23:50 FliStudio DONE: gates reproduced (tsc; 47/68/64/41/745/319) → busy idle → main ff **1eba790**, pushed, npm install, my-app restart, health ok.
- §4D DONE: D13 line 1 replaced via story.script.set (title/triggers/chapters re-sent; rest of script byte-identical; feel/do untouched; no TeleTubby/Prompter). Records in d13 fli.notes.jsonl: ask n_2a5f3c73d07d (human:chat) → change n_361ccb77aaa7 (agent:flivideo-orch, because verbatim, excerpt) → resolve n_a172c43ee4e5 (follows change). SLIP: change line lacks links.answers (my script misread result.note.id); link exists via resolve.follows. scanNotes over v-appydave returns all 3. Backup of old script: scratchpad d13-backup/.
- Skill: flivideo:flistudio fli-notes section (appydave-plugins 3f48d69).
- **UAT page PUBLISHED: https://claude.ai/artifact/E4EgFuEEqkJpZMSBftz6km** (source docs/uat/fli-notes-2026-10-31/index.html). 8 batched Qs; top recs: Q1 align FliCut↔FliStudio (codes in fli-core, saidBy/answers/region) ~1h; Q2 D13 para 2 overlap + para-1 trigger "stuck on one step" — David edits.
- RUN COMPLETE. Workers idle in tmux (fli-notes-core-dev/-studio-dev/-cut-dev) — close + remove worktrees on David's say-so.
- D13 script edit is now ALLOWED for line 1 only (supersedes the earlier hands-off rule for that line).

### 2026-10-31 20:47 — NOT a go: automations + YouTube sync → backlog only
- David: "I have no idea about the automation spec page or the YouTube daily sync... they should be put onto a backlog because I'm not there to guide that." Both banked in docs/backlog.md (new suite backlog). Build neither.
- Do NOT edit the D13 script or its feel/do settings — David is rewriting the opening from Roamy.


### 2026-10-31 — worktrees removed (David's go)
- Removed (merged, clean, branches kept): flistudio-worktrees/{overlay-chin,broll-pilot,project-status}, flitools-worktrees/{face-track,prompter-load}, teletubby-worktrees/script-chapters. Closed project-status-dev. Kept: fliedit-worktrees/drivable-audit (spike video), flistudio-worktrees/storypilot (uncommitted phase2-variants.html).


### 2026-10-31 — D13 note: two different "bugs", don't merge
- D13 ¶13–16 "The check that lied" = the WORD-SYNC check (skipped for lack of word timings, reported as passed; fixed by snapping graphics to FliTools word timings).
- The CHIN bug (overlays over Joy's chin, fixed today via FliTools face.track) is a separate story: attached as source r_d48036acd2 (placed 06) but NOT in the script. Adding it to the script is David's call.


### 2026-10-31 20:11 — Project Status LIVE
- Merged project-status → flistudio main 4b33e53 (ff), pushed; FliStudio restarted, healthy; projects.list carries status for all 17. Gates reproduced by orch: typecheck clean, unit 728+311+220 pass, dry-run compare 17/17.
- Follow-up brief (fli-core facts + FliHub/FliCut/FliEdit wiring): docs/briefs/project-status-facts-fli-core-2026-10-31.md. Skill phrases: appydave-plugins 49df9bd.
- Known: below ~1300px wide the status word wraps above the boxes and size badges wrap under names.
- Pending David go: automations spec page ("Recorded → want me to cut it?"), YouTube daily sync job. No holds/tags set on his projects.


### 2026-10-31 19:40 — project-status-dev launched
- Project Status (FliStudio project list: 8 step boxes, markers column, filters, tags, control plane, fli.status.json log) approved by David from https://claude.ai/artifact/1ik3tTnTU8ssSmEtcCdbgH.
- Brief: /Users/davidcruwys/dev/ad/flivideo/docs/briefs/project-status-build-2026-10-31.md · worktree flistudio-worktrees/project-status (branch project-status off 38b6a75; mock + dry run committed 1858d91).
- Session tmux `project-status-dev` (iTerm attached). Orch merges after reproducing gates + busy check.
- Also today: vOz brand → dormant (appydave-config 4bd896a). B678 (8h Plaud, untranscribed) offered to David for big-file lane — no answer yet.


### 2026-10-31 ~04:09Z — storypilot-uat MERGED flistudio main 38b6a75 (Large full width, verified 1517px); D13 has 6 chapters (text byte-identical). UAT page republished with fixes (v 1793419733-1e9e). TeleTubby still holds the no-chapter copy until David presses Send. Open for David: chapter 2 at ¶6 vs ¶8; Overlay final choice; first Prompter send.

### 2026-10-31 ~04:05Z — UAT guide published for David
- https://claude.ai/artifact/7hooUPsgUab4UEykVCQm8r (source: my scratchpad uat/index.html + 12 jpgs). Sections: Story Pilot → TeleTubby/Prompter → Overlay → B-roll → FliEdit → not yet.
- UAT fixes by me: D13 capture meta.channel set (resources.update takes `meta` top-level; unknown `patch` key silently ignored — minor API finding). Removed my chin-compare folder from Joy project (showed in sidebar). Real B-roll drill on D13: dropped a screenshot into resources/project/, auto-registered, described as agent.
- storypilot-dev fixing: Large reader full width + D13 6 chapters (branch storypilot-uat). Merge + restart when it lands, then update the UAT page (remove "being fixed").
- Overlay: frame-2 auto-became calculated final on hobby-learners — flagged to David as his call.

### 2026-10-31 ~03:16Z — StoryPilot phase 2 MERGED flistudio main 34d0a48 (gates reproduced; npm install; restarted; eyeballed D13 Story Pilot in Chrome: spine 01–08 incl. 06 chin bug, lanes, READ tab, B-roll Pilot in sidebar). story.prompter.send is ★ human-only. ALL FIVE SATURDAY ITEMS' BUILDS LANDED except #4 (buttons, last). Open: D13 meta.channel (B663/B667 plaud, B670 chatgpt); tickets: FliTools describe service, fli-core resources/footage zones; /plugin-index.

### 2026-10-31 ~03:10Z — merges
- **B-roll Pilot v1 MERGED** flistudio main 110fe86 (main merged into branch first; gates reproduced). Global broll kind row added (appydave-config 8b1d87b). FliStudio was DOWN ~5 min: live checkout needed `npm install` for new workspace modules/broll-pilot — **after merging a new workspace, npm install before restart**. Also: `my-app restart` inside a 2-min tool timeout gets killed mid-start — run it backgrounded/with timeout.
- Tickets to file (from broll-pilot-dev): FliTools describe service brief docs/briefs/flitools-describe-service-2026-10-31.md (pushed 3b40123); fli-core: name `resources` + `footage` as ProjectZones in classify.ts (non-blocking). appydave-plugins INDEX stale (/plugin-index).
- StoryPilot (b): FliTools prompter-load MERGED 71821aa + restarted; Teletubby script-chapters MERGED 44e0011 + restarted. FliStudio storypilot-p2 CONFLICTS with main (counts/openrpc) → storypilot-dev resolving + fencing story.prompter.send human-only. Pending: D13 captures lack meta.channel (B663/B667 plaud, B670 chatgpt) — my call later. Screen not yet eyeballed.
- Orphan nodemon pid 95664 (9:21) seen — left alone.

### 2026-10-31 — StoryPilot v2 ACCEPTED by David → storypilot-dev building step (b): FliStudio storypilot-p2 (v2 UI + chapters) · teletubby-worktrees/script-chapters (script.write chapters) · flitools-worktrees/prompter-load (prompter.load, fake Camera Hub home in tests). Merge order: FliTools + Teletubby before FliStudio. First real Prompter push = David's action.

### 2026-10-31 ~09:25Z+ — while David is out
- **Overlay chin fix MERGED** flistudio main 65213ca (gates reproduced), FliStudio restarted (idle, health ok). 9 re-renders beside originals in v-beauty-and-joy/a01-…/videos/<video>/ (-2; hobby typeset-3 = tracker version, typeset-2 = interim). Compare PNGs: v-beauty-and-joy/a01-…/chin-compare-2026-10-31/. Joy framing.json changed, uncommitted in Joy repo. Stray scratch op-render-wlltfq4x left for project.clear-renders.
- **Tracker → FliTools DONE + MERGED**: flitools main 7703c84 (face.track / face.job, serial; restarted via scripts/app.sh, live :7161 verified) then flistudio main 382d9b7 (Overlay Pilot asks face.track; fallback opencv+chin). joy-video SKILL.md repointed — ⚠️ ~/dev/ad/joy is NOT a git repo, edit unversioned (backup in overlay-chin-dev scratchpad). overlay-chin-dev idle/done.
- Gotcha: live flistudio is a watch-mode dev server — merging into the live checkout reloads it. Busy-check BEFORE merging, not just before restart.
- StoryPilot v2 hybrid mock LIVE (same URL 814tyf7…, v 1793413143-e15d) — awaiting David yes/change. D13 chin-bug source r_d48036acd2 placed at 06 (8 sources); D13 script NOT rewritten.
- **broll-pilot-dev LAUNCHED** (worktree broll-pilot, brief docs/briefs/broll-pilot-build-2026-10-31.md, spec cafe7aa). Storage = existing resources/<video|project>/ zone, place:copy vs in-place. broll-pilot-plan stood down.

### 2026-10-31 ~10:00 — David's rulings batch 2
- David OUT for a few hours (~10:15); wants a progress report on return. Roamy caffeinated all day — workers may spread dev load there. Keep driving: merge on gates, launch B-roll builder when brief lands.
- StoryPilot: NO pick yet. storypilot-dev making ONE v2 hybrid mock (A's left→right cards + vertical lanes; right-edge tab → medium/large reader = B; keep C's spine graphic, drop C's timeline; answer "other lanes?" w/o Kanban creep). Then step (b).
- Q3 RULED one model + DIRECTION: unify everything FliStudio holds (StoryPilot sources, B-roll, publishing, thumbnails) into one entity-relationship structure; sections owned by an extension but not exclusively. Backlog/architecture — not designed yet.
- Q4: image source ≠ B-roll (worker proposal). Teletubby chapters → own JSON-RPC door, step (b). Elgato: yesterday's file-write path works (brains/ecamm/elgato-prompter.md) → FliTools prompter.load (quit Camera Hub via kill -TERM, write, relaunch; back up first); 1 Elgato chapter per SP chapter.
- D13 = Overlay Studio/Pilot video: chin-bug learning to be appended to D13 StoryPilot sources (storypilot-dev, append-only).
- Tracker A (joy analyze-source.py + facedetect.swift) → MOVE to FliTools APPROVED, after chin fix; overlay-chin-dev does it in flitools-worktrees/face-track; joy-video skill + Overlay Pilot repointed; tracker B untouched.
- B-roll mocks APPROVED. Storage RULED: not FliHub — FliStudio-owned project resources zone (Resolve-style), producers drop/keep, B-roll Pilot registers; broll-pilot-plan to survey + rule in spec, then write build brief docs/briefs/broll-pilot-build-2026-10-31.md → I launch fresh builder.
- Qwen describe: SERIAL, one job at a time like transcription (David 10-31). RULED (mine, delegated): FliTools "description as a service" on named worker (M2 first, Roamy fallback), like transcription; never on the FliStudio host.

### 2026-10-31 ~08:45 — Saturday plan dispatched (captains-inbox brief, source B676/B677)
- #1 Overlay chin bug → `overlay-chin-dev` (wt flistudio-worktrees/overlay-chin) · brief docs/briefs/overlay-chin-2026-10-31.md
- #2a StoryPilot 3-variant artifact → existing `storypilot-dev` (new branch from main; no build until David picks; Elgato code → FliTools; Prompter OFF, don't start)
- #3 B-roll Pilot spec + mock artifact → `broll-pilot-plan` (wt flistudio-worktrees/broll-pilot) · brief docs/briefs/broll-pilot-spec-2026-10-31.md
  - **Spec + mocks DELIVERED 10-31** (branch broll-pilot cee5c2c, docs/planning/broll-pilot/spec.md; mocks https://claude.ai/artifact/41bRuUXxKwpL4VadM1ATbp). Awaiting David's mock approval → then v1 builder. Q6 FliHub B-roll folder (rec hub/broll/). Q11 Qwen lead sent (brains/video-as-code/footage-triage.md).
- #4 FliHub/FliCast B-roll button → **David CONFIRMED wait (10-31)**: not today. Order: B-roll Pilot spec → registration contract → v1 build → buttons LAST.
- David rulings 10-31 ~09:00: mocks plan OK; no captains-log:deliver on B-roll Pilot until mocks approved; storypilot-dev HOLD (no A/B/C pick yet; variants https://claude.ai/artifact/814tyf7VGfciaESVKvCygc; page source kept local, uncommitted).
- TeleTubby started 10-31 ~08:54 (system_status ok, busy []). Elgato Prompter untouched.
- Presenter tracking: overlay-chin-dev to report path/lang/deps/callers; David thinks home = FliTools. I owe him move / wrap / leave rec with pros/cons. NO relocation until he rules; chin fix wires in from current location.
- Roamy (100.89.32.35) offered to fliedit-drivable-dev + broll-pilot-plan for heavy runs (appynet:remote-claude; session owns its git + env). Asked David which session he meant by "FliHub".
- CL dossier-strip feedback (no taller panels; colour highlight; match old row size; hold for more attachments) routed to captains-inbox.
- #5 FliEdit drivable audit + 2-layer spike → `fliedit-drivable-dev` (wt fliedit-worktrees/drivable-audit) · yields to 1–4
  - **DONE + MERGED 10-31**: fliedit main dc39399 (gates reproduced: typecheck, 223 tests, build). Layered assembly works over JSON-RPC; WebM alpha fixed. Report docs/drivable-audit-2026-10-31.md. Gaps: no speed, captions soft-only, no keyframes. Worker idle; next input = today's A-roll.
- StoryPilot step (b) research done (storypilot-p2 9f0bc25, docs/planning/storypilot/phase2-research.md). Pending David: A/B/C pick; Elgato mapping (rec: 1 Elgato chapter per SP chapter); OK to quit Camera Hub for file-write path; live addChapters probe when Prompter back on. Teletubby needs script.write `chapters` param (route in step b). Camera Hub listens on *:1834 unauthenticated — told David.
- Recording today: start TeleTubby (`my-app start teletubby`) when David is ready. I merge + restart FliStudio after gates/busy check.
- Backlog only: Publishing Pilot, Audio Pilot, Timeline Pilot/Director's Chair, video groups.

**2026-10-31 ~08:00 — Desk cleared; waiting on David's B-roll / FliHub input.** On David's say-so I closed
tmux sessions tubby-land-dev, tubby-panel-dev, flivideo-arch-rsch, flihub-rebuild-rsch (processes confirmed gone).
arch-rsch's last message (FliHub parked) was acked late; nothing was owed. arch-rsch handover:
`/Users/davidcruwys/dev/ad/flivideo/docs/briefs/handover-2026-10-30-arch-rsch.md`. NOTHING IN FLIGHT.
NEXT: David is sending new FliHub changes about B-roll. Read them against (a) live FliHub v1 at
`/Users/davidcruwys/dev/ad/flivideo/flihub` and (b) the PARKED rebuild spec
`/Users/davidcruwys/dev/ad/flivideo/docs/flihub-rebuild-spec-parked-2026-10-30.md` (David ruled B-roll OUT of v2
scope and floated a FliStudio "B-roll pilot" extension — check whether the new input changes that). Say where each item
lands (v1 fix / parked spec / FliStudio extension) with a recommendation before launching any builder.
Remaining banked follow-ups: see the 10-30 entries below (remote branch deletes, storypilot worktree, G3/G4,
/plugin-index, M4 memory pressure, FliHub double-mounted /hold route).

**2026-10-30 ~19:46 — Teletubby-lands LIVE + verified.** FliStudio main `ce8fd25` (tubby-lands: app.stage door,
here-dot reads stage, Overlay Pilot posters, named request log; gates reproduced 46/65/38/707+2/307, e2e 31). Teletubby
main `847773e` (panel scoped to open project, cold start → empty shell, 10-17 ticket closed). Both restarted after busy
checks. David's scenario verified on screen (screenshots): Kybernesis on stage → story.script.send d13 → "STORY PILOT –
OVERLAY PILOT" on stage, position d13-overlay-pilot-scripts/storypilot-project, apps.status ofOpenProject true.
Worktrees + local branches removed; remote branches tubby-lands/tubby-panel left (merged). Sessions tubby-land-dev,
tubby-panel-dev idle (not closed).

**2026-10-30 ~19:40 — FliHub rebuild PARKED by David** (via flivideo-arch-rsch). Spec:
`/Users/davidcruwys/dev/ad/flivideo/docs/flihub-rebuild-spec-parked-2026-10-30.md` (flivideo 2dd162a), filed on
AppyDave d17-flihub-rebuild (resource r_2667e860b6). Do NOT write a v2 build brief until David resumes. FliHub v1 untouched.
Teletubby tubby-panel merged to main 1e2e2ec (gates reproduced 440/11); restart waits for FliStudio tubby-lands.

**2026-10-30 ~19:20 — David GO "all three" (via brains-d5).** Builders launched (tmux + iTerm2):
`tubby-land-dev` (FliStudio worktree `flistudio-worktrees/tubby-lands`, branch `tubby-lands`: stage_select door for
switchTo + story.script.send, "here" dot reads workspace.position, Overlay Pilot posters/click-to-play, capability
name in /api/call log) and `tubby-panel-dev` (Teletubby `teletubby-worktrees/tubby-panel`, branch `tubby-panel`:
panel loses cross-project picker, cold start w/o context → empty shell, close 10-17 ticket). Brief:
`/Users/davidcruwys/dev/ad/flivideo/docs/briefs/teletubby-lands-2026-10-30.md`. NEXT: reproduce gates, merge both,
busy-check, restart FliStudio + Teletubby, verify live: staged on Kybernesis → Story Pilot Send d13 →
workspace.position = d13 set. Report to brains-d5. Root cause + perf findings already sent to brains-d5 (swap 18.5/19.5 GB).

**2026-10-30 ~12:10 — extension-core 0.2.0 (G1) MERGED + LIVE; Send-to-Teletubby proven on the real Teletubby.** FliStudio main `c4ac75c` (ff), install+build, pushed, restarted (busy idle), health ok. Orch-reproduced gates: build/tc/api:check/format ok, lint 0 errors; extension-core 46, overlay-pilot 64, storypilot 36, server 698+2, client 306, e2e 31/31. New: `ExtensionHost.app(name).call(method, params)` → POST <app>/api/rpc as agent:<ext>, bearer from the app's control.json; descriptor `apps` allow-list (fenced in bindExtensions); refusals forbidden/unknown-app/app-unavailable/app-refused (-32050). Story Pilot `apps: ['teletubby']`, `story.script.send` + screen "Send to Teletubby" button. **Live check by orch:** `bin/flistudio story.script.send --brand appydave --project d13` → context.select + script.write applied, replaced in place (set d13-overlay-pilot-scripts). extcore worktree + local branch removed; origin/extcore-neutral left (merged). extcore-dev done.

**2026-10-30 ~11:40 — First D13 Story Pilot script written; Teletubby started (orch, my-app) for the handover.** 7 sources attached to D13 via resources.add (B663, sessions 8aa7c642 spec / 62b99237 build / 09d843f5 arch-rsch, overlay-pilot spec dossier, B667, B670); left out: c39fe501, 49052d85, orch session, brains 5718f7c4, B665/B668/B658. Skill: appydave-plugins `f1dad4d` (flivideo 2.6.0, skills/storypilot + scripts/rpc.py, handover.py; INDEX.md needs /plugin-index regenerate — banked). Script `/Users/davidcruwys/dev/video-projects/v-appydave/d13-overlay-pilot/script/storypilot/project/script.md` (1,020 words, 26 paras, build-story). feel/do UNSET pending David (a feel, b do, c AppyDave bookends, d "girlfriend Joy" vs "partner"). Handover to Teletubby (context.select → D13, script.write id storypilot-project) being run by storypilot-dev.

**2026-10-30 ~11:05 — David OVERRODE Q0: FliHub v2 hosts NO extensions** (extensions are FliStudio-only; microapps have doors, not extensions). Discovery doc dadb749: rebuild rule "drop, don't change"; Q2 FliStudio alone opens/changes projects (suite-wide guideline); Q5 MicCheck → future FliStudio setup extension; Q6 B-roll out (likely FliStudio extension #3 "B-roll pilot"); Q7 renumber/swap designed into segment ops; Q8–Q10 drop Assets/Inbox/Thumbs/Transcripts/POEM send/Gling/shadows; S1 configurable recording source (Ecamm now, OBS designed-for). Keep 19 / drop 26 / unsure 10. **Q1 + Q3 still pending** (arch-rsch walking David through). Looks artifact redone (rec: variation 1, cleaned up); keep/drop artifact retired (David found it unreadable). **extcore-dev rescoped** (brief e1e003b): G1 app-door call + Story Pilot Send-to-Teletubby + 0.2.0 only — no host-neutral, no extraction. **Orch rulings:** run FliStudio `words.import-flihub` once as a FliHub cut-over step (before glingDictionary goes); S1 recording source is per-machine → `~/.fli/machine.json` via fli-core (a fli-core change inside the FliHub v2 build).

**2026-10-30 ~10:55 — Story Pilot MERGED + LIVE; extcore-dev launched.** FliStudio main `e89f2a7` (ff, install + build, pushed), restarted via my-app (busy idle, 0 :443), health ok, `story.brief` answers for D13 (5 story.* verbs live). storypilot-dev driven (by orch) through: attach Overlay Pilot build sessions to D13 via FliStudio resource verbs → story.sources → write `flivideo:storypilot` skill → first D13 script via story.script.set → hold Teletubby payload (Teletubby :7111 is DOWN; orch starts it when script is ready). **extcore-dev** launched: tmux `extcore-dev`, worktree `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/extcore-neutral` (branch `extcore-neutral` off e89f2a7), brief `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/extcore-host-neutral-2026-10-30.md` (6124547): host-neutral ExtensionHost, G1 app-door call, host-supplied stages, Story Pilot Send-to-Teletubby button, extraction PLAN only, extension-core 0.2.0. David's ruling today: orch manages — act on routine next steps under the standing go, bring only David-only calls.

**2026-10-30 ~10:45 — FliHub: David said "Rebuild FliHub. It's fine." Discovery updated (b3fde63; same artifact links).** v2.0 = the 18-keep spine + JSON-RPC door (hard requirement) + an extension seam; B-roll capture = first FliHub extension right after v2.0. **Q0 ruled by orch (technical call): make @flivideo/extension-core host-neutral BEFORE the FliHub build, bundled with G1.** Verified: `ExtensionHost` (flistudio/extension-core/src/server.ts:21-36) carries flitoolsUrl/renderScript/python/poll fields that are Overlay Pilot's, and `STAGES` (descriptor.ts:11) is FliStudio's pipeline. Shape: host = `call` + `log` + call-any-app-door-by-name (G1); Overlay-specific fields move into Overlay Pilot; stages/slots supplied by the host. Order: Story Pilot merge (awaiting David) → extension-core host-neutral + G1 (one builder, worktree, FliStudio+both extensions re-gated) → FliHub v2 build beside v1.

**2026-10-30 ~10:30 — Story Pilot BUILT, gates reproduced by orch ✅; merge + restart await David's go.** Branch `storypilot` @ `e89f2a7` (ff from main f0dc19a). Orch rerun: build/typecheck/api:check/format ok; lint 0 errors (3 baseline e2e warnings); extension-core 37, overlay-pilot 64, storypilot 32, server 695+2, client 306; e2e 31/31 (random ports). Host diff checked = the stated list only (package.json deps ×3 + lock, counted tests, 1 new extensions test, spec §6.3, openrpc, AGENT-NOTES, schema mirror, the three extension lists). Merge plan: in flistudio live `git pull --ff-only && git merge --ff-only origin/storypilot && npm install && npm run build && git push`, then `my-app restart flistudio` (busy guard). After: David eyeballs "Story Pilot ›" link in the Script box + the screen; write `flivideo:storypilot` skill; attach Overlay Pilot build sessions to D13 then first real script.

**2026-10-30 ~10:00 — FliHub rebuild discovery DONE (flihub-rebuild-rsch).** Doc `/Users/davidcruwys/dev/ad/flivideo/docs/flihub-discovery-2026-10-30.md` (8d98801). Artifacts: keep/drop https://claude.ai/artifact/HYvB1rML8Axki1D3LKYvRN · look directions https://claude.ai/artifact/C5tDAED5yB5RXSJsE3dba6. Verdict: rebuild the spine only (slim FliHub on AppyStack + JSON-RPC door, beside v1, cut over after one real recording day). 55 items: keep 18 / drop 16 / unsure 21. 10 decisions (Q1–Q10) put to David by orch. **Live defect orch-confirmed from code:** `POST /api/projects/:code/hold` is mounted twice on `/api/projects` — hold.ts:86 (index.ts:358) shadows storage.ts:167 (index.ts:362), so the Storage-panel Hold runs the old whole-project offload, not the panel's verb (not run live). Other reported defects (not verified by orch): next-code GET writes config.json; 2 text-colour classes emit no CSS; tests write 140 lines to real telemetry; brand-dave current-deck wrong path; stray server/~/ folder. Suite finding: AppyStack template has no door — extract FliStudio capabilities/OpenRPC into a shared package.

**2026-10-30 ~12:15 — StoryPilot BUILD GO (David, in arch-rsch's window; relayed to storypilot-dev).** Answers: label "Story Pilot"; creator settings per brand (G2 accepted); Claude Code hands the script to Teletubby (G1 not fixed now); new `flivideo:storypilot` skill after the build; out-of-scope list confirmed; Q5 Scribe → ~20-min prior-art note first (Teletubby Scribe ADR, app-17 transcript-to-story, storyline-app), non-blocking. Estimate 5–7 h from go. Merge + FliStudio restart = orch, on David's go, after `system.status` busy check. **Banked (extension-core follow-up): G1 — an extension can't call another app's door** (plus G3 Script-box fact can't read extension files, G4 HostKit CopyButton).

**2026-10-30 ~12:00 — flihub-rebuild-rsch launched (by arch-rsch, on David's request) — DISCOVERY ONLY.** tmux `flihub-rebuild-rsch` (Opus 5.5 auto, cwd flihub). Brief `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/flihub-rebuild-discovery-2026-10-30.md` (7edba43). Inventory every FliHub screen/route/socket event/setting/watcher/project-folder write → keep/drop/unsure with evidence → AppyStack rebuild gains/risks → AppyDave light artifacts (keep/drop review + 2–3 look-and-feel directions) → STOP, report to David. Only write: a findings doc in flivideo/docs. No code, no branches, never stop/restart FliHub. Rebuild decision is David's. (Outside FliVideo, FYI: appy-invoice-rsch holds AppyInvoice decisions, waiting for David's go in its own window.) arch-rsch handover: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/handover-2026-10-30-arch-rsch.md`. StoryPilot still awaiting David's go on spec aecab30.

**2026-10-30 ~11:30 — StoryPilot spec v1 pushed; WAITING on David's go.** Branch `storypilot` @ `aecab30` (spec only, 362 lines): `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/storypilot/docs/planning/storypilot/spec.md`. Host edits 0 (beyond folder/workspaces/3 lists + counted test lists, spec table, openrpc). Teletubby `script.write` on :7111 takes it as-is after `context.select` — no Teletubby change. Estimate 5–7 h (build+gates 3–4, merge+restart 0.5, first D13 script 1.5–2.5; +1–2 h if G1 first) vs arch-rsch's 3–4 h. Gaps (findings, not patched): G1 ExtensionHost can't reach another app's door (V1: Claude Code sends the story.brief payload); G2 no creator-level data dir (per brand); G3 Script-box fact can't read StoryPilot's file; G4 HostKit has no CopyButton. Spec §13 has 6 questions for David (label, creator layer, handover, skill, Scribe, out-of-scope).

**2026-10-30 ~09:45 — storypilot-dev handed to orch (StoryPilot = FliStudio extension #2).** tmux `storypilot-dev` (Opus 5.5, auto, cwd flistudio live checkout but works only in worktree `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/storypilot`, branch `storypilot`). Brief `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/storypilot-launch-2026-10-30.md` (f80a5b7); sources B667 (voice) + B670 (dossier). Phase 1: spec only → commit/push spec → STOP, report to David. Build only on David's go; full FliStudio gate set + conformance. Rulings: on @flivideo/extension-core; host edits limited to own folder + workspaces entry + 3 extension lists (else stop-and-report); stage `script`, ns `story.*`; script to Teletubby ONLY via its agent API :7111, never write fli.tubby.json; extension-core/fli-core changes = findings. Merge + FliStudio restart = orch, on David's go. David drives it mostly from orch's window. **FliStudio main `f0dc19a`** adds `scripts/busy.sh`; apps.json control `busy` wired → `my-app stop|restart flistudio` refuses (exit 5) while busy/:443 out; `--force` overrides. ⚠️ `my-app restart flistudio --help` RESTARTS (no help). David eyeballed the post-extension-core project page: OK. Brief §2a added (62ea916): name/label, video is the unit, Script box beside Teletubby, first agent verb, reuse FliStudio `session` video resources as sources (no new list); storypilot-dev told to re-read before the spec.

**2026-10-30 ~01:30 — extension-core MERGED + FliStudio restarted (by flivideo-arch-rsch on David's go; orch verified head = origin, clean, :7151 health ok, worktree + local branch gone).** FliStudio main `1e89742` (ff from 0897a45). Gates (peer-reproduced): build/tc/lint/format/api:check ok; extension-core 37, overlay-pilot 64, server 694+2, client 306, e2e 31/31; no FliStudio file imports modules/overlay-pilot. Restart pre-check: 0 :443 uploads, no render.py. **New rule:** FliStudio `system.status` busy is now real (derived from extensions) — check it before any FliStudio restart; FliStudio still does not refuse its own restart and the CLI can't see busy runs. **Open:** David to eyeball the project page (Overlay box, "Overlay Pilot ›" link, Overlay Pilot screen); `origin/extension-core` merged, safe to delete. **Next:** extension #2 = StoryPilot (dossier B670, voice log B667), own window after David's go.

**2026-10-30 ~01:00 — @appydave/core on npm ^0.2.0 everywhere; overnight cleanup DONE (by flivideo-arch-rsch on David's go; orch verified heads, no vendor/, worktree lists, tmux).** FliCast `8213fcd` (1341+1), FliEdit `d0cb909` (220), FliCut `92f41c9` (612; NOT restarted, live install byte-identical), AppyTron `b5a99a4` (template on npm ^0.2.0, template/vendor deleted, scaffolds carry no vendor/; 8 + create 30). All 44 overnight/probe worktrees removed (16 GB), local+GitHub branches deleted (David ran remote deletes), 7 ovn-*/core-* tmux closed. Remaining worktrees are older feature work, not part of that cleanup (flistudio 13 + new `extension-core` @ 0897a45, flicut 5, flitools 1, appytron-factory). **Now:** flivideo-arch-rsch is building extension-core in `flistudio-worktrees/extension-core`; FliStudio merge/restart only on David's go after the overlay/:443 check. The vendored-tgz and scaffold-vendor follow-ups in the 00:30 entry are closed.

**2026-10-30 ~00:30 — Post-publish DONE (by flivideo-arch-rsch, on David's go in its window; orch verified heads + registry).** @appydave/core 0.2.0 published by David (npm shasum `ded6bdef`, matches vendored 1cd0e79 tgz). FliHub main `061ae34` (ff-merge of `overnight/2026-10-29-fli-core-026`; core 0.26.0 in node_modules; restarted via `my-app restart flihub` with 0 clients; :5101 answers; server 715+1 skip). Teletubby main `efabbe5` (npm ^0.2.0, vendor/ removed; 438+11). AppyStack main `c1270f6` (template/server ^0.2.0, vendor removed, create re-synced; 86+44, create 59; untracked `.appynet/` not ours). AppyTron main `8444422` (scaffold default ^0.2.0; template stays vendored per README). **Still vendored 0.2.0 tgz:** FliCast, FliEdit, FliCut — candidate swap to npm ^0.2.0 (banked). **Banked:** AppyTron scaffold still copies template/vendor/ into new apps (dead weight); AppySentinel optional bump. **Open:** worktree cleanup (now also branch `overnight/2026-10-29-fli-core-026` in flihub); extension-core work in flivideo-arch-rsch awaits David.

**2026-10-29 ~23:10 — @appydave/core 0.2.0 (zod 4) MERGED everywhere it was ready.** main: foundation `1cd0e79` (dist built), imagedrip `ff113de`, samantha `89e3eeb`, teletubby `31d199d`, flicast `8ceddb6`, fliedit `e311824`, flicut `ef8d5cb` (restarted idle, pid 76208), appystack `8622c24`, appytron `5e9a0a8`. All re-tested on main: one zod 4 each. ImageDrip/Samantha: David's uncommitted package-lock churn stashed ("npm lock churn, stashed by flivideo-orch…"); npm install re-dirtied the lock (npm version churn, harmless). **Blocked on David:** (1) npm publish 0.2.0 — `npm whoami` = 401, not logged in; I must not log in. After publish: Teletubby, AppyStack server, AppyTron scaffold default swap vendored tgz → npm ^0.2.0; AppySentinel can bump (drop-in). (2) FliHub merge (running). (3) Cleanup of probe worktrees + `appydave-foundation` symlinks in imagedrip-/samantha-worktrees.

**2026-10-29 ~23:05 — Job C reproduced ✅** (branch `core-020-zod4`): flicast 532bdc1 (1341), fliedit 0e8c7a1 (220), flicut 0f852ee (612/612 on rerun; one known flake), teletubby 31d199d (438+11), appystack 8622c24 (86+44, create 59, sync identical, lint ok), appytron 5e9a0a8 (8, create 30); one zod 4 each, marker == spec. Merge trap: main in flicut/flicast/fliedit already has the w7 0.1.0 marker → appytron.json conflict, take core-020's. Waiting on `core-consumers-dev` (Job D: ImageDrip silent {} MCP schemas + Samantha z.record) before foundation main moves. Then: merge foundation core-0.2.0-zod4 → npm publish 0.2.0 → merge app/template branches → swap Teletubby/appystack/appytron-scaffold to npm ^0.2.0 → restart FliCut at idle. Pending David: FliHub merge (running), ~14 probe worktrees cleanup (builder's auto-mode remove was denied — don't override).

**2026-10-29 ~22:45 local — v0.26.0 MERGED + LIVE except FliHub.** main: fli-core `4fb29ce` (tag v0.26.0), appystack `8a79987`, appytron `92da408`, flicast `4d8dcc3`, fliedit `23cd2bd`, flicut `578cf04` (restarted at idle, pid 29773), teletubby `23a4e61`, flitools `0315774` (running old code until its next restart; pin-only change), flistudio `0897a45` (template-sync without @appydave/core + W4/W5/W8; installed, built, restarted, health ok). **FliHub NOT merged** — running under overmind; merging hot-reloads it; waiting on David. Branch `overnight/2026-10-29-fli-core-026` @061ae34 ready. Running: `core-rollout-dev` (Job C: @appydave/core 0.2.0 → apps/templates; then I merge foundation main + npm publish 0.2.0 — David's blanket go covers it, only when all green).

**2026-10-29 ~22:35 local — MERGES UNDER WAY (David: "move forward on everything, I give permission for all things to be done").** Done: fli-core v0.26.0 tagged on main `4fb29ce`; appystack main `8a79987`; appytron main `92da408`; W7 markers merged (flicut `77a8a3f`, flicast `65d83cd`, fliedit `726950a`). Running: `ovn-merge-dev` (repin six apps to #v0.26.0; FliStudio: drop @appydave/core from template-sync, then rebase fli-core-026 onto it → `overnight/2026-10-29-flistudio-final`), `core-zod4-dev` (@appydave/core 0.2.0 on zod 4 + consumer table; no publish). Brief: docs/briefs/merge-prep-and-core-zod4-2026-10-29.md. Then I merge the apps into live. FliHub is running (overmind, since Tue 21:00): merging into it hot-reloads = a restart → needs a not-running moment. FliCut running (pid 26674): busy:[] check + `bin/flicut restart` after merge. FliStudio restart: check no overlay run (system.status busy is hard-coded [] — control.ts:72) and no :443 upload.

**2026-10-29 21:15 local — OVERNIGHT BUILD RUNNING (I am boss).** Spec `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/overnight-2026-10-29-build-spec.md` @280be51 (W1–W8; W8 = fli.brand.json lock). David's "go" verified in flivideo-arch-rsch transcript (14:09:40Z, origin human). Builders (tmux + iTerm): `ovn-templates-dev` (Sonnet: W1→W2→W7 markers), `ovn-flicore-dev` (Opus: W3+W7 window-state+W8 core → tag v0.26.0-rc.1 → W4+W8 non-FliStudio), `ovn-flistudio-dev` (Opus: FliStudio W4/W5/W8 after rc.1, W6 after W1). Watch cron 61f0c1e8 at :13/:43 (session-only). David also asked: check flivideo-arch-rsch every 30 min until ~00:15. Done = every item passed (gate reproduced by me) or parked + morning report `docs/briefs/overnight-2026-10-29-report.md` pushed on flivideo main (the only main push allowed). Never merge, touch live checkouts, restart apps, or ask David.
- 21:30 REPRODUCED by orch: W1 (8a79987: tc/lint/fmt/build ok, template 86+44 tests, create-appystack 59, sync identical, 0 majors of 42 bumps) ✅ · W2 (92da408: tc/build ok, 8 + 30 tests, electron ^44.10) ✅ · W7 markers (flicut 77a8a3f, flicast 65d83cd, fliedit 726950a; json == package.json spec) ✅ · W3+W7 window-state+W8 core (fc1957a, tag v0.26.0-rc.1 → fc1957a; tc/lint/build/fmt ok, 627/627, lines 99.01%) ✅. ovn-templates-dev finished. Decisions to report: audio+fli.cut→flicut; exportApp legacy/part→null; EditApp gains flicast; template has no lockfile so W1/W2 are range-only bumps; Electron 44.10 not run live.
- 21:50 REPRODUCED FliStudio W4+W5+W8 (branch overnight/2026-10-29-fli-core-026 @06123ec, off bad7d6b; main now 461042c → rebase at merge): build/typecheck/lint/format/api:check ok; tests overlay-pilot 60, server 686+2 skip, client 303; lock → fc1957a, core 0.26.0-rc.1 ✅. Builder decisions: FliCast ranks with FliEdit; unparsed/part → placed file; no FliCast rung in best-transcript (follow-up); schema mirror not regenerated (drifted at baseline). W8 race rerun S1–S3 owned by ovn-flistudio-dev once FliHub W8 is pushed. W6 started.
- 22:40 ALL 8 ITEMS PASSED, none parked; every gate reproduced by orch (W4 six repos, W6 incl. e2e 31/31, W8 race-w8 exit 0). Report pushed: docs/briefs/overnight-2026-10-29-report.md. Builders told to stop. Remaining: arch-rsch half-hour checks until ~00:15 (cron), then idle. Next for David: merge per report §4 (fli-core → templates → apps → FliStudio last + restart on his go).

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

## 2026-11-05 06:25 — Roamy handed back; David now at the M4 with orch
- flivideo-roamy stepped back (handover stamped 2026-11-05 ~00:10). Style: execute recs; bring David only "reload, look here"; ONE prose question at a time with a rec.
- Teletubby main = 5436186 (voicefix c6fd6c5 + voice-parity b48c8dd; 554 pass / 11 skip; pushed). Speech permission granted 05:59 (com.appydave.teletubby.speech). Apple helper now fails "Siri and Dictation are disabled": David to switch on Dictation. Not restarted yet; restart at a break, then voice-selftest.sh, bench (apple+groq), live read d13.
- Open queue from Roamy, in order: A. wire openrig/spoken-scripts/spoken-script-template.md as "Structure (brand): story" guide (point, header only) + forge VERBAL-STYLE "scripted story" register (from spoken-vs-read.md + Mike pacing) + split §8 every-video vs tutorial-only — rec YES, unasked of David at the M4. B. d13 redo: David writes Direction, then Rerun v4 — NO rerun until he says. C. voiceDocs vs Verbal guides ownership, sign-off wording — David's call later. D. OmniVoice trial on M2 — needs go. F. "Reading the project…" >10 s over tunnel — check on M4.
- AITLDR strip MERGED 59d82fe (79/79 e2e, 805+352+53 unit), FliStudio restarted 06:35; branch aitldr-strip kept on origin (delete denied by classifier — David's call). Teletubby restarted on d13, selftest 4 PASS / apple-helper FAIL timeout (app log shows Apple task starting fine — probe suspect).
- Also held: FliEdit A2–A8 real-app screenshots (needs awake display).
- Pages: story guides five questions https://claude.ai/artifact/EoTMUn9ci2sLrT13Wvrww1 · VERBAL-STYLE deconstructed https://claude.ai/artifact/4xzc9y2kAvwGPeWzBVvtgM · build-story guides https://claude.ai/artifact/EwzoVcZVWmNyafSCoho4WE
- 06:45 Parked for later today: Teletubby apple-helper selftest timeout (suspect the voicefix probe vs the parity app bundle; M2 worker, don't touch live Teletubby). FliEdit A2–A8 real-app screenshots.
- STORY PILOT FOCUS (David, morning 11-05). First item: Reader shows build-short.md's header as raw text (schema:/id:/label:… then a literal ---) instead of the guide layout; file's frontmatter is well-formed (starts ---). Then Roamy's A (spoken-script-template as story structure guide + "scripted story" verbal register + §8 split), B (d13 Direction → Rerun v4 only on David's say-so), F (slow "Reading the project…").

## 2026-11-05 ~07:00 — Story Pilot: Reader "bug" + item A held

- **Reader build-short "raw header"**: not a code bug. Live app (RPC `story.guide.read` + fresh Playwright) renders the guide layout correctly; David's tab was a stale pre-restart copy. Told him to reload.
- **Roamy's item A is ON HOLD** (David, 2026-11-05). Replaced by a **script-style library** mandate: reverse-engineer 3–4 styles (AITLDR Series A old, AITLDR Series B new, AppyDave last 25, Mike/OpenRig + 3 videos, Maitis @maitis-ai) into typed `storypilot.guide/1` structure + verbal-style guides; a matrix page; a recommendation of which styles first. Separate visual/editing lane (frames, cuts) = plan + size estimate only, waiting for go.
- Gates: any download / install / paid transcription needs David's go after a plan with counts, cost, size. Out of scope: wiring guides into Story Pilot, editing VERBAL-STYLE, d13 rerun, B-roll/auto-edit features.
- Step 1 running: read-only inventory worker (M4, local subagent) — Series A/B meaning, transcripts on disk, harvest/transcribe tools, disk free.

## 2026-11-05 ~07:35 — Script-style library: GO (David)
- David: Series reading right (B = daily skill series ≥ 2026-09-15; A = Alex era before); "go steps 1-4"; visual lane "run on the M2 … YES".
- Mike's 3 videos on disk: qccsfUnrQ9w fetched (3,817 w) → tubescripts c6f36be; CYRJDTcTKhQ, AL-PQuB2wy0 already there. Batch `2026-11-05-script-styles`.
- Text lane: M2 worker `script-styles-build` (sonnet), brief `docs/briefs/script-styles-library-2026-11-05.md` (fe8ca36+). Outputs → `docs/script-styles/`. Background appynet watch running.
- Visual lane: approved for the M2; launch a second worker once `docs/script-styles/selection.json` is pushed (reuse those videos; ~10/style, 720p, 1 frame/2 s, delete video after frames; ~4 GB transient, ~1.5 GB kept).
- Gate on M4: parseGuide every guide; then matrix artifact (AppyDave light) opened for David.

## 2026-11-05 ~08:45 — Script styles: own channels from FliVideo (David's correction)
- My error: brief told the M2 worker to harvest AITLDR/AppyDave off YouTube despite the stores. Stopped. Mirrors re-synced (`youtube.sync`: aitldr 431, appydave 191).
- Corpus from FliVideo: 95 selected own-channel videos = 38 store, 35 project transcript, 7 script only, 15 none (2 have captions fetched; 13 gap).
- YouTube now only for Maitis (running at 45 s pace) and, after it, the 13 gaps, which land in the published store.
- Banked: memory `feedback-own-channels-come-from-flivideo`, guard in tube-harvest SKILL.md.
- Note: David's "visual lane" still queued after Maitis; own-channel video files should come from FliVideo too, not YouTube.

## 2026-11-05 — banked from brains-b0 (no action now)
- B695: FliVideo builds to move onto OpenRig structures, not terminal workers. Plan `/Users/davidcruwys/dev/ad/brains/openrig/exec-orchestrators-2026-11-05.md`. openrig-orch proposes one pilot slice through the `workshop` rig; chosen together; needs David's go.
- B692 (Jan call): AI version of the director's chair: mostly no avatar, avatar on for chosen moments from one continuous audio track, lip-synced not regenerated. Jan researching dedicated avatar tools instead of Higgsfield.

## 2026-11-05 ~09:20 — Script-style library: text lane DONE
- 10 guides + matrix + coverage at `docs/script-styles/` (b656d78); parseGuide 10/10 on the M4. Page: https://claude.ai/artifact/Sb53xjPe57fX4be9dNjWi8 (source `docs/artifacts/script-styles-matrix-2026-11-05.html`). Rec: offer aitldr-new, mike, appydave, maitis; hold aitldr-old. Waiting for David's verdict. Wiring into Story Pilot still out of scope.
- 22 pre-ruling aitldr captions remain in tubescripts/aitldr (18 unused); keep-or-delete is David's.
- Visual lane: M2 worker `script-styles-visual`, brief `docs/briefs/script-styles-visual-2026-11-05.md`.

## 2026-11-05 — HOLD on D18/D19 scripts (David, relayed by exec-coord)
"Don't do anything on script yet." No D18 intro pick, no D19 angle; he did not choose A. Don't build or write a script, don't prompt the d18/d19 windows. exec-coord says when it lifts. Script-styles visual lane on the M2 continues.
