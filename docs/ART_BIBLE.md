# Afterflow — Art Bible

> **Status:** v0.7, provisional. Becomes **v1.0** when Phase 0 is approved. Items marked 🔬 are decided by the Phase 0 tests.
> **Rule:** every asset request follows this document. If an asset needs to break a rule, update this document first.

---

## 1. Look in one sentence

A small English countryside, soft storybook pixel art, **warm and golden where the world is alive** and **cold blue-grey and still where it has been drained**, with gentle overgrowth over the ruins of past lives.

---

## 2. Technical grid (locked)

| Setting | Value |
|---|---|
| Internal resolution | **480×270** (integer scale ×4 to 1920×1080) |
| Tile size | **32×32** |
| Screen in tiles | 15 × ~8.4 |
| Perspective | **Low top-down** (3/4) for characters and map objects, **high top-down** for ground tilesets (PixelLab's closest option to square top-down). Never mix angles within an asset class. |
| Character sprite directions | **4** (south, west, east, north) |
| Movement | 8-way analog (sprites don't need diagonals) |
| Pixel density | Uniform. No scaled-up or scaled-down sprites in-game. |

### 2.1 Canvas sizes

🔬 In `create_character` standard mode, **`size` sets roughly the figure height, not the canvas**. The canvas grows around the figure: `size: 64` returned a 92×92 canvas with a 64–73px figure. So choose `size` from the target figure height. Crop or re-pivot the padded canvas in Godot.

| Asset class | `size` (≈ figure height) |
|---|---|
| Awa, NPCs, standard enemies | **40** (target ~38px) |
| Small enemies / critters | **30** (target ~29px) |
| Large enemies | **60** (target ~58px) |
| Bosses | **60–80** |
| Map objects | Canvas in multiples of the 32px grid |

---

## 3. PixelLab parameters (locked)

These apply to every character, creature and object unless this document says otherwise.

| Parameter | Value |
|---|---|
| Camera / view | `low top-down` (tilesets: `high top-down`) |
| Outline | `selective outline` |
| Shading | `basic shading` |
| Detail | `medium detail` |
| Directions | `4` |
| Tileset tile size | `32` |

All enum strings were verified against the PixelLab MCP tool schemas on 2026-09-25.

### 3.0 Which tool for which asset (locked)

Tool defaults don't match the locked parameters, so **always pass every parameter explicitly**.

| Asset class | Tool | Settings | Typical cost |
|---|---|---|---|
| Characters, NPCs, enemies | `create_character`, **`mode: "standard"`** | `view: "low top-down"`, `outline: "selective outline"`, `shading: "basic shading"`, `detail: "medium detail"`, `n_directions: 4`, `size` from §2.1 | 1 generation |
| Ground tilesets | `create_topdown_tileset`, `mode: "standard"` | `view: "high top-down"`, `tile_size: 32` (the default is 16), `outline: "selective outline"`, `shading: "basic shading"`, `detail: "medium detail"` | 1–4 generations, usually 3–4 |
| Map objects | `create_map_object` | `view: "low top-down"`, `outline: "selective outline"`, `shading: "basic shading"`, `detail: "medium detail"`, width/height in multiples of 32 | Check the cost line on first use |

- **Ground fill exception:** large fill terrain (grass etc.) uses `detail: "low detail"` with an irregular, non-directional texture, so it doesn't read as a repeating grid. Break up repetition further with flipped/rotated fill variants (`tools/fill_variants.py`), used as weighted alternative tiles in Godot.
- Only **standard** mode honours all the locked parameters. `v3` and `pro` always produce 8 directions and ignore shading, and `pro` costs 20–40 generations. Don't use them without Tom's approval.
- Don't use `create_1_direction_object` for map objects: it has no outline, shading or detail settings, and it costs 20–40 generations.

### 3.1 Prompt template

Every prompt is built from three parts, always in this order:

```
[SUBJECT] + [SUBJECT DETAILS] + [STYLE SUFFIX]
```

**Style suffix (use verbatim):**
```
cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

For drained-area variants of objects that can't be handled by the shader (rare), swap the suffix for:
```
cosy English countryside, soft storybook pixel art, faded cold blue-grey colours, still and lifeless
```

Record every final prompt in ASSET_MANIFEST.md.

### 3.2 Consistency workflow

1. Generate **3–4 variants** per asset and pick the best.
2. Where a PixelLab tool accepts a style or reference image, use an **approved in-game asset** (from `art/final/`), never an outside reference image.
3. Remap every download to the palette (§6) before judging it.
4. Judge assets **in a mock screenshot** at 480×270, not in isolation.

---

## 4. Awa

### 4.1 Description

- About 12 years old, with **long, straight ginger hair**, loose or loosely tied.
- Inquisitive and capable: **an explorer, not a warrior.**
- **Outfit:** knee-length tunic in **oatmeal and rust** tones, leggings, sturdy brown boots, and a brown leather **satchel** worn across the body (the diary lives here).
- **Signature accent:** a **faded blue scarf**. PixelLab rarely gets it right, so it's fixed after the remap with `tools/recolour.py` (recipe in ASSET_MANIFEST §5). It's her alone, makes her findable on green and brown screens, and echoes the cold half of the palette.
- **Weapon:** a plain wooden **walking stick**.

### 4.2 Hard rules

- ❌ No green tunic, no pointed hood or cap, no sword, no shield. She must never read as a cosplay of an existing game hero.
- ❌ No elements taken from any existing character. Reference images inform mood only.
- ✅ She should read as **her own character** at a glance.

### 4.3 Proportions 🔬

- **Variant A:** natural proportions (about 6 heads). The risk is that her head is only 6–7px.
- **Variant B:** semi-natural (about 4 heads). Still clearly a real girl, not chibi.
- Both get generated in Phase 0 and judged in the mock. **Winner: Variant A** (`chr_awa_a` opt5: `stylized` preset, `size: 40`), chosen by Tom on 2026-09-25.
- Round 1 (`size: 64`, custom proportions): figures came out ~2 tiles tall, and A and B looked the same. Round 2 uses `size: 40` with the `stylized` preset for A and `cartoon` for B.

### 4.4 Base prompt (Phase 0)

```
12 year old girl explorer, long straight ginger hair loosely tied, knee-length oatmeal and rust tunic,
faded blue scarf, small leather satchel on a strap across body, leggings, sturdy brown boots,
holding a plain wooden walking stick, curious expression, [natural proportions | slightly stylised ~4 heads tall],
cosy English countryside, soft storybook pixel art, muted warm natural colours, gentle light
```

---

## 5. Environments

### 5.1 Meadow village (Biome 1)

A small English hamlet, deliberately **smaller in scale** than a real village. Stone cottages, timber framing, slate roofs, split-rail fences, barrels, log piles, birch and oak trees, and worn dirt paths through warm olive and yellow-green grass. It should feel lived-in, soft and golden-afternoon.

- **Grass:** olive `a2a947` with pale `cddf6c` flecks, scattered with fill variants (see the manifest).
- **Rivers:** teal water `0b8a8f` with pale ripples. The tile ripples are horizontal, so **rivers run mostly east–west** with gentle bends. Flow and motion come from a Godot scroll shader, which stops when an area is drained (§8.1). Soften stepped diagonal banks with reeds, stones or bridges.

### 5.2 Old woodland (Biome 2)

Tall straight trunks, hazy **golden shafts of light**, dark leaf-litter floor, heavily shadowed edges. Cathedral-like: beautiful, but you feel small.

### 5.3 Abandonment layer (everywhere)

Roofless stone cottages, moss-covered walls and trunks, ivy, ferns, leaf litter. People left and nature quietly moved in. It's **alive and green**, never grey.

- **Ruins are built from crumbled wall pieces only** (uneven tops, stepped broken ends, ivy), softened with ferns, bushes and scattered stones. **No straight, angular or modular walls** (the building-kit look was rejected). Ruins are baked or placed as objects over the meadow, with grass showing through inside.

### 5.4 Other biomes

Lakes and wetlands, highland ruins, and coast and cliffs will be defined after Phase 0, using the same rules.

---

## 6. Colour

### 6.1 Palette 🔬

- **Test palette:** Resurrect 64 (Lospec). The file lives at `tools/palettes/resurrect-64.hex`.
- **Fallback:** a custom 40–48-colour palette built from the approved Phase 0 assets, split deliberately into a **warm half** (golden, olive, ochre, rust, ginger) and a **cold half** (blue, teal, grey fog).
- Compare them side by side in Phase 0. **Winner:** _TBD_.
- **Every asset** is remapped to the winning palette. No exceptions.

### 6.2 Colour language

| Meaning | Colour |
|---|---|
| **Alive / cosy** | Warm golden light, olive and yellow-green, ochre, warm wood |
| **Drained** | Cold blue-grey and teal, desaturated, still |
| **Awa** | Ginger hair plus a blue scarf. Always the most readable thing on screen. |
| **The world's creatures** | A shared pale glow or white "eye" signature |

---

## 7. Enemies (visual)

- Made from **each biome's own materials**: moss and petals, bark, stone, water.
- **Shared signature** across all enemies, such as a soft pale glow or a single white eye. 🔬 Settled on the first enemy.
- Meadow enemies are almost cute. Towards the source they get larger, colder and stranger.
- Never gory. Never horror.

---

## 8. Lighting and atmosphere (Godot side)

- **Authored per area**, with no real-time day/night cycle.
  - Village: golden afternoon.
  - Woodland: hazy and golden, with dark edges.
  - Drained areas: dusk-blue.
- **Godot 2D lights** for the lantern, windows and shrines. **Fog overlays**, soft **god-ray** shaders, and a darkness tint per area.
- **No normal maps.** PixelLab doesn't produce them, and we accept flat-lit sprites.
- **The lantern's warm light pool** in dark places is a key mood tool.

### 8.1 The drain shader

- A colour shift from warm towards cold blue-grey, with desaturation.
- **Stops movement**: no swaying grass, still water.
- One tileset serves both the healthy and drained states. **Don't generate separate drained tilesets.**

### 8.2 Tone ceiling

The eeriest areas may approach cold, lonely dread. **Never** jump scares, gore or chase horror. It should be unsettling, not frightening.

---

## 9. UI

- **Health:** small leaves on a sprig (top-left) that wilt when Awa takes hits.
- **Current item:** bottom-right.
- **The diary:** the UI hub. Its handwriting style must be identical for old and new entries.
- Detailed UI art is defined in Phase 1+.

---

## 10. Reference images

- Kept in `art/reference/` **for mood only**, and gitignored.
- **Never** pass them to PixelLab as input, and never copy them.
- Current set: a character mood reference for Awa, an English village top-down mood reference, an overgrown ruined cottage, a hazy golden forest, and a cold foggy lighting reference.

---

## 11. Change log

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-09-24 | Initial provisional bible from the planning session |
| 0.2 | 2026-09-25 | Tilesets use `high top-down`; added §3.0 tool choice per asset class; verified the parameter enums against the PixelLab MCP |
| 0.3 | 2026-09-25 | §2.1: `size` is the figure height, not the canvas; Awa `size` 40. §4.4: satchel wording. Round 2 proportion test |
| 0.4 | 2026-09-25 | §4.3: Variant A wins (opt5). §4.1: scarf colour fixed with `tools/recolour.py` |
| 0.5 | 2026-09-25 | §3.0: ground fill exception (low detail, fill variants) |
| 0.6 | 2026-09-25 | §5.1: approved meadow grass and river colours; rivers run east–west |
| 0.7 | 2026-09-25 | §5.3: ruins from crumbled pieces only, no angular walls |
