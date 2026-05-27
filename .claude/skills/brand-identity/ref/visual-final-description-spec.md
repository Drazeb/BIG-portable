# Spec — Format de description du visuel final (consommé par Phase 3B-7d Pitch)

## Pourquoi ce format

Ce document spécifie ce qu'un skill externe (générateur d'image final via MJ + Nano Banana) doit produire en sortie pour que le pitch designer (Phase 3B-7d) puisse ancrer son travail dans l'image générée.

Le pitch ne re-décrit pas l'image (il la lit). Le pitch tisse la métaphore directrice de l'image dans son récit (Ancrage Brief, Intention créative, Direction visuelle, Bénéfices business). Sa qualité dépend directement de la richesse et de la précision de cette description.

Ce format est **orienté ancrage narratif**, pas orienté production technique. La fiche de production (prompts MJ, paramètres, itérations) reste interne au skill externe — elle ne fait pas partie de ce que le pitch consomme.

**Anti-contamination** : la fiche est lue par un LLM qui doit prendre des décisions narratives. Elle ne doit donc pas contenir de listes d'exemples qui formeraient un menu déguisé. Chaque champ décrit une dimension à renseigner ; le rédacteur du fichier renseigne la valeur unique qui correspond à l'image produite.

---

## Format à produire (template)

```markdown
# Description du visuel final — {brand} · concept {N}

## A. Identité du visuel

- **Fichier source** : chemin absolu ou relatif du fichier image livré
- **Outil de génération** : nom de l'outil ayant produit l'image finale (MJ / Nano Banana / autre)
- **Dimensions** : largeur × hauteur en pixels
- **Aspect ratio** : ratio explicite (forme : portrait / paysage / carré laissée libre, mais le ratio numérique est obligatoire)

## B. Sujet et métaphore

- **Sujet principal** : ce qu'on voit dans l'image, en 1 phrase factuelle
- **Métaphore narrative** : ce que l'image INCARNE par rapport au concept narratif retenu, en 1-2 phrases. C'est la traduction visuelle de la métaphore directrice du concept.
- **Lien au concept** : comment l'image sert le récit du pitch, en 1-2 phrases. Pourquoi CETTE image et pas une autre. Quel territoire principal / secondaire elle incarne.

## C. Composition et cadrage

- **Cadrage** : distance du sujet (macro, mi-distance, large — termes libres mais explicites)
- **Composition** : règle d'organisation spatiale (asymétrique, centrée, spread, monolithique — formuler avec un mot précis)
- **Élément dominant dans l'image** : ce sur quoi l'œil se pose en premier
- **Espace négatif** : pourcentage approximatif du cadre + position (à gauche / en haut / autour / etc.)

## D. Atmosphère

- **Lumière** : source + direction + température (en Kelvin si pertinent) + contraste
- **Grain / matière** : type de grain (filmique, numérique, quasi-imperceptible) + qualité de surface
- **Palette dans l'image** : 3 à 5 hex codes dominants observés effectivement dans le rendu (pas la palette de marque, mais ce que l'image montre VRAIMENT)
- **Mood général** : 1 phrase qui capture l'atmosphère (ce que ressent le spectateur)

## E. Ancre stylistique (traçable depuis la fiche styliste)

Chaque dimension est renseignée AVEC une citation de la phrase de la fiche styliste retenue qui la justifie. Format obligatoire : `valeur (Source dans la fiche : "phrase exacte")`. Si une dimension ne peut être ancrée dans la fiche, le signaler explicitement (`pas d'ancrage direct dans la fiche, dérivé par cohérence du registre`).

- **Registre visuel** : famille à laquelle appartient l'image (photographie éditoriale, photo macro matière, illustration flat, infographique, etc. — termes libres)
- **Traitement lumineux** : comment la lumière incarne le style retenu
- **Grain / matérialité** : comment la texture incarne le style retenu
- **Niveau d'abstraction** : figuratif / semi-abstrait / abstrait pur, et pourquoi
- **Traitement des bords** : nets / doux / mixtes — sur quelles zones de l'image

## F. Anti-patterns (ce que l'image n'est PAS)

3 à 5 puces qui décrivent ce que l'image refuse explicitement. Cible : les codes du Ventre Mou sectoriel + les clichés du registre choisi qu'on a évités. Format : "Pas X — parce que Y" (chaque ligne dit ce qu'on a refusé et pourquoi). Cette section nourrit la section "Position ZAG" et "Anti-territoire" du pitch.

## G. Intégration recommandée dans le style-tile

Au moins 1 option (3 max). Chaque option décrit comment l'image vit dans le style-tile :
- **Option [N] — [nom court]** :
  - Position dans la composition (Voice Block / Atmosphere / zone médiane)
  - Comment elle dialogue avec le texte (overlay, side-by-side, derrière, etc.)
  - Ratio occupé dans la vue
  - Quel est le bénéfice de cette option (signature, lecture, ancrage atmosphérique)

## H. DNA visuel transmissible

Bullet list de 3 à 5 lignes ultra-condensées, qui sera utilisée pour calibrer toute itération future (re-prompt MJ, recadrage, génération de variantes Recraft) sans avoir à relire toute la fiche. Format type :
- Registre : ...
- Lumière : ...
- Grain : ...
- Palette ciblée : ...
- Référence ergonomique : ... (1-2 photographer / illustrateur / studio identifiés, vérifiables)

## I. Niveau d'évaluation

Note honnête sur 10 du visuel produit + gap résiduel vers 10 si applicable. Cette section ne fait pas partie du pitch lui-même mais permet à l'utilisateur de calibrer ses attentes.

## J. Ce que le pitch peut tisser

3 à 5 angles narratifs que le pitch designer peut développer dans son output. Cette section ne dicte pas le pitch — elle pointe les leviers narratifs activés par l'image. Le pitch designer reste libre de les utiliser ou non. Format type :
- Pour la section "Intention créative" du pitch : la métaphore directrice peut être tissée comme [angle narratif]
- Pour la section "Pont Brief → Créa" / Univers : l'image incarne [territoire X] par [tel choix visuel]
- Pour la section "Direction visuelle" : la cohérence palette + typo + image se justifie par [tel angle]
- Pour la section "Bénéfices business [Différenciation]" : l'image éloigne du Ventre Mou par [tel écart explicite]
- Pour la section "Avis du DA — Force majeure" : la cohérence concept ↔ image ↔ palette ↔ typo est totale par [tel argument]
```

---

## Sections OBLIGATOIRES (minimum vital)

Si le skill externe doit produire un format compact, ces 6 sections sont le socle indispensable pour que le pitch puisse s'ancrer :

| Section | Pourquoi obligatoire |
|---|---|
| **A. Identité du visuel** | Sans le fichier source + dimensions + ratio, le pitch ne peut pas dimensionner ses options d'intégration |
| **B. Sujet et métaphore** | C'est le pivot narratif. Sans cela, le pitch ne peut pas tisser la cohérence concept ↔ image |
| **D. Atmosphère** | Le pitch utilise palette dans l'image + lumière + grain pour justifier la cohérence palette + typo + image |
| **F. Anti-patterns** | Le pitch utilise les anti-patterns pour la section "Anti-territoire" + "Bénéfices business [Différenciation]" |
| **G. Intégration recommandée** | Le pitch a besoin d'au moins 1 option d'intégration pour structurer la section "Direction visuelle" et "Visuels recommandés" |
| **H. DNA visuel transmissible** | Permet la cohérence avec les phases aval (Phase 4 styletile, Phase 6A Batch 2 chapitre dataviz) |

Les sections C / E / I / J sont **fortement recommandées** mais peuvent être omises si l'image est très simple ou si le pipeline de production externe ne sait pas les renseigner. Dans ce cas, le pitch fera un travail légèrement moins fin mais reste fonctionnel.

---

## Exigences de qualité (à respecter par le skill externe)

1. **Traçabilité fiche styliste (section E)** : chaque dimension de l'ancre stylistique CITE textuellement la phrase de la fiche styliste qui la justifie. Si pas d'ancrage possible, le signaler. C'est la règle D51 (le penseur visuel DÉRIVE depuis la fiche, n'invente pas).

2. **Métaphore narrative non-littérale (section B)** : la métaphore narrative ne décrit pas le sujet de l'image (qui est déjà dans "Sujet principal"). Elle décrit ce que l'image INCARNE — un fragment de temps, un signe vital, un retrait, un sédiment. C'est ce qui permet au pitch de tisser le récit, pas une légende d'image.

3. **Anti-patterns spécifiques au cas (section F)** : les anti-patterns ne sont pas génériques ("pas de stock photography"). Ils citent les codes spécifiques du Ventre Mou sectoriel évités (codes typés du brief) ET les clichés du registre choisi évités (codes typés du style retenu). Format obligatoire : "Pas X — parce que Y".

4. **Hex codes vérifiables (section D, palette dans l'image)** : la palette renseignée correspond à ce qui est OBSERVABLE dans l'image, pas à la palette de marque. Si l'image dérive de la palette de marque, le signaler explicitement (par exemple : "fidèle à la palette c1 à 95%, gap résiduel sur l'accent qui tire légèrement vers Y").

5. **Référence ergonomique vérifiable (section H, DNA)** : si une référence est citée (photographer, illustrateur, studio), elle doit être réelle et vérifiable (pas inventée par le LLM).

---

## Comment le pitch consomme ce fichier

Le subagent Phase 3B-7d (pitch designer) reçoit ce fichier en input direct. Il l'utilise pour :

- Construire la section "Pont Brief → Créa" du pitch (sous-section Univers) — en s'appuyant sur la métaphore narrative (B) + le sujet (B) + l'ancre stylistique (E)
- Construire la section "Direction visuelle" — en s'appuyant sur la palette dans l'image (D) + le grain (D) + l'atmosphère (D) + l'intégration recommandée (G)
- Construire la section "Anti-territoire" / "Bénéfices business [Différenciation]" — en s'appuyant sur les anti-patterns (F)
- Construire la section "Visuels recommandés" — en s'appuyant sur le sujet (B) + cadrage (C) + composition (C) + lumière (D) + intégration (G)
- Construire la section "Avis du DA — Force majeure" — en s'appuyant sur la cohérence concept ↔ image ↔ palette ↔ typo (croisement de toutes les sections)

Le pitch ne re-décrit pas l'image. Il cite, intègre, tisse.

---

## Liens projet

- Plan de chantier penseur visuel : `ref/plan-refactor-penseur-visuel-EN-COURS.md`
- Template prompt Perplexity : `ref/perplexity-prompt-template.md` (en amont)
- REX itération prompt Perplexity : `ref/perplexity-prompt-rex.md`
- Décision D51 (styles AVANT direction visuelle) : `DECISIONS.md`
- Décision D52 (Phase 4 artefact hybride avec ancrage support) : `DECISIONS.md`
