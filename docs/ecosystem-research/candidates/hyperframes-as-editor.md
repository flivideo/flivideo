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

## Experiment X2 runtime + X1 — 2026-11-03 (M4)

**Verdict: X2 PASS at runtime (loopback, unauthenticated, no CORS). X1 PARTIAL-PASS: four of five edit operations and the music bed are scriptable by CLI `--json`; ducking and ripple are not single CLI verbs; render matches.** 05's X1 pass is "all five operations via CLI `--json`, render matches, Studio stays responsive on 20 min" — strictly **not met** (see gaps; the 20-minute responsiveness test was not run, the project is 65 s).

*Earlier today the first attempt was blocked by the permission checker; David then approved running the CLI inside `~/dev/upstream/scratch/X1` only, and this is the retry.*

**Setup** (M4, scratch `~/dev/upstream/scratch/X1/`, ~35 min of wall time incl. builds): clone `./sync.sh --only hyperframes` (updated, `6feb4bec7`), copied without `.git`. The repo is a **bun** workspace: `pnpm install` fails on workspace packages, so `bun install --ignore-scripts` (12 s) and `bun run --filter @hyperframes/<pkg> build`, **one at a time in order** parsers, core, lint, engine, player, producer, inspector, sdk, studio-server, studio (parallel build fails on missing parsers dist). Then `tsx src/cli.ts <cmd>` works. Telemetry off (`DO_NOT_TRACK=1`, `HYPERFRAMES_NO_TELEMETRY=1`). Scratch grew to 4.6 GB (node_modules + builds + Chromium cache + media).

**X2 runtime (observed)** — `hyperframes preview <dir> --port 7210 --no-open --foreground` (default bind; without `--foreground` it forks a background child that fails here on `hideChildConsoles.js` in a source checkout):
- `lsof`: `bun … TCP 127.0.0.1:7210 (LISTEN)` — loopback only.
- Read: `GET /api/projects`, `/api/projects/proj`, `/files/index.html` → 200, no auth.
- Mutation: `POST /api/projects/proj/files/x2-probe.txt` `{"content":…}` → **201**, file created on disk (deleted afterwards). A PUT from `Origin: http://evil.example` returned 428 only because the file needs an `If-Match` precondition version, not because of any origin/auth check. `POST /file-mutations/patch-element/index.html` with no credentials rewrote `index.html` (used below).
- CORS: no `Access-Control-*` headers on a request with a foreign Origin; preflight OPTIONS → 404 (so browsers block cross-origin reads/writes with preflight; simple requests still reach the server).
- M2 over Tailscale: `ssh davidcruwys@100.126.70.25 curl http://100.82.235.39:7210/api/projects` → connection refused (curl rc 7), same for `mac-mini-m4.local:7210`. **Fails as required.**

**X1 on a d01 copy** (project `proj`: `03-1`+`03-2` takes re-encoded to 25 fps CFR = 65.2 s, 2 DJI clips cut to 12 s 1080p25 as b-roll, a generated sine tone as the "music"; `hyperframes check` passes lint/layout once gsap is served locally from `assets/` — the blank template's jsdelivr `<script>` timed the check out at 60 s even though the CDN answers curl):
| Operation | Via CLI `--json`? | Result |
|---|---|---|
| cut | `timeline split '#take2' 45` | yes, `take2` + `take2-2`, receipt + backup path |
| ripple-delete | `timeline delete '#take1' --start 12 --end 14`, then 4× `timeline move` to close the gap | **delete leaves a gap**; no ripple verb, the agent must compute and issue the moves (or one `timeline apply` plan, not tried) |
| move | `timeline move '#take2-2' 43` | yes |
| trim | `timeline trim '#broll1' --duration 5` | yes |
| music bed | `<audio>` track 2 + `timeline set '#music' --volume 0.5` | yes |
| duck | `timeline set` accepts only `volume=`, `rate=`, `track=`; **`data-automation` lane refused** | done via **REST** `patch-element` (`html-attribute data-automation`, lane 1→0.35→1), not CLI |
| render | `render … -q draft -f 25 -o render-x1.mp4` | **65.2 s, 1920×1080 h264/aac, 16.6 MB, 42 s to render** (hardware GPU, 3 workers); frame at 9 s shows the DJI b-roll over the take |
Evidence files: `~/dev/upstream/scratch/X1/{proj,render-x1.mp4,t.py,preview.log}`. NOT verified: the audio ducking is audible (only that the attribute is in the file and the render completed); Studio responsiveness on 20 minutes; whether the render and the preview agree frame for frame.

**What FliStudio would need** (Inference): keep loopback bind and a FliStudio-owned token proxy if the UI must be reached off-box (no auth, writes + render spawn unauthenticated); an adapter that turns "ripple delete" into delete + moves; use REST `patch-element` for duck/automation; serve gsap locally; run it as a bun-built workspace (not `npx`) when from source. FliEdit stays the footage assembler (E-A) until ripple and ducking have first-class verbs.

**Left running for David**: Studio at http://127.0.0.1:7210/#project/proj (stop: `kill 57524` on the M4, or `pkill -f "cli.ts preview"`).
