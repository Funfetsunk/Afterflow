"""Draw the 16-bit shrine designs pixel by pixel in the Afterflow v1 palette.

Shrines are the world's mind keeping Awa alive (GDD), so they should look a
little too clean and too advanced for the countryside: smooth machined stone
with a cold pale glow, half reclaimed by moss. PixelLab kept washing this out
(no outlines, pale blobs), so the designs are drawn here instead, following the
Art Bible rules: 2e222f outlines, 2-3 tones per material, light from the top
left, front-facing (top faces seen as a band), a cast shadow down and to the
right on the grass.

  monolith  dark slate obelisk with bevelled top, glowing seam and round core
  ring      pale stone ring on its neck, a glowing orb floating in the middle

Both stand on the same two-tier plinth with a glowing groove. Glow colours are
8fd3ff/ffffff; in Godot a 2D light adds the real glow.

Run from the project root:
    python tools/kits/make_shrine16.py
Writes art/final/shrine/obj_shrine16_{monolith,ring}.png (then tools/make_stamp.py).
"""

import math
import random
from pathlib import Path

from PIL import Image

W, H = 32, 46
OUT = Path("art/final/shrine")

C = {k: tuple(int(v[i:i + 2], 16) for i in (0, 2, 4)) + (255,) for k, v in {
    "out": "2e222f", "white": "ffffff", "pale": "c7dcd0", "stone": "9babb2", "stone_d": "7f708a",
    "slate_l": "7f708a", "slate": "625565", "slate_d": "3e3546", "glow": "8fd3ff", "glow_d": "4d9be6",
    "moss": "374e4a", "moss_l": "676633", "shadow": "374e4a", "tuft": "313638",
}.items()}


def rect(px, x0, y0, x1, y1, col):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px[x, y] = C[col]


def box(px, x0, y0, x1, y1, top_rows):
    """A front-facing block: pale top face, stone front darkening to the right, outlined."""
    rect(px, x0, y0, x1, y1, "out")
    rect(px, x0 + 1, y0 + 1, x1 - 1, y0 + top_rows, "pale")
    rect(px, x0 + 1, y0 + top_rows + 1, x1 - 1, y1 - 1, "stone")
    rect(px, x1 - 3, y0 + top_rows + 1, x1 - 1, y1 - 1, "stone_d")
    for x in range(x0 + 1, x1):                     # crisp edge between top and front
        px[x, y0 + top_rows + 1] = C["white"] if x < x0 + 4 else px[x, y0 + top_rows + 1]


def plinth(px):
    box(px, 3, 37, 28, 44, 2)                       # lower tier
    for x in range(6, 26, 3):                       # glowing groove along the front
        px[x, 42] = C["glow"]
        px[x + 1, 42] = C["glow"]
    box(px, 7, 33, 24, 37, 1)                       # upper tier (overlaps the lower's top)
    rect(px, 8, 37, 23, 37, "out")


def monolith(px):
    x0, x1, y0, y1 = 10, 21, 4, 33
    rect(px, x0, y0 + 3, x1, y1, "out")
    for k in range(3):                              # bevelled top
        rect(px, x0 + 3 - k, y0 + k, x1 - 3 + k, y0 + k, "out")
    for y in range(y0 + 1, y1):
        inset = max(0, 3 - (y - y0)) + 1
        for x in range(x0 + inset, x1 - inset + 1):
            col = "slate"
            if x <= x0 + inset:
                col = "slate_l"                     # lit left edge
            elif x >= x1 - inset - 2:
                col = "slate_d"                     # shaded right face
            px[x, y] = C[col]
    rect(px, x0 + 3, y0 + 1, x1 - 3, y0 + 2, "slate_l")    # lit bevel on top
    for y in range(y0 + 10, y1 - 2):                # the seam
        px[15, y] = C["glow"]
        px[16, y] = C["glow_d"]
    cx, cy = 15.5, y0 + 9                           # the core
    for y in range(y0 + 5, y0 + 14):
        for x in range(x0 + 1, x1):
            d = math.hypot(x - cx, y - cy)
            if d < 1.6:
                px[x, y] = C["white"]
            elif d < 2.8:
                px[x, y] = C["glow"]
            elif d < 3.6:
                px[x, y] = C["out"]


def ring(px):
    cx, cy, r_out, r_in = 15.5, 17.5, 11.5, 7.2
    rect(px, 13, 28, 18, 33, "out")                 # the neck
    rect(px, 14, 28, 17, 33, "stone")
    px[14, 29] = px[14, 30] = C["pale"]
    px[17, 29] = px[17, 30] = C["stone_d"]
    for y in range(H):
        for x in range(W):
            d = math.hypot(x - cx, y - cy)
            if r_in - 1 <= d <= r_out:
                edge = d > r_out - 1 or d < r_in
                if edge:
                    px[x, y] = C["out"]
                    continue
                # light from the top left: the band's outer top-left is pale, inner bottom-right dark
                lit = ((cx - x) + (cy - y)) / (d or 1)
                if lit > 0.8 and d > (r_in + r_out) / 2:
                    px[x, y] = C["white"]
                elif lit > 0.2:
                    px[x, y] = C["pale"]
                elif lit > -0.7:
                    px[x, y] = C["stone"]
                else:
                    px[x, y] = C["stone_d"]
    for y in range(H):                              # floating orb
        for x in range(W):
            d = math.hypot(x - cx, y - cy)
            if d < 1.5:
                px[x, y] = C["white"]
            elif d < 2.6:
                px[x, y] = C["glow"]
            elif d < 3.3:
                px[x, y] = C["glow_d"]
    for x, y in ((15, 12), (20, 17), (11, 18), (16, 23)):     # faint motes inside the ring
        px[x, y] = C["glow"]


def overgrow(px, rng):
    """Moss creeping over the plinth's bottom corners and tufts at its foot."""
    for x0, y0, w in ((4, 38, 6), (22, 38, 4), (8, 34, 3)):   # clumps draped over tier edges
        for dx in range(w):
            depth = rng.choice((1, 2, 2, 3)) if 0 < dx < w - 1 else 1
            for dy in range(depth):
                x, y = x0 + dx, y0 + dy
                if px[x, y][3] and px[x, y] not in (C["glow"], C["glow_d"]):
                    px[x, y] = C["moss_l"] if dy == 0 else C["moss"]
    for x in (3, 7, 12, 20, 26):                    # grass tufts growing up over the plinth foot
        for dx, h in ((0, 2), (1, 3), (2, 2)):
            for y in range(45 - h, 45):
                px[x + dx, y] = C["moss"] if y < 44 else C["tuft"]


def with_shadow(img):
    """Cast shadow down and to the right from the lower part of the silhouette."""
    out = Image.new("RGBA", (img.width + 2, img.height + 1), (0, 0, 0, 0))
    mask = img.getchannel("A")
    mp = mask.load()
    for y in range(int(img.height * 0.4)):
        for x in range(img.width):
            mp[x, y] = 0
    out.paste(Image.new("RGBA", img.size, C["shadow"]), (2, 1), mask)
    out.alpha_composite(img)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, draw in (("monolith", monolith), ("ring", ring)):
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        px = img.load()
        plinth(px)
        draw(px)
        overgrow(px, random.Random(f"shrine-{name}"))
        img = with_shadow(img.crop(img.getchannel("A").getbbox()))
        path = OUT / f"obj_shrine16_{name}.png"
        img.save(path)
        print(path, img.size)


if __name__ == "__main__":
    main()
