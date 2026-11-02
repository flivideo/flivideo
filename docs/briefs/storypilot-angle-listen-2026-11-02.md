---
created: 2026-11-02
timestamp: 2026-11-02T13:50+07:00
---
# Brief: listen to proposed angles (and their intros) — a play button per proposal (2026-11-02)

**From:** `flivideo-orch` (Swagger). **To:** `storypilot-dev`. Report to `flivideo-orch` by name.

## David's words (2026-11-02, looking at D13's "Proposed angles" block)
"Angles are something I'm always going to want to listen to, not read. Automated audio for it and a play button would be useful."

## Build
- In the **Proposed angles** block (the A / B / C rows with **USE THIS**), add a **play button** to each proposal.
  It speaks the proposal with Kokoro through the same speech path Listen already uses (FliTools speech, cached by
  text hash, so a second play is instant and an unchanged proposal is never regenerated). One playing at a time;
  pressing another stops the first. Space / J / K / L behave as in Listen while one is playing.
- **Intros:** the three-intros run wrote an intro per angle into files
  (`/Users/davidcruwys/dev/video-projects/v-appydave/d13-overlay-pilot/script/three-intros-2026-11-02.md`,
  `/Users/davidcruwys/dev/video-projects/v-appydave/d18-story-pilot/resources/three-intros-2026-11-02.md`). Let a
  proposal carry an optional `intro` text (extend `story.angle.propose`, Story Pilot's own verb, backwards compatible);
  when present, the play button reads the angle line, then the intro. Backfill D13 and D18 proposals from those files
  through the verb (agent writes; never `story.angle.set`).
- Also a **"play all three"** control that reads A, B, C in order with a short spoken label ("Angle A") before each.
- Audio generates automatically when proposals are written or changed (the Listen staleness pattern); show a small
  "generating" state, never a modal.
- Run it through a UX pass. Script sheet keeps its 960px cap.

## Done means
- Typecheck, `npm test`, targeted storypilot e2e only (add one: proposals render a play button; play requests speech).
- **Real-browser proof** on your branch, then (after orch merges) on live :7150 with D13: press play on B, hear-able
  evidence = audio element playing + its src, screenshot. Save to `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-02/`.
- Branch from current main (`cecb09d`) in a fresh worktree, never the live checkout. Do not merge or restart. Report
  branch + commit + proof paths.

## Limits
Story Pilot module only. Never set or remove an angle. Questions to orch with a recommendation.
