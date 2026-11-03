---
created: 2026-11-03
timestamp: 2026-11-03T21:00+07:00
---
# Brief: Show chips — leading dot inset (2026-11-03)

**From:** `flivideo-orch`. **To:** `chip-dot-dev` (**M2**). **Go:** David via `flivideo-roamy`, ~20:55.
**Machine: M2** — code, standing ruling; no other FliStudio client work in progress on the M4.

On the **filled** "Needs attention" chip the red dot touches the chip's left edge. Give a leading dot the same left inset the
text has on the other chips. Check every chip that carries a leading dot, filled and outlined, and hover/⊕/⊖ states (the ⊕/⊖ slot
from `1d5ef8b` must not shift). CSS only: `client/src/styles/status.css` (and `StatusList.tsx` only if markup must change).

Worktree off origin/main (`1d5ef8b` or later): `git -C ~/dev/ad/flivideo/flistudio fetch origin && git -C ~/dev/ad/flivideo/flistudio worktree add ~/dev/ad/flivideo/flistudio-worktrees/chip-dot-inset -b chip-dot-inset origin/main`; `npm install`; `npm run build -w extension-core` before vitest.

Gate: typecheck, client unit, and the FULL `e2e/project-status.spec.ts` (`npm run build` first). Push the branch; report sha +
tails; STOP. Orch re-gates on the M4, merges, restarts and screenshots the filled Needs-attention chip.
