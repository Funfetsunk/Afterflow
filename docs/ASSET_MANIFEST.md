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
| 2026-09-21 → 2026-10-21 | Tier 1 (Pixel Apprentice) | 159 | 859 of 2,000 were already used this cycle before Afterflow started; 1,140 left on 2026-09-25; 1,000 left after north-star round 1; 990 after 16px grass-path; 981 after the 16px river |

---

## 3. Shared parameters

Unless a row says otherwise, every asset uses the locked Art Bible §3 parameters (`high top-down`, `single color black outline`, `basic shading`, `low detail`, 4 directions, 16px tiles) and the Art Bible §3.1 style suffix, is remapped to the Afterflow v1 palette (`tools/palettes/afterflow-v1.hex`), and matches the north star. The "Credits" columns record **generations** spent.

---

## 4. Phase 0 v2: 16-bit rebuild

Direction reset on 2026-09-25 (Art Bible §0): 320×180, 16px tiles, 16-bit SNES-era top-down style. The superseded v0.x record is in `docs/archive/ASSET_MANIFEST_v0.md`.

| ID | Asset | Size | PixelLab ID(s) | Variants | Chosen | Credits | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| `ns_meadow_village` | North-star screen: meadow village | 320×180 | r1: pixflux opt1–4 `3dbacb68-e21e-40e3-8f42-90801e7a1cdc`, `7125c297-cd92-4af2-802a-24697a796597`, `14d236de-e843-4bd2-8456-c7729eed7476`, `30424275-a201-4494-bd23-3344c1a90fa4`; pixen opt5–8 `e503ab74-76bc-457a-ab13-5256c282ed8e`, `eae764ff-9567-4ca5-8f75-6e5ef23d3598`, `d3f0dffd-1326-423f-8408-1102b6623364`, `304468a2-33b6-4a29-a262-e7e76350ca0b` | 8 | **r2 mix** | 8 | approved | **North star approved and locked by Tom, 2026-09-25** ('I love the style'). Tom noticed slight discolouration in Awa's hair: her restored pixels aren't a clean ramp, so don't use this image as Awa's reference. Art Bible §3.2 step 1. Seeds 1–4 per model; opt1–2/5–6 `medium detail`, opt3–4/7–8 `low detail`; `high top-down`, `single color black outline`, `basic shading` (pixflux). Only r1 opt4 and opt6 are kept in `art/raw|final/north_star/` (the r2 inputs); the others are in git history. Sheet: `art/mocks/review_north_star_r1.png`. opt5/opt7 came out letterboxed. **r2 (Tom: 'opt4 layout with opt6 colours', 0 generations):** `art/final/north_star/ns_meadow_village_r2_mix.png` = opt4 recoloured by material into opt6's colours: `recolour.py art/final/north_star/ns_meadow_village_r1_opt4.png art/final/north_star/ns_meadow_village_r2_mix.png --map a2a947=547e64 676633=374e4a 374e4a=313638 d5e04b=676633 fca790=966c6c c7dcd0=ab947a 7f708a=966c6c 323353=3e3546 165a4c=374e4a 547e64=676633 484a77=4d65b4 4d9be6=8fd3ff 9babb2=ab947a 6e2727=4c3e24 753c54=45293f 7a3045=45293f e6904e=966c6c cd683d=9e4539 c32454=fbb954 a24b6f=ffffff`, then Awa's original pixels restored in the box (116,80)–(140,108) so she keeps her ginger hair. Review: `art/mocks/review_north_star_r2_mix_6x.png` |
| `chr_awa` | Awa, 16-bit | ~24–28px | — | — | — | — | planned | After the north star |
| `ts_meadow_grass-path` | Meadow grass ↔ dirt path | 16px | opt1 `8ac020c5-a28a-4d5b-b459-9a2fcb463352`<br>opt2 `ef8b1e7d-c1b8-40e4-a2b4-7345c28494da`<br>opt3 `475e723f-b5ea-4a60-8379-170c91b7133a` | 3 | **opt3** | 10 | approved | **Approved by Tom, 2026-09-25.** opt1: orange patterned path; opt2: yellow grass; opt3 closest to the north star. opt3 recipe: `palette_remap.py ... --palette tools/palettes/afterflow-v1.hex`, then `recolour.py art/final/ts_meadow_grass-path_opt3.png art/final/ts_meadow_grass-path_opt3_ns.png --map ab947a=966c6c 966c6c=ab947a 323353=313638 625565=374e4a 753c54=45293f` (path base/speck swap, edge colours to the north star's). Grass tufts: 8 tufted 16×16 grass tiles cut from the north star → `art/final/ts_meadow_grass-fill_ns0..7.png` (grass-only windows with a clean 547e64 border), scattered at ~45%. Review: `art/mocks/review_v2_grass-path_vs_north_star.png`. `create_topdown_tileset` standard, 16px, `high top-down`, `single color outline`, `basic shading`, `low detail`. opt1–2 flush (transition 0), opt3 grass fringe (0.25). Grass base tiles: opt1 `dcac0256-d8b6-40c9-a614-3ec956cb11cc`, opt2 `f1678a83-d09b-4ad3-a520-f7bf4bc43e19`, opt3 `85b48458-e668-48e9-ab68-c57aa28fe613` |
| `ts_meadow_grass-water` | Meadow grass ↔ river (ledge) | 16px | opt1 `a2dc6317-4a20-44e9-937e-148f57c864c9`<br>opt2 `10fd48dd-3904-4591-87a5-6fa6754cc02a`<br>opt3 `62b5d23f-d47d-4d15-b11f-3ea69f845298` | 3 | **opt2** | 9 | approved | **Approved by Tom, 2026-09-25** (opt2 recoloured plus the cut ledge pairs on straight runs). Rivers run straight east–west for now; bends need corner tiles adjusted to the north star's ledge height. opt1/opt3: thin lip, bright flat blue water. opt2: one-tile cliff ledge (25-tile layout; ledge row marked `=` in wang_layout maps), north-star water blue and foam line, but the ledge face came out as orange/pale vertical planks. opt2 recipe: remap to afterflow-v1, then `recolour.py art/final/ts_meadow_grass-water_opt2.png art/final/ts_meadow_grass-water_opt2_ns.png --map 753c54=45293f 323353=2e222f ab947a=3e3546 cd683d=9e4539 fbb954=9e4539 7f708a=3e3546 625565=45293f d5e04b=374e4a 966c6c=45293f`. Reviews: `art/mocks/review_v2_grass-water_options.png`, `review_v2_grass-water_vs_north_star.png`. **Straight ledge runs use 7 matched top/bottom pairs cut from the north star's riverbank** (y 144–176, windows clear of the path; top row grass tones, bottom row water tones) → `art/final/ts_meadow_ledge_ns_top0..6.png` / `_bot0..6.png`, placed with `wang_layout.py --ledge-pairs art/final/ts_meadow_ledge_ns`. The north star's ledge is ~1.2 tiles tall against the tileset's ~1.75, so **bends and ends still use the tileset tiles and won't match in height yet**. Review: `art/mocks/review_v2_river_nsledge_vs_north_star.png`. `upper_base_tile_id` = approved grass `85b48458-e668-48e9-ab68-c57aa28fe613`. opt1: earth ledge, transition 0.5; opt2: one-tile ledge, transition 1.0 (25 tiles); opt3: low stone/earth wall, 0.5 |
| `ts_village_buildings` | Building tiles (walls, roofs, doors, windows) | 16px | — | — | — | — | planned | Painted, not one-off sprites |
| `npc_villager01` | The miller, 16-bit | ~24–28px | — | — | — | — | planned | |
| `obj_shrine01` | Shrine, 16-bit | 16×32 | — | — | — | — | planned | |
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

<!-- Add one block per asset. -->

---

## 6. Rejected / retired

| ID | Reason | Date |
|---|---|---|
| — | — | — |

v0.x rejections: see `docs/archive/ASSET_MANIFEST_v0.md`.
