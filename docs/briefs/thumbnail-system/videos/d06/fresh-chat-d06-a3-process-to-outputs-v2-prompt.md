# ART DIRECTION (read this first — it is the point)

Create a premium cinematic YouTube thumbnail: the creator in his warm, dimly lit home studio, leaning back from his desk with a satisfied got-it grin, pointing at a large monitor. The monitor shows the attached Headshot Picker screenshot exactly as supplied: a wall of his own headshots in a web app. Out of the screen, one finished YouTube-thumbnail card flies toward the viewer, glowing with warm yellow light, featuring one of his headshots. Story: a folder of photos becomes a thumbnail automatically. Warm practical lamps, amber rim light, shallow depth of field, a camera and mic softly out of focus. Photographic realism, finished professional-thumbnail quality.

# RUN NOTES
- Produce ONE finished 16:9 thumbnail for spec d06.a3. Not a contact sheet.
- Attached files, matched by filename: headshot-appydave-13.png, headshot-appydave-29.png, headshot-appydave-1.png, headshot-picker-ui.jpg. Headshots are IDENTITY REFERENCES: invent the pose and expression described, keep him recognisable. Anything marked literal_use is shown as supplied.
- Do NOT render the headline; keep its region calm.
- Judge it as a finished YouTube thumbnail before returning (creative gate), then give a 5-line QC note.

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

# RECIPE
```json
{
  "id": "process_to_outputs",
  "layout_family": "process_visualization",
  "story_shape": "A sequence of processing steps produces one or more visible outputs",
  "layout": "Left-to-right sequence of simplified process frames feeding output icons",
  "presenter_role": "Optional; repeated frames may replace a hero portrait",
  "required_assets": [
    "Authentic or illustrative process frames",
    "Verified output types"
  ],
  "typical_graphics": [
    "Repeated frames",
    "Directional arrows",
    "Output icons",
    "Simplified timeline"
  ],
  "lighting": "Consistent across all frames",
  "background": "Light brand canvas",
  "when_not_to_use": [
    "Processes that cannot be simplified visually",
    "Stories without meaningful outputs",
    "Topics where multiple small frames become illegible"
  ],
  "related_recipes": [
    "agent_pipeline_hero"
  ]
}
```

# THUMBNAIL SPEC
```json
{
  "id": "d06.a3",
  "version": "2.0",
  "schema_version": "1.1",
  "art_direction": "Create a premium cinematic YouTube thumbnail: the creator in his warm, dimly lit home studio, leaning back from his desk with a satisfied got-it grin, pointing at a large monitor. The monitor shows the attached Headshot Picker screenshot exactly as supplied: a wall of his own headshots in a web app. Out of the screen, one finished YouTube-thumbnail card flies toward the viewer, glowing with warm yellow light, featuring one of his headshots. Story: a folder of photos becomes a thumbnail automatically. Warm practical lamps, amber rim light, shallow depth of field, a camera and mic softly out of focus. Photographic realism, finished professional-thumbnail quality.",
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
    "recipe": "process_to_outputs",
    "story": "His photo library now produces thumbnails for him",
    "visual_hook": "A thumbnail card flying out of the picker on screen",
    "hero": "The flying thumbnail card plus the pointing presenter",
    "emotion": "Satisfaction, a system that works",
    "style": "Cinematic creator-studio photography",
    "avoid": [
      "Redrawing or inventing the picker UI",
      "Checkerboards",
      "Cluttered desk"
    ]
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "usage": "identity_reference",
    "references": [
      {
        "file_id": "headshot-appydave-13.png",
        "cid": "c13",
        "why": "standing grin, grey shirt"
      },
      {
        "file_id": "headshot-appydave-29.png",
        "cid": "c29",
        "why": "frontal grin, clear face"
      },
      {
        "file_id": "headshot-appydave-1.png",
        "cid": "c1",
        "why": "frontal neutral, clear face"
      }
    ],
    "performance_to_create": {
      "expression": "Satisfied grin",
      "gaze": "Toward the monitor or the flying card",
      "pose": "Seated, leaning back, one arm pointing at the screen",
      "framing": "Waist-up, left third"
    }
  },
  "assets": {
    "required": [
      {
        "id": "identity_references",
        "source": "attached",
        "files": [
          "headshot-appydave-13.png",
          "headshot-appydave-29.png",
          "headshot-appydave-1.png"
        ]
      },
      {
        "id": "picker_ui",
        "source": "attached",
        "files": [
          "headshot-picker-ui.jpg"
        ],
        "usage": "literal_use",
        "note": "Show on the monitor as supplied; do not redraw"
      }
    ]
  },
  "composition": {
    "canvas": [
      1280,
      720
    ],
    "environment": "hybrid_photographic",
    "layout": "Presenter left third, monitor centre-right, flying card breaking out toward camera on the right, headline zone top",
    "focal_order": [
      "Flying card",
      "Presenter",
      "Monitor",
      "Headline"
    ]
  },
  "rendering": {
    "mode": "cinematic_image_generation_plus_compositing",
    "generate_unified_scene": true,
    "allow_dark_cinematic_background": true,
    "use_reference_photographs": true,
    "generate_final_text_in_image": false
  },
  "text_layer": {
    "headline": "AI PICKS MY FACE",
    "alternates": [
      "PHOTOS TO THUMBNAILS",
      "MY THUMBNAIL MACHINE"
    ],
    "render_mode": "post_composite",
    "font": "Bebas Neue",
    "weight": 400,
    "size_px": 88,
    "minimum_size_px": 64,
    "position": "Top band",
    "bbox": [
      25,
      40,
      190,
      700
    ],
    "color": "#faf5ec",
    "accent": {
      "words": [
        "FACE"
      ],
      "color": "#ffde59"
    }
  },
  "variations": {
    "count": 1
  },
  "quality_checks": [
    "Presenter recognisable as David (face, glasses, hair, age)",
    "One clear visual event, readable in 1 second",
    "Cinematic cohesion: lighting, shadow and depth unified",
    "No checkerboards, no slide or mockup look",
    "Headline region left calm; headline legible at 320x180 after compositing",
    "Picker screenshot shown as supplied, not redrawn"
  ]
}
```