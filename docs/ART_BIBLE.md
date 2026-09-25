# Afterflow — Art Bible

> **Status:** v1.0, **awaiting Tom's sign-off** (Phase 0 exit). Once signed off, the rules below are locked for Phase 1; changing one means updating this document first.
> **Rule:** every asset request follows this document. If an asset needs to break a rule, update this document first.

---

## 0. Direction

The target is the look and feel of **16-bit SNES-era top-down action-adventures** (Tom's touchstone: *A Link to the Past*). This replaced the v0.1–v0.7 direction on 2026-09-25, when Tom found the first village mock didn't hang together; everything, Awa included, was rebuilt.

- The v0.x assets are **superseded**. Their record is in `docs/archive/ASSET_MANIFEST_v0.md`.
- **Never** name Zelda (or any other game) in prompts, **never** pass Nintendo or other games' art to PixelLab, and never copy existing tiles or characters. We are after the *style* of the era, not its assets. Awa stays her own character (§4.2).
- **North star (locked 2026-09-25):** `art/final/north_star/ns_meadow_village_r2_mix.png`. It is the style reference for everything. The approved village mock `art/mocks/v2_village_full_6x.png` rebuilds it from the tile kits (side by side: `art/mocks/review_v2_village_vs_north_star.png`), which proves the kits reach it.

---

## 1. Look in one sentence

A small English countryside in **bold, readable 16-bit top-down pixel art**, **warm where the world is alive** and **cold blue-grey and still where it has been drained**, with gentle overgrowth over the ruins of past lives, and a few things that are quietly too clean and too advanced to belong.

---

## 2. Technical grid (locked)

| Setting | Value |
|---|---|
| Internal resolution | **320×180** (integer scale ×6 to 1920×1080) |
| Tile size | **16×16** |
| Screen in tiles | 20 × 11.25 |
| Camera | **One camera for everything:** ground straight top-down; walls, fronts and characters face the viewer; roofs seen from above. **No angled or isometric objects.** |
| Outlines | **Dark outlines on everything** (characters, objects, buildings, terrain edges), in the palette's darkest colour `2e222f` |
| Shading | Simple 2–3 tones per material, **light from the top left**, on every asset |
| Character sprite directions | **4** (south, east, north, west) |
| Movement | 8-way analog (sprites don't need diagonals) |
| Pixel density | Uniform. No scaled-up or scaled-down sprites in-game. |
| **Everything is tiles** | **All environment art lives on the 16px grid as tiles.** Only characters, enemies and items are free-moving sprites. Three kinds: **terrain autotiles** (grass, path, river: paint any shape), **modular kits** (cottage walls/roofs, fences, crumbled ruin walls, woodland: any length or footprint), **fixed tile stamps** (a tree, bush, standing stone, shrine, gable cottage, lane crossing: placed as a block of tiles, per-tile collision in Godot). |

### 2.1 Sizes (settled)

| Asset class | On screen |
|---|---|
| Awa, NPCs | **24–28px** figures in 40×40 frames (`create_character` standard, `size: 28`) |
| Meadow enemies | ~17×19px body in a 24×24 frame; larger and stranger towards the source |
| Large enemies / bosses | 32–64px |
| Cottages | Painted from the kit, 4–8 tiles wide, roof 2–3 rows + 2-row wall; gable cottage 4 tiles wide, 5–7 tall |
| Props | Stamps of 1×1 (flowers, rubble) to 3×3 (oaks); shrine 2×3 |

In `create_character` standard mode `size` sets roughly the **figure height**, not the canvas.

### 2.2 Grounding (every object)

Nothing may look pasted on (Tom). Every building, prop and character is **grounded**:

- **Grass tufts over the base** (walls keep the north star's tufted base rows).
- A **cast shadow on the grass down and to the right** in `374e4a` (a column beside buildings, an offset silhouette under props, a soft ellipse under creatures).

---

## 3. How assets are made

### 3.1 Choose the method

Phase 0 showed that PixelLab is best at people and whole scenes, and weakest at small or unusual objects at our camera. Pick in this order:

1. **Cut from the north star** when the north star already shows the thing (terrain edges, cottages, gable cottage, lane crossing, bushes, fences). `tools/cut_prop.py` and the `tools/kits/make_*.py` scripts do this reproducibly. This is the most cohesive option.
2. **Generate with PixelLab** for characters (`create_character` standard) and for anything the north star doesn't show, with the north star as the style image wherever the tool accepts one (`color_image_url` for `create_image_pixflux`).
3. **Draw in code** (a `tools/kits/make_*.py` script, palette colours only, same outline/shading rules) when PixelLab results come back muddy, washed out or without outlines. This is how the shrine and the meadow creature were made. The script is the recipe: re-run it to rebuild the asset.

Whatever the method, remap to the palette (§6), check it **in a 320×180 mock** next to Awa, never in isolation, and log it in the manifest.

### 3.2 PixelLab parameters (locked)

Taken from the north star (`create_image_pixflux`, seed 4).

| Parameter | Value |
|---|---|
| Camera / view | `high top-down` (tilesets too) |
| Outline | `single color black outline` where offered, otherwise `single color outline` |
| Shading | `basic shading` |
| Detail | `low detail` |
| Directions | `4` |
| Tileset tile size | `16` |

- Only **standard** mode of `create_character` honours all the parameters. `v3` and `pro` need Tom's approval (8 directions, 20–40 generations for `pro`).
- **Always pass every parameter explicitly**; tool defaults differ.
- `create_image_pixflux` has a **32×32 minimum** canvas; ask for a small subject "in the middle of the frame" for anything smaller.
- Known weak spots: `create_1_direction_object` has no style settings; PixelLab building kits don't produce usable roofs at our camera; its forest tilesets can't draw crowns (the woodland is baked from tree stamps); L-shaped or north–south wall prompts come back as neat geometry.

### 3.3 Prompt template

```
[SUBJECT] + [SUBJECT DETAILS] + [STYLE SUFFIX]
```

**Style suffix (use verbatim):**
```
cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
```

Record every final prompt in ASSET_MANIFEST.md. Never put a game or franchise name in a prompt. Generate **3–4 variants** per asset.

---

## 4. Awa

### 4.1 Description

- About 12 years old, with **long, straight ginger hair**, loose or loosely tied.
- Inquisitive and capable: **an explorer, not a warrior.**
- **Outfit:** knee-length tunic in **oatmeal and rust** tones, leggings, sturdy brown boots, and a brown leather **satchel** worn across the body (the diary lives here).
- **Signature accent:** a **faded blue scarf**. It's hers alone and makes her findable on green and brown screens.
- **Weapon:** a plain wooden **walking stick**.

### 4.2 Hard rules

- ❌ No green tunic, no pointed hood or cap, no sword, no shield. She must never read as a cosplay of an existing game hero.
- ❌ No elements taken from any existing character. Reference images inform mood only.
- ✅ She should read as **her own character** at a glance.

### 4.3 Approved sprite and colour integrity

- **Approved 2026-09-25:** `chr_awa` (`art/final/chr_awa_{s,e,n,w}.png`), `create_character` standard, `size: 28`, `default` preset, §3.2 parameters: a 24–27px figure.
- Hair is repainted with `tools/hair_ramp.py` (ramp `e6904e`/`cd683d`/`9e4539`) on **every** frame, including every future animation frame.
- ⚠️ **Colour integrity (Tom):** her hair must be a **clean ginger ramp** with no stray off-tone pixels. Every recolour, palette pass or shader must **leave Awa untouched**, including the drain (§8.1). Check every new Awa frame for hair and skin discolouration before review.

### 4.4 Base prompt

```
12 year old girl explorer, long straight ginger hair loosely tied, knee-length oatmeal and rust tunic,
faded blue scarf, small leather satchel on a strap across body, leggings, sturdy brown boots,
holding a plain wooden walking stick, curious expression,
cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
```

### 4.5 Other people

NPCs follow Awa's recipe (`create_character` standard, `size: 28`, 4 directions) and must never share her signature colours (ginger hair, blue scarf). Approved: **the miller** (`npc_villager01`: flat cap, grey beard, long pale apron).

---

## 5. Environments

### 5.1 Meadow village (Biome 1)

A small English hamlet, deliberately **smaller in scale** than a real village. Stone cottages, timber framing, slate roofs, split-rail fences, oaks and birches, and worn dirt lanes through meadow grass. Lived-in and cosy.

- **Terrain (approved):** grass `547e64` with sparse dark tufts cut from the north star, 8 fill variants; brown lanes `966c6c` with pale specks, **1 tile wide** with fringed grass edges; river `4d65b4` with a pale broken foam line under a dark earth **ledge** about 1.2 tiles tall. **Rivers run straight east–west** (bend tiles don't match the ledge height yet). The **lane crossing** stamp (`ford`) runs a lane on through the ledge to the water.
- **Cottages (approved):** painted from the 16px kit (`ts_cottage16`: roof nine-slice layer of any depth + 2-row wall layer with windows and door, chimney stamps, cast-shadow column; `tools/paint_cottage16.py`), so every house has its own footprint. The **gable-end cottage** stamps (`gable_d0..d2`) add the north star's second house type.
- **Fences, bushes, flowers, standing stones (approved):** stamps and kits cut from the north star. **Trees** (two oaks, a birch) are PixelLab generations with the north star as the forced palette, their ground patches turned into `374e4a` shadows. **Woodland** is baked from the tree stamps into one tile layer (`tools/paint_forest.py`), with enclosed gaps shaded `313638`.
- **Composition (from the north star):** a row of oaks running off the top edge behind the roofs, cottages with a grass strip along their walls, lanes meeting at right angles, a grass band with props above the river ledge. Little empty grass.

### 5.2 Old woodland (Biome 2)

Tall straight trunks, hazy **golden shafts of light**, dark leaf-litter floor, heavily shadowed edges. Cathedral-like: beautiful, but you feel small. Defined in Phase 1+ with the same rules.

### 5.3 Abandonment layer (everywhere)

Roofless stone cottages, moss-covered walls, ivy, ferns. People left and nature quietly moved in. It's **alive and green**, never grey.

- **Ruin kit (approved):** `ts_ruin16`, the cottages' own stone broken down: stone-sized broken tops with a pale cap and outline, moss and ivy, weathered darker lower courses, rubble stamps at the foot. East–west runs, painted with `tools/paint_tiles.py ... ruin`.
- **Crumbled pieces only:** uneven tops, stepped broken ends, no straight, angular or modular-looking walls.

### 5.4 Shrines

- **Shrine (approved):** `shrine_monolith`, a 2×3 stamp drawn by `tools/kits/make_shrine16.py`. Shrines are the world's mind keeping Awa alive (GDD), so they look **ancient-future**: too clean and too advanced for the countryside, with moss taking them back. A dark slate obelisk (`7f708a`/`625565`/`3e3546`) with a bevelled top, a glowing seam and round core, on a two-tier pale plinth (`c7dcd0`/`9babb2`/`7f708a`) with a glowing groove.
- **Machine glow is pale cyan** (`ffffff`/`8fd3ff`/`4d9be6`). In Godot a 2D light adds the real glow.

### 5.5 Other biomes

Lakes and wetlands, highland ruins, and coast and cliffs are defined in Phase 1+, using the same rules.

---

## 6. Colour

### 6.1 Palette (locked)

- **Afterflow v1 palette:** the north star's 28 colours plus two skin tones (`fca790`, `fdcbb0`), 30 colours in all, every one a Resurrect 64 colour. File: `tools/palettes/afterflow-v1.hex`.
- **Every asset** is remapped to it: `python tools/palette_remap.py <in> <out> --palette tools/palettes/afterflow-v1.hex`. New colours are added only with Tom's approval, and only from Resurrect 64 (`tools/palettes/resurrect-64.hex`).

### 6.2 Colour language

| Meaning | Colour |
|---|---|
| **Alive / cosy** | Muted meadow greens (`547e64`, `374e4a`), soft brown lanes (`966c6c`), warm pale stone (`ab947a`), plum-grey slate (`625565`, `3e3546`), blue water (`4d65b4`, `8fd3ff`) |
| **Drained** | Cold blue-grey and teal, desaturated, still |
| **Awa** | Ginger hair plus a blue scarf. Always the most readable thing on screen. |
| **The world's mind** (shrines, old mechanisms) | Pale cyan glow (`8fd3ff`) on dark slate and pale machined stone |
| **The world's body** (creatures) | One large white eye with a dark pupil (§7) |
| **Cast shadows** | `374e4a` on grass |

---

## 7. Enemies (visual)

- Made from **each biome's own materials**: moss and petals, bark, stone, water.
- **Shared signature (settled):** every creature has **one large white eye** (`ffffff`, `c7dcd0` rim) with a small dark pupil, and it is always the brightest thing on the creature, drained or not.
- **Meadow creature (approved):** `enm_meadow01`, the mossling (olive `676633` moss ball with `374e4a` shade, a two-leaf sprout, one pale petal, stubby feet), drawn by `tools/kits/make_creature16.py`.
- Creature bodies must **contrast with the ground** they stand on (the mossling is olive, not grass green).
- Meadow enemies are almost cute. Towards the source they get larger, colder and stranger.
- Never gory. Never horror.

---

## 8. Lighting and atmosphere (Godot side)

- **Authored per area**, with no real-time day/night cycle.
  - Village: warm afternoon.
  - Woodland: hazy and golden, with dark edges.
  - Drained areas: dusk-blue.
- **Godot 2D lights** for the lantern, windows and shrines. **Fog overlays**, soft **god-ray** shaders, and a darkness tint per area.
- **No normal maps.** We accept flat-lit sprites.
- **The lantern's warm light pool** in dark places is a key mood tool.

### 8.1 The drain shader

- A colour shift from warm towards cold blue-grey, with desaturation (preview: `tools/compose_mock.py --drain`).
- **Awa is excluded** (mocks use `nodrain`); creature eyes and shrine glows stay the brightest things on screen.
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

---

## 11. Phase 0 approved set (for Phase 1 import)

Everything below is `approved` in ASSET_MANIFEST.md; Phase 1 copies it into `assets/` for Godot.

| Group | Assets |
|---|---|
| Terrain | grass fill variants, grass-path, grass-water (river), north-star ledge pairs, `ford` |
| Buildings | `ts_cottage16` kit, `gable_d0..d2` |
| Kits | `ts_fence16`, `ts_ruin16` (+ rubble stamps), `ts_forest16` library |
| Stamps | oaks, birch, bushes, flowers, standing stone, rubble, `shrine_monolith` |
| Characters | Awa (`chr_awa_{s,e,n,w}`), the miller (`npc_villager01_{s,e,n,w}`) |
| Enemies | mossling (`enm_meadow01_{s,e,n,w}`) |
| Reference mocks | `v2_village_full_6x.png` and its drained version |

Still to do in Phase 1+: walk/idle animations (Awa's hair ramp on every frame), river bends at ledge height, a door for the gable cottage's side, UI art, other biomes.

---

## 12. Change log

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-09-24 | Initial provisional bible from the planning session |
| 0.2–0.7 | 2026-09-25 | v0.x direction (480×270, 32px): parameters, Awa variant A, meadow and river colours, crumbled ruins |
| 0.8 | 2026-09-25 | **Direction reset:** 16-bit SNES-era top-down style; 320×180 with 16px tiles; one camera, dark outlines, top-left light; new style suffix; north-star-first workflow; rebuild everything including Awa |
| 0.9 | 2026-09-25 | North star locked; parameters locked from it; Afterflow v1 palette; Awa colour-integrity rule |
| 0.10–0.15 | 2026-09-25 | 16px terrain, Awa, everything-is-tiles, cottage kit and grounding rule, ruin kit approved |
| 0.16 | 2026-09-25 | Shrine approved (ancient-future monolith, pale cyan machine glow) |
| 0.17 | 2026-09-25 | Enemy signature settled (one large white eye with a pupil); meadow mossling approved |
| 0.18 | 2026-09-25 | Gable-end cottage and lane crossing approved; full village mock approved against the north star |
| **1.0** | 2026-09-25 | **Phase 0 consolidation for sign-off:** sizes settled (§2.1), grounding rule (§2.2), method order cut / generate / draw in code (§3.1), NPC rule (§4.5), colour roles for the world's mind and body (§6.2), drain excludes Awa (§8.1), approved set for Phase 1 (§11); superseded v0.x notes removed |
