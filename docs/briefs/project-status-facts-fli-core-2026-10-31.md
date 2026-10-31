# Brief: project status facts — fli-core helper + FliHub / FliCut / FliEdit wiring — 2026-10-31

**Status:** follow-up to `project-status-build-2026-10-31.md` (ruling 6). Not started. Owner: flivideo-orch to schedule.
**Why now is fine to wait:** FliStudio v1 scans the folders and already reproduces the dry run for all 17 v-appydave
projects. Facts make the status faster and more exact (and let an app say what a folder scan cannot, like "editing
finished"); nothing is broken without them.

## What exists (FliStudio, branch `project-status`)

- `fli.status.json` at the project root: `{ schema: 1, entries: StatusEntry[] }`, append-only.
  `StatusEntry = { step, state, by, at, why, note?, tags?, brollSource?, fact? }` —
  schema `StatusEntry` / `StatusFile` in `flistudio/shared/src/contracts.ts`.
- Read/append helper: `flistudio/server/src/capabilities/status-log.ts` (`readStatusLog`, `appendStatus`,
  `latestSetting`, `latestFact`, `tagsOf`), marked `TODO(fli-core)`.
- The derivation already reads facts: an entry with `fact: true` and `state` `done` | `part` counts as evidence for its
  step beside the disk (the newer wins; `why` becomes the box's evidence line). Test:
  `project-status.test.ts` › "a fact an app wrote counts as evidence".
- Step keys (the list is data, `STEPS` in `project-status.ts`): `idea script record edit export final launch publish`.

## 1. fli-core (one minor release)

Move, do not redesign:

1. `StatusEntry`, `StatusFile`, `STATUS_FILE = 'fli.status.json'` into fli-core `contracts` (browser-safe, like `Stamp`).
2. `recordFact(projectDir, { step, state: 'done' | 'part', by: 'app:<name>', why })` — appends one entry with
   `fact: true` and `at` = now, under fli-core's `takeLock` (`fli.status.json.lock`, same wait/stale values as words /
   series) + `atomicWrite`. Never rewrites or drops a line. An unusable file is left alone and the call throws.
3. `readStatus(projectDir)` → entries (absent → `[]`).
4. Tests on temp dirs; the schema mirror regenerated.

Then FliStudio drops its local copy and imports from fli-core (`status-log.ts` keeps `latestSetting` etc. or they move
too — orch's call; recommendation: move all five, they are pure).

**Rule for apps:** an app only ever writes `fact: true` entries. Settings, holds, notes and tags are a person's (through
FliStudio's `project.status.set` / `project.hold` / `project.note` / `project.tags.set`). `by` is `app:<name>`.

## 2. Wiring (one small change per app, each in its own repo — not FliStudio's lane)

| App | When | Fact |
|---|---|---|
| FliHub | after a take is saved / renamed into `hub/recordings` | `{ step: 'record', state: 'part', why: '<n> takes · chapters <list>' }`; `state: 'done'` when the person marks recording finished (if FliHub has such an action; otherwise only `part`) |
| FliCut | after an export finishes (`last-export.json` written) | `{ step: 'export', state: 'done', why: '<file> exported' }`; on "edit finished" (if added) `{ step: 'edit', state: 'done' }` |
| FliEdit | after its `-final` export | `{ step: 'export', state: 'done', why: '<file> (FliEdit)' }` |
| Overlay / B-roll Pilot | optional, later | their own steps once per-brand recipes exist (out of scope now) |

Each app: one call to `recordFact` at the moment the work lands, failure logged and ignored (a fact is a hint; the scan
still runs). No app reads `fli.status.json`.

## Done when

- fli-core tag published with `recordFact` / `readStatus` + tests; FliStudio pinned to it, local helper removed, its
  `project-status.test.ts` still green.
- Each wired app has a test that a finished action appends exactly one fact with `by: app:<name>`.
- `npx tsx scripts/status-dry-run-compare.ts` in FliStudio still passes (facts must never change a box the disk already
  proves).

## Out of scope

Per-brand recipes / layer boxes, YouTube sync, a stall-threshold setting, the heat map, archive as a status.
