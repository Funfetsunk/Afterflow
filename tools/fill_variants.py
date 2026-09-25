"""Make alternative fill tiles from one seamless tile by flipping and rotating.

For low-detail ground textures (irregular speckle, no directional marks) the
7 flip/rotation copies still tile with each other and with the original
without visible seams, and they break up the grid you see when one tile
repeats. Use them as weighted alternative tiles in the Godot TileSet, and
preview them with wang_layout.py --fill-variants.

Don't use this on tiles with directional detail (shadows, lit edges, grass
blades leaning one way): flipped copies will show it.

Usage:
    python tools/fill_variants.py art/final/sheet.png 0 96 art/final/ts_meadow_grass-fill
    -> ts_meadow_grass-fill_00.png (original) ... _07.png

Arguments: source image, then the tile's top-left x y (32x32 tile), then the
output path prefix.
"""

import argparse
from pathlib import Path

from PIL import Image

TILE = 32
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


def main():
    parser = argparse.ArgumentParser(description="Flip/rotate a seamless tile into 8 fill variants.")
    parser.add_argument("source", type=Path)
    parser.add_argument("x", type=int)
    parser.add_argument("y", type=int)
    parser.add_argument("prefix", help="output path prefix; _00.._07.png is appended")
    args = parser.parse_args()

    tile = Image.open(args.source).convert("RGBA").crop((args.x, args.y, args.x + TILE, args.y + TILE))
    for index, steps in enumerate(TRANSFORMS):
        variant = tile
        for step in steps:
            variant = variant.transpose(step)
        path = Path(f"{args.prefix}_{index:02d}.png")
        path.parent.mkdir(parents=True, exist_ok=True)
        variant.save(path)
        print(path)


if __name__ == "__main__":
    main()
