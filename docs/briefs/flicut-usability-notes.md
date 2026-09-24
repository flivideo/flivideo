---
type: brief
title: FliCut usability notes — batch
description: "David's hands-on FliCut observations (d04 edit, 2026-09-24), collected as a batch for one usability pass — NOT yet dispatched."
created: 2026-09-24
timestamp: 2026-09-24
status: collecting
---

# FliCut usability notes — batch

**Purpose**: One place for David's UI observations while he uses FliCut on d04. He asked for them to be
**batched, not delegated one by one**: *"Not everything I'm asking you to do needs to be delegated
straight away. A lot of what I'm going to talk about is just user interface stuff. I think baking it all
up would be better than just doing it."*

**For Agents**: flivideo-orch keeps adding to this. Nothing here is dispatched until David says the batch
is ready. Then it becomes one usability brief for the `flicut` window: mock first, frontend-design skill,
minimal but functional.

David's headline: *"I don't think you've used this application. I think this whole application has not
been viewed from any sort of serious usability point of view because nothing feels nice."*

## Already dispatched before the batch rule (in flight in the flicut window)
- Real undo/redo (⌘Z walks back, ⇧⌘Z forward) + a clickable history panel.
- The film strip follows the playhead; the scrollbar is visible; trackpad scroll pans.
- J/K/L match FliHub/FliCast (J = reverse) + an on-screen speed/direction indicator.
- Trim → frame-accurate in/out: mock https://claude.ai/artifact/GoVGaZPzBq28U86c3yBJJy, 3 questions
  open (exact vs padded; ←/→ = playhead, I/O = in/out, inverse → ⇧I; commit at once). **Awaiting David.**

## Observations (verbatim + what the code does)

| # | David said | What it actually does (code: `flicut/src/renderer/src/Editor.tsx`) | Problem |
|---|---|---|---|
| 1 | "skip cuts … Pressing the button doesn't seem to change the interface, so I'm not sure what it's doing." | `viewState.skipCuts` (K): playback jumps over removed material. Playback only. | No visible change; the purpose is invisible |
| 2 | "I don't really understand what inverse cuts are about." | `inverseCuts` (I): plays ONLY removed material (audit), with a yellow "AUDIT" banner on the player | The name doesn't say "audit removed bits"; it also reshapes the transcript |
| 3 | "turn off show cuts. I get these big blank areas on the screen." | `showCuts` (H) hides removed words, but paragraph blocks keep their space | Hidden text leaves holes; it should collapse |
| 4 | "I don't really understand what first and last are doing. They feel like a weird toggle." | `⇤ first` / `last ⇥`: toggle-cut the whole first/last segment (usually lead-in/out silence); line-through when cut | One-click toggle on an invisible segment; no preview of what goes |
| 5 | "trim beginning … I can't understand what [it] does" | whole-timeline mask before the playhead (being replaced by in/out) | See the trim mock |
| 6 | Timeline "doesn't scroll … kinetic or momentum … should the film strip be scrolling with you?" | no follow; drag scrubs | in flight (film strip) |
| 7 | "Is there an undo history? Can we even see the history?" | undo toggles; history is read-only | in flight (undo/history) |
| 8 | Speed: "no indication of how fast we're going" (J slowed rather than reversed) | J/K/L semantics differ from the other apps | in flight (J/K/L) |
| 9 | Lead-in "half a second or a second of padding at the beginning, which I might want to play around with" | only via pad 0.15/0.15 (cuts) or the trim buttons | covered by the trim mock's worked example |

## Ideas to consider in the pass (orch, not David — to discuss)
- A real usability review: someone actually uses FliCut end to end on d04 (screenshots, a task list:
  review cuts, fix a bad cut, trim lead-in, audit removed material, export) and writes the friction log
  before any redesign.
- Group the toolbar by job (View · Playback · Edit), with plain labels and a one-line tooltip each.
- Make view toggles show their effect (e.g. skip cuts → strip gaps / a player badge "skipping cuts").

## Product first — what a human wants to do in a Gling-style cut editor (orch, 2026-09-24)

David: *"even before you do usability research, I want you to think about the product … what real
usability means for a human … What sort of things would I want to be able to do? It should just be a
simple list."*

Grounding: Gling's own framing ("edit the video by editing the transcript — delete a sentence and the
video follows"; one-click cut silences / bad takes / filler words — https://www.gling.ai/save-time,
https://www.gling.ai/), and our Gling teardown
`/Users/davidcruwys/dev/ad/brains/video-editing-as-code/gling-ui-surface-map.md` (the WORD is the unit;
silence/filler/bad take are *labels the AI puts on takes* that you accept or reverse; Gling's toolbar is
just play · speed · show cuts · skip cuts · split · pace · zoom).

### The jobs (a human, editing a talking-head rough cut)
1. **Watch it as the viewer will** — play the finished edit start to finish, cuts skipped.
2. **Read it like a script** — the transcript is the video; delete a sentence, the video follows.
3. **See what the AI took out, and why** — pause / um / bad take, and how much in total.
4. **Overrule the AI** — keep or remove one cut, or a whole kind of cut, in one place.
5. **Pick the best take** — when I said a line three times, choose which one stays.
6. **Check a join sounds natural** — play a few seconds either side of a cut.
7. **Set the pace** — tighter or looser pauses for the whole video, hearing the result before committing.
8. **Set exact start and end** — frame-accurate in/out on a clip (lead-in, lead-out).
9. **Find a moment** — search a word, jump to the next cut or the next clip.
10. **Move fast** — play/pause, J/K/L, speed shown on screen, frame step.
11. **Know where I am** — time in the finished video and which source clip I'm in.
12. **Fix a misheard word** — correct the transcript without changing the cut.
13. **Undo anything** — step back and forward, see the history, jump to a point.
14. **Hear clean audio** — compare raw vs enhanced and choose.
15. **Export and know what I got** — length, files, where they went.
16. **Pick up where I left off** — reopen exactly as I left it.
17. **Let an agent do a pass, then review it** — it proposes, I approve.
18. **Fine-grain control (David, 2026-09-24)** — zoom into a tight spot and move an edge by 1–2 frames
    without the drag jumping 20–30; a modifier that re-scales the timeline (or works around the words
    on screen) for precision; zoomed-in waveform and picture frames to *see* the exact spot. His words:
    *"The problem with a tool like Gling is that it only has one level of visibility … There's never really
    a modify key … If you try to drag a line, you could move 20 or 30 frames at a time when you only want to
    move one or two frames, but you also want to visualise that … seeing visible waveforms and pictorial
    forms in a zoomed-in aspect would actually be a lovely capability."*

### What "real usability" means here
- **Usability is number one; layout and visualisation come right behind it** (David: "usability has to be number one, and then how it's all laid out and visualised is also incredibly important").
- **The video is the truth.** Every action shows its effect on the finished video at once.
- **Nothing is lost.** Everything is reversible, and I can always see what's hidden.
- **Name controls by the job, not the mechanism** ("play finished video", not "skip cuts").
- **Modes are visible.** I can always tell what state I'm in (auditing, skipping, trimming).
- **One obvious way to do each job.** The keyboard for speed, the mouse for precision.

## Blueprint decisions (David, 2026-09-24, walking https://claude.ai/artifact/LPsaH4jcz2rhS2WxCvTSFg)
- **§1 Layout: approved as recommended.** One mode switch (Watch finished · Review cuts · Hear removed) replaces show/skip/inverse; edits open in **Review cuts**. Removed material as chips; two-lane timeline; both clocks; inspector.
- **§2 Cut loupe: approved** ("This feels really cool").
  - Opens on **⌥-click a cut** (or Enter on a selected cut); Esc closes. A plain click only selects.
  - It appears **inline under the words** (not in a side panel).
  - Play around = **2 s before, 1 s after** (to be tuned after use).
- **§3 Precision patterns: all 13 to be implemented** as mapped in the loupe column.
- **New requirement: help** (*"we should have good, easy-to-access help because I won't remember any of [the keys]"*). **Approved: all three layers plus a how-it-works page.**
  1. Tooltips on every control (what it does · its key).
  2. Contextual key strip inside the loupe and the other modes, shown only while you're in them.
  3. `?` opens a cheat sheet of every shortcut, grouped by job, with search; it can be **pinned** beside the editor (orch's call, since David didn't pick between print and pin).
  4. A "how FliCut works" page: the modes, the loupe, the chips, undo/history. For coming back after weeks away.
- **§4 Pick the best take: approved as recommended.** A simple version first: FliCut groups repeated takes as "↺ take N of M" chips and you click the one to keep. "Pick the best one for me" comes later.
- **§4 Fix a misheard word: yes, thought through as 8 bad-wording cases.** The cases: (1) own names misheard repeatedly, (2) one-off mishearing, (3) said it wrong, (4) style/format, (5) split/merged words, (6) missing/invented words, (7) filler misjudged, (8) people/place names. David: *"almost all of them from the eight listed are real."*
  - **Case 3 (said it wrong): no decision yet.** It needs more software; re-recording is *not* the answer for now.
  - **Corrections stay in the FliCut edit.** They do NOT write back to the raw transcript: *"it is crossing a boundary … I will say no."*
  - **Dictionaries and wording rules live in FliStudio, not FliCut** (RULING): levels **global? → brand → project**. David: *"What I'm calling global probably is brand level … Maybe I do need both levels."* Design with all three and let global be optional/empty. **One centralised word store for the whole suite** (FliTools' vocabulary included). FliCut (and FliTools, FliHub, the rest) *use* them. *"FliCut just uses the information. That way, the other tools can also use it if needed."* This implies FliStudio owns a word-rules store, with FliTools' vocabulary and FliCut's dictionary reading from it.
  - Fixing words in FliHub is wanted but **out of scope** for this work.
- **§5 Every key is also a verb: approved.** Agents may make the fine edits themselves (`cut.nudge`, `take.choose`, `word.correct`, …). This is a **tentative** yes (*"I'm going to say yes, but I'm not sure in reality"*). Default working rule until he's used it: agents **propose** and David approves in the loupe; in an explicit autopilot pass (like d04) they apply directly, and every change is an undoable history entry. Revisit after real use.
