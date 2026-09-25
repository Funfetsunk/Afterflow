"""Assemble a cottage sprite from vertical slices cut from the north star.

The north star's long cottage is cut into full-height slices (ridge, slate
roof, eave and wall run through every slice), listed in a kit JSON such as
tools/kits/cottage_ns.json. Any sequence of slices is a valid cottage, so one
kit paints houses of any length, with the door, windows and chimney wherever
you want them: the RPG Maker idea, in the north star's own pixels.

Usage:
    python tools/build_cottage.py tools/kits/cottage_ns.json out.png end_l wall_a door window_small end_r
    python tools/build_cottage.py kit.json out.png end_l window_big post window_small_b door end_r --chimney 57

Arguments after the output are slice names, left to right. Start with end_l
and finish with end_r. --chimney X places the kit's chimney piece on the
ridge with its left edge X pixels from the cottage's left edge (repeatable;
omit for no chimney). --recolour applies exact colour swaps to the result,
using palette colours only.
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image


def parse_colour(text):
    text = text.strip().lstrip("#")
    if len(text) != 6:
        sys.exit(f"Expected RRGGBB, got {text!r}")
    return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))


def main():
    parser = argparse.ArgumentParser(description="Assemble a cottage from north-star slices.")
    parser.add_argument("kit", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("slices", nargs="+", help="slice names, left to right")
    parser.add_argument("--chimney", type=int, action="append", default=[], metavar="X",
                        help="place a chimney with its left edge X px from the left")
    parser.add_argument("--recolour", nargs="+", default=[], metavar="FROM=TO")
    args = parser.parse_args()

    kit = json.loads(args.kit.read_text())
    unknown = [s for s in args.slices if s not in kit["slices"]]
    if unknown:
        sys.exit(f"Unknown slice(s) {unknown}; the kit has {sorted(kit['slices'])}")

    parts = [Image.open(kit["slices"][s]).convert("RGBA") for s in args.slices]
    width = sum(p.width for p in parts)
    cottage = Image.new("RGBA", (width, kit["height"]), (0, 0, 0, 0))
    x = 0
    for part in parts:
        cottage.alpha_composite(part, (x, 0))
        x += part.width

    if args.chimney:
        if "chimney" not in kit:
            sys.exit("This kit has no chimney piece")
        chimney = Image.open(kit["chimney"]["image"]).convert("RGBA")
        for cx in args.chimney:
            if not 0 <= cx <= width - chimney.width:
                sys.exit(f"--chimney {cx} is off the roof (0..{width - chimney.width})")
            cottage.alpha_composite(chimney, (cx, kit["chimney"]["y"]))

    swaps = {}
    for pair in args.recolour:
        source, target = pair.split("=", 1)
        swaps[parse_colour(source)] = parse_colour(target)
    if swaps:
        pixels = cottage.load()
        for y in range(cottage.height):
            for x in range(cottage.width):
                r, g, b, a = pixels[x, y]
                if a and (r, g, b) in swaps:
                    pixels[x, y] = swaps[(r, g, b)] + (a,)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    cottage.save(args.output)
    print(f"{args.output}: {width}x{kit['height']} from {len(parts)} slices")


if __name__ == "__main__":
    main()
