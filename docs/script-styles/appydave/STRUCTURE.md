---
format_type: screen-recorded build-along / walkthrough (AppyDave channel, newest 25 uploads)
artifact: video-structure
version: 1.0.0
distilled_from: 22 distinct recordings (17 FliVideo store transcripts + 5 FliVideo projects covering 8 videos) of the newest 25
corpus_window: 2025-12 … 2026-10
generated: 2026-11-05
last_updated: 2026-11-05
prompt: initial forge, script-style library (M2 text lane)
retrieval_pool: FliVideo store /Users/davidcruwys/dev/video-projects/published/appydave/videos/<id>/transcript.txt and projects v-appydave/d10…d12 (copied to /tmp/ss/corpus/appydave/)
source: FliVideo transcripts and segment transcripts (no script.md exists for these videos); intent left TODO(David)
schema: storypilot.guide/1
id: appydave-structure
label: AppyDave — structure
type: structure
level: global
gist: A 8-30 minute screen-recorded build-along: a framing question or "day N" recap, "let's get into it", the thing being built with the screen as the script, and a fixed "I'm Happy Dave, like and subscribe, see you in the next video" close.
appliesTo: {form: tutorial, length: long}
---

# AppyDave — Video Structure

## Script type it fits
**Tutorial / build-along** (vibe-coding and agent walkthroughs shown live). Not a story; the narration follows what is on screen. One short exception: `kmau3FiZd6g` (2:55) is a demo explainer.

## Sources — which text is which
- **17 FliVideo store transcripts** (`transcript.txt`, spoken words).
- **8 videos from 5 FliVideo projects** (`v-appydave/d10…d12`): the files are **per-segment transcripts** whose names are the chapter names (`01-1-intro`, `02-1-overview`, …). One project (d12) is shared by three published videos (IL-voVs9IBE, 7KLyrUefQ_c, EH_sax6dUaA) and another by two (M978wEYFz1E, yFOhSJqU5rk), so the 8 videos give **5 distinct segment lists**; word counts per video could not be separated and wpm is taken from the 17 store videos only.
- **No `script.md`/`short-script.md` exists** for AppyDave: nothing here is a planned script.
- Gaps: none (all 25 had a FliVideo source).

## Measured (python over transcript text)
- Store videos (n=17): duration median **937 s** (484-7,343), words median **2,961**, speaking rate median **187 wpm** (152-201), questions per minute median **0.33**.
- Opening shape (first ~15 words, n=17): "Welcome to / It's / This is day N of the 12 days of Claude" **8**; an opening question or "Imagine…" (Are you / Do you love / Could you / Is it possible / Imagine) **6**; other 3.
- Closing (last 200-500 characters, n=17): "I'm Happy Dave" appears in **20 of 22** distinct recordings (anywhere; the caption also spells it "Abby Dave", "Api Dave", so this undercounts); "like and subscribe" in the last 400 chars **12**; "see you in the next video" in the last 200 chars **11**; a community/Skool link in the last 500 chars **10**.
- "Let's get into it" in the first 900 characters: **6** of 17.
- Project segment shares (5 distinct projects; share of that project's segment words):
  - d10 FliCut (X8heILK1aeQ, 8:21): intro 7% · overview 17% · demo 54% · launch/optimising 6% · outro 15%.
  - FliHub/FliStudio (M978wEYFz1E, 9:54): intro 11% · overview 22% · demo 48% (+6% second demo) · outro 8% · behind the scenes 6%.
  - headshots (kn_54J1fxec, 5:33): intro 9% · overview 14% · setup 14% · annotate 28% · artefact 18% · outro 18%.
  - face-tracking (kmau3FiZd6g, 2:55): intro 6% · demo 22% · how-it-works 24% · agents 33% · outro 15%.
  - d12 OpenRig (IL-voVs9IBE, 19:09): intro 6% · overview 8% · four demo blocks 68% · workflows 8% · contrib 3% · resources 5% · outro 1%.
  Intro is 6-11% of words in all five.

## Interpreted
### 1. Essence
Show the thing working on the screen and talk through it, with a recurring frame ("day N of the 12 days of Claude", "in the last video in this series…") that links each video to the previous one.

### 2. Segment map
1. Intro (6-11%): a "Do you wish / Are you…?" problem question or a series recap ("Welcome to day six… I'm happy Dave. Let's get into it.").
2. Overview / progress check (14-22%): "let's look at our quest progress", what was done yesterday, what this video does.
3. Demo blocks (the bulk): narrated "what we'll do is… we can see that…" screen work; often several blocks named after the thing built.
4. Result check or side note (small).
5. Outro (1-18%): invitation to the community ("skill community, link in the description"), a next-video tease where there is a series, and the sign-off.

### 3. Retention
Series continuity (the 12 days of Claude, 12 videos on 2025-12-25 to 2026-01-05) and next-video teases are the observed devices; no mid-roll recap or re-hook is evident in the sampled openings/closings. Middles were measured, not read in full.

### 4. Close
Fixed: community link → "please like and subscribe" → "I'll see you in the next video" → "I'm Happy Dave" (order varies).

## Fidelity checklist
- [ ] opens with a problem question, an imagine-if, or a "day N" recap in the first 25 words
- [ ] a "let's get into it" before 2 minutes
- [ ] screen demo is >= 50% of the words
- [ ] a community link near the end
- [ ] sign-off contains "like and subscribe" and "see you in the next video"
- [ ] speaking rate 150-205 wpm

## TODO(David)
- TODO(David): the 12-days-of-Claude videos (12 of 25) are one series; should a Story Pilot "AppyDave" structure be series-agnostic?
- TODO(David): the Oct-2026 videos have chaptered segments (intro/overview/demo/outro) - is that the structure you want the guide to teach?
