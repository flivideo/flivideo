---
type: reference
tags: [flivideo, ecosystem-research, capability-landscape, B686, B687]
description: "The twelve B687 capability categories mapped to external candidates, research depth (deep/light/none) and the owning FliVideo app. Research only; nothing here is decided."
created: 2026-11-03
timestamp: 2026-11-03T12:30+07:00
---

# 03b — Capability landscape (12 categories)

**Purpose**: One map of the twelve B687 §5.1 research categories → candidate engines → how deep B2 went → which FliVideo app owns the concern today. Written by B2 (`b686-rsch`), M2, 2026-11-03. Stars/dates are from `gh api`, 2026-11-03.

**For Agents**: Plan is `/Users/davidcruwys/dev/ad/brains/north-star/deliver-2026-11-03-B686-flivideo-ecosystem-research.md`. Every row links to a `candidates/` file. **All outcome leans are B2's lean, not approved.** Do not draw any candidate as part of the current system; B3 builds the target view from this.

## Observed fact / inference / recommendation key
Each candidate file separates *Observed* (read in the repo or from `gh api`), *Inference*, *Lean (not approved)*. Anything not read in code is marked **UNVERIFIED**.

## The twelve categories

| # | Category | FliVideo owner today | Depth | Candidates (file) | B2 one-line lean (not approved) |
|---|---|---|---|---|---|
| 1 | Teleprompters | Teletubby | deep | Textream, QPrompt ([teleprompter](candidates/teleprompter.md)) | Textream has the only verified agent-reachable surface (HTTP+WebSocket "Director", `textream://` URL scheme); absorb ideas, keep Teletubby unless agent-drive proves out |
| 2 | Screen recording | FliCast | light | Cap, open-recorder, Screenize, Recordly ([screen-recording](candidates/screen-recording.md)) | Prior brain work stands: Cap = Loom job; open-recorder/Screenize = event-log editor ideas; no replace |
| 3 | Timeline editing | FliEdit | deep | Kdenlive/MLT, libopenshot, Shotcut/MLT, FilmCraft ([fliedit-replacement](candidates/fliedit-replacement.md)); Concat, added 2026-11-08 ([concat](candidates/concat.md)) | MLT is the credible headless engine; Kdenlive's GUI is not agent-drivable; replacing FliEdit is a large bet, lean none/absorb-engine |
| 4 | Automated cutting | FliCut | light | auto-editor, LosslessCut, video-use ([flicut-alternative](candidates/flicut-alternative.md)) | No Gling/Descript-class OSS found that beats FliCut; auto-editor is the useful engine/tool |
| 5 | Composition & motion graphics | Motion Pilot (idea) | light | Remotion, Motion Canvas, Manim ([remotion](candidates/remotion.md), [motion-canvas](candidates/motion-canvas.md)) | Already owned: Remotion + HyperFrames. Motion Canvas/Manim: note only |
| 6 | Media & B-roll management | B-roll Pilot | deep | Immich, ResourceSpace, Dam'It brain ([broll-dam](candidates/broll-dam.md)) | Immich is the mature, API-first option (AGPL); Dam'It design stands unless Immich proves per-media-type tagging |
| 7 | AI orchestration | Pilots (workflows) | deep | OpenMontage ([openmontage](candidates/openmontage.md)) | Same problem class as the pilots; harvest patterns, do not depend (AGPL, 1.5k-file instruction payload) |
| 8 | Scriptwriting | Story Pilot | light | OpenMontage script stage, Textream Director ([script-writing](candidates/script-writing.md)) | No standalone OSS scriptwriting engine surfaced; Story Pilot stays |
| 9 | B-roll selection | B-roll Pilot / Story Pilot | light | folded into #6 and #7 | See [broll-dam](candidates/broll-dam.md) and [openmontage](candidates/openmontage.md) |
| 10 | Overlays | Overlay Pilot | deep | HyperFrames ([hyperframes-as-editor](candidates/hyperframes-as-editor.md)) | HyperFrames already underlies overlays; question is whether its Studio is an editor surface (spike: yes, see plan §7) |
| 11 | Craft projects | none (reference) | light | ArtCraft's 7 Craft apps ([craft-projects](candidates/craft-projects.md)) | Roll-up only; prior brain audit cited, not redone |
| 12 | Capture routing | FliHub | none | none | B686: nothing comparable; no change. Not researched |

**Added 2026-11-08**: [Concat](candidates/concat.md) — an editor an agent can drive through MCP, and a possible CapCut replacement. AGPL-3.0: study only, never port code.

## Out of scope (one line each)
- Godot, Three.js, Blender: building blocks David may build on, not external tools (B686). Not researched.
- FliHub alternatives: B686 says none needed.
- The 50-example motion study: B683-era, running in ChatGPT.
- ArtCraft clones remain on the M4 only; B2 cites `brains/artcraft/`.
