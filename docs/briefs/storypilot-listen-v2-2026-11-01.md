---
created: 2026-11-01
timestamp: 2026-11-01T20:25+07:00
---
# Brief: Story Pilot Listen v2 — word highlight, speed, edit-in-place with live regenerate (2026-11-01)

**From:** `flivideo-orch`. **To:** `storypilot-dev`. **Order: AFTER Prep Unit 1 is reported and acked, BEFORE Prep Unit 2.**
Branch: new `listen-v2` from whatever main is when you start (orch will have merged prep-v1).

## David, verbatim (2026-11-01 ~20:20)
"When we're playing a video, you can see yellow highlights of the word that we're on. You can also play it at any speed:
2x, 3x, whatever. The same sort of patterns we see should exist… I do like that there are sections. That's pretty cool…
I really do need to be able to edit the words. If so, let's not do the pop-up modal dialogue. That was a mistake of mine,
but the speed settings are needed, the ability to edit, and if we do edit a section, having it regenerate dynamically
would be important."

## Build
1. **Word highlight**: the word being spoken gets the same yellow highlight FliStudio/FliHub use when playing a video with
   its transcript. Find that existing video transcript highlighter and reuse its component/styles; do not build a second one.
   Timings come from FliTools `speech.synthesize` `words[]` (flitools-dev is adding them on branch `speech-words`;
   orch will tell you when it is live, and the shape). Click a word = seek there (as the video player does, if it does).
2. **Speed**: same speed control as the video player (1x … 2x, 3x), remembered per user like the video one.
3. **Edit in place**: each section/paragraph is editable inline in Listen (no modal, no pop-up). Saving writes back to the
   story script through the existing story verbs. David's edit is David's (the Prep "never rewrite the script" rule is for
   the skill, not him).
4. **Live regenerate**: an edited paragraph goes stale by its hash (you already have this), regenerates automatically after
   save (debounced), shows a small "regenerating" state on that paragraph only, and playback picks up the new audio.
5. Keep the sections; keep the play bar, auto-next. UX pass as you go.

## Gates
typecheck, lint, `npm test`, targeted e2e (highlight advances, speed change, edit → regenerate → new audio plays; mock
FliTools in e2e). Do not run the full suite. Commit, push `listen-v2`. Do not merge or restart FliStudio. Report to orch.
