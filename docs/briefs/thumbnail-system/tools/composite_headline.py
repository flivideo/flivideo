#!/usr/bin/env python3
"""Text-layer compositor: overlay a spec's headline onto a generated image (post_composite).

Usage: composite_headline.py <spec.json> <generated.png> <out.png> [--highlight WORD]
Reads text_layer.headline / size_px / bbox ([top,left,bottom,right] in 0-1000) from the spec.
Font: Bebas Neue (OFL, tools/fonts/). Also writes <out>-320.png, the mobile check.
"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont

spec, src, out = sys.argv[1:4]
hl = sys.argv[sys.argv.index('--highlight') + 1].upper() if '--highlight' in sys.argv else None
t = json.load(open(spec))['text_layer']
img = Image.open(src).convert('RGB').resize((1280, 720), Image.LANCZOS)
top, left = t['bbox'][0] * 720 // 1000, t['bbox'][1] * 1280 // 1000
size = max(t.get('size_px', 88), t.get('minimum_size_px', 64)) * 1.4  # spec sizes assume 1280 canvas; Bebas runs small
font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'fonts', 'BebasNeue-Regular.ttf'), int(size))
d = ImageDraw.Draw(img)
x = left
for i, word in enumerate(t['headline'].split()):
    w = d.textlength(word, font=font)
    if hl and word.strip('?!.').upper() == hl.strip('?!.'):
        d.rounded_rectangle([x - 10, top + size * .14, x + w + 10, top + size], radius=10, fill='#ffde59')
    d.text((x, top), word, font=font, fill='#342d2d')
    x += w + d.textlength(' ', font=font)
img.save(out)
img.resize((320, 180), Image.LANCZOS).save(out.replace('.png', '-320.png'))
print(out)
