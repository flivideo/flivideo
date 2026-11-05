---
created: 2026-11-05
timestamp: 2026-11-05T09:20+07:00
---
# Brief — Script-style library, visual and editing lane (M2 worker)

**Purpose**: Record the visual and editing style of each of the 5 script styles, for B-roll Pilot and auto-editing to read later. Not a Story Pilot requirement. **Owner**: flivideo-orch (M4). **Machine**: M2 (David, 2026-11-05: "run on the M2 ... YES"; 107 GB free). Plan shown to David: https://claude.ai/artifact/Sb53xjPe57fX4be9dNjWi8, section "Separate lane".

## Rules
- **Our own channels come from FliVideo first.** AITLDR and AppyDave video files are read over SSH from the M4 (`davidcruwys@100.82.235.39`, read-only) under `/Users/davidcruwys/dev/video-projects/v-aitldr/b*/videos/*/*final.mp4` and `/Users/davidcruwys/dev/video-projects/v-appydave/*/`. Copy to the M2 only what you sample, into a working folder, and delete after frames are taken. Never write on the M4. Never touch the live FliStudio or anything running there.
- **YouTube video download only for**: Mike (3), Maitis (10), and any AITLDR or AppyDave video with no file in FliVideo. List those own-channel exceptions in the report. Use `yt-dlp -f "bv*[height<=720]+ba/b[height<=720]"`, 60 s or more between videos, no cookies. On a 429, wait and retry slower; if it persists, stop and report.
- **Disk**: frames kept about 1.5 GB in total, working video up to 5 GB and deleted after. If the estimate is going to be beaten by more than 2×, stop and report. No paid services, no installs (ffmpeg must already be there; if not, report).
- **Output**: frames outside git at `~/dev/script-style-frames/<style>/<video-id>/`. Files in git at `~/dev/ad/flivideo/docs/script-styles/<style>/VISUAL.md`. Never commit frames or video.
- Do not edit any STRUCTURE.md, VERBAL-STYLE.md, Story Pilot code, B-roll Pilot or any app. Do not build features.
- Use `command grep` (bare grep is shimmed).

## Steps
1. **Sample** from `~/dev/ad/flivideo/docs/script-styles/selection.json` (`git pull` first): 10 each of `aitldr-new` (long), `aitldr-old`, `appydave`, `maitis`, spread across the list, and all 3 of `mike`. Say how you picked. Write the list to `docs/script-styles/visual-selection.json`, with each video's source (FliVideo path or YouTube).
2. **Extract** per video with ffmpeg: 1 frame every 2 s at 640 px wide JPEG, and cut points by scene detection (`select='gt(scene,0.3)'` with timestamps). Record the threshold; if it clearly over- or under-detects for a style (screen recordings often do), adjust and say so.
3. **Analyse.** For each style write `VISUAL.md` with:
   - **Measured**: cuts per minute (per video and median), mean and median shot length, how measured.
   - **Observed from frames** (sample and look at them; do not read every frame): shot types, framing, on-screen text and graphics, B-roll share (estimate, with how), transitions, avatar or presenter use.
   - **Interpreted**: what makes it that style.
   - **Sources**: video ids and titles. **Not established**: anything you could not tell.
   - **Who reads this**: one section naming where B-roll Pilot and auto-editing would read it (check `flivideo:broll-pilot` and the FliEdit/FliCut docs for the real seam; if there is none yet, say so). Do not build it.
4. **Compare.** `docs/script-styles/visual-matrix.md`: rows = 5 styles; columns = cuts per minute, shot types, on-screen text, B-roll share, framing, transitions.
5. Delete the working video. Report final disk used. Commit + push (`git pull --rebase` first).

## Report back
Counts per style, the table, own-channel videos that had to come from YouTube, disk used, commit SHA, not verified. End with exactly one line: `APPYNET: done — ...` or `APPYNET: blocked — ...`. Emit that line only when actually done or blocked, never for status. Report from your own output; nothing else.
