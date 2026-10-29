# Brief — merge prep for v0.26.0, and @appydave/core on zod 4 (2026-10-29)

**Purpose**: Two builder jobs that follow the overnight build. David gave his go at about 22:25 on 2026-10-29: "move forward on everything, I give permission for all things to be done". `flivideo-orch` is the boss.

**For Agents**:
- `ovn-merge-dev` does **Job A** only, and `core-zod4-dev` does **Job B** only.
- Both work in worktrees, push branches only, and report to flivideo-orch with SendMessage.
- flivideo-orch does every merge into a live checkout, and every app start or restart, itself.

**Already done:** fli-core `v0.26.0` is tagged on main at `4fb29ce`, unchanged from rc.1.

**Background:**
- Overnight report: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/overnight-2026-10-29-report.md`
- Architecture review: `/Users/davidcruwys/dev/ad/flivideo/docs/architecture-review-2026-10-29.md` (§1.2 is the zod split).

## Job A · ovn-merge-dev (Opus)

### A1 · The six apps
**Repos:** flicast, fliedit, flicut, flitools, teletubby, flihub.

In each existing worktree, `/Users/davidcruwys/dev/ad/flivideo/<repo>-worktrees/fli-core-026` (branch `overnight/2026-10-29-fli-core-026`):
1. Rebase onto current `origin/main` if main has moved.
2. Change every `#v0.26.0-rc.1` to `#v0.26.0`.
3. Install explicitly: `npm install "@flivideo/core@github:flivideo/fli-core#v0.26.0"` (FliHub adds `-w server -w shared`).
4. Confirm `node_modules/@flivideo/core/package.json` says `0.26.0`, and that the lockfile resolves `fli-core.git#4fb29ce`.
5. FliCast's `control-plane.test.ts` asserts the pin string; update it.
6. Re-run that repo's gate exactly as the overnight report §1 lists it. Commit and push the branch.

### A2 · FliStudio
1. **On `overnight/2026-10-29-template-sync`** (worktree `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/template-sync`):
   - remove the `@appydave/core` dependency from the server;
   - restore FliStudio's own pre-W6 `server/src/config/logger.ts`;
   - update `docs/template-sync-2026-10-29.md` so the logger row reads "kept-app until @appydave/core 0.2.0 (zod 4)";
   - re-run the gate, including e2e, then push.
2. **Then on `overnight/2026-10-29-fli-core-026`** (worktree `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/fli-core-026`):
   - rebase onto the updated template-sync branch head;
   - re-resolve the lockfile;
   - repin all four workspaces to `#v0.26.0`, with the explicit install;
   - re-run the full gate, including e2e;
   - push it as `overnight/2026-10-29-flistudio-final`. That branch must fast-forward from current FliStudio `origin/main` plus template-sync.

### A3 · Report
Report each repo's branch, head and gate numbers to flivideo-orch. **Done when every A1/A2 branch is pushed and gate-passed, or parked with a reason.**

## Job B · core-zod4-dev (Opus)

**Goal:** `@appydave/core` **0.2.0 on zod 4**, so that every app has one zod. Today the family installs zod 3 through `@appydave/core` and zod 4 through fli-core, and Teletubby has already hit a TS2719 error from it.

**Repo:** `/Users/davidcruwys/dev/ad/apps/appydave-foundation`, package `packages/core`. Work in a worktree under `/Users/davidcruwys/dev/ad/apps/appydave-foundation-worktrees/`, on branch `core-0.2.0-zod4`.

### B1 · Move core to zod 4
- zod 4 as a dependency, or as a **peer dependency**. Decide which and write down why. A peer dependency avoids a second copy; it is the review's alternative.
- Fix `src/config.ts` and anything else that uses zod 3 API (`.issues` vs `.errors`, `z.string().email()` changes, error maps).
- Keep the public API the same apart from the zod major.
- Version 0.2.0, with a CHANGELOG entry.
- Gate: typecheck, build and tests pass.

### B2 · Consumer impact (read-only, measured)
- Find every consumer: the review lists 12 (AppyStack template, AppyTron template, FliCast, FliEdit, FliCut, Teletubby, AngelEye, Captain's Log and others). Grep to confirm.
- Find how each one gets the package: npm `^0.1.0`, or a vendored tgz such as `file:vendor/appydave-core-0.1.0-791e1c9.tgz`.
- In a throwaway worktree per FliVideo consumer, install a packed 0.2.0 tgz and run typecheck and tests. Record the result in a table.
- **Do NOT edit consumer branches or publish to npm.** flivideo-orch decides the rollout from your table.

### B3 · Report
Send flivideo-orch the branch, head, gate numbers, the consumer table and your dependency-vs-peer decision.

## Limits (both jobs)

- Never merge to main, touch a live checkout, start/stop/restart any app, run `my-app`, or `npm publish`.
- No `pkill -f` or `killall`.
- Never use ports 7150, 7151, 7121, 7161, 5173 or 5101; tests use random ports.
- Never touch `/Users/davidcruwys/dev/video-projects/`, `~/.config/appydave/` or `~/.claude/`.
- Park, with a reason, anything that fails its gate after 3 attempts.

## Job C · core-rollout-dev (Opus): roll @appydave/core 0.2.0 out to its consumers

Added 2026-10-29 by flivideo-orch. Job B is done: branch `core-0.2.0-zod4` @ `1cd0e79` in `/Users/davidcruwys/dev/ad/apps/appydave-foundation-worktrees/core-0.2.0-zod4`.
- zod is a **peer dependency** (`^4.0.0`).
- The packed tgz is at `/Users/davidcruwys/dev/ad/apps/appydave-foundation-worktrees/appydave-core-0.2.0-1cd0e79.tgz`. It is not published.
- Probe worktrees `<repo>-worktrees/core020-probe` (flicast, fliedit, flicut, teletubby) already sit on 0.2.0. Reuse them or remove them.

**Branching rule:**
- Each FliVideo app gets a new branch, `core-020-zod4`.
- Base it on `origin/overnight/2026-10-29-fli-core-026` **once that branch pins `#v0.26.0`**. ovn-merge-dev is doing the repin; poll `git show origin/overnight/2026-10-29-fli-core-026:package.json`.
- Templates branch off current main: appystack `8a79987`, appytron `92da408`.

### The items

- **C1 · FliCast + FliEdit**
  - Vendor `vendor/appydave-core-0.2.0-1cd0e79.tgz`.
  - Point the package.json `@appydave/core` spec **and** the `appytron.json` `core` marker at it; they must be equal.
  - Run the gate (overnight report §1 commands).
  - Measured as drop-in.
- **C2 · FliCut:** the same as C1, plus fix its zod 3 idioms:
  - `z.record` with one argument, in `src/shared/project.ts:78,187,190`. Add the key schema.
  - `z.ZodTypeDef` in `src/main/ipc-router.ts:9`.
  - `process-supervisor` "captures stdout" is a known flake.
- **C3 · Teletubby**
  - Vendored 0.2.0. Record that npm `^0.2.0` replaces it after the publish.
  - Retire `src/core/zod3-json-schema.ts`, which reads zod 3's `_def.typeName`. Project through zod 4 instead: fli-core's path or `z.toJSONSchema`.
  - Fix `handlers.ts` (68 TS errors) and `input-shapes.ts` (5).
  - Regenerate the API: `npm run api:openrpc`.
  - Gate: no newly failing test.
- **C4 · Templates**
  - **AppyStack** `template/` + `create-appystack/template`: zod `^3` → `^4`, and core → 0.2.0. Use the tgz or a `file:` link for now, and record the npm swap. Fix what breaks, run `npm run sync`, and gate as in W1.
  - **AppyTron** template: vendored 0.2.0 + marker. Gate as in W2.
- **C5 · Probe only (read-only)**
  - ImageDrip and Samantha (a live `file:` link to foundation `packages/core`), plus AppySentinel core and its template.
  - Point a throwaway worktree at the `core-0.2.0-zod4` worktree, and run typecheck and tests.
  - Report a verdict per consumer.

**Done when:** every C item is gate-passed with its branch pushed, or parked with a reason. Report a table to flivideo-orch.

**Limits:** the same as Jobs A and B. No merges to main, no `npm publish`, no app starts.
