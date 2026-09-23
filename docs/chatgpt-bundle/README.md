# ChatGPT source bundle — FliVideo

**Purpose**: A small, self-contained set of markdown files describing the current FliVideo suite, for
uploading as sources to the "FliVideo" ChatGPT project, so David can talk through running FliVideo on
autopilot.

**For Agents**: Don't hand-edit the generated files. Rebuild with `docs/chatgpt-bundle/build.sh`: it copies
each app's `docs/SYSTEM.md` and `docs/AGENT-NOTES.md`, the map, fli-core's README, the agent-drivable
reference and the walkthrough, and strips frontmatter, absolute paths and file:line anchors.
`40-flitools-state.md` is hand-written (FliTools has no SYSTEM.md yet).

Start with `00-flivideo-map.md`, then `01-autopilot-walkthrough.md`.
