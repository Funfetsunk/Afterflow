"""Rebuild a character's hair as a clean 3-tone ramp, lit from the top left.

PixelLab often draws small-sprite hair as one flat colour, and palette passes
can leave stray off-tone pixels in it (Art Bible §4.3: Awa's hair must be a
clean ginger ramp). This finds the hair by colour, keeps only the region(s)
connected to the top of the sprite (so a hand or satchel in the same colour is
left alone), and repaints it:

    light  on pixels whose neighbour above is not hair (the lit crown)
    dark   then on pixels whose neighbour below or to the right is not hair
    light  then on pixels whose neighbour to the left is not hair
    base   everywhere else
Thin strands framing the face therefore come out dark, like 16-bit hair shading.

Usage:
    python tools/hair_ramp.py in.png out.png --hair 9e4539 --ramp e6904e cd683d 9e4539
    python tools/hair_ramp.py in.png out.png --hair 9e4539 --ramp e6904e cd683d 9e4539 --map c4bbb5=fdcbb0

--hair takes one or more source colours that make up the hair. --ramp is
light, base, dark. --map applies extra exact colour swaps afterwards (e.g. eye
whites). Run it on art/final/ frames, after palette_remap.py.
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
    parser = argparse.ArgumentParser(description="Repaint hair as a clean light/base/dark ramp.")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--hair", nargs="+", required=True, metavar="RRGGBB")
    parser.add_argument("--ramp", nargs=3, required=True, metavar=("LIGHT", "BASE", "DARK"))
    parser.add_argument("--map", nargs="+", default=[], metavar="FROM=TO")
    args = parser.parse_args()

    hair_colours = {parse_colour(c) for c in args.hair}
    light, base, dark = (parse_colour(c) for c in args.ramp)

    image = Image.open(args.input).convert("RGBA")
    pixels = image.load()
    w, h = image.size
    bbox = image.getchannel("A").getbbox()
    if not bbox:
        sys.exit("Empty image")

    def is_hair_colour(x, y):
        return 0 <= x < w and 0 <= y < h and pixels[x, y][3] and pixels[x, y][:3] in hair_colours

    # Flood fill from hair pixels in the top two rows of the sprite (the head).
    seeds = [(x, y) for y in range(bbox[1], min(bbox[1] + 2, bbox[3])) for x in range(w) if is_hair_colour(x, y)]
    hair, stack = set(seeds), list(seeds)
    while stack:
        x, y = stack.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (nx, ny) not in hair and is_hair_colour(nx, ny):
                hair.add((nx, ny))
                stack.append((nx, ny))
    if not hair:
        sys.exit("No hair found at the top of the sprite")

    counts = {"light": 0, "base": 0, "dark": 0}
    for x, y in hair:
        a = pixels[x, y][3]
        if (x, y - 1) not in hair:
            pixels[x, y] = light + (a,)
            counts["light"] += 1
        elif (x, y + 1) not in hair or (x + 1, y) not in hair:
            pixels[x, y] = dark + (a,)
            counts["dark"] += 1
        elif (x - 1, y) not in hair:
            pixels[x, y] = light + (a,)
            counts["light"] += 1
        else:
            pixels[x, y] = base + (a,)
            counts["base"] += 1

    swaps = {}
    for pair in args.map:
        source, target = pair.split("=", 1)
        swaps[parse_colour(source)] = parse_colour(target)
    swapped = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a and (r, g, b) in swaps:
                pixels[x, y] = swaps[(r, g, b)] + (a,)
                swapped += 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    print(f"{args.input} -> {args.output}: hair {len(hair)} px "
          f"(light {counts['light']}, base {counts['base']}, dark {counts['dark']}), swapped {swapped} px")


if __name__ == "__main__":
    main()
