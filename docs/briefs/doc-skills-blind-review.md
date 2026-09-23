---
type: brief
title: Blind review of the three doc skills — evidence log
description: "Collects evidence from the 2026-09-23 doc runs (schema-mirror → system-context → craft-readme) across the Fli apps, as input for an independent review of the three dev-team skills once all runs land."
created: 2026-09-23
timestamp: 2026-09-23
status: runs complete — review pending
---

# Blind review of the three doc skills — evidence log

**Purpose**: Hold what the real runs produced, so an independent reviewer can judge the three skills
from outputs, not from their SKILL.md text.

**For Agents**:
- Append evidence as runs land; do not edit the skills from here.
- The review starts only when every run in the table below is done (David, 2026-09-23).
- Skills under review: `/Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/{schema-mirror,system-context,craft-readme}/`.
  Method: `/Users/davidcruwys/dev/ad/flivideo/docs/agent-comprehension-docs.md`.

---

## Runs

| App | Steps | Commits | State |
|---|---|---|---|
| FliCut | 1, 2, 3 | d992f4d … 47594d8 | landed |
| FliCast | 1, 2, 3 | 3a535b3 (mirror, verify OK, 470 structures / 135 closed sets, 16 refactor findings reported, not fixed) · fba04a5 (SYSTEM + AGENT-NOTES, `commit: b061e5e`, AGENT-NOTES 210 → 190 lines) · c3db70e (README) | landed |
| Teletubby | 1, 2, 3 (first time) | "docs: agent-comprehension doc run"; SYSTEM/AGENT-NOTES `commit: 806729c`; ADR-004 + README now say Scribe writes scripts | landed; follow-up 9015c03; **mirror hand-corrected deef359 — a generated file edited by hand, overwritten on the next regeneration**; FliCut zod note 19725fe. The `@docs/AGENT-NOTES.md` line is **not** in CLAUDE.md (the window won't edit CLAUDE.md on a peer's request; waiting on David) |
| FliStudio | re-run 1, refresh 2, 3 (after the trash change) | mirror regenerated (149 structures; verify 57 diffs → exit 0) · SYSTEM + AGENT-NOTES `commit: 81d909a` (46ce2c6) · README links mirror + map | landed |
| FliHub | 1 (first time), refresh 2, light 3 (after the trash change ae2d9b1) | 2fddba7 (docs only). Mirror first run: 330 shapes / 104 closed sets, verify exit 0, one gap (`ContextBodySchema` built with `.partial()`), 19 refactor findings. SYSTEM/AGENT-NOTES `commit: ae2d9b1`, AGENT-NOTES 114 lines | landed |
| fli-core | README link to the mirror only | README links docs/schema-mirror.md (v0.6.0) | landed |
| FliTools | — | — | held: no code, no remote |

## Defects found

### schema-mirror

1. **Zod imported through a re-export is silently skipped.** `zodLocals()` only binds `z` when the
   import source is `zod` or `zod/*`
   (`/Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/schema-mirror/scripts/extract_typescript.mjs:198-215`).
   FliCut imports `z` from `@appydave/core` in 5 files (`src/shared/project.ts:18`, `src/shared/ipc.ts:6`,
   `src/main/ipc-router.ts:2`, `src/main/index.ts:4`, `src/main/control-surface.ts:15`), so every Zod
   schema there (edit file, settings, HTTP bodies) is missing from FliCut's mirror, **with no gap entry**,
   and `verify_mirror.py` still exits 0. Reported by flivideo-orch; reproduced in brains 2026-09-23.
   Severity: high — the mirror looks complete and verified while missing the core contracts.
   **Teletubby is worse**: same import pattern, and its mirror page states "Cannot be mirrored: Nothing"
   while every Zod schema is missing — the page asserts completeness it does not have.
   **Consequence seen:** Teletubby's mirror was hand-corrected (deef359) to cover the gap, which the
   generator will silently undo. Fix the extractor rather than the page.
2. **Nothing runs verify.** FliStudio's mirror drifted 53 differences within a day of generation
   (verify run 2026-09-23). Drift is only caught when someone thinks to run it.

9. **Stale build artefacts swept in.** FliHub's first extraction read stale `shared/*.d.ts` and would
   have published dead Feb-2026 shapes; needed an exclude flag (recorded in FliHub's AGENT-NOTES). The
   default scope excludes tests and configs but not declaration files.

### system-context

3. **No `commit:` in the templates.** Staleness can't be measured without it; the runs added it by hand.
4. **AGENT-NOTES line limit not enforced.** The "well under 200 lines" rule (SKILL.md:24,129) was broken
   by FliCast (210) until this run trimmed it to 190.
5. **Third-party defaults contradict the method**: output to `context/` or `.context/`, import via
   `CLAUDE.local.md`, "do not modify CLAUDE.md" (SKILL.md:225-229,553-556,617) vs the method's `docs/` +
   `@docs/AGENT-NOTES.md` in CLAUDE.md. Runs were told to follow the method.
6. **Writes facts about other skills that go stale** — three AGENT-NOTES said "no TypeScript extractor"
   and were wrong the same day.

10. **Hand-written file:line anchors drift.** FliHub's AGENT-NOTES cited `ProjectStage` at :438; it had
    moved to :274. Dropped in favour of pointing to the mirror — the skill should never hand-write
    anchors the mirror already carries.

### craft-readme

7. **Still refers to CONTEXT.md** (SKILL.md:8,23,77,129), not SYSTEM.md / AGENT-NOTES.md.
8. **Doesn't reliably point into steps 1–2**: fli-core's README linked its mirror 0 times.

11. **Invented a doc.** FliHub's README listed a "collaborator setup" guide that does not exist. The
    skill's self-review did not catch a dead link.

## Related decision (held for David)

`appydave:doc-drift` should become the layer over the three steps (staleness check + regenerate in order)
and move into `dev-team`; `appydave:doc-architect` stays out of the method. Assessed 2026-09-23; edits
held until this review.
