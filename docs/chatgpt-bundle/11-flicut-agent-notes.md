<!-- FliVideo source bundle · flicut AGENT-NOTES · generated from flicut/docs/AGENT-NOTES.md -->


# FliCut — Agent Notes

Only what the code can't tell you. The rules not to break are in `CLAUDE.md` and are not
repeated here.

## Where the schemas are

Every type, Zod schema and closed set is in `docs/schema-mirror.md` (generated; `verify_mirror.py
docs/schema-mirror.json` must exit 0 — regenerate it after a schema change, never hand-edit it).
Its recorded gaps: exported scalar constants and the `z.infer` aliases of object schemas — read
those in source. Never copy a shape into prose.

- Adding an audio arm means changing BOTH `ARM_REGISTRY` (`src/shared/audio-arms.ts`) and
  `audioProfileSchema` (`project.ts`).
- Shared Fli contracts (`fli.studio.json`, `brands.json`, `labPath`, `appFileName`,
  `parseVideoFolder`): `@flivideo/core` (`fli-core`). Cite it,
  don't restate it.

## Tooling

- After any change under `src/shared` or `src/main`, run `scripts/app.sh restart` before trusting
  saves, exports or the control surface. HMR reloads the renderer but never main, and the log
  looks clean either way. Restarting repaints David's window, so the live-instrument rule in
  CLAUDE.md applies.
- Use `FLICUT_HEADLESS=1` for API-only runs. It gives the full control surface with no window
  (`src/main/index.ts`).
- The control port is 7121 (`FLICUT_CONTROL_PORT`). The port and token are both in
  `<userData>/control.json`, mode 0600. `bin/flicut` reads it: exit 0 ok, 2 refused, 3 not
  running.
- If you override `HOME` to isolate a run, also set `DEEP_FILTER_BIN` and `FLICUT_MLX_WHISPER`.
  Otherwise the audio arms stall after `hp.wav`.
- Any `FLICUT_*` override must come with `APPYTRON_HOME`. Without it, the env value gets saved
  into the real `settings.json`.
- Use `command grep`, not bare `grep -r`. The shim follows `.gitignore` and returns a clean zero for
  files it never read.
- To prove a fix, run the test against the pre-fix `src/` first and watch it fail
  (`git stash push -u -- src scripts`). Without `-u` a NEW module stays on disk and the "pre-fix"
  run silently passes.
- **`app.sh` tests must pin `FLICUT_ELECTRON_PATTERN` to a temp path** — `start`/`stop` kill FliCut's
  Electrons, so the default pattern lets a test run kill a real FliCut.
- **Never send OS keystrokes** (osascript `keystroke` / `key code`) to drive a native dialog. David
  works on this machine with Claude sessions in iTerm tabs; a missed dialog sends the keys (and an
  Enter) to whatever is frontmost. Prove UI with CDP, a unit test, or say "not screen-proven".

## Non-default conventions

- **"Cut" in identifiers means MASK.** `isCut`, `take.cut` and `cutParams` predate ADR-0001's
  vocabulary (MASK / TRIM / SPLIT / GAP). The renames (`isCut`→`masked`, `Clip`→`Segment`, …) are
  owed and deliberately deferred. Don't do them piecemeal, and never alongside a semantic change.
- **A clip's `start`/`end` are authoritative** (ADR-0002). Never reset them from the take. Several
  clips may share one take, and words resolve to a clip by midpoint through `elementsWithin`, the
  only implementation. Don't write a second one.
- **Masked clips store RAW bounds. Kept neighbours next to a mask are PADDED into it.** Before you
  read or move a boundary, work out which frame it is in (`nudgeBoundary`'s comment has the
  2026-09-07 defect).
- **User trims become SPLIT + MASK with `cutBy: 'user'`** (ADR-0003). No user gesture changes a
  source range.
- **`EPSILON` (1e-6 s) is float fuzz. `1 / project.metadata.framerate` is the model's minimum.**
  Never swap one for the other, and never hardcode a framerate. `DEFAULT_FPS` is only allowed
  where no project exists (`docs/units-contract.md`).
- **The `sha` field in history entries is a six-digit snapshot id**, not a git SHA. It kept the
  name so the renderer stayed unchanged.
- **Values imported by the renderer:** `prose.ts` is also value-imported (by `Script.tsx`), and it
  is safe because it imports types only. So is `audio-arms.ts` (by `Editor.tsx`, the export panel's
  checkboxes), which imports nothing. A new renderer-safe file must value-import nothing that
  reaches Zod; the lists in `defaults.ts` and CLAUDE.md lag the code.

## Pitfalls

- **Any new settings field needs `.default()`.** `settings.ts` falls back to defaults wholesale
  when parsing fails, which silently wipes David's saved folders.
- **When a path parameter's meaning changes, grep every caller.** `cleanWork(dir)` →
  `cleanWork(workDir)` still typechecked, and `/api/batch {clean:true}` deleted `project.json`. The
  guard that now refuses an edit folder has to stay.
- **Key per-edit state by the edit's absolute path**, never by the route that reached it. The
  legacy history dir is `_legacy/flicut/<folder>-<sha1(abspath)[:8]>` for exactly this reason.
- **`path.relative` never fails.** Contract edits need `assertInsideProject` too, or a
  `../../Volumes/T7/…` path gets written as if it were relative.
- **Only context changes reach the renderer (FC-33, open).** A control-surface write to a project
  that is open in the window isn't pushed there, and the window's next save overwrites it. Don't
  write over the API to an edit David has open unless he knows.
- **Keep audit mode off on open.** `open()` forces `inverseCuts: false`. Don't restore it from
  `viewState.json`.
- **Never let the arm be picked by a number.** Report LUFS/SNR, never rank arms, never
  auto-select one. David chose a100 by ear: the export panel ticks it (`EXPORT_DEFAULT_ARMS`,
  hard-coded) and the API cascade defaults to it. Don't add a remembered or Home-screen default.
- **Transcription only runs when a window has the edit open** (`Editor.tsx` effect). Anything that
  creates an edit for David (the hand-off) must make sure a window exists — ask Electron
  (`BrowserWindow.getAllWindows()`), never trust a remembered `hostWindow`.
- **Every new transcribe path must call `dropPlaceholderClips` first** (FC-39). `store.create` builds
  clips on a placeholder whole-file take; `applyProposals` matches by `mediaId:takeIndex` and keeps
  the stale clip, so each file plays twice.
- **`onReady` re-runs on macOS `activate`** (Dock click with no window). Anything it starts must be
  idempotent — a second control surface on 7121 hit EADDRINUSE and nulled the live one.
- **React StrictMode runs effects twice in dev.** A guard on a render-time value is stale for the
  second run (FC-38, double "already transcribing"); guard on the store's live state instead.
- **Use `identity.aspect`, not `projectIntents().aspect`**, for the project's aspect. The latter
  fills in 16:9 and hides "unset"; unset must fall back to the footage.
- **Tailwind `/opacity` on a bare `var()` colour compiles to nothing.** Every colour token needs
  its `-rgb` twin (see `index.css`).
- **`electron-builder` ships everything not excluded and ignores `.gitignore`.** Packaging has
  never been run for real (FC-32). Do a dry run and list the asar before the first DMG.

## Decisions worth knowing

- **Future B, and take-splitting is abandoned** (ADR-0002). The transcript is written only by
  transcription. Re-read the ADR before building anything that needs "one take = one clip". That
  invariant is gone on purpose.
- **Undo is lab snapshots** (ADR-0004). A `baseline: on disk` snapshot is recorded when the newest
  snapshot ≠ the disk, and it must run inside the same `serialise()` step as the write. Inside that
  step, call `recordLocked`, not `record`, which would deadlock on its own lock.
- **Legacy edits are never converted on open.** Converting one would change a live edit under
  David. Only their undo history moves to the lab.

## Scope limits

- There is no post-ASR transcript correction. The dictionary only seeds `--initial-prompt`. Where a
  correction should live is an open ADR, so don't invent a correction layer.
- Every descoped feature and unresolved question in CLAUDE.md stands. Don't resolve spec §12 items
  by guessing.

---
Longer explanation for humans: [SYSTEM.md](./SYSTEM.md). It is not loaded into agent context.
