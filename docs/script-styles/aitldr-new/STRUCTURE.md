---
format_type: scripted skill-demo (AITLDR Series B, daily Claude-skill series, long ~2-4.5 min + ~30 s short)
artifact: video-structure
version: 1.0.0
distilled_from: 22 long-video scripts (section maps) + 17 final transcripts + 11 short texts (of 45 selected)
corpus_window: 2026-09-15 … 2026-10-31
generated: 2026-11-05
last_updated: 2026-11-05
prompt: initial forge, script-style library (M2 text lane)
retrieval_pool: FliVideo projects /Users/davidcruwys/dev/video-projects/v-aitldr/b01…b25 (copied to /tmp/ss/corpus/aitldr/)
source: FliVideo project script.md / short-script.md (planned) + <name>-final.txt transcripts (spoken); intent left TODO(David)
schema: storypilot.guide/1
id: aitldr-new-structure
label: AITLDR Series B — structure
type: structure
level: global
gist: A 2-3 minute "skill demo": a first-person proof hook, a one-line promise, a short community plug, a three-to-four-beat walkthrough with on-screen numbers, a use-it-for-clients highlight and a reply-in-the-comments close.
appliesTo: {form: tutorial, length: short}
---

# AITLDR Series B (2026-09-15 on) — Video Structure

This guide covers the **long format of Series B** (27 videos on @aitldr's /videos tab, 127-271 s, the "main" daily video) and, in the Short section, its **~30 s companion** (18 on /shorts). Both come from the same FliVideo project (`v-aitldr/bNN-<skill>`), which holds a long `script.md` and a `short-script.md`.

## Script type it fits
**Tutorial / skill demo** (here is a Claude skill; here is what it did on our own channel; here is how to get it). Hosted by "Alex". Every video is also a funnel to the AI TLDR community on Skool.

## Sources — which text is which
- **Script (planned)**: `script.md` / `short-script.md` from the FliVideo project. Used for the **section skeleton** (22 long scripts, 11 short-scripts). The script files carry production tags (`[ANIMATION]`, `[ON-SCREEN TEXT]`, `[NOTE]`) and section names with planned start times; the spoken text is the `[ON CAMERA]` + `[VOICEOVER]` lines.
- **Final transcript (spoken)**: `<skill>-final.txt` / `<skill>-short-final.txt`. Used for **words, speaking rate, hooks and closes**. 17 long + 9 short.
- Where only a script exists (kind=script-only: 5 long b21-b25, 2 short), counts are marked "script".
- **Matched by title (orch, `matched: by title`, not linked in the project)**: `8uypPWDhDs8` (b04-shot-list `script.md`), `a2EGJnOCpoA` (b01-yt-performance final transcript), `5r8dGfwSbjI` short (b05-title-lab short final + `short-script.md`), `P4c-XkAeJxI` (b26-repurpose `script.md`). They were checked after the guide was drafted and change two details only (below); the headline numbers were not recomputed.
- **Remaining gaps** (FliVideo kind=none, orch filling): long `q724ELdSywE`; short `UJXxVigGahk`, `iWGZOYoGU-w`, `fm1WrkZ9Bvk`, `6zAtQHHg6Io`, `aZjw4FzKZrM`, `Pi2Ggb2hWM4`.
- The scripts follow a shared template, so this guide describes a template, not a free-form human structure.

## Measured (python over script and transcript files; long = final transcript where one exists)
- Duration median **165 s** (127-268), words median **470** (354-688), speaking rate median **164 wpm** (150-180), n=17 finals.
- Short: **81-89 words** (n=9 finals), 27-38 s, 139-184 wpm.
- Script section lists (n=22 long scripts): `THUMBNAIL IDEA` and `NOTES` in all 22; `HOOK` 19, `VALUE PROMISE` 18, `TOOLS INTRO` 18, `BEST HIGHLIGHT` 18, `CALL TO ACTION` 18, `MID-CTA` 16; 3-4 named body sections between TOOLS INTRO and BEST HIGHLIGHT (names differ per skill, e.g. THE CUES / THE PICTURE / ONE TRACK).
- Planned timings in the script headers: HOOK 0:00 · VALUE PROMISE 0:10-0:16 · MID-CTA 0:16-0:25 · TOOLS INTRO ~0:28-0:30.
- Hook length median **30 words** (24-46, n=19 scripts); HOOK is ~8% of the words, VALUE PROMISE ~5%, MID-CTA ~6%, TOOLS INTRO ~11%, BEST HIGHLIGHT ~10%, CALL TO ACTION ~8% (median shares).
- Of 17 final transcripts: a number (digit or number word) inside the first 30 words **14**; a first-person word (my/mine/I/we published) in the first 30 words **12**; a question in the first 30 words **9**; "by the end of this video" **16**; a direct ask to reply/comment in the last 25 words **16**; "links in the bio" in the last 45 words 8 (the scripts say "description" or "Skool"; the finals often differ from the scripts).

## Interpreted
### Two template generations (script sequence)
- **Gen 1** (b03-b21, 2026-09-17 to 2026-10-20, 18 scripts): HOOK → VALUE PROMISE ("By the end of this video, you'll know how to…") → MID-CTA ("By the way, I'm Alex, and if you want all my AI workflows, prompt packs, and tools like this, you can join our AI creator community. Links in the description. Let's dive in.") → TOOLS INTRO ("Two things: Claude Code, and a skill called …") → 3-4 beats → BEST HIGHLIGHT → CALL TO ACTION → THUMBNAIL IDEA → NOTES. (b03 and b05 name the third section INTRO instead of MID-CTA.)
- **Gen 2** "skill-episode variant" (b23-b26, 2026-10-22 to 2026-10-30, 4 scripts, script-only; b26 `P4c-XkAeJxI` matched by title confirms the same PROOF…TEASE sequence): PROOF (0:00) → THE BREAK (0:05) → THE WHY (0:15) → GUIDE (0:22) → WHAT IT GETS YOU (0:30) → HOW WE MADE IT (1:05) → BEFORE → AFTER (1:50) → GET IT (2:10) → TEASE (2:25). The script's own note: "proof first, setup after 1:30 in two lines… Claude and the skill named at HOW WE MADE IT, about 43% in". b04 (`8uypPWDhDs8`, matched by title) is a Gen 1 variant with `INTRO` + `STEP 1: INSTALL / STEP 2: RUN IT / STEP 3` beats and a `VERIFY BEFORE RECORDING` block. b22 (oddec0MA4p8) is a hybrid (HOOK > THE BREAK > THE WHY…).
- TODO(David): is Gen 2 the direction for new scripts, or an experiment?

### Segment map (Gen 1, the majority)
1. HOOK (~30 words, 0:00): first-person proof with a number ("I copied the same little pill into 14 videos."; "Seventy-nine seconds of my three minute screen recording was one spinner.") or "Does X …? Mine did."
2. VALUE PROMISE (0:10-0:16): one sentence.
3. MID-CTA (0:16-0:25): community plug and "Let's dive in".
4. TOOLS INTRO (0:28): Claude Code + the named skill; "No API keys"; install in a sentence.
5. Body (3-4 beats, each with an animation and an on-screen text card holding a number).
6. BEST HIGHLIGHT: the part the host would use, with a client angle ("if you edit for other channels, you can hand a client a finished sound pass the same day").
7. CALL TO ACTION: where to get the skill, one thing to run, a request to reply.

- **First episode** (b01 `a2EGJnOCpoA`, matched by title; 560 words, final transcript) opens on a problem statement ("You're posting videos, but you still don't know what's actually working."), has no "by the end of this video" line and no "Mine did" first-person proof, so the Gen 1 pattern is not yet fixed on day one. The "by the end of this video" count over finals is therefore 16 of 18.

### Short (~30 s)
Lines are id'd `H1…` (hook), `S1…` (steps/promise), `C1…` (calls). Most frequent id patterns: H1 S1-S5 C1 (3 of 11 short-scripts), H1 H2 S1 S2 C1 C2… (variants). It reuses the long video's intro and outro avatar clips ("reused intro + outro, no new words, no new avatar" - Gtn1ThkuylU short-script): hook sentence(s), the "By the end of this video, you'll know…" promise, then a CTA with a reply request. 2 of 9 finals contain "by the end of this video".

## Fidelity checklist
- [ ] a first-person proof or number inside the first 30 words
- [ ] a one-sentence promise before 0:20
- [ ] a community plug ("I'm Alex… join our AI creator community… Let's dive in") by 0:30 (Gen 1)
- [ ] a "Claude Code and a skill called …" intro naming the skill
- [ ] 3-4 body beats, each with a numeric on-screen text
- [ ] a "best highlight" beat with a client or income angle
- [ ] the last two sentences give one thing to run and ask the viewer to reply
- [ ] long total 350-700 words; short 80-90 words

## TODO(David)
- TODO(David): which generation does Story Pilot offer: Gen 1 (promise-and-plug) or Gen 2 (proof-first, plug at the end)?
- TODO(David): is the BEST HIGHLIGHT "sell it to clients" beat a requirement or a monetisation experiment? (the scripts tag it MONETIZATION PLACEMENTS in Gen 2)
