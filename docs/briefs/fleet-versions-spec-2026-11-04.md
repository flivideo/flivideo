---
created: 2026-11-04
timestamp: 2026-11-04T17:10+07:00
---
# Brief: spec page — FliStudio brings the Fli apps up to date on other people's machines (2026-11-04)

**From:** `flivideo-orch`. **To:** `fleet-versions-spec` (**M4**). Report to `flivideo-orch` and STOP.
**Go:** David, 2026-11-04 ("What would this all look like?"). **Machine: M4** — research + a published page, no code; the M2 is
offline, and artifacts publish from here. **No code, no branch, no changes on anyone's machine, no restarts, no roster edits.**

## David's ask
From FliStudio, on machines like Jan's or David Kaff's, bring FliStudio and the other Fli apps (about five, incl. Teletubby) up to
the latest version (e.g. a git pull). They do NOT need restarting.

## 1. Find what exists first (read, don't assume; cite file:line)
- App set: `~/.config/appydave/apps.json` (`group: flivideo` entries) and the my-app registry `~/dev/ad/apps/app-registry`.
  List exactly what the registry says (FliStudio, FliCut, FliEdit, FliHub, Teletubby, FliCast …): repo path, branch, start mode.
- Machines: `~/.config/appydave/machines.json`. Jan = `jan-mini` (Tailscale 100.106.92.117, user janreyes, shared from his own
  tailnet; memory: Jan's code moves by git bundles — `/Users/davidcruwys/.claude/projects/-Users-davidcruwys-dev-ad-brains/memory/jan-mac-access.md`).
  **David Kaff is not in the roster: say so, treat him as "machine not yet known".**
- What FliStudio already has to build on: `app.launch` / my-app doors (`flistudio/server/src/capabilities/launch.ts`), the
  lifecycle contract (`/Users/davidcruwys/.claude/projects/-Users-davidcruwys-dev-ad-brains/memory/app-lifecycle-contract.md` and
  what it points to), any version/health verbs (grep the capability registry, `api/openrpc.json`).
- Versions: compare sha / branch / dirty for each app on the **M4** (local) and the **M2** (ssh over Tailscale — it may be
  offline: say so). For **Jan**: only access that already exists and is permitted; read-only; if unclear, don't connect — record
  "not checked, why". Never change anything on Jan's machine.

## 2. Design — one recommendation plus alternatives
- **Versions view**: machines × apps; each cell = sha, commits behind origin/main, uncommitted changes y/n, last pulled.
- **Bring to latest** per app or per machine = fetch + `pull --ff-only` + `npm install` only if the lockfile changed. **No restart.**
  Refuse (with the reason shown) on uncommitted changes, non-main branch, or diverged history.
- **Reaching other machines**: compare (a) ssh over Tailscale from FliStudio, (b) a small agent on each machine that FliStudio asks,
  (c) git bundles for machines without GitHub access (Jan). Security trade-off for each. These are other people's machines: propose
  a **consent model** (who approves, when, whether the owner must be present, what's logged).
- **Agent-drivable**: JSON-RPC verbs (e.g. `fleet.versions`, `fleet.update`), stamped who did it, dry-run first.
- **After a pull**: the running app keeps the old code until its next restart → show "update ready, restart pending".

## 3. Publish
Load `brand-dave:brand` first. AppyDave light only; `grep -c "prefers-color-scheme"` = 0; pass
`/Users/davidcruwys/dev/ad/appydave-plugins/canvas/skills/visual-brief/scripts/check-artifact.mjs`. Content: a mock of the Versions view
(real app names and real M4 shas), the flow, the options table, the consent model, the recommendation, and the 1–2 decisions only
David can make. Publish with claude-artifacts; add a row to `/Users/davidcruwys/dev/ad/brains/ARTIFACTS.md` (git pull first, only
that file); save the source as `/Users/davidcruwys/dev/ad/flivideo/docs/specs/fleet-versions-2026-11-04.html` plus a short
`fleet-versions-2026-11-04.md` (Purpose / For Agents / findings with file:line / recommendation / decisions). Commit only those files;
push (GitHub may be in an outage — if the push fails, say so; the commit stays local).

## Report
URL, the recommendation in 3 lines, the 1–2 decisions for David, what was not checked. STOP.
