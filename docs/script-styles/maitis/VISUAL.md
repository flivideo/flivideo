---
created: 2026-11-05
timestamp: 2026-11-05T10:30+07:00
---
# maitis — visual and editing style

Scope: 10 of the 15 sampled @maitis-ai long videos (spread across the list). All from YouTube (not own channel).

## Measured

How: `ffmpeg select='gt(scene,T)',showinfo` over the whole video gives cut timestamps; cuts/min = cuts ÷ duration × 60; shot length = gap between consecutive cuts (first and last shot included). **Primary threshold T = 0.3** (the brief's). **T = 0.15** is recorded beside it. 'Change/min' is a second, independent measure: the mean absolute pixel difference between consecutive frames sampled every 2 s (64×36 grey), counted when above 8/255 — it catches slide-to-slide changes that a dissolve or a dark-on-dark card hides from the scene detector, but it cannot see anything faster than 2 s, so it is a floor.

**maitis (n = 10) — median cuts/min @0.3: 9.3; @0.15: 13.2; median shot length @0.3: 4.5 s; mean shot length @0.3 (mean of per-video means): 6.5 s; median change/min (2 s frames): 18.4.**

| video | length | source | cuts/min @0.3 | median shot @0.3 | mean shot @0.3 | cuts/min @0.15 | change/min |
|---|---|---|---|---|---|---|---|
| KscFyux4dVk | 22.2 min | YouTube | 4.5 | 8.6 s | 13.2 s | 7.2 | 16.0 |
| nndv3V5Q7HY | 11.1 min | YouTube | 8.1 | 5.0 s | 7.3 s | 10.5 | 16.5 |
| 4b-D8Nr0jQc | 9.5 min | YouTube | 7.5 | 4.6 s | 7.9 s | 10.5 | 16.1 |
| I1ISxjjsKNw | 15.8 min | YouTube | 8.5 | 4.5 s | 7.0 s | 12.2 | 16.0 |
| qQ9VBlXlSaI | 6.7 min | YouTube | 6.1 | 4.5 s | 9.5 s | 10.3 | 18.7 |
| iaxh4Vt6_SI | 21.0 min | YouTube | 10.1 | 4.4 s | 5.9 s | 14.1 | 18.0 |
| WqYoGfbYb7Q | 10.5 min | YouTube | 16.4 | 2.1 s | 3.6 s | 28.1 | 21.3 |
| HTrKAn2qJUE | 10.7 min | YouTube | 17.0 | 2.5 s | 3.5 s | 28.0 | 22.7 |
| mVh3YktAhDA | 5.9 min | YouTube | 16.8 | 2.3 s | 3.5 s | 24.0 | 23.5 |
| 0iFEPUeQyz4 | 11.0 min | YouTube | 18.6 | 2.0 s | 3.2 s | 29.2 | 22.5 |

## Observed from frames

Frames reviewed for 2 of 10 (KscFyux4dVk, 0iFEPUeQyz4), plus the numbers for all.

- **Presenter**: a real on-camera host in a styled room (two different hosts/rooms across the two videos viewed), full-frame, ~30–50 % of frames, medium close-up, speaking to camera with hand gestures; large animated word-highlight captions in some (e.g. 'a DETAILED prompt').
- **Shot types**: a rapid mix of **screen captures** (UI, browser, Slack), **dark UI/diagram motion-graphics cards** (flow diagrams, headline words like 'No expensive AI'), **news clips and source cards** (a CNN-style breaking-news clip, tweets, articles), **cinematic stock or generated footage** (sunset, climber, airport) and brand logos (Grok, iPhone keynote).
- **On-screen text**: heavy — kinetic captions, headline cards, UI labels and logos.
- **B-roll share (estimate)**: ~50–70 %, of which a real share is *footage-type* B-roll (stock, news, generated video), unlike the AITLDR and AppyDave styles. Method: tiles in the 16-frame sheets.
- **Transitions**: hard cuts; the highest cut rate of the five (median 9.3/min @0.3, shot length median 4.5 s), ranging 4.5–18.6/min across the ten.

## Interpreted

A **fast YouTube-tech-explainer style**: host to camera, cut every ~4 s to supporting visuals (screen, news, stock, graphic) so the picture is never static for more than a few seconds. This is the one style where B-roll in the sense of cutaway footage matters.

## Sources

- `KscFyux4dVk` — Forget Claude Code: DeepSeek + REA Clones Anything 100% FREE (No Paid API) (YouTube)
- `nndv3V5Q7HY` — You Can Clone Any App for FREE (REA + 9Router) Complete End-to-End Tutorial (YouTube)
- `4b-D8Nr0jQc` — You Can Use Claude Opus 5.5 & Fable 5.1 for FREE (Anyone Can Do This) (YouTube)
- `I1ISxjjsKNw` — Claude Opus 5.5 Just Killed Expensive Video Editors? (Under $1 Per Video) (YouTube)
- `qQ9VBlXlSaI` — RIP ChatGPT and Claude? Google Just Dropped Carbon (YouTube)
- `iaxh4Vt6_SI` — I Tested Every Free AI Tool So You Don't Have To (YouTube)
- `WqYoGfbYb7Q` — 4 Free Chrome Extensions That Turn Chrome Into an AI Operating System (YouTube)
- `HTrKAn2qJUE` — The New Claude Can Build Things AI Couldn't Do Before (YouTube)
- `mVh3YktAhDA` — I Tested Grok 4.7: The Reality Check Nobody Is Talking About (YouTube)
- `0iFEPUeQyz4` — Is AI Getting Too Dangerous? Claude, Meta, and the Week's Biggest Breakthroughs (YouTube)

## Not established

- Only 2 of 10 viewed on contact sheets.
- Which cuts are the host vs B-roll was not counted per cut.
- The two hosts seen are not confirmed to be the same channel owner across all 10.
- Frames are 640 px, one every 2 s; anything faster than 2 s (flash cuts, sub-second graphic pops) is invisible to the frame review and only partly visible to the scene detector.
- Share estimates are by eye from 16-frame contact sheets (16 evenly spaced frames per video) on a subset of videos, not counted on every frame.
- YouTube-sourced files are re-encoded at ≤720p; FliVideo/T7 files are the editor's own export. Scene scores can differ slightly between the two.

## Who reads this

Nothing reads it yet — there is no seam. Checked: `flivideo:broll-pilot` (skill) and its spec `~/dev/ad/flivideo/flistudio/docs/planning/broll-pilot/spec.md`: B-roll Pilot is a **catalogue** of described assets (`broll.register` / `broll.describe.*` / `broll.list`); it "never places anything on a timeline and never picks" and has no notion of a script style. Placement is "Timeline Pilot, later" (not built). `flivideo:fliedit` lays overlays on a FliCut export through typed capabilities (`edit.*`), driven by an agent or David; it takes no style input, and a grep of the flistudio, flicut and fliedit docs for "script style" found nothing. The natural future reader is whatever picks B-roll for a script (Timeline Pilot or an auto-edit step), reading this file by style name next to `STRUCTURE.md`. Not built; not proposed in code.
