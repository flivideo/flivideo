---
created: 2026-11-05
timestamp: 2026-11-05T15:05+07:00
---
# Brief: my-app restart leaves an orphan nodemon (M2 worker)

**Owner**: flivideo-orch (M4), who gates and merges. **David's go**: 2026-11-05. **Folder**: fresh clone of the `app-registry` repo (remote from `git -C ~/dev/ad/apps/app-registry remote get-url origin`) at `~/dev/labs/app-registry-cleanup`. Branch `restart-orphans`.

## The bug
Each `my-app restart flistudio` on the M4 leaves the previous nodemon alive with ppid=1. It has been killed by hand each time. FliStudio runs `npm run dev` under `concurrently --kill-others` inside tmux session `my-app-flistudio`; the tree is tmux → concurrently → npm → nodemon → tsx → node.

## Do
1. Diagnose from the code and a **throwaway fixture on this machine**: a tiny app with the same process shape (`concurrently`, `npm run`, `nodemon`), registered through a temporary config, never the real registry. Reproduce the orphan first and record the before.
2. Fix it so stop and restart end the app's whole process tree, and only that tree. Never kill by name or pattern across the machine: other apps and sessions run nodemon. Keep the refuse-while-busy behaviour and `--force` unchanged.
3. Show it after the fix: same fixture, three restarts, zero orphans, an unrelated nodemon left alive.

If the right fix belongs in FliStudio's dev script rather than my-app, say so and end with `APPYNET: question`.

## Rules
Don't run `my-app` against any real app, and don't edit the live `~/dev/ad/apps/app-registry` or `~/.config/appydave/`. Clean up the fixture and its processes. Push the branch; don't merge. Use `command grep`.

End with exactly one line: `APPYNET: done — <one line>`, `APPYNET: blocked — <why>` or `APPYNET: question — <a real decision>`. Never for status.
