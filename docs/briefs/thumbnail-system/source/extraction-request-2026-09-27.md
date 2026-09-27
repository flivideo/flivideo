Please do NOT generate any images in this reply. Text and JSON only.

The nine-concept board is the quality bar, but right now it can't be reproduced: it came from one short prose prompt that leaned on this chat's history. I want to turn it into a system I can run again in a fresh chat with no history. Please give me the following, as JSON code blocks where it's JSON:

(a) NINE FILLED SPECS. One complete JSON spec for each concept on the board, using the schema you proposed (video, creative recipe, assets, composition, rendering, variations, quality_checks) plus the new sections below: d01 A1 Cinematic creator, A2 Creator + interface, A3 Visual transformation; d02 A1 Noisy room to clean audio, A2 Cutty agent workflow, A3 Clipped word detection; d03 A1 Tracking quadrants, A2 Works in any language, A3 Agent places graphics. Fill in every field with what actually made that tile work: presenter pose/expression and which portrait role, framing and side, props, UI elements, labels, lighting, background. Each spec must be self-contained enough to paste into a fresh chat with only its listed assets attached.

(b) RECIPES. Name the nine concepts as reusable recipes (e.g. "cinematic_creator", "before_after_waveform"), each written generically with no video-specific details: what story shape it suits, layout, presenter role, required assets, typical graphics, and when not to use it. If two tiles are really the same recipe, say so.

(c) TEXT LAYER. Add an explicit "text_layer" section to the schema: headline wording (and alternates), whether the text is rendered inside the image by the model or overlaid afterwards by a compositor (recommend a default and say why), font/weight, position, safe area, and a minimum text size rule for readability at small YouTube sizes.

(d) BRAND CONFIG. A separate "brand" block for AppyDave that the specs reference by id rather than repeat. Force LIGHT MODE: cream #faf5ec background, brown #342d2d text, yellow #ffde59 accent/CTA, amber #c8841a secondary. The board wrongly used dark backgrounds in several tiles; the brand block should forbid that and say how dark areas may be used, if at all (small accents only).

(e) PRESENTER SEED. A "presenter" slot that points at an external portrait library (by portrait role, e.g. surprised / thinking / confident / pointing-left, plus an optional file id) instead of photos uploaded into the chat. Library location is TBD, so use a placeholder path.

Finally, give me the updated universal schema on its own (all sections, with a one-line description per field), so I can keep it as the template.
