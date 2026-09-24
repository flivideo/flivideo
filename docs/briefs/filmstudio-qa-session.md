---
type: brief
title: FilmStudio Q&A session
description: "Preload for a fast, interactive Q&A where David learns what RxFilmStudio actually does, from a user's point of view."
created: 2026-09-24
timestamp: 2026-09-24
status: active
---

# FilmStudio Q&A session

**Purpose**: David read the study and said *"that didn't tell me anything about it"*. The study is
organised for mapping (buckets, target apps, verdicts). He wants to understand the **app itself**, as
someone who would use it. This window is his Q&A partner.

**For Agents**: You are window `filmstudio-work`, cwd `/Users/davidcruwys/dev/ad/brains/filmstudio`.
Read-only: don't edit files, don't build or run the app, don't download anything.

## Preload — read these first, in full
1. `/Users/davidcruwys/dev/upstream/repos/filmstudio-study/README.md`
2. Every file in `/Users/davidcruwys/dev/upstream/repos/filmstudio-study/docs/` (17 design docs:
   simple-mode, timeline-editing, screen-recording, video-generation, remotion-live-preview,
   caption-export, agent-tools, marketplace, subscription-plan, …)
3. `/Users/davidcruwys/dev/upstream/repos/filmstudio-study/_release-notes.md` (v1.0.0 → v1.9.0)
4. The brain: `INDEX.md`, `verdict.md`, `tech-notes.md`; use `capability-inventory.md` (398 rows) and
   `flivideo-mapping.md` as lookup tables, not as reading.
5. Skim the view folders to picture the screens: `/Users/davidcruwys/dev/upstream/repos/filmstudio-study/film-workflow/views/`
   (agent, caption, editor, imagegen, marketplace, music, narrative, recording, remotion, simplemode,
   videogen, …).

## How to open
A plain tour, about 10 lines, of **using FilmStudio start to finish**: you open it, you see…, you make
a project…, you record or generate…, you edit on the timeline…, you add captions/overlays…, you
export. Say which parts need RxLab credits. No bucket names, no FliVideo mapping, no jargon without a
one-line definition. Then stop and wait for his first question.

## How to answer
- Short and plain — this is a fast conversation. Lead with the answer; offer depth, don't dump it.
- Describe what a user **sees and does**. Use the source only to be accurate, and say "the code shows…"
  when a detail comes from code rather than docs.
- If he asks how it compares to FliVideo, use `flivideo-mapping.md`, and name the app.
- If you don't know, say so and say where you'd look.
- `grep` here is a ugrep shim: use `command grep` or `rg --no-ignore`.

## Standing context (don't raise unless asked)
- Its source has no licence: read and learn, never copy code.
- The FliGate idea (one MCP door for every Fli app) is David's open architecture question. He likes
  it, but also sees a shared fli-core adapter and MCP-as-plugin as options. It is to be written up as
  a proposal and decided in consultation later — not settled here.
