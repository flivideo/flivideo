---
created: 2026-11-02
timestamp: 2026-11-02T13:00+07:00
---
# Brief: Story Pilot key bugs David found in the real app (2026-11-02)

**From:** `flivideo-orch` (Swagger). **To:** `storypilot-dev`. Report to `flivideo-orch` by name.

## The bugs (David, live FliStudio, after 84f3d43 was merged)

1. **Listen keys:** only Space works. **J** (slower), **K** (1x) and **L** (faster) do nothing.
2. **Reader `[` / `]`:** the reader steps from document to document, but the **document cards do not scroll or highlight**
   to follow the current document.

Orch's earlier report claimed both as shipped on e2e alone, without a real-browser check. That was wrong; this
time the bar is a real browser.

## Done means

- Root cause named for each (e.g. focus target, key handler scope, event swallowed by an input, `jkl` wiring in
  `@flivideo/extension-core`). Do not guess: reproduce first in a real browser.
- Fix on a fresh branch from current main (`c2719c4` or later) in your worktree, never the live checkout
  `/Users/davidcruwys/dev/ad/flivideo/flistudio`.
- **Proof stage 1 (yours, before reporting):** your branch on non-live ports, driven in a real browser
  (Claude in Chrome or headed Playwright). For each bug: a screenshot or GIF showing the key press and the result
  (speed readout changing for J/K/L; the active card scrolled into view and highlighted for `[` / `]`).
  Save under `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-02/`.
- Gates: typecheck, `npm test`, targeted e2e only (storypilot specs). Add an e2e that presses J/K/L and `[`/`]`
  with focus where a real user's focus would be (on the page body after clicking a card), not a synthetic focus.
- Report to orch: branch + commit, root causes, proof file paths. Orch gates, merges, restarts.
- **Proof stage 2 (after orch merges and says go):** open live FliStudio `http://localhost:7150` in a real browser,
  repeat both checks, save the screenshots/GIF to the same folder, report the paths. Read-only on live: no edits.

## Limits

- Story Pilot module and, only if the root cause lives there, `@flivideo/extension-core` keys (flag first —
  shared contract). Nothing else.
- Do not merge, do not restart FliStudio. Do not run the full e2e suite (machine is overloaded).
- Questions to `flivideo-orch` with a recommendation.
