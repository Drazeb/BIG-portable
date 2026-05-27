# Passation — Session Arbitre Anti-Slop pour tests E2E BIG (3B → Phase 4)

> **Document de référence pour la session "arbitre"** qui va analyser les
> résultats des tests E2E BIG (Brand Identity Generator) lancés à partir de la
> Phase 3B et allant jusqu'à la Phase 4. Mission : juger si le chantier
> anti-slop fonctionne — détecter le slop résiduel, valider les chantiers,
> alerter sur les régressions.
>
> Cette session est **arbitre**, pas implémenteur. Elle ne modifie pas le
> code BIG. Elle reçoit des résultats (style-tiles HTML, palettes, fiches de
> style, pitchs) et produit un verdict structuré.

---

## 0. TL;DR

- BIG a subi un gros chantier anti-slop entre fin avril 2026 sur **Phase 4** (Vague 2 + 2.5) et **Phase 3B** (chantiers 1-2-3-4 commités, 5-6 statut variable).
- Le système anti-slop est **stratifié** : prompt N1/N2 + gates Python déterministes + critiques sémantiques.
- Source canonique des règles : **skill `/audit-slop`** (4 grilles, 19+ fichiers sources externes, ~212 règles brutes).
- 8 gates Python opérationnels couvrent les principaux carrefours.
- L'arbitre doit savoir : (a) toutes les règles, (b) où elles s'appliquent dans le pipeline, (c) comment lire un audit-slop final, (d) comment détecter slop résiduel.
- **Ce document est self-contained** — l'arbitre n'a pas besoin de fouiller le repo.

---

## 1. Mission de l'arbitre

### 1.1 Ce qu'on attend de toi

Quand Charles te transmet un résultat de test E2E (typiquement : un dossier de session BIG `outputs/test-{brand}-{label}/` avec ses 9 palettes, 9 fiches de style, 3 pitchs, 3 style-tiles HTML, et possiblement un audit-slop), tu dois :

1. **Identifier ce qui a été produit** (les artefacts du test, leur cohérence)
2. **Lancer ou interpréter les gates Python** sur chaque artefact pertinent
3. **Lancer ou interpréter le skill `/audit-slop`** sur les style-tiles HTML finaux
4. **Détecter le slop résiduel** : règles qui auraient dû être bloquées mais qui sont passées
5. **Produire un verdict structuré** : par carrefour, par règle, avec sévérité
6. **Comparer avec les baselines** (sessions de référence pré-anti-slop)
7. **Alerter** si tu détectes une régression vs un chantier précédent

### 1.2 Ce que tu ne fais PAS

- Pas de modification de code BIG (pas d'Edit sur les prompts, scripts, SKILL.md)
- Pas de commit
- Pas de patches sur les gates (signaler à Charles si un gate semble cassé, sans le corriger)
- Pas de re-run du pipeline BIG (juste analyser ce qui est fourni)

### 1.3 Format du verdict attendu

```markdown
# Verdict arbitre — test {brand}-{label} ({date})

## Résumé exécutif
- Score anti-slop global : X/10 (calcul décrit en §6)
- Carrefours conformes : N/6
- Carrefours avec slop résiduel : liste
- Régressions vs chantiers précédents : liste (vide si aucune)
- Score audit-slop final HTML : X/10 (si audit-slop lancé)

## Détail par carrefour
[Sections détaillées]

## Slop résiduel détecté
[Liste avec localisation + sévérité + règle violée + référence canonique]

## Recommandations
[Pour Charles, sans implémenter]
```

---

## 2. Vue d'ensemble du chantier anti-slop BIG

### 2.1 Le problème slop

Les LLM produisent par défaut des outputs avec des **marqueurs slop AI** :
- **Chromatique** : `#000000`/`#ffffff` purs sur surfaces, AI purple/blue gradient (`#6366f1` style indigo Tailwind), aurora 3 blobs génériques, accent moins saturé que dominante
- **Typographique** : Inter / Roboto / Open Sans / Lato / Montserrat (les "invisibles"), Times / Georgia sans justification, mono-fonte sans contraste
- **Compositionnel** : 50/50 hero rigide, grid 3 cards identiques, 3 features icon+title+desc, footer 4 colonnes, hero centré avec CTA solo, hover qui monte (translateY)
- **Verbal** : filler words AI ("Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve"), fake names ("John Doe", "Acme", "Nexus", "SmartFlow"), justifications creuses
- **Animation/effet** : box-shadow glow sans offset, animation infinite décorative, glassmorphism par défaut, neumorphism, gradient text via background-clip

### 2.2 La grille audit-slop (référentiel canonique)

Le skill `/audit-slop` (`.claude/skills/audit-slop/SKILL.md`) est le **référentiel central**. Il audite un style-tile HTML BIG sur **4 grilles indépendantes** + 1 synthétiseur :

| Agent auditeur | Sources | Règles |
|---|---|---|
| **Craft Moderne** | Impeccable + Taste Skill (7 variantes) + GStack — 19 fichiers | ~130 règles |
| **Vercel Technique** | `vercel-command.md` | ~60 règles |
| **BIG Pipeline** | 10 fichiers BIG + 2 gates Python | ~80 règles |
| **Perplexity Temporel** | `perplexity-styles-datés-vs-actuels-2026.md` | ~85 styles + marqueurs datés |

Total brut : **~212 règles**. Après dédup : **~158 universelles** (HTML vanilla) + **~54 contextuelles** (React/Framer/Stitch — N/A pour BIG qui produit du HTML).

**Extraction consolidée** : `ref/extraction-vague2-2026-04-26.md` recense **182 règles distinctes** classées par destination (TIER_1, GATE_PYTHON, CRITIQUE_TIER_2, CRITIQUE_TIER_3, N_A_HTML_VANILLA).

### 2.3 Architecture stratifiée

Sur 2 niveaux de pipeline :

**Phase 4 (HTML produit, audité par audit-slop)** — Vague 2 finalisée 26 avril :
- **TIER 1** : ~28 règles structurantes injectées dans le prompt Designer Phase 4 (limite empirique : ~25-30, sinon sur-engineering observé)
- **Gates Python déterministes** : `phase4-blacklist-gate.py` (17 patterns datés grep-ables) + `phase4-finishing-gate.py` (8 checks Vague 1 + 33 checks Vague 2 WARN)
- **4 Critiques sémantiques** + 1 Synthétiseur : `phase-4check-{a11y,composition,typo-copy,craft,synthetiseur}.md` couvrent ~80 règles non-grep-ables

**Phase 3B (choix amont consommés par Phase 4)** — chantiers 1-6 :
- **Chantier 1** routeur chromatique 3B-0a
- **Chantier 2** palette 3B-3
- **Chantier 3** fonts 3B-1/3B-2
- **Chantier 4** styliste 3B-7a
- **Chantier 5** direction visuelle 3B-5 (statut variable — voir §3)
- **Chantier 6** pitch designer 3B Interaction 3 (statut variable — voir §3)

### 2.4 Convention de formulation 3 niveaux N1/N2/N3

**Référence canonique** : `ref/anti-slop-formulation-guide.md` (à connaître par cœur).

| Niveau | Forme | Risque | Verdict |
|---|---|---|---|
| **N1** Principe abstrait | `Do NOT center everything symmetrically` | Aucun | ✅ OK prompt |
| **N2** Pattern nommé non-substituable | `Do NOT use neumorphism` | Aucun | ✅ OK prompt |
| **N3** Énumération précise (fonts/hex/syntax) | `Do NOT use #6366f1`, `Do NOT use Inter` | **CONTAMINATION CRÉATIVE PROUVÉE** sur 17 tests | ❌ JAMAIS prompt — gate Python |

**Stratégie 3 (amont + aval) validée** : N1/N2 dans le prompt + N3 dans le gate Python. Tous les chantiers anti-slop respectent cette stratification.

**Clause anti-cousin** : pour les règles à risque de substitution proche (banni Inter → choisit Roboto), les listes vivent dans le code Python avec leurs cousins explicites.

---

## 3. État des chantiers anti-slop par carrefour (29 avril 2026)

### 3.1 Phase 4 — Vague 2 + Vague 2.5 + correctifs ✅

**Commits clés** :
- `eab5905` (26 avril) : Vague 2 architecture (4 Critiques parallèles + 80 règles + gates étendus)
- `d41bc7a` (27 avril) : refactor Phase 4 state machine + patches P3-P13 (anti-régression rollback, P4 backups, P7 pauses, P8 vrai parallélisme, P9 parse-blacklist, P10 pré-extraction :root, P11 pas de SendMessage)
- `d42acd4` (28 avril) : P14 — Designer correction par 3 passes de sévérité
- `f26846c` (28 avril) : P15 — extract-trace.py anti-pollution gates
- `e1c0b26` (28 avril) : R-017 font-display: swap dans phase4-finishing-gate
- `754d95a` (28 avril) : fix CSS leakage du visual thinker vers pitch designer

**Architecture finale** : state machine 15 sous-étapes atomiques (4.1-4.15) avec pré/post-conditions bash.

### 3.2 Chantier 1 — Routeur chromatique 3B-0a ✅

**Commit** : `ecc3d11` (27 avril)

**Fichiers** :
- `phases/phase-3b-gamut-router.md` — bloc 4 règles N1/N2
- `scripts/phase3b-gamut-router-anti-slop.py` — 9 checks (~600 lignes)
- `lib/gamut-visual.mjs` — adapté pour rendre badges cumulables
- `SKILL.md` zone 3B-0a

**Innovation** : **tag `[SLOP_RISQUE]` cumulable** avec TERRITOIRE/[SECTORIEL]. Permet d'autoriser une gamme à risque MAIS la signaler en aval. Le sub-agent palette qui consomme la sortie applique alors une vigilance accrue.

**Pattern PASS_WITH_PATCH** : si oubli trivial (qualification OK mais tag absent), l'orchestrateur patche silencieusement.

### 3.3 Chantier 2 — Palette 3B-3 ✅

**Statut** : implémenté, modifications devraient être commitées (vérifier `git status`).

**Fichiers** :
- `phases/phase-3b-palette.md` — bloc 5 règles N1/N2
- `scripts/phase3b-palette-anti-slop.py` — 10 checks (~700 lignes), conversions OKLCH/WCAG standalone
- `SKILL.md` zone 3B-3 (Vague 2bis) — sous-section GATE ANTI-SLOP après GATE CHROMATIQUE existant

**Patches importants** :
- **WCAG mode-aware** : lit "Mode fond dominant" et ne vérifie que les paires utilisées (sinon impossibilité de Bg dark presque-noirs)
- **Distance LCH complète pour accent** : reconnaît les accents en opposition chaud/froid (pas juste delta_chroma)

**Métriques validation** (sur 9 palettes Camille équivalentes) :
- Avant règles : 51 violations totales, 0/9 PASS
- Après règles + patches : 0 violations, 9/9 PASS clean au premier coup
- **Réduction du slop ~98%**, drama chromatique préservé

### 3.4 Chantier 3 — Fonts 3B-1/3B-2 ✅ (en cours mais avancé)

**Commits** :
- `b6921d9` (28 avril) : Phase 1bis — tooling multi-source + 6 pools 110 fontes
- `21e0502` (29 avril) : Phase 2 — règles N1/N2 anti-slop dans prompts penseurs

**Fichiers** :
- `phases/phase-3b-penseur.md` — bloc R-display-1/2/3 (caractère distinctif, dashboard=serif banni, editorial=serif+sans)
- `phases/phase-3b-penseur-body.md` — bloc R-body-1/2/3/4 (body matche concept, contraste structurel display×body, mono-fonte conditionnelle, dashboard sans serif body)
- `ref/font-axes-tags.json` — 110 fontes × 3 axes (structure/construction/proportion) pour check pairing display × body
- `scripts/phase3b-fonts-anti-slop.py` — gate Python existant
- `ref/plan-master-chantier-3-fonts-2026-04-28.md` — plan canonique

**Pool finalisé** : ~111 fontes uniques sur 12 registres ≥10 (rapport Perplexity v3 adopté).

**À vérifier dans tes audits** : si un pitch cite une font hors du pool autorisé pour le curseur A.

### 3.5 Chantier 4 — Styliste 3B-7a ✅

**Commit** : `2edcbfb` (28 avril) — gate Python avec 21 markers Partie C.

**Fichier** : `scripts/phase3b-style-anti-slop.py` (~340 lignes)

**Mission du gate** : scanner la fiche `style-choice-c{N}-{variant}.md` pour détecter les marqueurs Partie C (slop transverses) **recopiés du catalogue dans les sections prescriptives positives**.

**Sections scannées** : "Signatures à incarner", "Modulations dues au mix"

**Sections ignorées** (où nommer les marqueurs est légitime) : "INTERDITS actifs", "Garde-fous anti-slop activés", "Avis du DA", "Scan exhaustif", "Longlist ordonnée"

**21 markers en 5 catégories** :
- **Couleurs/Gradients** : Tailwind purple/indigo, Aurora 3 blobs centrés, gradient violet→blue
- **Typographie** : Inter mono-font, Roboto fallback
- **Layout** : centered hero+CTA, 3 features boxes
- **Effects** : glow shadow, infinite animation, glassmorphism par défaut
- **Voir le code complet pour les autres marqueurs**

### 3.6 Chantier 5 — Direction visuelle 3B-5 ⚠ statut à confirmer

**État au 29 avril** : aucun commit dédié visible. Le prompt `phases/phase-3b-penseur-visuel.md` ne contient pas de bloc structuré "RÈGLES ANTI-SLOP" (vérifié par grep). Pas de `phase3b-visual-anti-slop.py` dans `scripts/`.

**Documents préparatoires existants** :
- `ref/analyse-anti-slop-3b-style-visual-pitch-2026-04-28.md` — section dédiée direction visuelle avec 7 lacunes pré-identifiées
- Le prompt actuel a déjà des bonnes règles (soustractif, anti-stock, ancre stylistique, concrétude) — mais auto-évaluées

**Implication pour ton audit** : si Charles n'a pas démarré ce chantier, le carrefour direction visuelle n'a **PAS de filet anti-slop mécanique**. Le slop visuel passe par autoévaluation. À surveiller :
- Sujets stock dans `{brand}-visual-direction-c{N}.md` (mains sur clavier, équipe diverse souriante…)
- Matières clichées (marbre veiné, béton rugueux, liquid chrome…)
- Signatures temporelles datées (Aurora 3 blobs, light shaft, filament bokeh)
- Diversité inter-images insuffisante

### 3.7 Chantier 6 — Pitch designer 3B Interaction 3 ⚠ statut à confirmer

**État au 29 avril** : aucun commit dédié anti-slop visible. Le prompt `phases/phase-3b-design.md` ne contient pas de bloc structuré "RÈGLES ANTI-SLOP" (vérifié par grep — seule mention isolée). Pas de `phase3b-pitch-anti-slop.py` dans `scripts/`.

**Existant** : seulement `phase3b-css-gate.py` qui vérifie "ZÉRO CSS dans le pitch" (Règle Cardinale uniquement).

**Documents préparatoires** :
- `ref/passation-anti-slop-pitch-2026-04-28.md` — passation rédigée, attend implémentation
- `ref/analyse-anti-slop-3b-style-visual-pitch-2026-04-28.md` — section pitch avec 11 zones suspectes pré-identifiées

**Implication pour ton audit** : le pitch est le **point de convergence** du pipeline. S'il n'a pas de gate dédié, surveiller particulièrement dans `{brand}-pitch-c{N}.md` et `{brand}-pitch.md` :
- Filler words AI (Elevate, Seamless, Unleash, Next-Gen, Game-changer, Delve, Revolutionize)
- Fake names (John Doe, Jane Doe, Acme, Nexus, SmartFlow, Flowbit, Quantumly, NovaCore)
- Compositions interdites prescrites (50/50 hero, grid 3 cards, etc.)
- Cards prescrites comme artefact (interdites par mémoire utilisateur)
- Voisinage marques surfait (Aesop / Apple / Bloomberg / Dieter Rams)
- Cohérence amont (hex hors palette, fonts hors pool, style ≠ choix 3B-7a)
- Diversité atmosphérique inter-concepts (≥1/3 non-sombre)
- Anti-hover qui monte vocabulairement ("se soulève", "monte au survol")

---

## 4. Liste exhaustive des règles intégrées (par carrefour)

### 4.1 Phase 4 — TIER 1 (28 règles structurantes injectées dans Designer)

Documents :
- `ref/anti-slop-blacklist-tier1.md` — 6 compositions macro à éviter
- `ref/finition-elite-tier1.md` — 11 règles palette + CSS moderne + neutres tintés + type scale + spacing
- `ref/hierarchie-visuelle-tier1.md` — 5 règles restraint + 1 dominant + données/labels + variation densité + séparation par fond
- `ref/a11y-fondamentaux-tier1.md` — 6 règles a11y non-négociables (focus-visible, prefers-reduced-motion, touch targets 44px, etc.)

### 4.2 Phase 4 — Critiques aval (~80 règles)

Documents core (lus par les Critiques) :
- `ref/anti-slop-blacklist-core.md` — Anti-patterns sémantiques détaillés
- `ref/finition-elite-core.md` — Craft CSS détaillé
- `ref/hierarchie-visuelle-core.md` — Hiérarchie multi-dimensions
- `ref/typography-core.md` — Pairing fonts, weights, letter-spacing, line-height
- `ref/ux-writing-core.md` — Boutons spécifiques, errors, empty states, voice/tone
- `ref/interaction-core.md` — 8 états interactifs, forms, modales, touch

### 4.3 Phase 4 — Gates Python déterministes

**`scripts/phase4-blacklist-gate.py`** (~17 patterns FAIL bloquants) :
- `check_hover_translateY` — pas de translateY au hover
- `check_hover_translateX` — pas d'arrow slide au hover
- `check_hover_scale_excessive` — scale > 1.02 banni
- `check_infinite_animations` — pas d'animation infinite décorative
- `check_glow_shadows` — box-shadow `0 0 Npx` sans offset banni
- `check_text_shadow_glow` — text-shadow glow banni
- `check_section_clip_path` — wave/zigzag dividers bannis
- `check_staggered_fadeup` — @keyframes translateY+opacity banni (utiliser @starting-style)
- `check_backdrop_blur_excessive` — blur > 16px banni (max 12px)
- `check_letter_spacing_hover` — letter-spacing au hover banni
- `check_underline_scalex` — scaleX(0)→scaleX(1) underline reveal banni
- `check_accent_bar` — bordures latérales colorées >2px bannies
- `check_overline_decorative_line` — trait décoratif ::before/::after sur overline banni
- `check_stroke_circles` — cercles SVG stroke sans fill (contour amateur)
- `check_blend_mode_difference_on_text` — mix-blend-mode: difference sur texte
- `check_figurative_svg` — SVG figuratif (>20 commandes path ou >12 enfants)
- `check_graphic_layer_presence` — grain SVG + ≥3 radial-gradients obligatoires

**Plus 4 WARN Vague 2** :
- `R-082` gradient text (background-clip:text + gradient)
- `R-108` emojis dans markup
- `R-109` Lucide icon library default
- `R-114` custom mouse cursors

**`scripts/phase4-finishing-gate.py`** (8 checks Vague 1 FAIL + 33 checks Vague 2 WARN) :
- Vérifie ombres ≥2 niveaux, easing physiques nommés, hover multi-property, rythme spacing variable, retenue hovers, techniques avancées ≥4 parmi 9
- Vague 2 : R-017 font-display swap, autres checks finition

### 4.4 3B-0a Routeur — 4 règles N1/N2 + 9 checks gate

**Prompt** `phase-3b-gamut-router.md` :
- R1 : Zone violet/indigo qualification + tag `[SLOP_RISQUE]` obligatoires
- R2 : Neutres orientés (jamais "gris neutres" tout court)
- R3 : Spécificité (≥3 mots ou qualificatif)
- R4 : Pas de doublons déguisés

**Gate** `phase3b-gamut-router-anti-slop.py` :
- 7 FAIL stricts : format strict, pas de mots-températures dans noms, spécificité min, pas de restrictions de rôle, pas de doublons (Jaccard >0.5), justifications présentes, justifications non génériques
- 2 TAG-or-FAIL : zone violet/indigo handling, neutres non orientés (PASS_WITH_PATCH si qualifié sans tag)

### 4.5 3B-3 Palette — 5 règles N1/N2 + 10 checks gate

**Prompt** `phase-3b-palette.md` :
- R1 : Pas de pur noir/blanc sur surfaces principales
- R2 : Neutres tintés vers la dominante
- R3 : UN SEUL accent saturé distinct du Primary
- R4 : Anti-cousin AI purple/blue Tailwind
- R5 : Vigilance accrue si gamme `[SLOP_RISQUE]`

**Gate** `phase3b-palette-anti-slop.py` :
- check_format_strict (7 rôles exacts)
- check_hex_validity
- check_no_invented_roles (pas de Primary Light, Surface, Neutral mid…)
- check_no_pure_black_white (sur Bg dark/light/Text primary)
- check_no_ai_tailwind_defaults (regex blacklist + zone LCH purple/indigo)
- check_neutrals_tinted (chroma OKLCH > 0.005)
- check_saturation_extremes (L>0.95 ou L<0.10 → C<0.04)
- **check_wcag_contrast (mode-aware)** — lit "Mode fond dominant"
- **check_accent_distinct (distance LCH complète)** — chroma + hue
- check_justifications_non_generic

### 4.6 3B-1/3B-2 Fonts — 7 règles N1/N2 (+ gate Python existant)

**Prompt `phase-3b-penseur.md` (display)** :
- R-display-1 : caractère distinctif (anti défauts génériques)
- R-display-2 : dashboard = serif banni
- R-display-3 : editorial = serif+sans pairing

**Prompt `phase-3b-penseur-body.md`** :
- R-body-1 : body matche le concept (pas neutre par défaut)
- R-body-2 : contraste structurel display × body sur 3 axes
- R-body-3 : mono-fonte conditionnelle (single font + multi-weights vs deux fonts en compétition)
- R-body-4 : dashboard = sans serif body

**Gate** `phase3b-fonts-anti-slop.py` (existant — voir le code pour la liste exacte des checks).

**Pool de fontes** : `ref/font-axes-tags.json` — 110 fontes × 3 axes (structure/construction/proportion) + 6 pools indexés par curseur A.

### 4.7 3B-7a Styliste — Gate 21 markers Partie C

**Gate** `phase3b-style-anti-slop.py` (~340 lignes).

**Sections scannées dans la fiche style-choice** :
- "Signatures à incarner"
- "Modulations dues au mix"

**Sections ignorées** :
- "INTERDITS actifs" / "Garde-fous anti-slop activés" / "Avis du DA" / "Scan exhaustif" / "Longlist ordonnée"

**21 markers Partie C** (du catalogue `ref/styles-bibliotheque.md`) :
- Couleurs/Gradients : purple/indigo Tailwind, Aurora 3 blobs centrés, gradient violet→blue
- Typographie : Inter mono-font, Roboto fallback
- Layout : centered hero+CTA, 3 features boxes, footer 4 columns
- Effects : glow shadow, infinite animation, glassmorphism par défaut, neumorphism
- Animation : translateY au hover, staggered fade-up
- (Et autres — voir `ref/styles-bibliotheque.md` Partie C pour la liste exhaustive du catalogue)

### 4.8 3B-5 Direction visuelle / 3B Interaction 3 Pitch

**État** : pas de gate dédié au 29 avril. Le seul gate sur le pitch est `phase3b-css-gate.py` (uniquement ZÉRO CSS).

**Si tu détectes du slop dans ces zones** : noter explicitement que le carrefour n'a pas de filet mécanique aujourd'hui — c'est attendu, à signaler à Charles.

---

## 5. Sources canoniques des règles

### 5.1 Skill `/audit-slop` (`.claude/skills/audit-slop/`)

C'est le **référentiel central**. Architecture :
```
audit-slop/SKILL.md                              # Orchestrateur 4 grilles + synthétiseur
audit-slop/agents/craft-moderne.md               # Agent 1
audit-slop/agents/vercel-technique.md            # Agent 2
audit-slop/agents/big-pipeline.md                # Agent 3 (lance les gates Python)
audit-slop/agents/perplexity-temporel.md         # Agent 4
audit-slop/agents/synthetiseur.md                # Synthétiseur arbitre
audit-slop/sources/                              # Sources externes (19 fichiers)
  ├─ impeccable/SKILL.md + reference/{color, typography, spatial, motion, interaction, responsive, ux-writing, craft, extract}.md
  ├─ taste-skill/{taste, redesign, soft, minimalist, brutalist, images, stitch}-skill.md
  ├─ gstack/{plan-design-review, design-review}.md
  └─ vercel-command.md
```

**Pour invoquer** : `/audit-slop --session {session_dir} --concept N` (mode 3 intégré BIG) ou `/audit-slop {html_path}` (mode 2 autonome).

**Sortie** : rapport markdown consolidé avec score 0-10 sur 4 dimensions + verdict global ABANDONNÉ / AI SLOP / MOYEN / BON / ELITE.

**Référence canonique pour comprendre l'audit** : `audit-slop/SKILL.md`.

### 5.2 Documents BIG anti-slop (TIER 1 + core + formulation)

**Le guide d'or** :
- `ref/anti-slop-formulation-guide.md` — convention 3 niveaux N1/N2/N3 (à connaître par cœur)

**TIER 1 (lus par Designer Phase 4)** :
- `ref/anti-slop-blacklist-tier1.md`
- `ref/finition-elite-tier1.md`
- `ref/hierarchie-visuelle-tier1.md`
- `ref/a11y-fondamentaux-tier1.md`

**Core (lus par Critiques aval)** :
- `ref/anti-slop-blacklist-core.md`
- `ref/finition-elite-core.md`
- `ref/hierarchie-visuelle-core.md`
- `ref/typography-core.md`
- `ref/ux-writing-core.md`
- `ref/interaction-core.md`

### 5.3 Extraction consolidée Vague 2 (LE référentiel pour mapping)

**`ref/extraction-vague2-2026-04-26.md`** — 182 règles distinctes avec :
- ID (R-001 à R-182)
- Source principale + autres sources où la règle apparaît
- Type (UNIV / CTX)
- Domaine (typography / spacing / interaction / color / composition / motion / ux-writing / responsive / a11y / content / performance / craft)
- Polarité (NEG / POS)
- Grep-ability (OUI / PARTIEL / NON)
- Sévérité (CRITIQUE / MOYENNE / POLISH)
- Destination proposée (TIER_1 / GATE_PYTHON / CRITIQUE_TIER_2 / CRITIQUE_TIER_3 / N_A_HTML_VANILLA)
- Couverture BIG (présent / partiel / absent)

**Quand tu doutes d'une règle** : commencer par chercher son ID R-NNN dans ce fichier.

### 5.4 Documents Perplexity (datation temporelle)

- `ref/perplexity-styles-datés-vs-actuels-2026.md` — classification 85 styles UX/UI (INTEMPOREL / ACTUEL / CYCLIQUE / DATÉ) + marqueurs slop documentés
- `ref/perplexity-composition-patterns-report.md` — 12 patterns datés × 12 actuels
- `ref/perplexity-composition-detail-report.md` — détail composition

### 5.5 Catalogue de styles (référentiel styliste)

- `ref/styles-bibliotheque.md` — 34 styles Partie A + 10 Partie B (datés/cycliques) + **Partie C marqueurs slop transverses** (le référentiel pour le gate styliste)
- `ref/style-matching-rules.md` — 5 règles matching + 2 règles pairing
- `ref/styles-matching-protocol.md` — protocole 5 étapes du styliste

---

## 6. Méthodologie d'analyse d'un test E2E

### 6.1 Inputs attendus du test

Quand Charles te transmet un test, attends-toi à recevoir un **session_dir** comme :
```
outputs/test-{brand}-{label}/
├─ .session-id
├─ .test-context.md
├─ {brand}-brief-analysis.md            # Phase 1
├─ {brand}-scoping.md                   # Phase 2A
├─ {brand}-context-clean.md             # Phase 2D
├─ {brand}-concepts-narratifs.md        # Phase 3A
├─ {brand}-chromatic-gamuts.md          # 3B-0a routeur
├─ {brand}-aesthetic-selections.md      # 3B-0b
├─ {brand}-penseur-c{1,2,3}.md          # 3B-1 display
├─ {brand}-penseur-body-c{1,2,3}.md     # 3B-1 body
├─ {brand}-font-backups.md              # 3B-2 designer visuel
├─ {brand}-palette-c{1,2,3}-{a,b,c}.md  # 3B-3 palettes (9 fichiers)
├─ {brand}-palette-c{1,2,3}.md          # palettes choisies (3 fichiers)
├─ {brand}-style-choice-c{1,2,3}-{a,b,c}.md  # 3B-7a 9 fichiers
├─ {brand}-style-choice-c{1,2,3}.md     # styles choisis
├─ {brand}-style-specimen-c{1,2,3}-{a,b,c}.html  # 3B-7b spécimens
├─ {brand}-visual-direction-c{1,2,3}.md # 3B-5 direction visuelle
├─ {brand}-pitch-c{1,2,3}.md            # 3B Interaction 3
├─ {brand}-pitch.md                     # assemblage final
└─ {brand}-style-tile-concept-{1,2,3}.html  # Phase 4 outputs
```

### 6.2 Workflow d'analyse (étapes)

**Étape 1 — Inventaire** : lister les fichiers présents, repérer les manquants. Si un artefact attendu manque, le pipeline a planté — signaler.

**Étape 2 — Gates Python sur chaque artefact 3B**.

Pour chaque carrefour, exécuter le gate correspondant et capturer le verdict :
```bash
# Routeur
python3 scripts/phase3b-gamut-router-anti-slop.py outputs/{session}/{brand}-chromatic-gamuts.md --json-output

# Palette (9 fichiers à vérifier)
for c in 1 2 3; do for v in a b c; do
  python3 scripts/phase3b-palette-anti-slop.py outputs/{session}/{brand}-palette-c${c}-${v}.md --json-output
done done

# Styliste (9 fichiers)
for c in 1 2 3; do for v in a b c; do
  python3 scripts/phase3b-style-anti-slop.py outputs/{session}/{brand}-style-choice-c${c}-${v}.md --json-output
done done

# Fonts (3 fichiers display + 3 body)
for c in 1 2 3; do
  python3 scripts/phase3b-fonts-anti-slop.py outputs/{session}/{brand}-penseur-c${c}.md --json-output
done

# Pitch (CSS gate uniquement aujourd'hui)
for c in 1 2 3; do
  python3 scripts/phase3b-css-gate.py outputs/{session}/{brand}-pitch-c${c}.md
done
```

**Étape 3 — Audit-slop final sur les style-tiles** :
```
/audit-slop --session test-{brand}-{label} --concept 1
/audit-slop --session test-{brand}-{label} --concept 2
/audit-slop --session test-{brand}-{label} --concept 3
```

**Étape 4 — Cross-checks manuels** (pour les zones sans gate) :
- Direction visuelle : grep sujets stock / matières clichées / signatures datées dans `{brand}-visual-direction-c{N}.md`
- Pitch : grep filler words / fake names / compositions interdites prescrites / voisinage marques surfait dans `{brand}-pitch-c{N}.md`
- Cohérence amont/aval : hex du pitch ⊂ palette validée ; fonts du pitch ⊂ font-backups ; style cité = style choisi

**Étape 5 — Détection de slop résiduel** :
- Marqueurs Partie C dans le HTML final qui auraient dû être bloqués
- AI tells classiques (Inter, #6366f1, glassmorphism par défaut, hero centré CTA solo) dans le HTML
- Cohérence palette/typo : Primary du HTML correspond à la palette validée ?

**Étape 6 — Synthèse et verdict**.

### 6.3 Métriques de réussite (baselines documentées)

**Chantier 2 palette (Camille)** :
- Avant règles : 51 violations sur 9 palettes (0/9 PASS)
- Après règles + patches : 0 violations (9/9 PASS clean au premier coup)
- Réduction ~98%

**Score audit-slop sur VoltaPilot c2 "Pouls Profond"** :
- 15 avril (baseline pré-Vague 2) : 4.0/10
- 24 avril (post Étape 1 factorisation) : 6.0/10
- 26 avril (post Vague 1+1bis) : 7.0/10
- 26 avril (post Vague 2 + refactor R3) : 6.0/10 ⚠ régression "jeu de la taupe", corrigée par Vague 2.5
- **Cible visée** : ≥7.5/10 (idéal 8.0+)
- BIG Pipeline ≥7/10
- Vercel ≥8/10
- Craft ≥6/10
- Perplexity ≥8.5/10

### 6.4 Cas de slop résiduel à reconnaître

**Slop chromatique** :
- Hex `#000000` ou `#ffffff` exacts dans CSS sur surfaces principales
- Hex AI Tailwind exact (`#6366f1`, `#7c3aed`, `#a855f7`, `#3b82f6`) dans la palette ou le CSS
- Variables CSS `--bg-dark` ou `--text-primary` non tintées (chroma OKLCH < 0.005)
- Accent moins saturé que Primary
- Plusieurs Accents inventés dans la palette

**Slop typographique** :
- `font-family: Inter` ou famille bannie dans le HTML
- Fonts Tailwind par défaut sans personnalisation (Geist seul = OK, Geist + Plus Jakarta = suspect)
- 2 fonts en compétition sans contraste structurel sur 3 axes
- Pairing daté (Playfair + Lato, Cormorant + Montserrat)

**Slop compositionnel** :
- Hero centré + sous-titre + CTA solo (le pattern AI tell #1)
- Grid 3 cards identiques avec icon + titre + description
- 3 features en boxes uniformes
- Footer 4 colonnes de liens
- Pricing centré avec option centrale highlightée
- Carousels comme conteneurs de contenu
- Device frames (laptop/phone mockup) comme hero

**Slop animation/effet** :
- `transform: translateY(-Npx)` au hover
- `box-shadow: 0 0 Npx` (glow sans offset)
- `animation: ... infinite`
- Glassmorphism décoratif par défaut (backdrop-filter blur sur toutes les cards)
- Neumorphism (double shadow inset/outset symétrique)
- Gradient text via background-clip:text

**Slop verbal** :
- "Elevate your X", "Seamlessly integrate", "Unleash the power", "Next-gen solution", "Game-changing", "Delve into"
- "John Doe", "Jane Doe", "Acme Corp", "Nexus Inc", "SmartFlow", "Flowbit", "Quantumly", "NovaCore"
- "Lorem ipsum", "Click here"
- Apostrophes droites en français (`'` au lieu de `'`)

**Slop temporel (Perplexity)** :
- Aurora UI 3 blobs génériques centrés
- Y2K chrome / vaporwave
- Claymorphism bubbly
- Glassmorphism pur 2020-style
- Brand watermark oversize

### 6.5 Faux positifs connus (à ne pas réflagger)

- Palettes "tons doux monochromes" : Bg dark et Bg light très proches mais différents (>1.5:1) — légitime, ne pas flag
- Accents froids dans palettes chaudes (et inversement) : valides via distance LCH (chroma + hue)
- Mode SOMBRE avec Bg dark presque-noir (`#0E0C0A`) + Text primary clair : OK avec WCAG mode-aware
- Mots "chaud", "froid" dans les **prescriptions de prompt** mais PAS dans les noms de gammes
- "Card" mentionnée dans le pitch SI le concept l'exige (mais artefact prescrit ≠ card empilée par défaut)

### 6.6 Format de rapport arbitre

Structure recommandée :

```markdown
# Verdict arbitre — {brand} session {label} ({date})

## Résumé exécutif
- Score anti-slop global : X/10
- Carrefours conformes : N/6
- Carrefours avec slop résiduel : [liste]
- Score audit-slop final HTML : X/10 (si lancé)
- Régressions vs baseline : [aucune | liste]

## Détail par carrefour

### 3B-0a Routeur chromatique
- Verdict gate : PASS | FAIL ({N} violations)
- Détail violations : [liste avec fichier:ligne]
- Tag [SLOP_RISQUE] présent : oui/non sur quelles gammes

### 3B-3 Palette (9 variantes)
- Verdict global : N/9 PASS
- Détail par variante : [c1-a, c1-b, c1-c, c2-a, c2-b, c2-c, c3-a, c3-b, c3-c]
- Cas patches mode-aware / LCH déclenchés : oui/non

### 3B-1/3B-2 Fonts
- Verdict gate fonts : PASS | FAIL
- Fontes choisies hors pool : oui/non
- Pairings serif+sans détectés / OK : N/3

### 3B-7a Styliste (9 variantes)
- Verdict global : N/9 PASS
- Marqueurs Partie C détectés : [liste]

### 3B-5 Direction visuelle (sans gate)
- Cross-checks manuels :
  - Sujets stock détectés : [liste]
  - Matières clichées : [liste]
  - Signatures datées : [liste]

### 3B Pitch (CSS gate uniquement aujourd'hui)
- Verdict CSS gate : PASS | FAIL
- Cross-checks manuels :
  - Filler words AI : [liste]
  - Fake names : [liste]
  - Compositions interdites prescrites : [liste]
  - Cohérence amont (palette/fonts/style) : OK | dérive [détail]

### Phase 4 (audit-slop final)
- Score Craft Moderne : X/10
- Score Vercel : X/10
- Score BIG Pipeline : X/10
- Score Perplexity : X/10
- Verdict consolidé synthétiseur : ABANDONNÉ | AI SLOP | MOYEN | BON | ELITE

## Slop résiduel détecté

| Localisation | Règle violée | Source canonique | Sévérité |
|---|---|---|---|
| ... | ... | ... | CRITIQUE/MOYENNE/POLISH |

## Régressions vs chantiers précédents
[Si gate qui passait avant FAIL maintenant, ou inversement]

## Recommandations pour Charles
[Actions concrètes, sans implémenter]
- Si carrefour visuel/pitch sans gate identifié comme source de slop majeur → recommander prioriser ces chantiers
- Si gate qui FAIL régulièrement sur cas légitimes → recommander patch (calque WCAG mode-aware)
- Si pattern de slop récurrent non couvert → proposer nouveau check
```

---

## 7. Outils à disposition

### 7.1 Scripts gates Python (8 disponibles)

| Script | Rôle | Mode JSON |
|---|---|---|
| `phase4-blacklist-gate.py` | 17 patterns CSS datés FAIL + 4 WARN Vague 2 | Non (CLI) |
| `phase4-finishing-gate.py` | 8 checks Vague 1 + 33 Vague 2 | Oui (`--json-output`) |
| `phase3b-css-gate.py` | ZÉRO CSS dans pitch | Non (CLI) |
| `phase3b-gamut-router-anti-slop.py` | Routeur chromatique 9 checks | Oui |
| `phase3b-palette-anti-slop.py` | Palette 10 checks | Oui |
| `phase3b-fonts-anti-slop.py` | Fonts (voir code pour checks) | Oui |
| `phase3b-style-anti-slop.py` | Styliste 21 markers Partie C | Oui |
| `parse-blacklist-violations.py` | Parse stdout blacklist gate | (helper) |
| `extract-trace.py` | Extract trace pour anti-pollution | (helper) |

### 7.2 Skill `/audit-slop` (audit final HTML)

`.claude/skills/audit-slop/SKILL.md` — invocation `/audit-slop --session {dir} --concept N`. Lance 4 agents en parallèle + synthétiseur. Produit un rapport consolidé.

### 7.3 Skill `/audit-elite` (juge relatif)

`.claude/skills/audit-elite/SKILL.md` — juge impitoyable qui compare les style-tiles aux étalons Awards. **Complémentaire** à audit-slop : audit-slop dit "ça respecte les règles", audit-elite dit "ça soutient la comparaison face à un site élite primé". Utiliser quand audit-slop dit ELITE pour confirmer.

### 7.4 Sessions de référence (baselines)

Pour comparer "avant/après chantier" :

| Session | Brand | Quoi |
|---|---|---|
| `outputs/test-camille-test-20260415-1733/` | Camille | **Avant règles** (palettes 51 violations) |
| `outputs/test-camille-test-20260424-1907/` | Camille | Récent partiellement nettoyé |
| `outputs/test-camille-test-20260427-1545/` | Camille | Post-routeur anti-slop |
| `outputs/test-camille-test-20260427-3b3-anti-slop-v2/` | Camille | Test palette v2 (avec patches) — **9/9 PASS** |
| `outputs/test-voltapilot-vague2.5-20260427-*/` | VoltaPilot | Phase 4 vague 2.5 |

---

## 8. Limites reconnues du système (à connaître pour ne pas faire d'audit naïf)

### 8.1 Trous de couverture connus

1. **Direction visuelle 3B-5 sans gate Python dédié** (au 29 avril) — slop visuel via auto-évaluation. À surveiller.

2. **Pitch designer sans gate dédié** — seulement `phase3b-css-gate.py` (ZÉRO CSS uniquement). Filler words / fake names / compositions interdites prescrites passent.

3. **Trou "accent dans gamme exclue"** : le routeur peut exclure une gamme (ex: cyans turquoise pour Camille, ventre mou tech/wellness) MAIS la palette met cet accent quand même via la règle "accent libre". Aucun gate. Cas observé Foyer Parabolique C avec Accent cyan `#3FB8C9`.

4. **Bug pipeline température** : la prescription "Température chaude" du scoping (Phase 2A) n'est pas remontée au routeur. Le routeur peut "dévier" de la prescription du scoping. Charles a décidé "vivre avec" pour l'instant.

5. **Divergence A/B/C subtile** : depuis les chantiers, les divergences sont plus pondérées (les anciennes "fortes" violaient des règles). Pas un bug, un trade-off assumé.

### 8.2 Faux positifs résolus mais à reconnaître

- WCAG strict sur les 2 fonds simultanément → patch mode-aware (lit "Mode fond dominant")
- Accent_distinct par delta_chroma seul → patch distance LCH (chroma + hue)
- Inversion atmosphérique seuil 4.5:1 → assoupli à 1.5:1 (palettes "tons doux" préservées)

### 8.3 Architecture non-uniforme

Les 6 carrefours 3B n'ont pas tous le même niveau de couverture :
- Routeur, Palette, Fonts, Styliste : gate Python dédié + N1/N2 dans prompt
- Direction visuelle, Pitch : N1/N2 partiel dans prompt + pas de gate dédié

C'est attendu. Charles attaque les chantiers par priorité.

---

## 9. Référentiel exhaustif des fichiers à connaître

### 9.1 À lire en début de mission (~45 min total)

| Fichier | Pourquoi |
|---|---|
| `ref/anti-slop-formulation-guide.md` | Convention 3 niveaux N1/N2/N3 |
| `ref/extraction-vague2-2026-04-26.md` | Les 182 règles consolidées avec ID + destination |
| `ref/passation-anti-slop-pour-3b.md` | Vague 2 Phase 4 — architecture détaillée |
| `ref/passation-anti-slop-fonts-2026-04-28.md` | Méthodologie consolidée |
| `ref/analyse-anti-slop-3b-style-visual-pitch-2026-04-28.md` | Analyse re-challengée des 3 derniers carrefours |

### 9.2 Référence quand tu doutes d'une règle

| Domaine | Fichier |
|---|---|
| Color | `audit-slop/sources/impeccable/reference/color-and-contrast.md` + `ref/finition-elite-{tier1,core}.md` |
| Typography | `audit-slop/sources/impeccable/reference/typography.md` + `ref/typography-core.md` |
| Spacing/Layout | `audit-slop/sources/impeccable/reference/spatial-design.md` + `ref/hierarchie-visuelle-{tier1,core}.md` |
| Motion | `audit-slop/sources/impeccable/reference/motion-design.md` |
| Interaction | `audit-slop/sources/impeccable/reference/interaction-design.md` + `ref/interaction-core.md` |
| UX writing | `audit-slop/sources/impeccable/reference/ux-writing.md` + `ref/ux-writing-core.md` |
| A11y | `ref/a11y-fondamentaux-tier1.md` |
| Composition | `audit-slop/sources/gstack/design-review.md` + `ref/anti-slop-blacklist-{tier1,core}.md` |
| AI Tells | `audit-slop/sources/taste-skill/taste-skill.md` (section 7) + `audit-slop/sources/gstack/plan-design-review.md` |
| Datation | `ref/perplexity-styles-datés-vs-actuels-2026.md` |
| Catalogue styles | `ref/styles-bibliotheque.md` (Parties A/B/C) |

### 9.3 Documents internes au chantier anti-slop 3B

| Fichier | Cible |
|---|---|
| `ref/passation-anti-slop-pour-3b.md` | Vague 2 Phase 4 |
| `ref/passation-vague2-2026-04-26.md` | Passation Vague 2 |
| `ref/plan-vague2-point1-regles-negatives-externes.md` | Plan Vague 2 |
| `ref/plan-vague2-point2-regles-positives.md` | Plan Vague 2 |
| `ref/plan-master-chantier-3-fonts-2026-04-28.md` | Plan canonique chantier 3 fonts |
| `ref/passation-anti-slop-fonts-2026-04-28.md` | Passation chantier 3 fonts |
| `ref/passation-anti-slop-phase4-typography-2026-04-28.md` | Passation typo Phase 4 |
| `ref/passation-anti-slop-pitch-2026-04-28.md` | Passation chantier 6 pitch |
| `ref/onboarding-anti-slop-pour-styliste-2026-04-28.md` | Onboarding chantier 4 styliste |
| `ref/analyse-anti-slop-3b-style-visual-pitch-2026-04-28.md` | Analyse pré-faite 3 carrefours restants |

### 9.4 Mémoire utilisateur (préférences Charles)

`MEMORY.md` (déjà chargé en contexte). Notamment :
- `feedback_no_undiscussed_changes.md` — pas de changements hors périmètre
- `feedback_step_by_step_testing.md` — une seule modif par test
- `feedback_no_copyable_cards_in_examples.md` — artefacts exotiques uniquement, pas de KPI cards
- `feedback_no_confirmation_between_waves.md` — enchaîner A→B→C sans pause
- `feedback_competent_over_lean_subagents.md` — pour corrections, réutiliser le subagent compétent

### 9.5 Documents utilisateur Charles

- `CLAUDE.md` global utilisateur : ton direct, français, vulgarisation des termes techniques pour Charles non-développeur
- `CLAUDE.md` projet : conventions Git, REX systématique, ARCHITECTURE/CHANGELOG/DECISIONS
- `Documents/framework-claude-md.md` — framework méta sur CLAUDE.md

---

## 10. Quick reference — commandes d'audit type

```bash
# Inventaire session
ls -la outputs/test-{brand}-{label}/ | head -50

# Tous gates 3B en série
SDIR="outputs/test-{brand}-{label}"
BRAND="{brand}"

# Routeur
python3 scripts/phase3b-gamut-router-anti-slop.py "$SDIR/$BRAND-chromatic-gamuts.md" --json-output

# Palette (9 variantes)
for c in 1 2 3; do for v in a b c; do
  echo "=== palette-c${c}-${v} ==="
  python3 scripts/phase3b-palette-anti-slop.py "$SDIR/$BRAND-palette-c${c}-${v}.md" --json-output | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['verdict'],len(d['violations']))"
done; done

# Styliste (9 variantes)
for c in 1 2 3; do for v in a b c; do
  echo "=== style-choice-c${c}-${v} ==="
  python3 scripts/phase3b-style-anti-slop.py "$SDIR/$BRAND-style-choice-c${c}-${v}.md" --json-output | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['verdict'],len(d['violations']))"
done; done

# Fonts (3 display + 3 body)
for c in 1 2 3; do
  python3 scripts/phase3b-fonts-anti-slop.py "$SDIR/$BRAND-penseur-c${c}.md" --json-output
done

# Pitch CSS (gate existant uniquement)
for c in 1 2 3; do
  python3 scripts/phase3b-css-gate.py "$SDIR/$BRAND-pitch-c${c}.md"
done

# Phase 4 sur HTML
for c in 1 2 3; do
  python3 scripts/phase4-blacklist-gate.py "$SDIR/$BRAND-style-tile-concept-${c}.html"
  python3 scripts/phase4-finishing-gate.py "$SDIR/$BRAND-style-tile-concept-${c}.html" --json-output
done

# Audit-slop final (skill)
# /audit-slop --session test-{brand}-{label} --concept 1 (etc.)
```

---

## Dernière mise à jour

2026-04-29 — Rédigé par la session ayant complété les chantiers 1 (routeur) et 2 (palette + patches), et conçu les passations pour les chantiers 3 (fonts), 4 (styliste), 6 (pitch).

**État au 29 avril** : Phase 4 Vague 2 + 2.5 + P14 + R-017 commités. Chantiers 3B 1-2-3-4 commités. Chantiers 5 (visuel) et 6 (pitch) statut variable — vérifier `git log` au démarrage de mission. La session arbitre doit en tenir compte dans son verdict.
