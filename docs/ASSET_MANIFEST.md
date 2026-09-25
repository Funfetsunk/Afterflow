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
| 2026-09-21 → 2026-10-21 | Tier 1 (Pixel Apprentice) | 0 | 859 of 2,000 were already used this cycle before Afterflow started; 1,140 left on 2026-09-25 |

---

## 3. Shared parameters

Unless a row says otherwise, every asset uses the Art Bible §3 defaults: `low top-down` (tilesets: `high top-down`), `selective outline`, `basic shading`, `medium detail`, 4 directions, 32px tiles, plus the standard style suffix. The tool and mode for each asset class are in Art Bible §3.0. The "Credits" columns record **generations** spent.

---

## 4. Phase 0: sample set

### 4.1 Characters

| ID | Asset | Canvas | Animations | PixelLab char ID | Variants | Chosen | Credits | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `chr_awa_a` | Awa, natural proportions | 64 | idle, walk | — | — | — | — | planned | Proportion test A |
| `chr_awa_b` | Awa, semi-natural (~4 heads) | 64 | idle, walk | — | — | — | — | planned | Proportion test B |
| `npc_villager01` | Villager (placeholder role) | 64 | idle | — | — | — | — | planned | Matches the winning Awa proportions |
| `enm_meadow01` | Meadow creature (moss/petal, pale-glow signature) | 48 | idle | — | — | — | — | planned | Sets the enemy family signature |

### 4.2 Tilesets

| ID | Asset | Tile | Lower / upper terrain | PixelLab tileset ID | Variants | Chosen | Credits | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `ts_meadow_grass-path` | Meadow grass ↔ dirt path | 32 | grass / worn dirt path | — | — | — | — | planned | |
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

### `chr_awa_a`
```
(not generated yet)
```

### `chr_awa_b`
```
(not generated yet)
```

<!-- Add one block per asset. -->

---

## 6. Rejected / retired

| ID | Reason | Date |
|---|---|---|
| — | — | — |
