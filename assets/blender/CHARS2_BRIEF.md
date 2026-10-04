# Brief wave 2: more animated characters and gameplay props (Blender → GLB)

Read `assets/blender/BRIEF.md`, `assets/blender/mglib.py` and `assets/blender/CHARS_BRIEF.md` first. ALL rules of
CHARS_BRIEF apply (folder `chars`, `kind='char'`, `grounded=False`, named parts = separate objects with origin on the
pivot and zero rotation, front = Blender −Y, feet on z=0, ≤ 6 materials, ≤ 3500 tris, ≤ 120 KB, charming
chunky cartoon style with big expressive eyes where it makes sense, check every Cycles preview with the Read tool
and iterate, `node tools/glb_sheet.js chars` must say NO ERRORS). Six characters already exist in `chars`
(cow, crab, penguin, scorpion, ghost, planet): look at their previews to match the style, and do NOT touch them.
`_l` = the character's own left = +X.

## Agent A
### `knight` (De ridder, castle) — height ~1.9 m, collision radius 0.5
Standing knight that spins a morning star around itself on a chain (the game draws the chain).
Parts: `body` (legs, armoured torso with a purple tabard, a blue shield with a gold cross on its left arm,
everything except the head and the right arm), `head` (helmet with visor slit, red plume; pivot at the neck),
`arm_r` (right arm reaching out to the side (−X), pivot at the shoulder, hand at the end gripping),
`star` (the spiked iron ball, radius ~0.3 with ~10 spikes, origin at its CENTRE, placed anywhere e.g. on the
ground beside the knight; dark iron material named exactly **`star`**; the game makes it glow red before a swing).

### `dragon` (De mechanische draak, finale) — a big clockwork dragon that sits on a stone pedestal OUTSIDE the course
and sweeps its long tail over the podium. Body ~4 m long, ~3.5 m high incl. pedestal; bronze, steel and gold.
Parts: `body` (stone pedestal block ~2.6×2.4×1.6 m, bronze torso with gold spikes, a turning gear on the flank can
be included statically), `head` (neck + head with horns and glowing eyes `glow_eyes`, the face looks to −Y like every model;
pivot at the base of the neck on the torso), `jaw` (lower jaw, pivot at the hinge,
may be parented to `head`), `wing_l`, `wing_r` (folded bat-like mechanical wings, pivot at the shoulder),
`tail_seg` (ONE tail segment, ~0.45 m long, ~0.45 m thick, centred on its origin, bronze/steel with a gold spike on
top; the game copies it along the tail with decreasing scale), `tail_tip` (the arrow/spade shaped tail end,
origin at its base, pointing along −Y).
The tail leaves the body at its back (+Y) around z ≈ 0.7; put a note with that point in the manifest notes.

### `drone` (De drone + mini-robots, space) — a cute flying robot, ~1.0 m wide, origin at its body CENTRE
(it floats; `grounded=False`, centre at z=0 is fine). The game recolours the shell via material **`shell`**.
Parts: `body` (round shell, glass dome with a little face/visor, eye `glow_eye` on the front −Y),
`rotor_1`..`rotor_4` (propellers on short struts at the 4 diagonals, pivot at the rotor centre, spin around Z),
`arm` (a punching arm pointing forward along −Y, length 1.0 from its pivot at the body centre to a red boxing glove
at the end; the game scales it along its length to extend it).

### `boulder` (Rotsblokken, volcano) — rolling boulder with a face, radius exactly **1.0**, origin at its CENTRE
(the game scales it). Parts: `rock` (lumpy volcanic rock sphere with glowing cracks `glow_lava`, rotated by the game
while rolling), `face` (big angry/funny eyes with brows and a mouth on the −Y side, sitting just outside the rock
surface; stays upright while the rock rolls).

## Agent B
### `bumper` (Bumpers, space) — pinball bumper, radius exactly **0.55** at the base, height ~0.55
Parts: `base` (dark metal body), `cap` (top cap, origin at its base centre; the game squashes/scales it),
and a neon ring with material named exactly **`bumper_glow`** (magenta, emissive) that may be part of `base`.

### `torch` (Fakkels, castle/haunted/finale) — wall torch on a pole, ~2.2 m high
Parts: `body` (wooden pole with iron bracket and bowl), `flame` (stylised layered flame, origin at its base,
emissive material **`glow_flame`**; the game flickers its scale).

### `button` (Schakelaar, meadow/finale) — a big round red push button with cute eyes on a metal base, radius ~0.45
Parts: `base`, `cap` (the red dome with eyes, origin at its base centre; the game presses it down; material named
exactly **`cap`**, the game turns it green when pressed).

### `lantern` (Lantaarns, haunted) — iron lamp post ~2 m with a hanging lantern cage
Parts: `body` (post and arm), `cage` (lantern with glass panes of material **`lantern_glass`** and a small roof,
pivot at its hanging point; the game swings it), `flame` (inside the cage, may be parented to `cage`,
material **`glow_flame`**).

### `shield_sign` (Schild, castle) — a round heraldic shield (radius 0.46, red/white/gold rings with a blue rim)
on a short wooden post, facing −Y. Parts: `body` (post), `shield` (pivot at its centre; the game wobbles it).

### `golf_flag` — the hole flag pole, height 2.4 m (thin white pole with a gold ball on top and a little cup-rim
ring at the bottom). Parts: `body` only (the game adds the waving cloth itself). ≤ 600 tris.
