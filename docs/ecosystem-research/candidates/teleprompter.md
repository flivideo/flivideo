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

## Experiment X5 — 2026-11-03

**Verdict: PARTIAL — security half answered (FAIL on "restricted to trusted network"); script-push and word-progress half NOT proven (UNVERIFIED).** 05's pass test needs both.

**Setup** (M4): Textream **v1.7.1**, `Textream.dmg` from https://github.com/f/textream/releases/tag/v1.7.1 (sha256 `b1225e2d…15b9`), Developer-ID signed + notarized (Fatih Akin), MIT. Installed in `/Applications/Textream.app`. Director enabled by `defaults write dev.fka.textream directorModeEnabled -bool true` + relaunch (key found in the binary and `NotchSettings.swift`). Scratch: `~/dev/upstream/scratch/X5/`.

**Observed — bind and auth**
- `lsof`: `TCP *:7575 (LISTEN)` (HTTP) and `*:7576` (WebSocket) — **all interfaces**, not loopback. Source agrees: `DirectorServer.swift` creates `NWListener(using: .tcp, on: port)` with no interface restriction.
- A 64-hex `AUTH_TOKEN` is required as first WebSocket frame; a wrong token is closed. **But the token is embedded in the HTML served by unauthenticated `GET http://<mac>:7575/`**, so the token protects nothing: the M2 reached `http://100.82.235.39:7575` over Tailscale, fetched the token, and the WebSocket accepted it (no close). Anyone on the LAN/tailnet can therefore send `setText`/`stop`. Traffic is unencrypted (README says so).
- Protocol (README): `setText`, `updateText{readCharCount}`, `stop`; server broadcasts `{words, highlightedCharCount, totalCharCount, isActive, isDone, isListening, lastSpokenText, audioLevels}` at ~10 Hz. So word progress *is* script-readable by design.

**Observed — the failure to prove push/progress**: pushing d13's script (1049 words, `script/storypilot/project/script.md`, copy) with `setText` made the app **hang its main thread** in `-[AVAudioEngine inputNode]` (`sample` output); the HTTP and WS listeners then stopped answering, 0 state frames received. Reproduced after restart, and again with `listeningMode=classic`. Probable cause (Inference, not verified): the mic / speech-recognition permission prompt cannot be answered because the M4's screen was **locked** (`CGSSessionScreenIsLocked = true`, screenshot black) — or Ecamm's audio helper holds the input. A human at an unlocked screen granting Microphone + Speech access would settle it. `textream://read?text=` was **not** tested (same code path would start the mic).

**Cleanup**: Director switched back off (`directorModeEnabled=false`), app relaunched and left open, **no listeners** (`lsof` count 0), no d13 script loaded.

**What FliStudio would need** (Inference): do not enable Director on a shared network as-is; if added, bind via a firewall/Tailscale ACL or front it with a FliStudio-owned proxy; prefer the `textream://` link-out for send-to-prompter. Re-run the push with mic permission granted before any lean change.
