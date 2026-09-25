"""Build a compose_mock.py layout from a PixelLab Wang tileset and a terrain map.

The terrain map is a text file of vertex rows: '#' = lower terrain,
'.' = upper terrain. A map with C columns and R rows gives (C-1) x (R-1)
tiles; 21 x 13 vertices covers the 320x180 screen (20 x 12 tiles of 16px, the last
row partly off screen); pass --legacy to compose_mock.py for v0.x 32px maps. Each tile is chosen by its four corners and cut
from the sheet with the bounding_box from the tileset's metadata JSON.

Optional --fill-variants / --lower-variants: extra tile-sized PNGs used at random
in place of the full-upper / full-lower tile (e.g. grass or water variations),
to preview how a Godot TileSet with weighted alternative tiles breaks up
repetition. --variant-chance applies to both. --seed makes it repeatable.

Usage:
    python tools/wang_layout.py art/raw/ts_x.json art/final/ts_x.png map.txt out.json
    python tools/wang_layout.py meta.json sheet.png map.txt out.json \\
        --fill-variants art/final/grass_v1.png art/final/grass_v2.png --variant-chance 0.4 --seed 3 \\
        --sprite art/final/chr_awa_a_s.png 196 150

Then: python tools/compose_mock.py out.json

--extra CHAR META SHEET adds a second tileset that shares the same upper
terrain (e.g. '~' = water, next to '#' = path, both against grass '.'). A cell
may mix '.' with one lower terrain only; '#' and '~' must not touch.
--extra-variants PNG... scatters alternatives on full cells of the extra terrain.
"""

import argparse
import json
import random
import sys
from pathlib import Path



def main():
    parser = argparse.ArgumentParser(description="Wang tileset + terrain map -> mock layout JSON.")
    parser.add_argument("metadata", type=Path, help="tileset metadata JSON from PixelLab")
    parser.add_argument("sheet", help="palette-remapped tileset PNG in art/final/")
    parser.add_argument("terrain_map", type=Path, help="text file of vertex rows ('#' lower, '.' upper)")
    parser.add_argument("output", type=Path, help="layout JSON to write")
    parser.add_argument("--fill-variants", nargs="+", default=[], metavar="PNG",
                        help="alternative full-upper tiles to scatter at random")
    parser.add_argument("--lower-variants", nargs="+", default=[], metavar="PNG",
                        help="alternative full-lower tiles to scatter at random")
    parser.add_argument("--extra", nargs=3, metavar=("CHAR", "META", "SHEET"),
                        help="second tileset for another lower terrain")
    parser.add_argument("--extra-variants", nargs="+", default=[], metavar="PNG",
                        help="alternative full tiles for the extra terrain")
    parser.add_argument("--variant-chance", type=float, default=0.35,
                        help="chance a full cell uses a variant (default 0.35)")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--sprite", nargs=3, action="append", default=[], metavar=("PNG", "X", "Y"),
                        help="sprite to draw on top at pixel position X Y (repeatable)")
    args = parser.parse_args()

    rows = [line.rstrip("\n") for line in args.terrain_map.read_text().splitlines() if line.strip()]
    if len({len(row) for row in rows}) != 1:
        sys.exit("Terrain map rows must all be the same length")

    def load_lookup(path):
        lookup = {}
        for tile in json.loads(Path(path).read_text())["tileset_data"]["tiles"]:
            corners, box = tile["corners"], tile["bounding_box"]
            key = (corners["NW"], corners["NE"], corners["SW"], corners["SE"])
            lookup[key] = [box["x"], box["y"], box["width"], box["height"]]
        return lookup

    # lower-terrain char -> (sheet, corner lookup, full-lower variants)
    tilesets = {"#": (args.sheet, load_lookup(args.metadata), args.lower_variants)}
    if args.extra:
        char, meta, sheet = args.extra
        tilesets[char] = (sheet, load_lookup(meta), args.extra_variants)

    rng = random.Random(args.seed)
    items = []
    for r in range(len(rows) - 1):
        for c in range(len(rows[0]) - 1):
            chars = (rows[r][c], rows[r][c + 1], rows[r + 1][c], rows[r + 1][c + 1])
            lowers = {ch for ch in chars if ch != "."}
            if len(lowers) > 1:
                sys.exit(f"Cell {c},{r} mixes two lower terrains {sorted(lowers)}; keep grass between them")
            lower = lowers.pop() if lowers else "#"
            if lower not in tilesets:
                sys.exit(f"Unknown terrain character {lower!r}")
            sheet, lookup, lower_variants = tilesets[lower]
            key = tuple("upper" if ch == "." else "lower" for ch in chars)
            if key not in lookup:
                sys.exit(f"Tileset has no tile for corners {key}")
            variants = {("upper",) * 4: args.fill_variants, ("lower",) * 4: lower_variants}.get(key)
            if variants and rng.random() < args.variant_chance:
                items.append({"image": rng.choice(variants), "cell": [c, r]})
            else:
                items.append({"image": sheet, "cell": [c, r], "crop": lookup[key]})

    for image, x, y in args.sprite:
        items.append({"image": image, "at": [int(x), int(y)]})

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"background": "#2e222f", "items": items}, indent=1))
    print(f"{args.output}: {len(items)} items")


if __name__ == "__main__":
    main()
