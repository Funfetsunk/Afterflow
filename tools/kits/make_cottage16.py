"""Build the 16px cottage tile kit from the north star's long cottage.

Everything is on the 16px grid (Art Bible §2, "everything is tiles"). Two
layers, painted separately (Tom chose separate roof and wall layers):

  roof  : roof_{top,mid,bot}_{l,m,r}   3x3 nine-slice; repeat _mid rows for a
          deeper roof and _m columns for a longer one.
  wall  : wall_{top,bot}_{l,m,r}, plus feature columns (top + bottom tile):
          window_big, window_small, door. Walls are 2 tiles (32px) tall.
  stamp : chimney (1 column x 3 rows), drawn over the roof's top row.

The north-star wall is 21 rows; 11 rows are added below the windows: stone
columns take a real 11-row block of plain stone (rows 70-80 of the plain-wall
columns), timber posts repeat their own rows 79/80. The door is stretched
proportionally instead: rows 65-72 (frame + dark upper panels), 68-72 again,
73-80 (lit lower panels, with the latch), 81-85 (plain lower panel, below the
latch), 81-86 (bottom + outline) = 32 rows. The base keeps the north star's own rows 82-86, with grass tufts
overlapping the stone (Tom: with a clean hard base the houses looked pasted on).

  shadow: shadow_{roof_mid,roof_bot,wall_top,wall_bot}, the cast shadow on the
          grass to the right of the house (north star x 288-303).
  (No doorstep: what looked like a step in the north star is the path itself
  running up to the door; paths are painted with the terrain tiles.)

Run from the project root:
    python tools/kits/make_cottage16.py
Writes art/final/tiles/cottage16/*.png and tools/kits/cottage16.json.
"""

import json
from pathlib import Path

from PIL import Image

NS = "art/final/north_star/ns_meadow_village_r2_mix.png"
OUT = Path("art/final/tiles/cottage16")
X0 = 187                     # north-star x of the roof's left outline (local column 0)
OUTLINE = (0x2e, 0x22, 0x2f)
GROUND = {(0x54, 0x7e, 0x64), (0x37, 0x4e, 0x4a), (0x31, 0x36, 0x38)}


def main():
    ns = Image.open(NS).convert("RGB")
    px = ns.load()
    OUT.mkdir(parents=True, exist_ok=True)

    def column(col, rows):
        """One local column (list of RGBA) over the given north-star rows."""
        return [px[X0 + col, y] + (255,) for y in rows]

    def tile(cols, rows, transparent_cols=()):
        img = Image.new("RGBA", (len(cols), len(rows)), (0, 0, 0, 0))
        p = img.load()
        for i, col in enumerate(cols):
            if col in transparent_cols:
                continue
            for j, colour in enumerate(column(col, rows)):
                p[i, j] = colour
        return img

    # ---- roof: rows 24-39 top, 40-55 mid, 49-64 bottom; columns 0-15 left, 16-31 middle, 85-100 right
    roof_rows = {"top": range(24, 40), "mid": range(40, 56), "bot": range(49, 65)}
    roof_cols = {"l": list(range(0, 16)), "m": list(range(16, 32)), "r": list(range(85, 101))}
    names = {}
    for rk, rows in roof_rows.items():
        for ck, cols in roof_cols.items():
            name = f"roof_{rk}_{ck}"
            tile(cols, rows).save(OUT / f"{name}.png")
            names[name] = f"{OUT.as_posix()}/{name}.png"

    # ---- wall: build each wall column as 32 rows
    door_cols = set(range(63, 80))
    post_cols = {3, 4, 5, 6, 47, 48, 49, 50, 94, 95, 96, 97, 98, 99, 100}   # timber posts, and the cast shadow at 98-100
    plain = list(range(7, 20)) + [34, 35, 36]                        # 16 columns of plain stone

    def wall_column(col, index):
        top = list(range(65, 81))                                    # 16 rows as drawn
        base = list(range(82, 87))                                   # 5 base rows, tufts kept
        colours = [px[X0 + col, y] + (255,) for y in top]
        if col in door_cols:
            rows = list(range(65, 73)) + list(range(68, 73)) + list(range(73, 81)) + list(range(81, 86)) + list(range(81, 87))
            return [px[X0 + col, y] + (255,) for y in rows]
        if col in post_cols:
            filler = [px[X0 + col, y] + (255,) for y in ([79, 80] * 6)[:11]]
        else:                                                        # a real block of plain stone
            source = plain[index % len(plain)]
            filler = [px[X0 + source, y] + (255,) for y in range(70, 81)]
        colours += filler + [px[X0 + col, y] + (255,) for y in base]
        return colours

    def wall_tiles(cols, transparent=()):
        img = Image.new("RGBA", (16, 32), (0, 0, 0, 0))
        p = img.load()
        for i, col in enumerate(cols):
            if col in transparent:
                continue
            for j, colour in enumerate(wall_column(col, i)):
                p[i, j] = colour
        return img.crop((0, 0, 16, 16)), img.crop((0, 16, 16, 32))

    wall_defs = {
        "wall_l": (list(range(0, 16)), (0, 1, 2)),                   # 3px roof overhang left transparent
        "wall_m": (plain, ()),
        "wall_r": (list(range(7, 16)) + list(range(94, 101)), ()),   # its last 3 columns are cast shadow
        "window_big": (list(range(18, 34)), ()),
        "window_small": (list(range(51, 63)) + [34, 35, 36, 37], ()),
        "door": (list(range(63, 70)) + list(range(71, 80)), ()),
    }
    for name, (cols, transparent) in wall_defs.items():
        assert len(cols) == 16, name
        top, bot = wall_tiles(cols, transparent)
        for part, img in (("top", top), ("bot", bot)):
            key = f"{name}_{part}"
            img.save(OUT / f"{key}.png")
            names[key] = f"{OUT.as_posix()}/{key}.png"

    # ---- cast shadow column (north star x 288-303): shadow and grass only, anything else becomes grass
    grass = (0x54, 0x7e, 0x64, 255)
    keep = {(0x37, 0x4e, 0x4a), (0x31, 0x36, 0x38), (0x54, 0x7e, 0x64)}

    def shadow_tile(rows):
        img = Image.new("RGBA", (16, len(rows)), (0, 0, 0, 0))
        p = img.load()
        for i in range(16):
            for j, y in enumerate(rows):
                c = px[288 + i, y]
                p[i, j] = (c + (255,)) if c in keep else grass
        return img

    shadow_wall = [y for y in range(65, 81)] + ([79, 80] * 6)[:11] + list(range(82, 87))
    shadow_defs = {"shadow_roof_mid": list(range(52, 62)) + list(range(56, 62)),
                   "shadow_roof_bot": list(range(49, 65)),                 # shadow starts 3 rows down (roof of 2)
                   "shadow_roof_bot_full": [52, 53, 54] + list(range(52, 65)),  # under a middle row: no gap
                   "shadow_wall_top": shadow_wall[:16],
                   "shadow_wall_bot": shadow_wall[16:]}
    for name, rows in shadow_defs.items():
        shadow_tile(rows).save(OUT / f"{name}.png")
        names[name] = f"{OUT.as_posix()}/{name}.png"

    # ---- chimney stamp: north-star columns 57-72 (x 244-259), rows -8..39 as a 1x3 stamp;
    # keep only the chimney (rows 4-30) and clear everything else
    chimney = Image.new("RGBA", (16, 48), (0, 0, 0, 0))
    cp = chimney.load()
    for i in range(16):
        for y in range(4, 31):
            colour = px[X0 + 57 + i, y]
            if y < 24 and colour in GROUND:
                continue
            cp[i, y + 8] = colour + (255,)
    for k, part in enumerate(("chimney_0", "chimney_1", "chimney_2")):
        chimney.crop((0, k * 16, 16, k * 16 + 16)).save(OUT / f"{part}.png")
        names[part] = f"{OUT.as_posix()}/{part}.png"

    Path("tools/kits/cottage16.json").write_text(json.dumps({"tile": 16, "tiles": names}, indent=1))
    print(f"{len(names)} tiles -> {OUT}")


if __name__ == "__main__":
    main()
