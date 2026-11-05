# Style matrix — Story Pilot script-style library (text lane, 2026-11-05)

| Style | Structure guide | Verbal-style guide | Script type | Sample size | Strongest trait | Fit for Story Pilot |
|---|---|---|---|---|---|---|
| **mike** (OpenRig, Mike Schwarz) | `mike/STRUCTURE.md` (`mike-structure`) | `mike/VERBAL-STYLE.md` (`mike-verbal`) | story (long); one tutorial variant | 3 long + 3 short measured; story format n=2 | Opens on a bare claim grounded in a real count, then traces an incident back step by step and flips the frame at the close | Best match to `story / long`; the only story-led style here. Sample is tiny and the newest video (Q) is a tutorial, so story guidance rests on 2 videos |
| **aitldr-old** (Series A) | `aitldr-old/STRUCTURE.md` (`aitldr-old-structure`) | `aitldr-old/VERBAL-STYLE.md` (`aitldr-old-verbal`) | tutorial / showcase | 25 of 25 (21 FliVideo + 4 filled from captions) | Fixed like-subscribe-bell sign-off (17 of 19 from mid-2025) and an early community plug | Low priority: hype-heavy, superseded by Series B, the boilerplate is a brand tic not a structure |
| **aitldr-new** (Series B) | `aitldr-new/STRUCTURE.md` (`aitldr-new-structure`) | `aitldr-new/VERBAL-STYLE.md` (`aitldr-new-verbal`) | tutorial / skill demo, 2-3 min + 30 s short | 27 long (22 scripts, 17 finals, 1 caption), 18 shorts (12 companions, 6 standalone) = 45 of 45 | A named section template (HOOK, PROMISE, plug, TOOLS INTRO, 3-4 beats, BEST HIGHLIGHT, CTA) with a number in the hook | Strongest `tutorial / short` fit; has real scripts with planned timings; two template generations so Story Pilot must pick one |
| **appydave** | `appydave/STRUCTURE.md` (`appydave-structure`) | `appydave/VERBAL-STYLE.md` (`appydave-verbal`) | tutorial / build-along (long) | 22 distinct recordings (of 25) | Thinking-aloud "we" narration of a live screen, with a "day N" series frame and the "I'm AppyDave" sign-off | Good `tutorial / long` fit and David's own voice; transcripts only, no scripts, 12 of 25 are one series |
| **maitis** (@maitis-ai) | `maitis/STRUCTURE.md` (`maitis-structure`) | `maitis/VERBAL-STYLE.md` (`maitis-verbal`) | tutorial / explainer (long) | 15 of 16 long-form | A dollar-figure hook ("this used to cost X, now free") and a chaptered walkthrough | Useful contrast for `tutorial / long` (cost-shock hook, up to 20 chapters); competitor voice, so use the structure and not the wording |

All ten guides carry a `storypilot.guide/1` header (`level: global`). Validation with `parseGuide` is at the M4 gate (not available on the M2).

## Recommendation: offer these four first

1. **aitldr-new** - the clearest, most reusable template, with planned timings and real scripts behind it, for `tutorial / short`.
2. **mike** - the only `story / long` model; offer it, but label it "based on 2 story videos" until more exemplars exist.
3. **appydave** - David's own long-form tutorial voice and a clean intro/overview/demo/outro segment shape for `tutorial / long`.
4. **maitis** - a different hook mechanism (cost shock) and heavy chaptering for `tutorial / long`; gives Story Pilot a genuine second option beside AppyDave.

Hold **aitldr-old** back: its distinctive element is a sign-off boilerplate, its hooks are hype-style, and Series B replaced it.

Reasons: (a) the four cover both `form` values and both `length` values between them (story/long; tutorial/short; tutorial/long x2); (b) three of the four rest on 15+ videos, mike on 2; (c) the two with FliVideo scripts (aitldr-new) have the most checkable structure. Not established: whether any of these styles performs better on the channel; no view or retention data was joined to the structure.
