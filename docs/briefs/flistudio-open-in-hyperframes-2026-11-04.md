---
created: 2026-11-04
timestamp: 2026-11-04T08:55+07:00
---
# Brief: FliStudio "Open in HyperFrames" button, built like FliCut's launch (2026-11-04)

**From:** `flivideo-orch`. **To:** `hf-door-dev` (**M2**). Report to `flivideo-orch` and STOP.
**Go:** David, 2026-11-04 ("a video on FliStudio built like the FliCut one" = this launch button). **Machine: M2** — code,
standing ruling. **Start only after** `help-system` and `guide-slots` are merged to flistudio main (orch releases you).

## Read first
- How FliCut opens: `flistudio/server/src/capabilities/launch.ts` (+ `launch.test.ts`), `app.launch` in `registry.ts`, the door
  log, and the client button that calls it. Mirror that, don't invent a second path.
- The app: `hyperframes-studio` in `~/.config/appydave/apps.json` (M4, 127.0.0.1:7210, `my-app`), README
  `~/dev/ad/apps/hyperframes-studio/README.md`. Studio serves ONE project dir, named in `~/dev/ad/apps/hyperframes-studio/project-path`;
  switching = write that file + `my-app restart hyperframes-studio`.
- Project convention: a video's HyperFrames projects live at `<video project>/hyperframes/<name>/` (first one:
  `v-appydave/d01-flivideo-tour/hyperframes/d01-trial`).

## Do
1. `app.launch` accepts `app: hyperframes` (or the app's registered key — match how flicut is named). For a video: find its
   `hyperframes/<name>/` project (one → open it; several → the newest, and list them in the answer; none → refuse
   `notFound` with a clear message, don't create one). If Studio isn't running, start it via `my-app`; if it's serving a
   different project, point `project-path` at this one and restart via `my-app`. Then open
   `http://127.0.0.1:7210/#project/<name>`. Stamp and door-log it like FliCut.
2. A button where the FliCut button is ("Open in HyperFrames"), shown only when the video has a `hyperframes/` project; tooltip
   per the new help-system rule (no inline key-hint text).
3. Tests: unit for the resolve rules (one / several / none / Studio down / other project), the e2e spec for the screen the button
   sits on, **run in full**. Regenerate `api/openrpc.json` if the contract changes.
4. Worktree: `git -C ~/dev/ad/flivideo/flistudio fetch origin && git -C ~/dev/ad/flivideo/flistudio worktree add ~/dev/ad/flivideo/flistudio-worktrees/hf-door -b hf-door origin/main`;
   `npm install`; `npm run build -w extension-core` before vitest. The M2 has no hyperframes-studio app: tests stub `my-app`
   and the HTTP check; never start real servers.

## Out of scope
The X2 token proxy (Studio stays loopback); FliEdit; creating HyperFrames projects; the upstream clone.

## Report
Branch sha, test counts before → after, e2e spec name + pass count, the exact `app.launch` call. Orch re-gates on the M4
(full e2e spec, merge, restart), then screenshots the button and the Studio it opens on d01.
