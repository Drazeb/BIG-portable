# Catalogue — Patterns de Composition avec Images

6 patterns CSS pour intégrer des images dans les style-tiles.
Chaque pattern est calibré par curseur A (niveau d'audace).

**Règle absolue** : image posée en bandeau rectangulaire = JAMAIS acceptable.
Un `<div>` avec `border-radius` + `object-fit: cover` sans aucune interaction visuelle avec le layout est un NON.

**Note `data-visual`** : chaque `<img>` porte un attribut `data-visual="c{concept}-{n}"` utilisé pour le swap haute résolution en post-traitement. Ne JAMAIS supprimer, renommer ou modifier cet attribut.

---

## Pattern 1 — Split asymétrique avec gradient de liaison

**Curseur A** : ≥ 1 (tous niveaux)
**Quand l'utiliser** : image portrait ou paysage avec un sujet décentré. Idéal pour hero blocks et voice blocks.

```
┌──────────────────────────────────────────┐
│                                          │
│   ┌─────────────┬───────────────────┐    │
│   │             │                   │    │
│   │   TEXTE     │░░░░ IMAGE ░░░░░░░│    │
│   │   (55%)     │░░░░ (45%) ░░░░░░░│    │
│   │             │  gradient →→→     │    │
│   │             │  fond section     │    │
│   └─────────────┴───────────────────┘    │
│                                          │
└──────────────────────────────────────────┘
```

Le gradient `::after` fond l'image dans la couleur de fond de la section — pas de bord net.

```css
.split-hero {
  display: grid;
  grid-template-columns: 55fr 45fr;
  align-items: center;
  min-block-size: 100vh;
  overflow: hidden;
}

.split-hero__content {
  padding-inline: var(--space-2xl);
}

.split-hero__visual {
  position: relative;
  block-size: 100%;
}

.split-hero__visual img {
  display: block;
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
}

/* Gradient de liaison — fond l'image vers la couleur de fond */
.split-hero__visual::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to right,
    var(--color-surface) 0%,
    oklch(0% 0 0 / 0) 40%
  );
  pointer-events: none;
}
```

---

## Pattern 2 — Image en fond avec mask-image

**Curseur A** : ≥ 1 (tous niveaux)
**Quand l'utiliser** : image atmosphérique (paysage, texture, ambiance). Parfait pour atmosphere blocks et sections de mood.

```
┌──────────────────────────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ░░░░░ IMAGE EN FOND (opacity basse) ░░░ │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ░░░░░░ mask-image : fondu vertical ░░░░ │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│                                          │
│         TEXTE AU PREMIER PLAN            │
│         (z-index supérieur)              │
│                                          │
│                    ░░░ fondu ░░░░        │
│                         transparent      │
└──────────────────────────────────────────┘
```

L'image est positionnée en absolute derrière le contenu, avec un `mask-image` qui la fait disparaître progressivement.

```css
.masked-bg {
  position: relative;
  overflow: hidden;
  isolation: isolate;
}

.masked-bg img {
  position: absolute;
  inset: 0;
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
  opacity: 0.25;
  mask-image: linear-gradient(
    to bottom,
    black 30%,
    transparent 80%
  );
  z-index: -1;
}

.masked-bg__content {
  position: relative;
  z-index: 1;
  padding: var(--space-2xl);
}
```

---

## Pattern 3 — Clip-path conceptuel

**Curseur A** : ≥ 2
**Quand l'utiliser** : image forte avec un sujet bien identifiable. Le clip-path DOIT refléter le concept de la marque (angulaire = tech/précision, organique = nature/humain, géométrique = structure/confiance).

```
┌──────────────────────────────────────────┐
│                                          │
│         ╱‾‾‾‾‾‾‾‾‾‾‾‾‾‾╲                │
│        ╱░░░░░░░░░░░░░░░░░╲               │
│       │░░░░░ IMAGE ░░░░░░░│              │
│       │░░░ clip-path ░░░░░│              │
│        ╲░░░ conceptuel ░░╱               │
│         ╲______________╱                 │
│                                          │
│              TEXTE                       │
│                                          │
└──────────────────────────────────────────┘
```

La forme du clip-path est un choix narratif, pas décoratif.

```css
.clipped-visual {
  position: relative;
  display: grid;
  place-items: center;
  padding: var(--space-2xl);
}

.clipped-visual img {
  inline-size: min(500px, 80%);
  aspect-ratio: 4 / 3;
  object-fit: cover;
  /* Exemple : forme angulaire (tech/précision) */
  clip-path: polygon(
    10% 0%, 100% 0%, 90% 100%, 0% 100%
  );
  transition: clip-path 0.6s var(--ease-out-expo);
}

/* Micro-animation hover — la forme respire */
.clipped-visual img:hover {
  clip-path: polygon(
    5% 2%, 98% 0%, 92% 98%, 2% 100%
  );
}
```

---

## Pattern 4 — Full-bleed avec blend-mode

**Curseur A** : ≥ 2
**Quand l'utiliser** : image avec de la richesse tonale (pas un aplat). L'image couvre toute la section, le blend-mode l'intègre à la palette. Idéal pour atmosphere blocks sombres ou sections immersives.

```
┌──────────────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░░ IMAGE FULL-BLEED ░░░░░░░░░░░░░░░░░░░│
│░░░░ blend-mode: luminosity ░░░░░░░░░░░░░│
│░░░░ opacity: 0.3 ░░░░░░░░░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│                                          │
│          TEXTE EN OVERLAY                │
│          (contraste garanti)             │
│                                          │
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└──────────────────────────────────────────┘
```

```css
.fullbleed-section {
  position: relative;
  overflow: hidden;
  background-color: var(--color-surface-dark);
  isolation: isolate;
}

.fullbleed-section img {
  position: absolute;
  inset: 0;
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
  mix-blend-mode: luminosity; /* ou multiply, overlay selon palette */
  opacity: 0.3;
  z-index: -1;
}

/* Overlay gradient pour garantir la lisibilité du texte */
.fullbleed-section::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    oklch(0% 0 0 / 0.6) 0%,
    oklch(0% 0 0 / 0.3) 50%,
    oklch(0% 0 0 / 0.7) 100%
  );
  z-index: -1;
}

.fullbleed-section__content {
  position: relative;
  z-index: 1;
  padding: var(--space-3xl) var(--space-2xl);
  color: var(--color-text-inverse);
}
```

---

## Pattern 5 — Overflow négatif

**Curseur A** : ≥ 3 (rupture uniquement)
**Quand l'utiliser** : l'image doit casser la grille, déborder de son conteneur, créer une tension visuelle. L'image est un élément perturbateur dans le layout.

```
┌──────────────────────────────────────────┐
│                                          │
│     TEXTE                                │
│                                          │
│              ┌────────────────────┐      │
│              │░░░░░░░░░░░░░░░░░░░│      │
│              │░░░░░ IMAGE ░░░░░░░│──────┤ ← déborde
│              │░░░░░ déborde ░░░░░│      │   du container
│              │░░░░░ du cadre ░░░░│      │
│              └────────────────────┘      │
│         ▲ margin négatif                 │
│         └─ casse la grille               │
└──────────────────────────────────────────┘
```

L'image transgresse les limites — margin négatif, clip-path biseauté, glow.

```css
.overflow-section {
  position: relative;
  padding: var(--space-2xl);
  overflow: visible; /* CRITIQUE — permet le débordement */
}

.overflow-visual {
  position: relative;
  margin-block-start: calc(-1 * var(--space-3xl));
  margin-inline-end: calc(-1 * var(--space-xl));
  z-index: 2;
}

.overflow-visual img {
  display: block;
  inline-size: 120%; /* déborde du conteneur */
  max-inline-size: none;
  aspect-ratio: 16 / 10;
  object-fit: cover;
  clip-path: polygon(
    5% 0%, 100% 3%, 97% 100%, 0% 95%
  ); /* bords biseautés */
  box-shadow:
    0 4px 12px oklch(0% 0 0 / 0.15),
    0 20px 60px oklch(0% 0 0 / 0.1),
    0 0 80px oklch(var(--color-primary-l) var(--color-primary-c) var(--color-primary-h) / 0.15);
    /* glow dans la couleur primaire */
}
```

---

## Pattern 6 — Chevauchement texte/image via grid overlap

**Curseur A** : ≥ 2
**Quand l'utiliser** : quand texte et image doivent se répondre visuellement. Le texte est PAR-DESSUS l'image, pas à côté. Idéal pour voice blocks à fort impact et manifesto sections.

```
┌──────────────────────────────────────────┐
│                                          │
│   ┌──────────────────────────────────┐   │
│   │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│   │
│   │░░░░░░░░ IMAGE ░░░░░░░░░░░░░░░░░│   │
│   │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│   │
│   │  ┌──────────────────┐  gradient │   │
│   │  │                  │  overlay  │   │
│   │  │   TEXTE          │  direc-   │   │
│   │  │   z-index: 2     │  tionnel  │   │
│   │  │                  │           │   │
│   │  └──────────────────┘           │   │
│   │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│   │
│   └──────────────────────────────────┘   │
│                                          │
└──────────────────────────────────────────┘
```

Texte et image partagent la meme cellule grid. Le gradient directionnel assure la lisibilité.

```css
.overlap-hero {
  display: grid;
  /* Texte et image dans la même zone */
  grid-template-columns: 1fr;
  grid-template-rows: 1fr;
  min-block-size: 80vh;
}

.overlap-hero > * {
  grid-column: 1 / -1;
  grid-row: 1 / -1;
}

.overlap-hero img {
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
  z-index: 0;
}

/* Gradient directionnel — adapté à la zone focale de l'image */
.overlap-hero__overlay {
  z-index: 1;
  background: linear-gradient(
    135deg,
    var(--color-surface) 30%,
    oklch(0% 0 0 / 0.4) 60%,
    oklch(0% 0 0 / 0) 100%
  );
}

.overlap-hero__content {
  z-index: 2;
  align-self: end;
  padding: var(--space-2xl);
  max-inline-size: 60ch;
}
```

---

## Résumé par curseur A

| Curseur | Patterns disponibles | Logique |
|---------|---------------------|---------|
| A = 1 | 1 (Split), 2 (Mask-image) | Structuré, propre, pas un rectangle posé |
| A = 2 | 1, 2, 3 (Clip-path), 4 (Full-bleed), 6 (Overlap) | Signal distinctif, technique au service du concept |
| A = 3 | Tous, dont 5 (Overflow) | Transgression, grid cassée, tension visuelle |

## Combinaisons

Un style-tile avec plusieurs images peut mixer les patterns. Par exemple :
- Voice Block → Pattern 1 (split) + Atmosphere → Pattern 4 (full-bleed)
- Voice Block → Pattern 6 (overlap) + Artefact → Pattern 3 (clip-path)

La variété de technique entre les sections renforce la richesse visuelle.
