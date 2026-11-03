---
created: 2026-11-03
timestamp: 2026-11-03T20:25+07:00
---
# Brief: Projects SHOW chips — filled/outline + ⊕/⊖, drop the hint and ✓ (2026-11-03)

**From:** `flivideo-orch`. **To:** `show-filter-dev` (**M2**). **Go:** David via `flivideo-roamy`, ~20:20.
**Machine: M2** — code, standing ruling. **Start after** your `lastwork-fallback` unit is pushed; branch this off that branch
(or rebase onto main once orch merges it). Branch: `show-chips-redesign`. FliStudio client only: `client/src/screens/StatusList.tsx` + its CSS.

## Why
David rejected the look in `7df0913`: the grey hint "Click = just this one · ⌘-click = add more" is lost at the end of the row,
and hidden chips drawn with strikethrough + dashed border read as deleted/abandoned.

## New design
1. **Filled chip = shown** (brand brown `#342d2d` fill, cream `#faf5ec` text). **Outline chip = hidden** (1px hairline
   `--brand-border`, brown text). No strikethrough, no dashed border for hidden — **except the Abandoned chip's own label**,
   which keeps its strikethrough (that is its meaning). "All" follows the same filled/outline rule.
2. Hover or focus an **outlined** chip → a small **⊕** button at its right edge (`aria-label="Add <status>"`); clicking ⊕ adds
   that status to what's shown. Clicking the chip **name** = just this one (unchanged). On a **filled** chip when 2+ are shown,
   hover/focus shows **⊖** (`aria-label="Remove <status>"`) to remove it. Keyboard-reachable (Tab to the chip, the ⊕/⊖ is
   focusable; Enter/Space activate).
3. ⌘/Ctrl-click keeps working as a shortcut, unchanged.
4. **Delete** the hint line. **Remove** the ✓ badge (fill carries "shown").
5. Behaviour and persistence (localStorage per brand, `?show=`) unchanged.

## Gate (yours)
Unit + typecheck; the **FULL** `e2e/project-status.spec.ts` (`npm run build` first), updated for ⊕/⊖: add via ⊕, remove via ⊖,
name-click solos, ⌘-click still adds, persistence across a new browser context still passes; full unit suite green (PIL-only
failures on the M2 noted, not fixed). Push the branch; report sha + tails. Orch re-gates on the M4, merges ff-only, restarts, and
screenshots (a) one shown + hover on an outlined chip with ⊕ visible, (b) two shown.
