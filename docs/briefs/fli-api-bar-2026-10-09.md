---
created: 2026-10-09
timestamp: 2026-10-09
---

# The Fli API bar: FliCast audit, the standard, the FliEdit gap (2026-10-09)

**Purpose**: David's brief, dispatched by `flivideo-orch`, handover
`/Users/davidcruwys/dev/ad/brains/docs/handovers/HANDOVER-2026-10-09-fli-api-gap-flicast-fliedit.md`. Audit FliCast
(don't assume it's gold), write the bar for "agent-drivable app + API page usable by humans and agents equally",
gap-analyse FliEdit live against it, close the gaps, and write it up so the other apps can be done the same way.

**For Agents**: The bar (§2) is the standard to hold any Fli app to. The repeatable procedure is the playbook:
`/Users/davidcruwys/dev/ad/flivideo/docs/fli-api-playbook.md`. Every claim here was checked live against a
throwaway project (`/private/tmp/fli-api-gap/`) unless it says *code-read*.

## Verdict

- **FliCast is the best Fli API, but it is not gold.** The design holds up: one seam, the ★ fence in the core,
  refusals as data, an in-app console, and pages that label which copy they are. Three bugs let a careless call do
  the wrong thing without telling anyone (§1.2). Its own generated page and uat had drifted out of date.
- **FliEdit has the same seam with nothing for a person to use.** Every edit is a verb (62), but it had no callable
  page, no console, one Help-menu link, and the same three door bugs as FliCast. Its version string was Electron's.
- **Now done:**
  - **FliEdit is at the bar except viewer control.** It has a capability console, an open spec, a "which copy"
    banner, a committed snapshot, and a hardened door.
  - **FliCast's three door bugs are fixed.**
  - **The console features live in fli-core v0.23.0,** so every app gets them by bumping one dependency.
  - **Viewer-control verbs are ticketed** (§4).

## 1 · FliCast audit (live, isolated home, throwaway project)

Started the README way, `npm run app -- start`, with `FLICAST_HOME=/private/tmp/fli-api-gap/flicast-home` and a
throwaway `--project`. Exercised it over `/v1/rpc` and through the Help → Capability console window. FliCast `df360dc`.

### 1.1 Genuinely good — keep and copy

| What | Evidence |
|---|---|
| One seam `core.call(principal, verb, input, {dryRun, idempotencyKey})` behind every door; ★ fence enforced in the core | `project.reveal` as `agent:gap` → `−32001 forbidden` |
| Dry run returns the patch **and** its inverse; nothing changes | `zoom.add` dry run: `changed` + `inverse`, `zoom.list` unchanged |
| Refusals are data (ADR-0007) — a refusal tells you how to succeed | overlapping `zoom.add` → `−32035 overlap` with the clashing zoom and every free range |
| Undo by principal | `history.undoBy agent:gap` removed only `agent:gap`'s zoom |
| Open, token-free surface: `/v1/docs` + `/v1/openrpc.json` (no secret in them, asserted by test) | both 200 without a token |
| The page says **which copy** it is | served: "LIVE — THIS MACHINE … Read-only … Open Help → Capability console…"; console: "CAPABILITY CONSOLE — LIVE … calling as agent:console" |
| Console is a separate window, IPC as hard-coded `agent:console`, narrow preload, ★ offered and refused, writes dry-run first, undo per result (ADR-0008) | opened from Help; uat story 49 |
| Generated, drift-checked surfaces (`npm run api:check` in pre-push) | `api:check`: 140 methods, current |
| Batches and notifications refused with a reason, not silently half-done | `http-door.ts:119-125` (code-read) |

### 1.2 Bugs (fixed in this run)

| Bug | Evidence (before) | Effect |
|---|---|---|
| **Suite principal header ignored.** Only `X-FliCast-Principal` is read; the suite's `x-fli-principal` (fli-core `PRINCIPAL_HEADER`, sent by FliEdit's CLI, FliTools, fli-core's console) silently becomes `agent:http` | `http-door.ts:205`; `marker.add` with `x-fli-principal: agent:suite` → history `agent:http` | the caller's edits are beyond `history.undoBy <its name>`; provenance lies |
| **`dryRun: "true"` (a string) applies the write** | `http-door.ts:176` and `:262` (`=== true`); `zoom.add {dryRun:"true"}` → zoom created | a preview becomes a real edit |
| **`dryRun` beside `params` on `/v1/rpc` is ignored → applies** | `http-door.ts:146` reads only `params`; `{"dryRun":true}` at envelope level → zoom created | the same, for anyone who guesses the JSON-RPC shape |
| **The page contradicts itself on the ★ count**: tile says 12 ★, banner says "the ★ ten", figure says "The ten ★ verbs" | `gen-api-page.mjs:612`, `:813` | readers can't trust the numbers |
| **The page says the try-it panel "must call the door with a token" — "if it is ever added"** | `gen-api-page.mjs:748` | the console exists (ADR-0008) and works over IPC; the page describes a design that was rejected |
| **uat story 49 failed on main**: `expectConsoleStars: 10`, the console has 12 | `uat/stories/story-49-…md:26`; `node uat/run.mjs 49` → FAIL "found 12" | the gate for the console was red and nobody knew |

### 1.3 Weak — ticketed, not fixed here

- **The second console page is weaker than the first.** The "agent door open" chip opens `api/control-plane.html`
  (fli-core `renderApiPage`, `scripts/gen-control-plane.mjs:26`). It has a dry-run box that starts **unticked**,
  no undo, and no which-copy banner. That breaks ADR-0008 §6 on its own app's second surface. Fix with the fli-core
  v0.23.0 bump (ticket T-FC1).
- A door ★ refusal carries no `principal` in `data` (`project.reveal` → `data:{failureMode}` only); FliEdit's does.
- ADR-0005/0008 prose still says 132 verbs and "ten ★". They are history and say so, but the CLAUDE.md "twelve" is
  the only current count in prose.

## 2 · The bar — "agent-drivable app + API page usable by humans and agents equally"

Taken from FliCast as audited, with its bugs fixed rather than copied. **B1–B12 must all hold.**

| # | Bar item | Done when |
|---|---|---|
| B1 | **One seam.** Every door (UI IPC, HTTP `/v1/call` + `/v1/rpc`, CLI, console, MCP) calls the same `core.call(principal, verb, input, opts)` | a verb added once appears on every door |
| B2 | **The fence is in the core.** Human-only verbs (and human-only *params*) are refused for `agent:*`/`cli` with `forbidden` and `data.principal` | firing a ★ verb as an agent → `−32001`, principal named |
| B3 | **Principal is exact.** Read `x-fli-principal` (an app may also read its legacy header). Refuse a disagreeing pair or a foreign `x-*-principal`; never guess | a wrong header → 4xx naming the right one, nothing done |
| B4 | **Dry run is safe.** `dryRun` is a boolean or absent — anything else is refused; it rides in `params` on `/v1/rpc` and a misplaced one is refused; dry run returns patch + inverse and changes nothing | `dryRun:"true"` → `invalidInput`, nothing changed |
| B5 | **Every write is heard.** JSON-RPC notifications (no `id`) are refused, not run silently; batches are refused or all-or-nothing | a no-`id` write → `−32600`, nothing changed |
| B6 | **Undo by principal.** `history.undoBy {principal, n}` removes only that caller's edits | undo one agent's edit; a person's edit stays |
| B7 | **Refusals are data.** Named `failureMode`, stable JSON-RPC code, typed `details` a caller can retry from | a refusal names what to change |
| B8 | **The surface is open.** `GET /v1/docs` and `GET /v1/openrpc.json` need no token, carry no token or project data (tested), loopback only | both 200 without auth; test asserts no token bytes |
| B9 | **A callable page in the app.** A capability console window: every verb listed and callable, ★ offered and refused on screen, fixed `agent:console` principal over IPC (no token, no principal field, no human bridge in that window), **dry run ticked by default**, an Undo beside every applied write | fire / dry-run / apply / undo / refusal by real clicks |
| B10 | **Which copy.** Every rendering says whether it is the console (live), the page a running app serves (live, read-only, where to fire), or a snapshot (generated date) | three banners, worked out at load |
| B11 | **Findable.** Help → Capability console… (with a shortcut), a visible chip/button in the main window, the CLI prints the URL, `/v1/docs` says where the console is | a person finds it without being told |
| B12 | **Generated, never hand-kept.** Spec, page, snapshot and CLI help come from the registry. A drift check runs in the gate. A snapshot's date changes only when its content does | `api:check` fails on a stale file |
| B13 | **Every UI action has a verb** (or a written reason it is human-only). View state included: transport, playhead, zoom, selection, panels | the coverage table has no unexplained gap |
| B14 | **Correct identity.** `/v1/health`, `system.status` and OpenRPC `info.version` report the app's own version | not Electron's |

## 3 · FliEdit gap table (live, isolated home, throwaway project)

FliEdit `2ac6a1c` before; started with `scripts/app.sh start` on `FLIEDIT_HOME=/private/tmp/fli-api-gap/fliedit-home`.

| Bar item | FliCast | FliEdit (before) | Action taken |
|---|---|---|---|
| B1 one seam | ✅ | ✅ 62 verbs, `/v1/call` + `/v1/rpc` + CLI + IPC | — |
| B2 fence in core | ✅ (no `principal` in door refusal data) | ✅ `edit.reveal` → `−32001` with `details.principal` | — |
| B3 exact principal | ❌ suite header ignored → `agent:http` | ❌ `x-flicast-principal` ignored → `agent:http` (live: history `by agent:http`) | **Fixed both.** FliEdit refuses any foreign `x-*-principal` (400, names `x-fli-principal`); FliCast reads both headers, refuses a disagreeing pair or a foreign one |
| B4 safe dry run | ❌ `"true"` applies; envelope-level ignored | ❌ `"true"` applies (live: marker created) | **Fixed both**: non-boolean refused `invalidInput`; FliCast refuses an envelope-level `dryRun`/`idempotencyKey` |
| B5 every write heard | ✅ refuses notifications | ❌ no-`id` write ran, answered `204` (live: marker created) | **Fixed**: fli-core `answerJsonRpc({refuseNotifications})`, FliEdit opts in → `−32600`, nothing runs |
| B6 undo by principal | ✅ | ✅ | — |
| B7 refusals are data | ✅ | ✅ | — |
| B8 open surface | ✅ | ⚠️ `/v1/docs` open; **`/v1/openrpc.json` behind the token** | **Fixed**: open, test asserts no token in either |
| B9 callable console | ✅ (2nd page weaker, T-FC1) | ❌ reference only (`mode:"reference"`, `rpcPath:null`), no console window | **Built**: `src/main/api-console.ts` + `src/preload/console.ts` (fliConsole only, no `window.fliedit`), IPC `fliedit:console-call` → `core.call('agent:console')`. Page from fli-core v0.23.0 with `dryRunDefault` + `undoBy: history.undoBy`. Verified by real clicks over CDP (below) |
| B10 which copy | ✅ | ❌ none | **Built** in fli-core (`surface` option); FliEdit's door page, console and snapshot all carry it |
| B11 findable | ✅ Help + status-line chips + CLI `docs` | ❌ Help → "API reference" only | **Fixed**: Help → Capability console… (⇧⌘K), toolbar button "API · door :7171", `fliedit docs`, banner points at the console |
| B12 generated + snapshot | ✅ (snapshot = committed page) | ⚠️ spec generated; **no snapshot** | **Added** `api/reference.html` (generated, drift-checked; date = day the content last changed) |
| B13 every UI action a verb | ✅ (coverage audit) | ❌ viewer has none: play/pause, J/K/L, step, prev/next edit, Home/End, seek, zoom/fit, snapping, select/select-all/deselect, inspector tabs, go-to-marker/chapter/caption | **Ticketed** (§4) — view state lives only in the renderer; needs a main↔renderer view channel |
| B14 identity | ✅ | ❌ reported **44.4.5** (Electron's) under `app.sh` — `index.ts:24` read the launcher's stub `package.json` | **Fixed**: reads its own `package.json` (name-checked); console banner now "FliEdit 0.1.0" |
| Oddity: `context.get` | n/a (FliCast: `context.get` = open contract, `context.active` = project) | `context:null, missing:[]` with an edit open (folder-only launch) | **Fixed**: folder-only context reported with `brand`/`project` null and listed in `missing`; `edit {name, path, projectDir}` always present |
| Oddity: CLI dry-run went out as `cli` | — | `--as` absent ⇒ `cli`, silently | **Fixed**: `$FLI_PRINCIPAL` honoured; every verb call prints `fliedit: as <principal>` (with the hint when `cli`) on stderr. `cli` stays the default — it is the documented CLI principal, not a bug |

**Human-only in FliEdit** (unchanged, correct): `edit.pickPath`, `edit.reveal`; `export.start` with `overwrite`;
`system.quit`/`restart` with `force`.

### Live proof of the FliEdit console (built worktree, real clicks over CDP)

`/private/tmp/fli-api-gap/scripts/console-probe.mjs`:
- Clicked the toolbar "API · door :57816" → the console window opened. Banner: "CONSOLE — LIVE · inside FliEdit
  0.1.0, calling as agent:console. 62 methods · 5 ★ …". `window.fliConsole` = object; `window.fliedit` = undefined.
- `marker.add`: the dry-run box was ticked by default. Firing it returned `dryRun:true` with no Undo offered, and
  0 markers were written.
- Unticked and fired again: 1 marker written, and "Undo — history.undoBy agent:console" appeared. Clicking it said
  "Undone", leaving 0 markers.
- `edit.reveal` → `−32001 forbidden`, `principal: agent:console`. Asking for the console a second time focused the
  same window (2 windows total).

Not verified: the editor repainting beside the console on screen (the display was asleep; the core event path is
unchanged).

## 4 · Tickets for openrig-orch

**Why viewer control is ticketed, not built:** every viewer action (playhead, transport, zoom, selection, snapping,
inspector tab) is renderer state in `src/renderer/src/store.ts`. Nothing in main or the core knows it. Making it
drivable means:
- a view-state model,
- a main→renderer command channel with an answer,
- a `view.*` capability family that is non-undoable and never touches the document,
- events, and a decision on whether an agent may move a person's playhead mid-play.

That is a design-sized bundle, not a fix. It belongs with the other openrig work.

| # | Title | Done when |
|---|---|---|
| T-FE1 | FliEdit `view.get` — the viewer's state as data | returns `{playhead, playing, shuttleRate, zoom, scroll, snapping, selection[], inspectorTab}`; `context.get`-style query, read-only |
| T-FE2 | FliEdit `view.transport` — play / pause / stop / shuttle (J/K/L rates) | an agent plays and stops the viewer; Space/J/K/L call the same verb; `view.get` reflects it |
| T-FE3 | FliEdit `view.seek` — absolute frame, ±frames, prev/next edit point, start/end, go-to marker/chapter/caption | every arrow/Home/End key and every marker-list click is this verb; refuses out-of-range with the valid range in `details` |
| T-FE4 | FliEdit `view.zoom` — in / out / fit / set | ⌘= / ⌘- / ⇧Z call it; `view.get.zoom` matches |
| T-FE5 | FliEdit `view.select` — set / add / all / none, and `view.snapping` | ⌘A, Esc, clicks and N call them; selection-dependent keys (⌫, E, ⌘D, ⌘L) read the same state |
| T-FE6 | FliEdit `view.inspector` — which tab/panel is showing | a click on a tab and the verb do the same thing |
| T-FE7 | FliEdit view verbs in the pinned table + console | the capability count, `api:check` and the console list them; none is ★; none mints an undo entry (test) |
| T-FC1 | FliCast: bump `@flivideo/core` v0.18 → v0.23 and pass `dryRunDefault`, `undoBy: 'history.undoBy'`, `surface` in `scripts/gen-control-plane.mjs` | the "agent door open" page dry-runs first and offers Undo; `api:check` + `test/main/control-plane.test.ts` green; preload's `fliConsole.call` honours `{dryRun}` |
| T-FC2 | FliCast: put `principal` in door refusal `data` | `project.reveal` as `agent:x` → `data.principal: "agent:x"` on `/v1/rpc` and `/v1/call` |

## 5 · Where the changes are

| Repo | Commit | What |
|---|---|---|
| `flivideo/fli-core` | `fc55518` (v0.23.0) | `renderApiPage` `dryRunDefault`, `undoBy`, `surface`; `answerJsonRpc` `refuseNotifications` |
| `flivideo/fliedit` | see the report to flivideo-orch | console window + preload + IPC, door hardening, open spec, snapshot, `context.get`, CLI principal, version |
| `flivideo/flicast` | see the report to flivideo-orch | door principal + dryRun, page text, uat story 49 |
