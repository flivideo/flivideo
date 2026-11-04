# Brief: Story Pilot typed guides: every guide is a Markdown file with a fixed header

**Purpose**: Build brief. Make every story guide one typed object: a Markdown file whose header (frontmatter) follows a
`storypilot.guide/1` schema, with the prose as its body. JSON settings refer to guides by id and stop carrying prose.
Move the two build-story spines out of `defaults.json` into Markdown.

**For Agents**: Owner `flivideo-orch`; build on the **M2**, gate and merge on the M4, restart via `my-app` (heads-up to
`flivideo-roamy` first, as tonight). From `flivideo-roamy`. **Go: David, 2026-11-04 ~19:30** ("yes, write the brief
for orch and then ask orch to execute on it"). Research it rests on, read first:
`/Users/davidcruwys/dev/ad/flivideo/docs/research/storypilot-guide-object-model-2026-11-04.md` (7a185f3).

## Why (measured, see the research)

- The JSON side is already zod-typed and validated (`shared/contracts.ts`, `host.ts`, `store.ts`). That isn't the problem.
- The problem is that "prose that steers the writer" lives in four unrelated forms:
  - `Profile.spine`, a string in JSON;
  - `Template.text`; the hidden `build-story-spine` is a verbatim copy of the spine;
  - `Guide.pointer`, which points to a Markdown file with no contract;
  - `voiceDocs`, a list of bare paths.
- Markdown guides have no header contract, so card summaries are guessed by `summaryOf()` and show file meta, not advice.
- Read → on the build-story guide had to dig into JSON.

## The model

```yaml
---
schema: storypilot.guide/1     # required
id: build-story                # required, kebab, unique
label: Build story (long form) # required
type: structure                # required: verbal | voice | structure | lens | other
level: global                  # required: global | brand | series | video
gist: …                        # required: ONE line, what this guide tells the writer
appliesTo: {form: story, length: long}   # optional
brands: [appydave]             # optional
---
<the prose the writer reads>
```

- Other keys in the header are kept and ignored. This matters: VERBAL-STYLE.md and VIDEO-STRUCTURE.md carry provenance
  (`version`, `distilled_from`, `corpus_window`, `prompt`, `retrieval_pool` …) that the `brand-dave:verbal-style-forge`
  and `structure-forge` skills write on purpose. **Never remove or rewrite them.**
- **A new kind of guide = a new file with this header, no code.**

## Do

1. **`@flivideo/core`: `GuideDoc` (zod) + `parseGuide(text) → {header, body} | {error}`.**
   - Framework-free, as fli-core is today.
   - Unit tests cover:
     - a valid file;
     - each missing required key;
     - a bad enum;
     - unknown keys kept;
     - no frontmatter.
   - Tag a release; flistudio pins the tag.
2. **The spines become files.**
   - Create `modules/storypilot/guides/build-story.md` and `build-short.md`. Each body is today's `spine` text **word for word**.
   - `Profile.spine` → `Profile.guide` (a guide id).
   - `activeProfile` resolves the guide's body. `story.brief` returns the active profile's guide `{id, path, gist, body}`, so builds read the same words as today.
   - Remove from `defaults.json`:
     - the `spine` strings;
     - the `build-story-spine` template.
   - Remove `build-story-spine` from `v-appydave/-storypilot/templates.json` `hidden`, since it would now name nothing.
   - Git keeps the old text; list each removal in the report.
3. **Seeds point at files.** The two Global structure seeds point at the new `.md` files, not `defaults.json#profile=…`.
4. **Validate on list.**
   - The guide list parses each pointed `.md` with `parseGuide`.
   - A card's one-liner is the header's `gist`.
   - A file with no header or a bad one still shows, with its reason on the card ("no guide header" / "invalid: missing gist"), plus the old `summaryOf()` text dimmed as a fallback. Never fail silently, never hide the card.
5. **"Used by this video" on each card.**
   - The active profile's guide is "used".
   - A guide whose `appliesTo` doesn't match the video's form/length is "not used", with the reason shown ("short only", "tutorials only").
   - Otherwise it's "available". Label only: builds do **not** start filtering by `appliesTo` in this brief.
6. **Read → shows the advice.**
   - For a guide `.md`: the header as a small strip (type · level · applies-to · gist), then the body rendered.
   - "Show source" reveals the raw file, coloured (reuse b34d5d3's renderer).
   - The JSON-fragment view stays for any other JSON pointer.
7. **Strict JSON.**
   - Make `Guide`, `Profile` and `Template` `.strict()`, so a misspelt key fails instead of being silently dropped.
   - First load every real file (shipped defaults, `v-appydave/-storypilot/*.json`, any brand or video `guides.json` on the M4) and confirm they pass. Report any that wouldn't, before switching.
8. **Headers on the existing Markdown guides.** Add only the guide keys; **don't touch the body or the existing keys**.
   - `brand-dave/skills/brand/references/appydave/VERBAL-STYLE.md`;
   - `brand-dave/skills/brand/references/_formats/educational/VIDEO-STRUCTURE.md`;
   - `v-appydave/voice-profile.md`: it has no frontmatter, so add a block at the top;
   - `flivideo/docs/research/appydave-hook-study-2026-11-03.md`.
   - The `gist` for each is **drafted by the agent** from the file's own content, one line each. List the six gists in the report, because **David approves the wording**.
9. **The forge skills keep the guide keys.**
   - Update the frontmatter template in `brand-dave:verbal-style-forge` and `brand-dave:structure-forge`, so a regeneration writes or keeps `schema/id/label/type/level/gist`. Bump the brand-dave plugin version.
   - Update `flivideo:storypilot` step 5: "Follow the active profile's guide (from story.brief)", replacing the paraphrased beats. Bump the flivideo plugin version.
10. **A test that loads every seeded guide file** (on the M4, where the files live) and fails on any invalid header.

## Out of scope

- Changing any guide's prose.
- `creator.voiceDocs` vs the Verbal guides. Both list the same two files; which owns them is David's call later.
- The "I'm AppyDave, let's get into it" signature.
- Filtering builds by `appliesTo`.
- Series vs video project.
- The speed control.

## Gate and report

- **Gate:**
  - fli-core unit tests and tag;
  - flistudio typecheck and unit;
  - the **full storypilot e2e on the M4**, including the guides tab and Read → on each guide type;
  - every other suite green.
- **Builds unchanged:** confirm a dry `story.brief` on d13 returns the same spine words as before, by diffing the text.
- **Screenshots on d13:**
  - the Guides section with gists and used / not used;
  - Read → on build-story;
  - one invalid-header card, made on a copy, not on a real guide.
- **Report to `flivideo-roamy`:**
  - commits per repo;
  - the removals list;
  - the six drafted gists for David to approve;
  - any real file that failed the strict check.
