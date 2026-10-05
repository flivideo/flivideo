# Transcription robustness: word lists, engine levelling, scorecard (2026-10-05)

**Purpose**: Make transcription hands-off for every future video (D07 and on). The word list always applies, engines level each other up word by word, and every change is measured against a baseline.
**For Agents**: flitools owns this. flivideo-orch dispatched it on David's go (2026-10-05, "GO", "execute on whatever you think best"). Transcription stays deterministic code; no agent or model sits in the loop.

## What went wrong (why this brief exists)
The word list for CrisperWhisper was built and merged on 10-04 (5a15fbb). The M2 came back on 10-05 still running 6ddd8b6, and the backfill started by itself, so all of D02–D06 ran WITHOUT the word list. The M4 handed jobs to an out-of-date worker without checking.
David: "when we get to new videos in the future, like D7 or whatever, I don't have to go through this bullshit. I need it to be all robust and working properly."

## David's words on the design (2026-10-05)
- "We have four different audio systems, though we've only tested three so far." The four: Groq, mlx-whisper, CrisperWhisper and ElevenLabs Scribe (untested, off).
- "With the three we've got, we should be able to get an increment. We should have smart levelling up as each one kicks into play."
- "CrisperWhisper does some really good stuff, but sometimes it fails, and it may need the Groq or the mlx-whisper fallback mechanisms, mostly at a word level, not at a full structure level."
- "We got time... I don't care if we had to rerun everything again, as long as we can keep track of whether we've improved or not."
- Project codes (D01, A01…Z99) are "a never-changing code"; handle them "by a programmatic mechanism rather than a word list".
- Word lists "can have sources that are not just here"; agents will be first-class citizens in the future. (Correction, David 2026-10-05: the agent is **Cutty**. "Cardi" is a mishearing of Cutty and is now Cutty's heardAs.)

## Work, in order

### 1. Worker version gate (robustness, first)
- Before handing a pass-2 job to a remote worker, the M4 checks the worker's FliTools version (commit) against its own.
- If the worker is behind, deploy it automatically (`scripts/deploy-worker.sh`, as for 10-05). If that can't be done, HOLD the queue with a visible reason in queue.status. Never run a job on old code silently.
- Record the worker's commit and `engine.vocabulary` on every result, so a missing word list shows up in the data.
- Test: a fake worker reporting an older commit gets deployed or held, never sent work.

### 2. Scorecard + baseline (so improvement is tracked)
- A deterministic verb (e.g. `transcribe.scorecard { project }`) that reports per take and per project:
  - the best engine and which engines exist;
  - agreement % between engines;
  - fillers left;
  - words restored from another engine;
  - word-list hits and misses (each name and its heardAs found or still misheard in the best text and SRT);
  - SRT health;
  - the code/version and vocabulary used.
- Seed: flivideo-orch's comparison script `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/transcription-compare-seed.py` (it writes to a scratch path; make it a real verb).
- **Baseline = today's D01–D06 state:** v-appydave 77b3003a + flitools' per-project commits e20f5eb2…ccbf56e0, word list at 30f20e73. Save the baseline scorecard as a file in the brand repo (e.g. `<project>/hub/transcripts/scorecard.json` with history), so every later run is compared with it.
- Baseline numbers from orch: D01–D06 average agreement 94–99%; ~25 brand mistakes still in SRTs ("abhi/appy dave", "kyber nesis", "head shot", "a cam", "d 0 six", "d zero one", "69" for 16:9, "school", "cardi"); 59/59 takes best = CrisperWhisper.

### 3. Measurement, then re-run (GO from David, M2 only)
- The "no measurement runs" rule from the OOM brief is LIFTED for the M2 only (32 GB, one job at a time, memory gate on). The M4 still never runs CrisperWhisper.
- Run `scripts/measure-crisper-vocab.sh` on the six D01 takes. Check prompt echo and word timings with the real model.
- If it's better, re-run D01–D06 pass 2 with the word list (force). Scorecard before and after; commit per project in v-appydave.
- If it's worse or broken, say so with the numbers and keep the baseline.

### 4. Project codes by pattern, not a word list
- A deterministic normaliser in the spelling stage (SRT/TXT and the best words) turns spoken codes into the canonical code: letter A–Z plus 01–99, e.g. "d 0 six", "d zero one", "D 0 1", "dee oh six" → D06 / D01.
- Only fires on a letter-plus-digits shape. Tests for the false positives (e.g. "a 1" as ordinary speech), and say how it decides.
- Applies to every brand. Not a word-list entry.

### 5. Word-level levelling across engines
- Today: words from Whisper replace CrisperWhisper fillers (df62835); pass-1 splice for folded words; whole-file fallback when CrisperWhisper loops (DJI_0253) or crashes (DJI_0242).
- Target: CrisperWhisper's timings stay the spine. Where it fails on a stretch (loop, crash, folded words, a misheard name the word list knows), take the words for THAT stretch from Groq or mlx, keeping the timing where possible. Fall back per stretch, not per file.
- A name the word list knows wins over a common-word mishearing when another engine heard the name at the same place. That's how "I" for AI and "school" for skill get settled per occurrence, never by a blanket rule.
- Each engine that finishes later (levelling up) re-runs the merge, so the best transcript only ever improves. The scorecard records it.
- Keep the ElevenLabs Scribe slot in the design (off; David: "another day").

### 6. Word-list sources (design note only, no build)
- Write a short note in `/Users/davidcruwys/dev/ad/flivideo/docs/shared-data-levels.md`: word lists may gain sources beyond the three files, e.g. an agent registry (agent names such as Cutty) once agents are first-class. Who would own it, and how it merges.

### 7. Real-word corrections: ARCHITECT FIRST, do not build yet
David (2026-10-05): "Skool needs to be in the word list, even though it is a real word... this fits in with the same problem as the code: should it be a post-review rather than letting the model fix these words that are real? Maybe this is a specific filter that you run post-transcription, and maybe we're going to have a custom rules system around this... This is not just a simple go-and-do-it matter. This is something we need to think through, architect, and build properly."
- Cases: "school"→Skool, "I"→AI, "skill"/"school", "69"→16:9; the project codes (step 4) are the same family.
- Write a design (no code): a post-transcription rules stage. Cover where it sits (after the merge, before SRT/TXT); the rule kinds (pattern codes, context rules, engine-vote, word-list names); per-occurrence decisions with evidence; how a rule is authored and reviewed (David's review vs automatic); a record of every change made, so it can be undone and scored; and how it relates to step 5's levelling and the word store levels.
- Deliver it as a short doc in `/Users/davidcruwys/dev/ad/flivideo/docs/` and report to flivideo-orch for David's review. Step 4 can still ship as the first, narrow rule (codes), but name it as an instance of this stage.

## Rules
- Deterministic code only. Build in the `flitools-build` worktree; never edit the live tree that launchd runs.
- Tests green, pushed to main. Deploy to the M2 with `deploy-worker.sh`. Ask flivideo-orch for the M4 restart (or do it at a safe point between jobs and say so).
- Commit v-appydave transcript changes per project, and report them. Roamy sync is orch's.
- Report to flivideo-orch after each numbered step: commits, scorecard deltas, anything that went the wrong way.
