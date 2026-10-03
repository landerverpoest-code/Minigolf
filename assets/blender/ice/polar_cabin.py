import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender'); sys.path.insert(0, '/home/user/Minigolf/assets/blender/ice')
from mglib import *
reset()
from _kit import *

LOG = mat('log', '#9a6a40', rough=0.85)
DARK = mat('wood_dark', '#5e3e26', rough=0.85)
SNOW = mat('snow', '#f2f7ff', rough=0.7)
STONE = mat('stone', '#7d8594', rough=0.9)
GLOW = mat('glow_window', '#ffd27a', rough=0.4, emit='#ffa640', emit_strength=5.0)
rnd = random.Random(31)

W, D = 4.0, 3.0          # buitenmaat muren (x, y)
r = 0.13                 # stamstraal
NL = 8                   # stammen per muur
Hw = 2 * r * NL + r      # muurhoogte
Hr = Hw + 1.6           # nokhoogte
OV = 0.22                # uitsteek bij de hoeken
# --- blokhut-muren ---
for i in range(NL):
    z = r + 2 * r * i
    for s in (-1, 1):
        o = cyl(r, W + 2 * OV, loc=(0, s * D / 2, z), rot=(0, math.pi / 2, 0), verts=6, material=LOG if i % 2 else DARK)
        o = cyl(r, D + 2 * OV, loc=(s * W / 2, 0, z + r), rot=(math.pi / 2, 0, 0), verts=6, material=DARK if i % 2 else LOG)
# gevels (stammen worden korter)
ng = 5
for j in range(ng):
    z = Hw + r + 2 * r * j
    f = 1 - (z - Hw + r) / (Hr - Hw + 0.1)
    L = (D + 0.2) * f
    if L < 0.3: break
    for s in (-1, 1):
        cyl(r * 0.95, L, loc=(s * W / 2, 0, z), rot=(math.pi / 2, 0, 0), verts=6, material=LOG if j % 2 else DARK)
# --- dak ---
EY = D / 2 + 0.42; EZ = Hw - 0.05
ang = math.atan2(Hr - EZ, EY)
slope_len = math.hypot(EY, Hr - EZ)
for s in (-1, 1):
    cy, cz = s * EY / 2, (Hr + EZ) / 2
    rb = box((W + 2 * OV + 0.5, slope_len + 0.1, 0.12), loc=(0, cy, cz), rot=(-s * ang, 0, 0), material=DARK)
    n = Vector((0, s * math.sin(ang), math.cos(ang)))
    sn = box((W + 2 * OV + 0.65, slope_len + 0.18, 0.3), loc=Vector((0, cy, cz)) + n * 0.2, rot=(-s * ang, 0, 0), material=SNOW)
    bev(sn, 0.1, seg=2)
ridge = cyl(0.22, W + 2 * OV + 0.6, loc=(0, 0, Hr + 0.2), rot=(0, math.pi / 2, 0), verts=8, material=SNOW)
# sneeuwrand: bolle overhangende klodders langs de dakgoot
for s in (-1, 1):
    n = Vector((0, s * math.sin(ang), math.cos(ang)))
    for k in range(8):
        x = -W / 2 - 0.25 + k * (W + 0.5) / 7 + rnd.uniform(-0.08, 0.08)
        c = Vector((x, s * (EY + 0.04), EZ + 0.05)) + n * 0.12
        sphere(1.0, loc=c, seg=7, rings=4, material=SNOW, scale=(rnd.uniform(0.3, 0.42), 0.16, 0.14))
# ijspegels langs de dakrand (voor en achter)
for s in (-1, 1):
    for k in range(9):
        x = -W / 2 - 0.3 + k * (W + 0.6) / 8 + rnd.uniform(-0.1, 0.1)
        h = rnd.uniform(0.15, 0.4)
        cone(0.05, h, loc=(x, s * (EY + 0.02), EZ - 0.12 - h / 2 + 0.05), rot=(math.pi, 0, 0), verts=4, material=SNOW)
# --- schoorsteen (steen) ---
CX, CY = W / 2 - 0.75, 0.55
for k in range(9):
    z = Hw - 0.6 + k * 0.34
    w = 0.62 if k % 2 == 0 else 0.58
    box((w, w, 0.32), loc=(CX + rnd.uniform(-0.02, 0.02), CY + rnd.uniform(-0.02, 0.02), z), rot=(0, 0, rnd.uniform(-0.05, 0.05)), material=STONE, bevel=0.03)
ztop = Hw - 0.6 + 8 * 0.34 + 0.16
box((0.7, 0.7, 0.1), loc=(CX, CY, ztop + 0.05), material=STONE, bevel=0.02)
cap = lathe([(0.38, ztop + 0.08), (0.36, ztop + 0.16), (0.2, ztop + 0.22), (0.0, ztop + 0.23)], verts=8, material=SNOW, loc=(CX, CY, 0))
box((0.3, 0.3, 0.12), loc=(CX, CY, ztop + 0.2), material=DARK)
# --- deur (voor, -Y) ---
FY = -D / 2 - r
box((0.95, 0.12, 1.75), loc=(0, FY - 0.02, 0.9), material=DARK, bevel=0.02)
for k in range(4):
    box((0.2, 0.05, 1.6), loc=(-0.33 + k * 0.22, FY - 0.09, 0.86), material=LOG)
box((0.06, 0.06, 0.06), loc=(0.3, FY - 0.14, 0.9), material=DARK)
# luifel boven de deur
box((1.4, 0.7, 0.08), loc=(0, FY - 0.32, 1.95), rot=(0.25, 0, 0), material=DARK)
sl = box((1.5, 0.78, 0.16), loc=(0, FY - 0.32, 2.06), rot=(0.25, 0, 0), material=SNOW)
bev(sl, 0.05, seg=2)
for x in (-0.6, 0.6):
    cyl(0.06, 1.95, loc=(x, FY - 0.6, 0.97), verts=6, material=LOG)
# trapje
box((1.3, 0.5, 0.16), loc=(0, FY - 0.35, 0.08), material=LOG, bevel=0.02)
# --- ramen met warme gloed ---
def window(cx, cy, cz, face_y=True, w=0.8, h=0.75, s=-1):
    rot = (0, 0, 0) if face_y else (0, 0, math.pi / 2)
    def P(dx, dy, dz):
        v = Vector((dx, dy, dz))
        if not face_y: v = Vector((-dy * 1, dx, dz)) if s < 0 else Vector((dy, dx, dz))
        return Vector((cx, cy, cz)) + v
    off = s * 0.0
    box((w, 0.04, h), loc=P(0, s * 0.03, 0), rot=rot, material=GLOW)
    for dz in (-h / 2, h / 2):
        box((w + 0.16, 0.1, 0.09), loc=P(0, s * 0.06, dz), rot=rot, material=DARK)
    for dx in (-w / 2, w / 2):
        box((0.09, 0.1, h + 0.1), loc=P(dx, s * 0.06, 0), rot=rot, material=DARK)
    box((0.05, 0.08, h), loc=P(0, s * 0.07, 0), rot=rot, material=DARK)
    box((w, 0.08, 0.05), loc=P(0, s * 0.07, 0), rot=rot, material=DARK)
    sill = box((w + 0.3, 0.22, 0.1), loc=P(0, s * 0.12, -h / 2 - 0.08), rot=rot, material=SNOW)
    bev(sill, 0.04, seg=2)
    for dx in (-1, 1):
        box((0.3, 0.05, h + 0.05), loc=P(dx * (w / 2 + 0.22), s * 0.04, 0), rot=rot, material=LOG)
window(-1.15, FY - 0.04, 1.25)
window(1.15, FY - 0.04, 1.25)
# zijraam (-X)
SX = -W / 2 - r
gl = box((0.04, 0.6, 0.6), loc=(SX - 0.03, 0, 1.3), material=GLOW)
for dz in (-0.3, 0.3):
    box((0.1, 0.76, 0.09), loc=(SX - 0.06, 0, 1.3 + dz), material=DARK)
for dy in (-0.3, 0.3):
    box((0.1, 0.09, 0.7), loc=(SX - 0.06, dy, 1.3), material=DARK)
box((0.08, 0.05, 0.6), loc=(SX - 0.07, 0, 1.3), material=DARK)
ss = box((0.22, 0.86, 0.1), loc=(SX - 0.12, 0, 0.95), material=SNOW); bev(ss, 0.04, seg=2)
# lantaarn naast de deur
lan = cyl(0.07, 0.18, loc=(0.75, FY - 0.2, 1.45), verts=6, material=GLOW)
cone(0.1, 0.1, loc=(0.75, FY - 0.2, 1.59), verts=6, material=DARK)
box((0.04, 0.2, 0.04), loc=(0.75, FY - 0.1, 1.6), material=DARK)
# --- houtstapel rechts ---
for row in range(3):
    for k in range(4 - row):
        cyl(0.12, 0.8, loc=(W / 2 + 0.55, -0.6 + k * 0.25 + row * 0.125, 0.12 + row * 0.22), rot=(0, math.pi / 2, 0), verts=6, material=LOG if (k + row) % 2 else DARK)
wsn = box((0.85, 0.7, 0.1), loc=(W / 2 + 0.55, -0.6 + 0.375, 0.75), material=SNOW); bev(wsn, 0.04, seg=2)
# --- sneeuwduinen tegen de muren ---
for (x, y, sx, sy) in [(-1.6, -D / 2 - 0.35, 0.9, 0.5), (1.7, D / 2 + 0.4, 1.0, 0.55), (-W / 2 - 0.4, 0.9, 0.5, 0.9), (W / 2 + 0.35, 0.8, 0.45, 0.7)]:
    m = rock(1.0, loc=(x, y, 0.0), scale=(sx, sy, 0.35), seed=int(x * 10 + y), sub=1, jitter=0.05, material=SNOW)
    for v in m.data.vertices: v.co.z = max(v.co.z, 0.0)
    shade_smooth(m, 60)
join_all('polar_cabin')
report()
finish('ice', 'polar_cabin', kind='hero', footprint=2.8,
       notes='Blokhut van stammen met dik sneeuwdak, ijspegels, stenen schoorsteen, deur met luifel, warme ramen + lantaarn (glow_window), houtstapel')
closeup('polar_cabin')
