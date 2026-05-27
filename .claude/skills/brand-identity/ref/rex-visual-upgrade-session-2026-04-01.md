# REX — Session d'optimisation visuels BIG (1-2 avril 2026)

Session marathon de 2 jours. Suite directe de la session 30 mars - 1er avril (Axe 1 visuels). Cette session traite les Axes 2 (CSS/composition) et 3 (layout/taille).

---

## CONTEXTE DE DÉPART

Score estimé avant session : ~7.5/10. Cible : 9-10/10 (niveau Awards).

### Ce qui avait été fait (session précédente, 30 mars)
- Axe 1 (qualité des visuels eux-mêmes) traité : penseur visuel, skill `/visual-brief`, règles visibilité images
- Audit de 88 sites Awards avec stats de layout (stacked 27%, full-bleed 23%, split 19%)
- Identification des 3 gaps principaux : layout monotone, pas de layering, surfaces plates

### Ce qui restait à faire
- Axe 2 : techniques CSS (layering texte/image, 3ème couche, surfaces enrichies, post-traitement)
- Axe 3 : layout et taille (variété des layouts, taille typo, taille du visuel)

---

## CE QUI A ÉTÉ FAIT

### 1. Prompt Phase 4 renforcé (`phases/phase-4-styletile.md`)

**3 règles ajoutées au socle "FINITION ÉLITE" :**

a) **Typo hero ≥ 8vw** : `font-size: clamp(4rem, 8vw, 12rem)` minimum pour le H1. Exception : stacked centré peut descendre à 4-5vw.

b) **Fond texturé obligatoire** : chaque section doit avoir de la profondeur. Sur fond SOMBRE : grain SVG + au moins 1 radial-gradient coloré visible (opacity ≥ 0.10). Sur fond CLAIR : grain subtil + radial-gradient suffit. Un aplat seul = interdit.

c) **Dialogue texte/image obligatoire** : si images fournies, au minimum un gradient de liaison + un point de contact visuel (z-index, chevauchement, overlap). Le "split muet" (texte et image séparés) = interdit.

### 2. Penseur visuel enrichi (`phases/phase-3b-penseur-visuel.md`)

**4 ajouts :**

a) **Principe soustractif** (défaut) : un sujet, une lumière, rien d'autre. La matière du sujet EST la texture.

b) **Principe de densité intentionnelle** : deux stratégies valides (densité matière bord à bord OU espace négatif maîtrisé). Le vide SUBI (flou atmosphérique ni dense ni intentionnel) = interdit.

c) **Règle de concrétude** : les prescriptions techniques doivent être au niveau d'un prompt de génération. Format : "{sujet} en {cadrage}, {texture}, {lumière}". Les formulations narratives abstraites = interdites.

d) **Volet COMPOSITION dans l'analyse étalon** (étape 6a-bis) : en plus du craft, analyser comment les étalons intègrent le visuel dans le hero (layout, hiérarchie, layering, liaison). Nouveau champ "Intégration recommandée" dans le format de sortie de l'Image 1 Hero.

### 3. Squelettes CSS ajoutés (`ref/css-patterns-phase4.md`)

**2 nouveaux Voice Block patterns :**

- **VB-9 : Stacked** (~80 lignes) — texte centré en haut, image en dessous qui émerge dans le viewport. Techniques : @starting-style, mask-image, @property animé, color-mix.
- **VB-10 : Full-bleed overlay** (~90 lignes) — image absolute inset:0, texte en bas z-index:2, gradient de lisibilité directionnel. Techniques : mix-blend-mode, mask-image, @property, backdrop-filter, @starting-style.

Les 8 squelettes existants (VB-1 à VB-8) sont INTACTS.

### 4. Menu penseur design élargi (`phases/phase-3b-design.md`)

Ajout de "Stacked" et "Full-bleed overlay" dans le menu des compositions (qui passe de 9 à 11 options).

### 5. Mapping orchestrateur mis à jour (`SKILL.md`)

- Stacked et Full-bleed overlay ajoutés dans la liste des types reconnus pour `{css_pattern_block}`
- Ajoutés aussi dans la règle de diversité inter-concepts

### 6. Swap 3C ↔ 3B-5 : visuels AVANT pitch

**Changement d'orchestration majeur :**
- AVANT : 3B-4 (direction visuelle) → 3B-5 (pitch) → 3C (visuels)
- APRÈS : 3B-4 (direction visuelle) → 3B-5 (visuels) → 3B-6 (pitch)

**Pourquoi** : permet d'itérer sur les visuels AVANT de créer le pitch. Si Recraft ne produit pas un bon résultat pour le type de visuel prescrit, on peut changer la direction et retester sans avoir à refaire le pitch.

**Modification du visual-brief** : refactorisé pour lire les `palette-c*.md` + `visual-direction-c*.md` au lieu des pitches (qui n'existent plus à ce stade). La dépendance aux pitches est cassée.

### 7. Awards screenshots dans Phase 4

**Nouveau bloc `{awards_etalon_block}`** injecté dans le prompt Phase 4 :
- L'orchestrateur vérifie si des fichiers `etalon-*.png` existent dans le dossier de session
- Si oui, les encode en basse résolution et les injecte avec une directive anti-contamination
- Le subagent Phase 4 VOIT les étalons et peut calibrer son niveau d'intégration

### 8. Phase 4B DA Check enrichi (`phases/phase-4bis-da-check.md`)

**Axe 4 — Niveau élite** ajouté :
- Si des étalons Awards sont dans le dossier de session, le subagent DA les lit
- Compare la profondeur de surface, l'intégration image, l'impact typographique, la densité intentionnelle
- Prescrit des corrections si en dessous du niveau des étalons

### 9. 6 exemples HTML refaits avec images

**Distribution finale :**

| Exemple | Curseur | Layout | Image hero |
|---------|---------|--------|------------|
| A (Clarity Analytics) | A=1 | Split asymétrique 55/45 | Réseau géométrique lumineux |
| F (Domaine des Music) | A=1 | Stacked | Structure cellulaire mousse/plante |
| B (Maison Solène) | A=2 | Stacked | Papier luxueux roulé |
| E (Méridien Labs) | A=2 | Full-bleed overlay | Grille topographique 3D |
| C (Archipel Studio) | A=3 | Full-bleed overlay | Béton brut macro |
| D (Fréquence Noire) | A=3 | Stacked | Ondes sonores néon |

**Méthodologie qui a fonctionné** : les heroes ont été codés par des subagents Phase 4 (pas manuellement). Chaque subagent a reçu un mini-pitch + l'image + les contraintes CSS élite. Le CSS est au niveau BIG (oklch, @layer, @property animé, clip-path, mask-image, etc.). Puis les sections artefact/atmosphere des exemples ORIGINAUX (restaurés depuis git) ont été fusionnées avec les heroes via Python (le hero comme base, artefact/atmosphere ajoutés).

**Méthodologie qui n'a PAS fonctionné** : modifier les exemples existants avec des regex (CSS bricolé, proportions cassées, fusions qui détruisent le CSS). Modifier manuellement les heroes après génération les dégrade systématiquement.

**KPI cards retirées** : la `summary-bar` de l'exemple A (4 KPI cards "overline + gros chiffre + label") a été supprimée. Pattern le plus copiable identifié.

### 10. Test-big : phases renommées + renumérotées

Ancien : 3B-4 → 3B-5 → 3C → 4
Nouveau : 3B-4 → 3B-5 → 3B-6 → 4

Noms clarifiés avec outputs entre parenthèses (ex: "Direction visuelle du penseur (type de visuel, ancre stylistique, prescriptions techniques, intégration recommandée)").

### 11. Skill `/audit-elite` créé

Agent juge impitoyable qui compare les style-tiles aux étalons Awards. Workflow : analyse des étalons → analyse du code CSS → comparaison sur 8 axes → diagnostic avec prescriptions actionnables. Invocation : `/audit-elite`.

---

## DÉCOUVERTES ET LEÇONS APPRISES

### Découverte 1 — Les exemples n'avaient AUCUNE image
5 des 6 exemples HTML étaient purement typographiques/CSS. Le subagent Phase 4 n'avait jamais VU un modèle d'intégration image dans un hero. Le pattern "Code > Rules" jouait CONTRE nous pour l'image.

### Découverte 2 — Concrétude et principe soustractif
Lors d'un test rapide de génération d'images (10 images pour les exemples), on a produit des visuels quasi-étalon en quelques minutes. Analyse :
- **Facteur A (reproductible)** : les prescriptions étaient au niveau de concrétude d'un prompt Recraft ("béton brut en macro, veinage visible, lumière latérale") au lieu de narratif abstrait ("capture la solidité pérenne").
- **Facteur B (reproductible)** : le principe soustractif ("un sujet, une lumière, rien d'autre") — identifié dans les Awards.
- **Facteur C (non reproductible)** : l'absence de contraintes narratives (pas de brief, pas de territoires, pas de ventre mou). Le pipeline réel impose des contraintes qui limitent le champ mais assurent la pertinence.

### Découverte 3 — Les squelettes CSS ne couvraient pas les layouts Awards
Les 2 layouts les plus fréquents aux Awards (Stacked 27%, Full-bleed overlay 23%) n'avaient PAS de squelette CSS ni d'option dans le menu du penseur design. Le système ne pouvait pas les prescrire.

### Découverte 4 — Le subagent ne VOIT PAS le rendu
Le subagent Phase 4 lit le code HTML/CSS en texte. Il ne voit pas le rendu visuel. Ce qui compte pour lui, c'est le NIVEAU TECHNIQUE du code (oklch, @property, clip-path), pas l'apparence. Les exemples doivent être bons en CODE, pas juste en visuel.

### Découverte 5 — Modifier les exemples avec des regex les dégrade
Chaque tentative de correction CSS par regex (changer une font-size, un padding, un gradient) a dégradé le résultat. La raison : les regex touchent le mauvais sélecteur, les proportions cascadent de façon imprévisible, et on ne voit pas le résultat. La seule approche qui a fonctionné : faire recoder les heroes par des subagents Phase 4 qui produisent du CSS cohérent d'un seul tenant.

### Découverte 6 — Les proportions stacked Awards
Les stacked Awards (Flighty, Wone, Hear) ont des proportions précises :
- Texte : ~40-45% du viewport (titre ~4-5vw en centré, pas 8vw)
- Image : ~50-55% du viewport, visible immédiatement
- Transition : douce (gradient 15-20%), PAS brutale
- Padding top : confortable (~5-8vh), pas écrasé
- Espacement : confortable entre les éléments, pas tassé

### Découverte 7 — La densité intentionnelle n'est PAS universelle
La règle "le sujet remplit 90% du cadre" (type ICOMAT) n'est PAS universelle. 4 des 7 étalons Awards ont du vide intentionnel (MOAK, LiquidSolar, GlyphicBio, Anima). La bonne règle : chaque zone est soit matière dense soit espace négatif maîtrisé. Le vide SUBI (ni l'un ni l'autre) = interdit.

### Découverte 8 — Les KPI cards sont le pattern le plus copiable
Le pattern "overline + gros chiffre + label" dans les artefacts d'exemples est reproduit verbatim par le subagent, quel que soit le type d'artefact du concept. Solution : n'utiliser que des artefacts "exotiques" (data tables, schedule grids) dont la structure est inapplicable à d'autres contextes.

---

## CE QUI MARCHE BIEN (résultats des tests)

### Test VoltaPilot (Phase 4 seule)
- Score avant : 6.5/10 (split basique, pas de layering, fond plat)
- Score après : 7.5-8/10 (composition plus riche, textures, typo plus grande)
- Le subagent a produit du "Superposition" (composition prescrite par le pitch pré-existant) au lieu du full-bleed overlay souhaité → normal car le pitch venait de l'ancien système

### Test VoltaPilot (Phase 3B-4 + 3B-5 + 3B-6 + 4)
- Le penseur visuel a prescrit du "macro expérimental sur surface organique" (concret, pas narratif)
- Les visuels générés sont à 7-8/10 (vs 6.5 pour le prisme de la session précédente)
- Le principe soustractif et la concrétude se voient dans les prescriptions
- Le style-tile final : meilleur que le premier test mais le layout reste limité par les étalons pas encore injectés

---

## CE QUI NE MARCHE PAS ENCORE / ENJEUX OUVERTS

### 1. Les exemples stacked (B et D)
Les proportions stacked sont difficiles à calibrer. Après de nombreuses itérations, les proportions sont "correctes" mais pas encore au niveau Flighty/Wone. La transition texte→image est le point le plus délicat. Les heroes standalone fonctionnent, la fusion avec les artefacts/atmospheres est fragile.

### 2. Le clip-path et @starting-style manquants sur certains exemples
- F (A=1) n'a pas de clip-path (acceptable pour A=1 structuré)
- B et D n'ont pas de @starting-style (manque d'animations d'entrée)
Risque : 1 projet sur 2 recevra un exemple sans ces techniques → le subagent ne les reproduira pas.
Décision : on laisse tel quel pour l'instant. Le prompt Phase 4 exige un quota de techniques avancées qui force le subagent à en utiliser d'autres.

### 3. L'agent `/audit-elite` n'a pas encore été testé
Créé mais pas validé en conditions réelles. À tester sur un style-tile existant.

### 4. La non-répétition de layout entre les 3 concepts
Discutée mais reportée. Quand 3 concepts sont générés, ils peuvent tous être en split. Une règle de diversité pourrait forcer : au moins 2 layouts différents parmi les 3.

### 5. L'espace négatif comme levier
Identifié comme levier #5 dans le rapport, discuté en détail (analogie vitrine Apple), mais pas implémenté dans le prompt ni les exemples. À traiter dans une session future.

---

## FICHIERS MODIFIÉS (exhaustif)

| Fichier | Modification |
|---------|-------------|
| `phases/phase-4-styletile.md` | +3 règles socle (typo, texture, dialogue) + section Awards étalons + règle texture fonds sombres renforcée |
| `phases/phase-3b-penseur-visuel.md` | +principe soustractif + densité intentionnelle + concrétude + volet composition étalon + champ "Intégration recommandée" |
| `phases/phase-3b-design.md` | +2 options menu (Stacked, Full-bleed overlay) |
| `phases/phase-4bis-da-check.md` | +Axe 4 niveau élite |
| `ref/css-patterns-phase4.md` | +VB-9 Stacked + VB-10 Full-bleed overlay |
| `SKILL.md` | +mapping VB-9/VB-10, +Awards étalon block, +swap 3C↔3B-5, +diversité composition |
| `examples/standard/style-tile-example-A.html` | Hero refait (split, réseau géométrique), KPI cards retirées |
| `examples/standard/style-tile-example-B.html` | Hero refait (stacked, papier luxueux) |
| `examples/standard/style-tile-example-E.html` | Hero refait (full-bleed, grille topo) |
| `examples/standard/style-tile-example-F.html` | Hero refait (stacked, mousse organique) |
| `examples/rupture/style-tile-example-C.html` | Hero refait (full-bleed, béton brut) |
| `examples/rupture/style-tile-example-D.html` | Hero refait (stacked, ondes néon) |
| `.claude/skills/visual-brief/SKILL.md` | Refactorisé : lit palettes + visual-directions au lieu des pitches |
| `.claude/skills/test-big/SKILL.md` | Phases renumérotées (3B-5, 3B-6), noms clarifiés, ordre mis à jour |
| `.claude/skills/audit-elite/SKILL.md` | CRÉÉ — skill agent juge impitoyable |
| `ref/rapport-gap-visual-elite.md` | CRÉÉ — rapport complet des 8 leviers avec exemples Awards |

## FICHIERS CRÉÉS (non versionnés, dans outputs/)

| Fichier | Contenu |
|---------|---------|
| `outputs/hero-tests/hero-{A,B,C,D,E,F}-*.html` | Heroes standalone générés par subagents Phase 4 |
| `outputs/Visuels pour exemples HTML/` | 10 images Recraft pour les exemples |
| `outputs/Visuels pour exemples HTML/resized/` | Versions 800px JPEG + base64 |
| `outputs/Exemples Awards macro-abstract/` | Screenshots Awards étalons (ICOMAT, POUCH, etc.) |
| `outputs/pattern-demo/` | Audit des 88 sites Awards (session précédente, réutilisé) |

---

## PROCHAINES ÉTAPES (pour la session suivante)

1. **Tester** : relancer un test Phase 4 complet avec les nouveaux exemples + Awards étalons + prompt renforcé
2. **Tester `/audit-elite`** : invoquer sur un style-tile existant, vérifier que le diagnostic est actionnable
3. **Itérer les exemples stacked** (B et D) : les proportions sont correctes mais pas encore élite
4. **Ajouter @starting-style et clip-path** aux exemples qui en manquent (si faisable sans casser)
5. **Non-répétition layout** : implémenter la règle de diversité entre les 3 concepts
6. **Espace négatif** : ajouter au prompt Phase 4 ou au penseur visuel
7. **Commit** : commit massif de tous les changements

## Dernière mise à jour : 2026-04-02
