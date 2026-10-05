import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from dkit import *
from dkit import _obj

# Witch on a broomstick (LIFE_BRIEF "haunted/witch"). Origin = broom CENTRE, broom along Y:
# handle to -Y (front), bristles at +Y (back). Up = +Z, left = +X.

# ---------------------------------------------------------------- materials (6)
PURPLE = mat('witch_purple', '#8c3fd6', rough=0.6)
BLACK = mat('witch_black', '#25222e', rough=0.7)
SKIN = mat('witch_skin', '#86d65a', rough=0.55)
WOOD = mat('broom_wood', '#8b5a34', rough=0.8)
STRAW = mat('straw', '#f0aa35', rough=0.85)
WHITE = mat('witch_white', '#f6f3ea', rough=0.5)

B = []
# ---------------------------------------------------------------- broom
stick = bezier(V(0, -0.9, 0.05), V(0, -0.45, 0.0), V(0, 0.0, -0.005), V(0, 0.46, 0.0), n=7)
B.append(tube(stick, [0.03, 0.028, 0.027, 0.026, 0.026, 0.026, 0.027, 0.028], seg=6, material=WOOD))
B.append(ell(V(0, -0.9, 0.05), (0.045, 0.04, 0.045), seg=6, rings=4, material=WOOD))      # knob at the handle end
B.append(ell(V(0.025, -0.62, 0.025), (0.018, 0.02, 0.018), seg=5, rings=3, material=WOOD))  # knot
# bristles: core bundle + fanned straw spikes, purple bindings
B.append(lathe([(0.04, 0.0), (0.075, 0.08), (0.13, 0.25), (0.16, 0.42), (0.12, 0.5), (0.0, 0.5)], seg=9, material=STRAW,
               M=Matrix.Translation((0, 0.4, 0)) @ rotm((-90, 0, 0))))
rnd = random.Random(7)
for i in range(13):
    a = TAU * i / 13 + rnd.uniform(-0.1, 0.1)
    r0 = 0.1
    base = V(math.cos(a) * r0 * 0.7, 0.62, math.sin(a) * r0 * 0.7)
    tipv = V(math.cos(a) * rnd.uniform(0.15, 0.21), 0.9 + rnd.uniform(-0.02, 0.0), math.sin(a) * rnd.uniform(0.15, 0.21))
    B.append(spike(base, tipv - base, r=0.045, h=(tipv - base).length, seg=4, material=STRAW))
for y, r in ((0.45, 0.068), (0.52, 0.09)):
    B.append(band(V(0, y, 0), V(0, 1, 0), r, 0.035, seg=10, material=PURPLE, bulge=1.08))

# ---------------------------------------------------------------- witch (sits on the stick, leaning forward)
HIP = V(0, 0.08, 0.06)
# skirt with a jagged hem, draped over the stick
def skirt(u, v):
    a = TAU * u
    top_r, bot_r = 0.13, 0.27
    r = top_r + (bot_r - top_r) * (v ** 0.8)
    z = 0.3 - 0.36 * v
    jag = 0.045 * v * v * (1 if (round(u * 14) % 2 == 0) else -1)
    rx = r * (1.15 if abs(math.cos(a)) > 0.3 else 1.0)
    return V(math.cos(a) * rx * 1.05, 0.06 + math.sin(a) * r * 0.85, z + jag - 0.04 * max(0, -math.sin(a)) * v)
B.append(surf(skirt, 20, 3, material=BLACK, close_u=True))
# torso + chest (leaning forward)
TC = V(0, 0.03, 0.42)
B.append(ell(TC, (0.13, 0.11, 0.16), seg=8, rings=6, material=BLACK, rot=(-14, 0, 0)))
B.append(band(V(0, 0.055, 0.29), V(0, -0.25, 1), 0.135, 0.04, seg=8, material=PURPLE, bulge=1.06))     # sash
B.append(ell(V(0, -0.085, 0.295), (0.035, 0.012, 0.03), seg=6, rings=3, p=0.6, material=STRAW, rot=(-14, 0, 0)))   # buckle
# arms reaching forward to the stick, green hands gripping it
for sx in (-1, 1):
    SH = V(sx * 0.12, 0.0, 0.52)
    EL = V(sx * 0.17, -0.18, 0.33)
    HA = V(sx * 0.055, -0.36, 0.06)
    B.append(tube([SH, EL, HA + V(0, 0.05, 0.035)], [0.055, 0.05, 0.068], seg=6, material=BLACK))
    B.append(ell(HA, (0.045, 0.05, 0.04), seg=6, rings=5, material=SKIN))
    B.append(ell(HA + V(-sx * 0.035, -0.02, 0.0), (0.016, 0.03, 0.016), seg=5, rings=3, material=SKIN))   # thumb
# legs astride the stick: purple/white striped stockings + pointy black boots with curled toes
for sx in (-1, 1):
    hp = V(sx * 0.1, 0.0, 0.02)
    kn = V(sx * 0.2, -0.16, -0.08)
    an = V(sx * 0.17, -0.06, -0.36)
    path = bezier(hp, kn + V(0, 0.0, 0.08), kn + V(0, 0.02, -0.06), an, n=8)
    for i in range(len(path) - 1):
        B.append(tube([path[i], path[i + 1]], [0.05 - 0.01 * i / 8, 0.05 - 0.01 * (i + 1) / 8], seg=5,
                      material=PURPLE if i % 2 == 0 else WHITE, cap=False))
    boot = bezier(an + V(0, 0.03, -0.02), an + V(0, -0.06, -0.07), an + V(0, -0.2, -0.05), an + V(0, -0.24, 0.03), n=5)
    B.append(tube(boot, [0.052, 0.058, 0.045, 0.03, 0.018, 0.008], seg=6, material=BLACK))
    B.append(band(an + V(0, 0.02, 0.0), an - kn, 0.05, 0.03, seg=6, material=BLACK, bulge=1.15))

# head: green face, long nose with a wart, big grin, big eyes, orange hair
HC = V(0, -0.07, 0.74)
NH = len(B)
B.append(ell(HC, (0.15, 0.14, 0.15), seg=12, rings=7, material=SKIN,
             shape=lambda n: Vector((n.x, n.y, n.z - 0.12 * n.z * n.z * (1 if n.z < 0 else 0) + 0.0))))
nose = bezier(HC + V(0, -0.12, 0.0), HC + V(0, -0.2, 0.0), HC + V(0, -0.24, -0.035), n=4)
B.append(tube(nose, [0.04, 0.032, 0.022, 0.014, 0.006], seg=5, material=SKIN))
B.append(ell(HC + V(0.022, -0.2, 0.005), (0.012, 0.012, 0.012), seg=5, rings=3, material=SKIN))   # wart
for sx in (-1, 1):
    B += eye_lo(HC + V(sx * 0.06, -0.115, 0.045), d=(sx * 0.35, -1, 0.1), r=0.045, white=WHITE, black=BLACK, depth=0.6,
                tall=1.2, pupil=0.5, look=(-sx * 0.25, 0, 0.1), seg=8)
    # eyebrows (mischievous)
    br = bezier(HC + V(sx * 0.025, -0.14, 0.1), HC + V(sx * 0.06, -0.135, 0.115), HC + V(sx * 0.1, -0.11, 0.12), n=3)
    B.append(tube(br, 0.008, seg=4, material=BLACK))
# big grin: dark crescent + white teeth on the upper lip
gr = [HC + V(0.1 * math.sin(t), -0.15 * math.cos(t * 0.8) + 0.0, -0.06 - 0.035 * math.cos(t)) for t in
      [(-1.25 + 2.5 * k / 8) for k in range(9)]]
B.append(tube(gr, [0.008, 0.016, 0.024, 0.029, 0.03, 0.029, 0.024, 0.016, 0.008], seg=5, material=BLACK, flat=0.4))
B.append(tube([p + V(0, -0.01, 0.017) for p in gr[1:-1]], [0.006, 0.009, 0.011, 0.012, 0.011, 0.009, 0.006], seg=4,
              material=WHITE, flat=0.5))
# hair: orange puffs at the sides + strands flowing back
for sx in (-1, 1):
    B.append(ell(HC + V(sx * 0.13, 0.04, -0.02), (0.06, 0.08, 0.09), seg=6, rings=4, material=STRAW, rot=(20, 0, 0)))
    for k in (1,):
        st = bezier(HC + V(sx * (0.08 + 0.04 * k), 0.06, 0.05), HC + V(sx * (0.14 + 0.03 * k), 0.2, -0.02),
                    HC + V(sx * (0.12 + 0.05 * k), 0.34, -0.1 + 0.05 * k), n=3)
        B.append(tube(st, [0.042, 0.034, 0.02, 0.006], seg=5, material=STRAW))
B.append(ell(HC + V(0, 0.09, 0.0), (0.12, 0.08, 0.12), seg=7, rings=5, material=STRAW))
# pointy purple hat with a wide brim, black band and straw buckle; tip bends backwards
HB = HC + V(0, 0.01, 0.1)
B.append(lathe([(0.0, -0.012), (0.3, -0.006), (0.31, 0.006), (0.0, 0.016)], seg=16, material=PURPLE,
               M=Matrix.Translation(HB) @ rotm((-10, 0, 0))))
hat = bezier(HB, HB + V(0, 0.03, 0.25), HB + V(0, 0.1, 0.38), HB + V(0, 0.25, 0.44), n=6)
B.append(tube(hat, [0.15, 0.125, 0.095, 0.065, 0.04, 0.02, 0.004], seg=10, material=PURPLE, round_end=True))
B.append(band(hat[0] + V(0, 0.0, 0.035), hat[1] - hat[0], 0.145, 0.05, seg=10, material=BLACK, bulge=1.04))
B.append(ell(hat[0] + V(0, -0.15, 0.04), (0.035, 0.012, 0.03), seg=6, rings=3, p=0.5, material=STRAW, rot=(-8, 0, 0)))
# slightly enlarge the head + hat for cartoon proportions
SH_ = Matrix.Translation(HC + V(0, 0, -0.1)) @ Matrix.Diagonal((1.12, 1.12, 1.12, 1)) @ Matrix.Translation(-(HC + V(0, 0, -0.1)))
for o in B[NH:]:
    xf(o, SH_)
body = part(B, 'body', (0, 0, 0), angle=60)

# ---------------------------------------------------------------- cape: pivot at the shoulders, flowing backwards
SHC = V(0, 0.07, 0.56)
def cape_fn(u, v):
    x = (u - 0.5)
    w = 0.15 + 0.25 * v                       # widens towards the hem
    y = SHC.y + 0.05 + 0.5 * v - 0.06 * v * v
    z = SHC.z - 0.18 * v - 0.26 * v * v + 0.05 * math.sin(u * TAU * 2.0) * v * v
    wrap = 0.09 * (1 - (2 * x) ** 2) * (1 - 0.6 * v)  # rounds over the back
    return V(x * 2 * w, y + wrap, z + wrap * 0.6)
cape = surf(cape_fn, 8, 5, material=PURPLE)
C = [cape, tube([V(-0.14, 0.03, 0.56), V(0, 0.09, 0.61), V(0.14, 0.03, 0.56)], 0.024, seg=5, material=BLACK)]   # collar
part(C, 'cape', SHC, angle=70)

# ---------------------------------------------------------------- cat: tiny black cat sitting on the bristles, pivot at its feet
CF = V(0, 0.76, 0.15)
K = []
K.append(ell(CF + V(0, 0.01, 0.075), (0.065, 0.07, 0.08), seg=7, rings=5, material=BLACK))         # body (sitting)
for sx in (-1, 1):
    K.append(ell(CF + V(sx * 0.03, -0.045, 0.012), (0.018, 0.028, 0.014), seg=5, rings=3, material=BLACK))   # front paws
KH = CF + V(0, -0.025, 0.19)
K.append(ell(KH, (0.068, 0.058, 0.058), seg=8, rings=5, material=BLACK))
for sx in (-1, 1):
    K.append(spike(KH + V(sx * 0.04, 0.0, 0.035), (sx * 0.4, 0.05, 1), r=0.025, h=0.06, seg=4, material=BLACK))
    K.append(frame(ell(V(0, 0, 0), (0.021, 0.01, 0.024), seg=6, rings=4, material=STRAW), KH + V(sx * 0.028, -0.047, 0.008), (sx * 0.3, -1, 0.05)))
    K.append(frame(ell(V(0, 0, 0), (0.006, 0.006, 0.019), seg=4, rings=3, material=BLACK), KH + V(sx * 0.029, -0.056, 0.008), (sx * 0.3, -1, 0.05)))
K.append(ell(KH + V(0, -0.058, -0.012), (0.009, 0.006, 0.006), seg=5, rings=3, material=PURPLE))     # tiny nose
tail = bezier(CF + V(0.04, 0.06, 0.03), CF + V(0.12, 0.1, 0.05), CF + V(0.1, 0.12, 0.18), CF + V(0.06, 0.09, 0.22), n=6)
K.append(tube(tail, [0.016, 0.015, 0.014, 0.013, 0.012, 0.011, 0.01], seg=4, material=BLACK, round_end=True))
for o in K:
    xf(o, Matrix.Translation(CF) @ Matrix.Diagonal((1.3, 1.3, 1.3, 1)) @ Matrix.Translation(-CF))
part(K, 'cat', CF, angle=60)

std_view()
print_ext()
if '--close' in sys.argv:
    closeup('witch', (0, -0.1, 0.75), 1.4, d=(0.35, -1, 0.25))
    sys.exit()
notes = ('Witch on a 1.8 m broomstick, origin (0,0,0) = broom CENTRE; broom along Y, handle tip at y=-0.9 (front, -Y), '
         'bristles to y=+0.9 (back). Parts/pivots: body (origin 0,0,0: broom + witch: pointy purple hat bending back, green face '
         'with a big grin, orange hair, black dress with jagged hem, purple/white striped stockings, pointy boots); '
         'cape (purple, flowing backwards, pivot at the shoulders %s); cat (tiny black cat sitting on the bristles, pivot at its '
         'feet %s, yellow eyes). Materials: witch_purple, witch_black, witch_skin, broom_wood, straw, witch_white.'
         % (fmt(SHC), fmt(CF)))
finish('haunted', 'witch', kind='char', footprint=0.9, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('witch', dirs={'front': (0, -1, 0.15), 'side': (1, 0, 0.1), 'back': (-0.7, 1, 0.4), 'top': (0.2, -0.4, 1)})
    montage('witch', keys=('front', 'side', 'back', 'top'))
