"""Besneeuwde den (gedeeld door snowy_pine en snowy_pine_small)."""
from _kit import *


def pine_mats():
    return dict(
        green=mat('pine_green', '#1b5844', rough=0.85),
        green2=mat('pine_green_light', '#2a7155', rough=0.85),
        snow=mat('snow', '#f2f7ff', rough=0.7),
        trunk=mat('pine_trunk', '#6a4a33', rough=0.9),
    )


def pine(M, base=(0, 0, 0), height=5.0, radius=1.5, tiers=5, verts=10, seed=1, trunk_h=0.7, snow_start=0.32):
    rnd = random.Random(seed)
    base = Vector(base)
    parts = []
    tr = cyl(radius * 0.12, trunk_h + 0.3, loc=base + Vector((0, 0, (trunk_h + 0.3) / 2)), verts=6, material=M['trunk'], r2=radius * 0.08)
    parts.append(tr)
    span = height - trunk_h
    th = span / ((tiers - 1) * 0.62 + 1.0)
    for i in range(tiers):
        f = i / max(tiers - 1, 1)
        r = radius * (1 - 0.62 * f)
        z0 = base.z + trunk_h + i * th * 0.62
        h = th * (1.0 if i < tiers - 1 else 1.15)
        ph = rnd.uniform(0, 1)
        g = lathe([(r * 0.45, z0 + h * 0.12), (r, z0), (0.0, z0 + h)], verts=verts,
                  material=M['green'] if i % 2 == 0 else M['green2'], loc=(base.x, base.y, 0), phase=ph)
        # gekartelde rand: om en om naar binnen/omhoog
        for k, v in enumerate(g.data.vertices):
            if abs(v.co.z - z0) < 1e-4 and k % 2:
                v.co.x = base.x + (v.co.x - base.x) * 0.84; v.co.y = base.y + (v.co.y - base.y) * 0.84; v.co.z += h * 0.07
        parts.append(g)
        # sneeuwkap op het bovenste deel, met druppels naar beneden
        zs = z0 + h * snow_start; rs = r * (1 - snow_start)
        s = lathe([(rs * 0.8, zs + 0.02), (rs + 0.06, zs), (0.0, z0 + h + 0.06)], verts=verts, material=M['snow'],
                  loc=(base.x, base.y, 0), phase=ph + math.pi / verts)
        for k, v in enumerate(s.data.vertices):
            if abs(v.co.z - zs) < 1e-4:
                dz = h * (0.16 if k % 3 == 0 else (0.06 if k % 3 == 1 else 0.0)) * rnd.uniform(0.7, 1.2)
                v.co.z -= dz
                sc = 1 + dz / (h * (1 - snow_start)) * 0.95
                v.co.x = base.x + (v.co.x - base.x) * sc; v.co.y = base.y + (v.co.y - base.y) * sc
        parts.append(s)
    return parts
