# Brief: Story Pilot Direction box (David's standing instruction per video)

**Purpose**: Build brief. Each video's script gets a **Direction**: David's own standing custom instruction for that
video. It is saved with script versions, shown with the script, and read by every build.

**For Agents**: Owner `flivideo-orch`; build on the **M2**, re-gate and merge on the M4, restart via `my-app`. From
`flivideo-roamy`. **Go: David, 2026-11-04** ("DIRECTION BOX (GO)"). Builds on W4 (versions, build record, Rerun).

## Why (David, 2026-11-04)

"Do you ever receive custom guidance, custom instruction, from me anywhere currently? Even when I did get you to do
stories in the past, I'd do it from Claude Code, tell you where to pull everything from, but I'd still give you a custom
instruction. Now you've just given me a button called rerun, which seems like it's missing something."

Today a build is steered by the Angle (one line about *what* the video is about), the Global/Brand templates, the
settings, and the Rerun change note (one run only, hidden in the panel). Nothing holds David's standing *how*.

## Do

1. **Data.** A `direction` text per video in `script/storypilot/<video|project>/story.json` (or beside it), stamped
   `{by, at}`. Every change to it is a version in W4's history (kind `edit`, note "direction"), so undo/restore covers
   it.
2. **Verbs.** `story.direction.get` / `story.direction.set`. Agents may set it **only when David asked them to**;
   stamped `agent:<name>`. Shown as "set by" on screen.
3. **Screen.** A Direction box at the top of the Script section, above the text: multi-line, edit in place, saves on
   blur, shows who set it and when. Empty state: "Your standing instruction for this video: what to pull from, what to
   stress, what to avoid."
4. **Builds read it.** `story.brief` returns `direction`. The storypilot skill puts it first in a build's instructions.
   `story.build.record` records the direction's text hash and version.
5. **Rerun.** The change note's label becomes "What to change this time". The composed instruction includes the
   Direction (always) and the note (when given). Recreate also uses the Direction.
6. **Skill.** Update `flivideo:storypilot` (build section + Rerun) and bump the flivideo plugin version.

## Out of scope

The story-guides slots (separate brief); the content of any guide; changing the Angle.

## Gate and report

Unit + typecheck; the full storypilot suite, with e2e for Script and Rerun in full; every other suite green. Screenshots
on a **copy** of a project: the empty Direction box, a filled one, and History showing a direction edit. Report to
`flivideo-orch`.
