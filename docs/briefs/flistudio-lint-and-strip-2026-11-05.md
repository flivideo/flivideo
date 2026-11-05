---
created: 2026-11-05
timestamp: 2026-11-05T15:05+07:00
---
# Brief: FliStudio lint errors + update strip entry (M2 worker)

**Owner**: flivideo-orch (M4), who gates and merges. **David's go**: 2026-11-05. **Folder**: fresh clone at `~/dev/labs/flistudio-cleanup` (never the live checkout `~/dev/ad/flivideo/flistudio`). Branch `lint-and-strip` from origin/main. Run `npm install`, then `npm run build` first.

## 1. Six dep-cruiser errors (from f1e54a4)
`npm run lint` fails on main. `client/src/components/Viewer.tsx` and `modules/storypilot/client/Listen.tsx` import `@flivideo/core/dist/ui` (`index.d.ts`, `speed.css`) directly, breaking `fli-core-only-through-its-public-entry` and, for Viewer, `ui-shell-takes-only-types-from-shared-and-core`.
Check what `@flivideo/core` actually exports. Import through a declared public entry if one exists. If the shared SpeedControl legitimately needs runtime UI from core, a narrow, commented rule exception for that one public entry is acceptable; don't weaken the rules any wider, and report the exception. If the only proper fix is a change to fli-core, end with `APPYNET: question` rather than changing fli-core. Speed control must behave the same.

## 2. Update strip: hyperframes-studio
`apps.updates.list` returns `hyperframes-studio` as `cannot-check` because it has no git origin. It is local-only. Leave it out of the update check and the strip, driven by "no origin / local-only" data or config rather than a hard-coded special case if that's about as simple. Add a test. Other apps unchanged.

## Gate before you finish
`npm run typecheck`, `npm run lint` (0 errors), `STORYPILOT_SEEDS_ALL=1 npm test`. Don't run e2e: this repo's e2e doesn't work on the M2 (known); orch runs it on the M4. Push the branch. Don't merge, restart anything or touch a live app. Use `command grep` (bare grep is shimmed).

End with exactly one line: `APPYNET: done — <one line>`, `APPYNET: blocked — <why>` or `APPYNET: question — <a real decision>`. Never for status.
