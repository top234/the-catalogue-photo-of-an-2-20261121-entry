#!/usr/bin/env python3
"""Generate entry.png — The Pocket Cloud Maker (NIMBUS-1).
Deterministic, seeded, no time/date in output. PIL only."""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
random.seed(20261121)

img = Image.new("RGB", (W, H))
px = img.load()
# vertical background gradient: light grey studio
for y in range(H):
    t = y / (H - 1)
    r = int(232 - 14 * t)
    g = int(232 - 14 * t)
    b = int(234 - 12 * t)
    for x in range(W):
        px[x, y] = (r, g, b)
d = ImageDraw.Draw(img, "RGBA")

# floor: slightly darker band + soft horizon line
d.rectangle([0, 782, W, H], fill=(203, 203, 206))
d.line([0, 782, W, 782], fill=(185, 185, 189), width=2)

# ---- soft shadow layer ----
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([250, 748, 700, 812], fill=(0, 0, 0, 90))
sd.ellipse([660, 762, 800, 800], fill=(0, 0, 0, 60))
shadow = shadow.filter(ImageFilter.GaussianBlur(18))
img.paste(shadow, (0, 0), shadow)
d = ImageDraw.Draw(img, "RGBA")

# ---- cloud (drawn first so nozzle sits under it) ----
cloud_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(cloud_layer)
# grey underside puffs, then white tops
puffs = [(380, 305, 95), (450, 265, 110), (530, 275, 100), (580, 325, 80),
         (410, 355, 85), (490, 345, 105), (560, 370, 75), (340, 350, 65)]
for (cx, cy, r) in puffs:
    cd.ellipse([cx - r, cy - r + 14, cx + r, cy + r + 14], fill=(176, 182, 190, 255))
for (cx, cy, r) in puffs:
    cd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 255))
# soft highlight blobs
for (cx, cy, r) in [(450, 260, 55), (530, 270, 50), (400, 305, 45)]:
    cd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 255))
cloud_layer = cloud_layer.filter(ImageFilter.GaussianBlur(3))
img.paste(cloud_layer, (0, 0), cloud_layer)
d = ImageDraw.Draw(img, "RGBA")
# small rain dots under cloud (3 tiny drops, hint of the joke's rain)
for (x, y) in [(400, 448), (520, 452)]:
    d.ellipse([x - 4, y - 6, x + 4, y + 6], fill=(140, 170, 205, 220))

# ---- device body: brushed steel ----
bx0, by0, bx1, by1 = 300, 560, 620, 760
# vertical metallic gradient strips
for x in range(bx0, bx1):
    t = (x - bx0) / (bx1 - bx0)
    v = int(168 + 55 * math.sin(t * math.pi) + 18 * math.sin(t * 9.0))
    v = max(150, min(235, v))
    d.line([x, by0, x, by1], fill=(v, v + 2, v + 6))
# rounded outline + top/bottom edges
d.rounded_rectangle([bx0, by0, bx1, by1], radius=28, outline=(90, 92, 98), width=3)
d.line([bx0 + 28, by0 + 2, bx1 - 28, by0 + 2], fill=(245, 246, 248), width=3)
d.line([bx0 + 28, by1 - 2, bx1 - 28, by1 - 2], fill=(110, 112, 118), width=3)
# brushed-metal horizontal streaks
for i in range(26):
    y = by0 + 18 + i * 7
    x0 = bx0 + 14 + random.randint(0, 60)
    x1 = min(bx1 - 14, x0 + random.randint(60, 200))
    d.line([x0, y, x1, y], fill=(255, 255, 255, 28), width=1)
# recessed front panel
d.rounded_rectangle([330, 600, 590, 720], radius=16, outline=(120, 122, 128), width=2)
# small dial + indicator light
d.ellipse([360, 640, 396, 676], outline=(80, 82, 88), width=3, fill=(210, 212, 216))
d.line([378, 658, 390, 646], fill=(70, 72, 78), width=3)
d.ellipse([540, 648, 556, 664], fill=(90, 160, 120))
# brand text on body
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
    font_s = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
except Exception:
    font = ImageFont.load_default()
    font_s = font
d.text((460, 682), "NIMBUS-1", font=font, fill=(60, 62, 68), anchor="mm")
d.text((460, 706), "POCKET CLOUD MAKER", font=font_s, fill=(110, 112, 118), anchor="mm")

# ---- brass nozzle ----
nx0, nx1 = 432, 488
d.rectangle([nx0, 500, nx1, 562], fill=(176, 138, 62))
d.rectangle([nx0, 500, nx0 + 10, 562], fill=(214, 178, 96))
d.rectangle([nx1 - 10, 500, nx1, 562], fill=(128, 96, 40))
d.rectangle([420, 488, 500, 506], fill=(198, 158, 80), outline=(120, 90, 38))
d.rectangle([420, 488, 432, 506], fill=(228, 196, 116))
d.ellipse([428, 478, 492, 494], fill=(214, 178, 96), outline=(120, 90, 38))
# nozzle tip opening (dark)
d.ellipse([446, 480, 474, 490], fill=(70, 52, 22))
# thin vapour wisp from nozzle to cloud
wisp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
wd = ImageDraw.Draw(wisp)
wd.line([460, 478, 452, 440, 462, 410], fill=(255, 255, 255, 170), width=7)
wisp = wisp.filter(ImageFilter.GaussianBlur(4))
img.paste(wisp, (0, 0), wisp)
d = ImageDraw.Draw(img, "RGBA")

# ---- umbrella accessory (right side) ----
ux = 720
# canopy: red arc
d.pieslice([ux - 78, 560, ux + 78, 700], start=180, end=360, fill=(178, 52, 52))
d.pieslice([ux - 78, 560, ux + 78, 700], start=180, end=360, outline=(120, 30, 30), width=3)
# canopy ribs
for ang in (200, 225, 250, 270, 290, 315, 340):
    a = math.radians(ang)
    d.line([ux, 630, ux + 78 * math.cos(a), 630 + 70 * math.sin(a)], fill=(140, 38, 38), width=2)
# scalloped edge
for cx in range(ux - 78, ux + 79, 26):
    d.ellipse([cx - 13, 622, cx + 13, 642], fill=(178, 52, 52))
# tip
d.line([ux, 552, ux, 568], fill=(90, 90, 90), width=4)
d.ellipse([ux - 4, 546, ux + 4, 556], fill=(90, 90, 90))
# stick + J handle
d.line([ux, 630, ux, 748], fill=(96, 70, 46), width=5)
d.arc([ux - 14, 734, ux + 14, 766], start=0, end=180, fill=(96, 70, 46), width=5)

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
