---
created: 2026-11-01
timestamp: 2026-11-01T11:40+07:00
---
# Brief: FliStudio — quiet ✎ notes icon + Projects "Show" filter (2026-11-01)

**From:** `flivideo-orch` (Swagger). **To:** `flistudio-dev` (tmux `flistudio-dev`).
**Worktree:** `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/studio-dev`, branch `studio-dev`, from main `62a4524`.
**Go:** David, 2026-11-01 ~11:35 +07 ("we should be using the appropriate windows or even potentially creating new
windows when needed"). **Report to `flivideo-orch` by name (SendMessage).** Questions → orch with a recommendation; never wait on David.

## Lane

You are the **FliStudio app** worker (anything outside Story Pilot). Story Pilot code belongs to `storypilot-dev`
(worktree `rail-v2`), which is mid-build on `modules/storypilot/**`. **Do not touch `modules/storypilot/`.** Do not
merge, do not restart FliStudio, do not touch the live checkout `/Users/davidcruwys/dev/ad/flivideo/flistudio`.

Read first: `/Users/davidcruwys/dev/ad/flivideo/flistudio/CLAUDE.md`, `docs/AGENT-NOTES.md` in your worktree, and run the
`appystack:appystack-conventions` skill.

## Unit 1 — bring back a quiet ✎ notes icon in the top bar

**David's words, verbatim (today, 11:20):** "It's just that it's at the place that used to be the notes area. What
happened to the notes button? Did we remove that based on my last conversation? I didn't remember giving a ruling to
remove it, per se. I did give plenty of rulings about making the user interface more streamlined … I thought we had a
button there, and now it's been replaced by a different button, but the old one's disappeared. That felt a bit odd."

**Earlier, 07:30 (the ruling that removed the notes page):** "yes remove notes page" and "It wasn't asked for, and
it's certainly not in the format I want." The v2 brief
(`/Users/davidcruwys/dev/ad/flivideo/docs/briefs/fli-notes-v2-quiet-capture-and-lab-2026-11-01.md` §2) also recorded:
"A small, quiet icon in the top bar as a fallback toggle is acceptable (David: 'that would be okay')." It was never built.

**Also David, today:** "if there is [a shortcut], I should be able to hover over that button and know that there is a shortcut."

**Build:**
- A small, quiet ✎ icon in the top bar, beside the Frames button (`client/src/components/TopBar.tsx`).
- Click = toggle the existing sticky note-capture mode (the one ⌘⇧ hold-click already uses; one shared implementation, do not fork it).
- Tooltip names the gesture: e.g. "Notes — hold ⌘⇧ and click anything. Click here to stay in note mode."
- **No notes page, no counter, no panel.** That ruling stands.
- Rule for this and every top-bar button you touch: if it has a shortcut, the tooltip says so.

## Unit 2 — Projects "Show" filter: between radio and checkbox

**David's words, verbatim (today):** "the conversation was about radio buttons versus checkbox buttons and how I wanted
something in between. Yet I don't remember anything ever being done."
Screenshot of the current state: `/private/tmp/claude-501/-Users-davidcruwys-dev-ad-brains/f73fd5e0-e8b2-40ea-a51a-c97dd7efe8db/images/5.png`
(chips: Needs attention · Working · Not started · Published · Parked · Abandoned; off chips struck through).

**Why it matters:** D18 vanished from the list under a "Working"-only filter while David was working on it.

**Orch ruling (the "in between"):**
- **Click** a chip = show only that status (solo, radio-like).
- **⌘-click** a chip = add/remove it from the set (checkbox-like).
- An **All** chip that turns every status on.
- **★ rows (worked on today) always show**, whatever the filter.
- Tooltip on the chips states the gesture ("Click: only this · ⌘-click: add or remove").
- Keep the current visual language (struck-through = off); persist the selection the way it does now.

## Done =

- Gates in the worktree: `npm run build -w shared` then typecheck, `npm test`, and an e2e for each unit
  (✎ toggles note mode; click solos, ⌘-click adds, All resets, a ★ row survives a filter that excludes it).
- Screenshots at 2000 and 1440: top bar with tooltip showing; Projects list after a solo, after a ⌘-click add.
- Commit per unit, push `studio-dev`. **Do not merge.** Report to `flivideo-orch`: commits, gate tails, screenshot
  paths, and every taste call you made.
