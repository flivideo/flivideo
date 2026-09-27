# ART DIRECTION (read this first — it is the point)

Create a premium cinematic YouTube thumbnail showing a creator who has built an AI system to select his best headshot. On the left, a collection of photographic portraits recedes into a sophisticated, dark digital workspace. One portrait has been selected and emerges dramatically from the collection, illuminated by warm yellow light. On the right, a large, recognizable portrait of the creator reacts with genuine astonishment, looking toward the selected photograph. Use photographic realism, carefully controlled lighting, dramatic depth, luminous interface details and a powerful visual hierarchy. The image must feel like a finished thumbnail from a professional technology creator, not a presentation slide, photo gallery or software mockup. The central visual story is that AI has selected one image from a large library.

# RUN NOTES
- Produce ONE finished 16:9 thumbnail for spec d06.a1 v2. Not a contact sheet.
- Attached PNGs are identity references and candidate headshots, matched by filename: headshot-appydave-23.png, headshot-appydave-15.png, headshot-appydave-58.png, headshot-appydave-29.png, headshot-appydave-86.png, headshot-appydave-20.png, headshot-appydave-30.png, headshot-appydave-33.png, headshot-appydave-13.png. You may re-pose and relight the presenter to fit the scene; keep his face, glasses, age and hair recognisable.
- Do NOT render the headline; leave its region (upper left) calm. Labels '106 HEADSHOTS' / 'AI PICK' may be omitted if they compete.
- Judge the result as a finished YouTube thumbnail before returning it (creative gate in the instructions), then give a 5-line QC note.

# Thumbnail Director — Execution Instructions v1.0

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
  "id": "ai_selection_reveal",
  "layout_family": "decision_reveal",
  "story_shape": "A system evaluates many candidates and selects one",
  "dramatic_event": "One result emerges from a collection",
  "visual_hook": "A single highlighted winner",
  "layout": "Receding candidates, dominant selection and optional human reaction",
  "presenter_role": "Surprised, curious or confident",
  "required_assets": [
    "Candidate images",
    "Selected image or approved illustrative selection",
    "Optional presenter portrait"
  ],
  "typical_graphics": [
    "Selection border",
    "Directional flow",
    "Subtle evaluation indicators"
  ],
  "preferred_environment": "cinematic_dark",
  "lighting": "High-contrast editorial lighting with one strongly illuminated result",
  "visual_hierarchy": [
    "Selected result",
    "Human reaction",
    "Candidate collection"
  ],
  "when_not_to_use": [
    "Videos without a meaningful selection process",
    "Situations where the selected result cannot be represented accurately",
    "Topics that require detailed numerical comparisons"
  ]
}
```

# THUMBNAIL SPEC
```json
{
  "id": "d06.a1",
  "version": "2.0",
  "schema_version": "1.1",
  "art_direction": "Create a premium cinematic YouTube thumbnail showing a creator who has built an AI system to select his best headshot. On the left, a collection of photographic portraits recedes into a sophisticated, dark digital workspace. One portrait has been selected and emerges dramatically from the collection, illuminated by warm yellow light. On the right, a large, recognizable portrait of the creator reacts with genuine astonishment, looking toward the selected photograph. Use photographic realism, carefully controlled lighting, dramatic depth, luminous interface details and a powerful visual hierarchy. The image must feel like a finished thumbnail from a professional technology creator, not a presentation slide, photo gallery or software mockup. The central visual story is that AI has selected one image from a large library.",
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
    "recipe": "ai_selection_reveal",
    "story": "AI examines a collection of headshots and selects one",
    "visual_hook": "One dramatically selected portrait emerging from many candidates",
    "hero": "Selected headshot",
    "secondary_hero": "Presenter reacting to the AI selection",
    "emotion": "Discovery and astonishment",
    "visual_metaphor": "One photograph emerging from a digital library",
    "style": "Cinematic photographic technology editorial",
    "reference_quality": "Original nine-concept thumbnail board",
    "avoid": [
      "Presentation-slide appearance",
      "Checkerboard transparency patterns",
      "Six equally prominent portrait cards",
      "Flat portrait gallery",
      "Generic futuristic holograms",
      "Unnecessary interface decorations",
      "Unnaturally exaggerated facial expressions"
    ]
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "identity_reference": {
      "source": "Headshot Picker artefact https://claude.ai/artifact/EZbkmPK3zb8Vfi7u5soeQF (attached PNGs)",
      "required": true,
      "preserve_face": true,
      "preserve_glasses": true,
      "preserve_natural_age": true,
      "preserve_hairstyle": true
    },
    "reaction_portrait": {
      "portrait_role": "surprised",
      "preferred_asset": "headshot-appydave-23.png",
      "file_id": "headshot-appydave-23.png",
      "expression": "Authentic astonishment",
      "pose": "Upper body angled toward selected photograph",
      "gaze": "Looking toward the selected photograph",
      "position": "Right foreground",
      "framing": "Large cinematic close-up",
      "bbox": [
        70,
        590,
        980,
        990
      ],
      "generation_policy": "Use original photo when pose works; otherwise generate a reviewed identity-preserving variation",
      "cid": "c23"
    },
    "selected_portrait": {
      "portrait_role": "confident",
      "preferred_asset": "headshot-appydave-15.png",
      "file_id": "headshot-appydave-15.png",
      "position": "Left-center",
      "framing": "Large selected portrait card",
      "bbox": [
        200,
        220,
        850,
        580
      ],
      "selection_status": "Illustrative selection, not a verified AI result",
      "cid": "c15"
    }
  },
  "assets": {
    "required": [
      {
        "id": "identity_references",
        "source": "attached",
        "status": "provided",
        "minimum_count": 3,
        "files": [
          "headshot-appydave-23.png",
          "headshot-appydave-15.png",
          "headshot-appydave-58.png"
        ]
      },
      {
        "id": "candidate_headshots",
        "source": "attached",
        "status": "provided_subset",
        "minimum_count": 6,
        "files": [
          "headshot-appydave-29.png",
          "headshot-appydave-86.png",
          "headshot-appydave-20.png",
          "headshot-appydave-30.png",
          "headshot-appydave-33.png",
          "headshot-appydave-13.png"
        ]
      }
    ],
    "optional": [
      {
        "id": "actual_ai_selection",
        "source": "<VIDEO_ASSETS_ROOT>/D06/selection-result.json",
        "purpose": "Identify the photograph genuinely selected by the system"
      },
      {
        "id": "actual_application_screenshot",
        "source": "<VIDEO_ASSETS_ROOT>/D06/picker-interface.png",
        "purpose": "Optional authentic supporting interface"
      }
    ],
    "asset_requirements": {
      "preserve_identity": true,
      "use_supplied_headshots": true,
      "do_not_invent_additional_people": true,
      "do_not_fabricate_real_application_screenshots": true,
      "allow_illustrative_selection_interface": true,
      "do_not_present_illustrative_selection_as_actual_result": true
    }
  },
  "composition": {
    "canvas": [
      1280,
      720
    ],
    "aspect_ratio": "16:9",
    "coordinate_system": "normalized_1000",
    "background": {
      "description": "Sophisticated dark cinematic digital workspace",
      "primary_colors": [
        "#242022",
        "#342d2d"
      ],
      "secondary_colors": [
        "#faf5ec",
        "#ffde59",
        "#c8841a"
      ],
      "depth": "Strong foreground-background separation",
      "texture": "Subtle atmospheric depth",
      "avoid": [
        "Flat solid black",
        "Overpowering neon",
        "Busy circuit-board patterns"
      ]
    },
    "layout": "Three-layer cinematic selection reveal",
    "primary_region": {
      "bbox": [
        180,
        200,
        850,
        580
      ],
      "content": "One large selected portrait",
      "treatment": "Warm yellow edge illumination, realistic photographic depth, clear selection indicator"
    },
    "secondary_region": {
      "bbox": [
        70,
        590,
        980,
        990
      ],
      "content": "Large reaction portrait",
      "treatment": "Integrated cinematic portrait lighting, subtle warm rim, realistic contact shadows"
    },
    "supporting_region": {
      "bbox": [
        210,
        20,
        850,
        400
      ],
      "content": "Several smaller candidate headshots receding into the background",
      "treatment": "Perspective, depth of field and restrained illumination"
    },
    "graphics": [
      "One dominant selected portrait",
      "Four to six smaller candidate portraits",
      "One yellow selection indicator",
      "One subtle directional visual connecting the library to the selected image"
    ],
    "labels": [
      "106 HEADSHOTS",
      "AI PICK"
    ],
    "lighting": {
      "style": "Cinematic editorial",
      "key_light": "Soft neutral light on reaction portrait",
      "accent_light": "Warm yellow light around selected image",
      "background_light": "Subtle controlled highlights",
      "contrast": "High",
      "subject_separation": "Strong"
    },
    "focal_order": [
      "Selected photograph",
      "Reaction portrait",
      "Headline",
      "Background candidate photographs"
    ],
    "interaction": "Reaction portrait visibly looks toward the selected image"
  },
  "rendering": {
    "config_id": "rendering.thumbnail.v2",
    "mode": "cinematic_image_generation_plus_compositing",
    "generate_unified_scene": true,
    "allow_dark_cinematic_background": true,
    "use_reference_photographs": true,
    "prefer_original_face_when_compatible": true,
    "allow_reviewed_pose_generation": true,
    "render_selection_indicator_separately": true,
    "render_headline_separately": true,
    "generate_final_text_in_image": false,
    "avoid_checkerboard_backgrounds": true,
    "avoid_flat_cutout_compositing": true,
    "preserve_intermediate_assets": true
  },
  "text_layer": {
    "headline": "AI PICKED THIS",
    "alternates": [
      "WHICH ME?",
      "106 PHOTOS. ONE PICK.",
      "MY AI PHOTO PICKER"
    ],
    "render_mode": "post_composite",
    "font": "Bebas Neue",
    "weight": 400,
    "size_px": 88,
    "minimum_size_px": 64,
    "position": "Upper left",
    "bbox": [
      20,
      35,
      185,
      580
    ],
    "safe_margin_px": 48,
    "color": "#faf5ec",
    "accent": {
      "words": [
        "THIS"
      ],
      "color": "#ffde59"
    },
    "supporting_labels": {
      "enabled": false,
      "reason": "Avoid competing with the central selection story"
    }
  },
  "variations": {
    "count": 3,
    "strategies": [
      {
        "id": "selection_reveal",
        "description": "Large selected portrait emerging from smaller candidate images, with reaction portrait on the right"
      },
      {
        "id": "ai_decision",
        "description": "Strong visual emphasis on the chosen portrait and a restrained AI selection indicator"
      },
      {
        "id": "library_to_winner",
        "description": "A receding collection of headshots leads toward one dramatically illuminated selection"
      }
    ]
  },
  "quality_checks": [
    "Central story clearly communicates automated selection",
    "Selected portrait dominates candidate portraits",
    "Presenter identity remains recognizable",
    "Reaction and selected photograph interact visually",
    "Scene has coherent cinematic lighting",
    "No checkerboard transparency patterns",
    "No presentation-slide appearance",
    "Dark background creates useful contrast",
    "Yellow highlights direct attention",
    "No fabricated actual AI result",
    "Headline remains legible at 320x180",
    "Overall result resembles a finished professional thumbnail"
  ],
  "provenance": "ChatGPT board chat 2026-09-27, after test 1 was judged half done; fonts reconciled to Bebas Neue"
}
```