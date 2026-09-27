# d06 — Presenter headshot artefact (AppyDave) — video fact sheet

**Status: recorded, not edited.** 9 takes on 2026-09-27 (intro → outro all present), in `/Users/davidcruwys/dev/video-projects/v-appydave/d06-presenter-headshot-artefact/hub/`. Two transcripts (03-2, 04-1) end in transcription-loop garbage; the audio is probably fine but the text there is unusable. No titles, launch pack or thumbnail yet. **This is the first live test of the thumbnail system.**

## Titles (drafted here, not approved)
- **Working title:** I Turned My Headshots Into an AI Picker
- Option 1: Which Face Should AI Use? Tagging My Headshots for Thumbnails
- Option 2: 106 Photos of Me, Tagged So AI Can Pick One
- Option 3: My AI Now Knows All My Facial Expressions

## Premise
David has dozens of 2024 studio headshots that he wants AI to use when it builds thumbnails. In Claude Code he has every photo described and tagged against one fixed vocabulary (expression, gaze, framing, outfit), then turns the result into a published artefact, the Headshot Picker. People browse it; AI reads its manifest.

## Who it's for
Creators who use their own face in thumbnails and marketing, and anyone wiring AI into a content pipeline.

## The promise
Your headshots become a searchable library that you and your AI can pick from by concept ("surprised, looking left"). There are two reusable recipes: tag my photos, then publish my picker.

## Chapter by chapter
| # | Chapter | What's shown | Key line |
|---|---|---|---|
| 1 | Intro | David to camera; shows the ChatGPT concept board ("thumbnails like this") | "Are you ever trying to manage your headshot photos for marketing material?" / "I'm Appy Dave, let's get into it." |
| 2 | Overview | The unpublished d01–d03 videos; the ChatGPT board process | "I had all these questions about the presenter itself, like where should they be? What sort of expressions should they do?" |
| 3 | Setup | Older thumbnails using small cutouts of him: black shirt, blue shirt, corporate | "Since I do have about 50 different images… could I bring them into an artifact… and label them?" |
| 4 | Annotate | Claude Code describing every image, building a manifest and ontology; the `/btw as prompt` trick | "There's an ontology, there's a short list…" |
| 5 | Artefact | The Headshot Picker: shortlist, black shirt, grey standing, expressions, filters, the AI links, and two recipes | "I didn't design it for AI, so I've just made one more modification." |
| 6 | Outro | Kybernesis FDE work, the B-roll agent, elephant-sanctuary footage | "Let AI discover them to make the thumbnail that you'll see at the beginning of this video." / "I'm Appy Dave. Please like and subscribe." |

## Strongest visual moments
- **A wall of his own faces**: the picker grid, dozens of David cutouts on a checkerboard, each with an expression tag.
- **One face with its tags**: expression / gaze / framing labels pointing at a single headshot.
- **Photos → picker → thumbnail**: a pile of raw photos, the tagged picker, and a finished thumbnail using one of them.
- The shocked hands-on-cheeks shot (c58) and the surprised shots read instantly at small size.

## Proper nouns
Headshot Picker · Claude Code · artifact/artefact · ontology · manifest · ChatGPT · Kybernesis · B-roll agent · AppyDave · Skool. Transcript mis-hearing: "Are you ever trained to manage" = "trying to".

## Tone / brand
AppyDave: warm, practical builder. **Light mode only.** Brand config: `../../brands/appydave.json`.

## Already decided about thumbnails
- The outro promises that the thumbnail **uses one of the tagged headshots**. So the face is in: this answers "face or no face" for d06.
- Nothing else has been decided.

## Note from David (2026-09-27)
The original 9-tile ChatGPT board (`../../source/board-2026-09-26.png`) almost works as a d06 thumbnail in its own right. It shows many expressions, every one fits the video, and it's literally the thing the video is about. It's not chosen, but it's a strong signal for the `creator_ecosystem` "wall of faces" direction (spec a1), and possibly a new recipe: *the board as the thumbnail*.

## What's missing
Edit, titles sign-off, chapters/timestamps, CTA links.

```yaml
thumbnail_assets:
  brand: appydave
  presenter:
    on_camera: david
    face_in_thumbnail: yes            # promised in the outro
    library: "Headshot Picker — https://claude.ai/artifact/EZbkmPK3zb8Vfi7u5soeQF (manifest.json + agents.md; prefs collection for favourites)"
    library_manifest_local: /Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/headshots-manifest.json
    favourites: none yet              # prefs collection empty on 2026-09-27; picks below come from the manifest's shortlist + expression filter
    picks:                            # cid → absolute PNG (T7); ids are stable
      c58: /Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-58.png   # shocked, hands-on-cheeks, best_pick
      c30: /Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-30.png   # surprised, head-and-shoulders, gaze camera
      c16: /Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-16.png   # thinking, hand-on-chin, waist-up, best_pick
      c29: /Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-29.png   # grin
      c86: /Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-86.png   # thinking, black shirt
      c20: /Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-20.png   # skeptical, arms crossed
      c33: /Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-33.png   # concerned, gaze left
      c13: /Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-13.png   # grin, hands on hips, standing
    not_available: [pointing]         # 'pointing' is in the vocabulary but 0 of 106 cutouts have it
  screenshots:
    - id: headshot-picker-ui
      what: Headshot Picker page, shortlist tab, filters + first two rows of cutouts
      status: have
      path: /Users/davidcruwys/dev/ad/flivideo/docs/briefs/thumbnail-system/videos/d06/assets/headshot-picker-ui.jpg
  footage_frames: []
  logos: [appydave]
  props_real: [checkerboard transparency grid, tag chips]
  headline_candidates:
    - "WHICH ME?"
    - "AI PICKS MY FACE"
    - "AI TAGGED MY FACE"
    - "106 FACES"
  must_be_accurate:
    - "106 transparent cutouts (150 photos total), 2024 studio shoot"
    - "Tags are expression / gaze / framing / outfit, from a fixed vocabulary"
    - "It's a Claude artefact called Headshot Picker"
```
