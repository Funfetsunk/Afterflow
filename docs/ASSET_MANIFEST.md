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
| 2026-09-21 → 2026-10-21 | Tier 1 (Pixel Apprentice) | 140 | 859 of 2,000 were already used this cycle before Afterflow started; 1,140 left on 2026-09-25; 1,000 left after north-star round 1 |

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
| `ts_meadow` | Meadow terrain (grass, path, water) | 16px | — | — | — | — | planned | |
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

<!-- Add one block per asset. -->

---

## 6. Rejected / retired

| ID | Reason | Date |
|---|---|---|
| — | — | — |

v0.x rejections: see `docs/archive/ASSET_MANIFEST_v0.md`.
