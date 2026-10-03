import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale')
from mglib import *
from mgx import *
reset()
purple = mat('royal_purple', '#5b2a86', rough=0.55)
gold = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
crimson = mat('crimson', '#b0213a', rough=0.7)
marble = mat('marble', '#efe9f2', rough=0.35)
V = Vector
P = []
SEG = {'a': (0, 1, 'h'), 'b': (1, 0.5, 'v'), 'c': (1, -0.5, 'v'), 'd': (0, -1, 'h'), 'e': (-1, -0.5, 'v'), 'f': (-1, 0.5, 'v'), 'g': (0, 0, 'h')}
DIG = {1: 'bc', 2: 'abged', 3: 'abgcd'}
def digit(n, cx, cz, y, s=0.22, m=None):
    out = []
    for k in DIG[n]:
        ux, uz, o = SEG[k]
        w, h = (s * 0.9, s * 0.2) if o == 'h' else (s * 0.2, s * 0.9)
        out.append(box((w, 0.05, h), loc=(cx + ux * s * 0.5, y, cz + uz * s), material=m))
    return out
# (x, hoogte, plaats, frontkleur)
blocks = [(0.0, 1.45, 1, gold), (-1.65, 0.95, 2, marble), (1.65, 0.6, 3, crimson)]
for (x, h, n, col) in blocks:
    P.append(box((1.6, 1.5, h), loc=(x, 0, h / 2), material=purple, bevel=0.04))
    P.append(box((1.68, 1.58, 0.08), loc=(x, 0, h - 0.02), material=gold))
    P.append(box((1.66, 1.56, 0.08), loc=(x, 0, 0.04), material=gold))
    zc = h - 0.33 if n == 1 else h * 0.5 + 0.03
    disc = cyl(0.25 if n != 1 else 0.24, 0.05, loc=(x, -0.77, zc), rot=(math.pi / 2, 0, 0), verts=12, material=col)
    P.append(disc)
    ring = torus(0.26, 0.03, loc=(x, -0.79, zc), rot=(math.pi / 2, 0, 0), seg=12, ring=3, material=gold, smooth=False)
    P.append(ring)
    P += digit(n, x, zc, -0.81, s=0.14, m=gold if col is crimson else purple)
# rode loper met traptreden naar plaats 1
for i in range(3):
    P.append(box((0.9, 0.4, 0.25 * (i + 1)), loc=(0, -0.95 - (2 - i) * 0.4, 0.25 * (i + 1) / 2), material=crimson))
P.append(box((0.9, 2.2, 0.03), loc=(0, -3.05, 0.015), material=crimson))
for sx in (-1, 1):
    P.append(box((0.05, 2.2, 0.035), loc=(sx * 0.45, -3.05, 0.018), material=gold))
# paaltjes met fluwelen koord langs de loper
for sx in (-1, 1):
    posts = [V((sx * 0.8, -2.2, 0)), V((sx * 0.8, -3.7, 0))]
    for p in posts:
        P.append(cyl(0.12, 0.05, loc=p + V((0, 0, 0.025)), verts=8, material=gold))
        P.append(cyl(0.03, 0.85, loc=p + V((0, 0, 0.45)), verts=6, material=gold))
        P.append(ico(0.06, loc=p + V((0, 0, 0.9)), sub=1, material=gold, smooth=True))
    rope = [posts[0] + V((0, 0, 0.85)), posts[0].lerp(posts[1], 0.5) + V((0, 0, 0.62)), posts[1] + V((0, 0, 0.85))]
    P.append(tube(smooth_path(rope, 2), r=0.025, seg=4, material=crimson, smooth=True))
# gouden ster bovenop plaats 1
star = [(0.28 * math.sin(i * math.pi / 5) * (1 if i % 2 == 0 else 0.45), 0.28 * math.cos(i * math.pi / 5) * (1 if i % 2 == 0 else 0.45)) for i in range(10)]
P.append(prism(star, 0.08, gold, axis='y', loc=(0, 0.45, 1.45 + 0.32), bevel=0.01))
P.append(box((0.08, 0.06, 0.1), loc=(0, 0.45, 1.47), material=gold))
join(P, 'stage_podium')
report()
finish('finale', 'stage_podium', kind='hero', footprint=2.6, notes='1-2-3 winnaarspodium (cijfers als geometrie) met rode loper, traptreden, paaltjes met koord en gouden ster')
