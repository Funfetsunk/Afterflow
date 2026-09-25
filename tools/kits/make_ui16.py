"""Draw the Phase 2 UI, pickup and effect sprites pixel by pixel in the palette.

Small, flat, readable pieces where PixelLab is weakest (Art Bible §3.1: draw in
code). Every colour is an Afterflow v1 palette colour; outlines are 2e222f,
light comes from the top left.

  HUD      leaf_full / leaf_wilted / leaf_empty (health leaves on the sprig),
           sprig_end, item_frame, key_icon
  items    lantern (icon and pickup), key, heart_leaf, torn_page
  panels   panel_dialogue (9-slice, 24x24, 8px margins), panel_diary (9-slice)
  effects  slash_0..2 (the stick's arc, facing east; rotated in-engine),
           spin_0..3, hit_spark, poof_0..2, faded_mark (lantern-revealed writing)

Run from the project root:
    python tools/kits/make_ui16.py
Writes art/final/ui/*.png (tools/export_assets.py copies them to assets/ui/).
"""

import math
from pathlib import Path

from PIL import Image

OUT = Path("art/final/ui")
P = {k: tuple(int(v[i:i + 2], 16) for i in (0, 2, 4)) + (255,) for k, v in {
    "out": "2e222f", "plum": "3e3546", "slate": "625565", "mauve": "7f708a",
    "moss": "374e4a", "grass": "547e64", "olive": "676633", "lime": "d5e04b",
    "bark": "4c3e24", "brown": "966c6c", "stone": "ab947a", "cream": "fdcbb0", "peach": "fca790",
    "gold": "fbb954", "amber": "e6904e", "rust": "cd683d", "white": "ffffff", "pale": "c7dcd0",
    "grey": "9babb2", "cyan": "8fd3ff",
}.items()}
CLEAR = (0, 0, 0, 0)


def canvas(w, h):
    return Image.new("RGBA", (w, h), CLEAR)


def draw(img, rows, key):
    """Paint an ASCII picture: each char maps to a palette name via key ('.' = clear)."""
    px = img.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != "." and ch in key:
                px[x, y] = P[key[ch]]
    return img


def outline(img):
    """Add a 2e222f outline around every opaque pixel."""
    src = img.copy()
    s, d = src.load(), img.load()
    for y in range(img.height):
        for x in range(img.width):
            if s[x, y][3]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < img.width and 0 <= ny < img.height and s[nx, ny][3] and s[nx, ny] != P["out"]:
                    d[x, y] = P["out"]
                    break
    return img


LEAF = [
    "....aa...",
    "...aabb..",
    "..aabbbb.",
    ".aabbvbbb",
    ".abbvbbbb",
    "abbvbbbbc",
    "abvbbbbc.",
    ".vbbbcc..",
    "v.ccc....",
]


def leaf(light, base, dark, vein):
    return outline(draw(canvas(11, 11).crop((0, 0, 11, 11)), [" " + r for r in [""] + LEAF],
                        {"a": light, "b": base, "c": dark, "v": vein}))


def item_frame():
    img = canvas(22, 22)
    px = img.load()
    for y in range(22):
        for x in range(22):
            corner = (x in (0, 21) and y in (0, 21))
            if corner:
                continue
            edge = x in (0, 21) or y in (0, 21)
            inner = x in (1, 20) or y in (1, 20)
            px[x, y] = P["out"] if edge else P["slate"] if inner else P["plum"]
    return img


LANTERN = [
    "....oooo....",
    "...o....o...",
    "..bbbbbbbb..",
    "..bggggggb..",
    "..bgwyyagb..",
    "..bgyyyagb..",
    "..bgyyaagb..",
    "..bgaaaagb..",
    "..bggggggb..",
    "..bbbbbbbb..",
    "...bbbbbb...",
]


def lantern():
    return outline(draw(canvas(14, 14), ["." + r for r in [""] + LANTERN],
                        {"o": "bark", "b": "bark", "g": "brown", "w": "white", "y": "gold", "a": "amber"}))


KEY = [
    ".ggg......",
    "gg.gg.....",
    "g...gggggg",
    "gg.gg..g.g",
    ".ggg......",
]


def key_sprite():
    img = draw(canvas(12, 9), ["." * 12, ".." + KEY[0], ".." + KEY[1], ".." + KEY[2], ".." + KEY[3], ".." + KEY[4]],
               {"g": "gold"})
    px = img.load()
    for x in range(2, 12):                               # shade the underside
        for y in range(img.height - 1, -1, -1):
            if px[x, y][3]:
                px[x, y] = P["amber"]
                break
    return outline(img)


def heart_leaf():
    base = leaf("lime", "olive", "moss", "moss")
    img = canvas(13, 13)
    img.alpha_composite(base, (1, 1))
    px = img.load()
    for x, y in ((2, 2), (11, 3), (1, 10)):              # a faint glint of life around it
        px[x, y] = P["lime"]
    return img


def torn_page():
    img = canvas(12, 12)
    px = img.load()
    for y in range(1, 11):
        for x in range(2, 10):
            if (x + y) % 7 == 0 and y in (1, 10):         # torn edges
                continue
            px[x, y] = P["cream"]
    for y in (3, 5, 7):
        for x in range(3, 8 + (y % 2)):
            px[x, y] = P["brown"]
    for y in range(1, 11):                              # the tear down the right side
        px[9 + (y % 2), y] = P["peach"]
    return outline(img)


def panel(fill, border, light):
    """9-slice panel, 24x24 with 8px margins: outline, border band, inner light line."""
    img = canvas(24, 24)
    px = img.load()
    for y in range(24):
        for x in range(24):
            d = min(x, y, 23 - x, 23 - y)
            if d == 0 and (x in (0, 23) and y in (0, 23)):
                continue
            if d == 0:
                px[x, y] = P["out"]
            elif d == 1:
                px[x, y] = P[border]
            elif d == 2:
                px[x, y] = P[light] if (x < 12 or y < 12) else P[border]
            else:
                px[x, y] = P[fill]
    return img


def arc_frames(radius, width, spans, colours):
    """The stick's swing: a crescent sweeping clockwise through `spans` (degrees), facing east."""
    frames = []
    size = radius * 2 + 4
    c = size / 2
    for a0, a1 in spans:
        img = canvas(size, size)
        px = img.load()
        for y in range(size):
            for x in range(size):
                d = math.hypot(x + 0.5 - c, y + 0.5 - c)
                ang = math.degrees(math.atan2(y + 0.5 - c, x + 0.5 - c))
                if a0 <= ang <= a1 and radius - width <= d <= radius:
                    px[x, y] = P[colours[0] if d > radius - 1.5 else colours[1]]
        frames.append(img)
    return frames


def spin_frames():
    frames = []
    for k in range(4):
        start = -180 + k * 90
        frames += arc_frames(13, 4, [(start, start + 160)], ("white", "pale"))
    return frames


def hit_spark():
    img = canvas(9, 9)
    px = img.load()
    for i in range(9):
        px[4, i] = P["white"]
        px[i, 4] = P["white"]
    for i in (2, 6):
        px[i, i] = P["pale"]
        px[i, 8 - i] = P["pale"]
    return img


def poof_frames():
    frames = []
    for r in (3, 5, 7):
        img = canvas(18, 18)
        px = img.load()
        for k in range(8):
            ang = k * math.pi / 4 + r * 0.2
            x, y = int(9 + math.cos(ang) * r), int(9 + math.sin(ang) * r)
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                if 0 <= x + dx < 18 and 0 <= y + dy < 18:
                    px[x + dx, y + dy] = P["pale"] if r < 7 else P["grey"]
        frames.append(img)
    return frames


def faded_mark():
    """A carved spiral with an eye at its heart: the recurring symbol, revealed by lantern light."""
    img = canvas(16, 16)
    px = img.load()
    for t in range(0, 360 * 2, 6):
        r = 1.5 + t / 130
        a = math.radians(t)
        x, y = int(8 + math.cos(a) * r), int(8 + math.sin(a) * r)
        if 0 <= x < 16 and 0 <= y < 16:
            px[x, y] = P["pale"]
    px[8, 8] = P["white"]
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sprites = {
        "leaf_full": leaf("lime", "olive", "moss", "moss"),
        "leaf_wilted": leaf("stone", "brown", "bark", "bark"),
        "leaf_empty": leaf("plum", "plum", "plum", "slate"),
        "item_frame": item_frame(),
        "lantern": lantern(),
        "key": key_sprite(),
        "heart_leaf": heart_leaf(),
        "torn_page": torn_page(),
        "panel_dialogue": panel("out", "slate", "mauve"),
        "panel_diary": panel("cream", "brown", "white"),
        "hit_spark": hit_spark(),
        "faded_mark": faded_mark(),
    }
    for i, f in enumerate(arc_frames(12, 4, [(-100, -40), (-70, 20), (-20, 80)], ("white", "pale"))):
        sprites[f"slash_{i}"] = f
    for i, f in enumerate(spin_frames()):
        sprites[f"spin_{i}"] = f
    for i, f in enumerate(poof_frames()):
        sprites[f"poof_{i}"] = f
    for name, img in sprites.items():
        img.save(OUT / f"{name}.png")
    print(f"{len(sprites)} sprites -> {OUT}")


if __name__ == "__main__":
    main()
