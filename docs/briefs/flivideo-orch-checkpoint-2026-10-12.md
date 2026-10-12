---
title: "flivideo-orch checkpoint (2026-10-12, before /compact)"
created: 2026-10-12
timestamp: 2026-10-12
---

# Checkpoint: flivideo-orch — 2026-10-12

**Purpose**: Where the FliVideo orchestrator (tmux `flivideo-orch`, M4) is up to, for the post-compact session.

**For Agents**: Read first after `/compact`. Role: route David's FliVideo feedback to builders (background agents in
worktrees), merge + restart + verify, relay with `d10-ai-powered-video-cuts` (was d08-plan; same session, now on D10) and `lead@ylo-thumbs` (they tmux-send into `flivideo-orch`;
reply with `tmux send-keys -t d10-ai-powered-video-cuts -l '…'` then `Enter`). Standing rules: CLAUDE prefs + memory index.

## Current step
**Idle, all shipped.** Every FliVideo repo is clean and pushed; M4, Roamy and M2 are in step (2026-10-12 ~15:40).
Heads: flihub 18ecbe4 · flistudio ea4eae0 · flicut 1d612de · flitools ea26b38 · flivideo docs b2117e0 · plugins dc9e8cf.

## Done today (live)
- FliStudio: social posts (X/LinkedIn/Facebook pieces, group gate, verbs) · thumbnail pool gallery (#60) · one-yellow
  pass (#59) · staged files named `1-video…5-thumb-3` in `~/Library/Caches/flistudio/upload` (#62) · "Now post it" on
  Publish once Live (#63) · Discard cut (#56).
- FliHub: incoming order, chapter-move numbering, Renumber 1…N, tags after recording, rename-while-transcribing fix
  (e618df8), ↻ redo-transcript button (18ecbe4).
- FliTools: splice guard, force-redo, CrisperWhisper chunk-overlap repair + "text repeated" health check (ea26b38),
  live on M4 and M2 worker.
- FliCut: transcript warning (1b59bec) + "↻ reload transcript" per recording (e6197f1, verb `edit.reloadTranscript`).
  D10 03-6/03-7 reloaded (0 rewound words; 5 hand cuts in 03-6 41–50 s dropped — David re-cuts). Backup:
  `/Users/davidcruwys/dev/video-projects/v-appydave/d10-ai-powered-video-cuts/-trash/2026-10-12-before-reload/`.
- Docs: runbook `/Users/davidcruwys/dev/ad/flivideo/docs/runbooks/transcript-looks-wrong.md`; ylo
  `/Users/davidcruwys/dev/ad/appydave-plugins/ylo/references/social-posts.md`.
- D08 is LIVE: https://youtu.be/M978wEYFz1E. Social posts drafted, link filled; David posts by hand.

## In progress
- [ ] David's UAT of the FliCut reload on D10 (6 steps given in chat; he reports a failing step number).  ← YOU ARE HERE

## Pending (offer, don't start unasked)
- [ ] Runbook step 4 + ticket `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/flicut-reload-one-recording.md` still say
      FliCut can't reload one recording — update both (feature now exists).
- [ ] Offered: run the new transcript health check across D08–D10.
- [ ] UI notes not built (`/Users/davidcruwys/dev/ad/flivideo/docs/briefs/ui-notes-2026-10-11-d07.md`): #57 FliHub card
      wording, #58 end-screen swap/remove, #61 `resources.update` drops tags (batched).
- [ ] e2e drill fails at the 390px Publish-desk scroll-width check (on main too).
- [ ] D08 Launch gates: end screen (needs #58), social (David approves + ticks Posted).
- [ ] Cleanup: rig `ylo-thumbs` still up (David's/lead's — ask before `rig down`); stale worktrees
      `flistudio-worktrees/{pool,r1,social,stage-names}`, `flicut-worktrees/{reload-recording,reapply,reapply-home}`,
      `flitools-worktrees/chunk-overlap` (merged ones are safe to remove; check `reapply*` first — not ours today).
- [ ] Not investigated: FliHub `manage.test.ts` "delete-subfolder" flaked 1 in 9.

## Before starting the next step
- Check whether an app is open yourself (`ps aux | grep "[F]liCut.app/Contents/MacOS"`), never ask David.
- FliCut runs from the live checkout in dev mode: edits there hot-reload his window. Worktree until it's closed.
- FliStudio restart is ours (`npm run build -w shared` + `touch server/src/index.ts`, health on 7151). Never restart
  FliHub by hand (nodemon). FliTools: `scripts/app.sh restart`; M2 worker `scripts/deploy-worker.sh`.
- Roamy sync = pull, npm install, rebuild shared, restart, health-check 5101/7150/7151/7161.

## Ruled out this window
- Upload staging inside the project folder: David ruled it out (duplicates forever). Stays in Caches.
- "It's FliCut drawing twice": proven data — CrisperWhisper 30 s chunk overlap written twice (03-6, 03-7).
- Rename race / fold-splice as the duplication cause: ruled out by hashes (13 recordings, 13 distinct transcripts).
- Accepting a builder's "too big, ticketed" on a fix David asked for: wrong — send it back to build.
- Asking David whether FliCut is closed: check the process instead.
