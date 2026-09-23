---
type: brief
title: Investigate OBS — install, configure, autopilot (alongside Ecamm Live)
description: "Investigation brief: can OBS Studio run on autopilot on the M4 Mini to stream to more platforms and grow the audience, alongside Ecamm Live? Findings + go/no-go; no build."
created: 2026-09-23
timestamp: 2026-09-23
status: open
---

# Investigate OBS — install, configure, autopilot

**Purpose**: Decide whether OBS Studio should join the recording/streaming setup to grow the audience
through streaming reach. Replacing Ecamm Live is *not* the goal, though the findings may show it.

**For Agents**:
- This is a spike. Output is a findings doc plus a go/no-go. Build nothing, change no app.
- Ecamm Live stays as it is throughout.

**Type**: investigation · **Owner**: unassigned · **Raised by**: David, 2026-09-23

---

## Questions

1. **Install and configure** OBS Studio on the M4 Mini: scenes, sources, audio. What is the minimum
   setup that matches today's Ecamm recording look?
2. **Autopilot**: can OBS be driven hands-free (obs-websocket, CLI, Stream Deck) so a stream or
   recording starts and stops the way the Ecamm pedal does now?
3. **Reach**: which platforms can it stream to at the same time (YouTube, X, LinkedIn, Twitch, …),
   directly or through Restream? Restream is on the free plan with no channels connected.
4. **Fit with FliVideo**: where do OBS recordings land, and can FliHub pick them up like Ecamm takes
   (watch folder, naming)? The original spec said OBS "should adapt with minimal changes"
   (`/Users/davidcruwys/dev/ad/flivideo/fli-brief/docs/fli-video.md`; see also
   `/Users/davidcruwys/dev/ad/flivideo/docs/prior-art-fli-brief.md`).
5. **Cost and risk**: CPU/GPU load of recording + streaming on the M4 Mini (24 GiB), and anything
   that conflicts with Ecamm (camera, mic or Stream Deck contention).

## Done when

A findings doc answers 1–5 with evidence (measured, not recalled) and recommends one of:
stream with OBS alongside Ecamm · switch to OBS · don't bother.

## Out of scope

- Removing or reconfiguring Ecamm Live.
- Changing FliHub, FliCast or any other app's code.
