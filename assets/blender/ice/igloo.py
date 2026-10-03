import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice')
from mglib import *
reset()
from _kit import *

BLOCK = mat('snow_block', '#eef5ff', rough=0.6)
JOINT = mat('ice_joint', '#9fc6e6', rough=0.5)
GLOW = mat('glow_inside', '#ffb867', rough=0.5, emit='#ff9a3a', emit_strength=7.0)
SNOW = mat('snow', '#f7fbff', rough=0.75)
rnd = random.Random(4)

R = 1.5; T = 0.16; GAP = 0.035


def shell_block(th0, th1, ph0, ph1, R, T, sub=1):
    """Blok op een bol: azimut th0..th1, elevatie ph0..ph1 (rad)."""
    def P(th, ph, r):
        return Vector((math.cos(th) * math.cos(ph) * r, math.sin(th) * math.cos(ph) * r, math.sin(ph) * r))
    gt0 = GAP / (2 * R * max(math.cos(ph0), 0.2)); gp = GAP / (2 * R)
    th0 += gt0; th1 -= gt0; ph0 += gp; ph1 -= gp
    ths = [th0 + (th1 - th0) * i / sub for i in range(sub + 1)]
    vs, fs = [], []
    for r in (R + T, R):
        for ph in (ph0, ph1):
            for th in ths:
                vs.append(P(th, ph, r))
    n = sub + 1
    def idx(layer, row, i): return layer * 2 * n + row * n + i
    for i in range(sub):
        fs.append((idx(0, 0, i), idx(0, 0, i + 1), idx(0, 1, i + 1), idx(0, 1, i)))    # buiten
        fs.append((idx(0, 0, i + 1), idx(0, 0, i), idx(1, 0, i), idx(1, 0, i + 1)))    # onder
        fs.append((idx(0, 1, i), idx(0, 1, i + 1), idx(1, 1, i + 1), idx(1, 1, i)))    # boven
    fs.append((idx(0, 0, 0), idx(0, 1, 0), idx(1, 1, 0), idx(1, 0, 0)))
    fs.append((idx(0, 1, sub), idx(0, 0, sub), idx(1, 0, sub), idx(1, 1, sub)))
    o = mesh_obj(vs, fs, BLOCK, 'blk')
    fix_normals(o)
    return o

# --- koepel van blokken ---
rows = [12, 12, 11, 9, 7, 5]
nr = len(rows)
blocks = []
for j, nb in enumerate(rows):
    ph0 = (math.pi / 2) * j / (nr + 0.6); ph1 = (math.pi / 2) * (j + 1) / (nr + 0.6)
    off = (j % 2) * 0.5 + rnd.uniform(-0.1, 0.1)
    for i in range(nb):
        th0 = 2 * math.pi * (i + off) / nb; th1 = 2 * math.pi * (i + 1 + off) / nb
        mid = (th0 + th1) / 2
        # opening voor de tunnel (voorkant -Y)
        d = math.atan2(math.sin(mid + math.pi / 2), math.cos(mid + math.pi / 2))
        if j < 2 and abs(d) < 0.42: continue
        b = shell_block(th0, th1, ph0, ph1, R, T, sub=2 if j < 3 else 1)
        bev(b, 0.03)
        blocks.append(b)
# topblok
cap_ph = (math.pi / 2) * nr / (nr + 0.6)
capr = math.cos(cap_ph + GAP / (2 * R)) * (R + T)
cap = lathe([(capr, math.sin(cap_ph) * (R + T) - 0.04), (capr * 0.6, (R + T) * 0.985), (0, R + T)], verts=8, material=BLOCK)
# voeglaag (binnenste bol, iets donkerder blauw)
inner = sphere(R + 0.01, loc=(0, 0, 0), seg=16, rings=8, material=JOINT)
bm_ = bmesh.new(); bm_.from_mesh(inner.data)
bmesh.ops.delete(bm_, geom=[v for v in bm_.verts if v.co.z < -0.01], context='VERTS')
bm_.to_mesh(inner.data); bm_.free()
# --- tunnel ---
TR = 0.72; Y0 = -R + 0.25; Y1 = -R - 0.85
nt = 3; na = 5
for k in range(nt):
    y0 = Y0 + (Y1 - Y0) * k / nt; y1 = Y0 + (Y1 - Y0) * (k + 1) / nt
    off = (k % 2) * 0.5
    for i in range(na + (k % 2)):
        a0 = math.pi * max(0, (i - off)) / na; a1 = math.pi * min(na, (i + 1 - off)) / na
        if a1 - a0 < 0.05: continue
        ga = GAP / (2 * TR); gy = GAP / 2
        a0 += ga; a1 -= ga
        vs = []
        for r in (TR + T, TR):
            for y in (y0 - gy, y1 + gy):
                for a in (a0, a1):
                    vs.append(Vector((math.cos(a) * r, y, math.sin(a) * r)))
        # 0..3 buiten (y0a0, y0a1, y1a0, y1a1), 4..7 binnen
        fs = [(0, 1, 3, 2), (6, 7, 5, 4), (0, 2, 6, 4), (1, 5, 7, 3), (0, 4, 5, 1), (2, 3, 7, 6)]
        b = mesh_obj(vs, fs, BLOCK, 'tb'); fix_normals(b); bev(b, 0.025)
# voeg-binnenkant tunnel
tin = lathe([(TR + 0.02, 0), (TR + 0.02, 1)], verts=12, material=JOINT, cap0=False, cap1=False)
place(tin, rot=(math.pi / 2, 0, 0), loc=(0, Y0 + 0.05, 0))
bm_ = bmesh.new(); bm_.from_mesh(tin.data)
bmesh.ops.delete(bm_, geom=[v for v in bm_.verts if v.co.z < -0.05], context='VERTS')
bm_.to_mesh(tin.data); bm_.free()
for v in tin.data.vertices:
    v.co.y = Y0 + 0.1 if v.co.y > (Y0 + Y1) / 2 else Y1 + 0.05
# warme gloed binnenin (halve schijf iets terug in de tunnel)
gl = [Vector((0, Y1 + 0.45, 0))]
for i in range(9):
    a = math.pi * i / 8
    gl.append(Vector((math.cos(a) * TR, Y1 + 0.45, math.sin(a) * TR)))
mesh_obj(gl, [(0, i + 1, i + 2) for i in range(8)], GLOW, 'glow')
floor = box((TR * 2, abs(Y1 - Y0) + 0.3, 0.04), loc=(0, (Y0 + Y1) / 2, 0.02), material=JOINT)
# --- sneeuw rondom ---
drift = lathe([(R + 0.55, 0.0), (R + 0.32, 0.17), (R + 0.08, 0.28), (R - 0.05, 0.3)], verts=18, material=SNOW, jitter=0.05, seed=2, cap0=False, cap1=False)
bm_ = bmesh.new(); bm_.from_mesh(drift.data)
bmesh.ops.delete(bm_, geom=[f for f in bm_.faces if f.calc_center_median().y < 0 and abs(f.calc_center_median().x) < TR + 0.1], context='FACES')
bm_.to_mesh(drift.data); bm_.free()
shade_smooth(drift, 60)
# losse ijsblokken en sneeuwhoopjes
for (x, y, rz) in [(1.55, -1.45, 0.4), (1.85, -1.1, 1.1)]:
    b = box((0.42, 0.28, 0.24), loc=(x, y, 0.12), rot=(0, 0, rz), material=BLOCK, bevel=0.03)
box((0.42, 0.28, 0.24), loc=(1.68, -1.3, 0.36), rot=(0, 0, 0.8), material=BLOCK, bevel=0.03)
m = rock(0.4, loc=(-1.75, -1.05, 0.0), scale=(1.3, 1.0, 0.55), seed=3, jitter=0.08, material=SNOW)
shade_smooth(m, 60)
for v in m.data.vertices: v.co.z = max(v.co.z, 0.0)
join_all('igloo')
report()
finish('ice', 'igloo', kind='hero', footprint=1.9,
       notes='Iglo van verspringende sneeuwblokken met voegen, ingangstunnel naar -Y met warme gloed (glow_inside)')
closeup('igloo')
