"""Cut the lane-through-the-ledge crossing from the north star as a 3x4 stamp.

In the north star the village lane runs straight down through the river ledge
to the water: the ledge stops on both sides of it with a grass fringe, and the
lane carries on over the bank. The river ledge tiles (ts_meadow_ledge_ns_*)
come from north-star rows 144-175, so the crossing is cut from the same rows,
plus the grass band above (128-143, the lane between its fringes) and one row
of water below.

The cut is offset 8px (north-star x 152-199) so that the lane sits on a grid
line, where tools/wang_layout.py draws a one-vertex path: paint the path down to
the vertex at the stamp's top edge (a path vertex may not touch the ledge row),
then place this stamp with the lane's vertex column in its middle.

North-star flowers in the grass either side of the lane are painted out.
The north star shows only 4 rows of the water row (176-179); the rest of that
row repeats those 4 rows.

Run from the project root:
    python tools/kits/make_ford16.py
    python tools/make_stamp.py art/final/obj_ford16.png ford --left
"""

from PIL import Image

NS = "art/final/north_star/ns_meadow_village_r2_mix.png"
X0, X1 = 152, 200
Y0, Y1 = 128, 180                    # grass band 128-143, ledge 144-175, 4 visible water rows
LANE = (4, 27)                       # local columns of the lane and its fringes
GRASS = {(0x54, 0x7e, 0x64), (0x37, 0x4e, 0x4a), (0x31, 0x36, 0x38), (0x67, 0x66, 0x33)}
GRASS_FILL = (0x54, 0x7e, 0x64, 255)


def main():
    ns = Image.open(NS).convert("RGBA")
    cut = ns.crop((X0, Y0, X1, Y1))
    out = Image.new("RGBA", (X1 - X0, 64), (0, 0, 0, 0))
    out.alpha_composite(cut, (0, 0))
    water = ns.crop((X0, 176, X1, 180))
    for y in range(52, 64, 4):
        out.alpha_composite(water, (0, y))
    # clear the north star's flowers from the grass either side of the lane (one is cut in half)
    px = out.load()
    for y in range(24):
        for x in range(out.width):
            if not LANE[0] <= x <= LANE[1] and px[x, y][:3] not in GRASS:
                px[x, y] = GRASS_FILL
    out.save("art/final/obj_ford16.png")
    print("art/final/obj_ford16.png", out.size)


if __name__ == "__main__":
    main()
