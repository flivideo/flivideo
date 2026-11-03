---
created: 2026-11-03
timestamp: 2026-11-03T21:18+07:00
---
# Rework: W1 — e2e must never reach the real Captain's Log (2026-11-03)

**From:** `flivideo-orch`. **To:** `storypilot-w1-dev` (M2), branch `storypilot-w1b`.

M4 re-gate of `f632774`: all unit suites green (storypilot 279), but **1 e2e failed**:
`e2e/storypilot-reader.spec.ts:121` expects "CAPTAINS_LOG_URL is not set on this FliStudio". The M4's shell exports
`CAPTAINS_LOG_URL=https://mac-mini-m2.tail1acb0f.ts.net`; the e2e server inherited it and called the **real** Captain's Log
("Captain's Log has no capture B901"). It passes on the M2 only because the M2 has no such export. Test-isolation bug.

## Fix
1. `e2e/global-setup.ts` (and any unit test that builds `StudioConfig` from env) sets `CAPTAINS_LOG_URL` explicitly for the
   spawned server — removed, or pointed at a local stub. A test must never reach the real CL.
2. If cheap: a CL-configured variant using a local stub server that returns a capture, so the live card's happy path is covered.
3. Prove it: `export CAPTAINS_LOG_URL=https://example.invalid && npx playwright test e2e/storypilot-reader.spec.ts` passes.
4. Typecheck + full unit + storypilot e2e. Commit on `storypilot-w1b`, normal push (no force). Report the sha, STOP.
