# Minigolf Avontuur 3D

Een volledige 3D-minigolfgame in **één HTML-bestand** (`index.html`). Open het bestand in een moderne browser en speel meteen.

- 9 holes met elk een eigen thema, layout, sfeer, muziek en speciaal element (koe, rotsblokken, ridder, krab, pinguïn, schorpioen, spook, drone en draak)
- Three.js r128 via cdnjs. Alle textures, modellen en geluiden worden procedureel gegenereerd (canvas, geometrie in code, WebAudio)
- 2D-fysica (x,z) met een vaste timestep van 120 Hz en adaptieve substeps; botsingen tussen cirkel en capsule met correcte reflectie, ook voor bewegende obstakels
- 1–4 spelers (hot-seat), highscore in localStorage

**Besturing:** sleep vanaf de bal naar achteren (katapult) of houd Spatie ingedrukt · slepen of ←/→ om de camera te draaien · scrollwiel of +/− om te zoomen · O = overzicht · R = terug (+1 strafslag) · P = pauze · M = geluid aan/uit
