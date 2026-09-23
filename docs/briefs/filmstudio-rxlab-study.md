---
type: brief
title: FilmStudio (RxLab) — capability study
description: "Learn everything about FilmStudio (https://filmstudio.rxlab.app/): website capabilities first, then whether it can be downloaded and reverse-engineered, then where each capability would live in FliVideo (FliEdit? its own app?)."
created: 2026-09-23
timestamp: 2026-09-23
status: active
---

# FilmStudio (RxLab) — capability study

**Purpose**: David wants to understand FilmStudio completely and decide whether it is the model for
the missing **FliEdit** (Stage 3, after FliCut), a feature source for existing Fli apps, or something
to keep as its own thing.

**For Agents**: Run in window `filmstudio-rsch`. Work phase by phase. Phase 2's download needs David's
explicit go (it is untrusted code). Report to `flivideo-orch` via SendMessage at each phase end.

David's ask (2026-09-23, verbatim): *"I would like us to learn everything we can about this
application. I guess we should start with the website. We should read it and understand all its
capabilities. Then after that, we should consider whether we can download it and reverse engineer
it. I guess we need to find out all the capabilities and what they would look like. As features in
fly video and in particular, which application they would go into, it could be that this whole
application is just something we want on its own. Maybe it's the new fly edit, maybe it's something
else I don't really know."*

## Precedent — reuse the method, don't reinvent it

Screen Studio was reverse-engineered on 2026-09-10:
- brain: `/Users/davidcruwys/dev/ad/brains/screen-studio/` (read its INDEX.md first — shape to copy)
- study tree: `/Users/davidcruwys/dev/upstream/repos/screenstudio-study/` (local-only, `.gitignore` = `*`)
- The finding that mattered: *where compute happens* (local vs server) decides whether it is
  automatable and replicable. Answer that question for FilmStudio too.

FliVideo context: suite map `/Users/davidcruwys/dev/ad/flivideo/README.md` (4 stages; FliEdit
"brings everything together with overlays", missing). Latest end-to-end run:
`/Users/davidcruwys/dev/video-projects/v-appydave/d04-flivideo-autopilot/-run/run-report.md`.

## Phase 1 — the website (no download)
Read https://filmstudio.rxlab.app/ and every page it links (docs, features, pricing, changelog,
FAQ, blog, GitHub/releases if any). Also search for independent sources (reviews, forums, videos).
Output: a capability inventory — every feature, one row each: what it does · UI/automation surface
(CLI? scripting? API? plugins? file formats?) · platform · local vs cloud · price tier · source URL.
Mark claims that only marketing makes.

## Phase 2 — can we download and reverse-engineer it? (assess, then ASK)
Determine: platforms, how it's distributed (dmg / app store / web app / open source?), licence and
EULA terms on reverse engineering, trial limits, tech stack signals (Electron? Qt? native? web?).
STOP and message flivideo-orch with a recommendation + exactly what would be downloaded (file,
source, size) before downloading anything. If it is a web app, reading its shipped JS in the browser
is phase 1 work, not a download.

## Phase 3 — map to FliVideo
For every capability: which Fli app it belongs in (FliStudio / FliHub / FliCast / FliCut /
Teletubby / FliTools / FliEdit-to-be / new app / not wanted), what it would look like as an
agent-drivable capability there, and effort. Then the verdict David asked for: is FilmStudio the
model for FliEdit, a feature donor, or its own thing — with the reasoning.

## Deliverables
- Brain: `/Users/davidcruwys/dev/ad/brains/filmstudio/` (INDEX.md + capability inventory + tech
  notes + FliVideo mapping), following `/Users/davidcruwys/dev/ad/brains/brain-creation-guide.md`.
- Study tree (only if phase 2 is approved): `/Users/davidcruwys/dev/upstream/repos/filmstudio-study/`,
  local-only like the Screen Studio one.
- A short summary back to flivideo-orch: verdict + top 5 capabilities worth having + where they go.

## Out of scope
Building anything in any Fli repo. Buying a licence. Installing or running the app without David's go.
