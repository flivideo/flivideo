# Thumbnail system (v0, 2026-09-27)

**Purpose**: Turn the one-off 9-concept board (ChatGPT, 26 Sep) into a thumbnail method David can run again. The top priority is repeatability, not novelty.
**For Agents**:
- Start here for any "make thumbnails for dNN" request on AppyDave videos.
- v0 is untested. It becomes the basis for a skill or agent only after the **fresh-chat repeatability test** (below) passes.
- Separate from ThumbForge (`/Users/davidcruwys/dev/ad/apps/thumbforge-market-evidence/`, style exploration) and from the older skills (`appydave-thumbnail`, `ylo-thumb-prompt`, `ylo-thumb-text`). It takes ideas from them and replaces none of them.

---

## Where things are

| File | What |
|---|---|
| `schema.json` | the universal thumbnail spec, with a description for every field (a field dictionary, not a JSON Schema validator) |
| `brands/appydave.json` | AppyDave brand config (`brand.appydave.light.v1`): light mode forced, dark areas ≤25% and contained |
| `presenter/appydave.json` | presenter library manifest by role. Location TBD from portraits-rsch; interim fallback is the T7 cutouts |
| `rendering.json` | global rendering defaults (1280×720, one thumbnail per job, text composited afterwards) |
| `text-layer.json` | text-layer contract: `post_composite` by default, 64px minimum headline, must stay legible at 320×180 |
| `recipes.json` / `recipes.md` | the recipe library: 9 recipes in 6 layout families, generic with no video details |
| `execution-instructions.md` | the kickoff prompt to paste into a fresh chat ahead of the configs and a spec |
| `specs/d0N-aN-<recipe>.json` | the 9 filled specs, one per board tile (also regression examples: re-run them whenever the system changes) |
| `brief-format.md` | per-video input: fact sheet + `thumbnail_assets` |
| `source/board-2026-09-26.png` | the quality bar (the ChatGPT board) |
| `source/chatgpt-reply-2026-09-27.md` | ChatGPT's "why it worked" reply |
| `source/extraction-request-2026-09-27.md` | the message that asked ChatGPT for the method |
| `source/chatgpt-method-2026-09-27.md` | ChatGPT's raw answer, which the files above were built from |

Fact sheets for d01–d03 and the reference photos are in `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/thumb-research-2026-09-26/`.

## Run order

```
fact sheet ─► recipe pick ─► JSON spec ─► image ─► text layer ─► quality check ─► selection board
 (brief)      (recipes.md)   (schema +    (model)  (compositor    (spec's          (3 per video,
                              brand +               by default)    quality_checks)  David picks)
                              presenter)
```

1. **Fact sheet.** Write or refresh `dNN-factsheet.md` in the brief format, including `thumbnail_assets`. *Source:* the FliHub project transcripts plus the launch pack.
2. **Recipe pick.** Choose 3 *different* recipes from `recipes.md` that fit the video's "Strongest visual moments". Drop any recipe whose required assets are marked `need`. *Source:* the fact sheet.
3. **JSON spec.** Copy `schema.json`, fill it in for each chosen recipe, reference `brand: appydave` and a presenter role, and save it as `specs/dNN-aN-<recipe>.json`. *Source:* recipe + fact sheet + brand config.
4. **Image.** In a **fresh** chat, paste `execution-instructions.md`, then brand + presenter + rendering + text-layer configs, then the spec; attach only the assets its `assets` block lists. Background and scene only, no headline. *Source:* spec + portrait library + real screenshots.
5. **Text layer.** Overlay the headline afterwards as the spec's `text_layer` says (compositor default). *Source:* `headline_candidates` in the fact sheet.
6. **Quality check.** Run the spec's `quality_checks`: identity, technical accuracy, brand/light mode, and readability at 160px wide. Flag failures instead of quietly accepting them.
7. **Selection board.** 3 finished thumbnails per video. David picks, asks for a variation, or approves several for A/B.

## Inputs and where they come from

| Input | Frequency | Location |
|---|---|---|
| Brand rules | once | `brands/appydave.json` (derived from the `brand-dave:brand` skill) |
| Presenter portraits | once, refreshed | **portrait library: location TBD from portraits-rsch.** Interim fallback: `/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/` (106 cutouts; search `…/headshots-manifest.json`). The T7 is external: a missing path means it's unmounted, not deleted. |
| Recipes | once, grows | `recipes.md` |
| Fact sheet + `thumbnail_assets` | every video | `…/docs/briefs/<batch>/dNN-factsheet.md` |
| Real screenshots / frames | when the recipe needs them | listed in `thumbnail_assets` |
| Approved title/headline | when finalised | fact sheet |

## Presenter slot (pluggable)

Specs never embed or upload photos. They name a **role** (e.g. `surprised`, `pointing-right`) plus an optional file id. The library is resolved at run time: the portraits-rsch location once it's decided, otherwise the 2024 cutouts. Changing the library changes no spec.

## Status and next step

- v0 was built from ChatGPT's own account of the board. **None of it has been re-generated yet.**
- **Next: the repeatability test.** Paste ONE spec (suggest `specs/d03-a1-detection-overlay.json`, the most readable concept, whose one required asset, `headshot-appydave-23.png`, already exists) into a *fresh* ChatGPT conversation with no history, attach only its listed assets, and compare the result with the board tile. Pass means board quality with no chat history. Only after a pass: build the skill or agent.

## Edits made on top of ChatGPT's output

- **Fonts:** ChatGPT proposed Inter 900. Replaced with AppyDave's Bebas Neue for headlines (single weight, 400) and Oswald 700 for labels, per `brand-dave:brand`.
- **Presenter library:** portrait `path` placeholders kept. Added `file_id` plus an `interim_path` into the T7 cutouts or the upload pack.
- **Specs:** each gets `video.fact_sheet` → the absolute fact-sheet path.
- ChatGPT's own caveat: coordinates, font sizes and lighting are *new production decisions*, not measurements of the board. The board was one image, so these specs aim to reproduce its creative direction, not its pixels.
- Poses the library doesn't have yet (`pointing_left/right`, `concerned`, `listening`) are marked `missing`. `d02-a3` relies on `listening`.
