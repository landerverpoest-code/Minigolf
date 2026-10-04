import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale'); from _deco import *

PURPLE = mat('balloon_purple', '#7a3cc8', rough=0.25)
CRIMSON = mat('balloon_red', '#e0304a', rough=0.25)
GOLD = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
WHITE = mat('balloon_white', '#f6f2fa', rough=0.25)
DARK = mat('stone_dark', '#3d3648', rough=0.9)
COLS = [PURPLE, GOLD, CRIMSON, WHITE]

rnd = random.Random(7)
SPAN, HT = 4.6, 4.2           # boog langs X, opening naar -Y


def arch_pt(t):
    """t in [0,1]: van linkervoet over de top naar rechtervoet (parabool-achtige boog)."""
    a = math.pi * t
    x = -math.cos(a) * SPAN / 2
    z = 0.35 + math.sin(a) ** 0.85 * (HT - 0.35)
    return Vector((x, 0, z))


def balloon(p, r, m, seg=8, rings=6):
    b = sphere(r, seg=seg, rings=rings, material=m, scale=(1, 1, 1.12))
    deform(b, lambda c: Vector((c.x * (1 - 0.18 * max(0, -c.z / r)), c.y * (1 - 0.18 * max(0, -c.z / r)), c.z)))
    return T(b, loc=p)


# --- gewichten / voetstukken
for s in (-1, 1):
    x = s * SPAN / 2
    box((0.7, 0.7, 0.22), loc=(x, 0, 0.11), material=DARK, bevel=0.03)
    lathe([(0.25, 0.22), (0.25, 0.3), (0.1, 0.36)], verts=8, material=GOLD, cap1=True, loc=(x, 0, 0))
# --- clusters van 4 ballonnen langs de boog (spiraal in kleuren), kleine vulballonnetjes ertussen
# boog op gelijke booglengte bemonsteren
_ts = [j / 400 for j in range(401)]
_cum = [0.0]
for j in range(1, 401):
    _cum.append(_cum[-1] + (arch_pt(_ts[j]) - arch_pt(_ts[j - 1])).length)
def t_at(f):
    target = f * _cum[-1]
    for j in range(1, 401):
        if _cum[j] >= target:
            return _ts[j]
    return 1.0
N = 21
for i in range(N):
    t = t_at(i / (N - 1))
    c = arch_pt(t)
    tan = (arch_pt(min(1, t + 0.01)) - arch_pt(max(0, t - 0.01))).normalized()
    nrm = Vector((0, 1, 0)).cross(tan).normalized()  # naar buiten
    side = Vector((0, 1, 0))
    for k in range(4):
        a = k * math.pi / 2 + i * 0.5
        off = (nrm * math.cos(a) + side * math.sin(a)) * 0.22
        balloon(c + off, 0.22, COLS[(k + i) % 4], seg=7, rings=4)
# --- top: grote gouden ster met twee ballonnen + golfbal
top = arch_pt(0.5) + Vector((0, 0, 0.55))
star = []
for i in range(10):
    a = math.pi / 2 + i * TAU / 10
    r = 0.5 if i % 2 == 0 else 0.22
    star.append((r * math.cos(a), top.z + r * math.sin(a)))
st = prism(star, 0.14, material=GOLD, axis='Y')
# ster een beetje bol: middenvoorpunt
for s in (-1, 1):
    balloon(top + Vector((s * 0.6, 0.0, -0.15)), 0.26, CRIMSON if s < 0 else PURPLE, seg=8, rings=6)
# --- losse ballonnen aan touwtjes bij de voeten
for s in (-1, 1):
    base = Vector((s * SPAN / 2, 0, 0.36))
    for k, (dx, dy, h, m) in enumerate(((0.35 * s, -0.2, 1.7, GOLD), (0.55 * s, 0.15, 1.35, WHITE), (0.2 * s, -0.35, 1.15, CRIMSON))):
        tip = base + Vector((dx, dy, h))
        tube([base, base.lerp(tip, 0.5) + Vector((0.05 * s, 0, 0)), tip - Vector((0, 0, 0.24))], 0.008, verts=3, material=WHITE, cap0=False, cap1=False)
        balloon(tip, 0.2, m, seg=7, rings=5)
        cone(0.035, 0.05, loc=tip - Vector((0, 0, 0.235)), verts=4, material=m)
# --- slinger van vlaggetjes onder de boog
pts = [arch_pt(0.12 + 0.76 * i / 10) * 1.0 for i in range(11)]
for i in range(11):
    t = 0.12 + 0.76 * i / 10
    pts[i] = Vector((pts[i].x * 0.78, -0.05, 2.65 - 0.5 * math.sin(math.pi * i / 10)))
tube(pts, 0.012, verts=3, material=GOLD, cap0=False, cap1=False)
for i in range(10):
    p0, p1 = pts[i], pts[i + 1]
    mid = (p0 + p1) / 2
    mesh_obj([p0.lerp(p1, 0.1), p0.lerp(p1, 0.9), mid - Vector((0, 0, 0.28))], [(0, 1, 2), (2, 1, 0)], COLS[i % 4], 'flag')
# --- confetti op de grond
for k in range(24):
    x = rnd.uniform(-SPAN / 2 - 0.5, SPAN / 2 + 0.5); y = rnd.uniform(-0.9, 0.9)
    q = mesh_obj([(-0.04, -0.025, 0), (0.04, -0.025, 0), (0.04, 0.025, 0), (-0.04, 0.025, 0)], [(0, 1, 2, 3)], COLS[k % 4], 'conf')
    T(q, rot=(0, 0, rnd.uniform(0, 180)), loc=(x, y, 0.005))
o = join_all('balloon_arch')
report()
done('finale', 'balloon_arch', kind='hero', footprint=2.8,
     notes='Ballonnenboog: spiraal van glanzende paarse, gouden, rode en witte ballonclusters over een boog van 4.6 m, grote gouden ster met twee ballonnen op de top, voetstukken met gewichten, losse ballonnen aan touwtjes, vlaggetjesslinger onder de boog, confetti op de grond; doorgang langs Y')
