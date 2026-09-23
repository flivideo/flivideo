<!-- FliVideo source bundle · FliTools state · written 2026-09-23 from the flitools session -->

# FliTools — state on 2026-09-23

**What it is**: the shared-tools service for the FliVideo suite, starting with transcription. One
always-on service that every app, skill and agent calls, instead of each app transcribing on its own.

**State**: design half-ruled. **No code and no endpoint exist yet.**

## Ruled (David)
1. The service always **returns word-timed JSON**. By default it also saves `json` / `srt` / `txt` into a
   `transcripts/` folder beside the recording. The caller can pass `save_to`, or `save:false`.
2. It **reuses** an existing transcript of the same content, so each recording is transcribed once.
3. **Engine**: Groq first, local mlx-whisper as the fallback. Jobs run one at a time, queued.
4. **Two levels of transcript**: the raw one (the canonical recording, owned by FliTools) sits beside the
   recording. The edited one (the cut, with ums and bad takes removed) is derived by FliCut from the raw
   words and lives with the edit.

## Open
- **Gateway**: do apps and skills call FliTools over HTTP directly (with fli-core carrying only a thin
  typed client and "where is this recording's transcript"), or go through fli-core?
- Where the code lives, whether it builds on the AppySentinel boilerplate or starts fresh.
- A slot for a Claude Agent SDK chat (talk to a project's transcripts, e.g. "write me an intro"), shown
  as one reusable chat component in every app.

## Transcription today vs planned
- **Today**: FliHub transcribes a take when it is promoted (no word timings). FliCut re-transcribes every
  clip itself with word timings when an edit opens. FliCast transcribes only on "Generate captions".
  None of them reuses the others' work.
- **Planned**: every app asks FliTools; the raw word-timed transcript is made once beside the recording;
  FliCut builds its cut from it.
