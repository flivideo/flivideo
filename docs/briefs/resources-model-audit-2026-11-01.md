---
created: 2026-11-01
timestamp: 2026-11-01T12:00+07:00
---
# Brief: FliStudio "resources" — map the data model, propose one (2026-11-01)

**From:** `flivideo-orch` (Swagger). **To:** `resources-rsch` (tmux `resources-rsch`). **Report to `flivideo-orch` by name.**
**READ-ONLY on code and project data.** You write exactly two things: the doc below and (optionally) a spec page via
`dev-team:spec-page`. No code changes, no RPC writes, no edits under `~/dev/video-projects/`. Do not restart anything.

## David's words, verbatim (2026-11-01 ~11:55)

"With this particular screen where we've got the transcript for Joy, if we wanted to play it with audio, we probably
got tools like Kokoro. We can turn it into audio for us. But I don't know where we would put the resource if we
actually created it based on the transcript. Where would you suggest? Where are we thinking of resources, because
there's also a little bit of confusion, I believe? Between the fact that I've got resources showing up twice in the
menu on the left. That's something we should investigate. Plus resources that belong to different things, or at least
are managed by different things. You've got resources for B-roll, you've got resources for story capture, and you've
got resources in general … I don't know whether the data model has clarity."

Screenshots: `/private/tmp/claude-501/-Users-davidcruwys-dev-ad-brains/f73fd5e0-e8b2-40ea-a51a-c97dd7efe8db/images/11.png`
(D13 Story Pilot script) and `…/images/12.png` (left menu: `RESOURCES/ 0`, `SCRIPT/ 0`, … `RESOURCES 9`).

## What orch already saw (a lead, not a finding — verify)

- D13 = `/Users/davidcruwys/dev/video-projects/v-appydave/d13-overlay-pilot/`: has a `resources/` folder and
  `fli.resources.json`. Likely `RESOURCES/` (folder icon) = the folder on disk, `RESOURCES` (paperclip) = the attached
  records in `fli.resources.json`. Same word, two things. Sidebar code: `client/src/screens/ProjectHome.tsx` (~L818, ~L1015).

## Do

1. **Inventory every "resource-like" store** FliStudio and its extensions read or write: the `resources/` and `script/`
   folders, `fli.resources.json`, B-roll Pilot's pool/assets, Story Pilot's sources (`storypilot.story`), Overlay Pilot,
   captures/dossiers/sessions/artifacts linked from outside the project, `-renders`, trash, anything in `@flivideo/core`
   (`/Users/davidcruwys/dev/ad/flivideo/fli-core` or the pinned package). For each: where it lives, its shape, who writes
   it (app/extension/agent), who reads it, and what the UI calls it. Cite file:line.
2. **Explain the double "Resources" in the left menu** precisely (and `SCRIPT/` beside it).
3. **Answer the concrete case:** a Kokoro TTS read of D13's script (an audio file generated from the transcript). Where
   should the file live on disk, how does it get recorded so Story Pilot can find and play it, and how does it stay
   distinct from a real recording?
4. **Propose one clear model**: a small vocabulary (e.g. *files the project owns* vs *things attached by reference* vs
   *extension-owned working sets*), what each menu entry should be called, and the smallest set of changes to get
   there. Rank the changes; flag anything that touches the shared `fli-core` contract.

## Deliver

- `/Users/davidcruwys/dev/ad/flivideo/docs/specs/resources-model-2026-11-01.md`: inventory table, a mermaid diagram of
  the stores and who writes/reads them, the double-menu explanation, the Kokoro answer, the proposed model, ranked
  changes. Plain language first; David may not know the terms, so define them inline.
- Commit + push that doc in the flivideo repo (`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`).
- Report to `flivideo-orch`: the path, a 5-line summary, and every claim you could NOT verify.
