"""Draw the meadow creature (enm_meadow01) pixel by pixel in the Afterflow v1 palette.

The world's creatures are its white blood cells, made from each biome's own
materials, with one shared signature so players read them as a family (GDD §8,
Art Bible §7). The meadow one is almost cute: a round ball of moss with a
two-leaf sprout and a pale petal, stubby feet, and a single large white eye,
the family signature. PixelLab's attempts came out muddy (yellow blotches, messy
eye), so it is drawn here, following the Art Bible rules: 2e222f outlines,
olive moss lit from the top left (d5e04b crown / 676633 / 374e4a), so it stands out from the 547e64 grass, a soft 374e4a shadow.

Two eye styles for the signature:
  pupil  white eye, c7dcd0 rim, small dark pupil: cute, alive
  blank  white eye, c7dcd0 rim, no pupil: blank and faintly strange

Run from the project root:
    python tools/kits/make_creature16.py
Writes art/final/enm/enm_meadow01_<eye>_{s,e,n,w}.png (24x24 frames).
"""

import math
from pathlib import Path

from PIL import Image

S = 24
OUT = Path("art/final/enm")
C = {k: tuple(int(v[i:i + 2], 16) for i in (0, 2, 4)) + (255,) for k, v in {
    "out": "2e222f", "shine": "d5e04b", "lit": "676633", "moss": "676633", "dark": "374e4a", "deep": "313638",
    "white": "ffffff", "rim": "c7dcd0", "petal": "fdcbb0", "petal_d": "fca790", "leaf": "547e64", "sprout_l": "547e64",
}.items()}
CX, CY, RX, RY = 11.5, 13.5, 7.6, 6.8          # body ellipse


def body(px):
    for y in range(S):
        for x in range(S):
            d = ((x - CX) / RX) ** 2 + ((y - CY) / RY) ** 2
            if d <= 1:
                # top-left light: lit crown, base moss, dark lower right
                lit = (CX - x) / RX + (CY - y) / RY
                col = "shine" if lit > 1.45 else "dark" if lit < -0.7 else "moss"
                px[x, y] = C[col]
    for y in range(S):                          # outline: any empty pixel touching the body
        for x in range(S):
            if px[x, y][3] == 0 and any(
                    0 <= x + dx < S and 0 <= y + dy < S and px[x + dx, y + dy][3] and px[x + dx, y + dy] != C["out"]
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = C["out"]
    for x, y in ((6, 11), (9, 9), (14, 17), (16, 12), (8, 16)):   # moss texture flecks
        if px[x, y] in (C["moss"], C["lit"]):
            px[x, y] = C["dark"]


def feet(px):
    for fx in (7, 14):
        for x in range(fx, fx + 3):
            px[x, 20] = C["deep"]
            px[x, 21] = C["out"]
        px[fx - 1, 20] = px[fx + 3, 20] = C["out"]


def sprout(px, back=False):
    for y in (4, 5, 6):                          # stem
        px[11, y] = C["dark"]
    for x, y in ((8, 3), (9, 3), (9, 4), (10, 4)):          # left leaf
        px[x, y] = C["shine"]
    for x, y in ((12, 2), (13, 2), (13, 3), (14, 3), (12, 3)):   # right leaf
        px[x, y] = C["moss"]
    for x, y in ((7, 3), (8, 2), (9, 2), (10, 3), (11, 3), (8, 4), (11, 2), (12, 1), (13, 1), (14, 2),
                 (15, 3), (14, 4), (13, 4), (10, 5), (12, 5), (12, 6), (10, 6)):
        if px[x, y][3] == 0:
            px[x, y] = C["out"]
    px_petal = [(15, 8), (16, 8), (16, 7)] if not back else [(6, 8), (7, 8), (7, 7)]
    for i, (x, y) in enumerate(px_petal):        # one pale petal caught in the moss
        px[x, y] = C["petal"] if i < 2 else C["petal_d"]


def eye(px, ex, ey, pupil, squash=1.0):
    for y in range(S):
        for x in range(S):
            d = math.hypot((x - ex) / squash, y - ey)
            if d < 2.3:
                px[x, y] = C["white"]
            elif d < 3.2:
                px[x, y] = C["rim"]
            elif d < 3.9 and px[x, y] != C["out"] and px[x, y][3]:
                px[x, y] = C["out"]
    if pupil:
        for dx, dy in ((0, 0), (0, 1)) if squash != 1 else ((0, 0), (1, 0), (0, 1), (1, 1)):
            px[int(ex) + dx, int(ey) + dy] = C["out"]
    px[int(ex) - 1, int(ey) - 2] = C["white"]    # catch-light stays white


def shadow(img):
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    px = out.load()
    for y in range(19, 23):
        for x in range(S):
            if ((x - 12.5) / 8.5) ** 2 + ((y - 21) / 1.8) ** 2 <= 1:
                px[x, y] = C["dark"]
    out.alpha_composite(img)
    return out


def frame(direction, pupil):
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    px = img.load()
    body(px)
    feet(px)
    sprout(px, back=direction == "n")
    if direction == "s":
        eye(px, 11.5, 13.0, pupil)
    elif direction == "e":
        eye(px, 15.0, 13.0, pupil, squash=0.75)
    img = shadow(img)
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for style, pupil in (("pupil", True), ("blank", False)):
        for d in "sen":
            frame(d, pupil).save(OUT / f"enm_meadow01_{style}_{d}.png")
        frame("e", pupil).transpose(Image.FLIP_LEFT_RIGHT).save(OUT / f"enm_meadow01_{style}_w.png")
    print(f"8 frames -> {OUT}")


if __name__ == "__main__":
    main()
