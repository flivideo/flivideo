# Brief — let a FliStudio extension call another app's door (G1) (2026-10-30)

> **RESCOPED 2026-10-30 ~11:05 by flivideo-orch — David overrode Q0.** FliHub v2 hosts NO extensions;
> extensions belong to FliStudio only. So: **DROP work items 1 (host-neutral ExtensionHost), 3 (host-supplied
> stages) and 5 (extraction plan).** **KEEP 2 (G1 — call another app's door by name) and 4 (Story Pilot
> Send-to-Teletubby, proves G1), plus 6 (version 0.2.0, CHANGELOG, README, spec/AGENT-NOTES rows).** G1 matters
> more now: FliStudio extensions will call FliHub v2's door. Leave Overlay Pilot's host fields where they are.
> Gate and limits unchanged. Done = branch pushed, every gate passing, report to flivideo-orch.


**Purpose**: The one change that has to land before the FliHub v2 build: FliStudio and FliHub must share
one extension contract, and an extension must be able to call another FliVideo app's door.

**For Agents**:
- You are `extcore-dev`. `flivideo-orch` is your boss: report to it with SendMessage, never park waiting
  on David in your own window. Every decision goes to flivideo-orch with a recommendation and pros/cons.
- Work only in a worktree. Push the branch. flivideo-orch merges and restarts.

## Why (ruled by flivideo-orch, Q0 of the FliHub discovery)

- `/Users/davidcruwys/dev/ad/flivideo/flistudio/extension-core/src/server.ts:21-36` — `ExtensionHost`
  carries Overlay Pilot's own needs (`flitoolsUrl`, `renderScript`, `python`, `flitoolsTimeoutMs`,
  `pollMs`, `fetch`) next to the generic ones (`call`, `log`).
- `extension-core/src/descriptor.ts:11` — `STAGES` is FliStudio's pipeline, hard-coded.
- G1 (from the Story Pilot spec §9): the host holds no address for Teletubby, FliCut, FliHub… so an
  extension cannot call another app. Story Pilot V1 works around it via Claude Code.
- FliHub v2 (decided: rebuild, `/Users/davidcruwys/dev/ad/flivideo/docs/flihub-discovery-2026-10-30.md`)
  ships an extension seam; B-roll capture is its first extension. It must use the same contract.

## Repo and branch

- Repo `/Users/davidcruwys/dev/ad/flivideo/flistudio` (extension-core is a workspace package inside it).
- Worktree `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/extcore-neutral`, branch
  `extcore-neutral`, off `origin/main` (currently `e89f2a7`, Story Pilot merged).

## The work

1. **Host-neutral `ExtensionHost`.** The generic host is `call`, `log`, plus the new app-door call (step 2).
   Everything Overlay-Pilot-specific moves into Overlay Pilot (its own config/options, supplied by the
   FliStudio host when it binds that extension). Story Pilot keeps working unchanged in behaviour.
2. **G1 — call another app's door.** One generic way: `host.app(name).call(method, params)` (shape is
   yours) through that app's own JSON-RPC door, saying who is calling (principal = the extension).
   Addresses come from the host (FliStudio reads them from `~/.config/appydave/apps.json` or its existing
   app-door config — find what FliStudio already uses for its stub doors / app doors, reuse it).
   Add a rule for which extension may call which app (an allow-list in the descriptor is fine).
   FliHub has no door yet — that is expected; the call refuses cleanly.
3. **Stages from the host.** `STAGES` becomes host-supplied (FliStudio passes its pipeline; FliHub will
   pass its own). The descriptor validates `stage` against what the host offers. Keep FliStudio's
   existing stage keys and `ProjectHome.tsx` behaviour identical.
4. **Story Pilot's Send button (proves G1).** Add `story.script.send` (or the shape you pick) that hands
   the current script to Teletubby via `context.select` + `script.write` on its door, plus a Send button
   on the Story Pilot screen. Claude Code's manual hand-off keeps working.
5. **Consumable outside FliStudio — PLAN ONLY.** Write
   `/Users/davidcruwys/dev/ad/flivideo/docs/extension-core-extraction-plan.md`: how FliHub v2 will consume
   extension-core (own repo + git tag like fli-core, or another route), with a recommendation and
   pros/cons. Do NOT create a GitHub repo.
6. Version bump extension-core to 0.2.0 with a CHANGELOG entry; update its README; spec/AGENT-NOTES rows.

## Gate (FliStudio's full set, all must pass, no newly failing test)

build · typecheck · lint (0 errors) · format:check · api:check · `npm test` (extension-core, overlay-pilot,
storypilot incl. conformance, server, client) · `npm run test:e2e` (random ports — it already uses them).
Baseline on `e89f2a7`: extension-core 37, overlay-pilot 64, storypilot 32, server 695+2, client 306, e2e 31.

## Limits

- Never touch the live checkout `/Users/davidcruwys/dev/ad/flivideo/flistudio`, never merge to main,
  never start/stop/restart any app or run `my-app`. Never test against ports 7150/7151/7111/7121/7161/5173/5101.
- No `pkill -f` / `killall`. Never touch `/Users/davidcruwys/dev/video-projects/`, `~/.config/appydave/`
  (read-only is fine), `~/.claude/`.
- fli-core changes are findings, not edits.
- Park, with a reason, anything that fails its gate after 3 attempts.

## Done when

Branch pushed, every gate passing, extraction plan written. Report to flivideo-orch: head, gate numbers,
the new host shape in ~10 lines, the extraction recommendation, and anything you parked.
