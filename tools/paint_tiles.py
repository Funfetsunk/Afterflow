"""Paint stamps and fence runs into a mock layout as 16px grid cells.

Usage:
    python tools/paint_tiles.py layout.json stamp oak_a 4 6
    python tools/paint_tiles.py layout.json fence 3 5 6
    python tools/paint_tiles.py layout.json ruin 2 6 end_l high full mid low end_r

stamp NAME COL ROW   place a stamp from tools/kits/stamps.json; COL ROW is the
                     cell of its bottom-left tile (stamps sit on their base)
fence COL ROW LEN    a fence run of LEN posts from tools/kits/fence16.json:
                     LEN-1 post-and-rail tiles then an end post
ruin COL ROW TYPE... a crumbled wall run from tools/kits/ruin16.json, one column
                     per TYPE (full high mid low stub end_l end_r), 2 tiles tall
                     with ROW as its top row; variants a/b/c rotate by column,
                     and the last column carries a slim cast shadow on its right

Items are appended to the layout; re-run compose_mock.py after.
"""

import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Paint stamps and fence runs into a mock layout.")
    parser.add_argument("layout", type=Path)
    parser.add_argument("kind", choices=["stamp", "fence", "ruin"])
    parser.add_argument("args", nargs="+")
    args = parser.parse_args()

    layout = json.loads(args.layout.read_text()) if args.layout.exists() else {"items": []}
    items = []
    if args.kind == "stamp":
        name, col, row = args.args[0], int(args.args[1]), int(args.args[2])
        stamps = json.loads(Path("tools/kits/stamps.json").read_text())
        if name not in stamps:
            sys.exit(f"Unknown stamp {name!r}; have {sorted(stamps)}")
        stamp = stamps[name]
        top = row - stamp["rows"] + 1
        for r, tile_row in enumerate(stamp["tiles"]):
            for c, tile in enumerate(tile_row):
                items.append({"image": tile, "cell": [col + c, top + r]})
    elif args.kind == "ruin":
        col, row, kinds = int(args.args[0]), int(args.args[1]), args.args[2:]
        kit = json.loads(Path("tools/kits/ruin16.json").read_text())["tiles"]
        for i, kind in enumerate(kinds):
            variant = "abc"[(col + i) % 3] + ("_shadow" if i == len(kinds) - 1 else "")
            for part, dr in (("top", 0), ("bot", 1)):
                key = f"ruin_{kind}_{variant}_{part}"
                if key not in kit:
                    sys.exit(f"Unknown ruin column {kind!r}")
                items.append({"image": kit[key], "cell": [col + i, row + dr]})
    else:
        col, row, length = (int(a) for a in args.args[:3])
        if length < 2:
            sys.exit("A fence needs at least 2 posts")
        kit = json.loads(Path("tools/kits/fence16.json").read_text())["tiles"]
        for i in range(length - 1):
            items.append({"image": kit["fence_m"], "cell": [col + i, row]})
        items.append({"image": kit["fence_end"], "cell": [col + length - 1, row]})

    layout["items"].extend(items)
    args.layout.write_text(json.dumps(layout, indent=1))
    print(f"{args.layout}: +{len(items)} tiles ({args.kind} {' '.join(args.args)})")


if __name__ == "__main__":
    main()
