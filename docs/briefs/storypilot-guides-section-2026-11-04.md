---
created: 2026-11-04
timestamp: 2026-11-04T10:35+07:00
---
# Brief: Guides as a Sources-style section above Sources, with the SHOW-chip filter as the standard (2026-11-04)

**From:** `flivideo-orch`. **To:** `guides-section-dev` (**M2**). Report to `flivideo-orch` and STOP.
**Go:** David, 2026-11-04 ~10:30. **Machine: M2** — code, standing ruling. Orch re-gates on the M4, merges, restarts.

## Why (David)
The Guides tab (merged 8eaaa19) "doesn't feel usable": a 5×4 grid, 13/20 cells empty dashed boxes, cards show only a label and
tool chips (Open, `>_`, change, ×, ⓘ), raw path inputs inline, so you can't see what a guide says. The Sources column next to it
"feels a lot cleaner". David wants to **see and read every guide on screen** before any script work today.

## Do
1. **Move Guides out of the rail.** No Guides tab. A **Guides section directly above Sources** in Story Pilot's main view, built
   like Sources (`modules/storypilot/client/` — find the Sources cards and copy their structure and CSS, don't invent new):
   - one card per guide: number, type chip (verbal / voice / structure / lens / other), level chip (global / brand /
     video project / video), title, **a one-line summary of what the guide says**, the pointer in mono, and **Read →** that opens
     the guide in the **same Reader** Sources use (read the pointed file at view time; never store its text in Story Pilot);
   - summary: the file's own Purpose line / first heading paragraph, read at view time; if none, the first ~160 chars.
     Stamp nothing, write nothing into the guide files;
   - management (change pointer, remove, add) behind a quiet "edit" affordance on the card, not always-visible chips;
   - **missing slots collapse** to one quiet line per level ("Missing: brand voice · brand lens · story structure"), each
     clickable to add a pointer.
2. **Filter = the Projects SHOW-chip control, made the standard.** Reuse the filter in `client/src/screens/StatusList.tsx`
   (filled = shown, outline = hidden, name-click solos, ⊕ adds, ⊖ removes, ⌘-click adds, persistence) — **extract it into a
   shared FliStudio component** (e.g. `client/src/components/FilterChips.tsx`) that both Projects and Story Pilot use, with
   Projects' behaviour and its e2e unchanged. Two chip rows over Guides: **Level** (Global · Brand · Video project · Video) and
   **Type** (Verbal · Voice · Structure · Lens · Other). Persist per brand like Projects does.
   Write the rule in `flistudio/CLAUDE.md`: "Filtering uses the shared FilterChips control (Projects SHOW pattern); don't build
   new filter UIs." (Moving it to fli-core's shared UI layer is a follow-on, after the help-system package choice lands.)
3. Remove the Guides tab and its rail entry; keep the verbs (`story.guides.list/set`, `story.brief` guides) unchanged.
4. Tests: re-point `e2e/storypilot-guides.spec.ts` to the section (cards render with summary, Read → opens the Reader with the
   file's text, filter solo/add/remove, missing line, add a pointer); `e2e/project-status.spec.ts` must pass unchanged in full;
   rail/look specs updated for the tab's removal. Unit for summary extraction.

## Setup / parallel
`git -C ~/dev/ad/flivideo/flistudio fetch origin && git -C ~/dev/ad/flivideo/flistudio worktree add ~/dev/ad/flivideo/flistudio-worktrees/guides-section -b guides-section origin/main`; `npm install`; `npm run build -w extension-core` before vitest.
Parallel: `direction-box-dev` (Direction box at the top of the Script section, Rerun label, `story.brief.direction`) and
`help-system-dev` (Prep.tsx / Listen.tsx, tooltips). Keep out of their files; if you must touch `StoryPilot.tsx`, keep the diff small.

## Gate / report
Typecheck, full unit, the FULL storypilot e2e specs + `project-status.spec.ts` (`npm run build` first). Screenshots on the
d13 project: the Guides section with both chip rows, one filter solo, the Reader open on VERBAL-STYLE, the missing line.
Push branch `guides-section`; report sha, test counts before → after, screenshot paths.
