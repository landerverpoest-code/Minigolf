import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/castle'); from _deco import *

STONE = mat('stone_warm', '#a69c8f', rough=0.9)
STONE_D = mat('stone_dark', '#867b6f', rough=0.9)
WATER = mat('water', '#2c5e93', rough=0.08)
SPRAY = mat('water_light', '#9fd4f0', rough=0.1, emit='#6fb8e0', emit_strength=0.25)
MOSS = mat('moss', '#5c8a35', rough=0.95)

rnd = random.Random(7)
# --- geplaveide cirkel: ring van tegels
for ring, (r0, r1, n) in enumerate(((1.45, 1.95, 20), (1.95, 2.35, 24))):
    for i in range(n):
        a0 = TAU * (i + 0.04) / n + ring * 0.1; a1 = TAU * (i + 0.96) / n + ring * 0.1
        pts = [(r0 * math.cos(a0), r0 * math.sin(a0)), (r1 * math.cos(a0), r1 * math.sin(a0)), (r1 * math.cos(a1), r1 * math.sin(a1)), (r0 * math.cos(a1), r0 * math.sin(a1))]
        t = prism(pts, 0.06 + rnd.uniform(-0.01, 0.01), material=STONE if (i + ring) % 3 else STONE_D, axis='Z')
# --- achthoekig bekken: muurtje van blokken met dekstenen
NB = 8; RB = 1.4
basin_floor = cyl(RB, 0.1, verts=NB, loc=(0, 0, 0.05), material=STONE_D)
for i in range(NB):
    a = TAU * (i + 0.5) / NB
    side = 2 * RB * math.sin(math.pi / NB)
    c = Vector((math.cos(a), math.sin(a), 0)) * RB * math.cos(math.pi / NB)
    wall = box((0.22, side * 0.98, 0.42), loc=(c.x, c.y, 0.25), rot=(0, 0, a), material=STONE, bevel=0.025)
    cap = box((0.34, side + 0.06, 0.09), loc=(c.x * 1.01, c.y * 1.01, 0.5), rot=(0, 0, a), material=STONE_D, bevel=0.02)
    # pilastertje op de hoek
    ca = TAU * i / NB
    box((0.2, 0.2, 0.52), loc=(RB * 1.02 * math.cos(ca), RB * 1.02 * math.sin(ca), 0.26), rot=(0, 0, ca), material=STONE_D, bevel=0.02)
    box((0.24, 0.24, 0.07), loc=(RB * 1.02 * math.cos(ca), RB * 1.02 * math.sin(ca), 0.56), rot=(0, 0, ca), material=STONE, bevel=0.015)
# water in het bekken met rimpelringen
water = cyl(RB * 0.93, 0.02, verts=NB, loc=(0, 0, 0.4), material=WATER, rot=(0, 0, math.pi / NB))
for r in (0.55, 0.85):
    lathe([(r, 0.411), (r + 0.02, 0.413), (r + 0.04, 0.411)], verts=16, material=SPRAY, cap0=False, cap1=False)
# --- middenzuil met twee schalen
col = lathe([(0.36, 0.3), (0.36, 0.42), (0.28, 0.48), (0.2, 0.55), (0.17, 0.75), (0.18, 0.95), (0.24, 1.02), (0.24, 1.08)],
            verts=10, material=STONE, cap0=False, cap1=False)
bowl1 = lathe([(0.2, 1.05), (0.55, 1.12), (0.8, 1.25), (0.82, 1.33), (0.74, 1.33), (0.5, 1.22), (0.0, 1.2)], verts=14, material=STONE)
w1 = cyl(0.73, 0.02, verts=14, loc=(0, 0, 1.3), material=WATER)
col2 = lathe([(0.12, 1.3), (0.1, 1.55), (0.14, 1.65), (0.14, 1.7)], verts=8, material=STONE_D, cap0=False, cap1=False)
bowl2 = lathe([(0.1, 1.68), (0.3, 1.74), (0.42, 1.84), (0.42, 1.89), (0.36, 1.89), (0.0, 1.8)], verts=10, material=STONE)
w2 = cyl(0.36, 0.02, verts=10, loc=(0, 0, 1.87), material=WATER)
# bekroning: knop + fontein-straaltje
fin = lathe([(0.08, 1.85), (0.1, 1.95), (0.06, 2.05), (0.1, 2.15), (0.0, 2.25)], verts=8, material=STONE_D)
jet = tube([(0, 0, 2.2), (0, 0, 2.45), (0, 0, 2.55)], [0.05, 0.035, 0.0], verts=6, material=SPRAY, smooth=True)
# vallende waterstralen over de schaalranden (bogen)
for k in range(6):
    a = TAU * k / 6 + 0.25
    d = Vector((math.cos(a), math.sin(a), 0))
    pts = [d * 0.42 + Vector((0, 0, 1.88)), d * 0.52 + Vector((0, 0, 1.75)), d * 0.6 + Vector((0, 0, 1.55)), d * 0.64 + Vector((0, 0, 1.32))]
    tube(pts, [0.03, 0.035, 0.03, 0.025], verts=4, material=SPRAY, smooth=True, squash=(1, 1.6))
for k in range(8):
    a = TAU * k / 8
    d = Vector((math.cos(a), math.sin(a), 0))
    pts = [d * 0.82 + Vector((0, 0, 1.33)), d * 0.95 + Vector((0, 0, 1.15)), d * 1.04 + Vector((0, 0, 0.8)), d * 1.08 + Vector((0, 0, 0.42))]
    tube(pts, [0.035, 0.04, 0.035, 0.03], verts=4, material=SPRAY, smooth=True, squash=(1, 1.6))
# spatbolletjes waar de stralen het water raken
for k in range(8):
    a = TAU * k / 8
    ico(0.07, loc=(1.08 * math.cos(a), 1.08 * math.sin(a), 0.42), sub=1, material=SPRAY, scale=(1, 1, 0.5), smooth=True)
# --- mosplekken op de rand
for k in range(5):
    a = rnd.uniform(0, TAU)
    m = ico(0.14, sub=1, material=MOSS, scale=(1.4, 1.0, 0.35), jitter=0.02, seed=k)
    T(m, rot=(0, 0, math.degrees(a)), loc=(RB * 1.02 * math.cos(a), RB * 1.02 * math.sin(a), 0.55))


# --- twee stenen banken op de plaveiring (links en rechts)
def bench(angle):
    P = []
    P.append(box((1.3, 0.42, 0.1), loc=(0, 0, 0.46), material=STONE, bevel=0.025))
    for x in (-0.48, 0.48):
        P.append(box((0.16, 0.34, 0.4), loc=(x, 0, 0.23), material=STONE_D, bevel=0.02))
        P.append(box((0.24, 0.4, 0.06), loc=(x, 0, 0.04), material=STONE_D))
    # leuning met krul
    P.append(box((1.2, 0.08, 0.36), loc=(0, 0.2, 0.72), rot=(-0.12, 0, 0), material=STONE, bevel=0.02))
    for x in (-0.62, 0.62):
        P.append(cyl(0.09, 0.1, verts=8, loc=(x, 0.18, 0.88), rot=(0, math.pi / 2, 0), material=STONE_D))
    o = join(P, 'bench')
    d = Vector((math.cos(angle), math.sin(angle), 0))
    return T(o, rot=(0, 0, math.degrees(angle) - 90), loc=d * 2.15)


bench(math.radians(10))
bench(math.radians(170))
# graspluk en struikjes naast de banken
for k, ang in enumerate((40, 140, 220, 320)):
    a = math.radians(ang)
    b = ico(0.28, sub=2, material=MOSS, scale=(1.1, 1.0, 0.8), jitter=0.04, seed=20 + k)
    T(b, loc=(2.3 * math.cos(a), 2.3 * math.sin(a), 0.2))
o = join_all('stone_bench_fountain')
shade_smooth(o, 50)
report()
done('castle', 'stone_bench_fountain', kind='hero', footprint=2.5,
     notes='Pleinfontein: achthoekig stenen bekken met pilasters en dekstenen, middenzuil met twee schalen en bekroning, vallende waterstralen en spatten, rimpelend water, mosplekken, geplaveide cirkel met twee stenen banken en struikjes')
