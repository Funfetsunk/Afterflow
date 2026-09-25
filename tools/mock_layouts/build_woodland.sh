#!/bin/sh
# The old woodland (40x22 cells): leaf-litter floor, a grass clearing where the
# lane from the meadow arrives (west edge, rows 10-12), dense canopy along the
# top and bottom, a thicket in the middle, and the hollow oak's doorway at the
# top (cells 25-29, base row 5). Run from the project root.
set -e
L=tools/mock_layouts/woodland.json
rm -f $L
python tools/wang_layout.py art/raw/ts_meadow_grass-path_opt3.json art/final/ts_meadow_grass-path_opt3_ns.png \
  tools/mock_layouts/map_woodland.txt $L \
  --extra '~' art/raw/ts_wood_leaves-grass.json art/final/ts_wood_leaves-grass_v2.png   --extra-variants art/final/ts_wood_leaves_fill_0.png art/final/ts_wood_leaves_fill_1.png art/final/ts_wood_leaves_fill_2.png     art/final/ts_wood_leaves_fill_3.png art/final/ts_wood_leaves_fill_4.png art/final/ts_wood_leaves_fill_5.png   --fill-variants art/final/ts_meadow_grass-fill_ns0.png art/final/ts_meadow_grass-fill_ns1.png     art/final/ts_meadow_grass-fill_ns2.png art/final/ts_meadow_grass-fill_ns3.png art/final/ts_meadow_grass-fill_ns4.png   --variant-chance 0.9 --seed 5
python tools/paint_forest.py $L 0 0 24 5
python tools/paint_forest.py $L 31 0 9 6
python tools/paint_forest.py $L 0 17 40 5
python tools/paint_forest.py $L 0 0 4 7
python tools/paint_forest.py $L 12 9 6 5
python tools/paint_forest.py $L 33 9 7 5
python tools/paint_forest.py $L 23 0 9 3
python tools/paint_tiles.py $L stamp hollow_oak 25 5
for s in "oak_a 7 8" "birch_a 22 9" "oak_b 27 14" "oak_a 8 15" "birch_a 31 8" "standing_stone 20 15" \
         "bush_a 10 12" "bush_b 23 12" "rubble_a 19 12" "flowers_c 3 11" "flowers_a 5 13"; do
  python tools/paint_tiles.py $L stamp $s
done
