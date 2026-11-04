---
created: 2026-11-04
timestamp: 2026-11-04T17:45+07:00
---
# Brief: Teletubby voice-follow — self-test gate, auto-off when off track, rate limiting fixed at the source, fallback on first refusal (2026-11-04)

**From:** `tubby-voicefix-dev` (drafted at David's request). **To:** `flivideo-orch`. Report to David and STOP.
**Go:** ⛔ **NOT GIVEN.** David has seen the recommendations but has not said go on items 2–4. Item 1 is a merge + restart +
self-test, and orch's normal between-takes rule applies to it. Do not build items 2–4 until David says go.
**Machine: M4.** Teletubby runs here on d13 (`scripts/app.sh status`); the logging run below happened here. Build in a worktree
off teletubby `main` once go is given, never in the live checkout.
**Follows:** `docs/briefs/teletubby-voice-logging-and-selftest-2026-11-04.md` (logging `c2a86cf`, merged; self-test `c6fd6c5`,
local on branch `voicefix`, not merged, not pushed — GitHub outage).

## Symptom (17:25–17:29, real app, d13 "Story Pilot — Overlay Pilot", logging build `c2a86cf`)

Source: `/Users/davidcruwys/dev/ad/flivideo/teletubby/.logs/app.log`, lines with `"msg":"voice"`. The path works end to end
(mic granted via iTerm, HyperX QuadCast open, Groq hearing David correctly). Four things are wrong:

1. **The prompter moves only at paragraph ends.** The aligner confirmed progress inside p4 every 2 s, but the prompter did not
   move until the paragraph boundary:
   ```
   17:26:22 groq 200 "So I wrote it down."                                   aligner advanced p4
   17:26:24 groq 200 "…as one line and it became the North"                 aligner advanced p4
   17:26:26 groq 200 "…the Norse staff, the whole thing."                    aligner advanced p4
   17:26:28 groq 200 "…star for the whole thing. Joy's videos don't go out…" aligner advanced p4
   17:26:30 groq 200 "…she's blocked on beautiful meaningful texts"          aligner advanced p4
   17:26:32 groq 200 "…meaningful text overlays."                            aligner advanced p5  MOVED
   17:26:36 groq 200 "…I'm Abbey Dave, let's get into it."                   aligner advanced p6  MOVED
   ```
   So for 10–20 s per paragraph nothing visible happens: the most likely reading of the 17:15 "nothing happens" report.
   That run predates the logging, so this is not proven for 17:15.
2. **About 41% of Groq requests got 429** (46 of 112 in 17:25:25–17:29:58). The brief's earlier "~50%" was an estimate; this is
   the count. All 46 came after 17:26:42. The 13 requests during the reading itself all got 200, and the refusals arrive in a
   near-alternating 200/429 pattern while the chip polled on.
3. **It kept listening off script.** After 17:26:42 David stopped reading, talked to the session, and (by his account) went to
   another app and dictated with Wispr Flow. Voice stayed on: the aligner logged 52 steps (43 `no-match`, 9 `held-no-agreement`)
   with 0 moves, and Groq kept being called. In ~2 min of silence Groq returned `"Thank you."` over and over (Whisper's
   silence hallucination), spending the key's rate limit for nothing.
4. **429 never reaches the fallback.** `src/main/voice/groq-live.ts` returns early on 429 ("back off, not a failure"), so the
   failure counter never moves and Apple can never take over while Groq is rate-limited.

## Do

1. **Gate: run the self-test in the app first.** Merge `c6fd6c5` (branch `voicefix` in `~/dev/ad/flivideo/teletubby`) into
   teletubby `main`. Restart Teletubby on d13 **only at a between-takes break**, announcing it to David in one line before it
   happens. Then run `bash scripts/voice-selftest.sh` and record PASS/FAIL for `mic-permission`, `groq-roundtrip` and
   `apple-helper`. If `apple-helper` FAILs on Speech Recognition, David must allow it: System Settings → Privacy & Security →
   Speech Recognition → **iTerm** (Teletubby inherits its permissions from the iTerm session that started it). **Items 3–4
   depend on Apple passing.** If `groq-roundtrip` FAILs with 429, turn the Voice chip off, wait a minute and re-run before
   recording it.
2. **Auto-off when off track** (David's option A). Voice turns itself off after **~30 s of continuous aligner `no-match` /
   `held-no-agreement` while the audio has speech in it**, or after **~90 s of silence** (pcm peak below ~0.01). The chip shows
   why, e.g. "voice off — off script" or "voice off — silence". Every auto-off decision is one `voice` log line (reason, how long,
   last aligner reason, peak). The thresholds are starting guesses, tuned after a real take. ⛔ **Do NOT auto-off on window
   blur / focus loss**: Ecamm is in front during recording.
3. **Fix rate limiting at the source.** (a) Do not send a tick to Groq when the new audio's peak is below the silence threshold;
   this removes the "Thank you." hallucinations. (b) Tick 2 s → 3 s. (c) Honour Groq's `Retry-After` header on a 429. Do not
   write Groq's per-minute limit into code, comments or docs as a fact unless it is verified against Groq's published
   documentation, with the URL cited.
4. **Fall back on the first refusal**, only after 3 has landed and item 1 shows Apple PASS. Any Groq 429 or hard error switches to
   Apple straight away; retry Groq after 60 s. Log each switch (from, to, why) as a `voice` line, and show the engine on the chip
   as today.
5. **Open question for David, not a task.** On the mic (17:26:46–17:27:12) David asked for highlighting more often than once per
   paragraph, at parity with the original prompter ("it was able to highlight a lot more often… similar parity on the feature on
   our one?"). That is a new feature (sub-paragraph progress shown on screen). Put it to David as a question; do not schedule it.

Tests for 2–4: unit tests with stubbed clocks and recognisers (no real Groq); `npm run typecheck` and `npm test` green. Then a
real take with David reading two paragraphs, showing in `.logs/app.log`: no Groq calls during silence, an auto-off line after
walking away, and a fallback line if a 429 occurs.

Out of scope: the highlight-frequency feature (item 5); pushing `voicefix` while GitHub is down; any change outside the voice path.

## Report

To David, then STOP:
- Item 1: the self-test output (all five lines) from inside the app, and whether Speech Recognition had to be granted.
- Items 2–4 (only if go was given): sha, test counts, and the `voice` log lines from the real take showing auto-off, the silence
  gate and (if it occurred) a fallback switch.
- Item 5: David's answer, or "still open".
