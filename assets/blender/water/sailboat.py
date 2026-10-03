import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/water')
from mglib import *
reset()
from _kit import *

WHITE = mat('boat_white', '#f6f4ee', rough=0.5)
CORAL = mat('boat_coral', '#ef6a4c', rough=0.5)
WOOD = mat('boat_wood', '#b98450', rough=0.75)
TURQ = mat('boat_turq', '#27b8c4', rough=0.5)
SAIL = mat('sail', '#fffdf6', rough=0.85)

# --- romp (alleen boven de waterlijn; onderkant = waterlijn z=0) ---
# x: achter (-) naar voor (+); per station: (x, halve breedte waterlijn, halve breedte dek, dekhoogte)
st = [(-1.45, 0.42, 0.55, 0.48), (-1.0, 0.5, 0.62, 0.48), (-0.2, 0.52, 0.64, 0.5), (0.6, 0.42, 0.56, 0.55),
      (1.15, 0.22, 0.36, 0.62), (1.55, 0.0, 0.02, 0.7)]
secs = []
for x, ww, wd, h in st:
    xs = x + (0.08 if ww == 0 else 0)
    secs.append([(x, -ww, 0), (x, -(ww + wd) / 2 - 0.02, 0.16), (x, -wd, h), (x, wd, h), (x, (ww + wd) / 2 + 0.02, 0.16), (x, ww, 0)])
# band 0: onderste strook (coral), 1: wit, 2: dek, 3: wit, 4: coral, 5: bodem
hull = loft(secs, mats=[CORAL, WHITE, WOOD], band_mats=[0, 1, 2, 1, 0, 0], closed=True, cap0=True, cap1=False)
bev(hull, 0.02)
# reling-rand
for s in (-1, 1):
    pts = [(x, s * (wd + 0.015), h + 0.03) for x, ww, wd, h in st]
    tube(pts, [0.035] * len(pts), verts=4, material=WHITE, name='rail')
# kajuit
cab = box((0.9, 0.62, 0.28), loc=(-0.25, 0, 0.62), material=WHITE, bevel=0.05)
roof = box((1.0, 0.7, 0.07), loc=(-0.25, 0, 0.79), material=TURQ, bevel=0.025)
for s in (-1, 1):
    for xx in (-0.5, -0.05):
        box((0.22, 0.04, 0.1), loc=(xx, s * 0.31, 0.65), material=TURQ)
# mast + giek
MX = 0.25
mast = cyl(0.045, 3.75, loc=(MX, 0, 0.5 + 1.87), verts=6, material=WOOD)
boom = cyl(0.035, 1.75, loc=(MX - 0.85, 0, 1.0), rot=(0, math.pi / 2, 0), verts=6, material=WOOD)
# grootzeil (bol)
top = Vector((MX - 0.04, 0, 4.15)); tack = Vector((MX - 0.05, 0, 1.06)); clew = Vector((MX - 1.68, 0, 1.06))
def mainsail(u, v):
    # u: 0 = mast, 1 = achterlijk; v: 0 = onder, 1 = top
    luff = tack + (top - tack) * v
    leech = clew + (top - clew) * v
    p = luff + (leech - luff) * u
    bulge = math.sin(math.pi * u) * (1 - v) * 0.28 + math.sin(math.pi * u) * 0.05
    return p + Vector((0, bulge, 0))
ms = grid_sheet(mainsail, 3, 4, material=SAIL, name='mainsail')
shade_smooth(ms)
# fok
jt = Vector((MX + 0.02, 0, 3.6)); jb = Vector((1.45, 0, 0.75)); jc = Vector((MX + 0.2, 0, 0.95))
def jib(u, v):
    luff = jb + (jt - jb) * v
    leech = jc + (jt - jc) * v
    p = luff + (leech - luff) * u
    return p + Vector((0, math.sin(math.pi * u) * (1 - v) * 0.22, 0))
jb_ = grid_sheet(jib, 2, 3, material=SAIL, name='jib')
shade_smooth(jb_)
# vlaggetje
flag = mesh_obj([(MX, 0, 4.25), (MX, 0, 4.0), (MX - 0.42, 0.05, 4.1)], [(0, 1, 2)], CORAL, 'flag')
cone(0.06, 0.12, loc=(MX, 0, 4.3), verts=6, material=CORAL)
# roer
rud = box((0.28, 0.05, 0.4), loc=(-1.52, 0, 0.3), material=TURQ, bevel=0.02)
tiller = cyl(0.02, 0.5, loc=(-1.3, 0, 0.62), rot=(0, math.pi / 2 - 0.2, 0), verts=5, material=WOOD)
# reddingsboei op kajuit
torus(0.13, 0.045, loc=(-0.25, -0.36, 0.62), rot=(math.pi / 2, 0, 0), seg=10, ring=5, material=CORAL)
join_all('sailboat')
report()
finish('water', 'sailboat', kind='scatter', footprint=1.6,
       notes='Zeilbootje; romp afgesneden op de waterlijn (oorsprong = waterlijn, z=0 is wateroppervlak). Boeg naar +X')
closeup('sailboat')
