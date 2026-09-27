# ChatGPT method extraction — reply to the 2026-09-27 request (current_node chain)

Conversation: https://chatgpt.com/c/6ab76474-f070-83ec-ba92-902ae2179e79

<!-- user 2026-09-27T03:00:38.713Z -->

Please do NOT generate any images in this reply. Text and JSON only.

The nine-concept board is the quality bar, but right now it can't be reproduced: it came from one short prose prompt that leaned on this chat's history. I want to turn it into a system I can run again in a fresh chat with no history. Please give me the following, as JSON code blocks where it's JSON:

(a) NINE FILLED SPECS. One complete JSON spec for each concept on the board, using the schema you proposed (video, creative recipe, assets, composition, rendering, variations, quality_checks) plus the new sections below: d01 A1 Cinematic creator, A2 Creator + interface, A3 Visual transformation; d02 A1 Noisy room to clean audio, A2 Cutty agent workflow, A3 Clipped word detection; d03 A1 Tracking quadrants, A2 Works in any language, A3 Agent places graphics. Fill in every field with what actually made that tile work: presenter pose/expression and which portrait role, framing and side, props, UI elements, labels, lighting, background. Each spec must be self-contained enough to paste into a fresh chat with only its listed assets attached.

(b) RECIPES. Name the nine concepts as reusable recipes (e.g. "cinematic_creator", "before_after_waveform"), each written generically with no video-specific details: what story shape it suits, layout, presenter role, required assets, typical graphics, and when not to use it. If two tiles are really the same recipe, say so.

(c) TEXT LAYER. Add an explicit "text_layer" section to the schema: headline wording (and alternates), whether the text is rendered inside the image by the model or overlaid afterwards by a compositor (recommend a default and say why), font/weight, position, safe area, and a minimum text size rule for readability at small YouTube sizes.

(d) BRAND CONFIG. A separate "brand" block for AppyDave that the specs reference by id rather than repeat. Force LIGHT MODE: cream #faf5ec background, brown #342d2d text, yellow #ffde59 accent/CTA, amber #c8841a secondary. The board wrongly used dark backgrounds in several tiles; the brand block should forbid that and say how dark areas may be used, if at all (small accents only).

(e) PRESENTER SEED. A "presenter" slot that points at an external portrait library (by portrait role, e.g. surprised / thinking / confident / pointing-left, plus an optional file id) instead of photos uploaded into the chat. Library location is TBD, so use a placeholder path.

Finally, give me the updated universal schema on its own (all sections, with a one-line description per field), so I can keep it as the template.

<!-- assistant 2026-09-27T03:00:40.991Z -->

# AppyDave Thumbnail Director — Reproducible Specification v1.0

This is a portable specification designed to work in a fresh chat without relying on conversation history.

It contains a separate brand configuration, an external portrait-library contract, nine filled thumbnail specifications, a reusable recipe catalogue, text-rendering rules and a universal template.

Three important distinctions:

- **Observed:** The nine concepts, their compositions and their visual elements come from the generated contact sheet and your D01–D03 fact sheets.
- **Specified:** Exact coordinates, font sizes, asset filenames and some lighting instructions are new production decisions intended to reproduce those concepts. They weren't recorded in the original generation.
- **Not guaranteed:** The original board was generated as one image. The specifications below are designed to reproduce its creative direction as nine independent thumbnails, not guarantee pixel-identical outputs.

The D01 video is still unfinished, D02's existing launch material is unapproved, and D03 doesn't yet have a launch pack. Consequently, all thumbnail headlines below are proposals rather than approved publishing copy. <FileCite ref="turn0file0" line_range_start={3} line_range_end={9}/> <FileCite ref="turn0file1" line_range_start={1} line_range_end={9}/> <FileCite ref="turn0file2" line_range_start={1} line_range_end={9}/>

All nine specifications use 1280 × 720 pixels. Their normalized bounding boxes follow the convention `[top, left, bottom, right]`, with coordinates ranging from 0 to 1000.

---

# A. Shared configuration

These configuration objects should be supplied alongside the individual thumbnail specifications. This avoids repeating brand rules and portrait-library settings nine times.

## A1. Brand configuration

The original board used dark backgrounds to create contrast. Your explicit production requirement overrides that treatment: every finished thumbnail must use a light-mode composition.

Dark software panels, dark waveform displays and small shadows are permitted as supporting objects. A dark photographic environment must not become the dominant background.

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
    "primary_font": "Inter",
    "fallback_font": "Arial",
    "headline_weight": 900,
    "label_weight": 700,
    "headline_case": "uppercase",
    "headline_color": "#342d2d",
    "minimum_headline_size_px": 64,
    "preferred_headline_size_px": 88,
    "minimum_label_size_px": 28
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
  }
}
```

The red and teal colors are proposed supporting tokens, derived from D02's documented problem/control convention. They are not replacements for the four primary brand colors. <FileCite ref="turn0file1" line_range_start={42} line_range_end={58}/>

The 25% dark-area limit is a proposed production constraint, not a measured property of the original board.

## A2. Presenter library

The presenter library is an external asset dependency. A new conversation should receive the library manifest and only the photographs required by the selected thumbnail specification.

An image model cannot necessarily open a local or cloud path by itself. The production system must resolve the manifest's asset paths into actual image attachments or accessible image inputs.

```json
{
  "id": "presenter.appydave.v1",
  "display_name": "AppyDave",
  "library": {
    "root": "<PORTRAIT_LIBRARY_ROOT>",
    "manifest": "<PORTRAIT_LIBRARY_ROOT>/manifest.json",
    "storage_provider": "TBD",
    "asset_resolution_required": true
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
      "file_id": null,
      "status": "provided",
      "expression": "Wide eyes, open mouth",
      "clothing": "Light blue shirt",
      "framing": "Upper body",
      "suitable_for": [
        "Unexpected results",
        "Discovery",
        "Warnings",
        "Product demonstrations"
      ]
    },
    "confident": {
      "path": "<PORTRAIT_LIBRARY_ROOT>/headshot-appydave-15.png",
      "file_id": null,
      "status": "provided",
      "expression": "Friendly smile",
      "clothing": "Light blue shirt",
      "framing": "Standing, approximately three-quarter body",
      "pose": "One hand on hip"
    },
    "thinking": {
      "path": "<PORTRAIT_LIBRARY_ROOT>/headshot-appydave-103.png",
      "file_id": null,
      "status": "provided",
      "expression": "Restrained, conversational smile",
      "clothing": "Dark shirt",
      "framing": "Upper body",
      "note": "Thinking gesture is not present in the original"
    },
    "outdoor": {
      "path": "<PORTRAIT_LIBRARY_ROOT>/david-3-elephant.jpg",
      "file_id": null,
      "status": "provided",
      "expression": "Natural conversational expression",
      "framing": "Close selfie",
      "environment": "Elephant sanctuary"
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

The supplied portraits establish your identity and clothing references. They do not include every gesture shown in the generated contact sheet.

In particular, pointing, hand-on-head and cupped-ear poses must be sourced separately or generated as variations and reviewed.

## A3. Global rendering and text rules

This block establishes the default production behavior for all nine specifications.

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
    "font_family": "Inter",
    "font_fallback": "Arial",
    "font_weight": 900,
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

**Text-layer recommendation:** generate the visual image without final headline text, then overlay the headline using a graphics compositor.

This provides exact spelling, predictable font sizes, editable copy and consistent typography. It also avoids having to regenerate the entire image when a video title changes.

The minimum 64-pixel headline size is a starting production rule. The final acceptance test is whether the headline remains legible in a 320 × 180 preview.



<!-- assistant 2026-09-27T03:01:05.401Z -->

---

# B. Nine filled thumbnail specifications

All nine reference the shared configuration above. Each specification contains its own video brief, creative instructions, presenter selection, assets, composition, rendering instructions, text layer, variations and quality checks.

The `asset_requirements` field distinguishes assets you already supplied from assets that still need to be captured or created. Where a specific screenshot isn't available, the specification describes a conceptual mockup and prohibits presenting it as authentic product footage.

## D01 — FliVideo tour

The D01 fact sheet describes a suite of creator tools, a shirt-change hook, the FliHub recording inbox, agent interaction, automatic screencast zooming and teleprompter functionality. These provide the visual foundation for the three concepts. <FileCite ref="turn0file0" line_range_start={20} line_range_end={38}/>

### D01 A1 — Cinematic creator

<badge>Recipe: creator_ecosystem</badge>

The hero is your surprised expression. The supporting image is a collection of applications you've built, arranged as a recognizable software ecosystem.

The contact sheet used a dark application-wall background. This specification converts it into cream-colored editorial artwork with contained dark application tiles.

```json
{
  "id": "d01.a1",
  "version": "1.0",
  "video": {
    "id": "D01",
    "brand_id": "brand.appydave.light.v1",
    "topic": "FliVideo creator automation tour",
    "working_title": "The Apps and Agents I Use to Automate My YouTube",
    "audience": "Human YouTubers and solo creators",
    "promise": "A suite of custom apps and agents automates the production work around a human presenter"
  },
  "creative": {
    "recipe": "creator_ecosystem",
    "story": "One human creator built an interconnected production system",
    "hero": "Presenter",
    "secondary_hero": "FliVideo application ecosystem",
    "emotion": "Surprise, curiosity and ownership",
    "visual_metaphor": "Creator revealing his collection of tools",
    "style": "Warm cinematic editorial technology",
    "reference_tile": "D01 A1"
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "portrait_role": "surprised",
    "file_id": null,
    "preferred_asset": "headshot-appydave-23.png",
    "expression": "Wide eyes and open mouth",
    "pose": "Upper body facing camera, optionally pointing toward the application wall",
    "gesture_status": "Pointing requires a new asset or reviewed variation",
    "framing": "Medium close-up",
    "position": "Right",
    "bbox": [60, 570, 970, 990],
    "lighting": "Soft frontal portrait light with restrained warm rim",
    "identity_policy": "Preserve original face and glasses"
  },
  "assets": {
    "required": [
      {
        "id": "presenter",
        "source": "portrait_library",
        "role": "surprised",
        "status": "provided"
      },
      {
        "id": "app_tiles",
        "source": "<VIDEO_ASSETS_ROOT>/D01/app-logos/",
        "status": "required",
        "items": [
          "FliStudio",
          "FliHub",
          "FliCast",
          "FliCut",
          "Teletubby",
          "Kyber Studio"
        ]
      }
    ],
    "optional": [
      "Approved FliVideo logo",
      "Authentic recording-timeline screenshot",
      "Approved agent icon"
    ],
    "asset_requirements": {
      "use_authentic_logos_when_available": true,
      "invent_product_logos": false,
      "mockup_policy": "Clearly mark conceptual UI as illustrative"
    }
  },
  "composition": {
    "canvas": [1280, 720],
    "background": "Cream editorial studio with subtle warm paper texture",
    "layout": "Two-column hero and ecosystem",
    "primary_region": {
      "bbox": [60, 570, 970, 990],
      "content": "Large presenter cutout"
    },
    "secondary_region": {
      "bbox": [100, 40, 740, 550],
      "content": "Six prominent application tiles in a structured grid"
    },
    "supporting_region": {
      "bbox": [760, 50, 920, 530],
      "content": "Small sequence of video frames connected by an amber arrow"
    },
    "graphics": [
      "Six application tiles",
      "Simple recording timeline",
      "One yellow directional arrow",
      "Subtle contact shadows"
    ],
    "labels": [
      "FliStudio",
      "FliHub",
      "FliCast",
      "FliCut",
      "Teletubby",
      "Kyber Studio"
    ],
    "lighting": "Warm editorial studio lighting",
    "focal_order": [
      "Presenter",
      "Application ecosystem",
      "Headline"
    ]
  },
  "rendering": {
    "config_id": "rendering.thumbnail.v1",
    "mode": "image_generation_plus_compositing",
    "generate_background": true,
    "composite_presenter": true,
    "composite_authentic_logos": true,
    "generate_final_text_in_image": false,
    "force_light_mode": true,
    "maximum_major_elements": 3
  },
  "text_layer": {
    "headline": "I BUILT ALL THIS",
    "alternates": [
      "MY AI VIDEO SYSTEM",
      "AUTOMATING MY YOUTUBE"
    ],
    "render_mode": "post_composite",
    "font": "Inter",
    "weight": 900,
    "size_px": 80,
    "minimum_size_px": 64,
    "position": "Upper left",
    "bbox": [20, 35, 170, 550],
    "safe_margin_px": 48,
    "color": "#342d2d",
    "label_policy": "Use authentic product names; render all labels with compositor"
  },
  "variations": {
    "count": 3,
    "strategies": [
      "Surprised portrait with application wall",
      "Confident portrait with simplified application wall",
      "Presenter with application tiles and production timeline"
    ]
  },
  "quality_checks": [
    "Presenter identity preserved",
    "Correct FliVideo application spelling",
    "Authentic logos or clearly illustrative tiles",
    "Light background",
    "Readable application hierarchy",
    "No unsupported claims about product capabilities",
    "Mobile-size readability"
  ]
}
```

### D01 A2 — Creator and interface

<badge>Recipe: creator_interface</badge>

This concept uses your face as the primary human element and a software interface as the evidence. The original board depicted an FliHub-style recording inbox with transcript indicators and video previews.

```json
{
  "id": "d01.a2",
  "version": "1.0",
  "video": {
    "id": "D01",
    "brand_id": "brand.appydave.light.v1",
    "topic": "FliVideo recording and automation",
    "working_title": "The Apps and Agents I Use to Automate My YouTube",
    "audience": "Creators who film themselves",
    "promise": "Show how custom applications and agents organize recording, transcripts and editing"
  },
  "creative": {
    "recipe": "creator_interface",
    "story": "The presenter demonstrates the system he built",
    "hero": "Presenter",
    "secondary_hero": "FliHub recording interface",
    "emotion": "Confidence and thoughtful curiosity",
    "visual_metaphor": "Human creator in control of software",
    "style": "Premium editorial software photography",
    "reference_tile": "D01 A2"
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "portrait_role": "thinking",
    "file_id": null,
    "preferred_asset": "headshot-appydave-103.png",
    "expression": "Thoughtful and approachable",
    "pose": "Hand near chin",
    "gesture_status": "Thinking gesture requires a reviewed variation",
    "framing": "Medium close-up",
    "position": "Right foreground",
    "bbox": [100, 520, 960, 980],
    "lighting": "Soft neutral frontal light with subtle warm edge"
  },
  "assets": {
    "required": [
      {
        "id": "presenter",
        "source": "portrait_library",
        "role": "thinking",
        "status": "provided_without_requested_gesture"
      },
      {
        "id": "interface",
        "source": "<VIDEO_ASSETS_ROOT>/D01/flithub-inbox.png",
        "status": "required"
      }
    ],
    "optional": [
      "Authentic video-preview frame",
      "Transcript-status screenshot",
      "Recording waveform"
    ],
    "asset_requirements": {
      "preserve_interface_structure": true,
      "preserve_real_product_identity": true,
      "do_not_fabricate_real_recording_data": true
    }
  },
  "composition": {
    "canvas": [1280, 720],
    "background": "Cream studio with a large contained software window",
    "layout": "Interface left and center, presenter right",
    "primary_region": {
      "bbox": [100, 520, 960, 980],
      "content": "Presenter foreground"
    },
    "secondary_region": {
      "bbox": [120, 30, 860, 710],
      "content": "Authentic FliHub inbox interface"
    },
    "graphics": [
      "Recording list",
      "Video preview",
      "Transcript status indicators",
      "Small waveform"
    ],
    "labels": [
      "FliHub",
      "Transcript"
    ],
    "lighting": "Natural portrait lighting with subtle UI highlights",
    "focal_order": [
      "Presenter",
      "Transcript indicators",
      "Software interface"
    ],
    "depth": "Presenter overlaps contained interface slightly"
  },
  "rendering": {
    "config_id": "rendering.thumbnail.v1",
    "mode": "authentic_interface_composite",
    "generate_background": true,
    "composite_presenter": true,
    "composite_interface": true,
    "generate_final_text_in_image": false,
    "force_light_mode": true
  },
  "text_layer": {
    "headline": "MY AI VIDEO SYSTEM",
    "alternates": [
      "I BUILT MY OWN TOOLS",
      "AUTOMATED YOUTUBE"
    ],
    "render_mode": "post_composite",
    "font": "Inter",
    "weight": 900,
    "size_px": 76,
    "minimum_size_px": 64,
    "position": "Upper left",
    "bbox": [20, 35, 190, 490],
    "safe_margin_px": 48,
    "color": "#342d2d",
    "label_policy": "Preserve authentic interface labels"
  },
  "variations": {
    "count": 3,
    "strategies": [
      "Presenter foreground with recording inbox",
      "Presenter beside transcript-status indicators",
      "Presenter with recording inbox and enlarged video preview"
    ]
  },
  "quality_checks": [
    "Presenter identity preserved",
    "Software interface accurately represented",
    "Transcript status indicators visible",
    "No invented recording metadata",
    "Headline does not cover important UI",
    "Cream remains dominant background",
    "Readable at mobile size"
  ]
}
```

### D01 A3 — Visual transformation

<badge>Recipe: creator_transformation</badge>

This is the before-and-after story. The original board showed a stressed creator surrounded by equipment and paperwork, transitioning into an enthusiastic creator with a simplified automated production system.

It is a conceptual interpretation of the video's automation premise, not documentary evidence of a literal before-and-after event.

```json
{
  "id": "d01.a3",
  "version": "1.0",
  "video": {
    "id": "D01",
    "brand_id": "brand.appydave.light.v1",
    "topic": "Automating human YouTube production",
    "working_title": "The Apps and Agents I Use to Automate My YouTube",
    "audience": "Creators overwhelmed by production work",
    "promise": "Custom tools can simplify the work surrounding human video creation"
  },
  "creative": {
    "recipe": "creator_transformation",
    "story": "Production chaos becomes an organized automated workflow",
    "hero": "Before-and-after presenter",
    "secondary_hero": "Production equipment and software",
    "emotion": "Frustration changing to enthusiasm",
    "visual_metaphor": "Complexity transformed into simplicity",
    "style": "Warm editorial before-and-after photography",
    "reference_tile": "D01 A3"
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "portrait_role": "surprised",
    "file_id": null,
    "preferred_asset": "headshot-appydave-23.png",
    "expression": "Left: concerned or overwhelmed; right: enthusiastic",
    "pose": "Left: hand near head; right: pointing toward software",
    "gesture_status": "Both gestures require reviewed variations",
    "framing": "Two matched medium close-ups",
    "position": "Left and right",
    "bbox": [90, 40, 950, 420],
    "lighting": "Soft neutral lighting on both sides"
  },
  "assets": {
    "required": [
      {
        "id": "presenter",
        "source": "portrait_library",
        "role": "surprised",
        "status": "provided"
      },
      {
        "id": "software",
        "source": "<VIDEO_ASSETS_ROOT>/D01/approved-software-screenshot.png",
        "status": "required"
      }
    ],
    "optional": [
      "Camera",
      "Microphone",
      "Recording checklist",
      "Editing timeline"
    ],
    "asset_requirements": {
      "before_scene_may_be_illustrative": true,
      "after_scene_uses_authentic_software": true,
      "avoid_unverified_performance_claims": true
    }
  },
  "composition": {
    "canvas": [1280, 720],
    "background": "Cream editorial background",
    "layout": "Left-to-right transformation",
    "primary_region": {
      "bbox": [130, 30, 930, 430],
      "content": "Before: presenter with recording equipment and paperwork"
    },
    "secondary_region": {
      "bbox": [130, 590, 930, 970],
      "content": "After: presenter with simplified software workflow"
    },
    "transition_region": {
      "bbox": [400, 420, 620, 590],
      "content": "Large yellow directional arrow"
    },
    "graphics": [
      "Camera",
      "Microphone",
      "Production checklist",
      "Contained software interface",
      "Yellow transformation arrow"
    ],
    "labels": [
      "BEFORE",
      "AFTER"
    ],
    "lighting": "Warm consistent lighting across both scenes",
    "focal_order": [
      "Two presenter expressions",
      "Transformation arrow",
      "Production equipment and software"
    ]
  },
  "rendering": {
    "config_id": "rendering.thumbnail.v1",
    "mode": "two_scene_composite",
    "generate_background": true,
    "composite_presenter": true,
    "composite_authentic_software": true,
    "generate_final_text_in_image": false,
    "force_light_mode": true
  },
  "text_layer": {
    "headline": "FROM CHAOS TO CONTROL",
    "alternates": [
      "I AUTOMATED MYSELF",
      "LESS EDITING. MORE VIDEOS."
    ],
    "render_mode": "post_composite",
    "font": "Inter",
    "weight": 900,
    "size_px": 72,
    "minimum_size_px": 64,
    "position": "Upper center",
    "bbox": [20, 70, 160, 930],
    "safe_margin_px": 48,
    "color": "#342d2d",
    "labels": [
      "BEFORE",
      "AFTER"
    ]
  },
  "variations": {
    "count": 3,
    "strategies": [
      "Two contrasting presenter expressions",
      "Equipment chaos versus clean workflow",
      "Production checklist versus automated software"
    ]
  },
  "quality_checks": [
    "Both presenter images remain recognizable",
    "Before-and-after relationship immediately understandable",
    "Transformation is presented as conceptual",
    "Software imagery accurately represented",
    "Light-mode background",
    "Directional arrow visible",
    "Mobile readability"
  ]
}
```



<!-- assistant 2026-09-27T03:01:35.297Z -->

---

## D02 — Cutty audio cleanup

D02 has three particularly useful visual subjects: the noisy recording environment, the audio-processing pipeline and the clipped-word warning. These are all documented in its fact sheet. The existing launch pack also proposed three corresponding headline directions, but none has been approved. <FileCite ref="turn0file1" line_range_start={20} line_range_end={34}/> <FileCite ref="turn0file1" line_range_start={42} line_range_end={58}/>

### D02 A1 — Noisy room to clean audio

<badge>Recipe: diagnostic_transformation</badge>

The board's strongest element is the contrast between the physical source of the problem and three stacked waveform displays. Your surprised expression gives the technical diagram a human focal point.

```json
{
  "id": "d02.a1",
  "version": "1.0",
  "video": {
    "id": "D02",
    "brand_id": "brand.appydave.light.v1",
    "topic": "Cutty audio cleanup",
    "working_title": "I Built an AI Agent That Cleans My Audio",
    "audience": "Creators recording in noisy environments",
    "promise": "Compare audio cleanup profiles and reduce unwanted noise"
  },
  "creative": {
    "recipe": "diagnostic_transformation",
    "story": "Noisy recording becomes cleaner audio",
    "hero": "Presenter reacting to recording noise",
    "secondary_hero": "Three waveform profiles",
    "emotion": "Surprise and discovery",
    "visual_metaphor": "Visible noise reduction",
    "style": "Editorial technical demonstration",
    "reference_tile": "D02 A1"
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "portrait_role": "surprised",
    "file_id": null,
    "preferred_asset": "headshot-appydave-23.png",
    "expression": "Wide-eyed, reacting to the problem",
    "pose": "One finger near lips",
    "gesture_status": "Requires reviewed variation",
    "framing": "Medium close-up",
    "position": "Left",
    "bbox": [180, 30, 970, 510],
    "lighting": "Soft natural studio light with warm edge"
  },
  "assets": {
    "required": [
      {
        "id": "presenter",
        "source": "portrait_library",
        "role": "surprised",
        "status": "provided"
      },
      {
        "id": "waveforms",
        "source": "<VIDEO_ASSETS_ROOT>/D02/audio-profile-waveforms/",
        "status": "required",
        "preferred": "Authentic comparison profiles"
      }
    ],
    "optional": [
      "Fan photograph",
      "Air-conditioner photograph",
      "DeepFilterNet label"
    ],
    "asset_requirements": {
      "authentic_waveforms_preferred": true,
      "synthetic_waveforms_must_be_illustrative": true,
      "do_not_invent_measured_improvement": true
    }
  },
  "composition": {
    "canvas": [1280, 720],
    "background": "Cream recording-room illustration with subtle fan and air-conditioner",
    "layout": "Presenter left, waveform comparison right",
    "primary_region": {
      "bbox": [170, 20, 970, 520],
      "content": "Large presenter reacting to noisy recording"
    },
    "secondary_region": {
      "bbox": [160, 530, 900, 960],
      "content": "Three vertically stacked waveform panels"
    },
    "graphics": [
      "Contained fan",
      "Air-conditioner",
      "Raw red waveform",
      "Levelled amber waveform",
      "Denoised teal waveform"
    ],
    "labels": [
      "RAW",
      "LEVELLED",
      "DENOISED"
    ],
    "lighting": "Soft warm room lighting",
    "focal_order": [
      "Presenter",
      "Waveform comparison",
      "Noise sources"
    ]
  },
  "rendering": {
    "config_id": "rendering.thumbnail.v1",
    "mode": "portrait_and_waveform_composite",
    "generate_background": true,
    "composite_presenter": true,
    "render_waveforms_deterministically": true,
    "generate_final_text_in_image": false,
    "force_light_mode": true
  },
  "text_layer": {
    "headline": "FANS ON. STILL CLEAN.",
    "alternates": [
      "CLEAN AUDIO. NO STUDIO.",
      "I FIXED MY AUDIO"
    ],
    "render_mode": "post_composite",
    "font": "Inter",
    "weight": 900,
    "size_px": 72,
    "minimum_size_px": 64,
    "position": "Upper left",
    "bbox": [20, 35, 170, 920],
    "safe_margin_px": 48,
    "color": "#342d2d",
    "labels": [
      "RAW",
      "LEVELLED",
      "DENOISED"
    ]
  },
  "variations": {
    "count": 3,
    "strategies": [
      "Presenter with three waveform profiles",
      "Noisy room with prominent cleaned waveform",
      "Raw versus denoised waveform comparison"
    ]
  },
  "quality_checks": [
    "Presenter identity preserved",
    "Three profiles distinguishable",
    "Red indicates the problem",
    "Teal indicates the cleaned result",
    "Waveforms not represented as measured data unless authentic",
    "Dark panels occupy limited canvas area",
    "Headline readable at 320x180"
  ]
}
```

### D02 A2 — Cutty agent workflow

<badge>Recipe: agent_pipeline_hero</badge>

This is the only tile in the D02 row that doesn't depend on your face. It uses an approachable robot as a visual representation of Cutty, with a simplified audio-processing pipeline surrounding it.

The robot is an illustrative character, not an established Cutty character design. It should only become permanent branding after approval.

```json
{
  "id": "d02.a2",
  "version": "1.0",
  "video": {
    "id": "D02",
    "brand_id": "brand.appydave.light.v1",
    "topic": "Cutty audio-processing agent",
    "working_title": "I Built an AI Agent That Cleans My Audio",
    "audience": "Creators interested in automated editing",
    "promise": "Show how an agent coordinates several audio-processing operations"
  },
  "creative": {
    "recipe": "agent_pipeline_hero",
    "story": "One agent coordinates multiple audio-processing steps",
    "hero": "Illustrative Cutty robot",
    "secondary_hero": "Audio-processing pipeline",
    "emotion": "Friendly technical competence",
    "visual_metaphor": "An assistant managing an audio production line",
    "style": "Premium editorial product illustration",
    "reference_tile": "D02 A2"
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "portrait_role": null,
    "file_id": null,
    "visible": false,
    "reason": "Agent is the visual hero"
  },
  "assets": {
    "required": [
      {
        "id": "cutty_character",
        "source": "<BRAND_ASSETS_ROOT>/agents/cutty-approved.png",
        "status": "missing",
        "fallback": "Generate illustrative robot concept for approval"
      }
    ],
    "optional": [
      "FliCut logo",
      "Approved audio-processing icons",
      "Authentic processing diagram"
    ],
    "asset_requirements": {
      "agent_character_requires_approval": true,
      "do_not_claim_character_is_official_until_approved": true,
      "processing_steps_must_match_fact_sheet": true
    }
  },
  "composition": {
    "canvas": [1280, 720],
    "background": "Warm cream with subtle yellow circular accent",
    "layout": "Central robot with a horizontal processing flow",
    "primary_region": {
      "bbox": [160, 350, 800, 650],
      "content": "Friendly Cutty robot with small headphones"
    },
    "secondary_region": {
      "bbox": [300, 40, 650, 340],
      "content": "Input audio and processing stages"
    },
    "output_region": {
      "bbox": [300, 680, 650, 960],
      "content": "Clean output waveform"
    },
    "graphics": [
      "Input audio icon",
      "Separate audio",
      "Denoise",
      "Level",
      "Check clipped words",
      "Reattach",
      "Amber directional arrows",
      "Teal clean waveform"
    ],
    "labels": [
      "CUTTY",
      "DENOISE",
      "LEVEL",
      "CHECK WORDS"
    ],
    "lighting": "Soft studio product lighting",
    "focal_order": [
      "Cutty",
      "Audio input and output",
      "Processing steps"
    ]
  },
  "rendering": {
    "config_id": "rendering.thumbnail.v1",
    "mode": "illustration_plus_deterministic_diagram",
    "generate_background": true,
    "generate_agent_concept_if_missing": true,
    "render_diagram_separately": true,
    "generate_final_text_in_image": false,
    "force_light_mode": true
  },
  "text_layer": {
    "headline": "ONE AGENT. FOUR FIXES.",
    "alternates": [
      "MEET CUTTY",
      "MY AI AUDIO EDITOR"
    ],
    "render_mode": "post_composite",
    "font": "Inter",
    "weight": 900,
    "size_px": 76,
    "minimum_size_px": 64,
    "position": "Upper center",
    "bbox": [20, 100, 160, 900],
    "safe_margin_px": 48,
    "color": "#342d2d",
    "labels": [
      "CUTTY",
      "DENOISE",
      "LEVEL",
      "CHECK WORDS"
    ]
  },
  "variations": {
    "count": 3,
    "strategies": [
      "Robot centered between input and output",
      "Robot beside simplified processing flow",
      "Large clean waveform with smaller robot"
    ]
  },
  "quality_checks": [
    "Cutty character approved or clearly illustrative",
    "Processing operations factually supported",
    "Flow direction unambiguous",
    "No invented performance measurements",
    "Labels legible",
    "Cream background dominant",
    "Mobile readability"
  ]
}
```

### D02 A3 — Clipped word detection

<badge>Recipe: diagnostic_warning</badge>

This concept has an unusually strong visual metaphor: a red vertical marker interrupts a waveform, indicating a word that may have been clipped.

Your listening pose directs the viewer's attention toward the technical problem.

```json
{
  "id": "d02.a3",
  "version": "1.0",
  "video": {
    "id": "D02",
    "brand_id": "brand.appydave.light.v1",
    "topic": "Detecting potentially clipped words",
    "working_title": "I Built an AI Agent That Cleans My Audio",
    "audience": "Creators frustrated by automatic editing errors",
    "promise": "Show how Cutty identifies words that may have been clipped"
  },
  "creative": {
    "recipe": "diagnostic_warning",
    "story": "The agent catches an audio problem before it is missed",
    "hero": "Presenter listening",
    "secondary_hero": "Waveform with red warning marker",
    "emotion": "Concern and focused attention",
    "visual_metaphor": "An interrupted waveform",
    "style": "Clean technical editorial photography",
    "reference_tile": "D02 A3"
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "portrait_role": "listening",
    "file_id": null,
    "fallback_portrait_role": "thinking",
    "preferred_fallback_asset": "headshot-appydave-103.png",
    "expression": "Concerned and attentive",
    "pose": "One hand cupped around ear",
    "gesture_status": "Requires new photograph or reviewed variation",
    "framing": "Medium close-up",
    "position": "Left",
    "bbox": [130, 30, 960, 520],
    "lighting": "Neutral editorial portrait lighting"
  },
  "assets": {
    "required": [
      {
        "id": "presenter",
        "source": "portrait_library",
        "role": "listening",
        "status": "missing"
      },
      {
        "id": "waveform",
        "source": "<VIDEO_ASSETS_ROOT>/D02/clipped-word-example.png",
        "status": "required"
      }
    ],
    "optional": [
      "Authentic audio-profile screenshot",
      "Approved Cutty icon"
    ],
    "asset_requirements": {
      "red_marker_must_represent_potential_clipping": true,
      "do_not_claim_confirmed_clipping_without_evidence": true
    }
  },
  "composition": {
    "canvas": [1280, 720],
    "background": "Cream editorial background",
    "layout": "Listening presenter left, diagnostic comparison right",
    "primary_region": {
      "bbox": [130, 20, 960, 530],
      "content": "Presenter listening intently"
    },
    "secondary_region": {
      "bbox": [170, 550, 510, 970],
      "content": "Upper waveform with red clipping marker"
    },
    "supporting_region": {
      "bbox": [550, 550, 880, 970],
      "content": "Lower comparison waveform with teal confirmation icon"
    },
    "graphics": [
      "Red vertical warning marker",
      "Warning icon",
      "Two waveform panels",
      "Teal confirmation symbol"
    ],
    "labels": [
      "WORD MAY BE CLIPPED"
    ],
    "lighting": "Soft neutral studio lighting",
    "focal_order": [
      "Listening presenter",
      "Red warning marker",
      "Waveform comparison"
    ]
  },
  "rendering": {
    "config_id": "rendering.thumbnail.v1",
    "mode": "portrait_plus_diagnostic_composite",
    "generate_background": true,
    "composite_presenter": true,
    "render_waveforms_deterministically": true,
    "generate_final_text_in_image": false,
    "force_light_mode": true
  },
  "text_layer": {
    "headline": "IT ATE YOUR WORDS",
    "alternates": [
      "AI CUT MY WORDS",
      "CATCH CLIPPED WORDS"
    ],
    "render_mode": "post_composite",
    "font": "Inter",
    "weight": 900,
    "size_px": 76,
    "minimum_size_px": 64,
    "position": "Upper left",
    "bbox": [20, 35, 165, 920],
    "safe_margin_px": 48,
    "color": "#342d2d",
    "callout": {
      "text": "WORD MAY BE CLIPPED",
      "position": "Above warning marker",
      "minimum_size_px": 28
    }
  },
  "variations": {
    "count": 3,
    "strategies": [
      "Listening presenter and warning marker",
      "Large interrupted waveform with small presenter",
      "Problem waveform versus corrected waveform"
    ]
  },
  "quality_checks": [
    "Presenter identity preserved",
    "Red marker clearly visible",
    "Warning described as potential clipping",
    "Waveforms authentic or explicitly illustrative",
    "No unsupported claims about third-party editors",
    "Light background dominant",
    "Readable at mobile size"
  ]
}
```



<!-- assistant 2026-09-27T03:01:59.839Z -->

---

## D03 — Cutty presenter tracking

D03 demonstrates detecting a presenter's head frame by frame and determining where graphics can be placed. Its strongest visual elements are the face-detection box, directional quadrants and graphics positioned around a moving presenter. <FileCite ref="turn0file2" line_range_start={11} line_range_end={33}/>

One factual constraint matters here: the video includes footage of a Thai-speaking presenter who isn't identified in the fact sheet. The specification must not substitute your face and present that as authentic demo footage.

### D03 A1 — Tracking quadrants

<badge>Recipe: detection_overlay</badge>

Your face is the hero, and a simple geometric system explains the technology. The directional labels should be large enough to communicate the concept without requiring the viewer to inspect a complicated diagram.

```json
{
  "id": "d03.a1",
  "version": "1.0",
  "video": {
    "id": "D03",
    "brand_id": "brand.appydave.light.v1",
    "topic": "Cutty presenter tracking",
    "working_title": "I Taught AI Where My Face Is",
    "audience": "Creators using video overlays",
    "promise": "Explain how an agent finds safe positions for graphics around a presenter"
  },
  "creative": {
    "recipe": "detection_overlay",
    "story": "AI identifies the presenter and understands surrounding space",
    "hero": "Presenter inside detection box",
    "secondary_hero": "Four directional quadrants",
    "emotion": "Discovery and enthusiasm",
    "visual_metaphor": "Computer vision made visible",
    "style": "Editorial photography with technical annotation",
    "reference_tile": "D03 A1"
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "portrait_role": "surprised",
    "file_id": null,
    "preferred_asset": "headshot-appydave-23.png",
    "expression": "Wide eyes and open mouth",
    "pose": "Facing camera, optionally pointing toward face-detection box",
    "gesture_status": "Pointing requires reviewed variation",
    "framing": "Large medium close-up",
    "position": "Center",
    "bbox": [150, 260, 980, 740],
    "lighting": "Soft frontal light with subtle warm rim"
  },
  "assets": {
    "required": [
      {
        "id": "presenter",
        "source": "portrait_library",
        "role": "surprised",
        "status": "provided"
      }
    ],
    "optional": [
      "Authentic face-detection output",
      "Approved Cutty icon"
    ],
    "asset_requirements": {
      "tracking_overlay_can_be_illustrative": true,
      "do_not_present_static_mockup_as_actual_tracking_output": true
    }
  },
  "composition": {
    "canvas": [1280, 720],
    "background": "Cream studio background with restrained geometric annotations",
    "layout": "Centered presenter with tracking overlay",
    "primary_region": {
      "bbox": [150, 260, 980, 740],
      "content": "Large presenter portrait"
    },
    "secondary_region": {
      "bbox": [190, 290, 720, 710],
      "content": "Yellow rectangular detection box around head"
    },
    "supporting_region": {
      "bbox": [150, 170, 860, 830],
      "content": "Four directional quadrant labels surrounding presenter"
    },
    "graphics": [
      "Yellow detection rectangle",
      "Subtle dashed outer tracking boundary",
      "Four directional labels",
      "Thin measurement lines"
    ],
    "labels": [
      "N",
      "S",
      "E",
      "W"
    ],
    "lighting": "Warm editorial portrait lighting",
    "focal_order": [
      "Presenter face",
      "Detection box",
      "Directional labels"
    ]
  },
  "rendering": {
    "config_id": "rendering.thumbnail.v1",
    "mode": "portrait_plus_vector_overlay",
    "generate_background": true,
    "composite_presenter": true,
    "render_tracking_geometry_deterministically": true,
    "generate_final_text_in_image": false,
    "force_light_mode": true
  },
  "text_layer": {
    "headline": "AI KNOWS MY FACE",
    "alternates": [
      "GRAPHICS NEVER COVER ME",
      "MY AI TRACKS ME"
    ],
    "render_mode": "post_composite",
    "font": "Inter",
    "weight": 900,
    "size_px": 76,
    "minimum_size_px": 64,
    "position": "Upper left",
    "bbox": [20, 35, 175, 470],
    "safe_margin_px": 48,
    "color": "#342d2d",
    "directional_labels": {
      "font_weight": 900,
      "size_px": 44,
      "color": "#c8841a"
    }
  },
  "variations": {
    "count": 3,
    "strategies": [
      "Centered presenter with tracking quadrants",
      "Offset presenter with emphasized detection box",
      "Presenter with tracking boundary and one highlighted safe zone"
    ]
  },
  "quality_checks": [
    "Presenter identity preserved",
    "Detection box follows face position",
    "N/S/E/W labels correctly positioned",
    "Headline does not obstruct face",
    "Tracking geometry visually understandable",
    "Light-mode compliance",
    "Mobile readability"
  ]
}
```

### D03 A2 — Works in any language

<badge>Recipe: presenter_demo_evidence</badge>

The original tile combines your portrait with a Thai-speaking presenter, a tracking overlay and small graphics. It uses a human example to make an abstract technical feature tangible.

The video demonstrates tracking on Thai-language footage. That doesn't independently prove compatibility with every language, so the proposed headline is deliberately narrower than the original tile label.

```json
{
  "id": "d03.a2",
  "version": "1.0",
  "video": {
    "id": "D03",
    "brand_id": "brand.appydave.light.v1",
    "topic": "Presenter tracking demonstrated on Thai-language footage",
    "working_title": "AI That Frames the Presenter",
    "audience": "Creators interested in automated visual editing",
    "promise": "Show tracking and graphic placement on footage of a Thai-speaking presenter"
  },
  "creative": {
    "recipe": "presenter_demo_evidence",
    "story": "The creator introduces a real example of the technology working",
    "hero": "Tracked demo presenter",
    "secondary_hero": "AppyDave introducing the demonstration",
    "emotion": "Confidence and discovery",
    "visual_metaphor": "A presenter surrounded by correctly positioned graphics",
    "style": "Clean editorial technology demonstration",
    "reference_tile": "D03 A2"
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "portrait_role": "confident",
    "file_id": null,
    "preferred_asset": "headshot-appydave-15.png",
    "expression": "Friendly smile",
    "pose": "Looking toward or pointing at demonstration",
    "gesture_status": "Pointing requires reviewed variation",
    "framing": "Medium close-up",
    "position": "Left",
    "bbox": [180, 20, 960, 400],
    "lighting": "Soft natural editorial lighting"
  },
  "assets": {
    "required": [
      {
        "id": "presenter",
        "source": "portrait_library",
        "role": "confident",
        "status": "provided"
      },
      {
        "id": "demo_presenter",
        "source": "<VIDEO_ASSETS_ROOT>/D03/thai-presenter-frame.png",
        "status": "required",
        "identity": "Unknown",
        "must_use_authentic_footage": true
      }
    ],
    "optional": [
      "Approved graphic overlays from demonstration",
      "Authentic detection coordinates",
      "Thai-language audio transcript"
    ],
    "asset_requirements": {
      "do_not_invent_demo_presenter_identity": true,
      "do_not_replace_demo_presenter_with_appydave": true,
      "use_authentic_demo_frame": true
    }
  },
  "composition": {
    "canvas": [1280, 720],
    "background": "Cream editorial canvas",
    "layout": "AppyDave left, tracked presenter right",
    "primary_region": {
      "bbox": [180, 20, 960, 400],
      "content": "AppyDave introducing the demonstration"
    },
    "secondary_region": {
      "bbox": [150, 470, 930, 930],
      "content": "Authentic Thai-speaking presenter with tracking box"
    },
    "supporting_region": {
      "bbox": [250, 400, 800, 980],
      "content": "Small graphic overlays positioned around tracked presenter"
    },
    "graphics": [
      "Yellow face-detection rectangle",
      "N/S/E/W indicators",
      "Small graphic overlay examples",
      "Small Thai flag icon if appropriate"
    ],
    "labels": [
      "N",
      "S",
      "E",
      "W"
    ],
    "lighting": "Consistent neutral editorial treatment",
    "focal_order": [
      "Tracked demo presenter",
      "Tracking geometry",
      "AppyDave"
    ]
  },
  "rendering": {
    "config_id": "rendering.thumbnail.v1",
    "mode": "authentic_demo_frame_composite",
    "generate_background": true,
    "composite_presenter": true,
    "composite_authentic_demo_frame": true,
    "render_tracking_geometry_deterministically": true,
    "generate_final_text_in_image": false,
    "force_light_mode": true
  },
  "text_layer": {
    "headline": "AI TRACKS THIS PRESENTER",
    "alternates": [
      "WATCH THE GRAPHICS MOVE",
      "TRACKING IN ACTION"
    ],
    "render_mode": "post_composite",
    "font": "Inter",
    "weight": 900,
    "size_px": 72,
    "minimum_size_px": 64,
    "position": "Upper left",
    "bbox": [20, 35, 165, 900],
    "safe_margin_px": 48,
    "color": "#342d2d",
    "label_policy": "Render directional labels with compositor"
  },
  "variations": {
    "count": 3,
    "strategies": [
      "Creator introducing tracked presenter",
      "Tracked presenter with creator inset",
      "Tracked presenter with emphasized graphic safe zones"
    ]
  },
  "quality_checks": [
    "Authentic demo footage used",
    "Demo presenter identity not invented",
    "No unsupported universal-language claim",
    "Tracking geometry correctly positioned",
    "Graphic overlays avoid presenter",
    "Light-mode compliance",
    "Mobile readability"
  ]
}
```

### D03 A3 — Agent places graphics

<badge>Recipe: process_to_outputs</badge>

This is the most technical D03 concept. It presents several successive tracked frames, then uses arrows to show graphics being placed into the available space.

The original tile used a dark technical panel. This version places a contained workflow on a cream canvas.

```json
{
  "id": "d03.a3",
  "version": "1.0",
  "video": {
    "id": "D03",
    "brand_id": "brand.appydave.light.v1",
    "topic": "Automated graphic placement around presenters",
    "working_title": "Cutty Presenter Tracking",
    "audience": "Creators and developers building automated video workflows",
    "promise": "Show how tracking data can identify positions for future automated overlays"
  },
  "creative": {
    "recipe": "process_to_outputs",
    "story": "Frame-by-frame tracking produces candidate graphic positions",
    "hero": "Sequence of tracked presenter frames",
    "secondary_hero": "Graphic placement outputs",
    "emotion": "Technical clarity",
    "visual_metaphor": "Tracked frames feeding a placement system",
    "style": "Clean technical editorial diagram",
    "reference_tile": "D03 A3"
  },
  "presenter": {
    "library_id": "presenter.appydave.v1",
    "portrait_role": "confident",
    "file_id": null,
    "preferred_asset": "headshot-appydave-15.png",
    "visible": true,
    "expression": "Natural conversational expression",
    "pose": "Several successive frames showing movement",
    "framing": "Small repeated video-frame portraits",
    "position": "Upper center",
    "bbox": [200, 80, 650, 720],
    "note": "Prefer authentic consecutive video frames over repeating one photograph"
  },
  "assets": {
    "required": [
      {
        "id": "tracking_frames",
        "source": "<VIDEO_ASSETS_ROOT>/D03/tracking-frame-sequence/",
        "status": "required",
        "preferred": "Authentic consecutive video frames"
      }
    ],
    "optional": [
      "Authentic tracking coordinates",
      "Graphic placement examples",
      "Approved Cutty icon",
      "Editing timeline"
    ],
    "asset_requirements": {
      "frame_sequence_must_be_temporally_consistent": true,
      "illustrative_frames_must_not_be_presented_as_real_output": true,
      "do_not_claim_finished_automated_overlay_capability": true
    }
  },
  "composition": {
    "canvas": [1280, 720],
    "background": "Cream technical editorial canvas",
    "layout": "Tracked frame sequence flowing toward graphic outputs",
    "primary_region": {
      "bbox": [210, 50, 640, 730],
      "content": "Four successive presenter frames with tracking boxes"
    },
    "secondary_region": {
      "bbox": [240, 750, 680, 960],
      "content": "Three candidate graphic output icons"
    },
    "supporting_region": {
      "bbox": [700, 60, 920, 940],
      "content": "Simplified editing timeline"
    },
    "graphics": [
      "Four presenter frames",
      "Yellow detection rectangles",
      "Directional labels",
      "Amber arrows",
      "Image icon",
      "Text icon",
      "Video icon",
      "Editing timeline"
    ],
    "labels": [
      "N",
      "S",
      "E",
      "W"
    ],
    "lighting": "Neutral and consistent across all video frames",
    "focal_order": [
      "Tracked frame sequence",
      "Output arrows",
      "Graphic icons",
      "Timeline"
    ]
  },
  "rendering": {
    "config_id": "rendering.thumbnail.v1",
    "mode": "deterministic_workflow_composite",
    "generate_background": false,
    "composite_authentic_frames": true,
    "render_diagram_deterministically": true,
    "generate_final_text_in_image": false,
    "force_light_mode": true
  },
  "text_layer": {
    "headline": "GRAPHICS FIND THEIR PLACE",
    "alternates": [
      "AI FINDS THE SPACE",
      "OVERLAYS ON AUTOPILOT"
    ],
    "render_mode": "post_composite",
    "font": "Inter",
    "weight": 900,
    "size_px": 72,
    "minimum_size_px": 64,
    "position": "Upper left",
    "bbox": [20, 35, 170, 900],
    "safe_margin_px": 48,
    "color": "#342d2d",
    "label_policy": "Render all tracking labels and output icons separately"
  },
  "variations": {
    "count": 3,
    "strategies": [
      "Four tracked frames feeding three graphic outputs",
      "Large tracking sequence with small timeline",
      "One highlighted safe zone feeding a graphic placement example"
    ]
  },
  "quality_checks": [
    "Tracking sequence temporally consistent",
    "Directional labels correctly positioned",
    "Candidate positions not misrepresented as completed automation",
    "Graphic outputs visually distinct",
    "Arrows indicate correct flow",
    "Cream canvas dominant",
    "Mobile readability"
  ]
}
```



<!-- assistant 2026-09-27T03:02:27.935Z -->

---

# C. Reusable recipe catalogue

The nine concepts can be implemented as nine named presets, but they do not represent nine completely different composition systems.

There are six underlying layout families: creator showcase, transformation, diagnostic comparison, pipeline, annotated demonstration and process visualization.

Keeping the nine presets preserves the creative distinctions in your board. Sharing the six underlying layout families reduces implementation complexity.

The following catalogue is deliberately generic. It contains no D01, D02 or D03-specific content.

```json
{
  "catalogue_id": "thumbnail.recipes.v1",
  "version": "1.0",
  "recipes": [
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
    },
    {
      "id": "creator_interface",
      "layout_family": "creator_showcase",
      "story_shape": "A human creator demonstrates or explains one specific software product",
      "layout": "Large authentic interface with overlapping presenter portrait",
      "presenter_role": "Thinking, confident or pointing",
      "required_assets": [
        "Approved presenter portrait",
        "Authentic product screenshot"
      ],
      "typical_graphics": [
        "Application interface",
        "One highlighted feature",
        "Subtle annotation"
      ],
      "lighting": "Neutral editorial portrait lighting",
      "background": "Light brand canvas",
      "when_not_to_use": [
        "Products without usable screenshots",
        "Complex interfaces that cannot be simplified",
        "Stories where the software itself is not central"
      ],
      "related_recipes": [
        "creator_ecosystem"
      ]
    },
    {
      "id": "creator_transformation",
      "layout_family": "transformation",
      "story_shape": "A human creator moves from a recognizable problem to a better working situation",
      "layout": "Left-to-right before-and-after comparison with a prominent directional transition",
      "presenter_role": "Concerned before; confident or enthusiastic after",
      "required_assets": [
        "Approved presenter portraits or reviewed variations",
        "Problem illustration",
        "Result illustration or authentic product imagery"
      ],
      "typical_graphics": [
        "Before-and-after panels",
        "Directional arrow",
        "Contrasting equipment or software"
      ],
      "lighting": "Matched lighting between both scenes",
      "background": "Light brand canvas",
      "when_not_to_use": [
        "Stories without a meaningful transformation",
        "Cases where the result is unverified",
        "Topics requiring a detailed technical explanation"
      ],
      "related_recipes": [
        "diagnostic_transformation"
      ]
    },
    {
      "id": "diagnostic_transformation",
      "layout_family": "transformation",
      "story_shape": "A measurable or observable technical problem becomes a better technical result",
      "layout": "Presenter on one side; stacked diagnostic comparisons on the other",
      "presenter_role": "Surprised, concerned or explanatory",
      "required_assets": [
        "Presenter portrait",
        "Authentic or explicitly illustrative diagnostic data"
      ],
      "typical_graphics": [
        "Stacked comparison panels",
        "Color-coded diagnostic traces",
        "Before-and-after indicators"
      ],
      "lighting": "Neutral editorial lighting",
      "background": "Light brand canvas",
      "when_not_to_use": [
        "Stories without comparable outputs",
        "Cases where fabricated measurements might be mistaken for real data",
        "Topics with no clear visual diagnostic"
      ],
      "related_recipes": [
        "creator_transformation",
        "diagnostic_warning"
      ]
    },
    {
      "id": "agent_pipeline_hero",
      "layout_family": "pipeline",
      "story_shape": "One agent or tool coordinates multiple processing operations",
      "layout": "Central product or agent hero with simplified input-to-output flow",
      "presenter_role": "Not required",
      "required_assets": [
        "Approved agent or product character",
        "Verified process steps"
      ],
      "typical_graphics": [
        "Input icon",
        "Output icon",
        "Directional arrows",
        "Three to five process labels"
      ],
      "lighting": "Soft product illustration lighting",
      "background": "Light brand canvas",
      "when_not_to_use": [
        "Agents without an approved visual identity",
        "Pipelines too complicated to simplify accurately",
        "Videos primarily about human experiences"
      ],
      "related_recipes": [
        "process_to_outputs"
      ]
    },
    {
      "id": "diagnostic_warning",
      "layout_family": "diagnostic_comparison",
      "story_shape": "A tool detects or highlights a specific problem that the viewer should notice",
      "layout": "Human reaction beside one dominant diagnostic warning",
      "presenter_role": "Concerned, listening or surprised",
      "required_assets": [
        "Approved presenter portrait",
        "Authentic or illustrative diagnostic graphic"
      ],
      "typical_graphics": [
        "Warning marker",
        "Highlighted problem area",
        "Optional comparison panel"
      ],
      "lighting": "Neutral editorial lighting",
      "background": "Light brand canvas",
      "when_not_to_use": [
        "Stories without a genuine detectable problem",
        "Cases where warning graphics exaggerate the severity",
        "Topics requiring several equally important explanations"
      ],
      "related_recipes": [
        "diagnostic_transformation"
      ]
    },
    {
      "id": "detection_overlay",
      "layout_family": "annotated_demonstration",
      "story_shape": "A technical system identifies, measures or understands something visually",
      "layout": "One large subject with a simple technical overlay",
      "presenter_role": "Surprised, neutral or explanatory",
      "required_assets": [
        "Approved subject photograph",
        "Verified overlay geometry or clearly illustrative annotations"
      ],
      "typical_graphics": [
        "Detection rectangle",
        "Directional markers",
        "Measurement lines",
        "Highlighted region"
      ],
      "lighting": "Clear neutral photography",
      "background": "Light brand canvas",
      "when_not_to_use": [
        "Features that cannot be represented with simple annotations",
        "Cases where the overlay would obscure the subject",
        "Claims requiring proof that a static illustration cannot provide"
      ],
      "related_recipes": [
        "presenter_demo_evidence"
      ]
    },
    {
      "id": "presenter_demo_evidence",
      "layout_family": "annotated_demonstration",
      "story_shape": "A creator introduces a real demonstration that provides evidence of a technical capability",
      "layout": "Creator portrait beside an authentic demonstration frame",
      "presenter_role": "Confident, explanatory or pointing",
      "required_assets": [
        "Approved creator portrait",
        "Authentic demonstration screenshot or frame"
      ],
      "typical_graphics": [
        "Highlighted demonstration region",
        "One or two explanatory annotations",
        "Small supporting icons"
      ],
      "lighting": "Consistent editorial treatment",
      "background": "Light brand canvas",
      "when_not_to_use": [
        "Stories without authentic demonstration footage",
        "Examples requiring unverified claims",
        "Demonstrations too visually complicated for thumbnail scale"
      ],
      "related_recipes": [
        "detection_overlay",
        "creator_interface"
      ]
    },
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
  ],
  "layout_families": [
    "creator_showcase",
    "transformation",
    "pipeline",
    "diagnostic_comparison",
    "annotated_demonstration",
    "process_visualization"
  ]
}
```

The closest overlaps are `creator_ecosystem` and `creator_interface`, `creator_transformation` and `diagnostic_transformation`, and `detection_overlay` and `presenter_demo_evidence`.

They should share layout components but remain separate presets because their asset requirements and storytelling purposes differ.

---

# D. Text-layer contract

The text layer should be independently editable and must not be baked into the generated background image.

This is particularly important for your workflow because titles may change after recording or editing. A new headline should not require regenerating your portrait, software imagery or supporting graphics.

```json
{
  "id": "text_layer.contract.v1",
  "version": "1.0",
  "default": {
    "render_mode": "post_composite",
    "reason": "Exact spelling, consistent typography, editable headlines and predictable layout",
    "font_family": "Inter",
    "font_fallback": "Arial",
    "font_weight": 900,
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

The font-size values are starting constraints, not universal guarantees. A narrow headline region may require fewer words, a different line break or a wider text area.

For thumbnail production, a short readable headline is more useful than forcing a long title into the design.



<!-- assistant 2026-09-27T03:02:49.491Z -->

---

# E. Universal thumbnail schema

This final object is the reusable master template. Unlike the nine filled specifications, it contains descriptions and expected value types rather than video-specific creative decisions.

It is a JSON template and field dictionary, not a formal JSON Schema validator. It is designed to be copied into a new conversation or implemented as a configuration contract in a thumbnail-generation application.

```json
{
  "schema_version": "1.0",
  "description": "Portable specification for one reproducible YouTube thumbnail",
  "id": "Unique thumbnail specification identifier",
  "version": "Version of this individual thumbnail specification",

  "video": {
    "id": "Unique video or project identifier",
    "brand_id": "Reference to external brand configuration",
    "topic": "Actual subject of the video",
    "working_title": "Current video title, which may be unapproved",
    "audience": "Intended viewers",
    "promise": "What the video genuinely delivers"
  },

  "creative": {
    "recipe": "Identifier from the reusable recipe catalogue",
    "story": "One-sentence visual story",
    "hero": "Primary visual subject",
    "secondary_hero": "Supporting visual subject, if needed",
    "emotion": "Intended emotional tone",
    "visual_metaphor": "Concrete visual representation of the story",
    "style": "Photographic or illustrative treatment",
    "reference_tile": "Optional identifier of the approved visual reference"
  },

  "presenter": {
    "library_id": "External presenter-library identifier",
    "portrait_role": "Desired expression or portrait category",
    "file_id": "Optional exact external asset identifier or null",
    "preferred_asset": "Preferred filename from the library",
    "visible": "Boolean indicating whether the presenter appears",
    "expression": "Desired facial expression",
    "pose": "Desired body position or gesture",
    "gesture_status": "Available, missing or requires reviewed variation",
    "framing": "Close-up, medium close-up or another camera framing",
    "position": "Position within the thumbnail",
    "bbox": "Normalized presenter bounding box [top,left,bottom,right]",
    "lighting": "Lighting treatment",
    "identity_policy": "Identity-preservation instructions"
  },

  "assets": {
    "required": [
      {
        "id": "Logical asset identifier",
        "source": "External asset path or library reference",
        "role": "Purpose of the asset",
        "status": "provided, required, missing or illustrative",
        "file_id": "Optional external file identifier"
      }
    ],
    "optional": [
      "Additional useful asset identifiers or descriptions"
    ],
    "asset_requirements": {
      "use_authentic_assets": "Whether authentic source assets are mandatory",
      "allow_illustrative_assets": "Whether conceptual graphics may be generated",
      "missing_asset_policy": "What to do when an asset cannot be resolved",
      "accuracy_constraints": "Requirements preventing misleading imagery"
    }
  },

  "composition": {
    "canvas": [
      1280,
      720
    ],
    "background": "Description of the background and its visual treatment",
    "layout": "Overall composition strategy",
    "primary_region": {
      "bbox": "Normalized bounding box",
      "content": "Description of primary content"
    },
    "secondary_region": {
      "bbox": "Normalized bounding box",
      "content": "Description of secondary content"
    },
    "supporting_region": {
      "bbox": "Optional normalized bounding box",
      "content": "Optional supporting content"
    },
    "graphics": [
      "List of visual graphics and annotations"
    ],
    "labels": [
      "Exact supporting text labels"
    ],
    "lighting": "Scene-wide lighting treatment",
    "focal_order": [
      "First visual priority",
      "Second visual priority",
      "Third visual priority"
    ],
    "depth": "Optional layering and overlap instructions"
  },

  "rendering": {
    "config_id": "Reference to external rendering configuration",
    "mode": "Generation, compositing or hybrid rendering strategy",
    "generate_background": "Boolean",
    "composite_presenter": "Boolean",
    "composite_authentic_assets": "Boolean",
    "render_diagram_deterministically": "Boolean",
    "generate_final_text_in_image": "Boolean",
    "force_light_mode": "Boolean",
    "maximum_major_elements": "Optional integer complexity limit"
  },

  "text_layer": {
    "headline": "Exact proposed thumbnail headline",
    "alternates": [
      "Alternative headline one",
      "Alternative headline two"
    ],
    "render_mode": "post_composite",
    "font": "Inter",
    "weight": 900,
    "size_px": 88,
    "minimum_size_px": 64,
    "position": "Human-readable headline position",
    "bbox": "Normalized headline bounding box",
    "safe_margin_px": 48,
    "color": "#342d2d",
    "labels": [
      "Optional supporting labels"
    ],
    "callout": {
      "text": "Optional callout wording",
      "position": "Optional callout placement",
      "minimum_size_px": 28
    }
  },

  "variations": {
    "count": 3,
    "strategies": [
      "First controlled creative variation",
      "Second controlled creative variation",
      "Third controlled creative variation"
    ]
  },

  "quality_checks": [
    "Presenter identity preserved",
    "Visual story matches the video",
    "Required assets resolved",
    "Technical claims supported",
    "Brand rules followed",
    "Text spelling verified",
    "Mobile-size readability confirmed",
    "Output reviewed before publication"
  ]
}
```

## Fresh-chat execution instructions

The specification is only one part of reproducibility. A new conversation also needs explicit execution instructions so the model knows how to interpret the JSON and handle missing assets.

Use the following as the reusable kickoff prompt.

<WritingBlock id="73581" variant="document"># Thumbnail Director — Execution Instructions v1.0

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

Do not treat generated examples as approved publishing assets until the user has reviewed them.</WritingBlock>

The key to reproducing the nine-concept board is to preserve four things together: **the video facts, the approved visual recipe, the actual source assets and the rendering instructions.** JSON makes those decisions portable; the asset library and execution process make them usable.

For the first implementation, I would use these nine specifications as regression examples. Every time the Thumbnail Director changes, regenerate the nine designs and compare them with the approved reference board. That gives you a practical way to detect whether improvements to the system are preserving the creative quality you originally liked.