---
created: 2026-10-09
timestamp: 2026-10-09
---

# Requirements bundle for openrig-orch (2026-10-09)

**Purpose**: Everything David raised on 2026-10-09 that is headed for openrig-orch (Roamy), gathered in one place. David routes it; flivideo-orch does not send it.

**For Agents**: Each item says where its detail lives. Items marked HELD are not ready to build.

## 1. Thumbnail configuration in FliStudio (from the interview)
- Thumbnail = image + **prompt (its own resource, linked by code; one prompt → many thumbnails)** + **0..n text variants, 0 or 1 selected**, every variant kept.
- **Text position stored per variant**; FliStudio draws the final thumbnail (text over image), so moving text re-renders without regenerating the image.
- Presenter refs: 0..n links into the brand's presenter B-roll (0 = no presenter). The headshot-proposal UI is HELD (risk of a big build).
- Before designing: read FliGen Day 8 thumbnail generator (FR-12/FR-19: Save to Library with full config, Reuse Configuration) — `/Users/davidcruwys/dev/ad/flivideo/fligen/docs/FR-19-DEVELOPER-HANDOVER.md`.
- Rule: each step (prompt, render, text layout) exists once as a callable piece; the ylo skills and FliStudio both call it. Current pipeline: ylo-pairs → `thumbnail-system/tools/build_prompt.py` → ThumbDrip (ChatGPT) → `tools/composite_headline.py` → `resources.add`.

## 2. Lightweight B-roll in FliStudio
- Presenter is a B-roll type per brand (AppyDave: 106 cutouts at `/Users/davidcruwys/dev/image-projects/i-appydave/presenter/`; AITLDR: Alex).
- FliStudio LINKS/QUERIES B-roll by code, never owns it; B-roll becomes a first-class app later, so migration is a move, not a rewrite.
- Reference material for a video (e.g. Nick's channel screenshots, thumbnails, notes) needs an **image kind** in the `knowledge` group (CT-0106 has dossier/capture/link/note only) and probably brand-level storage for material reused across videos.

## 3. FliEdit overlays on a FliCut export
Five tickets + nice-to-haves, with live verification: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/fliedit-overlay-use-case-2026-10-09.md`. API-page bar and gap work: `/Users/davidcruwys/dev/ad/flivideo/docs/briefs/fli-api-bar-2026-10-09.md`.

## 4. Skool: research + a Skool agent (NEW, David 2026-10-09)
- David doesn't know what Skool can do beyond the basics (e.g. free posts inside a paid community, free tiers, a separate free community). Research Skool's actual features from primary sources, against the existing brain `/Users/davidcruwys/dev/ad/brains/skool/` (8 files; latest audit `appydave-community-audit-2026-09-14.md`).
- Peer evidence (screenshots 2026-10-09): RoboNuggets and Chase AI run a **separate free Skool community** for freebies next to the paid one; Simon Scrapes links a per-video doc on a second Skool URL. Not verified how.
- Goal (David): a Skool agent so learnings compound over time; and the description tool can split "free" vs "members" automatically once real freebies exist.

## 5. Description tool (ylo-description) — APPROVED 1–4 (David 2026-10-09)
1. Top line = this video's resource: "Get the <thing> from this video → <Skool link>". Today's model: **members get it** ("available to members of the AppyDave community"), since everything is in the low-cost paid community; a true-free variant comes later (see §4).
2. Body = 3 sentences, problem first, + "The short version: <one-sentence answer to the title>".
3. A keyword sentence near the bottom (keyword spine).
4. Related same-topic videos (series path).
Evidence: `/Users/davidcruwys/dev/ad/brains/youtube-craft/practice/descriptions-sources-2026-10-09/peer-teardown-jev-cohort.md`.
