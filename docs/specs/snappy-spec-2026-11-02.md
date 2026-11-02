---
created: 2026-11-02
timestamp: 2026-11-02T10:40+07:00
status: spec only — no repo, no code
source: Captain's Log B682 (voice) + B683 dossier §13–17, §25, §27
html: /Users/davidcruwys/dev/ad/flivideo/docs/specs/snappy-spec-2026-11-02.html
---
# Snappy — spec (2026-11-02)

**Verdict:** buildable now, small. The hard idea (named regions, the "tripod") already exists in David's ScreenTour; what is
missing is a **native** shell around it: global hotkeys, a visible outline, and a **send** step into B-Roll Pilot. One real trap
found by measurement (§4.4): AppKit and `screencapture` disagree on where y=0 is. Eight decisions for David in §9.

**Snappy in one line:** a menu-bar agent that remembers named screen regions, lets you cycle them from the keyboard with a
visible outline, snaps the active one, and *sends* the PNG (with region + group names) to B-Roll Pilot. No library of its own.

## 1. Prior art — what exists, what to keep

Searched `~/dev` (this machine is the M4 Mini, `mac-mini-m4`), the zsh aliases and David's ChatGPT history.

| # | Tool | Where | What it did | Keep / drop |
|---|---|---|---|---|
| 1 | **ScreenTour** (Python 3.14 + Textual TUI) | `/Users/davidcruwys/dev/ad/apps/screentour/` (2 commits, 1,125 lines; `CONTEXT.md` is good) | A "tripod": lock a region, press Space, get `name_01.jpg`, `name_02.jpg`… Named regions in `~/.screentour/regions.json` (name, x, y, w, h, MRU order). Per-folder sessions. Timed capture (3/5/10/15/30 s). Optional ImageMagick label. Mouse-tracker to set corners (pyobjc). Engine = `screencapture -R` | **Keep the concepts:** region as the central abstraction; names are *series* with an auto counter (that is exactly the dossier's "sequence information"); timed capture; MRU. **Drop:** the TUI (it can't show the shot, hides behind the thing you capture, "not easy to remember where it is" per its own notes), per-folder sessions, in-place labelling (destroys the original), Python 3.14. **Import** its `regions.json` once. |
| 2 | **zsh functions** `sc`, `sc_1080`, `scc`, `sct` | `/Users/davidcruwys/.oh-my-zsh/custom/aliases-screencapture.zsh` | One hand-coded rectangle per function, e.g. `screencapture -R -3590,275,2820,930 -D 1 "$1.png"`, plus many commented-out ones (code, terminal, web 720, web vertical) | **Proof of the need:** David has been hand-typing regions for years, and the coordinates go **negative** (a display left of main). Snappy replaces these. |
| 3 | **Ruby "screenshot builder"** (`bin/screenshot_builder.rb`, `lib/openai_101/tools/screen_shot/`, Mar 2024) | ChatGPT thread `2024-03-08--screenshot-builder-tool--68ad0787` — the thread is just "wait for guidance, yay" (533 bytes). **The gem was not found on disk** (searched `~/dev` to depth 5) | Nothing recoverable | Drop. Absence is *not* proven for other machines. |
| 4 | **ChatGPT threads on `screencapture`** | `~/dev/raw-intake/chatgpt/david/loose/2023-11-16--macos-screencapture-command-explained…`, `2025-06-21--screencapture-function-explanation…`, `2024-05-10--windows-screen-capture-tools…` | The CLI flag list; a 2025 multi-monitor complaint ("`-D 2` still gives the MacBook"); Windows equivalents (NirCmd, MiniCap) | **Lesson:** multi-display is the recurring pain. (The 2025 thread's claim "`-D` is ignored with `-R`" is plausible but I did not verify it; see §4.4 for what I *did* measure.) Windows is out of scope. |
| 5 | Polyrecorder / Screen Studio brain | `/Users/davidcruwys/dev/ad/brains/screen-studio/polyrecorder-capture-engine.md` | A video-recording engine study | Not relevant: Snappy is stills. |

Not found: a Swift or Rust capture tool anywhere under `~/dev`. The user's "built several in Ruby/Python/others" is
ScreenTour + the zsh functions + the lost Ruby gem.

## 2. macOS building blocks (cited)

**Capture**
- `SCScreenshotManager` (ScreenCaptureKit): `captureImage(contentFilter:configuration:)` macOS 14.0+; `captureImage(in:)` macOS 15.2+;
  `captureScreenshot(rect:configuration:)` macOS **26.0**+. [Apple data JSON for SCScreenshotManager and both methods]. This Mac is
  macOS 26.6.2 (`sw_vers`), so all three exist here. `SCContentFilter(display:excludingWindows:)` lets the capture skip our own
  windows (Apple's documented pattern; the example I fetched was from a secondary summary, not the page body).
- `screencapture -R x,y,w,h` (system CLI, `man screencapture`): measured **0.18 s** for a 400×300 region on this Mac;
  Retina handled (400×300 pt → 800×600 px on the 2× main display). Needs the same Screen Recording permission.
- `CGWindowListCreateImage` (legacy): I could not confirm its deprecation status — Apple's page needs JavaScript and the data
  endpoint returned nothing. **Do not build on it** regardless.

**Permissions** (TCC)
- Screen & System Audio Recording is required for capture. `CGPreflightScreenCaptureAccess()` / `CGRequestScreenCaptureAccess()` check and ask.
- macOS 15 (Sequoia) re-prompts monthly for screen-recording apps, reported to include ScreenCaptureKit apps
  ([9to5Mac](https://9to5mac.com/2024/08/14/macos-sequoia-screen-recording-prompt-monthly/),
  [TidBITS](https://tidbits.com/2024/08/19/apple-reduces-excessive-sequoia-permission-requests-shifts-to-monthly)).
  2024 reporting; **I did not verify behaviour on macOS 26** — spike S1 should.
- A permission is granted to a *binary/bundle identity*. A CLI run from iTerm borrows iTerm's grant; a proper signed `.app`
  holds its own and keeps it across rebuilds only if the signing identity is stable (general macOS behaviour, not tested here).

**Global hotkeys**
- Carbon `RegisterEventHotKey`: reported (crate docs, a Dev.to write-up) to be the one global-hotkey API that needs **no**
  Accessibility / Input Monitoring prompt; caveat reported that it can lose to a frontmost app that consumes the key.
  `CGEventTap` needs Input Monitoring. Sources disagree on details; third-party, not Apple docs.
  ([Rust `global-hotkey` docs](https://docs.rs/global-hotkey/latest/global_hotkey/) — event loop + manager must live on the main thread.)

**Overlay (the outline)**
- A borderless, click-through, floating `NSWindow` on every screen draws the frame. The catch: community reports say
  `sharingType = .none` **no longer hides a window from ScreenCaptureKit on macOS 15+** (legacy APIs still honour it), with no
  official Apple statement
  ([Apple forum thread](https://developer.apple.com/forums/thread/808016), [write-up](https://www.producthunt.com/p/jobpath/how-apps-hide-windows-from-screen-capture-and-what-broke-in-macos-15)).
  So **do not rely on window flags to keep the outline out of the shot** — see D5.

**Language: Rust vs Swift**
| | Rust | Swift |
|---|---|---|
| Capture | `screencapturekit` 11.1.1 (updated 2026-10-26), `objc2-screen-capture-kit` 0.3.2, `xcap` 0.9.8, `scap` 0.0.8 (stale) | first-class |
| Hotkeys | `global-hotkey` 0.9.0 (updated 2026-10-16, 7M downloads) | Carbon via a 30-line wrapper |
| Overlay + menu-bar item + TCC prompts | `objc2-app-kit` 0.3.2 — works, but you write AppKit through unsafe bindings | native |
| Toolchain here | rustc 1.94.1 | Swift 6.3.3 |
(crates.io API, 2026-11-02.) Three of the four hard parts (overlay, menu bar, permission identity) are AppKit. Rust helps only for a
shared core or if David wants Rust for its own sake.

## 3. What Snappy is (and is not)

**Is:** region store · cycle · outline · capture · send. Keyboard-first. One process (menu-bar agent, no Dock icon) + a CLI.
**Is not:** a library, a viewer, an annotator, a describer/tagger, a recorder, or a FliStudio module (dossier §13, §16.3, §16.6, §24).
**Boundary:** Snappy does fast capture + sends context. B-Roll Pilot owns description, tags, grouping, storage.

## 4. The design

### 4.1 Region (the central abstraction)
```jsonc
{ "id": "r_code", "name": "Code editor", "group": "recording-setup",     // group goes downstream
  "scope": { "level": "brand", "brand": "appydave" },                      // global | brand | project (+ project code)
  "display": { "uuid": "…CGDisplay UUID…", "name": "SAMSUNG", "pointsWxH": [2560,1440] },
  "rect": [x, y, w, h],           // POINTS, top-left origin, RELATIVE to that display's top-left
  "order": 3, "active": true }
```
- ≤ 15 *active* regions (soft limit, warn at 16). Many saved, few active (dossier §14.1).
- Active set = global + the brand's + the current project's regions, sorted by `order`.
- Store: one JSON file `~/.config/appydave/snappy.json` (beside `brands.json`, `fli.resources.json`); atomic write (ScreenTour's pattern).
- One-time `snappy import-screentour` reads `~/.screentour/regions.json` (those are global x,y,w,h → convert to display-relative).

### 4.2 Interaction
| Action | Default key (configurable) | CLI |
|---|---|---|
| next / previous region | ⌃⌥→ / ⌃⌥← | `snappy next` / `prev` |
| capture active region | ⌃⌥Space | `snappy capture` |
| capture after countdown (3/5 s) | ⌃⌥C | `snappy capture --in 3` |
| timed series (N shots, every S s) | menu / CLI | `snappy series --count 10 --every 1` |
| show/hide outline | ⌃⌥O | `snappy outline on|off` |
| new region (drag a rectangle) | ⌃⌥N | `snappy region add "Code editor"` |
Defaults are *proposals* — conflicts with other apps not checked (S3).
CLI talks to the agent over a Unix socket in `~/Library/Application Support/Snappy/`. A CLI verb means a Stream Deck / DeckHand button can trigger it (inference — not tested).

### 4.3 Outline and feedback
- Outline = 3 px AppyDave-yellow frame drawn **just outside** the region rect (the margin is its own, so the capture never contains it), with the region name on a small tab outside the frame.
- On capture the frame flashes; a menu-bar tick confirms "sent" or shows "queued". Countdown digits render in the tab, outside the rect.
- Belt and braces: the capture filter excludes Snappy's own windows (`SCContentFilter(display:excludingWindows:)`), but the design does not depend on it.

### 4.4 Regions and displays — the trap I measured
This Mac has four displays. AppKit (`NSScreen`) says display 1 is `(-1920, 0, 1920×1080)` with a **bottom-left** origin; `screencapture -R` uses a **top-left** origin.
Capturing `-R -1500,100,400,300` (meant: 300 px tall on that display) returned a **400×40** image — the strip where the rect overlaps
that display in top-left space (display 1 starts at y=360 there, since main is 1440 tall). So:
- **Store regions display-relative, top-left origin, in points**; convert to global only at capture time using `CGDisplayBounds` (top-left space), never `NSScreen.frame`.
- Identify a display by its **UUID** (`CGDisplayCreateUUIDFromDisplayID`), not its number or position.
- On a display change: match by UUID; else by name + size; else mark the region **unresolved** (greyed, skipped by cycling, "re-aim" prompt). Never silently capture the wrong area.
- Window movement: v1 regions are *screen* areas, not window-attached (the tripod). "Follow this app's window" is a later feature.
- Output is native pixels (2× display → 2× image). A 1× display gives a 1× image; offer an optional "scale to N px wide" per region later.

### 4.5 Capture modes (dossier §15)
| Mode | v1 | How |
|---|---|---|
| Single | yes | capture active region |
| Tab-by-tab / scrolling | yes, for free | same region, repeated; each capture increments the **series** counter |
| Countdown | yes | 3 or 5 s, digits in the tab |
| Timed series | yes | N shots every S s on a monotonic timer; `sequence {series, index, of}` |
| Multi-region coordinated | no (§15.5, future) | structure allows it: a series could hold a *list* of region ids |
| Scroll-stitching, video | no | out of scope |

### 4.6 Send, don't store (dossier §16.3)
No library. Each capture is written to a **spool** then sent:
- Spool: `~/Library/Application Support/Snappy/spool/<id>.png` + `<id>.json`. Deleted **only after** the receiver confirms. If FliStudio is down, files stay, the menu bar shows "N queued", retry on next launch / every 30 s. Unsent shots are never swept.
- First receiver: B-Roll Pilot's existing contract `broll.register` (`/Users/davidcruwys/dev/ad/flivideo/flistudio/docs/planning/broll-pilot/spec.md` §6):
  `POST http://127.0.0.1:<port>/api/rpc` (port + bearer token from `~/Library/Application Support/flistudio/control.json`; today port 7151), header `x-fli-principal: agent:snappy` (a new principal; the spec lists only flihub and flicast),
  `place: "copy"` (the spool file is a temp, so FliStudio keeps a copy and Snappy deletes its own), `from.app: "snappy"`.
- Mapping:
  | Snappy knows | `broll.register` field |
  |---|---|
  | brand, project (the current **target**) | `brand`, `project` |
  | spool file path | `file` |
  | region name + group | **no field today** → `tags: ["snappy", "region:code-editor", "group:recording-setup"]` now; ask for `from.region`, `from.group` (decision D7) |
  | capture time | `from.recordedAt` |
  | series/index | **no field today** → `from.take: "<series>:<NN>"`; tags `series:<name>` |
  | form | `"image"` (let FliStudio infer) |
- Transport is JSON-RPC over HTTP on loopback; no extra service needed. Not tested live — the spec describes it, I did not call it.
- **Target**: Snappy holds a *current brand/project* (set from menu or `snappy target d13`), because §4.1's "project-scoped" regions need it. Default = last used. No guess from the front window.

### 4.7 Enrichment (dossier §16.6)
Snappy does none. It sends fast; B-Roll Pilot describes in the background ("silent → frame-sampled description", its spec §5). Snappy's only metadata duty is to be accurate.

## 5. Answers to dossier §25 (Snappy)

| Question | Answer |
|---|---|
| Previous screen-capture apps in the repos? | ScreenTour (`/Users/davidcruwys/dev/ad/apps/screentour`), the zsh `sc_*` functions, a Ruby screenshot builder that was only a ChatGPT thread. §1. |
| Which concepts/code are reusable? | **Concepts:** region as tripod, series + counter, MRU, timed capture, atomic JSON. **Code:** none directly (Python/Textual); `capture.py`'s counter regex is 6 lines worth re-writing. §1. |
| Which macOS APIs best support region capture + overlays? | Capture: ScreenCaptureKit (`SCScreenshotManager`, 14+; `rect` variant 26+) with `screencapture -R` as a proven fallback/baseline. Overlay: borderless click-through `NSWindow` drawn *outside* the rect. §2, §4.3. |
| Rust or Swift? | **Swift** for the agent (3 of 4 hard parts are AppKit). Rust is viable (crates are current) but adds an Objective-C bridge for no gain. D1. |
| Background service with CLI, TUI or UI? | **Menu-bar agent (no Dock icon) + CLI over a socket.** No TUI. D3. |
| Global hotkeys? | Carbon `RegisterEventHotKey`: no extra permission reported, works from any app. Configurable. Avoid CGEventTap (Input Monitoring). §2, §4.2. |
| Regions across display changes / window movement? | Store per-display (UUID), points, top-left origin; unresolved regions are flagged, never guessed. Windows don't move regions in v1. §4.4. |
| Transport to B-Roll Pilot? | Existing `broll.register` JSON-RPC on FliStudio's loopback door, bearer token from `control.json`. §4.6. |
| Metadata per capture? | Region name/id/group, scope, brand, project, timestamp, series/index/of, display name, pixel size, Snappy version. Sent via tags + `from.*` today; two missing fields requested (D7). §4.6. |
| Temp files before delivery? | `~/Library/Application Support/Snappy/spool/`, deleted only on confirmed receipt; queued + retried if FliStudio is down. §4.6. |

## 6. Permissions & packaging
- Needs: Screen & System Audio Recording. Nothing else expected (no Accessibility, no Input Monitoring, no Automation) if hotkeys use Carbon.
- Must be a **signed `.app` with a stable identity**, otherwise the grant is lost on rebuild (general macOS behaviour; verify in S1).
- Start/stop via `my-app` per David's rule (servers go through `my-app`); the agent is a launch-at-login item later. No work here — no repo yet.

## 7. First build slice (when David says go)
1. Menu-bar agent + region file + import ScreenTour regions.
2. Cycle + outline + single capture to the spool.
3. Send to B-Roll Pilot, queue on failure.
4. Countdown + timed series.
Out of v1: multi-region, window-follow, label/annotate, scroll-stitch, video, describing, Windows.

## 8. Spikes to run before locking (each ≤ 1 hour, no repo needed)
- **S1 Permission + capture:** a signed 40-line Swift tool captures a rect via `SCScreenshotManager` and via `screencapture` as a child; confirm which process the Screen Recording grant attaches to and whether a rebuild keeps it; see the macOS 26 re-prompt.
- **S2 Outline leak:** draw the outside-the-rect frame and a window with `sharingType = .none`; capture with SCK and with `screencapture`; look at the pixels.
- **S3 Hotkeys:** register ⌃⌥← → Space under Carbon; test with iTerm, VS Code, Chrome, Electron focused; check clashes with Stream Deck, Rectangle-style tools, Ecamm.
- **S4 Four-display geometry:** round-trip a region through UUID + relative rect on this Mac's four displays; capture on each, including the negative-x one.

## 9. Decisions — APPROVED by David, 2026-11-02 ("yes to all")

| # | Decision | Approved answer |
|---|---|---|
| 1 | Language | **Swift** |
| 2 | Capture engine | **ScreenCaptureKit** in-process (`screencapture -R` stays the S1 baseline) |
| 3 | Interface | **Menu-bar agent + CLI** (no TUI) |
| 4 | Hotkeys | **⌃⌥← / ⌃⌥→ cycle · ⌃⌥Space snap · ⌃⌥C countdown** (configurable) |
| 5 | Outline | **Drawn outside the region** (3 px margin) |
| 6 | Region storage | **One config file** `~/.config/appydave/snappy.json`, with a **`scope` field on each region** (global \| brand \| project) |
| 7 | B-Roll Pilot contract | **Region, group and sequence fields go to B-Roll Pilot**, routed through `flivideo-orch` |
| 8 | Output | **PNG** at native pixels |

**Future direction (David, 2026-11-02):** FliStudio may later provide brand-level and machine-level configuration.
Snappy's single file is the v1 answer; design the region `scope` field so a later FliStudio-provided brand/machine
config can supply or override regions without a format change.

**Not started:** the four spikes (§8) wait until the OpenRig developer-rig plan is approved — David, 2026-11-02.

The original options and recommendations are kept below for the record.

### 9a. The decisions as put to David

1. **Language: Swift or Rust?** *Rec: Swift.* Overlay, menu bar and permission identity are AppKit; Rust's capture and hotkey crates are fine but you'd wrap AppKit anyway. Rust only if you want it for the fleet's other tools.
2. **Capture engine.** *Rec: ScreenCaptureKit in-process,* with `screencapture -R` as the baseline in spike S1. In-process means Snappy holds the permission and can exclude its own windows.
3. **Interface.** *Rec: menu-bar agent + CLI, no TUI.* Your priority is keyboard speed; ScreenTour's TUI was the part that got lost behind the thing it captured.
4. **Hotkey defaults.** *Rec: ⌃⌥← / ⌃⌥→ cycle, ⌃⌥Space capture, ⌃⌥C countdown,* configurable. Ready to change after S3 shows clashes.
5. **Outline contamination.** *Rec: draw the frame outside the region (3 px margin).* It cannot be in the shot, whatever macOS does with `sharingType`. The cost: you lose a few pixels of framing context. Alternative: hide the frame for ~50 ms during capture (flickers).
6. **Region storage + scope.** *Rec: one file `~/.config/appydave/snappy.json`,* scope = global | brand | project, display-anchored. Alternative: per-project files inside each project (better portability, worse for brand presets).
7. **B-Roll Pilot contract: add two fields.** `from.region` (+ id) and `from.group`, and a `sequence {series,index,of}`. Works today through tags and `from.take`, but group-based organising (dossier §16.5) should be a field, not a tag. This is a change to **another lane's spec**, so it goes through `flivideo-orch` — I have not touched it.
8. **Output format.** *Rec: PNG, native pixels.* ScreenTour wrote JPG. PNG keeps text sharp for overlays; B-Roll Pilot can derive thumbnails. Alternative: JPG for smaller timed series.

Also for the record, **ScreenTour:** *Rec: leave as is,* import its regions, retire it once Snappy ships. Do not extend it.

## 10. What I checked, and what I didn't
Checked: dossier §13–17, §24–28; ScreenTour `CONTEXT.md`, `session-learnings-2026-04-24.md`, `capture.py`, `regions.py`; zsh `aliases-screencapture.zsh`; four ChatGPT threads; B-Roll Pilot spec §6; `control.json` (port 7151, token not read into this doc); `NSScreen` frames, `screencapture -R` timing and the 400×40 result on this Mac; crates.io versions; Apple's documentation data for SCScreenshotManager availability.
Not checked: Apple's pages for `CGWindowListCreateImage` deprecation and `NSWindow.sharingType` (no static content); macOS 26 behaviour of the monthly permission re-prompt; whether `screencapture` run as a child of a signed app uses the parent's permission; any live `broll.register` call; hotkey clashes; B-Roll Pilot's *built* state (only its spec).

## 11. Sources
- Apple documentation data: `developer.apple.com/tutorials/data/documentation/screencapturekit/scscreenshotmanager.json` (and `…/captureimage(in:completionhandler:).json`, `…/capturescreenshot(rect:configuration:completionhandler:).json`) — availability macOS 14.0 / 15.2 / 26.0.
- `man screencapture` (local); `screencapture` empirical runs, 2026-11-02, mac-mini-m4.
- [9to5Mac: Sequoia monthly screen-recording prompt](https://9to5mac.com/2024/08/14/macos-sequoia-screen-recording-prompt-monthly/) · [TidBITS](https://tidbits.com/2024/08/19/apple-reduces-excessive-sequoia-permission-requests-shifts-to-monthly)
- [Rust global-hotkey docs](https://docs.rs/global-hotkey/latest/global_hotkey/) · [Dev.to on Carbon hotkeys](https://dev.to/quicopy/the-macos-global-shortcut-that-wont-fire-in-zed-when-a-23-year-old-carbon-api-meets-a-self-drawn-24o9)
- [Apple Developer Forums: sharingType none vs ScreenCaptureKit](https://developer.apple.com/forums/thread/808016) · [Product Hunt write-up](https://www.producthunt.com/p/jobpath/how-apps-hide-windows-from-screen-capture-and-what-broke-in-macos-15)
- crates.io API: `screencapturekit`, `objc2-screen-capture-kit`, `xcap`, `global-hotkey`, `objc2-app-kit`, `scap`.
- Internal: `/Users/davidcruwys/dev/ad/flivideo/docs/specs/b683-dossier-2026-11-02.md`, `/Users/davidcruwys/dev/ad/flivideo/flistudio/docs/planning/broll-pilot/spec.md`, `/Users/davidcruwys/dev/ad/apps/screentour/CONTEXT.md`.
