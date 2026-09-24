---
type: brief
title: FliCut editor UX — deep research
description: "Deep research into editor usability, layout, visualisation and fine-grain control for a Gling-style text-based cut editor, to ground FliCut's redesign."
created: 2026-09-24
timestamp: 2026-09-24
status: active
---

# FliCut editor UX — deep research

**Purpose**: David, 2026-09-24: *"usability has to be number one, and then how it's all laid out and
visualised is also incredibly important. I think we need to do deep research into this."* FliCut works
technically, but *"nothing feels nice"*. Before any redesign we need to know how the best editors solve
the jobs FliCut must do.

**For Agents**: Window `flicut-rsch`. RESEARCH ONLY: no code changes in any Fli repo, and don't touch the
running FliCut. Report to `flivideo-orch` via SendMessage.

## Inputs — read first
- The job list (18 jobs) + David's observations: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/flicut-usability-notes.md`
- Gling teardown: `/Users/davidcruwys/dev/ad/brains/video-editing-as-code/gling-ui-surface-map.md`, `gling-project-format.md`; the INDEX of that brain
- Screen Studio (what it does well): `/Users/davidcruwys/dev/ad/brains/screen-studio/`
- FilmStudio timeline notes: `/Users/davidcruwys/dev/ad/brains/filmstudio/` (capability-inventory §timeline, verdict)
- FliCut today: `/Users/davidcruwys/dev/ad/flivideo/flicut` (docs/SYSTEM.md, src/renderer/src/Editor.tsx, Timeline.tsx, hotkeys.ts) — read-only
- The trim in/out mock: https://claude.ai/artifact/GoVGaZPzBq28U86c3yBJJy

## Questions
1. **Fine-grain control (David's #18, the headline).** How do pro and prosumer editors let you move an edge
   by 1–2 frames and SEE it? Find concrete patterns and name the product for each: Final Cut Pro
   precision editor, the Premiere trim monitor and ripple/roll, DaVinci Resolve cut page (dual timeline:
   whole-edit overview + zoomed detail), Avid trim mode, Descript, Gling, Audacity/Logic/Pro Tools zoom
   and waveform, Screen Studio, CapCut. Include modifier keys (⌥/⇧ drag = fine), magnifier/loupe, dual
   timelines, zoom-to-selection, frame-by-frame keys, and trim views that show the frames either side of
   a cut. Which of these would work *around the words* in a transcript-first editor?
2. **Layout and visualisation.** How text-first editors (Descript, Gling, Riverside, Premiere
   text-based editing, CapCut) lay out transcript, preview, timeline and controls; how they show
   removed material, modes and pace; what they put on screen versus hide. What makes them feel "nice"?
3. **Walk the 18 jobs.** For each: the best-in-class pattern (product + how it works), how FliCut does it
   today (read the code), and the gap.
4. **Agent parity.** For each pattern, note how an agent would do the same job through a verb, so the UI
   and the agent surface stay one model.

Use web research (docs, official help pages, reviews, tutorials); cite URLs. Screenshots from the web are
fine as references (don't redistribute them). Consider running FliCut read-only on d04 only if David
says so; he is using it.

## Deliverables
- A research doc: `/Users/davidcruwys/dev/ad/brains/video-editing-as-code/editor-ux-research.md`
  (brain standards; add it to that brain's INDEX). Sections: the fine-grain control patterns (with a
  recommendation), layout and visualisation patterns, the 18-jobs gap table, agent parity, and a
  recommended direction for FliCut in 10 bullets.
- A visual companion: a light-mode AppyDave artifact (load brand-dave:brand + frontend-design) that SHOWS
  the recommended layout and the fine-grain control idea as sketches. Look and feel needs visuals.
- Commit + push the brain file. Send flivideo-orch: the doc path, the artifact link, and a 5-line summary.

## Out of scope
Building or changing FliCut. Dispatching fixes. Deciding for David — this is research plus a recommendation.
