---
created: 2026-11-02
timestamp: 2026-11-02T14:30+07:00
---
# FliStudio loose ends — audit, 2026-11-02 (read-only)

**By:** `storypilot-dev`, for `flivideo-orch`. Nothing in `flistudio` was changed or committed (the only writes are this file and a
scratch extractor run outside the repo). Checked against FliStudio `main` at `698df5a`.

| # | Thing | Verdict |
|---|---|---|
| 1 | `aitldr-production` (2 commits, 125 behind main) | **Do not merge as-is. Keep the ref** (it is pushed to `origin/aitldr-production`); decide whether to port it. Ask David / Jan first. |
| 2 | `pair-remove` worktree (`publish-social-fix`, 0 ahead) | **Safe to remove**, after archiving the untracked script (it has been run; archive copy is optional). |
| 3 | `docs/schema-mirror.{md,json}` | **Stale: 443 differences.** Regenerating is four commands and a commit; do it once the Story Pilot / B-roll contracts stop moving. |

---

## 1. `aitldr-production`

**State.** Worktree `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/aitldr-production`, clean (no untracked or modified files).
`git rev-list --count main..HEAD` = 2; `HEAD..main` = 125 (the orch note said 111; it has grown). The branch is pushed
(`origin/aitldr-production`), so removing the worktree loses nothing. Fork point `3ea915d` (2026-10-13).

### What the two commits do

Both are by David's session with `Co-Authored-By: Claudia`; both are AITLDR-only (the page makes no call for AppyDave).

| Commit | Date | What |
|---|---|---|
| `99e8ff2` feat(aitldr): read-only Production strip per day + stage chip in the Series list | 2026-10-14 | New read-only capability `production.view { brand, project? }` (+1 capability, 105 then). Parses Jan's `/prod` files: `script/plan.md` "Production checklist" (top-level boxes are stages, ticked/total, `next` = first open, `last` = latest dated note, "Carried over" kept out of the count, open `→ [ ]` asides surfaced) and `script/handoff/handoff.md` (File table + Sent date; a file counts as here when `voice/` or `avatar/` holds that name or `name-tN`). Missing or unparseable files are said with a reason, never guessed. UI: a Production strip on the project page and a stage chip per Day in the Series list. Parser tests on byte-exact copies of b16/b17/b18. |
| `8acc93f` feat(aitldr): six-step strip from files + "waiting on team", per brand as data (Jan 009) | 2026-10-15 | `production.view` also returns `steps` from `shared/src/production-steps.ts` (`PRODUCTION_STEPS`, keyed by brand, pure data). AITLDR: Script → Voice → Alex → Animation → Final → Short → Published, each read from files that exist; states done / waiting (team step while `script/handoff/` exists) / gap (a later Final/Short/Published is done) / open. Compact strip per Day in the Series list. Fixtures from Jan's Mac (b13 gap, b16 waiting, b18 complete+published, b19 built motion, b20 plan only, AppyDave none). |

Size: 29 files, +3331 / −8, mostly tests and fixtures; real code is `server/src/capabilities/production.ts` (~410 lines),
`shared/src/production-steps.ts` (127), `Production.tsx`, `productionModel.ts`, CSS.

### Who asked

- **Jan, message 009, 2026-10-15** — `/Users/davidcruwys/dev/aitldr/aitldr-brain/team/comms/009-from-jan.md`: "FliStudio idea: an AI-TLDR
  pipeline strip on the project home", Script → Voice → Alex → Animation → Final → Short, "done" read from files, a "waiting on team"
  state, per brand (not in FliStudio's code), maybe a 7th "Published". It is framed as *"an idea for David to judge, not a request to build now"*.
  The second commit implements exactly its three thoughts.
- The first commit cites a "gaps doc 2026-10-14, gaps 1–2" (spec row in the branch's `docs/specification.md`). **I could not find that doc** on disk
  (searched `flivideo/docs`, `flistudio/docs`, the aitldr-brain comms). Unverified who wrote it; it reads as David's own list.
- I found **no reply** to 009 in the comms folder (010 is `start-day`, 011 is an unrelated status). So there is no record that Jan was told
  the strip exists or asked for it as a build. Whether Jan wants this is unverified.

### Does it still apply to main?

**No, not cleanly.** `git merge-tree --write-tree main aitldr-production` (read-only) reports **10 conflicted files**:
`.dependency-cruiser.cjs`, `api/openrpc.json`, `client/src/api.ts`, `client/src/screens/ProjectHome.tsx`, `client/src/styles/studio.css`,
`server/src/capabilities/{capabilities,door}.test.ts`, `server/src/cli/cli.test.ts`, `shared/package.json`, `shared/src/index.ts`.
Seven of those are mechanical (counted lists, regenerated openrpc, a CSS tail, package exports). The real ones are `ProjectHome.tsx`
(the page has been reworked since: pipeline strip, extensions, status) and `studio.css`. I did not run its tests against main.

### The overlap that matters

Main now has **Project status** (brief `project-status-build-2026-10-31`): a status column **computed from files**, for every brand, with
`STEPS` as data "so a brand recipe can swap it later" (`server/src/capabilities/project-status.ts`: idea, script, record, edit, export,
final, launch, publish). That is the same idea as Jan 009 (state read from files, per-brand list as data, a stall/held notion), built
generically. What Jan's branch has that main does **not**:

1. The AITLDR-specific steps (Voice / Alex / Animation come from the team, not from FliStudio's own folders).
2. The **"waiting on team"** state keyed on `script/handoff/` and the handoff table — the part Jan said helps most.
3. Parsing Jan's `/prod` `plan.md` checklist (stage, next step, loose-end asides).
4. A compact strip per Day in the Series list.

Items 1–3 are the value; 4 is UI. `production-steps.ts` is the part that translates directly into a Project-status brand recipe.

### Recommendation

**Keep the ref, do not merge, and do not remove the branch from origin.** Then one question to David (or Jan via the liaison):
*"Does the Project-status column already answer Jan 009, or do you want the 'waiting on team' part?"*

- If **no**: drop it. Tag it first (`git tag archive/aitldr-production origin/aitldr-production`) so the work is findable.
- If **yes**: re-do it on main as a **Project-status brand recipe** (AITLDR steps + the waiting state) and carry across only the
  parser (`production.ts`) and the byte-exact b16–b19 fixtures, not the old page/CSS. Roughly half a day; the conflicts above are the reason
  not to rebase it.

The worktree itself (clean, branch on origin) can be removed any time.

---

## 2. `pair-remove` worktree

`/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/pair-remove`, branch `publish-social-fix`, HEAD `3ea915d`.

- **0 ahead of main**; `3ea915d` is an ancestor of main (`git merge-base --is-ancestor` = yes). Also on `origin/pair-remove` and
  `origin/publish-social-fix`. The fix it was built for — "marking published decides nothing; a newer proposal asks again (D10)" — is in main.
- The only untracked file is `scripts/repair-d10-social.py` (137 lines). **What it does:** a one-off, dry-run-by-default repair of **D10**
  (`appydave/d10-ai-powered-video-cuts`) after the 2026-10-13T07:03:17Z "mark published" click that restamped every `chosen` piece as
  `published`. Per piece it (A) undoes the stamp (status `published`→`chosen`, `changed` back to its `added` stamp) and (B) for pieces with a newer
  undecided proposal (social x/linkedin/facebook, description, chapters, pinned-comment) turns the old decision into a plain `candidate`. The video
  stays published. `--apply` writes `fli.resources.json` atomically and refuses if the file changed while running. Paths and resource ids are hard-coded to D10.
- **It has already been run.** `fli.resources.json` in D10 now shows six of those pieces as `candidate` with `changed.by = agent:repair-d10`
  (2026-10-14T01:37:15Z), the social/description/chapters/pinned-comment rows exactly as step B describes; the keywords / end-screen / studio-settings
  pieces are back to their original `chosen` stamps; the video is still `published`. The one remaining `07:03:17.106Z` stamp is the video itself,
  which the script says to leave.
- A different, earlier repair script (`flivideo/docs/runbooks/repair-d10-publish-stamp.py`, untracked there) takes another approach (delete records,
  back up to `-trash`). The pair-remove one is the one whose result is on disk.

**Safe to remove: yes.** Spent, hard-coded to one project, its effect is in the data and its cause is fixed in main. Value: low (only as a worked
example of the lane rule's "repair through the file, atomically, dry-run first"). If you want it kept, copy it to
`/Users/davidcruwys/dev/ad/flivideo/docs/runbooks/repair-d10-social.py` **before** `git worktree remove` (an untracked file does not survive
`--force`), and say in the first line that it was applied on 2026-10-14. I did not copy it (read-only brief).

---

## 3. `docs/schema-mirror.md`

**How stale.** Generated `2026-11-01T01:00:55Z` at commit `1eba790` (the fli-notes commit). Since then 8 commits changed contract-bearing code
(`shared/src`, the three modules' `shared/`, `extension-core/src`): Story Pilot Listen, Listen v2, Prep, Templates, Recorded segments, B-roll catalogue
upload/scan, fli-notes v2. `verify_mirror.py docs/schema-mirror.json` exits **1 with 443 differences**.

Concrete misses in the committed mirror (counted by search): `AudioStatusOutput` / `AudioParagraph` 0, `AngleSetInput` 0, `PrepSetInput` 0,
`TemplatesSetInput` 0, `SegmentSetInput` 0, `broll.upload` 0. And shapes it does hold have moved: the `Script` object there lacks `presenter`.

**What regenerating gives** (I ran the extractor to a scratch file outside the repo, not over the committed mirror):

| | committed (2026-11-01) | fresh run (2026-11-02) |
|---|---|---|
| declarations | 1204 | 1307 |
| mirrored | 1011 | 1106 |
| not read | 184 | 192 |
| gaps | 9 | 9 |
| findings | 22 | 23 (6 new, 5 gone; new ones are minor "REFACTOR" notes: set `ROLES` in storypilot `contracts.ts:154`, `AUTOMATIC` in broll-pilot `index.ts:69`, `RAW_CHANNELS` in storypilot `story.ts:114` name a set without a declaring symbol) |

**What it takes** (per `flivideo/docs/agent-comprehension-docs.md` step 1; `S` = `/Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/schema-mirror/scripts`):

```bash
cd <a worktree of main with npm ci>          # the extractor uses the repo's own typescript and exits 3 rather than guess
python3 $S/detect_stack.py .                  # typescript/zod must show [OK ]
python3 $S/extract_typescript.py . -o docs/schema-mirror.json
python3 $S/render_mirror.py docs/schema-mirror.json -o docs/schema-mirror.md
python3 $S/verify_mirror.py docs/schema-mirror.json      # must exit 0
```

Then read the page's "Cannot be mirrored" table (9 gaps; shapes from `@flivideo/core` are named gaps by design) and commit both files. About ten
minutes of work, one commit; the diff is large (the `.md` is ~11.6k lines) so review it as "regenerated", not line by line.

**Cautions.**
- `docs/AGENT-NOTES.md` tells agents to read this mirror "do not retype shapes"; right now that sends them to a page that omits Prep, Listen,
  Templates and Segments. That is the real cost of leaving it stale.
- Do it when the Story Pilot / B-roll lanes are quiet, or it is stale again within a unit. A cheap guard is to run `verify_mirror.py` in
  `npm run lint` (or CI) so drift fails loudly; I have not tried that, so treat it as a suggestion.
- The extractor reads the working tree, so regenerate from a clean checkout of main, not from a feature branch.

---

## What I did not establish

- Whether Jan still wants the Production strip, and who wrote the "gaps doc 2026-10-14" (not found).
- Whether `aitldr-production`'s tests pass against main (not run; only the merge conflicts were counted, read-only).
- Whether anything else points at the `pair-remove` / `publish-social-fix` branch names (CI, notes); only their git ancestry was checked.
