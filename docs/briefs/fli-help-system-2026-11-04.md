# Brief: one help system for the Fli apps (key hints out of the page)

**Purpose**: Build brief. Replace inline key-hint text ("J slower · K 1x · L faster") with one shared help system, lifted
from FliCut, used across FliStudio.

**For Agents**: Owner `flivideo-orch`; build on the **M2** in a worktree, re-gate and merge on the M4, restart via
`my-app`. From `flivideo-roamy`. **Go: David, 2026-11-04** ("KEY HINTS → ONE HELP SYSTEM (GO)"). No further David
decisions needed.

## Why (the recurring mistake)

FliCut has had a four-layer help system since 2026-09-24 (`flicut/src/renderer/src/Help.tsx`): a tooltip on every
control (what it does and its key), a key strip for the current context, a **?** cheat sheet, and "how FliCut works".
FliStudio never got it. Each new FliStudio screen copied the nearest example, which was inline text:
`client/src/components/Viewer.tsx:394`, `modules/storypilot/client/Prep.tsx:233`,
`modules/storypilot/client/Listen.tsx:453`. A one-off fix on 2026-11-03 (`5b9324e`) moved one hint into a tooltip but
left no shared component and no rule, so it came back. David has now flagged this several times.

**One-line reason for David:** inline hints take space on every screen forever and teach nothing after the first day.
In a tooltip and the ? sheet they are there when you look for them, gone when you don't, and the same in every app.

## Do

1. **Shared help.** Lift FliCut's `Help.tsx` model into shared code: the key data per context, tooltip text with the
   key, the ? cheat sheet overlay (searchable, grouped by job), and an optional key strip.
   - ⚠️ `@flivideo/core` (`fli-core`) has **no React today** (no `.tsx`, no react dependency). Choose and report: a
     `@flivideo/core/ui` subpath with react as a peer dependency, or a sibling package. Keep the key data
     (framework-free) in core whichever you choose.
   - FliCut keeps working unchanged. Switching FliCut to the shared copy is a follow-on; do it only if it's cheap and
     its tests stay green.
2. **FliStudio uses it.** Viewer, Story Pilot Prep and Story Pilot Listen:
   - remove the inline key-hint text;
   - put the keys in each control's tooltip (`title` plus `aria-label`, as `5b9324e` did);
   - add a **?** key and a small ? button that opens the cheat sheet for the current screen.
   - Sweep FliStudio for any other inline key hints and treat them the same way; list them in the report.
3. **Tests.** The existing tests assert the hint text (`client/src/components/Viewer.test.tsx:195,231`,
   `modules/storypilot/client/screen.test.ts:908`). Re-point them to where the keys now live (tooltip / aria-label / ?
   sheet). **Do NOT add a "no inline key-hint text" guard test.** Whether that becomes a test or a static-analysis rule
   is a separate investigation (`docs/research/ui-rule-test-vs-static-analysis-2026-11-04.md`).
4. **Write the rule where builders read it:**
   - `appydave-plugins/brand-dave/skills/brand/SKILL.md`, AppyDave key rules (app surfaces): "Keyboard shortcuts live
     in tooltips and the ? cheat sheet, never as inline text beside a control." Bump the brand-dave plugin version.
   - `flivideo/flistudio/CLAUDE.md`: the same rule, plus where the shared help lives.

## Out of scope

The speed control's look (mocks first, separate job); the guard test or lint rule; FliHub; Teletubby.

## Gate and report

Unit + typecheck; the e2e specs for the screens touched (Viewer, Story Pilot reader / Listen / Prep), run in full; every
other suite green. Screenshots: Listen and Viewer without the inline text, one tooltip showing a key, and the ? sheet
open. Report to `flivideo-orch` with commits, test counts, the package choice, and the swept list.
