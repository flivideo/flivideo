---
type: reference
title: "07 · How the B686 research run was executed (M4 orchestrates, M2 works)"
description: "Short record of how the 2026-11-03 FliVideo ecosystem research actually ran: windows, machines, what synced how, what went wrong, and what to reuse next time."
tags: [ecosystem-research, execution, appynet, m2, m4, deliver, B686]
created: 2026-11-03
timestamp: 2026-11-03T13:15+07:00
---

# 07 · Research execution

**Purpose**: A record of how this run was organised and what it taught, so the next multi-machine research run
starts from it. Written by B1 (`b686-arch-write`) at the end of its block; B3 may append the B2/B3 halves.

**For Agents**: The plan is canonical at
`/Users/davidcruwys/dev/ad/brains/north-star/deliver-2026-11-03-B686-flivideo-ecosystem-research.md` (§3 execution
shape, §5 blocks, §7–§9 records). This file says what happened, not what was planned.

---

## Shape as run

```
M4  flivideo-orch ── appynet.sh start m2 <name> … (attached iTerm2 windows on the M4)
                         │
M2  tmux b686-arch-write  (B1, Opus)   ── 01 · 02 · 03 · 07 + brains/north-star/four-umbrellas-30000ft.md
M2  tmux b686-rsch        (B2, Sonnet) ── 03b · candidates/   (same flivideo repo, disjoint paths)
                         │  both push to GitHub
M4  b686-synth-write      (B3, Opus)   ── 04 · 05 · 06 · 00 + the closing artifact   (after B1 + B2 report)
```

Observed on the M2 at ~13:00 +07: tmux sessions `b686-arch-write` and `b686-rsch` both created 10:00 and attached.

## What worked

- **One canonical plan file in the brains repo**, a copy as the brief in `flivideo/.appynet/briefs/`, and a status
  stamp at the top: B1 read §7–§10 first, found them empty, and started from scratch with no guessing.
- **Disjoint paths** for the two writers in one repo (B1: 01/02/03/07; B2: 03b/candidates). Each stages explicit
  paths and runs `git pull --rebase` before pushing.
- **Reading code without touching it**: `git fetch` on each app repo, then `git archive origin/main | tar -x` into
  the session scratchpad. This reads the code that runs on the M4 without pulling, building or editing the M2
  checkouts.

## What went wrong / watch next time

| Problem | Effect | Next time |
|---|---|---|
| **M2's `flistudio` was 133 commits behind** origin (local `08a82b8`, 2026-10-15; origin `e7dea41`); `flitools` 6 behind. The plan's "`flistudio/modules/` verified" was true on the M4 and **false on the M2 working copy** | A naive read on the M2 would report "no extensions exist" | Before any read-only architecture pass on the M2, run `git fetch` + compare `HEAD` vs `@{u}` for every app repo; read from origin when behind. The M2 drift warning in `~/.claude/CLAUDE.md` applies to app repos too |
| M2's `flistudio` has untracked files (`.claude/plugins/`, several `.claude/skills/*`, `.mcp.json`, `.openrig/`) that pre-date this run | `git status --porcelain` is not empty, so AC 12's "porcelain empty" cannot pass literally | AC 12 should read "unchanged by this run": compare against a snapshot taken at the start |
| Snappy is on the M4 only (`~/dev/ad/apps/snappy`), absent on the M2 | Had to `ssh` to the M4 to verify it | Check asset paths on the machine that will do the work, not only on the planner's |
| zsh treats `$R:e…` as a history modifier (`origin/main:extension-core` → broken) | Lost a few tool calls | Write `${R}:path` in zsh |

## Reuse

- The read-only recipe: `git -C <repo> fetch -q && git -C <repo> archive origin/main | tar -x -C <scratch>/<repo>`.
- The status-stamp + §7–§10 "skip what landed" convention made re-entry safe; keep it.

---

## B2 and B3 halves (appended by B3, `b686-synth-write`, M4, 2026-11-03 ~14:00 +07)

- **B2** (`b686-rsch`, M2, **Sonnet** — orch's call, not the plan's Opus) ran in parallel with B1 on disjoint paths
  (03b + `candidates/`), cloned 8 of the 10-clone cap via `upstream-add` with a *scoped* scan, and pushed flivideo
  `6353e14` + brains `9bbba6fa`. Its deviations are in the plan §8.
- **B3** started on the M4 after both reported; pulled both repos (already current), read 01–03b, 07 and all 11
  candidate files, wrote 04 · 05 · 06 · 00, then built and published the closing artifact.
- **What worked**: B2's per-file field discipline (AC7) made the per-candidate outcome table in 04 a mechanical
  read; the plan's §7 spike records answered B3's two hardest questions (HyperFrames editor surface; three
  extensions in code) without re-reading code.
- **Watch next time**: grouped candidate files (several repos per file) make "every candidate row" ambiguous — 04
  numbers candidates C1–C19 itself. Ask B2 for one ID per repo up front. Several "cited, not re-verified" entries
  (Cap, Remotion, FilmCraft) carry brain claims; they are labelled, but a Sonnet researcher leaned on brains more
  than an Opus one might.
