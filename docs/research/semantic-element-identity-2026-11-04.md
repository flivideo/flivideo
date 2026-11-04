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

**Found (correction by flivideo-roamy, 2026-11-04).** It's in `flivideo-orch`'s own transcript on the M4
(`~/.claude/projects/-Users-davidcruwys-dev-ad-brains/f73fd5e0-e8b2-40ea-a51a-c97dd7efe8db.jsonl`), David's turn at
**2026-11-03T03:49:03Z (10:49 +07)**. The search below missed it because the session lives under the *brains* project
folder, not FliVideo's. David, verbatim:

> "what is available for us to know on a page? There are only three things that I can think of:
> 1. An actual DOM path
> 2. When Field Tester is annotating the page, it's added some information because Field Tester only allows you to select
>    certain elements on the page anyway. It's gone through and done something and probably written labels at the same time.
> 3. Or every element on the page should potentially get some sort of ARIA Am I saying that right, or semantic title,
>    semantic description, or something like that?
>
> Because if we did the third type and it was just something we did as almost a hook, you can't even write the page unless
> you annotate correctly. This is where the spaghetti rig got involved and used static analysis… 'Are all your elements
> actually made readable for, say, blind viewers…' …then you could provide both a DOM path and a semantic description. The
> pros, the conversation needs more the semantic description, but knowing where it is is also important.
>
> And then we'd be able to improve the selector because currently, when you do selection, there's a very limited number of
> boxes that appear… it feels like something is missing.
>
> I just want this to be thought of as a backlog or just notes around Field Tester in general"

Orch's reply (03:49:46Z) recommended:
- send all three with every point: the ARIA name, the hand-placed label and the DOM path;
- make ARIA naming a gate, as the Spaghetti rig did;
- add a "point at anything" selector mode that falls back to the nearest named element.

A worker then checked Anthropic's docs: what a click on an element sends isn't documented. That was banked in
`docs/briefs/field-tester-pointing-notes-2026-11-03.md` (9d5b3aa). **The recommendation below should be re-checked
against David's three-way framing.**

The original search, for the record:

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

## 6 · Re-check against David's three ways (flivideo-orch, 2026-11-04)

Checked §4 against David's 2026-11-03 10:49 framing and orch's 10:49 reply. Verdict: **§4 holds, with three amendments.**

| David's way (10:49) | Orch reply (10:49) | §4 as written | Amendment |
|---|---|---|---|
| 1 · DOM path ("knowing where it is is also important") | send it with every point | **Missing.** `path[]` is a data-identity path; `data-src` is a code location (dev only). Neither is the DOM path | Add `domPath` (a stable CSS path, computed by the picker at click time) to the payload. Cheap, works in production builds, and lets an agent re-find the element |
| 2 · Field Tester's hand labels | send it | ✅ `data-note-target`, extended and nested | none |
| 3 · ARIA / semantic name on every element, enforced "as a hook… you can't even write the page unless you annotate" (the Spaghetti-rig static-analysis framing) | make ARIA naming a gate | ⚠️ aria is used as a label source, and the gate is a **rendered e2e coverage test** only | Gate at write time too: a JSX lint rule (jsx-a11y-style accessible-name on interactive elements and headings) at `warn` → `error`, matching `ui-rule-test-vs-static-analysis-2026-11-04.md` §7. Keep the rendered coverage test for what lint can't see (text nodes, nesting). Lint first, test second |
| "the selector… a very limited number of boxes" | add a "point at anything" mode that falls back to the nearest named element | **Missing.** Nesting makes more things *named*, not more things *pickable* | Add a "point at anything" picker mode: any element under the cursor is selectable; it reports its own identity or the nearest ancestor's, plus `domPath` |

**Payload, amended:** `app`, `screen/url`, `path[]` of `{type,id,kind}`, `label` (aria-derived), `domPath`, `words` (capped),
`src` (dev only). **First slice, amended:** Story Pilot nested targets + the point-at-anything mode + the lint rule at `warn`;
the coverage test follows.

Still David's: the prefix rename (above), and whether ARIA-on-every-element is a hard gate (`error`) or advisory (`warn`).
