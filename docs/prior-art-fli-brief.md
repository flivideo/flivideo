---
type: reference
title: Prior art — FliBrief (deprecated 2026-09-23)
description: What is still useful from the deprecated FliBrief repo and its Dec-2025 four-stage FliVideo vision, distilled so nobody needs to open fli-brief again.
created: 2026-09-23
timestamp: 2026-09-23
status: active
---

# Prior art — FliBrief (deprecated 2026-09-23)

**Purpose**: Keep the reusable ideas from FliBrief (the Editor Brief tool built for the external editing company) and the original four-stage FliVideo vision, before the repo is retired.

**For Agents**:
- Read this before designing project/episode layout, naming, trash, or vocabulary in FliHub / FliStudio / fli-core.
- Read before specifying FliEdit (editor brief), Scribe (scripting) or FliYLO (launch optimiser).
- Every section cites its source by absolute path + line range. "Carries into" lines are **suggestions**, not rulings.
- This is prior art, not current spec. Check "Where today differs" before copying anything.

All sources are under `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/`.

---

## 1. Container Project / episode model

- Two project shapes:
  - **Standard project** = one video. Root holds `assets/`, `recordings/`, final deliverables at root.
  - **Container project** = a series. Root holds episode folders; each episode mirrors a standard project.
- Episode folder naming: `{NN}-{episode-name}`, e.g. `01-flivideo-project-kickoff`. Episodes are optional.
- The Dec-2025 doc used bare numeric episodes (`001/`, `002/`); the older docs used `01-episode-name/`.
- Per-scope subfolders: `recordings/`, `chapters/` (joined chapter video), `.trash/`, `assets/`, `transcription/`, `shorts/`.
- Only **one active project (or episode)** at a time; all incoming recordings route there.
- Config: global state in `~/.fli-video.json` (current project + episode); per-project `.fv.json` with a `video` section and an `episodes` section of the same shape.
- Project types were planned per brand/channel: long-form (default), podcast/series (episodes), shorts, course; plus text projects (articles, lessons, factsheets, ebooks, lead magnets).
- Shorts: original plan was **both** a `shorts/` folder inside the parent project *and* "related shorts projects" stored as separate linked projects.

Example: `a27-xmen-my-video-project/01-flivideo-project-kickoff/recordings/03-2-outro-cta.mov`, with sibling `chapters/`, `shorts/`, `.trash/`.

Source:
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/fli-video.md` lines 37–58, 330–333
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-2-recording/core-concepts.md` lines 95–110, 247–287
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/technical-specifications.md` lines 292–297, 315–367, 405–429, 444–449, 546–569

Carries into (suggestion): **fli-core** (project/episode model + config shape), **FliHub** (folder layout, one-active-project routing).

---

## 2. Brand table with short codes

| Code | Brand | Status (as written) | Type |
|---|---|---|---|
| `dc` | DavidCruwys | Inactive | Website (umbrella) |
| `ad` | AppyDave | Active | YouTube @appydave |
| `ac` | AppyDaveCoding / AppyCast | Dormant | YouTube @appydavecoding |
| `fv` | FliVideo | In development | SaaS app, @flivideo |
| `aitldr` | AI-TLDR | Active | Faceless YouTube @aitldr |
| `trend` | Trend10 | Development | YouTube @trend10 |
| `kl` | Klueless | Development | Website (DSL) |
| `kk` | KoziKafe | Active | Physical business |
| `ess` | Emotional Support Spiders | Concept | Agentic world / website |
| `wp` | WinningPrompts | Dormant | YouTube @winningprompts |
| `c9` | Carnivore90 | Legacy | YouTube @carnivore90 |

- Codes sat inside project names: `a20-ad-open-interpreter`.
- Older spec used `t1` for Trend10; the brand table uses `trend`. Pick one if reused.
- Kybernesis, Beauty & Joy, Joy Juice, client brands are **absent** — the table predates them.

Source:
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-2-recording/brands.md` lines 5–17, 87–99
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/technical-specifications.md` lines 331–352

Carries into (suggestion): **fli-core** (brand registry with short codes; reconcile against today's brand list first).

---

## 3. Pillars

- ⚠️ `stage-2-recording/pillars.md` is **byte-identical to `brands.md`** (verified with `cmp`). It holds no pillar content.
- The only pillar content in the repo is a definition + one example:
  - Pillar = recurring thematic/format focus area of a brand (niche + topic + format + style).
  - AppyDave core pillars: prompt engineering, AI agents, coding with AI. Secondary: 555 Manifesto, KlueLess.

Source:
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-2-recording/pillars.md` lines 1–99 (duplicate of brands)
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-2-recording/core-concepts.md` lines 87–91
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/technical-specifications.md` line 77

Carries into (suggestion): **fli-core** (pillar as a brand attribute). Real pillar lists live elsewhere (`~/dev/ad/content-pillars/`), not here.

---

## 4. Chapter-segment naming + trash/undo rules

**Project name**: `{seq}-{brandCode}-{slug}` or `{seq}-{slug}`. Seq runs `a00…a99`, then `b00…`. Example `a27-xmen-my-video-project`. Older names carried a status suffix (`-IN-PROGRESS`, `-NOT-STARTED`, `-CI`).

**Recording name**: `{chapter}-{sub}-{chapterName}[-{tag}…].mov`
- `03-1-outro.mov`, `03-2-outro-cta.mov`, `03-3-outro-endcards.mov`
- Tags must be **pre-configured** so the parser can split tags from chapter name (`cta`, `endcards`).
- A reverse parser was specified (name → `{ChapterSequence, Subsequence, ChapterName, Tags}`).
- Chapter names are short: intro, overview, example, question, answer, summary, outro. Typical 15-min video ≈ 5–8 chapters.
- Extra instruction tags for the editor: `INTRO`, `CTA`, `TRIM`, `TRIM-40s`, `BROLL`, `TELEPROMPT`, `OUTRO`.

**Approval / trash flow**
- New Ecamm drops (`Ecamm Live Recording on 2023-12-18 at 09.58.55.mov`) are **unapproved** until named.
- On "save", the take is renamed to chapter-segment form and **all prior unnamed takes move to trash**.
- Trash folder created **on demand only**; takes can be reviewed and restored (undo); "empty trash" deletes the folder.
- On chapter change, prompt for the new chapter short name.

Source:
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-2-recording/naming-project-folders.md` lines 9–128, 183–236, 240–270, 281–350
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/fli-video.md` lines 67–75, 317–328
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/technical-specifications.md` lines 369–403, 571–615

Carries into (suggestion): **FliHub** (naming + trash), **fli-core** (name parser + tag registry).

---

## 5. Vocabulary

- **Rule Matcher** — identifies new recordings/assets by filename pattern + folder + extension; feeds the File Mover.
- **Asset Watcher** — watches in real time and renames/moves: Ecamm/OBS recordings → project; Leonardo/Canva downloads → asset folder.
- **Media Rollup** — combining recordings and/or transcripts:
  - *Chapter rollup*: all parts of chapter 01 recorded → one chapter video + transcript (automatic).
  - *Shorts rollup*: intro/body/outro → one short (inferred, needs user confirm).
  - *Full video rollup*: all chapters → full video + transcript.
  - Video and transcript rollups run **independently**.
- **Business Unit** — the business that owns a brand/channel/pillar; affiliate links attach to a business unit or a creator.
- **Content Graph** — relationships between videos, series, shorts, articles, posts across brands/channels.
- **Recording Session** — ordered chapters/parts at project or episode level, transcribed on the fly; new chapter triggers chapter processing.
- **Editor Brief** — instructions for the editor: key points, chapter titles, suggested B-roll (see §6).

Source:
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-2-recording/core-concepts.md` lines 25–52, 64–67, 112–158, 176–178, 205–207, 231–245, 291–298

Carries into (suggestion): **fli-core** (shared glossary), **FliHub** (Rule Matcher, Asset Watcher), **FliStudio** (Recording Session, Media Rollup).

---

## 6. Editor Brief concept

**Problem**: the creator could not tell the editor which B-roll to use, where on the timeline, tied to which sentence.

**Model**
- Transcript split into **Intro / Content / Outro** sections → sentences → **visual concepts**.
- Each visual concept has an **original prompt**, an **enhanced prompt**, and generated images.
- User clicks images to assign **selection order** (1, 2, 3); drag to reorder.
- Export = brief with asset placement, timing, priority + an **asset manifest**.

**Data shape (input)**

```json
{ "project_name": "Sample Project",
  "sections": { "intro": [], "content": [], "outro": [] },
  "visual_concepts": [{ "concept_id": "vc1", "description": "…",
    "prompts": { "original": "…", "enhanced": "…" },
    "images": [{ "image_id": "img2", "file_path": "…", "selected": true }] }] }
```

Export: `{ project_name, selected_images: [{ concept_id, images: [{ image_id, file_path, order }] }] }`.

**UI** — five-panel dockable layout: header (project switch, search), left (transcript tree with CTA tags), central grid (one row per visual concept), right (sentence, prompts, big preview, reorder list), footer (progress "15 of 30 selected", save/export, undo/redo). Panels lock with a lock icon or Cmd+~.

**Planned, never built**: reusable concept templates, completeness QC, PDF/text export.


Source:
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/fli-video.md` lines 115–174, 247–255
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-3-editing/README.md` lines 1–49
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-3-editing/requirements/functional-requirements.md` lines 1–36; `components-list.md` 1–46; `data-structure.md` 1–7; `ux-requirements.md` 1–16; `non-functional-requirements.md` 1–13
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-3-editing/design/interaction-design.md` 1–5; `ui-flow-diagram.md` 1–7
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-3-editing/code-samples/load_data_structure.json` 1–22; `export_data_structure.json` 1–11

Carries into (suggestion): **FliEdit** (sentence → visual concept → ordered asset model; the brief becomes an internal edit plan now that editing is in-house).

---

## 7. Stage 1 and Stage 4 notes

**Stage 1 — Pre-production** (never started)
- Concept capture, script/beat outlines, shot planning, asset checklists, topic research, brand/pillar alignment.

**Stage 4 — Publishing** (built as AWB prompts, "ready to port")
- Summary + abridged transcript; optional intro/outro split.
- Preliminary topic + rough title.
- "12 metadata concepts" (keywords, search strings, tone…) — list never finalised.
- YouTube chapters from transcript sections.
- Thumbnail style, AI image prompts, overlay text, title variants.
- Description (hook, chapters, CTA) + engagement-driving pinned comment.
- Post-publish social posts (X, Facebook, LinkedIn, Skool) carrying video/playlist link.
- Shorts: identify candidates, titles, descriptions + hashtags, social posts.
- Built as AWB Gen 1 (now archived): 49+ prompts in 7 sections — prep, chapters, B-roll, analysis, title/thumb, metadata, social. Path: `~/agent-workflow-builder/ad-agent_architecture/prompts/youtube/launch_optimizer/`.

Source:
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-1-preproduction/README.md` lines 1–22
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-4-publishing/README.md` lines 1–32
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/fli-video.md` lines 18–29, 178–273

Carries into (suggestion): **Scribe** (Stage 1), **FliYLO** (Stage 4 checklist + the 7-section prompt order).

---

## 8. SRT converter requirements

- Browser-only tool: drop or paste `.srt` → clean paragraph transcript.
- Input: `.srt` only, ≤10 MB, UTF-8, CRLF/LF/CR; auto-convert on paste.
- Parse: sequence / `HH:MM:SS,mmm --> …` / text / blank; accept `,` or `.` decimals; skip malformed blocks, don't fail the file.
- Clean: strip `<b> <i> <u> <font>`; join blocks into sentences; add missing punctuation; paragraph every ~4 sentences.
- Output: live word count, one-click copy.
- Design choice worth keeping: per-segment transcripts were `.txt`, not SRT, because segments get concatenated downstream.

Source:
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/utilities/srt-converter-requirements.md` lines 1–237
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/utilities/README.md` lines 20–34
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/fli-video.md` lines 77–84, 350–388

Carries into (suggestion): **fli-core** (SRT → text util), **FliHub** (transcript handling).

---

## 9. Content Intelligence, Affiliate Management, Insight Explorer

- **Content Intelligence** — central repository of *published* content (videos, articles, posts) across all brands/channels. Uses: cross-reference related videos, pick end-card videos, help write descriptions, vector search. Includes Content Graph, shorts analysis, and close-out (archive published; back up paused/unpublished).
- **Affiliate Management** — affiliate links at brand/business-unit or creator level; each link has description (to match against transcripts), hierarchy, search index, group/tag.
- **Insight Explorer** — competitor video + keyword analysis → content plans from top performers.

Source:
- `/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/stage-2-recording/core-concepts.md` lines 40–52, 195–227

Carries into (suggestion): **Content Intelligence** (missing app), with affiliate matching as a FliYLO description step.

---

## Where today differs

- **Trash**: original was on-demand `recordings/.trash/` (sometimes `project/.trash/`, plus a `.backup/` in fli-video.md). FliHub today uses `-trash/` at project root — `/Users/davidcruwys/dev/ad/flivideo/flihub/shared/paths.ts:78`.
- **Chapters folder**: original `chapters/` at project/episode root; FliHub today uses `recordings/-chapters/` — `/Users/davidcruwys/dev/ad/flivideo/flihub/shared/paths.ts:44,77`.
- **Editor**: original named Gling as final assembler from approved segments; today FliCut edits in-house.
- **Shorts**: original allowed shorts as separate linked projects. David ruled 2026-09-23 that shorts spun off one long-form video live **inside that project's `videos/`**, not as separate projects.
- **Multi-video projects**: David ruled 2026-09-23 that Kybernesis ×10 and Beauty & Joy ×3 are standalone multi-video projects — the nearest modern equivalent of the Container Project.
- **Segment naming was never consistent** across the old docs: `1-1-intro` (fli-video.md), `02-1-content` (core-concepts, naming spec), `02-a-content` letters (technical-specifications). Don't treat any one as canonical.

---

## Not harvested

- `presentations/`, `recent-presentation-assets/`, `agent-flip-cards.html` — token-optimisation and demo decks; talk material, not design input.
- `stage-2-recording/klue-architecture/` — `.klue` DSL models of the old Stage 2 commands; superseded by FliHub code.
- `stage-2-recording/cli.md`, `overview.md`, `stage-1-preproduction/project-new.md` — `ad-project-new/rename/list` CLI + server spec; FliHub owns project creation.
- `stage-2-recording/file-mover.md` — the long form of Rule Matcher (§5); open only if FliHub's watcher rules are redesigned.
- `stage-2-recording/ux.md`, `stage-3-editing/development/`, `design/branding-guidelines.md` — dockable-UI detail and an off-brand green palette.
- `project-roadmap.md`, `INDEX.md` — navigation for a retired plan. `------chaters.txt` — chapter timestamps of an unrelated BMAD video.
- `utilities/README.md` cites `video-file-namer-replit.md`, which is not in the repo.
