---
created: 2026-11-04
timestamp: 2026-11-04T17:20+07:00
---
# Brief: Teletubby voice-follow — fix "nothing happens", add real logging and a self-test (2026-11-04)

**From:** `flivideo-orch`. **To:** `tubby-voicefix-dev` (**M4**). Report to `flivideo-orch` and STOP.
**Go:** David, 2026-11-04 17:18 ("you haven't got proper logging… let's deal with it, or do a little test so I can get this working").
**Machine: M4** — the live test is happening here now (Teletubby running on d13, pid in `scripts/app.sh status`) and the M2 is unreachable.
Work in a worktree, never the live checkout: `git -C ~/dev/ad/flivideo/teletubby worktree add ~/dev/ad/flivideo/teletubby-worktrees/voicefix -b voicefix main` (GitHub has an outage; branch off local `main` = a31fce1).

## Symptom (17:15, real app, d13 "Story Pilot — Overlay Pilot")
David clicked the Voice chip ON and pressed V while presenting: **no macOS microphone prompt, nothing visible on the chip, nothing in
`.logs/app.log`**. Facts: launcher bundle `~/Library/Application Support/appydave-launchers/Teletubby.app`
(`com.appydave.teletubby.dev`, ad-hoc signed, Info.plist HAS NSMicrophoneUsageDescription); the user TCC db has **no microphone row**
for it (never asked); `GROQ_API_KEY` IS in the app's env; no Groq connection; press log works (a ↓ at 17:08 logged, no `voice` entries).
Code: `src/main/index.ts:~209` (`voiceControl` → `systemPreferences.askForMediaAccess`), `src/renderer/src/voice-live.ts:37`
(`getUserMedia`), `src/renderer/src/store.ts:~657`, `src/main/voice/{voice-session,groq-live,apple-live,secrets}.ts`. Voice errors
are only `emit`ted to the UI, never logged.

## Do
1. **Logging, everywhere in the voice path** (main logger → `.logs/app.log`, one line per event): V/chip toggle received (renderer →
   main), `voiceControl` start/stop, `getMediaAccessStatus('microphone')` before asking, `askForMediaAccess` result, getUserMedia
   success/failure (renderer → main IPC), recogniser chosen/fallback/error, each Groq request (status, ms — never the key), aligner
   step decisions. Errors also show on the chip as text.
2. **Find and fix the root cause** of "nothing happens" — prove it with the log lines from a real run, not a guess.
3. **Self-test** David can run with one command: `bash scripts/voice-selftest.sh` (and a door capability `voice_selftest`) that
   prints PASS/FAIL per check: key found; mic permission status (and how to grant if denied); Groq round trip on a 2 s bundled
   sample (latency, text); Apple helper present/permission; aligner on the sample vs a 2-paragraph script. Plain-English fix line
   per FAIL.
4. Tests: unit for the self-test checks (stubs) and the logging calls on the error paths. `npm run typecheck`, `npm test` green.
5. Commit on `voicefix` (local; push when GitHub allows). Do NOT restart the running Teletubby yourself — STOP and report: root
   cause with the log evidence, sha, test counts, the self-test output on this machine. Orch merges, restarts on d13, and runs the
   live test with David.
