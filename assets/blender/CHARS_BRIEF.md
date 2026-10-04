# Brief: animated characters (Blender → GLB) for Minigolf Avontuur 3D

Read `assets/blender/BRIEF.md` (general workflow, style, `mglib.py`, previews, `tools/glb_sheet.js`) first.
This brief replaces its rules where they differ.

The game has moving characters that are currently built from primitive spheres/boxes and look poor.
You build new, much nicer versions in Blender. The game ANIMATES the separately named parts listed
below by rotating them around their origin, so the part structure is the most important requirement.

## Rules for every character
- Theme folder: **`chars`** → `assets/blender/chars/<name>.py`, `assets/models/chars/<name>.glb`,
  `assets/previews/chars/<name>.png`. Call `finish('chars', '<name>', kind='char', footprint=..., grounded=False, notes=...)`
  (`grounded=False`: you place everything yourself so the feet stand on z=0; `finish` then does not move objects).
- **Do NOT join the named parts.** Each named part is its own mesh object, with its **origin exactly at its
  pivot** (hip, shoulder, neck, hinge…). Set the origin with e.g. `bpy.ops.object.origin_set(type='ORIGIN_CURSOR')`
  after placing the 3D cursor, or build the part around (0,0,0) and then move the object. Do not apply the
  location of named parts. Rotation must be zero (apply rotation/scale is fine) so the game's axes are predictable.
- No parenting (all parts top level) unless stated. Everything not listed is joined into `body`.
- Front of every character faces **Blender −Y**, up is +Z, units are metres, feet/base on z=0.
- Style: cute, chunky, expressive cartoon (big eyes with white + dark pupil + highlight, smooth shading with
  `shade_smooth`, slight bevels), clearly readable from 8–15 m away. Saturated colours. ≤ 6 materials,
  total ≤ 3500 tris, GLB ≤ 120 KB.
- Material names listed below must be used exactly (the game changes those materials at runtime).
- The preview must show the character nicely; check it with the Read tool and iterate until it looks
  genuinely good and charming. Also run `node tools/glb_sheet.js chars` at the end (NO ERRORS required).
- In the manifest `notes`, list each part name and its pivot.

## Characters
### `cow` (Koe Bertha, meadow) — body length ~1.5 m (nose to tail root ~2.0), height ~1.6 m
Collision: body capsule 0.9 m long, radius 0.5; head circle radius 0.3 about 0.9 m in front of the centre.
Parts: `body` (torso with spots, udder, a golden bell on a collar), `head` (pivot at the neck, includes horns,
ears, eyes, pink snout), `leg_fl`, `leg_fr`, `leg_bl`, `leg_br` (pivot at the hip/shoulder, hooves at z=0),
`tail` (pivot at the tail root, hanging down with a tuft). Spots: geometry patches or a separate black material.

### `crab` (De reuzenkrab, islands) — shell ~1.1 m wide, ~0.8 m deep, ~0.75 m high incl. eye stalks
Collision: body radius 0.55; the claws reach 0.55–1.15 m in front of the centre.
Parts: `body` (shell, eye stalks with big eyes, mouth), `arm_l`, `arm_r` (pivot at the shoulder on the body front
side, arm + big claw pointing forward −Y), `jaw_l`, `jaw_r` (the movable upper pincer half; this ONE part
may be parented to its arm, origin at the hinge), `leg_l1..leg_l3`, `leg_r1..leg_r3` (pivot at the body side).
Bright red/orange.

### `penguin` (De pinguïn, ice) — height ~1.45 m
Collision radius 0.42.
Parts: `body` (black body, white belly using a material named exactly **`belly`**, orange feet), `head`
(pivot at the neck: black head, white face patches, orange beak, big eyes, maybe a tiny scarf), `flipper_l`,
`flipper_r` (pivot at the shoulder, hanging down along the body).

### `scorpion` (De schorpioen, desert) — body ~1.6 m long without the tail, ~0.5 m high
Collision: body capsule 1.1 m long radius 0.5; the tail/sting is animated separately by the game.
Parts: `body` (head with angry-cute eyes, thorax segments; the tail root ends at the back, around z 0.45),
`leg_l1..leg_l4`, `leg_r1..leg_r4` (pivot at the body side), `arm_l`, `arm_r` (pivot at the shoulder, arm with
pincer pointing forward), `jaw_l`, `jaw_r` (movable pincer half, parented to its arm, origin at the hinge),
`tail_seg` (ONE tail segment ~0.32 m long, ~0.3 m thick, centred on its origin, placed anywhere, e.g. off to
the side; the game copies it 7 times along a curve), `sting` (the stinger, origin at its base, pointing down
−Z, ~0.4 m long, material named exactly **`sting`**, golden). Dark brown/black shell with amber accents.

### `ghost` (Het spook, haunted) — floating, bottom of the sheet ~0.15 m above z=0, top ~1.9 m
Collision radius 0.55.
Parts: `body` (classic sheet ghost with a wavy hem, material named exactly **`ghost`**: pale blue-white,
the game makes it transparent and glowing), `arm_l`, `arm_r` (little round sheet arms, pivot at the shoulder,
same `ghost` material), `face` (two big dark oval eyes and blush cheeks, very slightly in front of the body),
`mouth` (an open dark "O" mouth, origin at its centre; the game scales it).

### `planet` (Mini-planeet / Saturnus, space) — origin at the planet CENTRE
The planet sphere has radius exactly **1.0** (the game scales it), centred on (0,0,0); call `finish` with
`grounded=False` and do NOT move it to the ground.
Parts: `planet` (banded purple/pink gas-giant sphere with a cute face: big eyes and a smile on the −Y side),
`ring` (a wide, slightly tilted (≈20° around X) ring with a few coloured bands, inner radius 1.3, outer 1.8),
`moon` (a small cratered moon, radius 0.22, origin at its centre, placed at e.g. x = 1.6, z = 1.0).
