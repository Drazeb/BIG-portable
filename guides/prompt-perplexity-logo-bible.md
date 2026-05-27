# Prompt Perplexity — Recherche : Framework Elite de Création de Logo

## Contexte

Je développe un système automatisé de création d'identité de marque (Brand Identity Generator). Le système utilise Claude (LLM Anthropic) comme "directeur artistique IA" qui analyse un brief marketing complet, génère des concepts stratégiques, puis produit des livrables visuels (style-tiles HTML, iconographie, data-viz, direction photo, etc.).

**Le problème qu'on résout** : Pour la partie LOGO spécifiquement, le LLM ne peut pas générer de logos visuels de qualité (limite structurelle confirmée). On adopte donc une approche hybride : Claude conçoit le concept créatif du logo et génère un prompt optimisé → l'utilisateur exécute ce prompt dans Recraft AI (outil de génération vectorielle SVG) → le SVG revient dans le pipeline.

**Ce qu'on construit** : Un "cerveau de designer logo d'élite" — un fichier de référence (~bible) qui encode les principes, frameworks et méthodologies que le système utilisera pour :
1. Transformer un brief stratégique (tension de marque, positionnement, curseurs créatifs, concept choisi) en un concept logo précis
2. Évaluer et itérer sur ce concept
3. Traduire ce concept en un prompt visuel optimal pour un outil IA de génération d'image

## Ce que je connais déjà (ne pas me renvoyer ça)

Je maîtrise déjà ces fondamentaux — pas besoin de les couvrir :

- **Principes Gestalt** : proximité, continuité, figure/fond, similarité, closure
- **Scalabilité** : favicon test (16px), monochrome test, inversion test, smartwatch test
- **Negative space** et golden ratio / grilles de construction
- **Taxonomie morphologique** : wordmark, lettermark, pictorial mark, abstract mark, emblem, monogram, combination mark, mascot
- **Références classiques** : Paul Rand, Massimo Vignelli, Saul Bass (leurs principes généraux)
- **Erreurs classiques** : trop de détails, clichés sectoriels, manque de distinctivité, non-scalable
- **Prompt engineering pour Midjourney/Recraft** : structure de prompt, paramètres, keywords — cette partie est déjà couverte séparément

## Ce que je cherche (les TROUS à combler)

### 1. Méthodologies structurées des grands studios de branding (2023-2026)

Comment les studios d'élite passent concrètement du brief au concept logo ? Je cherche des **frameworks méthodologiques documentés**, pas des principes généraux.

Exemples de studios ciblés : Pentagram, Wolff Olins, Collins, Koto, Landor, Interbrand, DixonBaxi, Porto Rocha, Sagmeister & Walsh, Base Design.

Questions spécifiques :
- Quelles sont les étapes structurées de leur processus créatif logo ? (pas le process business/client, le process CRÉATIF interne)
- Comment passent-ils de l'insight stratégique au concept visuel ? Quel est le "pont" entre stratégie et forme ?
- Utilisent-ils des frameworks nommés (ex: "brand idea → visual metaphor → form exploration → refinement") ?
- Quelle place pour le sketching exploratoire vs la construction géométrique ?
- Comment gèrent-ils la tension entre originalité et fonctionnalité ?

### 2. Grille d'évaluation objective d'un logo (critères de DA élite)

Je cherche les **critères objectifs et mesurables** qu'un directeur artistique senior utilise pour évaluer un logo. Pas "est-ce que c'est joli" mais une grille structurée.

Questions spécifiques :
- Existe-t-il des grilles d'évaluation publiées par des DA ou des écoles de design reconnues ?
- Quels sont les critères au-delà de la scalabilité et de la lisibilité ? (ex: mémorabilité, distinctivité, pertinence sémantique, longévité, adaptabilité système)
- Comment évalue-t-on la "justesse" d'un logo par rapport à un positionnement de marque ?
- Y a-t-il un scoring ou ranking utilisé en pratique dans les agences ?
- Le concept de "logomark stress test" — quels tests concrets au-delà du favicon/monochrome ?

### 3. Principes modernes de design de logo (2024-2026 spécifiquement)

Les tendances récentes qui FONCTIONNENT (pas les effets de mode éphémères), validées par les praticiens.

Questions spécifiques :
- Quelles évolutions post-flat design sont durables ? (néo-brutalisme, dimensional logos, variable logos, etc.)
- Comment le "debranding" (simplification extrême type Mastercard, Google) influence-t-il la pratique ?
- Les "responsive logos" / logos adaptatifs — est-ce un standard maintenant ou encore émergent ?
- Impact de l'IA sur les attentes esthétiques : les logos doivent-ils être PLUS distinctifs qu'avant pour sortir du bruit généré par l'IA ?
- Quelles sont les directions esthétiques qui émergent en réaction à la saturation IA (imperfection volontaire, craft, hand-drawn revival, etc.) ?

### 4. Le pont stratégie → forme : comment traduire un positionnement en choix visuels

C'est le coeur de ce que je cherche. Comment un designer expert fait le SAUT entre "la marque est positionnée sur X avec une tension Y" et "donc le logo sera Z" ?

Questions spécifiques :
- Existe-t-il des frameworks documentés pour mapper des attributs de marque (ex: "innovation", "confiance", "audace") vers des choix formels (angulaire vs organique, géométrique vs libre, statique vs dynamique) ?
- Comment les sémioticiens du design (type Groupe µ, ou plus récents) analysent-ils la signification des formes dans les logos ?
- Y a-t-il des recherches récentes (2023-2026) sur la perception des formes géométriques en branding ?
- Le concept de "visual metaphor" dans le logo — comment les meilleurs designers la construisent-ils ? (pas juste "on a mis une flèche dans le FedEx", mais le process de pensée qui y mène)
- Comment quantifier/structurer le niveau d'abstraction d'un logo ? (figuratif → stylisé → abstrait → géométrique pur)

### 5. Systèmes de logos (logo comme partie d'un système d'identité)

Questions spécifiques :
- Comment les studios modernes conçoivent-ils le logo dès le départ comme PARTIE d'un système (pas isolé) ?
- Le concept de "design tokens" appliqué au logo — des éléments du logo qui se retrouvent dans l'iconographie, les patterns, etc.
- Comment Wolff Olins / Collins construisent-ils cette cohérence système dès le logo ?
- Best practices pour que le logo "dialogue" avec le reste de l'identité visuelle

### 6. Anti-patterns et pièges de la création de logo IA-assistée

Questions spécifiques :
- Quels patterns visuels les outils IA (Midjourney, DALL-E, Recraft) génèrent-ils de manière répétitive ? (pour qu'on les évite explicitement)
- Quels "tells" permettent de repérer un logo généré par IA ?
- Comment les designers pros "cassent" les propositions IA pour les rendre uniques ?
- Y a-t-il des publications/articles (2024-2026) qui analysent les biais visuels des IA en logo design ?

## Format de réponse souhaité

Pour chaque section (1 à 6), je voudrais :
- Les **frameworks/méthodologies nommés** avec leurs sources
- Des **citations directes** de designers ou DA reconnus (avec nom + date)
- Des **principes actionnables** (pas des généralités)
- Des **exemples concrets** de logos récents (2023-2026) qui illustrent les principes
- Les **sources** (articles, livres, conférences, interviews) avec dates

**Période cible** : Privilégier absolument les sources de 2023 à février 2026. Accepter les sources plus anciennes UNIQUEMENT si ce sont des références fondatrices toujours citées par les praticiens actuels.

**Niveau de détail** : Professionnel / praticien. Pas de vulgarisation grand public. Je m'adresse à quelqu'un qui va coder un système expert — j'ai besoin de principes suffisamment précis pour être traduits en instructions algorithmiques.

**Ce que je NE cherche PAS** :
- Des conseils de prompt engineering pour Midjourney/Recraft (déjà couvert)
- Des recommandations d'outils IA (déjà couvert)
- Des principes basiques de design (déjà connus)
- Du contenu marketing/affilié sur des logo makers SaaS
