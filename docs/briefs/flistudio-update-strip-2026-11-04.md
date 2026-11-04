---
created: 2026-11-04
timestamp: 2026-11-04T17:45+07:00
---
# Brief: FliStudio "apps out of date" strip — check and update this machine's Fli apps (2026-11-04)

**From:** `flivideo-orch`. **To:** `update-strip-dev` (**M2**). Report to `flivideo-orch` and STOP.
**Go:** David, 2026-11-04 ~17:40 ("I think we can start building it. Yeah, go on it."). **Machine: M2** — code, standing ruling.
Design + findings: `docs/specs/fleet-versions-2026-11-04.md` (read the Decision section at the end — it narrows the page) and the page
https://claude.ai/artifact/3nJ5v9cSYu8KGryjjGdvh9.

## What David wants
If you're running FliStudio and any Fli app on **this machine** is behind, a quiet strip at the top says so, with an Update button.
Updating never restarts anything. Works the same on the M4, the M2, Jan's machine, anyone's.

## Do
1. **App set** = `~/.config/appydave/apps.json` entries with `group: "flivideo"` whose `path` exists on this machine and is a git repo
   (resolve `~`). Read at check time; don't hard-code app names.
2. **Check** (fixed commands via `execFile`, no shell): `git fetch --quiet origin`; branch; `rev-list --count HEAD..origin/main`
   (behind) and `origin/main..HEAD` (ahead); dirty = `status --porcelain` non-empty; last-fetched time. A fetch failure (offline,
   GitHub down — there is an outage today) = state "couldn't check" with the reason, never an error toast. One check at a time.
   Timer: at server start, then every 4 h (one constant), plus "Check now". **No launchd/background job** — FliStudio's server only.
3. **Update one app** (and "Update all"): refuse with the reason shown when dirty, branch ≠ main, or diverged (ahead > 0); else
   `git merge --ff-only origin/main`; if `package-lock.json` changed between the old and new sha → `npm install` in that repo (log
   its tail); never restart. Afterwards mark **"updated · restart pending"** when the app is running (my-app status) — for FliStudio
   itself compare the sha it started on with the sha now on disk.
4. **Verbs** (agent-drivable, stamped `changed.by`, door-logged, dry-run): `apps.updates.list` (cached status + checkedAt),
   `apps.updates.check` (run a check now), `apps.update { app | all, dryRun? }`. Regenerate `api/openrpc.json`; update the pinned
   capability tests on purpose; `bin/flistudio` gets the same.
5. **Strip** at the very top of FliStudio's app shell, AppyDave light, quiet: hidden when everything's up to date; otherwise e.g.
   "3 apps out of date · FliStudio 9 · Teletubby 9 · FliEdit 2 · Update all". Clicking an app opens a small panel: behind/ahead,
   dirty, branch, last checked, Update (or the refusal reason), restart pending. "Check now" there. Tooltips per the help-system rule
   (no inline key hints). Uses existing components/tokens.
6. **Tests**: unit with **real temp git repos** (origin + clone): behind, dirty refusal, non-main refusal, diverged refusal,
   ff update, lockfile-changed → install called (stubbed), unchanged → not called, fetch failure → "couldn't check". e2e for the
   strip with the server status stubbed (hidden / shown / refusal / restart pending), run in full.

## Setup / gate
Worktree: `git -C ~/dev/ad/flivideo/flistudio fetch origin && git -C ~/dev/ad/flivideo/flistudio worktree add ~/dev/ad/flivideo/flistudio-worktrees/update-strip -b update-strip origin/main`;
`npm install`; **`npm run build` first**, then typecheck + full unit + the e2e you add + `project-status.spec.ts`. Never touch the
M2's live checkout (it has 9 uncommitted files — not yours). Push branch `update-strip` (if GitHub still fails, commit locally and say
so); report sha, test counts before → after, screenshots of the strip states; STOP. Orch gates on the M4 and merges.

## Out of scope
Other machines (no ssh, no bundles), restarts, any background job, changing apps.json.
