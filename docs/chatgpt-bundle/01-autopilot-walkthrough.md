<!-- FliVideo source bundle · end-to-end walkthrough · generated from docs/d04-autopilot-walkthrough.md -->


# FliVideo end to end — test video d04 on autopilot

**Purpose**: Show, step by step, how far an agent can drive one real video through the FliVideo suite
today, and exactly where it stops. The gap list at the end is the input for designing "FliVideo on
autopilot".

**For Agents**:
- Each step names the app, the route an agent calls, what it writes, and the state: **WORKS**,
  **BROKEN** or **MISSING**. ★ means human-only by design.
- Grounded in each app's code at 2026-09-23 (the app sessions answered from their own repos). The
  Electron apps were stopped that day, so "WORKS" means tested in code, not watched live this week.
- The central map is `README.md` in this repo. Per-app detail is in each app's `docs/SYSTEM.md` and
  `docs/AGENT-NOTES.md`.

> **The test video is `d04`** (David, 2026-09-23). The code `d03` is already taken in AppyDave
> (`d03-cutty-presenter-tracking`).
>
> **Starter media (David):** re-recording takes and re-shooting footage is slow, so the d04 run starts
> from D01's material (`v-appydave/d01-flivideo-tour`): its **4 FliHub takes** (`hub/recordings/01-1-intro`,
> `01-2-intro`, `02-1-overview`, `03-1-outro`, with transcripts) and **3–4 of its Pocket 4 footage clips**
> (`footage/NN-<name>-<clip>.mp4`, with `.txt` transcripts). They are copied into d04 as if they had just
> been recorded, so steps 2 and 3 can be exercised without a camera. Not done yet; this is the plan for the
> first autopilot run.

---

## How an agent reaches each app

| App | Door (HTTP) | Auth today | CLI | MCP |
|---|---|---|---|---|
| FliStudio | `127.0.0.1:7151` · `POST /api/call {name, input}` · `GET /api/capabilities` | loopback only, no token (token + principals being built) | `bin/flistudio <capability> --flag …` (works with the server down) | none |
| FliHub | `127.0.0.1:5101` · ~150 REST routes | loopback only (127.0.0.1 + ::1), no token; foreign browser origins refused | none | none |
| FliCast | `127.0.0.1:7131` · `POST /v1/call`, `/v1/rpc` | bearer token from `control.json` | `node bin/flicast.mjs <verb> --json --as agent:x` | `flicast_describe`, `flicast_call` |
| FliCut | `127.0.0.1:7121` · REST under `/api/` | bearer token from `control.json` | `bin/flicut` (3 commands) | none |
| Teletubby | `127.0.0.1:7111` · `POST /api/invoke` | bearer token from `control.json` | `bin/teletubby.mjs call <verb> --input '{…}'` | none |

Every app is started, stopped and restarted from a shell with `scripts/app.sh start|stop|restart
--brand … --project …`. **No app can be quit by an agent through its door yet.** FliStudio is adding
`app.stop` / `app.restart` for all of them now.

---

## Step 1 — Create the project (FliStudio) · WORKS

- **Call**: `project.create {brand:"appydave", name:"<d04 name>", code:"d04", aspect:"16:9", shape:"single", languages:["en"]}`
  - CLI: `bin/flistudio project.create --brand appydave --name "…" --aspect 16:9 --shape single`
- **Writes**: `<brand root>/<code>-<slug>/fli.studio.json` (id + intents). The code is the next free one;
  pass `code` to choose. New projects use the **hub** layout, so recordings go under `hub/`.
- The aspect matters later: FliHub warns when a take doesn't match it, and FliCut starts new edits in it.

## Step 1b (optional) — Put a script on the prompter (Teletubby) · WORKS, one catch

- **Open**: `scripts/app.sh start --brand appydave --project <code>-<slug>`, or re-point a running app
  with `context_select {brand, project}`.
- **Write**: `write_script {name:"Intro", text:"…", video?:"<name>", triggers?:{…}}`. The text comes from
  an AI or the future scripting app. **Teletubby never writes scripts**; it shows and edits them.
- **Triggers**: pass them in the same call, or `write_trigger_set` later. Without them the script shows
  but can't step.
- **BROKEN (catch)**: if the project already has another script set attached, the stage opens that set
  and the new script only appears in the setup panel. Choosing a set is UI-only by design.
- ★ Stepping through the script and pressing record in Ecamm are a person's actions.
- **MISSING**: no link between a Teletubby script and a FliHub take.

## Step 2 — Record takes (FliHub + Ecamm)

All HTTP on `127.0.0.1:5101`. FliHub has no CLI and no MCP.

| Sub-step | Route | State |
|---|---|---|
| Set the active project | `POST /api/context {brand, project, video?}` (check `refused`; a refusal keeps the previous project) | WORKS |
| Record | ★ a person presses record in Ecamm; there is no route | by design |
| Take lands in Incoming | watcher adds it to a pending list and emits socket `file:new`; agent polls `GET /api/files` | WORKS |
| Aspect check | automatic at ingest (frame size + black-bar detection) against the project's `aspect`; result appears as `aspectCheck` on `GET /api/files` | WORKS, but **BROKEN for agents (race)**: if the agent renames before the check finishes (a few seconds), the check is skipped silently. Wait for `aspectCheck` before renaming. Mismatches persist and show on `GET /api/recordings`; dismiss with `POST /api/recordings/aspect-dismiss {files}` |
| Name and promote | `GET /api/suggested-naming` (next chapter + sequence), then `POST /api/rename {originalPath, chapter, sequence, name, tags?}` → `hub/recordings/{chapter}-{seq}-{name}.mov` | WORKS |
| Transcribe | queued automatically by the rename → `hub/transcripts/*.txt|.srt|.json` (no word timings). Status `GET /api/transcriptions`; retry `POST /api/transcriptions/queue {path}` | WORKS; no cancel route |

- FliHub is being rebuilt, so it will **not** adopt the shared agent layer the other apps are getting.

## Step 3 — Bring in the camera footage (Pocket 4) · MISSING

- There is **no capability** that copies or registers footage. FliStudio only *reads* a top-level
  `footage/` folder: it lists the files (`assets.list`) and offers them in Start an edit.
- **Today**: a person copies the clips into `<project>/footage/` by hand (Finder or `cp`), renamed to
  `NN-<name>-<clip>.mp4`, with transcripts beside them. That's what D01 did.
- **Needs a ruling** before it can be built: FliStudio may not write into a project folder without
  David's word. A `footage.import` must settle copy vs move, the source (card, folder), and renaming.

## Step 4 — Record screencast demos (FliCast)

| Sub-step | Route | State |
|---|---|---|
| Open on the project | `scripts/app.sh start --brand appydave --project …`, or `context.select {brand, project}`; check with `context.get` | WORKS |
| Choose screen, mic, camera, system audio | `recording.defaults.set` (`displayId:"main"`, `microphone`/`camera`: `"none"` or a device id). `null` = not chosen → refused `notChosen` | WORKS, with a gap: `recording.devices` is ★, so an agent can't list the real device ids |
| Name the cast, pre-flight | `recording.arm {name}` (a taken name is refused `exists`); `recording.check` lists missing permissions | WORKS |
| Record and stop | `recording.start` / `stop` / `cancel` | ★ **human-only by design**. The one-time Screen Recording permission for "FliCast" and Relaunch are a person's too |
| After the take | `recording.state`, `project.list`, `project.open`, `project.rename` | WORKS |
| Export | `export.presets` → `export.start {projectId}` (no path = default) → poll `task.status` | WORKS |

- **Writes**: `fli.cast.<name>.json` + `cast/<name>/recording/` at the take; `videos/<name>/<name>-final.mp4`
  at export. FliStudio's Start an edit picks up that final export (and the raw scenes if asked).

## Step 5 — Start the edit (FliStudio → FliCut) · WORKS (not yet watched live end to end)

- **Pick the files**: `assets.list {brand, project}` returns recordings, footage and casts (final exports,
  raw scenes).
- **Call**: `edit.start {brand, project, name:"<kebab-name>", files:[project-relative paths in timeline order], ifExists?:"refuse"|"open"}`
- FliStudio checks each file is inside the project, starts FliCut if needed, and calls FliCut
  `POST /api/video/open {brand, project, video, create:true, files:[absolute], ifExists}` with FliCut's
  token. FliCut writes `fli.cut.<name>.json`; FliStudio writes nothing.
- **Refusals**: `edit-exists` (409), `file-not-found`, `app-unavailable`.
- **Progress**: `edit.status` reads FliCut's `GET /api/status` (which edit is open, transcription progress).

## Step 6 — Cut and export (FliCut)

| Sub-step | Route (all on `127.0.0.1:7121`, bearer token) | State |
|---|---|---|
| Receive the hand-off | `POST /api/video/open {…, create:true, files, ifExists}` | WORKS. Opens a window if none |
| Transcribe | automatic when a **window** has the edit open (mlx-whisper large-v3, word timings; ~4 min for 19 min of audio). Headless alternative: `POST /api/projects {name, files, process:true}` → job, poll `GET /api/jobs/:id` | WORKS in the window. **MISSING**: no verb to transcribe an existing edit headless |
| Watch progress | `GET /api/status` → `transcribing {current, total, phase, pct}` | WORKS |
| Cut pauses and "ums" | `PATCH /api/projects/:id/params {pauseDuration, paddingStart, paddingEnd, cutFillerWords…}`; dry run `POST /api/projects/:id/cuts?preview=1`; mask a clip `PATCH /api/projects/:id/segments/:clipId {isCut}` | WORKS at clip level. **MISSING**: word-level split/trim over HTTP (window only). **BROKEN (FC-33)**: if the window has the same edit open, its next save overwrites agent edits. Close the edit in the window first |
| Audio clean-up + export | `POST /api/projects/:id/export {arms:["none","a100","a12"], formats?:["mp4","srt"]}` → job | WORKS. Writes `videos/<name>/<name>-cut.mp4` (plain) and `<name>-audio-a100.mp4` etc. 409 `export-exists` unless `overwrite:true` |
| Mark the final | FliCut never writes `-final`. FliStudio `export.place --kind final` places the chosen file | WORKS |

## Transcription across the steps · works three ways today, one way planned

- **Today**: FliHub transcribes a take when it's promoted, into `hub/transcripts/`, **without** word
  timings. FliCut re-transcribes every clip itself, **with** word timings, when an edit opens. FliCast
  transcribes only on "Generate captions". None of them reuses the others' work.
- **Planned (FliTools, no code yet)**: one always-on service. It returns word-timed JSON, saves
  json/srt/txt in `transcripts/` beside the recording by default, and reuses a transcript of the same
  content. Groq first, local mlx-whisper as fallback, one job at a time. FliCut derives its edited
  transcript from those raw words. Still open: whether apps call it directly or through fli-core.

---

## Gaps that block an autopilot run

Ordered by how early they stop the run.

1. **Recording is human-only.** Ecamm record (FliHub) and FliCast record/stop are a person's action by design. Autopilot means "a person presses record; agents do everything else".
2. **No agent can quit or restart an app.** Only `scripts/app.sh` from a shell. FliStudio `app.stop` / `app.restart` for every app is being built now.
3. **Camera footage has no import.** A person copies Pocket 4 clips into `footage/`. `footage.import` needs David's ruling on copy vs move, source and renaming.
4. **FliHub's aspect-check race.** An agent that renames a take too fast skips the check silently.
5. **FliCut transcription needs a window.** No headless verb transcribes an existing edit (the separate `process:true` pipeline does, for a new one).
6. **FliCut cutting over HTTP is clip-level only.** Word-level split/trim is window-only, and an open window overwrites agent edits on its next save (FC-33).
7. **Transcription is done three times, differently.** FliHub (no word timings), FliCut (word timings), FliCast (captions). FliTools, one shared service, is designed but not built.
8. **FliCast can't list real mic/camera devices for an agent** (`recording.devices` is human-only), so an agent can pick only "main" / "none" or known ids.
9. **Teletubby opens the wrong script set** when a project already has one attached, and there is no link between a script and a FliHub take.
10. **Uneven agent doors.** FliStudio has no token yet; FliHub has no token, CLI, MCP or capability list; only FliCast has MCP. The shared agent layer (fli-core: capability contract, human-only flag, numbered refusals, discovery file, OpenRPC docs page and console, lifecycle verbs) is being built now and adopted by FliStudio, Teletubby and FliCut.
11. **Not yet watched live end to end.** Start an edit → FliCut and the FliCast naming change are proven in tests, not on a real run this week.
