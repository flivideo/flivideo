---
created: 2026-11-01
by: curation-rsch
status: research, read-only; no code, skills or projects touched
---
# Curation inventory — what already curates sessions, captures and dossiers

**Verdict:** nothing existing does "keep a story's sources placed, ordered, and known-fresh". Several pieces do the *synthesis* well; **none records what source state its output was built from**, so none can tell it is stale. The single biggest design fact: **Story Pilot's server has no way to call a skill** (no spawn / LLM call in `flistudio/modules/storypilot/server/`), it is driven *from* Claude Code over JSON-RPC. So "an app triggers a skill" is a gap, not a given.

## 0. Method and what I could not verify

- Ran the mandatory inventory: 2,605 `SKILL.md` files across the five roots (file count, mostly cached/build copies). Worked from the live `~/dev/ad/appydave-plugins/<plugin>/skills/*/SKILL.md` only.
- Read each skill's frontmatter and grepped bodies for staleness terms (stale / hash / refresh / as-of / drift / superseded). **I did not read every skill end to end**; "no staleness handling" means *none found by those greps plus the description*. A grep miss is not proof of absence (no positive control run beyond finding known hits like dossier's sha256).
- Not verified: how `captains-log:find`/`enrich-check` enrich captures; `abridge` internals beyond its frontmatter; whether any skill outside `appydave-plugins` curates (the other ~40 project-local skill folders were not read).

## 1. Table

"Staleness?" = records what source state it was built from AND can detect it is out of date. "Callable" = could Story Pilot (an app) trigger it without a Claude Code agent in the loop.

| Skill / piece | Plugin | Does | Input → output | Staleness? | Places/orders? | Callable from Story Pilot? |
|---|---|---|---|---|---|---|
| `captains-log:dossier` | captains-log | ChatGPT conversation → working dossier, filed as a `chatgpt` capture | ChatGPT chat (via Chrome) → dossier capture | **Partial, wrong direction.** sha256 proves the *copy* is byte-exact, not that the dossier is current. A conversation that continues gets **another** dossier (`previous_dossier:` link), never an update. Nothing says "this dossier predates 40 new turns" | No | No. Agent drives Chrome |
| `captains-log:keeper` ("Donna") | captains-log | Builds one draft note per scope with links to each item's canonical source, saved to Captain's Log | codes/paths/URLs/conversation → note capture | Only "stale **drafts**" (unsaved), not stale content. Explicitly **will not sort, bucket, rank or route** | **No, by design** | No. Agent skill, M2-only save |
| `captains-log:find` / `enrich-check` | captains-log | Query/write/run captures; enrichment check | capture codes → results | Not assessed | No | CL has an HTTP API (`$CAPTAINS_LOG_URL`), so *reading* is app-callable; synthesis is not |
| `steno:fact-sheet` | steno | Corpus (conversation, transcript, doc set) → one durable labelled fact sheet (FACT / DECISION / INFERENCE / OPEN…), states own limits | corpus → sheet | **Closest.** Has `MODE=refresh` (patch keeping claim IDs) and "states its own limits". But no recorded source-state stamp that a machine could compare; refresh is human-invoked | No (organises by claim, not by story) | No |
| `steno:steno` | steno | Live meeting scribe, structured notes | spoken dumps → note | n/a (live) | No | No |
| `sesh:session-archaeology` | sesh | Reads N past sessions, synthesises what changed, triangulated against git | session IDs → digest | Verifies claims against the repo (good), but output is not stamped with session line-counts / end-times | No | No. Fans out reader subagents |
| `sesh:retrospective` | sesh | Judges sessions against the SKILL.md that governed them | session IDs → critique | No | No | No |
| `sesh:session-recall` / `session-rescue` | sesh | *Find* a session from vague memory / crash paste | → `claude --resume` command | n/a | Ranks candidates, not placement | No |
| `appydave:lisa` | appydave (**legacy plugin**) | KDD librarian: capture a learning live; reconstruct a KDD from transcripts | transcripts → KDD | Has `status --run <dir>` (run progress), not source freshness | Promotes learning→pattern | No |
| `appydave:lexi` | appydave (legacy) | Brain librarian; has "stale as current" / supersession audit | brain files → audit | **Yes for brains**, not for sessions | No | No |
| `sitrep:topic-map` / `run-map` | sitrep | Subject map / plan-position map of the **current** conversation; run-map has open-items | live conversation → view | n/a (reads the live thread) | Weights threads, no story order | No |
| `writers-room:observer` | writers-room | Read-only recorder of a multi-agent run into a typed event log (MD + JSONL); can reconstruct after the fact | rig/queue/transcripts → run-log | Append-only log, timestamped; no "built-from" stamp on the reconstruction | Chronological only | No |
| `writers-room:showrunner` / `story-editor` / `scribe` / `voice-coach` / `segment-writer` | writers-room | Topic → angles (gate) → beat sheet → script → voice grade. `segment-writer` reads a FliStudio `knowledge` group | research → script | No | **Story Editor orders into beats** (the only existing placer), but for a *topic + research*, not for attached sources | No. Crew run inside Claude Code |
| `flivideo:storypilot` | flivideo | Reads `story.brief`, writes the build-story script, saves via `story.script.set`, hands to Teletubby | brief → script | No. Script is not stamped with source state | Uses `sources` order; does not decide it | **It *is* the agent side**: Claude Code → JSON-RPC door |
| `abridge` (agent, `~/.claude/agents`) | n/a | Near-lossless summary of large content (sonnet) | big text → structured summary | No | No | No |
| `compass:set-north-star` / `go-north` / `coverage` | compass | Interview David → a repo's North Star; judge work against it | David + repo → goal doc | n/a | n/a | No. Repo-scoped, not video-scoped |

### Story Pilot's own (non-skill) pattern — how a source becomes RAW vs SYNTH today

Code: `flistudio/modules/storypilot/shared/contracts.ts` (L154-201), `server/story.ts`.

- **Placement is a manual, flat list.** `story.sources.set` takes *the project's resource ids, each with a `role`* (`what-happened · why · who · how-to-tell · other`) and an optional label. "This only orders and labels them." `story.json` holds `sources[]`. Anything not in it is "not placed". That is exactly D18's 20 unplaced.
- **RAW vs SYNTH is derived at read time from the resource's kind/channel, not stored.** `Layers = { raw: {what, known}|null, synth: [{what, by, text}] }`. Rule in the comment: Plaud/omi/note/keeper captures and Claude session transcripts are **raw**; a `chatgpt` capture (dossier), a note, the `why` line are **synth**. `raw.known:false` when a capture's channel wasn't recorded. So the answer to David's question ("automatic, synthesised, or raw-then-synthesised later?") is: **they arrive raw or as someone else's synthesis; Story Pilot never produces a synthesis itself and nothing "becomes" synthesised later.**
- **Provenance exists, freshness does not.** `Provenance` records session id/name/machine/transcript, capture code+channel, `writtenIn`, and `added` stamp. There is **no** field for "built from session X up to turn N / N lines / mtime". `server/story.ts` stats the transcript file (L415) to read it, but nothing is persisted for comparison.
- **The only working staleness mechanism in the whole suite is the Listen spec** (`storypilot-listen-2026-11-01.md` §3): audio is keyed by a **content hash** of (words, voice, speed, engine); "stale = current hash ≠ stored hash, computed live, no timestamps". That is the pattern to copy for synthesis.
- `story.settings` has `audience`, `feel`, `do` (David B667: "never defaulted") at creator › brand › series › video. There is **no `angle` or north-star field** (grep of `contracts.ts` for angle/north: no hits; positive control `feel` hit).

## 2. Gaps

1. **No synthesis anywhere is stamped with its source state.** Dossier = copy-verified only. Fact-sheet `refresh` and archaeology are manual and unstamped. This is David's "how do I know the synthesis is stale" question, and nothing answers it.
2. **A growing source has no identity across syntheses.** Dossier forks a new capture per continuation; sessions get re-read from scratch. Nothing links "synth v2 of session X" to "synth v1".
3. **Nobody places material for a *video's* story.** Story Editor orders beats for a topic; Keeper refuses to rank; Story Pilot orders only what David hand-sorts.
4. **App → skill is impossible today.** Story Pilot server never calls an LLM or spawns Claude. A "refresh" button needs a trigger path (see §3).
5. **Overload is unaddressed.** Every existing skill produces *more* text. None produces a one-line "what this source is, whether it's current, where it goes" that David can scan instead of read (his "19 boxes" complaint).
6. **No angle field** in Story Pilot; see §4.

## 3. Recommendation: reuse vs replace

**Build one new skill in `flivideo` (e.g. `flivideo:storypilot-curate`). Placement rule: a domain plugin, never the legacy `appydave` plugin** (Lisa/Lexi live there; reuse them by reference only).

Reuse:
- **`steno:fact-sheet` as the synthesis engine for one source.** Its labelled-claim format and `refresh` mode (keep claim IDs) is the right unit. Do not rewrite it; call it per source.
- **`abridge` / reader-subagent pattern from `session-archaeology`** for big transcripts (noise-stripped, one per session).
- **`flivideo:storypilot` + `story.brief` / `story.sources.set` / `story.source.read`** as the I/O: the door already exists.
- **Listen's content-hash staleness** as the staleness model.
- **`writers-room:story-editor`'s angle gate** (3-4 angles, human picks) for the angle step.

Replace / add (the genuinely new part):
- **A per-source digest sidecar** with a **source stamp**: for a session, `{transcript path, line count, last-turn timestamp, hash of the user-turn text}`; for a capture, `{code, content sha}`; for a dossier, `{capture code, conversation_id}`. Stale = stamp ≠ current, computed live, like Listen. Digest also carries: one-line gist, raw/synth tag, proposed `role`, proposed position, one-line "why here".
- **Placement proposal, never silent placement:** the skill proposes role+order; David approves in the UI (he said he doesn't want to read, but wants it "placed properly").
- **Trigger path:** app marks stale and shows a button, but the refresh is run by a Claude Code session (or a `claude -p` the app spawns). That needs David's decision (see below). Not built here.
- Do not reuse Keeper (refuses ordering by design) or Dossier (ChatGPT-only, new-capture-per-continuation).

## 4. Angle / north star — who sets, uses or overrides one

- **`writers-room:story-editor` / `showrunner`** are the only skills that *set* an angle: propose 3-4, then "**Wait for the user to choose — the angle is their call**" and offer "or describe your own". So the design **respects** the human, but only if the human is present at the gate. In `from session` mode the Showrunner hands Story Editor a *stake candidate as the angle seed*, i.e. an agent-derived seed precedes David's choice.
- **Nothing in `flivideo:storypilot` or the Story Pilot settings holds an angle.** `feel` and `do` are the nearest ("what the viewer should feel / do"), explicitly never defaulted. They are outcomes, not a point of view. This is the hole David hit: with no angle field, an agent (D19/AppyStack) invented three angles ("spaghetti is stupid") that contradicted his view ("a great idea, we haven't got it working yet; the video is about getting it to work, an anti-slop AI system"). I did **not** read that session (sessions-rsch owns it); this is inferred from his quote.
- **`compass:set-north-star`** interviews David *first* and checks against repo evidence, the right order, but it is repo-scoped, not per-video.
- **Does any skill override the human's angle?** None *by rule*. The failure mode is by *omission*: no stored angle means any agent can fill the gap.

**Chicken or egg?** My take: **both, in order.** A *provisional* angle from David (one sentence, his words, before curation) is what lets curation decide relevance and placement; the evidence then confirms, sharpens or contradicts it, and a contradiction is surfaced *to David*, never resolved by the agent. Without an early angle, curation can only be "everything, summarised", which is the 19-boxes problem. So: add an **`angle`** (David's sentence, verbatim, with a `set-by: david` marker and date) at video level next to `feel`/`do`; curation reads it, may *propose* a revision, may not write it.

**Is "curation" the right name?** It fits the *screen* (a list you tidy) but undersells the job, which is: **read, digest, place, and keep fresh**, against an angle. Candidates: **"Story Prep"** (plain, matches Story Pilot), **"Source Desk"**, **"Briefing"**. I'd call the skill **`storypilot-prep`** and the thing it keeps up to date a **source digest**. The staleness word David used ("refreshable") should appear in the UI as "digest out of date · Refresh".

## 5. Decisions for David

1. **Trigger path:** (a) app shows "stale" and David runs the skill in Claude Code (cheap, today) · (b) app spawns `claude -p` itself (a button, but new infrastructure and cost). Recommend **(a)** now, (b) later.
2. **Angle field:** add `angle` to Story Pilot settings at video level, written only by David? Recommend **yes**.
3. **Name:** `storypilot-prep` vs keep "curation". Recommend `prep`.
