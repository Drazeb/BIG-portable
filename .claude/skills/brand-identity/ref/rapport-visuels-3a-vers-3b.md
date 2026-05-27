# Rapport : Déplacer "Visuels recommandés" et "Graine Logo" de Phase 3A vers Phase 3B

## Contexte — Le problème de contamination sectorielle en Phase 3A

La Phase 3A génère les concepts narratifs (métaphores, postures, registres de communication). Son objectif : produire des concepts **territory-first** — c'est-à-dire des concepts dont la métaphore ÉMERGE des mots-clés des territoires créatifs, pas du secteur d'activité de la marque.

Pour atteindre cet objectif, le subagent 3A est **volontairement isolé** de toute information sectorielle :
- Il ne lit PAS le brief
- Il ne lit PAS le scoping
- Il ne reçoit PAS le nom de la marque (même les output paths sont anonymisés)
- Les territoires, le profil esthétique et le ventre mou sont **décontaminés** par un subagent dédié qui retire tout marqueur sectoriel (noms propres, jargon, références métier)

Ce dispositif anti-contamination a été mis en place et validé sur 2 marques (Atelier Vermeil — compostage, et Camille — conseil en stratégie de marque). Résultat : passage de 0/3 territory-first à 3/3 territory-first sur les deux marques.

## Le problème résiduel — Visuels et Logo forcent la reconstruction sectorielle

Malgré la décontamination, le texte d'élaboration des concepts contient encore des termes sectoriels (ex: "compost fumant", "camions de collecte", "tables couvertes d'épluchures" pour Atelier Vermeil). Ces termes apparaissent principalement dans deux sections :

1. **"Visuels recommandés"** — le subagent doit imaginer des photos/illustrations concrètes qui serviraient le concept. Pour ce faire, il est FORCÉ de se projeter dans le concret du métier de la marque. Même avec des inputs décontaminés, la recommandation visuelle exige de répondre à "à quoi ça ressemble en vrai ?" — ce qui active la reconstruction sectorielle.

2. **"Graine Logo"** — même mécanisme : imaginer une forme/symbole pour le logo pousse le subagent à se demander "quel est l'objet symbolique de cette marque ?", ce qui ramène au secteur.

Ces deux sections sont les derniers vecteurs de contamination identifiés. Les MÉTAPHORES sont propres (territory-first), mais le texte visuel/logo réintroduit du secteur.

## Diagnostic — Mauvaise répartition des responsabilités

Le subagent 3A est un **stratège narratif**. Voici ce qu'il a comme "cerveau" (fichiers de référence qu'il lit) :

| Fichier | Ce qu'il apporte |
|---------|-----------------|
| `persona-and-rules.md` | Persona DA + calibrage curseurs A×B |
| `bible-design-strategie.md` | Théorie design, positionnement, stratégie |
| `phase3-pitch-example.md` | 1 exemple concept-only (Maison Kaolin) |

Ce qu'il n'a PAS (volontairement, pour l'anti-contamination) :
- `master-style-guide.md` — guide de style complet
- `html-showroom-spec.md` — font pools, techniques CSS, compositions
- Exemples design complets (prudent/décalé/rupture avec specs visuelles)
- Le brief complet
- Le scoping complet (avec ventre mou DESIGN = codes visuels du secteur à éviter)
- Les signaux visuels de résolution de tension

On demande donc à un subagent **sans framework visuel** de faire des recommandations visuelles. Résultat : il improvise en reconstruisant le secteur implicitement.

Le subagent 3B, lui, a TOUT le framework nécessaire :
- `master-style-guide.md`
- `html-showroom-spec.md` (font pools, CSS, compositions)
- 3 exemples design complets
- Brief + scoping complets (avec ventre mou design, signaux visuels)
- Les concepts narratifs validés comme input

Il dérive déjà la palette, la typo, la surface, l'artefact, la philosophie d'interaction, le registre atmosphérique, la composition, la carte d'inspiration. Les visuels recommandés et la graine logo sont les seuls éléments visuels qui échappent à cette logique de dérivation.

## Proposition de solution

### Ce qui change en Phase 3A

Retirer les sections **"Visuels recommandés"** (section 3) et **"Graine Logo"** (section 4) du template de sortie du subagent 3A.

Le concept narratif produit par 3A deviendrait :
1. Ancrage Territoires (inchangé)
2. Intention créative (inchangé)
3. Avis du DA (inchangé — actuellement section 5, deviendrait section 3)

Fichiers impactés en 3A :
- `phases/phase-3a-concepts.md` — retirer les sections 3 et 4 du template, renuméroter
- `examples/phase3-pitch-example.md` — retirer les sections correspondantes de l'exemple Maison Kaolin
- `SKILL.md` section Phase 3A — mettre à jour la description du format de sortie si elle mentionne visuels/logo

### Ce qui change en Phase 3B

Ajouter la responsabilité de **"Visuels recommandés"** et **"Graine Logo"** au subagent 3B.

Le subagent 3B produit déjà pour chaque concept :
- Ancrage Brief (repris de 3A + pont Brief→Créa)
- Intention créative (reprise de 3A)
- Direction visuelle (typo, palette, surface, atmosphère, etc.)
- Carte d'Inspiration
- Visuels recommandés (actuellement "REPRENDRE de Pass A, affiner")
- Avis du DA

Les changements dans `phases/phase-3b-design.md` :
1. **"Visuels recommandés"** : au lieu de "REPRENDRE de Pass A, affiner", le subagent 3B DÉRIVE les visuels à partir du concept narratif + du brief + du profil esthétique. Il a tout le contexte nécessaire (secteur, style guide, ventre mou design) pour faire une recommandation informée. Le registre visuel (photo vs illustration, familles visuelles) peut être déplacé dans le prompt 3B.
2. **"Graine Logo"** : ajouter une section dans le template 3B. Le subagent 3B est mieux placé pour imaginer une direction logo parce qu'il connaît la direction visuelle complète (palette, typo, surface) et le secteur.

### Ce qui ne change PAS

- Le flow orchestrateur (3A → checkpoint → 3B) reste identique
- La décontamination en amont de 3A reste en place
- La Phase 3C (visuels de référence / prompts MidJourney) continue de lire les visuels recommandés depuis le pitch — simplement, ils viendront de 3B au lieu de 3A
- La Phase Logo (si utilisée) continue de fonctionner normalement

### Point d'attention

Le répertoire des familles visuelles (Illustration : 10 familles, Photographie : 10 familles) est actuellement dans `phase-3a-concepts.md`. Il faudra le déplacer dans `phase-3b-design.md` pour que le subagent 3B puisse s'y référer. Ce répertoire est un outil de classification, pas de contamination — il peut être déplacé tel quel.

## Résumé

| Aspect | Avant | Après |
|--------|-------|-------|
| Visuels recommandés | Générés en 3A (sans framework visuel), repris en 3B | Dérivés en 3B (avec framework complet + contexte sectoriel) |
| Graine Logo | Générée en 3A (sans contexte design) | Dérivée en 3B (avec direction visuelle complète) |
| Concept 3A | 5 sections | 3 sections (ancrage + intention + avis DA) |
| Contamination résiduelle | Visuels/logo forcent la reconstruction sectorielle | Supprimée — 3A ne fait plus de projection visuelle concrète |
| Qualité des recommandations visuelles | Improvisée (pas de style guide, pas de ventre mou design) | Informée (style guide + exemples + ventre mou design + brief) |
