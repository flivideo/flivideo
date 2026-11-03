---
type: architecture
title: "03 · Apps, extensions, tools — the taxonomy, the 80-20 guardrail and the extraction trigger"
description: "What an app, an extension (pilot), a tool and a foundation each own inside an umbrella; David's 80-20 rule for extensions, measured against the three built pilots; the pilot→app extraction trigger; five enforcement options with who enforces each; one recommendation, not approved."
tags: [ecosystem-research, taxonomy, extensions, pilots, guardrail, 80-20, flivideo, B686]
created: 2026-11-03
timestamp: 2026-11-03T13:00+07:00
status: proposal
---

# 03 · Apps, extensions, tools

**Purpose**: Write down the three-layer split David described in B686 (apps own capabilities, tools own discrete
operations, extensions own workflows), test his 80-20 idea against the code, and give options for **who enforces
it and how** — the question he left open.

**For Agents**:
- §1–§2 are David's model (B686), checked against the code. §3 is measured from FliStudio origin `e7dea41`.
- §4 (enforcement) and §5 (recommendation) are **proposals, not approved**. They go to the approval register
  (06). Do not add lint rules, descriptor checks or CI steps from this file.
- The split applies to any umbrella (B686: "that pattern could apply to any studio umbrella, not just video"); the
  examples are FliVideo because it is the only one built (`/Users/davidcruwys/dev/ad/brains/north-star/four-umbrellas-30000ft.md`).
- Prior art this builds on, not repeats: the Studio pattern template and its promotion rule,
  `/Users/davidcruwys/dev/ad/brains/brand-dave/studio-pattern-synthesis-2026-10-30.md` §2 and §5.5.

---

## 1. Definitions

| Layer | Answers | Owns | Who drives it | FliVideo examples (observed) |
|---|---|---|---|---|
| **Umbrella** | "which business area?" | a name, a unit of work (a video project), a registry group | — | FliVideo |
| **App** | "what **can** I do?" | a **capability**: a deep, bespoke surface (cutting, editing, recording, prompting), its own process, its own files, a door agents can drive | humans *and* agents equally, through the same door | FliStudio (also the control plane), FliHub, FliCut, FliCast, FliEdit, Teletubby |
| **Extension** (a *pilot*) | "what am I **trying to accomplish**?" | a **workflow and its working context** for one unit of work: the data a person needs to see, query and follow; it calls apps' capabilities for the heavy lifting | a person following a structure; an agent running the same steps | Story Pilot, Overlay Pilot, B-roll Pilot (Motion Pilot = idea) |
| **Tool** | "do this one thing" | a **discrete operation** any layer may invoke, no workflow, no UI of its own | anything: an app, an extension, FliStudio, an agent | FliTools: `transcribe`, `audio.clean`, `speech.synthesize`, `face.track`, `prompter.load` |
| **Foundation** | "where things live; how to be drivable" | shared rules and contracts | — | fli-core (domain core + the door), extension-core (the extension contract), `@appydave/core` |

David's words (B686): "Apps own capabilities … Tools own discrete operations that anyone can invoke and
extensions own the workflows and working context." And: "FliStudio is an app but it's part of the umbrella."

**One-line tests** (inference, mine):
- *Is it an app?* It would still be useful with no workflow around it, and it needs its own process or its own
  deep UI.
- *Is it a tool?* It has a verb and an input, and no opinion about the project's stage.
- *Is it an extension?* Take away the project/stage context and it stops making sense.

## 2. The 80-20 rule and the extraction trigger

**David said** (B686): "80 [percent] of those extensions are usually a read aspect … they're not read only …
they're holding data, they're visualizing data, they're querying data, they're showing data flows." And the
trigger: "if you start seeing me build a full editing application into a pilot, this would be the time … have we
gone beyond the pilot and into the app … we should start designing an app around the problem."

Stated as a rule (proposal):

> **An extension is mostly read: about 80% of it holds, shows and queries the unit of work; about 20% writes, and
> its writes mostly *ask an app or a tool* to do the work. When an extension starts to *own* a capability — a
> renderer, an editor, a long-running process, a media pipeline — that capability is extracted into an app or a
> tool, and the extension calls it.**

The extraction trigger, combining B686 with the synthesis §5.5 (any one holds → consider extraction):

| # | Trigger | Source |
|---|---|---|
| T1 | A pilot grows an editing surface (a timeline, a canvas, a frame-accurate player) | B686 |
| T2 | It needs its own process or runtime (Electron, a long-running worker, a GPU) | synthesis §5.5 |
| T3 | A second host or a second extension needs the same capability | synthesis §5.5 |
| T4 | Three or more related extensions share state | synthesis §5.5 |
| T5 | Its writes stop delegating: it shells out to media binaries or writes files outside its own `fli.<ext>…json` | inference — the measurable form of T1 |

Extraction outcomes are the same four as the research (B686): put the capability in an existing app, add a new app
(e.g. a "FliMotion" for overlays/motion, B686), use someone else's app, or leave it.

## 3. Measured: the three built pilots against the rule

From FliStudio origin `e7dea41` (method in `02-flivideo-current-state.md` §1.2).

| Pilot | Query verbs | Command verbs | Query share | Spawns processes | Owns capability code? | Reading (inference) |
|---|---|---|---|---|---|---|
| **Overlay Pilot** | 10 | 3 | ~77% | yes — `server/media.ts` spawns `python3 render/render.py` ("one ffmpeg pass per look"); `server/sources.ts` runs `ffprobe` | **yes**: a renderer + a grammar | Reads like a pilot by verbs, but **owns a renderer**: T5 holds, T1 is close. This is the "fine line" David named (should overlays live in Overlay Pilot or a FliMotion app?) |
| **B-roll Pilot** | 6 | 7 | ~46% | yes — `server/media.ts` runs `ffprobe`/`ffmpeg` (facts, stills into its own render cache, scene scan) | some: media probing + still extraction | Write-heavy by verbs; much of it registers and tags takes for *this project* (FliHub calls `broll.register`). T5 partly holds |
| **Story Pilot** | 9 | 13 | ~41% | no direct spawn found | no — it **delegates**: `host.app('teletubby')`, `host.app('flitools').call('speech.synthesize')` | Write-heavy by verbs but every heavy write is delegated. **The pattern the rule wants**, despite failing a naive 80% count |

**What the measurement shows** (inference):
1. **A raw query/command ratio is the wrong metric on its own.** Story Pilot fails 80-20 by count yet is the
   best-behaved pilot; Overlay Pilot passes by count yet is the one owning a capability. The real signal is
   **whether writes delegate** (T5), not how many writes there are.
2. **None of the three is "a full editing application"** (T1 not met). Overlay Pilot is nearest.
3. Nothing here is a judgement on Story Pilot or Overlay Pilot's behaviour — both are being tested by David today
   and were read, not run or changed.

## 4. Who enforces it, and how — five options

Each is independent; they stack.

| # | Option | What it checks | Who enforces | When it fires | Cost | Catches |
|---|---|---|---|---|---|---|
| **E1** | **Descriptor declaration** in extension-core: each extension declares `delegates: [...]` (the apps/tools its commands call) and `owns: [...]` (any capability it keeps on purpose); `defineExtension` refuses an undeclared `owns` | intent, at the author's desk | **the code** (`extension-core/src/descriptor.ts`, alongside the existing `query ⇔ read-only` check); David approves any `owns` entry | build/test time | small — the descriptor is already validated at define time | T1, T5 (if honest) |
| **E2** | **Dependency-cruiser rule**: a module's server may not import `node:child_process` (or named media/render libraries) unless listed in an allow-file | capability code sneaking in | **the linter** — `.dependency-cruiser.cjs`, run by `npm run lint` (already fences every `modules/<name>/`) + husky pre-commit | every commit | small; today it would flag Overlay Pilot and B-roll Pilot (both spawn), so it starts with an allow-list | T2, T5 |
| **E3** | **Tripwire report**: a script prints per extension: LOC, query/command split, spawn sites, files written outside its own `fli.<ext>` file, `host.app` calls; thresholds warn, never fail | drift over time | **the orchestrating agent** reads it at each delivery; **David** sees the trend | per delivery / weekly | small–medium (a script in `flistudio/scripts/`) | T1–T5 as numbers |
| **E4** | **Spec-time question**: every pilot spec answers "which capabilities does this pilot borrow, and from which app/tool? what does it own, and why?" before a build is approved | design intent | **David**, at the spec/rulings step; the speccing agent must ask | before code | ~zero — a section in the spec template | T1, T3 before they happen |
| **E5** | **Review skill step**: a "pilot or app?" check in the delivery review (e.g. inside `dev-team:one-seam` or `dev-team:delivery-review`), reading E3's report and the diff | judgement calls the numbers miss | **a reviewing agent**, escalating to David | at each delivery review | medium (skill change) | T1, T4 |

## 5. Recommendation — **not approved**

> **Start with E4 + E3 (report-only), add E2 with an allow-list once the report has a few readings; leave E1 and
> E5 until a pilot actually crosses a trigger.**

Why: E4 costs nothing and catches the problem before code exists. E3 turns the 80-20 idea into numbers without
blocking anyone — and §3 shows a naive threshold would block the wrong pilot. E2 is cheap because the fence
already exists, but it must start with Overlay Pilot and B-roll Pilot allow-listed, or it fails the build on day
one. E1 and E5 add ceremony that is only worth it once a real extraction is on the table.

**Open for David** (to the approval register): (a) is "writes must delegate" the right reading of 80-20, rather
than a literal 80% read count? (b) does Overlay Pilot's renderer count as "an app inside a pilot" today, which would
start the FliMotion question (04)?

## Sources

- B686 voice log, `/Users/davidcruwys/dev/raw-intake/plaud/2026-11-03-0838-2026-11-03-083808.md`
- FliStudio origin/main `e7dea41`: `extension-core/src/descriptor.ts`, `extension-core/src/server.ts`,
  `.dependency-cruiser.cjs`, `modules/*/server/media.ts`, `modules/overlay-pilot/server/sources.ts`,
  `modules/storypilot/server/{index,angles,audio}.ts`
- `/Users/davidcruwys/dev/ad/brains/brand-dave/studio-pattern-synthesis-2026-10-30.md` §2, §5.5
- `/Users/davidcruwys/dev/ad/flivideo/docs/architecture-review-2026-10-29.md` §5 (extension-core design)
- `/Users/davidcruwys/dev/ad/brains/creator-stack/tool-taxonomy.md` (the catalogue's accept/reject rule for *tools* — a different axis: it classifies third-party tools, not layers inside an umbrella)
