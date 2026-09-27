---
type: brief
title: Video resources model
description: "One per-video record of everything that belongs to a video — launch titles and thumbnails (many candidates, some chosen), chapters, tags, description, community links, affiliate slots, artefacts — held by FliStudio, readable and writable by agents."
created: 2026-09-27
status: proposal — waiting on David (nothing built)
---

# Video resources model

**Purpose**: David wants one place per video for its "resources" — what launches it on YouTube, what goes to Skool,
where affiliate links plug in, and the artefacts made for it — visible in a UI and, above all, driven by agents through
verbs. This doc is detailed enough to build the whole thing in one pass. Nothing is built until David approves it and
the mock (https://claude.ai/artifact/GovQGoVjJ7McNEzGsXv1wL).

**Ask of David**: the decisions in §9 (each has a recommendation). The rest is design.

---

## 1. What already exists (researched 2026-09-27 — reuse, don't duplicate)

| Thing | Where | What it holds | How this model uses it |
|---|---|---|---|
| **YLO `launch.json`** | zod contract `/Users/davidcruwys/dev/agents/ylo/docs/schema/launch-metadata.schema.ts`; one real record at `v-appydave/d02-cutty-audio-cleanup/launch.json` | The launch **workshop**: P01–P12 analysis, `TitleCandidate{id,text,emotion,score,rank,rationale,provenance}`, `ThumbnailText`, `ThumbnailPrompt`, `Chapter{n,title,timestamp}`, `Description{short,full,chapters,keyword_tags[]}`, and exactly 3 `Variant` slots | Stays YLO's. A title YLO wants on the video becomes a **resource** that points back at its candidate (`ref: { schema: 'ylo.launch', id: 't3' }`). Scores and rationale stay in `launch.json`; they are not copied. |
| **Thumbnail system** | `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/thumbnail-system/schema.json` → **`generation_record`** (flivideo b0f4277, thumbs-work) | One generated thumbnail: `thumbnail_id`, `spec_ref`, `spec_sha`, `brand_id`, `recipe`, `presenter{library_id,role,file_id}`, `generation{tool,model,…}`, `text_layer`, `files{background,final}`, `quality` | Stored **as-is** as the `meta` of a thumbnail resource (`ref.schema = 'thumbnail.generation'`). It has no status on purpose: its `_note` says FliStudio owns candidate / in test / chosen. |
| **FliHub `brand-config.json`** | `/Users/davidcruwys/dev/ad/flivideo/flihub/server/brand-config.json` | Per brand: `socialLinks.skool`, `ctas.foldCta` ("Join Skool Community"), `affiliates[{name,url,active}]`, `playlists`, `descriptionTemplate` | The **brand-level** link library for now. A per-video affiliate or community slot names an entry here (`ref: { schema: 'flihub.brand-config', id: '<affiliate name>' }`); it does not copy the URL. |
| **FliHub `.flihub-state.json`** | per project | `title?` (the one title that shipped), `chapters`, `ships` | The published fact, FliHub's today. See §9 Q4. |
| **Tuber** | `/Users/davidcruwys/dev/agents/tuber` | 5 titles in chat, one per angle; reads FliStudio `video.text` over `/api/rpc` as `agent:tuber` | Becomes a producer: `resources.add { kind: 'title', ref: { schema: 'tuber' } }`. It already has the transport. |
| **FliLaunch / app-02 spec** | `/Users/davidcruwys/dev/ad/flivideo/flilaunch` (dormant since 2026-05-10; YLO took its P01–P12 contract); `brains/brand-dave/app-requirements/app-02-youtube-launch-optimizer.md` | 10–20 titles → 3 finals; 6 thumbnail concepts → 3 finals; description = synopsis + chapters + **affiliate slots** + **CTA/community links** + legal; 10–15 keyword tags | Gives the taxonomy (§2) and "3 finals" = YouTube test slots, which this model stores as a status and does not cap. |
| **The word store** | fli-core v0.11.0 `words.ts` + FliStudio `words.*` | The precedent this copies: one fli-core schema, one FliStudio writer, agent-open verbs, `Stamp {at, by}` on every entry, apps read the file themselves | Same pattern, same `Stamp`. |

**Does it belong in FliStudio? Yes — the code agrees.** FliStudio is the project front door that agents already use
(`video.text`, `words.*`, `apps.status`), owns the only store written for others (`fli.words.json`), and is the one app
that knows every video in a project (`videos/<name>/`, D15). What it does **not** own is the thinking: YLO keeps the
launch workshop, thumbs-work keeps generation, FliHub keeps brand links. FliStudio keeps **the list of what a video has
and which ones are chosen** — the index everyone else points into.

---

## 2. Taxonomy

A **resource** is one thing that belongs to a video. Its **kind** says what it is; the kind belongs to a **group**.

| Group | Kind | Value | Many candidates? | Choosing | Typical producer |
|---|---|---|---|---|---|
| **launch** (YouTube) | `title` | `text` | **yes, N** | `chosen` (one) · `in-test` (YouTube's test takes 3; not capped here) | Tuber, YLO, David |
| | `thumbnail` | `path` (+ `meta` = generation_record) | **yes, N** | `chosen` (one) · `in-test` | thumbs-work, David |
| | `description` | `text` | yes | `chosen` (one) | YLO |
| | `chapters` | `meta.chapters: [{n, title, timestamp}]` (YLO's `Chapter`) | yes | `chosen` (one) | YLO, FliHub |
| | `keywords` | `meta.tags: string[]` (YouTube tags) | yes | `chosen` (one) | YLO |
| **community** (Skool) | `skool-post` | `url` | no | `published` when posted | David |
| | `download` | `path` or `url` | no | — | David |
| | `community-link` | `url` | no | — | David |
| **affiliate** | `affiliate-slot` | `ref` → brand-config affiliate | no | — | future affiliate app |
| **artefact** | `artifact` | `url` (claude.ai/artifact/…) | no | `published` | Claude sessions |
| | `page` | `url` or `path` (HTML) | no | — | Claude sessions |
| | `file` | `path` | no | — | anyone |
| **other** | anything new | any | — | — | — |

Found by the research and added: `description`, `chapters` and `keywords` as separate kinds (app-02 and YLO keep them
apart); `download` (app-02 "downloads"); `affiliate-slot` as a *slot*, not a link (§1: the link lives with the brand).

---

## 3. Where each group lives

| Group | Now | Later |
|---|---|---|
| launch · community · artefact | **`<project>/fli.resources.json`**, one file per project, each resource tagged with its `video` | same |
| affiliate | the slot is a resource here; the **link** stays in FliHub `brand-config.json` | a future affiliate app owns the catalogue; slots keep their `ref` |
| brand-wide links (Skool URL, socials, CTAs) | FliHub `brand-config.json` (read, never copied) | optional brand level `v-<brand>/fli.resources.json` (§9 Q3) |
| thumbnail images | wherever the generator writes them (thumbs-work: "output folder not decided") — the resource holds the path | a project folder for them (§9 Q6) |

**Why one file per project, not per video**: a title idea often exists before any `videos/<name>/` folder does, and a
single-video project needs no name at all. `video` is a field: a `videos/` folder name, or `null` for "the project's
video". The file sits at the project top next to `fli.words.json` (D1 naming: FliStudio's own file, `fli.<segment>.json`).

---

## 4. The record

One shape for every kind. Kind-specific detail goes in `meta` (stored as the producer wrote it) or `ref` (a pointer to
the producer's own record) — never new top-level fields.

```ts
// fli-core (proposed v0.12.0) — zod, like WordsFile
Resource = {
  id: string,                    // 'r_' + short random; stable; every verb names a resource by it
  kind: string,                  // 'title' | 'thumbnail' | … | any new word (§8)
  video: VideoFolderName | null, // which video; null = the project's (single) video
  title?: string,                // a human label ("Cool headshot, surprised")
  text?: string,                 // the value for text kinds (the title itself, a description)
  url?: string,                  // for web things (artifact, skool post)
  path?: string,                 // project-relative when inside the project, else absolute
  tags: string[],                // free words, lower-case; suggestions come from tags already used
  audience: ('youtube' | 'skool' | 'internal')[],
  status: 'candidate' | 'in-test' | 'chosen' | 'published' | 'retired',
  ref?: { schema: string, id?: string, file?: string }, // 'ylo.launch' t3 · 'thumbnail.generation' d03.a1.r1
  meta?: Record<string, unknown>, // the producer's payload, as-is (generation_record, chapters, tags)
  added: Stamp,                   // {at, by} — who added it (human:ui, cli, agent:tuber…)
  changed: Stamp,                 // who changed it last
}
ResourcesFile = { schema: 1, resources: Resource[] }
```

- `Stamp` is fli-core's (v0.11.0), the same as the word store's: `by` is the caller's principal.
- A resource never owns a file. Removing it removes the entry, never the image or the page.
- `status` is the only selection state in the whole system (thumbs-work and YLO's slot `locked` defer to it — §9 Q2).

---

## 5. Many candidates: titles and thumbnails

- **Store N.** There is no limit on candidates of any kind.
- **Statuses**:
  - `candidate` — an option;
  - `in-test` — one of the versions in YouTube's test-and-compare;
  - `chosen` — the one going live;
  - `published` — it went live;
  - `retired` — kept for history, hidden by default.
- **One chosen per video and kind**: choosing a title (or thumbnail, description, chapters, keywords) demotes the
  previous chosen one back to `candidate`, in the same write.
- **In test, not capped**: any number may be `in-test`. `resources.status` answers with a **warning** (not a refusal)
  when a video has more than 3 of a kind in test, because that is YouTube's limit today — and may not be tomorrow.
- **Pairing a title with a thumbnail** (YLO's "variant" story): tag both with the same word (`pair-a`), or use YLO's
  slots. Not a new field (§9 Q2).
- **Thumbnail metadata**: each thumbnail's `meta` is its `generation_record` — creative spec, settings, reference
  headshots by id, output files, quality flags. The UI shows the image from `path` and the rest behind an ⓘ.

---

## 6. Verbs (FliStudio, agent-open, on `/api/rpc`, the CLI and the screens)

Declared like the rest (`shared/src/contracts.ts` + `HANDLERS`); every write stamps the caller. David ruled on
2026-09-24 that agents may change anything as long as who and when are kept — so no ★ fence.

| Verb | Input | Does |
|---|---|---|
| `resources.list` | `{ brand, project, video?, kind?, group?, tag?, status?, all? }` | The matching resources, newest first; `retired` only with `all` |
| `resources.add` | `{ brand, project, video?, kind, title?, text?, url?, path?, tags?, audience?, status?, ref?, meta? }` | Adds one; answers the stored record with its `id` |
| `resources.update` | `{ brand, project, id, title?, text?, url?, path?, audience?, meta? }` | Changes fields (not kind, not status) |
| `resources.tag` | `{ brand, project, id, add?, remove? }` | Adds and removes tags |
| `resources.status` | `{ brand, project, id, status }` | Sets the status; `chosen` demotes the other chosen of that video + kind; warns past 3 `in-test` |
| `resources.remove` | `{ brand, project, id }` | Removes the entry (never a file) |
| `resources.kinds` | `{}` | The kind registry (§8) — so an agent knows what exists and what "value" each kind takes |

Refusals reuse the vocabulary: `project-not-found`, `video-not-found` (a `video` that is not a `videos/` folder and not
`null`), `invalid-input`, plus one new frozen code `resource-not-found`.

**Readers**: `video.text` gains the chosen title and description; apps read `fli.resources.json` themselves through a
fli-core `readResources()` (as with `readWords`), so nothing needs FliStudio running to read.

---

## 7. Who owns what, now and later

| Group | Writes the record | Produces the content | Later |
|---|---|---|---|
| launch | FliStudio (verbs) | Tuber (titles), YLO (titles, description, chapters, keywords), thumbs-work (thumbnails), David | YLO / a revived launch optimiser drives it through the same verbs |
| community | FliStudio | David (Skool posts), Claude sessions (downloads) | a Skool link-out when there is one — still just `url`s here |
| affiliate | FliStudio (the slot) | FliHub brand-config (the link) | a future affiliate app owns links; slots keep pointing |
| artefact | FliStudio | Claude sessions (artifacts, pages), David | — |

The **UI** is a Resources panel on the project page, per video (mock, §10). The **agent route** is the verbs — and is
the one David will use most.

---

## 8. How new ideas get in fast

- `kind` is **an open word**, not an enum. `resources.add { kind: 'shorts-hook' }` works today: the record stores it,
  the UI shows it in an "other" group with its text / url / path, and every verb handles it.
- The **kind registry** (group, label, value field, many?, choosing rule) is a data table in fli-core. Adding a row gives
  the kind its group and choosing rule. That is a code release of a list, not a migration — no file on disk changes.
- Anything a kind needs beyond `text`/`url`/`path`/`tags` goes in `meta`, so the file schema stays `1`.
- A new producer (a new agent, a new app) needs nothing but the verbs and a `ref.schema` name for its own record.

---

## 9. Decisions for David (each with a recommendation)

1. **FliStudio holds it, in `<project>/fli.resources.json`, one file per project with a `video` field per resource?**
   → **Yes.** The code agrees (§1). Per-video files break down for ideas made before a video folder exists.
2. **YLO's `launch.json` and this store — who holds "chosen"?** → **This store.** YLO keeps its workshop (scores,
   analysis, the 3 variant slots) and adds what it recommends as resources with `ref: ylo.launch`. One place answers
   "which title is live". Otherwise YLO's `locked` slot and FliStudio's `chosen` can disagree.
3. **Brand-wide links (Skool URL, affiliates) — move them out of FliHub's `brand-config.json`?** → **Not now.** Point
   at them (`ref: flihub.brand-config`). Move them when the affiliate app exists.
4. **The published title — FliHub's `.flihub-state.json title` or `status: published` here?** → **Here**, and FliHub
   reads it later (a FliHub ticket). Until then both exist and FliHub's is the one YouTube got.
5. **More than 3 in the YouTube test: refuse or warn?** → **Warn.** David: "don't cap it at 3".
6. **Where do thumbnail image files go?** → **Not decided here.** thumbs-work says the output folder is open; resources
   hold whatever path is written. Recommend `<project>/thumbnails/` when David picks.
7. **Is YLO's `launch.json` name OK?** It breaks D1 ("no generic names") — `fli.ylo.json` would fit. → YLO's call; flag
   only.

---

## 10. First real record (today, after approval)

Orch is confirming with David which project today's artefact belongs to (d05 `d05-flivideo-tour-take1` or d06
`d06-presenter-headshot-artefact`). With the store built, it is one call:

```json
{ "jsonrpc": "2.0", "id": 1, "method": "resources.add",
  "params": { "brand": "appydave", "project": "d06", "kind": "artifact", "title": "<artefact name>",
              "url": "https://claude.ai/artifact/<id>", "tags": ["shown-in-video"], "audience": ["skool", "internal"] } }
```

That is the general model's first instance: the same verb and file carry titles and thumbnails next.

## 11. Build plan (one pass, after approval)

1. fli-core v0.12.0: `Resource`, `ResourcesFile`, `ResourceKind` registry, `readResources`, pure `addResource` /
   `setStatus` (with the demote rule) / `tagResource` / `removeResource`, `writeResourcesFile`.
2. FliStudio: the 7 verbs, `resource-not-found`, the Resources panel (mock), `video.text` gains chosen title +
   description; tests on fixture estates.
3. Producers, each in its own window: Tuber (`resources.add` titles), thumbs-work (thumbnail + generation_record), YLO
   (recommended candidates), FliHub ticket (published title).

Out of scope: the launch optimiser itself, the affiliate app, any Skool integration, YouTube uploads.
