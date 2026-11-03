---
created: 2026-11-03
timestamp: 2026-11-03T18:30+07:00
---
# Brief: FliStudio Projects "Show" filter — remember it for real, and make ⌘-click discoverable (2026-11-03)

**From:** `flivideo-orch` (Swagger). **To:** `show-filter-dev` (**M2**, cwd `/Users/davidcruwys/dev/ad/flivideo`). Report to `flivideo-orch`.
**Go:** David via `flivideo-roamy`, ~18:25. **Third report of this bug — full gate.**
**Machine: M2** — standing ruling: code changes run on the M2 by default; no FliStudio work is in progress on the M4.

## Context
- Commits `faff662` (click solos, ⌘-click adds) and `5beb2fd` (`?show=` URL + sessionStorage per brand).
- `client/src/screens/StatusList.tsx` (~:46–60 state init + `setHidden`; ~:101–102 chip click) and
  `client/src/screens/statusModel.ts` (`CATEGORIES`, `decodeShow`/`encodeShow`, `DEFAULT_HIDDEN`).
- Why 5beb2fd passed while the bug survived: its e2e only reloaded the same tab; sessionStorage is per-tab and dies with
  the tab, so a new tab, a deck link or a browser restart lose it.

## Setup (M2, never the live checkout)
`git -C ~/dev/ad/flivideo/flistudio fetch origin && git -C ~/dev/ad/flivideo/flistudio worktree add ~/dev/ad/flivideo/flistudio-worktrees/show-filter-persist -b show-filter-persist origin/main`
(the M2's flistudio checkout is far behind origin; branch from `origin/main`). `npm install` in the worktree.

## Do
(a) **Persistence:** store per brand in **localStorage** (key `fs.show.<brand>`), keep `?show=`. Precedence: URL wins →
localStorage → default. Writes keep using `replaceState`. Optional: read an old sessionStorage value once as a migration, then
drop it.
(b) **Discoverability — keep the behaviour exactly** (click solos, ⌘/Ctrl-click adds/removes):
- a permanent one-line hint under the chips: **"Click = just this one · ⌘-click = add more"** — small, brand-quiet (muted
  colour, body font, no box);
- when **more than one** status chip is selected, each selected chip shows a **✓**. One selected → no ✓.
- No mode switch, no checkboxes.

## Gate (yours, on the M2)
- Unit tests for precedence (URL > localStorage > default) and for the ✓ rule (0/1/2+ selected).
- **e2e that proves persistence across a new browser context**: pick two chips in page A, then open a **new page / new context
  sharing the same storage state** (or close and reopen) at the brand URL **with no `?show=`** and assert the same two are
  selected; also assert `?show=` overrides storage. Run only the targeted spec(s), never the full e2e suite.
- `npm run typecheck`, `npm test`, the targeted e2e — all green. Commit on `show-filter-persist`, **push the branch** to origin.
  Do not merge, do not restart anything.
- STOP and report to `flivideo-orch`: branch + sha(s), diff stat, unit/typecheck/e2e tails (with the e2e test name that covers the
  new context). Orch reproduces on the M4, merges, restarts and takes the screenshot.

## Limits
FliStudio client only (plus tests). Don't touch server, fli-core, or video projects. Keep the M2 light (no renders).
