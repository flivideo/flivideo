---
created: 2026-11-01
timestamp: 2026-11-01T22:30+07:00
---
# Story Pilot Prep: how to use it (for David, 2026-11-02)

Live: FliStudio main 3f6804e; skill `flivideo:storypilot-prep` (appydave-plugins 66266b0). Use a NEW Claude Code window so the skill loads.

1. **Angle (optional first).** FliStudio → project → Story Pilot. Double-click the angle line, write one line in your words.
   Toggle "provisional · proof pending" if it is not proven yet. No angle? Skip; the skill proposes up to 3, you click **Use this**.
2. **Run it.** In the video's own Claude window (e.g. `d19-storypilot-work`): `/flivideo:storypilot-prep d19`
   or "prep the story for D19". It places, orders, gives reasons, marks raw/synth, flags contradictions. It never writes your
   angle, never rewrites the script, never deletes.
3. **Read it.** Angle on top, numbered list under it. "contradicts angle" = keep as a struggle beat, or sharpen the angle.
   Wrong? **undo prep** (top line).
4. **Folded row at the bottom.** "+N about the tool · N suggested for removal": **put in the story** or **retire** (hides, never deletes).
5. **Later.** "out of date · copy refresh ask" → paste into Claude Code.

## Start with D19 (`/Users/davidcruwys/dev/video-projects/v-appydave/d19-spaghetti-rig`)
- Trial run on a copy proposed: (1) "Getting the anti-slop rig to work" (your words), (2) "The rig didn't prove it on the game,
  so we made it prove it on a real app", (3) "Gates, not prompts: what it took to make AI code clean on purpose".
- It put 16 of 50 sources in the story, 32 "about the tool", 3 suggested removals. **Check that "about the tool" line**: for D19
  the rig IS the subject, so the skill read it as "the rig's machinery, not the getting-it-to-work journey". That decides how short the list is.
- The weigh-up (beat 11) is flagged "contradicts": keep it as the beat the AppyStack run answers, or cut it.

## Known gaps
- Captain's Log / ChatGPT sources show "unknown" freshness (FliStudio cannot read them).
- Most summaries don't record what they were made from, so only the skill's own notes get freshness.
