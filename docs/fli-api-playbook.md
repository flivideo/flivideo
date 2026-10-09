---
created: 2026-10-09
timestamp: 2026-10-09
---

# Fli API playbook: audit → bar → gap → fix

**Purpose**: The repeatable way to bring any Fli app (FliHub, FliCut, FliStudio, FliTools, Teletubby, …) up to the
"agent-drivable app + API page usable by humans and agents equally" bar. It was worked out on FliCast and FliEdit
on 2026-10-09.

**For Agents**: The bar itself, and the FliCast/FliEdit worked example, live in
`/Users/davidcruwys/dev/ad/flivideo/docs/briefs/fli-api-bar-2026-10-09.md` (§2 is the bar, B1–B14). This file is the
procedure. Do one app per run. Never use a real `v-*` project.

## The loop

```
1 AUDIT (live)  →  2 BAR (B1–B14, copy §2)  →  3 GAP TABLE  →  4 FIX or TICKET  →  5 PROVE (real clicks)  →  6 WRITE UP
```

## 0 · Before you touch anything

- [ ] Note which Fli apps are running (`lsof -nP -iTCP -sTCP:LISTEN | grep ':71'`). Never stop or restart a process
      you did not start, and never touch FliHub, FliCut or FliStudio processes when the brief excludes them.
- [ ] Find the app's isolation knobs: `<APP>_HOME`, `<APP>_PORT`, `<APP>_PROJECT_DIR`, `LAUNCH_HIDDEN`, any
      `isolated-env` script. **Always** run on an isolated home.
- [ ] Work in a git worktree. If `package.json` has a relative `file:` dependency, keep the worktree at the same
      directory depth, or repoint that one symlink in `node_modules`.
- [ ] No prettier config in the repo? **Don't run prettier.** Its defaults reformat whole files. Edit by hand, in the
      file's own style.

## 1 · Audit — the live-probe recipe

```bash
P=/private/tmp/<app>-api-gap; mkdir -p $P/{home,proj}
ffmpeg -loglevel error -f lavfi -i testsrc=size=1280x720:rate=30:duration=12 \
       -f lavfi -i sine=frequency=440:duration=12 -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest $P/test.mp4
<APP>_HOME=$P/home <APP>_PROJECT_DIR=$P/proj bash scripts/app.sh start      # the README's way, isolated
TOK=$(python3 -c "import json;print(json.load(open('$P/home/control.json'))['token'])")
rpc(){ curl -s -H "authorization: Bearer $TOK" -H 'content-type: application/json' \
            -H "x-fli-principal: agent:probe" -d "$1" http://127.0.0.1:<port>/v1/rpc; echo; }
```

Fire each probe below, then **read state back to prove what happened** (a list verb, `history.list`). The answer
alone proves nothing.

| Probe | Request | Bar item | Pass |
|---|---|---|---|
| open surface | `curl -o /dev/null -w '%{http_code}' …/v1/docs` and `…/v1/openrpc.json` with no token | B8 | both 200, no token in the bytes |
| create something | e.g. `edit.create` / `project.importVideo` on `$P/proj` | B1 | ok |
| dry run | a write with `"params":{…,"dryRun":true}` | B4 | patch + inverse; list unchanged |
| **string dry run** | `"dryRun":"true"` in params | B4 | `invalidInput`; **list unchanged** |
| **misplaced dry run** | `"dryRun":true` beside `params` | B4 | refused; **list unchanged** |
| **notification** | the same write with no `"id"` | B5 | `−32600`; **list unchanged** |
| **foreign header** | send `x-flicast-principal: agent:x` (or any `x-<other>-principal`) instead | B3 | refused; never recorded as `agent:http` |
| suite header | `x-fli-principal: agent:probe` then `history.list` | B3 | history says `agent:probe` |
| ★ fence | a human-only verb as `agent:probe` | B2 | `−32001 forbidden`, `data` names the principal |
| refusal as data | provoke a conflict (overlap, missing id) | B7 | `failureMode` + code + `details` you could retry from |
| undo by principal | `history.undoBy {"principal":"agent:probe"}` | B6 | only your edit goes |
| identity | `/v1/health`, `system.status`, OpenRPC `info.version` | B14 | the app's version, not Electron's |
| context | `context.get` with something open | — | never "nothing" while something is open |
| CLI | the app CLI with `--dry-run` and without `--as` | B3 | says who it called as |
| findability | the menus (`osascript … get name of every menu item of menu "Help" of menu bar 1`), the main window, the CLI help | B11 | a console reachable without being told |
| UI actions → verbs | read the key map / toolbar / panels: list every action and the verb it calls | B13 | gap list |

## 2 · The bar

Copy B1–B14 from the bar file, §2. Don't rewrite them per app; if an app genuinely needs a different rule, add a row
saying why.

## 3 · Gap table

One row per bar item, plus a row per oddity you found. Columns, always these four:

| bar item | reference app (FliCast) | this app (before) | action taken |
|---|---|---|---|

Put evidence in every cell: `file:line`, or the live request plus what you read back.

## 4 · Fix — the shared parts first

Most of the bar is already in `@flivideo/core` (v0.23.0+). Bump the pin (a tag, never `file:`), then:

| Need | fli-core | App-side |
|---|---|---|
| B5 | `answerJsonRpc(body, seam, { codes, names, refuseNotifications: true })` | — |
| B9 console page | `renderApiPage(doc, { console: { rpcPath, principal: 'agent:console', dryRun: true, dryRunDefault: true, undoBy: 'history.undoBy' }, surface: {…} })` | a non-modal window loading that page, a **separate preload exposing only `window.fliConsole.call(method, params, {dryRun})`**, and an IPC handler that calls the core as the constant `agent:console`. Pattern: FliEdit `src/main/api-console.ts`, `src/preload/console.ts`, `src/main/index.ts` (`IPC.consoleCall`) |
| B10 | `surface: { generatedAt?, consoleHint }` on every rendering | — |
| B8 | — | serve `/v1/docs` and `/v1/openrpc.json` **before** the auth check; test that neither contains the token |
| B3/B4 | — | reject a foreign `x-*-principal`; reject a non-boolean `dryRun` (FliEdit `foreignPrincipalHeader` and `dryRunOption` in `src/main/control/http-door.ts`) |
| B11 | — | Help → Capability console… (⇧⌘K), a button in the main window, `<app> docs` in the CLI |
| B12 | — | commit a generated snapshot (`api/reference.html`), drift-checked, dated by content (FliEdit `scripts/api.gen.ts`) |

**Fix or ticket?** Fix anything that is a door, page or identity bug, or that fli-core already provides. Ticket new
verb *families* that need a new main↔renderer channel or a product decision (FliEdit's viewer control). A ticket is a
title plus a checkable done-when, filed in the app's bar section under "Tickets for openrig-orch".

**Before pushing:** run the repo's whole gate (typecheck, unit, integration, golden, build, `api:check`,
`docs:check`, the uat story for the console if it has one, and whatever `.githooks/pre-push` runs). Ask
`flivideo-orch` before pushing anything a running app would hot-reload, or anything in a shared repo (fli-core). No
force-push.

## 5 · Prove it — real clicks, not a code trace

Drive the **built** app over CDP with `playwright-core`'s `_electron.launch` on an isolated home (FliEdit:
`/private/tmp/fli-api-gap/scripts/console-probe.mjs`). It must:

1. click the main-window entry point → the console window opens;
2. read the banner (CONSOLE — LIVE, principal, counts) and assert `window.fliConsole` exists and the human bridge
   does not;
3. fire a write with the box ticked by default → `dryRun:true`, no Undo button, state unchanged;
4. untick and fire → state changed, Undo shown; click it → state restored;
5. fire a ★ verb → `forbidden`, principal named;
6. ask for the console again → the same window, focused;
7. take a screenshot of the console and look at it.

`screencapture` shows black when the display is asleep. A CDP screenshot of the page still works.

## 6 · Evidence format

In the app's bar section (or its own dated brief in `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/`):

- **Verdict** first (good / bad / done), in plain words.
- **Audit**: good / bugs / weak, each with `file:line` or a live request → answer → read-back.
- **Gap table** (four columns above).
- **Live proof**: the probe script path and its output, numbers included (markers before/after, codes).
- **Not verified**: say what you did not check, plainly.
- **Tickets for openrig-orch**: title + done-when.
- **Commits**: repo · hash · one line.

## Order for the rest of the suite (prepared, not started)

| App | Uses `renderApiPage` | Likely first gaps |
|---|---|---|
| FliCut | `src/main/control-surface.ts` | B9 console window, B10, B3/B4/B5 door bugs |
| FliStudio | `server/src/capabilities/http.ts` (web, not Electron) | B9 needs a `tokenPath` or same-origin session instead of IPC; B3/B4/B5 |
| FliTools | `src/server.ts` (a service, no window) | B9 as a served console with `tokenPath`; B11 via CLI + docs |
| Teletubby | `src/main/control-server.ts` | as FliCut |
| FliHub | none found | the whole bar — start at B1 |
| FliCast | done; tickets T-FC1, T-FC2 | — |
