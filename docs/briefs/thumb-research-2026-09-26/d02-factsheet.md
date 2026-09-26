# d02 — Cutty audio cleanup (AppyDave) — video fact sheet

**Status: recorded.** 18 takes, about 1,050 words, 5:52 before the edit. A launch pack exists (titles, description, chapters, 24 thumbnail prompts). An agent (YLO) wrote all of it standing in for David, and **David has not approved any of it.** Thumbnail images have not been generated.

## Titles (from launch-export.md, not approved)
- **Working title:** I Built an AI Agent That Cleans My Audio | Meet Cutty
- Option 1: Clean Audio in a Noisy Room, No Studio (YLO's top-scored title)
- Option 2: Clean Audio in a Noisy Room: The Agent That Kills Hiss
- Option 3: Your Editor Is Clipping Words — Here's How I Catch It

## Premise
David records in a room with fans and an air conditioner running. Cutty, his AI "first-level assistant editor", separates the audio from the video, cleans it with several models, and flags words that may have been clipped. The result is clean audio with no studio.

## Who it's for
Creators who record regularly and fight hiss, uneven volume, and editors (Gling, Descript) that cut off words.

## The promise
Clean audio in a noisy room, from a good mic and a simple camera. You compare the profiles by ear. Krisp's noise suppression is no longer in the chain, so no words get suppressed.

## Chapter by chapter
| # | Chapter | What's shown | Key line |
|---|---|---|---|
| 1 | Three audio problems | David to camera | "How much grief is audio processing causing you?" / "I've got a couple of fans and an air conditioner going on, and it's creating a lot of hiss." |
| 2 | Why I built Cutty | Clips from his Kybernesis agent videos where the audio was poor | "What Kybernesis builds is a full agent system." |
| 3 | Meet Cutty | The agent team (Brandy handles branding, Vicky does overlays, Cutty does audio). A flow diagram: separate the audio, split it across models, de-hiss, level, denoise (DeepFilterNet), reattach. | "It's my first level assistant editor." |
| 4 | Comparing audio profiles | A generated page for each video with 4–6 audio profiles: raw, levelled, de-hissed, fully denoised. A **red line** marks a word that may be clipped. | "One of the biggest issues I have… with video editors like Gling and Descript where they're cutting off words." |
| 5 | Recap / FliCut | Clean audio in a noisy room. FliCut plays and auto-removes ums and ahs, controlled by Cutty. | "I name my agents after the micro apps that I build for them." |
| 6 | Outro | Tease for d03 (finding the presenter's frame). Plugs for Kybernesis and the AppyDave Skool. | "I'm AppyDave, please like and subscribe." |

## Strongest visual moments
- The noisy room: fans and an air conditioner behind a calm presenter.
- The stacked audio-profile waveforms, going from jagged raw to clean.
- The red "clipped word" marker on a waveform.
- The team of named agents (Cutty, Brandy, Vicky).

## Proper nouns
Cutty · FliCut · Kybernesis · AppyDave · DeepFilterNet (DFN) · Krisp · Gling · Descript · Brandy · Vicky · Skool. Transcript mis-hearings to ignore: "Crisp", "CADDI", "Kudi", "FlyCut", "DFN12 or 100". The last one is unclear audio, most likely DeepFilterNet variants.

## Tone / brand
AppyDave: warm, practical builder. Light theme only. Colours: yellow #ffde59, brown #342d2d, cream #faf5ec.

## Already decided about thumbnails (YLO draft, not approved)
- Three A/B slots. Each has overlay text that is **composited afterwards and never rendered by the image model**, plus one small "subliminal" word rendered in the scene:
  - Slot 1: "FANS ON. STILL CLEAN." with subliminal DFN
  - Slot 2: "ONE AGENT. FOUR FIXES." with subliminal CUTTY
  - Slot 3: "IT ATE YOUR WORDS" with subliminal GLING
- 8 styles × 3 prompts, in `launch-thumbnail-prompts.md`:
  - A: 3D paper world
  - B: editorial illustration
  - C: miniature diorama
  - D: AppyDave comic/retro
  - E: bold poster
  - F: photo cutout
  - G: neon brutalism
  - H: white-space paper cut
- Style H is the current default ("very low element count, white as a material").
- Rules: one story, one metaphor, one hero. Red means problem, teal means control. Reserve negative space for the headline.
- Most prompts **exclude David's face**. Whether the thumbnail uses his face at all is an open question.

## What's missing
David's sign-off on the titles and styles, generated images, post-edit timestamps, and the CTA and affiliate links.
