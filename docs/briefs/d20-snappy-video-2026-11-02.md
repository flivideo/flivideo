---
created: 2026-11-02
timestamp: 2026-11-02T13:30+07:00
---
# Brief: create the Snappy video project (D20) and preload its story sources (2026-11-02)

**From:** `flivideo-orch` (Swagger). **To:** `d20-snappy-work` (this window is the Snappy video's home, like
`d13-overlaypilot-video` / `d18-storypilot-video`). Report to `flivideo-orch` by name.

## 1. Create the project
- Orch checked: `v-appydave/` live codes run d05…d19, no `d2*` anywhere (live or `archived/`). **Confirm D20 is still free**
  (also in FliStudio's project list) before creating. Name: `d20-snappy`.
- Create it the way D19 was created (FliStudio / FliHub's create path — find it via the `flivideo:flistudio` and
  `flivideo:flihub` skills; never hand-roll `fli.studio.json`). Convention: `/Users/davidcruwys/dev/ad/brains/video-as-code/project-folder-convention.md`.

## 2. Preload story sources (`resources.add`, see `flivideo:storypilot` SKILL.md "kinds")
1. **B682** — David's Plaud voice log, 2026-11-02 06:33; the Snappy part is roughly the last ~10 minutes (screen capture
   from "we might as well start… pre-empting another build" to "I want to go with Snappy"). kind `capture`,
   `ref {schema:"captains-log", id:"B682"}`, `meta.why` naming the Snappy section.
2. **B683** — the ChatGPT dossier (§13–17, §25, §27 are Snappy). kind `capture`, ref B683. Local copy:
   `/Users/davidcruwys/dev/ad/flivideo/docs/specs/b683-dossier-2026-11-02.md`.
3. **The Snappy spec, as a LIVING source** — kind `dossier`, `path` = `/Users/davidcruwys/dev/ad/flivideo/docs/specs/snappy-spec-2026-11-02.md`
   (pointer to the file, never a copy), `meta.why`: "living spec — will evolve; Prep re-reads it and flags it out of date".
   Stamp it with `story.source.stamp` so a later change shows the out-of-date pill.
4. **"Why Snappy is needed"** — write a short piece (≤300 words) built ONLY from David's own words in B682 (quote him;
   years of hand-typed `sc_*` regions, the blog-post screenshot tool he loved 10 years ago, region + cycle + stop-motion,
   "it won't be built into FliStudio… needs to be closer to a native application"). Save it in the project's resources
   zone, attach as kind `dossier`, `meta.why` "David's words, compiled 2026-11-02".

## 3. Record the video concept — as David's idea, NOT as an angle
Add a project note (`fli.notes` via the flistudio skill's note verb) or a resource of kind note, verbatim:
> **Concept (David, 2026-11-02):** Build Snappy in Swift with an off-the-shelf simple developer/tester rig template from
> OpenRig. The rig is reusable for future Swift apps, and the learnings from this first build are banked for them.
> **Tie-in:** at the end of D12 David promised "a started team which is just a coder and reviewer"
> (`/Users/davidcruwys/dev/video-projects/v-appydave/d12-openrig-agent-teams/hub/transcripts/09-3-other-resources.txt`).
Attach that D12 transcript file as a source too (kind `dossier`, path, why "the promise this video keeps").
**Never call `story.angle.set` or `story.angle.propose`.** No Prep run, no intros, no script — David hasn't asked.

## Limits
- Do not touch FliStudio code, do not restart anything. Commit the project files in `v-appydave` (only `d20-snappy/`) and push.
- STOP and report: project path, resource ids, anything that refused.
