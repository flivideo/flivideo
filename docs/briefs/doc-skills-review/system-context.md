# Review: `dev-team:system-context`, judged by what it produced

Reviewer: independent subagent, 2026-09-23. Scope: the skill at
`/Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/system-context/` and its ten outputs in
flistudio, flihub, flicut, flicast and teletubby. Evidence tags: `[checked: …]` means read or run by
me; `[inferred]` means reasoned, not observed.

## 1. Verdict

- **The content is mostly true and useful.** In the four repos written after the schema mirror existed,
  every AGENT-NOTES claim I sampled matched the code (about 30 claims across 4 repos). The "derivation
  test" idea produces real pitfalls, not a restatement of the directory tree.
- **The skill as written did not produce these outputs.** Its location (`context/` or `.context/`),
  its loading method (`CLAUDE.local.md`, "never touch CLAUDE.md") and its frontmatter (no commit) were
  all replaced by the method doc. One repo (Teletubby) ended up with its notes not loaded at all.
- **Nothing keeps the files true.** There is no commit stamp in the template, no staleness check,
  no line/size gate and no ban on hand-typed `file:line`. FliHub's loaded notes went wrong within 6
  hours of being written. They stayed wrong for about 25 hours, through 6 edits, until a full re-run
  replaced them (2fddba7). The M4 checkout, 2 commits behind, still loads the broken copy.

## 2. Findings, ranked by severity

### HIGH

**H1. The skill and the method doc disagree on where the files go and how they load. The skill was never updated.**
- What's wrong: SKILL.md writes to `context/` or `.context/`, loads through `CLAUDE.local.md`, and
  says "Do not modify `CLAUDE.md`" [checked: SKILL.md:210-231, :553-564, :589-617]. The method puts the
  files in `docs/` and adds an `@docs/AGENT-NOTES.md` line to `CLAUDE.md` [checked:
  /Users/davidcruwys/dev/ad/flivideo/docs/agent-comprehension-docs.md:30 and "Done when" #2]. SKILL.md
  was last changed 2026-09-07, before the method existed [checked: `git log` → 115fff3 2026-09-07].
- Evidence: every run passed `docs/` as an override. FliCast's SYSTEM.md even says so:
  `regenerate: "Run dev-team:system-context with <ctx> = docs/ …"` [checked:
  /Users/davidcruwys/dev/ad/flivideo/flicast/docs/SYSTEM.md:87]. None of the 5 repos has a
  `CLAUDE.local.md` [checked: `ls` in all 5].
- Consequence: a later `/system-context` run, without the method doc in its prompt, follows SKILL.md.
  It will create `.context/`, write a machine-local `CLAUDE.local.md`, and leave the `docs/` copies to
  go stale next to it [inferred].
- Fix: SKILL.md: add an **owned-repo mode** as the default for repos David owns. That mode writes
  `docs/SYSTEM.md` + `docs/AGENT-NOTES.md` and makes sure `CLAUDE.md` contains
  `@docs/AGENT-NOTES.md`. Keep `.context/` + `CLAUDE.local.md` only as a third-party mode, picked
  when the git remote is not David's. Delete the duplicated "Output Location" table (it appears twice:
  :214 and :523).

**H2. Teletubby's AGENT-NOTES is never loaded.**
- What's wrong: `/Users/davidcruwys/dev/ad/flivideo/teletubby/CLAUDE.md` (656 lines) and `AGENTS.md`
  contain no reference to `AGENT-NOTES` [checked: `command grep -c AGENT-NOTES` → 0 and 0]. There is
  no `CLAUDE.local.md` either.
- Consequence: the five pitfalls and three decisions in that file (for example, the reserved
  `<project>-scripts` id and the `onReady`/`activate` trap) reach no agent. The only file meant for
  agents is the one agents never see.
- Fix: add `@docs/AGENT-NOTES.md` to Teletubby's CLAUDE.md. In SKILL.md, add a closing check that
  **fails the run** when the import line is missing from whatever file the chosen mode loads.

**H3. FliHub's loaded notes carried hand-typed line numbers that went wrong the same day.**
- *Correction after reconciliation:* I reviewed the local checkout
  `/Users/davidcruwys/dev/ad/flivideo/flihub`, which is `main...origin/main [behind 2]`
  [checked: `git status -sb`]. `origin/main` at 2fddba7 (2026-09-23 11:05) has a refreshed
  AGENT-NOTES (114 lines, `commit: ae2d9b1`, no line anchors) and a SYSTEM.md with no anchors and
  relay/sync marked as removed [checked: `git show origin/main:docs/…`]. The history below is still
  accurate. The damage was about 25 hours of wrong anchors, fixed by a full re-run, not by any check.
  The local checkout still serves the old copy to every agent session opened there. Nothing in the
  skill or the method notices that the working copy's notes are behind the ones pushed.
- What's wrong: `/Users/davidcruwys/dev/ad/flivideo/flihub/docs/AGENT-NOTES.md:18-19` lists
  `Config :190, ProjectStage :438, DEFAULT_PROJECT_STAGES :455, ProjectStats :496, socket events
  :660/:705, ProjectState :1181`. At HEAD they are at :28, :263, :280, :322, :486/:529 and :1005
  [checked: `command grep -nE` on shared/types.ts]. That makes 7 of the 8 anchors wrong (only
  `NAMING_RULES :16` still holds).
- Timeline: correct when written at c57ff0a (2026-09-22 10:12). Broken at 19ddd05 (15:51, the
  relay/sync removal). Since then AGENT-NOTES was edited 6 more times, including 49894aa, which
  updated the notes *for* 19ddd05, and nobody fixed the anchors [checked: `git show c57ff0a:shared/types.ts`,
  `git log c57ff0a..HEAD -- docs/AGENT-NOTES.md`].
- SYSTEM.md has the same problem: `types.ts:1181`, `:438`, `holdUtils.ts:11`, `configManager.ts:121`
  (now 114), `hold.ts:93`, `storage.ts:185` and `storageTree.ts:24` no longer point at the thing named
  [checked: `sed -n` on each].
- Consequence: a line number looks precise, so an agent trusts it and reads the wrong code. This is
  the "wrong is worse than missing" case the skill itself cites (SKILL.md:37-38).
- Fix: SKILL.md: **ban `file:line` in both files.** Cite a symbol (`ProjectState` in `shared/types.ts`)
  or point at the schema mirror, whose anchors can be checked. Add a gate: any match for
  `\.(ts|tsx|js|py|rb):[0-9]+` or `` ` :[0-9]+ `` fails the run.

**H4. FliHub SYSTEM.md described deleted code for a day. (Fixed on origin/main by 2fddba7; still present in the local M4 checkout.)**
- What's wrong: it has a whole workflow "Hand a project to an editor machine (relay …)" citing
  `server/src/routes/relay.ts`, plus failure modes "Sync push commits everything" and "Stale sync
  status" citing `sync.ts` [checked: flihub/docs/SYSTEM.md, Key Workflows + Failure Modes]. Four of
  its `sources` no longer exist: `routes/relay.ts`, `routes/sync.ts`, `RelayTool.tsx`, `SyncTool.tsx`
  [checked: existence loop over the `sources` list]. It also says "There is **no schema mirror** …
  `/dev-team:schema-mirror` has no TypeScript extractor". The TS extractor shipped 2026-09-22 10:35
  (89ca58a), 23 minutes after this file was written [checked: plugins `git log`].
- The loaded AGENT-NOTES repeats that claim ("there is no mirror", AGENT-NOTES.md:13-15). FliHub is
  the only one of the five repos with no `docs/schema-mirror.*` [checked: `ls docs`].
- SYSTEM.md was last touched at c57ff0a, 9 commits ago [checked]. It has no `commit:` stamp, so
  nothing marks it as stale.
- Consequence: agents are told to skip a tool that now works. Humans reading SYSTEM.md learn about a
  relay lane that no longer exists.
- Fix: in the repo, run the mirror step, then refresh both files. In SKILL.md, a refresh must check
  that every `sources:` path still exists and treat any missing path as a forced refresh. The skill's
  own "Re-read files in the existing `sources` list" step (:238) has no gate behind it.

### MEDIUM

**M1. The template has no commit stamp, and nothing checks staleness.**
- Template A/B frontmatter has only `generated` / `status` [checked: SKILL.md:271-281, :337-344].
  Four of the five runs added `commit:` on their own initiative (flistudio 81d909a, flicut d992f4d,
  flicast b061e5e, teletubby 806729c). FliHub has none in the local checkout
  [checked: frontmatter of all 10]; on origin/main it has `commit: ae2d9b1` (see the H3 correction).
- Where a stamp exists, it works: `git log <commit>..HEAD` shows 3 / 2 / 3 / 2 commits since
  [checked]. But nothing runs that check. The trigger "is the context stale" (SKILL.md:11) has no
  procedure behind it.
- Fix: add `commit: <short sha of HEAD at generation>` to both templates. Add a `staleness` step: list
  the commits since the stamp that touch any `sources:` path, and if there are any, report the file
  as stale.

**M2. The size limit counts lines, so long lines get around it, and nothing enforces it.**
- FliCast AGENT-NOTES is 190 lines and **16,661 bytes** (about 4k tokens, loaded every session).
  FliStudio's is 90 lines / 6.3 KB and Teletubby's 54 lines / 2.8 KB [checked: `wc -l`, `wc -c`].
  Many FliCast lines run well past 120 characters (e.g. :50-56 is a single 7-line bullet).
- The skill's only limit is "well under 200 lines" / "if it approaches 200 … cut" [checked:
  SKILL.md:24, :129, :392]. 190 is "approaching", yet the file shipped.
- Fix: SKILL.md: set the limit in bytes (for example ≤ 8 KB) as well as lines, and wrap at 110
  columns. Add a check command to the Quality Checks section.

**M3. Notes about sibling docs and other tools go stale fastest.**
- Teletubby AGENT-NOTES:16-17 says "Never `npm run dev`: the README still shows it". The same commit
  (9015c03, step 3) removed `npm run dev` from README [checked: `git show 9015c03 -- README.md`]. So
  the note was false when it was committed.
- Teletubby SYSTEM.md (last failure mode) and AGENT-NOTES:23 say the mirror's "Cannot be mirrored:
  Nothing" is wrong. One minute later (deef359) the mirror page was hand-corrected [checked:
  `git log` + schema-mirror.md:1101]. So SYSTEM.md's "It still reports … Nothing" is now false.
  Also, a hand edit to a generated page will be lost the next time the mirror is regenerated [inferred].
- FliCut AGENT-NOTES:17-19 and SYSTEM.md describe the same extractor defect. That is true today
  [checked: extract_typescript.py has no `@appydave/core` handling], but it becomes false as soon as
  the extractor is fixed.
- FliCast AGENT-NOTES:80-81 points into `~/dev/ad/brains/ARTIFACTS.md`, and :68-69 into the plugin
  repo. Both are cross-repo facts that no check in this repo covers.
- Fix: SKILL.md: add a fifth "does not qualify" rule. Nothing about another tool's defects or another
  file's current content. Link to the tracking ticket or file instead. Run step 2 **after** step 3
  (README), or re-check AGENT-NOTES once README is written.

**M4. `context.globs.json` goes where its only reader never looks.**
- SKILL.md:404 says write `<ctx>/context.globs.json` "so `query_apps` can discover" it. `query_apps`
  only reads `<repo>/context.globs.json` at the repo root [checked:
  /Users/davidcruwys/dev/ad/appydave-tools/lib/appydave/tools/app_context/app_finder.rb:51,
  globs_loader.rb:93].
- flistudio, flicut, flicast and teletubby wrote `docs/context.globs.json` [checked: `ls`], so
  `query_apps` cannot see them. FliHub's root copy (from April, updated since) is the only one it can
  find.
- Fix: either write the file to the repo root, or change `query_apps` to also check `docs/` and
  `context/`. Until one of those happens, stop calling this output "for query_apps".

**M5. SYSTEM.md and AGENT-NOTES duplicate each other by design, so each fact can drift in two places.**
- The skill fills AGENT-NOTES from SYSTEM dimensions 4, 5 and 8 (SKILL.md:105-108). So each pitfall
  exists twice. FliCut: placeholder clips / `dropPlaceholderClips`, the `HOME` override and
  `DEEP_FILTER_BIN`, the audit-mode reset, `.default()` on settings and the 7121 re-bind all appear in
  both [checked: both files]. FliHub shows the cost: both copies went stale together (H3/H4).
- Fix: SYSTEM.md sections 5 and 8 should link to the AGENT-NOTES entry rather than repeat it, or
  AGENT-NOTES should be the only home of the imperative form, with SYSTEM.md keeping only the story.

**M6. CLAUDE.md contradicts AGENT-NOTES, and no check compares them.**
- FliStudio CLAUDE.md "Hard rules" says "FliStudio writes only `fli.studio.json` and placed exports"
  [checked: flistudio/CLAUDE.md]. AGENT-NOTES (loaded right below it) documents `project.rename`,
  `project.migrate-layout` and `project.empty-trash`, all of which move or delete files [checked:
  AGENT-NOTES.md:71-86; handlers exist in `server/src/capabilities/`].
- Teletubby AGENT-NOTES:11 says "nothing CLAUDE.md already says", then repeats "never `npm run dev`",
  which is already in CLAUDE.md:459 [checked].
- Fix: the skill's check "Nothing duplicated from CLAUDE.md" (:399) should also cover *contradicted*.
  On refresh, list any CLAUDE.md rule that the new notes contradict, as a finding for the human.

### LOW

**L1. Machine-specific rules sit in committed files.** "On this machine bare `grep -r` is shimmed" (FliStudio
AGENT-NOTES:22), "on the M4" (FliCast :34), "David works on this machine with Claude sessions in iTerm
tabs" (FliCut :52-53) [checked]. These are true on the M4, false for Jan's or Mary's clones [inferred],
and are per-person rules, not repo facts. Move them to the user-level CLAUDE.md.

**L2. SYSTEM.md restates counts that drift.** "9,191 lines", "132 capabilities in 23 families", "Ten ★
verbs" (FliCast SYSTEM.md). They are accurate today [checked: `wc -l` = 9191, HUMAN_ONLY = 10,
defineCapability = 132], but the page itself says it never restates shapes. The test file already pins
the count, so cite the test rather than the number.

**L3. The skill's claims about outside tools and papers have no source.** It cites "ETH Zurich (2026)
… −0.5% SWE-bench Lite", "grill-with-docs (624K installs)" and what `/doctor` now proposes
(SKILL.md:34-41, :195). None of them links to a primary source [checked: SKILL.md]. I did not verify
them [not checked].

**L4. The skill says it has references/templates/scripts. It has none.** The skill is a single
661-line SKILL.md [checked: `find`]. Its bootstrap, globs generation and quality checks are all prose,
so every gate depends on the agent remembering to run it. That is why H2, H3 and M2 got through.

**L5. The FliStudio import is inline.** `- Agent notes (…— loaded): @docs/AGENT-NOTES.md · human
narrative…` (flistudio/CLAUDE.md:13). I did not confirm that Claude Code resolves an `@` import in the
middle of a bullet [not checked]. FliCut and FliCast put it on its own line.

## 3. What works well and must be kept

- **Splitting by audience.** SYSTEM.md (for people, not loaded) and AGENT-NOTES (for agents, loaded).
  Every repo kept to it.
- **The derivation test and the four qualifying categories.** The resulting notes are real traps that
  checked out against the code. Examples:
  - FliStudio: `npm run test:e2e` builds first and the e2e harness runs `server/dist`
    [checked: package.json:17, e2e/global-setup.ts:96]; the 90% line threshold
    [checked: server/vitest.config.ts:17]; `FLISTUDIO_NO_REVEAL` [checked: server/src/index.ts:55];
    `lstat` before rename [checked: identity.ts:249].
  - FliCut: port 7121, the 0600 `control.json`, exit codes 2/3, `EPSILON = 1e-6`, `recordLocked`,
    `inverseCuts: false` on open, `z` from `@appydave/core` [all checked, src/main/*, src/shared/*].
  - FliCast: `@flivideo/core#v0.4.1`, 132 `defineCapability`, UAT port 9333, `notChosen: -32048`,
    no workflows in `.github` [checked].
  - FliHub: the router mount order hold → storage [checked: server/src/index.ts:308/312];
    `machineRole` still saved but nobody reads it [checked]; promotion always writes `.mov`
    [checked: shared/naming.ts:352].
- **Linking to the schema mirror instead of retyping shapes.** Where a mirror existed, SYSTEM.md
  contained zero hand-typed line anchors (0 in flistudio, flicut, flicast and teletubby vs 10 in
  flihub) [checked: `command grep -oE` count].
- **"Never scaffold."** No empty sections found.
- **The "What changed" diff on refresh, with a reason for every removal.** Keep it, and make it list
  deleted `sources`.
- **Recording decisions with their date and who made the call** (e.g. "David rejected … 2026-09-22").
  This is the part no code can recover.

## 4. Proposed SKILL.md changes

1. **Triggers:** add "refresh agent notes", "are the agent notes stale", "check AGENT-NOTES". Give
   "is the context stale" a real procedure (see 5).
2. **Modes, decided first:**
   - *owned* (the default when `git remote` is under `flivideo/`, `appydave/` or `klueless-io/`, or
     `CLAUDE.md` is tracked): write `docs/`, add `@docs/AGENT-NOTES.md` to `CLAUDE.md` on its own line.
   - *third-party*: write `.context/`, add `.git/info/exclude`, load through `CLAUDE.local.md`.
   - Remove the "never modify CLAUDE.md" rule for owned mode, and remove the duplicated
     two-folder section.
3. **Templates:** add `commit:` to both frontmatters. In SYSTEM.md, sections 5 and 8 link to the
   AGENT-NOTES entry for any trap already there.
4. **Content bans (added to the cut list):**
   - no `file:line`;
   - no counts copied from code;
   - no statements about another tool's defects or another file's current content;
   - no machine-specific rules;
   - nothing that contradicts CLAUDE.md.
5. **Gates, as a shipped `scripts/check_context.py`:**
   - AGENT-NOTES ≤ 150 lines **and** ≤ 8 KB;
   - no `\.(ts|tsx|js|mjs|py|rb):\d+`;
   - every `sources:` path exists;
   - the import line is present in the loading file;
   - `commit:` is present, with a count of the commits since it that touch `sources:` paths
     (that count is the staleness answer).
   - A non-zero exit fails the run.
6. **Order:** state that when `schema-mirror` exists for the stack, it runs first; and that
   AGENT-NOTES is re-checked after README is refreshed.
7. **`context.globs.json`:** write it where `query_apps` reads it (the repo root), or fix
   `query_apps` first.
8. **Put the rationale on a diet:** move the evidence and history paragraphs (ETH, MITRE, `/doctor`,
   the CONTEXT.md naming story) into `references/rationale.md`, with source links.

## 5. What I did not check

- Whether Claude Code resolves an inline `@path` in the middle of a bullet (FliStudio CLAUDE.md:13).
- The ETH / MITRE / `/doctor` / install-count claims in SKILL.md.
- Whether each `context.globs.json` glob matches files. I only read the `context` and `narrative` keys.
- Whether `verify_mirror.py` still passes on Teletubby after the hand-edit to schema-mirror.md.
- Runtime behaviour. I read the code only: no app was started and no tests were run. The `[inferred]`
  failure modes in FliHub SYSTEM.md (for example the shadowed Hold route) were not reproduced.
- About 25 of FliCast's roughly 60 AGENT-NOTES claims, and most SYSTEM.md workflow steps in all five
  repos. I sampled 6–12 claims per app.
- fli-core. It is out of scope and has no SYSTEM/AGENT-NOTES.

## 6. Reconciliation

(Added after reading `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/doc-skills-blind-review.md`.)

**Its system-context items that I found independently**
- #3, no `commit:` in the templates → my M1. I agree.
- #4, the line limit is not enforced → my M2. I agree. I add that 190 lines is still 16.6 KB, so a
  line limit alone can be gamed with long lines.
- #5, third-party defaults contradict the method → my H1. I agree, and I rate it higher: it is why
  Teletubby's notes are unloaded (H2).
- #6, facts about other skills go stale → my M3 and H4. I only saw it in FliHub's local copy. The
  log says three AGENT-NOTES carried it; the other two were already corrected when I read them.
- #10, hand-written anchors drift → my H3. Same example (`ProjectStage :438`). The log says it moved
  to :274; I measured :263 at local HEAD. The two measurements were taken at different commits, so
  both can be right.
- Teletubby's missing `@docs/AGENT-NOTES.md` (mentioned in the log's Runs table) → my H2.

**What I missed or got wrong**
- **FliHub was re-run on `origin/main` (2fddba7).** My checks ran against the M4's local checkout,
  which is 2 commits behind. On origin, H3 and H4 are already fixed. I corrected both inline. What
  still holds: about 25 hours of drift that no check caught, and a local checkout that still loads
  the stale notes.
- I did not look at how `--exclude 'shared/*.d.ts'` interacts with the mirror (the log's schema-mirror
  #9). That belongs to schema-mirror's review, not this one.

**Where I disagree**
- None of the log's items is wrong. On #10, the log's fix is "point to the mirror". I would go
  further: ban `file:line` in both files with a mechanical gate. Pointing to the mirror only helps
  where a mirror exists, and FliHub had none for its first 25 hours.

**What I found that the log does not have**
- H2 as a skill defect: the skill has no final check that the import line exists, so an unloaded
  AGENT-NOTES passes silently.
- M3 examples beyond the extractor:
  - Teletubby's "README still shows `npm run dev`" was false in the same commit;
  - Teletubby SYSTEM.md's "still reports Nothing" became false one minute later;
  - FliCast points into `brains/ARTIFACTS.md` and the plugin repo.
  - The skill needs a rule to re-check AGENT-NOTES after step 3.
- M4: `context.globs.json` is written to `docs/`, but `query_apps` only reads the repo root
  (`app_finder.rb:51`). Four of the five are invisible to their only consumer.
- M5: SYSTEM.md and AGENT-NOTES duplicate pitfalls by design, which doubles the drift surface.
- M6: CLAUDE.md contradicts AGENT-NOTES in FliStudio ("writes only `fli.studio.json`…" vs
  rename/migrate/empty-trash).
- L1: machine-specific rules (the M4 grep shim, "this machine") are committed into repos Jan and Mary
  will clone.
- L4: the skill ships no scripts, references or templates, so every gate is prose.
- Local vs pushed: a stamp on the pushed copy says nothing about the copy an agent actually loads.
  A staleness check should run against the working tree's `HEAD`, and should also warn when the
  tree is behind `origin`.

**Not re-checked after reading the log**: I did not `git fetch` any repo, so "up to date with origin"
for flistudio, flicut, flicast and teletubby rests on the last fetch those clones did.
