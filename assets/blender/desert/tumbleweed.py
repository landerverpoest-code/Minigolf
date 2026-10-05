import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/meadow')
from _lifekit import *

# ---------------------------------------------------------------- materials (3)
TAN = mat('twig_tan', '#d9b47a', rough=0.85)
STRAW = mat('twig_straw', '#ecd39a', rough=0.85)
BROWN = mat('twig_brown', '#8d5c33', rough=0.85)
R = 0.6
rnd = random.Random(11)


def rand_unit():
    while True:
        v = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)))
        if 0.05 < v.length <= 1:
            return v.normalized()


def wander(p, d, n, step, rmin, rmax, curl):
    """Curved branch path on/inside the ball: keeps its radius in [rmin, rmax], bends smoothly."""
    pts = [p.copy()]
    axis = rand_unit()
    for i in range(n):
        d = (Matrix.Rotation(curl * rnd.uniform(0.6, 1.4), 3, axis) @ d).normalized()
        axis = (axis + rand_unit() * 0.35).normalized()
        q = p + d * step
        r = q.length
        if r > rmax:
            q = q * (rmax / r)
        elif r < rmin:
            q = q * (rmin / max(r, 1e-4))
        d = (q - p).normalized(); p = q
        pts.append(p.copy())
    return pts


tw = []
MATS = [TAN, TAN, BROWN, STRAW]
# long branches looping round the ball (most of them near the shell -> airy, see-through middle)
for k in range(45):
    r0 = rnd.uniform(0.4, 0.56)
    p = rand_unit() * r0
    t = rand_unit(); t = (t - p.normalized() * t.dot(p.normalized())).normalized()
    inner = k % 6 == 0
    pts = wander(p, t, 6, rnd.uniform(0.15, 0.19), 0.2 if inner else 0.38, 0.6, rnd.uniform(0.25, 0.45))
    th = rnd.uniform(0.018, 0.025)
    rad = [th * (1 - 0.55 * i / (len(pts) - 1)) for i in range(len(pts))]
    m = MATS[k % len(MATS)]
    tw.append(tube(pts, rad, seg=3, material=m, cap=False))
    # a couple of forked twigs
    for j in (2, 4):
        if rnd.random() < 0.6:
            b0 = pts[j]
            bd = (pts[j + 1] - pts[j]).normalized()
            bd = (bd + rand_unit() * 0.9).normalized()
            bp = wander(b0, bd, 2, rnd.uniform(0.07, 0.1), 0.3, 0.6, 0.5)
            tw.append(tube(bp, [rad[j] * 0.8, rad[j] * 0.55, rad[j] * 0.3], seg=3, material=m, cap=False))
# small dense core so it reads as one tangled ball from far away
for k in range(4):
    p = rand_unit() * 0.12
    pts = wander(p, rand_unit(), 4, 0.1, 0.05, 0.25, 0.8)
    tw.append(tube(pts, 0.02, seg=3, material=BROWN, cap=False))

body = part(tw, 'body', (0, 0, 0), angle=70)
# exact radius 0.6 (max vertex distance from the centre)
rmax = max(v.co.length for v in body.data.vertices)
body.data.transform(Matrix.Scale(R / rmax, 4)); body.data.update()
print('RMAX', max(v.co.length for v in body.data.vertices))
report(); print_ext()
lo, hi = bounds()
print('EXTENTS', tuple(round(v, 3) for v in lo), tuple(round(v, 3) for v in hi))
notes = ('Parts/pivots: body (origin 0,0,0 = ball centre; radius exactly 0.6 = max vertex distance; ~50 curved branch tubes '
         'with forked twigs in tan/straw/brown, airy). Not grounded: the bottom sits at z=-0.6; the game rolls it.')
std_view()
finish('desert', 'tumbleweed', kind='char', footprint=0.6, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('tumble', dirs={'front': (0, -1, 0.15), 'top': (0.01, 0.01, 1)})
    closeup('tumble_far', (0, 0, 0), 14, d=(0.6, -1, 0.3), lens=50)
    montage_files([f'{SCRATCH}/tumble_{k}.png' for k in ('front', 'top', 'far')], f'{SCRATCH}/tumble_views.png')
