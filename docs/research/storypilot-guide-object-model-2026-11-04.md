# Story Pilot guides: are the files typed, and what object model should guides have?

**Purpose**: A measured answer to David's question (2026-11-04 evening): is Story Pilot's guide/settings JSON a typed object
model or loose JSON poked by custom code, and what one object model should every story guide (JSON or Markdown) follow?
Read and recommend only; nothing built.

**For Agents**:
- Read before any work on Story Pilot guides, profiles, templates or card summaries.
- Owner `flivideo-orch`; written by `flivideo-roamy` from M4 code at flistudio `b34d5d3`. No brief until David says go.

## 1 · Findings

| File | Typed? | Validated at runtime? | Reads/writes through | Duplicates | Drift risk |
|---|---|---|---|---|---|
| `modules/storypilot/defaults.json` (schema `storypilot.defaults/1`) | Yes: zod in `shared/contracts.ts` (`SettingsBlock`, `Profile`, `Template`, `Guide`) | Yes: `host.ts` parses it three times (`Defaults.parse`, `z.array(Template).parse`, `z.array(SeedGuide).parse`); tests load the real file (`settings.test.ts`, `characterization.test.ts`, `guides.test.ts:40`) | `server/host.ts` (read once, cached) | build-story spine = `profiles[build-story].spine` **and** `templates[build-story-spine].text` (verbatim) | Schemas are not `.strict()`, so a typo in an optional key (`apliesTo`) is **silently dropped**, not rejected. `#profile=build-story` in a guide pointer is a plain string: renaming the profile breaks the card with no error |
| `<brand>/-storypilot/settings.json` | Yes (`BrandFile` / `SettingsBlock`) | Yes: `store.ts` `readJson(file, schema)` → `schema.parse`; writes via `applyPatch` → `SettingsBlock.parse` → `writeAtomic` | `server/store.ts` (one module) | `creator.voiceDocs` lists VERBAL-STYLE.md + voice-profile.md, **the same two files** as the brand Verbal guides; `voice.signatures` still holds "I'm AppyDave, let's get into it" (contradicts the build-short spine and the 2026-11-03 story-video ruling) | Same non-strict caveat |
| `<brand>/-storypilot/templates.json` | Yes (`TemplatesFile`) | Yes (`readJson`) | `store.ts` | hides `build-story-spine` (the duplicate above) | Low |
| `<brand>/-storypilot/guides.json` | Yes (`GuidesFile` / `StoredGuide`) | Yes (`readJson`) | `store.ts` | — | **Doesn't exist for v-appydave yet**; all six cards are shipped seeds |
| Markdown guides (VERBAL-STYLE, voice-profile, VIDEO-STRUCTURE, hook study) | **No** | **No.** Frontmatter is skipped; nothing is read from it | `guides.ts summaryOf()` heuristic: a "Purpose" line, else the paragraph under the first heading, else the first 160 characters | The flivideo:storypilot skill paraphrases the build-story spine (step 5) | High: four files, four different frontmatter shapes, so the card summary is whatever the heuristic happens to hit (file meta, not advice) |

Markdown frontmatter today:

| Guide | Frontmatter | What the card summary picks up |
|---|---|---|
| VERBAL-STYLE.md | `brand, artifact: verbal-style, version, distilled_from, corpus_window, generated, …` | "Companion docs: visual identity in DESIGN.md…" (meta) |
| voice-profile.md | none | the blockquote "Synthesized from all 182 as-aired transcripts…" (provenance) |
| _formats/educational/VIDEO-STRUCTURE.md | `format_type: educational, artifact: video-structure, version, …` | "Format-scoped, not brand-scoped…" (meta) |
| hook study | `created, timestamp` | its `## Purpose` (a research purpose, not advice) |

**Verdict on David's suspicion:**
- **The JSON side is NOT loose.** It's zod-typed, validated on load and write, goes through two modules (`host.ts` shipped, `store.ts` brand/video), and the real defaults.json is loaded in tests.
- **His instinct is right about the model, though.** "Prose that steers the writer" exists as four unrelated things: `Profile.spine` (a string in JSON), `Template.text` (a string in JSON), `Guide.pointer` → a Markdown file with no type, and `voiceDocs` (bare paths).
- **The Markdown half has no contract at all.** That's why cards show file meta and Read → had to dig into JSON.

## 2 · Recommended model: a Guide is a typed Markdown document

```
 guide file (Markdown)                         JSON settings / seeds
┌────────────────────────────────┐            ┌─────────────────────────────┐
│ ---                            │            │ profile: build-story        │
│ schema: storypilot.guide/1     │◀── by id ──│ profiles: [{id, label,      │
│ id: build-story                │            │   form, length,             │
│ label: Build story (long form) │            │   guide: "build-story"}]    │
│ type: structure                │            │ (no spine text)             │
│ level: global                  │            └─────────────────────────────┘
│ appliesTo: {form: story,       │            ┌─────────────────────────────┐
│             length: long}      │◀── path ───│ guides registry: {id, path} │
│ gist: Five beats: problem →    │            │ + empty slots               │
│   why → tension → turn →       │            └─────────────────────────────┘
│   resolution. No invented drama│
│ ---                            │   GuideDoc schema + parser (zod, framework-free)
│ <the prose the writer reads>   │   in @flivideo/core; load-time check rejects a
└────────────────────────────────┘   bad file and the card shows why
```

- **Required frontmatter:** `schema, id, label, type, level, gist`. Optional: `appliesTo, brands`.
  - Existing provenance keys (`version`, `distilled_from` …) stay and are ignored.
  - Adding a new kind of guide = a new file with this header, no code.
- **Types and validation:**
  - `GuideDoc` (zod) plus `parseGuide(text)` in `@flivideo/core`. It's framework-free, the same rule fli-core follows for key data, and other apps (Teletubby, Captain's Log) can read guides too.
  - Story Pilot validates each pointed file at list time.
  - A bad header shows as "invalid: missing gist" on the card, never silently.
  - One test loads every seeded guide file.
  - Make `Guide`, `Profile` and `Template` `.strict()` so JSON typos fail.
- **Migration (David decides keep or delete):**
  - New `modules/storypilot/guides/build-story.md` and `build-short.md`, holding today's spine text word for word.
  - `Profile.spine` becomes `Profile.guide` (an id). The seed pointers change from `defaults.json#profile=…` to those files.
  - **Would be deleted:**
    - the `spine` strings in defaults.json;
    - the hidden `build-story-spine` template;
    - the skill's paraphrase in step 5, replaced by "read the active profile's guide".
  - **To decide separately:** `creator.voiceDocs` vs the Verbal guides (one list should own those two files), and the "let's get into it" signature.

## 3 · Earlier recommendations, re-judged

| # | Before | After this finding |
|---|---|---|
| 1 | Mark which guides this video uses | **Kept, and now computed:** the active profile's `guide` id plus `appliesTo` against the video's form/length gives "used / not used, because…" |
| 2 | Card summary says what the guide tells the writer | **Becomes the `gist` field**: no heuristic. Six one-line gists to write (metadata, not content) |
| 3 | Read → opens prose, "show source" underneath | **Falls out of the model:** every guide is Markdown, so the source is the file itself. Tonight's JSON-fragment view (b34d5d3) becomes a stopgap |
| 4 | Move spines out of JSON into Markdown (later) | **Promoted to step 1 of the migration.** It isn't optional any more: it is what makes 1–3 cheap |

Out of scope: building, editing any guide's prose, series vs video project.
