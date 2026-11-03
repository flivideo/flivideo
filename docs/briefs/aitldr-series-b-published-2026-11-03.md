---
created: 2026-11-03
timestamp: 2026-11-03T17:40+07:00
---
# Brief: FliStudio landing page — status/heat map, "Published", and Series B YouTube URLs (2026-11-03)

**From:** `flivideo-orch` (Swagger). **To:** `aitldr-published-rsch` (M4, cwd `/Users/davidcruwys/dev/ad/flivideo`).
Report to `flivideo-orch` by name. **Source:** David's questions, relayed by `roamy-home-orch` ~17:35. He isn't watching: run to done.

David is looking at FliStudio's project landing page for the AITLDR Series B list (b01 yt-performance … b17 captions,
`/Users/davidcruwys/dev/video-projects/v-aitldr/bNN-*`). Rows show LAUNCH PREP or EXPORTED, all with LAST WORK 27 Oct;
filter chips read "Published 0", "Working 29".

## Answer with evidence (file:line, read-only on code)
1. **Heat map + status:** what computes the row's status word and the strip of stage squares; when it refreshes (page
   load / scan / cron / file watcher). Why every row shows 27 Oct as LAST WORK — stale, or real? (Check the files'
   real mtimes / facts-log entries for two or three projects; note `v-aitldr-premerge-2026-10-27/` exists next door —
   a merge/copy on 27 Oct may have reset dates.) Source: `/Users/davidcruwys/dev/ad/flivideo/flistudio/` and
   `/Users/davidcruwys/dev/ad/flivideo/fli-core/`; skill `flivideo:flistudio`.
2. **Published:** exactly which field/file makes a project Published, who sets it, and whether a YouTube URL or video id
   flips it.
3. **Series B URLs:**
   - Find where AITLDR channel videos were catalogued before (appydave-tools, the `ylo` skills, `appydave:tube-harvest`,
     `v-aitldr/catalog/`, FliStudio's `youtube.sync` and its local list, Captain's Log). Did any of it cover Series B?
   - If URLs aren't known, list the AITLDR channel's uploads with the tooling that already exists (FliStudio
     `youtube.sync` is public-only and read-only — fine; don't add new credentials) and match them to bNN projects.
   - **Write** the URL only where the match is unambiguous (title or episode number clearly matches), and only through
     the field/verb that drives Published — prefer a FliStudio/fli-core verb over hand-editing JSON; if only hand-editing
     is possible, edit one project, confirm it turns Published in the UI, then do the rest. List ambiguous/unmatched
     ones; never guess.
   - **Prove it:** "Published N" chip count before and after, each with a screenshot of the landing page
     (FliStudio at http://localhost:7150, or the dev URL `my-app` reports). Save screenshots under
     `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-03/`.

## Limits
- **Don't collide with `jan-video-intake`** (a roamy-home-orch worker copying Jan's new videos into v-aitldr projects
  right now): do not create, move or copy media in `v-aitldr/`; only write the published field. If new bNN projects
  appear while you work, include them in the table.
- No FliStudio/fli-core code changes, no restarts, no `my-app` changes. If Published can only be fixed by a code change,
  stop and describe it.
- Close any browser you open.
- Commit only what you wrote (`git add <paths>`): the report below plus any project-data repo the field lives in (check
  whether `v-aitldr` is a git repo; commit there only your field edits). Push.
- Write the answers + mapping table to `/Users/davidcruwys/dev/ad/flivideo/docs/reports/aitldr-series-b-published-2026-11-03.md`.
- STOP and report to `flivideo-orch`: the three answers (short, with file:line), the mapping table
  (bNN → URL → matched / ambiguous / unmatched), chip count before → after with screenshot paths, and the shas.
