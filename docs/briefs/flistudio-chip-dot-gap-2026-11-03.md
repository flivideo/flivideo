---
created: 2026-11-03
timestamp: 2026-11-03T20:50+07:00
---
# Brief: Show chips — tighten the dot-to-label gap (2026-11-03)

**From:** `flivideo-orch`. **To:** `chip-gap-dev` (**M2**, code, standing ruling). **Go:** flivideo-roamy for David, ~20:48.

After `35225b5` the leading dot is inset correctly, but the gap between the dot and the label ("Needs attention") is about 3× the
dot's left inset, so the chip looks padded (`/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-03/chip-dot-inset.png`).
Set the dot→label gap equal to the dot's left inset (≈ the other chips' text inset) so the chip is no wider than it needs to be.
Filled and outlined; ⊕/⊖ slot must not shift. CSS only (`client/src/styles/status.css`).

Worktree off origin/main: `git -C ~/dev/ad/flivideo/flistudio fetch origin && git -C ~/dev/ad/flivideo/flistudio worktree add ~/dev/ad/flivideo/flistudio-worktrees/chip-dot-gap -b chip-dot-gap origin/main`; `npm install`; `npm run build -w extension-core`.
Gate: typecheck, client unit, FULL `e2e/project-status.spec.ts` (`npm run build` first). Push the branch, report sha + tails, STOP.
