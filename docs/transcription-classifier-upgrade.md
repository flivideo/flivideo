---
created: 2026-10-05
status: design for David's review (robustness phase 2, write-up 9). NOT to be built now; David: "I'm not saying we use it now."
owner: flitools
brief: /Users/davidcruwys/dev/ad/flivideo/docs/briefs/transcription-robustness-2026-10-05.md
related: /Users/davidcruwys/dev/ad/flivideo/docs/post-transcription-rules.md · /Users/davidcruwys/dev/ad/flivideo/docs/transcription-audit-trail.md
---

# Upgrade path: fast classifier models inside the post-transcription rules stage

**The ask.** David: *"there's a whole new class of ways of solving this problem that might be free or near-free and
fast… we have the ability to upgrade to these options through the same little post-review package… none of that
makes sense until such time as you've got a bit of an audit trail."* So the rules stage gets a **pluggable decision
provider**. Today's deterministic rules are one provider; a classifier can be another, behind the same interface,
measured before it may act.

## What the research says (found, cited)
- **Jev** is a hosted "System One" decision model from TypeSafe AI (`jev-1.13.0`, `POST https://api.typesafe.ai/v1/systemone`,
  $0.042 per million input tokens, output free). It returns a typed answer plus a probability for questions you define:
  Choice, Score, and **Noul** (a yes/no with a 0–1 probability). "It is not an LLM… nothing cheap and calibrated sits
  between 'regex' and 'call Claude'." (`/Users/davidcruwys/dev/ad/brains/jev/INDEX.md` line 27;
  `/Users/davidcruwys/dev/ad/brains/jev/jev-fundamentals.md`)
- **Speed and cost claims are vendor numbers**: "20–200× faster, 40–400× cheaper than comparable LLMs". Real accuracy on
  David's data: unknown. (`/Users/davidcruwys/dev/ad/brains/jev/jev-hype-vs-measured.md`)
- **Local open clones** (Jev's weights are closed): **Von** (ModernBERT 395M with 3 decision heads, under 15 ms per
  decision, CPU only: "safest pilot"); **Kev** (Qwen3.5 0.8B/4B/9B, 87–88%); **SemIf** (stock Qwen3.5-4B, 81%, logit
  scoring, no training). Only Von-sized models are plausible on the M4, and that is unmeasured.
  (`/Users/davidcruwys/dev/ad/brains/jev/jev-local-alternatives.md` lines 34–50)
- **The one measured classification comparison** is Captain's Log's, and it was LLM against LLM (Haiku vs Sonnet on 329
  captures). Jev was never run: "the only measured one".
  (`/Users/davidcruwys/dev/ad/apps/captains-log/docs/reports/haiku-enricher-shadow-2026-09-25.md`)
- **Clef** (David: "Jev now has competitors from Cloudflare, and it's called Clef"). It isn't written up in the brains
  on the M4 or on Roamy yet, so these facts come from the public sources, checked 2026-10-05:
  - Cloudflare launched it 2026-10-01. There are two sizes, **Clef** and **Clef-flash**, both open-weights decision
    models and **API-compatible with Jev** (state plus typed questions in, a probability per option out).
    (https://blog.cloudflare.com/clef-decision-models/ ; https://developers.cloudflare.com/workers-ai/models/clef/)
  - Clef is 27B, fine-tuned from Qwen3.8-27B, and it also reads images. It's **on Ollama**, so it can run locally.
    (https://ollama.com/library/clef)
  - Hosted on Workers AI: Clef-flash 9¢ and Clef 24¢ per million tokens, against Jev's 4.2¢ (community comparison,
    r/LocalLLaMA). OpenAI announced a Decisions API in limited preview on 2026-09-29, so there are now three in two
    weeks (https://flaviocopes.com/clef/).
  - **What this means here:** the provider interface below is Jev-shaped, so Jev, Clef and Clef-flash all plug into it
    with the same request. A 27B model is too heavy for the memory-squeezed M4. It might fit on the M2 (32 GB), but the
    M2 runs CrisperWhisper and has one-job memory rules. Clef-flash's size and Von (CPU) are the local candidates to
    measure.

## The shape: candidates, providers, an arbiter

```
 words after levelling
        │
        ▼
 CANDIDATES (deterministic, cheap)          e.g. every "school"/"skill", every bare number that might be a ratio,
        │                                        every "I" in a stretch where AI is the topic
        ▼
 PROVIDERS answer each candidate            deterministic@<commit>   (acts today)
        │                                   classifier:von@<ver>     (shadow: logged, never applied)
        ▼                                   classifier:jev-1.13.0    (shadow, if hosted is allowed)
 ARBITER: which answer is applied           rule state (auto/review) + the provider's promotion status
        ▼
 decisions[] (Layer 1) + every candidate and every provider's answer (Layer 2, transient)
```

```ts
type Candidate = {
  id: string; rule: string; at: number; words: string[];      // what is being judged ("school" at 33.68)
  window: string;                                            // ±8 words of context
  engines: Record<string, string | null>;                    // what each engine heard at that place
  options: string[];                                         // ["keep", "Skool"]
};
interface DecisionProvider {
  id: string; version: string;                               // "deterministic" / "classifier:von"
  mode: 'act' | 'shadow';
  decide(c: Candidate[]): Promise<Array<{ id: string; answer: string; confidence: number }>>;
}
```

- **The candidates stay deterministic.** A classifier never chooses *where* to look, only *what* a candidate is. That
  keeps the volume small and the trail complete.
- **Mapping to Jev:** one Noul per candidate. "In this sentence, 'school' names the Skool community platform." The
  probability is the confidence. A Choice question suits several options ("16:9 / 9:16 / a number").
- **The deterministic provider's confidence is 1.0** when it fires and 0 when it doesn't, so both providers are scored
  on the same records.

## Before a classifier may act: measured, then promoted
1. **Shadow.** It answers every candidate. Its answers go into the transient trail only, never into the words.
2. **Scored against two references:**
   - **David's verdicts** (confirmed / rejected review decisions): the labelled set;
   - **the deterministic provider**: agreement, and where they differ, who was right by David's verdict.
3. **Promotion gate** (David's call; a proposal):
   - at least 50 labelled candidates for that rule;
   - precision at or above the deterministic provider's on the same set;
   - no confirmed decision overturned.
   Then it may act, in `review` state first, like any new rule.
4. **Demotion:** if a rejected decision came from the classifier, it goes back to shadow for that rule.

## What the audit trail (write-up 8) must record for this to work
- Every **candidate**, including the ones no provider changed. Without the negatives, precision can't be measured.
- Every **provider's answer and confidence**, with provider id and version, on the same candidate id.
- David's **verdict**, joined to the candidate id, kept durably (it is the training and test set).
- The **window and engines' words** as the provider saw them, so a disagreement can be replayed.

## Where it pays and where it doesn't (honest numbers)
- **Today's rules see very few cases.** D01–D06 gave **5** format/context candidates. A classifier gains nothing there,
  and 50 labels would take months.
- **Where it could earn its place is "I" → AI.** That is vote-only today, so it is fixed only when another engine heard
  "AI" at that spot. When every engine heard "I", nothing fixes it. "I" occurs 3–50 times per project (122 across
  D01–D06, about 25× the format/context candidates), so the candidate set grows fast enough to label, and a classifier ("does 'I' here mean AI?") could catch what no engine heard. That is the
  first rule worth a shadow run, once the trail records candidates.
- **Privacy:** hosted Jev sends transcript text to TypeSafe. Groq already receives the audio for pass 1, so the text is
  not more sensitive, but the M2 never calls out and holds no keys, so a hosted provider runs on the M4 only. **Von on
  CPU** is local, free and keyless, and the research names it the zero-risk first test.

## Recommendation (when the trail exists, not now)
Build Layer 1 of the trail, then the candidate records in Layer 2. Then run **Von in shadow on the "I"/AI candidates**
for D01–D07, scored against David's verdicts on a sample. Clef-flash, local through Ollama, is the next candidate. Hosted Jev or Clef is tried only if the local ones fall
short and David agrees to send text out.

## Not decided (David)
1. Whether a hosted provider (Jev) is acceptable at all, or local only.
2. The promotion gate numbers.
