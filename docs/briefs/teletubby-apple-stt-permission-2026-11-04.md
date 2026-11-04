---
created: 2026-11-04
timestamp: 2026-11-04T10:55+07:00
---
# Brief: Apple speech helper can't ask for permission — make it a proper app bundle (2026-11-04)

**From:** `flivideo-orch`. **To:** `tubby-applestt-dev` (**M2**). Report to `flivideo-orch` and STOP.
**Go:** within David's 2026-11-04 go on voice-follow (live mic, Groq vs Apple). **Machine: M2** — code.

## What happened (M4, 10:48)
After David accepted the Xcode licence, `native/apple-stt/build.sh` built `apple-stt`, and `scripts/recognizer-bench/run.sh apple`
run from an iTerm2 window failed with `apple: {"status":0,"error":"speech_auth"}` — status 0 = not determined, **no macOS
dialog appeared**. A bare command-line binary run under node under iTerm2 inherits iTerm2 as the responsible process, and iTerm2's
Info.plist has no `NSSpeechRecognitionUsageDescription`, so the request can't prompt.

## Do
1. Package the helper as a minimal signed-ad-hoc **`.app` bundle** (e.g. `native/apple-stt/build/TeletubbySpeech.app`) with its own
   Info.plist (`CFBundleIdentifier com.appydave.teletubby.speech`, `NSSpeechRecognitionUsageDescription`,
   `NSMicrophoneUsageDescription`), and launch it so it is its **own responsible process** (LaunchServices / `open -W -a … --args`,
   with stdin/stdout through a FIFO or a localhost socket as you judge simplest). It must ask once, and say clearly in its output
   when permission is denied (System Settings → Privacy & Security → Speech Recognition).
2. The bench (`scripts/recognizer-bench/run.sh apple`) and Teletubby's Apple fallback use the bundle. Groq path unchanged.
3. Tests: unit for the launcher's error mapping (denied / not determined / restricted / ok) with the native part stubbed.
4. Update `docs/voice-follow-bakeoff-2026-11-04.md` M4 steps. Worktree off `origin/main` (a31fce1+), branch `apple-stt-bundle`.

## Gate
`npm run typecheck`, `npm test` green. You can't grant the permission on the M2 — that's expected; say so. Push; report sha and the
exact M4 command; STOP. Orch runs it on the M4 with David (he clicks Allow).
