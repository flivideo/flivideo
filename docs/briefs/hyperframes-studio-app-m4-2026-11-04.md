---
created: 2026-11-04
timestamp: 2026-11-04T08:40+07:00
---
# Brief: HyperFrames Studio as a proper app on the M4 (`my-app` · :7210 · d01 project kept) (2026-11-04)

**From:** `flivideo-orch`. **To:** `hf-studio-app` (**M4**). Report to `flivideo-orch` and STOP.
**Go:** David, 2026-11-04 ~08:35 ("rebuild it properly on the M4 … install it in my apps directory, thought of like any of my
apps"). **Machine: M4** — an app David watches and uses; no FliStudio code in this job.

## Why
Last night's X1 trial ran Studio from `~/dev/upstream/scratch/X1` (deleted 2026-11-04 07:05) with a d01 test project, started by
hand and stopped by a timer. David wants it installed like his other apps: one home, `my-app start|stop|status`, survives
restarts, and a project that doesn't vanish. Recipe and evidence of last night: `docs/ecosystem-research/candidates/hyperframes-as-editor.md`
§Experiment X1 and §X2 runtime; trial brief `docs/briefs/trial-run-m4-steps-1-2-4-2026-11-03.md` step 4.

## Do
1. **Home:** `~/dev/ad/apps/hyperframes-studio/` (David's ruling: his apps directory). Prefer the **published npm CLI pinned to an
   exact version** (`hyperframes@0.9.9` today) in that folder's `package.json` — small, upgradeable with one bump. Fall back to a
   clone at a release tag only if the published CLI can't serve Studio; say which and why. Never install into or modify
   `~/dev/upstream/repos/hyperframes`. Add a README.md (what it is, upstream URL + licence Apache-2.0, version, how to upgrade,
   ports) and `git init` it locally (no GitHub remote) with node_modules ignored.
2. **Lifecycle:** add `hyperframes-studio` to `~/.config/appydave/apps.json` the way other apps are (display, path, ports {client:
   7210}, group `flivideo`, control start/stop/status/logs, notes: loopback-only, no auth, mutating + render routes). Follow
   `~/dev/ad/apps/app-registry` conventions (read how flicut / flistudio are registered). It must bind **127.0.0.1** only. Commit +
   push the appydave-config change (`git -C ~/.config/appydave` pull first; only apps.json).
3. **Projects live with the video, not the app:** recreate last night's d01 trial composition (chapter 03 + 2 DJI clips, callout,
   cutaway, music duck — per §X1) at `~/dev/video-projects/v-appydave/d01-flivideo-tour/hyperframes/d01-trial/`, **referencing**
   d01 media by relative path or symlink — never copying media. Don't change anything else in d01. Studio should open with this
   project available; say how it finds projects (flag/config) and how a second project would be added.
4. **Prove it:** `my-app start hyperframes-studio` → `lsof` shows 127.0.0.1:7210 → the d01 project opens at
   `http://127.0.0.1:7210/#project/d01-trial` → screenshot (Playwright, close the browser after) → `my-app stop` → nothing listening →
   `my-app start` again and leave it **running** for David. Kill any orphan you create. Disk: report the app folder size.
5. Commit the d01 project's text files (html/json, not media) in v-appydave (`git add` that folder only), push.

## Out of scope
FliStudio code (the "Open in HyperFrames" door is a separate M2 job, pending David's go); renders beyond one draft check; the X2
token proxy; upstream clone changes.

## Report
Install choice + version, apps.json entry, project path + how Studio finds it, lsof line, screenshot path, folder size, commits
(appydave-config, v-appydave, the app's local repo). Anything not verified, say so.
