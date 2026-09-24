<!-- FliVideo source bundle · d04 autopilot UAT run report · generated from ~/dev/video-projects/v-appydave/d04-flivideo-autopilot/-run/run-report.md -->


# d04 run report — first autopilot UAT (2026-09-23)

**Purpose**: What happened when an agent (`d04-work`) built d04 end to end through the FliVideo apps'
own surfaces, acting as a user. It covers facts, pass/fail against the plan, gaps found, fixes made
during the run, architecture notes, and a log of messages carried between windows.

**Verdict**: d04 was built end to end, with one human touch (FliCast record/stop). 13 of 15 criteria
pass. AC5 is partial (the queue drained too fast to count). AC10 fails: the exported captions drift up
to ~1 s late by the end. The run found 17 gaps. Two blocked a step, and both were fixed and restarted
during the run (FliStudio footage verbs; FliCut mixed-resolution export).

**Plan**: `~/dev/ad/brains/docs/handovers/deliver-2026-09-23-B587-B588-d04-uat.md` §5b.
**Raw call log**: `-run/run.log` in this folder (every door call with its reply, times +07).

## 1. Facts

| Thing | Value |
|---|---|
| Project | appydave `d04`, id `72113060-77cd-4aa9-b5f3-366b38c95e4d`, 16:9, single, en |
| Folder | created as `d04-d04-autopilot-test` → renamed `d04-flivideo-autopilot` ("flivideo autopilot") |
| Hub takes | 4 via Ecamm folder → FliHub Incoming: `01-1-intro` 6.0 s, `01-2-intro` 4.5 s, `02-1-overview` 7.6 s, `03-1-outro` 3.6 s (1080p25) |
| Footage | 4 Pocket 4 clips via `footage.import`: 05 (53.8 s), 09 (35.0 s), 10 (32.4 s), 11 (23.7 s); HEVC 3840×2160 10-bit 59.94 |
| Cast | `studio-tour-broll` 20.5 s, 1080p30, spoken; recorded by David |
| Edit | FliCut `d04-autopilot-cut`, 8 files, source 182.68 s, 17 cuts, planned 167.88 s |
| Export | `videos/d04-autopilot-cut/d04-autopilot-cut-cut.mp4` (raw, −19.4 LUFS, LRA 10) and `…-audio-a100.mp4` (cleaned, −15.2 LUFS, LRA 5.5), both 168.96 s 1080p25; `…-audio-a100.srt` (30 cues) + `.txt` |
| Scripts | Teletubby `d04-intro`, `d04-outro` in set `d04-d04-autopilot-test-scripts`; intro on stage |
| Human touches | 1: David typed the cast name and pressed Record/Stop in FliCast |
| Run time | 22:23 → 22:47 +07, including two fix-and-restart cycles |

Edit order (the plan's 6 slots, footage slots holding 2 clips each):
`hub 01-1-intro → hub 02-1-overview → footage 05 → footage 10 → cast → footage 09 → footage 11 → hub 03-1-outro`
(`01-2-intro` was left out as the weaker intro take.)

## 2. Acceptance criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | d04 via `project.create` | PASS | `project.get d04` |
| 2 | Hub takes via FliHub Incoming | PASS | `GET /api/files` showed each with `aspectCheck.status: ok` before `POST /api/rename` |
| 3 | Hub transcript status polled | PASS | takes 2–4 went `none` → `complete`. Take 1 was already `complete` at the first poll |
| 4 | Footage via `footage.import` | PASS | after a FliStudio restart (G1) |
| 5 | Queue auto-fed, drain observed | PARTIAL | import reply showed running/queued, and `footage.queue` then showed 4 done, scoped to project d04 + app flistudio. Groq finished in seconds, so there was no counted N→0 |
| 6 | Footage json (word-timed) + srt + txt | PASS | `footage/transcripts/*`: 132/87/69/60 words |
| 7 | Cast exported + auto transcript | PASS | export result `transcript.jobId 5ef4fa45`; `transcript.jobs` done (app flicast, project d04) |
| 8 | Start an edit with the mixed order | PASS | `edit.start` → FliCut `edit.get` lists the 8 medias in order |
| 9 | Output shorter than the inputs | PASS | 168.96 s rendered vs 182.68 s source (−13.7 s); `cuts.apply` removedSeconds 14.8 |
| 10 | Export transcript + SRT aligned | **FAIL** | SRT + TXT exist, but cues drift late: overview +0.07 s, footage 11 +0.82 s, outro +0.98 s (source audio cross-correlated against the export). SRT built from the planned 167.88 s; render is 168.96 s (G13) |
| 11 | Cleaned audio | PASS | a100 arm: −15.2 LUFS / LRA 5.5 vs raw −19.4 / 10 |
| 12 | Teletubby 2 scripts listed | PASS | `get_set` lists both; `stage_select` intro → `list_rigs` position confirms; both still listed after the rename |
| 13 | `project.rename` | PASS | folder `d04-flivideo-autopilot`, code `d04` and id unchanged |
| 14 | No bypass | PASS | only one file copy into an app's path, the Ecamm delivery (D7). Everything else went through app doors. Diagnostics (ffprobe, one 2 s ffmpeg repro, audio cross-correlation) read the project and wrote only to the agent's scratchpad. This report and `run.log` are the only direct writes into the project |
| 15 | This report | PASS | `-run/run-report.md` |

## 3. Gaps found

| # | App | Gap | Blocked? | Status |
|---|---|---|---|---|
| G1 | FliStudio | the running server predated c7ead0f, so `footage.*` was missing live ("unknown-capability") | step 4 | **FIXED in run**: restarted on current main (pid 7810) |
| G2 | FliStudio ↔ FliTools | `footage.import` reported clip 09's transcript as `refused` ("FliTools answered outside its contract"), yet FliTools had created job `ae47afce` and finished it | no | reported |
| G3 | FliStudio | `project.create` doesn't strip a leading code from the name ("d04 autopilot test" → `d04-d04-…`) | no | fixed in d7742a4, not live yet |
| G4 | FliHub | transcription status reads `none` between promote and `complete`, with no queued or transcribing state | no | recorded (D3: FliHub out of layer) |
| G5 | FliCast | the armed name from `recording.arm` doesn't reach the window's Record sheet (Name empty) | no (human step covered it) | reported |
| G6 | Teletubby | `write_script` returned `n:1` for both scripts; `get_set` then shows outro 1, intro 2 | no | sent to teletubby |
| G7 | FliCut | **export failed on mixed frame sizes**: segments were joined with no scale or fps step first → ffmpeg EINVAL (exit 234) | **step 7** | **FIXED in run**: d91ec7d normalises each segment to 1920×1080 25p yuv420p 48k stereo |
| G8 | FliCut | the export job dropped ffmpeg's stderr ("exited 234" only) | no | FIXED in d91ec7d |
| G9 | FliCut | thumbnail extraction ran twice at once for the same clip (footage 05) | no | reported |
| G10 | Teletubby | set id keyed on folder name | no | fixed in 711e315 before the rename; set survived the rename |
| G11 | FliCut | `export.start` with `arms` silently ignores `formats`, so no SRT/TXT was written | no (a second single-arm call made them) | reported |
| G12 | FliCut | `export.last` returns `no-export-yet` after an arms export, and after the rename it returns paths under the old folder | no | reported |
| G13 | FliCut | **SRT drifts from the render** (~1 s by 2:45). SRT uses the planned timeline; the render rounds per segment (likely a side effect of G7's fix) | no | reported |
| G14 | FliStudio | `project.rename` doesn't re-point running apps. Afterwards FliHub had `context: null`, and FliCut/FliCast/Teletubby still pointed at the vanished folder until `app.launch` switched them | no | new |
| G15 | FliCast | after switching to the renamed project, `project.list` was empty until `project.open` on `fli.cast.studio-tour-broll.json` (recents are keyed by absolute path) | no | new |
| G16 | Teletubby | switching project leaves the set choice UI-only ("pick the set in Teletubby"), by design | no | by design, noted |
| G17 | Walkthrough doc | said FliStudio has no token; it now needs bearer + `x-fli-principal` | no | orch fixing |

## 4. Architecture notes (cross-app)

- **Project identity.** Some apps key the project on the folder name: Teletubby's set id (fixed in
  run), FliCut's lab and undo history (FC-40, fli-core labPath), and FliCast's recents. Others key it on
  the code (FliTools queue = `d04`). FliCut's edit stores project-relative media paths, so the edit
  itself survived the rename. A rename also isn't broadcast to running apps (G14). **Rule going
  forward: the code (`d04`) is identity; the folder name is display.** A rename should tell every open
  app, like `app.launch` does.
- **Six doors, five dialects.** FliStudio: `POST /api/call {name,input}` + bearer + `x-fli-principal`.
  FliCut: JSON-RPC `POST /api/rpc` + bearer. FliCast: CLI `family verb --json --as`. Teletubby:
  CLI `call snake_name --input` (dotted names only over its RPC). FliHub: plain REST, no token. The
  shared layer has made status, quit and capabilities uniform, but not the call shape or verb names
  (`system.status` vs `system_status`). An agent needs a per-app adapter today.
- **Result shapes differ.** FliStudio `{ok,value}`, FliCast `{ok,value,meta}`, Teletubby
  `{ok,data}`, FliCut `{jsonrpc,result}`. Error shapes differ too (`error.code` /
  `error.failureMode` / JSON-RPC code). Job polling differs as well: FliCast `task.status` → `status`;
  FliCut `job.get` → `state`.
- **Transcription is converging.** FliStudio footage and the FliCast cast both went through FliTools
  (same `transcripts/` layout beside the media, word-timed, queue keyed on the code). FliHub (own
  transcripts, no word timings) and FliCut (own mlx-whisper on edit open, ~1 min for 8 files) still
  transcribe separately (D4), so every d04 file was transcribed twice.
- **Mixed media is normal.** One short video mixed 1080p25 studio takes, a 1080p30 screencast and
  4K59.94 10-bit HEVC camera footage. Any app that combines media must normalise (G7), and keep every
  derived artefact on the timeline it actually rendered (G13).
- **Diligence is uneven, as expected.** FliCast was the reference and behaved exactly as documented.
  FliStudio, FliCut and Teletubby had their new verbs, but the live processes lagged the code (G1), and
  the new paths hit untested combinations (G7, G11, G12). The run mostly surfaced deployment and
  combination bugs, not missing design.

## 5. Ferrying log (item 7: should there be a structured channel?)

Every message carried between windows during the run (SendMessage, relayed by flivideo-orch):

| Time | From → to | What | Could a channel carry it? |
|---|---|---|---|
| 22:24 | d04-work → orch → flistudio | stale server / restart (G1) | yes: capability-missing event |
| 22:25 | flistudio → d04-work | restarted, new token | yes: app-restarted event |
| 22:27 | d04-work → orch → David | FliCast armed, please record | yes: human-action-needed event |
| 22:28 | orch (from David's screen) → d04-work | armed name not in window (G5) | only with window-state feedback |
| 22:29 | orch → d04-work | David done recording | redundant: `recording.state` showed it |
| 22:30 | orch → d04-work | don't restart FliTools/FliStudio mid-run; rename naming advice | yes: run-lock / maintenance flag |
| 22:33 | d04-work → orch → flicut | export blocked (G7) | yes: job-failed event with stderr |
| 22:34 | orch → d04-work | Teletubby set keyed on folder; check after rename | partly: a contract note, not an event |
| 22:40 | flicut → d04-work | restarted on d91ec7d, re-run export | yes: app-restarted event |
| 22:41 | teletubby → d04-work | restarted on 711e315, stage re-applied | yes: app-restarted event |
| 22:43 | d04-work → orch → flicut | G11–G13 | yes: job-result / gap event |

Pattern: nearly all ferried messages were one of four kinds: (a) an app restarted or needs a restart
after a code change, (b) a human must act, (c) a job failed and why, (d) don't touch X while the run is
live. All four are events an app or the orchestrator could publish. Evidence favours a small suite
event feed (`app.restarted`, `human.needed`, `job.failed`, `run.lock`) over free-form relay. Design
question only, not built (out of scope).

## 6. Fixes made during the run

| Fix | Where | Effect |
|---|---|---|
| FliStudio restarted on current main | flistudio window, pid 7810 | `footage.import/list/queue` live (G1) |
| Per-segment normalisation + stderr tail in job errors | flicut d91ec7d, restarted pid 81463 | mixed-resolution export works (G7, G8) |
| Set keyed on project code | teletubby 711e315, restarted pid 91845 | scripts survive rename (G10) |
| Leading-code strip in `project.create` | flistudio d7742a4 | committed; goes live after the run (G3) |

## 7. Follow-ups

1. **FliCut G13 (fails AC10)**: build the SRT/TXT from the rendered timeline, or snap segment
   trims to frame boundaries so plan and render agree. Re-export d04 and re-check the three spot points.
2. **FliCut G11/G12**: honour `formats` on the arms path, or refuse it; make `export.last` see arms
   exports and follow a rename.
3. **FliStudio G14**: `project.rename` re-points every open app (or publishes a rename event).
4. **FliStudio ↔ FliTools G2**: align the submit reply contract (probably a reuse/dedupe path).
5. **FliCast G5, G15**: armed name reaches the window; recents follow a renamed project.
6. **FliHub G4**: expose queued/transcribing in `/api/transcriptions/status` (record only, per D3).
7. **Re-run readiness**: this run is the baseline. A re-run is a new project (d05) from the same
   `-reference/d01/` fixtures. Deploy lag hit twice (G1, and G3 not live), so a pre-run check
   "every app's pid is newer than its HEAD commit" should come first.
8. **Out of scope, unchanged**: bad-take detection (D1), FliCut → FliTools transcription (D4),
   suite event bus (item 7; evidence in §5).
