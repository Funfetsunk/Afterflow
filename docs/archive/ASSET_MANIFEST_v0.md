# Afterflow — Asset Manifest archive: Phase 0 v1 (superseded)

> Everything here was superseded by the 16-bit direction reset on 2026-09-25 (Art Bible §0). The files were deleted from `art/` on 2026-09-25 and survive in git history (commit `3dc26cf` and earlier). Kept for the lessons learned and the generation record. The matching PixelLab-side assets (20 characters, 12 tilesets, 2 building kits, 40 objects; exactly the IDs listed here) were deleted from Tom's PixelLab account on 2026-09-25 at his request.

## 3. Shared parameters

Unless a row says otherwise, every asset uses the Art Bible §3 defaults: `low top-down` (tilesets: `high top-down`), `selective outline`, `basic shading`, `medium detail`, 4 directions, 32px tiles, plus the standard style suffix. The tool and mode for each asset class are in Art Bible §3.0. The "Credits" columns record **generations** spent.

---

## 4. Phase 0 v1: sample set (superseded 2026-09-25)

### 4.1 Characters

| ID | Asset | Canvas | Animations | PixelLab char ID | Variants | Chosen | Credits | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `chr_awa_a` | Awa, natural proportions | 64 | idle, walk | v1 `8bda0c99-1bf8-4a38-8098-5b84435dd1b1`<br>v2 `ed05190f-6949-473c-8c68-6c43a691895d`<br>v3 `cca51333-238b-4e40-88bb-2471fcee6be9`<br>v4 `d4feabd1-0633-4494-96e2-a7a9284c268f` | 4 | — | 4 | rejected | Proportion test A. Files `chr_awa_a_opt1..4_<dir>.png` (`optN` = candidate, not an approved version). Output canvas 92×92, figure 64–73px tall including the stick. Standard mode, custom proportions `head_size 0.75, arms_length 1.0, legs_length 1.15, shoulder_width 0.9, hip_width 1.0` |
| `chr_awa_b` | Awa, semi-natural (~4 heads) | 64 | idle, walk | v1 `84b9fb9c-c78b-447e-a90a-572e7f9c66e7`<br>v2 `028168c8-6c39-4984-ace1-cee41aea6d1f`<br>v3 `1ff98f42-5fa2-410a-88dc-974e4a965a89`<br>v4 `5623fac1-3037-42fd-b4ce-6107505db80b` | 4 | — | 4 | rejected | Proportion test B. Files `chr_awa_b_opt1..4_<dir>.png` (`optN` = candidate, not an approved version). Output canvas 92×92, figure 64–73px tall including the stick. Standard mode, custom proportions `head_size 1.15, arms_length 0.85, legs_length 0.85, shoulder_width 0.9, hip_width 1.0` |
| `chr_awa_a` (round 2) | Awa, natural proportions | size 40 | idle, walk | opt5 `d2ae985b-0b48-483e-8b89-f50a664913a0`<br>opt6 `7a22ff4f-d79b-463e-b971-6440cf8fe691`<br>opt7 `06e1daa3-6c98-4bba-9e6b-220a40f965b0`<br>opt8 `9e946017-d28e-4695-b8f1-b46e7e76b2e6` | 4 | **opt5** | 4 | approved | Standard mode, preset `stylized`. Canvas 56×56, figure 40–42px. **Tom chose opt5 (2026-09-25).** Scarf recoloured to blue with `tools/recolour.py`, see §5. Final files: `art/final/chr_awa_a_<dir>.png`. **Approved by Tom, 2026-09-25**, with the scarf fix. Animations still to do. Files `chr_awa_a_opt5..8_<dir>.png` |
| `chr_awa_b` (round 2) | Awa, semi-natural (~4 heads) | size 40 | idle, walk | opt5 `5770fdd2-236c-4f5e-a2df-6c80d0f76adc`<br>opt6 `ae5c0edf-fbe5-4dc2-bac9-6f5bffedfbf3`<br>opt7 `9f9c5451-46d7-40c7-ae93-53a63050a821`<br>opt8 `b3b8e18d-6f19-4340-9314-f960fd84962b` | 4 | — | 4 | rejected | Standard mode, preset `cartoon`. Canvas 56×56, figure 37–39px. Variant A won the proportion test. Files `chr_awa_b_opt5..8_<dir>.png` |
| `npc_villager01` | Villager: the miller (GDD §10 candidate) | size 40 | idle | opt1 `8731f4d7-44c5-4d46-b555-4af48ddebbf0`<br>opt2 `1d32d66e-ea14-4c22-9909-1689a1761109`<br>opt3 `f01d0b17-d471-4746-a098-cb5d4ca73fef`<br>opt4 `b6930593-3d9c-4e21-9589-2a1b53d0ce82` | 4 | **opt1** | 4 | approved | **Approved by Tom, 2026-09-25** ('Miller is fine'). Standard mode, `stylized` preset (matches Awa). Muted colours, no ginger or blue, so Awa stays the most readable figure. opt1: bearded, flat cap |
| `enm_meadow01` | Meadow creature (moss/petal, pale-glow signature) | 48 | idle | — | — | — | — | planned | Sets the enemy family signature |

### 4.2 Tilesets

| ID | Asset | Tile | Lower / upper terrain | PixelLab tileset ID | Variants | Chosen | Credits | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `ts_meadow_grass-path` | Meadow grass ↔ dirt path | 32 | worn dirt path (lower) / grass (upper) | opt1 `0118a881-47c2-4676-897e-7c5fd39a432b`<br>opt2 `e36260f4-2900-42b3-bf93-02d61adb2545`<br>opt3 `66603775-e1b1-4a15-b4b0-043de9803292` | 3 | — | 12 | rejected | Standard mode, `high top-down`, transition 0.25. Each cost 4 generations. Review mocks: `art/mocks/mock_tiles_grass-path_opt1..3`. The metadata JSON sits next to each raw sheet. Grass base tile IDs (for chaining): opt1 `7a626433-9713-40a4-9c9e-772ef67bde3e`, opt2 `00916dff-3832-460b-a5a9-1771c03cd544`, opt3 `e0a97c7b-bd09-494b-85e3-8a6a24374b3c`. `seed` is rejected by the server despite being in the schema |
| `ts_meadow_grass-path` (round 2) | Meadow grass ↔ dirt path | 32 | dirt footpath (lower) / opt1 grass, chained (upper) | opt4 `299b845c-84df-4e6c-a0e9-f8c54435fd65`<br>opt5 `b37306a7-7e82-4ecb-9644-2c9297f1b22d`<br>opt6 `f2e1880a-cf87-4234-806a-bdc0d44602b1` | 3 | — | 6 | rejected | opt5's path tile was carried into round 3 through chaining. 2 generations each, cheaper when chained. Review mocks: `art/mocks/mock_tiles_grass-path_opt4..6`. Round 1 paths looked sunken, like cliffs. Round 2: `transition_size 0`, `upper_base_tile_id` = opt1 grass `7a626433-9713-40a4-9c9e-772ef67bde3e`, flat-path wording |
| `ts_meadow_grass-path` (round 3) | Meadow grass ↔ dirt path | 32 | opt5 path, chained (lower) / new low-detail grass (upper) | opt7 `798acd37-3538-4719-a1b4-54065bcf2a59`<br>opt8 `2f05aa5c-f23e-492b-a04d-24f2c4a3fb19`<br>opt9 `dbd4ec8a-d465-4a10-92ca-9e4c67e5171f` | 3 | **opt7** | 6 | approved | **Approved by Tom, 2026-09-25** (opt7 grass recoloured to olive, plus fill variants; the path is opt5's). Tom: opt5 path good, but the grass repeated too visibly. `lower_base_tile_id` = opt5 path `be051fd0-b806-48fa-80cc-73372fb70513`; `detail: low detail` (exception to Art Bible §3 for ground fill). opt7 grass is 2-colour irregular speckle, recoloured lime→olive: `recolour.py ... --map 91db69=a2a947 d5e04b=cddf6c` → `art/final/ts_meadow_grass-path_opt7_olive.png`. Fill variants: `fill_variants.py art/final/ts_meadow_grass-path_opt7_olive.png 0 96 art/final/ts_meadow_grass-fill --tile 32` → `_00`–`_07`. opt8 teal sprigs in a grid, opt9 orange dash grid: rejected |
| `ts_meadow_grass-water` | Meadow grass ↔ river water | 32 | river water (lower) / approved grass, chained (upper) | opt1 `82f02a27-85f2-4714-99e8-0abd796d497b`<br>opt2 `50b6d4ff-771a-4e65-8277-4da8b3fc66be`<br>opt3 `c2b57419-e2ff-4f0f-a4d7-980446293837` | 3 | **opt2** | 8 | approved | **Approved by Tom, 2026-09-25**: opt2, water recoloured to teal, calm ripple variants. Recipe: `recolour.py art/final/ts_meadow_grass-water_opt2.png ..._opt2_olive.png --map 91db69=a2a947 d5e04b=cddf6c`, then `recolour.py ..._opt2_olive.png ..._opt2_teal.png --map 9babb2=0b8a8f`, then `fill_variants.py art/final/ts_meadow_grass-water_opt2_teal.png 64 32 art/final/ts_meadow_water-fill --thin 0.6 0.4 0.25 0 --stroke-colour 8ff8e2 --seed 7 --tile 32` (keep only `_00`–`_03`: rotations would turn the ripples; `_thin0`–`_thin3` are calmer copies). Ripples are horizontal, so rivers should run mostly east–west; flow direction and motion come from a Godot scroll shader, which stops when drained. River spine. Review mocks: `art/mocks/mock_tiles_grass-water_opt1..3` (grass recoloured to olive, fill variants scattered). `upper_base_tile_id` = approved grass `7b2ed5ec-0dcd-40b7-acd3-7edeb03c23f4`, `detail: low detail`. opt1–2: muddy bank, transition 0.25; opt3: flush edge, transition 0. The grass needs the olive recolour |
| `ts_woodland_floor` | Old woodland (second pass) | 32 | leaf litter / forest undergrowth | — | — | — | — | planned | Darker-biome test |

### 4.3 Map objects

| ID | Asset | Size | PixelLab object ID | Variants | Chosen | Credits | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| `obj_cottage01` | Stone and timber cottage, slate roof | 96×96 canvas | opt1 `d7c49ef3-0a60-418b-841c-bb868caa86ef`<br>opt2 `29c76286-8125-4a38-b18a-45ab469e109a`<br>opt3 `17b663eb-a3a5-4b71-9f08-b499efcf1cff`<br>opt4 `298a6e66-4296-452b-b860-086d066c83bc` | 8 | **opt8** | 8 | approved | **Approved by Tom, 2026-09-25: opt8** (cartoony round 2). Final file: `art/final/obj_cottage01.png` (copy of `obj_cottage01_opt8.png`). **Consistency test (opt9–12, same prompt, 4 generations):** `c82161cd-9d67-4f1d-8177-c3c71198fda4`, `19a8efe8-a780-47c7-9399-6b5f5dd9cce7`, `750f714b-62c6-46cc-9d56-083674e7345a`, `304fa274-7871-4ba0-bb41-82c161d97af8`: all 4 match opt8's style, with varied roofs; opt9/10 face the front, opt11/12 are slightly angled. The style is repeatable. opt1–4 rejected: Tom wanted it 'a little more cartoony'. Round 2 (opt5–8): `a97790ae-81de-469f-b7d7-74048b60f006`, `8485e2e7-3982-4a0c-95f8-ea3f8cab2df8`, `4d88ec3a-42f6-4bfe-b582-0b4bbdf2b517`, `8ad7c801-a120-434a-b3c7-40289c7ada00`, 4 generations, in review: `art/mocks/mock_objects_cottage01_r2`. Lived-in. `create_map_object`, 1 generation each. opt1/opt3 face the front (matches the tile grid); opt2/opt4 are angled. Mock: `art/mocks/mock_objects_cottage01` |
| `obj_ruin01` | Roofless overgrown stone cottage | 96×96 canvas | opt1 `ef97e8a5-abfb-4401-b601-97247a00a515`<br>opt2 `5b6f813c-4a3c-41d6-b05d-0984cc3cd3fa`<br>opt3 `2f5923d6-e8b7-4f95-b872-6e16796cf001`<br>opt4 `8ba9272a-19fe-4b38-b908-3fd0c653e6d0`<br>opt5 `d56b7723-a9e8-4694-b8d3-24dbe4b7c491`<br>opt6 `fe95e339-ecf6-4fcc-8880-6b2ff9e8c504`<br>opt7 `a3347132-d912-49a4-bb05-0043a34abb64`<br>opt8 `281dde02-9a7f-447b-baf7-912c066a5dcf` | 8 | — | 8 | rejected | Tom chose a building kit instead (2026-09-25). Abandonment layer. Both rounds kept a roof despite the wording; opt5 comes closest (a partly collapsed roof). Round 2 had a stronger 'no roof, front view' prompt. Mocks: `mock_objects_ruin01`, `mock_objects_ruin01_r2` |
| `obj_ruin_kit` | Ruin building kit: mossy low stone walls, doorways, corners (roofless by construction) | 32×24 cells on 52×63 pieces | kit `cd06f577-a689-4ae8-8315-f3cca30d9746` | 1 | kit | 20 | rejected | **Retired 2026-09-25:** Tom: 'I don't like the angular stuff at all', so ruins are built from crumbled wall pieces only. Tiles stay in `art/raw|final/obj_ruin_kit/` for reference.  `create_building_kit`, `square_topdown`, `tile_size 32`, `wall_tiles 1`. 80 pieces in `art/raw/obj_ruin_kit/` (index → role in the get_tiles_pro placement rules; outer corners NW=12 NE=9 SW=11 SE=10, sides N=1 S=3 W=4 E=2, south door 36/37). **Cells are 32×24 (foreshortened), not 32×32**, so ruins are baked into single sprites (anchor (10,31), 32×24 pitch) and placed as objects, with meadow grass showing through. Review: `art/mocks/review_obj_ruin_kit_baked.png` |
| `obj_ruin_props` | Rubble, ferns and a bush to soften ruin breaks | 32×32 (rubble02 64×32) | rubble01 `dde39acc-62d8-4bb2-a9d6-39c03898513e`<br>rubble02 `d35e520e-0413-4c34-9be0-489ac1db622f`<br>ferns01 `2e0de861-dc9c-4805-bb5b-f5894463c2e2`<br>bush01 `cf457baf-6b47-41b0-8abc-1f87db131323` | 4 | — | 4 | review | `create_map_object`, locked params. Files `obj_rubble01/02`, `obj_ferns01`, `obj_bush01`. Natural-ruin trial: `art/mocks/review_obj_ruin_kit_natural.png` |
| `obj_ruin_breaks` | Broken-wall pieces and rubble to make kit ruins look natural (Tom chose option B) | 48×48 / 64×48 / 32×32 | wallend opt1 `40b6723b-51ae-4b05-9c32-d314eafd4385`, opt2 `e35e17a4-c312-4ddd-9075-e78c57b1b677`<br>wallcrumble opt1 `f389c6a6-4c61-4249-b7d9-8b55ffdf5b28`, opt2 `2d173c17-040e-4ece-ad5c-f4102a82b5b6`<br>rubble03 opt1 `2998c747-898a-409b-bc15-fe0b2aa2c707`, opt2 `0ea64457-81e4-465f-aa53-f2c9a21ef07d` | 6 | wallcrumble opt1+opt2 | 6 | approved | **wallcrumble opt1 and opt2 approved by Tom, 2026-09-25** ('keep the crumbled walls'). Final files: `art/final/obj_wallcrumble01.png`, `obj_wallcrumble02.png`. Grass base removed: `recolour.py art/final/obj_wallcrumbleNN.png art/final/obj_wallcrumbleNN_clean.png --strip-ground 4c3e24 676633 a2a947 --ground-outline 2e222f` (use the `_clean` files). Scene: `art/mocks/review_ruin_fragments_scene_v2.png`. wallend opt1/2 came out as doorways and rubble03 opt1 as a pink slab: all three rejected. wallcrumble opt1 (low, uneven) and opt2 (steps down) work; rubble03 opt2 is subtle scatter. Hero ruin trial: `art/mocks/review_ruin_hero_scene.png` |
| `obj_ruin_breaks` (round 2) | More crumbled shapes: corner, north–south wall, long run, stub | 64×64 / 32×64 / 96×48 / 32×32 | corner opt1 `156c9bd5-fc85-4481-ac36-3286af7e3441`, opt2 `bc0a4824-30e8-4ecc-9a0b-ff21385cdd09`<br>wallns opt1 `d3edd315-b8c2-4b55-93d7-2ae31116ed7c`, opt2 `803b5721-e5d4-4204-9444-a7762bd2205e`<br>wallcrumble opt3 `1f12610e-e2ef-49e7-a994-981888aa198d`<br>stub `9388f296-c675-4120-85b9-ada15ca14f33` | 6 | — | 6 | rejected | wallcrumble opt3 rejected by Tom: 'looks too different' (flatter, purple bricks). Corners came out as crenellated castle corners, the north–south walls as a pyramid and a staircase, the stub as a well: all rejected. Ruins are therefore built from east–west fragments (mirrored for variety) plus plants: `art/mocks/review_ruin_fragments_scene.png` |
| `obj_cottage_kit` | Test: paintable cottage building kit (Tom asked for RPG Maker-style painted buildings) | 32×32 cells on 52×98 pieces | kit `a94fa868-ae8a-423f-9bc4-a754df831ee5` | 1 | — | 20 | review | `create_building_kit`, `square_topdown`, `tile_view_angle 90`, `wall_angle 45`, `wall_tiles 2`, `layout materials`. The grid works (floor cells exactly 32×32, anchor (10,56)), but the materials are flat, 2 storeys dwarf Awa, and the roof pieces don't read as a roof when assembled (the front wall hides under a flat slab). Reviews: `art/mocks/review_cottage_kit_boxes.png`, `review_cottage_kit_gable.png`, `review_cottage_kit_sheet.png` |
| `obj_shrine01` | Shrine (respawn point) | 32×64 canvas | opt1 `38d8b195-8d85-46d8-880b-0f4a79017b72`<br>opt2 `44ef2783-d5ee-4084-b688-adde3ffd88b3`<br>opt3 `92352ea3-59c3-4dc4-8892-eba8bec9e342`<br>opt4 `5833ec1c-4b5b-42c8-9bad-a35d920c489d` | 4 | **opt2** | 4 | approved | **Approved by Tom, 2026-09-25**: opt2 with pale glow A. Final file: `art/final/obj_shrine01.png` = `recolour.py art/final/obj_shrine01_opt2.png art/final/obj_shrine01.png --map fbff86=c7dcd0 fbb954=9babb2`. Story object: old, calm, faintly strange. The glow came out warm orange; pale-glow recolour trials on opt2: `art/mocks/review_obj_shrine01_glow_trials.png` (A: `fbff86=c7dcd0 fbb954=9babb2`, B: `fbff86=8ff8e2 fbb954=0eaf9b`) |

### 4.4 Mock screenshots

| ID | Scene | Contents | Palette | Status | Notes |
|---|---|---|---|---|---|
| `mock_meadow_village` | Meadow village | Awa, villager, 2 cottages, path, river edge, crumbled ruin, shrine | Resurrect 64 | review | `art/mocks/mock_meadow_village_v1(_4x).png`; layout `tools/mock_layouts/mock_meadow_village.json`, map `map_meadow_village.txt` |
| `mock_overgrown_ruin` | Ruin in the meadow | Awa, ruin, shrine, enemy | Resurrect 64 | planned | |
| `mock_drained` | Drained version of the meadow | Same as above, with a simulated drain colour shift | Resurrect 64 | review | `art/mocks/mock_meadow_village_v1_drained(_4x).png`. Awa is excluded from the drain (`nodrain`), as in-game |
| `mock_meadow_custom` | Meadow village | Same as `mock_meadow_village` | Custom warm/cold | planned | Palette comparison |
| `mock_woodland` | Old woodland | Awa, woodland tiles, enemy | Winner | planned | Second pass |

---

## Prompt log (v1)

### `chr_awa_a` (round 1, opt1–4)
```
12 year old girl explorer, long straight ginger hair loosely tied, knee-length oatmeal and rust tunic, faded blue scarf, brown leather satchel across body, leggings, sturdy brown boots, holding a plain wooden walking stick, curious expression, natural proportions, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

### `chr_awa_b` (round 1, opt1–4)
```
12 year old girl explorer, long straight ginger hair loosely tied, knee-length oatmeal and rust tunic, faded blue scarf, brown leather satchel across body, leggings, sturdy brown boots, holding a plain wooden walking stick, curious expression, slightly stylised ~4 heads tall, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

### `chr_awa_a` (round 2, opt5–8)
```
12 year old girl explorer, long straight ginger hair loosely tied, knee-length oatmeal and rust tunic, faded blue scarf, small leather satchel on a strap across body, leggings, sturdy brown boots, holding a plain wooden walking stick, curious expression, natural proportions, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

**Scarf fix for `chr_awa_a` (apply to every new frame of this character, including animations):**
```
python tools/recolour.py art/final/<in>.png art/final/<out>.png --map 547e64=4d65b4 374e4a=484a77 313638=323353 7f708a=9babb2
```
Greens and violet-grey become the Resurrect 64 blue ramp. Check the leggings afterwards: stray dark-green shading pixels there turn navy, which matches the leggings.

### `chr_awa_b` (round 2, opt5–8)
```
12 year old girl explorer, long straight ginger hair loosely tied, knee-length oatmeal and rust tunic, faded blue scarf, small leather satchel on a strap across body, leggings, sturdy brown boots, holding a plain wooden walking stick, curious expression, slightly stylised ~4 heads tall, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

### `ts_meadow_grass-path`
```
lower_description: worn dirt path, packed earth with small pebbles, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
upper_description: warm olive and yellow-green meadow grass, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
transition_description: soft grass edge with small tufts over the dirt
transition_size: 0.25
```

### `ts_meadow_grass-path` (round 2, opt4–6)
```
lower_description: soft brown dirt footpath, packed earth, faint worn texture, flat and level with the grass, no height difference, no cliff edge, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
upper_description: warm olive and yellow-green meadow grass, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
upper_base_tile_id: 7a626433-9713-40a4-9c9e-772ef67bde3e
transition_size: 0
```

### `ts_meadow_grass-path` (round 3, opt7–9)
```
lower_description: soft brown dirt footpath, packed earth, faint worn texture, flat and level with the grass, no height difference, no cliff edge, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
lower_base_tile_id: be051fd0-b806-48fa-80cc-73372fb70513
upper_description: soft meadow grass, low detail, subtle uneven texture, gently varied olive and yellow-green tones, no regular pattern, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
transition_size: 0
detail: low detail
```

### `ts_meadow_grass-water`
```
lower_description: calm shallow river water, soft gentle ripples, muted blue-green, low detail, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
upper_description: soft meadow grass, low detail, subtle uneven texture, gently varied olive and yellow-green tones, no regular pattern, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
upper_base_tile_id: 7b2ed5ec-0dcd-40b7-acd3-7edeb03c23f4
opt1-2: transition_size 0.25, transition_description: low soft muddy riverbank with a few reeds, gently sloping, not a cliff
opt3: transition_size 0
detail: low detail
```

### `obj_cottage01`
```
small English stone cottage, timber framing, grey slate roof, chimney, wooden front door, small windows, flower box, lived-in, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

### `obj_ruin01` (opt1–4)
```
roofless ruined stone cottage, crumbling walls, empty window holes, moss and ivy overgrowth, ferns and grass growing inside, abandoned long ago but alive and green, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

### `obj_ruin01` (opt5–8)
```
ruin of a stone cottage with no roof at all, only broken low stone walls left standing, open to the sky, grassy floor visible inside the walls, moss and ivy on the walls, ferns, abandoned long ago but alive and green, front view, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

### `obj_shrine01`
```
small old stone wayside shrine, weathered carved standing stone with a small niche, faint soft pale glow inside the niche, moss at the base, calm and faintly strange, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

### `obj_ruin_kit`
```
wall_description: mossy broken low stone walls of a ruined cottage, crumbling uneven tops, ivy and small ferns, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
floor_description: overgrown soft meadow grass floor, low detail, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
tile_type: square_topdown, tile_size: 32, wall_tiles: 1
```

### `obj_cottage01` (round 2, opt5–8)
```
cartoony storybook English cottage, chunky rounded shapes, slightly exaggerated proportions, thick soft slate roof with a gentle sag, crooked stone chimney, round-topped wooden door, small round window, stone walls, flower boxes, front view, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

### `obj_ruin_props`
```
rubble01 (32×32): small pile of fallen mossy stones from a ruined wall, tumbled rubble with grass growing between, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
rubble02 (64×32): scattered fallen mossy stones and broken wall blocks half sunk in grass, wide low rubble, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
ferns01 (32×32): lush clump of green ferns, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
bush01 (32×32): small round leafy green bush with a little ivy, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

### `obj_ruin_breaks`
```
wallend (48×48): crumbling broken end of a low ruined stone wall, the wall steps down unevenly to the left into fallen stones, pale beige stone cap on top, dark brown-grey stone face, ivy and moss, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
wallcrumble (64×48): long low crumbled section of a ruined stone wall, uneven broken top, some stones missing, pale beige stone cap, dark brown-grey stone face, ivy and moss, grass at the base, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
rubble03 (32×32): a few flat fallen stone blocks lying in the grass, square-cut wall stones, pale beige tops, some moss, no face, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

### `obj_ruin_breaks` (round 2)
```
corner (64×64): L-shaped corner of a long low crumbled ruined stone wall, two walls meeting at a corner, uneven broken tops, some stones missing, pale beige stone cap, dark brown-grey stone face, ivy and moss, grass at the base, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
wallns (32×64): long low crumbled ruined stone wall running away from the viewer, north to south, seen from above and slightly in front, uneven broken top, some stones missing, pale beige stone cap, dark brown-grey stone, ivy and moss, grass at the base, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
wallcrumble opt3 (96×48): same prompt as wallcrumble
stub (32×32): short low crumbled stub of a ruined stone wall, just a few courses of stones left, uneven broken top, pale beige stone cap, dark brown-grey stone face, ivy and moss, grass at the base, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

### `npc_villager01`
```
friendly middle-aged village miller, flour-dusted cream apron over a brown waistcoat, rolled-up sleeves, flat cap, brown trousers, sturdy boots, kind expression, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

### `obj_cottage_kit`
```
wall_description: cartoony storybook English cottage walls, chunky rounded pale stones with soft cream mortar, slightly uneven, warm and cosy, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
floor_description: warm wooden plank cottage floor, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
floor2_description: soft chunky dark plum slate roof tiles with a gentle sag, cartoony storybook roof, cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
tile_type: square_topdown, tile_size: 32, wall_tiles: 2, tile_view_angle: 90, wall_angle: 45, layout: materials
```

## 6. Rejected / retired

| ID | Reason | Date |
|---|---|---|
| `chr_awa_a` opt1–4, `chr_awa_b` opt1–4 | Round 1: `size: 64` gave ~2-tile-tall figures; proportions didn't separate A from B | 2026-09-25 |
| `chr_awa_a` opt6–8 | Round 2: not chosen (opt8 also read as bare legs) | 2026-09-25 |
| `chr_awa_b` opt5–8 | Round 2: variant A won the proportion test (opt7 also read as bare legs) | 2026-09-25 |
| `ts_meadow_grass-path` opt1–3 | Paths looked sunken, like cliffs; the path textures read as carpet, planks or cobbles | 2026-09-25 |
| `ts_meadow_grass-path` opt4–6 | Flat paths were fine (opt5's was kept), but the grass repeated too visibly | 2026-09-25 |
| `ts_meadow_grass-path` opt8–9 | Grass marks lined up in a visible grid | 2026-09-25 |
| `ts_meadow_grass-water` opt1 | Striped sage water, too close to the grass colour | 2026-09-25 |
| `ts_meadow_grass-water` opt3 | Flush edge, water barely separates from the grass | 2026-09-25 |
| `obj_ruin_kit` | Angular geometry; Tom prefers crumbled walls only | 2026-09-25 |
| `obj_wallcorner` opt1–2, `obj_wallns` opt1–2, `obj_wallstub` | Angular corners, pyramid, staircase, well | 2026-09-25 |
| `obj_wallend` opt1–2, `obj_rubble03` opt1 | Came out as doorways / a pink slab | 2026-09-25 |

