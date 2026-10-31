# Brief: fli-notes — a lasting record of notes, asks and changes across FliVideo — 2026-10-31

**From:** the Roamy session `flivideo-field-trial-plan`. **To:** `flivideo-orch` on the M4.
**Go:** David, 2026-10-31 ~23:00 +07, verbatim: *"go with recomendations"*, given in reply to the overnight plan
below (FliStudio + FliCut, fli-core first, D13 opening applied as the first live record). This is David's go for the
whole brief. Taste calls that come up are batched for the morning; they do not stop the run.
**Run:** overnight, long-horizon. David wakes up to it built, merged and ready to try. Done = he clicks it in the app.

---

## 1. Why

Field Trial (`dev-team:field-trial`) has been rebuilt ad hoc per app as a fix-it backlog. David wants something
permanent instead: a running record of what a person or agent **noticed, asked for or changed**, attached to anything
in the FliVideo apps and kept forever, so that over weeks it shows patterns the data alone can't ("David keeps
changing the opening words" → a voice-guide or prompt change). Today those lessons die inside Claude Code
conversations. Field Trial becomes one way to feed and read this record; the record itself is a suite standard.

## 2. Rulings (settled with David tonight — do not re-open)

1. **No thumbs, no ratings.** One message box, like Claude artifact comments: point at something, write a message.
   Evidence: DSP's 37 real items were 32 👎 / 2 👍 / 3 💡, all 37 with prose, and the prompt fix (`174595a`) came from
   the prose. Do not add 👍/👎/❓ or stars.
2. **Three kinds only:**
   - `note`: kept, never nags ("it might be cool to highlight that word in the edit");
   - `ask`: a to-do until done, then links to the change that did it ("change the opening to…");
   - `change`: written **by the app**, automatically, when a record changes.
   The note box has one **"this is an ask"** switch, off by default (off = `note`).
3. **The app logs every change itself, at the door.** Every write command already knows before, after, who (the
   token's principal) and when. So the app writes the `change` record; no skill has to remember. Write commands gain
   an **optional** `because` (the human's words, verbatim) and `session` (Claude Code session id). Missing `because`
   = still logged, just no why. This is the enforcement mechanism — it lives in code, not in skill instructions.
4. **Apps:** FliStudio + FliCut only. The other four, and AppyStack/AppyTron templates, come later.
5. **Home:** the shape and helpers in **fli-core**; the data in a **per-project file** in the project folder.
   Notes about an app itself (not a project) go in that app's own data folder.
6. **Kept apart from decisions.** Gates, approvals, Project Status holds/settings stay where they are. Do not write
   notes into `fli.status.json`.
7. **Off by default.** A small icon + keyboard shortcut per app turns it on; hover outlines what can take a note;
   click opens the box. Agents write with the UI off.

## 3. The record (concept — the builder picks field names in fli-core's style)

| Field | Holds |
|---|---|
| `id`, `at` | id; ISO time |
| `by` | fli-core `Stamp` principal: `human:ui`, `human:chat`, `agent:<name>`, `cli` |
| `kind` | `note` · `ask` · `change` |
| `channel` | `ui` · `chat` · `voice` · `agent` |
| `target` | `app`, `entityType`, `entityId` (plain strings, synthetic keys allowed), `field?`, `region?`, scope `one` / `many` (`entityIds[]`) / `aggregate` (a described query) |
| `where` | `brand`, `project`, `video?` |
| `text` | the human's words, verbatim — the most valuable field |
| `before` / `after` | for `change`: a snapshot, or a diff when large (a 1,000-word script must not be copied in full every write); always keep the actual words near the target, because paragraph numbers move |
| `producer` | prompt/skill/model/version that produced the "before", where known |
| `status` | `kept` (notes) · `open` → `done` (asks); `change` has no status |
| `links` | `session`, Captain's Log B-code, commit, `answers` (the ask a change fulfilled), `follows` |
| `meta` | free bag |

Append-only, one line per record (`fli.notes.jsonl` is the suggested name), under fli-core's lock + atomic-append
pattern (same as words / series / the planned `recordFact`). Never rewrite history; a status change is a new line
that refers to the old id.

## 4. Build

Workers in worktrees only, never on live ports; busy-check before merging into watch-mode apps; `npm install` after
any new workspace. Gates reproduced before each merge.

**A. fli-core (minor release, first).**
- The record schema (zod, browser-safe, beside `Stamp`), schema mirror regenerated.
- `addNote(projectDir|appDir, record)`, `readNotes(dir)`, `scanNotes(roots, filter)` — the last one answers
  "everything on D13" and "every `change` to a StoryPilot script across all projects".
- Tests on temp dirs.

**B. FliStudio** (pinned to the new fli-core).
- **Door logging:** every write capability appends a `change` (before, after, by, at, optional `because`/`session`).
  Start with StoryPilot (`story.script.set`, `story.settings.set`, `story.sources.set`), resources, Overlay Pilot
  beats, Project Status writes; then the rest. Grouping several changes from one session for reading is a reader
  concern — store each.
- **Agent verbs:** `notes.add`, `notes.list` (project / target / kind / open asks), `notes.resolve` (an ask → done,
  linking the change).
- **UI:** the off-by-default icon + shortcut; taggable things carry a target attribute (precedent: the ndis tool's
  `data-review-id` + one drop-in layer); the note box with the "ask" switch; a per-project notes list showing notes,
  open asks and changes (with before/after).

**C. FliCut** (Electron/AppyTron): the same note box + toggle, and door logging on its edit writes (`fli.cut.*`).

**D. First live record — David's D13 opening (this is the end-to-end test).**
Once B is merged and live: apply David's new opening to D13 through `story.script.set` with `because` = his words,
`by` = the agent, `session` = the Roamy session id below. It replaces **only the first line** of
`/Users/davidcruwys/dev/video-projects/v-appydave/d13-overlay-pilot/script/storypilot/project/script.md`:

- **Before:** "What do you do when the thing stopping someone you care about isn't the camera, isn't the editing,
  it's one small boring step that nobody has time for?"
- **After (David's words, tidy only obvious transcription slips — keep his phrasing):** "My girlfriend is not a
  content creator. She is a self-employed nail artist. She has to promote her business using online social media,
  and we've found that she's naturally a really good content creator who can do one-shot videos of 45 to 90 seconds
  really easily. She's full of life and knowledgeable about her topic, but she has a problem getting videos
  published, and that problem is me."
- **Because (verbatim):** "I didn't like the starting line of the phrase that was already there too much. Feel more
  like me, and I'm working on the idea that my girlfriend isn't a content creator, but she's fucking good at it.
  She's so good when she does videos. She's full of life, full of knowledge, all that sort of stuff, but she never
  gets videos done because I don't do the overlays. That's the problem, right?"
- First write the `ask` record (channel `chat`, `by: human:chat`), then the change, linked by `answers`.
- **Only this line.** If the next paragraphs now repeat it ("My girlfriend Joy runs a beauty business…"), do **not**
  rewrite them: list the overlap in the morning report as an open ask for David. Feel/do settings stay untouched.
  Do not resend to TeleTubby / Prompter.

## 5. Out of scope

- The other four apps; AppyStack/AppyTron template changes.
- Editing the Field Trial skills (`dev-team:field-trial*`) or the brain
  (`/Users/davidcruwys/dev/ad/brains/prompt-patterns/feedback-capture-surface-pattern.md`) — Roamy does that after,
  from what the build proves.
- Any classifier / auto-tagging / roll-up. Capture first; read later.
- Anything in §2 of your backlog (automations, YouTube sync).

## 6. Done when

- fli-core released with the schema + three helpers + tests; FliStudio and FliCut pinned to it.
- FliStudio: a write through `story.script.set` produces exactly one `change` line with before/after/by/at; with
  `because` it carries the words. Test proves it.
- FliStudio + FliCut: toggle off by default; on → click a target → note saved with the right target; "ask" switch
  makes it an open ask; `notes.resolve` closes it.
- D13: the ask + change records exist and link; `scanNotes` over v-appydave returns them.
- A **morning UAT page** (AppyDave brand, light only): what to click in each app, what to look for, what isn't done,
  and the batched questions with a recommendation each. Checkpoint updated.

## 7. Known risks

- Your context is long and a Claude Code update is pending: keep progress in `docs/orch-checkpoint.md` as you go so a
  compaction or restart can resume. Restarting yourself to take the update is your call.
- Transcript or Joy quotes in notes: notes stay in project folders; do not paste note contents into commits in
  other repos.

Source session: Roamy `flivideo-field-trial-plan`, Claude session `afaf0ee4-6ed3-47d8-84f0-42414018231a`.
