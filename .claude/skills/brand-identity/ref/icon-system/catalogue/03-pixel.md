# 03 — Pixel art

## Nom canonique et alias
- **Nom canonique** : Pixel art
- **Alias usuels** : 8-bit, 16-bit, bitmap art, pixelated, retro game art, low-res mosaic
- **ID stable** : `03-pixel`

## Époque d'origine et revivals
- **Origine** : contrainte hardware jeu vidéo 1980s (Atari, NES, Game Boy)
- **Revival mainstream** : 2010s indie game (Stardew Valley, Celeste, Hyper Light Drifter)
- **2024-2026** : revival "brand identity" — Cassette tape, Are.na (partiel), GitHub Pixels initiative (2024), marques tech-counterculture qui revendiquent l'héritage hacker

## Traits formels
- **Stroke** : aucun stroke conventionnel — la "ligne" est faite de pixels adjacents
- **Fill** : rectangles `<rect>` SVG sur grille stricte 12×12, 16×16, 24×24 ou 32×32 unités
- **Géométrie** : grille pixel STRICTE, refus de l'anti-aliasing (`shape-rendering: crispEdges`)
- **Texture** : la grille est la texture — pixels visibles assumés
- **Composition** : symétrie possible mais asymétries pixel-perfect signature

## Marques contemporaines qui l'emploient (2024-2026)
1. **GitHub Pixels** — initiative 2024, pixel art celebration
2. **Cassette Tape** — identité 2024 (label musical)
3. **itch.io** — interface depuis 2020, plus assumé en 2024-2026
4. **Lo-fi Hip Hop streams** — pixel art omniprésent sur YouTube Live
5. **Twitch emote ecosystem** — pixel emotes 2024-2026

## Couleurs natives
- **Palette stricte** : 4-8 couleurs MAXIMUM par icône (contrainte hardware historique)
- **Palettes nommées** : DB16 (16 couleurs), Pico-8 palette (16 couleurs), Game Boy 4 nuances
- **Mode sombre** : variante "1-bit" (noir/blanc strict) possible et signature
- **Pas de dégradés** : par construction (pixel = couleur unique)

## Formats natifs en stack Claude Code
- **SVG `<rect>` sur grille** : avec `shape-rendering="crispEdges"` ABSOLUMENT obligatoire
- **viewBox petite** : 12 12, 16 16, 24 24 (jamais plus grand)
- **CSS grid possible** : alternative aux SVG rects (mais SVG plus propre)
- **Couleurs en hex strict** : pas d'opacité, pas d'`oklch` (anti-aliasing implicite)

## Grain naturel (où la famille brille)
- Marques tech-retro / gaming / dev tools / hacker culture
- Marques counterculture qui refusent les codes corporate
- Marques avec héritage 80s-90s / nostalgie assumée
- Identités "indie / artisanal / fait-main numérique"
- Mascottes / favicons / petits éléments d'interface qui doivent être reconnaissables à 16×16

## Compatibilités concept (tons)
- **Brut / contre-culture** : excellent (signature native)
- **Geek / tech-pointue** : excellent
- **Retro / nostalgie** : excellent
- **Ludique / gaming** : excellent
- **Indie / artisanal numérique** : excellent
- **Minimalisme / contrainte** : très bon (par contrainte hardware)
- **Sérieux / corporate** : très faible (anti-corporate par essence)
- **Premium / luxe** : très faible
- **Patrimoine ancien / artisanal physique** : faible (anti-physique)
- **Éditorial long-form** : faible (illisible à grande taille)

## Incompatibilités évidentes
- Marques B2B SaaS sérieuses → trop décalé
- Marques luxe / institutional → choquerait la cible
- Marques bien-être / lifestyle adulte → trop ludique
- Hero à grande échelle → la pixel art reste petite par nature

## Sources datées
- GitHub Pixels initiative (2024) — github.com/pixels
- Cassette Tape identity 2024 — observé via Brand New
- Pico-8 community (2024-2026) — Lexaloffle
- itch.io interface 2024-2026
- *Pixel Art's Quiet Renaissance in Branding* — It's Nice That, novembre 2024
- DB16 / DB32 palettes — DawnBringer (référence historique 2009, toujours utilisée)
- Pico-8 16-color palette — Lexaloffle (2014, standard de facto 2024)
