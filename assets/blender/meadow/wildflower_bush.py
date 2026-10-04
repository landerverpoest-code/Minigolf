import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/meadow'); from _deco import *

GREEN = mat('leaf', '#4f9c33', rough=0.8)
PURPLE = mat('petal_purple', '#8a5ad8', rough=0.6)
PINK = mat('petal_pink', '#f27aa6', rough=0.6)
RED = mat('petal_red', '#e8433a', rough=0.6)
YEL = mat('petal_yellow', '#ffcd2e', rough=0.5)

rnd = random.Random(11)


def lupin(base, top, mat_, h=0.38, r=0.075):
    """Stengel + kegelvormige bloemaar met getande ringen."""
    base, top = Vector(base), Vector(top)
    parts = [rod(base, top, r=0.012, verts=4, material=GREEN)]
    n = 4
    prof = [(0.0, -0.02)]
    for i in range(n):
        t = i / n
        rr = r * (1 - t * 0.8)
        prof.append((rr, h * t))
        prof.append((rr * 0.62, h * t + h / n * 0.55))
    prof.append((0.0, h + 0.03))
    sp = lathe(prof, verts=5, material=mat_, phase=rnd.uniform(0, 1))
    d = (top - base).normalized()
    q = d.to_track_quat('Z', 'Y')
    sp.data.transform(Matrix.Translation(top) @ q.to_matrix().to_4x4()); sp.data.update()
    parts.append(sp)
    return parts


# --- bladrozet onderaan (handvormige lupinebladeren)
for i in range(9):
    a = TAU * i / 9 + rnd.uniform(-0.2, 0.2)
    d = Vector((math.cos(a), math.sin(a), rnd.uniform(0.25, 0.7)))
    leaf((0, 0, 0.04), d, length=rnd.uniform(0.3, 0.42), width=0.07, curl=0.12, fold=0.03, material=GREEN, segs=2)
for i in range(5):
    a = TAU * i / 5 + 0.3
    d = Vector((math.cos(a), math.sin(a), 1.4))
    leaf((math.cos(a) * 0.06, math.sin(a) * 0.06, 0.1), d, length=0.3, width=0.06, curl=0.1, fold=0.03, material=GREEN, segs=2)

# --- lupines: hoge aren in drie kleuren
spikes = [((0.02, 0.0), (0.0, -0.02, 0.75), PURPLE, 0.42), ((0.12, 0.08), (0.2, 0.12, 0.62), PINK, 0.36),
          ((-0.1, 0.06), (-0.2, 0.12, 0.66), PURPLE, 0.38), ((0.05, -0.1), (0.12, -0.22, 0.55), YEL, 0.32),
          ((-0.06, -0.08), (-0.14, -0.18, 0.5), PINK, 0.3), ((0.0, 0.14), (0.04, 0.26, 0.58), PURPLE, 0.34)]
for (bx, by), tp, m, h in spikes:
    lupin((bx, by, 0.02), tp, m, h=h)

# --- klaprozen en madeliefjes op dunne steeltjes
heads = [((0.32, -0.12, 0.5), RED, 4, 0.07), ((-0.3, -0.05, 0.44), RED, 4, 0.065), ((0.26, 0.24, 0.42), RED, 4, 0.06),
         ((-0.22, 0.3, 0.36), YEL, 7, 0.05), ((0.36, 0.06, 0.3), YEL, 7, 0.045), ((-0.34, -0.25, 0.3), PINK, 6, 0.05)]
for p, m, n, R in heads:
    p = Vector(p)
    b = Vector((p.x * 0.3, p.y * 0.3, 0.02))
    mid = (b + p) / 2 + Vector((p.x * 0.15, p.y * 0.15, 0))
    tube([b, mid, p], [0.009, 0.008, 0.007], verts=3, material=GREEN, cap0=False, cap1=False)
    f = flower_head(R=R, rc=R * 0.3, petals=n, cup=R * 0.35, petal_mat=m, heart_mat=(GREEN if m is RED else YEL if m is not YEL else RED), wide=0.9)
    nrm = Vector((p.x, p.y, 0.9)).normalized()
    orient(f, nrm, p)

o = join_all('wildflower_bush')
shade_smooth(o, 70)
for p in o.data.polygons:
    if o.data.materials[p.material_index].name not in ('leaf', 'petal_red'):
        p.use_smooth = False  # aren en bloemblaadjes facet-gearceerd
report()
done('meadow', 'wildflower_bush', kind='scatter', footprint=0.45,
     notes='Wilde-bloemenstruik: rozet van bladeren met zes hoge lupine-aren (paars, roze, geel), rode klaprozen en gele/roze bloemetjes op dunne steeltjes')
