---
type: reference
tags: [flivideo, ecosystem-research, candidate, B686, hyperframes]
description: "Can HyperFrames be driven as an editor inside FliVideo (like FliCut), and how does it overlap FliEdit?"
created: 2026-11-03
timestamp: 2026-11-03T12:30+07:00
---

# HyperFrames as an editor surface

**Purpose**: Can HyperFrames be driven as an editor inside FliVideo (like FliCut), and how does it overlap FliEdit?

**For Agents**: Research only (B686 B2, 2026-11-03). *Observed* = read in repo or via `gh api`; *Inference* and *Lean* are B2's and **not approved**. Anything unread is **UNVERIFIED**. Index: [../03b-capability-landscape.md](../03b-capability-landscape.md).

## Verdict (spike, plan §7)
**Observed**: it is an editor surface, not only a renderer. **Inference**: it is a *composition/motion-graphics* editor, weaker as a general footage-cutting NLE.

- **Repo**: https://github.com/heygen-com/hyperframes (clone `188475aaf`, 2026-10-08, at `/Users/davidcruwys/dev/upstream/repos/hyperframes`).
- **Licence**: Apache-2.0 (GitHub API). Commercial use allowed.
- **Stars / last commit**: 77,839★, pushed 2026-11-03T03:35Z, 225 open issues, pre-1.0 (`@hyperframes/studio` 0.8.141).
- **Agent surface** *(Observed in code)*:
  - Embeddable NLE React components: `EditorShell`, `NLEPreview`, `Timeline`, `Dock`, `Player` (`packages/studio/src/index.ts`) — can be mounted like FliCut inside FliStudio.
  - REST API (Hono) in `packages/studio-server`: file CRUD, `file-mutations/{split-element,patch-element,remove-element,wrap-elements,insert-composition,freeze-frame}`, GSAP mutations, `/history` undo/restore/claim (`routes/files.ts`, `routes/history.ts`).
  - CLI with `--json`: `timeline` (move/trim/split/delete/set/duplicate verbs, `packages/cli/src/timeline/a2Commands.ts`), `history`, `check`, `snapshot`, `preview --context --json` (live user selection).
  - Headless `@hyperframes/sdk` editing engine (`packages/sdk/src/session.ts`).
  - **No JSON-RPC, no MCP server found.** An adapter would be thin REST/CLI.
- **Security**: *Observed* — repo has `SECURITY.md`; studio-server routes include path-safety tests (`routes/files.pathSafety.test.ts`). Studio-server is a local HTTP service: exposure/auth model **UNVERIFIED**; assume localhost-only until checked. Headless Chrome (Puppeteer) renders arbitrary HTML/JS compositions, so untrusted compositions run code.
- **Two questions**:
  1. *Elegant?* Yes for overlays and motion graphics timed to transcripts (HTML + GSAP, deterministic render, `check` gate). Not shown for multi-hour A/V editing; **UNVERIFIED** (not run).
  2. *Agent-drivable safely?* Strongest in this research: documented CLI/REST, undo history, project lock for multiple agents, rendered-output audit.
- **Outcome lean (not approved)**: *add* as an editor capability inside FliStudio alongside FliCut (what David asked); *absorb* for overlays (already the engine under Overlay Pilot work); *replace FliEdit* only if the footage-editing gap is closed — open question.

## Overlap with FliEdit (shared question with FliEdit replacement)
- FliEdit = assembly of footage into a multi-track timeline. HyperFrames timeline = clips of HTML/media on tracks, `data-start/duration/track-index`, rendered from the browser.
- Overlap: placing and timing media and overlays. Gap: no footage-centric cut/ripple/audio-mix evidence found. **UNVERIFIED** beyond reading the code.
- Prior brain study: `brains/video-as-code/hyperframes-fundamentals.md`, `api-surfaces.md`, `creating-with-hyperframes.md`.

## Experiment X2 — 2026-11-03

**Verdict: PASS on code-read only — runtime measurement NOT DONE (UNVERIFIED).** 05's pass test is "binds localhost by default, or takes a token".

**Observed in code** (clone `188475aaf`, read-only):
- **Default bind is loopback.** `packages/cli/src/server/portUtils.ts:447`: `host = bindHost ?? (process.env.HYPERFRAMES_PREVIEW_HOST?.trim() || "127.0.0.1")`, listen at `:472`. The comment at `:439-446` (finding "F-001") says the API is unauthenticated and LAN exposure is opt-in via `HYPERFRAMES_PREVIEW_HOST=0.0.0.0`.
- **`packages/studio-server` never listens.** It is a Hono app (`createStudioApi.ts`); the CLI (`packages/cli/src/server/studioServer.ts`) mounts and binds it.
- **No token auth, no CORS middleware.** No `hono/cors` and no Access-Control headers in `studio-server/src` or `cli/src/server`. The only `*token*` is `X-Hyperframes-Write-Token` (`routes/history.ts:28`), a write-attribution label, not auth.
- **Only guard is a Host check against DNS rebinding.** `server/telemetryIdentity.ts:77` (`isLoopbackHost`), `:251`, `identityAllowed`. Its own comment says it is "not access control". `/api/open-in-desktop` POST adds Origin/Sec-Fetch-Site checks (`server/desktopRoutes.ts:11`).
- **Mutating routes, all unauthenticated** (bind address is the only protection):
  - File write/create/delete: `routes/files.ts:2597` (PUT), `:2704` (POST), `:2724` (DELETE), `:3403` (PATCH); `file-mutations/*` from `:2743`; `gsap-mutations*` from `:3536`; `duplicate-file` `:3432`; upload `:3467`.
  - History undo/restore: `routes/history.ts:96,102`.
  - Process / compute spawn: `routes/render.ts:66` (render, headless Chrome), `routes/loudness.ts:84`, `routes/media.ts:166`, `routes/freezeFrame.ts:185` (ffmpeg), `routes/registry.ts:16` (installs catalog blocks).
- Upstream's own docs in the code say that with `HYPERFRAMES_PREVIEW_HOST=0.0.0.0` anyone on the LAN can read/write/delete project files and spawn renders.

**NOT checked (UNVERIFIED)**: actual `lsof` bind line, `curl` read and mutation, M4-over-Tailscale read, live CORS headers. Cause: starting the server in the scratch copy was refused by the harness auto-mode classifier (two attempts, no reason given), and `npx bun` was refused earlier. Scratch state: `~/dev/upstream/scratch/x2/` (hyperframes copy + `pnpm install --ignore-scripts` for `@hyperframes/cli...`, plus `project/`); nothing is running. Run recipe: `cd ~/dev/upstream/scratch/x2/hyperframes/packages/cli && ../../node_modules/.bin/tsx src/cli.ts preview ../../../project --port 4791 --no-open`.

**What FliStudio would need to embed it safely** (Inference): keep the default loopback bind and never set `HYPERFRAMES_PREVIEW_HOST`; if FliStudio's UI must reach it from another machine, put it behind a FliStudio-owned token proxy (or Tailscale-only bind to the single tailnet IP) because the upstream API has no auth; treat all `file-mutations`/`render` routes as full-trust; only open compositions you trust (they run code in headless Chrome).

## Experiment X2 runtime + X1 — 2026-11-03 (M4) — BLOCKED, NOT RUN

**Verdict: no new evidence. Stopped at the permission checker, as the brief instructs.** The X2 code-read PASS above still stands; the runtime half (lsof bind line, curl read + mutation, CORS header, M2-over-Tailscale read that must fail) and all of X1 are **UNVERIFIED**.

**Done**: `./sync.sh --only hyperframes` (clone updated, 496 MB); copied to `~/dev/upstream/scratch/X1/hyperframes` (no `.git`); `pnpm install --ignore-scripts --filter "@hyperframes/cli..."` OK in 25 s (node 24.13, pnpm 11.20). Scratch is 3.0 GB with that install.

**Blocked command** (denied by the auto-mode classifier, no reason given — the same refusal the earlier M2 attempt hit): `cd ~/dev/upstream/scratch/X1/hyperframes/packages/cli && ../../node_modules/.bin/tsx src/cli.ts --help` (the `tsx` runner for the CLI source; even `--help`). Nothing was started; no workaround tried.
