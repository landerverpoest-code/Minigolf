import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/desert'); from _deco import *

GOLD = mat('gold', '#f5c542', rough=0.35, metal=0.55)
STONE = mat('sandstone', '#e3bb7c', rough=0.85)
STONE_D = mat('sandstone_dark', '#c39257', rough=0.9)
TURQ = mat('turquoise', '#27bfb0', rough=0.45)
LAPIS = mat('lapis', '#2f4fa8', rough=0.4)

# --- getrapte sokkel met turquoise band
box((1.3, 1.3, 0.18), loc=(0, 0, 0.09), material=STONE_D, bevel=0.03)
box((1.1, 1.1, 0.42), loc=(0, 0, 0.39), material=STONE, bevel=0.03)
box((1.14, 1.14, 0.06), loc=(0, 0, 0.5), material=TURQ)
box((1.2, 1.2, 0.08), loc=(0, 0, 0.64), material=STONE_D, bevel=0.02)
# hiërogliefje-blokjes op de voorkant
for k, x in enumerate((-0.3, 0.0, 0.3)):
    box((0.12, 0.02, 0.12), loc=(x, -0.555, 0.33), material=LAPIS if k == 1 else STONE_D)
Z = 0.68
# --- gouden mestkever, kop naar -Y
shell = sphere(1.0, seg=12, rings=7, material=GOLD, scale=(0.38, 0.48, 0.3))
deform(shell, lambda c: Vector((c.x, c.y, max(c.z, -0.02) * (1 if c.z > 0 else 0.3))))
T(shell, loc=(0, 0.08, Z + 0.06))
# naad tussen de dekschilden + lapis rand
box((0.025, 0.85, 0.05), loc=(0, 0.1, Z + 0.34), rot=(0.0, 0, 0), material=LAPIS)
deform(bpy.context.scene.objects[-1], lambda c: Vector((c.x, c.y, c.z - 1.2 * (c.y - 0.1) ** 2)))
# borststuk
thor = sphere(1.0, seg=10, rings=6, material=GOLD, scale=(0.3, 0.17, 0.2))
T(thor, loc=(0, -0.42, Z + 0.12))
# kop met tandjes (clypeus)
head = sphere(1.0, seg=8, rings=5, material=GOLD, scale=(0.2, 0.12, 0.1))
T(head, loc=(0, -0.62, Z + 0.08))
for k in range(-2, 3):
    cone(0.03, 0.08, loc=(k * 0.06, -0.73, Z + 0.09), rot=(math.pi / 2, 0, 0), verts=4, material=GOLD)
for s in (-1, 1):
    sphere(0.035, loc=(s * 0.14, -0.66, Z + 0.13), seg=5, rings=3, material=LAPIS)
# zes pootjes met knik
for s in (-1, 1):
    for k, (y, a) in enumerate(((-0.4, -40), (-0.1, 0), (0.25, 40))):
        r = math.radians(a)
        p0 = Vector((s * 0.22, y, Z + 0.08))
        p1 = Vector((s * 0.45, y + math.sin(r) * 0.2, Z + 0.14))
        p2 = Vector((s * 0.55, y + math.sin(r) * 0.32, Z + 0.0))
        tube([p0, p1, p2], [0.03, 0.025, 0.018], verts=4, material=GOLD)
# zonneschijf die de kever boven zijn kop duwt
disc = cyl(0.26, 0.06, verts=12, material=GOLD, rot=(math.pi / 2, 0, 0), loc=(0, -0.78, Z + 0.42))
cyl(0.19, 0.07, verts=12, material=TURQ, rot=(math.pi / 2, 0, 0), loc=(0, -0.78, Z + 0.42))
cyl(0.1, 0.08, verts=8, material=LAPIS, rot=(math.pi / 2, 0, 0), loc=(0, -0.78, Z + 0.42))
o = join_all('scarab_statue')
shade_smooth(o, 40)
report()
done('desert', 'scarab_statue', kind='scatter', footprint=0.8,
     notes='Gouden scarabee op een getrapte zandstenen sokkel met turquoise band en hiërogliefblokjes: glanzende dekschilden met lapis-naad, borststuk, kop met tandjes, zes geknikte pootjes, duwt een gouden zonneschijf met turquoise/lapis kern')
