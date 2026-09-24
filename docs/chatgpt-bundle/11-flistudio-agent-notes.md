<!-- FliVideo source bundle · flistudio AGENT-NOTES · generated from flistudio/docs/AGENT-NOTES.md -->


# FliStudio — Agent Notes

Only what the code cannot tell you. Everything here failed the derivation test on purpose.

## Tooling

- Build `shared` before anything that imports it: `npm run build -w shared` (a fresh checkout's `npm test` fails
  without it).
- E2E: always `npm run test:e2e`. It builds first; the drill runs `server/dist`, so `npx playwright test` alone tests
  the **previous** build and passes or fails on stale code.
- Server tests fail below 90% line coverage — new server code needs tests in the same commit.
- `npm run lint` includes dependency-cruiser; module boundaries (estate / identity / assets / launch / capabilities /
  cli) are enforced, not advisory.
- On this machine bare `grep -r` is shimmed to ugrep and obeys `.gitignore`; use `command grep` for searches that
  must be complete.

## Where the schemas are

- `docs/schema-mirror.md` (+ `.json`) is generated from the code with file:line anchors — read it, do not retype
  shapes. After changing `shared/src/contracts.ts` regenerate it (technique:
  `docs/agent-comprehension-docs.md`, step 1); `verify_mirror.py` exits 1 on drift.
  Shapes imported from `@flivideo/core` are listed there as gaps — fli-core's own `docs/schema-mirror.md` holds them.
- For the live contract ask the app: `bin/flistudio list`, or `GET /api/capabilities` (JSON Schema per capability).

## Non-default conventions

- **A new capability is declared, never routed.** Add it to `CAPABILITIES` in `shared/src/contracts.ts` and to
  `HANDLERS` in `server/src/capabilities/registry.ts`; HTTP, CLI and pickers follow. Then update the counted lists in
  `capabilities.test.ts` and `cli.test.ts` (both assert the exact set), the spec §6.3 table, and run
  `npm run api:openrpc` (`api/openrpc.json` is byte-compared by `api:check` and `door.test.ts`; prettier ignores it).
- **Decide the fence when you declare it.** `humanOnly: true`, or `{ when(input), note }` for the part only a person may
  do (fli-core `defineCapability`). `callCapability(ctx, name, input, principal)` enforces it for `agent:*` and `cli`;
  the screens call as `human:ui`, the CLI as `cli` (or `--as agent:<name>`, never human). A new refusal name needs a
  frozen code in `FAILURE_CODES` (`shared/src/contracts.ts`) — append, never renumber.
- HTTP tests that play the screens send `x-fli-principal: human:ui`; with no header a caller is `agent:anonymous`.
  The built server (e2e) requires the bearer token — the drill reads it from the fixture home's control file.
- Handlers **throw `Refusal(code, message)`** with a code from the shared failure vocabulary; `callCapability` turns it
  into `{ ok: false, error }`. Never return an error object from a handler.
- Every module takes `StudioConfig` instead of calling `os.homedir()`. Tests build it over a fixture estate
  (`server/src/test/fixture-estate.ts`); never point a test at the live estate, `~/.config/appydave` or `~/.fli`.
- `slugify` and `withoutOwnCode` exist twice (server `identity.ts`, client `format.ts`) for the create preview — change
  both together. A name starting with the project's own code (`d04 intro`) loses that copy, with a warning.
- The screens edit in place by **double-click** (folder code chip, project name). David rejected a separate edit field
  next to a read-only one (2026-09-22) — keep one element that becomes editable.

## Pitfalls

- **Never announce a write from inside a capability.** The server reflects the disk (R33, `estate/watch.ts` →
  `estate:changed`, and `useCall` refetches per brand). A new write path is live for free; a new screen gets it by
  reading through `useCall` with a `brand` input. Emitting from handlers would miss the CLI, which runs in-process.
- **`path.reveal` runs `open` through an injected `ctx.reveal`.** Tests pass a stub; without one, under vitest it
  throws rather than open Finder, and the e2e server gets a no-op from `FLISTUDIO_NO_REVEAL=1`. The location icons
  are `span role="button"` (they sit in clickable rows and the brand card) and the `>_` glyph is CSS, so it never
  joins a line's text — assert on `data-path`, not on text.
- **A launch raises the app's window through an injected `Revealer`** (`launch/reveal.ts`), passed only by the running
  server and the CLI. Tests pass none; the e2e server runs with `FLISTUDIO_NO_REVEAL=1`. Never call `realRevealer` from
  a test — it opens real windows on David's screen.
- **T7 in tests**: `StudioConfig.storageRoot` is `/Volumes/T7` only for the real home; under an overridden home it is
  `<home>/T7`. Migration tests create that folder as a mounted stand-in — never point a test at `/Volumes`.
- Watcher tests must wait until FSEvents is armed (`armed()` in `estate/watch.test.ts`): a change made right after
  `watchEstate` resolves can be missed under full-suite load.
- **Never hard-code `recordings/` or `transcripts/`.** New projects keep them under `hub/` (spec D14); ask
  `projectLayout()` / `projectLayoutPaths()` from `@flivideo/core` (≥ v0.5.0, self-healing: no recordings anywhere → hub; FliHub calls the same function). A stray
  `hub/` without `hub/recordings/` never hides a legacy project's `recordings/`; the layouts are never merged.
  FliStudio reads a legacy project under both transcript names (`transcripts/`, `recording-transcripts/`).
- `project.get` / any `project` argument by **code** refuses as `project-ambiguous` when an archived folder shares the
  code (fixture: `a01-xmen` vs `archived/a01-old-xmen`). Pass the folder name or the id.
- `fs.rename` onto an existing *empty* directory succeeds silently on macOS — `renameProject` checks with `lstat` first;
  keep that check in any new move.
- The allocator never backfills: `nextCode` is the one after the highest code live or archived. A free lower code is
  only reachable as an explicit `code`.

## Decisions worth knowing

- **R32 (David 2026-09-22): FliStudio owns the outer envelope.** It may rename the project folder and name, only through
  `project.rename`. The **code never changes** (a code change is a future, separate capability) and the id never
  changes. FliStudio must keep its own state (recents) right and tell the apps; v1 only reports which apps have work.
- **R4 / L4: read-only over every app.** Never write an app's store or any `fli.<app>…json`. A gap in what an app
  accepts is a ticket in that app's repo, not a workaround here (spec §10).
- **The lane rule replaced "writes only fli.studio.json"** (David 2026-09-23). A new write into a project is fine when it
  is FliStudio's own job and goes through a capability; a write into another app's area, a move or overwrite of a
  source, or a delete is not — the last only on David's word (human-only in the contract).

## Scope limits

- Deletes only inside a project's `-trash/` (`project.empty-trash { confirm: true }`, David 2026-09-23). Never touch
  `recording-shadows/` (retired; removal waits on David).
- Copies into a project only through `footage.import` (d04 D5: copy, never move, never over a file). Transcripts are
  FliTools' job (fli-core `transcribeQueued`), never FliStudio's; tests point `flitoolsControlFile` at a stub under the
  fixture home — the real FliTools is reached only with `FLISTUDIO_FLITOOLS_CONTROL`.
- Does NOT move or rename files inside a project — except `project.migrate-layout { apply: true }`, which
  moves `recordings/` + `recording-transcripts/` under `hub/` only on David's "move" (dry run by default).
- **Project intents** (`aspect`, `languages`, `shape`) live in `fli.studio.json`. Write only the fields that changed: FliCut
  treats a *stated* aspect as the new-edit aspect, and an unset one as "follow the footage". `shape` is a hint with no behaviour.
- Does NOT push context into running apps beyond each app's door 3; Teletubby's script-set choice is UI-only by design.

---
Deep comprehension narrative for humans: [SYSTEM.md](./SYSTEM.md) — not loaded into agent context.
