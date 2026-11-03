---
created: 2026-11-03
timestamp: 2026-11-03T21:05+07:00
---
# Brief: Story Pilot — story.templates.set/list agent-drivable (2026-11-03)

**From:** `flivideo-orch`. **To:** `templates-dev` (**M2**). Report to `flivideo-orch`.
**Ruling:** David via `flivideo-roamy`, ~21:00: story instructions must be agent-drivable; `story.templates.set` being human-only is
"a gap in the API interface". **Machine: M2** — code, standing ruling.

## Setup
Worktree off origin/main: `git -C ~/dev/ad/flivideo/flistudio fetch origin && git -C ~/dev/ad/flivideo/flistudio worktree add ~/dev/ad/flivideo/flistudio-worktrees/templates-agent -b templates-agent origin/main`; `npm install`; `npm run build -w extension-core` before vitest.
**Parallel work:** `storypilot-w1-dev` is changing `modules/storypilot` on branch `storypilot-w1` (islands, source read, CL card).
Keep your diff minimal and confined to the templates verbs, their contract entries and tests, so whichever merges second rebases
cleanly. Don't touch the source-read / island code.

## Do
1. Open `story.templates.set` and `story.templates.list` to agent callers, stamped with who (`changed.by: "agent:<name>"`), exactly
   the way `story.settings.set` does it (find and mirror that pattern: humanOnly flag, contract entry, stamp). Keep the human UI
   unchanged. If there's no way to unhide/hide the shipped default templates, add one (a `hidden` toggle on set, or a small verb),
   stamped the same way.
2. Document the verb in the `flivideo:storypilot` skill:
   `/Users/davidcruwys/dev/ad/appydave-plugins/flivideo/skills/storypilot/SKILL.md` — when to set **Global** vs **Brand**, the
   exact call shape, and that each change is stamped. Bump the flivideo plugin version
   (`/Users/davidcruwys/dev/ad/appydave-plugins/flivideo/.claude-plugin/plugin.json`). `git pull` appydave-plugins first;
   commit only those two files there; push.
3. Tests: an agent set → list → hide → unhide round trip; the stamp is recorded; update W0's template characterization tests in
   `modules/storypilot/server/characterization.test.ts` where they pinned "human-only" (flip, with a comment naming this ruling).

## Gate
storypilot module suite + typecheck + the storypilot e2e specs (`npm run build` first; `e2e/storypilot-reader.spec.ts` and any
other `e2e/storypilot*.spec.ts`). Push branch `templates-agent`; STOP and report: shas (flistudio + appydave-plugins), test counts
before → after, and the **exact JSON-RPC call** an agent uses to set a Global and a Brand template (method, params). Orch re-gates
on the M4, merges, restarts.
