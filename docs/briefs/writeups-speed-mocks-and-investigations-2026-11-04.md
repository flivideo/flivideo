# Brief: speed-control mocks + three write-ups (no builds)

**Purpose**: One asynchronous M2 worker job: four speed-control mocks, plus three investigation write-ups. Research and
design only.

**For Agents**: Owner `flivideo-orch`, who dispatches this to an **M2** worker (async; it reports back to
`flivideo-orch`). From `flivideo-roamy`. **Go: David, 2026-11-04.** **No code, no builds, no test changes.** Commit and
push everything to `flivideo` main under the paths below.

## A · Speed-control mocks (AppyDave light, `canvas:visual-brief`, load `brand-dave:brand` first)

**David:** ten speed buttons is too many. He's thinking pagination-style: a few visible speeds (3, maybe 5) around the
current one, with previous/next to go further. **One unified control** for four places. Mock each in its real context:

| Place | Today's code |
|---|---|
| Story Pilot Listen | `flistudio/modules/storypilot/client/Listen.tsx` (~:440, ten buttons, 0.25×–4×) |
| FliStudio video Viewer | `flistudio/client/src/components/Viewer.tsx` |
| FliHub playback | `flihub/client/src/components/` (Recording / Incoming video modals) |
| FliCut | `flicut/src/renderer/src/Player.tsx` |

- Show 3-visible and 5-visible variants, the edge states (at 0.25× and at 4×), and how J/K/L map onto it.
- No inline key-hint text: keys go in tooltips and the ? sheet (`docs/briefs/fli-help-system-2026-11-04.md`).
- Pass `check-artifact.mjs`. Publish with the claude-artifacts tool **if it is available on the M2**. If it isn't,
  commit the HTML and tell orch, who publishes from the M4. Source:
  `flivideo/docs/artifacts/speed-control-mocks-2026-11-04.html`. Add a row to `brains/ARTIFACTS.md`. Orch opens it for
  David on the M4.

## B · Semantic element identity → `flivideo/docs/research/semantic-element-identity-2026-11-04.md`

- **Problem:** the field tester can select only a small hand-picked set of targets (`data-note-target`). In Story
  Pilot, all five targets are "the whole script" (`story-script:<project>/<video>`) plus a region label, so a single
  source, chapter or paragraph can't be picked. Element chat needs the same thing.
- **David's bar:** every practically meaningful element has semantic identity, so the AI knows what it is without David
  explaining: anything with visible content, headings included, but not padding divs. Identity = what it is, the data it
  shows, and ideally where it lives in the code.
- **Options to weigh:** id, data attributes (extend `data-note-*`), aria-label / roles, a mix, or a build-time source map
  (component name and file).
- **Find the lost discussion:** an earlier aria-label / semantic-tagging conversation with David. Search M4 and M2
  transcripts (`~/.claude/projects/**.jsonl`, David's own turns) and `flivideo/docs`. Roamy may be offline: say so if it
  can't be checked. Quote David with timestamps, or say plainly that it wasn't found.
  - Roamy (2026-11-04 07:40 +07): scanned transcripts from the last 45 days that mention aria-label / semantic tagging (first 30 files); **none had a matching David turn**. The hits were agent text only. Roamy is otherwise unchecked.
- **Output:** problem, options table, recommendation. It serves both the field tester and element chat
  (`docs/element-chat-kickoff-2026-11-04.md`).

## C · Test or static analysis? → `flivideo/docs/research/ui-rule-test-vs-static-analysis-2026-11-04.md`

- **Question:** should "no inline key-hint text" (and rules like it) be a unit/e2e test or a static-analysis rule?
- **Tie it to the Spaghetti Rig static-analyzer work** (v-appydave `d19-spaghetti-rig`; its `fli.resources.json` on the M4
  lists, among others:
  - the brain notes `brains/ai-meetups/ai-engineers/2026-10-17-anti-slop-spaghetti-busters-static-analysis-ladder.md`
    and `…-omer-static-analyzers-enforce-code-quality.md`;
  - the Gate Ladder artifact;
  - `appyrigs/runs/spaghetti/appyrig/decisions.md`.)
- Cover: what each catches, where it runs (pre-commit / CI / rig gate), cost, and false positives. Recommend one.

## D · Skill or rig? → `flivideo/docs/research/recurring-ui-mistake-skill-vs-rig-2026-11-04.md`

- **Question:** is a recurring UI mistake (like the key hints, back three times) better stopped by a skill or by an
  OpenRig rig? David leans to rigs as the long-term fix.
- Use the key-hint history:
  - FliCut Help 2026-09-24;
  - Viewer 2026-10-05;
  - `5b9324e` 2026-11-03;
  - David's 2026-11-04 complaint.
- Also use `~/.claude/projects/-Users-davidcruwys-dev-ad-brains/memory`-style evidence where reachable, and the
  `openrig` / `appyrigs` brains.
- Compare when each fires, who maintains it, and how it learns. Recommend, and say what would prove the recommendation
  wrong.

## Report

To `flivideo-orch`: the artifact URL (or "needs publishing"), the four commits, and one line per write-up with its
recommendation.
