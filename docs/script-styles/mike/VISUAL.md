---
created: 2026-11-05
timestamp: 2026-11-05T10:30+07:00
---
# mike — visual and editing style

Scope: all 3 given videos (qccsfUnrQ9w, CYRJDTcTKhQ, AL-PQuB2wy0) from YouTube; mirror of the OpenRig talks.

## Measured

How: `ffmpeg select='gt(scene,T)',showinfo` over the whole video gives cut timestamps; cuts/min = cuts ÷ duration × 60; shot length = gap between consecutive cuts (first and last shot included). **Primary threshold T = 0.3** (the brief's). **T = 0.15** is recorded beside it. 'Change/min' is a second, independent measure: the mean absolute pixel difference between consecutive frames sampled every 2 s (64×36 grey), counted when above 8/255 — it catches slide-to-slide changes that a dissolve or a dark-on-dark card hides from the scene detector, but it cannot see anything faster than 2 s, so it is a floor.

**mike (n = 3) — median cuts/min @0.3: 0.9; @0.15: 3.2; median shot length @0.3: 26.8 s; mean shot length @0.3 (mean of per-video means): 73.2 s; median change/min (2 s frames): 5.7.**

| video | length | source | cuts/min @0.3 | median shot @0.3 | mean shot @0.3 | cuts/min @0.15 | change/min |
|---|---|---|---|---|---|---|---|
| qccsfUnrQ9w | 19.9 min | YouTube | 0.9 | 26.8 s | 63.0 s | 1.3 | 6.7 |
| CYRJDTcTKhQ | 30.3 min | YouTube | 0.5 | 22.8 s | 106.9 s | 3.6 | 4.1 |
| AL-PQuB2wy0 | 24.8 min | YouTube | 1.2 | 31.9 s | 49.7 s | 3.2 | 5.7 |

## Observed from frames

Frames reviewed for 2 of 3 (qccsfUnrQ9w, AL-PQuB2wy0).

- **Presenter**: effectively absent — a small circular face-cam in a corner of 1–2 of the 16 tiles, otherwise voice-over.
- **Shot types**: dark-theme **motion-graphic explainer cards** (one heading per beat — 'A rig is a team.', 'Pods.', 'A task in the queue.'), **AI-generated or rendered illustrations** (a warehouse, toy-robot office, a dog on a moon base), **terminal and TUI screen captures** (OpenRig UI) and one article page with highlighted text.
- **On-screen text**: one large sentence heading per card and diagram labels; no captions seen.
- **B-roll share (estimate)**: ~90 %+ is non-presenter (cards, illustrations, screens); the 'footage' proper is generated illustration, not camera footage.
- **Transitions**: very few hard cuts (median 0.9/min @0.3, shot ~27 s); cards animate in place.

## Interpreted

A **narrated, graphics-led explainer**: voice carries it, a designed card per idea, a fixed dark palette, no presenter. Closest relative in the five is aitldr-new (card-per-idea) but with no avatar and much longer holds.

## Sources

- `qccsfUnrQ9w` — (title not recorded) (YouTube)
- `CYRJDTcTKhQ` — (title not recorded) (YouTube)
- `AL-PQuB2wy0` — (title not recorded) (YouTube)

## Not established

- n = 3, so no spread to speak of; per-video values range 0.5–1.2 cuts/min.
- One of the three (CYRJDTcTKhQ) was not viewed; its 0.15 median shot (0.1 s) reflects detector noise on animation, not real cuts.
- Frames are 640 px, one every 2 s; anything faster than 2 s (flash cuts, sub-second graphic pops) is invisible to the frame review and only partly visible to the scene detector.
- Share estimates are by eye from 16-frame contact sheets (16 evenly spaced frames per video) on a subset of videos, not counted on every frame.
- YouTube-sourced files are re-encoded at ≤720p; FliVideo/T7 files are the editor's own export. Scene scores can differ slightly between the two.

## Who reads this

Nothing reads it yet — there is no seam. Checked: `flivideo:broll-pilot` (skill) and its spec `~/dev/ad/flivideo/flistudio/docs/planning/broll-pilot/spec.md`: B-roll Pilot is a **catalogue** of described assets (`broll.register` / `broll.describe.*` / `broll.list`); it "never places anything on a timeline and never picks" and has no notion of a script style. Placement is "Timeline Pilot, later" (not built). `flivideo:fliedit` lays overlays on a FliCut export through typed capabilities (`edit.*`), driven by an agent or David; it takes no style input, and a grep of the flistudio, flicut and fliedit docs for "script style" found nothing. The natural future reader is whatever picks B-roll for a script (Timeline Pilot or an auto-edit step), reading this file by style name next to `STRUCTURE.md`. Not built; not proposed in code.
