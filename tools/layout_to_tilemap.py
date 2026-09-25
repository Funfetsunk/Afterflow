"""Convert a compose_mock.py layout into TileMapLayer data for the meadow TileSet.

Maps are designed with the same tools as the mocks (wang_layout.py, paint_*.py),
so a map that looks right as a mock is painted into Godot cell for cell. Every
layout tile is looked up in the exported atlases (tools/export_assets.py) and
becomes (source id, atlas cell) in resources/tilesets/meadow.tres:

  ground       the Wang terrain tiles, fill/ledge extras and the lane crossing
  objects_1..n everything painted on top, in painter's order; when a cell is
               already taken, the tile goes to the next objects layer, so
               overlaps (a roof over a tree crown) survive

Sprites placed with "at" (characters) are skipped; they are scene nodes.

Writes <out>.json with, per layer, the cells and the TileMapLayer.tile_map_data
bytes (base64, Godot's format: uint16 version 0, then per cell int16 x, int16 y,
uint16 source, uint16 atlas x, uint16 atlas y, uint16 alternative, little-endian),
plus a full-size preview PNG of the map.

Usage (from the project root, after build_tileset.py):
    python tools/layout_to_tilemap.py tools/mock_layouts/p1_meadow.json resources/maps/p1_meadow
"""

import argparse
import base64
import json
import struct
import sys
from pathlib import Path

from PIL import Image

T = 16
TS = Path("assets/tilesets")
KITS = Path("tools/kits")
SHEETS = {"art/final/ts_meadow_grass-path_opt3_ns.png": 0, "art/final/ts_meadow_grass-water_opt2_ns.png": 1}
KIT_SOURCES = {"cottage16": 3, "fence16": 4, "ruin16": 5, "forest16": 6}
FORD_CELLS = set()                               # the lane crossing is ground, not an object
TEXTURES = {0: "terrain/meadow_grass_path.png", 1: "terrain/meadow_grass_water.png", 2: "terrain/meadow_extras.png",
            3: "cottage16.png", 4: "fence16.png", 5: "ruin16.png", 6: "forest16.png", 7: "stamps.png"}


def build_lookup():
    """image path (as written in layouts) -> (source id, (atlas x, atlas y))"""
    lookup = {}
    extras = json.loads((TS / "terrain" / "meadow_extras.json").read_text())["tiles"]
    for i in range(8):
        lookup[f"art/final/ts_meadow_grass-fill_ns{i}.png"] = (2, tuple(extras[f"grass_fill_{i}"]))
    for i in range(7):
        lookup[f"art/final/ts_meadow_ledge_ns_top{i}.png"] = (2, tuple(extras[f"ledge_top_{i}"]))
        lookup[f"art/final/ts_meadow_ledge_ns_bot{i}.png"] = (2, tuple(extras[f"ledge_bot_{i}"]))
    for kit, sid in KIT_SOURCES.items():
        index = json.loads((KITS / f"{kit}.json").read_text())
        paths = index.get("tiles", index)
        cells = json.loads((TS / f"{kit}.json").read_text())["tiles"]
        for name, path in paths.items():
            lookup[path] = (sid, tuple(cells[name]))
    stamps = json.loads((KITS / "stamps.json").read_text())
    blocks = json.loads((TS / "stamps.json").read_text())["stamps"]
    for name, s in stamps.items():
        ox, oy = blocks[name]["origin"]
        for r, row in enumerate(s["tiles"]):
            for c, path in enumerate(row):
                lookup[path] = (7, (ox + c, oy + r))
    for path in (p for row in stamps["ford"]["tiles"] for p in row):
        FORD_CELLS.add(lookup[path])
    return lookup


def encode(cells):
    data = bytearray(struct.pack("<H", 0))
    for (x, y), (sid, (ax, ay)) in sorted(cells.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        data += struct.pack("<hhHHHH", x, y, sid, ax, ay, 0)
    return base64.b64encode(bytes(data)).decode()


def main():
    parser = argparse.ArgumentParser(description="Layout JSON -> TileMapLayer data for the meadow TileSet.")
    parser.add_argument("layout", type=Path)
    parser.add_argument("out", type=Path, help="output path without extension")
    args = parser.parse_args()

    lookup = build_lookup()
    ground, objects, skipped = {}, [], 0
    for item in json.loads(args.layout.read_text())["items"]:
        if "cell" not in item:
            skipped += 1
            continue
        cell = tuple(item["cell"])
        img = item["image"]
        if img in SHEETS:
            x, y, _, _ = item["crop"]
            ground[cell] = (SHEETS[img], (x // T, y // T))
            continue
        if img not in lookup:
            sys.exit(f"No atlas tile for {img}; re-run tools/export_assets.py and tools/build_tileset.py")
        entry = lookup[img]
        if entry[0] == 2 or entry in FORD_CELLS:
            ground[cell] = entry
            continue
        for layer in objects:
            if cell not in layer:
                layer[cell] = entry
                break
        else:
            objects.append({cell: entry})

    layers = {"ground": ground}
    layers.update({f"objects_{i + 1}": layer for i, layer in enumerate(objects)})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out = {name: {"cells": len(cells), "tile_map_data": encode(cells)} for name, cells in layers.items()}
    Path(f"{args.out}.json").write_text(json.dumps(out, indent=1) + "\n")

    xs = [x for layer in layers.values() for x, _ in layer]
    ys = [y for layer in layers.values() for _, y in layer]
    w, h = (max(xs) + 1) * T, (max(ys) + 1) * T
    preview = Image.new("RGBA", (w, h), (0x2e, 0x22, 0x2f, 255))
    atlases = {sid: Image.open(TS / tex).convert("RGBA") for sid, tex in TEXTURES.items()}
    for layer in layers.values():
        for (x, y), (sid, (ax, ay)) in layer.items():
            if x >= 0 and y >= 0:
                preview.alpha_composite(atlases[sid].crop((ax * T, ay * T, (ax + 1) * T, (ay + 1) * T)), (x * T, y * T))
    preview.save(f"{args.out}_preview.png")
    print(f"{args.out}.json: " + ", ".join(f"{n} {len(c)}" for n, c in layers.items())
          + f"; {skipped} sprite items skipped; preview {w}x{h}")


if __name__ == "__main__":
    main()
