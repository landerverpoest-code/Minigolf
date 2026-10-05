import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
sys.path.insert(0, '/home/user/Minigolf/assets/blender/space')
from dkit import *
from dkit import _obj

# Flying saucer for the ambient-life wave (LIFE_BRIEF "space/ufo").
# NOTE: saved as `ufo_flyer` because `space/ufo` already exists (a grounded hero model) and must not be modified.

# ---------------------------------------------------------------- materials (6)
METAL = mat('ufo_metal', '#c3cfdd', rough=0.3, metal=0.4)
TRIM = mat('ufo_trim', '#30236a', rough=0.35, metal=0.3)
GLASS = mat('ufo_glass', '#c8f6ff', rough=0.08, alpha=0.22)
ALIEN = mat('alien', '#7fe04a', rough=0.5)
LIGHTS = mat('glow_ufo_lights', '#ffe14a', rough=0.4, emit='#ffc61a', emit_strength=3.0)
BEAM = mat('glow_beam', '#b6ffcf', rough=0.5, emit='#8dffb8', emit_strength=1.6, alpha=0.32)

B = []
SEG = 24
# ---------------------------------------------------------------- saucer hull (centre of the rim plane = origin)
RIM = 1.5
low = lathe([(0.0, -0.33), (0.36, -0.33), (0.8, -0.26), (1.25, -0.15), (RIM, -0.02)],
            seg=SEG, material=METAL, caps=(True, False))
B.append(low)
up = lathe([(RIM, 0.02), (1.3, 0.1), (0.95, 0.2), (0.74, 0.27), (0.0, 0.28)], seg=SEG, material=METAL,
           caps=(False, True))
B.append(up)
# rim band (dark) between the two hull halves
B.append(lathe([(RIM - 0.02, -0.045), (RIM + 0.045, 0.0), (RIM - 0.02, 0.045)], seg=SEG, material=TRIM, caps=(False, False)))
# raised panel ring on the upper hull + dome seat collar
B.append(lathe([(1.14, 0.142), (1.1, 0.175), (1.04, 0.168)], seg=SEG, material=TRIM, caps=(False, False)))
B.append(lathe([(0.84, 0.25), (0.8, 0.33), (0.7, 0.32)], seg=SEG, material=TRIM, caps=(False, False)))
# emitter at the bottom (glowing ring around the beam start)
B.append(lathe([(0.36, -0.33), (0.29, -0.375), (0.2, -0.345)], seg=16, material=LIGHTS, caps=(False, False)))
B.append(lathe([(0.2, -0.345), (0.0, -0.35)], seg=16, material=TRIM, caps=(False, False)))

# ring of coloured lights on the rim
NL = 12
for i in range(NL):
    a = TAU * (i + 0.5) / NL
    c = V(math.cos(a) * (RIM + 0.05), math.sin(a) * (RIM + 0.05), 0.0)
    B.append(ell(c, (0.085, 0.085, 0.075), seg=6, rings=4, material=LIGHTS))
# small portholes on the upper slope, between the big lights
for i in range(6):
    a = TAU * i / 6 + 0.25
    r = 0.98
    B.append(ell(V(math.cos(a) * r, math.sin(a) * r, 0.19), (0.05, 0.05, 0.03), seg=6, rings=4, material=LIGHTS))

# ---------------------------------------------------------------- glass dome
DZ = 0.3
dome = ell(V(0, 0, DZ), (0.76, 0.76, 0.74), seg=20, rings=10, material=GLASS)
bm = bmesh.new(); bm.from_mesh(dome.data)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < DZ - 0.01], context='VERTS')
bm.to_mesh(dome.data); bm.free()
B.append(dome)
# antenna on top of the dome
B.append(cyl_between((0, 0, DZ + 0.73), (0, 0, DZ + 0.9), 0.018, seg=6, material=TRIM))
B.append(ell(V(0, 0, DZ + 0.93), (0.05, 0.05, 0.05), seg=8, rings=5, material=LIGHTS))

# ---------------------------------------------------------------- tiny green alien waving inside the dome
F = DZ  # floor height inside the dome
NB = len(B)
# little control console in front of the alien
B.append(ell(V(0, -0.36, F + 0.1), (0.16, 0.08, 0.1), seg=8, rings=5, p=0.7, material=TRIM))
B.append(ell(V(-0.06, -0.39, F + 0.2), (0.025, 0.025, 0.025), seg=6, rings=4, material=LIGHTS))
B.append(cyl_between((0.07, -0.36, F + 0.19), (0.07, -0.33, F + 0.27), 0.012, seg=5, material=METAL))
B.append(ell(V(0.07, -0.33, F + 0.28), (0.03, 0.03, 0.03), seg=6, rings=4, material=LIGHTS))
# body (pear) and legs
B.append(ell(V(0, 0, F + 0.2), (0.12, 0.1, 0.15), seg=8, rings=5, material=ALIEN,
             shape=lambda n: Vector((n.x * (1.15 - 0.3 * n.z), n.y * (1.15 - 0.3 * n.z), n.z))))
for sx in (-1, 1):
    B.append(ell(V(sx * 0.06, -0.03, F + 0.04), (0.05, 0.07, 0.035), seg=6, rings=4, material=ALIEN))
# head: big, wide at the top
HC = V(0, -0.01, F + 0.47)
B.append(ell(HC, (0.19, 0.16, 0.15), seg=12, rings=7, material=ALIEN,
             shape=lambda n: Vector((n.x * (1.0 + 0.12 * n.z), n.y, n.z - 0.12 * n.x * n.x))))
# big black almond eyes with a light glint
for sx in (-1, 1):
    ec = HC + V(sx * 0.085, -0.13, 0.015)
    e = ell(V(0, 0, 0), (0.065, 0.03, 0.04), seg=8, rings=5, material=TRIM)
    xf(e, Matrix.Translation(ec) @ rotm((0, sx * -22, sx * -25)))
    B.append(e)
    B.append(ell(ec + V(sx * 0.02, -0.03, 0.018), (0.014, 0.008, 0.014), seg=6, rings=4, material=METAL))
# smile
sm = bezier(HC + V(-0.055, -0.145, -0.07), HC + V(0, -0.17, -0.11), HC + V(0.055, -0.145, -0.07), n=4)
B.append(tube(sm, 0.01, seg=4, material=TRIM))
# antennae with glowing tips
for sx in (-1, 1):
    pts = bezier(HC + V(sx * 0.07, 0.0, 0.13), HC + V(sx * 0.1, 0.0, 0.25), HC + V(sx * 0.17, -0.02, 0.29), n=5)
    B.append(tube(pts, [0.014, 0.012, 0.011, 0.01, 0.009, 0.008], seg=5, material=ALIEN))
    B.append(ell(pts[-1], (0.03, 0.03, 0.03), seg=6, rings=4, material=LIGHTS))
# right arm (-X) raised high, waving; left arm on the console lever
SR = V(-0.1, -0.01, F + 0.29)
wave = bezier(SR, SR + V(-0.1, 0.0, 0.03), SR + V(-0.16, -0.03, 0.17), n=5)
B.append(tube(wave, [0.03, 0.028, 0.026, 0.025, 0.024, 0.024], seg=5, material=ALIEN))
hand = wave[-1] + V(-0.01, -0.01, 0.04)
B.append(ell(hand, (0.04, 0.025, 0.045), seg=8, rings=5, material=ALIEN))
for k in (-1, 1):   # spread fingers
    B.append(ell(hand + V(k * 0.022, -0.002, 0.04), (0.012, 0.012, 0.026), seg=5, rings=3, material=ALIEN))
SL = V(0.1, -0.01, F + 0.29)
arm2 = bezier(SL, SL + V(0.05, -0.08, -0.04), V(0.07, -0.31, F + 0.29), n=5)
B.append(tube(arm2, 0.026, seg=5, material=ALIEN))

# enlarge the alien + console so it reads from afar
SA = Matrix.Translation((0, 0, F)) @ Matrix.Diagonal((1.3, 1.3, 1.3, 1)) @ Matrix.Translation((0, 0, -F))
for o in B[NB:]:
    xf(o, SA)
body = part(B, 'body', (0, 0, 0), angle=60)

# ---------------------------------------------------------------- beam: translucent cone of light, origin at its top
TOP = -0.35
L = 2.5
BM = []
BM.append(lathe([(1.05, TOP - L), (0.3, TOP)], seg=24, material=BEAM, caps=(False, False), smooth=True))
for t in (0.4, 0.78):   # scanning rings inside the beam
    r = 0.3 + (1.05 - 0.3) * t - 0.02
    z = TOP - L * t
    BM.append(lathe([(r, z - 0.035), (r + 0.02, z), (r, z + 0.035)], seg=24, material=BEAM, caps=(False, False)))
beam = part(BM, 'beam', (0, 0, TOP), angle=80)

std_view()
print_ext()
notes = ('Flying saucer ~3.2 m wide (named ufo_flyer because space/ufo already exists as a grounded hero). Parts/pivots '
         '(Blender coords, front -Y): body (origin (0,0,0) = saucer CENTRE in the rim plane; metallic saucer, dark rim band, '
         'ring of 14 rim lights + 14 small upper lights + emitter ring = glow_ufo_lights, glass dome ufo_glass (alpha 0.32) '
         'with a tiny green alien waving inside, antenna); beam (translucent light cone, origin at its top = saucer underside '
         '(0,0,-0.35), points down -Z, 2.5 m long, top radius 0.3, bottom radius 1.05, open ends, 3 scanning rings; material '
         'glow_beam (alpha 0.32), the game fades it). Materials: ufo_metal, ufo_trim, ufo_glass, alien, glow_ufo_lights, glow_beam.')
finish('space', 'ufo_flyer', kind='char', footprint=1.6, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('ufo_flyer', dirs={'front': (0, -1, 0.25), 'side': (1, 0, 0.1), 'top': (0.2, -0.5, 1), 'under': (0.4, -0.6, -0.5)})
    montage('ufo_flyer', keys=('front', 'side', 'top', 'under'))
if '--close' in sys.argv:
    closeup('ufo_flyer', (0, 0, 0.75), 2.2, d=(0.3, -1, 0.35))
