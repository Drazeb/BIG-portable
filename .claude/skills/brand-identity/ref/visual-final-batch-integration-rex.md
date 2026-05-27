# REX — Intégration de la librairie `visual-final/` dans Batch 3 (et brièvement Batch 2, retirée)

Sujet : comment les visuels finaux dérivés (`outputs/{brand}-{session}/visual-final/`) sont consommés par Batch 3 (ch08/ch10). Décision de référence : D54 (12 mai 2026), amendée le 2026-05-14 (retrait de la cover band Batch 2 — voir section « Amendement 2026-05-14 » ci-dessous). Convention de rangement : `ref/` n'a pas le doc — voir `outputs/test-camille-test-20260511-1330/PASSATION-batch3-utilisation-visuels.md` et la mémoire `feedback_visual_final_convention.md`.

## Amendement 2026-05-14 — retrait de la cover band Batch 2

**Constat à l'usage** (sur Camille `test-camille-test-20260513-1453`) : la cover band éditoriale du Batch 2 (image full-bleed `background-image` du hero `visual-final/`, overlay gradient, wordmark Gloock en bas) **rend mal** (jugement Charles : « moche »). Elle entre aussi en concurrence visuelle avec le hero du style-tile/Batch 1 sans apporter de valeur éditoriale propre sur ce qui reste une planche de documentation système.

**Décision** : retirer la cover band du Batch 2. Le Batch 2 ouvre désormais comme le Batch 3 — skip-link → `<main>` → kicker éditorial sobre (« Volume II · Système de Signes ») → chapitre 05 normal. Plus aucun référencement de `visual-final/` côté Batch 2 ; le batch redevient strictement self-contained. La mention du volume vit dans le `<title>`, le kicker discret, et le footer.

**Pourquoi ça reste cohérent avec D54** : la valeur principale de D54 était la consommation de la librairie dans **Batch 3 ch.08 (moodboard) et ch.10 (schémas)** — c'est là que les images dérivées remplacent un faux moodboard CSS par les vraies images. La cover band Batch 2 n'était qu'un bonus d'affichage non analytique, écartée à l'usage. La librairie reste consommée par Batch 3 comme prévu.

**Fichiers modifiés** : `phases/phase-6a-batch2.md` (section « BANDE DE COUVERTURE » → « ENTRÉE ÉDITORIALE SOBRE »), `SKILL.md` (étape Inventaire — retrait du routage cover band + variable `{cover_visual_rel}` non injectée + références mises à jour), `ref/html-showroom-spec.md` §8 (Batch 2 retiré de la consommation `visual-final/`), `ref/visual-final-batch-integration-rex.md` (cet amendement), `DECISIONS.md` D54 (amendement), `CHANGELOG.md`, MEMORY.

## Historique D54 (12 mai 2026) — état d'origine, conservé pour traçabilité

## Problème

La capacité de générer une librairie de visuels dérivés (hero, animation, atmosphère ×4 intensités, closeup, macro, pov, schéma) existe (skill `/visual-prompt`, framework des 7 types dans `nb-prompting-guide.md` §11) mais ces images dormaient dans `visual-final/` sans être exposées dans les livrables : seule l'image-pivot du style-tile (base64) était visible. Le chapitre 08 du Batch 3 ("Direction Photo") fabriquait un faux moodboard en CSS au lieu de montrer les vraies images.

## Ce qu'on a essayé / écarté

- **Tout mettre dans le Batch 2** (demande initiale de Charles) → écarté : Batch 2 n'a pas de chapitre adapté (05 logo / 06 icônes / 04 composants / 07 dataviz) ; une galerie y serait une section orpheline et alourdirait un subagent déjà à ~12 sous-sections + ~10 gates. Compromis retenu : une **bande de couverture** (affichage, pas analyse) en tête de Batch 2 satisfait le besoin de "visibilité rapide client" ; le gros de la librairie va dans Batch 3 ch08 (qui EST déjà la "Direction Photo").
- **Embedding base64 self-contained** → écarté : 4-6 images ~1200px alourdiraient massivement le HTML, et les animations `.html` ne sont de toute façon pas inlinables. Retenu : **chemin relatif** (`<img src="visual-final/…">`, `<iframe src="visual-final/…animation.html">`). Conséquence assumée : Batch 2 (si cover) et Batch 3 (si visuels) ne sont plus 100 % self-contained — le dossier `visual-final/` voyage avec eux (même logique que les vidéos déjà dans la spec §8).
- **Auto-matching de la palette** quand `visual-final/` contient plusieurs palettes pour le concept → écarté : exigerait une analyse visuelle, fragile. Retenu : l'orchestrateur **demande à l'utilisateur** laquelle correspond au style-tile retenu (cas rare).

## Solution retenue (mécanique)

1. **Orchestrateur, Phase 6A, nouvelle étape "Inventaire des visuels finaux dérivés"** (avant le lancement des subagents Batch 2/3) :
   - glob `{session_dir}/visual-final/`, parse le naming `{brand}-c{N}-{paletteID}-{type}[-{variante}].{ext}` (regex dans SKILL.md), exclut les fichiers `*-source.*` / `*-v{N}-source.*` (sources hires), restreint à `c{chosen_concept_number}` ;
   - 0 visuel → `{cover_visual_rel}` = `{visual_library_ch08}` = `{visual_library_ch10}` = `''`, fin de l'étape (pipeline strictement inchangé) ;
   - ≥ 2 palettes → demande utilisateur, filtre sur la palette confirmée ;
   - routage : cover band ← 1 visuel (préférence `hero` → `atmosphere`/`dramatique` → `atmosphere`/`doux` → premier `atmosphere` → premier `closeup`/`pov`/`macro` ; jamais `.html` ni `.svg`) ; ch08 ← `hero`/`animation`/`atmosphere`/`closeup`/`macro`/`pov` ; ch10 ← `schema` ;
   - construit `{cover_visual_rel}` (chaîne de chemin relatif), `{visual_library_ch08}` et `{visual_library_ch10}` (blocs markdown : table des fichiers + règles d'affichage).
2. **`phase-6a-batch2.md`** : section "BANDE DE COUVERTURE (conditionnelle)" — si `{cover_visual_rel}` non vide, ouvre `<body>` sur une `<section class="batch2-cover">` (image en `background-image`, overlay gradient `--color-primary-dark`, nom de marque en `--font-display`, sous-titre concept). Pas une section analytique. Vide → rien.
3. **`phase-6b-batch3.md`** : `{visual_library_ch08}` injecté après `{batch3_shared_context}` dans le prompt ch08 + directives dans le garde-fou et dans 08.1/08.2/08.3 (les images réelles remplacent les cartes CSS descriptives ; les 4 niveaux d'intensité `atmosphere` SONT la démonstration du color grading en 08.2 ; les animations en `<iframe loading="lazy">` non modifiées). `{visual_library_ch10}` idem pour les `schema` (en contexte d'usage, jamais isolés). Note dans CONTRAINTES TECHNIQUES partagées sur le chemin relatif / non self-contained.
4. **`ref/html-showroom-spec.md` §8** : la ligne "pas propagés aux Batches 2 et 3" est nuancée (vraie pour l'image-pivot base64, fausse pour la librairie dérivée) + nouvelle sous-section "Librairie de visuels finaux dérivés".
5. **`test-big/SKILL.md`** : `visual-final/` ajouté en prérequis optionnel de 6A/6B ; note "copier le dossier `visual-final/` complet depuis le source quand `{start_phase}` ≥ 3B-7d" ; exemples de démarrage 6A/6B ; liste utilisateur.

## Pourquoi ça marche

- **Fallback total** : tout le mécanisme est conditionné par la présence de `visual-final/`. Absent → variables vides → les prompts Batch 2/3 sont mot pour mot ceux d'avant. Zéro régression possible sur les sessions sans librairie.
- **Le subagent invente moins, pas plus** : en ch08, remplacer un faux moodboard CSS par de vraies images réduit la charge créative ; ça sert aussi directement la règle Show > Tell (montrer au lieu de décrire).
- **Chemins relatifs résolus correctement** : `open outputs/{brand}-{session}/{batch}.html` → `visual-final/…` se résout en `outputs/{brand}-{session}/visual-final/…` ✓. Les animations `.html` référencent leur propre bg image en chemin relatif depuis `visual-final/` ✓.
- **Routage `schema` → ch10** (pas Batch 2 ch07 dataviz) : un schéma "façon papier scientifique" est une illustration dans un registre technique, plus proche du langage illustratif de la marque que d'un graphique de données. Choix tranché avec Charles.

## Pièges connus / à surveiller

- Si `/visual-prompt` dépose des fichiers au naming hétérogène (sessions BIG pré-2026-05-12), ils ne matchent pas le regex → ignorés. C'est voulu (cf. passation §7) : se fier uniquement au nouveau naming.
- Le dossier `visual-final/` doit accompagner les HTML livrés (Batch 2 avec cover, Batch 3 avec visuels). À vérifier au packaging (Phase 8) — non couvert par ce chantier, à traiter si besoin.
- Si le subagent ch08 reçoit beaucoup de visuels (ex: hero + animation + 4 atmosphères + macro + pov + closeup), le rendu peut devenir lourd visuellement. Charles prune dans la boucle d'itération Batch 3 ("retire celle-là, trop").
