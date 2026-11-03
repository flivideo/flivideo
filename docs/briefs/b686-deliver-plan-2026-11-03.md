---
created: 2026-11-03
timestamp: 2026-11-03T10:05+07:00
---
# Brief: plan the B686/B687 delivery (window A only, plan gate) — 2026-11-03

**From:** `flivideo-orch` (Swagger). **To:** `b686-deliver-plan` (M4, Opus, cwd `/Users/davidcruwys/dev/ad/brains`).
Report to `flivideo-orch` by name. **Go:** David, typed in flivideo-orch 2026-11-03 ("they probably should run on the M2,
and they probably should use a Captain's Log deliver").

## Inputs
- **B686** (Plaud, 2026-11-03 08:38) — David's spoken instructions. **The voice log wins on intent.**
- **B687** (chatgpt dossier #2 of conversation `6ae529f0-15d4-83ec-8335-3a3978e6c671`, previous dossier **B683**).
  Brief on M2: `~/dev/raw-intake/chatgpt/briefs/2026-11-03-video-coding-plan-dossier-2.md`. Read B683 only for baseline.
- B685 is noise. Endpoint: `https://mac-mini-m2.tail1acb0f.ts.net` (never localhost).

## Do — `captains-log:deliver` §1–§6, then the delivery file, then STOP (plan gate)
Run the skill's hearing and planning half exactly as written: hear (transcript, not synopsis) → ledger (mark source
B686/B687 per item) → dedupe → research what exists on disk → plan via `appydave:goal-plan` with a checkable AC table →
audit plan vs ledger line by line → constraints in prose with recommendations. Write the delivery file where the skill says
(a brains folder that holds briefs/quests; `deliver-2026-11-03-B686-<slug>.md`), commit and push.

**Then STOP. Do NOT launch window B.** Today runs a *plan gate* (David's call): orch shows him a one-screen plan and waits for
his go. Return to flivideo-orch a one-screen summary: numbered ledger lines (one line each), the windows and machines,
in/out of scope, the constraints and their defaults, spend/time guess, and the draft launch line(s) (checker-validated).

## What David already said (from B686 — carry, don't re-decide)
- It is a **research and architecture exercise, not a commitment to build**. Most output is documents and diagrams.
- Deliverables he named: a 30,000-ft **four-umbrella** doc (FliVideo, AppyFactory, Community Builder/Skool, Founder OS — light);
  **current FliVideo architecture** (6 apps: FliStudio, FliHub, FliCut, FliCast, FliEdit, Teletubby; pilots Overlay, Story,
  B-roll, Motion (idea); FliTools); a **possible target architecture** where each researched item gets one of: absorb capability
  / add an app / replace one of ours / no change; the **apps vs extensions vs tools** taxonomy and the **80-20 extension
  guardrail**, with "who enforces it, and how" as an open question; an **approval register** so nothing is assumed decided.
- Research: mature, well-liked open-source candidates agents can drive (JSON-RPC or similar): HyperFrames (high interest:
  editor inside FliVideo? overlap with FliEdit), OpenMontage (orchestration vs our pilots), Remotion, Motion Canvas,
  teleprompter (top 2 + comparison), screen recording (FliCast), FliCut alternatives (Gling/Descript-like), a timeline editor
  that could replace FliEdit, B-roll/media asset management, the "craft" projects ChatGPT named (verify they exist first).
  Depth: code, GitHub stars/health, security. Deep on the replacement candidates; lighter elsewhere.
- Placement: **M4 orchestrates; M2 does the heavy research, upstream clones and documents**, synced back. Upstream clones go
  through `~/dev/upstream/repos.jsonl` + `upstream:upstream-add` / `sync.sh`, never ad-hoc.
- David wants to see the worker terminals (the phrase was garbled — "all in further"; likely "in iTerm" / visible windows).
  Flag it as a constraint with a recommendation.
- David is testing the Story Pilot and Overlay Pilot transcripts himself today: plan nothing that touches those apps.

## Constraints from orch
- M2 is for unwatched builds; keep its RAM free for CrisperWhisper → propose how many concurrent M2 sessions (rec ≤2).
- Artefacts: AppyDave, light only, ghost-check 0. Docs in the repo that owns them (FliVideo docs in flivideo; umbrella doc
  in brains — you choose, say where).
- No app code changes, no merges, no restarts, no rig launches, no OpenRig upgrade.

## Limits
Planning only. No research beyond what planning needs (locating what exists). No cloning. Questions to flivideo-orch with a rec.
