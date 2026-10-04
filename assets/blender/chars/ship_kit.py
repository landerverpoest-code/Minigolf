"""Shared ship builder for ship_water / ship_lava (chars agent). Bow = -Y, waterline z=0."""
import sys, math, random
sys.path.insert(0, '/home/user/Minigolf/assets/blender')
from mglib import *
from skit import *

Y_BOW, Y_STERN = -2.7, 2.4
MAST_Y = -0.25


def deck(y):
    return 0.72 + 0.28 * ((y + 0.1) / 2.5) ** 2


def keel(y):
    return -0.55 + 0.42 * max(0.0, (-y - 0.9) / 1.8) ** 1.6 + 0.12 * max(0.0, (y - 1.4) / 1.0)


def beam(y):
    if y < -0.4:
        return max(0.03, 1.15 * math.sqrt(max(0.0, 1 - ((y + 0.4) / 2.3) ** 2)))
    return 1.15 - 0.28 * ((y + 0.4) / 2.8) ** 2


def hull_mesh(material):
    ys = [Y_BOW, -2.62, -2.5, -2.3, -2.0, -1.6, -1.1, -0.5, 0.1, 0.7, 1.3, 1.9, Y_STERN - 0.12, Y_STERN]
    secs = []
    for y in ys:
        rt = 0.1
        zc = deck(y) - rt
        secs.append((y, zc, beam(y), rt, zc - keel(y)))
    return loft_y(secs, seg=24, material=material, p=0.62)


def ring_on(o, y, z, sx, push=0.0):
    return surf(o, V(0, y, z), V(sx * 5, y, z), push)


def top_at(o, x, y):
    p, n = surf(o, V(x, y, 6), V(x, y, -6))
    return p


def orient(p, n):
    return Matrix.Translation(p) @ n.to_track_quat('Z', 'Y').to_matrix().to_4x4()


def sail_grid(W0, W1, zb, zt, y0, bulge, nu=8, nv=6, material=None, jag=0.0, holes=(), seed=1):
    """Billowing square sail between two yards (bulges toward -Y). Returns (obj, border pts)."""
    rnd = random.Random(seed)
    bm = bmesh.new()
    G = []
    for j in range(nv + 1):
        v = j / nv
        row = []
        for i in range(nu + 1):
            u = -1 + 2 * i / nu
            W = W0 + (W1 - W0) * (1 - v)
            z = zb + v * (zt - zb)
            if j == 0 and jag:
                z += (jag if i % 2 else -jag * 0.3) * (0.4 + 0.6 * rnd.random()) if 0 < i < nu else 0
            b = bulge * (1 - u * u * 0.85) * (1 - (2 * v - 1) ** 2 * 0.55)
            row.append(bm.verts.new((u * W / 2 * (1 + 0.05 * math.sin(math.pi * v)), y0 - b, z)))
        G.append(row)
    for j in range(nv):
        for i in range(nu):
            if (i, j) in holes:
                continue
            bm.faces.new((G[j][i], G[j][i + 1], G[j + 1][i + 1], G[j + 1][i]))
    border = [G[0][i].co.copy() for i in range(nu + 1)]
    left = [G[j][0].co.copy() for j in range(nv + 1)]
    right = [G[j][nu].co.copy() for j in range(nv + 1)]
    o = mesh_obj(bm, material)
    return o, border, left, right


def flag_mesh(L, Hh, x0, y0, z0, material, waves=1.2, amp=0.08, notch=False, nu=5, nv=2):
    """Flag attached at (x0,y0) pole, spanning z0..z0+Hh, flying toward +Y with a sine wave in X."""
    bm = bmesh.new()
    G = []
    for j in range(nv + 1):
        row = []
        for i in range(nu + 1):
            u = i / nu
            yy = y0 + u * L
            xx = x0 + amp * math.sin(u * math.pi * 2 * waves) * u
            zz = z0 + Hh * j / nv - 0.08 * u * u
            if notch and i == nu and j == 1:
                yy -= L * 0.22
            row.append(bm.verts.new((xx, yy, zz)))
        G.append(row)
    for j in range(nv):
        for i in range(nu):
            bm.faces.new((G[j][i], G[j][i + 1], G[j + 1][i + 1], G[j + 1][i]))
    o = mesh_obj(bm, material)
    return o
