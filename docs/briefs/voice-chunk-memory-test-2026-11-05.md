---
created: 2026-11-05
timestamp: 2026-11-05T16:20+07:00
---
# Plan: voice chunk and memory test, M2 (NOT STARTED, waiting for David's go)

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
