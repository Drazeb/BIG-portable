# REX — Composition créative des images dans les Style-Tiles (Phase 4)

Date : 2026-03-04
Session : test-camille-test-20260304-0116
Observé par : Charles + Claude
Lié à : `ref/rex-visual-integration-phase4.md` (REX précédent sur la visibilité des images)

---

## Contexte : le REX précédent est résolu

Le REX `rex-visual-integration-phase4.md` documentait le problème "le subagent Phase 4 ne voit pas les images". La Solution A (images basse résolution 400px JPEG q60 injectées dans le prompt) a été implémentée et **fonctionne** :

- Les images `.tmp-prompt-c{concept}-{n}.jpg` sont créées à 400px
- Elles sont encodées en base64 (~5-8K tokens par image)
- Les subagents les reçoivent via le Read tool (multimodal) et les VOIENT réellement
- Le swap haute résolution en post-traitement (4A-bis) fonctionne

**Le problème documenté ici est NOUVEAU** : même quand le subagent VOIT les images, il les intègre de façon basique — "posées" dans des conteneurs rectangulaires plutôt que composées en dialogue avec le reste du design.

---

## Problème

### Ce qu'on observe visuellement

Les images sont placées dans des blocs rectangulaires empilés verticalement. Elles ressemblent à des photos dans un article de blog plus qu'à des éléments structurants d'une composition de design. L'impression est que le design a été fait SANS les images, puis qu'elles ont été ajoutées après dans des "trous" prévus à cet effet.

### Captures d'écran de référence

Dossier : `/Users/charlesbezard/Documents/Captures écran/`

**Concept 2 — L'Observatoire (3 images, le cas le plus flagrant) :**

- `Capture d'écran 2026-03-04 à 10.21.15.png` — Voice Block : grille éditoriale 3 colonnes en haut, puis image de l'observatoire en bandeau pleine largeur en dessous. L'image est juste POSÉE sous le texte, comme une photo dans un article. Aucun chevauchement, aucune interaction layout/image.

- `Capture d'écran 2026-03-04 à 10.21.30.png` — Zone artefact/atmosphere : la coupole d'observation est en bandeau 16:9, suivie DIRECTEMENT par l'instrument de navigation en bandeau 16:9. Deux images empilées l'une sur l'autre en mode blog, séparées par un petit gap. Aucune composition entre elles ni avec les éléments environnants.

- `Capture d'écran 2026-03-04 à 10.21.44.png` — Idem, zoom sur les deux bandeaux empilés (coupole + astrolabe). Les images sont de grande qualité et s'intègrent chromatiquement (bleu nuit/cuivre cohérents), mais la COMPOSITION est plate.

**Concept 1 — Cristal Brut (2 images, mieux intégrées) :**

- `Capture d'écran 2026-03-04 à 10.21.52.png` — Voice Block : composition split 60/40, l'image du réseau cristallin est dans la partie droite avec un `clip-path` polygonal animé (facettes cristallines). C'est MIEUX — il y a un dialogue forme/concept. Mais l'image de l'Atmosphere block (plans de clivage) est elle aussi dans un conteneur rectangulaire avec juste un clip-path asymétrique léger.

### Le delta entre les deux concepts prouve que c'est faisable

Le concept 1 montre que le subagent PEUT faire de l'intégration créative (clip-path polygonal lié au concept cristallin). Le concept 2 ne le fait pas — il se contente de `border-radius: 6px` + `object-fit: cover` dans des conteneurs rectangulaires empilés.

---

## Analyse du code CSS réel

### Concept 2 — L'Observatoire (intégration BASIQUE)

Les 3 images utilisent le même pattern minimal :

```css
/* Image 1 — Voice Block hero (observatoire) */
.voice-hero-image {
    grid-column: 1 / 4;     /* pleine largeur dans la grille */
    grid-row: 3;             /* sous le texte */
    block-size: 340px;       /* hauteur fixe → bandeau */
    border-radius: 6px;      /* coins arrondis basiques */
    overflow: hidden;
}
.voice-hero-image img {
    object-fit: cover;
    object-position: center 35%;   /* cadrage vertical adapté */
}
.voice-hero-image::after {
    /* gradient d'overlay pour transition vers le fond */
    background: linear-gradient(to top, oklch(0.96 ... / 0.9) 0%, transparent 60%);
}

/* Image 2 — Dashboard central (astrolabe) */
.dashboard__central {
    grid-column: 1 / 3;
    block-size: 280px;       /* encore un bandeau hauteur fixe */
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid var(--color-border);
}
.dashboard__central img {
    object-fit: cover;       /* même pattern */
}

/* Image 3 — Atmosphere (coupole) */
.atmosphere-visual {
    block-size: 360px;       /* encore un bandeau */
    border-radius: 6px;
    overflow: hidden;
}
.atmosphere-visual img {
    object-fit: cover;
    filter: saturate(0.9) brightness(0.95);
}
```

**Diagnostic : AUCUNE technique de composition créative** — pas de `clip-path`, pas de `mask-image`, pas de `mix-blend-mode` significatif, pas de chevauchement texte/image, pas de forme non-rectangulaire. Les 3 images sont dans des boîtes rectangulaires à coins arrondis avec un gradient d'overlay. C'est la technique de base, pas une composition pensée.

### Concept 1 — Cristal Brut (intégration MEILLEURE)

```css
/* Image 1 — Voice Block (réseau cristallin) */
.voice-block__visual {
    aspect-ratio: 1;
    --facet-clip: 15%;
    clip-path: polygon(
        var(--facet-clip) 0%, 100% 0%,
        100% calc(100% - var(--facet-clip)),
        calc(100% - var(--facet-clip)) 100%,
        0% 100%, 0% var(--facet-clip)
    );
    transition: --facet-clip var(--transition-slow), clip-path var(--transition-slow);
}
.voice-block__visual:hover { --facet-clip: 10%; }  /* la facette "tourne" au hover */
.voice-block__visual::after {
    mix-blend-mode: multiply;  /* overlay teinté grès */
}

/* Image 2 — Atmosphere (plans de clivage) */
.atmosphere-block__visual {
    clip-path: polygon(0% 8%, 92% 0%, 100% 92%, 8% 100%);  /* forme asymétrique */
    transition: clip-path var(--transition-slow);
}
.atmosphere-block__visual:hover {
    clip-path: polygon(0% 5%, 95% 0%, 100% 95%, 5% 100%);  /* micro-animation */
}
.atmosphere-block__visual::after {
    mix-blend-mode: multiply;
}
```

**Diagnostic : intégration CRÉATIVE** — `clip-path` polygonal qui incarne le concept (facettes cristallines), animation au hover via `@property`, `mix-blend-mode: multiply`. Il y a un DIALOGUE entre la forme CSS et le concept narratif. C'est ce qu'on veut partout.

---

## Pourquoi le concept 2 est basique et le concept 1 est mieux

### Ce n'est PAS le curseur A

Les deux concepts sont en A=2. Le curseur A prescrit :

> A=2 : Au moins UNE asymétrie contrôlée. Au moins UNE surface expressive. Au moins UNE technique CSS non-standard.

Les images "posées en bandeaux" ne sont PAS un comportement prescrit par A=2. Même A=1 ("compositions structurées") ne veut pas dire "images posées à plat" — une composition structurée peut intégrer une image en split avec overlay, en fond de section avec mask, etc.

### C'est le pattern "Code > Rules" (encore)

C'est le même mécanisme qu'on a documenté pour le CSS moderne (D19/D20) et la finition élite :

1. **Les instructions disent** : "compose EN FONCTION du contenu réel", "clip-path/mask-image EN DIALOGUE avec l'image"
2. **Les exemples style-tile NE MONTRENT PAS d'images** — les 3 exemples (A, B, C) sont des style-tiles sans visuels
3. **Le subagent n'a jamais vu** à quoi ressemble une intégration créative d'image dans un style-tile → il fait le truc safe

Le concept 1 s'en sort mieux PARCE QUE le pitch dit explicitement "clip-path: polygon() pour les formes géométriques angulaires (facettes cristallines)". Le subagent a appliqué cette technique à l'image. Le concept 2 n'avait pas d'instruction aussi directe pour le traitement des images → il a fait le minimum.

### Le prompt Phase 4 a les bons PRINCIPES mais pas les bons EXEMPLES

Dans `phase-4-styletile.md` (lignes 55-60) :
```
## DIRECTIVE VISUELLE (si des images sont fournies ci-dessus)
- Adapte les overlays/gradients aux zones sombres et claires de l'image
- Positionne le texte là où l'image offre du contraste
- Utilise clip-path/mask-image en dialogue avec la composition de l'image
```

C'est correct mais ce sont des **principes**. Le LLM a besoin de **code concret** pour savoir ce que "en dialogue avec la composition" veut dire en CSS. Sans modèle visuel, il interprète "dialogue" comme "j'ai mis un gradient d'overlay".

---

## Solutions proposées

### Solution 1 — Catalogue de patterns d'intégration image (recommandée, haute priorité)

Ajouter dans le prompt Phase 4 (ou dans un fichier ref/ dédié) un **catalogue de patterns CSS concrets** pour l'intégration d'images. Le LLM voit du code → il le reproduit/adapte.

Exemples de patterns à documenter :

**Pattern A — Image en split avec chevauchement texte**
```css
/* L'image occupe 55% de la largeur, le texte chevauche de 10% */
.hero { display: grid; grid-template-columns: 55% 1fr; }
.hero__image { grid-column: 1; grid-row: 1; }
.hero__content {
    grid-column: 1 / 3;  /* chevauche les 2 colonnes */
    grid-row: 1;
    padding-inline-start: 48%;  /* le texte commence sur l'image */
    z-index: 1;
}
.hero__image::after {
    /* gradient qui fond l'image vers le texte */
    background: linear-gradient(to right, transparent 60%, var(--bg) 100%);
}
```

**Pattern B — Image en fond de section avec mask-image**
```css
/* L'image est en fond, découpée par un mask organique */
.section {
    position: relative;
    background: var(--bg);
}
.section__image {
    position: absolute;
    inset: 0;
    z-index: 0;
}
.section__image img {
    width: 100%; height: 100%;
    object-fit: cover;
    mask-image: linear-gradient(to bottom, black 30%, transparent 80%);
    opacity: 0.15;  /* image en fond subtil */
}
.section__content { position: relative; z-index: 1; }
```

**Pattern C — Image découpée en forme conceptuelle (clip-path)**
```css
/* L'image suit une forme liée au concept */
.visual {
    clip-path: polygon(10% 0, 100% 0, 90% 100%, 0 100%);
    /* ou circle(), ellipse(), path() selon le concept */
}
```

**Pattern D — Image qui déborde de son conteneur (z-index + negative margin)**
```css
/* L'image dépasse le cadre de sa section — casse la grille intentionnellement */
.card__image {
    margin-block-start: -3rem;  /* déborde au-dessus de la card */
    margin-inline-end: -2rem;   /* déborde à droite */
    clip-path: polygon(0 8%, 100% 0, 95% 100%, 5% 92%);
    box-shadow: 0 20px 48px oklch(0.2 0.02 30 / 0.15);
}
```

**Pattern E — Composition split asymétrique avec gradient de liaison**
```css
/* Grille 2 colonnes, image à gauche avec gradient qui fond dans le design */
.split { display: grid; grid-template-columns: 1.2fr 1fr; gap: 0; }
.split__image {
    position: relative;
    min-block-size: 500px;
}
.split__image img {
    object-fit: cover;
    filter: saturate(0.85);
}
.split__image::after {
    /* gradient qui crée une transition douce vers la colonne texte */
    background: linear-gradient(
        to right,
        transparent 0%,
        transparent 65%,
        var(--bg) 100%
    );
}
```

**Pattern F — Mix-blend-mode pour teinter l'image dans la palette**
```css
/* L'image est teintée dans la palette du concept (pas juste posée) */
.visual-wrapper {
    background: var(--color-primary);  /* fond coloré sous l'image */
}
.visual-wrapper img {
    mix-blend-mode: luminosity;  /* l'image perd ses couleurs, garde la luminosité */
    opacity: 0.85;
}
/* Variante : overlay pour teinter tout en gardant les détails */
.visual-wrapper img { mix-blend-mode: overlay; }
```

### Solution 2 — Directive de composition renforcée dans le prompt Phase 4

Remplacer le bloc "DIRECTIVE VISUELLE" (actuellement 5 lignes de principes) par une directive plus explicite :

```markdown
## DIRECTIVE VISUELLE — COMPOSITION AVEC IMAGES

Les images ne sont PAS des décorations à poser dans des conteneurs.
Elles sont des ÉLÉMENTS STRUCTURANTS de la composition.

### Ce qu'on NE veut PAS
- Image en bandeau pleine largeur posée entre deux sections
- Image dans un div rectangulaire avec juste border-radius + object-fit: cover
- Images empilées verticalement comme dans un article de blog
- Image isolée du reste du layout (pas de chevauchement, pas d'interaction visuelle)

### Ce qu'on VEUT
- L'image PARTICIPE à la composition (en split avec le texte, en fond avec mask, découpée par clip-path, en chevauchement avec un autre élément)
- Le layout est PENSÉ AVEC l'image (pas construit puis l'image ajoutée après)
- Au moins UNE technique de composition parmi : clip-path sur l'image, mask-image, chevauchement texte/image via grid overlap, mix-blend-mode significatif, image en fond de section avec overlay
- Les gradients d'overlay ne sont pas juste "posés" mais LIENT l'image au design (transition vers la couleur de fond, fondu dans le texte adjacent)

### Le test : si on retirait l'image, le layout devrait sembler INCOMPLET (pas identique mais avec un trou)
```

### Solution 3 — Ajouter des images aux exemples style-tile

C'est la solution la plus lourde mais la plus efficace à long terme (pattern "Code > Rules"). Si les exemples A, B, C contiennent des images intégrées de façon créative, le subagent VERRA comment faire.

**Difficulté** : les exemples sont pour des brands fictives. Il faudrait soit :
- Générer des images Recraft/MJ pour chaque exemple (lourd)
- Utiliser des images placeholder (carré coloré avec des zones claires/sombres) qui montrent les TECHNIQUES CSS sans nécessiter un vrai visuel
- Injecter dans les exemples des images en SVG minimaliste (formes abstraites) qui montrent les patterns clip-path, mask-image, blend-mode

**Variante plus légère** : ne pas ajouter d'images aux exemples existants, mais créer UN exemple dédié "intégration image" dans `ref/` qui montre les 5-6 patterns CSS avec des placeholders visuels.

### Solution 4 — Enrichir les fiches visuelles avec une recommandation de COMPOSITION (pas juste de CSS)

Actuellement la fiche enrichie (Solution C du REX précédent) propose :
```
- **Recommandation CSS** : placer dans la partie supérieure du voice-block, gradient linéaire...
```

Enrichir avec une recommandation de COMPOSITION :
```
- **Recommandation de composition** : SPLIT 55/45 avec l'image à gauche, le texte chevauche sur 10% de l'image via grid overlap. Gradient de liaison de l'image vers le fond lin. L'image est l'ancrage visuel du Voice Block, pas un bandeau sous le texte.
- **Pattern CSS recommandé** : Pattern A (split avec chevauchement) ou Pattern E (split asymétrique avec gradient de liaison)
```

Ce qui donne à l'orchestrateur (qui VOIT l'image et comprend la composition globale) le pouvoir de prescrire le pattern, et au subagent le code concret à appliquer.

---

## Recommandation combinée

| Priorité | Solution | Impact | Effort |
|----------|----------|--------|--------|
| **1 (immédiat)** | Solution 2 — Directive renforcée | Moyen — oriente les choix mais "Rules" seules | Faible (~20 lignes à modifier dans phase-4-styletile.md) |
| **2 (court terme)** | Solution 1 — Catalogue de patterns | Fort — "Code > Rules" prouvé | Moyen (~100 lignes dans un fichier ref/) |
| **3 (court terme)** | Solution 4 — Fiches enrichies avec composition | Fort — l'orchestrateur prescrit le pattern | Faible (~15 lignes dans le SKILL.md, section visual_reference_block) |
| **4 (moyen terme)** | Solution 3 — Images dans les exemples | Très fort — le modèle ultime | Fort (création d'assets + modification des 3 exemples) |

**L'idéal** : combiner 1 + 2 + 4 (effort raisonnable, impact cumulatif fort). La Solution 3 en chantier séparé quand les exemples seront mis à jour.

---

## Note sur le curseur A et les images

Le curseur A (Audace de composition) ne DOIT PAS limiter la qualité d'intégration des images. Même en A=1 :
- Une image en split avec gradient de liaison est une composition "structurée" (A=1)
- Une image en fond de section avec mask-image est "structurée"
- Un clip-path rectangulaire avec un léger angle est "structuré"

Ce qui change avec A :
- **A=1** : Image intégrée dans une composition structurée (split régulier, fond avec mask linéaire)
- **A=2** : Image avec une technique distinctive (clip-path conceptuel, chevauchement texte/image, mix-blend-mode significatif)
- **A=3** : Image qui casse les conventions (full-bleed avec texte par-dessus, fragmentation, collage, multi-image en overlap)

Ce qui ne change PAS avec A : la qualité de l'intégration. "Image posée en bandeau" n'est jamais acceptable, même en A=1.

---

## Fichiers à modifier

| Fichier | Modification |
|---------|-------------|
| `phases/phase-4-styletile.md` | Remplacer le bloc "DIRECTIVE VISUELLE" (lignes 55-60) par la version renforcée (Solution 2) + référence au catalogue de patterns |
| `ref/image-composition-patterns.md` | NOUVEAU — catalogue de 5-6 patterns CSS concrets avec code (Solution 1) |
| `SKILL.md` section `{visual_reference_block}` (~ligne 1100-1135) | Ajouter le champ "Recommandation de composition" et "Pattern CSS recommandé" dans la fiche visuelle enrichie (Solution 4) |

---

## Dernière mise à jour : 2026-03-04
