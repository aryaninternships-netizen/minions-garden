#!/usr/bin/env python3
# Author tulip Lottie animations, pure code.
# Outputs: assets/field.json (hero swaying field) + assets/<variety>.json loops.
# Gotchas honored: one fill per group, first shape renders ON TOP, in/out points set.

import json
import math

from lottie import objects, Point, Color

FPS = 30
FRAMES = 120

GREEN = Color(0.24, 0.55, 0.30)
DGREEN = Color(0.18, 0.42, 0.24)


def path(group, pts, color, closed=True):
    g = group.add_shape(objects.Group())
    p = g.add_shape(objects.Path())
    bez = p.shape.value
    for pt in pts:
        bez.add_point(Point(*pt))
    if closed:
        bez.close()
    g.add_shape(objects.Fill(color))
    return g


def smooth_path(group, pts, color):
    # points with in/out tangents: (x, y, tx, ty) tangent mirrored
    g = group.add_shape(objects.Group())
    p = g.add_shape(objects.Path())
    bez = p.shape.value
    for x, y, tx, ty in pts:
        bez.add_smooth_point(Point(x, y), Point(tx, ty))
    bez.close()
    g.add_shape(objects.Fill(color))
    return g


def build_tulip(layer, x, base_y, height, petal, edge, phase, scale=1.0,
                sway=6.0, parrot=False):
    """One tulip: stem + 2 leaves + 3-petal bloom, swaying at anchor=base."""
    t = layer.add_shape(objects.Group())
    t.transform.anchor_point.value = Point(0, 0)
    t.transform.position.value = Point(x, base_y)
    t.transform.scale.value = Point(scale * 100, scale * 100)

    h = height
    bw = h * 0.30  # bloom half-width

    # bloom group (topmost, added first)
    bloom = t.add_shape(objects.Group())
    by = -h  # bloom base y
    # center petal ON TOP
    smooth_path(bloom, [
        (0, by - bw * 1.9, bw * 0.5, 0),
        (bw * 0.55, by - bw * 0.6, 0, bw * 0.5),
        (0, by + bw * 0.15, bw * 0.45, 0),
        (-bw * 0.55, by - bw * 0.6, 0, -bw * 0.5),
    ], petal)
    # side petals (edge color, slightly darker/lighter)
    for sx in (-1, 1):
        pts = [
            (sx * bw * 0.55, by - bw * 2.0, bw * 0.35, sx * bw * 0.3),
            (sx * bw * 0.95, by - bw * 0.5, 0, bw * 0.4),
            (0, by + bw * 0.2, bw * 0.5, 0),
            (sx * bw * 0.1, by - bw * 0.9, 0, -bw * 0.4),
        ]
        if parrot:  # jagged fringe: extra spike at the tip
            pts.insert(1, (sx * bw * 1.15, by - bw * 1.4, bw * 0.1, bw * 0.1))
        smooth_path(bloom, pts, edge)

    # stem
    stem = t.add_shape(objects.Group())
    g = stem.add_shape(objects.Group())
    r = g.add_shape(objects.Rect())
    r.position.value = Point(0, -h / 2)
    r.size.value = Point(h * 0.045 + 2, h)
    r.rounded.value = 2
    g.add_shape(objects.Fill(GREEN))

    # leaves
    leaves = t.add_shape(objects.Group())
    for sx, ly in ((-1, -h * 0.30), (1, -h * 0.42)):
        smooth_path(leaves, [
            (sx * 2, ly, h * 0.04, 0),
            (sx * h * 0.22, ly - h * 0.16, h * 0.05, -h * 0.06),
            (sx * h * 0.30, ly - h * 0.34, h * 0.02, -h * 0.04),
            (sx * h * 0.14, ly - h * 0.10, -h * 0.04, h * 0.05),
        ], DGREEN if sx < 0 else GREEN)

    # sway: gentle rotation loop, phase-offset
    for f in range(0, FRAMES + 1, 10):
        ang = sway * math.sin(2 * math.pi * (f / FRAMES) + phase)
        t.transform.rotation.add_keyframe(f, ang)
    return t


VARIETIES = {
    # name: (petal color, edge color, parrot fringe?)
    "triumph_red":    (Color(0.82, 0.12, 0.16), Color(0.65, 0.07, 0.12), False),
    "darwin_orange":  (Color(0.96, 0.55, 0.10), Color(0.85, 0.38, 0.05), False),
    "queen_of_night": (Color(0.24, 0.09, 0.22), Color(0.15, 0.05, 0.15), False),
    "parrot_purple":  (Color(0.55, 0.25, 0.65), Color(0.40, 0.15, 0.52), True),
    "fringed_pink":   (Color(0.95, 0.55, 0.70), Color(0.88, 0.40, 0.60), True),
    "white_emperor":  (Color(0.97, 0.96, 0.92), Color(0.88, 0.86, 0.80), False),
}


def make_single(name, petal, edge, parrot):
    an = objects.Animation(FRAMES, FPS)
    an.width, an.height = 300, 400
    layer = objects.ShapeLayer()
    layer.in_point, layer.out_point = 0, FRAMES
    an.add_layer(layer)
    build_tulip(layer, 150, 380, 300, petal, edge, phase=0.0, sway=4.0,
                parrot=parrot)
    with open(f"assets/{name}.json", "w") as fh:
        json.dump(an.to_dict(), fh)


def make_field():
    an = objects.Animation(FRAMES, FPS)
    an.width, an.height = 1200, 500
    layer = objects.ShapeLayer()
    layer.in_point, layer.out_point = 0, FRAMES
    an.add_layer(layer)
    names = list(VARIETIES)
    # back row first? No: first shapes render on top -> add FRONT row first.
    rows = [
        (492, 1.00, 0),   # front
        (470, 0.80, 3),
        (450, 0.62, 6),   # back
    ]
    import random
    rnd = random.Random(7)
    for base_y, sc, off in rows:
        xs = list(range(60, 1200, 95))
        for i, x in enumerate(xs):
            petal, edge, parrot = VARIETIES[names[(i + off) % len(names)]]
            build_tulip(layer, x + rnd.randint(-18, 18), base_y,
                        int(170 * sc + rnd.randint(-15, 15)), petal, edge,
                        phase=rnd.uniform(0, 6.28), scale=sc,
                        sway=5.0, parrot=parrot)
    with open("assets/field.json", "w") as fh:
        json.dump(an.to_dict(), fh)


for name, (p, e, fr) in VARIETIES.items():
    make_single(name, p, e, fr)
make_field()
print("wrote all tulip jsons")
