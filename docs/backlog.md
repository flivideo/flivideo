# FliVideo suite backlog

Banked ideas and jobs, not active work. **Nothing here gets built without David's go.** Each entry says where it came
from and what it depends on. App-specific backlogs stay in each app's own `docs/backlog.md`. This file is for work that
crosses apps.

## Waiting for David to guide (not a go)

David, 2026-10-31 20:47 +07: "I have no idea about the automation spec page or the YouTube daily sync... they should be
put onto a backlog because I'm not there to guide that."

### Automations: "you've recorded, want me to cut it?"
- **Idea:** status changes trigger an offer of the next step.

  | When | Offer |
  |---|---|
  | Recorded | cut it |
  | Cut | export |
  | Exported | make final |
  | Final | draft the launch |
  | Published | social posts |

- **Permissions:** each step is off, ask me, or do it and tell me. The default is ask me.
- **Where the offer appears:** a "next" button on the FliStudio project row, and/or an agent message in Buzz, with
  voice later.
- **Where each part lives:**
  - signals: the fli-core facts log;
  - the next-step map and permissions: FliStudio;
  - the actual work: the existing apps agents can already drive.
- **Depends on:** the Project Status facts follow-up,
  `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/project-status-facts-fli-core-2026-10-31.md`.
- **Needs from FliHub:** a "takes added" event, and an optional "Done recording" button.
- **Orch's suggested first slice:** "Recorded → offer to cut", because outro detection already exists.

### YouTube daily sync
- **What exists:** FliStudio has `youtube.sync`, but it is manual and read-only (API key, public videos only). The local
  copy of the YouTube list is stale since 2026-10-15.
- **Idea:**
  - run the sync daily, after an upload, and on "mark published";
  - tick the Published box automatically when a YouTube video matches a project;
  - flag videos that are on YouTube but not linked to any project.
- **Open question:** seeing private, unlisted or scheduled videos would need the YouTube sign-in that uploads already
  use. Read-only public access is the safe default.

### Ecosystem research: 21 decisions (2026-11-03, B686/B687)
- **What it is:** the finished research on where FliVideo is going: apps vs pilots, the 80-20 rule, which outside
  tools to absorb, add or replace. Index: `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/00-index.md`.
  Map: https://claude.ai/artifact/FikDp9d9cn3MzQmo3zpqq6
- **The decisions:** `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/06-approval-register.md`, rows
  R1–R21, all open. Only David changes a row.
- **When to pick it up:** the main chain is **R1 → R3 → R4** (what 80-20 means → is Overlay Pilot's renderer an app →
  FliMotion). It waits until David has finished testing the pilots.
- **Can be done any time:** R13 (licence posture: run AGPL tools unmodified, never copy their code) is one ruling;
  X2 (is HyperFrames' studio server safe to embed?) is a ~1 h read-only check on the M2.
- **Experiments:** X1–X9 in `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/05-research-experiments.md`,
  each needs its own go (R21).
- **Repos it studied:** 8 clones registered in `~/dev/upstream/repos.jsonl`, downloaded on the M2 only.
- **Trial plan (2026-11-03):** how to run the useful ones on the M4 against d01-flivideo-tour, in order (auto-editor → Textream → HyperFrames X2/X1 → video-use → FliStudio seam → Immich on M2): `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/08-trial-plan-on-m4.md`.

## Banked (backlog only)

- **Pilots:**
  - Publishing Pilot (refactor)
  - Audio Pilot
  - Timeline Pilot (also called Director's Chair: placement, timing, Ken Burns)
  - Motion Pilot (planned, project d16)
  - *Source:* B676/B677.
- **Video groups:** series- or tag-based collections; a document attached virtually to many groups. *Source:* B677 D9.
- **Per-brand status recipes:** the status boxes come from a brand's configured step list, not a fixed 8. Each app or
  Pilot declares its box. For example, AITLDR has "AI voice" instead of "David narrated". *Source:* David 2026-10-31,
  status mock.
- **One model (Q3):** FliStudio's state drifts toward one entity-relationship structure; extensions own sections, but not
  exclusively. *Source:* David 2026-10-31.
- **FliHub / FliCast B-roll button:** calls `broll.register`. Agreed to come after B-roll Pilot v1, which is now live.
- **FliTools describe service:** brief at
  `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/flitools-describe-service-2026-10-31.md`.
- **fli-core zones:** name `resources` and `footage` as ProjectZones, which fixes the sidebar's "RESOURCES/ 0".
- **fli-notes capture, banked 2026-11-01 (each needs a design first; do not build).** *Source:* David, relayed in
  `docs/briefs/david-rulings-and-storypilot-handover-2026-11-01.md` §A3, plus his Lab notes on D13.
  - Screenshots as part of a note (drag-in, paste-in, or region select): pointing at one element misses the area he means.
  - Capture inside extensions (Story Pilot isn't noteable yet), and clean capture across every app and extension.
  - "SuperRig": an OpenRig rig that learns how to add capture to any app and maintains it. Belongs with the OpenRig work.
  - FliHub side panels (rebuild parked): Chapters / Help / DAM tabs push the content aside instead of popping over it;
    settings become a contextual right-hand tab that expands to medium or large. Same idea for Story Pilot's settings
    (Lab note on D).
  - A hand-edit affordance in the script for a comma or one word at recording time.
  - Reading looks as a shared library: a global terminal / white-focus switch usable across all apps, both React and
    Electron (Lab note on C).
