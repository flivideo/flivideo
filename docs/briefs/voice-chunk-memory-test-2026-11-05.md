---
created: 2026-11-05
timestamp: 2026-11-05T16:20+07:00
---
# Brief: voice chunk and memory test, M2 worker (David's go, 2026-11-05)

**Purpose**: Find out whether smart-paragraph chunks keep local voice generation safe on the M2's 32 GB, and how steady the pace is. **Folder**: `~/dev/labs/voice-poc/`. **Model**: `mlx-community/VoxCPM2-8bit`, mlx-audio 0.6.4, 7 steps, cfg 2.0 (as takes A to D).

## Stage 1: repeat runs (one short script, the 202-word narration)
Same voice sample and text each time. Five runs: three with no seed, two with the same `mx.random.seed` set before `generate`. Measure words per second, pause pattern and whether the two seeded files match byte for byte. Answers how much pace moves by chance, and whether A vs B can be read as the voice sample at all.

## Stage 2: D13 at a 300-word limit
- Break only at paragraph ends, never mid-paragraph. Script: `~/dev/video-projects/v-appydave/d13-overlay-pilot/script/storypilot/project/script.md`.
- Before and after each chunk log: MLX peak GB, memory in use, swap used, generation seconds, audio seconds, words per second. Also poll memory every 5 s between and during chunks.
- Between chunks: delete the chunk's arrays and call `mx.clear_cache()`, then log what comes back. **If memory doesn't drop back, say plainly that splitting failed to protect the M2.**
- Stop rule: don't start a chunk unless memory and swap pass a check. Stop if swap grows hard.
- A failed chunk is redone alone; finished chunks stay on disk as files, so a restart loses nothing.
- Join with a 50 ms crossfade and no inserted silence. Report where each join falls, so David can listen for it.

## Reused from FliTools, not invented
| Pattern | Where | Use here |
|---|---|---|
| Split to a measured cap with a safety margin | `src/transcribe/audio.ts:100-108` (`GROQ_MAX_BYTES`, 0.8 margin) | Word limit set from measured GB per word, with a margin |
| One heavy job at a time, memory checked before each, model unloaded when done | `src/transcribe/crisper.ts:14-17`, `src/transcribe/service.ts:1008,1048,1064` | Same rules per chunk |
| Durable job state, attempts counted | `src/transcribe/editQueue.ts` | Per-chunk record on disk (JSON files in this test, no queue built) |
| Keep a retry only when it's better, record attempts | `src/transcribe/service.ts:658-671` | Retried chunk records its attempts |
Not reused: the Scribe, Groq, mlx order, which `docs/architecture.md:191` marks superseded by two passes (`src/transcribe/providers.ts:8-16`). Those are engine fallbacks; this has one engine. CrisperWhisper (pass 2, local verbatim words) can supply the word timings for pace, one job at a time, after generation and never alongside it.

## Out of scope
Building a tool, FliTools changes, D13 publishing, any paid call.

## Worker instructions
- **Read first**: `REPORT.md`, `gen2.py` and `measure2.py` in this folder. Extend with a new script, `gen3.py`; keep the same model and settings. Read the generate code at the pinned version before writing it.
- **Voice sample**: the new sample, `work2/ref2.wav` + `work2/ref2.txt` (take C, the one David said sounded like him). Own recordings only; no other voice.
- **D13 script**: copy `script.md` read-only from the M4 (`davidcruwys@100.82.235.39`) into `work3/`. It has 26 paragraphs, 1,049 words; a 300-word limit should give chunks of 262, 262, 296 and 229. Don't edit the text.
- **Order**: Stage 1, then Stage 2. Check swap and memory before each stage.
- **Stop rule**: before each chunk, require at least 18 GB free and no swap growth since the start of the run. Stop and report if swap grows by more than 2 GB at any point, or the machine is struggling. Don't lower the limit or retry in a loop to get through. A failed chunk gets one redo; a second failure stops the run.
- **If memory doesn't drop back in one process**, finish the chunk in progress, report it plainly, then run the remaining chunks in a fresh process each and measure that as a second way of protecting the M2.
- **Pace**: word timings for each chunk, using the same local whisper method as `measure2.py`, after generation and never alongside it. Report words per second per chunk and how far apart they are, compared with Stage 1's spread by chance.
- **Join checks**: confirm no digital silence at any join, and list each join's time in the full file.

## Deliverables
- `work3/chunks/` per-chunk audio and a JSON record for each (attempts, measurements). `work3/memory.jsonl` for the 5 s poll.
- `page3/index.html` with relative-path audio: full D13 at the top, the narration chunk boundaries and join times beside it, then the table per chunk (words, peak GB, memory in use before and after, swap, generation seconds, audio seconds, words per second), the memory-over-time chart as inline SVG, Stage 1's results and a seed answer. Light-only AppyDave page (cream `#faf5ec`, white cards, `#342d2d` text, Oswald + Roboto, `color-scheme: light`, no `prefers-color-scheme`).
- A section in `REPORT.md`, with a plain answer to each: did memory drop back; is chunking safe at 300 words; total time; what can't be concluded. Commit text and page locally, and keep `.wav` files out of git.

## Rules
David's voice stays on this machine: no remote, no upload, no hosted call, telemetry off. No ElevenLabs or paid calls. Stay in this folder apart from the read-only copy, nothing global, no `sudo`, no servers (orch serves the page). One generation at a time. Don't touch any FliVideo app. Use `command grep`.

End with exactly one line: `APPYNET: done — <one line>`, `APPYNET: blocked — <why>` or `APPYNET: question — <a real decision>`. Never for status.
