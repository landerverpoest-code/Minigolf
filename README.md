# Minigolf Avontuur 3D

Een 3D-minigolfgame in de browser (three.js r128). Open `index.html` en speel meteen.

- **9 werelden × 3 banen = 27 holes**, elk thema met eigen muziek, sfeer en banen die veranderen: knoppen en hekken, ophaalbruggen, uitbarstende vulkanen, eb en vloed, drijvende ijsschotsen, een tornado, verborgen lantaarnbruggen, mini-planeten met zwaartekracht, een draaibrug, een veerpont, valluiken, krachtvelden en meer
- Spelmodi: **Alle 27 holes**, **Speel een wereld** (de 3 holes van één thema, met scorekaart en record) of **een losse hole** (met beste score per hole)
- 1–4 spelers (hot-seat), geen slagenlimiet (na 10 slagen kies je: stoppen met +2 of doorspelen), highscores in localStorage
- **Decoratie gemaakt in Blender**: ruim 100 low-poly modellen (schuur, windmolen, kasteeltorens, vuurtoren, iglo, sfinx, mausoleum, raket, trofee, …)
  - bron-scripts: `assets/blender/<thema>/*.py` (Blender als Python-module `bpy`)
  - modellen + previews: `assets/models/<thema>/`, `assets/previews/<thema>/`
  - in de game: `models/<thema>.js`, gebouwd met `python3 tools/build_models.py` (quantiseert met gltf-transform)
  - zonder de map `models/` werkt de game ook, dan met eenvoudigere procedurele decoratie
- 2D-fysica (x,z) op 120 Hz met substeps en correcte botsingen, ook met bewegende obstakels; alle elementen draaien op een spelklok

**Besturing:** sleep vanaf de bal naar achteren (katapult) of houd Spatie ingedrukt · slepen of ←/→ om de camera te draaien · scrollwiel of +/− om te zoomen · O = overzicht · R = terug (+1 strafslag) · P = pauze · M = geluid aan/uit

**Testen** (Playwright): `node tools/smoke.js` (alle holes laden), `tools/solve.js`, `tools/phys.js`, `tools/kin.js`, `tools/beauty.js` (sfeerbeelden).
