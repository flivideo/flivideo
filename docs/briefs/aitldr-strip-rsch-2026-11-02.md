---
created: 2026-11-02
timestamp: 2026-11-02T13:15+07:00
---
# Brief: reconstruct Jan's AITLDR production strip (message 009) — research only (2026-11-02)

**From:** `flivideo-orch` (Swagger). **To:** `aitldr-strip-rsch`. This window is David's place to talk the idea
through; you prepare him, then stay in the conversation with him.

**Why:** David ruled NOT to drop the strip (11-02 report, decision 5). He only vaguely remembers what Jan proposed.

## Sources
- Jan's message: `/Users/davidcruwys/dev/aitldr/aitldr-brain/team/comms/009-from-jan.md` (2026-10-15) and any replies
  around it in the same `comms/` folder.
- The archived build: tag `archive/aitldr-production` in `/Users/davidcruwys/dev/ad/flivideo/flistudio`
  (commits `99e8ff2`, `8acc93f`; fork point `3ea915d`). Read it with `git show` / `git log -p` only.
- Orch's audit: `/Users/davidcruwys/dev/ad/flivideo/docs/specs/flistudio-loose-ends-2026-11-02.md` §1.
- The files it parsed: Jan's `/prod` files (`script/plan.md`, `script/handoff/handoff.md`) — locate real AITLDR projects
  under `/Users/davidcruwys/dev/video-projects/v-aitldr/` and say which ones still have them.

## Produce
`/Users/davidcruwys/dev/ad/flivideo/docs/specs/aitldr-strip-reconstruction-2026-11-02.md`:
1. What Jan asked for, in his words (quote).
2. What was built (the six steps, states done/waiting/gap/open, where each is read from) with a small ASCII mock of the strip.
3. What has changed since 10-15 (FliStudio is now ~125 commits ahead; does `production.view` still fit; is the AITLDR
   `/prod` file shape still what Jan uses today).
4. Three options for David (port as-is / rebuild on today's FliStudio / something else), each with cost and a recommendation.
5. Questions only Jan can answer.
Then give David a short summary in this window and wait for him.

## Limits
- Research only. **Do not restore or recreate the worktree, do not check out the tag into a working tree, do not merge,
  do not delete the tag.** Do not message Jan.
- Commit your doc to `/Users/davidcruwys/dev/ad/flivideo` (docs only) and push. Report the path to `flivideo-orch` by name.
