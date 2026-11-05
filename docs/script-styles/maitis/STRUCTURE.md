---
format_type: free-AI-tools explainer / screen-recorded tutorial (Maitis @maitis-ai, 6-22 min)
artifact: video-structure
version: 1.0.0
distilled_from: 15 videos (of the channel's 16 long-form; +31 Shorts not sampled)
corpus_window: 2026-08 … 2026-11
generated: 2026-11-05
last_updated: 2026-11-05
prompt: initial forge, script-style library (M2 text lane)
retrieval_pool: /Users/davidcruwys/dev/upstream/tubescripts/maitis/
source: YouTube auto-captions (tube-harvest fetch.py, free yt-dlp) + chapter lists; strategic intent left TODO(David)
schema: storypilot.guide/1
id: maitis-structure
label: Maitis — structure
type: structure
level: global
gist: A price-or-cost-shock hook ("this used to cost X, now it's free"), a chaptered free-tool walkthrough with levels or a clone demo, and a subscribe-and-see-you-in-the-next-one close.
appliesTo: {form: tutorial, length: long}
---

# Maitis (@maitis-ai) — Video Structure

## Script type it fits
**Tutorial / explainer** (a "free alternative" walkthrough, an app-cloning build, or a model-release comparison). Not a story.

## Sources
YouTube auto-captions for 15 videos (the channel has **16** long-form videos in total, newest 2026-11-03; 15 = the 10 most-viewed + 5 newest, but the 5 newest were all in the top 10, so topped up with the next 5 by views = all but the least-viewed). No script files exist for this creator. Channel-wide: 16 long-form + 31 Shorts, no streams tab.
Videos: KscFyux4dVk, qKsMQg4WB6s, nndv3V5Q7HY, 4b-D8Nr0jQc, MuLGacYq7WA, I1ISxjjsKNw, qQ9VBlXlSaI, R4vFYbQTGbY, iaxh4Vt6_SI, WqYoGfbYb7Q, _TWyiaF_sV0, HTrKAn2qJUE, mVh3YktAhDA, sWqlHMUb9ec, 0iFEPUeQyz4.

## Measured (python over caption text with [music] / >> tags removed; chapters from the video description)
- Duration median **644 s** (357-1,335); words median **1,987**; speaking rate median **175 wpm** (164-214); chapters median **8** (4-20).
- Opening (first ~60 words): a number or price ($, "million", a count) **13 of 15**; the word "free" **4**; "Right now,…" opener **3**; "stop scrolling / stop everything you're doing and watch this" **2**; an in-medias-res clip or quote (">>" dialogue) 2.
- First chapter (the hook block) ends at 0:53-2:30 in the five videos whose chapter lists were read (KscFyux4dVk 2:30, nndv3V5Q7HY 1:05, _TWyiaF_sV0 0:53, sWqlHMUb9ec 1:10, HTrKAn2qJUE 1:00).
- Close (last 60 words): the word "subscribe" **14 of 15**; "see you in the next one" in the last 200 characters **8**; a direct "drop it in the comments / tell me in the comments" ask **8**.
- Questions per video: 0-15 (median 5); median sentence 9-16 words.
- Series framing: "day one / day two of learn AI without paying" in 2 (MuLGacYq7WA, iaxh4Vt6_SI).

## Interpreted
### 1. Essence
Name a pain (a bill, a locked-in tool), claim a free route, then show it working in chaptered steps.

### 2. Segment map (from chapter lists)
1. Hook block (0:00 to ~1-2:30): the price shock or launch news, stated as a fact with a number.
2. Levels / setup chapters ("Level 1: What is REA?", "Level 2: Claude Code for free with 9Router", "Install REA", "Connect OpenRouter free models") - nndv3V5Q7HY, KscFyux4dVk.
3. The demo build or test, often 2-4 chapters ("Build a Slack Clone…", "Testing all four apps", "Testing the Free Photoshop Alternative").
4. A catch / honesty chapter ("The Catch About Early Alpha", "Price vs performance: whose charts can you trust?").
5. Recap / final results, then the subscribe close.

### 3. Retention
The chapter list is itself the structure (up to 20 chapters, e.g. _TWyiaF_sV0); numbered "Level 1/2/3" and "Doc 1/2/3" lists carry the viewer; honesty chapters add trust. Middles were not read in full.

### 4. Close
"Subscribe" with a reason ("because there's plenty more where this came from"), a next-episode or part-two promise, a comment prompt.

## Fidelity checklist
- [ ] a price, count or dollar figure in the first 60 words
- [ ] the first chapter ends by 2:30
- [ ] 4-20 chapters, at least one a "catch / caveat / what to know" chapter
- [ ] last 60 words contain "subscribe"
- [ ] speaking rate 164-215 wpm

## TODO(David)
- TODO(David): the 16-video sample is small and recent (2026-08 on); is Maitis's structure meant as a model for cost-shock hooks, or only a competitor reference?
