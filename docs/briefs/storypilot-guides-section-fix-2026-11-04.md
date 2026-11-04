---
created: 2026-11-04
timestamp: 2026-11-04T10:00+07:00
---
# Brief: Guides section — fix the 5 e2e failures the M4 gate found (2026-11-04)

**From:** `flivideo-orch`. **To:** `guides-fix-dev` (**M4**). Report to `flivideo-orch` and STOP.
**Machine: M4** — the failing look specs read d13/d18 real project data that exists only on the M4 (they skip on the M2), and
the gate is already in progress here. Fix in a worktree, never the live checkout.

## Setup
`git -C ~/dev/ad/flivideo/flistudio fetch origin && git -C ~/dev/ad/flivideo/flistudio worktree add ~/dev/ad/flivideo/flistudio-worktrees/guides-fix -b guides-section-3 origin/guides-section-2`; `npm install`; `npm run build` (needed before typecheck/unit in a fresh worktree).
Context: `docs/briefs/storypilot-guides-section-2026-11-04.md` (what the section is) — keep its design.

## Failures (orch gate on the M4, guides-section-2 @ f32db19)
1. `e2e/storypilot-look.spec.ts:103` ×4 (d13 + d18 at 2000 and 1440): `getByTestId('side-panel').getByTestId('sp-read')` not
   found — the Reader no longer opens in the side panel where the spec expects it. Find whether the spec's Read click now hits a
   **Guide** card's Read → (Guides sit above Sources) or whether Read stopped opening the Reader. **Behaviour rule:** a Guide's
   Read → and a Source's Read → must both open the same Reader in the side panel (`sp-read`). Fix the code if either doesn't;
   re-scope the spec's selector to Sources only if the code is right.
2. `e2e/storypilot-listen.spec.ts:340` (J/K/L keys): `locator('.sp-lane .sp-card').first()` expected `/is-reading/` — the first
   `.sp-lane .sp-card` is now presumably a Guide card. Guide cards must not be mistaken for source/script cards: give the Guides
   section its own lane/card classes (or a distinct container) so Listen's reading state and any `.sp-lane .sp-card` selectors
   only see what they did before. Don't weaken the Listen test.

## Gate
Typecheck + full unit, then the FULL storypilot e2e set + `project-status.spec.ts` on the M4 (all green; look specs must RUN,
not skip). Screenshots on the live-data d13 copy the look spec uses: Guides section with chip rows, Reader open on a guide.
Push branch `guides-section-3`; report sha, the cause of each failure, test counts, screenshot paths. STOP.
