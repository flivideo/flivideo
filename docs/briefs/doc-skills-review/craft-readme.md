# Review — dev-team:craft-readme

**Purpose**: An independent review of the `craft-readme` skill, judged by the six READMEs it produced in the FliVideo suite on 2026-09-22/23, not by what its docs claim.
**Reviewer**: independent subagent, 2026-09-23. Read-only: nothing was edited except this file.
**Skill**: `/Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/craft-readme/` (SKILL.md, 5 references, 7 templates, all read in full)
**Method it serves**: `/Users/davidcruwys/dev/ad/flivideo/docs/agent-comprehension-docs.md` (the README is step 3)
**Outputs reviewed**: `README.md` in flistudio, flihub, flicut, flicast, teletubby and fli-core under `/Users/davidcruwys/dev/ad/flivideo/`

---

## 1. Verdict

- **The outputs are mostly good. The skill did not make them good; the method brief did.** Every relative link resolves (0 of about 70 broken), the scripts and ports quoted match the code, and each app README points into SYSTEM.md, AGENT-NOTES.md and (where it exists) the schema mirror, with almost no word-for-word copying.
- **The skill is out of date with its own pipeline.** It still says `system-context` writes `CONTEXT.md` and it never mentions the schema mirror. So the "point into steps 1–2" behaviour came from the runner's brief, and a cold `/craft-readme` run would not repeat it.
- **Where the outputs fail, they fail the same way:** facts copied by hand that go stale with nothing to catch them. Examples: repo visibility shown as "private", old `@flivideo/core` versions, the FliHub folder layout, a capability table missing one verb, and refusal-code tables repeated in three repos. The fix is a check the skill runs before it finishes, not better prose.

---

## 2. Findings, ranked

### HIGH

**H1. The skill contradicts `system-context`, and it has never heard of the schema mirror.**
- What is wrong: SKILL.md says `system-context` writes "the internal `CONTEXT.md`" and treats `CONTEXT.md` as the input to read and the place to defer detail to [checked: /Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/craft-readme/SKILL.md:8, :23, :25-27, :77, :117, :129]. `system-context` now writes `SYSTEM.md` + `AGENT-NOTES.md` and says outright that it does NOT own `CONTEXT.md` [checked: /Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/system-context/SKILL.md:4, :182-184]. None of the skill's files mention `SYSTEM.md`, `AGENT-NOTES` or `schema-mirror` [checked: `command grep -rn "SYSTEM\|AGENT-NOTES\|schema" SKILL.md references templates` finds only unrelated hits].
- Evidence the outputs were steered from outside: every app README links SYSTEM.md and AGENT-NOTES.md [checked: grep counts, all 5 apps ≥1], and the flicast commit message says "point into the mirror, SYSTEM and AGENT-NOTES" [checked: `git -C flicast log` c3db70e]. That wording comes from the method doc, not the skill [inferred].
- Consequence: run without the method brief, the skill would tell the agent to look for, link to and defer detail to `CONTEXT.md`, which is now either missing or a superseded April snapshot (as in FliHub) [checked: /Users/davidcruwys/dev/ad/flivideo/flihub/CONTEXT.md:38 carries the "Superseded" pointer].
- Fix: SKILL.md: replace every `CONTEXT.md` with "`docs/SYSTEM.md` (people) + `docs/AGENT-NOTES.md` (agents) from `system-context`, plus `docs/schema-mirror.md` from `schema-mirror`". Add a Phase 2 step: "if those three files exist, the README must link each of them once, in a docs table, and must not restate any schema, enum or closed set they hold." Update the description frontmatter the same way.

**H2. Repo visibility and licence claims are false, and nothing checks them.**
- FliHub README says "Access to the private `flivideo/fli-core` repo" (:44), "CI can't install the private `fli-core` dependency" (:159) and "Private repository — AppyDave. No license is granted." (:165) [checked: `git -C /Users/davidcruwys/dev/ad/flivideo/flihub show origin/main:README.md`, at 2fddba7]. FliCast README calls `@flivideo/core` "a **private** repo" [checked: /Users/davidcruwys/dev/ad/flivideo/flicast/README.md:74].
- `gh repo view` reports `flivideo/fli-core` PUBLIC and `flivideo/flihub` PUBLIC (flistudio, flicut and flicast are PRIVATE) [checked: `gh repo view <repo> --json visibility`, run 2026-09-23].
- Caveat: this check shows visibility today. It does not show when either repo changed, so the READMEs may have been true when written [not established].
- Consequence: a public FliHub repo tells visitors it is private and unlicensed, and a reader chasing the CI failure goes after an SSH-access cause that may no longer apply.
- Fix: SKILL.md Phase 2 "Gather grounding": add "confirm repo visibility (`gh repo view --json visibility`) and whether a LICENSE file exists, for this repo and every dependency the README calls private or public. State the status only after that check, or leave it out."

**H3. Version numbers written into prose are stale, even though the skill bans them.**
- fli-core README's Install block pins `"github:flivideo/fli-core#v0.1.0"` [checked: /Users/davidcruwys/dev/ad/flivideo/fli-core/README.md:21]. The package is `0.6.0` and tags run to `v0.6.0` [checked: fli-core/package.json version; `git -C fli-core tag`]. A new consumer copying it pins a version five releases old.
- FliCut README says the resolver is "on `@flivideo/core` v0.1.0" [checked: /Users/davidcruwys/dev/ad/flivideo/flicut/README.md:115], but FliCut pins `#v0.5.0` [checked: flicut/package.json].
- The skill already has the rule ("no hardcoded versions in prose", SKILL.md Phase 4; universal-principles §B "No stale version numbers"), but it is a line on a self-review list with no mechanical check behind it [checked: SKILL.md:103-108].
- Fix: fli-core/README.md:21 → `#vX.Y.Z` plus "use the latest tag (`git ls-remote --tags …`)". flicut/README.md:115 → drop the version. SKILL.md Phase 4: add a grep gate so that every `v\d+\.\d+` or `#v…` in the README must equal the manifest's version or pin, or be removed.

### MEDIUM

**M1. FliHub's folder layout went stale within a day. Since resolved on origin, but my local checkout still had the stale copy.**
- The working copy at `/Users/davidcruwys/dev/ad/flivideo/flihub` (HEAD 7a5fc7d) is **2 commits behind origin/main** (2fddba7) [checked: `git rev-parse HEAD origin/main` after `git fetch`]. Its README says takes move "into `recordings/`" and draws only the top-level legacy tree [checked: flihub/README.md:9, :111-123 in the working copy]. The code defaults new projects to `hub/recordings/` [checked: flihub/shared/paths.ts:13-19].
- The origin/main README (2fddba7, "light 3" after the trash change) fixes this: it describes both layouts and the `projectLayoutSync` rule [checked: `git diff HEAD origin/main -- README.md`].
- What this still shows: the 09-22 README went stale when fli-core v0.5.0 landed on 09-23, and only a manual re-run caught it. Also, the READMEs on the machine where agents actually work can lag the pushed version, with nothing to say so.
- Fix: none needed in the file now. Someone should pull flihub on this machine (not done: this review edits nothing). Skill: change C6 (the "last true at" stamp) would make the lag visible.

**M2. Closed sets copied by hand into READMEs, where they will drift.**
- FliStudio's "Agent door" table lists 15 capabilities. The registry has 16, and the table leaves out `apps.status` [checked: /Users/davidcruwys/dev/ad/flivideo/flistudio/README.md:40-56 vs /Users/davidcruwys/dev/ad/flivideo/flistudio/server/src/capabilities/registry.ts:50-65]. The method's own note for FliStudio says "the agent door describes itself … does not copy the capability list" [checked: agent-comprehension-docs.md, Per-repo notes].
- The refusal-code vocabulary is shared and owned by fli-core, yet it is written out again as a table in three READMEs: flihub:89-99, flicut:142-154, flicast:176-180 [checked]. It also lives in flicast/docs/open-contract.md:31-36 and fli-core/docs/schema-mirror.md:198, :761+ [checked]. That breaks the method rule "The Fli family shares contracts … Cite them; do not restate them."
- Consequence: five hand copies of one closed set, with nothing checking them. The FliStudio table was already one verb short on the day it was written.
- Fix: flistudio/README.md: replace the table with 3–4 example rows plus "full list: `bin/flistudio list` / `GET /api/capabilities`". flihub, flicut and flicast READMEs: replace each refusal table with one line and a link to `fli-core/docs/schema-mirror.md` (the OpenContextResult kinds), plus only this app's deviations ("FliHub never sends `not-a-project` or `video-not-found`"). Skill: change C2.

**M3. FliCut and FliCast READMEs are the house, not the door.**
- FliCut runs 220 lines and FliCast 221 [checked: `wc -l`]. Both sit at the skill's own ~200–300-line ceiling (SKILL.md:124), and much of what they hold is reference: FliCut has export-name semantics, legacy-edit resolution, the undo baseline and the lab tree (flicut/README.md:156-201); FliCast has a 9-row prerequisites table, the permissions procedure and a 5-client matrix (flicast/README.md:67-164).
- Verbatim overlap with SYSTEM.md is near zero (≤1% of README 8-word sequences) [checked: 8-gram overlap script, flistudio 1%, all others 0%]. So this is not duplication: the README has become the *only* home of contract detail that the method places in SYSTEM.md, open-contract.md or the mirror [inferred].
- Consequence: agents load AGENT-NOTES, not the README, so contract detail kept only in the README goes unseen by the audience the method is written for [inferred from method doc "Audience: the agents"].
- Fix: flicut/README.md:156-201 ("Where an edit's files go") → move to docs/SYSTEM.md or a docs/open-contract.md, leaving a 6-line tree and a link. Skill: change C4.

**M4. Sibling apps have no shared shape, and the suite map is patchy.**
- The section headings share nothing across the five sibling apps [checked: `grep '^## '` on each README]. flistudio: Run / Commands / Agent door / What FliStudio writes / Layout. flihub: Features / Get started / Open contract / Layout / Documentation / Development / License. flicut: Why / What makes it different / Using / Requirements / Driving / Open contract / Going deeper. flicast: Status / Shape / Install / First run / Clients / Open contract / Develop / For agents / Going deeper. teletubby: Why / What / Quick start / Docs / Setup on another machine / Related. The docs table is titled "Documentation", "Going deeper", "Docs", or is absent (flistudio uses inline bullets).
- Suite map `/Users/davidcruwys/dev/ad/flivideo/README.md`: mentioned as plain text in flistudio (:12-13) and teletubby (:144); absent from flihub, flicut, flicast and fli-core [checked: grep counts]. FliStudio chose not to make it a link on purpose, because it is cross-repo [checked: flistudio commit dee3c6b message].
- Consequence: an agent moving between apps finds "how do I run it / where are the docs / what does it open" in a different place every time.
- Fix: skill change C5 (a suite-sibling template). In each app README, add the same closing line, e.g. "Part of the FliVideo suite — map: `~/dev/ad/flivideo/README.md` (flivideo root repo)".

**M5. The skill has no shape for a private, single-creator suite app.**
- Its templates and blueprints assume public open source: logo `<picture>`, CI/stars badges, "Cloud (fastest): signup link", an SDK matrix, sponsors [checked: templates/app.md, templates/service.md; references/project-type-blueprints.md Type 1]. Nothing in the skill says "suite", "family of apps" or "private" [checked: grep, 0 relevant hits].
- The outputs sensibly ignored all of that. None has a badge or a cloud path. But that was the agent's judgment against the template, not something the skill guided [inferred].
- Fix: add a template `templates/suite-app.md` (see C5), with detection in the Phase 1 table: "one of several sibling repos sharing a contract library → suite app".

### LOW

**L1. Machine-ops runbooks in public READMEs.** Teletubby (PUBLIC) spends 42 lines on regenerating jump aliases on David's machines (rbenv, `aliases-jump.zsh`) [checked: /Users/davidcruwys/dev/ad/flivideo/teletubby/README.md:99-140]. FliHub (PUBLIC) links CLAUDE.md for its "machine inventory" [checked: flihub/README.md:137]. This is maintainer content, not front door. Fix: move it to teletubby/CLAUDE.md or AGENT-NOTES.md and leave a one-line pointer.

**L2. Cross-repo paths that do not resolve from inside the repo.** `flistudio/docs/open-contract.md` (flihub/README.md:63), "FliStudio `docs/specification.md`" (fli-core/README.md:12) and `video-as-code/project-folder-convention.md` in brains (fli-core/README.md:37) have no root and no link [checked]. On GitHub they are dead text. Fix: write them as absolute `~/dev/ad/...` paths (the convention teletubby uses) or as GitHub URLs.

**L3. (Withdrawn: a stale checkout.)** I first reported that FliHub has no mirror. That was true only of the local working copy (7a5fc7d). origin/main 2fddba7 has `docs/schema-mirror.md` + `.json`, and the README links it [checked: `git ls-tree origin/main docs`; the origin README diff]. The lesson carries into C3: a README review must run against the pushed commit, not whatever is checked out.

**L4. Licence statements do not match across siblings.** FliHub: "no license granted", no LICENSE file, public repo. FliStudio: private repo with an MIT footer. FliCast: "Private repo · MIT". Teletubby: "open-source … MIT" [checked: READMEs, `ls LICENSE*`, gh visibility]. Probably deliberate per repo, but no one confirmed the intent [inferred]. It would be covered by the H2 fix.

---

## 3. What works well — keep it

- **Links resolve.** 0 broken among about 70 relative markdown links across the six READMEs [checked: link-extract script, `os.path.exists` per link]. Every linked file is tracked in git [checked: `git ls-files` cross-check; the untracked hits were runtime paths such as `fli.studio.json`, not doc links].
- **Commands are real.** Every `npm run …` quoted exists in package.json: flistudio test/test:e2e/lint/typecheck/format:check/build, flihub test/typecheck/lint, flicast docs:check/uat/test:golden/dev:debug, fli-core test/typecheck/lint/format:check/build [checked: package.json `scripts` per repo]. FliCast says honestly that there is no `npm run lint`, which is true [checked]. CLI entry points exist: `bin/flistudio`, `bin/flicut`, `bin/teletubby.mjs` (with the `write_script` verb it uses), `bin/flicast.mjs`, `bin/flicast-mcp.mjs` [checked: `ls bin`; teletubby/src/core/handlers.ts:904].
- **Ports match the code.** FliHub 5100/5101 [checked: flihub/client/vite.config.ts:8, flihub/Procfile]; Teletubby 7110/7111 [checked: teletubby/electron.vite.config.ts:28, src/main/control-server.ts:33]; FliCut control 7121 [checked: flicut/src/main/index.ts:497]; FliCast 7130/7131 [checked: flicast/electron.vite.config.ts:27, src/main/paths.ts:40]. FliCast's "FliCut uses 5173" matches FliCut having no renderer port set (electron-vite default) [inferred: no `port` in flicut/electron.vite.config.ts].
- **Points into the three docs.** All 5 apps link SYSTEM.md and AGENT-NOTES.md. All 5 link the mirror (FliHub only at origin/main 2fddba7). fli-core correctly links only its mirror, since it is step 1 only per the method [checked: grep counts + origin diff].
- **No `CONTEXT.md` resurrected.** No app README points to a CONTEXT.md as current. FliHub's CONTEXT.md carries the superseded pointer [checked: flihub/CONTEXT.md:38]. The one CONTEXT.md mention is AppyTron's, which exists [checked: flicast/README.md:219].
- **Near-zero duplication of SYSTEM.md** (≤1% shared 8-word sequences) [checked].
- **Honest, measured claims** with a named source: FliCut's ch01 numbers → BUILD-LOG.md, FliCast's perf → docs/perf/2026-09-15.json, and FliCast's "True at `b061e5e`" stamp, which is a real commit [checked: `git cat-file -t b061e5e`]. Keep the stamp: it is the one README that says when it was last true.
- **Real hooks.** FliCut's Gling-vs-FliCut table and Teletubby's three-column diagram are strong above-the-fold proof, which is what the skill's principles ask for.

---

## 4. Proposed SKILL.md changes

- **C1 — Rename the partner docs.** Every `CONTEXT.md` → `docs/SYSTEM.md` + `docs/AGENT-NOTES.md` (from system-context) + `docs/schema-mirror.md` (from schema-mirror). Update the description frontmatter, the "external twin" paragraph, Phase 2, Phase 5 and the hard rules. Update references/universal-principles.md §C row "Internal design rationale" and references/ecosystem-and-tools.md:41, :86, :92.
- **C2 — "Point into steps 1–2" as a hard rule.** If `docs/schema-mirror.md` exists, the README must not contain a table of any enum, union, capability list or refusal set. It links the mirror or the self-describing command (`<cli> list`, `GET /api/capabilities`) and lists only this app's deviations. For a suite: a shared contract is cited in the contract library's mirror, never restated.
- **C3 — A link-and-fact gate in Phase 4** (a script, not a checklist line):
  1. every relative link and backticked repo path resolves (`test -e`);
  2. every `npm run X` / `bin/X` named exists in the manifest or the tree;
  3. every port number appears in code/config (`command grep -rn <port>`);
  4. every version string equals the manifest's version or pin, or is removed;
  5. every "private/public/licensed" claim equals `gh repo view --json visibility` plus the presence of a LICENSE file.
  6. every row in a docs table that names contents ("collaborator setup", "API reference") has a matching file in the linked folder (`ls` the folder, compare the nouns);
  7. run against `origin/main` after a `git fetch`, not a working copy that may lag.
  Fail on any miss. FliCast already has `npm run docs:check` for (1). Borrow it.
- **C4 — A home test for each section.** Before writing a section, ask: "Would an agent need this, and does it load AGENT-NOTES rather than the README?" If yes, it belongs in AGENT-NOTES/SYSTEM, and the README gets one line and a link. Keep a hard line budget (≤150 for an app in a suite), and let content that goes over move out rather than be squeezed in.
- **C5 — A suite-sibling template** (`templates/suite-app.md`), detected when a repo depends on a shared contract library with sibling repos. Fixed section order: tagline + proof → Run (`npm install`, `npm run app`, ports) → Open it on a project (link to the open contract + this app's deviations only) → Drive it (CLI/door, pointing at the self-describing list) → Docs table (SYSTEM · AGENT-NOTES · schema-mirror · spec · kdd, same titles every time) → Develop → footer with the suite-map line + licence. In Refresh mode, read one already-refreshed sibling README first and match its headings.
- **C6 — A "last true at" stamp.** Require `True at <short-sha> (<date>)` near Status, as FliCast does, so a later refresh can `git diff <sha>..HEAD` the manifest, ports and layout, and drift like M1 becomes visible.
- **C7 — Drop what does not fit** the internal-tool shape from the default path: badges, logo `<picture>`, cloud signup, SDK matrix, stars. Keep them only for the public-library and public-app shapes.

---

## 5. What I did not check

- Whether any command actually *runs*. I checked that scripts, binaries and verbs exist, not that `npm test` passes or `npm run app` starts. Nothing was executed; no app was started.
- Anchor fragments inside links (e.g. flicut `#where-an-edits-files-go`). I only reasoned that the heading matches [inferred].
- The content of the linked docs (SYSTEM.md, spec, kdd). I checked that they exist, not that the READMEs describe them accurately.
- Claims such as FliCast's "132 capabilities in 23 families", FliCut's measured ch01 numbers, and FliHub's features list beyond `/api/query` existing [checked only: flihub/server/src/index.ts references `/api/query`].
- When fli-core or flihub became public (see H2 caveat). A true-when-written "private" and a false-when-written "private" look identical from today's `gh` output.
- The skill's other templates in depth, beyond reading them. The library/CLI templates were not exercised by these outputs.
- Link and command checks were run against the **local working copies**. flistudio, flicut, flicast, teletubby and fli-core are at origin/main. FliHub is 2 commits behind, and its origin README was checked only by diff (the new schema-mirror link resolves in the origin tree; the other links are unchanged).
- The *descriptions* in docs tables, as against the link targets. My link check proved `docs/guides/` exists, not that it holds what the row claims (see Reconciliation, item 11).
- Whether David wants a shared sibling shape at all (M4/C5) is a preference call, not a defect I can prove.

---

## 6. Reconciliation (added after reading the blind-review evidence log)

Source: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/doc-skills-blind-review.md`, section "craft-readme" (items 7, 8, 11), read after sections 1–5 were on disk.

**Found independently**
- **Item 7 (still refers to CONTEXT.md)** = my H1. I also found the other half: the skill never mentions the schema mirror, and `system-context` explicitly disowns CONTEXT.md (system-context/SKILL.md:182-184). That explains *why* the outputs pointed into steps 1–2 anyway: the method brief did it, not the skill.

**Missed**
- **Item 11 (invented a doc: "collaborator setup" guide).** It was in the working copy I read (flihub/README.md:135, "Troubleshooting, cross-platform and collaborator setup"), and I did not flag it. My link check proved `docs/guides/` exists. It could not see that the row *describes* a guide that is not there (the folder holds cross-platform-setup, release-process, troubleshooting, wsl-development-guide) [checked: `ls flihub/docs/guides`]. A resolving link is not a true description, so I added gate item 6 to C3. It is fixed at origin/main 2fddba7 ("Troubleshooting, cross-platform and WSL setup, release process") [checked: origin diff].

**Disputed / qualified**
- **Item 8 ("fli-core's README linked its mirror 0 times").** No longer true: fli-core/README.md:67 links `docs/schema-mirror.md` [checked], added in 805f8c5 (the log's own Runs table says the same). As a statement about the *skill* it stands, since the skill has no instruction to link a mirror (H1). As a statement about the current output it is stale.
- **Item 11's framing, "the skill's self-review did not catch a dead link."** It was not a dead link: `docs/guides/` resolves. It was a false description behind a live link, which a link checker (the fix the phrase implies) would also miss. The needed gate is a contents check (C3.6), not only a link check.

**Mine, not in the log**
- H2: repo visibility and licence claims contradict `gh` (fli-core and flihub are PUBLIC; the READMEs say private).
- H3: stale versions written into prose: fli-core's Install pins `#v0.1.0` (current v0.6.0); FliCut says core v0.1.0 (pins v0.5.0).
- M2: hand-copied closed sets. FliStudio's capability table leaves out `apps.status`, and the shared refusal-code table is restated in three READMEs, against the method's "cite, do not restate".
- M3: FliCut and FliCast READMEs (≈220 lines) hold contract detail found nowhere else, so agents that load AGENT-NOTES never see it.
- M4/M5/C5: no shared sibling shape across the five apps; the suite-map pointer is in only 2 of 6; the skill has no suite or internal-tool template.
- M1 (resolved on origin): FliHub's layout went stale the day after its refresh, and the local checkout on this machine still lags origin by 2 commits. The lag is a finding in itself: the log records the run as "landed", which is true of the remote, not of the working copy.
- L1: machine-ops runbook (jump aliases) in the public Teletubby README. L2: cross-repo relative paths that are dead on GitHub.
