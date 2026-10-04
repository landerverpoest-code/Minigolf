import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/space'); from _deco import *

FOIL = mat('gold_foil', '#f0b04a', rough=0.35, metal=0.35)
CELL = mat('solar_cell', '#1d3f8f', rough=0.2, metal=0.4)
GREY = mat('metal_grey', '#9aa4b2', rough=0.4, metal=0.5)
DUST = mat('moon_dust', '#7a7c86', rough=1.0)
GLOW = mat('glow_beacon', '#ff40c8', rough=0.3, emit='#ff2ab8', emit_strength=2.5)

rnd = random.Random(3)
# krater met opgeworpen rand
crater = lathe([(1.3, 0.0), (1.05, 0.12), (0.85, 0.16), (0.65, 0.08), (0.3, 0.03), (0.0, 0.03)], verts=12, material=DUST, jitter=0.07, seed=2, sx=1.1)
flat(crater)
CRATER_RIM = crater
# brokken rond de krater
for k in range(4):
    a = k * TAU / 4 + 0.5
    c = chunk(0.1 + 0.04 * (k % 2), (1.3, 1.0, 0.8), cuts=4, seed=20 + k, material=DUST, flat_bottom=0.3, base_sub=1)
    T(c, loc=(1.25 * math.cos(a) * 1.1, 1.25 * math.sin(a), 0.03))
sat = []
# romp: achthoekige trommel met goudfolie en ringen
body = lathe([(0.0, -0.45), (0.32, -0.45), (0.35, -0.4), (0.35, 0.4), (0.32, 0.45), (0.0, 0.45)], verts=8, material=FOIL, phase=math.pi / 8)
sat.append(body)
for z in (-0.25, 0.25):
    sat.append(lathe([(0.37, z - 0.03), (0.37, z + 0.03)], verts=8, material=GREY, phase=math.pi / 8, cap0=False, cap1=False))
# schoteltje bovenop
dish = lathe([(0.05, 0.0), (0.3, 0.1), (0.32, 0.14), (0.0, 0.05)], verts=10, material=GREY)
T(dish, loc=(0, 0, 0.5)); sat.append(dish)
sat.append(rod((0, 0, 0.45), (0, 0, 0.75), r=0.02, verts=4, material=GREY))
sat.append(sphere(0.04, loc=(0, 0, 0.77), seg=5, rings=3, material=GLOW))
# één heel zonnepaneel, één afgebroken
def panel(n, x0, dirn):
    P = [rod((dirn * 0.35, 0, 0), (dirn * (x0 + 0.05), 0, 0), r=0.025, verts=4, material=GREY)]
    for i in range(n):
        x = dirn * (x0 + 0.1 + i * 0.42 + 0.2)
        P.append(box((0.4, 0.035, 0.6), loc=(x, 0, 0), material=CELL))
        P.append(box((0.42, 0.04, 0.03), loc=(x, 0, 0.3), material=GREY))
        P.append(box((0.42, 0.04, 0.03), loc=(x, 0, -0.3), material=GREY))
        P.append(box((0.02, 0.04, 0.6), loc=(x + 0.2, 0, 0), material=GREY))
    return P
sat += panel(3, 0.4, 1)
sat += panel(1, 0.4, -1)
# afgescheurde kabeltjes
for k in range(3):
    sat.append(tube([(-0.95, 0.0, 0.1 * k - 0.1), (-1.05, 0.05 * k, 0.1 * k - 0.15), (-1.12, -0.05, 0.1 * k - 0.05)], 0.01, verts=3, material=GREY, cap0=False, cap1=False))
s = join(sat, 'sat')
# schuin in de krater geboord
T(s, rot=(20, -28, 15), loc=(0, 0, 0.42))
clip_below(s, 0.04)
fix_normals(s)
# afgebroken paneel ligt los in het stof
lose = []
lose.append(box((0.4, 0.6, 0.035), loc=(0, 0, 0), material=CELL))
lose.append(box((0.03, 0.62, 0.04), loc=(0.2, 0, 0), material=GREY))
lose.append(box((0.03, 0.62, 0.04), loc=(-0.2, 0, 0), material=GREY))
lp = join(lose, 'loose')
T(lp, rot=(8, -5, 35), loc=(-1.0, 0.75, 0.12))
# rookpluimpje / vonkjes
for k in range(3):
    sphere(0.08 - 0.02 * k, loc=(0.25 + 0.05 * k, -0.1, 0.95 + 0.18 * k), seg=5, rings=3, material=DUST)
o = join_all('crashed_satellite')
report()
done('space', 'crashed_satellite', kind='scatter', footprint=1.4, center=True,
     notes='Neergestorte satelliet schuin in een krater: achthoekige goudfolie-romp met ringen, schoteltje en knipperend antennelampje (glow_beacon), één heel zonnepaneel van drie vakken en een afgebroken stomp met kabeltjes, los paneel in het stof, brokstukken en rookwolkjes')
