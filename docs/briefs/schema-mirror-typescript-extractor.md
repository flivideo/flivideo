# Brief — add a TypeScript + zod extractor to `dev-team:schema-mirror`

**Written** 2026-09-22 by the FliStudio session (David approved extending the skill; the approach below is Claude's
call, delegated by David). **Runs in**: `/Users/davidcruwys/dev/ad/appydave-plugins`. **Model**: Opus (extractor design
is judgement work).

## Why

The Fli apps (FliStudio, FliHub, FliCut, FliCast, Teletubby, fli-core) are all TypeScript + zod. `schema-mirror` ships
only `extract_python.py`; `detect_stack.py` reports `typescript` and `zod` as `[GAP] … UNMIRRORED`. Step 1 of the agent
comprehension technique (`/Users/davidcruwys/dev/ad/flivideo/docs/agent-comprehension-docs.md`) therefore cannot run on
any of them.

## Read first

- `/Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/schema-mirror/SKILL.md`
- `…/schema-mirror/references/adding-a-stack.md` (the IR contract and extractor rules — follow it exactly)
- `…/schema-mirror/references/derivation-gate.md`
- `…/schema-mirror/scripts/extract_python.py` and `scripts/mirror_lib.py` (the reference extractor and the gate)
- `/Users/davidcruwys/dev/ad/appydave-plugins/CLAUDE.md` (version bump before commit)

## The approach — decided, build this

**Static extraction, anchored, no runtime evaluation.** The skill's one property is that every value is read from a
`file:line` and the gate re-opens that line. Loading modules and calling `z.toJSONSchema` gives accurate shapes but no
anchors, so it is rejected as the primary route.

1. **Parser**: the TypeScript compiler API, resolved from the **target repo's own** `node_modules/typescript` (every Fli
   repo has it). The skill adds no npm dependency. If the target has no `typescript`, exit with a clear error — never
   fall back to regex parsing.
2. **Shape**: a Node script (e.g. `scripts/extract_typescript.mjs`) does the parsing and emits the IR; keep the CLI of
   `extract_python.py` (positional root, `-o`, `--include`, `--exclude`, `--no-default-excludes`). If the skill's
   conventions want a `.py` entry point, a thin wrapper that runs node is fine. It must end by running the existing
   Python gate (`mirror_lib.validate_ir`) and exit non-zero on violations — do not reimplement the gate in JS.
3. **One extractor, both registry rows**: `typescript` and `zod` in `STACKS` (`mirror_lib.py`) both name it.
4. **What it extracts** (grade `declared` when a single symbol states the whole thing):
   - TS: exported `interface`, `type` aliases of object shapes, string/number literal unions, `enum`, `as const` objects
     and arrays used as closed sets.
   - zod: `z.object({...})` (fields + anchors), `z.enum([...])`, `z.literal`, `z.union` / `z.discriminatedUnion` of
     literals, `.extend({...})`, `.shape` access, `z.infer` aliases linked to their schema.
   - **Composition**: follow an identifier to its definition when it is resolvable statically inside the repo (same
     file, or an import from a relative path) and anchor at the definition, per the "reached through another symbol"
     rule. An import from a package (e.g. `@flivideo/core`) is recorded as a reference to that package, not expanded.
   - **Helper calls that build schemas** (e.g. `scanned(ProjectRow)`, `zoneScan(...)`, `callResult(...)`): record as
     `unresolved` with the helper named and what was looked at. A named gap is a correct answer.
   - Closed sets reconstructed from control flow (`switch` on a string field with no declaring union) → `derived`, with
     the required refactor finding.
5. **Tests** for the extractor on small fixture files covering each case above, in whatever form the skill's existing
   scripts use (add a minimal one if none exists).

## Pilot, in this order

1. `/Users/davidcruwys/dev/ad/flivideo/fli-core` — pure contracts, 30 TS files.
2. `/Users/davidcruwys/dev/ad/flivideo/flistudio` — `shared/src/contracts.ts` composes from `@flivideo/core`.

For each: render to `docs/schema-mirror.md` + `docs/schema-mirror.json`, run `verify_mirror.py` (must exit 0), open a
sample of anchors by hand, and fix the **extractor** — never the output — for any miss. Then commit the two mirror files
in that repo (docs only) and push to `main`.

## Done when

- Extractor + registry rows + tests + SKILL.md / `adding-a-stack.md` updated (per-stack notes for TypeScript/zod), plugin
  version bumped, committed and pushed in `appydave-plugins`.
- fli-core and FliStudio each have a committed, verifying mirror.
- `/Users/davidcruwys/dev/ad/flivideo/docs/agent-comprehension-docs.md`: replace the "Known gap" note with how to run
  step 1 on TypeScript repos; commit and push (repo `/Users/davidcruwys/dev/ad/flivideo`).
- Final message = report: files changed (absolute paths), commits, what the extractor declares / derives / leaves
  unresolved on each pilot (counts), and what you could not handle.

## Out of scope

- Do not run the mirror on FliHub, FliCut, FliCast or Teletubby — that is the next step, after David sees the pilots.
- Do not change any application code in the Fli repos. Refactor findings go in the report.
- Do not touch the renderer or verifier with stack-specific branches (if needed, the IR is missing a field — say so).
