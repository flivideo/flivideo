---
created: 2026-11-04
timestamp: 2026-11-04T11:00+07:00
---
# Speed control — phase 1 implementation plan + phase 2 matrix (2026-11-04)

**Purpose**: How to build the one 3-visible speed control across the four players, and the phase 2 matrix of shared playback controls.
**For Agents**: Plan only (M2, no code edited). Inputs: `docs/research/speed-control-decisions-2026-11-04.md` (David's rulings), the four players, fli-core `transport.ts`, and `origin/help-system` of fli-core + flistudio (read 2026-11-04). Line numbers are from each repo's checkout on this machine today.

## Verdict
Phase 1 is **small in code, wide in files**. The control is ~one component + one pure helper; the cost is moving four consumers and
rewriting the tests that assert "ten buttons". Two findings change the shape of the plan:

1. **FliHub is not on the ladder, and not on fli-core in the client.** FliHub's client has no `@flivideo/core` dependency (only
   `flihub/server/package.json:19` pins v0.26.0). Its presets are `[1, 1.5, 2, 2.5, 3, 4]` with default **2×**
   (`flihub/client/src/hooks/useVideoPlayback.ts:10-11`) and it has **no J/K/L at all** — `useVideoPlayback.ts:68-87` handles only Space and Escape.
   "J/K/L unchanged" is therefore *new behaviour* in FliHub, not a no-op.
2. **FliCut has no speed buttons today.** It has only the `SpeedBadge` (Player.tsx:207, shown when rate ≠ 1×) and the readout (Player.tsx:188-192),
   driven by J/K/L plus a **second, different ladder** `RATES = [0.5, 0.75, 1, 1.25, 1.5, 2, 3]` on `[` `]` (`hotkeys.ts:87-93`; Editor.tsx:563-565).
   So FliCut gains a control; it does not swap one.

## Dependency: where shared React UI lives (help-system-dev)
Read from `origin/help-system` (fli-core `7f23961`, flistudio `8880c9d`) — **help-system-dev has not chosen a fli-core UI layer.** What it did:
- **fli-core gets framework-free data only**: `src/help.ts` (`HELP_SCREENS`, `searchHelp`, `tip()`, `speedTip(triage)`), exported on `./contracts`. No React, no DOM.
- **The React skin lives in flistudio**: `extension-core/src/help.tsx` (`HelpSheet`, `HelpButton`), imported as `@flivideo/extension-core/help`
  (`Viewer.tsx` on that branch, line 4/440). FliCut (Electron, not in flistudio's workspace) and FliHub cannot import that.
- fli-core `package.json` exports today: `.` and `./contracts` only; deps: `zod` only; no `react`, no JSX in `tsconfig.build.json`.

**So for the speed control the choice is still open.** I plan for both and pick one:

| | A. `@flivideo/core/ui` subpath (**pick**) | B. sibling package `@flivideo/ui` |
|---|---|---|
| What | New `./ui` export in fli-core; `react` as an **optional peerDependency**; JSX compiled in the same build | New repo/package, depends on fli-core |
| For | One repo, one version pin, one `git+` install the apps already do (`github:flivideo/fli-core#vX`); David's ruling says "fli-core's UI layer" | Keeps fli-core framework-free (its "no React" rule stays absolute); fli-core consumers that never render UI pay nothing |
| Against | Breaks fli-core's framework-free stance unless `./ui` stays strictly isolated (the architecture test at `fli-core/test/architecture.test.ts` would need a rule: `ui/` may import `react`, nothing else may) | New repo, new release cadence, one more `github:` pin in 4 apps |
| Cost | +~1 step (arch-test rule, tsconfig `jsx`, `@types/react` dev dep) | +~2 steps (repo, CI, publish) |

**I'd pick A**, with `ui/` fenced by an architecture-test rule and *only the speed control* in it for phase 1. Reason: David already said "fli-core's UI layer";
the install path already exists in all four apps; B is the move if phase 2 grows a lot of UI. **Whichever help-system-dev finally picks, speed goes in the same place** — if it
picks B, step 1 below targets that package instead and nothing else changes. Re-check `origin/help-system` before building.

**Styling** is the second constraint: FliStudio/Story Pilot use plain CSS (`.fs-ctl__speeds`, studio.css:1373), FliCut and FliHub use Tailwind with different palettes.
The component therefore ships **unstyled-by-default with stable class hooks** (`fli-speed`, `fli-speed__rate`, `fli-speed__edge`, `…is-active`, `…is-disabled`) plus an
optional `@flivideo/core/ui/speed.css` that uses CSS variables (`--fli-speed-bg/fg/active`). Each app maps the variables once. No Tailwind inside fli-core.

## 1. Phase 1 plan

### The shared pieces (fli-core)
**Pure helper** (framework-free, in `src/transport.ts` next to `FORWARD_SPEEDS`, exported on `./contracts` so non-React callers and tests can use it):
```ts
speedWindow(rate: number, visible = 3, ladder = FORWARD_SPEEDS)
  → { rates: number[]; start: number; canBack: boolean; canForward: boolean }
```
- Window = `visible` consecutive rungs, **centred on the active rate**, clamped so it pins at `0.25×` (first rung) and `4×` (last rung) — at the pins the window slides, it does not shrink.
- Off-ladder rate (FliCut's 1.25× from `[`/`]`, or a stale localStorage value): window is built around the **nearest rung**, and the control shows no active rung (same snap `jkl()` already does, `transport.ts:36-39`).
- Chevron paging: ‹ / › move the *window* one rung or move the *rate* one rung? **My take: they step the rate** (what the mocks showed as the chevron = slower/faster, same as J/L), so the lit rung stays in the middle. Ruled-in mock is the source — see question Q1.

**Component** `SpeedControl` in the UI layer:
```ts
interface SpeedControlProps {
  value: number;                       // current rate
  onChange: (rate: number) => void;    // user clicked a rung or a chevron
  visible?: number;                    // default 3
  ladder?: readonly number[];          // default FORWARD_SPEEDS
  disabled?: boolean;                  // no media loaded
  triage?: boolean;                    // Footage triage viewer: K is keep → tooltip drops "K 1x" (speedTip(true))
  className?: string;
  'data-testid'?: string;              // each player keeps its existing id: viewer-*, sp-listen-speed
}
```
- Renders `[‹] [r1] [r2*] [r3] [›]`; `‹` gets `disabled` + `aria-disabled` when the active rate is `0.25×`, `›` at `4×` ("that chevron greys out").
- Rungs are `<button aria-pressed>` (keeps the pattern every test already uses).
- **Tooltips and the ? sheet**: container `title`/`aria-label` = `speedTip(triage)` (already on `origin/help-system`, `fli-core/src/help.ts`); chevrons `tip('Slower','J')` / `tip('Faster','L')`.
  No inline key text (David's rule) → the `.fs-ctl__keys` spans go. The ? sheet already has the rows (`SPEED` row in `HELP_SCREENS`); nothing new to add for FliStudio. FliCut's own `Help.tsx:39` row stays until FliCut moves onto the shared help data (separate follow-on, noted in `help.ts` header).
- Pure presentational + controlled. **It does not bind keys.** J/K/L stay where they are in each player (all four already route through `jkl()`, except FliHub which gets it in its step).
- FliCut's `±8×` reverse stays its own badge: the control renders in an optional `trailing` slot, or FliCut renders `SpeedBadge` beside it (FliCut step 4). Not in the shared component.

### Per-player changes
| # | Player | Stack | Files | What changes |
|---|---|---|---|---|
| P1 | **FliStudio Viewer** | AppyStack web | `flistudio/client/src/components/Viewer.tsx:386-398` (the `.fs-ctl__speeds` block incl. `viewer-speed-keys` span), `Viewer.tsx:33` (`SPEEDS` const may go), `flistudio/client/src/styles/studio.css:1373-1385` | Replace the ten-button map with `<SpeedControl value={prefs.speed} onChange={s => set({speed:s})} triage={!!marks}/>`. Drop the keys span. Key handling (`speedKey`, line 169-175, 249) untouched. CSS: keep `.fs-ctl__speeds` only for the Size group (line 399); map the new variables. `help-system` already edits this region — **rebase on it first** (see order). |
| P2 | **Story Pilot Listen** | AppyStack web (inside FliStudio) | `flistudio/modules/storypilot/client/Listen.tsx:439-456` (block), `:18` (`SPEEDS` export — check importers), `storypilot.css:1235` | Same swap, `data-testid="sp-listen-speed"` kept. `setSpeed` (312-321) and `readSpeed` (20-24) unchanged. Drop `sp-listen-speed-keys` span (already removed on `origin/help-system`, replaced by `title`). |
| P3 | **FliHub** playback modal + WatchPage | AppyStack web, **no core in client** | `flihub/client/src/components/shared/SpeedControl.tsx` (replace/delete), `shared/VideoControlsBar.tsx:10,136`, `hooks/useVideoPlayback.ts:10-11,40-48,68-87`, `components/WatchPage.tsx:47,59,171-177`, `shared/VideoPlayerModal.tsx:80-82,241-242`, `flihub/client/package.json` (+`@flivideo/core`) | (a) Add `@flivideo/core` to the client; (b) `SPEED_PRESETS` → `FORWARD_SPEEDS`; (c) add J/K/L to `useVideoPlayback` via `jkl()` (new behaviour); (d) swap `SpeedControl` for the shared one. **Two things need David**: the stored default is **2×** (`DEFAULT_SPEED`) and the `localStorage` key `flihub:watch:playbackSpeed` holds `1.5/2/2.5/3/4` values — all still on the ladder, so no migration; keep 2× default? (Q2). |
| P4 | **FliCut Player** | Electron (AppyTron), Tailwind | `flicut/src/renderer/src/Player.tsx:179-192` (control row: play button, timecode, readout), `Player.tsx:207-225` (`SpeedBadge`), `Editor.tsx:756` (second `SpeedBadge` use), `Editor.tsx:563-565`, `hotkeys.ts:87-93` (`RATES`/`nextRate`), `flicut/package.json:33` (core pin) | Add `<SpeedControl>` into the Player's control row (the row at Player.tsx:179); bridge `onChange` → `setView({playbackRate})` the same path J/L use (Editor.tsx:483-487). Keep `SpeedBadge` for reverse (`reverse !== null`) — it already hides at 1×. **`[`/`]` and `RATES` decision (Q3)**: either retire `RATES` so `[`/`]` use the shared ladder, or leave it and accept off-ladder 1.25×. |

How the Electron and AppyStack apps consume it: identical. Both already install fli-core by `github:flivideo/fli-core#<tag>` (flicut v0.28.0, flistudio v0.29.0, flihub server v0.26.0).
The renderer is plain React 18 (FliCut) / React 19 (FliStudio, FliHub) — the peer range must be `^18 || ^19`. FliCut's renderer imports `@flivideo/core/contracts` already (hotkeys.ts:84), so a `./ui` import is the same pattern.
Versions: this is a **minor bump** of fli-core (new exports), then each app bumps its pin.

### Tests that assert the current buttons (to rewrite)
| Where | Line | Asserts | Becomes |
|---|---|---|---|
| `flistudio/modules/storypilot/client/screen.test.ts` | 869-896 | "speed: the clip viewer's ladder" — exact ten labels `0.25x … 4x` in `sp-listen-speed`, click `2x`, `aria-pressed` | 3 visible around the active rate; click a rung / chevron to reach 2×; ladder itself asserted in fli-core, not here |
| same | 901-923 | `sp-listen-speed-keys` text (on `origin/help-system` already → `title` attr, line ~907) | the container `title` = `speedTip()`; chevrons titled |
| `flistudio/client/src/components/Viewer.test.tsx` | 154-231 | `lit()` filters pressed buttons ending `x` → `['1x']…`: **still valid** (active rung always visible) | keep; one assertion that exactly 3 rungs are in the DOM |
| same | 189-196 | clicks `3x` straight from the default (button no longer in window), then asserts `viewer-speed-keys` text (195) | step to 3× by chevron/keys first; text assertion → `title` |
| same | 207-231 | triage: `viewer-speed-keys` = "J slower · L faster" (231) | `title` = `speedTip(true)` |
| `flistudio/e2e/storypilot-listen.spec.ts` | 275-278 | clicks `2x` button by name | 2× is **not visible from 1×** (window 0.75/1/1.5) → click `›` twice, or press `l` |
| same | 348-362 | `on()` reads the pressed button; clicks `2x` at 355-358, then `k`/`l` | `on()` still works; replace the `2x` click with chevrons |
| `flicut` | — | **No test touches Player speed UI** (`flicut/test/` has no Player/SpeedBadge test; grep'd `speed-badge`, `SpeedBadge`) | new: a Player test for the control + the pin edge |
| `flihub` | — | **No test touches SpeedControl/WatchPage/VideoPlayerModal** | new: component test + J/K/L in `useVideoPlayback` |
| `fli-core/test/transport.test.ts` | 14-47 | ladder + `jkl` | keep; add `speedWindow` cases (middle, both pins, off-ladder) + arch-test rule for `ui/` |

Flag: if the arrows don't step the rate (Q1), the e2e clicks need `page.getByRole` on the revealed rung instead.

### Order of work (and machine)
All on **M2** (build default; unwatched; `help-system` also is on the M2 per this brief). Run via `flivideo-orch`.

| Step | Work | Size | Blocks |
|---|---|---|---|
| 0 | Wait/confirm `help-system` merged (or at least rebase on `origin/help-system`: it edits Viewer.tsx, Listen.tsx, both tests and `storypilot.css`, and adds `speedTip`) | S | everything in flistudio |
| 1 | **fli-core**: `speedWindow()` + tests; `./ui` export (`SpeedControl.tsx`, `speed.css`), peer dep, tsconfig `jsx`, arch-test rule, README + CHANGELOG, minor tag | **M** (≈½ day) | 2–5 |
| 2 | **FliStudio**: bump pin, P1 Viewer + P2 Listen + CSS + tests (unit + e2e rewritten per table) | **M** | — |
| 3 | **FliHub**: add core dep to client, ladder swap, J/K/L in the hook, swap control, new tests | **M** | David's Q2 |
| 4 | **FliCut**: bump pin, add control to Player row, keep reverse badge, resolve `RATES`/`[ ]`, new Player test | **M** | David's Q3 |
| 5 | Run each app's real UI (FliStudio Viewer + Listen, FliHub modal, FliCut) — David's "done" = he has run it | S each | — |
Steps 2, 3, 4 are independent once 1 lands (parallel). Total ≈ 2–3 working days of agent time; steps 2+3+4 are the long pole.
Show David the shared component's look (one screenshot per app skin) **after step 1 and before 2–4** — his decisions say "plan first, show David before code".

### Still David's call
- **Q1** Chevrons: step the *rate* (my take, J/L-equivalent, lit rung stays centred) or *page the window* (shows 3 more rungs, rate unchanged until clicked)?
- **Q2** FliHub default speed stays **2×** (current) while others default 1×? (My take: keep 2× — it's a viewing habit; the default is per-app config, not part of the control.)
- **Q3** FliCut `[` `]` and its `RATES` ladder (adds 1.25×, drops 0.25×/2.5×/3.5×/4×): retire it (shared ladder everywhere), or keep it? (Take: retire; one ladder is the point.)
- **Q4** Package choice A (`@flivideo/core/ui`, my pick) vs B (sibling) — confirm once help-system-dev decides.
- **Q5** Do FliHub's WatchPage *and* modal both get it (they share `VideoControlsBar`, so yes by default)?

## 2. Phase 2 matrix — shared playback controls
Cell format: **has it?** (file:line) · what it calls "next". ✗ = absent. FliHub is the reference set.

| Feature | FliHub (modal + WatchPage) | FliStudio Viewer | Story Pilot Listen | FliCut |
|---|---|---|---|---|
| **Auto-next** | ✓ toggle "Auto Next" `shared/VideoControlsBar.tsx:156-164`; on end → `playNextSegment` `WatchPage.tsx:393`, persisted `flihub:watch:autonext` `:62,:223`. Calls it **segment** (chapters contain segments). | ✓ "Auto next" `Viewer.tsx:419`, on `onEnded` `:291-293`, pref `autonext` `:39,:55`. Next = **item/file** in the list. | ✓ checkbox "auto-next" `Listen.tsx:435-437`, on `ended` `:191-200`, key `storypilot:listen:autonext` `:15`. Next = **paragraph** (`nextOf`, `:167`), across chapters. | ✗ (one project timeline; no list). "Next thing" = **cut** (`nextCut`, `hotkeys.ts:60`, ⌥→). |
| **Transcript display** (word / phrase / off) | ✓ `TranscriptSyncPanel` `WatchPage.tsx:752`, `VideoPlayerModal.tsx:271`; collapse `:211`. Word/phrase not a user switch here. | ✓ pill by word (or line); show/hide `prefs.transcript` `Viewer.tsx:42,:58,:428-432`; synced `:313`. | ✓ word highlight in the script text (`words`, cue via `cueOfWords` `:4`, `:128`); no off switch (it *is* the script). | ✓ caption strip, current + next **phrase** with word lit `Player.tsx:180,:235-253`; hidden in inverse mode `:180`. No user off. Script panel (`Script.tsx`) is separate. |
| **Autoplay** | ✓ toggle `VideoControlsBar.tsx:144-152`; `flihub:watch:autoplay` `WatchPage.tsx:61,:217` | ✓ "Autoplay" `Viewer.tsx:413`, pref `:38,:54` | ✗ (plays on Play / click of a paragraph) | ✗ (plays on Space) |
| **Size** (N / L) | ✓ `SizeToggle` `VideoControlsBar.tsx:15,:140` | ✓ N/L `Viewer.tsx:41,:57,:323,:399-402` | ✗ (audio player — no picture) | ✗ (fixed aspect by project, `Player.tsx:161`) |
| **Info** (duration, file size) | ✓ modal `VideoPlayerModal.tsx:255-261` (`formatDuration`, `formatFileSize`); WatchPage shows filename + counter `:634` | ✓ time / duration + `bytes(item.file.size)` `Viewer.tsx:381-384` | ✓ "¶n/N" + audio state `Listen.tsx:457-469` (no file size) | ✓ timecode `current / total` `Player.tsx:185-187`; no file size (it is a timeline) |
| **Prev / next buttons** | ✓ ← → with disabled edges `VideoControlsBar.tsx:85-111` (titles "Previous (←)", "Next (→)") | ✓ "Previous"/"Next" with "(n/N)" `Viewer.tsx:358-368`; ←/→ keys | ✓ "Previous/Next paragraph" `Listen.tsx:385-406`; ←/→ in title | ✗ buttons; cuts via ⌥← ⌥→ (`hotkeys.ts` HOTKEY_HINT `:96`). |
| **Play button** | ✓ `PlayPauseButton` `VideoControlsBar.tsx:100` | ✓ `viewer-play` `Viewer.tsx:377` | ✓ `sp-listen-play` `Listen.tsx:396-399` | ✓ ▶/❚❚ `Player.tsx:182` |
| **Space = play/pause** | ✓ `useVideoPlayback.ts:77` (modal + WatchPage) | ✓ `Viewer.tsx:250-253` (AV only) | ✓ `Listen.tsx:266-268` | ✓ `hotkeys.ts:123` (plays around the cut inside the loupe) |
| **Speed (phase 1)** | ✓ 6 presets, no JKL | ✓ 10 buttons + JKL | ✓ 10 buttons + JKL | badge + JKL only |

**Names for "the next thing"**: FliHub *segment* · Viewer *item* (file) · Listen *paragraph* · FliCut *cut*. The control has to be labelled per player, not shared as one word.

**What to share first (paragraph)**: Share **Space = play/pause + prev/next/play** first. It is the one row where all four already behave the same, so it is a
true no-op for users and only removes four implementations; the shared piece is a tiny "transport row" (play, prev, next, disabled edges, labels via a `nextLabel` prop —
segment / item / paragraph / cut). Then **auto-next + autoplay** (three of four have it, all persist a boolean to `localStorage` with different keys — one hook with a `storageKey`
prop). Leave transcript display and size for last: they differ in kind (pill vs caption strip vs highlighted script; picture size doesn't exist for Listen) and each is a rendering
decision, not a control. Info (duration/size) stays per-player — different data. Prerequisite for any phase 2 sharing in FliHub: **it needs `@flivideo/core` in its client**, which phase 1 step 3 adds anyway.
