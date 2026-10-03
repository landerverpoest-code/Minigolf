import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice')
from mglib import *
reset()
from _kit import *

WOOD = mat('sled_wood', '#c08850', rough=0.75)
WOOD2 = mat('sled_wood_dark', '#93633a', rough=0.75)
RED = mat('sled_red', '#d8323a', rough=0.45, metal=0.1)
ROPE = mat('rope', '#e8d6a8', rough=0.9)
SNOW = mat('snow', '#f2f7ff', rough=0.7)

L = 1.0; W = 0.44; H = 0.22
# latten
for i in range(5):
    y = -W / 2 + 0.05 + i * (W - 0.1) / 4
    box((L * 0.86, 0.075, 0.025), loc=(-0.03, y, H), material=WOOD if i % 2 == 0 else WOOD2)
for x in (-0.36, 0.3):
    box((0.06, W + 0.04, 0.035), loc=(x, 0, H - 0.03), material=WOOD2)
# glijders (rood, gekruld aan de voorkant)
for s in (-1, 1):
    y = s * (W / 2 + 0.01)
    pts = [(-0.5, y, 0.03), (-0.2, y, 0.015), (0.25, y, 0.015), (0.45, y, 0.05), (0.55, y, 0.15), (0.53, y, 0.25), (0.45, y, 0.28), (0.4, y, 0.22)]
    tube(pts, [0.022] * len(pts), verts=4, material=RED, squash=(1.0, 0.7))
    for x in (-0.36, 0.3):
        box((0.035, 0.03, H - 0.06), loc=(x, y * 0.98, (H - 0.03) / 2 + 0.005), material=RED)
# touw
rope = tube([(0.47, -W / 2, 0.24), (0.62, -0.12, 0.12), (0.72, 0.0, 0.02), (0.62, 0.12, 0.02), (0.47, W / 2, 0.24)],
            [0.012] * 5, verts=3, material=ROPE)
# sneeuwplukje op het zitvlak
s = rock(0.08, loc=(-0.2, 0.05, H + 0.02), scale=(1.5, 1.2, 0.5), seed=2, jitter=0.1, material=SNOW)
join_all('sled')
report()
finish('ice', 'sled', kind='edge', footprint=0.55, notes='Houten slee met rode gekrulde glijders, touw en een plukje sneeuw')
closeup('sled')
