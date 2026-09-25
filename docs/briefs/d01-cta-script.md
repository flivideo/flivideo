---
type: brief
title: d01 flivideo-tour — call-to-action script (draft)
description: "Draft CTA section for AppyDave video d01 (flivideo-tour): what the last 10 AITLDR videos demonstrate, label options for the creator-skills offer, three spoken CTA paragraphs with an order and bridges, and one visual idea per offer."
created: 2026-09-25
timestamp: 2026-09-25
status: draft — for David to read aloud and cut
---

# d01 flivideo-tour — CTA script (draft)

**Purpose**: Give David a teleprompter-ready call-to-action for d01, with three offers backed by evidence.

**For Agents**:
- Read this before you write or change d01's closing CTA or its end-screen graphics.
- Section A is evidence from the AITLDR channel. The transcripts are listed under Sources.
- Section C is spoken copy. Keep it plain and use short lines. Don't add hype.

---

## ⚠️ Decisions to make before recording

1. **Which Skool does offer 2 point to?** AITLDR's videos send viewers to **AITLDR's own Skool**
   (`skool.com/ai-tldr-3566`, the "AI creator community", presented by Alex). Offer 3 is **AppyDave's Skool**
   (`skool.com/appydave-6257`). The draft below points offer 2 at "the AITLDR channel" and keeps
   one Skool ask, AppyDave's, at the end. If the skills are meant to be downloaded from AppyDave's Skool too, change the
   last line of offer 2.
2. **Don't promise a timeline in the Kybernesis line.** The public page says *6 to 18 months*. The internal FDE
   library says *"agentify a company in a week"*. That conflict is unresolved (see
   `/Users/davidcruwys/dev/ad/brains/kybernesis/fde-engagement-model.md`, section dated 2026-09-25). The script
   avoids both.

---

## A. What AITLDR demonstrates (latest 10 long-form videos)

All 10 are from the channel's `/videos` tab, not Shorts. Most run under 5 minutes, which is normal for this channel.
Upload window: to 2026-09-24.

| # | Title | Skill / workflow shown | What it automates |
|---|---|---|---|
| 1 | Running Out of Video Ideas? Try This Claude Skill | **Idea Bank** (Claude Code skill + Python scoring + yt-dlp) | Mines your own notes for pain points ("by hand", "I had to"), checks demand on YouTube, skips what you've already made, and ranks 30 ideas with evidence. |
| 2 | This Claude Skill Found What Was Wrong With My YouTube Hooks | **Hook Doctor** | Checks a script's hook against rules (length in your WPM, problem-first, proof on screen, matches the title), then writes 5 rewrites of different types. |
| 3 | I Stopped Guessing YouTube Titles—This Claude Skill Scores Them for Me | **Title Lab** | Writes 10 titles from the finished script, scores each against your channel's median views, and writes `titles.md` with the top 3 and reasons. |
| 4 | This Claude Code Skill Creates Your Shot List Before You Record | **Shot List** | Turns a script into four sheets (presenter, VO, shot cards grouped by app, claim checks) and flags narration with no shot and claims the tool can't back up. |
| 5 | How to Make Thumbnails That Get Views Using AI (Full Tutorial) | **Thumbnail skill** (Claude → ChatGPT / Nano Banana) | Learns your brand once, then turns a script into 6 thumbnail prompts ready to paste, across 2 layouts and several render styles. |
| 6 | This Claude AI Skill Writes Your YouTube Scripts for You | **/script** skill + script-generator agent | Takes a topic to an outline you approve, then to a recordable script with timestamps, screen actions, a thumbnail idea and a CTA, saved to an archive folder. |
| 7 | Want to Know Which Videos Are Killing Your Channel? | **YT Performance** skill | Pulls public channel data, separates Shorts from long-form, adjusts for video age, and reports best and worst videos, the channel baseline and patterns. |
| 8 | How to Bring Classical Paintings to Life With AI | **Face-in-painting cinematic** skill (Claude + Zeen) | Builds a character sheet from a selfie and a painting, an empty location, and a monster asset, then writes a director-style animation prompt. |
| 9 | This AI Niche Is Printing Money Right Now (Anime Cooking Shorts) | **Character-sheet + storyboard** prompts → Google Flow agent + Omni | Builds a looping anime cooking short: reference sheet, 6-beat storyboard, panels, and the final clip, with only the broken shots redone. |
| 10 | The Paper Layer Trend Explained (And How You Can Do It) | **Paper video** skill → Google Flow agent → ElevenLabs → CapCut | Turns a poem or story into papercraft scene prompts and animation prompts, then adds voice-over and an edit. |

**Synthesis.** AITLDR is a working, public test bed for a **YouTube pre-production pipeline built from small Claude skills**.
Each skill does one job and writes a file the next one reads. The order is: **Idea Bank → Title Lab → Hook
Doctor → /script → Shot List → Thumbnails**, with **YT Performance** closing the loop. `titles.md` feeds Hook Doctor
and `script.md` feeds Shot List. The pattern repeats across the videos:
- no API keys;
- deterministic Python for the scoring, so the same input gives the same ranking;
- Claude doing the judgement;
- honesty checks built in, such as claim verification and "search shows interest, not your views".

The other four videos (paintings, anime shorts, paper layer, thumbnails) cover the **AI-visual side**: consistent
characters, storyboards, and prompts written for Google Flow, Zeen, ChatGPT and Nano Banana. Together they show the
same pipeline serving a **faceless AI presenter** (Alex) and a human one. Shot List even has a "presenter, camera"
mode for people who film themselves. That is the case for offer 2.

---

## B. Label options for offer 2

The current label is *"simple skills for automating content creation workflows for human and AI influencers"*. It is
too long to say, and "influencers" reads as social-media-personality rather than YouTube creator.

| Option | Why it might work | Weakness |
|---|---|---|
| **Claude skills for creators** ⭐ | Uses the exact phrase the AITLDR titles use ("This Claude Skill…"). It is short, and "creators" covers human and faceless channels. | Doesn't name YouTube, but the video context does. |
| YouTube pipeline skills | Names the pipeline, which is the real value (idea → title → hook → script → shots → thumbnail). | "Pipeline" is jargon to some viewers. |
| Creator workflow skills | Plain, and close to David's original wording. | Generic, and says nothing about Claude. |
| The AITLDR skill kit | Branded, and points straight at the evidence. | Means nothing to someone who hasn't seen AITLDR. |
| Pre-production skills | Accurate for 6 of the 10 videos. | Undersells the visual/animation workflows. |

**Recommendation: "Claude skills for creators"**. Say "for on-camera *and* faceless channels" once in the paragraph
instead of putting it in the label. It is the term viewers already search and click on (AITLDR's own titles prove it),
it is short enough for an on-screen chip, and it drops the word "influencers".

---

## C. The three offers — spoken script

### Recommended order: Kybernesis → Claude skills for creators → Skool (keeps David's order)

- **Narrow to broad, highest commitment to lowest.** Kybernesis speaks to a small group (business owners).
  Skool is something every viewer can do today. Put it last so it is the ask that sticks.
- **It calls back to the tour.** Kyber Studio already appears in chapter 4, so the Kybernesis line lands while
  it is fresh.
- **Offer 2 sets up offer 3.** "Here's the evidence, here's where I build it" hands straight into the Skool ask.
- The alternative (skills first, since it is the most on-topic for creators) buries Kybernesis in the middle, where it
  interrupts two creator offers. Not recommended.

Lines are broken for the teleprompter. Each paragraph fills one screen.

---

**1 · Kybernesis — custom agents for businesses**

> Now, a few ways I can help.
> If you run a business, the agent you saw in Kyber Studio
> is the same kind of thing we build for companies.
>
> Through Kybernesis, we build custom agents for your business.
> They sit inside the tools your team already uses,
> and they run in your own accounts.
>
> If that sounds useful, the link's in the description.
> Let's have a chat.

*Bridge →* "But most of you are here for the content side, so…"

---

**2 · Claude skills for creators**

> I also build Claude skills for creators.
> Small skills. Each one does one job.
>
> Find the idea. Score the titles. Fix the hook.
> Write the script. Plan the shots. Make the thumbnail.
>
> And you can see them working.
> My AI TLDR channel has put out ten videos in ten days,
> and every one of them runs on these skills.
>
> They work whether you're on camera or faceless.
> Check out AI TLDR. Link below.

*Bridge →* "And if you want to see how all of this gets built…"

---

**3 · Skool — build FliVideo in public**

> …come and join me in my Skool community.
> That's where I'm building FliVideo and all these tools in public.
>
> You get my own skills, my workflows,
> and the applications you saw today.
> FliStudio, FliHub, FliCast, and whatever comes next.
>
> Link's in the description.
> Come build with me.

*Close →* "I'm AppyDave. See you in the next one." (to match the intro line.)

---

## D. Visual ideas (ideas only, nothing generated)

| Offer | What it shows | Tool fit |
|---|---|---|
| **1 · Kybernesis** | A single agent node drops into a row of the client's own app icons (email, chat, docs). Glowing lines connect them while a small "runs in your accounts" lock settles on the frame. End card: the Kybernesis wordmark on the brand's dark surface. | **HyperFrames**: simple motion graphics, with the dark Kybernesis palette as an accent card inside the light AppyDave video. |
| **2 · Claude skills for creators** | A conveyor of six skill cards (Idea Bank → Title Lab → Hook Doctor → Script → Shot List → Thumbnails). Each drops a file chip (`titles.md`, `script.md`, `shotlist.md`) into the next, and a stack of the 10 real AITLDR thumbnails fans out at the end. | **HyperFrames** for the pipeline animation. Use the real AITLDR thumbnails as images; don't generate new ones, because real thumbnails are the evidence. |
| **3 · Skool** | A workbench "build in public" hero: the FliVideo app tiles (FliStudio, FliHub, FliCast, FliCut) being assembled on a bench, with community avatars gathered around. The Skool URL is shown as a yellow CTA pill. | **Image generation** (Nano Banana) for one still hero, then **HyperFrames** for the kinetic text and pill pop-in over it. Use the AppyDave palette: cream canvas, yellow CTA. |

---

## Sources

- AITLDR transcripts (fetched 2026-09-25 with `tube-harvest` `pick.py` + `fetch.py`, yt-dlp captions, 10/10 fetched):
  `/Users/davidcruwys/dev/upstream/tubescripts/aitldr/`. Batch manifest:
  `/Users/davidcruwys/dev/upstream/tubescripts/_batches/2026-09-25-aitldr-cta/manifest.jsonl`.
- d01 recorded takes: `/Users/davidcruwys/dev/video-projects/v-appydave/d01-flivideo-tour/hub/transcripts/*.txt`.
  ⚠️ `03-4-flistudio.txt` ends in a transcription loop ("I can go back to fly studio" repeated), so the tail of that take may be bad.
- Kybernesis FDE: `/Users/davidcruwys/dev/ad/brains/kybernesis/fde-engagement-model.md`.
- AppyDave Skool URL: `/Users/davidcruwys/dev/ad/brains/skool/`, from the 2026-09-14 discovery audit.
