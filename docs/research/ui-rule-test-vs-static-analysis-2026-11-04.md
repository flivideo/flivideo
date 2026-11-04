# Should "no inline key-hint text" be a test or a static-analysis rule?

**Purpose**: Picks the enforcement mechanism for UI rules like "keyboard shortcuts live in tooltips and the ? sheet,
never as inline text beside a control". Research and recommendation; nothing built.

**For Agents**:
- Read before writing any guard for a UI rule. The help-system brief (`docs/briefs/fli-help-system-2026-11-04.md` §3)
  deliberately did **not** add a guard test, pending this.
- Owner `flivideo-orch`. Written by the M2 research worker, 2026-11-04.

## 1 · Verdict

**Make it a static-analysis rule (an ESLint rule on JSX), run in the existing `npm run lint` and so in pre-commit and
CI. Keep one small unit test per rule, but only to test the rule itself.** Do not add per-screen "no hint text" tests.

Why in one line: the offence is a *string in source*, found at the moment it is typed, with no app running; a test only
finds it after the screen renders, and (as the evidence below shows) tests in this repo have ended up defending the
offence.

## 2 · The evidence this decision rests on

| Fact | Where |
|---|---|
| The hint "J slower · K 1x · L faster" is still rendered as text in two live places | `flistudio/client/src/components/Viewer.tsx:394` (a string inside a ternary in JSX) and `modules/storypilot/client/Listen.tsx:453` (JSX text) |
| **Tests assert the offending text**, so the suite is green while the rule is broken | `Viewer.test.tsx:195, 231` and `modules/storypilot/client/screen.test.ts:908` check the hint's `textContent` |
| The Reader got fixed (`5b9324e`, 2026-11-03) and the sibling Listen control kept the pattern | `git show 5b9324e`: touched `StoryPilot.tsx` and one test only |
| Each fix was local to the surface that was complained about | FliCut Help, Viewer, Reader: three fixes, no shared check |

A per-screen test cannot catch the fourth instance because nobody has written the fourth screen's test yet. A lint rule
sees every `.tsx` file whether or not a test exists for it.

## 3 · What each approach catches

| | Static-analysis rule (ESLint/Oxlint on JSX) | Unit test (jsdom render) | E2E test (real browser) |
|---|---|---|---|
| Finds a hint typed as JSX text or a string in JSX | Yes, in any file, rendered or not | Only on screens that have a test and reach that state | Only on screens a spec visits |
| Finds a hint behind a condition (`marks ? … : …`, like `Viewer.tsx:394`) | Yes: it inspects every string literal under JSX | Only if the test sets the condition | Only if the spec does |
| Finds a hint built at runtime (a template string assembled from data; no live example found) | Partly: sees the template pieces, not the data | Yes, if rendered | Yes, if rendered |
| Knows a hint is in `title`/`aria-label` (allowed) vs visible (not) | Yes: attribute vs child is explicit in the AST | Yes via `getByTitle` vs text, but easy to mis-assert | Same |
| Finds visual problems (hint drawn in an image or canvas) | No | No | Screenshot only |
| Can be defeated by | A string assembled in a helper outside JSX; an exemption comment | A test that is never written | A spec that is never written |

## 4 · Where it runs, cost, false positives

| | Rule (lint) | Unit test | E2E |
|---|---|---|---|
| Runs | Editor, pre-commit (`lint-staged` is already in `flistudio/package.json`), CI via `npm run lint` | `npm test`, CI | `npm run test:e2e`, slower, not pre-commit |
| Feedback time | Seconds, at the edit | Tens of seconds | Minutes |
| Build cost | One rule (~60 lines) plus a rule test; reused in every app that shares the config | One test per screen, forever | One spec per screen |
| Maintenance | One place: the regex/token list and the allow-list | Per screen, and tests get re-pointed when copy changes (as the help-system brief has to do now) | Same, heavier |
| False positives | Yes, tunable (see below) | Rare, but false negatives are the real risk | Rare |

**False positives to design for.** I ran a naive regex (a key letter next to a verb) over the FliVideo apps to see how
bad it is: it matched `const [open, setOpen] = useState`, `press Sync now`, and comments, and it missed the real hint at
`Viewer.tsx:394`, which sits in a ternary. That is exactly why it must be an AST rule, not a grep:

- Look only at **JSXText** and **string literals that are children of a JSXExpressionContainer** (including inside
  conditionals and template literals), never at attributes, imports, comments or hook code.
- A "hint" = a key token (`[A-Z]`, `⌘ ⇧ ⌥ ⌃`, `Esc`, `Enter`, `Space`, `←→↑↓`, `[ ]`) next to an action word, usually
  joined by `·`, `:` or `=`. Start narrow (the `X verb · Y verb` shape and "press X") and widen only when a real miss
  appears.
- **Allow** `title`, `aria-label`, `aria-keyshortcuts`; the shared help data and the ? sheet component (path allow-list);
  `*.test.*`. Prose like "Click here or press Esc to stop" (a notice telling the user what to do *now*) is arguably
  legitimate; the brief's rule is about hints **beside a control**, so start by flagging only **inside the control's
  own JSX subtree or its immediate siblings**, and log the rest at `warn` for one review before promoting.

Expected noise after tuning: the `Esc to stop` style notices are the main gray area. Decide them once, in the rule's
allow-list, not per file.

## 5 · How it ties to the Spaghetti Rig static-analyzer work

Sources read: brain notes `2026-10-17-anti-slop-spaghetti-busters-static-analysis-ladder.md` and
`…-omer-static-analyzers-enforce-code-quality.md`; `~/dev/appyrigs/runs/spaghetti/appyrig/decisions.md` and
`~/dev/appyrigs/rigs/DESIGN-RULES.md`. (The Gate Ladder artifact is listed in `d19-spaghetti-rig/fli.resources.json` on
the M4; I did not open the published page.)

- **Same shape as Omer's gates.** His premise: "don't argue with agents in prompts — make the build fail". anti-slop
  already is "ban the lie in the syntax tree", one rule per pattern, with **agent-actionable messages**. Our rule
  should follow that: the error text says "move the key into `title`/`aria-label` and the ? sheet; see brand
  SKILL.md", so the agent that trips it fixes it correctly.
- **Method to copy** (ladder "method" section): calibrate on the real code first (count today's offenders; there are
  at least two), pick the strictest setting whose findings are genuinely worth fixing, no suppressions or baselines,
  and prove the gate catches the real thing with a **probe fixture** (a file that must fail). Our rule needs three
  probes: JSX text, ternary string, template literal. All three must fail; `title=` must pass.
- **False positives teach agents to work around a rule.** anti-slop's weeks of precision work after v1 is the warning.
  Budget for it rather than shipping a noisy rule.
- **Severity trap.** The AppyStack run found a gate that "survived the proof test" while set to `warn` (decisions
  2026-11-01, G05 withdraw-to-fix). Probe the rule with severity `error` and assert a nonzero exit.
- **Where it belongs on the ladder.** It is a **project-lint** gate (step 3 in Omer's order: Oxlint + custom rules),
  not an architecture gate. Local, fast and cheap. The AppyStack/AppyTron gate work is the natural home for the rule
  once the pattern generalizes: a `fli-ui` ESLint plugin in `@flivideo/core`'s tooling, applied by the template's
  `eslint.config.js`.
- **Cost reality check.** Spaghetti on AppyRig took 136 PRs in 7 days, including a rig. A *single JSX rule* does not
  need a rig to build; it needs one commit, one probe test, one allow-list.

## 6 · What still needs a test

Two things a lint rule cannot do, so keep them as tests:

1. The **rule's own tests** (valid/invalid snippets, the probes above).
2. The **positive** half: "the key IS in the tooltip and the ? sheet" for a given control. That asserts presence of the
   replacement (the help-system brief's re-pointed tests do this), and is a legitimate unit test.

## 7 · Recommendation and what would change it

Recommend **the ESLint JSX rule, plus its own tests**. Order of work: count current offenders, write the rule at `warn`
with the three probes, fix the two live offenders, promote to `error`, document in the brand skill.

Would prove this wrong:
- The rule's false-positive rate stays high after one tuning round (more than a handful of allow-list entries): then a
  rendered-DOM test over a few canonical screens is the better net.
- A fourth instance appears that the rule cannot see (string assembled outside JSX, or an image): then add the runtime
  DOM check as a second net, not instead.
- Hints turn out to be allowed in some contexts David actually wants (a notice like "press Esc to stop" beside a
  control): then the rule is too blunt and the policy needs to be written more narrowly before any tool is.
