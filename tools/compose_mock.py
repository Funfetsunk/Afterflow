"""Compose a 480x270 mock screenshot from art/final/ assets.

The scene is described by a JSON layout file. Items are drawn in list
order, so later items sit on top of earlier ones. Coordinates are in
game pixels (top-left origin). "cell" is a shortcut for 32px tile
positions: [col, row] means x = col * 32, y = row * 32.

    {
      "background": "#2e222f",
      "items": [
        {"image": "art/final/tile_grass.png", "fill": [0, 0, 480, 270]},
        {"image": "art/final/tile_path.png", "cell": [3, 4]},
        {"image": "art/final/chr_awa_b_idle_s.png", "at": [200, 120]},
        {"image": "art/final/sheet.png", "at": [260, 120], "crop": [0, 0, 48, 48], "flip": true}
      ]
    }

Item keys:
    image   path to a PNG, relative to the project root; must be in art/final/
    at      [x, y] top-left position in pixels
    cell    [col, row] top-left position in 32px tiles (instead of "at")
    fill    [x, y, w, h] repeat the image to cover this rectangle
    crop    [x, y, w, h] use only this part of the image (e.g. one frame of a sheet)
    flip    true to mirror horizontally

Usage:
    python tools/compose_mock.py tools/mock_layouts/meadow_village.json
    python tools/compose_mock.py layout.json -o art/mocks/mock_meadow_village_v1.png
    python tools/compose_mock.py layout.json --drain          # full drain
    python tools/compose_mock.py layout.json --drain 0.5      # half strength

Writes <name>.png at 1x (480x270) and <name>_4x.png at 1920x1080 using
nearest-neighbour scaling. Without -o, the output is
art/mocks/mock_<layout name>.png, with "_drained" added when --drain is on.

The drain is only a preview of the Godot shader (Art Bible 8.1): it
desaturates and shifts colours towards cold blue-grey. Its output is not
palette-locked, just as the shader's won't be.
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageColor, ImageOps

ROOT = Path(__file__).resolve().parent.parent
FINAL_DIR = ROOT / "art" / "final"
MOCKS_DIR = ROOT / "art" / "mocks"
WIDTH, HEIGHT = 480, 270
TILE = 32
SCALE = 4

# Drain tuning: how far colours move towards grey, and the cold tint
# applied to that grey. Both are scaled by the --drain strength.
DRAIN_DESATURATION = 0.75
DRAIN_TINT = (0.80, 0.90, 1.05)  # multipliers on luminance: cold blue-grey


def load_item_image(item, number):
    """Open an item's image, enforcing the art/final/ rule, and apply crop/flip."""
    if "image" not in item:
        sys.exit(f"Item {number}: missing \"image\"")
    path = (ROOT / item["image"]).resolve()
    if not path.is_relative_to(FINAL_DIR):
        sys.exit(f"Item {number}: {item['image']} is not in art/final/. "
                 "Mocks may only use palette-remapped final assets.")
    if not path.is_file():
        sys.exit(f"Item {number}: {item['image']} not found")

    image = Image.open(path).convert("RGBA")
    if "crop" in item:
        x, y, w, h = item["crop"]
        image = image.crop((x, y, x + w, y + h))
    if item.get("flip"):
        image = ImageOps.mirror(image)
    return image


def compose(layout):
    background = ImageColor.getrgb(layout.get("background", "#000000"))
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), background + (255,))

    for number, item in enumerate(layout.get("items", []), start=1):
        image = load_item_image(item, number)
        w, h = image.size

        if "fill" in item:
            fx, fy, fw, fh = item["fill"]
            tiled = Image.new("RGBA", (fw, fh))
            for y in range(0, fh, h):
                for x in range(0, fw, w):
                    tiled.paste(image, (x, y))
            canvas.alpha_composite(tiled, (fx, fy))
            continue

        if "cell" in item:
            x, y = item["cell"][0] * TILE, item["cell"][1] * TILE
        elif "at" in item:
            x, y = item["at"]
        else:
            sys.exit(f"Item {number}: needs \"at\", \"cell\" or \"fill\"")

        if x >= WIDTH or y >= HEIGHT or x + w <= 0 or y + h <= 0:
            print(f"Warning: item {number} ({item['image']}) is entirely off screen")
            continue
        # alpha_composite can't take negative offsets, so paste via a layer.
        layer = Image.new("RGBA", (WIDTH, HEIGHT))
        layer.paste(image, (x, y))
        canvas = Image.alpha_composite(canvas, layer)

    return canvas.convert("RGB")


def drain(image, strength):
    """Desaturate and shift towards cold blue-grey. strength 0..1."""
    desaturation = DRAIN_DESATURATION * strength
    result = image.copy()
    pixels = result.load()
    for y in range(result.height):
        for x in range(result.width):
            r, g, b = pixels[x, y]
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            cold = [luminance * t for t in DRAIN_TINT]
            pixels[x, y] = tuple(
                max(0, min(255, round(c + (k - c) * desaturation)))
                for c, k in zip((r, g, b), cold)
            )
    return result


def main():
    parser = argparse.ArgumentParser(description="Compose a 480x270 mock from art/final/ assets.")
    parser.add_argument("layout", type=Path, help="JSON layout file")
    parser.add_argument("-o", "--output", type=Path, help="1x output path (default: art/mocks/mock_<layout name>.png)")
    parser.add_argument("--drain", type=float, nargs="?", const=1.0, default=None, metavar="STRENGTH",
                        help="simulate the drain, strength 0..1 (default 1 when the flag is given)")
    args = parser.parse_args()

    if args.drain is not None and not 0 <= args.drain <= 1:
        sys.exit("--drain strength must be between 0 and 1")

    try:
        layout = json.loads(args.layout.read_text())
    except (OSError, json.JSONDecodeError) as error:
        sys.exit(f"Can't read layout {args.layout}: {error}")

    mock = compose(layout)
    if args.drain is not None:
        mock = drain(mock, args.drain)

    output = args.output
    if output is None:
        suffix = "_drained" if args.drain is not None else ""
        output = MOCKS_DIR / f"mock_{args.layout.stem}{suffix}.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    output_4x = output.with_name(f"{output.stem}_4x{output.suffix}")

    mock.save(output)
    mock.resize((WIDTH * SCALE, HEIGHT * SCALE), Image.NEAREST).save(output_4x)
    print(f"{output} ({WIDTH}x{HEIGHT})")
    print(f"{output_4x} ({WIDTH * SCALE}x{HEIGHT * SCALE})")


if __name__ == "__main__":
    main()
