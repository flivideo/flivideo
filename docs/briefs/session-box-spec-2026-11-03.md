---
created: 2026-11-03
timestamp: 2026-11-03T12:00+07:00
---
# Spec page (growing): the FliStudio "session box" — talk to a Claude session from the app (2026-11-03)

**Status: COLLECTING David's ideas through the day. v1 build waits for his go.** Owner: `flivideo-orch`.

## David's framing (verbatim anchors, 2026-11-03)
- "if I type into it and press send, it would actually tap into one of my Claude terminals"
- "not meant to be a full-blown chatbot. It's really just a window into the field I'm typing into" — "maybe two or three
  messages might be useful"
- Target changes with context: FliStudio code talk → `flivideo-orch`; reviewing D13 → `d13-overlaypilot-video`; or a new one.
- "the ability for older sessions, especially if they were started fresh from FliStudio… to clean up over time"
- "an extension of the concept of field testing, which is kind of live chat… whether this is smart… or a mess"

## Spike result (branch `send-to-session`, 962b1b8 + ebe2a15, NOT merged)
- Works: send into a named tmux session; last 3 messages read back from the transcript; per-project remembered target;
  every send logged to `fli.notes.jsonl` (`change`, target `session-send`). Proof:
  `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-03/send-to-session-1-sent-to-spike-echo.png`.
- Security: FliStudio :7150 is reachable from the tailnet (Vite `host: true`, tailscale serve :8443), so this route is
  remote code execution on the M4 unless guarded. Guard built: door token + every XFF hop loopback + refuse tailscale-*
  headers; needs `xfwd: true` in the Vite proxy and a Vite restart to take effect.

## Not built — ideas for v1
- New session from the box: `box-` prefix, chosen cwd, checker-validated launch line, human-confirmed.
- Reaping: list `box-*` with `#{session_activity}`, "stop idle > N h" on David's click only; never other sessions.
- Chat stream feel (last N turns), field-test link (page/area David was on when he sent).

## Ideas log (append as David talks)
- **12:00 — point-and-ask (BACKLOG, needs David's approval).** David: "we already have Command+Shift… to point at an area of
  the screen… for adding notes… could we have another modifier, maybe Command+Option+Shift, that does exactly the same thing,
  but this pops up as a little modal?" Existing gesture: `client/src/components/noteGesture.ts` (⌘⇧ hold → targets with
  `data-note-target` highlight → click opens the note box; any other key spoils the hold — ⌥ would need to be allowed).
  Orch rec: **one gesture, two outcomes** — keep ⌘⇧-click; the note box gains "→ ask <session>" next to Save, so an ask is a
  note that is also sent, carrying the pointed-at target (entity, field, region, label) as context. Alternative: ⌘⌥⇧-click
  opens the session modal directly. The pointed-at target is the piece that answers "knowing what part of the interface you're on".
