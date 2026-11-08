---
type: reference
tags: [flivideo, ecosystem-research, candidate, concat, mcp, editor]
description: "Concat: a free, local-first video editor that agents can drive through a built-in MCP server. A possible CapCut replacement. AGPL, study only."
created: 2026-11-08
timestamp: 2026-11-08T15:00+07:00
---

# Concat: an editor agents can drive

**Purpose**: Note Concat as an outside editor worth watching: agents can cut video in it through MCP, and it may replace CapCut.

**For Agents**: Research only (2026-11-08). *Observed* = read via `gh repo view` / `gh api` (README, `docs/MCP.md`); nothing was cloned, built or run. *Lean* is not approved. Index: [../03b-capability-landscape.md](../03b-capability-landscape.md).

- **Repo**: https://github.com/jub0t/Concat. Registered in the upstream registry (`concat`), **not cloned**.
- **Licence**: AGPL-3.0 (`gh repo view`). **Study only / clean-room.** Never copy or port its code into FliVideo.
- **Stars / last commit**: about 15.4k★, pushed 2026-11-08. Latest release v0.2.9 (beta), 2026-11-05.
- **What it is** *(Observed, README)*: free, local-first video editor. Native Rust engine with a GPU compositor. macOS, Windows, Linux, Android, iOS (sideloaded). Local Whisper auto-captions, text-to-speech and voice cloning, background removal, keyframes with a curve editor, about 100 effects, multi-track and multi-timeline, voice cleanup, export up to 4K60 (H.264, HEVC, AV1). No account, no watermark, no upload.
- **Agent surface** *(Observed, `docs/MCP.md`)*: built-in MCP server, started with `concat --mcp`, plus a JSON-RPC API for scripts. Tools cover projects, reading the timeline, importing media, cutting, trimming, splitting, moving, speed, titles, captions, keyframes, effects, frame grabs and export. Two modes: through the open window (Automation setting on) or headless with no window. Files are written only under the home folder unless `CONCAT_MCP_ROOTS` allows more. An agent cannot yet edit the project you have on screen ("live mode" is planned, issue #337).
- **Security**: not scanned (not cloned). If it is ever cloned, run the `upstream:upstream-add` scan first. Media decoders parse untrusted files; not assessed.

## Why it matters

An editor an agent can drive through MCP, and a possible CapCut replacement.

## Two questions

1. *Does it solve the production problem elegantly?* For a general timeline edit with captions, yes on paper. It is beta.
2. *Can agents drive it safely?* It is built for it: MCP tools, project locks, a home-folder write fence. **UNVERIFIED** until someone runs it.

## Outcome lean (not approved)

*Watch and trial* as an outside tool, used as an app (run it, drive it through MCP). Do not depend on its code (AGPL). Compare with FliEdit in [fliedit-replacement](fliedit-replacement.md).
