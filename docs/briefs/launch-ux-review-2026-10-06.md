# Launch wizard — UX review, 2026-10-06

**Purpose**: A ranked UX review of FliStudio's Launch wizard (D03 unfinished, D02 published), with concrete fixes and a ruling on the Description "…more fold" redesign.

**For Agents**:
- Read this before any Launch / upload-wizard UI pass.
- Findings are ranked; the "Top 5" section is the build order.
- Screenshots: `/Users/davidcruwys/dev/ad/brains/.playwright-mcp/uxr-*.png`.
- David's own list it builds on: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/ui-notes-2026-10-06.md` (items 1–38).

## Verdict (5 lines)

1. **Better than the board, but the wizard wasn't actually built as a wizard.** The mock gave each step one value and one copy button. The build put the whole deciding board (approval cards, banners, pools, shortlist, Tuber's reasoning) back inside every step.
2. That's why it feels heavy. Title & thumbnails is 3,089 px tall on D03 and 3,551 px on D02, and Next is at the very bottom.
3. The wizard starts ~335 px down the page, under project chrome. Two nav columns (project sidebar and step rail) squeeze the step card to about 880 px.
4. The Description fold uses four devices and three numbers that contradict each other (69 / 100 / 157). On D03, where nothing is wrong, it still highlights a sentence as if it were.
5. Fix order: split Decide from Upload → give the wizard the screen → previews instead of the fold cluster → one status language in the rail → brand defaults shown as values, not decisions.

**Method**: `appydave:ux-review` lenses (frontend-design, arrange, typeset, colorize, clarify, critique, distill, harden), applied by one reviewer against the live app in Playwright at 1512×945. The 14-agent fan-out wasn't run, and there's no `.impeccable.md`, so the design context was the AppyDave brand plus David's notes. I clicked only rail steps; no data was changed. I saw no hot-reload during the review: the Subtitles merge into step 1 was already live when I started.

---

## Blockers (stop the fast "next, next, next" job)

### B1. Decide and Upload are welded together. The Title step is a 3,000+ px scroll
- **Step**: 2 · Title & thumbnails (both videos)
- **Screens**: `uxr-d03-02-title-thumbs.png`, `uxr-d02-02-title-thumbs.png`
- **What's wrong**: The upload kit for the 3 pairs (good) is followed by the packaging approval, a 26-row title pool with "why" toggles, a 4–6 thumbnail pool, a "Pick a title and a thumbnail" bar, and then **the same 3 pairs again** as a shortlist with Mark winner / Remove pair. You see each thumbnail three times. Next is ~3,000 px down. That's item 24 ("too much, too far away") all over again, inside one step.
- **Fix**: The Upload step shows only what the mock showed: pairs 1–3, each with its thumbnail, a **Copy title** button and **Copy path / Finder**, then Next. Move the pools, shortlist, re-pairing and Mark winner to a separate **Decide** view, reached by a small "Change pairs →" link on the step. Mark winner belongs on the published video's after-live step, not in the upload flow.

### B2. The wizard doesn't own the screen
- **Step**: all
- **Screens**: `uxr-d03-01-landing.png`, `uxr-d03-01-video-subtitles.png`
- **What's wrong**: Above every step sit the project title, path row, "PROJECT trash · renders · apps · resources" strip, a "LAUNCH" heading, the "PUBLISHING" chip and a progress bar, so the step header starts at y≈335. Left to right there are three columns: project sidebar (280 px), step rail (250 px), then the card. Item 34 again.
- **Fix**: When `zone=launch`, collapse the project sidebar to a 56 px icon strip, hide the Project strip and the "Launch" h3, and put the video chip in the step header line: `STEP 3 OF 11 · DETAILS · cutty-presenter-tracking 2:54`. The step card should start under the app bar.

---

## Major

### M1. The Description "…more fold" is four warnings that disagree
- **Step**: 3 · Description
- **Screens**: `uxr-d02-03-description.png`, `uxr-d02-03b-fold-zoom.png`, `uxr-d03-03-description-full.png`
- **What's wrong**:
  - It says the same thing four ways: an amber warning box, a monospace counter ("132 characters before the link · aim for under ~69"), two lines of brown small print ("about 100 … 157 or more … Approximate: YouTube folds by lines…"), and a highlighted band inside the text.
  - **Three numbers, no shared meaning.** 69, 100 and 157 appear together, and nothing says which one counts.
  - **On D03 nothing is wrong** (the link is at character 67), yet the band still highlights "Cutty, my AI video editing agent, tracks the presenter frame". That reads as an error marker.
  - **On D02, already live and approved**, it still shouts "move it up", and he can't act on that.
  - The small print admits the count is the wrong measure ("YouTube folds by lines").
- **Fix**: see the full ruling under "The Description fold" below.

### M2. Approval chrome sits on top of the value he came to copy
- **Steps**: 3 · Description, plus Chapters on the same step
- **Screen**: `uxr-d03-03-description-full.png`
- **What's wrong**: Before the Copy button there are:
  - a DRAFT pill;
  - a full-width yellow banner in internal language: "tuber is waiting for your decision here: D03 description body ready; chapters wait for the edited cut";
  - a provenance line: "Proposed by tuber; waiting for you. Source: proposal by agent:tuber." This says "Tuber proposed it" three times;
  - Edit and Approve.

  "Copy description" is the smallest button in the card. Under it, Chapters carries the same banner, provenance line and Approve a second time.
- **Fix**: One line, right-aligned in the card header: `Tuber's draft · [Approve] [Edit]`. Approve stays yellow, because it's the decision. **Copy description** becomes the big button in the top-right of the value box. Delete the provenance line. Banner wording, if one is kept at all: "Read it, then Approve or Edit" (item 16). Chapters on this step collapses to one line: `Chapters (6) — inside the description · fit the 2:55 cut · [Approve] [show]`.

### M3. The rail speaks two status languages and gets some of them wrong
- **Step**: rail (all)
- **Screens**: `uxr-d03-11-pinned-comment.png`, `uxr-d02-01-video.png`
- **What's wrong**:
  - Some rows show a step number (1, 9, 10) and the rest show a status icon (✓ ● –). So the header's "Step 3 of 11" can't be matched to anything in the rail.
  - There are two counters ("1/7 decided · 6 to go" vs "Step 3 of 11"), and you need a legend at the bottom ("✓ decided · ● waiting for you · – not ready") to read them.
  - **Pinned comment shows ● "waiting for you" while its card says MISSING.** Tags and End screen show "–" for the same state.
  - On published D02, Visibility still shows "9", unticked.
- **Fix**: Always show the step number in the circle. Show status as a small trailing dot after the label: green = done, amber = needs you, grey = nothing yet. Use one counter in the rail header, "6 decisions left", and delete the legend. Missing drafts get the grey dot. Visibility ticks when the YouTube link is saved.

### M4. Brand defaults are dressed as per-video decisions
- **Steps**: 4 Playlists, 5 Audience, 7 Language & category
- **Screens**: `uxr-d03-04-playlists.png`, `uxr-d03-05-audience.png`, `uxr-d03-07-language.png`
- **What's wrong**:
  - Every one has a dashed card saying "BRAND DEFAULTS · PLAYLISTS [BRAND DEFAULTS]" (said twice), "never counted as your decision until you approve them. Source: brand defaults", and an **Approve** button.
  - Playlists asks him to approve "none picked".
  - Audience offers **Copy audience** for a radio button, and the note right under it says "Nothing to paste: it's one click in YouTube".
  - Category shows the raw ID: **"26 Howto & Style"**. The mock stripped the ID; the build brought it back.
- **Fix**: Defaults are approved once per brand, not per video. The step shows the value big and plain ("**Not made for kids**", "**Howto & Style · English**") with no Approve and no Copy, plus a small "change for this video" link. Strip the leading number from the category. If the playlist is empty, auto-skip the step in Next order and show it greyed in the rail.

### M5. Step 1 asks him to choose between files he can't tell apart
- **Step**: 1 · Video + subtitles
- **Screen**: `uxr-d03-01-video-subtitles.png`
- **What's wrong**: "picked by rule (newest FliCut export) **2 candidates — check**" sits over a radio list: `…-audio-a100.mp4 … 2:54 RULE rule's pick` and `…-audio-a12.mp4 … 2:54 found by name`. The lengths are the same and the labels are internal (a100, a12, RULE, "found by name"). "check" sounds like a problem.
- **Fix**: Show the one picked file. Put a quiet link under it: "Not this one? 2 exports →", which opens the list with plain labels (exported time, length, "audio a100 = the one you approved" or similar). Never use the word "check" unless something's actually wrong. Also cut the second **Copy SRT path** button under the SRT card: the card already has one (keep the `S` shortcut hint).

### M6. A published video has no "Live" state
- **Steps**: whole page, 10 · YouTube link
- **Screens**: `uxr-d02-01-video.png`, `uxr-d02-10-youtube-link.png`
- **What's wrong**: D02 is live, but Launch opens at step 1, "Video + subtitles", as if he still had to upload. The only sign that it's published is on step 10: "✓ Published: https://youtu.be/…". The one job left after going live (pinned comment) is the last step.
- **Fix**: On a published video, show a green strip under the step header: `● Live · youtu.be/yFOhSJqU5rk · [Copy link] [Open ↗]`. Land on the first unfinished after-live step (Pinned comment), or show a summary.

### M7. Changing step doesn't bring you to the top of the step
- **Step**: rail navigation
- **Screen**: `uxr-d02-10-youtube-link.png` (header scrolled off after coming from a long step)
- **What's wrong**: After a long step (Title 3,000 px, Description 2,000 px), clicking the next rail item keeps the old scroll position, so the step title and its "where in YouTube" line are off-screen. Seen once, after I had scrolled manually. The cause isn't isolated.
- **Fix**: On step change, `scrollIntoView({block:'start'})` the step header. This matters less once B1 and B2 land.

---

## Minor

- **Empty states don't match** (Tags/End screen "NOT READY … waits for Tuber's draft" vs Pinned "MISSING … Write it"), and none offers **Ask Tuber**. Use one card everywhere: "Tuber hasn't drafted this yet." `[Write it] [Ask Tuber]`. Screens: `uxr-d03-06-tags.png`, `uxr-d03-08-end-screen.png`, `uxr-d03-11-pinned-comment.png`.
- **"PLUS / Subscribe element"** on End screen is a stray label/value pair. Fold it into the instruction line: "…End screen → add Subscribe + the videos below". `uxr-d03-08-end-screen.png`.
- **An unlabelled ↗ icon** sits next to FINDER / COPY PATH on every file. Label it **Open** (item 28's rule: every icon gets a word). `uxr-d03-01-video-subtitles.png`.
- **Pair thumbnails are small** (~160 px wide) at the top of step 2 but big (~230 px) in the shortlist below. David judges visually, so make the upload-kit thumbnails the big ones (~320 px) once B1 removes the shortlist.
- **Title step instruction is a paragraph** ("Details → Title takes pair 1's title (and pair 1's image is the main thumbnail). Then Details → Thumbnail → Test & Compare: add pairs 2+ as title-and-thumbnail pairs."). Replace it with: "Paste title 1 into **Title**. Then **Thumbnail → Test & Compare**: add all 3 pairs."
- **Visibility and YouTube link are two steps for one screen in YouTube.** Merge them: "Pick Public / Unlisted / Schedule in YouTube, then paste the link it shows you here → [Mark published]."
- **Mark published works at 1/7 decided** with no hint (`uxr-d03-10-youtube-link.png`). Keep it allowed, but add one plain line: "6 things aren't decided yet."
- **"Last step" is a disabled yellow button** (`uxr-d03-11-pinned-comment.png`). The yellow reads as a call to action. Replace it with "Done → project" or hide it.
- **Banner text says "tuber"** in lower case. Use "Tuber".
- **Possible order issue (unverified)**: YouTube Studio may ask for the video language before it accepts a subtitle upload. If so, the "Language & category" value needs to be visible on step 1, or the language set first. Check this in Studio before changing anything.

---

## The Description fold: ruling on the candidate fix

**Your candidate** (two small "what viewers see" previews, phone ≈100 / desktop ≈157 characters ending "… more", plus one plain line only when the first link is hidden) **is right**. Ship it with these four upgrades:

1. **Clip by lines, not characters.** Render each preview as a box at the real-ish width with `-webkit-line-clamp` (phone box ~340 px, 2 lines; desktop box ~620 px, 3 lines; Roboto 14 px), with a bold **…more** pinned to the end of the last line. That's how YouTube folds, so the "approximate, it's by lines" disclaimer can go. The exact widths and line counts YouTube uses weren't checked here: label the boxes "Phone (roughly)" and "Desktop (roughly)" and tune them once against a real screenshot.
2. **Show links blue inside the preview.** Then he can *see* whether the Skool link made it above the fold. That's the visual check he wants, and it needs no number.
3. **One plain line only when the first link is clipped on the phone preview**, written as an action: "Your Skool link is hidden on phones. Move 'Join my Skool community' into the first sentence. [Edit]". Show nothing when it's fine. Show nothing (or a muted grey version) once the description is approved or the video is live.
4. **Collapse the full 2,000+ character body** under the previews to ~6 lines with "Show all (2,255 characters)". In Upload mode the job is Copy, not reading. Reading belongs in Decide.

**Delete outright**: the amber warning box, the monospace counter, "aim for under ~69", the two lines of brown small print, and the highlighted band inside the text.

Layout:

```
DESCRIPTION                         Tuber's draft · [Approve] [Edit]
┌ Phone (roughly) ───────┐ ┌ Desktop (roughly) ─────────────────┐
│ Fans and an air condi… │ │ Fans and an air conditioner running│
│ tioner running, and my │ │ and my audio still comes out clean.│
│ audio still… more      │ │ Here's the AI agent… more          │
└────────────────────────┘ └────────────────────────────────────┘
Your Skool link is hidden on phones. Move it into the first sentence. [Edit]
┌──────────────────────────────────────────────── [COPY DESCRIPTION] ┐
│ (first 6 lines)…                      Show all (2,255 characters) ▾ │
└─────────────────────────────────────────────────────────────────────┘
Chapters (7) inside the description · fit the 5:44 cut ✓      [show]
```

---

## Top 5 changes, in order

1. **Split Decide from Upload, as in the mock.** Each Upload step is the "where in YouTube" line, the value, one big primary Copy (or Copy path + Finder) button, and Next. Approve/Edit becomes one compact chip. Pools, shortlist, re-pairing, Mark winner and Tuber's reasoning move to the Decide view. (Fixes B1, M2, and David's items 15, 24, 25, 33.)
2. **Give the wizard the screen.** In `zone=launch`, collapse the project sidebar to icons, hide the Project strip and the Launch heading, put the video chip in the step header, and scroll to the top on step change. (B2, M7, items 1, 34.)
3. **Replace the fold cluster with line-clamped phone/desktop previews**, plus one action line only when the link is hidden. (M1.)
4. **One status language in the rail.** Always a step number, a trailing status dot, and one "N decisions left" counter. Fix the wrong states: Pinned comment ●, Visibility "9" on a live video. (M3, item 3.)
5. **Show brand defaults as values, not decisions.** No per-video Approve, no Copy for radio/dropdown fields, strip "26", auto-skip empty Playlists. On a published video, show the Live strip and land on Pinned comment. (M4, M6.)

## Cut entirely

- The fold's warning box, character counter, "aim for under ~69", brown small print and highlight band.
- The "Proposed by tuber; waiting for you. Source: proposal by agent:tuber." provenance line on every card.
- The title pool, thumbnail pool, "Pick a title and a thumbnail" bar and the duplicate shortlist pairs from the Upload step (they move to Decide).
- The Copy buttons on Audience, Category and Language (they're clicks in YouTube, not pastes).
- The "BRAND DEFAULTS · X [BRAND DEFAULTS]" double label and its Approve button.
- The rail legend ("✓ decided · ● waiting for you · – not ready"), once the dots are self-evident.
- The "PROJECT trash · renders · apps · resources" strip and the "LAUNCH" h3 inside the wizard.
- The second "Copy SRT path" button.

## Praise (keep these)

- The "where in YouTube" line on every step (e.g. "YouTube Studio → Create → Upload videos → Select files. Press Cmd+Shift+G, paste the path") is exactly right.
- Copy path / Finder on every file, and the keyboard hints (← → C S).
- The subtitles merge into step 1 reads well: video and .srt in one place, with "With timing (don't paste the text)".
- Empty steps turn Next into "Skip for now", an honest and fast affordance.
- Brand: light only, cream canvas, Oswald headings, yellow kept for primary actions. It looks like AppyDave.

## Screenshots

All under `/Users/davidcruwys/dev/ad/brains/.playwright-mcp/`:
`uxr-d03-01-landing.png`, `uxr-d03-01-video-subtitles.png`, `uxr-d03-02-title-thumbs.png`, `uxr-d03-03-description-full.png`, `uxr-d03-04-playlists.png`, `uxr-d03-05-audience.png`, `uxr-d03-06-tags.png`, `uxr-d03-07-language.png`, `uxr-d03-08-end-screen.png`, `uxr-d03-09-visibility.png`, `uxr-d03-10-youtube-link.png`, `uxr-d03-11-pinned-comment.png`, `uxr-d02-00-landing.png` (loading state), `uxr-d02-01-video.png`, `uxr-d02-02-title-thumbs.png`, `uxr-d02-03-description.png`, `uxr-d02-03b-fold-zoom.png`, `uxr-d02-10-youtube-link.png`.
