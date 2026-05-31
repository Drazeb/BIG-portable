---
name: test-big
description: Test Runner pour BIG — Lance le pipeline Brand Identity Generator à partir d'une phase spécifique, en réutilisant les artifacts d'une session précédente. Invoke with /test-big.
user_invocable: true
---

# Test Runner BIG — Orchestrateur

Tu es l'orchestrateur du test runner pour le pipeline **Brand Identity Generator (BIG)**. Tu permets de reprendre l'exécution du pipeline à une phase précise, en pointant vers un dossier contenant les artifacts d'une session précédente.

**Pourquoi ce skill existe :** Le pipeline BIG complet prend ~1h+. Pour itérer sur une phase spécifique (ex: Phase 4 Style-Tiles), il faut pouvoir reprendre à cette phase sans refaire les précédentes.

**Principe :** Ce skill ne contient aucune logique de génération. Il prépare l'environnement puis exécute les instructions de `brand-identity/SKILL.md` à la phase demandée.

---

## ONBOARDING — PREMIÈRE ACTION OBLIGATOIRE

**RÈGLE ABSOLUE** : À chaque invocation de `/test-big`, tu DOIS :
1. D'abord faire un check git update silencieux (étape 0a ci-dessous)
2. Puis afficher le message d'onboarding (étape 0b) — avec ou sans alerte selon le résultat

Ne pas résumer, ne pas reformuler. Copier tel quel.

### Étape 0a — Check git update (Bash silencieux)

Lancer dans Bash, capturer le résultat dans une variable `{git_behind}` :

```bash
GIT_BEHIND=""
if [ -d ".git" ] && git remote get-url origin >/dev/null 2>&1; then
  git fetch origin main --quiet 2>/dev/null || true
  LOCAL=$(git rev-parse HEAD 2>/dev/null || echo "")
  REMOTE=$(git rev-parse origin/main 2>/dev/null || echo "")
  if [ -n "$LOCAL" ] && [ -n "$REMOTE" ] && [ "$LOCAL" != "$REMOTE" ]; then
    GIT_BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "?")
  fi
fi
echo "GIT_BEHIND=$GIT_BEHIND"
```

Stocker la valeur dans `{git_behind}` (vide si à jour, sinon nombre de commits de retard).

### Étape 0b — Affichage de l'onboarding

Afficher EXACTEMENT le logo ci-dessous (copier tel quel) :

---

```
                       ╔════════════════════════════════════╗
                       ║  ██████╗ ██╗ ██████╗               ║
   __          __      ║  ██╔══██╗██║██╔════╝  Brand        ║
  / /____ ___ / /_     ║  ██████╔╝██║██║  ███╗ Identity     ║
 / __/ -_|_-</ __/     ║  ██╔══██╗██║██║   ██║ Generator    ║
 \__/\__/___/\__/      ║  ██████╔╝██║╚██████╔╝              ║
                       ║  ╚═════╝ ╚═╝ ╚═════╝               ║
                       ╚════════════════════════════════════╝
```

**SI `{git_behind}` n'est PAS vide (mise à jour disponible)**, afficher EN PLUS, juste après le logo et avant le message d'accueil :

```
▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰
   [!] [!]  {git_behind} MISES À JOUR DISPO  [!] [!]
▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰

{git_behind} commits sur GitHub.
Lance `./update.sh` ou dis-moi "update" et je le fais.
```

(Si `{git_behind}` est vide → ne rien afficher, passer directement au message d'accueil.)

Bienvenue dans le Test Runner BIG. Je vais te demander à quelle phase tu veux reprendre, sur quel dossier de session, et préparer l'environnement pour relancer le pipeline.

### Si l'utilisateur demande une mise à jour

Si l'utilisateur tape **"update"**, **"mets à jour"**, **"lance update"**, **"fais l'update"**, **"git pull"**, ou tout équivalent (au lieu de choisir une phase), exécuter le script de mise à jour AVANT de continuer :

```bash
./update.sh 2>&1
```

Présenter le récap de sortie à l'utilisateur. Puis annoncer :

> "Mise à jour faite. Relance `/test-big` pour repartir sur la version à jour, ou choisis ta phase de départ pour démarrer avec la version actuelle."

---

## ÉTAPE 1 — Collecte des paramètres

Demander à l'utilisateur les 4 paramètres suivants (un par un ou groupés si l'utilisateur les fournit d'emblée) :

### 1.1 Phase de départ

**IMPORTANT : Ne PAS utiliser AskUserQuestion pour cette étape.** La liste a 12 entrées, ce qui dépasse la limite de l'outil. Afficher la liste ci-dessous en texte brut dans ta réponse, et l'utilisateur répondra avec le code de la phase.

Afficher exactement ce texte :

```
À quelle phase voulez-vous reprendre ?

  1    — Analyse du brief (brief analysé, score de confiance)
  2A   — Scoping stratégique (tension de marque, ventre mou sectoriel, diagnostic température)
  2B   — Choix des curseurs A×B (niveau d'audace, niveau de rupture)
  2C   — Extraction des territoires (15-20 mots-clés → 4-5 clusters)
  2D   — Pondération des territoires (Principal / Secondaire / Accent)
  3A1  — Concepts narratifs (Mode Sélectif : choix d'un registre à l'Étape 2E, pool → 10 candidats → 0 à 3 retenus)
  3A2  — Concepts supplémentaires (batch additionnel — autre ou même registre, accumulation)
  3B-1 — Routeur chromatique v2 (grille territoire×aptitude : validées/exclues, enforce filtres durs + gate v2, planche grille)
  3B-2 — Palettes (buckets d'aptitude ; 3 palettes A/B/C par concept, divergence dégressive mécanique, 3 gates, planche comparative, choix utilisateur, mini-check aversions couleur)
  3B-3 — Choix des polices (penseur typo + designer typo : longlists, descriptions, top 3 display+body, planches duos, font-recap)
  3B-4 — Spécimens (typo + palette choisie, spécimen visuel typo+couleurs)
  3B-7a-pre — Routeur de styles (tag binaire SECTORIEL/NON-SECTORIEL des 34 styles selon le ventre mou — exécuté 1 fois par projet, source de vérité pour Gate 5)
  3B-7a — Stylistes A/B/C (divergence séquentielle 3×3 fiches : matching libre, divergence vs A, registre ≠ A et B — enchaîne automatiquement A→B→C)
  3B-7b — Spécimens stylisés (9 sub-agents parallèles : 3 concepts × 3 variantes A/B/C)
  3B-7-checkpoint — Choix utilisateur entre les 3 variantes de style par concept (12 onglets : 9 spécimens enrichis d'un bandeau sticky + 3 matrices de scan exhaustif 34 styles × 3 variantes ; choix "C1→A, C2→C, C3→B" avec mini-check aversions registre) + choix d'UN concept à porter en avant pour la phase visuelle (séquentiel — fichier .concept-pour-3B-7c)
  3B-7c — Direction visuelle ancrée Perplexity (séquence 10 sous-étapes pour UN concept : approche sujet + type visuel + prompt Perplexity + recherche refs Cosmos/Behance/ArtStation + image finale MJ/NB2 + description fine spec). Branche A (Mockup ou CSS/SVG procédural) bypasse Perplexity et utilise le subagent legacy phase-3b-penseur-visuel.md.
  3B-7d — Pitch design complet (assemblage final avec la fiche canonique : typo + palette + style + visuels + composition + interactions)
  3B-7e — Génération de variantes visuelles supplémentaires (skill /visual-prompt mode variantes — 2e opportunité d'enrichir la librairie visual-final/ après finalisation des pitches)
  4    — Style-tiles HTML (hero + zone médiane + atmosphere, 3 pages, SANS artefact)
  4-val — Validation hero+atmosphere, puis lancement subagents artefact
  4-art — Artefacts dédiés (3 subagents parallèles, insertion dans les style-tiles)
  4B   — Audit visuel DA (comparaison screenshots vs pitch)
  5    — Itération + choix du concept final
  5D   — Animation du style-tile retenu (optionnelle ; couche GSAP/CSS additive, 2-3 variantes de dosage)
  L    — Logo (concept + génération MJ + vectorisation)
  6A   — Système de signes (icônes, patterns, éléments graphiques ; + bande de couverture si une librairie visual-final/ existe)
  6B   — Narration étendue (pages complémentaires ; chapitre 08 affiche les visuels finaux réels si visual-final/ existe)
  7    — Documentation finale (design specs)
  8A   — Brand Book éditorial (intro Identity Card + 8 sections + closing, optionnel — invoque skill /brand-book + sous-skill SPG /generate-mini-deck) — exécuté d'un bloc, non-reprenable au milieu
  8B   — Design System HTML technique (sobre type Carbon/Atlassian — sidebar nav, foundations exhaustives, tokens prêts à copier — invoque skill /design-system autonome, ~80K tokens) — exécuté d'un bloc, non-reprenable au milieu
  9    — Packaging final (dossier {brand}-identity-{slug}/ avec fichiers renommés, prêt à livrer — inclut le sous-dossier brand-book/ si Phase 8A exécutée)
```

Attendre la réponse de l'utilisateur, puis stocker dans `{start_phase}`.

### 1.2 Dossier source

Demander le chemin vers le dossier contenant les artifacts des phases précédentes.

Indice à donner à l'utilisateur : les sessions BIG sont dans `.claude/skills/brand-identity/outputs/`. On peut aussi pointer vers n'importe quel dossier contenant les fichiers.

Stocker le chemin absolu résolu dans `{source_dir}`.

### 1.3 Nom de la brand

**Détection automatique (tenter dans l'ordre) :**

1. Lire `{source_dir}/.session-id` → le brand est le premier segment avant `|`
2. Lister les fichiers `{source_dir}/*-brief-analysis.md`, `{source_dir}/*-scoping.md`, `{source_dir}/*-pitch.md` → extraire le préfixe commun avant le premier `-brief-analysis`, `-scoping`, ou `-pitch`
3. Si aucune détection ne fonctionne → demander à l'utilisateur

Dans tous les cas, **confirmer** avec l'utilisateur : "Brand détectée : `{brand}`. C'est correct ?"

Stocker dans `{brand}`.

### 1.4 Label de session test

Proposer automatiquement un label basé sur la date :

```bash
date +"%Y%m%d-%H%M"
```

Format proposé : `test-{YYYYMMDD-HHmm}` (ex: `test-20260222-1430`).

L'utilisateur peut modifier ou accepter tel quel.

Stocker dans `{session_label}`.

---

## ÉTAPE 2 — Validation du dossier source

Scanner `{source_dir}` et vérifier que les fichiers requis pour la phase demandée existent.

### Table des prérequis par phase

| `{start_phase}` | Fichiers requis dans `{source_dir}` |
|---|---|
| `1` | Aucun (on part de zéro) |
| `2A` | `{brand}-brief-analysis.md` |
| `2B` | + `{brand}-scoping.md` (avec section Tension) |
| `2C` | + `{brand}-scoping.md` (avec curseurs A×B) |
| `2D` | + `{brand}-territoires-v*.md` |
| `3A1` | + `{brand}-scoping.md` (avec section Mix de Territoires) |
| `3A2` | + `{brand}-scoping.md` (avec section Mix de Territoires) + `{brand}-concepts-narratifs*.md` (au moins 1 batch existant) |

| `3B-1` | + `{brand}-concepts-narratifs.md` + `{brand}-validated-temperature.md` (optionnel — guidance température depuis Phase 2A ; si absent, le routeur tourne sans). Le routeur est isolé des autres fichiers. |
| `3B-2` | + `{brand}-concepts-narratifs.md` + `{brand}-chromatic-gamuts.md` (⚠ doit être au format grille territoire×aptitude du routeur v2 — l'orchestrateur en dérive les buckets via `project_buckets.py` ; une vieille session 3-catégories sans aptitude → relancer `3B-1`) + `{brand}-ventre-mou-chromatique.md` si présent. Le subagent palette consomme les buckets + concept ; les fonts ne sont PAS un input ; les aversions sont confrontées a posteriori par mini-check orchestrateur lisant brief-analysis.md) |
| `3B-3` | + `{brand}-concepts-narratifs.md` + `{brand}-chromatic-gamuts.md` + `{brand}-palette-c*.md` (canoniques) + variantes `{brand}-palette-c*-{a,b,c}.md` (penseurs typo + designer typo arrivent APRÈS la palette ; ils consomment chromatic-gamuts, pas la palette) |
| `3B-4` | + `{brand}-palette-c*.md` + `{brand}-font-backups.md` (spécimens typo + palette choisie) |
| `3B-7a-pre` | + `{brand}-scoping.md` (le routeur extrait le ventre mou complet ; les 34 styles sont extraits dynamiquement par l'orchestrateur depuis `ref/styles-bibliotheque.md` — pas d'autre input projet) |
| `3B-7a` | + `{brand}-palette-c*.md` + `{brand}-font-backups.md` + `{brand}-specimen-c*.html` + `{brand}-style-sectoriel-tags.md` (sortie 3B-7a-pre — sans elle, Gate 5 ne peut pas valider la règle B inter-variantes ; si absent, lancer 3B-7a-pre d'abord). Les 3 sous-vagues A→B→C s'enchaînent automatiquement, pas de reprise possible à mi-séquence. PAS de visuals — le styliste ne consomme pas les visuels. |
| `3B-7b` | + 9 fichiers `{brand}-style-choice-c{1,2,3}-{a,b,c}.md` (le specimen consomme la fiche de style de SA variante) |
| `3B-7-checkpoint` | + 9 fichiers `{brand}-style-specimen-c{1,2,3}-{a,b,c}.html` (l'orchestrateur compose 3 pages d'index pointant vers ces spécimens) |
| `3B-7c` | + `{brand}-style-choice-c*.md` (canoniques, post-checkpoint) + `{brand}-palette-c*.md` + `{brand}-font-backups.md` + `{brand}-specimen-c*.html` + `.concept-pour-3B-7c` (numéro du concept choisi pour la phase visuelle, produit à l'Étape 5quater du checkpoint). Depuis le refactor 5 mai 2026, séquence séquentielle pour UN concept. Branche A (Mockup ou CSS/SVG) utilise le subagent legacy ; Branche B (Photo/Illu/3D/Pattern) utilise les nouveaux subagents `phase-3b-7c-perplexity-prompt-generator.md` + `phase-3b-7c-image-final-describer.md`. |
| `3B-7d` | + `{brand}-style-choice-c*.md` (canoniques) + `{brand}-palette-c*.md` + `{brand}-font-backups.md` + **soit** `{brand}-visual-pivot-c*.md` (Branche B, format spec — image finale dans `visual-final/`) **soit** `{brand}-visual-direction-c*.md` (Branche A ou pré-refactor 5 mai 2026, format legacy). Le pitch designer lit en cascade visual-pivot → visual-direction → dérivation libre. |
| `3B-7e` | (legacy — équivalent du skill `/visual-brief` ; depuis le refactor 5 mai 2026, la génération MJ/NB2 est intégrée dans 3B-7c.7 via skill externe `/visual-prompt` ou `/visual-brief`. Démarrage 3B-7e direct n'est utile que pour les pipelines pré-refactor) |
| `3B-7` | (alias rétrocompatible) → mappe sur `3B-7d` (pitch complet) |
| `4` | + `{brand}-pitch.md` (ou `{brand}-pitch-c*.md` individuels) + visuels MJ/Recraft (optionnels, produits en 3B-7e) |
| `4-val` | + au moins 3 fichiers `{brand}-style-tile-concept-*.html` (hero+zone médiane, SANS artefact complet) + `{brand}-pitch.md` |
| `4-art` | + au moins 3 fichiers `{brand}-style-tile-concept-*.html` (validés par l'utilisateur) + `{brand}-pitch.md` |
| `4B` | + au moins 1 fichier `{brand}-style-tile-concept-*.html` (complet, avec artefact) + `{brand}-pitch.md` |
| `5` | + au moins 1 fichier `{brand}-style-tile-concept-*.html` |
| `5D` | + le style-tile retenu `{brand}-style-tile-concept-{chosen_concept_number}.html` (complet) + (utile) `{brand}-style-choice-c{chosen_concept_number}.md` ou `{brand}-pitch.md` (pour le registre). Les refs `ref/animation-catalogue.md` et `ref/animation-implementation-guide.md` sont dans le repo (pas dans `{source_dir}`), pas besoin de les copier. |
| `L` | + au moins 1 fichier `{brand}-style-tile-concept-*.html` (le choisi) |
| `6A` | + `{brand}-style-tile-concept-*.html` (le choisi) + `{brand}-style-choice-c*.md` (fiche styliste 3B-7a) + `{brand}-concepts-narratifs.md` (concept décontaminé) + `{brand}-territoires-v*.md` + `{brand}-style-sectoriel-tags.md` (ventre mou) + `{brand}-pitch-c*.md` (pour Étape 6A-0 router icônes, depuis D59) + **(optionnel)** le dossier `visual-final/` (alimente Batch 3 ch.08/10) |
| `6B` | + au moins 1 fichier `{brand}-batch2-*.html` (+ `visual-final/` optionnel, idem 6A) |
| `7` | + au moins 1 fichier `{brand}-batch3-*.html` |
| `8A` | + `{brand}-design-specs*.md` (de la Phase 7) — pack BIG complet en place dans `{session_dir}/` (les 5 fichiers + `visual-final/`) ; Phase 8A invoque le skill /brand-book qui lit ces fichiers et écrit dans `{session_dir}/brand-book/` |
| `8B` | + `{brand}-design-specs*.md` (de la Phase 7) — pack BIG complet en place dans `{session_dir}/` (les 5 fichiers + `visual-final/`) ; `{session_dir}/brand-book/` optionnel (Phase 8A recommandée mais pas obligatoire) ; Phase 8B invoque le skill /design-system qui lit ces fichiers et écrit dans `{session_dir}/design-system/` |
| `9` | `8A` done OU Phase 8A skippée + `{brand}-design-specs*.md` (de la Phase 7) — toutes les briques pré-existantes (style-tile-concept-*, batch2-*, batch3-*, design-specs-*, logo-*) sont copiées et renommées dans `{brand}-identity-{slug}/`. Si Phase 8A exécutée, le sous-dossier `brand-book/` est aussi copié. |

**Chaque phase inclut les prérequis de toutes les phases précédentes** (cumulatif).

**Algorithme :**

```
prerequisites = construire la liste cumulative des fichiers requis pour {start_phase}
missing = []
pour chaque fichier requis :
    si le fichier n'existe pas dans {source_dir} :
        ajouter à missing
si missing n'est pas vide :
    afficher : "⚠ Fichiers manquants pour la phase {start_phase} :"
    lister les fichiers manquants
    demander : "Voulez-vous continuer malgré tout ? (oui/non)"
    si non → arrêter
sinon :
    afficher : "✓ Tous les fichiers requis sont présents."
```

---

## ÉTAPE 3 — Extraction des variables

Extraire les variables nécessaires à l'exécution de la phase demandée. Quand l'extraction automatique échoue, **demander à l'utilisateur**.

### Table d'extraction

| Variable | Source | Méthode d'extraction | Phases qui en ont besoin |
|---|---|---|---|
| `{cursor_a}` | `{brand}-scoping.md` | Chercher "Curseur A" ou "cursor_a" ou le tableau des curseurs, extraire la valeur (1, 2, ou 3) | ≥ 2D |
| `{cursor_b}` | `{brand}-scoping.md` | Chercher "Curseur B" ou "cursor_b", extraire la valeur (1, 2, ou 3) | ≥ 2D |
| `{territory_mix}` | `{brand}-scoping.md` | Chercher la section "## Mix de Territoires", extraire le bloc complet (Principal + Secondaire + Accent) | ≥ 3A1 |
| `{example_level}` | Dérivé de `{cursor_a}` | Si `cursor_a` = 3 → `"rupture"`, sinon → `"standard"` | ≥ 4 |
| `{chosen_concept_number}` | Demander à l'utilisateur | Numéro du concept choisi (1, 2, ou 3) | ≥ 6A |
| `{chosen_concept_name}` | `{brand}-pitch.md` ou demander | Lire les noms des 3 concepts dans le pitch, proposer celui correspondant au numéro, confirmer | ≥ 6A |
| `{chosen_concept_slug}` | Dérivé de `{chosen_concept_name}` | Slugify : minuscules, espaces → tirets, suppression accents et caractères spéciaux | ≥ 6A |

**Procédure :**

1. Lire les fichiers source nécessaires
2. Pour chaque variable requise par `{start_phase}` et les phases suivantes :
   - Tenter l'extraction automatique
   - Si échec → demander à l'utilisateur
3. Afficher un récapitulatif de toutes les variables extraites et demander validation

---

## ÉTAPE 4 — Création de l'environnement de test

### 4.1 Créer le dossier de test

```bash
# Définir les chemins
BIG_SKILL_DIR="{absolute_path_to}/.claude/skills/brand-identity"
TEST_DIR="${BIG_SKILL_DIR}/outputs/test-{brand}-{session_label}"

# Vérifier que le dossier n'existe pas déjà
test -d "${TEST_DIR}" && echo "ERREUR: ce dossier existe déjà" || mkdir -p "${TEST_DIR}"
```

Stocker `{test_dir}` = chemin absolu du dossier créé.
Stocker `{session_dir}` = `test-{brand}-{session_label}` (nom du dossier uniquement).

### 4.2 Créer le .session-id

```bash
echo "{brand}|{session_label}|$(date +%s)" > "{test_dir}/.session-id"
```

### 4.3 Copier les fichiers source (FILTRÉ par phase)

**Principe** : ne copier que les fichiers qui sont des OUTPUTS des phases **strictement antérieures** à `{start_phase}`. Un test qui redémarre à la phase X doit avoir un environnement vierge pour X, avec uniquement les prérequis.

**Table des outputs par phase :**

| Phase | Patterns de fichiers produits |
|-------|-------------------------------|
| `1` | `{brand}-brief-analysis.md` (contient section "## Aversions client" si Point 15 non-vide, sinon "Aucune aversion déclarée") |
| `2A` | `{brand}-scoping.md` (section Tension & Ventre Mou + Diagnostic Température), `{brand}-validated-temperature.md` (mini-fichier : verdict chaud/froid/neutre + justification — consommé par le routeur chromatique 3B-1) |
| `2B` | `{brand}-scoping.md` (ajout curseurs A×B) |
| `2C` | `{brand}-scoping-filtered.md` (version filtrée pour le clustering), `{brand}-territoires-v*.md`, `{brand}-qualites-v*.md` (extraction mots-clés en amont du clustering) |
| `2D` | `{brand}-scoping.md` (ajout section Mix de Territoires) |
| `3A1` | `{brand}-context-clean.md` (décontamination Étape 2D-bis), `{brand}-concepts-narratifs-v*.md` (1 à 3 concepts par batch retenu), `{brand}-concepts-selectif-recap-v*.md` (récap des 10 candidats par registre), dossier intermédiaire `.tmp-selectif-v*/` (pool runs + définitions + évaluations — fichiers de travail, EXCLUS du packaging). Un batch à 0 retenu ne produit aucun fichier `concepts-narratifs-v*`. |
| `3A2` | (aucun nouveau pattern — batch supplémentaire ajoute des v2, v3… au pattern `{brand}-concepts-narratifs-v*.md` de 3A1) |
| `3B-1` | `{brand}-chromatic-gamuts.md` (grille territoire×aptitude), `{brand}-ventre-mou-chromatique.md` (directive sectorielle générée, si secteur), `{brand}-grid-visual.html` (planche grille) |
| `3B-2` | `{brand}-buckets.md` + `{brand}-vm-palette-directive.md` (intermédiaires dérivés), `{brand}-palette-c{1,2,3}-{a,b,c}.md` (9 variantes A/B/C — divergence séquentielle dégressive), `{brand}-palette-c{1,2,3}.md` (3 canoniques copiés après choix user), `{brand}-palette-comparison.html` (planche mockups 3×3) |
| `3B-3` | `{brand}-penseur-c{1,2,3}.md` (longlists display 12-15 fonts), `{brand}-penseur-body-c{1,2,3}.md` (longlists body 10 fonts), `{brand}-descriptions-c{1,2,3}.md` (descriptions sans noms), `{brand}-font-backups.md` (top 3 display+body avec backups), `{brand}-font-recap-all.html` (planche unifiée 3 concepts × 6 fonts), `font-pool-duo-display-c{1,2,3}-*.png` (planches duos display), `font-pool-duo-body-c{1,2,3}-*.png` (planches duos body), `font-pool-font-selection-c{1,2,3}.png` (planche récap par concept) |
| `3B-4` | `{brand}-specimen-c{1,2,3}.html`, `{brand}-specimen-c{1,2,3}.png` |
| `3B-7a-pre` | `{brand}-style-sectoriel-tags.md` (tableau 34 styles × tag binaire SECTORIEL/NON-SECTORIEL + justification 1 ligne — source de vérité pour Gate 5 INTER-variantes) |
| `3B-7a` | 9 fichiers `{brand}-style-choice-c{1,2,3}-{a,b,c}.md` (3 sous-vagues séquentielles A→B→C : matching libre, divergence vs A, registre ≠ A et B — enchaînement automatique) |
| `3B-7b` | 9 fichiers `{brand}-style-specimen-c{1,2,3}-{a,b,c}.html` (1 spécimen par variante). |
| `3B-7-checkpoint` | Au checkpoint, l'orchestrateur (a) injecte un bandeau informatif (concept + variante + style + palette + fonts) en sticky en haut de chaque spécimen, (b) compose 3 fichiers `{brand}-style-scan-matrix-c{1,2,3}.html` (matrice 34 styles × 3 variantes A/B/C avec COMPATIBLE/INCOMPATIBLE + raison au survol + encadré orange sur le style dominant retenu), (c) ouvre les 12 fichiers dans 12 onglets séparés (9 spécimens + 3 matrices). Outputs après choix utilisateur : `{brand}-style-choice-c{1,2,3}.md` (canoniques copiés depuis la variante choisie) **+ `.concept-pour-3B-7c`** (fichier de marquage simple contenant le numéro 1/2/3 du concept retenu pour la phase visuelle — ajouté 5 mai 2026). |
| `3B-7c` | **Branche A** (Mockup ou Fond CSS/SVG procédural) : `{brand}-visual-direction-c{N}.md` (1 fichier canonique, format legacy avec prescriptions techniques + DNA visuel transmissible). **Branche B** (Photo/Illu/3D/Pattern, depuis le refactor 5 mai 2026) : `{brand}-perplexity-prompt-c{N}.md` (prompt prêt à coller) + `{brand}-perplexity-response-c{N}.md` (réponse Perplexity — déposée par l'utilisateur) + `visual-pivot-choice.md` (choix utilisateur de l'idée pivot) + `visual-refs/ref-*.{ext}` (5-8 images de référence — déposées par l'utilisateur) + `visual-final/{brand}-visual-final.{ext}` (image finale produite par skill externe MJ/NB2 — déposée par l'utilisateur) + `{brand}-visual-pivot-c{N}.md` (description fine au format spec `ref/visual-final-description-spec.md`, 10 sections A-J — version provisoire produite à 3B-7c.4 puis version finale produite à 3B-7c.9). Pas de variantes a/b/c — UN seul concept traité (séquentiel). Si reprise mid-pipeline, le subagent legacy `phase-3b-penseur-visuel.md` reste disponible pour les pipelines pré-refactor 5 mai 2026. |
| `3B-7d` | `{brand}-pitch-c{1,2,3}.md` (per-concept), `{brand}-pitch.md` (assemblé) — = ancien `3B-7c` |
| `3B-7e` | Variantes ajoutées à `visual-final/{brand}-c{N}-{paletteID}-{type}[-{variante}].{ext}` (atmosphere/closeup/macro/pov dérivés du hero via /visual-prompt mode variantes — APRÈS le pitch). Format legacy `{brand}-visual-brief.md` accepté en input pour les sessions pré-refactor mai 2026. |
| `4` | `{brand}-style-tile-concept-{1,2,3}.html` (3 fichiers par concept, hero + zone médiane + atmosphere, AVEC placeholder artefact) |
| `4-val` | (aucun nouveau fichier — validation conversationnelle ; backups `.bak-iter0-pre-correction` créés si itération) |
| `4-art` | (aucun nouveau fichier — modifie in-place les `{brand}-style-tile-concept-{1,2,3}.html` en injectant l'artefact à la position du placeholder) |
| `4B` | `{brand}-da-check.md`, `screenshot-c*-*.png` |
| `5` | (aucun nouveau fichier — variables d'état uniquement : `{chosen_concept_number}`, `{chosen_concept_slug}`) |
| `5D` | `{brand}-animation-menu.md` (catalogue + preset recommandé, ouvert en MarkView), `{brand}-style-tile-concept-{n}-animated-v{1,2,3}.html` (variantes de dosage), puis après choix : `{brand}-style-tile-concept-{n}-animated.html` (variante retenue, promue) + `{brand}-animation-spec.md` (preset retenu + deps CDN) + dossier `_archive-anim-{round}/` (les variantes non retenues). Le style-tile statique `{brand}-style-tile-concept-{n}.html` reste **inchangé**. Si l'utilisateur dit Non à l'Étape 5D-0 → aucun fichier. |
| `L` | `{brand}-logo-concept-{slug}.md` (concept + 3 prompts MJ), `{brand}-logo-{slug}-vector-{1,2,3}.svg` (post-vectorisation), `{brand}-logo-{slug}.png` |
| `6A` | `{brand}-icon-family-choice.md` (output Étape 6A-0 router famille d'icônes, D59) + `{brand}-batch2-{slug}.html` (Étape 6A-1) |
| `6B` | `{brand}-batch3-{slug}.html` |
| `7` | `{brand}-design-specs-{slug}.md` |
| `8A` | Sous-dossier `{session_dir}/brand-book/` contenant : `{brand}-brand-book.html` (livrable principal) + `visual-final/` (copié) + `pitch-deck-mini/slide-{01..06}-*.png` (6 PNG retina 2560×1440) + `{brand}-linkedin-mockup.{html,png}` (paysage 1000×563 retina) + `{brand}-x-mockup.{html,png}` (carré 1000×1000 retina) + `{brand}-landing-fullpage.png` (capture style-tile) |
| `8B` | Sous-dossier `{session_dir}/design-system/` contenant : `{brand}-design-system.html` (livrable principal, 11 sections : Color, Typography, Spacing, Iconography, Logo, Data viz, Photography, Composition, Illustration, Motion, Tokens) + `{brand}-design-system-inventory.json` (~200 items attendus vs présents) + `{brand}-design-system-audit-sources.json` (mapping items source) + `{brand}-design-system-audit-report.json` (rapport script Python) + sous-dossier `visual-final/` (copié) |
| `9` | Dossier `{brand}-identity-{slug}/` contenant les fichiers renommés : `{brand}-style-tile.html`, `{brand}-batch2.html`, `{brand}-batch3.html`, `{brand}-design-specs.md`, assets logo (SVG + PNG), `{brand}-pitch.md` ou `{brand}-extracted-dna.md` selon mode, **+ sous-dossier `brand-book/`** copié depuis `{session_dir}/brand-book/` si Phase 8A a été exécutée |

**Note `visual-final/`** : ce dossier est créé en 3B-7c (image-pivot du style-tile) mais peut aussi recevoir, plus tard et hors pipeline (skill `/visual-prompt`), une **librairie de visuels finaux dérivés** (`{brand}-c{N}-{paletteID}-{type}[-{variante}].{ext}`). Quand `{start_phase}` ≥ `3B-7d`, la copie filtrée doit reprendre **le dossier `visual-final/` complet** depuis le source (pas seulement `{brand}-visual-final.{ext}`) — il est consommé par Phase 4 (ancrage visuel), Batch 2 (cover band) et Batch 3 (ch08/ch10).

**Algorithme :**

```
phases_ordonnées = [1, 2A, 2B, 2C, 2D, 3A1, 3A2, 3B-1, 3B-2, 3B-3, 3B-4, 3B-7a-pre, 3B-7a, 3B-7b, 3B-7-checkpoint, 3B-7c, 3B-7d, 3B-7e, 4, 4-val, 4-art, 4B, 5, 5D, L, 6A, 6B, 7, 8A, 8B, 9]

fichiers_a_copier = []
pour chaque phase P dans phases_ordonnées :
    si P == {start_phase} : STOP
    fichiers_a_copier += patterns de la table ci-dessus pour P

# Copier uniquement ces fichiers
pour chaque pattern dans fichiers_a_copier :
    cp "{source_dir}/"<pattern> "{test_dir}/"
```

**Exemples :**
- Démarrage **2A** → copier brief-analysis (contient les aversions client si Point 15 a été rempli)
- Démarrage **3A1** → copier brief-analysis + scoping + validated-temperature + scoping-filtered + territoires + qualites-v*
- Démarrage **3A2** → idem 3A1 + concepts-narratifs-v* + context-clean (batches déjà accumulés + contexte décontaminé)
- Démarrage **3B-1** → idem 3A2 + validated-temperature (si présent — guidance optionnelle pour le routeur)
- Démarrage **3B-2** (palettes) → idem 3B-1 + chromatic-gamuts (grille×aptitude) + ventre-mou-chromatique + grid-visual (output de 3B-1). ⚠ requiert le format v2 (aptitude) — vieille session 3-catégories → relancer 3B-1
- Démarrage **3B-3** (typo) → idem 3B-2 + palette-c* canoniques + 9 variantes palette-c*-{a,b,c} + palette-comparison
- Démarrage **3B-4** (spécimens) → idem 3B-3 + tous les outputs typo (penseur-c*, penseur-body-c*, descriptions-c*, font-backups, font-recap-all, planches PNG)
- Démarrage **3B-7a-pre** (routeur de styles) → idem 3B-4 (le routeur n'a besoin que du scoping pour le ventre mou ; les fichiers en amont sont copiés par cohérence pour permettre l'enchaînement automatique vers 3B-7a)
- Démarrage **3B-7a** (stylistes) → idem 3B-7a-pre + `{brand}-style-sectoriel-tags.md` (sortie du routeur). Si le fichier n'existe pas dans le source, lancer 3B-7a-pre d'abord.
- Démarrage **3B-7c** (direction visuelle ancrée Perplexity) → idem 3B-4 + specimen-c* + style-choice canoniques (post-checkpoint) + `.concept-pour-3B-7c` (numéro du concept retenu pour la phase visuelle, requis depuis le refactor 5 mai 2026)
- Démarrage **3B-7d** (pitch) → idem 3B-7c + **soit** `{brand}-visual-pivot-c{N}.md` + `visual-final/{brand}-visual-final.{ext}` (Branche B — refactor 5 mai 2026) **soit** `{brand}-visual-direction-c*.md` (Branche A ou pré-refactor — format legacy)
- Démarrage **3B-7e** (legacy — génération visuels MJ/Recraft via skill séparé `/visual-brief`) → idem 3B-7d + pitch. Note : depuis le refactor 5 mai 2026, la génération MJ/NB2 est intégrée à 3B-7c.7. Démarrage 3B-7e direct n'est utile que pour les pipelines pré-refactor.
- Démarrage **4** → copier tout jusqu'à 3B-7e inclus (brief-analysis, scoping, concepts-narratifs*, palette canoniques + variantes, fonts, style-choice canoniques, visual-pivot OU visual-direction selon branche, image finale `visual-final/`, pitch, visuels MJ/Recraft si générés)
- Démarrage **5D** (animation du style-tile) → tout jusqu'à 5 inclus, dont le style-tile retenu `{brand}-style-tile-concept-{n}.html` (complet) + `{brand}-style-choice-c*.md` / `{brand}-pitch.md`. Pas besoin de copier les refs `ref/animation-*.md` (elles sont dans le repo). Demander à l'utilisateur le numéro du concept retenu si non déductible.
- Démarrage **6A** → tout jusqu'à 5/5D/L inclus, dont le style-tile choisi (et sa version `-animated.html` si 5D a été fait) et le dossier `visual-final/` complet s'il existe (cover band Batch 2 + ch08/ch10 Batch 3)
- Démarrage **6B** → tout jusqu'à 6A inclus (sauf batch3 et zone 2 ; le dossier `visual-final/` est repris s'il existe)
- Démarrage **8** → tout jusqu'à 7 inclus (toutes les briques pré-existantes seront copiées-renommées dans `{brand}-identity-{slug}/`)

**Important** : copie, pas lien symbolique. Les fichiers copiés dans le dossier de test sont indépendants des originaux.

### 4.4 Écrire le fichier .test-context.md

Créer `{test_dir}/.test-context.md` avec le contenu suivant :

```markdown
# Test Context

- **Date** : {date ISO}
- **Source** : {source_dir}
- **Phase de départ** : {start_phase}
- **Brand** : {brand}
- **Session label** : {session_label}
- **Session dir** : {session_dir}

> ⚠️ **Mode test — pipeline anti-slop partiellement actif.** Une session test-big
> qui démarre à une phase autre que `1` exécute UNIQUEMENT les phases ≥ `{start_phase}`.
> Les contrôles anti-slop des phases précédemment skippées (gates Phase 4 4A-loop,
> Critiques, gates Phase 3B) ne tournent PAS sur cette session. Les outputs produits
> à partir de `{start_phase}` peuvent contenir des patterns que la phase amont aurait
> détectés/corrigés en pipeline complet. **Ne pas considérer ces outputs comme validés
> qualité production** — ils servent à itérer rapidement sur la phase testée.

## Variables extraites

| Variable | Valeur |
|---|---|
| cursor_a | {cursor_a} |
| cursor_b | {cursor_b} |
| territory_mix | {territory_mix} |
| example_level | {example_level} |
| chosen_concept_number | {chosen_concept_number} |
| chosen_concept_name | {chosen_concept_name} |
| chosen_concept_slug | {chosen_concept_slug} |

(Seules les variables pertinentes pour la phase de départ et suivantes sont renseignées.)
```

### 4.5 Confirmation

Afficher un résumé à l'utilisateur :

```
Environnement de test prêt :
  Dossier : {test_dir}
  Session : {session_dir}
  Phase de départ : {start_phase}
  Fichiers copiés : {N} fichiers

⚠️ Mode partiel : les contrôles anti-slop des phases < {start_phase} ne tournent
   pas sur cette session. Output utile pour itérer, NON validé qualité production.

Prêt à lancer la phase {start_phase}. On y va ?
```

Attendre validation avant de continuer.

---

## ÉTAPE 5 — Exécution du pipeline BIG

### 5.1 Charger le SKILL.md de BIG

```
Lire le fichier : {big_skill_dir}/SKILL.md
```

Où `{big_skill_dir}` = chemin absolu vers `.claude/skills/brand-identity`.

### 5.2 Localiser la phase demandée

Mapping `{start_phase}` → section dans SKILL.md :

| `{start_phase}` | Section à chercher dans SKILL.md |
|---|---|
| `1` | `## PHASE 1 — Brief Analysis` |
| `2A` | `### Étape 2A (subagent) : Tension & Ventre Mou` (puis enchaîne 2B→2C→2D ; produit aussi `{brand}-validated-temperature.md` via le bloc 2bis Diagnostic de température) |
| `2B` | `### Étape 2B (orchestrateur) : Présentation & Collecte des curseurs` (puis enchaîne 2C→2D) |
| `2C` | `### Étape 2C (subagent) : Territoires Créatifs` (puis enchaîne 2D) |
| `2D` | `### Étape 2D (orchestrateur, inline) : Mix pondéré` |
| `3A1` | `### Étape 2D-bis (orchestrateur) : Décontamination du contexte` (produit `context-clean.md`), puis `### Étape 2E (orchestrateur, inline) : Choix du registre` (ouvre `ref/registres-creatifs.md`), puis `### Étape 3A — Concepts Narratifs (Mode Sélectif)` (sous-étapes S1-S10). |
| `3A2` | Batch supplémentaire : commence au Checkpoint Pass A simplifié (3 options : nouveau batch autre registre / nouveau batch même registre / avancer). L'option de relance enchaîne l'Étape 3A — Mode Sélectif (version auto-incrémentée, ou réutilisée si le batch précédent était à 0 retenu). |
| `3B-1` | `### Étape 3B-0 — Routeur chromatique v2 (subagent isolé, AVANT le design dérivé)` dans le SKILL.md de BIG (note : BIG nomme cette étape `3B-0`, test-big la nomme `3B-1` pour avoir une séquence continue). Subagent isolé, produit la grille `chromatic-gamuts.md` (territoire×aptitude) + enforce + gate v2 + planche grille, validation user des gammes, puis enchaîne 3B-2. |
| `3B-2` | `### Étape 3B — Design Dérivé (Pass B)` — commence à la `#### Vague 1 — Palettes par divergence séquentielle dégressive` (pré-calcul buckets + directive ; 3 palettes A/B/C par concept, divergence mécanique, 3 gates, planche comparative, choix utilisateur) |
| `3B-3` | `#### Vague 2 — Penseurs typographiques` dans l'Étape 3B — sous-vagues : Vague 2 (penseurs) → Vague 2bis (gate anti-slop) → Vague 2ter (designer typo : descriptions, choix top 3, font-backups, planche font-recap) |
| `3B-4` | `#### Vague 3 — Spécimens anticipés` dans l'Étape 3B — spécimens typo + palette choisie |
| `3B-7a-pre` | `#### Étape 3B-7a-pre — Routeur de styles (subagent isolé, TOUJOURS exécuté avant 3B-7a)` dans l'Étape 3B. Sub-agent isolé qui produit `{brand}-style-sectoriel-tags.md` (tag binaire SECTORIEL/NON-SECTORIEL des 34 styles selon le ventre mou). Puis enchaîne 3B-7a. |
| `3B-7a` | `#### Étape 3B-7a — Styliste (divergence séquentielle A→B→C)` dans l'Étape 3B (lance la séquence complète A → B → C → 3B-7b → 3B-7-checkpoint, point d'arrêt naturel = choix utilisateur des variantes ; pas de reprise possible à mi-séquence — soit on relance tout, soit on ne relance pas). Si `{brand}-style-sectoriel-tags.md` n'existe pas, lancer 3B-7a-pre d'abord. |
| `3B-7b` | `#### Étape 3B-7b — Spécimen stylisé (9 sub-agents PARALLÈLES — 3 concepts × 3 variantes)` dans l'Étape 3B (puis enchaîne 3B-7-checkpoint) |
| `3B-7-checkpoint` | `#### Étape 3B-7-checkpoint — Choix utilisateur entre les 3 variantes par concept` dans l'Étape 3B (point d'arrêt naturel — pause user) |
| `3B-7c` | `#### Étape 3B-7c — Direction visuelle ancrée Perplexity (séquence en 10 sous-étapes pour UN concept)` dans l'Étape 3B (depuis le refactor 5 mai 2026 — séquence séquentielle pour UN concept ; Branche A bypasse Perplexity pour Mockup/CSS-SVG, Branche B utilise Perplexity + recherche manuelle Cosmos/Behance/ArtStation + génération MJ/NB2 externe + description fine au format spec) |
| `3B-7d` | `#### Étape 3B-7d — Pitch complet (resume des 3 designers EN PARALLÈLE)` dans l'Étape 3B (= ancien `3B-7c` = ancien `Interaction 3`) |
| `3B-7e` | `### Étape 3B-7e — Génération de variantes visuelles supplémentaires (skill séparé `/visual-prompt` mode variantes)` dans l'Étape 3B (= ancien `3B-6` = ancien `Étape 3C` — historiquement `/visual-brief`, déprécié depuis mai 2026) |
| `3B-7` | (alias rétrocompatible) → `#### Étape 3B-7d — Pitch complet` (mappe sur `3B-7d`) |
| `4` | `## PHASE 4 — Style-Tile HTML` (hero + zone médiane + atmosphere, SANS artefact complet) |
| `4-val` | `### Étape 4.1bis` — Pause utilisateur validation HTML v0, puis enchaîne gates + artefact |
| `4-art` | `### Étape 4.7` — Subagents artefact dédiés (insertion dans les style-tiles via placeholder) |
| `4B` | `## PHASE 4bis — DA Check` |
| `5` | `## PHASE 5 — Itération & Choix Final` |
| `5D` | `## ÉTAPE 5D — Animation du style-tile` (proposition 5D-0 → analyse + preset 5D-1 → choix 5D-2 → subagent `phases/phase-5d-animation.md` 5D-3 → itération 5D-4 → finalisation 5D-5) |
| `L` | `## PHASE LOGO` |
| `6A` | `## PHASE 6A — Batch 2 (Système de Signes)` (depuis D59 du 2026-05-27 : **2 étapes filles** — `### Étape 6A-0 — Router Famille d'Icônes` (subagent isolé qui choisit 1 famille parmi 8 et écrit `{brand}-icon-family-choice.md` + validation user obligatoire) puis `### Étape 6A-1 — Batch 2 HTML` (subagent designer Batch 2 actuel avec chapitre 06 refondu en 3 sections). Inclut, après l'injection SVG, l'étape « Gate anti-slop Batch 2 » — `scripts/phase6-batch-gate.py`, D56 ; auto-correction chirurgicale 1 tour sur `deterministic_fails`. Le gate a besoin du `:root` du style-tile retenu, déjà parmi les fichiers copiés au démarrage 6A) |
| `6B` | `## PHASE 6B — Batch 3` (inclut « Étape 6B-6 — Gate anti-slop Batch 3 », D56, après l'assemblage) |
| `7` | `## PHASE 7 — Zone 2` |
| `8A` | `## PHASE 8 — Brand Book éditorial (optionnelle)` dans le SKILL.md de BIG (le titre reste "PHASE 8" côté BIG pour stabilité interne) — invoque skill /brand-book qui invoque sous-skill SPG /generate-mini-deck. Exécuté d'un bloc, non-reprenable au milieu. |
| `8B` | `## PHASE 8b — Design System technique (optionnelle)` dans le SKILL.md de BIG (le titre reste "PHASE 8b" côté BIG pour stabilité interne) — invoque skill /design-system autonome, pas de sub-skill. Exécuté d'un bloc, non-reprenable au milieu. |
| `9` | `## ÉTAPE FINALE — Packaging des livrables` (création du dossier `{brand}-identity-{slug}/` avec fichiers renommés ; inclut le sous-dossier `brand-book/` si Phase 8A exécutée, et le sous-dossier `design-system/` si Phase 8B exécutée) |

### 5.3 Exécuter

Exécuter les instructions de la phase en substituant :

| Variable SKILL.md | Valeur test |
|---|---|
| `{skill_dir}` | Chemin absolu vers `.claude/skills/brand-identity` |
| `{session_dir}` | `{session_dir}` (le dossier de test : `test-{brand}-{session_label}`) |
| `{brand}` | `{brand}` |
| Toutes les variables de l'étape 3 | Les valeurs extraites/collectées |

**Le dossier output est `{test_dir}`** — toutes les écritures de fichiers vont dans ce dossier.

### 5.4 Continuer ou s'arrêter

Après chaque phase terminée, demander à l'utilisateur :

```
Phase {N} terminée. Que souhaitez-vous faire ?
  1. Continuer vers la phase suivante
  2. Relancer cette phase (avec ajustements)
  3. Arrêter ici
```

**Respecter la boucle d'itération de BIG** : ne jamais passer à la phase suivante sans validation explicite de l'utilisateur.

---

## RÈGLES

1. **Zéro modification de BIG** — Ce skill lit et suit `brand-identity/SKILL.md` tel quel. Aucun couplage, aucune dépendance inversée.
2. **Isolation totale** — Chaque test crée son propre dossier. Les fichiers source ne sont jamais modifiés.
3. **Copie, pas liens** — Toujours `cp`, jamais de symlinks. Protège les originaux.
4. **Anti-/tmp/** — JAMAIS utiliser `/tmp/`. Toujours `{test_dir}/.tmp-*` pour les fichiers temporaires.
5. **Traçabilité** — Le `.test-context.md` documente tout. On sait toujours d'où vient un test.
6. **Ref et examples de BIG** — Utiliser `{skill_dir}/ref/` et `{skill_dir}/examples/` de brand-identity directement. Ce skill n'a pas ses propres ref/examples.
