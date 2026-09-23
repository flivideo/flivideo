<!-- FliVideo source bundle · flicast SYSTEM · generated from flicast/docs/SYSTEM.md -->


# FliCast — System Context

The human orientation narrative. Not loaded into agent context; agents read `AGENT-NOTES.md`.
True at the `commit:` in the frontmatter (first written at `0a5d10c`, 2026-09-16). Every shape — the
document, the capability contract, the refusal details, the recording defaults — is in the generated
[`schema-mirror.md`](./schema-mirror.md), anchored to `file:line`; this page names them and never restates them.

## Purpose

FliCast lets David (and later members of his paid community) record a screencast and then have the
edit done **as data**, by a person in the editor or by an agent over the command line, with the same
verbs, the same undo and the same audit trail, so that "zoom in on the terminal between 2:12 and 2:18"
is one typed, dry-runnable, reversible call rather than a mouse job.

## Core Abstractions

- **The capability core** (`src/core`, pure TypeScript). One seam, `core.call(principal,
  name, input)`. The capabilities come in families (`project`, `scene`, `slice`, `zoom`, `mask`, `layout`,
  `cursor`, `marker`, `style`, `preset`, `overlay`, `output`, `audio`, `preview`, `export`, `history`,
  `context`, `settings`, `system`, `task`, `recording`, `suggestion`, `capabilities`) — the count is pinned in
  `test/capabilities.pinned.test.ts` and generated into `api/openrpc.json`. Each is a query,
  command, task or event with zod input and output, a side-effect class, failure modes and a principal
  allow-list. Everything else (IPC, the HTTP door, the CLI, the MCP server, the capability console, the skill) is an
  adapter over this seam. A refusal is data too: `failureMode` + a `details` object typed per mode
  (`src/core/refusal-details.ts`, ADR-0007) that carries enough to succeed on the next call.
- **The document** (`src/core/model/schema.ts`). A versioned, declarative edit: sources, scenes, slices
  (source range → playback with a time scale), zooms, masks, layouts, cursor ranges, markers, style,
  captions. The renderer holds a mirror and applies the JSON patches the core emits; it never edits it.
  Time in the API is milliseconds on the **output** timeline; records are stored in **source** time.
- **Principals and provenance.** Every call names who: `human:ui`, `cli`, or `agent:<name>` (`agent:mcp` for the MCP server,
  `agent:console` for the capability console). The kind
  (human / agent / cli) gates the verb; the string is recorded on every history entry, audit row and
  generated record, so `history.undoBy` can take back one principal's edits and leave the others.
  The ★ verbs (`HUMAN_ONLY` in `src/core/registry.ts`) are never reachable from outside the window.
- **Ports.** The core speaks to the world only through interfaces the main process implements:
  `StorePort` (packages, cast projects, home-level files), `RecordKitPort` (capture), `RenderPort`
  (frames and export), `CaptionsPort`, `AudioPort`, `SystemPort` (relaunch, dialogs, Finder, log tail),
  `ClockPort`/`RandomPort` (determinism), `OpenContextPort` (the brand/project the run is pointed at).
  Tests swap any of them; the uat harness swaps RecordKit and captions beneath the real app.
- **Two project forms, told apart only by the store.** A `.flicast` package
  (`~/FliCast Projects/<name>.flicast/project.json` + `recording/`) when no brand context is open; a
  **cast project** (`<projectDir>/fli.cast.<name>.json` + `cast/<name>/`, scratch in `~/fli/lab/…`) when
  FliCast was pointed at a video project. The core never parses a path; five `StorePort` methods carry
  the difference (ADR-0002).

## Key Workflows

### Record a take and land in the editor
1. The person opens the Record sheet and makes **every** choice on purpose — target, its display / window / device,
   microphone (or "No microphone"), camera (or "No camera"), system audio — and types a **Name**. Nothing is chosen
   on their behalf: until all are made, ● Record is off and `recording.arm` refuses `notChosen` listing each one
   (capture-choices-2026-09-22, David's rulings after his first real capture). Device lists are re-read on focus, on
   a grant change and on a 10 s poll while the sheet is on screen, because RecordKit has no device-change event.
2. **● Record** → `recording.arm { name }` (the destination of the take is snapshotted **now**: a name means a NEW
   cast project — a taken name is refused before anything is recorded; without one, into the open cast project as
   its next scene, else `<home>/recordings`) →
   `recording.start`. The core runs a real `countdown` state, then `preparing` with a 15 s bound and one
   automatic retry, then `recording`. The HUD (a small always-on-top window, content-protected so it is
   absent from the video) shows the phase and only the buttons that phase accepts.
3. **■ Stop** → `stopping` → `ingesting`: the RecordKit bundle (`screen-0.mov`, `mic-0.m4a`,
   `input-events.json`) is adopted into the project, the auto-zoom generator runs over the click log,
   the project opens, the editor comes forward and draws the first frame with no click.
   "Stop & start a new scene" ingests the take as scene N and re-arms into the same project.

### Edit from the command line (the skill's loop)
1. `flicast context active --json` → which project is active (or a hint to open one).
2. `flicast preview timeline` → the whole edit as text; `zoom list`, `slice list` … for detail.
3. Every command `--dry-run` first: the answer carries the JSON patch, its inverse and warnings.
4. Apply with `--idempotency-key <run>:<n>` (a retry replays the first answer instead of editing twice).
5. `flicast preview frame --at 2:15 --width 640` → a PNG rendered headless in the hidden worker window.
6. `flicast history undo-by --principal agent:claude-code --steps 2` → only that principal's edits go.
   Order matters: add the zoom, then change the speed (records live in source time).

### Drive it from an MCP client, or read the API
1. `.mcp.json` registers `bin/flicast-mcp.mjs`: a stdio JSON-RPC server that forwards to the running app's
   `POST /v1/rpc` as `agent:mcp`. It reads `control.json` for the token, so the app must be up.
2. The door speaks two envelopes over one `core.call`: the original `POST /v1/call` (the CLI and the skill)
   and JSON-RPC 2.0 at `POST /v1/rpc`, with integer error codes that are never renumbered (ADR-0006).
3. The app serves its own reference at `GET /v1/docs` (the generated `api/capability-surface.html`) and
   `GET /v1/openrpc.json`. The same page opens inside FliCast as the capability console (status line
   `N capabilities` / `agent door open`, or Help → Capability console…), where every verb is callable
   as `agent:console` and the ★ verbs are attempted and refused in front of the reader (ADR-0008).

### Export
1. `export.start { presetId, path, overwrite? }` is a Task: it returns a `taskId` at once; progress
   streams as `task.progress` events (transient, never replayed).
2. The hidden render-worker window decodes with mediabunny + WebCodecs, composites in PixiJS with the
   same code the preview uses, encodes H.264, and streams chunks to main, which writes them at their
   byte positions. Audio (mic, slices at speed, generated click sounds) is mixed offline in the worker.
3. Markers become MP4 chapters (an ffmpeg remux; a `.chapters.txt` sidecar when ffmpeg is missing).
   GIF goes through ffmpeg + gifsicle. An existing target is never truncated before the encoder exists
   (`.partial`, then rename); replacing one needs `overwrite: true` + `confirm: true`.
4. With no path, a cast project exports to `<projectDir>/videos/<name>/<name>-final.<ext>` (fli-core names it; David's
   "one shape everywhere", the same as FliCut) — where FliStudio's "Start an edit" offers it as the take's Cast item.

### Open FliCast on a brand's video project (the open contract)
1. `scripts/app.sh start --brand appydave --project a01-xmen [--video xmen]` (FliStudio's door 2 runs the same line)
   builds, then starts FliCast **as its own macOS app** through LaunchServices, the flags as its argv → one resolver
   (`src/main/open-context.ts`) over `@flivideo/core` v0.4.1. Already running? The same command re-points it through
   `flicast context select` instead of restarting; `app.sh show` brings it forward.
2. The context belongs to the run (never written to settings). A refusal is typed (`unknown-brand`,
   `project-ambiguous` …) and leaves the previous context untouched.
3. `project.create { name }` then makes `fli.cast.<name>.json` + `cast/<name>/` at the top of that video
   project, and takes are captured straight into it.

## Design Decisions

- **Editing logic lives in the Electron main process, inside a pure core, not in the renderer.** So
  every edit is reachable headlessly (CLI, HTTP, tests in plain Node) and the UI is one client.
  *Alternative*: edit in the renderer and save whole documents, as Screen Studio does. *Rejected*: a
  verb that exists only in a window is unreachable from outside, whatever the CLI claims (the ImageDrip
  trap named in `docs/spec/agent-surface.md` §7).
- **Authorization by principal kind in the core, not at the door.** Deleting the CLI changes nothing;
  a new adapter cannot widen the surface by accident. *Alternative*: per-adapter allow-lists.
  *Rejected*: the seam between adapters is exactly where the quality-3 audit found an S8 bypass.
- **RecordKit as the capture engine, on a trial now and a $500/year indie licence before the first
  outside distribution** (ADR-0001). *Alternatives*: Screen Studio's bundled recorder (one display, no
  licence path), a bespoke Swift capture binary (months). *Rejected*: RecordKit gives multi-display sync
  and the input-event log the agent-first editor depends on.
- **A UI gesture is one undo entry, merged in the core by an explicit gesture id** (fixes-2026-09-14b).
  A slider drag is many `style.set` calls; each still flows through the one core path so the preview and
  every other client stay truthful, and the entry merges. *Alternative*: commit only on release.
  *Rejected*: it needs a second, optimistic document path in the renderer that drifts from the core,
  and a lost release event silently drops the edit.
- **Optimistic version check instead of a command mutex** (quality-8 AR-1). A command that started on
  an older document is refused with `conflict`. *Alternative*: a mutex around `core.call`. *Rejected*: it
  deadlocks `recording.stop → ingest → project.create` and any handler that invokes another verb.
- **Cast projects inside the video project, scratch in the lab, no nested git** (ADR-0002). FliStudio
  and agents see FliCast's work with `ls fli.*.json`; the brand repo tracks the decision file; captures
  are already in the project when the take ends. *Alternative*: keep `.flicast` packages under `cast/`.
  *Rejected*: a hidden scratch folder and a generic `project.json` invisible to the `fli.*.json` rule.
  Undo never used git (measured before the flip), so stopping the repos was a default change.
- **JSON-RPC 2.0 at the door, additive** (ADR-0006). The door was already RPC in a private envelope;
  adopting the standard one made the MCP server a thin adapter. *Alternative*: a REST resource model.
  *Rejected*: the operations are acts on a document and its history (`slice.merge`, `history.undoBy`), and
  the ★ fence is on acts, not nouns — a URL space has nowhere to put it. `/v1/call` stays; nothing deprecated.
- **A typed verb per closed sub-object, never a document-wide patch** (ADR-0004). `output.set` is the first;
  `scene.set` and `project.settings.set` are ruled but not built. *Alternative*: one `document.patch`.
  *Rejected*: it would bypass per-field validation and the ★ fence on privacy-relevant fields (`fps` is
  deliberately immutable — every generated record was computed against it).
- **Two tests instead of ESLint for the dependency boundaries.** `core-boundary` and
  `renderer-boundary` are greps with positive controls, inside `npm test`. Adding ESLint is a new
  devDependency and David's call (W5 review F8).

## Non-obvious Constraints

- **The `@appydave/core` link is relative to the repo and must be built.** `file:../../apps/
  appydave-foundation/packages/core` resolves against the clone's location; the package's `dist/` is
  what the import finds. A clone anywhere else, or an unbuilt foundation, typechecks with "Cannot find
  module" and 11 main-process test files fail to load while the build still passes.
- **macOS grants Screen Recording to the RESPONSIBLE process, which is inherited down the launch chain.**
  Under overmind FliCast was a child of a tmux server, so the same build recorded when started from iTerm and was
  denied from a tmux-rooted launcher (2026-09-22). `scripts/app.sh` now starts it through LaunchServices from a launcher
  bundle ("FliCast", `com.appydave.flicast.dev`, remade only per Electron version), so FliCast holds its own grant.
  The app must still be restarted after granting (R-TCC); `npm run dev` runs as a child and gets its parent's grant.
- **Without the Screen Recording grant, RecordKit lists no displays.** That is the truth, not a stuck
  helper. The M4 (no grant) sees `displays: []` from every enumeration; the restart-the-helper recovery
  fires only when the Mac has displays **and** the grant is present.
- **"App must be running" is inherent.** Rendering needs the hidden worker window, so the CLI exits 2
  with the launch line when there is no `control.json`.
- **The principal is self-asserted.** One bearer token per launch; the caller names itself in
  `X-FliCast-Principal`. The kind cannot escalate past agent/cli, but the name in provenance is
  attribution, not identity (agent-surface §3, Q-A1).
- **Zoom first, then change speed.** Records are in source time; a zoom added over output 2:12–2:18
  stretches with a later slow-down. Slowing first moves output 2:18 to a different source time and a
  zoom added afterwards covers half the span. The spec's own transcript got this wrong; the L11 parity
  test pins the right order.
- **A zoom spans at least 1 s of source and may not overlap another zoom** (refused, not merged;
  `fit: true` finds the nearest free gap). Slices are at least 100 ms.
- **`npm test` and the uat app must not run at the same time.** The vitest workers starve Electron's
  renderers and CDP calls time out at 15 s.
- **An agent session cannot record or take OS screenshots** (no Screen Recording grant for the tmux server).
  A real capture is HUMAN: a person at the screen of a Mac whose FliCast holds the grant. The harness swaps a fake engine beneath the adapter (`APP_TEST_HOOKS=1 FLICAST_FAKE_RECORDKIT=1`) to
  drive the lifecycle end to end.
- **Window positions are not FliCast's own.** They live in fli-core's store shared with FliCut and Teletubby
  (`~/.fli/window-state.json`, keyed `<app>/<role>`), found through the account's real home whatever HOME a test
  sets — so a test window reopens on David's second screen. A test home uses its own `flicast/scratch*` keys; the
  real editor's spot is never touched by a test run.

- **The keystroke overlay draws less than was recorded, on purpose.** An unmodified single key is drawn only with
  `singleLetters` on (default ON for new projects; a loaded document keeps its value), so "Show keystrokes ON + 35
  keys + a blank frame" is the rule, not a broken renderer — `overlay.get` reports `recorded` and `shown`. With
  `singleLetters` on, a typing run is ONE press per word whose label grows letter by letter (the planner reads the
  label at *t*); Space ends the word and is absorbed, Enter / Tab / shortcuts end it and draw, and `shown` counts words
  (17 keys → 4 shown). The copied Screen Studio `pop prev; continue` rule is gone on purpose (typing-runs-2026-09-17k,
  David's ruling). A run's case comes from Shift, because `keyTitle` is the keycap and `characters` is never read; a
  lone Shift before Shift+letter draws `⇧` for ~50 ms. Labels join with a NO-BREAK space (forensic §8.2): build test
  expectations with `labelOf`, never by typing `'⌘ S'`.
- **The capability surface page is also a published artifact** (registered in the brains' artifact register):
  republish it with its registered `url`, or a new copy forks.

## Expert Mental Model

- **The verb is the product; the window is a view of it.** A newcomer looks for the button; the fluent
  reader asks what capability the button calls (`data-verb` on every control) and tries it with
  `--dry-run` from a second terminal. If the CLI cannot do it, the UI is hiding logic, and that is the
  bug.
- **Two timelines, one arithmetic.** Source time is what was recorded; output time is what the viewer
  sees after slices and speed changes. `slice.timeMap` converts both ways. Every "why did my zoom move"
  puzzle is this conversion; every record stores source time on purpose.
- **A destination is decided at arm, a document at commit, a history entry at gesture close.** Three
  different moments; knowing which one governs a behaviour (where a take lands, when autosave fires,
  when `history.jsonl` grows) is what separates reading the code from guessing at it.
- **Determinism is a property you assert, not a mood.** Generators are keyed by an inputs hash, the
  clock and randomness are ports, frame hashes are compared across two exports. When something looks
  flaky, the first question is which port leaked wall-clock or `Math.random` in.
- **Failures are words with a next step.** `words.ts` gives every capture error code a sentence and a
  `next` (try again / permissions / continue / none); refusals name the clashing record in words and
  carry its id in `details`. A bare code or `[object Object]` reaching a screen is a regression.
- **Absence and success must not look alike.** Every grep-shaped test carries a positive control; the
  uat run aborts if its deliberately-broken story passes; a golden that regenerates a missing fixture is
  a tautology and is refused. Read a green with that in mind.

## Scope Limits

- Does NOT press Record, grant permissions, pick files or answer confirmations from an agent; those
  are ★ human-only by design (`spec/security-privacy.md` S8). The agent arms and tells the person what to press.
- Does NOT record typed characters by default. Capture needs two person-only switches: Settings permits it
  (`keystrokeCaptureAllowed`) and the Record sheet's "Capture keystrokes" chooses it per recording
  (`recording-defaults.json`). `characters` is stripped from every event an agent can read.
- Does NOT pause a recording; RecordKit 0.87.2 has no pause. "Stop & start a new scene" is the
  substitute, and scenes concatenate in output time.
- Does NOT copy, move or delete a cast project yet (`unsupported`). Rename works (2026-09-22): the three places —
  document, `cast/<name>/`, lab folder — move together, and a rename that moves files starts a fresh undo stack. Copy /
  move / delete need the same three places handled. Packages can do all four.
- Does NOT cut talking-head video by transcript; that is FliCut. Does NOT plan or write scripts; that
  is Storyline. Does NOT run a daemon or a TUI; the CLI is the terminal surface and the app must be up.
- Does NOT ship: no packaging, signing or notarisation has been run; the RecordKit helper must be
  re-signed under the Developer ID at that point (R-NOTARISE).
- Writes a cast project's export, with no path given, to `<projectDir>/videos/<name>/<name>-final.<ext>` (roadmap
  §1.2f, done 2026-09-22 — fli-core v0.3.0 names it). A `.flicast` package still exports to `<projectsDir>/<name>.<ext>`.

## Failure Modes

- **The app "crashed" after a recording, vanished from the Dock and Cmd-Tab.** Not a crash: the HUD
  had turned the process into a macOS `UIElement`. Fixed by unsetting `setVisibleOnAllWorkspaces`
  before closing the HUD; if it recurs, `lsappinfo info -only ApplicationType` on the pid from
  `control.json` is the instrument.
- **"Preparing…" forever, every HUD button refused.** RecordKit's `prepare()` hung (Roamy: 2 of 11
  starts, always after `[InputRecorder] … failed to capture any rects before timeout`). Now bounded at
  15 s → `failed { prepareTimeout }` with the phase that stalled in `flicast logs` (`capture: phases`).
  Cause inside the helper still open; re-measure on the next RecordKit release (ADR-0001).
- **"display 1 is not available" / no displays listed while a fresh app sees one.** A stale helper.
  The adapter retries once and restarts the helper (only with displays present and the grant held, at
  most once a minute). Compare against a fresh app before blaming macOS.
- **Orphaned `recordkit-rpc` at ~20 % CPU.** A helper holding a recorder survives a SIGKILL of Electron
  (it reparents to launchd). The app stops its own on every exit path and reaps this install's stale
  ones at launch; a `pkill` of Electron, or the trial probe, still leaves one. `pgrep -fl recordkit-rpc`.
- **`Cannot find package 'zod'` or "Cannot find module '@appydave/core'" at import.** The foundation is
  not installed or not built; `npm install` in FliCast "succeeds" anyway. See README § Install.
- **`fjp.compare is not a function` in the app, tests green.** A CommonJS package imported as a
  namespace loses its named exports in the built main bundle only. Default-import CJS packages. The uat
  harness catches this class; a green unit suite alone does not.
- **`Unterminated string literal` in a file that typechecks.** A string ending in `import"` in the main
  bundle trips the chassis's esm-shim regex. `npm run build` is part of every gate for this reason.
- **Exported audio ~44 ms late.** AAC priming with no edit list; every onset (clicks, mic) sits 44 ms
  after its event. Known, measured, unfixed; the golden measures relative to the first onset.
- **`door off` in the footer.** Another process holds `FLICAST_PORT` (7131). Read the terminal; run
  with another port and point the CLI at it.
- **`flicast: the app refused the token`.** A stale `control.json` from a previous launch, or
  `FLICAST_TOKEN` pointing at another instance. Restart the app or fix the env.
- **A generated surface is stale.** `api/openrpc.json`, `api/capability-surface.html` and the skill's
  verb reference (`references/verbs.md` in the `flivideo:flicast` skill) are generated from a running build; after a verb change they disagree with the app until
  regenerated. `npm run api:check` and `node scripts/skill-verbs.mjs --check` say so without writing.
- **A green test that proves nothing.** The suite's own instruments have failed silently before (a
  golden regenerating its fixture, a grep with no positive control, a mutation sample where 14 of 50
  mutants survived). When a test "always passes", check that it can fail.
