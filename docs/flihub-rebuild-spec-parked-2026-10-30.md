# FliHub rebuild: parked spec

> **PARKED 2026-10-30 by David. Nothing built; FliHub v1 is live and unchanged.**

**Purpose**: Everything decided about the FliHub v2 rebuild, in one place, so the rebuild can resume without the chat that produced it. Where this file and the chat differ, this file wins. Where it and the discovery report differ on an item, the discovery report has the evidence and code citations.

**For Agents**:
- Start here when the rebuild resumes. Then read the two linked documents; don't copy from them, they are the evidence.
- Written 2026-10-30 by `flivideo-arch-rsch`, from its session with David. FliVideo builds, merges and restarts belong to `flivideo-orch`; its checkpoint is `/Users/davidcruwys/dev/ad/flivideo/docs/orch-checkpoint.md`.
- **Never stop, restart or `pkill` FliHub v1 or its overmind.** That overmind is shared with AngelEye and Captain's Log.
- Filed in FliStudio as a `dossier` resource on AppyDave **D17** (`d17-flihub-rebuild`), the video about this rebuild.

## Linked, not copied

- Discovery report (inventory, keep/drop table with `file:line`, migration risks, appendices): `/Users/davidcruwys/dev/ad/flivideo/docs/flihub-discovery-2026-10-30.md`. Last change `372cdfa`.
- Discovery brief (why the rebuild started): `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/flihub-rebuild-discovery-2026-10-30.md`.
- Looks artifact: https://claude.ai/artifact/C5tDAED5yB5RXSJsE3dba6. It shows 0 (today, real screenshots), 1 (cleaned up), 2 (denser) and 3 (FliStudio colours).

## 1 · What v2 is

- **Decided by David:** "Rebuild FliHub. It's fine."
- **The shape:**
  - a slim FliHub on the current AppyStack template, with a JSON-RPC door so agents can drive it (a hard requirement);
  - the depcruise fence from day one;
  - built beside v1 on spare ports;
  - v1 stays runnable, and it remains the home of anything not yet re-homed (storage hold/archive, until Q3 is ruled).
- **Why:** FliHub predates AppyStack, has no template marker, and is the one FliVideo app an agent cannot drive.
- **Recommended look: variation 1 (cleaned up).** Dropped features removed, columns lined up, file names on one line, the broken text colours fixed. Every button keeps its name and its place. Variations 2 (denser) and 3 (FliStudio colours) can be combined with 1.

## 2 · The rebuild rule (David)

> "We can drop shit, but we're not changing shit."

Every kept feature keeps its exact behaviour, its buttons, their labels and their positions. "Rebuild is not new features." Anything not on the keep list is dropped or waits; nothing kept gets redesigned.

## 3 · David's rulings

| ID | Ruling |
|---|---|
| Q0 | **No extensions in FliHub or any microapp.** Extensions live only in the root app, FliStudio. Microapps have doors, not extensions. B-roll capture is not a FliHub extension; FliStudio's third extension is probably a "B-roll pilot" (details later). |
| Q2 | **FliStudio alone opens or changes projects.** This is a guideline, not a hard ruling, and overriding it must be done holistically. FliHub v2 opens on what FliStudio sends (C1). The in-app brand switcher, project dropdown and pins (C2, C3) likely go. |
| Q5 | MicCheck and the sound-level tools are not FliHub's. They become future FliStudio (setup) extensions. Old artifacts exist, some possibly on Roamy. |
| Q6 | B-roll is out of scope. "Rebuild is not new features." |
| Q7 | Renumber and swap are useful. Build them cleanly into the segment operations (T2), and don't follow the old naming conventions. |
| Q8 | Drop the Assets, Inbox and Thumbs tabs, the Transcripts tab, and POEM/AWB/YLO send. |
| Q9 | Gling is gone; that's FliCut's job. Drop Gling prep and the dictionary, after the cut-over step in §7. |
| Q10 | Shadow recordings are gone. |
| S1 | The recording source is configurable: Ecamm today, possibly OBS later, each with its own folder and naming rules. Only Ecamm is built and tested; no OBS testing. Per machine, see §4. |
| C7 | Delete-a-whole-project is dropped (recorded in the discovery report). |

Counts after these rulings: **19 keep, 26 drop, 10 unsure.**

## 4 · Recording source: per machine, in `~/.fli/machine.json`

- **Where it lives:** `~/.fli/machine.json`, through fli-core. This is the existing per-machine settings convention: `fli-core/src/machine.ts:11`, "this machine's settings" (D5, roadmap §1.2b).
  - It is not FliHub's own config, and not per brand: it describes the machine and its recording software, not a channel.
  - An earlier suggestion, `~/.config/appydave/`, was withdrawn in favour of this.
  - flivideo-orch ruled the same way.
- **Shape**, a list of sources:

```json
{ "id": "ecamm", "label": "Ecamm Live", "watchFolder": "<Ecamm output folder>", "filePattern": "<Ecamm file-name pattern>", "nameRules": { } }
```

  Fields: `{id, label, watchFolder, filePattern, nameRules}`. **Only Ecamm is filled in.** The values come from v1's current config (V4: watch folder and recording names). OBS can be added later without restructuring.
- **Who builds it:** this is a small fli-core addition. It is part of the v2 build, and flivideo-orch owns it.

## 5 · Section 1, Capture: the plain-language walkthrough

This is what was put to David. **He has not yet signed off S1–S5.**

- **S1. Watching the Ecamm folder.** When Ecamm finishes a recording, the file lands in its output folder. FliHub notices straight away and shows it as a card in Incoming. If the page reloads, the cards come back. *Keep.* The recording source becomes the setting described in §4.
- **S2. Naming a take and moving it into the project.** Each Incoming card has today's naming controls: chapter number, take name, suggestions from the common-names list, and optional tags. Choosing gives the file its proper name and moves it into the project's recordings, where it appears in the Recordings panel. *Keep, exactly as it is.*
- **S3. The buttons on each Incoming card** (FR-174, flihub `9e6917e`):
  - **Rename · Keep** (amber): name this take, keep the others.
  - **Rename · Discard** (blue, primary, on the right): name this take, bin the rest. This is David's usual move.
  - **Discard** (red): bin this take.

  The card also has **Send several** (process several takes at once) and the discard confirmation box. *Keep, all unchanged.*
- **S4. Two automatic checks on a new take.** These run quietly in the background while a card sits in Incoming. They show a warning on the card and never block anything.
  - **Wrong shape:** a landscape take in a 9:16 project, or the reverse.
  - **Audio dropouts:** short bursts of dead silence mid-speech that chop off word endings. Found on D01 in 15 of 33 takes, probably caused by Krisp's microphone noise filter.

  *Keep.*
- **S5. Discard goes to the project's `-trash/` folder.** It is moved, not deleted, so it can be recovered until the trash is emptied. *Keep.*

Section 2 (takes and chapters: T1–T9) was next and was never walked through.

## 6 · Estimate

**This is arch-rsch's own estimate. It has never been measured.**

| Part | Agent hours |
|---|---|
| New AppyStack app plus the JSON-RPC door | ~2 |
| Capture flow (S1–S5: watcher, naming, card buttons, exact behaviour) | 3–4 |
| Takes and chapters, renumber and swap | 3–4 |
| The rest of the kept items | 2–3 |
| Recording-source setting in `~/.fli/machine.json` (fli-core) | ~1 |
| Parity tests (behaves exactly like v1) | 2–3 |
| **Total** | **~13–17** |

On top of the build:
- **one real recording day** on v2, done by David, with v1 still available;
- **a cut-over of about 30 minutes**, done by flivideo-orch.

The 10 unsure items can move the total either way.

## 7 · Cut-over steps (in order)

1. Run FliStudio's `words.import-flihub` once, then drop `glingDictionary` from FliHub's `server/config.json`. This is a flivideo-orch ruling; `words.import-flihub` lives at `capabilities/words.ts:278`.
2. Swap ports 5100/5101 and the FliHub entry in `~/.config/appydave/apps.json`. Those ports are hard-coded in FliStudio and apps.json, and AppyRadar probes them.
3. Re-point the skills that call FliHub (`flivideo:flihub` and the others in the discovery report's skills table).

## 8 · Known v1 defect: double-mounted Hold route

`POST /api/projects/:code/hold` is mounted twice on `/api/projects`.

- `hold.ts:86`, mounted at `server/src/index.ts:358`, shadows `storage.ts:167`, mounted at `:362`.
- So the Storage panel's **Hold** button runs the old whole-project copy to T7 and deletes nothing locally, while its toast says "Held heavy files to T7".
- The panel's intended handler (copy the heavy folders, then delete them locally) is dead code.

flivideo-orch confirmed this from the code. It was not run live, and it is not fixed. v2 drops the button (H2), and v1 still has the defect.

## 9 · Still open for David

1. **Section 1 sign-off:** do S1–S5 stay exactly as they are today?
2. **Q1: how big is v2.0?** These are the 10 unsure items:

| ID | Item | The question |
|---|---|---|
| T4 | Park a take ("safe") | Do you park takes? |
| T6 | Ships: one video vs one per chapter | FliHub's job or FliStudio's? |
| T8 | Recently-named strip + undo rename | Keep, or rely on the segment journal? |
| T9 | Chapter context panel while naming | Keep or drop? |
| X4 | Transcript viewers + combine a chapter's text | Keep or drop (FliStudio's `video.text` covers best transcript)? |
| X5 | Local transcription telemetry log | Keep or drop (it sends nowhere)? |
| H1 | Hold / restore / archive / batch offload to T7 | See Q3 |
| H3 | Storage activity log | Goes with H1 |
| D6 | Startup `-safe/` migration | Needed for 2 legacy T7 projects on restore? |
| V3 | Developer drawer | Keep, or let the door's read verbs replace it? |

3. **Q3: hold / archive.** David wanted a clearer explanation first.
   - **Hold** copies a project's heavy files to the T7 and frees the Mac's space.
   - **Archive** moves a whole finished project to the T7.
   - **Restore** brings one back.

   The recommendation is that this belongs in FliStudio, which owns projects. Until that is built, v1 keeps doing it and v2 leaves it out.

**Next step when resumed:** David answers 1–3. Then flivideo-orch writes the v2 build brief. **No build brief until David resumes the rebuild.**
