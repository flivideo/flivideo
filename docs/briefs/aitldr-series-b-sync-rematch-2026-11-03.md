---
created: 2026-11-03
timestamp: 2026-11-03T18:00+07:00
---
# Brief: Series B — fresh public youtube.sync, then re-match the leftovers (2026-11-03)

**From:** `flivideo-orch`. **To:** `aitldr-sync-rsch` (M4, cwd `/Users/davidcruwys/dev/ad/flivideo`). Report to `flivideo-orch`.
**Go:** David's go for recommended work, relayed by `roamy-home-orch` ~17:55 (ruling 1). Run to done.

## Read first
`/Users/davidcruwys/dev/ad/flivideo/docs/reports/aitldr-series-b-published-2026-11-03.md` — the earlier pass: method,
the "clear" rule (duration pattern mains +4.5…+5.5 s, Shorts +0…+1.1 s, AND title/description/transcript matches the
project's own content, AND ranks first against other same-format uploads), the resource shape it hand-wrote, and the table.

## Do
1. Run FliStudio's **public, read-only** `youtube.sync` for the AITLDR brand (verb via FliStudio at http://localhost:7150
   or its CLI; skill `flivideo:flistudio`). No new credentials, no OAuth, no uploads. Report the mirror's new video count
   and newest publish date (was 426, last sync 29 Oct).
2. Re-match, same rule, ONLY these: **b26** (main + Short), **b24/b25 Shorts**, the unmatched Shorts **b11–b15, b17–b22**,
   **b05 Short** (was ambiguous on length), and the stray **GaExvmBUa0I** (place only if clear). Do not touch any id
   already written. b01 main stays reverted unless new evidence proves it.
3. Write only clear matches, same shape/stamp as before (`by: agent:aitldr-sync-rsch`). Commit in v-aitldr with
   `git add <exact paths>` — **never** `b26-repurpose/fli.resources.json` if Jan's uncommitted edit is still there: if
   b26 matches, report it instead of writing, so Jan's edit isn't mixed in. Never commit `b27-postmortem/` or any
   `transcripts/` folder. Push; no amend, no force.
4. Append a dated "Pass 2" section to the report (table: bNN, video, id, YouTube title, durations, verdict), commit
   flivideo, push. Screenshot the AITLDR landing page after (`docs/reports/proof-2026-11-03/series-b-published-5-pass2.png`)
   and give the chip counts. Close any browser you open.

## Limits
No code changes, no restarts. Another worker is changing FliStudio code in a worktree; don't touch `flistudio/` or `fli-core/`.
STOP after the pushes; report: sync count, rows written, rows still unmatched, chip counts, shas.
