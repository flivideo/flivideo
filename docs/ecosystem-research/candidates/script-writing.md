---
type: reference
tags: [flivideo, ecosystem-research, candidate, B686, script]
description: "How would scriptwriting be done as an agent-orchestrated capability, and is there OSS worth adopting?"
created: 2026-11-03
timestamp: 2026-11-03T12:30+07:00
---

# Script writing (orchestration side) (light)

**Purpose**: How would scriptwriting be done as an agent-orchestrated capability, and is there OSS worth adopting?

**For Agents**: Research only (B686 B2, 2026-11-03). *Observed* = read in repo or via `gh api`; *Inference* and *Lean* are B2's and **not approved**. Anything unread is **UNVERIFIED**. Index: [../03b-capability-landscape.md](../03b-capability-landscape.md).

- **Repo**: no single repo. Reference points: OpenMontage `pipeline_defs/talking-head.yaml` (stage `script`, `/Users/davidcruwys/dev/upstream/repos/OpenMontage`); Textream Director Mode ([teleprompter.md](teleprompter.md)).
- **Licence**: OpenMontage AGPL-3.0; Textream MIT.
- **Stars / last commit**: OpenMontage 75,436★ / 2026-10-28; Textream 4,220★ / 2026-09-06.
- **Agent surface**: OpenMontage script stage is agent-instruction-driven (not an API). Textream accepts pushed text over HTTP/WebSocket and `textream://`. No standalone OSS scriptwriting engine with an API surfaced in this pass; **UNVERIFIED** that none exists (no dedicated search).
- **Security**: see the two linked files.
- **Two questions**: (1) scriptwriting is the LLM's job, the system's job is the stage gate and revision loop. (2) Story Pilot already owns this in FliVideo.
- **Outcome lean (not approved)**: *none*; borrow the stage/revision-cap pattern if Story Pilot grows.
