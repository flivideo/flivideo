---
type: index
title: "00 · FliVideo ecosystem research — index"
description: "Entry point for the B686/B687 FliVideo ecosystem research (2026-11-03): reading order, what each doc holds, its status, and where the one closing artifact is."
tags: [ecosystem-research, index, flivideo, umbrellas, B686, B687]
created: 2026-11-03
timestamp: 2026-11-03T13:55+07:00
---

# 00 · FliVideo ecosystem research — index

**Purpose**: One place to start. The research David asked for in Captain's Log B686 (voice log, 2026-11-03 08:38)
with the ChatGPT dossier B687: the four umbrellas, the verified FliVideo land, the apps/extensions/tools split, the
outside candidates, a *possible* target and the register of what needs his approval.

**For Agents**:
- **Research, not a build plan.** 02 is the only "what is" doc; 04 is *possible*; nothing is decided until a row in
  06 changes. The plan that produced this is
  `/Users/davidcruwys/dev/ad/brains/north-star/deliver-2026-11-03-B686-flivideo-ecosystem-research.md`.
- David reads the **closing artifact**, not these files: "FliVideo ecosystem map" (URL in the plan §10 and in
  `/Users/davidcruwys/dev/ad/brains/ARTIFACTS.md`).

## Reading order

| # | Doc | What it holds | Status | By |
|---|---|---|---|---|
| 01 | [01-umbrella-architecture.md](01-umbrella-architecture.md) → `/Users/davidcruwys/dev/ad/brains/north-star/four-umbrellas-30000ft.md` | Four umbrellas (FliVideo, AppyFactory, Community Builder, Founder OS): purpose, unit of work, apps, one diagram | provisional | B1 |
| 02 | [02-flivideo-current-state.md](02-flivideo-current-state.md) | Six apps, three built extensions + Motion Pilot (idea), FliTools, fli-core — paths, SHAs, ports, doors, diagram | verified 2026-11-03 | B1 |
| 03 | [03-apps-extensions-tools.md](03-apps-extensions-tools.md) | Definitions, the 80-20 guardrail measured, extraction triggers T1–T5, five enforcement options | proposal | B1 |
| 03b | [03b-capability-landscape.md](03b-capability-landscape.md) | The 12 capability categories → candidates, depth, owning app | research | B2 |
| — | [candidates/](candidates/) | 11 files: deep — fliedit-replacement, hyperframes-as-editor, openmontage, broll-dam, teleprompter; light — flicut-alternative, screen-recording, craft-projects, script-writing, remotion, motion-canvas | research | B2 |
| 04 | [04-potential-target-architecture.md](04-potential-target-architecture.md) | Per candidate: absorb / add / replace / none; five design questions; a *possible* diagram | possible | B3 |
| 05 | [05-research-experiments.md](05-research-experiments.md) | Nine bounded Level-4 experiments (X1–X9) | planned, none run | B3 |
| 06 | [06-approval-register.md](06-approval-register.md) | 21 rows David rules on | all open | B3 |
| 07 | [07-research-execution.md](07-research-execution.md) | How the M4/M2 run went, what to reuse | record | B1 + B3 |
| 08 | [08-trial-plan-on-m4.md](08-trial-plan-on-m4.md) | Trial plan: 7 shortlisted outside apps walked through on d01-flivideo-tour, how each runs on the M4 and reaches FliStudio, one order of play. Visual: `trial-plan-on-m4.html` | plan, nothing run | eco-trial-plan |

## In one paragraph

FliVideo is the only built umbrella: FliStudio (control plane, 172 OpenRPC methods) hosts three extensions and
launches five satellite apps; FliTools is the shared tool service; fli-core is the domain core (02). Outside, nothing
is a mature *and* agent-drivable replacement for FliEdit; HyperFrames Studio is the strongest agent-drivable editor
surface but composition-first; Immich is the strongest B-roll store but AGPL + Docker; Textream is the only
agent-drivable teleprompter; OpenMontage is the pilots' problem class in YAML, AGPL (03b, candidates). The possible
target (04) adds a FliMotion app on HyperFrames, a B-roll library app, and an auto-editor tool — each a separate,
open row in 06.
