# Overnight build report — 2026-10-29

**Purpose**: The result of the overnight build run by `flivideo-orch` to `overnight-2026-10-29-build-spec.md`: what passed, what was decided, and the order to merge it in.

**For Agents**:
- Read this before merging any `overnight/2026-10-29-*` branch.
- Nothing here is merged. `main` is untouched in every app repo.
- The gate numbers below were re-run by flivideo-orch in each builder's worktree. They are not copied from builder claims.

## Verdict

**All eight items passed. Nothing was parked.** Every branch is pushed, and fli-core tag `v0.26.0-rc.1` is on `fc1957a`. The run finished about 22:40 local, roughly 1h25m after launch.

**Builders:**
- `ovn-templates-dev` (Sonnet): W1, W2, and the W7 markers.
- `ovn-flicore-dev` (Opus): W3, the fli-core part of W7, W8 in fli-core and FliHub, and W4 for six apps.
- `ovn-flistudio-dev` (Opus): W4, W5 and W8 in FliStudio, W6, and the W8 race rerun.

## 1 · Results

**Gate rule:** after ≥ baseline, with no newly failing test. Every row was reproduced by orch.

| Item | Repo | Branch @ head | Baseline → after (orch rerun) |
|---|---|---|---|
| W1 | appystack | `overnight/2026-10-29-w1-deps` @ `8a79987` | template: typecheck, lint, format, build ok; tests 86 + 44 → 86 + 44; create-appystack 59 → 59; `diff -rq template create-appystack/template` empty; 0 majors in 42 bumps |
| W2 | appytron | `overnight/2026-10-29-w2-deps` @ `92da408` | template: typecheck and build ok, 8 → 8 tests; create-appytron 30 → 30, typecheck ok; Electron ^44.10 |
| W3 + W7b + W8 core | fli-core | `overnight/2026-10-29-fli-core-026` @ `fc1957a`, tag `v0.26.0-rc.1` | typecheck, lint, build, format ok; tests 580 → 627; line coverage 99.01% (gate 90) |
| W4 | flicast | `overnight/2026-10-29-fli-core-026` @ `233779c` | typecheck and build ok; 1341 + 1 skip → same |
| W4 | fliedit | same branch @ `256c98c` | typecheck and build ok; 215 → 220 (new `media-resolver.test.ts`) |
| W4 | flicut | same branch @ `73290f1` | typecheck and build ok; 612 → 612/612 on orch's rerun (one run had 1 known flake, which passed on re-run) |
| W4 | flitools | same branch @ `46e6578` | typecheck ok; 170 → 170. FliTools has no `build` script, so it exits 1 both before and after |
| W4 | teletubby | same branch @ `7213a73` | typecheck and build ok; 438 + 11 skip → same |
| W4 + W8 | flihub | same branch @ `50f33fc` | typecheck and build ok; lint 32 → 32 (baseline problems); shared 115, client 373; server 705 → 715 (one run had 1 flake, which passed on re-run) |
| W4 + W5 + W8 | flistudio | `overnight/2026-10-29-fli-core-026` @ `06123ec` (off `bad7d6b`) | build, typecheck, lint, format, api:check ok; overlay-pilot 60, server 678 → 686 (+2 skip), client 303 |
| W6 | flistudio | `overnight/2026-10-29-template-sync` @ `da89aa0` (off `461042c`) | same checks ok; overlay-pilot 60, server 678 (+2 skip), client 303, **e2e 31/31** (random port, headless) |
| W7a | flicut, flicast, fliedit | `overnight/2026-10-29-w7-marker` @ `77a8a3f` / `65d83cd` / `726950a` | each `appytron.json` `core` equals its package.json `@appydave/core` spec |
| W8 race | FliHub + FliStudio + fli-core | branches above | `race-w8.mts` exits 0. S0–S3a lose nothing. S3b and S4: 0 of 200 lost; 11 and 182 FliHub saves got a 409 "reload" |

**Checks that apply to every row:**
- `grep -rn "kind: *'final'"` finds nothing in the src of any app. FliStudio's single hit is a test that checks `final` is *refused*.
- Every `node_modules/@flivideo/core` reports `0.26.0-rc.1`.
- Every lockfile resolves `fli-core.git#fc1957a9`.

**The W8 race script** is now kept in `/Users/davidcruwys/dev/ad/flivideo/docs/runbooks/brand-race/race-w8.mts`.
- Run it from a folder holding it, with FliStudio's tsx:
  `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/fli-core-026/node_modules/.bin/tsx race-w8.mts`
- It imports from the branch worktrees, so it only works while they exist.
- **Positive control:** the original `race.mts` against the live v0.25 code still shows the losses (S4 lost 198 of 200).

## 2 · Decisions made under the delegation

**fli-core (W3, W8):**
1. **Audio files have an owner.** `audio` + `fli.cut.<v>.json` → flicut, on the evidence of FliCut's `pipeline.ts:164`, which writes `<v>-audio-<arm>`. `part` → "placed file", because only FliStudio's `export.place` writes parts.
2. **`exportApp()` stays name-only.** It returns `null` for `legacy` and `part` rather than guessing, and callers that have the project use `wholeVideoOwner`. Two old assertions changed: `legacy` was `fliedit`, and `part` was `flicut`.
3. **New app list.** A `WholeVideoApp` enum (flicut, fliedit, flicast, flistudio) is used by both `wholeVideoOwner` and `PublishExport.app`. `EditApp` also gained `flicast`.
4. **`updateBrandSettings` returns a version** computed from the bytes it wrote. It never re-reads. A failing `mutate` releases the lock and rethrows.
5. **New `atomicWriteSync` (internal)** for `window-state.ts`'s close-time save.
6. **fli-core now has a CHANGELOG.md.** None existed before; it starts at v0.26.0-rc.1.

**FliStudio (W5, W6):**
1. **Final-video ranking:** FliCast ranks with FliEdit, above FliCut. Overlays still lead.
2. **Unparsed files and parts** now show as "placed file". They used to show as "generated render".
3. **best-transcript has no FliCast step.** A FliCast final reports under `flicut`. Adding a step would change the contract, so this is a **follow-up**.
4. **The schema mirror was not regenerated** in FliStudio, FliCast or FliEdit. It was already out of date at baseline, and nothing gates it.
5. **W6 adds `@appydave/core ^0.1.0`** to FliStudio's server, because the template's `logger.ts` needs it. That package uses zod 3 internally; FliStudio stays on zod 4.
6. **W6 deleted two recipe domain files.** They were template-owned and unchanged, and the template had already removed them.
7. **W6 kept FliStudio's own** `.env.example`, `rateLimiter.test.ts` and `socket.test.ts`. The template versions need template code that FliStudio doesn't carry.
8. **The full per-file table** is `docs/template-sync-2026-10-29.md` on the W6 branch: 112 rows.

**FliHub (W8):**
1. **The version travels as a header** (`x-brand-config-version`). That keeps the payload exactly in brand-config shape.
2. **A POST with no version is refused** with 428. That stops any client quietly reopening the lost update.
3. **FliHub's writes are now validated** by fli-core `BrandSettings`. The real `v-appydave/fli.brand.json` was checked read-only: it validates, and only known keys are present.

**Templates (W1, W2):**
1. **No lockfile in either template.** The bumps raise package.json ranges only, to the versions already installed.
2. **`@hookform/resolvers` 6 skipped:** it's a major.
3. **create-appytron stays on vitest 2,** as the spec required.
4. **Electron 44.10 is accepted** on typecheck, build and tests. **It was never launched.**

## 3 · Parked

None.

**Not run, with the reason:**
- **FliEdit `test:integration` (`door.test.ts`).** It binds port 7171, FliEdit's own port, so it was left for a human run.
- **Live Electron launch of the W2 template.**

## 4 · Merge order (David's go; nothing here is automatic)

**1. fli-core first**, then tag the release:
```bash
cd /Users/davidcruwys/dev/ad/flivideo/fli-core && git pull --ff-only && git merge --ff-only origin/overnight/2026-10-29-fli-core-026 && npm version 0.26.0 --no-git-tag-version && git commit -am "release: v0.26.0" && git tag v0.26.0 && git push && git push origin v0.26.0
```
Copy the v0.26.0-rc.1 CHANGELOG entry to v0.26.0 before the commit.

**2. Templates** (independent, any time):
```bash
cd /Users/davidcruwys/dev/ad/apps/appystack && git pull --ff-only && git merge origin/overnight/2026-10-29-w1-deps && git push
cd /Users/davidcruwys/dev/ad/apps/appytron && git pull --ff-only && git merge origin/overnight/2026-10-29-w2-deps && git push
```

**3. Apps except FliStudio** (FliCast, FliEdit, FliCut, FliTools, Teletubby, FliHub). In each app's `fli-core-026` worktree:
1. Change every `#v0.26.0-rc.1` to `#v0.26.0`.
2. Run the explicit install, `npm install "@flivideo/core@github:flivideo/fli-core#v0.26.0"` (FliHub adds `-w server -w shared`).
3. Check `node_modules/@flivideo/core/package.json` says `0.26.0`, then run the tests and commit.
4. Merge into main from the live checkout, only while that app is not running.

Then merge the `overnight/2026-10-29-w7-marker` branch in FliCut, FliCast and FliEdit (a one-line `appytron.json` change).

**Traps:**
- FliCast's `control-plane.test.ts` asserts the exact pin string, so update it with the repin.
- A plain `npm install` keeps the rc commit from the lockfile.

**4. FliStudio last.** It's live and needs a restart.
1. Merge `overnight/2026-10-29-template-sync` first. It's off current main `461042c`.
2. Rebase `overnight/2026-10-29-fli-core-026`, which is off the older `bad7d6b`, onto it. Both branches change package.json and the lockfile, so re-resolve the lock.
3. Repin to `#v0.26.0` and re-run the gate.
4. Then in `/Users/davidcruwys/dev/ad/flivideo/flistudio`, run `git pull --ff-only && npm install && npm run build`.
5. Run `/Users/davidcruwys/dev/ad/apps/app-registry/bin/my-app restart flistudio` **only on David's go and only with no upload in flight** (the :7151 process with zero :443 connections).

## 5 · Worktrees to remove after merge

Move these to `-trash` or run `git worktree remove`. Check each is clean first.

**Tonight's builds:**
- `/Users/davidcruwys/dev/ad/flivideo/{fli-core,flicast,fliedit,flicut,flitools,teletubby,flihub,flistudio}-worktrees/fli-core-026`
- `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/template-sync`
- `/Users/davidcruwys/dev/ad/flivideo/{flicut,flicast,fliedit}-worktrees/overnight-w7-marker`
- `/Users/davidcruwys/dev/ad/apps/appystack-worktrees/overnight-w1`
- `/Users/davidcruwys/dev/ad/apps/appytron-worktrees/overnight-w2`

**The 2026-10-29 read-only checks:**
- `/Users/davidcruwys/dev/ad/flivideo/{flicast,fliedit,flicut,teletubby}-worktrees/template-drift-check`
- `/Users/davidcruwys/dev/ad/flivideo/{flicast,fliedit,flicut,flitools,teletubby,flihub}-worktrees/fli-core-025-check`

**Also still present from the 2026-10-28 Overlay Pilot build:**
- `flistudio-worktrees/overlay-pilot`
- `fli-core-worktrees/overlay-by-video`
- `flitools-worktrees/audio-clean`
- `flicut-worktrees/audio-via-flitools`

## 6 · Follow-ups (banked, not authorised)

- **best-transcript:** add a FliCast step. This is a contract change.
- **Schema mirrors:** regenerate them in FliStudio, FliCast and FliEdit. They had drifted before tonight.
- **FliHub "reload" banner:** under truly simultaneous saves, most FliHub saves get the "Changed in another app — reload" message. Nothing is lost, but if it happens in practice, consider an automatic retry.
- **FliTools:** it has no `build` script.
- **FliCut:** its `pnpm-lock.yaml` has been stale since 2026-09-01 and has no fli-core entry.
- **The extension core** (review §5) is tomorrow's work with David.
