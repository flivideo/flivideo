# Story Pilot W1: Document Islands

**Purpose**: Build brief for W1 of the Story Pilot plan. Every source becomes a typed *Document Island* whose nature
decides its badge, fields, canonical home, and whether FliStudio keeps it, shows it live, or never copies it.

**For Agents**: Read in full before starting. You can't open the plan artifact; everything you need is here and in
`docs/briefs/storypilot-captains-log-mapping-2026-11-03.md` (the design note: read "The rule: three tiers",
"Session sources", "Islands across all story videos"). Owner: `flivideo-orch`. From: `flivideo-roamy` (David delegated
the plan; W1 needs no further David decisions).

## Where you start

- flistudio main ≥ `2509f5e`, with W0's characterization tests (`modules/storypilot/server/characterization.test.ts`,
  `e2e/storypilot-reader.spec.ts`). Fresh worktree: `npm run build -w extension-core` before vitest.
- W0 pinned two **KNOWN BUG (W1)** cases. Flipping them from "bug pinned" to "fixed" is part of this job.
- Build on the **M2** in a worktree off origin/main. The M2's status-hook stall is fixed (3 s cap); if a worker shows
  "running … hooks" for minutes, `pkill -f "it2 set-status"`.

## 1 · The island registry (shared)

One table in `modules/storypilot/shared/` that every other part reads. For each kind: `nature` (what it is, the badge
words), canonical `home`, `tier` per field (keep / live / never), `layer` default (raw / synth), and how to open it.

| Island (badge words) | Kind / test | Home | Keep | Live | Never |
|---|---|---|---|---|---|
| **Claude session** | `session` | `.jsonl` on its machine | pointer, title, why, **dock extract** | – | whole transcript |
| **Plaud recording** / **Omi recording** | `capture`, channel plaud/omi | Captain's Log (M2) | `ref.id`, title, why | synopsis, date, length, signal, state | transcript, tags |
| **ChatGPT dossier** | `capture` channel chatgpt **or** `dossier` from ChatGPT | Captain's Log / file | pointer, title, why | (CL fields if a capture) | – |
| **Spec / doc** | `dossier` that is a repo file | git repo file | path, title, why | file text on read | – |
| **Agent note** | `note` | inside `fli.resources.json` | all (it is the canonical) | – | – |
| **Claude artifact** | `artifact` (claude.ai URL) | claude.ai (login) | URL, title, why | – (app can't read; say so) | – |
| **Web link** | `link` | the web | URL, title, why | – | – |
| **B-roll** | `broll` | project folder | path | – | – |

Badges show the **nature**, never the storage word. Captain's Log captures read `CAPTAIN'S LOG · B663` plus the
nature, e.g. "Plaud recording". These names are decided; don't re-litigate them.

## 2 · Session dock extract (the cross-machine fix)

- A command (agent verb plus a CLI script in the storypilot skill) that runs **on the machine where the transcript
  lives**. It writes `resources/sessions/<session_id>.turns.json` into the project: David's turns only (skill bodies,
  pasted blocks, cross-session messages, `[Image #n]` and tool results removed), each with `{index, timestamp, text}`
  anchors, plus `{session_id, machine, path, bytes, sha256, extractedAt, by}`.
- The Reader and `story.source.read` use the extract when it's present; they fall back to the transcript, then to "not
  on this machine (made on Roamy, run the extract there)".
- **No 60k cut on the extract.** `story.source.read` gains `offset`/`limit` paging for agents. The Reader may still
  show the first part but must say "show the rest" (the UI itself is W2; the verb and its contract are W1).
- Fix the **skill-text leak** in `ownTurn` (user-role "Base directory for this skill:" bodies and `isMeta` messages).
- Staleness: when the transcript's size or mtime changes, the extract is marked out of date (reuse Prep's stamp idea).

## 3 · Captain's Log live card

- FliStudio server config `CAPTAINS_LOG_URL` (M4: `https://mac-mini-m2.tail1acb0f.ts.net`, reachable, health 200).
  Never hard-code the host.
- Server fetch of a capture's metadata (synopsis, createdAt, source/channel, signal, state; duration if the API gives
  it, else omit) with a short cache. Offline → one line "Captain's Log unreachable" while keeping tier-1 fields.
- Deep link `${CAPTAINS_LOG_URL}/?open=<CODE>` exposed on the source (UI button is W2).
- Stop writing `meta.channel` for new captures (it's tier 2); leave existing ones.
- Write-back: when a capture is placed in a story, record provenance in Captain's Log (`capture_mark_used`
  equivalent HTTP call, `usedBy: "<brand>/<project> Story Pilot"`). Idempotent. If the API isn't there, report and skip.

## 4 · Tests (flip W0's pins, add W1's)

- Every registry kind: badge words, layer, open target.
- KNOWN BUG (W1) cases now assert the fix.
- Extract: filter correctness, anchors, hash, paging, out-of-date detection, the fallback order.
- CL card: success, offline, unknown code (mock HTTP; no live CL in tests).
- Run against fixture shapes of **d13, d14, d18, d19** (d19 is the stress case: 73 islands, every kind).

## Out of scope

The Reader redesign (W2: chat-style sessions, "show the rest" UI, the Open button styling); story instructions and
settings (W3); rerun, versions and undo (W4); copying transcripts; rebuilding Captain's Log; reading claude.ai artifacts
from the app.

## Gate and report

Unit + typecheck; the full storypilot module suite; `storypilot-reader.spec` updated to the new badges; every other
suite green. Merge ff-only on the M4 and restart via `my-app`. Then:
1. Run the dock extract **on the M4** for d13's three sessions.
2. Tell `flivideo-roamy` the exact command for **Roamy**, which runs it for d14 and d19's Roamy-made sessions.

Report to `flivideo-roamy`: commits, test counts before → after, the registry table as built, extract sizes for d13,
and anything in this brief that turned out wrong.
