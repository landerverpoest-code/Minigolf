import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/finale')
from mglib import *
from mgx import *
reset()
bronze = mat('bronze', '#9c6634', rough=0.45, metal=0.4)
gold = mat('gold', '#f2c14e', rough=0.3, metal=0.4)
crimson = mat('crimson', '#a01e34', rough=0.6)
basalt = mat('basalt', '#3d3648', rough=0.9)
glow = mat('glow_eyes', '#ff7a1a', rough=0.4, emit='#ff6a10', emit_strength=2.5)
V = Vector
P = []
# rots met lavabarsten
rk = rock(1.45, sub=2, material=basalt, scale=(1.25, 1.05, 0.62), jit=0.08, seed=5)
chop(rk, 6, seed=11, depth=(0.8, 0.93), minz=0.2)
T(rk, loc=(0, 0, 0.3))
P.append(rk)
for k, (a, z0, z1) in enumerate([(-1.75, 0.2, 0.75), (-1.2, 0.15, 0.6), (-0.4, 0.2, 0.8), (0.6, 0.1, 0.65), (2.3, 0.2, 0.7)]):
    pts = []
    for j in range(4):
        z = z0 + (z1 - z0) * j / 3
        aa = a + 0.12 * math.sin(j * 2.1 + k)
        loc, nor = surface_hit(rk, (math.cos(aa), math.sin(aa), 0), center=(0, 0, z))
        if loc is not None:
            pts.append(loc + nor * 0.01)
    if len(pts) >= 2:
        P.append(tube(pts, r=[0.0] + [0.05] * (len(pts) - 2) + [0.0], seg=3, material=glow, smooth=False))
top = surface_hit(rk, (0, 0, 1), center=(0, 0, 0.5))[0].z
print('rock top', top)
# ruggengraat: staartpunt -> heup -> borst -> nek -> kop
spine = [V((1.55, -0.95, top - 0.6)), V((1.45, -0.7, top - 0.15)), V((1.2, -0.2, top + 0.08)), V((0.8, 0.45, top + 0.12)), V((0.1, 0.85, top + 0.15)),
         V((-0.6, 0.6, top + 0.2)), V((-0.75, 0.0, top + 0.35)), V((-0.35, -0.2, top + 0.65)), V((0.0, 0.05, top + 1.15)), V((0.05, 0.0, top + 1.8)),
         V((0.0, -0.05, top + 2.4)), V((0.0, -0.3, top + 2.95)), V((0.0, -0.62, top + 3.25))]
rad = [0.02, 0.08, 0.14, 0.2, 0.26, 0.32, 0.4, 0.5, 0.52, 0.4, 0.28, 0.25, 0.25]
sp = smooth_path(spine, 3); rr = interp(rad, 3)
body = tube(sp, r=rr, seg=8, material=bronze, smooth=True)
shade_smooth(body, 45)
P.append(body)
# stekels langs de rug (goud)
fr = frames(sp)
for i in range(6, len(sp) - 2, 2):
    t, N, B = fr[i]
    back = V((0, 0.0, 1)).lerp(V((0, 1, 0.25)), min(1, max(0, (sp[i].z - top - 0.3) / 1.2))).normalized()
    out = (back - t * back.dot(t)).normalized()
    h = 0.16 + 0.35 * rr[i]
    base = sp[i] + out * rr[i] * 0.85
    c = cone(rr[i] * 0.3 + 0.04, h, verts=4, material=gold)
    q = V((0, 0, 1)).rotation_difference((out + t * 0.5).normalized())
    T(c, rot=q.to_euler(), loc=base + (out + t * 0.5).normalized() * h * 0.4)
    P.append(c)
# buikplaten (goud) aan de voorkant van borst en nek
for i in range(len(sp) - 16, len(sp) - 3, 2):
    t, N, B = fr[i]
    front = V((0, -1, -0.2))
    out = (front - t * front.dot(t)).normalized()
    pl = box((rr[i] * 0.95, 0.05, 0.13), material=gold)
    q = V((0, -1, 0)).rotation_difference(out)
    T(pl, rot=q.to_euler(), loc=sp[i] + out * rr[i] * 0.9)
    P.append(pl)
# kop
H = []
H.append(ico(0.3, sub=2, material=bronze, smooth=True, scale=(1.0, 1.15, 0.85)))
sn = cyl(0.2, 0.55, loc=(0, -0.38, -0.04), rot=(math.pi / 2, 0, math.pi / 4), verts=4, r2=0.12, material=bronze)
T(sn, scale=(1.15, 1, 0.75), pivot=(0, -0.38, -0.04)); bev(sn, 0.03); H.append(sn)
jaw = cyl(0.16, 0.45, loc=(0, -0.33, -0.17), rot=(math.pi / 2 + 0.25, 0, math.pi / 4), verts=4, r2=0.09, material=bronze)
T(jaw, scale=(1.1, 1, 0.5), pivot=(0, -0.33, -0.17)); H.append(jaw)
for sx in (-1, 1):
    H.append(ico(0.075, loc=(sx * 0.165, -0.21, 0.08), sub=1, material=glow, smooth=True, scale=(1, 0.7, 1)))
    H.append(box((0.14, 0.12, 0.05), loc=(sx * 0.15, -0.2, 0.15), rot=(0.2, 0, sx * 0.3), material=bronze))
    horn = smooth_path([V((sx * 0.12, 0.05, 0.18)), V((sx * 0.2, 0.3, 0.3)), V((sx * 0.25, 0.6, 0.32)), V((sx * 0.22, 0.85, 0.2))], 2)
    H.append(tube(horn, r=interp([0.07, 0.055, 0.035, 0.0], 2), seg=5, material=gold, smooth=True))
    H.append(cone(0.05, 0.25, loc=(sx * 0.3, 0.05, 0.0), rot=(0, sx * 1.9, 0), verts=4, material=gold))
    H.append(cone(0.025, 0.09, loc=(sx * 0.07, -0.55, -0.15), rot=(math.pi, 0, 0), verts=4, material=gold))
hd = join(H, 'head')
T(hd, scale=1.35, rot=(0.25, 0, 0), loc=sp[-1] + V((0, -0.15, 0.1)))
P.append(hd)
# poten
for sx in (-1, 1):
    # voorpoot
    fl = smooth_path([V((sx * 0.3, -0.2, top + 1.2)), V((sx * 0.42, -0.45, top + 0.75)), V((sx * 0.36, -0.55, top + 0.35)), V((sx * 0.36, -0.75, top + 0.08))], 2)
    P.append(tube(fl, r=interp([0.17, 0.13, 0.1, 0.09], 2), seg=6, material=bronze, smooth=True))
    P.append(ico(0.13, loc=(sx * 0.36, -0.82, top + 0.06), sub=1, material=bronze, smooth=True, scale=(1.1, 1.3, 0.6)))
    # achterpoot
    P.append(ico(0.36, loc=(sx * 0.5, 0.05, top + 0.55), sub=2, material=bronze, smooth=True, scale=(0.75, 1.15, 1.0)))
    hl = smooth_path([V((sx * 0.55, 0.0, top + 0.4)), V((sx * 0.62, -0.35, top + 0.15)), V((sx * 0.6, -0.65, top + 0.07))], 2)
    P.append(tube(hl, r=interp([0.16, 0.12, 0.1], 2), seg=6, material=bronze, smooth=True))
    P.append(ico(0.14, loc=(sx * 0.6, -0.72, top + 0.06), sub=1, material=bronze, smooth=True, scale=(1.1, 1.3, 0.6)))
    for (fx, fy) in [(0.36, -0.82), (0.6, -0.72)]:
        for k in (-1, 0, 1):
            P.append(cone(0.03, 0.12, loc=(sx * fx + k * 0.07, fy - 0.17, top + 0.04), rot=(math.pi / 2 + 0.3, 0, 0), verts=4, material=gold))
# gevouwen vleugels
for sx in (-1, 1):
    sh = V((sx * 0.32, 0.18, top + 2.0))
    wr = V((sx * 0.62, 0.55, top + 3.05))
    tips = [V((sx * 0.85, 1.0, top + 1.1)), V((sx * 0.95, 1.05, top + 0.55)), V((sx * 0.8, 0.85, top + 0.3))]
    P.append(tube(smooth_path([sh, sh.lerp(wr, 0.5) + V((sx * 0.12, -0.05, 0)), wr], 2), r=[0.1, 0.09, 0.08, 0.07, 0.06], seg=5, material=bronze, smooth=True))
    P.append(cone(0.06, 0.3, loc=wr + V((0, 0.0, 0.15)), verts=4, material=gold))
    for tp in tips:
        P.append(tube([wr, wr.lerp(tp, 0.5) + V((sx * 0.08, 0.05, 0)), tp], r=[0.05, 0.04, 0.0], seg=4, material=bronze, smooth=False))
    hip = V((sx * 0.45, 0.45, top + 0.7))
    pts = [sh, wr, tips[0], tips[0].lerp(tips[1], 0.5) + V((-sx * 0.05, -0.05, 0.12)), tips[1], tips[1].lerp(tips[2], 0.5) + V((-sx * 0.05, -0.05, 0.1)), tips[2], hip]
    bm = bmesh.new()
    vs = [bm.verts.new(p + V((sx * 0.02, 0.02, 0))) for p in pts]
    bm.faces.new(vs)
    P.append(link_bm(bm, 'wing', crimson))

T(join(P, 'dragon_statue'), scale=1.2)
report()
finish('finale', 'dragon_statue', kind='hero', footprint=2.2, notes='bronzen draak opgerold op een basaltrots met gevouwen vleugels; ogen + lavabarsten = glow_eyes')
