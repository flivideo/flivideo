# Brief: D19 Spaghetti Rig — gather everything into Story Pilot — 2026-11-01

**From:** `flivideo-orch`. **To:** `d19-storypilot-work` (tmux, M4). **Go:** David, 2026-11-01 ~09:55 +07, verbatim:
*"We could create a new video then… it'll be D19… Spaghetti Rig, as an actual story, is based on some of the ideas in
D12. But it's the whole area that we need to build up and document… we did a full week of coding on the spaghetti game
work. We learnt so many problems, and we created so many artefacts. They could all be included… we're testing it out
one more time in a brand new run. This time, we're doing it on AppyStack… we've got a fuck tonne of data… we should
start putting it directly into the video. You have to talk to Roamy to find. Let's gather as much information as we can
and get it all together. There should also be a whole lot of Captains Log around this as well."*

**Project:** `/Users/davidcruwys/dev/video-projects/v-appydave/d19-spaghetti-rig`. It was created through FliStudio's
`project.create` (code `d19`, name `spaghetti-rig`) and is empty.

## Job: gather, don't write the script yet
Fire `flivideo:storypilot` and `flivideo:flistudio` first, and work through FliStudio's verbs (`resources.*`,
`story.sources.set`). **Attach** every source as a resource with a one-line "why it is here". Then order them in Story
Pilot's "story, in order" as a first pass. Do not write `script.md`; David decides the angle after he sees the pile.

## Where the material is (locate all of it; don't assume this list is complete)
1. **Captain's Log.** Fire `captains-log:find`. Sweep text ∪ tag for spaghetti, spaghetti rig, Spaghetti Busters,
   Omer/Omar, gate ladder, AppyRig, ladder. Include Plaud voice logs and ChatGPT dossiers, and attach them as `capture`
   resources with their B-codes.
2. **Published artefacts.** `/Users/davidcruwys/dev/ad/brains/ARTIFACTS.md`, rows mentioning spaghetti / ladder /
   rig. Known so far:
   - Spaghetti Rig Origin Story
   - Validation Pack
   - Ladder Report
   - Run Log
   - Run Sheet
   - Lo-Fi
   - Game Forms
   - Busters Gate Ladder
   - Tier 3 Checkup
   - OpenRig vs AppyRig
   - the OpenRig meetup deck
3. **Run data.** `/Users/davidcruwys/dev/appyrigs/runs/spaghetti/`:
   - `spaghetti-rig/`, which holds the validation pack, weigh-up, tier-3 checkup and run log;
   - `appystack/`, the new run;
   - `appyrig/`.
4. **Brain files.**
   - `/Users/davidcruwys/dev/ad/brains/openrig/spaghetti-*.md`: audit brief, G05 postmortem, learning edits, rig config vs OpenRig.
   - `/Users/davidcruwys/dev/ad/brains/ai-meetups/ai-engineers/2026-10-17-anti-slop-spaghetti-busters-static-analysis-ladder.md`.
5. **Live / recent sessions on this M4.**
   - `appyrig-spaghetti-work`: the AppyRig driver of the game run.
   - The **AppyStack re-run**, tmux group `ladder-appystack`: `orch-lead`, `orch-architect`, `orch-driver` / `driver-appystack`, `gates-desk` and `review-judge`, plus its `decisions-driver.md`.
   - Attach them as `session` resources by name and Claude session id (`sesh:session-recall` if needed). **Read their transcripts; never message, steer or stop those sessions.**
6. **Roamy.** `spgame-spaghetti-work` on Roamy, the week of game coding. Ask it, via SendMessage to `spgame-spaghetti-work` (Remote Control), for a pointer list: its handover / docs paths, key commits, artefacts and the problems learnt. Attach what it sends. It cannot always reply, so if nothing comes back, say so in your report.
7. **D12** (`d12-openrig-agent-teams`, published) for the ideas this builds on. Link it; don't copy it.

## Rules
- Never write into other projects' folders.
- Never move or delete video files or takes.
- Never stop or message the ladder-appystack seats.
- Read-only on other repos.
- Notes stay in the project folder; don't paste transcript quotes into commits elsewhere.

## Done when
- D19 holds the gathered resources, each with a "why it is here", and Story Pilot has a first-pass order.
- Report to `flivideo-orch` (SendMessage):
  - counts by kind;
  - anything you could not reach (Roamy, sessions);
  - the 3–5 strongest story beats you see, each one sentence with its source.
- Stop there.
