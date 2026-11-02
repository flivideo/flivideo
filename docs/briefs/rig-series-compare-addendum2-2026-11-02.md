---
created: 2026-11-02
timestamp: 2026-11-02T18:15+07:00
---
# Brief addendum 2: David's verdict frame — is AppyTron a working version? (2026-11-02)

**From:** `flivideo-orch`. **To:** `rig-compare-rsch`. Extends `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/rig-series-compare-addendum-2026-11-02.md`; this frame governs it.

## David, verbatim (relayed via roamy-home-orch, 18:10)
"If OpenRig loosened the rules or did anything to get around violations, I don't consider the AppyTron run a working
version, and we go back to the AppyTron rig. The goal was always to run it the way a human would: get the application into
good working order AND stop bad code in future, without stupid over-engineering like Spaghetti Rig's magic keys and magic
numbers, when we were really just looking at data. We should have taught the programmer, and more importantly the
architect, a better way to do it."

## Weigh three questions, with evidence for each
1. Will FUTURE code improve? (prevention)
2. Did bad code ALREADY in the system improve? (remediation)
3. Is the push for deterministic rules itself over-engineering — a rule that should have been architect guidance?

## Required: one table per run (AppyTron, AppyStack), one row per gate (all of them)
Columns: the rule · violations when switched on · resolved by (**code fixed / rule loosened** (error→warn, threshold raised)
**/ suppressed** (disable comments, ignore lists, baselines, scoped-out paths) **/ none**) · verdict (**earns its place /
over-engineered, should be architect guidance / papered over**).

Grep the app repos — read-only (`git fetch` and `gh` are fine; no checkout changes, no commits there):
`/Users/davidcruwys/dev/ad/apps/appytron`, `/Users/davidcruwys/dev/ad/apps/appystack` (or the run's PR diffs via `gh pr diff`)
for `eslint-disable`, oxlint ignores, `@ts-ignore` / `@ts-expect-error`, baseline / allowlist files added during the run,
and config diffs that weakened severity or thresholds. Count before vs after the run.

## Bottom line, stated plainly
"AppyTron is a working version" or "AppyTron goes back to the rig", with the deciding evidence. Same for AppyStack if the
evidence differs. Do NOT relaunch or change anything; that is David's call.

Put the tables + bottom line in the artefact (same slug) and in
`/Users/davidcruwys/dev/appyrigs/runs/ladder/analysis/d19-story-insight-2026-11-02.md`. Commit, push, report to `flivideo-orch`.
