"""Make alternative fill tiles from one seamless tile by flipping and rotating.

For low-detail ground textures (irregular speckle, no directional marks) the
7 flip/rotation copies still tile with each other and with the original
without visible seams, and they break up the grid you see when one tile
repeats. Use them as weighted alternative tiles in the Godot TileSet, and
preview them with wang_layout.py --fill-variants.

Don't use this on tiles with directional detail (shadows, lit edges, grass
blades leaning one way): flipped copies will show it. For tiles with a single
direction, such as horizontal water ripples, use only _00-_03 (original,
mirror, flip, 180 degrees): they keep the direction. _04-_07 turn it 90 degrees.

Usage:
    python tools/fill_variants.py art/final/sheet.png 0 96 art/final/ts_meadow_grass-fill
    -> ts_meadow_grass-fill_00.png (original) ... _07.png

Arguments: source image, then the tile's top-left x y (16x16 by default; --tile to change), then the
output path prefix.

--thin: also write calmer copies of the original with some strokes of one
colour removed (e.g. water ripples), for tiles whose marks sit in visible rows.
Each value is the fraction of strokes kept; removed strokes are painted with
the tile's most common colour. A stroke is a group of touching pixels.
    python tools/fill_variants.py sheet.png 64 32 art/final/ts_water-fill \
        --thin 0.6 0.4 0.25 0 --stroke-colour 8ff8e2 --seed 7
    -> also ts_water-fill_thin0.png ... _thin3.png
"""

import argparse
import random
from collections import Counter
from pathlib import Path

from PIL import Image

TILE = 16  # overridden by --tile
TRANSFORMS = [
    [],
    [Image.Transpose.FLIP_LEFT_RIGHT],
    [Image.Transpose.FLIP_TOP_BOTTOM],
    [Image.Transpose.ROTATE_180],
    [Image.Transpose.ROTATE_90],
    [Image.Transpose.ROTATE_270],
    [Image.Transpose.TRANSPOSE],
    [Image.Transpose.TRANSVERSE],
]


def strokes_of(tile, colour):
    """Groups of 8-connected pixels of one colour, in scan order."""
    pixels, seen, strokes = tile.load(), set(), []
    for y in range(TILE):
        for x in range(TILE):
            if pixels[x, y][:3] != colour or (x, y) in seen:
                continue
            stroke, i = [(x, y)], 0
            seen.add((x, y))
            while i < len(stroke):
                cx, cy = stroke[i]
                i += 1
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < TILE and 0 <= ny < TILE and (nx, ny) not in seen \
                                and pixels[nx, ny][:3] == colour:
                            seen.add((nx, ny))
                            stroke.append((nx, ny))
            strokes.append(stroke)
    return strokes


def main():
    parser = argparse.ArgumentParser(description="Flip/rotate a seamless tile into 8 fill variants.")
    parser.add_argument("source", type=Path)
    parser.add_argument("x", type=int)
    parser.add_argument("y", type=int)
    parser.add_argument("prefix", help="output path prefix; _00.._07.png is appended")
    parser.add_argument("--thin", nargs="+", type=float, default=[], metavar="KEEP",
                        help="write calmer copies keeping this fraction of strokes")
    parser.add_argument("--stroke-colour", help="RRGGBB of the strokes to thin")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--tile", type=int, default=16, help="tile size in pixels (v0.x assets: 32)")
    args = parser.parse_args()

    global TILE
    TILE = args.tile
    tile = Image.open(args.source).convert("RGBA").crop((args.x, args.y, args.x + TILE, args.y + TILE))
    for index, steps in enumerate(TRANSFORMS):
        variant = tile
        for step in steps:
            variant = variant.transpose(step)
        path = Path(f"{args.prefix}_{index:02d}.png")
        path.parent.mkdir(parents=True, exist_ok=True)
        variant.save(path)
        print(path)

    if args.thin:
        if not args.stroke_colour:
            parser.error("--thin needs --stroke-colour")
        colour = tuple(int(args.stroke_colour.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        base = Counter(tile.get_flattened_data()).most_common(1)[0][0]
        strokes = strokes_of(tile, colour)
        rng = random.Random(args.seed)
        for index, keep in enumerate(args.thin):
            calm = tile.copy()
            pixels = calm.load()
            for stroke in strokes:
                if rng.random() > keep:
                    for x, y in stroke:
                        pixels[x, y] = base
            path = Path(f"{args.prefix}_thin{index}.png")
            calm.save(path)
            print(f"{path} ({keep:.0%} of {len(strokes)} strokes kept)")


if __name__ == "__main__":
    main()
