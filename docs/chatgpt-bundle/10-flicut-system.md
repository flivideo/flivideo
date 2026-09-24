<!-- FliVideo source bundle · flicut SYSTEM · generated from flicut/docs/SYSTEM.md -->


# FliCut — System Context

For people new to this codebase. Agents get the short version in
[AGENT-NOTES.md](./AGENT-NOTES.md). The rules not to break are in [`CLAUDE.md`](../CLAUDE.md), and
this page does not repeat them. The product tour is in [`README.md`](../README.md). These docs follow
the suite's [agent comprehension docs method](https://github.com/flivideo/flivideo/blob/main/docs/agent-comprehension-docs.md).

> **Schema mirror.** [`schema-mirror.md`](./schema-mirror.md) holds every type, Zod schema and closed
> set, generated from the code with `file:line` (regenerated 2026-09-23 with dev-team 0.4.0, which binds
> `z` through `@appydave/core`). Its recorded gaps — scalar constants and the `z.infer` aliases of
> object schemas — are listed on the page; read those in source.

## Purpose

FliCut lets David cut one video from the recordings and footage he hands it, by editing its
word-level transcript on his own Mac, and get back an MP4 with the right cuts and the right
loudness. It replaced Gling, which got the same few things wrong on every chapter.

## Core Abstractions

- **Media → Take → Element (the transcript)**: a *media* is one source file. Transcription
  splits it into *takes*: runs of words separated by pauses. A pause is a take with no words.
  *Elements* are the words and punctuation, each with its own source timing
  (`src/shared/project.ts`). Only transcription writes takes. After ADR-0002 no edit gesture
  changes them. They stay the ASR's record of what was said.
- **Clip (the timeline)**: a clip points at `(mediaId, takeIndex)`, has `start`/`end` in source
  time and an `offset` on the output ruler, and has a decision (`isCut`) plus who made it
  (`cutBy: 'proposal' | 'user'`). Several clips may share one take. A word belongs to whichever
  clip holds its **midpoint** (`elementsWithin`, `src/shared/layers.ts`). The timeline stores
  `clipsWithCuts` (every segment) as the truth. `clips` (kept only) is rebuilt from it on every
  write.
- **Proposal versus decision**: `take.cut` is what the engine suggests (silence, filler, or
  nothing). `clip.isCut` is what happens. `cutBy: 'user'` protects a clip from the next proposal
  run (`applyProposals`). The four operations on the timeline are MASK, TRIM, SPLIT and GAP
  (ADR-0001). In the code, "cut" as a verb always means MASK.
- **Edit location (where an edit lives)**: an edit is addressed by a *ref* string. For a
  *contract* edit that is the path of `fli.cut.<name>.json` inside a video project. For a
  *legacy* edit it is the path of a `project.json` folder. `EditLocation`
  (`src/main/edit-location.ts`) turns a ref into every path that edit uses: the decision file,
  sidecars, work dir, exports, view state and undo history. Each layout is kept as it is. Neither
  is converted into the other.
- **Open context (brand / project / video)**: a context for this run only. Three ways in (the
  picker, launch args, HTTP/CLI) all go through one resolver (`src/main/open-context.ts`, built on
  `@flivideo/core`). While a context is open it replaces the stored folder settings. It is never
  saved.

These fit together like this: open a context → find the edit for its location → load the takes
and clips → edit the clips → write through `ProjectStore`, which saves an undo snapshot. The cut
engine only writes proposals. The exporter only reads kept clips.

## Key Workflows

### Start an edit from FliStudio (the normal way in, since 2026-09-22)
1. In FliStudio David names the edit, ticks sources (recordings, footage, cast) and orders the
   clips. FliStudio chooses; FliCut is handed the result (FC-37) — it looks in no folders itself.
2. FliStudio makes ONE call: `POST /api/video/open {brand, project, video, create:true,
   files:[absolute, in order], ifExists}` (`src/main/app-core.ts` `openVideo`). It re-points the
   context, creates `fli.cut.<name>.json` with the files in exactly that order, and refuses an
   existing name with `409 edit-exists` (FliStudio then offers "open it as it is" or another name).
3. The window shows the edit and comes forward — opened fresh if FliCut had no window
   (`src/main/handoff-window.ts`). This matters: **transcription is driven by the window**, so a
   hand-off with no window would create the edit and then do nothing.
4. `GET /api/status` reports `transcribing {current, total, phase, pct}` so FliStudio can show
   "FliCut is transcribing 2/5"; the editor shows a full-width banner at the same time.

### Cut a video by hand
1. Open a context (`scripts/app.sh start --brand … --project …`, or the picker), or open a legacy
   project under the settings root (`~/Movies/FliCut` by default, `src/main/index.ts`).
2. **+ New edit** starts pre-filled with the project's recordings in chapter order, found through
   `@flivideo/core`'s layout (`projectRecordings`, `src/main/open-context.ts`); add, remove and
   reorder freely. The aspect is the project's *stated* aspect (`fli.studio.json`), else it
   follows the footage. With a context open, media must be inside the project
   (`assertInsideProject`). Each media starts as one placeholder take covering the whole file.
3. Transcription starts when the edit opens (`Editor.tsx`), one file at a time: `mlx_whisper` with
   word timestamps, the dictionary as `--initial-prompt`, `ffmpeg silencedetect` to check word
   timing, then `segmentTakes` (`src/main/transcriber.ts`, `src/shared/transcript.ts`). A file's
   placeholder clips are dropped on its first transcription (FC-39).
4. `proposeCuts` labels the takes, and `applyProposals` projects the labels onto the clips. The
   first and last takes are never cut by default.
5. David clicks words and pause pills to mask or restore them, trims the head and tail at the
   playhead, and sets pause lengths. Each gesture is a pure function in `layers.ts` returning a new
   `Project`, and each save adds a lab snapshot, so ⌘Z works.
6. He exports. The export panel's checkboxes pick the audio clean-ups — *Off*, *Strong* (a100,
   ticked by default), *Gentle* (a12) — one file each from ONE shared render (`exportArms`).
   `buildPlan` snaps each segment to frames once; ffmpeg re-encodes (word-level cuts cannot be
   stream-copied). Names follow D15 (`@flivideo/core` v0.3+): `videos/<name>/<name>-cut.mp4` for Off,
   `<name>-audio-<token>.mp4` for a clean-up; a legacy edit writes to `exports/`.

### Audit what was removed
1. Press **I** (inverse cuts). The playlist plays only the masked material, which takes about 10 s
   for a 70 s chapter (README).
2. Anything restored becomes `cutBy: 'user'`, so re-running Pace will not overwrite it.
3. `GET /api/projects/:id/overrides` lists every clip where David disagreed with the engine
   (`diffLayers`).

### Drive it without the window (Cutty or a script)
1. Start it headless: `FLICUT_HEADLESS=1` gives the control surface with no window
   (`src/main/index.ts`). The port and bearer token are in `control.json` under userData, file
   mode 0600.
2. Point it at a context: `POST /api/context` or `bin/flicut open …`, then `POST /api/video/open`.
3. Use the five verbs over HTTP: create, add media, set params (`PATCH …/params`), propose
   (`POST …/cuts`, with `?preview=1` for a dry run) and export (`POST …/export`). Long verbs return
   202 with a job id, which you poll at `/api/jobs/:id`.
4. `POST /api/batch` and `POST /api/projects {chapter}` select takes by `NN-` file prefix. That is
   the no-context workflow only: inside a project there is no takes folder, and both answer
   `409 no-takes-folder` (FC-37).

### Compare audio treatments
1. `POST …/export { arms: ['none','a100','a12'] }` decodes and renders once, then applies each arm
   to a copy (`exportArms`, `src/main/pipeline.ts`).
2. The levels summary reports LUFS and LRA. It never ranks the arms. David picked a100 by ear, so
   the export panel ticks it by default (`EXPORT_DEFAULT_ARMS`, hard-coded — there is no Home
   default and no "remember my last choice"); the API keeps its own cascade.

## Design Decisions

- **The transcript is never edited. Only the timeline is (ADR-0002, "Future B")**: word masks
  splice clips, and takes stay as the ASR produced them.
  - *Alternative considered*: splitting takes so each take matches one clip ("Future A"), which
    shipped briefly on 2026-09-07.
  - *Why rejected*: fragments of a split became units the next proposal could re-label (U1).
    Nothing merged them back (U2). Masking a word could not be undone the way masking a pause
    could, and marker anchors broke on every mask. Future B removes all of these problems instead
    of patching each one.
- **User trims are SPLIT + MASK, not changes to source ranges (ADR-0003)**: head/tail trims and the
  pause chip leave the frames reachable, so every trim shows as frost and Uncut reverses it.
  - *Alternative considered*: really moving `srcIn`/`srcOut`.
  - *Why rejected*: it strands source material or needs GAP, which is parked. It can't be undone
    without a journal, and it loses the frost David asked for.
- **Undo is a snapshot history in the lab, not git (ADR-0004)**: every write saves a copy of the
  edit file under `<lab>/history/`, keeping the newest 100 (`src/main/edit-history.ts`).
  - *Alternative considered*: a git repo per edit (the old way), a lab git repo with `--work-tree`,
    or undo held in memory.
  - *Why rejected*: a nested repo inside a brand repo is invisible to the brand repo. A lab repo
    needs an explicit `GIT_DIR` on every call. In-memory undo would lose undo across restarts,
    which is still an open question in spec §12.
- **An audio arm is an export-time setting, and arms are a registry (FC-13)**: changing the arm
  changes no cut. Adding an arm means adding a `ARM_REGISTRY` entry and an `audioProfileSchema`
  value.
  - *Alternative considered*: a switch statement, or picking the "best" arm automatically by
    SNR/LUFS.
  - *Why rejected*: a12 measures best and audibly buzzes, so a metric would pick the wrong arm.
    David's ear decides.
- **Context lives only for the session, with one resolver for three doors (W4, C2/C4)**: the
  context is held in memory and never written to `settings.json`.
  - *Alternative considered*: saving the last project in settings.
  - *Why rejected*: a plain `npm run app` must behave as before (README §Open contract).
    `[inferred]` The same failure has happened before: a session-scoped `FLICUT_PROJECTS_ROOT` got
    saved into the real settings and pointed the app at a temp dir (learnings 2026-08-31,
    "[batch] Session env must never seed durable config").
- **FliCut is handed its inputs (FC-37, David 2026-09-22)**: a new video is created from an explicit,
  ordered file list; nothing is read from, or refused against, FliHub's recordings folder.
  `@flivideo/core`'s layout only sets where a file dialog opens and what + New edit pre-fills.
  - *Alternative considered*: `recordings/<NN>-*` as the input truth (the chapter model).
  - *Why rejected*: FliCut is an editor that is handed its inputs; FliHub's folders moved
    (`hub/recordings`), and D01's footage lived in `footage/` — a hard-coded folder refused real work.
- **The control surface is loopback HTTP, not IPC**: Electron IPC can't be reached from outside
  the process, so Cutty and the skill drive `127.0.0.1:7121` with a bearer token.
  - *Alternative considered*: a CLI that edits the files directly.
  - *Why rejected* `[inferred]`: that would skip the Zod validation, the undo snapshots and the
    per-edit write serialisation that `ProjectStore` provides.
- **One seam under every HTTP door (ADR-0005, fli-core v0.7.3)**: each REST route and each JSON-RPC
  call (`/api/rpc`) is a named capability (`src/main/capabilities.ts`) run through
  `ControlSurface.call`, which applies fli-core's ★ fence before any handler. The spec
  (`api/openrpc.json`), the reference page (`/api/docs`) and the console (`/api/console`) are
  generated from the same contracts. Agents can quit or restart FliCut (`system.quit` /
  `system.restart`, or `bin/flicut quit|restart`) unless it is busy transcribing, exporting,
  running a job or saving. `force` is a person's, and so is `overwrite: true` on an export.
  - *Alternative considered*: JSON-RPC only, or moving the window onto the core as well.
  - *Why rejected*: FliStudio, the CLI and the skill call the REST paths; moving the window is the
    audit's L item and would change the live instrument. The window's IPC still bypasses the
    seam; FC-33 is closed separately (outside writes are pushed to the window, and a window save
    that has not seen one is refused, `src/main/edit-sync.ts`).

## Non-obvious Constraints

- **Stored clip bounds on a masked clip are raw, and kept neighbours are padded.** A kept edge next
  to a mask sits `paddingEnd`/`paddingStart` inside the masked material. Anything that reads a
  boundary has to know which one it has. `nudgeBoundary` got this wrong on 2026-09-07 and moved
  the boundary the wrong way.
- **"Typed 0.3 s" is not "heard 0.3 s".** The pause chip sets the raw kept span, and padding adds
  up to `paddingStart + paddingEnd` on top. ADR-0003 accepts this deliberately.
- **Audit mode is cleared on open.** `ProjectStore.open` always resets `inverseCuts` to false,
  because a project that silently reopened in inverse mode was reported as "playback broken".
- **An edit opened in context scope has to belong to the open project.** `locate()` refuses a
  `fli.cut.*.json` ref when no context is open, or when the file sits in a different project.
- **Exports of contract edits have exact names and are never auto-numbered.** An existing target
  returns `409 export-exists` before anything renders. `overwrite: true` renders to
  `.<stem>.pending.*` and renames only after success. Legacy edits still get `-2` names.
- **A missing required settings field loses the user's saved folders.** `settings.ts` falls back
  to the defaults wholesale when parsing fails, so any new field needs `.default()` (as
  `defaultArm` has).
- **A new edit is built on placeholder takes.** `store.create` gives each media one whole-file take
  (so an untranscribed edit is still a valid timeline) and a clip on it. Transcription replaces the
  takes; its clips must go with them (`dropPlaceholderClips`), or the stale whole-file clip survives
  beside the real ones — every edit made between 2026-09-07 and 2026-09-22 played each file twice
  (FC-39).
- **Only an aspect the project STATES counts.** `projectIntents()` fills in 16:9 for a project with
  none, which would hide "unset"; FliCut reads `identity.aspect` directly (`open-context.ts`), so an
  unset project still follows its footage. FliStudio's Create screen always states one.
- **Time is float seconds everywhere except the export plan and the display.** Frames exist only
  in `buildPlan`, which snaps once, and in `fmtTimecode`, whose third field is frames.
  `docs/units-contract.md` is the rulebook.

## Expert Mental Model

- **Think in decisions over words, not clips on a track.** A newcomer looks for "delete this
  clip". An expert asks which words and pauses are masked, and who masked them. The timeline is a
  rendering of that answer.
- **The diff between the two layers is the product data.** `diffLayers` is not a debug view. It is
  where David disagreed with the engine, and it is how the engine gets tuned against Gling
  (learnings 2026-08-31, IoU 0.957).
- **Every edit is a pure `Project → Project` function, and the store is the only writer.** To
  know what a gesture does, read its `layers.ts` function. To know whether it persisted and can be
  undone, look only at `ProjectStore.write`.
- **The ref tells you the layout.** `isContractRef(ref)` decides everything that follows: relative
  paths, lab work dir, exact export names. When something is in the wrong place, first check which
  layout the ref resolved to.
- **The window is part of the pipeline, not just the view.** Auto-transcription is a renderer
  effect, the hand-off needs a window to show, and every window restores its spot from the shared
  `~/.fli/window-state.json` (`@flivideo/core` v0.4+, keyed `flicut/main` / `flicut/scratch`). When
  "nothing happened", first ask whether a window existed.
- **Distrust checks that read the app's own bookkeeping.** The playlist clock, a green typecheck
  and a clean HMR log all report what the app believes. Promoted pattern P1
  (`docs/kdd/patterns.md`) says to prefer the layer that is not under test (presented frames, a
  screenshot, an ffprobe of the output).

## Scope Limits

- Does NOT do diarisation, bad-take detection, captions, auto-zoom or CTA overlays. The
  `cutBadTakes` toggle is stored so it round-trips, and nothing acts on it (`project.ts`).
- Does NOT correct transcripts after ASR. The dictionary only seeds `--initial-prompt`, so a
  mangled proper noun cannot be fixed, and a hand fix would be lost on re-transcription. Where
  corrections should live is an open ADR (learnings 2026-09-07).
- Does NOT own brand/project identity. It reads `brands.json`, `fli.studio.json` and
  `~/.fli/machine.json` through `@flivideo/core`
  (`fli-core`), and FliStudio's `docs/open-contract.md` owns
  the contract.
- Does NOT choose its own sources. Which files make a video, and in what order, is FliStudio's job
  (or David's, in + New edit); FliCut takes the list it is given.
- Does NOT reuse a transcript it did not make. There is no import door (FC-30), and its cache is
  keyed by a media id minted per edit, so re-creating an edit re-transcribes.
- Does NOT migrate legacy `project.json` edits into `fli.cut` files. That is a separate step, done
  deliberately on a copy.
- Does NOT commit or `git init` anything. Undo history is per machine and does not travel.
- Does NOT support NTSC-exact timing. Framerate is a float, which is fine at integer rates
  (`docs/units-contract.md`, known limit).

## Failure Modes

- **Blank window, every gate green**: something from `project.ts`/`ipc.ts` was value-imported into
  the renderer, which pulls Zod and Node built-ins into the bundle. No error appears. Recognise it
  by screenshot (`scripts/dev-shot.sh`) or CDP, never by the main log.
- **Renderer shows new behaviour while main runs old code**: electron-vite HMR reloads the
  renderer, including `src/shared`, but never main. The log looks clean either way. Saves and
  exports then run the old model against the new renderer. Restart after changing `src/shared` or
  `src/main`.
- **"This edit was changed outside the window" (FC-33, fixed 2026-09-23)**: an agent wrote the edit
  while David's save was in flight. His change was refused, not written, and the window now shows
  the disk. It is by design: before the fix the window's save silently replaced the agent's write.
- **Hand-off made the edit, but nothing happened**: FliCut was running with its window closed. Fixed
  2026-09-22 (`bringUpForHandoff` opens a window when none exists and logs `[handoff] …`). If it
  recurs, `GET /api/status` shows `window.open:false` and `transcribing:null`.
- **"no brand project" and empty folders on a reopened window**: the ES-module preload
  (`window.flicut`) can arrive after the page's first script. `boot()` now waits for it
  (`src/renderer/src/bridge.ts`); a genuine failure shows an error instead of a silently wrong screen.
- **"Stopped", but FliCut is still running** (fixed 2026-09-23, `d4c4e2e`): `electron-vite dev` does not forward
  signals, so FliCut's Electron could outlive it as an orphan (ppid 1), and `app.sh stop` used to report success when
  overmind exited. Now `stop` checks `/api/health` and FliCut's own pids, escalating SIGTERM → SIGKILL, and `start`
  clears an orphan. The quit path cannot be blocked by a throw or an EPIPE (`src/main/quit-guards.ts`). If it
  recurs: `pgrep -fl 'flivideo/flicut/node_modules/.*Electron.app/Contents/MacOS/Electron'` and `ps -o ppid=`.
- **Something started twice after reopening from the Dock**: on macOS `activate` re-runs `onReady`.
  Anything it starts must be idempotent — the control surface once re-bound 7121, hit EADDRINUSE and
  nulled its own handle.
- **Every clip plays twice after the first transcription**: placeholder clips were not dropped (see
  Non-obvious Constraints). Check `clipsWithCuts` for a `[0, duration]` clip beside real ones.
- **The first change to an old edit cannot be undone**: this was fixed by the `baseline: on disk`
  snapshot (W4 review F2). If undo ever returns `null` on an edit with history, check that
  `#baseline` still runs inside the same `serialise()` step as the write.
- **Audio arm stalls after `hp.wav` in an isolated run**: `HOME` was overridden, so
  `~/bin/deep-filter` and `~/.local/bin/mlx_whisper` no longer resolve. Set `DEEP_FILTER_BIN` /
  `FLICUT_MLX_WHISPER`. Treat it as a test-harness problem, not a product bug.
- **A style silently does nothing**: Tailwind opacity modifiers on bare `var()` colours compile to
  no CSS. Check with the compiler probe before debugging React (learnings 2026-09-07).
- **Loudness misses target**: with the limiter engaged, gain is not linear. The chain measures
  again after the limiter and corrects, up to `MAX_LEVEL_PASSES = 5` passes
  (`src/main/audio-chain.ts`).

## The open contract and where an edit's files go (moved from the README, 2026-09-23)

FliCut opens the same way as every FliVideo app (FliStudio `docs/open-contract.md`):
a **brand**, a **project** and optionally a **video**, through three doors that share one resolver
(`src/main/open-context.ts`, on [`@flivideo/core`](https://github.com/flivideo/fli-core)).

| Door | How |
|---|---|
| 1 · Picker | Header button or Home → brand → project → video (plain list; the real design is FliStudio's) |
| 2 · Launch | `scripts/app.sh start --brand appydave --project a01-xmen --video flivideo-tour`, or `FLIVIDEO_BRAND` / `FLIVIDEO_PROJECT` / `FLIVIDEO_VIDEO` (argv wins). Already running? The same command re-points it through door 3 |
| 3 · API / CLI | `POST /api/context { brand, project, video? }` · `GET /api/context` · `POST /api/video/open { brand?, project?, video, create?, files?, ifExists? }` on the control port — FliStudio's one-call "Start an edit" hand-off: files in timeline order, `409 edit-exists` unless `ifExists:"open"` · `bin/flicut open --brand … --project … [--video …]`, `bin/flicut video flivideo-tour [--create footage/01-a.mp4 …]`, `bin/flicut context` |

- **The context belongs to this run (C2).** It is never written to `settings.json`. With no context,
  the stored settings (`projectsRoot`, `recordingsDir`, `deliverDir`) are the fallback — a plain
  `npm run app` behaves as before. While a context is open, `GET /api/settings` shows the context's folders;
  `PATCH /api/settings` ignores those folders when they are echoed back unchanged and refuses a changed one with
  `409 context-open`, so a read-modify-write client cannot make a project's folders the global defaults. The
  window reads and writes settings through the same guard, and its Home panel shows the project's folders read-only.
- **FliCut is handed its inputs (FC-37).** Inside a project there is no takes folder: `recordingsDir` reads `""`,
  chapter-by-prefix (`POST /api/projects {chapter}`, `/api/batch`) is refused `409 no-takes-folder`, and a new video
  is created from the files it is given — `POST /api/video/open { video, create: true, files: [...] }` (relative
  paths are the project's) or **+ New edit**. `@flivideo/core`'s layout (`hub/recordings` or `recordings`) only
  sets where the file dialog opens (`context.inputHint`); nothing is read from it or refused against it.
- A malformed `POST` body (wrong types, not JSON) is `400 invalid-body` with the issues, never a 500.
- `GET /api/context` → `{ context, missing, picker, refused? }`. **Check `refused` first**: it is the
  last *launch* that could not resolve; the context beside it is unchanged. API refusals come back
  in the HTTP response and are never kept.
- A project is a folder name, a `fli.studio.json` id, or a whole code (`a01`). A code is matched over
  members **and** plain folders: one match opens it, two or more refuse. A folder without
  `fli.studio.json` opens as `membership: "folder"`.

**Refusal codes** are one vocabulary across the Fli apps, held in `RefusalCode`
([`schema-mirror.md`](./schema-mirror.md)) and mapped to their `@flivideo/core` source in `REFUSAL_FROM_CORE`
(`src/main/open-context.ts`). FliCut never sends `not-a-project` (a plain folder opens as `membership: "folder"`),
and `video-not-found` means no `videos/<name>/` folder and no edit — another app's takes never count (FC-37).
FliCut-only codes: `edit-exists` and `outside-project` (the hand-off), `no-takes-folder`, `context-open`,
`export-exists`.

### Where an edit's files go

```
a01-xmen/                                   the video project (in the brand's one git repo)
├── fli.cut.flivideo-tour.json              the edit — every media path relative to the project
├── fli.cut.flivideo-tour/                  -words.json, -words.health.json, last-export.json
├── footage/01-intro.mp4                    source files you added (any folder in the project), never edited
└── videos/flivideo-tour/flivideo-tour-cut.mp4   the export (+ -cut.srt); a clean-up arm is flivideo-tour-audio-<token>.mp4

~/fli/lab/v-appydave/a01-xmen/flicut/flivideo-tour/
├── work/                                   filmstrips, peaks, WAVs, audio-chain stages, the audio-arms base render
│                                           and levels summary — regenerable
├── history/                                the undo stack (one snapshot per write)
└── viewState.json                          playhead, zoom — presentation, not a decision
```

**Exports have exact names, and a re-export asks first.** Videos are named, not numbered (D15, `@flivideo/core`
v0.3.0): `videos/<name>/` holds only `<name>-cut.<ext>` (untouched — also what *Off* writes) or
`<name>-audio-<token>.mp4` for a clean-up arm (`flivideo-tour-audio-a100.mp4`, kind `audio`). There is never a `-2` copy. If
the target exists, the export is refused before anything renders: `POST /api/projects/:id/export` answers `409
{ code: "export-exists", paths }`, a batch reports the chapter and moves on, and the editor asks *Replace it?*.
Passing `overwrite: true` (or confirming) renders to a hidden `.<stem>.pending.*` file and renames it over the
target only once the render and audio are done, so a failed render leaves the previous export intact. A call-layer
crop doesn't change the name, because it is part of the cut. Legacy `exports/` keep their old naming (pattern,
`--token`, `-2`).

**Media must live in the project.** A `fli.cut` edit travels with the brand repo, so a media file outside the
project (a take held on the T7, another project's folder) is refused on create and on save: copy it into the
project first. A climbing `../../Volumes/…` path would only work on this machine. Legacy edits keep
their absolute paths.

**Which file wins for a video**: `fli.cut.<name>.json` if it exists; otherwise a legacy
`project.json` edit in a folder of that name (in the project, a subfolder, or one level deeper,
e.g. `first-edit/<name>/`); otherwise none, and `create` makes a new `fli.cut` file. **Why the new file
wins, and the old one is never converted:** the contract file is where every Fli app looks, and a
legacy edit may be one David is still cutting. Converting it in place would change a live edit
under him. So a legacy edit is read and written where it is, with its own `work/` and `exports/`, and
only its undo history moves (`~/fli/lab/_legacy/flicut/<folder>-<hash>/history/`). Before each save and each
undo, FliCut checks that the newest snapshot matches the file on disk. If it doesn't (an edit from before W4,
a `git pull`, another machine, a hand edit), the disk bytes are recorded first as `baseline: on disk`, so ⌘Z
never skips past a state that existed. Moving a legacy edit
to the new layout is a separate, deliberate step (on a copy first), not something FliCut does on open.

**No git.** FliCut no longer creates a repo per edit or commits on save (roadmap §1.2c): undo is the lab
history above ([ADR-0004](kdd/decisions/adr-0004-undo-history-in-the-lab-not-git.md)). Existing nested
repos are left untouched.
