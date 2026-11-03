---
created: 2026-11-03
timestamp: 2026-11-03T19:35+07:00
---
# Brief: Textream vs Teletubby — what can we harvest, above all voice-following (2026-11-03)

**From:** `flivideo-orch` (Swagger). **To:** `textream-harvest-rsch` (**M2**, cwd `/Users/davidcruwys/dev/ad/flivideo`). Report to `flivideo-orch`.
**Go:** David to orch, 2026-11-03 ~19:30. **Machine: M2** — read-only research he won't watch, and the Textream clone lives there.

## David's words
"If we've got the code, we should look at it and see whether there's anything we can harvest from it for Teletubby … a full
review of it compared against Teletubby … The main thing I'm looking for is the voice: listening to the voice and
automatically changing the text."

## Sources (read-only)
- Textream: `~/dev/upstream/repos/textream` on the M2 (registered; Swift/macOS; **MIT** — unlike the AGPL tools, R13 does
  not forbid copying, but any copied code keeps its MIT notice + attribution). Release tested on the M4: v1.7.1.
- What the M4 trial already found: `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/candidates/teleprompter.md`
  §Experiment X5 (Director server on all interfaces, token leaked in its own page; `setText` hung on mic access).
- Teletubby: `/Users/davidcruwys/dev/ad/flivideo/teletubby` (Electron + TypeScript; read its `CLAUDE.md`, `AGENT-NOTES`,
  `docs/`, `src/`). `git pull` first. Skill `flivideo:teletubby`. Teletubby is fed by Story Pilot (`script.write`,
  `prompter.load` via FliTools, Elgato Prompter / Camera Hub).

## Do
1. **Voice-following first (the main ask).** How does Textream follow the speaker and move the text? Trace it in code with
   file:line: audio capture (AVAudioEngine), recognizer (Apple Speech / on-device?), how recognised words are aligned to the
   script (fuzzy match, char count, look-ahead window, recovery when the speaker skips or ad-libs), scroll/highlight logic,
   latency, language/offline behaviour, and its "listening modes" (e.g. `classic`). Note what is Apple-only.
2. **Teletubby today:** does it have any voice/auto-scroll? What drives scrolling now (manual, speed, Elgato dial)? Where
   would voice-following plug in (renderer vs main process, Electron mic permission, an existing transcriber like FliTools'
   CrisperWhisper/Groq/mlx-whisper)?
3. **Full side-by-side review** — a table of features (script load, formatting, mirroring, speed control, remote control,
   multi-screen/Elgato, chapters, voice follow, word highlight, notch/overlay UI, security model) with Textream vs Teletubby
   and a harvest verdict per row: **take the idea / port the code (MIT, with attribution) / skip**.
4. **Voice-following options for Teletubby**, each with cost and risk: (a) port Textream's alignment algorithm to TS and
   feed it from Apple Speech via a small native helper; (b) feed it from a local streaming whisper (what FliTools already
   has); (c) run Textream itself beside Teletubby (security fail noted — only if fixed). Recommend one, with a smallest
   first slice David could try.
5. Write `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/textream-vs-teletubby-harvest.md` (frontmatter like
   the other ecosystem docs; Purpose + For Agents), link it from `candidates/teleprompter.md` and `00-index.md`.
   Commit only those files, push.

## Limits
Read-only on Textream and Teletubby code: no edits, no builds, no running the app, no mic access. No new clones. Keep the M2
light. Timebox ~2 h. STOP after the push and report to `flivideo-orch`: how Textream's voice-following works (3–5 lines),
the recommended option + first slice, the top 5 harvest items, the sha.
