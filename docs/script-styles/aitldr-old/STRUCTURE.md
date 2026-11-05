---
format_type: tutorial/showcase (AITLDR Series A, pre-2026-09-15)
artifact: video-structure
version: 1.0.0
distilled_from: 25 videos with text (of 25 selected; 65 non-Short videos >=5 min in the era)
corpus_window: 2024-09 … 2026-07
generated: 2026-11-05
last_updated: 2026-11-05
prompt: initial forge, script-style library (M2 text lane)
retrieval_pool: FliVideo store, M4 /Users/davidcruwys/dev/video-projects/published/aitldr/videos/<id>/transcript.txt (copied to /tmp/ss/corpus/aitldr/)
source: FliVideo published-video transcripts (21) + 4 transcripts filled into the FliVideo store from YouTube auto-captions (d_YPcRVnAQM, sBJo4h1q_0E, XJdxVmNyxmg, BA435LYtYho); strategic intent left TODO(David)
schema: storypilot.guide/1
id: aitldr-old-structure
label: AITLDR Series A — structure
type: structure
level: global
gist: A 5-10 minute AI-tool tutorial or showcase — question/claim hook, a promise, an early community plug, step-by-step body, then a fixed like-subscribe-bell sign-off.
appliesTo: {form: tutorial, length: long}
---

# AITLDR Series A (pre-September-2026) — Video Structure

## Script type it fits
**Tutorial / showcase** (how to do one thing with an AI tool; or a "50 styles" gallery). Not a story. Why: the openers promise "I'll show you…"; the middle is steps; no narrative tension was found. Some early items are two-voice "podcast" dialogues (see Measured).

## Sources
Text used for **transcripts only** — there is no script file in FliVideo's store for this era (kind=store: `transcript.txt`, the spoken words, unpunctuated in many cases). 21 came from the FliVideo store; 4 (`d_YPcRVnAQM`, `sBJo4h1q_0E`, `XJdxVmNyxmg`, `BA435LYtYho`) were missing there and are YouTube auto-captions now filled into the store (sources.json note "filled from YouTube captions"). No gaps remain. Selection method: 25 of 65 non-Short @aitldr videos >=300 s before 2026-09-15, stratified by quarter, top views per quarter (docs/script-styles/selection.json).
Videos: f-fYGjCmbp4, -BpLUPgwg4A, ZOGacWMMYYI, AWaAj15enVE, x3SgWqdW-wQ, zAtTJGj4Wbg, xeOqo7nB08Q, iXu4QeKkSmA, WdvkyImhJIw, lDFyPts_jWI, z1jM3mF5hCk, kMXkKzlKNnQ, I1V-ACIpon4, 7_0Alw1tGVE, IgxYt5snV1U, CZXZyMyo_lo, aGxqn6jnSFU, ciRCM-SRZII, lWKzuIjwQvQ, 7O_-z6xaFi4, WRPtQMPw1rg, d_YPcRVnAQM, XJdxVmNyxmg, sBJo4h1q_0E, BA435LYtYho.
Read for the skeleton: the openings (first ~70 words) and closings (last ~45 words) of the first 21 store transcripts and the 4 filled ones, plus their measured stats; middles were not read in full.

## Measured (how: python over transcript text; words / duration from metadata; sentence stats only where the transcript is punctuated)
- n=25. Duration median **372 s** (304-808), words median **1,027** (652-1,605), speaking rate median **141 wpm** (119-196; the 196 is the dialogue item ZOGacWMMYYI). The 4 filled captions: 154, 143, 144 and 157 wpm.
- Sign-off boilerplate **"Don't forget to like, subscribe, and hit the bell icon for more exciting updates."**: present in **0 of 6** videos before 2025-07-18, in **17 of 19** from 2025-07-18 on. The two exceptions: lDFyPts_jWI (2025-09-29) ends "hit subscribe for more AI video guides"; sBJo4h1q_0E (2026-07-12) ends "like subscribe and hit the bell so you don't miss the next one".
- "Community / link in the description" plug inside the first 20% of the text: **14 of 25**; the word "community" first lands at 25-80 s in 12 of those.
- "Step one" appears in **8 of 25**; "Section one" in 1; "Let's dive in / get started / jump / begin" in 10.
- Opening shape (first ~80 chars): question / "what if" / "imagine" = **10 of 25**; claim, demo-first or "stop scrolling" statement = 15 of 25.
- Questions per minute median **0.21** (0-2.17) - not a question-driven style.
- Two-voice "podcast" dialogue or character voices (`>>` or `[music]` tags): ZOGacWMMYYI, -BpLUPgwg4A, aGxqn6jnSFU (partly), iXu4QeKkSmA, kMXkKzlKNnQ, IgxYt5snV1U.
- **New with the filled captions - two story/cartoon showcases:** XJdxVmNyxmg ("Imagine building a gigantic ship on dry land before a single drop of rain had fallen. That was Noah's task." - a Vox-style video built to demonstrate the method) and BA435LYtYho (an AI cartoon series; opens in character voices). Both still end with the standard like-subscribe-bell line. This widens "tutorial/showcase" to include narrated stories as the showcase content, but the host-facing sections (promise, plug, sign-off) are the same.

## Interpreted
### 1. Essence
One tool or one trick explained to a creator audience in 5-10 minutes, with a gift (prompt pack / community) offered early and a fixed sign-off.

### 2. Segment map
1. Hook (~20-50 words): question ("Have you ever…", "What if…") or a bold claim (2026 videos lean to a claim or a shown artefact: "The intro you're watching right now took me about 60 seconds to create.").
2. Promise: "In this video, I'll show you…" (9 of 25 contain "in this video").
3. Community plug and/or link-in-description, often inside the first minute (14 of 25).
4. Body: numbered steps ("Step one…") or a 50-item gallery, tool UI on screen.
5. Reflective close question or recap.
6. Fixed sign-off (see Measured).
Proportions of the middle were not measured.

### 3. Retention
No re-hook device was found in the sampled openings/closings; length is carried by the list or gallery. TODO(David): are the 50-style galleries a deliberate retention format?

### 4. Close
Like/subscribe/bell boilerplate, community link, sometimes "see you in the next one" (7 of 25), occasionally a vote request ("I'll build whichever one gets the most votes", lWKzuIjwQvQ).

## Fidelity checklist
- [ ] hook is a question/what-if or a claim in the first 2 sentences
- [ ] an explicit promise sentence ("in this video…") before minute 1
- [ ] a community/description-link plug within the first 20% of the runtime
- [ ] body in numbered steps or a counted list
- [ ] final sentence is the like-subscribe-bell line (from mid-2025 on)
- [ ] total words 650-1,600 for 5-13 minutes

## TODO(David)
- TODO(David): is this the structure Story Pilot should offer, or only the 2026 variant (claim-first, artefact-first)?
- TODO(David): era boundaries: where does "Alex-hosted" start and stop inside this sample?
