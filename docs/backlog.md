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
