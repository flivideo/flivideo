# d06 selection board v2 (2026-09-27)

`d06-selection-board-v2.png`. Three thumbnails, each from a fresh ChatGPT chat with no history, the v2 brief and 3-9 identity references. Headlines composited by `tools/composite_headline.py`.

| Tile | Chat | Claude's read vs the 9-tile board |
|---|---|---|
| A1 AI selection reveal | 6ab8993a-8210-83ec-9e8d-356c4ecd2f63 | Board-level drama. The pointing hero is invented. Busiest of the three |
| A2 Face tagging | 6ab89c4c-915c-83ec-8d43-9944a8a3839f | Cleanest and reads fastest. Less story than the board tiles (no object or world, just a face plus labels). **Headline clashed with a label chip at the spec position and was moved lower-left** |
| A3 Photos to thumbnail | 6ab89c9b-64f0-83ec-8758-5960ab50065f | Closest to the board: a real scene, a performance (pointing, grin) and a visual event (card flying out of the picker). The monitor UI is re-rendered, not the literal screenshot; fine at thumbnail size |

**Measured lesson:** the compositor placed text where the spec said, not where the image left room. Fix for v3: the art direction must *name* the empty headline zone ("keep the top-left third empty dark background"), and the compositor must check for overlap (or pick the calmest region) before placing text.

**Still open for David:** likeness of the generated faces, dark thumbnails as a brand rule, and his pick.
