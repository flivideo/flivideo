---
created: 2026-11-04
timestamp: 2026-11-04T08:55+07:00
---
# Brief: the d01 trial composition in FliEdit, rendered side by side with HyperFrames (2026-11-04)

**From:** `flivideo-orch`. **To:** `fliedit-sbs` (**M4**). Report to `flivideo-orch` and STOP.
**Go:** David, 2026-11-04 (relayed). **Machine: M4** — a watched render, no code. **No FliEdit code changes.**

## Read first
- `docs/ecosystem-research/candidates/hyperframes-vs-fliedit.md` (the comparison you add results to).
- The HyperFrames side: `~/dev/video-projects/v-appydave/d01-flivideo-tour/hyperframes/d01-trial/` (`index.html` = the
  composition: chapter 03 = takes 03-1 + 03-2, two DJI cutaways, a callout, a sine-tone "music" bed ducked 1→0.35→1).
  Studio app: `hyperframes-studio` on 127.0.0.1:7210 (`my-app`), README `~/dev/ad/apps/hyperframes-studio/README.md`.
- FliEdit: `/Users/davidcruwys/dev/ad/flivideo/fliedit` — `CLAUDE.md`, `docs/AGENT-NOTES.md`, `docs/drivable-audit-2026-10-31.md`,
  `bin/fliedit.mjs`, skill `flivideo:fliedit`.

## Do
1. **Render the HyperFrames side** once: `hyperframes render … -q draft` (or the app's documented way) from the d01-trial dir.
   Output into `~/dev/video-projects/v-appydave/d01-flivideo-tour/hyperframes/renders/` (not git). Note wall time.
2. **Rebuild the same composition in FliEdit**, driven through its door/CLI, as a new FliEdit edit for d01 (project-local, media
   referenced — never copy or write into d01's footage/recordings). Same takes, same cutaway in/out points and positions, same
   callout timing, same music bed and duck, same 1920×1080 / 25 fps. Read the times from `index.html`.
   - **Where FliEdit can't do a step, record the gap and move on — no workarounds** (e.g. callout: FliEdit has no text layer;
     duck: no volume automation — note what the nearest native option would be, but don't build it by splitting/fading by hand).
   - FliEdit has no `my-app` lifecycle. Prefer windowless/headless door use; if the app window is needed, start it with its
     own `bash scripts/app.sh start` and stop it after. Don't edit apps.json.
3. **Render** it with `export.start` into the same `renders/` folder; note wall time.
4. **Side-by-side page** `docs/artifacts/hyperframes-vs-fliedit-d01-2026-11-04.html`: load `brand-dave:brand` first and
   `canvas:visual-brief`; AppyDave light only; `grep -c "prefers-color-scheme"` = 0; pass `check-artifact.mjs`. Contents: a
   step table (step · HyperFrames · FliEdit · gap), 3–4 matched frame grabs (same timestamps: before cutaway, cutaway, callout,
   duck), render times, file sizes, local paths to both renders. Publish with claude-artifacts if available (add the row to
   `/Users/davidcruwys/dev/ad/brains/ARTIFACTS.md`); else say "needs publishing".
5. Append `## Side-by-side d01 — 2026-11-04` to `hyperframes-vs-fliedit.md` with the measured results; update the "Not verified"
   list. Commit only these docs (flivideo; brains ARTIFACTS.md if published) and the FliEdit edit file's text if it lives in
   v-appydave (`git add` that path only). Push.

## Out of scope
FliEdit code, new verbs, lifting HyperFrames code, the upstream clone, the FliStudio button.

## Report
Both render paths + times, the gap list, artifact URL (or "needs publishing"), commits. Say what wasn't verified (e.g. duck audibility).
