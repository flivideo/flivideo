# Per-video thumbnail brief format

**Purpose**: The one input that changes per video. It's the existing FliVideo fact sheet plus a `thumbnail_assets` section.
**For Agents**:
- Write one per video before picking recipes. The worked examples are `../thumb-research-2026-09-26/d01-factsheet.md`, `d02-…` and `d03-…`.
- A recipe may only use an asset listed under `thumbnail_assets` with status `have`. Never design around an image that doesn't exist.

---

## Sections (the existing fact-sheet format)

```markdown
# dNN — <working title> (<brand>) — video fact sheet

**Status: <recorded | NOT FINISHED | published>.** Takes, word count, runtime, what's missing.

## Titles
- **Working title:** …
- Option 1–3: …            (mark "not approved" until David signs off)

## Premise
## Who it's for
## The promise
## Chapter by chapter        (| # | Chapter | What's shown | Key line |)
## Strongest visual moments  (the concrete visuals a thumbnail could use; the most valuable section)
## Proper nouns              (plus transcript mis-hearings to ignore)
## Tone / brand              (brand id → brands/<id>.json)
## Already decided about thumbnails
## What's missing
```

## New section: `thumbnail_assets`

Put it at the end of the fact sheet as a fenced YAML block, so it can be parsed.

```yaml
thumbnail_assets:
  brand: appydave                      # → brands/appydave.json
  presenter:
    on_camera: david                   # david | other | none. d03's demo presenter is a Thai speaker, not David
    face_in_thumbnail: undecided       # yes | no | undecided (David's call; d02 is still open)
    portrait_roles_wanted: [surprised, pointing-right]
    library: "portrait library: location TBD from portraits-rsch"
    fallback: /Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/
  screenshots:                         # real product UI. Composite it; don't let the model invent it
    - id: flihub-inbox
      what: FliHub inbox with transcript badges
      status: have | need              # need = must be captured before this recipe can run
      path: <absolute path or blank>
  footage_frames:
    - id: thai-presenter-quadrants
      what: frame with N/S/E/W quadrants over the presenter
      status: need
      path:
  logos: [flivideo, cutty]             # ids resolved from the brand config
  props_real: [fan, air-conditioner]   # things that really appear in the video
  headline_candidates:                 # short; the text layer picks one
    - "FANS ON. STILL CLEAN."
  must_be_accurate:                    # facts a thumbnail must not get wrong
    - "Cutty is the agent; FliCut is the app"
```

**Rule**: a spec's `assets` block may only reference ids from this list. A recipe that needs something marked `need` is flagged at the recipe-pick step instead of being invented.
