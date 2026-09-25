# Afterflow — Asset Manifest

> The single source of truth for every generated asset. If it's in the game, it's in this file.
> **Purpose:** any future session can regenerate or extend an asset with exactly the same settings.

---

## 1. How to use this file

- **Before generating:** add the asset here with status `planned`.
- **After generating:** fill in the PixelLab IDs, the exact prompt used, the variant count, the chosen variant and the credits spent.
- **Never overwrite an `approved` asset.** Create a new version (`_v2`) and a new row.

### 1.1 Status values

`planned` → `generating` → `review` → `approved` | `rejected`

### 1.2 Naming convention

```
<type>_<name>[_<variant>][_<anim>][_<dir>].png
```

| Prefix | Type | Example |
|---|---|---|
| `chr_` | Player character | `chr_awa_b_walk_s.png` |
| `npc_` | NPC | `npc_villager01_idle_e.png` |
| `enm_` | Enemy | `enm_meadow01_idle_n.png` |
| `boss_` | Boss | `boss_woodland_idle_s.png` |
| `ts_` | Tileset | `ts_meadow_grass-path.png` |
| `obj_` | Map object | `obj_cottage01.png` |
| `ui_` | UI element | `ui_health_leaf.png` |
| `mock_` | Mock screenshot | `mock_meadow_village_v1.png` |

Directions: `s`, `w`, `e`, `n`. Lowercase with hyphens inside names.

### 1.3 File locations

- `art/raw/`: PixelLab downloads, untouched. Never edit these.
- `art/final/`: palette-remapped versions, the only ones used for mocks and the game.
- `art/mocks/`: composed mock screenshots.

---

## 2. Credit log

MCP generations draw from the subscription allowance (2,000 per cycle on Tier 1, resetting on the 21st). Paid credits are a separate balance, currently $0. Check with `get_balance`.

| Cycle | Plan | Generations used (Afterflow) | Notes |
|---|---|---|---|
| 2026-09-21 → 2026-10-21 | Tier 1 (Pixel Apprentice) | 178 | 859 of 2,000 were already used this cycle before Afterflow started; 1,140 left on 2026-09-25; 1,000 left after north-star round 1; 990 after 16px grass-path; 981 after the 16px river; 977 after Awa v2; 971 after trees; 962 after the forest tileset attempt |

---

## 3. Shared parameters

Unless a row says otherwise, every asset uses the locked Art Bible §3 parameters (`high top-down`, `single color black outline`, `basic shading`, `low detail`, 4 directions, 16px tiles) and the Art Bible §3.1 style suffix, is remapped to the Afterflow v1 palette (`tools/palettes/afterflow-v1.hex`), and matches the north star. The "Credits" columns record **generations** spent.

---

## 4. Phase 0 v2: 16-bit rebuild

Direction reset on 2026-09-25 (Art Bible §0): 320×180, 16px tiles, 16-bit SNES-era top-down style. The superseded v0.x record is in `docs/archive/ASSET_MANIFEST_v0.md`.

| ID | Asset | Size | PixelLab ID(s) | Variants | Chosen | Credits | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| `ns_meadow_village` | North-star screen: meadow village | 320×180 | r1: pixflux opt1–4 `3dbacb68-e21e-40e3-8f42-90801e7a1cdc`, `7125c297-cd92-4af2-802a-24697a796597`, `14d236de-e843-4bd2-8456-c7729eed7476`, `30424275-a201-4494-bd23-3344c1a90fa4`; pixen opt5–8 `e503ab74-76bc-457a-ab13-5256c282ed8e`, `eae764ff-9567-4ca5-8f75-6e5ef23d3598`, `d3f0dffd-1326-423f-8408-1102b6623364`, `304468a2-33b6-4a29-a262-e7e76350ca0b` | 8 | **r2 mix** | 8 | approved | **North star approved and locked by Tom, 2026-09-25** ('I love the style'). Tom noticed slight discolouration in Awa's hair: her restored pixels aren't a clean ramp, so don't use this image as Awa's reference. Art Bible §3.2 step 1. Seeds 1–4 per model; opt1–2/5–6 `medium detail`, opt3–4/7–8 `low detail`; `high top-down`, `single color black outline`, `basic shading` (pixflux). Only r1 opt4 and opt6 are kept in `art/raw|final/north_star/` (the r2 inputs); the others are in git history. Sheet: `art/mocks/review_north_star_r1.png`. opt5/opt7 came out letterboxed. **r2 (Tom: 'opt4 layout with opt6 colours', 0 generations):** `art/final/north_star/ns_meadow_village_r2_mix.png` = opt4 recoloured by material into opt6's colours: `recolour.py art/final/north_star/ns_meadow_village_r1_opt4.png art/final/north_star/ns_meadow_village_r2_mix.png --map a2a947=547e64 676633=374e4a 374e4a=313638 d5e04b=676633 fca790=966c6c c7dcd0=ab947a 7f708a=966c6c 323353=3e3546 165a4c=374e4a 547e64=676633 484a77=4d65b4 4d9be6=8fd3ff 9babb2=ab947a 6e2727=4c3e24 753c54=45293f 7a3045=45293f e6904e=966c6c cd683d=9e4539 c32454=fbb954 a24b6f=ffffff`, then Awa's original pixels restored in the box (116,80)–(140,108) so she keeps her ginger hair. Review: `art/mocks/review_north_star_r2_mix_6x.png` |
| `chr_awa` | Awa, 16-bit | size 28 | opt1 `13d1c8e8-f7fe-4d99-b30e-34b798be4d5e`<br>opt2 `357556ed-daa6-4916-b67c-313fe8990fb6`<br>opt3 `77e8b342-cf95-4d15-a76c-35a0ed703f23`<br>opt4 `bc522d1a-9118-4c3b-9a51-38ca5ec06843` | 4 | **opt2** | 4 | approved | **Approved by Tom, 2026-09-25** (opt2 with hair_ramp and eye fix). Final files `art/final/chr_awa_{s,e,n,w}.png`. opt1: pale torso read as a bare midriff; opt3: off-brief (mint shirt, bow); opt4: bright hair but a pale blotch on the back of the head. opt2: best design, but flat one-tone rust hair and grey eye whites that read as glasses. Fix: `hair_ramp.py art/final/chr_awa_opt2_<d>.png art/final/chr_awa_<d>.png --hair 9e4539 --ramp e6904e cd683d 9e4539 --map 9babb2=fdcbb0` → clean 3-tone ginger ramp (lit crown, dark face-framing strands) and skin-tone eye whites. Figure 24–27px. Reviews: `art/mocks/review_v2_awa_options.png`, `review_v2_awa_opt2_hair_fix.png`, `v2_awa_final_scene_6x.png`. `create_character` standard, `high top-down`, `single color black outline`, `basic shading`, `low detail`, 4 directions. opt1–2 `default` preset, opt3–4 `cartoon`. Check the hair ramp (Art Bible §4.3) |
| `ts_meadow_grass-path` | Meadow grass ↔ dirt path | 16px | opt1 `8ac020c5-a28a-4d5b-b459-9a2fcb463352`<br>opt2 `ef8b1e7d-c1b8-40e4-a2b4-7345c28494da`<br>opt3 `475e723f-b5ea-4a60-8379-170c91b7133a` | 3 | **opt3** | 10 | approved | **Approved by Tom, 2026-09-25.** opt1: orange patterned path; opt2: yellow grass; opt3 closest to the north star. opt3 recipe: `palette_remap.py ... --palette tools/palettes/afterflow-v1.hex`, then `recolour.py art/final/ts_meadow_grass-path_opt3.png art/final/ts_meadow_grass-path_opt3_ns.png --map ab947a=966c6c 966c6c=ab947a 323353=313638 625565=374e4a 753c54=45293f` (path base/speck swap, edge colours to the north star's). Grass tufts: 8 tufted 16×16 grass tiles cut from the north star → `art/final/ts_meadow_grass-fill_ns0..7.png` (grass-only windows with a clean 547e64 border), scattered at ~45%. Review: `art/mocks/review_v2_grass-path_vs_north_star.png`. `create_topdown_tileset` standard, 16px, `high top-down`, `single color outline`, `basic shading`, `low detail`. opt1–2 flush (transition 0), opt3 grass fringe (0.25). Grass base tiles: opt1 `dcac0256-d8b6-40c9-a614-3ec956cb11cc`, opt2 `f1678a83-d09b-4ad3-a520-f7bf4bc43e19`, opt3 `85b48458-e668-48e9-ab68-c57aa28fe613` |
| `ts_meadow_grass-water` | Meadow grass ↔ river (ledge) | 16px | opt1 `a2dc6317-4a20-44e9-937e-148f57c864c9`<br>opt2 `10fd48dd-3904-4591-87a5-6fa6754cc02a`<br>opt3 `62b5d23f-d47d-4d15-b11f-3ea69f845298` | 3 | **opt2** | 9 | approved | **Approved by Tom, 2026-09-25** (opt2 recoloured plus the cut ledge pairs on straight runs). Rivers run straight east–west for now; bends need corner tiles adjusted to the north star's ledge height. opt1/opt3: thin lip, bright flat blue water. opt2: one-tile cliff ledge (25-tile layout; ledge row marked `=` in wang_layout maps), north-star water blue and foam line, but the ledge face came out as orange/pale vertical planks. opt2 recipe: remap to afterflow-v1, then `recolour.py art/final/ts_meadow_grass-water_opt2.png art/final/ts_meadow_grass-water_opt2_ns.png --map 753c54=45293f 323353=2e222f ab947a=3e3546 cd683d=9e4539 fbb954=9e4539 7f708a=3e3546 625565=45293f d5e04b=374e4a 966c6c=45293f`. Reviews: `art/mocks/review_v2_grass-water_options.png`, `review_v2_grass-water_vs_north_star.png`. **Straight ledge runs use 7 matched top/bottom pairs cut from the north star's riverbank** (y 144–176, windows clear of the path; top row grass tones, bottom row water tones) → `art/final/ts_meadow_ledge_ns_top0..6.png` / `_bot0..6.png`, placed with `wang_layout.py --ledge-pairs art/final/ts_meadow_ledge_ns`. The north star's ledge is ~1.2 tiles tall against the tileset's ~1.75, so **bends and ends still use the tileset tiles and won't match in height yet**. Review: `art/mocks/review_v2_river_nsledge_vs_north_star.png`. `upper_base_tile_id` = approved grass `85b48458-e668-48e9-ab68-c57aa28fe613`. opt1: earth ledge, transition 0.5; opt2: one-tile ledge, transition 1.0 (25 tiles); opt3: low stone/earth wall, 0.5 |
| `obj_cottage_kit` | Cottage slice kit cut from the north star's long cottage | 86px tall slices | — (0 generations) | — | kit | 0 | superseded | Approved 2026-09-25, then superseded the same day by `ts_cottage16` (slice widths weren't on the 16px grid). 9 full-height vertical slices (ridge cap, slate roof, eave, stone wall run through each): `end_l`, `wall_a`, `window_big`, `wall_b`, `post`, `window_small_b`, `door`, `window_small`, `end_r`, from x 187–287, rows 0–85 of `ns_meadow_village_r2_mix.png`. Cleaning: above the ridge nothing is kept; the chimney (x 244–259, rows 4–30) is lifted out as a separate 16×27 piece (`obj_cottage_chimney_piece.png`) and the ridge behind it is filled from the ridge 16px to its left; below the eave nothing outside the wall outlines (x 190–284) is kept (Tom spotted a fence stub on the left wall); grass pixels on the eave rows and at the wall base (rows ≥80) are removed. The house body rebuilds the north star with 0 differing pixels. Kit: `tools/kits/cottage_ns.json`; `tools/build_cottage.py kit out.png <slices...> [--chimney X]`. Built: `obj_cottage_tiny` (end_l door window_small end_r --chimney 26), `obj_cottage_small` (end_l wall_a door window_small end_r), `obj_cottage_chimney` (end_l window_small window_small_b door window_big end_r --chimney 24), `obj_cottage_long` (end_l window_big wall_b post window_small_b door wall_a window_big end_r --chimney 20 --chimney 70). Review: `art/mocks/review_v2_cottages_scene_6x.png` |
| `ts_cottage16` | **16px cottage tile kit** (Art Bible §2: everything is tiles), roof and wall as separate layers | 16×16 tiles | — (0 generations) | — | kit | 0 | approved | **Approved by Tom, 2026-09-25** ('they are good'). Built from the north star's long cottage by `tools/kits/make_cottage16.py` → 29 tiles in `art/final/tiles/cottage16/`, index `tools/kits/cottage16.json`. Roof: 3×3 nine-slice `roof_{top,mid,bot}_{l,m,r}` (north-star rows 24–39 / 40–55 / 49–64; columns 0–15 / 16–31 / 85–100 from x 187); repeat `_mid` rows and `_m` columns for any size. Wall: 2 tiles tall, `wall_{l,m,r}` and feature columns `window_big`, `window_small`, `door` (each `_top` + `_bot`); the north star's 21-row wall gets 11 rows added below the windows (plain-stone block rows 70–80; posts repeat rows 79/80); the **door is stretched proportionally**: rows 65–72, 68–72, 73–80, 81–85, 81–86 (Tom saw a dark band when two plank rows were repeated); base keeps the north star's own rows 82–86 **with grass tufts overlapping the stone** (a clean hard base made the houses look pasted on, Tom). Door narrowed to 16px (plank column 70 dropped). **Grounding:** cast-shadow column to the right `shadow_{roof_mid,roof_bot,roof_bot_full,wall_top,wall_bot}` (north star x 288–303; the wall's last 3 columns are shadow too); the painter adds it. **No doorstep:** what looked like a step under the north star's door is the path itself (Tom saw 'path' at the door's foot), so paths are painted with the terrain tiles. Chimney: 1×3 stamp `chimney_{0,1,2}` over the roof's top row. Paint with `tools/paint_cottage16.py layout.json --at C R --walls l ... r --roof N [--chimney C]`. Review: `art/mocks/review_v2_cottage16_6x.png`. **Supersedes the slice kit below for building** |
| `obj_cottage_roofs` | Roof colour variants for the cottage kit | — | — (0 generations) | — | 5 | 0 | approved | **Approved by Tom, 2026-09-25.** `build_cottage.py ... --roof` recolours only the slate rows (kit `roof_rows` 31–61). plum (default), navy `--roof 625565=484a77 3e3546=323353`, clay `--roof 625565=9e4539 3e3546=6e2727`, moss `--roof 625565=676633 3e3546=4c3e24`, brown `--roof 625565=966c6c 3e3546=45293f`. Pale thatch rejected (blends into the walls). Built: `obj_cottage_long_clay`, `obj_cottage_small_navy` |
| `obj_props_ns` | Props cut from the north star | various | — (0 generations) | — | all | 0 | approved | **Approved by Tom, 2026-09-25.** `tools/cut_prop.py` (border flood fill through background colours; `--largest` drops scraps). `obj_standing_stone_ns` (6 113 30 146 --largest), `obj_bush_ns1` (56 120 82 148), `obj_bush_ns2` (82 120 108 148), `obj_flowers_ns1..5` (142 132 158 150 / 182 132 200 150 / 266 113 286 131 / 286 130 306 150 / 302 113 320 133), `obj_fence_ns` (143 70 189 89 --bg 547e64 374e4a 313638 966c6c ab947a 676633 4c3e24 --largest), `obj_cottage_gable_ns` (18 14 106 111 --bg 547e64 374e4a 313638 676633 --largest, then tree roots above the peak removed: rows 0–7 cleared, ridge capped with `2e222f`, stray fragments dropped). Trees are clipped by the frame, so they can't be cut. Scene: `art/mocks/review_v2_village_scene_6x.png` |
| `ts_stamps` | Fixed tile stamps (Art Bible §2): trees, bushes, standing stone, flowers | 16px tiles | — (0 generations) | — | all | 0 | approved | **Approved by Tom, 2026-09-25.** `tools/make_stamp.py <sprite> <name>` pads to whole tiles (bottom-centre) and splits into `art/final/tiles/stamps/<name>_r<row>c<col>.png`, registry `tools/kits/stamps.json`; paint with `tools/paint_tiles.py layout stamp NAME COL ROW` (bottom-left cell). Stamps: `oak_a` 3×3 (tree oak opt3), `oak_b` 3×3 (oak opt1), `birch_a` 2×3 (birch opt1), `bush_a`/`bush_b` 2×2, `standing_stone` 2×2, `flowers_a..e` 1×1. **Grounding:** bushes and stone re-cut with their north-star cast shadow kept (`cut_prop.py ... --bg 547e64 --largest`); trees keep their baked ground patch recoloured to the north star's shadow `374e4a` (ground rows 4/8/6; `676633 d5e04b a2a947 547e64` → `374e4a`), other yellow highlights `d5e04b` → `676633`. Scene: `art/mocks/review_v2_tiles_village_6x.png` |
| `ts_fence16` | Fence kit from the north star's picket fence | 16px tiles | — (0 generations) | — | kit | 0 | approved | **Approved by Tom, 2026-09-25.** `fence_m` (post x 142–146 + rail 147–153, 159–162; rows 72–87) and `fence_end` (post x 187–191), rail shadow kept, grass transparent; kit `tools/kits/fence16.json`; paint `tools/paint_tiles.py layout fence COL ROW LEN` |
| `npc_villager01` | The miller, 16-bit | ~24–28px | — | — | — | — | planned | |
| `obj_trees` | Meadow trees (oak, birch), 16-bit | 48×48 / 32×48 canvas | oak opt1–3 `672d4c05-9eb4-4173-b152-eacc80bb9b3d`, `9fb3883b-1f64-407e-82ae-5bd84158f71b`, `f12d1d84-2fd4-40ba-aaf1-78cd8eb5e03f`<br>birch opt1–3 `b05c4dbc-059a-4c98-b7e2-2a60d066b09d`, `3e0fd666-7c9f-4576-87a9-e3585d797fd8`, `7f9a660d-840c-43af-9e83-5967e0944a1f` | 6 | oak opt3, oak opt1, birch opt1 (Claude's picks) | 6 | approved (as stamps) | `create_image_pixflux`, seeds 1–3, locked §3 parameters, `no_background`, **`color_image_url` = the north star** (forced palette, via its public GitHub raw URL). Then remap to afterflow-v1 and `recolour.py <in> <out> --strip-ground 547e64 374e4a 313638 676633 d5e04b a2a947 --ground-rows N --map d5e04b=676633` (baked ground shadow removed, loud yellow highlights to olive; N = 4 oak opt3, 8 oak opt1, 6 birch opt1), cropped → `obj_tree_oak`, `obj_tree_oak_b`, `obj_tree_birch`. Rejected: oak opt2 (khaki, yellow ground ring), birch opt2 (blue diamond canopy), birch opt3 (khaki). Scene: `art/mocks/review_v2_village_trees_6x.png` |
| `obj_shrine01` | Shrine, 16-bit | 16×32 | — | — | — | — | planned | |
| `ts_forest` | Forest canopy ↔ meadow grass autotile | 16px | opt1 `3d6eb3b3-92c1-469a-980a-d06faab52f5c`<br>opt2 `32eb8c0b-90e6-4138-a071-d9597b86a3b1`<br>opt3 `d4158e9b-0214-462d-bb63-44813e66a83c` | 3 | — | 9 | rejected | **All three rejected** (`art/mocks/review_v2_forest_tilesets_rejected.png`): opt1 a flat 4-colour dark blob, opt2 striped crop rows with an orange trim, opt3 a regular polka-dot grid. PixelLab's terrain model doesn't draw tree crowns. **Replaced by a woodland built from the approved tree stamps** (overlapping staggered rows of `oak_a`/`oak_b`/`birch_a`, back to front): `art/mocks/review_v2_forest_stamps_6x.png`, in review. Tree masses of any size. Grass is the **lower** terrain here (`lower_base_tile_id` = approved grass `85b48458-e668-48e9-ab68-c57aa28fe613`), canopy the upper. opt1: canopy edge with shadow and trunks, 0.25; opt2: trunk row as a one-tile cliff, 1.0 (25 tiles); opt3: bumpy shadowed edge, 0.5 |
| `ts_forest16` | **Paintable woodland** (one tile layer) baked from the approved tree stamps | 16px tiles | — (0 generations) | — | tool + library | 0 | approved | **Approved by Tom, 2026-09-25.** Tom chose the stamp woodland look ('yes for now'). `tools/paint_forest.py layout COL ROW W H` plants `oak_a`/`oak_b`/`birch_a` on a staggered lattice (every 2 columns, alternate rows shifted; species from a fixed position pattern, so maps are reproducible), draws back to front, fills gaps **fully enclosed by crowns** with deep shade `313638` (a rectangular fill looked blocky), slices into cells and reuses identical tiles from the shared library `art/final/tiles/forest16/` (index `tools/kits/forest16.json`; 55 tiles after two test forests). Review: `art/mocks/review_v2_forest_tiles_6x.png` |
| `ts_ruin16` | Crumbled ruin-wall kit, 16-bit | 16px tiles | — | — | — | — | planned | Art Bible §5.3: crumbled, not angular |
| `enm_meadow01` | Meadow creature | ~16–24px | — | — | — | — | planned | Sets the enemy signature |

---

## 5. Prompt log

Record the **exact** final prompt for every approved asset.

### `ns_meadow_village` (round 1)
```
top-down view of a small English village in a green meadow, two small stone cottages with dark slate roofs and chimneys, a winding dirt path, a short wooden fence, round bushes and little flowers, a river along the bottom edge, an old standing stone shrine and a crumbled mossy stone wall, a small girl with long ginger hair and a blue scarf standing on the path, game screenshot on a 16px tile grid, cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
```

### `ts_meadow_grass-path`
```
lower_description: flat soft brown dirt path with sparse light speckles, cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
upper_description: flat muted deep green grass with a few small dark grass tufts, sparse and clean, cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
opt3 only: transition_size 0.25, transition_description: short grass fringe with a thin dark edge along the path
```

### `ts_meadow_grass-water`
```
lower_description: calm flat blue river water with a thin pale foam line where it meets the bank, cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
upper_description: (same as grass-path) + upper_base_tile_id 85b48458-e668-48e9-ab68-c57aa28fe613
opt1 transition 0.5: dark earth riverbank ledge with a grassy fringe on top, dropping straight down to the water
opt2 transition 1.0: dark earth riverbank ledge one tile tall with a grassy fringe on top, dropping straight down to the water
opt3 transition 0.5: low dark stone and earth river wall with a grassy lip, simple and bold
```

### `chr_awa`
```
12 year old girl explorer, long straight ginger hair loosely tied, knee-length oatmeal and rust tunic, faded blue scarf, small leather satchel on a strap across body, leggings, sturdy brown boots, holding a plain wooden walking stick, curious expression, cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
```

### `obj_trees`
```
oak (48×48): round leafy English oak tree with a dense rounded canopy and a short thick trunk, seen from a high top-down angle, cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
birch (32×48): slender silver birch tree with a pale white trunk and a light airy leafy canopy, seen from a high top-down angle, cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
```

### `ts_forest`
```
lower_description: (approved grass) + lower_base_tile_id 85b48458-e668-48e9-ab68-c57aa28fe613
opt1/opt2 upper: dense dark green forest canopy seen from above, rounded leafy tree crowns packed together, olive highlights on top-left, cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
opt3 upper: thick woodland of round leafy treetops seen from above, dark green with olive highlights, cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
opt1 transition 0.25: rounded edge of the canopy with a dark shadow and a few tree trunks showing beneath it
opt2 transition 1.0: a row of tree trunks and dark shade beneath the edge of the canopy
opt3 transition 0.5: bumpy rounded canopy edge casting a dark shadow onto the grass
```

<!-- Add one block per asset. -->

---

## 6. Rejected / retired

| ID | Reason | Date |
|---|---|---|
| — | — | — |

v0.x rejections: see `docs/archive/ASSET_MANIFEST_v0.md`.
