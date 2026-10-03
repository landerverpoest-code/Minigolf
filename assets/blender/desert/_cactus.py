"""Gedeelde cactus-bouwers (saguaro / cactus_post)."""
from _kit import *


def cactus_mats():
    return dict(
        green=mat('cactus_green', '#4f9b45', rough=0.7),
        dark=mat('cactus_dark', '#3a7a37', rough=0.7),
        flower=mat('cactus_flower', '#ffe4ec', rough=0.6),
        yellow=mat('flower_yellow', '#ffcc33', rough=0.6),
        sand=mat('sand', '#e6c48a', rough=0.95),
    )


def dome_end(pts, rads, r, up=Vector((0, 0, 1))):
    p = Vector(pts[-1])
    pts += [p + up * r * 0.35, p + up * r * 0.75, p + up * r * 0.95]
    rads += [r * 0.88, r * 0.55, 0.0]


def stem(pts, rads, M, verts=10, ribs=0.09):
    t = tube(pts, rads, verts=verts, material=M['green'], ribs=ribs, cap0=False)
    t.data.materials.append(M['dark'])
    # groeven donkerder: vlakken die aan een groefpunt beginnen
    for i, p in enumerate(t.data.polygons):
        if len(p.vertices) == 4:
            # vertex-index binnen de ring
            k = p.vertices[0] % verts
            p.material_index = 1 if k % 2 == 1 else 0
    return t


def arm(base_dir, h0, out=0.55, up=0.9, r=0.17, trunk_r=0.28, M=None, verts=8, elbow=0.22):
    d = Vector((math.cos(base_dir), math.sin(base_dir), 0))
    pts = [d * (trunk_r * 0.3) + Vector((0, 0, h0)), d * (trunk_r + 0.12) + Vector((0, 0, h0 + 0.02)),
           d * (out - 0.05) + Vector((0, 0, h0 + elbow * 0.35)), d * out + Vector((0, 0, h0 + elbow)),
           d * (out + 0.02) + Vector((0, 0, h0 + up * 0.6)), d * out + Vector((0, 0, h0 + up))]
    rads = [r, r, r * 1.02, r, r * 0.98, r * 0.95]
    dome_end(pts, rads, r * 0.95)
    return stem(pts, rads, M, verts=verts), pts[-1]


def flower(c, M, s=1.0, n_dir=Vector((0, 0, 1))):
    c = Vector(c); nd = Vector(n_dir).normalized()
    sd = nd.cross(Vector((1, 0, 0))) if abs(nd.x) < 0.9 else nd.cross(Vector((0, 1, 0)))
    sd.normalize(); up2 = nd.cross(sd).normalized()
    vs = [c + nd * 0.02 * s]; fs = []
    for j in range(10):
        a = 2 * math.pi * j / 10
        rr = (0.09 if j % 2 == 0 else 0.05) * s
        vs.append(c + (sd * math.cos(a) + up2 * math.sin(a)) * rr + nd * (0.04 * s if j % 2 == 0 else 0.01 * s))
    for j in range(10):
        fs.append((0, 1 + j, 1 + (j + 1) % 10))
    f = mesh_obj(vs, fs, M['flower'], 'flower')
    cc = cone(0.03 * s, 0.03 * s, loc=c + nd * 0.03 * s, verts=5, material=M['yellow'])
    return f
