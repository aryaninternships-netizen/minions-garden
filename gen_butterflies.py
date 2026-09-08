#!/usr/bin/env python3
# Butterfly wing atlas: 6 species, one per cell, drawn from traced wing
# outlines (forewing sweeps up-and-out, hindwing rounds down-and-in) smoothed
# with Catmull-Rom, then shaded, veined and marked per species.
# Refs: monarch, blue morpho, tiger swallowtail, peacock, painted lady, jezebel.
from PIL import Image, ImageDraw, ImageFilter

CELL, COLS, ROWS, SS = 320, 3, 2, 3
W, H = CELL * COLS, CELL * ROWS
img = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# outlines in body space: x out from body, y up. Anchored near (0,0).
FORE = [(0.04, 0.06), (0.26, 0.46), (0.52, 0.78), (0.80, 0.86),
        (0.99, 0.66), (1.00, 0.40), (0.84, 0.16), (0.50, 0.02), (0.14, -0.02)]
HIND = [(0.05, -0.04), (0.38, -0.10), (0.66, -0.30), (0.78, -0.58),
        (0.68, -0.82), (0.42, -0.88), (0.20, -0.70), (0.08, -0.36)]


def catmull(pts, n=14):
    """closed Catmull-Rom through pts"""
    out, m = [], len(pts)
    for i in range(m):
        p0, p1 = pts[(i - 1) % m], pts[i]
        p2, p3 = pts[(i + 1) % m], pts[(i + 2) % m]
        for j in range(n):
            t = j / n
            t2, t3 = t * t, t * t * t
            out.append((
                0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                       (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
                0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)))
    return out


def place(pts, cx, cy, s, flip):
    return [(cx + (-x if flip else x) * s, cy - y * s) for x, y in pts]


def shade(poly, base, dark):
    d.polygon(poly, fill=base)
    cx = sum(p[0] for p in poly) / len(poly)
    cy = sum(p[1] for p in poly) / len(poly)
    for k, f in enumerate((0.74, 0.46)):
        inner = [(cx + (x - cx) * f, cy + (y - cy) * f) for x, y in poly]
        mix = tuple(int(base[i] + (dark[i] - base[i]) * (0.16 + k * 0.18))
                    for i in range(3)) + (255,)
        d.polygon(inner, fill=mix)


def species(col, row, base, dark, rim, spots, spot_col,
            band=None, band_col=None, tips=None, tail=False, veins=7):
    cx = (col * CELL + CELL / 2) * SS
    cy = (row * CELL + CELL * 0.52) * SS
    s = CELL * SS * 0.44
    fore_s = catmull(FORE)
    hind_s = catmull(HIND)
    for flip in (False, True):
        for pts, is_fore in ((hind_s, False), (fore_s, True)):
            poly = place(pts, cx, cy, s, flip)
            shade(poly, base, dark)
            d.line(poly + [poly[0]], fill=rim, width=int(5 * SS), joint="curve")
        if tail:                                    # swallowtail streamers
            p = place(hind_s, cx, cy, s, flip)[int(len(hind_s) * 0.42)]
            d.line([p, (p[0] + (-1 if flip else 1) * 8 * SS, p[1] + 52 * SS)],
                   fill=rim, width=int(7 * SS))
        # veins fan from the wing root
        for pts, root_y, cnt in ((fore_s, 0.06, veins), (hind_s, -0.06, veins - 2)):
            poly = place(pts, cx, cy, s, flip)
            root = (cx + (-1 if flip else 1) * s * 0.05, cy - root_y * s)
            for i in range(cnt):
                t = 0.10 + i * (0.60 / max(cnt - 1, 1))
                p = poly[int(t * (len(poly) - 1))]
                d.line([root, p], fill=rim, width=max(int(1.6 * SS), 1))
        if band:                                    # hindwing colour band
            inner = [(x * band, y * band) for x, y in HIND]
            d.polygon(place(catmull(inner), cx, cy, s, flip), fill=band_col)
        for (which, t, rr) in spots:
            poly = place(fore_s if which == "f" else hind_s, cx, cy, s, flip)
            px, py = poly[int(t * (len(poly) - 1))]
            px, py = cx + (px - cx) * 0.84, cy + (py - cy) * 0.84
            r = rr * s
            d.ellipse([px - r, py - r, px + r, py + r], fill=spot_col)
            if rr > 0.05:
                r2 = r * 0.40
                d.ellipse([px - r2, py - r2 * 1.5, px + r2, py + r2 * 0.2],
                          fill=(252, 252, 252, 230))
        if tips:
            poly = place(fore_s, cx, cy, s, flip)
            for (t, rr) in tips:
                px, py = poly[int(t * (len(poly) - 1))]
                r = rr * s
                d.ellipse([px - r, py - r, px + r, py + r],
                          fill=(255, 255, 255, 240))
    # body: thorax, abdomen, antennae
    d.ellipse([cx - s * 0.050, cy - s * 0.16, cx + s * 0.050, cy + s * 0.62],
              fill=(42, 34, 29, 255))
    d.ellipse([cx - s * 0.070, cy - s * 0.26, cx + s * 0.070, cy - s * 0.02],
              fill=(28, 23, 21, 255))
    for sgn in (-1, 1):
        d.line([(cx, cy - s * 0.24), (cx + sgn * s * 0.22, cy - s * 0.56)],
               fill=(30, 25, 22, 255), width=int(2.2 * SS))
        d.ellipse([cx + sgn * s * 0.22 - 4 * SS, cy - s * 0.56 - 4 * SS,
                   cx + sgn * s * 0.22 + 4 * SS, cy - s * 0.56 + 4 * SS],
                  fill=(30, 25, 22, 255))


species(0, 0, (234, 129, 30, 255), (170, 74, 15, 255), (24, 18, 16, 255),
        [("f", 0.30, 0.028), ("f", 0.40, 0.026), ("f", 0.50, 0.024),
         ("h", 0.30, 0.024), ("h", 0.45, 0.022), ("h", 0.60, 0.020)],
        (255, 255, 255, 245), veins=8)                      # monarch
species(1, 0, (63, 114, 222, 255), (26, 56, 152, 255), (20, 24, 48, 255),
        [("h", 0.36, 0.052), ("h", 0.56, 0.042)],
        (224, 232, 247, 210), veins=6)                      # blue morpho
species(2, 0, (247, 212, 63, 255), (200, 152, 26, 255), (26, 21, 16, 255),
        [("h", 0.40, 0.030), ("h", 0.58, 0.026)],
        (76, 112, 196, 240), tail=True, veins=9)            # tiger swallowtail
species(0, 1, (172, 49, 40, 255), (112, 26, 24, 255), (36, 20, 18, 255),
        [("f", 0.36, 0.072), ("h", 0.44, 0.062)],
        (50, 66, 148, 245), veins=6)                        # peacock
species(1, 1, (217, 136, 75, 255), (156, 88, 44, 255), (50, 33, 24, 255),
        [("h", 0.34, 0.024), ("h", 0.50, 0.022), ("h", 0.66, 0.020),
         ("f", 0.55, 0.022)],
        (42, 31, 27, 240), tips=[(0.22, 0.032), (0.32, 0.024)], veins=7)
species(2, 1, (248, 246, 239, 255), (203, 199, 188, 255), (36, 31, 28, 255),
        [("h", 0.34, 0.036), ("h", 0.50, 0.032), ("h", 0.66, 0.028)],
        (226, 62, 48, 248), band=0.80, band_col=(250, 199, 54, 255), veins=7)

img = img.resize((W, H), Image.LANCZOS).filter(ImageFilter.SMOOTH)
img.save("assets/butterflies.png")
print("wrote assets/butterflies.png", img.size)
