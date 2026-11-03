# Story Pilot W2: the Reader and source cards say what they are

**Purpose**: Build brief for W2 of the Story Pilot plan. Uses W1's island registry and dock extract so the Reader shows
each Document Island honestly: what it is, where it lives, your words vs Claude's vs an AI summary, and the whole text.

**For Agents**: Read in full. Starts only after W1 is merged (it reads W1's registry, `story.source.read` paging, the
CL live card and the deep link). Background is the design note
`docs/briefs/storypilot-captains-log-mapping-2026-11-03.md` (sections "What David saw", "Session sources",
"Dossier sources", "Session RAW", "Note sources"). Owner: `flivideo-orch`. From: `flivideo-roamy`. No David decisions
needed: the look follows the AppyDave app rules (cream page, white cards, hairlines; no filled-box-in-filled-box).

## What David saw (screens, 2026-11-03)

1. A Captain's Log source badged CAPTURE, with no link out, and an agent instruction printed to him ("read it in
   Captain's Log (captains-log:find…)").
2. A session's RAW box: only the first paragraph of each turn says "David:"; nothing says Claude's side is hidden;
   `[Image #3][Image #4]` placeholders leak; skill text shows up as his (fixed in W1); "(the first part shown)" with no way
   to see the rest.
3. A spec badged DOSSIER with its whole header card (Status / Name / Session / Merged / One-line take) above the fold.
   He couldn't tell what it was.
4. The "Send to session" box sits folded below the whole Story Pilot page. He didn't find it.

## Changes

**A · Badges and the "Where it came from" box**
- The badge = the island's nature from W1's registry (Plaud recording, Claude session, ChatGPT dossier, Spec / doc,
  Agent note, Claude artifact, Web link, B-roll). Captain's Log islands also show `CAPTAIN'S LOG · B663`.
- One **Open ↗** link per island when the registry has an open target (CL deep link, file path, URL). Never print agent
  instructions to the human.
- "Where it came from" lists home, machine and path or code, extract freshness ("extract from 3 Nov, transcript
  unchanged" / "out of date"), and who attached it.

**B · Captain's Log card**
- Under our title and why: a live strip of synopsis · date · length · source · signal · state, from W1's card. Offline
  → one quiet line, keep the rest.

**C · Sessions read like a conversation**
- Chat-style: David's turns shown, each fully marked as his. Claude's turns folded to one line each ("Claude replied:
  412 words · show"), expandable in place.
- Header: "Claude Code session · <purpose if known> · <date> · <name> · <machine>".
- No `[Image #n]` placeholders (replace with a small "image" chip, or drop).
- **Show the rest:** never a silent cut. Page through W1's `offset`/`limit`, with "show more" and a count.

**D · Documents put the story-relevant part first**
- For a spec/doc island: the one-line take and David's 👤 quotes first, then the header card and the full body folded
  behind "the whole document".

**E · Send to session where you can see it**
- Move the box out of the page bottom: a compact "Send to session" control in Story Pilot's header area (or the side
  rail), opening the existing panel. Keep it OFF unless `FLISTUDIO_SEND_TO_SESSION=1`, local-only, token-guarded.

## Out of scope

New panels or a JSON viewer; rerun, versions and undo (W4); story instructions content (David will talk it through
later); any change to how sources are stored (W1 owns that).

## Gate and report

Unit + typecheck; the full storypilot suite; `storypilot-reader.spec` extended to cover the badge per kind, Open ↗, the
CL strip (mocked), the chat view with folded Claude turns, "show more" paging, and the moved Send-to-session control.
Every other suite green. Build on the M2, re-gate and merge on the M4, restart via `my-app`. Then screenshot four states
on d13: (1) a Captain's Log card, (2) a session in chat view with one Claude turn expanded, (3) the spec card, (4) the
Send-to-session control. Report to `flivideo-roamy` with commits, counts and screenshot paths.
