# Ticket: FliTools describe service (description as a service) — 2026-10-31

**For:** FliTools (its own build, its own repo). **From:** the B-roll Pilot v1 build (FliStudio extension #3, branch
`broll-pilot`). **Ruled by:** flivideo-orch, delegated by David, 2026-10-31 (B-roll Pilot spec §5.3, Q3, Q11).
**Status:** not started. B-roll Pilot's client side is built and tested against a stub; it works without this
service (assets wait for Claude Code) and starts using it the day these verbs answer.

## What it is

The sibling of transcription-as-a-service (`/Users/davidcruwys/dev/ad/flivideo/docs/briefs/transcription-as-a-service.md`):
**send frames, get descriptions back.** No app describes images itself. B-roll Pilot only enqueues frames and reads the
results back.

```
 machine running FliStudio (M4)                         named describe worker (M2 first → Roamy fallback)
 B-roll Pilot ─ describe.submit ─▶ local FliTools ── push jpg + sha ──▶ FliTools: queue → memory gate → qwen-video
 B-roll Pilot ◀─ describe.job ──── local FliTools ◀── poll result ──── (Qwen3-VL-8B-Instruct 4-bit, mlx-vlm)
```

## Rules (carried over from transcription-as-a-service)

1. **One job at a time.** The worker runs a single serial queue: never two descriptions in parallel. A 12-frame cast
   is 12 jobs in line. (A Qwen pass peaks at 8.2 GB — brains `model-routing/by-modality-video-understanding.md`.)
2. **Never on the FliStudio machine.** The worker is named by ONE setting in `~/.config/appydave/flitools.json`, M2
   first, Roamy as the fallback — chosen by FliTools, not by the caller. Suggested shape, beside `transcription`:
   ```json
   { "describe": { "worker": { "ssh": "davidcruwys@100.126.70.25", "name": "mac-mini-m2" },
                   "fallback": { "name": "roamy" }, "model": "mlx-community/Qwen3-VL-8B-Instruct-4bit" } }
   ```
3. **Identity is the frame's sha256.** A second submit of the same bytes answers the existing job or its finished
   result; nothing is described twice.
4. **The worker only computes and never calls back.** The local FliTools pushes, then polls; the machine that holds the
   asset writes the result (B-roll Pilot writes the resource).
5. **One frame in, one description out.** Never a whole video as one pass (`qwen-video --fps 1` loops into repeated
   shots on a long video — same brain file).
6. Reading the queue is open on the tailnet; submitting needs the worker's bearer token.

## The verbs B-roll Pilot already calls (FliTools may rename; tell B-roll Pilot's adapter)

On the local FliTools door, `POST /api/rpc`, JSON-RPC 2.0, as `agent:flistudio`. Adapter:
`/Users/davidcruwys/dev/ad/flivideo/flistudio-worktrees/broll-pilot/modules/broll-pilot/server/flitools.ts`.

| Verb | Params | Answer |
|---|---|---|
| `describe.submit` | `{ sha256, image (base64), mime ('image/jpeg' \| 'image/png'), context: { form, title, tags[] }, app: 'flistudio' }` | a job: `{ id, status: queued \| running \| done \| failed, sha256, result? }` |
| `describe.job` | `{ id }` | `{ id, status, result?: { description, shows?, goodFor?, tags[], model }, error? }` |
| `queue.status` | — | waiting / running / last finished / `waitingFor` (shared with transcription, or a `describe` section) |
| `config.get` / `config.set` | — | the `describe` block above, so the FliStudio gear can show it |

- `context` is there so the description is about the right thing (a screencast of a terminal, a thumbnail …): put it
  in the prompt.
- `tags`: short subject words. B-roll Pilot stores them `ai-`-prefixed (Joy's `tag_broll` fence after 945 junk tags) —
  the service may prefix them or not.
- `model`: the model id that ran, recorded on the asset.
- Errors: a JSON-RPC error with `data.failureMode` (`app-unavailable` when the worker is down, `app-busy`, …). B-roll
  Pilot treats any error, a missing verb (`-32601`) or no answer as "service down" and sends the asset to the Claude
  Code queue with the reason — never a failure.

## Done when

- `describe.submit` / `describe.job` answer on the local FliTools; jobs run on the named worker, one at a time.
- A second submit of the same sha256 returns the same job / result.
- The M4 never loads the model (check `ps` / memory during a 12-frame run).
- B-roll Pilot's describe route passes against the real service on a fixture project (no code change expected beyond
  verb names, if FliTools renames them).
