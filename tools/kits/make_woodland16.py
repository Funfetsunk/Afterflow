"""Draw the Phase 2 woodland and dungeon sprites pixel by pixel in the palette.

Same rules as make_creature16.py (Art Bible §7): creatures are made of their
biome's material and share one large white eye with a dark pupil; outlines are
2e222f, light comes from the top left, bodies contrast with the ground (the
woodland floor is dark leaf litter, so the barkling is pale bark with a mossy cap).

  barkling_{s,e,n,w}          24x24  woodland creature (charges in a line)
  warden_{idle,raise,dazed}   48x48  the hollow oak's guardian (boss), facing the camera
  door_locked, door_boss      32x32  dungeon doors (2x2 cells) set into the root walls
  ts_wood_leaves_fill_0..5    16x16  leaf-litter fill variants (the Wang sheet's own full
                                     tile repeats as a visible dot grid)

Run from the project root:
    python tools/kits/make_woodland16.py
Writes art/final/enm/*.png and art/final/dungeon/*.png.
"""

import math
from pathlib import Path

from PIL import Image

P = {k: tuple(int(v[i:i + 2], 16) for i in (0, 2, 4)) + (255,) for k, v in {
    "out": "2e222f", "bark": "4c3e24", "brown": "966c6c", "stone": "ab947a", "moss": "374e4a",
    "grass": "547e64", "olive": "676633", "lime": "d5e04b", "white": "ffffff", "rim": "c7dcd0",
    "plum": "3e3546", "slate": "625565", "gold": "fbb954", "amber": "e6904e", "pale": "c7dcd0",
    "deep": "313638", "rust": "cd683d", "amber2": "9e4539",
}.items()}


def canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def ellipse(px, cx, cy, rx, ry, col, w, h):
    for y in range(h):
        for x in range(w):
            if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                px[x, y] = P[col]


def outline(img):
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


def eye(px, ex, ey, r, pupil_dx=0, closed=False):
    """The family signature: a large white eye with a pale rim and a dark pupil."""
    for y in range(int(ey - r - 2), int(ey + r + 2)):
        for x in range(int(ex - r - 2), int(ex + r + 2)):
            d = math.hypot(x + 0.5 - ex, y + 0.5 - ey)
            if closed:
                if abs(y + 0.5 - ey) < 0.8 and d <= r:
                    px[x, y] = P["out"]
                continue
            if d <= r - 0.8:
                px[x, y] = P["white"]
            elif d <= r + 0.2:
                px[x, y] = P["rim"]
            elif d <= r + 1.1:
                px[x, y] = P["out"]
    if not closed:
        pr = max(1, int(r / 2.5))
        for y in range(pr + 1):
            for x in range(pr + 1):
                px[int(ex + pupil_dx - pr / 2) + x, int(ey - pr / 2) + y] = P["out"]


def shadow(img, cx, cy, rx, ry):
    out = canvas(*img.size)
    ellipse(out.load(), cx, cy, rx, ry, "moss", *img.size)
    out.alpha_composite(img)
    return out


# --- barkling -----------------------------------------------------------------

def barkling(direction):
    img = canvas(24, 24)
    px = img.load()
    x0, x1, y0, y1 = 6, 17, 8, 19
    for y in range(y0, y1 + 1):                          # stump body, pale bark with grooves
        for x in range(x0, x1 + 1):
            if (x in (x0, x1)) and y in (y0, y1):
                continue
            col = "stone" if x < x0 + 3 else "brown" if x < x1 - 2 else "bark"
            if (x - x0) % 4 == 2 and y > y0 + 2:
                col = "bark" if col != "bark" else "plum"
            px[x, y] = P[col]
    ellipse(px, 11.9, 8.5, 6.4, 2.6, "grass", 24, 24)    # mossy cap
    for x, y in ((8, 8), (10, 7), (14, 8), (12, 9)):
        px[x, y] = P["olive"]
    px[9, 7] = P["lime"]
    for k in range(4):                                   # twig horns
        px[7 - k // 2, 6 - k] = P["bark"]
        px[16 + k // 2, 6 - k] = P["bark"]
    px[5, 3], px[18, 3] = P["bark"], P["bark"]
    for fx in (7, 14):                                   # root feet
        for x in range(fx, fx + 3):
            px[x, 20] = P["bark"]
    if direction == "s":
        eye(px, 11.9, 13.5, 3.0)
    elif direction == "e":
        eye(px, 14.5, 13.5, 2.6, pupil_dx=1)
    elif direction == "w":
        eye(px, 9.5, 13.5, 2.6, pupil_dx=-1)
    img = outline(img)
    return shadow(img, 12, 21, 7, 1.8)


# --- the warden (boss) ------------------------------------------------------------

def warden(pose):
    img = canvas(48, 48)
    px = img.load()
    lift = {"idle": 0, "raise": -4, "dazed": 3}[pose]
    ellipse(px, 24, 30 + lift / 2, 13, 12, "brown", 48, 48)          # hunched bark body
    for y in range(18, 44):                                          # bark grooves, shaded right
        for x in range(10, 39):
            if px[x, y][3]:
                if x > 29:
                    px[x, y] = P["bark"]
                elif x < 17:
                    px[x, y] = P["stone"]
                if (x + y // 3) % 6 == 0:
                    px[x, y] = P["bark"]
    ellipse(px, 23, 19 + lift, 12, 6, "moss", 48, 48)                # moss mantle over the shoulders
    ellipse(px, 21, 17 + lift, 8, 3.5, "grass", 48, 48)
    for x, y in ((16, 17), (19, 15), (24, 16), (27, 18), (14, 20)):
        px[x, y + lift] = P["olive"]
    arm_y = {"idle": 30, "raise": 14, "dazed": 36}[pose]            # long root arms
    for side in (-1, 1):
        sx = 24 + side * 12
        for t in range(14):
            x = sx + side * (t // 2)
            y = int(26 + (arm_y - 26) * t / 13) + (t % 3 == 0)
            for w in range(2):
                if 0 <= x + w * side < 48 and 0 <= y < 48:
                    px[x + w * side, y] = P["bark"]
        for k in range(3):                                           # root fingers
            fx, fy = sx + side * 7 + side * k, arm_y + 1 + (k % 2)
            if 0 <= fx < 48 and 0 <= fy < 48:
                px[fx, fy] = P["bark"]
    for fx in (15, 20, 28, 33):                                      # feet roots
        for y in range(42, 45):
            px[fx, y] = P["bark"]
            px[fx + 1, y] = P["bark"]
    eye(px, 24, 28 + lift, 5.2, closed=(pose == "dazed"))
    img = outline(img)
    return shadow(img, 24, 45, 17, 3)


# --- dungeon doors ------------------------------------------------------------------

def door(kind):
    img = canvas(32, 32)
    px = img.load()
    for y in range(32):                                  # root frame
        for x in range(32):
            if x < 3 or x > 28 or y < 3:
                px[x, y] = P["bark"] if (x + y) % 5 else P["brown"]
    for y in range(3, 32):                               # planks
        for x in range(3, 29):
            plank = (x - 3) // 6
            col = "brown" if plank % 2 == 0 else "stone"
            if (x - 3) % 6 == 0:
                col = "bark"
            px[x, y] = P[col]
    for y in (9, 24):                                    # iron bands
        for x in range(3, 29):
            px[x, y] = P["slate"]
            px[x, y + 1] = P["plum"]
    if kind == "locked":
        for y in range(15, 21):                          # keyhole plate
            for x in range(13, 19):
                px[x, y] = P["gold"] if (x, y) not in ((13, 15), (18, 15), (13, 20), (18, 20)) else P["brown"]
        px[15, 17], px[16, 17], px[15, 18], px[16, 18], px[15, 19] = (P["out"],) * 5
    else:                                                # the boss door: the spiral-eye mark carved in
        for t in range(0, 360 * 2, 5):
            r = 2 + t / 110
            a = math.radians(t)
            x, y = int(16 + math.cos(a) * r), int(18 + math.sin(a) * r)
            if 3 <= x < 29 and 3 <= y < 32:
                px[x, y] = P["pale"]
        eye(px, 16, 18, 2.2)
    for x in range(32):
        px[x, 0] = P["out"]
    for y in range(32):
        px[0, y] = P["out"]
        px[31, y] = P["out"]
    return img


def leaf_fill(seed):
    import random
    rng = random.Random(f"leaves-{seed}")
    img = Image.new("RGBA", (16, 16), P["bark"])
    px = img.load()
    leaf_cols = ["rust", "rust", "amber2", "olive", "brown"]
    for _ in range(9):                                   # scattered fallen leaves, 2-3 px each
        x, y = rng.randrange(16), rng.randrange(16)
        col = P[rng.choice(leaf_cols)]
        for dx, dy in rng.choice((((0, 0), (1, 0)), ((0, 0), (0, 1)), ((0, 0), (1, 0), (1, 1)))):
            px[(x + dx) % 16, (y + dy) % 16] = col
    for _ in range(6):                                   # dark gaps between the leaves
        x, y = rng.randrange(16), rng.randrange(16)
        px[x, y] = P["deep"]
    return img


def main():
    for i in range(6):
        leaf_fill(i).save(f"art/final/ts_wood_leaves_fill_{i}.png")
    enm, dun = Path("art/final/enm"), Path("art/final/dungeon")
    enm.mkdir(parents=True, exist_ok=True)
    dun.mkdir(parents=True, exist_ok=True)
    for d in "senw":
        barkling(d).save(enm / f"barkling_{d}.png")
    for pose in ("idle", "raise", "dazed"):
        warden(pose).save(enm / f"warden_{pose}.png")
    door("locked").save(dun / "door_locked.png")
    door("boss").save(dun / "door_boss.png")
    print("barkling x4, warden x3, doors x2")


if __name__ == "__main__":
    main()
