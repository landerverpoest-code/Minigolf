import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
white = mat('panel_white', '#e9edf2', rough=0.45)
grey = mat('metal_grey', '#9aa4b2', rough=0.4, metal=0.5)
navy = mat('navy', '#1e2a48', rough=0.55)
gold = mat('gold_foil', '#f0b04a', rough=0.35, metal=0.35)
cell = mat('solar_cell', '#1d3f8f', rough=0.2, metal=0.4)
V = Vector
P = []
P.append(box((0.7, 0.7, 0.18), loc=(0, 0, 0.09), material=grey, bevel=0.025))
P.append(cyl(0.12, 1.9, loc=(0, 0, 1.1), verts=8, material=white))
P.append(cyl(0.16, 0.14, loc=(0, 0, 0.6), verts=8, material=navy))
P.append(box((0.36, 0.36, 0.32), loc=(0, 0, 2.15), material=white, bevel=0.03))
P.append(box((0.3, 0.02, 0.18), loc=(0, -0.18, 2.15), material=gold))
P.append(cyl(0.06, 3.4, loc=(0, 0, 2.2), rot=(0, math.pi / 2, 0), verts=6, material=grey))
tilt = math.radians(32)
for sx in (-1, 1):
    W = []
    cx = sx * 0.95
    W.append(box((1.45, 1.05, 0.04), loc=(cx, 0, 0), material=white))
    nx, ny = 4, 3
    for i in range(nx):
        for j in range(ny):
            x = cx - 0.69 + (i + 0.5) * 1.38 / nx
            y = -0.49 + (j + 0.5) * 0.98 / ny
            W.append(box((1.38 / nx - 0.04, 0.98 / ny - 0.04, 0.03), loc=(x, y, 0.025), material=cell))
    W.append(box((1.45, 0.06, 0.06), loc=(cx, 0.0, -0.04), material=grey))
    w = join(W, 'wing')
    T(w, rot=(tilt, 0, 0), loc=(0, 0, 2.2))
    P.append(w)
P.append(cyl(0.1, 0.12, loc=(1.72, 0, 2.2), rot=(0, math.pi / 2, 0), verts=6, material=navy))
P.append(cyl(0.1, 0.12, loc=(-1.72, 0, 2.2), rot=(0, math.pi / 2, 0), verts=6, material=navy))
join(P, 'solar_array')
report()
finish('space', 'solar_array', kind='scatter', footprint=0.45, notes='zonnepaneel-vleugels op een paal; cellen als losse geometrie (rasterlijnen = frame)')
