---
created: 2026-11-02
timestamp: 2026-11-02T17:45+07:00
---
# Brief: three-way rig comparison + "did the gates improve or only prevent?" (2026-11-02)

**From:** `flivideo-orch` (Swagger). **To:** `rig-compare-rsch` (M4, cwd `/Users/davidcruwys/dev/appyrigs`).
Report to `flivideo-orch` by name. **Go:** David, relayed from `roamy-home-orch` 17:35. He does not want to watch: run to done.

## Task
1. Extend `/Users/davidcruwys/dev/appyrigs/runs/ladder/appystack/analysis/cross-run-comparison.md` with an **AppyTron column**.
   Sources: `/Users/davidcruwys/dev/appyrigs/runs/ladder/appytron/analysis/WEIGH-UP.md`, `.../appytron/decisions-driver.md`,
   `.../appytron/prs.json` (if missing, `gh pr list -R appydave/appytron --state merged --json …`). Timeline to verify, not
   copy: Spaghetti game ~6 days / 136 PRs · AppyStack ~1 day / 29 PRs · AppyTron ~17 h / 23 PRs. Correct any number the
   evidence contradicts and say so.
2. Answer David's question, with evidence (file paths, line counts, PR numbers):
   - Did the gate ladders **improve** existing app code, or mainly **prevent** bad code in future? (AppyTron weigh-up:
     app code 710 → 790 lines, gates 0 → 14, gate proofs added no coverage.)
   - Why didn't deterministic gates lift the quality of LLM-built apps from older models?
   - Is prevention-only still worth what it cost (time, PRs, tokens where recorded)? Give a verdict, then the case against.
   - What each run learned that made the next better (Spaghetti → AppyStack → AppyTron), from `/Users/davidcruwys/dev/appyrigs/LEARNED.md`.
3. Publish it as a Claude artefact: load `brand-dave:brand` first; AppyDave, **light only**; `grep -c prefers-color-scheme`
   must be 0. Lead with the verdict, then the three-column table, then the evidence. Keep the HTML source at
   `/Users/davidcruwys/dev/appyrigs/runs/ladder/analysis/three-way-comparison-2026-11-02.html` (create the folder) and use
   `publish_files`.
4. Commit only your files in appyrigs (`git add <paths>`; leave `.openrig/` alone), push to main.

## Done means
File + HTML committed and pushed (give the sha), artefact URL. Report both to `flivideo-orch`; orch registers the URL on D19.

## Limits
Read-only on everything else: do not touch the rigs, their worktrees, the appystack/appytron repos, or any tmux session.
Do not run builds. Questions to `flivideo-orch` with a recommendation.
