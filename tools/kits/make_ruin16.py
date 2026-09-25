"""Build the 16px crumbled ruin-wall kit from the cottage kit's north-star stone.

Ruins are the cottages' own stone, broken down (Art Bible §5.3: crumbled,
alive and green, never angular). Each ruin column is 1 tile wide and 2 tiles
tall (like a cottage wall), with a jagged broken top at one of several heights:

  full  high  mid  low  stub   straight runs at different heights
  end_l end_r                  stepped ends crumbling down towards the outside

Every broken top gets a dark 2e222f outline and a pale stone cap (you see the
tops of the stones from our high top-down camera), plus moss and a little ivy
in the palette's greens. The base keeps the cottage stone's grass tufts.
Tops follow a seeded random walk in stone-sized steps (3-6px; 1-2px steps read
as spikes) with sudden drops and missing chunks (a straight
interpolated profile read as a staircase; Tom rejects angular ruins). Each type
also has a _shadow variant for the last column of a run: a slim shadow down
its right edge that follows the broken top (a full shadow column read as a slab).
The lower courses are weathered one step darker (ab947a -> 966c6c, 966c6c ->
625565) below ~60% of the wall (a boundary that wanders per column, randomly
dithered above it) and damp moss along
the base, so walls have weight. Rubble stamps (fallen stones, same colours) are
written to art/final/obj_rubble16_*.png for tools/make_stamp.py.
Three variants per type (a, b, c) so long runs don't repeat; all random choices
are seeded, so the kit rebuilds identically.

Run from the project root (after make_cottage16.py):
    python tools/kits/make_ruin16.py
Writes art/final/tiles/ruin16/*.png and tools/kits/ruin16.json.
"""

import json
import random
from pathlib import Path

from PIL import Image

KIT = Path("tools/kits/cottage16.json")
OUT = Path("art/final/tiles/ruin16")
T = 16
H = 32                                   # two tiles tall, like a cottage wall
OUTLINE = (0x2e, 0x22, 0x2f, 255)
CAP = [(0xab, 0x94, 0x7a, 255), (0xab, 0x94, 0x7a, 255), (0x96, 0x6c, 0x6c, 255)]
MOSS = [(0x37, 0x4e, 0x4a, 255), (0x67, 0x66, 0x33, 255)]
IVY = (0x37, 0x4e, 0x4a, 255)

# top of the wall (y of the outline row) per type: (left, right) heights; jitter added per column
TYPES = {
    "full": (3, 3), "high": (9, 9), "mid": (15, 15), "low": (21, 21), "stub": (26, 26),
    "end_l": (24, 6),                     # low on the left, rising: the wall's broken left end
    "end_r": (6, 24),                     # high on the left, falling: the broken right end
}


def stone_block(tiles):
    """16x32 plain stone from the cottage kit (wall_m top over bottom)."""
    block = Image.new("RGBA", (T, H), (0, 0, 0, 0))
    block.alpha_composite(Image.open(tiles["wall_m_top"]).convert("RGBA"), (0, 0))
    block.alpha_composite(Image.open(tiles["wall_m_bot"]).convert("RGBA"), (0, T))
    return block


def profile(kind, rng):
    """Top y per column: a random walk around the type's height, with drops and chunks."""
    left, right = TYPES[kind]
    tops, x, y = [], 0, left + rng.choice((-2, 0, 2))
    while x < T:
        run = rng.choice((3, 4, 4, 5, 6))                         # whole stones: no 1-2px spires
        target = left + (right - left) * min(x, T - 1) / (T - 1)
        y += rng.choice((-3, -2, -1, 0, 0, 1, 2, 3)) + (target - y) * 0.5
        if rng.random() < 0.15:
            y += rng.choice((4, 6))                               # a missing chunk
        tops += [int(max(1, min(H - 4, round(y))))] * run
        x += run
    return tops[:T]


def build(kind, variant, stone):
    rng = random.Random(f"{kind}-{variant}")
    tops = profile(kind, rng)
    tile = Image.new("RGBA", (T, H), (0, 0, 0, 0))
    src, dst = stone.load(), tile.load()
    for x in range(T):
        top = tops[x]
        for y in range(top, H):
            dst[x, y] = src[x, y]
        dst[x, top] = OUTLINE                                   # outline along the broken top
        for k in (1, 2):                                        # pale cap: the tops of the stones
            if top + k < H - 6:
                dst[x, top + k] = rng.choice(CAP)
        if top + 3 < H - 6:
            dst[x, top + 3] = OUTLINE if rng.random() < 0.5 else src[x, top + 3]
    for x in range(T):                                          # vertical outline where the top steps
        for nx in (x - 1, x + 1):
            if 0 <= nx < T and tops[nx] > tops[x]:
                for y in range(tops[x], min(tops[nx] + 1, H)):
                    dst[x, y] = OUTLINE
    for _ in range(rng.randint(4, 7)):                          # moss clumps over the cap and upper face
        x = rng.randrange(T)
        y0 = tops[x] + rng.randint(0, 5)
        w, hgt = rng.randint(2, 5), rng.randint(1, 3)
        for dx in range(w):
            for dy in range(hgt):
                xx, yy = x + dx, y0 + dy
                if 0 <= xx < T and tops[xx] < yy < H - 5 and rng.random() < 0.85:
                    dst[xx, yy] = MOSS[1] if dy == 0 else rng.choice(MOSS)
    for _ in range(rng.randint(1, 2)):                          # ivy strands with leaves
        x = rng.randrange(1, T - 1)
        for yy in range(tops[x] + 1, min(tops[x] + rng.randint(6, 13), H - 5)):
            dst[x, yy] = IVY
            if rng.random() < 0.4:
                side = x + rng.choice((-1, 1))
                if 0 <= side < T and tops[side] < yy:
                    dst[side, yy] = MOSS[1]
    return tile, tops


STONE_DARKER = {(0xab, 0x94, 0x7a): (0x96, 0x6c, 0x6c), (0x96, 0x6c, 0x6c): (0x62, 0x55, 0x65)}
DARK_FROM = 20          # wall rows below this are weathered darker (the base is rows 27-31)


def weather(tile, tops, rng):
    """Darken the lower courses, dithered at the boundary, and add damp moss at the base."""
    px = tile.load()
    edge = DARK_FROM
    for x in range(T):
        edge = max(DARK_FROM - 3, min(DARK_FROM + 3, edge + rng.choice((-1, 0, 0, 1))))   # wandering boundary
        for y in range(max(tops[x] + 4, edge - 2), H):          # all the way down; base tufts are grass colours
            r, g, b, a = px[x, y]
            if not a or (r, g, b) not in STONE_DARKER:
                continue
            if y >= edge or rng.random() < 0.45:              # random dither just above the boundary
                px[x, y] = STONE_DARKER[(r, g, b)] + (a,)
        if rng.random() < 0.3:                                 # damp moss creeping up from the ground
            for y in range(H - 7, H - 5):
                if px[x, y][3]:
                    px[x, y] = MOSS[0]
    return tile


def rubble(seed, width, count):
    """A scatter of fallen stones: pale top, stone body, darker base, outline, cast shadow."""
    rng = random.Random(seed)
    img = Image.new("RGBA", (width, T), (0, 0, 0, 0))
    px = img.load()
    shadow = (0x37, 0x4e, 0x4a, 255)
    stones = []
    for _ in range(count):
        w, h = rng.randint(4, 6), rng.randint(3, 4)
        x = rng.randint(1, width - w - 2)
        y = rng.randint(T - h - 6, T - h - 2)
        stones.append((y, x, w, h))
    for y, x, w, h in sorted(stones):                         # back to front
        for yy in range(y + 1, y + h + 2):                     # shadow down and to the right
            for xx in range(x + 1, x + w + 2):
                if 0 <= xx < width and 0 <= yy < T and not px[xx, yy][3]:
                    px[xx, yy] = shadow
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                edge = yy in (y, y + h - 1) or xx in (x, x + w - 1)
                if edge:
                    px[xx, yy] = OUTLINE
                elif yy == y + 1:
                    px[xx, yy] = CAP[0]
                elif yy == y + h - 2 and h > 3:
                    px[xx, yy] = (0x62, 0x55, 0x65, 255)
                else:
                    px[xx, yy] = (0x96, 0x6c, 0x6c, 255)
        if rng.random() < 0.5:                                  # a dab of moss on top
            mx = x + rng.randint(1, max(1, w - 3))
            px[mx, y + 1] = MOSS[1]
    return img


def add_shadow(tile, tops):
    """Slim cast shadow down the right edge of a run's last column, following its top."""
    shadow = (0x37, 0x4e, 0x4a, 255)
    px = tile.load()
    top = tops[-1] + 3
    for x in (T - 3, T - 2, T - 1):
        for y in range(top + (x - (T - 3)), H - 1):
            if px[x, y][3] == 0 or px[x, y][:3] in {(0x54, 0x7e, 0x64)}:
                px[x, y] = shadow
    return tile


def main():
    tiles = json.loads(KIT.read_text())["tiles"]
    stone = stone_block(tiles)
    OUT.mkdir(parents=True, exist_ok=True)
    names = {}
    for kind in TYPES:
        for variant in "abc":
            tile, tops = build(kind, variant, stone)
            tile = weather(tile, tops, random.Random(f"weather-{kind}-{variant}"))
            shadowed = add_shadow(tile.copy(), tops)
            for suffix, img in (("", tile), ("_shadow", shadowed)):
                for part, box in (("top", (0, 0, T, T)), ("bot", (0, T, T, H))):
                    key = f"ruin_{kind}_{variant}{suffix}_{part}"
                    path = OUT / f"{key}.png"
                    img.crop(box).save(path)
                    names[key] = path.as_posix()
    for name, width, count in (("a", T, 2), ("b", T, 3), ("c", T, 2), ("pile", 2 * T, 6)):
        rubble(f"rubble-{name}", width, count).save(f"art/final/obj_rubble16_{name}.png")
    Path("tools/kits/ruin16.json").write_text(json.dumps({"tile": T, "tiles": names}, indent=1))
    print(f"{len(names)} tiles -> {OUT}")


if __name__ == "__main__":
    main()
