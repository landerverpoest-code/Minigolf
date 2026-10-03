import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert')
from mglib import *
reset()
from _kit import *

SAND = mat('sandstone', '#e3bb7c', rough=0.85)
SAND2 = mat('sandstone_dark', '#c39257', rough=0.9)
TURQ = mat('turquoise', '#27bfb0', rough=0.45)
TERRA = mat('terracotta', '#c9573c', rough=0.7)
GOLD = mat('gold', '#f5c542', rough=0.35, metal=0.55)
rnd = random.Random(21)
R = 0.36


def fluted(z0, z1, r, verts=12, rib=0.07, jag_top=0.0, jag_bot=0.0, loc=(0, 0, 0), seed=0):
    rr = random.Random(seed)
    o = lathe([(r * 1.0, z0), (r * 0.97, z1)], verts=verts, material=SAND, loc=loc)
    for k, v in enumerate(o.data.vertices):
        f = (1 + rib) if (k % verts) % 2 == 0 else (1 - rib)
        v.co.x = loc[0] + (v.co.x - loc[0]) * f; v.co.y = loc[1] + (v.co.y - loc[1]) * f
        if abs(v.co.z - z1) < 1e-4 and jag_top:
            v.co.z -= rr.uniform(0, jag_top)
        if abs(v.co.z - z0) < 1e-4 and jag_bot:
            v.co.z += rr.uniform(0, jag_bot)
    return o

# --- staande, afgebroken zuil ---
box((1.05, 1.05, 0.22), loc=(0, 0, 0.11), material=SAND2, bevel=0.03)
lathe([(0.5, 0.22), (0.46, 0.34), (0.0, 0.34)], verts=12, material=SAND)
fluted(0.34, 1.75, R, jag_top=0.35, seed=1)
for z, m in ((0.5, TERRA), (0.58, TURQ), (0.66, GOLD)):
    lathe([(R * 1.1, z), (R * 1.1, z + 0.06)], verts=12, material=m, cap0=False, cap1=False)
# --- omgevallen stuk ---
piece = fluted(0.0, 1.35, R * 0.96, jag_top=0.25, jag_bot=0.2, seed=2)
for z, m in ((1.0, TERRA), (1.08, TURQ)):
    lathe([(R * 1.06, z), (R * 1.06, z + 0.06)], verts=12, material=m, cap0=False, cap1=False)
fall = join([piece] + [o for o in bpy.context.scene.objects if o.name.startswith('lathe') and o is not piece and abs(bounds([o])[0].z - 1.0) < 0.1 or (o.name.startswith('lathe') and abs(bounds([o])[0].z - 1.08) < 0.01)], 'fall')
place(fall, loc=(0.85, -0.55, R * 0.9), rot=(0, math.pi / 2 - 0.05, -0.5))
# --- lotus-kapiteel op de grond ---
cap = lathe([(0.3, 0.0), (0.33, 0.12), (0.5, 0.35), (0.66, 0.6), (0.68, 0.68), (0.0, 0.68)], verts=16,
            mats=[SAND, TURQ, GOLD], band_mats=[1, 0, 0, 0, 2, 0])
for k, v in enumerate(cap.data.vertices):
    if 0.2 < v.co.z < 0.66 and (k % 16) % 2 == 0:
        v.co.x *= 1.1; v.co.y *= 1.1   # lotusbladen
abacus = box((0.62, 0.62, 0.14), loc=(0, 0, 0.75), material=SAND2, bevel=0.03)
neck = fluted(-0.35, 0.0, 0.3, jag_bot=0.15, seed=4)
capj = join([cap, abacus, neck], 'capital')
place(capj, loc=(-1.1, -0.35, 0.5), rot=(math.pi / 2 + 0.25, 0, 0.7))
# --- puin ---
for k in range(5):
    a = rnd.uniform(0, 2 * math.pi); d = rnd.uniform(0.7, 1.4)
    rock(rnd.uniform(0.08, 0.16), loc=(math.cos(a) * d, math.sin(a) * d, 0.04), scale=(1.4, 1.0, 0.8), seed=k + 9, jitter=0.15,
         material=SAND if k % 2 else SAND2, rot_z=a)
join_all('broken_column')
o = bpy.context.scene.objects['broken_column']
for v in o.data.vertices: v.co.z = max(v.co.z, 0.0)
report()
finish('desert', 'broken_column', kind='scatter', footprint=1.2,
       notes='Afgebroken Egyptische zuil met geschilderde banden, een omgevallen zuilstuk en een lotuskapiteel op de grond')
closeup('broken_column')
