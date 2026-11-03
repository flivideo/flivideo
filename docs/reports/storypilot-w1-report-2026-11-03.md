# Story Pilot W1 — Document Islands: build report (2026-11-03)

**For**: `flivideo-orch` (re-gate on the M4, merge, restart, d13 dock extract). **From**: the W1 build session on the M2.
**Brief**: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/storypilot-w1-document-islands-2026-11-03.md`.
**Status**: pushed and stopped. Nothing merged, nothing restarted. Worktrees left in place for orch to clean up.

W1 is pushed to `storypilot-w1` (`debd138`). All four parts of the brief are built and tested. On the M2 the only
failures are the 14 overlay-pilot unit tests and 2 overlay e2e tests that fail on origin/main too, because the M2 has
no Python `PIL` for the renderer.

## Commits

- flistudio `storypilot-w1`: `debd138`, branched from origin/main `2509f5e`.
  Worktree: `/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/storypilot-w1`.
- appydave-plugins `storypilot-w1`: `1bc84ea` (flivideo 2.7.3). It adds the Roamy wrapper `dock_extract.py` and
  three SKILL.md changes: read sessions to the end, don't write `meta.channel`, and placing a capture writes `usedBy`
  back to Captain's Log by itself. Merge it after flistudio.
  Worktree: `/Users/davidcruwys/dev/ad/appydave-plugins-worktrees/storypilot-w1`.
- `client/src` is untouched (show-chips) and so are the templates verbs (templates-dev). Two files may need a trivial
  rebase against templates-agent: `modules/storypilot/shared/contracts.ts` (verb list) and the storypilot SKILL.md
  (different sections).

## Tests on the M2, before → after

| Suite | Before | After |
|---|---|---|
| storypilot | 221 | **278** ✓ (coverage 97.6% lines) |
| server | 759 ✓ · 4 ✗ | 759 ✓ · 4 ✗ (PIL) |
| overlay-pilot | 61 ✓ · 10 ✗ | 61 ✓ · 10 ✗ (PIL) |
| extension-core / broll-pilot / client | 55 / 53 / 335 | unchanged ✓ |
| e2e | not run before | 45 ✓ · 2 ✗ (overlay, PIL) · 12 skipped |

- Typecheck, lint, format and `api:check` are clean; OpenRPC has 173 methods.
- The 12 e2e skips are the specs that copy the real d13/d18/d19 folders, which aren't on the M2. A grep finds nothing
  in them that W1 changes, but only the M4 gate actually runs them.
- `storypilot-reader.spec` passes with the new badges.

## The registry as built (`modules/storypilot/shared/islands.ts`)

| Badge | Key | Home | Keep | Live | Never | Layer | Opens |
|---|---|---|---|---|---|---|---|
| Claude session | `session` | `.jsonl` on its machine | pointer, title, why, dock extract | – | whole transcript | raw | reader |
| Plaud / Omi recording | `plaud` / `omi` | Captain's Log (M2) | `ref.id`, title, why | synopsis, date, length, source, signal, state | transcript, tags | raw | `?open=` link |
| Captain's Log capture | `capture` (no source known yet) | Captain's Log (M2) | same | same | same | raw | `?open=` link |
| ChatGPT dossier | `chatgpt-dossier` | Captain's Log, or a file | pointer, title, why | CL fields if a capture | – | synth | link, else file |
| Spec / doc | `spec` | a git repo file | path, title, why | file text on read | – | synth | file |
| Agent note | `note` | `fli.resources.json` | all of it | – | – | synth | reader |
| Claude artifact | `artifact` | claude.ai (login) | URL, title, why | – (and it says so) | – | synth | url |
| Web link | `link` (also `page`) | the web | URL, title, why | – | – | raw | url |
| B-roll | `broll` | project folder | path | – | – | raw | file |

A Captain's Log capture also shows the mark `CAPTAIN'S LOG · B663`.

## d13 extract sizes (dry run on the M4, nothing written)

| Session | Turns | Chars | Transcript |
|---|---|---|---|
| `8aa7c642` | 20 | 27,705 | 8.6 MB |
| `62b99237` | 18 | 6,141 | 39.8 MB |
| `09d843f5` | 29 | 17,291 | 11.0 MB |

The old filter's 58k and 80k were mostly skill bodies (30k and 74k). Every real David turn is kept. So source 04's
"60k cut" was about 92% skill text.

## CAPTAINS_LOG_URL

Set `CAPTAINS_LOG_URL=https://mac-mini-m2.tail1acb0f.ts.net` in **flistudio's root `.env`** on the M4
(`/Users/davidcruwys/dev/ad/flivideo/flistudio/.env`; the server loads it through dotenv, read by
`studioConfigFromEnv` in `server/src/config/studio.ts`). Until then every capture says "CAPTAINS_LOG_URL is not set".

## How the dock extract runs

**On the M4, after merge and restart** — for each d13 session, run `story.session.extract {brand: "appydave",
project: "d13", resource: <id>}` with ids `r_7ee2c9ec90`, `r_d5034beb28` and `r_d85c3984ac`.

**On Roamy, after the merge.** Roamy has both transcripts, but it has neither project folder and its flistudio checkout
is 13 days old:

```
git -C ~/dev/ad/flivideo/flistudio pull && git -C ~/dev/video-projects/v-appydave pull
python3 ~/dev/ad/flivideo/flistudio/modules/storypilot/scripts/dock_extract.py --project ~/dev/video-projects/v-appydave/d14-appy-invoice --session 6c2d63f4 --by agent:flivideo-roamy
python3 ~/dev/ad/flivideo/flistudio/modules/storypilot/scripts/dock_extract.py --project ~/dev/video-projects/v-appydave/d19-spaghetti-rig --session 633b7385 --by agent:flivideo-roamy
cd ~/dev/video-projects/v-appydave && git add d14-appy-invoice/resources/sessions d19-spaghetti-rig/resources/sessions && git commit -m "dock extracts (Roamy)" && git push
```

Then `git pull` v-appydave on the M4. The `.gitignore` lets `*.turns.json` through.

## What the brief got wrong

1. **"Stop writing `meta.channel`"**: no code writes it. Agents set it by hand through `resources.add`, so the fix is
   the SKILL.md line.
2. **`capture_mark_used` "equivalent HTTP call"**: Captain's Log has no REST route for it. I call the MCP tool over
   its stateless `POST /mcp`, which works today.
3. **d19 has 74 islands, not 73.** Its sessions put the machine in `meta.host`, not `meta.machine`, so the machine
   never showed. Provenance now falls back to `meta.host`.
4. **d18 has two `session` resources that are brief `.md` files** (`tool: "brief"`, no session id). They now show as
   Spec / doc.
5. **d18's session tagged "roamy" (`afaf0ee4`) has its transcript on the M4.** The two that are really unreadable are
   d14's `6c2d63f4` and d19's `633b7385`, as the brief said.
6. **The brief doesn't say how a Roamy extract reaches the M4.** It goes through the v-appydave git repo, as in the
   command above.
7. **"A CLI script in the storypilot skill"**: the real script lives in flistudio, where `sessions.test.ts` checks it
   gives the same output as the TypeScript code. The skill has a small wrapper that runs it.
8. **"Show the rest"** is wording only for now ("the first part shown · show the rest: N more characters"). The button
   is W2.
9. **Two W0 pins changed beyond the KNOWN BUG ones.** `[Image #n]` is now stripped instead of dropping the whole turn.
   The artifact read now says it can't be read, which the registry asks for.
10. **A third hard-coded verb count** lives in `door.test.ts`. AGENT-NOTES didn't list it; it does now.
11. **The schema mirror** was already 1,392 differences out of date on origin/main. I didn't regenerate it, because
    the repo notes say that conflicts across lanes.
