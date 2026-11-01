---
created: 2026-11-01
timestamp: 2026-11-01T12:50+07:00
---
# Brief: FliTools — a text-to-speech verb (Kokoro) for Story Pilot "Listen" (2026-11-01)

**From:** `flivideo-orch` (Swagger). **To:** `flitools-dev` (tmux `flitools-dev`). **Report to `flivideo-orch` by name.**
**Worktree:** `/Users/davidcruwys/dev/ad/flivideo/flitools-worktrees/tts-verb`, branch `tts-verb`, from main `71821aa`.
**Go:** David, 2026-11-01 ~12:45 +07: "I pretty much like the listen page. I think it's now time to build it."

## Read first

- The approved design: `/Users/davidcruwys/dev/ad/flivideo/docs/specs/storypilot-listen-2026-11-01.md` (§ who runs it,
  § ownership table). FliTools owns speech synthesis; Story Pilot must never shell out to Python.
- FliTools' own `README.md` / docs, and how an existing verb is built end to end (transcription is the closest
  precedent). Match its patterns: verb registration, `api/` contract, the `@flivideo/core` client (`fli-core/src/flitools.ts`), tests.
- Kokoro on this machine: the `appydave:kokoro-tts` skill shows how Kokoro is installed and invoked today (venv, voices).
  Use it as a reference for the engine, not as the runtime path.

## Build

1. A FliTools verb (name it by FliTools' convention, e.g. `speech.synthesize`): input = text, voice (default from a
   config), output path (absolute; caller decides; Story Pilot will pass a path under the project's `-renders/`).
   Output = an audio file + duration + the voice used. Idempotent: same text + voice + path → no-op if the file exists.
2. A capability check (e.g. `speech.available` or folded into an existing health/capabilities verb): reports whether
   Kokoro is installed on this machine and why not if not ("not installed on this machine" must be a clean error, not a crash).
3. Batch-friendly: Story Pilot will ask for ~26 paragraphs at once. Either accept a list or make sequential calls cheap
   (keep the model warm). State which in the report.
4. The `@flivideo/core` client method, if that is how FliStudio talks to FliTools: **flag it in your report before
   touching fli-core**. A fli-core change is a shared-contract change and needs orch's go.

## Lane and limits

- FliTools only. Do not touch FliStudio or Story Pilot (`storypilot-dev` builds that side against your contract).
- Do not merge, do not restart the live FliTools service (`:7161`), do not edit launchd.
- Do not install system-wide packages; if Kokoro is missing for FliTools' runtime, report exactly what is needed.

## Done =

- Typecheck + tests green in the worktree; a test that synthesises a short sentence to a temp path (skip cleanly when
  Kokoro is unavailable, and say so); a timing for one ~60-word paragraph.
- The verb contract written down (method name, params, result, errors) in FliTools docs; paste it into your report
  so orch can hand it to `storypilot-dev`.
- Commit, push `tts-verb`. Report to `flivideo-orch`: commit, gate tails, the contract, timing, anything unverified.
