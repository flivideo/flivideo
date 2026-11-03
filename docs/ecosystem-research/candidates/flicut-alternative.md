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

## Experiment X6 — 2026-11-03

**Verdict: PASS on silence cuts (comparable, one CLI call, ~0.1 s per take). Does not cover FliCut's filler/bad-take cuts.** 05's pass test: "comparable or better silence cuts in one CLI call".

**Setup** (M4, ~5 min): auto-editor **29.3.1** (`uv venv` + `uv pip install auto-editor` in `~/dev/upstream/scratch/X6/`; the wheel downloads the release binary `auto-editor-macos-arm64` from github.com/WyattBlue/auto-editor on first run). Unlicense. Input: copies / read-only reads of d01 takes; FliCut cut read from `fli.cut.flivideo-tour.json` (cutParams: silences + fillers on, pause 0.5 s, padding 0.15 s).

**Take `03-1-flistudio.mov` (29.24 s)**
| | cuts | kept |
|---|---|---|
| FliCut | 0–0.53 s, 17.11–17.59 s | 28.23 s (2 ranges) |
| auto-editor `--edit audio:threshold=0.04 --margin 0.2s --export v1` | 0–0.52 s, 17.17–17.57 s (+1 tiny cut) | 28.20 s (3 ranges) |

Same two silences found, boundaries within ~0.06 s. Margin matters: `--margin 0.1s` over-cuts (12 ranges, 26.8 s kept); `0.2s` matches. **No equivalent of FliCut's "pause ≥ 0.5 s" parameter** — it cuts every sub-threshold gap not covered by margin, so tiny extra cuts appear.

**All 20 d01 takes** (same settings): FliCut kept total **526.0 s**, auto-editor **538.0 s**; per-take |difference| summed 24.5 s; 10/20 takes within 0.5 s. Biggest gaps: `04-1-kybernesis` (FliCut 34.1 s vs auto 41.1 s), `05-2-flicast`, `02-2-overview` — FliCut also removes filler words and bad takes, which auto-editor (audio-level only) cannot see; `03-4-flistudio` and `06-1` the reverse (auto cuts more). Caveat: this is count/duration comparison, **not** a listen test for false cuts — nobody has played the outputs; the FliCut side includes filler cuts so the two are not like-for-like.

**Evidence**: `~/dev/upstream/scratch/X6/` (`flicut-03-1.json`, `auto.v1.json`). Output of `--export v1` is JSON `chunks [startFrame, endFrame, speed]`, speed 99999 = cut; the timebase is auto-editor's own (24.93 fps for this file), so a wrapper must convert frames → seconds.

**What FliStudio/FliTools would need** (Inference): a `cut.silence` verb that shells out to `auto-editor --export v1` and converts chunks to seconds; expose it as a *second proposal lane* in FliCut, never replacing its transcript-based cuts. Value is as a cheap no-transcript pre-pass; for a take with a transcript FliCut already does more.
