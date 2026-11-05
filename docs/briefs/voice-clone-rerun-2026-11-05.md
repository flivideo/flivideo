---
created: 2026-11-05
timestamp: 2026-11-05T15:05+07:00
---
# Brief: voice clone rerun with a clean sample and continuous text (M2 worker)

**Owner**: flivideo-orch (M4). **David's go**: 2026-11-05. **Folder**: `~/dev/labs/voice-poc/` on the M2 (read `REPORT.md`, `gen.py`, `script.txt` first).

## Why
David on take-2, the clone of his voice: "okay, except that between every sentence there was a breath, a pause, and some sort of background hiss." Likely causes, unproven: 17 lines generated separately and joined, and a 10.8 s reference clip with a noise floor around -42 dB.

## Do
1. **Better reference**: from David's own recordings only, pick a cleaner, steadier passage with a matching accurate transcript. Read-only from the M4 over SSH (`davidcruwys@100.82.235.39`, `~/dev/video-projects/`); the earlier clip came from his d10 FliCut recording. Measure the noise floor of candidates and record it. No cleanup that alters his voice unless you test it as a separate variant.
2. **Continuous text**: generate the same script as one piece or in long paragraphs, not line by line. If the engine limits length, split at paragraph breaks and join with a short crossfade.
3. Make at most three variants, so the cause can be separated: new reference + old line-by-line; new reference + continuous; and, if useful, one more. One generation at a time.
4. Measure each against the old take-2: duration, real-time factor, pause lengths between sentences, noise floor in those pauses, clipping. You can't judge how it sounds; don't claim quality.

## Deliverable
`page2/index.html` with relative-path audio: old take-2 first, then each variant, unlabelled until revealed, then the measurements. Light-only AppyDave page (cream `#faf5ec`, white cards, `#342d2d` text, Oswald + Roboto, no `prefers-color-scheme`). Add a short section to `REPORT.md`; commit locally.

## Rules
David's voice stays on this machine: no remote, no upload, no hosted call, telemetry off. Don't clone anyone else. No ElevenLabs calls, no paid calls. Stay in this folder, nothing global, no `sudo`. Other workers are using this machine: stop and report if it swaps hard. Start no server; orch serves the page. Use `command grep`.

End with exactly one line: `APPYNET: done — <one line>`, `APPYNET: blocked — <why>` or `APPYNET: question — <a real decision>`. Never for status.
