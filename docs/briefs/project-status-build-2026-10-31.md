# Brief: Project Status (FliStudio project list) — BUILD — 2026-10-31

**Builder:** a fresh session launched by flivideo-orch. **Reports to:** flivideo-orch (SendMessage `flivideo-orch`).
Never park waiting on David; route every question to orch with a recommendation.

**Worktree (build here, nowhere else):** `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/project-status`
- Branch `project-status`, off FliStudio main `38b6a75`.
- Check `pwd` and the branch first, and stop if either differs.

**Approved:** David approved the mock on 2026-10-31: "I love where you've taken this Artefact… build this out."

## Goal

FliStudio's brand project list should answer three things at a glance: what is published, what is being worked on,
and what needs attention.

- **Status is worked out from evidence on disk.** Apps and extensions move it forward as they work.
- **A person (or an agent asked by one) can override any step, park, abandon and write notes.**
- **When later evidence disagrees with a human setting, show the conflict.** Never silently overwrite the human
  setting, and never freeze it.

## Read first

1. **The approved mock. It is the visual contract.**
   - Published: https://claude.ai/artifact/1ik3tTnTU8ssSmEtcCdbgH
   - Source: `docs/planning/project-status/mock.html` in the worktree.
   - Match it closely. Its "Eight questions" cards hold the recommended answers, and those are now the rulings below.
2. **The dry-run derivation and its output.**
   - `docs/planning/project-status/derive-dry-run.py`
   - `docs/planning/project-status/dry-run-v-appydave-2026-10-31.json`
   - The script shows the detection rule for each box. It read `publish.status` over RPC; the server should compute the
     same thing natively.
3. **Worktree conventions.**
   - The worktree's `CLAUDE.md` and `docs/AGENT-NOTES.md`.
   - Fire `appystack:appystack-conventions` before changing code.
   - Read `dev-team:drivable` for the RPC side.
4. **Prior art in the codebase:**
   - The existing project list page: the brand page with Project / Name / Videos / Apps with work here / Touched.
   - `projects.list`, which already returns `apps` and `touchedAt`.
   - `publish.status` readiness rows. They already carry `state` / `why` / `by` / `at`, so copy that shape.
5. **Captain's Log state and recency styling**, for the recency tint:
   - `/Users/davidcruwys/dev/ad/apps/captains-log/client/src/styles/index.css` around `.cl-row[data-age]`.
   - `ageBucket` in `client/src/captures/helpers.ts`.

## Rulings (do not re-open)

1. **Boxes, not a strict ladder.** There are 8 boxes in a fixed order:

   Idea · Script · Recorded · Editing · Exported · Final cut · Launch prep · Published

   - Each box is one of: done, part, empty, skipped (empty but a later box has evidence), or stale.
   - The stage word is the furthest box that has evidence.
   - Model the boxes as a **list of steps**, not 8 hard-coded fields. Per-brand recipes come later (see Out of scope),
     so keep the list swappable.
2. **Detection, deterministic.** Port it from `derive-dry-run.py`:

   | Box | Done | Part | Stale |
   |---|---|---|---|
   | Script | `script.md` exists | a StoryPilot `story.json` with no script | |
   | Recorded | an intro segment **and** an outro segment among the takes in `hub/recordings` | anything less | |
   | Editing | an export exists | a `fli.cut.*.json` exists | |
   | Exported | an `.mp4` in `videos/*/` | | the publish readiness `video` row is `stale` |
   | Final cut | readiness `video` row is `set` | | |
   | Launch prep | 4/4 of title, thumbnail, description, chapters | 1–3 of them | |
   | Published | readiness `published` row is `set` | | |

   - Takes are named `NN-T-label`, for example `01-1-intro`.
   - With a script, Recorded also shows chapter coverage, e.g. "0 / 6 chapters" for d13 from its `story.json`.
   - "Editing finished" can't be detected; a person says so.
   - A project with several videos takes its row stage from the furthest video. The tooltip names each video.
3. **Last work.** Use the newest file mtime, excluding `-trash/`, `-renders/`, `.flihub-*` bookkeeping and `.DS_Store`.
   - Recency tint in 4 buckets, the same as Captain's Log: today, yesterday, 2–6 days, older (no tint). Use AppyDave
     amber.
   - ★ marks work done today.
   - A **pulse** shows when a project is not published, not parked and has had no work for 14 days or more.
4. **Every change is timestamped.** Keep an append-only log per project in a new file `fli.status.json` at the project
   root. Each entry is `{step, state, by, at, why}`. That log holds human overrides, holds (parked / abandoned, plus a
   `brollSource` flag on abandoned), notes and tags.
   - Stamp `by` with the principal: `human:ui` or `agent:<name>`.
   - Computed state is NOT stored. It is recomputed on read and cached.
5. **Overrides and conflicts.**
   - A human step setting (Auto / Done / Not yet / Skip) stands until evidence newer than it disagrees.
   - When it does, show a one-line conflict on the row. Example: "You: Parked · 6 new takes today → Back on? / Keep
     parked".
   - The row pulses, and nothing changes until a person answers.
   - "Auto" clears the override and goes back to the computed state.
6. **Where it lives.** FliStudio owns the derivation, the overrides, the UI and the RPC.
   - In v1, FliStudio **scans the folders**. That works today.
   - Also define a small fli-core helper and schema that apps will later call to write facts ("takes added",
     "exported"). Write a short follow-up brief in `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/` for wiring it into
     FliHub, FliCut and FliEdit.
   - **Do not edit other apps.**
7. **Row layout. David's latest feedback is final.** Columns:

   `#` · markers · Project · Apps with work here · Tags · Status · Last work

   - **Markers column:** three fixed slots right after the code.
     - pulse (clickable, opens the control plane);
     - ✎ (a person set something);
     - ★ (worked on today) or ⏸ (parked).
   - **Status column:** a fixed-width stage word in mono first, then a gap, then the 8 boxes. No "part" or "stale"
     words; the box styling shows them, and the tooltip explains.
   - **Hover / focus on status** shows the evidence per box, plus who / when / why / notes.
   - **Apps with work here stays.** Chips open that app on that project, through the existing launch path if there is
     one. Add extensions: StoryPilot (`script/storypilot/`), Overlay Pilot, B-roll Pilot, FliEdit, with whatever
     folder marker each writes.
   - **No tabs, no group headings.** The list keeps one linear order. Use show/hide filter chips with counts:
     - Needs attention · Working · Not started · Published · Parked · Abandoned (Abandoned is off by default);
     - plus tag chips.
8. **Control plane.** Clicking a pulse or a status cell opens a panel for that project:
   - all 8 steps, each with its evidence and an Auto / Done / Not yet / Skip control;
   - a **Notes** field (AI reads notes, so expose them over RPC);
   - Still going / Park / Abandon. Abandon has a "keep as B-roll source" switch.
   - a history line built from the log.
9. **Tags.**
   - Tags are per project, with one shared list per brand.
   - Edit them inline in the Tags cell, with type-ahead from tags already in use.
   - Rename a tag once and every project follows.
   - Tag chips in the filter bar.
   - "+ tag" shows faintly on untagged rows.
   - Series (Cutty) is unchanged.
10. **RPC (drivable, agent-callable).** None of these are human-only:
    - `project.status` (one project: steps, evidence, overrides, holds, notes, conflicts, next);
    - a `status` field on `projects.list`;
    - `project.status.set` (step override);
    - `project.hold`;
    - `project.note`;
    - `project.tags.set`;
    - `tags.list`;
    - `tags.rename`.

    Follow the module and OpenRPC registration steps in AGENT-NOTES.

    Add phrases to the `flivideo:flistudio` skill: "what's stalled", "status of my projects", "park d09",
    "mark d05 abandoned", "tag d14 invoicing". The skill lives in `/Users/davidcruwys/dev/ad/appydave-plugins/flivideo/`.
    Commit that change separately and tell orch.

## Out of scope

- The heat map.
- Archive as a status.
- A setting for the stall threshold.
- Per-brand recipes and layer boxes (keep the step list swappable, but don't build recipes).
- YouTube sync.
- Editing FliHub, FliCut, FliEdit, FliTools or any extension's code.
- **Setting real holds or tags on David's projects.** David sets them himself in the UI. Proposed tags appear in the
  mock only.

## Never

- Never write `fli.status.json` (or anything else) into real project folders under `~/dev/video-projects/` during
  development or tests.
  - Use a fixture copy, the same way the existing tests use fixture estates.
  - Reading the real `v-appydave` folders to compare the dry run is fine.
- Never test against live ports 7150 / 7151 / 7111 / 7121 / 7161 / 5173 / 5101. Use the worktree's own ports.
- Never merge to main or restart apps. Orch merges and restarts.
- Never `pkill` or `killall` with patterns.
- Never touch `fli.edit.*` files, takes or video files.

## Definition of done

| # | Criterion | How to check |
|---|---|---|
| 1 | The server derivation reproduces the dry run for all 17 v-appydave projects (stage + every box state) | A test/script comparing against `dry-run-v-appydave-2026-10-31.json`, run read-only against the real folder; d13/d09 script text may differ |
| 2 | The list matches the mock's row layout | Playwright screenshot on worktree ports, attached in the report |
| 3 | Filters (status + tag) hide/show rows with correct counts; Abandoned is hidden by default | e2e |
| 4 | Control plane: an override, a note and a hold are written to `fli.status.json` with by/at, then reflected in the row (✎ appears) | e2e on a fixture |
| 5 | Conflict: override, then newer evidence, gives the conflict line and a pulse; "Auto" clears it | unit + e2e on a fixture |
| 6 | Tags: add, type-ahead, rename across projects, filter | e2e on a fixture |
| 7 | RPC verbs listed in capabilities / OpenRPC and drivable by an agent principal | RPC test, as `agent:test` |
| 8 | Gates green: typecheck, unit, lint, e2e | the command output in the report |
| 9 | The fli-core follow-up brief is written; the skill phrases are added | paths in the report |

Commit on `project-status`. Then SendMessage `flivideo-orch` with:
- the DoD table with pass/fail;
- the gate output;
- the screenshots;
- the follow-up brief path;
- anything deferred, with the reason.
