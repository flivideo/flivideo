---
type: plan
title: Doc skills — improvement plan (from the blind review)
description: "One ranked change plan for dev-team:schema-mirror, system-context and craft-readme, plus doc-drift as the layer over them, synthesised from three independent reviews of the 2026-09-23 runs on six Fli repos."
created: 2026-09-23
timestamp: 2026-09-23
status: applied 2026-09-23 — appydave-plugins 320ec2b (dev-team 0.4.0, appydave 10.2.0); app re-runs dispatched to flivideo-orch
---

# Doc skills — improvement plan

**Purpose**: Turn three blind reviews into one ordered change list David can approve in one go.

**For Agents**:
- Sources: `schema-mirror.md`, `system-context.md`, `craft-readme.md` in this folder (the findings and
  evidence), and the evidence log `../doc-skills-blind-review.md`.
- Skills live in `/Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/`. Waves 1–3 applied in 320ec2b.

---

## The one-line diagnosis

The outputs are mostly true **because the method brief overrode the skills**, not because of them.
Where they fail, it is always the same shape: **a fact written once, then nothing checks it** —
and in schema-mirror's case, a check that shares the blind spot it is meant to catch.

## Wave 1 — correctness (do first)

| # | Skill | Change | Why |
|---|---|---|---|
| 1 | schema-mirror | Detect `z` by the zod *API*, not the import string: follow re-exports (`@appydave/core` → zod) or detect `z.object/z.enum` call shapes | FliCut lost 22 schemas, Teletubby 20, silently |
| 2 | schema-mirror | Every page carries a standing **"Never read by this extractor"** block + a census check (declared `export` counts vs mirrored + gaps). "Nothing" may never print while families were skipped | the page claims completeness it does not have |
| 3 | schema-mirror | Exclude `*.d.ts` / build output by default; fail on duplicate ids | FliHub: 117 duplicates, dead Feb shapes |
| 4 | schema-mirror | verify also checks stale anchors and that `.md` still matches `.json`; stop storing an absolute repo path | verify missed shifted lines and the hand-edited Teletubby page; FliHub's stored path is dead (exit 2) |
| 5 | system-context | **Owned-repo mode as default**: `docs/` + `@docs/AGENT-NOTES.md` in CLAUDE.md; `.context/` + CLAUDE.local.md only for third-party repos | skill and method disagree; Teletubby's notes load nowhere |
| 6 | craft-readme | Replace every CONTEXT.md reference with SYSTEM / AGENT-NOTES / schema-mirror; "link the mirror, never copy a closed set" is a hard rule | a run without the brief would not point into steps 1–2 |

## Wave 2 — gates (make "true when written" stay true)

| # | Skill | Change |
|---|---|---|
| 7 | system-context | Ship `scripts/check_context.py`: AGENT-NOTES ≤ 150 lines **and** ≤ 8 KB; no `file:line`; `sources:` paths exist; import line present; `commit:` present + commits-since count. Non-zero exit fails the run |
| 8 | system-context | Add `commit:` to both templates; content bans: no `file:line`, no counts copied from code, no claims about other tools/files, no machine-specific rules, nothing contradicting CLAUDE.md |
| 9 | craft-readme | Ship a link-and-fact gate: links resolve, named scripts exist, ports in code, versions = manifest, public/private = `gh repo view`, docs-table rows match folder contents; run against `origin/main` |
| 10 | craft-readme | `True at <sha> (<date>)` stamp near Status; a suite-sibling template (same section order for every Fli app, links the suite map) |

## Wave 3 — the layer over the three (David's "sits over them")

| # | Change |
|---|---|
| 11 | Move `appydave:doc-drift` into `dev-team` (pattern: the `sesh` extraction; rewrite 5 references, bump both plugin versions) |
| 12 | Give doc-drift a **doc-set mode**: run `verify_mirror.py` + `check_context.py` + the README gate, then regenerate only what failed, in order 1 → 2 → 3. Generated files (`schema-mirror.*`) are regenerated, never line-edited |
| 13 | Point `agent-comprehension-docs.md` "Re-running later" at doc-drift |
| 14 | `doc-architect` stays out of the method (decision pending: keep in `appydave` or retire) |

## Smaller items (batch with the wave they touch)

- system-context: write `context.globs.json` to the repo root where `query_apps` reads it (4 of 5 repos invisible today) — or fix `query_apps`.
- system-context: move rationale/history (ETH, MITRE, `/doctor`, naming story) into `references/rationale.md`.
- schema-mirror: page usability — keep field docs (98 dropped in FliStudio), add an index (FliCast page is 332 KB), stop "refactor to enum" advice on keyboard keys / HTTP headers / zod internals.

## After the skills change — re-run

Re-run step 1 on **FliCut and Teletubby** (zod), then doc-drift's doc-set mode across all six repos.
Teletubby's hand-corrected mirror (`deef359`) is then replaced by a generated one.

## Fixes in the app repos found by the reviews (not skill changes)

- FliHub + FliCast READMEs call fli-core / FliHub **private** — both are public on GitHub.
- Stale versions in READMEs: fli-core install pins `#v0.1.0` (now v0.6.0); FliCut says core v0.1.0 (pins v0.5.0).
- FliStudio's CLAUDE.md "writes only fli.studio.json" contradicts its AGENT-NOTES.
- Teletubby's CLAUDE.md now loads `@docs/AGENT-NOTES.md` (teletubby 6547eca, David's go).
- FliHub's main checkout on the M4 is 2 commits behind origin (flivideo-orch told).

## Follow-ups found by the re-runs

- schema-mirror: an **object whose values are zod schemas** (Teletubby `INPUT` in `src/core/input-shapes.ts:78` — every verb's input schema) is not read; the census lists it under "never read" (object constant), so it is disclosed, not silent. Extractor improvement: walk object-literal values that are zod schemas. Found in Teletubby re-run a5c44a7, verified in brains 2026-09-23 (all three gates exit 0).
