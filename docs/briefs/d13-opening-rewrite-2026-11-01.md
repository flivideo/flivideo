# Brief: D13 — rewrite the opening as a story writer, not a paste — 2026-11-01

**From:** Roamy session `flivideo-field-trial-plan`. **Go:** David, 2026-11-01 ~07:30 +07: "Go on both… Okay, I like option A."
**Run on:** the M4. **Use:** the `flivideo:storypilot` skill (story.brief first). David will narrate this today.

## The job

David gave an **instruction**, not replacement text. Yesterday his words were pasted in almost verbatim as line 1 and the
rest left alone, so paragraph 2 now repeats the opening. Undo that mistake properly:

1. `story.brief {brand:"appydave", project:"d13"}`; read the creator voice docs (`settings.voiceDocs`) and the sources
   the skill tells you to.
2. **Rewrite the opening (chapter 1, ¶1–¶5)** in David's voice, carrying this intent:
   - *His point:* Joy is not a content creator, she's a self-employed nail artist who has to promote her business on
     social media. Turns out she's naturally really good at it: one-shot videos, 45–90 seconds, full of life,
     knows her topic. But her videos don't get published, and the problem is him (he doesn't do the overlays).
   - *His reason, verbatim:* "I didn't like the starting line… Feel more like me, and I'm working on the idea that my
     girlfriend isn't a content creator, but she's fucking good at it… she never gets videos done because I don't do
     the overlays. That's the problem, right?"
   - *His rule for this kind of request:* "I'll never be as good a writer as you… you still need to write it
     properly… make sure that everything is coherent with the greater document." Write it for reading aloud.
3. **Remove the repetition** (current ¶2 "My girlfriend Joy runs a beauty business…") and make ¶3–¶5 flow from the new
   opening. Keep "I'm AppyDave, let's get into it" after the hook. Touch later chapters **only** if coherence demands
   it, and say exactly where.
4. Update the ¶1 trigger (it still reads "stuck on one step"); keep chapters valid.
5. Save with `story.script.set`, passing `because` = David's reason above and `session` = your session id.
6. Write a readable before/after for chapter 1 to `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/d13-opening-rewrite-2026-11-01-diff.md`
   (old paragraphs, new paragraphs, one line per change on *why*).

## Out of scope

- Feel / do settings, sources, chapters 2–6 beyond coherence fixes.
- **No** send to TeleTubby or the Prompter — David presses those.
- Any FliStudio code.

## Done when

The script is saved, the diff file exists, and your final reply gives the new chapter-1 text in full plus the file
path, ending `APPYNET: done`.
