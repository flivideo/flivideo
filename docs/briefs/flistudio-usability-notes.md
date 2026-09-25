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

## 2. App order + stage groups; "Start an edit" → "Start a cut" (2026-09-25)
**David**: "I think the order in which applications show in FliStudio is important. I think FliHub should be followed by FliCast, and there should be something around them, thin, subtle, but nice, that says that this is about recording. Then there should be teletubby before both of them. And this is all about scripting. And then next should be FliCut and FliEdit, and this is all about editing. And then the term that says 'Start an edit' really should be, in this case, 'Start a cut' because it's only for FliCut, not for FliEdit."
**Ruling (David's words)**: order = Teletubby · FliHub · FliCast · FliCut · FliEdit, grouped **Scripting** (Teletubby) · **Recording** (FliHub, FliCast) · **Editing** (FliCut, FliEdit), with a thin, subtle group frame + label. Applies to both the app cards row and the APPS rail list. Rename the DO button "Start an edit →" to "Start a cut →" (it only starts FliCut).
**Status**: released with #1 as one mock-first brief (orch, 2026-09-25).
