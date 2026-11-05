---
created: 2026-11-05
timestamp: 2026-11-05T10:30+07:00
---
# aitldr-new — visual and editing style

Scope: 10 of the 27 long (2–4.5 min) videos made since 2026-09-15, all from FliVideo `final.mp4` on the M4. Shorts (18) were not sampled in this lane.

## Measured

How: `ffmpeg select='gt(scene,T)',showinfo` over the whole video gives cut timestamps; cuts/min = cuts ÷ duration × 60; shot length = gap between consecutive cuts (first and last shot included). **Primary threshold T = 0.3** (the brief's). **T = 0.15** is recorded beside it. 'Change/min' is a second, independent measure: the mean absolute pixel difference between consecutive frames sampled every 2 s (64×36 grey), counted when above 8/255 — it catches slide-to-slide changes that a dissolve or a dark-on-dark card hides from the scene detector, but it cannot see anything faster than 2 s, so it is a floor.

**aitldr-new (n = 10) — median cuts/min @0.3: 1.3; @0.15: 4.4; median shot length @0.3: 16.7 s; mean shot length @0.3 (mean of per-video means): 37.3 s; median change/min (2 s frames): 8.1.**

| video | length | source | cuts/min @0.3 | median shot @0.3 | mean shot @0.3 | cuts/min @0.15 | change/min |
|---|---|---|---|---|---|---|---|
| P4c-XkAeJxI | 3.4 min | FliVideo (M4) | 0.6 | 8.2 s | 67.2 s | 2.4 | 6.8 |
| XJXg98uMAVY | 2.9 min | FliVideo (M4) | 4.9 | 8.7 s | 11.5 s | 14.9 | 12.5 |
| VtFZNkGYnaU | 2.8 min | FliVideo (M4) | 0.7 | 22.4 s | 56.3 s | 1.8 | 6.7 |
| yh-ko-CwXyg | 2.6 min | FliVideo (M4) | 3.0 | 12.2 s | 17.6 s | 6.8 | 10.6 |
| 8KhyDQLB0Po | 2.7 min | FliVideo (M4) | 1.1 | 21.4 s | 39.9 s | 4.5 | 7.5 |
| c_9TqD0GlXk | 2.2 min | FliVideo (M4) | 0.5 | 64.5 s | 64.5 s | 6.0 | 13.5 |
| TdBL1A7kMd4 | 2.7 min | FliVideo (M4) | 1.5 | 17.3 s | 32.0 s | 4.1 | 7.5 |
| Nrd5PnLkMk4 | 3.3 min | FliVideo (M4) | 2.1 | 16.2 s | 25.0 s | 4.2 | 8.7 |
| a2EGJnOCpoA | 3.6 min | FliVideo (M4) | 1.1 | 34.6 s | 43.2 s | 2.2 | 4.4 |
| D3srragTwPQ | 2.0 min | FliVideo (M4) | 3.4 | 14.7 s | 15.3 s | 4.9 | 10.8 |

## Observed from frames

Frames reviewed on contact sheets for 3 of the 10 (a2EGJnOCpoA, c_9TqD0GlXk, XJXg98uMAVY).

- **Presenter**: one fixed AI avatar in two sets — a couch/living-room set and a white-shelf desk set (the shelf set appears once in the middle of c_9Tq). Full-frame at the hook, sometimes at the mid-roll, and always at the sign-off; about 15–25 % of frames in the sheets viewed. Always the same framing: wide medium shot, centred, seated, hands visible. Occasionally a small lower-third label (`/broll-prompts`, `Rights Check`).
- **Shot types**: the other ~75–85 % is full-screen **designed motion-graphic cards** on a navy or cream/halftone background: one big headline (e.g. 'How the skill works', 'Evidence. Not guesses.'), bullet reveals, stat tiles and bar charts, a 'case file / exhibit' illustrated theme in XJXg, and **terminal or app screen captures set inside a card frame** (torn-paper border in c_9Tq; floating dark window in a2EG). No real footage and no stock.
- **On-screen text**: heavy and constant — every graphic card has a headline; keyword stickers and callouts (`BEFORE`/`AFTER`, `No filming.`, `2 things.`) pin to the presenter or the screen capture; captions at the foot only on some cards (XJXg exhibit cards).
- **B-roll share (estimate)**: if 'B-roll' means anything other than the presenter, ~75–85 %; if it means filmed cutaway footage, ~0 %. Method: tiles in the 16-frame sheets classified presenter vs graphic/screen.
- **Transitions**: scene detection finds few hard cuts (median 1.3/min @0.3) but the 2 s-frame change measure finds a visible change roughly every 7 s — most changes are fades, wipes or in-card animation, not hard cuts. Hard cuts happen mainly presenter ↔ graphic.
- **Avatar use**: the avatar *is* the presenter; the format uses it as bookends and lets graphics carry the middle.

## Interpreted

A **template-driven explainer**: bookend the video with the avatar, carry the argument with one-idea-per-card motion graphics and a framed screen capture of the skill running, with a consistent brand (navy/cream, yellow accent, sticker callouts). Pace is set by card changes (~one per 7 s), not by cuts. For B-roll Pilot this style wants *graphics and screen captures*, not footage.

## Sources

- `P4c-XkAeJxI` — How to Repurpose YouTube Videos With Claude Code (FliVideo (M4))
- `XJXg98uMAVY` — Avoid YouTube Copyright Claims With This Claude Skill! (FliVideo (M4))
- `VtFZNkGYnaU` — Turn Long Videos Into YouTube Shorts Automatically With Claude! (FliVideo (M4))
- `yh-ko-CwXyg` — I Let Claude Fix My YouTube Captions — Here's What Happened (FliVideo (M4))
- `8KhyDQLB0Po` — This Claude Skill Fixed My Animation Timing (FliVideo (M4))
- `c_9TqD0GlXk` — I Had No B-Roll. This Claude Skill Wrote the Prompts (FliVideo (M4))
- `TdBL1A7kMd4` — How to sound natural on camera | Claude Cue Cards (FliVideo (M4))
- `Nrd5PnLkMk4` — This Claude Skill Found What Was Wrong With My YouTube Hooks (FliVideo (M4))
- `a2EGJnOCpoA` — Want to Know Which Videos Are Killing Your Channel? Watch This Now! (FliVideo (M4))
- `D3srragTwPQ` — I Stopped Guessing YouTube Titles—This Claude Skill Found My Best One (FliVideo (M4))

## Not established

- Shorts (18 of the 45) not sampled; their visual rhythm is probably faster, unverified.
- Whether a given card change is a hard cut or a transition was not classified per video.
- Frames are 640 px, one every 2 s; anything faster than 2 s (flash cuts, sub-second graphic pops) is invisible to the frame review and only partly visible to the scene detector.
- Share estimates are by eye from 16-frame contact sheets (16 evenly spaced frames per video) on a subset of videos, not counted on every frame.
- YouTube-sourced files are re-encoded at ≤720p; FliVideo/T7 files are the editor's own export. Scene scores can differ slightly between the two.

## Who reads this

Nothing reads it yet — there is no seam. Checked: `flivideo:broll-pilot` (skill) and its spec `~/dev/ad/flivideo/flistudio/docs/planning/broll-pilot/spec.md`: B-roll Pilot is a **catalogue** of described assets (`broll.register` / `broll.describe.*` / `broll.list`); it "never places anything on a timeline and never picks" and has no notion of a script style. Placement is "Timeline Pilot, later" (not built). `flivideo:fliedit` lays overlays on a FliCut export through typed capabilities (`edit.*`), driven by an agent or David; it takes no style input, and a grep of the flistudio, flicut and fliedit docs for "script style" found nothing. The natural future reader is whatever picks B-roll for a script (Timeline Pilot or an auto-edit step), reading this file by style name next to `STRUCTURE.md`. Not built; not proposed in code.
