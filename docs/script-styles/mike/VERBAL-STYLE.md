---
brand: openrig-mike
artifact: verbal-style
version: 1.0.0
distilled_from: 6 transcripts (3 long: H, C, Q; 3 short) - below the skill's 10-15
corpus_window: 2026-04 … 2026-11
generated: 2026-11-05
last_updated: 2026-11-05
prompt: initial forge, script-style library (M2 text lane)
retrieval_pool: /Users/davidcruwys/dev/upstream/tubescripts/openrig/
source: transcripts (auto-captions); strategic intent left TODO(David)
schema: storypilot.guide/1
id: mike-verbal
label: Mike (OpenRig) — verbal style
type: verbal
level: global
gist: A plain-spoken solo engineer: second-person, 11-word sentences, concrete first, honest about what he does not know, no hype words.
appliesTo: {form: story}
---

# Mike (OpenRig) — Verbal Style

> Sample warning: 6 transcripts, auto-captions (punctuation and "Herder"/"Herdr" are caption artefacts). Voice traits below are consistent across all six unless noted.

## Script type it fits
Story or explainer in first person from a practitioner running the thing for real. Not a sales voice. Fits Q-style demos as well (voice is shared; structure differs).

## Sources
AL-PQuB2wy0, CYRJDTcTKhQ, qccsfUnrQ9w, KlzyePs3bSk, yCFSRnPDFqY, vndsXRBPGio.

## Measured (per 1,000 words; how: regex counts on caption text)
| | H | C | Q | Klz | yCF | vnd |
|---|---|---|---|---|---|---|
| "you" | 8.7 | 19.1 | 23.8 | 22.3 | 13.3 | 22.2 |
| "I" | 23.2 | 24.2 | 12.6 | 14.9 | 15.5 | 23.1 |
| "just" | 5.1 | 6.6 | 11.8 | 10.9 | 11.0 | 14.2 |
| "like" | 10.6 | 10.3 | 8.4 | 8.0 | 8.1 | 11.5 |
| "basically" | 0.7 | 1.0 | 0.8 | 0.6 | 0.7 | 1.8 |
| "Now," sentence opener | 1.0 | 0.8 | 7.6 | 2.3 | 0 | 0 |
| "So," opener | 1.7 | n/a | 12.6 | 8.0 | 7.4 | 10.6 |
Median sentence 11-13 words in all six; speaking rate 153-206 wpm.
Observed: the demo/product videos (Q and shorts) use more "you / just / So," than the two story videos, which are "I"-heavy.

## Interpreted
### 1. Essence
An engineer explaining what he actually runs, as if to a colleague at a desk.

### 2. Tone (1-10)
- Formal-Casual: 7 - contractions, "like", "kind of"; but precise terms (seat, pod, rig) are used exactly.
- Serious-Funny: 4 - dry asides ("I asked for a doghouse"), not jokes.
- Respectful-Irreverent: 3 - never mocks the agent: "Pretty reasonable."
- Matter-of-fact-Enthusiastic: 4 - understated; excitement is shown by scale numbers, not adjectives.

### 3. Signature moves (verbatim, from transcripts)
- Honest unknowns: "Well, honestly, I'm not even sure." / "I definitely don't know where it'll be in six months." (Q)
- Plain scale numbers: "I have about 300 agents set up ... around 100 to 200 working throughout the day, across about 60 rigs." (Q)
- Self-correction on the page: "Now, does this just run forever? No. You have to maintain it." (Q)
- Defines the term the first time: "Now, a harness wraps the model and gives it tools." (Q)
- Analogy by comparison to a known tool: "I intentionally modeled this on Terraform and Docker." (Q)
- Starts a sentence with "So" or "Now," to pivot (Q: ~20 per 1,000 words together).

### 4. Anti-voice (not observed in any of the six)
No greeting ("hey guys", "welcome back"); no "game-changer / revolutionary / insane / mind-blowing"; no urgency CTAs ("smash"); no all-caps shouting. TODO(David): confirm which of these you want enforced rather than just observed.

### 5. Cadence
Short declaratives then a longer explaining sentence; story passages run shorter (8-9.5 words median, from the brain, n=1 each). Questions are rhetorical-and-answered ("So how do we fix this babysitting problem? Well,").

## Fidelity checklist (falsifiable)
- [ ] 0 greeting words in the first sentence
- [ ] 0 hype adjectives from the list above
- [ ] median sentence 10-13 words
- [ ] at least one honest unknown ("I'm not sure", "I don't know") per 10 minutes
- [ ] every new term defined in the sentence that introduces it
- [ ] at least one concrete count (agents, hosts, PRs) in the first minute

## TODO(David)
- TODO(David): is "understated" the target, or would you want more energy than Mike?
