---
created: 2026-11-04
timestamp: 2026-11-04T10:00+07:00
---
# Brief: speed control — implementation PLAN only (phase 1) + phase 2 matrix (2026-11-04)

**From:** `flivideo-orch`. **To:** `speed-plan-rsch` (**M2**, cwd `~/dev/ad/flivideo`). Report to `flivideo-orch` and STOP.
**Go:** David, 2026-11-04 (decisions recorded on the mocks page). **Machine: M2** — unwatched planning. **No code edits.**

## Read first
- `docs/research/speed-control-decisions-2026-11-04.md` (David's decisions — they override the mocks' original recommendation).
- The live mocks: https://claude.ai/artifact/L27SoDDdwoEsH1bWiMBBZX (or `docs/artifacts/speed-control-mocks-2026-11-04.html` for
  the drawings; the decisions are only in the git note above).
- The four players: `flistudio/modules/storypilot/client/Listen.tsx`, `flistudio/client/src/components/Viewer.tsx`,
  `flihub/client/src/components/shared/` (VideoControlsBar / SpeedControl), `flicut/src/renderer/src/Player.tsx`; fli-core's
  `FORWARD_SPEEDS` and `jkl()`.
- **Dependency:** `help-system-dev` is choosing where shared React UI lives in fli-core (`@flivideo/core/ui` subpath vs a sibling
  package) on branch `origin/help-system` of flistudio / fli-core. Read its choice (`git fetch`; its report or diff) and plan the
  speed control in the SAME place. If it isn't decided yet, say so and plan for both, naming the one you'd pick.

## Write `docs/research/speed-control-plan-2026-11-04.md`
1. **Phase 1 plan:** the shared component (API: `visible` default 3, value, onChange, the ladder, disabled edges, tooltips + ? sheet
   entries via the help system); per player the exact files and what changes; how FliCut (Electron) and the AppyStack apps
   consume it; tests per player (which existing tests assert the ten buttons — list them with file:line); order of work and which
   machine; anything still David's call. Size each step.
2. **Phase 2 matrix** (no plan beyond it): rows = auto-next, transcript display (word / phrase / off), autoplay, size, info
   (duration, file size), prev / next / play buttons, Space = play/pause; columns = FliHub, FliStudio Viewer, Story Pilot Listen,
   FliCut. Each cell: has it? (file:line) and what that player calls its "next thing". Then one paragraph: what to share first.
3. Commit only that file; push.

## Report
The plan's step list with sizes, the package choice it assumes, open questions for David, the sha.
