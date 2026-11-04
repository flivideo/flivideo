---
created: 2026-11-04
timestamp: 2026-11-04T10:35+07:00
---
# Brief: FliEdit ← HyperFrames watch list + a deeper UI/UX gap analysis (research only) (2026-11-04)

**From:** `flivideo-orch`. **To:** `fliedit-watch-rsch` (**M4**). Report to `flivideo-orch` and STOP.
**Go:** David, 2026-11-04 ~10:30 ("deeper dive gap analysis on the M4"; keep the two apps "not in lockstep, but understand the gap
and how to close it"). **Machine: M4** (David's call; HyperFrames Studio is installed here). **No code. No FliEdit changes.**

## Do
1. **Watch list** at `/Users/davidcruwys/dev/ad/flivideo/fliedit/docs/upstream-watch-hyperframes.md` (FliEdit owns it). Rows:
   feature · what HyperFrames does (version seen) · FliEdit today (file/verb) · how we'd rebuild it our way (clean-room, never
   lift) · value to David · size · priority. Seed with H1–H5 from
   `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/candidates/hyperframes-vs-fliedit.md`. Header: re-check rule =
   whenever `~/dev/ad/apps/hyperframes-studio` bumps its pinned `hyperframes` version (and say so in that app's README).
2. **UI/UX deep dive.** David saw "beautiful styling in HyperFrames we could transfer" and that FliEdit "is working incredibly
   well". Start the Studio (`my-app start hyperframes-studio`) and FliEdit (`fliedit/scripts/app.sh start --brand appydave
   --project d01-flivideo-tour --video d01-hf-sbs`); compare screen by screen with Playwright screenshots (close the browser
   after): timeline, inspector, selection, transport, preview, styling, motion, empty/hover states. For each candidate: what
   it is, screenshot pair, why it'd help FliEdit, and how it fits FliEdit's own design (AppyDave brand, light). Add the
   worthwhile ones to the watch list as UX rows.
3. **Close both apps** at the end (`my-app stop hyperframes-studio`; `scripts/app.sh stop`) and confirm nothing listens on 7210.
4. Commit the watch list (fliedit repo, only that file + the Studio README line in its local repo); a short summary section
   appended to `hyperframes-vs-fliedit.md` (flivideo); push. If an artifact helps David see the pairs, AppyDave light only,
   ghost-check 0, publish, add the ARTIFACTS.md row.

## Report
Top 5 UX transfers with one line each, the watch-list path, commits, artifact URL if any.
