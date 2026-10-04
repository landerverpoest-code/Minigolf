import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/volcano'); from _deco import *

BASALT = mat('basalt', '#3a322e', rough=0.9)
STEM = mat('char_stem', '#4a2a22', rough=0.8)
LEAF = mat('ash_leaf', '#5a3a2c', rough=0.85)
GLOW = mat('glow_lava', '#ff6a00', rough=0.45, emit='#ff4800', emit_strength=3.0)
HOT = mat('glow_lava_hot', '#ffd040', rough=0.4, emit='#ffb020', emit_strength=3.5)

rnd = random.Random(3)
# basaltvoetje
base = chunk(0.16, (1.3, 1.1, 0.5), cuts=6, seed=8, material=BASALT, flat_bottom=0.3, base_sub=1)
T(base, loc=(0, 0, 0.02))
# stengels met gloeiende bloesems (bekervormig, puntige blaadjes)
heads = [((0.0, 0.0), (0.03, -0.04, 0.46), 0.075), ((0.08, 0.05), (0.2, 0.08, 0.36), 0.062),
         ((-0.07, 0.03), (-0.19, 0.06, 0.32), 0.06), ((0.02, -0.07), (0.07, -0.2, 0.24), 0.052)]
for (bx, by), tp, R in heads:
    tp = Vector(tp); b = Vector((bx, by, 0.06))
    mid = b.lerp(tp, 0.5) + Vector((0, 0, 0.03))
    tube([b, mid, tp], [0.014, 0.011, 0.009], verts=3, material=STEM, cap0=False)
    # kelk: buitenste ring gloeiend oranje, binnenste hart heetgeel
    f = flower_head(R=R, rc=R * 0.35, petals=5, cup=R * 0.7, petal_mat=GLOW, heart_mat=HOT, wide=0.95)
    f2 = flower_head(R=R * 0.6, rc=R * 0.2, petals=5, cup=R * 0.6, petal_mat=HOT, wide=0.9)
    T(f2, rot=(0, 0, 36), loc=(0, 0, 0.004))
    for o in (f, f2):
        orient(o, Vector((tp.x * 1.5, tp.y * 1.5, 1)), tp)
# donkere puntige bladeren
for i in range(5):
    a = TAU * i / 5 + 0.4
    leaf((math.cos(a) * 0.05, math.sin(a) * 0.05, 0.07), Vector((math.cos(a), math.sin(a), 0.6)), length=0.17, width=0.04,
         curl=0.06, fold=0.015, material=LEAF, segs=2)
join_all('fire_flowers')
report()
done('volcano', 'fire_flowers', kind='edge', footprint=0.22,
     notes='Vuurbloemen: vier gloeiende lavabloesems (glow_lava/glow_lava_hot) met dubbele kelk op donkere stengels, puntige asbladeren, basaltvoetje')
