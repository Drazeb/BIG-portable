# Guide de Direction Visuelle — Pour le DA photo/illu (Skill Visual Brief)

Ce fichier donne au skill Visual Brief le jugement créatif d'un directeur artistique spécialisé en direction photographique et iconographique. Il ne remplace PAS les guides techniques MJ/Recraft (qui disent COMMENT prompter) — il dit QUOI prompter et POURQUOI.

---

## 1. CONCEPT NARRATIF → DIRECTION VISUELLE

Le concept narratif est une métaphore. La direction visuelle traduit cette métaphore en choix concrets de lumière, cadrage, composition et traitement. Ce tableau donne les réflexes de traduction :

### Registres émotionnels et leur traduction visuelle

| Registre du concept | Lumière | Cadrage | Composition | Traitement couleur | Texture/Grain |
|---------------------|---------|---------|-------------|-------------------|---------------|
| **Tension / Conflit** | Clair-obscur, source latérale dure, ombres marquées | Angles non-conventionnels (plongée, contre-plongée, dutch angle) | Diagonales dominantes, déséquilibre assumé, sujet excentré | Contraste élevé, désaturation sélective | Grain prononcé, bords nets |
| **Harmonie / Unité** | Lumière diffuse, dorée ou bleutée, enveloppante | Plan moyen, hauteur d'yeux, frontal ou 3/4 | Symétrie ou quasi-symétrie, centrage, lignes horizontales | Palette restreinte, tons analogues, saturation moyenne | Lisse, net, bords doux |
| **Mouvement / Transformation** | Lumière directionnelle qui "guide" le regard | Travelling mental (lignes de fuite, profondeur de champ marquée) | Lignes courbes, spirales, flux, espace devant le sujet | Dégradés progressifs, couleurs qui "migrent" | Flou de mouvement sélectif, net/flou contrasté |
| **Précision / Rigueur** | Lumière studio, uniforme, sans ambiguïté | Frontal, orthogonal, cadrage serré | Grille stricte, alignements, espacement régulier | Palette froide, gris + 1 accent, contraste net | Ultra-net, pas de grain, bords chirurgicaux |
| **Organique / Naturel** | Lumière naturelle, golden hour, contre-jour doux | Plan large ou macro extrême (pas de milieu) | Asymétrie naturelle, règle des tiers, espace négatif généreux | Tons chauds, terreux, désaturés, analogues | Grain filmique léger, bords doux |
| **Rupture / Disruption** | Éclairage dramatique, néon, couleur artificielle | Grand angle déformant, très gros plan, angle impossible | Fragmentation, collage, superposition, hors-cadre | Couleurs non-naturelles, duotone, surexposition | Grain fort, artefacts assumés, textures brutes |
| **Luxe / Premium** | Lumière sculpturale, reflets contrôlés, halo subtil | 3/4 avec profondeur, bokeh maîtrisé | Espace négatif dominant (60%+), sujet isolé, minimalisme | Palette sombre + or/cuivre/argent, saturation basse | Net avec micro-texture matière (cuir, métal, soie) |
| **Proximité / Humain** | Lumière douce latérale, fenêtre naturelle | Portrait cadré poitrine ou plan américain, regard caméra | Règle des tiers, sujet dominant, fond simplifié | Tons chair fidèles, balance chaude, contraste doux | Grain filmique modéré, peau naturelle |
| **Technologie / Innovation** | Rétro-éclairage, lumière bleue/froide, reflets spéculaires | Isométrique ou vue 3/4 plongeante | Lignes de perspective convergentes, motifs répétitifs, profondeur | Palette froide (bleu, cyan, violet), haute saturation accent | Ultra-net, lisse, pas de grain |
| **Héritage / Tradition** | Lumière Rembrandt, clair-obscur classique, chaleur ambrée | Cadrage classique, plan moyen, stabilité | Composition triangulaire, symétrie architecturale, frontalité | Sépia, tons chauds désaturés, palette restreinte | Grain filmique fort, vignettage, bords sombres |

### Comment utiliser ce tableau

1. Identifier le **registre émotionnel dominant** du concept narratif (la métaphore)
2. Croiser avec le **secteur du brief** pour ajuster (ex: "Tension" pour une banque ≠ "Tension" pour un label musical — même direction, intensité différente)
3. Le curseur A module l'**intensité** : A=1 reste sage dans le registre, A=3 pousse vers l'extrême

---

## 2. PRINCIPES DE COMPOSITION POUR VISUELS DE MARQUE

Ces principes ne sont pas des règles de photo génériques — ils sont adaptés au contexte spécifique BIG : les visuels seront intégrés dans un style-tile HTML où du texte, des CTA et des éléments UI coexistent avec l'image.

### 2.1 — Espace négatif intentionnel

Un visuel de marque n'est pas une photo d'art autonome. Il doit **laisser de la place** aux éléments qui viendront se superposer (titre, baseline, CTA).

| Usage prévu | Où placer l'espace négatif | Prompt : comment le demander |
|-------------|---------------------------|------------------------------|
| Full-bleed hero | Zone supérieure-gauche OU inférieure (pour overlay texte) | "vast negative space in upper left quadrant", "atmospheric sky/gradient occupying top third" |
| Split hero | Rien — le sujet DOIT occuper son panneau | Pas de mention d'espace négatif — sujet plein cadre |
| Background texture | Partout — le visuel EST l'espace | "seamless", "no focal point", "even distribution" |
| Clip-path / masque | Sujet centré avec fond simple (sera découpé) | "isolated subject", "clean background", "strong silhouette" |

### 2.2 — Lignes de force et direction du regard

Les lignes dominantes de l'image guident l'œil. Dans un style-tile, elles doivent guider vers le contenu de marque (titre, CTA), pas en dehors.

- **Lignes vers l'intérieur** (convergentes vers le centre/texte) → BIEN pour hero
- **Lignes vers l'extérieur** (divergentes vers les bords) → BIEN pour atmosphere block (expansion)
- **Lignes diagonales** → dynamisme, tension — cohérent avec curseur A ≥ 2
- **Lignes horizontales** → calme, stabilité — cohérent avec A=1

### 2.3 — Contraste figure/fond pour la lisibilité

Quand du texte sera posé sur l'image (overlay), le visuel doit avoir des zones de **contraste prévisible** :

- **Zone sombre uniforme** → texte clair lisible → prompt : "deep shadows in [zone]", "dark gradient toward [direction]"
- **Zone claire uniforme** → texte sombre lisible → prompt : "bright overexposed area in [zone]", "soft light flooding [direction]"
- **Zone texturée/complexe** → texte ILLISIBLE sans overlay CSS → à éviter dans les zones de texte

### 2.4 — Échelle et recadrage

Le visuel sera affiché à différentes tailles et potentiellement recadré (clip-path, aspect-ratio différent). Il doit survivre au recadrage :

- **Sujet centré** → survit à tout recadrage → le plus sûr
- **Sujet en tiers** → survit au recadrage horizontal, pas vertical → bon pour split
- **Sujet sur un bord** → risque de perte au recadrage → uniquement si usage connu et fixe

---

## 3. USAGE PRÉVU → TYPE D'IMAGE À PROMPTER

C'est la section la plus critique. Le même concept peut donner des images TRÈS différentes selon comment elles seront utilisées dans le style-tile. **Décider l'usage AVANT de prompter.**

### Matrice usage × caractéristiques

| Usage dans le style-tile | Composition de l'image | Sujet | Fond | --ar recommandé | Densité de détails |
|--------------------------|----------------------|-------|------|-----------------|-------------------|
| **Full-bleed hero** (image = le fond entier) | Large, atmosphérique, pas de point focal unique | Abstrait ou scène large, PAS un objet isolé | Le fond EST le sujet (ciel, texture, paysage, gradient naturel) | 16:9 ou 21:9 | Faible à moyenne — les détails seront sous le texte |
| **Split hero** (image dans une moitié) | Sujet fort d'un côté, composition asymétrique | Objet, personne, ou scène avec poids visuel clair | Secondaire, simplifié, peut être flou | 3:4 ou 4:5 (portrait) | Moyenne à haute — l'image est vue à 100% |
| **Clip-path / masque** (forme découpée) | Sujet isolé sur fond simple, forte silhouette | Objet avec contours nets et reconnaissables | Uni ou très simple (sera coupé) | 1:1 ou 4:3 | Haute — la forme découpée attire l'attention |
| **Fond texture / pattern** | Répartition uniforme, pas de hiérarchie, abstrait | Pas de sujet — texture pure (matière, tissu, grain, eau) | N/A — tout est fond | 16:9 | Faible et uniforme — c'est un fond |
| **Overlay blend-mode** (image mélangée à la couleur) | N'importe — le blend-mode va transformer | Fonctionne mieux avec des contrastes forts (noir/blanc) | Peu importe — sera fondu | 16:9 | Contraste > détail — les nuances seront perdues |
| **Collage / multi-crops** (plusieurs découpes) | Plusieurs zones d'intérêt distinctes | Scène riche avec des détails isolables | Varié — chaque zone sera extraite | 3:2 ou 16:9 | Haute — on va zoomer dans les zones |

### Règle d'or

> **Ne prompte JAMAIS une image sans savoir comment elle sera utilisée.**
> Un visuel "générique beau" n'existe pas. Un bon visuel de marque est un visuel CONÇU pour son emplacement.

---

## 4. CALIBRAGE PAR CURSEUR A

Le curseur A (Audace) ne change pas seulement les techniques CSS — il change le TYPE de visuel approprié.

| Curseur | Type de visuel | Traitement | Prompt keywords |
|---------|---------------|-----------|-----------------|
| **A=1** (Prudent) | Photo stock premium, lifestyle épuré, illustration flat propre | Propre, lumineux, professionnel, pas de grain, pas d'effet | "clean", "professional", "bright", "editorial", "minimal" |
| **A=2** (Décalé) | Photo éditorial/mode, illustration stylisée, macro matière | Direction artistique visible, parti pris de lumière ou couleur | "editorial", "moody", "dramatic lighting", "stylized", "artistic" |
| **A=3** (Rupture) | Art conceptuel, abstrait, surréalisme, expérimental | Grain, distorsion, couleur non-naturelle, composition cassée | "surreal", "experimental", "abstract", "distorted", "unconventional", "raw" |

---

## 5. COHÉRENCE MULTI-IMAGES D'UN MÊME CONCEPT

Quand on génère 2-3 images pour un même concept, elles doivent sembler venir du **même univers visuel**. C'est le rôle de l'ancre stylistique (voir framework MJ/Recraft). Mais au-delà de l'ancre technique, le DA vérifie :

### Checklist de cohérence

- [ ] **Température de lumière** identique (pas un chaud + un froid)
- [ ] **Niveau de grain/netteté** identique (pas un filmique + un ultra-net)
- [ ] **Palette** compatible (les couleurs dominantes se répondent)
- [ ] **Niveau d'abstraction** cohérent (pas un réaliste + un abstrait)
- [ ] **Registre émotionnel** aligné (pas un serein + un dramatique)

### Variation autorisée entre images d'un même concept

Seuls le **SUJET** et la **COMPOSITION** varient :
- Image 1 : scène large (hero atmosphérique)
- Image 2 : détail/macro (texture, matière)
- Image 3 : mise en situation (lifestyle, contexte d'usage)

Le traitement artistique (touche, lumière, grain, bords, abstraction) reste **identique** — c'est l'ancre.

---

## 6. ANTI-PATTERNS VISUELS

### Ce qu'un DA ne valide jamais

| Anti-pattern | Pourquoi c'est mauvais | Exemple |
|-------------|----------------------|---------|
| **Photo stock générique** | Aucun signal de marque, interchangeable | Main qui tient un stylo devant un laptop |
| **Visuel littéral du secteur** | Ventre Mou — tous les concurrents ont la même image | Stéthoscope pour la santé, engrenages pour l'industrie |
| **Visuel déconnecté du concept** | L'image ne raconte pas la même histoire que la marque | Concept "enracinement" + photo aérienne de ville |
| **Surproduction artificielle** | Trop retouché, trop parfait, impression "IA" | Skin smoothing excessif, HDR poussé, reflets impossibles |
| **Complexité visuelle partout** | L'œil ne sait pas où se poser, fatigue visuelle | 3 images toutes très détaillées et chargées |
| **Même cadrage × 3** | Monotonie, pas de rythme visuel | 3 plans moyens frontaux |

### Le test du "Ventre Mou visuel"

Comme pour le Ventre Mou sectoriel dans BIG : si l'image pourrait convenir à n'importe quel concurrent du même secteur → c'est du Ventre Mou visuel. L'image doit porter la **spécificité du concept narratif**, pas juste le secteur.

---

## 7. CE QUE L'ANALYSE VISUELLE DOIT CONTENIR (et ne pas contenir)

Le skill Visual Brief **décrit** les propriétés visuelles de l'image. Il ne **prescrit PAS** comment l'intégrer dans le style-tile — cette décision appartient au subagent Phase 4, qui a le pitch et le concept sous les yeux.

### L'analyse DOIT contenir (description factuelle de l'image)
- **Palette dominante** : couleurs HEX + proportions
- **Zones sombres/claires** : localisation + est-ce qu'un texte serait lisible dessus ?
- **Bords** : transition douce, nette, ou texturée
- **Composition** : lignes de force dominantes (verticales, diagonales, cercles...)
- **Zone focale** : où est le sujet principal
- **Mood** : chaud, froid, dramatique, doux...
- **Grain** : net, filmique, granuleux, lisse

### L'analyse NE DOIT PAS contenir (prescription d'intégration)
- ~~Pattern recommandé~~
- ~~Placement (Voice Block / Atmosphere)~~
- ~~Technique CSS clé~~
- ~~Zone texte recommandée~~

**Pourquoi** : Le skill Visual Brief n'a pas le contexte du pitch. Il ne sait pas si la composition Voice Block est "Superposition" ou "Split", ni si l'atmosphère est sombre ou claire. Prescrire un pattern d'intégration sans ce contexte mène à des conflits (ex: l'analyse prescrit "hero split" alors que le pitch prescrit "minimaliste radical").
