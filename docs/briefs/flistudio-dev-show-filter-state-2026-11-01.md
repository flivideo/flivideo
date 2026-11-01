---
created: 2026-11-01
timestamp: 2026-11-01T13:25+07:00
---
# Brief: FliStudio unit 7: the Projects "Show" filter keeps its state (2026-11-01)

**From:** `flivideo-orch`. **To:** `flistudio-dev` (tmux `flistudio-dev`). **Report to `flivideo-orch` by name, then stay idle until acked.**
**Worktree:** `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/studio-dev`, branch `studio-dev-2`, from main `68dffc0`.

## David's words, verbatim

"We constantly lose state on the show buttons at the top… I tend to, every now and then, come back, and they're all
changed around now… I just did a back arrow, and you don't remember from page to page."

## Ruling (reverses this morning's "don't persist")

- The Show filter selection lives in the **URL query string** (so the browser back arrow restores it), with
  **sessionStorage** as the fallback when you arrive at the Projects page without a query (e.g. from the menu).
- Click solos / ⌘-click adds / All: unchanged. **★ rows (worked on today) still always show**, whatever the filter.
- Use `replaceState`-style updates for chip clicks if pushing a history entry per click would make "back" step
  through filter changes; the requirement is: Projects → open a project → back = same filter. Name your choice.
- Code: the Show filter added in `faff662` (client/src/screens, `statusModel.ts` and the Projects/status screen).

## Gates (machine is overloaded: targeted e2e only)

- typecheck, lint, `npm test`.
- e2e, targeted: a new test that sets a filter (solo + one ⌘-click add), opens a project, presses back, and asserts
  the same chips are on; plus one that reloads the page and asserts the filter survives via the URL. Run only that
  spec and `project-status.spec.ts`. Do **not** run the full suite.
- Commit, push `studio-dev-2`. Do not merge. Report, then idle.
