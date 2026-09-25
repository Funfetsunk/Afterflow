"""Paint a cottage from the 16px kit onto a mock layout, tile by tile.

Adds tile placements ("cell" items) to a compose_mock.py layout JSON, the way
Godot's TileMap layers will hold them: a roof layer (nine-slice), a wall layer
(2 rows), the cast shadow on the grass to the right, and optional chimney
stamps over the roof's top row. Lead a path up to each door with the terrain tiles.

Usage:
    python tools/paint_cottage16.py layout.json --at 3 2 --walls l window_big door m r --roof 3 --chimney 3
    python tools/paint_cottage16.py layout.json --at 12 1 --walls l door window_small r --roof 2

--at COL ROW    grid cell of the roof's top-left tile
--walls ...     wall columns, left to right: l, m, r, window_big, window_small, door
--roof N        roof depth in tiles (2 = top + bottom, 3+ adds middle rows)
--chimney C     place a chimney over roof column C (0 = leftmost); repeatable
--kit PATH      kit JSON (default tools/kits/cottage16.json)

The cottage is len(walls) tiles wide and roof + 2 tiles tall. Items are
appended in painter's order (roof, wall, chimney); re-run compose_mock.py after.
"""

import argparse
import json
import sys
from pathlib import Path

WALL_KEYS = {"l": "wall_l", "m": "wall_m", "r": "wall_r",
             "window_big": "window_big", "window_small": "window_small", "door": "door"}


def main():
    parser = argparse.ArgumentParser(description="Paint a 16px-kit cottage into a mock layout.")
    parser.add_argument("layout", type=Path)
    parser.add_argument("--at", nargs=2, type=int, required=True, metavar=("COL", "ROW"))
    parser.add_argument("--walls", nargs="+", required=True)
    parser.add_argument("--roof", type=int, default=3)
    parser.add_argument("--chimney", type=int, action="append", default=[])
    parser.add_argument("--kit", type=Path, default=Path("tools/kits/cottage16.json"))
    args = parser.parse_args()

    tiles = json.loads(args.kit.read_text())["tiles"]
    width = len(args.walls)
    if width < 2 or args.walls[0] != "l" or args.walls[-1] != "r":
        sys.exit("--walls must start with l and end with r (at least 2 columns)")
    if args.roof < 2:
        sys.exit("--roof must be at least 2")
    unknown = [w for w in args.walls if w not in WALL_KEYS]
    if unknown:
        sys.exit(f"Unknown wall column(s) {unknown}; use {sorted(WALL_KEYS)}")

    c0, r0 = args.at
    items = []

    def place(name, col, row):
        items.append({"image": tiles[name], "cell": [col, row]})

    for r in range(args.roof):
        band = "top" if r == 0 else "bot" if r == args.roof - 1 else "mid"
        for c in range(width):
            side = "l" if c == 0 else "r" if c == width - 1 else "m"
            place(f"roof_{band}_{side}", c0 + c, r0 + r)
    for c, key in enumerate(args.walls):
        place(f"{WALL_KEYS[key]}_top", c0 + c, r0 + args.roof)
        place(f"{WALL_KEYS[key]}_bot", c0 + c, r0 + args.roof + 1)
    # cast shadow on the grass to the right: roof rows below the top, then both wall rows
    for r in range(1, args.roof):
        if r < args.roof - 1:
            place("shadow_roof_mid", c0 + width, r0 + r)
        else:
            place("shadow_roof_bot_full" if args.roof > 2 else "shadow_roof_bot", c0 + width, r0 + r)
    place("shadow_wall_top", c0 + width, r0 + args.roof)
    place("shadow_wall_bot", c0 + width, r0 + args.roof + 1)
    for c in args.chimney:
        if not 0 <= c < width:
            sys.exit(f"--chimney {c} is outside the roof (0..{width - 1})")
        for k in range(3):
            place(f"chimney_{k}", c0 + c, r0 - 2 + k)

    layout = json.loads(args.layout.read_text()) if args.layout.exists() else {"items": []}
    layout["items"].extend(items)
    args.layout.write_text(json.dumps(layout, indent=1))
    print(f"{args.layout}: +{len(items)} tiles, cottage {width}x{args.roof + 2} at {c0},{r0}")


if __name__ == "__main__":
    main()
