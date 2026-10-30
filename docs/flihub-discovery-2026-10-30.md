# FliHub — rebuild discovery

**Purpose**: What FliHub really does today, which parts are worth carrying, and what a rebuild on current AppyStack would gain and cost. Input to David's rebuild decision.

**For Agents**:
- Written 2026-10-30 by `flihub-rebuild-rsch` from the brief `docs/briefs/flihub-rebuild-discovery-2026-10-30.md`. FliHub was at `061ae34`.
- Discovery only. No code was changed, and FliHub was never stopped or restarted. The only live probe was `GET /api/system/health`.
- It builds on, and does not repeat, `flihub/docs/rebuild-2026/` (North Star, requirements archaeology, live-app findings, agent-drivable audit). Where those docs and this one disagree, this one is newer. The North Star's §2c "FliHub is the control plane" was overtaken by FliStudio from September on.
- The keep/drop/unsure list below is the same list the review artifact shows (one source). The full per-route, per-screen and per-file tables (with file:line) are in the four appendices at the end.

## Decided: rebuild (David, 2026-10-30)

David, relayed by flivideo-arch-rsch: **"Rebuild FliHub. It's fine."** This doc no longer asks *whether* to rebuild. It is the input for *how*:
- the 55-item keep/drop/unsure list decides what the rebuild carries over;
- the look-and-feel artifact is for David to pick from;
- the migration-risk list below covers what must not break at cut-over.

**Hard requirement: the rebuilt FliHub has a JSON-RPC door.** Extensions, starting with B-roll capture, depend on it.

**Recommended shape:**
- A slim FliHub on AppyStack, with the door from day one.
- It carries the 18 "keep" items and today's on-disk formats.
- It does not port the 16 "drop" items.
- The 21 "unsure" items wait for David's rulings.
- It is built beside the live app and cut over after one real recording day.

### The evidence for that scope

- **The part David uses is small, and it is where the tangle is.** David (B659, 2026-10-28): *"any recordings coming into Ecamm Live go into FliHub… I can watch them, transcribe them on the fly… route them to chapters and segments… see them all combined together as one long video. And that's pretty much all it does."* Every commit since August lands in that spine. The rest is 51.5k lines carrying 14 screens, 165 routes and 23 socket event types.
- **FliStudio has taken over about half of FliHub** since September: brands, projects, codes, stages, transcription view, words, trash, thumbnails, publishing and assets. FliStudio says outright that changing takes "stays FliHub's job" (`flistudio/client/src/screens/ProjectHome.tsx:1786`).
- **The door can't be added cheaply to today's code.** Today there are 165 hand-written Express handlers, 51+ of which return errors with HTTP 200, and a 922-line `App.tsx` that threads props to every tab (North Star §1).
- **Live defects the rebuild removes rather than patches:**
  - the Storage panel's Hold does the wrong thing (H2);
  - a GET writes config (C6);
  - stage overrides bleed across brands (C5);
  - two text-colour classes, used 155 times, produce no CSS.
- **The stack does not change.** FliHub is already on Express 5, React 19, Vite, Tailwind 4, Socket.io 4 and zod 4. The gain is the architecture, the door and the tooling.

## Counts

| | Count |
|---|---|
| **Keep** | **18** |
| **Drop** | **16** |
| **Unsure** | **21** |
| Total review items | 55 (features, grouped from 165 routes, 14 screens, ~40 panels, 9 watchers, 4 background jobs, ~30 on-disk writers) |

"Keep" needs evidence of use: a commit since August from live use, David's own words, or a live dependent. "Drop" needs evidence that it is dead, deprecated by David, or now owned by another app. Everything else is **unsure**, even when it looks obvious.

## How much of FliHub there is

| Surface | Count | Source |
|---|---|---|
| Code | 51,533 lines (TS/TSX, excluding tests), 84 test files | `wc`, appendix A |
| HTTP routes | 165 across 24 areas (74 GET, 91 mutating); 20 router mounts, 4 of them on `/api/projects` | appendix A |
| Socket events | 23, all server to client; 2 declared and never sent; no external listener | appendix A |
| Screens | 14 (10 in the nav, 4 behind the gear menu), about 40 panels and modals | appendix B |
| Dead client code | 5 unmounted components (the largest is 955 lines), 15 hooks with no caller | appendix B |
| Config | 23 `Config` fields (8 dead or half-dead), 11 env vars, 14 external files read or written | appendix C |
| Watchers / jobs | 9 chokidar watchers, 4 background jobs (FliTools queue, 20 s pass-2 poller, aspect queue, sound-hole queue) | appendix C |
| Writers into project folders | about 30, plus 6 targets outside them (Ecamm dir, ~/Downloads, T7 holding and published, ~/.flihub, server/) | appendix C |

## Who depends on FliHub (a rebuild must not break these)

| Dependent | What it touches | Risk |
|---|---|---|
| **FliStudio** | `POST/GET /api/context` on fixed `127.0.0.1:5101` (`launch/doors.ts:148-168`); runs `scripts/app.sh open`; migrate-layout asks FliHub's door whether a project is open; reads `.flihub-state.json` chapter titles; `words.import-flihub` reads `glingDictionary` from **FliHub's server/config.json**; reads take transcripts (`best-transcript.ts`) | **High.** Only live HTTP caller. Keep port 5101 and the `/api/context` contract, or change FliStudio in the same release |
| **FliTools** | Writes into FliHub's `hub/transcripts/`; only principal `agent:flihub` with `force_save` may replace FliHub-made files; writes `.txt` last because FliHub reads `.txt` as "done" (FR-94) (`flitools/src/transcribe/service.ts:340-374,717-738`) | **High.** Keep the principal name and the done signal |
| **FliCut** | Reads `hub/transcripts/<stem>.json` and `engines/<take>.mlx-flihub.json`; tells the user "redo it in FliHub ↻" | Medium. Formats are fli-core/FliTools-owned; keep the ↻ verb |
| **FliEdit** | Reads `hub/recordings/` | Low (layout is fli-core's) |
| **Skills** | `flivideo:flihub` (12 command docs, mostly `GET /api/query/*`, plus inbox write); `ylo-titles` and `ylo-description` **write** titles with `PUT …/title`; brand-dave `gather` and `current-deck` (the latter uses a wrong path, `/api/projects/resolve`); teletubby's courtesy GET | Medium. All are hand-written curl; re-point them to door verbs, or keep a thin REST shim for one release |
| **Socket.io** | No external listener (checked: FliStudio, FliDeck, FliGen, FliVoice, Storyline and AngelEye all connect to their own servers) | **Low.** The rebuild can redesign its events freely |
| **apps.json / AppyRadar** | Port probe on 5100/5101; `start_script ./start.sh`, `agent_start npm run app` | Low. Update the registry entry |

## What the rebuild gets from current AppyStack

| Gain | Today in FliHub | After | Note |
|---|---|---|---|
| **JSON-RPC door + OpenRPC** | No door. 165 REST routes, a hand registry listing 34, ad-hoc errors (353 `success:false` sites) | One capability core with named verbs (`takes.promote`, `segments.op`, `transcription.redo`…), a generated `api/openrpc.json` with `--check`, refusals as data | **The template does not ship the door.** `appystack/template/server/src/routes` has only `health` and `info`. The door is FliStudio's (`server/src/capabilities/`, 127 methods). A rebuild ports FliStudio's pattern, or the pattern is first extracted into a shared package. That extraction is a finding for the suite, not FliHub's job |
| **Template tooling** | No husky, no lint-staged, no `@appydave/appystack-config`, no depcruise, no Playwright e2e; CI red on every push (git+ssh fli-core); lint baseline has known errors | husky + lint-staged, shared eslint/ts/prettier presets, depcruise fences, Playwright e2e, helmet, rate limiter, request logger, tested shutdown and listen-error | FliHub has no log file: output goes only to the Overmind pane. Template pino + a `.logs/` file fixes the "silent failures leave no trail" rule in CLAUDE.md |
| **Extension seam (required: B-roll depends on it)** | No way to add a capability without editing the spine; B-roll was a branch inside `POST /api/rename` | The spine is the core, and extensions add namespaced verbs on the door (e.g. `broll.capture`, `broll.tag`) through a declared entry, fenced by depcruise | **`@flivideo/extension-core` is FliStudio-host-specific** (`ExtensionHost`, `HostKit`, FliStudio's stage keys). FliHub v2 needs either a host-neutral extension-core (a suite change: a finding for flivideo-orch, not FliHub's job) or its own thin host that follows the same rules (namespaced verbs, entry-only imports, conformance test). Decide this before the build starts, because the door's shape follows from it |
| **Fenced tabs (extension-core pattern)** | Tabs share state through `App.tsx` props; North Star measured 4 `groupByChapter` copies and 15 hand-rolled modals | The spine as the core; each surviving tab (e.g. MicCheck, if kept) as a fenced module that depcruise forbids from reaching into the spine | `@flivideo/extension-core` itself is FliStudio-host-specific (`ExtensionHost`). FliHub would borrow the **rules** (namespaced verbs, entry-only imports, conformance test), not the package. Alternatively, a kept tab becomes a FliStudio extension instead |
| **Marker + upgradability** | No `appystack.json`; drifts silently from the template | `appystack.json` marker, `lastUpgrade`, template-sync | The orch checkpoint banks "the AppyStack and AppyTron upgrade tools are unsafe" as a follow-up. Upgradability is real only after that is fixed |
| **Agent-drivable** | The one FliVideo satellite an agent can't drive | Door + CLI + skill generated from OpenRPC, in line with FliCut, FliCast and FliStudio | Lets the D04-style autopilot run promote, segment and redo-transcript without a browser |

## Migration-risk list

What must not break when v2 replaces v1. Owners and evidence are in Appendix D.

### 1. Data on disk (highest risk: the formats are the contract)

| What | Where | v2 must | Evidence |
|---|---|---|---|
| Hub layout | `hub/recordings`, `hub/transcripts` (all 13 local projects) | read and write it exactly; layout comes from fli-core `projectLayoutSync` | Appendix C §3 |
| Legacy layout | `recordings`, `recording-transcripts`: 62 projects on T7 `v-appydave-old`, 7 in `youtube-PUBLISHED` | **recommend: not read it.** A restored legacy project goes through FliStudio's `project.migrate-layout` first | Appendix C §4 |
| `.flihub-state.json` v1 | 10 local, 12 on T7; written through an allowlist that silently drops unknown fields | read v1 unchanged; stop dropping fields; keep chapter titles where FliStudio reads them (`flistudio/server/src/assets/assets.ts:233`) | `projectState.ts:76-108` |
| `.flihub-segment-journal.json` | 3 projects (d01, d11, d12) | read it, or undo of past segment ops is lost | `segmentOps.ts:228-244` |
| Transcripts | two JSON shapes (old whisper, FliTools `flitools.transcript/<n>`); `engines/<base>.<engine>.*` copies; `.txt` written last = done | carry the engine copies on every move; check `schema` before reading | AGENT-NOTES; FliTools `service.ts:340-374` |
| `fli.words.json` | project, brand and global word stores | write through fli-core only | `routes/state.ts:268-304` |
| `-trash/` | including FliTools' `-trash/<date>-pre-flitools/`; T7 rsync excludes it | same folder name; trash pill counts what empty removes | David ruling 2026-09-23 |
| Global config | `server/config.json`: 36 stage overrides and 2 priorities keyed by bare folder name, plus `glingDictionary` | don't migrate stage/priority (FliStudio owns stages); import the 24 Gling words once (Q9) | Appendix C §4 |
| Legacy leftovers | `recording-shadows/` (56 T7), `-safe/` (2 T7), `-chapters/` (3 T7), `edit-*` (33 T7) | ignore; never write | Appendix C §4 |

### 2. Live dependents (FliStudio, FliTools, FliCut, FliEdit)

| Dependent | Depends on | Break if v2… |
|---|---|---|
| FliStudio launch door | `POST/GET /api/context` on fixed `127.0.0.1:5101` (`flistudio/server/src/launch/doors.ts:148-168`) | moves port 5101 or changes the context contract. **Either keep `/api/context` as a REST shim, or change FliStudio to call the new door in the same release** |
| FliStudio reveal / open | runs `flihub/scripts/app.sh open` (`reveal.ts:25`) | removes or renames that script |
| FliStudio migrate-layout, project-rename | ask FliHub's door whether a project is open, and refuse if it is | stops answering "what's open" |
| FliStudio words import | `words.import-flihub` reads `glingDictionary` from FliHub's `server/config.json` (`capabilities/words.ts:278`) | drops the field before the one-time import |
| FliStudio best-transcript | reads take transcripts and `engines/` copies as owner `flihub` | renames files or drops the engine copies |
| FliTools | only principal `agent:flihub` with `force_save` may replace FliHub-made transcripts (`service.ts:717-738`) | sends a different principal name |
| FliCut | reads `hub/transcripts/<stem>.json` and `engines/<take>.mlx-flihub.json`; tells the user "redo it in FliHub ↻" | drops the redo action or changes the engine id `mlx-flihub` |
| FliEdit | lists `hub/recordings/` (`resolver.ts:97`) | changes the layout (it can't: fli-core owns it) |

### 3. Skills and commands (hand-written curl)

| Skill | Calls | Action at cut-over |
|---|---|---|
| `flivideo:flihub` (12 command docs) | `GET /api/query/*`, `POST /api/projects/:code/inbox/write`, health | regenerate from the OpenRPC door; drop inbox write if Q8 drops the inbox |
| `ylo:ylo-titles`, `ylo:ylo-description` | **write** titles: `PUT /api/projects/:code/title`, `…/chapters/NN/title` | re-point to the door's title verbs |
| brand-dave `gather`, `current-deck` | `GET /api/query/projects…`; `current-deck` uses a wrong path today | re-point; fix the path |
| `flivideo:teletubby` | courtesy `GET /api/query/projects/:code` | re-point |

### 4. Socket.IO consumers (low risk)

No external listener. FliStudio, FliDeck, FliGen, FliVoice, Storyline and AngelEye each connect to their own servers. v2 is free to redesign its live events. Two v1 events (`file:renamed`, `file:error`) are subscribed but never sent; don't carry them.

### 5. Process, ports and the shared Overmind

| Risk | Detail | Mitigation |
|---|---|---|
| Shared supervisor | v1 runs under an Overmind shared with AngelEye and Captain's Log; never `pkill overmind` | v2 gets its own `my-app` lifecycle (CLAUDE-PREFERENCES "servers go through my-app") and is never added to the shared Procfile during the build |
| Ports | 5100/5101 are hard-coded in FliStudio and `~/.config/appydave/apps.json`; AppyRadar probes them | build v2 on spare ports; swap ports and the apps.json entry at cut-over only |
| Live instrument | David uses FliHub during recording days; HMR and nodemon push changes into his tab | build in its own repo/folder; cut over on a non-recording day; v1 stays runnable as the fallback for a week |
| No log | v1 output goes only to the Overmind pane | v2 writes `.logs/` from day one (template pino) |

### 6. Scope risks

- **Scope gravity.** North Star §1 measured a tab going from portable to coupled in four hours (MicCheck). Write the depcruise fence on day one, or v2 regrows v1.
- **Unanswered unsure items become silent drops.** Hold/archive (H1) has no other home today. Leave it in v1, which stays runnable for storage, until Q3 is ruled.

## Decisions only David can make

Each has a recommendation. Q1–Q4 and Q6 shape the build; the others can be answered as the work reaches them. A new one comes first:

| # | Decision | Recommendation | For | Against |
|---|---|---|---|---|
| Q0 | **RULED 2026-10-30 by flivideo-orch: host-neutral extension-core, made before the FliHub build starts. The same change fixes G1 (an extension calling another app's door by name). Owner: flivideo-orch, after Story Pilot merges.** Original question, extension host for FliHub v2: make `@flivideo/extension-core` host-neutral, or give FliHub its own thin host following the same rules? | **Host-neutral extension-core**, as a suite change owned by flivideo-orch, decided before the FliHub build starts | One extension contract across FliStudio and FliHub; B-roll could later also show in FliStudio | A change to a package FliStudio and Overlay Pilot already use; it delays the FliHub start |

Evidence for Q0: `ExtensionHost` (`flistudio/extension-core/src/server.ts:21-36`) carries FliStudio and Overlay Pilot specifics (a `renderScript` that defaults to `modules/overlay-pilot/render/render.py`, FliTools polling), and `STAGES` is FliStudio's pipeline (`descriptor.ts:11`). The orch checkpoint already banks a related gap, G1: "ExtensionHost can't reach another app's door".



| # | Decision | Recommendation | For | Against |
|---|---|---|---|---|
| Q1 | ~~Rebuild, refresh or leave?~~ **Decided 2026-10-30: rebuild.** Open part: **how big is v2.0?** | **The spine only** (18 keep items) plus the door and an extension seam, built beside the live app | Small, well-evidenced scope; v1 keeps running until v2 passes a recording day | A second FliHub exists for a while; the dependents in the migration-risk list must be checked at cut-over |
| Q2 | **Who opens projects?** FliStudio only, or FliHub too (brand switcher, project dropdown, Projects tab)? | **FliStudio only.** FliHub opens on what FliStudio sends through `/api/context`, with a minimal recent-projects picker at most | Removes C2–C6 and their bugs; one owner for identity | Opening FliHub always needs FliStudio up (or a launch arg) |
| Q3 | **Hold / archive / T7: where does it live?** | **Out of FliHub, into FliStudio**, as part of the project lifecycle. Park it until then; v1 stays the tool for it meanwhile | FliStudio already owns project identity and the brand roots; H2 shows the FliHub version is confused | FliStudio gains a big, data-moving feature; until it lands, storage stays in v1 |
| Q4 | **Which look** for v2? | **Direction A, "Recording desk"** (see the look-and-feel artifact) | Built for the foot-pedal loop; everything else is a tab | Least like FliStudio; B or C read more like the suite |
| Q5 | **MicCheck**: keep in FliHub, or move to Teletubby's setup panel? | **Move to Teletubby** (or leave in v1 until then) | It is a pre-recording check; Teletubby is the pre-recording screen | Teletubby gains a server API and a socket stream |
| Q6 | **B-roll capture** (B659: b-roll as tagged segments, plus pinned/locked chapters): how does it arrive? | **As the first FliHub extension, on the door, straight after v2.0.** v2.0 ships the door and the extension seam; pinned chapters go in the spine's chapter model | Proves the extension seam on a real need; the old FR-161 lane (a branch inside promote) is dropped either way | Needs the extension-host decision (host-neutral extension-core, or FliHub's own thin host) before the build |
| Q7 | **Older manage tools** (renumber / swap chapters without guard or journal) | **Fold into guarded segment ops**; don't port the unguarded paths | One safe path; swap-chapters currently strands titles | A swap-chapters verb must be designed into segment ops |
| Q8 | **Assets, Inbox, Thumbs, POEM/AWB/YLO send, Transcripts tab**: still used? | **Drop all from FliHub.** Inbox writes go to FliStudio resources | Zero commits since March; FliStudio covers each | If one is used weekly, it's missed on cut-over day |
| Q9 | **Gling**: retired? | **Yes, retire.** Import the 24 `glingDictionary` words into the suite word store once | FliCut does the cutting; removes FliStudio's read of FliHub's config | None known |
| Q10 | **Shadows strip-out** (56 T7 projects) | **Approve the strip-out** already inventoried in `flihub/docs/deprecation/shadow-recordings-inventory.md`; v2 never reads `recording-shadows/` | Ends the Jan-era cluster | Restores of old projects carry dead folders until cleaned |

Smaller yes/no questions are on the review artifact, one per unsure item.

## Live defects found (not fixed: discovery only)

- **H2: the Storage panel's Hold** is answered by `hold.ts:86` (whole-project copy, no local delete). The panel's intended handler, `storage.ts:167` (heavy folders, then local delete), is dead because of mount order (`server/src/index.ts:358` before `:362`). The toast says "Held heavy files to T7". Verified from code and mount order only; the POST was not run because it moves real data.
- **C6:** `GET /api/projects/next-code` writes `projectCodeHighWater` into `server/config.json` (`server/src/routes/index.ts:468`).
- **Styling:** `text-warm-primary` (93 uses) and `text-warm-faint` (62 uses) produce no CSS, because the theme declares `--color-text-warm-*` (`client/src/index.css:23-26`). That text falls back to inherited near-black. Confirmed in a 2026-09-04 build, not in the running app.
- **Tests write the real telemetry file:** 140 of 1,287 lines in `server/transcription-telemetry.jsonl` point at temp test folders.
- **Stray folder:** `server/~/dev/video-projects/v-appydave/{b93,b96}/edits/prep/` was written by an old feature with an unexpanded `~`.
- **Wrong path in a skill:** brand-dave `current-deck` calls `/api/projects/resolve` (should be `/api/query/projects/resolve`).
- **Stale comment:** `POST /api/trash` says it moves to `.trash/`. The code uses `-trash/` like everything else. One of the sub-inventories reported this as two trash folders; checking the code showed only the comment is wrong.

## Look and feel today

- **Palette:** "Warm Linen" (B048, chosen to be camera-friendly because FliHub appears in videos). Canvas `#e8e0d4`, cards `#f5f1eb`, brown text. Stock Tailwind blue is used for active and primary states.
- **Type:** system sans, `font-mono` for filenames, emoji as icons. Only MicCheck has designed type (Oswald + Roboto Mono, "instrument panel").
- **Layout:** one centred 896 px column under a two-row header (breadcrumb, then plain text tabs).
- **Compared with FliStudio:** FliStudio uses the AppyDave tokens (`flistudio/client/src/styles/tokens.css`). FliHub is close but not the same, and it uses blue where the brand uses yellow.

## Artifacts

- **Keep/drop review** (scan and answer, with Copy my answers): https://claude.ai/artifact/HYvB1rML8Axki1D3LKYvRN. Generated from the item list below.
- **Look-and-feel directions** for v2 (A Recording desk · B Take timeline · C Suite sibling): https://claude.ai/artifact/C5tDAED5yB5RXSJsE3dba6

## Item list (55)

Columns: id · area · item · where · verdict · evidence · question/note.


| id | area | item | where | verdict | evidence | question / note |
|---|---|---|---|---|---|---|
| S1 | Capture spine | Ecamm folder watcher + Incoming queue (file:new / file:deleted, replay on connect) | server/src/watcher.ts:9-75 · server/src/index.ts:130-195,396 | **keep** | David 2026-10-28 (B659): "any recordings coming into Ecamm Live go into FliHub". North Star §1 sentence. FR-174 commits 10-25/26. |  |
| S2 | Capture spine | Naming + promote a take (POST /api/rename, suggested naming, NamingControls) | server/src/routes/index.ts:209-318 · client/src/components/NamingControls.tsx | **keep** | North Star §1 "promotes the one you pick". Incoming area: 7 handler commits since June. |  |
| S3 | Capture spine | Incoming card actions: Rename·Keep / Rename·Discard / Discard, Send several, DiscardModal | client/src/components/FileCard.tsx · SendSeveralBar.tsx · DiscardModal.tsx · App.tsx:471 | **keep** | FR-174 shipped 2026-10-25/26 (9e6917e, a00c656, 9d58e4a) from David's live use. |  |
| S4 | Capture spine | Take checks: aspect mismatch + sound-hole (digital-zero dropout) probes | server/src/index.ts:141-170 · utils/aspectCheck.ts · utils/soundHoles.ts:114 | **keep** | Built Sep 23–Oct 4 after real failures; North Star v2 principle "absence and success must never look the same". |  |
| S5 | Capture spine | Trash-incoming to -trash/ (POST /api/trash) | server/src/routes/index.ts:409-445 | **keep** | Part of the record-dislike-record loop (North Star §1). | The route comment says .trash/ but the code uses paths.trash (-trash/). Comment is stale; behaviour is fine. |
| T1 | Takes & chapters | Recordings view by chapter: inline rename, renumber, split, + tag | client/src/components/RecordingsView.tsx (1,744 lines) | **keep** | Most active screen: 19 commits since June (latest 10-12). B659: "route them to chapters and segments". |  |
| T2 | Takes & chapters | Guarded segment ops + undo journal (POST /api/segments/op, preview, undo) | server/src/routes/segments.ts:77-132 · utils/segmentOps.ts:228-244,531,964 | **keep** | CT-0107 (10-08). Refuses while a FliCut cut names the take; the only safe renumber path (AGENT-NOTES). |  |
| T3 | Takes & chapters | Older bulk rename / renumber / swap-chapter tools (/api/manage/*, 12 routes) | server/src/routes/manage.ts:178-1059 | **unsure** | 6 commits since June, but these paths have no FliCut guard and no journal (AGENT-NOTES), and swap-chapters leaves FR-157 titles behind (archaeology). | Fold renumber/swap into guarded segment ops, or keep as power tools? |
| T4 | Takes & chapters | Safe / park a take | client/src/hooks/useRecordingsApi.ts (useMoveToSafe, useParkRecording) · utils/safeMigration.ts | **unsure** | Park is used by Watch (WatchPage). No commit or voice evidence that David parks takes. | Do you park takes, or is trash + keep enough? |
| T5 | Takes & chapters | Chapter + project YouTube titles (FR-157, PUT …/title) | server/src/routes/state.ts · client InlineTitle | **keep** | ylo-titles and ylo-description skills write them; FliStudio reads them (assets.ts:233). |  |
| T6 | Takes & chapters | Ships: one video vs one per chapter (FR-168) | server/src/routes/state.ts · client ShipsSelector | **unsure** | One feature commit (2026-09-08); FliStudio owns video identity now. | Does FliHub still need to know ships, or does FliStudio? |
| T7 | Takes & chapters | Chapter overrides file (.chapter-overrides.json) | server/src/routes/projects.ts:470-512 | **drop** | 0 files on disk across live projects; its UI (ProjectStatsPopup) is never mounted; hooks have zero callers. |  |
| T8 | Takes & chapters | Recently-named strip + in-memory undo rename | client/src/components/RecentlyNamedStrip.tsx · routes/index.ts:672,800-817 | **unsure** | 0 commits since March. Undo is valuable, but the segment journal now covers it durably. | Keep a recently-named strip in v2? |
| T9 | Takes & chapters | Chapter context panel while naming | client/src/components/ChapterContextPanel.tsx · App.tsx:1033 | **unsure** | 0 commits since March; no voice evidence either way. |  |
| W1 | Watch & playback | Watch tab: combined playback, 2× default, chapter/segment cascade, transcript sync | client/src/components/WatchPage.tsx · TranscriptSyncPanel | **keep** | B659: "I can see them all combined together as one long video… really nice video playback… fast, transcript, go to the next one". |  |
| W2 | Watch & playback | Player modals (← / → between takes, Space) + video streaming routes | client/src/components/shared/VideoPlayerModal.tsx:129 · server/src/routes/video.ts | **keep** | Same quote; video routes 4 commits since June. |  |
| W3 | Watch & playback | Dictionary quick-add in the player → fli.words.json | server/src/routes/state.ts:268-304 · DictionaryQuickAdd | **keep** | Project word list 2026-10-04 (editing pass item 16, David). FliCut/FliTools consume the word store. | Data stays in fli-core's word store; FliHub just writes through it. |
| X1 | Transcription | Queue takes to FliTools + pass-2 upgrade poller + transcript follows renames | server/src/routes/transcriptions.ts:184-483 · utils/flitoolsClient.ts:73 · utils/transcriptFollow.ts | **keep** | B584 (David 2026-09-27): FliTools transcribes, FliHub queues. B659: "transcribe them on the fly as I record". 6 commits since June. |  |
| X2 | Transcription | Redo transcript ↻ per take, health / suspect flags | RecordingsView.tsx · transcriptions.ts:291 | **keep** | Shipped 10-12. FliCut tells the user "redo it in FliHub ↻" (flicut transcript-warning.ts:59). |  |
| X3 | Transcription | Transcripts tab (queue + list page) | client/src/components/TranscriptionsPage.tsx | **unsure** | 0 commits since 2026-03-24. FliStudio has a transcription view + queue (capabilities/transcription.ts). | Do you open this tab, or watch progress on the take rows? |
| X4 | Transcription | Transcript viewers + combine-chapter (writes NN-chapter.txt) | TranscriptModal.tsx · VideoTranscriptModal.tsx · transcriptions.ts:739 | **unsure** | No recent commits; FliStudio's video.text gives the best transcript per video. |  |
| X5 | Transcription | Transcription telemetry JSONL (local only) | server/src/utils/telemetry.ts:17-70 | **unsure** | Sends nowhere. 1,287 lines, 140 of them test pollution from temp dirs. |  |
| C1 | Open contract & brand | Open-contract door: POST/GET /api/context, launch args, context:changed, refused banner | server/src/routes/context.ts · utils/openContext.ts · ContextRefusedBanner | **keep** | FliStudio's ONLY live HTTP call into FliHub (flistudio launch/doors.ts:148-168). 4 commits since June. |  |
| C2 | Open contract & brand | In-app brand switcher (GET /api/brands, POST /switch) | client/src/components/BrandSwitcher.tsx · server/src/routes/brands.ts | **unsure** | FliStudio picks the brand and launches FliHub on it. No evidence whether David also switches inside FliHub. | If FliStudio always opens FliHub on the right project, can the switcher go? |
| C3 | Open contract & brand | Project dropdown + pinned projects | App.tsx:497-584 · config.projectPriorities | **unsure** | 2 pinned projects in config. Same question as the brand switcher. |  |
| C4 | Open contract & brand | Projects tab: list, stages, priority, disk scan, new-project form | client/src/components/ProjectsPanel.tsx · NewProjectForm.tsx · routes/projects.ts | **drop** | FliStudio owns project list, create, codes, adopt, rename and the pipeline strip (Projects.tsx, estate/projects.ts). AGENT-NOTES: adoption is FliStudio's job. | Move "open a project" to FliStudio; FliHub keeps a minimal picker at most. |
| C5 | Open contract & brand | Stage overrides + priorities in global server/config.json | server/src/utils/projectStats.ts:160 · config.projectStageOverrides (36) | **drop** | Live finding L5: 47% dead; keyed by bare folder name so they bleed across brands; David shelves by moving the folder, so shelved/archived chips always show zero. |  |
| C6 | Open contract & brand | Project codes high-water + GET /api/projects/next-code (a GET that writes config) | server/src/routes/index.ts:463-468 · utils/nextProjectCode.ts | **drop** | FliStudio allocates codes (estate/projects.ts allocateCode). The stored mark already lags (d05 vs d13). |  |
| C7 | Open contract & brand | Delete a whole project (DELETE /api/projects/:code, type-to-confirm) | server/src/routes/projects.ts:728 · ProjectDeleteModal | **unsure** | Destructive; FliStudio has no delete-project verb. No evidence of use. | Should project delete live in FliStudio, or nowhere? |
| C8 | Open contract & brand | Brand config editor (fli.brand.json publish block) | client/src/components/ConfigPanel.tsx:1063 · utils/managedBrandConfig.ts:33-81 | **drop** | FliStudio's BrandPublishPanel writes the same file. Two writers caused the W8 race; the suite rule is "the owning app is the only writer". |  |
| R1 | Trash | Header trash pill: count + empty -trash/ (shows ? when unreadable) | client TrashIndicator · server/src/routes/projects.ts:665 · utils/safeDelete.ts:83 | **keep** | David ruling 2026-09-23: trash must stay visible and emptiable (AGENT-NOTES). |  |
| H1 | Storage (T7) | Hold / restore / archive / unarchive / batch-offload (17 routes) + Storage panel + T7 pill | server/src/routes/hold.ts · storage.ts · client StoragePanel · SsdIndicator | **unsure** | 1 commit since June. David: "I don't know where to find anything for doing the archives… there's no unified approach." No FliStudio equivalent exists. | Where should hold/archive live: FliHub, FliStudio, or a separate storage tool? |
| H2 | Storage (T7) | Storage panel's Hold button (answered by the wrong handler) | hold.ts:86 shadows storage.ts:167 (mount order index.ts:358/362) · client useStorageApi.ts:77 | **drop** | Verified by code: the panel toasts "Held heavy files to T7" but gets the B064 whole-project copy with no local delete. The storage.ts handler is dead code. | Whatever H1 decides, this duplicate must not be carried. |
| H3 | Storage (T7) | Activity log ~/.flihub/storage-activity.jsonl | server/src/utils/storageActivityLog.ts:23-33 | **unsure** | 1 line on this machine. | Goes with H1. |
| D1 | Deprecated cluster | B-roll lane (FR-161): b-roll/ folder, B-Roll tab, promote branch | routes/index.ts:211-278,557,580 · video.ts:56 · BRollPage.tsx | **drop** | David deprecated it 2026-09-22 (archaeology). | B659's new idea (b-roll as tagged chapter-1 segments) is a different feature: see question Q6. |
| D2 | Deprecated cluster | Chapter video generation (FR-58/131), 4 routes, 2+2 answer 410 | server/src/routes/chapters.ts:35-53 · manage.ts:317 | **drop** | Already 410 since 2026-09-15. |  |
| D3 | Deprecated cluster | FR-126 edit-folder manifest | server/src/utils/editManifest.ts:199-243 · developer.ts:57 | **drop** | Zero writers; setEditManifest has zero callers; useManifestStatus has zero callers. |  |
| D4 | Deprecated cluster | Edit folders create (edit-1st/2nd/final) | server/src/routes/edit.ts:118,147 | **drop** | Never defined in code (docs/architecture/edit-folders.md); FliCut now owns first/second/final edits. |  |
| D5 | Deprecated cluster | recording-shadows/ residual handling | utils/renameRecording.ts · utils/storageTree.ts:23 | **unsure** | 56 T7 projects still have shadow folders. AGENT-NOTES: don't touch until David rules on the strip-out. | Rule on the shadow strip-out (inventory ready in docs/deprecation/). |
| D6 | Deprecated cluster | Startup -safe/ migration (FR-111) | server/src/index.ts:416-433 · utils/safeMigration.ts | **unsure** | No -safe/ left locally; 2 legacy T7 projects still have one and would trip it on restore. |  |
| A1 | Other tabs | Assets tab: assign images to chapter slots, prompts, clipboard paste (12 routes, 2 watchers) | server/src/routes/assets.ts · client AssetsPage.tsx (1,462 lines) | **unsure** | 0 commits since March. FliStudio has resources/assets. The flihub skill's images-command still reads /api/query/…/images. | Still used? If yes, FliHub or FliStudio? |
| A2 | Other tabs | Thumbs tab: import thumbnails from a ~/Downloads zip, reorder (8 routes, zip watcher) | server/src/routes/thumbs.ts · ThumbsPage.tsx | **drop** | 0 commits since March. FliStudio owns thumbnails (ThumbPool, launch/publish). |  |
| A3 | Other tabs | Inbox tab + POST /api/projects/:code/inbox/write | server/src/routes/projects.ts:787-791 · InboxPage.tsx | **unsure** | 0 commits since March, but the flihub skill's write-command still writes here. | Retire the inbox in favour of FliStudio resources? |
| A4 | Other tabs | Final media + YouTube chapter SRT + LLM chapter verify (6 routes) | server/src/routes/projects.ts · utils/finalMedia.ts · llmVerification.ts | **drop** | Only UI was ProjectStatsPopup, which is never mounted. FliStudio publish/launch owns chapters and finals. |  |
| A5 | Other tabs | POEM WUI / AWB / YLO send (7 routes, PoemWuiPage) | server/src/routes/poem-wui.ts · client PoemWuiPage | **unsure** | 0 UI commits. YLO is now a Claude plugin; the brand-config part moved to FliStudio (C8). | Do you still send to POEM/AWB/YLO from FliHub? |
| A6 | Other tabs | Gling edit prep + glingDictionary | server/src/routes/edit.ts:72-76 · config.glingDictionary (24 words) | **unsure** | FliCut now cuts (B659). But FliStudio's words.import-flihub reads glingDictionary from FliHub's config. | Is Gling retired? If so, import the 24 words into fli.words once, then drop. |
| A7 | Other tabs | MicCheck tab + server API + query + skill command | client MicCheckPage.tsx · server/src/routes/miccheck.ts · utils/micCheckStore.ts | **unsure** | Built 2026-08-26..29; 3 saved sessions. North Star: it was portable for 4 hours, then coupled. Could live in Teletubby's setup panel. | Keep MicCheck in FliHub, or move it? |
| V1 | Dev tools & config | API Explorer + hand-written apiRegistry | client/src/components/ApiExplorer.tsx · shared/apiRegistry.ts | **drop** | Lists 34 of 165 routes. A generated OpenRPC door replaces it by design. |  |
| V2 | Dev tools & config | Mockups page | client/src/components/MockupsPage.tsx | **drop** | Static links; two cards point at removed features (Sync Hub, Relay). |  |
| V3 | Dev tools & config | Developer drawer (state / config / telemetry JSON viewer) | client/src/components/DeveloperDrawer.tsx · routes/developer.ts | **unsure** | 0 commits since March. The door's read verbs would cover it. |  |
| V4 | Dev tools & config | Config: directories + recording names (watchDirectory, commonNames, availableTags, imageSourceDirectory) | ConfigPanel.tsx:602,809 · configManager.ts:116-158 | **keep** | Live fields read by the watcher and naming UI. | imageSourceDirectory goes with A1. |
| V5 | Dev tools & config | Dead config: fileExtensions, whisper*, chapterRecordings, machineRole, CLIENT_URL env | shared/types.ts:66-93 · configManager.ts · config/env.ts:8 | **drop** | Read by nothing (config inventory). |  |
| V6 | Dev tools & config | Read-only query API /api/query/* (15 routes) | server/src/routes/query/* | **keep** | The flivideo:flihub skill (12 command docs), brand-dave gather/current-deck and the teletubby skill call it. | In v2 these become door verbs; skills are re-pointed. |
| V7 | Dev tools & config | Dead socket events file:renamed / file:error | shared/types.ts:542-585 · client useSocket.ts:60,95 | **drop** | Declared and subscribed, never emitted. |  |
| V8 | Dev tools & config | Header ··· actions (copy path, open in Finder) + connection dot | App.tsx:509-539,1026 · routes/system.ts | **keep** | Small, used on every project; FliStudio has path.reveal for the same need. |  |


---

# Appendices: raw inventories (file:line)

Produced by four read-only sub-inventories on 2026-10-30 and checked by spot-checks. One claim was found wrong and is corrected in the defects section: the "two trash folders" claim (`.trash/` vs `-trash/`). Paths are relative to `/Users/davidcruwys/dev/ad/flivideo/flihub` unless absolute.


## Appendix A. Server: routes, mounts, sockets

Generated 2026-10-30, read-only, from `/Users/davidcruwys/dev/ad/flivideo/flihub` at `061ae34`. Route files: `server/src/routes/` (paths below are relative to it). Mounts: `server/src/index.ts:276-385`.

**Method**: every `router.<verb>(` in `server/src/routes/**/*.ts` (non-test) was extracted by script; full path = mount prefix + route path. Purpose comes from the JSDoc/comment above each handler; mutation was classified by scanning the handler body for fs/rsync/state/config writes and then hand-checked for every non-GET. Not checked: mutation inside called utils beyond the names visible in the handler (e.g. `finishSession`, `applySegmentOp` were read by name, not traced in full).

**Totals**: 165 routes (74 GET, 91 mutating verbs) across 24 areas. 19 route files + 9 query files. No routes registered directly on `app` (only `app.use`).

### Mount table (order matters: first match wins)

| # | index.ts line | Prefix | Router file |
|---|---|---|---|
| 1 | 276 | `/api/transcriptions` | transcriptions.ts |
| 2 | 290 | `/api` | index.ts (createRoutes) |
| 3 | 294 | `/api/assets` | assets.ts |
| 4 | 298 | `/api/thumbs` | thumbs.ts |
| 5 | 303 | `/api/system` | system.ts |
| 6 | 313 | `/api/projects` | projects.ts |
| 7 | 317 | `/api/query` | query/index.ts |
| 8 | 321 | `/api/chapters` | chapters.ts |
| 9 | 325 | `/api/video` | video.ts |
| 10 | 329 | `/api/edit` | edit.ts |
| 11 | 339 | `/api/manage` | manage.ts |
| 12 | 342 | `/api/segments` | segments.ts |
| 13 | 346 | `/api/poem-wui` | poem-wui.ts |
| 14 | 350 | `/api` | state.ts |
| 15 | 354 | `/api/developer` | developer.ts |
| 16 | 358 | `/api/projects` | hold.ts |
| 17 | 362 | `/api/projects` | storage.ts |
| 18 | 367 | `/api/miccheck` | miccheck.ts |
| 19 | 370 | `/api/brands` | brands.ts |
| 20 | 385 | `/api/context` | context.ts |

Note: `/api/projects/*` is served by FOUR routers: `index.ts` (at `/api`, line 290: `GET /projects/next-code`, `POST /projects`), `projects.ts` (313), `state.ts` (at `/api`, line 350: `/projects/:code/state|words|title|ships|chapters/:chapter/title`), `hold.ts` (358), `storage.ts` (362).

### Duplicates / shadowing

| Path | Winner | Dead | Notes |
|---|---|---|---|
| `POST /api/projects/:code/hold` | `hold.ts:86` (B064 whole-project rsync to T7 holding, mount 358) | `storage.ts:167` (storage-panel WU1 transactional two-pass hold of heavy subfolders + local rm, mount 362) | hold.ts handler always responds (never `next()`), so storage.ts's version is unreachable. Matches AGENT-NOTES. The storage-panel UI therefore gets B064 semantics (copy only, no local delete) when it calls Hold. |

No other method+path collisions after normalising params. Checked param-vs-literal shadowing too (`/api/query/projects/resolve` is declared before `/:code`; `query/transcripts` `/chapters/:chapterName/srt` before `/:recording/srt`; `/api/projects/disk/scan-all` has no earlier 2-segment POST) — none found.

**Functional overlaps (different paths, same job)** — candidates for a rebuild to collapse:

- Chapter rename: `POST /api/recordings/rename-chapter` (index.ts:1251) vs `POST /api/manage/rename-chapter` (manage.ts:438).
- Undo rename: `POST /api/recordings/undo-rename` (index.ts:741, FR-50) vs `POST /api/manage/undo-rename` (manage.ts:812, B047) vs `POST /api/segments/undo` (segments.ts:106, journalled).
- Renumber: `POST /api/manage/renumber-chapter` (manage.ts:748) and `/api/rename` Seq vs `POST /api/segments/op` — AGENT-NOTES says only `/api/segments/op` is guarded+journalled.
- Delete transcripts: `DELETE /api/manage/delete-transcripts` (manage.ts:326) vs `DELETE /api/transcriptions/transcript/:filename` (transcriptions.ts:597).
- Trash: `POST /api/trash` (index.ts:409, `.trash/`) vs `POST /api/recordings/trash` (index.ts:1157, `-trash/`) — **[CORRECTED: the code uses `-trash/` for both; only the comment says `.trash/`]**
- Config read: `GET /api/config`, `GET /api/developer/config`, `GET /api/query/config`.
- Chapters (YouTube timestamps): `GET /api/projects/:code/chapters` vs `GET /api/query/projects/:code/chapters`.
- Transcript text: `GET /api/transcriptions/combined`, `GET /api/query/projects/:code/transcript/text`, `GET /api/poem-wui/status`.
- Hold/archive: hold.ts (B064, 10 routes) and storage.ts (WU1, 7 routes) are two generations of the same T7 feature, both live.

### Area summary

| Area | Routes | Mutating | Route files | Commits since 2026-06-01 touching these handlers (`git log -L`) | Commits to the whole file(s) since 2026-06-01 | Last touched (handler) | Last commit subject | Deprecation |
|---|---|---|---|---|---|---|---|---|
| incoming / naming / promotion | 5 | 2 | index.ts | 7 | 19 | 2026-10-12 | fix(transcription): the job follows the take — a rename mid-transcription no longer strand | `/api/rename` has b-roll branch; shadow gen removed 2026-09-04 |
| config | 2 | 1 | index.ts | 2 | 19 | 2026-09-22 | refactor: remove git sync (Sync Hub) and relay collaboration |  |
| recordings management | 10 | 8 | index.ts | 11 | 19 | 2026-10-12 | fix(transcription): the job follows the take — a rename mid-transcription no longer strand |  |
| b-roll (FR-161, deprecated) | 2 | 1 | index.ts | 2 | 19 | 2026-09-04 | feat(FR-161): b-roll lane — chapter-less sibling folder, promote from Incoming, B-Roll tab | DEPRECATED (David 2026-09-22, archaeology §cluster) |
| segments (CT-0107) | 5 | 3 | segments.ts | 4 | 5 | 2026-10-08 | D07-UAT-1: read-only segment op preview (POST /api/segments/preview) |  |
| manage (bulk rename/chapters) | 12 | 9 | manage.ts | 6 | 6 | 2026-10-12 | fix(manage): takes moved to another chapter are numbered from that chapter | regen-chapters/regen-all 410 |
| project state / words / titles | 9 | 7 | state.ts | 3 | 3 | 2026-10-04 | feat(words): project-level word list — "remember for this video" (editing pass item 16, fl |  |
| projects (registry/stats/stage/delete/disk/trash) | 10 | 6 | index.ts, projects.ts | 10 | 21 | 2026-10-05 | fix(trash): the header trash counts and empties subfolders of -trash/, matching FliStudio |  |
| inbox | 1 | 1 | projects.ts | 0 | 6 | - |  |  |
| transcriptions | 11 | 4 | projects.ts, transcriptions.ts | 6 | 13 | 2026-10-12 | feat(transcripts): Redo transcript (↻) on each recording row; T⚠ names words that go back  |  |
| final media + YouTube chapters (SRT) | 6 | 2 | projects.ts | 0 | 6 | - |  |  |
| chapter video generation (410, deprecated) | 4 | 0 | chapters.ts | 2 | 2 | 2026-09-15 | fix(W3): F8 remove chapter-preview leftovers; PUT /api/chapters/config answers 410 | 2 of 4 return 410; roadmap §1.2e |
| assets/images | 12 | 7 | assets.ts | 0 | 0 | - |  |  |
| thumbs | 8 | 4 | thumbs.ts | 0 | 0 | - |  |  |
| video streaming | 3 | 0 | video.ts | 4 | 4 | 2026-09-22 | refactor: remove git sync (Sync Hub) and relay collaboration | b-roll folder in allow-list |
| edit folders | 3 | 2 | edit.ts | 2 | 2 | 2026-10-04 | feat(words): project-level word list — "remember for this video" (editing pass item 16, fl | edit-1st/2nd undefined in code (docs/architecture/edit-folders.md) |
| hold/archive/storage/T7 | 17 | 11 | hold.ts, storage.ts | 1 | 1 | 2026-09-22 | refactor: remove git sync (Sync Hub) and relay collaboration | 1 dead duplicate |
| brands | 2 | 1 | brands.ts | 2 | 2 | 2026-09-15 | fix(W3): F2 the brand switcher resolves roots like doors 2/3 (resolveBrandRoot) |  |
| context / open-contract | 2 | 1 | context.ts | 4 | 5 | 2026-09-22 | chore(open-contract): pin @flivideo/core v0.3.0 — videos are named, not numbered (D15) |  |
| miccheck | 9 | 2 | miccheck.ts, query/miccheck.ts | 2 | 2 | 2026-08-26 | feat(miccheck): server API — live stream + persisted session reports |  |
| poem-wui / YLO | 7 | 1 | poem-wui.ts | 2 | 2 | 2026-10-29 | Pin @flivideo/core v0.26.0-rc.1; fli.brand.json writes are locked and versioned (W8) |  |
| developer | 3 | 0 | developer.ts | 0 | 0 | - |  | exposes FR-126 editManifest (deprecated, zero writers) |
| system | 7 | 0 | system.ts | 2 | 2 | 2026-09-22 | refactor: remove git sync (Sync Hub) and relay collaboration |  |
| query (read-only, /api/query) | 15 | 0 | query/chapters.ts, query/export.ts, query/images.ts, query/inbox.ts, query/index.ts, query/projects.ts, query/recordings.ts, query/transcripts.ts | 4 | 4 | 2026-09-08 | feat(FR-168): ships — declare whether a project makes one video or one per chapter |  |
| **Total** | **165** | | | | | | | |

Commit counts: column 5 is per-handler line range (`git log -L <start>,<end>:<file>`, handler = its line to the line before the next route), union of hashes per area; column 6 is `git log -- <file>` for the whole route file(s), so shared files (index.ts, projects.ts) inflate it. Neither counts changes in `server/src/utils/*` that a handler calls.

### Routes by area

### incoming / naming / promotion (5)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/suggested-naming` | index.ts:139 | FR-4: GET /api/suggested-naming - Calculate next chapter/segment based on existing files / NFR-6: Using projectDirectory with getProjectPaths() | no |  |  |
| GET | `/api/files` | index.ts:203 | GET /api/files - List pending files | no |  |  |
| POST | `/api/rename` | index.ts:209 | POST /api/rename - Rename and move a file | YES: moves Ecamm take into recordings/ (or b-roll/), writes .flihub-state.json, queues transcription | recordings:changed | FR-161 b-roll branch inside |
| DELETE | `/api/files/:encodedPath` | index.ts:398 | DELETE /api/files/:path - Remove a file from pending (discard without renaming) | no (in-memory pending list only) |  |  |
| POST | `/api/trash` | index.ts:409 | FR-5: POST /api/trash - Move file to .trash/ directory in target folder | YES: moves file to -trash/ (comment says .trash/; corrected) |  |  |

### config (2)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/config` | index.ts:133 | GET /api/config - Get current configuration | no |  |  |
| POST | `/api/config` | index.ts:173 | POST /api/config - Update configuration / FR-89: Support all config fields including split project directory / FR-116: Support common names editing | YES: config.json |  |  |

### recordings management (10)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/recordings` | index.ts:609 | FR-14: GET /api/recordings - List all recordings in project's recordings directory / NFR-6: Using projectDirectory with getProjectPaths() / FR-111 Phase 3: Rewritten to u | no |  |  |
| GET | `/api/recordings/recent-renames` | index.ts:725 | FR-50: GET /api/recordings/recent-renames - Get recent renames for undo | no |  |  |
| POST | `/api/recordings/undo-rename` | index.ts:741 | FR-50: POST /api/recordings/undo-rename - Undo a recent rename | YES: renames recording back, trashes transcripts |  |  |
| POST | `/api/recordings/safe` | index.ts:853 | FR-15: POST /api/recordings/safe - Mark file(s) as safe / FR-111 Phase 3: Rewritten to use state file instead of moving files | YES: state file (safe flag) | recordings:changed |  |
| POST | `/api/recordings/restore` | index.ts:932 | FR-15: POST /api/recordings/restore - Restore file(s) from safe state / FR-111 Phase 3: Rewritten to use state file instead of moving files | YES: state file (unsafe) | recordings:changed |  |
| POST | `/api/recordings/aspect-dismiss` | index.ts:990 | Aspect warning: POST /api/recordings/aspect-dismiss { files: string[] } — hide the warning on / these recordings (kept in state with dismissedAt). Reports which files had | YES: state file (aspect dismissedAt) | recordings:changed |  |
| POST | `/api/recordings/park` | index.ts:1019 | FR-120: POST /api/recordings/park - Mark file(s) as parked | YES: state file (parked) | recordings:changed |  |
| POST | `/api/recordings/unpark` | index.ts:1097 | FR-120: POST /api/recordings/unpark - Restore file(s) from parked state | YES: state file (unpark) | recordings:changed |  |
| POST | `/api/recordings/trash` | index.ts:1157 | FR-156: POST /api/recordings/trash - Move recording(s) and every sibling / artifact (transcripts) into -trash/. / Pass dryRun: true to get the same discovery result witho | YES: moves recording + transcripts to -trash/, state file (dryRun option) | recordings:changed,transcripts:changed |  |
| POST | `/api/recordings/rename-chapter` | index.ts:1251 | FR-47/FR-130: POST /api/recordings/rename-chapter - Rename the label for all files in a chapter / Simplified using delete+regenerate pattern (152 lines → ~80 lines) | YES: renames all files in a chapter (+transcripts/state keys) |  |  |

### b-roll (FR-161, deprecated) (2)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/broll` | index.ts:557 | FR-161: GET /api/broll — list the current project's b-roll files | no |  | FR-161 b-roll |
| DELETE | `/api/broll/:filename` | index.ts:580 | FR-161: DELETE /api/broll/:filename — move to -trash/ (recoverable) | YES: moves b-roll file to -trash/ |  | FR-161 b-roll |

### segments (CT-0107) (5)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| POST | `/api/segments/op` | segments.ts:75 | POST /api/segments/op — `{ mode, chapter, segment / before, source? / sources?, name?, tags?, direction? }`. */ | YES: renumber/replace/insert/delete takes, journal .flihub-segment-journal.json, may queue transcription | recordings:changed |  |
| POST | `/api/segments/preview` | segments.ts:96 |  / POST /api/segments/preview — the same body as /op: what it would trash and renumber, or the same refusal (409); / nothing on disk changes. A confirmation shows this, s | no (dry preview) |  |  |
| POST | `/api/segments/undo` | segments.ts:106 | POST /api/segments/undo — `{ id? }`: the latest change, from the journal on disk (survives a restart). */ | YES: reverts journalled segment op | recordings:changed |  |
| POST | `/api/segments/placeholder` | segments.ts:117 | POST /api/segments/placeholder — `{ filename, placeholder }`: R7, mark a segment to re-record (state only). */ | YES: state file (placeholder flag) | recordings:changed |  |
| GET | `/api/segments/journal` | segments.ts:140 | GET /api/segments/journal — the project's segment changes, newest first. */ | no |  |  |

### manage (bulk rename/chapters) (12)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/manage/recordings-folder-path` | manage.ts:50 |  / GET /api/manage/recordings-folder-path / FR-141: Returns the recordings folder path for the current project /  | no |  |  |
| POST | `/api/manage/bulk-rename` | manage.ts:84 | Returns: / { / success: boolean; / renamedCount: number; / transcriptionQueued: boolean; / files: Array<{ old: string; new: string }>; / errors?: Array<{ file: string; er | YES: renames recordings (+sweep), queues transcription |  |  |
| POST | `/api/manage/regen-transcripts` | manage.ts:246 |  / Returns: / { / success: boolean; / queued: number; / total: number; / force: boolean; / } /  | YES: queues FliTools transcriptions (overwrites transcripts) |  |  |
| POST | `/api/manage/regen-chapters` | manage.ts:317 |  / POST /api/manage/regen-chapters, POST /api/manage/regen-all — 410 Gone. / Both made chapter preview videos (FR-58/FR-131), deprecated by FliStudio roadmap §1.2e. / Exi | no (410) |  | 410 Gone |
| POST | `/api/manage/regen-all` | manage.ts:317 |  / POST /api/manage/regen-chapters, POST /api/manage/regen-all — 410 Gone. / Both made chapter preview videos (FR-58/FR-131), deprecated by FliStudio roadmap §1.2e. / Exi | no (410) |  | 410 Gone |
| DELETE | `/api/manage/delete-transcripts` | manage.ts:326 |  / DELETE /api/manage/delete-transcripts / Delete transcript files (.txt, .srt, .json) for the current project. / Body: { files?: string[] } — recording filenames; omit f | YES: deletes transcript .txt/.srt/.json |  |  |
| DELETE | `/api/manage/delete-subfolder` | manage.ts:379 |  | YES: deletes a recordings subfolder |  |  |
| POST | `/api/manage/rename-chapter` | manage.ts:438 | } /  / Returns: / { / success: boolean; / filesRenamed: number; / error?: string; / } /  | YES: renames chapter label across files | recordings:changed |  |
| POST | `/api/manage/swap-chapters` | manage.ts:570 | } /  / Returns: / { / success: boolean; / filesSwapped: number; / error?: string; / } /  | YES: swaps two chapters (renames) | recordings:changed |  |
| POST | `/api/manage/renumber-chapter` | manage.ts:748 |  / POST /api/manage/renumber-chapter / Close the gaps in one chapter's sequence numbers: 03-2, 03-3 → 03-1, 03-2. Names and tags are / kept; order is the current sequence | YES: renumbers sequences in a chapter | recordings:changed |  |
| POST | `/api/manage/undo-rename` | manage.ts:812 | B047: Undo the last bulk rename operation /  / Returns: / { / success: boolean; / filesReverted: number; / error?: string; / } /  | YES: reverts last bulk rename | recordings:changed |  |
| POST | `/api/manage/split-chapter` | manage.ts:879 |  / Body: / { / chapter: string;          // source chapter, e.g. "04" / splitAtSequence: number;  // files with seq >= this move to new chapter / } /  / Returns: SplitCha | YES: renames files into new chapter | recordings:changed |  |

### project state / words / titles (9)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/projects/:code/state` | state.ts:66 | GET /api/projects/:code/state / Read project state file /  / Returns: / - { success: true, state: ProjectState } / - { success: false, error: string } on error /  / If st | no |  |  |
| POST | `/api/projects/:code/state` | state.ts:117 | Update project state file /  / Request body: { recordings: Record<string, RecordingState> } / Merges with existing state (doesn't replace entirely) /  / Returns: / - { su | YES: merges into .flihub-state.json | recordings:changed |  |
| PATCH | `/api/projects/:code/state/dictionary` | state.ts:190 | PATCH /api/projects/:code/state/dictionary / FR-118: Update project-specific Gling dictionary /  / Request body: { words: string[] } /  / Returns: / - { success: true, wo | YES: state file (dictionary) | recordings:changed |  |
| GET | `/api/projects/:code/words` | state.ts:268 | project-level words only, never brand or global). Writes go through fli-core's one locked write path, the same / code FliStudio's words.add uses, so it works with FliStud | no |  |  |
| POST | `/api/projects/:code/words` | state.ts:288 |  | YES: project words file via fli-core locked write |  |  |
| DELETE | `/api/projects/:code/words` | state.ts:298 |  | YES: project words file via fli-core locked write | recordings:changed |  |
| PUT | `/api/projects/:code/title` | state.ts:343 |  / PUT /api/projects/:code/title / FR-157: Set the project-level YouTube title. Body: { title: string } ('' clears) /  | YES: state file (title) | projects:changed |  |
| PUT | `/api/projects/:code/ships` | state.ts:373 |  / PUT /api/projects/:code/ships / FR-168: set the render grain. Body: { ships: 'per-project' / 'per-chapter' } / Required as well as the create-time selector, because BO | YES: state file (ships) | projects:changed,recordings:changed |  |
| PUT | `/api/projects/:code/chapters/:chapter/title` | state.ts:405 |  / PUT /api/projects/:code/chapters/:chapter/title / FR-157: Set a chapter's YouTube title. Body: { title: string } ('' clears) /  | YES: state file (chapter title) | recordings:changed |  |

### projects (registry/stats/stage/delete/disk/trash) (10)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/projects/next-code` | index.ts:463 | FR-12: POST /api/projects - Create a new AppyDave video project / FR-163: Next project code — highest ever issued + 1, per root (D1/D2) | YES (side effect on a GET): may raise projectCodeHighWater in config.json |  |  |
| POST | `/api/projects` | index.ts:477 |  | YES: mkdir project folder, config.json, state file |  |  |
| GET | `/api/projects/stats` | projects.ts:103 | GET /api/projects/stats - Get extended stats for all projects | no |  |  |
| PUT | `/api/projects/:code/priority` | projects.ts:143 | PUT /api/projects/:code/priority - Update project priority (pin/unpin) | YES: config.json (priority) |  |  |
| PUT | `/api/projects/:code/stage` | projects.ts:189 | PUT /api/projects/:code/stage - Update project stage (manual override) / FR-80: Updated to support new 8-stage workflow | YES: config.json (stage override) |  |  |
| POST | `/api/projects/disk/scan-all` | projects.ts:524 | B062: POST /api/projects/disk/scan-all — Scan all projects and populate the disk size cache | in-memory disk cache only |  |  |
| GET | `/api/projects/:code/disk` | projects.ts:571 | B062: GET /api/projects/:code/disk — Get disk size for a single project (cache-first) | in-memory disk cache only |  |  |
| GET | `/api/projects/:code/trash` | projects.ts:605 | Trash visibility (David, 2026-09-23: -trash/ is allowed only if it is ALWAYS visible and / emptiable any time). GET /api/projects/:code/trash — read -trash/ fresh on ever | no |  |  |
| DELETE | `/api/projects/:code/trash` | projects.ts:651 | B062 Wave 2: Delete trash folder contents for a project | YES: empties project -trash/ |  |  |
| DELETE | `/api/projects/:code` | projects.ts:683 | FR-152: DELETE /api/projects/:code — Permanently delete a project's local directory / Guard 1: confirmationCode must match project code exactly | YES DANGER: rm -r local project dir (confirmationCode) | projects:changed |  |

### inbox (1)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| POST | `/api/projects/:code/inbox/write` | projects.ts:742 | FR-59: POST /api/projects/:code/inbox/write - Write file to inbox subfolder | YES: writes file into inbox/<sub>/ |  |  |

### transcriptions (11)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/projects/:code/transcript-sync` | projects.ts:243 | FR-48: GET /api/projects/:code/transcript-sync - Get detailed transcript sync status | no |  |  |
| GET | `/api/transcriptions` | transcriptions.ts:498 | === API Routes === / GET /api/transcriptions - Get all transcription state | no |  |  |
| GET | `/api/transcriptions/status/:filename` | transcriptions.ts:507 | GET /api/transcriptions/status/:filename - Get status for specific file | no |  |  |
| GET | `/api/transcriptions/transcript/:filename` | transcriptions.ts:535 | GET /api/transcriptions/transcript/:filename - Get transcript content / FR-94: Supports ?format=txt/srt query param, defaults to txt if available | no |  |  |
| DELETE | `/api/transcriptions/transcript/:filename` | transcriptions.ts:597 | FR-48: DELETE /api/transcriptions/transcript/:filename - Delete orphaned transcript / Supports optional ?project=code query param to delete from a specific project | YES: deletes orphaned transcript files |  |  |
| POST | `/api/transcriptions/queue` | transcriptions.ts:635 | POST /api/transcriptions/queue - Manually queue a transcription | YES: queues FliTools job (writes transcripts later) |  |  |
| GET | `/api/transcriptions/chapter-status/:chapter` | transcriptions.ts:664 | Enhancement B: GET /api/transcriptions/chapter-status/:chapter - Check chapter transcript status | no |  |  |
| POST | `/api/transcriptions/combine-chapter` | transcriptions.ts:695 | Enhancement B: POST /api/transcriptions/combine-chapter - Combine all chapter transcripts | YES: writes combined chapter transcript |  |  |
| POST | `/api/transcriptions/queue-all` | transcriptions.ts:763 | FR-30 Enhancement: POST /api/transcriptions/queue-all - Queue transcription for all videos / FR-94: Only transcribe real recordings | YES: queues all untranscribed |  |  |
| GET | `/api/transcriptions/pending-count` | transcriptions.ts:842 | FR-92: GET /api/transcriptions/pending-count - Count files needing transcription | no |  |  |
| GET | `/api/transcriptions/combined` | transcriptions.ts:884 | FR-55: GET /api/transcriptions/combined - Get combined transcript for entire video | no |  |  |

### final media + YouTube chapters (SRT) (6)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/projects/:code/final` | projects.ts:287 | GET /api/projects/:code/final - Get final video and SRT info for a project | no |  |  |
| GET | `/api/projects/:code/chapters` | projects.ts:308 | GET /api/projects/:code/chapters - FR-34: Extract chapter timestamps from SRT | no |  |  |
| POST | `/api/projects/:code/chapters/verify` | projects.ts:347 | POST /api/projects/:code/chapters/verify - FR-34 Enhancement: Verify chapter with LLM | no disk; calls LLM |  |  |
| GET | `/api/projects/:code/chapters/overrides` | projects.ts:385 | GET /api/projects/:code/chapters/overrides - Get all chapter overrides for a project | no |  |  |
| POST | `/api/projects/:code/chapters/override` | projects.ts:405 | POST /api/projects/:code/chapters/override - Set a chapter override | YES: writes chapter override JSON |  |  |
| DELETE | `/api/projects/:code/chapters/override/:chapter/:name` | projects.ts:483 | DELETE /api/projects/:code/chapters/override/:chapter/:name - Remove a chapter override | YES: writes chapter override JSON |  |  |

### chapter video generation (410, deprecated) (4)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/chapters/config` | chapters.ts:39 | GET /api/chapters/config - Get chapter recording configuration | no |  |  |
| PUT | `/api/chapters/config` | chapters.ts:48 | PUT /api/chapters/config - 410 Gone (roadmap §1.2e): nothing reads these settings any more | no (verify) |  | 410 Gone |
| POST | `/api/chapters/generate` | chapters.ts:53 | POST /api/chapters/generate - 410 Gone (roadmap §1.2e) | no (verify) |  | 410 Gone |
| GET | `/api/chapters/status` | chapters.ts:58 | GET /api/chapters/status - Existing chapter recordings (legacy) and the chapters available | no |  |  |

### assets/images (12)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/assets/incoming` | assets.ts:42 | GET /api/assets/incoming - Scan image source directory for pending images | no |  |  |
| GET | `/api/assets/images` | assets.ts:106 | GET /api/assets/images - List existing images and prompts in project's assets/images/ / NFR-6: Using projectDirectory with getProjectPaths() | no |  |  |
| GET | `/api/assets/next-image-order` | assets.ts:181 | GET /api/assets/next-image-order - Calculate next available image order / FR-22: Also considers prompt files when calculating next order / NFR-6: Using projectDirectory w | no |  |  |
| POST | `/api/assets/assign` | assets.ts:230 | POST /api/assets/assign - Assign (rename and move) an image to the project | YES: moves incoming image into assets/images/ (rename+move) |  |  |
| DELETE | `/api/assets/incoming/:encodedPath` | assets.ts:367 | DELETE /api/assets/incoming/:encodedPath - Remove an incoming image (move to trash) | YES: moves incoming image to trash |  |  |
| GET | `/api/assets/image/:encodedPath` | assets.ts:392 | GET /api/assets/image/:encodedPath - Serve an image file (for thumbnails) | no |  |  |
| POST | `/api/assets/prompt` | assets.ts:428 | FR-22: POST /api/assets/prompt - Create, update, or delete a prompt file / FR-38: If content is empty, delete the prompt file (Option A) | YES: writes/deletes prompt .txt in assets/images/ |  |  |
| GET | `/api/assets/prompt/:filename` | assets.ts:570 | FR-22: GET /api/assets/prompt/:filename - Read a prompt file for editing / NFR-6: Using projectDirectory with getProjectPaths() | no |  |  |
| DELETE | `/api/assets/prompt/:filename` | assets.ts:613 | FR-38: DELETE /api/assets/prompt/:filename - Delete a prompt file (Option B) | YES: deletes prompt file |  |  |
| DELETE | `/api/assets/images/:filename` | assets.ts:650 | FR-49: DELETE /api/assets/images/:filename - Delete an assigned image (move to -trash/) | YES: moves assigned image to -trash/ |  |  |
| POST | `/api/assets/clipboard/assign` | assets.ts:700 | FR-42: POST /api/assets/clipboard/assign - Save clipboard image directly to assets/images/ | YES: writes clipboard PNG into assets/images/ |  |  |
| POST | `/api/assets/clipboard/incoming` | assets.ts:781 | FR-42: POST /api/assets/clipboard/incoming - Save clipboard image to incoming folder | YES: writes clipboard PNG into image source (incoming) dir |  |  |

### thumbs (8)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/thumbs/zips` | thumbs.ts:83 | GET /api/thumbs/zips - List ZIP files in ~/Downloads that contain images | no |  |  |
| GET | `/api/thumbs/zip/:filename/contents` | thumbs.ts:127 | GET /api/thumbs/zip/:filename/contents - Preview images in a ZIP file | no |  |  |
| POST | `/api/thumbs/import` | thumbs.ts:178 | POST /api/thumbs/import - Import selected images from a ZIP file | YES: extracts ZIP images into assets/thumbs/ |  |  |
| GET | `/api/thumbs` | thumbs.ts:251 | GET /api/thumbs - List current thumbnails in assets/thumbs/ | no |  |  |
| GET | `/api/thumbs/image/:filename` | thumbs.ts:296 | GET /api/thumbs/image/:filename - Serve a thumbnail image | no |  |  |
| POST | `/api/thumbs/reorder` | thumbs.ts:319 | POST /api/thumbs/reorder - Rename files to match new order | YES: renames thumbs to new order |  |  |
| DELETE | `/api/thumbs/zip/:filename` | thumbs.ts:369 | DELETE /api/thumbs/zip/:filename - Delete a ZIP file from Downloads | YES: deletes ZIP in ~/Downloads |  |  |
| DELETE | `/api/thumbs/:filename` | thumbs.ts:402 | DELETE /api/thumbs/:filename - Delete a thumbnail and renumber remaining | YES: deletes thumb + renumbers rest |  |  |

### video streaming (3)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/video/:projectCode/:folder/:filename` | video.ts:41 |  / GET /:projectCode/:folder/:filename / Stream a video file from a project's recordings directory / Supports Range requests for seeking /  / folder: 'recordings' or '-ch | no |  | folder allow-list includes b-roll (FR-161) |
| GET | `/api/video/recordings/:filename` | video.ts:150 |  / FR-128: GET /recordings/:filename / Stream a recording from the current project's recordings folder / Supports Range requests for seeking /  | no |  |  |
| GET | `/api/video/incoming/:filename` | video.ts:231 |  / FR-106: GET /incoming/:filename / Stream an incoming video file from the watch directory / Supports Range requests for seeking /  | no |  |  |

### edit folders (3)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/edit/prep` | edit.ts:15 | GET /api/edit/prep - Get edit prep data | no |  |  |
| POST | `/api/edit/create-folders` | edit.ts:106 | POST /api/edit/create-folders - Create all edit folders | YES: mkdir edit folders in project |  |  |
| POST | `/api/edit/create-folder` | edit.ts:128 | FR-124: POST /api/edit/create-folder - Create a single edit folder | YES: mkdir one edit folder |  |  |

### hold/archive/storage/T7 (17)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/projects/ssd-status` | hold.ts:35 | B064: GET /api/projects/ssd-status / Global SSD mount check — no project code needed. Used by header indicator. | no |  |  |
| GET | `/api/projects/:code/hold/status` | hold.ts:48 | B064: GET /api/projects/:code/hold/status / Returns current hold status: location, SSD mount | no |  |  |
| POST | `/api/projects/:code/hold` | hold.ts:86 | B064: POST /api/projects/:code/hold / Body: { dryRun?: boolean } / rsync local project → T7 holding area; runs verify automatically on success | YES: rsync project -> T7 holding (dryRun option) |  | DUP: WINS |
| POST | `/api/projects/:code/hold/verify` | hold.ts:169 | B064: POST /api/projects/:code/hold/verify / On-demand verification — compare local vs holding by file count + bytes | no (compares local vs holding) |  |  |
| DELETE | `/api/projects/:code/local` | hold.ts:204 | B064: DELETE /api/projects/:code/local / Body: { confirmCode: string } / DANGER — deletes local project directory; requires HOLDING copy + verification | YES DANGER: deletes local project dir (needs confirmCode + verified holding) |  |  |
| POST | `/api/projects/:code/hold/restore` | hold.ts:277 | B064: POST /api/projects/:code/hold/restore / rsync T7 holding → local project directory; runs verify automatically on success | YES: rsync T7 holding -> local |  |  |
| DELETE | `/api/projects/:code/holding` | hold.ts:341 | B064: DELETE /api/projects/:code/holding / Body: { confirmCode: string } / DANGER — deletes HOLDING copy from T7 SSD; requires local copy + verification | YES DANGER: deletes T7 holding copy |  |  |
| GET | `/api/projects/archive-inventory` | hold.ts:420 | size, T7 held size, hold flag, derived state, and last-touched timestamp. /  / Moved here from manage.ts during WU1 delivery-review patches because the / aggregation reus | no |  |  |
| POST | `/api/projects/batch-offload` | hold.ts:490 | WU3: POST /batch-offload — body { projects: string[] } / Only projects in `local` state are accepted; others recorded as failures. | YES: rsync many projects -> T7 |  |  |
| POST | `/api/projects/batch-delete-local` | hold.ts:560 | WU3: POST /batch-delete-local — body { projects: string[] } / Only projects in `held-local` state are accepted; others recorded as failures. | YES DANGER: deletes many local project dirs |  |  |
| GET | `/api/projects/:code/storage-tree` | storage.ts:128 | GET /:code/storage-tree / ------------------------------------------------------------------------- | no |  |  |
| POST | `/api/projects/:code/hold` | storage.ts:167 |  / P3: transactional two-pass — / Pass 1: rsync+verify every heavy subfolder to HOLDING. If ANY fails, / STOP and return 500 with no local deletion. HOLDING may have / pa | DEAD (shadowed by hold.ts:86). Would rsync heavy subfolders -> T7 then rm local |  | DUP: DEAD (shadowed by hold.ts:86) |
| POST | `/api/projects/:code/restore-held` | storage.ts:289 | POST /:code/restore-held / Restore HEAVY subfolders from HOLDING → local. HOLDING copy stays. / ------------------------------------------------------------------------- | YES: rsync heavy subfolders T7 -> local |  |  |
| POST | `/api/projects/:code/archive` | storage.ts:373 | POST /:code/archive / Copy WHOLE local folder → PUBLISHED/<brand>/<code>/ (flat, no buckets), / verify, then delete local folder entirely. /  / P1: refuse when PUBLISHED  | YES DANGER: rsync whole project -> T7 PUBLISHED then rm local |  |  |
| POST | `/api/projects/:code/unarchive` | storage.ts:491 | POST /:code/unarchive / Copy whole PUBLISHED folder → local. T7 copy stays. /  / P2: refuse when local dir already exists (even empty shell). / -------------------------- | YES: rsync PUBLISHED -> local |  |  |
| POST | `/api/projects/:code/held-archive` | storage.ts:580 | performs the whole transition server-side with verify-before-destroy: / 1) restore heavy subfolders HOLDING → local (rsync) / 2) verify restored dirs match HOLDING (verif | YES DANGER: restore held + archive + rm local |  |  |
| GET | `/api/projects/:code/storage-activity` | storage.ts:758 | GET /:code/storage-activity?limit=10 — WU5: recent activity for project. / Returns most-recent-first. Tolerant of missing log file (returns []). / ----------------------- | no |  |  |

### brands (2)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/brands` | brands.ts:24 |  | no |  |  |
| POST | `/api/brands/switch` | brands.ts:39 |  | YES: config.json (projectDirectory/brand) via updateConfig | projects:changed,recordings:changed |  |

### context / open-contract (2)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/context` | context.ts:17 |  | no |  |  |
| POST | `/api/context` | context.ts:21 |  | YES: config.json via applyContext->updateConfig (re-points active brand/project) |  |  |

### miccheck (9)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| POST | `/api/miccheck/session/start` | miccheck.ts:51 | POST /session/start | in-memory session | miccheck:started |  |
| POST | `/api/miccheck/session/:id/tick` | miccheck.ts:82 | POST /session/:id/tick | in-memory session | miccheck:tick |  |
| POST | `/api/miccheck/session/:id/event` | miccheck.ts:138 | POST /session/:id/event — client-detected observations that cannot be re-derived / from the 1 Hz series (a level step is defined over 500 ms). | in-memory session |  |  |
| POST | `/api/miccheck/session/:id/room-reference` | miccheck.ts:159 | POST /session/:id/room-reference — store the captured noise floor | in-memory session |  |  |
| POST | `/api/miccheck/session/:id/finish` | miccheck.ts:170 | POST /session/:id/finish | YES: persists session file (finishSession) | miccheck:finished |  |
| POST | `/api/miccheck/session/abandon` | miccheck.ts:203 | POST /session/abandon — the tab closed without finishing. / Explicit so a stale run cannot masquerade as live forever. | YES: persists abandoned session (finishSession) | miccheck:finished |  |
| GET | `/api/query/miccheck/live` | query/miccheck.ts:42 | GET /live | no |  |  |
| GET | `/api/query/miccheck/sessions` | query/miccheck.ts:95 | GET /sessions | no |  |  |
| GET | `/api/query/miccheck/sessions/:id` | query/miccheck.ts:103 | GET /sessions/:id | no |  |  |

### poem-wui / YLO (7)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/poem-wui/status` | poem-wui.ts:48 | GET /api/poem-wui/status — find SRT, return stripped text + metadata | no |  |  |
| POST | `/api/poem-wui/send` | poem-wui.ts:99 | POST /api/poem-wui/send — send transcript to POEM WUI | external POST to POEM WUI (no local disk) |  |  |
| POST | `/api/poem-wui/send-ylo` | poem-wui.ts:162 | POST /api/poem-wui/send-ylo — send transcript to YouTube Launch Optimizer (Supabase inbox) | external POST to Supabase YLO inbox |  |  |
| POST | `/api/poem-wui/resume` | poem-wui.ts:225 | POST /api/poem-wui/resume — load saved .awb.json back into AWB and open browser | external POST to AWB + opens browser |  |  |
| GET | `/api/poem-wui/brand-config` | poem-wui.ts:264 | GET /api/poem-wui/brand-config — return raw brand-config.json for editing | no |  |  |
| POST | `/api/poem-wui/brand-config` | poem-wui.ts:294 | POST /api/poem-wui/brand-config — write updated brand-config.json | YES: writes brand-config.json (managed publish, 409/428 guard) |  |  |
| GET | `/api/poem-wui/chapter-data` | poem-wui.ts:335 | GET /api/poem-wui/chapter-data — chapter list with firstWords from raw transcripts | no |  |  |

### developer (3)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/developer/project-state` | developer.ts:57 |  / Response: { / success: true, / content: { version: 1, recordings: {...}, editManifest: {...}, glingDictionary: [...] }, / filePath: '/path/to/project/.flihub-state.jso | no |  | exposes FR-126 editManifest (deprecated) |
| GET | `/api/developer/config` | developer.ts:110 |  / Response: { / success: true, / content: { watchDirectory: '...', projectDirectory: '...', ... }, / filePath: '/path/to/server/config.json', / size: 5678, / lastModifie | no |  |  |
| GET | `/api/developer/telemetry` | developer.ts:156 | Response: { / success: true, / content: '{"startTimestamp":"...","endTimestamp":"...",...}\n{"startTimestamp":"...",...}\n', / filePath: '/path/to/server/transcription-te | no |  |  |

### system (7)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/system/environment` | system.ts:191 |  / GET /api/system/environment /  / FR-96: Detect the server's runtime environment for path format guidance. / Returns platform info, WSL detection, and path format examp | no |  |  |
| POST | `/api/system/open-folder` | system.ts:263 | Success: { success: true, path: string } / Error: { success: false, error: string } /  / Security: Only accepts predefined folder keys, not arbitrary paths. / The actual  | no disk; launches Finder/Explorer |  |  |
| GET | `/api/system/health` | system.ts:344 |  / GET /api/system/health /  / Simple health check endpoint to verify FliHub is running. / Returns server status and current project info. /  | no |  |  |
| POST | `/api/system/open-file` | system.ts:371 | { subfolder: string, filename: string } /  / Response: / Success: { success: true, path: string } / Error: { success: false, error: string } /  / Security: Only accepts s | no disk; launches default app |  |  |
| POST | `/api/system/open-file-by-path` | system.ts:435 | Response: / Success: { success: true, path: string } / Error: { success: false, error: string } /  / Security: Only accepts files that are managed by FliHub: / - config.j | no disk; launches default app |  |  |
| GET | `/api/system/path-exists` | system.ts:489 |  / Response: / { exists: boolean, path: string } /  / Security: Path is expanded (~ resolved) but not restricted to config paths. / This is safe because we're only checki | no |  |  |
| GET | `/api/system/watchers` | system.ts:531 |  / GET /api/system/watchers /  / FR-90: Get list of all active file watchers. / Used by Config panel to show watcher status. /  / Response: / { watchers: Array<{ name: st | no |  |  |

### query (read-only, /api/query) (15)

| Method | Full path | Handler | Purpose | Mutates disk? | Emits | Flags |
|---|---|---|---|---|---|---|
| GET | `/api/query/projects/:code/chapters` | query/chapters.ts:24 | GET / - Get chapters with timestamps | no |  |  |
| GET | `/api/query/projects/:code/export` | query/export.ts:38 | GET / - Export project data | no |  |  |
| GET | `/api/query/projects/:code/images` | query/images.ts:23 | GET / - List images for a project | no |  |  |
| GET | `/api/query/projects/:code/inbox` | query/inbox.ts:24 | GET / - List inbox files and subfolders (FR-59) | no |  |  |
| GET | `/api/query/projects/:code/inbox/:subfolder/:filename` | query/inbox.ts:144 | GET /:subfolder/:filename - Read inbox file content (FR-64) | no |  |  |
| GET | `/api/query/config` | query/index.ts:39 | Config endpoint (system metadata) | no |  |  |
| GET | `/api/query/projects/resolve` | query/projects.ts:81 | FR-61: GET /resolve - Resolve partial project code | no |  |  |
| GET | `/api/query/projects` | query/projects.ts:126 | GET / - List projects | no |  |  |
| GET | `/api/query/projects/:code/transcript/text` | query/projects.ts:257 | FR-114: GET /:code/transcript/text - Combined transcript as plain text | no |  |  |
| GET | `/api/query/projects/:code` | query/projects.ts:319 | GET /:code - Project detail | no |  |  |
| GET | `/api/query/projects/:code/recordings` | query/recordings.ts:29 | GET / - List recordings for a project | no |  |  |
| GET | `/api/query/projects/:code/transcripts` | query/transcripts.ts:26 | GET / - List transcripts for a project | no |  |  |
| GET | `/api/query/projects/:code/transcripts/:recording` | query/transcripts.ts:130 | GET /:recording - Get single transcript content | no |  |  |
| GET | `/api/query/projects/:code/transcripts/chapters/:chapterName/srt` | query/transcripts.ts:186 | FR-77: GET /chapters/:chapterName/srt - Get chapter SRT file / NOTE: Must be defined BEFORE /:recording/srt to avoid "chapters" matching as :recording | no |  |  |
| GET | `/api/query/projects/:code/transcripts/:recording/srt` | query/transcripts.ts:229 | FR-75: GET /:recording/srt - Get SRT subtitle file content | no |  |  |

### Socket.io events

All server→client. `ClientToServerEvents` is empty (`shared/types.ts:588`); the only server-side listener is `io.on('connection')` (index.ts:391) + `socket.on('disconnect')` (index.ts:399). Declared contract: `shared/types.ts:542-585`.

| Event | Emitted at (server/src/) | Payload | Trigger |
|---|---|---|---|
| `file:new` | index.ts:133 (watcher), index.ts:396 (`socket.emit` replay of pending files on connect) | `FileInfo` | New Ecamm take in watchDirectory |
| `file:sound-holes` | index.ts:148 | `{ path, soundHoles }` | Sound-hole probe finished |
| `file:aspect` | index.ts:165 | `{ path, aspectCheck }` | Aspect probe finished |
| `file:deleted` | index.ts:176 | `{ path }` | Pending file removed from disk |
| `file:renamed` | **never emitted** | `{ oldPath, newPath }` | Declared types.ts; client listens (client/src/hooks/useSocket.ts:60) — dead |
| `file:error` | **never emitted** | `{ path, error }` | Declared; client listens (useSocket.ts:95) — dead |
| `recordings:changed` | WatcherManager.ts:62 (recordings watcher, cfg :151-153); routes/index.ts:127,334,912,970,1010,1078,1135,1228; routes/state.ts:167,230,332,389,422; routes/manage.ts:536,723,793,858,1059; routes/segments.ts:85,109,132; routes/brands.ts:59; utils/openContext.ts:248 via index.ts:380 | none | Any recording/state change |
| `projects:changed` | WatcherManager.ts:62 (projects watcher :165-167); routes/state.ts:356,388; routes/projects.ts:732; routes/brands.ts:58; utils/openContext.ts:247 via index.ts:380 | none | Project folder / title / ships / brand / context change |
| `transcripts:changed` | WatcherManager.ts:62 (:198-200); routes/index.ts:1229 | none | Transcript folder change / recording trash |
| `inbox:changed` | WatcherManager.ts:62 (:181-183) | none | inbox/ change |
| `thumbs:changed` | WatcherManager.ts:62 (:213-215) | none | assets/thumbs change |
| `thumbs:zip-added` | WatcherManager.ts:62 (:112-114) | none | New ZIP in ~/Downloads |
| `assets:incoming-changed` | WatcherManager.ts:62 (:124-126) | none | Image source dir change |
| `assets:assigned-changed` | WatcherManager.ts:62 (:136-138) | none | assets/images change |
| `transcription:queued` | routes/transcriptions.ts:483 | `{ jobId, videoPath, position }` | Job queued |
| `transcription:started` | routes/transcriptions.ts:192 | `{ jobId, videoPath }` | Job starts at FliTools |
| `transcription:progress` | routes/transcriptions.ts:250 | `{ jobId, text }` | Streamed text |
| `transcription:complete` | routes/transcriptions.ts:291 | `{ jobId, videoPath, transcriptPath, health }` | Done (health = B584 suspect flags) |
| `transcription:error` | routes/transcriptions.ts:327 | `{ jobId, videoPath, error }` | Failed |
| `miccheck:started` | routes/miccheck.ts:76 | `{ sessionId }` | POST /api/miccheck/session/start |
| `miccheck:tick` | routes/miccheck.ts:132 | `{ sessionId, tick }` | 1 Hz tick |
| `miccheck:finished` | routes/miccheck.ts:196, 221 | `{ sessionId }` | finish / abandon |
| `context:changed` | index.ts:378 (from utils/openContext.ts:249) | `OpenContextState` | POST /api/context or launch args |

Removed: FR-58/FR-131 chapter-preview events (comment at shared/types.ts, "previews deprecated (roadmap §1.2e)").

### Deprecated / dead surface (per docs/rebuild-2026/requirements-archaeology-2026-09.md §"deprecation cluster" lines 80-99 and docs/AGENT-NOTES.md)

| Item | Live server surface | Status |
|---|---|---|
| b-roll lane (FR-161) | `GET /api/broll` (index.ts:557), `DELETE /api/broll/:filename` (index.ts:580), b-roll branch in `POST /api/rename` (index.ts:211-278), `'b-roll'` in video.ts:56 folder allow-list, `HEAVY_SUBFOLDERS` (utils/storageTree.ts:23) | Deprecated 2026-09-22, still fully wired. Hold/restore must keep carrying `b-roll/`. |
| FR-126 edit-folder manifest | No route writes it; `GET /api/developer/project-state` (developer.ts:57) exposes `editManifest`; `setEditManifest` has zero callers | Deprecated, dormant |
| Shadows FR-83 | No route. Generation removed 2026-09-04 (comment index.ts:375); renameRecording sweep still moves shadows (archaeology l.125) | Deprecated, residual handling only |
| Chapter video generation FR-58/FR-131 | `PUT /api/chapters/config` (chapters.ts:48) 410, `POST /api/chapters/generate` (chapters.ts:53) 410, `POST /api/manage/regen-chapters` + `/regen-all` (manage.ts:317) 410; `GET /api/chapters/config` + `/status` still answer (legacy) | 4 routes return 410 |
| Relay / git sync | No routes left (removed commit "refactor: remove git sync (Sync Hub) and relay collaboration", 2026-09-22) | Gone |
| `storage.ts:167` POST hold | Shadowed by hold.ts:86 | Dead code |
| `machineRole` | Still saved by `POST /api/config`; read by nothing (AGENT-NOTES) | Dead field |

### Surprises worth knowing

- `GET /api/projects/next-code` (index.ts:463) **writes config.json** (raises `projectCodeHighWater`) — a GET with a side effect.
- The storage-panel's own Hold (`storage.ts:167`, transactional, deletes local heavy folders) is unreachable. The client StoragePanel (`client/src/components/shared/StoragePanel.tsx:27` -> `client/src/hooks/useStorageApi.ts:77`, `buildMutation('hold', 'Held heavy files to T7')`) POSTs to `/api/projects/:code/hold`, so it is answered by B064 `hold.ts:86` (whole-project rsync, no local delete) while toasting "Held heavy files to T7". Established by reading code + mount order only; not exercised at runtime (POST would move real data).
- ~~Two trash folder conventions~~ **[CORRECTED]**: `POST /api/trash` uses `paths.trash` (`-trash/`); only its comment says `.trash/`.
- `file:renamed` / `file:error` are in the typed contract and the client subscribes, but the server never emits them.
- `assets.ts` and `thumbs.ts` handlers have had zero commits since 2026-06-01; the hot spots are index.ts (recordings + promotion), projects.ts, manage.ts, segments.ts, transcriptions.ts.
- `POST /api/poem-wui/*` and `POST /api/projects/:code/chapters/verify` make outbound network calls (POEM WUI, Supabase YLO inbox, AWB, an LLM) from a loopback-only server.


## Appendix B. Client: screens, panels, shortcuts, look

Repo: `/Users/davidcruwys/dev/ad/flivideo/flihub` @ `061ae34` (main, clean). All paths relative to `client/src/`.
Method: static greps over source (excluding `*.test.*`) plus `git log`. Nothing was run in a browser; "mounted" means "rendered by a JSX tag reachable from App.tsx", not "observed on screen".

### 0. Shell and routing

- **No router library.** `App.tsx` holds `activeTab` state (`App.tsx:115`), synced to `location.hash` (`getTabFromHash` `App.tsx:90`, `hashchange` listener `App.tsx:128`). The 14 valid hashes are `VALID_TABS` (`App.tsx:69-84`); an unknown hash falls back to `incoming`.
- Providers: `main.tsx` mounts one `QueryClientProvider` (TanStack Query) around `<App/>`. `sonner` `<Toaster position="top-right" richColors/>` at `App.tsx:468`.
- Root: `<div className="min-h-screen bg-page flex flex-col">` (`App.tsx:467`).
- App-level hooks: `useSocket` (`App.tsx:199`, incoming file list + connection), `useRecordingsSocket` (`:222`), `useDeveloperSocket` (`:224`), `useContextSocket` + `useOpenContext` (`:226-227`), plus `useConfig`, `useProjects`, `useSuggestedNaming`, `useRecordings`, `useRecentRenames`, `useUndoRename`, `useSetProjectTitle`, `useTrashFile`, `useUpdateConfig`, `useOpenFolder`, `useBestTake`.
- `<main>` is `max-w-4xl mx-auto px-4 py-6` for every tab except Projects, which is full-bleed `flex-1 flex flex-col overflow-hidden` (`App.tsx:782`). The footer is hidden on Projects (`App.tsx:1020`).

### 1. Top-level tabs/screens

Two ways in: the **nav row** (10 visible tabs) and the **gear menu** (4 hidden tabs plus the Developer drawer).

| # | Hash / label | Entry point | Mounted at | Component (file) | Purpose | Hooks → endpoints | Socket events | Last touch | Commits since 2026-06-01 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `incoming` / "Incoming" (+count badge) | nav `App.tsx:669` (default tab) | `App.tsx:784-871` | inline in App: `NamingControls`, `FileCard` list, `SendSeveralBar`, `AspectWarningBanner`, `RecentlyNamedStrip`; floating `ChapterContextPanel` (`App.tsx:1033-1037`) | Name or promote new Ecamm takes (chapter-seq-name-tags), Rename·Keep/Discard, send several, b-roll promote | `useSuggestedNaming` GET `/api/suggested-naming`; `useRename` POST `/api/rename`; `useTrashFile` POST `/api/trash`; `useSegmentOp` POST `/api/segments/op`; `useRecentRenames`/`useUndoRename` `/api/recordings/recent-renames`, `/undo-rename`; `useDismissAspectWarning` POST `/api/recordings/aspect-dismiss` | `file:new`, `file:renamed`, `file:deleted`, `file:aspect`, `file:sound-holes`, `file:error` (`hooks/useSocket.ts:49-95`); `recordings:changed` | App.tsx 2026-10-25; FileCard 2026-10-26 | App 13, FileCard 10, NamingControls 0, SendSeveralBar 1, RecentlyNamedStrip 0, ChapterContextPanel 0 |
| 2 | `recordings` / "Recordings" | nav `App.tsx:684` | `App.tsx:881-916` (InlineTitle for project title `:887`, OpenFolder Recordings/Safe `:911-912`) | `components/RecordingsView.tsx` (1744 lines) | Chapter-grouped list of named takes: inline rename/renumber/split, tags, safe/park, segment move/placeholder, delete, transcripts | `useRecordings` GET `/api/recordings`; `useRenameRecording` `/api/rename`; `useBulkRename`, `useSplitChapter`, `useRenumberChapter`, `useBatchUndoRename` (`/api/manage/*`); `useMoveToSafe`/`useRestoreFromSafe`, `useParkRecording`/`useUnparkRecording`; `useSetChapterTitle`; `useTranscribeAll` POST `/api/transcriptions/queue-all`; `usePendingTranscriptionCount`; `useRecordingDelete` (→ `/api/recordings/trash`, `/api/segments/*`); raw fetch `/api/transcriptions/{queue,status,transcript,combine-chapter}` | `recordings:changed` | 2026-10-12 | **19** (most active screen) |
| 3 | `b-roll` / "B-Roll" | nav `App.tsx:694` | `App.tsx:874-878` | `components/BRollPage.tsx` | FR-161 b-roll lane: list, play inline, delete | `useBrollList` GET `/api/broll`; `useDeleteBroll` DELETE; video src `/api/video/:code/b-roll/:file` | none | 2026-09-04 | 2 |
| 4 | `watch` / "Watch" | nav `App.tsx:704` | `App.tsx:919-923` | `components/WatchPage.tsx` | Full-width player with hover-out chapter/segment cascade, 2x default speed, size toggle, transcript sync highlight | `useRecordings`, `useParkRecording`/`useUnparkRecording`, `useVideoPlayback`, `useVideoAspect`; video `/api/video/:code/:folder/:file`; `TranscriptSyncPanel` raw fetch `/api/query/projects/:code/transcripts/.../srt` | `recordings:changed` | 2026-09-08 | 3 |
| 5 | `transcriptions` / "Transcripts" | nav `App.tsx:714` | `App.tsx:926-930` | `components/TranscriptionsPage.tsx` | Transcription queue and progress, list of transcripts | `useConfig`; raw fetch `/api/transcriptions`, `/api/query/projects/:code/transcripts`; `TranscriptionProgressBar` (`useProjects`) | `transcription:progress/complete/error/started/queued` (`TranscriptionsPage.tsx:79-83`, raw socket) | 2026-03-24 | 0 |
| 6 | `inbox` / "Inbox" | nav `App.tsx:724` | `App.tsx:933-937` | `components/InboxPage.tsx` | FR-59 project `inbox/` (raw/dataset/presentation) browser + file viewer | `useInbox`, `useInboxFileContent`, `useOpenInboxFile` POST `/api/system/open-file` | `inbox:changed` | 2026-03-24 | 0 |
| 7 | `assets` / "Assets" | nav `App.tsx:734` | `App.tsx:940-945` | `components/AssetsPage.tsx` (1462 lines) | Assign incoming images to chapter/seq slots, prompts, clipboard paste, shift-hover preview | `useIncomingImages` `/api/assets/incoming`, `useProjectImages` `/api/assets/images`, `useAssignImage`, `useDelete*Image`, `useSave/Load/DeletePrompt` `/api/assets/prompt`, `useClipboardAssign`/`useClipboardToIncoming` `/api/assets/clipboard/*`, `useNextImageOrder`; raw `/api/assets/image/:path`, `/api/transcriptions/transcript/:file` | `assets:incoming-changed`, `assets:assigned-changed` | 2026-03-24 | 0 |
| 8 | `thumbs` / "Thumbs" | nav `App.tsx:744` | `App.tsx:948-953` | `components/ThumbsPage.tsx` | YouTube thumbnail import from zip, reorder (shift-click), delete | `useZipFiles` `/api/thumbs/zips`, `useZipContents`, `useThumbs` `/api/thumbs`, `useImportFromZip`, `useReorderThumbs`, `useDeleteThumb`, `useDeleteZip` | `thumbs:changed`, `thumbs:zip-added` | 2026-03-24 | 0 |
| 9 | `export` / "Manage" | nav `App.tsx:754` (also via T7 pill `App.tsx:594` → storage tool) | `App.tsx:956-965` | `components/ManagePanel.tsx` + fixed-left `ToolsSidebar` (`ManagePanel.tsx:491`) | Power tools. Sidebar groups: **Record** → Regen (`:318`); **Edit** → Gling/Edit (`GlingEditTool` `:479`), AWB (`PoemWuiPage` `:480`); **Storage** → Storage (`StoragePanel` `:483`) | `useRecordings`, `useConfig`; raw POST `/api/manage/regen-transcripts`, `/api/manage/delete-:target`; Gling: `useEditPrep`, `useCreateEditFolder(s)`, dictionary updates, raw `/api/manage/recordings-folder-path`; AWB: `usePoemWuiStatus`, `useSendToPoem`, `useSendToYlo`, `useResumeInAwb` (`/api/poem-wui/*`); Storage: `useStorageTree`, hold/restore/archive/unarchive `POST /api/projects/:code/:verb`, `useStorageActivity` | `recordings:changed` | 2026-09-22 | ManagePanel 4, StoragePanel 1, GlingEditTool 1, PoemWuiPage 0 |
| 10 | `projects` / "Projects" | nav `App.tsx:765`; also "All projects..." in the project dropdown; `BrandSwitcher` lands here | `App.tsx:968-984` | `components/ProjectsPanel.tsx` (808 lines) | FR-148 project list (filterable table): stage/priority edits, hold status, disk scan, new project; opens `ProjectDrawer` | `useProjects` GET `/api/projects/stats`, `useCreateProject` POST `/api/projects`, `useUpdateProjectPriority`/`Stage` PUT, `useDiskScanAll` POST `/api/projects/disk/scan-all`, `useHoldStatus`, `useUpdateConfig`, `useRefetchSuggestedNaming` | `projects:changed`, `transcripts:changed` | 2026-09-22 | 5 |
| 11 | `config` / "Configuration" | gear menu `App.tsx:628` (also `handleNavigateToConfig` `:422`) | `App.tsx:987-995` | `components/ConfigPanel.tsx` (1261 lines) | Settings, 5 internal tabs (`ConfigPanel.tsx:567-571`): Directories (`:602`), Recording Names (`:809`), Collaboration (`:790`), Advanced (`:1018`), Brand (`:1063`) | `useConfig`/`useUpdateConfig` `/api/config`, `useWatchers` `/api/system/watchers`, `useEnvironment` `/api/system/environment`, `useBrandConfig`/`useUpdateBrandConfig` `/api/poem-wui/brand-config`; raw `/api/system/path-exists` | none | 2026-10-29 | 4 |
| 12 | `mockups` / "Mockups" | gear menu `App.tsx:633` | `App.tsx:998-1002` | `components/MockupsPage.tsx` | Static link hub to Mochaccino design mockups (`.mochaccino/designs/`) and legacy `client/public/mocks/`. No API. | none | none | 2026-03-26 | 0 |
| 13 | `miccheck` / "Mic Check" | gear menu `App.tsx:638` | `App.tsx:1005-1009` | `components/MicCheckPage.tsx` (+ `MicCheckSnapshot` `:390`, `MicCheckReport` `:413`) | Live mic monitoring in the browser (Web Audio). Snapshot verdict test is the primary UI. It has its own Oswald + Roboto Mono "instrument panel" typography. | `useMicAnalyser` (browser only, no server) | none | 2026-08-29 | MicCheckPage 4, useMicAnalyser 5 |
| 14 | `api-explorer` / "API Explorer" | gear menu `App.tsx:643` | `App.tsx:1012-1017` | `components/ApiExplorer.tsx` (default export) | FR-119 Postman-lite: lists `shared/apiRegistry` endpoints by group, builds params, fires raw fetches at `API_URL` | raw fetch to any registered endpoint | none | 2026-03-25 | 0 |

### 2. Header widgets, menus, drawers (always mounted)

Header layout (`App.tsx:483-776`) has two rows inside `max-w-4xl`. The **top row** reads `FliHub › Brand ▾ › PROJECT-CODE ▾ ···`, then on the right `Trash · T7 pill | ⚙`. The **bottom row** is the 10-tab nav.

| Widget | Mounted at | Purpose | Hooks / endpoints | Commits since 06-01 |
|---|---|---|---|---|
| `BrandSwitcher` | `App.tsx:491` | Brand dropdown. Switching repoints the app at that brand root, then jumps to Projects. Esc closes. | `useBrands` GET `/api/brands`, `useSwitchBrand` POST `/api/brands/switch` | 1 (2026-09-03) |
| Project switcher dropdown (inline) | `App.tsx:497-584` | Lists pinned projects (⭐) and "All projects..." | `useUpdateConfig` (switch) | (App) |
| `HeaderDropdown` "···" project actions | `App.tsx:509-539` | Copy for calendar · Copy full path · Open in Finder | `useOpenFolder` POST `/api/system/open-folder` | 0 |
| `TrashIndicator` | `App.tsx:593` | Always-visible `-trash/` count + size, confirm and empty (shows "?" when unreadable) | `useTrashSummary`, `useDeleteTrash` DELETE | 2 |
| `SsdIndicator` (T7 pill) | `App.tsx:594-597` | T7 SSD connected state; click opens Manage → Storage | `useSsdStatus` GET `/api/projects/ssd-status` | 1 |
| `HeaderDropdown` ⚙ gear menu | `App.tsx:601-660` | Configuration · Mockups · Mic Check · API Explorer · Developer Tools · (divider) GitHub (flivideo/flihub) · Video Projects (github appydave-video-projects/v-appydave). The gear icon turns blue on the 4 hidden tabs. | — | 0 |
| `DeveloperDrawer` | `App.tsx:480` (opened by gear "Developer Tools" `:648`) | FR-127 right-hand resizable slide-out (300-1000px, default 800), **dark Monaco editor**. 3 file tabs: `.flihub-state.json`, `config.json`, `telemetry.jsonl` (`DeveloperDrawer.tsx:37-39`). Esc closes. | `useDeveloperProjectState` `/api/developer/project-state`, `useDeveloperConfig` `/api/developer/config`, `useDeveloperTelemetry` `/api/developer/telemetry`; raw POST `/api/system/open-file-by-path` | 0 (2026-03-25) |
| `ContextRefusedBanner` | `App.tsx:778-780` | W3 banner when an open-contract launch was refused (dismissable) | uses `useOpenContext` GET `/api/context` | 1 |
| `DiscardModal` | `App.tsx:471-478` | After send-several or Rename·Keep: discard the remaining incoming takes? Enter/Esc. | — | 1 (2026-10-25) |
| `ConnectionIndicator` (footer) | `App.tsx:1026` | Socket connected/reconnecting dot. The footer also shows the collapsed project path. | `useSocket` state | 0 |
| `Toaster` (sonner) | `App.tsx:468` | Top-right toasts | — | — |

### 3. Nested panels, modals, overlays

| Component | Mounted at | Kind | Purpose | Hooks / endpoints |
|---|---|---|---|---|
| `NamingControls` | `App.tsx:787` | panel | Chapter/seq/name/tag inputs with glow-pulse feedback, New Chapter | (props) |
| `FileCard` | `App.tsx:833` | card | Incoming take: Rename·Keep (amber), Rename·Discard (blue primary), Discard (red), B-roll, preview, landing slot | `useRename`, `useTrashFile`, `useSegmentOp`, `useRecordings` |
| `IncomingVideoModal` → `VideoPlayerModal` | `FileCard.tsx:361` → `IncomingVideoModal.tsx:47` | modal | Preview incoming take, with dictionary quick-add | `useProjectDictionary`, `useAdd{Global,Project}DictionaryWord`; `/api/video/incoming/:file` |
| `SendSeveralBar` | `App.tsx:816` | bar | CT-0107: send several picked takes as consecutive segments | `useSegmentOp` |
| `AspectWarningBanner` | `App.tsx:814` | banner | Loud warning when a take's aspect mismatches the project | `useDismissAspectWarning` |
| `RecentlyNamedStrip` → `VideoPlayerModal` | `App.tsx:863` → `RecentlyNamedStrip.tsx:86` | strip + modal | Recently named takes with undo and preview | `/api/video/recordings/:file` |
| `ChapterContextPanel` | `App.tsx:1035` | floating panel (fixed, right of content) | Shows existing chapters while naming (Incoming only) | (props) |
| `InlineTitle` | `App.tsx:887`, RecordingsView | inline edit | FR-157 project/chapter titles; saves on blur/Enter | `useSetProjectTitle` PUT |
| `BatchToolbar` | `RecordingsView.tsx:1459` | toolbar | Bulk select actions | — |
| `PreviewPanel` | `RecordingsView.tsx:1474` | panel | Preview of a rename change set | — |
| `SplitMarker` | `RecordingsView.tsx:1593` | inline | Chapter split marker | — |
| `EditableFileRow` | `RecordingsView.tsx:1602` | row | Inline rename, + tag, split here, trash, preview | — |
| `AspectWarningChip`, `SoundHoleChip` | `RecordingsView.tsx:1625,1627` | chips | Per-take aspect / digital-zero dropout flags | — |
| `SegmentControls` | `RecordingsView.tsx:1628` | inline | Placeholder flag, move up/down | `useSegmentOp`, `useSegmentPlaceholder` |
| `useRecordingDelete` + `SegmentUndoButton` (from `shared/RecordingDelete.tsx`) | `RecordingsView.tsx:44,749`; its `ConfirmationModal`s at `RecordingDelete.tsx:124,149` | hook + modals | Guarded delete that closes up segments, with undo | `usePreviewTrashRecordings`, `useTrashRecordings`, `useSegmentPreview`, `useSegmentUndo` |
| `ChapterPanel` (flyout "chapters") | `RecordingsView.tsx:1661` | slide-out | Chapter list/titles; raw `/api/poem-wui/chapter-data` | — |
| `ChapterHelpPanel` (flyout "help") | `RecordingsView.tsx:1676` | slide-out | Chapter naming help | — |
| `DamHelpPanel` (flyout "dam") | `RecordingsView.tsx:1687` | slide-out | DAM/storage help text | — |
| `TranscriptModal` → `FileViewerModal` | `RecordingsView.tsx:1692`, `TranscriptionsPage.tsx:247` | modal | View one transcript (txt/srt) | raw `/api/transcriptions/transcript/:file` |
| `VideoTranscriptModal` | `RecordingsView.tsx:1702` | modal | Combined chapter transcript; Esc | raw `/api/transcriptions/combined` |
| `RecordingVideoModal` → `VideoPlayerModal` | `RecordingsView.tsx:1707` | modal | Play a named recording; ←/→ prev/next | `/api/video/recordings/:file`, dictionary hooks |
| `UndoToast` | `RecordingsView.tsx:1735` | toast | Undo last rename batch | — |
| `VideoPlayerModal` (shared) | 3 callers above | modal | Player + `VideoControlsBar` (`:238`) + `TranscriptSyncPanel` (`:271`) + `DictionaryQuickAdd` (`:286`) | `useVideoPlayback`, `useVideoAspect` |
| `TranscriptionProgressBar` | `TranscriptionsPage.tsx:105` | bar | Queue progress | `useConfig`, `useProjects` |
| `ImagePreviewOverlay` | `AssetsPage.tsx:1343` | overlay | Shift-hover large image preview | — |
| `ClipboardPasteModal` | `AssetsPage.tsx:1347` | modal | Paste image from clipboard; Enter/Esc | — |
| `FileViewerModal` | `InboxPage.tsx:180`, `TranscriptModal.tsx:72` | modal | Generic text file viewer | — |
| `ProjectListToolbar` | `ProjectsPanel.tsx:501` (+ ProjectDrawer) | toolbar | Filters/search for project list | — |
| `NewProjectForm` | `ProjectsPanel.tsx:758` | form | Create project with next code + ships (one video / many) | `useNextProjectCode` `/api/projects/next-code` |
| `ProjectDrawer` | `ProjectsPanel.tsx:805` | drawer | Project detail: disk usage, ships, trash, transcribe all, delete; Esc | `useProjectDisk`, `useDeleteTrash`, `useSetProjectShips`, `useTranscribeAll`, `useDeleteProject`, `useOpenFolder` |
| `ProjectDeleteModal` | `ProjectDrawer.tsx:439` | modal | Type-to-confirm project delete | — |
| `ShipsSelector` | `NewProjectForm.tsx:143`, `ProjectDrawer.tsx:205` | control | FR-168 ships selector | — |
| `ToolsSidebar` | `ManagePanel.tsx:491` | fixed left sidebar (`left-8 top-32 w-[200px]`) | Manage tool nav | — |
| `ConfirmationModal` | `ManagePanel.tsx:499`, `TrashIndicator.tsx:47`, RecordingDelete | modal | Generic confirm with file list; Esc | — |
| `StoragePanel` → `StorageStateHeader`/`StorageActions`/`StorageTree`/`StorageActivityFeed` | `ManagePanel.tsx:483` → `StoragePanel.tsx:154,168,199,203` | tool page | Active/held/archived state, hold/restore/archive, tree, activity feed | `useStorage*` |
| `MicCheckSnapshot`, `MicCheckReport` | `MicCheckPage.tsx:390,413` | panels | Snapshot verdict, end-of-run report | — |

### 4. Keyboard shortcuts

| Key | Where | Effect |
|---|---|---|
| Space | `hooks/useVideoPlayback.ts:77` (document keydown) | Play/pause in Watch and in player modals |
| ← / → | `shared/VideoPlayerModal.tsx:129-134` | Previous/next recording in the player modal |
| Shift (hold) | `hooks/useShiftHover.ts:61-72` | Enables hover image preview (Assets) |
| Shift+click | `ThumbsPage.tsx:171` | Range or reorder selection |
| Esc | BrandSwitcher `:20`, HeaderDropdown `:39`, DeveloperDrawer `:63`, ProjectDrawer `:103`, ProjectDeleteModal `:39`, ConfirmationModal `:48`, FileViewerModal `:52`, VideoTranscriptModal `:73`, RecordingsView flyouts `:1275`, ClipboardPasteModal `:29`, DiscardModal `:20`, inline editors | Close or cancel |
| Enter | DiscardModal `:20` (confirm), ClipboardPasteModal `:26`, InlineTitle `:58`, EditableFileRow `:134,331`, BatchToolbar `:100`, DictionaryQuickAdd `:77`, NewProjectForm `:123`, ConfigPanel `:978` | Submit |

There are no global app shortcuts: no tab hotkeys and no command palette.

### 5. Dead and hidden surfaces

### Dead (component file exists, never rendered from App)
| Component | Evidence | Notes | Last touch |
|---|---|---|---|
| `components/HoldDeleteModal.tsx` | zero importers | B064 type-to-confirm delete-local/delete-holding modal. Its hooks `useDeleteLocal`, `useDeleteHolding`, `useVerifyHolding`, `useRestoreFromHolding` (`hooks/useHoldApi.ts`) have zero callers too. | 2026-04-08 |
| `components/ProjectStatsPopup.tsx` (955 lines) | zero importers | Old per-project stats popup (final media, chapter verify/override). Takes `TranscriptSyncModal` down with it (its only parent, `ProjectStatsPopup.tsx:450`). Hooks reachable only through it: `useFinalMedia`, `useChapters`, `useVerifyChapter`, `useSetChapterOverride`, `useTranscriptSync`, `useQueueTranscription`, `useDeleteTranscript`. | 2026-03-24 |
| `components/TranscriptSyncModal.tsx` | only parent is dead | — | 2026-09-22 |
| `shared/PageHeader.tsx`, `shared/SelectionBadge.tsx`, `shared/SlideOutDrawer.tsx` | exported from `shared/index.ts`, never imported | `SlideOutDrawer` was superseded by B041 ("no slide-out drawers") | 2026-03-24 |

### Dead hooks (exported, zero callers anywhere)
`useChapterOverrides`, `useRemoveChapterOverride`, `useProjectState`, `useWriteToInbox` (useProjectsApi) · `useRenameChapter` (useRecordingsApi) · `useCleanEditFolder`, `useRestoreEditFolder`, `useManifestStatus` (useEditApi; **FR-126 edit-manifest leftover**) · `useDeleteSubfolder` (useProjectDiskApi) · `useRefetchThumbs`, `useRefetchZips` (useThumbsApi) · plus the 4 hold hooks above.

### Hidden or developer-only (gear menu, no nav tab)
- **Mockups** (`#mockups`): a static design-link hub. 3 of its Mochaccino cards point at **removed features**: "Sync Hub" (git sync) and "Relay Redesign" (`MockupsPage.tsx:18-28`), plus "Recording Editor". There is no API.
- **Mic Check** (`#miccheck`): a real, recently built tool (Aug 2026), placed in the gear menu only.
- **API Explorer** (`#api-explorer`): a developer request builder over `shared/apiRegistry`. It can fire destructive endpoints (hold/archive/delete) against live data; AGENT-NOTES warns about API probing.
- **Developer Tools** drawer: a raw JSON viewer for state/config/telemetry. It is the only dark surface in the app.
- **Config** sits in the gear menu too, but it is a primary screen, not a developer one.

### 6. Deprecated areas and leftovers

| Area | Where | Status |
|---|---|---|
| **B-Roll tab (FR-161, deprecated but still in the code)** | nav `App.tsx:694-701`, page `App.tsx:874-878` → `BRollPage.tsx`; promote button `FileCard.tsx:148-171,325-330`; `hooks/useBrollApi.ts` | Fully live and visible in the nav. AGENT-NOTES: "deprecated, don't extend". |
| Shadow recordings (FR-83) | `ConfigPanel.tsx:1020` comment says the section was removed 2026-09-04 | Removed from the client. No shadow UI is left. |
| Relay / git sync | Removed 2026-09-22 (`19ddd05`). Leftovers: `MockupsPage.tsx:18-28` cards; stale comments `shared/VideoPlayerModal.tsx:2` ("Relay previews"), `shared/StoragePanel.tsx:3` ("mirrors RelayTool.tsx"); `RecentlyNamedStrip`/`TranscriptSyncPanel` came from the relay commit `c028aa8` but are still used | Cosmetic only |
| `machineRole` | Config → **Collaboration** tab (`ConfigPanel.tsx:790-806`) holds only a Recorder/Editor select. `ToolsSidebar.tsx:1` TODO to gate tools by role | Read by nothing (AGENT-NOTES). The whole Collaboration tab is vestigial. |
| Gling dictionary | Config → Recording Names, "Global Dictionary Words ... for Gling transcription" (`ConfigPanel.tsx:~830`) | The `glingDictionary` value no longer reaches any engine (FliTools owns words) |
| Edit manifest (FR-126) | `useManifestStatus` in `hooks/useEditApi.ts:83` | Dead hook |
| Chapter-video / chapter-preview | `ConfirmationModal` cleanup in `8cf8435`; `useTranscriptionsApi` change `e07885d` | Already stripped |
| Hold / offload v1 (B064) | `HoldDeleteModal` + 4 hooks | Dead. Superseded by the StoragePanel hold/archive verbs. |
| PoemWuiPage "AWB" tool | `ManagePanel.tsx:480` | Live but untouched since 2026-04-12 (0 commits) |

### 7. Activity ranking (commits since 2026-06-01)

| Most active | n | Least active / frozen since spring (0 commits) |
|---|---|---|
| RecordingsView.tsx | 19 | AssetsPage (1462 lines), ThumbsPage, InboxPage, TranscriptionsPage, TranscriptModal, VideoTranscriptModal, TranscriptionProgressBar |
| App.tsx | 13 | ApiExplorer, MockupsPage, DeveloperDrawer, PoemWuiPage |
| FileCard.tsx | 10 | NamingControls, ChapterContextPanel, RecentlyNamedStrip, HeaderDropdown, ConnectionIndicator |
| useRecordingsApi.ts | 8 | BatchToolbar, UndoToast, SplitMarker, VideoControlsBar, FileViewerModal |
| ProjectsPanel 5, EditableFileRow 5, useMicAnalyser 5, useSocket 5 | | index.css: 0 (last touched 2026-03-24, B048/B049) |
| ManagePanel 4, ConfigPanel 4, MicCheckPage 4, useSegmentsApi 4 | | |

Net: the Incoming → Recordings recording-day loop and the Projects list got almost all the attention from June to October. Assets, Thumbs, Inbox and Transcripts have not changed since the Warm Linen pass (2026-03-24).

### 8. Visual system: how it looks today

**Theme: "Warm Linen" (B048, 2026-03-24, `fb99b1b`).** It is a camera-friendly, low-glare beige palette defined as Tailwind v4 `@theme` tokens in `index.css:9-31`. It is a single light theme: zero `dark:` classes and no `prefers-color-scheme`.

| Token | Hex | Role | Uses in .tsx |
|---|---|---|---|
| `--color-page` → `bg-page` | `#e8e0d4` | page canvas (darkest beige) | 1 (root) |
| `--color-surface-muted` | `#eee8de` | sidebars, muted panels | 117 |
| `--color-surface-hover` | `#ede5d8` | hover rows | 107 |
| `--color-surface` | `#f5f1eb` | cards, dropdowns (lightest) | 110 |
| `--color-warm-header` | `#f0ebe3` | header band | 1 |
| `--color-warm` / `border-warm` / `warm-divider` | `#d4cdc4` | hairline borders | 180 |
| `--color-warm-strong` / `border-warm-strong` | `#b8a99a` | stronger borders | 101 |
| `--color-warm-secondary` | `#4a3e30` | secondary text (dark brown) | 325 |
| `--color-warm-muted` | `#7a6e5e` | muted text | 405 (most-used class) |
| `--color-text-warm-primary` | `#2a2018` | intended primary text | **see defect** |
| `--color-text-warm-faint` | `#9a8a78` | intended faint text | **see defect** |

**Token defect (verified against the built CSS `client/dist/assets/index-zwRuRZH9.css`, built 2026-09-04):** the primary and faint tokens are declared as `--color-text-warm-primary` and `--color-text-warm-faint`, so Tailwind generates `text-text-warm-primary`. The components use `text-warm-primary` (93 uses, including the "FliHub" H1 at `App.tsx:487`) and `text-warm-faint` (62 uses), and **no CSS rule is emitted for either.** That text falls back to the inherited colour, which is near-black. `bg-warm-subtle` (2 uses) is undefined too. The live dev server's CSS was not checked; the dist build is the evidence.

**Accent colours are stock Tailwind on top of the linen.** Blue-600 is the active tab, links, project name and primary buttons (`text-blue-600` 63, `bg-blue-600` 28). Red is destructive and errors (`bg-red-50`, `text-red-500/600/700`). Green is success. Amber is Rename·Keep and warnings. Purple appears only on the Mockups icon. Focus feedback uses glow-pulse keyframes in blue/green/red (`index.css:33-73`).

**Typography.** The base is the Tailwind default system sans stack; no app font is loaded. `font-mono` appears 141 times (filenames, paths, codes). The only webfonts are Oswald 500-700 and Roboto Mono, loaded in `client/index.html` for **MicCheckSnapshot only** (its own instrument-panel style, deliberately separate). The DeveloperDrawer uses Monaco's dark editor theme. Emoji are used as icons throughout (📋 📂 ⚙️ 🎨 🎙️ 🔌 🔍 🔗 🎬 ⭐).

**Layout shell.**
- `min-h-screen bg-page` column.
- Header `bg-warm-header shadow-sm`, content capped at `max-w-4xl` (896px, centred). The top row is `FliHub` (text-xl semibold) › brand ▾ › **project code in blue** ▾ ···, with Trash and T7 pills, a divider and the ⚙ gear on the right.
- The bottom row is a flat text tab strip: inactive `text-warm-muted`, active `text-blue-600 font-medium`, with a count badge on Incoming. There are no pill or underline tab chrome.
- Content is a centred narrow column, except Projects, which goes full width. Two screens put chrome in the side margins: Manage (`ToolsSidebar` fixed at `left-8`, 200px) and Incoming (`ChapterContextPanel` fixed just right of the 896px column).
- The footer shows the project path and a connection dot. Toasts are top-right.
- Cards are `bg-surface border-warm rounded-lg`. Dropdowns are `shadow-lg`.


## Appendix C. Config, watchers, jobs, on-disk writes, real data

Read-only discovery, 2026-10-30, M4 Mini, repo `/Users/davidcruwys/dev/ad/flivideo/flihub` @ `061ae34`.
Paths relative to repo root unless absolute. `S` = `server/src`.

---

### 1. Settings / config files

### 1a. Files outside the code that FliHub reads or writes

| File | Direction | Reader / writer (file:line) | Notes |
|---|---|---|---|
| `server/config.json` | R + W | load `S/config/configManager.ts:42`, save `:116`; path `S/index.ts:54` | Main machine config. Gitignored. Rewritten whole on every save (allowlist `toSave`). Template: `server/config.template.json` |
| `server/.env` | R | `S/index.ts:51` (dotenv), schema `S/config/env.ts:5` | PORT, NODE_ENV, CLIENT_URL, YLO_BEARER_TOKEN, YLO_INBOX_URL (secret: token — not printed) |
| `server/.launch-context.json` | R + W | `S/utils/openContext.ts:273` (writeJson `{launchId, appliedAt}`); path `S/index.ts:56` | W3: stops a nodemon restart re-applying `FLIVIDEO_LAUNCH_ID` launch args |
| `server/.transcript-follow.json` | R + W | read `S/routes/transcriptions.ts:84`, write `:94`; path `S/index.ts:273` | `{renames[], pass2[]}` — rename + pass-2 watches survive restart. Currently empty |
| `server/transcription-telemetry.jsonl` | append + R | `S/utils/telemetry.ts:17,70`; caller `S/routes/transcriptions.ts:306` | **Local file only — sends nowhere.** 1,287 lines, 558 KB. **140 lines are test pollution** (paths under `/var/folders/.../T/`): tests append to the real file |
| `server/brand-config.json` (bundled) | R + **W** | `S/utils/poemWuiUtils.ts:11`; written by `POST /api/poem-wui/brand-config` `S/routes/poem-wui.ts:326-327` when no managed file / no `brandConfigPath` | A request can overwrite a git-tracked repo file |
| `~/.config/appydave/brands.json` | R only | `S/utils/brands.ts:11,45`; fli-core `readBrands` in `S/utils/openContext.ts` + `S/utils/managedBrandConfig.ts:23` | Never written (`brands.ts:4`). Uses `brands.<key>.name`, `.locations.video_projects`, `.locations.ssd_backup`. 11 brands present |
| `~/.fli/machine.json` | R only | fli-core `readMachineSettings` — `S/utils/brands.ts:82`, `openContext.ts:101`, `managedBrandConfig.ts:27` | `brandRoots` override. **Does not exist on this M4** (`~/.fli/` has `studio/`, `window-state.json` only) |
| `<appydave brand root>/fli.brand.json` (`publish` block) | R + W | read `S/utils/managedBrandConfig.ts:33`; write `:81` via fli-core `updateBrandSettings` (lock `fli.brand.json.lock`, atomic) | Optimistic concurrency: `POST /brand-config` needs header `x-brand-config-version` (`S/routes/poem-wui.ts:303`), 428 if missing, 409 if changed. Version = sha256 of bytes. Hard-wired to brand `appydave` (`managedBrandConfig.ts:19`) |
| `<project>/fli.studio.json` | R only | fli-core `readIdentity`: aspect `S/utils/aspectCheck.ts:154`, languages `S/utils/transcriptionLanguage.ts:3`, code `S/utils/nextProjectCode.ts:128` | Owned by FliStudio/fli-core |
| `<project>/fli.words.json` | R + **W** | `S/routes/state.ts:268-304` (`rememberWord` :294, `removeWordAt` :304, fli-core); merged read `S/routes/edit.ts:72` | Also global `~/.config/appydave/fli.words.json` + brand `v-<brand>/fli.words.json` read via fli-core `readWords` |
| `~/.flihub/storage-activity.jsonl` | append | `S/utils/storageActivityLog.ts:23,31-33`; caller `S/routes/storage.ts:116` | Global log of hold/archive verbs (1 line here) |
| `~/.flihub/miccheck/<sessionId>.json` | W + R | `S/utils/micCheckStore.ts:39,293-299` | Written on `POST /api/miccheck/session/:id/finish` (`S/routes/miccheck.ts:170`). 3 sessions here |
| user-supplied `brandConfigPath` file | R + W | `S/routes/poem-wui.ts:276,326` | Not set in current config |

### 1b. Environment variables

| Var | Default | Where | Status |
|---|---|---|---|
| `PORT` | 5101 | `S/config/env.ts:7`; used `S/index.ts:53` | live (also `cleanupPort` kill -9 on that port at boot `S/index.ts:59-85`) |
| `NODE_ENV` | development | `env.ts:6`, `S/middleware/errorHandler.ts:46` | live |
| `CLIENT_URL` | http://localhost:5173 | `env.ts:8` | **dead** — parsed, never read |
| `YLO_BEARER_TOKEN` | — | `env.ts:11`, `S/routes/poem-wui.ts:169` | live (send-ylo) |
| `YLO_INBOX_URL` | hard-coded Supabase function URL | `env.ts:12`, `poem-wui.ts:170` | live |
| `FLITOOLS_URL` | http://127.0.0.1:7161 | `S/utils/flitoolsClient.ts:75` | live |
| `FLIVIDEO_LAUNCH_ID` + `FLIVIDEO_*` / `--brand --project --video` | — | `S/utils/openContext.ts:44`, `S/index.ts:410` | live (door 2 launch context) |
| `WATCH_DIR` | `~/Movies/Ecamm Live/` | `S/config/configManager.ts:22` | default only |
| `IMAGE_SOURCE_DIR` | `~/Downloads` | `configManager.ts:35` | default only |
| `WSL_DISTRO_NAME` | — | `S/routes/system.ts:196` | Jan-era WSL path (open in Explorer) |
| `PROJECTS_ROOT`, `HOME` | — | `S/scripts/scanProjects.ts:66` | offline script only |

### 1c. `Config` fields (`shared/types.ts:66-93`) — read/write status

Save path = `saveConfig` allowlist `S/config/configManager.ts:116-158`. Update path = `POST /api/config` destructure `S/routes/index.ts:173-198` → `updateConfig` `S/index.ts:200-261`. A second save path is the projects router setter `S/index.ts:306-312` (`Object.assign` + save — whole config).

| Field | Saved? | Updatable via | Real consumers | Verdict |
|---|---|---|---|---|
| `watchDirectory` | yes | /api/config | Ecamm watcher `S/index.ts:436`, video/segments/system routes | live |
| `projectDirectory` | **no** (derived `configManager.ts:72-77`, `index.ts:218`) | (destructured but `updateConfig` ignores it) | everywhere | live, derived |
| `projectsRootDirectory` | yes | /api/config, brands switch `S/routes/brands.ts:51`, context | ~20 server files | live |
| `activeProject` | yes | /api/config, context, brands | many | live |
| `fileExtensions` | no | — | **nothing** (watcher hard-codes `*.{mov,mp4}` `S/watcher.ts:18`) | **DEAD** |
| `availableTags` | yes | **not** via /api/config (not destructured) | `S/routes/index.ts`, query, client naming | live, read-only from UI |
| `commonNames` | yes | /api/config | naming UI | live |
| `imageSourceDirectory` | yes | /api/config | incoming-images watcher, assets | live |
| `projectPriorities` | yes (if non-empty) | projects router | `S/utils/projectStats.ts` | live (2 pinned) |
| `projectStageOverrides` | yes | projects router | `projectStats.ts:160` | live (36 entries) |
| `projectStages` | yes (if present) | — | `projectStats.ts:164` legacy fallback, **used as a map keyed by code though typed `ProjectStage[]`** | legacy / type-wrong; absent in config |
| `projectCodeHighWater` | yes | updateConfig merge `index.ts:238` | `S/utils/nextProjectCode.ts` | live (3 roots) |
| `chapterRecordings` | **no** | — | `S/routes/chapters.ts:35` (GET /api/chapters/config) | **DEAD** (FR-58 generation is 410) |
| `glingDictionary` | yes (always, `[]` default) | /api/config | `S/routes/edit.ts:76` (Gling edit-prep dictionary) | semi-live: feeds Gling edit prep only, no transcription engine (24 words) |
| `poemWuiUrl` | yes | — (hand-edit) | `S/routes/poem-wui.ts:108,243` | live |
| `brandConfigPath` | yes | — | `poem-wui.ts:60,267-326` | live-but-unset |
| `machineRole` | yes | /api/config | only echoed: `S/routes/system.ts:239`, ConfigPanel; ToolsSidebar has a TODO only | **DEAD** (read by nothing) |
| `diskThresholds` | **no** (default injected on load `configManager.ts:99`) | — | client `ProjectsPanel.tsx:698` | live as constant; **not persistable** |
| `holdingPath` | yes | /api/config, brands switch | hold/storage/openContext/archiveInventory | live |
| `publishedPath` | yes | /api/config, brands switch | storage/brands/nextProjectCode | live |
| `whisperBinary` / `whisperModel` / `whisperLanguage` | **no** | — | **nothing** in server or client | **DEAD** (B584: FliTools transcribes) |
| (legacy) `targetDirectory` | migrated away `configManager.ts:53` | — | — | migration only |

---

### 2. Watchers + background jobs

### 2a. chokidar watchers

| Name | Path / pattern | Events | Options | Emits (socket) | Defined |
|---|---|---|---|---|---|
| ecamm (separate) | `<watchDirectory>/*.{mov,mp4}` | add, unlink | `ignoreInitial:false`, `awaitWriteFinish` (`shared/constants.ts` WATCHER) | `file:new` (+ ffprobe duration), `file:deleted`; triggers aspect + sound-hole checks | `S/watcher.ts:9-75`, wired `S/index.ts:130-195` |
| zip | `~/Downloads/*.zip` | add, unlink | debounce 200 | `thumbs:zip-added` | `S/WatcherManager.ts:109` |
| incoming-images | `<imageSourceDirectory>/*.{png,jpg,jpeg,webp}` (+caps) | add, unlink | 200 | `assets:incoming-changed` | `:121` |
| assigned-images | `<project>/assets/images` | add, unlink, change | depth 0 | `assets:assigned-changed` | `:133` |
| recordings | `getProjectPaths().recordings` (hub/recordings or recordings) | add, unlink, change | depth 0 | `recordings:changed` | `:147` |
| projects | parent of project dir (brand root) | addDir, unlinkDir | depth 1, 500 ms, dotfiles ignored | `projects:changed` | `:161` |
| inbox | `<project>/inbox` | add, unlink, addDir, unlinkDir | depth 2, 300 ms | `inbox:changed` | `:178` |
| transcripts | `getProjectPaths().transcripts` | add, unlink, change | 300 ms | `transcripts:changed` | `:195` |
| thumbs | `<project>/assets/thumbs` | add, unlink, change | 300 ms | `thumbs:changed` | `:210` |

Project watchers restart when `projectDirectory` changes (`WatcherManager.ts:224-239`). Note: the layout is resolved once at watcher start — a project that flips legacy→hub (first promote creates `hub/recordings`) keeps watching the old path until project switch.

### 2b. Queues, timers, startup, shutdown

| Item | What | file:line |
|---|---|---|
| Transcription queue | In-memory `queue[]` + `activeJob`; submits to FliTools `POST` (wait:false) then polls `GET /api/jobs/:id` ~2 s; emits `transcription:queued/started/progress/complete/error` | `S/routes/transcriptions.ts:75,184-330,416-483`; client `S/utils/flitoolsClient.ts:73` |
| Pass-2 poller | `setInterval(checkPass2, 20_000)` — watches FliTools edit-grade upgrades, resubmits `tier:'edit', forceSave` | `transcriptions.ts:339-410`, interval set `S/index.ts:274` |
| Telemetry | append one JSONL line per finished job to `server/transcription-telemetry.jsonl` — no network | `S/utils/telemetry.ts:67`, `transcriptions.ts:306` |
| Aspect check queue | serial ffprobe per new take vs `fli.studio.json` aspect; `file:aspect` | `S/index.ts:157-170`, `S/utils/aspectCheck.ts` |
| Sound-hole queue | serial ffmpeg decode per new take; `file:sound-holes`; persisted to state on promote and **back-filled into `.flihub-state.json` on GET recordings listing** | `S/index.ts:141-151`, `S/utils/soundHoles.ts:114`, `S/routes/index.ts:101-115,682` |
| Watcher debounce | per-watcher setTimeout | `S/WatcherManager.ts:58` |
| Startup: port cleanup | `lsof -ti:PORT` + `kill -9` | `S/index.ts:59-85` |
| Startup: launch context | applies `--brand/--project/--video` / `FLIVIDEO_*` once per launch id | `S/index.ts:409-413` |
| Startup: FR-111 safe migration | moves `recordings/-safe/*` up into recordings and marks `safe:true` in state; rmdir `-safe` | `S/index.ts:416-433`, `S/utils/safeMigration.ts:101,154` |
| Startup: watchers | ecamm + `initAll` | `S/index.ts:436-438` |
| Shutdown | SIGINT/SIGTERM → stop pass-2 timer + clear queue (`killActiveProcess` — nothing to kill since B584), close watchers, io, http; force exit 3 s | `S/index.ts:452-480`, `transcriptions.ts:944` |
| No log file | console only (Overmind pane) | — |

---

### 3. Files written inside project folders

Layout (fli-core `classify.js` `LAYOUT_DIRS`, `projectLayoutSync`): `hub` = `hub/recordings`, `hub/transcripts`; `legacy` = `recordings`, `recording-transcripts`. Rule: `hub/recordings` exists → hub; else any of `recordings`, `recording-transcripts`, `transcripts` exists → legacy; else hub. Everything else is project-root-relative in both layouts (`shared/paths.ts:65-93`). `<rec>` / `<tx>` below = the layout's folders.

| Path (in project) | Op | Writer file:line | Trigger |
|---|---|---|---|
| `<project>/` | mkdir | `S/routes/index.ts:513` | `POST /api/projects` (folder only; hub by default) |
| `<project>/` (whole) | rm -rf | `S/routes/projects.ts:728` | `DELETE /api/projects/:code` (confirmation code guard) |
| `<rec>/<NN-S-name-TAGS>.mov` | move in from Ecamm dir | `S/routes/index.ts:293,318` | `POST /api/rename` (promote). Always `.mov` |
| `b-roll/<name>` | move in from Ecamm dir | `S/routes/index.ts:209-318` (`destination:'b-roll'`) | promote to b-roll (FR-161, deprecated) |
| `<rec>/*` rename | rename | `S/utils/renameRecording.ts:48,245` | rename/renumber/swap/split chapter: `S/routes/index.ts:1362`, `S/routes/manage.ts:178,522,652,678,711,788,839,1012,1041`, undo `S/routes/index.ts:800,817` |
| `<tx>/<base>.{txt,srt,json}` + `<tx>/engines/<base>.<engine>.*` | rename alongside take | `S/utils/renameRecording.ts:80-148`, `S/utils/transcriptFollow.ts:115,132` | any take rename; follow-on for in-flight jobs |
| `<rec>/-chapters/*` | unlink | `S/utils/renameRecording.ts:63-73` | rename deletes stale chapter videos (generation itself 410) |
| `<rec>/-safe/` | move out + rmdir | `S/utils/safeMigration.ts:101,127,154` | startup migration |
| `<tx>/*` | delete | `S/routes/transcriptions.ts:623`; `S/routes/manage.ts:346,355` | `DELETE /api/transcriptions/transcript/:f`; `DELETE /api/manage/delete-transcripts` |
| `<tx>/NN-chapter.txt` | write | `S/routes/transcriptions.ts:739-742` | `POST /api/transcriptions/combine-chapter` |
| `<tx>/*.{json,srt,txt}` | **written by FliTools, not FliHub** | (`S/utils/flitoolsClient.ts:5`) | FliHub queues |
| `-trash/<file>[-N]` | move in | incoming: `S/routes/index.ts:429,445`; take+artifacts: `S/utils/recordingArtifacts.ts:90-102` via `S/routes/index.ts:1211`; b-roll `S/routes/index.ts:593,598`; image `S/routes/assets.ts:674,686`; undo transcripts `S/utils/transcriptFiles.ts:80-88`; segment ops `S/utils/segmentOps.ts:531-532` | trash buttons, segment replace/delete, undo |
| `-trash/<date>-pre-flitools/` | **written by FliTools** (force_save) | `flitoolsClient.ts:38` | pass-2 forceSave |
| `-trash/` contents | rm | `S/utils/safeDelete.ts:83` via `S/routes/projects.ts:665` | `DELETE /api/projects/:code/trash` |
| `.flihub-state.json` | atomic write (`.tmp` + rename), allowlisted fields | `S/utils/projectState.ts:76-108` | callers: `S/routes/index.ts:105,333,519,908,966,1009,1074,1131,1225`; `S/routes/state.ts:163,227,355,387,421`; segmentOps; renameRecording; safeMigration |
| `.flihub-segment-journal.json` | atomic write | `S/utils/segmentOps.ts:228,243-244` | `POST /api/segments/op`, `/undo` (`S/routes/segments.ts:77,108`) |
| empty dirs after segment op | remove | `S/utils/segmentOps.ts:964` | segment op cleanup |
| `.chapter-overrides.json` | write / delete | `S/routes/projects.ts:470,510,512` | `POST/DELETE /api/projects/:code/chapters/override` |
| `fli.words.json` | write (fli-core) | `S/routes/state.ts:294,304` | `POST/DELETE /api/projects/:code/words` |
| `inbox/{raw,dataset,presentation}/<file>` | write | `S/routes/projects.ts:787,791` | `POST /api/projects/:code/inbox/write` |
| `inbox/**` / any subfolder | rm entries | `S/routes/manage.ts:406` | `DELETE /api/manage/delete-subfolder` |
| `assets/images/<NN-S-Iv-label>.ext` | move from `~/Downloads` | `S/routes/assets.ts:343,346` | `POST /api/assets/assign` |
| `assets/images/*.png` (clipboard) | write | `S/routes/assets.ts:759,762` | `POST /api/assets/clipboard/assign` |
| `assets/images/*.txt` prompts | write / delete | `S/routes/assets.ts:520,543,546,636` | `POST /api/assets/prompt`, `DELETE /prompt/:f` |
| `assets/thumbs/*` | write (unzip), delete, rename, reorder | `S/routes/thumbs.ts:203,209,227,344,353,418,437` | `POST /api/thumbs/import`, `/reorder`, `DELETE /:f` |
| `edit-1st/ edit-2nd/ edit-final/` | mkdir | `S/routes/edit.ts:118,147` | `POST /api/edit/create-folders`, `/create-folder` |
| edit-folder file copy/clean (FR-126 manifest) | copy / remove | `S/utils/editManifest.ts:199,224,243` | **no route imports these — dead code**; state `editManifest` still preserved/renamed (`projectState.ts:90`, `segmentOps.ts:559-586`) |
| `recording-shadows/` | — | none (only travels on hold/offload `S/utils/storageTree.ts:23-27`) | legacy, read/move only |
| `s3-staging/` | — | path exposed `S/routes/system.ts:305`; excluded from hold (`S/utils/holdUtils.ts:10`) | no writer |
| `final/` | — | read only (`finalMedia.ts`) | no writer |

### 3b. Written outside project folders

| Target | Op | file:line | Trigger |
|---|---|---|---|
| Ecamm watch dir (`~/ecamm` here) | files moved OUT (promote / trash) | `S/routes/index.ts:318,445` | promote, trash incoming |
| `~/Downloads/*.zip` | delete | `S/routes/thumbs.ts:388` | `DELETE /api/thumbs/zip/:f` (and import reads from Downloads `:194`) |
| `<imageSourceDirectory>` (~/Downloads) | write clipboard image; delete incoming | `S/routes/assets.ts:812,815,378` | clipboard/incoming, `DELETE /incoming/:p` |
| T7 HOLDING `/Volumes/T7/youtube-HOLDING/<brand>/<project>` | rsync -a in, rm local; restore rsync back; rm holding | `S/utils/holdUtils.ts:307-342,413,481`; `S/routes/hold.ts:144,261,398,534,612`; `S/routes/storage.ts:226-274,341-354` | hold, batch-offload, delete-local, delete-holding, restore-held |
| T7 PUBLISHED (`publishedPath`, here `/Volumes/T7/beauty-and-joy`) | rsync in + rm local; unarchive back | `S/routes/storage.ts:447-475,553-556,655-744` | archive, unarchive, held-archive |
| rsync excludes | `-trash/`, `s3-staging/`, `.DS_Store`, `._*` | `S/utils/holdUtils.ts:10` | **`-trash` is not carried to T7** |
| `server/*` state files | see §1a | | |
| `docs/analysis/discrepancies.{json,csv}`, `project-discrepancies.md` | write | `S/scripts/scanProjects.ts:666-822` | offline script only |

---

### 4. Real data sample (read-only)

**`server/config.json` keys (14):** watchDirectory (`~/ecamm`), projectsRootDirectory (v-beauty-and-joy), activeProject (`a01-nail-art-…`), availableTags (2), commonNames (10), imageSourceDirectory, glingDictionary (24), projectPriorities (2 pinned), projectStageOverrides (**36**: published 15, shelved 14, first-edit 3, recording 2, ready-to-publish 1, archived 1), projectCodeHighWater (3 roots: appydave d05, beauty-and-joy a01, kybernesis a01), poemWuiUrl, machineRole (`recorder`), holdingPath, publishedPath. Not present: brandConfigPath, projectStages, chapterRecordings, diskThresholds, whisper*.
- `projectStageOverrides` and `projectPriorities` are keyed by **bare folder name**, not root — not brand-scoped.
- appydave high-water `d05` while live folders go to `d13` (high-water also counts live folders, so harmless, but the stored mark lags).

**Other server files:** `.launch-context.json`, `.transcript-follow.json` (empty), `transcription-telemetry.jsonl` (1,287 lines; 140 from test temp dirs), `archive/transcription-telemetry-2025-12-16-to-2026-01-03.jsonl.gz`, and a **stray literal `server/~/dev/video-projects/v-appydave/{b93,b96}/edits/prep/` tree** — an unexpanded-`~` write from an old feature (no current code writes `edits/prep`).

**Live projects (`~/dev/video-projects`):** v-appydave 13 coded projects (d01–d13) — 11 hub, 2 empty (→hub); beauty-and-joy 1 hub; kybernesis 1 hub; aitldr 23 coded projects with **no FliHub folders at all** (FliStudio-shaped: footage/, videos/, motion/…). 10 `.flihub-state.json`, 3 `.flihub-segment-journal.json` (d01, d11, d12), 12 `engines/` dirs, 0 `.chapter-overrides.json`, 0 shadows locally. Hub sample `d08`: `-renders -trash .flihub-state.json fli.cut.* fli.resources.json fli.studio.gates.json fli.studio.json hub/{recordings,transcripts} resources videos`. Its state: `version, recordings` (19 entries, only `soundHoles`).

**Legacy on T7** (`/Volumes/T7/v-appydave-old`, 62 projects): recordings 61, recording-transcripts 61, **recording-shadows 56**, edit-* 33, s3-staging 21, assets/thumbs 18, `.flihub-state.json` 12, assets/images 5, `-chapters` 3, `-trash` 3, `-safe` 2, inbox 1. `youtube-PUBLISHED/appydave` 7 projects (legacy, incl. `.awb.json`, recording-shadows); `youtube-HOLDING/appydave` 1.


## Appendix D. Dependents, FliStudio overlap, usage signal

Method: `command grep` across sibling repos (node_modules/dist/.git excluded), live `src` separated from docs.
Not established: runtime call frequency (FliHub has no log file; no access logs exist), and whether skills are
actually invoked (no AngelEye query run). "Live code" = in a `src/` path that ships; "doc" = markdown/skill text.

### 1. External callers

### A. HTTP API callers (port 5101)

| Caller | file:line | Calls | Kind |
|---|---|---|---|
| FliStudio launch door | flistudio/server/src/launch/doors.ts:148-168 | `POST /api/context {brand,project,video?}`, `GET /api/context` (health + read) on fixed `http://127.0.0.1:5101` | **LIVE code** — the only live HTTP client found |
| FliStudio reveal | flistudio/server/src/launch/reveal.ts:25,115-117 | runs FliHub's `scripts/app.sh open` (not HTTP) | LIVE |
| FliStudio lifecycle | flistudio/server/src/launch/lifecycle.ts:38 | notes FliHub is "human-only to stop" | LIVE (comment on behaviour) |
| FliStudio ProjectHome | flistudio/client/src/screens/ProjectHome.tsx:1838 | "Open in FliHub ↗" → `launchApp('flihub', …)` (via door above) | LIVE |
| skill flivideo:flihub | appydave-plugins/flivideo/skills/flihub/*.md | see table below | skill doc (agent-driven curl) |
| ylo:ylo-titles | appydave-plugins/ylo/skills/ylo-titles/SKILL.md:152-153 | `GET /api/system/health`, **`PUT /api/projects/<code>/title`** (writes .flihub-state.json) | skill doc — a WRITER |
| ylo:ylo-description | appydave-plugins/ylo/skills/ylo-description/SKILL.md:203-204 | health, **`PUT /api/projects/<code>/chapters/03/title`** | skill doc — a WRITER |
| ylo README | appydave-plugins/ylo/README.md:92 | ".flihub-state.json is the published fact" (titles) | doc |
| brand-dave gather | appydave-plugins/brand-dave/commands/gather.md:148-152 | `GET /api/query/projects`, `/projects/<code>`, `/recordings` | command doc |
| brand-dave current-deck | appydave-plugins/brand-dave/commands/current-deck.md:76,147 | `GET /api/projects/resolve?q=` (note: wrong prefix vs `/api/query/projects/resolve`), `/api/query/projects?recent=10` | command doc |
| teletubby skill | appydave-plugins/flivideo/skills/teletubby/SKILL.md:124 | `GET :5101/api/query/projects/:code` courtesy check | skill doc |
| Teletubby app | teletubby/src/core/input-shapes.ts:139 | comment only — courtesy check is NOT done in code ("existence not checked here") | comment, no live call |
| flicut skill | appydave-plugins/flivideo/skills/flicut/SKILL.md:206 | mentions FliHub skill as sibling pattern | doc |
| archived brand-dave flihub-integration | appydave-plugins/_archived/brand-dave-skills/flihub-integration/SKILL.md | inbox/write, query/* | archived |
| apps.json | ~/.config/appydave/apps.json:11-24 | registry entry (ports 5100/5101, start_script ./start.sh, agent_start `npm run app`) | config — read by AppyRadar Sentinel port probe (tests: appyradar-sentinel/src/__tests__/parsers.test.ts:259-278) |
| locations.json | ~/.config/appydave/locations.json:382-391 | jump alias | config |
| appydave:app-query / llm-context | appydave-plugins/appydave/skills/app-query/SKILL.md:30-56 | reads FliHub SOURCE via query_apps globs, not the API | skill doc |
| AngelEye, DeckHand, Samantha, Captain's Log, Watchtower | — | no live code calls 5101/5100 (hits are logs, transcripts, entity names) | none |
| FliDeck | flideck/server/src/routes/query.ts:43-117 | its own `/api/query` (copied pattern), does not call FliHub | none |

#### flivideo:flihub skill — command docs → endpoints (all GET unless marked)
- SKILL.md — index of all below + `GET /api/query/config`, `/api/system/health`, mentions `PUT /api/projects/:code/title`, `PUT /api/projects/:code/chapters/NN/title`, `/api/rename`
- projects-command.md — `/api/query/projects` (`?filter=pinned`, `?recent=N`, `?stage=…`)
- project-command.md — `/api/query/projects/:code`
- resolve-command.md — `/api/query/projects/resolve?q=`
- recordings-command.md — `/api/query/projects/:code/recordings` (`?chapter=`, `?missing-transcripts=true`)
- transcripts-command.md — `/api/query/projects/:code/transcripts` (`?chapter=`, `?include=content`, `&format=text`), `/transcripts/:recording`
- chapters-command.md — `/api/query/projects/:code/chapters` (`?format=text`)
- images-command.md — `/api/query/projects/:code/images` (`?chapter=`)
- export-command.md — `/api/query/projects/:code/export` (`?include=transcripts`)
- read-command.md — `/api/query/projects/:code/inbox`, `/inbox/:subfolder/:filename`
- write-command.md — **`POST /api/projects/:code/inbox/write`**
- miccheck-command.md — `/api/query/miccheck/live`, `/sessions`, `/sessions/:id`
- health-command.md — `/api/system/health`

### B. Socket.io consumers
**None external.** socket.io-client imports outside FliHub: flistudio/client/src/live.ts:23 (`io({path:'/socket.io'})` = its own server), flideck, fligen, flivoice, storyline-app (each their own server), angeleye tests. No code connects to :5101's socket.

### C. File-level dependents (read/write FliHub's on-disk outputs) — the real coupling
| Dependent | file:line | Touches | R/W |
|---|---|---|---|
| FliStudio assets | flistudio/server/src/assets/assets.ts:233-237; shared/src/contracts.ts:618 | `.flihub-state.json` chapters[NN].title | Read (R4: never written) |
| FliStudio words | flistudio/server/src/capabilities/words.ts:233,278; registry.ts:288 `words.import-flihub` | `glingDictionary` in FliHub server config + each project's `.flihub-state.json` | Read (import) |
| FliStudio estate | flistudio/server/src/estate/projects.ts:33,41,66-73 | detects FliHub activity by `recordings/` or `hub/recordings/` existence | Read |
| FliStudio best-transcript / video-text | capabilities/best-transcript.ts:17,135-222; video-text.ts:121 | FliHub take transcripts (`<take>.srt`, `engines/<take>.<engine>.srt`), owner `flihub` | Read |
| FliStudio ProjectHome | client/src/screens/ProjectHome.tsx:88,145,181,1783-1786,1955 | lists recordings by chapter "as in FliHub", shows `-trash/` FliHub fills; "changing takes stays FliHub's job" | Read |
| FliStudio migrate-layout | capabilities/migrate-layout.ts:74-125 | moves `recording-transcripts/`→hub layout; refuses while FliHub has project open (asks FliHub's door) | Read + moves files |
| FliStudio project-rename | capabilities/project-rename.ts:8 | asks running apps (incl. FliHub) what's open before moving folder | Read (door) |
| FliStudio brand-publish | capabilities/brand-publish.ts:25,202 | `fli.brand.json` — both FliHub (brand-config Save, commit 69af03a) and FliStudio write it; W8 lock in fli-core brand-settings.ts:181 | **Shared write** |
| FliCut reload-transcript | flicut/src/main/reload-transcript.ts:5-6,49,138-144; shared/ipc.ts:54,454; renderer Script.tsx:34,456 | `<project>/hub/transcripts/<stem>.json` (flitools.transcript/2) after FliHub's ↻ redo | Read |
| FliCut transcriber | flicut/src/main/transcriber.ts:106-112,155 | `hub/transcripts/engines/<take>.mlx-flihub.json` | Read |
| FliCut transcript-warning | flicut/src/shared/transcript-warning.ts:59 | tells user "redo it in FliHub (↻)" — UX dependency on FliHub's redo button | Read/UX |
| FliEdit resolver | fliedit/src/main/media/resolver.ts:97 | lists `hub/recordings/` as source `flihub` | Read |
| FliTools | flitools/src/transcribe/service.ts:340-374,717-738,1474,1576-1614,1796-1825; location.ts:7-54; capabilities.ts:49,93 | WRITES into FliHub's `hub/transcripts/`; detects FliHub-made files (`ownerOf`→'flihub'); only principal `agent:flihub` + force_save may replace them; moves old ones to `-trash/<date>-pre-flitools/`; `.txt` written last because FliHub reads .txt as "done" (FR-94) | Read+Write (FliHub is a caller of FliTools :7161) |
| fli-core | src/classify.ts:37-41,106-120,288-372; recording.ts:5-6; brand-settings.ts:25-26,181; reveal.ts:10 | owns layout (`hub/` zones, LAYOUT_DIRS mirrors FliHub shared/paths.ts), naming (follows FliHub shared/naming.ts), `-trash/`, brand settings moved from FliHub's brand-config.json | Library FliHub consumes; **no 'flihub' app id/registry entry** in fli-core |
| Teletubby | src/shared/domain.ts:183-238; input-shapes.ts:27-32,134-145; SetupPanel.tsx:61,171 | stores FliHub folder name verbatim; mirrors FliHub's kebab grammar | identity only, no file/API read |
| FliCast | src/core/ops/project.ts:447; open-context.ts:101 | "flihub-demo" only as example string | none |
| ylo plugin | ylo/references/brand-input-contract.md:18 | `flihub/server/brand-config.json` "stays as FliHub's fallback" | doc |

### 2. FliStudio features that now duplicate FliHub

| Feature | FliHub | FliStudio evidence |
|---|---|---|
| Brand switcher | BrandSwitcher.tsx, routes/brands.ts (FR-162) | screens/BrandPicker.tsx; registry.ts:168 `brands.list` |
| Project list + create + next code | ProjectsPanel, NewProjectForm (FR-163 code high-water) | screens/Projects.tsx:24-64 (create, adopt, CodeChip); estate/projects.ts:159-213 `codeInUse`, `allocateCode`, `listBrandProjects`; registry.ts:169-172 |
| Archived-range awareness | FR-163 archived/ scan | estate/projects.ts:128-182 |
| Project rename | (FliHub: does NOT rename) | registry.ts:173 `project.rename` |
| Stages / pipeline | projectStageOverrides, stage chips | ProjectHome.tsx:71-76,1021 PipelineStrip (stages by app: Recording = flihub+flicast) |
| Recordings view by chapter | RecordingsView | ProjectHome.tsx:88-181,1783-1841 (read-only mirror "with FliHub's layout"; edits stay FliHub's) ; registry.ts:175 `takes.list` |
| Chapter titles | ChapterPanel, PUT chapters/:NN/title (FR-157) | reads them: assets.ts:233 |
| Transcripts view / queue / settings | TranscriptionsPage, /api/transcriptions | components/Transcription.tsx; capabilities/transcription.ts (FliTools settings + queue); registry.ts:216-218; `video.text` best-transcript ladder |
| Word list / dictionary | glingDictionary, project words (5e8edca) | components/Words.tsx; registry.ts:284-288 incl. `words.import-flihub` |
| Trash count + empty | header trash pill (ae2d9b1, 1b6b920 "matching FliStudio") | components/TrashReview.tsx; registry.ts:179-181 `trash.list`, `project.empty-trash`, `brand.empty-trash` |
| Thumbnails | ThumbsPage, routes/thumbs.ts | components/ThumbPool.tsx, ThumbLightbox.tsx; publish/launch capabilities |
| Publish / brand publishing settings | brand-config editor (69af03a), poem-wui send-ylo | components/Publish*.tsx, BrandPublishPanel.tsx, YouTubeUpload/UploadWizard; registry.ts:243-268 publish.*, youtube.*, brand.publish.* |
| Assets / resources | AssetsPage, InboxPage, inbox write | components/Resources.tsx; registry.ts:174 `assets.list`, 275-283 resources.* |
| Reveal in Finder | /api/system/open-folder | registry.ts:215 `path.reveal`; fli-core reveal.ts:10 "like FliHub's" |
| Layout migration | (FliHub never migrates) | `project.migrate-layout` registry.ts:192 |
| Hold / archive / T7 offload | hold.ts, storage.ts, archive endpoints | **no equivalent found** in FliStudio capabilities (only archived-range code checks) |
| Ingest / naming / Incoming / segment ops / MicCheck / watcher | core FliHub | **no equivalent** — FliStudio defers ("Changing takes … stays FliHub's job", ProjectHome.tsx:1786) |

### 3. Git activity

- Since 2026-07-01: 193 commits (Aug 33, Sep 109, Oct 51). **Zero commits 2026-04-16 → 2026-08-18** (last pre-gap: 3b3b2f1 2026-04-16 storage-panel).
- Touched Aug–Oct (live features):
  - Recordings / Incoming / naming: FR-174 Rename·Keep/Discard cards (10-25/26), FR-173 trash restore order, CT-0107 guarded segment ops + undo journal (10-08), renumber, + tag, inline rename tags (10-12), FR-156 delete, FR-154 orientation playback, aspect warning (09-23/27), sound-hole flag (10-04)
  - Transcription: B584 → FliTools (09-27), redo ↻ per row (10-12), job follows renamed take, engines/ copies (10-04), health
  - Chapter/project YouTube titles FR-157 (08-30), FR-168 ships per-chapter (09-08)
  - Brand switcher FR-162, project codes FR-163 (09-03..25), hub layout + fli-core pins (09-22..10-29), brand-config / fli.brand.json (10-06, 10-29 W8)
  - Open contract W3 `/api/context` (09-15), loopback-only security (09-23), trash pill (09-23, 10-05)
  - MicCheck (08-26..29), words list (10-04)
  - Removals: shadows (09-04), relay + git sync (09-22), chapter previews 410 (09-15), b-roll deprecated (09-22)
- Untouched since ≤ April (last-commit dates): assets.ts / thumbs.ts routes (03-19), AssetsPage, InboxPage, ThumbsPage, TranscriptionsPage, TranscriptModal, ChapterContextPanel, ClipboardPasteModal, ApiExplorer, DamHelpPanel, DeveloperDrawer, RecentlyNamedStrip, TranscriptSyncPanel, MockupsPage (03-24..26), HoldDeleteModal (04-08), PoemWuiPage, ProjectDeleteModal (04-12), developer.ts (02-13). Hold/archive/storage untouched since 04-16.

### 4. Usage signal from rebuild docs

From DEAD-ENDS-AND-PAIN.md (230 features, 64 dead ends, 23 still-present-but-unused):
- Storage hold/offload/archive: David verbatim "I don't know where to find anything for doing the archives… how to put stuff on hold… restore… delete locally. There's no unified approach." Three UIs built, two deleted; archive-inventory/batch-offload/batch-delete endpoints kept but unused.
- Manage tools: F003 "Tools bolted onto a page that was never designed to hold them" — SlideOutDrawer repudiated; inline editing (B047) won.
- Unused residue: FR-126 edit manifest, API Explorer/apiRegistry (stale), scanProjects.ts, RelayBrowser, Pino, zod env, RecordingState.stage, MockupsPage registry drift, FliLaunch triage (never committed).
- Pivot: FliHub moved from "David's own tool" to "source of pre-calculated truth consumed by other apps" (FliLaunch/ALS) — but stage was a manual label that drifts.
- 2026-04-12: decision to rebuild from scratch (v2 requirements + Baku spec), then 4 months idle.

From audit/live-app-findings.md:
- L5: 47% of stage overrides dead; `shelved`/`archived` are write-only — David shelves by MOVING the folder to `archived/`, so those filter chips always show zero.
- L1: public query API advertises an abandoned stage vocabulary; L4: brain doc points at an endpoint that never existed.
- L12: filename preview lies — likely cause of "rename feels untrustworthy".
- L14: 153 elements use colour classes that produce no CSS (theme inconsistency).
- L15: of 7 client socket listeners, `file:renamed` and `file:error` are dead.

Net: David uses FliHub *on recording days* for ingest → name → chapter/segment management → transcription redo → titles; he does not use (or can't find) storage/archive, relay, shadows, b-roll, API explorer, mockups, edit manifest.
