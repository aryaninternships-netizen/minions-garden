#!/usr/bin/env python3
# HUD weather icons as Lottie: spinning sun, rain cloud, moon.
import json
import math

from lottie import objects, Point, Color

FPS, FRAMES = 30, 90


def new_anim(w=100, h=100):
    an = objects.Animation(FRAMES, FPS)
    an.width, an.height = w, h
    layer = objects.ShapeLayer()
    layer.in_point, layer.out_point = 0, FRAMES
    an.add_layer(layer)
    return an, layer


def ellipse(group, cx, cy, w, h, color):
    g = group.add_shape(objects.Group())
    e = g.add_shape(objects.Ellipse())
    e.position.value = Point(cx, cy)
    e.size.value = Point(w, h)
    g.add_shape(objects.Fill(color))


def rect(group, cx, cy, w, h, r, color):
    g = group.add_shape(objects.Group())
    rc = g.add_shape(objects.Rect())
    rc.position.value = Point(cx, cy)
    rc.size.value = Point(w, h)
    rc.rounded.value = r
    g.add_shape(objects.Fill(color))


GOLD = Color(0.99, 0.78, 0.15)
CLOUD = Color(0.62, 0.68, 0.76)
BLUE = Color(0.35, 0.55, 0.85)
PALE = Color(0.93, 0.93, 0.85)

# sun: disc + 8 rotating rays
an, layer = new_anim()
sun = layer.add_shape(objects.Group())
core = sun.add_shape(objects.Group())
ellipse(core, 50, 50, 34, 34, GOLD)
rays = sun.add_shape(objects.Group())
rays.transform.anchor_point.value = Point(50, 50)
rays.transform.position.value = Point(50, 50)
for i in range(8):
    a = i * math.pi / 4
    rect(rays, 50 + 27 * math.cos(a), 50 + 27 * math.sin(a), 4, 12, 2, GOLD)
    # rotate each ray rect via its own group? keep simple bars radial:
rays.transform.rotation.add_keyframe(0, 0)
rays.transform.rotation.add_keyframe(FRAMES, 360)
json.dump(an.to_dict(), open("assets/icon_sun.json", "w"))

# rain cloud: cloud + 3 falling drops looping
an, layer = new_anim()
for i, (dx, delay) in enumerate([(-14, 0), (0, 30), (14, 60)]):
    drop = layer.add_shape(objects.Group())
    ellipse(drop, 50 + dx, 0, 6, 10, BLUE)
    for f in range(0, FRAMES + 1, 10):
        ph = ((f + delay) % FRAMES) / FRAMES
        drop.transform.position.add_keyframe(f, Point(0, 55 + ph * 35))
cloud = layer.add_shape(objects.Group())
ellipse(cloud, 38, 42, 34, 26, CLOUD)
ellipse(cloud, 60, 38, 40, 32, CLOUD)
ellipse(cloud, 50, 48, 60, 24, CLOUD)
json.dump(an.to_dict(), open("assets/icon_rain.json", "w"))

# moon: crescent + twinkling star
an, layer = new_anim()
star = layer.add_shape(objects.Group())
star.transform.anchor_point.value = Point(74, 30)
star.transform.position.value = Point(74, 30)
ellipse(star, 74, 30, 8, 8, PALE)
for f in range(0, FRAMES + 1, 15):
    s = 100 if (f // 15) % 2 else 40
    star.transform.scale.add_keyframe(f, Point(s, s))
shadow = layer.add_shape(objects.Group())
ellipse(shadow, 58, 44, 30, 30, Color(0.13, 0.16, 0.25))
moon = layer.add_shape(objects.Group())
ellipse(moon, 48, 50, 36, 36, PALE)
json.dump(an.to_dict(), open("assets/icon_moon.json", "w"))

print("wrote weather icons")
