---
created: 2026-11-08
timestamp: 2026-11-08T15:30+07:00
---
# AITLDR production strip — as built

**Purpose**: What FliStudio now shows for AITLDR days, read from the code, and what the mock had that was not built.

**For Agents**:
- Read from FliStudio `main`, commit `59d82fe` (2026-11-04, "feat(status): AITLDR production strip as a brand recipe"). The strip files are unchanged on `origin/main` since then.
- The rules live in `flistudio/shared/src/production-steps.ts`; the evaluator is `flistudio/server/src/capabilities/production-strip.ts`; the UI is `flistudio/client/src/components/ProductionStrip.tsx`.
- Background and the mock: [aitldr-strip-reconstruction-2026-11-02.md](aitldr-strip-reconstruction-2026-11-02.md), [aitldr-strip-visual-2026-11-02.html](aitldr-strip-visual-2026-11-02.html) (artifact https://claude.ai/artifact/6aS8ixcVMGvcPZFrC4QEdE).

## What it is

A read-only strip of seven steps per AITLDR day, worked out from files in the project folder. Nobody ticks anything. It rides on the existing `project.status` call as an extra `production` field. Only brands listed in `PRODUCTION_STEPS` get it (today only `aitldr`); every other brand's output has no such field.

## The seven steps

| # | Step | Done when | Team step? |
|---|---|---|---|
| 1 | Script | `script/script.md` exists | no |
| 2 | Voice | `voice/` holds an audio file not starting `short-` | yes (audio) |
| 3 | Alex | `avatar/` holds an `intro` and an `outro` video, not starting `short-` | yes (video) |
| 4 | Animation | a video in `-renders/remotion/out`, `motion/remotion/out`, `motion/remotion/build`, `motion/hyperframes` or `-renders/hyperframes` | no |
| 5 | Final | `videos/<skill>/<skill>-final.mp4` exists | no, closes |
| 6 | Short | `videos/<skill>-short/<skill>-short-final.mp4` exists | no, closes |
| 7 | Published | Launch has a YouTube link marked published in `fli.resources.json` | no, closes |

`<skill>` is the folder name without its code (`b18-overlay-pack` → `overlay-pack`). The HyperFrames folders in step 4 are the fix the brief asked for.

## The four states

| State | Glyph | Meaning |
|---|---|---|
| done | ✓ | the step's files are there |
| waiting | ⏳ | "waiting on team": a team step (Voice, Alex) while `script/handoff/` exists and the files the handoff table owes are not back |
| gap | ! | no file, but a later closing step (Final, Short, Published) is done: the day went on without it |
| open | ○ | nothing yet ("not yet") |

A closing step that is done ends any earlier waiting. Owed files come from the File table in `script/handoff/handoff.md`; a file counts as back when `voice/` or `avatar/` holds the same name, or the same name with a take number (`-t2`).

## The waiting rule

`PRODUCTION_WAITING_ENDS_WHEN = 'every'` in `flistudio/shared/src/production-steps.ts`.

- `'every'` (the default): waiting ends only when every owed file for that step is back.
- `'any'`: waiting ends as soon as any file for the step lands.

Jan has not answered which he wants, so it is one constant: a one-line change.

## Where it shows

- **Brand page** (`/b/aitldr`, the Project status list): one compact strip under each day's row, with a short "still owed" note (for example "Voice: 2 files owed").
- **Project page**: a **Production** box between the project header and the pipeline strip. It shows the handoff line ("Handoff sent 2026-10-21" or "No handoff yet"), the seven chips, and one line per waiting step listing the owed files.
- Each chip's tooltip says the rule ("Done when …"), the files found, and what is still owed.
- Agents and scripts get the same data from `project.status` (and `bin/flistudio project status`).

## In the mock but not built

- The **handoff table** on the project page (each owed file with Who and State: back / not found / optional). Built shows only the list of owed files for a waiting step.
- The **"plan.md says"** panel: ticked count ("12 of 19"), next open box, loose ends. `plan.md` is not read at all.
- The **reason under each box** on the page. Built puts it in the hover tooltip only.
- Fixing the old status boxes for AITLDR. The default eight-step status column (Idea … Published) still shows for AITLDR rows, so its "Exported, next: Final cut" nag is still there beside the new strip.
- The **"try it" any/every toggle**. Built has no switch in the UI; the rule is the constant above.
- Mock-only extras: the "AITLDR recipe" label on the list and the "new · AITLDR only" tag on the box.

## Not checked

- I read the code and tests only. I did not open FliStudio or look at the live screens.
- The commit named in the hand-off, `fcb585a`, was not found on the M4 or the M2 copy (all branches). The strip on `main` is `59d82fe`.
