# Catalogue d'Animations — Style-Tile (Étape 5D)

> **Stack visée** : GSAP 3.13+ (`ScrollTrigger`, `SplitText`) via CDN + CSS natif. Pas de smooth-scroll par défaut (scroll natif), pas de WebGL/3D/vidéo.
> **Lu par** : l'orchestrateur (Étape 5D — pour présenter le menu et choisir le preset recommandé) ET le sous-agent animateur (`phases/phase-5d-animation.md`).
> **Pour l'implémentation concrète** (snippets GSAP/CSS, garde-fous, non-régression) : voir `ref/animation-implementation-guide.md`.
> **Dernière vérification** : 2026-05-12.

Le catalogue est organisé en **6 axes**. Un « preset » = une combinaison d'options, une par axe (axe E et F peuvent rester sur « aucune »). L'utilisateur n'est pas censé connaître ces noms — la colonne *Description* est rédigée pour ça.

---

## Axe A — Comportement du scroll

C'est un réglage global, pas un effet visuel.

| Option | Nom standard | Description | Note |
|---|---|---|---|
| **A1 · Natif** | *native scroll* | Le scroll par défaut du navigateur/OS — instantané, précis, « sec ». Aucune librairie. | **Défaut.** Pas de sensation de lest. |
| **A2 · Lissé** | *smooth scroll* (a.k.a. *scroll smoothing*, *inertia/lerp scroll*, péj. *scroll hijacking*) | Une lib (Lenis, GSAP ScrollSmoother) interpole le scroll → glissé, « premium ». | Donne une sensation « lourde/pâteuse » que beaucoup détestent. **Opt-in uniquement**, jamais imposé, jamais dans un preset par défaut. |

---

## Axe B — Entrée du hero (au chargement de la page)

| Option | Nom standard | Description | Note |
|---|---|---|---|
| **B0 · Aucune** | — | Le hero s'affiche directement. | |
| **B1 · Fondu montant** | *fade-up* (souvent *staggered fade-up*) | Overline, titre, sous-titre, CTA apparaissent en fondu + légère montée, en cascade. | Le plus sobre. |
| **B2 · Typo par lignes** | *split-text line reveal* / *line mask reveal* | Le titre est découpé en lignes ; chaque ligne monte (souvent depuis un cache, effet « store qui se lève »), avec un léger flou qui se résorbe. | Nécessite `SplitText`. Attention aux jambages (« q », « g ») si on clippe — préférer montée + fondu sans clip dur. |
| **B3 · Typo par mots** | *split-text word reveal* | Idem mais mot par mot. | Plus « kinetic », vite chargé sur un titre long. |
| **B4 · Typo par lettres** | *split-text char reveal* | Idem mais lettre par lettre. | À réserver à de très courts titres / wordmarks. |
| **B5 · Volet** | *clip-path reveal* / *mask wipe* | Un bloc (image, panneau, bandeau) se dévoile par un volet qui s'ouvre. | Sur un bloc, pas forcément le texte. |
| **B6 · Mise au net** | *blur-in* / *focus pull* | L'élément arrive flou et se met au net. | Joli mais coûteux à rendre — à doser, brefs uniquement. |
| **B7 · Compteurs** | *number counter* / *odometer* | Les chiffres-clés (KPI, « €340 M ») défilent de 0 à leur valeur. | Au chargement OU quand la zone devient visible (voir D8). |

---

## Axe C — Animations du hero liées au scroll

⚠ **Compatibilité overlay calé sur l'image** : si le hero contient un overlay positionné (SVG/canvas dont la géométrie dépend du cadrage exact de l'image — ex : le faisceau du phare de Camille), les options qui zooment ou déplacent l'image/l'overlay sont **interdites** (« mode sûr hero »).

| Option | Nom standard | Description | Overlay calé ? | Note |
|---|---|---|---|---|
| **C0 · Aucune** | — | Le hero défile normalement, rien de spécial. | ✅ OK | |
| **C1 · Parallaxe 1 couche** | *parallax scrolling* (version minimale) | Quand on scrolle, seul le premier plan (le bloc de texte du hero) se « décolle » : il monte un peu plus vite que le fond resté fixe. | ✅ OK | **Recette de référence (prototype Camille v3).** Le fond et l'overlay ne bougent jamais. |
| **C2 · Parallaxe multi-couches** | *layered parallax* | Fond / médian / premier plan défilent à 3 vitesses différentes → profondeur. | ⊘ Interdit (déplace le fond) | |
| **C3 · Fondu de sortie** | *scroll-triggered fade-out* (combiné avec C1 = *hero exit* / *scroll-away hero*) | Le contenu du hero s'efface progressivement au fil du scroll, révélant la scène derrière. | ✅ OK | Souvent combiné avec C1. |
| **C4 · Épinglage + scrub** | *pin & scrub* / *sticky hero* | La section hero « colle » à l'écran pendant un temps de scroll ; pendant ce temps une mini-séquence se joue calée sur la position de scroll. | ⊘ Interdit (zoom/déplace l'image) | Très « Awwwards » mais vite vu sur un style-tile parcouru rapidement — pin court (≤ 60-80vh) si utilisé. |
| **C5 · Zoom lent** | *Ken Burns* (au scroll) | L'image de fond zoome/dézoome lentement au fil du scroll. | ⊘ Interdit (zoome l'image) | |
| **C6 · Header condensé** | *sticky / condensing header* | Le header devient une barre fine (fond, ombre, blur) une fois qu'on a scrollé un peu. | ✅ OK | N'affecte pas l'image. Demande de passer le header en `position: fixed`. |

---

## Axe D — Reveals du reste de la page (sections sous le hero)

| Option | Nom standard | Description | Note |
|---|---|---|---|
| **D0 · Aucun** | — | Les sections s'affichent telles quelles. | |
| **D1 · Apparition par le bas** | *fade-up on scroll* / *reveal on scroll* / *scroll-into-view* | Chaque bloc apparaît en fondu + montée quand il entre dans le viewport. | **Recette de référence.** Le standard. |
| **D2 · Cascade** | *staggered reveal* | Idem mais les éléments d'un même groupe arrivent décalés l'un après l'autre. | |
| **D3 · Volet** | *clip-path wipe* | Le bloc se dévoile par un volet qui s'ouvre. | |
| **D4 · Apparition zoomée** | *scale-in* / *pop-in* | Le bloc arrive légèrement réduit puis prend sa taille. | À doser, vite « bouncy ». |
| **D5 · Entrée latérale** | *slide-in* | Le bloc entre depuis la gauche ou la droite. | À ne pas multiplier (effet « carrousel »). |
| **D6 · Tracé de trait** | *line drawing* / *SVG path animation* (`stroke-dashoffset`) | Une ligne / un filet / une signature se « dessine ». | Idéal pour hairlines, rails de progression, soulignés, signature. |
| **D7 · Dévoilé d'image** | *image clip reveal* | Une image se dévoile par un masque qui s'ouvre. | |
| **D8 · Compteurs en vue** | *number counter on view* | Les chiffres défilent quand la section devient visible. | |
| **D9 · Parallaxe intra-page** | *element parallax* | Une image dans une section se déplace un peu plus vite/lentement que le texte autour. | Léger, à ne pas multiplier ; jamais sur un bloc avec overlay calé. |

---

## Axe E — Micro-interactions (au survol / au pointeur)

| Option | Nom standard | Description | Note |
|---|---|---|---|
| **E0 · Aucune** | — | Au-delà des états hover déjà présents dans le style-tile. | |
| **E1 · États hover riches** | *enhanced hover states* | Boutons/cartes qui réagissent (ombre, déplacement, couleur, flèche qui glisse). | Souvent déjà dans le style-tile — n'ajouter que si pauvre. |
| **E2 · Bouton magnétique** | *magnetic button* | Le bouton est légèrement « attiré » vers le curseur quand on l'approche. | Signature « creative dev ». 1-2 boutons max. |
| **E3 · Curseur custom** | *cursor follower* / *custom cursor* | Un élément (point, halo, label) suit le curseur. | Vite gimmick — **jamais dans un preset par défaut**, opt-in. |
| **E4 · Inclinaison 3D** | *3D tilt* | Une carte s'incline selon la position du curseur. | À réserver à un visuel/une carte « héros ». |
| **E5 · Bandeau défilant** | *marquee* / *ticker* | Un bandeau de texte défile en boucle horizontale. | CSS pur possible. Au chargement, pas au survol — mais même famille « décor cinétique ». |
| **E6 · Image au survol** | *hover image reveal* | Au survol d'un lien, une image apparaît. | Typique des listes de projets/cas. |

---

## Axe F — Fond / ambiance (animation continue, indépendante du scroll)

| Option | Nom standard | Description | Note |
|---|---|---|---|
| **F0 · Statique** | — | Rien ne bouge en fond. | |
| **F1 · Dégradé animé** | *animated gradient* | Un dégradé (conique/radial) tourne ou « respire » très lentement. | Sobre **si lent** (cycle ≥ 20-30s). CSS + `@property`. |
| **F2 · Grain animé** | *animated grain/noise* | Un bruit/grain scintille subtilement. | Très discret. |
| **F3 · Aurora / mesh** | *mesh gradient* / *aurora* | Des taches de couleur floues dérivent. | ⚠ **Marqueur d'AI-slop** dès que c'est visible. À éviter ; si vraiment utilisé, ultra-subtil et jamais sur un fond clair. |
| **F4 · Particules** | *particle field* | Petits points qui flottent. | ⚠ Vite daté/gimmick. À éviter. |
| **F5 · SVG/canvas sur-mesure** | *bespoke SVG/canvas animation* | Animation faite main propre au concept (ex : le faisceau du phare de Camille, une vague, un signal qui pulse). | Le plus « identitaire » — mais déjà dans le style-tile s'il existe. **Le sous-agent ne le crée pas** (ce n'est pas générable en série) ; il le laisse intact. |
| **F6 · Vidéo / shader** | *video background* / *shader background* | Fond vidéo ou shader 3D. | **Hors v1** (lourd, WebGL). |

---

## Presets recommandés par profil

L'orchestrateur (Étape 5D-1) choisit le preset selon : (1) le hero a-t-il un overlay calé sur l'image ? (2) le registre / la famille de style du style-tile retenu ? Premier match gagne. Tous les presets utilisent **A1 (scroll natif)**.

| # | Profil du style-tile | Preset | Combinaison |
|---|---|---|---|
| **P1 · Sobre-Sûr** | Le hero a un overlay calé sur l'image (SVG/canvas, géométrie pixel) — *mode sûr obligatoire* | « Le texte se décolle » | A1 · B0 · **C1+C3** · **D1** · E0 · F0 *(F5 conservé tel quel s'il existe)* |
| **P2 · Éditorial-Cinétique** | Registre éditorial / magazine / brutaliste-typo, pas d'overlay calé | « Typo qui arrive, sections qui montent » | A1 · **B2** · C1+C3 · **D2** + **D6** *(hairlines)* · E0 · F0 |
| **P3 · Premium-Profond** | Registre premium / luxe / cinématique, image hero pleine, pas d'overlay calé | « Hero qui se déploie » | A1 · **B1** · **C4** *(pin court ≤ 70vh)* + **C5** *(Ken Burns léger)* · **D1** · E0 · F1 *(dégradé très lent, si la palette s'y prête)* |
| **P4 · Tech-Net** | Registre tech / SaaS / dashboard, beaucoup de données et de chiffres | « Données qui s'installent » | A1 · B1 · C1+C3 · **D2** + **D8** *(compteurs)* · **E1** · F0 |
| **P5 · Minimal** | Style très épuré / suisse / institutionnel, peu de matière | « Apparitions discrètes » | A1 · B1 · C3 · **D1** · E0 · F0 |
| **P0 · Aucun** | L'utilisateur veut juste « un peu de vie » sans rien d'audacieux | « Reveals au scroll seuls » | A1 · B0 · C0 · **D1** · E0 · F0 |

> **Le preset n'est qu'une proposition.** L'utilisateur peut retirer/ajouter n'importe quelle option de n'importe quel axe (sauf celles barrées ⊘ par le mode sûr). L'orchestrateur transmet au sous-agent la liste finale d'options + le flag `hero_safe_mode`.
