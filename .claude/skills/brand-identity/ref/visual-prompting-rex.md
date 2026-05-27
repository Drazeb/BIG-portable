# REX — Visual Prompting : de "stock" à "correct+" (session 2026-03-31)

## Problème

Les prompts MidJourney générés par le skill `/visual-brief` produisaient des images de niveau stock (2-3/10) avec des dérives systématiques : steampunk, fantasy, registre victorien. Après itération intensive (~70 images, 15 passes de prompts, 2 outils), on est arrivé à du correct+ (7.5-8.5/10). Ce REX documente ce qui a marché et ce qui n'a pas marché.

## Ce qu'on a essayé (et pourquoi ça n'a pas marché)

### MidJourney — Prompt direct
- **Résultat** : dérives d'archétypes (steampunk, fantasy, Victorian) impossibles à corriger par le prompt seul
- **Pourquoi** : MJ a des associations profondes dans son training set. "brass + clockwork + dark" = steampunk, quels que soient les négatifs dans --no. Les mots-clés du sujet pèsent plus lourd que les instructions de registre.

### MidJourney — Anti-archétype (reality anchors)
- **Ce qu'on a fait** : ajout de "real", "documentary", "Nature magazine", "Hodinkee editorial", "contemporary" + négatifs exhaustifs (--no steampunk, fantasy, victorian, alchemy...)
- **Résultat** : registre amélioré (moins de fantasy) mais traitement toujours "propre/stock premium"
- **Pourquoi** : les reality anchors corrigent le REGISTRE mais pas le TRAITEMENT. MJ sait faire "réel" mais pas "réel + gritty + grain filmique"

### MidJourney — Traitement agressif (Kodak Tri-X 1600)
- **Ce qu'on a fait** : "shot on Kodak Tri-X 400 pushed to 1600 ISO, heavy grain, crushed blacks, harsh chiaroscuro"
- **Résultat** : MJ a produit un meilleur grain MAIS a perdu la palette (arc-en-ciel au lieu de bleu-violet restreint, retour au chaud/ambre sur le bureau)
- **Pourquoi** : quand MJ investit du "budget cognitif" sur le traitement, il relâche le contrôle sur la palette et le sujet. Les deux ne coexistent pas.

### MidJourney — --sref (Style Reference)
- **Ce qu'on a fait** : image de courbes métalliques sombres (traitement élite) comme style reference
- **Résultat --sw 100** : traitement PARFAIT (texture, grain, contraste élite) mais image 100% monochrome — la palette bleu-violet a disparu
- **Résultat --sw 50/25** : couleur revient très lentement, traitement se dégrade proportionnellement
- **Pourquoi** : la --sref écrase la palette du prompt proportionnellement à --sw. Pas de sweet spot où le traitement survit ET la couleur aussi — c'est un curseur, pas un commutateur.

### MidJourney — Remix (sur image monochrome)
- **Ce qu'on a fait** : remix des images monochromes --sref avec des prompts de recoloration
- **Résultat** : la couleur ne revient pas. L'ADN de l'image source est trop dominant.
- **Pourquoi** : Remix préserve la structure ET le traitement chromatique de l'image source. On ne peut pas "recolorer" une image monochrome par Remix.

### MidJourney — Retexture
- **Ce qu'on a fait** : retexture des images monochromes avec "blue-violet light, lavender shadows"
- **Résultat** : la couleur est appliquée comme MATIÈRE (corrosion, patine chimique colorée) pas comme LUMIÈRE
- **Pourquoi** : Retexture change les textures de surface par définition. "Blue-violet" = "peindre les surfaces en bleu-violet", pas "éclairer avec de la lumière bleu-violet"

### MidJourney — Edit/Inpainting
- **Non fonctionnel** pour notre cas (changement global de lumière, pas de zone locale à modifier)

## Solution retenue : Recraft base + Remix itératif

### Étape 1 — Recraft prompt direct (base "correcte")
- **Ce qu'on a fait** : prompts Recraft courts, naturels, avec palette HEX et références éditoriales (Nature, Kinfolk, Hodinkee)
- **Résultat** : images avec sujet fidèle, palette correcte, registre documentaire MAIS traitement trop propre/lisse (niveau Unsplash, pas Awards)
- **Pourquoi ça marche pour la base** : Recraft est littéral — il fait CE QU'ON DEMANDE sans dériver vers des archétypes. Sa faiblesse (traitement sage) est acceptable comme point de départ.

### Étape 2 — Remix Recraft (montée en qualité)
- **Ce qu'on a fait** : Remix de l'image Recraft avec un prompt de traitement agressif, en variant le niveau de similitude (3 variations : peu similaire, moyen, très similaire)
- **Prompt type** : "Make the overall image darker and grittier with visible film grain throughout, deepen the black shadows, make the [surfaces] more tactile with visible [détails de matière], intensify the [couleur directionnelle] from the [côté]"
- **Résultat** : le traitement s'améliore significativement (grain, contraste, texture) tout en PRÉSERVANT le sujet et la palette de la base. C'est le combo qu'aucune approche MJ n'a réussi.

### Étape 3 — Itération ciblée
- **Sélection** de la meilleure variation → nouveau Remix avec ajustements ciblés → re-sélection
- **Artefact identifié** : Recraft interprète "grain" comme "gouttelettes d'eau/pluie". Solution : ajouter "dry dusty atmosphere with no moisture or water" ou "remove all water droplets and rain replacing them with dry film grain texture"
- **Dégradation progressive** : chaque round de Remix dégrade légèrement la qualité (doc Recraft le confirme). Limiter à 2-3 rounds max.

### Étape 4 — Ajustements structurels
- **Étendre ou rogner** dans Recraft pour corriger le ratio (ex: 1:1 → 3:4 portrait)
- Recraft génère du contenu cohérent pour les zones ajoutées (bokeh habité, fond prolongé)

## Pourquoi ça marche

Le Remix Recraft résout le problème fondamental qu'on avait avec MJ : **séparer le sujet/palette du traitement**.

| Étape | Ce qui est fixé | Ce qui est modifié |
|---|---|---|
| Recraft base | Sujet + palette + composition | — |
| Remix | Sujet + palette (préservés) | Traitement (grain, contraste, texture) |

MJ ne peut pas faire cette séparation — quand on pousse le traitement, le sujet/palette dérivent. Recraft Remix le peut parce qu'il part d'une image existante et ne modifie que ce que le prompt décrit.

## Limites identifiées

### Limites IA universelles (ni MJ ni Recraft)
1. **Overhead 90°** : aucun outil ne produit une vraie plongée verticale stricte. ~75° est le max.
2. **DOF extrême sélective** ("bande diagonale étroite") : les deux outils produisent du bokeh doux, jamais la sélectivité d'un vrai objectif macro f/1.4.
3. **Grain filmique authentique** : aucun outil ne produit un vrai grain Kodak Tri-X. On obtient de la "texture granuleuse" mais pas du grain film.
4. **Couleur = lumière directionnelle** : les deux outils appliquent la couleur comme propriété de surface ou filtre global, pas comme éclairage directionnel venant d'un côté.

### Limites Recraft spécifiques
5. **"Grain" → "pluie"** : Recraft interprète systématiquement le vocabulaire de texture filmique comme des gouttelettes d'eau. Nécessite un contre-prompt explicite.
6. **Dégradation multi-round** : chaque Remix dégrade. Au-delà de 3 rounds, le texte manuscrit se corrompt, les formes se déforment.
7. **Plafond de traitement** : même avec Remix, Recraft reste plus "propre" que le niveau Awards. Le gap final (correct → élite) n'est pas comblé par le prompting seul.

### Limites MJ spécifiques
8. **Archétypes de training set** : brass+clockwork+dark = steampunk, leather+wood+low light = Victorian. Impossible à surmonter par le prompt.
9. **Palette instable** : MJ perd la palette quand on pousse le traitement. Les deux ne coexistent pas à haut niveau.
10. **Lavande = matière** : MJ rend les couleurs violettes comme des substances physiques (cristaux, corrosion) au lieu de lumière colorée.

## Biais de notation identifié : dérive du référentiel

### Le problème
Le DA (skill visual-brief) a systématiquement surnoté les images (~2 points au-dessus de l'évaluation externe). Raison : il compare chaque batch au batch PRÉCÉDENT (delta relatif) au lieu de comparer à la CIBLE (écart absolu à la prescription). Plus la session avance, plus le référentiel dérive vers le bas — "mieux qu'avant" remplace "conforme à la prescription."

### Comment ça s'est manifesté
- Images MJ steampunk (3/10) → images Recraft propres (6/10) notées 8/10 parce que "le steampunk est résolu"
- Images MJ --sref avec rubis violets notées 8/10 alors qu'elles revenaient au registre fantasy — le DA s'est laissé impressionner par la texture améliorée et a ignoré la régression de registre
- Le recalibrage est venu d'une session externe qui a comparé aux sites Awards (ICOMAT, POUCH, Planhat), pas aux batchs précédents

### Recommandation : gate de comparaison absolue
Avant de noter une image, le DA doit faire un check en 2 temps :
1. **Comparaison relative** (vs batch précédent) — utile pour savoir si on progresse
2. **Comparaison absolue** (vs prescription originale, critère par critère) — c'est celle qui donne la NOTE

La note finale = la comparaison absolue. La comparaison relative ne sert qu'à orienter l'itération.

### Recommandation : référentiel visuel externe
Le skill devrait demander à l'utilisateur de fournir 1-2 images de RÉFÉRENCE DE NIVEAU (pas de style — de NIVEAU de qualité) en début de session. Ces images servent d'étalon : "est-ce que notre résultat est au même niveau de craft que cette référence ?" Sans étalon externe, le DA n'a aucun moyen de calibrer "élite" vs "correct."

### Ce qui s'est passé concrètement dans cette session
- Des images de référence ont été fournies (courbes métalliques, verre ambre, liquide bleu) mais pour servir de **style reference MJ (--sref)** — pas comme étalon de niveau de qualité. Le DA les a utilisées comme input technique, pas comme benchmark.
- Le recalibrage est venu d'une **session externe** qui a comparé les résultats à des sites Awards (ICOMAT, POUCH, Planhat) et a dit "c'est du Unsplash correct, pas du Kinfolk." Mais le DA n'a jamais VU ces sites — il a lu un feedback textuel sur des captures d'écran.
- Le seul référentiel du DA était la **prescription textuelle** ("couverture Nature", "Hodinkee", "Kinfolk") — des mots, pas des images. Des mots s'interprètent de manière plus ou moins exigeante selon le contexte. Des images, non.
- **Si 2-3 captures de sites Awards avaient été montrées en début de session** comme "voilà le niveau qu'on vise", le DA aurait eu un étalon visuel concret et n'aurait pas noté 8/10 des images de niveau Unsplash.

### Implémentation recommandée
Ajouter une étape 0-bis dans le skill `/visual-brief` : après identification de la session et avant le routage, demander :
> "Avez-vous 2-3 images de référence qui montrent le NIVEAU de qualité visé (pas le style — le craft, la finition, le traitement) ? Par exemple des captures de sites que vous admirez. Ça me servira d'étalon pour évaluer mes résultats."
Si l'utilisateur en fournit, les garder en mémoire comme benchmark pour chaque gate de notation.

---

## Recommandations pour le framework

### 1. Ajouter Recraft Remix comme workflow principal pour les registres photo
Le routing actuel dit "P1-P6 → MJ exclusif". C'est faux. Pour les registres qui demandent palette fidèle + traitement non-conventionnel, le workflow devrait être :
```
Recraft base (sujet + palette) → Remix itératif (traitement) → Étendre/rogner (ratio)
```

### 2. Ajouter une Gate D — Anti-archétype fiction
Avant de finaliser un prompt MJ, vérifier : "Cette combinaison de mots-clés active-t-elle un archétype fiction connu ?" Table des archétypes à documenter dans le guide MJ.

### 3. Ajouter une Gate E — Anti-Unsplash
Après génération, vérifier : "Cette image pourrait-elle être vendue sur Unsplash/stock ?" Si oui, le traitement est trop sage. C'est différent de l'anti-stock existant (qui vérifie le sujet, pas le traitement).

### 4. Documenter les artefacts Recraft Remix
- "grain" → gouttelettes d'eau. Antidote : "dry film grain, no moisture or water"
- Dégradation multi-round : max 2-3 passes
- Le texte manuscrit se corrompt en premier — utiliser similitude très élevée si l'image contient du texte

### 5. Ajouter le workflow --sref MJ comme option de dernier recours
Pour les cas où le traitement Recraft est insuffisant ET que la palette n'est pas critique (ex: images quasi-monochromes), le workflow --sref reste viable. Documenter les valeurs --sw recommandées.

### 6. Ajouter une 6ème dimension à l'ancre stylistique : registre de réalité
Les 5 dimensions actuelles (touche, lumière, grain, abstraction, bords) ne couvrent pas le registre documentaire/fiction. Ajouter : "Registre : documentaire / éditorial / fictionnel / fantastique". Cette dimension force à vérifier que le prompt entier "sonne" comme du réel.

### 7. Le penseur visuel devrait flaguer les combinaisons MJ dangereuses
Quand la direction visuelle prescrit "mouvement horloger patiné en macro basse lumière", le penseur devrait ajouter : "⚠ MJ steampunk trigger — ancrer dans le réel". Le DA (skill visual-brief) ne peut pas deviner quelles combinaisons sont dangereuses sans cette alerte.

### 8. Documenter Recraft comme outil photo dans le guide
Le guide Recraft actuel ne couvre que les registres illustration (I1, I2, I4, I7, T2). Il faut ajouter une section "Photo réaliste" avec : modèle recommandé (V4 Pro Realistic Image), structure de prompt, styles préfaits utiles, workflow Remix, artefacts connus.

## Métriques de la session

| Métrique | Valeur |
|---|---|
| Images générées | ~70+ |
| Passes de prompts | ~15 |
| Outils testés | MJ v7 (prompt, --sref, Remix, Retexture, Edit), Recraft V4 Pro (prompt, Remix, Étendre) |
| Temps estimé | ~3h |
| Niveau initial (MJ direct) | 2-3/10 (stock/steampunk) |
| Niveau intermédiaire (Recraft direct) | 5-7/10 (correct/Unsplash) |
| Niveau final (Recraft + Remix) | 7.5-8.5/10 (correct+) |
| Gap restant vers élite (9-10) | Traitement encore trop sage vs sites Awards |

## Dernière mise à jour : 2026-03-31
