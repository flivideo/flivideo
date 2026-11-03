---
created: 2026-11-03
---
# AITLDR Series B — status, Published, and YouTube URLs (2026-11-03)

Worker: `aitldr-published-rsch`. Brief: `docs/briefs/aitldr-series-b-published-2026-11-03.md`.

## Result
**Published chip: 0 → 25** (b01–b25). Screenshots: `docs/reports/proof-2026-11-03/series-b-published-1-before.png` (0), `-2-pilot-b01.png` (1), `-3-after.png` (25).

## 1. Heat map + status
- Status word, stage and squares: `flistudio/server/src/capabilities/project-status.ts` — step list `:~100-215` (Idea → Script → Recorded → Editing → Exported → Final → Launch → Published); `compute()` `:~480`; `finish()` `:665-697` sets the category (published > stalled > working).
- Recomputed on every read (page load / `projects.list`), cached per project against a cheap disk fingerprint (dir mtimes, file count, status file, brand files): `statusOf` `:453-473`. No cron. The page also updates live through the estate watcher (`client/src/live.ts`).
- Chips and counts: `client/src/screens/statusModel.ts` (`CATEGORIES`, `countsOf`).
- **LAST WORK = newest mtime of any file in the project** (bookkeeping excluded), `project-status.ts:640`. 27 Oct is real, not stale: the newest files in b01/b05 are the `*-final.srt` files, all rewritten 2026-10-27 09:20 (a bulk captions write; `v-aitldr-premerge-2026-10-27/` is the same day). So the date means "the bulk caption write", not per-video work.
- Side effect of my write: `fli.resources.json` is not excluded as bookkeeping, so marking a project Published bumps its LAST WORK to today and shows the ★ (worked today).

## 2. What makes a project Published
- A `video` resource in the project's `fli.resources.json` with `status: "published"` and `meta.youtubeId` (+ `meta.url`, `meta.publishedAt`). Read by `publishedVideos()` (`fli-core/src/publish.ts:713`) → `publishedRow` (`:635`) → Published step `project-status.ts:204-213`.
- Normally set by the human-only flow: `publish.promote --kind video` (a person's gate; `contracts.ts:4663-4672`) then `publish.mark-published --youtube-id` (`flistudio/server/src/capabilities/publish.ts:788`; needs a chosen final, `fli-core publish.ts:822`). A YouTube id or link flips it. Nothing else does (no scan of the channel).
- None of the Series B projects had any `video` resource, so the verbs could not run for an agent (promote of a video is human-only). I hand-wrote the one resource (shape copied from an existing published resource in v-appydave `d02`), stamped `by: agent:aitldr-published-rsch`, `publishedAt` = the real YouTube publish time from the mirror. b01 was done first and confirmed in the UI before the rest.
- Not set: "Final cut" and Launch prep squares. Published shows green, Final stays "skipped" (the hand-written resource is published, not chosen).
- **Non-YouTube (Skool b28–b30):** `parseYoutubeId` accepts only YouTube ids/links and `publishedVideos` requires `meta.youtubeId`, so a Skool URL cannot drive Published today; it needs a code change (a non-YouTube published resource, or a `meta.url`-only path). Stopgap that needs no code: `project.status.set --step publish --setting done` (a manual override, no URL kept). Not done: no URL known, and David hasn't said Skool-only counts as Published.

## 3. Series B URLs
- Prior catalogue: `v-aitldr/catalog/catalog.json` is a 2026-05-30 snapshot (337 videos) — **no Series B**. The FliStudio mirror `~/dev/video-projects/published/aitldr/` (last `youtube.sync` 2026-10-29, 426 videos, all public) **does** cover it; I read that, no new sync and no credentials.
- Matching evidence: local `videos/<v>/<v>-final.mp4` length vs channel length (channel is consistently +5 s for longs, +0–1 s for shorts), upload.md description vs channel description, and upload order. Titles were rewritten at upload, so title alone rarely matched.

| Project | Video | YouTube id | Status |
|---|---|---|---|
| b01 | yt-performance | a2EGJnOCpoA | matched (exact title; length 216 vs 251 s, differs — see notes) — written |
| b01 | short | Jr1lwtcNBFU | matched — written |
| b02 | script | j1Hpvsu79Xg | matched — written |
| b02 | short | iKGBS_7OtJw | matched — written |
| b03 | thumbnail-prompt | 0B8UzTL-h6E | matched — written |
| b03 | short | IYlHBYI8Fxs | matched — written |
| b04 | shot-list | 8uypPWDhDs8 (long on channel) | **no local long video** — not written |
| b04 | short | I2xF9A0Rg6s | matched — written |
| b05 | title-lab | D3srragTwPQ | matched — written |
| b05 | short | 5r8dGfwSbjI (candidate) | **ambiguous**: topic fits, length 33.1 vs 38 s (+5, others +1) — not written |
| b06 | hook-doctor / short | Nrd5PnLkMk4 / 1BVB9cnxL10 | matched — written |
| b07 | idea-bank / short | idUuJkfh61k / Mw6HU-0b7lE | matched — written |
| b08 | cue-cards / short | TdBL1A7kMd4 / g00d9RY7GXo | matched — written |
| b09 | vo-prep / short | OQTr8bB7GdE / wmnMpetixCM | matched — written |
| b10 | demo-sandbox / short | 6KEJxgUO0G0 / 0ixwtrYd6mI | matched — written |
| b11 | broll-prompts | c_9TqD0GlXk | matched — written; short unmatched |
| b12 | gap-check | moRWKeCxOAI | matched — written; short unmatched |
| b13 | cta-lines | jWfwJqH3gY4 | matched — written; short unmatched |
| b14 | timing-sheet | 8KhyDQLB0Po | matched — written; short unmatched |
| b15 | upload-pack | kHmv8l_VkGM | matched — written; short unmatched |
| b16 | cut-list | w4LpBamBkCs | matched — written (no short) |
| b17 | captions | yh-ko-CwXyg | matched — written; short unmatched |
| b18 | overlay-pack | Ew8a157XEYg | matched (title near-exact) — written; short unmatched |
| b19 | sfx-cues | Gtn1ThkuylU | matched — written; short unmatched |
| b20 | quick-short | VtFZNkGYnaU | matched — written; short unmatched |
| b21 | angle-lab | 5VB3b4f__uE | matched (description 0.69 + length + order; title differs) — written; short unmatched |
| b22 | avatar-blocks | oddec0MA4p8 | matched — written; short unmatched |
| b23 | rights-check / short | XJXg98uMAVY / pwi9Oqlkfps | matched — written |
| b24 | end-screen | 9m8ztxRKLRo | matched — written; **short unmatched** (no channel Short of ~27 s after 27 Oct) |
| b25 | community-post | jWuBSWSCp1M | matched — written; **short unmatched** |
| b26 | repurpose (+short) | — | **unmatched**: not on the channel as of the 29 Oct sync. Jan's dirty file left alone |
| b27 | postmortem | — | untracked, Jan's; no videos yet. Untouched |
| b28 | skool-intro | — | unmatched: Skool storefront; not on YouTube mirror. See §2 |
| b29 | skool-inside | — | same |
| b30 | skool-start-here | — | same |

Channel uploads in the window with no Series B home: `GaExvmBUa0I` (30 s Short, 23 Oct, "fix your messy script in 30 seconds") — could be b02/b21 reuse, ambiguous; `Pi2Ggb2hWM4` (20 s), `aZjw4FzKZrM` (68 s Vox), `6zAtQHHg6Io` (11 s) — not Series B.

## Notes / open
- Only the long (or the only) video per project is what flips the chip; the project shows Published even where just one of two videos is published (b04: the long exists on YouTube but has no local file).
- b01 long: channel 251 s vs local final 216 s — the title matches exactly, so written, but the shipped cut may differ from the local final.
- The mirror is as of 29 Oct; anything published after that is unseen. A fresh `youtube.sync` (public only) would settle b26 and the b24/b25 Shorts.
- All 34 resources are agent-stamped (`agent:aitldr-published-rsch`); David can `publish.relink`/clear any he disagrees with.


## Verification pass (after c4ea5e1 was pushed) — requested by flivideo-orch
All 34 ids rechecked against the channel mirror's title and duration for that id. Rule used for "clear": duration fits the pattern (mains +4.5…+5.5 s, Shorts +0…+1.1 s) AND the YouTube title/description matches that project's own content (local title candidates and upload.md for mains; the Short's own transcript for Shorts, since Shorts have no local title). Every row also ranks first against all other same-format uploads by transcript similarity, except where noted.
- **Reverted: b01 main only** — title exact, but 251 s vs the local final's 216 s (35 s, not the +5 s pattern); the shipped cut is not the local final. The id is probably right, but unproven. Reverted in new commit `17fd8ad` (no amend, no force-push). b01 stays Published through its Short.
- Looked weak but kept after reading the content: b02 Short (YouTube description empty; transcript is "blank page… script" = title), b01 Short, b17 (transcript = the captions/channel-name story = title; **note: YouTube's description on `yh-ko-CwXyg` is the Cut List text pasted from b16 — a YouTube-side error to tell Jan**).
- Thinnest margins, kept: b13 (title ↔ CTA, +4.8 s), b15, b16 (YouTube description names "Cut List").
- **Was a wrong id pushed in c4ea5e1?** No wrong id that I can find: 33 of 34 pass title/content and duration. One (b01 main, `a2EGJnOCpoA`) was unproven rather than shown wrong; it was in the pushed commit for a few minutes and is now removed. Strictly: c4ea5e1 contained 1 unproven id, 0 known-wrong.
- Chip: before 0 (`series-b-published-1-before.png`) → 25 after c4ea5e1 (`-3-after.png`) → **25 after the revert** (`series-b-published-4-after-verify.png`).

| bNN | video | YouTube id | YouTube title | YT dur vs local final | verdict |
|---|---|---|---|---|---|
| b01 | main (yt-performance) | [a2EGJnOCpoA](https://youtu.be/a2EGJnOCpoA) | Want to Know Which Videos Are Killing Your Channel? Watch This Now! | 251s vs 216.1s (+34.9) | **reverted** (title exact, but 251 vs 216 s: not a clear match; 17fd8ad) |
| b01 | short (yt-performance-short) | [Jr1lwtcNBFU](https://youtu.be/Jr1lwtcNBFU) | Low Views? This Claude Skill Helps You Find Out Why | 34s vs 33.0s (+1.0) | clear |
| b02 | main (script) | [j1Hpvsu79Xg](https://youtu.be/j1Hpvsu79Xg) | This Claude AI Skill Writes Your YouTube Scripts for You | 268s vs 263.0s (+5.0) | clear |
| b02 | short (script-short) | [iKGBS_7OtJw](https://youtu.be/iKGBS_7OtJw) | Struggling to Write YouTube Scripts? Use This AI Skill Now! | 32s vs 31.7s (+0.3) | clear |
| b03 | main (thumbnail-prompt) | [0B8UzTL-h6E](https://youtu.be/0B8UzTL-h6E) | How to Make Thumbnails That Get Views Using AI (Full Tutorial) | 262s vs 256.7s (+5.3) | clear |
| b03 | short (thumbnail-prompt-short) | [IYlHBYI8Fxs](https://youtu.be/IYlHBYI8Fxs) | This AI Skill Creates Clickable Thumbnails | 38s vs 37.4s (+0.6) | clear |
| b04 | short (shot-list-short) | [I2xF9A0Rg6s](https://youtu.be/I2xF9A0Rg6s) | Turn Any Script Into a Shot List With Claude | 35s vs 34.2s (+0.8) | clear |
| b05 | main (title-lab) | [D3srragTwPQ](https://youtu.be/D3srragTwPQ) | I Stopped Guessing YouTube Titles—This Claude Skill Scores Them for Me | 127s vs 122.3s (+4.7) | clear |
| b06 | main (hook-doctor) | [Nrd5PnLkMk4](https://youtu.be/Nrd5PnLkMk4) | This Claude Skill Found What Was Wrong With My YouTube Hooks | 205s vs 199.7s (+5.3) | clear |
| b06 | short (hook-doctor-short) | [1BVB9cnxL10](https://youtu.be/1BVB9cnxL10) | This Claude Skill Caught My Weak Hooks | 32s vs 31.8s (+0.2) | clear |
| b07 | main (idea-bank) | [idUuJkfh61k](https://youtu.be/idUuJkfh61k) | Running Out of Video Ideas? Try This Claude Skill | 175s vs 170.3s (+4.7) | clear |
| b07 | short (idea-bank-short) | [Mw6HU-0b7lE](https://youtu.be/Mw6HU-0b7lE) | How I never run out of video ideas | 27s vs 26.2s (+0.8) | clear |
| b08 | main (cue-cards) | [TdBL1A7kMd4](https://youtu.be/TdBL1A7kMd4) | How to sound natural on camera | Claude Cue Cards | 165s vs 160.2s (+4.8) | clear |
| b08 | short (cue-cards-short) | [g00d9RY7GXo](https://youtu.be/g00d9RY7GXo) | Stop Sounding Like You’re Reading Your Script | Claude Cue Cards | 32s vs 31.2s (+0.8) | clear |
| b09 | main (vo-prep) | [OQTr8bB7GdE](https://youtu.be/OQTr8bB7GdE) | I Stopped Trusting My AI Voiceover Until Claude Checked Every Line | 179s vs 174.1s (+4.9) | clear |
| b09 | short (vo-prep-short) | [wmnMpetixCM](https://youtu.be/wmnMpetixCM) | My AI Voice Added a Sentence I Never Wrote — Claude Caught It | 34s vs 33.0s (+1.0) | clear |
| b10 | main (demo-sandbox) | [6KEJxgUO0G0](https://youtu.be/6KEJxgUO0G0) | Protect Your Privacy: The Claude Code Demo Sandbox | 132s vs 126.6s (+5.4) | clear |
| b10 | short (demo-sandbox-short) | [0ixwtrYd6mI](https://youtu.be/0ixwtrYd6mI) | I Accidentally Showed Private Data on YouTube—Here’s the Claude Skill I Use Now | 29s vs 28.9s (+0.1) | clear |
| b11 | main (broll-prompts) | [c_9TqD0GlXk](https://youtu.be/c_9TqD0GlXk) | I Had No B-Roll. This Claude Skill Wrote the Prompts | 134s vs 129.1s (+4.9) | clear |
| b12 | main (gap-check) | [moRWKeCxOAI](https://youtu.be/moRWKeCxOAI) | I Thought I'd Recorded Everything. Claude Checked My Footage and Found 9 Missing Shots | 143s vs 138.4s (+4.6) | clear |
| b13 | main (cta-lines) | [jWfwJqH3gY4](https://youtu.be/jWfwJqH3gY4) | Stop Reusing the Same YouTube CTA — Use This Claude Skill | 152s vs 147.2s (+4.8) | clear |
| b14 | main (timing-sheet) | [8KhyDQLB0Po](https://youtu.be/8KhyDQLB0Po) | This Claude Skill Fixed My Animation Timing | 165s vs 159.5s (+5.5) | clear |
| b15 | main (upload-pack) | [kHmv8l_VkGM](https://youtu.be/kHmv8l_VkGM) | This Claude Skill Writes My YouTube Descriptions for Me | 165s vs 159.8s (+5.2) | clear |
| b16 | main (cut-list) | [w4LpBamBkCs](https://youtu.be/w4LpBamBkCs) | This Claude Skill Finds Dead Time in Your Videos Automatically | 169s vs 163.7s (+5.3) | clear |
| b17 | main (captions) | [yh-ko-CwXyg](https://youtu.be/yh-ko-CwXyg) | I Let Claude Fix My YouTube Captions — Here's What Happened | 163s vs 158.0s (+5.0) | clear |
| b18 | main (overlay-pack) | [Ew8a157XEYg](https://youtu.be/Ew8a157XEYg) | This Claude Skill Turns Your Script Into Ready-to-Use Video Overlays | 157s vs 151.7s (+5.3) | clear |
| b19 | main (sfx-cues) | [Gtn1ThkuylU](https://youtu.be/Gtn1ThkuylU) | Stop Adding Sound Effects Manually! Let Claude Do It | 148s vs 142.8s (+5.2) | clear |
| b20 | main (quick-short) | [VtFZNkGYnaU](https://youtu.be/VtFZNkGYnaU) | Turn Long Videos Into YouTube Shorts Automatically With Claude! | 174s vs 169.0s (+5.0) | clear |
| b21 | main (angle-lab) | [5VB3b4f__uE](https://youtu.be/5VB3b4f__uE) | How I Use Claude Code to Simplify My Video Scripts | 163s vs 157.5s (+5.5) | clear |
| b22 | main (avatar-blocks) | [oddec0MA4p8](https://youtu.be/oddec0MA4p8) | This Claude Skill Can Save You Money on AI Avatar Videos | 142s vs 137.3s (+4.7) | clear |
| b23 | main (rights-check) | [XJXg98uMAVY](https://youtu.be/XJXg98uMAVY) | Avoid YouTube Copyright Claims With This Claude Skill! | 178s vs 173.0s (+5.0) | clear |
| b23 | short (rights-check-short) | [pwi9Oqlkfps](https://youtu.be/pwi9Oqlkfps) | How to Check Your Videos for Copyright Issues Using Claude | 30s vs 29.2s (+0.8) | clear |
| b24 | main (end-screen) | [9m8ztxRKLRo](https://youtu.be/9m8ztxRKLRo) | Stop Losing Views! Fix Your YouTube End Screens With Claude | 151s vs 145.5s (+5.5) | clear |
| b25 | main (community-post) | [jWuBSWSCp1M](https://youtu.be/jWuBSWSCp1M) | How I Automate YouTube Community Posts With Claude Code | 157s vs 152.1s (+4.9) | clear |


## Pass 2 — fresh public `youtube.sync`, then re-match (worker `aitldr-sync-rsch`, 2026-11-03)
**Sync:** `flistudio youtube.sync --brand aitldr` (public, read-only, 30 quota units): **426 → 429 videos**; newest publish **2026-10-31 00:37Z** (`iWGZOYoGU-w`, Vox-style Short, not Series B). The mirror had not been synced since before 29 Oct, so everything from 29 Oct on was new. Three new uploads: `iWGZOYoGU-w` (60 s), `fm1WrkZ9Bvk` (11 s), `P4c-XkAeJxI` (3:27).

| bNN | video | id | YouTube title | YT vs local final | verdict |
|---|---|---|---|---|---|
| b26 | main (repurpose) | [P4c-XkAeJxI](https://youtu.be/P4c-XkAeJxI) | How to Repurpose YouTube Videos With Claude Code | 207 s vs 201.5 s (+5.5) | **clear, NOT written** (Jan's uncommitted edit is still in `b26-repurpose/fli.resources.json`; brief says report instead). Title = project topic, duration fits, only long upload after b25. Caveat: YouTube's description is the Title Lab text pasted in (YouTube-side error, like b17), and the mirror has no transcript for it |
| b26 | short (repurpose-short, 27.7 s) | — | — | — | unmatched: no Short ≈ 28 s exists after 27 Oct (new Shorts are 11 s, 11 s, 60 s Vox) |
| b21 | short (angle-lab-short) | [GaExvmBUa0I](https://youtu.be/GaExvmBUa0I) | How to fix your messy script in 30 seconds | 30 s vs 29.6 s (+0.4) | **clear, written** (`1ad9515` in v-aitldr). Description names the Angle Lab skill and "keeps one promise"; local SRT opens with the same line |
| b05 | short (title-lab-short) | [5r8dGfwSbjI](https://youtu.be/5r8dGfwSbjI) | Find Your Best YouTube Title Before You Publish | 38 s vs 33.1 s (+4.9) | **still ambiguous, not written**: topic fits, but +4.9 s is the main-video pattern, not the Short's +0…1.1 |
| b24, b25 | shorts | — | — | — | unmatched: no ~27 s / ~29 s Short in the mirror after 27 Oct |
| b11–b15, b17–b20, b22 | shorts | — | — | — | unmatched: no unclaimed Short in the window; the only unclaimed ones are `Pi2Ggb2hWM4` (20 s, "Claude edited this whole video"), `6zAtQHHg6Io` (11 s), `fm1WrkZ9Bvk` (11 s), none matching these lengths or topics |
| b01 | main | a2EGJnOCpoA | — | 251 s vs 216 s | stays reverted: no new evidence |

**Chips (AITLDR landing, after):** Needs attention 0 · Working 4 · Not started 1 · **Published 25** · Parked 0 · Abandoned 0. Unchanged because b21 was already Published through its main. Screenshot: `docs/reports/proof-2026-11-03/series-b-published-5-pass2.png`.
