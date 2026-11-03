---
type: plan
title: "05 · Research experiments (Level 4 — planned, not run)"
description: "Nine bounded experiments that would settle the open leans in 04: question, method, machine, timebox, pass/fail, which register row it feeds. None has been run; each needs David's go."
tags: [ecosystem-research, flivideo, experiments, level-4, hyperframes, mlt, immich, textream, auto-editor, B686, B687]
created: 2026-11-03
timestamp: 2026-11-03T13:45+07:00
status: planned
---

# 05 · Research experiments

> **PLANNED, NOT RUN.** B687 §5.2: "Planning these experiments does not authorise implementing them." Each one
> needs its own go from David (register row R21). None of them edits an app repo.

**Purpose**: Turn every "UNVERIFIED" that blocks a lean in `04` into a small, timeboxed test with a clear pass/fail,
so a decision can be made on evidence rather than on reading code.

**For Agents**:
- Run an experiment only after David approves it by ID (X1…X9). Run on the **M2** in a scratch folder under
  `~/dev/upstream/scratch/<id>/` (or the session scratchpad), never inside `flivideo/<app>/`.
- Use registered clones only (`~/dev/upstream/repos/…`); new clones go through `upstream:upstream-add`.
- Test media: copies of an existing finished project's files, never the originals; nothing from a project David is
  editing.
- Write the result into the candidate file (`candidates/<slug>.md`, a dated "Experiment" section) and flip the
  matching row in `06` from open to *evidence in*. The decision stays David's.

---

| ID | Settles | Question | Method (short) | Machine | Timebox | Pass if | Fail means |
|---|---|---|---|---|---|---|---|
| **X1** | Q2 E-C, C1 replace | Can HyperFrames Studio edit *footage*, not just compositions? | Load a copy of a 15–20 min talking-head + 5 B-roll clips into a HyperFrames project; via CLI `timeline` verbs: cut, ripple-delete, move, trim; add a music bed + duck; render | M2 | 3 h | All five operations via CLI `--json`, render matches, Studio stays responsive on 20 min | FliEdit stays the footage editor (E-A) |
| **X2** | C1 add | What does `studio-server` expose and to whom? | Start studio-server; `lsof -iTCP` for bind address; read the auth middleware; curl a mutation from another tailnet host | M2 | 1 h | Binds localhost by default, or takes a token | Needs a proxy/token wrapper before it can sit in FliStudio |
| **X3** | Q2 E-B, C2 | Can an FliEdit edit file render through MLT? | Hand-translate one `fli.edit.<name>.json` (copy) into MLT XML; render with `melt` headless; compare to FliEdit's render (duration, frame diff at 5 points) | M2 | 3 h | Same output within a frame; render time ≤ FliEdit's | MLT not worth the translator |
| **X4** | Q3 B-B, C7 | Can Immich hold per-media-type tags and a project view? | Docker-compose Immich on M2 (tailnet only); import 50 B-roll clips; create typed tags (shot type, subject, brand) and albums per project via API with a scoped key; query "brand X, shot type Y" | M2 | 4 h | Typed tags (or a workable convention) + API query + project albums all work; disk + RAM recorded | Build Dam'It's own store (B-A) |
| **X5** | Q4, C10 | Is Textream's Director port safe and drivable? | Run Textream on the M4 (macOS app); enable Director; push a Story Pilot script copy over HTTP/WebSocket and via `textream://`; check bind address + auth | M4 | 1.5 h | Script push + word progress readable by a script; listener restricted to trusted network | Absorb ideas only; no add |
| **X6** | C12 | Does auto-editor's silence cut beat or match FliCut's? | Run `auto-editor` on a copy of a raw take FliCut already cut; compare cut list, kept duration, false cuts | M2 | 1.5 h | Comparable or better silence cuts in one CLI call | No tool added |
| **X7** | C13 | Do video-use's meaning-based passes add something FliCut lacks? | Run video-use on the same take as X6 with its transcript; compare proposals against FliCut's final cut | M2 | 2 h | ≥ 2 cut ideas FliCut missed that David would keep | Ideas noted, nothing absorbed |
| **X8** | R1, R3, Q1 | What do the five triggers (03 T1–T5) read today, as numbers? | A read-only script over a `git archive` of FliStudio origin: per-module LOC, query/command split, spawn sites, files written outside `fli.<ext>`, `host.app` calls (03's E3 report, run once, not committed to FliStudio) | M2 | 1.5 h | A table David can read; the Overlay Pilot reading is clear | Measurement method needs rework |
| **X9** | C3 | Does libopenshot have a usable JSON timeline API? | Read `libopenshot` `Timeline::Json`/`SetJson` and the Python binding; build in scratch; load/save one timeline | M2 | 1.5 h | Round-trip JSON timeline from Python | libopenshot stays *none* |

**Suggested order if David approves a batch** (inference): **X8 → X2 → X1** (the Q1 critical path, all read-only
or scratch-only, ~6 h) · then **X4** (largest, needs a Docker yes) · **X5, X6, X7** any time · **X3, X9** only if
Q2 moves past E-A.

**Not experiments** (no test would change the lean): QPrompt, Shotcut, LosslessCut, Recordly/open-recorder/Screenize,
Motion Canvas/Manim, ResourceSpace — all *none* in 04.
