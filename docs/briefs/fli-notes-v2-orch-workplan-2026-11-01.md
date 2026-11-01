# fli-notes v2 — orch work plan — 2026-11-01

**Parent brief (read it in full first):** `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/fli-notes-v2-quiet-capture-and-lab-2026-11-01.md`
(flivideo `8c092bf`). Corrections from David: `/Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/field-trial/references/learnings.md`
(the 2026-11-01 entries). David's go, 2026-11-01 ~07:30 +07: *"Go on both… Okay, I like option A."* and *"yes remove notes page"*.
**Orch:** `flivideo-orch` (SendMessage). Route questions to orch with a recommendation; never wait on David. Taste calls:
decide on the recommendation, list them in your report.

The same three workers as v1 carry on (they know the v1 code). New branch `notes-v2` cut from `origin/main` in the
same worktree.

| Session | Worktree (build here only) | Branch | Brief section |
|---|---|---|---|
| `fli-notes-core-dev` | `/Users/davidcruwys/dev/ad/flivideo/fli-core-worktrees/notes-record` | `notes-v2` | §3 life states |
| `fli-notes-studio-dev` | `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/fli-notes` | `notes-v2` | §1, §2, §3 readers, §4 Lab |
| `fli-notes-cut-dev` | `/Users/davidcruwys/dev/ad/flivideo/flicut-worktrees/fli-notes` | `notes-v2` | §1, §2, §3 readers |

## Hand-off: fli-core `0.28.0-rc.1`

1. Core builds life states (`live` · `done` · `used` · `stale` · `replaced`, each settle line carrying its reason /
   pointer), appended as new lines; `readNotes`/`scanNotes` default to live, with a history option; v1 ask
   `open`→`live`, `done`→`done`; v1 files still read. **App-neutral field names** (no FliVideo words). Tag
   `v0.28.0-rc.1` on the branch (never push `main`), then message orch and both app workers with the exported names
   and one usage example.
2. App workers start at once on §1 (removal) and §2 (gesture); repin to `github:flivideo/fli-core#v0.28.0-rc.1` when
   the rc lands and map `notes.list` / `notes.resolve` onto life states (`notes.resolve` stays as an alias that settles
   to `done`; add a settle verb for the other states).
3. Orch merges fli-core, tags `v0.28.0`, repins the apps at merge time.

## Gesture — one spec, both apps (one shared implementation per app, not per page)

- Hold **⌘+⇧** → every element carrying the app's target attribute highlights **under the pointer** as it moves
  (outline only, no layout shift).
- **Click while held** → capture-phase listener, `preventDefault` + `stopPropagation`; opens the small note box
  anchored on that target. A link or button under it does nothing. Test proves it on a link.
- **Release** (either key up, or window blur) → highlights gone; DOM/screen exactly as before.
- Note box keeps v1's "this is an ask" switch. Esc / click-away closes it.
- Optional quiet top-bar icon as fallback toggle (no count, no badge).

## Lab notes (studio)

Notes taken in the Lab target the variant, e.g. `entityType: "lab-variant"`, `entityId: "storypilot-lab:B"`, and keep
the words of what they were about. Promotion is out of scope; the settle-to-`used` path just has to exist.

## Rules for every worker

- `pwd` + branch check first; stop if either differs.
- Fire `appystack:appystack-conventions` (FliStudio) / `appytron:appytron-conventions` (FliCut) first.
- Own ports only — never 7150/7151/7111/7121/7161/5173/5101. Fixture project dirs only for writes — never write into
  `/Users/davidcruwys/dev/video-projects/`. Reading D13's real story data (read-only) for the Lab is fine.
- **Do not write D13** — a separate session (`d13-write`) is rewriting its opening.
- Never merge to main, restart apps, `pkill`/`killall` with patterns, touch takes / video files / `fli.edit.*`, or
  write notes into `fli.status.json`.
- Report to orch with: Done-when rows you own (pass/fail + how checked), gate output, screenshots for UI, taste calls
  taken, anything deferred with its reason.
