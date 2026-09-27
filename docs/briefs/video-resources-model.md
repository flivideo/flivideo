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
the mock (mock v2: https://claude.ai/artifact/GovQGoVjJ7McNEzGsXv1wL).

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
single-video project needs no name at all. `video` is a field: a video name in the `videos/` naming (kebab-case — the
folder need not exist yet), or `null` for "the project's video". The file sits at the project top next to
`fli.words.json` (D1 naming: FliStudio's own file, `fli.<segment>.json`).

**The kind registry lives in the same files, levelled like the word store** (§8): `kinds` and `groups` blocks in
`~/.config/appydave/fli.resources.json` (global, seeded with the standard kinds), `v-<brand>/fli.resources.json`
(brand) and `<project>/fli.resources.json` (project). One file shape at every level; `resources` is used at the project
level only for now.

**How you get to it (v2 of the mock)**: `RESOURCES <count>` in the rail's *In this project* group (the count is every
non-retired resource in the project, all videos), and a one-line summary on the project page — "Resources 11 · 5 chosen:
titles, thumbnails, description… · 4 titles · 4 thumbnails" — generated from the registry, which opens the panel.

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
// The registry — data, levelled global → brand → project, lower level wins on the same key
ResourceGroup = { group: string, label: string, order: number, changed: Stamp }
ResourceKind = {
  kind: string,                  // the key resources use
  group: string,                 // a ResourceGroup key; unknown → 'other'
  label: string,                 // "Shorts hooks"
  value: 'text' | 'url' | 'path' | 'image' | 'list' | 'chapters' | 'ref', // which renderer draws it (§8)
  many: boolean,                 // candidates expected
  choose: 'none' | 'one' | 'one+test' | 'published', // the choosing rule the verbs enforce
  hint?: string,                 // one line for the ⓘ and for agents
  changed: Stamp,
}
ResourcesFile = {
  schema: 1,
  groups: ResourceGroup[],       // may be empty at any level
  kinds: ResourceKind[],
  off: { kind?: string, group?: string, changed: Stamp }[], // a lower level hides an inherited row
  resources: Resource[],         // project level only (for now)
}
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
| `resources.kinds` | `{ brand?, project? }` | The merged registry (groups + kinds, each with the level it came from) — so an agent knows what exists and how each kind is valued and chosen |
| `resources.kinds.add` | `{ level, brand?, project?, kind? , group? }` | Adds or replaces a kind or group row at one level (stamped) |
| `resources.kinds.remove` | `{ level, brand?, project?, kind? , group? }` | Removes a row, or (for an inherited one) turns it off at that level |

Refusals reuse the vocabulary: `project-not-found`, `invalid-input` (a `video` that is not a kebab video name or
`null`), plus one new frozen code `resource-not-found`. A `video` whose folder does not exist yet is allowed — ideas come
first.

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

The **UI** is a Resources panel on the project page, per video (mock v2: https://claude.ai/artifact/GovQGoVjJ7McNEzGsXv1wL). The **agent route** is the verbs — and is
the one David will use most.

---

## 8. How new ideas get in fast

The panel, the summary line and every verb are driven by the **registry as data**; the only code is one renderer per
**value type** and one rule per **choosing rule**. The mock proves it: its second video (`guest-interview`) uses
`shorts-hook`, `sponsor-read`, `code-repo` and `guest-bio`, and the same function draws it.

**Exactly what changes when a new idea appears:**

| The new idea | Example | What changes |
|---|---|---|
| A new kind, and nobody has described it | `guest-bio` | **Nothing.** `resources.add { kind: 'guest-bio', text }` works; it shows under **Other**, drawn as text, choosing rule `none` |
| A new kind that should sit in a group, have a label or be chosen | `shorts-hook` (many, `one+test`) | **One registry row** — a file edit or `resources.kinds.add`, at the level it belongs to (project for a one-off, brand for AppyDave, global for everyone) |
| A new group | `sponsor` | **One group row** (plus its kinds' rows) |
| A kind that stops applying somewhere | no `skool-post` for a client brand | **One `off` row** at that brand |
| Extra data a kind needs | a sponsor read's deadline, a repo's branch | **Nothing** — it goes in `meta`, stored as given, shown behind the ⓘ |
| A new **value type** — a new way to *draw* a value | a playable audio clip, a timecode range on the video | **Code**: one renderer in the panel (and, if it is validated, its shape in fli-core). Until then the kind can use `text` or `url` and still work |
| A new **choosing rule** | "rank 1–5", "one per platform" | **Code**: one rule in `resources.status` |
| A new producer (agent, app) | a sponsor-tracking agent | **Nothing** — the verbs, plus a `ref.schema` name for its own record |

No file on disk is ever migrated for any of these: the file schema stays `1`.

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
8. **Which level does the standard registry live at?** → **Global** (`~/.config/appydave/fli.resources.json`, git-synced
   like `fli.words.json`), seeded once with §2's kinds. Brand and project rows only add or switch off. Alternative: ship
   the defaults in fli-core code — rejected, because then adding a standard kind needs a release.
9. **Where does "Resources" sit in the rail?** → **In *In this project*, after Videos, with a count**, plus the summary
   line on the project page (mock v2). Alternative: under *Do* — rejected, it is project material, not an action.

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

1. fli-core v0.12.0: `Resource`, `ResourceKind`, `ResourceGroup`, `ResourcesFile`, `readResources` (merging the
   registry global → brand → project), pure `addResource` / `setStatus` (the choosing rules) / `tagResource` /
   `removeResource` / `addKind` / `removeKind`, `writeResourcesFile`; the standard kinds as a seed file, not as code.
2. FliStudio: the 9 verbs, `resource-not-found`, the rail entry + summary line + a panel generated from the registry
   (renderers per value type), `video.text` gains chosen title + description; seed the global registry; tests on
   fixture estates, including a kind with no row and a project-level kind.
3. Producers, each in its own window: Tuber (`resources.add` titles), thumbs-work (thumbnail + generation_record), YLO
   (recommended candidates), FliHub ticket (published title).

Out of scope: the launch optimiser itself, the affiliate app, any Skool integration, YouTube uploads.
