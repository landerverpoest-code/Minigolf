import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale')
from mglib import *
from mgx import *
reset()
wood = mat('wood', '#8a5a34', rough=0.85)
purple = mat('royal_purple', '#5b2a86', rough=0.6)
gold = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
crimson = mat('crimson', '#b0213a', rough=0.6)
glow = mat('glow_fuse', '#ffb040', rough=0.4, emit='#ff8a1a', emit_strength=2.0)
V = Vector
P = []
P.append(box((0.7, 0.5, 0.32), loc=(0, 0, 0.16), material=wood))
for z in (0.06, 0.26):
    P.append(box((0.72, 0.52, 0.05), loc=(0, 0, z), material=purple))
# vuurwerkbuizen (gedraaid profiel met gekleurde band en puntdop)
tubes = [(-0.18, -0.08, 0.36, crimson), (0.04, -0.1, 0.46, purple), (-0.1, 0.12, 0.52, gold), (0.17, 0.1, 0.38, crimson)]
for (x, y, h, m) in tubes:
    t = lathe([(0.075, 0.0), (0.075, h - 0.09), (0.082, h - 0.03), (0.0, h + 0.07)], seg=6, material=m, loc=(x, y, 0.3), cap_bot=False)
    band = gold if m is not gold else crimson
    set_mat(t, band, lambda c, n, h=h: 0.3 + h - 0.09 < c.z < 0.3 + h - 0.03)
    P.append(t)
# twee raketten op stokjes
for (x, y, rz, m) in [(0.38, 0.0, 0.25, crimson), (-0.38, 0.05, -0.2, purple)]:
    r = [cyl(0.008, 0.6, loc=(0, 0, 0.3), verts=3, material=wood),
         lathe([(0.04, 0.51), (0.04, 0.73), (0.0, 0.84)], seg=5, material=m, cap_bot=True)]
    set_mat(r[1], gold, lambda c, n: c.z > 0.74)
    rr = join(r, 'rk'); T(rr, rot=(0, rz, 0), loc=(x, y, 0.15)); P.append(rr)
# lont met vonkje
P.append(tube([V((0.04, -0.1, 0.82)), V((0.07, -0.12, 0.88)), V((0.1, -0.1, 0.92))], r=0.008, seg=3, material=wood, smooth=False))
P.append(ico(0.03, loc=(0.105, -0.1, 0.93), sub=1, material=glow))
join(P, 'firework_rack')
report()
finish('finale', 'firework_rack', kind='edge', footprint=0.42, notes='houten krat met vuurwerkbuizen en twee raketten; brandend lontje = glow_fuse')
