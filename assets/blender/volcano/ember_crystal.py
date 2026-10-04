import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/volcano'); from _deco import *

BASALT = mat('basalt', '#3a322e', rough=0.9)
BASALT_L = mat('basalt_light', '#5a4b43', rough=0.85)
EMBER = mat('glow_ember', '#ff7a18', rough=0.2, emit='#ff4a00', emit_strength=1.3)
HOT = mat('glow_ember_hot', '#ffc040', rough=0.2, emit='#ff9010', emit_strength=1.5)
CORE = mat('ember_core', '#8a2a10', rough=0.3)

rnd = random.Random(21)
# rotsvoet met kleinere brokken
base = chunk(0.4, (1.25, 1.1, 0.7), cuts=9, seed=4, material=BASALT, flat_bottom=0.35, base_sub=1)
T(base, loc=(0, 0, 0.05))
for k, (x, y, s) in enumerate(((0.52, 0.25, 0.16), (-0.5, -0.2, 0.13), (0.3, -0.48, 0.1))):
    c = chunk(s, (1.2, 1.0, 0.7), cuts=5, seed=30 + k, material=BASALT_L, flat_bottom=0.3, base_sub=1)
    T(c, loc=(x, y, s * 0.2))


def crystal(p, h, r, rot, m, seg=6):
    c = lathe([(r * 0.85, -0.1), (r, h * 0.72), (r * 0.55, h * 0.88), (0, h)], verts=seg, material=m, cap0=True, phase=rnd.uniform(0, 1))
    # binnenste band donkerder rood (diepte-effect) op de onderste segmenten
    recolor(c, [m, CORE], lambda f: 1 if f.center.z < h * 0.12 else None)
    jitter(c, r * 0.08, seed=int(h * 100))
    return T(c, rot=(rot[0], rot[1], rnd.uniform(0, 360)), loc=p)


spec = [((0, 0, 0.2), 1.05, 0.13, (0, 0), EMBER), ((0.14, -0.06, 0.18), 0.72, 0.1, (16, 24), HOT),
        ((-0.15, 0.04, 0.18), 0.8, 0.1, (-10, -26), EMBER), ((0.04, 0.16, 0.16), 0.6, 0.085, (-28, 8), HOT),
        ((-0.05, -0.17, 0.16), 0.5, 0.08, (30, -12), EMBER), ((0.24, 0.12, 0.12), 0.4, 0.065, (-16, 44), EMBER),
        ((-0.26, -0.1, 0.12), 0.38, 0.06, (20, -46), HOT), ((0.12, -0.26, 0.1), 0.3, 0.05, (44, 20), HOT),
        ((-0.2, 0.22, 0.1), 0.34, 0.055, (-36, -30), EMBER)]
for p, h, r, rot, m in spec:
    crystal(p, h, r, rot, m)
# losse gloeiende scherfjes op de grond
for k in range(4):
    a = k * 1.7 + 0.3
    c = chunk(0.05, (1.5, 0.8, 0.6), cuts=3, seed=80 + k, material=HOT if k % 2 else EMBER, base_sub=1)
    T(c, rot=(0, 25, a * 50), loc=(0.62 * math.cos(a), 0.55 * math.sin(a), 0.02))
join_all('ember_crystal')
report()
done('volcano', 'ember_crystal', kind='scatter', footprint=0.7,
     notes='Gloeiende ambercristallen: cluster van oranje/heetgele zeskantige kristallen (glow_ember, glow_ember_hot) met donkerrode voet op een basaltrots, losse gloeiende scherfjes')
