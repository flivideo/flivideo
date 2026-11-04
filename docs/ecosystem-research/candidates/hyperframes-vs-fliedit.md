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
- **What's in sync now lives in one place:** `/Users/davidcruwys/dev/ad/flivideo/fliedit/docs/upstream-watch-hyperframes.md` (state per row; re-check when `hyperframes-studio` bumps its pinned version). This file is the research behind it.
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
- **Not verified:** that either duck is audible (see side-by-side below: not isolated); FliEdit ripple delete on real footage;
  HyperFrames transitions, captions, speed; Studio on a 20-minute project. Render speed of the same composition: measured
  once, below (one run each, unequal settings, so indicative only).

## Side-by-side d01 — 2026-11-04

Same composition (d01 trial, chapter 03: takes 03-1 + 03-2, DJI_0235 at 8 s and DJI_0237 at 45 s for 5 s each, callout 3–7 s,
music bed at 0.5 ducked 1→0.35→1) built in both editors, 1920×1080, 25 fps, 65.12 s, M4. FliEdit was driven only through its
JSON-RPC door (hidden, isolated home); no FliEdit code changed. Page: https://claude.ai/artifact/LArug5HPJAjmcaQsXsVJxW
(source `docs/artifacts/hyperframes-vs-fliedit-d01-2026-11-04.html`).

| | HyperFrames 0.9.9 | FliEdit @ dc39399 |
|---|---|---|
| Render | `render -q draft -f 25`: **38.1 s**, 14,204,902 B | `export.start` veryfast crf 20: **13.9 s**, 19,899,570 B |
| Output | `…/d01-flivideo-tour/hyperframes/renders/d01-trial-hyperframes-draft-25fps.mp4` | `…/hyperframes/renders/d01-trial-fliedit-25fps.mp4` |
| Edit | `hyperframes/d01-trial/index.html` | `d01-flivideo-tour/fli.edit.d01-hf-sbs.json` |

Steps: takes (✅ `source.add`+`clip.place`), both cutaways (✅ one `cutaway.apply` call, frames 200 and 1125 × 125, fit fill),
music bed level (✅ `volumeDb −6.02` = 0.5). Frame grabs at 1 s, 10 s and 30 s are visually identical; at 5 s HyperFrames shows the callout.

**Gaps recorded (no workarounds built):**
- **Callout (H3 + H2):** FliEdit has no text/graphic layer or keyframed animation. Nearest native: `caption.add` (soft subtitle,
  not an on-frame box). Not used.
- **Duck (H1):** one `volumeDb` per clip plus fadeIn/fadeOut. Nearest native: split the music clip and fade pieces by hand. Not done.
- Not a FliEdit gap, a HyperFrames note: composition declares no fps so render defaults to 30; `-f 25` was needed.

**Findings:** the cut-and-assemble half was straightforward and drivable first time; FliEdit rendered ~2.7× faster, though HyperFrames
was also drawing an animated layer and the quality settings differ (draft vs crf 20), so treat the ratio as indicative.

**Still not verified:** duck audibility — speech and music are mixed, so mean-volume windows (HyperFrames 0–2 s −22.0 dB vs
4–6 s −26.7 dB; FliEdit −22.7 vs −25.4 dB) cannot isolate the music; no music-only render was made. FliEdit's −6.02 dB not compared
by ear. One run each; no repeat timings.

## Watch list + UI/UX deep dive — 2026-11-04 (M4)

Owned by FliEdit: `/Users/davidcruwys/dev/ad/flivideo/fliedit/docs/upstream-watch-hyperframes.md` (H1–H5 plus ten UX rows U1–U10;
screenshot pairs in `fliedit/docs/upstream-watch-assets/`). Re-check whenever the Studio's pinned `hyperframes` version bumps.
Top UX transfers: U1 light quiet chrome (AppyDave tokens) · U2 clip thumbnails + waveforms · U3 typed inspector header with
empty-state help · U4 compact transport · U5 icon toggles for snap/link. One FliEdit window and one Studio session only; research, no code.
