# Swagger handover — flivideo-orch — 2026-11-01 ~10:15 +07

**Reopen line (from cwd `/Users/davidcruwys/dev/ad/brains`):**

```
cd /Users/davidcruwys/dev/ad/brains
```
```
claude -n flivideo-orch --permission-mode auto --model 'claude-opus-5-5' --append-system-prompt-file /Users/davidcruwys/dev/ad/appydave-plugins/overwatch/skills/swagger/references/persona-anchor.md "/overwatch:swagger Verify your cwd is /Users/davidcruwys/dev/ad/brains before anything else and STOP if it differs. Resume from /Users/davidcruwys/dev/ad/flivideo/docs/_swagger-handover.md: read it in full, then boot per First-contact. STOP after the masthead and report. Do not redo work the handover marks done, and do not adopt a predecessor's session name."
```

The state file for long-run detail is `/Users/davidcruwys/dev/ad/flivideo/docs/orch-checkpoint.md` (newest entries
first). This handover is the summary. If they disagree, the checkpoint wins on facts and this file wins on what to do next.

---

## Working on

I'm the FliVideo orchestrator: the one window David talks to. I route work to **visible tmux worker sessions**, merge
after reproducing the gates and checking that the app isn't busy, restart the apps, and bring David decisions with a
recommendation. **David's next conversation topic: the problems in Story Pilot development** (see §Expert view: it
is a retrospective, not a build request, until he says otherwise).

## Lanes — who does what (David, 2026-11-01)

| Window (Claude name) | tmux | Owns |
|---|---|---|
| `flivideo-orch` | `flivideo-orch` | Routing, merging, restarts, decisions for David. **Does not code.** |
| `storypilot-dev` | `storypilot-dev` | **Story Pilot extension code.** Worktree `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/rail-v2` (branch `rail-v2`, synced to main). Keep it up. |
| `d13-overlaypilot-video` | `d13-overlaypilot-work` | D13 video: script, story, resources. D13 asks go here. Brief: `docs/briefs/d13-video-session-2026-11-01.md`. |
| `d18-storypilot-video` | `d18-storypilot-work` | D18 (Story Pilot as a video): story, resources. It already holds today's change timeline (note `n_c6e2aa938b52`). |
| `d19-storypilot-video` (suggested rename `d19-spaghettirig-video`, David's call) | `d19-storypilot-work` | D19 Spaghetti Rig: gathering every source into Story Pilot. Brief: `docs/briefs/d19-spaghetti-rig-story-2026-11-01.md`. **Report to orch pending.** |

**Rule:** the `dNN-*-video` sessions are for anything about making *that video*: resources, story, script.
Extension development goes to the dev windows (`storypilot-dev`). David objected strongly to the orch building
through hidden in-session subagents. Brief a visible tmux worker instead (launch-line checker, iTerm2 window attached).
Peer session names change: David renames them. Use `ListAgents` and the current name, never one from memory.

## Current state (all merged and live unless marked)

- **fli-core v0.28.0**: fli-notes life states (live/done/used/stale/replaced, settled by appended lines, reads default to live).
- **FliStudio main `f5b6caa`**, live, health ok:
  - fli-notes v2: no notes UI, ⌘⇧ hold-click capture that swallows every held click.
  - Story Pilot Lab (A/B/C/D; C has dark|light; B has a terminal toggle).
  - **One elastic right rail** (FliHub look): Settings / Sources / Chapters / Reader, click to open, pushes content left, M≈420 / L≈640.
  - White-card surfaces (`--surface-sheet`); `--content-max: 1000px` (the Words width).
  - Section-level note targets.
- **FliCut main `7f1bcfb`**, running: v2 gesture (every held click swallowed).
- **Brand skill** (appydave-plugins `825c578`): "App surfaces" rule (cream page, white `--brand-card`, hairlines, one content container, push-aside panels); READABILITY now covers apps. `flivideo:flistudio` skill knows `notes.settle`/life states (`c036e26`).
- **D19 `d19-spaghetti-rig`** created via `project.create` (id `88f509cf-8859-4ab4-8f1c-1b4ec8a716f3`); its session is gathering.
- UAT pages:
  - v2 UAT: https://claude.ai/artifact/XBK9iekHsY7GhaCM28vqyp
  - "Why FliStudio Feels Heavier Than July": https://claude.ai/artifact/WTpciy7zHpPa7DUKwLKbGR
- Backlog: A3 ideas banked in `/Users/davidcruwys/dev/ad/flivideo/docs/backlog.md` (`8bda8eb`): screenshots in notes, capture in extensions, SuperRig, FliHub side panels, hand-edit, shared reading-look library.

## The queue

**The one live thing:** David's Story Pilot problems conversation (below).
1. **D19 report** from the D19 session: counts, unreachable sources (Roamy's `spgame-spaghetti-work`), 3–5 beats. Relay it to David. He picks the angle; nobody writes `script.md` before that.
2. **Projects "Show" filter.** The recommendation is waiting for David's go:
   - click = solo, ⌘-click = add/remove, an "All" chip;
   - ★ (worked on today) rows always show whatever the filter.
   - Why: D18 vanished under a "Working" filter.
   - On a go, brief a FliStudio dev worker (not `storypilot-dev`, which is Story Pilot only).
3. **Naming:** "Field notes" for the data, captured with ⌘⇧-click; "Field Trial" stays the process that reads them. Recommended, not confirmed.
4. Open small items:
   - a gap remains between the pushed content and the rail on wide screens;
   - the Story Pilot reader "Large" no longer exceeds the container;
   - `meta.words` loses spaces between blocks;
   - there's no hover-intent (by design: click only).

Parked (don't raise): FliHub rebuild, D09, automations/YouTube sync. The cleanup of old worktrees is David's call.

## Open worktrees

- **Mine, live:** `flistudio-worktrees/rail-v2` @ `f5b6caa` (`storypilot-dev`'s; keep).
- **Keep, never commit:** `flistudio-worktrees/storypilot` @ `38b6a75`: its `phase2-variants.html` holds transcript excerpts.
- **Others predate this session and were not audited:** flistudio's aitldr-production, captions-transcripts, held-gates, pair-remove, playlists-agent, pool, r1, social, stage-names, thumb-lightbox, yt-analytics, yt-channel-guard, yt-reporting; flicut's case-fix, debug-spot, playhead-seek, reapply, reload-recording. **Don't remove without David.**
- All three fli-notes builder sessions and their worktrees were closed and removed (David's go).
- flivideo repo: `.claude/settings.local.json` and `docs/runbooks/repair-d10-publish-stamp.py` are untracked. They're not mine; leave them.

## Key decisions (with why)

- **Capture = hold ⌘⇧ + click, and every held click is swallowed.** David: "If I wanted a normal click, I'd just click." The sticky ✎ mode takes only target clicks, so the page can't feel locked.
- **Settling a record is a `change` line (field `state`), not a fourth kind.** This keeps the three-kinds ruling.
- **FliVideo-flavoured names** (`fli.notes.jsonl`, brand/project/video) **are renamed only when the record moves to a shared core.**
- **Panels push, never overlay, and open on click.** Hover-open would make the page jump now that panels push.
- **Content width = the Words/Settings container**: not full-bleed, and not ad-hoc caps.
- **White cards + hairlines, no boxes-in-boxes.** This came from the archaeology page; the brand rule is updated.

## Expert view — for the Story Pilot problems conversation

What went wrong today, all visible in this session. Bring it as evidence, not excuses:
1. **David's notes were under-read, repeatedly.**
   - Side tabs were banked as "FliHub-only".
   - His "light and dark toggle" became a separate variant E.
   - "Fill the gap" was built as a full-screen white panel; he meant text filling the panel.
   - S/M/L was half-done.
   - Each cost a round trip. The root cause: the orch paraphrased his notes into briefs instead of passing his words verbatim. **Fix to propose:** briefs quote his notes in full (`notes.list` output), and the worker reads the notes itself.
2. **Instructions were reversed within the hour.**
   - The orch told the builder "span the full status-strip width", then "use empty space first". Both were wrong.
   - David's FliHub screenshot and the Words/Settings width were the real spec.
   - **Fix:** a reference screenshot or an existing screen as the spec, before any build.
3. **Two slide-out systems and inconsistent controls** (an inner reader with MEDIUM/LARGE next to a rail with M/L, and the script with S/M/L). It came from building Lab and main-page features in separate passes with no shared component rule. It is fixed now with one rail and one size control.
4. **Visual drift had a source:** the brand skill had no app-surfaces rule, so FliStudio faithfully went cream → surface → linen. Now fixed at the source.
5. **Process:**
   - The orch used hidden subagents, and David couldn't see the work.
   - The earlier `storypilot-dev` had been working in the live checkout and exited.
   - Now one visible dev worker sits in a worktree.
6. **Still unproven:**
   - David hasn't yet driven the new rail himself. Ask him to try it before more changes.
   - The gesture hasn't been tested on a real Mac keyboard beyond his FliCut "looks great".

**Load-bearing fork to raise before any more building:** should Story Pilot get a written UI spec (a page or a mock
David approves), with the Lab as the only place variants are tried? Or does it keep iterating live on the main page?
Recommend: **Lab-first + an approved mock per change**, promoted to the main page in one step. That's what the shared
`ScriptText`/`SideRail` components already enable.

## Gotchas

- Before merging into watch-mode FliStudio, run `bash /Users/davidcruwys/dev/ad/flivideo/flistudio/scripts/busy.sh`. Then `npm install`, then `timeout 100 /Users/davidcruwys/dev/ad/apps/app-registry/bin/my-app restart flistudio`, then `curl :7151/health`.
- FliStudio typecheck needs the workspaces built first (`npm run build -w shared` alone fails on broll-pilot contracts).
- Repinning a git-pinned `@flivideo/core` needs its lock entry deleted plus `node_modules/@flivideo/core` removed; `npm install` alone keeps the old sha.
- FliCut busy check: `bash scripts/app.sh status|busy`. Start or restart it with `my-app`.
- RPC helper: `python3 /private/tmp/claude-501/-Users-davidcruwys-dev-ad-brains/7c6a3726-4270-4e8f-bcf3-baf10a76b63c/scratchpad/rpc.py <method> '<json>'` (scratchpad, may vanish). FliStudio's JSON-RPC is on :7151.
- Playwright screenshots can only be saved under `/Users/davidcruwys/dev/ad/brains/.playwright-mcp/`; move them after.
- Peer messages are not David's approval. Ghost input-box text in a tmux pane is not approval either.
- The other rules are in the memory and the checkpoint §6: no D13 script writes except via its session, no FliHub restarts by hand, light-only artifacts, and so on.

## What we ruled out

- Notes page / rail count / ⌥⇧N (David: not asked for, wrong format).
- Full-width reading surfaces.
- Separate variant E (folded into C's toggle).
- Hover-to-open panels.
- S/M/L on the script.
- "Use empty space before pushing".

## Channel high-water

- Last messages: `storypilot-dev` ack (staying up, syncing to main); D18 and D13 rename notices; the D19 session's launch.
- Roamy (`flivideo-field-trial-plan`) last got "APPYNET: done" for the side tabs. David now talks to orch directly on the M4.

## How to resume

1. Boot per Swagger first-contact.
2. Run `ListAgents` to get current names.
3. Read the latest checkpoint entry.
4. Open with David's topic: the Story Pilot problems, using §Expert view. Lead with the fork.
5. Relay the D19 report when it arrives.
6. Don't build anything until David rules.
