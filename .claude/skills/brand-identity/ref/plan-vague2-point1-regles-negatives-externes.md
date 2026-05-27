# Plan Vague 2 — Point 1 : Intégration des règles anti-slop NÉGATIVES des skills externes

## Contexte

Vague 1 (24-26 avril 2026) a fait le pivot architectural Designer + Critique + Correcteur avec hiérarchisation TIER 1/2/3, sur les règles **déjà historiquement présentes** dans BIG (factorisation des anti-patterns datés + socle finition + hiérarchie).

Le skill `/audit-slop` consolide ~158 règles universelles extraites de 4 sources externes (Vercel, Impeccable, GStack, Taste Skill) — dont **la grande majorité n'est pas dans BIG**. Vague 1 n'en a importé que ~8 (le bloc a11y `a11y-fondamentaux-tier1.md`). Reste ~150 règles à intégrer.

**Cible** : score audit-slop ≥ 8.5/10 (vs 7.0/10 actuel) sans toucher au design (sprint mécanique uniquement).

## Sources des règles à intégrer

Toutes dans `/Users/charlesbezard/Library/CloudStorage/GoogleDrive-charles.bezard@gmail.com/Mon Drive/Claude Code/Brand Identity Generator/.claude/skills/audit-slop/sources/` :

- `impeccable/SKILL.md` + `impeccable/reference/{color-and-contrast,typography,spatial-design,motion-design,interaction-design,responsive-design,ux-writing,craft,extract}.md` (~98 règles)
- `taste-skill/{taste-skill,redesign-skill,soft-skill,minimalist-skill,brutalist-skill,images-taste-skill,stitch-skill}.md` (~62 règles, dédup à faire)
- `gstack/{plan-design-review,design-review}.md` (~18 règles)
- `vercel-command.md` (~34 règles)

Total brut ~212 règles, ~158 universelles après dédup cross-source.

## Étapes d'exécution

### Étape 1 — Re-extraction exhaustive (agent Explore)

Lancer 1 agent Explore "very thorough" avec ce prompt EXACT (reproduit de la session du 24 avril qui avait produit l'extraction de 212 règles uniques) :

```
MISSION CRITIQUE : extraction EXHAUSTIVE de TOUTES les règles du skill audit-slop, 
avec classification universel/contextuel et mapping vers emplacement BIG.

Pour CHAQUE règle des 20 fichiers sources externes, produire :
- ID (R-001, R-002, ...)
- Règle (formulation ≤ 1 ligne)
- Source principale (fichier + section)
- Aussi présente dans (autres sources)
- Type : UNIVERSEL / CONTEXTUEL
- Domaine : a11y / typo / color / spacing / motion / interaction / copy / responsive / 
  performance / composition / craft / content
- Grepable : OUI / NON / PARTIEL
- Sévérité : CRITIQUE / MOYENNE / POLISH
- Destination BIG proposée (POUR LES UNIVERSELLES) : 
  TIER 1 (anti-slop-blacklist-tier1, finition-elite-tier1, hierarchie-visuelle-tier1, a11y-fondamentaux-tier1)
  / GATE PYTHON (phase4-blacklist-gate.py, phase4-finishing-gate.py)
  / CRITIQUE TIER 2/3 (anti-slop-blacklist-core, finition-elite-core, hierarchie-visuelle-core)
  / N/A HTML vanilla (Framer Motion, React, nuqs, hydration)
- Déjà dans BIG ? OUI (où) / PARTIELLEMENT / NON

Lire intégralement les 20 fichiers sources externes + les fichiers BIG actuels 
(refs *-core.md, *-tier1.md, scripts/*.py, phases/phase-4-*.md).

Livrable : tableau exhaustif markdown.
```

Durée : 30-45 min. Output : ~1500 lignes markdown avec tableau complet.

### Étape 2 — Validation Charles sur classification

Présenter à Charles :
- Statistiques : N règles universelles à injecter / N N/A HTML vanilla / N déjà dans BIG
- Liste des règles à promouvoir TIER 1 (CRITIQUE non-négociables, ex: a11y supplémentaires) — soumettre pour validation
- Liste des règles GATE PYTHON (grep-ables) — confirmer les regex
- Liste des règles CRITIQUE TIER 2/3 (sémantiques) — confirmer scope

Charles tranche les ambiguïtés (ex: telle règle est-elle universelle ou contextuelle ? promouvoir TIER 1 ou laisser TIER 2 ?).

### Étape 3 — Implémentation par destination

#### 3a. Extension des gates Python (~30-40 règles binaires)

Modifier `scripts/phase4-blacklist-gate.py` et/ou `scripts/phase4-finishing-gate.py` pour ajouter les checks regex des règles externes grep-ables :

- Bloc a11y : focus-visible présent sur interactifs, `outline:none` sans `:focus-visible`, `transition:all`, `prefers-reduced-motion`, `100vh`, `user-scalable=no`, `touch-action`
- Bloc typo : apostrophes droites FR, straight quotes, ellipsis `...`, fonts bannies (Inter, Roboto, Open Sans, Fraunces, Newsreader, Lora, Crimson, Playfair, Cormorant, Instrument Serif), `font-variant-numeric: tabular-nums`
- Bloc copy : Lorem Ipsum, fake names (Jane/John Doe, Acme, Nexus, SmartFlow), filler words (Elevate, Seamless, Unleash, Next-Gen, Delve, Game-changer, Revolutionize)
- Bloc technique Vercel : `<meta name="theme-color">`, `<link rel="preconnect">`, `<link rel="preload" as="font">`, `color-scheme`, `<img>` width+height, `loading="lazy"`, `viewport-fit=cover`, `env(safe-area-inset-*)`

Chaque nouveau check démarre en **WARN** pendant 5 runs de validation, puis passe en **FAIL** si aucun faux positif.

#### 3b. Extension du core blacklist (~50-60 règles sémantiques)

Enrichir `ref/anti-slop-blacklist-core.md` (utilisé par le Critique uniquement) avec les règles sémantiques universelles de :

- `impeccable/spatial-design.md` : squint test (général), multi-dimension hierarchy, optical alignment, z-index semantic scale
- `impeccable/typography.md` : line-height inverse à line length, max 65-75ch body, light-on-dark line-height +0.05-0.1, font pairing multi-axe
- `impeccable/motion-design.md` : durations standard, ease-out entries / ease-in exits, height via grid-template-rows
- `impeccable/interaction-design.md` : focus ring 2-3px / outline-offset 2px, modales inert + dialog, dropdowns position fixed, undo toast > confirmation, gesture affordance
- `gstack/plan-design-review.md` : 7-pass review framework, Trunk Test, Goodwill Reservoir
- `taste-skill/*.md` : 26 ANTI-AI-SLOP RULES, AI Tells

Format : ligne courte actionnable (Niveau 1-2 selon `anti-slop-formulation-guide.md`). Pas de listes nominatives (fonts, hex précis) — celles-ci en gate Python.

#### 3c. Promouvoir certaines règles en TIER 1 (~3-5 max)

Après revue Charles : promouvoir au TIER 1 (= Designer en mode CRÉATION) les règles VRAIMENT structurantes que le Designer doit avoir dès le départ. Candidats probables :
- Multi-dimension hierarchy (anti-sur-emphasis, complète "Restraint")
- Squint test général (principe transversal)
- Z-index semantic scale (architecture token)
- Mobile-first CSS (architecture responsive)

Ajouter au fichier TIER 1 approprié (`finition-elite-tier1.md` ou `hierarchie-visuelle-tier1.md`).

#### 3d. REFACTORING ARCHITECTURE Critique : 4 subagents en parallèle + Synthétiseur (PIVOT VAGUE 2)

**Pivot validé 26 avril** : avec ~60-80 nouvelles règles sémantiques en Vague 2, le Critique unique se retrouve à devoir traiter ~600 lignes de règles + le HTML complet → risque de surcharge cognitive (faux négatifs).

Solution : refactorer en **4 subagents Critiques spécialisés en parallèle** (pattern audit-slop éprouvé) + **1 Synthétiseur**.

**4 Critiques spécialisés à créer** :
| Subagent | Domaine | Sources lues | Taille cible |
|---|---|---|---|
| `phases/phase-4check-a11y.md` | A11y défensif TIER 1 + a11y/perf TIER 2/3 + Vercel technique | `a11y-fondamentaux-tier1.md` + sections a11y/perf de `anti-slop-blacklist-core.md` | ~80 lignes |
| `phases/phase-4check-composition.md` | Anti-patterns compositionnels macro + hiérarchie sémantique | `anti-slop-blacklist-core.md` §1 compositions + `hierarchie-visuelle-core.md` | ~80 lignes |
| `phases/phase-4check-typo-copy.md` | Fonts, line-height, copy guidelines, typo française (sémantique) | `anti-slop-blacklist-core.md` §3+§5 + `finition-elite-core.md` typo | ~70 lignes |
| `phases/phase-4check-craft.md` | Ombres, easing, motion, couche graphique, finition CSS | `finition-elite-core.md` + `anti-slop-blacklist-core.md` §1 effets/animations + §2 couche graphique | ~80 lignes |

**Synthétiseur** :
| Fichier | Rôle |
|---|---|
| `phases/phase-4check-synthetiseur.md` | Reçoit 4 JSON correction lists + pitch concept. Dédoublonne, priorise (CRITIQUE > MEDIUM > POLISH), arbitre contradictions. Output : 1 JSON consolidé pour Designer mode CORRECTION (compat ascendante avec boucle 4A-loop). ~50 lignes |

**Modification SKILL.md Étape 4A-loop** : remplacer l'invocation unique `phase-4check.md` par invocation parallèle des 4 subagents (Task tool avec `run_in_background: true`) + appel séquentiel Synthétiseur après réception des 4 JSON.

**Garde-fous** :
- Si 1 Critique plante → continuer avec les 3 autres (synthèse dégradée mais non-bloquante)
- Si 2+ Critiques plantent → fallback au Critique unique (re-utilise `phase-4check.md` actuel comme back-up)
- Watchdog 600s par Critique
- Format JSON strict validé par l'orchestrateur

**`phase-4check.md` actuel** : conservé en fallback (architecture dégradée si 2+ Critiques spécialisés plantent).

#### 3e. Étendre les sources lues par les Critiques selon enrichissement core

Pas de changement structurel pour les 4 nouveaux Critiques — ils lisent les `*-core.md` complets selon leur domaine. L'enrichissement Vague 2 (3c.2) ajoute automatiquement des règles dans leur scope.

### Étape 4 — Test sur Pouls Profond + 1 brief alternatif

Relancer `/test-big` depuis Phase 4 sur :
- `test-voltapilot-test-20260425-1634` (concept 2 = Pouls Profond, baseline 7.0/10)
- 1 autre brief récent (Camille ou autre) pour valider la généralisation

Cible :
- Score audit-slop ≥ 8.5/10
- Aucune régression sur le sur-engineering visuel
- Boucle Critique converge en 1-2 itérations
- Tous les marqueurs JSON présents (incluant `.pipeline-audit-c{N}.json` désormais obligatoire)

### Étape 5 — Documentation

Mettre à jour :
- `CHANGELOG.md` : entrée date Vague 2 Point 1
- `DECISIONS.md` : D5X promotion N règles externes en TIER 1 / D5Y enrichissement core blacklist
- `ARCHITECTURE.md` : section "Couverture règles externes audit-slop"
- `MEMORY.md` : marquer chantier Vague 2 Point 1 complété

## Fichiers à modifier (récap)

### Probablement modifiés
- `scripts/phase4-blacklist-gate.py` (+~30 checks)
- `scripts/phase4-finishing-gate.py` (+~10 checks)
- `ref/anti-slop-blacklist-core.md` (+~50 règles)
- `ref/finition-elite-core.md` (+~10 règles)
- `ref/hierarchie-visuelle-core.md` (+~5 règles)
- `ref/anti-slop-blacklist-tier1.md` (+~3-5 règles si promotions)
- `ref/finition-elite-tier1.md` (+~2-3 règles si promotions)
- `phases/phase-4check.md` (mise à jour pointeurs sources si besoin)

### Possiblement créé
- `scripts/phase4-tier1-a11y-gate.py` (gate Python dédié si on veut un check mécanique des TIER 1 a11y)

### Inchangés
- `ref/a11y-fondamentaux-tier1.md` (déjà fait en Vague 1bis)
- `phases/phase-4-styletile.md` + `phase-4-artefact.md` + `phase-6a-batch2.md` + `phase-6b-batch3.md` (les imports `{*_tier1}` sont déjà en place)
- `SKILL.md` (les pré-conditions et boucle sont déjà en place)

## Risques et mitigations

| Risque | Mitigation |
|---|---|
| Sur-engineering visuel revient si trop de règles promues TIER 1 | Promotion limitée à 3-5 règles max, validation Charles avant chaque promotion |
| Faux positifs gates Python qui bloquent le pipeline | WARN → FAIL progressif (5 runs sans faux positif avant FAIL) |
| Couvrir tout le périmètre audit-slop = pipeline lent | Acceptable — gates Python ajoutent 10-30s, OK selon Charles |
| Critique trop chargé avec ~50 nouvelles règles → loupe des trucs | Le Critique a déjà accès aux core complets ; prompt à ajuster légèrement, pas restructurer |

## Cible et succès

- Score audit-slop sur Pouls Profond ≥ 8.5/10
- Sur-engineering visuel artefact toujours absent
- Boucle Critique converge en ≤ 2 itérations
- 0 plantage background subagents
- Audit trail `.pipeline-audit-c{N}.json` produit (grâce au Patch A déjà appliqué)

Effort estimé : **~4-5 sessions** (Étape 1 + 2 = 1 session ; Étape 3 = 2-2.5 sessions incluant refactoring Critique en 4 subagents + Synthétiseur ; Étape 4-5 = 0.5 session).

## Dernière mise à jour

2026-04-26 — Plan rédigé pour exécution dans nouvelle session après passation.
