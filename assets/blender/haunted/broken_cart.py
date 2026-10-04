import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/haunted'); from _deco import *

WOOD = mat('wood', '#6a4630', rough=0.85)
WOOD_D = mat('wood_dark', '#3b2820', rough=0.9)
IRON = mat('iron', '#2b2733', rough=0.45, metal=0.6)
MOSS = mat('moss', '#4a6e30', rough=1.0)
GLOW = mat('glow_lamp', '#ffd36a', rough=0.4, emit='#ffb53a', emit_strength=3.0)

rnd = random.Random(4)
L, Wd, BZ = 1.6, 0.9, 0.55
# --- kar, gekanteld: rechterwiel kapot, laadbak zakt naar rechts (+X) en rust op de grond
cart = []
cart.append(box((L, Wd, 0.06), loc=(0, 0, BZ), material=WOOD_D))
for i in range(5):
    x = -L / 2 + 0.16 + i * (L - 0.32) / 4
    cart.append(box((0.26, Wd - 0.04, 0.025), loc=(x, 0, BZ + 0.045), material=WOOD))
for sy in (-1, 1):
    for k, z in enumerate((BZ + 0.14, BZ + 0.32)):
        if sy < 0 and k == 1:
            # gebroken plank aan de voorkant
            cart.append(box((L * 0.55, 0.045, 0.13), loc=(-L * 0.2, sy * Wd / 2, z), material=WOOD))
            cart.append(box((L * 0.25, 0.045, 0.13), loc=(L * 0.36, sy * Wd / 2 - 0.08, z - 0.12), rot=(0.25, 0.6, 0), material=WOOD))
        else:
            cart.append(box((L + 0.04, 0.045, 0.13), loc=(0, sy * Wd / 2, z), material=WOOD if k else WOOD_D))
    for x in (-L / 2 + 0.04, 0, L / 2 - 0.04):
        cart.append(box((0.07, 0.07, 0.42), loc=(x, sy * (Wd / 2 + 0.04), BZ + 0.18), material=WOOD_D))
cart.append(box((0.045, Wd, 0.3), loc=(-L / 2, 0, BZ + 0.22), material=WOOD))
# disselboom naar -X, steunt op de grond
cart.append(plank((-L / 2 + 0.1, 0, BZ - 0.04), (-L / 2 - 1.0, 0.05, 0.05), w=0.08, t=0.08, material=WOOD))
cart.append(box((0.06, 0.55, 0.06), loc=(-L / 2 - 0.8, 0.05, 0.15), material=WOOD))
# as
cart.append(rod((-0.15, -Wd / 2 - 0.2, 0.42), (-0.15, Wd / 2 + 0.2, 0.42), r=0.035, verts=5, material=IRON))
# heel wiel links (-Y kant)
def wheel(R=0.42, broken=False):
    P = []
    seg = 10
    rim = lathe([(R, -0.04), (R, 0.04), (R - 0.07, 0.04), (R - 0.07, -0.04), (R, -0.04)], verts=seg, material=WOOD, cap0=False, cap1=False)
    if broken:
        bm = bmesh.new(); bm.from_mesh(rim.data)
        dl = [f for f in bm.faces if 1.6 < (math.atan2(f.calc_center_median().y, f.calc_center_median().x) % TAU) < 3.4]
        bmesh.ops.delete(bm, geom=dl, context='FACES')
        bm.to_mesh(rim.data); bm.free()
    P.append(rim)
    P.append(cyl(0.08, 0.14, verts=6, material=WOOD_D))
    for k in range(6):
        if broken and k in (2, 3):
            continue
        a = TAU * k / 6 + 0.3
        P.append(plank((0.06 * math.cos(a), 0.06 * math.sin(a), 0), ((R - 0.03) * math.cos(a), (R - 0.03) * math.sin(a), 0), w=0.04, t=0.035, up=(0, 0, 1), material=WOOD))
    return join(P, 'wheel')
w1 = wheel()
T(w1, rot=(90, 0, 0), loc=(-0.15, -Wd / 2 - 0.15, 0.42))
cart_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
# alles kantelen om de linker wielas-lijn: rechterkant (+Y) zakt
for o in cart_objs:
    T(o, rot=(-16, 0, 0), pivot=(0, -Wd / 2 - 0.15, 0.0))
# kapot wiel plat tegen de kar aan
w2 = wheel(broken=True)
T(w2, rot=(8, -6, 20), loc=(0.55, Wd / 2 + 0.55, 0.05))
# losse planken en spaak
plank((0.9, 0.2, 0.03), (1.4, -0.15, 0.03), w=0.14, t=0.03, material=WOOD)
plank((0.75, -0.75, 0.02), (1.1, -0.65, 0.05), w=0.04, t=0.03, material=WOOD)
# mos en een gloeiende lantaarn die nog aan de kar hangt
for k, (x, y) in enumerate(((-0.4, 0.55), (0.6, -0.35), (-1.2, 0.3))):
    m = ico(0.18, sub=1, material=MOSS, scale=(1.4, 1.0, 0.35), jitter=0.03, seed=k)
    T(m, loc=(x, y, 0.03))
LZ = Vector((-1.05, -0.55, 0.0))   # omgevallen-maar-brandend lantaarntje op de grond
lathe([(0.09, 0.0), (0.09, 0.04), (0.0, 0.045)], verts=6, material=IRON, loc=LZ)
lathe([(0.065, 0.04), (0.07, 0.22)], verts=6, material=GLOW, loc=LZ, cap0=False)
lathe([(0.1, 0.22), (0.06, 0.29), (0.0, 0.33)], verts=6, material=IRON, loc=LZ)
for k in range(3):
    a = TAU * k / 3
    rod(LZ + Vector((0.075 * math.cos(a), 0.075 * math.sin(a), 0.04)), LZ + Vector((0.075 * math.cos(a), 0.075 * math.sin(a), 0.22)), r=0.012, verts=3, material=IRON)
torus(0.05, 0.01, loc=LZ + Vector((0, 0, 0.36)), rot=(math.pi / 2, 0, 0), seg=6, ring=3, material=IRON)
# pompoen in de bak
sphere(0.16, loc=(-0.25, 0.1, 0.0), seg=8, rings=5, material=GLOW, scale=(1, 1, 0.8)) if False else None
o = join_all('broken_cart')
# ondergrond: alles boven z=0 houden
clip_below(o, 0.0)
shade_smooth(o, 35)
report()
done('haunted', 'broken_cart', kind='scatter', footprint=1.3, center=True,
     notes='Gebroken houten kar: laadbak met losse plankjes en een gebroken zijplank, zakt scheef weg; één heel spaakwiel, het kapotte wiel ligt ernaast, disselboom op de grond, losse planken, mosplekken en een nog brandend lantaarntje (glow_lamp)')
