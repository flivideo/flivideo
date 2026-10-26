# FliCut restart safety: busy guard, reopen, remembered skips, engine-change review

**Purpose**: Feature request for `flivideo-orch` from the D12 overnight run (2026-10-26). Restarting FliCut lost no
edits, but it killed a render, came back with nothing open, and new code silently re-applied cuts David had skipped.

**For agents**: read in full; R1–R4 are build requests, R5 is a question to answer, R6 is a check. Finish with the
`APPYNET: done` line in §5.

**From**: David, via the Roamy session, 2026-10-27.

**Status stamp (2026-10-27)**: nothing started.

## 1. What happened (evidence)

- FliCut was restarted three times in 12 minutes on 26 Oct (21:50 Roamy, 21:59 and 22:02 flivideo-orch after a bare
  "Restart" from David that may have meant the Claude update). Source:
  `/Users/davidcruwys/dev/video-projects/v-appydave/d12-openrig-agent-teams/job/thumbs/friction.md` (rows 22:02, 22:36).
- **Edits survived.** History 000040 → 000146 is intact. Per `src/renderer/src/store.ts`, every edit commits a history
  snapshot at once; drags are merged and flushed after `MERGE_MS = 800`; view state saves after 300 ms; a graceful quit
  saves before closing.
- **What was lost or changed:**
  1. Render job `62e1f45462dbb54a` was killed mid-run (`interrupted: FliCut restarted while this job ran`). B4 worked:
     the record survived. The work did not.
  2. After the restart FliCut's open context was `null`; flivideo-orch reopened `appydave / d12-openrig-agent-teams` by hand.
  3. B1 (`ebae9bb`) re-applied six proposed filler cuts David had chosen to **skip** (F2, F4, F8–F11 in
     `…/job/cut/edit-list.md`) on the next save. A skip is stored as "left as proposed", not as a dismissal.
- **Root cause:** live FliCut runs from its main code folder, so a merge reaches the running app and its open edit.

## 2. Requests

| # | Request | Done means |
|---|---|---|
| R1 | **Busy guard before restart.** FliCut reports `busy` (running render/transcribe/export job, pending merged save) in `/api/status`. `npm run app:restart` and `my-app restart flicut` refuse while busy and print what is running, unless `--force`. | A restart during a render is refused with the job id; `--force` still works |
| R2 | **Reopen after restart.** FliCut reopens the last open project/edit. Interrupted jobs can be re-queued with one call (or resume themselves). | After a restart, `GET /api/status` shows the same context; an interrupted render can be re-run without re-sending its body |
| R3 | **A skip is remembered.** Rejecting or skipping a proposed cut is stored as a dismissal (`by: user`), and no later re-propose or engine fix brings it back. | Test: dismiss a proposed filler, re-propose with B1 maths, the filler stays kept |
| R4 | **Engine changes don't silently rewrite an open edit.** Proposed cuts record the engine version that made them. When the maths changes, FliCut shows a "proposals changed" diff and waits for a human/agent to accept before saving them. | Test: load an edit made by older maths, nothing changes until accepted |
| R5 | **Question, don't build:** should live FliCut run from a release folder or worktree, promoted on purpose, instead of main? Give the trade-offs and your recommendation. | A short answer in your report |
| R6 | **Check:** `ControlSurface.flushJobRecords()` exists (`src/main/control-surface.ts:1092`) but I couldn't see it called on the quit path (`src/main/index.ts`, `quit-guards.ts`). Confirm or wire it. | Answer plus fix if needed |

Also from the D12 report, fix or file:
- **Two lengths for one edit:** `edit.get` says kept 1150.95 s (19:11); `edit.render` makes 1174.76 s (19:35),
  `plannedDuration` the same. ~0.6 s per take, probably edge padding counted as removed. They must agree, or `edit.get`
  must say what it excludes.
- **Stale `.part.mp4`** left by the killed render in
  `…/job/thumbs/render/.openrig-agent-teams-render.render-ac244a78/`: clean up on restart or report it.

## 3. Don't

- Don't change the D12 edit `openrig-agent-teams`. Don't restore the six skipped "uh"s: David decides that after listening.
- Don't restart FliCut without telling David it reloads his window (and, once R1 exists, check busy first).

## 4. Out of scope

Exporting or publishing D12 · deleting or archiving takes (never `dam archive --force`).

## 5. How to finish

Commit and push. End with:
`APPYNET: done — R1–R4: <status each>; R5: <one-line answer>; R6: <status>; length gap: <status>`
