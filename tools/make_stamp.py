"""Turn a prop sprite into a fixed tile stamp on the 16px grid.

Everything in the world is tiles (Art Bible §2). A single tree, bush or
standing stone is a "fixed stamp": a small block of 16x16 tiles placed together.
This pads the sprite to whole tiles (anchored bottom-centre, so its base sits
on a grid line), splits it, and records it in tools/kits/stamps.json.

Usage:
    python tools/make_stamp.py art/final/obj_bush_ns1.png bush_a
    python tools/make_stamp.py art/final/obj_tree_oak.png oak_a --out art/final/tiles/stamps

Writes <out>/<name>_r<row>c<col>.png and adds {"cols", "rows", "tiles"} under
<name> in tools/kits/stamps.json. Paint with tools/paint_tiles.py stamp.
"""

import argparse
import json
import math
from pathlib import Path

from PIL import Image

TILE = 16
REGISTRY = Path("tools/kits/stamps.json")


def main():
    parser = argparse.ArgumentParser(description="Pad a prop to whole 16px tiles and split it into a stamp.")
    parser.add_argument("sprite", type=Path)
    parser.add_argument("name")
    parser.add_argument("--out", type=Path, default=Path("art/final/tiles/stamps"))
    args = parser.parse_args()

    sprite = Image.open(args.sprite).convert("RGBA")
    sprite = sprite.crop(sprite.getchannel("A").getbbox())
    cols = math.ceil(sprite.width / TILE)
    rows = math.ceil(sprite.height / TILE)
    canvas = Image.new("RGBA", (cols * TILE, rows * TILE), (0, 0, 0, 0))
    canvas.alpha_composite(sprite, ((canvas.width - sprite.width) // 2, canvas.height - sprite.height))

    args.out.mkdir(parents=True, exist_ok=True)
    tiles = []
    for r in range(rows):
        row = []
        for c in range(cols):
            path = args.out / f"{args.name}_r{r}c{c}.png"
            canvas.crop((c * TILE, r * TILE, (c + 1) * TILE, (r + 1) * TILE)).save(path)
            row.append(path.as_posix())
        tiles.append(row)

    registry = json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {}
    registry[args.name] = {"cols": cols, "rows": rows, "source": args.sprite.as_posix(), "tiles": tiles}
    REGISTRY.write_text(json.dumps(registry, indent=1))
    print(f"{args.name}: {cols}x{rows} tiles from {args.sprite}")


if __name__ == "__main__":
    main()
