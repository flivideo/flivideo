# Story Pilot W2.1 — Reader fixes: build report (2026-11-03)

**For**: `flivideo-orch` (re-gate on the M4, merge, restart). **From**: the W2.1 build session on the M2.
**Brief**: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/storypilot-w2-1-reader-fixes-2026-11-03.md`.
**Status**: pushed and stopped. Nothing merged or restarted.

Branch `storypilot-w2-1` at **`c968ec7`**, one commit on main `c827c92`.
Worktree: `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/storypilot-w2-1`.

## The three defects

| # | What the d13 screenshot showed | Cause | Fix |
|---|---|---|---|
| 1 | Spec "File" row: label + `>_` only | The kit's `Here` draws icons, never the path text | The row prints the stored path in full, with the path icons; "not on this machine" (red) when the file isn't here, never hidden. `story.source.read` gains `fileHere` (true / false / null when no file is named). |
| 2 | Bullets cut mid-sentence; `~~…~~` as literal tildes | `docParts` took 👤 quotes **line by line**, so a hard-wrapped bullet became two | Quotes are whole items now (a bullet with its wrapped lines, a paragraph, a table row). Markdown joins a wrapped list line with a space (a nested bullet keeps its own line) and renders `~~x~~` as `<s>`. |
| 3 | Open Send-to-session panel covered the Reader's tabs and M / L / × | W2 made it overlay | It opens in the page flow and pushes the Story Pilot area down (panels push, never overlay). |

## Tests (M2, shell set to `CAPTAINS_LOG_URL=https://example.invalid`, CL stub enforced)

| Suite | Before (`c827c92`) | After |
|---|---|---|
| storypilot | 296 | **302** ✓ |
| storypilot e2e | 5 ✓ · 11 skipped | **5 ✓** · 11 skipped (ran twice) |
| server | 759 ✓ · 4 ✗ | 759 ✓ · 4 ✗ (PIL) |
| overlay-pilot | 61 ✓ · 10 ✗ | 61 ✓ · 10 ✗ (PIL) |
| extension-core / broll-pilot / client | 55 / 53 / 335 | unchanged ✓ |
| Typecheck, lint, format, `api:check` | | clean; 173 methods |

The 14 failures fail on main too (no Python `PIL` on the M2). The 11 skips need the real d13/d18/d19 folders, so only
the M4 runs them.

New tests, one or more per defect:
- **File row:** a present file shows its full path with the icons; a missing one shows its stored path plus "not on
  this machine" (also in "Where it came from"); `fileHere` is true / false / null.
- **Bullets:** a hard-wrapped bullet stays one item and one sentence; a wrapped 👤 bullet is one quote; `~~x~~` renders
  as `<s>`.
- **Popover:** the e2e opens the Reader first, then the panel, and asserts its box never meets the Reader's tab bar and
  that the Story Pilot area moves below it. I checked it fails on the old CSS.

## Notes

1. **The d13 spec file exists on the M4.** Its stored path is absolute; the card's `overlay-pilot/spec.md` is only the
   last two path segments, and the Reader had already read the file (the take and quotes rendered from it). The row
   was empty because nothing printed the path. With W2.1 it shows in full, and "not on this machine" appears only
   where it really is missing.
2. **One old pin flipped on purpose:** a Markdown list item's wrapped line used to render as `<br>`; it is now a space,
   as Markdown treats a soft wrap. A nested bullet (4+ spaces) still keeps its own line.
