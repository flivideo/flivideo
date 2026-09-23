<!-- FliVideo source bundle · agent-drivable reference (FliCast) · generated from flicast/docs/agent-drivable-reference.md -->

# Agent-drivable: the FliCast reference checklist

**Status**: reference, 2026-09-23, true at the commit that added this file. For the other Fli apps (FliStudio,
FliHub, FliCut, Teletubby) to measure themselves against. Checklist, not narrative — how FliCast works inside is
[`SYSTEM.md`](./SYSTEM.md); every shape named here is in [`schema-mirror.md`](./schema-mirror.md).

Each item: **what** · why it matters · **where in FliCast** · **check in another app**.

## 1 · The core

- [ ] **One capability core — every edit is a named verb.** Zod in/out, a kind (query · command · task · event), a
  side-effect class, failure modes, allowed principals. *Why:* a verb that exists only as a button is unreachable
  by an agent, whatever the CLI claims. *Where:* `src/core/capability.ts` (`defineCapability`), `src/core/ops/*.ts`,
  the set pinned in `test/capabilities.pinned.test.ts`. *Check:* is there ONE `call(principal, name, input)` seam
  that the UI also goes through, and a test that fails when a verb is added unannounced?
- [ ] **The UI is a client of the core, never an editor.** *Why:* otherwise the UI can do things no agent can.
  *Where:* renderer applies the core's JSON patches; `test/renderer-boundary.test.ts`, `test/core-boundary.test.ts`.
  *Check:* grep the UI for document writes that bypass the verb seam.
- [ ] **Dry-run, undo, idempotency on every command.** `dryRun` returns the patch + inverse; `idempotencyKey`
  replays instead of editing twice; history is per principal (`history.undoBy`). *Why:* an agent can look before it
  leaps, retry safely, and take back only its own edits. *Where:* `src/core/core.ts`, `src/core/ops/history.ts`.
  *Check:* can an agent preview a change, retry a call without doubling it, and undo only its own edits?
- [ ] **Long work is a Task.** `export.start`, `audio.improve`, `overlay.captions.generate` return a `taskId`;
  progress streams as events; `task.status` / `task.cancel`. *Where:* `src/core/ops/task.ts`. *Check:* does a slow
  verb block the caller, or hand back a handle?

## 2 · The doors (same core, several projections)

- [ ] **HTTP control door on loopback.** `127.0.0.1:7131` (`FLICAST_PORT`, `0` = ephemeral): `POST /v1/call`,
  JSON-RPC 2.0 `POST /v1/rpc`, `GET /v1/capabilities`, `GET /v1/events` (ND-JSON), `GET /v1/health`.
  *Where:* `src/main/control/http-door.ts`, ADR-0006. *Check:* `curl 127.0.0.1:<port>/v1/health`, then
  `/v1/capabilities` with the token.
- [ ] **Auth by a per-launch bearer token in a control file.** `FLICAST_HOME/control.json` holds port, token, pid;
  the caller names itself in `X-FliCast-Principal`. *Where:* `src/main/control/http-door.ts`, `src/main/paths.ts`.
  *Check:* does the door refuse without the token, and can a client discover port + token without asking a person?
- [ ] **A CLI that is only a client of the door.** Help generated from `capabilities.list`; `--json`, `--dry-run`,
  `--idempotency-key`, `--as agent:<name>` on every verb. *Where:* `bin/flicast.mjs`. *Check:* is `--help`
  generated from the running app, or hand-written (and therefore stale)?
- [ ] **An MCP server — two tools that reach everything, not one tool per verb.** `flicast_describe` +
  `flicast_call`, plus six curated tools for the usual loop; forwards to `/v1/rpc` as `agent:mcp`. *Where:*
  `bin/flicast-mcp.mjs`, `.mcp.json`. *Check:* `node bin/<app>-mcp.mjs --self-test`; count its tools.
- [ ] **A Claude skill that speaks the CLI.** *Where:* the `flivideo:flicast` skill in appydave-plugins; its verb
  list is generated (`npm run skill:verbs`). *Check:* is the skill's verb list generated or hand-copied?

## 3 · Swagger-like: the self-describing surface

- [ ] **A machine-readable spec.** `api/openrpc.json` (OpenRPC 1.3.2; `x-` extensions carry principals, the ★
  fence, failure modes), served at `GET /v1/openrpc.json`. *Where:* `scripts/gen-openrpc.mjs`, ADR-0005.
  *Check:* is there one generated spec, with a `--check` that fails when it is stale (`npm run api:check`)?
- [ ] **A human reference page served by the app itself.** `GET /v1/docs` (unauthenticated, read-only) = the
  generated `api/capability-surface.html`; Help → API reference opens it. *Where:* `scripts/gen-api-page.mjs`,
  `src/main/control/api-assets.ts`. *Check:* does the running app serve its own docs?
- [ ] **Pick a verb, fill the fields, fire, see the result — inside the app.** The capability console: a window
  loading the same page with a narrow preload, every verb callable as `agent:console`, the ★ verbs attempted and
  refused in front of the reader. *Where:* ADR-0008, `src/main/api-console.ts`, `src/preload/console.ts`,
  `src/main/ipc/console-call.ts`. *Check:* can a person fire any verb as an agent without writing code, and see the
  refusals the fence makes?
- [ ] **The suite's control plane — the same page in every app.** "agent door open" opens `@flivideo/core`'s
  `renderApiPage(openrpc, { console })` (v0.7.0), generated to `api/control-plane.html` and fired through
  `window.fliConsole` as `agent:console`. *Where:* `scripts/gen-control-plane.mjs`, ADR-0008 § Amendment.
  *Check:* does the app render fli-core's page from its own spec, rather than hand-rolling a console?

## 4 · Refusals are data

- [ ] **Named failure modes, stable integer codes, typed details.** `failureMode` + `details` carrying enough to
  succeed on the next call (e.g. `notChosen.details.unchosen`, `overlap.details.free`); codes never renumbered.
  *Where:* `src/core/failure-codes.ts`, `src/core/refusal-details.ts`, ADR-0007. *Check:* can an agent recover from
  a refusal in one round trip without re-reading the document?

## 5 · Context: brand / project / video (the open contract)

- [ ] **Launch pointed at a project, re-point while running.** Door 2: `scripts/app.sh start --brand … --project …
  [--video …]` (argv); door 3: `context.select` / `flicast context select`. The context belongs to the run, never to
  settings; a refused launch keeps the previous context. *Where:* `src/main/open-context.ts`, `docs/open-contract.md`.
  *Check:* does the app accept the same flags, answer `context.get`, and refuse with the suite's codes?
- [ ] **Say what is active.** `context.active`, `context.get` (check `refused` first). *Check:* can an agent ask
  "what is open?" before acting?

## 6 · Lifecycle an agent can drive

| Action | Agent via door / CLI / MCP | Agent via shell | Human only |
|---|---|---|---|
| Is it up? | `GET /v1/health`, `system.status` (pid, startedAt, context, busy), `system.diagnostics` | `scripts/app.sh status` | — |
| Start (on a project) | — (the app must be up to answer) | `scripts/app.sh start [--brand --project]` | — |
| Bring to front | — | `scripts/app.sh show` | — |
| Open / close / list projects | `project.open`, `project.close`, `project.list`, `project.create` | — | picking a path (`project.pickPath` ★) |
| Logs | `system.logs`, `flicast logs --tail N` | `scripts/app.sh logs` | — |
| **Quit** | `system.quit` — the orderly quit after the reply; refused `app-busy` (details `busy`) during a take or a running task | `scripts/app.sh stop` (a Quit Apple event to the bundle id) | ⌘Q · `system.quit { force: true }` |
| **Restart / relaunch** | `system.restart` — starts again on the CURRENT brand/project/video; same `app-busy` rule. (`recording.relaunch`, for a new grant, stays ★) | `scripts/app.sh restart` | Relaunch FliCast button · `system.restart { force: true }` |

The three are `@flivideo/core` v0.7.0's lifecycle contract (`src/core/ops/lifecycle.ts`): the same shapes in every Fli app.
`force: true` is refused for agents and the CLI in the core; the door refuses every `human:*` principal, so only the UI can force.
*Check:* list which rows another app can do without a person — and which it can do only from a shell.

## 7 · The launcher (macOS permissions follow the app, not the launcher's parent)

- [ ] **The app runs as its own bundle, started by LaunchServices.** `scripts/app.sh` builds, then
  `open -n -a $FLICAST_HOME/launcher/FliCast.app --args out/main/index.js …` (bundle id `com.appydave.flicast.dev`,
  ad-hoc signed once per Electron version). *Why:* macOS charges Screen Recording to the responsible process;
  launched from tmux or an agent, the grant was the launcher's parent's. *Check:* `ps -o ppid= -p <app pid>` is 1,
  and System Settings lists the app by its own name. Only needed for apps that need a TCC grant.

## 8 · The test harness

- [ ] **A fake engine beneath the real app.** `APP_TEST_HOOKS=1 FLICAST_FAKE_RECORDKIT=1` swaps the capture port
  only; the real UI, core and host run. *Where:* `src/main/index.ts`, `uat/README.md`.
- [ ] **uat stories drive the BUILT app over CDP and locate controls by verb.** Every control carries `data-verb`;
  a deliberately broken self-test story must fail or the run aborts. *Where:* `uat/`, `npm run uat`,
  `test/renderer-interaction.test.ts`. *Check:* can a test press a control without knowing its label or position?
- [ ] **Isolated homes.** Harnesses launch through `scripts/isolated-env.mjs` (`FLICAST_HOME`, user home, no
  `FLIVIDEO_*`), so a run never touches real projects. *Check:* `test/main/harness-env.test.ts`.

## 9 · Agent-safety rules

- [ ] **A ★ fence in the core.** Press Record, grant permissions, pick a file, reveal in Finder: refused for
  `agent` and `cli` principals inside `core.call`, not in an adapter (`HUMAN_ONLY` in `src/core/registry.ts`).
- [ ] **No OS keystrokes or clicks to drive the app** — verbs, or CDP in the harness. Real key presses, native
  dialogs and TCC grants stay human.
- [ ] **Privacy by construction:** typed characters are never captured unless a person turns it on twice
  (`docs/spec/security-privacy.md`); `characters` is stripped from anything an agent reads.
- [ ] **Never `pkill -f electron`** (other Fli apps match); stop an app by its own control path.

## 10 · Shared through `@flivideo/core` vs FliCast-only

| Shared (fli-core — cite its mirror, don't re-implement) | FliCast-only (a pattern to copy, not a library) |
|---|---|
| open-args parsing (`parseOpenArgs`), brands, project resolution | the capability core, registry, ★ fence |
| `fli.<app>.<name>.json` naming (`appFileName` / `parseAppFile`) | the HTTP door, CLI, MCP server, skill |
| lab paths (`labPath`) | OpenRPC + capability-surface generators, the console |
| video folder / file naming (`videoFolderName` / `videoFileName`) | failure codes + typed refusal details |
| window positions (`placeWindow` / `loadWindow` / `trackWindow`) | the LaunchServices launcher, the uat harness |
| the control-plane page (`renderApiPage`, v0.7.0) · suite refusal codes (`SUITE_FAILURE_CODES`, FliCast's numbers) | FliCast's own capability page, its preload bridge |

FliCast's door-2 resolution chain (`src/main/open-context.ts`) is hand-rolled over fli-core because fli-core's
`resolveOpenContext` refuses plain folders; it moves into fli-core when `acceptFolders` ships.
