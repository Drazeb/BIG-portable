# Plan — Refactor du Penseur Visuel (Phase 3B-7c) avec Perplexity

**Statut** : IMPLÉMENTATION FAITE (5 mai 2026) — tests E2E à exécuter avant clôture
**Date initiale** : 2 mai 2026 — **Mise à jour** : 5 mai 2026
**Source** : conversation 30 avril → 5 mai 2026 (sessions Opus 4.7)

---

## État d'implémentation — 5 mai 2026

L'architecture validée a été implémentée en 7 étapes (A à G) sur la branche main du repo BIG :

| Étape | Commit | Description |
|-------|--------|-------------|
| A | `c8f965d` | Bascule séquentielle au checkpoint 3B-7-checkpoint (UN concept choisi → `.concept-pour-3B-7c`) |
| B | `62f81ca` | Subagent `phases/phase-3b-7c-perplexity-prompt-generator.md` (génère le prompt Perplexity à partir du template canonique sanctuarisé v5) |
| C | `1110f35` | Subagent `phases/phase-3b-7c-image-final-describer.md` (multimodal — produit la description finale au format spec `ref/visual-final-description-spec.md`) |
| D | `c4aaa48` | Refactor de l'orchestrateur 3B-7c dans SKILL.md — 10 sous-étapes 3B-7c.1 à 3B-7c.10 (avec branche A bypass Perplexity pour Mockup/CSS-SVG, branche B Perplexity + Cosmos + MJ/NB2) |
| E1 | `19dc87a` | Subagent pitch (`phases/phase-3b-design.md`) — lecture en cascade visual-pivot → visual-direction → dérivation libre + nouvelle "DIRECTIVE — ANCRAGE VISUEL OBLIGATOIRE" qui systématise le pattern `DIRECTIVE-PITCH-VISUAL-ANCHORING.md` |
| E2 | `71ef68c` | Orchestrateur 3B-7d (SKILL.md) — cascade + image en multimodalité + lecture multimodale obligatoire dans le subagent |
| F | `85be94b` | test-big SKILL.md — 5 zones mises à jour (menu, prérequis, outputs, démarrages, mapping section SKILL) |

**Tests E2E à exécuter avant clôture** :
1. **Branche A — Mockup produit** : test-big sur un projet existant en mode 3B-7c, choisir Mockup, vérifier que Perplexity est bypassé et `{brand}-visual-direction-c{N}.md` est généré directement.
2. **Branche A — Fond CSS/SVG procédural** : pareil, choisir CSS/SVG procédural, vérifier bypass.
3. **Branche B — Photo (cas VoltaPilot)** : test-big sur VoltaPilot c2, choisir Conceptuel + Photo, vérifier la séquence complète (prompt Perplexity généré, onglets Cosmos ouverts, pause utilisateur, dépose des fichiers, image finale, description finale).
4. **Branche B — Illustration (cas Liminal fictif)** : pareil, choisir Conceptuel + Illustration, vérifier que les onglets ArtStation+Behance s'ouvrent.
5. **Test pitch ancré** : après 3B-7c, lancer 3B-7d, vérifier que le pitch tisse le motif visuel dans Voice Block / Artefact / Interaction / Atmosphere / Logo (≥4 sections sur 5).
6. **Test cohérence test-big** : relancer test-big sur 3B-7c avec une session post-refactor, vérifier que les 3 tables (menu, prérequis, outputs) sont à jour.

**Décisions tranchées pendant la session 2-5 mai 2026** :
- Voie médiane sur concept narratif amont : TESTÉE ET ÉCARTÉE (cf. section dédiée plus bas — la libération de la métaphore ne libère pas des clichés, elle change juste le pool)
- Variantes A/B/C de divergence sur l'image-pivot : SUPPRIMÉES (UN seul concept, UNE seule image-pivot)
- Bascule séquentielle Phase 4 : OPTION 2 retenue (3 style-tiles dont 1 avec image-pivot, 2 sans image — choix utilisateur à l'entrée Phase 4 entre 3 / 1 / pause)
- Mockup et Fond CSS/SVG procédural : bypass Perplexity, utilisation du subagent legacy `phase-3b-penseur-visuel.md`
- Format de description finale : suit la spec sanctuarisée `ref/visual-final-description-spec.md` (10 sections A à J)
- Multimodalité du pitch : le subagent pitch lit l'image finale via Read tool

**Fichiers de référence sanctuarisés** (créés ou existants à utiliser) :
- `ref/perplexity-prompt-template.md` (v5)
- `ref/perplexity-prompt-rex.md` (REX itération v1→v5)
- `ref/visual-final-description-spec.md` (spec format des 10 sections A-J)
- `ref/plan-refactor-penseur-visuel-EN-COURS.md` (ce fichier)

---

⚠ Le contenu ci-dessous était la version sanctuarisée du 2 mai 2026 (avant les tests voie médiane et avant l'implémentation A-F). Il est conservé comme mémoire historique et pour référence des choix architecturaux pris.

---

## Contexte

Le **penseur visuel actuel** (Phase 3B-7c) prescrit la direction visuelle technique d'un concept BIG en 2 passes (étapes 1-4bis : arbitrage + ancre stylistique dérivée de la fiche styliste ; étapes 5-6 : prescription des 3 images concrètes + DNA visuel + gate qualité). Output : `{brand}-visual-direction-c{N}.md`.

**Constat empirique** (sessions 30 avril → 2 mai 2026) : Claude seul produit des images-pivot **médianes** parce que son training textuel converge sur les associations les plus probables (autoroutes statistiques type "main + objet" en figuratif). Pour atteindre le niveau élite, il faut un agent web-aware (Perplexity) qui puise dans la pratique contemporaine actuelle.

**Charles a obtenu un style-tile élite** lors d'un test pratique (`outputs/test-voltapilot-test-20260501-1134/voltapilot-style-tile-concept-2.html`) en suivant le process : Perplexity → choix d'image-pivot → recherches Cosmos/portfolios → MJ avec refs élite → itération NB2 multi-turn → image finale. Ce process est validé empiriquement.

---

## Architecture validée (5 étapes)

```
Phase 3B-7-checkpoint (style retenu)
   ↓
[BASCULE SÉQUENTIELLE — UN SEUL CONCEPT à partir d'ici]
L'utilisateur choisit UN concept parmi les 3 (sur la base des spécimens + spécimens stylisés)
   ↓
ÉTAPE 1 — Penseur Visuel (refactorisé)
- Arbitrage visuel (Image générée + fond CSS / Fond CSS pur)  [GARDÉ]
- Arbitrage sujet (Conceptuel / Littéral transcendé / Mockup) [GARDÉ]
- Demande à l'utilisateur le TYPE DE VISUEL souhaité (Photo / Illustration / 3D / Pattern / Aucune image) [NOUVEAU — transformation de l'étape 3 actuelle]
- Ancre stylistique 5 dimensions DÉRIVÉE de la fiche styliste [GARDÉ — étape 4bis actuelle]
- Génère le prompt Perplexity à partir du template (`ref/perplexity-prompt-template.md`)
   ↓
ÉTAPE 2 — Perplexity
- L'utilisateur copie le prompt dans Perplexity, ramène la réponse
- 5 idées d'images-pivot avec photographers/illustrateurs reconnus + URLs
- Mots-clés de recherche associés (5-8 par idée)
   ↓
ÉTAPE 3 — Tri humain + recherche d'images
- L'utilisateur choisit UNE image-pivot parmi les 5
- L'orchestrateur ouvre AUTOMATIQUEMENT les recherches Cosmos dans le navigateur (idée 11 — bash open URL)
- L'utilisateur ramène 5-8 images de référence (depuis Cosmos / portfolios des artistes nommés)
   ↓
ÉTAPE 4 — Skill `visual-brief-MJ` (à développer par autre session)
- Reçoit l'image-pivot + les images de référence + l'ancre stylistique + le concept narratif
- Produit des prompts MidJourney avec les refs élite
- Génère aussi des prompts de correction multi-turn pour itération
- L'utilisateur itère dans MJ ou Nano Banana 2 selon les ajustements à faire
- Output final : 1 image (ou plusieurs) validée par l'utilisateur
   ↓
ÉTAPE 5 — Retour Penseur Visuel
- Reçoit l'image finale validée (multimodalité — Read tool sur l'image)
- Produit la description fine pour le pitch (`{brand}-visual-pivot-c{N}.md`)
- Format proposé : sujet + composition + atmosphère + palette dominante + métaphore activée + photographer ref + intégration recommandée pour le pitch + métaphores narratives à privilégier dans le pitch
   ↓
Phase 3B-7d Pitch (existante)
- Reçoit `{brand}-visual-pivot-c{N}.md` + l'image encodée en base64 (multimodalité)
- Construit un pitch ULTRA-COHÉRENT avec le visuel + le reste des inputs
```

---

## Décisions de scoping prises (validées par Charles)

| Sujet | Décision |
|-------|----------|
| **Bascule séquentielle** | UN concept choisi à 3B-7-checkpoint, plus de 3 concepts en parallèle après. Implication : pas de pitch ×3, pas de style-tile ×3, Phase 4 traite UN concept |
| **Mode OUVERT/FERMÉ** | Simplifié — laisser Perplexity proposer librement (pas de mode formalisé). Confirmé sur le test VoltaPilot c2 où le mode OUVERT a très bien marché |
| **Type de visuel** | Choix utilisateur parmi 5 options macro : Photo / Illustration / 3D / Pattern-Texture / Aucune image (CSS pur). Granularité plus fine (28 sous-types A1-G4) à recalibrer si nécessaire plus tard |
| **Ouverture automatique des onglets Cosmos** | OUI — l'orchestrateur lance `open "https://www.cosmos.so/search?q=..."` pour chaque requête. À étendre plus tard à Are.na / Behance / ArtStation selon le médium |
| **Itération MJ ↔ NB2** | Le skill visual-brief-MJ produit des prompts MJ + des prompts de correction multi-turn. L'utilisateur itère manuellement dans MJ ou NB2 (multi-turn natif NB2). Pas d'itération automatisée par le skill (à voir plus tard) |
| **Format pitch** | Description structurée + multimodalité (image en base64). Format précis à calibrer sur `outputs/test-voltapilot-test-20260501-1134/DIRECTIVE-PITCH-VISUAL-ANCHORING.md` (existant, pas encore lu en détail) |
| **Voie médiane sur concept narratif** | À TESTER — voir section dédiée ci-dessous |

---

## Voie médiane sur le concept narratif — TESTÉE ET ÉCARTÉE (2 mai 2026)

### Principe testé

Hypothèse : Claude étant médian sur les métaphores visuelles, peut-être que la métaphore visuelle elle-même devrait venir de Perplexity (qui voit l'élite contemporaine), pas de Claude. On testait : concept narratif Claude = positionnement + métaphore-cadre large + archétype + tension (sans métaphore visuelle prescrite). Perplexity proposait alors la métaphore visuelle directrice + les 5 images-pivot.

### Tests réalisés sur Liminal

**Test v6-amont** (concept narratif amont avec tagline "Cartographier l'invisible" préservée) : Perplexity a convergé sur la cartographie comme métaphore — exactement la métaphore prescrite par Claude dans le v5 baseline. **Convergence forte** sur 3 idées sur 5 quasi-identiques entre v5 et v6. La voie médiane n'apportait pas de fertilité — la tagline biaisait le résultat.

**Test v7-neutre** (brief totalement nettoyé du vocabulaire cartographique : tagline "Donner forme à l'invisible", suppression de "territoire / exploration / traversée / cartographe" du brief, retrait de la cartographie de la liste des candidats métaphoriques) : Perplexity a basculé sur la **cristallographie / minéralogie**. Théorie de l'amorçage par tagline confirmée. **Mais le résultat dégrade** :
- 4 idées sur 5 sont des clichés du champ cristallographique : portrait avec cristaux dans la tête (cliché NFT 2021 / wellness éditorial), grotte cristalline (cliché Blender new age — Perplexity le reconnaît lui-même mais le recommande quand même), agrégats flottants (dans la liste anti-clichés explicite, ignoré), mains en suspension cristalline (retour du pattern main+objet)
- 1 idée fraîche seulement (Croissance dendritique, semi-abstrait)
- Comparaison v5 baseline : 3 idées fortes sur 5
- **v5 > v7 nettement** sur la qualité créative

### Diagnostic profond

**Aucun champ métaphorique n'est intrinsèquement "frais".** Chaque champ a ses propres autoroutes de clichés établis dans la pratique illustrative éditoriale :
- Cartographie → main avec compas, paysages flottants, archipels
- Cristallographie → portrait avec cristaux dans la tête, grottes cristallines, mains qui se cristallisent
- (Probablement Botanique) → cerveau-plante, racines mentales, fleurs émotionnelles
- (Probablement Architecture) → maison mentale, pièces d'émotions, escaliers infinis

Libérer Perplexity d'une métaphore ne le libère pas des clichés — ça change juste le pool dans lequel il pioche.

Pire : sans la métaphore prescrite par Claude (qui est cohérente avec le pitch en aval), Perplexity peut choisir une métaphore qui ne matche pas le reste du pipeline (dissonance narrative pitch ↔ visuel).

### Décision actée

**On garde le pattern v5 comme défaut** : Claude (Phase 3A) prescrit la métaphore narrative directrice (positionnement + métaphore directrice précise + archétype + tension). Perplexity prend le relais sur les images-pivot **dans cette métaphore**, sans la rediscuter.

Le travail anti-cliché se fait **à l'intérieur d'une métaphore** (via les mécanismes du template v5 : concepts émergents 2025-2026, auto-critique honnête, anti-clichés sectoriels explicites, diversité géographique, etc.) — pas en changeant de métaphore.

### Mode manuel optionnel (Charles)

Charles peut, à sa discrétion sur un projet précis, demander manuellement la voie médiane (concept narratif amont + Perplexity propose la métaphore). C'est une option utilisateur, pas un défaut système. **Le système BIG ne déclenche jamais cette voie automatiquement.**

### Fichiers de test conservés (référence historique)

- `~/Downloads/perplexity-prompt-test-illustration-liminal-v6-amont.md` (avec tagline préservée)
- `~/Downloads/perplexity-prompt-test-illustration-liminal-v7-neutre.md` (brief nettoyé)
- `~/Downloads/A. Métaphore directrice retenue.md` (rapport Perplexity v6)
- `~/Downloads/A. Métaphore directrice retenue (1).md` (rapport Perplexity v7)

---

## Questions encore ouvertes

| # | Question | Importance |
|---|----------|-----------|
| 1 | **Mécanique pratique du retour Perplexity dans BIG** : Charles colle dans un fichier `{brand}-perplexity-response-c{N}.md` ? Autre mécanisme ? | Élevée — touche l'orchestrateur |
| 2 | **Format précis du retour des images de référence Cosmos** : Charles dépose dans `outputs/{session}/visual-refs/c{N}/img-1.jpg` ? Naming convention ? | Élevée |
| 3 | **Lecture du `DIRECTIVE-PITCH-VISUAL-ANCHORING.md`** (existant dans test-voltapilot-test-20260501-1134) pour calibrer le format pitch précis | Moyenne — à faire avant la finalisation du plan |
| 4 | **Granularité du menu type de visuel** : 5 macro suffisent ou il faut 28 sous-types ? À voir empiriquement quand on commence à utiliser | Faible — peut être ajusté plus tard |
| 5 | **Test reproductibilité Perplexity** : si on relance 3 fois, sort-il les mêmes 5 idées ? | Moyenne — à tester avant industrialisation |
| ~~6~~ | ~~Validation de la voie médiane~~ | **TRANCHÉE 2 mai 2026** — voie médiane écartée comme défaut système, mode manuel possible si Charles le demande explicitement (cf. section "Voie médiane TESTÉE ET ÉCARTÉE") |
| 7 | **Adaptation aux médiums non-illustration / non-photo** (3D, pattern, mixed-media) : le template Perplexity tient-il ? | Moyenne — à valider quand on rencontre le cas |

---

## Chantiers liés (références internes)

| Fichier | Rôle |
|---------|------|
| `ref/perplexity-prompt-template.md` | Template canonique sanctuarisé (v5) |
| `ref/perplexity-prompt-rex.md` | REX itération v1→v5 + pièges à ne plus reproduire |
| `outputs/Captures/Captures diverses/Test cable/passation-test-iteration-visuels-elites.md` | Passation pour autre session Sonnet sur les tests d'itération NB2/MJ/Image2 (HORS scope architecture) |
| `outputs/test-voltapilot-test-20260501-1134/DIRECTIVE-PITCH-VISUAL-ANCHORING.md` | Directive existante pour ancrer le pitch dans le visuel — à lire pour calibrer le format pitch |
| `outputs/test-voltapilot-test-20260501-1134/voltapilot-style-tile-concept-2.html` | Style-tile élite obtenu empiriquement (preuve de concept) |

---

## Prochaines actions (ordre proposé)

1. ~~Test voie médiane~~ — **FAIT 2 mai 2026, voie médiane écartée**
2. ~~Comparaison v5 vs v6-amont~~ — **FAIT, v5 gagne**
3. **Lecture du `DIRECTIVE-PITCH-VISUAL-ANCHORING.md`** pour calibrer le format pitch précis
4. Réponses aux questions 1, 2, 3, 4, 5, 7 ouvertes ci-dessus
5. **Plan d'implémentation final** consolidé dans un nouveau fichier `plan-refactor-penseur-visuel-FINAL.md`
6. Implémentation : modification du SKILL.md de BIG pour intégrer la nouvelle Phase 3B-7c, mise à jour des outputs, mise à jour du SKILL.md de test-big

---

## Dernière mise à jour : 2 mai 2026
