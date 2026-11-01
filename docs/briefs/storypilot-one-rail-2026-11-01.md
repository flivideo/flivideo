# Brief: Story Pilot — one elastic right rail (FliHub look), reader folded in, section note targets — 2026-11-01

**From:** `flivideo-orch`. **To:** `storypilot-dev` (tmux), worktree
`/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/rail-v2` (branch `rail-v2`, from origin/main `367f10c`, `npm ci`
done). **Go:** David, 2026-11-01 ~09:30 +07, in the orch window. Report to `flivideo-orch` (SendMessage).
Questions → orch with a recommendation; never wait on David.

## Read first
- Reference images:
  - `/private/tmp/claude-501/-Users-davidcruwys-dev-ad-brains/7c6a3726-4270-4e8f-bcf3-baf10a76b63c/scratchpad/flihub-tabs-ref.png`: FliHub's tabs, the look David wants.
  - `/private/tmp/claude-501/-Users-davidcruwys-dev-ad-brains/7c6a3726-4270-4e8f-bcf3-baf10a76b63c/scratchpad/storypilot-two-systems.png`: today's Story Pilot, with two slide-out systems.
- FliHub tab code, for the look only (read-only):
  - `/Users/davidcruwys/dev/ad/flivideo/flihub/client/src/components/ChapterPanel.tsx`
  - `DamHelpPanel.tsx`
  - `ChapterHelpPanel.tsx`
  - their CSS
- Current code in `modules/storypilot/client/`:
  - `SideRail.tsx`
  - `StoryPanels.tsx`
  - `Lab.tsx`
  - `ScriptText.tsx`
  - the main Story Pilot page: it has an inner source reader with MEDIUM/LARGE and a vertical CLOSE tab, and the script's Width S/M/L.
- Fire `appystack:appystack-conventions` first. Typecheck needs the workspaces built: `npm run build -w shared` alone fails on `@flivideo/broll-pilot/contracts`, so build the modules too.

## David's verdict on today's build (his words)
> "Medium and large don't do anything… These tabs over on the right don't look correct, and they don't look the way
> we did in FliHub… this is a fixed-frame window, and it's meant to be an expanding window, like a dynamic or elastic
> one… settings… should take up space and push the main content window to the left… Instead, it's just fixed."
>
> "It's like we've built two slide-out systems: one from the outer area, where you put settings, and another inner one
> for the reading pane. But the reading pane probably needs to sit in the same place that settings do… Consistency,
> please. One control has just large and medium. The other one has small, medium, large, and they don't even look the
> same." On the script width control: "Just get rid of it for now. It's not adding value."

## Build
1. **One rail, FliHub look.** The tabs are attached flush to the window's right edge, with vertical labels, rounded on the outer side only. They are not floating cards inside the page.
2. **Elastic push.** Opening a panel takes real width from the right; the main content column visibly narrows and shifts left. It never overlays, and it never just fills empty space: the "use empty space first" rule from this morning is reversed. Closing restores the layout. Animate it smoothly.
3. **M / L that work.** Use one size-control component everywhere: M ≈ 420px, L ≈ 640px, or whatever reads well. Changing the size visibly changes the panel width and pushes the content further.
4. **Fold the inner reader into the rail.** The source reader becomes a **Reader** panel on the same rail. Clicking a source card or node opens and pins it. Remove the inner reader pane, its CLOSE tab and its MEDIUM/LARGE control. The story section keeps its timeline and source columns.
5. **Remove the Width S/M/L control** from both the main Story Pilot script and the Lab. Lab B/C/D stay, and so do the dark/light and terminal toggles.
6. **Panels:** Settings, Sources, Chapters and Reader, on the main page and in the Lab. The Lab may omit Reader.
7. **⌘⇧ note gesture, section-level targets.** Give note targets to the Story card, the Script card, each panel and the rail. Clicking a card's own padding or empty area targets the card; the innermost target still wins. Use plain labels, e.g. "Story Pilot · Script section".
8. Keep every edit control and behaviour, the white-card + hairline style, and light-only.

## Rules
- Own ports only: never 7150/7151/7111/7121/7161/5173/5101.
- Fixture projects only: never write to `/Users/davidcruwys/dev/video-projects/`.
- No merge to main, no app restarts, no pkill.

## Done when
- e2e checks:
  - tabs are flush to the viewport's right edge (±2px);
  - opening Settings narrows/shifts the main content box, with no intersection;
  - M→L widens the panel and narrows the content;
  - clicking a source opens Reader in the rail, and there is no inner reader;
  - there is no Width S/M/L;
  - a ⌘⇧-click on the Script card padding opens a note labelled "Script section".
- Gates pass: format:check, typecheck, lint, test, api:check, test:e2e.
- Commit on `rail-v2` with the Claudia + Claude Opus 5.5 co-author trailers, then `git push -u origin rail-v2`.
- Screenshots in `test-results/rail/`:
  - main page closed;
  - Settings at M;
  - Settings at L;
  - Reader open;
  - Lab with Chapters open;
  - the Script-section note box.
- Report to `flivideo-orch` with the sha, one line per gate, screenshot paths, taste calls, and anything not done.
