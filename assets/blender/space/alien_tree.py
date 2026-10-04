import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/space'); from _deco import *

STALK = mat('alien_stalk', '#5b3fa0', rough=0.6)
LEAF = mat('alien_leaf', '#22a69a', rough=0.6)
ROCK = mat('alien_rock', '#343a58', rough=0.9)
BULB = mat('glow_bulb', '#d020b8', rough=0.3, emit='#ff3ae0', emit_strength=1.2)
CYAN = mat('glow_crystal_cyan', '#1590b0', rough=0.15, emit='#22d8f8', emit_strength=1.1)

rnd = random.Random(12)
# --- gedraaide, geribde stam die zich splitst in drie bochtige armen
trunk = [Vector(p) for p in ((0, 0, 0), (0.05, 0.0, 0.7), (-0.05, 0.05, 1.4), (0.0, 0.0, 1.9))]
tube(trunk, [0.32, 0.22, 0.18, 0.16], verts=7, material=STALK, smooth=True, twist=0.4)
# wortelknollen
for k in range(4):
    a = k * TAU / 4 + 0.4
    d = Vector((math.cos(a), math.sin(a), 0))
    tube([d * 0.1 + Vector((0, 0, 0.3)), d * 0.45 + Vector((0, 0, 0.06)), d * 0.65 + Vector((0, 0, -0.02))], [0.13, 0.08, 0.0], verts=5, material=STALK, smooth=True)
tops = []
for k, (a, L, rise) in enumerate(((0.3, 1.0, 1.0), (2.4, 1.1, 0.8), (4.3, 0.9, 1.25))):
    d = Vector((math.cos(a), math.sin(a), 0))
    p0 = Vector((0, 0, 1.85))
    p1 = p0 + d * L * 0.5 + Vector((0, 0, rise * 0.55))
    p2 = p0 + d * L + Vector((0, 0, rise * 0.75))
    p3 = p0 + d * L * 1.15 + Vector((0, 0, rise * 0.65))
    tube([p0, p1, p2, p3], [0.13, 0.1, 0.08, 0.06], verts=5, material=STALK, smooth=True)
    tops.append((p3, d))
# --- bolle gloeiende vruchten / kronen aan de uiteinden: paddenstoelachtige hoed + hangende bol
for k, (p, d) in enumerate(tops):
    cap = lathe([(0.0, -0.05), (0.5, 0.0), (0.55, 0.08), (0.42, 0.22), (0.2, 0.32), (0.0, 0.35)], verts=8, material=LEAF, smooth=True)
    recolor(cap, [LEAF, CYAN], lambda f: 1 if f.normal.z < -0.3 else None)
    T(cap, scale=0.8 + 0.15 * k, loc=p + Vector((0, 0, 0.02)))
    # stippen op de hoed
    for j in range(4):
        a = j * TAU / 4 + k
        sphere(0.06, loc=p + Vector((0.28 * math.cos(a), 0.28 * math.sin(a), 0.22 * (0.8 + 0.15 * k))), seg=5, rings=3, material=BULB)
    # hangende gloeibol
    q = p - Vector((0, 0, 0.32)) + d * 0.08
    rod(p, q, r=0.02, verts=3, material=STALK)
    sphere(0.12, loc=q - Vector((0, 0, 0.08)), seg=6, rings=4, material=BULB, scale=(1, 1, 1.25))
# --- kleine bolletjes langs de stam
for k, z in enumerate((0.6, 1.1, 1.5)):
    a = k * 2.2
    sphere(0.07, loc=(0.2 * math.cos(a), 0.2 * math.sin(a), z), seg=5, rings=3, material=CYAN)
o = join_all('alien_tree')
report()
done('space', 'alien_tree', kind='scatter', footprint=0.7,
     notes='Buitenaardse boom: gedraaide paarse stam met wortelknollen die zich splitst in drie armen met turquoise paddenstoelhoeden (gloeiende cyaan onderkant), magenta gloeistippen en hangende gloeibollen (glow_bulb, glow_crystal_cyan)')
