"""Build the gable-end cottage stamps from the north star's left cottage.

The 16px cottage kit (make_cottage16.py) only builds long cottages seen from
the front. The north star's other house turns its gable end to the camera: a
slate roof with the ridge running away from us, a triangular stone gable and a
short wall with one window. It is exactly 4 tiles (64px) wide, so it stays on
the grid as a fixed stamp.

The roof planes have a straight band (north-star rows 47-62) that can repeat,
so the stamp comes in three roof depths:

  d0  5 tiles tall  (band left out)
  d1  6 tiles tall  (as in the north star)
  d2  7 tiles tall  (band repeated)

Clean-up: the crop starts at row 22, below the tree trunk behind the ridge
top, and the roof top gets a closing outline; the lean-to shed on its right is
left out. A 374e4a cast shadow runs
down the right side of the roof and wall on the grass (Art Bible grounding rule),
so each stamp is 5 tiles wide with the house on the left 4.

Run from the project root:
    python tools/kits/make_gable16.py
Writes art/final/obj_gable16_d{0,1,2}.png; then make them stamps with
    python tools/make_stamp.py art/final/obj_gable16_d1.png gable_d1 --left
"""

from PIL import Image

NS = "art/final/north_star/ns_meadow_village_r2_mix.png"
X0, X1 = 20, 84                  # house columns (roof outline to roof outline)
TOP, BAND0, BAND1, BOTTOM = 22, 47, 63, 115   # rows: roof top, repeat band [47, 63), wall base
GROUND = {(0x54, 0x7e, 0x64), (0x37, 0x4e, 0x4a), (0x31, 0x36, 0x38)}
OUTLINE = (0x2e, 0x22, 0x2f, 255)
SHADOW = (0x37, 0x4e, 0x4a, 255)
SHADOW_W = 8


def cut(ns):
    """The house on transparency: background flood-filled away from the crop edge."""
    img = ns.crop((X0, TOP, X1, BOTTOM)).convert("RGBA")
    px = img.load()
    w, h = img.size
    stack = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    seen = set()
    while stack:
        x, y = stack.pop()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h) or px[x, y][:3] not in GROUND:
            continue
        seen.add((x, y))
        px[x, y] = (0, 0, 0, 0)
        stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    # the lean-to shed's edge below the eaves (north-star x 80-83, rows 90+)
    for y in range(90 - TOP, h):
        for x in range(60, w):
            px[x, y] = (0, 0, 0, 0)
    return img


def tidy_ridge(img):
    """Close the roof top with an outline (the crop starts below the tree trunk behind the ridge)."""
    px = img.load()
    for x in range(img.width):
        col = [px[x, y][3] for y in range(img.height)]
        if any(col):
            top = col.index(255) if 255 in col else None
            if top is not None and px[x, top] != OUTLINE:
                px[x, top] = OUTLINE
    return img


def stack(img, repeats):
    """Top part, the roof band `repeats` times (0-2), then the gable and wall."""
    top = img.crop((0, 0, img.width, BAND0 - TOP))
    band = img.crop((0, BAND0 - TOP, img.width, BAND1 - TOP))
    rest = img.crop((0, BAND1 - TOP, img.width, img.height))
    parts = [top] + [band] * repeats + [rest]
    out = Image.new("RGBA", (img.width, sum(p.height for p in parts)), (0, 0, 0, 0))
    y = 0
    for p in parts:
        out.alpha_composite(p, (0, y))
        y += p.height
    return out


def with_shadow(img):
    """Cast shadow on the grass to the right: a straight-edged column from the
    full-width roof down to the base, filling in under the eaves beside the wall."""
    out = Image.new("RGBA", (img.width + SHADOW_W, img.height), (0, 0, 0, 0))
    px = img.load()
    op = out.load()
    start = next(y for y in range(img.height) if px[img.width - 1, y][3])   # roof reaches its right edge
    for y in range(start + 1, img.height - 1):
        right = max((x for x in range(img.width) if px[x, y][3]), default=img.width - 1)
        for x in range(right + 1, img.width + SHADOW_W):
            op[x, y] = SHADOW
    out.alpha_composite(img)
    return out


def drop_specks(img, min_size=4):
    """Remove tiny detached scraps left by the background cut."""
    px = img.load()
    w, h = img.size
    seen = set()
    for sy in range(h):
        for sx in range(w):
            if (sx, sy) in seen or not px[sx, sy][3]:
                continue
            comp, todo = [], [(sx, sy)]
            seen.add((sx, sy))
            while todo:
                x, y = todo.pop()
                comp.append((x, y))
                for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= n[0] < w and 0 <= n[1] < h and n not in seen and px[n][3]:
                        seen.add(n)
                        todo.append(n)
            if len(comp) < min_size:
                for q in comp:
                    px[q] = (0, 0, 0, 0)
    return img


def main():
    ns = Image.open(NS).convert("RGB")
    house = tidy_ridge(drop_specks(cut(ns)))
    for repeats, name in ((0, "d0"), (1, "d1"), (2, "d2")):
        img = with_shadow(stack(house, repeats))
        path = f"art/final/obj_gable16_{name}.png"
        img.save(path)
        print(path, img.size)


if __name__ == "__main__":
    main()
