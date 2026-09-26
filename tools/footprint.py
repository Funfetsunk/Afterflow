"""Where an object meets the ground: its collision footprint.

Top-down objects should only block at their base (a trunk, the foot of a bush,
a stone's bottom), so Awa can walk behind crowns and tops. The footprint is the
bounding box of the object's solid pixels in its lowest few rows; the cast
shadow (374e4a) is not solid.

Used by tools/build_tileset.py (stamps, kits) and tools/paint_forest.py (baked
woodland).
"""

SHADOW = {(0x37, 0x4e, 0x4a)}


def footprint(img, depth=5, min_height=4):
    """(x0, y0, x1, y1) of the base in img pixels (x1/y1 exclusive), or None if empty."""
    px = img.load()
    w, h = img.size
    solid_rows = [y for y in range(h) if any(px[x, y][3] and px[x, y][:3] not in SHADOW for x in range(w))]
    if not solid_rows:
        return None
    bottom = solid_rows[-1]
    top = bottom - depth + 1
    xs = [x for y in range(max(0, top), bottom + 1) for x in range(w)
          if px[x, y][3] and px[x, y][:3] not in SHADOW]
    y0 = min(top, bottom + 1 - min_height)
    return (min(xs), max(0, y0), max(xs) + 1, bottom + 1)


def split_by_cells(rect, cell_size=16):
    """Split an img-space rect into {(col, row): (x0, y0, x1, y1) in cell-local pixels}."""
    x0, y0, x1, y1 = rect
    out = {}
    for row in range(y0 // cell_size, (y1 - 1) // cell_size + 1):
        for col in range(x0 // cell_size, (x1 - 1) // cell_size + 1):
            cx, cy = col * cell_size, row * cell_size
            ix0, iy0 = max(x0, cx), max(y0, cy)
            ix1, iy1 = min(x1, cx + cell_size), min(y1, cy + cell_size)
            if ix1 > ix0 and iy1 > iy0:
                out[(col, row)] = (ix0 - cx, iy0 - cy, ix1 - cx, iy1 - cy)
    return out
