# D11 agent edit — review sheet (2026-10-15)

**Purpose**: First test of an agent hand-editing a FliCut cut. Everything below was applied to
`fli.cut.openrig-youtube-automation.json` through FliCut's own API (one undo step each). Nothing exported.

**For Agents**:
- Read this before re-editing D11 or running the next agent edit.
- Every cut David undoes here is a taste lesson. Record it under "What David changed".

## Result

| | Before | After |
|---|---|---|
| Kept length | 11:32 (691.7 s) | **10:48 (648.0 s)** |
| Removed by this pass | — | 43.7 s across 14 places |
| Spelling fixes | 1 (ECamm Live) | 42 words |

- Backup of the untouched file: `/Users/davidcruwys/dev/video-projects/v-appydave/d11-openrig-youtube-automation/-trash/2026-10-15-before-agent-edit/fli.cut.openrig-youtube-automation.json`
- Undo route: FliCut's history (Cmd-Z, or `edit.restore` to sha `000028`, the state before this pass).
- Your earlier decisions were not touched (anything marked `cutBy: user` was skipped).

## Cuts to check (times are in the NEW edit)

Play each at 2.5×. Undo any you don't like.

| At | Clip | Removed | Why |
|---|---|---|---|
| 3:35 | 04-2 | 1.0 s | false start "and we've got drip", said again straight after |
| 4:16 | 05-1 | 3.7 s | first "movement going on on all four"; the retake says "all 4 seats" |
| 4:37 | 05-1 | 0.9 s | false start "And this is where and" |
| 4:43 | 05-1 | 1.6 s | "That we just saw movement on" restates the line before |
| 5:08 | 05-2 | 8.8 s | fumbled pass: "copy first move plus stage. Don't really know what that's saying… this through to this", redone cleanly next. ⚠️ The kept line now opens "But it is the idea that…", so check the join. |
| 5:57 | 05-4 | 4.0 s | false start "So what we've got going on with the conversation with", restarted after the "uh" |
| 6:25 | 05-4 | 2.0 s | "we might want to play around with it", restated with "a few different thumbnail ideas" |
| 6:31 | 05-4 | 2.2 s | false start "One of the other things from the fly copy" |
| 6:39 | 05-4 | 3.4 s | fumble "a little bit of def default values" (retake follows) |
| 6:43 | 05-4 | 2.2 s | false start "And it's already started to write the key" |
| 9:00 | 06-1 | 2.4 s | false start "After that, we can go and select some from" |
| 9:12 | 06-1 | 2.2 s | false start "lastly, the end screen that it's" |
| 10:04 | 06-3 | 2.7 s | false start "and the FliCut video that we're both seeing everything on" |
| 10:36 | 07-1 | 6.4 s | fumbled CTA "…check out my community. I've got a come to.", redone cleanly next |

## Flagged, NOT changed — your call

1. **03-2 at 2:25: your take choice reads badly.** You toggled this pair four times and landed on keeping
   "What we want to do today though is figure out how to get the same thing working." The next kept line is
   "is get the same sort of team working within OpenRig". Together they say "…the same thing working. is get the same
   sort of team…".
   - **My take:** keep take 2 instead ("What we want to do today though / is get the same sort of team working
     within OpenRig"). In FliCut that's the ↺ takes group on 03-2: pick 2.
2. **01-2 at 0:39: "and the …criptions".** The start of "descriptions" sounds clipped in the recording.
   Listen; the caption now reads "descriptions".
3. **04-3 at 3:57: "building up the thumbnails, building up."** It trails off into a 3 s pause that is
   already cut. Kept as is.
4. **06-2 at 9:34: "That therefore, but I ended up generating…"** reads oddly but has no retake. Kept.
5. **Silent screen stretches.** I read words, not pictures. I didn't judge demo moments where you wait on screen.

## Caption spelling fixed (captions only; audio unchanged)

- OpenRig: "open rig", "open rigs" and "open re" (9 places)
- AppyRig: "Appy rig" and "Appy Rig" (3)
- Herdr: "Herder" and "Herta" (3)
- AppyDave: "appy dave"
- Skool: "skill community" and "school community"
- Claude Code, Codex: "cloud code Codex"
- Claude Code: "Claudine Code"
- image drip: "image trip"
- terminal multiplexer: "terminal multi placer"
- seat(s): "site(s)" (5)
- Ecamm Live: "ECamm Live" (your earlier fix had the capital C)

## Chapters (FliCut has no chapter verb, so these are not in the file yet)

```
0:00 Intro: a swarm of agents on your YouTube launch
1:05 The launch area in FliStudio
2:46 Setting up OpenRig and Herdr
4:10 Running the rig: handoffs, questions, thumbnails
8:31 The finished YouTube assets
10:20 What's next: OpenRig + AppyRig
```

- The CTA (0:50–1:05) is folded into the intro.
- The copy agent in the D11 launch team will write its own chapters from the exported SRT. These are a
  cross-check.

## Your part

1. Open FliCut on D11: `cd ~/dev/ad/flivideo/flicut && npm run app`. FliCut was stopped after the pass,
   so this gives you a window.
2. Play each row above at 2.5× and undo any you disagree with. Decide flag 1.
3. Export. That writes `videos/openrig-youtube-automation/` and unblocks the D11 launch team.

## What David changed (fill in after review)

- …
