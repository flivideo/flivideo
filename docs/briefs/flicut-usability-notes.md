---
type: brief
title: FliCut usability notes — batch
description: "David's hands-on FliCut observations (d04 edit, 2026-09-24), collected as a batch for one usability pass — NOT yet dispatched."
created: 2026-09-24
timestamp: 2026-09-24
status: collecting
---

# FliCut usability notes — batch

**Purpose**: One place for David's UI observations while he uses FliCut on d04. He asked for them to be
**batched, not delegated one by one**: *"Not everything I'm asking you to do needs to be delegated
straight away. A lot of what I'm going to talk about is just user interface stuff. I think baking it all
up would be better than just doing it."*

**For Agents**: flivideo-orch keeps adding to this. Nothing here is dispatched until David says the batch
is ready. Then it becomes one usability brief for the `flicut` window: mock first, frontend-design skill,
minimal but functional.

David's headline: *"I don't think you've used this application. I think this whole application has not
been viewed from any sort of serious usability point of view because nothing feels nice."*

## Already dispatched before the batch rule (in flight in the flicut window)
- Real undo/redo (⌘Z walks back, ⇧⌘Z forward) + a clickable history panel.
- The film strip follows the playhead; the scrollbar is visible; trackpad scroll pans.
- J/K/L match FliHub/FliCast (J = reverse) + an on-screen speed/direction indicator.
- Trim → frame-accurate in/out: mock https://claude.ai/artifact/GoVGaZPzBq28U86c3yBJJy, 3 questions
  open (exact vs padded; ←/→ = playhead, I/O = in/out, inverse → ⇧I; commit at once). **Awaiting David.**

## Observations (verbatim + what the code does)

| # | David said | What it actually does (code: `flicut/src/renderer/src/Editor.tsx`) | Problem |
|---|---|---|---|
| 1 | "skip cuts … Pressing the button doesn't seem to change the interface, so I'm not sure what it's doing." | `viewState.skipCuts` (K): playback jumps over removed material. Playback only. | No visible change; the purpose is invisible |
| 2 | "I don't really understand what inverse cuts are about." | `inverseCuts` (I): plays ONLY removed material (audit), with a yellow "AUDIT" banner on the player | The name doesn't say "audit removed bits"; it also reshapes the transcript |
| 3 | "turn off show cuts. I get these big blank areas on the screen." | `showCuts` (H) hides removed words, but paragraph blocks keep their space | Hidden text leaves holes; it should collapse |
| 4 | "I don't really understand what first and last are doing. They feel like a weird toggle." | `⇤ first` / `last ⇥`: toggle-cut the whole first/last segment (usually lead-in/out silence); line-through when cut | One-click toggle on an invisible segment; no preview of what goes |
| 5 | "trim beginning … I can't understand what [it] does" | whole-timeline mask before the playhead (being replaced by in/out) | See the trim mock |
| 6 | Timeline "doesn't scroll … kinetic or momentum … should the film strip be scrolling with you?" | no follow; drag scrubs | in flight (film strip) |
| 7 | "Is there an undo history? Can we even see the history?" | undo toggles; history is read-only | in flight (undo/history) |
| 8 | Speed: "no indication of how fast we're going" (J slowed rather than reversed) | J/K/L semantics differ from the other apps | in flight (J/K/L) |
| 9 | Lead-in "half a second or a second of padding at the beginning, which I might want to play around with" | only via pad 0.15/0.15 (cuts) or the trim buttons | covered by the trim mock's worked example |

## Ideas to consider in the pass (orch, not David — to discuss)
- A real usability review: someone actually uses FliCut end to end on d04 (screenshots, a task list:
  review cuts, fix a bad cut, trim lead-in, audit removed material, export) and writes the friction log
  before any redesign.
- Group the toolbar by job (View · Playback · Edit), with plain labels and a one-line tooltip each.
- Make view toggles show their effect (e.g. skip cuts → strip gaps / a player badge "skipping cuts").
