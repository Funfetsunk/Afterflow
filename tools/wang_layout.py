"""Build a compose_mock.py layout from a PixelLab Wang tileset and a terrain map.

The terrain map is a text file of vertex rows: '#' = lower terrain,
'.' = upper terrain. A map with C columns and R rows gives (C-1) x (R-1)
tiles; 16 x 10 vertices covers the 480x270 screen (15 x 9 tiles, the last
row partly off screen). Each tile is chosen by its four corners and cut
from the sheet with the bounding_box from the tileset's metadata JSON.

Optional --fill-variants: extra 32x32 PNGs used at random in place of the
full-upper tile (e.g. grass variations), to preview how a Godot TileSet with
weighted alternative tiles breaks up repetition. --seed makes it repeatable.

Usage:
    python tools/wang_layout.py art/raw/ts_x.json art/final/ts_x.png map.txt out.json
    python tools/wang_layout.py meta.json sheet.png map.txt out.json \\
        --fill-variants art/final/grass_v1.png art/final/grass_v2.png --variant-chance 0.4 --seed 3 \\
        --sprite art/final/chr_awa_a_s.png 196 150

Then: python tools/compose_mock.py out.json
"""

import argparse
import json
import random
import sys
from pathlib import Path

TILE = 32


def main():
    parser = argparse.ArgumentParser(description="Wang tileset + terrain map -> mock layout JSON.")
    parser.add_argument("metadata", type=Path, help="tileset metadata JSON from PixelLab")
    parser.add_argument("sheet", help="palette-remapped tileset PNG in art/final/")
    parser.add_argument("terrain_map", type=Path, help="text file of vertex rows ('#' lower, '.' upper)")
    parser.add_argument("output", type=Path, help="layout JSON to write")
    parser.add_argument("--fill-variants", nargs="+", default=[], metavar="PNG",
                        help="alternative full-upper tiles to scatter at random")
    parser.add_argument("--variant-chance", type=float, default=0.35,
                        help="chance a full-upper cell uses a variant (default 0.35)")
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--sprite", nargs=3, action="append", default=[], metavar=("PNG", "X", "Y"),
                        help="sprite to draw on top at pixel position X Y (repeatable)")
    args = parser.parse_args()

    rows = [line.rstrip("\n") for line in args.terrain_map.read_text().splitlines() if line.strip()]
    if len({len(row) for row in rows}) != 1:
        sys.exit("Terrain map rows must all be the same length")

    metadata = json.loads(args.metadata.read_text())
    lookup = {}
    for tile in metadata["tileset_data"]["tiles"]:
        corners, box = tile["corners"], tile["bounding_box"]
        key = (corners["NW"], corners["NE"], corners["SW"], corners["SE"])
        lookup[key] = [box["x"], box["y"], box["width"], box["height"]]

    def terrain(char):
        return "lower" if char == "#" else "upper"

    rng = random.Random(args.seed)
    items = []
    for r in range(len(rows) - 1):
        for c in range(len(rows[0]) - 1):
            key = (terrain(rows[r][c]), terrain(rows[r][c + 1]),
                   terrain(rows[r + 1][c]), terrain(rows[r + 1][c + 1]))
            if key not in lookup:
                sys.exit(f"Tileset has no tile for corners {key}")
            if key == ("upper",) * 4 and args.fill_variants and rng.random() < args.variant_chance:
                items.append({"image": rng.choice(args.fill_variants), "cell": [c, r]})
            else:
                items.append({"image": args.sheet, "cell": [c, r], "crop": lookup[key]})

    for image, x, y in args.sprite:
        items.append({"image": image, "at": [int(x), int(y)]})

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"background": "#2e222f", "items": items}, indent=1))
    print(f"{args.output}: {len(items)} items")


if __name__ == "__main__":
    main()
