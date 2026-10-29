# Overnight build — 2026-10-29: templates, fli-core v0.26, pins, whole-video names and owners

**Purpose**: One coordinated overnight build on the M4, run by `flivideo-orch`. Upgrade the templates' dependencies (no majors), bring FliStudio level with its template, release fli-core v0.26 as a release candidate, move every app onto it, retire `-final` writes, and give whole-video files one owner rule.

**For Agents**:
- You are `flivideo-orch` (the boss). You plan, launch builders, reproduce their gates, and park what cannot pass. You do not build.
- David approved this run in chat on 2026-10-29 ("go"), with the authority in §2. **He is asleep: do not ask him anything.**
- Background and reasoning: `/Users/davidcruwys/dev/ad/flivideo/docs/architecture-review-2026-10-29.md` (§1.1–1.4).
- Written by `flivideo-arch-rsch`.

---

## 1 · Done condition

The run is done when every item W1–W7 is **✅ gate passed** (branch pushed, evidence in the report) or **⏸ parked with a written reason**, and the morning report (§6) is committed and pushed to the flivideo repo. Stop there.

## 2 · Authority

**Allowed:**
- Create worktrees under each repo's `*-worktrees/` folder, on branches named `overnight/2026-10-29-<item>`.
- Commit to those branches and push them.
- In fli-core only, push the tag `v0.26.0-rc.1` on the W3 branch commit. Consumers pin it; `main` is untouched.
- Choose libraries and test design within each repo's existing stack, and decide anything the brief leaves open. Record each decision in the report.

**NOT allowed. If an item needs one of these, park it and say why:**
- Merging or pushing to `main` in any repo. David merges in the morning.
- Touching a live checkout: `flistudio/`, `flicut/`, `flihub/`, `flicast/`, `fliedit/`, `teletubby/`, `flitools/`, `fli-core/`, `apps/appystack/`, `apps/appytron/` themselves.
- Starting, stopping or restarting any app (FliStudio, FliCut, FliHub, FliTools above all), or `my-app`. No `pkill -f` or `killall`.
- Running a dev server in a worktree on ports 7150, 7151, 7121, 7161, 5173 or 5101. Use the test runner only; anything that must listen gets a random port.
- Running `appystack-upgrade` or the AppyTron upgrade engine against any app. Both overwrite app files silently (review §1.4).
- Any major version change.
- Any change to `/Users/davidcruwys/dev/video-projects/`, `~/.config/appydave/`, or `~/.claude/`.
- The extension-core refactor (review §5). It is tomorrow's work, with David.

## 3 · Gate rule (every item)

1. **Baseline first:** in the fresh worktree, before any change, record the typecheck error count, unit test pass/fail counts, lint and build results.
2. **After the change:** typecheck errors ≤ baseline, tests pass ≥ baseline with **no newly failing test**, and lint/build no worse.
3. **You reproduce it:** run the gate commands yourself in the builder's worktree; never trust a builder's word.
4. **Flaky tests** already known (`requestLogger`, `hear-it`, `fc37-inputs`) may fail if they also fail at baseline; say so.

## 4 · Items, in order

Order: W1 and W2 can run in parallel, W3 must finish before W4–W6, and W7 is independent. At most 3 builders at once. Sonnet for W1/W2/W7, Opus for W3–W6.

### W1 · AppyStack template: patch/minor dependency bumps
- **Repo:** `/Users/davidcruwys/dev/ad/apps/appystack`, branch off `main`. **Never touch `spaghetti/step3-wip`.**
- **Do:**
  - Bump every outdated dependency in `template/` (all workspaces) to its latest **within the same major**. Examples: express 5.3, socket.io 4.8.4, react 19.3.1, tailwind 4.3.3, vitest 4.1.12, playwright 1.64.1, typescript-eslint 8.72.1.
  - Same for `create-appystack/`.
  - Then `npm run sync`, so `create-appystack/template` equals `template/` (it is stale today).
- **Excluded majors:** vite 8, @vitejs/plugin-react 6, vitest 5, typescript 7, zod 4, eslint 10, @eslint/js 10, react-hooks 7, msw 3, pino 10, pino-http 11, dotenv 18, jest-dom 7, globals 17, @types/node 26.
- **Done when:**
  - `git diff` of every package.json shows no changed major;
  - typecheck, lint, format:check, build and the root `npm test` pass in `template/`;
  - `diff -r template create-appystack/template` (excluding node_modules) is empty;
  - `create-appystack` tests pass.

### W2 · AppyTron template: patch/minor dependency bumps
- **Repo:** `/Users/davidcruwys/dev/ad/apps/appytron`. This is the canonical repo; `appytron-factory` is a leftover worktree, so ignore it.
- **Do:**
  - Bump within the same major: react 19.3.1, vitest 5.0.5, zustand 5.0.16, electron-updater 6.8.11, electron-builder 26.18, prettier 3.9.10, vite 7.3.7, @types/node 24.19.
  - Electron 44.3 → 44.10 is allowed **only if** build and tests pass. Otherwise keep 44.3 and say so.
- **Excluded majors:** electron 45, electron-vite 6, vite 8, plugin-react 6, typescript 7, and create-appytron's vitest 2 → 5.
- **Done when:**
  - no major changed;
  - `template/`: `npm run typecheck`, `npm test` and `npm run build` pass;
  - `create-appytron`: `npm test` and `npm run typecheck` pass.
- **Out of scope:** upgrading the four AppyTron apps. The engine has no scaffold baseline and would wipe each app's preload IPC bridge.

### W3 · fli-core v0.26.0-rc.1: whole-video kinds and one owner rule
- **Repo:** `/Users/davidcruwys/dev/ad/flivideo/fli-core`. Worktree off `main` (v0.25.0, `7648b9f`).
- **Ruling (by `flivideo-arch-rsch` on David's delegation, 2026-10-29):**
  - **New kinds.** A whole video made by an app is named after **how it was made**, never "final" (R11):
    - FliEdit's export is `<name>-edit.<ext>`;
    - FliCast's export is `<name>-cast.<ext>`.
    - Add `edit` and `cast` to `VideoFileKind`, each with no variant. Round-trip tests go next to the existing ones.
  - **One owner rule, in fli-core,** used by every app. Add `wholeVideoOwner(projectDir, video, file)` → `{ app: 'flicut'|'fliedit'|'flicast'|'flistudio'|null, source: string }`:
    1. **By kind, confirmed by a decision file:**
       - `cut` + `fli.cut.<video>.json` → flicut;
       - `edit` + `fli.edit.<video>.json` → fliedit;
       - `cast` + `fli.cast.<video>.json` → flicast;
       - `overlay` → flistudio ("Overlay Pilot render").
       - A kind whose decision file is missing → `{app:null, source:'placed file'}`.
    2. **`legacy` (`-final`):** exactly one of `fli.edit`/`fli.cast` for that video → that app. Both → `{app:null, source:'two candidates: fliedit, flicast'}`.
    3. **Otherwise:** if `-renders/` or `motion/` exists → `'generated render'`. Else → `'placed file'`. This keeps FliStudio's current fallback (`flistudio/server/src/capabilities/publish.ts` `finalSource`).
    4. `audio`, `part` and unknown kinds → `{app:null, source:'placed file'}` unless rule 1 is extended with evidence. The builder checks who writes them and records it.
  - **Parse:** keep `-final` as legacy-read only. `videoFileName` still cannot write it.
- **Done when:**
  - lint, typecheck and `npm test` (coverage gate) pass;
  - tests cover every row of the rule above with fixture folders;
  - CHANGELOG has a v0.26.0-rc.1 entry;
  - the branch is pushed and tag `v0.26.0-rc.1` is pushed on its head;
  - `npm view`-free check: `git ls-remote --tags origin v0.26.0-rc.1` shows it.

### W4 · Pin every app to v0.26.0-rc.1; FliCast and FliEdit stop writing `-final`
- **Repos:** flicast, fliedit, flicut, flihub (server + shared), flitools, teletubby, and flistudio (server, shared, client, `modules/overlay-pilot`).
- **Do:**
  - One worktree per repo; set every `@flivideo/core` pin to `github:flivideo/fli-core#v0.26.0-rc.1` and reinstall.
  - **FliCast:**
    - `src/main/store/package-store.ts` `videoExportPath`: use `kind:'cast'`.
    - `test/main/control-plane.test.ts:48` asserts the pin string; update it.
  - **FliEdit:**
    - `src/main/media/resolver.ts` `exportPath`: use `kind:'edit'`.
    - The owner loop at about line 92 (which checks `fli.cut`/`fli.cast`/`fli.edit` regardless of kind, last one wins) is replaced by `wholeVideoOwner`.
  - **Everything else:** fix only what the bump breaks. No refactors.
  - **FliCut, FliHub, FliTools, Teletubby:** expected trivial. Teletubby jumps from v0.7.3; read its `src/core/fli-zod.ts` before touching zod.
- **Done when, per repo:**
  - the gate rule in §3 holds;
  - `command grep -rn "kind: *'final'" <repo>/src` (or `server/src`) finds nothing;
  - every lockfile resolves `@flivideo/core` to the rc tag commit.
- Every repo that cannot pass is parked on its own; the others continue.

### W5 · FliStudio uses the owner rule
- **Repo:** the same FliStudio worktree as W4 (`overnight/2026-10-29-fli-core-026`).
- **Do:**
  - Replace `finalSource` in `server/src/capabilities/publish.ts` with `wholeVideoOwner`.
  - FliStudio recognises `-edit` and `-cast` exports as whole-video candidates.
  - The `PublishExport['app']` type gains `flicast`/`flicut`/`flistudio` if it lacks them.
  - The `export.place` description in `shared/src/contracts.ts` (around line 3378) still lists `final`; fix the text.
  - Regenerate the schema mirror if FliStudio's checks require it.
- **Done when:**
  - the §3 gate holds;
  - there is a new test: a project fixture with `fli.cast.<v>.json` + `<v>-cast.mp4` shows `app:'flicast'`, and one with a legacy `-final` and both decision files shows "two candidates".

### W6 · FliStudio level with its template (hand merge, no upgrade tool)
- **Repo:** a FliStudio worktree, branch `overnight/2026-10-29-template-sync`, off FliStudio `main`.
- **Do:**
  1. `appystack.json`: set `scaffoldCommit` to `522079a` (the real scaffold; `28d3805b…` exists nowhere) and `version` to the W1 template's create-appystack version. Set `lastUpgrade` to the run date.
  2. Take the template's `server/src/config/logger.ts` change: it is unchanged in FliStudio since scaffold, so it is a pure template fix.
  3. Do **not** re-add `client/src/hooks/useSocket.ts`; FliStudio deleted it in `1fb3d1d`. Keep FliStudio's own `rateLimiter.ts`, `requestLogger.ts`, `validate.ts`, `ci.yml` and `eslint.config.js`. They are app-modified (zod 4 `.issues`, polled routes).
  4. Recipe skill files under `.claude/skills/recipe/`: take the template's version only where FliStudio's copy is unchanged since `522079a`.
  5. Bump FliStudio's dependencies to the **same patch/minor set as W1**. No majors. FliStudio is already ahead on zod 4; keep it.
  6. Write `docs/template-sync-2026-10-29.md` in the worktree: one row per template-owned file, with taken / kept-app / merged and the reason.
- **Done when:**
  - the §3 gate holds, including FliStudio's e2e suite if it runs headless with no fixed ports (the known 390px e2e failure is baseline);
  - `git diff --stat` touches only the files in that table, package.json files and lockfiles.
- **Depends on W1** (it uses W1's versions). If W1 parks, W6 still does steps 1–4 and 6.

### W7 · Marker and doc truth (small)
- **Do**, each on its own branch:
  - `appytron.json` `core` in flicut, flicast and fliedit → `"file:vendor/appydave-core-0.1.0-791e1c9.tgz"` (what package.json actually uses).
  - In fli-core, add `window-state.ts` to the W3 branch: it uses fli-core's own `atomicWrite` instead of its hand-rolled tmp-rename (non-hidden temp, millisecond collisions, no cleanup).
- **Done when:**
  - each `appytron.json` value equals the app's package.json `@appydave/core` spec;
  - fli-core tests pass with `window-state.ts` importing `atomicWrite` from `./fs-utils.js`.

### W8 · `fli.brand.json`: no lost updates between FliHub and FliStudio (CONFIRMED 2026-10-29)
- **Evidence:** in `scratchpad/race/race.mts` (session flivideo-arch-rsch; summarised in review §1.3), scenario S1 loses the update with no simultaneous clicks:
  1. FliHub's Brand Config panel is loaded;
  2. a publish change is applied in FliStudio;
  3. Save is clicked in FliHub;
  4. FliStudio's change and its `_meta.history` stamp are lost.
  The cause: FliHub posts its whole cached `publish` block, and neither app locks.
- **Do:**
  - **fli-core, on the W3 branch, before tagging rc.1:**
    - export `takeLock` (it exists in `src/fs-utils.ts:110`, but is not exported);
    - add `updateBrandSettings(brandRoot, mutate)`, which takes `fli.brand.json.lock`, re-reads inside the lock, applies `mutate`, writes atomically and releases;
    - export `brandSettingsVersion(file)`, a sha256 of the file bytes.
  - **FliStudio (W4/W5 worktree):** `brand-publish.ts` `applyPublish` (around line 226) and `youtube.ts` `setBrandPlaylists` (around line 238) write only through `updateBrandSettings`.
  - **FliHub (W4 worktree):**
    - `managedBrandConfig.ts` `writeManagedPublish` writes through `updateBrandSettings`;
    - GET `/api/poem-wui/brand-config` returns `version`;
    - the POST (`routes/poem-wui.ts` around line 290) must send back the `version` it loaded, and the server refuses `409 changed-elsewhere` if the file changed since;
    - `ConfigPanel.tsx` shows "Changed in another app — reload" on 409.
    - This is optimistic concurrency: it fixes S1, and the lock fixes S2/S3.
- **Done when:**
  - the §3 gate holds in fli-core, FliStudio and FliHub;
  - there are new tests:
    - fli-core: two concurrent `updateBrandSettings` both survive;
    - FliHub: a stale `version` → 409, and the file is untouched;
    - FliStudio: `applyPublish` runs under the lock;
  - the race script's S1–S3 scenarios, rerun against the branch code, lose nothing.
  - The script is `/Users/davidcruwys/dev/ad/flivideo/docs/runbooks/brand-race/race.mts`.
  - Its imports point at the live checkouts (read-only). Copy it into a worktree and repoint lines 7–10 at the W4/W8 worktrees.
  - It only ever writes temp copies of the brand file (`REAL` is read, never written). Keep it that way.
- **Out of scope:** fli-core stripping unknown keys on write. It is noted in the review; today's file has only known keys.

**W4 trap (measured):** after changing the pin, a plain `npm install` keeps the OLD commit from the lockfile. Install explicitly:
- `npm install "@flivideo/core@github:flivideo/fli-core#v0.26.0-rc.1"` (FliHub: add `-w server -w shared`; FliStudio: the four workspaces);
- then confirm `node_modules/@flivideo/core/package.json` says `0.26.0-rc.1`.

**W4 baselines (measured against v0.25, 2026-10-29):**
- **Breaks:** only FliCast and FliEdit (the `final` kind).
  - FliCast: 7 test failures (6 in `open-contract.test.ts`, caused by the cast export path silently becoming `null`, plus the pin assertion).
  - FliEdit: `exportPath` throws at runtime with no test covering it. **Add one.**
- **Clean:** FliCut, FliHub, FliTools and Teletubby are clean.
- **Known flakes under parallel load:**
  - FliCut: `hear-it`, `restart-safety-app-sh`, `start-an-edit`;
  - Teletubby: `process-supervisor`;
  - FliHub client: `recordingDelete` Undo;
  - FliTools: exits 1 from EPIPE while every test passes.
- **FliHub:** the root `npm test` chains with `&&`, so run the server tests separately.

## 5 · Watching

- Attach an iTerm window to every builder so David can see the run.
- Check each builder every 20–30 minutes.
- If a builder is 3 attempts into the same failure, park the item. Do not loop.

## 6 · Morning report

Write `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/overnight-2026-10-29-report.md`, then commit and push it on flivideo `main`. That is the only `main` push allowed; it is a docs-only repo push.

**Contents:**
1. **A table for W1–W8:** status, branch, head commit, baseline vs after numbers, and the gate commands you reproduced.
2. **Decisions made** under the delegation.
3. **Parked items**, with reasons.
4. **A merge order for David**, with exact commands:
   - fli-core first: merge, then retag `v0.26.0` on main;
   - then repin each app from `#v0.26.0-rc.1` to `#v0.26.0`;
   - then the apps;
   - **FliStudio last**, because it is live and needs `my-app restart flistudio` after `npm install` + build. Only on David's go.
5. **Worktrees to remove after merge.** Also remove the read-only check worktrees made on 2026-10-29: `*-worktrees/template-drift-check` (flicast, flicut, fliedit, teletubby) and `*-worktrees/fli-core-025-check`.
