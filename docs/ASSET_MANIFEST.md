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
| 2026-09-21 → 2026-10-21 | Tier 1 (Pixel Apprentice) | 40 | 859 of 2,000 were already used this cycle before Afterflow started; 1,140 left on 2026-09-25; 1,100 left after grass-path round 3 |

---

## 3. Shared parameters

Unless a row says otherwise, every asset uses the Art Bible §3 defaults: `low top-down` (tilesets: `high top-down`), `selective outline`, `basic shading`, `medium detail`, 4 directions, 32px tiles, plus the standard style suffix. The tool and mode for each asset class are in Art Bible §3.0. The "Credits" columns record **generations** spent.

---

## 4. Phase 0: sample set

### 4.1 Characters

| ID | Asset | Canvas | Animations | PixelLab char ID | Variants | Chosen | Credits | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `chr_awa_a` | Awa, natural proportions | 64 | idle, walk | v1 `8bda0c99-1bf8-4a38-8098-5b84435dd1b1`<br>v2 `ed05190f-6949-473c-8c68-6c43a691895d`<br>v3 `cca51333-238b-4e40-88bb-2471fcee6be9`<br>v4 `d4feabd1-0633-4494-96e2-a7a9284c268f` | 4 | — | 4 | rejected | Proportion test A. Files `chr_awa_a_opt1..4_<dir>.png` (`optN` = candidate, not an approved version). Output canvas 92×92, figure 64–73px tall including the stick. Standard mode, custom proportions `head_size 0.75, arms_length 1.0, legs_length 1.15, shoulder_width 0.9, hip_width 1.0` |
| `chr_awa_b` | Awa, semi-natural (~4 heads) | 64 | idle, walk | v1 `84b9fb9c-c78b-447e-a90a-572e7f9c66e7`<br>v2 `028168c8-6c39-4984-ace1-cee41aea6d1f`<br>v3 `1ff98f42-5fa2-410a-88dc-974e4a965a89`<br>v4 `5623fac1-3037-42fd-b4ce-6107505db80b` | 4 | — | 4 | rejected | Proportion test B. Files `chr_awa_b_opt1..4_<dir>.png` (`optN` = candidate, not an approved version). Output canvas 92×92, figure 64–73px tall including the stick. Standard mode, custom proportions `head_size 1.15, arms_length 0.85, legs_length 0.85, shoulder_width 0.9, hip_width 1.0` |
| `chr_awa_a` (round 2) | Awa, natural proportions | size 40 | idle, walk | opt5 `d2ae985b-0b48-483e-8b89-f50a664913a0`<br>opt6 `7a22ff4f-d79b-463e-b971-6440cf8fe691`<br>opt7 `06e1daa3-6c98-4bba-9e6b-220a40f965b0`<br>opt8 `9e946017-d28e-4695-b8f1-b46e7e76b2e6` | 4 | **opt5** | 4 | approved | Standard mode, preset `stylized`. Canvas 56×56, figure 40–42px. **Tom chose opt5 (2026-09-25).** Scarf recoloured to blue with `tools/recolour.py`, see §5. Final files: `art/final/chr_awa_a_<dir>.png`. **Approved by Tom, 2026-09-25**, with the scarf fix. Animations still to do. Files `chr_awa_a_opt5..8_<dir>.png` |
| `chr_awa_b` (round 2) | Awa, semi-natural (~4 heads) | size 40 | idle, walk | opt5 `5770fdd2-236c-4f5e-a2df-6c80d0f76adc`<br>opt6 `ae5c0edf-fbe5-4dc2-bac9-6f5bffedfbf3`<br>opt7 `9f9c5451-46d7-40c7-ae93-53a63050a821`<br>opt8 `b3b8e18d-6f19-4340-9314-f960fd84962b` | 4 | — | 4 | rejected | Standard mode, preset `cartoon`. Canvas 56×56, figure 37–39px. Variant A won the proportion test. Files `chr_awa_b_opt5..8_<dir>.png` |
| `npc_villager01` | Villager (placeholder role) | 64 | idle | — | — | — | — | planned | Matches the winning Awa proportions |
| `enm_meadow01` | Meadow creature (moss/petal, pale-glow signature) | 48 | idle | — | — | — | — | planned | Sets the enemy family signature |

### 4.2 Tilesets

| ID | Asset | Tile | Lower / upper terrain | PixelLab tileset ID | Variants | Chosen | Credits | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `ts_meadow_grass-path` | Meadow grass ↔ dirt path | 32 | worn dirt path (lower) / grass (upper) | opt1 `0118a881-47c2-4676-897e-7c5fd39a432b`<br>opt2 `e36260f4-2900-42b3-bf93-02d61adb2545`<br>opt3 `66603775-e1b1-4a15-b4b0-043de9803292` | 3 | — | 12 | rejected | Standard mode, `high top-down`, transition 0.25. Each cost 4 generations. Review mocks: `art/mocks/mock_tiles_grass-path_opt1..3`. The metadata JSON sits next to each raw sheet. Grass base tile IDs (for chaining): opt1 `7a626433-9713-40a4-9c9e-772ef67bde3e`, opt2 `00916dff-3832-460b-a5a9-1771c03cd544`, opt3 `e0a97c7b-bd09-494b-85e3-8a6a24374b3c`. `seed` is rejected by the server despite being in the schema |
| `ts_meadow_grass-path` (round 2) | Meadow grass ↔ dirt path | 32 | dirt footpath (lower) / opt1 grass, chained (upper) | opt4 `299b845c-84df-4e6c-a0e9-f8c54435fd65`<br>opt5 `b37306a7-7e82-4ecb-9644-2c9297f1b22d`<br>opt6 `f2e1880a-cf87-4234-806a-bdc0d44602b1` | 3 | — | 6 | rejected | opt5's path tile was carried into round 3 through chaining. 2 generations each, cheaper when chained. Review mocks: `art/mocks/mock_tiles_grass-path_opt4..6`. Round 1 paths looked sunken, like cliffs. Round 2: `transition_size 0`, `upper_base_tile_id` = opt1 grass `7a626433-9713-40a4-9c9e-772ef67bde3e`, flat-path wording |
| `ts_meadow_grass-path` (round 3) | Meadow grass ↔ dirt path | 32 | opt5 path, chained (lower) / new low-detail grass (upper) | opt7 `798acd37-3538-4719-a1b4-54065bcf2a59`<br>opt8 `2f05aa5c-f23e-492b-a04d-24f2c4a3fb19`<br>opt9 `dbd4ec8a-d465-4a10-92ca-9e4c67e5171f` | 3 | **opt7** | 6 | approved | **Approved by Tom, 2026-09-25** (opt7 grass recoloured to olive, plus fill variants; the path is opt5's). Tom: opt5 path good, but the grass repeated too visibly. `lower_base_tile_id` = opt5 path `be051fd0-b806-48fa-80cc-73372fb70513`; `detail: low detail` (exception to Art Bible §3 for ground fill). opt7 grass is 2-colour irregular speckle, recoloured lime→olive: `recolour.py ... --map 91db69=a2a947 d5e04b=cddf6c` → `art/final/ts_meadow_grass-path_opt7_olive.png`. Fill variants: `fill_variants.py art/final/ts_meadow_grass-path_opt7_olive.png 0 96 art/final/ts_meadow_grass-fill` → `_00`–`_07`. opt8 teal sprigs in a grid, opt9 orange dash grid: rejected |
| `ts_meadow_grass-water` | Meadow grass ↔ river water | 32 | grass / river water | — | — | — | — | planned | River spine |
| `ts_woodland_floor` | Old woodland (second pass) | 32 | leaf litter / forest undergrowth | — | — | — | — | planned | Darker-biome test |

### 4.3 Map objects

| ID | Asset | Size | PixelLab object ID | Variants | Chosen | Credits | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| `obj_cottage01` | Stone and timber cottage, slate roof | ~3×3 tiles | — | — | — | — | planned | Lived-in |
| `obj_ruin01` | Roofless overgrown stone cottage | ~3×3 tiles | — | — | — | — | planned | Abandonment layer |
| `obj_shrine01` | Shrine (respawn point) | ~1×2 tiles | — | — | — | — | planned | Story object: old, calm, faintly strange |

### 4.4 Mock screenshots

| ID | Scene | Contents | Palette | Status | Notes |
|---|---|---|---|---|---|
| `mock_meadow_village` | Meadow village | Awa A/B, villager, cottage, paths, river edge | Resurrect 64 | planned | |
| `mock_overgrown_ruin` | Ruin in the meadow | Awa, ruin, shrine, enemy | Resurrect 64 | planned | |
| `mock_drained` | Drained version of the meadow | Same as above, with a simulated drain colour shift | Resurrect 64 | planned | Previews the shader |
| `mock_meadow_custom` | Meadow village | Same as `mock_meadow_village` | Custom warm/cold | planned | Palette comparison |
| `mock_woodland` | Old woodland | Awa, woodland tiles, enemy | Winner | planned | Second pass |

---

## 5. Prompt log

Record the **exact** final prompt for every approved asset.

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

<!-- Add one block per asset. -->

---

## 6. Rejected / retired

| ID | Reason | Date |
|---|---|---|
| `chr_awa_a` opt1–4, `chr_awa_b` opt1–4 | Round 1: `size: 64` gave ~2-tile-tall figures; proportions didn't separate A from B | 2026-09-25 |
| `chr_awa_a` opt6–8 | Round 2: not chosen (opt8 also read as bare legs) | 2026-09-25 |
| `chr_awa_b` opt5–8 | Round 2: variant A won the proportion test (opt7 also read as bare legs) | 2026-09-25 |
| `ts_meadow_grass-path` opt1–3 | Paths looked sunken, like cliffs; the path textures read as carpet, planks or cobbles | 2026-09-25 |
| `ts_meadow_grass-path` opt4–6 | Flat paths were fine (opt5's was kept), but the grass repeated too visibly | 2026-09-25 |
| `ts_meadow_grass-path` opt8–9 | Grass marks lined up in a visible grid | 2026-09-25 |
