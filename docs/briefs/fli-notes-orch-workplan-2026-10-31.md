# fli-notes overnight — orch work plan — 2026-10-31

**Parent brief (read it in full first):** `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/fli-notes-suite-record-2026-10-31.md`
(flivideo `cda4daa`). David's go, 2026-10-31 ~23:00 +07: *"go with recomendations"*. This file only splits that brief
into three workers and fixes the hand-offs. **Orch:** `flivideo-orch` (SendMessage). Route every question to orch with
a recommendation; never wait on David. Taste calls: decide on the recommendation, list them in your report.

## Workers

| Session | Worktree (build here only) | Branch | Brief section |
|---|---|---|---|
| `fli-notes-core-dev` | `/Users/davidcruwys/dev/ad/flivideo/fli-core-worktrees/notes-record` | `notes-record` | §4A |
| `fli-notes-studio-dev` | `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/fli-notes` | `fli-notes` | §4B |
| `fli-notes-cut-dev` | `/Users/davidcruwys/dev/ad/flivideo/flicut-worktrees/fli-notes` | `fli-notes` | §4C |

§4D (the D13 first live record) and the morning UAT page are orch's, after B is merged and live.

## Hand-off: the fli-core release candidate

1. `fli-notes-core-dev` builds §4A, bumps to `0.27.0-rc.1`, adds a CHANGELOG entry in the v0.26.0 style, commits on
   `notes-record`, pushes the branch and the tag `v0.27.0-rc.1` (never push `main`), then messages orch **and**
   both app workers (`fli-notes-studio-dev`, `fli-notes-cut-dev`) with: exported names, the record type, file name,
   and one usage example.
2. The app workers start at once on the parts that don't need the schema (target attributes, the toggle + shortcut,
   the note box, the door-logging seam inside their write paths). When the rc message arrives they pin
   `github:flivideo/fli-core#v0.27.0-rc.1` everywhere `@flivideo/core` is pinned, `npm install`, and finish.
   Don't vendor or `file:`-link fli-core in a commit.
3. Orch merges fli-core to `main`, tags `v0.27.0`, and repins the apps to `#v0.27.0` at merge time.

## Rules for every worker

- `pwd` + branch check first; stop if either differs.
- Fire the platform conventions skill first (`appystack:appystack-conventions` for FliStudio,
  `appytron:appytron-conventions` for FliCut); `dev-team:drivable` for the RPC verbs.
- Own ports only — never 7150/7151/7111/7121/7161/5173/5101. Fixture project dirs only — never write into
  `/Users/davidcruwys/dev/video-projects/`. Reading real folders is fine.
- Never merge to main, restart apps, `pkill`/`killall` with patterns, touch takes / video files / `fli.edit.*`, or
  write notes into `fli.status.json`.
- No thumbs/ratings/stars. Three kinds only: `note`, `ask`, `change`.
- Report to orch with: DoD rows from the brief's §6 that you own (pass/fail + how checked), gate output (typecheck,
  unit, lint, e2e), screenshots for UI, the decisions you took on taste calls, and anything deferred with the reason.
