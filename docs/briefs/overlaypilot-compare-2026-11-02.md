---
created: 2026-11-02
timestamp: 2026-11-02T09:55+07:00
---
# Brief: Overlay Pilot — synchronized side-by-side comparison (2026-11-02)

**From:** `flivideo-orch`. **To:** `overlaypilot-dev`. **Report to `flivideo-orch` by name, then idle until acked.**
**Worktree:** create `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/op-compare`, branch `op-compare`, from main `3f6804e`.
Lane: `modules/overlay-pilot/**` only. Do not touch storypilot or broll-pilot.
**Source (read the named sections in full):** Captain's Log B682 (David's voice log, 2026-11-02 06:33) and its dossier B683, on disk at `/Users/davidcruwys/dev/ad/flivideo/docs/specs/b683-dossier-2026-11-02.md`. Fetch either with the captains-log MCP `capture_get` if you need David's exact words. Section 8 (esp. 8.2, 8.3).

**Why:** David's demo for the Overlay Pilot video: pick 2–3 looks, generate, then show the renders side by side. Also a real feature.

## Build
- Select 2–4 renders of the same source → **Compare** button opens them side by side (no modal dialog if avoidable; David
  dislikes pop-up modals for review views. A full-width in-page view is fine).
- **Group play**: one play/pause/seek drives all, kept in sync.
- **One voice**: only the first (or chosen) video has audio; others muted. Click a video to make it the voice.
- **Mute all** toggle, independent of which one is the voice.
- **Keep this one**: mark the preferred render as the chosen look (use the module's existing "chosen/keep" concept if one exists).
- Find the existing name for "look" (David: "it's a look and feel… it'll be in the application").

## Gates
typecheck, lint, `npm test`, targeted overlay-pilot e2e only. UX pass. Screenshots at 2000 and 1440. Commit, push. Do not merge or restart.

---

## Handover — window closed 2026-11-02 (flivideo-orch)

**State:** Compare shipped. Branch `op-compare` (b245736) merged to FliStudio main at 466be52; restarted and healthy.
The e2e flake was pre-existing (a clean 3f6804e failed the v2 test 4/6): the screen lags the disk by seconds; the expect at
`e2e` line ~365 now waits 30 s (test-only change). v2 test 8/8 alone, both overlay-pilot tests 2/2 together.
Temporary worktree `flistudio-worktrees/op-base` removed. Window `overlaypilot-dev` closed by orch on David's ruling (idle).

**Next unit (not started — waits on David):** demo support for the Overlay Pilot video. David records the demo in FliHub
(pick 2–3 looks → generate → Compare side by side → Keep this one); that recording becomes a B-roll asset and the demo is
woven into D13's script (B682/B683 §8.2–8.3). Open questions to re-check when it restarts:
- Compare sync on a long render has not been checked (only short test renders).
- Compare has not been viewed by David in a real browser.

**To resume:** launch a fresh `overlaypilot-dev` from a worktree off current main (never the live checkout), read this brief
and the D13 project (`/Users/davidcruwys/dev/video-projects/v-appydave/d13-overlay-pilot/`), then ask orch for the unit.
