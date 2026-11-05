---
created: 2026-11-05
timestamp: 2026-11-05T10:45+07:00
---
# Brief — SVG + three.js technique test (plain M2 session, not a rig)

**Purpose**: Find out whether SVG assets plus HyperFrames and three.js are a good way to make programmatic explainers quickly, as Martin Puskas claims, or whether something simpler or better wins. **Owner**: flivideo-orch (M4). **David's go**: 2026-11-05. **Machine**: M2 (builds by default; a fresh folder touches nothing live). Exploration only: not a FliVideo build.

## The subject
A 30-second explainer of how an agent team ships a feature, told as a top-down dungeon crawl. The party (lead, builder, QA, reviewer) enters, the tests gate blocks the way, the party fights a bug boss, QA checks, the reviewer opens the door, and the party reaches the loot chest: a shipped PR. No voice-over or music needed; on-screen labels carry the story.

**Art is ours and original.** No characters, monsters, names or visual style from D&D or any existing game.

## Assets: 10 SVGs, written by you (Claude), by hand or by script
lead, builder, QA, reviewer, bug boss, tests gate/door, loot chest, floor tile, wall tile, torch. One palette, one line style, so they look like one set. Keep them in `assets/`, one file each. Make them good: the art quality is part of what's being tested.

## Build the same scene three ways
| | Technique | Question |
|---|---|---|
| A | SVG + GSAP animation in HyperFrames, flat 2D | Is the simple baseline already enough? |
| B | SVG + three.js in HyperFrames (depth, camera moves, lighting) | Does three.js earn its extra work? |
| C | SVG + three.js, playable in a browser: move the party with the keyboard | Can the same assets become something you walk around in? |

A and B render to MP4 at 1920×1080, about 30 s, under 15 MB each. C is one self-contained HTML file that opens from disk with three.js inlined.

Then write a short note on PixiJS, Lottie, Rive and Remotion for this job, from their current docs. Build a fourth version only if one looks clearly better for it, and say why.

## Measure, for each of A, B and C
- Time to build, lines of code, render time, file size, any frames that are visibly broken.
- **The agent-change test:** make the boss red, move the door to the other side, change one label. Record the time and how many lines changed, then re-render. This is the question that matters most for FliVideo.
- Your screenshots of frames at 5, 15 and 25 s.

Give a verdict: which you'd use for an explainer, what you'd never use, and what this did not establish. Be honest if flat 2D wins. Don't call anything "stunning": show it.

## Rules
- **Folder**: `~/dev/labs/svg-dungeon-test/`, created new, with its own `git init`, no remote. Install HyperFrames and three.js only there, nothing global. Use pinned versions and record them. Read the `hyperframes-read-first` skill and its siblings first (if the M2 lacks them, read the HyperFrames docs and say so).
- No paid APIs, no API keys, no image generation, no ChatGPT. David may separately check the unverified Images 2.6 SVG export claim; don't depend on it.
- **Don't touch**: FliStudio, Story Pilot, any FliVideo app or checkout, D18 or D19, `~/dev/rig-work`, or the `workshop-flistudio` rig.
- **The M2 is also running that rig and memory is tight**: one render at a time, no parallel builds. Stop and report if a render needs over 8 GB or the machine is swapping hard. No long-running servers left behind: use a temporary static server only while testing, on a free port above 7300, and stop it.
- HyperFrames is used here as a tool. Don't copy its code anywhere else.
- Use `command grep` (bare grep is shimmed).

## Stop rule
This session doesn't grow. If you find a repeatable pipeline, write it up in `RIG-CANDIDATE.md` with the steps, the seats you'd expect and what a check would look like. Don't build the pipeline.

## Deliverables, in the folder
- `assets/*.svg`, `a/`, `b/`, `c/`, `renders/a.mp4`, `renders/b.mp4`, `c/index.html`, `frames/`.
- `RESULTS.md`: scorecard, the agent-change results, alternatives note, verdict, not established.
- `page/index.html`: a light-only AppyDave page, David's report. Cream `#faf5ec` page, white cards, `#342d2d` text, Oswald + Roboto, no dark theme and no `prefers-color-scheme`. It holds the two videos side by side (`../` is not allowed: copy them into `page/` and use relative paths), the 10 assets shown as a contact sheet (inline), the frame comparisons, the scorecard and the verdict. Link the playable version as `page/play.html`, a copy of C. Keep all of `page/` under 45 MB. Orch publishes it.

Commit in that folder. End your final reply with exactly one line: `APPYNET: done — <one line>` or `APPYNET: blocked — <why>`. Emit that line only when actually done, blocked, or needing a real decision; never for status.
