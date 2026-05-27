# Passation — Architecture anti-slop BIG pour application aux étapes 3B

> **Lecture obligatoire avant tout travail sur les étapes 3B.** Ce document contient TOUT le contexte nécessaire pour comprendre comment fonctionne le système anti-slop appliqué aujourd'hui en Phase 4, ce qui marche, ce qui ne marche pas, et les pièges. À toi ensuite d'analyser les phases 3B (`phase-3b-*.md`) pour identifier où et comment appliquer ces règles.

---

## 0. TL;DR pour démarrer rapidement

- Le pipeline BIG produit des style-tiles HTML. L'audit-slop externe les note sur 10 selon 4 dimensions (Craft Moderne / Vercel Technique / BIG Pipeline / Perplexity Temporel).
- Une **Vague 2 anti-slop** a intégré ~120 règles dans BIG en amont (Phase 4) pour réduire les marqueurs AI-slop. Une **Vague 2.5 corrective** (en cours, 2026-04-27) a ajouté 4+3 patches structurels pour fixer des bugs de pipeline.
- Score audit-slop sur le brief de référence "VoltaPilot c2 Pouls Profond" : baseline 7.0/10 → 6.0/10 après refactor (régression à cause des bugs corrigés depuis), cible visée 8.0/10.
- L'architecture anti-slop est volontairement **stratifiée** : Designer création voit peu de règles (TIER 1 ~28), Critiques en aval voient le reste (~80+). Ne pas inverser cette logique sans très bonne raison.
- Les phases 3B (palette, typographie, design dérivé, pitch, spécimens, etc.) ont leur propre logique mais peuvent bénéficier de patterns analogues. **Ce travail reste à faire.**

---

## 1. Contexte général — qu'est-ce que l'anti-slop dans BIG

### 1.1 Le problème que BIG essaie de résoudre

Les LLM produisent par défaut des outputs qui contiennent des **marqueurs d'AI-slop datés** : patterns visuels qui révèlent que c'est généré par IA et qui paraissent vieux (techniques de 2017-2023 bouclées). Exemples :
- `transform: translateY(-2px)` au hover (cliché 2017)
- `letter-spacing` qui change au hover (cliché footer 2017)
- Glow shadows sans offset directionnel
- Glassmorphism décoratif par défaut
- Centrage symétrique de tout
- Grid de 3 cards identiques (pattern AI-tell #2)
- Apostrophes droites en français (`'` au lieu de `'`)
- "Lorem Ipsum", "John Doe", "Acme Corp"
- Filler words ("Elevate", "Seamless", "Unleash", "Next-Gen", "Delve")
- Fonts surutilisées (Inter, Roboto, Open Sans, Lato, Montserrat)
- Gradient text via `background-clip: text` (trend 2019-2020)

Sans intervention, un Designer LLM produit ces patterns naturellement parce qu'ils dominent dans son training data.

### 1.2 La stratégie anti-slop

3 leviers complémentaires :

1. **TIER 1 — Règles structurantes injectées dans le prompt du Designer en mode CRÉATION**. Limité à ~25-30 règles (au-delà : sur-engineering observé, le Designer "performe" toutes les règles au lieu de les appliquer avec discernement).

2. **Gates Python déterministes** (`scripts/phase4-blacklist-gate.py` + `scripts/phase4-finishing-gate.py`) : checks regex mécaniques sur le HTML produit. Rapides, pas de variabilité LLM, mais ne couvrent que les patterns grep-ables (~50-60 règles).

3. **Critiques sémantiques en aval** : 4 subagents spécialisés (a11y, composition, typo-copy, craft) qui auditent le HTML produit selon ~80 règles non-grep-ables. Plus 1 Synthétiseur qui consolide leurs JSON.

Le pipeline détecte les violations et déclenche des **boucles de correction** (Designer mode CORRECTION CHIRURGICALE) avec garde-fous anti-régression.

### 1.3 Les sources des règles

L'audit-slop externe s'appuie sur 4 sources externes :
- **Vercel** (production-ready, perf, a11y)
- **Impeccable** (8 fichiers : color, typography, spatial, motion, interaction, responsive, ux-writing, craft)
- **GStack** (design review, plan-design-review)
- **Taste Skill** (7 variantes : taste, redesign, soft, minimalist, brutalist, images, stitch)

Total ~212 règles brutes, ~158 universelles (HTML vanilla), ~54 contextuelles (datation, registre).

Sur les 158 universelles, BIG en a importé ~150 (Vague 2 + Vague 1 + 1bis avant).

---

## 2. Architecture en place

### 2.1 Les 4 fichiers TIER 1 (lus par le Designer création)

Localisation : `ref/`

| Fichier | Rôle | Volume actuel |
|---|---|---|
| `anti-slop-blacklist-tier1.md` | 6 compositions macro à éviter (50/50 hero, grid 3 cards, etc.) | 6 règles |
| `finition-elite-tier1.md` | Palette + CSS moderne + neutres tintés + type scale + spacing scale | 11 règles |
| `hierarchie-visuelle-tier1.md` | Restraint + 1 dominant + données/labels + variation densité + séparation par fond | 5 règles |
| `a11y-fondamentaux-tier1.md` | 6 règles a11y non-négociables (focus-visible, prefers-reduced-motion, touch targets 44px, etc.) | 6 règles |
| **TOTAL TIER 1** | | **28 règles** |

**Convention de formulation TIER 1** (CRITIQUE — cf. `ref/anti-slop-formulation-guide.md`) :
- Niveau 1 : principe abstrait (`Do NOT center everything symmetrically`)
- Niveau 2 : pattern nommé non-substituable (`Do NOT use neumorphism`)
- Niveau 3 : énumération précise (fonts/hex/syntax) → **JAMAIS dans le prompt**, uniquement en gate Python

**Pourquoi c'est critique** : le LLM utilise les valeurs concrètes comme inspiration créative. Un prompt qui dit "Do NOT use Inter" pousse le LLM à utiliser une font similaire à Inter. Donc les listes nominatives vivent dans le code Python uniquement.

**Limite empirique** : ~25 règles TIER 1 max. Au-delà, sur-engineering observé (cas Pouls Profond 24 avril : chiffre 287,4 à 12rem, 3 plans visuels en compétition, copy métaphorique délirant). On est actuellement à 28 (légèrement au-dessus, sans dégât observé).

### 2.2 Les 6 fichiers core (lus uniquement par les Critiques en aval)

Localisation : `ref/`

| Fichier | Rôle | Lu par |
|---|---|---|
| `anti-slop-blacklist-core.md` | Anti-patterns sémantiques (composition, hovers datés, animations infinies, glow shadows...) | Critique Composition + Critique Craft |
| `finition-elite-core.md` | Craft CSS détaillé (shadows tintées, easing physiques, motion principles, dark mode, optical alignment...) | Critique Craft |
| `hierarchie-visuelle-core.md` | Hiérarchie multi-dimensions, restraint, density variation, design variance | Critique Composition |
| `typography-core.md` | Pairing fonts, weights, letter-spacing, line-height, OpenType features | Critique Typo-Copy |
| `ux-writing-core.md` | Boutons spécifiques, errors what/why/how, empty states, voice/tone, Title Case | Critique Typo-Copy |
| `interaction-core.md` | 8 états interactifs, forms, modales, touch, scroll-margin | Critique A11y |

Ces fichiers contiennent **~80 règles** au total, invisibles du Designer création par design.

### 2.3 Les 2 scripts Python (gates déterministes)

Localisation : `scripts/`

| Script | Rôle | Patches récents |
|---|---|---|
| `phase4-blacklist-gate.py` | 17 patterns datés grep-ables (hover-translateY, glow-shadow, zigzag-clip-path, etc.) — verdict FAIL | Inchangé depuis Vague 1 |
| `phase4-finishing-gate.py` | Vague 1 (8 checks structurants) + Vague 2 (33 checks WARN-only informationnels) | **P4** : ajout `--json-output` qui produit un JSON structuré complet (vague1 + vague2) — élimine le shortcut "résumé stdout tronqué" |
| `parse-blacklist-violations.py` | **NEW P9a** — parse le stdout du blacklist gate et produit un JSON corrections list compatible avec le pattern P6 | Créé le 27 avril |

**Pourquoi P4 et P9a sont importants** : avant, l'orchestrateur lisait le stdout des gates et écrivait un JSON corrections en mode "interprétation LLM". Il oubliait régulièrement les violations vague2 ou les violations blacklist. **Solution : remplacer l'instruction LLM par un script Python déterministe**. Plus de shortcut possible.

### 2.4 Les 5 subagents Critique (Vague 2)

Localisation : `phases/`

| Subagent | Domaine | Refs lues |
|---|---|---|
| `phase-4check-a11y.md` | A11y défensif TIER 1 + a11y/perf TIER 2/3 + Vercel technique | a11y-fondamentaux-tier1.md, anti-slop-blacklist-core (a11y), interaction-core.md |
| `phase-4check-composition.md` | Anti-patterns compositionnels macro + hiérarchie sémantique | anti-slop-blacklist-core (compositions), hierarchie-visuelle-core.md, anti-slop-blacklist-tier1.md |
| `phase-4check-typo-copy.md` | Typographie + UX-writing/copy sémantique | typography-core.md, ux-writing-core.md, finition-elite-tier1.md (typo) |
| `phase-4check-craft.md` | Craft CSS (shadows/easing/surfaces) + motion + finition CSS | finition-elite-core.md, finition-elite-tier1.md, anti-slop-blacklist-core (effets/animations) |
| `phase-4check-synthetiseur.md` | Consolide les 4 JSON correction lists, dédoublonne, priorise, signe | (lit uniquement les 4 JSON Critiques) |

**Pattern P3 (synthesizer signature)** : le Synthétiseur produit un JSON consolidé avec un champ `synthesizer_subagent_signature` qui prouve qu'il a vraiment été invoqué (vs orchestrateur qui aurait fabriqué le JSON manuellement).

**Pattern P8 (4 Critiques en VRAI parallèle)** : l'orchestrateur DOIT envoyer les 4 invocations Task tool DANS LE MÊME MESSAGE avec `run_in_background=true`. Sinon les 4 tournent séquentiellement (~24 min cumulés au lieu de ~6 min en vrai parallèle). La sous-étape 4.10 du SKILL.md a une POST-CONDITION qui mesure le wall-clock pour détecter le shortcut.

### 2.5 Le Critique unique de Vague 1 (fallback)

`phase-4check.md` — Critique monolithique enrichi (~600 lignes de règles). Conservé en **fallback** : utilisé uniquement si ≥ 2 des 4 Critiques spécialisés plantent. Architecture dégradée mais non-bloquante.

### 2.6 Le Designer Phase 4 (subagent générateur)

Localisation : `phases/phase-4-styletile.md` (création style-tile) et `phases/phase-4-artefact.md` (création artefact UI mini-app).

**Modes du Designer** :
- **Mode CRÉATION** (priorité par défaut) : génère le HTML from scratch avec TIER 1 injectées
- **Mode CORRECTION CHIRURGICALE** : reçoit un HTML existant + JSON corrections list → patche UNIQUEMENT les zones listées, JAMAIS hors liste

**Pattern P6 (généralisé)** : tout contrôleur (gates Python + gate visuel + Critiques) produit un JSON corrections. L'orchestrateur lit ce JSON et invoque un **nouveau Designer mode CORRECTION** avec ce JSON. **Le contrôleur ne patche JAMAIS le HTML lui-même** (il n'a pas le cerveau CSS du Designer, ses patches seraient incohérents).

**Pourquoi P6 est important** : `SendMessage` (qui aurait permis de "resumer" un Designer existant avec des corrections) **n'est pas accessible aux subagents Claude Code**. Donc on ne peut pas demander au contrôleur de "faire patcher" le Designer. Solution : produire un JSON, l'orchestrateur invoque un nouveau Designer fresh.

### 2.7 Le SKILL.md zone Étape 4 — state machine atomique 15 sous-étapes

Localisation : `SKILL.md` (lignes ~2710-3700, dépendant des patches successifs).

**Architecture validée le 26 avril** : 15 sous-étapes atomiques numérotées (4.1 à 4.15), chacune avec :
- ⛔ **Pré-condition bash bloquante** (`exit 1` si artefact attendu absent)
- ▸ **Action unique** (1 invocation Task tool OU 1 commande bash OU 1 décision)
- ⛔ **Post-condition bash bloquante** (`exit 1` si artefact attendu absent)
- ➡️ **Transition explicite** vers la sous-étape suivante

**Convention de nommage des artefacts** : `.{type}-c{N}-{stage}.json`
- types : `gates-finishing`, `gates-blacklist`, `finishing-gate`, `critique`, `pipeline-audit`
- N : numéro de concept (1, 2, 3)
- stage : `v0`, `v1`, `art`, `iter0`, `iter1`

**15 sous-étapes** :
| ID | Nom | Conditionnelle ? |
|---|---|---|
| 4.1 | Création HTML v0 (Designer mode CRÉATION) | NON |
| 4.1bis | **Pause utilisateur** (P7) — validation HTML v0 | NON |
| 4.2 | Gates Python v0 (blacklist + finishing avec --json-output) | NON |
| 4.3 | Gate visuel v0 (subagent contrôleur Puppeteer) | NON |
| 4.4 | Production JSON corrections v0 (P6 + P9b script déterministe) | NON |
| 4.5 | Designer correction v0→v1 (anti-régression P3) | OUI (skip si corrections vide) |
| 4.6 | Re-validation v1 + rollback si gates empirent | OUI |
| 4.7 | Designer artefact (P10 :root pré-extrait + P11 anti-timeout) | NON |
| 4.7bis | **Pause utilisateur** (P7) — validation artefact | NON |
| 4.8 | Re-validation post-artefact + production JSON corrections art (P9b) | NON |
| 4.9 | Correction post-artefact (P3 anti-régression) | OUI |
| 4.10 | Critique 4-parallèle iter0 (P8 vrai parallèle) | NON |
| 4.11 | Synthétiseur iter0 (P3 signature) | NON |
| 4.12 | Designer correction iter0 (P3 anti-régression) | OUI |
| 4.12bis | **Pause utilisateur** (P7) — validation finale | OUI (si 4.12 a tourné) |
| 4.13 | Boucle iter1 (re-Critique + Synth + Designer correction) | OUI (skip si 4.12 sauté) |
| 4.14 | Audit consolidé `.pipeline-audit-c{N}.json` (Patch A + P1) | NON |
| 4.15 | Swap haute résolution + ouverture browser | NON |

**Détection dynamique des concepts** (en début de zone Étape 4) : l'orchestrateur calcule `CONCEPTS = liste des concepts qui ont un pitch en Phase 3`, le persiste dans `.phase4-concepts.txt`, et **toutes les sous-étapes itèrent sur cette liste** (pas de hardcode `for n in 1 2 3`). Permet les runs partiels (ex: c2 seul).

---

## 3. Les patches successifs (chronologie + ce qu'ils corrigent)

### 3.1 Patches Vague 1 + 1bis (24-26 avril)

| Patch | Quoi | Pourquoi |
|---|---|---|
| **Patch A** | Pré-condition stricte sur 4A-bis qui force la production de `.pipeline-audit-c{N}.json` (4.14) | L'orchestrateur sautait régulièrement 4.14 |
| **Patch B** | Audit défensif TIER 1 dans `phase-4check.md` | TIER 1 oublié par le Designer (`touch-action: manipulation`), Critique ne re-vérifiait pas |

### 3.2 Patches Vague 2 (extension règles externes — 26 avril)

| Patch | Quoi |
|---|---|
| Refactor 1 Critique → 4 Critiques + Synthétiseur | Cf. section 2.4 |
| Création des refs core typography-core.md, ux-writing-core.md, interaction-core.md | +75 règles sémantiques |
| Promotions TIER 1 : R-003 (neutres tintés), R-010 (type scale modulaire), R-023 (spacing scale 4pt) | TIER 1 passé de 16 → 19 (compté grossier ; en compté atomique, 28 actuels) |
| **P1** | `verdict_critiques` dans `.pipeline-audit-c{N}.json` (OK / DEGRADE / SHORTCUT_DETECTE / FALLBACK_VAGUE1) |
| **P2** | Pré-condition stricte avant Synthétiseur (≥ 3/4 Critiques valides, sinon fallback Vague 1) |
| **P3** | `synthesizer_subagent_signature` obligatoire dans le JSON consolidé (preuve d'invocation) |
| **P4** | `phase4-finishing-gate.py --json-output` produit un JSON structuré complet (vague1 + vague2) — élimine le shortcut résumé stdout |
| **P5** | SKILL.md Étape 4.2 force la lecture du JSON complet (pas le résumé) — protocole strict |
| **P6** | Pattern "contrôleur → JSON corrections → Designer mode CORRECTION" appliqué en 4A-ter (pre-refactor) puis généralisé à toutes les sous-étapes de correction |

### 3.3 Refactor architectural R3 (26-27 avril)

Transformation de la zone Étape 4 du SKILL.md d'un pseudocode narratif (~1048 lignes) en state machine atomique (~858 lignes). Élimine la classe de bugs "shortcut orchestrateur" qui avait généré 8 patches réactifs précédemment. Documenté dans `ref/etape4-refactor-draft.md`.

### 3.4 Détection dynamique des concepts (27 avril matin)

Patch ajouté pour gérer les runs partiels (ex: c2 seul). Le hardcode `for n in 1 2 3` partout dans la state machine cassait sur les runs avec 1 seul concept.

### 3.5 Patches Vague 2.5 corrective (27 avril, suite à test E2E)

Test révèle 4 bugs structurels dans le refactor :

| Patch | Quoi | Pourquoi |
|---|---|---|
| **P3 (étendu à 4.5)** | Anti-régression rollback Designer correction. Re-run gates post-correction, rollback vers backup si violations augmentent | "Jeu de la taupe" : Designer correction introduit des violations en corrigeant |
| **P3-bis** | Fix bug latent `total_fails` → `fail_count` dans 4.6/4.9/4.13 | Le rollback ne se déclenchait JAMAIS car la clé JSON était fausse |
| **P4** | Standardisation convention nommage backups (4 conventions chaotiques → 4 noms cohérents auto-explicatifs) | Bug `.bakiter0` qui faisait skipper iter1 |
| **P7** | 3 pauses utilisateur (4.1bis, 4.7bis, 4.12bis) | Run de 2h non-stop sans intervention possible |
| **P8** | Forcer 4 Critiques en VRAI parallèle (directive "même message" + détection wall-clock) | 4 Critiques tournaient séquentiellement (~24 min) au lieu de parallèles (~6 min) |

### 3.6 Patches correctifs (27 avril après-midi, suite test E2E avorté)

Test E2E avec V2.5 révèle 3 nouveaux bugs :

| Patch | Quoi | Pourquoi |
|---|---|---|
| **P9a** | Création `scripts/parse-blacklist-violations.py` qui parse mécaniquement le stdout du blacklist gate | L'orchestrateur ignorait les violations blacklist FAIL et écrivait JSON corrections vide → 4.5 SKIP → violations restaient |
| **P9b** | SKILL.md zones 4.4 et 4.8 invoquent ce script (au lieu de l'instruction LLM "orchestrateur extrait") + assertion `INCOHÉRENCE` si blacklist FAIL et corrections vides | Élimine STRUCTURELLEMENT le shortcut LLM (mécanisme déterministe) |
| **P10** | (a) Orchestrateur pré-extrait le `:root` du HTML v0 dans `.tmp-root-extract-c{N}.css` (3 KB vs 441 KB) et le passe au Designer artefact en variable `{root_extract}`. (b) Checklist atomes phase-4-artefact.md réduite de 25 → 15 essentiels + 5-7 optionnels | Designer artefact timeout 18 min (HTML 441 KB trop lourd à lire + checklist trop ambitieuse) |
| **P11** | Directive stricte "NE PAS utiliser SendMessage en cas de timeout" + protocole "relancer Task fresh, max 2 tentatives" | L'orchestrateur tentait SendMessage (indisponible Claude Code) en cas de timeout |

---

## 4. Ce qui marche bien (à reproduire)

### 4.1 Patterns architecturaux validés

1. **Stratification TIER 1 / Critiques en aval** — éviter de surcharger le Designer création. Les Critiques captent les violations TIER 2/3 sans contaminer la créativité.

2. **Pattern P6 (contrôleur → JSON corrections → Designer mode CORRECTION)** — préserve le cerveau CSS du Designer pour les corrections. Les patches sont cohérents avec le design system du concept.

3. **Mécanismes déterministes > instructions LLM** — chaque fois qu'on a remplacé une instruction textuelle par un script bash/Python, on a éliminé une classe de shortcuts. Ex : P4/P5 (`--json-output` au lieu de "résumer stdout"), P9a/P9b (script parse-blacklist au lieu de "orchestrateur extrait").

4. **State machine atomique avec pré/post-conditions bash** — empêche les "pioches" du LLM dans un guide narratif. Chaque sous-étape a un seul thing à faire, vérifié mécaniquement.

5. **Détection dynamique des concepts** — pas de hardcode `for n in 1 2 3`. Permet les runs partiels et la robustesse.

6. **Parallélisme intra-concept (4 Critiques)** — gain ~18 min vs séquentiel. À condition de bien spécifier "MÊME MESSAGE orchestrateur" + `run_in_background=true`.

7. **Synthétiseur signature SHA-256** — preuve cryptographique d'invocation. Élimine le shortcut "orchestrateur fabrique le JSON consolidé".

### 4.2 Conventions de formulation qui marchent

- **3 niveaux** (cf. `ref/anti-slop-formulation-guide.md`) :
  - N1 : principe abstrait → OK dans prompt
  - N2 : pattern nommé → OK dans prompt
  - N3 : valeurs/listes nominatives → JAMAIS dans prompt, uniquement gate Python

- **Clause anti-cousin** : pour les règles à risque de substitution proche (banni Inter → choisit Roboto), ajouter "X et ses cousins (Y-style era Z)".

- **Reformulation sobre conditionnelle** : "Si telle condition, alors..." plutôt que "DOIT toujours faire X". Évite le sur-engineering.

---

## 5. Ce qui ne marche PAS (pièges à éviter)

### 5.1 Anti-patterns architecturaux

1. **Surcharger TIER 1** — au-delà de ~25-30 règles, le Designer "performe" toutes les règles au lieu de les appliquer avec discernement. Cas Pouls Profond 24 avril : chiffre 287,4 à 12rem, 3 plans visuels en compétition. **Garder TIER 1 minimal**.

2. **Mettre des règles N3 (valeurs/listes) dans le prompt** — le LLM les utilise comme inspiration créative au lieu de les éviter. Ex : `Do NOT use #6366f1` lit comme "cette teinte est cool, je peux jouer autour".

3. **Donner au LLM la responsabilité d'extraire/résumer un output technique** — il pioche ce qui l'arrange. Toujours préférer un script déterministe.

4. **Pseudocode narratif** dans le SKILL.md — le LLM le lit comme un guide à interpréter, pas comme une procédure à suivre. Solution : pré/post-conditions bash exécutables.

5. **Boucles inline** (`while iter < 2`) — source de shortcut prouvée. Préférer des sous-étapes distinctes (4.10 puis 4.13 pour iter1).

6. **Faire patcher le HTML par un contrôleur** — il n'a pas le cerveau CSS du Designer, les patches sont incohérents. Toujours invoquer un nouveau Designer mode CORRECTION.

7. **Tenter `SendMessage` après timeout d'un subagent** — `SendMessage` n'est pas accessible aux subagents Claude Code et ne fonctionne pas après timeout. Toujours relancer un Task fresh.

### 5.2 Bugs récurrents observés

- **Shortcut résumé stdout** : l'orchestrateur lit le stdout d'un script Python et "résume" en perdant les détails (ex: 12 WARN Vague 2 perdus). Solution : `--json-output` qui produit un JSON structuré directement.

- **Shortcut "JSON vide"** : l'orchestrateur écrit `{"corrections":[]}` même quand un gate FAIL. Solution : script déterministe + assertion de cohérence (`if blacklist FAIL and corrections empty → exit 1`).

- **Shortcut audit consolidé** : l'orchestrateur saute la production de `.pipeline-audit-c{N}.json`. Solution : pré-condition stricte sur la sous-étape suivante qui exit 1 si le fichier est absent.

- **Shortcut "fabriquer le marqueur"** : l'orchestrateur écrit un faux marqueur PASS sans avoir invoqué le subagent. Solution : marqueur JSON structuré avec preuves (sha256, signatures, timestamps).

- **Designer correction qui empire** ("jeu de la taupe") : Designer correction introduit des violations en corrigeant. Solution : anti-régression rollback (re-run gates post-correction, rollback si violations augmentent).

### 5.3 Pièges spécifiques à connaître

- **HTML peut atteindre 400-450 KB** — Designer artefact ne peut pas le lire intégralement (timeout). Solution : pré-extraction `:root` (3 KB) côté orchestrateur.

- **Cahier de charges artefact 25 atomes** = mockup d'app surchargé. Réduit à 15 essentiels + 5-7 optionnels (P10).

- **Assertions de cohérence sont essentielles** — vérifier que ce que les sources disent est cohérent avec ce que le pipeline a produit (ex: blacklist FAIL → corrections ≥ 1, sinon ERROR).

---

## 6. État actuel et résultats observés

### 6.1 Score audit-slop sur VoltaPilot c2 (Pouls Profond)

| Date | Score pondéré | BIG Pipeline | Vercel | Craft | Perplexity |
|---|---|---|---|---|---|
| 15 avril (baseline pré-Vague 2) | 4.0/10 | 3 | 2 | 3 | 9 |
| 24 avril (post Étape 1 factorisation) | 6.0/10 | 7 | 3 | 6 | 9 |
| 26 avril 02:54 (post Vague 1+1bis) | **7.0/10** | **8.5** | 3.5 | 6 | 9 |
| 26 avril 23:35 (post Vague 2 + refactor R3) | **6.0/10** ⚠ | **3** ⚠ | 8 | 6 | 8.5 |
| 27 avril (post Vague 2.5 + correctifs) | À MESURER | cible ≥7 | cible ≥8 | cible ≥6 | cible ≥8.5 |

**Régression du 26 avril** : refactor R3 a multiplié les passes Designer correction → "jeu de la taupe" (5 violations blacklist dans le HTML livré). Vague 2.5 (P3 anti-régression + P3-bis fix latent + P4 backups + P7 pauses + P8 parallélisme) corrige cette régression.

**Test du 27 avril matin** révèle 3 bugs supplémentaires (P9, P10, P11) corrigés dans la foulée. Test E2E complet à venir.

### 6.2 Cible visée

- Score audit-slop ≥ 7.5/10 (idéal 8.0+)
- BIG Pipeline ≥ 7/10
- Run Phase 4 ≤ 75 min (vs 120 min hier)
- 0 shortcut orchestrateur détecté sur 3 runs consécutifs

---

## 7. Liste exhaustive des fichiers de référence

### 7.1 Architecture / état du chantier

| Fichier | Rôle |
|---|---|
| `SKILL.md` | Pipeline complet (~5750 lignes). Zone Étape 4 = state machine atomique 15 sous-étapes |
| `ref/etape4-refactor-draft.md` | Draft du refactor R3 — utile pour comprendre la philosophie |
| `ref/passation-vague2-2026-04-26.md` | Passation Vague 2 (rapport pour reprise de session) |
| `ref/test-r4-instructions.md` | Instructions de test E2E pour valider Phase 4 |
| `ref/passation-anti-slop-pour-3b.md` | **CE FICHIER** |

### 7.2 Règles anti-slop — TIER 1 (vu par Designer création)

| Fichier | Volume | Domaine |
|---|---|---|
| `ref/anti-slop-blacklist-tier1.md` | 6 règles | compositions macro à éviter |
| `ref/finition-elite-tier1.md` | 11 règles | palette + CSS moderne + spacing/typo scales |
| `ref/hierarchie-visuelle-tier1.md` | 5 règles | hiérarchie + restraint + densité |
| `ref/a11y-fondamentaux-tier1.md` | 6 règles | a11y non-négociables |

### 7.3 Règles anti-slop — Critique core (vu uniquement Critiques)

| Fichier | Domaine | Lu par |
|---|---|---|
| `ref/anti-slop-blacklist-core.md` | Anti-patterns sémantiques (compositions, hovers, animations, glow...) | Composition + Craft |
| `ref/finition-elite-core.md` | Craft CSS (shadows, easing, motion, dark mode) | Craft |
| `ref/hierarchie-visuelle-core.md` | Hiérarchie multi-dim, density, design variance | Composition |
| `ref/typography-core.md` | Pairing fonts, weights, letter-spacing, line-height | Typo-Copy |
| `ref/ux-writing-core.md` | Boutons, errors, empty states, voice/tone | Typo-Copy |
| `ref/interaction-core.md` | 8 états, forms, modales, touch | A11y |

### 7.4 Refs documentation

| Fichier | Rôle |
|---|---|
| `ref/anti-slop-formulation-guide.md` | **OBLIGATOIRE** — convention 3 niveaux N1/N2/N3 + clause anti-cousin |
| `ref/extraction-vague2-2026-04-26.md` | Extraction exhaustive 182 règles externes audit-slop |
| `ref/plan-integration-anti-slop.md` | Plan historique du chantier Vague 1 |
| `ref/plan-vague2-point1-regles-negatives-externes.md` | Plan Vague 2 point 1 |
| `ref/plan-vague2-point2-regles-positives.md` | Plan Vague 2 point 2 |

### 7.5 Subagents Phase 4

| Fichier | Rôle |
|---|---|
| `phases/phase-4-styletile.md` | Designer Phase 4 mode CRÉATION + mode CORRECTION CHIRURGICALE |
| `phases/phase-4-artefact.md` | Designer artefact (UI mini-app à intégrer dans le style-tile) |
| `phases/phase-4check.md` | Critique unique (fallback Vague 1) |
| `phases/phase-4check-a11y.md` | Critique a11y/perf/robustesse |
| `phases/phase-4check-composition.md` | Critique composition + hiérarchie |
| `phases/phase-4check-typo-copy.md` | Critique typo + UX-writing |
| `phases/phase-4check-craft.md` | Critique craft + motion |
| `phases/phase-4check-synthetiseur.md` | Synthétiseur (consolide les 4 JSON Critiques) |

### 7.6 Scripts Python

| Fichier | Rôle |
|---|---|
| `scripts/phase4-blacklist-gate.py` | 17 patterns datés grep-ables (FAIL bloquant) |
| `scripts/phase4-finishing-gate.py` | 8 checks structurants (vague1 FAIL) + 33 checks WARN (vague2) — supporte `--json-output` |
| `scripts/parse-blacklist-violations.py` | **NEW P9a** — parse stdout du blacklist gate → JSON corrections list |

### 7.7 REX (retours d'expérience)

Tous dans `ref/` :
- `exclusion-metaphores-rex.md` — éviter les métaphores hors-sujet
- `font-selection-rex.md` — sélection de fonts (sans mentionner les noms en prompt)
- `landing-demo-rex.md`
- `logo-generation-rex.md`, `logo-lockup-rex.md`, `logo-vectorization-rex.md` — chantier logo
- `recraft-routing-rex.md` — routage Recraft
- `show-vs-tell-rex.md` — règle "Show > Tell" (CSS doit DÉMONTRER, pas décrire)
- `svg-injection-rex.md` — injection SVG
- `visual-prompting-rex.md` — prompting visuel

---

## 8. Pour ta session — prochaines étapes recommandées

Tu as maintenant TOUT le contexte de l'architecture anti-slop appliquée à la Phase 4. Pour appliquer ces patterns aux étapes 3B (palette, typographie, design dérivé, etc.), je te suggère cette démarche :

### 8.1 Démarche d'analyse

1. **Lire les phases 3B existantes** (`phases/phase-3b-*.md`) pour comprendre :
   - Quelles décisions sont prises (palette, fonts, type-scale, spacing tokens, registre, etc.)
   - Sous quelle forme (variables, listes, choix utilisateur)
   - Quels artefacts sont produits (qui sont ensuite consommés par Phase 4)

2. **Identifier les zones de risque** :
   - Choix de fonts qui pourraient revenir vers les training defaults (Inter, Roboto, etc.)
   - Palette qui pourrait inclure des hex bannis (`#000000`, `#ffffff`, `#6366f1` purple AI)
   - Type-scale ou spacing qui pourrait dériver vers les conventions 14/15/16/18 ad hoc
   - Métaphores créatives qui pourraient introduire des marqueurs slop datés

3. **Mapper les règles anti-slop applicables** :
   - Lesquelles viennent de TIER 1 (déjà vues du Designer Phase 4 en aval) ?
   - Lesquelles devraient s'appliquer EN AMONT en 3B (avant que le Designer Phase 4 prenne le relais) ?
   - Risque de doublon ? Risque de conflit ?

4. **Décider de l'architecture pour 3B** :
   - Faut-il un TIER 1 spécifique pour les subagents 3B ?
   - Faut-il des gates Python dédiés (ex: vérifier que la palette ne contient pas de hex bannis) ?
   - Faut-il des Critiques en aval (ou bien une validation utilisateur suffit) ?

### 8.2 Points de vigilance

- **Ne pas dupliquer les règles** entre 3B et Phase 4. Si une règle est déjà appliquée en TIER 1 Phase 4, elle s'applique au HTML produit, mais peut-être pas aux choix amont (palette/fonts) qui ne sont pas du HTML.

- **Les choix 3B sont consommés en Phase 4** (palette, fonts, etc.). Si 3B produit une palette avec un hex banni, Phase 4 va l'utiliser → audit-slop va le détecter. Donc règle = bloquer EN AMONT.

- **Risque de sur-engineering** : si on rajoute trop de règles en 3B, on bloque la créativité du Designer/Penseur 3B. Garder le strict nécessaire.

- **Patterns 3B vs Phase 4 sont différents** : 3B fait des choix conceptuels (qu'est-ce que je vais utiliser), Phase 4 fait du HTML (comment je l'utilise). Les règles "anti-slop daté" comme `Do NOT translateY hover` n'ont aucun sens en 3B (pas de CSS produit). À l'inverse, "Do NOT use Inter" a un sens en 3B (choix de font) ET en Phase 4 (gate Python).

### 8.3 Livrables attendus

Selon ce que Charles te demandera :
- Diagnostic de couverture anti-slop des étapes 3B actuelles (audit)
- Plan d'application des règles aux étapes 3B (state machine ? gates Python ? Critiques ?)
- Implémentation effective (patches sur les `phase-3b-*.md`)
- Tests E2E (relancer le pipeline complet)

**Important** : maintenir la cohérence avec l'architecture existante. Pas réinventer un système anti-slop parallèle qui ne parlerait pas avec celui de Phase 4.

---

## 9. Contact / questions à Charles avant démarrage

Si tu reprends cette session, voici les choses à clarifier avec Charles :

1. **Périmètre 3B** : toutes les phases `phase-3b-*.md` ou seulement palette + typographie ?
2. **Profondeur** : audit + plan, ou implémentation directe ?
3. **Architecture cible** : reproduire le pattern state-machine (pré/post-conditions bash) ou laisser plus de latitude ?
4. **Test** : faut-il un test E2E dédié 3B après les patches, ou ça remontera dans le test global Phase 4 ?
5. **Limite TIER 1 3B** : si on crée des refs TIER 1 spécifiques 3B, quelle est la limite ? (différente de la limite TIER 1 Phase 4 qui est ~25)

---

## Dernière mise à jour

2026-04-27 — Rédaction du rapport de passation pour application des règles anti-slop aux étapes 3B. Tous les patches Vague 1 + 2 + 2.5 + correctifs P9-P11 appliqués sur Phase 4. Test E2E final en cours côté Charles.
