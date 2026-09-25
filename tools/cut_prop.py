"""Cut a prop out of a scene (e.g. the north star) onto a transparent background.

A plain colour key can't separate a green bush from green grass, so this
flood-fills inwards from the crop's border through "background" colours only;
the prop's dark outline stops the fill, so the prop's own colours inside the
outline survive even when they match the background.

Usage:
    python tools/cut_prop.py art/final/north_star/ns_meadow_village_r2_mix.png 58 120 81 147 art/final/obj_bush_ns1.png
    python tools/cut_prop.py scene.png X0 Y0 X1 Y1 out.png --bg 547e64 374e4a 313638 966c6c --largest

X0 Y0 X1 Y1 is the crop box, inclusive. --bg lists the background colours
(default: the meadow grass, tufts and grass shadow). Isolated background-coloured
specks left touching nothing are removed too. --largest keeps only the biggest
connected shape, dropping detached scraps (tree trunks, bits of a neighbour).
"""

import argparse
import sys
from pathlib import Path

from PIL import Image

DEFAULT_BG = ["547e64", "374e4a", "313638"]


def parse_colour(text):
    text = text.strip().lstrip("#")
    if len(text) != 6:
        sys.exit(f"Expected RRGGBB, got {text!r}")
    return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))


def main():
    parser = argparse.ArgumentParser(description="Cut a prop out of a scene by flood-filling its background.")
    parser.add_argument("scene", type=Path)
    parser.add_argument("box", nargs=4, type=int, metavar=("X0", "Y0", "X1", "Y1"))
    parser.add_argument("output", type=Path)
    parser.add_argument("--bg", nargs="+", default=DEFAULT_BG, metavar="RRGGBB")
    parser.add_argument("--largest", action="store_true", help="keep only the largest connected shape")
    args = parser.parse_args()

    x0, y0, x1, y1 = args.box
    crop = Image.open(args.scene).convert("RGBA").crop((x0, y0, x1 + 1, y1 + 1))
    pixels = crop.load()
    w, h = crop.size
    background = {parse_colour(c) for c in args.bg}

    def is_bg(x, y):
        return pixels[x, y][:3] in background

    border = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    seen = {p for p in border if is_bg(*p)}
    stack = list(seen)
    while stack:
        x, y = stack.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and is_bg(nx, ny):
                seen.add((nx, ny))
                stack.append((nx, ny))
    for x, y in seen:
        pixels[x, y] = (0, 0, 0, 0)

    # Drop leftover specks: opaque pixels with no opaque 4-neighbour.
    specks = [(x, y) for y in range(h) for x in range(w) if pixels[x, y][3]
              and not any(0 <= nx < w and 0 <= ny < h and pixels[nx, ny][3]
                          for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))]
    for x, y in specks:
        pixels[x, y] = (0, 0, 0, 0)

    if args.largest:
        remaining = {(x, y) for y in range(h) for x in range(w) if pixels[x, y][3]}
        best = set()
        while remaining:
            start = remaining.pop()
            part, stack = {start}, [start]
            while stack:
                x, y = stack.pop()
                for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if n in remaining:
                        remaining.discard(n)
                        part.add(n)
                        stack.append(n)
            if len(part) > len(best):
                best = part
        for y in range(h):
            for x in range(w):
                if pixels[x, y][3] and (x, y) not in best:
                    pixels[x, y] = (0, 0, 0, 0)

    bbox = crop.getchannel("A").getbbox()
    if not bbox:
        sys.exit("Nothing left after removing the background")
    crop = crop.crop(bbox)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    crop.save(args.output)
    print(f"{args.output}: {crop.width}x{crop.height} (removed {len(seen)} background px, {len(specks)} specks)")


if __name__ == "__main__":
    main()
