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
