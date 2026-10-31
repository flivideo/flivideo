# Brief: B-roll Pilot — spec + UI mocks (no build) — 2026-10-31

**Worker:** `broll-pilot-plan` · **Worktree:** `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/broll-pilot` (branch `broll-pilot`, from main `ce8fd25`)
**Reports to:** flivideo-orch (SendMessage `flivideo-orch`). Never park waiting on David — route questions to orch.
**Priority:** #3. Spec only. **Do not write implementation code** — David approves the mocks first.

## Source — read the voice log, not just the dossier
- Captain's Log **B676** (Plaud voice log, wins on intent) and **B677** §4–6, §8, §9 D4–D6, D9, §10 Q4, Q7
  (`capture_get` via captains-log MCP or `$CAPTAINS_LOG_URL`). B677's appendix is the verbatim voice session.
- Prior art: FliStudio extension pattern — `modules/overlay-pilot`, `modules/storypilot`,
  `docs/planning/overlay-pilot/` (spec shape), `@appydave/extension-core`.
- FliHub context: `/Users/davidcruwys/dev/ad/flivideo/docs/flihub-rebuild-spec-parked-2026-10-30.md`
  (parked — read only, don't edit) and `/Users/davidcruwys/dev/ad/flivideo/docs/flihub-discovery-2026-10-30.md`.

## What the spec must cover
- **Catalogue / organiser**, not generator or editor. A Pilot: one problem, an API an agent drives (`dev-team:drivable`).
- **Auto-describe on drop-in** + taxonomy/ontology so a later AI can choose footage. The three screencast kinds
  (silent → human or frame-sampled description; voice-only → transcript; on-camera → transcript).
- **Provenance + type + raw/synthesized**, mirroring StoryPilot's resource pattern, but visual.
- **Scope levels:** per project (in); cross-project references, e.g. thumbnails of earlier published videos (in);
  brand/global reusable (out now — structure for it).
- Assets are *available*, not final — reusable, or unused.
- **Registration contract** that FliHub and FliCast will call: path + transcript + tags, **files stay where they
  are** (registration, not relocation). Define it so the FliHub/FliCast buttons can be built against it.
- **Out of scope:** timeline placement (future Timeline Pilot / Director's Chair), Motion Pilot, video groups.
- Open questions section with a recommendation for each.

## Deliverables
1. Spec at `docs/planning/broll-pilot/spec.md` in the worktree, using `appydave:goal-plan` shape
   (In/Out of Scope, Definition of Done, AC table `# · Criterion · How to check`).
2. **UI mocks as ONE Claude Artifact** — load `brand-dave:brand` first; AppyDave brand, **LIGHT ONLY**
   (`grep -c prefers-color-scheme` = 0). Show the catalogue grid, an asset card opened (description,
   provenance, tags, scope level), and the drop-in/describe flow. Test the link before reporting.
3. Commit + push the branch. Message flivideo-orch with the spec path and artifact URL.

## Never
- No implementation code, no new server routes, no FliHub edits.
- Don't edit the parked FliHub rebuild spec.
