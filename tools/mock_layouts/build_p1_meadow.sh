#!/bin/sh
# Phase 1 test meadow (40x22 cells, about 2x2 screens) from approved assets only,
# composed like the village mock: tree row and woodland at the top, cottages
# along the village lane, a lane down to the river crossing, the river ledge
# along the bottom. Converted to Godot TileMapLayers by tools/layout_to_tilemap.py.
# Run from the project root.
set -e
L=tools/mock_layouts/p1_meadow.json
rm -f $L
python tools/wang_layout.py art/raw/ts_meadow_grass-path_opt3.json art/final/ts_meadow_grass-path_opt3_ns.png \
  tools/mock_layouts/map_p1_meadow.txt $L \
  --extra '~' art/raw/ts_meadow_grass-water_opt2.json art/final/ts_meadow_grass-water_opt2_ns.png \
  --fill-variants art/final/ts_meadow_grass-fill_ns0.png art/final/ts_meadow_grass-fill_ns1.png \
    art/final/ts_meadow_grass-fill_ns2.png art/final/ts_meadow_grass-fill_ns3.png art/final/ts_meadow_grass-fill_ns4.png \
    art/final/ts_meadow_grass-fill_ns5.png art/final/ts_meadow_grass-fill_ns6.png art/final/ts_meadow_grass-fill_ns7.png \
  --ledge-pairs art/final/ts_meadow_ledge_ns --seed 11
python tools/paint_forest.py $L 0 0 10 7
for t in "oak_a 10 2" "oak_b 14 2" "birch_a 18 2" "oak_a 22 2" "oak_b 26 2" "oak_a 30 2" "oak_b 34 2" "oak_a 37 2"; do
  python tools/paint_tiles.py $L stamp $t
done
python tools/paint_tiles.py $L stamp gable_d1 12 9
python tools/paint_tiles.py $L stamp shrine_monolith 17 8
python tools/paint_tiles.py $L fence 17 9 2
python tools/paint_cottage16.py $L --at 22 5 --walls l window_big m window_small door window_small r --roof 3 --chimney 3
python tools/paint_cottage16.py $L --at 32 6 --walls l window_small door r --roof 2 --chimney 1
python tools/paint_tiles.py $L ruin 3 13 end_l high full mid low end_r
python tools/paint_tiles.py $L stamp ford 19 20
python tools/paint_forest.py $L 33 12 7 6
for s in "rubble_pile 9 14" "rubble_a 2 15" "rubble_c 8 16" "standing_stone 12 16" "bush_a 15 14" "bush_b 24 16" \
         "bush_a 29 13" "flowers_a 5 17" "flowers_b 10 12" "flowers_c 17 13" "flowers_d 22 13" "flowers_e 27 17" \
         "flowers_a 31 16" "flowers_c 1 9" "flowers_e 11 9" "flowers_b 30 9" "birch_a 26 15" "oak_b 1 17"; do
  python tools/paint_tiles.py $L stamp $s
done
