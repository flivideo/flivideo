# Review: dev-team:schema-mirror

Reviewer: independent subagent, 2026-09-23. Judged on what the skill produced in six Fli repos, not on what its docs claim.
Skill: `/Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/schema-mirror/` (every file read in full).
Scripts were run read-only. Extraction output went to `/private/tmp/claude-501/sm-review/`, and the mutation tests ran on a
scratch copy of fli-core at `/private/tmp/claude-501/sm-review/mut/fli-core`.

## 1. Verdict

- **Partly fit.** It is accurate where it reads: every anchor resolves, sampled fields match the source, and verify catches real drift.
- **Not fit as a completeness claim.** It silently drops whole families of schemas. In FliCut and Teletubby that includes every zod schema. The page still says the gaps are only what it lists, and verify still exits 0.
- **Fix the zod detection and add a "declared but not read" census, and it is fit.** Until then, treat the page as a partial index, not as the full schema.

## 2. Findings, ranked

### HIGH-1: zod is detected by import string, so a re-exported `z` makes every schema vanish silently
- **What's wrong:** `zodLocals()` only counts `z` as zod when the import is literally from `'zod'` or `'zod/...'` [checked: /Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/schema-mirror/scripts/extract_typescript.mjs:204]. If a file gets `z` from another package, `zs.size === 0` and no schema in that file is looked at (`:1131`, `:1142`, `:1147`).
- **Evidence:**
  - FliCut takes `z` from `@appydave/core` in 6 files [checked: /Users/davidcruwys/dev/ad/flivideo/flicut/src/shared/project.ts:18]. All 22 top-level zod schemas are missing from the mirror, including the project file model: `elementSchema`, `takeSchema`, `mediaSchema`, `clipSchema`, `timelineSchema`, `cutParamsSchema`, `cutLabelSchema`, `resolutionSchema` and `audioProfileSchema` [checked: /Users/davidcruwys/dev/ad/flivideo/flicut/src/shared/project.ts:25-134 against docs/schema-mirror.json, via /private/tmp/claude-501/sm-review/inv.py].
  - Teletubby takes `z` from `@appydave/core` in 5 files. All 20 zod schemas are missing, including `paragraphSchema`, `projectFileSchema` and the input shapes [checked: /Users/davidcruwys/dev/ad/flivideo/teletubby/src/shared/domain-schema.ts:14].
  - FliCast has one such file [checked: /Users/davidcruwys/dev/ad/flivideo/flicast/src/main/ipc-router.ts]. It has no top-level schemas, so nothing was lost there.
- **Consequence:** FliCut's page lists one gap (Python scripts) and says nothing about zod [checked: /Users/davidcruwys/dev/ad/flivideo/flicut/docs/schema-mirror.md:1414-1420]. Teletubby's generated page says "Nothing. Every closed set and shape in scope resolved" (see HIGH-2). An agent reading FliCut's mirror would conclude the app has no validated project schema.
- **Fix:** in `extract_typescript.mjs:zodLocals`, resolve each imported binding with the checker. Follow `getAliasedSymbol` through re-exports, and treat the binding as zod when its declaration's source file sits under a `zod` package in `node_modules`. Keep the string match as a fast path. Add a fixture where `z` is re-exported through a local module and through a package, in `scripts/tests/fixtures/ts-sample`. Separately, have `detect_stack.py` look for the zod signal in workspace `package.json` files and lockfiles, not just the root. FliStudio uses zod in 10 files but `detect_stack` shows no zod row, because zod is declared in `shared/package.json` [checked: `python3 detect_stack.py /Users/davidcruwys/dev/ad/flivideo/flistudio`].

### HIGH-2: completeness claims are false, and nothing in the pipeline can tell
- **What's wrong:** the "Cannot be mirrored" table and the gap count only list things the extractor *tried and failed* to read. Declarations it never recognised produce no entry. When the list is empty, the renderer prints "Nothing. Every closed set and shape in scope resolved to an authority in the source." [checked: /Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/schema-mirror/scripts/render_mirror.py:143].
- **Evidence:**
  - Teletubby's JSON has 0 unresolved entries while 20 zod schemas are missing [checked: /Users/davidcruwys/dev/ad/flivideo/teletubby/docs/schema-mirror.json, `len(unresolved)=0`].
  - Silently dropped top-level declarations, with no gap recorded:
    - FliStudio: `type View` (a literal union plus template literals) [checked: /Users/davidcruwys/dev/ad/flivideo/flistudio/client/src/screens/ProjectHome.tsx:22-30]; the schema aliases `ProjectsListInput = BrandInput` and `ProjectGetInput = ProjectInput` [checked: /Users/davidcruwys/dev/ad/flivideo/flistudio/shared/src/contracts.ts:150,162].
    - Teletubby: `CapabilityName = (typeof CAPABILITIES)[number]['name']`, the app's capability vocabulary, built by `query(...)` helpers [checked: /Users/davidcruwys/dev/ad/flivideo/teletubby/src/shared/capabilities.ts:338].
    - FliCast: `Quality = keyof typeof QUALITY_K` and `ClickSoundName` [checked: /Users/davidcruwys/dev/ad/flivideo/flicast/src/core/export/presets.ts:16, src/core/audio/click-sounds.ts:15].
  - Classes are never read (FliCut 15, Teletubby 15, FliCast 11). The page never says so; only `references/adding-a-stack.md` does.
  - Grep census of top-level `type` aliases missing with no gap: FliStudio 13, FliCut 19, FliCast 16, Teletubby 23, fli-core 5. Many are legitimately function types or generics, but none is disclosed [checked: /private/tmp/claude-501/sm-review/inv.py over each repo].
- **Consequence:** this is the failure mode the skill itself calls "worst" (SKILL.md step 1): a partial mirror that reads as complete. The operator in Teletubby noticed and hand-edited the page (see MED-1). The FliCut operator did not notice.
- **Fix:** add a census pass to `extract_typescript.mjs:extractFile`. For every top-level `interface`, `type`, `enum`, `class`, and every `const` whose initializer is a call or identifier, the extractor must either emit an entry or push an `unresolved` entry (`subject`, `reason: "declared but not read: <construct>"`). In `render_mirror.py`, replace the "Nothing." sentence with counts: "N top-level declarations; M mirrored; K listed below". Also print a fixed "Never read by this extractor" list on every page: classes, mapped and generic aliases, template-literal unions, schemas built inside functions.

### HIGH-3: verify cannot detect any of the misses above, and it ignores stale anchors
- **What's wrong:** `verify_mirror.py` re-runs the same extractor and diffs the output [checked: /Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/schema-mirror/scripts/verify_mirror.py:28-49]. A construct the extractor cannot see is invisible to verify too. `_index` also drops anchors, so shifted line numbers are not reported.
- **Evidence** (mutation tests on the scratch copy of fli-core):
  - **Positive control:** adding `export const Ctl = z.object(...)` in a file importing from `'zod'` → verify reports it as NEW.
  - Adding a schema whose `z` is re-exported through `./zz` → no difference reported.
  - Adding `type View = 'a'|'b'|\`x:${string}\``, `export const AppFileAlias = AppFile`, a class with a literal-union field, and `Pick<>` → no difference reported.
  - Inserting 3 lines at the top of `src/identity.ts` → verify reports no new difference. Yet `validate_ir` on the committed IR then fails ("anchor src/identity.ts:30 does not contain 'schema'").
  - [checked: commands run against /private/tmp/claude-501/sm-review/mut/fli-core]
  - The one baseline diff in that copy came from my symlinked `node_modules`, which changes a `Pick (node_modules/typescript/lib/lib.es5.d.ts)` label. That makes the next point real: those labels depend on the environment.
- **Consequence:** the method's "done when: verify exits 0" [checked: /Users/davidcruwys/dev/ad/flivideo/docs/agent-comprehension-docs.md:74] passed on FliCut and Teletubby while their core schemas were missing. After an unrelated edit, the page can cite wrong line numbers while verify says OK.
- **Fix:**
  - In `verify_mirror.py:main`, also run `ml.validate_ir(old, root)` on the committed IR and fail if it reports anything. That catches stale anchors cheaply.
  - Diff the census counts from HIGH-2, so a new unread declaration counts as drift.
  - Compare the committed `.md` against `render(old)` (see MED-1).
  - In `extract_typescript.mjs:refsIn`, label TS lib types (`lib.*.d.ts`) as built-ins, not by file path.

### MED-1: the committed page can diverge from the JSON, and one already has
- **Evidence:** Teletubby's `.md` carries a hand-written correction ("Hand-corrected 2026-09-23. The generator says 'Nothing', and that is wrong") that is not in the JSON. The same page header still says "Do not hand-edit", and its summary table says `gaps 0` [checked: /Users/davidcruwys/dev/ad/flivideo/teletubby/docs/schema-mirror.md:1099-1109, and diff against a fresh `render_mirror.py` of its JSON: 11 lines differ]. The other four repos' pages match a fresh render exactly [checked: same diff, 0 lines].
- **Consequence:** the next regeneration erases the only disclosure of HIGH-1 in Teletubby, and verify will not warn. The skill gives the operator no legitimate way to record a gap they found by hand.
- **Fix:**
  - `verify_mirror.py`: add `--md <path>` (default: the JSON path with `.md` in place of `.json`). Fail when it differs from `render(old)` once volatile lines are masked.
  - Add a sanctioned input, `docs/schema-mirror.known-gaps.json` (subject, reason, looked_at). `extract_typescript.py` merges it into `unresolved` and marks those entries `source: operator`, so a person can record a gap without editing generated output.
  - SKILL.md step 3: state that this is the only allowed channel.

### MED-2: `.d.ts` build output is in scope by default, which creates duplicate ids
- **Evidence:** FliHub keeps `shared/*.d.ts` build output in git next to the `.ts` source [checked: `git -C /Users/davidcruwys/dev/ad/flivideo/flihub-aspect ls-files 'shared/*.d.ts'`]. Its committed mirror needed a manual `--exclude shared/*.d.ts` [checked: /Users/davidcruwys/dev/ad/flivideo/flihub-aspect/docs/schema-mirror.json scope]. Without that exclude the extractor emits 486 structures, 117 of them under duplicate ids, because `fileId` strips `.d.` so `types.d.ts` and `types.ts` share an id, and 152 anchor into `.d.ts`. The gate passed [checked: /private/tmp/claude-501/sm-review/flihub-nodts.json]. `verify._index` keys structures by id, so the duplicates collapse and one copy hides the other.
- **Fix:**
  - `extract_typescript.py`: add `*.d.ts` to `DEFAULT_EXCLUDES`, except files containing `declare module` or `declare global`, or at least any `.d.ts` that has a sibling `.ts`/`.tsx`.
  - `mirror_lib.validate_ir`: reject duplicate structure and closed-set ids.
  - `extract_typescript.py`: also exclude `scripts/e2e-*`, `*testing.ts` and `*/scripts/*` by default, or say in the page that they are included. FliCut's mirror includes `scripts/e2e-*.ts` [checked: /Users/davidcruwys/dev/ad/flivideo/flicut/docs/schema-mirror.json anchors] and FliCast's includes `src/core/testing.ts`.

### MED-3: the gate is weaker than SKILL.md says
- **What SKILL.md claims:** the gate "opens every anchor and checks the value is actually on that line", which makes hand-typing mechanically blocked.
- **What the code does:** fields and members pass on a *substring* match, and structure anchors are not checked against their name at all [checked: /Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/schema-mirror/scripts/mirror_lib.py:132-147].
- **Evidence:** on the scratch IR I added all of the following, and `validate_ir` returned `[]`:
  - a fake member `'e'` to `ProjectShape`
  - a duplicate member
  - a fake field `'s'`
  - a changed field type
  - an invented structure at `src/identity.ts:1`
  - [checked: python run against /private/tmp/claude-501/sm-review/mut/fli-core]
- **Consequence:** what actually stops hand-typing is verify's re-extraction [inferred from verify_mirror.py:_index], not the gate. SKILL.md and derivation-gate.md overstate the gate.
- **Fix:** `mirror_lib.check_anchor`:
  - match on token boundaries (`\b` / quote-delimited for string members)
  - require the structure's last id segment on its anchor line
  - reject duplicate members
  - Then reword SKILL.md "The gate" to say what it guarantees: the value is legible at the anchor. It does not guarantee the value is correct.

### MED-4: the page is hard for an agent to use at size, and it drops what the extractor read
- **Size:** FliCast's page is 331,918 bytes over 6,220 lines [checked: `wc`], so an agent cannot read it whole. There is no index. Sections go closed sets → constants → shapes, each ordered by file.
- **Dropped docs:** field docs are extracted but never rendered. FliStudio's JSON has 98 field docs, for example "`null` when `videos/` could not be read" on `ProjectRow.videos`, and none reach the page [checked: /Users/davidcruwys/dev/ad/flivideo/flistudio/docs/schema-mirror.json vs .md, grep count 0]. Closed sets never carry their JSDoc at all: `ProjectAspect`'s "Absent → 16:9" is lost [checked: extract_typescript.mjs:702-706; /Users/davidcruwys/dev/ad/flivideo/fli-core/src/identity.ts:9-10]. `aliases` (the `z.infer` type names) are in the JSON but not on the page. That does no harm in these repos, where the names match [checked], but it will hide FliCut's `Clip`/`clipSchema` pairs once HIGH-1 is fixed [inferred].
- **Union variants:** these render under a "field | type" header, with variant expressions as the "field" names [checked: /Users/davidcruwys/dev/ad/flivideo/fli-core/docs/schema-mirror.md:615-623].
- **Fix** (`render_mirror.py`):
  - render `doc` for fields and sets
  - add an `aliases:` line
  - use a "variant | shape" header for union kinds
  - add a one-line-per-id index at the top (id → `file:line`)
  - offer `--split-by-dir` for repos with more than about 150 entries

### LOW-1: noisy derived sets that produce bad refactor advice
- **Evidence:**
  - HTTP header names: `enhance-transport.h (branching) ['x-goog-resumable','content-type']`
  - RIFF chunk ids: `wav-peaks.id ['fmt ','data']`
  - keyboard keys: `hotkeys.e.key`, `App.e.key`, `Viewer.e.key`
  - zod internals: `input-shapes.def.typeName ['ZodOptional',...]`
  - [checked: derived sets listed from each repo's schema-mirror.json]
  - Each one carries "REFACTOR: declare it once (a z.enum…)", which is poor advice for `KeyboardEvent.key`.
- **Fix:** in `extract_typescript.mjs:subjectIsDeclaredElsewhere`/`controlFlow`, skip subjects whose declared type comes from a TS lib or `node_modules` declaration (DOM events, Headers, zod `_def`). In `derivedSet`, emit refactor findings only for sets that are compared in two or more places, or that reach a stored or IPC value.

### LOW-2: an absolute root in the IR breaks verify outside the original checkout
- **Evidence:** FliHub's mirror records `root: /Users/davidcruwys/dev/ad/flivideo/flihub-docs`, a checkout that no longer exists. Plain `verify_mirror.py` exits 2 with "repo root not found" [checked: run against /Users/davidcruwys/dev/ad/flivideo/flihub-aspect/docs/schema-mirror.json]. Note also that FliHub's mirror exists only on `origin/main` and in the `flihub-aspect` worktree. The local `flihub` main checkout is behind and has no `docs/schema-mirror.*` [checked: `git log --all -- docs/schema-mirror.json`].
- **Fix:** in `verify_mirror.py`, default `--root` to the git toplevel of the mirror file's directory, and fall back to the recorded root.

## 3. What works well and must be kept

- **Anchors are accurate.** Committed IR against current source: 0 gate violations in all 5 repos, and a fresh extraction moves 0 anchors (799 / 722 / 3,145 / 551 / 438 anchors) [checked: /private/tmp/claude-501/sm-review/*.fresh.json].
- **Fields are accurate where it reads.** 40 sampled structures (8 per repo) had field names matching the source. Every mismatch my grep flagged traced to my grep, not the mirror (one-liners, method signatures) [checked: /private/tmp/claude-501/sm-review/fields.py].
- **Spot checks of zod came out correct:**
  - `FailureCode` (26 members, one anchor per line) [checked: /Users/davidcruwys/dev/ad/flivideo/flistudio/shared/src/contracts.ts:31-58]
  - `BrandSummary` with inherited `BrandRef` fields anchored at the base
  - discriminators on `BrandCounts.state` and `WriteIdentityResult.kind` (with `refused` anchored inside the `Refused` factory)
  - `CapabilityName` read through `Object.keys(CAPABILITIES)`
  - Teletubby's `as const` sets `PRINCIPALS`, `ERROR_CODES`, `ZONES` and `OPEN_REFUSAL_CODES`
- **Verify catches real drift with a readable diff.** On the `flihub-aspect` working tree it reported 7 differences, including the new `AspectCheck` interface and the new fields on `FileInfo`/`RecordingState` [checked].
- **Gaps are honest when they are reached:**
  - helper-built schemas (`scanned`, `zoneScan`, `defineCapability` × 132)
  - a base imported from a package, reported as a PARTIAL field list (`OtherFolderRow`)
  - `.partial()` (`SettingsPatch`)
  - Python and JSON-Schema halves of the repo
- **Design choices to keep:**
  - parsing with the target's own TypeScript, with no regex fallback
  - file-qualified ids
  - line-insensitive gap keys in verify
  - JSON committed next to the markdown
  - the renderer is stack-independent
- **Tests pass:** 21/21 [checked: `SCHEMA_MIRROR_TYPESCRIPT=…/fli-core/node_modules/typescript python3 tests/test_extract_typescript.py`].

## 4. Proposed changes to SKILL.md

- **Step 1 (detect):** say that zod detection covers workspace `package.json` files and that the zod row can be absent while zod is in use. Replace "must show [OK ]" in the method doc accordingly.
- **Step 2 (extract):** document the `.d.ts` default (once MED-2 is fixed). Until then, warn: "if a repo commits build output next to source, exclude it; duplicate ids mean you did not".
- **Step 3 (judgement):** add a mandatory census check: "compare the page against `rg '^export (const|type|interface|enum|class)'` counts; any sizeable family absent from both mirror and gaps is an extractor miss". Name the known misses: re-exported `z`, schema aliases, template-literal unions, classes. Point to `known-gaps.json` as the only legitimate way to record an operator-found gap. Never edit the `.md`.
- **Step 6 (verify):** state plainly what verify does *not* catch: things the extractor cannot see, and (until fixed) stale anchors. Add the `.md`-matches-JSON check.
- **"The gate":** reword to what `check_anchor` really guarantees (the value is legible at the line, by substring).
- **Page contract:** require a standing "Never read by this extractor" block on every rendered page, so "Nothing" can never appear while classes or aliases were skipped.
- **Triggers:** fine as written. Consider adding "is the schema mirror complete" / "what does the mirror not cover".

## 5. What I did not check

- The Python extractor (`extract_python.py`). No Python targets were in scope.
- Whether `defineCapability(...)` schemas in FliCast (132 uses) could reasonably be followed.
- FliHub in depth. I checked its scope, the `.d.ts` behaviour and verify, not its field accuracy.
- Whether each derived set's members are complete. I checked only that they exist and are anchored.
- Behaviour on Roamy or another checkout path, beyond the missing-root case.
- My grep census is syntactic, so its counts of "missing" type aliases include legitimate non-schemas such as function types and generics. The zod counts were confirmed by reading the files.

## 6. Reconciliation

(Added after reading `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/doc-skills-blind-review.md`.)

**Found independently:**
- **Log #1** (zod through a re-export is skipped, no gap is recorded, verify exits 0, Teletubby's page says "Nothing", and a hand-correction will be overwritten) → my HIGH-1, HIGH-2 and MED-1. One small correction to my own count: FliCut has **5** files under `src/` that take `z` from `@appydave/core`, matching the log [checked: grep of /Users/davidcruwys/dev/ad/flivideo/flicut/src]. My "6" came from a whole-repo count.
- **Log #9** (stale `shared/*.d.ts` pulled into scope by default) → my MED-2. I add what the log does not say: 117 duplicate ids, which the gate lets through and verify's index collapses.

**Missed:**
- **Log #2** (nothing runs verify; FliStudio drifted 53 differences within a day). I saw the SKILL.md step that suggests a hook, but I did not check whether one was wired. I have now: no repo has `verify_mirror` in `.husky`, `.github`, `package.json`, `.git/hooks` or `lefthook.yml` [checked: grep across all six repos]. So I confirm it. Today FliStudio verifies clean, because it was regenerated since.

**Dispute:**
- None on substance. On **log #2**, the fix is only partial: wiring verify into CI would *not* have caught log #1, because verify re-runs the same blind extractor. That is my HIGH-3. A hook needs the census and `validate_ir` changes before it is worth trusting.

**Found here, not in the log:**
- Silent drops beyond zod, none disclosed as gaps: schema aliases (`ProjectsListInput = BrandInput`), template-literal unions (`View`), Teletubby's `CapabilityName`, classes, and `keyof typeof` aliases (HIGH-2).
- Verify ignores stale anchors, even though `validate_ir` on the committed IR would catch them (HIGH-3).
- TS lib types are labelled with file paths that depend on the environment (HIGH-3).
- The gate passes hand-typed members, fields, types and whole structures (MED-3).
- The renderer drops field docs (98 in FliStudio), set docs and aliases. Pages reach 332 KB with no index, and union variants appear under a "field" header (MED-4).
- `detect_stack` misses zod when it is declared only in a workspace `package.json` (FliStudio) (HIGH-1 fix).
- Derived sets from DOM keys, HTTP headers and zod internals produce bad refactor advice (LOW-1).
- The absolute `target.root` breaks verify for FliHub's committed mirror (LOW-2). FliHub's local `main` is behind `origin/main` and has no mirror files.
