---
type: reference
tags: [flivideo, ecosystem-research, candidate, B686, motion-canvas]
description: "Programmatic animation tools named in the earlier research; what they are and whether agents can drive them."
created: 2026-11-03
timestamp: 2026-11-03T12:30+07:00
---

# Motion Canvas and Manim (light)

**Purpose**: Programmatic animation tools named in the earlier research; what they are and whether agents can drive them.

**For Agents**: Research only (B686 B2, 2026-11-03). *Observed* = read in repo or via `gh api`; *Inference* and *Lean* are B2's and **not approved**. Anything unread is **UNVERIFIED**. Index: [../03b-capability-landscape.md](../03b-capability-landscape.md).

## Motion Canvas
- **Repo**: https://github.com/motion-canvas/motion-canvas (clone `7b91435`, `/Users/davidcruwys/dev/upstream/repos/motion-canvas`).
- **Licence**: MIT. **Stars / last commit**: 19,659★, pushed 2026-07-02 (four months before today), 177 open issues. Slower cadence than HyperFrames/Remotion.
- **Agent surface**: *Observed* packages: `core`, `2d`, `create`, `player`, `ui`, `vite-plugin`, `e2e`; one CLI bin (`create-motion-canvas`, a scaffolder). TypeScript generator-function animations with a Vite editor UI. No agent API, CLI render or MCP found; **UNVERIFIED** headless rendering details.
- **Security**: scoped scan CLEAN; npm install hooks not examined.
- **Two questions**: (1) elegant for explainers with an editor UI. (2) agent-drivable — weakly (code generation only).
- **Outcome lean (not approved)**: *none*; HyperFrames/Remotion already cover this lane.

## Manim (one line)
- **Repo**: https://github.com/ManimCommunity/manim. **Licence**: MIT. **Stars / last commit**: 42,170★, pushed 2026-11-02. **Agent surface**: Python code + CLI render (general knowledge, not verified in a clone — **UNVERIFIED**). **Security**: not cloned. **Two questions**: math/explainer animation; code-driven so agent-writable. **Outcome lean (not approved)**: *none*.
