# A recurring UI mistake: stop it with a skill or an OpenRig rig?

**Purpose**: Decides what should stop a mistake that keeps coming back (the running case: inline key-hint text beside
controls). David leans to rigs as the long-term fix. This tests that lean against the evidence. Research only.

**For Agents**:
- Read with `ui-rule-test-vs-static-analysis-2026-11-04.md` (the gate this note leans on).
- Owner `flivideo-orch`. Written by the M2 research worker, 2026-11-04.

## 1 · Verdict

**Neither a skill nor a rig is what stops it. A gate stops it** (the lint rule in the companion note). The question
then becomes who *puts the rule in the gate* and who *notices the next recurring mistake*. For that, **David's lean is
right: a rig is the right long-term home, but for the learning loop, not as the thing that stops each mistake.**

| Job | Best tool |
|---|---|
| Stop the mistake at the moment it is typed | Lint rule in `npm run lint` (deterministic, no agent needed) |
| Tell a builder the rule exists and why | Skill / CLAUDE.md line (cheap, passive) |
| Notice that a mistake has recurred, and turn it into a gate | A rig: the transcript-mining loop that already exists in `appyrigs` |

## 2 · The history (what a skill-style fix has done so far)

| When | What | Fixed where | Came back |
|---|---|---|---|
| 2026-09-24 | FliCut Help: key text beside controls (per the brief; FliCut's help work is `58c5698`, 09-27) | FliCut only | Yes |
| 2026-10-05 | Viewer: J/K/L added with an inline "J slower · K 1x · L faster" (`360a942`) | FliStudio Viewer | Still present: `Viewer.tsx:394` |
| 2026-11-03 | Reader hint text moved to title/aria-label (`5b9324e`) after David: "that belongs on the buttons" | Reader only | Sibling Listen control still has it: `Listen.tsx:453` |
| 2026-11-04 | David's complaint again; the help-system brief writes the rule into brand `SKILL.md` and `flistudio/CLAUDE.md` | Prose rules | Open |

Three things stand out:

1. **Every fix was local to the surface complained about.** The learning stayed in a commit message.
2. **Tests defended the mistake.** `Viewer.test.tsx:195,231` and `screen.test.ts:908` assert the hint text, so a green
   suite said "fine". A rule given to agents as prose can't override a test that says the opposite.
3. **The rule has just now been written down for builders** (the brief). Until then no artifact anywhere said it, so
   "skill vs rig" has not actually been tried: nothing has yet failed *despite* a skill.

Wider evidence from this repo's own history: in `~/dev/appyrigs/LEARNED.md` and the spaghetti `decisions.md`, the
lessons that stuck became **gates** (e.g. "mutate rule SEVERITY on every gate" after a `warn` gate passed its own proof
test). I did not measure how often prose notes recur. I did not find memory-folder evidence for key hints specifically; the
`~/.claude/projects/-Users-davidcruwys-dev-ad-brains/memory` folder has no file matching hint/tooltip.

## 3 · Skill vs rig, compared

| | Skill (or CLAUDE.md rule) | OpenRig rig | Gate (lint rule) |
|---|---|---|---|
| **When it fires** | When an agent loads it. Brand `SKILL.md` is not always loaded; David has said this recurs for artifact brand rules (global preferences, "artifacts" section) | When someone starts the rig / hands it work. Fires on a schedule or ticket, not on a keystroke | Every edit, every commit, every CI run, for human or agent |
| **Who maintains it** | David or any agent editing a file; cheap | The rig's lead agent, plus David for rulings; the spaghetti run needed an outside driver and a judge | Whoever owns the config; changes are code review |
| **How it learns** | Only when a person edits the text. Does not notice recurrences | Can: `transcript-mine` mines all session logs into a shortlist of "preference rules to prune/add, skill candidates" (live on Roamy, `appyrigs/README.md`) | Learns only by being edited, but never forgets |
| **Cost** | Near zero to write; a few hundred tokens per load | High. Spaghetti: 136 PRs in 7 days, orchestrators outside the rig, a judge bottleneck, refresh failures (`DESIGN-RULES.md`) | One rule plus probes |
| **Failure mode** | Silent: an agent that never loads it breaks the rule and nothing flags it | Slow and expensive for a one-rule problem; stalls at tier boundaries waiting for a go | False positives; defeated by code outside the pattern |
| **Evidence it works here** | The key-hint rule has not yet been tested in skill form | Rigs built the AppyStack/AppyTron gates, but those were large, multi-gate jobs | Gates are what stuck in the spaghetti run |

## 4 · Why "rig" is still the right long-term bet (for a narrower job)

David's instinct is a good one if the rig's job is **"own recurring UI mistakes"**, not "be the guard". Concretely, a
small rig (or a mode of `transcript-mine`) that:

1. Reads session logs and `git log` for repeated corrections of the same shape (David's "that belongs on the buttons",
   "back three times").
2. Proposes the rule: a candidate lint rule plus probe fixtures plus the one-line skill text, as a PR for David.
3. Is gated like the spaghetti rig: calibrate on real code, probe, no baselines.

That uses what rigs are actually good at (long-running, multi-agent, remembers across sessions) and keeps the
enforcement itself deterministic and free. It also answers "how does it learn?": the rig is the learner, the gate is the
memory.

The thing to avoid: building a rig whose agents *re-check every PR for hint text by reading it*. That is slower and less
reliable than the lint rule, and burns context on every PR (the spaghetti run measured 327k-token seats and a judge
taking 50–90 minutes per PR).

## 5 · Recommendation

1. **Now (cheap, this week):** the lint rule (companion note), the skill/CLAUDE.md line (already in the help-system
   brief), and re-pointing the three tests. This stops the mistake.
2. **Later (the rig lean):** extend `transcript-mine` or a small sibling so a repeated correction produces a *proposed
   gate*, not just a preference-rule shortlist. First test: ask it, retroactively, whether it would have flagged key
   hints after the second occurrence.
3. **Don't** build a dedicated rig for this one mistake.

## 6 · What would prove the recommendation wrong

- **A fourth key-hint instance gets past the lint rule** because the pattern is more varied than JSX text (images, text
  from data). Then the gate is not enough and a review agent in a rig earns its cost.
- **The mining loop produces proposals nobody merges**, or its false-positive rate matches the noise it replaces. Then
  the rig is cost without learning and a plain checklist skill is better.
- **A skill-only attempt works** for a quarter without a recurrence. I could not test this: the rule has only just been
  written. If it holds, the gate is insurance, not necessity.
- **Mistakes of other kinds don't reduce to a lint rule** (layout, taste, copy tone). Those need judgement, which is the
  case where a rig or review agent is the right tool and this recommendation does not apply.

## 7 · What this does not establish

I read the rig's docs and run notes, not its internals, and did not run anything. The 136-PR figure and orchestrator
issues are from `DESIGN-RULES.md` and describe a much bigger job than this one; I am inferring that a small rig costs
less, not measuring it. "FliCut Help 2026-09-24" is taken from the brief; I did not locate that specific commit.
