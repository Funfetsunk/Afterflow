"""Build the meadow TileSet resource from the exported atlases in assets/tilesets/.

A Godot TileSet with dozens of atlas tiles, terrain peering bits and collision
polygons can't be set up through the MCP tools, and by hand it's error-prone,
so it is generated from the same JSON indexes tools/export_assets.py writes.
The result is an ordinary TileSet resource: open it in the editor to inspect or
tweak it (and re-run this after exporting new art; hand edits are overwritten).

Sources (ids are stable, so painted maps keep working after a rebuild):
  0 terrain/meadow_grass_path   PixelLab Wang sheet: grass / path
  1 terrain/meadow_grass_water  Wang sheet: grass / bank (ledge face) / water
  2 terrain/meadow_extras       grass fill variants, north-star ledge pairs
  3 cottage16  4 fence16  5 ruin16  6 forest16  7 stamps

Terrain set 0 (match corners): 0 grass, 1 path, 2 water, 3 bank. Painting grass
picks at random among every all-grass tile, weighted by `probability`, so the
fill variants scatter on their own; the north-star ledge pairs outweigh the
sheet's own straight ledge tiles.

Physics layer 0 is `world` (collision layer 1): walls, roofs, trees, fences,
the ledge face. Physics layer 1 is `water` (collision layer 8). Terrain tiles
block per quarter (a bank or water corner blocks its quarter); kit and stamp
tiles block by the rules in main() below.

Stamp cells carry a y_sort_origin at the stamp's base, so on a y-sorted
objects layer Awa walks behind a tree crown or the shrine and in front of
their bases (the gable's shadow column and the lane crossing are left flat).

Usage (from the project root, after tools/export_assets.py):
    python tools/build_tileset.py
Writes resources/tilesets/meadow.tres.
"""

import json
from pathlib import Path

from PIL import Image

T = 16
H = T // 2
TS = Path("assets/tilesets")
OUT = Path("resources/tilesets/meadow.tres")

TERRAINS = [("grass", "0.33, 0.49, 0.39"), ("path", "0.59, 0.42, 0.42"),
            ("water", "0.3, 0.4, 0.71"), ("bank", "0.18, 0.13, 0.18")]
CORNER_BITS = {"NW": "top_left_corner", "NE": "top_right_corner",
               "SW": "bottom_left_corner", "SE": "bottom_right_corner"}
QUARTERS = {"NW": (-H, -H), "NE": (0, -H), "SW": (-H, 0), "SE": (0, 0)}
WORLD, WATER = 0, 1


def rect(x, y, w, h):
    return f"PackedVector2Array({x}, {y}, {x + w}, {y}, {x + w}, {y + h}, {x}, {y + h})"


FULL = rect(-H, -H, T, T)


class Atlas:
    """One TileSetAtlasSource: tiles keyed by atlas cell, each a dict of properties."""

    def __init__(self, sid, texture):
        self.sid, self.texture, self.tiles = sid, texture, {}

    def tile(self, cell):
        return self.tiles.setdefault(tuple(cell), {"polys": []})

    def lines(self):
        out = [f'[sub_resource type="TileSetAtlasSource" id="atlas_{self.sid}"]',
               f'texture = ExtResource("tex_{self.sid}")', f"texture_region_size = Vector2i({T}, {T})"]
        for (x, y), t in sorted(self.tiles.items(), key=lambda kv: (kv[0][1], kv[0][0])):
            k = f"{x}:{y}/0"
            out.append(f"{k} = 0")
            if t.get("y_sort_origin"):
                out.append(f"{k}/y_sort_origin = {t['y_sort_origin']}")
            if "probability" in t:
                out.append(f"{k}/probability = {t['probability']}")
            if "corners" in t:
                names = [TERRAIN_INDEX[c] for c in t["corners"].values()]
                centre = max(set(names), key=lambda n: (names.count(n), -n))
                out.append(f"{k}/terrain_set = 0")
                out.append(f"{k}/terrain = {centre}")
                for corner, bit in CORNER_BITS.items():
                    out.append(f"{k}/terrains_peering_bit/{bit} = {TERRAIN_INDEX[t['corners'][corner]]}")
            counts = {}
            for layer, pts in t["polys"]:
                i = counts.get(layer, 0)
                counts[layer] = i + 1
                out.append(f"{k}/physics_layer_{layer}/polygon_{i}/points = {pts}")
        return out


TERRAIN_INDEX = {}


def terrain_tile(atlas, cell, corners, lower, probability=None):
    """A Wang tile: corners in terms of upper/lower/transition, mapped to terrain ids."""
    names = {"upper": "grass", "lower": lower, "transition": "bank"}
    named = {c: names[v] for c, v in corners.items()}
    t = atlas.tile(cell)
    t["corners"] = named
    if probability is not None:
        t["probability"] = probability
    for c, name in named.items():                      # block the quarters under bank or water
        if name in ("bank", "water"):
            x, y = QUARTERS[c]
            t["polys"].append((WORLD if name == "bank" else WATER, rect(x, y, H, H)))


def coverage(path, cell):
    img = Image.open(path).convert("RGBA").crop((cell[0] * T, cell[1] * T, (cell[0] + 1) * T, (cell[1] + 1) * T))
    return (T * T - img.getchannel("A").histogram()[0]) / (T * T)


def main():
    for i, (name, _) in enumerate(TERRAINS):
        TERRAIN_INDEX[name] = i
    atlases = []

    # 0, 1: Wang sheets
    for sid, (name, lower) in enumerate((("meadow_grass_path", "path"), ("meadow_grass_water", "water"))):
        a = Atlas(sid, f"res://assets/tilesets/terrain/{name}.png")
        for tile in json.loads((TS / "terrain" / f"{name}.json").read_text())["tiles"]:
            corners = tile["corners"]
            key = "".join(corners[c][0] for c in ("NW", "NE", "SW", "SE"))
            prob = 0.25 if key == "uuuu" else 0.05 if key in ("uutt", "ttll") else None
            terrain_tile(a, tile["cell"], corners, lower, prob)
        atlases.append(a)

    # 2: extras (grass fill variants, ledge pairs)
    a = Atlas(2, "res://assets/tilesets/terrain/meadow_extras.png")
    for name, cell in json.loads((TS / "terrain" / "meadow_extras.json").read_text())["tiles"].items():
        if name.startswith("grass_fill"):
            corners = dict.fromkeys(CORNER_BITS, "upper")
        elif name.startswith("ledge_top"):
            corners = {"NW": "upper", "NE": "upper", "SW": "transition", "SE": "transition"}
        else:
            corners = {"NW": "transition", "NE": "transition", "SW": "lower", "SE": "lower"}
        terrain_tile(a, cell, corners, "water", 1.0)
    atlases.append(a)

    # 3-6: kits
    for sid, kit in ((3, "cottage16"), (4, "fence16"), (5, "ruin16"), (6, "forest16")):
        a = Atlas(sid, f"res://assets/tilesets/{kit}.png")
        png = TS / f"{kit}.png"
        for name, cell in json.loads((TS / f"{kit}.json").read_text())["tiles"].items():
            t = a.tile(cell)
            cov = coverage(png, cell)
            block = {
                "cottage16": not name.startswith("shadow") and not name.startswith("chimney"),
                "fence16": True,
                "ruin16": cov >= 0.3,
                "forest16": cov >= 0.6,
            }[kit]
            if block:
                t["polys"].append((WORLD, FULL))
        atlases.append(a)

    # 7: stamps
    a = Atlas(7, "res://assets/tilesets/stamps.png")
    for name, s in json.loads((TS / "stamps.json").read_text())["stamps"].items():
        (ox, oy), (cols, rows) = s["origin"], s["size"]
        for r in range(rows):
            for c in range(cols):
                t = a.tile((ox + c, oy + r))
                bottom = r == rows - 1
                shadow_col = name.startswith("gable") and c == cols - 1
                if name != "ford" and not shadow_col:
                    t["y_sort_origin"] = (rows - 1 - r) * T + H   # sort the whole stamp by its base
                if name.startswith("gable"):
                    block = c < cols - 1                      # the last column is the cast shadow
                elif name.startswith(("oak", "birch")):
                    block = bottom and c == cols // 2         # the trunk
                elif name.startswith(("bush", "standing_stone", "shrine")):
                    block = bottom
                elif name == "ford":
                    # the lane runs down local x 8-23 (the cut is offset 8px): the left
                    # column blocks only its outer half, the right column all of it
                    block = False
                    if r in (1, 2, 3) and c != 1:
                        layer = WORLD if r < 3 else WATER
                        t["polys"].append((layer, rect(-H, -H, H, T) if c == 0 else FULL))
                else:
                    block = False                             # flowers, rubble
                if block:
                    t["polys"].append((WORLD, FULL))
    atlases.append(a)

    lines = ['[gd_resource type="TileSet" format=3]', ""]
    for at in atlases:
        lines.append(f'[ext_resource type="Texture2D" path="{at.texture}" id="tex_{at.sid}"]')
    lines.append("")
    for at in atlases:
        lines += at.lines() + [""]
    lines += ["[resource]",
              "physics_layer_0/collision_layer = 1",
              "physics_layer_0/collision_mask = 0",
              "physics_layer_1/collision_layer = 128",
              "physics_layer_1/collision_mask = 0",
              "terrain_set_0/mode = 1"]
    for i, (name, colour) in enumerate(TERRAINS):
        lines += [f'terrain_set_0/terrain_{i}/name = "{name}"', f"terrain_set_0/terrain_{i}/color = Color({colour}, 1)"]
    for at in atlases:
        lines.append(f'sources/{at.sid} = SubResource("atlas_{at.sid}")')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"{OUT}: {sum(len(at.tiles) for at in atlases)} tiles in {len(atlases)} sources")


if __name__ == "__main__":
    main()
