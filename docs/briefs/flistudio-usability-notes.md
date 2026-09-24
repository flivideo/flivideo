---
type: brief
title: FliStudio usability notes
description: "Batch of David's hands-on FliStudio observations, explained from the code, waiting to be released as one mock-first brief."
created: 2026-09-24
timestamp: 2026-09-24
status: active
---

# FliStudio usability notes

**Purpose**: collect David's FliStudio UI observations (batch rule), with orch's explanation from code and a proposal; released to `flistudio` as one mock-first brief when David says.

**For Agents**: append, don't dispatch piecemeal.

## 1. App working folders shown as media folders (2026-09-24)
**David**: "I don't really know what to make of the other folders that get made. I'm not saying we've got to get rid of them, but they're just not clear … there are certainly working files from other applications, though there's nothing in them. It's still not right to show them, not the way you're doing it. Maybe a different way, but not that way." (screenshots: rail shows FLI.CUT.D04-AUTOPILOT-CUT/ 0, FLI.EDIT.ABC/ 0, FLI.EDIT.D04-FLIEDIT-UAT/ 0 …; detail pane lists raw UUID words.json filenames)
**Explained (code)**: `client/src/screens/ProjectHome.tsx` ~L728 lists every project subfolder as a media place ("has no media at its top level" / "Also in this folder: …"). Each FliCut/FliEdit edit = `fli.<app>.<name>.json` + a sibling `fli.<app>.<name>/` working folder (FliCut: words/health/last-export; FliEdit: history.jsonl + backups). `fli.edit.abc` = David's own FliEdit edit (history by human:ui). Relates to the 2026-09-23 ON-HOLD ruling "working-folder display in FliStudio".
**Proposal (orch)**: drop working folders from "In this project"; add one **Edits** group — a row per edit (readable name, app badge, last changed), click opens it in its app; working folder only via a small "files" affordance on the row.
