# D12 cut run: FliCut/FliStudio fixes + a new "render current edit" verb

**Purpose**: Brief for `flivideo-orch`. (1) The bugs and gaps the D12 agent-driven cut run hit; (2) one new FliCut
feature, API first, whose first real caller is the D12 thumbnail/title rig.

**For agents**: read in full. Part 2 (the render verb) is the blocker for a waiting job: build it first after the
filler fix. Finish with the `APPYNET: done` line in §4.

**From**: David, via the Roamy session, 2026-10-26.

**Status stamp (2026-10-26)**: nothing started.

## Sources (read these, don't take this brief's word for the details)

- Phase 0 API map and gap table: `/Users/davidcruwys/dev/ad/brains/video-editing-as-code/d12-cut-rig-phase0-2026-10-26.md` §6
- D12 runbook (what actually happened, with evidence files):
  `/Users/davidcruwys/dev/video-projects/v-appydave/d12-openrig-agent-teams/job/cut/runbook.md` (+ `evidence/`)
- D12 edit list (filler analysis, §F): `…/job/cut/edit-list.md`
- D11 precedent: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/d11-agent-edit-review-2026-10-15.md` ("Rogue-sound pass")

## Part 1: bugs and gaps (in priority order)

| # | Problem | Evidence | What "fixed" means |
|---|---|---|---|
| B1 | **Filler cuts remove nothing.** All 14 filler cuts on D12 removed ~0.05 s in total. The 0.15 s padding on the kept words either side swallows the "uh", so every "uh" is still audible. Same family as D11's "filler overlaps a kept pause" (pause wins, `removed: 0`). **Highest priority.** | runbook Step 3 result table; `evidence/cutlist-auto.json`; edit-list §F (measured "uh" spans vs cut spans) | A proposed filler cut removes the filler's measured sound. Padding never re-includes a filler. A regression test built from a real D12 filler (e.g. 01-1 @ 3.11–3.64) |
| B2 | **FliStudio `assets.list` returns takes in name order**: 06-10 sorts before 06-2. There is no "select all takes in recording order" verb; only the Start-a-cut screen sorts (by chapter, then segment), client-side | `flistudio/client/src/screens/ProjectHome.tsx:135-140`, `:1682-1714` | A server verb (or an `assets.list` option) that returns a project's takes in recording order, filtered the way Start-a-cut filters. The screen uses it too, so they can't drift |
| B3 | **`edit.start` starts FliCut itself** when it is down | `flistudio/server/src/launch/edit-start.ts:62-74` | An opt-out (e.g. `start:false` → refuse `flicut-down`). Default can stay as it is |
| B4 | **FliCut job state is in memory only.** A restart loses the "done" signal (`job-not-found`) | `flicut/src/main/control-surface.ts:192` (`#jobs = new Map`) | A job's final state survives a restart (or `job.get` answers from what's on disk). Your call how |
| B5 | **Two transcriptions race.** The window auto-transcribes an edit it opens; an agent's `edit.transcribe` then gets `transcription-running`. On D12 the window won, and the agent's job was redundant | runbook Step 3 "What actually happened"; `flicut/docs/AGENT-NOTES.md` | One of: `edit.transcribe` attaches to the running transcription and returns that job; or the hand-off can say "don't auto-transcribe". The caller gets one job to poll either way |
| B6 | **FliStudio's "ready" is a guess**: transcription seen to finish *or* 8 s with none seen | `flistudio/client/src/screens/StartEdit.tsx:420-440` | "Ready" comes from FliCut's real state (job or `/api/status`), never a timer |

Report back per row: fixed (commit) / deferred (why) / disagree (why).

## Part 2: new FliCut verb, "render the current edit" (API first)

**Who calls it:** agents. A UI button is optional.

**What it does:** renders the edit **as it stands now, every cut applied**, as **one** output covering all takes in
edit order (not one file per take). It is **not an export**: it doesn't write to `edits/` or `videos/`, doesn't
stamp the edit as exported, and doesn't touch whatever FliStudio uses to track exports.

**Outputs (one call):**
- **Audio: required.** MP3 or WAV (caller picks; one is enough).
- **Video MP4: optional**, a flag in the same call.
- **Transcript: required, in every format the real export produces** (SRT, TXT and whatever else export writes),
  **generated the same way export generates them.** The point is the export-grade transcript, not FliCut's stitched
  copy of the per-take transcripts, which is less accurate. If export re-transcribes the rendered audio, this does too.

**Rules:**
- **Read-only on the edit:** the edit file is unchanged and the undo history doesn't move. Prove it in a test
  (edit file hash and `edit.history` head are the same before and after).
- **Caller names the output location.** Your choice whether results come back as a stream or are written to a
  caller-given path. **State which you chose in your reply.**
- **Returns a job** to poll (`GET /api/jobs/<id>` like the others: `running | done | error`, `result` lists every
  file written). Mind B4: this is exactly the job a rig will poll.
- Reachable through the same seam as the other verbs (REST + `POST /api/rpc`), and listed in capabilities.

**First real caller:** the D12 thumbnail/title rig, on edit `openrig-agent-teams` in project
`d12-openrig-agent-teams` (brand `appydave`). Test it on that edit, read-only. **Do not change that edit**: David's
approved edit list is about to be applied to it by the `d12-cut-rig` session.

## Part 3: out of scope

- Exporting or publishing D12. Changing the D12 edit.
- Deleting, moving or archiving any take (never `dam archive --force`).

## Part 4: how to finish

Commit and push in the repos you change. End your report with one line naming the verb and endpoint:

`APPYNET: done — render verb <verb> at <METHOD path>; B1–B6: <one-word status each>`
