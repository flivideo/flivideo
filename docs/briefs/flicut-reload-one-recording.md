# Ticket — FliCut: "Reload this recording's transcript"

**Status**: TICKET, not built. Written 2026-10-12 by the D10 transcript-repair session. Too big to build safely the
same day: it touches the timeline layer (ADR-0002 clips, ADR-0007 exact edges, ADR-0012 wings) and the
corrections/overrides keys inside a live edit.

## Why

D10 `03-6-flicut` and `03-7-flicut` were transcribed by CrisperWhisper with the 40–50 s chunk overlap written twice.
FliTools now drops that duplicate (`dropRewoundWords`, flitools c63b2c0) and both transcripts were redone clean
(hub/transcripts, pass 2, 0 words back in time). **The FliCut edit still holds the old words and the inverted takes**
(`take_mv4wwnrh_o3_6wbi` 03-6, `take_mv4wwny0_qa_s8ij` 03-7). FliCut now shows a warning on both recordings
(flicut 1b59bec). It has no way to pick up the new transcript.

## What exists today (verified 2026-10-12)

- FliCut never reads `hub/transcripts/<name>.json`. It asks FliTools (`transcribeViaFlitools`,
  `src/main/transcriber.ts:141`). FliTools answers from its sha256 cache, which now holds the clean pass 2.
- It builds takes once, at transcription (`segmentTakes`, `src/main/transcriber.ts:161`). Take ids are random
  (`src/shared/transcript.ts:152`).
- Both entry points skip a media that already has a transcript:
  - IPC `transcribeStart`: `src/main/index.ts:540`
  - RPC `edit.transcribe`: `src/main/pipeline.ts:110`
- There is no reload, re-transcribe, rebuild-takes or remove-media verb (RPC list `api/openrpc.json`).
- Cut decisions have three keys:
  - `timeline.clipsWithCuts`: `mediaId` + `takeIndex` + source `start`/`end`, plus `cutBy`, `exactStart/End` and `wing`.
  - `corrections`: `<takeId>#<elementIndex>` (`src/shared/project.ts:174`).
  - `heardOverrides`: the same key.

## What to build

One verb, exposed as an RPC method and as a button on the recording header in Script (`Script.tsx`, beside the
transcript warning):
`edit.reloadTranscript { edit, mediaId }`

1. Ask FliTools for the recording's current best transcript (the cache, or a forced run when the caller asks).
2. Rebuild that one media's `takes` and `transcript` the same way `transcribeMedia` does.
3. Re-project that media's clips from the new takes.
   - Keep every **user** decision (`cutBy: 'user'`, exact edges, wings) whose source-time span still lies on words
     with matching times (±50 ms).
   - Report the decisions that could not be kept. Never drop them silently.
   - Proposals are recomputed.
4. Re-key `corrections` and `heardOverrides` for that media by the word's source time, not its take index. Drop and
   report any key whose word is gone.
5. Before writing anything, snapshot the edit into `history/`, as every edit write already does.
6. Never touch any other media, and never touch `fli.edit.*`.

## Done when

- A test on a trimmed D10 03-6 fixture (old duplicated takes → new clean transcript) leaves:
  - no word back in time
  - no inverted take
  - every user cut on 30–41 s and 50–74 s kept, unchanged
  - the other medias' clips byte-identical
- Run on the real D10 cut (after copying `fli.cut.ai-powered-video-cuts.json` and `fli.cut.ai-powered-video-cuts/` to
  `-trash/<date>-before-reload/`):
  - only 03-6 and 03-7 change (prove it with a diff of the other medias' clips, corrections and overrides)
  - the warning on both clears
- The runbook `docs/runbooks/transcript-looks-wrong.md` step 4 is updated from "not possible yet" to the button.

## Interim (until built)

There is no supported reload. The only routes are:

- **A new cut.** It picks up the clean transcripts, but loses every decision.
- **Hand-editing the edit file.** Clear the media's `transcript` and `takes`, then run `edit.transcribe`. This is
  unsupported: the clips for that media would point at take indexes that no longer exist.

Neither route is recommended. David decides.
