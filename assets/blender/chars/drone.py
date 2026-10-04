import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from akit import *
from ccp_kit import _obj

# ---------------------------------------------------------------- materials (6)
SHELL = mat('shell', '#e4eaf2', rough=0.32, metal=0.35)        # the game recolours this one
GLASS = mat('glass', '#c4f3ff', rough=0.03, metal=0.0, alpha=0.25)
DARK = mat('dark', '#2a303d', rough=0.4, metal=0.5)
GLOW = mat('glow_eye', '#ff1a10', rough=0.3, emit='#ff1205', emit_strength=2.2)
ACC = mat('accent', '#ffb627', rough=0.3, metal=0.55)
GLOVE = mat('glove', '#e3342f', rough=0.42)

B = []
# ---------------------------------------------------------------- shell (lower bowl) + equator ring
shell = ell(V(0, 0, 0), (0.42, 0.42, 0.3), seg=16, rings=10, material=SHELL,
            shape=lambda n: Vector((n.x, n.y, min(n.z, 0.17))))
B.append(shell)
B.append(torus(R=0.415, r=0.038, loc=(0, 0, 0.045), seg=16, ring=5, material=ACC))
# panel seams / bolts around the bowl
for k in range(8):
    a = TAU * (k + 0.5) / 8
    B.append(ell(V(math.cos(a) * 0.39, math.sin(a) * 0.39, -0.09), (0.025, 0.025, 0.025), seg=4, rings=3, material=ACC))
# thruster underneath
B.append(lathe([(0.0, -0.36), (0.1, -0.36), (0.13, -0.33), (0.12, -0.27), (0.08, -0.25)], seg=12, material=DARK))
B.append(torus(R=0.12, r=0.02, loc=(0, 0, -0.3), seg=12, ring=5, material=ACC))
# ---------------------------------------------------------------- glass dome with the little face inside
B.append(ell(V(0, 0, 0.05), (0.33, 0.33, 0.32), seg=18, rings=10, material=GLASS,
             shape=lambda n: Vector((n.x, n.y, max(n.z, 0.0)))))
head = ell(V(0, 0.02, 0.16), (0.26, 0.24, 0.2), seg=12, rings=8, material=DARK)
B.append(head)
# big round eye + happy smile on the face screen (front -Y)
B.append(frame(ell(V(0, 0, 0), (0.1, 0.035, 0.11), seg=12, rings=6, material=GLOW), V(0, -0.21, 0.2), V(0, -1, 0.15)))
B.append(frame(ell(V(0, 0, 0), (0.03, 0.012, 0.035), seg=6, rings=4, material=SHELL), V(0.035, -0.245, 0.24), V(0, -1, 0.15)))
smile = [V(math.sin(a) * 0.075, -math.cos(a) * 0.2, 0.09 - 0.03 * math.cos(a * 1.0) + 0.0) for a in [math.radians(x) for x in (-40, -20, 0, 20, 40)]]
smile = [V(p.x * 1.1, -0.228 + abs(p.x) * 0.2, 0.065 + (p.x ** 2) * 5) for p in smile]
B.append(tube(smile, 0.014, seg=5, material=GLOW))
# antenna through the top of the dome
B.append(cyl_between((0, 0.02, 0.33), (0.0, 0.05, 0.5), 0.012, seg=5, material=DARK))
B.append(ell(V(0, 0.05, 0.52), (0.035, 0.035, 0.035), seg=8, rings=5, material=ACC))
# ---------------------------------------------------------------- struts + rotor ducts at the 4 diagonals
ROT = {}
RC = 0.47
for k, (sx, sy) in enumerate(((1, -1), (-1, -1), (-1, 1), (1, 1))):
    d = V(sx, sy, 0).normalized()
    c = d * (RC * math.sqrt(2) * 0.95) + V(0, 0, 0.08)
    c = V(sx * RC * 0.95, sy * RC * 0.95, 0.08)
    B.append(tube([d * 0.36 + V(0, 0, 0.02), c - d * 0.23 + V(0, 0, 0.0)], [0.045, 0.035], seg=6, material=DARK))
    B.append(torus(R=0.235, r=0.032, loc=tuple(c), seg=14, ring=4, material=SHELL))
    B.append(cyl(0.05, 0.08, loc=tuple(c + V(0, 0, -0.05)), verts=8, material=DARK))      # motor under the rotor
    ROT[k + 1] = c
body = apart(B, 'body', (0, 0, 0))
for p in body.data.polygons:
    pass

# ---------------------------------------------------------------- rotors (pivot at the rotor centre, spin around Z)
for k, c in ROT.items():
    R = [cyl(0.04, 0.03, loc=tuple(c + V(0, 0, 0.01)), verts=8, material=ACC),
         ell(c + V(0, 0, 0.03), (0.025, 0.025, 0.02), seg=6, rings=4, material=ACC)]
    for j in range(2):
        a = math.pi * j + (0.4 if k % 2 else -0.4)
        bl = ell(V(0.11, 0, 0), (0.11, 0.035, 0.008), seg=6, rings=3, material=DARK)
        xf(bl, Matrix.Translation(c + V(0, 0, 0.012)) @ Matrix.Rotation(a, 4, 'Z') @ Matrix.Rotation(math.radians(12), 4, 'X'))
        R.append(bl)
    apart(R, f'rotor_{k}', tuple(c))

# ---------------------------------------------------------------- punching arm (pivot at body centre, points -Y, glove at y=-1)
AZ = -0.11
A = [cyl_between((0, -0.2, AZ), (0, -0.4, AZ), 0.06, seg=10, material=DARK),
     cyl_between((0, -0.38, AZ), (0, -0.42, AZ), 0.075, seg=10, material=ACC)]
# scissor extender: zig-zag links in the horizontal plane
ys = [-0.42 + i * (-0.42 / 4) for i in range(5)]          # -0.42 .. -0.84
for i in range(4):
    y0, y1 = ys[i], ys[i + 1]
    for s in (-1, 1):
        A.append(cyl_between((s * 0.07, y0, AZ + s * 0.008), (-s * 0.07, y1, AZ + s * 0.008), 0.016, seg=4, material=ACC))
    A.append(ell(V(0, (y0 + y1) / 2, AZ), (0.024, 0.024, 0.03), seg=5, rings=3, material=DARK))
# glove: cuff + mitt + thumb + lace stripe
GC = V(0, -1.0, AZ)
A.append(cyl_between((0, -0.82, AZ), (0, -0.9, AZ), 0.085, seg=10, material=SHELL, r2=0.1))
A.append(ell(GC + V(0, 0.0, 0.0), (0.15, 0.15, 0.135), seg=12, rings=7, material=GLOVE,
             shape=lambda n: Vector((n.x, n.y * (1 + 0.1 * n.z), n.z * (1 - 0.1 * n.y)))))
A.append(ell(GC + V(0.0, -0.11, 0.06), (0.12, 0.06, 0.08), seg=8, rings=5, material=GLOVE))     # knuckle bulge
A.append(ell(GC + V(0.13, -0.02, -0.02), (0.05, 0.085, 0.06), seg=8, rings=5, material=GLOVE, rot=(0, 0, -15)))  # thumb
A.append(tube([GC + V(-0.04, 0.09, 0.12), GC + V(0.0, 0.11, 0.13), GC + V(0.04, 0.09, 0.12)], 0.012, seg=4, material=SHELL))
arm = apart(A, 'arm', (0, 0, 0))

report()
notes = ('Parts/pivots (Blender coords, front -Y, left=+X): body (origin 0,0,0 = body centre; round shell bowl (material shell, '
         'recolourable) with accent equator ring, glass dome (material glass, alpha 0.25) holding a dark face screen with one big '
         'round eye glow_eye + glowing smile, antenna, thruster below, 4 struts with rotor ducts (ducts also material shell)); '
         'rotor_1 %s (front-left), rotor_2 %s (front-right), rotor_3 %s (back-right), rotor_4 %s (back-left): pivot at the rotor '
         'centre, spin around Z (three.js y); arm: pivot at the body centre (0,0,0), points -Y, scissor extender + red boxing '
         'glove centred at (0,-1,%.2f) (glove front at y=-1.15); scale it along Blender Y (three.js z) to extend. Shell radius 0.42, '
         'width over the ducts ~1.36. Materials: shell, glass, dark, glow_eye, accent, glove.'
         % (fmt(ROT[1]), fmt(ROT[2]), fmt(ROT[3]), fmt(ROT[4]), AZ))
finish('chars', 'drone', kind='char', footprint=0.5, grounded=False, notes=notes)
if '--views' in sys.argv:
    views('drone', dirs={'front': (0, -1, 0.25), 'side': (1, 0, 0.3), 'top': (0.3, -0.5, 1)})
