---
created: 2026-11-01
by: sessions-rsch
status: research, read-only; no code, skills, sessions, captures or projects touched
---
# How David asks sessions to become story material (2026-10-01 → 2026-11-01)

**Verdict.** The ask has been the same for a month: *"I don't want to read it all, but I want it placed properly, current, and refreshable."* What went wrong each time is not that an agent summarised badly. It is that **nothing carried a stamp saying what a summary was built from, who placed it, or whose angle it served**. The one angle failure I could trace (D19 / AppyStack) is the same hole.

## 0. Method and what I could NOT verify

- **AngelEye was down** (`http://localhost:5051` unreachable), so I read Claude Code transcripts (`~/.claude/projects/*/*.jsonl`) directly with a small extractor that keeps only turns typed by a person or relayed by a named session. I did **not** use `sesh:session-archaeology` / `session-recall`: a month of sessions is too heavy for this machine (load ~28/10) and the brief bans fan-outs.
- **Captain's Log**: I searched metadata (`q=story`, `q=session`, since 2026-10-01; ~52 + 44 hits) and read **one** transcript in full, B667. I used synopses for the rest. I did not read B662, B665, B676 or B677 transcripts.
- **David's three quotes in `_curation-quotes.md`** ("19 boxes", "automatic or synthesised", "how do I know it is stale") reached me only as relayed by `flivideo-orch`. I searched the sessions I could reach and **did not find the original voice/typed turn**. Treat their timestamps and sessions as *unverified*. The angle quote (~13:35) I did find, relayed into session `d19-storypilot-video` at 05:24Z.
- **I could not find the session that "came up with three angles on its own"** (the AppyStack morning). `d19-storypilot-video` (id `933f03ab-2c4c-4654-ba02-0008ec84113e`) never produced angle options; it was told *not* to. The retiring orchestrator `flivideo-orch [b8d399]` is the likely source and its transcript was not located. So **who wrote the three "spaghetti is stupid" angles is unestablished.** What I can show is the D19 agent's later self-report (section 2.5).
- "Sessions" here = Claude Code sessions on this M4 only. Roamy's transcripts were not readable.
- Keyword searches (`angle|stale|synthes…`) rule out nothing: absence of a hit could mean the topic was said in different words.

## 1. Recurring asks (David's words, dated)

Story/video talk only. Code-feature talk is separated in section 5.

| # | The ask | David's words | Where |
|---|---|---|---|
| 1 | **Turn session logs into a narratable script** (the founding ask) | "I want to take all the session logs from Claude. Claude has all those sessions so it knows everything you did to get built… any time I steered the conversation… my recap at the end or my retro where I talk about what did we learn" | Captain's Log **B667**, 2026-10-29 07:04 (Plaud). Dossier version: **B670** (ChatGPT, same day) |
| 2 | **State in the app, thinking in the agent** | "FliStudio… is generally going to be… ordered… It's going to understand concepts like the Claude sessions that you want to use for source material and what order they should come in, maybe even with a little bit of labeling… I'll go over to Claude Code and I'll say… we're working on video D13" | B667 |
| 3 | **Gather first, decide the story after** | "capturing information *before* deciding what goes in a script" (brief paraphrase of David) | `docs/briefs/david-rulings-and-storypilot-handover-2026-11-01.md` B1; D19 brief: "Do not write `script.md`; David decides the angle after he sees the pile" (2026-11-01 ~09:55) |
| 4 | **A change request is an instruction to a writer, not text to paste** | "I'll never be as good a writer as you… you still need to write it properly… make sure that everything is coherent with the greater document." | D13 `fli.notes.jsonl` 2026-10-31 16:49Z; restated in `docs/briefs/d13-opening-rewrite-2026-11-01.md` |
| 5 | **Agent for thinking, UI for fine-tuning** | "at recording time he wants to change a comma or one word himself… that's the rationale for having a user interface" | rulings brief A3, 2026-11-01 |
| 6 | **Make the pile scannable and ordered** | "if you present me with 19 boxes… I'm overloaded… I don't know what I can use. I don't know what the linear order is." | relayed in `_curation-quotes.md`, 2026-11-01 (original **unverified**) |
| 7 | **Know raw from synthesised, and when a synthesis went stale** | "Did they come in automatic, synthesised, or… raw and then synthesised later?" / "how do I know the synthesis is now stale?" | same (original **unverified**) |
| 8 | **Find the old conversation** | B662 (2026-10-28 08:00, Plaud): asks whether an earlier conversation "in this project or another" covered the videos and apps he planned. Synopsis only; I did not read the transcript | Captain's Log B662 |
| 9 | **Cross-session knowledge must survive window closes** | "Send me what is in your head that is NOT on disk" (relayed rule for a closing session, 2026-09-03) | `video-projects-orch` → session `9e3f5c4e…` |

## 2. Failure patterns, with evidence

### 2.1 Paste instead of write (wrong action on a spoken ask)
David dictated a rewrite of D13's opening. It was pasted almost verbatim as line 1, paragraph 2 then repeated it. He had to re-state the rule (ask 4). **Evidence:** `docs/briefs/d13-opening-rewrite-2026-11-01.md` ("Yesterday his words were pasted in almost verbatim… so paragraph 2 now repeats the opening"); after the rewrite he called it "a wonderful introduction" (rulings brief B3).

### 2.2 Overload: attaching is not curating
D19 was told to gather and attach. It attached **50** sources (docs 20, artifacts 11, sessions 10, captures 5…) each with a one-line "why". D18 has **20** attached and **no `story.json`**, so none are placed (brief context). D13 is the contrasting case: 9 attached, 8 placed with roles. So the "19 boxes" complaint is real in data: more sources do not become a story without a placing step. **Evidence:** D19 session `933f03ab…` 03:04Z report; `_curation-quotes.md` context.

### 2.3 Stale synthesis, silently
- A ChatGPT conversation that continues produces a **new** dossier capture, not an update (e.g. OpenRig: B612 → B619 → B625, three dossiers of one thread). Nothing says B612 predates 40 turns. **Evidence:** B612/B619/B625 synopses; `docs/specs/curation-inventory-2026-11-01.md` gap 2.
- The D19 orchestrator itself warned: "I don't have a feed from ladder-appystack yet… Silence from me does not mean the run hasn't moved." D19's 50-source order was frozen at the 0.5.0 release while the run continued. **Evidence:** session `933f03ab…` 03:18Z.
- Same family earlier: a hardcoded three-directory "referrers" list made "nothing found" read as "none exist". David's rule, relayed 2026-09-08: "A DOCUMENT IS EVIDENCE OF INTENT, NEVER OF STATE… EVERY CLAIM MUST COME FROM THE FILESYSTEM AS IT IS RIGHT NOW." **Evidence:** v-appydave session `3ff165a5…` 2026-09-07 and 2026-09-08.

### 2.4 Unverified synthesis passed off as evidence
On 2026-09-02 a script-voice session picked three transcripts "by duration and category", derived a pattern, and presented it as corpus-derived voice evidence; only one was certified. David: "Stop producing script outlines. Run the voice-fidelity check that has now been asked for twice and not done." **Evidence:** v-appydave session `9e3f5c4e…`, 2026-09-02 02:36Z. (Outside the one-month window by a month, kept because it is the clearest example of the same shape.)

### 2.5 Angle invented, or filled by omission (D19 / AppyStack)
- Morning 2026-11-01: an agent produced angles that framed the spaghetti rig as pointless. David's reply (~13:35): "the spaghetti rig is a great idea. It's just that we haven't got it to work yet, and the video would be more about our getting it to work: an anti-slop AI system."
- His earlier ruling (~10:30, relayed): "I don't think we can answer this question. I could say that A might be the way to go, but we can't answer it until we've done AppyStack… I want the focus… 'I built an OpenRig that turns spaghetti into clean code.' I just haven't been able to prove that it's a true statement yet."
- The D19 session then recorded both as "PROOF PENDING", relabelled the hard beats "struggle", and flagged **one source that cuts against his angle** (`WEIGH-UP.md` §0: the test game "was already clean"; the ladder mostly added boilerplate). It offered two readings (struggle beat vs. conclusion) and let David choose. **That is the working pattern**: the contradiction is surfaced, not resolved by the agent. **Evidence:** session `933f03ab…` 03:10Z and 05:25Z.
- Why the hole exists: Story Pilot settings have `audience`, `feel`, `do` but **no `angle` field** (`curation-inventory-2026-11-01.md` §4). The thesis lived in free-text notes.
- **Not established:** which session wrote the three bad angles (section 0).

### 2.6 Notes landing in the wrong place
Three of seven records in D13's `fli.notes.jsonl` are Story Pilot Lab notes (look-and-feel), not D13 notes. They landed there because the Lab opens on D13's script. The orch also "misfiled the tabs as FliHub-only, and David caught it." **Evidence:** `docs/briefs/d13-video-session-2026-11-01.md` State section; orch background message in session `de04c63c…` 02:40Z. Same family as "raw vs synthesised confusion": the source (a note) was filed by *where it was taken*, not by what it is about.

### 2.7 Mixing code talk into video talk (itself a finding)
- D13's brief had to add a **silo rule**: "Material about Story Pilot as a subject belongs to D18, not D13. Story Pilot is only the tool that wrote D13's script." The D13 folder holds `script/storypilot/` *and* Lab notes about the tool's UI.
- David's own Saturday plan (B676/B677, 2026-10-31) mixes video recording, the Overlay Pilot chin bug, Story Pilot refactor, a FliHub button and FliEdit layering in one breath.
- D18's 20 attached sources are mostly *build* briefs (fli-notes, rail, Lab) which describe the tool, not a story about it. They are the "tool as subject" case and need a separate placing pass.
- **Cost:** a story curator reading these cannot tell "a decision about the video" from "a decision about the code" without that split.

## 3. What "coherent" means to David, in his words

- "make sure that everything is coherent with the greater document" — a local edit must leave the *whole script* consistent (D13, 2026-10-31).
- "I don't know what the linear order is" — coherence includes a visible sequence he can scan (relayed, unverified original).
- "so that I don't actually have to go in and read those things, but know that they're going to be placed properly, know that they're up to date, know that they're refreshable." — **placed + current + refreshable**, three separate properties (relayed).
- Angle-level coherence: "the video would be more about our getting it to work" — the *throughline* decides which sources are the story and which are struggle beats (D19).
- Not coherence: more detail. His reading-taste rule from the same day is related: the first "wall of text" screen needs contrast around the focus; rich text is hard, terminals easy (rulings brief B3).

## 4. Prior mining vs. new here

**Reused (cited, not redone):**
- `docs/specs/curation-inventory-2026-11-01.md` (curation-rsch): skill gaps, Listen's content-hash staleness model, no `angle` field, `storypilot-prep` naming. I **agree with all of it** and add only the evidence of how each gap bit in practice.
- `brains/video-as-code/aitldr-jan-workflow-observation-2026-10-09.md` Note 4 and `…dossier-2026-10-09.md`: **topic → angle → outline → script**, `/angle` as its own skill producing "3 angles + a recommendation", the chosen angle a *field* the script reads, and "up-front vs after the fact" (Jan prepares before recording; David mostly after, because he ad-libs). This is the first time David stated the angle model.
- `agents/ylo-thumbs/work/appydave/d12-openrig-agent-teams/ANGLES-d12.md`: an angle gate that works: three angles A/B/C each with a quoted cue, David picks, later "Change 01" rewrites them on his feedback. The angle was derived from the *finished* video's transcript.
- David's 2026-09-08 rule, 2026-09-02 voice-fidelity correction: reused as precedent for stale and unverified synthesis.

**New in this doc:**
1. The **ask as a time-ordered list** with quotes (section 1), tying B667 to the November requests.
2. The **angle timeline** (below).
3. Evidence that **placing, not attaching, is the missing step** (D13 8/9 placed vs D18 0/20 vs D19 0/50 ordered by a first pass).
4. The **silo problem** (2.7).
5. A caveat that three of David's quotes are unverified at source.

### Angle: before curation, or out of it? (answering David's "chicken or egg")
Observed order across projects:

| Video | When the angle was set | How |
|---|---|---|
| D12 | **After** the cut, from its render transcript | Agent proposed A/B/C with timestamps; David picked/revised (ANGLES-d12.md) |
| D10/D11 | **Before** angles: "step 2a, his ≤5 questions" then an angles gate | David's take first, then options (D10 kickoff session, 2026-10-13: "an area of understanding what the video is about and asking me my opinion before we do angles") |
| Presenter-headshot (Oct 9) | Three angles on one topic, written after the fact | B613/B614 |
| D13 | Never an angle field; the throughline came from David's own sentence ("she's fucking good at it, but I'm the problem") applied as a rewrite | 2.1 |
| D19 | **David held it open** pending the AppyStack run; offered a *provisional thesis* instead | 2.5 |

**My take, from the evidence:** both, in this order. A **provisional angle in David's own words, marked provisional and dated**, comes first, because without one curation can only be "everything, summarised" (the 19 boxes). The evidence then confirms, sharpens or contradicts it, and **a contradiction goes to David, never gets resolved by the agent**. D19 shows the half that already works (a source that cuts against the angle gets flagged). The hole is that the provisional angle has nowhere to live except notes, and no one marks an agent-proposed angle as an agent's.

## 5. Code-feature talk vs video/story talk (kept separate)

Out of scope here but met on the way: fli-notes v1/v2, the Lab variants, side tabs, the rail, hold-⌘⇧ capture, SuperRig, FliHub side panels, screenshots-in-notes. These are *Story Pilot as a tool*. They matter to this research in one way: they were the bulk of what D18 collected, so D18 is currently a tool diary rather than a story.

## 6. Open questions I could not close

1. Original, timestamped source of David's "19 boxes", "automatic/synthesised" and "stale" quotes.
2. Which session produced the three AppyStack angles.
3. Whether any Captain's Log capture between 2026-10-01 and 11-01 contains an earlier ask for a refresh/staleness feature (I read only synopses).
4. Roamy-side sessions (e.g. `afaf0ee4…`, copied to the M4, which I did not open).
5. A cheap confirmation, once AngelEye is up, via `get_day_conversations` for 2026-11-01.
