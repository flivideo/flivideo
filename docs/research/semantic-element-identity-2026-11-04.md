# Semantic element identity: how every meaningful element says what it is

**Purpose**: Decides how elements in a Fli app get an identity an AI can read without David explaining it. Serves the
field tester (⌘⇧ notes) and element chat. Research and recommendation only; nothing built.

**For Agents**:
- Read before specifying "select an element", the element payload (`docs/element-chat-kickoff-2026-11-04.md` §4) or any
  new `data-note-target`.
- Owner `flivideo-orch`. Written by the M2 research worker, 2026-11-04. Go: David.

## 1 · The problem

The picker can only select what someone hand-tagged with `data-note-target`. Two things follow.

**Coverage is tiny.** Across the apps, `data-note-target` appears in a limited set of places (FliCut: player, words, cuts,
segments, recordings; FliStudio: launch pieces, resources, Story Pilot). Anything else resolves to its nearest tagged
ancestor, or to nothing.

**Story Pilot's targets are all the same thing.** Every target in the screen is `story-script:<project>/<video>`
(`modules/storypilot/client/StoryPilot.tsx:268, 598`), and the only thing telling them apart is a free-text region
string: `paragraph 2`, `script section`, `story section`, `side rail`, `side <part> <tab>`. So "the whole script" is
always the target, and a single source, chapter or paragraph cannot be picked. The agent receiving the note has to guess
which paragraph from the label and the 500 characters of text.

What already works, and should be kept:

| Piece | Where | Note |
|---|---|---|
| `entityType:entityId` grammar, id may hold colons | `flistudio/client/src/components/noteGesture.ts:11`, FliCut `notes-target.ts` | Same grammar in both apps |
| Label fallback chain: `data-note-label` → `aria-label` → first 80 chars of text | `noteGesture.ts:144` | aria-label is already a fallback |
| `data-note-field`, `-region`, `-project`, `-video` | same | Region is the weak point |
| FliCut's finer types: `word:<take>#<i>`, `cut:<id>`, `segment:<id>`, `recording:<name>` | `flicut/src/renderer/src/Script.tsx`, `Timeline.tsx` | The model to copy: the id points at data, not at a place on screen |

**David's bar** (brief, 2026-11-04): every practically meaningful element has semantic identity, so the AI knows what it
is without being told. Anything with visible content, headings included; not padding divs. Identity = what it is, the
data it shows, and ideally where it lives in the code.

## 2 · The lost discussion

**Not found.** Searched David's own turns in session transcripts for aria-label, semantic tagging / ids / labels,
accessibility labels:

| Where | Scope | Result |
|---|---|---|
| M2 | 6,371 transcript files in `~/.claude/projects/` (grepped in place) | 12 hits in user turns. Ten are a pasted meetup summary ("extensive semantic tagging" of notes). The rest are two copies of one dictated turn, 2026-10-18T12:47Z: "we need to get better names for all of these … a semantic label attached to each of them clearly as well" — about naming plugin paths 1–4, not UI elements. **No aria-label / element-identity turn.** |
| M4 (over ssh) | the aria/semantic pattern over all projects (I read only the last 14 hits of that run, so treat it as partly checked); and the 170 FliVideo-project files with a wider pattern (`aria`, `every element`, `semantic`, `element identity`), read in full | No matching David turn in what I read. Hits were agent text (summaries mentioning `aria-current`, "ARIA fixes") and one orch relay of David's 2026-11-03 key-hint ruling, which is a different subject |
| Roamy | not checked (offline). Roamy's own note in the brief: 45 days, first 30 files, no matching turn | Unchecked beyond that |
| `flivideo/docs` | grep for aria-label / semantic | Only incidental uses (chip ⊕/⊖ labels, the help-system brief) |

What this does **not** establish: that the conversation never happened. It may have been voice-dictated with different
words ("name tags", "labels on things"), live in a Roamy session, or sit in a file not matched by my patterns. A third
pattern pass on M2 (`data-note`, `every element`, …) timed out and was stopped, so it is incomplete. If David
remembers a keyword or a rough date, a targeted search is cheap.

## 3 · Options

| # | Option | Gives | Coverage | Cost | Weakness |
|---|---|---|---|---|---|
| A | Plain `id` | A unique handle | Whatever is hand-set | Low | Says nothing about what or why. Collides in lists. Not set by React by habit |
| B | Extend `data-note-*` (add `kind`, `of`, a data ref) | What it is **and** the data it shows | Hand-placed, grows slowly | Low per element | Easy to forget. Today's problem repeated at a finer grain |
| C | aria roles and labels | Role (`heading`, `button`, `listitem`) and a human name; also improves accessibility | Medium; headings and controls already tend to have them | Low | Labels are words, not data refs. Roles are coarse (a paragraph has no role). Duplicates `data-note-label` |
| D | Build-time source map (a Babel/Vite plugin stamping `data-src="Listen.tsx:441 <SpeedControl>"` on every JSX element in dev builds) | Component name and file:line, for every element, with no hand work | Total | Medium (one plugin per app; dev builds only) | Says where, not what data. Verify it works with the React version in use: newer React dropped its own `_debugSource`, so the stamp has to come from the plugin, not React |
| E | Mix (recommended below) | All three answers | Total for "where", hand-tagged for "what data" | Medium | Needs a coverage check, or the hand-tagged layer decays |

## 4 · Recommendation: E, in three layers, with a coverage check

Identity has three questions; use the cheapest tool for each.

1. **What data it shows: hierarchical `data-note-target`, extended.**
   - Keep the grammar `type:id`. Add `data-note-kind` (`paragraph`, `chapter`, `source`, `heading`, `card`, `control`).
   - Make identity **nest**: each level tags itself, and the picker builds the path by walking ancestors. Story Pilot
     becomes `story-script:<p>/<v>` › `story-chapter:<p>/<v>#2` › `story-paragraph:<p>/<v>#2.3`, and
     `story-source:<id>` for a card. This replaces the free-text `region` string, which is the actual cause of "can't
     pick a paragraph".
   - The id points at data (as FliCut's `word:<take>#<i>` already does), never at a screen position.
2. **What it is, in words: aria first.** Do not hand-write `data-note-label` where an accessible name or role exists.
   Derive the label as `data-note-label` → `aria-label` → role + heading text → text. This is the existing chain with
   one more step. Headings get identity for free from `<h1–h6>` plus their text.
3. **Where it lives in code: build-time `data-src`, dev builds only.** One plugin in the AppyStack/AppyTron template,
   stripped from production. It covers every element with no discipline needed, which is the part hand-tagging can't.

**Keep it honest with a coverage check.** An e2e test walks the rendered DOM; every element with its own visible text,
every heading and every interactive element must resolve to an identity (own or nearest ancestor with `kind`), and it
fails with the list of misses. Padding divs have no text of their own, so they are exempt by construction. The test
also fits `ui-rule-test-vs-static-analysis-2026-11-04.md`: it needs a rendered page, so it is a test, not a lint rule.

**Payload to element chat** (matches kick-off §4): `app`, `screen/url`, `path[]` of `{type,id,kind}`, `label`, `words`
(capped), `src` (dev only). Both the field tester and element chat read the same payload.

**First slice**: Story Pilot only (paragraph, chapter, source card, headings), plus the coverage test on that screen.
Existing notes keep working because the old `story-script:` target stays the root of the path.

## 5 · What would prove this wrong

- The coverage test fails constantly on new screens and people silence it: then identity needs to be generated (option
  D extended to data refs through typed components), not tagged.
- `data-src` doesn't survive the Vite/Electron build, or its noise slows the DOM: fall back to B + C.
- Agents on the other end of the note ignore `path[]` and still guess from text: then the payload isn't the problem and
  this work isn't worth the attribute weight.

**Open for David**: whether the `data-note-*` prefix should become `data-el-*` once it serves element chat as well as
notes. Recommendation: rename only if the field tester's notes log can be migrated; otherwise keep the prefix and
alias.
