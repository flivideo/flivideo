---
title: "Launch + Publish: the plan (draft for David)"
created: 2026-10-11
timestamp: 2026-10-11
---

# Launch + Publish: the plan (draft for David, 2026-10-11)

**Purpose**: Merge everything David has said about FliStudio's Launch and Publish pages into one ordered plan, plus the team to send it to.

**For Agents**: Draft. Nothing dispatched until David says go. Sources: `ui-notes-2026-10-06.md` (items 1–43),
`requirements-bundle-2026-10-09.md` (FS-ANGLES-GATE, FS-UPLOAD-STAGING, FS-SHOWDOWN-CARD), the Publish UX brief
`/Users/davidcruwys/dev/ad/brains/brand-dave/channel-ops/runs/flistudio-publish-ux-brief-2026-10-05.md`.
Step 0 of every wave: check each item against the CURRENT page (some are already fixed: the 10-step order, "Read it, then Approve or Edit", copy/Finder buttons).

## Wave 1: unblock the decisions (bugs; small)
- Angles can be approved before thumbnails exist (FS-ANGLES-GATE, #35); a gate can be closed/superseded; agent names reach the record; propose before gate.open.
- Approve in the step footer beside Previous/Next (#40); chapters step before description (#39).
- Stale "waiting for your decision" banners (#27); newer suggestions after approval get a quiet "compare" (#36).
- "Test winner"/"Remove" only after the video is live, with undo; shortlisting clears a winner mark (#13, #19, #33).

## Wave 2: make it readable and trustworthy
- The work leads: blockers first, project dashboard below or folded (#1, #2, #34); one wording for counts (#3); "2 to fix" names its two things (#43).
- End screen shows related videos as thumbnails + titles from the brand archive (#41).
- Labelled copy buttons, one meaning per icon, brand defaults visible (#28–#30); chapters shown once (#31).
- Title pool and re-pairing explain themselves; original pairings kept (#12, #18); superseded proposals don't count as clutter (#32).
- ⓘ jitter (#11); tag warnings you can act on (#17); members-promise warning (#42).

## Wave 3: new features
- **Upload staging folder** (FS-UPLOAD-STAGING): MP4 + SRT + chosen thumbnails in one transient folder, path on the clipboard.
- **Launch ends in Publish**: the YouTube link box and "Mark published" at the end of the upload steps (#23).
- **Showdown card** (FS-SHOWDOWN-CARD): flivideo-orch designs 2–3 options as an artifact first; the build follows David's pick.
- Later, cross-app: visible undo + who-changed-what (#14).

## Team
OpenRig, 3 seats, on the M2 (same shape as flicut-reapply, no lead): **builder** (Opus) in a FliStudio worktree, **QA** (Opus, tests
each slice from a clean `git archive` with Playwright against a throwaway brand/project, never a real `v-*` project), **r1** (Fable, reads
every diff). One builder, because Waves 1–2 mostly touch the same files (`client/src/components/LaunchPieces.tsx`, `uploadSteps.ts`,
`server/src/capabilities/launch.ts`). Deliver a wave, push a branch, report once; David reviews on a real project, then merge.
