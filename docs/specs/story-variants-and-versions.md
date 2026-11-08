---
title: "Story variants and versions: Story Pilot to Teletubby"
description: "Spec and publish contract so Story Pilot publishes story variants with their own version history and Teletubby picks between them without becoming an editor."
created: 2026-11-08
timestamp: 2026-11-08
status: "for review (spec only, nothing built)"
---

# Story variants and versions: Story Pilot to Teletubby

**Purpose**: The model, the one publish contract, and the behaviour both apps must show, so a story can be republished mid-recording and regenerated into a selectable alternative.

**For Agents**: Slices 1 and 2 of the `variants` work. Section 5 is the contract both repos build to. Section 8 is what QA tests. Every code reference is relative to its repo (`flistudio`, `teletubby`) on the `variants` branch at the spec's date. Story Pilot paths sit under `flistudio/modules/storypilot/`.

**Round 2 changes this spec.** Section 12 is the current model for Story Pilot's side and names what it supersedes. Sections 5 and 7, Teletubby's side and the publish contract, still stand.

**Page**: [story-variants-and-versions.html](story-variants-and-versions.html) shows the before and after. This file is the record; if they disagree, this one wins.

## 1. The problem

The talent records from Teletubby, fed by Story Pilot (a module of FliStudio). In the talent's words:

> "Teletubby doesn't really have a concept of variants and that's my problem."
> "I might get halfway through the video and think, these words, they suck ... republish ... it'll go up to Teletubby as the same story, the same variant ... nothing will really change much on my screen other than a few words, and then I can keep recording to the end."
> "If I change a word in the story, that's certainly a version change on the variant."

Three things must work:

1. Publish a story from Story Pilot to Teletubby.
2. Change a few words and republish mid-recording. Teletubby shows the new words **in place**, keeping the reading position. Only the changed words move.
3. Regenerate in a different profile and publish. It arrives as a **new variant**, picked from a simple selector. Teletubby stays a recording tool.

## 2. Glossary

One meaning each, in the UI, the API and the code. No "draft", "revision" or "copy" for these two things.

| Word | Meaning |
|---|---|
| **Variant** | One regeneration of a story with a given profile set (structure, voice, style). Has a stable id, a free-text label, and its own version history. |
| **Version** | A word-level edit inside one variant. A number that goes up on each publish of changed words. |
| **Label** | Free text naming a variant. The default comes from the profile combination, e.g. `Tolkien · teaching · long`. Never a fixed long/short choice. |
| **Publish** | Story Pilot handing one variant at one version to Teletubby: the existing Send to Teletubby. |

"Script" keeps its existing meaning in each app: in Story Pilot, a file set under `scripts/<id>/`; in Teletubby, one entry in the on-demand set, holding transcripts.

## 3. The model

```
Story Pilot (owns history)                     Teletubby (read-only consumer)
──────────────────────────                     ──────────────────────────────
story for video X                              script  storypilot-<video|project>
├─ script A, profile P1  → variant A-p1  ───►  ├─ transcript A-p1  label · v8   (current words only)
│    versions/ v1 … v8                         │
├─ script A, profile P2  → variant A-p2  ───►  ├─ transcript A-p2  label · v9
└─ script B, profile P3  → variant B-p3  ───►  └─ transcript B-p3  label · v3
```

**A variant is a Teletubby transcript.** A transcript is already "one full body of words for this script", it already has per-transcript trigger sets, and the footer already has one chip per transcript, live mid-take, with a pulsing dot when one arrives (`teletubby/src/renderer/src/App.tsx:1006-1044`). So the selector is a control the talent already knows. That is the north-star test: no new control to learn.

### Where versions live (the open question from the talent's session)

**A republish creates a version in Story Pilot only.** Teletubby holds each variant's current words and displays its version number as read-only metadata. It has no version list, no back-to-earlier-words and no version history. The file is overwritten in place. Teletubby's existing per-write safety record (`recordPrior`) is unchanged and is not exposed as versions.

## 4. What exists and what is new

| Area | Exists today | New |
|---|---|---|
| Story Pilot scripts | Many scripts per story, each with its own `versions/`, undo/redo, audio (`modules/storypilot/server/versions.ts`) | Nothing about storing them |
| Story Pilot profile | Recipe: kind, style, narrator, four parts (`modules/storypilot/shared/contracts.ts:699`), recorded per build | Variant id and default label derived from it |
| Send | `story.script.send`: `context.select`, `script.write`, then `app.stage` (`modules/storypilot/server/index.ts:1221`). **Every script goes to one id**, `storypilot-<video\|project>`, so a second script overwrites the first (`modules/storypilot/server/story.ts:275,318`) | `variant` block on the write |
| Version number | Every saved edit gets `n`. A person's edits within 10s fold into one (`modules/storypilot/server/versions.ts:25,223`) | A publish ends the fold window (6.2) |
| Teletubby write | `write_script`: same id replaced in place, new id added (`src/core/text-script.ts:192`). Replaces the **whole** script | With `variant`: upsert one transcript, keep the others |
| Teletubby selector | Transcript chips on the footer strip, showing `corpus` | Chip shows the label |
| Keep position on refresh | `refresh` re-seats by paragraph id, no cue (`src/renderer/src/store.ts:517`) | Content anchor (7.4); ids are positional, so it is wrong today after an insert |
| Staging after a send | `app.stage` returns early if the script is already on stage (`server/src/launch/doors.ts:425`); otherwise `stage_select`, applied by `selectScript` | `stage_select` itself no-ops when already on stage (7.3); today, when reached, it resets to the top |

### Three defects this work must fix (traced in code, not yet reproduced by running)

1. **Re-staging the script already on stage sends the talent to the top, on two paths.** `stage_select` refuses only if the talent moved in the last 2 minutes (`TALENT_BUSY_WINDOW_MS`, `src/core/stage.ts:27`). Once it is accepted, the window runs `applyStageRequest` → `selectScript`, which sets `step: 0` and raises a cue card (`store.ts:905-908, 681-691`). **The screen's Send button normally does not reach this**: `app.stage` returns early when `workspace.position` already shows the set and script (`doors.ts:425`). It is reached by (a) an agent following `story.brief`'s `handover.calls`, which include `stage.select` directly (`story.ts:339-340`), and (b) a Send when there is no remembered position (`readPosition` null: `list_rigs` failed, or the window never wrote `remember_layout`).
2. **Paragraph ids are positional.** `p1..pN` are assigned in order on every write (`text-script.ts:81`), so inserting a paragraph before the talent makes "p7" a different paragraph. Refresh trusts the id.
3. **`video.text` joins all transcripts into one text** (`flistudio/server/src/capabilities/video-text.ts`, `paragraphs(c.transcripts ?? c)`). With two variants, Story Pilot's "same/changed" check (`teletubbyState`, `story.ts:284`) would say "changed" forever.

## 5. The publish contract (slice 2)

**One addition to one existing call**: `variant` on Teletubby's `script.write` (`write_script`).

| Question | Answer |
|---|---|
| Where the type lives | `INPUT.write_script` in `teletubby/src/core/input-shapes.ts`, published through `capabilities` and `api/openrpc.json`. Teletubby owns its door, so the schema that refuses a bad call also documents it. |
| Why not fli-core | Both apps consume it by pinned tag. A shared type would need a release in a third repo for one optional field that has one writer and one reader. |
| Who writes what | Story Pilot writes `script/storypilot/...` only. Teletubby writes `fli.tubby.json` only, through its own verb. Unchanged (FliStudio lane rule R4). |
| File | `<project>/fli.tubby.json`, still `schema: 1`. One additive optional field on a transcript. |
| Who calls it | `handoverOf` (`flistudio/modules/storypilot/server/story.ts:311`), the one place that builds the call. `story.script.send` and an agent following `story.brief` both use it. |

### The call

```jsonc
{ "method": "script.write", "params": {
    "id": "storypilot-project",           // unchanged: one Teletubby script per video
    "name": "Story Pilot — Overlay Pilot",
    "text": "First paragraph.\n\nSecond.",
    "project": "d13-overlay-pilot", "video": null, "takeaway": "...", "source": "...",
    "triggers": { "...": "unchanged" }, "chapters": [ "unchanged" ],
    "variant": {                          // NEW, optional
      "id": "main-3f9a1c2e",              // non-empty slug, stable for this variant
      "label": "Tolkien · teaching · long", // free text, 1 to 80 characters
      "version": 8                        // integer, 1 or more
    } } }
```

### The file

```jsonc
// fli.tubby.json → sets[] → scripts[] → transcripts[]
{ "id": "main-3f9a1c2e", "kind": "variant", "corpus": "main-3f9a1c2e",
  "talentId": null, "source": "Story Pilot (FliStudio) ...",
  "variant": { "label": "Tolkien · teaching · long", "version": 8 },   // NEW
  "topics": [ ], "triggerSets": [ ] }
```

The transcript's `id` **is** the variant id. `corpus` carries it too, because that field is id-format and cannot hold a free-text label. `kind` is a new value, `variant`: a script may hold only one `provenance` transcript because that is the originator's approved baseline (`domain.ts`, `validateScript`), and a regeneration is not that. A variant mark and the `variant` kind always go together, and `write_transcript` cannot create one.

### What `write_script` does when `variant` is present

| Situation | Result |
|---|---|
| Script does not exist | Created with this one transcript. |
| New variant id | Transcript **appended**, so chips never reorder under the talent. Script title, takeaway, summary, video and `n` are not touched. |
| Same id, higher version | That transcript replaced in place. Every other transcript untouched. |
| Same id, same version, identical content | `applied: false`, `unchanged: true`. No write, **no change event**. |
| Same id, same version, different triggers, chapters or label | Replaced in place. The version does not move: the words did not change. |
| Same id, same version, **different text** | Replaced in place, version unchanged. This happens when a recorded paragraph becomes a "plays here, not read" cue line: `presenterOf` (`segments.ts:109-119`) changes what is sent while the stored version's text is the same. |
| Same id, **lower** version | Refused `conflict` (409) with `details: { held, sent }`. A late or doubled send can never roll back the words. |
| Script holds the old unlabelled `text` transcript | Dropped on the first variant publish, which is how d13's existing script moves over with no migration step. If `text` is on stage, this counts as an in-place update: see 7.4. |

Without `variant`, behaviour is exactly today's, with one exception: a plain `write_script` on a script that **has** variants is refused `conflict`, because today's whole-script replace would silently delete them.

The successful answer adds `variant: { id, version, previousVersion, created }`. All existing fields stay.

### Staging

`stage_select` gains an optional `variantId`. FliStudio's `app.stage` passes it through. Its early return must compare the variant too: `shows()` (`doors.ts:366`) checks set and script only, and `readPosition` (`doors.ts:347`) drops the `transcriptId` that `workspace.position` already carries. Without that fix a new variant published while its script is on stage would never be staged. See 7.3.

### Read back

`video.text` gives each script a `variants: [{ id, label, version, text }]` (empty for a script with none). Its `text` stays for other callers. `teletubbyState` compares the **sent** text (`script.presenter`, as it does today) against that variant's text in Teletubby.

## 6. Story Pilot behaviour (slice 3)

### 6.1 Variant id

Derived, with nothing new stored:

```
profile   = the recipe the current words were built from:
            walk back from the newest version, following restoredFrom,
            to the first with build.recipe; else none
key       = kind + narrator + the ids of the four parts (voice, verbal, build, video)
variantId = no profile → <scriptId>
            profile    → <scriptId>-<first 8 hex of sha256(key)>
```

| The talent does | Variant | Why |
|---|---|---|
| Edits words | Same | Same script, same profile. |
| Picks a new profile but has not rebuilt | Same | The words were not built from it. `story.recipe.set` only stores a choice, so the script's own recipe is never read here. |
| Reruns with the same profile | Same, version goes up | No format change. |
| Reruns the same script with a different profile | **New** | Different key. |
| Creates a new script from this one and builds it | **New** | Different script id. |
| Undo or restore, within one profile | Same, version goes up | Restore writes a new version, and the walk follows `restoredFrom`. |
| Undo or restore **across a rebuild** in another profile | **Back to the earlier variant**, version goes up | The words are that variant's words again. A publish lands on its chip, and the toast names that chip. |

Part **pins** (content hashes) are excluded: refining a voice guide is not a regeneration in a new profile. Lenses and one-off instructions are excluded for the same reason. **Style** is excluded because it is only the bundle the parts started from: the same four parts chosen by hand or through a bundle are one profile.

### 6.2 Version

`version` is Story Pilot's own version number `n`, so the number in Teletubby is the row in Story Pilot's History. No second counter.

- It is the `n` of the **oldest version in the unbroken tail with the current words**, so a title or direction row with unchanged words does not bump it. The comparison is on the **stored version text**, not the presenter text that is sent (see the same-version row in section 5).
- One saved edit then republish is exactly +1. Several saves between publishes go up by that many; the number still only rises. **Called out for review:** the brief says "version+1", and a separate publish counter would give two numbers both called version.
- **A publish ends the 10-second fold window.** Stored as `published: true` on the version (a new optional field on `StoredVersion`); the fold test in `appendVersion` gains `!head.published`. Otherwise an edit right after a send would change the words under an already-published number.

### 6.3 Label

- Default: the voice part (else the narrator) · the build structure if it adds anything · the kind without `-story`. No profile: the script's title, else `as written`.
- Custom: a text box beside Send to Teletubby, showing the default. `story.script.send` takes an optional `label`, stored per variant in `script.json` (`variantLabels`). Changing it republishes the same version with the new label.
- Two variants can end up with the same default label. The tooltip shows the id, and the free-text label fixes it.

### 6.4 The send

`putInUse` stays. The toast says what happened and names the variant: `"…" v8 in place, position kept`, `New variant "…" in Teletubby`, or `Teletubby already has this`. A busy talent on a **different** variant reads as `arrived, not moved`, and is not shown as an error.

## 7. Teletubby behaviour (slice 4)

### 7.1 Read

Transcript and schema gain optional `variant: { label, version }`. `src/shared/domain.ts`, `domain-schema.ts`, schema mirror and `api/openrpc.json` regenerate.

### 7.2 The selector

The existing footer chips. One chip per variant, showing `variant.label ?? corpus`.

- A variant chip does not get the "source" tag: it isn't `provenance`.
- Label cut at about 24 characters, full label and version in the tooltip. The row scrolls rather than pushing the style chips off the strip.
- The version number is **not** on the chip: it would be something to read, and nothing about the take depends on it. It shows in the tooltip and setup panel.
- The arrival dot already means "landed, not yet looked at" and is reused as is, on a variant that is new or changed while not shown.
- A variant switch is silent (rule 2), lands at that variant's last paragraph this session, else its first. **Not** `correspondingParagraphId`: its topic ids are positional across unrelated stories, so it would land somewhere confident and wrong. Session memory only.

### 7.3 Staging never moves a talent already there

`stage_select` with the script and variant already on stage returns `{ applied: false, alreadyOnStage: true }` **before** the busy check. `applyStageRequest` does nothing in that case: no `selectScript`, no step change, no cue. `app.stage` reports `staged` at once. This is the door's own guard: it must hold however the call arrives, not only behind `app.stage`'s early return.

**A different variant of the script on stage:**

| Talent | Result |
|---|---|
| Moved in the last 2 minutes | `app_busy` as today. The variant arrives with its dot and the talent is not moved. |
| Idle | Moved to the published variant, silently, as a chip press would. They just pressed Send on it. |

To tell variants apart, `TalentActivity.observe()` keeps `transcriptId` (`src/core/stage.ts:77-82` drops it today; `workspace.position` already has it). `StageRequest` carries `variantId` too. A change of `transcriptId` counts as the talent moving, unless the window is landing where an agent just asked (`observe()`'s `onRequest` match, which must compare the variant).

### 7.4 In-place update keeps the position

A pure `reanchorParagraph(oldParagraphs, oldId, newParagraphs)` in `src/core`, used by `refresh` when the words of the variant on stage changed. It also runs across the one id change that is an update: when the unlabelled `text` transcript on stage is dropped by the first variant publish, the window follows the variant that replaced it (the only transcript left) and re-anchors by content, instead of falling through to `defaultTranscript` and `correspondingParagraphId`. In order:

1. The same text exists: the match nearest the old index.
2. Else the best word overlap of at least 0.5 (Dice on lower-cased words), nearest on a tie.
3. Else the same index, clamped to the last paragraph.

Case 3 replaces the existing "land at the end" fallback **for a version update only**: a deleted paragraph should land on the next thing to say. The trigger position keeps its ordinal within the paragraph, clamped.

### 7.5 Only the changed words move

On an in-place update:

- No cue card, no arrival dot, no animation, no flash, no remount of the stage.
- Unchanged paragraphs render identical text. The changed words swap; lines after them in that paragraph may re-wrap.
- The live paragraph stays on the reading line (rule 7). If a change above it shifts layout, it is re-seated with no animation.
- Anchored by paragraph and line, never by a pixel offset.
- Voice on: the driver is rebuilt from the new text at the live paragraph, re-anchoring exactly as a press does, so word tracking restarts at that paragraph's first word.

### 7.6 No editing

No field, button or verb in Teletubby changes words, labels or versions. The selector only chooses.

## 8. Done-check

| Slice | Proof |
|---|---|
| 2 contract | Teletubby: `write_script` table above, one test per row. FliStudio: `handoverOf` pins the exact call. |
| 3 Story Pilot | `variantId` table, version tail, fold ends at publish, label default and custom, `video.text` variants. FliStudio generators and doc checks pass. |
| 4 Teletubby | `reanchorParagraph` cases including insert before, delete, rewrite, and `text` to variant. `stage_select` at the door: script and variant on stage, idle and busy → `applied: false`, step unchanged, no cue. Different variant, idle → moved; busy → `app_busy`. Refresh keeps step with no cue. Real window: live paragraph's top within 1px after republish. FliStudio: `app.stage` with a different variant is not short-circuited; with `readPosition` null it does not reset the talent (defect 1, path b, reachable only on a cold start or a failed `list_rigs`, so tested here rather than in a window). |
| 5 Acceptance | On the d13 copy, real apps, screenshots. **Step one: with the old unlabelled script on stage, scroll mid-way and publish** (`text` to variant, position kept). Then: edit a few words and republish (position kept, words changed; all other paragraphs identical through `get_set` full, and the visible ones checked on stage); direct `stage_select` for the same set, script and variant mid-way, once busy and once after more than 2 real minutes idle (`applied: false, alreadyOnStage: true`, position and top unchanged: defect 1, path a); insert a paragraph above and republish (still on the same words: defect 2); a republish that changes a trigger above the live row enough to re-wrap it (active row in the driven list, Triggers-driven and Paragraph-driven, focus off and `D`; settled delta at most 1px after the new words are in the DOM plus 2 frames); generate a second variant with a different profile while busy (chip appears with dot, talent not moved); publish a variant while idle (talent moved to it); switch and switch back. |

`test_audit`: `dev-team:audit-test-quality` on the new tests. `duration`: from queue timestamps.

**How acceptance runs** (settled by a real run): Teletubby through Playwright's `_electron.launch` on the built app, because its renderer needs Electron's preload; FliStudio in an ordinary Playwright browser. Both point at a fixture home whose brand root is the d13 copy.

**The second variant's route**: `story.recipe.set` for a different profile, `story.script.set` with new words and `kind: build`, then `story.build.record`. That is the real server path with no model call; it does not prove anything about real model output.

**Test ids (slice 4)**: `live-row` on the active row in each zone; `live-paragraph` with `data-paragraph-id`; `transcript-chip` with `data-transcript-id` and `data-active`; `arrival-dot`; `cue-card`.

## 9. Out of scope

- Editing in Teletubby, ever.
- Version history, diffs or going back in Teletubby. Story Pilot has them.
- Deleting or archiving a variant from Teletubby's selector.
- Highlighting what changed on the stage: it would add something to read.
- Generating triggers for a variant. A variant with none shows the existing "nobody authored them" state (rule 3). All seven d13 scripts have triggers.
- Elgato Prompter send (`story.prompter.send`), unchanged.
- A per-variant view of Story Pilot's History. One `versions/` folder serves every variant of a script, so a variant's "own history" is the rows from its profile; Story Pilot's History shows them all together.
- A shared fli-core type.
- Migrating Teletubby sets other than by the first publish.
- Merge to main and M4 deploy.

## 10. What was checked, and what was not

**Read**: both repos' CLAUDE.md and agent notes; the code cited above; the talent's session transcripts; the d13 test copy (one Teletubby script, 26 paragraphs, 6 chapters, seven Story Pilot scripts, each with triggers).

**Not run**: nothing here was executed. The three defects are traced from code, and independent review confirmed 2 and 3 and corrected the trace of 1.

**Checked, and it adds to slice 4**: the stage position (`StagePosition`, `src/core/stage.ts:29`) holds set, script and paragraph, not the transcript. `workspace.position` (`src/shared/rig.ts:118-124`) already has the transcript id; `observe()` drops it. Keeping it is a core change, not a window change (7.3).

**Not checked, could change slice 4's size**: how far Chromium's scroll anchoring already holds the live row when text above it re-wraps. If it does, the re-seat in 7.5 is only a backstop.

## 11. Calls made

Recorded with reasons in the rig's notes, not waiting on anyone:

1. A variant is a Teletubby transcript, not a separate script: the selector already exists.
2. Version is Story Pilot's `n`, with no separate publish counter.
3. Variant id is derived from script id plus profile key; nothing new is stored.
4. Contract lives at Teletubby's door, not in fli-core.
5. Version number stays off the chip.

## 12. Round 2: every regeneration is its own script

### 12.1 Why

Round 1's contract and Teletubby's side held up. Inside Story Pilot, though, a variant was only a hash on one shared timeline: rebuilding a script with other guides continued the same version list, Undo walked from one variant's words into another's, and the only way to reach an earlier variant was finding its number in History. The talent's words were "each variant has its own version history". Real model rebuilds were also refused at Send, three times out of three, for a trigger rule Story Pilot never checked.

### 12.2 What this supersedes

| Round 1 | Now |
|---|---|
| Section 3: one script can hold several profiles, each a variant | One script is one variant. |
| 6.1: a rebuild of the same script with another profile is a new variant on that script | It is a new script. |
| 6.1: the variant id is the script id plus a profile hash, derived on every send | The id is stored once per script (12.4). Hashes survive only on chips already published. |
| 6.1: undo across a rebuild goes back to the earlier variant | Cannot happen for new work: each script's history starts at its own first version. Existing mixed histories stay as they are. |
| 6.3: default label from voice, build and kind, duplicates allowed | Two variants never show the same default (12.8). |
| 6.4: `putInUse` runs before the write | After Teletubby accepts it (12.6). |
| Section 9: a per-variant view of History is out of scope | History is per script, so that is what it now is. |

### 12.3 The rule: what makes a new script

The rule is enforced by the server, in `story.script.set`, so it holds on the screen, in the Copy instruction and for an agent calling the verbs directly. `story.script.set` gains an optional `mode` (`create`, `update`, `recreate`), used only with `kind: build`.

| A build arrives | The script has no words yet | The script has words |
|---|---|---|
| `create` | Written here | New script |
| `update`, no guide change | Written here | **A version on this script** |
| `update`, guides changed | Written here | New script |
| `recreate`, same or different guides | Written here | New script |
| `kind: build` with no `mode` | Written here | Refused, naming the modes |

**"Guides changed"** compares, by profile key (6.1), what the script would be built from now with what its current words were built from. Words with no recorded build read as the recipe the app already falls back to for them ("as before"). So an Update on a never-built script such as `main` is a version, pressing **Fine** without changing anything stays a version, and that Update's build record gives the words their first profile. Choosing really different guides and then rebuilding is a new script.

**Closing the other ways in:**

- An `agent:*` caller must pass `kind`. There is no default for agents; a person's edit still defaults to `edit`.
- `mode` with anything but `kind: build` is refused.
- While a Rerun is pending on the script, an agent write with `kind: edit` is refused, naming the pending Rerun.
- While a Rerun is pending, a build whose `mode` differs from the mode the screen asked for is refused, naming the asked mode. The screen's choice wins over the agent's flag.

An edit, an undo and a restore by a person are never builds and always stay on the script.

**The new script** takes the source's direction, angle, chosen recipe and selection, as **New from this** does, and `derivedFrom` names the source. Its history starts at version 1. The answer names it: `scriptId`, `forkedFrom`. `story.build.record` must use that `scriptId`. On a new script's first version `previousVersion` is treated as none. The source's Rerun is marked answered.

The source's chosen recipe goes back to the guide ids its own words were built from, with pins cleared so they don't read as changed, or to none if its words have no recorded build. A later Update there is then not read as a guide change.

### 12.4 The id scheme

`script.json` gains `variantId`, written once.

- A script created from now on: its own script id.
- An existing script with no stored id, at its next successful Send, resolved in order and then stored:
  1. Take the newest version marked `published`. Its id is what round 1 would have derived for it, walking back from that version and not from the head, which is the chip it last updated.
  2. Unless a later build with mode other than `update` changed the profile: a regeneration from before this change, never sent. That takes the id derived from the current words, as round 1 did.
  3. No published version: the id derived from the current words.

So `main` keeps updating the `main` chip even after an Update records a recipe for the first time, and a chip with a hashed id keeps that id. The version number stays the script's own `n`.

Accepted limit: a script from before this change that holds two chips resolves to the newest one published, so the older chip keeps its words and no script updates it again. Existing mixed histories stay as they are.

### 12.5 An abandoned or failed rebuild leaves nothing

The new script is created at the moment the words arrive, so a rebuild abandoned before that creates nothing, and a build refused by the trigger check creates nothing either. It carries `building: true` until `story.build.record` succeeds. Until then it is not live: not in the dropdown or `story.scripts.list`, not counted when resolving which script is meant, not in the label collision set, and `use`, `send` and `recipe.set` on it are refused.

**Retrying.** A record that fails leaves it hidden, and `build.py` says so. A build addressed to a source whose new script is still `building` replaces that hidden script; it never makes a second one. A build addressed to the `building` script itself replaces its words too.

Scripts with no words, from **New from this** or a batch, stay listed and read `no words yet`, so they cannot pass for a variant.

### 12.6 Send

**Trigger rule.** Teletubby's rule is unchanged: first trigger on paragraph 1, last on the last paragraph, never backwards. Story Pilot applies the same rule, in `story.script.set` with `kind: build`, before anything is written, so a bad map fails where it is made. The refusal names the trigger and the paragraph to fix.

**A map that goes bad later**, for example an edit that changes the paragraph count: the line beside Send gives the reason instead of "Send it again", and `teletubby.state` is `blocked`. Send stays clickable, so Teletubby's own answer can still be seen. A build with no triggers at all is allowed, as today.

**Teletubby's own reasons.** When Teletubby refuses anyway, its `violations` reach the Send message rather than "the write would break a domain rule".

**The skill.** `appydave-plugins/flivideo/skills/storypilot/SKILL.md` states the three-part rule, and `scripts/build.py` passes `mode`, records against the `scriptId` the write answers, and stops on a failed record.

**In use.** `putInUse` runs only after Teletubby accepts the write. A refused Send changes nothing about which script is in use.

**Rerun** names the picked script in its instruction, tells the agent which mode it is and what that does, and says to record against the `scriptId` the write answers.

### 12.7 Words on screen

| Place | Says |
|---|---|
| Dropdown label | Variant (`data-testid="sp-variant-pick"`) |
| Dropdown line | label · version · word count · in use, if it is · no words yet, if it has none. Nothing for not in use: the glossary rules out "draft". |
| New from this, tooltip | A new variant with this one's direction and guides (never its words) |
| The button that makes an empty one | New variant |
| Rerun, Update | Update: a new version of this variant |
| Rerun, Recreate | Recreate: a new variant, this one is kept |
| Fine, toast | "<label>: guides chosen. Rebuild to use them." |
| Beside Send | "This variant is on Teletubby, the same as here." · "Teletubby has an older version of this variant. Send it again." · "This variant is not on Teletubby yet." · the blocking reason |
| Label box | Variant label |
| History heading | Versions of this variant |
| Undo and Restore, toasts | "Back to v7 of this variant" |

"Script" stays where it means the words themselves, such as the Script section. "Use for the project" names no noun and stays.

**When a regeneration lands.** The picker stays where it is and nothing moves. A line beside the dropdown says "New variant ready: <label>", with one click to it, until it has been picked once.

### 12.8 Default labels

Two variants of one story never show the same default. Start from voice · build · kind, in creation order. Where a script's default collides with an earlier one's, only the newer one changes, so an existing chip's name stays stable: add whichever of verbal guide, video guide and narrator differs. If it still collides, a number is the last resort. The set compared is every listed script of the story, not `building` and not archived. A custom label is used as typed and is not compared.

### 12.9 Done-check

Per-step checks use no model calls. The final proof is in the mission brief and qa owns it: real regenerations with both models across at least three scripts, all sent to a real Teletubby, each variant's own history, and `main` plus an already-published chip updating in place, with controls at round 1's commits showing each check can fail. Word edits are versions and prove nothing about variants.

Testable without a model: the 12.3 table, one row each, through `story.script.set`; an Update on a never-built script stays a version; Recreate asked and `update` passed is refused; an agent `kind: edit` during a pending Rerun is refused; the 12.4 resolution on fixtures with published flags; Undo stopping at a new script's first version; a failed record leaving nothing in the dropdown; the 12.6 trigger refusals and the `blocked` state; a refused Send leaving `uses` unchanged; 12.8 collisions.

### 12.10 Out of scope, and what was not checked

Out of scope: a Redo button, removing chips, the Teletubby header. Teletubby should not need to change; its contract is untouched, and it will be named if that proves wrong.

Part of steps 1 and 2: `appydave-plugins/flivideo/skills/storypilot/SKILL.md` and `scripts/build.py`.

Checked by reading: the build, record and create paths, Rerun's instruction, the picker, Teletubby's trigger rule. Teletubby's `violations` already reach FliStudio's refusal details, and only the message text drops them. Nothing here has run.
