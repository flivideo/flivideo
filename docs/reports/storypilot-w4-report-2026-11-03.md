# Story Pilot W4: versions, undo, build record, Rerun (build report, 2026-11-03)

**For**: `flivideo-orch` (re-gate on the M4, merge, restart, screenshots on a project copy). **From**: the W4 build
session on the M2. **Brief**: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/storypilot-w4-rerun-versions-2026-11-03.md`.
**Status**: pushed and stopped. Nothing is merged or restarted, and d13 was not rerun.

## The two branches

| Repo | Branch | Commit | On top of |
|---|---|---|---|
| flistudio | `storypilot-w4` | **`ec746f5`** (one commit) | `c968ec7` (origin/main, W2.1) |
| appydave-plugins | `storypilot-w4` | **`e563f52`** (one commit) | main |

- flistudio worktree: `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/storypilot-w4`.
- The plugins branch updates the `flivideo:storypilot` skill and bumps flivideo to **2.8.0**. Merge it together with or
  after flistudio. Before that merge, `build.py` calls verbs the server doesn't have yet.

## Tests on the M2 (shell set to `CAPTAINS_LOG_URL=https://example.invalid`; e2e uses the CL stub from global-setup)

| Check | Before (`c968ec7`, W2.1 report) | After |
|---|---|---|
| storypilot | 302 | **324** ✓ (+16 server `versions.test.ts`, +6 client `history.test.ts`) |
| storypilot e2e | 5 ✓ · 11 skipped | **7 ✓** · 11 skipped (+2 `storypilot-versions.spec.ts`) |
| server | 759 ✓ · 4 ✗ | **760 ✓** · 4 ✗ (PIL) · 2 skipped |
| overlay-pilot | 61 ✓ · 10 ✗ | 61 ✓ · 10 ✗ (PIL) |
| extension-core / broll-pilot / client | 55 / 53 / 335 | unchanged ✓ |
| Full e2e | — | 49 ✓ · 2 ✗ · 12 skipped |
| Typecheck, lint, format, `api:check` | | clean; **179 methods** (was 173) |

- **The failures are all missing PIL.** The M2 has no Python `PIL`. That covers the 14 unit failures (same as before)
  and the 2 Overlay Pilot e2e failures (`overlay-pilot.spec.ts:34` and `:210`), whose error says
  `renderer gave no answer … No module named 'PIL'`. I did not re-run those two e2e on `c968ec7`. The M4 has PIL, so
  its re-gate settles them.
- **The 11 Story Pilot skips** need the real d13/d18/d19 folders, so they only run on the M4.
- **The new e2e uses a synthetic fixture project** (`a18-versions-w4`), so it runs on both machines. It never touches a
  real script.
- **Lint's 3 warnings** are old ones in `drill`, `social` and `thumb-pool` specs, not in W4 code.

## What changed, by brief section

**§1 Versions**
- Every `story.script.set` writes `script/storypilot/<video|project>/versions/v0001.json` and upward. Each file holds
  `{n, at, by, kind: edit|build|restore, note, restoredFrom}` plus the full text, title, triggers and chapters.
- `story.script.set` takes optional `kind` (`edit` default, or `build`) and `note`. It now answers
  `version {n, kind, coalesced}`.
- New verbs: `story.script.history`, `story.script.get {version?}`, `story.script.restore {version, note?}` and
  `story.script.undo`. Restore and undo always write a new version, so history is never rewritten.
- Undo after a restore goes to the version before the one it restored, so repeated Undo walks back.
- **Listen stays cheap.** Restore and undo answer `respeak`: the paragraphs whose audio is no longer fresh, using
  Listen's own per-paragraph hash. The screen feeds them to `useRegen`, so only those are spoken again. The e2e proves
  it: edit ¶2, Undo, and FliTools is asked for exactly one paragraph, the old ¶2.

**§2 Build record**
- `story.build.record` attaches the record to a `kind: build` version, once.
- The record holds: mode (create / update / recreate), instruction, previousVersion, islands, settings, templates,
  skill + version, model, by and at.
- Each island in the record carries its nature, layer and role, plus a **pin**: the extract's sha256 for a session,
  the file or text hash, or the Captain's Log code. It also carries freshness (fresh / out-of-date / unknown /
  extract-stale).
- Settings are the resolved settings, each with its level. Templates are listed by id, scope, label and a hash of
  their text.
- `story.brief.build` returns exactly these fields. The round-trip test passes them unchanged into
  `story.build.record`.
- **Skill:** a new `scripts/build.py` writes `kind: build` and then records it in one step.
  - If the record is refused, it exits 1 with `SCRIPT WRITTEN AS VERSION n BUT ITS BUILD WAS NOT RECORDED`.
  - I checked both paths against a fake door.
  - SKILL.md now says "never a bare `story.script.set`" and documents modes, Rerun, history and undo.

**§3 Rerun**
- A **↻ Rerun…** control sits under the script's meta line, in the page flow.
  - Modes: **Update** (the default; needs a change note) and **Recreate** (the note is optional).
  - It composes one instruction (`modules/storypilot/shared/rerun.ts`). The instruction names the skill, the
    `story.brief` params, the mode, the note, the current version, and "record the build … if the record fails, stop
    and say so".
- It sends through Send to session to a chosen session, `flivideo-orch` by default. With that feature off it offers
  **Copy instruction** instead.
- Either way, `story.rerun.mark` stores a marker that shows "rerun asked of <session>" (or "rerun copied for an
  agent"). It has a × to clear it, and a new build version clears it too; a plain edit does not.

**§4 Provenance**
- A new **History** rail tab, headed "How this script was built", lists every version newest first: who, when, kind,
  note, words and which paragraphs changed. Older versions have a Restore button.
- A build version opens "how it was built" as a plain `dl` list. A build with no record says so in red.
- The script line shows `v<n> · Undo · History`. There's no React Flow.

## Decisions I made that the brief didn't

1. **Only a person's saves fold together** (`human:*` within 10 s). An agent's writes are deliberate, so each one is its
   own version. Otherwise two quick `story.script.set` calls from Claude would silently become one.
2. **Scripts from before W4 show as a "seeded" version 1.** Reading the history never writes anything. The seed is
   written down at the next write, so Undo works on d13's existing script as soon as anyone edits it.
3. **`story.rerun.mark` takes `to`, not `session`.** The door strips `because` / `session` / `answers` as the notes
   envelope (`door-log.ts`), so a field called `session` never reaches the handler. The stored marker still says
   `session`.
4. **Send to session reaches the module through a new optional `HostKit.sessions` channel** in extension-core:
   `live()` and `send()`. ModuleKit implements it over the existing `/api/sessions/*` routes. The module still imports
   nothing from FliStudio. With no channel, or with `live()` refused (feature off), the module offers Copy.
5. **The brief says segment changes are versions, but there is nothing to version there.** `story.segment.set` never
   writes `script.md`: a recorded paragraph enters the script through `story.script.set`, which is already a version.
   So I left segments alone.
6. **The door log** now watches `story.script.restore` / `undo` (script before and after) and `story.rerun.mark`. I
   didn't watch `story.build.record`: it's still logged, just without a before/after. A new notes test covers undo and
   mark.
7. **No new failure codes.** Unknown version, record-on-an-edit, record twice and undo at v1 all use `invalid-input`.

## For the M4 re-gate

- **Build the whole workspace first.** `npm run build` builds extension-core, the modules and shared. In a fresh
  worktree, `shared` won't build until every module's `dist` exists.
- **`docs/schema-mirror.*` was not regenerated.** `npm run mirror:check` on this branch reports 1,546 differences, and
  almost all of them were already there before W4 (W1/W2 didn't regenerate it either). Regenerate it once on main
  after merging, rather than in each lane.
- **Restart, then a quick look:**
  - The Story Pilot page shows `v1` beside the script once anyone writes it. Before any write it shows `v1` seeded,
    from the existing script.
  - The History tab lists that seeded version.
- **Screenshots on a project copy** (the brief's two):
  - The History tab with two versions: edit one paragraph, then open History.
  - The Rerun box open.
  - My fixture versions are at `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/storypilot-w4/test-results/versions/`
    (`2000-history.png`, `2000-rerun-open.png`). They're my own check; yours are the record.
- **Send to session stays off by default** (`FLISTUDIO_SEND_TO_SESSION=1`). With it off, Rerun shows Copy only, which
  is the expected state.
