# Thumbnail recipe library

**Purpose**: Named, reusable thumbnail recipes with no video-specific details. Pick 3 *different* ones per video.
**For Agents**:
- Machine-readable source: `recipes.json` (generated from ChatGPT 2026-09-27). This page is a rendered view, so edit the JSON and regenerate.
- 9 recipes in 6 layout families. Near-twins share layout parts but differ in story or assets: `creator_ecosystem`/`creator_interface`, `creator_transformation`/`diagnostic_transformation`, `detection_overlay`/`presenter_demo_evidence`.

| Recipe | Family | Story shape | Board tile |
|---|---|---|---|
| `creator_ecosystem` | creator_showcase | One creator introduces a collection of interconnected tools or capabilities | d01.a1 |
| `creator_interface` | creator_showcase | A human creator demonstrates or explains one specific software product | d01.a2 |
| `creator_transformation` | transformation | A human creator moves from a recognizable problem to a better working situation | d01.a3 |
| `diagnostic_transformation` | transformation | A measurable or observable technical problem becomes a better technical result | d02.a1 |
| `agent_pipeline_hero` | pipeline | One agent or tool coordinates multiple processing operations | d02.a2 |
| `diagnostic_warning` | diagnostic_comparison | A tool detects or highlights a specific problem that the viewer should notice | d02.a3 |
| `detection_overlay` | annotated_demonstration | A technical system identifies, measures or understands something visually | d03.a1 |
| `presenter_demo_evidence` | annotated_demonstration | A creator introduces a real demonstration that provides evidence of a technical capability | d03.a2 |
| `process_to_outputs` | process_visualization | A sequence of processing steps produces one or more visible outputs | d03.a3 |

## `creator_ecosystem`

- **Story shape:** One creator introduces a collection of interconnected tools or capabilities
- **Layout:** Large presenter on one side; organized collection of product tiles on the other
- **Presenter:** Surprised, confident or pointing
- **Required assets:** Approved presenter portrait; Product logos or screenshots
- **Typical graphics:** Application tiles; Small icons; Connecting arrows; Simplified production timeline
- **Don't use for:** Single-feature demonstrations; Videos without a genuine collection of tools; Topics where application tiles would become illegible
- **Related:** creator_interface

## `creator_interface`

- **Story shape:** A human creator demonstrates or explains one specific software product
- **Layout:** Large authentic interface with overlapping presenter portrait
- **Presenter:** Thinking, confident or pointing
- **Required assets:** Approved presenter portrait; Authentic product screenshot
- **Typical graphics:** Application interface; One highlighted feature; Subtle annotation
- **Don't use for:** Products without usable screenshots; Complex interfaces that cannot be simplified; Stories where the software itself is not central
- **Related:** creator_ecosystem

## `creator_transformation`

- **Story shape:** A human creator moves from a recognizable problem to a better working situation
- **Layout:** Left-to-right before-and-after comparison with a prominent directional transition
- **Presenter:** Concerned before; confident or enthusiastic after
- **Required assets:** Approved presenter portraits or reviewed variations; Problem illustration; Result illustration or authentic product imagery
- **Typical graphics:** Before-and-after panels; Directional arrow; Contrasting equipment or software
- **Don't use for:** Stories without a meaningful transformation; Cases where the result is unverified; Topics requiring a detailed technical explanation
- **Related:** diagnostic_transformation

## `diagnostic_transformation`

- **Story shape:** A measurable or observable technical problem becomes a better technical result
- **Layout:** Presenter on one side; stacked diagnostic comparisons on the other
- **Presenter:** Surprised, concerned or explanatory
- **Required assets:** Presenter portrait; Authentic or explicitly illustrative diagnostic data
- **Typical graphics:** Stacked comparison panels; Color-coded diagnostic traces; Before-and-after indicators
- **Don't use for:** Stories without comparable outputs; Cases where fabricated measurements might be mistaken for real data; Topics with no clear visual diagnostic
- **Related:** creator_transformation, diagnostic_warning

## `agent_pipeline_hero`

- **Story shape:** One agent or tool coordinates multiple processing operations
- **Layout:** Central product or agent hero with simplified input-to-output flow
- **Presenter:** Not required
- **Required assets:** Approved agent or product character; Verified process steps
- **Typical graphics:** Input icon; Output icon; Directional arrows; Three to five process labels
- **Don't use for:** Agents without an approved visual identity; Pipelines too complicated to simplify accurately; Videos primarily about human experiences
- **Related:** process_to_outputs

## `diagnostic_warning`

- **Story shape:** A tool detects or highlights a specific problem that the viewer should notice
- **Layout:** Human reaction beside one dominant diagnostic warning
- **Presenter:** Concerned, listening or surprised
- **Required assets:** Approved presenter portrait; Authentic or illustrative diagnostic graphic
- **Typical graphics:** Warning marker; Highlighted problem area; Optional comparison panel
- **Don't use for:** Stories without a genuine detectable problem; Cases where warning graphics exaggerate the severity; Topics requiring several equally important explanations
- **Related:** diagnostic_transformation

## `detection_overlay`

- **Story shape:** A technical system identifies, measures or understands something visually
- **Layout:** One large subject with a simple technical overlay
- **Presenter:** Surprised, neutral or explanatory
- **Required assets:** Approved subject photograph; Verified overlay geometry or clearly illustrative annotations
- **Typical graphics:** Detection rectangle; Directional markers; Measurement lines; Highlighted region
- **Don't use for:** Features that cannot be represented with simple annotations; Cases where the overlay would obscure the subject; Claims requiring proof that a static illustration cannot provide
- **Related:** presenter_demo_evidence

## `presenter_demo_evidence`

- **Story shape:** A creator introduces a real demonstration that provides evidence of a technical capability
- **Layout:** Creator portrait beside an authentic demonstration frame
- **Presenter:** Confident, explanatory or pointing
- **Required assets:** Approved creator portrait; Authentic demonstration screenshot or frame
- **Typical graphics:** Highlighted demonstration region; One or two explanatory annotations; Small supporting icons
- **Don't use for:** Stories without authentic demonstration footage; Examples requiring unverified claims; Demonstrations too visually complicated for thumbnail scale
- **Related:** detection_overlay, creator_interface

## `process_to_outputs`

- **Story shape:** A sequence of processing steps produces one or more visible outputs
- **Layout:** Left-to-right sequence of simplified process frames feeding output icons
- **Presenter:** Optional; repeated frames may replace a hero portrait
- **Required assets:** Authentic or illustrative process frames; Verified output types
- **Typical graphics:** Repeated frames; Directional arrows; Output icons; Simplified timeline
- **Don't use for:** Processes that cannot be simplified visually; Stories without meaningful outputs; Topics where multiple small frames become illegible
- **Related:** agent_pipeline_hero
