import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/water')
from mglib import *
reset()
from _kit import *

CORAL = mat('beach_coral', '#f2674e', rough=0.6)
WHITE = mat('beach_white', '#fbf7ee', rough=0.6)
TURQ = mat('beach_turq', '#22b6c6', rough=0.6)
WOOD = mat('beach_wood', '#c18d55', rough=0.75)
YEL = mat('beach_yellow', '#ffcf3a', rough=0.6)

# --- parasol ---
UX, UY = 0.15, 0.25
pole = cyl(0.025, 1.85, loc=(UX, UY, 0.92), verts=6, material=WHITE)
tilt = (0.12, -0.1, 0)
prof = [(0.0, 1.95), (0.5, 1.82), (0.92, 1.6), (0.9, 1.54)]
can = lathe(prof, verts=10, material=CORAL, cap0=False, cap1=False)
can.data.materials.append(WHITE)
for p in can.data.polygons:
    a = math.atan2(p.center.y, p.center.x)
    p.material_index = int(((a + math.pi) / (2 * math.pi)) * 10) % 2
fin = sphere(0.045, loc=(0, 0, 1.98), seg=6, rings=4, material=WHITE)
cp = join([can, fin], 'canopy')
place(cp, loc=(UX, UY, 0), rot=tilt)
# --- ligstoel (strandstoel) ---
CX, CY = 0.2, -0.35
fr = []
for s in (-1, 1):
    x = CX + s * 0.26
    fr.append(tube([(x, CY - 0.45, 0.0), (x, CY - 0.45, 0.3), (x, CY + 0.35, 0.3), (x, CY + 0.62, 0.85)], [0.025] * 4, verts=4, material=WOOD))
    fr.append(tube([(x, CY + 0.25, 0.0), (x, CY + 0.25, 0.3)], [0.025] * 2, verts=4, material=WOOD))
fr.append(cyl(0.02, 0.56, loc=(CX, CY - 0.45, 0.3), rot=(0, math.pi / 2, 0), verts=4, material=WOOD))
fr.append(cyl(0.02, 0.56, loc=(CX, CY + 0.62, 0.85), rot=(0, math.pi / 2, 0), verts=4, material=WOOD))
# doek in strepen
def seat(u, v):
    # v: 0 voor -> 1 boven rugleuning; u: links->rechts
    y = CY - 0.42 + v * 1.0
    z = 0.3 + max(0, v - 0.75) * 2.1 - math.sin(math.pi * min(v / 0.8, 1)) * 0.07
    if v > 0.75: y = CY + 0.33 + (v - 0.75) / 0.25 * 0.27
    return Vector((CX - 0.24 + u * 0.48, y, z + 0.01))
sh = grid_sheet(seat, 3, 6, material=TURQ, name='seat')
sh.data.materials.append(WHITE)
for i, p in enumerate(sh.data.polygons):
    p.material_index = (i % 3) % 2
# --- handdoek ---
TX, TY = -0.55, -0.15
def towel(u, v):
    return Vector((TX - 0.32 + u * 0.64, TY - 0.7 + v * 1.4, 0.012 + (0.02 if v > 0.88 else 0)))
tw = grid_sheet(towel, 1, 7, material=YEL, name='towel')
tw.data.materials.append(WHITE)
for i, p in enumerate(tw.data.polygons):
    p.material_index = i % 2
tw2 = box((0.64, 0.18, 0.05), loc=(TX, TY + 0.62, 0.03), material=YEL, bevel=0.02)   # opgerold kussen
# --- strandbal ---
ball = sphere(0.14, loc=(-0.45, 0.55, 0.14), seg=6, rings=4, material=CORAL)
ball.data.materials.append(WHITE); ball.data.materials.append(TURQ)
for p in ball.data.polygons:
    a = math.atan2(p.center.y - 0.55, p.center.x + 0.45)
    p.material_index = int(((a + math.pi) / (2 * math.pi)) * 6) % 3
join_all('beach_set')
report()
finish('water', 'beach_set', kind='scatter', footprint=0.9,
       notes='Gestreepte parasol, houten strandstoel, handdoek en strandbal')
closeup('beach_set')
