# Minigolf Avontuur 3D

Een volledige 3D-minigolfgame in **één HTML-bestand** (`index.html`). Open het bestand in een moderne browser en speel meteen.

- 9 lange holes (1,5 tot 2 keer langer dan in de eerste versie, met bochten en extra secties), elk met een eigen thema, muziek en baanveranderende elementen:
  schakelaar en hek, vulkaanuitbarsting met stollende lavabrug, schild en ophaalbrug, eb en vloed met zandbanken, drijvende en brekende ijsschotsen, een tornado die je bal over een kloof slingert, lantaarns met verborgen bruggen, een draaiende muur en een mini-planeet met zwaartekracht
- Spelmodi: **Alle holes** (doorlopende scorekaart en eindscherm) of **Kies een hole** (losse hole met beste score per hole)
- Knop **Instructies** in het menu en als ?-knop tijdens het spelen
- Omgeving in drie lagen (voorgrond, middengrond, verre achtergrond) op heuvelachtig terrein, InstancedMesh voor bomen en details, water met golven en schuim, kwaliteitsoptie hoog/laag (laag automatisch op mobiel)
- Three.js r128 via cdnjs. Alle textures, modellen en geluiden worden procedureel gegenereerd (canvas, geometrie in code, WebAudio)
- 2D-fysica (x,z) met een vaste timestep van 120 Hz en adaptieve substeps; botsingen tussen cirkel en capsule met correcte reflectie, ook voor bewegende obstakels. Alle bewegende elementen draaien op een globale spelklok die alleen stopt bij pauze
- 1–4 spelers (hot-seat), highscores in localStorage

**Besturing:** sleep vanaf de bal naar achteren (katapult) of houd Spatie ingedrukt · slepen of ←/→ om de camera te draaien · scrollwiel of +/− om te zoomen · O = overzicht · R = terug (+1 strafslag) · P = pauze · M = geluid aan/uit
