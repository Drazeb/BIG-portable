# Rapport de passation — Réorganisation Phase 3B : déplacer la génération de visuels APRÈS le choix de styles (29 avril 2026)

> **Pour la prochaine session qui prendra ce chantier.**
> Tout est en mémoire ici, rien n'est dans le code. Aucune modif n'a encore été appliquée. Le chantier est au stade "faisabilité + pour/contre validés", pas de plan détaillé ligne par ligne.

---

## 1. Synthèse exécutive (5 lignes pour collègue pressé)

1. **Problème** : aujourd'hui le pipeline 3B fait penseur visuel (3B-5) + génération MJ/Recraft (3B-6) **AVANT** le choix de styles (3B-7a/b/checkpoint). Les visuels sont fixés sans connaître le style officiel retenu → risque de dissonance style ↔ visuel + gaspillage MJ ~3× (9 images au lieu de 27 utilisées).
2. **Solution proposée (Option B)** : inverser l'ordre — les styles sont arbitrés en premier, puis le penseur visuel reçoit la fiche de style canonique en input et prescrit des visuels alignés.
3. **Verdict structurel** : Option B est plus pertinente, calque la logique humaine d'un DA (style d'abord = univers global, visuels ensuite = incarnation).
4. **Statut** : pour/contre validés avec Charles, **pas de plan détaillé**, **pas de code touché**. Charles a demandé soit un test A/B empirique d'abord, soit une refonte directe — il n'a pas tranché.
5. **Coût estimé grosse maille** : 3-4h refonte directe, 5-6h avec test A/B préalable.

---

## 2. Contexte du chantier — pourquoi cette question s'est posée

### 2.1 Le pipeline actuel (29 avril 2026)

Dans `SKILL.md` BIG, l'ordre actuel est :

```
3B-1a/b   Routeur chromatique + inspiration esthétique
3B-2      Choix des polices
3B-3      Palette (3 variantes A/B/C par concept, choix utilisateur)
3B-4      Spécimens typo+palette
3B-5      Direction visuelle (penseur visuel)              ← prescrit type/sujets/cadrage/lumière des images
3B-6      Génération visuels MJ/Recraft                    ← génère les images
3B-7a-A/B/C   Styliste (3 sous-vagues, 3 fiches de style par concept)   ← choix officiel du style
3B-7b     Spécimens stylisés (9 sub-agents, 1 par concept × variante)
3B-7-checkpoint   Choix utilisateur de la variante de style
3B-7c     Pitch designer (assemblage final)
4         Phase 4 style-tile
```

### 2.2 Ce qui ne va pas dans cet ordre (les arguments QUE J'AVAIS DÉJÀ NOTÉS)

1. **Dissonance style ↔ visuel possible** : si le penseur visuel a prescrit "photo documentaire en lumière naturelle" et que le styliste retient ensuite "Dark Mode Cinema", les 2 univers se télescopent en Phase 4. Le pitch designer doit faire le grand écart.

2. **Gaspillage MJ ~3×** : aujourd'hui la Phase 3B-5 produit 3 directions visuelles A/B/C par concept = 9 directions × 3 images = 27 prompts MJ générés. À l'arrivée, l'utilisateur n'utilise qu'1 direction par concept = 9 visuels effectivement utilisés. Les 18 autres sont des artefacts intermédiaires non récupérables. Si on inverse l'ordre, on génère 9 directly alignées au style retenu.

3. **Décisions verrouillées en amont** : une fois les visuels MJ générés (coût en crédits), revenir en arrière est coûteux. Le styliste subit le visuel généré.

4. **Inversion de la logique humaine** : un DA expérimenté pense d'abord l'univers du style ("c'est un Editorial Grid"), puis le type d'image ("donc photo documentaire en multi-cols"). Pas l'inverse.

5. **Étalons culturels perdus** : la fiche de style retient des références culturelles (Linear, Apartamento, NYT Magazine, etc.) qui devraient guider le penseur visuel. Aujourd'hui le penseur visuel ne les a pas en input.

### 2.3 Ce qui marche dans l'ordre actuel (à NE PAS perdre en réorganisant)

1. Le concept narratif contient déjà beaucoup d'orientation visuelle (sujets, métaphores, atmosphère) → suffisant pour prescrire un visuel cohérent même sans le style.
2. La palette est déjà validée AVANT les visuels → cohérence palette ↔ visuel garantie.
3. Le penseur visuel actuel s'en sort empiriquement bien sans connaître le style (test VoltaPilot 26/04 + 29/04 : visuels MJ corrects).

→ Donc l'ordre actuel n'est pas catastrophique, juste sous-optimal.

---

## 3. Les 3 options évaluées (avec Charles, validées)

| Option | Mécanique | Verdict |
|---|---|---|
| **A — ordre actuel** | Visuels → Styles | ⚠ Risque dissonance + gaspillage MJ + logique inversée |
| **B — inversé** | Styles d'abord, puis visuels alignés au style retenu | ✓ **RECOMMANDÉ** — cohérence + économie + logique naturelle |
| **C — parallèle** (1 sub-agent fait style + visuels ensemble) | — | ✗ REJETÉ — perte de spécialisation, contexte explosif, pas de checkpoint intermédiaire |

Charles avait spontanément rejeté Option C. Sa question était entre A (statu quo) et B (inversion).

### 3.1 Tableau pour/contre détaillé Option A vs B

| Critère | Option A (actuel) | Option B (inversé) |
|---|---|---|
| Cohérence style ↔ visuel | ⚠ Risque dissonance | ✓ Garantie |
| Logique humaine DA | ✗ Inversée | ✓ Naturelle |
| Coût MJ / projet | ✗ ~27 images générées (18 inutilisées) | ✓ ~9 images |
| Spécialisation expertises sub-agents | ✓ | ✓ |
| Coût de refonte | 0 (statu quo) | ~3-4h |
| Risque casse pipeline | 0 | Modéré |
| Étalons culturels du style transmis au penseur visuel | ✗ Perdus | ✓ Disponibles via fiche styliste |
| **Qualité style-tile final attendue** | Variable (dépend du tirage) | Probablement plus stable |

---

## 4. Squelette du pipeline cible (Option B)

```
3B-1a/b   Routeur chromatique + inspiration esthétique          (inchangé)
3B-2      Choix des polices                                     (inchangé)
3B-3      Palette                                               (inchangé)
3B-4      Spécimens typo+palette                                (inchangé)
─── À PARTIR D'ICI, ORDRE INVERSÉ ───
3B-7a-A/B/C   Styliste 3 sous-vagues                            (DÉPLACÉ AVANT visuels)
3B-7b     Spécimens stylisés (9 sub-agents)                     (DÉPLACÉ AVANT visuels — sans images MJ, juste placeholders)
3B-7-checkpoint   Choix utilisateur variante de style           (DÉPLACÉ AVANT visuels)
─── le style canonique {brand}-style-choice-c{N}.md est fixé ───
3B-5      Direction visuelle (penseur visuel)                   (RECEVRA la fiche style en input)
3B-6      Génération visuels MJ/Recraft                         (1 set par concept selon style retenu)
3B-7c     Pitch designer (assemblage final)                     (inchangé conceptuellement, mais reçoit dans le bon ordre)
4         Phase 4 style-tile                                    (inchangé)
```

**Question de nommage** : faut-il renommer 3B-5 et 3B-6 en 3B-7d et 3B-7e (cohérence numérotation post-checkpoint) ? Ou garder les numéros actuels et accepter que l'ordre numérique ne reflète plus l'ordre d'exécution ? À trancher avec Charles.

---

## 5. Fichiers à modifier — liste exhaustive identifiée

### 5.1 Fichiers principaux

| Fichier | Modif attendue | Volume estimé |
|---|---|---|
| `.claude/skills/brand-identity/SKILL.md` | Déplacement du gros bloc Vague 2quater (penseur visuel) + section 3C (génération visuels) APRÈS la section 3B-7-checkpoint. Mise à jour des références entre sections. | ~200-300 lignes à déplacer + ~30 lignes à patcher |
| `.claude/skills/brand-identity/phases/phase-3b-penseur-visuel.md` | Ajouter `{style_choice}` comme variable d'input. Adapter le prompt pour que le penseur visuel s'aligne au style retenu (registre, atmosphère, signatures du style). | ~30 lignes à ajouter |
| `.claude/skills/brand-identity/phases/phase-3b-design.md` (pitch) | Vérifier l'ordre des inputs. Le pitch reçoit aujourd'hui `{visual_direction}` + `{style_choice}` + `{palette_direction}`. Vérifier que rien ne casse si l'ordre temporel change. | ~5-10 lignes éventuellement |
| `.claude/skills/test-big/SKILL.md` | Mise à jour des 3 tables : prérequis par phase (~L106), outputs par phase (~L216), mapping phase → section SKILL.md (~L336). Et la liste utilisateur (~L27) + algo `phases_ordonnées` (~L250). | ~20-30 lignes à patcher |

### 5.2 Fichiers à VÉRIFIER (impact possible mais à confirmer)

| Fichier | Quoi vérifier |
|---|---|
| `.claude/skills/brand-identity/phases/phase-3b-styliste.md` | Ne reçoit pas les visuels en input aujourd'hui (vérifié) — reste cohérent dans le nouveau flow. |
| `.claude/skills/brand-identity/phases/phase-3b-specimen-stylise.md` | Ne reçoit pas les visuels en input. Reste cohérent. |
| `.claude/skills/brand-identity/phases/phase-4-styletile.md` | Reçoit les visuels via `{visual_reference_block}`. Vérifier que la transmission marche pareil avec le nouvel ordre. |
| `.claude/skills/visual-brief/SKILL.md` | Skill séparé invoqué depuis Phase 3B-6. Vérifier que rien ne casse. |
| `.claude/skills/brand-identity/scripts/*.py` | Aucun gate Python touché normalement, mais vérifier les chemins en dur. |

### 5.3 Sessions de test existantes (NE PAS toucher mais comprendre)

Les sessions existantes (`outputs/test-*`) ont été générées dans l'ordre actuel. Elles serviront à comparer A vs B en test empirique. Ne PAS supprimer.

---

## 6. Dépendances cachées à vérifier avant de coder

1. **Le penseur visuel actuel (3B-5)** lit-il déjà la fiche styliste ? Réponse : **NON** (vérifié par grep `style_choice` dans `phase-3b-penseur-visuel.md` — absent). C'est un bon signe : il faut juste l'ajouter.

2. **Le pitch designer (`phase-3b-design.md`)** reçoit-il `{style_choice}` aujourd'hui ? Réponse : **OUI** (commit récent ajoutant FICHE DE STYLE — bloc `## FICHE DE STYLE — Déterminée EN AMONT`). Donc le pitch attend déjà la fiche en amont. Pas d'impact.

3. **La Phase 4 styletile** reçoit-elle `{style_choice}` aujourd'hui ? Réponse : **OUI** (j'ai ajouté ça dans un commit précédent — variable `{style_choice}` injectée dans `phase-4-styletile.md`). Pas d'impact.

4. **Les 3 sous-vagues styliste 3B-7a-A/B/C** dépendent-elles des visuels ? Réponse : **NON** (vérifié — le styliste lit palette + fonts + concept + scoping + ventre mou, pas les visuels). Indépendant.

5. **Les 9 spécimens 3B-7b** dépendent-ils des visuels ? Réponse : **NON** (vérifié — le specimen lit la fiche styliste + palette + fonts + concept narratif, pas les visuels). Indépendant.

6. **Le checkpoint user 3B-7-checkpoint** affiche-t-il les visuels ? Réponse : **NON** — il affiche les 3 spécimens HTML stylisés (qui n'incluent pas les visuels MJ — juste des placeholders gradients/formes). Indépendant.

→ Conclusion : la chaîne styliste → spécimens stylisés → checkpoint → pitch est ENTIÈREMENT INDÉPENDANTE de la chaîne penseur visuel → génération visuels. On peut les inverser sans casser leur logique respective.

7. **Mais point critique** : le `{visual_reference_block}` dans `phase-4-styletile.md` lit `{brand}-visual-c{N}-*.png` après la Phase 4. Donc les visuels DOIVENT être générés AVANT Phase 4. Dans l'Option B, ils sont générés entre 3B-7c (pitch) et Phase 4 — c'est OK.

---

## 7. Plan d'implémentation suggéré (en ordre)

**Phase 1 — Préparation** (~30 min)
1. Lire intégralement les 5 fichiers principaux à modifier (SKILL.md sections 3B-5/3B-6/3B-7a/b/c, phase-3b-penseur-visuel.md, phase-3b-design.md, test-big/SKILL.md)
2. Identifier les références croisées entre sections (qui mentionne qui)
3. Identifier les variables qui changent de timing

**Phase 2 — Modifs SKILL.md** (~1h-1h30)
1. Couper le bloc complet Vague 2quater (3B-5 — penseur visuel) + section 3C (3B-6 — génération visuels)
2. Le coller APRÈS la section 3B-7-checkpoint et AVANT l'Interaction 3 (3B-7c pitch)
3. Renuméroter les sous-titres si on choisit cette option (3B-5 → 3B-7d ?)
4. Mettre à jour les transitions textuelles ("Après le checkpoint utilisateur, on passe à la direction visuelle…")
5. Vérifier que tous les `{...}` variables substituées sont cohérents (rien ne pointe vers du futur)

**Phase 3 — Modifs phase-3b-penseur-visuel.md** (~30 min)
1. Ajouter la variable `{style_choice}` dans la liste des inputs
2. Insérer un bloc explicite "STYLE OFFICIEL — TU L'ALIGNES AU LIEU DE DEVINER" qui dit au penseur visuel que la fiche de style fait autorité sur le registre/atmosphère/signatures, et que sa direction visuelle DOIT s'aligner aux références culturelles + signatures du style retenu.
3. Ajouter dans le STATUS final un check "fidélité au style retenu" (auto-évaluation par le penseur)

**Phase 4 — Modifs test-big/SKILL.md** (~30 min)
1. Mettre à jour la liste utilisateur des phases (L27) — réordonner
2. Mettre à jour la table prérequis par phase (L106) — 3B-5 demande maintenant `{brand}-style-choice-c*.md` en plus
3. Mettre à jour la table outputs par phase (L216) — l'ordre des outputs change
4. Mettre à jour le mapping phase → section SKILL.md (L336)
5. Mettre à jour `phases_ordonnées` (L250)

**Phase 5 — Tests E2E** (~30 min - 1h)
1. Lancer `/test-big` sur un projet existant (Camille ou VoltaPilot) à partir de 3B-3 (palette) avec le nouvel ordre
2. Vérifier que la chaîne complète tourne sans erreur jusqu'au pitch
3. Comparer les visuels générés vs ancien run (cohérence avec le style retenu améliorée ?)

**Phase 6 — Commit** (~15 min)
1. Commit unique : `refactor: reorder Phase 3B — styles before visual direction (Option B)`
2. Mention dans le body : motivation + lien vers ce rapport de passation

---

## 8. Tests à faire pour valider

### Test minimum (smoke test)

Sur 1 projet existant (VoltaPilot 29/04 idéalement) :
1. Run complet 3B-3 → 3B-7c avec nouvel ordre
2. Vérifier qu'il n'y a pas de plantage / variable manquante
3. Vérifier que le pitch final est complet et cohérent

### Test qualitatif (A/B empirique)

Si Charles veut mesurer le gain :
1. Garder un run "Option A" (ancien ordre) sur VoltaPilot ou Camille (déjà fait — utiliser `outputs/test-voltapilot-test-20260429-1631`)
2. Lancer 1 run "Option B" sur le même projet
3. Comparer sur 6 critères (cf. rapport pitch comparatif fait précédemment) :
   - Précision des prescriptions
   - Cohérence interne style ↔ visuel ↔ pitch
   - Marqueurs slop évités
   - Respect palette
   - Ancrage concept
   - Anti-CSS

### Test critique (regression)

Vérifier qu'aucune Phase 4 ne plante par manque de visuel (ils sont maintenant générés plus tard dans le pipeline).

---

## 9. Risques + mitigations

| Risque | Probabilité | Mitigation |
|---|---|---|
| Le styliste se trompe → les visuels suivent et amplifient l'erreur | Moyen | Le checkpoint user 3B-7-checkpoint donne 3 variantes, l'utilisateur arbitre. Si rejet → resume du sub-agent styliste avec feedback. Visuels générés seulement APRÈS validation user du style. |
| Une référence croisée dans SKILL.md pointe vers une section qui a bougé | Élevé | Re-grep systématique après refonte : `grep -E "Vague 2quater|3B-5|3B-6|penseur visuel|génération visuel" SKILL.md` et corriger toutes les mentions. |
| Le penseur visuel ignore la fiche styliste si elle est mise dans le prompt mais sans contrainte forte | Moyen | Calque le pattern `phase-4-styletile.md` ajout récent : bloc "STYLE OFFICIEL — FAIT AUTORITÉ" avec règle de tranchée. + Test mental : si on retire `{style_choice}` du prompt, est-ce que la direction visuelle change vraiment ? Si non → fix nécessaire. |
| test-big SKILL.md non mis à jour → reprise de session impossible sur les phases 3B-5/3B-6 | Élevé | Phase 4 du plan dédiée à test-big. À tester avec un `/test-big` ciblé sur 3B-5 (= maintenant 3B-7d ?) après refonte. |
| Sessions existantes deviennent incompatibles | Faible | Les sessions existantes sont des outputs figés sur disque, on ne les modifie pas. Seuls les NOUVEAUX runs utiliseront le nouvel ordre. |

---

## 10. Strictement HORS scope (à ne PAS toucher)

1. **Phase 4 styletile** : reçoit déjà `{style_choice}` (ajouté précédemment) et `{visual_reference_block}`. Ne pas toucher.
2. **Le styliste 3B-7a et ses 3 sous-vagues** : refonte récente (commits `d41bc7a` + `2edcbfb` + `b0c51d5` + `6259cdf`), fonctionne bien. Ne pas re-toucher dans ce chantier.
3. **Le checkpoint user 3B-7-checkpoint** : marche bien. Ne pas toucher.
4. **La Phase 1, 2, 3A** : aucune raison d'y toucher.
5. **Les gates Python** (`phase3b-style-anti-slop.py`, `phase3b-palette-anti-slop.py`, `phase3b-gamut-router-anti-slop.py`, etc.) : indépendants de l'ordre.

---

## 11. Références à lire en priorité (~30 min de lecture)

### Pour comprendre le contexte technique

| Fichier | Pourquoi |
|---|---|
| `.claude/skills/brand-identity/SKILL.md` zone 3B-5 (~L1831-1990) — Vague 2quater Penseur visuel | Comprendre exactement ce qui sera déplacé |
| `.claude/skills/brand-identity/SKILL.md` zone 3B-6 (~L1990-2050) — Génération visuels | Idem |
| `.claude/skills/brand-identity/SKILL.md` zone 3B-7a/b/checkpoint (~L2050-2300) | Comprendre la chaîne styliste qui restera en place mais qui passera AVANT |
| `.claude/skills/brand-identity/phases/phase-3b-penseur-visuel.md` | Prompt du penseur visuel à modifier |
| `.claude/skills/brand-identity/phases/phase-3b-design.md` | Pitch designer — vérifier qu'il reçoit bien tous les inputs dans le nouveau timing |
| `.claude/skills/brand-identity/phases/phase-3b-styliste.md` | Pour confirmer qu'il ne dépend pas des visuels |
| `.claude/skills/brand-identity/phases/phase-3b-specimen-stylise.md` | Idem |
| `.claude/skills/test-big/SKILL.md` | Comprendre les 3 tables à mettre à jour |

### Pour comprendre l'historique du pipeline

| Fichier | Pourquoi |
|---|---|
| `.claude/skills/brand-identity/ref/passation-implementation-pistes-1+3-2026-04-25.md` | Historique de l'ajout du styliste 3B-7a (avril 2026) — pourquoi il a été inséré APRÈS les visuels (héritage historique, pas choix optimal) |
| `.claude/skills/brand-identity/ref/rex-visual-upgrade-session-2026-03-30.md` | REX session de modernisation visuelle — contient le pattern "Code > Rules" + audit Awards 88 sites |
| `.claude/skills/brand-identity/ref/visual-direction-guide.md` | Guide DA pour le penseur visuel — à connaître pour adapter le prompt |
| `DECISIONS.md` | Décisions D43-D44 sur l'ajout du penseur visuel et du skill `/visual-brief` (voir entrées avril 2026) |

### Pour comprendre l'objectif du pipeline (utile pour ne pas casser de fonctionnalités)

| Fichier | Pourquoi |
|---|---|
| `ARCHITECTURE.md` | Carte technique du pipeline BIG |
| `.claude/skills/brand-identity/ref/pipeline-overview.md` | Vue d'ensemble côté utilisateur |
| `CLAUDE.md` (workspace + projet) | Conventions du projet (commits, REX, documentation) |

---

## 12. Mémoire persistante à mettre à jour APRÈS implémentation

Si tu (la prochaine session) implémentes ce chantier avec succès :

1. **DECISIONS.md** — ajouter une entrée DXX :
   ```
   DXX (date) — Réorganisation Phase 3B : penseur visuel et génération visuels après le styliste
   Pourquoi : cohérence style ↔ visuel garantie, économie MJ ~3×, logique humaine respectée.
   ```

2. **CHANGELOG.md** — entrée datée avec mention "Refonte ordre Phase 3B Option B"

3. **MEMORY.md** (mémoire persistante de la session) — pointer vers le commit + ce rapport pour traçabilité

4. **ARCHITECTURE.md** — mettre à jour le schéma du pipeline 3B et la section "Mécanisme global" si l'ordre y est documenté

---

## 13. Questions ouvertes que je n'ai PAS résolues

1. **Renumérotation des phases** : on garde 3B-5/3B-6 (qui exécutent maintenant après 3B-7-checkpoint) ou on les renomme 3B-7d/3B-7e ? Trancher avec Charles.

2. **Test A/B avant refonte ?** Charles n'a pas tranché. Il a dit "soit test A/B, soit refonte directe". À reconfirmer avec lui.

3. **Faut-il aussi modifier le skill `/visual-brief`** (Phase 3C séparée) pour qu'il reçoive la fiche styliste ? Probablement oui, mais à confirmer empiriquement.

4. **Comment le penseur visuel "alignera" sa direction au style retenu ?** En théorie : il lit la fiche, identifie les références culturelles + atmosphère + registre, et prescrit un type d'image cohérent. Mais empiriquement il faut tester pour voir si ça marche sans tomber dans le templating ("le style est Editorial Grid donc je prescris automatiquement photo documentaire en multi-cols"). À vérifier au premier test.

5. **Coût en runtime** : si on fait des sous-vagues séquentielles, on rallonge le pipeline. À mesurer (gain qualité vs perte temps).

---

## 14. Synthèse 5 lignes pour collègue pressé (rappel)

1. **Chantier** : déplacer 3B-5 (penseur visuel) + 3B-6 (génération visuels) APRÈS 3B-7-checkpoint (choix utilisateur de la variante de style). Aujourd'hui c'est l'inverse.
2. **Pourquoi** : cohérence style ↔ visuel garantie + économie MJ ~3× + logique humaine respectée. Recommandé après pour/contre validés avec Charles.
3. **Statut** : pour/contre OK, **pas de code touché**, **pas de plan ligne par ligne**. Charles n'a pas tranché entre test A/B préalable et refonte directe.
4. **Coût** : ~3-4h refonte directe, ~5-6h avec test A/B préalable.
5. **Action recommandée** : (a) lire les 8 fichiers prioritaires de §11 (~30 min), (b) demander à Charles de trancher entre test A/B vs refonte directe, (c) suivre le plan §7 si refonte directe.

---

## Dernière mise à jour

**Date** : 2026-04-29
**Auteur** : Claude (session 28-29 avril, ayant aussi traité dans la même session : refonte 3B-7a en 3 sous-vagues divergentes, fix gate Python anti-slop styliste, fix incarnation checklist + above-the-fold mandate dans phase-3b-specimen-stylise.md)
**Commits récents pertinents pour le contexte** :
- `d41bc7a` — refactor 3B-7a 3 sous-vagues + ajout {style_choice} à Phase 4
- `2edcbfb` — gate Python anti-slop styliste
- `b0c51d5` — checklist d'incarnation specimen
- `6259cdf` — above-the-fold mandate specimen
- `69e67a8` — fix test-big merge 3B-7a-A/B/C
**Prochaine session attendue** :
1. Lire ce rapport (§1 + §11 priorité)
2. Lire les 8 fichiers prioritaires (~30 min)
3. Confirmer avec Charles : test A/B préalable ou refonte directe ?
4. Si refonte directe → suivre plan §7

---

## Implémentation faite — 29 avril 2026

**Statut** : Refonte directe exécutée, commit `6771bec`. **Test E2E reste à faire avant validation finale**.

**Décisions tranchées avec Charles avant exécution** :
1. **Refonte directe** (pas de test A/B préalable) — pour/contre considérés solides, pas besoin de mesure empirique préalable.
2. **3 renames** — 3B-5 (penseur visuel) → 3B-7c, 3B-7c (pitch) → 3B-7d, 3B-6 (génération visuels) → 3B-7e. Ordre alphabétique = ordre d'exécution.
3. **Skill `/visual-brief` (3B-7e) non touché** — premier test sans modif. Si test E2E révèle un manque d'ancrage côté générateur MJ/Recraft, on durcira dans un chantier suivant.
4. **Option B retenue** (visuels APRÈS pitch, pas avant) — analyse qualitative en profondeur a montré que l'apport marginal d'avoir les images pixelisées au pitch est faible (DNA visuel + fiche styliste suffisent à 95%), et le coût UX (pause MJ de 15-90 min en plein milieu de la 3B) est élevé.

**Mécanisme central de l'ancrage du penseur visuel sur la fiche styliste (4 leviers cumulés)** :
1. Bloc d'autorité `## STYLE OFFICIEL — FAIT AUTORITÉ` en intro du prompt + règle de tranchée explicite (si conflit direction naturelle ↔ fiche, le style gagne)
2. Recâblage Étape 4bis du prompt — chaque dimension de l'ancre stylistique (registre, lumière, grain, abstraction, bords) doit citer la phrase de la fiche qui la justifie, ou déduire d'une référence culturelle citée
3. Format de sortie modifié : sous-champ "Source dans la fiche" obligatoire pour chaque dimension
4. Critère "Fidélité au style retenu" ajouté à la gate qualité (étape 6b et tableau de sortie)

Pattern LLM exploité : "le LLM suit la contrainte la plus structurellement concrète, pas l'instruction abstraite" — recâbler la structure du prompt force l'ancrage par la mécanique, pas par l'instruction.

**Plus** : ajout d'un bloc "DNA visuel transmissible" en fin d'output du penseur visuel (3-5 lignes condensées : Registre / Lumière / Grain / Palette ciblée / Référence ergonomique) pour calibrer les paramètres techniques du générateur de prompts MJ/Recraft (--ar, --stylize, --chaos, références photographiques).

**Fichiers modifiés (commit `6771bec`)** :
- `.claude/skills/brand-identity/SKILL.md` (déplacement bloc Vague 4 L1983-2199 vers nouvelle position après checkpoint, renumérotation des 3 cibles, ajout `{style_choice}` dans variables, instruction PASSE 2 enrichie pour exiger le DNA visuel, 9 cross-références patchées)
- `.claude/skills/brand-identity/phases/phase-3b-penseur-visuel.md` (~80 lignes ajoutées : bloc d'autorité + recâblage 4bis + sous-champ "Source dans la fiche" + DNA visuel transmissible + critère gate)
- `.claude/skills/brand-identity/phases/phase-3b-design.md` (précision dans section "Visuels recommandés" : la direction visuelle est désormais ancrée sur la fiche styliste)
- `.claude/skills/test-big/SKILL.md` (5 zones patchées : liste utilisateur, table prérequis, table outputs, algorithme phases_ordonnées, mapping section SKILL.md)
- DECISIONS.md (entrée D51), CHANGELOG.md (entrée 2026-04-29), ARCHITECTURE.md (mention sous-pipeline post-spécimens), MEMORY.md (chantier complété + architecture actuelle)

**Reste à faire (post-commit)** :
- **Test E2E** sur VoltaPilot ou Camille : `/test-big` à partir de `3B-4` (spécimens) avec le nouvel ordre. Vérifier que styliste → spécimens → checkpoint → penseur visuel (avec fiche) → pitch → génération visuels tourne sans erreur. Vérifier dans l'output du penseur visuel que l'ancre stylistique cite des phrases de la fiche styliste. Vérifier la présence du DNA visuel en fin d'output (3-5 lignes).
- **Test qualitatif comparatif (optionnel)** : comparer le pitch produit avec un ancien run "Option A" archivé (`outputs/test-voltapilot-test-20260429-1631`) sur 6 critères (cohérence style ↔ visuel, marqueurs slop, ancrage concept, anti-CSS, etc.).

**En cas de problème détecté au test E2E** :
- Backup disponible : `.claude/skills/brand-identity/SKILL.md.bak-pre-3B7c-reorder-20260429-184811`
- Rollback possible via `git revert 6771bec`
- Si dérive du penseur visuel observée malgré le recâblage : durcir avec un 5e levier (auto-évaluation finale "si je retire `{style_choice}` de mes inputs, ma direction changerait-elle ?") qui était dans la proposition initiale mais retiré pour minimisme.
