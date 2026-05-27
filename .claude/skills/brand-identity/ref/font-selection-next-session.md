# Rapport pour la prochaine session — Sélection typographique Phase 3B

## Contexte

Session du 17-18 mars 2026 : refonte complète de la Phase 3B + exploration approfondie de la sélection typographique visuelle. Le REX complet est dans `ref/font-selection-rex.md`.

## État actuel (committé)

### Ce qui fonctionne
- Phase 3B en 3 subagents parallèles (1 par concept) — qualité supérieure au monolithique
- Préférences esthétiques : liste individuelle, sélection per-concept en 3B-0
- Cadre de compatibilité esthétique a priori en 3B (pas de gate a posteriori)
- Préférences esthétiques absentes de 3A (territory-first protégé)
- Script de génération de planches : support split mode + tags catégorie
- Gate numéros uniquement pour les shortlists (compliance ~100%)
- Assemblage pitch après 3B-bis (impossible de sauter la vérification specimen)

### Ce qui ne fonctionne pas encore
- Le shortlisteur fait des choix **corrects mais pas optimaux** pour les fonts display
- Le meilleur choix (#02 Abril Fatface pour un concept agraire) n'émerge dans aucun test
- Les fonts DECO sont parfois shortlistées malgré les tags enrichis

## Ce qu'il reste à faire

### 1. Tester l'approche par élimination
Au lieu de "shortliste 7 parmi 50", demander "pour chaque font (#01 à #50), dis COMPATIBLE ou INCOMPATIBLE avec ce concept (1 mot)". Les fonts restantes après élimination forment la shortlist naturelle.

**Pourquoi ça pourrait marcher** : ça force un jugement binaire sur CHAQUE font (pas de skip). Le LLM doit regarder chacune et décider. C'est structurellement différent de "trouve les 7 meilleures" où il s'arrête aux premières acceptables.

**Comment tester** : lancer un subagent avec planches de 10 + tags enrichis + consigne d'élimination sur le concept Le Sillon Tracé. Vérifier si #02 Abril Fatface est dans les "COMPATIBLE".

### 2. Formaliser les anti-patterns typographiques
Créer un fichier `ref/font-matching-antipatterns.md` avec des règles de croisement concept × font :
- Concept terreux/agraire/dense → PAS de didone capillaire (Bodoni, Cormorant). Chercher slab, bold serif, condensé massif.
- Concept technique/analytique → PAS de serif éditorial classique. Chercher sans géométrique, mono, condensé technique.
- Concept organique/vivant → PAS de géométrique pure. Chercher humaniste, variable, expressif.

Le subagent reçoit ce fichier et l'utilise comme filtre AVANT de shortlister.

### 3. Implémenter les planches de 10 avec tags enrichis
- Modifier le script pour générer les planches officielles (pas juste des tests)
- Regénérer les 6 pools (display A1/A2/A3, body A1/A2/A3) en planches de 10
- Ajouter les tags : SERIF/SANS pour display, MONO/PROP pour body, DECO-xxx pour les décoratives
- Mettre à jour le SKILL.md avec le nouveau flux shortlisteur

### 4. Tester les pools A1 et A2
- Faire le même audit de catégorisation (double run en planches de 2) sur les 4 pools restants
- Identifier les fonts à retirer ou à tagger
- Regénérer les planches

### 5. Test en prod (test-big)
- Lancer un test-big complet en 3B avec les nouvelles planches
- Vérifier que le flux shortlisteur → designer → specimen → assemblage fonctionne de bout en bout
- Auditer les choix typographiques

## Fichiers clés à lire en début de session

| Fichier | Pourquoi |
|---|---|
| `ref/font-selection-rex.md` | REX complet de cette session — tout ce qui a été testé et les résultats |
| `SKILL.md` section 3B | L'architecture actuelle (shortlisteur + designer + specimen) |
| `lib/font-pool-contact-sheet.mjs` | Le script de génération de planches (support split + tags) |
| `ref/font-pools/*-mapping.json` | Les mappings numéro → nom pour chaque pool |

## Questions ouvertes

1. L'approche par élimination résout-elle le problème de matching concept × font ?
2. Les anti-patterns typographiques formalisés améliorent-ils les choix ?
3. Faut-il une "feedback loop" simulée (montrer des bons et mauvais matchs en exemple) ?
4. Le designer sur mini-planche de 7 fait-il un meilleur choix final que le shortlisteur ?
