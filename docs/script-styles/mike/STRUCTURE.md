---
format_type: story-led explainer (solo creator, screen-recorded)
artifact: video-structure
version: 1.0.0
distilled_from: 2 story-led exemplars (H, C) + 1 tutorial variant (Q) + 3 short explainers measured only (of 7 OpenRig-channel videos on disk)
corpus_window: 2026-04 … 2026-11
generated: 2026-11-05
last_updated: 2026-11-05
prompt: initial forge, script-style library (M2 text lane)
retrieval_pool: /Users/davidcruwys/dev/upstream/tubescripts/openrig/
source: transcripts (auto-captions) + chapter lists + existing brains analysis; strategic intent left TODO(David)
schema: storypilot.guide/1
id: mike-structure
label: Mike (OpenRig) — structure
type: structure
level: global
gist: Open on a bare claim grounded in something real, hold one argument or question chain for 20-30 min, reveal by tracing back or paying off an early plant, close by flipping the frame.
appliesTo: {form: story, length: long}
---

# Mike (OpenRig) — Video Structure

> **Sample warning.** The forge skill asks for 8-15 exemplars of ONE format. Only **two** videos on disk are the story-led format this guide describes (H, C). The third long video (Q) is a different format (tutorial) and appears as a variant. Treat every number as "n=2 / n=1", not a distribution.

IDs: **H** = AL-PQuB2wy0 "I Run an AI Civilization in Herdr" (2026-09-18, 24:50, 385k views) · **C** = CYRJDTcTKhQ "How My AI Civilization Actually Works" (2026-10-17, 30:18, 113k) · **Q** = qccsfUnrQ9w "Agent Teams That Ship: Run an Everything Factory with OpenRig" (2026-11-04, 19:57, 785 views at fetch).

## Script type it fits
**Story** (long form) for H and C: a real experience told with a spine, ending in an idea. **Tutorial/explainer** for Q (see Variant). Why: H and C teach no commands; they use a real incident to carry a concept. Q walks an install-to-shipped-PR demo, with chapters labelled "Part 1..4".

## Sources
H, C, Q as above. Measured only (not used for the skeleton): KlzyePs3bSk (10:49, 2026-06-30), yCFSRnPDFqY (7:49, 2026-05-22), vndsXRBPGio (7:21, 2026-04-11), all short product explainers.

## Measured (how: caption text; sentences split on . ? !; time = word position / total words x duration, so +-30-40 s)
| | H | C | Q |
|---|---|---|---|
| Words / duration | 4,145 / 24:50 | 6,240 / 30:18 | 3,817 / 19:57 |
| Words per minute | 167 | 206 | 191 |
| Median sentence (words) | 11 | 12 | 11 |
| Questions (sentences ending ?) | 10 | 40 | 21 |
| Questions per min | 0.4 | 1.3 | 1.05 |
| First question at | ~7:25 | ~0:45 | ~0:10 |
| Longest gap between questions | ~374 s | ~140 s | ~259 s |
| Chapters (from description) | 15 | 16 | 24 |
Short explainers: 153-174 wpm, 0-3 questions each.

## Interpreted
### 1. Essence
A solo, screen-led video where one real thing (a fleet, an incident, a demo) carries one idea; the viewer is never asked to follow a command line.

### 2. Segment map (story-led, from H and C chapter lists)
1. **Cold claim + grounding** (0:00-~1:20 H; 0:00-1:18 C): H "agents are forming civilizations now"; C "after that last video, this crazy thing happened" (GitHub Trending). ~5% of runtime.
2. **Route / count the threads** (H ~2:45 "three things"; C 1:15 primer then thesis question at 2:21). ~5-10%.
3. **Tour / setup that earns trust** (H 3:16-10:47 tour + vocabulary; C 2:48-5:00 the Slack incident). ~30%.
4. **The turn: an incident traced back** (H 13:00 doghouse; C 2:48-3:15 "they don't know what they don't know"). Reveal by trace-back (each step "locally defensible").
5. **Abstraction passage** (C 5:30-19:43 ontology/maps, the long middle; H 16:46-20:10 context engineering). Mike names the dip himself: "we spent a long time in abstractions. Let's take a breather" (C 19:43).
6. **Proof on screen** (H 21:51 health view; C 23:39 stress test), signposted "Let's make this concrete".
7. **Frame reversal + next step** (H ~24:00 "warning shot"; C 29:45 "I was using this world building technique on you"). ~5%.
The existing brain (`brains/openrig/spoken-scripts/mike-mechanism.md`) holds the deeper hook / tension / reveal analysis; this guide does not repeat it.

### 3. Hook
- Opens with a claim, no greeting and no channel intro (H, C). Q breaks this: it opens on a second-person relatable line ("If you're like me, you spent a lot of your life in what feels like a factory") and asks a question at ~10 s.
- Hook length: first move lands in 1 sentence; grounding fact by sentence 3-4; the route in 30 s - 2:45 (H).

### 4. Retention
- Two tension engines: an outside argument held for the first half (H, 1 question in 13 minutes) or a dense question chain (C, a question every ~26 s median).
- Story passages use shorter sentences (8-9.5 words median vs ~11 explanation; n=1 passage each, from the brain).
- Self-admitted dips and "honesty brakes" before hard turns.

### 5. Transitions
Spoken signposts: "So, ..." / "Now, ..." openers, "Let's make this concrete", counted roadmaps ("three things", "who, what, how, where" in Q).

### 6. Close
Reverses or reframes the whole video (H, C); Q closes with "does this just run forever? No." then a teaser for the next video and a build-it-with-us ask.

### Variant: tutorial/demo (Q only, n=1)
Hook (0:00-2:46, 14%) → Part 1 set up and a real bug fix to a real PR (2:46-11:14, 42%) → Part 2 keep it running (11:14-14:19, 15%) → Part 3 open the artefact (14:19-16:50, 13%) → Part 4 grow it (16:50-19:04, 11%) → honest close (19:04-19:57, 4%). One bug carries Part 1; a recap "the who, the what, the how" (~10:15); "where" added at ~17:30.

## Fidelity checklist (falsifiable)
- [ ] first sentence is a statement or relatable scenario, not a greeting or "welcome"
- [ ] a real, checkable fact or number appears within the first 4 sentences
- [ ] the number of threads is stated aloud before the body begins (or a Part 1..N roadmap)
- [ ] one incident traced back step by step with each step called reasonable
- [ ] at least one early plant paid off later (named as such: "now you know why")
- [ ] at least one spoken admission of a dip, or an unknown ("I'm not even sure")
- [ ] median sentence length 10-13 words
- [ ] close reverses or reframes the opening, or states honestly what it does not do

## TODO(David)
- TODO(David): why this shape for Story Pilot - do you want the story-led (H, C) or demo (Q) skeleton as the offered default?
- TODO(David): is the "honest dip" device a thing to copy, or just Mike's temperament?
