# Editing pass findings — d01-flivideo-tour (2026-10-04)

**Purpose**: Everything David hit in his first real FliCut edit on Roamy with CrisperWhisper transcripts, ruled and prioritised, for flivideo-orch to execute.

**For Agents**:
- flivideo-orch: split into workers by app (FliCut, FliTools, FliHub, FliStudio, fli-core). Each worker: tests green, pushed to main, commit hash reported.
- Decisions marked RULED are David's — build them, do not re-open them. Items marked IDEA are for the backlog, not this pass.
- Evidence came from a Roamy session reading code and measuring audio; file:line refs were true at the commits named in each section.

---

## P1 — transcript correctness (FliTools, then FliCut)

1. **Words from Whisper, timings from CrisperWhisper (RULED, option 1).** Wherever CrisperWhisper emits `[UH]`/`[UM]` and the Whisper (mlx-flihub) transcript has a real word at the same moment, use Whisper's word. Evidence: `02-2-overview` — CrisperWhisper `"an [UH] influencer"` ×2 where Whisper has `"an AI influencer"`; also Crisper "Is channel" vs Whisper "is a channel", "Abhi Dave" vs "AppyDave". Both engine outputs already exist in `hub/transcripts/engines/<take>.{crisper,mlx-flihub}.json` — no re-transcription. Do it ONCE where transcripts are made (FliTools), so FliCut, FliStudio previews, captions and agents all get the same corrected text. Note today's plain `.txt` silently DROPS `[UH]`, so FliStudio previews read "an influencer" — the word "AI" vanishes.
2. **Give CrisperWhisper the word list.** `flitools/src/transcribe/crisper.ts` takes no vocabulary; groq.ts and mlx.ts do (`vocabularyPrompt`). Feed the same global/brand/project word list. Measure before/after on d01 ("Abhi Dave", "AI", "fly studio", "69 format" = 16:9, "D 0 six" = D06).
3. **A hesitation is a sound, not a word (RULED).** In the FliCut transcript show a real filler as a quiet chip in the same muted style as the pause chip (`⋯ 0.2s`), e.g. `⟨uh 0.2s⟩` — not the word `[UH]`. Never offer "Remember for <brand>" on a fix of a `[UH]` token (it is a sound failure, not vocabulary — David hit this: "Fixed [UH] → AI … REMEMBER FOR APPYDAVE").
4. **Edge case**: `isFillerTake` (`flicut/src/shared/transcript.ts:182`) cuts a take that is only fillers; a misheard "AI" standing alone between pauses would be auto-cut. After (1) this mostly disappears; guard it anyway (don't auto-cut a filler where the other engine heard a word).

## P1 — recording chain (FliHub)

5. **Detect zero-sound holes when a recording lands.** 15 of 33 d01 recordings have mid-speech stretches at digital zero (−90…−105 dB, 0.1–0.7 s, instant on/off) that chop word ends — e.g. `03-4-flistudio.mov` 12.34→12.99 s chops "we". Cause (strong evidence, not yet A/B tested): Ecamm on the M4 records from `KrispAudioDeviceMic`; Krisp zeroes what it judges non-voice. David is switching Ecamm to the real mic. FliHub must flag this at ingest (graph or alert per take), extending its existing mic-check analysis (`flihub/client/src/utils/micGrading.ts`) — David wants to know before editing, not during. FliHub has no audio cleanup step and should not get one.

## P1 — FliCut editing ergonomics

6. **One word, one click (RULED).** Clicking a single word must offer Cut / Uncut / Edit in place. Today cut is designed around a multi-word selection; double-click edits text but hides cut state; there is no Uncut except undo. "And" is the regular offender. Add a single-word uncut path (key + click).
7. **Transcript text size + / − buttons (RULED).** Too small on the laptop. ⌘= / ⌘− are already playback speed (`hotkeys.ts` FC-22), so these are buttons (persisted per machine).
8. **Playing-word highlight too faint (RULED)** — bigger and brighter.
9. **"CLIPPED?" pill clashes with the yellow playing highlight (RULED)** — give it a distinct colour (blue or pink), keep the meaning.
10. **Add clips to an existing cut.** David has 10–15 more takes to record for d01 and FliCut cannot add media to a cut once created (no add/insert media capability found in `src/main/capabilities.ts`). Propose append + insert-at-position as a capability an agent can call; FliStudio's Order list may be the entry point. Report the proposal to David before building if it touches the cut file schema. (His fallback idea: second FliCut + combine in FliEdit.)
11. **Caption strip under the video (RULED, design detail is yours).** When watching rather than reading: show the current phrase (pause-bounded) under the player, current word highlighted, next phrase faint underneath; fixed two-line height; change only at phrase boundaries; short fade — never jumpy. Check `src/shared/heard-captions.ts` for phrase splitting before writing new code.
12. **Zoomed-loupe vs main playback speed felt mismatched** (main at 1×, loupe felt faster, around clipped/shortened areas). Unconfirmed — reproduce and measure first; fix only if real.
13. **Visibility**: "remove filler words" lives only behind the `pace` button — show on the main screen when filler/pause removal is on. Cut colours (`Timeline.tsx:309`: pause #ccba9d, filler #c8841a, words #e0816b) are too subtle to read — propose a clearer legend/contrast (David likes the overview strip with the yellow viewport box — keep it). FliCut has no visible route to the word list — add a Words entry that shows where words live.

## P2 — shared data pattern (fli-core + docs)

14. **Write the pattern down once.** fli-core already implements global / brand / project files for words (`src/words.ts`), brand settings and resources: plain files on disk, any app reads via fli-core, FliStudio is the only writer. Document it as ONE FliVideo-level note (`docs/`), so it stops feeling messy.
15. **Standalone apps can't write.** FliCut's "Remember" goes through FliStudio's `words.add`; with no FliStudio running there's no write path. Decide and implement (e.g. fli-core writes the file directly with the same merge rules when FliStudio is absent).
16. **"Remember" offers brand only.** Add "remember for this video" (project level). David: FliHub should read and write project-level words, not go higher.

## IDEA — backlog only (not this pass)

- **Spoken edit instructions**: the transcript contains placement directions ("I'll include it just after take number three") — could be read and offered as a suggested placement.
- **Heal join** (regenerate ±1 word in David's voice) from `~/dev/ad/brains/video-editing-as-code/ai-speech-editing-research.md` §3 step 6 — researched 2026-09-27, never put on any backlog. Add to FliCut's backlog with that pointer.
- **Segment vs B-roll**: inserted footage that is its own segment belongs in the clip sequence; footage over the voice belongs in FliEdit.

## Out of scope

Krisp/Ecamm configuration (David does that by hand), FliCut cut-engine rewrites beyond the items above, any change to recordings on disk.
