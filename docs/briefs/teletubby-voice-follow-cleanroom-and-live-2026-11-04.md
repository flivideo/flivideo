---
created: 2026-11-04
timestamp: 2026-11-04T10:35+07:00
---
# Brief: Teletubby voice-follow — clean-room rebuild (replace the port) + live mic, Groq vs Apple (2026-11-04)

**From:** `flivideo-orch`. **To:** `tubby-voice-dev` (**M2**). Report to `flivideo-orch` at each STOP.
**Go:** David, 2026-11-04 ~10:30 ("if there's unbuilt code on Teletubby, we need to fix it… I want the same thing" as Textream).
**Machine: M2** for code; the live test is on the **M4** with David (mic + permission clicks).

## Correction this fixes (David)
Slice 1 (`d748f8a`) **ported** Textream's matcher with an MIT header. That's wrong for David: we never lift code, we **rebuild
the concept in our own style** (`upstream:clean-room`). Replace `src/core/voice-follow.ts` (and the ported tests) with a
clean-room implementation; remove the MIT header/attribution once no Textream code remains (the provenance record says what
concept was studied). Apple's speech recognition is Apple's, not Textream's.

## Phase A — clean-room (start now)
1. Run the `upstream:clean-room` skill (`/Users/davidcruwys/dev/ad/appydave-plugins/upstream/skills/clean-room/SKILL.md`):
   repo `~/dev/upstream/repos/textream` (MIT → style mode), scope "following a reader's voice through a script", target
   Teletubby (AppyTron). Reader writes the concept spec in `~/dev/upstream/clean-room/textream-voice-follow/`, including the
   **delta** vs what Teletubby already has (its step model, slice-1 replay harness, the KNOWN LIMIT in
   `teletubby/docs/voice-follow-slice1-results-2026-11-03.md`). The spec must include the **word-level agreement guard** (ad-libs
   must not advance).
2. Gate (overlap check), freeze. **STOP 1**: report the spec path + hash.
3. Builder (a fresh agent given only the frozen spec + Teletubby conventions, never the upstream path) implements it in a
   worktree: `git -C ~/dev/ad/flivideo/teletubby fetch origin && git -C ~/dev/ad/flivideo/teletubby worktree add ~/dev/ad/flivideo/teletubby-worktrees/voice-follow-2 -b voice-follow-2 origin/main`.
   **Wait for orch's release before coding** — `tubby-presslog-dev` is changing the replay script on branch `press-log`; you
   branch after it merges. Tests: forward-only, guard rejects unrelated speech (the 45-char false step must not happen), jumps,
   cue skipping; replay harness still works.

## Phase B — recognizer bake-off (after A)
Same rule as FliTools transcription (`flitools/docs/architecture.md:79-81`): **Groq primary if it wins, local fallback.** Build
both behind one interface: (1) **Apple** on-device streaming speech recognition (a small native helper, AppyTron conventions);
(2) **Groq** `whisper-large-v3-turbo` on short rolling audio chunks (key from the secrets file the way FliTools loads
`GROQ_API_KEY`; never log or commit it). Measure on the same audio, fed at real time from existing takes (d01 `hub/recordings`,
read-only copies): **latency** (spoken word → word available, median/p90), **word accuracy** vs the FliTools transcript, **steps
correct** through the aligner. Apple needs Speech + Microphone permission granted once by a human — if the M2 blocks on it, run
Groq on the M2 and leave Apple's numbers for the M4 session. Decision rule (David's): Groq if better on latency AND quality,
else Apple primary; the other is the fallback. **STOP 2**: report the table and the pick.

## Phase C — live (after B)
Wire mic → recognizer → aligner → scroll in Teletubby presenting mode: a visible on/off, off by default; manual ↓ always wins and
re-anchors; a quiet indicator when it's following vs waiting. Press log (from `press-log`) keeps running so every live read is
test data. Typecheck + tests green. Push branch; **STOP 3**: orch re-gates on the M4, merges, restarts Teletubby, and runs the
first live read with David on d13's script (he clicks Allow for Microphone + Speech).

## Out of scope
Any Textream code or file copied; changing how manual scrolling works; FliStudio.
