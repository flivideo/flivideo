---
type: reference
tags: [flivideo, ecosystem-research, candidate, B686, teleprompter]
description: "Leading one or two teleprompter apps, compared, with the agent-drivable test."
created: 2026-11-03
timestamp: 2026-11-03T12:30+07:00
---

# Teleprompter software (Teletubby alternatives)

**Purpose**: Leading one or two teleprompter apps, compared, with the agent-drivable test.

**For Agents**: Research only (B686 B2, 2026-11-03). *Observed* = read in repo or via `gh api`; *Inference* and *Lean* are B2's and **not approved**. Anything unread is **UNVERIFIED**. Index: [../03b-capability-landscape.md](../03b-capability-landscape.md).

Selection: GitHub search by stars for "teleprompter", 2026-11-03. Two chosen: the most-starred actively maintained desktop app (Textream) and the leading cross-platform dedicated app (QPrompt). Others seen: notchprompt 1,393★ (macOS notch, MIT), Imaginary-Teleprompter 299★, manifestinteractive/teleprompter 383★ (last push 2024-03).

## 1. Textream
- **Repo**: https://github.com/f/textream (clone `2c02f3e`).
- **Licence**: MIT. **Stars / last commit**: 4,220★, pushed 2026-09-06, 79 open issues.
- **Agent surface** *(Observed, README)*: "Remote Connection" HTTP + WebSocket server; **Director Mode** on port 7575 where a browser can write and push scripts and watch word progress at 10 Hz; `textream://read?text=...` URL scheme. All local-network, no relay server. Not JSON-RPC, but a real programmable surface. **UNVERIFIED**: auth on the Director port (README says "only on a local network and with devices you trust").
- **Security**: scoped scan CLEAN (0 hits). Unauthenticated LAN listeners when enabled; keep on tailnet/localhost. macOS Swift app; not built.
- **Two questions**: (1) *Elegant?* Strong: voice-tracked word highlighting, notch/overlay UX. (2) *Agent-drivable safely?* Yes via URL scheme and Director HTTP/WebSocket, given trusted network.
- **Outcome lean (not approved)**: *absorb ideas* (Director push-a-script flow maps onto Story Pilot → Teletubby); candidate to *add alongside* Teletubby; *replace* only if Teletubby's own features are subsets.

## 2. QPrompt
- **Repo**: https://github.com/Cuperino/QPrompt-Teleprompter (clone `47711f3`).
- **Licence**: GPL-3.0. **Stars / last commit**: 620★, pushed 2026-11-02, 144 open issues.
- **Agent surface**: *Observed* — Qt/QML cross-platform app with global hotkeys and an abstract input-source layer (`src/globalhotkeys.cpp`, `abstractinputsource.*`). **No network/remote API found in README or file names; UNVERIFIED** (not code-audited). Likely scriptable only by keystroke.
- **Security**: scoped scan CLEAN (0 hits). Not built.
- **Two questions**: (1) *Elegant?* Mature for pro-prompter hardware use (mirroring, remote hardware inputs). (2) *Agent-drivable?* Not demonstrated.
- **Outcome lean (not approved)**: *none*.

## Comparison
| | Textream | QPrompt |
|---|---|---|
| Stars / activity | 4,220★, 2026-09-06 | 620★, 2026-11-02 |
| Licence | MIT | GPL-3.0 |
| Platforms | macOS, iOS, iPadOS | Win/Mac/Linux/iOS (Qt) |
| Agent-drive | HTTP+WebSocket Director, URL scheme | hotkeys only (UNVERIFIED) |
| Script push | Yes (Director) | file open |
| Voice follow | Yes (mic tracking) | scroll-speed based (UNVERIFIED) |
| Fit to Teletubby | closest in spirit | alternative engine |
