<!-- FliVideo source bundle · flistudio SYSTEM · generated from flistudio/docs/SYSTEM.md -->


# FliStudio — System Context

## Purpose

FliStudio gives David (and next Jan and Mary) one place to pick a brand, pick or create a video project, see everything
in it, and open FliHub, FliCut, FliCast or Teletubby already pointed at it — so no app needs its own brand and project
picker, and an agent can do the same through a CLI.

## Core Abstractions

- **Brand root** — one folder per brand (`~/dev/video-projects/v-appydave`, …), found through `~/.config/appydave/brands.json`
  with the home prefix rewritten to this machine's user (spec A5). Everything FliStudio knows about a brand is read from
  that folder on every request; there is no cached copy. Each brand root is its own git repo (D6).
- **Project = a top-level folder that holds `fli.studio.json`** (A3). Membership is the file's existence, nothing else.
  The file carries `{ schema, id, brand, code, name, createdAt }` plus the optional **intents** `aspect`, `languages`
  (dominant first) and the `shape` hint (David 2026-09-23; shapes in fli-core, see `docs/schema-mirror.md`). The **code** (`d01`) is the brand-unique key; the
  **id** (uuid) is the identity that survives renames; the **name** and the folder slug are the changeable envelope
  (R32). Folders without the file are *other folders* — shown, never treated as projects, adoptable with one click.
- **The capability registry** — every action (list them with `bin/flistudio list`; the set is pinned in
  `capabilities.test.ts`) declared once in
  `shared/src/contracts.ts` (name, zod input/output, side effects, failure codes) and bound to handlers in
  `server/src/capabilities/registry.ts`. The HTTP door (`POST /api/call`), the CLI (`bin/flistudio`) and the screens all
  go through `callCapability`, so they cannot disagree. `GET /api/capabilities` publishes JSON Schemas for agents.
  Since fli-core v0.7.0 every call also names its **principal** (`human:ui`, `cli`, `agent:<name>`), and the ★ fence
  inside `callCapability` refuses human-only calls (emptying the trash, applying a layout move, stopping FliHub) for
  agents and the CLI. `POST /api/call` and JSON-RPC `POST /api/rpc` need the bearer token the server publishes in its
  control file; `/api/docs` and `/api/console` render the generated OpenRPC (`api/openrpc.json`).
- **Zones and layouts** — a project is read as zones: FliHub's recordings and transcripts (under `hub/` in the hub
  layout, at the top in the legacy one — fli-core's `projectLayout()` decides, self-healing: no recordings anywhere →
  hub), `videos/<name>/`, `cast/`, footage-like folders no zone claims, the apps' `fli.<app>…json` files and `-trash/`
  (its own zone since fli-core v0.6.0). Every collection comes back `scanned` or `unscanned` (with why) — never an empty
  list standing in for "could not read" (R12). The screen shows a problem only when there is one; scan times are not
  shown (David 2026-09-22).
- **Doors** — how FliStudio reaches another app: door 2 starts a stopped app with `scripts/app.sh start --brand
  --project` (paths from `~/.config/appydave/apps.json`); door 3 switches a running app through its own API. Each
  launch reports what reached the app and what could not (A7, open contract §3.1), then raises the app's window
  (`launch/reveal.ts`). `apps.status` reads each app's own context, so "Open on this project" comes from the app.
  FliCut has a third door: `edit.start` hands it an edit name and files in order (`POST /api/video/open`, FC-37).

These compose as: brand root → listing (members, other folders, archive) → one project → its zones → a door to an app.
`@flivideo/core` (pinned tag) owns the shapes and rules underneath — folder naming, the identity file, classification.

## Key Workflows

### Start a new video
1. On the Projects screen (a table of the brand's projects — one click opens one), press **+ New project** and type a
   name in its panel. The folder chip shows the next free code (`d04-the-quick-brown-fox`); double-click
   it to choose a different free code such as `d01`.
2. Create project → FliStudio makes `<code>-<slug>/` and writes `fli.studio.json`, nothing else, and lands on the
   project home.
3. Later, double-click the project name on the home screen to rename it: the folder becomes `<code>-<new-slug>`, the
   name is rewritten, the code and id stay.

### Bring an existing folder in
1. A folder like `d03-cutty-presenter-tracking` sits under *Other folders — not projects yet*, labelled from what is in
   it ("looks like a video project — 8 recordings").
2. Adopt as project → `fli.studio.json` is written with the folder's own code and a humanised name. Nothing else in the
   folder changes; legacy layouts (`first-edit/`, `recording-transcripts/`) are listed as legacy and left alone.

### Look at a project and open the right app
1. Project home: a left menu in three groups — **In this project** (Footage and other folders, Recordings in FliHub's
   layout, Videos, Cast, All files), **Do** (Start an edit, Settings) and **Apps** — and an always-visible Trash line.
   Each section says where its files live in one quiet line ("in hub/recordings/ · transcripts in hub/transcripts/").
2. A row opens the viewer: the clip plays in its own shape through `/api/media` (Range), with the transcript under it —
   a yellow word pill timed from whisper `.json` (else `.srt`), click a word to seek, speeds to 4x, settings remembered.
3. Launch FliHub / FliCut / FliCast / Teletubby: a stopped app is started with the project as launch arguments, a
   running one is switched through its API, then its window comes to the front. Each button shows the app's own state
   ("Open on this project" only when the app says so) and a toast says what happened.

### Start an edit in FliCut
1. Start an edit: name it (→ `videos/<name>/<name>-cut.mp4`), tick sources — Recordings by default, Footage and Cast
   (a FliCast take's `-final` export, raw scenes one tick away) — and order one combined list.
2. Open in FliCut → `edit.start` hands FliCut the name and absolute paths in order; FliCut writes its own edit. An
   existing name is never overwritten ("Open it as it is"). The line beside the button follows FliCut (`edit.status`):
   opening → transcribing N/M → ready.

### Set a project's intents, tidy it
1. Settings (or the create row): aspect, languages, shape hint. Only changed fields are written. Changing the aspect of
   a project that already holds material lists what is there and asks first; nothing is re-rendered.
2. Empty trash deletes what is inside `-trash/`, after an inline confirm.
3. An old (legacy) project moves to the hub layout with `project.migrate-layout` — a dry run first, `apply` on David's
   "move" (four projects moved 2026-09-23).

### An agent does the same
1. `bin/flistudio list` → the capabilities; `bin/flistudio <name> --json …` runs one (`--files a,b,c` for lists).
2. In a terminal every missing argument becomes a picker; with `--json` a missing argument is an error naming it.
3. `export.place` lets an agent (or Mary's skill) put a finished file into `videos/<name>/` under the name the
   library gives it — never overwriting, never moving the source.

## Design Decisions

- **Identity lives in a file inside the project folder, not a registry** (A3). The file travels with the folder on
  rename, move and across machines through the brand's git repo.
  - *Alternative considered*: a per-brand registry (e.g. extending `projects.json`).
  - *Why rejected*: it must be updated on every rename and move, and a central registry would not reach Jan's or Mary's
    Mac.
- **One capability set, several projections** (spec §6.3). The screen, HTTP and CLI call the same registry.
  - *Alternative considered*: separate REST routes for the UI and a CLI with its own logic.
  - *Why rejected*: two implementations drift; tests pin the registry once (`capabilities.test.ts`, `cli.test.ts`).
- **Read-only over every app's files** (R4, L4). FliStudio writes only `fli.studio.json`, placed exports and the
  project folder name (`project.rename`, R32). Apps create and edit their own files.
  - *Alternative considered*: FliStudio as the editor of project state for all apps.
  - *Why rejected*: each app owns its decisions; a hub that writes their stores becomes the thing that corrupts them.
- **Codes are allocated from disk, never backfilled** (A6, R15). The next code is the one after the highest used live
  or archived; a gap such as a free `d01` is reachable only by typing it.
  - *Alternative considered*: FliHub's high-water-mark file, or filling the lowest gap.
  - *Why rejected*: the high-water mark is gitignored and machine-local; backfilling risks reusing a code an archived
    or other-machine project still holds.
- **Web app on AppyStack, not Electron** (A1). Same stack as FliHub and Captain's Log, and the HTTP door the screen uses
  is also the one agents call.
  - *Alternative considered*: an Electron desktop app like FliCut.
  - *Why rejected*: a hub that reads and launches needs no native shell; packaging is later roadmap work (CR-42).
- **Self-healing layout (option A, David 2026-09-23)**: a project with no recordings anywhere is hub, decided once in
  fli-core so FliHub and FliStudio cannot disagree. A top-level `recording-transcripts/` or `transcripts/` counts as
  legacy evidence because media is not in git — another machine may hold only the transcripts.
  - *Alternatives considered*: FliHub creates `hub/` on open; a per-machine setting.
  - *Why rejected*: both put the rule in one app or one machine instead of the shared library.
- **FliCut is handed files, not folders** (FC-37). FliStudio chooses sources and order; FliCut never learns FliHub's
  layout. *Rejected*: FliCut reading `recordings/` itself — it broke the day recordings moved under `hub/`.
- **Migration moves whole folders and never merges.** `recordings/` and `recording-transcripts/` move as units into an
  absent `hub/…`; any overlap, an open FliHub, or a T7 held/published copy blocks it, and a failed step is undone.
  *Rejected*: merging into an existing `hub/` — two copies of a take with no rule for which wins.
- **The library is a pinned public dependency** (A9): `@flivideo/core` from `github:flivideo/fli-core#vX.Y.Z`, never a
  `file:` path or copied source, so every Fli app reads the same rules at a known version.

## Non-obvious Constraints
- **The fence is a contract, not a lock.** The token keeps other machines and web pages out; a local process that
  reads the control file and claims `human:ui` is not stopped. The fence guides cooperating agents — the same stance as
  FliCast's. The CLI can never call as a human, so David empties trash and applies moves from the screens.

- **The screen follows the disk, not the server's own writes** (R33). `server/src/estate/watch.ts` watches every brand
  root (`fs.watch`, recursive) and emits `estate:changed { brand, folders }`, debounced; the page refetches any call for
  that brand. So a change by the CLI, an agent, Finder or FliHub shows up without a refresh, and a project home open on
  a folder that gets renamed follows the project by id. A brand root that cannot be watched is logged and skipped.
- **The CLI does not go through the running server.** `bin/flistudio` runs the capability registry in its own process
  against the disk. That is fine because the server watches the disk (R33) — nothing needs to announce a write.
- **A code can be ambiguous.** `project.get` accepts a folder name, an id or a whole code; a code also used by an archived
  folder (the fixture's `a01-xmen` vs `archived/a01-old-xmen`) refuses as `project-ambiguous`. Refer by folder or id then.
- **Archived projects are listed, never opened** (R13), and `archived/` range folders (`a01-a49`) count as codes in use.
- **`fli.studio.json` must be valid to count.** An unreadable one makes the folder an *other folder*, and adopt refuses
  rather than overwrite it.
- **A stated aspect and an unset one behave differently.** FliCut starts new edits at the project's aspect only when
  `fli.studio.json` states one; unset means "follow the footage". So Settings writes only the fields changed, and an
  unset aspect is shown unset — never as 16:9.
- **Migration is per machine.** Media is gitignored (`*.mov`, `*.mp4` in each brand repo); the transcripts move shows in
  git as deletes plus new `hub/transcripts/`. Another machine that holds the media runs the migration itself.
- **A T7 copy pins a project's layout.** FliHub's hold/publish restores to the same relative paths, so a project with a
  `youtube-HOLDING` or `youtube-PUBLISHED` copy is not migrated; with the T7 unmounted the check cannot run and it
  refuses too. Tests use `<home>/T7`, never the real drive.
- **The display name and the folder slug can differ.** Renaming a folder by hand keeps identity (§11 #1) but leaves
  `name` stale; `project.rename` is the way to change both.

## Expert Mental Model

- **The disk is the database, and the server is its reflection.** There is no FliStudio model of the estate to keep in
  sync — every call re-reads the brand root, and the watcher tells open pages when to re-read. Questions like "does FliStudio know about X" become "is X on disk in the right shape".
- **Identity is the id, the key is the code, the rest is envelope.** Newcomers treat the folder name as the project; an
  expert refers to projects by id in automation and by code in conversation, and expects folder names to change.
- **Honest absence over tidy emptiness.** Every collection says `scanned` or `unscanned`; every launch says what was not
  passed. When something looks empty, the expert checks the scan stamp before believing it.
- **FliStudio points, the apps act.** It never fixes another app's state; a gap in what an app accepts becomes a ticket in
  that app's repo (spec §10), not a workaround here.

## Scope Limits

- Does NOT edit, trim, caption or render — FliHub (recordings), FliCut (edits), FliCast (captures); Teletubby only shows
  and edits a script in a prompter (writing scripts is a future app, Scribe).
- Does NOT move files inside a project except `project.migrate-layout` on David's "move"; other legacy folders
  (`first-edit/`, `recording-shadows/`) are listed and left alone (A8). Deletes only inside `-trash/`.
- Does NOT sync between machines or manage archive/publish; each brand root's git repo carries identity files.
- Does NOT change a project's code yet (R32 — a later, separate capability).
- Does NOT push a rename into apps that are already running; FliHub and FliCut are re-pointed on the next launch from
  FliStudio, and Teletubby's script set keeps the folder name it was given.

## Failure Modes

- **A brand that is not live** — its root was missing or unreadable when the server started, so `fs.watch` could not
  arm; the server logs "Brand root is not being watched" and that brand needs a refresh after outside changes.
  Restart the server once the root exists.
- **`unscanned` brand or zone** — the brand root is missing or unreadable (`no-brand-root`, `unscanned`); the UI shows
  "not scanned", never an empty list. Check the path `brands.json` gives after the home rewrite.
- **Door 2 silently not starting** — the app's checkout is not in `apps.json` or its `scripts/app.sh` fails; the toast
  says the app was not confirmed after the confirm timeout, and the app's own log is under `~/.fli/studio/logs/`.
- **`confirm-required`** — an aspect change on a project with material, or Empty trash, sent without `confirm: true`;
  the error's `details` list what is there.
- **`held-elsewhere` / `app-busy` / `would-overwrite` on migrate** — a T7 copy (or no T7), FliHub open on the project, or
  a `hub/recordings|transcripts` already present. The dry run lists these as blockers first.
- **`edit-exists` on Open in FliCut** — an edit of that name exists; FliCut never overwrites. Open it as it is or rename.
- **`code-taken` on create** — the typed or allocated code is used by a live, other or archived folder (including a
  range folder). Pick another; the chip shows the next free one.
- **`folder-exists` on rename** — a folder with the target `<code>-<slug>` already exists (even empty). Nothing was moved.
- **E2E green on old code** — the Playwright drill runs the built server (`server/dist`); `npx playwright test` without
  a build tests the previous build. Use `npm run test:e2e`, which builds first.
