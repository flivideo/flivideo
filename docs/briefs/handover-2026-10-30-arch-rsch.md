# Handover — flivideo-arch-rsch, closed 2026-10-30

**Purpose**: Where the architecture window got to, so a future session can carry on with architecture without this chat.

**For Agents**:
- This window was the architecture and research seat for FliVideo, 29–30 Oct 2026, on the M4.
- Read the three canonical documents below first. This file is only the index and the open list.
- Builds, merges and restarts belong to `flivideo-orch` (tmux `flivideo-orch`). Its checkpoint is `docs/orch-checkpoint.md`: read it, never edit it.

## The canonical documents (read these, in this order)

1. `/Users/davidcruwys/dev/ad/brains/brand-dave/studio-pattern-synthesis-2026-10-30.md`: David's three umbrellas (FliVideo, Appy Studio, the business umbrella), the Studio pattern as a template, corrections to his model, names, and the finance decision. Brains `2e5518c8`.
2. `/Users/davidcruwys/dev/ad/flivideo/docs/architecture-review-2026-10-29.md`: FliVideo's four layers, Overlay Pilot coupling C1–C7, and the extension-core design (§5). Its status stamp at the top says what got built.
3. `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/overnight-2026-10-29-report.md`: the overnight build (fli-core v0.26.0, the brand-settings race fix, templates).

## Done in this window (all merged and pushed)

- **fli-core v0.26.0 everywhere.** The FliHub merge (`061ae34`) was the last one; FliHub was restarted through `my-app`.
- **`@appydave/core` 0.2.0** (zod 4 peer) published to npm by David. Every consumer now takes it from npm and no vendored copies are left:
  - FliCast `8213fcd`, FliEdit `d0cb909`, FliCut `92f41c9`, Teletubby `efabbe5`;
  - AppyStack `c1270f6`, AppyTron `8444422` and `b5a99a4`.
- **`@flivideo/extension-core`** merged in FliStudio `1e89742`, with Overlay Pilot migrated onto it. David checked the project page.
- **FliStudio busy guard** (`f0dc19a`): `scripts/busy.sh`, plus `"busy"` in `~/.config/appydave/apps.json`.
- **Cleanup:** 44 overnight worktrees removed (16 GB), all their branches deleted locally and on GitHub, and 7 builder tmux sessions closed.
- **Dossier B670**, the StoryPilot ChatGPT conversation, filed beside voice log B667.
- **StoryPilot launched** as `storypilot-dev`. Brief: `docs/briefs/storypilot-launch-2026-10-30.md`, including the §2a addendum. It writes the spec, stops for David, then builds. flivideo-orch manages it.

## Open — waiting on David (updated 2026-10-30 evening)

- **FliHub rebuild: PARKED by David 2026-10-30.** Nothing has been built; FliHub v1 is live and unchanged.
  - Start here when it resumes: `/Users/davidcruwys/dev/ad/flivideo/docs/flihub-rebuild-spec-parked-2026-10-30.md` (flivideo `2dd162a`). It holds the rulings, the Section 1 walkthrough, the estimate, the cut-over steps and the open questions (S1–S5 sign-off, Q1 with the 10 unsure items, Q3 hold/archive).
  - The spec is filed in FliStudio on AppyDave **D17** (`d17-flihub-rebuild`), along with the discovery doc, the brief, the looks artifact and both sessions.
  - flivideo-orch has been told not to write a v2 build brief until David resumes the rebuild.
- **D13 Story Pilot settings:** what the viewer should feel, what they should do, the AppyDave bookends, and "girlfriend Joy" vs "partner".
- **AppyInvoice:** David reviews the vOz October draft INV-000042 (US$2,945). Nothing has been sent; every send and payment needs his go.
- **Delete the merged remote branch.** The classifier blocks this for agents, so David runs it himself: `git -C ~/dev/ad/flivideo/flistudio push origin --delete extension-core`.
- **Human checks:**
  - FliHub's "reload and save again" refusal: change brand settings in FliStudio while FliHub's ConfigPanel is open, then click Save in FliHub.
  - AppyTron on Electron 44 has never been launched.
- **Registry drift** (synthesis §1 #4 and #7):
  - apps.json has no `boilerplate` for flistudio;
  - locations.json's AppyTron consumers are missing FliCast and FliEdit;
  - `~/dev/ad/CLAUDE.md` points at `/apps/appyradar/`, but the live app is `apps/appyradar-sentinal`.
- **AppySentinel** is very out of date, and David rates the idea highly. Refresh it as its own job (consumers: appyradar-sentinal, switchboard, supportsignal-sentinal).
- **Overnight follow-up spec**, not yet written. The batch:
  - FliTools has no build script;
  - FliCut has a stale pnpm-lock and `pnpm-workspace.yaml`;
  - the AppyStack and AppyTron upgrade tools are unsafe;
  - retire the four duplicate FliTools clients (C7);
  - add a FliCast rung to best-transcript;
  - fli-core brand schemas strip unknown keys on write;
  - regenerate the schema mirrors in FliCast and FliEdit;
  - C6 (dist vs source resolution);
  - split Overlay Pilot's settings out of `ExtensionHost`.
- **The synthesis doc is out of date on extensions.** Its shared-extensions idea (§2 and §5.4 of `/Users/davidcruwys/dev/ad/brains/brand-dave/studio-pattern-synthesis-2026-10-30.md`) no longer holds. David has ruled that extensions live only in the root app, FliStudio; microapps get doors, not extensions.
- **Done since this list was first written:**
  - the finance decision went to `appy-invoice-rsch`, which built AppyInvoice v1;
  - Story Pilot was merged and went live;
  - extension-core 0.2.0 (G1, app-door calls) is live, and Send-to-Teletubby has been proven (see the orch checkpoint).

## Gotchas learned here

- **`my-app restart <app> --help` restarts the app.** `my-app` doesn't parse `--help`.
- **Remote branch deletes and killing tmux sessions** are blocked by the auto-mode classifier until David says so in-window.
- **The rule for shared files:** fli-core names *where* a shared file lives; the app that owns it decides its contents and is its only writer. Other apps go through the owner's door. StoryPilot hands scripts to Teletubby through Teletubby's API on :7111.
