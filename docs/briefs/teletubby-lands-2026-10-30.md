# Brief — Teletubby lands on the right script; Overlay Pilot media; named request log (2026-10-30)

**Purpose**: David's go ("Go with all three", 2026-10-30 evening, relayed by brains-d5) on three fixes found by
flivideo-orch's investigation of the B674 demo.

**For Agents**:
- Two builders: `tubby-land-dev` (FliStudio, Jobs A–C) and `tubby-panel-dev` (Teletubby, Job D).
- `flivideo-orch` is your boss. Report and route every decision to it with SendMessage; never park waiting on
  David in your own window. flivideo-orch merges, restarts and does the live verification.

## The finding (why)

Teletubby holds two different things:
- **context** — the project it is pointed at (`context_select` / `context_get`);
- **stage** — the set and script on screen (`workspace.position`, changed only by the talent's panel or `stage_select`).

`context_select` on a running Teletubby never moves the stage, by design (W6 F6,
`/Users/davidcruwys/dev/ad/flivideo/teletubby/src/renderer/src/App.tsx`, `onControlChanged`). FliStudio's door
(`/Users/davidcruwys/dev/ad/flivideo/flistudio/server/src/launch/doors.ts`, Teletubby `switchTo`) and Story Pilot's
`story.script.send` (`flistudio/modules/storypilot/server/index.ts`, `handoverOf` in `story.ts`) call only
`context_select` (+ `script.write`). Measured live: context = d13-overlay-pilot, `workspace.position.setId` =
`kybernesis-phase-1`. FliStudio's "Teletubby · here" dot reads `context_get` (`readContext`), so it is green while
the wrong words are on screen. Known gap: `teletubby/docs/briefs/stage-select-followups-2026-10-17.md` item 1.

`stage_select { setId, scriptId? }` is on the agent surface since 2026-09-23; it refuses `app_busy` while the talent
is on the prompter; the window applies it; the result is read from `list_rigs` → `workspace.position`.

## Job A · FliStudio — one door that always lands (tubby-land-dev)

1. **One sequence**, shared by the Teletubby door's `switchTo` (app.launch on a running Teletubby) and Story Pilot's
   `story.script.send`: `context_select` → `script.write` (send only) → `stage_select { setId, scriptId? }` → read
   `list_rigs` → `workspace.position` back (poll briefly; the window applies the request) and report what is on stage.
   - switchTo: stage the project's set when exactly one is attached (the open project's own set); none → say "no
     set attached"; several → stage the one the workspace remembered if it is this project's, else the first, and
     say which.
   - send: stage set `d13…-scripts`-style set that `script.write` wrote into, with `scriptId` = the written id.
   - `app_busy` → result says **"not staged: the talent is on the prompter"** — never a silent success, never a
     failure of the switch/write itself. Position read back ≠ requested → say so.
   - Remove the "choosing the set is UI-only" notPassed rows and comments that are now false (doors.ts, launch.ts).
   - Story Pilot's handover (`handoverOf` calls list, the Claude-Code hand-off) gains the `stage_select` step too.
2. **The "here" dot**: Teletubby is "here" only when context = this project AND `workspace.position.setId` is one of
   this project's sets. Context right but stage wrong → a distinct state that says so (e.g. "pointed here, showing
   <set>"). Find where the dot is computed (doors `readContext`, apps.status / ProjectHome) and change it there.
3. Stub doors (`server/src/test/stub-doors.ts`) learn `stage_select` + `list_rigs` position so tests cover: lands,
   app_busy, position mismatch, here vs pointed-but-showing-other.

## Job B · FliStudio — Overlay Pilot media (tubby-land-dev)

`flistudio/modules/overlay-pilot/client/OverlayPilot.tsx` (~L430–490) mounts a live `<video src=…#t=1
preload=metadata>` for every original and every render (Joy a01: 12 players over ~1.4 GB). Show poster stills
instead; generate a poster for each original the same way renders get theirs (server side, cached); mount a
`<video>` only when that tile is clicked (the existing Watch / clip viewer path). No `<video>` element on first paint.

## Job C · FliStudio — name the capability in the request log (tubby-land-dev)

Every `POST /api/call` log line carries the capability name (and principal), e.g.
`POST /api/call assets.list human:ui 200 120ms`. Never log input values or tokens.

## Job D · Teletubby — the panel and cold start (tubby-panel-dev)

1. The setup panel's PROJECT row loses the cross-project "all sets" chip/picker: it lists only the open project's
   sets. Choosing between sets and scripts **within** the project stays. With no project open, keep today's list
   (there is no project to scope to) — say so in a comment.
2. Cold start with no context (no `--brand/--project`) opens the empty shell (`EmptyShell`), not the remembered set
   from another project. With a context, today's `pickOpeningSet` rule stands.
3. Close `docs/briefs/stage-select-followups-2026-10-17.md`: Status CLOSED, item 1 → done in FliStudio branch
   `tubby-lands` (name the commit once flivideo-orch tells you, or say "FliStudio Job A"), item 2 → (a) kept.
4. Update tests (`pickOpeningSet`, `visibleSets`, panel) and the teletubby skill notes if they describe "all sets".

## Repos and branches

| Builder | Repo | Worktree | Branch |
|---|---|---|---|
| tubby-land-dev | `/Users/davidcruwys/dev/ad/flivideo/flistudio` | `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/tubby-lands` | `tubby-lands` off `origin/main` (`3ff0137`) |
| tubby-panel-dev | `/Users/davidcruwys/dev/ad/flivideo/teletubby` | `/Users/davidcruwys/dev/ad/flivideo/teletubby-worktrees/tubby-panel` | `tubby-panel` off `origin/main` (`efabbe5`) |

## Gates (all must pass, no newly failing test)

- FliStudio: build · typecheck · lint (0 errors) · format:check · api:check · `npm test` (extension-core,
  overlay-pilot, storypilot, server, client) · `npm run test:e2e`. Baseline at `c4ac75c`: extension-core 46,
  overlay-pilot 64, storypilot 36, server 698+2, client 306, e2e 31.
- Teletubby: typecheck · build · `npm test` (baseline 438 passed, 11 skipped) · `npm run api:openrpc` if the API moved.

## Limits

- Work only in your worktree. Never touch the live checkouts, never merge to main, never start/stop/restart any app,
  never run `my-app`. Never use ports 7150/7151/7111/7121/7161/5173/5101 — tests use random ports / stubs.
- Never touch `/Users/davidcruwys/dev/video-projects/`, `~/Library/Application Support/teletubby/`,
  `~/.config/appydave/` (read-only is fine), `~/.claude/`. No `pkill -f` / `killall`.
- Park, with a reason, anything that fails its gate after 3 attempts.

## Done when

Branch pushed, every gate passing. Report to flivideo-orch: head, gate numbers, what changed per item, anything parked.
flivideo-orch then merges both, checks `system.status` busy before restarting, and verifies David's exact scenario
live: Teletubby running and staged on Kybernesis → Story Pilot Send on d13 → `workspace.position` on the d13 set.
