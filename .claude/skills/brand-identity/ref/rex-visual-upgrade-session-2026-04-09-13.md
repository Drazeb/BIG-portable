# REX — Session 3ème couche graphique + artefact semi-standardisé (9-13 avril 2026)

Session de 5 jours. Suite des sessions précédentes (blacklists CSS, composition). Cette session traite la 3ème couche graphique décorative et la refonte de l'artefact.

---

## PROBLÈME DE DÉPART

Les style-tiles BIG sans visuels étaient pauvres en richesse graphique. Diagnostic (4 causes identifiées par les subagents Phase 4 eux-mêmes) :
1. **Biais de prudence** : le LLM sous-dose les patterns par peur de surcharger
2. **Priorisation structure > surfaces** : les textures/patterns traités comme bonus optionnel
3. **Substitution CSS au lieu de SVG** : gradients basiques au lieu de vrais SVG patterns
4. **Éléments omis par oubli** : séparateurs créatifs, mots en filigrane pas implémentés

---

## CE QUI A ÉTÉ FAIT — 9 COMMITS SUR MAIN

### Commit 1 — `603f1c6` : V1 couche graphique
- Section "COUCHE GRAPHIQUE DÉCORATIVE" ajoutée dans Phase 4 (6 catégories, seuils 3/4)
- Gate positif `check_graphic_layer_presence` dans blacklist-gate.py (premier check positif du système)
- Flag `--no-images` pour seuils rehaussés
- Suppression de l'interdiction SVG trop large ("INTERDICTION — NE PAS GÉNÉRER D'IMAGES")
- Gate 5 réécrit (data-visual only, plus d'interdiction SVG)
- "floating elements" reformulé → "particules en dérive infinie"
- ::before/::after : note ajoutée distinguant traits typo (interdit) de pseudo-éléments composition (OK)

### Commit 2 — `41553dc` : V2 parcimonie + opacité + SVG figuratif
- 6 catégories → 5 (brand watermark retiré comme catégorie)
- Seuils revus : 2 éléments de base obligatoires (grain + overlay) + additionnelles au choix
- Parcimonie : "2-3 éléments FORTS valent mieux que 6 fantômes"
- Seuil opacité ≥ 8% (hors grain)
- Check SVG figuratif : `<path>` >20 commandes + `<symbol>` >12 enfants → FAIL
- Accent bar pseudo-élément : détection ::before/::after narrow+tall+background

### Commit 3 — `c3a1c30` : Grain ≥ 8% + élément signature
- Grain opacity ≥ 8% appliqué dans le gate
- Élément signature obligatoire (avec ET sans images)
- "Fond texturé obligatoire" aligné avec les nouveaux seuils
- 4 exemples HTML (A, C, E, F) : grain monté de 0.07 à 0.10

### Commit 4 — `214b115` : REFACTOR ARTEFACT (majeur)
- Artefact séparé dans un subagent dédié (`phases/phase-4-artefact.md` créé)
- Structure semi-standardisée : panneau dominant + grille support + barre détails
- Workflow : Phase 4A (hero+zone médiane+atmosphere) → 4A-val (validation user) → 4A-art (subagent artefact) → 4A-art-gate
- Phase 3B : "STRATÉGIE D'ARTEFACT" → "STRATÉGIE DE DONNÉES MÉTIER" (prescrit les données, pas le type de composant)
- Artefact retiré des axes de divergence (5→4 axes)
- Variables `{concept_artefact_type}` et `{example_artefact_type}` retirées de Phase 4
- test-big : sous-étapes 4-val et 4-art ajoutées
- Les 6 exemples exotiques GARDÉS (anti-contamination = exemples structurellement différents)

### Commit 5 — `c0509e5` : Fix test-big
- Sous-étapes 4-val et 4-art ajoutées dans la liste de démarrage et les prérequis

### Commit 6 — `c158c1c` : Layout L artefact + opacités agressives
- Squelette CSS artefact : `grid-template-columns: 1fr` → `1.3fr 2fr` (layout en L)
- Panneau dominant en colonne gauche (pleine hauteur), grille+détails en colonne droite
- Opacités montées : grain ≥ 20%, patterns ≥ 20%, signature ≥ 25%
- Exemples A, C, D, E, F : grain monté à 0.22

### Commit 7 — `b69328e` : Grain tuilé 150px + seuils visuels calibrés + gate visuel
- **Technique grain obligatoire** : `background-image` data-uri + `background-size: 150px` (tuilé fin). SVG inline étiré (viewBox 400×400) INTERDIT (grain grossier/pixelisé)
- **Blend-mode** : `soft-light` obligatoire (pas overlay/multiply — trop atténuant)
- **Opacity grain** : 0.25-0.30
- Seuils d'opacité désormais CONTEXTUELS (dépendent du contraste lightness fond/élément)
- Formes : halos diffus ENCOURAGÉS, contours nets DÉCOURAGÉS
- **Gate visuel Puppeteer** ajouté dans SKILL.md (étape 3 du contrôleur) : screenshots par section + vérification visuelle

### Commit 8 — `ed0bd16` : Brand watermark retiré + clip-path interdit sur halos + grain 0.35-0.45 + crops ciblés
- **Brand watermark** : retiré des catégories admises (contaminant — 3/5 outputs, 1/21 Awards)
- **Clip-path sur halos** : INTERDIT (produit polygone flou amateur — 0/10 Awards l'utilisent sur les overlays)
- **Grain** : opacity montée à 0.35-0.45 (0.25-0.30 encore invisible en soft-light)
- **Gate visuel** : crops ciblés 400×400 au lieu de full-section 1440×900 (meilleure résolution pour le LLM)
- Gate vérifie aussi : absence de clip-path sur halos, absence de brand watermark

---

## DÉCOUVERTES FONDAMENTALES

### Sur la 3ème couche

1. **Les Awards ont soit AUCUNE 3ème couche (l'image suffit), soit une 3ème couche FORTE (≥25% opacity)**. Le "subtil discret à 8%" n'existe pas dans les Awards. C'était une invention de notre système.

2. **Le grain feTurbulence en overlay/multiply est invisible** même à 20-25%. Le blend-mode `overlay` atténue drastiquement l'opacité apparente. `soft-light` est meilleur mais nécessite ≥ 35% pour être perceptible.

3. **La technique de grain tuilé (background-image + background-size: 150px)** produit un grain fin. Le SVG inline étiré (viewBox 400×400 en width:100%) produit un grain grossier et pixelisé.

4. **La visibilité des patterns dépend du contraste lightness**, pas juste de l'opacité. Un dot-grid oklch(0.93 / 0.08) sur fond sombre (lightness 0.22) = TROP visible. Le même à oklch(0.45 / 0.08) = invisible. Le bon calibrage demande d'ajuster la lightness par rapport au fond.

5. **Le brand watermark (nom de marque en oversize semi-transparent) est ultra-contaminant** : listé comme option → apparaît 3/5 fois. Présent dans 1/21 sites Awards (POUCH). Retiré.

6. **Le clip-path sur les halos atmosphériques produit des polygones flous** amateurs. Aucun site Awards ne fait ça. Le subagent l'applique parce que le curseur A=3 dit "convention cassée = clip-path" et il l'applique partout.

7. **Les halos diffus (radial-gradient elliptiques sans contour net) sont le registre élite** pour les formes décoratives. Les formes à contour net (circles avec stroke, structures concentriques) produisent un résultat amateur.

### Sur l'artefact

8. **L'artefact créatif (composant métier spécifique) est le maillon faible** : qualité variable (5-6/10 vs 7-8/10 pour hero/atmosphere), forte dépendance au pitch ("Pitch > Exemples > Principes").

9. **L'artefact semi-standardisé avec subagent dédié** résout les 2 problèmes : finition fiable + couverture atomique systématique.

10. **L'empilement vertical** (5/5 artefacts empilés) est causé par le squelette CSS (`grid-template-columns: 1fr`). Le layout en L (1.3fr 2fr) casse l'empilement.

11. **Le contraste fort du panneau dominant n'est PAS un pattern Awards systématique**. Les composants Awards sont souvent monochromes. Le contraste vient de l'alternance entre SECTIONS, pas intra-composant.

### Sur le gate visuel

12. **Le Read tool affiche les images en miniature** (budget de tokens visuels). Un crop 1440×900 est compressé → les éléments subtils (grain, dots) sont invisibles. Un crop 400×400 ciblé utilise le même budget → meilleure résolution.

13. **Le gate visuel avec full-section crops NE FONCTIONNE PAS** pour les éléments subtils. Testé : le gate PASS mais le grain est invisible.

---

## RÉFÉRENCES — OÙ TROUVER LES ÉTALONS ET ANALYSES

### Captures Awards haute résolution
- **21 sites hero+full** : `.claude/skills/brand-identity/outputs/benchmark-awards-20260407/`
  - Sites : anima, caide, finsight, followart, futurelabel, gru, hear, icomat, junabase, kontenta, mazehq, meritfirst, mindjoin, muscatgroup, nory, ose-engineering, piplanning, qualytics, waabi, zeeframes, zerodrift
  - Format : `{site}-hero.png` + `{site}-full.png`

- **5 étalons macro** : `.claude/skills/brand-identity/outputs/test-voltapilot-test-20260402-1722/etalon-*.png`

- **Dossier pattern-demo** (88 sites Awards) : `outputs/pattern-demo/`

### Rapports et analyses
| Fichier | Contenu |
|---|---|
| `ref/rapport-gap-visual-elite.md` | 8 leviers d'optimisation, 10 heroes Awards analysés en détail |
| `ref/rex-visual-upgrade-session-2026-04-01.md` | REX session 1-2 avril (Axes 2+3 : CSS/composition + layout/taille) |
| `ref/rex-visual-upgrade-session-2026-04-04-08.md` | REX session 4-8 avril (blacklists CSS/composition, gates, exemples) |
| `ref/perplexity-composition-patterns-report.md` | Rapport 1 : patterns datés vs actuels |
| `ref/perplexity-composition-detail-report.md` | Rapport 2 : détail opérationnel |
| `ref/composition-blacklist-draft.md` | Draft blacklist composition (13 items → 9 validés) |
| `ref/interface-design-lens.md` | Principes d'interface + vocabulaire des compositions |

### Style-tiles de test (avec captures Puppeteer)
| Run | Dossier | Contenu |
|---|---|---|
| Test 10/04 (pré-artefact) | `test-{brand}-test-20260410-*` | 5 ST avec artefacts anciens |
| Test 11/04 (post-refactor artefact) | `test-{brand}-test-20260411-1903/` | 5 ST hero+atmo+artefact semi-standardisé |
| Test 12/04 (opacités agressives) | `test-{brand}-test-20260412-*` | 5 ST + versions BEFORE pour comparaison |
| Test 13/04 (dernière version) | `test-{brand}-test-20260413-*` | 5 ST avec grain tuilé + gate visuel |
| Clones artefact-v2 | `test-{brand}-test-artefact-v2/` | 3 dossiers avec pitchs reformatés (données métier) |

---

## ARTEFACT SEMI-STANDARDISÉ — État et cohérence avec Batch 2

### Architecture actuelle
- **Subagent dédié** (`phases/phase-4-artefact.md`) génère l'artefact APRÈS validation du hero+atmosphere
- **Structure semi-standardisée** en layout L (`grid-template-columns: 1.3fr 2fr`) :
  - Zone A (colonne gauche) : panneau dominant — chiffre display + label + badge
  - Zone B (colonne droite, haut) : grille de 3 cards métriques (tailles inégales, `align-content: start`)
  - Zone C (colonne droite, bas) : barre de détails — meta + bouton + input + toggle
- **Squelette CSS** : `ref/css-patterns-phase4.md`, section "ARTEFACT SEMI-STANDARDISÉ"
- **Le contenu vient du pitch** : section "Données métier clés" (3-5 métriques/chiffres/statuts)

### Éléments atomiques couverts par l'artefact (pour le Batch 2)
| Élément | Couvert | Où |
|---|---|---|
| Chiffre en typographie display | ✅ | Zone A — panneau dominant |
| Badge/statut textuel (fond teinté + texte) | ✅ | Zone A + cards Zone B |
| Séparation par fond (pas bordure) | ✅ | Panneau teinté vs cards sur surface |
| Densité variable (aéré vs dense) | ✅ | Zone A (aéré) vs Zone C (dense) |
| Cards/conteneurs (radius, shadow en contexte) | ✅ | 3 cards Zone B |
| Mini-dataviz (sparkline/barre de progression) | ✅ | Au moins 1 card Zone B |
| Hover secondaire (sur card) | ✅ | Cards Zone B |
| Bouton secondaire | ✅ | Zone C |
| Input/champ de formulaire | ✅ | Zone C (ajouté commit `0758e02`) |
| Toggle/switch | ✅ | Zone C (ajouté commit `0758e02`) |
| Micro-copie (labels, meta, annotations) | ✅ | Zone C |
| Hiérarchie 3 couches | ✅ | A > B > C |

### Éléments NON couverts par l'artefact (à gérer par le Batch 2)
| Élément | Pourquoi absent | Impact Batch 2 |
|---|---|---|
| Table avec colonnes/headers | Structure trop rigide pour le layout L | Le Batch 2 devra dériver le style table du `:root` + des cards |
| Tabs/navigation | Pas pertinent dans un composant de données | Le Batch 2 devra inventer |
| Iconographie (styles d'icônes) | C'est le job du Batch 2 ch.06 | Le Batch 2 s'appuie sur le `:root` |
| Dataviz complexe (courbes, donuts) | L'artefact n'a qu'une mini-dataviz | Le Batch 2 ch.07 s'appuie sur la palette + les proportions |

### Transmission style-tile → Batch 2
Le Batch 2 reçoit :
1. Le `:root` complet (palette, typo, spacing, radius, shadows, transitions) — extrait du style-tile
2. Les Google Fonts — extraites du style-tile
3. Le style-tile complet (hero + artefact + atmosphere) comme **référence de ton et de finition**
4. Le pitch extrait du concept choisi

**Ce que le Batch 2 doit RÉUTILISER de l'artefact** :
- Le style des badges (fond teinté + texte + couleur accent/primary)
- Le style des hovers (transitions multi-property, easing physiques)
- Le niveau de contraste fond/contenu (comment les zones se distinguent)
- Le style du bouton secondaire
- Le style de l'input et du toggle (nouveaux — commit `0758e02`)

**Ce que le Batch 2 doit INVENTER** (pas dans l'artefact) :
- Le style des icônes (ch.06) — dérivé des tokens formels du `:root` + du concept
- Le style de la dataviz (ch.07) — dérivé de la palette + des proportions du style-tile
- Le lockup logo (ch.05) — dérivé du concept + du logo fourni

### Bug corrigé — Double wrapper (commit `c2d6c93`)
Le placeholder `<!-- ARTEFACT_PLACEHOLDER -->` est maintenant DIRECTEMENT dans `<section class="artifact-witness">`, sans `<div class="artifact-witness__inner">` englobant. Le subagent artefact crée lui-même le wrapper `__inner`. Ceci évite le double nesting qui causait un artefact invisible.

### Fichiers clés pour le Batch 2
| Fichier | Rôle |
|---|---|
| `phases/phase-4-artefact.md` | Prompt du subagent artefact — structure semi-standardisée |
| `ref/css-patterns-phase4.md` | Squelette CSS de l'artefact (section "ARTEFACT SEMI-STANDARDISÉ") |
| `phases/phase-6a-batch2.md` | Prompt du subagent Batch 2 — lit le style-tile + le `:root` |
| `phases/phase-6b-batch3.md` | Prompt du Batch 3 — lit le style-tile + le résumé Batch 2 |
| `SKILL.md` lignes ~2995-3430 | Orchestration Phase 6A/6B — extraction `:root`, transmission variables |

---

## CHANTIERS OUVERTS (pour les sessions suivantes)

1. **Audit mapping A1/A2/A3** : vérifier que les techniques CSS prescrites par curseur sont en accord avec ce qu'on voit dans les Awards. Le clip-path sur les halos est un symptôme d'un problème plus large : le mapping prescrit des techniques sans vérifier leur pertinence élite. Les descriptions A1/A2/A3 ont été reformulées (session 13/04 — modifications dans `phase-3b-design.md` et `phase-4-artefact.md`) pour retirer les références à des techniques CSS concrètes et rester en langage sensoriel.

2. **Gate visuel en crops ciblés 250×250** : implémenté avec directive "impitoyable" (commit `55da19b`). Utilise `boundingBox()` pour localiser les éléments dans le DOM. Pas encore pleinement validé en conditions réelles.

3. **Grain** : monté à 0.35-0.45 en soft-light, tuilé 150px. Visible sur fond sombre (confirmé sur VoltaPilot). Borderline sur fond clair. Le gate visuel impitoyable devrait forcer le subagent à ajuster.

4. **Formes à contour net** : règle ajoutée (découragé) mais le subagent continue d'en produire occasionnellement (cercles stroke). Le gate visuel vérifie maintenant les formes à contour net (commit `55da19b`).

5. **Incohérence de nommage étalons** (noté depuis session précédente, toujours pas corrigé) : Phase 3B-5 vs Phase 4.

6. **Cohérence artefact → Batch 2** : l'artefact couvre maintenant ~90% des éléments atomiques (input + toggle ajoutés). Les éléments manquants (table, tabs, icônes, dataviz complexe) sont du ressort du Batch 2 qui les dérive du `:root` + du style-tile comme référence. À vérifier : est-ce que le Batch 2 exploite correctement les styles d'input/toggle/badge définis dans l'artefact ?

## Dernière mise à jour : 2026-04-13
