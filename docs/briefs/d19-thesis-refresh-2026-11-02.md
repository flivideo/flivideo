---
created: 2026-11-02
timestamp: 2026-11-02T18:45+07:00
---
# Brief: D19 thesis refresh + three angle proposals (2026-11-02)

**From:** `flivideo-orch` (Swagger). **To:** `d19-storypilot-video` (M4, cwd `/Users/davidcruwys/dev/video-projects/v-appydave/d19-spaghetti-rig`).
Report to `flivideo-orch` by name. **Go:** David via `roamy-home-orch` 17:35 ("Job C"). He isn't watching: run to done.

## Where D19 stands
Your last state (Sunday): thesis "PROOF PENDING", holding for AppyStack tier results and the finish. Both have landed:
- AppyStack and AppyTron runs finished. AppyTron: 23 PRs merged, `appydave/appytron` main `8c29f3f6`.
- The three-way comparison and the per-gate audit: https://claude.ai/artifact/BQK5MXiU1HNigqZg47arB7 (source
  `/Users/davidcruwys/dev/appyrigs/runs/ladder/analysis/three-way-comparison-2026-11-02.html`, appyrigs `beccb105`), the
  story insight `/Users/davidcruwys/dev/appyrigs/runs/ladder/analysis/d19-story-insight-2026-11-02.md`, and
  `/Users/davidcruwys/dev/appyrigs/runs/ladder/appystack/analysis/cross-run-comparison.md`.
- New on D19 today (Story Pilot tray): AppyTron progress + validation pack, the comparison, appytron WEIGH-UP / decisions
  files. Read them with the `flivideo:storypilot` skill / `story.*` verbs.

## Findings to carry (from the audit; carry its hedges)
- Gates mostly **prevent**; they **improved** existing code only where it was a mess (Spaghetti). Prevention is proven by
  planted bugs only, never by a real regression blocked.
- Bottom lines: AppyTron and AppyStack "a working version, with exemptions for David to confirm"; Spaghetti "back to the
  rig" by David's own test (data exempted by name, a coverage floor lowered).
- Over-engineering partly true: magic numbers, re-exports, cohesion/coupling and the proof harness should have been
  architect guidance. David: "We should have taught the programmer, and more importantly the architect, a better way."
- David's own reading ("the code was already good; gates keep bad code out") is **partly supported**: tidy, not good
  (AppyStack blind review C, 24 problems no gate touches). Do not present it as proven.

## Do
1. Rewrite D19's thesis in Story Pilot to fit the finished series (Spaghetti → AppyStack → AppyTron). Mark it provisional
   where proof is still missing.
2. Propose **three angles**, each with a short intro (as for D13/D18), via `story.angle.propose` (with `intro`) so they
   play in Story Pilot. **Do NOT lock or write the angle** — David picks.
3. Place/order the new sources only as proposals (undoable); remove nothing; do not touch the script.
4. Commit only the d19 folder in v-appydave, push. Report: thesis text, the three angles + intros, sha.

## Limits
D19 only. No rig launches, no app repos, no other projects. Questions to `flivideo-orch` with a recommendation.
