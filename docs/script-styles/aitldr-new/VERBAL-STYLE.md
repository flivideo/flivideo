---
brand: aitldr
artifact: verbal-style
version: 1.0.0
distilled_from: 17 long final transcripts + 5 long scripts (script-only) + 1 long caption fill + 9 short finals + 2 short scripts + 6 short caption fills
corpus_window: 2026-09-15 … 2026-10-31
generated: 2026-11-05
last_updated: 2026-11-05
prompt: initial forge, script-style library (M2 text lane)
retrieval_pool: /tmp/ss/corpus/aitldr/ (FliVideo project files)
source: FliVideo project final transcripts (spoken) and script.md (planned); intent left TODO(David)
schema: storypilot.guide/1
id: aitldr-new-verbal
label: AITLDR Series B — verbal style
type: verbal
level: global
gist: Calm first-person "I tested it on our own channel" narration: a number in every hook, plain verbs, numbers spelled the way a voice says them, one reply-in-comments ask to finish.
brands: [aitldr]
appliesTo: {form: tutorial}
---

# AITLDR Series B — Verbal Style

## Script type it fits
Tutorial / skill demo narration (host "Alex"), 2-3 minutes; shorts of ~85 words.

## Sources — which text is which
Voice traits are measured on the **final transcripts** (what was spoken, 17 long + 9 short); the script files supply the wording of fixed lines (MID-CTA, VALUE PROMISE) and production notes. Where the two differ the transcript wins: scripts say "Links in the description" / "Skool", the finals often say "links in the bio" and "AITLDR" (caption spelling of the brand varies: "clawed skill", "clod skill", "quad code" are caption errors for "Claude").

## Measured (per 1,000 words)
Long (n=23 incl. script-only): "you/your" **40.5** · "I" forms 7.7 · "we/our" 6.4 · "just" **0.8** · "so" opener 2.2 · "actually" 1.7 · "like" 3.2 (vs Series A: you 29.5, just 4.2, like 8.0).
Short (n=11): you 39.1 · I 6.4 · just 0.0.
Recurrent runs (in N of 23 long): "by the end of this video, you'll…" 18; "By the way, I'm Alex, and if you want all my AI workflows, prompt packs, and tools like this, you can join our AI creator community. Links in the description. Let's dive in." 16 (from the scripts); "Claude Code and a skill called" 16; "links in the description" 16.
Speaking rate median 164 wpm; median sentence 9-10 words (finals).

## Interpreted
### Essence
A friendly engineer reporting a measured result from their own channel, then handing the viewer one task.

### Tone (1-10)
Formal-Casual 6 · Serious-Funny 3 · Respectful-Irreverent 3 · Matter-of-fact-Enthusiastic 4. Enthusiasm is carried by counts, not adjectives (Series A used "insane/amazing/next level").

### Signature moves (verbatim, from FliVideo finals/scripts)
- The "Mine did." pivot: "Do your videos end with the same call to action each time? Mine did. Eight videos, one line, word for word." (jWfwJqH3gY4)
- Hard number in the hook: "Seventy-nine seconds of my three minute screen recording was one spinner." (w4LpBamBkCs)
- "Now Claude …": "Now Claude finds that dead time and writes the cut." (w4LpBamBkCs)
- No-friction install: "No API keys. Copy the folder into your Claude skills folder, restart Claude Code, and have ffmpeg installed." (Gtn1ThkuylU script)
- Result sentence with both numbers: "out of the hundred and fifty sounds I'd placed by hand, it landed on a hundred and fourteen." (Gtn1ThkuylU)
- Reply-ask close: "Run it on one raw recording before your next edit. Then drop your longest spinner in the comments." (w4LpBamBkCs); present in 16 of 17 finals.
- Numbers are written as spoken words in the script ("a hundred and fourteen", "Seventy-nine seconds").

### Anti-voice (observed absent in Series B, present in Series A)
"Don't forget to like, subscribe, and hit the bell icon…", "insane", "next level", "unbelievable" openers. Measured: the bell line appears in 0 of the 17 Series B finals' endings (the endings are reply asks); the one exception is the newest long video `q724ELdSywE` (2026-11-04, caption fill), which ends with the full Series A line. Hype: "This is insane." opens the standalone short `Pi2Ggb2hWM4`. TODO(David): ban list.

### Cadence
Hook sentences are short and stacked (3-5 sentences of 5-12 words); explanation sentences run 9-14 words. The host names a limitation honestly ("it finds under a third of what I placed by hand").

## Fidelity checklist
- [ ] a spoken number in the first 30 words
- [ ] "you/your" >= 30 per 1,000 words
- [ ] "just" <= 2 per 1,000 words; filler "like" <= 4 per 1,000
- [ ] zero "insane / amazing / next level / bell icon"
- [ ] the last 25 words ask the viewer to reply or run something
- [ ] numbers spelled the way a voice says them in script text

## TODO(David)
- TODO(David): is the "Alex" persona required in Story Pilot scripts, or only for AITLDR?
