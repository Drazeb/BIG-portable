---
name: brand-book
description: Génère un brand book HTML éditorial (cover + intro Identity Card + 8 sections + closing) à partir d'un pack d'identité BIG (design-specs, pitch, style-tile, batches, visuels finaux). Sections 07a Web + 07b Pitch Deck + 07c Réseaux sociaux générées automatiquement. Skill autonome, pas encore branché au pipeline BIG.
---

# Brand Book Generator

Skill standalone qui transforme un **pack d'identité BIG complet** (sortie du pipeline `/brand-identity`) en un **brand book HTML éditorial** structuré en **cover + sommaire + intro Identity Card + 8 sections + closing**, suivant un mode chromatique mixte (positif + Dark Cinema natif) et un slide rythm prédictible.

**Structure sanctuarisée 27 mai 2026** : section Voice & Tone retirée (focus brand identité visuelle, pas verbale), intro "Identity Card / Le pack en une vue" ajoutée en bento entre sommaire et Big Idea, renumérotation ex-07 SYSTEM → 06, ex-08 APPLICATIONS → 07, ex-09 PHOTO → 08. Sommaire et corps Big Idea / Concept passés en CSS multicol 2 colonnes.

**Invocation** : appel direct par l'utilisateur ou par un sub-agent (pas de slash command finalisée — skill en phase de test).

**Statut** : **autonome avec génération complète de la section 07 Applications branchée** (07a Web via capture style-tile, 07b Pitch Deck via sous-skill SPG `generate-mini-deck`, 07c Réseaux sociaux via templates LinkedIn + X et scripts de capture) **+ intro 00 Identity Card sanctuarisée 27 mai 2026**. **Pas encore branché au pipeline BIG** (le `/brand-identity` ne l'appelle pas en fin de pipeline — étape suivante).

---

## PERSONA

Tu es un **éditeur-designer de brand books** au croisement du studio Koto (rigueur éditoriale, palette claire posée à plat, manifesto sobre) et de Behance/Brand World classique (cover peinture pivot, sections numérotées, closing statement). Tu sais :

- Lire un pack BIG complet et identifier précisément QUELLE donnée nourrit QUELLE section
- Composer du long-scroll éditorial avec un rythme prédictible (sections de hauteur ~720-900px)
- Doser le silence visuel (whitespace généreux, colonnes ~55ch, pas de bourrage)
- Alterner mode immersif (1 atome esthétique = 1 page) et mode grille documentaire (composants côte à côte)
- Respecter les tokens canoniques de la marque (palette oklch, fonts, radius, halos) SANS jamais les remplacer par des valeurs génériques

Tu n'es PAS un stratège de marque (les concepts sont déjà figés dans le pack), tu n'es PAS un développeur back-end. Tu es l'**éditeur qui met en livre** une identité validée.

---

## INPUTS — Pack BIG attendu

Le skill est appelé avec **1 argument obligatoire** et **1 argument optionnel** :

**Argument 1 (obligatoire) — `pack_path`** : path absolu du pack d'identité BIG.

**Argument 2 (optionnel) — `pitch_deck_mini_path`** (sanctuarisé 30 mai 2026) : path absolu vers un dossier contenant déjà les 6 PNG du mini-deck pitch produites en amont (cas du mode pipeline BIG, voir Étape 2d Mode A). Si fourni, le skill SKIP l'invocation Task SPG (qui échouerait en niveau 2) et copie/utilise directement les PNG existants. Si absent, le skill invoque SPG via sub-agent Task (Mode B standalone — niveau 0 → 1 OK).

Format attendu pour `pack_path` : `outputs/{brand}-{session}/{brand}-identity-{concept}/` (mais le skill accepte aussi un dossier flat ne contenant que le pack, comme `outputs/voltapilot-identity/`).

Ce dossier DOIT contenir au minimum :

| Fichier | Rôle | Sections du brand book qui en dépendent |
|---------|------|------------------------------------------|
| `{brand}-design-specs.md` | Spec source de vérité (12 sections) | 01-08 (toutes), 07c (meta entreprise) |
| `{brand}-pitch.md` | Récit narratif du concept | 00 IDENTITY CARD (manifesto) + 01 BIG IDEA + 02 CONCEPT + 07b content-mapper + 07c tagline/about |
| `{brand}-style-tile.html` | Style-tile HTML | 07a WEB (via capture PNG) + extraction tokens canoniques (palette, fonts, radius, alias bento) + 07b Sub0-A analyse visuelle + 07c wordmark/avatar HTML |
| `{brand}-batch2.html` | Batch 2 signes | 00 IDENTITY CARD (4 icônes signature + dataviz signature), 03 IDENTITÉ (lockups), 06 SYSTÈME (icônes, UI, charts), 07b Sub0-A composants UI |
| `{brand}-batch3.html` | Batch 3 narration | 08 PHOTO & ILLUSTRATION, 07b Sub0-A sections éditoriales |
| `visual-final/` | Dossier des visuels finaux | COVER, 00 IDENTITY CARD (bb-cover bento), CLOSING, 08 PHOTO, 07c cover bandeau LinkedIn + X (hero painterly) |

**Anti-fragile** : si un fichier est absent, le skill log un warning et continue avec la section minimisée. Mais l'absence de `design-specs.md` est bloquante.

---

## ⚠ MODE D — Aspiration de Brand (sanctuarisé 2026-06-02)

Le skill brand-book peut être invoqué sur un pack produit en **mode aspiration** (Mode D du pipeline BIG). En mode D, la marque a été aspirée d'un site existant — il n'y a **PAS de pitch créatif**, donc plusieurs sections narratives ne peuvent pas être générées sans inventer des histoires que la marque ne reconnaîtrait pas.

### Détection automatique du mode D

À l'Étape 0 (identification de la session), vérifier :
- `{brand}-extracted-dna.md` présent ➜ probable mode D
- `{brand}-pitch.md` absent ➜ confirme mode D
- Si les deux conditions sont vraies : `MODE_D = true`. Sinon : `MODE_D = false` (mode A/B/C standard).

Logger explicitement au démarrage : `"Mode détecté : {A/B/C standard | D Aspiration}"`.

### Sections SKIPPÉES en mode D

| Section | Raison du skip | Alternative |
|---------|---------------|-------------|
| **01 BIG IDEA** | Section narrative qui raconte la métaphore fondatrice du concept. Sans pitch créatif, pas de Big Idea à raconter (la marque connaît sa Big Idea mieux que la machine). | Section retirée du sommaire et du HTML final. |
| **02 CONCEPT** | Section narrative qui développe le concept et la tension résolue. Sans pitch, rien à narrer. | Section retirée. |
| **07c Réseaux sociaux** | Mockups LinkedIn + X qui dépendent à la fois du tagline/about extrait du pitch ET des visuels de profil. En mode aspiration, les vrais comptes sociaux de la marque ont déjà leur identité réelle, on ne va pas la dupliquer en mockup. | Section retirée. Pas de capture mockup. |

### Sections DÉGRADÉES en mode D

| Section | Adaptation |
|---------|-----------|
| **00 INTRO Identity Card** | Le bento Identity Card est composé partiellement : <br>• `WORDMARK_*` ✅ généré (nom marque + overline générique) <br>• `BRAND_SIGNATURE_COORDS` / `_CADENCE` ⚠ remplacés par méta-data du DNA (ex: secteur + année si dispo dans DNA, sinon `"—"` / `"—"`) <br>• `MANIFESTO_LINE1` / `_LINE2` / `_SUB` ❌ skippés — le bloc manifesto du bento devient un bloc visuel placeholder (1 ligne courte type "Identité aspirée du site" + 1 ligne mono `"Mode D — Aspiration {date}"`) <br>• `IDENTITY_CARD_ICONS_4` ✅ extraites du batch2 <br>• `DATAVIZ_SIGNATURE_SVG` ✅ extraite du batch2 <br>• 6 jeux palette `COLOR_N_*` ✅ depuis DNA |
| **07a Web** | ✅ Inchangée (capture du style-tile). |
| **07b Pitch Deck** | ✅ **Génération possible** via construction préalable d'un **pitch synthétique Mode D** (cf. sous-section "Construction du pitch synthétique pour 07b" ci-dessous). Le mini-deck SPG produit ses 6 slides normalement — l'analyse visuelle (Étape 2 SPG) et les 6 archétypes (Étape 3 SPG) s'appuient sur le style-tile/batch2/batch3 et ne consomment pas le pitch. Seule l'Étape 4 SPG (content-mapper) utilise le pitch + design-specs, et la voice principale est dans le design-specs §01.4 (rempli en mode D par Phase 7). Le pitch synthétique Mode D fournit le complément "concept + vocabulaire signature" sans invention créative. |
| **07c Réseaux sociaux** | ❌ Skip (voir section SKIPPÉES). |

### Construction du pitch synthétique pour 07b (Mode D uniquement)

À l'Étape 2d (avant d'invoquer le mini-deck SPG), construire un fichier temporaire `{brand}-pitch.md` dans `{pack_path}/` (ou un alias) au format suivant, **pure restitution depuis le DNA, AUCUNE invention narrative** :

```
# {brand} — Synthèse Mode D pour Pitch Deck

**Mode** : Aspiration d'une brand existante (pas de pitch créatif)

## Concept

{nom de la marque} est {extrait section 6.3 du DNA — personnalité de marque en 1 phrase synthétique}.

{1 paragraphe descriptif composé depuis sections 5.1 (ton de voix) et 5.4 (logo style) du DNA}

## Voice

{copie intégrale de la section 5.1 du DNA — Ton de voix : registre, exemples headlines, vocabulaire, personnalité}

## Vocabulaire signature

**Preferred words** : {extraits du DNA section 5.1 vocabulaire dominant — liste mots-clés}
**Forbidden words** : (à laisser vide ou aligner sur design-specs §01.4 si présent)

## Tonalité

{extrait section 5.1 DNA — phrases caractéristiques + tonalité}
```

Ce fichier est **temporaire** (préfixe `.tmp-` recommandé : `{brand}-pitch.md.tmp-mode-d`) — il ne va PAS dans le pack final. Il sert uniquement à alimenter le mini-deck SPG en Étape 2d. Il peut être supprimé après génération des 6 PNG. **Alternative** : si SPG accepte un argument `pitch_override_content`, passer directement le contenu en mémoire sans créer de fichier.

### Sections INCHANGÉES en mode D (génération normale)

- Cover (painterly)
- Sommaire (renuméroté pour refléter les sections 01, 02, 07c skippées)
- **03 IDENTITÉ** (logo, lockups depuis batch2)
- **04 PALETTE** (depuis DNA + style-tile)
- **05 TYPOGRAPHIE** (depuis DNA + style-tile)
- **06 SYSTÈME** (depuis batch2 — icônes, UI, charts)
- **07a APPLICATIONS Web** (capture style-tile)
- **07b APPLICATIONS Pitch Deck** (en mode dégradé — voir section DÉGRADÉES + pitch synthétique Mode D)
- **08 PHOTO** (depuis batch3 + visual-final/)
- Closing (statement visuel)

### Variables Mustache en mode D

Toutes les variables relatives aux sections skippées doivent être initialisées à des valeurs vides ou des placeholders explicites pour éviter les substitutions parasites :

```
BIG_IDEA_H1            = ""    (section skippée)
BIG_IDEA_SUBTITLE      = ""
BIG_IDEA_P1/2/3        = ""
CONCEPT_*              = ""    (section skippée)
PITCH_DECK_TITLE       = (rédiger depuis pitch synthétique Mode D — ex: "Pitch deck — {brand}")
PITCH_DECK_SUBTITLE    = (rédiger depuis pitch synthétique Mode D — ex: "6 slides type B2B générées depuis l'identité aspirée")
MANIFESTO_LINE1        = "Identité aspirée du site"
MANIFESTO_LINE2        = ""
MANIFESTO_SUB          = "Mode D — Aspiration {date_aspiration}"
BRAND_SIGNATURE_COORDS = (méta DNA si dispo, sinon "—")
BRAND_SIGNATURE_CADENCE = (méta DNA si dispo, sinon "—")
TAGLINE                = ""    (utilisé par 07c — section skippée)
```

### Skip technique des étapes

| Étape SKILL.md | Action en mode D |
|----------------|-----------------|
| **Étape 1** | Lire DNA au lieu du pitch. Substituer le contenu pitch par une mini-synthèse Mode D (même format que celui produit en Phase 6A — palette dominante, typo, atomes, personnalité 5.1, style photo 5.2, style icônes 5.3) |
| **Étape 2b** Mockup LinkedIn | **SKIP** (07c skippée) |
| **Étape 2c** Mockup X | **SKIP** (07c skippée) |
| **Étape 2d** Mini-deck pitch SPG | **EXÉCUTÉ avec adaptation** : avant l'invocation SPG, construire un fichier `{brand}-pitch.md` synthétique temporaire (cf. sous-section "Construction du pitch synthétique pour 07b" ci-dessus). Puis lancer SPG normalement (Mode A pipeline OU Mode B standalone selon contexte). SPG produira ses 6 PNG normalement — l'analyse visuelle Sub0-A consomme uniquement les HTML, le content-mapper consomme le pitch synthétique + design-specs §01.4. |
| **Étape 2e** Composition Identity Card | Composer en mode dégradé (cf. tableau "Sections DÉGRADÉES" ci-dessus) |
| **Étape 3** Sub-agent générateur | Le prompt du sub-agent reçoit en plus de ses inputs habituels la variable `{MODE_D}` = true. Le sub-agent skippe les sections 01, 02, 07c et produit un sommaire renuméroté (07b restera présente avec les 6 PNG produites par SPG). |
| **Étape 4** template-vars.json | Inclure toutes les variables avec leurs valeurs vides/placeholders pour mode D — le template gérera le skip via Mustache conditionnel. PITCH_DECK_TITLE et PITCH_DECK_SUBTITLE sont rédigées depuis le pitch synthétique. |
| **Étape 4bis** Quality gate | Adapter — ne pas alerter sur l'absence des variables des sections skippées en mode D |

### Pourquoi cette approche

**Décision sanctuarisée avec Charles 2026-06-02** : en mode aspiration, la marque connaît son identité mieux que la machine. Inventer une métaphore, un Big Idea, un Concept narratif serait raconter une histoire que la marque ne reconnaîtrait pas. Mieux vaut un brand book **plus court mais 100% fidèle** à la marque réelle (style Carbon/Atlassian sur la partie visuelle, sans la couche éditoriale du concept). Le user qui aspire sa propre marque cherche un livrable pour ses **assets marketing**, pas une re-explication de qui il est.

---

## OUTPUTS

Dans `.claude/skills/brand-book/outputs/{brand}-test-v{N}/` :

```
{brand}-test-v{N}/
├── {brand}-brand-book.html              ← LIVRABLE PRINCIPAL (produit par render-brand-book.py)
├── template-vars.json                   ← Intermédiaire — valeurs des ~100 slots Mustache (Étape 4)
├── {brand}-batch2-inventory.html        ← Intermédiaire — extract-then-inject (Étape 2.5)
├── {brand}-batch2-inventory.json        ← Intermédiaire — manifest MD5 des composants (Étape 2.5)
├── {brand}-landing-fullpage.png         ← Capture full-page du style-tile
├── {brand}-style-tile.html              ← Copie du style-tile (utile pour re-capture)
├── {brand}-linkedin-mockup.png          ← Capture mockup LinkedIn (07c)
├── {brand}-x-mockup.png                 ← Capture mockup X (07c)
├── pitch-deck-mini/                     ← 6 PNG mini-deck SPG (07b)
│   ├── slide-01-cover.png
│   ├── slide-02-case-study.png
│   ├── slide-03-data-viz.png
│   ├── slide-04-dashboard-kpi.png
│   ├── slide-05-process-timeline.png
│   └── slide-06-icon-grid.png
└── visual-final/                        ← Copie des visuels finaux
    ├── {brand}-c{N}-{paletteID}-hero.png
    ├── {brand}-c{N}-{paletteID}-halo.png
    └── ...
```

Le numéro de version `v{N}` est déterminé par l'utilisateur au moment de l'invocation. Par défaut : incrémenter au-dessus du plus haut existant.

---

## FICHIERS DE RÉFÉRENCE

### Chargés au démarrage (OBLIGATOIRE — lire AVANT toute action)

| Fichier | Ce qu'il contient | Quand l'utiliser |
|---------|-------------------|------------------|
| `ref/structure.md` | Intro Identity Card + 8 sections détaillées (contenu, source dans le pack, mode chromatique, mode de présentation, hauteur indicative) | Construction de CHAQUE section |
| `ref/style-guide.md` | Règles formelles transverses : layout, slide rythm, mode mixte chromatique, tokens canoniques, anti-patterns | Pendant TOUTE la génération HTML |
| `ref/editorial-patterns.md` | Comment rédiger Big Idea, Concept — format éditorial 2-cols magazine, dose de silence | Sections 01, 02 |
| `ref/template-base.html` | Squelette HTML de départ (head, tokens, sections vides, classes utility, bento Identity Card complet) | Point de départ — tu copies puis tu peuples |

### Lus à la demande

| Fichier | Quand le lire |
|---------|---------------|
| `ref/benchmark-notes.md` | Si tu as un doute sur la forme d'une section (référence : 9 case studies Behance/Koto) |

---

## WORKFLOW

### Étape 0 — Identification de la session

Demander à l'utilisateur (ou recevoir en argument) :
1. **Path absolu du pack BIG** (ex: `outputs/voltapilot-identity/`)
2. **Numéro de version** pour l'output (ex: `v1`, `v2`...)

Vérifier l'existence du dossier source et des fichiers attendus. Lister explicitement ce qui est présent et ce qui manque.

### Étape 1 — Lecture des inputs

Lire dans l'ordre :
1. `{brand}-design-specs.md` (intégralement — c'est la source de vérité)
2. `{brand}-pitch.md` (intégralement) — ⚠ **Mode D** : ce fichier n'existe pas. Lire `{brand}-extracted-dna.md` à la place et noter les sections 5.1 (ton de voix), 5.2 (style photo), 5.3 (style icônes). Ne PAS chercher à extraire Big Idea / Concept / Manifesto — ces variables resteront vides (voir section "MODE D — Aspiration de Brand" ci-dessus).
3. `{brand}-style-tile.html` (extraire le bloc `:root` et la liste des Google Fonts importés)
4. `{brand}-batch2.html` (extraire les lockups, icônes, composants — pas réécrire, citer)
5. `{brand}-batch3.html` (extraire les exemples de prompting MJ et les références photo)
6. `ls visual-final/` (lister les visuels disponibles avec leurs noms canoniques)

À l'issue de cette étape, tu as en mémoire : palette oklch complète, fonts, radius, wordmark, ~~big idea, concept, manifesto~~ (en mode A/B/C uniquement — en mode D ces 3 variables sont vides), lockups, icônes canoniques (4 sélectionnées pour le bento + le set complet pour 06 Système), prompts MJ (en mode A/B/C — en mode D ces prompts sont remplacés par les `inputs/visuals/` aspirés s'ils existent), et le mapping des visuels finaux.

### Étape 2 — Génération des assets sections 07 + composition Identity Card

Cette étape produit **tous les PNG nécessaires aux sous-sections 07 APPLICATIONS** (07a Web, 07b Pitch Deck, 07c Réseaux sociaux) **et compose les variables du bento Identity Card** (00 intro). Cinq sous-étapes parallélisables (sauf 2e qui dépend de l'extraction batch2 faite en Étape 1).

#### Étape 2a — Capture PNG du style-tile (section 07a Web)

```bash
python3 .claude/skills/brand-book/scripts/capture-style-tile.py \
  "{pack_path}/{brand}-style-tile.html" \
  ".claude/skills/brand-book/outputs/{brand}-test-v{N}/{brand}-landing-fullpage.png"
```

Dépendances : `pip install playwright && playwright install chromium` (à faire une fois sur la machine).

**Pourquoi un PNG et pas une iframe ?** Les iframes posent des problèmes insolubles de scaling/scroll horizontal. Le PNG full-page rendu en headless Chrome à viewport 1280×800 capture fidèlement, et on l'insère ensuite comme `<img>` posé sur fond gradient palette avec drop-shadow.

#### Étape 2b — Mockup LinkedIn (section 07c)

1. **Charger le template** `ref/linkedin-profile-mockup.html`
2. **Substituer les Mustache** avec les données extraites Étape 1 (cf. tableau "Mapping Mustache 07c" plus bas), écrire dans `outputs/{brand}-test-v{N}/{brand}-linkedin-mockup.html`
3. **Lancer la capture** :
   ```bash
   python3 .claude/skills/brand-book/scripts/capture-linkedin-mockup.py \
     "outputs/{brand}-test-v{N}/{brand}-linkedin-mockup.html" \
     "outputs/{brand}-test-v{N}/{brand}-linkedin-mockup.png"
   ```
4. **Résultat** : PNG paysage **1000×563 retina ×2** (= 2000×1126 pixels physiques), fond transparent (la card LinkedIn flotte sur le beige de la cellule diptyque). Le script utilise `page.locator(".li-profile-card").screenshot(omit_background=True)`.

#### Étape 2c — Mockup X (section 07c)

1. **Charger le template** `ref/x-profile-mockup.html`
2. **Substituer les Mustache** (cf. tableau "Mapping Mustache 07c"), écrire dans `outputs/{brand}-test-v{N}/{brand}-x-mockup.html`
3. **Lancer la capture** :
   ```bash
   python3 .claude/skills/brand-book/scripts/capture-x-mockup.py \
     "outputs/{brand}-test-v{N}/{brand}-x-mockup.html" \
     "outputs/{brand}-test-v{N}/{brand}-x-mockup.png"
   ```
4. **Résultat** : PNG carré **1000×1000 retina ×2** (= 2000×2000 pixels physiques), fond blanc mode light X intrinsèque. Le script capture le viewport entier (PAS de `omit_background` ici — l'UI X officielle a un fond blanc qu'on conserve).

#### Étape 2d — Mini-deck pitch (section 07b) — MODE DUAL (sanctuarisé 30 mai 2026)

Cette étape produit les 6 PNG du mini-deck pitch consommées par la section 07b du brand book. **Le mécanisme dépend du contexte d'invocation** — c'est le fix du bug architectural Claude Code : un seul niveau de délégation Task autorisé (anti-récursion harness).

**Détection du mode** : si l'orchestrateur fournit en paramètre une variable `pitch_deck_mini_path` (chemin absolu vers un dossier contenant déjà les 6 PNG produites en amont par SPG), tu es en **mode pipeline (BIG)**. Sinon tu es en **mode standalone**.

##### Mode A — Pipeline (variable `pitch_deck_mini_path` fournie)

Le sub-agent brand-book est lui-même un niveau 1 (lancé par l'orchestrateur BIG niveau 0). Lancer un sous-Task SPG ici = niveau 2 = **REFUSÉ par l'harnais Claude Code**. Donc le pipeline BIG a déjà fait tourner SPG en parallèle (Étape 8-1 du BIG SKILL.md) et te passe le path PNG en argument.

Vérifier que les 6 PNG existent :
```bash
ls "{pitch_deck_mini_path}"/slide-01-cover.png \
   "{pitch_deck_mini_path}"/slide-02-case-study.png \
   "{pitch_deck_mini_path}"/slide-03-data-viz.png \
   "{pitch_deck_mini_path}"/slide-04-dashboard-kpi.png \
   "{pitch_deck_mini_path}"/slide-05-process-timeline.png \
   "{pitch_deck_mini_path}"/slide-06-icon-grid.png
```

Si le dossier `{pitch_deck_mini_path}` est DIFFÉRENT du dossier où le brand book attend les PNG (`{output_dir}/pitch-deck-mini/`), copier les 6 PNG dedans :
```bash
mkdir -p "{output_dir}/pitch-deck-mini/"
cp "{pitch_deck_mini_path}"/slide-*.png "{output_dir}/pitch-deck-mini/"
```

Si le dossier est DÉJÀ celui attendu (cas BIG qui produit direct dans `{session_dir}/brand-book/pitch-deck-mini/`), aucune copie nécessaire.

**Quality gate Mode A** : si une PNG manque, log un warning et continue (section 07b sera marquée "À générer manuellement"). Ne PAS tenter d'invoquer SPG en sous-Task (échouera).

##### Mode B — Standalone (pas de `pitch_deck_mini_path`)

Tu es lancé directement par l'utilisateur via `/brand-book {pack_path}` → niveau 0. Tu peux invoquer SPG via un sub-agent Task tool (niveau 1 = autorisé).

Lancer un **sub-agent Task tool (`general-purpose`)** qui invoque le sous-skill `generate-mini-deck` (dossier `/Slide Presentation Generator/.claude/skills/generate-mini-deck/`).

**Prompt du sub-agent** :
```
Tu es un sous-skill du brand-book. Ta mission : exécuter intégralement le
skill `generate-mini-deck` (lire son SKILL.md d'abord) avec ces paramètres :

- pack_path = "{pack_path absolu}"
- brand_slug = "{brand}" (slug court snake-case)
- output_dir = ".claude/skills/brand-book/outputs/{brand}-test-v{N}/pitch-deck-mini/"

Exécute ses 5 étapes (Étape 1 prep dossier identity SPG, Étape 2 Sub0-A
analyse visuelle, Étape 3 Sub0-B mode mini 6 archétypes, Étape 4
content-mapper voice brand, Étape 5 capture 6 PNG).

Skip intelligent : si VISUAL-ANALYSIS.md ou design-language.md existent
déjà dans /SPG/brands/{brand_slug}/, skip les étapes correspondantes.

Reporte STATUS: OK quand les 6 PNG sont produites dans output_dir, OU
STATUS: BLOCKED avec la raison.
```

**Quality gate Mode B** : `STATUS: OK` si les 6 PNG existent ET sont > 200 KB chacune. Sinon, log un warning et continue.

##### Output attendu (identique aux 2 modes)

6 PNG retina dans `{output_dir}/pitch-deck-mini/` :
- `slide-01-cover.png` (Cover, archétype SPG #1)
- `slide-02-case-study.png` (Case Study, #12)
- `slide-03-data-viz.png` (Data Viz, #9)
- `slide-04-dashboard-kpi.png` (Dashboard KPI, #10)
- `slide-05-process-timeline.png` (Process/Timeline, #7)
- `slide-06-icon-grid.png` (Icon Grid, #19)

**Pourquoi cette architecture duale ?** Limite dure de Claude Code : un seul niveau Task autorisé. Quand le BIG (niveau 0) lance brand-book (niveau 1), brand-book NE PEUT PAS lancer SPG en sous-Task (niveau 2 refusé). Le BIG fait donc tourner SPG en parallèle (lui aussi en niveau 1) et passe les PNG à brand-book. Le mode standalone reste préservé pour quand Charles lance `/brand-book` directement.

#### Étape 2e — Composition Identity Card (intro bento "Le pack en une vue") — **SANCTUARISÉ 27 mai 2026 (v4)**

Cette sous-étape ne produit pas de PNG : elle **compose en mémoire les variables Mustache** qui seront injectées dans le bento `.bento-v4` de la section `id="identity-card"`. Le bento v4 contient **7 cards en grille 3 cols × 6 rows × 120px** : Cover (1×4) · Wordmark enrichi (1×2) · Manifesto (2×2) · Icônes mini 4× bande horizontale (2×1) · Typo specimen Aa+Aa (2×1) · Dataviz (2×2) · Palette 6 couleurs (1×4).

**Différences clés vs v3** :
- Grille 3×6 × 120px (vs 3×3 × 240px en v3) → contrôle plus fin de la composition.
- **Palette à 6 couleurs** au lieu de 3 → le skill doit extraire 6 tokens couleur de `:root` et les nommer + classer par rôle.
- **Icônes en taille naturelle 32px** (PAS zoomées) — en v3 elles étaient en 64px et trop massives.
- **Wordmark enrichi** : overline (Brand ID · LL-{année}) + wordmark Gloock + signature mono 2 lignes (typiquement coordonnées géographiques + cadence/rythme propre à la marque, tirées du pitch). **Pas de tagline** (sanctuarisé sans, redondant avec le concept).
- Préfixe CSS `.bv4-*` (vs `.bb-*` en v3).

**Sources de composition** :

| Variable | Comment composer |
|----------|------------------|
| `{{COVER_VISUAL}}` | Choisir le visual hero principal dans `visual-final/` (chercher `{brand}-c{N}-{paletteID}-hero-*.{jpg,png}` — le plus painterly atmospheric) — chemin **relatif** depuis le brand-book HTML (`visual-final/...`). |
| `{{IDENTITY_CARD_TITLE}}` | Toujours `"Le pack en une vue."` (sanctuarisé). |
| `{{BRAND}}` | Slug du wordmark (bas-de-casse, ex: "camille"). |
| `{{WORDMARK_OVERLINE}}` | Texte mono court qui contextualise la card. Format canonique : `"Brand ID · LL-{année courante}"` (ex: `"Brand ID · LL-2026"`). |
| `{{BRAND_SIGNATURE_COORDS}}` + `{{BRAND_SIGNATURE_CADENCE}}` | **2 lignes mono contextuelles tirées du pitch** qui forment la signature bas de la card wordmark. Ligne 1 = typiquement coordonnées géographiques ou repère spatial (ex: `47°57′N · 5°06′W` pour Camille). Ligne 2 = cadence/rythme propre à la marque (ex: `Cadence 4 / 15s` pour Camille — rythme d'éclat du phare). Si la marque n'a pas de coords/cadence évidentes, choisir 2 méta-données mono signatures (ex: année de fondation + secteur, ou méthode + tempo). |
| `{{MANIFESTO_LINE1}}` + `{{MANIFESTO_LINE2}}` | 2 lignes Display courtes (3-6 mots chacune) extraites du `{brand}-pitch.md` (chercher la section Manifesto ou les piliers) — chaque ligne se termine par un `.` rendu en `<span class="dot">.</span>` qui prend la couleur accent. |
| `{{MANIFESTO_SUB}}` | 1 ligne de glose mono (10-20 mots) qui contextualise le manifesto. Souvent : "{positionnement court}. {Secteur} depuis {année si applicable}." |
| `{{ICONGRID_LABEL}}` | Label mono court (ex: `"Iconographie · 3 grammaires"` ou `"Iconographie"`). |
| `{{IDENTITY_CARD_ICONS_4}}` | **4 SVG icônes signature de la marque en bande horizontale**. Extraire 4 icônes depuis `{brand}-batch2.html` — chercher les `<svg aria-label="...">` dans la planche iconographique métier. Choisir 4 icônes qui couvrent les concepts clés du pitch (ex: Cap / Portée / Cadence / Ralliement pour Camille). Composer 4 blocs `<div class="bv4-icongrid__cell"><svg viewBox="0 0 32 32" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">...</svg></div>`. **Important** : le CSS force `svg { width: 32px; height: 32px; }` — l'icône s'affiche à sa taille naturelle, ne pas tenter de la grossir. Si les SVG source ont un viewBox plus large (ex: 48×48), garder le viewBox mais le CSS gère le rendu à 32px. |
| `{{FONT_DISPLAY_NAME}}` | Nom court de la fonte display (ex: "Gloock", "Authentic Sans"). |
| `{{FONT_MONO_NAME}}` | Nom court de la fonte mono/body (ex: "JetBrains", "Inter Mono"). |
| `{{DATAVIZ_LABEL}}` | Label court mono pour la dataviz (ex: "Cadence · 32 milles" pour Camille). Doit refléter une métrique signature de la marque. |
| `{{DATAVIZ_SIGNATURE_SVG}}` | **Bar chart SVG (6 barres dont 1 active en accent)**. Composer depuis batch2 (chercher un bar chart signature) ou utiliser le template par défaut : `<svg viewBox="0 0 320 150" preserveAspectRatio="xMidYMid meet">` avec 6 `<rect class="viz-bar">` dont 1 `is-active`, gridlines + axis + baseline + 6 labels d'axe (B1-B6 ou autre nomenclature brand). Voir le HTML Camille v4 §identity-card pour la structure exacte. |

**Palette 6 couleurs — RÔLES AGNOSTIQUES (refondu 2026-06-02)** — le skill extrait 6 tokens couleur depuis le `:root` du style-tile et compose 6 jeux de variables `{{COLOR_N_ROLE}}` + `{{COLOR_N_NAME}}` + `{{COLOR_N_HEX}}` pour N de 1 à 6, dans cet ordre canonique **agnostique de l'univers de marque** (avant le 2 juin 2026, ces rôles étaient calibrés sur Camille — "Fond profond / Surface claire / Détail froid / Surface beige / Accent signal / Accent chaud" — ce qui produisait des incohérences sur les marques aux univers chromatiques différents, notamment les marques light-dominant comme les SaaS B2B) :

| N | Rôle (mono caps) | Nom (display) | Source CSS prioritaire |
|---|------------------|---------------|------------------------|
| 1 | "Primaire" | Nom poétique de la couleur primaire de la marque | `--brand-color-primary` ou `--color-primary` |
| 2 | "Secondaire" | Nom poétique de la couleur secondaire | `--brand-color-secondary` ou `--color-secondary` |
| 3 | "Accent" | Nom poétique de l'accent | `--brand-color-accent` ou `--color-accent` |
| 4 | "Surface" | Nom de la surface dominante | `--brand-color-positive-bg` (si mode=light) ou `--brand-color-dark-bg` (si mode=dark) |
| 5 | "Texte" | Nom du texte principal | `--brand-color-positive-text` ou `--color-text-primary` |
| 6 | "Bord" | Nom du token de bord/séparateur | `--color-border` ou `--brand-color-positive-text` atténué |

Les 6 noms (col "Nom") sont **propres à chaque marque** — le skill reprend les noms poétiques du pitch / design-specs / DNA s'ils existent, sinon il forge un nom court (1-3 mots, display) cohérent avec l'univers de la marque (ex pour Camille : "Foyer / Brume / Marine / Nuit / Brume Cool / Cliff" ; ex pour Brevo : "Forest / Mint / Iris / Surface / Charbon / Brume"). Les rôles (col "Rôle") restent **canoniques et stables, agnostiques de l'univers** — ils décrivent la fonction structurelle universelle (Primaire/Secondaire/Accent/Surface/Texte/Bord), pas l'imagerie de Camille.

**Pourquoi ce refactor** : les anciens rôles ("Fond profond / Surface beige / Accent chaud") n'avaient de sens que pour des marques avec un univers chromatique riche en surfaces sombres + accent chaud (Camille, Vermeil, VoltaPilot). Pour une marque SaaS clair (Brevo : vert forêt + iris + mint), ces rôles forçaient des mappings absurdes. Les rôles agnostiques (Primaire/Secondaire/...) fonctionnent pour tous les univers chromatiques sans biais.

**Variables :root alias à injecter** (Étape 4 — :root sacré) :

```
--color-foyer:        var(--brand-color-accent);     /* ou alias direct vers la couleur native */
--color-foyer-warm:   {{COLOR_FOYER_WARM}};          /* version chaude/claire de l'accent */
--color-mist:         var(--brand-color-positive-bg); /* ou couleur Brume native */
--color-mist-cool:    {{COLOR_MIST_COOL}};           /* version plus claire (text-primary clair) */
--color-marine-cliff: {{COLOR_MARINE_CLIFF}};        /* détail froid — variante cliff/marine, sinon `--brand-color-accent-2` */
--color-night-clear:  {{COLOR_NIGHT_CLEAR}};         /* fond surface — Nuit Claire, lighten(--brand-color-dark-bg, ~5%) ; le CSS a un fallback `#142133` */
--font-display:       var(--brand-display);
--font-mono:          var(--brand-body);
--radius:             var(--brand-radius-xs);
```

**Quality gate** : 4 icônes extraites, 2 lignes manifesto extraites, 6 couleurs nommées et classées par rôle, signature wordmark (coords + cadence) extraite ou forgée. Si une composition échoue (ex: batch2 n'a pas d'icônes métier identifiables, ou la marque n'a pas de coords/cadence évidentes), log un warning et utiliser un placeholder visuel ou textuel cohérent (icône abstrait `circle + cross`, signature `"—"` / `"—"`).

---

### Étape 2.5 — Extraction inventory batch2 (extract-then-inject v5, SANCTUARISÉE 30 mai 2026)

Avant la génération HTML (Étape 4), **extraire mécaniquement** tous les composants UI / icônes / charts copiables-verbatim depuis `{brand}-batch2.html` vers un fichier inventory autonome. Ce mécanisme remplace l'ancienne approche "comptage + inventaire manuel par le sub-agent" qui s'est révélée insuffisante (cf. bug Atelier Vermeil 30/05/2026 : 28 SVG hachurés redessinés en versions plates, 4 badges + 4 toggles oubliés).

```bash
python3 .claude/skills/brand-book/scripts/extract-batch2-inventory.py \
  "{pack_path}/{brand}-batch2.html" \
  ".claude/skills/brand-book/outputs/{brand}-test-v{N}/{brand}-batch2-inventory.html" \
  --json-output ".claude/skills/brand-book/outputs/{brand}-test-v{N}/{brand}-batch2-inventory.json"
```

**Sortie attendue** :
- `{brand}-batch2-inventory.html` — document HTML autonome structuré par `<section data-inv="…">` × 10 catégories. Chaque bloc verbatim est borné par `<!-- BEGIN_BLOCK md5=<hash> -->` / `<!-- END_BLOCK -->`. Les `<defs>` SVG référencés via `url(#…)` sont **injectées inline** dans chaque SVG → chaque bloc est autonome.
- `{brand}-batch2-inventory.json` — manifest des hashes MD5 par catégorie, structure `{categories: {icons: {count, items: [{md5, label, source_line, ...}]}, buttons: {…}, …}}`. Consommé par le quality gate Étape 5.

**11 catégories extraites** :
- `icons` — wrappers `.glyph`, `.icon-card`, `.icon-cell`, `.icon-tile`, `.icon-spec`, `.stroke-step`, `.abstraction-step`, `.business-icon`
- `buttons` — `<button class="btn[ --variant]">` (hors `.tab`)
- `inputs` — wrappers `.field`, `.form-field`, `.input`, `.select`, `.input-wrap` contenant un `<input>` / `<select>` / `<textarea>`
- `badges`, `toggles`, `checkboxes` — wrappers à classe exacte ou BEM
- `cards` — `<article class="card[ --variant]">` + whitelist (`kpi-card`, `stat-card`, `metric-card`, `ui-card`, `data-card`, `tile`, `card--depth`, `card--kpi`)
- `tabs`, `alerts`, `progress` — wrappers conteneurs
- `charts` — SVG avec viewBox ≥ 150 dans au moins une dimension
- `lockups` — chapter de batch2 qui documente le logotype (contient .wordmark / .wordmark-plate / .lockup__mark / .exclusion__inner). Une seule entrée = la chapter entière, header retiré. Pour la section Identité (04) du brand book.

**Quality gate Étape 2.5** : lire `totals.all` du JSON. Si < 20, log `[WARN] Inventory minimaliste (totals.all=…)` et continuer (une marque peut avoir un batch2 légitime peu dense). Si = 0, **fail** (le script aurait dû lever une erreur, vérifier le format batch2).

**Précédence** : cette étape rend la règle 12 (Fidélité au pack source / §8quater) **automatiquement appliquée** au lieu de reposer sur la rigueur déclarative du sub-agent. La règle textuelle reste comme garde-fou conceptuel mais devient **subordonnée** à cette mécanique.

---

### Étape 3 — Copie des assets

```bash
cp -R "{pack_path}/visual-final" ".claude/skills/brand-book/outputs/{brand}-test-v{N}/"
cp "{pack_path}/{brand}-style-tile.html" ".claude/skills/brand-book/outputs/{brand}-test-v{N}/"
```

### Étape 4 — Production du `template-vars.json` (sanctuarisée v6 — 30 mai 2026)

> **RÈGLE STRUCTURELLE v6 (sanctuarisée 30 mai 2026 — remplace l'ancienne Étape 4 "génération HTML directe")**
>
> Tu **NE TOUCHES PLUS au HTML du brand book**. Tu produis UNIQUEMENT un fichier `template-vars.json` contenant les **valeurs** des slots Mustache du template. L'Étape 4bis lance un script Python qui fait la substitution mécanique — le markup HTML figé du template est **verrouillé par construction**.
>
> Bug que cette mécanique empêche (récurrent jusqu'au 30 mai 2026) : sub-agent qui réécrit / simplifie / invente le markup HTML d'une section pourtant figée par le template. Exemples observés :
> - 07b Pitch Deck (Vermeil) : spread asymétrique 2×3 (`s08b-spread > s08b-row--top + s08b-row--bottom`) remplacé par une grille à plat `.deck > .deck__slide × 6` → débordement viewport perdu.
> - Intro Identity Card v4 bento : "pétouille" sur l'arrangement des cellules.
>
> Avec cette mécanique : le sub-agent n'a même plus accès au markup. Impossible de le casser.
>
> **Slots AUTO-REMPLIS par le script (sanctuarisée v7 — 1er juin 2026 — option B)** : tu ne fournis PAS les slots ci-dessous dans `template-vars.json`. Le script `render-brand-book.py` les remplit automatiquement.
>
> | Slot template | Source automatique | Mécanique |
> |---------------|---------------------|-----------|
> | `{{BATCH2_INVENTORY_ICONS}}` à `{{BATCH2_INVENTORY_CHARTS}}` (8 slots) | `batch2-inventory.html` | Injection verbatim des `<article>` par catégorie. MD5 préservés → quality gate Étape 5 passe par construction. |
> | `{{BATCH2_INVENTORY_LOCKUPS}}` | `batch2-inventory.html` (catégorie lockups) | Injection verbatim de la chapter Logotype de batch2 (`.wordmark` / `.lockup` / `.exclusion__inner`) |
> | `{{PALETTE_PAGES_HTML}}` | Slots `COLOR_N_*` du JSON | Auto-composition de 6 pages couleur (rôle + nom + hex + swatch) |
> | `{{TYPO_SPECIMEN_HTML}}` | Slots `FONT_*` du JSON | Auto-composition de 3 specimens (Display / Body / Mono) avec Aa grand format |
> | `{{PHOTO_GALLERY_HTML}}` | Dossier `{output_dir}/visual-final/` | Listing des PNG existantes → grille auto |
>
> Cette mécanique évite la classe entière de bugs "le sub-agent réinvente le markup pour les sections listing". Bug observé Vermeil test E2E 31/05/2026 (23:36) : sections Identité / Palette / Typo / Photo restaient vides parce que le template avait des TODO HTML pas des slots. Maintenant ces 4 sections sont auto-composées depuis les données structurées.

#### 4.1 — Lister les slots attendus

Lire la liste complète des slots Mustache du template via :

```bash
grep -oE '\{\{[A-Z0-9_]+\}\}' .claude/skills/brand-book/ref/template-base.html | sort -u
```

Il y a ~106 slots uniques classés par section. **12 sont auto-remplis par le script** et ne doivent PAS être dans `template-vars.json` :
- 9 slots `BATCH2_INVENTORY_*` (ICONS / BUTTONS / INPUTS / BADGES / TOGGLES_CHECKBOXES / CARDS / MISC_UI / CHARTS / LOCKUPS)
- 3 slots auto-composés : `PALETTE_PAGES_HTML` / `TYPO_SPECIMEN_HTML` / `PHOTO_GALLERY_HTML`

Tu fournis donc ~94 slots dans le JSON (méta + tokens design + Identity Card v4 + éditoriaux + titres + sous-titres).

#### 4.2 — Composer les valeurs des slots

Pour CHAQUE slot non-BATCH2, produis une valeur en suivant les sources ci-dessous. Si tu ne sais pas pour un slot, mets une valeur placeholder visible (ex: `"À DÉFINIR"`) plutôt que de laisser manquer — l'Étape 5 surfacera la liste des `[MISSING:…]`.

**Méta (5 slots)** :
- `BRAND` : slug snake-case (ex: `les-vermeil`)
- `VERSION` : `"v1"`
- `YEAR` : année courante (ex: `"2026"`)
- `BRAND_THEME_COLOR` : hex `#RRGGBB` (couleur dominante palette, pour theme-color meta)
- `GOOGLE_FONTS_LINK` : balise `<link>` complète copiée depuis le style-tile
- **`MODE_CHROMATIQUE`** : valeur lue depuis le `:root` du style-tile (variable `--mode-chromatique`). Si absente : fallback `"dark"` (comportement legacy Camille). Valeurs possibles : `"light"`, `"dark"`, `"mixed"`. Pilote `<body data-mode="...">` qui active les overrides CSS adaptatifs du template (Cover, Closing, Photo s'adaptent à la luminance dominante de la marque).
- **`HAS_COVER_VISUAL`** : `"true"` si un fichier hero existe dans `visual-final/` (chercher `{brand}-c{N}-{paletteID}-hero*.{png,jpg,jpeg,webp}`), `"false"` sinon. Pilote `<body data-has-cover-visual="...">` qui force le fond solide (sans image) selon le mode chromatique en cas d'absence.
- **`HAS_CLOSING_VISUAL`** : idem pour le closing (chercher `{brand}-c{N}-{paletteID}-closing*` ou réutiliser le hero si absent).

**Tokens design (~20 slots)** : extraits du `:root` du style-tile (`FONT_DISPLAY`, `FONT_BODY`, `FONT_MONO`, `FONT_DISPLAY_NAME`, `FONT_MONO_NAME`, `COLOR_PRIMARY`, `COLOR_ACCENT`, `COLOR_ACCENT_2`, `COLOR_SECONDARY`, `COLOR_DANGER`, `COLOR_DARK_BG`, `COLOR_DARK_TEXT`, `COLOR_POSITIVE_BG`, `COLOR_POSITIVE_TEXT`, `COLOR_SUCCESS`, `COLOR_WARNING`, `COLOR_FOYER`, `COLOR_FOYER_WARM`, `COLOR_MIST`, `COLOR_MIST_COOL`, `COLOR_MARINE_CLIFF`, `COLOR_NIGHT_CLEAR`, `RADIUS_XS/SM/MD/LG`). **Obligatoire** pour que le rendu visuel soit cohérent.

**Sommaire (1 slot)** : `TOC_TITLE` (titre court H2 type "Le pack, chapitre par chapitre.")

**Intro Identity Card v4 bento (~22 slots)** : composés en Étape 2e — `IDENTITY_CARD_TITLE` (toujours "Le pack en une vue."), `COVER_VISUAL` (path relatif vers le hero), `WORDMARK_OVERLINE`, `BRAND_SIGNATURE_COORDS`, `BRAND_SIGNATURE_CADENCE`, `MANIFESTO_LINE1` / `MANIFESTO_LINE2` / `MANIFESTO_SUB`, `ICONGRID_LABEL`, `IDENTITY_CARD_ICONS_4` (string HTML contenant 4 SVG 32px concaténés), `DATAVIZ_LABEL`, `DATAVIZ_SIGNATURE_SVG` (string HTML contenant 1 SVG bar chart composé), et **6 jeux** `COLOR_N_ROLE` / `COLOR_N_NAME` / `COLOR_N_HEX` pour N de 1 à 6 (**rôles agnostiques refondus 2026-06-02** : Primaire / Secondaire / Accent / Surface / Texte / Bord — cf. tableau détaillé dans la section "Palette 6 couleurs — RÔLES AGNOSTIQUES" plus haut).

**Sections éditoriales (~10 slots)** :
- `BIG_IDEA_H1`, `BIG_IDEA_SUBTITLE`, `BIG_IDEA_P1/2/3` (depuis pitch.md, suivre `editorial-patterns.md`)
- `CONCEPT_H2`, `CONCEPT_P1/2/3` (idem)
- Titres simples : `IDENTITY_TITLE`, `PALETTE_TITLE`, `TYPO_TITLE`, `PHOTO_TITLE`

**Section Système — sous-titres / captions (~10 slots)** :
- `ICONOGRAPHY_SUBTITLE` : toujours `"Outline canonique · Solid pour le CTA · Duotone pour l'état actif."` (sanctuarisé)
- `ICONOGRAPHY_SUB_TITLE` / `UI_SUB_TITLE` / `DATAVIZ_SUB_TITLE` / `COMPOSITION_SUB_TITLE` + leurs captions (rédigés depuis design-specs §06 / §07)
- `COMPOSITION_GRID_DEMO` : HTML libre composé par toi pour la sous-section 06d Composition (pas d'extract automatique — la grille canonique est déduite de design-specs.md). Tu peux y mettre une grille SVG simple ou des blocs `<div>` avec annotations breakpoints.

**Section 07a Web (2 slots)** : `WEB_TITLE`, `WEB_CAPTION`

**Section 07b Pitch Deck (2 slots)** : `PITCH_DECK_TITLE`, `PITCH_DECK_SUBTITLE` (rédigés depuis pitch.md). Les 6 PNG sont déjà référencés en chemins relatifs `pitch-deck-mini/slide-01-cover.png` … `slide-06-icon-grid.png` dans le template — tu n'as PAS à les fournir, ils sont en dur.

**Section 07c Réseaux sociaux (3 slots)** : `SOCIAL_TITLE`, `SOCIAL_SUBTITLE`, `COLOR_CELL_LINKEDIN` (couleur beige claire chaude DISTINCTE du fond Brume du body — règle de dérivation détaillée plus bas dans le SKILL.md §MAPPING MUSTACHE 07c).

**Closing (2 slots)** : `CLOSING_STATEMENT`, `CLOSING_VISUAL`

#### 4.3 — Écrire le fichier `template-vars.json`

Écrire dans `{output_dir}/template-vars.json` un objet JSON `{clé → valeur}` où chaque clé est le nom du slot SANS les `{{}}`. Exemple :

```json
{
  "BRAND": "les-vermeil",
  "VERSION": "v1",
  "PITCH_DECK_TITLE": "Le relevé, en six planches.",
  "PITCH_DECK_SUBTITLE": "Deck commercial · 6 slides · ratio 16:9",
  "COLOR_1_ROLE": "Fond profond", "COLOR_1_NAME": "Bocage", "COLOR_1_HEX": "#1a2a18",
  "IDENTITY_CARD_ICONS_4": "<svg ...>...</svg> <svg ...>...</svg> <svg ...>...</svg> <svg ...>...</svg>",
  "...": "..."
}
```

**Cas particuliers pour les valeurs HTML** (slots qui prennent du markup, pas du texte) :
- `IDENTITY_CARD_ICONS_4` : string contenant 4 SVG 32px concaténés (les 4 icônes signature de la marque, extraites de batch2)
- `DATAVIZ_SIGNATURE_SVG` : string contenant 1 SVG bar chart composé
- `COMPOSITION_GRID_DEMO` : HTML libre pour la sous-section composition
- `GOOGLE_FONTS_LINK` : balise `<link>` complète

Échapper les guillemets internes (`"` → `\"`) selon le standard JSON. Le script `render-brand-book.py` valide le JSON avant substitution — si malformé, erreur claire avec la ligne en faute.

**Quality gate Étape 4** : `template-vars.json` doit contenir au minimum `BRAND`, `VERSION`, les 22 tokens design, et tous les slots de l'Identity Card v4 (sinon le bento s'affichera dégradé). Si un slot manque, le script le surfacera en Étape 4bis.

### Étape 4bis — Substitution mécanique via `render-brand-book.py` (sanctuarisée v6 — 30 mai 2026)

Une fois `template-vars.json` écrit en Étape 4, lancer le script :

```bash
python3 .claude/skills/brand-book/scripts/render-brand-book.py \
  .claude/skills/brand-book/ref/template-base.html \
  "{output_dir}/template-vars.json" \
  "{output_dir}/{brand}-brand-book.html" \
  --batch2-inventory "{output_dir}/{brand}-batch2-inventory.html"
```

Le script fait :
1. Lit le template + le JSON + l'inventory.
2. Pour chaque slot `{{VAR}}` du template : remplace par la valeur correspondante du JSON.
3. Pour les 8 slots `{{BATCH2_INVENTORY_*}}` : injection automatique des `<article>` depuis l'inventory (catégorie correspondante), commentaires `BEGIN_BLOCK md5=… / END_BLOCK` préservés.
4. Vérifie qu'aucun slot ne reste non substitué (sinon `[FAIL]`).
5. Écrit le brand book final.

**Sortie attendue OK** :
```
[INFO] Slots dans template : 102 uniques
[INFO] Variables fournies  : 94
[INFO] Injection auto batch2-inventory : 8 slots remplis
[OK]   Substitutions   : 115
[OK]   Brand book écrit : {output_dir}/{brand}-brand-book.html (~110 Ko, ~2200 lignes)
```

**Sortie possible avec slots manquants** (mode non-strict par défaut — les slots manquants deviennent `[MISSING:VAR_NAME]` visibles dans le brand book) :
```
[WARN] N slot(s) du template sans valeur dans vars.json :
         · {{COMPOSITION_GRID_DEMO}}
         · {{BIG_IDEA_P3}}
```

Si des slots sont marqués `[MISSING:…]` dans le brand book final → retourner sur l'Étape 4, enrichir `template-vars.json` avec les valeurs manquantes, relancer 4bis.

**Mode strict** : `--strict` ajouté → un slot manquant = exit 1. Utile pour valider que toutes les valeurs sont produites avant rendu. **Recommandé** une fois que tu es sûr d'avoir fourni tous les slots requis.

### Étape 5 — Vérification et ouverture

1. Vérifier que le fichier HTML est syntaxiquement valide (pas de tag non fermé évident)
2. Vérifier que toutes les images référencées existent :
   - `visual-final/*.png` (cover, closing, hero, atmospheres…) — y compris le hero référencé par `.bv4-cover` du bento Identity Card v4
   - `{brand}-landing-fullpage.png` (section 08a)
   - `pitch-deck-mini/slide-01-cover.png` à `slide-06-icon-grid.png` (section 08b — 6 fichiers)
   - `{brand}-linkedin-mockup.png` + `{brand}-x-mockup.png` (section 08c)
3. Vérifier que les 4 SVG icônes du bento Identity Card v4 sont rendues (regarder `.bv4-icongrid__row` dans le HTML — doit contenir 4 `<div class="bv4-icongrid__cell">` non vides, chacun avec un `<svg>` 32px)
4. Vérifier que la dataviz du bento (`.bv4-dataviz__viz`) contient un `<svg>` valide (pas un placeholder vide)
5. Vérifier que la palette du bento (`.bv4-palette`) contient bien **6 blocs** `<div class="bv4-palette__bloc ...">` non vides (rôle + nom + hex)
6. Vérifier que le wordmark enrichi (`.bv4-wordmark`) contient les 3 zones : overline, wordmark center, signature (2 lignes mono)

7. **QUALITY GATE FIDÉLITÉ BATCH2 — MÉCANIQUE HASH MD5 (sanctuarisée v5 / 30 mai 2026 — remplace l'ancien comptage Bash)** :

   La fidélité 1:1 est garantie par hash MD5 strict. Le script `verify-md5-fidelity.py` lit le manifest JSON produit Étape 2.5 et vérifie que CHAQUE hash attendu est présent dans le brand book final + que le contenu re-hashé match.

   ```bash
   INVENTORY_JSON=".claude/skills/brand-book/outputs/{brand}-test-v{N}/{brand}-batch2-inventory.json"
   BRANDBOOK=".claude/skills/brand-book/outputs/{brand}-test-v{N}/{brand}-brand-book.html"

   python3 .claude/skills/brand-book/scripts/verify-md5-fidelity.py "$INVENTORY_JSON" "$BRANDBOOK"
   ```

   **Sortie attendue OK** :
   ```
   [INFO] Attendus    : N blocs sur 11 catégories
   [INFO] Trouvés     : N blocs dans le brand book
   [OK]   Fidélité 1:1 verbatim vérifiée — N blocs présents et intacts.
   ```

   **Sortie possible FAIL** (exemples) :
   ```
   [FAIL] M bloc(s) ATTENDU(S) absent(s) du brand book :
            · abc123…  (icons)
            · def456…  (buttons)
   ```
   ou
   ```
   [FAIL] X bloc(s) ALTÉRÉ(S) (hash annoncé ≠ hash recalculé) :
            · annoncé=abc123  recalculé=ff9988
   ```

   **Action en cas de FAIL** :
   1. Relire la liste des MD5 manquants / altérés (regroupés par catégorie).
   2. Relancer **UNIQUEMENT le sub-agent de génération HTML (Étape 4)** avec un prompt enrichi :
      « Le quality gate Étape 5 a détecté que les blocs MD5 suivants ne sont pas présents (ou ont été altérés) dans le brand book : `<liste>`. Ces blocs viennent de `{brand}-batch2-inventory.html` (catégories `<X>`). Cherche-les via `<!-- BEGIN_BLOCK md5=<hash> -->`, copie-les VERBATIM dans la sous-section appropriée du brand book, et régénère le HTML. Ne modifie AUCUN caractère à l'intérieur des blocs. »
   3. Re-run quality gate. Si toujours FAIL après 2 itérations : escalade humaine (patch direct du HTML par l'utilisateur).

   **Cette mécanique remplace définitivement** l'ancien comptage Bash (`grep -c '<button'` etc.) qui était insuffisant : il pouvait passer alors que le sub-agent avait redessiné les composants en plus simple (le compte était bon mais la fidélité absente). Le hash MD5 verrouille la fidélité au caractère près.

8. Ouvrir le résultat dans le navigateur :
   ```bash
   open ".claude/skills/brand-book/outputs/{brand}-test-v{N}/{brand}-brand-book.html"
   ```
9. Reporter à l'utilisateur : nombre de sections produites, anomalies détectées, fichiers manquants, taille totale du brand book, **résultats du quality gate fidélité batch2 (compte par catégorie)**.

---

## MAPPING MUSTACHE 07c — Sources des données pour les templates LinkedIn + X

> **NOTE numérotation** : eyebrow affiché "07c" (après retrait Voice & Tone). Préfixe CSS conservé `.s08c-*` (sanctuarisé pour ne pas casser les feuilles existantes).

Les 2 templates `ref/linkedin-profile-mockup.html` et `ref/x-profile-mockup.html` contiennent des placeholders `{{...}}` substitués Étapes 2b et 2c. Voici d'où chaque variable est tirée :

### Variables communes (LinkedIn + X)

| Mustache | Source | Exemple Camille |
|----------|--------|-----------------|
| `{{BRAND_NAME}}` | `{brand}-design-specs.md` §00 (nom marque, souvent en bas-de-casse) | `camille.` |
| `{{BRAND_DISPLAY}}` | Style-tile `:root --brand-display` | `'Gloock', serif` |
| `{{BRAND_BODY}}` | Style-tile `:root --brand-body` | `'JetBrains Mono', monospace` |
| `{{BRAND_DARK_BG}}` | Style-tile `:root --brand-dark-bg` ou `--color-abyss` | `oklch(0.13 0.025 250)` |
| `{{BRAND_ACCENT_COLOR}}` | Style-tile `:root --brand-color-accent` (le point du wordmark) | `oklch(0.72 0.16 60)` |
| `{{BRAND_PRIMARY_FONT_URL}}` | Style-tile `<link>` Google Fonts du display | `https://fonts.googleapis.com/css2?family=Gloock&display=swap` |
| `{{COVER_IMAGE_URL}}` | `visual-final/{brand}-c{N}-{paletteID}-hero.jpg` (chemin relatif depuis le mockup HTML) | `visual-final/camille-c3-paletteA-hero.jpg` |

### Variables spécifiques LinkedIn

| Mustache | Source | Exemple Camille |
|----------|--------|-----------------|
| `{{WORDMARK_OVERLAY_HTML}}` | Composé : `<div class="camille-wordmark">{brand}<span class="accent">.</span></div>` + CSS inline pour positionner en bas-droit cover. Réutiliser le style wordmark déjà calé dans le style-tile. | `<div class="camille-wordmark">camille<span class="accent">.</span></div>` |
| `{{PROFILE_AVATAR_HTML}}` | Composé : `<div class="camille-avatar-mark">{Initiale}.</div>` avec le CSS `camille-avatar-mark` (font display + accent sur le point) | `<div class="camille-avatar-mark">J.</div>` |
| `{{TAGLINE}}` | `{brand}-pitch.md` §1 (la phrase signature courte du concept) | `Le Phare de Ralliement` |
| `{{META_SECTOR}}` | `{brand}-design-specs.md` §00 (industrie/secteur) | `Conseil en positionnement` |
| `{{META_CITY}}` | `{brand}-design-specs.md` §00 (ville HQ) ou défaut "Paris, France" | `Paris, France` |
| `{{META_FOLLOWERS}}` | Valeur plausible cohérente avec la taille marque (10-50 employés → 1-5K followers). Par défaut `"2K followers"`. | `2K followers` |
| `{{META_EMPLOYEES}}` | `{brand}-design-specs.md` §00 (taille équipe) ou valeur plausible | `2-10 employees` |

### Variables spécifiques X

| Mustache | Source | Exemple Camille |
|----------|--------|-----------------|
| `{{AVATAR_HTML}}` | Composé : `<div class="camille-avatar-mark">{Initiale}<span class="accent">.</span></div>` | `<div class="camille-avatar-mark">J<span class="accent">.</span></div>` |
| `{{COVER_OVERLAY_HTML}}` | Vide par défaut (`""`). Optionnel : wordmark overlay si la cover hero est très sombre et la marque a un wordmark spécifique pour le réseau social. | `""` |
| `{{HANDLE}}` | Composé : `@{brand_slug}_studio` ou `@{brand_slug}` (snake-case du nom marque) | `@camille_studio` |
| `{{POSTS_COUNT}}` | Valeur plausible (`"12"` à `"2,4 k"` selon taille marque). Par défaut `"12"`. | `12` |
| `{{BIO}}` | `{brand}-pitch.md` §1 condensé (1-2 phrases ~140 caractères avec coordonnées géographiques si pertinent) | `Le phare de ralliement des fondateurs en perte de repères. Conseil en positionnement de marque. 47°57'N · 5°06'W.` |
| `{{META_CATEGORY}}` | Identique `{{META_SECTOR}}` LinkedIn | `Conseil en positionnement` |
| `{{META_LOCATION}}` | Identique `{{META_CITY}}` LinkedIn | `Paris, France` |
| `{{META_URL}}` | Site web marque (`{brand_slug}.studio` ou `{brand_slug}.com` par défaut) | `camille.studio` |
| `{{META_BIRTHDAY}}` | `{brand}-design-specs.md` §00 (date de création) ou défaut récent | `Mis en service · 1863` |
| `{{META_JOINED}}` | Date plausible de création du compte X (souvent année courante) | `A rejoint X en 2026` |
| `{{STATS_FOLLOWING}}` | Valeur plausible (50-300) | `142` |
| `{{STATS_FOLLOWERS}}` | Valeur plausible (100-5000) | `2 387` |
| `{{FOLLOWED_BY}}` | Phrase type `"Suivi par {Personne 1}, {Personne 2} et {N} autres relations"` | `Suivi par Pierre Vasseur, Marie Dupont et 3 autres relations` |

### Règle de dérivation `{{COLOR_CELL_LINKEDIN}}`

La couleur de fond de la cellule LinkedIn doit être un **beige clair chaud** distinct du fond Brume de la page (`--brand-color-positive-bg`, souvent bleu-gris clair). Règle :

```
oklch(0.92 0.025 H)  où H = hue de --brand-color-accent
```

Pour Camille (accent hue ≈ 60 orange) → `oklch(0.92 0.025 78)` (légèrement décalé pour ne pas trop tirer vers l'orange).
Pour une marque avec accent vert (hue 145) → `oklch(0.92 0.025 100)` (légèrement vert pâle).

L'objectif : un beige clair en harmonie chromatique avec l'accent, mais désaturé pour rester un fond neutre.

### Règles de composition `WORDMARK_OVERLAY_HTML` / `AVATAR_HTML`

Reprendre les classes CSS du style-tile pour le wordmark (par ex `.camille-wordmark`, `.camille-avatar-mark`). Si le style-tile a une signature wordmark différente (ex: monogramme custom, lockup combiné), composer l'HTML en cohérence. **Toujours utiliser `--brand-display` pour la font et `--brand-accent` pour le point final ou l'élément accentué**.

---

## CONVENTIONS DE NOMMAGE

- **Dossier output** : `{brand}-test-v{N}/` (toujours `test-vN` tant que le skill n'est pas branché à BIG)
- **Brand book HTML** : `{brand}-brand-book.html`
- **Capture style-tile** : `{brand}-landing-fullpage.png`
- **Visuels finaux** : conservés sous leur nom canonique BIG (`{brand}-c{N}-{paletteID}-{type}-{variante}.{ext}`)

Voir aussi : feedback Charles `feedback_visual_final_convention.md` (mémoire de session).

---

## RÈGLES NON-NÉGOCIABLES

1. **Tokens canoniques de la marque, jamais de valeurs génériques** : palette oklch exacte, fonts exacts, radius exact (souvent `--radius-xs: 2px`), wordmark `{brand}.` avec le point final en couleur d'accent.
2. **Pas de pur noir #000 ni de pur blanc #FFF** : utiliser les Nuit d'Indigo / Brume de Plan / équivalents définis par la marque.
3. **Pas d'iframe pour la section 08** : capture PNG obligatoire.
4. **Pas de `box-shadow: 0 0 Npx`** sans offset directionnel (toujours une direction).
5. **Halos radial-gradient asymétriques uniques** (pas centrés en `50% 50%`).
6. **Respecter les don'ts** explicités dans le §12 de `{brand}-design-specs.md` (clichés à éviter spécifiques à la marque).
7. **Slide rythm** : une section = une page éditoriale de hauteur ~720-900px. Exceptions assumées : section 08 (PNG long-scroll) + section 07 (peut être plus longue à cause des 4 sous-blocs).
8. **Mode immersif vs grille** : palette, typo → 1 page COMPOSÉE (toute la palette/typo sur 1 page, pas 1 atome = 1 page). UI, charts, icônes, composition → tous côte à côte.
9. **Hiérarchie typographique FIGÉE** (voir `style-guide.md` §4bis) : utiliser EXCLUSIVEMENT les variables `--type-*` et les classes utilitaires `.section__eyebrow`, `.section__title`, `.section__subtitle`, `.section__body`, `.caption`, `.pull-quote`, `.big-number`, `.mono`. **Pas de tailles inline** (`style="font-size: ..."`). Les tailles des titres NE varient PAS d'une section à l'autre.
10. **Slide rythm 720-900px** par section. Exceptions assumées : Cover/Closing (100vh), 07a Web (PNG long ~1200-1600px), 07b Pitch Deck (spread ~1300px), 07c Réseaux sociaux (diptyque ~1100px). 06 Système est éclaté en 4 slides successives 06a/b/c/d, chacune ~720-900px.
11. **Contraste minimum de séparation — palette only stricte** (sanctuarisée 27 mai 2026) : tout bloc visible (card, tuile, panneau) doit être chromatiquement distinct de son conteneur parent (≥ 8-10 points lightness en oklch, OU hue différent, OU chroma ≥ 0.02 d'écart). **La couleur de contraste DOIT obligatoirement être une couleur de la palette canonique de la marque** (accessible via `var(--color-*)` ou `var(--brand-color-*)`). **AUCUNE COULEUR INVENTÉE n'est tolérée** — même si elle "matche le ton". Anti-pattern interdit : un bloc avec `background: var(--brand-color-positive-bg)` enfant d'une section qui a déjà ce fond → bloc invisible. Anti-pattern PIRE : `background: oklch(0.92 0.025 78)` (couleur ad-hoc inventée) → pollue l'identité chromatique du brand book. Si aucune couleur palette ne crée un contraste suffisant, basculer sur une teinte sombre de la palette (Marine Cliff, Nuit Claire, Abyss) avec texte clair. **Exception "spécimen sur fond natif"** : autorisée uniquement quand on documente l'élément sur sa couleur d'usage réelle (lockup sur fond Brume dans 04 Identité). Dans ce cas, bordure 1px subtile + commentaire HTML `<!-- mode spécimen : fond natif d'usage -->` obligatoire. Détails complets : `style-guide.md` §8bis.
12. **Fidélité au pack source — mécanique EXTRACT-THEN-INJECT v5** (sanctuarisée 30 mai 2026 — remplace l'ancien comptage déclaratif du 27 mai) : pour les sous-sections **Iconographie / Composants UI / Data viz** de la section Système, le brand book DOIT injecter VERBATIM les blocs HTML extraits par `scripts/extract-batch2-inventory.py` (Étape 2.5) dans les slots `{{BATCH2_INVENTORY_*}}` du template. **Aucune redessination de composant UI / icône / chart autorisée.** Le quality gate Étape 5 (`verify-md5-fidelity.py`) bloque la livraison si un bloc attendu manque ou a été altéré (hash MD5 strict, au caractère près). La règle textuelle de comptage manuel reste comme garde-fou conceptuel mais est **subordonnée** à cette mécanique. Bug que cette règle empêche : Atelier Vermeil 30/05/2026 — 28 SVG `viewBox 64×64` avec hachures `url(#hatch-cross)` redessinés en 20 SVG `32×32` plats `currentColor`, 4 badges + 4 toggles oubliés (déclaratif insuffisant). Détails complets : `style-guide.md` §8quater + Étape 2.5 + Étape 4 (bloc « RÈGLE EXTRACT-THEN-INJECT » en tête).

---

## CE QUI N'EST PAS DANS CE SKILL (encore)

### Sous-blocs Applications 07 — état au 27 mai 2026

| Sous-bloc | Statut |
|-----------|--------|
| **07a Web** | ✅ Branché (Étape 2a — capture style-tile) |
| **07b Pitch Deck** | ✅ Branché (Étape 2d — sous-skill SPG `generate-mini-deck`) |
| **07c Réseaux sociaux** | ✅ Branché (Étapes 2b + 2c — templates LinkedIn + X + captures) |
| **07d Bento Grid** | ❌ Pas implémenté (template à créer — vitrine condensée de personnalité brand) |

### Intro Identity Card (00) — état au 27 mai 2026

| Élément | Statut |
|---------|--------|
| **00 Identity Card (bento intro)** | ✅ Branché (Étape 2e — composition Mustache, sanctuarisé 27 mai 2026) |

### Autres
- Pas de branchement automatique depuis le pipeline BIG (`/brand-identity` ne l'appelle pas — étape suivante du chantier)
- Pas de skill miroir `test-brand-book` pour reprendre à mi-parcours
- Pas d'animation GSAP / interaction au scroll (sobriété volontaire pour v1)
- Pas d'export PDF (le brand book reste HTML, l'export PDF se fait via le navigateur)

### Skipés par décision (validés)
- Mockup mobile (sauf si ICP = app)
- Stats outcome chiffrées (impossible sans données client réelles)
- Lifestyle photo humain (hors capacité BIG)
- Mascot 3D (hors capacité BIG)

Ces points seront ajoutés une fois le skill validé sur 2-3 marques.
