# FliHub: placeholder chapters, re-recording and resequencing (assessment)

**Purpose**: What FliHub (and its neighbours) would need so David can leave a placeholder chapter, keep
recording, come back and re-record it (overwrite, replace or delete segments, and let the others close up).
**Assessment only**: nothing was built or changed. Every "today" claim carries `file:line` evidence.
**Brief**: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/flihub-rerecord-placeholder-assessment-brief-2026-10-07.md`
**Written**: 2026-10-07, against flihub `69af03a`. D01 was read, never written.

Paths below are relative to `/Users/davidcruwys/dev/ad/flivideo/` (flihub, flicut, flitools, flistudio, fli-core).

---

## Verdict

- **Today FliHub only goes forward.** The inbox always offers "highest segment + 1", nothing in the UI can
  change a segment number, and nothing closes a gap. Of the five scenarios, only "delete a take" works; the
  rest end in a gap, a duplicate number, or a manual Finder rename that orphans transcripts.
- **The real danger is not FliHub, it's the neighbours.** FliHub's own rename carries transcripts,
  engine copies and state. But FliCut edits and FliStudio's cut draft point at takes **by path**, and
  neither notices when a different take now lives at that path. Renumbering 06-2 → 06-1 makes an
  existing cut silently play the wrong take.
- **Recommendation**: keep segment numbers as **positions in the filename** (what David sees is the
  order), but only ever change them through **one guarded FliHub operation** that trashes, renames in a
  safe order, journals the moves, and refuses while a cut references an affected take. Build
  **"Replace this take"** first: it alone covers the placeholder case.

---

## 1. Today — what happens in each scenario

### How the next number is chosen

| Step | What happens | Evidence |
|---|---|---|
| Project opens | Template = highest chapter on disk, its highest segment + 1 | `flihub/shared/naming.ts:503-528` |
| After each promote / undo | Seq re-read from disk: highest + 1 in the template's chapter | `flihub/client/src/App.tsx:235-239`, `:280-284`; `shared/naming.ts:475-485` |
| "New Chapter" | highest recorded chapter + 1, seq 1 | `flihub/client/src/App.tsx:415-428` |
| Seq field | Free-text, editable by hand (digits only, max 3) | `flihub/client/src/components/NamingControls.tsx:199-203`; `shared/naming.ts:25-30` |
| Promote (`POST /api/rename`) | Builds `NN-S-slug[-TAGS].mov`, refuses **only if that exact filename exists**, moves the file, queues transcription | `flihub/server/src/routes/index.ts:270-276`, `:279-287`, `:299`, `:356` |
| Recordings list | Sorted chapter → segment → file mtime; duplicates allowed | `flihub/server/src/routes/index.ts:662-668` |
| Row editing | Chapter and name are editable; **segment is read-only** | `flihub/client/src/components/shared/EditableFileRow.tsx:23`, `:218` |
| Batch rename | UI always sends `sequenceMode: 'preserve'`; the API's `'renumber'` mode has no UI caller | `flihub/client/src/components/RecordingsView.tsx:1110-1116`; `server/src/routes/manage.ts:136-143` |
| Delete | Preview, then moves the take + `.json/.srt/.txt` + `engines/` copies to `-trash/` (suffix `-1`, `-2` on collision), clears safe/parked | `flihub/server/src/utils/recordingArtifacts.ts:29`, `:38-80`, `:86-104`; `server/src/routes/index.ts:1113-1180` |
| Restore from trash | **No route exists.** Only "restore from Safe" (a state flag) | `flihub/server/src/routes/index.ts:888` (safe flag only) |

### (a) Placeholder 06-1, later overwrite it

1. Inbox template says 06-2 (highest + 1). He types Seq `1`.
2. **Same slug** (`06-1-constant-improvement`) → 409 "Target file already exists" (`index.ts:279-287`). Dead end.
3. **Different slug** (`06-1-better-take`) → promotes. Now **two 06-1 files**, ordered by mtime
   (`index.ts:662-668`). The placeholder is still there.
4. He clicks Delete on the old 06-1 → it and its transcripts go to `-trash/` (`recordingArtifacts.ts:38-80`). Works.
5. **Orphans**: none in FliHub. **But**: a FliCut edit or FliStudio draft that referenced the old 06-1 now
   points at a missing file — FliCut "Breaks silently until export" (`flicut/docs/cut-model-spec.md:523`),
   FliStudio's draft silently drops it (`flistudio/client/src/screens/StartEdit.tsx:235-236`).
6. Safer order "delete first, then record with seq 1 and the same slug": works, because the old
   transcripts went to trash, so the new take isn't skipped as "already transcribed"
   (`flihub/server/src/routes/transcriptions.ts:254-258`, the FR-159 fix at `:276-283`).
   But it relies on David doing two steps in the right order with no guard.

### (b) Record 06-2, delete 06-1, have 06-2 become 06-1

1. Record → inbox offers 06-2 → promote. OK.
2. Delete 06-1 → trash. OK.
3. Make 06-2 into 06-1: **no UI path.** Segment is not editable inline (`EditableFileRow.tsx:218`), batch
   rename keeps the segment (`RecordingsView.tsx:1114`). Only the raw API (`manage.ts:142`) or Finder.
4. Finder rename → transcripts stay under `06-2-…` (orphaned), FliHub shows "no transcript" and re-queues;
   FliTools reuses the transcript from its sha256 cache so it's cheap (`flitools/src/service.ts:56`, `:276-282`),
   but `06-2-*.json/.srt/.txt` and `engines/06-2-*` stay behind as orphans.
5. **Result today: 06-2 sits alone in chapter 6.** It plays fine; it just looks wrong.

### (c) Delete the middle of three segments and close the gap

1. Delete 06-2 → trash. OK. Leaves `06-1, 06-3`.
2. Close the gap: same wall as (b). The API's renumber mode would rename `06-3 → 06-2` safely here
   (ascending order into a freed slot), but it also forces **one label on every file**
   (`manage.ts:95-101`, `:145-150`), and if any take is mid-transcription that one file fails and the
   rest succeed — a half-renumbered chapter (`renameRecording.ts:297-303`, `manage.ts:160-170`).
3. Undo for batch renames is **in memory only** and lost on server restart (`manage.ts:43`, `:772`).

### (d) Insert a new segment between two existing ones

1. No "6.5": segment is digits only (`shared/naming.ts:25-30`; fli-core `recording.ts:49-85`).
2. Typing Seq `2` with a different slug creates a **second 06-2** that sorts by mtime — i.e. *after* the
   original 06-2 (`index.ts:662-668`). Not an insert.
3. Real insert = shift 06-2..06-N up by one, top-down, then promote into the gap. FliHub has exactly this
   top-down cascade **for chapters** (split-chapter, `manage.ts:893`) but not for segments.

### (e) Re-record a whole chapter

1. Delete every take in the chapter (one by one, or "Safe all"/"Park all" are flags, not deletes).
2. Inbox: set chapter 06, seq 1 by hand (template will be in the latest chapter).
3. Works, with the same unguarded cut-reference risk as (a).

### What gets orphaned, by dependent

| Dependent | Keys on | On FliHub rename | On delete / overwrite | Evidence |
|---|---|---|---|---|
| Transcripts `hub/transcripts/<take>.*` | take basename | **carried** (5 exts) | **trashed** (3 exts; `.vtt/.tsv` left behind) | `renameRecording.ts:93-101`; `recordingArtifacts.ts:29` |
| FliTools engine copies `engines/<take>.<engine>.*` | take basename | **carried** | **trashed** | `renameRecording.ts:103-110`; `recordingArtifacts.ts:58-64` |
| `.flihub-state.json` recordings (safe/park/note/aspect/sound) | filename | **carried** | safe/park cleared | `renameRecording.ts:170-189`; `index.ts:1175-1176` |
| `.flihub-state.json` chapter titles | `"06"` | split/swap **don't** move them | — | `shared/types.ts:1050-1052`; no `chapters` reference in `manage.ts` |
| Image assets `NN-S-I…png` | chapter + segment | **not carried** | not touched | `shared/naming.ts:358-367` |
| FliTools job / cache | sha256 of content; queue stores abs path | fine (cache hit) | queued job ends "recording changed or is gone" | `flitools/src/service.ts:56`, `:1347-1350`; `editQueue.ts:9-21` |
| FliTools transcript `source.path/name` | path | goes stale (cosmetic) | — | `flitools/src/service.ts:735` |
| **FliCut** `fli.cut.<name>.json` | `medias[].filePath` (relative) | **silent break** | **silent wrong take** if another take lands on the same path | `flicut/src/shared/project.ts:56-60`; `project-store.ts:234-251`; `docs/cut-model-spec.md:523-525` |
| **FliStudio** cut draft `fli.studio.cut-draft.json` | project-relative paths | silently dropped from order | silently dropped | `flistudio/shared/src/contracts.ts:1137-1145`; `client/src/screens/StartEdit.tsx:235-236` |
| **FliStudio** `video.text` take ladder | segment number | "latest" take changes | "latest" take changes | `flistudio/server/src/capabilities/video-text.ts:112-118` |
| `-trash/` | basename | — | flat, suffixes `-1`; **no origin record, no restore** | `recordingArtifacts.ts:86-104` |

D01 confirms the FliCut shape: its cut holds all 20 takes, e.g. `"filePath": "hub/recordings/06-1-constant-improvement.mov"`
with a stable media `id` UUID and a separate `mediasTimeline` order (read-only inspection of
`d01-flivideo-tour/fli.cut.flivideo-tour.json`).

---

## 2. The model — positions or identities?

| Option | What it means | For | Against |
|---|---|---|---|
| **A. Positions** | Segment number = place in the chapter; renumber files on change | What David sees in Finder, FliHub and the cut agree; matches "recordings are canonical… named so you can see the sequence" (`brains/video-as-code/project-folder-convention.md:84-85`) and "stages live in the filename" (`project-structure-reading-list.md:71-72`) | Every renumber renames files; neighbours that key on path break |
| **B. Identities** | Numbers never change once given; order lives in metadata | No renames, paths stable, fits "metadata over renames/copies" (`project-structure-reading-list.md:89`; `project-folder-convention.md:261-263`) | Filename stops telling the order (06-2 alone at position 1 forever, "6.5" impossible in the name); every app must read a sidecar to know order; Finder shows the wrong story |
| **C. Positions, one guarded operation** *(recommended)* | A + renumbering only through one FliHub "Replace / Close up / Insert" op that trashes, renames in a safe order, writes a move journal, and refuses while a cut references an affected take | Keeps the filename as the truth David reads; identity already exists where it's needed (FliCut media UUID, FliTools sha256); the journal lets neighbours follow | Needs neighbours to read the journal (or FliCut's planned fingerprint relink) before renumbering is fully safe |

**My take: C.** The "metadata over renames" rulings are about *publishing* and *selects* (a choice
recorded about a file), not the take ladder — and the folder convention explicitly makes the recording
filename the canonical sequence. The pain isn't renaming as such; it's renaming **without telling the
neighbours**. FliCut already models identity (UUID + separate order) and has relink-by-fingerprint
specced (`flicut/docs/cut-model-spec.md:518-519`, not built). So: positions in the name, identity
in the edit tools, a journal in between.

⚠️ **Held question for David — what does a segment number mean?** FliStudio's `video.text` treats the
highest segment as "the latest take" (`video-text.ts:114-116`) — i.e. segments are *retakes, last one
wins*. D01's cut uses all 20 takes in order — i.e. segments are *pieces of the chapter*. Re-recording
semantics depend on which is true. This assessment assumes **pieces** (David's "three segments in a row,
get rid of segment two"), which makes FliStudio's "latest" label wrong for D01-style projects.

---

## 3. The inbox — a target segment

Today: always "highest + 1" (`naming.ts:475-485`); a hand-typed Seq can duplicate but never replace.

**Proposal: a "Lands as" control beside Seq**, three modes:

| Mode | Shown as | Effect |
|---|---|---|
| Next (default) | `→ 06-3 (next)` | Today's behaviour |
| Replace | `→ replaces 06-1` (pick from the chapter's takes) | Old 06-1 + transcripts + engine copies → `-trash/`, new take promoted as `06-1-<slug>` |
| Insert | `→ insert before 06-2` | 06-2..06-N shift up one (top-down), new take lands as 06-2 |

When the chapter is marked **placeholder**, the inbox preselects *Replace* for its single take.

**API**: extend `POST /api/rename` with `target?: { mode: 'next' | 'replace' | 'insert'; take?: string }`.
Server does the trash/shift/promote as one operation, journals it, and returns a `reason` when it
refuses (FliHub's refusal rule, `CLAUDE.md` FR-159): take mid-transcription, take referenced by a cut,
collision. No new client-side numbering logic — the server owns it.

---

## 4. Placeholder as a first-class thing

- **Where it lives**: `ChapterState` already exists for per-chapter data (`shared/types.ts:1050-1052`).
  Add `placeholder?: { note?: string; since: string }` (chapter), and optionally
  `RecordingState.rerecord?: true` (single take). Remember the three-edit rule for new state fields
  (`docs/AGENT-NOTES.md`, "A new ProjectState field…").
- **FliHub**: chapter header badge "PLACEHOLDER — re-record", a header count "2 to re-record", a
  "Mark as placeholder" action on the chapter, and auto-clear when a *Replace* lands in that chapter.
- **FliStudio**: shows the same marker on the project's take ladder. FliStudio shouldn't parse FliHub's
  state file itself — a typed reader belongs in fli-core next to the layout code.
- **Not** a filename tag (e.g. `-PH`): that would rename the take when the flag clears — the very rename
  churn this is avoiding.

---

## 5. Safety

| Rule | How |
|---|---|
| Overwrite never loses a take | Replace = trash first (existing `moveArtifactToTrash`), then promote. Never `fs.rename` over a file (`renameRecording.ts:238-241` already guards). |
| Undo survives a restart | Journal each operation (`moves: [{from,to}]`, `trashed: [{from, trashPath}]`) in `.flihub-state.json` or `-trash/.journal.jsonl`; undo replays it in reverse. Today's undo is memory-only (`manage.ts:43`) and the inbox undo expires after 10 min (`index.ts:67`). |
| Trash can be restored | Today `-trash/` is flat with no origin record (`recordingArtifacts.ts:86-104`). The journal gives each trashed file its origin, so "restore" becomes possible. |
| No half-renumbered chapter | Check all affected takes **before** moving any (transcribing? referenced by a cut? collision?); refuse the whole op with a reason. Rename via temp names (two-phase) so order never matters. |
| Transcripts stay matched | Already carried on rename (`renameRecording.ts:82-118`); add `.vtt/.tsv` to the trash list (`recordingArtifacts.ts:29`) and carry image assets keyed `NN-S-…`. |
| Cuts stay consistent | Phase 3 refuses when any `fli.cut.*.json` / `fli.studio.cut-draft.json` references an affected path. Phase 4 lets FliCut/FliStudio follow the journal (and FliCut's fingerprint relink catches anything else). |

---

## 6. Phased plan

| Phase | What | Owner | Size | Covers |
|---|---|---|---|---|
| **1. Replace this take** | Inbox "Lands as → replaces 06-1"; server trashes old take + artifacts, promotes under its number, journals it, undo restores; refuses if a cut references the old path | FliHub | S–M (~1 day) | (a), (e) |
| **2. Placeholder marker** | `ChapterState.placeholder`, badge + count in FliHub, auto-clear on Replace; fli-core reader; FliStudio shows it | FliHub + fli-core + FliStudio | S | the "what's left to redo" view |
| **3. Close up / Insert** | One "Resequence chapter" op: delete-and-close, insert-before, drag order; two-phase renames carrying transcripts, engines, state, image assets; whole-op refusal; persistent undo; trash restore | FliHub | M (~2-3 days) | (b), (c), (d) |
| **4. Neighbours follow** | fli-core journal read/write helpers; FliCut builds its specced fingerprint detect + relink and reads the journal; FliStudio remaps its draft via the journal instead of dropping entries | fli-core + FliCut + FliStudio | M–L | renumbering after a cut exists |

**Smallest useful first step: Phase 1.** It is the D07 flow exactly: record 06-1 as a placeholder, keep
going, come back, choose *Replace 06-1*. In that flow no cut exists yet, so the refusal guard almost
never fires. Phases 1 + 2 together are the whole placeholder story; 3 + 4 are general resequencing.

**Before Phase 1, David rules on**: (1) segment = piece or retake (§2 held question); (2) the model (C
recommended).

---

## Also found (not in scope, noted for the defect list)

- Split/swap chapter don't move chapter titles keyed `"06"` (`manage.ts` has no `chapters` reference).
- Batch rename response says `transcriptionQueued: true` but `renameRecording` queues nothing
  (`manage.ts:191-197` vs `renameRecording.ts:286-322`).
- Trash takes `.json/.srt/.txt` but rename carries `.vtt/.tsv` too (`recordingArtifacts.ts:29` vs
  `renameRecording.ts:93`).

## David's model — RULED 2026-10-07 (supersedes the §2 held question)

In David's words, condensed (flivideo-orch session, 2026-10-07):

- **Takes live in the inbox, not in recordings.** He commonly does 5–10 bad takes before accepting one. Bad takes rarely reach recordings.
- **Two normal inbox exits:** (a) ~60% of the time: pick the good take → everything else in the inbox is deleted. (b) He forgot to send a good take and has moved on to the next segment(s) → he must send *several* inbox takes in, as consecutive segments, and delete only the remaining bad ones.
- **A segment is a PIECE of the chapter.** A chapter = one or more sequential segments, each recorded clean (record, breathe, set up the next scene, record). All segments play, in order, with no editing. "Retake" is the wrong word in recordings.
- **The case this work is for:** a recorded segment that *becomes* bad — either deliberately (a placeholder, to be re-recorded when he knows more) or retroactively ("that recording is wrong") — so he comes back later and re-records that segment, **and possibly the segments after it**.

### What follows (flivideo-orch's ruling on the design)

1. **Inbox, multi-send:** select one or more takes → "send as segments N, N+1…" in the order picked → delete the rest. Covers exit (b).
2. **Inbox, target a segment:** the send defaults to "next segment"; it can instead target "replace chapter 6, segment 1". The old file goes to `-trash/` (never lost) and the new take takes its number. **Same number in, same number out — no renumber**, so FliCut paths and transcripts stay keyed.
3. **Re-record from here:** replacing segment N *and those after it* is the same action for a run (N..M). If the new run is shorter, the leftover old segments go to trash; a renumber happens only through the one guarded, logged action this assessment already recommends.
4. **Placeholder is a flag on a segment** (metadata, not a filename): shown in FliHub recordings and FliStudio as "to re-record", so the list of what's left is visible.
5. **FliStudio wording fix (small):** `video.text` marks the highest segment as `latest` (`flistudio/server/src/capabilities/video-text.ts:114-118`, contract `shared/src/contracts.ts:1424`) and the ladder's `why` text says "retakes included" (`best-transcript.ts:227-228`). The stitching itself is already right — it uses every segment in order. Drop `latest` and say "segments", not "takes/retakes".

**Correction (David, same day):** replacement is ~90% of cases, not all. **Insert** (segments 1 and 2 are fine but something belongs between them) and **reorder** (move a segment up/down) are part of the same feature, not a separate one. So item 2's "no renumber" holds for Replace only; Insert, Reorder and close-up go through the one guarded, journalled renumber (§5, Phase 3).

**Validated requirement for the build:** `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/flihub-segment-editing-requirement-2026-10-07.md` (handed to the Buzz coding team, D07 job 2).
