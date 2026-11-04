# Element chat: kick-off document (first pass)

**Purpose**: Starts the element-chat programme: a chat panel in any app that talks to a chosen Claude Code session about
the element David points at. It records David's rulings of 2026-11-04 and the history, and sets out the stages. It is
not a spec and not a go to build.

**For Agents**:
- Read before any analysis, spec or build on in-app chat, "send to session" or element selection.
- This is a **multi-app programme**: analysis → spec → multi-app build → unit tests → UAT → quality review. Do not skip
  to building.
- The field tester (⌘⇧ hold-and-click notes) is a **different job** (see §2). Don't merge them.

*Status 2026-11-04: kick-off written by `flivideo-roamy`. Next stage: analysis (§7). Nothing is built beyond today's
spike.*

## 1 · History (what was agreed vs built)

| When (2026-11-03, +07) | What | Outcome |
|---|---|---|
| ~10:20 | Send-to-session spike: "if I type into it and press send, it would actually tap into one of my Claude terminals"; "not meant to be a full-blown chatbot… a window into the field I'm typing into" | Built and merged: tmux send plus last 3 turns, door-token and loopback guarded (`flistudio/server/src/routes/sessions.ts`, `client/src/components/SendToSession.tsx`) |
| ~10:40 | Point-and-ask, logged in `docs/briefs/session-box-spec-2026-11-03.md`: "could we have another modifier, maybe Command+Option+Shift… but this pops up as a little modal?" | Logged as "needs David's approval", then never raised again. **Not built** |
| evening | W2 §E moved the box to Story Pilot's header | Built. Still sends **no element context** (brand and project go only into the notes log) |

David's original message could not be found verbatim in any M4 or Roamy transcript. The spec's quote is orch's
transcription.

## 2 · Two jobs, kept apart

| | Field tester | Element chat |
|---|---|---|
| Purpose | Observations to improve prompts and code | Change the data in front of you now |
| Timing | Batch, later | Live |
| Live session | No | Yes |
| Output | Notes (`fli.notes.jsonl`) | Changed data, through the session that built it |
| Gesture | **⌘⇧ hold-and-click** (stays here) | **"Select an element" button** inside the chat panel |

## 3 · David's rulings (2026-11-04)

- **Home: the boilerplate level.**
  - Element chat belongs in AppyStack (web) and AppyTron (Electron).
  - Prototype it in `@flivideo/core` plus FliStudio first, then move it up the stack.
  - Cover both web and Electron UI.
  - Captain's Log is a known non-Fli consumer.
- **Transport:**
  - The **Claude Agent SDK** as well as today's tmux send-and-read.
  - Either way, the session in the terminal still does the work and drives the app. The panel only talks to that
    session.
- **Use cases:**
  - a FliStudio extension (Story Pilot);
  - FliStudio's video launch area;
  - maybe thumbnail building;
  - **Teletubby** (Electron): fixing the script mid-recording.
- **Layout:**
  - The chat slides out from the **left**, as one context in a collapsible, switchable **left rail**, like VS Code's
    activity bar (files / plugins / chat).
  - Content stays in the middle.
  - Right-hand panels still **push** content in.
  - Follow other apps' conventions.
- **Selecting:**
  - A "select an element" button inside the pinned chat panel, as Claude Design does it: click the button, then click
    the element. The element is attached as context.
  - ⌘⇧ stays with the field tester. This retires the earlier "what should ⌘⇧-click do" question.
- **Not shared:** the send-to-terminal power.
  - Typing into a terminal is full control of the machine, so it stays **one guarded route**.
  - Other apps call that route; none gets its own copy.

## 4 · The pieces

```
 app (web or Electron)                                   machine
┌───────────────┬─────────────────────┬────────┐       ┌──────────────────────────┐
│ left rail     │ content (middle)    │ right  │       │ ONE guarded route        │
│ ▸ files       │                     │ panels │ ───▶  │  tmux send + tail  ─┐    │
│ ▸ chat ◀ open │  [element] ◀ select │ (push) │       │  Agent SDK session ─┼─▶ Claude Code session
│   to: session │                     │        │       └─────────────────────┘    │  (does the work,
│   📎 element  │                     │        │                                   │   drives the app)
└───────────────┴─────────────────────┴────────┘
```

| Piece | Shared? | Notes |
|---|---|---|
| Left rail plus chat panel UI | Yes, at boilerplate level (prototype in `@flivideo/core`) | Web and Electron |
| Select-an-element mode | Yes | Needs semantic element identity (see `docs/research/semantic-element-identity-2026-11-04.md`) |
| Element payload format | Yes | app, screen/URL, element id, what it is, the data or island it shows, its canonical home |
| Session picker plus last-N turns | Yes | Today's per-project remembered target is a start |
| Send route (tmux / SDK) | **No**: one guarded route per machine | Door token, loopback only |
| Element ids and their meaning | No: each app owns its own | |

## 5 · Open questions for the analysis stage

1. **Agent SDK vs tmux:** does the SDK attach to an existing interactive session, or does it start its own? What does
   "the session in the terminal still does the work" mean for each transport?
2. **Electron transport:** in AppyTron apps (Teletubby, FliCut), is the route reached over the app's own main process
   or over HTTP to a local daemon?
3. **Captain's Log** runs on the M2: which machine's sessions can it talk to?
4. **Session picker default:** "the session that built this data" from W4's build record, or the last one used?
5. **What counts as an element** depends on the semantic-identity work.
6. Existing AppyStack / AppyTron conventions for a left rail, and Claude Design's select-element pattern: study both
   before the spec.

## 6 · Out of scope for now

Building anything; the field tester; new sessions started from the panel; reaping old sessions; changes to the guard.

## 7 · Stages

| Stage | Output | Who |
|---|---|---|
| 1 Analysis | answers to §5, conventions survey, the Claude Design pattern | M2 worker via orch |
| 2 Spec | one spec page (AppyDave artifact) with the payload schema | orch, David approves |
| 3 Build (multi-app) | `@flivideo/core` + FliStudio first, then AppyStack / AppyTron, then Teletubby | M2 |
| 4 Unit tests | per package | M2 |
| 5 UAT | David, on Story Pilot and Teletubby | David |
| 6 Quality review | `dev-team:delivery-review` | orch |
