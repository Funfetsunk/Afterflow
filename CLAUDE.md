# CLAUDE.md — Afterflow

Instructions for Claude Code working in this repository. Read this file fully at the start of every session.

---

## 1. Project at a glance

- **Afterflow**: a 2D top-down Zelda-like, exploration and mystery first, polished Zelda-style combat.
- **Engine:** Godot **4.7.2-stable**. Latest stable at project creation. **Never upgrade** without Tom's explicit approval.
- **Language:** GDScript. Game data lives in `.tres` resources that can be edited in the Inspector.
- **Platform:** Windows desktop first, gamepad-first (keyboard supported).
- **Repo:** https://github.com/Funfetsunk/Afterflow
- **Local path:** `C:\Users\evans\Documents\afterflow`
- **MCPs:** Godot MCP Pro (editor control) and PixelLab MCP (art generation).

## 1a. Godot MCP Pro instructions (imported)

@docs/GODOT_MCP.md

> **Precedence:** if anything in `docs/GODOT_MCP.md` conflicts with this file, **this file wins**. In particular:
> - The Phase 0 no-code rule (§3) overrides its "Building a scene from scratch" workflow.
> - This is a **2D project**. Ignore the 3D tools (`add_mesh_instance`, `setup_camera_3d`, `add_gridmap`, etc.).
> - Prefer MCP tools. Use the CLI mode only as a fallback when the MCP tools aren't loaded.
> - `docs/GODOT_MCP.md` is vendor-supplied. Don't edit it; replace it wholesale when Godot MCP Pro updates.

## 2. Required reading

| Doc | When |
|---|---|
| `docs/GDD.md` | Any gameplay, story or level work |
| `docs/ART_BIBLE.md` | **Any** art generation or visual work |
| `docs/ASSET_MANIFEST.md` | Before and after **every** PixelLab generation |

If a request conflicts with these documents, **stop and ask Tom**. Don't silently deviate. When a design decision changes, update the relevant document in the same commit.

---

## 3. Current phase: PHASE 0 — LOOK DEVELOPMENT

> **2026-09-25: direction reset.** The target is now a 16-bit SNES-era top-down look at 320×180 with 16px tiles (Art Bible §0). All v0.x assets are superseded and everything, Awa included, is rebuilt. The north star is **locked** (`art/final/north_star/ns_meadow_village_r2_mix.png`), and so is the Afterflow v1 palette (`tools/palettes/afterflow-v1.hex`): remap every asset to it, and never let a recolour touch Awa (Art Bible §4.3).

> ⛔ **HARD RULE: no game code, scenes or gameplay scripts until Tom approves Art Bible v1.0.**

Allowed in Phase 0:
- PixelLab generation of the sample set (ASSET_MANIFEST §4)
- Python tools in `tools/` (palette remap, mock composer)
- Updating the documents

Not allowed in Phase 0:
- Godot scenes, nodes, GDScript gameplay, tilemaps, project-setting experiments

Phase exit: Tom approves the mocks, and the Art Bible reaches v1.0 with proportions, palette and enemy signature settled. Then update this section to Phase 1.

---

## 4. Repository layout

```
afterflow/
├── CLAUDE.md
├── CREDITS.md              # every sound, font and third-party asset: source, author, licence
├── project.godot
├── docs/
│   ├── GDD.md
│   ├── ART_BIBLE.md
│   └── ASSET_MANIFEST.md
├── art/                    # contains .gdignore, so Godot does NOT import this folder
│   ├── reference/          # mood references, gitignored, NEVER sent to PixelLab
│   ├── raw/                # untouched PixelLab downloads
│   ├── final/              # palette-remapped assets
│   └── mocks/              # 320×180 mock screenshots (v0.x mocks: 480×270)
├── tools/
│   ├── palettes/resurrect-64.hex
│   ├── palette_remap.py
│   ├── compose_mock.py
│   ├── recolour.py         # exact colour swaps (e.g. Awa's scarf)
│   ├── wang_layout.py      # Wang tileset + terrain map -> mock layout
│   ├── fill_variants.py    # flip/rotate a fill tile into 8 variants
│   ├── hair_ramp.py        # clean 3-tone hair ramp (Awa, Art Bible §4.3)
│   ├── paint_cottage16.py  # paint a 16px-kit cottage into a mock layout
│   ├── make_stamp.py       # prop sprite -> fixed 16px tile stamp
│   ├── paint_tiles.py      # paint stamps and fence runs into a mock layout
│   ├── paint_forest.py     # paint a woodland of any size as one tile layer
│   ├── build_cottage.py    # (superseded) slice-based cottages
│   ├── cut_prop.py         # cut a prop out of a scene (flood-fills the background)
│   ├── kits/               # slice kits (e.g. cottage_ns.json)
│   └── requirements.txt    # Pillow
└── assets/                 # Phase 1+: approved finals copied here for Godot to import
```

- `art/.gdignore` must exist (an empty file), so Godot doesn't import raw or working art.
- `.gitignore` must include `art/reference/`, `.godot/`, Python caches, and `addons/godot_mcp/`.
- `addons/godot_mcp/` is the paid Godot MCP Pro plugin and the repo is public, so it is **never committed**. On a fresh clone, copy it in from the Godot MCP Pro package, otherwise the editor reports missing autoloads.
- `.mcp.json` reads the PixelLab token from the `PIXELLAB_API_TOKEN` user environment variable. Never put the token in any file.

---

## 5. PixelLab workflow (every asset, every time)

1. **Check the manifest.** Add the asset as `planned` if it isn't already listed.
2. **Build the prompt** from the Art Bible §3.1 template: subject + details + the standard style suffix, **verbatim**.
3. **Use the parameters from Art Bible §3** (16-bit direction, 16px tiles, sizes from §2.1) and pass every parameter explicitly, because the tool defaults differ. Follow the north-star / style-lock workflow in Art Bible §3.2: once the north star is approved, use it as the style reference wherever a tool accepts one.
4. **Generate 3–4 variants.** Jobs are asynchronous (about 2–5 minutes), so poll with the matching `get_*` tool and don't resubmit duplicates.
5. **Download to `art/raw/`** using the manifest naming convention.
6. **Run the palette remap:** `python tools/palette_remap.py art/raw/<file> art/final/<file> --palette tools/palettes/afterflow-v1.hex`.
7. **Update the manifest:** IDs, exact prompt, variant count, credits used, status `review`.
8. **Show Tom** the remapped variants, ideally inside a mock (`tools/compose_mock.py`). Only Tom sets `approved`.

Rules:
- ❌ **Never** pass `art/reference/` images to PixelLab. Only approved `art/final/` assets may be used as style or reference inputs.
- ❌ Never recreate or imitate existing copyrighted characters, or other artists' work.
- ❌ Never overwrite an `approved` file. Version it (`_v2`).
- ❌ Don't generate separate "drained" tilesets. The drain is a shader (Art Bible §8.1).
- ✅ Log credits spent. Tom is on PixelLab **Tier 1 (Pixel Apprentice)**.

---

## 6. Tools (Phase 0, built)

Install the dependency with `python -m pip install -r tools/requirements.txt`. Each tool's usage is in its docstring.

- **`tools/palette_remap.py`**: maps every pixel to the nearest palette colour, preserves transparency, and takes a palette file argument, so switching palettes is a single re-run over `art/raw/`.
- **`tools/compose_mock.py`**: composes approved `art/final/` assets into an exact **320×180** image, exports it at both 1× and 6× (nearest-neighbour; `--legacy` uses the v0.x 480×270 / 32px setup, for layouts restored from git history), and has an optional **`--drain`** flag that simulates the drain (a shift towards cold blue-grey with desaturation).
- **`tools/recolour.py`**: swaps exact colours in `art/final/` sprites, for fixing one element PixelLab keeps getting wrong. Record every mapping in the manifest.
- **`tools/wang_layout.py`**: turns a PixelLab Wang tileset (sheet + metadata JSON) and a text terrain map into a `compose_mock.py` layout. It can scatter fill variants at random, to preview Godot's alternative tiles.
- **`tools/make_stamp.py`** / **`tools/paint_tiles.py`**: turn a prop into a fixed 16px tile stamp (registry `tools/kits/stamps.json`) and paint stamps, fence runs (`tools/kits/fence16.json`) or crumbled ruin runs (`tools/kits/ruin16.json`, built by `tools/kits/make_ruin16.py`) into a mock layout as grid cells. `tools/kits/make_shrine16.py` and `make_creature16.py` draw the shrine and the meadow creature in code; `make_gable16.py` and `make_ford16.py` cut the gable-end cottage and the lane-through-ledge crossing from the north star. `make_stamp.py --left` anchors a grid-aligned sprite bottom-left.
- **`tools/paint_forest.py`**: paints a woodland rectangle as one layer of 16px tiles, baked from the tree stamps (staggered lattice, back to front, enclosed gaps shaded); identical cells are reused from the shared library `art/final/tiles/forest16/`.
- **`tools/paint_cottage16.py`**: paints a cottage from the 16px kit (`tools/kits/cottage16.json`, built by `tools/kits/make_cottage16.py`) into a mock layout as grid cells: roof nine-slice of any depth, 2-row wall with l/m/r, windows and door, chimney stamps.
- **`tools/build_cottage.py`** (superseded by the 16px kit): assembles a cottage of any length from vertical slices cut from the north star (`tools/kits/cottage_ns.json`): pick the order of end, wall, window, door and chimney slices.
- **`tools/cut_prop.py`**: cuts a prop (bush, fence, stone, whole building) out of a scene onto transparency by flood-filling the background inwards from the crop edge; `--largest` drops detached scraps.
- **`tools/hair_ramp.py`**: repaints a character's hair as a clean light/base/dark ramp lit from the top left, touching only the hair connected to the top of the sprite. Run it on every Awa frame.
- **`tools/fill_variants.py`**: flips and rotates one seamless, non-directional fill tile into 8 variants.
- **`tools/mock_layouts/`**: JSON layouts for `compose_mock.py`. Terrain maps (`map_*.txt`) live here too.
- Python 3, Pillow. Keep the tools small, readable and documented.

---

## 7. Godot conventions (Phase 1+)

**Renderer:** `rendering/renderer/rendering_method = forward_plus` (already applied in Phase 0, with Tom's approval). Forward+ was chosen for its 2D lighting headroom, HDR 2D and glow on a Windows desktop target. The `.mobile` and `.web` overrides stay on `gl_compatibility`.

**Project settings to apply at the start of Phase 1** (via `set_project_setting`, **never** by editing `project.godot` directly):
- `display/window/size/viewport_width = 320`, `viewport_height = 180`
- Window override `1920×1080`; stretch mode `viewport`, aspect `keep`, scale mode `integer`
- `rendering/textures/canvas_textures/default_texture_filter = Nearest`
- `rendering/2d/snap/snap_2d_transforms_to_pixel = true`

**Workflow:**
- Use **Godot MCP Pro editor operations** for scenes, nodes, TileSets and the Inspector. Use GDScript for behaviour. Don't build whole scenes by script.
- `execute_editor_script` is for inspection and small one-off fixes only. **Never** use it to generate scenes, nodes or resources wholesale. Use the dedicated tools so the results are visible and editable in the editor.
- Visual and tuning values go in Inspector properties or `.tres` resources, not hardcoded in scripts.
- To check the visuals, use `play_scene` and then `get_game_screenshot`, which confirms pixel scale, integer scaling and palette in the running game. Always `stop_scene` afterwards.
- Data (items, enemies, NPC dialogue, area settings) goes in `.tres` resources.
- Naming: `snake_case` files and folders, `PascalCase` class names.
- Lighting: 2D lights, fog and god-ray overlays, and a darkness tint per area. **No normal maps.**

---

## 8. Git

- Small, focused commits with clear messages (for example, `art: approve chr_awa_b idle/walk`).
- Commit documents together with the change they describe.
- Tag milestones (`phase0-complete`, …).

## 9. Audio

- Music is composed by Tom (MIDI via piano). Don't generate or source music.
- SFX: free sounds under **CC0 or CC-BY only**, each **logged in `CREDITS.md`** when added.

## 10. Tone guard

Cosy on the surface, eerie underneath. Unsettling at most, **never** horror, gore or jump scares. Awa is an **explorer, not a warrior**, and must never resemble an existing game hero.
