---
created: 2026-11-03
timestamp: 2026-11-03T10:20+07:00
---
# Brief: Story Pilot — angle proposals vanish after "Use this"; intros hidden; "undo prep" unclear (2026-11-03)

**From:** `flivideo-orch` (Swagger). **To:** `storypilot-dev`. Report to `flivideo-orch` by name.
**Go:** David, typed in flivideo-orch 2026-11-03 ("We also need to fix that A, B, C issue"). He is testing Story Pilot today:
he is the user of this fix, so keep the change small and land it fast.

## What David hit (D13, `/Users/davidcruwys/dev/video-projects/v-appydave/d13-overlay-pilot`)
He clicked **Use this** on proposal A. The angle was set (`story.json` `angle.by: human:ui`, setAt 2026-11-03T02:48:33Z) and
**all three proposals disappeared** from the page. The data is intact (`angleProposals.items` still holds A/B/C with intros),
so this is display only. He can't get B/C back, can't switch, can't undo the pick.
Screens: `/private/tmp/claude-501/-Users-davidcruwys-dev-ad-brains/f73fd5e0-e8b2-40ea-a51a-c97dd7efe8db/images/7.png` (before),
`.../images/8.png` (after).

## Fix — three things, smallest change
1. **Proposals stay after a pick.** Under the chosen angle, keep the proposals reachable (collapsed is fine: "3 proposed
   angles · A chosen ▸"), each with ▶ play and **Use this** to switch. Add a **clear angle** action (back to "not set").
   Switching/clearing is a human UI action only (`by: human:ui`), and must be undoable: keep the previous angle (e.g.
   `angleHistory` or reuse an existing undo pattern) so one click puts it back. **No agent verb may set or clear the angle.**
2. **Show the intro text.** Playing A/B/C reads the full `intro`, but the page shows only the one-line angle; the intro sits
   behind an ⓘ. Make the intro readable on the page (expand under the proposal; open it while it plays), so what you hear is
   what you can see.
3. **"undo prep" / "redo prep" in plain words.** David doesn't know what they do. Change the label and the ⓘ text to say
   exactly what gets reverted (e.g. "undo AI arrangement — puts the beats/sources back as they were before the last prep
   pass; your angle and script are untouched" — use whatever is TRUE in the code; check `prepBefore`). If it touches the
   angle, say so.

## Gates (orch merges and restarts)
Fresh branch from FliStudio main `be723e5` in your worktree, never the live checkout. Typecheck, `npm test`, targeted
storypilot e2e only (never the full suite; machine is loaded). Prove it on a **copy** of D13's story.json in a real browser:
pick A → B/C still visible → switch to B → undo → clear → proposals as before; intro text visible; new prep label.
Screenshots to `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-03/storypilot-angles-*.png`.
Do not touch D13's or D19's real story.json. Report: branch + commit, test tails, screenshot paths, what "undo prep" really does.
