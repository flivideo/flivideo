---
title: "Idea — a central chapter store, and a two-level script (2026-10-17)"
description: "David's notes from D09 prep: chapters are planned before recording for the first time, which points to FliStudio owning chapters centrally, a video-level outline plus chapter-level scripts in Teletubby, and FliHub's real transcripts feeding back into later chapters."
tags: [flistudio, teletubby, flihub, chapters, idea]
created: 2026-10-17
timestamp: 2026-10-17
status: idea-not-decided
---

# Idea: a central chapter store and a two-level script

**Purpose**: Record David's 2026-10-17 observation before it's lost. Nothing here is decided or ticketed.

**For Agents**: Read this before designing chapters in FliStudio, a Teletubby outline view, or a FliHub→Teletubby feedback path. Treat it as a raw idea; ask David before building any of it.

## What happened

D09 is the first video where the chapters were planned **before** recording and loaded into Teletubby. David normally handwrites chapters and films his way through them.

- Outline: `/Users/davidcruwys/dev/ad/brains/openrig/d09-outline.md`
- Script: `/Users/davidcruwys/dev/ad/brains/openrig/d09-script.md`
- Teletubby set `openrig-coding-team`: one script per chapter, exported to `d09-openrig-coding-team/fli.tubby.json`

## The three notes (David's words, paraphrased)

1. **A central chapter store in FliStudio.** FliStudio already centralises resources and videos, but not chapters. If Teletubby and FliHub are going to talk to each other, they need one place that owns the chapter list.
2. **Two levels of Teletubby document.** A per-chapter script isn't enough on its own; there's also a whole-video outline. Build the outline first, then build each chapter's script around it.
3. **FliHub feeds back.** FliHub holds what was actually recorded, so a later chapter's script could be adjusted to what really happened in the earlier chapters.

## Facts that bear on it (checked 2026-10-17)

- Teletubby's model is set → script (`title`, `takeaway`, `summary`) → transcript → major/minor topic headings → paragraphs, plus triggers per paragraph (`src/shared/domain-schema.ts`). A set has only `title` and `description`, so there is **no video-level outline object** today. D09 put each chapter's job in `takeaway` and its screen and length in `summary`.
- FliStudio resource kinds include `chapters` (launch group: the YouTube chapter list, i.e. after the edit), not planned chapters.
- FliHub take names already carry a chapter number (`04-2-kybernesis` style). Inferred from file names, not checked against FliHub docs.
