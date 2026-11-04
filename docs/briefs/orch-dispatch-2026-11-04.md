---
created: 2026-11-04
timestamp: 2026-11-04T08:00+07:00
---
# Orch dispatch 2026-11-04 — setup + gate for the four 11-04 briefs

**From:** `flivideo-orch` (M4). Read your brief first, then your section here. **Machine: M2** for all three (code + unwatched
write-ups — standing ruling). Report to `flivideo-orch` and STOP; orch re-gates on the M4, merges, restarts.
**Never work in a live checkout** (`~/dev/ad/flivideo/flistudio`, `fli-core`, `flicut`): use the worktree named below.
Fresh FliStudio worktree: `npm install`, then `npm run build -w extension-core` before vitest. M2 known gaps: PIL-only
overlay-pilot render failures and the d13/d18 look specs skip — note them, don't fix them.

## help-system-dev — `docs/briefs/fli-help-system-2026-11-04.md`
- `git -C ~/dev/ad/flivideo/flistudio fetch origin && git -C ~/dev/ad/flivideo/flistudio worktree add ~/dev/ad/flivideo/flistudio-worktrees/help-system -b help-system origin/main`
- If you put code in fli-core: `git -C ~/dev/ad/flivideo/fli-core worktree add ~/dev/ad/flivideo/fli-core-worktrees/help-system -b help-system origin/main`;
  tag nothing — push the branch; point FliStudio at it with a `github:flivideo/fli-core#<sha>` ref on your branch and say so
  (orch tags the release at merge).
- Parallel: `guide-slots-dev` is adding a Guides tab to Story Pilot's rail and verbs in `modules/storypilot/server`. Keep
  your storypilot diff to Prep.tsx / Listen.tsx / their tests.
- appydave-plugins: `git pull` first; commit only the brand SKILL.md + brand-dave plugin.json; push.
- Push branch `help-system`; report: shas (flistudio, fli-core if any, appydave-plugins), package choice, swept list, test
  counts before → after, e2e spec names + pass counts, screenshot paths.

## guide-slots-dev — `docs/briefs/storypilot-guide-slots-2026-11-04.md`
- `git -C ~/dev/ad/flivideo/flistudio fetch origin && git -C ~/dev/ad/flivideo/flistudio worktree add ~/dev/ad/flivideo/flistudio-worktrees/guide-slots -b guide-slots origin/main`
- The seed pointers are checked on the **M4** (`ssh davidcruwys@100.82.235.39 'ls -la <path>'`) — read-only. Write the
  seed as data/code in your branch; do NOT write `guides.json` into any live brand/project folder on either machine
  (orch seeds on the M4 after merge, via the verb). Tests use temp dirs only.
- Parallel: `help-system-dev` edits Prep.tsx / Listen.tsx. Don't touch those.
- Regenerate `api/openrpc.json` (`npm run api:openrpc`); update the registry snapshot / extensions tests the new verbs hit.
- Push branch `guide-slots`; report: sha, the seeded list with any pointer missing on the M4, the exact JSON-RPC calls for
  list and set, test counts before → after, e2e spec names + pass counts, screenshot path (use a temp/copy brand root).

## writeups-rsch — `docs/briefs/writeups-speed-mocks-and-investigations-2026-11-04.md`
- cwd `~/dev/ad/flivideo` (docs only; `git pull` before each commit). No code, no worktree needed.
- M4 files are read via `ssh davidcruwys@100.82.235.39 'cat …'`. Transcript search: M2 locally, M4 over ssh; Roamy is
  offline — say so. Keep the M2 light (no bulk copies of transcripts; grep in place).
- If claude-artifacts isn't available, commit the HTML and say "needs publishing". The `brains/ARTIFACTS.md` row: orch adds
  it when it publishes.
- Report: artifact URL or "needs publishing", the commits, one line per write-up with its recommendation.
