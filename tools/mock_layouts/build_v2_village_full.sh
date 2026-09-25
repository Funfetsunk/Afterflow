#!/bin/sh
# Rebuild the full village mock (Phase 0 exit mock) from approved assets only.
# Composition follows the north star (art/mocks/review_north_star_r2_mix_6x.png):
# a row of oaks cut off by the top edge, deep-roofed cottages, 1-tile lanes,
# grass band above the river ledge. Run from the project root.
set -e
L=tools/mock_layouts/v2_village_full.json
rm -f $L
python tools/wang_layout.py art/raw/ts_meadow_grass-path_opt3.json art/final/ts_meadow_grass-path_opt3_ns.png \
  tools/mock_layouts/map_v2_village_full.txt $L \
  --extra '~' art/raw/ts_meadow_grass-water_opt2.json art/final/ts_meadow_grass-water_opt2_ns.png \
  --fill-variants art/final/ts_meadow_grass-fill_ns0.png art/final/ts_meadow_grass-fill_ns1.png \
    art/final/ts_meadow_grass-fill_ns2.png art/final/ts_meadow_grass-fill_ns3.png art/final/ts_meadow_grass-fill_ns4.png \
    art/final/ts_meadow_grass-fill_ns5.png art/final/ts_meadow_grass-fill_ns6.png art/final/ts_meadow_grass-fill_ns7.png \
  --ledge-pairs art/final/ts_meadow_ledge_ns --seed 7
# tree row along the top edge (crowns run off screen; trimmed below), drawn before the cottages
for t in "oak_a -1 1" "oak_b 4 1" "oak_b 8 1" "oak_a 11 1" "oak_b 14 1" "oak_a 18 1"; do
  python tools/paint_tiles.py $L stamp $t
done
python tools/paint_cottage16.py $L --at 1 1 --walls l window_big door r --roof 3 --chimney 2
python tools/paint_cottage16.py $L --at 11 1 --walls l window_big m window_small door window_small r --roof 3 --chimney 3
python tools/paint_tiles.py $L stamp shrine_monolith 9 4
python tools/paint_tiles.py $L fence 9 5 2
for s in "standing_stone 1 8" "bush_a 4 8" "bush_b 13 8" "flowers_a 6 8" "flowers_c 11 8" "flowers_b 15 8" "flowers_e 19 8" "flowers_d 0 5"; do
  python tools/paint_tiles.py $L stamp $s
done
python - <<'PY'
import json
p = "tools/mock_layouts/v2_village_full.json"
d = json.load(open(p))
# drop tiles that fall off the top/left edge (tree crowns, chimney tops)
d["items"] = [i for i in d["items"] if "cell" not in i or (i["cell"][0] >= 0 and i["cell"][1] >= 0)]
# nudge the standing stone half a tile down, clear of the lane
for i in d["items"]:
    if "standing_stone" in i["image"]:
        i["at"] = [i["cell"][0] * 16, i["cell"][1] * 16 + 8]
        del i["cell"]
d["items"] += [
    {"image": "art/final/chr_awa_s.png", "at": [98, 58], "nodrain": True},
    {"image": "art/final/npc_villager01_w.png", "at": [230, 80]},
    {"image": "art/final/enm_meadow01_w.png", "at": [276, 124]},
    {"image": "art/final/enm_meadow01_s.png", "at": [150, 124]},
]
json.dump(d, open(p, "w"), indent=1)
PY
python tools/compose_mock.py $L -o art/mocks/v2_village_full.png
python tools/compose_mock.py $L -o art/mocks/v2_village_full_drain.png --drain
