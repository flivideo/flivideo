---
type: reference
tags: [flivideo, ecosystem-research, candidate, B686, screen-recording]
description: "Top-tier open-source screen recorders, citing prior brain work (Cap evaluation, Screen Studio study)."
created: 2026-11-03
timestamp: 2026-11-03T12:30+07:00
---

# Screen recording (FliCast) — top OSS

**Purpose**: Top-tier open-source screen recorders, citing prior brain work (Cap evaluation, Screen Studio study).

**For Agents**: Research only (B686 B2, 2026-11-03). *Observed* = read in repo or via `gh api`; *Inference* and *Lean* are B2's and **not approved**. Anything unread is **UNVERIFIED**. Index: [../03b-capability-landscape.md](../03b-capability-landscape.md).

Prior work, not redone: `brains/video-as-code/cap-evaluation.md`, `brains/screen-studio/`, `brains/video-editing-as-code/INDEX.md` (recorder questions).

## Cap
- **Repo**: https://github.com/CapSoftware/Cap. **Licence**: AGPLv3 app, MIT capture crates (brain); GitHub shows NOASSERTION. **Stars / last commit**: 24,288★, pushed 2026-11-03.
- **Agent surface**: brain: "most agent-native recorder found" (CLI/automations in v0.5.x). Not re-verified by B2.
- **Security**: scanned 2026-07-05 per brain; not re-scanned.
- **Two questions**: (1) Loom job: yes; not an Ecamm-style live switcher (brain). (2) yes via CLI.
- **Outcome lean (not approved)**: *none/add* for Loom-style capture; does not replace Ecamm/OBS scenes.

## Recordly
- **Repo**: https://github.com/webadderallorg/recordly. **Licence**: AGPL-3.0 per registry (GitHub: NOASSERTION). **Stars / last commit**: 35,931★, pushed 2026-10-24.
- **Agent surface**: Electron recorder + motion-graphics editor; agent surface **UNVERIFIED**.
- **Security**: registered; not re-scanned here.
- **Two questions**: (1) rival to Cap with PixiJS compositor. (2) unknown.
- **Outcome lean (not approved)**: *none*; reference only.

## open-recorder
- **Repo**: https://github.com/imbhargav5/open-recorder. **Licence**: Apache-2.0. **Stars / last commit**: 91★, pushed 2026-10-27.
- **Agent surface**: SwiftUI app over a Rust JSON-lines service; edit document with zoom regions on disk (brain INDEX line 182).
- **Security**: registry notes it ships a Claude Code release skill that auto-discovers if opened as a workspace; do not open it as a workspace.
- **Two questions**: (1) small but well-structured. (2) JSON-lines service is agent-friendly.
- **Outcome lean (not approved)**: *absorb ideas* (edit-document format). Low stars: fails "people like it" bar on its own.

## Screenize
- **Repo**: https://github.com/syi0808/screenize. **Licence**: Apache-2.0. **Stars / last commit**: 618★, pushed 2026-05-22; development paused 2026-05-22 (registry).
- **Agent surface**: writes the Screen Studio polyrecorder event-log format (brain).
- **Security**: registry: its `CLAUDE.md` carries an auto-execute directive; scanned, see `brains/security/scan-log.md`. Never open it as a workspace.
- **Two questions**: (1) useful format reference. (2) not maintained.
- **Outcome lean (not approved)**: *none*; format reference only.
