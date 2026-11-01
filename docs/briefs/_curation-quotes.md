## David's words, verbatim (2026-11-01)

- "if you present me with 19 boxes like this, it's not much better when you just show me 6 boxes… I'm overloaded… I don't know what I can use. I don't know what the linear order is."
- "Did they come in automatic, synthesised, or are they often just raw and then they become synthesised later?"
- "if I ask for it to be synthesised, but it's an ongoing conversation, how do I know the synthesis is now stale?"
- The goal: "so that I don't actually have to go in and read those things, but know that they're going to be placed properly, know that they're up to date, know that they're refreshable."

## Context (checked by orch)

- D13 `/Users/davidcruwys/dev/video-projects/v-appydave/d13-overlay-pilot`: 9 attached, 8 placed in story sections (`script/storypilot/project/story.json` → sources[].role: why 2, what-happened 5, how-to-tell 1).
- D18 `/Users/davidcruwys/dev/video-projects/v-appydave/d18-story-pilot`: 20 attached (`fli.resources.json`), no story.json at all, so nothing placed; the screen shows them as the "not placed" set.
- Story Pilot design docs: `/Users/davidcruwys/dev/ad/flivideo/docs/specs/resources-model-2026-11-01.md`, `/Users/davidcruwys/dev/ad/flivideo/docs/specs/storypilot-listen-2026-11-01.md`; code `/Users/davidcruwys/dev/ad/flivideo/flistudio/modules/storypilot/`.

## Rules for both workers

READ-ONLY. You write exactly one doc (path below), commit + push it in the flivideo repo, then report to `flivideo-orch` by name and stop. No skill creation, no code, no edits to sessions/captures/projects. The machine is overloaded (load ~28/10 cores, swap 14/15 GB): no parallel agent fan-outs, no full test suites, keep processes light. Report every claim you could not verify.
