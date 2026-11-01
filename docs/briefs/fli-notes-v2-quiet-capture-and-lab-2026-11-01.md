# Brief: fli-notes v2 — quiet capture, life states, Story Pilot Lab — 2026-11-01

**From:** Roamy session `flivideo-field-trial-plan`. **To:** `flivideo-orch`, M4.
**Go:** David, 2026-11-01 ~07:30 +07, verbatim: "Go on both… Okay, I like option A." Also: "yes remove notes page".
**Follows:** `fli-notes-suite-record-2026-10-31.md` (v1, built overnight). Corrections to v1 are in
`/Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/field-trial/references/learnings.md` (2026-11-01 entries) — read them.

## Why v2

v1's data and door logging were right; its interface was wrong. David's goal is a **self-learning application**:
notes, instructions and observations attach as data to any row, element or group; **the AI reads them, he doesn't need
to.** Capture must be invisible until called, then vanish — "part of the landscape, without the landscape looking
different". The log stays quiet: not in his interface unless he turns it on as an extension.

This is meant to become how **every** app David builds learns, not a FliVideo feature.

## Timing and live-app rule

David is on Roamy now and will use FliStudio on the M4 **later today to narrate D13**. Build in worktrees now. Before any
merge into the live checkout: busy-check, and do not restart FliStudio or FliCut while he is working in them — tell
him (via the morning/UAT page or Roamy) and wait. A separate session is rewriting D13's opening: **do not write D13.**

## Build

**1. Remove (FliStudio + FliCut).** The Notes page/zone, the rail count, the before/after diff view, the ✎ toggle
button, and the ⌥⇧N / ⌘⇧N shortcut. Keep fli-core's record, the door logging and the `notes.*` verbs.
David: "It wasn't asked for, and it's certainly not in the format I want… It would need a design before we build it."

**2. Capture gesture — Option A, David's pick (both apps).**
- Left hand **holds ⌘ + ⇧**; anything that can take a note **highlights under the pointer** as the mouse moves.
- **Click while held** opens a small note box on that thing. The app **swallows that click** (capture phase,
  `preventDefault`), so a link or button under it does nothing — this removes the ⌘⇧-click-opens-a-tab catch.
- **Release** → highlights vanish; the app looks exactly as before.
- A small, quiet icon in the top bar as a fallback toggle is acceptable (David: "that would be okay").
- One shared implementation, not per page.

**3. Life states on the record (fli-core minor release).** Every record can be settled so future reads skip it while
history stays:

| State | Means |
|---|---|
| `live` | relevant; agents read it (default) |
| `done` | implemented |
| `used` | already fed into something — say what (e.g. a prompt version, a promoted page) |
| `stale` | no longer true — say why (interface moved on / thinking changed) |
| `replaced` | a newer record covers it — point at it |

State changes are appended as new lines (never rewrite). Readers (`readNotes`/`scanNotes`/`notes.list`) default to
`live` with an option for history. Map v1's ask `open`/`done` onto this. **Keep the schema app-neutral** — no FliVideo
words in field names — so it can later move into a shared core for all of David's apps. Do not move it yet.

**4. Story Pilot Lab (FliStudio).** A page beside Story Pilot (not replacing it) that reads the **real** D13 story data
and switches between reading variants, so David can play with them and later promote what he likes to the main page:

| Variant | What it shows |
|---|---|
| A · Now | today's script panel, as the baseline |
| B · White focus | cream page; clicking a chapter fades/glows it into a white reading surface (animated, polished) |
| C · Terminal feel | the same script in a monospace, terminal-like reading view |
| D · Settings | the "For whom and why" block shown behind a tab vs inline, side by side |

- Build variants from **one shared token/component** so promoting one later is a single change, not per page.
- The Lab is where Field Trial and A/B testing finally meet (the thing Mochaccino never had): notes taken in the Lab
  attach to the variant. When a variant is promoted or deleted, its notes become `used`, pointing at the final page —
  readable later, never orphaned (each note already stores the words of what it was about).
- Read-only on story data. Do not change the main Story Pilot page's look.

**David's reading taste (the reason for the variants):** white is the best surface for reading, but needs contrast
around the area in focus; cream is nice but harder to read; rich text is hard for him, terminals easy (unsure if that
holds everywhere); evolve by testing in isolation — never "restore" an old look. Story Pilot is the first wall-of-text
screen, which is why it is the test page.

## Out of scope

Promoting a variant to the main page; brand skill or template changes; other apps; any notes "management" screen.

## Done when

- FliStudio + FliCut: no visible notes UI; ⌘⇧ hold-highlight-click works and swallows the click; release restores the
  screen unchanged. Tests prove the click is swallowed on a link.
- fli-core released with life states + defaults; v1 records still read.
- Story Pilot Lab live with A–D on D13's real data; a Lab note lands as `live` against its variant.
- A short visual UAT page (AppyDave, light only): what to press, what to look for, what isn't done, batched questions
  with a recommendation each. Checkpoint updated.
