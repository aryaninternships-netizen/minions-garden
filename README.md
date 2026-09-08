# Minions Garden

An interactive 3D flower garden: hibiscus, Jacob's lily, raat ki rani, lilies, sunflowers, white and black roses, and a leafy lawn. Three.js, no build step.

**Live:** https://minions-garden.vercel.app

## What's in it

- **75,000 tulips** in curved colour bands across a rolling field, each bloom
  with its own height, hue jitter and a filled inner cup (petals, throat,
  pistil and anthers — not hollow shells).
- **200,000 grass blades** bending on the GPU.
- **Three cameras** — a cinematic FPV drone reel (lane skim, rise-and-reveal,
  orbit, mountain sweep), a free-fly drone, and a third-person walk mode
  following a rigged character.
- **Pick tulips** by clicking; gather five and tie a bouquet.
- **Hand control** — hit ✋ Hands and fly the garden with webcam gestures:
  pinch one hand and drag to steer, pinch both and pull them apart to fly
  forward. Runs on MediaPipe HandLandmarker, entirely on-device.
- **Live time of day** driven by your real clock, plus sunrise/noon/sunset/
  night presets, and clear/rain weather with wet-looking petals.
- **Butterflies** — six hand-drawn species that wander, home in on real
  blooms, land and bask, and roost at dusk or in rain.
- **Trees** grown from botanical rules: Honda branching, golden-angle
  phyllotaxis, da Vinci's taper rule, drooping whorled conifer boughs, and
  multi-frequency wind so trunk, branch and leaf each sway at their own rate.

## Pages

| File | What |
|---|---|
| `index.html` | the 3D garden |
| `varieties.html` | Lottie cards for six tulip cultivars |

## Generators

Asset generators, run with Python 3.13 (needs `pillow` and `lottie`):

```bash
python3 gen_tulips.py       # tulip Lottie loops for the varieties page
python3 gen_butterflies.py  # butterfly wing atlas -> assets/butterflies.png
python3 gen_weather.py      # sun / rain / moon HUD icons
python3 gen_girl.py         # 2D walk cycle (superseded by the 3D model)
```

## Credits

- Character model: Quaternius "Animated Women Pack" (CC0) via poly.pizza
- `assets/girl_web.json`: LottieFiles, Muammar Faiq, Lottie Simple License
