---
created: 2026-11-03
timestamp: 2026-11-03T11:30+07:00
---
# Story Pilot screen — queued changes, bundled (2026-11-03)

**Status: COLLECTING — not a build order.** David is noting changes to the Story Pilot screen through the day; they will be
bundled into one pass (likely mocks first). Do not build from this file until flivideo-orch says the batch is closed.
Owner: `flivideo-orch`. Each item: David's words, the screenshot, what he does and does not want.

## 1. Proposed-angles block is hard to read (11:30)
- Screenshot: `/private/tmp/claude-501/-Users-davidcruwys-dev-ad-brains/f73fd5e0-e8b2-40ea-a51a-c97dd7efe8db/images/13.png`
  Durable copy: `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-03/david-batch-01-angles-hard-to-read.png`.
- David: "this screen is looking pretty hard to read. And I do see the need for play buttons, fast and slower, and all that
  sort of stuff, but I don't necessarily like the way you've done it with all that text on the screen."
- Keep: play, speed (slower / 1x / faster), per-proposal play, Play all.
- Problem: the player status line written out as text ("Angle A · angle · 1x · J slower · K 1x · L faster · paused"), long
  "why" text inline after each angle, many link-styled controls in one band.
- Direction (to mock, not decided): controls as buttons/icons with key hints in tooltips (same rule as the Reader ‹ › fix),
  quieter provenance text, clearer hierarchy.

## 2. "prepped ⓘ · undo AI arrangement" is not understood (11:35)
- Screenshot: `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-03/david-batch-02-prepped-unclear.png`
- David: "I just don't understand this section." Tooltip reads "Placed and ordered by agent:storypilot-prep · 2 Nov, 12:28 pm".
- What it is: the prep agent arranged the sources (order, roles, set-aside) on 2 Nov 12:28; the link swaps that arrangement
  with the one from before it (press again to swap back).
- Problem: jargon ("prepped", agent id), sits in the ANGLE band though it is about the sources list, and the consequence of
  the click isn't stated. Direction (to mock): move it to the sources/beats list header, say it in a sentence
  ("AI put these in order on 2 Nov · put back how they were"), or hide it behind a history control.
- David (11:40) on orch's plain explanation: put THAT on screen as the info tip. Use this text, near verbatim:
  "Prepped: an AI sorted this video's sources on <date> — their order (beats 01, 02, 03…), each one's role, and which to set
  aside. Undo AI arrangement swaps that sorting with the one from before it ran; press again to swap back. It doesn't touch
  your angle, your script or your files."

## 3. Settings tab is not understood (11:40)
- Screenshot: `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-03/david-batch-03-settings-unclear.png`
- David: "I think this is an important thing that we do, but I don't understand it, and … there's not enough information to
  help me understand it on the screen somewhere. Maybe information [tips] help."
- Fields: profile, audience, feel, do, notes, voice (+ "set on this video" / "from the creator" origin lines).
- Want: an ⓘ per field saying what it is, what it changes downstream (which agent/step reads it), and an example.
  The notes row currently holds an agent's message ("feel and do are UNSET… Ask David") — that's a question to David
  living in a settings field; consider surfacing it as a prompt instead.

## 4. Intros: drop the "I'm AppyDave, let's get into it" sign-off in story style (11:40) — CONTENT RULE, not UI
- David: "I'm hating the 'I'm AppyDave. Let's get into it.' … it doesn't make sense in this storytelling style."
- Applies to all three D13 intros (and any intro written for a Build-story / long-form profile). Owner when worked: the
  intro/angle writing rule (storypilot / storypilot-prep skills + the server prompt that writes `intro`), not the screen.
  Do not rewrite existing intros until the batch is worked.

## 5. Oswald set on sentences is hard to read (12:15)
- Screenshot: `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-03/david-batch-05-oswald-sentences.png`
- David: "I don't find Oswald, when it's heavily loaded like this, readable… It feels okay for the pills."
- Diagnosis (orch, UX): the brand already says "Oswald labels the world. Roboto carries the meaning"
  (`brand-dave/skills/brand/references/appydave/DESIGN.md` principle 2). The angle proposals A/B/C break it: 25–35-word
  sentences set in bold condensed Oswald, mixed case, two lines each, stacked three deep. Pills, tabs, nav, section titles,
  beat numbers are short labels → Oswald is fine there.
- Direction: angle text (and any sentence-length content) in Roboto, medium weight for the chosen/lead line; Oswald stays
  for the letter "A", labels and buttons. Brand-level rule proposed separately (needs David's go: it touches every app).

## Related, already shipped today (context for the batch)
- d65a16d proposals stay after a pick / clear / undo angle / intro readable / "undo AI arrangement".
- 5b9324e Reader key hints moved onto the buttons.
- e7dea41 Play speaks only the intro, not the bold angle line.
