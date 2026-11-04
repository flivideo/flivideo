---
created: 2026-11-04
timestamp: 2026-11-04T17:40+07:00
---
# Fleet versions — FliStudio brings the Fli apps up to date on other machines (spec, 2026-11-04)

**Purpose:** design for a Versions view + "Bring to latest" in FliStudio. Research only; nothing was changed on any machine.
**For Agents:** read before building `fleet.versions` / `fleet.update`. Page: https://claude.ai/artifact/3nJ5v9cSYu8KGryjjGdvh9 · source `docs/specs/fleet-versions-2026-11-04.html`.

## Findings
- App set (six with code): FliStudio, FliCut, FliEdit, FliHub, Teletubby, FliCast — `~/.config/appydave/apps.json` (group `flivideo`); repos `git@github.com:flivideo/<app>.git`, `main`.
- FliStudio has `app.launch/stop/restart/stage` (`flistudio/api/openrpc.json:22,489,999,1458`; handler `server/src/capabilities/registry.ts:245`, code in `server/src/launch/`). `capabilities/launch.ts` (named in the brief) is the YouTube-launch feature, not this. **No fleet/version/update verb exists.**
- Jan (`jan-mini` in `~/.config/appydave/machines.json`): SSH works; GitHub does not work over his SSH, so repo updates travel as git bundles. **David Kaff is not in the roster.**
- Measured 2026-11-04 (behind = vs GitHub main, via `git ls-remote`): M4 all six latest and clean. M2: FliStudio 065129d 9 behind + 9 uncommitted, FliEdit dc39399 2 behind, Teletubby 44e0011 9 behind + 1 uncommitted, others latest. Jan: FliStudio 44d2fd8 3 behind clean, FliHub 3b3b2f1 194 behind + 1 uncommitted, other four not installed.

## Recommendation
Read-only Versions view first; then consent-gated "Bring to latest" (fetch, `pull --ff-only`, `npm install` only if the lockfile changed, never restart; refuse on dirty / non-main / diverged). SSH over Tailscale for David's own machines, git bundles for Jan and anyone off the tailnet, agent deferred. Fixed commands only, dry-run default, stamped principal, "update ready · restart pending" after a pull. Verbs: `fleet.versions`, `fleet.update`, `fleet.bundle`.

## Decisions for David
1. Jan: Versions standing, Update per-run with Jan (or his liaison) approving? (recommended)
2. David Kaff: how does his machine connect (Tailscale, or bundles only)? Recommend leaving him out of v1.

## Not checked
Kaff; Roamy / Mary / Angela; Jan's other Fli directories and what his uncommitted FliHub file is; node_modules vs lockfile; no fetch or pull was performed anywhere.

## Decision (David, 2026-11-04 ~17:40): a local "out of date" strip first
Each FliStudio checks **its own machine's** Fli apps and shows a quiet strip at the top when any is behind; the person at that
machine clicks Update. No cross-machine access in v1 (the fleet table is a later extra). Check at FliStudio startup + every 4 h
+ "Check now"; never auto-update; no background job (FliStudio's server timer only). Build brief:
`docs/briefs/flistudio-update-strip-2026-11-04.md`.
