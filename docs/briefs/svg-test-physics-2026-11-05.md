---
created: 2026-11-05
timestamp: 2026-11-05T11:40+07:00
---
# Brief — SVG dungeon test, step two: solid walls and physical objects (same worker, M2)

**Purpose**: David loved video B and doesn't want it changed much. His one complaint: **the characters walk through walls, so it doesn't hold up the way a game does.** He wonders whether it needs a game engine that understands objects have physical properties, and leaves the how to you. **Owner**: flivideo-orch. **David's go**: 2026-11-05.

## The question
What is the least we need for a video to be physically believable, and does that take a game engine?

Your diagnosis first, from your own code: why do they pass through walls? I expect it's because scripted tweens move sprites and nothing knows the walls exist, but confirm it.

## Try these in order, and stop at the first that's believable
| | Approach | Notes |
|---|---|---|
| 1 | **Solid map + pathfinding**: the map is data, characters route around walls (A* on a grid), plus group spacing so they don't overlap | Cheapest. May be all it takes |
| 2 | **Baked physics**: a physics engine (Rapier or similar) for collisions and reactions such as a boss hit knocking the party back, the gate swinging, the chest lid | Must be deterministic. HyperFrames seeks per frame, so simulate first and bake to a timeline, rather than simulating live during render. Show the same input gives the same frames |
| 3 | **A real game engine** (Godot, Phaser or similar) | Research from current docs. Build only if 1 and 2 clearly fall short, and say why. Headless render and agent editability are the questions |

## Prove it by measurement, not only by eye
Write a **validator**: for every frame, no character's footprint overlaps a wall tile or another character beyond an allowed margin. Run it on the **original B first** and report how many frames fail, so the problem is measured. Then run it on the new version: target zero. This also answers the earlier finding that only looking at frames caught defects.

Also check whether playable C has the same problem, and fix it if it's cheap, since a game should certainly stop at walls.

## Keep what he loved
- Same art, story, length, captions, torchlight, camera feel. Keep `renders/b.mp4` as it is, and write new files (`b-physics/`, `renders/b-physics.mp4`). Don't add features for their own sake.
- The camera must still not hide the action.
- Re-run the agent-change test (red boss, door moved, new label) on the new version. Agent editability is the question that matters most: does physics make a change safer or more fragile? Report lines changed and whether it was right first time.

## Rules
Same as before: this folder only, pinned versions at least two weeks old, nothing global, no paid APIs, no `sudo`, `--describe false` on snapshots. The M2 is also running `voice-poc` (a separate worker, not yours; don't touch it): one render at a time, and stop if the machine is swapping hard. No servers left running. Stay out of every FliVideo app. The stop rule still holds: update `RIG-CANDIDATE.md` rather than building a pipeline.

## Deliverables
- `renders/b-physics.mp4`, under 15 MB.
- `RESULTS-physics.md`: diagnosis, validator results before and after, what each approach cost (lines, build time, render time, file size), the change test, a plain answer to "does this need a game engine?", and not established.
- `page-physics/index.html` plus files: a light-only AppyDave page with the same styling rules as before. Original B and the new one side by side at the top, then the answer, then the numbers. Use the same frames-at-a-moment comparison showing where B went through a wall. Include `play.html` if C changed. Under 45 MB. Orch publishes it.

Commit in the folder. End with exactly one line: `APPYNET: done — <one line>` or `APPYNET: blocked — <why>` or `APPYNET: question — <a real decision>`. Never for status.
