# Test 1 vs the board: why it's "half done"

**Purpose**: David's verdict on test 1: "I would not use it. It feels half done." He'd use all nine board tiles. This file records why, and what v2 changes.
**For Agents**: read before writing any new spec. The board (`../../../../source/board-2026-09-26.png`) is the bar, not the spec.

## My diagnosis (Claude, written before asking ChatGPT)

| Board tile does | Test 1 does | Cause in our system |
|---|---|---|
| Presenter lives **in a scene**: a real room, depth of field, warm practical lights, bokeh | Figures floating on a flat cream void. A collage, not a place | Brand config forced a cream canvas, "no dark photo background, no vignette" |
| **Contrast and drama**: dark surroundings make the face and glowing objects pop | Everything is the same brightness, nothing pops | The same light-mode rule. **All nine tiles David would use are mostly dark** |
| Presenter **acts on the story**: points at the tiles, shushes, cups an ear, holds his head | Hero is shocked at nothing and doesn't look or point at the wall | Specs said "composite the original cutout, do not regenerate". Library has 0 pointing shots |
| Presenter **relit to match the scene** (rim light, same colour temperature) | Studio-white cutout lighting pasted onto paper | "prefer_original_cutout", "do_not_reinvent" push the model to paste, not render |
| Objects are **finished, glossy, glowing**: app icons, waveforms, UI with depth | **Checkerboard transparency grids**, which read as "unfinished placeholder" | My spec literally asked for checkerboard cards (taken from the picker UI) |
| Story is in the objects (tools, waveforms, detection box) | Story is in labels ("GRIN", "THINKING") | Recipe leaned on tag chips, not visual metaphor |
| Came from a **short evocative prompt** plus rich context | 21k characters of JSON coordinates and rules | Over-specification. The model executed literally, with no art direction |

**The big one:** the light-mode rule. It was applied to thumbnails from the artefact rule and the fact sheets, but the evidence (the nine tiles David would use) says thumbnails want scene depth and dark contrast. That's a brand ruling only David can make. Test 2 relaxes it as an **experiment**, not a ruling.

## What v2 changes (spec d06.a1 v2)
1. A real environment: warm creator studio or desk, shallow depth of field. Brand colours as accents (yellow, amber, cream cards), not as a flat canvas.
2. No checkerboards. Faces shown as glossy printed photos or cards on a board, or on a monitor.
3. The presenter interacts with the wall: pointing at, or holding, one photo. The model may re-pose and relight him from the cutouts (identity check stays).
4. The brief leads with a short art-direction paragraph (what the board prompt had). JSON supports it; it doesn't replace it.
