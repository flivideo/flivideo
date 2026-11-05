---
created: 2026-11-05
timestamp: 2026-11-05T10:30+07:00
---
# Script-style visual matrix

How measured, and what each column does and does not tell you, is in each style's `VISUAL.md`. Short version: cuts/min from ffmpeg scene detection (threshold 0.3, whole video); the other columns are by eye from 16-frame contact sheets of a subset of each sample, so treat shares as rough.

| style (n) | cuts/min (median @0.3 · @0.15) | median shot | shot types | on-screen text | B-roll share (est.) | framing | transitions |
|---|---|---|---|---|---|---|---|
| **aitldr-new** (10) | 1.3 · 4.4 | 16.7 s | AI avatar bookends; full-screen motion-graphic cards; screen capture inside a card frame | Heavy: headline on every card, stickers/callouts, stat tiles | ~75–85 % non-presenter (graphics/screens); ~0 % real footage | Wide medium seated avatar, centred; cards are full-frame | Few hard cuts; mostly fades/in-card animation; visible change ~every 7 s |
| **aitldr-old** (10) | 5.2 · 11.3 | 5.2 s | Two clusters: image/clip + screen montage with prompt cards, and slide decks; avatar at hook/sign-off in 2026 | Lower-third captions, numbered section cards, prompt cards; slides carry headlines | >50 % AI imagery/screens in montage videos; ~100 % graphics in slide videos | Full-frame imagery; avatar wide medium when present | Hard cuts in montage videos; fades in slide videos |
| **appydave** (10) | 1.5 · 4.4 | 12.5 s | Presenter full-frame + screen recordings with presenter picture-in-picture; sparse designed diagram cards in 2026 | Light; diagram/headline cards in 2026 renders; no burned-in captions seen | ~60–75 % screen/graphic under a PiP; ~0 % cinematic footage | Presenter medium shot (bookshelf room); PiP corner; letterboxed screens in Claudemas | Hard cuts, long takes |
| **maitis** (10) | 9.3 · 13.2 | 4.5 s | Host to camera + screen captures + news clips + stock/generated footage + dark UI cards | Heavy: kinetic captions, headline cards, logos | ~50–70 %, including real cutaway footage | Host medium close-up; full-frame B-roll | Hard cuts, fastest of the five |
| **mike** (3) | 0.9 · 3.2 | 26.8 s | Narration over dark motion-graphic cards, generated illustrations, TUI/terminal captures; face-cam rare | One large heading per card + diagram labels | ~90 %+ non-presenter (no real footage) | Full-frame cards; face-cam circle in a corner when present | Very few cuts; cards animate in place |

## Reading the matrix

- Cut rate alone does not separate the styles: aitldr-new (1.3/min) changes the picture about every 7 s through fades and card animation; the 2 s-frame change rate (median per style: aitldr-new 8.1, aitldr-old 13.8, maitis 18.4, appydave 6.7, mike 5.7 per min) gives a similar order (mike < appydave < aitldr-new < aitldr-old < maitis); cuts/min puts aitldr-new just below appydave.
- Maitis is the only style where cutaway **footage** (stock, news, generated video) is a real share; the other four rely on graphics and screen captures.
- aitldr-old is two looks in one bucket (montage vs slide deck); its median hides that.
- Sample sizes: 10, 10, 10, 10, 3. Source mix and caveats per style are in each `VISUAL.md` (Sources / Not established).
