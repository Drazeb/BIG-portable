# REX Vectorisation SVG — Méthode vtracer (Feb 2026)

## Contexte

Ce document décrit la méthode fiable pour convertir un logo PNG (généré via Midjourney) en SVG propre, utilisable dans le pipeline BIG. Il remplace l'ancienne méthode (écriture manuelle de paths SVG par le LLM) qui échoue systématiquement sur les formes organiques.

---

## Pourquoi l'écriture manuelle de SVG échoue (TOUJOURS)

### Le problème fondamental

Un LLM ne peut pas écrire à la main des paths SVG avec courbes de Bézier pour reproduire une forme organique complexe. Voici pourquoi :

1. **Pas de feedback visuel** : Le LLM écrit des coordonnées (ex: `C 20 14, 4 40, 10 78`) sans jamais VOIR le résultat. Il travaille à l'aveugle.

2. **Les courbes de Bézier sont contre-intuitives** : Les points de contrôle d'une cubique (`C x1 y1, x2 y2, x y`) ne sont pas SUR la courbe — ils la tirent vers eux. Sans visualisation, il est impossible de prédire la forme résultante.

3. **Erreurs cumulatives** : Une erreur de 5px sur un point de contrôle déforme toute la courbe. Sur un path de 10+ segments, les erreurs se cumulent et le résultat est méconnaissable.

4. **Les formes fermées (filled) sont piégeuses** : Pour un croissant (forme concave), il faut tracer le contour extérieur PUIS le contour intérieur en sens inverse, puis fermer avec `Z`. Le moindre décalage entre les deux contours crée des aberrations (épaisseurs variables, pointes qui se croisent).

### Résultat observé sur 3 tentatives

| Tentative | Approche | Résultat |
|-----------|----------|----------|
| V1 | Courbes séparées (outer + inner) | Traits fins au lieu de formes remplies |
| V2 | Path unique (outer edge → inner edge → Z) | Forme massive en V, proportions fausses |
| V3 | V2 avec ajustements de coordonnées | Forme de bouclier/barbe, pointes dédoublées |

**Conclusion : NE JAMAIS tenter d'écrire manuellement des paths SVG pour des logos organiques.** Même pour des logos "simples" (3-4 formes), le LLM échouera sur les courbes. Seules les formes purement géométriques (rectangles, cercles, polygones réguliers) sont réalisables à la main.

---

## La méthode qui fonctionne : vtracer (auto-trace)

### Principe

`vtracer` est un outil de vectorisation automatique (bitmap → SVG) écrit en Rust, disponible comme package Python. Il analyse les pixels de l'image PNG et génère des paths SVG fidèles à la forme originale.

### Installation

```bash
pip3 install vtracer
```

Version testée : 0.6.11 (Feb 2026). Le package est léger (~5 MB) et s'installe en quelques secondes.

### Commande de conversion

```bash
vtracer --input "{path_to_png}" \
        --output "{path_to_svg}" \
        --colormode color \
        --mode spline \
        --filter_speckle 4 \
        --color_precision 6 \
        --corner_threshold 60 \
        --segment_length 4 \
        --splice_threshold 45
```

**Paramètres clés :**
- `--colormode color` : Préserve les couleurs du PNG (pas de conversion N&B)
- `--mode spline` : Utilise des splines (courbes lisses) au lieu de polygones (plus fidèle pour les logos organiques)
- `--filter_speckle 4` : Supprime les artefacts inférieurs à 4px (antialiasing)
- `--color_precision 6` : Précision de la quantification couleur (6 = bon compromis)
- `--corner_threshold 60` : Seuil de détection des angles (60° = conserve les pointes du logo)
- `--segment_length 4` : Longueur des segments de spline (4 = bonne précision)
- `--splice_threshold 45` : Seuil de fusion des segments

### Résultat brut

vtracer produit un SVG avec :
- Un **path rectangulaire de fond** (la couleur de fond du PNG) → à supprimer
- **4-6 paths principaux** correspondant aux zones de couleur du logo → à conserver
- **10-15 petits paths d'artefacts** (antialiasing, transitions entre couleurs) → à supprimer
- Des **couleurs approximatives** (moyennées par zone) → à corriger
- Un `width/height` fixe (ex: 2048x2048) → à remplacer par un viewBox

---

## Post-processing (obligatoire)

Le SVG brut de vtracer n'est PAS directement utilisable. Il faut 5 étapes de nettoyage :

### Étape 1 — Identifier les paths

Ouvrir le SVG brut et identifier chaque `<path>` :
- **Path 1** (le plus grand, souvent le premier) : c'est le **fond** → SUPPRIMER
- **Paths 2-5** (les plus grands après le fond) : ce sont les **formes principales** du logo → CONSERVER
- **Paths 6+** (petits paths avec des coordonnées proches de 0-20px) : ce sont les **artefacts** → SUPPRIMER

**Comment distinguer un artefact d'une forme utile :** Les artefacts ont des fills dans des teintes intermédiaires (ex: `#F4EDE6`, `#DAB9A8`) qui ne correspondent à aucune couleur principale du logo. Les formes utiles ont des fills proches des couleurs principales.

### Étape 2 — Corriger les couleurs

Remplacer les couleurs approximatives de vtracer par les valeurs HEX exactes du `:root` du style-tile :

| Couleur vtracer (approximative) | Couleur cible (`:root`) | Rôle |
|--------------------------------|------------------------|------|
| La teinte la plus proche du primary | `--color-primary` exact | Forme principale |
| La teinte la plus sombre | `--color-depth` exact | Forme secondaire |
| La teinte accent/vive | `--color-accent` exact | Élément d'accentuation |
| Toute teinte intermédiaire | `--color-primary-dark` ou suppression | Ombre/transition |

### Étape 3 — Ajuster le viewBox

Remplacer `width="2048" height="2048"` par un `viewBox` qui cadre le logo :

1. Calculer les bornes des paths conservés (en tenant compte des `transform="translate(x,y)"`)
2. Ajouter ~5-10% de padding
3. Format : `viewBox="minX minY width height"`

Exemple : Si le logo occupe x:[330-1715], y:[454-1566] → `viewBox="250 380 1540 1240"`

### Étape 4 — Ajouter les métadonnées

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="...">
<title>{brand} Logo</title>
<!-- paths ici -->
</svg>
```

### Étape 5 — Valider visuellement

```bash
open -a "Google Chrome" "{path_to_svg}"
```

Comparer côte à côte avec le PNG original. Le SVG doit être fidèle en termes de :
- Silhouette générale
- Proportions relatives des formes
- Positionnement des éléments les uns par rapport aux autres

---

## Récapitulatif du workflow complet

```
PNG Midjourney (upscaled 4x)
        │
        ▼
   pip3 install vtracer  (si pas déjà installé)
        │
        ▼
   vtracer --input logo.png --output logo.svg \
           --colormode color --mode spline \
           --filter_speckle 4 --color_precision 6 \
           --corner_threshold 60 --segment_length 4 \
           --splice_threshold 45
        │
        ▼
   POST-PROCESSING (orchestrateur) :
   1. Supprimer le path de fond (premier path, fill = couleur de fond)
   2. Supprimer les paths d'artefacts (petits paths, couleurs intermédiaires)
   3. Corriger les fills → couleurs exactes du :root
   4. Remplacer width/height par viewBox
   5. Ajouter <title>
        │
        ▼
   Ouvrir dans Chrome → validation utilisateur
        │
        ▼
   SVG propre, prêt pour les déclinaisons (L4)
```

---

## Limites connues

1. **Complexité du SVG** : vtracer génère des paths avec beaucoup de points (courbes très détaillées). Le fichier SVG peut faire 10-30 KB pour un logo. C'est acceptable pour le web mais pas optimal pour l'édition dans Figma/Illustrator. Si l'utilisateur veut un SVG minimal (4-10 formes simples), il faudra une vectorisation externe (Figma auto-trace, Illustrator Image Trace).

2. **Logos avec texte** : vtracer trace les lettres comme des formes. Le texte ne sera pas éditable (pas de `<text>`). Pour des wordmarks/lockups, le texte doit être ajouté séparément via `<text>` avec `font-family` et `@import` Google Fonts.

3. **Fond non-blanc** : Si le PNG Midjourney a un fond coloré (pas blanc pur), vtracer le trace comme un path. Il suffit de supprimer ce path lors du post-processing.

4. **Logos très organiques/aquarellés** : vtracer produit un résultat correct mais avec beaucoup de micro-paths pour les dégradés. Pour ces cas, augmenter `--filter_speckle` à 8-12 et `--color_precision` à 4-5.

---

## Quand utiliser quelle méthode

| Type de logo | Méthode | Raison |
|-------------|---------|--------|
| Formes géométriques pures (cercles, carrés, triangles) | Écriture manuelle SVG | Coordonnées prévisibles, pas de courbes complexes |
| Logo organique / abstract mark | **vtracer** (cette méthode) | Courbes fidèles, impossible à la main |
| Wordmark (texte seul) | `<text>` SVG + Google Fonts | Texte éditable, pas besoin de tracer |
| Logo complexe avec dégradés | Vectorisation externe (Figma/Illustrator) | vtracer ne gère pas les gradients SVG |

---

*Document créé le 15 Feb 2026 — Testé avec succès sur le logo "Solstice Fertile" (Atelier Vermeil, session a2-b2).*
