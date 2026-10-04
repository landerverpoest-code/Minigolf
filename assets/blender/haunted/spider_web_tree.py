import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted'); from _deco import *

BARK = mat('bark', '#4a3d4c', rough=0.95)
BARK_L = mat('bark_light', '#62546a', rough=0.95)
WEB = mat('web_silk', '#e8e4f0', rough=0.6)
SPIDER = mat('spider_black', '#1d1a24', rough=0.5)
EYES = mat('glow_eyes', '#d8ff5a', rough=0.5, emit='#c6ff3a', emit_strength=3.0)

rnd = random.Random(3)
# --- dode stam, licht gedraaid, met wortels
tp = [Vector(p) for p in ((0, 0, -0.05), (0.04, 0, 0.6), (-0.06, 0.03, 1.3), (0.05, 0.0, 2.0), (0.15, 0.05, 2.6))]
tube(tp, [0.32, 0.24, 0.2, 0.16, 0.11], verts=6, material=BARK, smooth=True)
for k, a in enumerate((0.4, 2.0, 3.5, 5.0)):
    d = Vector((math.cos(a), math.sin(a), 0))
    tube([Vector((0, 0, 0.35)) + d * 0.08, Vector((0, 0, 0.1)) + d * 0.4, d * 0.75 + Vector((0, 0, -0.03))], [0.14, 0.08, 0.0], verts=4, material=BARK, smooth=True)
# --- takken (hoekig, kaal)
branches = [
    [(0.05, 0.0, 1.9), (0.6, -0.1, 2.35), (1.15, -0.15, 2.5), (1.5, -0.1, 2.75)],
    [(-0.04, 0.02, 1.5), (-0.55, 0.0, 1.95), (-1.0, 0.05, 2.05), (-1.3, 0.1, 2.4)],
    [(0.15, 0.05, 2.55), (0.1, 0.15, 3.1), (-0.15, 0.25, 3.5)],
    [(0.12, 0.02, 2.4), (0.45, 0.35, 2.85), (0.7, 0.5, 3.25)],
]
tips = []
for k, b in enumerate(branches):
    pts = [Vector(p) for p in b]
    tube(pts, [0.1 - 0.02 * k * 0.5] + [0.08 * (1 - i / len(pts)) + 0.015 for i in range(1, len(pts) - 1)] + [0.0], verts=4, material=BARK_L if k % 2 else BARK, smooth=True)
    tips.append(pts)
# twijgjes
for k, pts in enumerate(tips):
    p = pts[1]; d = (pts[2] - pts[1]).normalized()
    side = d.cross(Vector((0, 0, 1))).normalized() * (1 if k % 2 else -1)
    q = p + (d * 0.3 + side * 0.25 + Vector((0, 0, 0.35)))
    tube([p, q, q + Vector((0.05 * (1 if k % 2 else -1), 0, 0.15))], [0.035, 0.02, 0.0], verts=3, material=BARK_L)


# --- spinnenwebben: radialen + spiraal als dunne linten
def web(center, normal, R, nspokes=7, rings=4, anchors=None, seed=0):
    rr = random.Random(seed)
    n = Vector(normal).normalized()
    u = n.cross(Vector((0, 0, 1))); u = u.normalized() if u.length > 1e-3 else Vector((1, 0, 0))
    v = n.cross(u).normalized()
    c = Vector(center)
    spokes = []
    for i in range(nspokes):
        a = TAU * i / nspokes + rr.uniform(-0.15, 0.15)
        L = R * rr.uniform(0.8, 1.1)
        spokes.append((a, L))
    parts = []
    w = 0.012
    def strand(p0, p1):
        d = (p1 - p0)
        side = d.cross(n).normalized() * w
        return mesh_obj([p0 - side, p0 + side, p1 + side, p1 - side], [(0, 1, 2, 3), (3, 2, 1, 0)], WEB, 'strand')
    for a, L in spokes:
        parts.append(strand(c, c + (u * math.cos(a) + v * math.sin(a)) * L))
    for r in range(1, rings + 1):
        f = r / (rings + 0.6)
        for i in range(nspokes):
            a0, L0 = spokes[i]; a1, L1 = spokes[(i + 1) % nspokes]
            p0 = c + (u * math.cos(a0) + v * math.sin(a0)) * L0 * f
            p1 = c + (u * math.cos(a1) + v * math.sin(a1)) * L1 * f
            sag = (p0 + p1) / 2 - (c - (p0 + p1) / 2).normalized() * 0 - Vector((0, 0, 0.02))
            parts.append(strand(p0, sag)); parts.append(strand(sag, p1))
    return join(parts, 'web')


# groot web tussen stam en rechtertak, kleiner tussen stam en linkertak
web((0.72, -0.14, 1.9), (0.15, -1, 0.05), 0.8, nspokes=8, rings=3, seed=1)
web((-0.62, 0.0, 1.6), (-0.1, -1, 0.1), 0.58, nspokes=7, rings=3, seed=2)
# --- spin met gloeiende oogjes, hangend aan een draad
S = Vector((0.95, -0.22, 0.85))
rod(S + Vector((0, 0, 0.08)), Vector((1.0, -0.18, 2.55)), r=0.006, verts=3, material=WEB)
sphere(0.09, loc=S, seg=6, rings=4, material=SPIDER, scale=(1, 1.2, 0.9))
sphere(0.06, loc=S + Vector((0, -0.11, 0.0)), seg=5, rings=3, material=SPIDER)
for s in (-1, 1):
    sphere(0.014, loc=S + Vector((s * 0.025, -0.16, 0.02)), seg=3, rings=2, material=EYES)
    for k in range(4):
        y = -0.08 + k * 0.05
        p0 = S + Vector((s * 0.06, y, 0.0))
        p1 = S + Vector((s * 0.16, y + (k - 1.5) * 0.04, 0.07))
        p2 = S + Vector((s * 0.22, y + (k - 1.5) * 0.06, -0.06))
        tube([p0, p1, p2], 0.01, verts=3, material=SPIDER, cap0=False, cap1=False)
o = join_all('spider_web_tree')
report()
done('haunted', 'spider_web_tree', kind='scatter', footprint=0.8,
     notes='Dode kale boom met wortels en hoekige takken, twee grote spinnenwebben (radialen en hangende ringen) tussen stam en takken, zwarte spin met gloeiende oogjes (glow_eyes) aan een draad')
