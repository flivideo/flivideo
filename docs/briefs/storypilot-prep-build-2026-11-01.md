---
created: 2026-11-01
timestamp: 2026-11-01T20:10+07:00
---
# Brief: Story Pilot Prep — angle, source stamps, ordered list, and the `flivideo:storypilot-prep` skill (2026-11-01)

**From:** `flivideo-orch` (Swagger). **To:** `storypilot-dev` (tmux `storypilot-dev`). **Report to `flivideo-orch` by name, then stay idle until acked.**
**Go:** David, 2026-11-01 ~20:05 +07: "Approved." All five recommendations accepted.

## Read first

- The approved spec: `/Users/davidcruwys/dev/ad/flivideo/docs/specs/storypilot-prep-spec-2026-11-01.html`
  (artifact https://claude.ai/artifact/Afe683M3j1vj42RUjMDJ4S). §03 angle, §04 what the skill does + the autonomy table,
  §05 the UI mock, §06 how it's built.
- Background: `/Users/davidcruwys/dev/ad/flivideo/docs/specs/curation-inventory-2026-11-01.md`,
  `/Users/davidcruwys/dev/ad/flivideo/docs/specs/session-curation-asks-2026-11-01.md`.
- Listen's staleness pattern (your own code): `modules/storypilot/server/audio.ts` (per-paragraph hash).

## The five approved decisions (binding)

1. An **`angle`** field per video, written **only by David**. The skill may propose up to three, labelled as proposals; it never writes the field. Angle can be marked **provisional** ("proof pending") and carries a date.
2. Name: **`flivideo:storypilot-prep`**, in the FliVideo plugin (`/Users/davidcruwys/dev/ad/appydave-plugins/flivideo/skills/`), never the legacy `appydave` plugin.
3. It runs **from Claude Code now**; no in-app "run" button in this build.
4. Autonomy: place, order and refresh freely (proposals, undoable); **removal and angle are David's**; never rewrite the script.
5. Build briefs about the tool are set aside as **"about the tool, not the story"** by default.

## Unit 1 — data contract + UI (FliStudio, `modules/storypilot/**`)

Worktree: `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/rail-v2`. Start a new branch **`prep-v1` from main `58dcf2d`**.

- **Data in story.json:** `angle { text, provisional, setAt }` (David-only: the UI edits it; no agent-facing write verb, or a verb that refuses unless called from the UI, name your choice); per source: `placement { section | "suggest-remove" | "about-tool", order, reason, placedBy, placedAt }`, `kind: raw | synth`, `madeFrom` (for synth), and a **source stamp** `{ lastMessageAt, hash }`.
- **Verbs** (extend `story.*`): write placement/order/reason in one call (for the skill), propose angles (stored as proposals, separate from `angle`), compute staleness (the source has grown since its stamp → out of date). Flag anything that touches the shared `fli-core` contract **before** changing it.
- **UI** per §05: the angle line at the top (with provisional pill, edit in place), a short ordered list under it (number, title, raw/synth tag, one-line reason), an **out of date — refresh** pill, a **contradicts angle** flag, a collapsed "+N about the tool · N suggested for removal" row, cards stay below. Run it through a UX pass as you go. Script sheet keeps its 960px cap.
- Gates: typecheck, lint, `npm test`, targeted e2e only (one new spec for the ordered list + angle edit + out-of-date pill, plus the existing storypilot specs). **Do not run the full suite** (machine is overloaded).
- Commit, push `prep-v1`. **Report to orch after Unit 1** with the verb contract pasted in. Do not merge. Do not restart FliStudio.

## Unit 2 — the skill (after orch acks Unit 1)

- Create `flivideo:storypilot-prep` with the `skill-creator` skill, in `/Users/davidcruwys/dev/ad/appydave-plugins/flivideo/skills/storypilot-prep/`.
  Pull appydave-plugins first; commit only your skill folder; push to main.
- It reads a project's attached sources, places/orders them against the angle (or by time, saying it had no angle), marks raw/synth,
  stamps each synthesis, refreshes out-of-date ones when run, flags sources that contradict the angle, and writes via the Unit 1 verbs.
  Reuse patterns: `sesh:session-archaeology` / `abridge` for reading sessions, `steno:fact-sheet` refresh mode for re-synthesis.
- Prove it on **D19** (`/Users/davidcruwys/dev/video-projects/v-appydave/d19-storypilot-video/`, has David's angle verbatim) against a FliStudio
  running your branch on non-live ports, never the live :7150/:7151. Do not write to D19's live story.json; use a copy.
- Report: skill path + commit, the D19 proposed order, what you could not verify.

## Lane and limits

- Story Pilot and the new skill only. Do not touch FliTools, other modules, or the live checkout `/Users/davidcruwys/dev/ad/flivideo/flistudio`.
- Do not merge, do not restart FliStudio; orch gates and merges.
- Questions go to `flivideo-orch` with a recommendation; never wait on David.
