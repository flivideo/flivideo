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
 │   pass 1 now (Groq/mlx)   │ ◀── poll result ── │ never reaches out · holds no keys         │
 │   writes files beside rec │                    │ queue.status · config.get/set             │
 └──────────────────────────┘                    └──────────────────────────────────────────┘
```

## Decisions (agreed by David)
1. **One global setting.** No brand/project levels, no Inherit. A second level only when a real case appears (e.g. a private client project that must stay local).
2. **Settings sit behind a gear, top-right of FliStudio's header**, on every screen. Transcription is its first section. The left menu stays project actions only.
3. **One named pass-2 server.** The M2 rules apply when it takes over: it may be reached, never reaches out, holds no keys.
4. **Roamy never runs pass 2.** It reads finished transcripts that sync as small files beside the recording.
5. **The same settings picture on every machine:** pass-1 engine · pass-2 server + engine (CrisperWhisper / ElevenLabs) · that server's queue (waiting, running, last finished).

## How a pass-2 job reaches the server, and how the result gets back
- **Rule: the machine that holds the recording writes its transcript files. The server only computes.** This one rule covers the M4 now and the M2 later.
- **Recording on the server's own disk** (today: FliHub records on the M4, which is the server). Pass 1 finishes, and the job is queued locally by path. The server writes the files beside the recording, and normal sync carries them to Roamy. This is how it already works.
- **Recording elsewhere** (made on Roamy, or anything once the M2 is the server). After pass 1, the local FliTools **pushes** the job: 16 kHz mono FLAC (about 1 MB a minute) plus the sha256, through the existing upload door with `tier: edit`. The server keeps the audio in its own job store, transcribes it, and holds the result. The submitting machine **pulls** the result by polling the job, then writes `X.json/srt/txt` beside its recording, replacing pass 1 in place. The M2 is only ever called; it never calls out.
- **Identity is the sha256.** A second submit of the same content gets the existing job or the finished result. Nothing is transcribed twice.

## How a client on Roamy sees the queue
- Each machine knows one local thing: **the server's address** (e.g. `mac-mini-m4` / `100.82.235.39:7161`), in `~/.config/appydave/flitools.json`.
- Everything else is asked of the server over Tailscale: `queue.status` (waiting / running / last finished / `waitingFor`), and `config.get` / `config.set` (the one global setting lives **on the server**, so every machine shows the same picture). Each machine caches the last answer, so pass 1 still knows its engine while the server is off.
- The server serves the tailnet (`FLITOOLS_HOST=0.0.0.0`). Reading is open on the tailnet; changing settings or submitting needs the server's bearer token. That token is inbound-only, so it is not a key that reaches out.

## When the server is down, or held for memory
- **Pass 1 is unaffected**: it runs locally. Transcripts stay pass 1 (`verbatim: false`; FliCut shows "timings approximate").
- **Server unreachable**: the submitting machine keeps the job in its own on-disk **outbox** (today's queue format) and resubmits when the server answers. Nothing is lost, and nothing falls back to running pass 2 locally, Roamy least of all.
- **Held for memory**: the job waits on the server under today's memory rules. The gear screen shows `waitingFor` (e.g. "4.4 GB available, needs 14").

## What stays from today's build, and what changes
| Stays (built, live in FliTools main 41310c3) | Changes |
|---|---|
| Providers: groq-whisper, mlx-whisper, crisperwhisper, elevenlabs (off) | Settings: three levels → **one global**, stored on the server; the brand/project reads go |
| Two passes; `flitools.transcript/2`; energy-refined ends; health rules | Pass 2 goes to **the named server**, not to whichever FliTools took the call |
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
