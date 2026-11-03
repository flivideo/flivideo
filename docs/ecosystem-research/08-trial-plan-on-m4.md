---
type: plan
title: "08 · Trial plan on the M4 — the useful outside apps, run on a real video project, reached from FliStudio"
description: "Plan only (nothing installed). Shortlist of the outside apps worth running (auto-editor, Textream, HyperFrames Studio, video-use, Immich, MLT, Cap), each walked through on d01-flivideo-tour as if it were running: files in, clicks/verbs, output zone, what FliStudio shows; how it would run on the M4 (install, my-app entry, port, disk/RAM, licence); the smallest seam into FliStudio; the experiment that proves it; a verdict; and one ranked order of play."
tags: [ecosystem-research, flivideo, trial-plan, m4, flistudio, hyperframes, immich, textream, auto-editor, video-use, mlt, cap, B686, B687]
created: 2026-11-03
timestamp: 2026-11-03T17:10+07:00
status: plan
---

# 08 · Trial plan on the M4

> **PLAN ONLY.** Nothing here has been installed, cloned or run. Every step below needs David's go, and each
> experiment needs its own row ruled in `06` (R21). This file does **not** change any lean or Status in `06`.

**Purpose**: David, 2026-11-03: *"If there are actually useful applications, we need to figure out a way on the M4 to
actually get these applications running and connected into a FliStudio. Otherwise, we'll never see it … a plan of
action … on how to use each of them … as if we were running them based on one of our current video projects."*
This is that plan: which outside apps are worth running, what each would do on a real project, how it would run on
the M4, how FliStudio would reach it, and in what order to stand them up.

**For Agents**:
- Inputs: `04` (leans, C1–C19), `05` (X1–X9), `06` (R1–R21; **R6** AppyFactory and **R13** run AGPL unmodified,
  learn, never copy — both ruled), `candidates/*.md`. Observed today on the M4 (`mac-mini-m4.local`, 2026-11-03):
  FliStudio `136bb92`, `~/.config/appydave/apps.json` (38 apps), `~/dev/upstream/repos/`, the four projects in
  `/Users/davidcruwys/dev/video-projects/v-appydave/`.
- Three kinds of statement: **Observed** (read today), **UNVERIFIED** (not checked — install commands, RAM/disk
  figures for apps not installed, flags of CLIs not run), **Plan** (this file's proposal, not approved).
- **Machine change to flag**: `05` says run experiments on the **M2**. This plan proposes the **M4** for everything
  except Immich, because David asked for M4 and because FliStudio (`:7150` listening, observed) and the worked
  project live there. That is David's call (see *Decisions this needs*).
- Trial rule (from `05`): every trial works on **copies** of the project's files in
  `~/dev/upstream/scratch/<X-id>/`, never inside the project or an app repo. The "lands in" zones below are where
  output *would* go once an app is adopted — not where a trial writes.
- Do not edit `06` or any Status cell from this file.

---

## 1. The worked example: `d01-flivideo-tour`

**Pick: `/Users/davidcruwys/dev/video-projects/v-appydave/d01-flivideo-tour/`** — it is the only one of the four with
real footage, so it is the only one that can exercise the cutting, editing, B-roll and render candidates.

| Project | What is on disk (observed) | Exercises |
|---|---|---|
| **d01-flivideo-tour** ★ | 2.3 GB · `hub/recordings/` 20 Ecamm takes (`01-1-intro-HOOK.mov` … `07-2-teletuby.mov`) + word-level transcripts (`hub/transcripts/*.json`, engines incl. CrisperWhisper) · `footage/` 13 DJI clips (1.5 GB, 35–331 MB each) · 2 FliCast screen recordings (`fli.cast.flivideo-tour-1/2`) · a FliCut cut `fli.cut.flivideo-tour.json` (silence + filler cuts on, pause 0.5 s, padding 0.15 s) · a FliEdit edit `fli.edit.d01-flivideo-tour-edit.json` (1 DJI source, V1 + A1, 1080p25) · a Teletubby script `fli.tubby.json` (CTA v1) | auto-editor, video-use, HyperFrames, Immich, MLT, Cap, Textream (short script) |
| d13-overlay-pilot | 7.3 MB · Story Pilot script `script/storypilot/project/script.md` (a full spoken script), Kokoro audio, 1 B-roll resource, no footage | **second project, Textream only** — the full-length script David is about to record |
| d18-story-pilot | 2.4 MB · story.json + angle audio, no footage | nothing d01 can't show |
| d19-spaghetti-rig | 2.2 MB · story.json, 38 dossiers, no footage | nothing d01 can't show |

---

## 2. Shortlist

Kept = lean *add* or *absorb* **and** something we can actually run.

| # | App | Stage | Lean (04) | Kept because |
|---|---|---|---|---|
| A | **auto-editor** | cut | absorb as tool (C12) | one CLI, Unlicense, already cloned on M4 (`5ad05f9`) |
| B | **Textream** | record | absorb ideas; add after X5 (C10) | macOS app, MIT, the only agent-drivable prompter |
| C | **HyperFrames Studio** | edit / motion | add + absorb (C1) | Apache-2.0, editor components + CLI, cloned on M4 (`6feb4bec7`, v0.9.6) |
| D | **video-use** | cut | absorb ideas (C13) | MIT, cloned on M4 (`43cfc56`), agent-native |
| E | **Immich** | B-roll | add if X4 (C7) | strongest B-roll store; AGPL OK to run unmodified (R13) |
| F | **MLT / melt** | edit render | absorb only if FliEdit's render hurts (C2) | LGPL CLI; d01's edit file is a ready X3 input |
| G | **Cap** | record | none / add for Loom jobs (C15) | macOS app; kept only as an *ideas only* card |

**Dropped (lean *none*, one line each)**
- **Kdenlive / Shotcut** — GUIs over MLT with no agent surface; MLT (F) covers the engine.
- **libopenshot** — a library behind MLT in priority; nothing to open in FliStudio.
- **FilmCraft + the Craft apps** — "in development"; watch, re-check at first stable release (R19).
- **OpenMontage** — not an app; an agent-instruction system built on generative providers. Absorb the stage-graph
  pattern into pilot specs (R14); nothing to stand up.
- **ResourceSpace** — PHP + MySQL ops for a comparison point; Immich (E) is the trial.
- **Dam'It** — our own design, not runnable; it stays the design owner over whatever store wins (Q3).
- **QPrompt** — no agent surface found.
- **LosslessCut** — manual lossless trims; FliCut already cuts.
- **Recordly · open-recorder · Screenize** — format references only; never open the last two as a workspace.
- **Remotion** — already owned; no trial needed to keep it as an engine option (R20).
- **Motion Canvas · Manim** — HyperFrames/Remotion cover the lane.

---

## 3. One section per app

### A · auto-editor — "cut the dead air in one call"

- **Job (David's words)**: the silence pass, as a tool any app can call. Stage: **cut**.
- **Walk-through on d01 (as if running)**
  1. In FliStudio, David opens d01 → *Start a cut* is already done, so he opens FliCut on `flivideo-tour`.
  2. An agent (or FliCut) calls a FliTools verb, e.g. `cut.silence { file: hub/recordings/03-1-flistudio.mov,
     pause: 0.5, padding: 0.15 }` — the same numbers FliCut's `cutParams` already use (observed).
  3. FliTools runs `auto-editor` headless on that take and returns a keep/cut list as JSON (UNVERIFIED flags:
     `--edit audio`, `--margin 0.15s`, a JSON/timeline export).
  4. **Lands in**: `-renders/auto-editor/03-1-flistudio.cuts.json` (derived, disposable). FliCut shows the proposed
     cuts as a second lane beside its own word-level cuts; David keeps or drops them.
  5. **FliStudio shows**: nothing new — it is FliCut's view. Agents see a new FliTools verb.
- **On the M4**: install = pip/uv or a release binary (auto-editor is now written in Nim; method on
  auto-editor.com/installing — **UNVERIFIED**). **No `my-app` entry** — it is a CLI, not a server; FliTools (launchd,
  `:7161`) would own it. Disk < 100 MB, RAM < 500 MB per job (both UNVERIFIED). Licence: **Unlicense** — no gate.
- **Smallest seam**: a **background tool called by a FliTools verb**. No FliStudio code.
- **Proves it**: **X6** (1.5 h) — run on a *copy* of `03-1-flistudio.mov`, compare to FliCut's cut in
  `fli.cut.flivideo-tour.json`: cut list, kept duration, false cuts. Go needed: X6 under R21, plus "OK to install
  auto-editor on the M4".
- **Verdict: try first.** Cheapest, safest, no FliStudio change, can run while David tests the pilots.

### B · Textream — "push the script to the prompter and watch where I am"

- **Job**: a second teleprompter that an agent can drive, with voice-tracked word progress. Stage: **record**.
- **Walk-through (d13 script, d01 CTA as the short case)**
  1. In FliStudio, Story Pilot on d13 has the script (`script/storypilot/project/script.md`, observed).
  2. David clicks *Send to prompter → Textream* (Plan); FliStudio opens
     `textream://read?text=<script>` — or, with Director on, POSTs the script to Textream on `:7575`.
  3. Textream shows the script in the notch/overlay and highlights words as David speaks.
  4. An agent reads word progress (10 Hz over WebSocket, per README — UNVERIFIED) to know which paragraph he is on.
  5. **Lands in**: nothing in the project — the script stays in Story Pilot / `fli.tubby.json`. At most a note in
     `fli.notes.jsonl` ("recorded para 1–6 on Textream").
  6. **FliStudio shows**: a *Send to Textream* button beside the Teletubby one.
- **On the M4**: install = signed release / DMG from GitHub, or a brew cask (**UNVERIFIED**; it is not cloned on the
  M4 — clone is on the M2). `my-app` entry `textream` in the **Buzz pattern** (observed: `supervisor: script`,
  `start: open -a /Applications/Textream.app`, `status: pgrep …`, no port). Director port **7575** is fixed by the
  app; free on the M4 today (observed: not in `apps.json`, not listening). Disk ~50 MB, RAM ~200 MB (UNVERIFIED).
  Licence: **MIT**.
- **Smallest seam**: **link-out via the `textream://` URL scheme** — one `open` call, no server, no auth question.
  Director push comes only after X5 answers the auth question.
- **Proves it**: **X5** (1.5 h, already planned for the M4) — push a *copy* of d13's script by URL and by Director,
  read word progress from a script, check what `:7575` binds to and whether it asks for anything. Go: X5.
- **Verdict: try first** — but only when David is not mid-recording; the lean stays *absorb ideas into Teletubby*
  (Teletubby is operational and Story Pilot already calls it).

### C · HyperFrames Studio — "an editor for titles, overlays and motion that opens like FliCut"

- **Job**: make chapter cards, lower thirds, animated callouts timed to the transcript, and edit them in a timeline.
  Stage: **edit / motion** (FliEdit keeps footage assembly — E-A).
- **Walk-through on d01 (as if running)**
  1. In FliStudio on d01, David clicks *Open in HyperFrames* on chapter 03 (FliStudio).
  2. FliStudio (or an agent) creates a composition folder from **copies** of `hub/recordings/03-1-flistudio.mov`,
     its words file `hub/transcripts/03-1-flistudio.json`, and two DJI clips from `footage/`.
  3. An agent writes the composition: a "03 · FliStudio" chapter card at 0:00, three callouts timed to the words
     "brand", "project", "open the right app", a DJI cutaway at the B-roll beat. It runs `hyperframes check`.
  4. Studio opens in the browser (preview server; default port 3002 in the CLI source, observed — we would pin
     **7210**). David drags the callout later, trims the cutaway; the agent sees his selection via
     `preview --context --json` and the undo history via `/history`.
  5. David clicks Render. **Lands in**: composition in `fli.motion.03-flistudio/` (+ `fli.motion.03-flistudio.json`
     as its state file, following the `fli.cut.*` / `fli.edit.*` zone pattern — **zone name is a Plan, needs Q1/R4**),
     render in `-renders/motion/03-flistudio.mp4`.
  6. FliEdit picks up that MP4 as an overlay/clip source in `fli.edit.d01-flivideo-tour-edit.json`.
  7. **FliStudio shows**: the motion pieces listed under the project, each with *Open* and its last render.
- **On the M4**: install = Node (v24 present, observed) + `npx hyperframes` / the `@hyperframes/cli` package; Chromium
  for headless render pulled by Puppeteer. Clone on M4 is 495 MB (observed); node_modules + Chromium ~1 GB more
  (UNVERIFIED). RAM: Studio ~0.5 GB; render 1–3 GB (headless Chrome, UNVERIFIED). `my-app` entry
  `hyperframes-studio`, port **7210** (free in `apps.json` and not listening on the M4, observed), start
  `npx hyperframes preview --port 7210` in the composition folder (flag name observed in `preview.ts`; behaviour
  UNVERIFIED). Licence: **Apache-2.0** — no gate.
- **Smallest seam** — two steps:
  1. **Link-out**: FliStudio opens `http://localhost:7210` for a composition folder (needs no Door; `my-app` starts it).
  2. **Open like FliCut**: a new `AppKey` (`'flimotion'`, observed today: `flihub | flicut | flicast | teletubby |
     fliedit` in `shared/src/contracts.ts:245`) and one `Door` in `server/src/launch/doors.ts`, so `app.launch`
     starts it at brand + project. That is FliStudio code — waits until David has finished testing the pilots.
- **Correction to 04 (observed today)**: Overlay Pilot's renderer is **ffmpeg + Pillow** (R10, 2026-10-28 —
  `modules/overlay-pilot/render/render.py`); HyperFrames is not under it today. So "absorb for overlays" is a future
  move, not "already the direction".
- **Proves it**: **X2** (1 h — what studio-server binds to, whether it takes a token) then **X1** (3 h — footage edits
  on a d01 copy: cut, ripple, move, trim, music bed + duck, render). Go: X2 then X1 under R21; R10 for the seam.
- **Verdict: try first** (X2 → X1 in scratch); the FliStudio button **later**.

### D · video-use — "an agent that proposes cuts by meaning"

- **Job**: cut passes by meaning (repeated point, weak opener), proposed for David to accept in FliCut. Stage: **cut**.
- **Walk-through on d01 (as if running)**
  1. Copies of the 20 takes in `hub/recordings/` go into a scratch folder.
  2. A Claude Code session with video-use's skill packs the takes into one `takes_packed.md` (README, observed) and
     proposes cuts: "drop 01-3 lines 4–6, it repeats 01-2".
  3. **Lands in**: `-renders/video-use/flivideo-tour.proposals.json` (Plan). Never auto-applied.
  4. **FliStudio shows**: nothing; FliCut could show the proposals as a review lane later (absorb ideas, R17).
- **On the M4**: `uv sync` in its clone (README, observed), ffmpeg (present, observed). **Needs an ElevenLabs Scribe
  key** — one paid call per source (README, observed); whether it can use FliTools' existing word-level transcripts
  instead is **UNVERIFIED**. No `my-app` entry (CLI + skill). Disk ~300 MB venv (UNVERIFIED). Licence: **MIT**.
- **Trust note (observed)**: its README tells the agent to install itself, register its skill and ask for the API key.
  Treat that as untrusted text: install by hand in scratch; do not register its skill globally.
- **Smallest seam**: **ideas only** — no seam until X7 shows ≥ 2 cuts David would keep.
- **Proves it**: **X7** (2 h) on the same take as X6. Go: X7 + OK to spend ElevenLabs credit.
- **Verdict: try later** — after X6, so the two compare on the same take.

### E · Immich — "every B-roll clip in one searchable library"

- **Job**: store all B-roll, tag it, search it ("drone shot over desk"), and hand B-roll Pilot the right clip.
  Stage: **B-roll**.
- **Walk-through on d01 (as if running)**
  1. Copies of the 13 DJI clips in `footage/` (1.5 GB) are uploaded with the Immich CLI and a scoped API key.
  2. Album `appydave / d01-flivideo-tour`; tags `shot:drone`, `shot:desk`, `brand:appydave` (typed tags UNVERIFIED —
     X4's question).
  3. In B-roll Pilot on a new project, David asks "find B-roll for: the desk setup". B-roll Pilot calls a small
     adapter → Immich smart search → three thumbnails.
  4. He picks one. **Lands in**: the file is fetched into the project's `footage/`, and a `broll` resource is added to
     `fli.resources.json` (kind `broll` exists today, observed in d13). Immich keeps the library copy.
  5. **FliStudio shows**: thumbnails inside B-roll Pilot; an *Open in Immich* link for the full library.
- **On the M4**: **Docker** (Docker.app is installed on the M4, observed — but using it is **not approved**, R12/X4).
  Immich = server + ML + Postgres + Redis containers; RAM ~4–6 GB with ML, images ~3 GB, plus library + thumbnails
  (all UNVERIFIED). The M4 has 24 GB RAM and **68 GiB free** on `/` (observed) — tight next to dev builds. `my-app`
  entry `immich`, supervisor `docker compose`, port **7220** mapped to Immich's 2283 (7220 free, observed); tailnet
  only. Licence **AGPL-3.0** — R13: run unmodified, learn, never copy code.
- **Smallest seam**: **a background service behind a B-roll capability** (B-roll Pilot → adapter → Immich REST),
  plus **link-out** to the Immich web UI. No iframe.
- **Proves it**: **X4** (4 h). Go: **Docker yes** (R12) + X4 + which machine. Recommendation: **M2**, as 05 planned —
  keeps 6+ GB of containers off the dev machine.
- **Verdict: try later** — the biggest step and the only one needing Docker.

### F · MLT / melt — "a second render engine under FliEdit"

- **Job**: render FliEdit's edit file headless, if FliEdit's own render is slow or wrong. Stage: **edit (render)**.
- **Walk-through on d01**: copy `fli.edit.d01-flivideo-tour-edit.json` (1 DJI source, V1 + A1, 1080p25, observed) →
  translate to MLT XML → `melt edit.mlt -consumer avformat:out.mp4` → compare with FliEdit's render at 5 frames.
  **Lands in** (if adopted): `fli.edit.d01-flivideo-tour-edit/mlt/edit.mlt` + `-renders/mlt/…mp4`. **FliStudio
  shows**: nothing — FliEdit's Render button just uses it.
- **On the M4**: Homebrew formula `mlt` (UNVERIFIED); not installed (observed: no `melt`). No `my-app` entry (CLI).
  Disk ~200 MB, RAM ~1 GB per render (UNVERIFIED). Licence **LGPL-2.1** — linking allowed.
- **Smallest seam**: **background engine called by FliEdit** — FliEdit repo change, not FliStudio.
- **Proves it**: **X3** (3 h). Go: only if R9 moves past E-A.
- **Verdict: try later** — only if FliEdit's render path hurts (R11 lean: none).

### G · Cap — "a quick Loom-style share"

- **Job**: a 60-second share recording (e.g. "here's d01's cut, have a look") with a link. Stage: **record**.
- **Walk-through on d01**: David opens Cap, records FliStudio showing the d01 cut, gets a share link. **Lands in**:
  `cast/` or nowhere (Cap keeps its own library). **FliStudio shows**: at most a link-out.
- **On the M4**: macOS app (DMG, UNVERIFIED), Buzz-pattern `my-app` entry, no port. Licence: app AGPL (R13 OK to run),
  capture crates MIT.
- **Smallest seam**: **link-out only**. **Proves it**: no experiment planned. **Verdict: ideas only** — FliCast stays;
  revisit if a Loom-style job appears (R18).

---

## 4. Order of play on the M4

| Step | What | Cost | Runs while David tests the pilots? | Go needed |
|---|---|---|---|---|
| 1 | **auto-editor → X6** on a copy of `03-1-flistudio.mov` vs FliCut's cut | 1.5 h · < 100 MB · no server | **yes** — scratch only, no FliStudio code | X6 + install OK |
| 2 | **Textream → X5** with d13's script | 1.5 h · ~50 MB · macOS app | **yes**, but not during a recording session | X5 + install OK |
| 3 | **HyperFrames → X2** (bind/auth of studio-server) | 1 h · ~1 GB (node_modules + Chromium) | **yes** — scratch only | X2 |
| 4 | **HyperFrames → X1** on a d01 copy (chapter 03 + 2 DJI clips) | 3 h · ~2 GB working copies · 1–3 GB RAM render | **yes** — scratch only | X1 |
| 5 | `my-app` entries for what passed (`hyperframes-studio` :7210, `textream`) | 0.5 h | yes — registry only, no app code | "add my-app entries" |
| 6 | **video-use → X7** on the X6 take | 2 h · ~300 MB · ElevenLabs credit | **yes** — scratch only | X7 + spend OK |
| 7 | **FliStudio seam** for HyperFrames: link-out, then a `flimotion` Door | 0.5 day | **no** — FliStudio code | R10 (+ R4 for the zone name) |
| 8 | **Immich → X4** (recommend M2) | 4 h · 6+ GB containers + library | yes — separate machine | Docker yes (R12) + X4 + machine |
| 9 | **MLT → X3** | 3 h | yes — scratch only | only if R9 moves past E-A |
| — | Cap | — | — | not trialled |

**Total to the first visible result** (steps 1–4): ~7 h of agent time, ~3 GB disk, no FliStudio change, no Docker.

## 5. Decisions this needs (one at a time)

1. **Approve steps 1–4 as a batch** (X6, X5, X2, X1 on the M4, with installs of auto-editor, Textream and HyperFrames'
   npm packages)? Recommendation: **yes** — all scratch-only, nothing touches FliStudio or a pilot.
2. **M4 instead of M2** for those four (05 said M2)? Recommendation: **M4** for 1–4 (that is where FliStudio and d01
   are); **M2** for Immich.
3. **Docker for Immich** (R12/X4)? Recommendation: **later**, after steps 1–4 report.

## Sources

- `04-potential-target-architecture.md`, `05-research-experiments.md`, `06-approval-register.md` (read, not edited),
  `candidates/{hyperframes-as-editor,broll-dam,teleprompter,flicut-alternative,fliedit-replacement,screen-recording,openmontage}.md`.
- Observed on the M4, 2026-11-03: FliStudio `136bb92` — `server/src/launch/launch.ts` (`launchApp`, starts with
  `scripts/app.sh start --brand … --project …`, switches a running app through its API), `server/src/launch/doors.ts`
  (`Door`, `DOORS`), `shared/src/contracts.ts:245` (`AppKey`), `modules/overlay-pilot/render/render.py` header.
  `~/.config/appydave/apps.json` (Buzz entry as the GUI-app pattern; used ports). `~/dev/upstream/repos/`
  (hyperframes `6feb4bec7` v0.9.6, auto-editor `5ad05f9`, video-use `43cfc56`; immich, textream, mlt, cap not cloned
  on the M4). `hw.memsize` 24 GB, `df /` 68 GiB free, Docker.app present, no `auto-editor`/`melt` on PATH.
- Project files: `/Users/davidcruwys/dev/video-projects/v-appydave/{d01-flivideo-tour,d13-overlay-pilot,d18-story-pilot,d19-spaghetti-rig}/` (read only).
