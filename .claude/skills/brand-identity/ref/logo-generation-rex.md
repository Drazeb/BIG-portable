# REX — Génération de Logo dans le pipeline BIG

*Retour d'expérience du test Atelier Vermeil × SOLSTICE (février 2026). Ce document est destiné à la session qui implémentera la phase Logo dans SKILL.md.*

---

## 1. RÉSUMÉ EXÉCUTIF

La phase Logo s'insère **entre la Phase 5 (choix du concept) et la Phase 6A (Batch 2)**. Elle produit le mark SVG + toutes ses déclinaisons, qui alimentent ensuite le Batch 2 (section 05 — Logotype & Morphologie du Signe).

**Workflow validé** : Concept stratégique (Claude) → Prompts IA (Claude) → Génération image (Midjourney) → Tests & ajustements (utilisateur) → Upscale (Midjourney) → Vectorisation SVG (Claude Code) → Déclinaisons complètes (Claude Code).

**Conclusion principale** : Claude Code gère 80% du travail (concept, prompts, vectorisation, déclinaisons). L'utilisateur intervient sur la partie génération image (Midjourney) car c'est interactif et visuel. Recraft est inadapté pour la génération de lettermarks complexes.

---

## 2. CE QUI MARCHE / CE QUI NE MARCHE PAS

### 2.1 Recraft — Inadapté pour les lettermarks bicolores

**Testé exhaustivement** : 8+ rounds, 5+ styles, 3 niveaux d'artistic level, prompts courts et longs.

**Problème fondamental** : Recraft ne comprend pas les instructions compositionnelles complexes. Quand on demande "un A bicolore split gauche/droite", il produit :
- Des tangrams (carrés coupés en diagonale)
- Des motifs géométriques abstraits (papillons, croix, losanges)
- Des A monochromes avec accent d'une autre couleur
- Des blocs rectangulaires côte à côte

**Styles testés et résultats** :

| Style Recraft | Résultat | Verdict |
|---------------|----------|---------|
| Geometric Logo | Gradients systématiques, cadre carré forcé | **NON** |
| Vector art (V3) | Trop illustratif/libre (lobsters, origami) | **NON** |
| Minimal Vibrant Logo | Le meilleur pour les aplats. Mais ne résout pas le problème compositionnel | **PARTIEL** |
| Shape Stack Logo | Formes empilées, pas de letterform | **NON** |
| Typographic Logo | Non testé en détail (devrait être testé pour les wordmarks purs) | **À TESTER** |
| Tous styles × Artistic level bas | Aucune amélioration du respect du prompt | **NON** |

**Prompts courts vs longs** :
- Courts (2-3 lignes) → résultats plus propres mais toujours le même problème compositionnel
- Longs (10+ lignes ultra-directifs) → résultats PIRES. Recraft prend chaque mot littéralement ("parallelogram bars" → dessine des parallélogrammes au lieu d'un A)

**Quand Recraft EST utile** :
- Vectorisation d'images raster (outil Vectorize)
- Génération d'icônes simples et de patterns
- Export SVG natif
- **Phase 3C** : Recraft V4 recommandé pour illustrations flat/2D (I1), line art (I2) et infographiques (I7) — SVG natif, lignes nettes, couleurs maîtrisées
- Mais ATTENTION : la vectorisation auto-trace produit des tracés sur-complexes avec des couleurs dérivées. Claude Code fait mieux en SVG manuel pour les formes géométriques simples.

### 2.2 Midjourney — Excellent pour les lettermarks

**Midjourney comprend les intentions compositionnelles** là où Recraft échoue. Dès le premier prompt, MJ a produit 4 résultats exploitables avec un A bicolore split gauche/droite.

**Settings optimaux MJ** :
- `--ar 1:1` (carré)
- `--stylize 50` (bas = plus littéral, suit mieux le prompt)
- `--no` pour le negative prompt (équivalent Recraft)

**Structure de prompt qui fonctionne** :
```
Bold geometric letter A logo, split vertically down the center,
left half solid flat navy blue #1A1A2E, right half solid flat
terracotta #E2725B, sharp angular construction, white triangular
negative space where crossbar would be, minimalist logo design,
flat vector style, no gradients, clean white background
--ar 1:1 --stylize 50
--no gradient shadow 3d photorealistic leaf tree circle alchemy
rounded mountain diamond pattern
```

**Points clés du prompting MJ pour logos** :
1. Décrire la FORME résultante, pas la construction géométrique
2. Spécifier les couleurs avec les hex codes
3. Inclure "flat vector style" et "minimalist logo design"
4. Le `--stylize` bas (50) est crucial — sinon MJ prend trop de libertés
5. Le negative prompt (`--no`) est important pour éviter les dérives

**Itération dans MJ** :
- `Vary (Subtle)` → quasi-identique, peu utile pour les logos (trop proche)
- `Vary (Strong)` → produit des variations exploitables
- `Upscale 4x` → qualité suffisante pour vectorisation

### 2.3 Claude Code — Excellent pour vectorisation + déclinaisons

**Vectorisation via vtracer** (méthode validée — voir `ref/logo-vectorization-rex.md`) :
L'écriture manuelle de paths SVG par le LLM échoue systématiquement sur les formes organiques (3 tentatives documentées). La méthode fiable est `vtracer` (auto-trace) + post-processing en 5 étapes par l'orchestrateur.

**Lockups via `<svg>` imbriqué** (méthode validée — voir `ref/logo-lockup-rex.md`) :
NE JAMAIS utiliser `<g transform="scale(...)">` sur des paths vtracer. Utiliser un `<svg>` imbriqué avec tight viewBox calculé.

**Limites** : vtracer gère 80% des cas. Pour les formes géométriques pures, l'écriture manuelle reste possible. Pour les logos avec dégradés complexes, orienter vers vectorisation externe (Figma/Illustrator).

**Déclinaisons SVG** :
Claude Code génère instantanément toutes les variantes en modifiant les attributs `fill` des polygones :
- Bicolore (original)
- Négatif (fond sombre — adapter la couleur de la jambe qui disparaît)
- Monochrome navy
- Monochrome blanc
- Lockup primaire (vertical — mark + nom centré en dessous)
- Lockup secondaire (horizontal — mark + nom à droite)

**Points d'attention pour les lockups** :
- Le texte utilise la font display de la brand via `@import` Google Fonts → nécessite une connexion internet pour le rendu
- Pour production print, le texte doit être converti en outlines (Figma/Illustrator)
- Proportions lockup : le mark doit faire **1.5-2× la cap-height du texte**, pas plus. Erreur fréquente : mark trop grand par rapport au texte
- Aligner la baseline du texte avec la base du mark (pas le centre géométrique)

---

## 3. PROCESS PROPOSÉ — PHASE LOGO

### Position dans le pipeline

```
Phase 3 : Pitch (3 concepts)
Phase 4 : Style-Tiles HTML (3 en parallèle)
Phase 5 : Itération + choix du concept
  └─ Phase 5C : Slugification + nommage fichiers

  ══════════════════════════════════════════
  ► PHASE LOGO (NOUVELLE) ◄
  ══════════════════════════════════════════

Phase 6A : Batch 2 (intègre le logo SVG produit)
```

### Étapes détaillées

#### Étape L1 — Concept stratégique (subagent Claude)

**Input** : Brief, scoping (tension), pitch du concept choisi, :root du style-tile
**Output** : Fichier `{brand}-logo-concept-{slug}.md`

Le subagent utilise les frameworks de `ref/logo-design-bible.md` :
- §3 Le Pont (métaphore) → trouver le concept de logo
- §4 Archétype (Creator, Explorer, etc.)
- §5 Sémiotique de Peirce (Icône, Index, Symbole)
- §6 Grille Paul Rand /75
- §8 Scoring pondéré /100
- §13-15 Anti-patterns (IA tells, clichés secteur, biais LLM)
- §20-22 Templates par type de logo
- §26 Indexation curseurs

**Structure du fichier de sortie** (validée par test) :

```markdown
# LOGO — {Brand} × {CONCEPT}

> 1 concept de logo, 3 prompts à tester dans Midjourney.

## PARTIE 1 — LE CONCEPT
- Nom du concept
- L'idée en une phrase
- Pourquoi cette idée (lien avec la tension)
- 3 niveaux de lecture
- Ce que le logo N'EST PAS (anti-patterns)

## PARTIE 2 — PROMPTS MIDJOURNEY
### Prompt 1 — PRINCIPAL
- Prompt complet (copier-coller)
- Settings MJ (--ar, --stylize, --no)
### Prompt 2 — VARIANTE
### Prompt 3 — VARIANTE

## PARTIE 3 — SCORE PRÉDICTIF
- Grille Paul Rand /75 (seuil : 60)
- Scoring pondéré /100 (seuil : 75)

## ANNEXE — Travail stratégique
<details> (collapsible)
- Archétype, sémiotique, shape language
- Checklist anti-patterns
- Master Template
</details>
```

**Règles de prompting MJ pour le subagent** :
1. Toujours inclure `--ar 1:1 --stylize 50` dans les settings
2. Prompt ≤ 5 lignes, descriptif de la forme résultante
3. Inclure les hex codes des couleurs du :root
4. Inclure `flat vector style, no gradients, minimalist logo design, clean white background`
5. Negative prompt avec `--no` : gradient, shadow, 3d, photorealistic + clichés secteur + biais IA (hub branches, swoosh, orb)
6. Ne JAMAIS décrire la construction géométrique (éviter "parallelogram", "trapezoid")
7. Décrire ce qu'on VOIT, pas comment c'est construit

#### Étape L2 — Génération image (utilisateur dans Midjourney)

**Input** : Prompts du fichier concept
**Output** : Image PNG upscalée du logo retenu

L'orchestrateur présente les prompts et guide l'utilisateur :

```
📐 **Phase Logo — Génération dans Midjourney**

J'ai préparé 3 prompts dans le fichier concept. Voici le process :

1. Copie le **Prompt 1** dans Midjourney (c'est le principal)
2. Partage-moi la grille de résultats — je t'aide à choisir
3. Si aucun résultat ne convient, passe au Prompt 2 puis au 3
4. Quand un résultat te plaît :
   - **Vary (Strong)** pour explorer des micro-variations
   - **Upscale 4x** sur le gagnant final
   - Télécharge le PNG et envoie-le-moi

Je m'occupe ensuite de la vectorisation et des déclinaisons.
```

**Boucle d'itération** :
- L'utilisateur partage un screenshot → l'orchestrateur analyse et recommande
- Si aucun prompt ne donne de bon résultat → l'orchestrateur affine le prompt en s'appuyant sur les learnings (voir section 2)
- Maximum 3-5 rounds de génération avant de pivoter (changer de type de logo : abstract mark → lettermark → wordmark)

#### Étape L3 — Vectorisation (Claude Code)

**Input** : Image PNG upscalée envoyée par l'utilisateur
**Output** : SVG propre dans `{session_dir}/`

Process de Claude Code :
1. L'utilisateur fournit le chemin du fichier PNG (ou le dépose dans le dossier session)
2. Claude Code analyse la géométrie (Read de l'image ou, si disponible, auto-trace Recraft comme base de coordonnées)
3. Claude Code recrée le SVG manuellement avec :
   - Polygones/paths minimaux
   - Couleurs exactes du :root (`--color-primary`, `--color-depth`, etc.)
   - Fond transparent
   - Titre `<title>` pour accessibilité
4. Ouvre le SVG dans Chrome pour validation utilisateur

**Fichier** : `{session_dir}/{brand}-logo-{slug}.svg`

#### Étape L4 — Déclinaisons (Claude Code)

**Input** : SVG validé par l'utilisateur
**Output** : 6 fichiers SVG

| Fichier | Description | Couleurs |
|---------|-------------|----------|
| `{brand}-logo-{slug}.svg` | Bicolore original | Couleurs du concept |
| `{brand}-logo-{slug}-negatif.svg` | Sur fond sombre | Fond `--color-depth`, adapter les couleurs qui disparaissent (utiliser `--color-surface` ou blanc) |
| `{brand}-logo-{slug}-mono-navy.svg` | Monochrome sombre | Toutes les formes en `--color-depth` |
| `{brand}-logo-{slug}-mono-blanc.svg` | Monochrome clair | Toutes les formes en `#FFFFFF` |
| `{brand}-logo-{slug}-lockup-primaire.svg` | Mark + nom (vertical) | Mark bicolore + texte en `--color-depth` |
| `{brand}-logo-{slug}-lockup-secondaire.svg` | Mark + nom (horizontal) | Mark bicolore + texte en `--color-depth` |

**Règles des lockups** :
- Font : `--font-display` de la brand (via `@import` Google Fonts)
- Texte en `--color-depth`
- Proportions : mark = 1.5-2× la cap-height du texte
- Lockup horizontal : baseline du texte alignée avec la base du mark
- Lockup vertical : mark centré horizontalement au-dessus du texte, gap = ~15% de la hauteur du mark

#### Étape L5 — Validation + passage au Batch 2

L'orchestrateur ouvre les 6 SVG dans Chrome et demande validation :

```
✅ **Logo — 6 déclinaisons générées**

Vérifie dans le navigateur :
1. Bicolore → proportions OK ?
2. Négatif → lisibilité sur fond sombre ?
3. Mono navy → reconnaissable sans la couleur ?
4. Mono blanc → idem ?
5. Lockup primaire → équilibre mark/texte ?
6. Lockup secondaire → idem ?

Si tout est bon, on passe au Batch 2 (Phase 6A) qui intégrera ce logo dans la section 05.
```

Le Batch 2 (Phase 6A) reçoit le SVG bicolore et le lockup comme inputs pour la section 05 du showroom (Logotype & Morphologie du Signe).

---

## 4. FICHIERS DE RÉFÉRENCE

| Fichier | Rôle |
|---------|------|
| `ref/logo-design-bible.md` | Frameworks conceptuels (§1-§27) — archétypes, sémiotique, scoring, anti-patterns, templates par type |
| `ref/logo-generation-rex.md` | Ce document — REX + process + learnings techniques |
| `ref/master-style-guide.md` | Section 05 — spécifications des livrables logo (lockups, zones d'exclusion, variantes) |

---

## 5. INTÉGRATION DANS SKILL.md

### Variables à ajouter

```
{logo_svg}         → chemin du SVG bicolore validé
{logo_lockup}      → chemin du lockup primaire SVG
{logo_concept_file} → chemin du fichier concept MD
```

### Modification du flow

Après Phase 5C (slugification) :
1. Lancer le subagent Phase Logo (concept + prompts)
2. Boucle interactive avec l'utilisateur (Midjourney)
3. Vectorisation + déclinaisons par Claude Code
4. Validation
5. Passer à Phase 6A avec `{logo_svg}` disponible

### Impact sur le Batch 2

La Phase 6A lit actuellement le style-tile pour en extraire les specs. Elle devra AUSSI lire le `{logo_svg}` pour :
- Intégrer le logotype SVG dans la section 05.1
- Montrer les lockups dans la section 05.2
- Définir les zones d'exclusion dans la section 05.3
- Afficher les variantes de contexte dans la section 05.4

---

## 6. CHECKLIST POUR L'IMPLÉMENTATION

- [ ] Ajouter la Phase Logo dans SKILL.md (entre Phase 5C et Phase 6A)
- [ ] Mettre à jour `ref/pipeline-overview.md` (nouvelle étape)
- [ ] Créer le prompt du subagent L1 (concept stratégique) avec injection des frameworks de `logo-design-bible.md`
- [ ] Implémenter la boucle interactive L2 (orchestrateur guide l'utilisateur dans MJ)
- [ ] Implémenter L3 (vectorisation) — Claude Code lit le PNG, recrée le SVG
- [ ] Implémenter L4 (déclinaisons) — génération des 6 variantes SVG
- [ ] Modifier le prompt Phase 6A pour qu'il lise `{logo_svg}` en plus du style-tile
- [ ] Tester le pipeline complet sur un nouveau cas

---

## 7. ANNEXE — EXEMPLE DE SESSION COMPLÈTE

Référence : session Atelier Vermeil × SOLSTICE (février 2026)

**Durée totale phase logo** : ~2h (dont ~1h30 d'exploration Recraft infructueuse)
**Durée estimée avec le process optimisé** : ~30-45 min

**Séquence réelle** :
1. Concept "La Faille Fertile" (subagent, ~5 min)
2. 3 rounds Recraft abstract mark → tangrams systématiques (abandonné)
3. Pivot lettermark A → 2 rounds Recraft → meilleur mais pas bicolore
4. Pivot Midjourney → résultat exploitable au round 1
5. Vary (Strong) → 8 variations, choix du gagnant
6. Upscale 4x dans MJ
7. Vectorisation via vtracer + post-processing par Claude Code (~2 min)
8. 6 déclinaisons SVG (dont lockups via `<svg>` imbriqué) par Claude Code (~3 min)

**Outputs produits** :
```
outputs/les-vermeil-0213-1343/
├── les-vermeil-logo-concept-solstice.md        (concept + prompts)
├── les-vermeil-logo-solstice.svg                (bicolore)
├── les-vermeil-logo-solstice-negatif.svg        (fond sombre)
├── les-vermeil-logo-solstice-mono-navy.svg      (mono navy)
├── les-vermeil-logo-solstice-mono-blanc.svg     (mono blanc)
├── les-vermeil-logo-solstice-lockup-primaire.svg    (vertical)
└── les-vermeil-logo-solstice-lockup-secondaire.svg  (horizontal)
```
