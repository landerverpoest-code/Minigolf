import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
white = mat('panel_white', '#eef1f5', rough=0.4)
navy = mat('navy', '#1e2a48', rough=0.5)
gold = mat('gold_foil', '#f0b04a', rough=0.35, metal=0.35)
grey = mat('metal_grey', '#9aa4b2', rough=0.4, metal=0.5)
glow = mat('glow', '#30d8f0', rough=0.3, emit='#22e0ff', emit_strength=1.6)
V = Vector
P = []
# 6 wielen (lengte langs X, voorkant = -X? nee: rijrichting -Y)
for sx in (-1, 1):
    for y in (-0.62, 0.0, 0.62):
        P.append(cyl(0.21, 0.16, loc=(sx * 0.62, y, 0.21), rot=(0, math.pi / 2, 0), verts=8, material=navy))
        P.append(cyl(0.1, 0.18, loc=(sx * 0.62, y, 0.21), rot=(0, math.pi / 2, 0), verts=5, material=grey))
    # rocker-bogie armen
    P.append(tube([V((sx * 0.5, -0.62, 0.21)), V((sx * 0.5, -0.3, 0.45)), V((sx * 0.5, 0.15, 0.42)), V((sx * 0.5, 0.0, 0.21))], r=0.035, seg=3, material=grey, smooth=False))
    P.append(tube([V((sx * 0.5, 0.0, 0.21)), V((sx * 0.5, 0.35, 0.4)), V((sx * 0.5, 0.62, 0.21))], r=0.035, seg=3, material=grey, smooth=False))
    P.append(cyl(0.06, 0.08, loc=(sx * 0.46, 0.0, 0.43), rot=(0, math.pi / 2, 0), verts=6, material=gold))
# romp
P.append(box((0.84, 1.45, 0.3), loc=(0, 0, 0.58), material=white, bevel=0.04))
P.append(box((0.8, 1.35, 0.1), loc=(0, 0, 0.4), material=gold))
P.append(box((0.6, 0.05, 0.12), loc=(0, -0.735, 0.6), material=navy))
for x in (-0.18, 0.18):
    P.append(box((0.1, 0.03, 0.07), loc=(x, -0.76, 0.6), material=glow))
# zonnepaneel op het dek
P.append(box((0.9, 0.95, 0.04), loc=(0, 0.2, 0.76), material=grey))
for i in range(2):
    for j in range(3):
        P.append(box((0.4, 0.28, 0.03), loc=(-0.215 + i * 0.43, 0.2 - 0.31 + j * 0.31, 0.785), material=navy))
# mast met camerakop
P.append(cyl(0.035, 0.55, loc=(0.22, -0.5, 1.0), verts=6, material=grey))
cam = box((0.3, 0.14, 0.14), loc=(0.22, -0.52, 1.32), material=white, bevel=0.02)
P.append(cam)
for x in (0.14, 0.3):
    P.append(cyl(0.035, 0.04, loc=(x, -0.6, 1.32), rot=(math.pi / 2, 0, 0), verts=6, material=glow))
# antenne + schoteltje
P.append(cyl(0.015, 0.7, loc=(-0.3, 0.55, 1.1), verts=4, material=grey))
P.append(ico(0.03, loc=(-0.3, 0.55, 1.47), sub=1, material=glow))
d = lathe([(0.0, 0.0), (0.12, 0.02), (0.18, 0.07), (0.0, 0.01)], seg=8, material=white, cap_top=False)
T(d, rot=(math.radians(-50), 0, 0.5), loc=(-0.25, -0.45, 0.9))
P.append(d)
P.append(cyl(0.02, 0.15, loc=(-0.25, -0.45, 0.83), verts=4, material=grey))
# RTG achteraan
P.append(cyl(0.11, 0.3, loc=(0, 0.82, 0.62), rot=(math.radians(-30), 0, 0), verts=6, material=gold))
join(P, 'rover')
report()
finish('space', 'rover', kind='scatter', footprint=0.85, notes='zeswielige maanrover (rijrichting -Y) met rocker-bogie, zonnepaneel, camerakop (glow-ogen) en antenne')
