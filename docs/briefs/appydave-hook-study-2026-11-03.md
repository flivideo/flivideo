---
created: 2026-11-03
timestamp: 2026-11-03T20:40+07:00
---
# Brief: AppyDave hook study — research only, feeds W3 (2026-11-03)

**From:** `flivideo-orch`. **To:** `hook-study-rsch` (**M2**, cwd `/Users/davidcruwys/dev/ad/flivideo`). Report to `flivideo-orch`.
**Go:** David via `flivideo-roamy`, ~20:30 ("step 3 hook study, analysis, no code"). **Machine: M2** — unwatched research.

## Data (read-only, already held — no new installs, no new credentials)
- Published AppyDave mirror on the **M4**: `/Users/davidcruwys/dev/video-projects/published/appydave/videos/<videoId>/`
  (`metadata.json` with title + publishedAt, `transcript.txt`); 189 videos. Read via
  `ssh davidcruwys@100.82.235.39 'cat …'` or `scp` copies into your scratch. Pick the **~10 most recent** by `publishedAt`
  (skip Shorts unless fewer than 10 long ones exist in the last few months; say what you picked).
- If `transcript.txt` has no timings, estimate the first ~60 s as the first ~150–170 words and say so; if a timed caption
  file exists anywhere for a video (mirror, the project folder under `/Users/davidcruwys/dev/video-projects/v-appydave/`),
  prefer it.
- Voice rules to compare against:
  `/Users/davidcruwys/dev/ad/appydave-plugins/brand-dave/skills/brand/references/appydave/VERBAL-STYLE.md` (around line 71).
- Context for d13: `/Users/davidcruwys/dev/video-projects/v-appydave/d13-overlay-pilot/` (its Story Pilot script/brief, on the M4).
- David's standing content rule today: drop "I'm AppyDave, let's get into it" from story-style intros.

## Do
1. Per video: title, date, the first ~60 s (quoted, trimmed), **hook type**, the **psychological lever** (curiosity gap, pain,
   contrarian, stakes, proof, story-in-progress, …), **time/words to the first payoff**, and whether "I'm AppyDave, let's get
   into it" (or a variant) appears and **where**.
2. David's **habitual hook patterns** (what recurs, what's missing), and how they compare with VERBAL-STYLE.md :71.
3. **4–6 other hook structures suited to BUILD STORIES** (story-led, cause-and-effect / but-therefore, …): for each, what it is,
   why it fits a build story, and a **one-paragraph example written for d13 (Overlay Pilot)** in David's voice.
4. Write `/Users/davidcruwys/dev/ad/flivideo/docs/research/appydave-hook-study-2026-11-03.md` (Purpose + For Agents, a table for
   step 1). Commit only that file, push.

## Limits
No edits to VERBAL-STYLE.md, settings, scripts, or any project. No code. Keep the M2 light. Timebox ~1.5 h.
STOP and report to `flivideo-orch`: the 10 videos, the 3 strongest habitual patterns, the hook structures proposed, the sha.
