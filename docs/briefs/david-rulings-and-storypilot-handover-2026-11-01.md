# David's rulings + Story Pilot handover — 2026-11-01

**Status stamp:** written 2026-11-01 ~08:45 +07 on Roamy by session `flivideo-field-trial-plan`
(`afaf0ee4-6ed3-47d8-84f0-42414018231a`). David is now **at the M4** and wants to work there directly from here on.
Everything below is his, said in the Roamy session this morning, relayed by me. Nothing here is done yet unless marked ✅.

---

## Part A — for `flivideo-orch`

### A1. Answers to the fli-notes v2 UAT questions (https://claude.ai/artifact/XBK9iekHsY7GhaCM28vqyp)

| Q | David |
|---|---|
| Q1 empty-space click | **Do NOT pass it through.** "If I wanted a normal click, I'd just click without holding those keys, wouldn't I?" Swallow every ⌘⇧ click. |
| Q2 other key cancels | Didn't understand it; take your recommendation (keep). |
| Q3 Lab opens on B | **Yes.** |
| Q4 C's dark terminal | Try a **light terminal as variant E**, as a test. His other opinions on C are in his Lab notes — read them. |
| Q5 settle = change | Didn't fully understand; take your recommendation (keep). |
| Q6 rename | Rename when it moves to the shared setup, not before. |

He tested the gesture in FliCut: "looks great". Lab variant B: "I like that as I hover, it goes white. I particularly
like that when I click on it, it gets a little bit bigger and it pops out off the screen. Good fucking work."
He has entered notes in the Lab on the M4 — **read them** (`notes.list`) and say whether they came through cleanly.

### A2. Do now (his go)

1. **Restart FliStudio and start FliCut** — "I'm not using FliStudio or FliCut right now, so you can restart them, please."
2. **Close the finished builders** (`fli-notes-core-dev`, `-studio-dev`, `-cut-dev`) and remove their merged worktrees —
   "They could be closed if that's the case."
3. Q1 change + variant E (small).

### A3. Bank — do not build (each needs a design first)

- **Screenshots as part of a note** — drag-in, paste-in, or region select. Reason: pointing at a DOM element (e.g. the
  words "my girlfriend") misses the outer area he actually means; he wants to mark the region that matters.
- **Story Pilot (the extension) is not noteable yet** — the gesture doesn't reach it. The real problem: integrating
  capture into every part of every app and extension cleanly, without it being "a horrible thing to implement".
- **"SuperRig" idea** (play on Superman): capture like Field Trial is cross-cutting and error-prone, so it should be
  built by an OpenRig rig that learns the best way to add it to any app as it goes, created and maintained by a
  "SuperRig" (not necessarily Rig B — depends what Rig B does today). Not for this session; it belongs with the
  OpenRig work on the M4.
- **FliHub side panels** (FliHub rebuild is parked; add to its notes): the Chapters / Help / DAM hover tabs should
  **push the content aside and sit side by side**, not pop over it. Settings should be contextual — a tab on the right
  that expands when needed (he likes Story Pilot's medium/large idea).
- **A hand-edit affordance for the script.** David: an agent is smarter but slower for fine-tuning; at recording time
  he wants to change a comma or one word himself ("That's the rationale for having a user interface").

---

## Part B — for the new M4 session `d18-storypilot-work`

### B1. What this is

David wants the Story Pilot knowledge from the last two days captured **against a video about Story Pilot**, so it
becomes story material. "We have an overlay pilot, but we don't have Story Pilot… we're not recording the knowledge
against a video." This is capturing information *before* deciding what goes in a script.

### B2. Do

1. Create the AppyDave project **`d18-story-pilot`** in FliStudio (next free code; d13 Overlay Pilot, d15 B-roll
   Pilot, d16 Motion Pilot, d17 FliHub rebuild exist). Use the `flivideo:flistudio` skill.
2. Attach as sources (resources, kind `session`) with a one-line `meta.why` each:
   - the Roamy session: transcript copied to the M4 at
     `/Users/davidcruwys/.claude/projects/-Users-davidcruwys-dev-ad-brains/afaf0ee4-6ed3-47d8-84f0-42414018231a.jsonl`
     (machine of origin: roamy; do **not** `--resume` it — David will continue it on Roamy tonight);
   - the D13 writer session `d13-write` (session `730621cb-22e1-4823-b22f-2c4fb5ca09ba`) — the "rewrite as a writer,
     not a paste" correction;
   - this file and `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/d13-opening-rewrite-2026-11-01-diff.md`.
   Do not write the script; feel/do stay unset.
3. Then stay as David's conversation partner on the M4 for D13 recording and Story Pilot. He hand-edits the script
   himself; you don't touch D13 unless he asks.

### B3. What happened (for your context)

- **D13 (Overlay Pilot video):** opening rewritten by `d13-write` (flivideo `0ebe978`); David: "a wonderful
  introduction". He'll tweak words by hand at recording time (e.g. "bloody"). Folder committed to v-appydave by
  `d13-write`, on Roamy's reading of "I would want this pushed up" (David told).
- **The Story Pilot lessons, in David's words:**
  - A spoken change is an **instruction for the writer**, applied coherently across the script, then shown as a diff —
    not text to paste. ("I'll never be as good a writer as you… you still need to write it properly.")
  - **Agent for thinking, UI for fine-tuning.**
  - **Reading taste:** white reads best but needs contrast around the focus; cream is nice but harder to read; rich
    text is hard, terminals easy. Evolve looks by testing in isolation (the Lab), never "restore". Story Pilot is the
    first wall-of-text screen — which is why it is the test page.
  - **Self-learning apps:** notes are data for the AI, not a screen for him; capture invisible until ⌘⇧ is held.
- Drift report (why FliStudio reads heavier than July): https://claude.ai/artifact/WTpciy7zHpPa7DUKwLKbGR
- Field Trial corrections: `/Users/davidcruwys/dev/ad/appydave-plugins/dev-team/skills/field-trial/references/learnings.md`
  (2026-11-01).
