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
RUN NOTES FOR THIS CHAT
- Produce exactly ONE thumbnail: the spec below (d06.a1). Not a contact sheet, not variations.
- Attached files are the presenter-library cutouts. Match them by filename to `file_id` in the spec: headshot-appydave-58.png, headshot-appydave-29.png, headshot-appydave-86.png, headshot-appydave-20.png, headshot-appydave-30.png, headshot-appydave-33.png, headshot-appydave-13.png. Local paths in the JSON are for our records; use the attachments.
- Generate the image WITHOUT the headline (text_layer.render_mode = post_composite). Leave the headline region clean cream. The small tag chips on the face-wall cards ARE part of the image.
- After the image, give a short QC report against the spec's quality_checks.

BRAND CONFIG
```json
{
  "id": "brand.appydave.light.v1",
  "name": "AppyDave",
  "version": "1.0",
  "mode": "light_only",
  "colors": {
    "canvas": "#faf5ec",
    "text": "#342d2d",
    "accent": "#ffde59",
    "secondary": "#c8841a",
    "supporting_neutral": "#e8e0d4",
    "problem": "#d94b40",
    "success": "#268f83"
  },
  "color_semantics": {
    "yellow": "Highlights, arrows, calls to action and emphasis",
    "brown": "Headlines, outlines and primary labels",
    "amber": "Secondary emphasis and warm lighting",
    "red": "Problems, warnings and clipped audio",
    "teal": "Successful processing and clean results"
  },
  "background": {
    "required_base": "#faf5ec",
    "allow_subtle_texture": true,
    "allow_warm_gradient": true,
    "allow_full_dark_background": false,
    "allow_dark_vignette": false,
    "allow_dark_photo_background": false,
    "dark_regions": {
      "permitted": [
        "Contained software interfaces",
        "Waveform panels",
        "Small diagram elements",
        "Text and outlines",
        "Subtle contact shadows"
      ],
      "maximum_canvas_coverage_percent": 25,
      "must_be_visually_contained": true
    }
  },
  "visual_style": {
    "personality": [
      "Warm",
      "Practical",
      "Curious",
      "Hands-on builder",
      "Technically sophisticated"
    ],
    "photography": "Natural editorial photography",
    "graphics": "Clean editorial technology design",
    "lighting": "Soft neutral key light with optional warm rim",
    "complexity": "Low to medium",
    "avoid": [
      "Full-screen dark cinematic backgrounds",
      "Generic science-fiction imagery",
      "Unnecessary neon effects",
      "Excessive glow",
      "Decorative clutter",
      "Artificial facial exaggeration"
    ]
  },
  "typography": {
    "primary_font": "Bebas Neue",
    "fallback_font": "Oswald",
    "headline_weight": 400,
    "label_weight": 700,
    "headline_case": "uppercase",
    "headline_color": "#342d2d",
    "minimum_headline_size_px": 64,
    "preferred_headline_size_px": 88,
    "minimum_label_size_px": 28,
    "headline_font": "Bebas Neue",
    "label_font": "Oswald",
    "note": "Bebas Neue is single-weight; Oswald for labels, tags, ghost words. Source: brand-dave:brand (ChatGPT proposed Inter, overridden)."
  },
  "layout": {
    "aspect_ratio": "16:9",
    "width": 1280,
    "height": 720,
    "outer_safe_margin_px": 48,
    "maximum_primary_focal_points": 2,
    "maximum_headline_lines": 3,
    "maximum_headline_words": 6
  },
  "identity": {
    "preserve_presenter_identity": true,
    "prefer_original_photo_compositing": true,
    "allow_generated_pose_variations": true,
    "require_identity_review_for_generated_faces": true
  },
  "text_policy": {
    "default_render_mode": "post_composite",
    "allow_model_generated_final_headline": false,
    "allow_authentic_ui_text_in_screenshots": true,
    "allow_model_generated_decorative_text": false
  },
  "source": "ChatGPT extraction 2026-09-27, palette + fonts reconciled with brand-dave:brand skill"
}
```

PRESENTER LIBRARY
```json
{
  "id": "presenter.appydave.v1",
  "display_name": "AppyDave",
  "library": {
    "location": "Headshot Picker artefact (from portraits-rsch): https://claude.ai/artifact/EZbkmPK3zb8Vfi7u5soeQF",
    "root": "<PORTRAIT_LIBRARY_ROOT>",
    "manifest": "<PORTRAIT_LIBRARY_ROOT>/manifest.json",
    "interim_fallback_root": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/",
    "interim_fallback_manifest": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/headshots-manifest.json",
    "fallback_note": "T7 is an external drive; a missing path means unmounted, not deleted",
    "asset_resolution_required": true,
    "manifest_url": "https://claude.ai/artifact/EZbkmPK3zb8Vfi7u5soeQF (manifest.json, agents.md; favourites in db collection 'prefs')",
    "manifest_local": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/headshots-manifest.json",
    "id_scheme": "cid cN == file headshot-appydave-N.png (stable)",
    "private": "Shared 'anyone with the link' (view only). A plain script fetch gets Cloudflare's bot check (HTTP 403, 2026-09-27); whether ChatGPT's browsing can read it is untested. Image generation needs the PNGs attached regardless, so attach them from cutout.path."
  },
  "identity_policy": {
    "preserve_face": true,
    "preserve_glasses": true,
    "preserve_natural_age": true,
    "preserve_hairstyle": true,
    "do_not_beautify": true,
    "do_not_reinvent_facial_structure": true,
    "prefer_original_cutout": true
  },
  "portraits": {
    "surprised": {
      "path": "<PORTRAIT_LIBRARY_ROOT>/headshot-appydave-23.png",
      "file_id": "headshot-appydave-23.png",
      "status": "provided",
      "expression": "Wide eyes, open mouth",
      "clothing": "Light blue shirt",
      "framing": "Upper body",
      "suitable_for": [
        "Unexpected results",
        "Discovery",
        "Warnings",
        "Product demonstrations"
      ],
      "interim_path": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-23.png"
    },
    "confident": {
      "path": "<PORTRAIT_LIBRARY_ROOT>/headshot-appydave-15.png",
      "file_id": "headshot-appydave-15.png",
      "status": "provided",
      "expression": "Friendly smile",
      "clothing": "Light blue shirt",
      "framing": "Standing, approximately three-quarter body",
      "pose": "One hand on hip",
      "interim_path": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-15.png"
    },
    "thinking": {
      "path": "<PORTRAIT_LIBRARY_ROOT>/headshot-appydave-103.png",
      "file_id": "headshot-appydave-103.png",
      "status": "provided",
      "expression": "Restrained, conversational smile",
      "clothing": "Dark shirt",
      "framing": "Upper body",
      "note": "Thinking gesture is not present in the original",
      "interim_path": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-103.png"
    },
    "outdoor": {
      "path": "<PORTRAIT_LIBRARY_ROOT>/david-3-elephant.jpg",
      "file_id": "david-3-elephant.jpg",
      "status": "provided",
      "expression": "Natural conversational expression",
      "framing": "Close selfie",
      "environment": "Elephant sanctuary",
      "interim_path": "/Users/davidcruwys/dev/ad/flivideo/docs/briefs/thumb-research-2026-09-26/david-3-elephant.jpg"
    },
    "pointing_left": {
      "path": null,
      "file_id": null,
      "status": "missing",
      "required_pose": "Presenter pointing toward the left"
    },
    "pointing_right": {
      "path": null,
      "file_id": null,
      "status": "missing",
      "required_pose": "Presenter pointing toward the right"
    },
    "concerned": {
      "path": null,
      "file_id": null,
      "status": "missing"
    },
    "listening": {
      "path": null,
      "file_id": null,
      "status": "missing",
      "required_pose": "Presenter cupping one ear"
    }
  },
  "fallback_policy": {
    "missing_gesture": "Use an approved portrait and composite without changing the gesture, or generate a proposed variation for identity review",
    "missing_expression": "Select the closest available natural expression",
    "missing_file": "Report missing asset; do not substitute another person"
  }
}
```

RENDERING CONFIG
```json
{
  "id": "rendering.thumbnail.v1",
  "canvas": {
    "width": 1280,
    "height": 720,
    "aspect_ratio": "16:9",
    "coordinate_system": "normalized_1000",
    "bbox_order": [
      "top",
      "left",
      "bottom",
      "right"
    ]
  },
  "generation": {
    "generate_one_thumbnail_per_job": true,
    "contact_sheet_is_preview_only": true,
    "generate_background_separately_when_useful": true,
    "prefer_compositing_authentic_assets": true,
    "allow_generated_supporting_graphics": true
  },
  "text_layer_defaults": {
    "render_mode": "post_composite",
    "font_family": "Bebas Neue",
    "font_fallback": "Oswald",
    "font_weight": 400,
    "text_color": "#342d2d",
    "preferred_font_size_px": 88,
    "minimum_font_size_px": 64,
    "minimum_label_size_px": 28,
    "maximum_lines": 3,
    "maximum_words": 6,
    "safe_margin_px": 48,
    "mobile_preview": {
      "width": 320,
      "height": 180,
      "headline_must_remain_legible": true,
      "reduce_word_count_before_font_size": true
    }
  },
  "quality_checks": {
    "required": [
      "identity_preservation",
      "factual_accuracy",
      "light_mode_compliance",
      "composition",
      "text_accuracy",
      "mobile_readability",
      "asset_provenance"
    ],
    "manual_review": [
      "Final creative approval",
      "Generated facial variations",
      "Unverified product representations"
    ]
  }
}
```

TEXT-LAYER CONTRACT
```json
{
  "id": "text_layer.contract.v1",
  "version": "1.0",
  "default": {
    "render_mode": "post_composite",
    "reason": "Exact spelling, consistent typography, editable headlines and predictable layout",
    "font_family": "Bebas Neue",
    "font_fallback": "Oswald",
    "font_weight": 400,
    "text_transform": "uppercase",
    "text_color": "#342d2d",
    "preferred_font_size_px": 88,
    "minimum_font_size_px": 64,
    "minimum_label_size_px": 28,
    "maximum_headline_words": 6,
    "maximum_headline_lines": 3,
    "safe_margin_px": 48,
    "mobile_preview": {
      "width": 320,
      "height": 180,
      "require_legibility": true
    }
  },
  "fields": {
    "headline": "Primary thumbnail headline",
    "alternates": "Alternative headlines for selection or testing",
    "render_mode": "post_composite or model_generated",
    "font": "Font family",
    "weight": "Numeric font weight",
    "size_px": "Target headline font size",
    "minimum_size_px": "Minimum permitted headline font size",
    "position": "Human-readable placement instruction",
    "bbox": "Normalized text region [top,left,bottom,right]",
    "safe_margin_px": "Minimum distance from canvas edges",
    "color": "Headline color",
    "labels": "Supporting labels rendered separately",
    "callout": "Optional explanatory annotation"
  },
  "exceptions": {
    "authentic_screenshot_text": "Preserve text already present in authentic screenshots",
    "model_generated_text": "Only permit for experimental designs; not final production headlines",
    "tiny_interface_text": "May be simplified or omitted if illegible"
  },
  "validation": {
    "headline_fits_bbox": true,
    "headline_does_not_cover_hero": true,
    "headline_does_not_cover_critical_ui": true,
    "spelling_verified": true,
    "mobile_preview_checked": true,
    "reduce_words_before_reducing_font_size": true
  }
}
```

RECIPE
```json
{
  "id": "creator_ecosystem",
  "layout_family": "creator_showcase",
  "story_shape": "One creator introduces a collection of interconnected tools or capabilities",
  "layout": "Large presenter on one side; organized collection of product tiles on the other",
  "presenter_role": "Surprised, confident or pointing",
  "required_assets": [
    "Approved presenter portrait",
    "Product logos or screenshots"
  ],
  "typical_graphics": [
    "Application tiles",
    "Small icons",
    "Connecting arrows",
    "Simplified production timeline"
  ],
  "lighting": "Warm editorial portrait lighting",
  "background": "Light brand canvas",
  "when_not_to_use": [
    "Single-feature demonstrations",
    "Videos without a genuine collection of tools",
    "Topics where application tiles would become illegible"
  ],
  "related_recipes": [
    "creator_interface"
  ]
}
```

THUMBNAIL SPEC
```json
{
  "id": "d06.a1",
  "version": "1.0",
  "video": {
    "id": "D06",
    "brand_id": "brand.appydave.light.v1",
    "topic": "Tagging my headshots into an AI-readable picker",
    "working_title": "I Turned My Headshots Into an AI Picker",
    "audience": "Creators who use their own face in thumbnails",
    "promise": "Your headshots become a library you and your AI can pick from by expression, gaze and framing",
    "fact_sheet": "/Users/davidcruwys/dev/ad/flivideo/docs/briefs/thumbnail-system/videos/d06/d06-factsheet.md"
  },
  "creative": {
    "recipe": "creator_ecosystem",
    "story": "One creator, dozens of his own faces, all tagged and ready for AI",
    "hero": "Presenter, shocked",
    "secondary_hero": "Wall of his own tagged headshot cutouts",
    "emotion": "Surprise and amusement",
    "visual_metaphor": "Creator confronting a wall of himself",
    "style": "Warm editorial photography on a cream canvas"
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "portrait_role": "shocked",
    "file_id": "headshot-appydave-58.png",
    "cid": "c58",
    "interim_path": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-58.png",
    "expression": "Shocked, mouth open",
    "pose": "Hands on cheeks",
    "gesture_status": "Exists in the library as-is; composite the original cutout, do not regenerate the face",
    "framing": "Head and shoulders, large",
    "position": "Right",
    "bbox": [
      80,
      600,
      1000,
      990
    ],
    "lighting": "Soft frontal portrait light with restrained warm rim",
    "identity_policy": "Preserve original face and glasses"
  },
  "assets": {
    "required": [
      {
        "id": "presenter",
        "source": "portrait_library",
        "cid": "c58",
        "status": "provided"
      },
      {
        "id": "face_wall",
        "source": "portrait_library",
        "status": "provided",
        "items": [
          {
            "cid": "c29",
            "file_id": "headshot-appydave-29.png",
            "interim_path": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-29.png",
            "tag": "GRIN"
          },
          {
            "cid": "c86",
            "file_id": "headshot-appydave-86.png",
            "interim_path": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-86.png",
            "tag": "THINKING"
          },
          {
            "cid": "c20",
            "file_id": "headshot-appydave-20.png",
            "interim_path": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-20.png",
            "tag": "SKEPTICAL"
          },
          {
            "cid": "c30",
            "file_id": "headshot-appydave-30.png",
            "interim_path": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-30.png",
            "tag": "SURPRISED"
          },
          {
            "cid": "c33",
            "file_id": "headshot-appydave-33.png",
            "interim_path": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-33.png",
            "tag": "CONCERNED"
          },
          {
            "cid": "c13",
            "file_id": "headshot-appydave-13.png",
            "interim_path": "/Volumes/T7/Sync/david-profile/ash-dave-2024-headshots/jpg-transparent/headshot-appydave-13.png",
            "tag": "CONFIDENT"
          }
        ]
      }
    ],
    "optional": [],
    "asset_requirements": {
      "invent_extra_faces": false,
      "wall_uses_only_supplied_cutouts": true
    }
  },
  "composition": {
    "canvas": [
      1280,
      720
    ],
    "background": "Cream #faf5ec editorial canvas, subtle paper texture",
    "layout": "Two-column: face wall left, hero presenter right",
    "primary_region": {
      "bbox": [
        80,
        600,
        1000,
        990
      ],
      "content": "Large shocked presenter cutout"
    },
    "secondary_region": {
      "bbox": [
        220,
        40,
        960,
        570
      ],
      "content": "3x2 grid of small cutouts on light checkerboard cards, each with a brown tag chip"
    },
    "supporting_region": {
      "bbox": [
        40,
        40,
        200,
        570
      ],
      "content": "Headline area"
    },
    "graphics": [
      "Six rounded cards with light checkerboard behind each cutout",
      "Brown #342d2d tag chips with cream text (Oswald 700)",
      "One yellow highlight on the SURPRISED card"
    ],
    "labels": [
      "GRIN",
      "THINKING",
      "SKEPTICAL",
      "SURPRISED",
      "CONCERNED",
      "CONFIDENT"
    ],
    "lighting": "Even warm studio light",
    "focal_order": [
      "Presenter face",
      "Face wall",
      "Headline"
    ]
  },
  "rendering": {
    "config_id": "rendering.thumbnail.v1",
    "generate_background": true,
    "composite_presenter": true,
    "generate_final_text_in_image": false,
    "force_light_mode": true,
    "mode": "compositing_first",
    "composite_authentic_assets": true,
    "maximum_major_elements": 3
  },
  "text_layer": {
    "headline": "WHICH ME?",
    "alternates": [
      "106 FACES",
      "AI PICKS MY FACE"
    ],
    "render_mode": "post_composite",
    "font": "Bebas Neue",
    "weight": 400,
    "size_px": 88,
    "minimum_size_px": 64,
    "position": "Top left, above the face wall",
    "bbox": [
      40,
      40,
      200,
      570
    ],
    "safe_margin_px": 48,
    "color": "#342d2d",
    "highlight": {
      "word_background": "#ffde59",
      "applies_to": "one key word"
    }
  },
  "variations": {
    "count": 3,
    "strategies": [
      "3x2 wall left, presenter right",
      "Presenter centre, cards fanned around him",
      "Wall fills background at low contrast, presenter foreground"
    ]
  },
  "quality_checks": [
    "Presenter identity preserved (original cutout, not a regenerated face)",
    "Light-mode compliance: cream canvas, dark areas contained and under 25%",
    "Headline composited afterwards, spelled correctly, legible at 320x180",
    "Headline does not cover the hero face",
    "No invented UI: any picker imagery is the supplied screenshot or clearly illustrative",
    "Tag chips match each cutout's manifest expression",
    "Wall faces all come from the supplied cutouts"
  ]
}
```