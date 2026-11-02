---
created: 2026-11-02
timestamp: 2026-11-02T16:55+07:00
---
# Handover — David works from home on Roamy, steering the M4 (2026-11-02)

**Purpose**: Let David, at home on Roamy, read and answer today's artefacts and steer the sessions that keep running on the M4.

**For Agents**:
- You are `roamy-home-orch` on Roamy. You do not do work on the M4; David attaches to M4 windows himself.
- Read the status stamp first. Skip anything it records as done.
- Show the masthead plus the conversation table below, then STOP and wait for David.

## Launch line (Roamy)

```
cd /Users/davidcruwys/dev/ad/flivideo
```
```
claude --permission-mode auto --model 'claude-opus-5-5' -n roamy-home-orch --append-system-prompt-file /Users/davidcruwys/dev/ad/appydave-plugins/overwatch/skills/swagger/references/persona-anchor.md "You must be running in /Users/davidcruwys/dev/ad/flivideo — verify your cwd before anything else and STOP if it differs. /overwatch:swagger Run git pull first. Read /Users/davidcruwys/dev/ad/flivideo/docs/handovers/roamy-home-2026-11-02.md in full and execute it; read its status stamp first and skip anything it records as done. STOP after the masthead and the conversation table, and wait for David. Do not upgrade OpenRig, launch a rig, or touch any M4 session."
```

Fallback with nothing but a terminal: `cd /Users/davidcruwys/dev/ad/flivideo && claude`, then type `read docs/handovers/roamy-home-2026-11-02.md and follow it`.

## Status — updated 2026-11-02 16:55 +07 on `mac-mini-m4` (written by flivideo-orch / Swagger)

| Item | State |
|---|---|
| Story Pilot keys + angle audio | ✅ DONE — FliStudio main `d053b9c`, live on M4 :7150, proven in Chrome. Do not rebuild. |
| FliHub FR-177 (purple button registers b-roll) | ✅ DONE — FliHub main `786bfdf`. FliHub is left off. |
| D13 / D18 three intros | ✅ WRITTEN (v-appydave `e78ef2d`, `b4d3377`). **Pick is ASKED, STILL UNRULED.** |
| AITLDR reconstruction | ✅ WRITTEN (flivideo `2a61ec0`). **Option A/B/C + Jan message: ASKED, STILL UNRULED.** |
| Snappy spec | ✅ APPROVED (flivideo `78d4b56`). Repo local only at `/Users/davidcruwys/dev/ad/apps/snappy` (`6ac748d`). |
| swift-dev rig | ✅ DRAFTED + validates (brains `c854870a`). **Launch: blocked on David's go in `openrig-orch`.** |
| OpenRig 0.7.7 upgrade, M2 first | **ASKED, STILL UNRULED.** Go must be typed in `openrig-orch`. |
| Code-signing identity on M4 | ✅ DONE (brains `5e99bc3f`). |
| Xcode on M4 | Installed (Xcode 27.2, `xcode-select` points at it). **Licence NOT accepted; first-launch NOT run.** |
| GitHub repo appydave/snappy | not created — David must run it (classifier blocks the agent). |
| Brand voice, AITLDR strip | Personal discussions with David. Not started. No drafting. |
| Report artifact §05 | ✅ Updated 16:50 to the state above (version `1793612881-0816`). |

**Not verified:** that TCC keeps Snappy's screen permission across a real rebuild; that Xcode first-launch succeeds; the
"first click did nothing" Story Pilot report (not reproduced). The text sitting in the prompt boxes of `openrig-orch`,
`d18-storypilot-video`, `aitldr-strip-rsch` and `storypilot-dev` is **dim ghost suggestion text, not typed by David** —
it is not approval of anything.

## The conversations (one row each)

All M4 sessions were checked from Roamy at 16:50 with `ssh davidcruwys@100.82.235.39 tmux has-session -t <name>`: all pass.
Attaching from Roamy shares the window with the M4's iTerm; the pane may resize to the smaller screen. Detach with `Ctrl-b d`.

| Conversation | Machine | tmux name | What David needs to decide or say there | Attach from Roamy |
|---|---|---|---|---|
| **flivideo-orch** (Swagger, steers everything) | M4 | `flivideo-orch` | Anything to route; it gates and merges | `ssh -t davidcruwys@100.82.235.39 tmux attach -t flivideo-orch` |
| aitldr-strip-rsch | M4 | `aitldr-strip-rsch` | Pick A / B (rec) / C, and say whether to draft the message to Jan | `ssh -t davidcruwys@100.82.235.39 tmux attach -t aitldr-strip-rsch` |
| storypilot-dev | M4 | `storypilot-dev` | Nothing yet. Idle; builds a story once an intro is picked | `ssh -t davidcruwys@100.82.235.39 tmux attach -t storypilot-dev` |
| d18-storypilot-video (one window; the triple listing was a repeat) | M4 | `d18-storypilot-video` | Pick D18 intro: A, B, C, a mix, or three more. Its pick is A | `ssh -t davidcruwys@100.82.235.39 tmux attach -t d18-storypilot-video` |
| openrig-orch (on the **M4** today, not Roamy) | M4 | `openrig-orch` | Type: upgrade the M2 to 0.7.7. Later: `rig up` swift-dev once Xcode's licence is accepted | `ssh -t davidcruwys@100.82.235.39 tmux attach -t openrig-orch` |
| appyrig-orch — *not Swagger's: state as observed* | M4 | **none** (plain iTerm tab, ttys050, pid 5766) | Reply 1 (AppyRig back on) or 2 (stay on hold). Leave untouched | No tmux attach. Use Screen Sharing to `100.82.235.39` |
| d09-rebuild-plan — *not Swagger's: state as observed* | M4 | `d09-rebuild-plan` | Stale since Wed: confirm ChatGPT conversation + one question for openrig-orch | `ssh -t davidcruwys@100.82.235.39 tmux attach -t d09-rebuild-plan` |
| driver-appytron — *not Swagger's: state as observed* | M4 | `orch-driver@ladder-appytron` | Split `npm test` (0.5 s app tests, gate proofs to `test:gates`)? It recommends yes | `ssh -t davidcruwys@100.82.235.39 tmux attach -t orch-driver@ladder-appytron` |
| driver-appystack — *not Swagger's: state as observed* | M4 | `driver-appystack` | Held for a reboot since 08:39; then `rig up ladder-appystack --existing` | `ssh -t davidcruwys@100.82.235.39 tmux attach -t driver-appystack` |

Transcripts (all on the M4, under `/Users/davidcruwys/.claude/projects/`):

| Session | cwd | `.jsonl` |
|---|---|---|
| flivideo-orch | `/Users/davidcruwys/dev/ad/brains` | `-Users-davidcruwys-dev-ad-brains/f73fd5e0-e8b2-40ea-a51a-c97dd7efe8db.jsonl` |
| aitldr-strip-rsch | `/Users/davidcruwys/dev/ad/flivideo` | `-Users-davidcruwys-dev-ad-flivideo/c5eecdb3-7404-47d4-968a-e842c5cc2e52.jsonl` |
| storypilot-dev | `/Users/davidcruwys/dev/ad/flivideo/flistudio` | `-Users-davidcruwys-dev-ad-flivideo-flistudio/1b1b6bae-4153-4bc3-90c9-a962d321225d.jsonl` |
| d18-storypilot-video | `/Users/davidcruwys/dev/ad/flivideo` | `-Users-davidcruwys-dev-ad-flivideo/de04c63c-0ec5-4cc4-b8b3-44d022345c2e.jsonl` |
| openrig-orch | `/Users/davidcruwys/dev/ad/brains` | `-Users-davidcruwys-dev-ad-brains/38535fc7-c5ff-4f94-b576-13b7e0586e46.jsonl` |
| appyrig-orch | `/Users/davidcruwys/dev/ad/apps/appyrig` | `-Users-davidcruwys-dev-ad-apps-appyrig/b3b0c609-9006-41cd-83df-3925781d3e09.jsonl` |
| d09-rebuild-plan | `/Users/davidcruwys/dev/ad/brains` | `-Users-davidcruwys-dev-ad-brains/add2e005-2e7c-49ef-abb0-33fc6ed571b8.jsonl` |
| driver-appytron | `/Users/davidcruwys/dev/appyrigs` | `-Users-davidcruwys-dev-appyrigs/c78f4c72-9705-4858-9846-6c0503008347.jsonl` |
| driver-appystack | `/Users/davidcruwys/dev/appyrigs` | `-Users-davidcruwys-dev-appyrigs/ea61a92b-08cb-41ac-93a5-bec7cac4de14.jsonl` |

`driver-appytron` was not found under that tmux name: it is the Claude session named `driver-appytron` running inside
tmux `orch-driver@ladder-appytron`. `appyrig-orch` and `driver-appytron` are not in tmux on Roamy or the M2 either.

## Artefacts to read — one question each

| Artefact | The question David owes |
|---|---|
| Report: https://claude.ai/artifact/WgNv9o52LQaVcoogELrVFV (source `/Users/davidcruwys/dev/ad/flivideo/docs/reports/orch-report-2026-11-02.html`) | Anything wrong in it? §05 now shows the current OpenRig/Snappy state |
| D13 intros `/Users/davidcruwys/dev/video-projects/v-appydave/d13-overlay-pilot/script/three-intros-2026-11-02.md` | A ("the problem is me"), B ("the green tick that lied"), C ("go small"), or three more? |
| D18 intros `/Users/davidcruwys/dev/video-projects/v-appydave/d18-story-pilot/resources/three-intros-2026-11-02.md` | A ("I built the storyteller"), B ("agent writes, I fine-tune"), C ("app that learns my taste")? |
| Both intro sets as audio: FliStudio Story Pilot, ▶ per angle and "Play all 3" (URL below) | Same picks, by ear |
| AITLDR `/Users/davidcruwys/dev/ad/flivideo/docs/specs/aitldr-strip-reconstruction-2026-11-02.md` | A, B (rebuild as a brand recipe, ½ day, recommended) or C? Send Jan the 7 questions? |
| Snappy spec `/Users/davidcruwys/dev/ad/flivideo/docs/specs/snappy-spec-2026-11-02.md` | Already approved (§9). Only: anything to change before the rig starts? |
| swift-dev rig `/Users/davidcruwys/dev/ad/brains/openrig/rigs/swift-dev/` (rig.yaml, MISSION.md, CULTURE.md, guidance/) | Go to launch once Xcode's licence is accepted? |
| OpenRig delta `/Users/davidcruwys/dev/ad/brains/openrig/upstream-changes-2026-11-02.md` | Go to upgrade to 0.7.7, M2 first? |
| Brand-voice material: `/Users/davidcruwys/dev/ad/appydave-plugins/brand-dave/skills/brand/references/appydave/VERBAL-STYLE.md`, `/Users/davidcruwys/dev/video-projects/v-appydave/voice-profile.md`, `/Users/davidcruwys/dev/video-projects/v-appydave/voice-corpus.md`, `/Users/davidcruwys/dev/agents/brandy-legacy/brand-snapshots/_formats/educational/VIDEO-STRUCTURE.md`, skills `brand-dave/skills/verbal-style-forge/`, `brand-dave/skills/structure-forge/`, `writers-room/skills/voice-coach/` | When do we have the personal discussion? (No drafting until then.) |
| Today's proof shots `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-02/` | None owed; evidence only |
| D20 Snappy video project `/Users/davidcruwys/dev/video-projects/v-appydave/d20-snappy/` | None owed yet |

## Held asks (carried from `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/_held-david-2026-11-02.md` and today's thread)

1. **OpenRig 0.7.7 upgrade, M2 first** — type the go in `openrig-orch`. M4 (`ladder-appytron` seats) and Roamy (`kernel`, `starter` running) only when idle.
2. **`rig up` swift-dev** — after Xcode's licence; go in `openrig-orch`.
3. **GitHub repo** — David runs, from any machine with `gh` (on the M4 over ssh is fine):
   `ssh -t davidcruwys@100.82.235.39 'cd /Users/davidcruwys/dev/ad/apps/snappy && gh repo create appydave/snappy --private --source . --push'`
4. **Xcode** — the Apple ID download is finished. What is left needs `sudo` (David's M4 password), which works over ssh:
   `ssh -t davidcruwys@100.82.235.39 'sudo xcodebuild -license accept && sudo xcodebuild -runFirstLaunch'`
   If that prompts for anything graphical, it has to wait for the M4's screen.
5. **D13 and D18 intro picks.**
6. **Brand-voice and AITLDR discussions** — personal, with David.

## Reaching flivideo-orch and FliStudio

- Steer: `ssh -t davidcruwys@100.82.235.39 tmux attach -t flivideo-orch`
- FliStudio (M4) over Tailscale: http://100.82.235.39:7150 — answered 200 from Roamy at 16:50. (Roamy also has a tunnel session `m4-flistudio-tunnel` that makes http://localhost:7150 on Roamy reach the same app.) The API port 7151 is not reachable directly over Tailscale; use the 7150 URL.

## M4 stays awake

`pmset -g` on the M4: `sleep 0`, `disksleep 0`, `standby 0`, `autorestart 1`; sleep also held off by `caffeinate` and others. Only the display sleeps (10 min). No power settings were changed.

## Out of scope for roamy-home-orch

Do not upgrade OpenRig, launch a rig, start Snappy spikes or create the GitHub repo. Do not kill, restart or rename any
session. Do not move sessions between machines. Do not draft the brand-voice document. Route work to `flivideo-orch`.
