---
created: 2026-11-02
timestamp: 2026-11-02T13:15+07:00
---
# Brief: FliHub's purple B-roll button calls B-Roll Pilot's `broll.register` (2026-11-02)

**From:** `flivideo-orch` (Swagger). **To:** `flihub-broll-dev`. Report to `flivideo-orch` by name.
**Go:** David, 2026-11-02, decision 3 of the 11-02 report: "YES".

## Read first
- The contract: `/Users/davidcruwys/dev/ad/flivideo/flistudio/docs/planning/broll-pilot/spec.md` §6 (6.1 the call,
  6.2 rules, 6.3 what each button does, 6.4 refusals). The server side is live: `modules/broll-pilot/server/register.ts`
  in `/Users/davidcruwys/dev/ad/flivideo/flistudio` (read-only for you).
- FliHub's current button: `client/src/components/FileCard.tsx` (`handleBroll`, ~line 149; the purple "B-roll" button ~line 325,
  FR-161 — moves the take to `b-roll/`). Also `client/src/hooks/useBrollApi.ts`, `client/src/components/BRollPage.tsx`.
- FliHub's own `CLAUDE.md` / `AGENTS.md` and FR conventions (`docs/prd/`).

## The job
- The button registers the take with B-Roll Pilot through `broll.register` (FliStudio control channel, port 7151, see §6.1
  for transport + auth; never print the token), per §6.3: the take, its project, tags typed at the button.
- Handle every §6.4 refusal with a clear toast; when FliStudio is down, say so and do not lose the take.
- Decide (and state in your report) what happens to the old FR-161 move-to-`b-roll/` behaviour — §6.3 and the
  2026-09-22 ruling that FliHub `b-roll/` is deprecated are your guides. Recommend; flag before deleting behaviour.
- Write it up as a FliHub FR in `docs/prd/` (next free FR number — look it up).

## Where you work
- Worktree `/Users/davidcruwys/dev/ad/flivideo/flihub-worktrees/broll-register`, branch `broll-register` (from main 061ae34).
  **Never edit the live checkout** `/Users/davidcruwys/dev/ad/flivideo/flihub`, never FliStudio's repo.
- Run your branch on non-live ports. Prove it end to end against live FliStudio's `broll.register` with a **test project**
  (not a real video's resources), then show the registered item in B-Roll Pilot in a real browser: screenshot to
  `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-02/`.
- Gates: typecheck, lint, `npm test`, targeted tests only. Do not run any full e2e suite (machine is overloaded).

## Limits
- Do not merge, do not restart FliHub or FliStudio. Orch gates and merges.
- Do not change B-Roll Pilot or the §6 contract; if it is wrong, STOP and tell orch with a recommendation.
- Report: branch + commit, FR number, the old-button decision, proof paths, what you could not verify.
