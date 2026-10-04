---
type: reference
title: FliVideo — ecosystem map
description: "The one central map of the FliVideo suite: every app, what it does, its lifecycle bucket, which pipeline stage it owns, and where its own docs live. Points to per-app docs; never copies them."
created: 2026-09-23
timestamp: 2026-10-03
status: active
---

# FliVideo — ecosystem map

**Purpose**: One place that says which FliVideo apps exist, which are live, which pipeline stage each
owns, and where each app's own docs are. It points; it does not copy.

**For Agents**:
- Start here before working across more than one Fli app.
- Per-app detail lives in each app's `docs/` (see *Per-app docs*). Trust the code over any doc.
- Decisions and open problems live in the brain, not here:
  `/Users/davidcruwys/dev/ad/brains/video-as-code/open-problems-register.md`.
- This folder is **not a monorepo**. Each app is its own git repo; this root repo tracks only
  `.claude/`, `docs/`, `packages/` and this file (see `.gitignore`).

---

## The pipeline — four stages

| Stage | Owner | State |
|---|---|---|
| 1. Pre-production (scripting) | **Sally** (agent) | no app. The script work is done by the agent **Sally** (Showrunner, scripts): `/Users/davidcruwys/dev/agents/sally`. The script-writing *skills* are Showrunner → Story Editor → Scribe → Voice Coach, in `/Users/davidcruwys/dev/ad/appydave-plugins/appydave/skills/` |
| 2. Recording | **FliHub** (Ecamm takes) + **FliCast** (screen/webcam capture) | active |
| 3. Editing | **FliCut** (the cut) → **FliEdit** (brings everything together with overlays) | FliCut active · FliEdit early (v1) |
| 4. Publishing | **FliYLO** — YouTube launch optimiser | missing as an app. Spec: `/Users/davidcruwys/dev/ad/brains/brand-dave/app-requirements/app-02-youtube-launch-optimizer.md`; skills: `/Users/davidcruwys/dev/ad/appydave-plugins/ylo/skills/`; folds in FliLaunch and the Agent Workflow Builder publishing prompts |

**Teletubby is not Stage 1.** It displays and edits a script in a teleprompter. Writing the script
is Scribe's job.

**FliStudio** sits over all four stages: brand → project → open the right app.

**FliTools** sits under all of them as a headless service (transcription first). The apps send audio and get a transcript back.

**Domain fact:** recordings in `hub/recordings/` are signed-off FINAL takes. Several takes in one chapter are **sequential parts that all go together**, not alternatives. That is why Start a cut includes all of them, in order.

---

## The apps — four buckets

### Active

| App | What it does | Path |
|---|---|---|
| FliStudio | project home: brand → project → opens the right app | `/Users/davidcruwys/dev/ad/flivideo/flistudio` |
| FliHub | recordings hub: Ecamm takes, naming, transcripts | `/Users/davidcruwys/dev/ad/flivideo/flihub` |
| FliCast | screen and webcam capture | `/Users/davidcruwys/dev/ad/flivideo/flicast` |
| FliCut | editing: cuts a video from recordings and footage. The way in is FliStudio's **Start a cut**; a project with no cuts leads there | `/Users/davidcruwys/dev/ad/flivideo/flicut` |
| FliEdit | editing, after FliCut: composes cuts, overlays and captions into the final video. v1 (16/16 ACs, 2026-09-24); early. Gaps: `fliedit/docs/gap-ledger.md` | `/Users/davidcruwys/dev/ad/flivideo/fliedit` |
| Teletubby | teleprompter: shows and edits scripts | `/Users/davidcruwys/dev/ad/flivideo/teletubby` |
| fli-core | shared library `@flivideo/core`: project layout, zones, naming contracts | `/Users/davidcruwys/dev/ad/flivideo/fli-core` |
| FliTools | headless service (launchd `com.appydave.flitools`, :7161) and the suite's one transcriber. Pass 1: Groq, with mlx-whisper as the fallback. Pass 2 (edit-grade, async): CrisperWhisper locally, or ElevenLabs if switched. Memory rules: one job at a time, a memory check first, unload when idle. Design: `docs/briefs/transcription-as-a-service.md` | `/Users/davidcruwys/dev/ad/flivideo/flitools` |

### Dormant — will be revived

| App | Why it is kept | Path |
|---|---|---|
| Storyline | content planning; its own GitHub org (`appydave-storyline`). "Kind of dead, but it's not — we've got to do something with it" (David, 2026-09-23) | `/Users/davidcruwys/dev/ad/flivideo/storyline-app` |
| FliLaunch | YouTube launch packaging; folds into FliYLO | `/Users/davidcruwys/dev/ad/flivideo/flilaunch` |
| FliStack | the catalogue of creator tools (agents, skills, plugins, apps), as schema, data and scripts. No app UI | `/Users/davidcruwys/dev/ad/flivideo/flistack` |

### Deprecated (ruled 2026-09-23) — kept on disk, not worked on

| App | Note | Path |
|---|---|---|
| FliBrief | built for the external video-editing company: Editor Briefs for an outside editor. Also held the original Dec-2025 vision. Useful parts harvested into `docs/prior-art-fli-brief.md` | `/Users/davidcruwys/dev/ad/flivideo/fli-brief` |
| FliGen | video generation; no real work since Feb 2026 | `/Users/davidcruwys/dev/ad/flivideo/fligen` |
| FliVoice | ElevenLabs voice agent; no git repo of its own | `/Users/davidcruwys/dev/ad/flivideo/flivoice` |
| flihub-disk-observability | not an app: empty folders (`client/…`), no files | `/Users/davidcruwys/dev/ad/flivideo/flihub-disk-observability` |
| `@flivideo/config` | shared lint config; superseded by fli-core | `/Users/davidcruwys/dev/ad/flivideo/packages/@flivideo/config` |

**Outside the pipeline:** FliDeck (`/Users/davidcruwys/dev/ad/flivideo/flideck`) is a general viewer
for folder-based HTML artefacts. Kept, but it is not a video-pipeline app.

### Missing — to build

| App | Job | Notes |
|---|---|---|
| Stage-1 app | scripting as an app | today it is the agent Sally plus skills. Whether it needs an app is unruled |
| FliYLO | Stage 4: YouTube launch optimiser | wanted soon. Spec + skills already exist (see the pipeline table) |
| Content Intelligence | graph-based search across published content | its own app, or part of FliStudio — unruled |
| Affiliate Management, Insight Explorer | brand-management tools | likely part of FliStudio |

---

## Per-app docs

Every active app is documented by one method, in three steps:
`/Users/davidcruwys/dev/ad/flivideo/docs/agent-comprehension-docs.md`.

- `docs/schema-mirror.md` + `.json` — data shapes, generated from code, with a drift check
- `docs/SYSTEM.md` — how it works and why (for people)
- `docs/AGENT-NOTES.md` — pitfalls and conventions (for agents; loaded through the app's `CLAUDE.md`)
- `README.md` — the front door

Coverage changes as runs land, so it is not recorded here. The 2026-09-23 refresh of every active app
is tracked in `docs/briefs/doc-skills-blind-review.md`; to see the real state, look in the app's
`docs/`. FliTools has `docs/architecture.md` and a checkpoint, but no SYSTEM/AGENT-NOTES yet. Check a mirror with:
`python3 /Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/schema-mirror/scripts/verify_mirror.py <repo>/docs/schema-mirror.json`

---

## Machines

- **M4 Mini**: development (all code) and the transcription server.
- **Roamy**: editing and using the apps. It is synced from the M4 after every merged fix (pull, install, restart, health check). It never runs pass 2.
- **M2 (M2 Pro, 32 GB)**: being set up as a full peer and as the transcription worker for pass-2 jobs.

## Running the apps

- **`my-app`** (`/Users/davidcruwys/dev/ad/apps/app-registry/bin/my-app`) is the **process door**: `my-app status|start|show|stop|restart|logs <app>`. It reads the `control` blocks in `~/.config/appydave/apps.json`.
- **FliStudio** is the **project door**: it opens an app AT a brand and project (`app.launch`, `edit.start`, `ui.open`).
- Each app's own `scripts/app.sh` sits under both. FliTools is launchd only.
- **Identity:** every desktop app has an AppyDave icon and its real Dock name. Picks and recipe: `/Users/davidcruwys/dev/ad/brains/brand-dave/app-icons/icon-system.md`. FliCast and FliEdit launchers are signed with a stable per-Mac certificate, so macOS permission grants survive launcher rebuilds. AppyCtrl's dev Dock label stays "Electron", by design upstream.

## Shared data — global / brand / project

Words (`fli.words.json`), video resources (`fli.resources.json`) and brand settings (`fli.brand.json`) follow one
pattern: the same file at global / brand / project, read through fli-core, lower level wins. Where each lives, who
reads and writes it, the merge rules, and the one locked write path for words:
`/Users/davidcruwys/dev/ad/flivideo/docs/shared-data-levels.md`.

## Temporary folders in a project

- **`-trash/`** — the one temporary area. A leading `-` marks a folder as "not content"; fli-core
  never reads a `-` folder as a video. Rule (David, 2026-09-23): trash is allowed only if it is
  **always visible** (count + size) and can be **emptied at any time**, in FliHub **and** FliStudio.
- **`recording-shadows/`** — retired (FR-83, deprecated 2026-09-04). No code creates or reads it. Not a
  first-class folder; remove it from any project that still has one.

---

## History

- **Original vision (Dec 2025)** — four stages, FliHub as the Stage-2 foundation, FliBrief for Stage 3,
  Gling as the external editor. Harvested: `docs/prior-art-fli-brief.md`.
- **Feb 2026 tech-stack docs** in `docs/` (`flivideo-standard-architecture-v1.0.md`,
  `architecture-alignment-report.md`, `four-apps-progress-review-2026-02-14.md`,
  `replication-briefs-for-remaining-apps.md`) — superseded; they describe the first four apps' shared
  template, not today's suite.
- **Sept 2026** — the new suite: FliStudio, fli-core, FliCast, FliCut, Teletubby around FliHub.
  Cross-app plans: `docs/briefs/`.
- **2026-10-03** — FliCut is entered through Start a cut, and screens say "cut" (FliEdit owns "edit"). FliStudio gained Settings → Transcription (paused pending the transcription-as-a-service design). FliTools went two-pass. Real app icons and Dock names landed. ImageDrip (not FliVideo) retired in favour of the ThumbDrip skill.
