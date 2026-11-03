# Story Pilot ↔ Captain's Log: what to store, what to show live, what never to copy

**Purpose**: Running design note (David, 2026-11-03, from `flivideo-roamy`). It says how a Captain's Log (CL) capture
used as a Story Pilot source maps into FliVideo's own structures without rebuilding CL inside FliStudio.

**Status**: OPEN. David is still sending visuals; this file grows as he does. Nothing is built yet: no go given.

## What David saw (d13-overlay-pilot, source 01 "Jan, and the tool Joy was waiting for")

- The source is badged **CAPTURE**. Nothing says "Captain's Log", so he didn't recognise it as one.
- **No way to open it.** The panel prints an agent instruction to a human:
  "read it in Captain's Log (captains-log:find, capture_get B663). Story Pilot does not read Captain's Log yet."
- **CL's own screen explains more** than our panel does: synopsis, date, length (1h 08m), source (Plaud),
  signal (DIRECTION), tags and the transcript.

## The two shapes as they are today (measured 2026-11-03)

**Our record**: `v-appydave/d13-overlay-pilot/fli.resources.json`, id `r_86fddcdf9c`:

| Field | Value | Whose judgement |
|---|---|---|
| `kind` | `capture` | ours |
| `title` | "B663 — David × Jan scope the quick overlay tool" | ours (hand-written) |
| `ref` | `{schema: "captains-log", id: "B663"}` | **the pointer** |
| `meta.why` | why it matters *to this video* | ours: CL cannot know this |
| `meta.channel` | `plaud` | **copied from CL** (duplicates CL `source`) |
| `status`, `audience`, `added`, `changed` | | ours |

**CL capture** (MCP `captures_search`, metadata tier): `code`, `title`, `synopsis`, `tags`, `signal`, `createdAt`,
`state`, `stateBy`, `lastTouchedAt`, `sourceId`, `source`. The CL screen also shows duration, derived/suggested
tags, engagement and the transcript (`capture_get`, the expensive tier).

⚠️ A CL `title` is often just a timestamp (B663's is "2026-10-28 10:03:53"). The **synopsis** is CL's real
description, and our hand-written title is the readable one. Never replace ours with CL's title.

## The rule: three tiers

| Tier | Fields | Why |
|---|---|---|
| **1. Store (ours)** | `ref.id` (the code), our `title`, `meta.why`, `status`, `audience`, `added`/`changed` | judgements only FliVideo can make, plus the pointer |
| **2. Show live, don't store** | synopsis, `createdAt`, duration, `source`, `signal`, `state`, plus an **Open in Captain's Log ↗** link | CL owns these and they change (state, enrichment). Fetch when the panel opens |
| **3. Never copy** | transcript, tags (stated/derived/suggested), engagement | CL's ontology and bulk. Copying it is how you end up rebuilding CL |

**One write-back, not a copy:** when a capture is used in a video, record provenance in CL
(`capture_mark_used`, `usedBy: "<project> Story Pilot"`). CL can then show "used by d13", and nothing is duplicated.

`meta.channel` is a tier-2 field stored in tier 1. Leave it (harmless), but stop writing it for new captures.

## The deep link (exists today)

CL opens a capture from `/?open=<CODE>` (`client/src/captures/CaptureList.tsx:46–53`, code must match `^[A-Z]\d{3}$`).
For B663: `https://mac-mini-m2.tail1acb0f.ts.net/?open=B663`. Verified opening in Chrome from Roamy, 2026-11-03.
Build it from config (`CAPTAINS_LOG_URL`), never hard-code the host.

## Panel changes this implies (proposal, not approved)

1. Badge `CAPTURE` → **`CAPTAIN'S LOG · B663`**.
2. Replace the agent-instruction sentence with **Open in Captain's Log ↗** (the deep link).
3. Under our title and why, a live strip: synopsis · date · length · source · signal · state.
   If CL is unreachable, say so in one line and keep showing tier 1.

## Not yet verified

- That the FliStudio server on the M4 can reach CL on the M2 (`CAPTAINS_LOG_URL` set on the M4? Tailscale
  reachability from that process).
- Whether `captures_search` returns duration (the screen shows it; the metadata row above did not).

## Session sources (David's questions, 2026-11-03, d13 source 02 "the spec morning")

A **SESSION** source is a Claude Code conversation (here `8aa7c642`, named `overlay-pilot-spec`, 28 Oct). That one was a
spec-writing session, not a coding session. David couldn't tell from the panel.

- **SYNTH** = the one-line "why it is here", written by an agent (`by agent:claude-code`). Its job is to say why the
  source matters to *this* video so David doesn't have to read 58k characters. One sentence is the design, but nothing
  on screen says so.
- **RAW** = the words as said. For a session it shows **only David's turns** ("David's own turns · 58,187 characters");
  Claude's replies are removed. Problems: only the first paragraph of each turn says "David:", so continuations look
  unattributed. Nothing says Claude's side is hidden. Image placeholders leak through (`[Image #3][Image #4]…`).
- **Not a JSON viewer.** The source is a `.jsonl` transcript. A JSON tree would show tool calls and plumbing, not the
  conversation. Better: a chat-style view, with David's turns shown and Claude's turns folded (one click to expand), and
  the session's kind and purpose in the header.

Proposal (not approved): label RAW "Your words only. Claude's replies hidden [show]", mark every David paragraph, strip
`[Image #n]` placeholders, and badge the session as "Claude Code session · spec · 28 Oct · overlay-pilot-spec".

## Dossier sources (David's questions, 2026-11-03, d13 source 03 "the decisions, in David's words")

Badged **DOSSIER**, but it is **not** a ChatGPT download and **not** a synopsis. It is the Overlay Pilot spec file,
`flivideo/flistudio/docs/planning/overlay-pilot/spec.md` (resource `r_8fed973320`, `kind: "dossier"`), written by the
Claude spec session on 28 Oct (commits f24fa5f, b4c9164). The Reader renders its Markdown in full.

- "Dossier" clashes with Captain's Log, where a dossier is a ChatGPT-conversation write-up (e.g. B686). David read it
  that way. The kind should say what it is: **spec / document**, with the file name and who wrote it.
- The bold block above the rule is the spec's **header card**, i.e. the document's state, not the story:
  Status (stage: spec, handed to `flivideo-orch`) · Name (the ruled name R16 + where the code lives) · Session (the
  Claude session that kept it) · Merged (an older brief folded in, with David's approving quote) · One-line take (the
  idea in a sentence). "Naming" below the rule is the first body section (name candidates in David's words, collisions).
- For a story, only the one-line take and the 👤 quotes matter. Proposal (not approved): for document sources, show the
  one-line take plus David's 👤 quotes first, and fold the header card and full body behind "Open the document".

## Session RAW: the 60k cut and a filter leak (d13 source 04 "the build, the check that lied, and v2")

- **"(the first part shown)"**: `modules/storypilot/server/story.ts:358` `READ_LIMIT = 60_000`. A session's David-only text
  over 60,000 characters is cut at 60k, and the Reader has no way to see the rest. Source 04 is 79,931, so ~20k is
  never shown. A cut like this should at least offer "show the rest" or open the transcript.
- **Leak**: the David-only filter (`story.ts` ~:361, "never tool results, pasted blocks, images or messages from other
  sessions") lets **loaded skill text** through as if David typed it. Source 04 shows "David: Base directory for this
  skill: …appytron-conventions … # AppyTron conventions…". Claude Code injects skill bodies as user-role messages (to
  check: `isMeta` / the "Base directory for this skill" prefix); those should be dropped like tool results.
- **Send to session box** (the chat box, commit 136bb92) renders **below the whole Story Pilot screen**
  (`ProjectHome.tsx`, after `client.Screen`), so it sits at the very bottom of the page, folded. David didn't find it.

## The 60k cut also reaches the AI (David: "will this be a problem for building a story?")

Yes, in a bounded way. `story.source.read` returns the same clipped text, and `flivideo:storypilot-prep` (SKILL.md :88)
uses it when it is unsure about a source. It mostly places sources from their title and why line, and for long sessions
it is told to use `abridge` / `sesh:session-archaeology` (full transcript). Risk: endings are often the outcome (source
04 "…and v2"), so an AI building from the clipped text tells the story without its ending, unwarned. Fix: keep 60k as
the display limit, let agent callers page (`offset`) or ask for full text, and add "show the rest" for David. (The
skill already says to skip "Base directory…" turns: the skill-text leak, worked around in instructions, not the app.)

## Note sources and the label tangle (d13 sources 07, 08)

- **NOTE** (07 "the chin bug, and the trackers already built", `r_d48036acd2`): text an agent wrote **straight into
  the project**. No file or recording sits behind it, which is why "No raw words here". Two SYNTH layers: the note
  body (by `flivideo-orch`, the facts of the day-two chin fix) and the one-line why (by `agent:storypilot-dev`).
  "Written in `overlay-chin-dev`" names the session it came out of, but that session is not itself attached as a source.
- **Label tangle**: 08 is badged CAPTURE but is a **ChatGPT dossier** (CL B670, channel `chatgpt`), while 03 is badged
  DOSSIER and is a spec file. The kind badge describes storage (where it lives), David reads it as content (what it is).
  Proposal: badge = what it is (Plaud recording · Claude session · ChatGPT dossier · spec · agent note); storage goes in
  "Where it came from".

## David thinking out loud: synth + canonical, and how much of the canonical (2026-11-03, not a ruling)

David asked for these to be collected, not answered yet.

- He has been sending things from chat conversations into Story Pilot and doesn't know whether a skill did it. Open:
  which path attaches sources today (skill? agent verb? by hand?), and is it the same every time?
- A story wants **synthesised** information *and* the **canonical** data it came from.
- A conversation can be megabytes. Nobody wants the whole canonical record; they want **the canonical text around where
  the synthesis came from**, as context.
- Unsure whether that canonical slice should be **sent** (copied in) or only **referenced** (a pointer to the spot).

Angles to weigh later, not decided: a synthesis that carries anchors into its raw source (session + turn, capture +
timestamp); reading a window around an anchor instead of the first 60k; copy vs pointer per source kind (a local
transcript vs a Captain's Log capture on another machine); and how this meets the three-tier store/live/never rule above.
