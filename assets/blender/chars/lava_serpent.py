import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skit import *

RED = mat('serp_red', '#c8361c', rough=0.5)
DARK = mat('serp_dark', '#2b1d22', rough=0.35, metal=0.1)
GLOW = mat('glow_lava', '#ff6a00', rough=0.5, emit='#ff5200', emit_strength=2.0)
EYES = mat('glow_eyes', '#ffd400', rough=0.3, emit='#ffb800', emit_strength=2.5)
PUP = mat('pupil', '#160c0c', rough=0.3)
TOOTH = mat('tooth', '#fff1d6', rough=0.4)

# ---------------------------------------------------------------- neck
P0, P1, P2, P3 = V(0, 0.55, -0.55), V(0, 0.95, 0.45), V(0, -0.5, 0.75), V(0, -0.08, 1.38)
cpts = bezier(P0, P1, P2, P3, n=12)
crad = [0.4 - 0.15 * (i / 12) ** 0.9 for i in range(13)]
neck = tube(cpts, crad, seg=16, material=RED, cap=True)
# tangents for the belly field
TT = [(cpts[min(i + 1, 12)] - cpts[max(i - 1, 0)]).normalized() for i in range(13)]


def belly(p):
    best = min(range(13), key=lambda i: (p - cpts[i]).length_squared)
    t = TT[best]
    F = V(0, -1, 0.2); F = (F - t * F.dot(t)).normalized()
    return -((p - cpts[best]).normalized().dot(F) - 0.45) * 6


iso_paint(neck, belly, DARK)
bp = [neck]
# glowing seams between the dark belly plates + a jagged crack down the middle
for i in range(1, 12):
    c = (cpts[i] + cpts[i + 1]) * 0.5 if i < 12 else cpts[i]
    t = (TT[i] + TT[min(i + 1, 12)]).normalized()
    F = V(0, -1, 0.2); F = (F - t * F.dot(t)).normalized()
    side = t.cross(F).normalized()
    r = (crad[i] + crad[min(i + 1, 12)]) * 0.5 * 1.005
    arc = [c + (F * math.cos(math.radians(a)) + side * math.sin(math.radians(a))) * r for a in (-58, -30, 0, 30, 58)]
    arc[2] += t * 0.03 * (1 if i % 2 else -1)
    bp.append(tube(arc, 0.02, seg=4, material=GLOW, round_end=True))
# back spikes
for i in range(2, 12, 2):
    c = cpts[i]; t = TT[i]
    B = V(0, 1, 0.3); B = (B - t * B.dot(t)).normalized()
    r = crad[i]
    base = c + B * r * 0.85
    h = 0.24 - 0.012 * i
    bp.append(tube([base, base + B * h * 0.6 - t * h * 0.15, base + B * h - t * h * 0.45], [0.09 - 0.003 * i, 0.05, 0.004], seg=6, material=DARK))

# ---------------------------------------------------------------- head
H = V(0, -0.45, 1.66)


def head_shape(n):
    x, y, z = n
    if y < 0:               # snout tapers a bit and flattens
        k = 1 - 0.22 * (-y)
        x *= k
        z *= 1 - 0.18 * (-y)
    if z < 0:
        z *= 0.6            # flat underside where the jaw sits
    return Vector((x, y, z))


head = ell(H, (0.5, 0.66, 0.42), seg=18, rings=11, material=RED, shape=head_shape)
bp.append(head)
bpy.context.view_layer.update()
# brow ridges + eyes
for sx in (-1, 1):
    ec = H + V(sx * 0.27, -0.24, 0.29)
    bp += eye(ec, V(sx * 0.55, -1, 0.35), r=0.18, white=EYES, black=PUP, depth=0.7, tall=1.15, pupil=0.5,
              look=(-sx * 0.15, 0, 0.0), seg=14)
    bp.append(tube(bezier(ec + V(-sx * 0.1, 0.0, 0.2), ec + V(sx * 0.03, -0.06, 0.3), ec + V(sx * 0.16, 0.04, 0.22), n=4),
                   [0.025, 0.035, 0.035, 0.03, 0.015], seg=6, material=DARK, round_end=True))
    # curved horns
    hb = H + V(sx * 0.22, 0.3, 0.3)
    bp.append(tube(bezier(hb, hb + V(sx * 0.08, 0.15, 0.2), hb + V(sx * 0.12, 0.42, 0.22), n=5),
                   [0.08, 0.07, 0.055, 0.04, 0.025, 0.004], seg=8, material=DARK))
    # side frills: three spines
    for k, a in enumerate((-0.4, 0.0, 0.4)):
        fb = H + V(sx * 0.43, 0.25, 0.04 + a * 0.17)
        d = V(sx * 0.8, 0.6, a).normalized()
        bp.append(tube([fb, fb + d * 0.18, fb + d * 0.3], [0.05, 0.035, 0.004], seg=6, material=DARK if k != 1 else GLOW, flat=0.4))
    # nostrils
    bp.append(ell(H + V(sx * 0.11, -0.62, 0.15), (0.03, 0.02, 0.022), seg=6, rings=4, material=PUP))
    # upper fangs
    bp.append(tube([H + V(sx * 0.25, -0.42, -0.16), H + V(sx * 0.25, -0.44, -0.27)], [0.04, 0.002], seg=6, material=TOOTH))
# glowing crack on the forehead
bp.append(tube(bezier(H + V(0, -0.08, 0.42), H + V(0.05, 0.08, 0.43), H + V(-0.02, 0.24, 0.4), n=4), 0.018, seg=5, material=GLOW, round_end=True))
body = part(bp, 'body', (0, 0, 0), angle=55)

# ---------------------------------------------------------------- jaw (pivot at the hinge)
HG = H + V(0, 0.24, -0.18)
jp = []


def jaw_shape(n):
    x, y, z = n
    if z > 0:
        z *= 0.25            # flat top (mouth floor)
    if y < 0:
        x *= 1 - 0.25 * (-y)
    return Vector((x, y, z))


JC = H + V(0, -0.22, -0.22)
jaw = ell(JC, (0.4, 0.48, 0.17), seg=16, rings=8, material=RED, shape=jaw_shape)
iso_paint(jaw, lambda p: -(p.z - (JC.z + 0.02)) * 30, PUP)   # dark inside on top
jp.append(jaw)
# tongue
jp.append(ell(JC + V(0, -0.05, 0.035), (0.14, 0.24, 0.03), seg=10, rings=4, material=GLOW))
# bottom fangs + chin plate
for sx in (-1, 1):
    jp.append(tube([JC + V(sx * 0.2, -0.33, 0.02), JC + V(sx * 0.2, -0.34, 0.12)], [0.03, 0.002], seg=6, material=TOOTH))
jp.append(ell(JC + V(0, -0.05, -0.14), (0.2, 0.3, 0.04), seg=10, rings=4, material=DARK))
jaw_o = part(jp, 'jaw', HG, angle=55)
parent_keep(jaw_o, body)

report()
views('lava_serpent')
montage('lava_serpent')
finish('chars', 'lava_serpent', kind='char', footprint=0.6, grounded=False,
       notes=f'origin at the lava surface (0,0,0), neck continues to z=-0.6 below. parts: body (pivot 0,0,0); jaw pivot at hinge '
             f'({HG.x:.2f},{HG.y:.2f},{HG.z:.2f}) parented to body, open = rotate around Blender X (positive = down)')
