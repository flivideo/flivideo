---
created: 2026-11-03
timestamp: 2026-11-03T15:45+07:00
---
# Brief: experiment X2 — what does HyperFrames' studio-server expose, and to whom? (2026-11-03)

**From:** `flivideo-orch` (Swagger). **To:** `x2-hf-server-rsch` (M2, cwd `/Users/davidcruwys/dev/ad/flivideo`).
Report to `flivideo-orch` by name. **Go:** David, 2026-11-03 ~15:40 ("Do the safe, do the X2"). He isn't watching: run to done.

## Context (read first)
- Experiment definition: `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/05-research-experiments.md` row **X2**.
- Candidate file (write the result here): `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/candidates/hyperframes-as-editor.md`
  (line ~27 currently says the exposure/auth model is UNVERIFIED).
- Register row it feeds: **R10** in `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/06-approval-register.md`.
- Registered clone: `~/dev/upstream/repos/hyperframes` at `188475aaf` (package `packages/studio-server`, Hono REST API).

## Do
1. `git pull` in `/Users/davidcruwys/dev/ad/flivideo`. Do **not** pull or modify the upstream clone.
2. **Read** (no running yet): how studio-server picks its host/port, any auth/token/CORS middleware, and which routes
   mutate files or spawn processes (`packages/studio-server/src/**`, `routes/files.ts`, `routes/history.ts`, the CLI
   command that starts it in `packages/cli`). Note file paths + line numbers.
3. **Run it in scratch only:** copy the clone to `~/dev/upstream/scratch/x2/hyperframes` (`git worktree` or `cp -R`,
   not inside the registered clone), install deps there, start the studio server against a throwaway project in
   `~/dev/upstream/scratch/x2/project`.
4. Measure: `lsof -nP -iTCP -sTCP:LISTEN | grep <pid>` → bind address (127.0.0.1 vs 0.0.0.0/*). From this machine
   `curl` one read route and one harmless mutation (on the throwaway project). If it binds beyond localhost, try the
   same read from the M4 over Tailscale (`ssh davidcruwys@100.82.235.39 curl …`) — **read routes only from the M4**.
   Check whether any token/header is required. Check CORS headers on a cross-origin request.
5. Stop the server; confirm with `lsof` that nothing is still listening. Leave the scratch folder (note its size).
6. Write a dated `## Experiment X2 — 2026-11-03` section in the candidate file: verdict **pass / fail** against
   05's "Pass if: binds localhost by default, or takes a token", the evidence (bind line, curl outputs, code refs), and
   what FliStudio would need to embed it safely (e.g. bind flag, token proxy). Mark anything not checked as UNVERIFIED.
7. In `06-approval-register.md` row R10, append to the **Recommendation** cell only: "X2 2026-11-03: <pass/fail, one
   phrase>". **Never change any Status cell.**
8. Commit only those two files + this brief's result note if any (`git add <paths>`), push to main.

## Limits
- Timebox 1 h. No edits to any app repo (`flistudio/`, `fliedit/`, …) or to `~/dev/upstream/repos/*`.
- Nothing listening when you finish. No new clones (use `upstream:upstream-add` if one is truly needed — it isn't expected).
- Keep the M2 light: no renders, no Chrome renders of compositions beyond what starting the server needs.
- STOP after the push and report to `flivideo-orch`: verdict, bind address, auth yes/no, commit sha.
