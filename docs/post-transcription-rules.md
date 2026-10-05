---
created: 2026-10-05
status: design for David's review — nothing new built from this yet (robustness brief step 7)
owner: flitools
brief: /Users/davidcruwys/dev/ad/flivideo/docs/briefs/transcription-robustness-2026-10-05.md
---

# Post-transcription rules: fixing real words without letting the model guess

**The problem.** Some mishearings are real words, so the word list alone can't fix them: "school" for Skool, "I" for AI,
"skill"/"school", "69" for 16:9, and spoken project codes ("d 0 six"). Asking the transcriber to fix them (a prompt)
is worse than the disease: on 2026-10-05 the word list sent to CrisperWhisper came back as words and cost up to 30 s of
speech. David: *"should it be a post-review rather than letting the model fix these words … a specific filter that you
run post-transcription … something we need to think through, architect, and build properly."*

**The idea.** A deterministic **rules stage** that runs after the engines are merged and before anything is written for
people (SRT, TXT, captions). Each rule decides **per occurrence**, records its **evidence**, and can be **undone**.

```
engines ─▶ merge + word-level levelling ─▶ RULES STAGE ─▶ best words (JSON) ─▶ SRT / TXT / captions
 (Groq, CrisperWhisper,   (step 5: spine +                 (per occurrence,     (every change kept in
  mlx, Scribe slot)        names, gaps, loops)              evidence, undo)      health.rules, scored)
```

## Where it sits, and what it never touches
- **After** levelling, **before** SRT/TXT, on every engine's output and on recaption (saved JSON). It never runs inside
  a transcriber, and no model is involved.
- **Verbatim JSON words stay recoverable.** A rule's change is a layer: the engine copies in `engines/` are never
  rewritten, and the best file records each change, so undoing a rule means re-rendering without it.

## Rule kinds (one engine for all of them)

| Kind | Fires when | Example | Already built |
|---|---|---|---|
| **pattern** | A fixed, never-changing shape | spoken codes → D06 | ✅ step 4 (`codes.ts`) |
| **name** | A word-list name, or a heardAs of one | "Abhi Dave" → AppyDave | ✅ spelling stage + step 5 |
| **engine vote** | Another engine heard a known name *at the same place* | "I tell the." → AITLDR | ✅ step 5 (levelling) |
| **context** | A real word in a context that makes it a name | "school" → Skool only near "community", "group", "join", "classroom", or where an engine heard "Skool" | ❌ proposed |
| **format** | A spoken format token | "69 format" / "sixteen nine" → 16:9 | ❌ proposed |

A **context** rule is a word-list rule plus a condition: `{ find: "school", write: "Skool", when: { near: [...], within: 6 words } | { vote: true } }`.
"I" → AI is **vote-only**, never a context rule. "I" is the commonest word in English, and only another engine
hearing "AI" at that spot can justify the change.

## Every decision is per occurrence, with evidence
Each change writes one record into the best transcript's `health.rules[]`:
`{ rule, kind, at (seconds), before, after, evidence: { engines: { groq: "AI", crisper: "I" }, context: "... join the school community ..." } }`.
- Nothing is changed without evidence. A context rule with no context match, or a vote rule where no engine heard
  the name, leaves the word alone.
- The scorecard counts changes per rule and kind, so every rule's effect is measured against the baseline (as steps 4
  and 5 were: name misses 17 → 0).

## How a rule is written and reviewed
- **Where rules live:** in the word store, at the same levels as everything else (global → brand → project). That
  means a new `when` on today's `rules` entries, written only through fli-core `changeWordsFile`, as now. A pattern
  rule (codes) is built in, because it's the same everywhere.
- **Two states:** `auto` (applied on every run) and `review` (applied, but listed for David to confirm or reject).
  - New context and format rules start as `review`. Pattern, name and vote rules are `auto`, as they are today.
- **The review surface:** FliStudio's words screen lists `review` decisions with their evidence line. Confirm turns
  the rule `auto`; reject adds an exception (`off` for that occurrence or rule). The decision is David's, never an
  agent's.

## Relation to what exists
- **Step 4 (codes)** is the first pattern rule. **Step 5 (levelling)** is the engine-vote and name stage. Both already
  record their changes (`health.levelled`) and are scored. This stage gives them one home and adds context and
  format rules.
- **Word store levels** stay the single place for names and rules (`shared-data-levels.md`), including future sources
  such as an agent registry.

## Not decided (David)
1. **Who confirms review decisions:** David only, or also an editor per brand.
2. **Context words:** whether they're written per rule by hand, or learnt from confirmed decisions. A learnt list
   would still be deterministic at run time.
3. **Format tokens:** whether "16:9" belongs here, or in FliCut's caption styling.

**Recommendation:** build in this order: format (16:9) and context (Skool) as `review` rules, then the review list in
FliStudio, then promote rules to `auto` as David confirms them.
