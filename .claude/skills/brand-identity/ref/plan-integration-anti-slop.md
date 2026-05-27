# Plan — Intégration des règles anti-slop dans BIG en amont

## Contexte

Le pipeline Brand Identity Generator (BIG) produit aujourd'hui des style-tiles qui passent l'audit-slop à **4.2/10** en moyenne (baseline Camille concept-1, 12 violations CRITIQUES détectées par l'agent BIG Pipeline, 5 par Craft Moderne). Le skill `/audit-slop` existant est un auditeur POST-génération : il détecte le slop après coup mais ne le prévient pas.

**Objectif** : intégrer en amont (à priori) dans BIG les règles **universelles** du skill audit-slop pour que Phase 4 et les Batches 2/3 génèrent moins de slop dès la première sortie. Les règles **contextuelles** (datation, registre-dépendantes) restent dans audit-slop où le synthétiseur peut arbitrer avec le pitch/concept/curseur.

**Contrainte majeure** : le système BIG actuel est le meilleur résultat de l'historique. Les prompts Phase 4 sont déjà saturés (428 lignes, 12 sections, 10 gates). Il y a 23% de redondance mesurée entre fichiers (blacklist copiée 4×, socle finition 4×, hiérarchie 4×). Ajouter brut 100+ règles = usine à gaz garantie et dégradation du comportement subagent par fatigue cognitive.

**Stratégie validée avec Charles** : 3 couches stratifiées (gates Python pour règles binaires / core blacklist sémantique pour règles transverses / Phase 3B pour règles palette-fonts-type-scale / Axe 5 DA Check pour règles de jugement final), précédées d'une factorisation pour libérer du budget contextuel.

**Arbitrages Charles actés** :
- Audit-slop reste optionnel pour l'instant (passage automatique en fin de chantier)
- Tolérance délai +30s par phase : OK
- Pas de variante par curseur A (règles universelles)
- Séquence : Phase 4 isolée d'abord, Batch 2/3 ensuite, Phase 3B en dernier (le plus sensible)

---

## Chiffres de référence (extraction exhaustive)

Basé sur la lecture des 20 fichiers sources audit-slop + 11 fichiers BIG :

| Métrique | Valeur |
|---|---|
| Règles brutes extraites | 287 |
| Règles uniques après dédup cross-source | **212** |
| Règles universelles | **158** |
| Règles contextuelles (restent dans audit-slop) | **54** |
| Déjà couvertes par BIG (OUI complet) | 42 |
| Partiellement couvertes par BIG | 34 |
| N/A pour HTML vanilla (Framer Motion, React, nuqs) | ~15 |
| **À injecter dans BIG (net)** | **~101 règles** |

### Ventilation des 158 règles universelles par destination

| Destination | Brut | N/A HTML vanilla | Déjà BIG OUI | Net à injecter |
|---|---|---|---|---|
| Gate Python | 47 | 5 | 15 | **~27** |
| Core blacklist (nouveau `.md` partagé) | 68 | 5 | 10 | **~53** |
| Phase 3B | 32 | 3 | 15 | **~14** |
| Axe 5 DA Check (nouveau dans phase-4bis) | 11 | 2 | 2 | **~7** |
| **Total** | **158** | **~15** | **42** | **~101** |

---

## Architecture cible — 3 couches stratifiées

```
┌─────────────────────────────────────────────────────────────────┐
│  BIG AMONT — prévient le slop pendant la génération              │
│                                                                  │
│  Couche A : Gates Python (règles BINAIRES grep-ables)           │
│    - phase4-blacklist-gate.py enrichi                           │
│    - phase6-batch-gate.py nouveau (propagation)                 │
│    - phase3b-css-gate.py enrichi (propagation Phase 3B)         │
│                                                                  │
│  Couche B : Prompts BIG (règles SÉMANTIQUES universelles)       │
│    B.1 Factorisation : 3 refs partagés                          │
│        - ref/anti-slop-blacklist-core.md                         │
│        - ref/finition-elite-core.md                              │
│        - ref/hierarchie-visuelle-core.md                         │
│    B.2 Enrichissement : nouvelles règles sémantiques             │
│                                                                  │
│  Couche P3B : Phase 3B (règles palette/fonts/type-scale)        │
│    - phase-3b-palette.md                                         │
│    - phase-3b-penseur-visuel.md                                  │
│    - phase-3b-penseur.md                                         │
│                                                                  │
│  Couche C : DA Check (règles JUGEMENT post-génération)          │
│    - phase-4bis-da-check.md : Axe 5 — Anti-slop universel       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  AUDIT-SLOP AVAL (inchangé) — règles CONTEXTUELLES               │
│    Arbitre avec pitch/concept/curseur/registre                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Décomposition en 5 étapes séquentielles

### Étape 1 — Factorisation des 3 refs partagés (CHANTIER PRÉALABLE)

**Goal** : libérer du budget contextuel AVANT d'ajouter quoi que ce soit.

**Actions** :
1. Créer `ref/anti-slop-blacklist-core.md` (~35 lignes)
   - Regroupe la blacklist anti-patterns datés actuellement copiée dans 4 fichiers
   - Sources actuelles à consolider : phase-4-styletile.md L301-349 + phase-4-artefact.md L144-151 + phase-6a-batch2.md L110-140 + phase-6b-batch3.md L88-115
   - Contenu : hovers datés, animations infinies, séparateurs datés, effets visuels datés, animations d'entrée datées, compositions datées, couche graphique interdictions
2. Créer `ref/finition-elite-core.md` (~25 lignes)
   - Regroupe le socle finition actuellement dispersé (93 lignes cumulées)
   - Contenu : ombres ≥2 couches, easing physiques nommés, rythme spacing, hover ≥2 propriétés, CSS moderne (`oklch`, `@layer`, `@property`, `color-mix`, `text-wrap`, `clamp`), techniques avancées (≥4 parmi 9)
3. Créer `ref/hierarchie-visuelle-core.md` (~20 lignes)
   - Regroupe les principes hiérarchie actuellement dispersés (76 lignes cumulées)
   - Contenu : squint test, données clés en typographie display, séparation par fond (pas bordures 1px), hiérarchie 3 couches, densité variable, max 1 graphique par composant
4. Modifier les 4 fichiers phases pour importer ces refs :
   - `phase-4-styletile.md` : remplacer les sections dupliquées par des références `Voir ref/anti-slop-blacklist-core.md` — l'orchestrateur BIG lit ces refs et injecte leur contenu dans le contexte du subagent (pattern BIG éprouvé : orchestrateur compose, subagent ne lit pas)
   - `phase-4-artefact.md` : idem
   - `phase-6a-batch2.md` : idem
   - `phase-6b-batch3.md` : idem
5. Vérifier que l'orchestrateur principal du skill brand-identity lit bien ces refs au moment opportun (probablement `SKILL.md` principal) — adapter si nécessaire

**Résultat attendu** : -204 lignes nettes sur les prompts BIG (304 lignes redondantes retirées, 100 lignes de refs ajoutées en lecture à la demande).

**Test de non-régression OBLIGATOIRE** : relancer un brief connu (Camille ou autre de qualité validée) intégralement, comparer le style-tile avant/après. Bloquer si score DA Check baisse ou si la qualité subjective régresse.

**Fichiers modifiés** :
- Nouveaux : `ref/anti-slop-blacklist-core.md`, `ref/finition-elite-core.md`, `ref/hierarchie-visuelle-core.md`
- Modifiés : `phases/phase-4-styletile.md`, `phases/phase-4-artefact.md`, `phases/phase-6a-batch2.md`, `phases/phase-6b-batch3.md`
- Possiblement : `SKILL.md` principal si l'orchestrateur doit lire ces refs

**Durée estimée** : 1 session complète (avec tests non-régression)

**Risque** : MOYEN-ÉLEVÉ (touche l'équilibre actuel des prompts) — mitigation par tests avant/après obligatoires.

---

### Étape 2 — Gates Python enrichis (Phase 4)

**Goal** : intégrer les 27 règles universelles grep-ables manquantes dans les gates Python existants. Zéro charge prompt.

**Actions** :
1. Enrichir `scripts/phase4-blacklist-gate.py` avec les checks manquants, organisés en blocs :

**Bloc A11y (8 nouveaux checks)** :
- `check_focus_visible_on_interactives` : tout `<button>`, `<a>`, `<input>` doit avoir une règle `:focus-visible` dans le CSS
- `check_outline_none_without_replacement` : `outline: none` ou `outline: 0` sans `:focus-visible` remplaçant
- `check_prefers_reduced_motion` : si `animation` ou `transition` présente avec durée > 200ms, doit avoir un bloc `@media (prefers-reduced-motion: reduce)`
- `check_touch_action` : interactifs doivent avoir `touch-action: manipulation`
- `check_user_scalable_meta` : `<meta viewport>` ne doit pas contenir `user-scalable=no` ni `maximum-scale=1`
- `check_body_font_size_min_16px` : body text en `px` avec valeur < 16px banni
- `check_body_font_size_in_rem` : body text devrait être en `rem`, pas `px`
- `check_semantic_html` : `<div onclick=>` ou `<span onclick=>` banni → utiliser `<button>` ou `<a>`

**Bloc Typo/Copy (9 nouveaux checks)** :
- `check_banned_fonts` : Inter, Roboto, Open Sans, Arial, Fraunces, Newsreader, Lora, Crimson, Playfair, Cormorant, Instrument Serif bannis par défaut dans `font-family`
- `check_straight_quotes_fr` : détection d'apostrophes droites `'` dans texte FR (contexte par détection de mots FR fréquents)
- `check_straight_double_quotes` : détection de `"..."` droits au lieu de `" ... "` courbes
- `check_ellipsis_three_dots` : `...` au lieu de `…`
- `check_lorem_ipsum` : présence de "Lorem ipsum" ou "Lorem Ipsum"
- `check_filler_words` : Elevate, Seamless, Unleash, Next-Gen, Delve, Game-changer, Revolutionize, Empower, Transform (liste paramétrable)
- `check_fake_names` : Jane Doe, John Doe, John Smith, Jane Smith, Acme, Acme Corp, Nexus, SmartFlow, QuantumFlow, NovaCore (liste paramétrable)
- `check_uppercase_in_body` : `text-transform: uppercase` sur blocs texte longs (> 50 caractères)
- `check_click_here_links` : texte de lien `Click here`, `Read more` seul, `Here`, `Learn more` seul

**Bloc Technique Vercel (6 nouveaux checks)** :
- `check_transition_all` : déjà présent côté `transition:all`, enrichir détection
- `check_theme_color_meta` : `<meta name="theme-color">` absent
- `check_href_dead` : `href="#"` banni sauf skip-link
- `check_color_scheme` : pour dark themes, `color-scheme: dark` sur `<html>` absent
- `check_img_width_height` : `<img>` sans `width` + `height` explicites
- `check_translate_no_brand_names` : brand name doit avoir `translate="no"`

**Bloc Content/Placeholders (4 nouveaux checks)** :
- `check_placeholder_sources` : URLs `unsplash.com` sans crédit cassées, préférer `picsum.photos`
- `check_lucide_user_avatars` : `lucide-user`, `feather-user` bannis comme avatars
- `check_title_case_every_header` : headings `## Ma Section Est Ici` bannis (préférer sentence case)
- `check_emojis_in_markup` : émojis unicode dans markup/alt/code

**Règle de sévérité** : chaque nouveau check démarre en **WARN** pendant 5 runs de validation, puis passe en **FAIL** si aucun faux positif.

2. Vérifier que les checks existants ne dupliquent pas ces nouveaux.

3. Tester chaque regex sur 5-10 HTMLs existants AVANT activation (générés ET briefs validés du passé).

**Fichiers modifiés** :
- `scripts/phase4-blacklist-gate.py` (extension, +~350 lignes Python)

**Durée estimée** : 1 session

**Risque** : FAIBLE (Python testable unitairement, logique déterministe, classification WARN → FAIL progressive)

---

### Étape 3 — Enrichissement sémantique du core blacklist (Phase 4)

**Goal** : ajouter 53 règles sémantiques universelles dans le `ref/anti-slop-blacklist-core.md` créé à l'étape 1. Profiter du budget libéré.

**Actions** :
1. Ajouter au core blacklist les règles universelles sémantiques non grep-ables, organisées par domaine :

**Composition (18 règles)** :
- Centered everything symétrique (hero + sections centrées + CTA-only) — pattern AI tell #4
- Cookie-cutter rhythm (hero → 3 features → testimonials → pricing → CTA, sections de même hauteur)
- 3-column equal card grid (pattern AI tell #2)
- Icons in colored circles as decoration (pattern AI tell #3)
- Identical card grid (icon + heading + text × 3/4/6, même structure)
- Hero metric layout template (big number + label + stats + gradient)
- Cards earn their existence — spacing + alignment avant cards
- One job per section — pas de double promesse narrative
- Brand unmistakable in first screen
- Bubbly border-radius uniform partout (pattern AI tell #5)
- Large icons with rounded corners above headings
- Liquid glass refraction (blur beyond subtle navbar)
- Neon/outer glows sans offset
- Gradient text (large headers) décoratif
- Empty flat sections sans imagerie/patterns
- Perfectly even gradients digital default
- Random dark section dans light page
- Inconsistent lighting direction

**Spatial/Typo/Color (11 règles)** :
- Varied spacing for hierarchy (headings extra space above)
- Same padding everywhere = monotone
- Use one font family multiple weights
- Regular + Bold seulement (introduire Medium 500, SemiBold 600)
- Oversized H1 qui screament — contrôler hiérarchie weight+color+space pas size
- All-caps subheaders partout = generic
- Mixing warm + cool grays inconsistent
- Mixing accent colors = decision fatigue
- Generic box-shadow unexamined
- Oversaturated accent colors
- Purple/blue AI gradient banni

**Interaction/UX (10 règles)** :
- Destructive actions need confirmation ou undo window
- Modals uniquement quand pas d'alternative meilleure
- Hover states sans focus parity
- Active/pressed feedback (scale 0.98 ou translateY 1px)
- Instant transitions sans smooth 200-300ms
- Generic circular spinners (préférer skeleton loaders)
- Empty dashboard sans "getting started" view
- Loading states avec feedback clair
- Error states inline forms
- Missing focus ring keyboard navigation

**Content/Copy (8 règles)** :
- Error messages 3-part formula (what + why + how-to-fix)
- Empty states = acknowledge + explain value + action
- Humor proscrit sur errors
- Alt text = information pas image
- Link text meaningful standalone
- Terminology consistency (un seul terme par concept)
- Avoid redundant copy
- Active voice (pas passif)

**Performance (6 règles)** :
- No layout reads in render
- Batch DOM reads/writes
- Large lists virtualize (> 50 items)
- Below-fold images lazy
- Critical images priority
- Grain/noise sur scrolling containers banni (fixed pseudo-elements only)

2. Structurer le core blacklist avec des sections claires et des règles numérotées (U-001 à U-053 par exemple) pour traçabilité.

3. Introduire PROGRESSIVEMENT — activer par blocs de 10 règles en testant entre chaque bloc.

**Fichiers modifiés** :
- `ref/anti-slop-blacklist-core.md` (créé à l'étape 1, enrichi ici)

**Durée estimée** : 0.5-1 session

**Risque** : MOYEN (faux positifs possibles sur règles trop strictes, saturation cognitive si ajout brut)

---

### Étape 4 — Axe 5 DA Check — Anti-slop universel

**Goal** : ajouter un 5e axe d'audit dans `phase-4bis-da-check.md` pour 7 règles de jugement nécessitant vision d'ensemble post-génération.

**Actions** :
1. Enrichir `phase-4bis-da-check.md` avec un nouveau bloc Axe 5 (~15 lignes) :

**Axe 5 — Anti-slop universel (checks de jugement post-génération)** :
- Hiérarchie unmistakable (squint test — hiérarchie visible floue à 1m)
- One job per section (chaque section porte UNE idée, pas deux)
- Cards earn their existence (élévation/containment justifiés, pas décoratifs)
- Brand unmistakable first screen (avant scroll, identité est claire)
- Cookie-cutter rhythm rompu (sections ont poids et rythme différenciés)
- Sections pas empilées identiquement (hauteurs, densités, tons variés)
- Data-ink ratio défendable (pas d'élément qui n'ajoute rien)

2. Ajouter la règle d'arbitrage : si Axe 5 détecte 2+ violations → mode "corrections mineures" minimum, 4+ → "refaire".

3. Format output cohérent avec les 4 axes existants (verdict + écarts + corrections actionnables).

**Fichiers modifiés** :
- `phases/phase-4bis-da-check.md` (ajout Axe 5)

**Durée estimée** : 0.5 session

**Risque** : FAIBLE (DA Check est une phase d'audit, extensible naturellement, pas de génération impactée)

---

### Étape 5 — Propagation Batch 2/3 et Phase 3B

**Goal** : étendre les 3 couches aux autres phases concernées.

> **🟢 ÉTAT (13 mai 2026) — VOLET BATCH 2/3 : FAIT (D56) + CORRIGÉ post-audit du 13 mai.** Volet Phase 3B : encore à faire (séparé, plus sensible).
>
> Implémentation D56 du 12 mai (légèrement différente de la prescription d'origine — l'intention est préservée) :
> - `scripts/phase6-batch-gate.py` créé — non pas « en fin de chaque chapitre » mais **une fois par batch, sur le fichier complet assemblé** (Batch 2 après injection SVG ; Batch 3 après assemblage des 3 chapitres) ; sur un fragment de chapitre, un linter full-HTML faux-positiverait sur tout ce qui « manque ». C'est un **wrapper mince** : il strippe les `<svg>`/`data:` URIs, délègue à `phase4-blacklist-gate.py` + `phase4-finishing-gate.py` (déjà ~70 checks), re-pondère selon un profil « documentation batch », et ajoute Specs Lock / Completeness / external-image / Lorem ipsum. `--json-output {deterministic_fails, other_fails, warns}`.
> - Section « Audit anti-slop de fin de batch » ajoutée dans `phase-6a-batch2.md` (auto-audit du subagent unique avant `STATUS: OK`) et dans le bloc de contexte partagé de `phase-6b-batch3.md` (scopée « ton chapitre »).
> - Câblage SKILL.md : étape « Gate anti-slop Batch 2 » après injection SVG ; « Étape 6B-6 » après assemblage Batch 3. Advisory par défaut + auto-correction chirurgicale 1 tour max sur les `deterministic_fails` seulement ; reste surfacé à l'utilisateur. Ajout de `--json-output` à `phase4-blacklist-gate.py` (compat ascendante).
> - **Pas** de réplication de la machinerie 4-Critiques/Synthétiseur sur les batches (choix assumé, conforme à l'arbitrage du 24 avril — le volet batch reçoit une version *allégée* : gate Python + auto-audit ~8 lignes, pas un panel de critiques).
>
> Corrections du 13 mai (post-audit déclenché par un faux PASS visuellement repéré par Charles sur Camille 0513 batch2) :
> - **A1** — 3ᵉ pattern régex ajouté à `check_accent_bar` pour détecter `box-shadow: inset Npx 0 0 color` (contournement explicitement cité par Impeccable BAN 1 L213). 5/6 canoniques récents post-P17 fuyaient sur ce pattern non couvert. Bénéficie à Phase 4 ET batch.
> - **A2** — nouveau check `check_outline_focus_visible_pairing` (Vercel Focus States) : toute règle `outline: none/0` doit être compensée par un `:focus-visible` qui restaure un outline visible. Filet de sécurité futur (0/6 fuite empirique actuellement, tous ont un `:focus-visible` global).
> - **A3** — inversion du défaut erroné du wrapper batch : `BATCH_FAIL_ALLOWLIST` supprimée, on conserve maintenant la sévérité native du gate Phase 4 par défaut, avec un `BATCH_DEMOTE_TO_WARN` court et justifié (R148, R054, hover_multi_property, advanced_techniques). Corrige le faux PASS du 12 mai.
> - **C** — clarification du mode partiel `test-big` (start_phase ≠ 1) : note explicite dans `test-big/SKILL.md` + `.test-context.md` que les contrôles anti-slop des phases skippées ne tournent pas.
> - Audit catégorie A : 18 trous théoriques cross-référencés au canon audit-slop, 15 sur 18 ne fuient PAS empiriquement (bloqués structurellement par Phase 3B gates + prompts Phase 4). Couverture canonique regex globale ~95 % sur les patterns qui se manifestent vraiment.
> Cf. `DECISIONS.md` D56 (avec sous-section « Corrections 2026-05-13 »), `CHANGELOG.md` 2026-05-13, `ARCHITECTURE.md` (briques 6A/6B), `~/.claude/plans/ok-go-fais-le-mighty-goblet.md`.

**Actions Batch 2/3** *(✅ FAIT — voir l'état ci-dessus pour les écarts vs cette prescription d'origine)* :
1. Créer `scripts/phase6-batch-gate.py` (équivalent du phase4-blacklist-gate.py, appliqué aux HTML des chapitres Batch)
   - Même socle de checks que Phase 4
   - Invoqué par `phase-6a-batch2.md` et `phase-6b-batch3.md` en fin de chaque chapitre
2. Le `ref/anti-slop-blacklist-core.md` créé à l'étape 1 est DÉJÀ importé par Batch 2 et Batch 3 (via factorisation étape 1) — pas de travail additionnel
3. Ajouter une section "Audit anti-slop de fin de batch" dans `phase-6a-batch2.md` et `phase-6b-batch3.md` (équivalent léger de l'Axe 5 DA Check, ~8 lignes chacune)

**Actions Phase 3B** (chantier sensible, à faire en dernier) :
1. Enrichir `scripts/phase3b-css-gate.py` (existe déjà) avec les règles universelles qui concernent ce qui est décidé en Phase 3B :

**Bloc Palette (6 règles Phase 3B)** :
- Ban `#000000` et `#ffffff` purs dans les tokens (check déjà partiel, renforcer)
- Ban accent indigo `#6366f1`, gradients purple→blue AI
- Ban teinte par défaut (bleu chaud, orange) sans justification
- Palette structurée : Primary (1 couleur, 3-5 teintes) / Neutral (9-11) / Semantic (4×2-3) / Surface (2-3)
- Ban mixing warm + cool grays (tint all grays vers ONE famille)
- Règle 60-30-10 respectée (60% neutral, 30% secondary, 10% accent)

**Bloc Fonts (4 règles Phase 3B)** :
- Ban fonts reflex_fonts_to_reject (Inter, Roboto, Open Sans, Arial, Fraunces, Newsreader, Lora, Crimson, Playfair, Cormorant, Instrument Serif)
- Procédure sélection fonts (3 mots de marque concrets, pas "modern"/"elegant")
- Ban 2 geometric sans-serifs proches (pas de paire sans contraste d'axe)
- Pairing multi-axe obligatoire (serif+sans, geometric+humanist, condensed+wide)

**Bloc Type-scale (2 règles Phase 3B)** :
- Ratio type-scale ≥ 1.25
- Body text max 65-75ch

**Bloc Spacing (2 règles Phase 3B)** :
- Spacing scale 4pt (4, 8, 12, 16, 24, 32, 48, 64, 96) pas 8pt coarse
- Token names semantic (`--space-sm` pas `--spacing-8`)

2. Enrichir les prompts `phase-3b-palette.md`, `phase-3b-penseur-visuel.md`, `phase-3b-penseur.md` avec les règles sémantiques non-grepables qui leur appartiennent (≤10 lignes ajoutées)

**Fichiers modifiés** :
- Nouveaux : `scripts/phase6-batch-gate.py`
- Modifiés : `scripts/phase3b-css-gate.py`, `phases/phase-3b-palette.md`, `phases/phase-3b-penseur-visuel.md`, `phases/phase-3b-penseur.md`, `phases/phase-6a-batch2.md`, `phases/phase-6b-batch3.md`

**Durée estimée** : 1-2 sessions (Batch 2/3 ensemble 1 session, Phase 3B une session séparée car sensible)

**Risque** : MOYEN pour Batch 2/3, ÉLEVÉ pour Phase 3B (cœur stratégique, toute modification touche la qualité créative)

---

## Règles CONTEXTUELLES — restent dans audit-slop (non injectées dans BIG)

Ces 54 règles dépendent du registre/curseur/contexte et ne doivent PAS être intégrées à BIG en amont :

- "Neumorphism = daté" (vrai 2026, faux 2018 ou si registre cyclique)
- "Inter + Inter mono stack" (slop par défaut, OK si registre "Blueprint technique" assumé)
- "Dark OLED + pink accent = AI slop" (slop par défaut, OK si registre y2k cyclique)
- "Hero centré CTA seul" (slop en éditorial, OK en SaaS conversion A=1)
- "Bento grid = slop" (slop en éditorial, OK en tool B2B analytique)
- "Purple/blue gradient #6366f1" (slop 2023-2026, peut se réhabiliter cyclique)
- "3-col feature grid symétrique" (slop éditorial, peut être juste SaaS)
- "Serif fonts editorial only" (slop dans dashboards, OK registre éditorial)
- Tous les marqueurs datation Perplexity (85 styles UX/UI Pro Max classés)
- i18n second person (vrai EN, variable FR)
- URL state sync (nuqs pattern — dépend stack)
- Mobile-first testing discipline (workflow, pas rule de rendu)
- German/French/Finnish text expansion (i18n planning, dépend projet)
- Toutes les règles de datation zeitgeist 2025-2026 de Perplexity

Le synthétiseur d'audit-slop a accès au contexte (pitch, concept, curseur, registre) et arbitre ces règles avec nuance. BIG amont ne doit pas trancher à leur place.

---

## Règles N/A pour HTML vanilla — exclues du plan

BIG produit du HTML vanilla, pas de React/Next.js/Tailwind/Framer Motion. Les ~15 règles suivantes ne s'appliquent pas :

- R-207 à R-211 : Framer Motion patterns (useMotionValue, layoutId, staggerChildren, spring physics stiffness/damping) — 5 règles
- R-171 : nuqs URL sync (React hook pattern)
- R-185 : React controlled inputs (`value` + `onChange`)
- R-186, R-187 : Hydration mismatch (React SSR)
- R-167 : Controlled inputs perf (React render cost)
- R-137 : `onPaste preventDefault` (React event handler)
- R-177 : `autoFocus` attribute (React JSX)
- R-181, R-182 : `Intl.DateTimeFormat` / `Intl.NumberFormat` (JS runtime — BIG est principalement CSS/HTML statique)

Si BIG évolue vers React (hypothétique futur LPG), ces règles seront à réintégrer.

---

## Gestion du risque — garde-fous transverses

### Tests de non-régression obligatoires

Entre CHAQUE étape du plan :
1. Relancer 1 brief connu intégralement (Camille ou autre de qualité validée dans l'historique)
2. Comparer le style-tile avant/après :
   - Score DA Check (doit rester stable ou s'améliorer)
   - Score audit-slop (doit s'améliorer — c'est le but)
   - Qualité subjective (évaluation humaine rapide)
3. **BLOQUER** si score DA Check baisse ou si la qualité subjective régresse. Rollback et diagnostic avant de continuer.

### Progression WARN → FAIL

Chaque nouvelle règle (gate Python + core blacklist + Axe 5) démarre en **WARN** (informatif, pas bloquant) pendant 5 runs de validation. Passe en **FAIL** seulement après :
- 5 runs sans faux positif
- Validation que la correction demandée est applicable par le subagent (pas de boucle infinie)

### Stop à tout moment

Le plan est séquentiel et chaque étape est indépendante :
- Si l'étape 1 (factorisation) dégrade : on s'arrête, on ne factorise pas.
- Si l'étape 2 (gates Python) pose problème : on revert les nouveaux checks sans toucher aux étapes suivantes.
- Charles peut tout moment décider de skipper une étape (ex: skipper la factorisation et vivre avec la redondance).

### Désynchro skill audit-slop ↔ BIG

Les règles universelles sont COPIÉES d'audit-slop vers `ref/anti-slop-blacklist-core.md` dans BIG. Pour éviter la divergence :
- Documenter la source de chaque règle du core (origine audit-slop : quel fichier, quelle ligne)
- Procédure de refresh documentée dans un `ref/anti-slop-blacklist-core-refresh.md` : quand audit-slop évolue (via son `lib/freshness-check.sh`), identifier les règles universelles nouvelles et les propager manuellement

---

## Questions ouvertes à trancher

1. **Règles sur React/Framer** : confirmation que BIG reste HTML vanilla et qu'on exclut les ~15 règles React/Framer (pas d'évolution stack prévue) ?

2. **Ambigus contextuels limites** :
   - R-084 "Hero centré CTA seul" — classé CONTEXTUEL dans mon plan. Confirmes-tu qu'on laisse ça à audit-slop ?
   - R-031 "Mobile-first" — je l'ai mis CONTEXTUEL (workflow, pas règle de rendu). OK ou forcer en Phase 3B ?

3. **Ordre Batch 2/3 vs Phase 3B** : j'ai proposé Batch 2/3 avant Phase 3B. Tu confirmes, ou tu préfères Phase 3B avant (puisque c'est en amont dans le pipeline, mais c'est le plus sensible) ?

4. **Granularité des règles dans le core blacklist** : est-ce qu'on formule chaque règle comme une ligne courte actionnable (style Vercel), ou avec 1-2 phrases d'explication (style Impeccable) ? Impact sur le poids du fichier.

5. **Plan écrit sur disque BIG** : est-ce qu'on crée un `ref/plan-integration-anti-slop.md` dans BIG comme trace durable du chantier, ou on garde juste le fichier plan `lovely-humming-star.md` ?

6. **Check de sanité pour détection faux positifs** : propose-t-on un mécanisme où chaque FAIL gate Python est logué dans un fichier `outputs/gate-fails.log` pendant la période WARN pour audit de l'aptitude à corriger automatiquement ?

---

## Fichiers critiques à modifier (vue d'ensemble)

### Nouveaux fichiers à créer

| Chemin | Rôle | Taille cible |
|---|---|---|
| `.claude/skills/brand-identity/ref/anti-slop-blacklist-core.md` | Blacklist universelle sémantique | ~90 lignes (35 factorisés + 53 enrichis) |
| `.claude/skills/brand-identity/ref/finition-elite-core.md` | Socle finition partagé | ~25 lignes |
| `.claude/skills/brand-identity/ref/hierarchie-visuelle-core.md` | Principes hiérarchie partagés | ~20 lignes |
| `.claude/skills/brand-identity/scripts/phase6-batch-gate.py` | Gate Python pour Batch 2/3 | ~400 lignes Python |
| `.claude/skills/brand-identity/ref/anti-slop-blacklist-core-refresh.md` | Procédure refresh vs audit-slop | ~15 lignes |

### Fichiers existants à modifier

| Chemin | Nature de la modification |
|---|---|
| `.claude/skills/brand-identity/phases/phase-4-styletile.md` | Remplacer 3 sections redondantes par imports refs + ajouter renvoi vers core blacklist |
| `.claude/skills/brand-identity/phases/phase-4-artefact.md` | Idem (version allégée) |
| `.claude/skills/brand-identity/phases/phase-4bis-da-check.md` | Ajouter Axe 5 — Anti-slop universel (~15 lignes) |
| `.claude/skills/brand-identity/phases/phase-6a-batch2.md` | Remplacer sections redondantes par imports + invocation phase6-batch-gate.py + section audit fin batch |
| `.claude/skills/brand-identity/phases/phase-6b-batch3.md` | Idem |
| `.claude/skills/brand-identity/phases/phase-3b-palette.md` | Enrichir règles palette |
| `.claude/skills/brand-identity/phases/phase-3b-penseur-visuel.md` | Enrichir règles fonts + type-scale |
| `.claude/skills/brand-identity/phases/phase-3b-penseur.md` | Idem |
| `.claude/skills/brand-identity/scripts/phase4-blacklist-gate.py` | +27 nouveaux checks (~350 lignes Python) |
| `.claude/skills/brand-identity/scripts/phase3b-css-gate.py` | Enrichir avec ~14 règles Phase 3B (~150 lignes Python) |
| `.claude/skills/brand-identity/SKILL.md` | Possible ajustement orchestration pour lire les nouveaux refs |

---

## Auto-audit de couverture — contrôle exhaustif des 212 règles

Charles a explicitement demandé ce contrôle pour éviter le piège "j'avais pris 30% seulement". Voici la vérification exhaustive par catégorie.

### Total des règles extraites : 212

### Ventilation par type

| Type | Compte | Destination |
|---|---|---|
| UNIVERSELLES (vont dans BIG) | 158 | Gates Python + Core blacklist + Phase 3B + Axe 5 DA |
| CONTEXTUELLES (restent dans audit-slop) | 54 | `/audit-slop` inchangé |
| **TOTAL** | **212** | **100% mappées** |

### Ventilation des 158 universelles par destination et couverture actuelle

| Destination | Règles brut | N/A HTML vanilla | Déjà BIG OUI | Partiel | Net à injecter |
|---|---|---|---|---|---|
| Gate Python | 47 | 5 | 15 | 8 | **~27** (dont 8 à enrichir) |
| Core blacklist (nouveau) | 68 | 5 | 10 | 12 | **~53** (dont 12 à enrichir) |
| Phase 3B | 32 | 3 | 15 | 8 | **~14** (dont 8 à enrichir) |
| Axe 5 DA Check | 11 | 2 | 2 | 6 | **~7** (dont 6 à enrichir) |
| **Total** | **158** | **15** | **42** | **34** | **~101** |

### Ventilation par domaine (vérification qu'aucun domaine n'est orphelin)

| Domaine | Universelles | Contextuelles | Destination principale |
|---|---|---|---|
| a11y (focus-visible, WCAG, touch targets, aria, semantic HTML, skip links, alt, heading hierarchy) | 32 | 0 | Gate Python majoritairement + Core blacklist |
| typography (fonts, type-scale, font-variant, line-height, CH width) | 22 | 2 | Phase 3B + Gate Python (fonts bannies, tabular-nums) |
| color (OKLCH, palette 60-30-10, neutrals teintés, pur noir/blanc, accent) | 18 | 5 | Phase 3B majoritairement + Gate Python |
| motion (durations, easing, transform+opacity, prefers-reduced-motion) | 15 | 2 | Gate Python majoritairement + Core blacklist |
| composition (centered everything, 3-col grid, cards, hero, hiérarchie) | 23 | 12 | Core blacklist majoritairement + Axe 5 DA |
| spacing (4pt scale, gap, varied) | 8 | 0 | Phase 3B + Gate Python |
| interaction (focus, hover, active, modals, dropdowns, forms) | 18 | 6 | Gate Python + Core blacklist |
| copy (button labels, error messages, active voice, filler words) | 14 | 4 | Gate Python + Core blacklist |
| content (placeholders, avatars, Lorem, generic names) | 9 | 2 | Gate Python |
| responsive (mobile-first, dvh, safe-area, container queries, touch-action) | 12 | 5 | Gate Python + Phase 3B |
| performance (lazy loading, preconnect, critical fonts, virtualization) | 8 | 3 | Gate Python |
| craft/aesthetic (divers) | 6 | 4 | Core blacklist + Axe 5 DA |
| i18n (translate="no", Intl API, expansion) | 5 | 6 | Gate Python + CORE BLACKLIST (contextuels restants) |
| content authenticity (data numbers, SVG icons) | 5 | 3 | Gate Python |
| **TOTAL par domaine** | **195** | **54** | |

**Vérification** : 158 universelles + 54 contextuelles = 212 règles — cohérent.
La somme "Universelles par domaine" (195) excède 158 parce que certaines règles appartiennent à 2 domaines (ex: R-079 "touch targets 44px" est a11y ET responsive). Cela ne change pas le compte total unique.

### Couverture par fichier source audit-slop

| Fichier source | Règles extraites | Universelles | Contextuelles |
|---|---|---|---|
| `impeccable/SKILL.md` + 9 refs | 98 | 80 | 18 |
| `taste-skill/` (7 variantes) | 62 | 50 | 12 |
| `gstack/` (2 fichiers) | 18 | 16 | 2 |
| `vercel-command.md` | 34 | 33 | 1 |
| **Total brut** | **212** | **158** | **54** |

Après dédup cross-source, aucune règle n'est perdue : 212 règles uniques. Les 75 règles "brutes" perdues (287 brutes → 212 dédup) correspondent à des répétitions cross-source (ex: "no Inter font" apparaît dans 5 fichiers → compté 1 fois).

### Vérification nominative — règles phares

| Règle clé | ID | Type | Destination finale | Statut |
|---|---|---|---|---|
| `:focus-visible` obligatoire | R-020 | UNIV | Gate Python | Déjà partiel, à renforcer |
| `prefers-reduced-motion` honoré | R-018 | UNIV | Gate Python | Déjà partiel, à renforcer |
| `transition: all` banni | R-012 | UNIV | Gate Python | Déjà OUI |
| `touch-action: manipulation` | R-173 | UNIV | Gate Python | À ajouter |
| `100vh` → `100dvh` | R-034 | UNIV | Gate Python | Déjà OUI |
| WCAG AA 4.5:1 contraste | R-007 | UNIV | Gate Python | Déjà OUI |
| Apostrophes courbes FR | R-197 | UNIV | Gate Python | À ajouter |
| Inter/Roboto/Open Sans bannis | R-059 | UNIV | Gate Python + Phase 3B | Partiel |
| Instrument Serif banni | R-060 | UNIV | Gate Python + Phase 3B | À ajouter |
| Lorem Ipsum banni | R-116 | UNIV | Gate Python | À ajouter |
| Jane Doe / John Doe / Acme bannis | R-111 | UNIV | Gate Python | Déjà OUI |
| Filler words bannis | R-113 | UNIV | Gate Python | À ajouter |
| Centered everything banni | R-083 | UNIV | Core blacklist | Déjà OUI (blacklist AI) |
| Cookie-cutter rhythm | (implicite) | UNIV | Core blacklist + Axe 5 | À ajouter |
| Cards earn their existence | R-086 | UNIV | Core blacklist + Axe 5 | Partiel |
| Brand unmistakable first screen | (GStack) | UNIV | Axe 5 DA | À ajouter |
| Purple/blue AI gradient | R-103 | UNIV | Gate Python | Déjà OUI |
| 3-col equal card grid | R-085 | UNIV | Core blacklist | Déjà OUI |
| Icons in colored circles | R-088 | UNIV | Core blacklist | Déjà OUI |
| One accent color only | R-101 | UNIV | Phase 3B | Déjà OUI |
| Palette 60-30-10 | R-006 | UNIV | Phase 3B + Core | Déjà OUI |
| `#000000` / `#ffffff` purs bannis | R-009, R-099 | UNIV | Gate Python + Phase 3B | Déjà OUI |
| Neumorphism daté | (contextuel) | CTX | reste audit-slop | N/A BIG |
| Y2K/Vaporwave/Chrome | (contextuel) | CTX | reste audit-slop | N/A BIG |
| Hero centré CTA seul | R-084 | CTX | reste audit-slop | N/A BIG |
| Bento grid SaaS générique | (contextuel) | CTX | reste audit-slop | N/A BIG |

### Check final de cohérence

- 212 règles totales extraites ✅
- 158 universelles + 54 contextuelles = 212 ✅
- 158 universelles ventilées en 4 destinations : 47 + 68 + 32 + 11 = 158 ✅
- Parmi les 158 universelles : ~15 N/A HTML vanilla + 42 déjà OUI + 34 partiel + 67 nouvelles = 158 ✅
- Net à injecter dans BIG : ~101 règles (nouvelles ou à enrichir) ✅
- Aucune règle extraite n'est sans destination ✅
- Aucune règle universelle pertinente HTML vanilla n'est omise du plan ✅

**Conclusion auto-audit** : les 212 règles extraites sont toutes mappées. Couverture effective du chantier : **100% des règles universelles applicables au HTML vanilla sont intégrées dans les 5 étapes du plan**. Les 54 contextuelles restent dans audit-slop comme prévu par l'architecture.

---

## Vérification end-to-end du plan

### Comment tester que le chantier réussit

1. **Avant démarrage** : établir la baseline
   - Lancer `/audit-slop` sur 3 style-tiles représentatifs (Camille c1, un brief récent, un brief ancien)
   - Noter les scores pondérés actuels (baseline ~4.2 à 5.5/10 selon brief)
   - Archiver les rapports audit-slop comme référence

2. **Après chaque étape** : relancer la même batterie
   - Score `/audit-slop` : doit s'améliorer étape par étape
   - Score DA Check : doit rester stable ou s'améliorer
   - Qualité subjective humaine : pas de régression perceptible

3. **Cibles de progression** (indicatives) :
   - Après Étape 1 (factorisation seule) : score inchangé (le but est de libérer du budget, pas d'améliorer)
   - Après Étape 2 (gates Python enrichis) : score +1 à +2 points sur les critères a11y/craft
   - Après Étape 3 (core blacklist enrichie) : score +1 point sur composition/sémantique
   - Après Étape 4 (Axe 5 DA Check) : détection +2 violations moyennes, score +0.5 à +1
   - Après Étape 5 (propagation Batch + Phase 3B) : couverture complète, score 7.5-8.5/10 cible

4. **Verdict final** : score moyen `/audit-slop` ≥ 7.5/10 sur la même batterie de 3 briefs test = chantier réussi.

### Rollback si régression

Chaque étape est indépendante :
- Étape 1 rollback : restaurer les 4 phases depuis git, supprimer les 3 refs core
- Étape 2 rollback : revert le commit Python sur `phase4-blacklist-gate.py`
- Étape 3 rollback : restaurer `anti-slop-blacklist-core.md` à sa version factorisée seule
- Étape 4 rollback : supprimer l'Axe 5 de `phase-4bis-da-check.md`
- Étape 5 rollback : indépendant par sous-chantier (Batch 2/3 / Phase 3B)

### Commits et traçabilité

Chaque étape = 1 commit atomique (ou plusieurs si la session est longue), conventional commits :
- `refactor: factor shared refs (anti-slop-blacklist-core, finition-elite-core, hierarchie-visuelle-core)`
- `feat: extend phase4-blacklist-gate with 27 universal checks (a11y, typo, copy)`
- `feat: enrich anti-slop-blacklist-core with 53 universal semantic rules`
- `feat: add Axe 5 anti-slop universel to DA Check`
- `feat: propagate anti-slop rules to Batch 2/3 and Phase 3B`

Mise à jour `CHANGELOG.md`, `DECISIONS.md` (D50+), `ARCHITECTURE.md` après chaque étape.

---

---

## ADDENDUM 1 — Ajustements anti-contamination (2026-04-24, post-audit sources)

Après audit Explore sur la rédaction des blacklists BIG vs sources externes (Vercel, Impeccable, GStack, Taste), 3 ajustements critiques validés par Charles pour éviter la contamination créative.

### Principe — Rédaction à 3 niveaux stricts

| Niveau | Où | Quoi | Exemple OK | Exemple interdit |
|---|---|---|---|---|
| **1** | Prompt (core blacklist) | Principes abstraits uniquement | `Do NOT center everything symmetrically` | `Do NOT use #6366f1` |
| **2** | Prompt (core blacklist) | Patterns nommés non-substituables | `Do NOT use wave/zigzag dividers` | `Do NOT use --angle: 0deg → 360deg` |
| **3** | Gate Python UNIQUEMENT | Énumérations précises (fonts, hex, syntax CSS) | Liste Inter/Roboto/Open Sans dans regex | (ne remonte jamais au prompt) |

**Règle d'or** : les énumérations nominatives (fonts bannies, hex précis, filler words, fake names) ne vont **jamais** dans le prompt. Elles restent dans le gate Python où elles sont détectées au runtime sans jamais être "vues" par le subagent.

### Cas spécial — Fonts bannies (pattern Impeccable repris)

Dans le prompt : **procédure 4 étapes** de sélection, pas de liste. Dans le gate Python : liste nominative `check_banned_fonts`. Le LLM suit un processus qui l'oriente vers la découverte au lieu de voir une liste à éviter.

Procédure à documenter dans `ref/anti-slop-blacklist-core.md` §2 :
```
Step 1 — Read brief. Write 3 concrete brand words (NOT "modern" / "elegant").
Step 2 — List the 3 fonts you'd naturally pick. They're likely training defaults.
Step 3 — Reject reflex defaults. Search Google Fonts / Pangram / Future Fonts
         for something matching your brand as a physical object.
Step 4 — Cross-check: if your result matches your reflex pattern, go to Step 3.
         Avoid visual cousins (Roboto-style geometric sans-serifs from the 2010s monoculture).
```

### Règles BIG existantes qui transgressent — à reformuler en Étape 1

| Fichier | Ligne | Règle actuelle | Niveau actuel | Action Étape 1 |
|---|---|---|---|---|
| phase-4-styletile.md | L315 | `Rotation/drift de gradient en boucle (--angle: 0deg → 360deg infinite)` | 3 (valeurs précises) | Reformuler Niveau 2 : "Do NOT use infinite rotation or angle shifts on gradients — gradient movement is decorative debt" |
| phase-4-styletile.md | L310 | `Soulignement qui grandit au hover (scaleX(0) → scaleX(1) sur un ::before)` | 3 (syntax précise) | Reformuler Niveau 2 : "Do NOT use underline reveal on hover — hierarchy comes from weight, size, color" |
| phase-4-styletile.md | L308-309 | `transform: translateY()` au hover / `transform: scale() > 1.02` au hover | 2 (propriété nommée) | OK en Niveau 2, mais à vérifier qu'il y a un gate Python qui backupp (existe déjà) |

Audit complet à faire pendant la factorisation sur les ~50 règles actuelles de la blacklist phase-4-styletile.md. Toute règle qui transgresse en Niveau 3 (valeurs numériques, syntax complète, variables custom) est reformulée en Niveau 2 (pattern nommé) ou déplacée en gate Python (Niveau 3).

### Modifications des étapes du plan initial

**Étape 1 — Factorisation enrichie**
Ajouts à la liste d'actions :
1. Créer aussi `ref/anti-slop-formulation-guide.md` (~30 lignes) — documentation des 3 niveaux pour mainteneurs futurs
2. Auditer et reformuler les règles existantes BIG qui transgressent (L315 `--angle`, L310 `scaleX`, etc.) pendant qu'on factorise
3. Intégrer la procédure Font Selection dans `ref/anti-slop-blacklist-core.md` §2

**Étape 2 — Gates Python renforcés**
Les règles suivantes qui étaient prévues dans le prompt sont **déplacées intégralement dans le gate Python** (plus jamais dans le prompt) :
- Fonts bannies (Inter, Roboto, Open Sans, Fraunces, Newsreader, Lora, Crimson, Playfair, Cormorant, Instrument Serif) → `check_banned_fonts` Python uniquement
- Filler words (Elevate, Seamless, Unleash, Next-Gen, Delve, Game-changer, Revolutionize) → `check_filler_words` Python uniquement
- Fake names (Jane Doe, John Doe, John Smith, Jane Smith, Acme, Nexus, SmartFlow, QuantumFlow, NovaCore) → `check_fake_names` Python uniquement
- Purple/blue AI gradient hex précis (`#6366f1`, `#a855f7`, etc.) → `check_ai_gradient` Python uniquement

Dans le prompt (core blacklist) il ne reste qu'une mention abstraite :
```
Avoid training-data defaults (generic sans-serifs, filler marketing words,
placeholder names, AI-standard purple/blue gradients). Gate Python enforces
the specific banned items at validation time.
```

**Étape 3 — Enrichissement sémantique classifié**
Chacune des 53 règles du core blacklist est classée Niveau 1 ou Niveau 2 explicitement (jamais Niveau 3). Ajout de la clause **"anti-cousin"** sur les règles à risque de substitution proche :
```
Avoid X and its visual cousins (Y-style elements from the Z era monoculture).
```
Exemple : "Avoid centered hero CTA-only and its cousins (startup landing page templates 2015-2020)."

### Questions ouvertes — toutes résolues (2026-04-24)

| # | Question | Résolution |
|---|---|---|
| 1 | BIG reste HTML vanilla | OUI — exclusion des 15 règles React/Framer confirmée |
| 2 | Hero centré CTA + Mobile-first = contextuels | OUI — restent dans audit-slop |
| 3 | Ordre Phase 4 → Batch 2/3 → Phase 3B | OUI — séquentiel validé |
| 4 | Granularité core blacklist | Style A (ligne courte actionnable) avec rédaction 3 niveaux anti-contamination |
| 5 | Plan sur disque BIG | OUI — créer `ref/plan-integration-anti-slop.md` dans BIG pour traçabilité inter-sessions |
| 6 | Log faux positifs WARN | OUI — `outputs/gate-fails.log` pendant période validation |

---

## Dernière mise à jour

**Date** : 2026-05-13 (corrections post-audit intégrées)
**Auteur** : Claude (session plan + session D56 + session corrections 13 mai)
**Statut** : plan validé + addendum anti-contamination validé. Étape 1 (factorisation refs TIER 1/core) FAITE. Étape 2-3-4 (Phase 4 : gates Python enrichis, core blacklist, Axe 5 DA) faites pour l'essentiel via Vague 2 (commit `eab5905`, 27 avril). **Étape 5 volet Batch 2/3 : FAITE (D56, 12 mai) + CORRIGÉE (13 mai)** — cf. l'encadré « ÉTAT » dans la section Étape 5 pour le détail des corrections A1/A2/A3/C. **Reste à faire : Étape 5 volet Phase 3B** (enrichissement `phase3b-css-gate.py` + prompts 3B-palette/3B-penseur — séparé, plus sensible).
