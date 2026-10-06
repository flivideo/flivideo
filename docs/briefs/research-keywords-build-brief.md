---
type: brief
title: Research for video projects: keywords (build brief)
description: "Self-contained work order to build FliVideo's Research capability, module 1 keywords, inside FliStudio: free sources only, research.* verbs, resource kinds, phases with acceptance criteria, risks, and the one-time setup David does by hand."
created: 2026-10-06
status: ready for build — not started; needs David's go
---

# Build brief: Research for video projects, module 1: keywords

**Purpose**: Everything a build agent needs to build keyword research into FliStudio with no further research.

**For Agents**:
- Build in FliStudio (`/Users/davidcruwys/dev/ad/flivideo/flistudio/`), on the M4, as a new capability family `research.*`. Follow FliStudio's existing capability pattern (`bin/flistudio list` shows the conventions; spec: `docs/specification.md`; system: `docs/SYSTEM.md`).
- Evidence and reasoning (read before Phase 1):
  - Sources: `/Users/davidcruwys/dev/ad/brains/ylo/research/video-keyword-sources-2026-10-06.md`
  - Live samples: `/Users/davidcruwys/dev/ad/brains/ylo/research/video-keyword-sources-2026-10-06/`
  - Design: `/Users/davidcruwys/dev/ad/brains/ylo/research/research-capability-design-2026-10-06.md`
- **Out of scope**: paid sources (vidIQ, TubeBuddy, Keywords Everywhere, DataForSEO, Semrush/Ahrefs); browser automation of Studio, TikTok or Pinterest; changing D03; editing YLO skill files (propose those changes in a note instead).

## Goal

An agent working on a video project can ask "which phrases do people actually type on YouTube for this topic?" and "what did people search to find our last videos?". It gets answers stored on the project as resources, each with its source and timestamp. Tuber and the YLO skills use those answers for titles, the first lines of descriptions, tags and hashtags. Free sources only. Agents use verbs, never folders.

## Free source stack, in priority order

| # | Source | Phase | Official? | Auth |
|---|---|---|---|---|
| 1 | YouTube autocomplete `suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=&gl=&q=` | 1 (MVP) | **no**, undocumented | none |
| 2 | YouTube Analytics API: `insightTrafficSourceDetail` filtered `insightTrafficSourceType==YT_SEARCH`, `maxResults≤25`, `sort` required | 1 (MVP) | yes | OAuth, scope `yt-analytics.readonly` |
| 3 | YouTube Data API v3 `search.list` (100 calls/day, 1 unit each) + `videos.list` (1 unit, from 10,000/day) | 2 | yes | API key |
| 4 | Manual imports: Studio Trends tab (screenshot/paste), Keyword Planner (CSV), TikTok/Pinterest (screenshot) | 2 | n/a | David's own logins |
| 5 | Google Trends, YouTube filter, unofficial `/trends/api/explore` → `/widgetdata/multiline` with `property: youtube` | 3, **off by default** | **no** | none |

Sources 1 and 5 can disappear or be blocked at any time. Build them as separate adapters behind a per-brand switch.

## Verbs and data shapes

Use the verb table, resource kinds and JSON shapes in the design doc, section "Verbs" onward. Summary:

- `research.sources` (read-only) · `research.view` (read-only) · `research.ledger` (read-only)
- `research.keywords.suggest` · `research.keywords.rank` · `research.searchterms.pull` (Phase 1)
- `research.similar` · `research.import` (Phase 2) · `research.trend` (Phase 3)
- All take `--brand`, `--project`, `--as agent:<name>`; all are exposed on JSON-RPC `POST /api/rpc`.
- Storage only through the resources layer (`resources.add` internally): new group `research` with kinds `keyword-research`, `search-terms`, `similar-videos`, `research-import`; ranked output goes to the **existing** `keywords` kind as status `candidate`.
- Every observation carries `source`, `official`, `signal`, `value`, `unit`, `read_at`, `request`. **Never** write an autocomplete rank into a `score` or `monthly_searches` field.

## Phases

### Phase 0: setup (David, by hand; about 20 minutes, only needed for Phase 1's search terms)
See "What David sets up by hand". Phase 1's autocomplete half needs no setup and can start at once.

### Phase 1: MVP: autocomplete + own-channel search terms
Build: the `research` group and kinds; `research.sources`, `research.keywords.suggest` (with `expand: alphabet`), `research.keywords.rank`, `research.searchterms.pull`, `research.view`, `research.ledger`; the OAuth token handling (refresh token stored under `~/Library/Application Support/flistudio/research/`, never in a repo); caching and throttling.

Acceptance:
1. `flistudio research.keywords.suggest --brand appydave --project <test project> --as agent:test` with seeds "face tracking" and "AI video graphics" stores one `keyword-research` resource. `resources.list --kind keyword-research` shows it. Its observations include the phrases in the evidence samples (lists may drift day to day; check overlap, not equality).
2. A seed with no completions is stored with zero observations and listed under `unmeasured`. No error.
3. A second identical call the same day makes **no** network request (cache hit visible in `research.sources`).
4. A 429 or network failure is recorded in the resource's `errors[]` and in `research.sources`; the verb still returns cleanly.
5. `research.searchterms.pull --video <a published AppyDave video> --window 28d` stores ≤25 terms with views, appends them to `research.ledger`, and refuses a video with no `youtubeId` (`not-published`).
6. With no OAuth token, `research.searchterms.pull` refuses with `auth-missing` and a one-line fix; `research.sources` shows it as not ready.
7. `research.keywords.rank` writes a `keywords` resource with status `candidate`, `meta.items` and `meta.evidence`. Every evidence row maps to the YLO `description.keywords[]` fields. Nothing is chosen or approved.
8. No file is written inside a project folder except through the resources layer. Secrets appear in no resource, log or repo (check with `grep`).
9. `bin/flistudio list` shows the new verbs with their classes; the schema mirror and SYSTEM/spec docs are updated as FliStudio's own rules require.

### Phase 2: similar videos + manual imports
Build `research.similar` (Data API; budget 100 searches/day; snapshots expire after 30 days) and `research.import` (screenshot, CSV or paste kept as a `research-import` resource marked `manual`).

Acceptance:
1. `research.similar --phrase "ai motion graphics"` stores ≤25 videos with title, channel, views and publish date, using 1 search call + 1 `videos.list` call.
2. The daily search-call count is tracked and the verb refuses at 100 with `quota-exhausted`.
3. Snapshots older than 30 days are refreshed or removed by a sweep.
4. `research.import --source keyword-planner --file <csv>` stores `volume-range` observations as given, unchanged. `--source studio-trends --file <png>` stores the image plus any phrases typed in, marked `manual`.

### Phase 3: trends (opt-in) + post-publish loop automation
Build `research.trend`, refusing unless the brand setting `research.allowUnofficial` is `true`. Add a scheduled pull of search terms at +7 and +28 days after `publish.mark-published`. Ledger terms feed the next project's seeds.

Acceptance:
1. With the switch off, `research.trend` refuses with `source-disabled`.
2. With it on, it stores a 0–100 weekly series labelled `relative-interest`, `official: false`.
3. Publishing a test video schedules two pulls; their results reach `research.ledger`; the next `research.keywords.suggest` on the same brand includes overlapping ledger terms as seeds.

## Consumers (describe; YLO edits are separate)

- Tuber: `research.sources` → `video.text` → `research.keywords.suggest` → `research.keywords.rank` → titles.
- `ylo-description` §0b: read `research.view` in place of vidIQ screenshots; screenshots become `research.import`.
- `ylo-analyse` P08: becomes seeds.
- `ylo-publish` P4: hashtags from measured phrases only.

Write these as a proposed-change note in the YLO plugin's notes, for David to approve. Don't edit the skills.

## Risks

| Risk | Likelihood | Effect | Mitigation |
|---|---|---|---|
| Autocomplete endpoint changes or blocks | medium | MVP loses its main pre-publish signal | adapter isolation; record errors; manual import fallback |
| YouTube Developer Policies: "must not use undocumented APIs" applies once FliStudio is a registered API client | medium | policy breach on the official-API project | separate adapters, per-brand off switch, no shared Google Cloud key used for the undocumented calls; David decides whether to keep source 1 on |
| Unofficial Trends tagged `USER_TYPE_SCRAPER`, 429s | high | Phase 3 flaky | off by default; never on the MVP path |
| OAuth refresh token expires in 7 days while the consent screen is "Testing" | high if left in Testing | search-terms pulls stop silently | set the app "In production"; `research.sources` shows token age and fails loudly |
| `search.list` limit is 100/day | certain | caps Phase 2 | cache; budget counter; refuse at the limit |
| Analytics top-25 cap per query | certain | long tail invisible | pull per video and per window; the ledger aggregates |
| Studio Trends tab has no API (unverified absence) | — | manual only | `research.import` |
| Keyword Planner needs billing details; low spend may show ranges (unverified) | — | rough web numbers only | optional manual CSV import; label as web, not YouTube |

## What David sets up by hand

1. **Google Cloud project** (free): enable **YouTube Analytics API** (Phase 1) and **YouTube Data API v3** (Phase 2).
2. **OAuth consent screen**: External, add himself as a test user, then **publish to "In production"** to avoid 7-day refresh-token expiry (Google's OAuth docs). Expect the "unverified app" warning on his own consent. Whether Google requires verification for this scope is unverified, so check on the console.
3. **OAuth client** of type Desktop app. Hand its client JSON to the build agent's setup step by **file path**, not by pasting into chat. Then run the one-time consent as the AppyDave channel owner (`research.auth.login` or a setup script the builder provides).
4. **API key** for the Data API (Phase 2), restricted to the YouTube Data API.
5. **Optional**: a Google Ads account with billing details entered, for Keyword Planner manual exports. Not needed for any phase's acceptance.
6. **Decide** whether the undocumented autocomplete adapter stays on for AppyDave (recommended: on, with the risk above accepted), and whether Phase 3 Trends is ever turned on (recommended: off).
7. Prior art to check before writing OAuth code: `/Users/davidcruwys/dev/ad/appydave-tools/lib/appydave/tools/youtube_manager/authorization.rb` (not reviewed in research).
