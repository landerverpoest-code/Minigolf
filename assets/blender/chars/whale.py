import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
reset()
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skit import *

BLUE = mat('whale_blue', '#3f7fe0', rough=0.45)
BELLY = mat('whale_belly', '#cfe6ff', rough=0.5)
WHITE = mat('eye_white', '#ffffff', rough=0.3)
DARK = mat('pupil', '#1a2238', rough=0.35)
BLUSH = mat('blush', '#ff8fb0', rough=0.6)

Y0, Y1 = -2.0, 1.35        # nose, tail joint


def zc(y):
    return -0.08 + 0.2 * max(0.0, (y + 0.4) / (Y1 + 0.4)) ** 1.3


def prof(y):
    f = min(max((y - Y0) / 0.75, 0.0), 1.0)
    rnd_ = math.sqrt(max(0.0, 1 - (1 - f) ** 2))
    g = 1.0 if y < -0.4 else 1 - 0.64 * ((y + 0.4) / (Y1 + 0.4)) ** 1.5
    return rnd_ * g


secs = [(Y0 - 0.0, zc(Y0) - 0.05, 0, 0, 0)]
ys = [Y0 + 0.03, Y0 + 0.1, Y0 + 0.22, Y0 + 0.4, Y0 + 0.62, -1.05, -0.65, -0.25, 0.15, 0.55, 0.95, Y1, Y1 + 0.12]
for y in ys:
    k = prof(min(y, Y1))
    if y > Y1:
        k *= 0.72
    secs.append((y, zc(min(y, Y1)) - (0.05 if y < Y0 + 0.5 else 0.0), 0.98 * k, 0.9 * k, 0.98 * k))
secs.append((Y1 + 0.2, zc(Y1), 0, 0, 0))
torso = loft_y(secs, seg=24, material=BLUE)
bpy.context.view_layer.update()


def belly_field(p):
    # light belly / chin below a line that rises towards the mouth
    edge = zc(p.y) - 0.22 - 0.18 * max(0.0, (p.y + 0.6) / 1.9)
    return (p.z - edge) * 8


iso_paint(torso, belly_field, BELLY)
bp = [torso]
bpy.context.view_layer.update()

# pleats on the belly
for k in (-2, -1, 0, 1, 2):
    a = math.radians(-90 + k * 14)
    tg = [V(math.cos(a) * 2, y, zc(y) + math.sin(a) * 2) for y in (-1.75, -1.45, -1.15, -0.85, -0.6)]
    pts = []
    for t, y in zip(tg, (-1.75, -1.45, -1.15, -0.85, -0.6)):
        p, n = surf(torso, V(0, y, zc(y)), t, push=0.004)
        if p is not None:
            pts.append(p)
    if len(pts) > 2:
        bp.append(tube(pts, [0.02] * len(pts), seg=5, material=BELLY if False else BLUE, round_end=True))

# smile: curve across the front of the head
C = V(0, -1.2, zc(-1.2))
smile_t = []
for i in range(11):
    u = -1 + 2 * i / 10
    ang = u * 1.25            # around the head (0 = straight ahead)
    yy = -2.6 * math.cos(ang * 0.55)
    smile_t.append(V(math.sin(ang) * 2.2, yy, C.z - 0.38 + 0.22 * abs(u) ** 2.2))
mpts = surf_curve(torso, C, smile_t, push=0.004)
bp.append(tube(mpts, 0.028, seg=6, material=DARK, round_end=True))

# eyes
for sx in (-1, 1):
    p, n = surf(torso, V(0, -1.3, zc(-1.3)), V(sx * 1.1, -2.6, zc(-1.3) + 0.75), push=-0.05)
    d = (n + V(0, -0.6, 0.0)).normalized()
    bp += eye(p, d, r=0.22, white=WHITE, black=DARK, depth=0.55, tall=1.2, pupil=0.62, look=(-sx * 0.3, 0, 0.15), seg=14)
    # blush
    q, n2 = surf(torso, V(0, -1.35, zc(-1.35)), V(sx * 1.5, -2.4, zc(-1.35) + 0.12), push=0.0)
    R = n2.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    bp.append(xf(ell((0, 0, 0), (0.13, 0.08, 0.02), seg=8, rings=4, material=BLUSH), Matrix.Translation(q) @ R))
    # pectoral fins
    f0 = V(sx * 0.75, -0.7, zc(-0.7) - 0.45)
    bp.append(tube([f0 - V(sx * 0.1, 0, 0), f0 + V(sx * 0.3, 0.12, -0.12), f0 + V(sx * 0.62, 0.32, -0.2)], [0.16, 0.2, 0.06],
                   seg=10, material=BLUE, flat=0.28, round_end=True))

# blowhole on top + dorsal bump
bh, nb = surf(torso, V(0, -0.85, 0), V(0, -0.85, 3), push=0.0)
bp.append(xf(torus(0.09, 0.03, seg=12, ring=6, material=BLUE), Matrix.Translation(bh)))
bp.append(xf(ell((0, 0, 0), (0.08, 0.05, 0.015), seg=10, rings=4, material=DARK), Matrix.Translation(bh + V(0, 0, 0.012))))
dp, nd = surf(torso, V(0, 0.6, zc(0.6)), V(0, 0.6, 3), push=-0.04)
bp.append(tube([dp, dp + V(0, 0.18, 0.14), dp + V(0, 0.32, 0.18)], [0.16, 0.1, 0.02], seg=8, material=BLUE, flat=0.35, round_end=True))
for (sy, sa, rr) in ((-0.45, 0.35, 0.09), (-0.2, 0.62, 0.07), (0.05, 0.3, 0.06), (-0.5, -0.4, 0.08), (-0.15, -0.68, 0.065), (0.1, -0.35, 0.055)):
    q, n3 = surf(torso, V(0, sy, zc(sy)), V(math.sin(sa) * 2, sy, zc(sy) + math.cos(sa) * 2), push=-0.006)
    R = n3.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    bp.append(xf(ell((0, 0, 0), (rr, rr, 0.02), seg=8, rings=4, material=BELLY), Matrix.Translation(q) @ R))
body = part(bp, 'body', (0, 0, 0), angle=55)

# ---------------------------------------------------------------- tail (pivot at the tail base)
P = V(0, Y1, zc(Y1))
r0 = prof(Y1) * 0.9
tp = []
stock = loft_y([(Y1 - 0.12, P.z, 0, 0, 0), (Y1 - 0.06, P.z, r0 * 0.75, r0 * 0.7, r0 * 0.75), (Y1 + 0.1, P.z, r0 * 0.95, r0 * 0.9, r0 * 0.95),
                (Y1 + 0.4, P.z + 0.02, r0 * 0.75, r0 * 0.62, r0 * 0.66), (Y1 + 0.7, P.z + 0.04, r0 * 0.52, r0 * 0.38, r0 * 0.4),
                (Y1 + 0.9, P.z + 0.05, r0 * 0.36, r0 * 0.22, r0 * 0.24), (Y1 + 1.0, P.z + 0.05, 0, 0, 0)], seg=16, material=BLUE)
tp.append(stock)
half = [(0.05, 0.55), (0.32, 0.6), (0.66, 0.74), (0.93, 0.96), (1.06, 1.14), (0.98, 1.24), (0.7, 1.2), (0.4, 1.12), (0.15, 1.03), (0.0, 0.92)]
outline = [(x, Y1 + y) for x, y in half] + [(-x, Y1 + y) for x, y in reversed(half[:-1])][:-0] 
outline = [(x, Y1 + y) for x, y in half[:-1]] + [(0.0, Y1 + 0.88)] + [(-x, Y1 + y) for x, y in reversed(half[:-1])]
# outline must be CCW in XY
area = sum(outline[i][0] * outline[(i + 1) % len(outline)][1] - outline[(i + 1) % len(outline)][0] * outline[i][1] for i in range(len(outline)))
if area < 0:
    outline = outline[::-1]
fl = fin2d(outline, 0.17, material=BLUE, bevel=0.045, z=P.z + 0.05)
# thin the fluke towards its trailing edge / tips
for v in fl.data.vertices:
    t = min(1.0, max(0.0, (abs(v.co.x) - 0.1) / 0.9))
    v.co.z = P.z + 0.05 + (v.co.z - P.z - 0.05) * (1 - 0.45 * t) + 0.1 * t * t
iso_paint(fl, lambda p: (p.z - (P.z + 0.05)) * 40, BELLY)
tp.append(fl)
tail = part(tp, 'tail', P, angle=55)

report()
views('whale')
montage('whale')
finish('chars', 'whale', kind='char', footprint=2.2, grounded=False,
       notes=f'origin at water surface centre (0,0,0); body centred below/above z=0, nose at -Y. parts: body (pivot 0,0,0); '
             f'tail pivot ({P.x:.2f},{P.y:.2f},{P.z:.2f}) at the tail base, swing up/down = rotate around Blender X (three.js x)')
