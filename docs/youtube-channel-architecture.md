# YouTube channel sync, brand publishing settings and playlists — architecture

**Purpose**: Decide where YouTube channel data, per-brand publishing settings and credentials live in the Fli suite, and the shape of the local mirror, before the read side is built.
**For Agents**: Read before touching YouTube sync, brand publishing settings (CTAs, affiliates, playlists) or the Launch Playlists step. Status: **proposal, awaiting David's go** (2026-10-06). Brief: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/youtube-channel-sync-brief-2026-10-06.md`.

Already approved by David (not re-argued here): **mirror, not live**; a brand **YouTube** page in FliStudio; Launch's Playlists step offers the brand's real playlists; **writing back to YouTube is later**.

## Decisions at a glance

| # | Question | Decision |
|---|---|---|
| 1 | Where does sync live? | A `youtube` module in **fli-core** (API client + mirror reader/writer + schemas), driven by **FliStudio capabilities** `youtube.*`. yt-mirror is retired after its logic is ported. |
| 2 | Brand publishing settings' home | A `publish` block in each brand's **`fli.brand.json`** (git-tracked brand root), copied verbatim from FliHub's brand-config, plus a `youtube` block for playlist choices. Mirrored YouTube facts never go in it. |
| 3 | Keys and auth | One suite-wide read **API key** in `~/.secrets` (env name only in code). Later, OAuth: one Google "Desktop app" client, a **refresh token per channel** outside git. Nothing secret in brands.json or fli.brand.json. |
| 4 | Mirror shape | Per brand: `channel.json`, `playlists.json` (with members), `videos/<id>/…`, `sync.json`. Full re-list each sync; ~25–45 quota units per channel. |
| 5 | Freshness | "Sync now" (capability) + optional daily launchd job calling the FliStudio CLI. Age shown on the page; amber after 7 days. |
| 6 | Joins | `youtubeId` from `publish.published` ↔ mirrored video id. Playlist membership read from the mirror on both sides. |

---

## 1. Placement

### What exists

- **yt-mirror** (`/Users/davidcruwys/dev/ad/apps/yt-mirror/`): ~390 lines of Bun/TS. **Not a git repo, not registered, not scheduled**; last run 2026-05-09. Calls `channels` (forHandle), `playlistItems` (uploads), `videos` with a read API key. No playlists. Its "etag" is a home-made `views:likes:comments` string, not the HTTP ETag.
- **fli-core** (`@flivideo/core`, consumed as `github:flivideo/fli-core#vX`): already holds the shared contracts this needs — `brands.ts` (`readBrands`, `resolveBrandRoot`), `brand-settings.ts` (`fli.brand.json` schema, `readBrandSettings`/`writeBrandSettings`), `publish.ts` (`markPublished`, the `youtubeId` join), and the FliTools client.
- **FliTools** (:7161, launchd): a long-running tool shelf for slow, queued, one-at-a-time work (transcription). Owns transcription.
- **FliStudio**: the front door. Agents call capabilities over HTTP JSON-RPC (`flistudio/docs/AGENT-NOTES.md`); a capability is declared in `shared/src/contracts.ts` + `server/src/capabilities/registry.ts`; module boundaries enforced by dependency-cruiser.

### Options

| Option | For | Against |
|---|---|---|
| **A. fli-core `youtube` module + FliStudio `youtube.*` capabilities** | Same pattern as publish/series/brand-settings: core owns the files and schema, FliStudio is the door. FliHub, YLO and FliLaunch can read the mirror through the same library. One repo to version. | fli-core grows one module; needs a tag bump. |
| B. New `@flivideo/youtube` package | Clean separation. | A new repo, tag and release chain for ~500 lines; the mirror schema is a shared contract like the others in core. |
| C. FliTools service | Always-on, could own a schedule. | FliTools is for slow queued jobs; a sync is ~40 cheap HTTP calls. Adds a second door for agents (they must go through FliStudio). |
| D. Keep yt-mirror standalone, FliStudio shells out to it | No porting. | Not in git, not tested in-suite, a Bun process spawned from a Node server, and a second home for YouTube logic. |

**Recommendation: A.** Port yt-mirror's logic (channel resolve, uploads paging, video batching, thumbnails) into `fli-core/src/youtube/` with an injectable `fetch` (yt-mirror already does this, so its tests port too), add playlists. FliStudio adds a `youtube` server module (depends on fli-core only, like `estate`) and `capabilities/youtube.ts`. yt-mirror is left in place, unused, and David is told; delete only on his word.

**Reason:** every other shared Fli file (brand registry, brand settings, publish state, series) already follows "core owns the file and schema, FliStudio exposes it". The mirror is the same kind of thing, and agents get it through the existing door for free.

---

## 2. Brand publishing settings' new home

### What exists

- `/Users/davidcruwys/dev/ad/flivideo/flihub/server/brand-config.json`: **AppyDave only**, not keyed by brand. `brand`, `socialLinks`, `ctas {primaryCta, foldCta}`, `affiliates[6]`, `playlists` (10 `camelKey → playlistId`, no titles), `descriptionTemplate {legalDisclosure, endNote}`, `_meta` (2025-12-03, extracted from a Dropbox template).
- POEM copy `/Users/davidcruwys/dev/ad/poem-os/poem/data/youtube-launch-optimizer/config/brand-config.json`: **same content** (only key order and the trailing newline differ).
- `fli.brand.json` exists at all 10 brand roots (`/Users/davidcruwys/dev/video-projects/v-<brand>/`, each its own git repo). Schema is in fli-core (`schema, brand, colour, transcription?, gitignore?`). No code writes it yet.
- FliStudio's launch "brand defaults" (category, audience, language, `playlists: []`) are **hard-coded** in `flistudio/server/src/capabilities/launch.ts:87-97`.
- `~/.config/appydave/channels.json`: a second brand model; **only read by Ruby appydave-tools**. Its `@appydavelabs` handle disagrees with brands.json's `claudinglab`.

### Options for the home

| Option | For | Against |
|---|---|---|
| **A. `publish` + `youtube` blocks in each brand's `fli.brand.json`** | Already per brand, git-tracked, schema and atomic writer already in fli-core, already read by FliStudio and FliTools. | Brand repos must be committed when settings change (that is the point: managed). |
| B. brands.json | One file. | Identity registry in a private config repo; mixing long marketing text into it bloats every reader; fli-core's `Brand` type strips unknown fields. |
| C. New `fli.publish.json` per brand | Separates concerns. | A second per-brand file for the same owner, with no gain over a block. |

**Recommendation: A.** brands.json stays **identity** (key, name, `youtube_channel_id`, `youtube_handle`) and is the pointer: brand key → brand root → `fli.brand.json`.

### Field split

| Field | Kind | Where |
|---|---|---|
| Channel id, handle | identity | brands.json (already there) |
| Channel title, stats, playlist list (id, title, count, privacy), membership, videos | **mirrored** from YouTube | the mirror (§4), never hand-edited |
| CTAs, affiliates, social links, legal disclosure, end note, brand bio | **authored** | `fli.brand.json` → `publish` (verbatim shape of brand-config) |
| Which playlists are *active* for the brand; the usual picks for a new video | **authored** | `fli.brand.json` → `youtube.activePlaylists`, `youtube.defaultPlaylists` (playlist **ids**) |
| Studio defaults (category, audience, language) | authored | `fli.brand.json` → `studioDefaults` (replaces the hard-coded `BRAND_DEFAULTS`) |

Sketch (v-appydave):

```json
{
  "schema": 1, "brand": "appydave", "colour": "#ffde59",
  "publish": { "brand": {…}, "socialLinks": {…}, "ctas": {…}, "affiliates": […], "playlists": {…10 legacy keys…}, "descriptionTemplate": {…},
               "_meta": { "source": "flihub/server/brand-config.json (from Dropbox/team-awb/awb-appydave/-outcome-template.md)", "migratedAt": "2026-10-…", "lastUpdated": "2025-12-03" } },
  "youtube": { "activePlaylists": ["PL…"], "defaultPlaylists": ["PL…"] },
  "studioDefaults": { "category": "26 Howto & Style", "audience": "Not made for kids", "language": "English" }
}
```

`publish` keeps brand-config's exact shape so FliHub's existing mapper reads it unchanged. The 10 legacy `playlists` keys seed `youtube.activePlaylists` once (ids that the mirror still finds); the legacy map stays for provenance. aitldr and appydavelabs start with an empty `publish` block (no authored config exists for them today).

### Migration and repointing (old files are kept until David is told)

| Consumer | Change |
|---|---|
| FliHub `server/src/utils/poemWuiUtils.ts` `loadBrandConfig` | First source becomes `<appydave brand root>/fli.brand.json` `.publish`; the bundled file stays as fallback. FliHub's Brand tab editor becomes read-only with "edit in FliStudio" (FliStudio's brand page owns edits). Tests updated. |
| YLO `appydave-plugins/ylo/references/brand-input-contract.md` (+ the `ylo-description` skill's "never edit" note) | Repoint the path to `v-appydave/fli.brand.json` `.publish`; preferred: read through FliStudio (`brand.settings` capability, Part B). |
| POEM copy | Leave the file; add a `_meta.supersededBy` pointer note. POEM has no loader code (docs/prompts only). |
| `channels.json` | Not retired in this run (Ruby appydave-tools still reads it). Add `meta.supersededBy: brands.json`. |
| FliStudio `launch.ts` `BRAND_DEFAULTS` | Read `studioDefaults` + `youtube.defaultPlaylists` from `fli.brand.json`; the code constants become the fallback. |

Writes to `fli.brand.json` go through fli-core `writeBrandSettings` (whole-file atomic), so the schema in `brand-settings.ts` gains the three optional blocks (fli-core tag bump).

---

## 3. Keys and auth per brand

Facts (official docs, cited below):

- Public reads work with an **API key**. `mine=true` "can only be used in a properly authorized request" (OAuth) — [playlists.list](https://developers.google.com/youtube/v3/docs/playlists/list).
- `captions.download` needs OAuth (`youtube.force-ssl`), "requires the user to have permission to edit the video", and costs **200 units** — [captions.download](https://developers.google.com/youtube/v3/docs/captions/download).
- Every write (`playlistItems.insert`, `playlists.insert`, `videos.update`) costs **50 units** and needs OAuth — [quota costs](https://developers.google.com/youtube/v3/determine_quota_cost).
- Desktop apps: **loopback redirect + PKCE**; store the refresh token "in a secure, long-lived location"; losing it means repeating consent — [OAuth for installed apps](https://developers.google.com/youtube/v3/guides/auth/installed-apps).
- Quota is **per Google Cloud project**, 10,000 units/day shared across every endpoint except search/insert — [quota costs](https://developers.google.com/youtube/v3/determine_quota_cost).

The docs **do not say** whether `playlists.list?channelId=` with an API key includes private/unlisted playlists. Expectation: public only. Part B measures it on the three channels and reports.

**Decision (read phase, now):** one suite-wide key, `YOUTUBE_API_KEY`, in `~/.secrets` (the existing 600-permission env file). Not per brand: public reads don't need the channel owner, and quota is per Cloud project, not per key. FliStudio reads the key from its environment (`StudioConfig.youtubeApiKey`); yt-mirror's `.env` key is reused (moved to `~/.secrets` after confirming with David). Missing key → `youtube.sync` refuses with a clear code; reads of the mirror still work.

**Plan (write phase, later, not built):**

- One OAuth client (type "Desktop app") in the same Cloud project; client id/secret in `~/.secrets`.
- **One refresh token per channel**, gained by the channel owner signing in once through a `youtube.connect` human-only capability (loopback + PKCE, scope `youtube.force-ssl`). Stored outside git in the macOS Keychain (service `flivideo.youtube`, account = brand key); fallback `~/.config/flivideo/youtube-tokens/<brand>.json` at mode 600, git-ignored and outside any repo.
- brands.json only ever holds the **non-secret** channel id. `fli.brand.json` never holds credentials.
- Writes are human-only capabilities (`youtube.playlist.add`, …); agents propose, a person approves.
- With a token, sync can switch to `mine=true` and see private/unlisted items.

---

## 4. Data shape of the mirror

**Location:** `/Users/davidcruwys/dev/video-projects/published/<brandKey>/` (outside git; it is a regenerable cache). Keyed by **brand key**, not handle — handles change (`claudinglab` → AppyDave Labs). The existing `claudinglab/` folder is renamed to `appydavelabs/` on first sync; `appydave/`, `aitldr/` already match. Root is `StudioConfig.youtubeMirrorRoot` so tests use a fixture.

```
published/<brandKey>/
  channel.json        { id, handle, title, description, publishedAt, uploadsPlaylistId, subscriberCount, viewCount, videoCount, fetchedAt }
  playlists.json      { fetchedAt, playlists: [ { id, title, description, itemCount, privacy, publishedAt, thumbnail, etag,
                                                  items: [ { videoId, position, addedAt, videoPublishedAt } ] } ] }
  videos/<id>/
    metadata.json     { id, title, description, publishedAt, duration (ISO 8601), privacy, tags, categoryId, thumbnails{…}, statistics{…}, fetchedAt }
    thumbnail.jpg
    transcript.txt    (best effort, see below)
  sync.json           { lastSyncAt, ok, durationMs, quotaUnits, counts { videos, playlists, memberships }, warnings[], by (Stamp) }
```

YouTube's playlist resource has no "updated at"; the mirror keeps the HTTP `etag` per playlist and the `fetchedAt` of the list.

**Calls per channel sync** (each 1 unit — [quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)):

| Call | Count |
|---|---|
| `channels.list` `forHandle` / `id`, part `snippet,statistics,contentDetails` ([channels.list](https://developers.google.com/youtube/v3/docs/channels/list)) | 1 |
| `playlistItems.list` on the uploads playlist, 50/page | ⌈videos/50⌉ |
| `videos.list` `id=` 50 per call, part `snippet,contentDetails,status,statistics` ([videos.list](https://developers.google.com/youtube/v3/docs/videos/list)) | ⌈videos/50⌉ |
| `playlists.list` `channelId`, part `snippet,contentDetails,status`, 50/page | ⌈playlists/50⌉ |
| `playlistItems.list` per playlist, part `contentDetails,snippet` ([playlistItems.list](https://developers.google.com/youtube/v3/docs/playlistItems/list)) | Σ⌈items/50⌉ |

Estimate: appydave (183 videos) ≈ 1+4+4+1+~15 ≈ **25**; aitldr (324) ≈ 1+7+7+1+~20 ≈ **36**; appydavelabs (48) ≈ **10**. About **70 units for all three = under 1% of the day's 10,000.** Part B measures and reports the real number in `sync.json.quotaUnits`.

**Incremental:** send `If-None-Match` with stored ETags; a 304 means "not changed" — [getting started](https://developers.google.com/youtube/v3/getting-started). The same page says "All API requests, including invalid requests, incur at least a one-point quota cost", so ETags save bandwidth and rewrites, **not quota**. Given ~70 units, every sync re-lists everything; ETags only skip rewriting unchanged files, and thumbnails download only when the URL changes. No `search.list` (100/day cap).

**Transcripts:** `captions.download` is OAuth-only and 200 units — not used. yt-mirror's existing route (the `youtube-transcript` scraper, unofficial) is kept as an **opt-in, best-effort** step for videos without one; existing `transcript.txt` files are kept. Videos made in FliStudio already have FliTools transcripts in their projects, which remain the authority (FliTools owns transcription).

---

## 5. Freshness

- **Sync now**: `youtube.sync { brand }` — the only non-read capability. Open to agents (it only refreshes a cache) but refuses if the brand synced in the last 10 minutes, to protect quota.
- **Schedule (optional, off by default)**: a launchd job that runs `bin/flistudio youtube.sync --brand all` daily. CLI, not a server timer, because FliStudio isn't always running; launchd setup only with David's go.
- **Staleness shown**: "last synced 3 days ago · sync now" on the brand YouTube page and next to the Launch playlist list; amber after 7 days, plus "never synced" and the last error (`sync.json.ok:false`).
- Writes to the mirror are picked up by FliStudio's estate watcher pattern; no announcements from handlers.

---

## 6. Joins

- **Video ↔ project:** `publish.published { brand }` already lists `youtubeId` per project (stored by `publish.mark-published` in the project's `fli.resources.json`). `youtube.videos { brand }` returns each mirrored video with `project` (code, name) when a `youtubeId` matches, else `null` ("not made in FliStudio", e.g. older uploads).
- **Playlist membership both sides:** the brand page shows each playlist's members (linked to projects). A published project's Launch/publish view shows "in playlists: …" from the mirror. Before it is published, the Launch step's picks (`StudioSettings.playlists`) are **intent**; it stores playlist **ids** (titles come from the mirror) so a later write phase can act on them directly.
- A published video whose `youtubeId` isn't in the mirror yet shows "not in the last sync — sync now".

---

## Part B build plan (after go)

1. fli-core: `src/youtube/` (client, mirror read/write, zod schemas), `brand-settings.ts` gains `publish`, `youtube`, `studioDefaults`; tests; tag.
2. Migrate brand-config → `v-appydave/fli.brand.json` (verbatim + `_meta`); empty blocks for aitldr, appydavelabs.
3. FliStudio: `youtube` module + capabilities `youtube.channel`, `youtube.playlists`, `youtube.videos` (read), `youtube.sync`, `brand.settings` / `brand.settings.set` (playlist toggles); brand YouTube page; Launch Playlists step with real tick boxes, defaults pre-filled, agent proposal shown as a suggestion.
4. Repoint FliHub and YLO's doc; pointer notes on the POEM copy and channels.json.
5. Live sync on aitldr, appydave, appydavelabs; report playlists, videos, memberships and quota per channel; confirm the appydavelabs handle.

Out of scope: OAuth, any write to YouTube, Studio fill, deleting old files.

## Open points to check in Part B

- appydavelabs handle: brands.json says `claudinglab`, channels.json says `@appydavelabs`. Sync resolves by **channel id** (`UCLyscJVSp1l_V6gZg5F5wZg`), which settles it, and corrects brands.json's handle.
- Whether the API key sees private/unlisted playlists (see §3).
- Local fli-core clone is one tag behind origin (v0.18.0 vs v0.19.0); pull before building.
