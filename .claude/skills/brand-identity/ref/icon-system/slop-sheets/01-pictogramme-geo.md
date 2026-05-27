# 01 — Pictogramme géométrique propre — Fiche slop / anti-slop

**Famille** : `01-pictogramme-geo` · **Dernière revue** : 2026-05-27 · **Prochaine revue** : 2026-08-27

**Sources scannées** : Heroicons v2 (2023), Phosphor v2.0 (2024), Lucide latest (2025), Tabler v3 (2024), Iconoir (2024), Linear design system principles (2024), *Why Big Tech Logos All Look the Same* — It's Nice That (juin 2023), *The Blanding of Everything* — The Verge (2022).

---

## À BANNIR — 8 anti-patterns datés

### `[ANTI-01]` Stroke 1.5px uniforme partout sans variation
- **Description** : `stroke-width: 1.5` figé sur tous les paths, aucune hiérarchie sémantique
- **Preuve d'âge** : Heroicons v1 default 2020-2022, omniprésent dans templates Figma 2021-2023
- **Signature slop** : tueur de toute différenciation entre familles d'icônes
- **Contre-exemple pro** : Iconoir 2024 mix stroke 1px/2px par feature line

### `[ANTI-02]` Corner radius 2 partout (look "icon-in-square")
- **Description** : tous les angles arrondis à exactement 2px, conteneur carré arrondi 4px
- **Preuve d'âge** : Material Icons v2 (2018-2021), iOS UI kit 2020-2022
- **Signature slop** : signature templates gratuits Notion/SaaS 2022-2023
- **Contre-exemple pro** : Phosphor v2 angles francs assumés + parties arrondies optical

### `[ANTI-03]` Cercle gris derrière l'icône (en "feature card")
- **Description** : icône monochrome centrée dans un cercle gris pâle (oklch 0.92 ou similaire)
- **Preuve d'âge** : feature section SaaS B2B 2019-2022, vu 50000x sur Dribbble
- **Signature slop** : signature templates "modern dashboard 2020"
- **Contre-exemple pro** : Linear marketing 2024-2025, icônes sans conteneur, ratio espace blanc assumé

### `[ANTI-04]` "Duotone" = juste un aplat semi-transparent derrière le outline
- **Description** : duotone réduit à fill-opacity 0.2 sous le stroke principal
- **Preuve d'âge** : Heroicons solid v1, Phosphor duotone v1 (2021-2022)
- **Signature slop** : paresseux conceptuellement (le vrai duotone joue avec deux PLANS)
- **Contre-exemple pro** : Phosphor v2.0 (2024) duotone redessiné avec opposition de fonctions

### `[ANTI-05]` Sets monochromes + accent vert/orange semi-transparent (Notion template)
- **Description** : tout en gris + UN seul accent (souvent vert ou orange) en semi-opacité
- **Preuve d'âge** : signature templates Notion 2020-2022, Linear v1 2021
- **Signature slop** : illisible, oubliable, interchangeable
- **Contre-exemple pro** : Stripe icons 2024 mix accent par catégorie sémantique forte

### `[ANTI-06]` viewBox 24×24 strict refusant l'adaptation contextuelle
- **Description** : tous les icônes en viewBox 24 24 quel que soit l'usage (16, 32, 48)
- **Preuve d'âge** : Heroicons v1 contrainte 2020, Phosphor v1
- **Signature slop** : icône surchargée à 16px, vide à 48px, jamais bien
- **Contre-exemple pro** : Streamline v5 (2022) propose 16/20/24/32 par variantes optical

### `[ANTI-07]` Joints `stroke-linecap: butt` (terminaisons carrées par défaut)
- **Description** : oubli de spécifier `stroke-linecap: round`, terminaisons sèches
- **Preuve d'âge** : défaut SVG, signature des icônes "non finies" pour le design system pro
- **Signature slop** : amateur, pas pro
- **Contre-exemple pro** : 100% des biblios pro 2024 utilisent `round` par défaut

### `[ANTI-08]` Icônes interchangeables (mêmes 30-50 métaphores partout)
- **Description** : loupe, document, horloge, target, alerte, validé, settings, dashboard, graph — TOUJOURS les mêmes
- **Preuve d'âge** : symptôme du blanding documenté par The Verge 2022
- **Signature slop** : si on enlève le nom de la marque, on ne sait pas dire à qui appartient le set
- **Contre-exemple pro** : Linear 2025 sets contextuels (Triage, Cycles, Roadmap) avec métaphores spécifiques

---

## SIGNATURES PRO 2024-2026 — 5 patterns à reproduire

### `[SIG-01]` Stroke contrasté dans le même set (1px + 2px par hiérarchie)
- **Description** : mix de 2 épaisseurs dans le MÊME set pour signifier une hiérarchie (primary action plus épais, secondary plus fin)
- **Source** : Iconoir 2024, Pillar Icons 2024
- **Implémentation** : 2 stroke-widths distincts par fichier, basés sur fonction sémantique

### `[SIG-02]` Joints "open" délibérés (le trait ne se ferme pas systématiquement)
- **Description** : contours qui laissent un petit gap optical à 1-2 endroits, refus du tracé fermé partout
- **Source** : Lucide 2024-2025, Untitled UI Icons (2024)
- **Implémentation** : path avec ruptures volontaires à des endroits qui ne créent pas d'ambiguïté

### `[SIG-03]` Optical compensation pixel-perfect
- **Description** : décalage de 0.5px sur certains éléments pour compenser l'optical alignment
- **Source** : Streamline v5 (2022), continué par Tabler v3 (2024)
- **Implémentation** : nudging manuel des centres, refus du géométrique pur

### `[SIG-04]` Grille 16/20/24/32 assumée et VISIBLE dans la doc
- **Description** : design system qui documente explicitement les 4 tailles avec optical variants
- **Source** : Streamline v5 (2022), Material Icons v3 (2023)
- **Implémentation** : pour chaque icône, 4 viewBox optimisées (pas un seul SVG scalé)

### `[SIG-05]` Métaphores contextuelles par DOMAINE de la marque
- **Description** : refuser les 30-50 métaphores génériques, dériver les icônes du métier réel
- **Source** : Linear product icons 2024-2025, Vercel infra icons 2024
- **Implémentation** : chaque icône métier = métaphore spécifique au métier, pas Heroicons générique

---

## CHECKS MÉCANIQUES — 2 vérifications

### `[CHK-01]` Au moins 2 stroke-widths distincts dans l'ensemble du set
- **Règle** : pour éviter le 1.5px partout
- **Vérification** : extraire `stroke-width` du HTML, compter les valeurs distinctes ≥ 2

### `[CHK-02]` Tous les paths ont `stroke-linecap="round"` (ou défini en CSS)
- **Règle** : pas de terminaisons sèches amateur
- **Vérification** : grep — toute occurrence de path sans linecap round = warning

### `[CHK-03]` INCARNATION VISIBLE — ≥30% des icônes du set 06.1 ont un mix de stroke-widths
- **Règle** : `[SIG-01]` stroke contrasté DOIT être incarné, pas juste théorique. Au moins 6 icônes sur ~20 doivent contenir ≥2 valeurs `stroke-width` distinctes dans le même SVG
- **Vérification** : pour chaque SVG du set, extraire les `stroke-width=` (et `stroke-width:` CSS), si ≥2 distinctes → l'icône compte. Ratio (icônes mixed-stroke / total) doit être ≥30%
- **Si fail (<30%)** : la signature pro 2024-2026 n'est pas incarnée. Le set ressemble à du Heroicons v1 par défaut (1.5px partout). Re-dispatch designer : "Au moins 6 icônes du set DOIVENT contenir un mix de stroke-widths visible dans la même icône (contour 2px, détails internes 1px)."
