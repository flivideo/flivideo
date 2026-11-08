---
created: 2026-11-02
timestamp: 2026-11-02T15:10+07:00
---
# AITLDR production strip — reconstruction for David (2026-11-02)

> **Built 2026-11-04** (option B, FliStudio `59d82fe`). What it shows now, and what the mock had that was not built: [aitldr-strip-as-built.md](aitldr-strip-as-built.md).

**By:** `aitldr-strip-rsch`, for David (via `flivideo-orch`). Research only: nothing restored, merged or messaged.
Sources: Jan's 009, tag `archive/aitldr-production` (`99e8ff2`, `8acc93f`; fork `3ea915d`), orch audit §1, the real `/prod` files in `/Users/davidcruwys/dev/video-projects/v-aitldr/`, FliStudio `main` at `c2719c4`.

**Verdict first:** the idea is still good and Jan's file shape has not changed. But main's new Project status does **not** answer it for AITLDR (it reads FliVideo-style folders; AITLDR days live in `voice/`, `avatar/`, `motion/`). Recommendation: **rebuild on today's FliStudio as a brand recipe** (option B, about half a day), not a port.

## 1. What Jan asked for (009, 2026-10-15)

- Idea: "On an AITLDR project's home page, one strip across the top: **Script → Voice → Alex → Animation → Final → Short**. Each step shows done or not done, so I can open a project and see where it's at without reading `script/plan.md`."
- Why: "Right now the answer is in a 100-line plan.md checklist per project … A strip on each project, or one row per project on the brand page, would have shown that at a glance."
- "FliStudio could tell 'done' from files that already exist, so nobody has to tick anything."
- Three thoughts: (1) "**A 'waiting on team' state** between done and not done would help most. It's the one we lose track of: the handoff went out (`script/handoff/` exists) but Voice and Alex haven't come back." (2) "**Per brand** … maybe the steps live in brand config rather than in FliStudio's code." (3) "Maybe a 7th step, **Published**, which Launch probably already knows."
- Framing: "an idea for David to judge, not a request to build now. If it doesn't fit how FliStudio is built, no problem. Tell me and I'll keep using plan.md."
- No reply to 009 exists in `comms/` (010 = `start-day`, 011 = Day 26 status). Jan was never told it was built or declined.

## 2. What was built

Two commits, 2026-10-14/15, on branch `aitldr-production` (29 files, +3331; real code ≈ `server/src/capabilities/production.ts` ~410 lines, `shared/src/production-steps.ts` 127, `Production.tsx`, `productionModel.ts`, CSS). Read-only capability `production.view { brand, project? }`.

| # | Step | Done when | State logic | Read from |
|---|---|---|---|---|
| 1 | Script | `script/script.md` exists | done / open | file |
| 2 | Voice | audio in `voice/` (not `short-*`) | **waiting** while `script/handoff/` exists and not back | `voice/` + handoff table |
| 3 | Alex | an `intro` **and** an `outro` video in `avatar/` (not `short-*`) | **waiting** (as above) | `avatar/` + handoff table |
| 4 | Animation | video in `-renders/remotion/out/` or `motion/remotion/out|build/` | done / open (not team-gated: Remy can render early) | folders |
| 5 | Final | `videos/<skill>/<skill>-final.mp4` | done; **closes**: a missing earlier step becomes **gap** | file |
| 6 | Short | `videos/<skill>-short/<skill>-short-final.mp4` | done; closes | file |
| 7 | Published | Launch has a YouTube link marked published (`fli.resources.json`) | done; closes | resources |

States: **done / waiting / gap / open**. Steps are pure data per brand (`PRODUCTION_STEPS`, keyed `aitldr`); AppyDave has none, so no strip and no call. Also parsed: `plan.md` "Production checklist" (ticked/total, next open box, latest dated note, open `→ [ ]` asides) and `handoff.md` (File table + Sent date; a file counts as back when `voice/` or `avatar/` holds that name or `name-tN`). Missing/unparseable files are said with a reason, never guessed. Tests use byte-exact b16/b17/b18 copies plus b13 (gap), b16 (waiting), b18 (complete), b19, b20.

```
Project page (top of Production box)
 ┌─────────────────────────────────────────────────────────────────────┐
 │ [✓ Script] [⏳ Voice] [⏳ Alex] [○ Animation] [○ Final] [○ Short] [○ Published] │
 │ waiting on team: day23-body.wav, day23-intro.mp4, day23-outro.mp4    │
 │ plan.md: 11/18 · next: /gap-check against shot-list.md              │
 └─────────────────────────────────────────────────────────────────────┘
Series list (one compact strip per Day)
 Day 23  rights-check   ●●⏳⏳○○○   Day 22  avatar-blocks  ●●●●●●●
 legend: ● done  ⏳ waiting on team  ◐ gap  ○ open
```
(Mock is mine, from the commit messages; I did not render the branch.)

## 3. What has changed since 10-15

- **Branch is 127 commits behind main** and does not merge cleanly (10 files conflict; real ones `ProjectHome.tsx`, `studio.css`). It also predates the Project status feature.
- **Jan's file shape still holds (checked on disk today).** 17 of 23 AITLDR projects have `script/plan.md` with a "Production checklist" (b07–b23); b13–b23 (11 projects) also have `script/handoff/handoff.md`. Newest are b21/b22 (2026-10-21) and b23 (2026-10-27). Same sections, same "Sent <date>" line, same `day23-intro.mp4`-style file table. b01–b06 are older and have neither.
- **Drift to check:** returned file names vary (b23's voice came back as `voice over.mp3`, not `day23-body.wav`), so "file counts as back by handoff name" will miss it. The step rule "any audio in `voice/`" still works; the "owed files" list would show false misses. b17–b23 have `fli.resources.json`, so Published still has a source. b19+ animation sits in `motion/` (old rule covers it).
- **`production.view` itself still fits** as a read-only capability, but the capability count, openrpc, `contracts.ts` and `door/cli` tests it touched have all moved (the 7 mechanical conflicts).
- **Project status (main) overlaps in idea, not in content.** `server/src/capabilities/project-status.ts` computes a status column from files for every brand, "a list, so a brand recipe can swap it later". But its `STEPS` is one global list (Idea, Script, Recorded, Editing, Exported, Final cut, Launch prep, Published) detected from `scripts/`, recordings, cuts and exports. It knows nothing of `voice/`, `avatar/`, `motion/` or `script/handoff/`, and **there is no per-brand recipe mechanism yet** (the swap is a comment, not code). So for AITLDR it says the wrong things (no recordings in an AITLDR day) and cannot say "waiting on team".

## 4. Options

| | A. Port as-is | B. Rebuild on today's FliStudio (**recommended**) | C. Something else |
|---|---|---|---|
| What | Rebase/cherry-pick the 2 commits, fix 10 conflicts | New brand-recipe seam in Project status; AITLDR recipe = Jan's 7 steps + `waiting` state; carry across only the plan/handoff parser and the b16–b19 fixtures | Skip FliStudio code: a small script/skill in the aitldr repo that prints the strip from the same files (Jan runs it, or it writes a `status.md`) |
| Cost | ~2–3 h of conflict work, then a second page/UI to maintain beside Project status | ~½ day (orch's estimate; I agree) plus a recipe seam in `project-status.ts` | ~1–2 h; no FliStudio change |
| Pros | Fastest to something visible; tests exist | One status surface for all brands; brand-as-data honoured; Jan's "per brand" thought satisfied properly | Zero risk to FliStudio; works today |
| Cons | Two parallel status UIs; re-conflicts on every FliStudio change; page/CSS is stale | Touches the shared status engine (needs care; other brands unaffected if recipe is opt-in) | Not on the project home page, which is what Jan asked for; Jan must run something |

**Recommendation: B**, and only after Jan answers the two blocking questions below (the waiting rule depends on them). Interim cheap win if David wants something this week: C.

## 5. Questions only Jan can answer

1. Do you still want the strip, now that you know `plan.md` has been kept up to date through Day 23? Is it still a pain to find where a day is?
2. Is "waiting on team" still the most useful part, and how should it end: when **any** voice/avatar file lands, or only when every file in the handoff table is back (returns come under different names, e.g. `voice over.mp3`)?
3. Is `script/handoff/` created only when you send the team files? Does it ever get deleted afterwards? (The waiting rule relies on it existing.)
4. Do you want one strip per project (home page), one row per project on the brand page, or both?
5. Is the 7-step list right? Should the Short and the Final be separate steps, or is "Short" often skipped (b16 has none)?
6. Is the `plan.md` "Production checklist" format fixed (top-level boxes = stages, "Carried over" ignored, `→ [ ]` asides), or will it change?
7. Do you want it to show the next open checklist item ("next: /gap-check …") or only the strip?

## Unverified / not established

- I did not run the archived code or its tests, and did not render the UI. The ASCII mock is a sketch from commit messages.
- "Gaps doc 2026-10-14" (cited by commit 1) still not found.
- Whether Jan has seen the strip at all: no record either way.
