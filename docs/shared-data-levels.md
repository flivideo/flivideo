# Shared data: global / brand / project

**Purpose**: The one place that says where the suite's shared files live, who reads and writes each one, and how the
levels merge (editing pass item 14, 2026-10-04). True at fli-core v0.15.0.

**For agents**: Read a shared file only through fli-core. Never write one by hand-rolled JSON. Words go through
`changeWordsFile`, as described below.

---

## The pattern

Each kind of shared data is **one plain JSON file shape**, found at up to three levels:

```
global    ~/.config/appydave/<file>        the whole suite, this machine (travels with that folder's git repo)
brand     v-<brand>/<file>                 one channel
project   v-<brand>/<project>/<file>       one video
```

- **Lower wins.** If two levels have the same key, the project beats the brand and the brand beats global.
- **A lower level can switch off** an entry it inherits (`off`). It never deletes the higher file's entry.
- **Absent is empty.** A missing file, or one that cannot be used, counts as empty when it is read. Reading never
  throws, so an app keeps working with FliStudio down.
- **An unusable file is never overwritten.** A write refuses it, and a person fixes it by hand.
- **Every entry carries a `Stamp`** `{ at, by }`, where `by` is `human:ui`, `cli` or `agent:<name>`. It records who
  changed the entry and when.

## The files

| Data | File | Levels | Readers | Writer |
|---|---|---|---|---|
| **Words**: names (+ `heardAs`), spelling rules, fillers, `off` | `fli.words.json` | global · brand · project | FliCut (corrections), FliTools (vocabulary hint to the transcriber), FliStudio, FliHub (**project only**) | `changeWordsFile`, called by FliStudio `words.add`/`remove`/`promote`, or by an app directly (see below). FliHub writes project only. |
| **Video resources**: the registry of kinds/groups at every level; the resources themselves at project | `fli.resources.json` | global · brand · project | FliStudio | FliStudio (`writeResourcesFile`) |
| **Brand settings**: colour, transcription providers | `fli.brand.json` | brand | FliStudio (colour strip), FliTools (providers) | `writeBrandSettings` in fli-core. No app calls it yet, so the file is edited by hand today. |
| **Transcription providers** | `flitools.json` → `fli.brand.json` → `fli.studio.json` | global → brand → project | FliTools | Each file belongs to its own app. FliTools owns `flitools.json`, and FliStudio writes `fli.studio.json` (project settings). |

fli-core calls: `readWords` (then `vocabularyOf` / `fillersOf`) and `readResources` take
`{ globalFile, brandRoot, projectDir }` and read only the levels you pass; `readBrandSettings(brandRoot)` reads the one
brand file. That is how FliHub stays at project level:
it passes `projectDir` only.

## Writing words: one path for every app (item 15 decision)

**Decision (2026-10-04):** fli-core owns the write. Every change to a `fli.words.json` goes through
`changeWordsFile(file, change)` in fli-core:

1. It takes a lock file beside the target, `fli.words.json.lock`. If another writer holds it, it waits up to 3 s and
   then answers `busy`. A lock older than 10 s belonged to a crashed writer and is broken.
2. It **re-reads** the file under the lock, so it always merges into what is on disk now.
3. It applies the pure rule (`addWord` / `removeWord`).
4. It writes the file atomically (temp file, then rename).

Thin wrappers sit on top: `addWordAt(file, …)`, `removeWordAt(file, …)`, and
`rememberWord(level, { globalFile, brandRoot, projectDir }, entry, by)`.

**Who calls it:**
- **FliStudio running:** apps call FliStudio `words.add`. It resolves brand and project names to a folder, then calls
  `changeWordsFile`.
- **FliStudio absent:** an app that already knows the folder calls `rememberWord` / `removeWordAt` itself. FliCut
  standalone can do this. FliHub always does, at project level only.

**Why:** both routes run the same fli-core code, so there is exactly one set of merge rules, and FliStudio is never a
hard dependency for remembering a word. The lock plus the re-read covers the case of two apps writing at once. A test
runs twenty parallel writers, and all twenty entries land. "FliStudio is the only writer" (2026-09-24) protected *one
set of rules*. The rules now live in fli-core, so a direct write keeps that guarantee.

**"Remember", not "set":** a name sent with `merge: true` keeps the level's existing `heardAs` and spelling for that
term, then adds the new ones. Without `merge`, the entry replaces the old one. Callers never merge `heardAs`
themselves.

## Remember for this video (item 16)

- **FliStudio:** `words.add { level: 'project', brand, project, entry }`.
- **FliHub:** `POST /api/projects/:code/words { entry }`, `GET` and `DELETE` on the same path. These read and write
  `<project>/fli.words.json` only. FliHub's "add to project" dictionary action writes here, and the Gling dictionary
  includes these names.
- **Direct (no FliStudio):** `rememberWord('project', { projectDir }, entry, 'agent:<app>')`.

## Not in this pattern

- `.flihub-state.json` `glingDictionary` and FliHub's own `config.json` `glingDictionary` are FliHub's legacy lists.
  FliStudio `words.import-flihub` copies them into `fli.words.json`.
- Corrections made inside an edit stay in that edit's cut file. Nothing here rewrites a transcript.

Source: fli-core `src/words.ts`, `src/resources.ts`, `src/brand-settings.ts`, and the fli-core README.
