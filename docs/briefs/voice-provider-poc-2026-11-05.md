---
created: 2026-11-05
timestamp: 2026-11-05T11:20+07:00
---
# Brief — Local voice alternative to ElevenLabs: research + smallest test (M2 worker)

**Purpose**: Find out whether a local, self-hosted voice stack (VoiceStudio with VoxCPM first) could replace or supplement ElevenLabs. Proof of concept, not a migration. **Owner**: flivideo-orch (M4), managing only. **Machine**: M2 (David, 2026-11-05: a model download is expected; M2 Pro, 32 GB, 103 GB free). **David's go**: 2026-11-05, "pull together and execute".

## Start by checking these, because the spec may be wrong
- The spec calls the project **FliTalent / Project Synthespian**. Neither name is in `locations.json` or `apps.json`, or a folder on the M4 or M2 (searched 4 levels under `~/dev`). Look further (repos, docs, `~/dev/ad/brains/elevenlabs/`). Don't invent it. If it doesn't exist, say so and use the real ElevenLabs users instead: AITLDR voice-overs (`/Users/davidcruwys/dev/video-projects/v-aitldr/b*/voice/`, including `*.manifest.json` and `voiceover-alex.mp3`, read-only on the M4 over SSH at `davidcruwys@100.82.235.39`) and FliStudio's Story Pilot Listen.
- Yesterday's page said **OmniVoice Studio** with OmniVoice weights is non-commercial. The spec names **VoiceStudio** with a weak default OmniVoice engine, citing https://www.mindstudio.ai/blog/voicestudio-vs-elevenlabs (a vendor-adjacent blog). Establish from the primary repos whether these are the same project, what it's really called, and its current state.
- The spec's "AGPL-3.0" and "VoxCPM" claims come from that source chain. Verify against the actual LICENSE files and model cards.
- Spec text below is David's ChatGPT draft, so treat its facts as leads. Its "NVIDIA CUDA" means CUDA.

## Phase 1: feasibility, from primary sources (no install)
Answer with citations:
- **Apple Silicon**: does VoxCPM run on an M2 Pro or M4 without NVIDIA? MPS, MLX or CPU? Memory, speed, install effort, model size.
- **Word-level timing**: native in the API, or a separate alignment? What accuracy can we expect?
- **Automation**: local API or MCP; can cloning and generation run headless?
- **Licence**: app and each model, for commercial use. Say plainly what would and wouldn't be allowed on published videos.
- **Alternatives**: the current strongest local options on Apple Silicon (for example Kokoro, which Story Pilot Listen already uses, and any MLX-native voice-cloning model). Check for a better candidate than VoxCPM; don't assume.

Write this to `~/dev/labs/voice-poc/FEASIBILITY.md` and commit before installing anything.

## Phase 2: the smallest practical test
Carry on without asking if Phase 1 says a candidate can run on this Mac. David expects a model download. Don't install the full platform if the model can run on its own; pick the smallest route and say why.
- One script of about 60 seconds, from an existing voice-over. **Baseline: existing ElevenLabs audio on disk.** Generate no new ElevenLabs audio, because that costs credits.
- **Voice sample: David's voice only**, from his own recordings. Do not clone Alex or anyone else. If the ElevenLabs baseline is Alex's voice, say that the comparison is across different voices and also generate a built-in voice.
- Generate the same script with the candidate. Record time, realtime factor, peak memory and disk.
- Word timings: get them natively or through FliTools' transcription (`~/dev/ad/flivideo/flitools`; do not hand-roll a transcription loop or call Groq directly). Compare against the baseline's timing data where it exists, with a measured figure.
- Check the audio is intact by measurement (duration, clipping, silence). **You can't judge how it sounds; David's ear decides.** Don't claim quality.

## Rules
- **Folder**: `~/dev/labs/voice-poc/`, new, own `git init`, no remote. Python venv or similar inside it; nothing global, no Homebrew installs. Disk limit: stop and report if models and environment pass 30 GB.
- **Never touch**: ElevenLabs integration, any FliVideo app or live checkout, the running FliTools config, `~/dev/rig-work`, D18 or D19. No production dependency. Don't refactor anything; the provider interface is a written proposal only.
- **No paid calls, no new API keys, no secrets printed or committed.** Don't use an ElevenLabs key.
- **Voice data**: nothing of David's voice leaves this machine. Don't commit voice samples or a clone to any remote, and turn off telemetry where the tool offers it. Check each tool for hosted calls and anything sent to third parties.
- **Third-party code** is untrusted: read the install steps before running them, use pinned versions, and don't run `curl | sh`. If a step needs `sudo`, stop and report.
- **Load**: one generation at a time. Stop any server you start. Stop and report if the machine is swapping hard.
- Use `command grep` (bare grep is shimmed).

## Deliverables, in the folder
- `REPORT.md`, also copied to `~/dev/ad/flivideo/docs/research/voice-provider-poc-2026-11-05.md` and pushed: feasibility, Apple Silicon, word timing, API approach, licensing, measurements, a one-page provider-interface proposal (script input, voice selection, audio, word timings, metadata, errors), not established, and **one final recommendation: Proceed, Monitor or Reject.**
- `page/index.html`: a light-only AppyDave page for David (cream `#faf5ec` page, white cards, `#342d2d` text, Oswald + Roboto, no dark theme, no `prefers-color-scheme`). A/B audio players at the top, unlabelled until he reveals which is which, then the scorecard against the spec's six criteria: voice quality (David's ear), word timings, hardware, API, licensing, integration. Copy audio into `page/` with relative paths; under 45 MB. Orch publishes it, so note anything in it that you consider sensitive. If it holds a clone of David's voice, say so at the top of your report.

End your final reply with exactly one line: `APPYNET: done — <one line>` or `APPYNET: blocked — <why>` or `APPYNET: question — <a real decision>`. Emit it only for those, never for status.

## David's spec, for reference
Keep ElevenLabs as production. Investigate voice quality, word-level timing, hardware (Apple Silicon, CUDA), automation (API, MCP, headless) and licensing (AGPL-3.0, model licences). Explore a provider interface: ElevenLabs (production), VoiceStudio/VoxCPM (experimental). Acceptance: quality acceptable against ElevenLabs; timings accurate enough for the pipeline; practical on our hardware; unattended generation; licence fits commercial use; no substantial pipeline changes. Research before installation; keep it isolated and reversible; no new production dependencies.
