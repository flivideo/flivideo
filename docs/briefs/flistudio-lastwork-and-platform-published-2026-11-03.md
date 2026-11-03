---
created: 2026-11-03
timestamp: 2026-11-03T18:00+07:00
---
# Brief: FliStudio — LAST WORK ignores bookkeeping; Published accepts a platform URL (2026-11-03)

**From:** `flivideo-orch` (Swagger). **To:** `published-dev` (M4, cwd `/Users/davidcruwys/dev/ad/flivideo`). Report to `flivideo-orch`.
**Go:** David's go for recommended work, relayed by `roamy-home-orch` ~17:55 (rulings 2 and 3). Run to done; **orch merges**.

## Background
`/Users/davidcruwys/dev/ad/flivideo/docs/reports/aitldr-series-b-published-2026-11-03.md` §1–§2 (file:line refs).
FliStudio consumes fli-core as `"@flivideo/core": "github:flivideo/fli-core#v0.28.0"` (`flistudio/server/package.json:19`).

## Work in worktrees only (never the live checkouts)
- FliStudio: `git -C /Users/davidcruwys/dev/ad/flivideo/flistudio worktree add /Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/published-platform -b published-platform`
- fli-core: `git -C /Users/davidcruwys/dev/ad/flivideo/fli-core worktree add /Users/davidcruwys/dev/ad/flivideo/fli-core-worktrees/published-platform -b published-platform`

## Unit A — LAST WORK (FliStudio only)
In `flistudio/server/src/capabilities/project-status.ts` (~:640, `walked.newest`), exclude bookkeeping from the newest-mtime
walk: `fli.*.json` (incl. `fli.resources.json`), `fli.*.jsonl` (notes/facts logs), and the status file. LAST WORK must mean
media/script/other real work. Check the fingerprint cache (`statusOf` ~:453–473) still invalidates when bookkeeping changes
(status must still recompute; only the LAST WORK date ignores it). Tests: a project whose newest file is `fli.resources.json`
reports the older media date; one whose newest file is a script/media file reports that.

## Unit B — Published accepts a platform URL (fli-core then FliStudio)
- fli-core `src/publish.ts`: `publishedVideos()` (~:713) also accepts a published `video` resource with
  `meta.publishedUrl` (string URL) + `meta.platform` (`'youtube' | 'skool' | 'other'`) and no `youtubeId`. Return shape
  gains `platform` and `url`; `youtubeId` becomes optional. Existing youtubeId-only resources keep working exactly as now
  (platform defaults to `'youtube'`). Extend `mark-published` (~:819–841) with a `--url <url> --platform <p>` path
  that doesn't require a YouTube id; YouTube id path unchanged. Unit tests for both paths + back-compat. Bump to
  **0.29.0** with a CHANGELOG entry. Do NOT tag or push fli-core main — leave the branch for orch.
- FliStudio: `project-status.ts` Published step (~:204–213) and any `youtubeId` assumptions downstream (grep server +
  client) handle the optional id. If cheap, show the platform on the row (e.g. a small "Skool" label next to PUBLISHED when
  platform ≠ youtube). Point the dependency at the fli-core worktree only for local testing; the final diff will reference
  `#v0.29.0` after orch tags it.

## Gate (your side)
In each worktree: typecheck + unit tests green (`npm run typecheck`, `npm test` — targeted e2e only, never the full e2e suite).
Commit on the branches. **STOP and report** to `flivideo-orch` with: both branch names + shas, test/typecheck tails, the diff
stat, and anything that needed a judgement call. Orch will merge fli-core, tag v0.29.0, then tell you to bump FliStudio's
dependency; after that orch merges FliStudio, restarts and screenshots.

## Limits
No edits to video projects (another worker is writing v-aitldr). No `my-app` restarts. Don't touch the live
`flistudio/` or `fli-core/` checkouts. Don't record any Skool URL — David hasn't given them.
