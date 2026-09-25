"""Build the hollow-oak dungeon's rooms as a compose_mock layout (then layout_to_tilemap.py).

Rooms are one screen each (20x11 cells, GDD §13), on a grid; the room camera
snaps to them. Each room is walled with the dungeon16 kit: wall_top along the
top with the lit wall_face below it, wall edges down the sides and along the
bottom, and gaps (2 cells wide) where rooms connect. Locked doors are scenes
placed over their gap in Godot, so the gap itself is floor.

    (1,0) boss room            the warden; its north gap opens when it falls
    (0,1) dark room  (1,1) hall   dark room: lantern marks, key B; hall: barklings
    (0,2) entrance   (1,2) fight  entrance from the woodland (south gap);
                                  fight: clear it for key A (door A north)

Run from the project root:
    python tools/mock_layouts/build_hollow_oak.py
Writes tools/mock_layouts/hollow_oak.json.
"""

import json
import random
from pathlib import Path

RW, RH = 20, 11
KIT = json.loads(Path("tools/kits/dungeon16.json").read_text())["tiles"]

# room -> gaps: n/s/e/w; pillars: (col, row) of 2x2 root pillars inside the room
ROOMS = {
    (1, 0): {"gaps": "ns", "pillars": [(4, 4), (14, 4)]},
    (0, 1): {"gaps": "s", "pillars": [(5, 5), (13, 5)]},
    (1, 1): {"gaps": "ns", "pillars": [(6, 3), (12, 3), (6, 7), (12, 7)]},
    (0, 2): {"gaps": "nse", "pillars": []},
    (1, 2): {"gaps": "nw", "pillars": [(9, 5)]},
}


def build():
    rng = random.Random("hollow-oak")
    cells = {}
    for (rx, ry), room in ROOMS.items():
        ox, oy = rx * RW, ry * RH
        gaps = room["gaps"]
        for r in range(RH):
            for c in range(RW):
                gap = (("n" in gaps and r <= 1 and c in (9, 10)) or ("s" in gaps and r == RH - 1 and c in (9, 10))
                       or ("w" in gaps and c == 0 and r in (5, 6)) or ("e" in gaps and c == RW - 1 and r in (5, 6)))
                if gap:
                    name = f"floor_{rng.randrange(4)}"
                elif r == 0:
                    name = "wall_top"
                elif r == 1:
                    name = "wall_top" if c in (0, RW - 1) else "wall_face"
                elif r == RH - 1:
                    name = "wall_edge_t"
                elif c == 0:
                    name = "wall_edge_r"
                elif c == RW - 1:
                    name = "wall_edge_l"
                elif r == 2:
                    name = "floor_shadow"
                else:
                    name = f"floor_{rng.randrange(4)}"
                cells[(ox + c, oy + r)] = name
        for pc, pr in room["pillars"]:
            for dc in (0, 1):
                cells[(ox + pc + dc, oy + pr)] = "wall_top"
                cells[(ox + pc + dc, oy + pr + 1)] = "wall_face"
    items = [{"image": KIT[name], "cell": [x, y]} for (x, y), name in sorted(cells.items(), key=lambda kv: (kv[0][1], kv[0][0]))]
    Path("tools/mock_layouts/hollow_oak.json").write_text(json.dumps({"items": items}, indent=1))
    print(f"hollow_oak.json: {len(items)} cells in {len(ROOMS)} rooms")


if __name__ == "__main__":
    build()
