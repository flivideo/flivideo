---
created: 2026-10-03
status: design — for David to read before the transcription panel is reworked
owner: flitools (design) · flistudio (the gear + panel, later)
brief: /Users/davidcruwys/dev/ad/brains/.appynet-briefs/brief-transcription-as-a-service.md
---

# Transcription as a service

**The idea:** send audio, get a transcript back. Pass 1 (Groq, mlx fallback) runs wherever the app runs. Pass 2 (CrisperWhisper, verbatim) is offloaded work done by **one named transcription server**: the M4 now, the M2 later. No app does transcription itself.

```
 any machine (M4, Roamy)                          the transcription server (M4 now → M2 later)
 ┌──────────────────────────┐   pass-2 job        ┌──────────────────────────────────────────┐
 │ app → local FliTools      │ ── audio + sha ──▶ │ FliTools: queue → memory gate → Crisper   │
 │   pass 1 now (Groq/mlx)   │ ◀── poll result ── │ only computes · callers poll for results  │
 │   writes files beside rec │                    │ queue.status · config.get/set             │
 └──────────────────────────┘                    └──────────────────────────────────────────┘
```

## Decisions (agreed by David)
1. **One global setting.** No brand/project levels, no Inherit. A second level only when a real case appears (e.g. a private client project that must stay local).
2. **Settings sit behind a gear, top-right of FliStudio's header**, on every screen. Transcription is its first section. The left menu stays project actions only.
3. **One named pass-2 server.** The M4 now, the M2 later. The M2 is a full peer like the M4 and Roamy (David, 2026-10-03), so no special restrictions apply to it.
4. **Roamy never runs pass 2.** It reads finished transcripts that sync as small files beside the recording.
5. **The same settings picture on every machine:** pass-1 engine · pass-2 server + engine (CrisperWhisper / ElevenLabs) · that server's queue (waiting, running, last finished).

## How a pass-2 job reaches the server, and how the result gets back
- **Rule: the machine that holds the recording writes its transcript files. The server only computes.** This one rule covers the M4 now and the M2 later.
- **Recording on the server's own disk** (today: FliHub records on the M4, which is the server). Pass 1 finishes, and the job is queued locally by path. The server writes the files beside the recording, and normal sync carries them to Roamy.
- **Recording elsewhere** (made on Roamy, or anything once the M2 is the server). After pass 1, the local FliTools **pushes** the job: 16 kHz mono FLAC (about 1 MB a minute) plus the sha256, through the existing upload door with `tier: edit`. The server keeps the audio in its own job store, transcribes it, and holds the result. The submitting machine **pulls** the result by polling the job, then writes the files beside its recording under the naming rule below. Nothing is ever lost. The server only ever answers calls; it never has to call a client back.
- **Identity is the sha256.** A second submit of the same content gets the existing job or the finished result. Nothing is transcribed twice.

## File names: the best in the plain name, every engine kept (David's ruling 2026-10-03)
For one recording, `hub/recordings/01-1-intro-HOOK.mov`:
```
hub/transcripts/01-1-intro-HOOK.json .srt .txt                  ← the BEST available; apps read only this
hub/transcripts/engines/01-1-intro-HOOK.groq.json .srt .txt     ← pass 1, as Groq wrote it
hub/transcripts/engines/01-1-intro-HOOK.crisper.json .srt .txt  ← pass 2, as CrisperWhisper wrote it
                 (later engines/01-1-intro-HOOK.elevenlabs.*; an mlx fallback run is engines/…mlx.*)
```
- **Best available** = the pass-2 transcript when its health is no worse than pass 1's (fewer or equal suspect reasons; a tie goes to the verbatim one), else pass 1. While pass 2 has not run, the best is pass 1. The plain `.json` records which pass and engine it is (`pass`, `engine.name`, `verbatim`) and lists the engine copies beside it.
- **Why a subfolder and not `01-1-intro-HOOK.groq.json` beside it** (checked 2026-10-03; the evidence is in the next bullet). A dotted name is misread. A subfolder is skipped by every reader checked, because each scan filters files by a `.txt` name or a filename regex, and a folder named `engines` matches none of them:
  - FliStudio `assets.list` skips folders (`files()` drops directories, flistudio/server/src/assets/assets.ts `files`), and so does `video.text` (lists only `*.txt`, flistudio/server/src/capabilities/video-text.ts:100).
  - fli-core still classifies the subfolder as the `transcripts` zone (fli-core/src/classify.ts:71-78).
  - FliCut never reads the folder; it calls FliTools.
- **The dotted form fails because** fli-core `parseRecording` allows periods in a slug (fli-core/src/recording.ts:12). So `01-1-intro.groq.txt` reads as a recording "intro.groq", and with a tag (`-HOOK.groq`) it does not parse at all. In FliTools' own folder scans, FliHub would:
  - triple every take in chapter combine, /combined and export (routes/transcriptions.ts:496, :531, :712; query/export.ts:159);
  - list engine copies as orphans that "Delete all orphaned" would remove (utils/scanning.ts:62-78, routes/projects.ts:264);
  - add phantom chapter entries (utils/chapterExtraction.ts:143).
  FliStudio `video.text` would add phantom takes.
- **One FliHub change either way:** Undo (`trashTranscriptsFor`, utils/transcriptFiles.ts:36), rename (`renameDerivableFiles`, utils/renameRecording.ts:92) and trash-recording (utils/recordingArtifacts.ts:28) move exact `<base>.{json,srt,txt,vtt,tsv}` only. They must also carry `engines/<base>.*`, or the copies stay behind under a freed name.
- **Existing transcripts are not touched or swept.** Each one is the plain name already. The first time FliTools writes for that recording (a re-run or a pass-2 upgrade), it first copies the current plain files to `engines/<base>.<its engine>.*`, using the `engine.name` inside it. FliHub's old whisper output, which has no engine field, becomes `engines/<base>.mlx-flihub.*`. Then it writes the new best. Nothing is deleted.

## How a client on Roamy sees the queue
- Each machine knows one local thing: **the server's address** (e.g. `mac-mini-m4` / `100.82.235.39:7161`), in `~/.config/appydave/flitools.json`.
- Everything else is asked of the server over Tailscale: `queue.status` (waiting / running / last finished / `waitingFor`), and `config.get` / `config.set` (the one global setting lives **on the server**, so every machine shows the same picture). Each machine caches the last answer, so pass 1 still knows its engine while the server is off.
- The server serves the tailnet (`FLITOOLS_HOST=0.0.0.0`). Reading is open on the tailnet; changing settings or submitting needs the server's bearer token.

## When the server is down, or held for memory
- **Pass 1 is unaffected**: it runs locally. Transcripts stay pass 1 (`verbatim: false`; FliCut shows "timings approximate").
- **Server unreachable**: the submitting machine keeps the job in its own on-disk **outbox** (today's queue format) and resubmits when the server answers. Nothing is lost, and nothing falls back to running pass 2 locally, Roamy least of all.
- **Held for memory**: the job waits on the server under today's memory rules. The gear screen shows `waitingFor` (e.g. "4.4 GB available, needs 14").

## What stays from today's build, and what changes
| Stays (built, live in FliTools main 41310c3) | Changes |
|---|---|
| Providers: groq-whisper, mlx-whisper, crisperwhisper, elevenlabs (off) | Settings: three levels → **one global**, stored on the server; the brand/project reads go |
| Two passes; `flitools.transcript/2`; energy-refined ends; health rules | Pass 2 goes to **the named server**, not to whichever FliTools took the call. Pass 2 no longer *replaces* pass 1: the best goes in the plain name, each engine's output in `engines/` |
| On-disk pass-2 queue with claim/lease/complete | The same format doubles as each client's **outbox** |
| Memory rules: one CrisperWhisper per machine, memory check before each job, unload when empty | A machine role: `server` (runs pass 2) or `client` (pass 1 only; Roamy) |
| `config.get/set`, `queue.status` | Called **across the tailnet** by the FliStudio gear screen, not only locally |
| Upload door (`/api/transcribe/upload`) | Gains pass-2 submit (`tier: edit`); the client writes the files it gets back |

## Not covered, not decided
- **The M2's RAM is unverified.** SSH timed out, and AppyRadar's last data for it is from 2026-09-03 (offline). CrisperWhisper needs about 13 GB, so a 16 GB M2 is marginal and an 8 GB one cannot run it. **Check before naming it the server.**
- The gear screen's visual design (FliStudio's job; it waits on David).
- How the token reaches each machine, and whether reading the queue should need it at all.
- Backfill: whether existing pass-1 transcripts are queued for pass 2, or only new recordings.
- ElevenLabs budget/key, and languages other than en/de (no local verbatim engine).
- What happens if two machines hold copies of the same recording and both write the transcript. Today: the last writer wins, since both write the same content.
- FliCut's use of the words (alignment plan phase 2) and the "timings approximate" badge.
