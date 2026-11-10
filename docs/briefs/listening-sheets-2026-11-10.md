# Two listening sheets for David: D13 joins and the 7 Story Pilot scripts (10 Nov)

From exec-coord. David's words (10 Nov, ~19:50, on Roamy): "yes, build the listening sheet as an artifact with feedback fields … do the same for 02 Story Pilot: the missing happy path, that I can just listen to".

Context: the Fable research (B711) page https://claude.ai/artifact/38wBrhYoMzwRLU9vtJgwBc recommended (a) David labels ~15 D13 joins so the merged listening probe can be scored against his ear, and (b) David reads/listens to the 7 D13 Story Pilot scripts (main + 6 autopilot trials, 6 Nov) before anyone simplifies Story Pilot's UI. Findings: /Users/davidcruwys/dev/studies/fable-allocation/findings/1-flicut.md and 2-storypilot.md (git pull ~/dev/studies). David said "listen to 15 joins" was meaningless as written: no where, no how, no way to answer. These sheets fix that.

## Sheet 1: D13 joins (FliCut listening probe)
- One Claude Artifact page that works in a browser on Roamy (no FliCut, no M4 app needed).
- ~15 joins from the D13 edit, including the three already asked about (render4 0:51, 1:14, 2:54 in /Users/davidcruwys/dev/labs/d13-edit-qa/render4/overlay-pilot-render.wav), a mix the probe flagged and didn't flag. Pick them before publishing and record the pick and the probe/automatic-check verdict for each in a key file kept OFF the page (so David judges blind).
- Each join: a short clip (about 2 s before to 2 s after), playable on the page, with a replay button. Under it: Clean · Leftover · Too tight (one choice), plus a free-text note, plus a dictation (voice) note if the artifact `dictation` capability works.
- Answers saved with the artifact `db` capability (declare db + user), readable by agents with db_get/db_list, so David never copies anything back. Show "saved" per row.
- One plain line at the top: what a join is, what he's judging, about 10 minutes.
- After he submits: score the automatic check and the probe against his labels (hits, misses, false alarms) and report back to exec-coord in plain words.

## Sheet 2: the 7 Story Pilot scripts (D13)
- One Claude Artifact page to just listen: each of the 7 scripts read aloud (Kokoro, the house voice), with the text beside it. One-line header per script saying what made it (e.g. "AppyDave style · angle B"), without ranking them.
- Order: trial-appydave and main first, then the rest.
- Feedback per script, saved the same way (db): three quick questions from the research: Would I say this? · Is the spine true? · Would I record it today? (yes / nearly / no each), plus a free-text and dictation note.
- Scripts: on the M4 in D13's script/storypilot/project/scripts/*/script.json (lab copy on the M2: /Users/davidcruwys/dev/labs/variants-qa/d13-overlay-pilot/script/storypilot/project/scripts/). Read-only.
- After he answers: summarise which scripts (if any) he'd record, and what that says about whether to simplify Story Pilot's screen. Report to exec-coord.

## Rules
- AppyDave brand, light only (grep -c prefers-color-scheme = 0). Listen standard applies to page prose; the clips/scripts are the audio content.
- Private artifacts. Links as plain URLs. No changes to FliCut or Story Pilot code for this; extract audio and read files only. Build on the M2 by default (ruling 2026-11-03); the source audio is on the M4, copy what you need.
- Done when both pages are published, tested in a browser (audio plays, a test answer saves and reads back with db_get, then is cleared), and the two links are sent to exec-coord.
