# Brief: B-roll Pilot v1 — BUILD — 2026-10-31

**Builder:** a fresh session launched by flivideo-orch. **Reports to:** flivideo-orch (SendMessage `flivideo-orch`).
Never park waiting on David; route every question to orch with a recommendation.
**Worktree (build here, nowhere else):** `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/broll-pilot`, branch
`broll-pilot` (the spec and mocks are already committed on it, off FliStudio main `ce8fd25`). Check `pwd` and the
branch first, and stop if either differs.
**Approved:** David approved the mocks on 2026-10-31 ("I love it"; the three views are one tool). The spec is the
contract.

## Goal

Build **B-roll Pilot**, FliStudio extension #3. It is a catalogue of the visual material a video *might* use
(screenshots, screencasts, artefacts, animations, thumbnails of earlier videos). Each item is described on arrival so
that a later AI can choose footage. It has a registration contract (`broll.register`) that FliHub and FliCast will call
later. It is a Pilot: one problem, with a JSON-RPC door that an agent drives.

## Read first (in this order)

1. **The spec, which is the contract; every rule is in it:**
   `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/broll-pilot/docs/planning/broll-pilot/spec.md`
   The key sections:
   - §4 data: an asset is a `broll` **resource**, with no second store.
   - **§4.6 storage:** one `resources/` zone; files are registered in place or copied there with `place: 'copy'`.
   - §5 describe, especially **§5.3 description as a service**.
   - **§6 the registration contract.**
   - §7 verbs, §8 module layout, §10 the screen, §12 acceptance criteria.
2. **The approved mocks:** https://claude.ai/artifact/41bRuUXxKwpL4VadM1ATbp (source:
   `docs/planning/broll-pilot/mocks.html` in the worktree). They show one screen with three views: the grid, a card
   opened, and the drop-in with the describe queue. They were updated after approval for the two rulings below
   (`resources/` zone, describe service). If the mocks and the spec ever differ, **the spec wins**.
3. **The worktree's `CLAUDE.md` and `docs/AGENT-NOTES.md`.** §Modules covers how an extension is added, the
   counted-list and OpenRPC steps, and the fence.
4. **Prior art to copy, not reinvent:**
   - `modules/storypilot/`: state over resources, and conformance.
   - `modules/overlay-pilot/`: FliTools calls through the host, `-renders/<tool>/`, and the `BrollClip` field names
     `shows` / `goodFor`.
5. `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/transcription-as-a-service.md`, the pattern §5.3 mirrors.

## Rulings already made (do not re-open)

**Storage (David, relayed by orch):**
- `<project>/resources/<video|project>/` is the one resources zone.
- Files in a stable home are **registered in place**: FliCast projects, `footage/`, another project's published
  thumbnail.
- Files from an inbox, a cache or a download folder are **copied** into the zone with `place: 'copy'`: FliHub's incoming
  take, screenshots, Motion renders, anything in `-renders/`. Copy rules: APFS clone, else a plain copy; a taken name
  gets `-2`, `-3`; never write over a file.
- FliStudio never moves a source. A path in `-renders/` or `-trash/` is refused for registering in place.
- `hub/broll/` and a `broll/` folder are both withdrawn.

**Describe (orch, delegated by David):**
- Visual description is a **FliTools service** on a named worker: the M2 first, Roamy as the fallback. It **never** runs
  on the machine that runs FliStudio.
- **One job at a time.** The worker runs a single serial queue, exactly like transcription-as-a-service: never two
  jobs in parallel, and B-roll Pilot never fans out.
- Each job is one frame, described by Qwen3-VL-8B through `qwen-video`. A job's identity is the frame's sha256.
- B-roll Pilot **only enqueues frames and reads the results back**.
- The Claude Code queue (`broll.describe.queue` + `broll.describe.set`) stays as the second describer. It is also the
  fallback when the service is missing or down.

**The FliTools describe service itself is NOT this build:**
- Build B-roll Pilot's client side behind one adapter, and test it against a FliTools stub.
- Write the FliTools ticket as a short brief in `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/` and tell orch. It
  should name: verbs such as `describe.submit` / `describe.job` / `queue.status`, the serial queue, and the worker
  setting in `~/.config/appydave/flitools.json`.
- Do not edit FliTools.

**The data:**
- Assets are FliStudio resources of one kind, `broll`. Its global registry row is added with `resources.kinds.add`;
  until that row exists, the kind still stores and shows under `other`.
- Ten `broll.*` verbs, none of them human-only. Every write is stamped with who and when. No new failure codes.

## In scope

- The module `modules/broll-pilot/`, laid out as spec §8.
- Its ten verbs (§7) and the registration contract (§6).
- The resources-zone drop-in (§7.2).
- The describe routes (§5): transcript via FliTools, frames sent through the describe-service client, the Claude Code
  queue, and a person typing a description.
- The screen (§10), matching the mocks.
- The usual steps for a new extension:
  - the host wiring lines;
  - the counted capability lists;
  - the §6.3 table in FliStudio's own spec;
  - `npm run api:openrpc`.
- Tests that keep the server above the 90% line, and conformance.
- A skill, `flivideo:broll-pilot`, at `/Users/davidcruwys/dev/ad/appydave-plugins/flivideo/skills/broll-pilot/SKILL.md`.
  It drives register → describe.queue → describe.set over JSON-RPC.

## Out of scope

- **The FliHub and FliCast B-roll buttons.** They come LAST, as a separate step in their own repos, after v1 is merged.
  Do not edit FliHub or FliCast. David confirmed the order: spec → contract → v1 build → buttons.
- **The FliTools describe service.** Write the ticket (above). No `mlx`, `qwen` or other model call inside FliStudio.
- **Timeline placement of any kind** (where, how long, Ken Burns, corner vs full screen). That is Timeline Pilot, later.
- Motion Pilot and video groups.
- Brand / global B-roll: `scope: 'brand'` is refused in v1.
- Folding `footage/` into `resources/`.
- The fli-core `ProjectZone` ticket for `resources` / `footage`: write it as a note to orch, and don't edit fli-core.
- Browser upload.

## Definition of Done

**Every row of the acceptance table below passes.**

**All gates pass in the worktree:**
- `npm test`
- `npm run lint` (including dependency-cruiser)
- `npm run typecheck`
- `npm run test:e2e` (it builds first; never run bare `npx playwright test`)
- `npm run api:check`

**The e2e drill (spec §11) passes on a fixture copy of D13.** It registers four items:
- one FliHub-style take with `place: 'copy'`;
- one FliCast-style cast in place;
- one screenshot dropped into `resources/project/`;
- one cross-project thumbnail via `broll.link`.

Each item gets described. Every source file is byte-identical afterwards. `broll.list` returns a non-empty `shows` /
`goodFor` for each item.

**Then** commit and push `broll-pilot`, and message orch. David's own acceptance on his running FliStudio happens after
orch merges, and is not yours.

## Acceptance criteria (spec §12, verbatim)

| # | Criterion | How to check |
|---|---|---|
| 1 | The module binds as extension #3 with key `broll-pilot`, namespace `broll`, stage `record`, 10 verbs | `bin/flistudio list \| grep '^broll\.'` = 10 lines; `extensions.test.ts` passes |
| 2 | `broll.register` in place stores an absolute path and never touches the file | test: sha256 + mtime of the fixture file equal before/after; no new file under the project except `fli.resources.json` |
| 2a | `place: 'copy'` puts a copy in `resources/<video\|project>/`, never over a file, and leaves the source untouched | test: copy exists with the same sha256; source sha256 + mtime unchanged; a taken name gives `-2`; a second call with the same source returns `created: false` and no second copy |
| 2b | A path in `-renders/` or `-trash/` is refused in place | test: `invalid-input` |
| 3 | `broll.register` is idempotent (in place by path; copy by source sha256) | test: second call → `created: false`, one resource, tags merged, no second copy |
| 4 | A person's description is never overwritten by an automatic one | test: `describe.set method:human` then `method:agent` → refused `would-overwrite` |
| 5 | A voice screencast is described from its transcript with no agent | test with FliTools stub: register → `describe.state: described`, `method: transcript` |
| 6 | A silent screencast gets ≥3 fixed-interval frames in `-renders/broll-pilot/<id>/` and they go to the describe service | test with a FliTools describe stub: one job per frame (sha256 identity), results merged into `shows`/`goodFor`, `describe.method: frames`, `model` recorded, tags `ai-`-prefixed |
| 6a | Describe service down or missing → the asset waits for Claude Code, with the reason | test: stub returns `app-unavailable` → `broll.describe.queue` lists it, route `agent`, reason shown; nothing fails |
| 6b | Nothing describes on the FliStudio machine | dependency-cruiser / grep: no `mlx`, `qwen` or model call in `modules/broll-pilot/`; the only vision path is the FliTools client |
| 7 | A cross-project thumbnail is a pointer | test: `broll.link` → `scope: cross-project`, `ref.id` = source resource, source project's files unchanged |
| 8 | `scope: 'brand'` is refused in v1 | test: `invalid-input` |
| 9 | A missing file shows as `missing`, not an error | test: delete the fixture file → `broll.list` still returns the asset with `missing: true` |
| 10 | FliHub's call works over the door as `agent:flihub` with the bearer token | e2e: POST `/api/rpc broll.register` against the built server with the fixture control file |
| 11 | A file put in `<project>/resources/<video\|project>/` with no record is registered once; a file added by `resources.add` is not | watcher test (wait for `armed()`): one `broll` resource, `from.app: 'drop'`; a `resources.add` thumbnail stays a `thumbnail` |
| 12 | Module fence holds | `npm run lint` (dependency-cruiser rules for `modules/<name>/`) passes; `fence.test.ts`-style check |
| 13 | Conformance: the screen mounts and calls only queries | module `npm test` runs `conformance(descriptor, server, client)` |
| 14 | OpenRPC regenerated | `npm run api:check` exits 0 |
| 15 | Every file shown has Finder + copy-path; every still has Copy image | e2e asserts `data-path` on each card's file and a `CopyImage` on stills |
| 16 | Light only | `command grep -rc prefers-color-scheme modules/broll-pilot/client` = 0 per file, and the same search for `color-scheme: light` finds the pin (positive control) |
| 17 | Agent skill exists | `flivideo:broll-pilot` SKILL.md in appydave-plugins drives register → queue → describe.set over JSON-RPC |

## Rules for this run

**Fixture estates only:**
- Tests run in temp dirs (`server/src/test/fixture-estate.ts`). Never the live estate, `~/.config/appydave` or `~/.fli`.
- **Never use live ports.** Never start, stop or restart David's apps (FliStudio 7150/7151, FliHub, FliTools).
- Never call `realRevealer`. The e2e uses `FLISTUDIO_NO_REVEAL=1`.

**Setup:** the worktree has no `node_modules`. Run `npm ci`, then `npm run build` for extension-core and shared, before
any tests.

**Git:**
- **Do not merge to main.**
- Commit by explicit path. Other sessions share the repo, so never `git add -A` a directory.
- Push the branch with `env -u SSH_AUTH_SOCK git push`.
- No `git pull --rebase` while others are committing.

**UI (AppyDave):**
- Light only.
- Reuse `PathActions`, `CopyImage` and `CopyButton`.
- Edit in place by double-click.
- Show who and when in an ⓘ, never as a timestamp.

**On this machine, bare recursive `grep` is ugrep and obeys `.gitignore`.** Use `command grep`.

**Remote help (optional):**
- Roamy (`100.89.32.35`, user `davidcruwys`) is caffeinated and available all day to spread development load, through
  `appynet:remote-claude`.
- There you own your git pull/push and the environment. Work in a worktree only, and never use live ports.
- The M4 is short on memory, so put heavy runs on Roamy: the full e2e, and any frame-sampling experiment.

**Questions** go to flivideo-orch with a recommendation. Never wait on David.

## Report to orch when done

- The branch and commit.
- The gate results, with the counts pasted.
- The AC table, with the evidence for each row.
- The path to the FliTools describe-service ticket.
- The fli-core zone note.
- Anything in the spec you had to deviate from, and why.
