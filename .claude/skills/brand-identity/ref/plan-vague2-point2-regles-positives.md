# Plan Vague 2 — Point 2 : Intégration des règles anti-slop POSITIVES des skills externes

## Contexte

Identifié en ultrathink le 25 avril 2026 : les sources externes (Vercel, Impeccable, GStack, Taste) contiennent **~50 règles positives** ("Use X for Y") en plus des règles négatives. Vague 1 n'a pas importé ces positives. Filtre BIG style-tile : ~20 règles vraiment pertinentes (BIG = HTML vanilla vitrine + artefact mini-app, pas une app complète).

**Cible** : enrichissement qualitatif du craft (typo polish, perf, mobile, color cohesion). Score audit-slop attendu marginal (+0.3-0.5 pt) — surtout impact qualité visuelle perceptible.

## Inventaire — 20 règles positives à intégrer

### HAUTE PRIORITÉ (12 règles — vrai impact qualité visuelle)

| # | Règle positive | Source | Destination probable |
|---|---|---|---|
| 1 | **Multi-dimension hierarchy** : size + weight + color + position + space combinés (pas juste size) | Impeccable spatial | TIER 1 (`hierarchie-visuelle-tier1.md`) — anti-sur-emphasis |
| 2 | **Squint test** comme principe d'évaluation général (pas seulement CTA) | Impeccable spatial | TIER 1 (`hierarchie-visuelle-tier1.md`) — principe transversal |
| 3 | **Z-index semantic scale** (dropdown 100 / sticky 200 / modal-backdrop 300 / modal 400 / toast 500 / tooltip 600) | Impeccable + Vercel | Phase 3B (`phase-3b-palette.md` — tokens) |
| 4 | **Shadow tinted to background hue** (pas pur noir/opacity) | Impeccable + Taste | Critique TIER 2 (`finition-elite-core.md`) |
| 5 | **Light text on dark = +0.05-0.1 line-height extra** | Impeccable typography | Phase 3B (type-scale) ou Critique TIER 2 |
| 6 | **Optical alignment** (text negative margin -0.05em quand alignement à 0) | Impeccable spatial | Critique TIER 3 (polish) |
| 7 | **font-display: swap + fallback metrics matching** (size-adjust, ascent-override) | Vercel + Impeccable | Gate Python (binaire) |
| 8 | **color-scheme: dark on `<html>`** pour dark themes | Vercel | Gate Python (binaire) |
| 9 | **safe-area-inset** sur full-bleed sections | Vercel + Impeccable | Gate Python (binaire) |
| 10 | **Mobile-first CSS** (base mobile, min-width queries pour desktop) | Vercel + Impeccable | TIER 1 (`a11y-fondamentaux-tier1.md` — architecture responsive) |
| 11 | **Specific button labels** (verbe+object : "Save API Key" pas "Continue") | Vercel + Impeccable ux-writing | Critique TIER 2 |
| 12 | **Active voice + 3-part error formula** (what + why + how-to-fix) | Vercel + Impeccable + GStack | Critique TIER 3 (copy polish) |

### MOYENNE PRIORITÉ (8 règles — finition technique)

| # | Règle positive | Destination |
|---|---|---|
| 13 | `<link rel="preconnect">` pour Google Fonts | Gate Python |
| 14 | `<link rel="preload" as="font">` pour fonts critiques | Gate Python |
| 15 | `loading="lazy"` sur below-fold images | Gate Python |
| 16 | `fetchpriority="high"` sur image hero critique | Gate Python |
| 17 | `font-variant-numeric: tabular-nums` sur colonnes chiffrées | Gate Python |
| 18 | `touch-action: manipulation` sur interactifs | **Déjà TIER 1** depuis Vague 1bis (a11y-fondamentaux-tier1.md) — vérifier respect |
| 19 | Touch targets 44px minimum | **Déjà TIER 1** — vérifier respect |
| 20 | Skip link `<a class="skip-to-content">` en début de body | Gate Python |

### BASSE PRIORITÉ — SKIPPER pour BIG style-tile

Ces règles s'appliquent à des apps complètes, pas à BIG (vitrine + mini-app artefact) :
- Roving tabindex (pas de menus complexes)
- Modales inert + native dialog (pas de modales)
- Dropdowns position:fixed / Popover API (rare)
- Undo toast > confirmation (pas d'actions destructives)
- Gesture affordance (vitrine, pas app)
- Container queries vs viewport queries (sauf cas artefact)
- Intl.DateTimeFormat / NumberFormat (BIG mostly statique)
- Tables to cards on mobile (rare en style-tile)
- Progressive disclosure details/summary (rare)

## Étapes d'exécution

### Étape 1 — Validation Charles sur la liste de promotions

Soumettre à Charles :
- Liste HAUTE PRIORITÉ (12 règles) avec destination proposée
- Tranche : règle #1, #2, #10 → TIER 1 ? Ou Critique TIER 2 ?
- Tranche : règle #11, #12 (copy) → vraiment pertinent pour BIG style-tile (peu de copy) ?

### Étape 2 — Implémentation HAUTE PRIORITÉ

| Sous-étape | Action | Fichier |
|---|---|---|
| 2a | Ajouter règle #1 "Multi-dimension hierarchy" en TIER 1 sobre | `hierarchie-visuelle-tier1.md` |
| 2b | Ajouter règle #2 "Squint test" en TIER 1 principe transversal | `hierarchie-visuelle-tier1.md` |
| 2c | Ajouter règle #10 "Mobile-first" en TIER 1 ou note d'architecture | `a11y-fondamentaux-tier1.md` (section dédiée) |
| 2d | Ajouter règles #3 (z-index scale) à `phase-3b-palette.md` (tokens) | `phase-3b-palette.md` |
| 2e | Ajouter règles #4, #5, #6 à Critique core (TIER 2/3) | `finition-elite-core.md` ou `hierarchie-visuelle-core.md` |
| 2f | Ajouter règles #7, #8, #9 aux gates Python | `phase4-finishing-gate.py` |
| 2g | Ajouter règles #11, #12 à Critique core (copy guidelines) | `anti-slop-blacklist-core.md` ou nouveau ref `copy-elite-core.md` |

### Étape 3 — Implémentation MOYENNE PRIORITÉ

Enrichir `phase4-blacklist-gate.py` (ou nouveau script `phase4-perf-gate.py`) avec les checks 13-17, 20.

Règles 18-19 sont déjà en TIER 1 (Vague 1bis) — juste vérifier qu'elles sont respectées dans les tests.

### Étape 4 — Test sur Pouls Profond

Relancer le pipeline sur le brief baseline. Cible :
- Score audit-slop ≥ 8.5/10 (déjà visé en Point 1 — Point 2 marginal)
- Qualité visuelle perceptible : shadows tintés, line-height ajusté light-on-dark, fonts preloaded (LCP amélioré), z-index propre
- Pas de régression

### Étape 5 — Documentation

`CHANGELOG.md`, `DECISIONS.md` (D5Z règles positives intégrées), `ARCHITECTURE.md`.

## Effort estimé

**~1-2 sessions** (Point 2 plus court que Point 1 : moins de règles, plus ciblées, validation Charles plus rapide).

## Ordre d'exécution recommandé

**Faire Point 1 d'abord** (volume + impact anti-slop majeur), puis Point 2 (polish positif).

Si Point 1 atteint déjà ≥ 8.5/10 → Point 2 devient OPTIONNEL (rendement décroissant). Charles décide après mesure Point 1.

## Dernière mise à jour

2026-04-26 — Plan rédigé pour exécution dans nouvelle session après passation. Validation Charles requise sur classification TIER 1 vs Critique pour les règles #1, #2, #10, #11, #12.
