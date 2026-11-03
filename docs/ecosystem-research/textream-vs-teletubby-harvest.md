---
type: reference
tags: [flivideo, ecosystem-research, teleprompter, teletubby, textream, voice-following, B686]
description: "Textream (MIT, Swift) against Teletubby: how Textream's voice-following works in code, a side-by-side feature table with a harvest verdict per row, and the options for adding voice-following to Teletubby."
created: 2026-11-03
timestamp: 2026-11-03T20:40+07:00
---

# Textream vs Teletubby: what to harvest (voice-following first)

**Purpose**: Answer David's question of 2026-11-03: *"Is there anything we can harvest from Textream for Teletubby? The main
thing is the voice: listening to the voice and automatically changing the text."* Covers how Textream follows the speaker,
a full side-by-side comparison, and the options for Teletubby.

**For Agents**: Research only. It was a code read on the M2 (brief
[../briefs/textream-vs-teletubby-harvest-2026-11-03.md](../briefs/textream-vs-teletubby-harvest-2026-11-03.md)). Nothing
was built, run or given mic access. **Observed** = read in source at the commit below. **Inference** = reasoning, not
tested. The **Recommendation** is not approved. ⚠️ Teletubby's `CLAUDE.md:284` lists *"live listening … sync-to-voice"* as
**explicitly NOT built, and not to be added without asking**, so every option here needs David's go.

Sources: Textream `~/dev/upstream/repos/textream` @ `2c02f3e` (v1.7.1, **MIT, © 2026 Fatih Kadir Akin**). Teletubby
`/Users/davidcruwys/dev/ad/flivideo/teletubby` @ `44e0011`. FliTools `/Users/davidcruwys/dev/ad/flivideo/flitools`. Earlier
trial: [candidates/teleprompter.md §Experiment X5](candidates/teleprompter.md). Paths below are relative to
`Textream/Textream/` (the macOS app) unless they say otherwise.

---

## 1. How Textream follows your voice (Observed)

```
mic ─► AVAudioEngine tap (mono, hardware rate) ─► SFSpeechAudioBufferRecognitionRequest (partials ON)
                         │                                        │  each partial = WHOLE transcript so far
                         └► RMS level ─► VoiceActivityDetector    ▼
                                                     matchCharacters(spoken)
                                    ┌──────── char-level fuzzy scan ───┐
                                    │                                  ├─► bestOffset ─► 2-of-3 gate ─► recognizedCharCount
                                    └──────── word-level fuzzy scan ───┘                        (only ever moves forward)
                                                                                                      ▼
                                                           MarqueeTextView: highlight to char N, active word centred
```

| Stage | What it does | Where |
|---|---|---|
| **Capture** | A fresh `AVAudioEngine` each session, so a mic switch picks up the new format. Selected mic set via `kAudioOutputUnitProperty_CurrentDevice`. Tap downmixes to mono at the hardware rate and also computes RMS for the waveform and VAD. Restarts on `AVAudioEngineConfigurationChange`. | `SpeechRecognizer.swift:377-420`, `:493-545` |
| **Recognizer** | Apple `SFSpeechRecognizer(locale: speechLocale)`, `shouldReportPartialResults = true`, `taskHint = .dictation`. **`requiresOnDeviceRecognition` is never set**, so Apple may process audio on its servers. The README says the same ("may happen on-device or Apple may process microphone audio", README:66). | `:435`, `:461` |
| **Recognizer bias** | `contextualStrings` = up to 50 unique words of 5+ letters from the **unread** text, rebuilt on each task restart. | `:465-472`, `:697-705` |
| **The ~1-minute limit** | A timer restarts the task every **55 s** (`:786`). Error codes **1110 / 216** count as an expected timeout and restart at once with no limit. Other errors back off (0.5 to 1.5 s, max 10 tries). On restart, `matchStartOffset = recognizedCharCount`, so matching starts again from where you are. | `:581-600`, `:664-790` |
| **Alignment, strategy 1** | **Char-level** scan of normalised spoken text against the remaining source. On a mismatch it looks ahead up to **5 chars** in either string to resync. `[bracket cues]` are skipped. Returns the last *confirmed* match index. | `:876-967` |
| **Alignment, strategy 2** | **Word-level** scan. A word matches if it is exact or fuzzy: prefix match (3+ chars), a shared prefix of at least 60% of the shorter word, or edit distance ≤1 (≤4 chars), ≤2 (≤8 chars), ≤ len/3 beyond that. Words of 2 chars must match exactly. On a miss it skips up to **5 spoken words** (the STT added words) or **5 source words** (the speaker read fast or the STT dropped words). | `:975-1079`, `isFuzzyMatch :1081`, `editDistance :1100` |
| **Combine** | If the two results are within 20 chars, it averages them. Otherwise it takes the **further** one. | `SpeechTextAlignment.swift:86-95` |
| **Commit gate** | The position never moves backwards (`candidate > recognizedCharCount`). It commits if **both** strategies moved forward, if a cue was skipped, if the step is **15 chars or less**, or if **2 of the last 3** candidates agree within 10 chars. | `SpeechRecognizer.swift:829-866`, `SpeechTextAlignment.swift:97-117` |
| **Jumps / recovery** | A tap or manual jump sets `spokenAnchorPrefix = lastSpokenText`, so the old transcript is trimmed off, with 24 chars of slack for revisions. Results are ignored for **0.3 s** after a jump. A jump of **500+ chars** restarts the task so the bias words are refreshed. | `:174-189`, `:801-817` |
| **Scroll / highlight** | Word Tracking puts the active word at the **vertical centre**, or near the top (`readingPosition = .nearTop`). The timed modes anchor it near the bottom with smooth interpolation. | `MarqueeTextView.swift:384-410` |
| **Listening modes** | `wordTracking` (default) · `classic` (constant 0.5 to 8 words/s, no mic) · `silencePaused` = "Voice-Activated" (the timer runs only while the VAD says you are speaking). | `NotchSettings.swift:286-314`, `NotchOverlayController.swift:889-900` |
| **VAD** | RMS ≥ 0.04 switches it on at once. RMS ≥ 0.012 for 2 frames also switches it on. It stays on for 0.75 s after the voice stops. | `VoiceActivityDetector.swift:3-49` |

**What it does NOT handle (Inference from the code)**
- **Ad-libs.** It assumes **verbatim reading**. There is no re-anchoring search: it only scans forward from
  `matchStartOffset`, with a 5-word skip window. Speak 6+ words that are not in the script and nothing moves until you
  return to the text. Skip a paragraph and it stays stuck until you tap.
- **Latency.** It cannot be lower than Apple's partial-result cadence. Typically a few hundred ms (**UNVERIFIED**, not
  measured here).
- **Apple-only parts**: AVAudioEngine, SFSpeechRecognizer, CoreAudio device selection, the TCC prompts (Mic + Speech
  Recognition). **Portable**: all of `SpeechTextAlignment` plus the char/word matchers and the VAD. They are pure functions.
- **The cleanest copy to port is the iOS target**, `Textream/TextreamiOS/Speech/PromptMatcher.swift` (280 lines). It is the same
  algorithm as a pure `struct` with `match(transcript:) -> Int` and `jump(to:)`, and it comes with tests
  (`TextreamiOSTests/PromptCoreTests.swift:960` *matcherSkipsCueAndMovesForwardWithFuzzyTranscript*, `:972`
  *matcherNeverMovesBackward*).

## 2. Teletubby today (Observed)

- **No voice and no auto-scroll.** Movement is **discrete beat stepping**. `↓` / `Space` / `↑` call `stepNext` / `stepPrev`
  (`src/renderer/src/App.tsx:692-700`). "One key = one unit of the **driven zone**": paragraph, major topic or trigger
  (`src/renderer/src/store.ts:615-647`). It stays clamped inside the script.
- **Scroll** = `scrollIntoView({block:'start'})` on the live beat against a fixed **reading line** (26vh,
  `scroll-padding-top`), one frame late on purpose (`src/renderer/src/components/Zones.tsx:30-56`).
- **The only speed axis is none.** There is no wpm, no Elgato dial and no remote stepping. Elgato is a *separate* path:
  FliTools `prompter.load` writes Camera Hub's script files (`flitools/src/prompter/service.ts`). It does not drive Teletubby.
- **Where voice would plug in (Inference)**: the aligner is a pure function, so it lives in **`src/core`**. It sits beside
  `cadence.ts`, can be tested in vitest and is agent-callable. It is fed transcripts from **main** (a supervised child
  process, `src/main/process-supervisor.ts`). It emits "position" changes the renderer turns into `step`. Mic in the renderer
  (`getUserMedia`) would mean Electron needs `NSMicrophoneUsageDescription` in `electron-builder.yml` (absent today) and a
  permission handler (none today).
- **FliTools is not a live transcriber.** It is file-based and one-job-at-a-time, Groq (cloud) first then mlx_whisper, with
  a CrisperWhisper verbatim pass 2 (`flitools/src/capabilities.ts:34-40`, README:4-5). Streaming would be new work, and it
  would queue behind take transcription.

⚠️ **The model mismatch is the main finding.** Textream aligns against a **full verbatim script**. Teletubby's product is
**column 2, the trigger words**: talk *to* them, not read *from* them (North Star). With triggers driven, the talent is
improvising by design. A verbatim aligner will stall there, just as Textream stalls on ad-libs. Voice-follow fits Teletubby
cleanly only when **Paragraph (a transcript zone) is driven**. For trigger driving, the signal has to be *keyword
spotting*: "heard the next beat's trigger words, so advance". It cannot be character alignment.

## 3. Side by side

| Feature | Textream | Teletubby | Harvest verdict |
|---|---|---|---|
| **Voice follow** | 3 modes. Word Tracking via Apple Speech plus a dual fuzzy aligner (§1) | None. Ruled not-built without asking (`CLAUDE.md:284`) | **Port the code** (aligner + gate + jump anchoring, MIT) |
| **Word highlight** | Per character up to `recognizedCharCount`. Cues dimmed. Active word centred | Highlights the driven **beat**, not words | **Take the idea**: a within-beat progress tint, only if voice lands. Otherwise skip |
| **Voice-Activated (pause when silent)** | Timer runs only while the VAD is active (0.75 s hangover) | — | **Port the code** (VAD, 49 lines). Cheapest voice feature, no STT |
| **Speed control** | 0.5–8 words/s, mouse-scroll catch-up | None. Discrete steps by design | **Skip** (a constant scroll fights the beat model) |
| **Script load** | Editor, file drop, PPTX/Keynote presenter notes (`PresentationNotesExtractor.swift`), `textream://read?text=`, Director push | Agent control API 127.0.0.1:7111 (`script.write`, chapters → column-1 headings), fed by Story Pilot | **Take the idea**: presenter-notes import is a nice later door. Otherwise skip |
| **Formatting** | 4 fonts incl. OpenDyslexic, 4 sizes, highlight colours, `[cue]` annotations skipped by the aligner | 3-column zone model, text presets, trigger styles A/B/C | **Take the idea**: `[cue]` brackets skipped by the aligner, if scripts carry stage cues |
| **Mirroring** | H / V / both, per external display and per remote browser | `M` toggles mirror (`store.ts:819`) | **Skip** (Teletubby has it; axis choice is trivial if ever needed) |
| **Remote control** | Remote view :7373 and Director :7575, **all interfaces**, token leaked in the served page (X5) | Loopback only, session token, principals, OpenRPC | **Skip**. Teletubby's model is the right one |
| **Multi-screen / Elgato** | External display / Sidecar, display picker, notch follows the mouse | Lists displays (`src/main/index.ts:36`). Elgato via FliTools `prompter.load` | **Skip** |
| **Chapters / pages** | Multi-page with page advance. Director is single-page | Column-1 headings, paragraph/major/trigger units, end-card nudge | **Skip** (Teletubby's is richer) |
| **Notch / overlay UI** | Notch pill, floating glass window, fullscreen | Window/fullscreen with a camera-edge model, lens-aware strip | **Skip** (built for a laptop camera; David shoots on a 32" display) |
| **Hide from screen share** | `sharingType` toggle | — | **Take the idea** (one line in Electron: `setContentProtection(true)`) |
| **Learn from takes** | — | Cadence envelopes and scoring (`src/core/cadence.ts`) | n/a. Teletubby only |
| **Security model** | Unauthenticated in practice (X5: token in the page, unencrypted) | 127.0.0.1, token, asserted by a test | n/a. Teletubby wins |
| **Speech robustness** | 55 s preemptive restart, timeout codes 1110/216, mic-switch rebuild, `contextualStrings` bias | — | **Port the code** into whatever native helper we write |

## 4. Voice-following options for Teletubby

| | Option | Cost | Risk | Verdict |
|---|---|---|---|---|
| **(a)** | Port the aligner to TS (`src/core`). Feed it from **Apple Speech** through a small Swift helper (about 200 lines, reusing Textream's capture/restart code) that main spawns and that prints partial transcripts as JSON lines | Aligner ~1 day with tests ported. Helper ~1–2 days | TCC prompts belong to the helper or the parent app (signing, which binary asks). Set `requiresOnDeviceRecognition = true`, which Textream doesn't, to keep audio local. Mac-only (fine for this fleet) | **Recommended** |
| **(b)** | Same TS aligner, fed by **local streaming whisper** (mlx or whisper.cpp on 1–2 s windows) | New streaming path; FliTools has none | Higher latency (window-bound). Competes for the GPU with recording. Groq tier = cloud audio. Would contend with FliTools' one-job queue | Fallback, if Apple Speech is poor on David's accent or the vocabulary |
| **(c)** | Run Textream itself beside Teletubby | Zero build | Two prompters on one screen. No beat or trigger model. Director listens on all interfaces with a leaked token (X5). The mic hang in X5 is unexplained | **Skip** (fails the North Star test: more to look at) |

**Recommendation (not approved): (a), scoped to Paragraph driving first.**

**The smallest first slice, with no mic and no native code:** port `PromptMatcher` to `src/core/voice-follow.ts` (MIT
header + attribution) with Textream's two tests. Then build a **replay harness**: feed it a recorded take's FliTools
word-timed transcript, word by word at real timing, against the script it was read from. Print which beat the aligner
would have stepped to, and when, next to where David actually pressed `↓`. That proves or kills the idea on real takes
in an afternoon, before any permission prompts or helper binary. Slice 2 is the Swift helper. Slice 3 is trigger-word
spotting for the trigger zone.

## 5. Top 5 harvest items

1. **The dual aligner** (char + word fuzzy, 5-step look-ahead, `bestOffset`). Port from `TextreamiOS/Speech/PromptMatcher.swift`.
2. **The commit gate**: forward-only, 2-of-3 agreement, small steps and both-strategies-agree commit at once (`SpeechTextAlignment.swift:97`).
3. **Jump anchoring**: a manual `↑`/`↓` trims the old transcript and ignores results for 0.3 s, so voice and keys can coexist (`SpeechRecognizer.swift:174`, `:801`).
4. **Recognizer bias from upcoming text** (`contextualStrings`, 5+ letter words, max 50). For whisper the equivalent is `initial_prompt`.
5. **The VAD + "Voice-Activated" mode** (49 lines). A cheap no-STT first voice feature, plus the 55 s / error-1110 restart discipline for the helper.

*MIT obligation*: any copied file keeps `Copyright (c) 2026 Fatih Kadir Akin` and the MIT permission notice, and
Teletubby's `LICENSE`/README gains a third-party notice.
