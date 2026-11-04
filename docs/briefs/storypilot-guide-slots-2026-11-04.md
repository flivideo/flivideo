# Brief: Story Pilot guide slots (room for every story guide, pragmatic)

**Purpose**: Build brief. Give every story guide in the inventory a labelled slot in Story Pilot: a pointer to the real
file, never a copy, with type and level. Add empty slots for the missing cells, so David can start using them. No new
levels and no new structure.

**For Agents**: Owner `flivideo-orch`; build on the **M2**, re-gate and merge on the M4, restart via `my-app`. From
`flivideo-roamy`. **Go: David, 2026-11-04** ("STORY GUIDES (GO, PRAGMATIC)"). Research it rests on:
https://claude.ai/artifact/AeA1FzgAaT2iM25aiWuSx1, source
`/Users/davidcruwys/dev/ad/flivideo/docs/artifacts/storypilot-story-guides-2026-11-04.html` (inventory = Figure 2,
grid = Figure 3). Expect a later refactor, possibly into its own extension or app, so keep it simple and contained.

## Hard limits (David)

- **Don't change any guide's contents**, and don't rewrite settings values (the creator `voice.signatures` stamp stays
  as it is).
- **Don't decide series vs video project.** No new level. Use the existing levels; a "video project" row shows the
  series level, labelled "Video project (series, provisional)".
- A pointer only: store the absolute path or URL plus labels. Never copy file text into Story Pilot.

## Do

1. **Model.** A guide = `{id, label, type: verbal | voice | structure | lens | other, level: global | brand |
   series | video, appliesTo?: {form?: story | tutorial, length?: short | long}, pointer: path or URL | null, note?,
   changed}`. `pointer: null` = an empty slot waiting for David. Store per brand in `-storypilot/guides.json`
   (video level in the video's folder). `appliesTo` is a label only for now: builds don't filter by it yet.
2. **Seed** AppyDave (and vOz where shown) from the inventory, all pointers. These live on the M4: check each exists and
   mark any missing.
   - **Verbal, brand:** `brand-dave/skills/brand/references/appydave/VERBAL-STYLE.md`;
     `video-projects/v-appydave/voice-profile.md` (note: "overlaps VERBAL-STYLE; may merge later").
   - **Structure, global:** profiles build-story and build-short (pointer: `flistudio/modules/storypilot/defaults.json`
     with the profile id).
   - **Structure, brand:** `_formats/educational/VIDEO-STRUCTURE.md` (appliesTo tutorial);
     `flivideo/docs/research/appydave-hook-study-2026-11-03.md` (hooks).
   - **Empty slots:**
     - Voice, brand (Listen voice is a setting, not a guide);
     - Structure, brand, appliesTo story;
     - Lens, brand;
     - Structure and Lens at video project (series);
     - Lens, global.
   - **vOz** (brand voz, if a vOz brand root is registered): `v-voz/docs/brand/studio-narrative.md` (lens, brand); each
     project's `data/brand-variant.md` (lens) and `data/styleguide.md` (other: visual) as video-level slots.
3. **Verbs, agent-drivable:**
   - `story.guides.list {brand, project?, video?}`;
   - `story.guides.set` (add, change, clear a pointer, remove), stamped `{by}`; agents act only on David's word.
   - `story.brief` returns the guides for the video as pointers with labels, so a build can read them.
4. **Screen.** A **Guides** tab in Story Pilot's right-hand rail (it pushes content aside). It shows a level × type
   grid:
   - each filled slot shows its label and an Open ↗;
   - each empty slot is a dashed "add a guide" with a path field;
   - quiet styling (cream page, white cards, hairlines).
   - The existing Global/Brand templates stay where they are for now; add one line in the tab pointing to them.

## Out of scope

Filtering builds by `appliesTo` (the leak fix comes later, once David has used the slots); merging verbal docs; new
levels; guide contents.

## Gate and report

Unit + typecheck; the full storypilot suite, with e2e for the new tab in full; every other suite green. Screenshot the
Guides tab on AppyDave. Report to `flivideo-orch` with the seeded list, and any pointer that didn't resolve on the M4.
