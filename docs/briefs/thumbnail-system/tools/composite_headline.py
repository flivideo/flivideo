#!/usr/bin/env python3
"""Text-layer compositor: overlay a spec's headline onto a generated image (post_composite).

Usage: composite_headline.py <spec.json> <generated.png> <out.png> [--highlight WORD] [--zone auto|spec]
- Reads text_layer.headline / color / accent from the spec.
- --zone auto (default): scores candidate zones by visual busyness (edge density) and places the
  headline in the calmest one, because the image model doesn't always leave the zone the spec named.
  --zone spec: use text_layer.bbox ([top,left,bottom,right], 0-1000).
- Font is fitted to the zone width (never below text_layer.minimum_size_px, default 64); a soft
  shadow keeps it legible on busy ground. Also writes <out>-320.png, the mobile check.
Font: Bebas Neue (OFL, tools/fonts/).
"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat

spec, src, out = sys.argv[1:4]
arg = lambda k, d=None: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
t = json.load(open(spec))['text_layer']
hl = (arg('--highlight') or '').upper() or None
accent = t['accent'] if isinstance(t.get('accent'), dict) else {}
accent_words = [w.upper() for w in accent.get('words', [])]
color = t.get('color', '#342d2d')
min_px = t.get('minimum_size_px', 64)
FONT = os.path.join(os.path.dirname(__file__), 'fonts', 'BebasNeue-Regular.ttf')

img = Image.open(src).convert('RGB').resize((1280, 720), Image.LANCZOS)
W, H, M = 1280, 720, 40

# candidate zones (x0, y0, x1, y1): top/bottom bands, left/right/centre
Z = {'top-left': (M, M, 700, 210), 'top-right': (580, M, W - M, 210), 'top-centre': (240, M, 1040, 210),
     'bottom-left': (M, 520, 700, H - M), 'bottom-right': (580, 520, W - M, H - M)}
if arg('--zone', 'auto') == 'spec':
    b = t['bbox']; zone = (b[1] * W // 1000, b[0] * H // 1000, b[3] * W // 1000, b[2] * H // 1000); name = 'spec'
else:
    edges = img.convert('L').filter(ImageFilter.FIND_EDGES)
    score = {k: ImageStat.Stat(edges.crop(z)).mean[0] for k, z in Z.items()}
    name = min(score, key=score.get); zone = Z[name]

d = ImageDraw.Draw(img)
words = t['headline'].split()
x0, y0, x1, y1 = zone
zw, zh = x1 - x0, y1 - y0
def fit(lines):
    s = 170
    while s > 20:
        f = ImageFont.truetype(FONT, s)
        if max(d.textlength(' '.join(l), font=f) for l in lines) <= zw and s * len(lines) * 0.95 <= zh + (s * 0.9 if len(lines) > 1 else 0): return s
        s -= 4
    return s
one = [words]
splits = [[words[:i], words[i:]] for i in range(1, len(words))]
best2 = max(splits, key=fit) if splits else one
size, lines = (fit(one), one)
if splits and fit(best2) > size * 1.25: size, lines = fit(best2), best2   # wrap only when it buys real size
if size < min_px: print('WARNING: headline below minimum', size, file=sys.stderr)
f = ImageFont.truetype(FONT, size)
lh = int(size * 0.92)
block_h = lh * len(lines)
yb = y0 if 'top' in name or name == 'spec' else y1 - block_h
shadow = Image.new('RGBA', img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow)
for i, l in enumerate(lines):
    tw = d.textlength(' '.join(l), font=f)
    lx = x0 if 'left' in name or name == 'spec' else (x1 - tw if 'right' in name else x0 + (zw - tw) / 2)
    sd.text((lx + 3, yb + i * lh + 4), ' '.join(l), font=f, fill=(0, 0, 0, 170))
img.paste(Image.new('RGB', img.size, 'black'), (0, 0), shadow.filter(ImageFilter.GaussianBlur(6)))
if '--pill' in sys.argv:   # AppyDave brown panel behind the text: works on busy ground
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    widths = [d.textlength(' '.join(l), font=f) for l in lines]
    bx0 = min((x0 if 'left' in name or name == 'spec' else (x1 - w if 'right' in name else x0 + (zw - w) / 2)) for w in widths)
    od.rounded_rectangle([bx0 - 22, yb - 4, bx0 + max(widths) + 22, yb + block_h + size * 0.12], radius=16, fill=(52, 45, 45, 225))
    img.paste(ov, (0, 0), ov)
d = ImageDraw.Draw(img)
for i, l in enumerate(lines):
    tw = d.textlength(' '.join(l), font=f)
    x = x0 if 'left' in name or name == 'spec' else (x1 - tw if 'right' in name else x0 + (zw - tw) / 2)
    y = yb + i * lh
    for word in l:
        w = d.textlength(word, font=f); fill = color
        key = word.strip('?!.').upper()
        if hl and key == hl.strip('?!.'):
            d.rounded_rectangle([x - 10, y + size * .14, x + w + 10, y + size], radius=10, fill='#ffde59'); fill = '#342d2d'
        elif key in accent_words:
            fill = accent.get('color', '#ffde59')
        d.text((x, y), word, font=f, fill=fill)
        x += w + d.textlength(' ', font=f)
img.save(out)
img.resize((320, 180), Image.LANCZOS).save(out.replace('.png', '-320.png'))
print(out, name, size, len(lines), 'line(s)')
