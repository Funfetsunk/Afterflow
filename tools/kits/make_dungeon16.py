"""Draw the hollow-oak dungeon kit and the oak's entrance, pixel by pixel in the palette.

PixelLab's root-wall tileset came back almost black, with carvings that read as
windows, so the kit is drawn here (Art Bible §3.1: draw in code). Readability
first, like 16-bit dungeons: a lighter warm earth floor, dark tangled root
walls, and a lit wall face along the north wall. Outlines 2e222f, light from
the top left.

Tiles (16x16, art/final/tiles/dungeon16/, index tools/kits/dungeon16.json):
  floor_0..3         packed earth with pale root bits (variants)
  floor_shadow       floor under the north wall's face (shadow along the top)
  wall_top           the dark mass of roots (any wall seen from above)
  wall_face          the north wall's face, one tile tall, below wall_top
  wall_edge_l/r/t    wall_top with a lit rim where it meets the floor
                     (left wall's east rim = edge_r, right wall's = edge_l,
                     south wall's north rim = edge_t)
Stamp:
  art/final/obj_hollow_oak.png   80x80, the great oak's trunk with its doorway
                                 (5x5 cells; make_stamp.py ... hollow_oak --left)

Run from the project root:
    python tools/kits/make_dungeon16.py
"""

import json
import random
from pathlib import Path

from PIL import Image

T = 16
OUT = Path("art/final/tiles/dungeon16")
P = {k: tuple(int(v[i:i + 2], 16) for i in (0, 2, 4)) + (255,) for k, v in {
    "out": "2e222f", "plum": "3e3546", "deep": "313638", "bark": "4c3e24", "brown": "966c6c",
    "stone": "ab947a", "slate": "625565", "moss": "374e4a", "grass": "547e64", "olive": "676633",
    "cream": "fdcbb0",
}.items()}


def tile():
    return Image.new("RGBA", (T, T), P["brown"])


def floor(seed):
    rng = random.Random(f"floor-{seed}")
    img = tile()
    px = img.load()
    for _ in range(14):                                  # darker earth specks
        x, y = rng.randrange(T), rng.randrange(T)
        px[x, y] = P["bark"]
    for _ in range(5):                                   # lighter grit
        x, y = rng.randrange(T), rng.randrange(T)
        px[x, y] = P["stone"]
    for _ in range(rng.randint(0, 2)):                   # a small pale root curl
        x, y = rng.randrange(2, T - 4), rng.randrange(2, T - 3)
        for dx, dy in ((0, 0), (1, 0), (2, 1), (3, 1)):
            px[x + dx, y + dy] = P["stone"]
        px[x + 1, y + 1] = P["bark"]
    return img


def wall_top(seed=0):
    rng = random.Random(f"wall-{seed}")
    img = Image.new("RGBA", (T, T), P["deep"])
    px = img.load()
    for _ in range(4):                                   # tangled roots in the dark mass
        x, y = rng.randrange(T), rng.randrange(T)
        dx = rng.choice((-1, 1))
        for k in range(rng.randint(5, 10)):
            xx, yy = (x + k * dx) % T, (y + (k // 3) * rng.choice((0, 1))) % T
            px[xx, yy] = P["bark"]
            if k % 4 == 0:
                px[xx, (yy + 1) % T] = P["plum"]
    return img


def wall_face():
    img = Image.new("RGBA", (T, T), P["bark"])
    px = img.load()
    for x in range(T):                                   # vertical root strands, lit left
        for y in range(T):
            k = x % 4
            px[x, y] = P["brown"] if k == 0 else P["bark"] if k in (1, 2) else P["out"]
            if (x * 5 + y * 3) % 11 == 0:
                px[x, y] = P["plum"]
    for x in range(T):
        px[x, 0] = P["stone"]                            # lit top rim where the root mass bends down
        px[x, T - 1] = P["out"]                          # meets the floor
    for x in (3, 10):                                    # a moss tuft or two
        px[x, 1] = P["moss"]
        px[x + 1, 1] = P["grass"]
    return img


def floor_shadow():
    img = floor(9)
    px = img.load()
    for x in range(T):
        for y in range(3):
            px[x, y] = P["deep"] if y < 2 else P["bark"]
    return img


def wall_edge(side):
    img = wall_top(7)
    px = img.load()
    for i in range(T):
        if side == "r":
            px[T - 2, i], px[T - 1, i] = P["bark"], P["out"]
            px[T - 3, i] = P["brown"] if i % 3 else P["bark"]
        elif side == "l":
            px[1, i], px[0, i] = P["bark"], P["out"]
            px[2, i] = P["brown"] if i % 3 else P["bark"]
        else:
            px[i, 1], px[i, 0] = P["bark"], P["out"]
            px[i, 2] = P["brown"] if i % 3 else P["bark"]
    return img


def hollow_oak():
    """The great oak's trunk seen from the front, with a dark doorway at its foot."""
    W = H = 80
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = img.load()
    rng = random.Random("oak")
    for y in range(H):
        spread = max(0, (y - 52)) * 0.9                  # roots flare at the base
        x0, x1 = int(18 - spread), int(62 + spread)
        for x in range(max(0, x0), min(W, x1)):
            u = (x - x0) / max(1, (x1 - x0))
            col = "stone" if u < 0.18 else "brown" if u < 0.62 else "bark"
            if (x + (y // 7)) % 6 == 0:
                col = "bark" if col != "bark" else "out"
            px[x, y] = P[col]
    for _ in range(40):                                  # moss on the bark, thicker low down
        x, y = rng.randrange(20, 60), rng.randrange(10, 76)
        if px[x, y][3] and rng.random() < 0.5 + y / 160:
            px[x, y] = P["moss"] if rng.random() < 0.6 else P["grass"]
    for y in range(46, H):                               # the doorway: a dark arch two tiles wide
        for x in range(24, 56):
            cy = 58
            if y >= cy or ((x - 40) / 16) ** 2 + ((y - cy) / 12) ** 2 <= 1:
                px[x, y] = P["deep"] if y > 50 else P["out"]
    for x in range(24, 56):                              # a worn sill of packed earth
        px[x, H - 1] = P["bark"]
    src = img.copy()                                     # outline
    s = src.load()
    for y in range(H):
        for x in range(W):
            if s[x, y][3]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and s[nx, ny][3] and s[nx, ny] != P["out"]:
                    px[x, y] = P["out"]
                    break
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tiles = {f"floor_{i}": floor(i) for i in range(4)}
    tiles.update({"floor_shadow": floor_shadow(), "wall_top": wall_top(), "wall_face": wall_face(),
                  "wall_edge_l": wall_edge("l"), "wall_edge_r": wall_edge("r"), "wall_edge_t": wall_edge("t")})
    names = {}
    for name, img in tiles.items():
        path = OUT / f"{name}.png"
        img.save(path)
        names[name] = path.as_posix()
    Path("tools/kits/dungeon16.json").write_text(json.dumps({"tile": T, "tiles": names}, indent=1))
    hollow_oak().save("art/final/obj_hollow_oak.png")
    print(f"{len(names)} tiles -> {OUT}; art/final/obj_hollow_oak.png")


if __name__ == "__main__":
    main()
