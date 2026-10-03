import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

wood = mat('wood_dark', '#5a3b23', rough=0.85)
blue = mat('banner_blue', '#2f58ad', rough=0.8)
red = mat('banner_red', '#c0392f', rough=0.8)
gold = mat('gold', '#e3b23c', rough=0.35, metal=0.4)
stone = mat('stone_warm', '#a69c8f', rough=0.9)

parts = []
parts.append(box((0.32, 0.32, 0.18), loc=(0, 0, 0.09), material=stone, bevel=0.03))
parts.append(rod((0, 0, 0.1), (0, 0, 2.45), 0.04, 0.035, verts=6, material=wood))
parts.append(ico(0.07, sub=1, loc=(0, 0, 2.5), material=gold, scale=(1, 1, 1.4)))
# dwarslat met gouden eindknopjes
parts.append(rod((-0.42, -0.04, 2.25), (0.42, -0.04, 2.25), 0.022, verts=5, material=wood))
for sx in (-1, 1):
    parts.append(ico(0.035, sub=1, loc=(sx * 0.44, -0.04, 2.25), material=gold))
# vaandel: golvend raster, dubbelzijdig, zwaluwstaart; middenbaan blauw
W, H = 0.72, 1.35
cols, rows = 6, 4
def wave(x, z):
    u, v = x / W + 0.5, -z / H
    return 0.05 * math.sin(u * math.pi * 1.5 + v * 2.0) * (0.3 + v)
vs, fs, mi = [], [], []
for j in range(rows + 1):
    for i in range(cols + 1):
        x = (i / cols - 0.5) * W
        z = -j / rows * H
        if j == rows:
            z += 0.3 * (1 - abs(i - cols / 2) / (cols / 2))   # V-inkeping (zwaluwstaart)
        vs.append((x, wave(x, z), z))
for j in range(rows):
    for i in range(cols):
        a = j * (cols + 1) + i
        fs.append((a, a + cols + 1, a + cols + 2, a + 1))
        mi.append(1 if i in (2, 3) else 0)
n = len(vs)
vs2 = [(x, y + 0.012, z) for (x, y, z) in vs]
fs2 = [tuple(reversed([k + n for k in f])) for f in fs]
ban = mesh_obj(vs + vs2, fs + fs2, red)
ban.data.materials.append(blue)
for k, p_ in enumerate(ban.data.polygons):
    p_.material_index = mi[k % len(fs)]
xform(ban, loc=(0, -0.05, 2.22))
parts.append(ban)
# gouden keper op beide zijden, volgt de golf
for yoff in (-0.012, 0.024):
    ch = prism([(-0.3, -0.85), (0, -0.55), (0.3, -0.85), (0.3, -0.7), (0, -0.4), (-0.3, -0.7)], 0.01, material=gold)
    bend(ch, lambda c: (c.x, c.y + wave(c.x, c.z), c.z))
    xform(ch, loc=(0, -0.05 + yoff, 2.22))
    parts.append(ch)
# gouden zoom bovenaan
parts.append(box((0.76, 0.05, 0.05), loc=(0, -0.045, 2.22), material=gold))
o = join(parts, 'banner_pole')
smooth(o, 40)
report()
finish('castle', 'banner_pole', kind='edge', footprint=0.25, notes='vaandelstok op stenen voetje met golvend rood vaandel (zwaluwstaart), blauwe baan en gouden keper, gouden knoppen')
