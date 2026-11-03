---
type: reference
tags: [flivideo, ecosystem-research, candidate, B686, flicut]
description: "Is there an open-source alternative to FliCut (Gling/Descript-style cutting)? Light pass over repos already in upstream."
created: 2026-11-03
timestamp: 2026-11-03T12:30+07:00
---

# FliCut alternatives (light)

**Purpose**: Is there an open-source alternative to FliCut (Gling/Descript-style cutting)? Light pass over repos already in upstream.

**For Agents**: Research only (B686 B2, 2026-11-03). *Observed* = read in repo or via `gh api`; *Inference* and *Lean* are B2's and **not approved**. Anything unread is **UNVERIFIED**. Index: [../03b-capability-landscape.md](../03b-capability-landscape.md).

Verdict (inference): **no OSS match for a Gling/Descript-class transcript-first cutter that is also mature and agent-drivable**; the useful pieces are engines and tools. Prior study: `brains/video-editing-as-code/gling-ui-surface-map.md`, `ai-speech-editing-research.md`.

## auto-editor
- **Repo**: https://github.com/WyattBlue/auto-editor. **Licence**: Unlicense. **Stars / last commit**: 5,723★, pushed 2026-11-02 (`gh api`).
- **Agent surface**: deterministic CLI that removes silence/dead air, exports to Premiere/Resolve/Final Cut/Shotcut/Kdenlive timelines or renders (registry description, `repos.jsonl`); no AI/transcript. 
- **Security**: registered and scanned when added to upstream; this pass did not re-scan.
- **Two questions**: (1) elegant for silence cuts, not for meaning-based cuts. (2) yes, CLI, repeatable.
- **Outcome lean (not approved)**: *absorb* as a FliTools-style tool candidate; not a FliCut replacement.

## LosslessCut
- **Repo**: https://github.com/mifi/lossless-cut. **Licence**: GPL-2.0. **Stars / last commit**: 45,636★, pushed 2026-11-03.
- **Agent surface**: Electron GUI over FFmpeg stream-copy; no AI (registry). Agent surface not found; **UNVERIFIED**.
- **Security**: previously registered; not re-scanned here.
- **Two questions**: (1) excellent for lossless manual trims. (2) not shown.
- **Outcome lean (not approved)**: *none*.

## video-use (browser-use)
- **Repo**: https://github.com/browser-use/video-use. **Licence**: MIT. **Stars / last commit**: 30,431★, pushed 2026-10-08.
- **Agent surface**: Claude-Code-driven semantic cut engine using transcript word timestamps; never watches frames (registry description).
- **Security**: previously registered; not re-scanned here.
- **Two questions**: (1) closest to FliCut's transcript-first idea. (2) agent-native by design.
- **Outcome lean (not approved)**: *absorb ideas* (meaning-based cut passes); compare with FliCut's word-level cut before deciding.

## Gling / Descript
Commercial, not OSS. Gling project format and UI are studied in `brains/video-editing-as-code/gling-project-format.md` and `gling-ui-surface-map.md`. No OSS clone exists in `repos.jsonl`.
