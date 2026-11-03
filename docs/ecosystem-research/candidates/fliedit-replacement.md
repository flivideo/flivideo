---
type: reference
tags: [flivideo, ecosystem-research, candidate, B686, fliedit]
description: "Could someone else's timeline editor replace FliEdit and be driven by agents? Kdenlive/MLT, libopenshot, Shotcut/MLT, FilmCraft."
created: 2026-11-03
timestamp: 2026-11-03T12:30+07:00
---

# FliEdit replacement candidates

**Purpose**: Could someone else's timeline editor replace FliEdit and be driven by agents? Kdenlive/MLT, libopenshot, Shotcut/MLT, FilmCraft.

**For Agents**: Research only (B686 B2, 2026-11-03). *Observed* = read in repo or via `gh api`; *Inference* and *Lean* are B2's and **not approved**. Anything unread is **UNVERIFIED**. Index: [../03b-capability-landscape.md](../03b-capability-landscape.md).

## 1. Kdenlive + MLT (one engine, two layers)
- **Repo**: https://github.com/KDE/kdenlive (clone `020a578`), https://github.com/mltframework/mlt (clone `7a3319f`); both at `/Users/davidcruwys/dev/upstream/repos/{kdenlive,mlt}`.
- **Licence**: Kdenlive GPL-3.0; MLT LGPL-2.1 (GitHub API). Linking MLT from our code is LGPL; embedding Kdenlive code is GPL.
- **Stars / last commit**: Kdenlive 6,038★, pushed 2026-11-03. MLT 1,870★, pushed 2026-10-29 (`gh api`, 2026-11-03). Both active, not archived.
- **Agent surface**: *Observed* — MLT is a C framework with the `melt` CLI (`mlt/src/melt/melt.c`) and SWIG bindings for Python/Node/Java/etc. (`mlt/src/swig/`), and an XML project format. Kdenlive's `.kdenlive` file is MLT XML plus extra data, and "MLT is able to directly render Kdenlive project files" (`kdenlive/dev-docs/fileformat.md`). Kdenlive has a command-line render path (`kdenlive/src/main.cpp:482`). There is no JSON-RPC/MCP server and no GUI automation API found. So the practical agent route is: **edit the XML / MLT API, render headless with `melt`**, not "drive the Kdenlive window". **UNVERIFIED**: how stable the XML is across Kdenlive generations (the doc lists several generations).
- **Security**: *Observed* (scoped scan, `brains/security/scan-log.md`): 0 injection-phrase hits; MLT ships `AGENTS.md` and `CLAUDE.md` (read, ordinary build/test notes). Source/binaries not audited. Media decoders in C/C++ parse untrusted files (general class of memory-bug risk); not assessed. Nothing was built or run.
- **Two questions**:
  1. *Does it solve the production problem elegantly?* Mature general NLE (multi-track, effects, proxies). Strong for the generic timeline FliEdit approximates; no transcript-first or overlay-aware model.
  2. *Can agents drive it safely?* Only via XML/MLT API and headless render, not via the GUI. Safe-ish (no network service), but we would own an XML editing layer.
- **Outcome lean (not approved)**: *absorb* MLT as a possible render/assembly engine behind FliEdit; *replace* is not supported by evidence (no agent-drivable timeline UI). *none* for Kdenlive as a whole.

## 2. libopenshot (OpenShot's library)
- **Repo**: https://github.com/OpenShot/libopenshot (clone `528ebb1`).
- **Licence**: LGPL-3.0 (GitHub API).
- **Stars / last commit**: 1,582★, pushed 2026-11-03.
- **Agent surface**: *Observed* — C++ library with Python/Ruby/Java and Godot bindings (`libopenshot/bindings/`). Clips/timeline are objects with animated curves (`src/AnimatedCurve.*`, `Clip.cpp`). **UNVERIFIED**: JSON timeline import/export API (the OpenShot app uses one; not confirmed in this repo's README). Library only; the editor is a separate repo (openshot-qt, not cloned).
- **Security**: Scoped scan CLEAN (0 hits). FFmpeg-based decoding: same media-parsing caveat. Not built or run.
- **Two questions**:
  1. *Elegant?* A library, not an editor — it solves "render a timeline from code", which FliEdit already does its own way.
  2. *Agent-drivable?* Yes as a Python library; no ready editor UI to embed.
- **Outcome lean (not approved)**: *none* for now; a possible alternative render backend, lower priority than MLT.

## 3. Shotcut (MLT-based) — `gh api` only, not cloned
- **Repo**: https://github.com/mltframework/shotcut. **Licence**: GPL-3.0. **Stars / last commit**: 15,582★, pushed 2026-11-02.
- **Agent surface**: **UNVERIFIED** (not cloned; same MLT engine and XML as above, so same conclusion as Kdenlive).
- **Security**: not assessed (no clone, per the 10-clone cap and scope).
- **Two questions**: not answered beyond "same engine as Kdenlive; a second GUI over MLT".
- **Outcome lean (not approved)**: *none*.

## 4. FilmCraft (ArtCraft's Rust NLE) — cited, not redone
- **Repo**: https://github.com/storytold/filmcraft (clone on M4 only). **Licence**: MIT OR Apache-2.0 (per `brains/artcraft/security-audit.md`). **Stars / last commit**: not fetched here (**UNVERIFIED** for today); status "in development" per `brains/artcraft/apps.md`.
- **Agent surface**: Brain claims every Craft app is drivable by CLI, JSON control channel or MCP, control servers on localhost only (`brains/artcraft/apps.md`, `security-audit.md`). Not re-verified in code by B2 (ArtCraft clones are M4-only).
- **Security**: seven Craft apps "low concern on this read"; parent ArtCraft app needs care (see brain).
- **Two questions**: elegant — unproven (in development). Agent-drivable — claimed, not verified by B2.
- **Outcome lean (not approved)**: *none now*; **watch**. The brain already notes "strong overlap in goal, opposite approach" with FliCut/FliEdit.

## Roll-up
No candidate is both a mature timeline editor and agent-drivable through a documented API. HyperFrames Studio is the closest agent-drivable editor surface but is composition-oriented (see [hyperframes-as-editor.md](hyperframes-as-editor.md)). B3 should treat "replace FliEdit" as an open design question rather than a finding.
