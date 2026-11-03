---
type: reference
tags: [flivideo, ecosystem-research, candidate, B686, openmontage]
description: "Is OpenMontage's orchestration the same thing as FliVideo's pilots (workflows)? AGPL implications."
created: 2026-11-03
timestamp: 2026-11-03T12:30+07:00
---

# OpenMontage: orchestration vs the pilots

**Purpose**: Is OpenMontage's orchestration the same thing as FliVideo's pilots (workflows)? AGPL implications.

**For Agents**: Research only (B686 B2, 2026-11-03). *Observed* = read in repo or via `gh api`; *Inference* and *Lean* are B2's and **not approved**. Anything unread is **UNVERIFIED**. Index: [../03b-capability-landscape.md](../03b-capability-landscape.md).

- **Repo**: https://github.com/calesthio/OpenMontage (clone `9327439` at `/Users/davidcruwys/dev/upstream/repos/OpenMontage`, frozen reference per `brains/capability-registry/adoption-postures.md`). Beware the impostor `OpenMontage-app/OpenMontage` noted there.
- **Licence**: AGPL-3.0 (GitHub API; `LICENSE`). AGPL covers network use: running a modified version as a service obliges publishing source. Linking or deriving from it inside commercial FliVideo/AITLDR code is the blocker (brain: "AGPL blocks commercial DEPEND"). Ideas and patterns are not covered; copied code is.
- **Stars / last commit**: 75,436★, pushed 2026-10-28, 435 open issues (`gh api`).
- **Agent surface** *(Observed)*: not an app with an API. It is an **agent-instruction system**: `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `CURSOR.md`, `COPILOT.md`, `AGENT_GUIDE.md`, `pipeline_defs/*.yaml` (12 pipelines such as `talking-head.yaml`, `screen-demo.yaml`, `podcast-repurpose.yaml`, `clip-factory.yaml`), a `tools/` registry (capture, avatar, audio, analysis...), `skills/`, and a Remotion composer (`remotion-composer/`). Stages in `talking-head.yaml`: idea → script → scene_plan → assets → edit → compose → publish with revision caps. No MCP/JSON-RPC server found. The agent *is* the orchestrator.
- **Security**: earlier fleet scan: 0 HIGH / 3 MED (`adoption-postures.md`, shelf-life rule). Its large agent-instruction payload (brain: 1,583 files) is the main trust surface; many generative provider calls leave the machine.
- **Two questions**:
  1. *Elegant?* For topic-in → finished video via generative providers, yes in ambition; the brain scored it "mostly out of scope" for AppyDave because its momentum is generative providers (`creator-stack/automation-landscape.md`).
  2. *Agent-drivable safely?* It is agent-driven by design, but safety depends on instruction-file trust and provider keys. Not safe to adopt blind.

## Is it "the same thing as our pilots"? 
**Inference**: Partly. Both are *workflow definitions an agent follows over capabilities*. OpenMontage encodes them as YAML stage graphs + instruction files; FliVideo pilots are extension modules with UI and per-project data. Difference: pilots carry human review UI and project state; OpenMontage's pipelines are agent-script. That matches B686's framing: extensions own workflows, apps own capabilities.
- **Pattern worth harvesting (not depending)**: explicit stage graphs with per-stage revision caps and review gates (`pipeline_defs/talking-head.yaml`).
- **Outcome lean (not approved)**: *none* as a dependency (AGPL); *absorb ideas* into pilot design. Decision on AGPL posture belongs in the approval register (ledger #42).
