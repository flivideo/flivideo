---
created: 2026-11-03
timestamp: 2026-11-03T22:30+07:00
---
# Brief: Send-to-session read-back shows raw harness XML — filter it (2026-11-03)

**From:** `flivideo-orch`. **To:** `tail-filter-dev` (**M2**, code). Branch `session-tail-filter` off origin/main (`c968ec7`+).
Evidence: `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-03/w21-reader-4-send.png` — the "last three messages"
read-back shows a TYPED entry that is raw harness XML (`<task-notification><task-id>…<output-file>…`).

The tail (`server/src/routes/sessions.ts`, `/api/sessions/tail`) must apply the same rule as W1's David-turn filter
(`modules/storypilot` — find the ownTurn / dock-extract filter and **reuse it**, don't fork a second copy): drop
`task-notification`, `system-reminder`, `cross-session-message`, `tool_result`, `isMeta` entries (and skill bodies, pastes,
`[Image #n]` as W1 does). Keep real typed user turns and the assistant's replies.

Tests: unit tests for the tail with a task-notification line, a system-reminder line, a cross-session-message and a normal typed
turn (only the normal one survives as a user turn). Gate: typecheck + full unit + the storypilot e2e specs (CL stub enforced).
Note: `storypilot-w4-dev` is working in `modules/storypilot` on another branch — keep your diff minimal; if you must touch the
shared filter, make it an export, not a rewrite. Push the branch, report sha + tails, STOP.
