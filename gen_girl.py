#!/usr/bin/env python3
# Girl walk-cycle Lottie (back view): 21yo, waist-length hair, coral dress.
# Rendered by lottie-web onto a canvas -> CanvasTexture billboard in the 3D field.
import json
import math

from lottie import objects, Point, Color

FPS, FRAMES = 30, 60
W, H = 250, 520

SKIN = Color(0.79, 0.56, 0.39)
DRESS = Color(0.85, 0.35, 0.29)
DRESS_D = Color(0.72, 0.27, 0.22)
HAIR = Color(0.16, 0.10, 0.07)
HAIR_HI = Color(0.26, 0.17, 0.11)
SHOE = Color(0.31, 0.21, 0.16)

an = objects.Animation(FRAMES, FPS)
an.width, an.height = W, H
layer = objects.ShapeLayer()
layer.in_point, layer.out_point = 0, FRAMES
an.add_layer(layer)


def ellipse(group, cx, cy, w, h, color):
    g = group.add_shape(objects.Group())
    e = g.add_shape(objects.Ellipse())
    e.position.value = Point(cx, cy)
    e.size.value = Point(w, h)
    g.add_shape(objects.Fill(color))
    return g


def poly(group, pts, color):
    g = group.add_shape(objects.Group())
    p = g.add_shape(objects.Path())
    bez = p.shape.value
    for pt in pts:
        bez.add_point(Point(*pt))
    bez.close()
    g.add_shape(objects.Fill(color))
    return g


def swing(tgroup, ax, ay, amp, phase=0.0):
    """keyframe rotation swing around anchor over the loop"""
    tgroup.transform.anchor_point.value = Point(ax, ay)
    tgroup.transform.position.value = Point(ax, ay)
    for f in range(0, FRAMES + 1, 5):
        tgroup.transform.rotation.add_keyframe(
            f, amp * math.sin(2 * math.pi * f / FRAMES + phase))


# z-order: FIRST added renders ON TOP.
# hair on top (covers back), then head, arms, dress, legs at bottom.

hair = layer.add_shape(objects.Group())
swing(hair, 125, 95, 4.5)
poly(hair, [(101, 80), (149, 80), (158, 200), (152, 315), (138, 328),
            (112, 328), (98, 315), (92, 200)], HAIR)      # fall to waist
ellipse(hair, 125, 88, 74, 66, HAIR)                       # crown
ellipse(hair, 108, 250, 12, 130, HAIR_HI)                  # sheen strand

head = layer.add_shape(objects.Group())
ellipse(head, 125, 90, 56, 60, SKIN)
neck = layer.add_shape(objects.Group())
ellipse(neck, 125, 122, 18, 26, SKIN)

armL = layer.add_shape(objects.Group())
swing(armL, 92, 150, 14, math.pi)                          # opposite legs
ellipse(armL, 90, 195, 17, 95, SKIN)
armR = layer.add_shape(objects.Group())
swing(armR, 158, 150, 14, 0.0)
ellipse(armR, 160, 195, 17, 95, SKIN)

dress = layer.add_shape(objects.Group())
swing(dress, 125, 160, 2.0)                                 # subtle swish
poly(dress, [(100, 135), (150, 135), (162, 230), (178, 340),
             (72, 340), (88, 230)], DRESS)
poly(dress, [(150, 135), (162, 230), (170, 300), (150, 300)], DRESS_D)

legL = layer.add_shape(objects.Group())
swing(legL, 110, 335, 10, 0.0)
ellipse(legL, 110, 400, 20, 130, SKIN)
ellipse(legL, 110, 470, 30, 22, SHOE)
legR = layer.add_shape(objects.Group())
swing(legR, 140, 335, 10, math.pi)
ellipse(legR, 140, 400, 20, 130, SKIN)
ellipse(legR, 140, 470, 30, 22, SHOE)

json.dump(an.to_dict(), open("assets/girl_walk.json", "w"))
print("wrote assets/girl_walk.json")
