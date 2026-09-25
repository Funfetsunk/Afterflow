"""Export the approved Phase 0 art set into assets/ for Godot to import.

art/ is Godot-ignored working space; assets/ is what the game uses (CLAUDE.md
§4). This copies the approved set (Art Bible §11) and packs each tile kit into
one atlas PNG, which is what a Godot TileSet atlas source wants, plus a JSON
index next to it naming every tile's atlas cell:

  assets/characters/awa/awa_{s,e,n,w}.png            40x40 frames
  assets/characters/awa/awa_{idle,walk}_{d}_{i}.png  animation frames (hair-ramped)
  assets/characters/miller/miller_{s,e,n,w}.png
  assets/enemies/mossling/mossling_{s,e,n,w}.png     24x24 frames
  assets/tilesets/terrain/meadow_grass_path.png/.json  PixelLab Wang sheets with each
  assets/tilesets/terrain/meadow_grass_water.png/.json tile's corners (for terrain sets)
  assets/tilesets/terrain/meadow_extras.png/.json    grass fill variants, river ledge pairs
  assets/ui/*.png                                    HUD, pickups, panels, effects (tools/kits/make_ui16.py)
  assets/dungeon/*.png                               doors (tools/kits/make_woodland16.py)
  assets/enemies/warden/warden_<pose>.png            the boss (tools/kits/make_woodland16.py)
  assets/tilesets/<kit>.png/.json                    cottage16, fence16, ruin16, forest16:
                                                     {"tiles": {name: [col, row]}}
  assets/tilesets/stamps.png/.json                   every stamp as a contiguous block:
                                                     {"stamps": {name: {"origin": [col, row], "size": [cols, rows]}}}

Re-run after approving new art; it rebuilds assets/ from art/final/ and the kit
indexes in tools/kits/. Atlas positions are stable across runs (existing tiles
keep their cells, new ones are appended), so maps painted with the TileSet keep
working; tiles removed from a kit leave a gap. Only files listed
here are exported, so work-in-progress art never reaches the game.

Usage (from the project root):
    python tools/export_assets.py
"""

import json
import math
import shutil
from pathlib import Path

from PIL import Image

T = 16
OUT = Path("assets")
KITS = Path("tools/kits")
DIRS = "senw"

SPRITES = {                                       # out folder/name: art/final prefix
    "characters/awa/awa": "art/final/chr_awa",
    "characters/miller/miller": "art/final/npc_villager01",
    "enemies/mossling/mossling": "art/final/enm_meadow01",
    "enemies/barkling/barkling": "art/final/enm/barkling",
}
BOSS = ("art/final/enm/warden", ("idle", "raise", "dazed"))   # -> assets/enemies/warden/warden_<pose>.png
ANIMS = {                                         # out prefix: (art/final prefix, {animation: frames})
    "characters/awa/awa": ("art/final/awa_anim/chr_awa", {"idle": 4, "walk": 6, "swing": 4}),
}
WANG = {                                          # out name: (sheet, PixelLab metadata)
    "meadow_grass_path": ("art/final/ts_meadow_grass-path_opt3_ns.png", "art/raw/ts_meadow_grass-path_opt3.json"),
    "meadow_grass_water": ("art/final/ts_meadow_grass-water_opt2_ns.png", "art/raw/ts_meadow_grass-water_opt2.json"),
    "wood_leaves_grass": ("art/final/ts_wood_leaves-grass_v2.png", "art/raw/ts_wood_leaves-grass.json"),
}
EXTRAS = (
    [(f"grass_fill_{i}", f"art/final/ts_meadow_grass-fill_ns{i}.png") for i in range(8)]
    + [(f"ledge_top_{i}", f"art/final/ts_meadow_ledge_ns_top{i}.png") for i in range(7)]
    + [(f"ledge_bot_{i}", f"art/final/ts_meadow_ledge_ns_bot{i}.png") for i in range(7)]
    + [(f"leaves_fill_{i}", f"art/final/ts_wood_leaves_fill_{i}.png") for i in range(6)]
)
KIT_NAMES = ("cottage16", "fence16", "ruin16", "forest16", "dungeon16")
ATLAS_COLS = 8
STAMP_COLS = 16


def save_json(path, data):
    path.write_text(json.dumps(data, indent=1) + "\n")


def grid_atlas(named_paths, path, cols=ATLAS_COLS):
    """Pack 16px tiles into a grid; return {name: [col, row]}.

    Positions are stable: tiles already in the atlas's JSON index keep their
    cell, and new tiles take the next free cells, so painted maps never shift.
    """
    index_path = path.with_suffix(".json")
    old = json.loads(index_path.read_text()).get("tiles", {}) if index_path.exists() else {}
    index = {name: cell for name, cell in old.items() if name in dict(named_paths)}
    used = {tuple(c) for c in index.values()}
    free = (divmod(i, cols)[::-1] for i in range(10_000))
    for name, _ in named_paths:
        if name not in index:
            cell = next(c for c in free if c not in used)
            index[name] = list(cell)
            used.add(cell)
    rows = max(r for _, r in index.values()) + 1 if index else 1
    atlas = Image.new("RGBA", (cols * T, rows * T), (0, 0, 0, 0))
    for name, src in named_paths:
        c, r = index[name]
        atlas.alpha_composite(Image.open(src).convert("RGBA"), (c * T, r * T))
    atlas.save(path)
    return index


def export_sprites():
    for out, prefix in SPRITES.items():
        dest = OUT / out
        dest.parent.mkdir(parents=True, exist_ok=True)
        for d in DIRS:
            shutil.copyfile(f"{prefix}_{d}.png", f"{dest}_{d}.png")


def export_boss():
    prefix, poses = BOSS
    dest = OUT / "enemies" / "warden"
    dest.mkdir(parents=True, exist_ok=True)
    for pose in poses:
        shutil.copyfile(f"{prefix}_{pose}.png", dest / f"warden_{pose}.png")


def export_anims():
    for out, (prefix, anims) in ANIMS.items():
        for anim, frames in anims.items():
            for d in DIRS:
                for i in range(frames):
                    shutil.copyfile(f"{prefix}_{anim}_{d}_{i}.png", OUT / f"{out}_{anim}_{d}_{i}.png")


def export_ui():
    for folder in ("ui", "dungeon"):
        dest = OUT / folder
        dest.mkdir(parents=True, exist_ok=True)
        for src in sorted(Path(f"art/final/{folder}").glob("*.png")):
            shutil.copyfile(src, dest / src.name)


def export_terrain():
    dest = OUT / "tilesets" / "terrain"
    dest.mkdir(parents=True, exist_ok=True)
    for name, (sheet, meta) in WANG.items():
        shutil.copyfile(sheet, dest / f"{name}.png")
        tiles = json.loads(Path(meta).read_text(encoding="utf-8"))["tileset_data"]["tiles"]
        save_json(dest / f"{name}.json", {"tile": T, "tiles": [
            {"cell": [t["bounding_box"]["x"] // T, t["bounding_box"]["y"] // T], "corners": t["corners"]}
            for t in tiles]})
    save_json(dest / "meadow_extras.json", {"tile": T, "tiles": grid_atlas(EXTRAS, dest / "meadow_extras.png")})


def export_kits():
    dest = OUT / "tilesets"
    for kit in KIT_NAMES:
        data = json.loads((KITS / f"{kit}.json").read_text())
        tiles = data.get("tiles", data)            # forest16.json is a flat {hash: path} index
        named = sorted(tiles.items())
        save_json(dest / f"{kit}.json", {"tile": T, "tiles": grid_atlas(named, dest / f"{kit}.png")})


def export_stamps():
    """Shelf-pack every stamp as a contiguous block of cells, keeping its shape.

    Stable like grid_atlas: stamps already placed keep their origin; new ones
    are packed below the existing blocks.
    """
    stamps = json.loads((KITS / "stamps.json").read_text())
    index_path = OUT / "tilesets" / "stamps.json"
    old = json.loads(index_path.read_text()).get("stamps", {}) if index_path.exists() else {}
    placed = {n: tuple(v["origin"]) for n, v in old.items()
              if n in stamps and v["size"] == [stamps[n]["cols"], stamps[n]["rows"]]}
    top = max((placed[n][1] + stamps[n]["rows"] for n in placed), default=0)
    x, y, shelf = 0, top, 0
    for name in sorted((n for n in stamps if n not in placed), key=lambda n: (-stamps[n]["rows"], n)):
        cols, rows = stamps[name]["cols"], stamps[name]["rows"]
        if x + cols > STAMP_COLS:
            x, y, shelf = 0, y + shelf, 0
        placed[name] = (x, y)
        x, shelf = x + cols, max(shelf, rows)
    height = max(placed[n][1] + stamps[n]["rows"] for n in placed)
    atlas = Image.new("RGBA", (STAMP_COLS * T, height * T), (0, 0, 0, 0))
    index = {}
    for name, (sx, sy) in placed.items():
        s = stamps[name]
        for r, row in enumerate(s["tiles"]):
            for c, src in enumerate(row):
                atlas.alpha_composite(Image.open(src).convert("RGBA"), ((sx + c) * T, (sy + r) * T))
        index[name] = {"origin": [sx, sy], "size": [s["cols"], s["rows"]]}
    atlas.save(OUT / "tilesets" / "stamps.png")
    save_json(index_path, {"tile": T, "stamps": index})


def main():
    (OUT / "tilesets").mkdir(parents=True, exist_ok=True)
    export_sprites()
    export_anims()
    export_boss()
    export_ui()
    export_terrain()
    export_kits()
    export_stamps()
    files = sorted(p for p in OUT.rglob("*") if p.is_file() and p.suffix in (".png", ".json"))
    for p in files:
        print(p.as_posix())
    print(f"{len(files)} files in {OUT}/")


if __name__ == "__main__":
    main()
