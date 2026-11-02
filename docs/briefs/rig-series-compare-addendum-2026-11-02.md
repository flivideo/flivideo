---
created: 2026-11-02
timestamp: 2026-11-02T18:05+07:00
---
# Brief addendum: test "the code was already good; gates keep bad code out" (2026-11-02)

**From:** `flivideo-orch` (Swagger). **To:** `rig-compare-rsch` (M4, cwd `/Users/davidcruwys/dev/appyrigs`).
Report to `flivideo-orch` by name. **Go:** David via `roamy-home-orch`, 18:00. Run to done, he isn't watching.

## Already done (do not redo)
`/Users/davidcruwys/dev/ad/flivideo/docs/briefs/rig-series-compare-2026-11-02.md` was executed: appyrigs `e195a7d8` + `624cd2e6`,
artefact https://claude.ai/artifact/BQK5MXiU1HNigqZg47arB7 (slug `543ca1e9-52a5-4c15-b45a-3135bd5e2a56`), source
`/Users/davidcruwys/dev/appyrigs/runs/ladder/analysis/three-way-comparison-2026-11-02.html`. Verdict there: mostly prevention.

## The hypothesis to test — not to prove
David's reading: **the existing app code was already good, and the gates now keep bad code out.** He wants it as a D19 story
learning. The rival reading fits the same headline: **"app code barely changed" because the rig never tried to fix it.**
Weigh both. Evidence, per run (AppyStack, AppyTron; Spaghetti for contrast):
1. When each gate was switched on, how many violations did the existing code have, and how many fixes did it take?
   (gate records `runs/ladder/*/g*-record.md`, `*-measure*`, `c1-*`, PR diffs via `gh pr view`.)
2. Was any rule loosened so existing code would pass — error → warn, disabled, thresholds raised, paths scoped out/ignored?
   Check the gate configs in the merged PRs and the decisions files.
3. What did the blind reviews say about code quality? (`runs/spaghetti/*/blind-review*`, `runs/ladder/appystack/analysis-blind-*`,
   AppyStack/AppyTron judge folders.)

## Deliver
- A verdict: **supported / partly supported / not supported**, with the counts and quotes that decide it, and what remains
  unknown. State plainly if the evidence can't separate the two readings.
- Add it as a new section to the HTML and to `cross-run-comparison.md`; republish **the same artefact** (slug above,
  `publish_files` with `base_version` from `get_artifact`), light only, ghost-check 0. Commit only your files, push.
- Write the insight to `/Users/davidcruwys/dev/appyrigs/runs/ladder/analysis/d19-story-insight-2026-11-02.md`: one-line claim
  (as the evidence supports it, not as hoped), the verdict, 3–6 evidence bullets with file paths / PR numbers. Orch registers it on D19.
- Report to `flivideo-orch`: verdict, sha, artefact version.

## Limits
Read-only on everything else: no rigs, worktrees, appystack/appytron repos, tmux sessions, builds. Do not write to D19 yourself.
