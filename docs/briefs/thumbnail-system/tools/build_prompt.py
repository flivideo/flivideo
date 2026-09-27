#!/usr/bin/env python3
"""scene JSON + shared brand/style -> ONE compact JSON prompt for a chat image model.

Usage: build_prompt.py scenes/<id>.json [--out file]
The scene file is the only per-thumbnail input. Shared blocks live in shared/.
Prints the JSON to paste; its `attach` list is the reference images to upload with it.
"""
import json, sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scene = json.load(open(sys.argv[1]))
prompt = {
    "task": "Generate ONE finished 16:9 YouTube thumbnail image from this JSON. Keys are semantic; values are what I want.",
    "scene": scene["scene"],
    "presenter": scene["presenter"],
    "headline_zone": scene["headline_zone"] + " (leave clear; the headline is added afterwards)",
    "brand": json.load(open(os.path.join(root, "shared/brand-appydave.json"))),
    "style": json.load(open(os.path.join(root, "shared/style-board.json"))),
    "attach": ["style-reference-board.png"] + [r for r in scene["presenter"]["identity_references"]],
    "output": "the image only, then one line: what you would change",
}
text = json.dumps(prompt, indent=1, ensure_ascii=False)
if "--out" in sys.argv: open(sys.argv[sys.argv.index("--out") + 1], "w").write(text)
print(text)
