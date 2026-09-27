---
created: 2026-09-27
timestamp: 2026-09-27
status: proposed — awaiting David's go
owner: flicut-rsch (plan) → flitools + flicut windows (build, after go)
---

# Plan: FliCut word alignment — one word timeline, honest timings

**Job**: Stop the "fix one thing, break another" cycle in FliCut. The cause is not the cut model. It is the words underneath it:
- Whisper writes what you *meant*, not what you said: it drops repeats and false starts and folds them into long words.
- Its word edges are measured **303 ms early** on d06.

Everything built on those boxes then disagrees: the Script text, the captions, the word highlight, and the cut-to-word mapping.

This plan replaces the word source and makes every word-shaped output a projection of **one word timeline**:
- **FliTools** produces a verbatim, acoustically timed word list (WYSIWYG: exactly what was said, with honest edges). It makes no editorial decisions.
- **FliCut** owns all editorial choices.
- The Script text, captions and highlight are all *derived* from the source words plus the edit. None of them keeps its own timing.
- "Heal this sentence so it says X" sits on top as the last resort, not the foundation.

**Mode**: code

**Created**: 2026-09-27

**Status**: PLAN ONLY. Nothing is built until David says go.

---

## 0. What the evidence says (why this plan, and not another)

Measured today on d06 (01-1-intro, 02-1-overview, 04-1-annotate). The full scripts and table are in `/Users/davidcruwys/dev/ad/brains/video-editing-as-code/spikes/2026-09-27-alignment/results.md`.

| d06 failure | Whisper (what FliCut uses today) | ElevenLabs Scribe v2 | What it means |
|---|---|---|---|
| "we got the… we got the thumbnail" | one "we got the"; "thumbnail" 1.46 s long | both kept, "the," ends 35.50 s, "thumbnail" 0.48 s | Verbatim ASR fixes the dropped phrase |
| three takes in 04-1 | false starts folded ("that" 1.48 s, "it" 2.62 s, "prompt" 1.70 s) | "ki-", "so that…", "f-", "And here's the…" all kept; 0 words over 1.2 s | Take detection gets real boundaries to work from |
| "analyze" clipped by a pause cut | ends 440 ms early (15.76 vs sound to 16.20) | ends 20 ms early | Honest word ends stop the clipping |
| "And" cut but still heard | box 20.14–20.40 sits on a low murmur **before** the word | "And" 20.46–20.52; the sound starts 20.42 | The cut missed the word because the box was wrong. ⚠️ The earlier reading "the sound is at 19.90–20.14" is the word **"this"**; Scribe, CrisperWhisper and a CTC aligner agree independently |
| "recently" struck by an "And" cut | "recently" box starts 8.98, on top of "And" | "And" 9.04–9.18, "recently" 9.24–9.72 | Boxes no longer overlap, so a cut on one cannot take the other |
| **All word ends at pauses (n=33)** | mean −303 ms, 0% within 50 ms, **100% would clip audio** | mean −6 ms, MAE 77 ms, 33% clip. **Plus energy refine: MAE 57 ms, 12% clip** | Whisper edges are unusable for cutting. Scribe plus a cheap energy refine is good enough to cut on |

Two findings change the plan against the desk research:
1. **The aligner is not the primary timing source.** A local CTC forced aligner (MMS) on Scribe's text beat Scribe on word *starts* (72 vs 86 ms MAE), but lost on *ends* (114 vs 77 ms). It also failed on cut-off words ("ki-" +520 ms, "the…" −290 ms), which are the words that matter for takes. Scribe's own timings plus energy refinement win. The aligner's job is **re-timing text that was corrected**, not first-pass timing.
2. **FliCut already has most of the right model.** ADR-0002 already holds the source-media takes, written only by transcription; timeline segments are source ranges (an EDL: edit decision list); words resolve to segments. What is broken is the words themselves, plus three places that re-derive word timing separately:
   - the Script's word-to-clip midpoint rule;
   - `cuesFromProject` (captions);
   - `heard-captions.ts`, today's workaround that re-transcribes the finished audio so captions match what is heard.

   The workaround is a second source of truth. This plan retires it.

---

## 1. Stack

- **FliTools** (`/Users/davidcruwys/dev/ad/flivideo/flitools`, Node service on :7161, `flitools.transcript/1`). It is the only transcriber and owns transcript health (David, 2026-09-27). Today it runs Groq whisper-large-v3 with an mlx fallback.
- **FliCut** (`/Users/davidcruwys/dev/ad/flivideo/flicut`, Electron). The relevant modules:
  - `src/shared/layers.ts` (relayout, padding, `wordSpanWithin`, `userCutPaddingCap`);
  - `src/shared/transcript.ts`;
  - `src/shared/subtitles.ts` (`cuesFromProject`);
  - `src/shared/heard-captions.ts`;
  - `src/shared/corrections.ts` (ADR-0008 overlay);
  - `src/renderer/src/Script.tsx` and `Editor.tsx` (the word highlight);
  - `src/shared/take-groups.ts`.
- **fli-core**: thin typed FliTools client, plus `readWords` for the suite word store (`fli.words.json`, FliStudio is the only writer).
- **ElevenLabs Scribe v2** (`POST /v1/speech-to-text`, `model_id=scribe_v2`, `timestamps_granularity=word`). Measured cost on d06 is about $0.22 per audio hour. The key is in the fleet env files; never commit it.
- **Energy refinement**: 10 ms RMS against the clip's noise floor (+12 dB). It is pure numeric code, about 30 lines, already written in the spike (`score.py` `refine_end`).
- **Local fallback ASR**: mlx whisper stays as the offline fallback. It must be marked `verbatim: false`, so FliCut knows its timings can't be trusted for cutting.
- **Re-aligner for corrected text** (phase 3): pick between ElevenLabs Forced Alignment (the current key lacks the `forced_alignment` permission; David must widen it) and a commercially licensed local CTC model. ⚠️ The default MMS weights in ctc-forced-aligner are CC-BY-NC.
- **Conventions**:
  - FliCut ADR-0001/0002/0003/0007/0008 stand.
  - "Cut" in identifiers means MASK.
  - Source ranges never change from a user gesture.
  - `EPSILON` is not the minimum frame.
  - Any new settings field needs `.default()`.

## 2. In Scope

**Phase 1 — FliTools: a verbatim, honest word source**
- Add an engine `scribe` (ElevenLabs Scribe v2) as the **primary** raw transcriber. Groq whisper becomes the second choice, and mlx the offline fallback.
- Emit `flitools.transcript/2`, a superset of v1 so old readers keep working. Each word carries:
  - `id` (stable within the transcript);
  - `text`;
  - `start` and `end` (engine);
  - `endRefined` (energy);
  - `kind` (`word | cutoff | filler | event`);
  - `confidence?`.

  Top-level fields: `verbatim: true|false`, `timing: {engine, refine: "energy-v1", floorDb}`, `source.sha256`.
- Energy end refinement runs inside FliTools, once per transcript, so FliCut never re-derives it.
- Health rules gain "folded word" (any word over 1.2 s) and "unexplained speech" (a voiced run of 0.5 s or more with no word). These become suspect reasons, and a Whisper transcript that trips them is retried on Scribe.
- Reuse by content hash stays. A v1 transcript is **not** reused when a v2 source is available: it is re-made once, and the cost is logged.

**Phase 2 — FliCut: one word timeline, three projections**
- **One function answers "which source words are heard, and when, in the output":** `wordTimeline(project) → [{wordRef, text (after corrections), srcStart, srcEnd, outStart, outEnd, state}]`, where `state` is `kept | cut | boundary`. It is built from:
  - `media.takes` (source words);
  - `timeline.clipsWithCuts` (the EDL);
  - the export plan's frame-snapped segments.
- **The Script, the SRT/TXT and the word highlight all read `wordTimeline`.** `cuesFromProject` becomes a grouping of `wordTimeline` rows; the highlight looks up the row that contains the playhead's output time. `heard-captions.ts` is retired to a **check**: it re-transcribes the render and reports disagreement. It is no longer the caption source.
- **Word state comes from identity, not overlap.**
  - A word is `cut` when a mask covers 90% or more of its refined interval.
  - It is `kept` when a mask covers 10% or less.
  - Anything between is `boundary` and shows a marker. It is never silently struck or silently kept (the "recently" bug).
  - A cut the human makes by selecting words is stored as those words' refined span (ADR-0007's exactness carries over).
- **Padding for FliCut's own pause cuts** drops from the Whisper-era 0.15 s to a value set from measured data. The spike's p90 end error is 156 ms before refinement; the refined ends allow a smaller pad. The new value is proven on d06 rather than assumed.
- **Auto-join** at every kept/kept seam: snap to the quietest 10 ms frame within ±40 ms, then a 10 ms equal-power crossfade. Room tone is out of scope for v1 (see §3).

**Phase 3 — corrected text and "heal a sentence" (designed here, built only after phases 1–2 prove out on a real video)**
- **Re-time corrected text.** When David fixes words (ADR-0008 overlay), captions already use the fixed text. Timings are re-derived only when the fix changes the word count, by forced-aligning the corrected phrase inside its source span. The result is stored as an overlay on the edit, never written back to the transcript.
- **Heal this sentence to say X** is the top-level verb:
  - Select a sentence, type the target text.
  - FliCut first tries **reuse**: find the words in this or another take (take groups) and cut to them.
  - Next it tries **cut and join** (phase 2).
  - Only then does it **regenerate**: an inpainting backend (Resemble Audio Edit API, or ElevenLabs with a re-recorded line) conditioned on about 0.75 s either side. It generates 2–3 candidates for audition.
  - **Lip-sync** (sync.so lipsync-2, about $0.05/s) runs only when the face is on screen and the regenerated span changed length or words.
  - Every heal is recorded on the edit (`healedBy`, engine, cost, a reference to the original) and is reversible.
- The heal is a separate plan and a separate "go". This plan only reserves its place: the `wordTimeline` rows and `boundary` markers are the hooks it attaches to.

**Migration of existing FliCut edits**
- A project remembers which transcript produced its takes (`media.transcriptRef = {sha256, schema, engine}`).
- On opening an edit whose media has a v2 transcript available, FliCut offers **"Upgrade words"**; it does not upgrade silently. The upgrade:
  1. Converts every existing human mask (`cutBy: 'user'`) to **its source time range**. That is what it removed; masks are already source ranges, so nothing is lost.
  2. Replaces `media.takes` from the v2 words (take segmentation re-runs).
  3. Re-applies each human mask over the same source range, and flags any mask whose new word state is `boundary` for review.
  4. Re-keys `corrections` (`takeId#elementIndex`) by matching old and new word sequences: exact match, substitution, or unmatched → flagged. ADR-0008 already names this key-migration debt.
  5. Re-runs FliCut's own proposals (pauses, fillers) fresh; they are machine-made and cheap.
  6. Saves an undo snapshot first (ADR-0004/0006 history), so the upgrade is one undo step.
- **d06 is the migration test case**: its "And", "recently", "analyze" and "we got the" edits must come out right after the upgrade.

## 3. Out of Scope

- Building anything before David's "go" on this plan.
- The `flicut` window's live bug fixes. It keeps working, and this plan does not touch its current files until phase 2 is scheduled with it.
- Voice-clone setup, the regeneration backends and lip-sync: phase 3 is designed here but built under its own plan and spend approval.
- Room-tone fill at joins (v2 of auto-join, once crossfades are proven).
- Shipping CrisperWhisper, VoiceCraft or F5-TTS weights (non-commercial licences), or the default MMS CTC model (CC-BY-NC).
- Rewriting FliCut's MASK/TRIM/SPLIT vocabulary, or the owed identifier renames (AGENT-NOTES: never alongside a semantic change).
- FliCast's and FliHub's own caption paths. They can adopt `flitools.transcript/2` later.
- The ChatGPT project "AppyDave Videos".

## 4. Definition of Done

On d06, after "Upgrade words":
- The Script, the exported SRT and the word highlight agree word-for-word and within one frame, because all three come from `wordTimeline`.
- The four named d06 failures render correctly ("analyze" whole, "And" gone, "recently" kept, "we got the" present and cuttable).
- The 04-1 takes show their false starts as separate words.
- FliTools serves `flitools.transcript/2` from Scribe with the Whisper fallback working.
- `heard-captions` runs as a disagreement check and reports **0** disagreements on d06.
- David has watched the d06 cut in FliCut and said it's right.

## 5. Acceptance Criteria

| # | Criterion | How to check |
|---|-----------|--------------|
| 1 | FliTools returns `flitools.transcript/2` with `verbatim: true` from Scribe for a hub recording, and v1 readers still parse it | `POST :7161/api/transcribe` on d06 02-1 → `schema == "flitools.transcript/2"`, `engine.name == "scribe"`; FliHub/FliStudio reader tests pass unchanged |
| 2 | The dropped phrase is present | d06 02-1 words between 34.5 and 37.3 s contain "we got the" twice |
| 3 | No folded words on d06 | count of words with `end - start > 1.2` across d06 = 0; health reason `folded-word` absent |
| 4 | Take false starts are separate words | d06 04-1 contains the cut-offs "ki-" and "f-" as `kind: cutoff`, and "so I('m) just" 5 times |
| 5 | Refined word ends meet the accuracy target on d06 | spike `score.py` rerun on the v2 output: end MAE ≤ 60 ms and "clips audio" ≤ 15% at pause edges (spike baseline: 57 ms / 12%) |
| 6 | Whisper fallback is marked and flagged | force the mlx engine → `verbatim: false`; FliCut shows a "timings approximate" badge on that media |
| 7 | One word timeline feeds all three outputs | unit test: for 10 random mask sets on d06, the SRT cue words == the Script's kept words == the highlight lookup sampled every 40 ms, and cue times are within 1 frame of the `wordTimeline` `outStart`/`outEnd` |
| 8 | Nothing else computes word timing | `grep` finds no word-to-time logic outside `wordTimeline` (the midpoint rule in `elementsWithin`/`wordsOwnedByClip` is replaced or delegates to it) |
| 9 | Partial overlap never silently strikes a word | test: a mask covering 11–89% of a word yields `state: boundary` and a Script marker; 62% on "recently" → boundary, not cut |
| 10 | d06 named edits are right after "Upgrade words" | open d06 → Upgrade words → "And" (01-1 ~20.44 s) is cut and not heard, "recently" kept, "analyze" plays to its end, and "we got the" appears as its own cuttable words; checked by test and by David's ear |
| 11 | Migration keeps every human cut and correction, or flags it | upgrade report on d06 lists 0 lost masks and 0 lost corrections; each unmatched item is listed as `review`; one undo restores the pre-upgrade edit byte-for-byte |
| 12 | Auto-join removes clicks at seams | render d06; at every seam the peak sample jump across the join is ≤ the clip's local 95th-percentile sample jump (automated check); David hears no clicks |
| 13 | heard-captions is a check, not a source | the SRT is written from `wordTimeline`; the heard-captions run on the render reports 0 word disagreements on d06 |
| 14 | Cost is recorded | each Scribe job logs audio seconds and dollars; d06's total is under $0.10 |
| 15 | Phase 3 hooks exist without the heal being built | `wordTimeline` rows carry `boundary` state and a stable `wordRef`; the heal plan is a separate doc awaiting its own go |

## 6. Key References

- Spike results (this plan's evidence): `/Users/davidcruwys/dev/ad/brains/video-editing-as-code/spikes/2026-09-27-alignment/results.md`
- Desk research: `/Users/davidcruwys/dev/ad/brains/video-editing-as-code/ai-speech-editing-research.md`, `/Users/davidcruwys/dev/ad/brains/video-editing-as-code/editor-ux-research.md`, `/Users/davidcruwys/dev/ad/brains/video-editing-as-code/asr-boundary-and-aspect-findings.md`
- ChatGPT deep research + dossier: conversation `6ab8e4df-0364-83ec-9a01-eb5a542b2adb` ("Voice cloning options", project AppyDave Workflow & Process); Captain's Log dossier code: see results.md
- FliCut decisions: `/Users/davidcruwys/dev/ad/flivideo/flicut/docs/kdd/decisions/` (ADR-0002 word masks splice the timeline, ADR-0003, ADR-0007 exact hand cuts, ADR-0008 corrections overlay)
- FliCut conventions: `/Users/davidcruwys/dev/ad/flivideo/flicut/docs/AGENT-NOTES.md`, `/Users/davidcruwys/dev/ad/flivideo/flicut/docs/cut-model-spec.md`
- FliTools architecture + health rules: `/Users/davidcruwys/dev/ad/flivideo/flitools/docs/architecture.md`
- d06 edit: `/Users/davidcruwys/dev/video-projects/v-appydave/d06-presenter-headshot-artefact/fli.cut.d06-presenter-headshot-artefact.json`
- Handover that commissioned this: `/Users/davidcruwys/dev/ad/brains/docs/handovers/HANDOVER-2026-09-27-flicut-alignment.md`
- ElevenLabs STT: https://elevenlabs.io/docs/overview/capabilities/speech-to-text · Forced alignment: https://elevenlabs.io/docs/overview/capabilities/forced-alignment

## Build order and owners (after go)

| Step | Owner window | Gate |
|---|---|---|
| 1. FliTools `scribe` engine + transcript/2 + energy refine + new health rules (AC 1–6, 14) | `flitools` | d06 score.py rerun meets AC 5 |
| 2. FliCut `wordTimeline` + the three projections read it (AC 7, 8, 13) | `flicut` | AC 7 test green; no behaviour change on a v1 project |
| 3. Word state by identity + boundary markers + measured padding + auto-join (AC 9, 12) | `flicut` | d06 renders click-free |
| 4. "Upgrade words" migration (AC 10, 11) | `flicut` | David plays d06 and says it's right |
| 5. Phase 3 heal: separate plan, separate spend approval | — | David's go |

## Decisions David owns (asked, not assumed)

1. **Scribe primary, cloud.** It uploads audio to ElevenLabs, about $0.22/hour. The alternative is local CrisperWhisper for evaluation only, since its weights are non-commercial. Recommendation: Scribe primary, Groq and mlx as fallbacks.
2. **Widen the ElevenLabs key** to include `forced_alignment`, for phase 3 re-timing of corrected text. Recommendation: yes when phase 3 starts, not now.
3. **Upgrade existing edits on request** rather than automatically. Recommendation: on request, with d06 as the first.

---

## Suggested `/goal` condition

```
Phases 1-2 of /Users/davidcruwys/dev/ad/flivideo/docs/briefs/flicut-alignment-plan.md are done when: (1) FliTools POST /api/transcribe on d06 02-1-overview returns schema flitools.transcript/2 with engine.name "scribe" and verbatim true, and FliHub/FliStudio transcript reader tests pass unchanged; (2) d06 02-1 words 34.5-37.3 s contain "we got the" twice; (3) no d06 word has end-start > 1.2 s; (4) d06 04-1 contains cutoffs "ki-" and "f-" with kind cutoff; (5) re-running /Users/davidcruwys/dev/ad/brains/video-editing-as-code/spikes/2026-09-27-alignment/score.py against the v2 output gives end MAE <= 60 ms and clips-audio <= 15%; (6) forcing mlx yields verbatim false and FliCut shows a timings-approximate badge; (7) a FliCut unit test over 10 random mask sets on d06 shows SRT cue words == Script kept words == highlight lookup every 40 ms, cue times within 1 frame of wordTimeline; (8) grep finds no word-to-time logic outside wordTimeline; (9) a mask covering 11-89% of a word yields state boundary with a Script marker; (10) after "Upgrade words" on d06, "And" (01-1 ~20.44 s) is cut, "recently" kept, "analyze" whole, "we got the" present; (11) the upgrade report lists 0 lost masks and 0 lost corrections and one undo restores the prior edit byte-for-byte; (12) the rendered d06 has no seam whose peak sample jump exceeds the local 95th percentile; (13) the SRT is written from wordTimeline and heard-captions reports 0 disagreements; (14) Scribe jobs log seconds and dollars and d06 costs < $0.10. Constraints: FliCut and FliTools test suites stay green; ADR-0002/0007/0008 unchanged in meaning; no ElevenLabs key or secret committed; no voice-clone or lip-sync API called; no change outside flitools/, flicut/ and fli-core's client. Or stop after 20 turns and report which rows are unmet.
```
