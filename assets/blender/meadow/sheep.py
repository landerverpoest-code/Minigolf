import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/meadow'); from _deco import *

WOOL = mat('wool', '#f4efe4', rough=0.95)
WOOL_SH = mat('wool_shade', '#e2d8c6', rough=0.95)
FACE = mat('sheep_face', '#3b3330', rough=0.8)
EYE = mat('eye_white', '#fbf8f2', rough=0.4)
GRASS = mat('grass', '#4f9c33', rough=0.85)

# --- wollig lijf: kern + bolletjes wol (kop naar -Y)
cz = 0.5
core = sphere(1.0, seg=8, rings=4, material=WOOL_SH, scale=(0.27, 0.4, 0.24), loc=(0, 0.03, cz))
puffs = []
N = 19
for i in range(N):
    # fibonacci-punten op een ellipsoide, onderkant overslaan
    zf = 1 - 2 * (i + 0.5) / N
    if zf < -0.4:
        continue
    a = i * 2.39996
    rr = math.sqrt(1 - zf * zf)
    p = Vector((0.25 * rr * math.cos(a), 0.37 * rr * math.sin(a) + 0.03, cz + 0.2 * zf))
    r = 0.15 + 0.03 * math.sin(i * 1.7)
    m = WOOL if zf > -0.1 else WOOL_SH
    puffs.append(sphere(r, loc=p, seg=6, rings=4, material=m))
print('puffs', len(puffs))

# --- kop: donker, iets naar voren en omlaag (grazend-nieuwsgierig)
head = sphere(1.0, seg=7, rings=5, material=FACE, scale=(0.12, 0.17, 0.13))
deform(head, lambda c: Vector((c.x * (1 - 0.25 * max(0, -c.y / 0.17)), c.y, c.z)))
T(head, rot=(28, 0, 0), loc=(0, -0.47, 0.60))
# wolkuif op de kop
tuft = sphere(0.085, loc=(0, -0.43, 0.72), seg=6, rings=4, material=WOOL, scale=(1.2, 1, 0.8))
# oren (platte druppels, zijwaarts)
ears = []
for s in (-1, 1):
    e = sphere(1.0, seg=5, rings=3, material=FACE, scale=(0.1, 0.035, 0.022), smooth=False)
    T(e, loc=(s * 0.09, 0, 0))
    T(e, rot=(0, s * -25, s * -18), loc=(s * 0.1, -0.42, 0.68))
    ears.append(e)
# ogen: wit met zwart pupilletje
eyes = []
for s in (-1, 1):
    eyes.append(sphere(0.032, loc=(s * 0.075, -0.55, 0.65), seg=5, rings=3, material=EYE))
    eyes.append(sphere(0.017, loc=(s * 0.085, -0.575, 0.652), seg=4, rings=3, material=FACE))
# neusje
nose = sphere(1.0, seg=6, rings=3, material=EYE, scale=(0.045, 0.02, 0.025), loc=(0, -0.625, 0.525))
set_mat(nose, WOOL_SH)

# --- poten met hoefjes
legs = []
for x, y in ((0.14, -0.2), (-0.14, -0.2), (0.14, 0.24), (-0.14, 0.24)):
    legs.append(tube([(x, y, 0), (x, y, 0.07), (x * 0.95, y, 0.36)], [0.052, 0.042, 0.048], verts=5, material=FACE, cap1=False))
# staartje
tail = sphere(0.075, loc=(0, 0.47, 0.6), seg=5, rings=3, material=WOOL)

# --- graspolletje onder de snuit
blades = []
rnd = random.Random(4)
for i in range(12):
    a = rnd.uniform(0, TAU); r = rnd.uniform(0.0, 0.07)
    cx, cy = ((0.2, -0.32), (-0.22, 0.1), (0.05, 0.4))[i % 3]
    x, y = cx + r * math.cos(a), cy + r * math.sin(a)
    h = rnd.uniform(0.1, 0.17)
    lean = Vector((rnd.uniform(-0.05, 0.05), rnd.uniform(-0.05, 0.05), 0))
    blades.append(mesh_obj([(x - 0.018, y, 0), (x + 0.018, y, 0), Vector((x, y, h)) + lean], [(0, 1, 2)], GRASS, 'blade'))

join_all("sheep")
report()
done('meadow', 'sheep', kind='scatter', footprint=0.55,
     notes='Pluizig schaap: wolkig lijf (unie van bollen), donkere kop met wolkuif, flaporen, witte oogjes, poten met hoefjes, graspolletje; kijkt naar -Y')
