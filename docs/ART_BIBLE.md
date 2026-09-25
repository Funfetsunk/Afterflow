# Afterflow — Art Bible

> **Status:** v0.18, provisional. **Direction reset on 2026-09-25** (see §0). Becomes **v1.0** when Phase 0 is approved. Items marked 🔬 are decided by the Phase 0 tests.
> **Rule:** every asset request follows this document. If an asset needs to break a rule, update this document first.

---

## 0. Direction reset (v0.8)

Tom reviewed the first village mock (v0.7 assets): everything was going to look the same and **it didn't hang together**. The target is now the look and feel of **16-bit SNES-era top-down action-adventures** (Tom's touchstone: *A Link to the Past*). Everything is rebuilt in this style, **Awa included**.

- The v0.1–v0.7 assets are **superseded**, not deleted. They stay in `art/` and the manifest for reference.
- **Never** name Zelda (or any other game) in prompts, **never** pass Nintendo or other games' art to PixelLab, and never copy existing tiles or characters. We are after the *style* of the era, not its assets. Awa stays her own character (§4.2).
- **North star locked by Tom on 2026-09-25:** `art/final/north_star/ns_meadow_village_r2_mix.png` (opt4's layout in opt6's colours; recipe in the manifest). It is the style reference for everything that follows.
- Kept from v0.7: Awa's design, the colour language (§6.2: olive meadow, teal water, pale-glow creatures, cold drain), the drain concept, the tone, the tools and the workflow.

---

## 1. Look in one sentence

A small English countryside in **bold, readable 16-bit top-down pixel art**, **warm and golden where the world is alive** and **cold blue-grey and still where it has been drained**, with gentle overgrowth over the ruins of past lives.

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
| Character sprite directions | **4** (south, west, east, north) |
| Movement | 8-way analog (sprites don't need diagonals) |
| Pixel density | Uniform. No scaled-up or scaled-down sprites in-game. |
| **Everything is tiles** | **All environment art lives on the 16px grid as tiles** (Tom, 2026-09-25). Only characters, enemies and items are free-moving sprites. Three kinds: **terrain autotiles** (grass, path, river, forest canopy, hedges: paint any shape), **modular kits** (cottage walls/roofs, fences, crumbled ruin walls, cliffs: any length or footprint), **fixed tile stamps** (a single tree, standing stone, shrine: placed as a block of tiles, per-tile collision in Godot). |

### 2.1 Sizes 🔬

| Asset class | Target on screen |
|---|---|
| Awa, NPCs | **~24–28px** tall (about 1.5–1.75 tiles) |
| Standard enemies | ~16–24px |
| Large enemies / bosses | 32–64px |
| Buildings | Painted from 16px tiles, typically 4–6 tiles wide |
| Props (bushes, rocks, pots, signs) | 16×16, some 32×32 |

In `create_character` standard mode `size` sets roughly the **figure height**, not the canvas (measured in v0.3).

---

## 3. PixelLab parameters (locked 2026-09-25)

Taken from the north star, which was made with `create_image_pixflux`, `high top-down`, `single color black outline`, `basic shading`, `low detail`, seed 4.

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
- Lessons from v0.x still apply: `create_1_direction_object` has no style settings; PixelLab building kits don't produce usable roofs at our camera (§5); prompts for L-shaped or north–south walls come back as neat geometry.

### 3.1 Prompt template

```
[SUBJECT] + [SUBJECT DETAILS] + [STYLE SUFFIX]
```

**Style suffix (use verbatim):**
```
cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
```

Record every final prompt in ASSET_MANIFEST.md. Never put a game or franchise name in a prompt.

### 3.2 Workflow: north star first, then style lock

1. **North-star screen.** Generate complete single-screen scenes (320×180) of the meadow village until Tom approves one as "that's Afterflow". Scenes are cheap (`create_image_pixflux` / `create_image_pixen`, 1 generation each).
2. **Style lock.** The approved north star becomes the **style reference** for every later asset, wherever a PixelLab tool accepts a style image. Where a tool doesn't, match its prompt and parameters to the north star, and judge the result inside a mock next to it.
3. **Build from tiles.** Terrain, cliffs, fences and **buildings** are 16px tiles painted into the map; variety comes from arrangement and small repeated props, not from unique one-off art.
4. Generate **3–4 variants** per asset, remap to the palette (§6), and judge them **in a 320×180 mock**, never in isolation.
5. Style references must be **approved `art/final/` assets or the approved north star**, never outside images.

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

- **Approved 2026-09-25:** `chr_awa` opt2 (`create_character` standard, `size: 28`, `default` preset, locked §3 parameters): a 24–27px figure. Hair is repainted with `tools/hair_ramp.py` (ramp `e6904e`/`cd683d`/`9e4539`) on **every** frame.
- Hair, scarf and stick must read at a glance at this size: the ginger hair and blue scarf are her silhouette.
- ⚠️ **Colour integrity (Tom, 2026-09-25):** her hair must be a **clean ginger ramp** with no stray off-tone pixels. Every recolour or palette pass must **leave Awa untouched** (or exclude her pixels), and every new Awa frame is checked for hair and skin discolouration before review.

### 4.4 Base prompt

```
12 year old girl explorer, long straight ginger hair loosely tied, knee-length oatmeal and rust tunic,
faded blue scarf, small leather satchel on a strap across body, leggings, sturdy brown boots,
holding a plain wooden walking stick, curious expression,
cosy English countryside, 16-bit SNES-era top-down adventure pixel art, bold dark outlines, limited palette, light from the top left
```

---

## 5. Environments

### 5.1 Meadow village (Biome 1)

A small English hamlet, deliberately **smaller in scale** than a real village. Stone cottages, timber framing, slate roofs, split-rail fences, barrels, log piles, birch and oak trees, and worn dirt paths through warm olive and yellow-green grass. It should feel lived-in, cosy and golden-afternoon. **Buildings are painted from the 16px cottage kit** (`ts_cottage16`: roof nine-slice layer + 2-row wall layer with windows and door, chimney stamps, cast-shadow column; `tools/paint_cottage16.py`), so every house can have its own footprint. The **gable-end cottage** (`ts_gable16`, stamps `gable_d0..d2`, 3 roof depths) adds the north star's second house type, and the **lane crossing** (`ts_ford16`, stamp `ford`) runs a lane on through the river ledge. The approved village mock (`art/mocks/v2_village_full_6x.png`, built by `tools/mock_layouts/build_v2_village_full.sh`) matches the north star's composition. Houses must stay **grounded**: grass tufts over the wall base and a cast shadow on the grass to the right, with variety from arrangement and props: fences, bushes, flowers, pots, signs, log piles.

- **Grass (v0.x, superseded):** olive `a2a947` with pale `cddf6c` flecks. Keep the olive family.
- **Terrain (16px, approved 2026-09-25):** grass `547e64` with sparse dark tufts cut from the north star; brown path `966c6c` with pale specks; rivers in `4d65b4` with a pale broken foam line under a dark earth **ledge** about 1.2 tiles tall. **Rivers run straight east–west** for now, ending at map edges or bridges, until bend tiles match the ledge height. Recipes are in the manifest.

### 5.2 Old woodland (Biome 2)

Tall straight trunks, hazy **golden shafts of light**, dark leaf-litter floor, heavily shadowed edges. Cathedral-like: beautiful, but you feel small.

### 5.3 Abandonment layer (everywhere)

Roofless stone cottages, moss-covered walls and trunks, ivy, ferns, leaf litter. People left and nature quietly moved in. It's **alive and green**, never grey.

- **Ruin kit (approved 2026-09-25):** `ts_ruin16`, the cottages' own stone broken down: stone-sized broken tops with a pale cap and outline, moss and ivy, weathered darker lower courses, rubble stamps at the foot. East–west runs, painted with `tools/paint_tiles.py ... ruin`.
- **Ruins are built from crumbled wall pieces only** (uneven tops, stepped broken ends, ivy), softened with ferns, bushes and scattered stones. **No straight, angular or modular walls** (the building-kit look was rejected). Ruins are baked or placed as objects over the meadow, with grass showing through inside. (v0.x rule; re-check once the 16-bit style is locked.)

### 5.3a Shrines

- **Shrine (approved 2026-09-25):** `shrine_monolith`, a 2×3 tile stamp drawn by `tools/kits/make_shrine16.py`. Shrines are the world's mind keeping Awa alive (GDD), so they look **ancient-future**: too clean and too advanced for the countryside, with moss taking them back. A dark slate obelisk (`7f708a`/`625565`/`3e3546`) with a bevelled top, a glowing seam and round core, on a two-tier pale plinth (`c7dcd0`/`9babb2`/`7f708a`) with a glowing groove.
- **Machine glow is pale cyan** (`ffffff`/`8fd3ff`/`4d9be6`), apart from the creatures' pale glow. In Godot a 2D light adds the real glow.

### 5.4 Other biomes

Lakes and wetlands, highland ruins, and coast and cliffs will be defined after Phase 0, using the same rules.

---

## 6. Colour

### 6.1 Palette 🔬

- **Afterflow v1 palette (locked 2026-09-25):** the north star's 28 colours plus two skin tones (`fca790`, `fdcbb0`), 30 colours in all, every one a Resurrect 64 colour. File: `tools/palettes/afterflow-v1.hex`.
- **Every asset** is remapped to it: `python tools/palette_remap.py <in> <out> --palette tools/palettes/afterflow-v1.hex`. New colours are added only with Tom's approval, and only from Resurrect 64.
- Resurrect 64 (`tools/palettes/resurrect-64.hex`) stays as the superset; the custom warm/cold palette comparison is no longer needed.

### 6.2 Colour language

| Meaning | Colour |
|---|---|
| **Alive / cosy** | Deep muted meadow greens (`547e64`, `374e4a`), soft brown paths (`966c6c`), warm pale stone (`ab947a`), plum-grey slate (`625565`, `3e3546`), blue water (`4d65b4`, `8fd3ff`) |
| **Drained** | Cold blue-grey and teal, desaturated, still |
| **Awa** | Ginger hair plus a blue scarf. Always the most readable thing on screen. |
| **The world's creatures** | One large white eye with a dark pupil (§7) |

---

## 7. Enemies (visual)

- Made from **each biome's own materials**: moss and petals, bark, stone, water.
- **Shared signature (settled 2026-09-25):** every creature has **one large white eye** (`ffffff`, `c7dcd0` rim) with a small dark pupil, and it is always the brightest thing on the creature, drained or not. Set by `enm_meadow01`, the mossling (olive moss ball, sprout, one petal), drawn by `tools/kits/make_creature16.py`. Creature bodies must contrast with the ground they stand on.
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
| 0.8 | 2026-09-25 | **Direction reset:** 16-bit SNES-era top-down style (§0); 320×180 with 16px tiles; one camera, dark outlines, top-left light; new style suffix; north-star-first workflow and style lock; buildings painted from tiles; rebuild everything including Awa |
| 0.9 | 2026-09-25 | **North star locked** (§0); §3 parameters locked from it; §6.1 Afterflow v1 palette (30 colours from Resurrect 64); §6.2 alive colours; §4.3 Awa colour-integrity rule |
| 0.10 | 2026-09-25 | §5.1: approved 16px terrain (grass, path, river ledge); rivers straight east–west for now |
| 0.11 | 2026-09-25 | §4.3: 16-bit Awa approved; hair_ramp on every frame |
| 0.12 | 2026-09-25 | §5.1: buildings assembled from north-star slices (cottage kit approved) |
| 0.13 | 2026-09-25 | §2: everything environmental is 16px tiles (autotiles, modular kits, fixed stamps) |
| 0.14 | 2026-09-25 | §5.1: 16px cottage kit approved (separate roof/wall layers); grounding rule (tufted base, cast shadow) |
| 0.15 | 2026-09-25 | §5.3: ruin kit approved (weathered courses, rubble) |
| 0.16 | 2026-09-25 | §5.3a: shrine approved (ancient-future monolith, pale cyan machine glow) |
| 0.17 | 2026-09-25 | §7: enemy signature settled (one large white eye with a pupil); meadow mossling approved |
| 0.18 | 2026-09-25 | §5.1: gable-end cottage stamps and lane-through-ledge crossing approved; full village mock approved against the north star |
