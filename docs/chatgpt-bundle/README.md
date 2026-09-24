# ChatGPT source bundle — FliVideo

**Purpose**: A small, self-contained set of markdown files describing the current FliVideo suite, for
uploading as sources to the "FliVideo" ChatGPT project, so David can talk through running FliVideo on
autopilot.

**For Agents**: Don't hand-edit the generated files. Rebuild with `docs/chatgpt-bundle/build.sh`: it copies
each app's `docs/SYSTEM.md` and `docs/AGENT-NOTES.md`, the map, fli-core's README, the agent-drivable
reference and the walkthrough, and strips frontmatter, absolute paths and file:line anchors.
`40-flitools-state.md` is hand-written (FliTools has no SYSTEM.md yet).

Start with `00-flivideo-map.md`, then `01-autopilot-walkthrough.md`.

## Added 2026-09-24
- `40-flitools-state.md` — rewritten: FliTools is BUILT (v0.1.0, 7161, launchd); callers, limits, candidate next capabilities; FliGate = open proposal
- `50-d04-run-report.md` — the first autopilot UAT run (13/15; AC10 later fixed)
- `60-filmstudio-study.md` — FilmStudio study, verdict first (+ mapping, overlay comparison, capability inventory)
- `70-flicut-ux.md` — FliCut usability notes (18 jobs) + editor UX research (cut loupe, two-lane timeline, mode switch)
