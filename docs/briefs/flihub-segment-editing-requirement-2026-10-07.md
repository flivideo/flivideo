# FliHub — segment editing: replace, insert, reorder (validated requirement)

**Purpose**: A validated requirement for FliHub, ready for the Buzz coding team (D07 run 2, job 2 — the "FliHub, from David's other conversation" slot). It covers placeholder segments, re-recording, inserting and reordering segments inside a chapter.
**For Agents**: Orc sizes and slices this; Coder builds; Tester verifies on an isolated temp project. The research behind it is done — read it, don't redo it.
**Status**: VALIDATED by David, 2026-10-07 (flivideo-orch session). Written by `flivideo-orch`.

## Sources (read these, in this order)

| What | Where |
|---|---|
| The assessment (today's behaviour with file:line evidence, the model, safety rules, phased plan) | `/Users/davidcruwys/dev/ad/flivideo/docs/flihub-rerecord-placeholder-assessment.md` |
| Its visual page | https://claude.ai/artifact/1aLZPeUtgWRwmcshYYQmJ5 |
| The ruling in the brain | `/Users/davidcruwys/dev/ad/brains/video-as-code/project-structure-reading-list.md` § "Ruling 2026-10-07" |
| FliHub repo | `/Users/davidcruwys/dev/ad/flivideo/flihub/` (read its `CLAUDE.md` and `docs/AGENT-NOTES.md` first) |

## David's model (validated — the vocabulary is part of the requirement)

- **Takes live in the inbox.** David often records 5–10 bad takes before accepting one. They stay in the inbox and are deleted there.
- **Recordings hold segments.** A chapter is one or more **sequential segments**, each a clean piece; all of them play, in order, with no editing. Never call a recording a "retake" in the UI.
- **Two normal inbox exits.** (a) Pick the one good take → the rest are deleted (~60%). (b) He forgot to send a good take and moved on → he sends **several** takes in as consecutive segments, then deletes the rest.
- **The case this feature is for:** the shape of a chapter needs to change after segments are already in recordings. Three operations, **one feature**:
  1. **Replace** (~90% of cases) — a segment was a deliberate **placeholder**, or is found wrong later. Re-record it, and possibly the segments after it.
  2. **Insert** — segments 1 and 2 are fine, but something should go between them.
  3. **Reorder** — segments are out of order; move one up or down.

## Requirements

| # | Requirement | Acceptance (Tester checks on a temp project, never a real one) |
|---|---|---|
| R1 | **Inbox "Lands as"** beside Seq: *next* (default, today's behaviour) · *replace 06-1* · *insert before 06-2*. The server owns all numbering. | Each mode produces the expected file names; *next* is unchanged from today. |
| R2 | **Replace**: old segment + its transcripts, engine copies and image assets go to `-trash/`; the new take takes the same number. | Old files are in `-trash/`; new `06-1-<slug>.mov` exists; its transcript is queued. |
| R3 | **Insert**: segments from the insert point shift up one; the new take lands at the insert point. | 06-1, 06-2 → insert before 06-2 → 06-1, NEW = 06-2, old 06-2 = 06-3, transcripts follow their videos. |
| R4 | **Reorder**: move a segment up/down within its chapter (buttons; drag is optional). | 06-1, 06-2, 06-3 → move 06-3 up → 06-1, (old 06-3) = 06-2, (old 06-2) = 06-3; transcripts follow. |
| R5 | **Delete and close up**: delete a segment; later ones close the gap. | Delete 06-2 of three → 06-1, old 06-3 = 06-2; deleted files are in `-trash/`. |
| R6 | **Send several**: tick several inbox takes → they land as consecutive segments in the order picked; then "delete the rest". | Two takes picked → 06-3, 06-4; the remaining inbox takes go to trash only on confirm. |
| R7 | **Placeholder flag** on a segment (metadata in FliHub state, **not** a filename tag): badge in the recordings list, a "N to re-record" count, auto-clears when that segment is replaced. | Mark → badge + count; replace → cleared; file name never changes. |
| R8 | **One guarded operation** under R2–R5: check every affected file first (transcribing? referenced by a FliCut cut or FliStudio cut draft? collision?) and refuse the whole operation with a plain reason; rename two-phase (temp names) so no half-renumbered chapter can exist. | A refused op changes nothing on disk; a referenced segment returns the reason naming the cut. |
| R9 | **Journal + undo that survives a restart**: each op records moves and trashed files with origins; undo replays it in reverse, restoring from trash. | Op → restart server → undo → disk identical to before. |

**Out of scope for this job:** FliCut and FliStudio *following* a renumber (assessment Phase 4). R8 protects them by refusing instead. The FliStudio wording fix (drop the `latest` take flag, say "segments" not "retakes") is a separate small FliStudio ticket.

## Suggested slice for the one-day slot (Orc's call)

Build the **server operation first**: R8 + R9, with R2–R5 as modes of it, all covered by tests on a temp project. That is the shared core — replace, insert, reorder and close-up are the same two-phase renumber. Then UI in this order: R1 (inbox Lands as) → R7 (placeholder) → R4 buttons → R6. At the 4-hour check, cut UI, not the guard or the journal.

## Constraints

- Work in a **git worktree**; land only green commits. David may have FliHub running at :5100 from the live checkout.
- **Never touch a real video project.** Tests use a temp dir; FliHub's destructive routes act on real folders (uat2 `02-skill-candidates.md` E9).
- FliHub's `npm test` runs vitest in watch mode — use the one-shot command (uat2 CT-0079).
- Don't restart David's FliHub. New state fields follow the three-edit rule in FliHub `docs/AGENT-NOTES.md`.
- Commit and push (stage by name). Report to `flivideo-orch` when landed.
