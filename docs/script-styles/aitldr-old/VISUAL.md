---
created: 2026-11-05
timestamp: 2026-11-05T10:30+07:00
---
# aitldr-old — visual and editing style

Scope: 10 of the 25 older AITLDR long videos (published before 2026-09-15), spread 2024-09 to 2026-08. **All 10 from YouTube** (no old copy on the M4 T7 for any of them; own-channel exception, listed in Sources).

## Measured

How: `ffmpeg select='gt(scene,T)',showinfo` over the whole video gives cut timestamps; cuts/min = cuts ÷ duration × 60; shot length = gap between consecutive cuts (first and last shot included). **Primary threshold T = 0.3** (the brief's). **T = 0.15** is recorded beside it. 'Change/min' is a second, independent measure: the mean absolute pixel difference between consecutive frames sampled every 2 s (64×36 grey), counted when above 8/255 — it catches slide-to-slide changes that a dissolve or a dark-on-dark card hides from the scene detector, but it cannot see anything faster than 2 s, so it is a floor.

**aitldr-old (n = 10) — median cuts/min @0.3: 5.2; @0.15: 11.3; median shot length @0.3: 5.2 s; mean shot length @0.3 (mean of per-video means): 15.6 s; median change/min (2 s frames): 13.8.**

| video | length | source | cuts/min @0.3 | median shot @0.3 | mean shot @0.3 | cuts/min @0.15 | change/min |
|---|---|---|---|---|---|---|---|
| f-fYGjCmbp4 | 5.2 min | YouTube | 13.3 | 2.4 s | 4.4 s | 31.8 | 24.1 |
| AWaAj15enVE | 9.9 min | YouTube | 5.7 | 5.0 s | 10.4 s | 10.6 | 13.6 |
| x3SgWqdW-wQ | 6.2 min | YouTube | 11.3 | 1.8 s | 5.2 s | 30.0 | 18.8 |
| iXu4QeKkSmA | 6.0 min | YouTube | 4.3 | 7.6 s | 13.3 s | 10.7 | 13.5 |
| z1jM3mF5hCk | 13.5 min | YouTube | 4.8 | 5.9 s | 12.4 s | 19.8 | 24.7 |
| kMXkKzlKNnQ | 7.3 min | YouTube | 5.9 | 5.3 s | 9.9 s | 11.8 | 14.0 |
| ciRCM-SRZII | 5.1 min | YouTube | 1.9 | 6.9 s | 28.0 s | 2.9 | 5.8 |
| 7O_-z6xaFi4 | 10.1 min | YouTube | 1.3 | 8.4 s | 43.5 s | 1.4 | 5.5 |
| lWKzuIjwQvQ | 5.5 min | YouTube | 2.4 | 4.6 s | 23.6 s | 3.3 | 6.4 |
| BA435LYtYho | 5.4 min | YouTube | 12.1 | 1.7 s | 4.9 s | 25.0 | 14.6 |

## Observed from frames

Frames reviewed for 3 of 10 (AWaAj15enVE, BA435LYtYho, 7O_-z6xaFi4), plus the cut-rate numbers for all.

- **Two sub-looks, and the numbers split on them.** (a) **Image/screen-recording montage** (f-fYG, x3Sg, AWaAj, z1jM, BA435, kMXk): fast, 4–13 cuts/min, AI-generated images and video clips of the thing being made, screen recordings of the tool and ChatGPT prompt screens, with a prompt card with yellow-bordered text; presenter appears in a few tiles. (b) **Dark-navy slide deck** (7O_-z, ciRCM, lWKz, 2026 titles): almost no cuts (1–2/min), full-screen slides with a headline, small avatar circle on the hook, terminal screenshots, price tables; this is the look the newer series inherits.
- **Presenter**: the same avatar on the couch set appears at the hook and sign-off in the 2026 videos (BA435); the earlier ones show little or no presenter in the sheets viewed.
- **On-screen text**: lower-third captions (large, yellow/white, bottom third), numbered section cards ('3 STORYBOARD', '4 ANIMATE'), prompt cards labelled 'PROMPT'.
- **B-roll share (estimate)**: in sub-look (a) well over 50 % is AI-generated imagery/clips or screen recording; in sub-look (b) ~100 % graphics. Method: tiles in the 16-frame sheets.
- **Transitions**: hard cuts in (a); fades between slides in (b).

## Interpreted

Not one style but a **drift from an image-montage tutorial to a slide-led explainer** — which is why the cut rate varies 1.3–13.3/min with the median (5.2) describing neither cluster. Treat the cluster, not the median, as the unit if this style is read by tooling. By cut rate, the six 2024–2025 videos in the sample all sit at 4.3–13.3 cuts/min (montage-like); of the four 2026 videos only BA435 (2026-08) does, the other three are at 1.3–2.4 (slide-like). Only AWaAj, BA435 and 7O_ were actually looked at.

## Sources

- `f-fYGjCmbp4` — In KlueLess: The Clue is to do Less (YouTube; YouTube fallback: not on T7 aitldr-cold or youtube-PUBLISHED/aitldr (those hold only the 2024 a1-a100 series and the b01-b20 series); no title match)
- `AWaAj15enVE` — AI Does It ALL: Script, Visuals & Editing! (Next-Level AI Movie Trailers) (YouTube; YouTube fallback: not on T7 aitldr-cold or youtube-PUBLISHED/aitldr (those hold only the 2024 a1-a100 series and the b01-b20 series); no title match)
- `x3SgWqdW-wQ` — From Zero to Viral: AI-Powered Video Ad Creation (YouTube; YouTube fallback: not on T7 aitldr-cold or youtube-PUBLISHED/aitldr (those hold only the 2024 a1-a100 series and the b01-b20 series); no title match)
- `iXu4QeKkSmA` — Animate Multiple Characters Easily with Dzine AI (Lip Sync + Motion) (YouTube; YouTube fallback: not on T7 aitldr-cold or youtube-PUBLISHED/aitldr (those hold only the 2024 a1-a100 series and the b01-b20 series); no title match)
- `z1jM3mF5hCk` — Epic AI Movie Poster Showcase — 50 Styles | Use Chat GPT to Generate (YouTube; YouTube fallback: not on T7 aitldr-cold or youtube-PUBLISHED/aitldr (those hold only the 2024 a1-a100 series and the b01-b20 series); no title match)
- `kMXkKzlKNnQ` — Google's Notebook LM Just Changed Everything! (YouTube; YouTube fallback: not on T7 aitldr-cold or youtube-PUBLISHED/aitldr (those hold only the 2024 a1-a100 series and the b01-b20 series); no title match)
- `ciRCM-SRZII` — I Turned Static Infographics Into Motion Using AI (Nano Banana + Veo 3) (YouTube; YouTube fallback: not on T7 aitldr-cold or youtube-PUBLISHED/aitldr (those hold only the 2024 a1-a100 series and the b01-b20 series); no title match)
- `7O_-z6xaFi4` — I Connected ChatGPT Images 2.0 to Claude (Insane Results) (YouTube; YouTube fallback: not on T7 aitldr-cold or youtube-PUBLISHED/aitldr (those hold only the 2024 a1-a100 series and the b01-b20 series); no title match)
- `lWKzuIjwQvQ` — I Automated Nano Banana With Claude Code Skills (YouTube; YouTube fallback: not on T7 aitldr-cold or youtube-PUBLISHED/aitldr (those hold only the 2024 a1-a100 series and the b01-b20 series); no title match)
- `BA435LYtYho` — How to Create Your Own AI Cartoon Series (Full Workflow) (YouTube; YouTube fallback: not on T7 aitldr-cold or youtube-PUBLISHED/aitldr (those hold only the 2024 a1-a100 series and the b01-b20 series); no title match)

## Not established

- Only 3 of 10 viewed on contact sheets; the sub-look split for the other seven is inferred from cut rate and title, not looked at.
- Whether the in-video presenter in the older videos was a real person or the avatar was not established.
- Frames are 640 px, one every 2 s; anything faster than 2 s (flash cuts, sub-second graphic pops) is invisible to the frame review and only partly visible to the scene detector.
- Share estimates are by eye from 16-frame contact sheets (16 evenly spaced frames per video) on a subset of videos, not counted on every frame.
- YouTube-sourced files are re-encoded at ≤720p; FliVideo/T7 files are the editor's own export. Scene scores can differ slightly between the two.

## Who reads this

Nothing reads it yet — there is no seam. Checked: `flivideo:broll-pilot` (skill) and its spec `~/dev/ad/flivideo/flistudio/docs/planning/broll-pilot/spec.md`: B-roll Pilot is a **catalogue** of described assets (`broll.register` / `broll.describe.*` / `broll.list`); it "never places anything on a timeline and never picks" and has no notion of a script style. Placement is "Timeline Pilot, later" (not built). `flivideo:fliedit` lays overlays on a FliCut export through typed capabilities (`edit.*`), driven by an agent or David; it takes no style input, and a grep of the flistudio, flicut and fliedit docs for "script style" found nothing. The natural future reader is whatever picks B-roll for a script (Timeline Pilot or an auto-edit step), reading this file by style name next to `STRUCTURE.md`. Not built; not proposed in code.
