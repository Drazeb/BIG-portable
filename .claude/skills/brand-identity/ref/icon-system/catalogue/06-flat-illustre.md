# 06 — Flat illustré coloré

## Nom canonique et alias
- **Nom canonique** : Flat illustré coloré (variante "spot illustration")
- **Alias usuels** : flat illustration, spot illu, Notion-style, vector illustration, editorial flat
- **ID stable** : `06-flat-illustre`

## Époque d'origine et revivals
- **Origine** : aplats des affiches suisses (Müller-Brockmann 1950s) → repris en illustration éditoriale digitale début 2010s
- **Pic mainstream** : 2014-2020 (Google Material spot illu, Dropbox redesign 2017, Slack 2018, Notion 2019)
- **Tournant 2022-2026** : la version "Dropbox/Headspace pastel pâle" est devenue cliché ; les marques pros pivotent vers le flat illustré **éditorial cinéma** (palette plus contrastée, narration figurative, références cinéma / peinture)

## Traits formels
- **Stroke** : optionnel (le flat illustré moderne le réduit ou l'élimine). Si présent, contrasté avec les aplats (couleur saturée)
- **Fill** : aplats généreux de 3-6 couleurs par illustration, jamais de gradient lisse — la profondeur se fait par **superposition de plans aplats** (système "papier découpé")
- **Géométrie** : formes simplifiées mais identifiables (= pas abstraites comme l'ornemental, pas littérales comme la photo)
- **Texture** : possible grain photoshop léger (noise overlay) pour casser le côté "trop vectoriel propre" — signature 2024-2026
- **Composition** : narrative, souvent figures humaines simplifiées + objets métier, scène complète

## Marques contemporaines qui l'emploient (2024-2026)
1. **Linear** — illustrations marketing (flat moderne, palette graphique, observé été 2025) — [linear.app](https://linear.app)
2. **Pitch** — site marketing (flat éditorial sombre + accents saturés, 2024-2025)
3. **Arc Browser** — sections fonctionnalités (flat avec profondeur par plans, 2024)
4. **Substack** — illustrations newsletter écrivains (flat illustré éditorial, mode partiellement sombre, 2025)
5. **Mubi Notebook** — illustrations articles cinéma (flat illustré cinématographique, palette nuit/clair-obscur, 2024-2026)

## Couleurs natives
- **Palette principale** : 3-6 couleurs par illustration, contrastées, jamais pastel anémique
- **Mode sombre** : variante "flat illustré cinéma" — fond profond (charbon, indigo, bordeaux), aplats lumineux qui pop (laiton, ocre, ivoire)
- **Pas de gradients réalistes** — si gradient, c'est un dégradé bichrome assumé en aplat
- **Combinaisons fortes** : noir/crème + 1 accent ; indigo nuit + laiton + crème ; bordeaux + ocre + crème
- **Anti-palette** : pastels lavés Headspace-style, ou "blanding" pastel pâle 2018-2022

## Formats natifs en stack Claude Code
- **SVG inline multicouche** : 3-6 `<path>` ou `<polygon>` superposés, chacun en aplat de couleur
- **Pas de gradient SVG** : préférer juxtaposition de 2-3 aplats pour la "profondeur"
- **`filter` noise SVG** : `feTurbulence` + `feColorMatrix` pour overlay grain léger (signature 2024-2026)
- **Stroke optionnel** : 0.5px à 2px max, dans une couleur de la palette (pas du noir par défaut)
- **CSS `mix-blend-mode`** : utile pour les overlays narratifs (multiply, screen) sur compositions complexes

## Grain naturel (où la famille brille)
- Hero éditorial narratif (raconte une histoire en un coup d'œil)
- Spot illustrations pour articles / blog / newsletter
- Pictogrammes "feature card" avec scène contextuelle (pas juste un symbole)
- Marques qui veulent l'accessibilité B2C tout en restant éditoriales
- Concepts cinématographiques, narration figurative, palette nocturne contrastée

## Compatibilités concept (tons)
- **Chaleureux / accessible** : excellent (par défaut)
- **Cinématographique / nocturne** : excellent (variante flat cinéma, palette contrastée)
- **Éditorial / narratif** : excellent (signature naturelle)
- **Premium éditorial** : très bon (Mubi-like)
- **Méthodique / rigoureux** : bon si composition très structurée
- **Sérieux** : bon (à condition de palette charpentée, pas pastel)
- **Tech-startup neutre** : bon mais risque slop Notion-pastel
- **Brut / contre-culture** : faible (manque la matérialité)
- **Patrimoine ancien / artisanal** : faible (trop moderne par codes)

## Incompatibilités évidentes
- Marques qui demandent une matérialité ancienne (gravure / artisanat) → trop digital
- Marques qui demandent monochrome strict → tue le potentiel de la famille
- Concepts qui exigent forte autorité institutionnelle stricte → manque la gravité
- Mode sombre pure tech (uniquement neutres) → demande accents colorés

## Sources datées
- Linear — Marketing site, observé juillet 2025
- Mubi Notebook — articles éditoriaux 2024-2026
- *The Death of Corporate Memphis* — Eye on Design AIGA, mai 2024 (chronique sur la mort du pastel anémique)
- *Why Big Tech Logos All Look the Same* — It's Nice That, juin 2023
- Substack — newsletters featured writers 2025
- Pitch — site marketing redesign 2024
- COLLINS — Robinhood rebrand 2023, illustrations style guide
- Order Design (Jesse Reed) — projet "Mailchimp Illustration System" v2 (référence flat narratif systémique)
