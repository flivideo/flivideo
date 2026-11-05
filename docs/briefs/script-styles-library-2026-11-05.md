---
created: 2026-11-05
timestamp: 2026-11-05T07:30+07:00
---
# Brief — Script-style library (text lane), M2 worker

**Purpose**: Reverse-engineer 5 script styles into typed Story Pilot guides (structure + verbal style each), so Story Pilot can later offer 3–4 of them. **Owner**: flivideo-orch (Swagger, M4). **Machine**: M2 (David, 2026-11-05: "run on the M2 … YES"; M2 has 107 GB free, M4 62 GB).

**David's go (2026-11-05)**: steps 1–4 below. Series reading confirmed: **Series B** = AITLDR daily Claude-skill series (published on/after 2026-09-15; project folders `v-aitldr/b01…b30`); **Series A** = AITLDR videos before 2026-09-15 (Alex-hosted, "OLD" era).

## Rules
- Captions only via the **tube-harvest** skill scripts (`~/dev/ad/appydave-plugins/appydave/skills/tube-harvest/scripts/fetch.py`, yt-dlp, free). One batch: `2026-11-05-script-styles` (it exists; manifest at `~/dev/upstream/tubescripts/_batches/2026-11-05-script-styles/manifest.jsonl`; append rows, creator slugs `aitldr`, `appydave`, `openrig`, `maitis`). Read `tube-harvest/SKILL.md` first; obey its pacing; use `--cookies chrome` only if 429s persist.
- **No paid transcription, no API keys, no installs.** A video with no captions → record `no-captions` in coverage; do not transcribe it. Report it; orch decides.
- No audio/video downloads in this lane (the visual lane is separate).
- Read-only on the M4 (`ssh davidcruwys@100.82.235.39`): you may read `/Users/davidcruwys/dev/video-projects/published/{aitldr,appydave}/videos/*/metadata.json` and `/Users/davidcruwys/dev/aitldr/aitldr-brain/research/old-vs-new-2026-10/` to choose samples. Never write there.
- Never edit VERBAL-STYLE.md, Story Pilot code or guides, or anything in FliStudio. Do not wire guides in.
- `git pull` every repo before you start (`~/dev/upstream/tubescripts`, `~/dev/ad/flivideo`, `~/dev/ad/appydave-plugins`, `~/dev/ad/brains`). Commit + push your outputs (tubescripts and flivideo) when done. Never commit secrets.
- Use `command grep` (bare grep is shimmed).

## Steps
1. **Sample + fetch.**
   - AITLDR Series A: 25 **long-form** videos published before 2026-09-15, spread across the era (not just the last 25), preferring ones with high views. Say how you picked.
   - AITLDR Series B: **every** video on @aitldr published on/after 2026-09-15 (≈38 by 10-29, likely more now). Long and short both; tag each row long/short.
   - AppyDave: the **last 25** uploads on the AppyDave YouTube channel (use yt-dlp's flat playlist listing to get the true newest 25; the M4 metadata looked sparse).
   - Mike/OpenRig: already done — qccsfUnrQ9w (fetched), CYRJDTcTKhQ, AL-PQuB2wy0 (`~/dev/upstream/tubescripts/openrig/`). Existing analysis: `~/dev/ad/brains/openrig/spoken-scripts/` (spoken-script-template.md, mike-mechanism.md, spoken-vs-read.md) — built from only the latter two.
   - Maitis @maitis-ai: list the channel; sample **15** = the 10 most-viewed long-form + the 5 newest long-form (dedupe; top up from most-viewed). State the channel's total count.
   - Write `~/dev/ad/flivideo/docs/script-styles/selection.json`: per style, the chosen video ids with title, date, duration, views, transcript path. (The visual lane will reuse it — write it as soon as selection is done, commit + push it immediately.)
2. **Forge.** For each style (`aitldr-old`, `aitldr-new`, `appydave`, `mike`, `maitis`): run **brand-dave:structure-forge** (8–15 exemplars of ONE format) and **brand-dave:verbal-style-forge** (10–15 exemplars). Output to `~/dev/ad/flivideo/docs/script-styles/<style>/STRUCTURE.md` and `VERBAL-STYLE.md`. If a style mixes formats (e.g. Series B long vs short), split by format or say which format the guide covers.
   - Each file opens with a `storypilot.guide/1` header: `schema`, `id` (`<style>-structure` / `<style>-verbal`), `label`, `type` (structure | verbal), `level: global`, `gist` (one line), `appliesTo` where it fits (`{form: story|tutorial, length: short|long}`). Reference: `~/dev/ad/flivideo/flistudio/modules/storypilot/guides/build-story.md`. The header must be plain `key: value` lines between `---` fences (appliesTo as a flow map `{form: story, length: short}`), exactly as build-story.md does it. Orch validates every file with `parseGuide` on the M4 at the gate (the M2 has no built copy of it).
   - Each file has: **Script type it fits** (story / tutorial / explainer / other, with why); **Sources** (video ids + titles); **Measured** (counts, timings, word rates, hook lengths — with how measured) kept separate from **Interpreted**; strategic-intent sections the forge skills leave for a human marked `TODO(David)`, not invented.
   - Mike: add `mike/WHAT-CHANGED.md` — what qccsfUnrQ9w changes in the existing spoken-scripts analysis (confirmed / contradicted / new). Do not edit the brains files.
3. **Coverage.** `~/dev/ad/flivideo/docs/script-styles/coverage.md`: table source × wanted × found-on-disk × fetched × missing (with reason).
4. **Matrix data.** `~/dev/ad/flivideo/docs/script-styles/matrix.md`: rows = 5 styles; columns = Structure guide, Verbal-style guide, Script type, Sample size, plus a "Strongest trait" one-liner and a "Fit for Story Pilot" note. Then **one recommendation** (in a section, with reasons): which 3–4 styles Story Pilot should offer first.

## Report back (in your session, then stop)
Counts before/after, the coverage table, the 10 guide paths, the recommendation, the commit SHAs, and anything not verified. If blocked (429 that won't clear, a forge skill missing on the M2), stop and say so — do not work around it.
