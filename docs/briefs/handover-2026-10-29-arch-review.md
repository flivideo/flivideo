# Handover — FliVideo architecture review (2026-10-29)

**Purpose**: Open a fresh session for an architecture review of AppyStack, FliVideo as a whole system, FliStudio, and fli-core. David will give the detailed instructions in the new window.

**For Agents**:
- You are `flivideo-arch-rsch`. Orient, report a short map, then WAIT for David's instructions.
- Do not start the review itself before David speaks.

## Launch line

```
cd /Users/davidcruwys/dev/ad/flivideo
```
```
claude --permission-mode auto --model 'claude-opus-5-5' -n flivideo-arch-rsch "You must be running in /Users/davidcruwys/dev/ad/flivideo — verify your cwd before anything else and STOP if it differs. Read /Users/davidcruwys/dev/ad/flivideo/docs/briefs/handover-2026-10-29-arch-review.md in full and execute it. STOP after the orientation map and wait for David's instructions. Do not edit code, do not start or restart any app, and do not treat the February architecture docs as current."
```

## Governing frame

- **This IS:** an architecture review across four layers, steered by David:
  1. **AppyStack**: the RVETS template that FliStudio is built from;
  2. **FliVideo**: the whole family of apps as one system;
  3. **FliStudio**: the application;
  4. **fli-core** (`@flivideo/core`): the shared library for the Fli apps.
- **This IS NOT:** a build session. You change no code in any app repo, and you start, stop or restart no app. Builds come later, through `flivideo-orch`, in worktrees.
- **Model:** Opus, because this is judgement and design work.

## What to do now (orientation only)

Read enough to give David a one-screen map, then stop. The map covers:
- each layer: what it is, its repo, and its template;
- who depends on fli-core;
- the existing architecture docs, with their dates;
- the open contract decisions you can see.

Then ask David for his instructions.

## Starting facts

All of these were checked 2026-10-29 by flivideo-orch.

**Templates** (from the marker file at each repo root):
- AppyStack (`appystack.json`): FliStudio.
- AppyTron / Electron (`appytron.json`): FliCast, FliCut, FliEdit, Teletubby.
- No marker: FliHub, FliTools, FliDeck, FliGen, FliVoice, Storyline. Their template is not established.

**Where things live:**
- AppyStack: `/Users/davidcruwys/dev/ad/apps/appystack/`, with `create-appystack/` and `appystack-upgrade/` inside it.
- fli-core: `/Users/davidcruwys/dev/ad/flivideo/fli-core/`. It is at **v0.25.0** (the overlay-by-video change).

**Who depends on `@flivideo/core`** (from a package.json grep; worktrees excluded):
- FliStudio: server, shared, client and `modules/overlay-pilot`;
- FliHub: server and shared;
- FliCast, Teletubby and FliTools.
- **FliCut did not show up in the grep.** Verify that before you assert it either way.

**Existing architecture docs.** Both date from February 2026 and may be stale:
- `/Users/davidcruwys/dev/ad/flivideo/docs/flivideo-standard-architecture-v1.0.md`
- `/Users/davidcruwys/dev/ad/flivideo/docs/architecture-alignment-report.md`

**Live ports:**
- FliStudio: 7150 (client) and 7151 (server).
- FliCut: control port 7121.

## Open contract decision already on the table

**Which pipeline stage an extension belongs to.**
- **The problem:** FliStudio's project page puts every extension under the Overlay box. It is hard-coded in `PipelineStrip`, in `/Users/davidcruwys/dev/ad/flivideo/flistudio/client/src/screens/ProjectHome.tsx`.
- **flivideo-orch's recommendation (not yet ruled):** each extension declares `stage` in the descriptor it already exports (for example `OVERLAY_PILOT_MENU`). An extension with no stage goes into a plain "Extensions" group.

**Already settled by the project-page work** (FliStudio commits `e310415`, `1f9fc2b`, `079ef61`, `237046c`):
- An extension is a screen inside FliStudio, shown as a link with no running dot.
- FliStudio reads an extension's results from disk and never calls the module.
- Overlay is optional and never holds the project's current stage.
- An extension's renders compete to become the final video.

## Gotchas

- Run `hostname`; this should be `mac-mini-m4`.
- Builders work only in worktrees, never in live checkouts. Never restart FliCut or FliHub yourself.
- An absent marker file only means "not established". It is not proof of a template, either way.
- Context state: `/Users/davidcruwys/dev/ad/flivideo/docs/orch-checkpoint.md` holds flivideo-orch's state. Read it if you need it, but do not edit it.
