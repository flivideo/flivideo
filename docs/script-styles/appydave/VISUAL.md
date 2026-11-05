---
created: 2026-11-05
timestamp: 2026-11-05T10:30+07:00
---
# appydave — visual and editing style

Scope: 10 of the newest 25 @appydave long videos. Sources: 1 from FliVideo (IL-voVs9IBE render), 6 from the M4's T7 old copies **matched by title** (Claudemas Day N → `c0N`/`b9N` project, using `final/`, `edit-final/`, or `edit-1st/` for Rb6U3Z4DvnM which has no final), and 3 from YouTube because the published video is not on the M4 (M978wEYFz1E, kn_54J1fxec, AqLhqOCv9X0).

## Measured

How: `ffmpeg select='gt(scene,T)',showinfo` over the whole video gives cut timestamps; cuts/min = cuts ÷ duration × 60; shot length = gap between consecutive cuts (first and last shot included). **Primary threshold T = 0.3** (the brief's). **T = 0.15** is recorded beside it. 'Change/min' is a second, independent measure: the mean absolute pixel difference between consecutive frames sampled every 2 s (64×36 grey), counted when above 8/255 — it catches slide-to-slide changes that a dissolve or a dark-on-dark card hides from the scene detector, but it cannot see anything faster than 2 s, so it is a floor.

**appydave (n = 10) — median cuts/min @0.3: 1.5; @0.15: 4.4; median shot length @0.3: 12.5 s; mean shot length @0.3 (mean of per-video means): 51.0 s; median change/min (2 s frames): 6.7.**

| video | length | source | cuts/min @0.3 | median shot @0.3 | mean shot @0.3 | cuts/min @0.15 | change/min |
|---|---|---|---|---|---|---|---|
| IL-voVs9IBE | 19.1 min | FliVideo (M4) | 1.7 | 19.0 s | 34.8 s | 4.2 | 6.5 |
| M978wEYFz1E | 9.9 min | YouTube | 2.3 | 10.0 s | 24.7 s | 4.7 | 7.5 |
| kn_54J1fxec | 5.5 min | YouTube | 3.4 | 9.7 s | 16.6 s | 8.7 | 9.9 |
| AqLhqOCv9X0 | 15.1 min | YouTube | 0.5 | 90.1 s | 113.3 s | 2.0 | 8.8 |
| Rb6U3Z4DvnM | 20.7 min | T7 old copy (M4) | 1.5 | 13.6 s | 37.7 s | 5.6 | 7.4 |
| 2jMdt3U4AkA | 15.0 min | T7 old copy (M4) | 2.0 | 11.4 s | 29.0 s | 4.9 | 6.1 |
| XA3JZLOgMow | 12.2 min | T7 old copy (M4) | 1.4 | 8.1 s | 40.8 s | 10.3 | 6.9 |
| 7jCkq3T8nJo | 22.5 min | T7 old copy (M4) | 0.7 | 21.0 s | 79.3 s | 2.3 | 4.6 |
| aEJCzHKVHTg | 20.4 min | T7 old copy (M4) | 0.8 | 8.1 s | 71.9 s | 2.3 | 4.3 |
| -wL35QS_35o | 12.4 min | T7 old copy (M4) | 0.9 | 14.4 s | 62.1 s | 2.3 | 3.8 |

## Observed from frames

Frames reviewed for 5 of 10 (IL-voVs9IBE, aEJCzHKVHTg, Rb6U3Z4DvnM, kn_54J1fxec, M978wEYFz1E), plus numbers for all.

- **Presenter**: always David. Two forms: **full-frame** (talking head at the hook, mid-video resets and the outro, ~15–25 % of frames) and a **picture-in-picture** in the lower-right/left corner over every screen section — so presenter is on screen nearly the whole video.
- **Shot types**: screen recordings (terminal, editor, app UIs, browser) fill the rest. **Claudemas (Dec 2025)**: screen recordings are letterboxed on black with the PiP; long, mostly static, text-heavy. **Oct 2026 renders** (IL-voVs9IBE, kn_54J1fxec, M978): cream-background designed cards (diagrams, comparison tables, a stock-style image for a metaphor) and app screens under the PiP; FliVideo overlay-built.
- **On-screen text**: little added text in Claudemas; in the 2026 renders, diagram and headline cards and highlighted text on the screen captured. No burned-in captions seen in the frames.
- **B-roll share (estimate)**: ~60–75 % screen/graphic content with the presenter PiP; ~0 % cinematic or stock footage (one stock-style image in IL-voV). Method: tiles in the 16-frame sheets.
- **Transitions**: hard cuts; scene detection median 1.5/min @0.3 and long shots (median 12.5 s, and means up to ~51 s). Screen scrolling and typing do not trigger the detector.

## Interpreted

A **screen-share walk-through with the presenter always in view**: long takes, cuts only when the topic or screen changes, designed diagram cards used sparingly to explain structure. Two eras in the same channel: the Claudemas series (screen + PiP, minimal graphics) and the Oct 2026 overlay-rich FliVideo renders. Pace is slow; this style is the opposite end from Maitis.

## Sources

- `IL-voVs9IBE` — Asked for a Dog House, Got a Power Plant: OpenRig Agent Teams (FliVideo (M4))
- `M978wEYFz1E` — I Built My Own Recording Apps Around Ecamm Live (YouTube; YouTube fallback: no matching project/final on M4 T7 (d06/d07/d08 are current FliVideo projects holding only pre-overlay -cut.mp4 or audio, not the published video))
- `kn_54J1fxec` — Which Headshot Goes on My Thumbnail? Now AI Can Choose (YouTube; YouTube fallback: no matching project/final on M4 T7 (d06/d07/d08 are current FliVideo projects holding only pre-overlay -cut.mp4 or audio, not the published video))
- `AqLhqOCv9X0` — Claude Code Agents Working Together | Swarm Intelligence (YouTube; YouTube fallback: no matching project/final on M4 T7 (d06/d07/d08 are current FliVideo projects holding only pre-overlay -cut.mp4 or audio, not the published video))
- `Rb6U3Z4DvnM` — This Is Where Vibe Coding Turns Into a Finished Film (Claudemas #11) (T7 old copy (M4))
- `2jMdt3U4AkA` — From Transcript to Prompt Pack: Designing an AI Prompt Pipeline | Day 9 Claudemas (T7 old copy (M4))
- `XA3JZLOgMow` — I Added Music to My AI Story Pipeline (Suno + Claude Code) | Day 7 Claudemas (T7 old copy (M4))
- `7jCkq3T8nJo` — Build a Multi-Model Image Generator with FAL.AI + KIE.AI (Claudemas Day 4) (T7 old copy (M4))
- `aEJCzHKVHTg` — 12 Days of Claudemas: Building with Agent SDK "Day 2" (T7 old copy (M4))
- `-wL35QS_35o` — I Built a Text-to-Speech Generator in 15 Minutes (Claudemas Day 5) (T7 old copy (M4))

## Not established

- Only 5 of 10 viewed; M978 and kn_54 are YouTube re-encodes while Claudemas/IL-voV are editor files.
- Rb6U3Z4DvnM was measured on the `edit-1st` file, not a final export; it may differ from the published video.
- Graphic overlays that arrive after FliCut (the d06/d07 `-cut.mp4` files) were not sampled.
- Frames are 640 px, one every 2 s; anything faster than 2 s (flash cuts, sub-second graphic pops) is invisible to the frame review and only partly visible to the scene detector.
- Share estimates are by eye from 16-frame contact sheets (16 evenly spaced frames per video) on a subset of videos, not counted on every frame.
- YouTube-sourced files are re-encoded at ≤720p; FliVideo/T7 files are the editor's own export. Scene scores can differ slightly between the two.

## Who reads this

Nothing reads it yet — there is no seam. Checked: `flivideo:broll-pilot` (skill) and its spec `~/dev/ad/flivideo/flistudio/docs/planning/broll-pilot/spec.md`: B-roll Pilot is a **catalogue** of described assets (`broll.register` / `broll.describe.*` / `broll.list`); it "never places anything on a timeline and never picks" and has no notion of a script style. Placement is "Timeline Pilot, later" (not built). `flivideo:fliedit` lays overlays on a FliCut export through typed capabilities (`edit.*`), driven by an agent or David; it takes no style input, and a grep of the flistudio, flicut and fliedit docs for "script style" found nothing. The natural future reader is whatever picks B-roll for a script (Timeline Pilot or an auto-edit step), reading this file by style name next to `STRUCTURE.md`. Not built; not proposed in code.
