# YouTube channel sync, brand settings and playlists — architecture + build brief

**Purpose**: Hand-off for a fresh session to design where YouTube channel data and brand publishing settings live in the Fli suite, then build the read side (sync → brand YouTube page → Playlists step) and test it on three channels.
**For Agents**: Read in full before acting. This brief is self-contained and written for a session with no access to the chat that produced it. Commissioned by David 2026-10-06, written by `flivideo-orch`.

## Why this exists (David, 2026-10-06)

- On FliStudio Launch's **Playlists** step: *"The whole concept of playlists is a user interface without any practical implementation… I don't have a place to configure the playlists. I've got no way to synchronise playlists to what's really going on… no way to store playlists against the brand."*
- *"From an architecture perspective, is it going to be live connected to an API, or what's going to go on?"*
- *"I don't think the brand even knows what the YouTube channel is."* (Partly fixed; see the facts below.)
- On the brand config: *"It doesn't make any sense in FliHub anymore, now that we have FliTools and FliStudio. Where you put it, I don't know, but it's not a FliHub thing anymore. It's probably not managed."*
- *"I think we need something way more connected to YouTube and APIs and API keys for each of the brands somehow."*
- *"Is it a common library thing? Is it part of FliStudio? Is it part of FliTools? I don't know."* That placement is **your first job**.
- *"We're not using Ruby."* Don't build on appydave-tools' Ruby youtube_manager.
- Testing: *"do both the AITLDR and the AppyDave version, maybe even the Clauding Lab, which is not called that anymore"* (it's now **AppyDave Labs**, brand key `appydavelabs`, handle still `claudinglab`).

## What David has already approved (his "SURE"s)

1. **Mirror, not live.** A sync step pulls channel, videos and **playlists with their members** into a local copy, on a button press or a schedule. YouTube stays the truth; Fli apps read the local copy (fast, offline, reachable by agents through FliStudio's front door).
2. **A brand "YouTube" page in FliStudio:** the channel, its playlists (name, video count, which ones the brand actively uses), and every published video, each linked to its FliStudio project where one exists. Plus "last synced <age> · sync now".
3. **Launch's Playlists step** offers the brand's real playlists as checkboxes. Tuber (agent) can propose; the brand's usual picks are pre-filled.
4. **Writing back to YouTube is LATER** (adding to a playlist, Studio fill). It's out of scope for this run, but the design must leave room for it (OAuth per channel).

## Facts found (verified 2026-10-06 by flivideo-orch)

| Thing | Where | State |
|---|---|---|
| Channel mirror app | `/Users/davidcruwys/dev/ad/apps/yt-mirror/` (Bun/TS: `src/youtube-api.ts`, `archiver.ts`, `sync-state.ts`, `transcripts.ts`, `thumbnails.ts`; `scripts/archive.ts`) | Read-only `YOUTUBE_API_KEY` in its `.env`; `CHANNEL_HANDLES=aitldr,appydave,claudinglab`. Writes `~/dev/video-projects/published/<handle>/{channel.json,last-sync.json,videos/<id>/{metadata.json,thumbnail.jpg,transcript.txt}}`. **Last sync 2026-05-09** (5 months stale). **No playlists.** |
| Mirrored channels | `/Users/davidcruwys/dev/video-projects/published/` | appydave UC3fDZp6BryiFmBzVChBTlNg (183 videos) · aitldr UC8vD5DvNTh03eID8iOl07XQ (324) · claudinglab UCLyscJVSp1l_V6gZg5F5wZg (48) |
| Brand registry | `~/.config/appydave/brands.json` (private git repo appydave-config) | CANONICAL brand identity. `youtube_channel_id` + `youtube_handle` were added for appydave/aitldr on 2026-10-06 (commit 61f7842); appydavelabs already had its id. |
| Channels registry | `~/.config/appydave/channels.json` | Names only, a 2nd model of the same thing. Reconcile or retire it; brands.json wins. |
| **Brand publishing config** (CTAs, affiliates, **10 playlist IDs**, description template, legal) | `/Users/davidcruwys/dev/ad/flivideo/flihub/server/brand-config.json` | `_meta.lastUpdated 2025-12-03`, "extracted from Dropbox/team-awb/awb-appydave/-outcome-template.md". Unmanaged, and in the wrong app. A 2nd copy is in POEM: `/Users/davidcruwys/dev/ad/poem-os/poem/data/youtube-launch-optimizer/config/brand-config.json`. |
| brand-config consumers | FliHub: `server/src/routes/poem-wui.ts`, `server/src/utils/poemWuiUtils.ts`, tests `brandConfigRoute.test.ts`, `configManager.test.ts`, `poemWuiSend.test.ts`. YLO/Tuber reads affiliates/CTAs from it (see `/Users/davidcruwys/dev/ad/brains/ylo/estate-register-2026-10-05.md` §93, §204). | Find every consumer (`command grep -rn "brand-config" ~/dev/ad --exclude-dir=node_modules`) before moving it. |
| FliStudio Launch playlists step | `/Users/davidcruwys/dev/ad/flivideo/flistudio` client `uploadSteps.ts`/`UploadWizard.tsx`/`LaunchPieces.tsx`; settings come from the `studio-settings` resource / "brand defaults" | Shows "none picked"; nothing behind it. |
| Published-video link | FliStudio `publish.mark-published` stores `meta.youtubeId` on the final video resource; `publish.published` lists them per brand | The join point between a FliStudio project and a mirrored YouTube video. |

## Your job

### Part A: architecture (decide, write down, then build)

Write `/Users/davidcruwys/dev/ad/flivideo/docs/youtube-channel-architecture.md` answering, with a recommendation and its reason for each:

1. **Placement.** Where does YouTube sync live? Options: fold yt-mirror into the Fli suite as a library (`@flivideo/core` or a new `@flivideo/youtube` package), a FliTools service, a FliStudio capability set, or yt-mirror kept standalone and called by FliStudio. Weigh it against the suite's rules: **agents go through FliStudio's front door only** (capabilities over HTTP JSON-RPC, see `flistudio/docs/AGENT-NOTES.md`); FliTools owns transcription; fli-core holds shared contracts. Look at how fli-core exposes `brands.json` today.
2. **Brand publishing settings' new home.** Move FliHub's brand-config out of FliHub to a managed, git-tracked, per-brand home that the brand registry points to (e.g. `fli.brand.json` already exists at each `v-<brand>/` root; or brands.json; or a new file). Decide which fields are **mirrored from YouTube** (playlist list, channel facts) and which are **brand-authored** (CTAs, affiliates, which playlists are "active", description template, legal). Migrate verbatim and keep provenance (`_meta.source`). Repoint every consumer (FliHub, POEM copy, YLO/Tuber) or leave a pointer. **Don't delete the old files until every consumer is repointed and David has been told.**
3. **Keys and auth per brand.** Read (public data) works with an API key; private/unlisted videos and every write need **OAuth by the channel owner**. Design where per-brand credentials live (**never in git**: David's rule; secrets live in `~/.secrets` / NordPass; check `~/dev/ad/brains/davidcruwys/password-management.md` ONLY if David permits). Plan OAuth for the later write phase; don't implement it now.
4. **Data shape** of the mirror: channel, playlists (id, title, itemCount, privacy, updatedAt), playlist→video membership, and video (id, title, publishedAt, duration, privacy, thumbnails, the transcript you can get). Incremental sync (etags or updatedAt) and quota cost per sync. Use the official YouTube Data API v3 docs as the source and cite them in the doc; don't recall them.
5. **Freshness:** "sync now" button + an optional schedule; how staleness shows.
6. **Joins:** mirrored video ↔ FliStudio project (via `publish.published` youtubeId); playlist membership shown on both sides.

### Part B: build the read side, end to end

1. Sync with playlists + membership for **aitldr, appydave and appydavelabs** (handle claudinglab), refreshing the 5-month-old mirror. Do this only after Part A has settled where the code lives.
2. FliStudio capabilities (front door), e.g. `youtube.channel`, `youtube.playlists`, `youtube.videos`, `youtube.sync`, wherever Part A puts them, each read-only except sync.
3. A brand **YouTube** page in FliStudio: channel, playlists (with an "active for this brand" toggle stored in the brand's authored settings), videos linked to projects, "last synced · sync now".
4. Launch **Playlists** step: tick boxes from the brand's real playlists, brand's usual picks pre-filled, an agent proposal shown as a suggestion, human approve. Keep FliStudio's CLAUDE.md hard rules (copy + Finder icons; copy-path; light-only; never hand David a text file).
5. Tests per layer, plus a live run on all three channels. Report counts (playlists, videos, membership) per channel.

## Stop boundary

**STOP after Part A's architecture doc is written. Report its recommendations in a decision card** (≈10 lines: what it decides, options table, "My take: X, because…", one place to act; rule: `/Users/davidcruwys/dev/agents/factory-kit/talking-to-david.md`) to `flivideo-orch` via SendMessage, and to David in your window. Then **continue to Part B only on David's go.** After Part B, stop again and report. Never start the write phase (OAuth, playlist writes, Studio fill).

## Constraints

- No Ruby. TypeScript, Bun or Node, matching the target package.
- Never commit API keys or OAuth tokens. `.env` files stay git-ignored. Confirm before using any key.
- Respect YouTube API quota (10k units/day default): measure the cost of a full sync and report it.
- Don't restart running Fli apps (FliStudio hot-reloads; if the server gets stuck, tell `flivideo-orch`, don't kill processes).
- Commit and push finished work in each repo you touch (stage by name; pull --rebase first). Other workers may be in FliStudio at the same time.
- FliStudio's "agents never read or write project folders" rule applies to agents. Your sync code is FliStudio/library code, not an agent, so it's exempt.
- Report to `flivideo-orch` (SendMessage) at each stop.
