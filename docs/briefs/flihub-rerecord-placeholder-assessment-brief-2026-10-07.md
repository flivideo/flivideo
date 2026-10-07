# FliHub: placeholder chapters, re-recording and resequencing (assessment brief)

**Purpose**: Hand-off for a fresh research session. Assess what FliHub would need so David can leave a placeholder chapter, carry on recording, come back later and re-record it (overwrite, replace or delete segments, and let the others close up). This is an ASSESSMENT ONLY; build nothing.
**For Agents**: Read in full before acting. Written by `flivideo-orch` on 2026-10-07 from David's own words (quoted below). Report back to `flivideo-orch` via SendMessage.

## David's words (2026-10-07)

> One of the chapters has one item in it, and that's Chapter 6. This is a complete video, so I'm not after any changes here at all. But when I do video D07, I'm going to want to put in a placeholder chapter, and it's going to feel very much like Chapter 6. Then I'll keep going on to whatever the next chapter is, come back, and re-record it.
>
> Re-recording and moving stuff around has a few challenges. There's how you set it in the inbox. The inbox isn't designed to go backwards. It can go backwards, but it's not designed to, and it's certainly not designed to overwrite. It's not designed to have an effective segment number, because it wants to use the next one. Here, even if I could redo the inbox for chapter 6, it would be chapter 6-2, when really, if I wanted to overwrite 1, that's what I wanted.
>
> There's also a problem with the recordings themselves in Chapter 6. "What do I want to do with 06-01? I might want to delete it." Or I might want to record a 06-02, delete 01, then let 02 trickle up into position.
>
> This is all about putting in a placeholder, and later redoing that placeholder and maybe other stuff under it. Or there might be three segments in a row and I just want to get rid of segment two.
>
> What I'm looking for is not a fix. It's an assessment of what we'd want to do in FliHub to have this capability in the future.

## The example he's looking at

FliHub at http://localhost:5100/#recordings, project **D01** (`/Users/davidcruwys/dev/video-projects/v-appydave/d01-flivideo-tour/`). Chapters show as `NN Name`, with files named `<chapter>-<segment>-<slug>.mov` (e.g. `04-1-kybernesis.mov`, `04-2-…`, `04-3-…`), and each row has "→ Safe", "→ Park", "Delete" and a transcript marker. Chapter **06 Constant Improvement** has a single file, `06-1-constant-improvement.mov`; that's the shape a placeholder would have. **Read only: don't change D01 or any project.**

## What to assess

Read FliHub's code (`/Users/davidcruwys/dev/ad/flivideo/flihub/`): the inbox/recording flow (how the next chapter/segment number is chosen and how a new recording is named), the recordings view, Safe/Park/Delete, transcripts beside the takes (`hub/transcripts/<take>.*`, `engines/…`), and anything that renames. Also check the neighbours that depend on those names: FliCut (cuts reference media by path; `fli.cut.<name>.json`), FliTools transcription jobs, FliStudio (video.text's take ladder, Start-a-cut drafts), and the brains' rulings on naming (`/Users/davidcruwys/dev/ad/brains/video-as-code/project-structure-reading-list.md`, `project-folder-convention.md`, FliHub docs). Then answer:

1. **Today:** what happens step by step if he tries each scenario: (a) placeholder then come back and overwrite 06-1; (b) record 06-2, delete 06-1, have 06-2 become 06-1; (c) delete the middle of three segments and close the gap; (d) insert a new segment between two existing ones; (e) re-record a whole chapter. Where it breaks, and what gets orphaned (transcripts, FliCut cuts, FliTools jobs, trash).
2. **The model:** should segment numbers be **positions** (renumber on change) or **identities** (stable ids, with order as separate data)? Weigh this against the suite's rulings ("metadata over renames/copies/folders", "stages are filenames"), FliCut's path references, and transcripts keyed by take name. Give a recommendation and its reason.
3. **The inbox:** what an "effective/target segment" would look like, i.e. choosing "this next recording goes to chapter 6, replacing segment 1" or "insert as 6.5", versus always-next. What the UI and the API would need.
4. **Placeholder as a first-class thing:** a chapter marked "placeholder / to re-record", visible in FliHub (and FliStudio), so he can see what's left to redo.
5. **Safety:** overwrite means the old take goes to trash (`-trash/`), never lost, plus undo, and keeping FliCut and transcripts consistent after a renumber.
6. **A phased plan:** smallest useful first step, then the rest, with rough size, and which app owns each part (FliHub vs fli-core vs FliStudio).

## Deliverable

1. A written assessment at `/Users/davidcruwys/dev/ad/flivideo/docs/flihub-rerecord-placeholder-assessment.md` (file:line evidence for every "today" claim). Commit and push it in the flivideo repo (stage by name; end the message with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`).
2. **Also a visual page** (David can't read Markdown reports): publish it as a Claude Artifact in the AppyDave brand, light only. Load the `brand-dave:brand` skill first, follow the Artifact tool's rules, and run the ghost check `grep -c "prefers-color-scheme"` = 0. Show the scenarios as before/after diagrams of the chapter/segment list, plus a recommendation and a phased plan. Register it in `/Users/davidcruwys/dev/ad/brains/ARTIFACTS.md`.
3. Report to `flivideo-orch` via SendMessage: a decision card (≈10 lines: what it decides, an options table, "My take: X, because…", one place to act; rule at `/Users/davidcruwys/dev/agents/factory-kit/talking-to-david.md`), the artifact URL and the doc path.

## Constraints

- Assessment only: no code changes, and no edits to any video project or app.
- Don't start, stop or restart FliHub or any app. Read its code; if you need to see the UI, use read-only browser navigation only (Playwright, then browser_close), clicking nothing that writes (no Safe, Park, Delete or record).
- Stop after the report to `flivideo-orch`.
