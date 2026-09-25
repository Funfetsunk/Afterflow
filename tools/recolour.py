"""Swap exact colours in palette-remapped sprites.

For fixing one element that PixelLab keeps getting wrong (e.g. Awa's scarf)
without regenerating. Run it on art/final/ files, after palette_remap.py, and
use palette colours as targets so the result stays on the palette. Record the
mapping in ASSET_MANIFEST.md so the fix can be repeated on new frames.

Alpha is left untouched. Colours not in the mapping are left untouched.

Usage:
    python tools/recolour.py in.png out.png --map 547e64=4d65b4 374e4a=484a77
    python tools/recolour.py art/final/in.png art/final/out.png --map 547e64=4d65b4 --dry-run
"""

import argparse
import sys
from pathlib import Path

from PIL import Image


def parse_colour(text):
    text = text.strip().lstrip("#")
    if len(text) != 6:
        sys.exit(f"Expected RRGGBB, got {text!r}")
    return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))


def main():
    parser = argparse.ArgumentParser(description="Swap exact colours in a sprite.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--map", nargs="+", required=True, metavar="FROM=TO",
                        help="colour pairs as RRGGBB=RRGGBB")
    parser.add_argument("--dry-run", action="store_true", help="count pixels without writing")
    args = parser.parse_args()

    mapping = {}
    for pair in args.map:
        if "=" not in pair:
            sys.exit(f"Expected FROM=TO, got {pair!r}")
        source, target = pair.split("=", 1)
        mapping[parse_colour(source)] = parse_colour(target)

    image = Image.open(args.input).convert("RGBA")
    pixels = image.load()
    counts = {colour: 0 for colour in mapping}
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if a and (r, g, b) in mapping:
                counts[(r, g, b)] += 1
                pixels[x, y] = mapping[(r, g, b)] + (a,)

    for colour, count in counts.items():
        print("%02x%02x%02x -> %02x%02x%02x: %d px" % (colour + mapping[colour] + (count,)))
    if not args.dry_run:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        image.save(args.output)
        print(f"{args.input} -> {args.output}")


if __name__ == "__main__":
    main()
