# Master Style Guide — Les 9+1 Piliers de l'Identité

Ce document est le **"Système d'Exploitation"** du BIG. Il définit les standards de sortie pour transformer un brief marketing en une identité de classe mondiale.

---

## PARTIE A : PROTOCOLE D'INTÉGRITÉ

### Le Filtre d'Audit (Quality Gate)

Chaque élément produit doit valider ces 4 filtres :

1. **Cohérence de Différenciation** : L'élément respecte strictement le score du Curseur B
2. **Scalabilité Totale** : Efficacité du 16px au billboard 4K
3. **Clarté & Gestalt** : Hiérarchie immédiate et sans friction
4. **Intégrité Systémique** : Résonance entre les fondations (01) et l'exécution

### Séquence de Production

| Étape | Nom | Points | Scope |
|-------|-----|--------|-------|
| **Step 0** | La Fondation | 01 | V1 |
| **Batch 1** | L'ADN Visuel | 02, 03 | V1 |
| **Batch 2** | Le Système de Signes | 04, 05, 06, 07 | V2 |
| **Batch 3** | La Narration & L'Espace | 08, 09, 10 | V2 |

---

## PARTIE B : LES 9+1 PILIERS

### [STEP 0] — LA FONDATION (V1)

#### 01. Fondations Stratégiques & Territoire de Marque (The Soul)

C'est le **socle immuable** sur lequel tout repose.

- **Calibration Stratégique (The Intensity Matrix)** : Scores des curseurs A et B avec justification
- **L'Intention Créative (The Big Idea)** : Synthèse de la résolution de la Tension de Marque — comment le design va incarner les deux pôles contradictoires
- **Le Territoire Sémantique (The Mental Slot)** : Les 3 concepts-clés piliers qui définissent l'espace mental de la marque
- **Tone of Voice & Messaging** : Personnalité, vocabulaire privilégié, rythme éditorial, mots interdits
- **L'Ancre de Posture** : Analogie opérationnelle (ex: "L'Ingénieur Invisible", "Le Gardien Silencieux")

---

### [BATCH 1] — L'ADN VISUEL (V1)

#### 02. Color System & Hiérarchie Chromatique (The Color DNA)

Le système de couleurs est l'**empreinte émotionnelle** de la marque.

- **Primary Brand Scale** : Couleur d'autorité — 3 teintes (light, base, dark)
- **Secondary & Accent Scale** : Couleur d'énergie (CTA) — 3 teintes
- **Neutrals & Surfaces** : 5 nuances de gris/neutres pour la structure
- **Semantic & Status** : Success, Error, Warning, Info
- **Data-Viz Palette** : 4 couleurs harmonisées pour les KPI et graphiques
- **Compliance WCAG 2.1** : Test de contraste obligatoire (AA minimum, AAA visé)

**Indexation Curseur B** : Score B=3 → palette en rupture avec les codes sectoriels

#### 03. Typographie & Rythme Éditorial (The Voice)

La typographie est la **voix visuelle** de la marque.

- **Le Pairing Stratégique** : Duo Display (Caractère, émotion) + Body (Performance, lisibilité) — Google Fonts obligatoire
- **L'Échelle Modulaire (Type Scale)** : Ratio de progression **indexé sur le Curseur A**
  - A=1 : ratio ≤ 1.200 (Minor Third) — progression douce, classique
  - A=2 : ratio 1.250–1.333 (Major Third / Perfect Fourth) — contrastes marqués
  - A=3 : ratio ≥ 1.414 (Augmented Fourth+) — hiérarchie dramatique
- **Rôles Fonctionnels** : H1 (Hero), H2 (Section), H3 (Card), Body, Overline, Lead, Data/Mono, Caption
- **Directives de Lisibilité** : Interlignage (leading), espacement (tracking), longueur de ligne max

**Indexation Curseur A** : Score A=3 → display expérimental, variable fonts autorisées

#### 04. Code Civil Atomique (The Surface Logic)

Les micro-décisions de surface qui donnent sa **texture physique** à la marque.

- **Système d'Arrondis (Radius Logic)** : Le concept détermine la philosophie. Minimum 2 niveaux pour la hiérarchie visuelle. Valeurs et noms libres.
- **Élévation & Profondeur (Shadow System)** : Le concept détermine le vocabulaire d'élévation. Le nombre de niveaux est libre (de 0 à N). Philosophies possibles : portées classiques, inset/deboss, colorées, flat.
- **Gradients & Blending Logic** : Angles, types et intensité libres — guidés par le concept.
- **Épaisseurs & Tracés** : Lignes de précision (1px/1.5px pour les séparateurs, 2px pour les borders actifs)
- **Grille de Rythme** : Unité de base (4px ou 8px) pour tous les espacements

**Indexation Curseur A** : Le score A détermine l'intensité et la singularité des choix surface, pas leurs valeurs exactes

---

### [BATCH 2] — LE SYSTÈME DE SIGNES (V2)

#### 04. Code Civil Atomique : Composants UI (documentation visuelle)

La documentation visuelle des composants UI qui assemblent les tokens du Code Civil :
- **04.1 Buttons** : Primary (fond plein) et Secondary (outline/ghost), avec états default/hover/active/disabled
- **04.2 Form Elements** : Input, Toggle, Checkbox, Select — état default + actif
- **04.3 Badges & Statuts** : 4 variantes sémantiques (success/warning/error/info)
- **04.4 Cards & Containment** : Radius, shadow multi-layer, fond distinct, hover
- **04.5 Feedback & Navigation** : Alert, Progress indicator, Tab bar, Avatar

Source de vérité : l'artefact témoin du style-tile (`.artifact-witness`). Les composants sont extraits et documentés isolément.

#### 05. Logotype & Morphologie du Signe (The ID)
- Concept & Symbolique (justification sémiotique)
- Système de Lockups (Primaire, Secondaire, Icon-Only)
- Zone d'Exclusion & Lisibilité (Safe Area, tailles min)
- Variantes de Contexte (Positif, Négatif, Monochrome, OLED)

#### 06. Iconographie (The Symbols) — refonte D59 (2026-05-27)
- **06.1 Le set d'icônes UI** : 18-22 icônes utilisables (10-12 UI primaire + 4-6 UI métier + 4 statuts sémantiques), dans le traitement principal natif de la famille assignée par le routeur 6A-0
- **06.2 Traitements alternatifs** : 1-2 traitements (max), chacun étiqueté avec son cas d'usage business explicite (état normal / état actif / éventuellement variante dense)
- **06.3 Usage en contexte** : 1 mini-mockup (squelette imposé : sidebar / table+toolbar / toolbar / breadcrumb / list / nav) qui montre 4-6 icônes du set en condition réelle, en contraste actif vs inactif

**Famille graphique** : choisie par le routeur Phase 6A-0 parmi 8 candidates documentées dans `ref/icon-system/catalogue/` (pictogramme géométrique propre, isométrique, pixel art, gravure/linocut, ornemental art déco, flat illustré coloré, sticker/cut-out, brutaliste/ASCII). Chaque famille a sa fiche slop/anti-slop dans `ref/icon-system/slop-sheets/`. La nomenclature "Outline / Solid / Duotone" (héritage Heroicons) est NATIVE d'UNE seule famille (pictogramme géo) et n'est plus imposée par défaut — chaque famille a ses propres traitements natifs.

#### 07. Data Visualization & Evidence (The Truth)
- Style des Graphiques (interpolation, finition barres)
- Système de Grilles & Axes (opacité gridlines)
- Usage de la Couleur (palette Data-Viz dédiée)
- Typographie de la Donnée (style Data/Mono strict)

---

### [BATCH 3] — LA NARRATION & L'ESPACE (V2)

> Les piliers 08-10 seront développés en V2. Structures préservées.

#### 08. Direction Narrative & Photographique (The Mood)
- Style Photographique (Documentaire vs Editorial, éclairage)
- Traitement Chromatique (Color Grading, grain)
- Scénographie Produit (devices, mockups)
- Signature de Prompting IA (mots-clés pour génération d'images)

#### 09. Système de Composition & Rythme (The Structure)
- Architecture de Grilles (indexée sur Curseur A)
- Stratégie de Densité (Negative Space, paddings)
- Patterns de Mise en Page (Hero Split, Bento Grid, Feature Grid)
- Rythme Vertical (alignement sur l'unité de base)

#### 10. Système d'Illustration Narrative (The Visual Story)
- Angle de Métaphore (Abstrait vs Figuratif)
- Physique de l'Illustration (contours, remplissages, textures)
- Character Design (proportions, attitude)
- Lois de Composition (cohabitation texte/image)
- Directives de Prompting IA (terminologie cohérente)
