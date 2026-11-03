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
