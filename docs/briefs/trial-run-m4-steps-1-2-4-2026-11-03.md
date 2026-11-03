---
created: 2026-11-03
timestamp: 2026-11-03T18:30+07:00
---
# Brief: trial plan steps 1, 2, 4 — auto-editor (X6), Textream (X5), HyperFrames as editor (X1 + X2 runtime) (2026-11-03)

**From:** `flivideo-orch` (Swagger). **To:** `trial-run` (M4, cwd `/Users/davidcruwys/dev/ad/flivideo`). Report to `flivideo-orch`.
**Go:** David via `flivideo-roamy`, ~18:25: "trial-plan steps 1, 2 and 4 on the M4 … runs he watches, not coding."
**Machine: M4**, because David wants to see these apps running (watch rule), and no product code is written.

## Read first
- `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/08-trial-plan-on-m4.md` §1 (d01 is the worked example), §3 A
  (auto-editor), B (Textream), C (HyperFrames), §4 steps 1, 2, 4.
- `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/05-research-experiments.md` rows X6, X5, X1, X2 (pass/fail).
- `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/candidates/hyperframes-as-editor.md` §Experiment X2 (code-read
  pass; its runtime half is yours).
- Ruling R13: run AGPL tools unmodified, never copy their code into FliVideo.

## Rules for all three
- Everything under `~/dev/upstream/scratch/<X?>/` on the M4. **Copies** of d01 media only
  (`/Users/davidcruwys/dev/video-projects/v-appydave/d01-flivideo-tour/`); never write into the project folder.
- Installs are approved (David's go): `pipx`/`pip --user` or a venv for auto-editor; Textream as a macOS app (download
  the release, record its version and source URL); HyperFrames from the registered upstream clone — on the M4 it is not
  downloaded yet: `~/dev/upstream/sync.sh --only hyperframes`, then copy it into scratch, `pnpm install` there.
- Do not touch `flistudio/` or any app repo, `my-app`, or `~/.config/appydave/apps.json`. No Docker.
- Any server you start: confirm the bind address with `lsof`, and **stop it** before you finish; nothing left listening.
- Keep a short timed log per experiment.

## Step 1 — X6 auto-editor (1.5 h)
Run auto-editor on a copy of the raw take 08 §3 A names (`03-1-flistudio.mov` or as stated); compare its cut list and kept
duration with FliCut's cut of the same take (read FliCut's cut file from d01, read-only). Pass/fail per 05.

## Step 2 — X5 Textream (1.5 h) — not during a recording session
Install, enable Director; push a copy of d13's Story Pilot script over its HTTP/WebSocket and `textream://`; check whether
word progress is readable by a script; check bind address + auth. **Leave the app open on screen at the end with the d13
script loaded** so David can see it, and say so in the report.

## Step 4 — X1 HyperFrames as an editor, incl. X2 runtime (3 h)
Start the studio server (default bind) in scratch; X2 runtime: `lsof` bind line, one read + one harmless mutation by `curl`
locally, CORS header check, and a read attempt from the M2 over Tailscale (`ssh davidcruwys@100.126.70.25 curl …`) that must
FAIL if it binds loopback. Then X1 per 05 on a d01 copy (chapter 03 + 2 DJI clips): cut, ripple-delete, move, trim, music
bed + duck via CLI `--json`, render. **Open the Studio UI in a browser window for David at the end** (then stop the server only
after you report; say in the report that it is still running and how to stop it — orch will stop it).

## Write up
For each: a dated `## Experiment X? — 2026-11-03` section in the matching candidate file under
`docs/ecosystem-research/candidates/` (verdict, evidence, what FliStudio would need), and append "X? 2026-11-03: <pass/fail>"
to the **Recommendation** cell of its row in `06-approval-register.md` (R16 for X6, R15 for X5, R10/R9 for X1/X2). Never
change a Status cell. Commit only those files (`git add <paths>`), push.

## Limits / stop
Timebox ~6 h total; if one experiment stalls past its box, write what you have and move on. Disk: report scratch size at the
end. If the permission checker blocks starting a server, STOP that step and report exactly which command, so orch can ask
David — do not work around it. STOP after the push; report per experiment: verdict, key evidence, scratch path, what is
left open on screen.
