# 02 — Isométrique / 3D

## Nom canonique et alias
- **Nom canonique** : Isométrique / 3D
- **Alias usuels** : axonométrique, iso-illustration, 2.5D, cabinet projection, cavalière
- **ID stable** : `02-isometrique`

## Époque d'origine et revivals
- **Origine** : projection isométrique mathématique (Pohlke 1860), popularisée par les jeux vidéo 1980-1990 (SimCity, Diablo)
- **Pic mainstream** : 2017-2021 (Stripe website, Sketch, Slack illustrations)
- **Tournant 2022-2026** : la version "pastel iso" 2017-2019 est devenue cliché ; les marques pros pivotent vers iso plus dense / plus contrasté / mode sombre (Vercel, Cloudflare visualisations infra)

## Traits formels
- **Stroke** : optionnel, si présent 1-2px dans une couleur de la palette (jamais noir par défaut)
- **Fill** : 3-4 plans de couleur par objet (top + 2 côtés), nuances calculées à partir de la couleur de base
- **Géométrie** : axonométrie 30° (isométrique pure) ou cabinet 45° (plus dynamique), grille stricte
- **Texture** : optionnelle, grain léger possible en signature 2024-2026
- **Composition** : centrage avec point de fuite implicite, profondeur volumétrique assumée

## Marques contemporaines qui l'emploient (2024-2026)
1. **Cloudflare** — visualisations infrastructure (2024-2025)
2. **Vercel** — illustrations features (2024)
3. **Streamline Icons 3D** — bibliothèque référence (2022-2025, streamlineicons.com)
4. **Iconscout 3D** — bibliothèque 3D illustrative (2024-2025)
5. **Framer** — sections marketing iso (2024)

## Couleurs natives
- **Palette principale** : 3 nuances de la même teinte (light/mid/dark) par objet pour le shading
- **Multicolore** : 3-5 couleurs distinctes pour les objets différents
- **Mode sombre** : variante "iso wireframe" — uniquement stroke, sans fills, sur fond profond
- **Pas de gradient lisse** : profondeur par aplats de couleurs nuancées, pas par dégradé

## Formats natifs en stack Claude Code
- **SVG inline avec calculs géométriques** : polygones définis manuellement selon axonométrie 30°
- **3 polygones par face cubique** : top + côté gauche + côté droit, chacun avec son fill calculé
- **Stroke optionnel** : pour les arêtes (1px dans une couleur sombre de la palette)
- **CSS `transform: rotate3d()` possible** mais souvent contourné par axonométrie SVG pure (plus fiable)

## Grain naturel (où la famille brille)
- Hero éditorial conceptuel (visualiser une "architecture", un "système", une "construction")
- Marques infrastructure / cloud / système (clairement)
- Marques edutech / dataviz / visualisation de processus
- Concepts qui demandent de représenter de l'EMPILEMENT, de la STRUCTURE, ou de la TRANSFORMATION

## Compatibilités concept (tons)
- **Système / infrastructure** : excellent (signature native)
- **Construction / empilement** : excellent
- **Méthodique / rigoureux** : très bon (géométrie stricte)
- **Tech / outil** : très bon (tech crédible mais distinctif)
- **Premium tech** : bon (Cloudflare-like)
- **Ludique** : bon (héritage jeu vidéo)
- **Éditorial / narratif** : moyen (la projection iso est plus conceptuelle que narrative)
- **Artisanal / patrimoine** : faible (anti-artisanal)
- **Cinématographique** : faible (la projection iso casse l'immersion)
- **Brut / contre-culture** : faible

## Incompatibilités évidentes
- Marques éditoriales long-form (Mubi, Substack) → trop construit
- Marques de luxe héritage → trop technique
- Marques wellness / B2C lifestyle → trop froid
- Concepts qui demandent de la matière vivante / pictural → anti

## Sources datées
- Streamline 3D Icons (2022-2025) — streamlineicons.com
- Cloudflare illustrations 2024 — cloudflare.com
- Vercel Conf 2024 — illustrations événementiel
- Iconscout 3D 2024 — iconscout.com/3ds
- Framer marketing site 2024 — framer.com
- *The Return of Isometric Design (Without the Pastel)* — Eye on Design AIGA, août 2024
