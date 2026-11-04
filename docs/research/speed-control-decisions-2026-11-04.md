---
created: 2026-11-04
timestamp: 2026-11-04T09:55+07:00
---
# Speed control: David's decisions (2026-11-04)

**Purpose**: The decisions David recorded on the published mocks page, kept in git (the live artifact version
`1793756864-a912` at https://claude.ai/artifact/L27SoDDdwoEsH1bWiMBBZX holds them; the source HTML in
`docs/artifacts/speed-control-mocks-2026-11-04.html` predates them — **republish from the live version, not that file**).

**For Agents**: Read before planning or building the shared speed control or shared playback controls.

## Phase 1: speed control (plan first, show David before code)
- **3-visible everywhere**: Story Pilot Listen, FliStudio Viewer, FliCut Player, FliHub playback modal ("I like 3 visible").
- **One control across both stacks** (Electron and AppyStack). Measured stacks: FliStudio (incl. Story Pilot Listen) and
  FliHub are AppyStack web apps; FliCut is Electron (AppyTron). David's guess put Listen with FliCut; it is in FliStudio.
- **Edges approved**: window pins at 0.25× / 4×, that chevron greys out.
- **J / K / L unchanged**: the control follows fli-core's `jkl()`.
- **Tooltips approved**: keys in tooltips and the ? sheet, no inline key text.
- **Takes approved**: keep the ten-rate `FORWARD_SPEEDS` ladder; one component in fli-core's UI layer with `visible`
  (default 3); FliCut keeps its badge for ±8× reverse.

## Phase 2 (after phase 1): shared playback controls
FliHub is the reference set: auto-next ("segments" in FliHub), transcript display (word / phrase / off), autoplay, size
(large / normal), info (duration, file size), handy prev / next / play, **Space = play/pause everywhere**. Use each only where
it fits a player. Start with a matrix: which player has which feature today, and what each calls its "next thing".

## Plan approved + open questions ruled (David, 2026-11-04 19:40, via flivideo-roamy: "accept orch's takes on speed control")
- **Plan approved:** `docs/research/speed-control-plan-2026-11-04.md`. Step 1 (fli-core `speedWindow()` + shared `SpeedControl` in a
  `./ui` subpath, react as a peer dependency) builds now on the M2; one screenshot per app skin before steps 2–4.
- **Q2:** FliHub keeps its **2×** default; the other players start at 1× (default is per-app config, not part of the control).
- **Q3:** FliCut's own `[` `]` ladder is **retired** — one shared ladder everywhere.
- **Q5:** FliHub's **WatchPage and its modal both** get the control (they share `VideoControlsBar`).
- **Q4 (orch, technical):** package choice A, `@flivideo/core/ui` subpath; fli-core stays framework-free outside `ui/` (arch-test fence).
