# Finition Élite — Core

Standard universel de fabrication CSS. S'applique quel que soit le curseur A. Ce n'est pas de la créativité — c'est la qualité de fabrication.

**Portée** : importé par Phase 4 (styletile + artefact), Batch 2, Batch 3.

---

## Ombres portées

Les ombres servent 1 à 2 éléments CLÉS par section (CTA, accent), pas chaque conteneur. Un composant qui se distingue par son fond ou une bordure fine n'a pas besoin d'ombre — c'est un choix légitime.

Quand utilisées, les ombres empilent au moins 2 niveaux :
- Contact (courte, nette)
- Mid-range (diffuse)
- Ambient (large, subtile)

Les valeurs exactes sont libres. Un concept intentionnellement flat/shadowless (brutalist, papier) est légitime — mais une shadow simple isolée ne l'est pas.

## Échelle d'ombres cohérente

Quand le concept utilise des ombres, déclarer une échelle nommée (sm, md, lg, xl) et l'utiliser de façon ordonnée. Si une ombre est CLAIREMENT visible à distance normale de lecture, elle est trop forte — l'élite tend vers la subtilité, pas la démonstration. Une ombre trop appuyée signale un manque de confiance dans la hiérarchie typographique et spatiale.

## Ombres tintées sur la teinte de fond

Préférer les ombres tintées (teinte du fond ou de l'accent, à très basse opacité) plutôt que le noir pur opacifié. Une ombre noire `rgba(0,0,0,…)` plaquée sur un fond chaud crée une cassure chromatique. L'ombre doit appartenir à la même atmosphère que le fond — c'est elle qui fait sentir la profondeur sans casser la palette.

## Easing physiques

INTERDIT dans les transitions d'interaction : `ease`, `ease-in-out` seuls.

Déclarer dans `:root` au moins 2 courbes nommées (ex. `--ease-out-expo`, `--ease-out-back`) et les utiliser dans TOUTES les transitions.

## Rythme de spacing

Les sections d'un style-tile ou les chapitres d'un batch ne doivent PAS avoir le même `padding-block`. Variation visible entre les zones. Le Voice Block est immersif, l'Artefact adapte sa densité, l'Atmosphere conclut. Pas 3× `var(--space-2xl)`.

## Transitions multi-property

Au hover, au moins 2 propriétés changent simultanément (ex. background + box-shadow, border-color + background). Durées légèrement décalées quand possible (transition-fast sur le border, transition-base sur le background).

## Retenue des hovers

Les transformations hover sont subtiles : scale 1.01–1.02 max, pas 1.05+. Aucune propriété ne saute brutalement — tout est transitionné. Le lift au hover (translateY) est banni par `anti-slop-blacklist-core.md §1`.

## Parcimonie de l'accent couleur

La couleur accent est un ÉVÉNEMENT visuel — 1 à 2 éléments par viewport maximum. Le reste vit dans la famille de la couleur dominante. Un fond entier en couleur accent sur une section est plus impactant que 10 petits accents dispersés.

## Saturation calibrée par luminance

Aux extrêmes de luminance (proche blanc, proche noir), désaturer progressivement les teintes pour éviter l'aspect criard. La saturation maximale appartient aux mid-tones, pas aux highlights ni aux shadows. Une couleur très saturée à très haute luminance produit du néon involontaire ; à très basse luminance, elle produit une boue chromatique.

## Pas de gris sur fond coloré

Sur un fond teinté (même légèrement), le texte gris pur paraît délavé et sale. Préférer une nuance plus foncée du fond lui-même (mix de la teinte de fond avec du noir/blanc selon le mode) — le texte garde sa lisibilité tout en appartenant à la même famille chromatique.

## Dark mode n'est pas une inversion

Le dark mode ne se construit pas en inversant mécaniquement les couleurs du light mode. Construire la profondeur via des paliers de luminance entre surfaces (background, surface, elevated surface), pas via des ombres empilées. Désaturer les accents pour compenser le fond sombre — un accent vif sur fond noir vibre douloureusement. Les neutres en dark mode restent teintés, pas du gris pur.

## Couche graphique d'atmosphère

Les fonds plats sont un défaut, pas une neutralité. Une couche graphique d'atmosphère donne du corps : grain (texture fine, pseudo-element en `position: fixed`), gradients radiaux ou coniques diffus, masses colorées semi-transparentes. À doser selon le registre — discrète sur un concept éditorial, plus prononcée sur un concept éditorial-immersif. La règle : on ne la voit pas du premier coup, on sent juste que la surface n'est pas morte.

## Alignement optique

L'alignement mathématique (x, y identiques) ne suffit pas. Quand l'œil perçoit un décrochage entre deux éléments alignés "à la règle" (typo à côté d'un cercle, baseline à côté d'un capitale), corriger avec une marge négative légère pour rétablir l'alignement OPTIQUE. Vaut surtout pour les CTA, les badges, les premières lettres de titres — partout où une glyph côtoie une forme géométrique.

---

## Motion principles

## Spring physics premium, pas linear

Sur les composants premium, préférer un comportement type "spring lourd" (descente progressive vers la cible, sans rebond) plutôt qu'un linear ou un easing standard symétrique. Pas de spring bouncy — le rebond signale un produit grand public, pas un produit élite. Le mouvement doit avoir du POIDS, comme une masse qui se pose.

## Seuil perceptif court = instantané

En-dessous d'un seuil perceptif court, une transition est perçue comme instantanée. Cibler ce seuil pour les micro-feedbacks (hover, focus, toggle) — au-delà, l'utilisateur attend ; en-dessous, il ne voit pas la transition mais sent la fluidité. Les transitions plus longues sont réservées aux changements d'état spatiaux (ouverture de panneau, transition de section).

## Cap sur les staggered

Les animations staggered (cascade d'éléments) doivent capper leur délai cumulé total. Au-delà d'un seuil court, les derniers éléments arrivent si tard que l'utilisateur perçoit l'animation comme un bug ou un défaut de chargement. Mieux vaut un stagger serré sur 3-4 éléments visibles qu'un stagger ample sur 12 éléments dont la moitié arrive après que l'œil a quitté la zone.

## Démarrer avant d'avoir fini

Préférer faire apparaître le DÉBUT du travail (skeleton, état intermédiaire, placeholder structuré) plutôt que d'attendre le résultat complet. Le temps perçu se décale : l'utilisateur voit que ça avance, donc il attend mieux. Un spinner seul ne donne aucune information, le skeleton donne la forme à venir.

---

## Discipline d'exécution

## Ordre de construction

L'ordre de construction d'un style-tile ou d'un artefact n'est pas neutre :
1. Structure HTML sémantique
2. Layout et espace (grid, flex, spacing)
3. Typographie et couleur (la palette habille la structure)
4. États interactifs (hover, focus, active, disabled)
5. Motion (transitions, animations)
6. Responsive (adaptations par breakpoint)

Inverser l'ordre produit du slop : commencer par le motion ou les couleurs avant la structure conduit à habiller un squelette mal pensé. Le polish vient en dernier, jamais en premier.

## Boucle d'itération visuelle

À chaque itération, vérifier dans cet ordre :
1. Le brief est-il respecté (concept, registre, tension) ?
2. Les marqueurs anti-AI-slop sont-ils absents ?
3. Les DON'Ts (`anti-slop-blacklist-core.md`) sont-ils tous évités ?
4. Tous les états interactifs sont-ils couverts ?
5. Le responsive tient-il sur les breakpoints clés ?
6. Le polish (alignement optique, ombres tintées, easing physiques) est-il là ?

Sauter une étape produit une itération qui paraît "presque bien" sans qu'on sache pourquoi. La discipline d'audit interne fait la différence entre un 7/10 et un 9/10.

## CSS moderne — socle toujours présent

Quel que soit le curseur :
- `oklch()` pour la palette — gradients perceptuellement uniformes, pas de zone grise
- `@layer` pour organiser le CSS (reset → tokens → components → utilities)
- `@property` déclaré pour les custom properties animables
- `color-mix()` pour les variations (hover states, backgrounds tintés)
- `text-wrap: balance` sur les headings, `text-wrap: pretty` sur les paragraphes
- `clamp()` pour les tailles fluides (font-size, padding)
- Logical properties (`padding-inline`, `margin-block`) quand applicable

## CSS moderne — techniques avancées (quota)

Au moins **4 techniques** parmi les suivantes, QUEL QUE SOIT le curseur A :
- `@property` animé (couleur ou angle, dans un `@keyframes` ou transition)
- `clip-path`
- `mask-image`
- `@starting-style`
- `backdrop-filter`
- `mix-blend-mode`
- `:has()`
- `animation-timeline: view()`
- `@container`

Chaque technique doit SERVIR le concept, pas être plaquée. Le quota est un plancher de qualité de fabrication, pas un objectif décoratif. Voir le catalogue détaillé dans `html-showroom-spec.md` §6.

---

## Source et traçabilité

**Factorisation** : ce fichier remplace les sections redondantes dans :
- `phases/phase-4-styletile.md` (section "SOCLE DE FINITION ÉLITE" L148-211 et "DIRECTIVE DE QUALITÉ" L389-415)
- `phases/phase-4-artefact.md` (sections L112-125)
- `phases/phase-6a-batch2.md` (sections L39-61)
- `phases/phase-6b-batch3.md` (sections L36-58)

Les 4 phases importeront ce fichier via l'orchestrateur.

## Dernière mise à jour

2026-04-26 — Enrichissement craft + motion + discipline d'exécution (12 règles N1/N2 issues du skill audit-slop). Sections ajoutées : échelle d'ombres, ombres tintées, saturation par luminance, gris sur fond coloré, dark mode, couche graphique d'atmosphère, alignement optique, motion principles, discipline d'exécution.

2026-04-24 — Création par factorisation des 4 phases. Étape 1 du plan d'intégration anti-slop.
