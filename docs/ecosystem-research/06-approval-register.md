---
type: register
title: "06 · Approval register — B686 FliVideo ecosystem research"
description: "Every recommendation and open question from 01–05 in one table, each with options, a recommendation and a status. Default status for every row is unapproved until David rules. Nothing in the research is decided until its row here changes."
tags: [ecosystem-research, approval-register, decisions, flivideo, umbrellas, B686, B687]
created: 2026-11-03
timestamp: 2026-11-03T13:50+07:00
status: open
---

# 06 · Approval register

**Purpose**: B686: "keep a simple register of what needs your approval so that nothing is assumed decided." One row
per thing David must rule on. If it is not ruled here, it is not decided.

**For Agents**:
- **Every row starts unapproved.** Only David changes a Status cell, in his words (record the date and where he said
  it). An agent may add evidence to a row (e.g. an experiment result from `05`) but never flips its status.
- The Status column holds exactly one value per row; counting the default status phrase must equal the row count
  until David rules. Do not use that phrase anywhere else in this file.
- When David rules: change Status to `approved YYYY-MM-DD` / `rejected YYYY-MM-DD` / `deferred`, add his words in
  the Ruling column, and update the source doc's lean if he chose differently.
- Sources: `01` = `/Users/davidcruwys/dev/ad/brains/north-star/four-umbrellas-30000ft.md` · `03` taxonomy · `04`
  target · `05` experiments (all in this folder).

---

## Register

| # | Item | Source | Options | Recommendation | Status | Ruling |
|---|---|---|---|---|---|---|
| R1 | Reading of the **80-20 rule** | 03 §2–§3 open (a); ledger #9 | (a) literal ~80% read verbs · (b) **"writes must delegate"** to an app/tool | (b) — the literal count ranks the pilots backwards (Story Pilot 41% but delegates; Overlay Pilot 77% but owns a renderer) | not approved | |
| R2 | **Who enforces 80-20, and how** | 03 §4–§5; ledger #9 | E1 descriptor · E2 depcruise rule · E3 tripwire report · E4 spec-time question · E5 review-skill step | E4 + E3 (report only) now; E2 with an allow-list later; E1/E5 when a pilot crosses a trigger | not approved | |
| R3 | Does **Overlay Pilot's renderer** count as "an app inside a pilot" today? | 03 open (b); 04 Q1 | yes (start Q1) · no (leave) · measure first (X8) | Measure first (X8); no change while David tests Overlay Pilot | not approved | |
| R4 | **Motion: Motion Pilot vs a FliMotion app** | ledger #13; 04 Q1 | M-A pilot only · M-B FliMotion app + thin pilots · M-C status quo | M-B, later, spec first | not approved | |
| R5 | **Umbrella naming**: Studio vs OS vs per-umbrella names | ledger #12; 01 U1 | "Studio" · "OS" · own name per umbrella | Avoid "Studio" as the umbrella word (it collides with the FliStudio app); no stronger rec | not approved | |
| R6 | Development umbrella name: **AppyFactory vs Appy Studio** | 01 U2 | AppyFactory · Appy Studio | none — David's naming call (B686 leaned "Appy factory actually might be good") | approved 2026-11-03 | **AppyFactory.** David, 2026-11-03 to flivideo-orch: "Let's call it Appy Factory." |
| R7 | Is **unit of work** the right lens for every umbrella? | ledger #11; 01 U3 | yes for all · yes except Founder OS · drop it | Keep for FliVideo (video project) and AppyFactory (repo); leave Founder OS open | not approved | |
| R8 | Does **Community Builder** get its own control plane? | 01 U4 | own control plane · FliVideo output stage · later | Later — start as an output of FliVideo projects | not approved | |
| R9 | **FliEdit's fate** | ledger #15 #20; 04 Q2 | E-A keep + HyperFrames for composition · E-B keep + MLT under it · E-C replace with HyperFrames · E-D replace with Kdenlive/Shotcut | E-A now; E-B if render hurts (X3); E-C only after X1 | not approved | |
| R10 | **HyperFrames Studio as an editor in FliStudio** (opens like FliCut) | ledger #15; 04 C1 | add · absorb engine only · none | Add (composition editor) + absorb for overlays; after X2 | not approved | |
| R11 | **MLT** as FliEdit's render engine | 04 C2 | absorb · none | None until FliEdit's render path hurts; then X3 | not approved | |
| R12 | **B-roll DAM** (library-wide B-roll; Joy's tool redevelopment) | ledger #21; 04 Q3 | B-A Dam'It own store · B-B Dam'It design over Immich · B-C ResourceSpace · B-D none | B-B if X4 passes, else B-A; B-roll Pilot stays per-project | not approved | |
| R13 | **AGPL posture** (OpenMontage, Immich, Cap, Recordly) | ledger #42; 04 §1 | never touch · run unmodified + learn, never copy code · allow modified internal use | Run unmodified and learn; never copy AGPL code into FliVideo | approved 2026-11-03 | **Middle option: run AGPL tools unmodified as separate programs, learn from their code, never copy it into FliVideo.** David, 2026-11-03 to flivideo-orch: "yes, record R13 as the middle option". |
| R14 | **OpenMontage stage-graph + revision-cap pattern** into pilot specs | ledger #16; 04 Q5, C6 | absorb ideas · add OpenMontage as external pipeline · none | Absorb ideas (pairs with R2's E4) | not approved | |
| R15 | **Teleprompter**: keep Teletubby; Textream | ledger #17; 04 Q4, C10–C11 | absorb Textream ideas · add Textream as a second prompter · replace Teletubby · none | Absorb ideas; add only after X5 | not approved | |
| R16 | **auto-editor** as a FliTools `cut.silence`-shaped tool | ledger #18; 04 C12 | absorb as tool · none | Absorb, after X6 | not approved | |
| R17 | **video-use** cut-pass ideas into FliCut | ledger #18; 04 C13 | absorb ideas · add beside FliCut · none | Absorb ideas, after X7 | not approved | |
| R18 | **Screen recording**: Cap and the rest vs FliCast | ledger #19; 04 C15–C16 | add Cap for Loom-style capture · none | None — FliCast stays; Cap only if a Loom-style job appears | not approved | |
| R19 | **Craft projects / FilmCraft** | ledger #22; 04 C5, C17 | watch · add when mature · none | Watch; re-check at their first stable release | not approved | |
| R20 | **Engine for a motion app**: HyperFrames vs Remotion | 04 C18, Q1 | HyperFrames · Remotion · both | HyperFrames first (Apache-2.0, editor components, already under overlays); Remotion stays available | not approved | |
| R21 | **Run the Level-4 experiments** in 05 | ledger #39; 05 | approve by ID (X1–X9) · batch X8→X2→X1 · none | Batch X8 → X2 → X1 (read-only/scratch, ~6 h, M2) after David finishes testing pilots | not approved | |

**Count**: 21 rows. Every ★ lean in `04` maps to a row (C1→R10, C2→R11, C6→R14, C7/C9→R12, C10→R15, C12→R16,
C13→R17, C15→R18, C5/C17→R19, C18→R20; Q1→R4, Q2→R9, Q3→R12, Q4→R15, Q5→R14). Leans of *none* for C3, C4, C8,
C11, C14, C16, C19 need no ruling unless David wants one.

**Recorded, not open** (David already said it in B686; listed so nobody reopens it): FliHub needs no alternative ·
Godot/Three.js/Blender are building blocks, not tools · FliTalent is for the future · this is a research exercise,
not a build commitment.
