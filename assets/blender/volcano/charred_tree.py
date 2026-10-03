import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mgx import *

char = mat('char', '#221d1b', rough=0.95)
char_g = mat('char_grey', '#4a403b', rough=0.95)
ember = mat('glow_ember', '#ff6a10', rough=0.5, emit='#ff4a00', emit_strength=3.5)

rnd = random.Random(11)
parts = []
# kronkelige stam met wortelvoet
prof = [(0.42, 0), (0.3, 0.12), (0.24, 0.4), (0.21, 0.9), (0.19, 1.4), (0.17, 1.9), (0.14, 2.3)]
trunk = lathe(prof, seg=7, material=char, cap_bottom=False)
def twist(c):
    a = c.z * 0.9
    x, y = c.x * math.cos(a) - c.y * math.sin(a), c.x * math.sin(a) + c.y * math.cos(a)
    return (x + 0.18 * math.sin(c.z * 1.6), y + 0.1 * math.sin(c.z * 2.3 + 1), c.z)
# extra knoesten: radiale ruis
for v in trunk.data.vertices:
    d = Vector((v.co.x, v.co.y))
    if d.length > 0:
        k = 1 + 0.18 * noise.noise(Vector((v.co.x * 3, v.co.y * 3, v.co.z * 2)))
        v.co.x *= k; v.co.y *= k
bend(trunk, twist)
parts.append(trunk)
def tpos(z):
    return Vector(twist(Vector((0, 0, z))))
# wortels
for a in (0.3, 1.9, 3.4, 4.9):
    p0 = Vector((0.15 * math.cos(a), 0.15 * math.sin(a), 0.25))
    p1 = Vector((0.62 * math.cos(a + 0.2), 0.62 * math.sin(a + 0.2), -0.04))
    parts.append(rod(p0, p1, 0.14, 0.06, verts=5, material=char))

tips = []
def branch(p, d, L, r, depth, seed):
    """Kronkelige tak uit segmenten; vertakt zich."""
    rr = random.Random(seed)
    nseg = 2
    for i in range(nseg):
        d = (d + Vector((rr.uniform(-0.45, 0.45), rr.uniform(-0.45, 0.45), rr.uniform(-0.1, 0.3)))).normalized()
        q = p + d * (L / nseg)
        r2 = r * 0.78
        parts.append(rod(p - d * r * 0.5, q, r, r2, verts=5 if depth < 1 else 4, material=char))
        p, r = q, r2
    if depth < 1:
        for k in range(2):
            side = Vector((rr.uniform(-1, 1), rr.uniform(-1, 1), 0)).normalized()
            branch(p, (d + side * 0.8 + Vector((0, 0, 0.3))).normalized(), L * 0.6, r * 0.95, depth + 1, seed * 7 + k + 1)
    else:
        tips.append((p, d, r))
for k, (z, a, up) in enumerate(((1.75, 0.4, 0.55), (2.05, 2.6, 0.7), (2.25, 4.4, 0.9))):
    d = Vector((math.cos(a), math.sin(a), up)).normalized()
    branch(tpos(z), d, 1.25 - k * 0.15, 0.13, 0, 100 + k * 13)
# afgebroken top van de stam
top = tpos(2.3)
parts.append(rod(top - Vector((0, 0, 0.05)), top + Vector((0.05, 0.02, 0.45)), 0.14, 0.09, verts=6, material=char))
# gloeiende sintels op een paar takpunten en op de gebroken top
for i, (p, d, r) in enumerate(tips):
    if i % 2 == 0:
        parts.append(cyl(r * 0.95, 0.025, loc=p + d * 0.005, rot=d.to_track_quat('Z', 'Y').to_euler(), verts=4, material=ember))
parts.append(cyl(0.085, 0.03, loc=top + Vector((0.05, 0.02, 0.46)), verts=6, material=ember))
# afgebroken zijstompjes met gloeiend breukvlak
for (z, a, L) in ((0.95, 3.6, 0.35), (1.35, 0.9, 0.3)):
    p0 = tpos(z); d = Vector((math.cos(a), math.sin(a), 0.5)).normalized()
    parts.append(rod(p0, p0 + d * L, 0.08, 0.06, verts=5, material=char))
    parts.append(cyl(0.058, 0.02, loc=p0 + d * (L + 0.005), rot=d.to_track_quat('Z', 'Y').to_euler(), verts=5, material=ember))
# gloeiende scheuren in de stam + grijze asplekken
tree = surf_tree(trunk)
parts += crack_ribbon(tree, (0.2, -0.2, 0.7), (0.1, 0, 1), length=0.9, width=0.05, steps=8, seed=4, material=ember, branch=1)
parts += crack_ribbon(tree, (-0.2, 0.1, 1.5), (0, 0.2, 1), length=0.5, width=0.04, steps=5, seed=9, material=ember)
parts += crack_ribbon(tree, (0.25, 0.2, 0.3), (0.3, -0.2, 1), length=0.6, width=0.045, steps=6, seed=13, material=ember)
dust(trunk, char_g, 0.45, noise_amt=0.3, seed=2)
o = join(parts, 'charred_tree')
smooth(o, 50)
xform(o, scale=1.12)
report()
finish('volcano', 'charred_tree', kind='scatter', footprint=0.7, notes='verkoolde kronkelige kale boom met gloeiende sintels op takpunten en gloeiende scheuren in de stam (glow_ember)')
