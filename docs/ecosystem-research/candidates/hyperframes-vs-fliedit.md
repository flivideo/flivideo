---
type: research
title: "HyperFrames vs FliEdit — feature by feature, and what FliEdit could clean-room"
description: "Measured comparison of HeyGen's HyperFrames (X1 trial, 2026-11-03) and FliEdit (code read 2026-11-04 at dc39399), the gaps FliEdit could close by clean-room harvest, and what is and isn't verified."
tags: [ecosystem-research, hyperframes, fliedit, clean-room, B686, R9, R10]
created: 2026-11-04
timestamp: 2026-11-04T08:45+07:00
---

# HyperFrames vs FliEdit

**Purpose**: One place that says what each editor can actually do today, so FliEdit work can pick up the gaps without
re-researching. Written for when FliEdit work resumes; **no FliEdit build is planned by this doc.**

**For Agents**:
- Read before any FliEdit feature work, or before arguing R9 (FliEdit's fate) / R10 (HyperFrames as an editor) in
  `/Users/davidcruwys/dev/ad/flivideo/docs/ecosystem-research/06-approval-register.md`.
- Harvest means **clean room only** (David, 2026-11-04): FliEdit may reproduce a feature it sees in HyperFrames by studying it
  and writing its own code in its own style; it never lifts code. Route: the `upstream:clean-room` skill
  (`/Users/davidcruwys/dev/ad/appydave-plugins/upstream/skills/clean-room/SKILL.md`).
- Sources: HyperFrames X1/X2 evidence in [hyperframes-as-editor.md](hyperframes-as-editor.md); FliEdit code at
  `/Users/davidcruwys/dev/ad/flivideo/fliedit` @ `dc39399` and its `docs/drivable-audit-2026-10-31.md`, `docs/gap-ledger.md`.
- Side-by-side render of the same d01 composition: brief `docs/briefs/fliedit-side-by-side-d01-2026-11-04.md` (results get
  appended here).

## What HyperFrames is

HeyGen's open-source video-as-code framework (not Vercel's): video authored as HTML with `data-*` timing and a seekable
paused timeline, rendered by headless Chrome seek-per-frame + FFmpeg. Apache-2.0, pre-1.0, heavy churn (~2,000 commits
Aug 4 → Oct 17, per `~/dev/upstream/repos.jsonl`). Installed on the M4 as the `hyperframes-studio` app
(`~/dev/ad/apps/hyperframes-studio`, `hyperframes@0.9.9`, 127.0.0.1:7210, 2026-11-04).

## Feature by feature

Key: ✅ measured or read in code · ⚠️ partly · ❌ not there · UNVERIFIED = not checked.

| Feature | FliEdit (code @ dc39399) | HyperFrames (X1 2026-11-03 unless noted) | Who's ahead |
|---|---|---|---|
| Ripple delete | ✅ one verb `clip.rippleDelete` (`src/core/ops/edit-ops.ts:323`, `ops/ripple.ts`); rule marked provisional (D13); unit-tested, not exercised in a spike | ❌ as a verb: `timeline delete` leaves a gap, the agent issued 4× `timeline move` | **FliEdit** |
| Split / move / trim | ✅ `clip.split`, `clip.move`, `clip.trim` | ✅ `timeline split/move/trim` via CLI `--json` | even |
| Music bed + level | ✅ second audio track, `clip.setProps {volumeDb}` (constant per clip) | ✅ `<audio>` track + `timeline set --volume` | even |
| Music ducking (level dips under voice) | ⚠️ no volume automation: one `volumeDb` per clip plus audio `fadeIn/fadeOut`; a duck means splitting the music clip and fading each piece by hand | ⚠️ real automation lanes (`data-automation`, 1→0.35→1) but not a CLI verb — set via REST `patch-element`; audibility UNVERIFIED | **HyperFrames** (has the model; lacks the verb) |
| Animated callout / text graphic | ❌ no text or graphic layer; overlays are images or alpha video (`cutaway.apply`, PNG / ProRes 4444 / WebM alpha) made elsewhere | ✅ any HTML element animated with GSAP | **HyperFrames** |
| Keyframed position/scale/opacity | ❌ static `clip.setProps` ("no keyframed moves (v1)") | ✅ GSAP timelines (used in X1 callout) | **HyperFrames** |
| Transitions | ✅ dissolve + fade (`transition.set`); no wipes/slides | UNVERIFIED (a `shader-transitions` package exists in the repo) | FliEdit verified |
| B-roll / cutaway over a take | ✅ `cutaway.apply` (one step, one undo, all-or-nothing) | ✅ second video track, trimmed | even |
| Captions | ⚠️ soft `mov_text` + `.srt` only; burn-in blocked by ffmpeg without libass (G5) | UNVERIFIED as a captions feature; text is HTML so it renders burned in | likely HyperFrames, UNVERIFIED |
| Speed change | ❌ deferred in v1 | ⚠️ `timeline set` accepts `rate=` (seen in the refusal message); not exercised | HyperFrames, UNVERIFIED |
| Undo / history | ✅ `history.*` (undo, redo, jump, undoBy) | ✅ `routes/history.ts` undo/restore | even |
| Agent drivability | ✅ full JSON-RPC door, OpenRPC, dry-run, typed refusals | ✅ CLI `--json` + unauthenticated REST; gaps above | FliEdit more complete |
| Render | ✅ ffmpeg `export.start` | ✅ `render -q draft` 65 s in 42 s, 1920×1080 h264 | even; speed comparison UNVERIFIED |
| Output audit | ❌ | ✅ `hyperframes check` (lint, layout, motion, WCAG — per repo description; lint/layout pass seen in X1) | **HyperFrames** |
| Human editing UI | ✅ Electron timeline (FliEdit app) | ✅ Studio in the browser (drag callouts, trim) | different styles |
| Security | local Electron, door token | **no auth**; loopback is its only protection (X2) | **FliEdit** |
| Stability | ours | pre-1.0, heavy churn | **FliEdit** |

**Bottom line:** FliEdit is ahead on cut-and-assemble (ripple delete, drivable door, stability). HyperFrames is ahead on
the motion layer (animated graphics, keyframes, volume automation, output audit). "FliEdit stays the assembler" (R9 E-A)
was a statement about roles, not a measured win.

## Gaps FliEdit could close by clean-room harvest

Each row is a candidate for `upstream:clean-room`: concept spec from HyperFrames, FliEdit's own code. None is approved.

| # | Gap in FliEdit | Where to study it in HyperFrames | Size guess |
|---|---|---|---|
| H1 | Volume automation lanes (a duck as 3–4 points, one verb e.g. `clip.duck`) | `data-automation` attribute + the `patch-element` mutation in `packages/studio-server` routes (`gsap-mutations*`, `file-mutations/*`) | M |
| H2 | Keyframed position / scale / opacity | GSAP timeline model in `packages/core` / `packages/player` | L |
| H3 | Text / graphic layer (callouts) rendered in-frame, which also solves caption burn-in (G5) | HTML-element compositions + headless-Chrome frame capture (`packages/engine`, `packages/producer`) | L |
| H4 | Output audit (`check`: layout, motion, WCAG) | `packages/lint`, `hyperframes check` | M |
| H5 | Speed change | `timeline set rate=` handling in `packages/cli` | S–M |

Licence: Apache-2.0 permits reuse, but David's rule is concept-only regardless.

## Verified / not verified

- **Verified:** FliEdit verbs and ripple code (read 2026-11-04, `dc39399`); FliEdit audit table (2026-10-31 spike);
  HyperFrames X1 operations, render and X2 bind/auth (2026-11-03, M4); HyperFrames Studio app up on 127.0.0.1:7210 with
  project `d01-trial` (2026-11-04, `GET /api/projects` → 200).
- **Not verified:** that either duck is audible; FliEdit ripple delete on real footage; HyperFrames transitions, captions,
  speed; render speed of the same composition in both (the side-by-side job will measure it); Studio on a 20-minute project.
