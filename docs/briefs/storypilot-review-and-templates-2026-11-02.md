---
created: 2026-11-02
timestamp: 2026-11-02T09:55+07:00
---
# Brief: Story Pilot — review keys, Reader keys, templates band, recorded-segment cards (2026-11-02)

**From:** `flivideo-orch`. **To:** `storypilot-dev`. **Report to `flivideo-orch` by name after EACH unit, then idle until acked.**
**Worktree:** create `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/sp-review`, branch `sp-review`, from main `3f6804e`.
Lane: `modules/storypilot/**` (+ extension-core/sync if keys must be shared). Do not touch overlay-pilot or broll-pilot (other workers).
**Source (read the named sections in full):** Captain's Log B682 (David's voice log, 2026-11-02 06:33) and its dossier B683, on disk at `/Users/davidcruwys/dev/ad/flivideo/docs/specs/b683-dossier-2026-11-02.md`. Fetch either with the captains-log MCP `capture_get` if you need David's exact words. Sections 4, 6, 7. Also David's held asks: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/_held-david-2026-11-02.md` §1–2.

**Why today:** David wants the Overlay Pilot and Story Pilot scripts ready today so Tuesday is narration only.

## Unit 1 — keyboard (small, ship first)
- Listen: speed up / slow down / play-pause use **the same keys as the FliStudio/FliHub video player** (find them; share, don't copy).
  David: "they need to be the same keyboard shortcuts."
- Reader: a key to step to the next/previous paragraph or card; David suggests reusing the speed keys' pattern. Name your choice.
- Tooltips name the shortcut.

## Unit 2 — templates band (dossier §4)
- Investigate first: what storytelling templates, brand-voice and hook/marketing instructions already exist (codebase, `docs/`,
  brains, old storyline-app at `/Users/davidcruwys/dev/ad/flivideo/storyline-app`). Report what exists before building.
- Show them at the top of the sources, visually separate (soft border/tint), editable, labelled **Global** (e.g. storytelling)
  or **Brand** (e.g. brand voice). Not attached to the video; not counted as sources; not placed by Prep.

## Unit 3 — recorded-segment card (dossier §6)
- New source type: a recorded segment (a FliHub recording's transcript, e.g. David's Overlay Pilot demo). Its words are
  **concatenated into the script verbatim, never re-synthesised**; the script alternates written narration and recorded blocks.
- Listen plays the recorded block's real audio (or marks it "recorded — not voiced"); name your choice.

## Gates (each unit)
typecheck, lint, `npm test`, targeted storypilot e2e only (load is high). UX pass as you go. Commit, push. Do not merge or restart.
