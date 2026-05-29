# Architecture — Brand Identity Generator (BIG)

## Vue d'ensemble

Système de génération d'identités de marque de classe mondiale. Deux modes : **création** (à partir d'un brief marketing → 7 phases) ou **aspiration** (capture d'une marque existante depuis son site web → 5 phases). Les deux modes convergent pour produire des style-tiles HTML immersifs, un système de signes complet, et une documentation technique exportable.

**Input** : Un brief marketing OU des URLs de site web
**Output** : Style-tiles HTML + Batches visuels (icono, dataviz, photo, composition, illustration) + Design specs markdown + Logo SVG (optionnel)

**Fichier source** : `.claude/skills/brand-identity/SKILL.md` (~2200 lignes, l'orchestrateur). Les prompts subagents sont externalisés dans `phases/` (12 fichiers, ~1450 lignes) et lus à la demande par l'orchestrateur.

---

## Pipeline — Mode Création (Options A/B/C)

```
Phase 1 · Analyse du brief      → Score de confiance + Ventre Mou + signaux de Tension
     ↓
Phase 2 · Scoping                → Tension de Marque + Curseurs A×B + Territoires Créatifs (mots-clés → clusters → mix pondéré)
     ↓
Phase 3A · Concepts narratifs    → Mode Sélectif : registre → pool 100 mots → 10 évaluateurs filtrent → 0-3 concepts retenus (batches accumulables)
     ↓
Phase 3B · Design dérivé         → 3 pitchs complets (récit + direction visuelle)
     ↓
Phase 3C · Visuels de référence  → Prompts MidJourney (optionnel, toujours proposé)
     ↓
Phase 4 · Style-Tiles HTML       → 3 fichiers HTML immersifs (triptyque Voice/Artefact/Atmosphere)
     ↓
Phase 5 · Choix + itération      → 1 concept retenu, slug généré
     ↓
[5D · Animation] · Optionnel     → Preset recommandé + 2-3 variantes de dosage → `{tile}-animated.html` (coexiste avec le statique)
     ↓
[Logo]  · Optionnel              → Concept + MidJourney + vectorisation SVG + 6 variantes
     ↓
Phase 6A · Batch 2               → Logotype + Iconographie + Data Viz (HTML)
     ↓
Phase 6B · Batch 3               → Direction Photo + Composition + Illustration (HTML)
     ↓
Phase 7 · Documentation Markdown → Design specs validés (~45 sections couvrant tout le pack)
     ↓
[Phase 8 · Brand Book]  · Optionnel  → Sub-agent invoque /brand-book (cover painterly + Identity Card bento + 8 sections documentaires + closing) — sortie dans `{session_dir}/brand-book/`
     ↓
[Phase 8b · Design System] · Optionnel → Sub-agent invoque /design-system (HTML technique sobre type Carbon/Atlassian, 11 sections, sidebar nav, tokens prêts à copier) + audit Python automatique — sortie dans `{session_dir}/design-system/`
     ↓
Étape Finale · Packaging         → Pack final centralisé + déploiement Vercel (inclut brand-book/ si Phase 8 et design-system/ si Phase 8b exécutés)
```

## Pipeline — Mode Aspiration (Option D)

```
D1 · Collecte          → Screenshots + HTML + CSS extraits des URLs
  ↓
D2 · Extraction         → Brand DNA (tokens design avec niveaux de confiance)
  ↓
D3 · Validation         → User corrige/ajuste les tokens extraits
  ↓
D4 · Style-Tile         → 1 seul HTML fidèle à 100% des tokens
  ↓
D5 · Validation         → Puis convergence vers Phase 6A du mode création
```

---

## Mécanisme global : Orchestrateur + Subagents

Avant de détailler chaque brique, voici comment le système fonctionne mécaniquement :

- **L'orchestrateur** (le SKILL.md) est le chef de projet. Il ne génère rien lui-même (sauf les briefs visuels et le post-traitement). Il lance des subagents, collecte leurs résultats, les présente à l'utilisateur, et gère les boucles d'itération.
- **Les subagents** sont des agents spécialisés lancés via `Task tool` (subagent_type: "general-purpose"). Chacun reçoit un long prompt avec les fichiers de référence à lire, les inputs, la mission, et les quality gates à respecter. Ils écrivent leur output dans un fichier dans `outputs/{session_dir}/`.
- **La boucle d'itération** est la même partout : subagent produit → orchestrateur présente → user valide ou demande ajustement → si ajustement, orchestrateur resume le subagent (via `resume: agentId`) avec le feedback → le subagent reprend avec tout son contexte + le feedback → et ainsi de suite jusqu'à validation explicite.
- **Jamais de passage à la phase N+1 sans validation explicite de la phase N.**

### Session isolation

Dès que le nom de marque est connu (après le choix A/B/C/D), l'orchestrateur :
1. Demande un label de session (ex: "v1", "rupture", "a3b3-test") ou en génère un auto (format `MMDD-HHmm`)
2. Crée `outputs/{brand}-{session}/` et un fichier `.session-id` contenant `{brand}|{session}|{timestamp}`
3. **Avant chaque lancement de subagent**, vérifie que `.session-id` existe et correspond — sinon STOP

Tous les fichiers de la session vivent dans ce dossier. Ça permet de lancer plusieurs sessions en parallèle pour la même marque sans collision.

---

## Briques détaillées — Mode Création

### Phase 1 · Analyse du brief

- **Ce qu'elle fait** : Valide la complétude du brief sur 14 points obligatoires, attribue un score de confiance à chacun, identifie les codes visuels du secteur (Ventre Mou) et les tensions de marque
- **Input** : Brief (4 modes de collecte : fichier existant, template, conversationnel, aspiration)
- **Output** : `{brand}-brief-analysis.md` — Score de confiance global, Ventre Mou sectoriel, signaux de Tension
- **Règles clés** :
  - Bloque si confiance globale < 90% — force la clarification plutôt que la spéculation
  - Le Ventre Mou identifie ce que TOUS les concurrents font visuellement — pour l'éviter consciemment
- **Enchaînement** : Nourrit la Phase 2 avec la matière pour formuler la Tension et calibrer les curseurs

**Sous le capot** :
1. L'orchestrateur collecte le brief selon l'option choisie (A: fichier, B: template envoyé puis retourné, C: conversationnel question par question)
2. Lance **1 subagent** avec le brief en input. Le subagent lit 4 fichiers de référence : `persona-and-rules.md`, `bible-design-strategie.md`, `brief-alpha-template.md`, `master-style-guide.md`
3. Le subagent analyse chaque point du brief avec un score de confiance (0-100%), pondéré par importance (CRITIQUE ×3, ÉLEVÉ ×2, etc.)
4. Si score global < 90% → le subagent retourne STATUS: BLOCKED avec les questions précises à poser
5. L'orchestrateur présente les questions, collecte les réponses, relance le subagent avec brief + réponses
6. Si score ≥ 90% → STATUS: OK. L'orchestrateur ouvre le rapport dans TextEdit, affiche un résumé court dans le chat (~score global + Tension + Ventre Mou), et demande validation
7. Le rapport complet n'est PAS copié dans le chat (économie de tokens) — il est dans le fichier ouvert

---

### Phase 2 · Scoping (Tension + Curseurs)

- **Ce qu'elle fait** : Synthétise la Tension de Marque, collecte les choix créatifs de l'utilisateur
- **Input** : `{brand}-brief-analysis.md`
- **Output** : `{brand}-scoping.md` + `{brand}-territoires.md` (mots-clés + clusters + mix pondéré) + variables stockées (curseurs A×B, mix de territoires)
- **Règles clés** :
  - **Curseur A** (Audace Créative) : intensité du traitement visuel (1=Prudent / 2=Décalé / 3=Rupture). Indexe la typo, les layouts, la complexité CSS
  - **Curseur B** (Différenciation) : distance par rapport aux normes du secteur (1=Mimétisme / 2=Distinction / 3=Contre-pied ZAG). Indexe la palette, le ton, le langage visuel
  - Les 2 curseurs sont découplés — A=3 avec B=1 est valide
  - L'utilisateur choisit UNE combinaison A×B qui s'applique aux 3 concepts
  - 15-20 mots-clés extraits du brief (4 axes) → clustering en 4-5 territoires créatifs → mix pondéré par l'utilisateur (Principal/Secondaire/Accent)

**Sous le capot** — cette phase a 4 étapes distinctes :

**Étape 2A** (subagent) : Lance **1 subagent** qui lit l'analyse Phase 1 + les refs. Le subagent produit UNIQUEMENT la synthèse de la Tension et du Ventre Mou + un avis du DA. Il ne propose PAS de curseurs ni de noms de concepts — c'est explicitement interdit dans son prompt (pour ne pas biaiser le choix de l'utilisateur).

**Étape 2B** (orchestrateur) : Présente la Tension à l'utilisateur, demande validation. Puis affiche le système de curseurs A×B avec la description de chaque niveau (1/2/3) et demande le choix. C'est l'utilisateur qui décide, pas le système.

**Étape 2C** (subagent) : Territoires Créatifs. Un subagent extrait 15-20 mots-clés du brief selon 4 axes (métier/produit, valeurs/culture, marché/audience, aspirations/vision), puis les clustérise en 4-5 territoires créatifs (chacun avec un nom évocateur, 3-5 mots-clés, et une ligne de tension). L'orchestrateur présente les territoires à l'utilisateur.

**Étape 2D** (orchestrateur, inline) : Mix pondéré. L'utilisateur attribue un rôle à chaque territoire : Principal (le cœur du concept), Secondaire (colore et enrichit), Accent (touche distinctive). L'orchestrateur stocke le mix dans `{brand}-territoires.md`. Ce mix est la matière première pour les concepts narratifs.

**Étape 2D-bis** (orchestrateur, subagent) : Décontamination du contexte. Avant la génération des concepts, un subagent (`phases/phase-3a-decontamination.md`) produit `{brand}-context-clean.md` — version anonymisée et décontaminée du mix de territoires (sans jargon sectoriel, sans noms propres, sans direction). Produit une seule fois par projet (skip si déjà présent). Ce fichier est relu par le Mode Sélectif ET par de nombreuses phases de la 3B (palette, penseurs typo, styliste, routeur chromatique).

---

### Phase 3A · Concepts narratifs (Pass A)

- **Ce qu'elle fait** : Génère des récits conceptuels distincts à partir du mix de territoires créatifs. Zéro design — que du narratif. **Mode Sélectif unique (depuis le 28 mai 2026 — suppression des modes Génératif)** : l'utilisateur choisit un registre culturel ; les concepts sont CHOISIS dans un pool de ~100 mots tirés de ce registre puis filtrés contre le brief, ce qui produit des noms sobres ("Phare", "Magnitude") au lieu de noms enrichis artificiels ("Le Phare de Ralliement").
- **Input** : `{brand}-context-clean.md` (mix décontaminé, produit en Étape 2D-bis) + `{brand}-scoping.md` (Ventre Mou Narratif) + un registre choisi + curseurs A×B
- **Output** : `{brand}-concepts-narratifs-v{N}.md` (1 à 3 concepts par batch retenu) → la sélection finale assemble `{brand}-concepts-narratifs.md`, seul fichier lu par toute la Phase 3B
- **Règles clés** :
  - **Choix du registre à l'Étape 2E** : l'utilisateur choisit un registre dans `ref/registres-creatifs.md` (28 registres). Plus aucun choix de mode.
  - **Choix dans un pool** : le LLM choisit dans 100 mots du registre, pas d'invention de nom → noms mono-mots ou composés courts limpides
  - **Filtrage ancré sur le brief** : 10 évaluateurs parallèles classent les mots contre le mix de territoires + le ventre mou → seuls les mieux ancrés remontent comme candidats
  - **Sortie flexible 0 à 3** : l'utilisateur retient 0 à 3 mots par registre ; 0 retenu = exploration jetable (aucun fichier produit, aucun numéro de version consommé)
  - **Zéro spec visuelle** (pas de couleur, police, HEX) — le récit est jugé sur sa force conceptuelle uniquement
  - **Accumulation cross-batch** : un user peut accumuler v1 (registre A) + v2 (registre B) + v3 (registre A relancé) → sélection finale libre de 1 à 3 concepts parmi tout l'accumulé

**Sous le capot** (10 sous-étapes orchestrées) :

1. **S1 — Pool collectif** : 5 sub-agents Task vierges parallèles lancent `phases/phase-3a-selectif-pool.md` → 5 fichiers `pool-run{1..5}.md` dans `.tmp-selectif-v{N}/`. Aucun brief, aucun territoire transmis (anonymisation totale).
2. **S2 — Dédup + sélection 100** : `scripts/phase3a-selectif-build-pool.py` lit les 5 runs, dédup morphologique (lowercase + NFD), sélection stratifiée (tout le 5/5 + tout le 4/5 + 48 mots samplés uniforme dans le reste, seed=42).
3. **S3 — Split 10×10** : `scripts/phase3a-selectif-split-batches.py` randomise (seed=2026) et écrit `batches.json` + `batches-preview.md`.
4. **S4 — Évaluation parallèle** : 10 sub-agents Task parallèles lancent `phases/phase-3a-selectif-evaluator.md` avec `{mix_territoires}` + `{ventre_mou_narratif}` + leur batch de 10. Chacun produit : scan obligatoire des 10 (verdict EXPLOITABLE/INEXPLOITABLE), choix unique, dynamique narrative 3-5 phrases, justification chirurgicale par comparaison à 2-3 autres mots, auto-test brief-first.
5. **S5 — Extraction** : l'orchestrateur lit les 10 eval, extrait les 10 mots retenus.
6. **S6 — Définitions neutres** : 1 sub-agent Task lance `phases/phase-3a-selectif-definitions.md` avec UNIQUEMENT la liste des 10 mots + le registre. Aucun brief, aucun territoire, aucune justification (anti-biais).
7. **S7 — Récap MarkView** : assemblage de `{brand}-concepts-selectif-recap-v{N}.md` au format tableau (mot / définition neutre / dynamique / brief-first), ouvert en MarkView.
8. **S8 — Sélection user** : 0 à 3 mots retenus (0 = ne rien garder sur ce registre, on relance un autre/même registre au checkpoint).
9. **S9 — Assemblage** : pour chaque mot retenu, 1 sub-agent `phases/phase-3a-selectif-batch-assemble.md` produit la fiche au format Phase 3B. Output : `{brand}-concepts-narratifs-v{N}.md`. Exécutée uniquement si ≥1 mot retenu ; sinon aucun fichier produit et le numéro de version n'est pas consommé (pas de trou v1, v2, v3…).
10. **S10 — Retour Checkpoint** : checkpoint Pass A simplifié (3 options : nouveau batch autre registre / nouveau batch même registre / avancer au design).

**Pourquoi le Mode Sélectif unique (28 mai 2026) ?** Les modes Génératif (3 subagents séquentiels qui inventaient les concepts) produisaient des noms artificiellement complexifiés ("Le Phare de Ralliement" au lieu de "Phare") et des résultats nettement inférieurs au Sélectif. Le Sélectif **rend structurellement impossible** la complexification : le LLM ne génère plus le nom, il choisit dans un pool de 100 mots tirés d'un registre puis filtrés contre le brief. Validation empirique : sur le batch contenant "phare", le sub-agent évaluateur l'écarte EXPLICITEMENT comme cliché au profit de "sémaphore". Les deux modes Génératif ont donc été supprimés (le choix de mode était une complexité inutile).

**Pourquoi le two-pass (A puis B) ?** Si récit et design sont générés ensemble, le subagent justifie ses choix visuels par le récit au lieu de l'inverse. La séparation force le design à dériver d'un récit validé.

**Pourquoi le séquentiel au lieu du parallèle ?** Le parallèle (3 agents indépendants) produisait des concepts convergents — sans visibilité sur les autres, chaque agent trouvait la même "meilleure" réponse. Le séquentiel force la divergence : chaque subagent VOIT ce qui a déjà été fait et a l'obligation de prendre un autre chemin.

**Pourquoi le two-pass (A puis B) ?** Si le récit et le design sont générés ensemble, le subagent a tendance à justifier ses choix visuels par le récit au lieu de l'inverse. En séparant, le récit est validé AVANT le design, et le design doit explicitement dériver de ce récit validé. Chaque choix visuel doit répondre à "pourquoi CE choix pour CE concept ?"

---

### Phase 3B · Design dérivé (Pass B)

- **Ce qu'elle fait** : Dérive une direction visuelle complète de chaque récit validé
- **Input** : `{brand}-concepts-narratifs.md` (validé) + Phase 1 + Phase 2 + exemples
- **Output** : `{brand}-pitch.md` — 3 pitchs complets (narratif repris de Pass A + direction visuelle dérivée)
- **Règles clés** :
  - **Diversité obligatoire** : 3 schémas chromatiques différents, 3 layouts différents, 3 types d'artefact différents, 3 vocabulaires d'interaction différents, jamais la même police dans 2 concepts
  - **4 éléments stratégiques** ajoutés : type d'artefact, philosophie d'interaction, techniques CSS prioritaires, registre atmosphérique
  - **Calibration par Curseur A** : exigences minimales par niveau (A≥2 → au moins 1 asymétrie, 1 surface expressive, 1 technique non-standard)
  - **Anti-contamination** : interdit de copier quoi que ce soit des exemples fournis

**Sous le capot** :
1. Lance **1 subagent** qui lit : `persona-and-rules.md`, `bible-design-strategie.md`, `master-style-guide.md`, `html-showroom-spec.md` (pour les pools de polices indexés par curseur A), et **3 exemples de pitch** couvrant les 3 niveaux de curseur (prudent, décalé, rupture) — pour montrer la diversité de qualité attendue
2. Le subagent lit aussi les concepts narratifs validés (Pass A) et les outputs Phase 1 et 2
3. **Anti-contamination** : le prompt liste explicitement TOUTES les polices, palettes et triptyques des 3 exemples et interdit de les réutiliser
4. Pour chaque concept, le subagent :
   - Reprend le narratif de Pass A (ancrage brief, intention, bénéfices)
   - DÉRIVE la direction visuelle, dans l'ordre : palette HEX (avec harmonie chromatique déclarée — Vague 1, divergence séquentielle A/B/C avec choix utilisateur), puis typographie (Vague 2/2bis/2ter, choisie dans le pool du curseur A via Google Fonts), puis surface (radius/shadows/transitions), atmosphère
   - Ajoute les 4 éléments stratégiques : quel type de composant UI pour l'artefact (lié au secteur du brief), quel vocabulaire d'interaction (comment les éléments réagissent au hover/clic), quelles techniques CSS prioritaires (2-3, justifiées par le concept), quel registre atmosphérique (sombre/clair/coloré/texturé)
   - Produit une Carte d'Inspiration (classification du territoire visuel, pas invention)
   - Inclut un tableau comparatif des 3 concepts avec pastilles couleur inline
5. **Checklist calibrage** : avant de finaliser, le subagent vérifie que le TRAITEMENT de chaque concept correspond au curseur A (checklist explicite dans le prompt). Si A=2, chaque concept DOIT avoir ≥1 asymétrie, ≥1 surface expressive, ≥1 interaction qui exprime le concept, ≥1 technique CSS non-standard. Sinon → réajustement.
6. **Vérification visuelle typo + palette (3B-bis)** : l'orchestrateur extrait fonts + palettes du pitch, génère un HTML specimen (via `lib/font-palette-specimen.mjs`) chargé avec les Google Fonts réelles + swatches de palette + texte sur fonds colorés, capture un screenshot via Puppeteer, et resume le subagent 3B avec le screenshot. Le subagent voit le RENDU RÉEL de ses choix pour la première fois et peut corriger (max 2 itérations). Raison : sans cette étape, les incohérences typo ne sont découvertes qu'en Phase 4bis (audit DA), soit 2 phases trop tard.
7. L'orchestrateur ouvre le fichier dans TextEdit, affiche un résumé court dans le chat (~400 tokens : nom + palette + typo + territoire visuel pour chaque concept), et demande validation des 3 concepts. **Pas encore de choix** — les 3 sont validés ensemble.

**Règle typographique critique** : les polices doivent venir de Google Fonts (vérifiable). Chaque curseur A a un pool de 50+ polices. L'interdiction des "fausses" polices type Fontshare (General Sans, Satoshi, etc.) est dans le prompt car le subagent a tendance à les inventer.

**Sous-pipeline post-spécimens (depuis D51, 29 avril 2026)** : après les spécimens typo+palette validés (Vague 3), la séquence est `3B-7a (styliste) → 3B-7b (spécimens stylisés) → 3B-7-checkpoint (choix variante de style) → 3B-7c (penseur visuel) → 3B-7d (pitch) → 3B-7e (génération visuels MJ/Recraft)`. Le styliste choisit le style officiel reconnu (parmi 34 fiches du catalogue), valide visuellement par 9 spécimens stylisés (3 concepts × 3 variantes), l'utilisateur arbitre 1 variante par concept au checkpoint. Le penseur visuel **reçoit alors la fiche styliste retenue en input** et DÉRIVE son ancre stylistique (registre, lumière, grain, abstraction, bords) des signatures et références culturelles de la fiche — il n'invente plus librement. La direction visuelle est ensuite consommée par le pitch (qui reçoit aussi la fiche styliste) et par le skill `/visual-prompt` (3B-7e en mode variantes) pour la génération MJ/Nano Banana 2/Recraft. Cohérence garantie : un seul univers stylistique de bout en bout.

**Routeur chromatique 3B-0a — mode exhaustif (depuis D53, 5 mai 2026)** : étape pré-design qui précède la divergence des concepts. Subagent isolé (custom agent `chromatic-router`, aucun accès fichier) qui scanne un catalogue canonique de ~45 sous-gammes du spectre (`ref/chromatic-spectrum-catalog.md`, 14 familles de teintes × 2-5 sous-variantes) et classe chacune dans 3 catégories : recommandées (cible 10-15, plafond 18), non recommandées (étrangères ou redondantes fonctionnellement avec une recommandée — réserve d'arbitrage utilisateur), fortement non recommandées (contradictions franches). Le catalogue donne les CATÉGORIES, le routeur produit les NOMS contextualisés au brief (ex: "Bordeaux de sceau notarial" plutôt que "Rouges profonds bordeaux"). Gate anti-slop mécanique (`scripts/phase3b-gamut-router-anti-slop.py`, 11 checks dont inflation max 18 et couverture min 30 sous-gammes catégorisées). Planche HTML générée par `lib/gamut-visual.mjs` (3 sections, swatches en pleine couleur, distinction par bordure latérale rouge pour exclues / grise pour non recommandées). Le sous-agent palette aval (Phase 3B-3) reçoit le bloc complet et scanne les recommandées pour choisir 1-2 gammes dominantes.

---

### Phase 3C · Visuels de référence (SKILL SÉPARÉ : `/visual-prompt`, renommé 3B-7e depuis D51)

- **Ce qu'elle fait** : Génère les visuels finaux (hero + atmosphere/closeup/macro/pov dérivés) via un workflow itératif MidJourney → Nano Banana 2 → Recraft, et prépare leur intégration dans les Batches 2/3
- **Input** : Fiche styliste retenue (`{brand}-style-choice-c{N}.md`) + direction visuelle ancrée (`{brand}-visual-direction-c{N}.md` ou `{brand}-visual-pivot-c{N}.md`) + palette du concept retenu
- **Output** : Librairie `visual-final/{brand}-c{N}-{paletteID}-{type}[-{variante}].{ext}` (jusqu'à 7 types : hero, atmosphere ×4 intensités, closeup, macro, pov, schema) consommée par Batch 3 (chapitres 08/10)
- **Exécution** : **Skill standalone** (`/visual-prompt`) dans une **session Claude Code séparée** — 2 modes : **principal** (génération d'un visuel hero depuis une description Perplexity) et **variantes** (dérivation atmosphere/closeup/macro/pov depuis un hero existant)
- **Note historique** : remplace l'ancien skill `/visual-brief` (déprécié depuis mai 2026) qui produisait des prompts MJ/Recraft sans la qualité élite que permet le workflow itératif avec Nano Banana 2

**Sous le capot** :
1. L'orchestrateur BIG, en Phase 3B-7c.7, propose une 1re génération du **hero** via `/visual-prompt` mode principal (à partir de la description Perplexity de l'image-pivot).
2. En Phase 3B-7c.10 (juste après validation du hero), propose la **génération immédiate de variantes** via `/visual-prompt` mode variantes.
3. En Phase 3B-7e (largement optionnelle), propose une 2e opportunité d'enrichir la librairie si l'utilisateur veut générer plus de variantes une fois les pitches finalisés.
4. **Dans la session `/visual-prompt`** (contexte frais, framework librairie atmosphère chargé avec toute l'attention) :
   - Lit la fiche styliste et la direction visuelle directement sur disque
   - Génère via MidJourney pour la photo / art conceptuel / textures, ou Recraft pour les illustrations flat / line art / infographies
   - Utilise Nano Banana 2 (`/nano-banana-edit`) pour les corrections atomiques (couleur de fond, grain, tons, clair-obscur)
   - Gate élite 6/6 critères en sortie
   - Range les fichiers dans `visual-final/` avec naming standardisé (§11.7 du framework)
5. L'utilisateur revient dans la session BIG → l'orchestrateur détecte la librairie `visual-final/` et continue.

**Pourquoi un skill séparé** : L'orchestrateur, après ~8 phases, avait trop de contexte pour suivre rigoureusement les guides MJ/NB2/Recraft. Le skill dédié charge les guides avec un contexte frais et les suit à la lettre. Le mode "variantes" exploite le framework librairie atmosphère (`nb-prompting-guide.md §11` — 7 types × 4 niveaux d'intensité) pour produire une famille cohérente depuis un hero existant.

**Cerveau du skill** : `ref/visual-direction-guide.md` (jugement DA) + `ref/midjourney-prompting-guide.md` + `ref/recraft-prompting-guide.md` + `ref/recraft-routing-rex.md` + `ref/image-composition-patterns.md`

---

### Phase 4 · Style-Tiles HTML

- **Ce qu'elle fait** : Génère 3 fichiers HTML immersifs, chacun présentant un concept validé dans un format triptyque
- **Input** : `{brand}-pitch.md` + visuels base64 (optionnel) + exemple HTML du niveau A
- **Output** : 3 fichiers `{brand}-style-tile-concept-{1,2,3}.html`
- **Règles clés** :
  - **Format triptyque** : Voice Block (hero typographique) → Artefact Témoin (composant UI complexe) → Atmosphere Block (immersion/mood)
  - **:root sacré** : 40-60 CSS custom properties en 7 catégories
  - **11 quality gates** : Screenshot Test, Mason's Rule, cohérence curseurs, alignement brief, pas d'images auto-générées, zéro code mort, couverture custom properties, profondeur de surface, CSS moderne (min 4 techniques 2023-2026), anti-patterns datés (blacklist mécanique via `phase4-blacklist-gate.py` — aucun translateY hover, aucune animation infinite, aucun glow shadow, aucun séparateur fantaisie, etc.), finition élite

**Sous le capot** :
1. L'orchestrateur lance **3 subagents EN PARALLÈLE** (dans un seul message avec 3 Task tools) — un par concept
2. Chaque subagent reçoit un prompt quasi-identique, sauf :
   - Le numéro et nom du concept
   - Les détails visuels extraits du pitch (palette, typo, artefact recommandé, philosophie d'interaction, techniques CSS, registre atmosphérique)
   - Le bloc de visuels base64 (si fournis pour ce concept)
3. Chaque subagent lit 6 fichiers de référence : `persona-and-rules.md`, `bible-design-strategie.md`, `master-style-guide.md`, `output-framework-zone1.md` (règles du showroom), `html-showroom-spec.md` (spec technique), et **1 exemple HTML** correspondant au niveau du curseur A (il existe 3 exemples : un par niveau A)
4. L'exemple montre le NIVEAU DE QUALITÉ à atteindre (richesse CSS, techniques modernes, format triptyque), mais le subagent a l'interdit explicite de copier les choix créatifs (fonts, palette, type d'artefact, type de layout)
5. Le subagent génère un fichier HTML unique, self-contained (tout le CSS dans `<style>`, Google Fonts via `<link>`)
6. Le bloc `:root` contient les 7 catégories de custom properties : palette (primary, secondary, accent, surface, text, semantic, dataviz), typo (display, body, mono), type-scale (ratio indexé sur curseur A + tailles calculées), spacing, radius, shadows, transitions
7. Le subagent auto-vérifie les 11 gates avant de finaliser. Si un gate échoue → il corrige avant de livrer
8. **Mécanisme de l'artefact témoin (méthode 3 étapes — D52)** : un subagent dédié `phase-4-artefact.md` produit la zone médiane (composant UI complexe) selon une méthode hybride en 3 étapes — **(1) Ancrage support n°1 du brief** : le subagent identifie le type d'objet attendu par le brief (le support sur lequel la marque vit prioritairement) et le respecte. Le style retenu dit COMMENT signer, pas QUOI produire à la place. **(2) Grammaire interne libre** : le subagent pose en commentaire HTML (1-3 lignes) la forme de composition de l'artefact à l'intérieur du type d'objet imposé. La grammaire émerge du dialogue pitch + style + palette + fonts + interdits + brief, pas d'un catalogue d'archétypes pré-défini. **(3) Quotas par catégorie** : 5 catégories fonctionnelles avec quotas minimum (typographie ≥4 niveaux, donnée ≥2, état ≥1, action ≥1, identité brand ≥1 = ~9 atomes minimum). Le format de chaque atome est dicté par la grammaire posée à l'étape 2, pas par un template imposé. **Anti-contamination stricte** : aucun exemple concret d'archétype ou de format d'atome dans les consignes — les exemples deviennent un menu déguisé qui pousse le LLM à piocher au lieu d'inventer. La complétude design system est préservée par la checklist obligatoire de Batch 2 (chapitre 04 — Code Civil Atomique) qui force la création des composants UI manquants en s'appuyant sur le design language posé. Avant D52, l'artefact suivait une liste rigide de 15 atomes nommés (KPI dominant + segmented control + table + alerte + boutons primary/secondary + input + 2 cards + 5 niveaux typo + badge + navigation hint) qui forçait systématiquement le format dashboard productivity, quel que soit le concept.
9. Après livraison, **3 subagents contrôleurs** (étape 4A-ter) exécutent 2 scripts de gate mécaniques : `phase4-finishing-gate.py` (qualité CSS) + `phase4-blacklist-gate.py` (patterns datés). Si FAIL → renvoi au subagent Phase 4 pour correction (max 2 itérations)
10. L'orchestrateur ouvre les **3 fichiers dans 3 fenêtres de navigateur** (3 `open` successifs), présente les noms des concepts (A, B, C), et demande si ajustements souhaités avant le choix final

**Calibrage CSS par curseur A** — ce que chaque niveau exige concrètement dans le HTML :
- **A=1** : grilles régulières, surfaces simples, interactions conventionnelles, CSS moderne mais établi (oklch, @layer, text-wrap)
- **A=2** : ≥1 asymétrie (ratio 60/40, élément décalé), ≥1 surface expressive (texture, overlay, ombre colorée), interactions qui expriment le concept, ≥1 technique non-standard (@property animé, color-mix, clip-path, container query, animation-timeline)
- **A=3** : ≥1 convention de layout cassée (chevauchement, z-index expressif), surfaces composites (blend modes, masques), interactions narratives, ≥1 technique de pointe (@starting-style, scroll-driven animations, subgrid composé)

---

### Phase 5 · Choix + itération

- **Ce qu'elle fait** : L'utilisateur compare, ajuste, et choisit son concept final
- **Input** : 3 HTML dans le navigateur + feedback utilisateur
- **Output** : Concept choisi + slug

**Sous le capot** :
1. L'orchestrateur présente les 3 concepts par lettre (A, B, C) et demande si ajustements souhaités
2. Si ajustement sur un concept → **resume le subagent correspondant** (via `resume: agentId` du Task tool Phase 4) avec le feedback ciblé. Le subagent reprend avec tout son contexte + le feedback, modifie le HTML, et l'orchestrateur ré-ouvre le fichier dans le navigateur
3. Boucle jusqu'à validation explicite
4. Quand l'utilisateur choisit : l'orchestrateur stocke le numéro (1/2/3), le nom, et génère le **slug** (version URL-safe du nom, via un script Python : normalisation Unicode, minuscules, tirets, max 40 caractères)
5. Le slug est utilisé dans TOUS les noms de fichiers des phases suivantes
6. **À partir de maintenant, le :root du concept choisi est VERROUILLÉ** — il ne changera plus

---

### Étape 5D · Animation du style-tile (optionnelle, toujours proposée)

- **Ce qu'elle fait** : Ajoute une couche d'animation moderne (GSAP ScrollTrigger/SplitText + CSS natif) au style-tile retenu, sous forme de variantes de dosage à comparer
- **Input** : le style-tile retenu `{brand}-style-tile-concept-{n}.html` (complet) + le registre/style du concept (`{brand}-style-choice-c{n}.md` / `{brand}-pitch.md`) + `ref/animation-catalogue.md` + `ref/animation-implementation-guide.md`
- **Output** : `{tile}-animated.html` (variante retenue, dépend du CDN GSAP avec garde-fou statique) + `{brand}-animation-spec.md` (preset retenu + deps) + `{brand}-animation-menu.md` + `_archive-anim-{round}/` (variantes non retenues). Le style-tile statique reste **intact**.
- **Règles clés** :
  - **Couche purement additive** : le sous-agent n'ajoute que les `<script src>` CDN, un `<style>` scopé `html.gsap-anim …`, des `data-` neutres, et un `<script>` d'init en IIFE avec garde-fou. Il ne touche **jamais** au `:root`/`@layer tokens`/CSS validé/`<script>` existants → non-régression stricte (pourquoi : le style-tile statique est un livrable validé, l'animation est un bonus séparé).
  - **Scroll natif, pas de smooth-scroll par défaut** (pourquoi : le smooth-scroll donne une sensation « lourde » ; il reste proposable en opt-in mais jamais dans un preset).
  - **Mode sûr hero** : si le hero a un overlay calé sur le cadrage de l'image (SVG/canvas géométrie pixel — ex : faisceau de phare), pas de zoom/pin/parallaxe multi-couches sur le hero, on n'anime que le texte (pourquoi : zoomer/déplacer l'image désaligne l'overlay).
  - **Anti-slop** : pas de mesh/aurora/particules en fond, pas de pin long, easings sobres, `prefers-reduced-motion` toujours respecté.
- **Enchaînement** : reçoit le concept retenu de la Phase 5 → enchaîne sur la Phase Logo (ou Phase 6A).

**Sous le capot** — 6 sous-étapes (pattern Phase Logo) :

**5D-0 — Proposition** (orchestrateur) : question Oui/Non. Si non → `{animation_done}` = false, pipeline inchangé.

**5D-1 — Analyse + preset recommandé** (orchestrateur, inline — PAS de subagent) : lit le style-tile retenu → détecte les facteurs de risque hero (overlay positionné, vidéo de fond, mask-image) → `{hero_safe_mode}` ; lit `{brand}-style-choice-c{n}.md`/`{brand}-pitch.md` → `{registre}` ; lit `ref/animation-catalogue.md` § « Presets recommandés » → choisit le preset (P1 si mode sûr, sinon P2-P5 selon registre, défaut P0) ; génère `{brand}-animation-menu.md` (catalogue 6 axes + preset pré-coché ✅ + options incompatibles barrées ⊘), ouvert en MarkView ; présente un résumé court.

**5D-2 — Collecte du choix** (orchestrateur) : l'utilisateur ajuste/valide en langage libre → `{animation_choice}` (liste finale des options par axe, refusant les options barrées par le mode sûr).

**5D-3 — Sous-agent animateur** (1 subagent, `phases/phase-5d-animation.md`) : reçoit `{tile_basename}`, `{animation_choice}`, `{registre}`, `{hero_safe_mode}`, `{hero_overlay_note}` ; lit `ref/animation-catalogue.md` + `ref/animation-implementation-guide.md` + `ref/html-showroom-spec.md` (§6) + le HTML source ; produit 2-3 variantes `{tile_basename}-animated-v{1,2,3}.html` (subtil → médian → prononcé, même liste d'options, seul le dosage varie ; v3 peut ajouter au plus une option bonus compatible).

**5D-4 — Présentation + itération** (orchestrateur) : ouvre les variantes dans le navigateur, présente le résumé, l'utilisateur choisit une variante / demande des ajustements → resume le subagent (agentId) → reboucle jusqu'à validation.

**5D-5 — Finalisation** (orchestrateur) : promeut la variante retenue → `{tile_basename}-animated.html` ; archive les autres dans `_archive-anim-{round}/` ; écrit `{brand}-animation-spec.md` ; `{animation_done}` = true ; enchaîne sur la Phase Logo. Le packaging final (Étape Finale) copie aussi `{brand}-style-tile-animated.html` + `{brand}-animation-spec.md` dans le dossier livrable si `{animation_done}` = true.

**Stack** : GSAP 3.13 (`ScrollTrigger` + `SplitText`) via CDN. Garde-fou : `if (reduceMotion || !window.gsap || !window.ScrollTrigger) { revealAll(); return; }` → si le CDN est indisponible ou si l'OS demande de réduire les animations, le style-tile s'affiche statique. **Piège connu** : le style-tile animé n'est plus 100 % self-contained (dépend du CDN) — c'est assumé, d'où la coexistence avec la version statique. Prototypes de référence (recettes GSAP/CSS) : `outputs/test-camille-test-20260511-1330/camille-style-tile-concept-3-palette-B-creme-ANIM-v3.html` (+ variantes par effet `-ANIM-1/2/3/v2-phare-safe`).

---

### Phase Logo (optionnelle, toujours proposée)

- **Ce qu'elle fait** : Crée un logo professionnel en 5 étapes
- **Input** : Pitch du concept choisi, tension, scoping, :root du style-tile
- **Output** : 6 SVGs dans `outputs/{session_dir}/`

**Sous le capot** — 5 étapes séquentielles :

**L0 — Proposition** (orchestrateur) : Pose la question "Oui/Non". Si non → `{logo_available}` = false, les phases suivantes fonctionnent sans logo (backward compatible).

**L1 — Concept** (1 subagent) : Le subagent lit la `logo-design-bible.md` (~800 lignes, le guide complet), le REX logo, le pitch choisi, le scoping, et les variables :root. Il produit : idée centrale (métaphore pont stratégie→forme), 3 niveaux de lecture (immédiat/symbolique/systémique), anti-patterns vérifiés, type de logo recommandé, **3 prompts MidJourney** respectant les 7 règles du REX, et un score prédictif Paul Rand (seuils : 60/75 et 75/100 — si en dessous → itération avant de finaliser). Le fichier est ouvert dans TextEdit, les prompts NE SONT PAS copiés dans le chat.

**L2 — Génération** (utilisateur dans MidJourney) : L'utilisateur copie le Prompt 1 depuis le fichier, génère dans MidJourney. L'orchestrateur analyse les grilles de résultats, recommande quel résultat choisir. Boucle : Vary (Strong) pour micro-variations → Upscale 4x sur le gagnant → téléchargement PNG. Max 3-5 rounds par prompt, sinon pivot (changer de type de logo).

**L3 — Vectorisation** (orchestrateur) : Auto-trace via `vtracer` (pip package) : PNG → SVG. Post-traitement obligatoire : suppression du path de fond, suppression des artefacts d'antialiasing, correction des couleurs (fills approximatifs → HEX exacts du :root), ajustement du viewBox (cadrage serré + padding), ajout de métadonnées. **Règle critique** : ne JAMAIS écrire manuellement des paths SVG pour des logos organiques — ça échoue systématiquement (REX documenté).

**L4 — 6 déclinaisons** (orchestrateur) :
1. Bicolore (déjà fait en L3)
2. Négatif (fond dark, couleurs adaptées)
3. Monochrome navy (tout en `--color-depth`)
4. Monochrome blanc (tout en #FFFFFF)
5. Lockup primaire (mark + nom, vertical) — via technique `<svg>` imbriqué (pas `<g transform="scale()">` qui casse les paths vtracer — REX documenté, 3 échecs)
6. Lockup secondaire (mark + nom, horizontal)

Les lockups nécessitent un calcul de tight viewBox (les paths vtracer ont du padding) via script Python qui parse les coordonnées réelles des paths.

**L5 — Validation** : Les 6 SVGs sont ouverts dans Chrome. L'utilisateur valide ou demande des ajustements.

---

### Phase 6A · Batch 2 (Système de Signes) — refonte D59 (2026-05-27)

**Architecture en 2 étapes filles depuis D59** :
- **Étape 6A-0 — Router Famille d'Icônes** : nouveau subagent isolé qui choisit UNE famille parmi 8 (pictogramme géo / isométrique / pixel / gravure / ornemental / flat illustré / sticker / brutaliste) documentées dans `ref/icon-system/catalogue/`. Modèle copié du routeur chromatique 3B-0. Output : `{brand}-icon-family-choice.md`. Validation user obligatoire.
- **Étape 6A-1 — Batch 2 HTML** : subagent designer Batch 2 (existant, refondu) qui consomme la famille choisie + sa fiche catalogue + sa slop sheet et produit le HTML.

- **Ce qu'elle fait** : Génère un HTML couvrant Logotype (4 sections), Iconographie (3 sections refondues D59), UI Components (5 sections), Data Viz (4 sections)
- **Input** : :root extrait + pitch du concept choisi + SVGs logo (si disponibles) + exemple Batch 2 + **`{icon_family_id}` + `{icon_family_label}` + `{router_justification}`** (depuis Étape 6A-0) + fiches `ref/icon-system/catalogue/{id}.md` et `ref/icon-system/slop-sheets/{id}.md`
- **Output** : `{brand}-icon-family-choice.md` (Étape 6A-0) + `{brand}-batch2-{slug}.html` (Étape 6A-1, 11 sous-sections)
- **Règles clés** :
  - **Specs Lock** : le :root doit être IDENTIQUE à celui du style-tile validé
  - **Placeholder protocol** : les logos SVG sont injectés en post-traitement
  - **Chapitre 06 refondu en 3 sections orientées USAGE** (D59) : 06.1 Set d'icônes UI 18-22 icônes utilisables (UI primaire + UI métier + statuts) dans le traitement principal natif de la famille / 06.2 Traitements alternatifs 1-2 max étiquetés cas d'usage business / 06.3 Usage en contexte 1 mockup avec squelette imposé (sidebar / table+toolbar / toolbar / breadcrumb / list / nav, pas de duplication chapitre 04). PAS de "Outline/Solid/Duotone" en dur — chaque famille a ses propres traitements natifs.
  - **Anti-pattern racine** : les icônes du chapitre 06 sont des fonctions UI (search, settings, user, calendar…), PAS des illustrations narratives du concept (pas de phare, sextant, scène d'auscultation)
  - **Gate anti-slop (D56)** : après génération (et injection SVG), `scripts/phase6-batch-gate.py` tourne une fois sur le fichier complet ; auto-correction chirurgicale (1 tour max) sur les `deterministic_fails` (Specs Lock / Completeness / police bannie), reste surfacé à l'utilisateur

**Sous le capot** :
1. **Préparation par l'orchestrateur** (avant de lancer le subagent) — 5 étapes de préparation :
   - **Extraction du :root** : lit le HTML du style-tile choisi, extrait le bloc `<style>` contenant `:root { ... }` et les `<link>` Google Fonts
   - **Allègement du style-tile** : si le fichier fait > 200 Ko (images base64 embarquées), crée une version allégée (remplace les data URIs par des placeholders) pour ne pas exploser le contexte du subagent
   - **Extraction du concept choisi** : au lieu d'envoyer le pitch complet (~16K tokens, 3 concepts), extrait seulement le concept choisi + les métadonnées du header. Méthode : grep le heading du concept, lire de là jusqu'au heading du concept suivant
   - **Extraction du catalogue CSS** : extrait la section 6 de `html-showroom-spec.md` (vocabulaire CSS moderne) au lieu d'envoyer le fichier complet
   - **Si logo disponible** : extrait les dimensions du viewBox du SVG bicolore et construit un bloc d'instructions pour l'utilisation des placeholders (quels placeholders pour quelles sections, règles CSS obligatoires pour dimensionner les SVG injectés)
   - **Inventaire des visuels finaux dérivés** (D54) : scanne `{session_dir}/visual-final/`, parse le naming `{brand}-c{N}-{paletteID}-{type}[-{variante}].{ext}` (7 types : hero, animation, atmosphere ×4 intensités, closeup, macro, pov, schema), exclut les sources hires, restreint au concept retenu. Si plusieurs palettes → demande à l'utilisateur laquelle correspond au style-tile retenu. Construit `{cover_visual_rel}` (1 visuel pour Batch 2, hero de préférence), `{visual_library_ch08}` et `{visual_library_ch10}` (blocs table + règles d'affichage pour Batch 3). Dossier absent → les 3 variables vides, pipeline inchangé

2. Lance **1 subagent** avec toutes ces données pré-extraites. Le subagent lit aussi `persona-and-rules.md`, `bible-design-strategie.md`, `master-style-guide.md`, et un exemple de Batch 2 (pour le standard de qualité)

3. Le subagent génère un HTML avec 11 sections (depuis D59 : chapitre 06 passé de 4 à 3 sections) :
   - 05.1-05.4 : Logotype (concept, lockups, safe area, variantes contextuelles)
   - 06.1-06.3 : Iconographie REFONDUE D59 (Set d'icônes UI / Traitements alternatifs / Usage en contexte)
   - 04.1-04.5 : UI Components (Buttons, Forms, Badges, Cards, Feedback&Nav)
   - 07.1-07.4 : Data Viz (styles graphiques, grilles, palette, typo données)

4. Le subagent écrit un progress log (`{session_dir}/.progress-batch2.log`) à chaque chapitre terminé — l'orchestrateur peut le lire pour détecter les blocages

5. **Post-traitement** (orchestrateur) — si logo disponible :
   - Script Python qui remplace chaque `<!-- PLACEHOLDER:LOGO_* -->` par le contenu SVG réel
   - Vérification : `grep "PLACEHOLDER:LOGO"` doit retourner 0 résultats, `grep "<svg"` doit retourner ≥6
   - Si placeholders restent → un SVG est manquant → alerte utilisateur

6. **Gate anti-slop** (orchestrateur, D56) : extrait le `:root` du style-tile retenu dans `.expected-root.css`, lance `scripts/phase6-batch-gate.py {batch2_file} --batch 2 --cursor-a … --expected-root … --json-output .gate-batch2.json` (le gate strippe les `<svg>`/`data:` URIs, délègue aux gates Phase 4 `blacklist`+`finishing`, re-pondère selon un profil « documentation batch », ajoute Specs Lock / Completeness / external-image / Lorem ipsum). Si `deterministic_fails` non vide → resume le subagent Batch 2 (son `agentId`) en mode CORRECTION CHIRURGICALE avec la liste des violations → re-run du gate (1 tour max), résiduel surfacé à l'utilisateur. `other_fails` (anti-patterns datés visibles, …) et `warns` → affichés avec « je corrige ? », pas d'auto-trigger

7. L'orchestrateur ouvre le fichier dans le navigateur (APRÈS injection + gate) et demande validation

---

### Phase 6B · Batch 3 (Narration & Espace)

- **Ce qu'elle fait** : Génère un HTML couvrant Direction Photo (4 sections), Composition (4 sections), Illustration (5 sections)
- **Input** : :root + pitch + style-tile + Batch 2 (pour référence) + visuels finaux dérivés (`{visual_library_ch08}` / `{visual_library_ch10}`, si une librairie `visual-final/` existe — sinon vide)
- **Output** : `{brand}-batch3-{slug}.html` — 15 sections obligatoires
- **Règles clés** : Specs Lock identique au Batch 2 ; gate anti-slop (D56) après l'assemblage (« Étape 6B-6 »)

**Sous le capot** :
- Fonctionnement quasi-identique au Batch 2 : mêmes préparations orchestrateur (extraction :root, allègement, extraction concept, extraction catalogue CSS, inventaire des visuels finaux dérivés)
- Génération en 3 subagents séquentiels (ch08, ch09, ch10) qui lisent les mêmes refs + le style-tile + le Batch 2 (pour cohérence visuelle) ; le bloc de contexte partagé inclut la section « AUTO-AUDIT ANTI-SLOP DE TON CHAPITRE » (squint test, cards earn existence, data-ink, Show > Tell — scopé au chapitre)
- L'orchestrateur écrit le squelette HTML (header + `@layer` + `:root` extrait), chaque subagent écrit un fragment `.tmp-batch3-ch{NN}.html`, puis assemblage (Étape 6B-5) + `rm` des `.tmp`
- Les 15 sections : 08.1-08.4 (Photo), 09.1-09.4 (Composition), 10.1-10.5 (Illustration)
- **Visuels finaux dérivés (D54)** : si `visual-final/` contient des visuels pour le concept retenu, le chapitre 08 affiche les images réelles (atmosphere/macro → 08.1 moodboard + 08.2 color grading où les 4 niveaux d'intensité sont la démonstration littérale ; hero/pov/animation → 08.3 scénographie ; closeup → 08.1) **en remplacement** des cartes CSS qui ne faisaient que "décrire" une ambiance ; le chapitre 10 affiche les schemas en contexte d'usage. Embedding par chemin relatif (`<img src="visual-final/…">`, `<iframe>` pour les `.html`), jamais en base64 → le fichier n'est alors plus 100 % self-contained, le dossier `visual-final/` voyage avec
- Pas de placeholder protocol ici (pas de logos à injecter)
- **Étape 6B-6 — Gate anti-slop (D56)** : après l'assemblage, `scripts/phase6-batch-gate.py {batch3_file} --batch 3 …` tourne une fois sur le fichier assemblé (mêmes checks que Batch 2). Auto-correction (1 tour max) sur `deterministic_fails` : `specs-lock` → l'orchestrateur réécrit directement le `:root` du `@layer tokens` du header à l'identique ; `completeness`/`R013` → resume le subagent du chapitre concerné (champ `chapter` de la violation) en mode CORRECTION CHIRURGICALE sur le fichier assemblé. `other_fails`/`warns` surfacés à l'utilisateur
- Mêmes gates auto-déclarés que Batch 2 (Specs Lock, Completeness, Screenshot Test, Cursor Coherence, Zero Dead Code, Show > Tell, Anti-Patterns Datés, Finition Élite)

---

### Phase 7 · Documentation Markdown

- **Ce qu'elle fait** : Génère les design specs Markdown
- **Input** : Tous les outputs précédents (style-tile retenu, pitch, batches, brief analysis)
- **Output** : `{brand}-design-specs-{slug}.md` (~45 sections, 15-20K tokens) — source de vérité textuelle utilisée par les phases 8 et 8b
- **Enchaînement** : déclenche soit Phase 8 (Brand Book), soit Phase 8b (Design System), soit directement l'Étape Finale Packaging selon les choix utilisateur

---

### Phase 8 · Brand Book éditorial (optionnel)

- **Ce qu'elle fait** : Génère un brand book HTML éditorial pour les parties prenantes
- **Input** : Pack BIG complet (design-specs.md + style-tile + batch2 + batch3 + visual-final/) + dépendance SPG-portable côte à côte
- **Output** : Sous-dossier `{session_dir}/brand-book/` contenant `{brand}-brand-book.html` + visuels finaux + 6 PNG retina mini-deck + 2 mockups social
- **Règles clés** :
  - Question utilisateur skippable : `(a) Oui — générer` / `(b) Non — passer au Packaging`
  - Gate juste-à-temps SPG-portable (3 options : clone / dégradé sans Pitch Deck / skip complet)
  - **Règle §8quater "Fidélité au pack source"** (sanctuarisée 27 mai 2026) : inventaire 1:1 obligatoire pour les sections documentaires (06a Iconographie, 06b Composants UI, 06c Dataviz, 06d Composition)
- **Enchaînement** : si done → Phase 8b (Design System) ; si skip → directement Étape Finale Packaging

**Sous le capot** :
1. Orchestrateur lance 1 sub-agent Task tool qui invoque le skill `/brand-book`
2. Le skill brand-book lit le SKILL.md du brand-book (~600 lignes) et orchestre 7 sous-étapes (8-2a..e + 8-3)
3. La sous-étape 8-2d invoque elle-même un sous-sub-agent pour `/SPG/generate-mini-deck` (~150K tokens, le plus lourd)
4. Sortie centralisée dans `{session_dir}/brand-book/`, copiée en tête de l'index.html du pack final

---

### Phase 8b · Design System technique (optionnel)

- **Ce qu'elle fait** : Génère un design system HTML technique sobre type Carbon / Atlassian pour les équipes design et engineering. Complète le brand book par les spécifications opposables.
- **Input** : Pack BIG complet (design-specs.md + style-tile + batch2 + batch3 + visual-final/) — pas de dépendance externe
- **Output** : Sous-dossier `{session_dir}/design-system/` contenant :
  - `{brand}-design-system.html` (livrable principal, 11 sections : Color, Typography, Spacing, Iconography, Logo, Data viz, Photography, Composition, Illustration, Motion, Tokens)
  - `{brand}-design-system-inventory.json` (~200 items attendus vs présents)
  - `{brand}-design-system-audit-sources.json` (mapping items source)
  - `{brand}-design-system-audit-report.json` (rapport script Python)
- **Règles clés** :
  - Question utilisateur skippable : `(a) Oui — générer` / `(b) Non — passer au Packaging`
  - **14 règles sanctuarisées** dans `.claude/skills/design-system/ref/design-system-generation-rules.md` (notamment R12 inventaire 1:1, R13 catalogage strict — interdit business-speak sur captions —, R14 checklist par section)
  - **Tableau inventaire-type** dans SKILL.md (~120 items canoniques à compter dans la source)
  - **PAS de section Voice** (décision tranchée mai 2026 — appartient au brand book)
  - Audit Python automatique en fin de génération (`design-system-audit.py`) qui vérifie inventaire, sourcing, tailles font-size, patterns AI-slop
- **Enchaînement** : si done → Étape Finale Packaging (qui copie `design-system/` dans le pack final) ; si skip → directement Étape Finale Packaging

**Sous le capot** :
1. Orchestrateur lance 1 sub-agent Task tool qui invoque le skill `/design-system`
2. Le sub-agent lit OBLIGATOIREMENT (a) `SKILL.md` design-system, (b) `design-system-generation-rules.md`, (c) tableau inventaire-type, (d) template HTML de référence
3. Génère le HTML en 11 sections + 2 fichiers JSON d'audit en parallèle
4. Orchestrateur lance `python3 scripts/design-system-audit.py {session_dir} --json-output` pour validation anti-régression
5. Si audit fail (critical > 0) → question utilisateur (continuer / relancer / skip)
6. Sortie centralisée dans `{session_dir}/design-system/`, copiée dans l'index.html du pack final juste après le brand book

---

### Étape Finale · Packaging

- **Ce qu'elle fait** : Empaquète tout dans un dossier dédié et déploie sur Vercel
- **Input** : Tous les outputs précédents + brand-book/ si Phase 8 + design-system/ si Phase 8b
- **Output** : Dossier `{brand}-identity-{slug}/` avec tous les livrables + déploiement Vercel automatique

**Sous le capot** :
1. Crée le dossier de packaging dans `outputs/{session_dir}/`
2. Copie et renomme les fichiers :
   - Style-tile HTML (renommé pour enlever le "concept-{n}")
   - Batch 2 et 3 HTML
   - Design specs markdown
   - Pitch du concept choisi (extrait du pitch complet)
   - SVGs logo (6 variantes, si disponibles)
   - Images hero et atmosphere (extraites du HTML en base64 → reconverties en fichiers séparés)
   - Si `{brand_book_done}` : copie récursive de `brand-book/`
   - Si `{design_system_done}` : copie récursive de `design-system/`
3. Génère un `index.html` avec navigation : brand book en tête (si présent), puis design system, puis bento (legacy), puis style-tile, batch 2, batch 3
4. Déploiement Vercel automatique
5. Ouvre le dossier dans Finder

---

## Briques détaillées — Mode Aspiration

### D1 · Collecte (orchestrateur, pas de subagent)

- **Ce qu'elle fait** : Capture le site web existant
- **Input** : 2-5 URLs (homepage obligatoire) + nom de marque + logo (optionnel)

**Sous le capot** :
1. **Screenshots** via Chrome headless (`--headless --screenshot`, taille 1440×900). Si Chrome non trouvé → demande screenshots manuels
2. **HTML brut** via `curl -sL` pour chaque URL
3. **CSS extraction** : parse le HTML pour trouver les `<link rel="stylesheet">` et `<style>`, curl les CSS externes, concatène dans `{brand}-extracted-css.txt`
4. **Contenu texte** via WebFetch (pour analyse du ton de voix) — extraction de tout le texte visible avec hiérarchie
5. **Logo** si fourni : lu via Read tool (multimodal)

### D2 · Extraction (1 subagent)

- **Ce qu'elle fait** : Analyse tout pour produire le Brand DNA
- **Output** : `{brand}-extracted-dna.md`

**Sous le capot** :
- Le subagent lit le CSS extrait, les HTML, les screenshots (multimodal), le logo, et le contenu textuel
- Extraction en 6 étapes : tokens CSS (haute confiance), analyse visuelle des screenshots (confiance moyenne), analyse textuelle du ton (confiance moyenne), analyse logo, positionnement estimé (curseurs A×B), gap-filling (éléments manquants)
- Chaque valeur est annotée : ✅ Extrait (CSS) > 🔍 Analysé (visuel) > 💡 Proposé (gap-fill)
- **Règle** : les valeurs CSS ont priorité absolue. Ne jamais inventer une couleur qui n'est pas dans le CSS ou les screenshots.

### D3 · Validation (orchestrateur)

- Présente une synthèse courte (~400 tokens) : palette, typo, radius, style, curseurs estimés
- Demande corrections sur les points incertains
- Boucle jusqu'à validation explicite
- Complète les tokens manquants (data-viz, sémantiques)

### D4 · Style-Tile (1 subagent)

- Même format triptyque que Phase 4, mais **1 seul** (pas 3 concepts)
- Les tokens design sont EXACTEMENT ceux du Brand DNA (zéro déviation), le layout est libre
- Mêmes gates que Phase 4 créative

### D5 · Validation → Convergence

- L'utilisateur valide la fidélité du style-tile à sa marque
- Boucle d'itération si ajustements
- **Après validation** : le pipeline converge vers Phase 6A. Variables adaptées : pas de slug de concept (le brand name suffit), pas de pitch (le Brand DNA le remplace), le packaging inclut le Brand DNA au lieu du pitch

---

## Patterns transverses

| Pattern | Règle | Pourquoi |
|---------|-------|----------|
| **:root sacré** | 40-60 custom properties en 7 catégories, verrouillées après Phase 5 | Source de vérité unique — empêche la dérive entre batches et permet aux outils en aval (LPG, SPG) de consommer les tokens |
| **Anti-contamination** | Les exemples montrent le NIVEAU DE QUALITÉ, jamais la direction créative. Le prompt liste explicitement tout ce qu'il est interdit de copier | Empêche que toutes les marques finissent par se ressembler |
| **Session isolation** | 1 dossier + `.session-id` par exécution, vérifié avant chaque subagent | Permet d'explorer des directions parallèles sans collision |
| **Screenshot Test** | "Cet élément serait-il visible sur un screenshot du site en production ?" | Filtre les données techniques hors des HTML showroom |
| **Mason's Rule** | Zéro scaffolding visible (pas de "Section 02", labels, nuanciers) | Le showroom = vrai site de marque, pas documentation |
| **Placeholder protocol** | `<!-- PLACEHOLDER:X -->` remplacé en post-traitement par Python | Les SVG/images base64 sont trop lourds pour le prompt LLM |
| **Two-pass design** (3A → 3B) | Le récit d'abord, le design ensuite | Force le design à SERVIR le récit |
| **Subagent pattern** | 1 subagent par phase, resumable via agentId pour itération | Isole le contexte, permet l'itération sans relancer |
| **Extraction pré-subagent** | L'orchestrateur pré-extrait :root, concept choisi, catalogue CSS avant de lancer un subagent | Réduit le volume de tokens envoyés au subagent (envoyer le pitch complet de 16K tokens alors qu'on a besoin d'un seul concept serait du gaspillage) |
| **Archive avant régénération** | `_archive-pass-{N}/` (Phase 3B : pitches, penseurs, specimens, font backups) et `_archive-st-{N}/` (Phase 4 : style-tiles, screenshots, DA check) — numérotation séquentielle | Permet de revenir à un concept ou style-tile antérieur sans perte. Corrélé au versionnage des concepts narratifs (v1, v2...). Pour retrouver le concept 2 de la pass 1 : `_archive-pass-1/{brand}-pitch-c2.md` + `_archive-pass-1/{brand}-font-backups.md` |
| **Prompts externalisés** | Les prompts subagents vivent dans `phases/*.md`, lus au moment du lancement (pas chargés en contexte permanent) | Réduit le baseline token de ~57K à ~28K, doublant le nombre d'échanges avant compaction |
| **Boucle d'itération universelle** | Subagent produit → orchestrateur présente résumé → user valide ou feedback → si feedback, resume subagent → boucle | Même mécanique partout, jamais de passage à N+1 sans validation explicite |

---

## Fichiers de référence

| Fichier | Rôle | Lu par |
|---------|------|--------|
| `ref/persona-and-rules.md` | Persona DA + 4 règles comportementales | Tous les subagents |
| `ref/bible-design-strategie.md` | 5 principes design, frameworks (Gestalt, ZAG, Affordance), curseurs, tension | Tous les subagents |
| `ref/master-style-guide.md` | 9+1 piliers (fondations, atomes, systèmes, narration), quality gates | Phases 1, 2, 3B, 4, 6 |
| `ref/brief-alpha-template.md` | 14 points du brief + explications | Phase 1 |
| `ref/output-framework-zone1.md` | Règles Zone 1 (Screenshot Test, Mason's Rule, triptyque, diegetic UI) | Phases 4, D4, 6A, 6B |
| `ref/html-showroom-spec.md` | Spec technique HTML/CSS, :root structure, pools de fonts, catalogue CSS moderne | Phases 3B, 4, 6A, 6B |
| `ref/visual-direction-guide.md` | Principes composition, concept→visuels, usage→prompting, anti-patterns visuels, arbre de décision intégration | Skill `/visual-prompt` |
| `ref/midjourney-prompting-guide.md` | Framework technique MJ — 26 registres, arbre de décision, paramètres par type | Skill `/visual-prompt` |
| `ref/recraft-prompting-guide.md` | Framework technique Recraft V4 — prompting par type, checklist | Skill `/visual-prompt` |
| `ref/recraft-routing-rex.md` | REX routage MJ/Recraft — pourquoi certains registres vont vers Recraft | Skill `/visual-prompt` |
| `ref/image-composition-patterns.md` | 6 patterns CSS d'intégration d'images (split, mask, clip-path, full-bleed, overflow, overlap) | Skill `/visual-prompt`, Phase 4 |
| `ref/extraction-guide.md` | Structure du Brand DNA (pour mode aspiration) | Phase D2 |
| `ref/logo-design-bible.md` | Principes logo, concept, MidJourney, scoring Paul Rand (~800 lignes) | Phase Logo L1 |
| `ref/logo-generation-rex.md` | REX : règles prompting MJ, stratégie d'itération | Phase Logo L1 |
| `ref/logo-vectorization-rex.md` | REX : vtracer, post-processing SVG | Phase Logo L3 |
| `ref/logo-lockup-rex.md` | REX : construction lockups avec tight viewBox | Phase Logo L4 |
| `ref/animation-catalogue.md` | Catalogue d'animations (6 axes : scroll / entrée hero / hero au scroll / reveals sections / micro-interactions / fond) + presets recommandés par profil | Étape 5D (orchestrateur 5D-1 + sous-agent animateur) |
| `ref/animation-implementation-guide.md` | Guide technique de la couche d'animation : setup CDN GSAP + style scopé + init garde-fou, non-régression, mode sûr hero, recettes GSAP/CSS par option, anti-slop, stratégie des 2-3 variantes | Étape 5D (sous-agent `phases/phase-5d-animation.md`) |
| `ref/pipeline-overview.md` | Vue d'ensemble user-facing (ouvert à l'onboarding) | Utilisateur |
| `phases/*.md` | Prompts subagents externalisés (lus à la demande, pas en contexte permanent), dont `phase-5d-animation.md` (Étape 5D) | Phases 1, 2A, 2C, 3A, 3B, 4, 5D, Logo, 6A, 6B, 7, D2, D4 |
| `examples/` | 3 exemples de pitch (niveaux A=1/2/3) + exemples de style-tiles HTML + exemples de batches | Phases 3B, 4, 6A, 6B |
| `scripts/phase4-blacklist-gate.py` | Gate mécanique — scanne le HTML pour 11 patterns CSS datés (hover translateY, animations infinies, glow shadows, séparateurs, etc.) | Phase 4 (étape 4A-ter) |
| `scripts/phase4-finishing-gate.py` | Gate mécanique — vérifie qualité CSS (techniques modernes, finition, curseur) ; `--json-output` | Phase 4 (étape 4A-ter), wrappé par `phase6-batch-gate.py` |
| `scripts/phase6-batch-gate.py` | Gate anti-slop Batch 2/3 (D56) — wrapper mince : strippe SVG/base64, délègue aux 2 gates Phase 4, re-pondère selon un profil « documentation batch », ajoute Specs Lock / Completeness / external-image / Lorem ipsum ; sortie JSON `{deterministic_fails, other_fails, warns}` | Phases 6A, 6B |
| `scripts/phase3b-css-gate.py` | Gate mécanique — bloque les termes CSS dans les pitchs (sensations uniquement) | Phase 3B |
| `lib/puppeteer-screenshots.mjs` | Capture screenshots des style-tiles (full-page 1440px + hero 1440×900) | Phase 4bis |
| `lib/font-palette-specimen.mjs` | Génère un HTML specimen typo + palette, capture screenshot Puppeteer | Phase 3B-bis |

---

## Glossaire

| Terme | Signification |
|-------|---------------|
| **Ventre Mou** | Codes visuels génériques partagés par TOUS les concurrents du secteur — à éviter |
| **Tension de Marque** | 2 attributs contradictoires qui créent la différenciation (ex: "Rigueur × Ferveur") |
| **Curseur A** | Audace Créative — intensité du traitement (1=Prudent / 2=Décalé / 3=Rupture) |
| **Curseur B** | Différenciation — distance aux normes sectorielles (1=Mimétisme / 2=Distinction / 3=ZAG) |
| **ZAG** | Contre-positionnement intentionnel vs tendance du marché |
| **Pass A / Pass B** | Phase narrative (zéro design) puis phase design dérivé du narratif |
| **Artefact Témoin** | Composant UI complexe dans le style-tile qui prouve que le système fonctionne |
| **Voice Block** | Section hero du style-tile — personnalité via mots + typographie |
| **Atmosphere Block** | Section immersive du style-tile — mood, manifeste, ambiance |
| **Zone 1 / Zone 2** | Zone 1 = Showroom HTML (émotionnel, CEO-facing) / Zone 2 = Specs markdown (technique, opérationnel) |
| **Specs Lock** | Obligation d'utiliser le :root identique entre style-tile et batches |
| **Brand DNA** | Tokens design extraits d'un site existant (mode aspiration) |
| **Slug** | Version URL-safe du nom de concept (ex: "Symbiose Vivante" → `symbiose-vivante`), utilisé dans tous les noms de fichiers |

---

## Skills audit complémentaires

En dehors du pipeline principal, deux skills d'audit invocables à la demande permettent d'évaluer un style-tile généré par BIG (ou n'importe quel HTML). Ils sont **philosophiquement distincts** et **complémentaires** — l'un ne remplace pas l'autre.

### `/audit-elite` — Juge RELATIF (comparaison visuelle aux étalons Awards)

- **Persona** : DA senior impitoyable
- **Input** : style-tile HTML + pitch du concept + 2-3 étalons Awards (`etalon-*.png`) dans le session dir
- **Mécanisme** : capture Puppeteer (hero + full page) du style-tile, double analyse (visuelle via screenshots + technique via code CSS), comparaison aux étalons fournis
- **Output** : diagnostic tabulé sur 8 axes (Layout, Intégration image, Profondeur surface, Impact typo, Densité intentionnelle, Technique CSS, Finition, Alignement pitch), score /10, prescriptions prioritaires
- **Utilité** : mesurer l'écart au niveau Awards sur le plan visuel/culturel

### `/audit-slop` — Juge ABSOLU (règles binaires universelles)

- **Persona** : arbitre informé (pas de goût personnel)
- **Input** : style-tile HTML (mode autonome) OU session BIG + numéro de concept (mode intégré, charge automatiquement pitch/brief/curseurs)
- **Mécanisme** : lance 4 agents auditeurs en parallèle + 1 synthétiseur arbitre
- **Les 4 grilles orthogonales** :
  1. **Craft Moderne** — fusion de Impeccable (10 fichiers) + Taste Skill (7 variantes) + GStack (2 SKILL.md) = ~130 règles anti-slop externes
  2. **Vercel Technique** — `command.md` officiel Vercel (~70 règles a11y/perf/typo)
  3. **BIG Pipeline** — blacklist phase-4-styletile + scripts Python de gates + 10 principes Phase 4 + 12 patterns datés Perplexity + 8 leviers gap-elite (~80 règles pipeline-spécifiques)
  4. **Perplexity Temporel** — rapport styles datés vs actuels 2026 (~47 marqueurs de datation)
- **Arbitrage des contradictions** : le synthétiseur tranche les contradictions inter-grilles (ex : Taste dit "H1 trop gros" vs BIG dit "H1 trop petit") en fonction du **contexte projet** (registre, curseur A, pitch)
- **Output** : score pondéré global (30/20/30/20 Craft/Vercel/BIG/Perplex), top-10 violations prioritaires dédupliquées, contradictions arbitrées, matrice de couverture, verdict temporel (DATÉ / CYCLIQUE_RETOUR / ACTUEL / INTEMPOREL / HYBRIDE)
- **Check de fraîcheur opt-in** : à chaque invocation, propose de comparer les caches locaux aux versions distantes des règles externes, produit un rapport delta, mais n'applique jamais les changements auto
- **Utilité** : vérifier la conformité à un corpus de règles objectivables, détecter l'AI slop patterns, évaluer le positionnement temporel

**Les deux skills sont autonomes** — pas intégrés au pipeline BIG, invocables à la demande après Phase 4 (style-tile) ou sur n'importe quel HTML externe.

---

Dernière mise à jour : 2026-05-29 — Ajout Phase 8 Brand Book + Phase 8b Design System dans le pipeline et le schéma. Renommage Phase 7 (était "Documentation & Packaging") en "Documentation Markdown" + Étape Finale Packaging séparée.
