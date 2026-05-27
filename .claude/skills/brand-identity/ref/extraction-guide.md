# Guide d'Extraction — Brand DNA (Mode D)

Ce fichier est la référence pour le subagent de Phase D2. Il définit la structure attendue du document Brand DNA, les règles d'extraction, et les stratégies de gap-filling.

---

## 1. Structure du document Brand DNA

Le fichier `{brand}-extracted-dna.md` doit suivre EXACTEMENT cette structure :

```markdown
# {Brand} — ADN de Marque Extrait

## 1. PALETTE DE COULEURS

### 1.1 Couleurs primaires
- Primary: #XXXXXX — {usage observé} — {✅|🔍|💡}
- Primary Light: #XXXXXX — {usage} — {niveau confiance}
- Primary Dark: #XXXXXX — {usage} — {niveau confiance}

### 1.2 Couleurs secondaires / accent
- Secondary: #XXXXXX — {usage} — {niveau confiance}
- Accent: #XXXXXX — {usage} — {niveau confiance}
- Accent Light: #XXXXXX — {niveau confiance}
- Accent Dark: #XXXXXX — {niveau confiance}

### 1.3 Neutres
- Surface: #XXXXXX — {niveau confiance}
- Surface Alt: #XXXXXX — {niveau confiance}
- Depth: #XXXXXX — {niveau confiance}
- Neutral 100: #XXXXXX → Neutral 900: #XXXXXX — {niveau confiance}

### 1.4 Couleurs texte
- Text Primary: #XXXXXX — {niveau confiance}
- Text Secondary: #XXXXXX — {niveau confiance}
- Text Muted: #XXXXXX — {niveau confiance}
- Text On-Primary: #XXXXXX — {niveau confiance}
- Text On-Dark: #XXXXXX — {niveau confiance}

### 1.5 Couleurs sémantiques
- Success: #XXXXXX — {extrait ou proposé} — {niveau confiance}
- Warning: #XXXXXX — {extrait ou proposé} — {niveau confiance}
- Error: #XXXXXX — {extrait ou proposé} — {niveau confiance}
- Info: #XXXXXX — {extrait ou proposé} — {niveau confiance}

### 1.6 Palette Data-Viz (4 couleurs)
- DataViz 1: #XXXXXX — {niveau confiance}
- DataViz 2: #XXXXXX — {niveau confiance}
- DataViz 3: #XXXXXX — {niveau confiance}
- DataViz 4: #XXXXXX — {niveau confiance}

## 2. TYPOGRAPHIE

### 2.1 Familles
- Display: {font-family} — source: {Google Fonts / Adobe / système} — {niveau confiance}
- Body: {font-family} — source: {source} — {niveau confiance}
- Mono: {font-family} — source: {source} — {niveau confiance}

### 2.2 Échelle typographique
- Ratio estimé: {ratio} (basé sur les tailles observées)
- xs: {valeur}
- sm: {valeur}
- base: {valeur}
- lg: {valeur}
- xl: {valeur}
- 2xl: {valeur}
- 3xl: {valeur}
- 4xl: {valeur}
- 5xl: {valeur} (si observé)

### 2.3 Poids utilisés
- Display: {weights} — {niveau confiance}
- Body: {weights} — {niveau confiance}

## 3. CODE CIVIL ATOMIQUE

### 3.1 Radius
- sm: {valeur} — {niveau confiance}
- md: {valeur} — {niveau confiance}
- lg: {valeur} — {niveau confiance}
- xl: {valeur} — {niveau confiance}
- full: 9999px

### 3.2 Ombres
- Subtle: {valeur} — {niveau confiance}
- sm: {valeur} — {niveau confiance}
- md: {valeur} — {niveau confiance}
- lg: {valeur} — {niveau confiance}
- Elevated: {valeur} — {niveau confiance}

### 3.3 Espacements
- Grille de base: {valeur}px (8px standard ou observé)
- xs: {valeur}
- sm: {valeur}
- md: {valeur}
- lg: {valeur}
- xl: {valeur}
- 2xl: {valeur}

### 3.4 Transitions
- Fast: {valeur} — {niveau confiance}
- Base: {valeur} — {niveau confiance}
- Slow: {valeur} — {niveau confiance}

### 3.5 Gradients (si observés)
- {description du gradient et valeur CSS}

## 4. COMPOSANTS CLÉS (observés)

### 4.1 Boutons
- Style primaire: {description + propriétés CSS clés}
- Style secondaire: {description}
- Hover/Focus states: {description}

### 4.2 Cartes (si observées)
- {description + propriétés CSS clés}

### 4.3 Navigation
- {description du style de navigation}

### 4.4 Formulaires (si observés)
- {description des inputs, selects, etc.}

## 5. ANALYSE VISUELLE

### 5.1 Ton de voix
- Registre: {formel/décontracté/technique/poétique/etc.}
- Exemples headlines: {3-5 exemples caractéristiques}
- Vocabulaire dominant: {mots-clés récurrents}
- Personnalité: {3-5 adjectifs}

### 5.2 Style photographique
- Type dominant: {portrait/lifestyle/produit/etc.}
- Traitement chromatique: {naturel/saturé/désaturé/filtré/etc.}
- Éclairage: {naturel/studio/dramatique/etc.}

### 5.3 Style d'icônes
- Type: {outline/solid/duotone/mixed}
- Épaisseur: {fine/regular/bold}
- Coins: {rounded/sharp}

### 5.4 Logo (si fourni)
- Type: {wordmark/lettermark/pictorial/combinaison}
- Couleurs: {liste des couleurs du logo}
- Style: {description}
- Proportions: {ratio largeur/hauteur approximatif}

### 5.5 Densité & espace blanc
- Approche: {aéré/équilibré/dense}
- Ratio espace blanc estimé: {élevé/moyen/faible}

## 6. POSITIONNEMENT ESTIMÉ

### 6.1 Curseur A (Audace Créative): {1-3}
Justification: {2-3 phrases expliquant pourquoi ce score}
Signaux observés: {éléments visuels qui justifient le score}

### 6.2 Curseur B (Différenciation): {1-3}
Justification: {2-3 phrases expliquant pourquoi ce score}
Signaux observés: {éléments visuels qui justifient le score}

### 6.3 Personnalité de marque
{3-5 adjectifs avec justification}

## 7. LACUNES IDENTIFIÉES
- {Liste des éléments non trouvés ou incertains}
- {Pour chaque lacune : recommandation de gap-filling}
```

---

## 2. Niveaux de confiance

Chaque valeur extraite doit être annotée avec un niveau de confiance :

| Icône | Niveau | Signification |
|---|---|---|
| ✅ | **Extrait** | Trouvé directement dans le CSS/HTML — haute confiance |
| 🔍 | **Analysé** | Déduit de l'analyse visuelle des screenshots — confiance moyenne |
| 💡 | **Proposé** | Non trouvé, proposé par gap-filling — nécessite validation utilisateur |

---

## 3. Règles d'extraction CSS

### Priorité des sources
1. **CSS Custom Properties** (`--color-*`, `--font-*`, etc.) — source la plus fiable
2. **Valeurs inline dans `<style>`** — fiable
3. **Fichiers CSS externes** — fiable mais attention aux overrides
4. **Attributs `style=""` inline** — dernier recours

### Identification de la palette
1. Collecter TOUTES les couleurs uniques (hex, rgb, hsl, named colors)
2. Compter les occurrences de chaque couleur
3. Classifier par fréquence :
   - Les 1-2 couleurs les plus fréquentes en `background-color` ou `color` sur des éléments proéminents → **Primary**
   - Couleurs des boutons/CTAs/liens → **Accent**
   - Couleurs des `background-color` des sections → **Surface**
   - Couleurs des `color` sur le texte → **Text**
4. Vérifier avec les screenshots si la hiérarchie correspond visuellement

### Identification typographique
1. Chercher les `<link>` Google Fonts dans le `<head>`
2. Chercher les `@import` dans le CSS
3. Chercher les `@font-face` declarations
4. Parser les `font-family` declarations pour les stacks
5. La font des `h1`/`h2` → **Display**
6. La font du `body`/`p` → **Body**
7. La font des `code`/`pre` → **Mono** (si présente)

### Déduction de l'échelle typo
1. Collecter toutes les `font-size` declarations
2. Trier par taille croissante
3. Calculer le ratio entre chaque palier
4. Mapper sur l'échelle xs → 5xl

### Extraction des radius
1. Collecter toutes les `border-radius` declarations uniques
2. Identifier les patterns récurrents (petit, moyen, grand)
3. Mapper sur sm/md/lg/xl/full

### Extraction des ombres
1. Collecter toutes les `box-shadow` declarations
2. Classer par intensité (blur radius + spread)
3. Mapper sur subtle/sm/md/lg/elevated

---

## 4. Règles de gap-filling

### Palette Data-Viz (si absente)
1. Prendre la couleur Primary
2. Générer 3 variations à 90°, 180°, 270° sur la roue chromatique (HSL)
3. Ajuster la saturation pour cohérence visuelle
4. Vérifier que les 4 couleurs sont suffisamment distinctes entre elles

### Couleurs sémantiques (si absentes)
- **Success** : vert harmonisé avec la palette (#22C55E par défaut, ajuster la teinte)
- **Warning** : jaune/orange harmonisé (#F59E0B par défaut)
- **Error** : rouge harmonisé (#EF4444 par défaut)
- **Info** : bleu harmonisé (#3B82F6 par défaut, ou utiliser Primary si bleu)
- Ajuster la saturation et luminosité pour harmoniser avec le reste de la palette

### Typo Mono (si absente du site)
Proposer une famille cohérente avec la Body font :
- Body géométrique (Inter, Roboto) → JetBrains Mono, Fira Code
- Body humaniste (Open Sans, Lato) → Source Code Pro, IBM Plex Mono
- Body serif (Merriweather, Georgia) → Courier Prime, DM Mono
- Body technique (IBM Plex Sans, Space Grotesk) → IBM Plex Mono, Space Mono

### Transitions (si non trouvées)
- Fast: `150ms ease`
- Base: `250ms ease`
- Slow: `400ms ease`

### Espacements (si pattern non clair)
Utiliser une grille 8px :
- xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px, 2xl: 48px

---

## 5. Checklist de complétude

Avant de finaliser le Brand DNA, vérifier que TOUTES ces sections sont présentes :

- [ ] 1.1 Couleurs primaires (au moins primary + light + dark)
- [ ] 1.2 Couleurs secondaires/accent (au moins 1 accent)
- [ ] 1.3 Neutres (au moins surface + surface-alt)
- [ ] 1.4 Couleurs texte (au moins primary + secondary)
- [ ] 1.5 Couleurs sémantiques (success, warning, error, info)
- [ ] 1.6 Palette Data-Viz (4 couleurs)
- [ ] 2.1 Familles typo (au moins display + body)
- [ ] 2.2 Échelle typo (au moins base, lg, xl, 2xl)
- [ ] 2.3 Poids utilisés
- [ ] 3.1 Radius (au moins sm, md, lg)
- [ ] 3.2 Ombres (au moins sm, md, lg)
- [ ] 3.3 Espacements (au moins sm, md, lg, xl)
- [ ] 3.4 Transitions (fast, base, slow)
- [ ] 5.1 Ton de voix
- [ ] 5.2 Style photographique
- [ ] 5.3 Style d'icônes
- [ ] 6.1 Curseur A estimé avec justification
- [ ] 6.2 Curseur B estimé avec justification
- [ ] 6.3 Personnalité de marque
- [ ] 7 Lacunes identifiées

Si une section est incomplète → utiliser le gap-filling (section 4) et annoter avec 💡.
