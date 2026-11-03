# Story Pilot W4: rerun, versions, undo, build record

**Purpose**: Build brief for W4 of the Story Pilot plan. Every script change becomes a version you can step back to. Every
AI build leaves a record of what went in. A Rerun control asks an agent to *update* (or *recreate*) the script from the
same Document Islands.

**For Agents**: Read in full. Starts after W2.1 is merged. Background is the design note
`docs/briefs/storypilot-captains-log-mapping-2026-11-03.md` (sections "How the d13 script was actually built",
"David thinking out loud, round 2", "Rulings and re-sequence"). Owner: `flivideo-orch`. From: `flivideo-roamy`. No
David decisions needed to build it. The **first real run** (d13) waits for David's story-instructions conversation:
build the machinery, do NOT rerun d13.

## Why (David's words, 2026-11-03)

- "You might want to regenerate and know that you're connecting up to the same data, but you want a little bit of a
  custom instruction… a modification… says something very different to creating it the first time."
- "When you do a modification, you've also got the output script."
- "I wonder whether there's ever a need for history on those scripts."
- "An undo command… I've been typing in the word David so I can hear it through the regen… then I've got to go and
  delete it and let it regenerate again, when really I want to do an undo."
- Nobody could say how d13's script was built: it took a transcript dig (one hand-written pass by `storypilot-dev`,
  30 Oct, 4 minutes, no workflow, no instructions).

## 1 · Versions (every write)

- Every write of the script (`story.script.set`, paragraph edits in the Reader, segment changes, agent builds) appends
  a version under `script/storypilot/project/versions/` with `{n, at, by, kind: edit|build|restore, note}` and the
  full text. A small edit is still a version. Coalesce rapid keystroke saves from one person within ~10 s into one.
- Verbs: `story.script.history`, `story.script.get {version}`, `story.script.restore {version}` (writes a new
  version, never rewrites history), `story.script.undo` (= restore the previous).
- **Listen stays cheap:** after undo or restore, only paragraphs whose hash changed need new audio (reuse Listen's
  per-paragraph hash).

## 2 · Build record (every AI build)

When an agent writes a script as a build, it records `story.build.record` with the version:
`{mode: create|update|recreate, instruction (the change note), previousVersion, sources: [{resource, kind, nature,
layer, extract sha or file hash or CL code}], settings (resolved, each with its level), templates (ids + text hash),
skill + version, model, by, at}`. `story.brief` returns everything needed to fill it. Update the `flivideo:storypilot`
skill so a build always records it (and fails loudly if it can't).

## 3 · Rerun (compose and send; FliStudio never calls a model)

- A **Rerun** control on the script: mode **Update** (default: same islands + current script + the change note) or
  **Recreate** (same islands + settings + instructions, ignores the current script), and a change-note box.
- It composes one instruction for an agent: the storypilot skill, `story.brief`, the mode, the note, the current
  version number, and "record the build". It **sends it via the Send-to-session channel** to a chosen session (default
  `flivideo-orch`). If that feature is off, it offers Copy instead.
- A pending marker shows "rerun asked of <session> at <time>" until a new build version lands.

## 4 · Provenance in the Reader (a list, not a graph)

A "How this script was built" panel on the script: the version list (who, when, kind, note), and for build versions the
record as a plain list (mode, instruction, islands with natures and freshness, settings levels, instructions, skill,
model). No React Flow (ruled out for now).

## Tests

Version append and coalescing; restore and undo never lose history; the build record schema plus the `story.brief`
round trip; Rerun composes the right instruction for both modes and the Copy fallback; Listen regenerates only changed
paragraphs after undo; e2e: edit a paragraph, undo, the text and audio state come back, and the provenance panel shows
both versions.

## Out of scope

The d13 rerun itself (waits for David); the content of story instructions; React Flow; diffs beyond a simple
changed-paragraph highlight; running any model inside FliStudio.

## Gate and report

Unit + typecheck, every storypilot spec with the CL stub, and every other suite green. Build on the M2, re-gate and merge
on the M4, restart. Screenshots on a **copy** of a project (not d13's real script): the provenance panel with two
versions, and the Rerun control open. Report to `flivideo-roamy`.
