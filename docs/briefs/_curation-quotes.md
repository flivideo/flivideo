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

## ANGLE — David, verbatim (2026-11-01 ~13:35). Treat as part of the subject, not a side note.

"One of the things that is generally important with that curation skill you're talking about, whatever we're calling it Is like the bringing together of all the story elements is the angle of the story. I don't know whether there's chicken or egg around angles. I don't know whether you've got to wait till there's information before you do an angle, or you do it early. This actually came out in the work this morning around the AppyStack video, where it had come up with an angle on its own. It came up with three of them, but they were essentially around the idea that spaghetti is stupid. Like spaghetti, the spaghetti rig doesn't add value. I spent a week testing it, but in my mind, the spaghetti rig is a great idea. It's just that we haven't got it to work yet, and the video would be more about our getting it to work: an anti-slop AI system. I don't know whether an angle, or a north star for a video, a direction for a video, is needed to do proper curation, but it's something to consider. Again, I'm using the word curation because I can see it on the screen. You've got the curation research. I don't know whether this is curation or something else."

Both workers: cover the angle question in your doc. sessions-rsch — find how angles/north stars actually got set (or went wrong, e.g. an agent inventing an angle that contradicts David's view, as in the D19/AppyStack case this morning: the D19 session `d19-storypilot-video` and its Story Pilot notes). When did an angle exist before curation vs emerge from it? curation-rsch — which existing skills set, use or respect an angle / north star (e.g. `compass:set-north-star`, Story Pilot's feel/do/audience settings, `writers-room:*`), and whether any of them overrides the human's angle. Also: is "curation" even the right name for this job? Say what you'd call it.
