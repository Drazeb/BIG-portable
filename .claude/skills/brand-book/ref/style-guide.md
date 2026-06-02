# Style Guide — Règles formelles transverses du brand book

Ce document fixe les **règles formelles** qui s'appliquent à **toutes les sections** du brand book. Pour la rédaction des sections textuelles (01, 02, 06), voir aussi `editorial-patterns.md`. Pour la structure de chaque section, voir `structure.md`.

---

## 1. Layout global

### Single-column max-width
- **Max-width** : `1280-1400px` selon largeur de la marque. Par défaut : **1320px**.
- **Padding inline** : `clamp(24px, 5vw, 80px)` (responsive)
- **Padding vertical** par section : `clamp(80px, 12vh, 160px)` haut et bas
- **Centrage** : `margin-inline: auto;`
- Le **fond plein écran** (`background-color` ou `background-image`) déborde à 100vw via un wrapper externe, le contenu reste contenu dans la max-width.

```css
.section {
  width: 100%;
  padding-block: clamp(80px, 12vh, 160px);
  padding-inline: clamp(24px, 5vw, 80px);
}
.section__inner {
  max-width: 1320px;
  margin-inline: auto;
}
```

### Pas de grille 12-col
- Le brand book est un **document éditorial**, pas une landing page.
- Utiliser `display: flex` ou `display: grid` ponctuellement (pour les sous-blocs en grille documentaire de la section 07, ou les 2-cols Do/Don't de la section 06).
- Pas de framework grid genre Bootstrap.

---

## 2. Slide rythm — Hauteur prédictible

### Règle d'or
Chaque section a une **hauteur prédictible**, généralement **720-900px** sur desktop. Le scroll = défilement de "pages" éditoriales, pas une masse continue informe.

### Implémentation
- Utiliser `min-height: clamp(720px, 90vh, 900px)` sur chaque section
- Pour les sections fullbleed (cover, closing) : `min-height: 100vh; min-height: 100svh;`
- Pour la section 04 PALETTE en mode immersif : chaque "page" couleur a `min-height: 600px`

### Exceptions assumées
- **Section 08 WEB** : la capture PNG du style-tile est longue, la section peut atteindre 1200-2000px. C'est volontaire.
- **Section 07 SYSTEM** : 4 sous-blocs cumulés, peut atteindre 2400-3200px. C'est volontaire.
- **Section 04 PALETTE** : 9 "pages" couleur × 600-720px = 5400-6480px de hauteur cumulée. C'est volontaire (mode immersif assumé).

### Ratio cible
Sur desktop 1440×900, l'idéal est qu'une section "standard" tienne entre **0.8 et 1.0 fois la hauteur du viewport**.

---

## 3. Mode chromatique mixte

Le brand book alterne **trois modes** selon la section :

| Mode | Sections | Fond |
|------|----------|------|
| **Dark Cinema natif** | COVER, CLOSING, section 09 PHOTO | surface sombre dominante de la marque (ou équivalent dark de la palette) |
| **Positif** | 01 BIG IDEA, 02 CONCEPT, 03 IDENTITY, 04 PALETTE (wrapper), 05 TYPO, 06 VOICE | surface claire dominante ou équivalent clair de la palette |
| **Positif wrapper + îlots dark** | 07 SYSTEM, 08 WEB | Fond positif, mais les composants/captures sont en îlots dark canoniques |

### Application

```css
.section--positive {
  background-color: var(--brand-color-positive-bg); /* surface claire dominante */
  color: var(--brand-color-positive-text);
}

.section--dark-cinema {
  background-color: var(--brand-color-dark-bg); /* surface sombre dominante */
  color: var(--brand-color-dark-text);
}

.section--positive .island--dark {
  background-color: var(--brand-color-dark-bg);
  color: var(--brand-color-dark-text);
  border-radius: var(--brand-radius-xs);
  padding: clamp(24px, 4vw, 48px);
}
```

### Pour la section 08 WEB
Le wrapper est positif (fond clair), mais le **fond derrière l'image PNG** est un **gradient palette asymétrique** :

```css
.section--web .image-stage {
  background: radial-gradient(
    ellipse at 28% 35%,
    var(--brand-color-accent-1) 0%,
    var(--brand-color-accent-2) 40%,
    var(--brand-color-positive-bg) 80%
  );
  padding: clamp(40px, 8vh, 120px);
}
```

---

## 4. Mode immersif vs grille documentaire

### Atomes esthétiques → MODE IMMERSIF COMPOSÉ (1 page entière)
- **Sections concernées** : 04 PALETTE, 05 TYPOGRAPHIE, 06 VOICE
- **Principe correct** : **TOUS les items composés sur 1 SEULE page**, pas 1 page par item.
- **Format Solara/Agenie/MachineX vérifié** :
  - Palette : 4 à 11 grands rectangles de couleur **côte à côte sur 1 page**
  - Typo : Display + Body + Pairing + Type Scale **composés sur 1 page**
  - Voice : Pull-quote + descriptors + Do/Don't **composés sur 1 page**
- **Erreur à éviter** : ne pas faire "1 couleur = 1 page" (sur-immersion qui casse le slide rythm). Aucun benchmark sérieux ne fait ça.
- **Hauteur cible** : ~720-900px (1 slide), comme toute autre section éditoriale.

### Composants/système → MODE GRILLE DOCUMENTAIRE
- **Sections concernées** : 03 IDENTITY (lockups), 07 SYSTEM (icônes, UI, charts, composition), 09 PHOTO (cadrages canoniques)
- **Principe** : tous les items côte à côte sur une même page, pour permettre la **comparaison** et la **lecture documentaire**.
- **Format** : grille 2×N ou 3×N ou 4×N selon largeur. Chaque cellule a une vignette + un titre + une mini-description.

### Pourquoi cette dualité ?
Les **atomes esthétiques** sont des artefacts d'expérience (une couleur, c'est une émotion). Les **composants** sont des artefacts d'usage (un bouton, c'est un outil). Présenter une couleur dans une mini-vignette c'est trahir sa fonction émotionnelle. Présenter 12 boutons un par page c'est trahir leur fonction documentaire.

---

## 4bis. Hiérarchie typographique homogène — FIGÉE

**Règle absolue** : les tailles de titres ne varient PAS d'une section à l'autre. La hiérarchie est définie UNE fois en variables CSS et utilisée partout via classes utilitaires.

### Variables CSS de hiérarchie (à inclure dans `:root`)

```css
:root {
  /* Eyebrow — numéro + nom section (ex: "01 — BIG IDEA") */
  --type-eyebrow-size: 12px;
  --type-eyebrow-letter-spacing: 0.14em;
  --type-eyebrow-weight: 500;
  --type-eyebrow-text-transform: uppercase;
  --type-eyebrow-color: var(--brand-color-accent); /* accent primaire ou équivalent */

  /* Section title — grand H2 de la section (ex: "Le phare immobile") */
  --type-section-title-size: clamp(40px, 5vw, 64px);
  --type-section-title-line-height: 1.05;
  --type-section-title-letter-spacing: -0.02em;
  --type-section-title-weight: 400;
  --type-section-title-family: var(--brand-display);

  /* Section subtitle — sous-titre italique sous le titre (ex: "dans la matière qui tourbillonne.") */
  --type-section-subtitle-size: clamp(20px, 2.4vw, 32px);
  --type-section-subtitle-line-height: 1.3;
  --type-section-subtitle-style: italic;
  --type-section-subtitle-color: var(--brand-color-accent);

  /* Body — paragraphe courant */
  --type-body-size: clamp(16px, 1.2vw, 18px);
  --type-body-line-height: 1.6;
  --type-body-weight: 400;
  --type-body-family: var(--brand-body);

  /* Caption — légende sous une image, métadonnée, attribution */
  --type-caption-size: 13px;
  --type-caption-line-height: 1.5;
  --type-caption-weight: 400;
  --type-caption-color: var(--brand-color-text-secondary);

  /* Pull-quote — citation géante section Voice */
  --type-pull-quote-size: clamp(40px, 4vw, 64px);
  --type-pull-quote-line-height: 1.2;
  --type-pull-quote-style: italic;

  /* Big number — chiffre dominant (KPI dataviz, page numéro slide, etc.) */
  --type-big-number-size: clamp(56px, 7vw, 96px);
  --type-big-number-line-height: 0.9;
  --type-big-number-family: var(--brand-display);

  /* Mono — codes, HEX, oklch, métadonnées techniques */
  --type-mono-size: 13px;
  --type-mono-family: 'JetBrains Mono', ui-monospace, monospace;
  --type-mono-letter-spacing: 0.02em;
}
```

### Classes utilitaires (à inclure dans le template-base.html)

```css
.eyebrow {
  font-family: var(--brand-body);
  font-size: var(--type-eyebrow-size);
  font-weight: var(--type-eyebrow-weight);
  letter-spacing: var(--type-eyebrow-letter-spacing);
  text-transform: var(--type-eyebrow-text-transform);
  color: var(--type-eyebrow-color);
}

.section-title {
  font-family: var(--type-section-title-family);
  font-size: var(--type-section-title-size);
  font-weight: var(--type-section-title-weight);
  line-height: var(--type-section-title-line-height);
  letter-spacing: var(--type-section-title-letter-spacing);
  text-wrap: balance;
}

.section-subtitle {
  font-family: var(--brand-display);
  font-size: var(--type-section-subtitle-size);
  font-style: var(--type-section-subtitle-style);
  line-height: var(--type-section-subtitle-line-height);
  color: var(--type-section-subtitle-color);
}

.body-text {
  font-family: var(--type-body-family);
  font-size: var(--type-body-size);
  font-weight: var(--type-body-weight);
  line-height: var(--type-body-line-height);
}

.caption {
  font-family: var(--brand-body);
  font-size: var(--type-caption-size);
  line-height: var(--type-caption-line-height);
  color: var(--type-caption-color);
}

.pull-quote {
  font-family: var(--brand-display);
  font-size: var(--type-pull-quote-size);
  font-style: var(--type-pull-quote-style);
  line-height: var(--type-pull-quote-line-height);
  text-wrap: balance;
}

.big-number {
  font-family: var(--type-big-number-family);
  font-size: var(--type-big-number-size);
  line-height: var(--type-big-number-line-height);
}

.mono {
  font-family: var(--type-mono-family);
  font-size: var(--type-mono-size);
  letter-spacing: var(--type-mono-letter-spacing);
}
```

### Règles d'usage

- **Jamais de tailles inline** (`style="font-size: 48px"`). Toujours via classe utilitaire.
- **Chaque section** ouvre par : `eyebrow` (numéro + nom section) → `section-title` (titre court) → optionnel `section-subtitle` (italique accent) → corps (`body-text`).
- **La taille du titre de section est la MÊME** sur toutes les sections (sauf cover et closing qui ont leur propre dimensionnement).
- **Pas de "page title" géant en H1** sur certaines sections et "petit titre" sur d'autres. **Homogénéité stricte**.
- **Variation tolérée** uniquement pour : pull-quote (section Voice — `--type-pull-quote-size`), wordmark cover et closing (taille libre), spécimens "Aa" (section Typo — composition immersive).

---

## 5. Tokens canoniques de la marque

### Extraction obligatoire depuis le style-tile
Le brand book DOIT extraire les tokens depuis le bloc `:root` du `{brand}-style-tile.html` et les utiliser tels quels. JAMAIS de valeurs génériques.

Tokens à extraire systématiquement :

```css
:root {
  /* Palette — toujours en oklch() */
  --brand-color-primary: oklch(...);
  --brand-color-secondary: oklch(...);
  --brand-color-accent: oklch(...);
  --brand-color-positive-bg: oklch(...);  /* surface claire dominante */
  --brand-color-positive-text: oklch(...);
  --brand-color-dark-bg: oklch(...);      /* surface sombre dominante */
  --brand-color-dark-text: oklch(...);
  --brand-color-success: oklch(...);
  --brand-color-warning: oklch(...);
  /* ... 9 couleurs minimum */

  /* Fonts — exactement celles du style-tile */
  --brand-display: 'Gloock', serif;       /* ou autre selon marque */
  --brand-body: 'Inter', sans-serif;      /* ou autre selon marque */

  /* Radius */
  --brand-radius-xs: 2px;                 /* canonique BIG */
  --brand-radius-sm: 4px;
  --brand-radius-md: 8px;
  --brand-radius-lg: 16px;

  /* Wordmark accent */
  --brand-wordmark-accent: var(--brand-color-accent);
}
```

### Wordmark canonique
**Format** : `{brand}.` (nom de marque + point final).
- Le **point final** est en `color: var(--brand-wordmark-accent)`.
- Le reste du wordmark est en `color: var(--brand-color-positive-text)` ou `--brand-color-dark-text` selon le fond.
- En `--brand-display`.

### Pourquoi `--radius-xs: 2px` ?
C'est le radius canonique BIG dans la quasi-totalité des cas. Si la marque l'a changé (ex: 0px ou 999px pour un look spécifique), respecter le choix de la marque.

---

## 6. Couleurs interdites

### Pas de pur noir #000 ni pur blanc #FFF
- Le pur noir et le pur blanc sont **bannis** car ils écrasent la palette de la marque.
- Utiliser la surface sombre dominante (`--brand-color-dark-bg`) à la place de `#000`.
- Utiliser la surface claire dominante (`--brand-color-positive-bg`) à la place de `#FFF`.

### Si la marque n'a pas explicité ces tokens
Dériver depuis la palette principale :
- surface sombre dominante ≈ `oklch(0.18 0.04 270)` (sombre, légèrement teinté de la couleur primaire)
- surface claire dominante ≈ `oklch(0.97 0.005 90)` (clair chaud, jamais blanc cassé glacial)

---

## 7. Shadows et halos

### Pas de `box-shadow: 0 0 Npx`
- Interdit : `box-shadow: 0 0 24px rgba(...)` — c'est une lueur centrée, sans matérialité.
- Toujours **direction** : `box-shadow: 0 8px 24px -4px rgba(...)` — lumière vient d'en haut, ombre tombe en bas-droite.

```css
/* Ombre canonique pour image-stage section 08 */
.image-stage img {
  box-shadow:
    0 16px 32px -8px oklch(0.2 0.08 270 / 0.18),
    0 4px 8px -2px oklch(0.2 0.08 270 / 0.12);
}
```

### Halos radial-gradient asymétriques
- Interdit : `radial-gradient(circle at 50% 50%, ...)` — centré, statique.
- Toujours **asymétrique** : `radial-gradient(ellipse at 28% 35%, ...)` ou autre position non centrée.
- Idéal pour les fonds de section 04 PALETTE (sub-pages) et section 08 WEB.

---

## 8. Anti-patterns (clichés à éviter)

| Anti-pattern | Pourquoi | À la place |
|--------------|----------|------------|
| Statement-poster gigantesque pour Big Idea | Cliché Behance daté, manque d'éditorial | Format éditorial minimaliste (voir `editorial-patterns.md`) |
| Méta-fields en grille (Type / Date / Client) | Style-frame de présentation agence, pas brand book | Pas de méta — info dans le caption ou pas du tout |
| Palette en grille 3×3 swatches ronds | Stock photoshop preset, manque de soul | Mode immersif : 1 couleur = 1 page |
| Iframe pour la web | Scaling/scroll insolubles | PNG full-page capturé via Playwright |
| Mockup de smartphone Apple sur fond gradient | Cliché Dribbble | Si mockup nécessaire, utiliser un "cadre" abstrait neutre |
| Triple ombre portée empilée sur tout | "Glassmorphism" daté | Une seule ombre directionnelle propre |
| Gradients arc-en-ciel pop multicolore | Slop AI-générique | Gradients 2-3 couleurs de la palette, asymétriques |
| Fontes Roboto / Open Sans / Lato | Génériques sans personnalité | Utiliser les fonts définies par la marque |
| Texte centré sur de longs paragraphes | Illisible, slop poster | Aligné à gauche, colonne 55ch |
| Emojis dans le brand book | Pas pro | Pas d'emoji |
| Citation avec guillemets gigantesques en couleur fluo | Tumblr 2014 | Citation propre, sobre, sans décoratif |

### 8bis. Règle "Contraste minimum de séparation" — SANCTUARISÉE 27 mai 2026

Tout bloc visible (card, tuile, panneau, container) doit être **chromatiquement distinct** de son conteneur parent. C'est une règle universelle qui s'applique à :
- Les cellules du bento Identity Card (`.bv4-*`)
- Les diptyques sociaux (`.s08c-cell--*`)
- Les îlots dark dans une section positive (`.island--dark`)
- Tout `<figure>`, `<article>`, `.card`, `.chart-card`, etc.

**Différence minimum requise** entre fond enfant et fond parent :
- Lightness ≥ 8-10 points d'écart en oklch, OU
- Hue différent (au moins une différence de 30°), OU
- Chroma ≥ 0.02 d'écart

**RÈGLE CRITIQUE — Palette only stricte** : la couleur de contraste DOIT obligatoirement être une couleur de la palette canonique de la marque, accessible via une variable `var(--color-*)` ou `var(--brand-color-*)` définie dans le `:root`. **AUCUNE COULEUR INVENTÉE n'est tolérée**, même si elle "matche le ton". C'est PIRE qu'un manque de contraste : ça pollue l'identité chromatique avec une 7e/8e couleur qui n'existe pas dans le brand. Charles 27/05/26 : "il est allé chercher une couleur qui n'est pas dans la palette. C'est interdit. C'est pire que tout."

**Cas concret de violation à NE PAS reproduire** : utiliser `oklch(0.92 0.025 78)` (beige clair chaud inventé) sur les cards manifesto/typo du bento Identity Card parce qu'on cherchait un contraste avec la Brume du body. Solution correcte : basculer sur une couleur palette sombre (Marine Cliff, Nuit Claire, Abyss) avec texte clair. Le bento accepte d'avoir 70% de cases sombres si c'est ce que la palette propose.

**Anti-pattern interdit** : `background: var(--brand-color-positive-bg)` (ou `--color-mist`, ou n'importe quel token équivalent) sur un bloc enfant d'un conteneur qui a déjà ce même fond. Résultat = bloc invisible, "ce n'est plus un bento".

**Stratégies de contraste — uniquement parmi les couleurs de la palette** :
- Si fond parent = couleur claire (Brume, Encre de Veille…) → fond enfant = couleur sombre de la palette (Nuit, Nuit Claire, Marine Cliff)
- Si fond parent = couleur sombre → fond enfant = couleur claire ou accent (Foyer, Foyer Chaud)
- Si la palette ne propose AUCUNE teinte créant un contraste suffisant : on accepte que le bloc n'ait pas de séparation chromatique forte et on s'appuie sur l'ombre directionnelle + commentaire HTML d'intention.

**Exception "spécimen sur fond natif"** : quand on documente intentionnellement l'élément sur sa couleur d'usage réelle (ex: lockup brand affiché sur Brume parce qu'on veut montrer "voilà comment le lockup s'imprime sur Brume" — c'est le cas de la section 04 Identité). Dans ce cas :
- Bordure 1px subtile `rgba(...)` autorisée pour délimiter
- **Obligatoire** : commentaire HTML `<!-- mode spécimen : fond natif d'usage -->` juste avant la balise pour signaler l'intention au mainteneur
- La bordure 1px reste discrète (opacity ≤ 0.15 pour ne pas attirer l'œil)

**Cas pratiques de respect de la règle** (référence pour les futures marques) :
- Bento Identity Card manifesto : `var(--color-marine-cliff)` avec texte blanc (couleur palette sombre, contraste 60+ points oklch vs Brume body)
- Bento Identity Card typo : `var(--color-mist-cool)` (Encre de Veille, clair distinct de Brume body, alternance avec les cards sombres)
- Section 04 Identité — lockup `--brand-logo` sur fond `--brand-color-positive-bg` : EXCEPTION spécimen, bordure 1px subtile autorisée avec commentaire

### 8ter. Règle spécifique BENTO Identity Card — alternance dark/light obligatoire — SANCTUARISÉE 27 mai 2026

Le bento de la section 00 Identity Card doit respecter une **alternance chromatique** entre ses 7 cards pour éviter à la fois la monotonie sombre (toutes les cards en Marine Cliff/Nuit/Abyss) et la fadeur claire (toutes en Brume/Mist-cool).

**Distribution cible** pour les 7 cards (proportions indicatives) :
- **2-3 cards sombres** (palette dark : Abyss, Nuit Claire, Marine Cliff) → cover hero, wordmark, dataviz, ou manifesto selon focal éditorial
- **2-3 cards claires** (palette light : Mist-cool / Encre de Veille pour les claires douces ; Foyer / Foyer Chaud pour les claires warm)
- **1 card mixte** (palette grille 6 couleurs = sombre + clair)

**Anti-pattern à éviter** : bento où 5+ cards sur 7 sont en couleur sombre → atmosphère trop "nocturne uniforme" qui perd la respiration éditoriale. Charles 27/05/26 : "il devient pas très beau, là tu as que du dark."

**Règles annexes** :
- Aucune card ne doit avoir la même couleur que le fond body (`--brand-color-positive-bg`) — sinon elle disparaît
- Toutes les couleurs DOIVENT venir de la palette canonique (`var(--color-*)`) — voir §8bis
- L'alternance n'est pas géométrique stricte mais doit créer un rythme visuel évident au premier regard

**Référence Camille v4 (sanctuarisée)** :
- Cover (sombre painterly), Manifesto (Marine Cliff sombre), Wordmark (Abyss sombre), Dataviz (Abyss sombre) = 4 sombres
- Icônes (Foyer orange clair-warm), Typo (Mist-cool / Encre de Veille clair froid) = 2 claires
- Palette (6 couleurs mixtes) = 1 mixte
- Total : alternance équilibrée, atmosphère "phare dans la nuit" qui respire

### 8quater. Règle "Fidélité au pack source" — MÉCANIQUE EXTRACT-THEN-INJECT v5 (SANCTUARISÉE 30 mai 2026)

**Mécanique automatisée prévalente** : pour les sous-sections **07a Iconographie**, **07b Composants UI**, **07c Data viz** du Système (id="system" dans `template-base.html`), la fidélité au pack source est désormais **MÉCANIQUE** :

1. **Étape 2.5 du workflow** (SKILL.md) exécute le script `scripts/extract-batch2-inventory.py` qui extrait **verbatim** depuis `{brand}-batch2.html` les 10 catégories de composants suivantes vers `{brand}-batch2-inventory.html` :
   - `icons` (wrappers `.glyph`, `.icon-card`, `.icon-cell`, `.icon-tile`, `.stroke-step`, `.abstraction-step`, `.business-icon`, …)
   - `buttons` (`<button class="btn[ --variant]">`, hors `.tab`)
   - `inputs` (wrappers `.field`, `.form-field`, `.input`, `.select`, `.input-wrap`)
   - `badges`, `toggles`, `checkboxes`, `cards` (whitelist), `tabs`, `alerts`, `progress`, `charts`

2. Chaque bloc HTML extrait est borné par `<!-- BEGIN_BLOCK md5=<hash> -->` / `<!-- END_BLOCK -->`. Les `<defs>` SVG référencés via `url(#…)` sont **injectées inline** dans chaque SVG → chaque bloc est autonome.

3. **Étape 4** (génération HTML brand book) : le sub-agent copie VERBATIM ces blocs dans les slots `{{BATCH2_INVENTORY_*}}` du template. **Aucune redessination autorisée.** Le sub-agent compose UNIQUEMENT les wrappers HTML (grilles, headers, captions, eyebrows) AUTOUR des blocs. Il peut ajouter des `<span class="bk-mono">{label}</span>` à partir de `data-label` sur l'`<article>`.

4. **Étape 5** (quality gate) : `scripts/verify-md5-fidelity.py` lit le manifest JSON + le brand book final, vérifie que CHAQUE hash MD5 attendu est présent ET que le contenu re-hashé match. Un seul caractère altéré → `[FAIL]` → la sous-section concernée est régénérée.

**Ce que cette mécanique garantit** :
- 0 redessination de composant (anti-pattern Atelier Vermeil 30/05/2026 : 28 SVG `viewBox 64×64` avec hachures `url(#hatch-cross)` redessinés en 20 SVG `32×32` plats `currentColor` → **impossible** avec extract-then-inject).
- 0 simplification quantitative (si batch2 a 24 icônes, brand book a 24 icônes).
- 0 invention de variantes ou états (le sub-agent n'a accès qu'aux blocs verbatim).

**Liberté préservée du sub-agent** : composition des wrappers (grilles, colonnes, fonds, padding), rédaction des eyebrows / titres / captions, ordre d'affichage des blocs dans la grille.

**Périmètre hors mécanique** :
- **07d Composition** : pas d'extract automatique. La grille canonique est déduite de `design-specs.md` et générée librement par le sub-agent.
- **Bento Identity Card (intro 00)** : reste à la charge du sub-agent (n'est pas dans batch2).

**Garde-fou conceptuel résiduel** : la formulation textuelle ci-dessous reste comme rappel philosophique mais devient **subordonnée** à la mécanique. En cas de désaccord (nouveau type de composant non couvert), priorité à la mécanique : ajouter une nouvelle catégorie dans `extract-batch2-inventory.py` avant tout.

---

#### Formulation textuelle historique (garde-fou conceptuel — subordonnée à la mécanique ci-dessus)

Pour les sous-sections **07a Iconographie**, **07b Composants UI**, **07c Data viz**, **07d Composition**, le brand book doit présenter **TOUS les éléments documentés dans le pack source** (`batch2.html`, `batch3.html`), sans simplification ni réduction quantitative.

**Anti-pattern interdit** : "j'ai mis quelques exemples représentatifs" → NON. Le brand book doit refléter la **vraie densité** du système conçu par BIG. Sous-représenter dilue la valeur perçue du pack identité. Charles 27/05/26 : "tu n'en mets pas beaucoup dans le brand book… pareil pour la dataviz."

**Exception** : si batch2 contient deux versions contradictoires d'un même élément, prendre la dernière version chronologique ou la plus complète.

**Inventaire-type pour chaque section 07** :
| Section | Inventaire batch2 attendu |
|---------|--------------------------|
| 07a Iconographie | Toutes les icônes métier de la `Grammaire Iconique` + `DA illustrative · icônes métier` + les 3 grammaires (Outline / Solid / Duotone) |
| 07b Composants UI | TOUS les états de chaque composant (Buttons : Default/Hover/Active/Disabled × Primary/Secondary ; Form Elements : input + focus + error + toggle + checkbox/radio si présents ; Badges : toutes les variantes ; Cards : tous les containments ; Feedback/Navigation : tous les patterns) |
| 07c Data viz | TOUS les charts canoniques (Line + Bar + Donut + Échantillon grille si présent + tout autre type) |
| 07d Composition | TOUTES les grilles canoniques documentées (12-col / 8-col / hero asymétrique / etc.) |

**Note Camille v3 (legacy accepté)** : le brand book Camille v3 actuel ne respecte pas pleinement cette règle (composants UI sous-représentés : 3 boutons au lieu de 8, pas de toggle). C'est un legacy d'avant la mécanique v5. Pour les futures marques (Atelier Vermeil et au-delà), la mécanique extract-then-inject s'applique strictement.

---

## 9. Animation / interaction

### Sobriété volontaire
La v1 du brand book est **statique**. Pas de scroll-jacking, pas d'animation au scroll, pas de parallax.

Raison : un brand book est un **document de référence**, pas une démo. L'utilisateur le parcourt à son rythme.

### Exceptions tolérées
- **Smooth-scroll** sur les liens du sommaire (`scroll-behavior: smooth;`)
- **Hover discret** sur les visuels finaux (légère élévation ou caption qui apparaît)
- **Lightbox** pour la capture PNG de la section 08 (clic = ouvre l'image en grand) — facultatif v1

### Interdit
- Pas de GSAP, pas de Lenis, pas de ScrollTrigger
- Pas de cursor custom
- Pas de loader d'intro
- Pas de hero animé (la cover est statique, c'est une couverture de livre)

---

## 10. Accessibilité minimum

- Contraste AA minimum sur tous les textes (WCAG)
- Tailles fluides avec `clamp()` (jamais en `px` fixes pour les textes principaux)
- Images avec `alt` descriptif (sauf décoratifs : `alt=""`)
- Pas de couleur seule pour véhiculer une info (Do/Don't doivent avoir un label texte, pas juste vert/rouge)

---

## 11. Responsive

### Cible
- **Desktop principal** : 1280-1920px (le brand book est conçu pour être consulté sur desktop)
- **Tablet** : 768-1279px → max-width réduit, grilles passent en 2-col, padding réduit
- **Mobile** : <768px → tout passe en single-column, grilles deviennent stack vertical

### Breakpoints
```css
/* Mobile-first n'est PAS pertinent ici (brand book = desktop document) */
/* Donc on part desktop et on dégrade */

@media (max-width: 1024px) {
  /* Tablet */
}

@media (max-width: 640px) {
  /* Mobile */
}
```

### Section 04 PALETTE en mobile
Le mode immersif reste : 1 couleur = 1 page, mais le grand bloc passe en pleine largeur stack au-dessus des métadonnées.

---

## 12. Don'ts spécifiques à la marque

**Toujours consulter** le `{brand}-design-specs.md` §12 (ou équivalent "Don'ts" / "Anti-patterns") avant de finaliser une section. Chaque marque a ses interdictions propres (ex: pour Camille peut-être "pas de soleils ronds graphiques", pour VoltaPilot peut-être "pas de prises électriques stylisées").

Ces don'ts s'ajoutent à la liste universelle de la section 8 ci-dessus.
