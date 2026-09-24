<!-- FliVideo source bundle · FliTools state · hand-written 2026-09-24 from flitools git log, /health, docs/architecture.md and api/openrpc.json -->

# FliTools — current state (2026-09-24)

FliTools is the suite's shared local service. Its first capability is transcription. **It is built and
running** (the earlier "design only, no code" note is out of date).

## What exists
- **v0.1.0**, Node + TypeScript on the fli-core agent layer. Runs on **127.0.0.1:7161** under launchd
  (`com.appydave.flitools`, RunAtLoad + KeepAlive; logs in `~/Library/Logs/flitools/`).
- Repo: **github.com/flivideo/flitools** (private).
- **JSON-RPC** at `POST /api/rpc`: `transcribe.run`, `transcribe.find`, `transcribe.job`, `transcribe.jobs`,
  `system.status`, `system.quit`, `system.restart`. REST shortcuts: `POST /api/transcribe`,
  `POST /api/transcribe/upload`, `GET /api/transcript?path=`, `GET /api/jobs`. Console at `/docs`, spec at
  `/api/openrpc.json`.
- **Engines**: Groq `whisper-large-v3` first (word + segment timings); on any Groq failure it falls back
  to local `mlx_whisper` large-v3. One job at a time.
- **Output** `flitools.transcript/1`: word-timed JSON plus `.srt` and `.txt`, saved beside the recording
  (`hub/recordings/X` → `hub/transcripts/X.*`; anything else → `transcripts/` beside it).
- **Reuse**: the same content (by sha256) is never transcribed twice.
- **Queue** is agent-queryable and scoped by **project code** (e.g. `d04`, stable across renames) **and**
  requesting app (`x-fli-principal: agent:<app>`). No cross-app coalescing.
- **Overwrite guard**: it never writes over another app's transcript files unless the caller passes
  `save_to` or `force_save`.
- **Default vocabulary**: FliVideo, FliHub, FliCast, FliCut, FliStudio, FliTools, fli-core, Teletubby,
  AppyDave, AITLDR, Ecamm, Pocket 4 (a caller's list is appended).

## Who calls it
- **FliStudio** `footage.import`: copies clips into `footage/` and queues each one (via fli-core's
  FliTools client, v0.8.0+).
- **FliCast** export: a spoken cast export is auto-submitted.
- **Not migrated yet**: FliHub (still transcribes on its own, no word timings) and FliCut (its own
  mlx-whisper on edit open). In the d04 run every file was transcribed twice because of this.

## Known limits
- The queue lives in memory; a restart forgets job history (transcripts and the cache stay).
- No memory guard beyond one job at a time (a long mlx fallback can use ~17 GiB).
- Vocabulary is per call; merging FliHub's dictionary with FliCut's is still open.

## Designed but not built
- **Agent SDK chat** (`chat.open/send/close` per video project, over its transcripts) — a design slot only.

## Candidate next capabilities (for discussion, not decided)
- **Overlay render endpoint** (from the FilmStudio study): `overlay.create`, `overlay.render` (task:
  HyperFrames → alpha layer, content-hash cache), `overlay.frames` (PNG checks). Review and placement
  would live in FliEdit (or FliCut until FliEdit exists).
- **Brand glossary** as the Whisper prompt, shared by every app.
- **FliHub and FliCut transcription migration** onto FliTools (one transcript per file, word-timed).
- Transcription hardening seen in FilmStudio: chunking, timestamp validation, script alignment, media
  normalise/probe, transcript search.

## Open proposal — not decided
**FliGate** (one MCP door for the whole suite, generated from each app's OpenRPC) is an **open proposal**.
It is to be weighed against a **shared fli-core adapter** and **MCP delivered as a plugin** (and any other
option found), in a written pros-and-cons proposal decided with David. It is not settled.
