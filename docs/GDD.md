# Afterflow — Game Design Document

> **Status:** v0.1, design locked from the planning session. Phase 0 (look development) not yet started.
> **Spoiler warning:** this document contains the full story, including the ending. Keep that in mind when sharing it.

---

## 1. Overview

| | |
|---|---|
| **Working title** | Afterflow |
| **Genre** | 2D action-adventure (Zelda-like), exploration and mystery first |
| **Perspective** | 3/4 top-down ("low top-down") |
| **Engine** | Godot 4.x (latest stable, pinned; see CLAUDE.md), GDScript |
| **Tooling** | VS Code + Claude Code, Godot MCP Pro, PixelLab MCP |
| **Platform** | Windows desktop first, gamepad-first (keyboard supported) |
| **Length** | 2–4 hours |
| **Scope** | One interconnected overworld (5 biomes), 4 dungeons, final area |
| **Audience** | Family-friendly: unsettling at times, never frightening |

**One-line pitch:** A curious girl explores a lovely, quietly wrong countryside, and slowly discovers that the scars on the world are her own footprints from lives she can't remember.

---

## 2. Design pillars

1. **Discovery leads.** Exploration and solving the mystery are the heart of the game. The world should reward curiosity at every turn.
2. **Cosy on the surface, eerie underneath.** It looks lovely, but something keeps the player asking questions about the world, how it works, and how Awa fits into it.
3. **Combat is second, but polished.** Zelda-style, readable, satisfying feedback. It should challenge without ever stopping players from enjoying the world.
4. **Everything means something twice.** Every strange detail has a second meaning once the truth is known. Clues are planned deliberately, never scattered at random.

---

## 3. Story (full spoilers)

### 3.1 The truth

- **Awa** is caught in a time loop. Each loop begins with her waking as a 12-year-old girl with no memory of the world. She never ages between loops, however long she lived in the previous one.
- Every loop ends at the **river's source** with a **final choice**: *continue the loop* or *end it and let the world heal*.
- She has lived **dozens** of loops. Her journey to the source has taken weeks in some loops and decades in others. **Every time, she has chosen to continue.**
- She is not a villain. She isn't deliberately hurting anything, but her continued, looping existence **draws life out of the world**.
- Each loop has changed the world, through her actions and through how people reacted to her. People have been born and died across her loops.

### 3.2 The world's two responses (body and mind)

- **The body: the creatures.** The world defends itself like an immune system. Its creatures are white blood cells acting on reflex against an infection, and Awa is that infection. Drained areas therefore have more, and nastier, creatures.
- **The mind: the shrines.** The world knows it can't stop her, because only the final choice ends the loop. So it keeps her alive at the shrines, giving her the chance to choose differently, hoping one day she frees it.
- *In short: the body fights the fever by reflex; the mind keeps the patient alive.* This is never stated early. A late note or NPC can say it almost this plainly.

### 3.3 The walking stick (hidden)

- Every swing of Awa's walking stick draws some of the world's power into it. That's how a 12-year-old can defeat the world's creatures.
- **Never shown in-game.** It's discovered only late, through storytelling. Players who fought a lot should feel the weight of it.

### 3.4 The shade

- Ending a loop leaves a **shade** of herself behind for the next loop to find.
- **Only one shade exists at a time.** Creating a new shade destroys the previous one.
- The shade **lingers wherever it has something to say**. It helps fill gaps in the player's understanding and appears briefly on the approach to the source (see §9).

### 3.5 The diary

- Awa wakes with a diary in her satchel, containing hints about the world.
- It is **hers**. She has written in it across loops, but she (and the player) doesn't know that.
- New entries appear as she discovers things this loop, **in the same hand and voice as the old ones**. That's the quiet giveaway.
- The diary and Awa are the **only things that cross loops**. Documents and notes in the world do not reset between loops.

### 3.6 Endings

- The final choice happens at the source: **continue the loop** or **end it**.
- There is **no third option**. The sacrifice must stay real.
- "Continue" must be genuinely tempting, not the obviously wrong answer.
- **Knowledge-gated secrets enrich the epilogue** (what the healed world, or the next loop, becomes) without changing the choice itself.

---

## 4. Awa (player character)

- About 12 years old, with long, **straight** ginger hair. Inquisitive, capable, **an explorer, not a warrior**.
- Not weak: she can and will defend herself.
- Being a young girl frames the game around curiosity and exploration, not constant giant monsters and swordplay.
- Visual design: see ART_BIBLE.md §4. She must never read as a cosplay of an existing game hero.

---

## 5. World

### 5.1 Structure

- **One interconnected overworld.** Dungeon order is partly open, and the map folds back on itself with shortcuts.
- **The river is the spine**, running through every biome to its source.

### 5.2 Biomes

| # | Biome | Role | Dungeon |
|---|---|---|---|
| 1 | **Meadow village** | Start area, the most "lovely". Small English countryside hamlet. | none (lantern found in the overworld) |
| 2 | **Old woodland** | Tall trees, hazy golden light, dark edges | Hollow tree / burrow |
| 3 | **Lakes & wetlands** | River heartland | Drowned mill / sluice works |
| 4 | **Highland ruins** | Old stone, wind, abandonment | Observatory / temple ruins |
| 5 | **Coast & cliffs** | Edge of the world | Sea cave / lighthouse |
| — | **The source** | Most drained area. The reveal and the final choice. | Final area (not a standard dungeon) |

### 5.3 Two eerie layers (kept separate)

- **Abandonment / overgrowth.** Found everywhere and gentle: ruins reclaimed by moss, ivy and ferns, where people left (often because of past loops). Beautiful, sad, historical.
- **The drain.** Rarer, colder and more disturbing: colour washes towards blue-grey, and movement stops (still grass, still water, silence). It grows stronger towards the source.
- Noticing the difference between "nature took this back" and "something took the life from this" is an **early clue**.

### 5.4 Evidence of past loops (four layers)

1. **Her traces.** Old campsites, carvings, tools she left behind.
2. **Consequences.** Things she built, broke or changed, such as a bridge she broke or a village that moved.
3. **People.** Family stories and old portraits of "a red-haired girl". **Pitch this carefully** so it isn't immediately obvious that she has been here before.
4. **The drain.** Worst near where she lived longest.

Every dungeon was tackled in previous loops and shows signs of Awa's doing.

---

## 6. Progression and gating

- **Hybrid gating.**
  - **Items gate the critical path**, so every player can finish.
  - **Knowledge gates secrets** (torn diary pages, the shade's messages, deeper lore) and the richer epilogue.
- Understanding the world literally opens it.

---

## 7. Player verbs and combat

### 7.1 Movement

- **8-way analog movement**, with sprites facing **4 directions** (the classic Zelda approach).

### 7.2 Combat (Zelda-style)

- **Walking stick** is the only melee weapon: swings, plus a charged spin attack. No weapon upgrades or tiers.
- **Feel:** hit-stop, hit flash, knockback, light screen shake, clear enemy telegraphs.
- **No stamina system.** Fights are fair and readable. Bosses give a reasonable challenge, and nothing is punishing.
- **Open question:** whether to add a dodge/roll (see §15).

### 7.3 Key items (5, no tiers, quick-select)

| Item | Use | Found |
|---|---|---|
| **Lantern** | Lights dark areas, reveals faded writing and hidden marks | Early, in the overworld |
| **Slingshot** | Ranged attack, hits switches and distant targets | Dungeon (TBD) |
| **Vine hook** | Grapples across gaps, pulls objects | Dungeon (TBD) |
| **Bell** | Stuns certain creatures, wakes old mechanisms, makes shrines resonate | Dungeon (TBD) |
| **Waders** | Cross deep water | Dungeon (TBD) |

Assigning items to dungeons is open. Story hook: the lantern may later turn out to have been hers in an earlier loop.

---

## 8. Enemies

- **Concept:** the world's white blood cells, made from each biome's own materials (moss, bark, stone, water).
- **Shared visual signature** across all biomes, such as a soft pale glow or a single white "eye", so players read them as one family.
- **Escalation:** almost cute in the meadow; larger, colder and more numerous towards the source.

---

## 9. Bosses and finale

- **One boss per dungeon (4):** heavily corrupted guardian creatures. Challenging but fair.
- **Finale:** a quiet climb to the source, **no traditional final boss**. The current **shade** appears on the approach: a brief encounter, possibly a short fight or a blocked path, until Awa understands. Then the choice.

---

## 10. NPCs

- **About 6 named NPCs** across the whole adventure, supported by heavy environmental storytelling.
- They **do not remember Awa**.
- Candidate roles (to be finalised): the miller, the lighthouse keeper, a shrine-keeper, a child who has heard stories of the red-haired girl.
- Ambient villagers, if used, have one line each.

---

## 11. Story delivery

- **Environmental storytelling** is the backbone.
- **Documents and notes** found in the world persist across loops.
- **The diary** (§3.5), which also contains hidden **torn-out pages** as knowledge-gated secrets.
- **Warm but evasive NPCs.**
- **A few recurring symbols** for eerie mood, but no full cipher language.

---

## 12. Death, saving and respawn

- **Shrines** heal Awa and act as respawn points. There is **no loss on death**.
- **Autosave** on entering new areas.
- A mid-loop death is just a shrine respawn, a game mechanic. Diegetically, it's consistent with the world's mind keeping her alive, but this is never flagged on screen.
- Only the final choice ends a loop.

---

## 13. Camera, screen and HUD

- **Internal resolution 320×180**, integer-scaled (6× to 1080p), with 16px tiles (changed from 480×270 on 2026-09-25 for the 16-bit look, see Art Bible §0).
- **Camera:** scrolls smoothly and follows the player outdoors, clamped to area bounds. **Room-by-room** with slide transitions in dungeons. Dungeon rooms are designed around one screen (15 × ~8.4 tiles at 32px).
- **HUD (minimal):**
  - **Health:** leaves on a sprig, top-left. Leaves wilt as she takes hits, a quiet echo of the drain.
  - **Current key item:** bottom-right.
  - Everything else lives in the diary.
- **The diary is the single UI hub:** map, notes, hints and collected documents.

---

## 14. Audio

### 14.1 Music

- Composed by Tom: MIDI, played on piano.
- **Direction:** a cosy woodland feel. **Variations on the same themes** thin out and cool as areas become more drained, with near-silence at the source.
- **Principle:** the music reflects the drain. Warm areas are full; drained areas are sparse and cold.

### 14.2 Sound effects

- Free sound files, **CC0 or CC-BY**.
- **Every sound is logged in `CREDITS.md`** (source, author, licence) when it's added.

---

## 15. Open questions

- Dodge/roll: include one, or pure ALTTP-style movement?
- Which dungeon awards which key item?
- NPC names and exact roles (about 6).
- Biome and place names.
- Boss designs (4).
- Default control mapping (gamepad and keyboard).
- The shade's exact finale beat: a short fight or a non-combat encounter?

---

## 16. Roadmap

| Phase | Goal | Exit criteria |
|---|---|---|
| **0: Look development** | Art only, **no game code.** Generate the sample set, build the palette-remap and mock-composer tools, produce mock screenshots. | Art Bible v1.0 approved, with proportions, palette and parameters locked |
| **1: Foundation** | Godot project settings, Awa movement and animation, camera, meadow tilemap | Awa walks around a meadow at the correct scale |
| **2: Vertical slice** | Meadow + old woodland + first dungeon + boss, one shrine, lantern, diary basics, combat | Playable 15–20 min slice that feels like the game |
| **3: Production** | Remaining biomes, dungeons, items, NPCs, story | Full game playable start to finish |
| **4: Polish** | Endings, epilogue variants, audio pass, balance, bug fixing | Release candidate |
