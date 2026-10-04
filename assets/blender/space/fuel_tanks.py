import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/space'); from _deco import *

WHITE = mat('panel_white', '#eef1f5', rough=0.4)
GREY = mat('metal_grey', '#9aa4b2', rough=0.4, metal=0.5)
NAVY = mat('navy', '#1e2a48', rough=0.5)
ORANGE = mat('fuel_orange', '#f08a24', rough=0.45)
GLOW = mat('glow', '#30d8f0', rough=0.3, emit='#22e0ff', emit_strength=1.6)

# betonnen plaat
box((2.4, 1.6, 0.1), loc=(0, 0, 0.05), material=GREY, bevel=0.02)
# twee liggende tanks op zadels + één staande bol-tank
def tank(x, y, L, R, mat_band):
    t = lathe([(0.0, -L / 2 - R * 0.45), (R * 0.72, -L / 2 - R * 0.3), (R * 1.03, -L / 2), (R * 1.03, -L / 2 + 0.12), (R, -L / 2 + 0.13),
               (R, L / 2 - 0.13), (R * 1.03, L / 2 - 0.12), (R * 1.03, L / 2), (R * 0.72, L / 2 + R * 0.3), (0.0, L / 2 + R * 0.45)],
              verts=9, mats=[WHITE, mat_band], band_mats=[0, 0, 1, 0, 0, 0, 1, 0, 0], smooth=40)
    T(t, rot=(0, 90, 0), loc=(x, y, 0.1 + R + 0.12))
    for sx in (-L / 2 + 0.25, L / 2 - 0.25):
        prism([(-R * 0.75, 0), (R * 0.75, 0), (R * 0.75, R * 0.5), (-R * 0.75, R * 0.5)], 0.1, material=NAVY, axis='X', loc=(x + sx, y, 0.1))
    # kleppen en meter bovenop
    cyl(0.06, 0.12, loc=(x - L * 0.2, y, 0.1 + 2 * R + 0.15), verts=6, material=GREY)
    cyl(0.1, 0.03, loc=(x - L * 0.2, y, 0.1 + 2 * R + 0.22), verts=6, material=ORANGE)
    cyl(0.07, 0.03, loc=(x + L * 0.15, y - R * 0.6, 0.1 + R * 1.8), rot=(0.9, 0, 0), verts=8, material=GLOW)
    return t
tank(-0.15, -0.38, 1.6, 0.3, ORANGE)
tank(-0.15, 0.35, 1.6, 0.3, NAVY)
# staande bol-tank met poten
S = Vector((0.85, 0.0, 0.0))
sphere(0.38, loc=S + Vector((0, 0, 0.95)), seg=9, rings=6, material=WHITE)
torus(0.385, 0.03, loc=S + Vector((0, 0, 0.95)), seg=9, ring=3, material=ORANGE)
for k in range(4):
    a = k * TAU / 4 + math.pi / 4
    rod(S + Vector((0.4 * math.cos(a), 0.4 * math.sin(a), 0.1)), S + Vector((0.3 * math.cos(a), 0.3 * math.sin(a), 0.85)), r=0.035, verts=4, material=GREY)
cyl(0.05, 0.12, loc=S + Vector((0, 0, 1.38)), verts=6, material=GREY)
sphere(0.05, loc=S + Vector((0, 0, 1.47)), seg=6, rings=4, material=GLOW)
# leidingen tussen de tanks
tube([(-0.15 + 0.8 + 0.12, -0.38, 0.6), (0.55, -0.3, 0.5), (0.6, -0.15, 0.65), (0.6, 0, 0.75)], 0.035, verts=4, material=GREY, smooth=True)
tube([(-0.15 + 0.8 + 0.12, 0.35, 0.6), (0.55, 0.3, 0.45), (0.6, 0.15, 0.6)], 0.035, verts=4, material=GREY, smooth=True)
# brandstofslang met vulpistool
tube([(-1.1, -0.38, 0.42), (-1.25, -0.5, 0.25), (-1.2, -0.75, 0.12), (-0.95, -0.85, 0.13)], 0.03, verts=4, material=NAVY, smooth=True)
box((0.12, 0.05, 0.08), loc=(-0.9, -0.85, 0.14), material=ORANGE)
# waarschuwingsstrepen op de plaatrand
for k in range(4):
    box((0.12, 0.02, 0.05), loc=(-0.9 + k * 0.6, -0.805, 0.08), rot=(0, 0.6, 0), material=ORANGE)
o = join_all('fuel_tanks')
report()
done('space', 'fuel_tanks', kind='scatter', footprint=1.3,
     notes='Brandstofdepot: twee liggende witte tanks met oranje/navy banden op zadels, kleppen en gloeiende meters, staande bol-tank op vier poten met gloeiend lampje, verbindingsleidingen, slang met vulpistool, betonplaat met waarschuwingsstrepen')
