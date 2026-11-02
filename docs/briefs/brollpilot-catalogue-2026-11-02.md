---
created: 2026-11-02
timestamp: 2026-11-02T09:55+07:00
---
# Brief: B-Roll Pilot — minimum visual catalogue (2026-11-02)

**From:** `flivideo-orch`. **To:** `brollpilot-dev`. **Report to `flivideo-orch` by name after EACH unit, then idle until acked.**
**Worktree:** create `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/br-catalogue`, branch `br-catalogue`, from main `3f6804e`.
Lane: `modules/broll-pilot/**`. Do not touch storypilot or overlay-pilot.
**Source (read the named sections in full):** Captain's Log B682 (David's voice log, 2026-11-02 06:33) and its dossier B683, on disk at `/Users/davidcruwys/dev/ad/flivideo/docs/specs/b683-dossier-2026-11-02.md`. Fetch either with the captains-log MCP `capture_get` if you need David's exact words. Sections 9–12, 24 (boundaries), 27.

**Why:** first real use is the Overlay Pilot video's screenshots and demo recording. Do not build the full brand B-roll studio.

## Unit 1 — audit, then a one-page plan (no code)
- What B-Roll Pilot already does (module + `flivideo:broll-pilot` skill).
- Joy's B-roll application: locate it (`jump` / `~/.config/appydave/locations.json`), read its metadata model, filtering,
  grouping, and how it describes images and videos. What to reuse.
- FliHub: status of the "mark this recording as B-roll" capability (David: "I'm getting a new capability built into FliHub").
- Local vision / frame-description tooling already on this machine (FliTools? ffmpeg scene detect?).
- Plan: the smallest build for ingestion (clipboard paste, drag-drop, FliHub reference by provenance, no copy), describe +
  tags + human override (human wins), async background enrichment, simple grouping. Report it; wait for ack.

## Unit 2 — build the plan orch acks
Gates: typecheck, lint, `npm test`, targeted broll-pilot e2e only. UX pass. Commit, push. Do not merge or restart.
