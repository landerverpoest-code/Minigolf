# Decoratie-opdracht (Blender → GLB) voor Minigolf Avontuur 3D

De game (`/home/user/Minigolf/index.html`) is een 3D-minigolfspel in three.js **r128**. Je bouwt
mooie, gestileerde **low-poly** decoratiemodellen met Blender (Python-module `bpy` 4.2, headless) die
de game rond de banen plaatst. Jij schrijft **niets** in `index.html` en doet **geen** git-commando's.

## Werkwijze
1. Schrijf per model een script `assets/blender/<thema>/<naam>.py` dat begint met
   ```python
   import sys; sys.path.insert(0, '/home/user/Minigolf/assets/blender')
   from mglib import *
   reset()
   ```
   en eindigt met `finish('<thema>', '<naam>', kind=..., footprint=..., notes='...')`.
   Lees eerst `assets/blender/mglib.py` (helpers: mat, box, cyl, cone, sphere, ico, torus, bev, join, shade_smooth, finish, …).
   Je mag rechtstreeks `bpy`/`bmesh` gebruiken voor betere vormen (extrude, bevel, array, displace, boolean, …).
2. Draai het: `cd /home/user/Minigolf && python3 assets/blender/<thema>/<naam>.py 2>&1 | grep -E "MODEL|Error|Traceback" -A3`
   (Blender laden duurt ~3 s.) Dit schrijft `assets/models/<thema>/<naam>.glb`, een Cycles-preview in
   `assets/previews/<thema>/<naam>.png` en werkt `assets/models/<thema>/manifest.json` bij.
3. **Bekijk de preview** (Read-tool op de PNG) en verbeter tot het er echt goed uitziet.
4. Controleer per thema in three.js r128 (zoals in de game): `node tools/glb_sheet.js <thema>` → contactblad
   `assets/previews/<thema>/_sheet.png` + per model tris/materialen. Moet "NO ERRORS" geven. Bekijk het blad.

## Stijl
- Vrolijk, chunky, licht cartoonachtig low-poly (denk aan "Mario Golf" / "Golf With Your Friends").
  Duidelijke silhouetten, meerdere onderdelen en details (planken, ramen, dakpannen, bladclusters,
  scheuren, nerven), afgeschuinde randen (`bev`) voor mooie lichtranden. Geen kale primitieven.
- Kleuren: verzadigd maar niet schreeuwerig, passend bij het thema (zie lijst). Kleine kleurvariatie
  binnen een model (bv. 2 bladtinten) maakt het levendig.
- Alleen materiaalkleuren (Principled BSDF: kleur, roughness, metallic, emissie). **Geen beeldtextures.**
  Max ~5 materialen per model. Gloeiende delen: materiaalnaam begint met `glow` en heeft emissie
  (de game laat die zacht pulseren).
- Schaal: echte meters. De bal heeft straal 0.22 m, banen zijn ~5 m breed, muurtjes ~0.5 m hoog.
  Bomen 3–6 m, huizen/torens 5–14 m, randdetails 0.2–1 m.
- Oorsprong = midden van de voet, model staat op z=0 (`finish` zet het op de grond).
  **Voorkant naar Blender −Y** (wordt +Z in three.js).

## Technische grenzen
| kind | gebruik | tris | GLB |
|---|---|---|---|
| `edge` | kleine details vlak naast de baan (veel kopieën) | ≤ 300 | ≤ 25 KB |
| `scatter` | bomen/rotsen/objecten in de omgeving (tientallen kopieën, instanced) | ≤ 900 | ≤ 45 KB |
| `post` | vervangt een rond obstakel OP de baan; `footprint` = botsstraal, het model moet binnen die straal blijven op 0–0.6 m hoogte | ≤ 900 | ≤ 45 KB |
| `hero` | groot blikvangend stuk, 1–3 per baan in de achtergrond | ≤ 5000 | ≤ 200 KB |

- `footprint` = straal (m) van de voet: de game houdt die vrij van de baan.
- Pas alle transformaties toe (helpers doen dat). Gebruik geen subdivision die je niet nodig hebt.
- **Bewegend onderdeel** (optioneel, alleen voor hero's zoals molenwieken, radarschotel, vlag):
  laat dat onderdeel een APART object met naam `spin_<iets>` en zet zijn oorsprong op het draaipunt
  (niet joinen, geen `transform_apply` op locatie). Voeg aan `finish(...)` toe:
  `spin=[{'node': 'spin_blades', 'axis': 'z', 'speed': 1.2}]` waarbij `axis` de as is in **three.js-
  coördinaten** (Blender X→x, Blender Z→y, Blender Y→−z) in het lokale assenstelsel van het object.
  Draait het onderdeel rond zijn eigen Blender-Y-as (bv. wieken die naar −Y kijken) dan is dat `axis: 'z'`.
- Render ALLEEN met Cycles (zit in `finish`). **Nooit Eevee/Workbench** (crasht hier: geen EGL).
- Werk alleen in `assets/blender/<jouw thema's>/`, `assets/models/<jouw thema's>/` en
  `assets/previews/<jouw thema's>/`. Raak andere thema's en bestanden niet aan.

## Oplevering
Per thema minstens de gevraagde modellen, allemaal met preview, in het manifest, en een
contactblad zonder fouten. Sluit af met een kort verslag: per thema de modellen (naam, kind,
footprint, tris) en eventuele `spin`/`glow`-onderdelen, plus wat volgens jou het mooiste is.
