"""Swap exact colours in palette-remapped sprites.

For fixing one element that PixelLab keeps getting wrong (e.g. Awa's scarf)
without regenerating. Run it on art/final/ files, after palette_remap.py, and
use palette colours as targets so the result stays on the palette. Record the
mapping in ASSET_MANIFEST.md so the fix can be repeated on new frames.

Alpha is left untouched. Colours not in the mapping are left untouched.

--strip-ground: removes a ground patch baked under an object. Per column, from
the bottom up, pixels of the given colours (plus a dark outline colour sitting
directly under them) are made transparent until the first other pixel, so the
same colours higher up (e.g. moss on stones) are kept.

Usage:
    python tools/recolour.py in.png out.png --map 547e64=4d65b4 374e4a=484a77
    python tools/recolour.py in.png out.png --strip-ground 4c3e24 676633 a2a947 --ground-outline 2e222f
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
    parser.add_argument("--map", nargs="+", default=[], metavar="FROM=TO",
                        help="colour pairs as RRGGBB=RRGGBB")
    parser.add_argument("--strip-ground", nargs="+", default=[], metavar="RRGGBB",
                        help="ground colours to clear from the bottom of each column")
    parser.add_argument("--ground-outline", metavar="RRGGBB",
                        help="outline colour to clear when it sits under ground colours")
    parser.add_argument("--dry-run", action="store_true", help="count pixels without writing")
    args = parser.parse_args()
    if not args.map and not args.strip_ground:
        parser.error("give --map and/or --strip-ground")

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

    if args.strip_ground:
        ground = {parse_colour(c) for c in args.strip_ground}
        outline = parse_colour(args.ground_outline) if args.ground_outline else None
        cleared = 0
        for x in range(image.width):
            y = image.height - 1
            while y >= 0:
                r, g, b, a = pixels[x, y]
                above = pixels[x, y - 1] if y > 0 else (0, 0, 0, 0)
                is_outline = (outline is not None and (r, g, b) == outline
                              and above[3] and above[:3] in ground)
                if a and not ((r, g, b) in ground or is_outline):
                    break
                if a:
                    pixels[x, y] = (0, 0, 0, 0)
                    cleared += 1
                y -= 1
        # Trim "drips": bottom pixels left hanging with nothing beside or below them.
        for _ in range(4):
            drips = []
            for x in range(image.width):
                for y in range(image.height):
                    if not pixels[x, y][3]:
                        continue
                    side = [pixels[nx, y][3] for nx in (x - 1, x + 1) if 0 <= nx < image.width]
                    below = pixels[x, y + 1][3] if y + 1 < image.height else 0
                    if not any(side) and not below:
                        drips.append((x, y))
            for x, y in drips:
                pixels[x, y] = (0, 0, 0, 0)
            cleared += len(drips)
        print(f"ground cleared: {cleared} px")
    if not args.dry_run:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        image.save(args.output)
        print(f"{args.input} -> {args.output}")


if __name__ == "__main__":
    main()
