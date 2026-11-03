---
created: 2026-11-03
timestamp: 2026-11-03T11:10+07:00
---
# Brief: spike — "send to session" box in FliStudio (2026-11-03)

**From:** `flivideo-orch` (Swagger). **To:** `storypilot-dev` (after the angle-proposals unit is reported). Report to
`flivideo-orch` by name. **Go:** David 2026-11-03 ("could we have a field in the application… if I type into it and press
send, it would actually tap into one of my Claude terminals… we just need to do it as a test"; then "go do everything").

## The idea to prove
While David field-tests a page, he types an instruction into a small box, picks a Claude session by name, presses Send,
and the text lands in that session's prompt as if he had typed it. Proof first; no design polish.

## Smallest slice
- Server route (FliStudio server, M4 only, localhost): `GET` lists live tmux session names (`tmux ls -F '#S'`);
  `POST {session, text}` runs `tmux send-keys -t <session> -l <text>` then `Enter`. Use `execFile` with an args array (no
  shell string). Validate `session` against the live list; cap text length; refuse empty text.
- Client: one small "Send to session" box (session dropdown + textarea + Send) on the Story Pilot page only, behind a
  dev flag or a small disclosure so it doesn't clutter the page. Show "sent to <name>" or the error.
- Record each send to the project's notes (`fli.notes.jsonl` pattern, `by: human:ui`, `kind: session-send`) so the field
  test leaves a trail — reuse the existing field-trial/notes capture if there is one; say which.

## Proof
Start a throwaway tmux session `spike-echo` running `cat`, send text from the box in a real browser, show it arrived
(`tmux capture-pane`). Screenshot to `/Users/davidcruwys/dev/ad/flivideo/docs/reports/proof-2026-11-03/send-to-session-*.png`.
Do NOT send into any real Claude session during the proof. Kill `spike-echo` after.

## Gates and limits
Own branch from main in your worktree; typecheck, `npm test`, targeted e2e only. Do not merge or restart. Security note in
your report: who can reach the route (localhost only? FliStudio also serves on the tailnet at :7150 — say whether the route
is reachable from there and recommend a guard). Report branch + commit, tests, screenshot, and that security note.
