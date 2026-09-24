<!-- FliVideo source bundle · FliCut UX — the 18 jobs, David's observations, and the editor UX research (cut loupe, two-lane timeline, mode switch) · generated from docs/briefs/flicut-usability-notes.md, ~/dev/ad/brains/video-editing-as-code/editor-ux-research.md -->


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
`~/dev/ad/brains/video-editing-as-code/gling-ui-surface-map.md` (the WORD is the unit;
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



---


# Editor UX for a text-first cut editor

**Purpose**: Ground FliCut's usability redesign in how the best editors solve the jobs FliCut must do.
Research plus a recommendation. It decides nothing for David.

**For Agents**:
- Read this before designing or building any FliCut editor UI change: layout, trim, nudge, modes, pace, review.
- The headline answer to David's #18 (fine-grain control) is §1.4, the **cut loupe**.
- The visual companion is the artifact **FliCut Editor Blueprint**, <https://claude.ai/artifact/LPsaH4jcz2rhS2WxCvTSFg>. It shows the layout sketch and a working loupe. Source: [.artifacts/flicut-editor-blueprint.html](./.artifacts/flicut-editor-blueprint.html).
- The FliCut status claims in §3 read the code at `flivideo/flicut` **3fb91bd** (2026-09-24), not a running window. FliCut was not launched; David was using it on d04.
- Sources carry their own confidence. Items marked **[unverified]** come from secondary sites only. Adobe helpx returned 403 to the fetcher, so Adobe claims come from indexed snippets of those pages.

**Inputs**: brief `docs/briefs/flicut-editor-ux-research.md`; job list
and observations `docs/briefs/flicut-usability-notes.md`;
[gling-ui-surface-map.md](./gling-ui-surface-map.md); [../filmstudio/verdict.md](../filmstudio/verdict.md)
and [../filmstudio/capability-inventory.md](../filmstudio/capability-inventory.md) §timeline;
[../screen-studio/INDEX.md](../screen-studio/INDEX.md); FliCut `docs/SYSTEM.md`, `Editor.tsx`,
`Timeline.tsx`, `Script.tsx`, `Pace.tsx`, `hotkeys.ts`; the trim mock <https://claude.ai/artifact/GoVGaZPzBq28U86c3yBJJy>.

---

## Quick Find — answer first

| Question | Short answer | § |
|---|---|---|
| How do pros move an edge by 1–2 frames? | Select the **edge**, press `,` `.` (1 frame) with Shift for many. A two-up view shows the last frame out beside the first frame in | 1.1 |
| What stops a drag jumping 20–30 frames? | Edits by drag happen only in a **geared** view at a fixed px per frame (Logic's Control-Shift-drag breaks the 1:1 pointer link). The timeline drag stays a scrub | 1.3 |
| What is the one thing to build? | A **cut loupe** at the cut in the transcript: two-up frames, a ±5 frame strip, and a waveform zoomed to ±0.5 s (Resolve's audio auto-zoom) | 1.4 |
| How should removed material look? | A grey strikethrough or chip that stays visible, one click restores it, and the colour gives the reason. **Never a hole** | 2.2 |
| Show cuts / skip cuts / inverse cuts? | Replace all three with **one mode switch named by the job**: Watch finished · Review cuts · Hear removed | 2.3 |
| Is the FliCut timeline the wrong shape? | Make it two lanes: the whole edit (overview) plus a fixed-zoom detail lane (Resolve cut page) | 2.1 |
| What does FliCut lack most? | Play-around, take choice, transcript correction, edge nudge with two-up, word search | 3 |
| Can the agent do what the UI does? | Half of it. Propose, apply and export exist over RPC; nudge, inspect, trim, take choice and undo do not | 4 |

---

## 1. Fine-grain control (David's #18, the headline)

David: *"If you try to drag a line, you could move 20 or 30 frames at a time when you only want to move one
or two frames, but you also want to visualise that … seeing visible waveforms and pictorial forms in a
zoomed-in aspect would actually be a lovely capability."*

### 1.1 What each product does

| Product | How you move an edge by 1–2 frames | How you see it | Source |
|---|---|---|---|
| **Final Cut Pro** | Select the edit point (`[` left edge, `]` right edge). `,` / `.` = 1 frame, Shift = 10 frames. Option adds subframes on connected audio. Numeric: `+`/`−`, type `2`, Return. `⌥[` / `⌥]` trim to the playhead | **Precision Editor** (Control-E or double-click an edit): the outgoing clip sits above the incoming one with unused media dimmed; click any frame to move the edit there. **Detailed trimming feedback** shows a two-up in the viewer (last frame out, first frame in); hold Option to toggle it | [extend/shorten](https://support.apple.com/guide/final-cut-pro/extend-or-shorten-clips-ver9847ec25/mac) · [shortcuts](https://support.apple.com/guide/final-cut-pro/keyboard-shortcuts-ver90ba5929/mac) · [timecode entry](https://support.apple.com/guide/final-cut-pro/navigate-using-timecode-ver1632d762/mac) · [Precision Editor](https://support.apple.com/guide/final-cut-pro/use-the-precision-editor-verc1fac344/mac) · [two-up](https://support.apple.com/guide/final-cut-pro/show-trimming-details-in-the-viewer-ver3363b235/mac) |
| **Premiere Pro** | Trim mode: Opt-←/→ = 1 frame, Opt-Shift = "many" (the Large Trim Offset preference, default 5). Numeric: numpad +N / −N on the selected edit. Shift-click selects several edits to trim together | **Trim Monitor**: an outgoing pane and an incoming pane. Text-Based Editing does coarse cuts; fine-tuning happens on the timeline, and the Text panel has no word-boundary nudge | [trim mode](https://helpx.adobe.com/premiere-pro/using/trim-mode-editing.html) · [trim prefs](https://helpx.adobe.com/premiere/desktop/get-started/preferences-and-settings/trim-preferences.html) (snippets) · [Monahan, Adobe](https://blogs.adobe.com/kevinmonahan/2012/10/24/timeline-trimming-using-keyboard-shortcuts-in-premiere-pro-cs6/) · [TBE](https://helpx.adobe.com/premiere/desktop/edit-projects/edit-video-using-text-based-editing/edit-sequences-using-text-based-editing.html) |
| **DaVinci Resolve** | Edit page: `,` / `.` nudge 1 frame, Shift for more; U cycles the edge side; the Speed Editor jog dial trims live | **Cut page dual timeline**: "the upper timeline shows you the entire program while the lower timeline shows you a zoomed in area … you never have to zoom again". Its trim editor lays the clip out "in a film strip with each frame visible". ⭐ **Audio auto-zoom**: "when trimming, the clip audio will automatically zoom in so you can position your edit perfectly against dialog" | [Resolve cut page](https://www.blackmagicdesign.com/products/davinciresolve/cut) · [R11 shortcuts PDF](https://documents.blackmagicdesign.com/SupportNotes/DaVinci_Resolve_11_Mac_Keyboard_Shortcuts.pdf). Shift = 10 frames and the two-up/four-up trim layout are **[unverified]** in the current manual |
| **Avid Media Composer** | Trim mode (U): `,` / `.` = 1 frame, `M` / `/` = 10 frames. You pick the A side, the B side or both | The monitors show both frames. **Space loop-plays the transition** while you trim | [editvideofaster](https://www.editvideofaster.com/avid-keyboard-shortcuts-trimming/) **[unverified]**; the official [PDF](https://resources.avid.com/SupportFiles/attach/Keyboard%20Shortcuts.pdf) confirms trim mode and 10-frame steps |
| **Descript** | Zoom the timeline "until [the word] has been ungrouped", then hold Cmd and drag its boundary over the waveform. One word at a time. ←/→ step 1 frame. A gap is a number: right-click → *Edit word gap* (Cmd+G) | Wordbar over the waveform. **No two-up, no fine/coarse modifier.** Edit boundaries (¦) offer Regenerate and Restore, but no nudge | [wordbar](https://help.descript.com/hc/en-us/articles/10249346632717-The-wordbar) · [word gaps](https://help.descript.com/hc/en-us/articles/12878313339021-Trim-and-adjust-spaces-between-words) · [shortcuts](https://help.descript.com/hc/en-us/articles/10255582172173-Keyboard-shortcuts) · [edit boundaries](https://help.descript.com/hc/en-us/articles/20952542722957-Edit-boundaries) |
| **Gling** | Frame-quantised edge drag on the timeline (`ClipResize.tsx`, [FliCut Trim Options](../ARTIFACTS.md#flicut-trim-options)); Pace sets padding globally. No documented nudge key | One zoom level at a time, which is David's complaint. Reviews call it "no keyboard shortcuts" | [primalvideo](https://primalvideo.com/guides/gling-ai-tutorial/) · [gling.ai](https://www.gling.ai/). The absence of a nudge is **[unverified]**: there is no official help centre |
| **Logic Pro** | Option-←/→ nudges by a set value (ticks, frames, samples). ⭐ **Control-Shift-drag** moves by ticks, or samples when zoomed in, and "breaks the 1:1 relationship between the pointer and region movements" | Sample-level waveform zoom | [snap to grid](https://support.apple.com/guide/logicpro/snap-items-to-the-grid-lgcpf7c0f66a/mac) · [move regions](https://support.apple.com/guide/logicpro/move-regions-lgcpf7c0d489/mac) (snippet) |
| **Pro Tools** | Numpad ± nudges by the nudge value; Option nudges the clip **head**, Cmd the **tail** | Zoom Toggle (E) fills the window with the selection and toggles back | [production-expert nudge](https://www.production-expert.com/production-expert-1/pro-tools-nudge-shortcuts-clip-placement) · [zoom](https://www.production-expert.com/production-expert-1/pro-tools-zooming-shortcuts) **[unverified, secondary]** |
| **Audacity** | Zoom to Selection (Ctrl+E); **Zoom Toggle (Shift+Z)** flips between two preset zooms (default "normal" and "4 px per sample") | Sample-level waveform | [zooming manual](https://manual.audacityteam.org/man/zooming.html) |
| **Screen Studio** | Drag clip edges with a zoom slider; each trim becomes a yellow bubble you click to undo. **No documented frame nudge or modifier drag**; a zoom-timeline shortcut is an open request | Timeline only | [trimming guide](https://screen.studio/guide/trimming) · [feature request](https://hub.screen.studio/p/shortcut-to-zoom-timeline-cmd-scroll-pinch-to-zoom-cmd) |
| **CapCut desktop** | Arrows step 1 frame, Shift for several; Alt+scroll zooms; the magnet toggles snapping | Timeline only | [skillademia](https://www.skillademia.com/shortcuts/capcut-shortcuts/) **[unverified]** |

### 1.2 The patterns

| # | Pattern | Best example | Fits around the words? |
|---|---|---|---|
| P1 | Two-speed keyboard nudge on a selected edge (1 frame / N frames) | FCP `, .` + Shift = 10; Avid `, .` / `M /` | **Yes**: a selected cut becomes the selected edge |
| P2 | Pick the edge before moving it (out, in, both) | FCP `[ ]`; Resolve U; Avid A/B side | **Yes** |
| P3 | Numeric relative move (`+2 ⏎`) | FCP; Premiere numpad | **Yes** |
| P4 | Two-up frames at the join | FCP detailed trimming feedback; Premiere Trim Monitor | **Yes**: the core of the loupe |
| P5 | Filmstrip trim editor | Resolve trim editor; FCP Precision Editor | Adapted: keep a ±5 frame strip only |
| P6 | Overview + detail | Resolve cut page dual timeline | Adapted: the **transcript is the overview**, the loupe is the detail |
| P7 | Automatic waveform zoom when an edge is grabbed | Resolve cut page | **Yes**: the loupe opens already zoomed |
| P8 | Zoom toggle / zoom to selection | Audacity Shift+Z; Pro Tools E | Not needed: the loupe is always zoomed |
| P9 | Geared modifier drag | Logic Control-Shift-drag | Adapted: fixed px per frame inside the loupe |
| P10 | Loop-play the join while trimming | Avid Space; Premiere play-around | **Yes** |
| P11 | Snapping and scrub toggles | FCP N and Shift-S; CapCut magnet | Adapted: snap to word edge, energy minimum or zero crossing |
| P12 | Head/tail nudge with a set unit | Pro Tools ⌥ / ⌘ numpad | Folded into P1+P2 |
| P13 | The gap as an editable number | Descript *Edit word gap* | **Yes**: FliCut's pause chip already does this (ADR-0003) |

### 1.3 Why FliCut's drag jumps

`Timeline.tsx` maps the pointer 1:1 to output time at the current `pps` (px per second), and a drag only
scrubs. At the auto-fit zoom of a 4-minute edit on a 1,200 px strip, 1 px ≈ 0.2 s ≈ 5 frames, so even a
careful hand move is 20–30 frames. The only frame-exact edit is the arrow nudge, which moves the clip
**start** alone (`nudgeBoundary(p, id, 'start', d / fps)`) and zooms to frame level first. There is no way
to pick the out edge, no two-up and no geared drag.

**The fix is not a better zoom.** Every product that does this well either (a) moves edges by keys at a
fixed step, or (b) does the drag in a separate view whose gearing does not depend on the timeline zoom
(FCP Precision Editor, Resolve trim editor, Logic's geared drag).

### 1.4 Recommendation — the cut loupe

**One component, anchored to the cut in the transcript.** It combines FCP's two-up, Resolve's audio
auto-zoom and the FCP/Avid key grammar. The working sketch is section 2 of the artifact.

1. **Select a cut** in the script: click its chip or seam, or step with ⌥←/→. The loupe opens under the line.
2. **Pick the edge**: `[` OUT (end of kept material before the cut), `]` IN (first kept frame after it), `\` both (a roll).
3. **See it**:
   - two large frames, last frame out and first frame in;
   - a ±5 frame strip either side;
   - a waveform per edge at ±0.5–0.6 s of **source** time with frame ticks, ASR word bars and the removed side shaded, so you can see what a nudge would bring back.
4. **Move it**:
   - `,` `.` = ±1 frame, Shift = ±5 frames;
   - `+`/`−` then a number then ⏎;
   - drag on the waveform, geared at **12 px per frame** whatever the zoom, ⌥-drag at 40 px per frame;
   - `W` snaps to the word boundary (plus padding).
5. **Hear it**: Space loop-plays about 1 s either side of the join (Avid).
6. **Say where it is**: the readout gives the offset from the engine's proposal *and* from the nearest word boundary (`IN +2f from "idea starts"`). Humans and agents share that reference.

It fits the model without a new data type. An edge move is a SPLIT/MASK boundary change on the
clips either side, `cutBy: 'user'`, one undo step (ADR-0001 / ADR-0003). It also meets the trim mock:
per-clip in/out (`I`/`O`) is the same loupe with only one side. The mock's open question 2 (arrows move
the playhead) is consistent with this, because edges move with `,` `.` and not the arrows.

---

## 2. Layout and visualisation

### 2.1 How text-first editors lay out the screen

| Product | Transcript | Preview | Timeline | Notes |
|---|---|---|---|---|
| **Descript** | Main surface | Full-screen, stacked or side-by-side (View menu) | **Hidden by default** in the new timeline; handle above the transport (Ctrl+Opt+T); layout saved per project | [layout](https://help.descript.com/hc/en-us/articles/37508206076429-Manage-the-editor-layout-with-the-View-menu) · [new timeline](https://help.descript.com/hc/en-us/articles/36492789575565-The-new-timeline-experience) |
| **Gling** | Left, line by line, with a scissor per line | Right | Bottom: film strip plus waveform, Show/Skip cuts, Split, Pace, zoom | [gling-ui-surface-map.md](./gling-ui-surface-map.md) · [review](https://gregpreece.com/articles/ai-video-editor-gling-review) |
| **Riverside** | Main surface | Beside it | Secondary | [remove a word](https://support.riverside.com/hc/en-us/articles/14488573075741-Remove-a-word-or-phrase-from-the-recording) |
| **Premiere TBE** | Text panel, upper left, with a filter/search | Program monitor | Full NLE timeline (the real editing surface) | [RedShark](https://www.redsharknews.com/how-to-delete-pauses-and-filler-words-with-text-based-editing) |
| **CapCut** | A layout **mode** (Menu → Layout → Transcript-based editing) | — | Full timeline | [CapCut](https://www.capcut.com/resource/edit-video-with-text) |
| **FliCut today** | Left, dominant (`Script.tsx`, 65ch) | Right column, 34% (320–560 px) | Bottom, 160 px, dark, one lane at one zoom | `Editor.tsx` |

FliCut's proportions are already right; Gling, Descript and Riverside agree on transcript-dominant with the preview beside it. The problems are **what each region shows**, not where it sits.

### 2.2 How removed material is shown

| Pattern | Product | Verdict for FliCut |
|---|---|---|
| Grey strikethrough, visible, click to restore | Riverside, Descript *Ignore*, Gling | **Copy** |
| Pauses as inline glyphs sized by length: `•` `••` `•••` | Riverside ([pauses](https://support.riverside.com/hc/en-us/articles/12245776523677-Remove-individual-silences-and-pauses)) | **Copy**: pace becomes visible in the text |
| Pauses as `...` | Premiere ([Juno](https://www.junoschool.org/article/automatically-remove-pauses-filler-words-premiere-pro/)) | Weaker version of the above |
| Suggestions underlined, decisions struck through | Descript fillers (light-blue underline) ([fillers](https://help.descript.com/hc/en-us/articles/10164806394509-Removing-filler-words)) | **Copy**: separates "the engine proposes" from "it is cut", which FliCut's two layers already store |
| Seam mark `¦` where two kept pieces meet, with a per-seam fix | Descript edit boundaries | **Copy**: this is where the loupe opens |
| Show/hide deleted text toggle | Riverside, CapCut; requested for Descript ([request](https://feedback.descript.com/feature-requests/p/toggle-show-hide-ignored-text-in-script)) | Fold into the mode switch (§2.3) |
| Cut vs keep as red/grey blocks on a slim strip, click to toggle, drag edges | Kapwing Smart Cut ([help](https://www.kapwing.com/help/how-to-use-smart-cut/)), TimeBolt | Use on the overview lane, coloured by kind |
| Text simply disappears | Premiere (reported), Descript plain Delete | **Anti-pattern**, and FliCut's obs. #3 (hidden cuts leave blank holes) is a variant |

**Recommendation.** Removed material is always there as a **chip whose colour is the reason**: pause
(gold, `⋯ 0.8s` or dots), filler (amber strikethrough), discarded take (rose, `↺ take 2 of 3`), cut by hand
(blue). In *Watch finished* it collapses to a hairline seam, never a blank block.

### 2.3 Modes and state visibility

- Gling has two view toggles (Show cuts, Skip cuts) persisted in `playbackSettings.json` ([gling-ui-surface-map.md](./gling-ui-surface-map.md) §4). FliCut added a third (inverse cuts). David understood none of the three from the screen (obs. #1–3).
- **Recut** skips highlighted silence live during playback. **TimeBolt** has *Flip Timeline Selection*, which reviews only what is being cut ([features](https://www.timebolt.io/features)).
- Descript's Correct mode (Opt+C) has **no persistent mode indicator**, which is an anti-pattern to avoid ([correct](https://help.descript.com/hc/en-us/articles/10119613609229-Correct-your-transcript)).

**Recommendation.** Use one segmented control, named by the job, with a badge on the player:

| Mode | Script shows | Playback | Player badge |
|---|---|---|---|
| **Watch finished** | Kept words only; seams as hairlines | Skips every cut | `Finished video · 38 cuts skipped` |
| **Review cuts** (default) | Chips and struck words, clickable | Skips cuts | `Review · skipping cuts` |
| **Hear removed** | Removed material highlighted, kept text dimmed | Plays only removed material | Yellow frame, `Hear removed · 51 s` |

A Correct-text mode (§3 job 12) would be a fourth state, with a coloured frame around the script while it is on.

### 2.4 Pace

| Product | Control | Preview before commit |
|---|---|---|
| **Gling** | Pause-threshold slider (max 2 s = keep all) plus padding, shown as "Removes N pauses 3.2s" | Count only |
| **Descript** | *Shorten word gaps*: gaps "more than / between" X are shortened **to** Y (e.g. 200 ms); step through with Auto-advance and **Preview results** (auto-plays the surrounding audio); Shorten one or Shorten all ([shorten](https://help.descript.com/script-editing/shorten-word-gaps)) | **Yes, audible** |
| **Riverside** | "Remove pauses" slider plus *Revert to original*; filler removal is a **toggle** with Smart / Cut / Mute ([pauses](https://support.riverside.com/hc/en-us/articles/13993078729245-Remove-pauses-and-silences), [fillers](https://support.riverside.com/hc/en-us/articles/13364581561245-Remove-filler-words)) | Reversible |
| **Premiere** | Minimum pause length; Delete / Delete all; the 0.1 s floor leaves pauses behind; users ask for "shorten to X" ([forum](https://community.adobe.com/feature-requests-730/feature-request-allow-setting-fixed-pause-duration-after-deleting-pauses-in-text-based-editing-1328765)) | No; destructive bulk delete (**anti-pattern**) |
| **FliCut** | `Pace.tsx`: Gling's slider, padding, toggles, "Removes N pauses, Xs" | Count only; you cannot hear it |

**Recommendation.** Keep Gling's model, which FliCut already matches, and add Descript's two things:
**shorten to** a target (not only remove), and pending changes shown in the script (dashed) that you can
hear with play-around before Apply.

### 2.5 What makes them feel "nice"

From reviews and help pages, the same four habits recur:
1. **Nothing vanishes.** Removed text stays on screen, grey and restorable.
2. **Bulk is a switch, not a verdict.** It is reversible and has per-item exceptions. Descript users revolted over a filler bulk-remove without exceptions: *"I need to now go one word by word over 100s of words just to keep one of them. That's poor UI."* ([canny](https://descript.canny.io/feature-requests/p/bring-back-strikethrough-ignore-on-filler-words-edits))
3. **Two playback lenses**: the finished edit, and only what was cut.
4. **The transcript is home; the timeline is on demand.**

Complaints are the mirror image: markers that don't match the audio (Premiere's
[offset silences](https://community.adobe.com/bug-reports-733/premiere-pro-incorrectly-detects-silences-in-transcript-and-text-based-editing-1554235)),
aggressive cutting that kills deliberate pauses (Gling reviews,
[max-productive](https://max-productive.ai/blog/descript-vs-gling/)), and retake detection eating
deliberate repetition ([Chase Jarvis](https://chasejarvis.com/blog/descript-underlord-ai/)).

---

## 3. The 18 jobs — best in class vs FliCut today vs the gap

Status: ✅ has it · 🟡 partly · ❌ missing. FliCut column read from code at `3fb91bd`.

| # | Job | Best-in-class pattern (product) | FliCut today | Gap |
|---|---|---|---|---|
| 1 | Watch it as the viewer will | Recut live skip; Gling Skip cuts | 🟡 `skipCuts` (⇧K), playback only | Invisible. Make it the *Watch finished* mode with a badge |
| 2 | Read it like a script | Descript / Riverside: the doc *is* the edit | ✅ Script pane, word-snapped selection, Cut/Uncut bubble | Hidden cuts leave holes (obs. #3) |
| 3 | See what the AI took out, and why | Descript underline-vs-strike; Riverside pause dots; Premiere filter by Pauses / Fillers | 🟡 Struck words, pause chips, one "N cuts" count | No reason per cut; no totals by kind |
| 4 | Overrule the AI | Descript AI Tools list (every filler with timestamp and preview; Ignore / Delete per item); Riverside toggle plus per-item restore | 🟡 Click toggles; Pace toggles a kind; overrides list is API-only | No review queue that steps through removed items |
| 5 | Pick the best take | Gling bad-take detection; Descript *Remove retakes* as ignored text; TimeBolt *Look Ahead* strictness | ❌ Scope limit: `cutBadTakes` stored, nothing acts on it | Needs detection plus a "take N of M · keep this" chip |
| 6 | Check a join sounds natural | Avid Space loop in trim mode; Premiere play-around; Descript *Preview results* | ❌ Seek and play by hand | Add play-around (Space in the loupe, ⇧Space elsewhere) |
| 7 | Set the pace | Descript *shorten to* with audible preview; Gling Pace | 🟡 Gling-parity Pace panel with a count | Can't hear it before Apply; no "shorten to" |
| 8 | Set exact start and end | FCP `⌥[ ⌥]`; NLE I/O | 🟡 Whole-timeline trim at the playhead (⇧B / ⇧E) | Per-clip frame-exact in/out: the mock awaiting David's 3 answers |
| 9 | Find a moment | Descript / Premiere transcript search; Descript `#` markers as chapters | 🟡 ⌥←/→ cut jumps | No word search, no next clip, no markers |
| 10 | Move fast | NLE J/K/L; FCP on-screen speed | ✅ J/K/L with reverse, speed badge, K+J/L frame step, `[ ]` speed | Keys taught only in one long hint line |
| 11 | Know where I am | Premiere sequence + source timecode | 🟡 Output timecode on the strip; file name above each paragraph | No source time for the playhead |
| 12 | Fix a misheard word | Descript *Correct* (Opt+C, text only, Correct All) | ❌ Scope limit; where corrections live is an open ADR | Correct mode with a visible frame; `word.correct` verb |
| 13 | Undo anything | Descript version history; Underlord checkpoints with Revert | ✅ ⌘Z / ⇧⌘Z cursor plus restorable history (ADR-0006) | None |
| 14 | Hear clean audio | Descript Studio Sound with on/off preview | 🟡 Export-time choice only; A/B lives in a separate harness | No in-editor A/B |
| 15 | Export and know what I got | Descript / TimeBolt export summaries | ✅ Files, codec, planned vs actual length, LUFS, reveal | Counts by kind could be added |
| 16 | Pick up where I left off | Descript layout per project | ✅ View state stored per edit | None |
| 17 | Let an agent do a pass, then review it | Descript Underlord: checkpoint before each edit, Revert per response; the AI Tools panel and the agent share verbs | 🟡 RPC `cuts.preview` / `cuts.apply` / `overrides.list`; FC-33 conflict notice | No in-window "proposed by the agent" review queue |
| 18 | Fine-grain control | FCP two-up plus `, .`; Resolve audio auto-zoom; Logic geared drag | 🟡 ← → nudge the clip **start** ±1 frame; Z frame-zoom | No edge choice, no two-up, no geared drag. §1.4 |

**Tally**: 6 ✅ · 9 🟡 · 3 ❌. The three ❌ (takes, play-around, correction) are all review jobs.

---

## 4. Agent parity — every key is also a verb

FliCut's RPC today (`src/main`, method names): `edit.create/get/list/set-params/transcribe`,
`cuts.propose/preview/apply`, `segment.set-cut`, `overrides.list`, `export.start/last`, `video.open`,
`context.get/set`, `job.get`, `batch.run`, `settings.get/update`. That is the **decide-and-render** half.
The **precision and review** half has no verbs.

| Verb | UI key / gesture | Does | Status |
|---|---|---|---|
| `cut.select {edit, cut, edge: out\|in\|both}` | `[` `]` `\` | Pick the cut and its edge | new |
| `cut.nudge {cut, edge, by: -2f \| +40ms}` | `,` `.` Shift, geared drag | Move an edge. Returns the new frame, the delta from the proposal and the delta from the nearest word boundary | new |
| `cut.set {cut, edge, at: frame \| word:<id>.start, offset}` | `+2 ⏎`, `W` | Place an edge absolutely or relative to a word | new |
| `cut.inspect {cut, frames: 5, audio: 500ms}` | the loupe | Two-up PNGs, a strip PNG, a waveform PNG, and RMS at each edge. **The agent's loupe**: it can reject a mid-phoneme or mid-blink join before committing | new |
| `cut.preview {cut, preroll: 1s, postroll: 1s}` | Space | Render the join to a short clip | new |
| `edit.trim {clip, in?, out?, frames?}` | `I` / `O` | Per-clip in/out (spec in the trim mock) | new |
| `take.choose {group, keep}` | click a take chip | Keep one take, mask the rest | new (needs detection) |
| `word.correct {element, text}` | Correct mode | Text only; the cut is not touched | new (needs the open corrections ADR) |
| `history.list` / `history.restore {sha}` | ⌘Z, history panel | Same cursor as the window, so an agent pass is one undo step (Descript's checkpoint-before-edit) | new over RPC |
| `segment.set-cut` | click a word or chip | Keep or remove one segment | exists |
| `cuts.preview` / `cuts.apply` | Pace panel | Dry run, then apply | exists |
| `overrides.list` | review queue | Where the human disagreed | exists |
| `export.start` | Export | Render | exists |

**Rules for keeping the two surfaces one model**: every verb is the pure `layers.ts` function the key
calls (the store is the only writer); nudges are relative and return absolute results; each agent call is
one history entry. Descript's Underlord already works this way, with the AI Tools panel and the chat
sharing one verb set ([Underlord](https://help.descript.com/getting-started/underlord-beta-your-ai-co-editor-in-descript),
[revert](https://help.descript.com/hc/en-us/articles/36958274409357-Revert-or-rollback-changes-made-by-Underlord-beta)).

---

## 5. Recommended direction for FliCut (10 bullets)

Ordered by how much each item fixes David's "nothing feels nice".

1. **Build the cut loupe first** (§1.4). It answers #18 and it is where "nice" is felt: select a cut, see two frames and a zoomed waveform, nudge with `,` `.`, and hear it with Space.
2. **Nudge by edge, not by clip start.** `[` `]` `\` pick out, in or both; `,` `.` move 1 frame and Shift moves 5. Free ← → to move the playhead, as the trim mock proposes.
3. **Gear every drag.** Drags that change an edit happen only in the loupe, at a fixed 12 px per frame (⌥ for 40). A timeline drag stays a scrub.
4. **Replace show / skip / inverse cuts with one mode switch**: Watch finished · Review cuts · Hear removed, with a badge on the player (§2.3).
5. **Collapse removed material into chips whose colour is the reason** (pause, filler, take, by hand). No blank holes; double-click expands (§2.2).
6. **Split the timeline into two lanes**: the whole edit with cut marks coloured by kind and a window box, and a fixed-zoom detail lane that follows the playhead (Resolve cut page).
7. **Add play-around**: ±1 s around the playhead or the selected cut, looping while held. Checking joins is half of reviewing.
8. **Make bulk changes previewable and reversible.** Pace can shorten *to* a target and shows pending changes in the script before Apply, and a Review queue steps through removed items with auto-advance and auto-play (Descript).
9. **Group the toolbar by job and teach keys in place.** Each control shows its key in its tooltip and in the inspector, instead of one long hint line; show both clocks (finished time, source file @ source time) under the player.
10. **Give every key a verb** (§4), so an agent pass and a human pass are the same operations and the agent can *see* a join through `cut.inspect`.

**Not recommended**: a full Precision-Editor filmstrip view (too heavy for a talking-head rough cut), or a timeline zoom-toggle. The loupe is always zoomed, so it makes both unnecessary.

---

## What this research did NOT establish

- **No product was driven.** Everything comes from documentation, help pages, reviews and FliCut's source. FliCut was not launched (David was using it), so the §3 status is a code reading, not an observed session.
- **Gling's UI detail** beyond our own teardown comes from third-party reviews, and "Gling has no nudge" is unverified.
- **Adobe** pages were read through indexed snippets (403). **Avid, Pro Tools, CapCut and Resolve's current key defaults** come from secondary sources in places; the Resolve cut-page quotes are official.
- **No user testing.** "What feels nice" is taken from reviews and complaints, not from watching David use a loupe. The artifact's loupe is a sketch with synthetic frames and waveforms, meant to be felt, not measured.
- **12 px per frame and ±0.6 s** are starting values chosen for the sketch, not measured optima.

## Related

- [gling-ui-surface-map.md](./gling-ui-surface-map.md): Gling's controls and the two cut layers.
- [close-or-exceed.md](./close-or-exceed.md): where FliCut matches or passes Gling.
- [../filmstudio/verdict.md](../filmstudio/verdict.md): FilmStudio's timeline model, for FliEdit rather than FliCut.
- Artifacts: FliCut Editor Blueprint <https://claude.ai/artifact/LPsaH4jcz2rhS2WxCvTSFg> · the trim mock <https://claude.ai/artifact/GoVGaZPzBq28U86c3yBJJy> · [FliCut Trim Options](../ARTIFACTS.md#flicut-trim-options).



---

