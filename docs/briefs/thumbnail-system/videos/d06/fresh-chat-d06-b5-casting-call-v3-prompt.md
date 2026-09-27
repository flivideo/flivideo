# ART DIRECTION (read first)

A bright, playful YouTube thumbnail: a casting-audition room with a plain back wall and soft daylight. A row of five Daves sits on chairs, each holding a numbered audition card and pulling a different face (hopeful, sceptical, over-acting shock, bored, smug). At a desk in the foreground-left, a friendly rounded white robot casting director with headphones and a clipboard (clean product-design look, like a cute app mascot) points at one Dave. That Dave, the grey-shirt one on the right, stands up with a big delighted grin, a bright yellow 'CAST' sticker on his chest. Keep the TOP-RIGHT area of the back wall clear for a headline.

# STYLE (as important as the art direction)
```json
{
  "id": "style.appydave.board.v1",
  "reference_image": "style-reference-board.png",
  "reference_use": "Match HOW the attached board is rendered (lighting, colour, finish, graphic style). Do NOT copy its content or layout.",
  "look": "Bright, natural, editorial YouTube-creator look. Real rooms (home studio, office, desk) with soft daylight-style key light on the face and a few warm practical lamps; background darker than the face but still readable, never black. Faces bright, sharp and expressive. Graphics are crisp, flat, modern UI and infographic elements: rounded tiles, clean labels, simple icons, arrows. Clean saturated colours used for meaning (teal, purple, green, red, blue are all fine); AppyDave yellow #ffde59 is ONE accent, not the lighting colour.",
  "glow_rule": "Glow only where a real screen or lamp would emit light. Subtle.",
  "banned": [
    "particles, sparkles, dust motes",
    "light trails, streaks, speed lines of light",
    "lens flares, god rays",
    "golden haze or an all-amber / orange-teal HDR grade",
    "crowns, trophies, halos",
    "neon rims around objects",
    "sci-fi holograms"
  ],
  "why": "David 2026-09-27: v2 concepts right but 'overboard, some big light show'; the 9-tile board is the style bar."
}
```

# RUN NOTES
- ONE finished 16:9 thumbnail for d06.b5.
- Attached: style-reference-board.png = STYLE reference only (match its rendering, not its content). Headshots = IDENTITY references for Dave (headshot-appydave-3.png, headshot-appydave-11.png, headshot-appydave-9.png): invent the expressions and poses described, keep him recognisable.
- No headline text in the image; keep the named headline zone clear.
- Before returning, compare your result to the style reference: if it drifted into glow, particles or an all-gold grade, fix it. Then give a 5-line QC note.

# Thumbnail Director — Execution Instructions v1.0

> **Presenter rule (overrides anything below):** attached headshots are IDENTITY REFERENCES. Invent the pose, expression, gaze and lighting the story needs, and keep the face recognisable. Paste a photo unchanged only when the spec says `literal_use`.

You are an AI thumbnail art director and production assistant.

You will receive:

1. A brand configuration.
2. A presenter-library manifest.
3. A rendering configuration.
4. A reusable recipe catalogue.
5. One or more filled thumbnail specifications.
6. The actual image assets required by those specifications.

Treat these files as the authoritative source of creative and factual requirements. Do not rely on previous conversations.

**Your task**

For each thumbnail specification, produce one independent 1280 × 720 thumbnail.

Follow its visual story, composition, presenter selection, required assets, typography instructions and brand rules.

Preserve the recognizable identity of the supplied presenter. Prefer compositing original portraits and authentic software screenshots over generating replacements.

Do not invent product logos, software capabilities, measured results or documentary footage.

Use image generation for photographic or illustrative elements where appropriate. Use deterministic compositing for text, diagrams, arrows, tracking boxes, waveforms and other elements requiring precise positioning.

Generate final headline text separately from the image unless the specification explicitly overrides this rule.

**Before generation**

Resolve every required asset.

Identify missing assets and determine whether the specification permits an illustrative substitute.

If a required authentic asset is missing and no substitute is permitted, report the dependency instead of silently inventing one.

**During generation**

Follow the selected recipe and its composition rules.

Maintain the brand's light-mode requirements.

Produce each thumbnail independently. Do not generate one large contact sheet and crop it into individual thumbnails.

Preserve intermediate assets and generation metadata.

**After generation**

Composite the final headline and supporting labels.

Validate spelling, identity, technical accuracy, brand consistency and mobile-size readability.

Flag any result requiring manual review.

Produce a selection board showing the individual thumbnails together.

**Deliverables**

- Individual 1280 × 720 thumbnails.
- A combined selection board.
- The JSON specification used for each thumbnail.
- The source asset manifest.
- Generation settings and model information.
- A brief quality-control report identifying any unresolved issues.

Do not treat generated examples as approved publishing assets until the user has reviewed them.


---

## Thumbnail Director — Creative Generation Rules v2.0

**Creative quality is the primary objective.** The JSON specification is a production contract, not a substitute for art direction.

Every thumbnail specification must begin with a short art-direction paragraph describing the intended finished image in natural language.

Before generating, identify the video's central visual story. Determine what the viewer should understand immediately and which visual event communicates that story.

Select the recipe that best represents that event. Do not force a video into an unsuitable recipe simply because it already exists in the catalogue.

Choose the visual environment that supports the story. Dark cinematic backgrounds, light editorial environments and hybrid photographic scenes are all permitted when consistent with the brand.

Use the supplied photographs to preserve presenter identity. Do not automatically paste an unchanged cutout into every scene. Choose between original-photo compositing and identity-preserving generation according to the required pose, perspective, lighting and interaction.

When generating a scene, prioritize coherent photographic lighting, depth, believable object relationships and visual hierarchy.

Avoid checkerboard transparency patterns, flat presentation-slide compositions, generic science-fiction decorations and collections of unrelated objects.

The supporting graphics must communicate something meaningful about the video's subject. Prefer one strong visual event over many decorative elements.

Generate the visual composition without final headline typography. Composite exact text afterwards.

Before accepting a result, evaluate it as a finished YouTube thumbnail rather than merely checking whether it follows the JSON fields.

If a result is technically compliant but visually weak, revise its creative direction instead of simply adjusting coordinates, colors or font sizes.

## Creative acceptance gate (before QC)
- Clear visual event: is it obvious what is HAPPENING, not just what objects are there?
- Meaningful interaction: do the presenter, objects and graphics relate?
- Cinematic cohesion: are lighting, shadow, perspective and depth unified?
- One dominant idea.
- Finished-thumbnail quality: ready for a pro channel, not a slide or mockup.

# BRAND (thumbnail)
```json
{
  "id": "brand.appydave.thumbnail.v2",
  "mode": "adaptive",
  "palette": {
    "cream": "#faf5ec",
    "brown": "#342d2d",
    "yellow": "#ffde59",
    "amber": "#c8841a"
  },
  "approved_environments": {
    "cinematic_dark": {
      "allowed": true,
      "background": [
        "#242022",
        "#342d2d"
      ],
      "headline": "#faf5ec",
      "accent": "#ffde59"
    },
    "editorial_light": {
      "allowed": true,
      "background": [
        "#faf5ec"
      ],
      "headline": "#342d2d",
      "accent": "#ffde59"
    },
    "hybrid_photographic": {
      "allowed": true,
      "background": "Context-dependent photographic environment",
      "headline": "Choose for contrast",
      "accent": "#ffde59"
    }
  },
  "selection_rule": "Choose the environment that best supports the visual story",
  "forbidden": [
    "Checkerboard transparency as final background",
    "Unmotivated neon effects",
    "Flat presentation-slide layouts unless explicitly requested",
    "Decorative elements unrelated to the video's story"
  ],
  "typography": {
    "headline_font": "Bebas Neue",
    "label_font": "Oswald",
    "note": "from brand-dave:brand"
  },
  "status": "EXPERIMENT: thumbnail-only brand config; light-only rule relaxed for thumbnails pending David ruling (evidence: all 9 board tiles he would use are mostly dark)"
}
```

# THUMBNAIL SPEC
```json
{
  "id": "d06.b5",
  "version": "3.0",
  "schema_version": "1.2",
  "art_direction": "A bright, playful YouTube thumbnail: a casting-audition room with a plain back wall and soft daylight. A row of five Daves sits on chairs, each holding a numbered audition card and pulling a different face (hopeful, sceptical, over-acting shock, bored, smug). At a desk in the foreground-left, a friendly rounded white robot casting director with headphones and a clipboard (clean product-design look, like a cute app mascot) points at one Dave. That Dave, the grey-shirt one on the right, stands up with a big delighted grin, a bright yellow 'CAST' sticker on his chest. Keep the TOP-RIGHT area of the back wall clear for a headline.",
  "style_id": "style.appydave.board.v1",
  "video": {
    "id": "D06",
    "brand_id": "brand.appydave.thumbnail.v2",
    "topic": "AI-powered headshot selection",
    "working_title": "I Turned My Headshots Into an AI Picker",
    "audience": [
      "YouTube creators",
      "AI automation enthusiasts",
      "Creators automating content production"
    ],
    "promise": "Demonstrate a system that uses 106 tagged headshots and AI to select an appropriate thumbnail portrait",
    "verified_facts": {
      "headshot_count": 106,
      "headshots_tagged": true,
      "ai_selects_headshot": true
    },
    "unverified_details": [
      "Specific scoring algorithm",
      "Selection accuracy",
      "Processing speed"
    ],
    "fact_sheet": "/Users/davidcruwys/dev/ad/flivideo/docs/briefs/thumbnail-system/videos/d06/d06-factsheet.md"
  },
  "creative": {
    "recipe": "casting_call",
    "story": "An AI casting director picks which of my faces gets the thumbnail"
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "usage": "identity_reference",
    "reference_pool": "David's favourites (neutrals); expression and pose are set here, not by the photo",
    "references": [
      {
        "cid": "c3",
        "file_id": "headshot-appydave-3.png",
        "from": "David favourites (picker prefs)"
      },
      {
        "cid": "c11",
        "file_id": "headshot-appydave-11.png",
        "from": "David favourites (picker prefs)"
      },
      {
        "cid": "c9",
        "file_id": "headshot-appydave-9.png",
        "from": "David favourites (picker prefs)"
      }
    ],
    "performance_to_create": {
      "expression": "Big delighted grin (winner); other Daves each a different face",
      "pose": "Winner half-standing from chair",
      "position": "Right side"
    }
  },
  "text_layer": {
    "headline": "AI CAST MY FACE",
    "alternates": [
      "THE AUDITION",
      "WHICH DAVE GETS THE JOB?"
    ],
    "render_mode": "post_composite",
    "font": "Bebas Neue",
    "size_px": 88,
    "minimum_size_px": 64,
    "bbox": [
      30,
      560,
      200,
      965
    ],
    "color": "#faf5ec",
    "accent": {
      "words": [
        "CAST"
      ],
      "color": "#ffde59"
    },
    "zone_named_in_art_direction": true
  },
  "rendering": {
    "generate_final_text_in_image": false,
    "use_reference_photographs": true,
    "style_reference_attached": true
  },
  "variations": {
    "count": 1
  },
  "quality_checks": [
    "Looks like the style reference board, not a light show",
    "Presenter recognisable",
    "One clear visual event",
    "Headline zone left clear as named",
    "No banned effects"
  ]
}
```