import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert')
from mglib import *
reset()
from _kit import *

S1 = mat('sandstone', '#ddb172', rough=0.88)
S2 = mat('sandstone_dark', '#c39257', rough=0.9)
CASE = mat('limestone_casing', '#f1dcae', rough=0.7)
GOLD = mat('gold', '#f5c542', rough=0.35, metal=0.55)
DARK = mat('door_dark', '#3b2a20', rough=0.8)
rnd = random.Random(12)

B = 12.5          # basisbreedte
NC = 13           # treden in steen
HC = 0.62         # hoogte per trede
inset = 0.36      # inspringing per trede
z = 0.0
for i in range(NC):
    w = B - 2 * inset * i
    o = box((w + rnd.uniform(-0.05, 0.05), w + rnd.uniform(-0.05, 0.05), HC), loc=(rnd.uniform(-0.03, 0.03), rnd.uniform(-0.03, 0.03), z + HC / 2),
            material=S1 if i % 2 == 0 else S2, bevel=0.06)
    # verweerde hoeken: hoekpunten iets naar binnen/omlaag
    for v in o.data.vertices:
        if abs(abs(v.co.x) - w / 2) < 0.08 and abs(abs(v.co.y) - w / 2) < 0.08 and v.co.z > z + HC * 0.5 and rnd.random() < 0.35:
            v.co.z -= HC * rnd.uniform(0.2, 0.5)
    z += HC
# gladde bekleding bovenaan (nog intact)
w0 = B - 2 * inset * NC + 0.1
top_h = w0 * 0.78
casing = loft([[(-w0 / 2, -w0 / 2, z), (w0 / 2, -w0 / 2, z), (w0 / 2, w0 / 2, z), (-w0 / 2, w0 / 2, z)],
               [(-0.5, -0.5, z + top_h - 0.78), (0.5, -0.5, z + top_h - 0.78), (0.5, 0.5, z + top_h - 0.78), (-0.5, 0.5, z + top_h - 0.78)]],
              material=CASE, closed=True, cap0=True, cap1=True)
# afgebrokkelde rand van de bekleding: kleine blokjes onderaan
for k in range(10):
    side = k % 4; t = rnd.uniform(-0.4, 0.4) * w0
    p = [(t, -w0 / 2 + 0.15), (w0 / 2 - 0.15, t), (t, w0 / 2 - 0.15), (-w0 / 2 + 0.15, t)][side]
    box((rnd.uniform(0.4, 0.8), rnd.uniform(0.4, 0.8), 0.3), loc=(p[0], p[1], z + 0.1), rot=(0, 0, rnd.uniform(0, 1)), material=CASE)
# gouden topsteen
zc = z + top_h - 0.78
cap = loft([[(-0.55, -0.55, zc), (0.55, -0.55, zc), (0.55, 0.55, zc), (-0.55, 0.55, zc)], [(0, 0, zc + 1.0)]], material=GOLD, closed=True, cap0=True)
band = box((1.2, 1.2, 0.1), loc=(0, 0, zc + 0.02), material=GOLD)
# ingang op de voorkant (-Y) rond trede 3-4
ie = 3
we = B - 2 * inset * ie
box((1.0, 0.6, 1.2), loc=(0, -we / 2 + 0.15, ie * HC + 0.6), material=DARK)
box((1.5, 0.7, 0.3), loc=(0, -we / 2 + 0.12, ie * HC + 1.35), material=CASE, bevel=0.04)
for s in (-1, 1):
    box((0.25, 0.65, 1.2), loc=(s * 0.62, -we / 2 + 0.12, ie * HC + 0.6), material=CASE, bevel=0.03)
# trap naar de ingang
for k in range(ie):
    wk = B - 2 * inset * k
    box((1.6, 0.5, HC), loc=(0, -wk / 2 - 0.2, k * HC + HC / 2), material=CASE, bevel=0.04)
# puin en zand rond de voet
for k in range(12):
    a = rnd.uniform(0, 2 * math.pi)
    d = B / 2 + rnd.uniform(0.3, 1.0)
    x, y = math.cos(a) * d, math.sin(a) * d
    x = max(-B / 2 - 1, min(B / 2 + 1, x)); y = max(-B / 2 - 1, min(B / 2 + 1, y))
    if abs(x) < 1.2 and y < 0: continue
    b = box((rnd.uniform(0.3, 0.7), rnd.uniform(0.3, 0.6), rnd.uniform(0.25, 0.45)), loc=(x, y, 0.18), rot=(rnd.uniform(-0.2, 0.2), rnd.uniform(-0.2, 0.2), rnd.uniform(0, 3)),
            material=S1 if k % 2 else S2)
# zandduinen tegen twee hoeken
for (x, y, sx, sy, h) in [(B / 2 - 0.4, 1.8, 1.8, 3.4, 1.5), (-1.5, B / 2 - 0.3, 3.6, 1.6, 1.1)]:
    d = lathe([(1.0, 0.0), (0.75, 0.35), (0.4, 0.75), (0.0, 1.0)], verts=10, material=CASE, jitter=0.08, seed=int(x))
    place(d, loc=(x, y, 0), scale=(sx, sy, h))
    shade_smooth(d, 50)
for k in range(4):
    a = 0.6 + k * 1.4
    box((0.9, 0.7, 0.6), loc=(math.cos(a) * (B / 2 + 1.0), math.sin(a) * (B / 2 + 1.0) * 0.9, 0.25), rot=(0.15, -0.1, a), material=S2, bevel=0.06)
join_all('pyramid_small')
o = bpy.context.scene.objects['pyramid_small']
for v in o.data.vertices: v.co.z = max(v.co.z, 0.0)
report()
finish('desert', 'pyramid_small', kind='hero', footprint=6.6,
       notes='Kleine piramide: verweerde stenen treden, gladde bekleding bovenaan met gouden topsteen, ingang met trap aan de voorkant (-Y)')
closeup('pyramid_small')
