---
created: 2026-11-02
timestamp: 2026-11-02T09:55+07:00
---
# Brief: Snappy — research + spec page, no code (2026-11-02)

**From:** `flivideo-orch`. **To:** `snappy-rsch`. **Report to `flivideo-orch` by name, then STOP.**
**Source (read the named sections in full):** Captain's Log B682 (David's voice log, 2026-11-02 06:33) and its dossier B683, on disk at `/Users/davidcruwys/dev/ad/flivideo/docs/specs/b683-dossier-2026-11-02.md`. Fetch either with the captains-log MCP `capture_get` if you need David's exact words. Sections 13–17, 25 (Snappy questions), 27. David named it **Snappy** (not Fli-anything).

**What it is:** a native macOS region-based screenshot tool (not screencasting). Named regions (project- or brand-scoped,
~10–15 max), hotkeys to cycle regions left/right, a visible wireframe outline of the active region, instant capture, optional
countdown, timed stop-motion capture; no library of its own: it **sends** each capture (with region + group names) to an
endpoint, first receiver B-Roll Pilot. Describing/tagging happens in B-Roll Pilot, not Snappy. Likely Rust; CLI, TUI or service open.

## Do
1. Find David's past screen-capture tools (Ruby, Python, others) across `~/dev`; what each did, what to keep.
2. macOS APIs for region capture, overlays and global hotkeys (ScreenCaptureKit, CGWindow, etc.), permissions; Rust crates vs a
   thin Swift layer. Use current docs (context7 / web), cite them.
3. Answer every Snappy question in dossier §25 with a recommendation.
4. Write the spec with `dev-team:spec-page` (AppyDave brand, light only) at
   `/Users/davidcruwys/dev/ad/flivideo/docs/specs/snappy-spec-2026-11-02.md` (+ html), decisions for David numbered with recs.
   Commit + push in the flivideo repo. Report the path and the decisions. Do not start a repo or write code.
