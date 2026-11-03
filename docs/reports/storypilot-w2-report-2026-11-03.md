# Story Pilot W2 — the Reader: build report (2026-11-03)

**For**: `flivideo-orch` (re-gate on the M4, merge, restart, d13 screenshots). **From**: the W2 build session on the M2.
**Brief**: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/storypilot-w2-reader-ui-2026-11-03.md`.
**Status**: pushed and stopped. Nothing merged or restarted.

W2 is pushed as `storypilot-w2` at `c827c92`, one commit on main `188a202`.
Worktree: `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/storypilot-w2`.

## Tests on the M2 (shell set to `CAPTAINS_LOG_URL=https://example.invalid` throughout)

| Check | Before (`188a202`) | After |
|---|---|---|
| storypilot | 280 | **296** ✓ |
| storypilot e2e | 3 ✓ · 11 skipped | **5 ✓** · 11 skipped (ran twice in the full set) |
| server | 759 ✓ · 4 ✗ | 759 ✓ · 4 ✗ (PIL) |
| overlay-pilot | 61 ✓ · 10 ✗ | 61 ✓ · 10 ✗ (PIL) |
| extension-core / broll-pilot / client | 55 / 53 / 335 | unchanged ✓ |
| Typecheck, lint, format, `api:check` | | clean; 173 methods |

The 14 failures fail on main too, because the M2 has no Python `PIL`. The 11 skips need the real d13/d18/d19 folders,
so only the M4 runs them.

## What changed, by brief section

- **A · Badges:** each island shows its nature (plus `CAPTAIN'S LOG · B663` for captures) and one way out. That's
  "Open in Captain's Log ↗", "Open ↗" for a URL, or "File" with an always-visible copy-path icon. "Where it came from"
  lists home, machine, path or code, where the words were read from (extract date and machine, and whether the
  transcript changed since), and who attached it and when.
- **B · Captain's Log:** the live strip sits under our title and why. When offline it's one quiet line, shown once.
- **C · Sessions:** they read as a conversation. The header reads "Claude Code session · purpose · date · name ·
  machine". David's turns are in full, with images as a chip. Claude's replies fold to "Claude replied: N words · show"
  and open in place. "Showing 30 of 47 turns · show more" pages through the rest, so nothing is cut silently.
- **D · Spec / doc:** the one-line take and David's 👤 lines come first. The header card and body are folded behind
  "the whole document". Documents now come back whole, which flips W0's KNOWN GAP (W2) pin.
- **E · Send to session:** a compact pill at the top of Story Pilot, with its panel opening over the page. It's still
  off unless `FLISTUDIO_SEND_TO_SESSION=1`. The e2e answers its routes inside the browser, so nothing types into a real
  tmux session.

## Notes and things the brief didn't cover

1. **Folding Claude's turns needed Claude's text in the extract.** W1's extract held David's turns only. It now includes
   Claude's text replies (never tool calls, results, thinking or sidechains) and image counts. The Python twin changed
   too, and the parity test passes. **The d13 extracts made with W1 have no replies.** Re-run them on the M4 after merge
   (and Roamy's d14/d19 ones), or the chat view says "Claude's side is not in this extract".
2. **New API fields:** `story.source.read` takes `turnFrom` / `turnCount` and returns `raw.chat` and `raw.extract`. The
   extract schema stays `/1`, with `replies` optional.
3. **Subagent messages are now skipped.** Messages Claude Code marks as sidechains are left out of David's turns as well
   as Claude's replies.
4. **Cards and the Reader can disagree for new captures.** The source list never calls Captain's Log (W1 design), so a
   capture with no `meta.channel` shows "Captain's Log capture · Raw?" on its card and "Plaud recording · Raw" only in
   the Reader. Fixing it means the brief calling Captain's Log: about one call per capture, cached.
5. **"Purpose" only shows if `meta.purpose` is set,** and no existing session has it.
6. **`HostKit.Here` gained an optional `always`,** passed through by the host. Without it the File icon only appeared on
   hover.
7. **One e2e was flaky while I built it, now fixed.** It measured in viewport coordinates and before the page's fonts
   had settled. Six repeat runs since all pass.
8. **Fixture screenshots** of the four states are at
   `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/storypilot-w2/test-results/reader/`. They're for my own
   check; orch's d13 screenshots are the real record.
