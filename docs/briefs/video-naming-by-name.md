# Plan — videos named, not numbered (ruling "B only", David 2026-09-22)

**Status**: PLAN ONLY. No code changes until David approves. Written by the FliStudio session (fli-core owner) from
fli-core's code and a read-only sweep of FliCut, FliCast, FliHub and Teletubby (2026-09-22).

**The ruling** (relayed by `d01-work`): `videos/<name>/<name>-<kind>[-<variant>].<ext>` — e.g.
`videos/flivideo-tour/flivideo-tour-cut.mp4`, `…-cut.srt`, `…-audio-a100.m4a`, `…-final.mp4`;
`videos/flihub-demo/flihub-demo-final.mp4` (a FliCast export). No numbers. The name is on every file so a file explains
itself outside its folder. Everything in `videos/`; no `broll/` yet. Supersedes the 09-09 `<NN>-<name>/<NN>-<kind>`.

---

## 1 · fli-core (`src/video-file.ts`, `open-args.ts`, `open-context.ts`) → v0.3.0

| Today | Proposed |
|---|---|
| `VideoFolder = { video: NN, name }`, `VIDEO_FOLDER_PATTERN = <NN>-<kebab>` | `VideoFolder = { name, style: 'named' \| 'numbered', number: NN \| null }`. `parseVideoFolder` accepts a kebab name (`named`) **or** a legacy `<NN>-<kebab>` (`numbered`, read-only). |
| `videoFolderName({ video, name })` → `01-xmen` | `videoFolderName(name)` → `flivideo-tour`. Writers never produce `numbered`. |
| `parseVideoFile(fileName)` — self-contained (`NN-kind…`) | `parseVideoFile(fileName, videoName)` — **needs the folder name**: `flivideo-tour-audio-a100.m4a` only splits into name / kind / variant once you know the name is `flivideo-tour` (names are kebab and can contain `final`, `cut`…). Strips `<videoName>-`, then reads `<kind>[-<variant>].<ext>`. For a `numbered` folder it reads today's `NN-kind…`. Unmatched → `unknown-kind`, shown, never hidden (unchanged). |
| `videoFileName({ video, kind, variant, ext })` → `01-cut.mp4` | `videoFileName({ name, kind, variant, ext })` → `flivideo-tour-cut.mp4`. |
| `--video <NN>-<name>`; refusal `video-invalid` when not `NN-name` | `--video <name>` (kebab); a legacy `01-xmen` still resolves to `videos/01-xmen/`. `video-invalid` = not kebab. `video-not-found` unchanged. |

**Two naming guards** (both in fli-core, so every app agrees):
1. A **new** video name must **not start with `<digits>-`** (`10-tips` would read as a legacy numbered folder). Writers
   refuse it; suggest `tips-10` or `ten-tips`.
2. **Legacy detection is by name shape + contents**: a folder matching `<NN>-<kebab>` whose files are `NN-kind…` is
   `numbered`; otherwise it is `named`.

Breaking API → **v0.3.0**. Every app pins a tag, so nothing changes for an app until it bumps.

## 2 · The ripple, repo by repo

| Repo | fli-core pin | Size | What changes |
|---|---|---|---|
| **FliStudio** | v0.2.2 | ~30 sites, 10 test files | `assets.ts` video scan reads both styles; `export.place` names by `videoFileName({ name,… })`; `VideoGroup` carries style; client shows name (no `NN` column) and sorts by name; e2e fixtures `01-xmen` kept as the legacy case + a named fixture added. Spec: new **D-row superseding the 09-09 video shape**; `L1`/`L3` wording. |
| **FliCut** | v0.2.3 | ~20 src sites, 6 test files — **the real work** | Export names `<NN>-cut.mp4` → `<name>-cut.mp4`, audio arms `<name>-audio-<token>`; decision file `fli.cut.<NN>-<name>.json` → `fli.cut.<name>.json` (+ sidecar folder); `contractEditFile` / `videoOfEditFile`; the picker's `parseVideoFolder` gate; UI strings. |
| **FliCast** | **v0.1.0** | ~5 sites, 4 test files | Open-contract validation and messages only. **It writes nothing to `videos/` today** (no "point 6" export exists, no `nextVideoNumber`) — so its future export just uses `videoFolderName` / `videoFileName` from the start. |
| **FliHub** | v0.2.3 | ~4 sites | Open-contract schema/messages; one test (`openContract.test.ts:309`, `video: 'intro'` → today refused) **flips to accepted**. Its `padStart(2)` are chapter numbers and project codes — untouched. |
| **Teletubby** | **v0.1.0** | 0 | Passes `--video` through; never reads `videos/`. Bump only to stay current. |

## 3 · Order (readers before writers — nothing breaks between steps)

1. **fli-core v0.3.0** — reads both styles, writes named. Tests: both styles, the ambiguity guard, names containing kind
   words (`the-final-cut/the-final-cut-final.mp4`), legacy folders (`first-edit`) never parse as videos.
2. **FliStudio** bumps and reads both — so a named folder shows as a video the moment anyone writes one. (Even before
   this, it would show as an unrecognised `videos/` entry — never hidden.) `export.place` then writes named.
3. **FliHub** bumps (open contract only).
4. **FliCut** bumps last among writers, with its migration (§4).
5. **FliCast** and **Teletubby** bump v0.1.0 → v0.3.0 when convenient (FliCast before its first `videos/` export).

## 4 · What makes this risky — from the code

1. **FliCut's saved state is keyed by the number.** `fli.cut.01-xmen.json` + its sidecar folder, `deliveredTo` /
   `last-export.json` paths, and the "refuse re-export without overwrite" check all use numbered names. Without a
   migration they drop out of FliCut's picker. *Mitigation*: FliCut keeps reading `numbered` edits as legacy (never
   migrated without David), and only new edits are named.
2. **The number is what tells a video from a legacy folder today** (FliCut `edit-location.ts:101`,
   `open-context.ts:292`). Without it, `first-edit/` or `edits/` could parse as a video. *Mitigation*: legacy folder
   names (fli-core `LEGACY_FOLDERS`, `-`-prefixed) never parse as videos, and videos are only read **inside `videos/`**.
3. **Order is lost.** `01-main`, `02-short` sorted by intent; names sort alphabetically. Accepted by the ruling
   ("having a number … maybe not"); a sort control is later.
4. **Renaming a video renames every file in it** (the name is on each file). Needs a `video.rename` in FliStudio (like
   `project.rename`) before anyone renames by hand.
5. **Version skew**: FliCast and Teletubby jump v0.1.0 → v0.3.0, pulling in the hub layout too — harmless for them, but
   it should be its own commit with their tests run.

Nothing here makes the ruling a bad idea. **Measured 2026-09-22 (M4): no live project has a `videos/` folder** — the
only `videos/` folders are `v-*/catalog/videos/` and `published/*/videos/`, which are not projects (and `catalog/`
already names folders by slug, not number). So there is **nothing numbered to migrate** on this machine; the legacy
`numbered` read path exists for other machines and for FliCut's existing `fli.cut.<NN>-<name>.json` edits. The one
question for David: **once every machine is checked, can the `numbered` read path be dropped entirely**, rather than
kept as legacy?
