"""Paint a woodland of any size as one layer of 16px tiles.

Forests are built from the approved tree stamps (Tom, 2026-09-25: the stamp
woodland is the forest look; PixelLab's terrain tilesets can't draw crowns).
Trees are planted on a fixed staggered lattice, one base every 2 columns per
row with alternate rows shifted by one column, and drawn back to front so the
crowns overlap. The species at each lattice point comes from a fixed pattern of
the absolute grid position, so the same map always gives the same forest.

The overlapped render is sliced into 16px cells, and each cell is looked up in
a shared tile library (art/final/tiles/forest16/, index tools/kits/forest16.json)
by its pixels: identical cells reuse the same tile. Because the lattice
repeats, the library stays small and is, in effect, the forest tile set.

Usage:
    python tools/paint_forest.py layout.json 0 2 9 5
    python tools/paint_forest.py layout.json COL ROW WIDTH HEIGHT

COL ROW WIDTH HEIGHT is the canopy rectangle in grid cells. The front (bottom)
row shows trunks and shadows on the grass; crowns of the back row fill the top
row. Gaps completely enclosed by crowns (unreachable from outside the forest
without crossing a tree) are filled with deep shade 313638 so the woodland
reads dense; openings that reach the edge stay grass. Width >= 3, height >= 3.

For the TileSet, each tile's collision and y-sort origin are recorded in
tools/kits/forest16_meta.json: trunk bases (tools/footprint.py), the enclosed
deep shade and tiles of solid canopy (the wood's interior) block; crown tiles
sort at their tree's base, so Awa can walk behind the ragged edge of a wood
without disappearing into it.
"""

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image

from footprint import footprint, split_by_cells

TILE = 16
LIB_DIR = Path("art/final/tiles/forest16")
LIB_INDEX = Path("tools/kits/forest16.json")
META_INDEX = Path("tools/kits/forest16_meta.json")      # per tile: collision rects and y-sort origin
PATTERN = ["oak_a", "oak_b", "oak_a", "birch_a", "oak_b", "oak_a", "oak_b"]


def species(col, row):
    return PATTERN[(col // 2 + row * 3) % len(PATTERN)]


def main():
    parser = argparse.ArgumentParser(description="Paint a woodland as one layer of 16px tiles.")
    parser.add_argument("layout", type=Path)
    parser.add_argument("rect", nargs=4, type=int, metavar=("COL", "ROW", "WIDTH", "HEIGHT"))
    args = parser.parse_args()
    c0, r0, w, h = args.rect
    if w < 3 or h < 3:
        sys.exit("A forest needs at least 3x3 cells")

    stamps = json.loads(Path("tools/kits/stamps.json").read_text())
    images = {}

    def stamp_image(name):
        if name not in images:
            s = stamps[name]
            img = Image.new("RGBA", (s["cols"] * TILE, s["rows"] * TILE), (0, 0, 0, 0))
            for r, row in enumerate(s["tiles"]):
                for c, path in enumerate(row):
                    img.alpha_composite(Image.open(path).convert("RGBA"), (c * TILE, r * TILE))
            images[name] = img
        return images[name]

    # Canvas covers the canopy rectangle exactly (in cells).
    canvas = Image.new("RGBA", (w * TILE, h * TILE), (0, 0, 0, 0))
    plantings = []
    for base_row in range(r0 + 2, r0 + h):            # crowns reach 2 rows above the base
        start = c0 + ((base_row + c0) % 2)
        for col in range(start, c0 + w - 2, 2):       # oak stamps are 3 wide
            plantings.append((base_row, col, species(col, base_row)))
    trunk_rects, covers = [], []                     # canvas-space footprints; (opaque bbox, base y)
    for base_row, col, name in sorted(plantings):     # back to front
        img = stamp_image(name)
        rows = img.height // TILE
        x = (col - c0) * TILE
        y = (base_row - rows + 1 - r0) * TILE
        canvas.alpha_composite(img, (x, y))
        fp = footprint(img)
        if fp:
            trunk_rects.append((x + fp[0], y + fp[1], x + fp[2], y + fp[3]))
            bx0, by0, bx1, by1 = img.getchannel("A").getbbox()
            covers.append(((x + bx0, y + by0, x + bx1, y + by1), y + fp[3]))

    # deep shade only in gaps fully enclosed by crowns: flood the open area in from the edges
    shade = (0x31, 0x36, 0x38, 255)
    pixels = canvas.load()
    cw, ch = canvas.size
    outside = set()
    stack = [(x, y) for x in range(cw) for y in (0, ch - 1)] + [(x, y) for y in range(ch) for x in (0, cw - 1)]
    stack = [p for p in stack if pixels[p][3] == 0]
    outside.update(stack)
    while stack:
        x, y = stack.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= n[0] < cw and 0 <= n[1] < ch and n not in outside and pixels[n][3] == 0:
                outside.add(n)
                stack.append(n)
    shaded = []
    for y in range(ch):
        for x in range(cw):
            if pixels[x, y][3] == 0 and (x, y) not in outside:
                pixels[x, y] = shade
                shaded.append((x, y))

    # per cell (canvas-relative col, row): collision rects in cell-local pixels, y-sort origin
    cell_rects = defaultdict(list)
    for rect in trunk_rects:
        for cell, local in split_by_cells(rect, TILE).items():
            cell_rects[cell].append(list(local))
    shade_box = {}
    for x, y in shaded:                                # enclosed deep shade blocks too
        cell = (x // TILE, y // TILE)
        lx, ly = x % TILE, y % TILE
        b = shade_box.get(cell, [lx, ly, lx + 1, ly + 1])
        shade_box[cell] = [min(b[0], lx), min(b[1], ly), max(b[2], lx + 1), max(b[3], ly + 1)]
    for cell, box in shade_box.items():
        cell_rects[cell].append(box)
    def y_sort_for(cell):
        cx, cy = cell[0] * TILE, cell[1] * TILE
        bases = [base for (x0, y0, x1, y1), base in covers if x0 < cx + TILE and x1 > cx and y0 < cy + TILE and y1 > cy]
        return max(bases) - cy if bases else 0

    LIB_DIR.mkdir(parents=True, exist_ok=True)
    index = json.loads(LIB_INDEX.read_text()) if LIB_INDEX.exists() else {}
    meta = json.loads(META_INDEX.read_text()) if META_INDEX.exists() else {}
    items, new = [], 0
    for r in range(h):
        for c in range(w):
            cell = canvas.crop((c * TILE, r * TILE, (c + 1) * TILE, (r + 1) * TILE))
            if not cell.getchannel("A").getbbox():
                continue
            key = hashlib.md5(cell.tobytes()).hexdigest()[:12]
            if key not in index:
                path = LIB_DIR / f"forest_{key}.png"
                cell.save(path)
                index[key] = path.as_posix()
                new += 1
            if key not in meta:
                full = cell.getchannel("A").getextrema()[0] == 255      # solid canopy: the wood's interior
                meta[key] = {"rects": [[0, 0, TILE, TILE]] if full else cell_rects.get((c, r), []),
                             "y_sort": y_sort_for((c, r))}
            items.append({"image": index[key], "cell": [c0 + c, r0 + r]})
    LIB_INDEX.write_text(json.dumps(index, indent=1))
    META_INDEX.write_text(json.dumps(meta, indent=1))

    layout = json.loads(args.layout.read_text()) if args.layout.exists() else {"items": []}
    layout["items"].extend(items)
    args.layout.write_text(json.dumps(layout, indent=1))
    print(f"{args.layout}: +{len(items)} forest tiles ({new} new, library {len(index)})")


if __name__ == "__main__":
    main()
