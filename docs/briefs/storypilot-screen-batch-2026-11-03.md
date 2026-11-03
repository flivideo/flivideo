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

## Related, already shipped today (context for the batch)
- d65a16d proposals stay after a pick / clear / undo angle / intro readable / "undo AI arrangement".
- 5b9324e Reader key hints moved onto the buttons.
- (in progress) Play speaks only the intro, not the bold angle line.
