# Spécification Technique HTML/CSS — Style-Tile Showroom

Ce document comble le gap du système Gemini (la "FICHE FORMAT HTML" qui n'existait pas en tant que fichier dédié). Il définit les contraintes techniques pour la génération du fichier HTML Zone 1.

---

## 1. ARCHITECTURE DU FICHIER

### Single-File Self-Contained
Le Style-Tile est un **fichier HTML unique** contenant tout le CSS inline (pas de fichier externe).

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Brand} — Style-Tile — {Concept Name}</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family={Display}:wght@...&family={Body}:wght@...&display=swap" rel="stylesheet">
    <style>
        /* CSS Custom Properties + Tout le CSS ici */
    </style>
</head>
<body>
    <!-- Section A: Voice Block -->
    <!-- Section B: Artefact Témoin -->
    <!-- Section C: Atmosphere Block -->
</body>
</html>
```

---

## 2. CSS CUSTOM PROPERTIES (Obligatoires)

Le fichier DOIT déclarer ses variables design dans `:root`. C'est la colonne vertébrale technique invisible.

```css
:root {
    /* === PALETTE === */
    --color-primary: #...;
    --color-primary-light: #...;
    --color-primary-dark: #...;
    --color-secondary: #...;
    --color-accent: #...;
    --color-surface: #...;
    --color-surface-alt: #...;
    --color-text-primary: #...;
    --color-text-secondary: #...;
    --color-text-on-primary: #...;

    /* === TYPOGRAPHIE === */
    --font-display: '{Display Font}', {fallback};
    --font-body: '{Body Font}', {fallback};
    --font-mono: 'JetBrains Mono', monospace; /* si applicable */

    /* === TYPE SCALE === */
    --type-scale-ratio: {ratio}; /* 1.200 / 1.333 / 1.414 selon Curseur A */
    --text-xs: 0.75rem;
    --text-sm: 0.875rem;
    --text-base: 1rem;
    --text-lg: calc(var(--text-base) * var(--type-scale-ratio));
    --text-xl: calc(var(--text-lg) * var(--type-scale-ratio));
    --text-2xl: calc(var(--text-xl) * var(--type-scale-ratio));
    --text-3xl: calc(var(--text-2xl) * var(--type-scale-ratio));
    --text-4xl: calc(var(--text-3xl) * var(--type-scale-ratio));

    /* === CODE CIVIL ATOMIQUE === */
    /* === RADIUS — la philosophie vient du concept === */
    /* Minimum 2 niveaux requis pour les batchs suivants. Nommage libre. */

    /* === OMBRES — multi-couches obligatoire (si le concept utilise des shadows) === */
    --shadow-sm: 0 1px 2px oklch(... / .06), 0 4px 8px oklch(... / .03);
    --shadow-md: 0 2px 4px oklch(... / .06), 0 8px 20px oklch(... / .04), 0 20px 48px oklch(... / .025);
    --shadow-lg: 0 3px 6px oklch(... / .07), 0 12px 28px oklch(... / .05), 0 28px 56px oklch(... / .03);
    /* Alternative flat : --shadow-sm: none; --shadow-md: none; (si concept intentionnellement flat) */

    --space-unit: 8px; /* ou 4px */
    --space-xs: calc(var(--space-unit) * 1);
    --space-sm: calc(var(--space-unit) * 2);
    --space-md: calc(var(--space-unit) * 3);
    --space-lg: calc(var(--space-unit) * 5);
    --space-xl: calc(var(--space-unit) * 8);
    --space-2xl: calc(var(--space-unit) * 13);

    /* === TRANSITIONS — courbes physiques, jamais `ease` seul === */
    --ease-out-expo: cubic-bezier(.16, 1, .3, 1);
    --ease-out-back: cubic-bezier(.34, 1.56, .64, 1);
    --transition-fast: 120ms var(--ease-out-expo);
    --transition-base: 250ms var(--ease-out-expo);
    --transition-slow: 450ms cubic-bezier(.22, 1, .36, 1);
}
```

---

## 3. GOOGLE FONTS — INTÉGRATION

### Règles
- **Obligatoire** : Utiliser Google Fonts pour toutes les polices (garantit l'accessibilité universelle)
- **Display font** : Charger les weights nécessaires (400, 500, 600, 700 minimum)
- **Body font** : Charger 400, 400italic, 500, 600, 700
- **Preconnect** : Toujours inclure les liens preconnect pour la performance

### Sélection indexée sur les curseurs

**Principes :**
- CHOISIR dans le pool correspondant au curseur A ci-dessous — chaque pool contient 50+ options, c'est suffisant pour être singulier
- Si tu veux une font HORS pool : elle DOIT être vérifiée sur fonts.google.com ET correspondre au caractère décrit pour le curseur A
- INTERDIT de réutiliser les fonts des exemples fournis (Brygada 1918, Schibsted Grotesk, Prata, Alegreya Sans, Darker Grotesque, Space Mono)
- Viser la SINGULARITÉ : chaque projet mérite une combinaison typographique qu'on ne retrouve pas chez ses concurrents
- Les pairings serif+sans NE SONT PAS la seule option valide — sans+sans, serif+serif, sans+mono, display+mono sont tous légitimes selon le concept

**A=1 (Prudent)** — Pairings classiques et éprouvés :
- Caractère : lisibilité maximale, familiarité, confiance
- Pool display (~50, majorité serif + quelques sans classiques) : Brygada 1918, Labrada, Gilda Display, Marcellus, Faustina, Aleo, Neuton, Frank Ruhl Libre, Libre Caslon Display, Noto Serif Display, Petrona, Signika, Tinos, Zilla Slab, Gelasio, Domine, Encode Sans, Cabin, Barlow, Vollkorn, Cardo, Bitter, Spectral, Alegreya, Noto Sans Display, Ubuntu, Arimo, Chivo, Libre Franklin, Roboto Serif, IBM Plex Serif, Roboto Slab, Quicksand, Comfortaa, Josefin Sans, Outfit, Nunito, Cormorant Garamond, EB Garamond, PT Serif, Crimson Text, Noto Serif, Source Serif 4, Libre Baskerville, Merriweather, Lora, Raleway, Montserrat, Poppins, Playfair Display
- Pool body (~50, majorité sans + quelques serifs) : Geist, Schibsted Grotesk, Catamaran, Sarabun, Cantarell, Maven Pro, Hanken Grotesk, Encode Sans, Overpass, Hind, Archivo, Wix Madefor Text, Atkinson Hyperlegible, Red Hat Text, Instrument Sans, Lexend, Be Vietnam Pro, Albert Sans, Figtree, Urbanist, Outfit, Karla, Rubik, Plus Jakarta Sans, Manrope, Public Sans, Nunito Sans, Work Sans, Mulish, Noto Sans, Fira Sans, Ubuntu, Lato, Roboto, Open Sans, Literata, Newsreader, Roboto Serif, Crimson Text, Noto Serif, Merriweather, Lora, Source Serif 4, PT Sans, Libre Franklin, Chivo, IBM Plex Sans, DM Sans, Source Sans 3, Inter
- Type-scale : ratio ≤ 1.200

**A=2 (Décalé)** — Un display distinctif qui crée une voix reconnaissable :
- Caractère : personnalité affirmée, un trait mémorable (contrastes, géométrie, optical sizing)
- Pool display (~50, mix sans distinctifs + serifs éditoriaux) : Bricolage Grotesque, Gabarito, Calistoga, Manuale, Tenor Sans, Epilogue, Brygada 1918, Labrada, Sansita, Prata, Anybody, Commissioner, Geologica, Onest, Ancizar Serif, Wix Madefor Display, Gloock, Jost, Crimson Pro, Frank Ruhl Libre, Cormorant, Zalando Sans, Noto Serif Display, Roboto Serif, Libre Caslon Display, Red Hat Display, Albert Sans, Figtree, Urbanist, Instrument Sans, Lexend, Josefin Sans, Sora, Overpass, Libre Franklin, Archivo, Literata, Hanken Grotesk, Be Vietnam Pro, Schibsted Grotesk, Outfit, Maven Pro, IBM Plex Serif, Newsreader, Poppins, DM Serif Display, Playfair Display, Young Serif, Fraunces, Space Grotesk
- Pool body (~50) : Rethink Sans, Geist, Alegreya Sans, Spectral, Crimson Pro, Encode Sans, Commissioner, Onest, Epilogue, Instrument Sans, Barlow, Cabin, Noto Sans, Urbanist, Outfit, Wix Madefor Text, Atkinson Hyperlegible, Be Vietnam Pro, Lexend, Figtree, Albert Sans, Red Hat Text, Overpass, Hind, Mulish, Karla, Plus Jakarta Sans, Manrope, Public Sans, Nunito Sans, Work Sans, Lora, Source Serif 4, Literata, Newsreader, Noto Serif, Schibsted Grotesk, Hanken Grotesk, Ubuntu, PT Sans, Fira Sans, Libre Franklin, Roboto, Lato, Chivo, Open Sans, IBM Plex Sans, Source Sans 3, DM Sans, Inter
- Type-scale : ratio 1.250–1.333

**A=3 (Rupture)** — Display expérimental, variable fonts autorisées :
- Caractère : axes optiques, contrastes inattendus, terminaisons singulières, géométries non-standard
- Type-scale : ratio ≥ 1.414

**⚠ SÉLECTION VISUELLE (tous curseurs)** : le subagent reçoit des PLANCHES VISUELLES (images) avec les fonts numérotées, pas les noms. Il choisit sur l'apparence. L'orchestrateur traduit les numéros via les fichiers mapping dans `ref/font-pools/`. Les catégories ci-dessous restent une référence pour la composition des pools et la régénération des planches.

Pool display A=3 — CATÉGORIES :

| # | Catégorie | Description | Fonts |
|---|-----------|-------------|-------|
| D1 | Serif haut contraste | Contraste très marqué entre pleins et déliés, terminaisons fines, filiation Didone ou transitionnelle | Bodoni Moda, Abril Fatface, Cormorant Garamond, DM Serif Display, Gloock |
| D2 | Serif expressif | Empattements prononcés ou formes non-conventionnelles, densité forte sur la ligne de base | Eczar, Young Serif, Fraunces, Kalnia Glaze, Instrument Serif, Calistoga |
| D3 | Sans condensé | Largeur réduite, verticalité marquée, contreformes étroites | Darker Grotesque, Bebas Neue, Big Shoulders Inline, Funnel Display, Genos, Tourney, Bungee |
| D4 | Sans grotesque | Détails distinctifs sur un tracé neutre, ouvertures moyennes, chasse régulière | Familjen Grotesk, Schibsted Grotesk, Chivo, Rethink Sans, Bricolage Grotesque, Special Gothic Expanded One, Gabarito |
| D5 | Sans géométrique | Formes construites sur cercle, carré ou triangle, régularité stricte, terminaisons nettes | Righteous, Syne, Unbounded, Audiowide, Tektur, Rubik Mono One |
| D6 | Display volumétrique | Formes avec perspective ou profondeur, simulation de volume ou de rotation spatiale | Tilt Neon, Tilt Prism, Foldit, Nabla, Rampart One |
| D7 | Display texture/surface | Effets graphiques intégrés aux glyphes, surface ornementée, couches chromatiques | Rubik Glitch, Rubik Spray Paint, Rubik Wet Paint, Honk, Moirai One, Monoton, Bagel Fat One, Cairo Play, Climate Crisis |
| D8 | Display pixel/grille | Construction modulaire sur grille, pixels visibles, structure numérique | Sixtyfour, Pixelify Sans, Handjet, Silkscreen, Press Start 2P |

Overlaps autorisés (fonts éligibles dans une 2e catégorie) :
- Fraunces → aussi D1 (haut contraste dans les graisses fortes, axe WONK)
- Instrument Serif → aussi D1 (contraste élevé, proportions raffinées)
- Cormorant Garamond → aussi D2 (très expressif en grand corps)

Pool body A=3 — CATÉGORIES :

| # | Catégorie | Description | Fonts |
|---|-----------|-------------|-------|
| B1 | Sans humaniste | Tracé d'origine calligraphique, ouvertures larges, variations d'épaisseur organiques | Inclusive Sans, Rethink Sans, Atkinson Hyperlegible, Be Vietnam Pro, Lexend, Outfit, Encode Sans, Sono, Shantell Sans |
| B2 | Sans grotesque | Tracé neutre, chasse régulière, ouvertures moyennes | Familjen Grotesk, Schibsted Grotesk, Reddit Sans, Funnel Sans, Darker Grotesque, IBM Plex Sans, Source Sans 3, Inter, Space Grotesk, Geologica |
| B3 | Mono contemporain | Chasse fixe, dessin épuré, formes ouvertes, lisibilité hors contexte technique | Recursive, Geist Mono, Martian Mono, Azeret Mono, Red Hat Mono, DM Mono, Fragment Mono, Victor Mono, Kode Mono |
| B4 | Mono technique | Chasse fixe, optimisé pour la lecture longue, ligatures fréquentes | Fira Code, JetBrains Mono, Source Code Pro, Roboto Mono, IBM Plex Mono, Inconsolata, Ubuntu Mono, Noto Sans Mono |
| B5 | Mono à personnalité | Chasse fixe, dessin distinctif, formes reconnaissables entre toutes | Syne Mono, B612 Mono, Atkinson Hyperlegible Mono, Chivo Mono, Reddit Mono, Space Mono, Anonymous Pro |
| B6 | Mono vintage/mécanique | Chasse fixe, empreinte rétro ou mécanique, empattements ou terminaisons marquées | Spline Sans Mono, Share Tech Mono, Xanh Mono, Nova Mono, Cutive Mono, Overpass Mono, Courier Prime |

---

## 4. STRUCTURE DES 3 SECTIONS (TRIPTYQUE)

### Section A — Voice Block
```html
<section class="voice-block">
    <!-- FONCTION : transmettre la personnalité de marque en 3 secondes -->
    <!-- TOKENS À MONTRER : display font, palette dominante, au moins 1 CTA -->
    <!-- FORME LIBRE : hero, composition typo, full-bleed, split, animation... -->
    <!-- Le concept détermine la forme — pas l'inverse -->
</section>
```

**Objectif** : En 3 secondes, on comprend la personnalité de la marque.

### Section B — Artefact Témoin (généré en 2 temps)
```html
<section class="artifact-witness">
    <!-- PHASE 1 (Designer création) : génère le CADRE — fond, grain, overlay, 3ème couche -->
    <!-- + le commentaire <!-- ARTEFACT_PLACEHOLDER --> ET RIEN D'AUTRE. -->
    <!-- ⛔ NE PAS générer ici de composant / table / KPI / liste / formulaire. -->
    <!-- La zone reste vide (hors grain + overlays + placeholder) jusqu'à la Phase 2. -->
    <!-- PHASE 2 (Designer artefact, subagent dédié) : remplace le placeholder par le COMPOSANT. -->
    <!-- La méthode de génération du composant est dans phase-4-artefact.md. -->
    <!-- ⚠ NE consulte cette méthode QUE si tu es le subagent artefact. -->
</section>
```

**Objectif** : Section générée en 2 temps — d'abord le cadre (Phase 1), puis le composant applicatif (Phase 2). Le composant prouve que le système design fonctionne sur un écran réaliste. Sa méthode de génération vit dans `phase-4-artefact.md`. Les composants additionnels nécessaires à l'exhaustivité du système de signes sont documentés dans le Batch 2 (Phase 6A, chapitre 04 — Code Civil Atomique).

### Section C — Atmosphere Block
```html
<section class="atmosphere-block">
    <!-- FONCTION : montrer la palette en inversion et laisser une impression durable -->
    <!-- TOKENS À MONTRER : palette contrastée, atmosphère, navigation -->
    <!-- FORME LIBRE : pas obligatoirement sombre — peut être clair, coloré, texturé -->
    <!-- Contenu : slogan, mini-manifesto, copyright, liens fictifs -->
    <!-- INTERDICTION : nuanciers, noms de fonts, specs techniques -->
</section>
```

**Objectif** : Laisser une impression émotionnelle durable.

---

## 5. DIRECTIVES DE QUALITÉ VISUELLE

### Densité et richesse
- Le HTML doit être **visuellement riche** — pas un squelette avec 3 divs
- Utiliser des éléments décoratifs CSS (gradients, formes, lignes) pour l'atmosphère
- Le résultat doit être visuellement riche et complet — la qualité prime sur la quantité
- Chaque section doit respirer — l'espace vertical sert le concept

### Responsive
- Le fichier doit être **lisible** sur un écran de 1200px minimum
- Pas besoin d'être full-responsive (c'est un style-tile, pas un site de production)
- Utiliser `max-width` sur les conteneurs principaux (1200px recommandé)

### Couleurs et contraste
- Respecter WCAG 2.1 AA minimum pour le texte
- Utiliser les custom properties systématiquement (pas de valeurs hardcodées dans le HTML)

### Détails qui font la différence
- Utiliser `letter-spacing` sur les overlines et les éléments en caps
- Appliquer `font-feature-settings` si pertinent (tabular nums pour les données)
- Des `transitions` sur les éléments interactifs (boutons, cartes)
- Des `backdrop-filter` ou `mix-blend-mode` pour les sections à atmosphère

### Finition élite (universel)
- Ombres multi-couches : ≥2 niveaux empilés par box-shadow (contact + ambient minimum)
- Easing physiques : cubic-bezier nommés dans :root, utilisés dans toutes les transitions
- Rythme de spacing : les 3 sections ont des padding-block DIFFÉRENTS
- Hovers multi-property : chaque élément interactif change ≥2 propriétés (pas juste background-color seul)
- Retenue : transformations subtiles (scale 1.01-1.02), transitions fluides, pas de saut visuel

---

## 6. VOCABULAIRE CSS MODERNE (2023-2026)

Un style-tile est visualisé dans un navigateur moderne (Chrome/Safari dernière version). Tu DOIS exploiter les capacités CSS actuelles — pas te limiter au CSS de 2019. **Utilise au minimum 3-4 techniques de cette liste** dans chaque style-tile.

### Couleur moderne
| Technique | Usage | Exemple |
|-----------|-------|---------|
| `oklch()` | Espace perceptuel uniforme — meilleurs gradients, palettes plus vivantes | `color: oklch(0.7 0.15 145)` |
| `color-mix()` | Mélange de couleurs en CSS — variantes automatiques sans hardcoder | `color-mix(in oklch, var(--color-primary) 80%, white)` |
| `light-dark()` | Valeurs conditionnelles clair/sombre | `color: light-dark(#1a1a1a, #f5f5f5)` |

**Cas d'usage style-tile** : Déclarer la palette en `oklch()` dans le `:root` permet des gradients perceptuellement uniformes (pas de zone grise au milieu). `color-mix()` remplace les variantes `-light`/`-dark` hardcodées.

### Architecture CSS
| Technique | Usage | Exemple |
|-----------|-------|---------|
| `@layer` | Couches de cascade explicites — reset, tokens, components, utilities | `@layer reset, tokens, components, utilities;` |
| `@property` | Custom properties typées — rend les variables ANIMABLES | `@property --hue { syntax: '<angle>'; inherits: false; initial-value: 0deg; }` |
| `@scope` | Scoping CSS natif — isole les styles par section | `@scope (.artifact-witness) { ... }` |

**Cas d'usage style-tile** : `@layer` organise proprement le CSS (reset → tokens → sections). `@property` permet d'animer des couleurs oklch ou des gradients — impossible avec les custom properties classiques.

### Layout moderne
| Technique | Usage | Exemple |
|-----------|-------|---------|
| `subgrid` | Héritage d'axes de grille parent → alignements parfaits | `grid-template-columns: subgrid` |
| `@container` | Media queries au niveau composant — l'artefact s'adapte à son conteneur | `@container (min-width: 600px) { ... }` |
| Logical properties | `margin-inline`, `padding-block` — layout agnostique à la direction | `padding-inline: var(--space-lg)` |

**Cas d'usage style-tile** : `subgrid` pour aligner les éléments de l'artefact témoin. `@container` pour un artefact qui se restructure selon sa taille (pas la taille du viewport).

### Typographie avancée
| Technique | Usage | Exemple |
|-----------|-------|---------|
| `text-wrap: balance` | Équilibre automatique des lignes de heading | `h1 { text-wrap: balance }` |
| `text-wrap: pretty` | Évite les orphelins dans les paragraphes | `p { text-wrap: pretty }` |
| `font-variation-settings` | Axes variables (si variable font) — wght, wdth, opsz, GRAD | `font-variation-settings: 'opsz' 72, 'GRAD' 150` |
| `clamp()` pour typo fluide | Tailles qui s'adaptent au viewport sans media queries | `font-size: clamp(2rem, 5vw, 5rem)` |

**Cas d'usage style-tile** : `text-wrap: balance` sur tous les titres. `clamp()` pour le hero heading. Variable font axes si la font le supporte.

### Effets visuels & formes
| Technique | Usage | Exemple |
|-----------|-------|---------|
| `clip-path` | Découpe géométrique — diagonales, polygones, formes libres | `clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%)` |
| `mask-image` | Masque avec gradient ou SVG — fondus, textures, révélations | `mask-image: linear-gradient(to bottom, black 60%, transparent)` |
| `backdrop-filter` | Flou et effets sur l'arrière-plan (glassmorphism, etc.) | `backdrop-filter: blur(10px) saturate(1.3)` |
| `mix-blend-mode` | Fusion de couches — overlay, multiply, difference, exclusion | `mix-blend-mode: overlay` |
| SVG filters inline | Grain, noise, displacement — textures matérielles sans images | `<filter id="grain"><feTurbulence baseFrequency="0.65"/>` |

**Cas d'usage style-tile** : `clip-path` pour des transitions de section non-rectangulaires. `mask-image` pour des fondus atmosphériques. SVG noise pour la matérialité.

### Animation & interaction
| Technique | Usage | Exemple |
|-----------|-------|---------|
| `@starting-style` | État initial pour les transitions d'entrée (apparition fluide) | `@starting-style { opacity: 0; transform: translateY(20px); }` |
| `animation-timeline: view()` | Animations déclenchées par le scroll — sans JS | `animation-timeline: view(); animation-range: entry 0% cover 40%;` |
| `linear()` easing | Courbes d'easing personnalisées (bounce, spring, elastic) | `transition: transform 0.5s linear(0, 0.5 30%, 1.1 70%, 1)` |
| `@keyframes` + `oklch` | Animations de couleur perceptuellement uniformes | `from { background: oklch(0.5 0.2 0) } to { background: oklch(0.5 0.2 360) }` |

**Cas d'usage style-tile** : `animation-timeline: view()` pour des reveal au scroll. `@starting-style` pour l'apparition initiale des éléments.

### Sélecteurs modernes
| Technique | Usage | Exemple |
|-----------|-------|---------|
| `:has()` | Sélection de parent basée sur enfant — styles conditionnels | `.card:has(img) { grid-template-rows: auto 1fr; }` |
| `:where()` / `:is()` | Groupement de sélecteurs sans spécificité (`:where`) ou avec (`:is`) | `:where(.voice-block, .atmosphere-block) p { ... }` |
| `@container style()` | Style queries — conditionnel sur la valeur d'une custom property | `@container style(--theme: dark) { ... }` |

### RÈGLE D'UTILISATION
- **Socle de finition (TOUJOURS)** : `oklch()`, `@layer`, `@property`, `color-mix()`, `text-wrap: balance/pretty`, `clamp()` — ces 6 techniques sont de l'infrastructure invisible qui améliore tout style-tile, quel que soit le concept
- **Bonus contextuel (SI pertinent)** : `@container`, `:has()`, `clip-path`, `mask-image`, `animation-timeline`, `@starting-style` — ces techniques résolvent des problèmes spécifiques et ne doivent être utilisées que quand le composant s'y prête
- Chaque technique doit **servir le design**, pas être décorative — pas de container query sur un élément qui ne change jamais de taille, pas de :has() sur du contenu statique
- **oklch() est FORTEMENT RECOMMANDÉ** pour la palette — les gradients sont objectivement meilleurs qu'en hex/rgb

---

## 7. CHECKLIST PRÉ-GÉNÉRATION

Avant de générer le HTML, le subagent vérifie :

- [ ] Les Google Fonts sont bien chargées via `<link>`
- [ ] Toutes les custom properties sont déclarées dans `:root`
- [ ] Le type-scale ratio correspond au Curseur A
- [ ] La palette correspond aux choix de la Phase 3
- [ ] Le contenu est fictif mais réaliste et aligné avec le brief
- [ ] **Screenshot Test** : Zéro donnée technique visible
- [ ] **Mason's Rule** : Zéro scaffolding (pas de labels "Section 02", pas de HEX affichés)
- [ ] **Cursor Coherence** : Le niveau d'audace visuelle correspond aux scores A×B
- [ ] Le fichier est self-contained (pas de dépendance externe sauf Google Fonts)
- [ ] Le résultat est visuellement riche et complet — la qualité prime sur la quantité

---

## 8. INTÉGRATION DE VISUELS DE RÉFÉRENCE (optionnel)

Cette section s'applique **uniquement** si l'utilisateur a fourni des photos ou illustrations de référence après la Phase 3. Si aucun visuel n'a été fourni, cette section est ignorée et le Style-Tile est généré en mode typographique/graphique pur.

### Quand

- L'utilisateur a validé les 3 concepts (Phase 3)
- L'orchestrateur a proposé l'option "visuels de référence"
- L'utilisateur a fourni 1-2 images par concept
- Les images ont été analysées, redimensionnées si nécessaire, et encodées en base64

### Philosophie d'intégration

Les visuels sont des éléments **STRUCTURANTS** du triptyque, pas de la décoration. La composition doit **refléter le niveau d'Audace (A)** choisi par l'utilisateur.

### Répertoire de techniques de composition

| Technique | Description | Adapté pour |
|-----------|-------------|-------------|
| **Hero split** | Image en demi-largeur (50/50 ou 60/40) avec gradient de liaison | A ≤ 2 (structuré, efficace) |
| **Full-bleed overlay** | Image en fond 100% avec texte en overlay (blend-modes) | A 2-3 (immersif) |
| **Fragmentation** | Image découpée en plusieurs zones intercalées avec le texte | A = 3 (rupture) |
| **Diagonale** | Image en clip-path diagonal traversant la composition | A = 3 (dynamique) |
| **Masque typographique** | Texte qui "découpe" l'image (mix-blend-mode: difference) | A = 3 (expérimental) |
| **Collage/multi-crops** | Plusieurs crops asymétriques de l'image | A = 3 (éditorial) |
| **Vignette contextuelle** | Petite image dans une carte UI (Artefact Témoin) | Tous niveaux (optionnel) |
| **Fond atmosphérique** | Image en background-image avec overlay 70-90% | Tous niveaux (Atmosphere Block) |

### Guidance par niveau d'Audace

**A = 1 (Prudent)** : Privilégier hero split ou vignette. Compositions classiques et lisibles.

**A = 2 (Décalé)** : Hero split, full-bleed overlay, ou combinaisons créatives. Asymétries contrôlées acceptables.

**A = 3 (Rupture)** : **Le hero split classique est DÉCONSEILLÉ.** Privilégier fragmentation, diagonales, masques typographiques, collages. La composition doit bousculer les conventions tout en restant fonctionnelle.

Le catalogue complet de techniques est disponible pour TOUS les niveaux — un A=1 utilise les mêmes outils qu'un A=3, avec la même exigence de finition. Le curseur A calibre l'AUDACE de composition, pas la qualité de fabrication. Un style-tile qui n'utilise qu'une fraction des techniques disponibles sous-exploite la fabrication.

### Règles CSS obligatoires

```css
/* Cadrage — obligatoire sur toute image intégrée */
img.visual-ref {
    object-fit: cover;
    width: 100%;
    height: 100%;
    display: block;
}

/* Gradient de liaison (Voice Block hero split) */
.hero-split .image-container::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to right, var(--color-primary-dark), transparent);
    /* Inverser la direction si l'image est à gauche */
}

/* Overlay atmosphérique (Atmosphere Block) */
.atmosphere-block {
    position: relative;
    background-image: url('data:image/...');
    background-size: cover;
    background-position: center;
}
.atmosphere-block::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to bottom,
        rgba(var(--color-primary-dark-rgb), 0.85),
        rgba(var(--color-primary-dark-rgb), 0.95)
    );
}

/* Harmonisation chromatique (optionnel) */
img.visual-ref {
    filter: saturate(0.85); /* légère désaturation pour cohérence */
    mix-blend-mode: multiply; /* ou overlay, selon l'effet voulu */
}
```

### Règles de style

- **Pas de `border`** visible sur les images — intégration seamless avec le design
- **`object-fit: cover`** obligatoire — pas de déformation, pas de letterboxing
- **Gradient d'overlay** systématique pour lier l'image au fond du bloc
- **`mix-blend-mode`** autorisé (multiply, overlay) pour harmoniser les tons de l'image avec la palette `:root`
- **`filter`** autorisé pour le color grading (brightness, contrast, saturate, hue-rotate)
- L'image doit **influencer la composition** : le layout s'adapte à sa présence (full-bleed overlay si l'image est forte, stacked si elle est verticalement scénique, split asymétrique si elle est latérale, etc.) — le choix dépend du concept et de la nature de l'image, pas d'un pattern par défaut
- **Vidéo** : si l'utilisateur fournit un fichier vidéo (.mp4/.webm) en remplacement d'une image, les mêmes règles CSS s'appliquent. Le sélecteur cible `img` ET `video` : `.voice-block__hero-image img, .voice-block__hero-image video { ... }`. Attributs obligatoires : `autoplay loop muted playsinline`.

### Encodage

- Format : base64 inline dans `<img src="data:image/{ext};base64,{contenu}">` ou `background-image: url('data:image/...')`
- Le fichier HTML reste **self-contained** (pas de référence à un fichier externe)
- Taille max recommandée : **1200px de large** (redimensionné en amont par l'orchestrateur)
- Formats acceptés : JPEG, PNG, WebP
- **Vidéo** : fichier externe référencé par `<video src="{brand}-video-hero.mp4">` (PAS en base64 — les vidéos sont trop lourdes pour l'inline). Le fichier HTML n'est plus 100% self-contained quand une vidéo est présente — le .mp4 doit être dans le même dossier.

### Ce que les visuels ne sont PAS

- Pas de la décoration ou du remplissage
- Pas des éléments plaqués sur un design existant — le design NAÎT du dialogue entre le visuel et les specs
- L'image-pivot du style-tile (encodée base64 dans le triptyque) n'est pas propagée aux Batches 2 et 3 — ceux-ci héritent du `:root`, pas de cette image. **En revanche**, la librairie de visuels finaux dérivés (voir ci-dessous) est, elle, consommée par Batch 2 et Batch 3.

### Librairie de visuels finaux dérivés (Batch 2 cover + Batch 3)

Depuis 2026-05-12, une session BIG peut contenir une **librairie de visuels finaux dérivés** (générés hors pipeline par `/visual-prompt` / `/nano-banana-edit`), rangée dans `outputs/{brand}-{session}/visual-final/` avec le naming `{brand}-c{N}-{paletteID}-{type}[-{variante}].{ext}`. 7 types : `hero` · `animation` (HTML autoporteur) · `atmosphere` (4 niveaux d'intensité : `uniforme` → `parchemin` → `doux` → `dramatique`) · `closeup` · `macro` · `pov` · `schema` (diagramme vectoriel, registre « papier scientifique »).

**Si cette librairie existe pour le concept retenu** (l'orchestrateur la détecte en Phase 6A, "Inventaire des visuels finaux dérivés") :

- **Batch 2** : **ne consomme plus** la librairie depuis l'amendement D54 du 2026-05-14. La cover band éditoriale initialement prévue a été retirée (jugée « pas belle » à l'usage). Le Batch 2 ouvre désormais par un kicker sobre « Volume II · Système de Signes » (overline éditorial discret) → chapitre 05, format aligné sur l'ouverture du Batch 3.
- **Batch 3 — chapitre 08** affiche les visuels `hero`/`pov`/`animation`/`atmosphere`/`closeup`/`macro` réels : `atmosphere`/`macro` → 08.1 (moodboard) + 08.2 (les niveaux d'intensité sont la démonstration littérale du color grading) ; `hero`/`pov`/`animation` → 08.3 (scénographie) ; `closeup` → 08.1. Ces images **remplacent** les cartes CSS qui ne feraient que « décrire » une ambiance.
- **Batch 3 — chapitre 10** affiche les `schema` en contexte d'usage (illustration d'un propos), pas isolés.

**Embedding** : par **chemin relatif** (`<img src="visual-final/…">`, `<iframe src="visual-final/…animation.html" loading="lazy">`), JAMAIS en base64 (trop lourd à 4-6 images). Conséquence : le fichier Batch 3 (s'il a des visuels) n'est plus 100 % self-contained — le dossier `visual-final/` fait partie du livrable Batch 3 et l'accompagne (même logique que les vidéos). Le Batch 2 reste self-contained. Règles CSS sur les `<img>` : voir les "Règles CSS obligatoires" et "Règles de style" du §8 (`object-fit: cover`, pas de `border`, overlay gradient, `filter` autorisé pour l'harmonisation chromatique). Les `.html` d'animation sont autoportants — ne pas les modifier.

**Si la librairie n'existe pas** : Batch 3 est inchangé (moodboard CSS au lieu d'images réelles). Le Batch 2 a le même format dans tous les cas depuis l'amendement (kicker sobre).

---

## 9. CONCEPT NAME DISPLAY

### Règle
Le nom du concept DOIT être visible dans chaque livrable HTML, à deux endroits :

1. **`<title>`** : Inclure le nom du concept dans le tag `<title>` du document
2. **Footer tagline** : Le footer/colophon de chaque fichier HTML affiche le nom du concept

### Par livrable

| Livrable | `<title>` | Footer |
|----------|-----------|--------|
| Style-Tile | `{Brand} — Style-Tile — {Concept Name}` | `{Brand} — {Concept Name}` |
| Batch 2 | `{Brand} — Système de Signes — {Concept Name}` | `Système de Signes — {Concept Name}` |
| Batch 3 | `{Brand} — Narration & Espace — {Concept Name}` | `Narration & Espace — {Concept Name}` |
| Landing | `{Brand} — {Concept Name}` | Nom du concept dans `.footer__brand-desc` ou équivalent |

### Mode D (Brand Existante)
En mode D, il n'y a pas de concept — le nom de la marque seul suffit. Omettre le nom du concept du `<title>` et du footer.
