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
  8 dungeon16 (hollow-oak rooms: walls block, floors don't)
  9 terrain/wood_leaves_grass    Wang sheet: grass / woodland leaf litter

Terrain set 0 (match corners): 0 grass, 1 path, 2 water, 3 bank, 4 leaves. Painting grass
picks at random among every all-grass tile, weighted by `probability`, so the
fill variants scatter on their own; the north-star ledge pairs outweigh the
sheet's own straight ledge tiles.

Physics layer 0 is `world` (collision layer 1): walls, roofs, trees, fences,
the ledge face. Physics layer 1 is `water` (collision layer 8). Terrain tiles
block per quarter (a bank or water corner blocks its quarter). Houses, the
gable, the hollow oak and dungeon walls block whole tiles; everything else
blocks only at its footprint (tools/footprint.py: the solid base, not the crown
or top), so Awa can walk behind trees, bushes, stones, fences and ruins. The
baked woodland uses tools/kits/forest16_meta.json from tools/paint_forest.py.

Stamp cells carry a y_sort_origin at the stamp's base, so on a y-sorted
objects layer Awa walks behind a tree crown or the shrine and in front of
their bases (the gable's shadow column and the lane crossing are left flat).

Usage (from the project root, after tools/export_assets.py):
    python tools/build_tileset.py
Writes resources/tilesets/meadow.tres.
"""

import json
import re
from pathlib import Path

from PIL import Image

from footprint import footprint, split_by_cells

T = 16
H = T // 2
TS = Path("assets/tilesets")
OUT = Path("resources/tilesets/meadow.tres")
FOREST_META = Path("tools/kits/forest16_meta.json")

TERRAINS = [("grass", "0.33, 0.49, 0.39"), ("path", "0.59, 0.42, 0.42"),
            ("water", "0.3, 0.4, 0.71"), ("bank", "0.18, 0.13, 0.18"), ("leaves", "0.3, 0.24, 0.14")]
CORNER_BITS = {"NW": "top_left_corner", "NE": "top_right_corner",
               "SW": "bottom_left_corner", "SE": "bottom_right_corner"}
QUARTERS = {"NW": (-H, -H), "NE": (0, -H), "SW": (-H, 0), "SE": (0, 0)}
WORLD, WATER = 0, 1


def rect(x, y, w, h):
    return f"PackedVector2Array({x}, {y}, {x + w}, {y}, {x + w}, {y + h}, {x}, {y + h})"


FULL = rect(-H, -H, T, T)


def local_rect(r):
    """A rect in tile pixels (x0, y0, x1, y1; 0..16) as a centred collision polygon."""
    x0, y0, x1, y1 = r
    return rect(x0 - H, y0 - H, x1 - x0, y1 - y0)


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
        lower = "water"
        if name.startswith("grass_fill"):
            corners = dict.fromkeys(CORNER_BITS, "upper")
        elif name.startswith("leaves_fill"):
            corners, lower = dict.fromkeys(CORNER_BITS, "lower"), "leaves"
        elif name.startswith("ledge_top"):
            corners = {"NW": "upper", "NE": "upper", "SW": "transition", "SE": "transition"}
        else:
            corners = {"NW": "transition", "NE": "transition", "SW": "lower", "SE": "lower"}
        terrain_tile(a, cell, corners, lower, 1.0)
    atlases.append(a)

    # 3-6: kits
    for sid, kit in ((3, "cottage16"), (4, "fence16"), (5, "ruin16"), (6, "forest16"), (8, "dungeon16")):
        a = Atlas(sid, f"res://assets/tilesets/{kit}.png")
        png = Image.open(TS / f"{kit}.png").convert("RGBA")
        forest_meta = json.loads(FOREST_META.read_text()) if kit == "forest16" and FOREST_META.exists() else {}
        for name, cell in json.loads((TS / f"{kit}.json").read_text())["tiles"].items():
            t = a.tile(cell)
            img = png.crop((cell[0] * T, cell[1] * T, (cell[0] + 1) * T, (cell[1] + 1) * T))
            if kit in ("cottage16", "dungeon16"):              # houses and dungeon walls are solid
                if kit == "dungeon16" and name.startswith("wall") or                         kit == "cottage16" and not name.startswith(("shadow", "chimney")):
                    t["polys"].append((WORLD, FULL))
            elif kit == "fence16":                             # only the foot of the posts and rails
                fp = footprint(img, depth=6)
                if fp:
                    t["polys"].append((WORLD, local_rect(fp)))
            elif kit == "ruin16":                              # the wall's base strip; tops sort with it
                if name.endswith("_bot"):
                    fp = footprint(img, depth=10)
                    if fp:
                        t["polys"].append((WORLD, local_rect(fp)))
                    t["y_sort_origin"] = H
                else:
                    t["y_sort_origin"] = T + H
            elif kit == "forest16":                            # trunk bases and enclosed deep shade
                m = forest_meta.get(name, {})
                for r in m.get("rects", []):
                    t["polys"].append((WORLD, local_rect(r)))
                if m.get("y_sort"):
                    t["y_sort_origin"] = m["y_sort"]
        atlases.append(a)

    # 7: stamps
    a = Atlas(7, "res://assets/tilesets/stamps.png")
    stamps_png = Image.open(TS / "stamps.png").convert("RGBA")
    for name, s in json.loads((TS / "stamps.json").read_text())["stamps"].items():
        (ox, oy), (cols, rows) = s["origin"], s["size"]
        img = stamps_png.crop((ox * T, oy * T, (ox + cols) * T, (oy + rows) * T))
        base = {}                                       # (col, row) -> local rect of the footprint
        if name.startswith(("oak", "birch", "bush", "standing_stone", "shrine")):
            fp = footprint(img)
            if fp:
                base = split_by_cells(fp, T)
        for r in range(rows):
            for c in range(cols):
                t = a.tile((ox + c, oy + r))
                bottom = r == rows - 1
                shadow_col = name.startswith("gable") and c == cols - 1
                if name != "ford" and not shadow_col:
                    t["y_sort_origin"] = (rows - 1 - r) * T + H   # sort the whole stamp by its base
                if (c, r) in base:
                    t["polys"].append((WORLD, local_rect(base[(c, r)])))
                elif name.startswith("gable") and c < cols - 1:   # the last column is the cast shadow
                    t["polys"].append((WORLD, FULL))
                elif name == "hollow_oak" and not (bottom and 1 <= c <= 3):   # the doorway is open
                    t["polys"].append((WORLD, FULL))
                elif name == "ford" and r in (1, 2, 3) and c != 1:
                    # the lane runs down local x 8-23 (the cut is offset 8px): the left
                    # column blocks only its outer half, the right column all of it
                    layer = WORLD if r < 3 else WATER
                    t["polys"].append((layer, rect(-H, -H, H, T) if c == 0 else FULL))
    atlases.append(a)

    # 9: woodland floor Wang sheet (grass / leaf litter)
    a = Atlas(9, "res://assets/tilesets/terrain/wood_leaves_grass.png")
    for tile in json.loads((TS / "terrain" / "wood_leaves_grass.json").read_text())["tiles"]:
        corners = tile["corners"]
        key = "".join(corners[c][0] for c in ("NW", "NE", "SW", "SE"))
        terrain_tile(a, tile["cell"], corners, "leaves", 0.25 if key == "uuuu" else None)
    atlases.append(a)
    atlases.sort(key=lambda at: at.sid)

    # keep the resource's uid across rebuilds, so scenes' references stay valid
    old = re.search(r'uid="([^"]+)"', OUT.read_text().splitlines()[0]) if OUT.exists() else None
    uid = f' uid="{old.group(1)}"' if old else ""
    lines = [f'[gd_resource type="TileSet" format=3{uid}]', ""]
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
