# Local voice POC — report (2026-11-05, M2 Pro 32 GB)

**Recommendation: MONITOR.** It works, licences cleanly and runs headless, but nobody has judged the sound. David's ear decides; quality is not claimed here.

⚠ `page/take-2.mp3` is a **clone of David's voice** (from a 10.8 s clip of his d10 FliCut recording). It stays local and is not committed to any remote from this folder. `page/take-1.mp3` is **Alex's ElevenLabs voice** (AITLDR file, the channel's brand voice).

Detail on sources, licences and corrections: `FEASIBILITY.md` (committed before any install).

## What was tested
- Engine: **VoxCPM2 8-bit** via **mlx-audio 0.6.4** (MIT), weights `mlx-community/VoxCPM2-8bit` (Apache-2.0). No platform install; venv in this folder, pinned in `requirements.lock.txt`. HF telemetry disabled; grep of the TTS code path found no telemetry; only network use was the weight download.
- Script: 17 lines, ~200 words, ~65 s. **It is the whisper transcript of the baseline mp3** (`b05-title-lab/voice/voiceover-alex.mp3`, with "Cloud" fixed to "Claude"), so it may differ slightly from the text actually sent to ElevenLabs.
- Baseline: that existing ElevenLabs file, **Alex's voice**, so the comparison is across different voices. A built-in voice take was added as a control. No ElevenLabs call or key used.
- Timings: FliTools `/api/transcribe` with `engine: mlx` (local; the default would try Groq/Scribe, which I avoided for voice data).
- Not every AITLDR wav is ElevenLabs: `short-vo.wav` / `day4-*.wav` come from local **OmniVoice** (`generate_day4.py`). See flag below.

## Measurements
| | Clone (David) | Built-in | Baseline (ElevenLabs, Alex) |
|---|---|---|---|
| Audio length | 68.6 s | 72.0 s | 65.2 s |
| Generate time | 96.8 s | 67.3 s | n/a |
| Speed vs real time | 0.71x | 1.07x | n/a |
| Model load | 131.9 s (includes 3 GB download) | 2.4 s | n/a |
| Peak memory (MLX / process) | 6.45 / 4.94 GB | 6.26 / 3.45 GB | n/a |
| Disk | models 3.0 GB, venv 0.47 GB | | |
| Clipping / peak | 0% / 0.63 | 0% / 0.99 | 0% / 0.58 |
| Longest silence | 0.75 s | 0.70 s | 1.05 s |
| Word error vs script (local whisper) | 1.0% | 2.0% | 0.5% (circular: script came from it) |
| Line start error vs known bounds, median / p90 | 200 / 269 ms | 241 / 350 ms | no ground truth |
| Line end error, median / p90 | 480 / 613 ms | 361 / 490 ms | no ground truth |
The first run's slower speed includes a cold start, so 0.7x to 1.1x is the honest range. Swap in use was 2.4 GB of 3 GB before and after (shared with other services on this host); free memory stayed at 87%, no hard swapping. Only one generation ran at a time; nothing was left running.
Timing "ground truth" = the known position of each generated line in the file. The end error includes trailing silence the model leaves after a line, so it overstates alignment error. For ElevenLabs there is no native timing on disk (its files carry whisper-derived transcripts too), so no like-for-like timing comparison exists.

## Findings
- **Apple Silicon:** yes, MLX route, no NVIDIA. 8-bit is ~real time on M2 Pro. Good for batch voice-overs, not live.
- **Word timing:** not native; a separate local whisper pass gave usable words (1 to 2% word error), same mechanism the pipeline uses now.
- **Automation:** headless CLI, Python and OpenAI-style server (`/v1/audio/speech`); no MCP.
- **Licence on published videos:** VoxCPM2 (Apache-2.0) and mlx-audio (MIT): allowed commercially; the card forbids impersonation and asks that AI content be labelled. VoiceStudio the app is AGPL-3.0 and not needed. **OmniVoice weights are CC-BY-NC: not allowed commercially.**
- **Flag for David:** AITLDR's local wavs use OmniVoice (non-commercial weights). If those go into published videos, that licence question is separate from this POC and is his call.
- **Alternatives:** Kokoro (presets only, already in Story Pilot Listen), Chatterbox, Qwen3-TTS, Higgs v3 exist in mlx-audio; I did not benchmark or licence-check them. Nothing found that beats VoxCPM2 on evidence gathered, but absence of a test is not absence of a better one.

## Provider interface (proposal only; nothing built)
```
synthesize(request) -> result
request: { text | lines[{id,text}], voice: {kind: "preset"|"clone"|"design", id|ref_audio+ref_text|description},
           format: "wav"|"mp3", sample_rate?, seed?, language? }
result:  { audio_path, duration_s, sample_rate, lines[{id,start_s,end_s}],
           words[{text,start_s,end_s}] | null, words_source: "native"|"aligned"|"none",
           metadata: {provider, model, voice_id, version, gen_seconds, cost?}, warnings[] }
errors:  voice_not_found | text_rejected | rate_limited | provider_unavailable | timeout | licence_blocked (typed, retryable flag)
```
ElevenLabs implements it natively; local VoxCPM2 returns `words_source: "aligned"` via FliTools. Per-line generation gives exact line bounds for free.

## Not established
- How it sounds (David's ear), including whether the clone is acceptable.
- bf16/4-bit variants, longer scripts, other engines, quality of the clone vs reference.
- Whether VoiceStudio can host VoxCPM2 (its README doesn't list it).
- Licences of Kokoro/Chatterbox/Qwen3-TTS/Higgs; VoiceStudio Pro/Cloud terms.
- ElevenLabs native timing accuracy. Whether the OmniVoice wavs are published.
- Reproducibility across seeds; one run per variant only.

## Cleanup / reversibility
Delete `~/dev/labs/voice-poc/` (venv 0.47 GB, models 3.0 GB). Nothing global, no sudo, no brew. Audio samples are gitignored (`*.wav`, `work/`); only `page/*.mp3` is tracked locally; no remote.
