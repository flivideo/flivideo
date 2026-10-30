# FliHub rebuild — DISCOVERY brief

**Purpose**: Find out what FliHub really does today, and what a rebuild on current AppyStack would gain, so that David can decide whether and how to rebuild it. This is discovery only: no rebuild, and no code changes.

**For Agents**:
- Read this in full first. It is self-contained.
- Written 2026-10-30 by `flivideo-arch-rsch`. `flivideo-orch` (tmux `flivideo-orch`) coordinates FliVideo work. Its checkpoint is `/Users/davidcruwys/dev/ad/flivideo/docs/orch-checkpoint.md`: read it, never edit it.

## Facts already established (don't re-derive them)

- **FliHub** is at `/Users/davidcruwys/dev/ad/flivideo/flihub`. It is the video-project hub: an Express server on :5101 with Socket.io, and a React client on :5100.
- **It predates AppyStack.** Its first commit is `da12b86`, 2025-12-13. AppyStack (first commit 2026-02-26) was later distilled from FliHub, FliGen, FliDeck and Storyline: see `/Users/davidcruwys/dev/ad/apps/appystack/docs/architecture.md:11`.
- **No template marker.** It has no `appystack.json` and doesn't use `@appydave/appystack-config`.
- **No JSON-RPC door.** There is no `/api/rpc`, no `openrpc` and no `control.json` in `server/src`. It is the one FliVideo satellite an agent cannot drive.
- **It is on fli-core v0.26.0** (main `061ae34`). It holds the W8 brand-config version header: `x-brand-config-version`, with 409 on a stale version and 428 when the version is missing.
- **It runs under an overmind shared with AngelEye and Captain's Log.** NEVER stop, restart or `pkill` it, or overmind. Read-only probes of the running app (GET requests, reading logs) are fine.
- **Comparison points** for what current AppyStack looks like:
  - FliStudio, at `/Users/davidcruwys/dev/ad/flivideo/flistudio`: AppyStack 0.4.18, with a capability door, `@flivideo/extension-core` and dependency-cruiser fences.
  - The template itself, at `/Users/davidcruwys/dev/ad/apps/appystack/template`.

## The job

1. **Inventory everything.** Cover every screen and panel, every server route and socket event, every setting and config file it reads or writes, and every watcher and background job. Also cover every file it writes inside project folders, which is FliHub's own area: `hub/`, recordings, transcripts and so on.
   - Cite `file:line` for each item.
   - Use `command grep`, not bare grep: bare grep is shimmed to ugrep and skips gitignored files.
2. **Classify each item as keep, drop or unsure**, with evidence of use where you can find it. Useful places to look:
   - git log activity;
   - FliHub's `.logs/`;
   - whether other apps or skills call it (search `~/dev/ad/appydave-plugins`, FliStudio and fli-core);
   - Captain's Log captures about FliHub (`captains-log:find`);
   - FliStudio features that may now duplicate it.

   Mark anything you can't evidence as **unsure**, never as keep.
3. **List what a rebuild on current AppyStack would gain.** Cover:
   - the JSON-RPC door (agent-drivable, OpenRPC);
   - the template's tooling (husky, appystack-config, depcruise, e2e);
   - extension-core patterns;
   - a clean marker, and upgradability.

   Also list what it would cost or risk: data migration, Socket.io consumers, the shared overmind, and anything that FliStudio, FliCut or the skills depend on.
4. **Produce Claude artifacts.** Use the AppyDave brand, light mode only: load `brand-dave:brand` before writing any HTML.
   - (a) A keep/drop review page David can scan and answer.
   - (b) Two or three look-and-feel directions for a rebuilt FliHub.
5. **STOP and report to David.**
   - Lead with a verdict: rebuild, refresh or leave.
   - Give the artifact links, the counts (keep, drop, unsure), and the questions only David can answer.
   - David's input decides the rebuild.

## Constraints

- **Discovery only.** No code changes in FliHub or any other repo, no branches, no worktrees. The only file you may create is a findings document, committed and pushed to `/Users/davidcruwys/dev/ad/flivideo/docs/` (e.g. `flihub-discovery-2026-10-30.md`).
- **Never start, stop or restart FliHub** or any other app.
- **Report in plain language**, leading with the verdict.
