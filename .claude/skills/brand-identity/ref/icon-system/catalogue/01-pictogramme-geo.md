# 01 — Pictogramme géométrique propre (Heroicons-like)

## Nom canonique et alias
- **Nom canonique** : Pictogramme géométrique propre
- **Alias usuels** : Heroicons-style, Phosphor-like, Lucide, Tabler, Iconoir, system icons, UI icons
- **ID stable** : `01-pictogramme-geo`

## Époque d'origine et revivals
- **Origine** : iOS 7 flat (2013) → Material Design (2014) → Heroicons (2020, par les créateurs de Tailwind)
- **État actuel** : style dominant absolu du SaaS / dashboard depuis 2018, omniprésent dans les Figma kits gratuits et payants
- **Risque slop** : c'est l'autoroute statistique du LLM par défaut — choisir ce style demande justification explicite

## Traits formels
- **Stroke** : trait uniforme 1.5px ou 2px, terminaisons rondes (`stroke-linecap: round`), jointures rondes
- **Fill** : variantes Outline (stroke seul) / Solid (fill plein) / Duotone (stroke + fill semi-transparent)
- **Géométrie** : grille stricte 24×24 px par défaut, courbes Bézier propres et symétriques
- **Texture** : zéro texture — propreté vectorielle intégrale
- **Composition** : centrage systématique dans la viewBox, optical balance

## Marques contemporaines qui l'emploient (2024-2026)
1. **Linear** — UI icons, design system (2024-2025)
2. **Vercel** — interface dashboard (2024-2025)
3. **Stripe** — UI components, doc API (2024-2025)
4. **Notion** — interface principale (2024-2026)
5. **Figma** — interface produit (2024-2026)

## Couleurs natives
- **Palette principale** : monochrome currentColor (s'adapte au contexte texte)
- **Variantes** : duotone 2 tons (un fill plein + un stroke + une couleur d'accent)
- **Mode sombre** : inversion currentColor, pas de logique spécifique
- **Compatibilité** : avec n'importe quelle palette de marque (très versatile)

## Formats natifs en stack Claude Code
- **SVG inline** : 1 path principal + 1-2 path secondaires, fills/strokes en `currentColor`
- **Optimisation** : viewBox 24 24, paths optimisés
- **Pas de filter, pas de pattern, pas de gradient** : pureté vectorielle stricte
- **CSS minimal** : `stroke-width`, `stroke-linecap`, `fill` en `currentColor`

## Grain naturel (où la famille brille)
- UI dense (sidebar, toolbar, menu)
- Documentation technique (API doc, design system)
- Marques tech B2B qui se positionnent en "outil sérieux"
- Contextes où la neutralité icon est un atout (= ne pas attirer l'attention)

## Compatibilités concept (tons)
- **Sérieux fonctionnel** : excellent (style natif)
- **Neutre / outil** : excellent
- **Tech B2B SaaS** : excellent (mais risque slop générique)
- **Méthodique / rigoureux** : très bon (précision géométrique)
- **Premium discret** : bon (Linear-like)
- **Chaleureux / accessible** : faible (manque la chaleur)
- **Artisanal / patrimoine** : très faible (anti-matériau)
- **Cinématographique / narratif** : faible (pas de récit)
- **Ludique** : faible (intrinsèquement sérieux)
- **Brut / contre-culture** : faible (= l'establishment)

## Incompatibilités évidentes
- Marques qui veulent une signature graphique distinctive forte → c'est l'opposé
- Marques avec image-pivot pictural ou matérialité revendiquée → clash
- Marques de luxe / héritage → trop tech / startup
- Marques B2C lifestyle / communautaire → trop froid

## Sources datées
- Heroicons v2 (2023) — Tailwind Labs
- Phosphor Icons v2.0 (2024) — phosphoricons.com
- Lucide Icons latest (2025) — fork de Feather Icons
- Tabler Icons v3 (2024) — tabler-icons.io
- Iconoir Icons (2024) — iconoir.com
- *Why Big Tech Logos All Look the Same* — It's Nice That (2023) — critique du blanding qui s'applique aussi aux icônes
- Linear design system principles (2024)
