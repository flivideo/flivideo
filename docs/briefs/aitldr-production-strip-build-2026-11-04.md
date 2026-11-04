# Build brief: AITLDR production strip as a brand recipe (Option B)

Approved by David 2026-11-04: "move forward on building it out as per your ideas, then let me know how it looks based on Jan's videos."

## Goal
In FliStudio, show Jan's seven-step production strip for AITLDR days (Script, Voice, Alex, Animation, Final, Short, Published), computed from files on disk, with a "waiting on team" state. Read-only. No new writes to project folders.

## Read first
- Reconstruction: docs/specs/aitldr-strip-reconstruction-2026-11-02.md
- Visual mock (5 tabs): docs/specs/aitldr-strip-visual-2026-11-02.html (artifact https://claude.ai/artifact/6aS8ixcVMGvcPZFrC4QEdE)
- Jan's message: /Users/davidcruwys/dev/aitldr/aitldr-brain/team/comms/009-from-jan.md
- Existing code to extend: flistudio/server/src/capabilities/project-status.ts (global STEPS list; comment says a brand recipe can swap it)
- Prior art, READ ONLY, do not check out or delete: git tag `archive/aitldr-production` (commits 99e8ff2, 8acc93f). Use `git show`, never a working tree. Branch is 127 commits behind main.

## Build
1. Per-brand step recipe: STEPS becomes a lookup by brand, default unchanged for every other brand. AITLDR gets the seven steps.
2. Four states per step: done / waiting (team step while script/handoff/ exists and owed files not all back) / gap (a later step is done but this one has no file) / open.
3. Fix the Animation rule: look in motion/hyperframes/ as well as motion/remotion/ (HyperFrames since b17).
4. Show it on the brand page (a strip per day) and the project page (a Production box). Match the mock; real FliStudio tokens.
5. Expose via the existing project.status capability (and bin/flistudio), not a new door, unless the existing shape cannot carry it.

## Open rule (Jan has not answered, default shown)
Does "waiting" end when ANY owed file lands, or only when EVERY owed file is back? Default: every file back. Make it one constant so it is a one-line change. Do not message Jan.

## Verify
- Run on the real folders /Users/davidcruwys/dev/video-projects/v-aitldr/b13 to b23. Expected, from my re-run of Jan's rules: b13-b15 Alex gap; b16 Alex gap and Short open; b17 Voice gap, Alex gap, Animation open (before the HyperFrames fix); b23 Voice gap.
- Other brands' project.status output unchanged (diff before and after).
- Look at the real screens in a browser, not just tests.

## Not established (flag, do not guess)
- Jan's Mac may hold files missing here (b17 and b23 body voice, b13-b15 Alex), so some gaps may be false.
- Published step not evaluated yet.
- Whether Jan has seen the strip.

## Limits
Commit and push to main. No merging of the archive branch. Do not restart apps without David's go. Report back to David with a screenshot set, and to the session that briefed you.

## Orch dispatch (flivideo-orch, 2026-11-04 16:35)
- **Builder:** `aitldr-strip-dev`. **Machine: M4**, because the M2 is powered off (shut down 11:05 for David) and verification
  needs the real `v-aitldr/b13…b23` folders, which live on the M4.
- **Worktree, never the live checkout:** `git -C ~/dev/ad/flivideo/flistudio fetch origin && git -C ~/dev/ad/flivideo/flistudio worktree add ~/dev/ad/flivideo/flistudio-worktrees/aitldr-strip -b aitldr-strip origin/main`;
  `npm install`; **`npm run build` first** (fresh-worktree rule), then typecheck/tests.
- **Overrides "commit and push to main":** push branch `aitldr-strip` and STOP. Orch gates on the M4 (full unit + FULL e2e incl.
  `project-status.spec.ts`), merges ff-only, restarts FliStudio via `my-app` (orch's standing job; the brief's "no restart without
  David's go" is about the builder), and takes the screenshots on real b13–b23.
- Before → after: save `bin/flistudio project status` output (JSON) for 3 non-AITLDR projects (one appydave, one beauty-and-joy, one
  voz if present) and diff after — must be identical. Test the "every vs any owed file" constant both ways in unit tests.
- Report to `flivideo-orch`: sha, test counts before → after, the b13–b23 table (computed vs the brief's expected), the diff result.
