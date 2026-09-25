"""Remap images to a fixed palette.

Every visible pixel is replaced by the nearest colour in the palette.
Alpha is preserved exactly, and fully transparent pixels are cleared to
(0, 0, 0, 0) so stray hidden colours don't linger in the file.

Distance is "redmean" weighted RGB, a cheap approximation of perceived
colour difference that behaves better than plain RGB distance on greens
and skin tones.

Usage:
    python tools/palette_remap.py art/raw/<file>.png art/final/<file>.png
    python tools/palette_remap.py art/raw art/final            # whole folder
    python tools/palette_remap.py art/raw art/final --palette tools/palettes/custom.hex

Folder mode walks the input folder recursively, remaps every .png and
mirrors the folder structure in the output, so switching palettes is a
single re-run over art/raw/.

Palette files use the Lospec .hex format: one RRGGBB colour per line.
Blank lines and lines starting with ';' or '//' are ignored.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image

DEFAULT_PALETTE = Path(__file__).parent / "palettes" / "resurrect-64.hex"


def load_palette(path):
    """Return the palette as a list of (r, g, b) tuples."""
    colours = []
    for number, line in enumerate(Path(path).read_text().splitlines(), start=1):
        line = line.strip().lstrip("#")
        if not line or line.startswith((";", "//")):
            continue
        if len(line) != 6:
            sys.exit(f"{path}:{number}: expected RRGGBB, got {line!r}")
        try:
            colours.append(tuple(int(line[i:i + 2], 16) for i in (0, 2, 4)))
        except ValueError:
            sys.exit(f"{path}:{number}: expected RRGGBB, got {line!r}")
    if not colours:
        sys.exit(f"{path}: palette is empty")
    return colours


def nearest(colour, palette):
    """Return the palette entry closest to colour (redmean distance)."""
    r, g, b = colour

    def distance(entry):
        pr, pg, pb = entry
        mean_red = (r + pr) / 2
        dr, dg, db = r - pr, g - pg, b - pb
        return ((2 + mean_red / 256) * dr * dr
                + 4 * dg * dg
                + (2 + (255 - mean_red) / 256) * db * db)

    return min(palette, key=distance)


def remap_image(source, destination, palette):
    """Remap one image. Returns (colours before, colours after)."""
    image = Image.open(source).convert("RGBA")
    result = Image.new("RGBA", image.size)
    source_pixels, result_pixels = image.load(), result.load()
    cache = {}
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = source_pixels[x, y]
            if a == 0:
                continue  # new image is already (0, 0, 0, 0)
            if (r, g, b) not in cache:
                cache[(r, g, b)] = nearest((r, g, b), palette)
            result_pixels[x, y] = cache[(r, g, b)] + (a,)

    destination.parent.mkdir(parents=True, exist_ok=True)
    result.save(destination)
    return len(cache), len(set(cache.values()))


def main():
    parser = argparse.ArgumentParser(description="Remap images to a fixed palette.")
    parser.add_argument("input", type=Path, help="a .png file or a folder of them")
    parser.add_argument("output", type=Path, help="output .png file, or output folder in folder mode")
    parser.add_argument("--palette", type=Path, default=DEFAULT_PALETTE,
                        help=f"palette .hex file (default: {DEFAULT_PALETTE.name})")
    args = parser.parse_args()

    palette = load_palette(args.palette)

    if args.input.is_dir():
        jobs = [(path, args.output / path.relative_to(args.input))
                for path in sorted(args.input.rglob("*.png"))]
        if not jobs:
            sys.exit(f"No .png files in {args.input}")
    elif args.input.is_file():
        jobs = [(args.input, args.output)]
    else:
        sys.exit(f"Not found: {args.input}")

    print(f"Palette: {args.palette.name} ({len(palette)} colours)")
    for source, destination in jobs:
        before, after = remap_image(source, destination, palette)
        print(f"{source} -> {destination}  ({before} colours -> {after})")


if __name__ == "__main__":
    main()
