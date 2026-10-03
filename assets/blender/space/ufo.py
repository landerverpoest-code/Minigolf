import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from mglib import *
from mgx import *
reset()
hull = mat('hull', '#d5dbe4', rough=0.3, metal=0.55)
navy = mat('navy', '#1e2a48', rough=0.5)
glass = mat('glass_dome', '#bff4ff', rough=0.05, metal=0.0, alpha=0.3)
glow = mat('glow_lights', '#ff40d8', rough=0.3, emit='#ff2ad8', emit_strength=1.8)
alien = mat('alien_skin', '#7ed957', rough=0.5)
V = Vector
P = []
# schotel
sau = lathe([(0.0, -0.12), (0.55, -0.08), (1.2, 0.08), (1.75, 0.3), (2.02, 0.5), (2.0, 0.6), (1.65, 0.82), (1.25, 1.02), (0.95, 1.1)],
            seg=24, material=hull, smooth=True, cap_top=True)
shade_smooth(sau, 40)
set_mat(sau, navy, lambda c, n: math.hypot(c.x, c.y) < 0.6 and c.z < 0.0)
P.append(sau)
P.append(torus(2.0, 0.07, loc=(0, 0, 0.55), seg=24, ring=4, material=navy, smooth=False))
# lichtjes rond de rand
for k in range(12):
    a = k * TAU / 12
    P.append(ico(0.13, loc=(2.05 * math.cos(a), 2.05 * math.sin(a), 0.55), sub=1, material=glow, smooth=True))
# panelen bovenop
P.append(lathe([(1.5, 0.86), (1.52, 0.9), (1.38, 0.97), (1.36, 0.93)], seg=24, material=navy, cap_top=False, cap_bot=False))
for k in range(8):
    a = k * TAU / 8 + TAU / 16
    P.append(place_on(cyl(0.09, 0.04, verts=6, material=glow), sau, (math.cos(a), math.sin(a), 0.55), center=(0, 0, 0.6)))
# onderkant: gloeiende straalring + pootjes
P.append(lathe([(0.45, 0.01), (0.3, -0.06), (0.0, -0.08)], seg=12, material=glow, cap_top=False))
for k in range(3):
    a = k * TAU / 3 + 0.3
    P.append(tube([V((0.9 * math.cos(a), 0.9 * math.sin(a), 0.12)), V((1.15 * math.cos(a), 1.15 * math.sin(a), -0.15))], r=0.04, seg=4, material=navy, smooth=False))
    P.append(cyl(0.12, 0.04, loc=(1.17 * math.cos(a), 1.17 * math.sin(a), -0.17), verts=6, material=navy))
# koepel (glas) met klein alientje
dome = lathe([(0.92, 1.1), (0.88, 1.45), (0.72, 1.77), (0.42, 2.0), (0.0, 2.08)], seg=16, material=glass, smooth=True, cap_bot=False)
P.append(dome)
P.append(cyl(0.97, 0.1, loc=(0, 0, 1.12), verts=16, material=navy))
AL = []
AL.append(sphere(0.24, loc=(0, -0.05, 1.42), seg=10, rings=7, material=alien, scale=(1.0, 0.9, 1.12)))
AL.append(cyl(0.12, 0.35, loc=(0, -0.0, 1.12), verts=8, r2=0.08, material=alien))
for sx in (-1, 1):
    e = sphere(0.075, loc=(sx * 0.1, -0.24, 1.46), seg=8, rings=5, material=navy, scale=(1.0, 0.6, 1.35))
    T(e, rot=(0, sx * 0.35, 0), pivot=(sx * 0.1, -0.24, 1.46))
    AL.append(e)
    AL.append(tube([V((sx * 0.08, -0.02, 1.62)), V((sx * 0.16, 0.0, 1.75)), V((sx * 0.2, 0.02, 1.8))], r=[0.015, 0.012, 0.01], seg=3, material=alien, smooth=False))
    AL.append(ico(0.035, loc=(sx * 0.21, 0.02, 1.82), sub=1, material=glow, smooth=True))
al = join(AL, 'alien')
T(al, scale=1.3, pivot=(0, 0, 1.0), loc=(0, 0, 0.12))
P.append(al)
join(P, 'ufo')
report()
finish('space', 'ufo', kind='hero', footprint=2.1, notes='cartoon-vliegende schotel met glazen koepel en alientje; oorsprong onderaan (game laat hem zweven); glow_lights rond de rand + straalring')
