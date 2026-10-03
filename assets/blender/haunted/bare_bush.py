import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted')
from mglib import *
from mgx import *
reset()
bark = mat('bark', '#4a3d4c', rough=0.95)
thorn = mat('thorn', '#2a2230', rough=0.8)
berry = mat('berry', '#8a2350', rough=0.4)
V = Vector
parts = []
rnd = random.Random(11)
N = 10
for k in range(N):
    a = k * TAU / N + rnd.uniform(-0.25, 0.25)
    el = rnd.uniform(0.35, 1.2)
    d = V((math.cos(a) * math.cos(el), math.sin(a) * math.cos(el), math.sin(el)))
    L = rnd.uniform(0.75, 1.05)
    ax = d.cross(V((0, 0, 1))) if k % 2 else V((0, 0, 1)).cross(d)
    pts = grow(V((0, 0, 0.02)), d, L, 4, ax, 0.15, 0.55, seed=k, wob=0.12, shrink=0.3)
    parts.append(tube(pts, r=[0.055, 0.04, 0.028, 0.016, 0.0], seg=4, material=bark, smooth=False))
    # zijtak
    p = pts[2]; dd = (pts[3] - pts[2]).normalized()
    side = (dd.cross(V((0, 0, 1))).normalized() * (1 if k % 2 else -1) + V((0, 0, 0.6)) + dd * 0.4).normalized()
    sp = grow(p, side, 0.35, 2, dd.cross(side), 0.3, 0.6, seed=k + 20, wob=0.1)
    parts.append(tube(sp, r=[0.018, 0.01, 0.0], seg=3, material=bark, smooth=False))
    # doornen
    for j, t in enumerate((1, 3)):
        p = pts[t]; dd = (pts[t + 1] - pts[t]).normalized()
        n = dd.cross(V((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)))).normalized()
        parts.append(tube([p - n * 0.01, p + n * 0.07 + dd * 0.03], r=[0.013, 0.0], seg=3, material=thorn, smooth=False))
    if k % 3 == 0:
        parts.append(ico(0.028, loc=pts[3] + V((0, 0, -0.03)), material=berry, smooth=True))
parts.append(shade_smooth(ico(0.14, loc=(0, 0, 0), material=thorn, scale=(1.3, 1.3, 0.45), jitter=0.025, seed=2)))
join(parts, 'bare_bush')
report()
finish('haunted', 'bare_bush', kind='scatter', footprint=0.5, notes='doornige dode struik met een paar verdroogde bessen')
