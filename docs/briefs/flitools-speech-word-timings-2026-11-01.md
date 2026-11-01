---
created: 2026-11-01
timestamp: 2026-11-01T20:25+07:00
---
# Brief: FliTools — word timings for speech.synthesize (2026-11-01)

**From:** `flivideo-orch`. **To:** `flitools-dev` (tmux `flitools-dev`). **Report to `flivideo-orch` by name, then idle until acked.**
**Worktree:** `/Users/davidcruwys/dev/ad/flivideo/flitools-worktrees/tts-verb`; new branch `speech-words` from flitools main `06ed67e`.

## Why (David, verbatim, 2026-11-01 ~20:20)
"When we're playing a video, you can see yellow highlights of the word that we're on. You can also play it at any speed:
2x, 3x, whatever. The same sort of patterns we see should exist."

Story Pilot's Listen needs a word-by-word highlight, so each synthesized paragraph needs word start/end times.

## Build
1. `speech.synthesize` also returns (and writes beside the mp3, e.g. `<file>.words.json`) `words: [{ text, start, end }]` in seconds.
   Same shape as FliTools' transcription word timings if those exist, so FliStudio can reuse one highlighter. Name the shape.
2. Source of timings, in order of preference:
   a. Kokoro's own token timestamps (KPipeline results carry start/end per token in recent versions; check 0.9.4).
   b. Fallback: run FliTools' own transcription with word timestamps over the generated audio and align to the input text.
   State which you used and how accurate it looks on one paragraph (spot-check 3 words).
3. Idempotent cache stays: an existing mp3 without a words file gets timings computed without re-synthesizing.
4. Shared-contract rule: if `@flivideo/core` (fli-core) needs a change, flag it to orch first.

## Gates
typecheck + tests green; a test that asserts words are monotonic and cover the text (skip cleanly without Kokoro).
Commit, push `speech-words`. Do not merge. Do not restart :7161; orch gates, merges and restarts via `my-app restart flitools`.
Report: commit, gate tails, the result contract, timing source, accuracy spot-check.
