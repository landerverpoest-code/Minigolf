import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale'); from _deco import *

PURPLE = mat('royal_purple', '#5b2a86', rough=0.55)
CRIMSON = mat('crimson', '#b0213a', rough=0.55)
GOLD = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
MARBLE = mat('marble', '#efe9f2', rough=0.35)
DARK = mat('stone_dark', '#3d3648', rough=0.9)

H = 4.2
# marmeren voet met trapje
box((0.9, 0.9, 0.18), loc=(0, 0, 0.09), material=DARK)
lathe([(0.32, 0.18), (0.32, 0.26), (0.24, 0.32), (0.16, 0.36), (0.12, 0.5)], verts=8, material=MARBLE, cap1=False)
# paal met gouden ringen en bol
pole = lathe([(0.07, 0.48), (0.06, H)], verts=8, material=GOLD, cap0=False, cap1=False)
for z in (1.2, 2.6):
    lathe([(0.09, z - 0.04), (0.09, z + 0.04)], verts=8, material=GOLD, cap0=False, cap1=False)
sphere(0.13, loc=(0, 0, H + 0.08), seg=7, rings=5, material=GOLD)
cone(0.07, 0.25, loc=(0, 0, H + 0.3), verts=6, material=GOLD)
# dwarsbalk
rod((-0.75, -0.08, H - 0.2), (0.75, -0.08, H - 0.2), r=0.04, verts=6, material=GOLD)
for s in (-1, 1):
    sphere(0.07, loc=(s * 0.78, -0.08, H - 0.2), seg=5, rings=3, material=GOLD)
# vaandel: hangend doek met zwaluwstaart, licht golvend, paars met gouden rand
W, L = 1.3, 2.3
top = H - 0.24
def f(u, v):
    x = -W / 2 + u * W
    z = top - v * L
    # zwaluwstaart onderaan: midden hoger
    if v > 0.8:
        z += (1 - abs(u - 0.5) * 2) * (v - 0.8) / 0.2 * 0.4
    return Vector((x, -0.1 - 0.05 * math.sin(u * math.pi * 2 + v * 2) * v, z))
ban = grid_sheet(f, 4, 6, None, 'banner')
recolor(ban, [PURPLE, GOLD, CRIMSON], lambda p: 1 if (abs(p.center.x) > W / 2 - W / 6 * 0.99 and False) else 0)
bm = bmesh.new(); bm.from_mesh(ban.data)
bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.02) if hasattr(bmesh.ops, 'solidify') else None
bm.to_mesh(ban.data); bm.free()
# gouden zoom links/rechts en onderrand
for s in (-1, 1):
    pts = [f(0 if s < 0 else 1, v / 6) + Vector((0, -0.012, 0)) for v in range(7)]
    tube(pts, 0.025, verts=4, material=GOLD, cap0=False, cap1=False)
# embleem: gouden trofee op een rode schijf
E = Vector((0, -0.16, top - 0.95))
disc = cyl(0.42, 0.03, verts=12, material=CRIMSON, rot=(math.pi / 2, 0, 0), loc=E)
ring = torus(0.42, 0.03, loc=E, rot=(math.pi / 2, 0, 0), seg=12, ring=3, material=GOLD, smooth=True)
cup = lathe([(0.0, 0.0), (0.06, 0.0), (0.06, 0.03), (0.025, 0.06), (0.02, 0.14), (0.12, 0.2), (0.17, 0.33), (0.18, 0.42), (0.0, 0.42)], verts=6, material=GOLD, sx=1.0, sy=0.3)
T(cup, loc=E + Vector((0, -0.03, -0.24)))
for s in (-1, 1):
    tube([E + Vector((s * 0.15, -0.04, 0.12)), E + Vector((s * 0.27, -0.04, 0.08)), E + Vector((s * 0.25, -0.04, -0.03)), E + Vector((s * 0.12, -0.04, -0.06))], 0.018, verts=4, material=GOLD)
box((0.24, 0.05, 0.05), loc=E + Vector((0, -0.04, -0.27)), material=GOLD)
# sterretjes boven het embleem
for k, x in enumerate((-0.3, 0.0, 0.3)):
    st = []
    for i in range(10):
        a = math.pi / 2 + i * TAU / 10
        r = 0.08 if i % 2 == 0 else 0.035
        st.append((x + r * math.cos(a), top - 0.25 + (0.05 if k == 1 else 0) + r * math.sin(a)))
    so = mesh_obj([(x_, -0.15, z_) for x_, z_ in st], [list(range(10))[::-1]], GOLD, 'star')
    fix_normals(so)
    if so.data.polygons[0].normal.y > 0:
        so.data.flip_normals()
# kwastjes aan de dwarsbalk
for s in (-1, 1):
    tube([(s * 0.72, -0.1, H - 0.24), (s * 0.72, -0.1, H - 0.55)], 0.01, verts=3, material=GOLD)
    cone(0.05, 0.14, loc=(s * 0.72, -0.1, H - 0.6), verts=6, material=GOLD)
o = join_all('champion_banner')
report()
done('finale', 'champion_banner', kind='scatter', footprint=0.5,
     notes='Kampioensvaandel: gouden paal op marmeren voet met dwarsbalk, golvend paars vaandel met zwaluwstaart en gouden zoom, embleem van een gouden trofee op een rode schijf met gouden rand, drie gouden sterren, kwastjes')
