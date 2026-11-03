---
created: 2026-11-03
timestamp: 2026-11-03T16:20+07:00
---
# Brief: a plan of action to try the useful outside apps on the M4, inside FliStudio, on a real video project (2026-11-03)

**From:** `flivideo-orch` (Swagger). **To:** `eco-trial-plan` (M4, cwd `/Users/davidcruwys/dev/ad/flivideo`).
Report to `flivideo-orch` by name. **Go:** David, 2026-11-03 ~16:15. He isn't watching: run to done. **This is a PLAN — install,
clone and run nothing.**

## David's words (the requirement)
"If there are actually useful applications, we need to figure out a way on the M4 to actually get these applications
running and connected into a FliStudio. Otherwise, we'll never see it. Remember, we use applications. I'd almost need a
plan of action … on how to use each of them and how they could be used as if we were running them based on one of our
current video projects."

## Read first
- `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/00-index.md`, then `04-potential-target-architecture.md`,
  `05-research-experiments.md`, `06-approval-register.md`, and the files in `candidates/`.
- Rulings already made (do not reopen): **R6** AppyFactory; **R13** run AGPL tools unmodified as separate programs, learn
  from them, never copy their code into FliVideo. FliHub needs no alternative. FliStudio is video-first; apps open from it
  the way FliCut does (look at how FliStudio launches/links FliCut, FliEdit, Teletubby today — `flistudio/` source,
  read-only, and `/Users/davidcruwys/dev/ad/flivideo/README.md`).
- App lifecycle rule: every server on this fleet starts through `my-app` (`~/dev/ad/apps/app-registry/bin/my-app`,
  registry `~/.config/appydave/apps.json`). Docker is not yet approved (R12/X4 needs David's yes).
- Current video projects: `/Users/davidcruwys/dev/video-projects/v-appydave/` — d13-overlay-pilot, d18-story-pilot,
  d19-spaghetti-rig, d01-flivideo-tour. Read their folders (read-only) to pick ONE as the worked example; say why
  (it should have real footage/B-roll/script that exercises the most candidates). A second one only where the first
  can't show a candidate.

## Do
1. **Shortlist:** from 04's candidates, keep only the ones whose lean is *add* or *absorb* with something you can run
   (expect roughly: HyperFrames Studio, Immich, Textream, auto-editor, video-use, MLT/melt, maybe Cap). Drop *none*
   with one line each why.
2. **Per shortlisted app, one section:**
   - What job it would do for David, in his words (stage: script / record / cut / edit / B-roll / publish).
   - **The walk-through on the chosen video project**: step by step, as if it were running — which files from the project
     go in, what David clicks or which verb an agent calls, what comes out, where the output lands in the project folder
     (`fli.<ext>` zones), and what FliStudio shows.
   - **How it would run on the M4:** install method (brew / npm / pip / macOS app / Docker), the `my-app` entry it
     would need (name, port — check `apps.json` for free ports), disk + RAM estimate, licence and R13 posture.
   - **How it connects into FliStudio:** open-in-app button like FliCut, iframe/panel, background service called by a
     FliTools verb, or link-out only. Name the smallest seam.
   - Which experiment (X1–X9) proves it first, and the go it needs.
   - Verdict: **try first / try later / ideas only**.
3. **Order of play:** a single ranked sequence for the M4 — what to stand up first, second, third — with the cost of
   each step, and which steps can run while David is still testing the pilots (nothing that changes FliStudio code).
4. **Write** `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/08-trial-plan-on-m4.md` (frontmatter like the
   other docs; Purpose + For Agents), add it to `00-index.md`, and add one line under the backlog entry
   *Ecosystem research: 21 decisions* in `/Users/davidcruwys/dev/ad/flivideo/docs/backlog.md`.
5. **Publish a visual** for David (he doesn't read .md): load `brand-dave:brand` first; AppyDave, light only;
   `grep -c prefers-color-scheme` must be 0. Lead with the order of play as a table, then one card per app with the
   video-project walk-through. Source at
   `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/trial-plan-on-m4.html`, publish with `publish_files`
   (new artifact), add a row to `/Users/davidcruwys/dev/ad/brains/ARTIFACTS.md`.
6. Commit only your files (`git add <paths>`) in flivideo and brains; push both.

## Limits
- Plan only: no installs, clones, Docker, `my-app` changes, or edits to any app repo (`flistudio/`, `fliedit/`, …).
- **Do not edit `06-approval-register.md`** (a separate X2 worker is writing to it) or any Status cell anywhere.
- Mark anything you didn't verify as UNVERIFIED; carry the hedges from 03b/04.
- Timebox ~2 h. STOP after both pushes and report to `flivideo-orch`: the chosen video project and why, the order of play,
  the artifact URL, the shas.
