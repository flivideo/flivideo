---
created: 2026-11-03
timestamp: 2026-11-03T19:45+07:00
---
# Brief: Story Pilot W0 — characterization tests (the safety net), tests only (2026-11-03)

**From:** `flivideo-orch` (Swagger). **To:** `storypilot-w0-dev` (**M2**, cwd `/Users/davidcruwys/dev/ad/flivideo`). Report to `flivideo-orch`.
**Go:** David via `flivideo-roamy`, ~19:40. **Machine: M2** — code (tests only), standing ruling; no Story Pilot work in progress on the M4.

## Why
Plan: "Story Pilot: Document Islands, one plan" — https://claude.ai/artifact/VPGrG5kVDL1zM32Bxe5x8x (read it via the
claude-artifacts `read_artifact` tool if available; otherwise rely on the design note). Design note:
`/Users/davidcruwys/dev/ad/flivideo/docs/briefs/storypilot-captains-log-mapping-2026-11-03.md` — `git pull` flivideo, read the
last three sections. Before any Story Pilot change (W1 islands, W2 Reader, W3 instructions, W4 rerun), pin TODAY's behaviour.
Tests describe what the code does now, **including known-bad behaviour**, each marked e.g.
`// KNOWN BUG (W1): skill text counted as David's turn`. **Fix nothing.**

## Setup (M2, never the live checkout)
`git -C ~/dev/ad/flivideo/flistudio fetch origin && git -C ~/dev/ad/flivideo/flistudio worktree add ~/dev/ad/flivideo/flistudio-worktrees/storypilot-w0 -b storypilot-w0 origin/main`, `npm install` there.
Note: `show-filter-dev` is also working on the M2 in `flistudio-worktrees/show-filter-persist` (client StatusList) — different
files; don't touch its worktree.

## Scope — all in `flistudio/modules/storypilot` (+ `e2e/`)
1. `story.source.read` for EVERY island kind: session, capture, dossier (0 tests today), note, artifact (claude.ai URL), link,
   broll. Assert raw vs synth layers, provenance, and what each shows when its canonical is missing (session transcript not on
   this machine; dossier path missing).
2. The 60k cut: `READ_LIMIT` in `server/story.ts`. A >60,000-char session gives `truncated: true`, the first 60k, and the real
   char count (today only `truncated:false` is exercised).
3. ownTurn filter: a user-role message starting "Base directory for this skill:" is currently kept as a David turn — pin it as
   **KNOWN BUG (W1)**. Also pin that `pasted_content`, `cross-session-message`, `[Image #n]` and `tool_result` are dropped.
4. Settings resolution across defaults › creator › brand › series › video, including the "from" level per value and FIELDS level
   rules (`settings.test.ts` has 5 today). Templates: global/brand merge, hidden shipped default, and that `story.brief`
   carries templates.
5. ONE browser e2e on the Reader: open a source card from each of capture, session and dossier; assert badge text, the raw/synth
   chips and "Where it came from".
Fixtures: **synthetic only, never real transcripts.** Include one >60k session and one with an injected skill turn. Mirror d13's
shapes (resource ids/kinds from `v-appydave/d13-overlay-pilot/fli.resources.json` are fine as shapes — copy shapes, not content).

## Out of scope
Any production code change; refactors; coverage for its own sake; restarting FliStudio; merging.

## Gate (yours)
Record test counts per file BEFORE you start. Then: full unit suite + `npm run typecheck` green; the new e2e green (run only that
spec, never the full e2e suite); all pre-existing tests still green. Commit on `storypilot-w0`, **push the branch**.
STOP and report to `flivideo-orch`: branch + shas; test counts before → after per file; every KNOWN BUG pinned (one line each);
anything the plan/design note got wrong (e.g. a kind that doesn't exist, a field named differently). Orch reproduces on the M4
and merges ff-only.
