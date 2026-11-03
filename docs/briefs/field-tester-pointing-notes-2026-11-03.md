---
created: 2026-11-03
timestamp: 2026-11-03T12:20+07:00
---
# Notes (backlog, not a build order): how Field Tester knows what you pointed at (2026-11-03)

**Status: NOTES — David's thinking aloud, to be weighed later. Applies to Field Tester in general, not only the session box.**
Owner: `flivideo-orch`. Related: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/session-box-spec-2026-11-03.md`.

## David's question (verbatim anchors)
- "David is pointing at angle proposal B, the intro… how does the page know that?"
- Three ways a page can know: "an actual DOM path"; Field Tester's own labels ("only allows you to select certain elements…
  probably written labels"); "every element… some sort of ARIA… semantic title, semantic description".
- "you can't even write the page unless you annotate correctly… almost like a static analysis thing" (as the Spaghetti rig did).
- "currently… a very limited number of boxes appear… it feels like something is missing."
- "How are we distinguishing between the two?" (Field Tester vs the chat/session box.)

## What is true today (checked in code)
- The page knows ONLY layer 2: hand-placed attributes. `client/src/components/noteGesture.ts`: a target is
  `data-note-target="<entityType>:<entityId>"` plus optional `data-note-field`, `data-note-region`, `data-note-label`;
  nearest ancestor wins. That is why only some boxes light up: only elements a developer tagged.
- So "angle proposal B, the intro" is possible only where the proposal carries those attributes. Orch's sentence was the
  target, not something the page sends today by itself.

## The three layers — what each answers
| Layer | Answers | Strength | Weakness |
|---|---|---|---|
| 1 DOM path / selector | WHERE on the page | always there, no work | brittle across renders, meaningless to a reader |
| 2 Domain tag (`data-note-*`) | WHICH THING in our data (story `d13`, proposal `B`, field `intro`) | joins to data/verbs; stable | only where hand-added → the "limited boxes" |
| 3 Accessibility (role + accessible name + description) | WHAT IT IS to a person | universal if enforced; same tree screen readers AND agents/Playwright (`getByRole`) use | needs discipline; says nothing about data ids |

## Orch take (to weigh, not decided)
- Send all three as one bundle per point: name/role (meaning, for the conversation) + domain tag when present (identity,
  for acting) + DOM path (location fallback). The conversation leans on 3, the action leans on 2, 1 rescues the rest.
- Make layer 3 a gate, not a habit: an accessibility lint (`eslint-plugin-jsx-a11y`) at build plus an axe-core check in e2e —
  the Spaghetti-rig move (static analysis that refuses unlabelled interactive elements). Better for blind users, agents and
  Field Tester at once.
- Selector: keep tagged targets as the default; add a "point at anything" mode (e.g. an extra modifier) that falls back to
  the nearest element with an accessible name, so nothing is unpointable.
- Anthropic, checked 2026-11-03 (official docs first): **the docs do not say what a selection sends.**
  - Claude Code desktop docs list only the shortcut "`Cmd Shift S` | Select an element in the Browser"
    (https://code.claude.com/docs/en/desktop).
  - Artifacts Help Center: "highlight the text you want changed, click 'Edit with Claude'… Claude makes the edit where you
    marked it" — docs/markdown text only, payload undocumented (https://support.claude.com/en/articles/9487310).
  - Claude Design: "Inline comments let you click directly on a specific part of the canvas" — payload undocumented
    (https://support.claude.com/en/articles/14604416).
  - Third-party only (azukiazusa.dev, Claude Code Preview): a short tag+class selector (e.g. `<h1>.text-2xl.font-bold`) plus a
    screenshot of the element. Nothing anywhere mentions data attributes or ARIA.
  - To know for sure needs a hands-on devtools/network capture of one selection (David offered view-source). Not done.
  - Implication: nobody documented is doing layers 2+3; our bundle (domain tag + ARIA name + DOM path, plus element text and a
    screenshot crop) is a superset of the only reported approach.

## Naming (David: "I saw you use some word called session")
- **Session** = one Claude Code conversation, running in a terminal (tmux), with a name like `d13-overlaypilot-video`.
- **Field Tester / note** = capture an opinion about the app, kept as a trail (`fli.notes.jsonl`). No one answers.
- **Ask** (proposed name for the session box) = send words to a live session to get work done; it answers.
- Shared by both: **pointing** (the ⌘⇧ gesture) and the **target** bundle above.
