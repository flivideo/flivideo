<!-- FliVideo source bundle · FilmStudio study — verdict first (FliEdit blueprint; overlays via HyperFrames + FliTools; FliGate is an OPEN proposal) · generated from ~/dev/ad/brains/filmstudio/verdict.md, ~/dev/ad/brains/filmstudio/flivideo-mapping.md, ~/dev/ad/brains/filmstudio/overlay-comparison.md, ~/dev/ad/brains/filmstudio/capability-inventory.md -->


# RxFilmStudio — phase-3 verdict

**Purpose**: The decision layer of the FilmStudio study: what FilmStudio is to FliVideo, and what we take from it.

**For Agents**:
- Read this first when anyone asks "what did the FilmStudio study conclude" or "should FliEdit copy FilmStudio"
- Detail behind every line: [capability-inventory.md](./capability-inventory.md) (what it does, with proof), [flivideo-mapping.md](./flivideo-mapping.md) (where each piece goes), [overlay-comparison.md](./overlay-comparison.md) (overlays)
- ⛔ Obey the licence rule below before touching any FilmStudio file
- `fires_via: none` — the licence rule is captured here; nothing enforces it mechanically

---

## ⛔ Licence rule

> **RxFilmStudio's repo has no licence (all rights reserved): we read it and borrow ideas, architecture and file formats; we never copy its code into any Fli repo.**

Evidence: no `LICENSE` file, GitHub reports `license: null` (see [tech-notes.md](./tech-notes.md) §licence). This applies to every sketch in [flivideo-mapping.md](./flivideo-mapping.md): each is a re-design in our stack (TypeScript, fli-core, FliCast's PixiJS+WebCodecs, ffmpeg, HyperFrames, mlx), not a port.

## Verdict: mixed — a blueprint for FliEdit's model, a donor to several apps, and a shell we discard

| Part of FilmStudio | What it is to us | Goes to |
|---|---|---|
| Local sequence engine | **A blueprint for the missing FliEdit** — copy the MODEL, not the ENGINE | FliEdit |
| Screen recording extras, transcription hardening, suite rules | **A feature donor** | FliCast, FliTools, fli-core, the new FliGate |
| Marketplace, credits, accounts, in-app agent, Simple-mode wizard | **Its own thing** — a commercial shell | Nothing |

**The blueprint.** FilmStudio's sequence engine supplies the multi-track Timeline JSON with overlay and caption lanes, whole-timeline get/set that re-validates every clip, ripple and linked-clip edits, inserting a take as linked tracks, one compositor for preview and export, overlays as pre-rendered alpha clips re-rendered before export, and caption delivery at render (burn-in, embedded or sidecar). FliEdit copies that **model** but replaces the **engine**: AVFoundation, Core Image and SwiftData become `fli.edit.<name>.json`, FliCast's PixiJS+WebCodecs compositor and ffmpeg. FliEdit must also add what FilmStudio lacks: **markers and chapters**.

**The donor.** FliCast gets Record Actions, Replay-and-Record and crash checkpoints. FliTools gets glossary bias, chunking, timestamp validation, script alignment, media normalise/probe and transcript search. fli-core gets the source-URI grammar, the propose/approve review gate, format-version migration, persisted task handles, a caption serializer and the authorize()-on-every-door rule. A new **FliGate** would get one MCP door for the suite — ⚠️ **PROPOSAL, not settled**: a suite architecture decision for David (2026-09-24), not a finding of this study.

**The architecture is inverted relative to ours.** FilmStudio puts the agent *inside* the app, behind an MCP registry that external clients reach unfiltered (#311: any token holder can post real OS input and read screenshots). The suite keeps Claude Code *outside*, behind per-app doors and ★ fences. We take the tools, not the embedding.

## Where does compute happen?

Answered by the method from [../screen-studio/](../screen-studio/): **local compute can be automated and replicated; server compute can be neither.**

| | Rows (of 398) | Examples | Our call |
|---|---|---|---|
| **Local** (on the Mac) | 266 | Timeline model and validation, linked-track insert, preview = export compositor, caption delivery, render caches, alpha overlays, action logging and replay, crash recovery, WhisperKit, Apple translation, CLI agent paths | **Everything we take comes from here** — re-implementable in our stack |
| **Server** (RxLab, credit-metered) | 70 | Veo, Lyria, Gemini/Azure TTS, image generation, cloud transcription, chat proxy, marketplace, billing | **All rejected** |
| **Hybrid** | 57 | Local orchestration of a server call (e.g. Azure SSML built locally, synthesised remotely), marketplace install | Taken only for the local half |
| Unknown | 5 | Not built or not traced | — |

The synthesis pass put the server-dependent share at "roughly 35–40% of features"; by row count, server + hybrid is 127 of 398 (32%). Either way it is the half we don't want.

- Server work cannot be automated or replicated outside an RxLab account, is metered by credits, and is gated behind their account.
- If a generative capability is ever wanted, it becomes an **optional FliTools task on David's own key or local** (Kokoro TTS, nano-banana images) — never an RxLab route.
- The suite's only standing remote hop stays **FliTools → Groq on David's key, with an mlx fallback**.

**Not verified against a FilmStudio run**: engine claims come from its source code and its `Validation.md`. HyperFrames' transparent-output path for `compile-overlay.py` is untested.

## Top ten capabilities to take

| # | Capability | Target app | Why |
|---|---|---|---|
| 17 | `sequence_set_timeline` → `sequence.set` | FliEdit | Unanimous #1: an agent reads the whole timeline, edits it and writes it back with every clip re-validated — one verb covers most edits |
| 68 | Timeline data model (tracks, clips, sources) → `fli.edit.<name>.json` | FliEdit | The multi-track model with overlay and caption lanes; the foundation FliEdit is missing and FliCut deliberately lacks |
| 172 | Overlays as pre-rendered alpha clips | FliEdit | The FilmStudio lesson the overlay study adopts; the simple, robust path to "brings everything together with overlays" |
| 105 | Caption delivery at render (burn-in / embedded / sidecar) | FliEdit | Burn-in for shorts, sidecar for YouTube, on the final timeline — FliCut excludes captions on purpose |
| 49 | Insert a cast as linked per-component tracks | FliEdit | The bridge that brings FliCast screencasts into the combined edit |
| 330 | Source-URI grammar `<kind>:<ref>` + resolver | fli-core | Lets FliEdit place cuts, casts, overlays and captions without importing other apps |
| 189 | Brand glossary as Whisper prompt | FliTools | Fixes misheard AppyDave, FliCut, Claude, BMAD at the source, for every downstream app |
| 33 | Propose → approve ★ review gate | fli-core | Agents make bulk caption and edit fixes under the human-only fence; generalises Teletubby's `pending.approve` |
| 295 | Replay-and-Record | FliCast | Re-shoot a demo after a UI change without redoing it by hand; start stays human-only |
| 0 | One authenticated MCP door from the OpenRPC documents | FliGate (new — proposal, needs David's ruling) | Ends the "six doors, five dialects" adapter cost, with `authorize()` enforced |

## Overlay owner

- **FliTools owns overlay generation** — a headless render endpoint beside transcription: `overlay.create`, `overlay.render` (task: `compile-overlay.py` → HyperFrames; alpha layer or composited mp4; content-hash cache `vNNN-<hash8>`; pinned HyperFrames version), `overlay.frames` (PNG screenshots the agent checks before reporting).
- **FliEdit — or FliCut until FliEdit exists — owns review and placement**: the overlay sheet table plus preview or filmstrip is the human gate; approved overlays are placed as `overlay:<name>` alpha clips on an overlay track and re-rendered if stale before export.
- **Sheet drafting stays in skills**: `video-editor:overlay-sheet` and `overlay-compile`.
- **FliCast keeps only its screen-recording keystroke and caption overlays**, which should later read brand tokens.
- **No FliMotion app. No Remotion.** Full reasoning: [overlay-comparison.md](./overlay-comparison.md).

## Remotion licence consequence

- **For the plan above: none.** Nothing in the proposed stack imports `remotion`.
- **For a hypothetical FliEdit built on Remotion**: free while at most 3 people (David, Jan, Mary) touch its codebase. From a fourth person on, a Company Licence is mandatory, and a video editor or automated pipeline counts as "Remotion for Automators": $0.01 per render, minimum $100 a month, plus $25 a month per Remotion developer; under the (not yet in force) 5.0 terms, mandatory telemetry or monthly reporting, and a one-year licence tail after each release if distributed.
- **FilmStudio itself** bundles `remotion` 4.0.459 but its `THIRD-PARTY-NOTICES.txt` has 0 hits for "remotion" — another reason not to lift its engine.
- Detail and sources: [overlay-comparison.md](./overlay-comparison.md) §4.



---


# RxFilmStudio → FliVideo mapping

**Purpose**: For each FilmStudio capability, say where it belongs in the FliVideo suite (or that we don't want it), what it would look like as an agent-drivable capability in the fli-core contract style, and roughly how big it is.

**For Agents**:
- Use this when designing **FliEdit**, or when asked "should app X take FilmStudio feature Y"
- Row `#` = the row in [capability-inventory.md](./capability-inventory.md) §"Source-grounded capability buckets" — look there for what the feature does and its proof file
- The call summary lives in [verdict.md](./verdict.md); the overlay ownership reasoning in [overlay-comparison.md](./overlay-comparison.md)
- ⛔ Licence rule: **RxFilmStudio's repo has no licence (all rights reserved): we read it and borrow ideas, architecture and file formats; we never copy its code into any Fli repo.** Every sketch here is a re-design in our stack, not a port

---

## How this was produced

Three independent mapper passes (workflow lens, architecture lens, a third tie-breaker) each mapped all rows; a synthesis pass resolved disagreements (see the end of this file). The overlay study ([overlay-comparison.md](./overlay-comparison.md)) was applied on top and **overruled all three mappers on one point**: there is no FliMotion app, overlay rendering is a FliTools endpoint.

**Notation** (fli-core contract style): `verb {args}` · `query` = read-only · `command` = writes · `task` = long-running job with status · `reversible-write` = undoable · ★ = human-only verb (refuses agent principals) · refusals are typed codes. Effort: S (≤1 day) · M (days) · L (a week or two) · XL (bigger). Effort is not given for "no" rows.

## Summary

| Wanted | Rows |
|---|---|
| ✅ yes | 108 |
| 🟡 maybe | 79 |
| ❌ no | 211 |

| Target (yes + maybe rows) | Rows | What it gets |
|---|---|---|
| **FliEdit** (to be built) | 80 | The whole multi-track sequence model, verbs, compositor, captions delivery, export, markers/chapters, overlay placement and review |
| **FliTools** | 45 | Overlay render endpoint (HyperFrames), transcription hardening (glossary, chunking, validation, alignment, versions, search), media normalise/probe, optional own-key TTS/image |
| **FliCast** | 31 | Record Actions + Replay-and-Record, crash checkpoints, capture-source extras; many rows are "already exists, verify" |
| **fli-core** | 17 | Suite rules: source-URI grammar, propose/approve gate, write policy, format-version migration, persisted task handles, caption serializer, authorize() on every door |
| **FliStudio** | 8 | Library extras: kind filter, copy-vs-reference import, asset probe, trash |
| **FliGate** (invented) | 3 | One MCP door for the suite |
| FliCut · FliHub · Scribe | 1 each | Word nudge · take hide · delivery-cue markup |
| Teletubby · Storyline | 0 | No row lands here. Teletubby benefits indirectly (its `pending.approve` pattern is generalised into the fli-core review gate #33; it displays Scribe's delivery cues #231). Storyline has no counterpart in FilmStudio, which has no story-planning layer |

Duplicate rows (the same capability seen from two slices) are marked "Duplicate of #n" and counted once in spirit, twice in the table.

## Mapping by bucket

### Capture and recording

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 40 | recording_sources | FliCast | ✅ yes | recording.check (agent-open query) adds permission state; recording.devices stays ★ | S | Mostly exists; adds an agent pre-flight |
| 41 | recording_focus (observe the user's focused window) | none | ❌ no | — | — | Unanimous: privacy risk |
| 42 | recording_screenshot | FliCast | 🟡 maybe | capture.screenshot {windowId/bundleId, cursor?} command, external-side-effect -> png into project | S | Stills for overlays and thumbnails; overlaps ScreenTour |
| 43 | recording_get / recording_configure | FliCast | ✅ yes | recording.arm / recording.defaults.set exist; add sourceKind, windowIDs, fps, countdown | S | Largely exists |
| 44 | recording_start / recording_control | FliCast | 🟡 maybe | recording.pause ★ / recording.resume ★ (human-only like start/stop) | M | Pause is a known gap; start stays human-only (S8) |
| 49 | recording_insert_take | FliEdit | ✅ yes | sequence.insert-cast {project, sequence, cast, start?} command -> rendered cast or per-component linked tracks under one linkGroup | M | Unanimous: bridge from FliCast into the combined edit |
| 50 | recording_pet | none | ❌ no | — | — | Mascot |
| 273 | Screen Recording footage item + three run modes | FliCast | ✅ yes | recording.arm {mode content/actions/replay} | M | Made yes as the arming half of #295 |
| 274 | Capture sources: display / window(s) / area / iOS device | FliCast | 🟡 maybe | recording.arm {source display/window/area/iosDevice} | M | Area capture helps; iOS is rare |
| 275 | ScreenCaptureKit video pipeline | none | ❌ no | — | — | RecordKit already covers this |
| 276 | Multi-window take lifecycle | FliCast | 🟡 maybe | multi-window capture, one track per window | M | Rare |
| 277 | Webcam capture (multiple cameras) | FliCast | 🟡 maybe | cameraIDs[] | S | Could add a Pocket 4 angle |
| 278 | Microphone capture (multiple mics) | none | ❌ no | — | — | One mic |
| 279 | Per-app and system audio via Core Audio process taps | FliCast | 🟡 maybe | recording.arm {audio perApp[]/system}: one track per app + system | M | Demo audio ducked separately from voice |
| 280 | iOS device screen + device audio capture | FliCast | 🟡 maybe | folded into #274 (iosDevice) | M | Duplicate of #274 |
| 281 | Session controls: countdown, pause/resume, stop, change sources mid-take | FliCast | 🟡 maybe | recording.pause ★ / resume ★ as new segments; change-sources ★ while paused | M | Known gap |
| 282 | Shared host-clock A/V synchronisation | FliCast | 🟡 maybe | every writer offset onto one host clock, recording its start offset | S | Check against the unfixed ~44 ms audio lag |
| 283 | Crash / interruption recovery | FliCast | ✅ yes | fragmented MOV + 2 s Session checkpoint; project.recover query on open -> 'Interrupted' take | M | Unanimous: a take cannot be redone |
| 284 | Permission guide | none | ❌ no | — | — | recording.permissions ★ exists |
| 285 | Input previews (camera/mic/window) | none | ❌ no | — | — | Minor UI |
| 286 | Menu bar 'Quick Recording…' | FliCast | 🟡 maybe | menu bar quick-record into the current FliStudio project | S | Convenience |
| 287 | On-screen chrome kept out of the capture | FliCast | 🟡 maybe | exclude own chrome windows from capture (verify) | S | Probably handled already |
| 289 | Window / app screenshots | FliCast | 🟡 maybe | see #42 | S | Duplicate of #42 |
| 328 | ScreenRecordingProject / RecordingTake data | none | ❌ no | — | — | FliCast has its own model |
| 329 | Recording crash recovery from Session.json checkpoints | FliCast | ✅ yes | see #283 | M | Duplicate of #283 |
| 395 | RxPet recording mascot overlay | none | ❌ no | — | — | Mascot |

### Screen-action logging and auto-zoom

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 45 | recording_actions_edit (action script) | FliCast | ✅ yes | actions.edit {cast, op replace/insert/update/delete/reorder} command, reversible-write; reorder re-times | M | Base for repeatable screencasts |
| 46 | recording_perform_action (agent drives other apps' UI) | none | ❌ no | — | — | Agent synthesising input into other apps breaks S8 (mapper 1's maybe overruled 2-1) |
| 47 | recording_presentation (cursor, zoom, camera) | FliCast | ✅ yes | cursor.* / zoom.* / layout.* exist | S | Already covered |
| 48 | recording_shortcuts (keystroke subtitle cues) | FliCast | ✅ yes | overlay.keystrokes.set exists; optional per-clip cue style | S | Already covered |
| 99 | Zoom-lane clips (materialised auto-zoom) | FliCast | ✅ yes | zoom.* / zoom.regenerate exist; verify zooms are editable clips (move/trim/split, scale 1-8, focus, follow) | S | Mappers 2-3 say FliCast has editable zooms; verify, don't rebuild |
| 100 | Per-clip recording presentation and shortcut subtitles on the timeline | FliEdit | 🟡 maybe | a placed cast keeps its FliCast presentation by reference; prefer the rendered export | M | Re-owning cursor/zoom in FliEdit would duplicate FliCast |
| 291 | Pointer + click logging (all modes) | none | ❌ no | — | — | FliCast already logs the pointer |
| 292 | Keyboard shortcut capture → shortcut subtitle lane | FliCast | ✅ yes | verify keystroke capture is opt-in and modifier-only (⌘/⌃ combos) to a cue lane | S | Mostly exists; confirm the privacy-safe filter |
| 293 | Record Actions: editable action document | FliCast | ✅ yes | actions document per cast: actions.get/edit; move/click/drag/scroll/key/text; window-relative coords + AX ids | L | Base for re-shooting demos |
| 294 | Recording Movement editor | FliCast | 🟡 maybe | UI movement editor | M | Agent path first |
| 295 | Replay and Record (Mac automation) | FliCast | ✅ yes | recording.replay ★ {cast} task: runs actions while capturing a new take; start stays human-only (S8) | L | Re-shoot a demo after a UI change (mapper 3: maybe, XL, brittle) |
| 296 | Scripted capture-control, wait and screenshot actions | FliCast | ✅ yes | action kinds wait, waitForWindow, waitForElement, pause/resumeCapture | M | Needed to make #295 reliable |
| 297 | Replay execution log in the take | FliCast | ✅ yes | take stores the executed-actions log with actual times (audit) | S | Audit what the replay actually ran |
| 298 | iOS device automation via Appium/XCUITest | none | ❌ no | — | — | Appium out of scope |
| 299 | Synthetic cursor re-render | none | ❌ no | — | — | cursor.* exists |
| 300 | Auto-zoom from clicks (click-burst algorithm) | FliCast | 🟡 maybe | compare the 2.5 s window / 0.6 s merge constants with zoom.regenerate | S | Tuning reference only |
| 301 | Zoom lane: editable zoom clips + render evaluation | FliCast | ✅ yes | see #99 | S | Duplicate of #99 |
| 302 | Legacy presentation zoom intervals + render-time click synthesis | none | ❌ no | — | — | Legacy |

### Timeline and sequence editing

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 16 | sequence_list / sequence_create / sequence_get | FliEdit | ✅ yes | sequence.create {project, name, size/aspect, fps} command (default tracks T1 overlay, V1, A1, A2, C1); sequence.list/get query -> timeline JSON; refusals not-a-project, video-invalid | L | Unanimous. The core object of the missing Stage-3 app |
| 17 | sequence_set_timeline | FliEdit | ✅ yes | sequence.set {project, name, timeline} command, reversible-write, idempotent, one undo step; every clip re-inserted through editor rules; refusals overlap, track-kind-mismatch, video-not-found, unknown-definition | M | Unanimous #1 pick: read the JSON, edit it, write it back with rules enforced |
| 18 | sequence_add_track / sequence_reorder_tracks | FliEdit | ✅ yes | track.add {kind video/audio/caption/overlay}, track.reorder {ids[]} command | S | Overlays and captions need lanes; zoom lane stays in FliCast |
| 19 | sequence_add_clip / sequence_remove_clip | FliEdit | ✅ yes | clip.add {source uri, track, start?, in?, duration?, ripple?} / clip.remove {id, ripple?} command, reversible-write | M | Granular placement verbs alongside sequence.set |
| 20 | sequence_link_clips / sequence_track_alias | FliEdit | ✅ yes | clip.link {ids[]} / clip.unlink; track.alias {id, alias} command | S | Keeps a cast's screen, camera and audio moving together |
| 68 | Timeline data model (tracks, clips, sources) | FliEdit | ✅ yes | fli.edit.<name>.json: zod Timeline{size, fps, bg, tracks[kind video/audio/overlay/caption, name, alias, muted, enabled], clips{source uri, start, duration, in, rate, volume, opacity, linkGroup}}; schema exported from fli-core | M | The multi-track model FliEdit lacks; FliEdit owns it, schema in fli-core for interchange |
| 69 | Sequence create / settings (resolution, fps, background) | FliEdit | ✅ yes | sequence.create defaults size/fps from fli.studio.json aspect intent; presets 16:9, 9:16, 1:1, 4K; fps 25/30 | S | Gives the aspect intent real behaviour, incl. 9:16 shorts |
| 70 | Add / delete / reorder / alias / pin tracks | FliEdit | ✅ yes | UI track headers: add, reorder, alias, pin, delete (★ when the lane has clips) | M | David must be able to review an agent-built edit |
| 71 | Place footage on timeline (drag/drop, add clip) | FliEdit | ✅ yes | UI drag-drop with nextFreeStart; agent path is clip.add | M | Basic placement |
| 72 | Ripple insert (agent only) | FliEdit | ✅ yes | clip.add {ripple:true} splits the straddling clip and shifts the rest | S | Inserting a CTA or b-roll mid-video |
| 73 | Move clips (single and group, lane change) | FliEdit | ✅ yes | clip.move {ids, delta, lane?} command, all-or-nothing; refusal lane-incompatible | M | Core editing |
| 74 | Trim (leading/trailing edges) | FliEdit | ✅ yes | clip.trim {id, edge, to} command, bounded by source, neighbours and one frame | M | Core editing |
| 75 | Blade / split | FliEdit | ✅ yes | clip.split {id, at} command; linked clips split together | S | Core editing |
| 76 | Delete and ripple delete | FliEdit | ✅ yes | clip.remove {ids, ripple?}; attached transitions removed | S | Core editing |
| 77 | Speed change / retime | FliEdit | 🟡 maybe | clip.speed {id, pct/targetDuration} command | S | Occasional; FliCast already speeds casts |
| 78 | Reverse playback | none | ❌ no | — | — | No use in tutorial content |
| 79 | Selection model (click, additive, marquee, select all) | FliEdit | 🟡 maybe | UI selection: click, additive, marquee, select all | M | Secondary to the agent path |
| 80 | Link / unlink clips | FliEdit | ✅ yes | see #20 | S | Duplicate of #20 |
| 81 | Enable/disable clips and tracks | FliEdit | ✅ yes | clip.enable / track.enable {bool} command; disabled items skipped by render and captions | S | A/B an overlay without deleting it |
| 82 | Snapping | FliEdit | 🟡 maybe | UI snapping to clip edges and 0, frame quantise | S | UI nicety |
| 83 | Timeline zoom and skimming | FliEdit | 🟡 maybe | UI zoom + skim | S | UI nicety |
| 84 | Markers (absent) | FliEdit | ✅ yes | marker.add/list/remove; chapters.generate query from transcript -> MP4 chapters + YouTube chapter text for FliYLO | M | Unanimous: FilmStudio has no markers; YouTube chapters come from the final timeline |
| 85 | Align caption clip with original audio | FliEdit | 🟡 maybe | caption clips bound to their source clip, following its moves and trims | S | Likely unneeded if captions derive from the edit (#27) |
| 86 | Undo / redo | FliEdit | ✅ yes | history.undo/redo/list, principal-attributed snapshots covering agent edits (FliCast pattern) | M | People and agents share one undo; FilmStudio's agent edits are not undoable |
| 90 | Linear timeline editor window | FliEdit | ✅ yes | UI: library, viewer, inspector, timeline panes; layout in fli-core window-state | L | The review surface for what agents built |
| 91 | Clip inspector (picture, audio, timing) | FliEdit | ✅ yes | clip.set {fit, scale, offset, opacity, volume} command + inspector | M | Positions overlays and picture-in-picture |
| 92 | Audio mixing: clip volume, track mute, waveform drag | FliEdit | ✅ yes | clip.set {volume 0-2}, track.mute command; waveform UI | M | Music beds under voice |
| 93 | Audio level meter | FliEdit | 🟡 maybe | UI peak meter | S | FliCut arms already handle loudness |
| 94 | Playback engine (composition player) | FliEdit | ✅ yes | preview compositor reusing FliCast PixiJS+WebCodecs at 1280 edge; frame-exact seek | XL | Heaviest item. Reuse FliCast's engine, not AVFoundation. All local |
| 95 | Layered live preview (Remotion live in WebKit) | FliEdit | 🟡 maybe | live overlay layers in the viewer when no effects are active | L | Deferred; pre-rendered alpha (#172) comes first |
| 96 | Viewer transport | FliEdit | ✅ yes | UI transport: play, frame step, scrub | S | Basic |
| 97 | Clip filmstrip thumbnails | FliEdit | 🟡 maybe | filmstrip cache per source (FliCast preview.thumbnails precedent) | S | Nicety |
| 98 | Capability gating per footage type | FliEdit | ✅ yes | per-source-kind capability flags (cut, speed) checked by every verb; refusal operation-unsupported | S | Typed refusals when kinds are mixed |
| 138 | Apply template to film | FliEdit | 🟡 maybe | see #53 | M | Duplicate of #53 |
| 171 | Remotion clips on the timeline (live layered stage) | FliEdit | ✅ yes | source uri overlay:<name> placed on an overlay track; resolves to the latest FliTools render | M | Overlays as clips on a track — the core FilmStudio lesson |
| 172 | Cached ProRes-alpha preview fallback | FliEdit | ✅ yes | overlay clips composite the pre-rendered alpha layer; stale -> placeholder | S | Unanimous: the simple, robust path |
| 208 | Caption clips on a sequence timeline (agent) | FliEdit | ✅ yes | clip.add {source captions:<set>, track C1} | S | Needed for burn-in |
| 303 | Insert take as linked tracks | FliEdit | ✅ yes | see #49 | M | Duplicate of #49 |
| 304 | Link/unlink clips and track aliases (recording) | FliEdit | ✅ yes | see #20 | S | Duplicate of #20 |
| 319 | SequenceProject timeline storage | FliEdit | ✅ yes | see #106 | S | Duplicate of #106 |
| 320 | Timeline undo: window UndoManager vs agent edits | FliEdit | ✅ yes | see #86 | S | Duplicate of #86 |
| 347 | TimelineFocus: playhead follows the agent | FliEdit | ✅ yes | see #87 | S | Duplicate of #87 |

### Effects

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 103 | Clip effects and transitions on the timeline | FliEdit | ✅ yes | transition.add {clip, edge/join, kind dissolve/fade/wipe, duration} command | M | Overlay fades and occasional dissolves (2 of 3 yes) |
| 109 | Built-in effects (3) | FliEdit | 🟡 maybe | effect.add {clip, brightness/saturation/blur} bypassable stack | S | Blur behind text is the main use |
| 110 | Built-in transitions (3) | FliEdit | ✅ yes | transition kinds: dissolve, fade-through-colour, wipe (ffmpeg xfade) | S | The minimum set |
| 111 | Effect target rule | FliEdit | 🟡 maybe | effects only on picture tracks; refusal effect-target-invalid | S | Only if effects are built |
| 112 | Effects & Transitions browser panel | FliEdit | 🟡 maybe | UI effects browser | S | Only if humans apply effects themselves |
| 113 | Transition drop targets: In / Out / Join | FliEdit | 🟡 maybe | UI in/out/join drop zones | S | UI detail |
| 114 | Joined-clip linking and protected edits | FliEdit | 🟡 maybe | joined clips edit as one; refusal would-break-join | S | Only if transitions are built |
| 115 | Effect/transition inspector | FliEdit | 🟡 maybe | UI effect inspector; one undo step per gesture | S | Secondary |
| 116 | Unknown-definition passthrough and export gate | FliEdit | 🟡 maybe | unknown effect passes through in preview; export and agent writes refuse unknown-definition | S | Good refusal pattern if effects exist |
| 117 | Shared Core Image compositor (preview = export) | FliEdit | ✅ yes | principle: one compositor serves preview, frame and export | L | Unanimous: preview must equal export (already FliCast's lesson) |
| 118 | Installable CIFilter descriptor effects/transitions | none | ❌ no | — | — | Marketplace Core Image descriptors |
| 119 | Admin effect/transition descriptor editor | none | ❌ no | — | — | Admin |
| 211 | Caption styling | FliEdit | ✅ yes | captions.style.set {font, size, colour, bg, stroke, position}; default from fli-core brand caption tokens (shared with FliCast style) | M | Branded captions; tokens live in fli-core |
| 305 | Camera picture-in-picture presentation | FliCast | 🟡 maybe | layout.camera keyframes + follow-zoom | S | Animated picture-in-picture |
| 306 | Timed visibility intervals | FliCast | 🟡 maybe | layer.visibility {layer, from, to} | S | Hide the camera for a section |
| 386 | Effect/transition descriptor format | none | ❌ no | — | — | Marketplace format |

### Captions and transcription

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 27 | caption_create | FliEdit | ✅ yes | captions.create {project, sequence, from: cut:<name>/transcript ref} command: maps FliCut/FliTools word timings onto the edit timeline | S | Captions must follow the final timeline; FliCut excludes them |
| 28 | caption_transcribe | FliTools | ✅ yes | transcribe.run exists; record a version per run (engine, model, glossary hash, date); never overwrite without force_save | S | Only the versioning is new |
| 29 | caption_versions | FliTools | 🟡 maybe | transcript.versions {media} query; transcript.activate {media, n} command | M | Useful once Groq and mlx results or glossary re-runs coexist |
| 30 | caption_translate | FliTools | 🟡 maybe | translate.run {transcript, lang, scope missing/all} task, external-side-effect (chat.* on own key or Apple on-device) | M | Content is English; only for the fli.studio.json languages intent |
| 31 | caption_list_segments / caption_search_segments | FliTools | ✅ yes | transcript.search {project, query, context?} query; ignores case, accents, punctuation; returns media + ms | S | Unanimous: find where X is said across every take |
| 32 | caption_update_segment | FliEdit | 🟡 maybe | caption.update {sequence, index, text?/start_ms?/end_ms?} command, reversible-write; word timings re-matched | S | Fix words at final-caption level without touching the FliCut cut |
| 33 | caption_propose_edits (review gate) | fli-core | ✅ yes | <family>.propose {edits[]} writes nothing -> pending queue; pending.list query; pending.approve ★ / pending.reject ★ (human:ui); generalises Teletubby pending.approve | M | A suite rule (2 of 3); FliEdit captions are the first consumer |
| 34 | caption_set_speakers | none | ❌ no | — | — | Single speaker |
| 101 | Clip context-menu host actions (captions, lyrics) | none | ❌ no | — | — | Tied to narration and lyrics; the captions half is #27 |
| 105 | Caption clips: delivery at render (burn-in / embedded tx3g / sidecar) | FliEdit | ✅ yes | export.start {captions burn/embed (mov_text/tx3g per lang)/sidecar srt/vtt/none} | M | Unanimous: burn-in for shorts, sidecar for YouTube |
| 178 | Captions library item (CaptionProject) | FliEdit | 🟡 maybe | caption set item keyed to a source transcript/cut | S | FliTools transcript/1 may already fill this role |
| 179 | On-device transcription (WhisperKit) | FliTools | ❌ no | exists: mlx_whisper | — | Already exists |
| 180 | Whisper model manager | FliTools | 🟡 maybe | tools.engines query: engines, installed mlx models and sizes; RAM guard refuses insufficient-memory | S | RAM guard matters (mlx on long audio can take 17 GiB) |
| 181 | Cloud transcription via RxLab server (OpenAI / Azure / Gemini) | FliTools | ❌ no | — | — | Groq + mlx is enough; credit server route is out |
| 183 | Upload audio prep: compression + chunking | FliTools | ✅ yes | inside transcribe.run: 16 kHz mono re-encode, chunk ≤10 min or 24 MB, stitch onto one timeline | S | Unanimous: works around Groq's upload limit |
| 184 | Timing validation + fallback provider | FliTools | ✅ yes | validate monotonic, in-range timings; retry on mlx or repair + warning in meta | S | Unanimous: bad timings break FliCut's word-level cuts |
| 185 | Transcript versions | FliTools | 🟡 maybe | see #29 | M | Duplicate of #29 |
| 186 | Narration captions (script-aligned timings) | FliTools | ✅ yes | align.run {media, script} task -> script words take ASR timings | M | Unanimous: captions carry exact Teletubby/Scribe wording |
| 187 | Auto-captions on narration generation | none | ❌ no | — | — | Depends on TTS |
| 188 | Sentence cue building | fli-core | ✅ yes | cuesFromWords(words, maxChars): sentence cues at word boundaries; part of serializeCaptions (#35) | S | Split three ways; architecture lens: a shared pure rule |
| 189 | Glossary / terms (spelling bias) | FliTools | ✅ yes | brand glossary (canonical spellings + mishearings) stored in brand settings; passed as Whisper prompt to Groq and mlx | S | Unanimous; FliTools owns the verb, data in fli-core brand settings |
| 190 | {{Term}} translation placeholders | none | ❌ no | — | — | Translation |
| 191 | Caption segment read/search | FliTools | ✅ yes | see #31 | S | Duplicate of #31 |
| 192 | Direct caption edit | FliEdit | 🟡 maybe | see #32 | S | Duplicate of #32 |
| 193 | Speaker roster | none | ❌ no | — | — | Single speaker |
| 194 | Agent edit proposals with review gate | fli-core | ✅ yes | see #33 | S | Duplicate of #33 |
| 195 | AI caption splitting | FliEdit | 🟡 maybe | captions.propose-splits query -> proposals (#33) | S | Rules-based splitting may be enough |
| 196 | Glossary term review ('Check Terms…') | FliTools | ✅ yes | transcript.check-terms {transcript} query -> proposals for suspected glossary mishearings | S | Pairs with #189 |
| 197 | CLI batch caption review (dormant) | none | ❌ no | — | — | Dormant scaffolding |
| 198 | Caption assistant chat | FliTools | 🟡 maybe | chat.* over transcripts (already designed) | M | Already planned; external Claude Code covers it today |
| 199 | Translation: Apple on-device | none | ❌ no | — | — | Translation not a priority |
| 200 | Translation: AI backend | FliTools | 🟡 maybe | see #30 | M | Duplicate of #30 |
| 201 | Per-caption translation fix | none | ❌ no | — | — | Translation |
| 202 | Transcript language relabel | none | ❌ no | — | — | Minor |
| 203 | Karaoke retimer | none | ❌ no | — | — | Karaoke |
| 204 | Per-word timing inspector | FliCut | 🟡 maybe | word.nudge {edit, index, start_ms, end_ms} command | M | Tighter cut points |
| 205 | Segment editor + list tools | FliEdit | 🟡 maybe | captions.close-gaps {set, under_ms=300} command | S | Caption polish |
| 206 | Music lyrics (captions on music) | none | ❌ no | — | — | Lyrics |
| 207 | Align caption clip with original audio (captions view) | FliEdit | 🟡 maybe | see #85 | S | Duplicate of #85 |
| 232 | Plain-speech extraction and authored-pause map | FliTools | 🟡 maybe | script.plain {script} -> {spokenText, pauseMap} before align.run | S | Helper for #186 only if #231 is built |
| 241 | Auto-captions on narration (script as text, speech service as clock) | none | ❌ no | — | — | TTS-specific; script alignment is #186 |
| 327 | CaptionProject / CaptionSegment data | none | ❌ no | — | — | FliTools transcript format exists |
| 379 | Cloud transcription via server | FliTools | ❌ no | exists: Groq direct | — | Exists already, without a credit layer |
| 388 | Marketplace music lyric tracks | none | ❌ no | — | — | Lyrics |

### Generative audio (music, TTS)

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 22 | narration_generate | FliTools | 🟡 maybe | tts.run {text, voice} task -> wav + word-timed transcript beside target; local Kokoro (~/bin/speak) only | S | Workflow lens said no (David records his own voice); kept as maybe, local Kokoro only — never RxLab's metered TTS |
| 23 | music_generate | none | ❌ no | — | — | Lyria is server-side and metered; mapper 2's maybe overruled |
| 26 | Podcast tools (line-by-line narration editing) | none | ❌ no | — | — | Multi-speaker TTS podcasts are not part of the workflow |
| 213 | Music generation (Lyria 3 Pro) | none | ❌ no | — | — | Music generation |
| 214 | Music prompt builder (structured editor mode) | none | ❌ no | — | — | Music generation |
| 215 | Music free-prompt mode | none | ❌ no | — | — | Music generation |
| 216 | Music reference images | none | ❌ no | — | — | Music generation |
| 217 | Music output format (MP3/WAV) | none | ❌ no | — | — | Music generation |
| 218 | Lyrics text returned with music | none | ❌ no | — | — | Music generation |
| 219 | Song structure and lyrics editors | none | ❌ no | — | — | Music generation |
| 220 | Music prompt preview sheet | none | ❌ no | — | — | Music generation (dryRun preview already covered by fli-core humanOnly.when) |
| 221 | Music takes: history, playback, export, delete, timeline | none | ❌ no | — | — | Music generation |
| 222 | Narration generation (TTS) with provider dispatch | FliTools | 🟡 maybe | see #22 (local Kokoro) | S | Duplicate of #22 |
| 223 | Gemini TTS (single or two speakers) | none | ❌ no | — | — | Server TTS |
| 224 | Azure Neural/HD TTS via SSML | none | ❌ no | — | — | Azure |
| 225 | Azure long-script batching | none | ❌ no | — | — | Azure |
| 226 | Azure audio stitching | none | ❌ no | — | — | Azure |
| 227 | Azure voice pre-flight validation | none | ❌ no | — | — | Azure ("did you mean" on refusals is a nice fli-core idea to note) |
| 228 | Azure voice catalogue (proxy + 24h disk cache) | none | ❌ no | — | — | Azure |
| 229 | Voice preview (Azure + Gemini) | none | ❌ no | — | — | TTS |
| 230 | Localized preview text via Apple Translation | none | ❌ no | — | — | TTS |
| 231 | Delivery shortcodes ({{...}}) | Scribe | 🟡 maybe | script markup {{pause}}, {{emphasis}} authored in Scribe, shown as cues by Teletubby | S | Delivery cues on the prompter |
| 233 | Transcript editor with shortcode chips | none | ❌ no | — | — | TTS editor |
| 234 | Speaker casting and Azure voice parameters | none | ❌ no | — | — | TTS |
| 235 | Provider switch with per-provider voice memory (GUI only) | none | ❌ no | — | — | TTS |
| 239 | Narration prompt/SSML preview sheet | none | ❌ no | — | — | TTS |
| 240 | Narration progress + cancel | fli-core | 🟡 maybe | standard task progress {phase, done, total} + task.cancel for every kind:task | S | Polling exists but differs per app (status vs state); unify later |
| 242 | Narration takes: history, playback, export, delete, timeline | none | ❌ no | — | — | TTS |
| 323 | MusicProject / GeneratedMusic data | none | ❌ no | — | — | Generative data |
| 324 | NarrativeProject / GeneratedNarrative data | none | ❌ no | — | — | TTS data |
| 375 | Narration TTS via server (Azure / Gemini) | none | ❌ no | — | — | Server TTS |
| 376 | Azure voice catalog proxy | none | ❌ no | — | — | Azure proxy |
| 377 | Voice preview (billed) | none | ❌ no | — | — | Billed preview |
| 378 | Music via Lyria 3 Pro (async job) | none | ❌ no | — | — | Server music |

### Generative image and video

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 24 | image_generate | FliTools | 🟡 maybe | image.generate {prompt, aspect, transparent?} task, external-side-effect, own key (nano-banana path) -> png at save_to, versioned | S | Only if overlays need art inline; already exists as a skill |
| 25 | video_generate / video_job_status / video_resume | none | ❌ no | — | — | Veo is server-side and expensive; FliGen is deprecated |
| 38 | remotion_generate_image | FliTools | 🟡 maybe | overlay.asset.generate {overlay, prompt, transparent?} -> delegates to image.generate (#24), stages into overlays/<name>/public/generated/ | S | Own key only, never a credit account |
| 133 | Generate marketplace content/covers | none | ❌ no | — | — | Admin generation |
| 164 | AI image generation into a composition | FliTools | 🟡 maybe | see #38 | S | Duplicate of #38 |
| 247 | Image item (prompt → still) with takes | none | ❌ no | — | — | Covered by #24 and ThumbRack |
| 248 | Image model routing: Google direct vs Vercel AI Gateway | none | ❌ no | — | — | Server routing |
| 249 | Google-style image parameters | none | ❌ no | — | — | Generative detail |
| 250 | OpenAI/gateway-style image parameters | none | ❌ no | — | — | Generative detail (transparent option folded into #24) |
| 251 | Per-item image model picker + account default | none | ❌ no | — | — | Generative detail |
| 252 | Generated image takes gallery | none | ❌ no | — | — | Gallery UI |
| 253 | Remotion inline image generation | FliTools | 🟡 maybe | see #38 | S | Duplicate of #38 |
| 254 | Video item (Veo) generate → take | none | ❌ no | — | — | Veo |
| 255 | Veo parameter set | none | ❌ no | — | — | Veo |
| 256 | Per-model capability gating / clamp (VeoModelFamily) | none | ❌ no | — | — | Veo |
| 257 | Image-to-video: first frame / last frame interpolation | none | ❌ no | — | — | Veo |
| 258 | Reference images (asset consistency) | none | ❌ no | — | — | Veo |
| 259 | Video model picker (live catalog) | none | ❌ no | — | — | Veo |
| 260 | Resumable video jobs (persisted job handle) | fli-core | ✅ yes | persisted task handle {id, engine, input, startedAt} on disk; task.resume never resubmits; refusal job-lost | M | Workflow lens yes (in-memory FliTools queue, double-billing); architecture lens puts it in fli-core so every app's tasks get it |
| 261 | Video progress sheet + stop-waiting | none | ❌ no | — | — | Veo UI ("cancel only stops waiting" noted under #240) |
| 262 | Server-side Veo job lifecycle (submit / poll-finalize / store) | none | ❌ no | — | — | Server |
| 263 | Veo 2 multi-clip (numberOfVideos 1–2) | none | ❌ no | — | — | Veo |
| 264 | Local poster frame + probe for generated clips | FliStudio | 🟡 maybe | footage.list includes cached poster frame + probe (computed by FliTools media.probe) | S | Thumbnails in the project home; FliTools computes, FliStudio shows |
| 265 | Generated video takes list | none | ❌ no | — | — | Generative |
| 266 | Generated takes → timeline | none | ❌ no | — | — | Generative ("any file is a placeable source" is #330) |
| 267 | Duplicate image/video item | none | ❌ no | — | — | Generative |
| 270 | Marketplace admin generation (covers + footage) | none | ❌ no | — | — | Admin |
| 272 | Deferred/unimplemented video providers & ops | none | ❌ no | — | — | Not built |
| 325 | ImageGenProject / GeneratedImage data | none | ❌ no | — | — | Generative data |
| 326 | VideoGenProject / GeneratedVideo data | none | ❌ no | — | — | Generative data (pattern taken as #260) |
| 380 | Image generation via server | none | ❌ no | — | — | Server images |
| 381 | Veo video generation (submit + poll) | none | ❌ no | — | — | Server Veo |

### Motion graphics and overlays (Remotion)

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 36 | Remotion source file tools | FliTools | 🟡 maybe | overlay.files.list/read/write/edit {project, overlay, path} command, reversible-write, 200KB read cap; refusal path-outside-overlay. Only for gate-only agents | S | Mappers said FliMotion; folded into FliTools per the overlay study. Source is sheet + compiled HyperFrames index.html, so file verbs are secondary |
| 37 | remotion_take_screenshot / remotion_take_screenshots | FliTools | ✅ yes | overlay.frames {project, overlay, t / count 2-8} query -> PNG image content (hyperframes snapshot); deterministic; fast | S | Unanimous: the agent checks its own overlay by looking at it |
| 39 | Remotion asset attach/detach | FliTools | ✅ yes | overlay.asset.add/remove {overlay, path, kind image/audio} command, reversible-write | S | Brand logos and screenshots into overlays |
| 127 | Marketplace fonts | fli-core | 🟡 maybe | brands.json fonts[]; apps register them for captions and overlays | S | Brand fonts are a brand rule, not a purchase |
| 145 | RxRemotion native engine (no Node/Bun/Chromium/Studio) | FliTools | ✅ yes | overlay.render {project, overlay, sheet, brand, size, fps, alpha} task: compile-overlay.py -> HyperFrames (headless Chrome + FFmpeg) -> videos/<name>/<name>-overlay-<variant>.mov; single job at a time; no Remotion | L | Mappers wanted a FliMotion engine (XL/L). Overlay study sets engine (HyperFrames, Apache-2.0, in use) and owner (FliTools endpoint). No WebKit/Remotion port, so L |
| 146 | In-WebView esbuild-wasm compilation with fixed import catalog | FliTools | 🟡 maybe | pin hyperframes version per project (fixed-catalog analogue); render refuses on version drift | S | The catalog's lesson maps onto pinning pre-1.0 HyperFrames |
| 147 | Scoped loopback resource server | none | ❌ no | — | — | Internal detail of their WebKit engine; HyperFrames serves its own assets |
| 148 | Compilation cache + source/render fingerprinting | FliTools | ✅ yes | render hash = sheet + brand + blocks + size + fps + alpha -> vNNN-<hash8>; reuse on match | S | Unanimous; overlay-study change #2 |
| 149 | Live composition preview player (native transport) | FliEdit | ✅ yes | review pane embeds `hyperframes preview` of an overlay beside the sheet table, with hot reload | M | Review belongs in the editor (FliEdit, or FliCut until it exists) |
| 150 | Deterministic frame capture (virtual clock) | FliTools | 🟡 maybe | rely on HyperFrames seeking the paused GSAP timeline frame by frame; `hyperframes lint/check` refuses non-deterministic features | S | HyperFrames already seeks deterministically; no virtual clock needed |
| 151 | Alpha recovery via black/white matte snapshots | FliTools | 🟡 maybe | alpha output via HyperFrames transparent path (untested); matte recovery only as fallback | M | Alpha required; HyperFrames transparent path for compile-overlay.py untested |
| 154 | Native audio mixing of Remotion <Audio>/<Video> sound | FliTools | 🟡 maybe | mix overlay audio (stings) into the render | S | Occasional sting sounds |
| 155 | Native OffthreadVideo adapter for embedded video | none | ❌ no | — | — | Overlays are alpha layers; they don't embed video |
| 156 | Maps in compositions (MapKit + OpenStreetMap + Mapbox) | none | ❌ no | — | — | Maps out of scope |
| 157 | Bundled 3D / particles libraries | none | ❌ no | — | — | Generative extra |
| 160 | No-AI default composition seed | FliTools | ✅ yes | overlay.create seeds from brand skin (DESIGN.md/VIDEO.md) + devices.json blocks, no AI | S | A branded starting point |
| 161 | Remotion parameters inspector | FliTools | 🟡 maybe | overlay.sheet.set-row {overlay, t, device, copy} command (the sheet is the props layer) | M | The sheet plays the role of FilmStudio's props |
| 170 | Read-only source viewer with TSX highlighting | none | ❌ no | — | — | Editors already show source |
| 322 | RemotionProject + RemotionRender cache | FliTools | ✅ yes | see #158 and #148 | S | Duplicate |

### Export

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 21 | sequence_render / sequence_renders | FliEdit | ✅ yes | export.start {project, sequence, codec h264/hevc, res, captions burn/embed/sidecar/none} task (local ffmpeg or FliCast compositor); overwrite ★; export.status/cancel; refusal app-busy | L | The final render — FliEdit's reason to exist. Local, not AVFoundation |
| 35 | caption_export | fli-core | ✅ yes | serializeCaptions(transcript, {format srt/vtt/txt/json, granularity sentence/word}) pure fn; used by FliCut export and FliEdit captions.export | S | Split three ways; architecture lens wins — one serializer stops the exporters drifting |
| 104 | Sequence render (AVFoundation export) | FliEdit | ✅ yes | covered by export.start (#21): h264/hevc, res preset, mp4/mov via local ffmpeg | M | Duplicate of #21 |
| 134 | Marketplace preview renderer | none | ❌ no | — | — | Marketplace |
| 152 | Native movie/still export (H.264 MP4, ProRes 4444 MOV, PNG) | FliTools | ✅ yes | overlay.render output: ProRes 4444 / WebM alpha layer, H.264 composited mp4, PNG still | S | Alpha layers are what FliEdit composites; overlay-study change #1 |
| 153 | Parallel WebView render workers | FliTools | 🟡 maybe | workers:auto sized to cores and RAM; refuse insufficient-memory | S | M4 has 24 GiB; Chrome is memory-hungry |
| 168 | Render Version (into film) and Export to Disk | FliTools | ✅ yes | overlay.render res/fps presets; copy out to videos/ | S | Part of #145 |
| 169 | Render versions list | FliTools | ✅ yes | see #159 | S | Duplicate of #159 |
| 173 | Sequence export renders stale compositions first | FliEdit | ✅ yes | export.start first calls FliTools overlay.render for stale overlays (task dependency) | S | One command gives a final with no stale overlays |
| 209 | Caption file export (editor / MCP) | fli-core | ✅ yes | see #35 | S | Duplicate of #35 |
| 210 | Sequence render caption delivery | FliEdit | ✅ yes | see #105 | S | Duplicate of #105 |
| 307 | Shared recording renderer for preview, thumbnails and export | none | ❌ no | — | — | FliCast already shares one renderer |
| 321 | SequenceRender versions | FliEdit | ✅ yes | export.list {sequence} query -> videos/<name>/<name>-final-vNNN.mp4 + caption files + params | S | Versioned finals (not the overlay-<variant> name) |

### Agent and MCP surface

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 0 | Embedded MCP HTTP server | FliGate | ✅ yes | gate.mcp: POST /mcp; tools/list = union of each app's committed api/openrpc.json; tools/call -> that app's door via fli-core answerMcp + authorize(); principal agent:<mcp-client>; ★ verbs listed but refuse forbidden; refusals unauthorized, forbidden, app-busy, app-not-running | M | Mappers split (FliGate, per-app fli-core, FliAgent). Resolved: fli-core gives the answerMcp adapter + authorize(); FliGate (FliAgent merged in) is the single suite door. Fixes "six doors, five dialects" |
| 1 | MCP port, binding and bearer-token auth | fli-core | ✅ yes | control.bind: loopback by default; bindAll ★ (human:ui only); port probe base..base+9; bearer required even on localhost; refusal unauthorized | S | Mostly exists (control.json, 0600, bearerMatches). Adopt loopback default, port probe, bindAll as ★ |
| 2 | Connect external agent (Claude Code one-liner) | FliGate | ✅ yes | gate.connect-command query (read-only, loopback only) -> `claude mcp add --transport http fli <url> -H 'Authorization: Bearer <token>'` | S | Cheap onboarding line; one on the gateway, not one per app |
| 3 | Film routing: `film` argument and X-RxFilm-Document header | fli-core | ✅ yes | Optional `project` (code) arg injected into every project-scoped verb; x-fli-project header pins a session; else context.get; resolveProject; refusals project-ambiguous, project-not-found | S | A contract rule (2 of 3); FliGate only passes it through. Applies code-as-key (R32) |
| 55 | web_read | none | ❌ no | — | — | Claude Code has WebFetch |
| 56 | Simple-mode wizard tools | none | ❌ no | — | — | Consumer wizard |
| 57 | Agent window (system-wide, multi-thread) | none | ❌ no | — | — | The agent lives outside the apps, in Claude Code |
| 58 | Agent engines (five backends) | none | ❌ no | — | — | No embedded engines |
| 59 | AgentMCPBridge (in-app agent to own MCP server) | none | ❌ no | — | — | No embedded agent (lazy app launch via the gateway is a possible later FliGate detail) |
| 60 | Claude Code / Codex embedding: unsandboxed, pre-approved built-ins | none | ❌ no | — | — | Anti-pattern: unsandboxed, pre-approved Bash and Write |
| 61 | AgentToolPolicy write policy (review vs direct) | fli-core | ✅ yes | principal writePolicy review/direct: in review mode agent writes on gated families route to *.propose (#33); destructive stays humanOnly | S | Extends authorize() with a middle state between allowed and ★ |
| 62 | Simple-mode tool allowlist | none | ❌ no | — | — | Simple mode |
| 63 | AgentSkills (prompt-embedded know-how) | none | ❌ no | — | — | Plugin skills already carry this know-how outside the apps |
| 64 | Agent system prompt (AgentPrompts) | none | ❌ no | — | — | Embedded agent |
| 65 | Per-thread model and thinking-level pickers | none | ❌ no | — | — | Embedded agent |
| 67 | Tool-call cards in transcript | none | ❌ no | — | — | Chat UI |
| 87 | Agent follow-along playhead focus | FliEdit | ✅ yes | event timeline.focus {clipId, principal} after agent writes; UI selects the clip and seeks | S | David watches the agent work |
| 88 | Whole-timeline JSON replace (agent) | FliEdit | ✅ yes | see #17 | S | Duplicate of #17 |
| 89 | Agent 'Assembling a sequence' skill and tool policy | FliEdit | 🟡 maybe | flivideo:fliedit plugin skill (assemble, render), not an in-app prompt | S | Know-how lives in plugin skills |
| 130 | Admin authoring: drafts, categories, publish, delete | none | ❌ no | — | — | Admin |
| 131 | Server-defined authoring form schema | none | ❌ no | — | — | Admin |
| 132 | Upload pipeline (presigned R2) | none | ❌ no | — | — | Cloud upload |
| 135 | Create Marketplace Item from film piece | none | ❌ no | — | — | Marketplace |
| 136 | Portable project template definition (v1) | FliEdit | 🟡 maybe | recipe/1 JSON in brand root: shots{instructions, duration, requirement}, size, fps, transitions | M | Pairs with #53; could connect a future Scribe shot list |
| 137 | Extract template from film | FliEdit | 🟡 maybe | recipe.extract {sequence} query -> draft | M | Reuse the shape of a good episode |
| 139 | Marketplace chat card | none | ❌ no | — | — | Marketplace |
| 140 | Simple mode wizard (RxFilmTemplates) | none | ❌ no | — | — | Wizard |
| 141 | json-render option pages | none | ❌ no | — | — | Wizard |
| 142 | web_read (Simple-mode research) | none | ❌ no | — | — | WebFetch exists |
| 162 | Composition source file tools | FliTools | 🟡 maybe | see #36 | S | Duplicate of #36 |
| 163 | Deterministic composition screenshots for agents | FliTools | ✅ yes | see #37 | S | Duplicate of #37 |
| 165 | Attach/detach image and audio assets | FliTools | ✅ yes | see #39 | S | Duplicate of #39 |
| 166 | Agent Remotion authoring skill + Generate with AI | FliTools | ✅ yes | extend video-editor:overlay-sheet + overlay-compile skills to call FliTools overlay.render / overlay.frames; screenshot before reporting | S | Authoring loop stays a skill with a human-approved sheet |
| 167 | Simple mode (wizard) Remotion cards | none | ❌ no | — | — | Simple mode |
| 236 | Podcast tools (agent surface) | none | ❌ no | — | — | Podcast TTS |
| 237 | footage_* tools for music and narration | none | ❌ no | — | — | Generative items |
| 238 | Agent skill + Simple-mode policy for audio generation | none | ❌ no | — | — | In-app generative skill |
| 268 | Agent 'Generating footage' skill + tool policy | none | ❌ no | — | — | Generative skill |
| 290 | Focus observation for the agent (and auto-attach) | none | ❌ no | — | — | Privacy risk |
| 310 | Recording MCP tool set and in-app agent policy | FliGate | ✅ yes | expose FliCast's existing verbs (~130) through the gate via its openrpc.json | S | FliCast's own MCP exists; the gate unifies it |
| 311 | External MCP exposure of recording tools (no policy filter) | fli-core | ✅ yes | rule: MCP and HTTP doors call authorize() on every call; no unfiltered registry; ★ verbs refuse forbidden | S | FilmStudio's security hole, adopted as a rule |
| 335 | App-level agent store (Agent.store) | none | ❌ no | — | — | Embedded agent |
| 342 | Simple mode engine choice | none | ❌ no | — | — | Wizard |
| 348 | Simple mode tool allowlist (data-model view) | none | ❌ no | — | — | Wizard |
| 382 | Subscription chat proxy | none | ❌ no | — | — | FliTools chat.* uses its own key or the Agent SDK directly |

### Project and data model

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 5 | film_list | FliStudio | ✅ yes | projects.list exists; add openIn[] from apps.status (query) | S | Mostly exists; which app has a project open helps agents route |
| 7 | footage_list | FliStudio | ✅ yes | footage.list exists; add kind filter (take/cast/cut/final/overlay) + include_versions | S | Exists; kind filter is small |
| 8 | footage_get | FliStudio | 🟡 maybe | asset.get {project, path} query -> ffprobe (codec, fps, size, duration), transcript refs, owning app; refusal video-not-found | S | Useful for probing mixed media before an edit |
| 9 | footage_create | FliEdit | 🟡 maybe | item.create {project, kind: caption/title/marker-set} command, reversible-write | S | Only FliEdit-owned item kinds; generated-media kinds are out |
| 10 | footage_update (inspector parameters) | FliEdit | 🟡 maybe | item.update {project, id, patch} command, reversible-write, zod per kind; refusal video-invalid | S | Only for FliEdit's own item kinds |
| 11 | footage_delete | FliStudio | 🟡 maybe | asset.trash {project, path} reversible-write (moves to -trash/); project.empty-trash ★ is the only hard delete | S | Follows the -trash/ rule, never a hard delete like footage_delete |
| 12 | footage_duplicate | FliEdit | 🟡 maybe | sequence.duplicate {project, name, as} command -> fli.edit.<as>.json | S | Alternate cuts, e.g. a shorts variant |
| 13 | footage_move | none | ❌ no | — | — | fli-core projectLayout fixes the layout |
| 14 | footage_import | FliStudio | ✅ yes | footage.import exists; add copy:boolean (default true; false = reference in place; refusal missing if the file vanishes) | S | Referencing in place spares disk for 4K Pocket 4 footage on T7 drives |
| 15 | Library folders | none | ❌ no | — | — | No free-form folders |
| 66 | Agent transcript persistence and compaction | none | ❌ no | — | — | Claude Code and AngelEye already hold transcripts |
| 106 | Timeline persistence (TimelineCodec in SwiftData) | FliEdit | ✅ yes | fli.edit.<name>.json = {formatVersion, timeline}, sorted keys | S | Diffable, git-committable store; versioning rule is #314 |
| 107 | Import media (copy vs reference) | FliStudio | ✅ yes | see #14 | S | Duplicate of #14 |
| 158 | RemotionProject library item + on-disk project folder | FliTools | ✅ yes | overlay.create {project, name, kind} command -> <project>/overlays/<name>/{overlay-sheet.md, index.html, public/} (folder in fli-core projectLayout) | S | The overlay's home in the project |
| 159 | RemotionRender versions (render cache) | FliTools | ✅ yes | overlay.renders {overlay} query -> vNNN-<hash8> list | S | Versioned, reusable renders |
| 212 | Caption persistence model | none | ❌ no | — | — | SwiftData internals |
| 244 | Music/Narration SwiftData models | none | ❌ no | — | — | Generative data |
| 308 | Recording storage layout (film format 2) | none | ❌ no | — | — | FliCast has its own layout |
| 309 | Take library management | FliHub | 🟡 maybe | take.hide / unhide (reversible soft delete) | S | FliHub owns takes |
| 312 | .rxfilmstudio film package | none | ❌ no | — | — | Folder projects |
| 313 | Undocumented package folders | none | ❌ no | — | — | Internal detail (projectLayout lint idea noted) |
| 314 | Document.json metadata and format versioning / migration | fli-core | ✅ yes | formatVersion in fli.<app>.json; refuse newer (store-too-new); sibling backup before migrate-layout ★ | S | Unanimous: safe store migrations |
| 315 | Per-film SwiftData schema (Library.store) | none | ❌ no | — | — | SwiftData |
| 316 | GroupableProject library items and FootageKind | fli-core | 🟡 maybe | SourceKind enum (take, cut, cast, overlay, caption, file) backing #330 | S | Part of #330 |
| 317 | Library folders (ProjectGroup) | none | ❌ no | — | — | Folders |
| 318 | Imported assets: copy vs reference | FliStudio | ✅ yes | see #14 | S | Duplicate of #14 |
| 330 | Source-id grammar and DocumentMediaResolver | fli-core | ✅ yes | parseSourceUri('<kind>:<ref>') for cut:, cast:, overlay:, take:, captions:, file:<rel>; resolveSource() -> path or `unrendered` | S | Unanimous: the loose-coupling seam that lets FliEdit place any app's output |
| 331 | Workspace.json per-film panel layout | none | ❌ no | — | — | window-state.json exists |
| 332 | Persistence model: SwiftData autosave in place | none | ❌ no | — | — | Persistence detail |
| 333 | Multiple open films and `film` routing | fli-core | ✅ yes | see #3 | S | Duplicate of #3 |
| 334 | New / Open / Recent films | none | ❌ no | — | — | FliStudio already does this |
| 337 | Marketplace authoring workspace film (admin) | none | ❌ no | — | — | Admin |
| 339 | Marketplace project templates: apply to a film | FliEdit | 🟡 maybe | see #53 | M | Duplicate of #53 |
| 340 | Extract a project template from a film (admin) | none | ❌ no | — | — | Admin (local version is #137) |
| 341 | Simple mode wizard: session state machine | none | ❌ no | — | — | Wizard |
| 343 | Simple mode brief, location and upload import | none | ❌ no | — | — | Wizard |
| 344 | Simple mode research and template pick | none | ❌ no | — | — | Wizard |
| 345 | Simple mode style page (agent-authored json-render) | none | ❌ no | — | — | Wizard |
| 346 | Simple mode build, preview and hand-off to the editor | none | ❌ no | — | — | Wizard |
| 349 | Simple mode wizard template catalog (FilmTemplateCatalog) | none | ❌ no | — | — | Wizard |
| 387 | Project template JSON format | FliEdit | 🟡 maybe | recipe/1 validator refuses absolute paths | S | Only if recipes (#136) are built |

### Accounts and credits

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 4 | show_sign_in_dialog | none | ❌ no | — | — | RxLab account sign-in; the suite has no accounts |
| 6 | models_list (per-account model catalog) | none | ❌ no | — | — | Credit-priced model catalogue; engine discovery is #180 in FliTools |
| 123 | Buy with credits | none | ❌ no | — | — | Credits |
| 182 | Transcription metering | none | ❌ no | — | — | Credits |
| 243 | Metered billing for music and speech | none | ❌ no | — | — | Credits |
| 269 | Image/video credit metering | none | ❌ no | — | — | Credits |
| 350 | RxLab sign-in (OAuth PKCE + passkeys) | none | ❌ no | — | — | Accounts |
| 351 | Session restoration with retry | none | ❌ no | — | — | Accounts |
| 352 | Server bearer-token verification | none | ❌ no | — | — | Server |
| 353 | Website account login (Auth.js + @rxtech-lab/authjs-rxlab) | none | ❌ no | — | — | Server |
| 354 | Server-driven auth form schema | none | ❌ no | — | — | Server |
| 355 | Balance endpoint GET /api/v1/me | none | ❌ no | — | — | Billing |
| 356 | Billing summary GET /api/billing | none | ❌ no | — | — | Billing |
| 357 | Signed-in device tracking | none | ❌ no | — | — | Server |
| 358 | rx-subscription as balance/ledger/Stripe authority | none | ❌ no | — | — | Billing |
| 359 | Reserve -> settle -> release metering | none | ❌ no | — | — | Billing |
| 360 | Insufficient-credits HTTP 402 | none | ❌ no | — | — | Billing |
| 361 | Usage reconciliation cron | none | ❌ no | — | — | Billing |
| 362 | Hand-maintained unit price table | none | ❌ no | — | — | Billing |
| 363 | Web credit top-up checkout | none | ❌ no | — | — | Billing |
| 364 | In-app top-up sheet (RxSubscriptionIOS / Stripe) | none | ❌ no | — | — | Billing |
| 365 | Subscription paywall gate | none | ❌ no | — | — | Paywall |
| 366 | Account menu, sidebar footer and account sheet | none | ❌ no | — | — | Accounts |
| 367 | Web dashboard, usage, ledger and invoices pages | none | ❌ no | — | — | Web dashboard |
| 368 | Public model price list (/models) | none | ❌ no | — | — | Pricing |
| 369 | Curated model catalog + admin curation | none | ❌ no | — | — | Server catalog |
| 370 | Marketplace purchase with credits | none | ❌ no | — | — | Marketplace |
| 371 | Local / non-credit AI paths | none | ❌ no | — | — | Suite already local-first; confirms direction, not a feature |
| 372 | BYOK removal | none | ❌ no | — | — | Opposite of our model: David uses his own keys |
| 373 | Post-purchase return to app | none | ❌ no | — | — | Billing |

### Other (marketplace, platform, housekeeping)

| # | Feature | Target app | Wanted | Capability sketch (fli-core style) | Effort | Why |
|---|---|---|---|---|---|---|
| 51 | Marketplace browse and show | none | ❌ no | — | — | Marketplace |
| 52 | marketplace_install / marketplace_add_to_film | none | ❌ no | — | — | Marketplace |
| 53 | project_template_apply | FliEdit | 🟡 maybe | recipe.apply {project, recipe, bindings{req->source uri}} command -> NEW sequence + missing[]; resumable by applicationId | L | Local brand recipes (intro, body, CTA, end card), not a marketplace. FliBrief's Editor Brief is prior art |
| 54 | Marketplace admin authoring | none | ❌ no | — | — | Marketplace admin |
| 102 | Create Marketplace Item from a clip (admin) | none | ❌ no | — | — | Marketplace |
| 108 | ffmpeg Convert tab (never built) | FliTools | ✅ yes | media.normalize {path, profile 1080p25/proxy} task; ffmpeg; content-hash reuse; output beside source | M | FilmStudio designed it and never built it; mixed 4K59.94 HEVC footage needs one shared normaliser |
| 120 | Marketplace window (browse) | none | ❌ no | — | — | Marketplace |
| 121 | Server-driven sidebar taxonomy | none | ❌ no | — | — | Marketplace |
| 122 | Marketplace kinds (8) | none | ❌ no | — | — | Marketplace |
| 124 | Install / Uninstall / Reveal | none | ❌ no | — | — | Marketplace |
| 125 | Add to Film | none | ❌ no | — | — | Marketplace (a FliStudio brand asset shelf was floated, not adopted) |
| 126 | Library panel Marketplace tab | none | ❌ no | — | — | Marketplace |
| 128 | Music/sound preview with lyric tracks | none | ❌ no | — | — | Marketplace |
| 129 | Remotion composition publishing (executable content) | none | ❌ no | — | — | Marketplace |
| 143 | Marketplace i18n | none | ❌ no | — | — | Marketplace |
| 144 | What's New feature cards (Marketplace, Project templates) | none | ❌ no | — | — | Product marketing |
| 174 | Marketplace Remotion items (publish/install source archives) | none | ❌ no | — | — | Marketplace |
| 175 | Project templates with Remotion dependencies | none | ❌ no | — | — | Marketplace |
| 176 | Standalone RxRemotionExample CLI + package API | FliTools | ✅ yes | CLI door `flitools overlay render/check` with a smoke test | S | CLI parity with the suite |
| 177 | Legacy Bun/Studio runtime vestiges | none | ❌ no | — | — | Legacy code |
| 245 | Stale BYOK documentation and error strings | none | ❌ no | — | — | Stale docs |
| 246 | Marketplace authoring reuses music generation (admin) | none | ❌ no | — | — | Admin |
| 271 | OpenAIClient / OpenAIModelsClient (not image/video gen) | none | ❌ no | — | — | Embedded chat client |
| 288 | RxPet camera companion | none | ❌ no | — | — | Mascot |
| 336 | App-wide storage in Application Support | none | ❌ no | — | — | Internal |
| 338 | Settings persistence (Keychain vs UserDefaults) | fli-core | 🟡 maybe | bearer token and provider keys in Keychain, not 0600 json | S | Small hardening step |
| 374 | Presigned upload API | none | ❌ no | — | — | Cloud upload |
| 383 | Async AI job store + result delivery | none | ❌ no | — | — | Server job store (pattern taken as #260) |
| 384 | Marketplace catalog API | none | ❌ no | — | — | Marketplace |
| 385 | Marketplace admin authoring API | none | ❌ no | — | — | Marketplace |
| 389 | SF Symbols rendering API | none | ❌ no | — | — | Admin web |
| 390 | Sparkle auto-update + site download | none | ❌ no | — | — | The apps are not distributed |
| 391 | What's New feature cards | none | ❌ no | — | — | Product marketing |
| 392 | TipKit feature tips | none | ❌ no | — | — | Tips |
| 393 | User Guide window (designed, not built) | none | ❌ no | — | — | Not built |
| 394 | Localization incl. server responses | none | ❌ no | — | — | i18n |
| 396 | iOS support (legacy, not a current target) | none | ❌ no | — | — | Legacy iOS |
| 397 | Release timeline | none | ❌ no | — | — | Release history, not a feature |
## Invented apps

### FliGate — suite MCP gateway

> ⚠️ **Proposal, not settled.** Inventing the suite's single MCP door is an architecture decision for David; this study only records the case for it.

| | |
|---|---|
| **Purpose** | One running `/mcp` door for every Fli app. `tools/list` is generated from each app's committed `api/openrpc.json`; each `tools/call` is proxied to that app's own door through fli-core `answerMcp`, with `authorize()` enforced so ★ verbs still refuse agents (the #311 lesson). Passes `project` routing through, and offers the one-line `claude mcp add` command. The natural home for the proposed suite event feed (`app.restarted`, `human.needed`, `job.failed`) |
| **Verbs** | `gate.mcp`, `gate.connect-command`, `gate.status` |
| **Why not an existing app** | fli-core is a library and cannot be one endpoint. FliStudio launches apps but deliberately does not proxy their verbs. Per-app MCP doors from fli-core fix the dialect problem but still leave six doors. FliGate merges mapper 1's FliGate with mapper 3's FliAgent (a near-duplicate); mapper 2's per-app doors are kept as the fli-core layer underneath |
| **Features owned** | #0 Embedded MCP HTTP server, #2 Connect external agent, #310 Recording MCP tool set (exposing FliCast's ~130 verbs) |

### FliMotion — considered and rejected

All three mappers invented **FliMotion** to author and render overlays. It is **not kept**: the overlay study showed HyperFrames already renders headless, render is a stateless cacheable transform (so a FliTools endpoint), and review and placement belong in the editor. Its features were redistributed: render/frames/cache/create/assets → FliTools `overlay.*`; live preview (#149) → FliEdit; sheet authoring stays in the `video-editor:overlay-sheet` and `overlay-compile` skills. FliMotion is the named fallback if David later wants a standalone human authoring surface for overlays.

## Mapper disagreements and how they were resolved

1. **FliMotion** (unanimously invented) was **not kept** — see above. The overlay study's evidence overruled all three mappers.
2. **Overlay engine**: mappers proposed Remotion or HyperFrames; mapper 1 floated a native WebKit engine. Final: **HyperFrames only**, no Remotion (architecture, plus licence exposure from a fourth person on), and FilmStudio's RxRemotion is not used as code (no licence file, macOS 26 only, "do not distribute"). Effort for #145 drops from XL to L.
3. **MCP door (#0, #2)**: FliGate vs per-app fli-core `answerMcp` vs FliAgent. Merged: fli-core supplies the adapter and the `authorize()` rule; FliGate (absorbing FliAgent) is the single suite endpoint. Project routing (#3) goes to fli-core (2 of 3).
4. **Suite rules moved to fli-core** on architecture grounds over app placements: caption serializer (#35/#209, split three ways), cue building (#188, split three ways), review gate (#33, 2 of 3), persisted task handles (#260: FliTools vs fli-core vs "no"; the workflow lens said yes, so wanted = yes).
5. **Glossary (#189)**: FliTools owns the verb (2 of 3); the data lives in fli-core brand settings (mapper 2).
6. **Generative services (#22, #24)**: workflow lens said no; mappers 2 and 3 said maybe as FliTools tasks. Kept as **maybe, own-key or local only** (Kokoro, nano-banana). Music (#23) and Veo (#25) are no.
7. **#46, agent drives other apps' UI**: mapper 1's maybe (inside an armed replay only) overruled 2–1. Out: it breaks S8.
8. **#99/#301 editable zoom lane**: mapper 1 treated it as new work (M); mappers 2 and 3 say FliCast already has it. Set to S: verify, don't rebuild.
9. **#273 record mode and #296 replay waits**: majority said maybe; both made **yes** for coherence, because #295 Replay-and-Record is kept.
10. **#240 unified task progress**: mappers 1 and 3 said no (polling exists); mapper 2 flagged the `status` vs `state` dialect split. Kept as maybe.
11. **#108 media.normalize**: mapper 3 said no only because FilmStudio never built it. Workflow lens says yes (mixed Pocket 4 HEVC footage), so FliTools, yes.
12. **#321**: mapper 3 named final renders with the reserved `overlay-<variant>` name. Corrected to `<name>-final-vNNN`.
13. **#264 poster and probe**: FliStudio displays it (majority); FliTools `media.probe` computes it (mapper 2).

## What this mapping does not establish

- Nothing was built or run, in FilmStudio or in any Fli repo. Efforts are estimates from reading, not measurements.
- "Exists" claims about FliCast, FliTools and FliStudio verbs come from the mappers' reading of those repos and were not re-verified row by row in this pass.
- HyperFrames' transparent-output path for `compile-overlay.py` (#151, #152) is untested.



---


# Generated overlays — four approaches compared

**Purpose**: The required overlay comparison from the FilmStudio study (phase 3): what each overlay approach we have or could adopt actually is, how they compare, what FilmStudio teaches, and who should own overlay generation in FliVideo.

**For Agents**:
- Use this when asked "which engine for overlays", "should we use Remotion", or "which app owns overlays"
- The recommendation here **overrules the three phase-3 mappers' invented FliMotion app** — see [flivideo-mapping.md](./flivideo-mapping.md) §"Invented apps"
- For the Remotion licence consequence of a FliEdit, read §4 before proposing any `remotion` dependency
- `fires_via: none` — this is a captured recommendation, not an enforced rule

---

## Recommendation (answer first)

- **Standardise on HyperFrames**, driven by our own three-layer overlay method: vocabulary, overlay sheet, brand skin.
- **FliTools owns overlay rendering**, as a headless render endpoint.
- **FliCut, or FliEdit once built, owns review and placement.**
- **Do not adopt Remotion.** The reason is architecture, not licence cost.
- **FilmStudio's native WebKit engine** is the best *pattern* in the set (one native app, preview and export in the same engine, agent screenshots). We cannot adopt it as code: no licence file, macOS 26 only, and it is still Remotion underneath.

## 1. The four approaches

### (1) The FliVideo overlay style — really two systems

**(1a) FliCast built-in overlays.** A keystroke pill and a caption line.
- **Spec:** Zod fields in the project document, `flicast/src/core/model/schema.ts`.
- **Changes:** typed verbs (`style.set`, `overlay.captions.*`); controls carry `data-verb` so agents can drive them (ADR-0004).
- **Rendering:** the pure planner `flicast/src/core/render/planner.ts` feeds the PixiJS/WebCodecs compositor `flicast/src/compositor/index.ts`.
- **Brand control:** none. White Helvetica on 50% black, hard-coded (`compositor/index.ts, 300`).

**(1b) Talking-head graphic overlays.** The real overlay system.
- **Vocabulary:** 27 brand-neutral devices in `~/dev/ad/appydave-plugins/video-editor/skills/overlay-sheet/devices.json`.
- **Overlay sheet:** a markdown table, one row per beat, each with a quoted motivation from the transcript and five editorial guards. `~/dev/ad/appydave-plugins/video-editor/skills/overlay-sheet/SKILL.md`.
- **Brand skin:** `DESIGN.md` + `VIDEO.md` per brand under `~/dev/ad/appydave-plugins/brand-dave/skills/brand/references/<brand>/`.
- **Compile:** `compile-overlay.py` turns the sheet into a HyperFrames `index.html`; `blocks.py` contains no hex values and no font names. Skill: `~/dev/ad/appydave-plugins/video-editor/skills/overlay-compile/SKILL.md`.
- **Design grammar:** Brandy (7 archetypes, the layer contract, motion grammar, "consistent skin, varied structure"): `~/dev/agents/brandy/agent/skills/video-overlay-design.md`.
- **Method source:** `~/dev/ad/brains/video-as-code/overlay-sheet-method.md`.
- **Proven:** Guy Monroe 0011 — 7 beats + 3 cover plates, 4,961 frames in 100 s.

### (2) HyperFrames (HeyGen)

- **Licence and version:** Apache-2.0, npm `hyperframes` v0.8.68 — pre-1.0, releases almost daily.
- **Composition:** plain HTML with `data-start` / `data-duration` / `data-track-index` and one paused GSAP timeline at `window.__timelines[id]`.
- **Rendering:** headless Chrome via Puppeteer seeks the timeline frame by frame; FFmpeg encodes.
- **Tooling:** CLI with lint, check (also audits contrast and layout), snapshot, preview, render.
- **Measured on the M4:** 54 s of 1080p in about 38 s at draft quality, 6 workers.
- **Limits:** cannot edit footage; cannot fetch data at render time. Sources: `~/.agents/skills/hyperframes-read-first/SKILL.md`, `~/dev/ad/brains/video-as-code/hyperframes-fundamentals.md`.
- **In use:** the engine for 1b, `mochaccino:motion` and the live Joy pipeline.

### (3) Our Remotion experiments

- `~/dev/ad/appydave-app-a-day/009-remotion` — Remotion 4.0.417, React 19, Tailwind v4; five intro and chapter-card compositions; last touched 2026-02-04; `out/` empty.
- `~/dev/ad/joy/joy-videos` — DEPRECATED 2026-07-23; colours invented rather than taken from either brand; replaced by HyperFrames `joy-video`.
- Neither has a spec layer, a brand-token binding or code that calls `renderMedia()`. Both were rendered by hand via the Remotion CLI or Studio.

### (4) FilmStudio — Remotion through system WebKit

Clone: `~/dev/upstream/repos/filmstudio-study`.

- **Engine:** `Packages/RxRemotion` compiles the user's Remotion TSX inside a WKWebView with esbuild-wasm 0.25 against a fixed catalogue of 20 imports, pinning `remotion`, `@remotion/player`, `@remotion/three` at 4.0.459 (confirmed in `Resources/Web/manifest.json`). `@remotion/transitions`, `shapes` and `google-fonts` are absent.
- **Frame capture:** `Browser/capture.js` fakes the clock and seeds randomness; rejects `backdrop-filter`, `mix-blend-mode`, 3D transforms, WebGPU. Alpha is recovered from paired black and white snapshots (mean error 0.2475/255). AVFoundation encodes MP4, or MOV with alpha.
- **Agent tools:** 11 MCP tools — `remotion_read/write/edit_file`, `remotion_take_screenshot(s)` (480×270), asset add/remove (`film-workflow/clients/mcp/handlers/RemotionMCPHandlers.swift`).
- **Caching and timeline:** renders cached as `vNNN-<hash8>.mp4|mov`; composition clips sit on the NLE timeline and play live in WebKit layers.
- **Status and gaps:**
  - `Validation.md`: "not yet a completed release sign-off … Do not distribute".
  - **No brand system** — one theme-colour field plus the agent's taste.
  - **No LICENSE file in the repo** → all rights reserved.
  - **Remotion's own terms are missing from `THIRD-PARTY-NOTICES.txt`** (0 hits for "remotion").

## 2. Comparison table

| | (1a) FliCast overlays | (1b) Overlay-sheet + compile + Brandy | (2) HyperFrames (bare) | (3) Our Remotion experiments | (4) FilmStudio RxRemotion |
|---|---|---|---|---|---|
| **What an overlay is** | Keystroke pill and caption line | A timed graphic beat earned by speech (lower-third, callout, hero number, end card…) | Any timed HTML/GSAP element | Stand-alone intro or chapter card | Stand-alone composition clip on an NLE timeline |
| **Spec format** | Zod fields + typed verbs | `overlay-sheet.md` (t, device, copy, quoted motivation, safe zone) + `devices.json` | HTML with `data-*` timing + GSAP timeline | React TSX (`useCurrentFrame` / `interpolate` / `spring`) | React TSX + `COMPOSITION_*` constants in a SwiftData row |
| **Who authors** | Human in the editor, or an agent via verbs | Script scan → agent drafts the sheet → **human approves** → script compiles | Agent or human writes HTML | Human (agent assisting) | In-app agent edits the TSX; human watches |
| **Render engine** | PixiJS WebGL2 + WebCodecs + mediabunny | HyperFrames | Headless Chrome (Puppeteer) seek + FFmpeg | Remotion CLI (Chromium) | System WebKit + virtual clock + AVFoundation; no Node or Chromium |
| **Local vs cloud** | Local (Electron) | Local (cloud/Lambda paths unused) | Local by default; optional HeyGen cloud, AWS Lambda, GCP | Local | Local render; the LLM and `remotion_generate_image` go to RxLab and cost credits |
| **Headless / agent-drivable** | Yes, but inside the Electron app | **Fully**: CLI scripts, markdown in, MP4 out | **Yes**: CLI, lint, check | CLI yes, no agent spec | **Inside the app only** (its MCP); macOS 26 + a GUI process |
| **Brand control** | None (hard-coded) | **Strong**: tokens via CSS custom properties, `VIDEO.md` permission filter, series rule | None built in | None (Joy colours invented) | Weak: one theme colour |
| **Human review gate** | WYSIWYG | 7-row sheet reviewable in ~20 s, **before** paying for a render | Snapshot or filmstrip | Studio | Agent screenshots + live Player |
| **Output** | MP4 with overlays burnt in | MP4 (overlays composited over the source clip) | MP4 or MOV, alpha possible | MP4 | MP4, or MOV with alpha, as a timeline clip |
| **Licence** | Ours | Ours + Apache-2.0 | **Apache-2.0**, no seat or render fees | **Remotion licence** (free up to 3 people; §4) | App: **no licence (all rights reserved)**; engine bundles `remotion` 4.0.459 → Remotion terms apply |
| **Maturity** | Shipping (narrow scope) | Build stage 1; B2B scanner under-fires; 4 devices never auto-proposed | Pre-1.0, fast-moving | Abandoned | "Do not distribute" |

## 3. What FilmStudio actually teaches us

FilmStudio is **not a better overlay system than 1b** — no vocabulary, no sheet, no brand skin, no quoted-motivation guard; an agent writes free-form React per clip. What it does better is **integration**:

1. **One engine for preview and export**, with a content-hash render cache (`RemotionRenderService.currentHash`). Our 1b pipeline has the same property (`hyperframes preview` / `render`); FliCast previews in Pixi and has nothing branded to export.
2. **Overlays are clips on a timeline** with layered live preview (`TimelinePreviewController`). Our overlay composition *contains* the talking-head video — fine for a one-clip reel, wrong for a multi-clip edit, where an overlay should be its own alpha layer on a track.
3. **The agent screenshots the result before reporting** (`remotion_take_screenshots`, 2–8 frames). We already do this with the filmstrip-from-MP4 check.
4. **Alpha output.** MOV-with-alpha is the missing link for (2). HyperFrames can already render transparent output, so overlays can become standalone alpha layers without changing engine.

**Why not copy it**: no licence; Swift on macOS 26; unfinished by its own account; binds us to Remotion licensing; puts authoring inside a GUI app when our agents drive headless CLIs.

## 4. The Remotion licence consequence for a FliEdit

(There is no `fliedit` folder under `` today; this is about the hypothetical app.)

**Headcount is the first test.** The free licence covers a company of up to 3 people using Remotion commercially, "even if you set up an automation, launch a SaaS"; the count includes contractors who operate the codebase ([license](https://www.remotion.dev/docs/license), [FAQ](https://www.remotion.dev/docs/license/faq), [Terms 5.0 #TeamSize](https://www.remotion.dev/docs/terms)).

| Who touches the FliEdit codebase | Consequence |
|---|---|
| David alone | Free |
| David + Jan + Mary | 3 — still free |
| A fourth person (any contractor) | Company Licence mandatory |

**From a fourth person on:**
- A FliEdit that calls `renderMedia()` or embeds `<Player>` is **"Remotion for Automators"** — the FAQ names "video editors … automated video pipelines or using the Remotion Player".
- Cost: **$0.01 per render, minimum $100 a month**, plus $25 a month per person writing Remotion code.
- Under 5.0: **mandatory telemetry or monthly verifiable reporting**.

**If FliEdit were ever distributed:** an abstraction layer so users can't edit the Remotion code; render reporting still applies; the licence must stay active for **one year after the last published version** (each release restarts the year); letting users bring their own Remotion projects needs written approval.

**HyperFrames under Apache-2.0 carries none of these obligations** — no headcount, no render metering, no telemetry, no post-release tail. For an agent-first pipeline that renders often (variants, re-skins, drafts), per-render metering is exactly the wrong cost shape.

**Not established:** the 5.0 terms are not in force yet (latest release 4.0.527; the v4 LICENSE.md says nothing about bundling). Who actually touches which codebase was not checked.

## 5. Recommendation in full

### Engine: HyperFrames, via the overlay-sheet method

- **Already the de-facto standard** — it drives 1b, `mochaccino:motion` and Joy.
- **Remotion was tried twice and abandoned twice.**
- **The spec is where the value lies**: the markdown sheet with its quoted-motivation guard, and the brand skin kept separate from structure (one clip re-skinned into three brands at ~40 min each). Plain HTML + CSS custom properties is the natural compile target for tokens; React adds a build step and a licence for no gain.
- **It runs headless** — agents drive `compile-overlay.py` → `hyperframes lint/check/render`; FilmStudio's in-app MCP model would not suit them.
- **Keep the static fast path**: `~/dev/ad/appydave-plugins/video-editor/scripts/overlay-render.py` (PIL plates + one FFmpeg pass, ~4.4× faster) when nothing moves. Routing rule: "does anything move?"

**Changes to make, learned from FilmStudio:**
1. **Alpha-layer output mode** in `compile-overlay.py`: overlays only, no background video, transparent MOV or WebM — so an editor can place overlays as a track.
2. **Content-hash render cache** (sheet + brand + blocks + size + fps → `vNNN-<hash8>`), copying the `RemotionRenderService` idea.
3. **Pin the HyperFrames version** per project (pre-1.0, near-daily releases).
4. **Brand tokens for FliCast's pill and captions**, eventually — keep its real-time Pixi compositor but read font and colours from the same `DESIGN.md`. A small, separate fix, not a reason to merge the systems.

### Ownership: split generation from placement

| Responsibility | Owner | Why |
|---|---|---|
| **Overlay render service** (sheet + brand + clip → alpha layer or composited MP4, cached) | **FliTools**, a new verb (e.g. `POST /api/overlay/render`) beside transcription | FliTools is "the always-on tool shelf … call a tool behind an endpoint instead of each app implementing it" (`flitools/README.md`). It already owns transcription (overlay-sheet stage 0), runs under launchd on the M4, and one-job-at-a-time suits Chrome's memory appetite |
| **Drafting the sheet** | Agent + the `overlay-sheet` skill, calling FliTools transcribe → scan | Already the working pattern; keep it a skill |
| **Review and approval** | The editor: FliCut today, FliEdit if built. The sheet table is the gate, with the filmstrip beside it | The human decision point belongs where the footage is being cut |
| **Placement on a timeline** | FliCut or FliEdit, consuming alpha layers | The FilmStudio lesson: an overlay is a clip on a track |
| **FliCast** | Keeps only its screen-recording overlays (keystroke pill, captions) | Real-time, input-event driven; do not grow FliCast into a graphics editor |
| **A new app** | **No** | Every piece already has a home |

**In one line:** generation is a stateless, cacheable, agent-callable transform, so it belongs behind an endpoint; judgement is a human act at a review surface, so it belongs in the editor. FilmStudio merges the two in one GUI app — right for a single consumer product, wrong for a fleet of agents plus a human reviewer across several Fli apps.

**Remotion consequence of this plan: none.** Nothing in the proposed stack imports `remotion`. If a future FliEdit wants FilmStudio-style live React compositions, re-run the §4 headcount check first and budget at least $100 a month from the fourth person on.

## What these checks don't establish

- Nothing was rendered through FilmStudio; its engine claims come from its source and its own `Validation.md`.
- HyperFrames' transparent-output path for `compile-overlay.py` is untested — a proposed change.
- Where rendered overlay MP4s land on disk, and whether FliCut can already take alpha layers, were not checked.
- FliTools' routes beyond transcription were read from its README only.



---


# RxFilmStudio — capability inventory

**Purpose**: The phase-1 deliverable of the FilmStudio study: a complete list of what RxFilmStudio v1.9.0 does, and where each capability computes.

**For Agents**:
- Use this to answer "can FilmStudio do X" and "is X local or paid-cloud"
- Source column = a file in the repo `rxtech-lab/film-workflow` (`docs/…` unless given in full). Read, not run: **the app was never installed or executed**
- 🟡 = claimed by marketing only · 📝 = design doc, not shipped · ⚠️ = shipped but the doc itself says validation is incomplete
- ⭐ **Prefer the source-grounded buckets** (bottom half, phase 3) over the phase-1 tables: they are read from code, carry proof paths, and correct several phase-1 claims (e.g. ~70 → 94 MCP tools, Gemini TTS billed per audio-second not per token)
- Row numbers `#` in the buckets are shared with [flivideo-mapping.md](./flivideo-mapping.md)

---

## Status legend and the one headline

**Headline**: the editor, renderer, captions, effects and screen recorder are **local and scriptable through a 94-tool MCP server**. Every *generative* call (music, voice, image, video, cloud transcription) is **resold through an RxLab credits proxy** in front of Google/Azure/OpenAI. See [tech-notes.md](./tech-notes.md) §compute.

## Marketing claims vs what the source says

| Site claim (filmstudio.rxlab.app) | What the repo supports |
|---|---|
| "Generate cues with Lyria. Keep every take in one reel." | ✅ Lyria `lyria-3-pro-preview` via proxy; every generation is kept as a take |
| "Multi-speaker narration, tuned line by line" | ✅ Azure/Gemini TTS + `podcast_*` line-by-line tools |
| "Transcribe, translate, retime. Export VTT or SRT." | ✅ plus embedded `tx3g` tracks and burn-in |
| "Stills and reference art without leaving the app" | ✅ image generation via proxy |
| "A real timeline. 4K, 60 fps, straight out of the app" | ✅ 4K export preset (480p→4K). 🟡 **60 fps is not stated anywhere in the docs** — marketing only |
| "Ask for a change. Review every edit before it lands" | ⚠️ Partly. Only *captions* have a review gate (`caption_propose_edits` + review sheet). Other agent edits apply directly; Claude Code/Codex engines run **unsandboxed with every built-in pre-approved** (`agent-tools.md`) |
| "Free" | ✅ app is free; generation costs credits (300 free on signup) |

## Phase-1 inventory (marketing-level)

> ⚠️ **Marketing-level.** These tables were built on 2026-09-23 from the website and the design docs, before the clone. Keep them for the marketing-vs-source comparison; for any claim, use the source-grounded buckets below.

### Generation (all CLOUD via RxLab proxy `/api/v1/ai/*` unless noted)

| Feature | What it does | Surface | Provider | Compute | Price | Source |
|---|---|---|---|---|---|---|
| Music | Prompt → song, optional structure/lyrics; async job | Music tab · `music_generate` | Google Lyria (`lyria-3-pro-preview`) | CLOUD | ~200-pt hold, billed per audio-second | `subscription-plan.md` |
| Narration (TTS) | Multi-speaker script → speech; shortcodes for pauses/emphasis; ≤10 min SSML chunks stitched client-side | Narrative tab · `narration_generate` | Azure Neural TTS, Gemini TTS | CLOUD | ~30-pt hold; per character (Azure) / output tokens (Gemini) | `subscription-plan.md`, `feature-tips.md` |
| Podcast view | Line-by-line edit of a narration's speakers and lines | `podcast_create/list_speakers/add_content/update_content/remove_content/update_settings` | — | LOCAL orchestration | inherits narration | `agent-tools.md` |
| Voice browse/preview | List Azure voices (cached 24h); play a preview | GUI | Azure | CLOUD | list free, preview ≈1 pt | `subscription-plan.md` |
| Image | Prompt → stills for storyboards/thumbnails | Image tab · `image_generate` | Imagen / `gpt-image-1` etc. | CLOUD | ~60-pt hold, billed per image returned | `subscription-plan.md` |
| Video | Prompt (+first/last frame, reference images) → clip; submit→poll→download | Video tab · `video_generate`, `video_job_status`, `video_resume` | Google Veo 2 / 3 / 3.1 (fast, lite) | CLOUD | per second, tiered by resolution | `video-generation.md` |
| Video job resume | Job handle persisted; Resume/Discard banner survives quit (24h) | GUI banner | — | CLOUD | billed at submit | `video-generation.md` |
| Per-model option gating | Resolution/duration/seed/audio/refs clamp per Veo model | Params form · `footage_update` | — | LOCAL | — | `video-generation.md` |
| Video extension | 📝 not implemented | — | Veo | — | — | `video-generation.md` |
| OpenAI `/v1/videos` (Sora-shape) | 📝 deferred, not wired | — | — | — | — | `video-generation.md` |

### Captions

| Feature | What it does | Surface | Provider | Compute | Price | Source |
|---|---|---|---|---|---|---|
| Transcribe (cloud) | Audio → timed captions | Caption tab · `caption_transcribe` | Azure / OpenAI / Gemini | CLOUD | ~30-pt hold, per minute | `subscription-plan.md` |
| Transcribe (on-device) | Whisper, audio never leaves the Mac | GUI | WhisperKit | **LOCAL** | free | `subscription-plan.md`, `clients/captions/WhisperKitEngine.swift` |
| Translate (AI) | Translate a caption track | `caption_translate` | chat model via proxy | CLOUD | chat metering | `subscription-plan.md` |
| Translate (on-device) | Apple Translation framework | GUI | Apple | **LOCAL** | free | `whats-new-help-tipkit.md` |
| Segment edit/search | List, search, update segments; set speakers | `caption_list_segments`, `caption_search_segments`, `caption_update_segment`, `caption_set_speakers` | — | LOCAL | free | `agent-tools.md` |
| Agent edit review | Agent proposes caption edits; human approves in a review sheet | `caption_propose_edits` | — | LOCAL | free | `agent-tools.md` |
| Align to audio | Re-align a caption clip to its source clip's audio | Timeline menu | — | LOCAL | free | `timeline-editing.md` |
| Lyrics on music | SRT/VTT lyric tracks per language, retiming, merge captions as lyrics | GUI | — | LOCAL | free | `marketplace.md` |
| Export: burn-in | Cues drawn into pixels | Render sheet | Core Image | LOCAL | free | `caption-export.md` |
| Export: embedded | `tx3g` timed-text track per language | Render sheet | AVFoundation | LOCAL | free | `caption-export.md` |
| Export: sidecar | `.srt` / `.vtt` beside the movie, per language | Render sheet · `sequence_render(captions:"sidecar")`, `caption_export` | — | LOCAL | free | `caption-export.md` |
| Styling | Font/colour/position, strip punctuation, bilingual stacking | Inspector | — | LOCAL | free | `caption-export.md` |

### Timeline, effects, render (all LOCAL, free)

| Feature | What it does | Surface | Source |
|---|---|---|---|
| Sequence build | Create sequence, add/remove clips per take, set whole timeline | `sequence_create`, `sequence_add_clip`, `sequence_remove_clip`, `sequence_set_timeline`, `sequence_get` | `agent-tools.md` |
| Tracks | Video / audio / overlay / caption (multiple `C1…Cn`) / zoom lanes; reorder, pin, alias | `sequence_add_track`, `sequence_reorder_tracks` | `timeline-editing.md` |
| Clip ops | Trim, cut/split, move, reverse, speed (retiming strip), volume 0–200% on the waveform, enable/disable | Timeline | `timeline-editing.md` |
| Editing ergonomics | Undo/redo of every op, marquee multi-select, skimming (S) | Timeline | `timeline-editing.md` |
| Effects | Drag Core Image effects onto video/image/Remotion clips; reorder, bypass | Effects & Transitions panel | `effects-and-transitions.md` |
| Transitions | In / Out / Join targets; dissolve, wipe, fade-through-colour; resizable | Same panel | `effects-and-transitions.md` |
| Installable effects | JSON descriptor naming a built-in `CIFilter` + its controls | Marketplace | `Packages/RxVideoEffects/README.md` |
| Render | Stale Remotion clips first, then AVFoundation export: H.264/HEVC/audio-only · AAC · source or 480p→4K · mp4/mov/m4a; into the film as a version or to a folder | `sequence_render`, `sequence_renders` | `document-package.md` |
| Versions | Every generation and every render kept as a take; Remotion renders cached by source hash | Library | README |
| Scope limits (own statement) | "Audio, captions, source-library effects, compound clips and runtime plugin installation are outside this version" of effects | — | `effects-and-transitions.md` |

### Remotion (LOCAL, free)

| Feature | What it does | Surface | Source |
|---|---|---|---|
| Composition authoring | Agent reads/writes/edits the TSX, adds images/audio, screenshots frames | `remotion_list_files`, `remotion_read_file`, `remotion_write_file`, `remotion_edit_file`, `remotion_take_screenshot(s)`, `remotion_generate_image`, `remotion_add_image/audio`, `remotion_remove_image/audio` | `agent-tools.md` |
| Live preview + export without Node | esbuild-wasm in a Web Worker, WKWebView player, AVFoundation encode; ProRes 4444 for alpha | RxRemotion package | `remotion-live-preview.md`, `Packages/RxRemotion/README.md` |
| Maps | `@rxlab/remotion-maps`: MapKit or OpenStreetMap components | Settings → Maps | `remotion-live-preview.md` |

### Screen recording (v1.9.0, 2 days old — LOCAL, free) ⚠️

| Feature | What it does | Surface | Source |
|---|---|---|---|
| Record Content / Record Actions | Screen capture **plus an editable action document** of clicks, keys and scrolls | Recording inspector, floating toolbar, menu bar | `screen-recording.md` |
| Sources | Displays, windows, areas, **per-app system audio**, several mics as separate tracks, cameras incl. Continuity Camera, connected iPhone/iPad screens | Recording setup | `screen-recording.md`, `Info.plist` |
| Auto-zoom from clicks | "Generate Zooms from Clicks" → zoom clips on their own lane; merges near clicks; scale/focus/follow editable; nothing invented at render time | Inspector | `screen-recording.md` |
| Cursor treatment | Cursor visibility, click effects, smoothing, camera masks | Inspector | `screen-recording.md` |
| Action replay | Replay recorded actions on the Mac; on iOS devices via Appium/XCTest | `recording_perform_action`, `recording_actions_edit` | `screen-recording.md` |
| Screenshots for the agent | Window/app captures for agent context | `recording_screenshot`, `recording_focus` | `screen-recording.md` |
| RxPet | Animated camera-buddy overlay while recording | `Packages/RxPet` | `screen-recording.md` |
| ⚠️ Validation gap | The doc says camera/mic/device tests, 10-min A/V sync, Spaces/fullscreen and replay across targets "have not all been validated" | — | `screen-recording.md` |

### Agent and automation

| Feature | What it does | Surface | Compute | Source |
|---|---|---|---|---|
| Embedded MCP server | Whole tool surface over MCP, bearer token, localhost by default (opt-in LAN) | Settings → MCP | LOCAL | `agent-tools.md`, `whats-new-help-tipkit.md` |
| Library/folders | CRUD for footage items and folders; import files | `footage_list/get/create/update/duplicate/move/import/delete`, `folder_*` | LOCAL | `agent-tools.md` |
| Agent window engines | Claude Code, Codex (user's own login, unsandboxed, built-ins pre-approved) · Apple Intelligence (on-device, MCP only) · OpenAI-compatible endpoint · RxLab subscription chat | Agent window | mixed | `agent-tools.md`, `subscription-plan.md` |
| Skills per job | System prompt adds a skill per job (assemble sequence, generate footage, Remotion, captions) when its tools are offered | `AgentSkills.swift` | LOCAL | `agent-tools.md` |
| `web_read` | Fetch a public page's text/images; blocks private addresses | MCP | LOCAL (the Mac fetches directly; no RxLab hop) | `agent-tools.md` |
| Simple mode | Brief (or product URL) → template → style options → build → preview; agent authors the option pages as json-render specs | `wizard_present_templates/options`, `wizard_report_progress` | mixed | `simple-mode.md` |
| Project templates | Reusable film plans (prompt, shots, footage requirements, dependencies) extracted from a film and applied to another | `project_template_from_film` (admin), `project_template_apply` | CLOUD catalog, LOCAL apply | `marketplace.md` |

### Platform and commerce (CLOUD)

| Feature | What it does | Source |
|---|---|---|
| Marketplace | Footage, music, SFX, fonts, effects, transitions, Remotion comps, templates; credits (0 = free); ⌘⌥M; admin authoring incl. generated covers/previews; `en` + `zh-Hans` | `marketplace.md` |
| Account + credits | OAuth PKCE at `auth.rxlab.app`, passkeys; Stripe packs 1,000 pts / $1.30 … 50,000 / $65; 300 free pts; 1 pt ≈ $0.001 provider cost, 1.30× margin in pack price only | `subscription-plan.md` |
| Help | TipKit (46 tips) shipped; 📝 What's New sheet and User Guide window are design spec | `whats-new-help-tipkit.md`, `feature-tips.md` |
| ffmpeg Convert tab | 📝 **never built**, superseded by the AVFoundation export | `video-conversion-plan.md` |

## Phase-1 file formats (marketing-level)

| Format | What it is |
|---|---|
| `.rxfilmstudio` | Package dir: `Document.json`, `Workspace.json`, `Library.store` (**SwiftData/SQLite** — not plain JSON, unlike `.screenstudio`), `Media/{Music,Narration,Images,Videos,Captions,Imported}`, `Remotion/<id>/src`, `Renders/{Remotion,Sequences}`, `Cache/` |
| `com.rxlab.video-modifier` | Effect/transition descriptor (JSON over a built-in CIFilter) |
| `rxlab.film-workflow.library-item`, `.footage` | Drag/drop pasteboard types |
| Out | mp4/mov/m4a; `.srt`/`.vtt`; `tx3g` embedded captions; PNG stills |

⚠️ **Phase-1 gaps, now closed by phase 3 except the last**: the SwiftData schema and MCP tools are read below. Runtime behaviour is still not established — nothing was run.

---

## Source-grounded capability buckets (phase 3, 2026-09-24)

**Where these rows come from**: the read-only clone at `~/dev/upstream/repos/filmstudio-study` (v1.9.0 @ `f1e94dcf`): the Swift source, the 17 design docs, the MCP handler registrations, the SwiftData models and `_release-notes.md`. Every row was checked against its proof file by a verifier pass; the corrections it made are logged in [tech-notes.md](./tech-notes.md) §"Phase 3 open questions and verifier corrections". Proof paths are repo-relative to that clone. **Nothing was built or run**: behaviour claims come from reading code, not from observing the app.

**Row numbers (`#`)** are stable ids shared with [flivideo-mapping.md](./flivideo-mapping.md), which says where each capability belongs in FliVideo.

**The split in numbers**: 398 feature rows. 266 local, 70 server (RxLab), 57 hybrid, 5 unknown (not built or not traced). Some features appear in two buckets, seen from two slices (for example `web_read`, the podcast tools, the Simple-mode allowlist). They are kept as separate rows because each slice verified different details.

| Bucket | Rows |
|---|---|
| Capture and recording | 26 |
| Screen-action logging and auto-zoom | 18 |
| Timeline and sequence editing | 42 |
| Effects | 16 |
| Captions and transcription | 44 |
| Generative audio (music, TTS) | 34 |
| Generative image and video | 32 |
| Motion graphics and overlays (Remotion) | 19 |
| Export | 13 |
| Agent and MCP surface | 45 |
| Project and data model | 41 |
| Accounts and credits | 30 |
| Other (marketplace, platform, housekeeping) | 38 |

### Capture and recording (26)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 40 | recording_sources | Discovers displays, windows, apps, cameras, mics, iOS screens and permission state | LOCAL | `recording_sources` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift`<br>`docs/screen-recording.md` |
| 41 | recording_focus (observe the user's focused window) | Focused and last external window, a screenshot and Accessibility text of the observed app | LOCAL | `recording_focus` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift`<br>`film-workflow/clients/agent/AgentPrompts.swift` |
| 42 | recording_screenshot | One window or all windows of a bundle id as PNG image content; optional save to library | LOCAL | `recording_screenshot` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift` |
| 43 | recording_get / recording_configure | Inspect a recording project; patch sources, inputs, fps, countdown, pet and Appium fields | LOCAL | `recording_get`, `recording_configure` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift` |
| 44 | recording_start / recording_control | Start Record Content / Record Actions / replay; pause, resume, stop by operation_id | LOCAL | `recording_start`, `recording_control` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift` |
| 49 | recording_insert_take | Insert a take into a sequence as separate linked tracks; undoable | LOCAL | `recording_insert_take` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift` |
| 50 | recording_pet | Set the camera pet's mood, message and visibility | LOCAL | `recording_pet` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift` |
| 273 | Screen Recording footage item + three run modes | Record Content, Record Actions, Replay and Record; one session at a time app-wide | LOCAL | `recording_get`, `recording_configure`, `recording_start` | `film-workflow/models/ScreenRecordingProject.swift`<br>`film-workflow/clients/recording/RecordingSession.swift` |
| 274 | Capture sources: display / window(s) / area / iOS device | Display, one or more windows, an area, or a wired iPhone/iPad | LOCAL | `recording_sources`, `recording_configure` | `film-workflow/clients/recording/RecordingSources.swift`<br>`film-workflow/clients/recording/RecordingSetup.swift` |
| 275 | ScreenCaptureKit video pipeline | SCStream per source, 30/60 fps SDR, HEVC .mov, 2 s fragments; real cursor never captured | LOCAL | — | `film-workflow/clients/recording/RecordingSession.swift`<br>`film-workflow/clients/recording/RecordingMediaCapture.swift` |
| 276 | Multi-window take lifecycle | Each window its own track; closing windows end segments; geometry events stored | LOCAL | — | `film-workflow/clients/recording/RecordingSession.swift` |
| 277 | Webcam capture (multiple cameras) | Each camera its own track and capture session | LOCAL | `recording_configure`, `recording_sources` | `film-workflow/clients/recording/RecordingMediaCapture.swift` |
| 278 | Microphone capture (multiple mics) | Each mic its own 48 kHz PCM track with level meters | LOCAL | `recording_configure`, `recording_sources` | `film-workflow/clients/recording/RecordingMediaCapture.swift` |
| 279 | Per-app and system audio via Core Audio process taps | One track per chosen app plus a System Audio track | LOCAL | `recording_configure` | `film-workflow/clients/recording/RecordingAudioTap.swift` |
| 280 | iOS device screen + device audio capture | Wired iPhone/iPad screen and audio via CoreMediaIO | LOCAL | `recording_sources`, `recording_configure` | `film-workflow/clients/recording/RecordingSources.swift` |
| 281 | Session controls: countdown, pause/resume, stop, change sources mid-take | Countdown, pause/resume, stop, change sources while paused, Cmd-Shift-Esc | LOCAL | `recording_control`, `recording_start`, `recording_configure` | `film-workflow/clients/recording/RecordingSession.swift`<br>`film-workflow/views/recording/RecordingActiveControls.swift` |
| 282 | Shared host-clock A/V synchronisation | Every producer timed on one host clock with paused time removed | LOCAL | — | `film-workflow/clients/recording/RecordingMediaCapture.swift` |
| 283 | Crash / interruption recovery | Session.json checkpoint every 2 s; recovered takes rebuilt on open | LOCAL | — | `film-workflow/clients/recording/RecordingRecoveryService.swift` |
| 284 | Permission guide | Step-by-step setup for the five macOS permissions | LOCAL | `recording_sources` | `film-workflow/clients/recording/RecordingPermissions.swift` |
| 285 | Input previews (camera/mic/window) | Live camera preview, mic meter, window thumbnails during setup | LOCAL | — | `film-workflow/clients/recording/RecordingInputPreview.swift` |
| 286 | Menu bar 'Quick Recording…' | Always-present menu bar item to start recording | LOCAL | — | `film-workflow/views/recording/RecordingMenuBarControls.swift` |
| 287 | On-screen chrome kept out of the capture | Toolbar, pet, borders and controls excluded from capture | LOCAL | — | `film-workflow/views/recording/RecordingWindows.swift` |
| 289 | Window / app screenshots | SCScreenshotManager PNGs, optionally saved with capture metadata | LOCAL | `recording_screenshot` | `film-workflow/clients/recording/RecordingSources.swift` |
| 328 | ScreenRecordingProject / RecordingTake data | Settings, actions, presentation, style as JSON blobs; takes soft-deletable | LOCAL | `recording_get`, `recording_configure`, `recording_actions_edit`, `recording_presentation`, `recording_shortcuts`, `recording_pet`, `footage_get`, `footage_list` | `film-workflow/models/ScreenRecordingProject.swift` |
| 329 | Recording crash recovery from Session.json checkpoints | Every film open scans checkpoints and rebuilds or links takes | LOCAL | — | `film-workflow/clients/recording/RecordingRecoveryService.swift`<br>`film-workflow/document/ProjectDocument.swift` |
| 395 | RxPet recording mascot overlay | Pixel-camera mascot during recording, excluded from capture | LOCAL | — | `Packages/RxPet/Sources/RxPet/PetOverlayPresenter.swift` |

### Screen-action logging and auto-zoom (18)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 45 | recording_actions_edit (action script) | Edit a recording's action list: replace, insert, update, delete, duplicate, reorder (re-times) | LOCAL | `recording_actions_edit` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift`<br>`film-workflow/clients/recording/RecordingActions.swift` |
| 46 | recording_perform_action (agent drives other apps' UI) | Posts one real click/text/key/drag/scroll (or Appium device action) in the active session. "Explicit user intent" is descriptor text only | LOCAL | `recording_perform_action` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift`<br>`film-workflow/clients/recording/RecordingActions.swift` |
| 47 | recording_presentation (cursor, zoom, camera) | Patch project defaults or one clip's cursor, zoom intervals/autoZoom and camera presentation | LOCAL | `recording_presentation` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift` |
| 48 | recording_shortcuts (keystroke subtitle cues) | Inspect or edit ⌘/⌃ shortcut subtitle cues and their style | LOCAL | `recording_shortcuts` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift`<br>`film-workflow/clients/recording/RecordingActions.swift` |
| 99 | Zoom-lane clips (materialised auto-zoom) | Click-zoom windows become editable clips on a Z lane (scale 1-8, follow pointer, focus X/Y) | LOCAL | `recording_insert_take`, `sequence_add_clip`, `recording_presentation` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineEditor.swift`<br>`film-workflow/clients/recording/RecordingTimelineService.swift` |
| 100 | Per-clip recording presentation and shortcut subtitles on the timeline | Instance-level cursor, zoom, camera and shortcut cues editable per placed clip | LOCAL | `recording_presentation`, `recording_shortcuts` | `Packages/RxVideoEditor/Sources/VideoEditorUI/RecordingPresentationEditor.swift`<br>`Packages/RxVideoEditor/Sources/VideoEditorCore/Model/RecordingPresentation.swift` |
| 291 | Pointer + click logging (all modes) | Listen-only event tap logging pointer samples and left/right clicks per source | LOCAL | — | `film-workflow/clients/recording/RecordingActions.swift` |
| 292 | Keyboard shortcut capture → shortcut subtitle lane | ⌘/⌃ key-downs become 1.5 s cues on a caption lane; never ordinary typing | LOCAL | `recording_shortcuts` | `film-workflow/clients/recording/RecordingActions.swift` |
| 293 | Record Actions: editable action document | Input converted to 21 structured action kinds with window targets and AX ids | LOCAL | `recording_actions_edit`, `recording_get` | `film-workflow/clients/recording/RecordingActions.swift`<br>`film-workflow/views/recording/RecordingActionEditor.swift` |
| 294 | Recording Movement editor | Time strip + action list: add, duplicate, delete, reorder, edit fields | LOCAL | `recording_actions_edit` | `film-workflow/views/recording/RecordingActionEditor.swift` |
| 295 | Replay and Record (Mac automation) | Runs saved actions via Accessibility + synthetic events while capturing a new take | LOCAL | `recording_start`, `recording_perform_action`, `recording_control` | `film-workflow/clients/recording/RecordingActions.swift`<br>`film-workflow/clients/recording/RecordingSession.swift` |
| 296 | Scripted capture-control, wait and screenshot actions | wait, waitForWindow/Element, start/pause/resumeCapture, changeSource, screenshot actions | LOCAL | `recording_actions_edit`, `recording_perform_action` | `film-workflow/clients/recording/RecordingActions.swift` |
| 297 | Replay execution log in the take | Each executed action stamped with actual time in the take | LOCAL | `recording_get` | `film-workflow/clients/recording/RecordingSession.swift` |
| 298 | iOS device automation via Appium/XCUITest | Device Control window posting taps/swipes/text to Appium | LOCAL | `recording_perform_action`, `recording_actions_edit`, `recording_configure` | `film-workflow/clients/recording/RecordingDeviceAutomation.swift` |
| 299 | Synthetic cursor re-render | Vector cursor redrawn from samples on an overlay lane; click rings; smoothing | LOCAL | `recording_presentation` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Composition/RecordingRenderer.swift` |
| 300 | Auto-zoom from clicks (click-burst algorithm) | 2.5 s windows from clicks, merged within 0.6 s, materialised as zoom clips | LOCAL | `recording_presentation`, `recording_insert_take` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/RecordingPresentation.swift`<br>`film-workflow/clients/recording/RecordingTimelineService.swift` |
| 301 | Zoom lane: editable zoom clips + render evaluation | Zoom clips mapped to source clock; smoothstep ease; follow pointer | LOCAL | `recording_presentation` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Composition/RecordingRenderer.swift` |
| 302 | Legacy presentation zoom intervals + render-time click synthesis | Older presentation-level zooms; render-time synthesis when no lane clips | LOCAL | `recording_presentation` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/RecordingPresentation.swift` |

### Timeline and sequence editing (42)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 16 | sequence_list / sequence_create / sequence_get | List sequences; create one with default tracks; read a timeline as JSON | LOCAL | `sequence_list`, `sequence_create`, `sequence_get` | `film-workflow/clients/mcp/handlers/MCPSequenceHandlers.swift` |
| 17 | sequence_set_timeline | Replace a whole timeline with sequence_get's JSON shape; validated (no overlaps, kind fits track). The bulk-edit path | LOCAL | `sequence_set_timeline` | `film-workflow/clients/mcp/handlers/MCPSequenceHandlers.swift` |
| 18 | sequence_add_track / sequence_reorder_tracks | Add a video, audio, caption or overlay track; reorder all tracks | LOCAL | `sequence_add_track`, `sequence_reorder_tracks` | `film-workflow/clients/mcp/handlers/MCPSequenceHandlers.swift` |
| 19 | sequence_add_clip / sequence_remove_clip | Place one take by source_id (start, duration, in_point, ripple); remove a clip with optional ripple | LOCAL | `sequence_add_clip`, `sequence_remove_clip` | `film-workflow/clients/mcp/handlers/MCPSequenceHandlers.swift` |
| 20 | sequence_link_clips / sequence_track_alias | Link clips into an edit group; set a track display alias. Undoable via the key window | LOCAL | `sequence_link_clips`, `sequence_track_alias` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift`<br>`docs/screen-recording.md` |
| 68 | Timeline data model (tracks, clips, sources) | Codable Timeline: size, fps, background, ordered tracks (video/audio/overlay/caption/zoom) and clips with source, timing, picture/audio/text properties, link group | LOCAL | `sequence_get`, `sequence_set_timeline` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/Timeline.swift`<br>`docs/timeline-editing.md` |
| 69 | Sequence create / settings (resolution, fps, background) | Default lanes C1, V1, A1, A2; size presets 1080p/4K/720p/vertical/square; fps 24-60; background hex | LOCAL | `sequence_create`, `sequence_list`, `footage_update`, `footage_duplicate` | `Packages/RxVideoEditor/Sources/VideoEditorUI/SequenceSettingsView.swift`<br>`film-workflow/models/SequenceProject.swift` |
| 70 | Add / delete / reorder / alias / pin tracks | Add Track menu, drag reorder, alias, pin, delete (removes its clips). No zoom lane by hand | LOCAL | `sequence_add_track`, `sequence_reorder_tracks`, `sequence_track_alias` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineEditor.swift`<br>`Packages/RxVideoEditor/Sources/VideoEditorUI/SequenceTimelineView.swift` |
| 71 | Place footage on timeline (drag/drop, add clip) | Drag library footage onto a lane with snapped preview; overlaps go to the next free slot; agent adds by source_id | LOCAL | `sequence_add_clip`, `footage_list`, `footage_get`, `footage_import` | `Packages/RxVideoEditor/Sources/VideoEditorUI/SequenceTimelineView.swift`<br>`film-workflow/clients/mcp/handlers/MCPSequenceHandlers.swift` |
| 72 | Ripple insert (agent only) | Splits a straddling clip and shifts later clips on that track right | LOCAL | `sequence_add_clip` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineEditor.swift` |
| 73 | Move clips (single and group, lane change) | Drag moves a clip or selection + link groups by one delta; lane change only if every clip fits; all-or-nothing | LOCAL | `sequence_set_timeline` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineEditor.swift`<br>`Packages/RxVideoEditor/Sources/VideoEditorUI/TimelineClipInteraction.swift` |
| 74 | Trim (leading/trailing edges) | Edge trim bounded by source, neighbours and one frame; linked clips trim together | LOCAL | `sequence_set_timeline` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineEditor.swift`<br>`Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineLinks.swift` |
| 75 | Blade / split | Blade tool or Split at Playhead; linked clips split together; refused inside a transition | LOCAL | `sequence_set_timeline` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineEditor.swift` |
| 76 | Delete and ripple delete | Delete or ripple delete the selection. Gotcha: deleting one clip deletes its whole link group | LOCAL | `sequence_remove_clip` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineEditor.swift` |
| 77 | Speed change / retime | Constant per-clip speed by percent or duration; retime strip; refused on linked clips | LOCAL | `sequence_set_timeline` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineEditor.swift`<br>`Packages/RxVideoEditor/Sources/VideoEditorUI/ClipSpeedEditor.swift` |
| 78 | Reverse playback | Reverse toggle; only audio sources can reverse; reversed PCM cached in temp | LOCAL | `sequence_set_timeline` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineEditor.swift`<br>`Packages/RxVideoEditor/Sources/VideoEditorCore/Media/ReversedAudioCache.swift` |
| 79 | Selection model (click, additive, marquee, select all) | Click selects clip + link group; Cmd/Shift additive; Option = clip alone; marquee; Cmd-A. UI state only | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorUI/SequenceTimelineView.swift` |
| 80 | Link / unlink clips | Explicit edit group that moves, trims, splits and deletes together | LOCAL | `sequence_link_clips` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineLinks.swift`<br>`film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift` |
| 81 | Enable/disable clips and tracks | Disabled clip or lane keeps its place but is skipped by preview, render and captions | LOCAL | `sequence_set_timeline` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineEditor.swift`<br>`Packages/RxVideoEditor/Sources/VideoEditorCore/Model/Timeline.swift` |
| 82 | Snapping | Snap to clip edges and zero within 8 px, then frame-quantise; no toggle, no playhead snap | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineEditor.swift` |
| 83 | Timeline zoom and skimming | Zoom 0.5-400 px/s saved per sequence; S toggles hover skimming | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorUI/SequenceTimelineView.swift`<br>`film-workflow/models/SequenceProject.swift` |
| 84 | Markers (absent) | No markers, chapter points or in/out marks exist (verified with a positive control) | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/Timeline.swift` |
| 85 | Align caption clip with original audio | Moves a caption clip to the start of the clip playing its source audio | LOCAL | — | `film-workflow/document/CaptionAudioAlignment.swift`<br>`Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineEditor.swift` |
| 86 | Undo / redo | Whole-timeline snapshot undo per UI edit. Most MCP sequence edits are not undoable | LOCAL | — | `film-workflow/models/SequenceProject.swift`<br>`film-workflow/views/editor/TimelinePanel.swift` |
| 90 | Linear timeline editor window | Library, viewer, inspector and timeline panels; Effects & Transitions browser; layout saved in Workspace.json | LOCAL | — | `film-workflow/views/editor/EditorWindowView.swift`<br>`film-workflow/views/editor/TimelinePanel.swift` |
| 91 | Clip inspector (picture, audio, timing) | Source, enabled, speed, reverse, fit/scale/offset/opacity, volume 0-200%, caption stack and style. No keyframes | LOCAL | `sequence_set_timeline` | `Packages/RxVideoEditor/Sources/VideoEditorUI/ClipInspectorView.swift` |
| 92 | Audio mixing: clip volume, track mute, waveform drag | Per-clip volume by waveform drag or slider; track mute. No fades, pan, EQ or ducking | LOCAL | `sequence_set_timeline` | `Packages/RxVideoEditor/Sources/VideoEditorUI/TimelineClipInteraction.swift`<br>`Packages/RxVideoEditor/Sources/VideoEditorCore/Composition/TimelineCompositionBuilder.swift` |
| 93 | Audio level meter | Stereo peak meter reading the player's own mix | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorCore/Playback/AudioLevelReader.swift` |
| 94 | Playback engine (composition player) | AVMutableComposition + custom compositor; preview at 1280 long edge; exact seeks; frame step | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorCore/Playback/TimelinePlayerController.swift`<br>`Packages/RxVideoEditor/Sources/VideoEditorCore/Composition/TimelineVideoCompositor.swift` |
| 95 | Layered live preview (Remotion live in WebKit) | Remotion clips play live in WKWebView layers when no effects are active; else pre-rendered. Three preview paths | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorCore/Playback/TimelinePreviewController.swift`<br>`film-workflow/views/editor/EditorWindowView.swift` |
| 96 | Viewer transport | Play/pause, frame step, scrubber, timecode, go to start/end, full screen. No J/K/L | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorUI/SequenceViewerView.swift` |
| 97 | Clip filmstrip thumbnails | Shared frame-strip provider cached per source revision | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorUI/TimelineClipFilmstrip.swift` |
| 98 | Capability gating per footage type | Each source kind opts into duration, cut, reverse, speed and drag; every op checks them | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorCore/Media/TimelineEditingCapabilities.swift`<br>`film-workflow/document/TimelineDraggable+Models.swift` |
| 138 | Apply template to film | Build a NEW sequence from an owned template; bindings, missing items, blockers; resumable | HYBRID | `project_template_apply`, `footage_list`, `show_marketplace_item`, `sequence_render` | `film-workflow/clients/marketplace/ProjectTemplateService.swift` |
| 171 | Remotion clips on the timeline (live layered stage) | remotion:<uuid> clips play as live WebKit layers synced to the timeline clock | LOCAL | `sequence_add_clip`, `sequence_set_timeline`, `sequence_get` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Playback/TimelinePreviewController.swift`<br>`docs/remotion-live-preview.md` |
| 172 | Cached ProRes-alpha preview fallback | Disposable alpha ProRes renders (960 px cap) when live playback can't cope or effects are active | LOCAL | — | `film-workflow/clients/RemotionPreviewSessions.swift`<br>`film-workflow/clients/RemotionPreviewRenderJobs.swift` |
| 208 | Caption clips on a sequence timeline (agent) | Agent adds a caption track and places a captions item as a clip | LOCAL | `sequence_add_track`, `sequence_add_clip`, `sequence_get` | `film-workflow/clients/mcp/handlers/MCPSequenceHandlers.swift` |
| 303 | Insert take as linked tracks | Take inserted as one linked clip per component on matching lanes | LOCAL | `recording_insert_take` | `film-workflow/clients/recording/RecordingTimelineService.swift` |
| 304 | Link/unlink clips and track aliases (recording) | Link edit groups and set track aliases | LOCAL | `sequence_link_clips`, `sequence_track_alias` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift` |
| 319 | SequenceProject timeline storage | Whole timeline as one sorted-key JSON blob; opaque to SQL | LOCAL | `sequence_list`, `sequence_get`, `sequence_create`, `sequence_set_timeline`, `footage_update` | `film-workflow/models/SequenceProject.swift`<br>`Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineCodec.swift` |
| 320 | Timeline undo: window UndoManager vs agent edits | Editor edits undoable; core agent sequence edits are not; recording tools use the key window | LOCAL | `recording_insert_take`, `recording_presentation`, `recording_shortcuts`, `recording_actions_edit` | `film-workflow/models/SequenceProject.swift`<br>`film-workflow/clients/mcp/handlers/MCPSequenceHandlers.swift` |
| 347 | TimelineFocus: playhead follows the agent | Handlers set a pending focus; views move the playhead | LOCAL | `sequence_add_clip`, `sequence_set_timeline`, `project_template_apply` | `film-workflow/document/TimelineFocus.swift` |

### Effects (16)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 103 | Clip effects and transitions on the timeline | Drag effects onto clips or transitions onto edges/cuts; validated; no dedicated MCP tools | LOCAL | `sequence_set_timeline` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineModifiers.swift`<br>`docs/effects-and-transitions.md` |
| 109 | Built-in effects (3) | Brightness/Contrast, Saturation, Gaussian Blur; ordered, bypassable stack. Defaults are not neutral | LOCAL | `sequence_get`, `sequence_set_timeline`, `project_template_apply` | `Packages/RxVideoEffects/Sources/VideoEffectsCore/BuiltInModifiers.swift` |
| 110 | Built-in transitions (3) | Cross Dissolve, Fade through Color, Directional Wipe | LOCAL | `sequence_get`, `sequence_set_timeline`, `project_template_apply` | `Packages/RxVideoEffects/Sources/VideoEffectsCore/BuiltInModifiers.swift` |
| 111 | Effect target rule | Effects/transitions only on video, image or Remotion clips on non-audio tracks | LOCAL | `sequence_set_timeline` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineModifiers.swift` |
| 112 | Effects & Transitions browser panel | Tabbed sidebar with search, thumbnails and hover previews; drag onto clips | LOCAL | — | `Packages/RxVideoEffects/Sources/VideoEffectsUI/ModifierBrowser.swift` |
| 113 | Transition drop targets: In / Out / Join | Drop on first half = start, second half = end, a shared cut = Join | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorUI/TimelineModifierInteraction.swift` |
| 114 | Joined-clip linking and protected edits | Joined clips move together; edits that break a join are refused | LOCAL | `sequence_set_timeline`, `sequence_remove_clip` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineModifiers.swift` |
| 115 | Effect/transition inspector | Edit parameters, reorder, bypass, remove; one undo step per gesture | LOCAL | — | `film-workflow/views/editor/inspectors/ModifierInspector.swift` |
| 116 | Unknown-definition passthrough and export gate | Missing definition passes through in preview; export and agent writes refuse it while enabled | LOCAL | `sequence_set_timeline`, `sequence_render` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineModifiers.swift` |
| 117 | Shared Core Image compositor (preview = export) | One compositor for preview and export: effects, placement, opacity, transitions, track combine | LOCAL | `sequence_render` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Composition/TimelineVideoCompositor.swift` |
| 118 | Installable CIFilter descriptor effects/transitions | Marketplace JSON descriptor wrapping one built-in Core Image filter; no custom kernels | LOCAL | `marketplace_install` | `Packages/RxVideoEffects/Sources/VideoEffectsCore/CIFilterModifierDescriptor.swift`<br>`film-workflow/clients/marketplace/InstalledModifierLoader.swift` |
| 119 | Admin effect/transition descriptor editor | Admin editor with presets, defaults and raw JSON; no live preview | LOCAL | `marketplace_create`, `marketplace_update` | `film-workflow/views/marketplace/MarketplaceModifierEditor.swift` |
| 211 | Caption styling | Per-clip TextStyle: font, size, colours, background, position, stroke | LOCAL | `sequence_get`, `sequence_set_timeline` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/Timeline.swift`<br>`docs/caption-export.md` |
| 305 | Camera picture-in-picture presentation | Masked webcam with keyframed size/position; optional follow-zoom | LOCAL | `recording_presentation` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Composition/RecordingRenderer.swift` |
| 306 | Timed visibility intervals | Hide/show screen, camera or cursor layer between source times | LOCAL | `recording_presentation` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/RecordingPresentation.swift` |
| 386 | Effect/transition descriptor format | JSON mapping controls onto a built-in Core Image filter | HYBRID | — | `website/lib/marketplace/schema.ts`<br>`film-workflow/clients/marketplace/InstalledModifierLoader.swift` |

### Captions and transcription (44)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 27 | caption_create | Creates a captions item from a narration (text kept exactly) or an audio path | LOCAL | `caption_create` | `film-workflow/clients/mcp/handlers/MCPCaptionHandlers.swift` |
| 28 | caption_transcribe | New transcript version via WhisperKit (local) or OpenAI/Azure/Gemini through RxLab; narration-backed items only align timings | HYBRID | `caption_transcribe` | `film-workflow/clients/mcp/handlers/MCPCaptionHandlers.swift`<br>`film-workflow/clients/services/CaptionTranscriptionService.swift` |
| 29 | caption_versions | List, activate or delete transcript versions | LOCAL | `caption_versions` | `film-workflow/clients/mcp/handlers/MCPCaptionHandlers.swift` |
| 30 | caption_translate | Translate the active version (missing/stale or all); glossary terms as {{Term}}. Default backend is the RxLab subscription chat | HYBRID | `caption_translate` | `film-workflow/clients/mcp/handlers/MCPCaptionHandlers.swift`<br>`film-workflow/config/CaptionSettings.swift` |
| 31 | caption_list_segments / caption_search_segments | Page through captions; search caption words ignoring case, accents and punctuation | LOCAL | `caption_list_segments`, `caption_search_segments` | `film-workflow/clients/mcp/handlers/MCPCaptionHandlers.swift` |
| 32 | caption_update_segment | Edit one caption's text, timing, speaker or translation directly | LOCAL | `caption_update_segment` | `film-workflow/clients/mcp/handlers/MCPCaptionHandlers.swift` |
| 33 | caption_propose_edits (review gate) | Queue caption edits for one-by-one user approval; external proposals appear to have no visible review surface | LOCAL | `caption_propose_edits` | `film-workflow/clients/mcp/handlers/MCPCaptionHandlers.swift`<br>`film-workflow/clients/agent/AgentController.swift` |
| 34 | caption_set_speakers | Rename a speaker or replace the roster | LOCAL | `caption_set_speakers` | `film-workflow/clients/mcp/handlers/MCPCaptionHandlers.swift` |
| 101 | Clip context-menu host actions (captions, lyrics) | Narration clip → Create/Add Captions; music clips → lyrics add/edit/retime/merge | LOCAL | — | `film-workflow/views/editor/TimelinePanel.swift`<br>`film-workflow/document/NarrativeCaptionClip.swift` |
| 105 | Caption clips: delivery at render (burn-in / embedded tx3g / sidecar) | Burn in, mux tx3g per language, or write .srt/.vtt sidecars | LOCAL | `sequence_render` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Export/SubtitleTrackMuxer.swift`<br>`film-workflow/views/editor/CaptionRenderSection.swift` |
| 178 | Captions library item (CaptionProject) | Captions item owning audio, speakers, glossary, versions and segments | LOCAL | `caption_create` | `film-workflow/models/CaptionProject.swift` |
| 179 | On-device transcription (WhisperKit) | Core ML Whisper on the Mac; free, no sign-in; word timings where supported | LOCAL | `caption_create`, `caption_transcribe` | `film-workflow/clients/captions/WhisperKitEngine.swift`<br>`film-workflow/clients/captions/CaptionTranscriber.swift` |
| 180 | Whisper model manager | Download/size/RAM-filter WhisperKit variants from argmaxinc | HYBRID | — | `film-workflow/clients/captions/WhisperModelStore.swift` |
| 181 | Cloud transcription via RxLab server (OpenAI / Azure / Gemini) | Audio to /api/v1/ai/transcriptions; server calls provider with its own key | SERVER | `caption_create`, `caption_transcribe` | `film-workflow/clients/backend/BackendTranscriptionClient.swift`<br>`website/app/api/v1/ai/transcriptions/route.ts` |
| 183 | Upload audio prep: compression + chunking | Re-encode to 16 kHz AAC when worthwhile; chunk ≤10 min / ~24 MB and stitch | LOCAL | `caption_transcribe` | `film-workflow/clients/captions/CaptionAudioCompressor.swift`<br>`film-workflow/clients/captions/CaptionAudioChunker.swift` |
| 184 | Timing validation + fallback provider | Reject backwards/out-of-range timestamps; retry on a fallback provider or repair with a warning | HYBRID | `caption_transcribe` | `film-workflow/clients/captions/CaptionTranscriptValidator.swift` |
| 185 | Transcript versions | Every run appends a numbered, labelled version; activate or delete | LOCAL | `caption_transcribe`, `caption_versions` | `film-workflow/models/CaptionTranscriptVersion.swift` |
| 186 | Narration captions (script-aligned timings) | ASR used only for timings; script words take them, so text matches the script exactly | HYBRID | `caption_create`, `caption_transcribe` | `film-workflow/clients/captions/CaptionAligner.swift` |
| 187 | Auto-captions on narration generation | Generating narration also creates/aligns a linked caption project | HYBRID | — | `film-workflow/clients/services/NarrativeGenerationService.swift` |
| 188 | Sentence cue building | Provider phrases → sentence cues split at word boundaries, never across speakers | LOCAL | `caption_transcribe` | `film-workflow/clients/captions/CaptionCueBuilder.swift` |
| 189 | Glossary / terms (spelling bias) | Per-project canonical spellings biasing Whisper/Gemini/OpenAI prompts | LOCAL | — | `film-workflow/models/CaptionTerm.swift` |
| 190 | {{Term}} translation placeholders | Translations store glossary terms as placeholders filled per language at display/export | LOCAL | `caption_translate`, `caption_list_segments`, `caption_search_segments` | `film-workflow/models/CaptionTermPlaceholder.swift` |
| 191 | Caption segment read/search | Paged list and word search with context rows | LOCAL | `caption_list_segments`, `caption_search_segments` | `film-workflow/clients/mcp/handlers/MCPCaptionHandlers.swift` |
| 192 | Direct caption edit | Edit one caption by index immediately, no review | LOCAL | `caption_update_segment` | `film-workflow/models/CaptionSegmentEditing.swift` |
| 193 | Speaker roster | Rename or replace speakers; max_speakers clamped 2-35 client-side | LOCAL | `caption_set_speakers` | `film-workflow/models/CaptionSpeaker.swift` |
| 194 | Agent edit proposals with review gate | Validated edit batch held for approval in CaptionAIReviewSheet | LOCAL | `caption_propose_edits` | `film-workflow/clients/captions/ai/CaptionEditProposal.swift`<br>`film-workflow/views/caption/CaptionAIReviewSheet.swift` |
| 195 | AI caption splitting | LLM chooses where long captions break; produces a proposal | HYBRID | — | `film-workflow/clients/captions/ai/CaptionAISplitter.swift` |
| 196 | Glossary term review ('Check Terms…') | Finds likely misheard glossary terms and proposes fixes | HYBRID | — | `film-workflow/clients/captions/ai/CaptionTermReviewer.swift` |
| 197 | CLI batch caption review (dormant) | Unfinished scaffolding for CLI-driven caption review; no conforming type | LOCAL | `caption_propose_edits`, `caption_list_segments` | `film-workflow/clients/captions/ai/CaptionProposalInbox.swift` |
| 198 | Caption assistant chat | Plain-language caption editing in the agent window | HYBRID | `caption_propose_edits`, `caption_search_segments`, `caption_list_segments` | `film-workflow/clients/agent/AgentSkills.swift` |
| 199 | Translation: Apple on-device | Apple Translation framework, offline and free; UI only | LOCAL | — | `film-workflow/clients/captions/translation/AppleTranslationRunner.swift` |
| 200 | Translation: AI backend | LLM translation keeping placeholders; batches halve on overflow | HYBRID | `caption_translate` | `film-workflow/clients/captions/translation/AICaptionTranslationRunner.swift` |
| 201 | Per-caption translation fix | Rewrite or clear one caption's translation | LOCAL | `caption_update_segment`, `caption_propose_edits` | `film-workflow/models/CaptionTranslation.swift` |
| 202 | Transcript language relabel | Change the recorded language without translating | LOCAL | — | `film-workflow/clients/captions/CaptionLanguage.swift` |
| 203 | Karaoke retimer | Press Space at each caption boundary while audio plays | LOCAL | — | `film-workflow/views/caption/CaptionRetimeSheet.swift` |
| 204 | Per-word timing inspector | Word-level ruler; drag a boundary; keep-within or ripple mode | LOCAL | — | `film-workflow/views/caption/CaptionWordInspectorView.swift` |
| 205 | Segment editor + list tools | Caption list, sheet editor, Close Gaps Under 300 ms | LOCAL | `caption_update_segment` | `film-workflow/views/caption/CaptionSegmentListView.swift` |
| 206 | Music lyrics (captions on music) | Timed lyrics on music takes; merge captions as lyrics | LOCAL | — | `film-workflow/clients/captions/MusicLyrics.swift` |
| 207 | Align caption clip with original audio (captions view) | Timeline action moving a caption clip to its source audio clip | LOCAL | — | `film-workflow/document/CaptionAudioAlignment.swift` |
| 232 | Plain-speech extraction and authored-pause map | Strip shortcodes to spoken words and sum authored pauses for caption timing | LOCAL | `caption_create` | `film-workflow/clients/ShortcodeExpander.swift`<br>`film-workflow/models/CaptionReferenceUnit.swift` |
| 241 | Auto-captions on narration (script as text, speech service as clock) | captionsEnabled narration takes create linked script-exact caption projects | HYBRID | `caption_create` | `film-workflow/clients/services/NarrativeGenerationService.swift`<br>`film-workflow/models/NarrativeProject.swift` |
| 327 | CaptionProject / CaptionSegment data | Stored caption settings, versions, segments | LOCAL | `footage_update`, `footage_get`, `caption_create`, `caption_list_segments`, `caption_update_segment`, `caption_versions` | `film-workflow/models/CaptionProject.swift`<br>`film-workflow/models/CaptionSegment.swift` |
| 379 | Cloud transcription via server | OpenAI/Azure/Gemini transcription billed per audio-minute | SERVER | `caption_transcribe` | `website/app/api/v1/ai/transcriptions/route.ts` |
| 388 | Marketplace music lyric tracks | Per-language SRT/WebVTT lyric tracks with limits | SERVER | — | `website/lib/marketplace/lyrics.ts` |

### Generative audio (music, TTS) (34)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 22 | narration_generate | Speaks a narration item's paragraphs (Gemini or Azure) through RxLab; keeps audio + transcript as a take. Credits | SERVER | `narration_generate` | `film-workflow/clients/mcp/handlers/MCPGenerateHandlers.swift`<br>`film-workflow/clients/backend/BackendSpeechClient.swift` |
| 23 | music_generate | Generates a music item's track (Lyria) as a take. Credits | SERVER | `music_generate` | `film-workflow/clients/mcp/handlers/MCPGenerateHandlers.swift`<br>`film-workflow/clients/backend/BackendMusicClient.swift` |
| 26 | Podcast tools (line-by-line narration editing) | Create multi-speaker narration, list voices (static catalog), add/update/remove lines, patch settings. Data only; audio needs narration_generate | LOCAL | `podcast_create`, `podcast_list_speakers`, `podcast_add_content`, `podcast_update_content`, `podcast_remove_content`, `podcast_update_settings` | `film-workflow/clients/mcp/handlers/MCPPodcastHandlers.swift` |
| 213 | Music generation (Lyria 3 Pro) | Prompt → server job → poll → download → GeneratedMusic take | SERVER | `music_generate` | `film-workflow/clients/services/MusicGenerationService.swift`<br>`website/app/api/v1/ai/music/route.ts` |
| 214 | Music prompt builder (structured editor mode) | Vibe, genre, BPM, key, instruments, timed sections and lyrics → one text prompt | LOCAL | `footage_update`, `music_generate` | `film-workflow/clients/PromptBuilder.swift` |
| 215 | Music free-prompt mode | Free text appended as 'Additional instructions' | LOCAL | `footage_update` | `film-workflow/clients/services/MusicGenerationService.swift` |
| 216 | Music reference images | Images sent base64 with the prompt; server allows 4, UI allows 10 | HYBRID | `footage_duplicate`, `footage_get` | `film-workflow/views/music/MusicProjectParametersView.swift`<br>`website/app/api/v1/ai/music/route.ts` |
| 217 | Music output format (MP3/WAV) | Format picker that does not work; Lyria always returns MP3 | SERVER | `footage_update` | `website/app/api/v1/ai/music/route.ts` |
| 218 | Lyrics text returned with music | Lyria's text parts stored as lyricsText, not aligned | SERVER | `music_generate`, `footage_get` | `website/app/api/v1/ai/music/route.ts` |
| 219 | Song structure and lyrics editors | GUI editors for timed sections and lyric blocks | LOCAL | `footage_update` | `film-workflow/views/music/SongStructureEditorView.swift` |
| 220 | Music prompt preview sheet | Shows the assembled prompt before generating | LOCAL | — | `film-workflow/views/editor/inspectors/MusicInspector.swift` |
| 221 | Music takes: history, playback, export, delete, timeline | Takes list with player, export, delete, drag to timeline | LOCAL | `footage_get`, `sequence_add_clip` | `film-workflow/views/music/GeneratedMusicListView.swift` |
| 222 | Narration generation (TTS) with provider dispatch | Gemini or Azure TTS through RxLab; take saved with transcript/SSML | SERVER | `narration_generate` | `film-workflow/clients/services/NarrativeGenerationService.swift`<br>`website/app/api/v1/ai/speech/route.ts` |
| 223 | Gemini TTS (single or two speakers) | Natural-language transcript to Gemini TTS; PCM wrapped as WAV on the server | SERVER | `narration_generate`, `podcast_update_settings`, `footage_update` | `film-workflow/clients/NarrativePromptBuilder.swift` |
| 224 | Azure Neural/HD TTS via SSML | SSML built on the Mac, synthesised on the server | HYBRID | `narration_generate`, `podcast_update_settings`, `footage_update` | `film-workflow/clients/NarrativePromptBuilder.swift` |
| 225 | Azure long-script batching | Script split into ≤1200-char speak documents, sent sequentially | LOCAL | `narration_generate` | `film-workflow/clients/NarrativePromptBuilder.swift` |
| 226 | Azure audio stitching | Per-batch MP3/WAV joined locally | LOCAL | `narration_generate` | `film-workflow/clients/AzureAudioStitcher.swift` |
| 227 | Azure voice pre-flight validation | Checks voice names against the live list with did-you-mean suggestions | HYBRID | `narration_generate` | `film-workflow/clients/services/NarrativeGenerationService.swift` |
| 228 | Azure voice catalogue (proxy + 24h disk cache) | Voice list via RxLab proxy cached 24 h | HYBRID | — | `film-workflow/clients/AzureVoiceStore.swift` |
| 229 | Voice preview (Azure + Gemini) | Play button synthesises a sample; each uncached preview is billed | HYBRID | — | `film-workflow/clients/AzureVoicePreviewer.swift`<br>`film-workflow/clients/GeminiVoicePreviewer.swift` |
| 230 | Localized preview text via Apple Translation | Sample sentence translated on-device for non-English voices | LOCAL | — | `film-workflow/views/narrative/AzureVoicePreviewButton.swift` |
| 231 | Delivery shortcodes ({{...}}) | 23-entry inline cue language → SSML (Azure) or bracket tags (Gemini) | LOCAL | `podcast_add_content`, `podcast_update_content`, `footage_update` | `film-workflow/clients/ShortcodeExpander.swift` |
| 233 | Transcript editor with shortcode chips | Paragraph list with atomic shortcode chips and emotion menus | LOCAL | `podcast_add_content`, `podcast_update_content`, `podcast_remove_content` | `film-workflow/views/narrative/TranscriptEditorView.swift` |
| 234 | Speaker casting and Azure voice parameters | Speakers with voice, pitch, rate, volume, role, style degree | LOCAL | `podcast_update_settings`, `podcast_list_speakers`, `footage_update` | `film-workflow/views/narrative/NarrativeProjectParametersView.swift` |
| 235 | Provider switch with per-provider voice memory (GUI only) | GUI remembers each speaker's Gemini and Azure voice; MCP switch does not | LOCAL | — | `film-workflow/views/narrative/NarrativeProjectParametersView.swift` |
| 239 | Narration prompt/SSML preview sheet | Shows the assembled Gemini transcript or Azure SSML | LOCAL | — | `film-workflow/clients/NarrativePromptBuilder.swift` |
| 240 | Narration progress + cancel | Batch progress, stitching and captioning phases with Cancel | LOCAL | — | `film-workflow/views/narrative/NarrativeGenerationProgressView.swift` |
| 242 | Narration takes: history, playback, export, delete, timeline | Takes list with provider, speakers, duration; drag to timeline | LOCAL | `footage_get`, `sequence_add_clip` | `film-workflow/views/narrative/GeneratedNarrativeListView.swift` |
| 323 | MusicProject / GeneratedMusic data | Stored music settings and cascade-deleted takes | LOCAL | `footage_update`, `footage_get`, `music_generate` | `film-workflow/models/MusicProject.swift` |
| 324 | NarrativeProject / GeneratedNarrative data | Stored narration settings, speakers, paragraphs, takes | LOCAL | `footage_update`, `footage_get`, `narration_generate` | `film-workflow/models/NarrativeProject.swift` |
| 375 | Narration TTS via server (Azure / Gemini) | Server speech route, billed per character or audio-second | SERVER | `narration_generate` | `website/app/api/v1/ai/speech/route.ts` |
| 376 | Azure voice catalog proxy | Server proxy of Azure's voice list | SERVER | — | `website/app/api/v1/ai/voices/route.ts` |
| 377 | Voice preview (billed) | Previews go through the metered speech route | SERVER | — | `film-workflow/clients/AzureVoicePreviewer.swift` |
| 378 | Music via Lyria 3 Pro (async job) | Server Lyria job, output in S3, polled | SERVER | `music_generate` | `website/app/api/v1/ai/music/route.ts` |

### Generative image and video (32)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 24 | image_generate | Generates an image item's picture as a take. Credits | SERVER | `image_generate` | `film-workflow/clients/mcp/handlers/MCPGenerateHandlers.swift`<br>`film-workflow/clients/backend/BackendImageClient.swift` |
| 25 | video_generate / video_job_status / video_resume | Veo clip as a take (blocks for minutes); check a pending job; collect a submitted job without resubmitting | SERVER | `video_generate`, `video_job_status`, `video_resume` | `film-workflow/clients/mcp/handlers/MCPGenerateHandlers.swift`<br>`film-workflow/clients/backend/BackendVideoClient.swift` |
| 38 | remotion_generate_image | Prompt → image in public/generated/ (optional transparent); credits | SERVER | `remotion_generate_image` | `film-workflow/clients/mcp/handlers/RemotionMCPHandlers.swift`<br>`film-workflow/clients/RemotionTools.swift` |
| 133 | Generate marketplace content/covers | Admin generates covers, footage or music in an authoring workspace; credits | SERVER | `marketplace_generate`, `marketplace_job_status`, `marketplace_retry`, `marketplace_workspace` | `film-workflow/clients/marketplace/MarketplaceAuthoringService.swift` |
| 164 | AI image generation into a composition | Prompt → public/generated/ image via RxLab; transparency guessed from model name | SERVER | `remotion_generate_image` | `film-workflow/clients/RemotionTools.swift`<br>`film-workflow/clients/backend/BackendImageClient.swift` |
| 247 | Image item (prompt → still) with takes | Image library item; prompt-only generation via RxLab saved as takes | SERVER | `footage_create`, `image_generate` | `film-workflow/clients/services/ImageGenerationService.swift`<br>`website/app/api/v1/ai/images/route.ts` |
| 248 | Image model routing: Google direct vs Vercel AI Gateway | Server routes Imagen/Gemini to Google, others to the AI Gateway | SERVER | `image_generate` | `website/app/api/v1/ai/images/route.ts`<br>`website/lib/ai/catalog.ts` |
| 249 | Google-style image parameters | 14 aspect ratios, 512-4K resolution | SERVER | `footage_update` | `film-workflow/models/Enums/ImageGenEnums.swift` |
| 250 | OpenAI/gateway-style image parameters | Size, quality, format, compression, background, transparent | SERVER | `footage_update` | `film-workflow/models/Enums/ImageGenEnums.swift` |
| 251 | Per-item image model picker + account default | Per-item model from the curated catalog; stale ids replaced | HYBRID | `models_list`, `footage_update` | `film-workflow/views/imagegen/ImageGenProjectParametersView.swift` |
| 252 | Generated image takes gallery | Grid of takes with preview, copy path, reveal, delete | LOCAL | `footage_get` | `film-workflow/views/imagegen/GeneratedImageListView.swift` |
| 253 | Remotion inline image generation | Image straight into a composition's public/generated/ | SERVER | `remotion_generate_image` | `film-workflow/clients/RemotionTools.swift` |
| 254 | Video item (Veo) generate → take | Veo job submitted via RxLab, polled, downloaded, saved as a take | SERVER | `footage_create`, `video_generate` | `film-workflow/clients/services/VideoGenerationService.swift`<br>`website/app/api/v1/ai/videos/route.ts` |
| 255 | Veo parameter set | Prompt, negative prompt, aspect, resolution, duration, person gen, audio, count, seed | SERVER | `footage_update` | `film-workflow/models/Enums/VideoGenEnums.swift`<br>`website/lib/ai/veo.ts` |
| 256 | Per-model capability gating / clamp (VeoModelFamily) | Parameters clamped to a legal combination per Veo family, in Swift and TS | HYBRID | `footage_update` | `film-workflow/models/Enums/VideoGenEnums.swift`<br>`website/lib/ai/veo.ts` |
| 257 | Image-to-video: first frame / last frame interpolation | Optional first/last frames sent inline; GUI only | SERVER | — | `film-workflow/views/videogen/VideoGenProjectParametersView.swift` |
| 258 | Reference images (asset consistency) | Reference images for subject consistency on Veo 3.1; GUI only | SERVER | — | `film-workflow/views/videogen/VideoGenProjectParametersView.swift` |
| 259 | Video model picker (live catalog) | Veo models from Google's live list, filtered by price rows | SERVER | `models_list`, `footage_update` | `website/lib/ai/google-models.ts` |
| 260 | Resumable video jobs (persisted job handle) | Job id and start time saved on the item before waiting; Resume never resubmits | HYBRID | `video_job_status`, `video_resume`, `footage_get` | `film-workflow/clients/services/VideoGenerationService.swift`<br>`film-workflow/models/VideoGenProject.swift` |
| 261 | Video progress sheet + stop-waiting | Stage modal; cancel only stops waiting | LOCAL | — | `film-workflow/views/videogen/VideoGenProgressSheet.swift` |
| 262 | Server-side Veo job lifecycle (submit / poll-finalize / store) | Reserve, submit, poll, single finalizer lock, store in S3, bill | SERVER | `video_generate`, `video_resume` | `website/lib/ai/video-jobs.ts`<br>`website/app/api/v1/jobs/[jobId]/route.ts` |
| 263 | Veo 2 multi-clip (numberOfVideos 1–2) | Bills for every sample, delivers only the first | SERVER | `footage_update`, `video_generate` | `website/lib/ai/video-jobs.ts` |
| 264 | Local poster frame + probe for generated clips | JPEG poster at ~0.5 s and width/height/duration probe | LOCAL | — | `film-workflow/utils/VideoThumbnailer.swift` |
| 265 | Generated video takes list | Grid of video takes with preview and actions | LOCAL | `footage_get` | `film-workflow/views/videogen/GeneratedVideoListView.swift` |
| 266 | Generated takes → timeline | Generate tools return a sourceId for sequence_add_clip | LOCAL | `image_generate`, `video_generate`, `video_resume`, `sequence_add_clip` | `film-workflow/clients/mcp/handlers/MCPGenerateHandlers.swift`<br>`film-workflow/document/DocumentMediaResolver.swift` |
| 267 | Duplicate image/video item | Copies parameters and reference files, not takes | LOCAL | `footage_duplicate` | `film-workflow/clients/mcp/handlers/MCPLibraryHandlers.swift` |
| 270 | Marketplace admin generation (covers + footage) | Admin cover images and Veo footage for items | SERVER | `marketplace_generate`, `marketplace_job_status`, `marketplace_retry` | `film-workflow/clients/marketplace/MarketplaceAuthoringService.swift` |
| 272 | Deferred/unimplemented video providers & ops | No Sora, no Veo extension/edit/remix, no gateway video | — | — | `docs/video-generation.md` |
| 325 | ImageGenProject / GeneratedImage data | Stored image settings and takes | LOCAL | `footage_update`, `footage_get`, `image_generate` | `film-workflow/models/ImageGenProject.swift` |
| 326 | VideoGenProject / GeneratedVideo data | Stored Veo settings, frames and pendingJob* fields | LOCAL | `footage_update`, `footage_get`, `video_generate`, `video_job_status`, `video_resume` | `film-workflow/models/VideoGenProject.swift` |
| 380 | Image generation via server | Google direct or Vercel AI Gateway image route | SERVER | `image_generate` | `website/app/api/v1/ai/images/route.ts` |
| 381 | Veo video generation (submit + poll) | Server Veo submit and job polling | SERVER | `video_generate`, `video_job_status`, `video_resume` | `website/app/api/v1/ai/videos/route.ts`<br>`website/lib/ai/video-jobs.ts` |

### Motion graphics and overlays (Remotion) (19)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 36 | Remotion source file tools | List, read (200KB cap), write and exact-edit a composition's source; protected config files; fixed import catalog | LOCAL | `remotion_list_files`, `remotion_read_file`, `remotion_write_file`, `remotion_edit_file` | `film-workflow/clients/mcp/handlers/RemotionMCPHandlers.swift`<br>`film-workflow/clients/RemotionTools.swift` |
| 37 | remotion_take_screenshot / remotion_take_screenshots | One PNG at a time, or 2-8 evenly spaced frames, returned as image content (480x270) | LOCAL | `remotion_take_screenshot`, `remotion_take_screenshots` | `film-workflow/clients/mcp/handlers/RemotionMCPHandlers.swift`<br>`film-workflow/clients/RemotionStillCapture.swift` |
| 39 | Remotion asset attach/detach | Add/remove images (max 10) and audio into a composition's public/ folder | LOCAL | `remotion_add_image`, `remotion_remove_image`, `remotion_add_audio`, `remotion_remove_audio` | `film-workflow/clients/mcp/handlers/RemotionMCPHandlers.swift` |
| 127 | Marketplace fonts | Installed fonts registered for the app process; appear in caption style picker | LOCAL | `marketplace_install` | `film-workflow/clients/marketplace/MarketplaceFonts.swift` |
| 145 | RxRemotion native engine (no Node/Bun/Chromium/Studio) | Swift package compiling, previewing and rendering Remotion TSX inside system WebKit, encoding with AVFoundation. Validation.md: "Do not distribute" yet | LOCAL | — | `Packages/RxRemotion/README.md`<br>`Packages/RxRemotion/Sources/RxRemotion/RemotionEngine.swift`<br>`Packages/RxRemotion/Validation.md` |
| 146 | In-WebView esbuild-wasm compilation with fixed import catalog | esbuild-wasm bundles src/index.ts; bare imports only via a 20-key catalog of prebuilt vendor chunks | LOCAL | — | `Packages/RxRemotion/Browser/compiler.js`<br>`Packages/RxRemotion/Sources/RxRemotion/Resources/Web/catalog.json` |
| 147 | Scoped loopback resource server | 127.0.0.1 listener with random UUID path token serving runtime, project files, frames, maps | LOCAL | — | `Packages/RxRemotion/Sources/RxRemotion/ResourceServer.swift` |
| 148 | Compilation cache + source/render fingerprinting | Compiled output and renders keyed by source/asset/size/fps/alpha/map-settings hash | LOCAL | — | `Packages/RxRemotion/Sources/RxRemotion/CompilationCache.swift`<br>`film-workflow/clients/services/RemotionRenderService.swift` |
| 149 | Live composition preview player (native transport) | WKWebView @remotion/player driven by native transport; hot reload on source change | LOCAL | `footage_create` | `film-workflow/views/remotion/RemotionPlayerWebView.swift`<br>`Packages/RxRemotion/Browser/host.tsx` |
| 150 | Deterministic frame capture (virtual clock) | capture.js fakes time, seeds randomness, pumps rAF, rejects non-deterministic CSS/APIs | LOCAL | — | `Packages/RxRemotion/Browser/capture.js`<br>`Packages/RxRemotion/Compatibility.md` |
| 151 | Alpha recovery via black/white matte snapshots | Each frame captured on black and white; C routine rebuilds premultiplied RGBA | LOCAL | — | `Packages/RxRemotion/Sources/RxRemotion/RemotionWebPage.swift`<br>`Packages/RxRemotion/Sources/RxRemotionPixels/include/RxRemotionPixels.h` |
| 154 | Native audio mixing of Remotion <Audio>/<Video> sound | Page reports audio assets; Swift mixes them in an AVMutableComposition | LOCAL | — | `Packages/RxRemotion/Sources/RxRemotion/MovieExporter.swift` |
| 155 | Native OffthreadVideo adapter for embedded video | Embedded video frames decoded natively and swapped in as images during export | LOCAL | — | `Packages/RxRemotion/Sources/RxRemotion/NativeMedia.swift` |
| 156 | Maps in compositions (MapKit + OpenStreetMap + Mapbox) | MapKit snapshots, Leaflet OSM with proxied tiles, Mapbox with the user's token | HYBRID | — | `Packages/RxRemotion/Browser/maps.tsx`<br>`Packages/RxRemotion/Sources/RxRemotion/RemotionMaps.swift` |
| 157 | Bundled 3D / particles libraries | three, R3F, Drei, @remotion/three, tsParticles importable without install | LOCAL | `remotion_write_file`, `remotion_edit_file` | `Packages/RxRemotion/README.md`<br>`Packages/RxRemotion/Compatibility.md` |
| 160 | No-AI default composition seed | Default template: fade-in title of the project name on the theme colour | LOCAL | `footage_create` | `film-workflow/clients/RemotionCodeBuilder.swift` |
| 161 | Remotion parameters inspector | Form for text, duration, colour, size, fps, prompt, images, audio; patches COMPOSITION_* constants | LOCAL | `footage_update`, `footage_get` | `film-workflow/views/remotion/RemotionParametersView.swift` |
| 170 | Read-only source viewer with TSX highlighting | Sheet listing composition files with syntax highlighting; no in-app code editor | LOCAL | — | `film-workflow/views/remotion/RemotionSourceSheetView.swift` |
| 322 | RemotionProject + RemotionRender cache | Composition source folder and hash-keyed render cache | LOCAL | `footage_create`, `footage_update`, `footage_get`, `remotion_list_files`, `remotion_read_file`, `remotion_write_file`, `remotion_edit_file` | `film-workflow/models/RemotionProject.swift`<br>`film-workflow/models/RemotionRender.swift` |

### Export (13)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 21 | sequence_render / sequence_renders | Render a sequence (h264/hevc/none, aac/none, resolution, format, captions burn_in/embedded/sidecar/none); list kept versions. Synchronous, no progress | LOCAL | `sequence_render`, `sequence_renders` | `film-workflow/clients/mcp/handlers/MCPSequenceHandlers.swift` |
| 35 | caption_export | Write vtt/srt/text/json at sentence, word or word_karaoke granularity; per-language files | LOCAL | `caption_export` | `film-workflow/clients/mcp/handlers/MCPCaptionHandlers.swift` |
| 104 | Sequence render (AVFoundation export) | H.264 or HEVC highest-quality presets, AAC, 480p-4K, mp4/mov/m4a; versions under Renders/Sequences. No bitrate, ProRes or fps override | LOCAL | `sequence_render`, `sequence_renders` | `Packages/RxVideoEditor/Sources/VideoEditorCore/Export/TimelineExporter.swift`<br>`film-workflow/clients/services/SequenceRenderService.swift` |
| 134 | Marketplace preview renderer | ≤15 s 720p H.264 preview + cover per kind; mock images cost credits | HYBRID | `marketplace_render_preview`, `marketplace_job_status`, `marketplace_retry` | `film-workflow/clients/marketplace/MarketplacePreviewRenderer.swift` |
| 152 | Native movie/still export (H.264 MP4, ProRes 4444 MOV, PNG) | AVAssetWriter H.264 or ProRes 4444 with alpha; native audio remux; PNG stills | LOCAL | — | `Packages/RxRemotion/Sources/RxRemotion/MovieExporter.swift`<br>`Packages/RxRemotion/Sources/RxRemotion/NativeVideoEncoder.swift` |
| 153 | Parallel WebView render workers | 1-4 WebView workers, auto-sized to cores/RAM/frame size | LOCAL | — | `Packages/RxRemotion/Sources/RxRemotion/RemotionTypes.swift`<br>`Packages/RxRemotion/Validation.md` |
| 168 | Render Version (into film) and Export to Disk | 16:9 presets 480p-4K at 24/30/60 fps; render as version or export to disk | LOCAL | — | `film-workflow/views/remotion/RemotionExportSheet.swift`<br>`film-workflow/views/remotion/RemotionExportToDisk.swift` |
| 169 | Render versions list | List a composition's renders: play, reveal, export, delete | LOCAL | `footage_get` | `film-workflow/views/remotion/RemotionRenderListView.swift` |
| 173 | Sequence export renders stale compositions first | Stale Remotion clips re-rendered at sequence size before the normal exporter runs | LOCAL | `sequence_render` | `film-workflow/clients/services/SequenceRenderService.swift` |
| 209 | Caption file export (editor / MCP) | VTT/SRT/text/JSON with granularity, speaker style, translation mode, per-language files | LOCAL | `caption_export` | `film-workflow/clients/captions/CaptionExporter.swift` |
| 210 | Sequence render caption delivery | Burn-in, embedded tx3g per language, SRT/VTT sidecars, or none | LOCAL | `sequence_render` | `docs/caption-export.md`<br>`film-workflow/clients/services/SequenceRenderService.swift` |
| 307 | Shared recording renderer for preview, thumbnails and export | One RecordingRenderer for compositor, layered preview and thumbnails | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorCore/Composition/RecordingRenderer.swift` |
| 321 | SequenceRender versions | Render rows with file under Renders/Sequences/<id>/vNNN.mp4 | LOCAL | `sequence_render`, `sequence_renders` | `film-workflow/models/SequenceRender.swift` |

### Agent and MCP surface (45)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 0 | Embedded MCP HTTP server | In-app MCP server on POST /mcp: JSON-RPC 2.0, protocol 2025-03-26, serverInfo film-workflow 0.1.0; initialize, tools/list, tools/call, ping. Hand-rolled HTTP/1.1, no SSE (GET /mcp = 405), so long tools block the response | LOCAL | — | `film-workflow/clients/mcp/MCPServer.swift`<br>`film-workflow/clients/mcp/MCPRouter.swift`<br>`film-workflow/clients/mcp/MCPProtocol.swift` |
| 1 | MCP port, binding and bearer-token auth | Base port 7711, probes to +9; local-only unless "All interfaces"; Bearer token on every POST, localhost included; token in Keychain, created only when MCP is enabled; no TLS | LOCAL | — | `film-workflow/config/MCPSettings.swift`<br>`film-workflow/clients/mcp/MCPRouter.swift` |
| 2 | Connect external agent (Claude Code one-liner) | Settings shows a copyable `claude mcp add --transport http film <url> -H "Authorization: Bearer <token>"` | LOCAL | — | `film-workflow/views/settings/MCPSettingsView.swift` |
| 3 | Film routing: `film` argument and X-RxFilm-Document header | Optional `film` arg injected into film-scoped tools; the header pins a session; otherwise the active window's film. Unknown header id silently falls back | LOCAL | `film_list` | `film-workflow/clients/mcp/MCPToolRegistry.swift`<br>`film-workflow/clients/mcp/MCPRouter.swift` |
| 55 | web_read | Fetch a public page's title, text and large images directly (5 MB, 15 s). SSRF check covers literal IPs and local names only | LOCAL | `web_read` | `film-workflow/clients/mcp/handlers/MCPWebHandlers.swift` |
| 56 | Simple-mode wizard tools | Present templates/options, skip templates, report progress; park a page on the wizard session. Useless to external clients | LOCAL | `wizard_present_templates`, `wizard_skip_templates`, `wizard_present_options`, `wizard_report_progress` | `film-workflow/clients/mcp/handlers/MCPWizardHandlers.swift`<br>`docs/simple-mode.md` |
| 57 | Agent window (system-wide, multi-thread) | One app-wide agent window with concurrent threads, each targeting the film or one item; /new /clear /compact /stop | LOCAL | — | `film-workflow/views/agent/AgentWindowView.swift`<br>`film-workflow/clients/agent/AgentToolPolicy.swift` |
| 58 | Agent engines (five backends) | Apple Intelligence, OpenAI-compatible endpoint, RxLab subscription chat, Claude Code CLI, Codex CLI; all reach tools through the app's own MCP server | HYBRID | — | `film-workflow/clients/agent/AgentBackend.swift`<br>`film-workflow/clients/agent/AgentClientFactory.swift` |
| 59 | AgentMCPBridge (in-app agent to own MCP server) | Hands every engine the loopback /mcp URL with Bearer and film header; starts the server on demand. Latent 401 if MCP was never enabled (no token) | LOCAL | — | `film-workflow/clients/agent/AgentMCPBridge.swift`<br>`film-workflow/config/MCPSettings.swift` |
| 60 | Claude Code / Codex embedding: unsandboxed, pre-approved built-ins | CLI engines get the app tools plus Bash, Edit, Write, WebFetch etc., all pre-approved; Codex runs dangerFullAccess | LOCAL | — | `film-workflow/clients/agent/AgentToolPolicy.swift`<br>`film-workflow/clients/agent/AgentClientFactory.swift` |
| 61 | AgentToolPolicy write policy (review vs direct) | 'review' withholds direct caption edits/transcribe; footage_delete and folder_delete always withheld. In-app agent only; external clients unfiltered | LOCAL | `caption_propose_edits`, `caption_update_segment`, `caption_transcribe`, `footage_delete`, `folder_delete` | `film-workflow/clients/agent/AgentToolPolicy.swift`<br>`film-workflow/config/AgentSettings.swift` |
| 62 | Simple-mode tool allowlist | 28 named app tools + 4 wizard + 11 Remotion (43); no built-ins; no video, render or recording | LOCAL | — | `film-workflow/clients/agent/AgentToolPolicy.swift` |
| 63 | AgentSkills (prompt-embedded know-how) | Four static skill blocks rendered into the system prompt when their tools are offered | LOCAL | — | `film-workflow/clients/agent/AgentSkills.swift`<br>`film-workflow/clients/agent/AgentPrompts.swift` |
| 64 | Agent system prompt (AgentPrompts) | Shared context: focused window (untrusted), film model, built-ins block, target, tools, rules, skills, compaction prompt | LOCAL | — | `film-workflow/clients/agent/AgentPrompts.swift` |
| 65 | Per-thread model and thinking-level pickers | Pin model and effort per thread (Claude, Codex, subscription catalogs) | LOCAL | — | `film-workflow/clients/agent/AgentModelCatalog.swift`<br>`film-workflow/views/agent/AgentEngineMenu.swift` |
| 67 | Tool-call cards in transcript | One-line card per tool call with a detail sheet; special rows for wizard, marketplace, proposals | LOCAL | — | `film-workflow/views/agent/AgentToolCallCard.swift`<br>`film-workflow/clients/agent/AgentToolLabels.swift` |
| 87 | Agent follow-along playhead focus | After agent clip edits, editor selects the changed clip and moves the playhead so the user sees the agent work | LOCAL | `sequence_add_clip`, `sequence_set_timeline`, `sequence_remove_clip` | `film-workflow/document/TimelineFocus.swift`<br>`film-workflow/views/editor/EditorWindowView.swift` |
| 88 | Whole-timeline JSON replace (agent) | Read full JSON, edit, write back; every clip re-inserted through editor rules. Gotcha: silently resets track alias and pin; not undoable | LOCAL | `sequence_get`, `sequence_set_timeline` | `film-workflow/clients/mcp/handlers/MCPSequenceHandlers.swift`<br>`Packages/RxVideoEditor/Sources/VideoEditorCore/Model/Timeline.swift` |
| 89 | Agent 'Assembling a sequence' skill and tool policy | Built-in skill telling the agent how to use the sequence tools; text partly stale | LOCAL | `sequence_list`, `sequence_create`, `sequence_get`, `sequence_add_track`, `sequence_reorder_tracks`, `sequence_add_clip`, `sequence_remove_clip`, `sequence_set_timeline`, `sequence_render` | `film-workflow/clients/agent/AgentSkills.swift`<br>`film-workflow/clients/agent/AgentToolPolicy.swift` |
| 130 | Admin authoring: drafts, categories, publish, delete | Admin grids, drafts, categories, publish/unpublish, delete | SERVER | `marketplace_create`, `marketplace_update`, `marketplace_publish`, `marketplace_list`, `show_marketplace_item` | `film-workflow/clients/marketplace/MarketplaceAuthoringService.swift` |
| 131 | Server-defined authoring form schema | Editor fields built from a server form schema | SERVER | — | `film-workflow/clients/marketplace/MarketplaceFormSchema.swift`<br>`website/lib/marketplace/form-schema.ts` |
| 132 | Upload pipeline (presigned R2) | Presigned PUT upload, local measurement, finalize; retryable jobs | HYBRID | `marketplace_upload`, `marketplace_job_status`, `marketplace_retry` | `film-workflow/clients/marketplace/MarketplaceAuthoringService.swift` |
| 135 | Create Marketplace Item from film piece | 'Create Marketplace Item…' on library/timeline/take lists seeds a draft (admin) | HYBRID | — | `film-workflow/views/marketplace/MarketplaceSeedHost.swift` |
| 136 | Portable project template definition (v1) | JSON: prompt, style, guidance, size, fps, shots, footage requirements, dependencies; no media or paths | LOCAL | `marketplace_create`, `marketplace_update`, `marketplace_get` | `film-workflow/clients/marketplace/ProjectTemplateDefinition.swift` |
| 137 | Extract template from film | Turn a sequence into a template draft (admin); GUI opens an agent chat | HYBRID | `project_template_from_film`, `marketplace_update`, `marketplace_render_preview`, `show_marketplace_item` | `film-workflow/clients/marketplace/ProjectTemplateService.swift` |
| 139 | Marketplace chat card | Native card in chat with preview, price, Buy, Use in Current Film, Install | HYBRID | `show_marketplace_item` | `film-workflow/views/marketplace/MarketplaceChatCard.swift` |
| 140 | Simple mode wizard (RxFilmTemplates) | Guided New Film flow: engine → brief → research → template → options → build → preview | HYBRID | `wizard_present_templates`, `wizard_skip_templates`, `wizard_present_options`, `wizard_report_progress`, `web_read`, `marketplace_list`, `marketplace_get`, `project_template_apply` | `Packages/RxFilmTemplates/Sources/FilmTemplateKit/FilmTemplateCatalog.swift`<br>`docs/simple-mode.md` |
| 141 | json-render option pages | SwiftUI renderer for agent-written json-render specs | LOCAL | `wizard_present_options` | `Packages/RxFilmTemplates/Sources/JSONRenderUI/JSONRenderView.swift` |
| 142 | web_read (Simple-mode research) | Public page fetch used for wizard research; IP-literal SSRF block only | LOCAL | `web_read` | `film-workflow/clients/mcp/handlers/MCPWebHandlers.swift` |
| 162 | Composition source file tools | List, read, write, exact-edit composition files; protected paths | LOCAL | `remotion_list_files`, `remotion_read_file`, `remotion_write_file`, `remotion_edit_file` | `film-workflow/clients/mcp/handlers/RemotionMCPHandlers.swift`<br>`film-workflow/clients/RemotionProjectFiles.swift` |
| 163 | Deterministic composition screenshots for agents | One PNG or 2-8 frames at 480x270; a fresh engine per frame | LOCAL | `remotion_take_screenshot`, `remotion_take_screenshots` | `film-workflow/clients/RemotionStillCapture.swift` |
| 165 | Attach/detach image and audio assets | Copy local files into public/upload or public/audio; remove undoes both | LOCAL | `remotion_add_image`, `remotion_remove_image`, `remotion_add_audio`, `remotion_remove_audio` | `film-workflow/clients/mcp/handlers/RemotionMCPHandlers.swift` |
| 166 | Agent Remotion authoring skill + Generate with AI | Opens the agent targeted at a composition; skill: read, edit, sync constants, screenshot before reporting | HYBRID | `remotion_list_files`, `remotion_read_file`, `remotion_write_file`, `remotion_edit_file`, `remotion_take_screenshot`, `remotion_take_screenshots`, `remotion_generate_image`, `footage_get`, `footage_update` | `film-workflow/clients/agent/AgentSkills.swift`<br>`film-workflow/views/remotion/RemotionParametersView.swift` |
| 167 | Simple mode (wizard) Remotion cards | Wizard gets every Remotion tool to author title cards, lower thirds and end cards | HYBRID | `footage_create`, `remotion_write_file`, `remotion_edit_file`, `remotion_take_screenshots` | `film-workflow/clients/agent/AgentToolPolicy.swift`<br>`docs/simple-mode.md` |
| 236 | Podcast tools (agent surface) | Six podcast_* tools; bug: azureVoice vs voice field | LOCAL | `podcast_create`, `podcast_list_speakers`, `podcast_add_content`, `podcast_update_content`, `podcast_remove_content`, `podcast_update_settings` | `film-workflow/clients/mcp/handlers/MCPPodcastHandlers.swift` |
| 237 | footage_* tools for music and narration | Generic library tools; raw-value enum traps silently ignore documented values | LOCAL | `footage_create`, `footage_update`, `footage_get`, `footage_duplicate`, `footage_delete` | `film-workflow/clients/mcp/handlers/MCPLibraryHandlers.swift` |
| 238 | Agent skill + Simple-mode policy for audio generation | Skill steers footage_update → generate; Simple mode excludes podcast tools | LOCAL | `music_generate`, `narration_generate`, `caption_create`, `models_list` | `film-workflow/clients/agent/AgentSkills.swift`<br>`film-workflow/clients/agent/AgentToolPolicy.swift` |
| 268 | Agent 'Generating footage' skill + tool policy | Skill: set params, generate, resume after timeout, never resubmit | LOCAL | `image_generate`, `video_generate`, `video_job_status`, `video_resume`, `models_list`, `footage_update` | `film-workflow/clients/agent/AgentSkills.swift` |
| 290 | Focus observation for the agent (and auto-attach) | Focused window screenshot + Accessibility text auto-attached to agent turns during recording | LOCAL | `recording_focus` | `film-workflow/clients/recording/RecordingSources.swift`<br>`film-workflow/clients/agent/AgentController.swift` |
| 310 | Recording MCP tool set and in-app agent policy | 15 recording tools, all available to in-app conversation threads | LOCAL | `recording_sources`, `recording_focus`, `recording_screenshot`, `recording_get`, `recording_configure`, `recording_start`, `recording_control`, `recording_actions_edit`, `recording_perform_action`, `recording_presentation`, `recording_shortcuts`, `recording_insert_take`, `sequence_link_clips`, `sequence_track_alias`, `recording_pet` | `film-workflow/clients/mcp/handlers/MCPRecordingHandlers.swift`<br>`film-workflow/clients/agent/AgentToolPolicy.swift` |
| 311 | External MCP exposure of recording tools (no policy filter) | Any token holder gets all recording tools incl. real input injection; LAN if bindAll | LOCAL | `recording_perform_action`, `recording_focus`, `recording_screenshot`, `recording_start`, `recording_control` | `film-workflow/clients/mcp/MCPRouter.swift`<br>`film-workflow/clients/mcp/MCPServer.swift` |
| 335 | App-level agent store (Agent.store) | Threads and messages in one app-wide SwiftData store | LOCAL | — | `film-workflow/document/AppModelContainer.swift`<br>`film-workflow/models/AgentThread.swift` |
| 342 | Simple mode engine choice | First wizard page picks the agent engine | HYBRID | — | `film-workflow/views/simplemode/SimpleModeEnginePage.swift` |
| 348 | Simple mode tool allowlist (data-model view) | 43-tool allowlist enforced in filter and allows() | LOCAL | — | `film-workflow/clients/agent/AgentToolPolicy.swift`<br>`film-workflow/models/AgentThreadMode.swift` |
| 382 | Subscription chat proxy | OpenAI-shaped chat to Vercel AI Gateway, billed by tokens, not streamed | SERVER | `caption_translate`, `caption_transcribe` | `website/app/api/v1/ai/chat/route.ts` |

### Project and data model (41)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 5 | film_list | Lists open .rxfilmstudio documents (id, name, path, isActive). No tool opens, creates or closes a film | LOCAL | `film_list` | `film-workflow/clients/mcp/MCPToolRegistry.swift` |
| 7 | footage_list | Library items with kind, folder, take count and newest sourceId; film="*" fans out over every open film | LOCAL | `footage_list` | `film-workflow/clients/mcp/handlers/MCPLibraryHandlers.swift` |
| 8 | footage_get | One item's inspector parameters and takes; a sequence returns its timeline | LOCAL | `footage_get` | `film-workflow/clients/mcp/handlers/MCPLibraryHandlers.swift` |
| 9 | footage_create | Adds a library item of a creatable kind; a Remotion item is seeded and starts its live preview | LOCAL | `footage_create` | `film-workflow/clients/mcp/handlers/MCPLibraryHandlers.swift` |
| 10 | footage_update (inspector parameters) | Patches per-kind inspector fields; foreign keys silently ignored; takes never touched | LOCAL | `footage_update` | `film-workflow/clients/mcp/handlers/MCPLibraryHandlers.swift` |
| 11 | footage_delete | Removes an item, its takes and files (confirm=true). Withheld from the in-app agent, open to external clients | LOCAL | `footage_delete` | `film-workflow/clients/mcp/handlers/MCPLibraryHandlers.swift`<br>`film-workflow/clients/agent/AgentToolPolicy.swift` |
| 12 | footage_duplicate | Copies an item's parameters (not takes) into a new item | LOCAL | `footage_duplicate` | `film-workflow/clients/mcp/handlers/MCPLibraryHandlers.swift` |
| 13 | footage_move | Files an item under a folder or out of one | LOCAL | `footage_move` | `film-workflow/clients/mcp/handlers/MCPLibraryHandlers.swift` |
| 14 | footage_import | Imports a video/audio/image from a disk path; copy (default) or reference in place | LOCAL | `footage_import` | `film-workflow/clients/mcp/handlers/MCPLibraryHandlers.swift` |
| 15 | Library folders | Flat folders: list (per-kind counts), create, rename, delete (items kept) | LOCAL | `folder_list`, `folder_create`, `folder_rename`, `folder_delete` | `film-workflow/clients/mcp/handlers/MCPLibraryHandlers.swift` |
| 66 | Agent transcript persistence and compaction | Threads/messages in an app-wide Agent.store; auto-compaction to a ≤3-sentence summary | LOCAL | — | `film-workflow/document/AppModelContainer.swift`<br>`film-workflow/clients/agent/AgentTranscriptStore.swift` |
| 106 | Timeline persistence (TimelineCodec in SwiftData) | Timeline stored as {formatVersion 3, timeline} JSON in SequenceProject.timelineData; decode failure silently yields an empty timeline | LOCAL | — | `Packages/RxVideoEditor/Sources/VideoEditorCore/Model/TimelineCodec.swift`<br>`film-workflow/models/SequenceProject.swift` |
| 107 | Import media (copy vs reference) | Import sheet: copy into the film or reference via bookmark | LOCAL | `footage_import` | `film-workflow/views/editor/MediaImportSheet.swift`<br>`film-workflow/models/ImportedAsset.swift` |
| 158 | RemotionProject library item + on-disk project folder | SwiftData row (text, duration, colours, paths, size, fps, source) mapped to a src/ + public/ folder | LOCAL | `footage_list`, `footage_get`, `footage_create`, `footage_update`, `footage_delete`, `footage_duplicate`, `footage_move` | `film-workflow/models/RemotionProject.swift`<br>`film-workflow/clients/RemotionCodeBuilder.swift` |
| 159 | RemotionRender versions (render cache) | Versioned render rows stored as vNNN-<hash8>.mp4/.mov; reused on hash match | LOCAL | `footage_get` | `film-workflow/models/RemotionRender.swift`<br>`film-workflow/clients/services/RemotionRenderService.swift` |
| 212 | Caption persistence model | CaptionProject owns CaptionSegment rows; words, translations etc. embedded Codable | LOCAL | — | `film-workflow/models/CaptionProject.swift`<br>`film-workflow/models/CaptionSegment.swift` |
| 244 | Music/Narration SwiftData models | MusicProject/NarrativeProject with cascading take rows; no model field | LOCAL | `footage_get` | `film-workflow/models/MusicProject.swift`<br>`film-workflow/models/NarrativeProject.swift` |
| 308 | Recording storage layout (film format 2) | Per-operation media, Session.json, cursor.png, reference PNGs, action revisions | LOCAL | `recording_get` | `film-workflow/models/ScreenRecordingProject.swift`<br>`docs/screen-recording.md` |
| 309 | Take library management | Takes listed and soft-removed (undoable); thumbnails via real composition | LOCAL | `recording_get` | `film-workflow/clients/recording/RecordingTakeLibrary.swift` |
| 312 | .rxfilmstudio film package | Package dir: Document.json, Workspace.json, Library.store, media folders | LOCAL | `film_list` | `docs/document-package.md`<br>`film-workflow/document/ProjectDocument.swift` |
| 313 | Undocumented package folders | TemplateApplications/, Media/ScreenRecordings/…, Actions/ revisions, Media/Screenshots | LOCAL | `project_template_apply`, `recording_start`, `recording_actions_edit`, `recording_screenshot` | `film-workflow/clients/marketplace/ProjectTemplateService.swift`<br>`film-workflow/clients/recording/RecordingSession.swift` |
| 314 | Document.json metadata and format versioning / migration | formatVersion 2; newer refused; older backed up to a sibling then migrated | LOCAL | — | `film-workflow/document/ProjectDocument.swift` |
| 315 | Per-film SwiftData schema (Library.store) | 18 @Model types; 6 cascade parent→take relationships | LOCAL | `footage_list`, `footage_get` | `film-workflow/document/ProjectDocument.swift`<br>`film-workflow/models/` |
| 316 | GroupableProject library items and FootageKind | 9 footage kinds addressed by one footage_id | LOCAL | `footage_list`, `footage_get`, `footage_create`, `footage_update`, `footage_delete`, `footage_duplicate`, `footage_move` | `film-workflow/models/ProjectGroup.swift`<br>`film-workflow/clients/mcp/handlers/MCPLibraryHandlers.swift` |
| 317 | Library folders (ProjectGroup) | Flat, uniquely named folders | LOCAL | `folder_list`, `folder_create`, `folder_rename`, `folder_delete`, `footage_move` | `film-workflow/models/ProjectGroup.swift` |
| 318 | Imported assets: copy vs reference | Copied into Media/Imported or referenced via bookmark | LOCAL | `footage_import`, `marketplace_add_to_film` | `film-workflow/models/ImportedAsset.swift` |
| 330 | Source-id grammar and DocumentMediaResolver | '<prefix>:<uuid>' source strings resolved to files, cues or 'unrendered' | LOCAL | `footage_list`, `footage_get`, `sequence_add_clip` | `film-workflow/document/DocumentMediaResolver.swift` |
| 331 | Workspace.json per-film panel layout | Splits map and browser flags, debounced writes | LOCAL | — | `film-workflow/document/DocumentPanelLayout.swift` |
| 332 | Persistence model: SwiftData autosave in place | No explicit save; syncing an open package is risky | LOCAL | — | `film-workflow/document/ProjectDocument.swift`<br>`docs/document-package.md` |
| 333 | Multiple open films and `film` routing | Several films open; `film` arg on all but filmless tools | LOCAL | `film_list` | `film-workflow/clients/mcp/MCPToolRegistry.swift`<br>`film-workflow/document/ProjectDocumentController.swift` |
| 334 | New / Open / Recent films | ⌘N template gallery, ⌘⇧N blank film, ⌘O, recents | LOCAL | — | `film-workflow/film_workflowApp.swift`<br>`film-workflow/document/ProjectDocumentController.swift` |
| 337 | Marketplace authoring workspace film (admin) | Hidden per-item authoring film; the only way an agent can make a film | HYBRID | `marketplace_workspace` | `film-workflow/clients/marketplace/MarketplaceAuthoringService.swift` |
| 339 | Marketplace project templates: apply to a film | Apply a v1 template as a new sequence with saved progress | HYBRID | `project_template_apply`, `marketplace_list`, `marketplace_get`, `show_marketplace_item` | `film-workflow/clients/marketplace/ProjectTemplateService.swift`<br>`film-workflow/clients/marketplace/ProjectTemplateDefinition.swift` |
| 340 | Extract a project template from a film (admin) | Sequence → template draft → generalise → preview → publish | HYBRID | `project_template_from_film`, `marketplace_update`, `marketplace_render_preview`, `marketplace_publish`, `marketplace_workspace`, `show_marketplace_item` | `film-workflow/clients/marketplace/ProjectTemplateService.swift` |
| 341 | Simple mode wizard: session state machine | Phase machine from New Film to first cut | HYBRID | `wizard_present_templates`, `wizard_skip_templates`, `wizard_present_options`, `wizard_report_progress`, `web_read` | `film-workflow/clients/simplemode/SimpleModeSession.swift` |
| 343 | Simple mode brief, location and upload import | Brief form, reachability check, uploads copied in | LOCAL | — | `film-workflow/views/simplemode/SimpleModeLocationPage.swift` |
| 344 | Simple mode research and template pick | Agent reads the site, searches templates, presents ranked picks | HYBRID | `web_read`, `marketplace_list`, `marketplace_get`, `wizard_present_templates`, `wizard_skip_templates` | `film-workflow/clients/mcp/handlers/MCPWizardHandlers.swift` |
| 345 | Simple mode style page (agent-authored json-render) | Agent writes an options page as a json-render spec | LOCAL | `wizard_present_options` | `Packages/RxFilmTemplates/Sources/JSONRenderUI/JSONRenderSpec.swift` |
| 346 | Simple mode build, preview and hand-off to the editor | Build via template or sequence tools; live preview; open in editor | HYBRID | `project_template_apply`, `sequence_create`, `sequence_add_clip`, `sequence_set_timeline`, `wizard_report_progress` | `film-workflow/views/simplemode/SimpleModePreviewHost.swift` |
| 349 | Simple mode wizard template catalog (FilmTemplateCatalog) | One built-in guided template: company-intro-video | LOCAL | — | `Packages/RxFilmTemplates/Sources/FilmTemplateKit/FilmTemplateCatalog.swift` |
| 387 | Project template JSON format | Instructions, requirements, dependencies; no local paths | HYBRID | `project_template_apply`, `project_template_from_film` | `website/lib/marketplace/template.ts` |

### Accounts and credits (30)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 4 | show_sign_in_dialog | Opens the native RxLab sign-in dialog if signed out | LOCAL | `show_sign_in_dialog` | `film-workflow/clients/mcp/MCPToolRegistry.swift` |
| 6 | models_list (per-account model catalog) | Account's allowed generation models with credits per unit, filterable by capability | SERVER | `models_list` | `film-workflow/clients/mcp/handlers/MCPModelHandlers.swift`<br>`film-workflow/clients/backend/BackendModelCatalog.swift` |
| 123 | Buy with credits | Buy charges credits via the purchase endpoint; only the user's button can buy | SERVER | — | `film-workflow/clients/marketplace/MarketplaceClient.swift`<br>`film-workflow/clients/marketplace/MarketplaceStore.swift` |
| 182 | Transcription metering | Credits reserved per audio minute, settled per unit | SERVER | `caption_transcribe` | `website/app/api/v1/ai/transcriptions/route.ts`<br>`website/lib/billing/config.ts` |
| 243 | Metered billing for music and speech | Reserve, record unit usage, settle; Lyria bills at least 180 s | SERVER | `music_generate`, `narration_generate` | `website/lib/billing/unit-pricing.ts`<br>`website/app/api/v1/ai/speech/route.ts` |
| 269 | Image/video credit metering | Per-image and per-output-second billing with reservation floors | SERVER | `models_list` | `website/lib/billing/unit-pricing.ts`<br>`website/lib/billing/config.ts` |
| 350 | RxLab sign-in (OAuth PKCE + passkeys) | Native sign-in against auth.rxlab.app; tokens in Keychain | HYBRID | `show_sign_in_dialog` | `film-workflow/auth/AuthManager.swift`<br>`film-workflow/auth/AuthSessionClient.swift` |
| 351 | Session restoration with retry | Saved session restored; transient failures don't sign out | HYBRID | — | `film-workflow/auth/AuthSessionClient.swift` |
| 352 | Server bearer-token verification | Website verifies app bearer tokens via userinfo, cached 60 s | SERVER | — | `website/lib/auth/bearer.ts` |
| 353 | Website account login (Auth.js + @rxtech-lab/authjs-rxlab) | Browser dashboard login | SERVER | — | `website/lib/auth.ts` |
| 354 | Server-driven auth form schema | Localized sign-in/sign-up field schema | SERVER | — | `website/app/api/auth/ui-schema/[flow]/route.ts` |
| 355 | Balance endpoint GET /api/v1/me | User, balance and credit URLs; polled by the app | SERVER | — | `website/app/api/v1/me/route.ts` |
| 356 | Billing summary GET /api/billing | Balance plus purchasable packs | SERVER | — | `website/app/api/billing/route.ts` |
| 357 | Signed-in device tracking | Device sessions listed on the web dashboard | SERVER | — | `website/app/api/v1/me/route.ts`<br>`website/lib/db/schema.ts` |
| 358 | rx-subscription as balance/ledger/Stripe authority | Separate RxLab service holds balances, ledger and Stripe | SERVER | — | `website/lib/billing/subscription.ts` |
| 359 | Reserve -> settle -> release metering | Reserve estimate ×1.5, settle actual, release rest; off unless BILLING_ENABLED="true" | SERVER | — | `website/lib/billing/repository.ts`<br>`website/lib/ai/meter.ts` |
| 360 | Insufficient-credits HTTP 402 | 402 with available/required points mapped to an add-credits error | HYBRID | — | `website/lib/billing/errors.ts`<br>`film-workflow/clients/backend/BackendError.swift` |
| 361 | Usage reconciliation cron | Vercel cron re-prices gateway usage every 10 min | SERVER | — | `website/app/api/cron/reconcile-usage/route.ts` |
| 362 | Hand-maintained unit price table | Per-unit nano-USD rates for every metered model | SERVER | — | `website/lib/billing/unit-pricing.ts` |
| 363 | Web credit top-up checkout | Stripe checkout URL for credit packs | SERVER | — | `website/app/api/billing/checkout/route.ts` |
| 364 | In-app top-up sheet (RxSubscriptionIOS / Stripe) | In-app packs sheet; dormant in this build (empty key) | HYBRID | — | `film-workflow/views/account/TopUpSheet.swift` |
| 365 | Subscription paywall gate | Window-level curtain; dormant, fails open | HYBRID | — | `film-workflow/views/subscription/SubscriptionGate.swift` |
| 366 | Account menu, sidebar footer and account sheet | Credits, plan, usage and charges in the app | HYBRID | — | `film-workflow/views/account/AccountSheet.swift` |
| 367 | Web dashboard, usage, ledger and invoices pages | Balance, devices, operations, ledger, invoices on the web | SERVER | — | `website/app/(account)/dashboard/page.tsx` |
| 368 | Public model price list (/models) | Web page of models with credit estimates | SERVER | — | `website/app/(account)/models/page.tsx` |
| 369 | Curated model catalog + admin curation | Admin-curated allowlist per capability | SERVER | `models_list` | `website/app/api/v1/models/route.ts`<br>`website/lib/ai/catalog.ts` |
| 370 | Marketplace purchase with credits | Hold and settle an item's price; agents cannot buy | SERVER | `show_marketplace_item` | `website/lib/marketplace/purchase.ts` |
| 371 | Local / non-credit AI paths | WhisperKit, Apple Intelligence, Apple translation, CLIs, user endpoint: no credits | LOCAL | — | `film-workflow/clients/captions/CaptionTranscriber.swift`<br>`film-workflow/clients/agent/AgentBackend.swift` |
| 372 | BYOK removal | Bring-your-own-key generation removed in v1.8.0 | SERVER | — | `_release-notes.md`<br>`film-workflow/clients/AIBackend.swift` |
| 373 | Post-purchase return to app | filmstudio:// refresh deep links; /credits/complete page missing | HYBRID | — | `film-workflow/auth/AuthSessionBridge.swift`<br>`website/app/(account)/credits/page.tsx` |

### Other (marketplace, platform, housekeeping) (38)

| # | Feature | What | Local/Server | MCP tool(s) | Proof |
|---|---|---|---|---|---|
| 51 | Marketplace browse and show | List and get items; show_marketplace_item draws the only chat card with a Buy button | SERVER | `marketplace_list`, `marketplace_get`, `show_marketplace_item` | `film-workflow/clients/mcp/handlers/MCPMarketplaceHandlers.swift`<br>`film-workflow/clients/marketplace/MarketplaceClient.swift` |
| 52 | marketplace_install / marketplace_add_to_film | Download an owned/free item to this Mac; put it into a film and return a sourceId. Never purchases | HYBRID | `marketplace_install`, `marketplace_add_to_film` | `film-workflow/clients/mcp/handlers/MCPMarketplaceHandlers.swift` |
| 53 | project_template_apply | Apply an entitled template as a NEW sequence; reports missing requirements and blockers; resumable | HYBRID | `project_template_apply` | `film-workflow/clients/mcp/handlers/MCPMarketplaceHandlers.swift`<br>`docs/marketplace.md` |
| 54 | Marketplace admin authoring | Ten admin-only tools, hidden from tools/list unless canAuthor | HYBRID | `marketplace_create`, `marketplace_update`, `marketplace_upload`, `marketplace_generate`, `marketplace_render_preview`, `marketplace_job_status`, `marketplace_retry`, `marketplace_publish`, `marketplace_workspace`, `project_template_from_film` | `film-workflow/clients/mcp/handlers/MCPMarketplaceHandlers.swift`<br>`film-workflow/clients/marketplace/MarketplaceAuthoringService.swift` |
| 102 | Create Marketplace Item from a clip (admin) | Clip menu seeds a marketplace draft (admin only) | — | — | `film-workflow/views/editor/TimelinePanel.swift` |
| 108 | ffmpeg Convert tab (never built) | Superseded design for bundled ffmpeg conversion and convert_* tools | — | — | `docs/video-conversion-plan.md` |
| 120 | Marketplace window (browse) | Split-view catalogue window with search, paged grid and hover previews | SERVER | `marketplace_list`, `marketplace_get`, `show_marketplace_item` | `film-workflow/views/marketplace/MarketplaceWindowView.swift`<br>`film-workflow/clients/marketplace/MarketplaceClient.swift` |
| 121 | Server-driven sidebar taxonomy | Kinds, symbols, categories and counts from the server | SERVER | — | `film-workflow/clients/marketplace/MarketplaceTaxonomy.swift` |
| 122 | Marketplace kinds (8) | footage, remotion, audio, sound_effect, font, transition, effect, project_template | SERVER | `marketplace_list` | `film-workflow/clients/marketplace/MarketplaceModels.swift` |
| 124 | Install / Uninstall / Reveal | Signed download into Application Support, per-kind checks; installs shared by every film | HYBRID | `marketplace_install` | `film-workflow/clients/marketplace/MarketplaceStore.swift`<br>`film-workflow/clients/marketplace/MarketplaceDownloader.swift` |
| 125 | Add to Film | Copies installed footage/music/SFX/Remotion into a film's library | LOCAL | `marketplace_add_to_film` | `film-workflow/clients/marketplace/MarketplaceInstaller.swift` |
| 126 | Library panel Marketplace tab | Per-film list of installed items with Add to Film | LOCAL | — | `film-workflow/views/editor/library/LibraryMarketplaceSection.swift` |
| 128 | Music/sound preview with lyric tracks | Detail sheets play previews with SRT/VTT lyric captions | HYBRID | — | `film-workflow/views/marketplace/MarketplaceMusicPreview.swift`<br>`film-workflow/clients/marketplace/MarketplaceLyrics.swift` |
| 129 | Remotion composition publishing (executable content) | Admin publishes a composition's source zip; validated on upload and install | HYBRID | `marketplace_upload`, `marketplace_render_preview`, `marketplace_workspace`, `marketplace_add_to_film` | `film-workflow/clients/marketplace/RemotionProjectArchive.swift` |
| 143 | Marketplace i18n | Accept-Language drives en/zh-Hans server text | SERVER | `marketplace_list` | `docs/marketplace.md`<br>`film-workflow/clients/marketplace/MarketplaceClient.swift` |
| 144 | What's New feature cards (Marketplace, Project templates) | What's New sheet introduces the marketplace and templates | LOCAL | — | `docs/marketplace-feature-artwork.md`<br>`_release-notes.md` |
| 174 | Marketplace Remotion items (publish/install source archives) | Remotion source zips published and unpacked per film | HYBRID | `marketplace_upload`, `marketplace_publish`, `marketplace_install`, `marketplace_add_to_film` | `film-workflow/clients/marketplace/RemotionProjectArchive.swift`<br>`film-workflow/clients/marketplace/MarketplaceInstaller.swift` |
| 175 | Project templates with Remotion dependencies | Unrendered Remotion sources become apply blockers | HYBRID | `project_template_apply` | `film-workflow/clients/marketplace/ProjectTemplateService.swift` |
| 176 | Standalone RxRemotionExample CLI + package API | `swift run RxRemotionExample --check` smoke test; multi-composition engine API | LOCAL | — | `Packages/RxRemotion/Sources/RxRemotionExample/main.swift` |
| 177 | Legacy Bun/Studio runtime vestiges | Leftover code and strings from the pre-native Studio runtime | LOCAL | — | `film-workflow/views/remotion/RemotionPreviewWebView.swift`<br>`film-workflow/clients/RemotionRuntime.swift` |
| 245 | Stale BYOK documentation and error strings | Bundled manuals still describe bring-your-own-key setup | SERVER | — | `film-workflow/Resources/user_manual_music.md`<br>`film-workflow/config/AppConfig.swift` |
| 246 | Marketplace authoring reuses music generation (admin) | Admin music assets generated via MusicGenerationService | SERVER | — | `film-workflow/clients/marketplace/MarketplaceAuthoringService.swift` |
| 271 | OpenAIClient / OpenAIModelsClient (not image/video gen) | Chat/tool client for OpenAI-compatible endpoints and model listing | HYBRID | — | `film-workflow/clients/OpenAIClient.swift`<br>`film-workflow/clients/OpenAIModelsClient.swift` |
| 288 | RxPet camera companion | Animated character showing countdown, status and messages | LOCAL | `recording_pet` | `Packages/RxPet/Sources/RxPet/PetView.swift` |
| 336 | App-wide storage in Application Support | whisper/, tmp/, Agent.store, Marketplace/, MarketplaceAuthoring/ | LOCAL | `marketplace_install`, `marketplace_workspace` | `film-workflow/utils/FileStorage.swift` |
| 338 | Settings persistence (Keychain vs UserDefaults) | Keys in Keychain, agent/MCP settings in UserDefaults | LOCAL | — | `film-workflow/config/AppConfig.swift`<br>`film-workflow/config/MCPSettings.swift` |
| 374 | Presigned upload API | User-scoped presigned S3 PUT for large audio | SERVER | — | `website/app/api/v1/uploads/route.ts` |
| 383 | Async AI job store + result delivery | Job rows with S3 results as signed URLs | SERVER | `video_job_status`, `video_resume` | `website/app/api/v1/jobs/[jobId]/route.ts`<br>`website/lib/storage/s3.ts` |
| 384 | Marketplace catalog API | Localized, paginated published catalog | SERVER | `marketplace_list`, `marketplace_get`, `marketplace_install`, `marketplace_add_to_film` | `website/app/api/v1/marketplace/items/route.ts` |
| 385 | Marketplace admin authoring API | Admin CRUD via a catch-all route | SERVER | `marketplace_create`, `marketplace_update`, `marketplace_upload`, `marketplace_publish` | `website/app/api/v1/admin/marketplace/[...path]/route.ts` |
| 389 | SF Symbols rendering API | Server renders SF Symbols as SVG for web pickers | SERVER | — | `website/app/api/sf-symbols/route.ts` |
| 390 | Sparkle auto-update + site download | Sparkle appcast at update.filmstudio.rxlab.app | HYBRID | — | `Info.plist`<br>`website/app/lib/release.ts` |
| 391 | What's New feature cards | Launch sheet of unread feature cards | LOCAL | — | `film-workflow/views/whatsnew/WhatsNewFeature.swift` |
| 392 | TipKit feature tips | Contextual tips shown once | LOCAL | — | `film-workflow/views/tips/FilmWorkflowTips.swift` |
| 393 | User Guide window (designed, not built) | Design doc only | — | — | `docs/whats-new-help-tipkit.md` |
| 394 | Localization incl. server responses | en and zh-Hans across app and server | HYBRID | — | `website/lib/i18n/locale.ts` |
| 396 | iOS support (legacy, not a current target) | Past iOS branches; project builds macOS only | LOCAL | — | `film-workflow.xcodeproj/project.pbxproj` |
| 397 | Release timeline | Feature arrival versions from release notes | — | — | `_release-notes.md` |

## MCP tool list (94 names, source-grounded)

Registered in `film-workflow/clients/mcp/MCPToolRegistry.swift` and the handler files under `film-workflow/clients/mcp/handlers/`. The phase-1 count of "~70" came from `docs/agent-tools.md`, which leaves out the 15 recording-handler tools (they are listed in `docs/screen-recording.md`), `models_list` and `marketplace_add_to_film`. Note that `sequence_link_clips` and `sequence_track_alias` are registered by the *recording* handler.

| Family | Count | Tools |
|---|---|---|
| caption | 10 | `caption_create`, `caption_export`, `caption_list_segments`, `caption_propose_edits`, `caption_search_segments`, `caption_set_speakers`, `caption_transcribe`, `caption_translate`, `caption_update_segment`, `caption_versions` |
| library/session | 3 | `film_list`, `models_list`, `show_sign_in_dialog` |
| footage | 12 | `folder_create`, `folder_delete`, `folder_list`, `folder_rename`, `footage_create`, `footage_delete`, `footage_duplicate`, `footage_get`, `footage_import`, `footage_list`, `footage_move`, `footage_update` |
| generate | 6 | `image_generate`, `music_generate`, `narration_generate`, `video_generate`, `video_job_status`, `video_resume` |
| marketplace | 16 | `marketplace_add_to_film`, `marketplace_create`, `marketplace_generate`, `marketplace_get`, `marketplace_install`, `marketplace_job_status`, `marketplace_list`, `marketplace_publish`, `marketplace_render_preview`, `marketplace_retry`, `marketplace_update`, `marketplace_upload`, `marketplace_workspace`, `project_template_apply`, `project_template_from_film`, `show_marketplace_item` |
| podcast | 6 | `podcast_add_content`, `podcast_create`, `podcast_list_speakers`, `podcast_remove_content`, `podcast_update_content`, `podcast_update_settings` |
| recording | 13 | `recording_actions_edit`, `recording_configure`, `recording_control`, `recording_focus`, `recording_get`, `recording_insert_take`, `recording_perform_action`, `recording_pet`, `recording_presentation`, `recording_screenshot`, `recording_shortcuts`, `recording_sources`, `recording_start` |
| remotion | 11 | `remotion_add_audio`, `remotion_add_image`, `remotion_edit_file`, `remotion_generate_image`, `remotion_list_files`, `remotion_read_file`, `remotion_remove_audio`, `remotion_remove_image`, `remotion_take_screenshot`, `remotion_take_screenshots`, `remotion_write_file` |
| sequence | 12 | `sequence_add_clip`, `sequence_add_track`, `sequence_create`, `sequence_get`, `sequence_link_clips`, `sequence_list`, `sequence_remove_clip`, `sequence_render`, `sequence_renders`, `sequence_reorder_tracks`, `sequence_set_timeline`, `sequence_track_alias` |
| wizard/web | 5 | `web_read`, `wizard_present_options`, `wizard_present_templates`, `wizard_report_progress`, `wizard_skip_templates` |
| **Total** | **94** | |

Visibility rules that change what an agent actually sees:
- The 10 admin marketplace tools are dropped from `tools/list` unless the account can author (`canAuthor`).
- The 4 `wizard_*` tools throw without an active Simple-mode session, so they are useless to external clients.
- The in-app agent's `AgentToolPolicy` withholds only `footage_delete`, `folder_delete`, and (in the default "review" policy) `caption_update_segment` and `caption_transcribe`. **External MCP clients are not filtered at all.**

## File formats (source-grounded)

| Area | Format |
|---|---|
| Film package | `.rxfilmstudio` directory (UTType `rxlab.film-workflow.project`): `Document.json` `{id, formatVersion: 2, createdAt, appVersion}`, optional `Workspace.json` `{splits, effectsBrowserVisible?, footageBrowserVisible?}`, `Library.store` (+`-wal`/`-shm`, SwiftData/SQLite, 18 `@Model` entities), `Media/`, `Remotion/<id>/`, `Renders/`, `Cache/` |
| Undocumented package folders | `TemplateApplications/<id>.json`; `Media/ScreenRecordings/<projectId>/<operationId>/` (component `.mov` files, `Session.json` checkpoint v1, `Recovered-Actions.json`, `cursor.png`, `reference-<actionID>.png`); `Media/ScreenRecordings/<projectId>/Actions/<uuid>.json` (append-only action revisions); `Media/Screenshots/<uuid>.png` |
| Timeline | `SequenceProject.timelineData` = JSON envelope `{formatVersion: 3, timeline}` with sorted keys (`TimelineCodec`). Tracks `video/audio/overlay/caption/zoom`; clips carry source, timing, picture/audio/text, `linkGroupID`, recording fields; effect and transition instances inside |
| Source ids | `<prefix>:<uuid>` with prefixes `music`, `narration`, `image`, `video`, `remotion`, `imported`, `caption`, `screenRecording`, `recordingZoom`. No `marketplace` prefix |
| Recording blobs | JSON `Data` columns: `RecordingSettings`, `[RecordingAction]` (21 kinds), `RecordingClipPresentation`, `TextStyle`, `[RecordingComponent]` with geometry events; take `actionsData` = replay execution log |
| Recording media | HEVC `.mov` with 2 s fragments per screen/camera/device component; 16-bit 48 kHz PCM `.mov` per mic, app tap, system or device audio |
| Renders | `Renders/Sequences/<id>/vNNN.<ext>` (mp4/mov, m4a for audio-only; H.264 or HEVC + AAC); `Renders/Remotion/<id>/vNNN-<hash8>.mp4` (opaque) or `.mov` (ProRes 4444 + PCM, alpha); hash prefix `native-v1-` includes the map-settings fingerprint |
| Captions out | WebVTT (sentence/word/word_karaoke, `<v>` voice tags), SRT, plain text, JSON; embedded 3GPP `tx3g` tracks per language; `.srt`/`.vtt` sidecars; per-language files `{item}_{lang}.{ext}` |
| Transcription wire | Upload audio re-encoded to 16 kHz 32 kbps AAC `.m4a` when worthwhile; ≤4 MB multipart, larger via presigned S3 PUT + `object_key`; provider replies decoded client-side (OpenAI `verbose_json`, Azure fast-transcription, Gemini envelope) |
| TTS | Azure SSML with the `mstts` namespace (MP3 `audio-24khz-48kbitrate-mono-mp3` or WAV `riff-24khz-16bit-mono-pcm`, batches stitched); Gemini 24 kHz 16-bit PCM wrapped as WAV; shortcode syntax `{{name:arg|wrapped}}`; `azure-voices.json` 24 h cache |
| Music | Plain-text prompt with `[m:ss - m:ss] [Section] (intensity: x)` lines and `[m:ss]` lyric blocks; Lyria output is MP3 whatever format is asked for |
| Image and video generation | Images png/jpeg/webp in `Media/Images`; Veo mp4 in `Media/Videos` with a JPEG poster (q 0.85 at ~0.5 s); input frames sent as base64 JSON; snake_case backend wire format |
| Remotion project | `src/index.ts`, `src/Root.tsx` (composition `Main`), `src/Composition.tsx` (`COMPOSITION_WIDTH/HEIGHT/FPS/DURATION_IN_FRAMES`), `public/{upload,reference,generated,audio}/`; agent stills in `.agent-stills/<runId>/frame-N.png` (480×270, deleted after use); disposable preview cache `~/Library/Caches/com.rxlab.film-workflow/RemotionPreview/<key>/source.mov` |
| Bundled Remotion runtime | `Resources/Web`: `esbuild.wasm` (12 MB), `compiler.js`, `host.js`, `capture.js`, `catalog.json` (20 import keys), `manifest.json` (pinned deps, `remotion` 4.0.459), `vendor-*.js`, `THIRD-PARTY-NOTICES.txt` (0 hits for "remotion") |
| Effects | `CIFilterModifierDescriptor` JSON (format 1): id, kind effect/transition, built-in `filter`, `progressKey`, `inputs`, parameters with number/choice/colour controls and scale, `constants`, `clampEdges`; drag type `com.rxlab.video-modifier` |
| Templates and wizard | `ProjectTemplateDefinition` v1 JSON (prompt, videoStyle, editingGuidance, size, fps, `shots[]`, `footageRequirements[]`, `marketplaceItems[]`; local paths incl. `/private/` rejected); json-render flat spec `{root, elements}` plus `initial_state` |
| Marketplace | `~/Library/Application Support/com.rxlab.film-workflow/Marketplace/<kind>/<itemId>/` (`manifest.json`, `content.<ext>`, `preview.<ext>`); Remotion archive = zip of `src/`, `public/`, root configs + `rxremotion.json` (≤400 MB, ≤5,000 files, no symlinks); lyric tracks JSON (≤12 tracks, ≤2,000 cues, ≤512,000 bytes); preview = 720p H.264 ≤15 s |
| App-wide state | `Agent.store` (SwiftData, threads and messages) and `whisper/`, `tmp/`, `MarketplaceAuthoring/<sha256(userId)>/<itemId>/Preview.rxfilmstudio` under Application Support; UserDefaults `remotion.renderConcurrency`; Keychain for tokens and OSM config |
| MCP wire | HTTP/1.1 `POST /mcp`, JSON-RPC 2.0, protocol 2025-03-26, no SSE, `Connection: close`; public `GET /` and `/health`; image results as base64 PNG content; `MCPServerSpec.http` rendered into Claude `--mcp-config` and Codex `-c mcp_servers` overrides |
| Server | OpenAI chat-completions shape plus `rxlab_usage`; job rows with `progress_percent` and result URL; Sparkle `appcast.xml` at `update.filmstudio.rxlab.app` |



---

