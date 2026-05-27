# Passation — Chantier anti-slop Phase 3B, carrefour 3 : fonts (3B-1 / 3B-2)

> **Lecture obligatoire avant tout travail sur le carrefour fonts.** Ce document
> contient le contexte complet du chantier anti-slop appliqué à BIG, ce qui a été
> fait sur les carrefours précédents (1. routeur chromatique, 2. palette), les
> méthodes validées, les pièges rencontrés, et toutes les références sources.

---

## 0. TL;DR pour démarrer rapidement

- BIG produit des identités de marque. Sa Phase 4 (style-tiles HTML) avait été équipée d'une architecture **anti-slop** Vague 2 (~120 règles). Cf. `ref/passation-anti-slop-pour-3b.md` (le grand frère de ce document).
- En avril 2026, on a étendu cette architecture aux étapes **3B** (qui FIXENT les choix consommés par Phase 4 : palette, fonts, style, pitch).
- Carrefours déjà traités : **3B-0a routeur chromatique** (chantier 1, commité dans `ecc3d11`) et **3B-3 palette** (chantier 2, à committer).
- **Carrefour à attaquer maintenant** : **3B-1 (penseurs typographiques) + 3B-2 (designer visuel sur planches duos)**.
- Méthodologie validée : stratégie 3-niveaux N1/N2/N3 + pattern "amont prompt + aval gate Python" + tests sur cas réels.
- L'esprit neuf doit faire l'analyse propre du carrefour fonts. Ce document fournit le contexte, les références et les zones de risque pré-identifiées (référentiel, pas analyse).

---

## 1. Contexte global du chantier anti-slop dans BIG

### 1.1 Le problème

Les LLM produisent par défaut des outputs avec des **marqueurs AI-slop** : patterns visuels datés, fonts surutilisées, hex Tailwind par défaut, justifications creuses, format chaotique. Sans intervention, le pipeline BIG hérite de ces biais à chaque sub-agent.

### 1.2 La grille audit-slop (référentiel canonique)

Skill `/audit-slop` (`.claude/skills/audit-slop/`) audite un style-tile HTML sur **4 grilles indépendantes** + synthétiseur :
- **Craft Moderne** : Impeccable + Taste Skill (7 variantes) + GStack — 19 fichiers, ~130 règles
- **Vercel Technique** : `vercel-command.md` — ~60 règles
- **BIG Pipeline** : 10 fichiers BIG + 2 gates Python — ~80 règles
- **Perplexity Temporel** : `perplexity-styles-datés-vs-actuels-2026.md` — ~85 styles classifiés

Cf. `audit-slop/SKILL.md` pour l'architecture complète.

### 1.3 Vague 2 sur Phase 4 (déjà fait — référentiel d'architecture)

Cf. `ref/passation-anti-slop-pour-3b.md` (rédigé pour onboarder le chantier 3B). Points-clés :

- **3 leviers** : TIER 1 (28 règles dans le prompt Designer) + Gates Python déterministes + Critiques sémantiques (4 subagents spécialisés + 1 Synthétiseur)
- **Convention de formulation 3 niveaux** (`ref/anti-slop-formulation-guide.md`) :
  - **N1** principe abstrait (`Do NOT center everything symmetrically`) → OK prompt
  - **N2** pattern nommé (`Do NOT use neumorphism`) → OK prompt
  - **N3** énumération précise (fonts/hex/syntax) → **JAMAIS prompt** (contamination LLM prouvée), gate Python uniquement
- **Mécanismes déterministes > instructions LLM** : chaque fois qu'on a remplacé une instruction texte par un script bash/Python, on a éliminé une classe de shortcuts (P4, P9a, P9b)
- **Stratégie 3 (amont + aval)** : N1/N2 dans le prompt + N3 dans le gate Python. C'est ce qu'on applique à 3B.

### 1.4 Phase 3B en cours (où on en est)

Phase 3B = les sous-étapes qui FIXENT les choix consommés par Phase 4 :

| Sous-étape | Carrefour | Anti-slop |
|---|---|---|
| 3B-0a | Routeur chromatique | ✅ **Chantier 1 fait** (commit `ecc3d11`) |
| 3B-0b | Sélection inspiration esthétique | (touché incidemment) |
| 3B-1 | Penseurs typographiques (display + body) | ⏳ **Carrefour 3 — À FAIRE** |
| 3B-2 | Designer visuel sur planches duos | ⏳ **Carrefour 3 — À FAIRE** |
| 3B-3 | Palette (variantes A/B/C) | ✅ **Chantier 2 fait** (à committer) |
| 3B-5 | Penseur visuel | (carrefour ultérieur) |
| 3B-7a | Styliste | (carrefour ultérieur) |
| 3B-7b | Spécimen stylisé | (carrefour ultérieur) |
| 3B (Interaction 3) | Pitch designer complet | (carrefour ultérieur) |

L'ordre d'attaque est **chronologique du pipeline** : palette (fait) → **fonts** → style → pitch → visuels.

---

## 2. Méthodologie consolidée (à reproduire pour le carrefour fonts)

### 2.1 Pattern d'intégration en 5 étapes

1. **Audit du prompt actuel** : lire les fichiers `phase-3b-{carrefour}.md` et identifier ce qui existe déjà comme règles, ce qui manque
2. **Mapping N1/N2/N3** : pour chaque règle audit-slop applicable, décider si elle va dans le prompt (N1/N2) ou dans le gate Python (N3)
3. **Modifications prompt** : ajouter un bloc "## RÈGLES ANTI-SLOP (universelles)" dans le prompt sub-agent, AVANT le format de sortie
4. **Création gate Python** : `scripts/phase3b-{carrefour}-anti-slop.py` avec ~5-10 checks, mode `--json-output`, exit codes 0=PASS / 1=FAIL / 2=ERREUR
5. **Modification SKILL.md** : ajouter l'invocation du gate après la production du sub-agent, AVANT le checkpoint utilisateur. Pattern : si FAIL → resume du sub-agent (Task fresh, anti-dégradation, prompt relu disque) avec violations en feedback. Max 2 itérations. Si toujours FAIL après 2 reruns, accepter avec ⚠ visible.

### 2.2 Tests obligatoires

- **Test sur palette/sortie existante** : trouver un artefact réel (ancien) du même type, lancer le gate dessus, vérifier qu'il détecte des violations cohérentes
- **Test E2E** : cloner une session de test, supprimer le carrefour cible (mais garder amont), lancer le pipeline depuis ce carrefour
- **Comparaison avant/après** : compter les violations sur l'ancien (sans règles) vs nouveau (avec règles) → quantifier le gain

### 2.3 Patches post-test (anticipés)

Très probable qu'après le premier test, certains checks soient trop stricts. Pattern de réaction :
- Identifier le faux positif (cas légitime que le gate refuse à tort)
- Comprendre la cause structurelle (formulation mathématique trop rigide, manque de contexte, etc.)
- Patcher : assouplir le seuil, ajouter une dépendance contextuelle (ex: lire le mode dominant), passer à une métrique plus riche (ex: distance LCH au lieu de delta_C seul)
- Re-tester pour vérifier qu'on garde le gain anti-slop

Cf. section 4 ci-dessous pour les patches concrets faits sur palette.

---

## 3. Ce qui a été fait — chantiers 1 et 2 en détail

### 3.1 Chantier 1 — Routeur chromatique (3B-0a)

**Fichiers** :
- `phases/phase-3b-gamut-router.md` — bloc "RÈGLES ANTI-SLOP" ajouté (4 règles N1/N2)
- `scripts/phase3b-gamut-router-anti-slop.py` — créé, 9 checks (7 FAIL stricts + 2 TAG-or-FAIL pour zone violet/indigo et neutres non orientés)
- `lib/gamut-visual.mjs` — adapté pour rendre badges cumulables (TERRITOIRE / [SECTORIEL] / [SLOP_RISQUE])
- `SKILL.md` zone 3B-0a (l. 1018-1066) — gate intégré, ancien gate format inline supprimé

**Innovation principale** : le tag `[SLOP_RISQUE]`, cumulable avec TERRITOIRE/[SECTORIEL] dans la colonne Source. Pour les gammes dans la zone "training-defaults LLM" (violet/indigo, neutres pas orientés), le routeur DOIT qualifier (anti-cousin) ET tagger. Le tag se propage à la planche visuelle (badge rouge) et au sub-agent palette en aval (règle 5 du prompt palette).

**Pattern PASS_WITH_PATCH** : si le routeur a qualifié correctement mais oublié le tag, l'orchestrateur patche silencieusement le markdown sans déranger le sub-agent (omission triviale). Si le routeur n'a PAS qualifié → FAIL → resume.

**Test** : sortie Camille (test-camille-test-20260427-1545) PASS clean au premier coup (`9/9 checks anti-slop`). Détection effective des mots-températures, doublons, justifications génériques sur sorties anciennes.

### 3.2 Chantier 2 — Palette (3B-3)

**Fichiers** :
- `phases/phase-3b-palette.md` — bloc "RÈGLES ANTI-SLOP" ajouté (5 règles N1/N2)
- `scripts/phase3b-palette-anti-slop.py` — créé, 10 checks, conversion OKLCH/WCAG standalone (sans dépendance externe)
- `SKILL.md` zone 3B-3 (Vague 2bis) — sous-section "GATE ANTI-SLOP" ajoutée APRÈS le `GATE CHROMATIQUE` existant. Les deux s'enchaînent.

**5 règles N1/N2 dans le prompt** :
1. Pas de pur noir/blanc sur surfaces principales
2. Neutres tintés vers la dominante
3. Un seul accent saturé (distinct du Primary)
4. Anti-cousin AI purple/blue Tailwind (sans nommer les hex)
5. Vigilance accrue si la gamme du routeur porte `[SLOP_RISQUE]` (l'accent doit être en bord de gamme, pas au centre statistique)

**10 checks Python** :
1. Format strict 7 rôles (Primary, Secondary, Accent, Bg dark, Bg light, Text primary, Text secondary)
2. Hex valides
3. Pas de rôles inventés (Primary Light, Surface, Neutral mid…)
4. Pas de #000000 / #ffffff sur Bg dark/light/Text primary
5. Pas de hex AI Tailwind défaut + zone LCH purple/indigo (regex stricte + calcul LCH)
6. Neutres tintés (chroma OKLCH > 0.005)
7. Saturation réduite aux extrêmes (L>0.95 ou L<0.10 → C<0.04)
8. WCAG AA contraste **mode-aware** (cf. patches ci-dessous)
9. Accent distinct via **distance LCH complète** (cf. patches)
10. Justifications non vides + non génériques

### 3.3 Patches du chantier 2 (leçons importantes)

**Premier round de tests** (sans patches) :
- Sur 9 nouvelles palettes Camille : 7 PASS, 2 FAIL (c2-b WCAG, c3-b accent_distinct)
- Mais Charles a noté "moins créatif" — investigation a confirmé la perte de drama chromatique (Bg dark devenus taupes/gris moyens, plus de presque-noirs profonds)

**Cause identifiée** :
- Check WCAG initialement strict : exigeait Text primary lisible sur Bg light ET Bg dark simultanément. Mathématiquement infaisable si on veut un Bg dark presque-noir + Text primary sombre (ou inversement).
- Check accent_distinct mesurait seulement la différence de chroma (saturation). Refusait à tort les accents en opposition chaud/froid (ex: Primary ocre + Accent bleu marine = distinction visuelle forte par hue, mais saturations proches).

**Patch 1 — WCAG mode-aware** :
- Lit le `Mode fond dominant` (SOMBRE/CLAIR) du markdown palette
- Vérifie le contraste texte uniquement sur le fond effectivement utilisé en mode dominant
- Ajoute une vérification minimale (1.5:1 — pas 4.5:1) que les 2 fonds sont distinguables (sinon "même couleur 2 fois")

**Patch 2 — Distance LCH complète pour accent_distinct** :
- Remplace `delta_chroma` seul par `distance LCH` = combinaison de delta saturation + delta hue (position chaud/froid sur la roue)
- Reconnaît les accents froids dans palettes chaudes (et vice-versa) comme distincts

**Résultat post-patches** :
- 9/9 PASS clean au premier coup (vs 7/9 avant patches)
- Drama chromatique récupéré : 9/9 Bg dark presque-noirs profonds (L≈0.05-0.13) vs 0/9 avant patches
- 0 régression sur les 8 autres règles

### 3.4 Comparaison ancien vs nouveau (validation quantitative)

Sur les 9 palettes Camille équivalentes (3 concepts × 3 variantes) :
- **v0 (15 avril, sans règles)** : 51 violations totales, 0/9 PASS
- **v1 (27 avril après-midi, règles strictes)** : 3 violations, 7/9 PASS
- **v2 (27 avril soir, avec patches)** : 0 violations, 9/9 PASS

Réduction du slop ~98%. Drama chromatique préservé.

### 3.5 Limites reconnues

Trois limites identifiées sur le chantier palette qui ne sont PAS encore corrigées :

1. **Trou de couverture "accent dans gamme exclue"** : si le routeur exclut une gamme (ex: cyans turquoise pour Camille, raison ventre mou tech/wellness) mais le sub-agent palette met cet accent quand même (règle "accent libre" du prompt), le gate ne flag pas. Cas observé : c3-c v2 avec Accent cyan `#3FB8C9` sur concept "Foyer Parabolique" — slop sectoriel non détecté. Solution possible : check 11 qui lit la sortie du routeur et flag les accents tombant dans les gammes exclues. Reporté à un chantier 2bis.

2. **Bug pipeline température** : la prescription "Température chaude" du scoping (Phase 2A) n'est pas remontée au routeur. Le routeur ne reçoit que `aesthetic-profile.md` (souvent absent). Donc le routeur peut "dévier" de la prescription du scoping. Charles a décidé de "vivre avec" pour l'instant (l'utilisateur peut filtrer manuellement via la planche visuelle). À noter pour un chantier dédié.

3. **Divergence A/B/C plus subtile qu'avant** : en forçant le respect des règles, on élimine les anciennes "divergences à coup de slop" (accent désaturé, format chaotique). Pour récupérer plus de divergence sans rouvrir le slop, il faut enrichir le **prompt de divergence B/C** lui-même (forcer rotation de mode dominant ou de température), pas relâcher le gate. Reporté.

---

## 4. Le carrefour 3 — fonts (3B-1 / 3B-2) — ce que tu dois faire

### 4.1 Ce qui existe déjà (référentiel structurel)

**Architecture du carrefour fonts** : c'est plus complexe que palette parce qu'il y a **2 sub-agents distincts**.

#### Sub-agent 3B-1 : penseurs typographiques (textuel, AVEC noms)

Deux invocations parallèles par concept :
- `phases/phase-3b-penseur.md` — penseur display (12-15 fonts longlist)
- `phases/phase-3b-penseur-body.md` — penseur body (10 fonts longlist)

Le penseur reçoit la liste numérotée des fonts du **pool autorisé** (variable `{font_list_display}` ou `{font_list_body}`) et choisit dans cette liste. **Il ne peut pas inventer une font hors liste**.

Pool de fonts : `ref/font-pools/font-pool-display-A{1,2,3}-mapping.json` et `font-pool-body-A{1,2,3}-mapping.json`. Indexé par curseur A (niveau d'audace).

Output : `{brand}-penseur-c{N}.md` (display) et `{brand}-penseur-body-c{N}.md` (body) avec scan binaire COMPATIBLE/INCOMPATIBLE et longlist ordonnée 12-15 (display) ou 10 (body).

#### Sub-agent 3B-2 : designer visuel sur planches duos (visuel, SANS noms)

Le designer ne voit **pas les noms de fonts** — il voit des **planches PNG haute résolution** générées par `lib/font-pool-contact-sheet.mjs`. Les fonts sont anonymisées en référence "planche X position A/B".

Trois interactions séparées avec **gate par fichier obligatoire** entre interaction 1 et 2 :
1. **Interaction 1** : description pure des planches sans contexte concept (anti-biais de confirmation). Le designer ÉCRIT ses descriptions dans `{brand}-descriptions-c{N}.md`.
2. **Interaction 2** : choix sur les planches avec le concept narratif (resume avec descriptions précédentes en input + notes anonymisées du penseur).
3. **Interaction 3** (ailleurs, en 3B-design) : pitch complet avec NOMS RÉELS injectés.

Mécanisme d'anonymisation rang→position : l'orchestrateur shuffle les 10 fonts du penseur (Fisher-Yates) AVANT de les répartir sur les planches duos, pour casser le biais de primauté.

#### Validation visuelle 3B-bis

Après le pitch designer (Interaction 3), un script `lib/font-palette-specimen.mjs` génère un specimen PNG du concept (font display + body + palette). Le sub-agent designer est resume avec ce screenshot pour valider visuellement (et ajuster si besoin).

#### Backups et historique

`{brand}-font-backups.md` contient les choix principaux + 2 backups par concept. Permet de promouvoir un backup si la 1re sélection ne fonctionne pas en 3B-bis (changement de font sans tout reprendre).

### 4.2 Zones de risque pré-identifiées (référentiel — pas analyse)

Voici les règles audit-slop qui CONCERNENT les fonts, que j'avais déjà cartographiées dans la phase initiale (cf. `ref/extraction-vague2-2026-04-26.md`). À toi d'en faire le mapping N1/N2/N3 final et de décider quels checks coder.

| ID | Règle | Type | Notes pour le mapping |
|---|---|---|---|
| **R-013** | Ban Inter, Roboto, Open Sans, Lato, Montserrat (les "invisibles") | NEG, grep-able | N3 (gate Python) — la liste vit dans le code, jamais dans le prompt. À noter : le pool de fonts limité bloque déjà ces fonts en amont… **vérifier que le pool est sain** avant de coder un gate sur les fonts choisies |
| **Generic serifs** | Times New Roman, Georgia, Garamond, Palatino sans justification éditoriale | NEG, grep-able | N3 — idem, vérifier d'abord le pool |
| **R-016** | One font + multiple weights > two competing typefaces. Ajouter une 2e font seulement pour CONTRASTE structural authentique (serif/sans, geometric/humanist, condensed/wide) | POS, sémantique | N2 — règle déjà partiellement présente dans les prompts |
| **R-103** | Single font + weights > 2 fonts en compétition (semi-doublon R-016) | POS, sémantique | N2 — à fusionner avec R-016 dans le prompt |
| **R-014** | Procédure de sélection font (brief words → physical object → browse → avoid defaults) | POS, processuelle | Déjà implémentée structurellement par le pool + planches duos |
| **R-015** | Pair fonts with multi-axis contrast (Serif+Sans, Geometric+Humanist, Condensed+Wide) | POS, sémantique | N2 — règle de pairing |
| **R-017** | font-display: swap + size-adjust pour minimiser CLS | POS, technique | N/A en 3B (Phase 4 / HTML) |
| **R-019** | OpenType : tabular-nums data, small-caps abréviations, no ligatures code | POS, technique | N/A en 3B (Phase 4 / CSS) |
| **R-102** | Font weight range : Regular(400)+Medium(500)+SemiBold(600) min | POS, technique | N/A en 3B (Phase 4 / CSS) |

**Anti-cousin Inter** : si on bannit Inter, le LLM choisit Roboto. Liste de cousins à inclure dans le gate : "Inter et ses cousins (Roboto, Open Sans, Lato, Montserrat — sans serifs géométriques 2010s monoculture)".

**Marqueurs Perplexity Temporel** sur les fonts (cf. `audit-slop/agents/perplexity-temporel.md` qui pointe vers `ref/perplexity-styles-datés-vs-actuels-2026.md`) :
- Inter + Inter mono-font (mono-stack par défaut sur SaaS) — daté
- Pairings Playfair + Lato — daté
- Pairings Cormorant + Montserrat — daté
- Fonts contemporaines actuelles (registre 2025-2026) : Geist, Outfit, Cabinet Grotesk, Satoshi, PP Editorial New, Space Grotesk, etc.

### 4.3 Particularités à anticiper (à creuser)

1. **Le pool de fonts est CONTRAINT en amont** → le gate sur les fonts CHOISIES sera moins critique que pour la palette (où les hex sont libres). MAIS : il faut **vérifier que le pool lui-même est sain**. Si le pool A=1 contient Inter, c'est un slop structurel à corriger amont.
2. **Le designer voit des planches PNG** (pas les noms) → le risque de slop nominal est faible côté designer. Le slop peut venir du penseur (qui choisit les noms) OU du pool lui-même.
3. **Le pitch designer 3B-design Interaction 3** est l'endroit où les noms de fonts apparaissent en clair (variables `{display_font}`, `{body_font}`). Un gate sur le pitch (existe déjà : `phase3b-css-gate.py` mais limité à "ZÉRO CSS dans pitch") pourrait être étendu à "ZÉRO font datée mentionnée".
4. **Articulation avec gates existants** : `phase3b-css-gate.py` (gate existant pour le pitch) — à étendre ou créer un gate fonts séparé ?
5. **Cohérence avec le styliste 3B-7a** : le styliste choisit un style officiel parmi 34 (`ref/styles-bibliotheque.md`) qui a ses propres pairings typographiques recommandés. Risque de conflit avec la sortie du penseur typo qui a tourné AVANT le styliste.

### 4.4 Articulation avec les sous-agents et les artefacts

| Artefact | Produit par | Ce qu'on peut vérifier mécaniquement |
|---|---|---|
| `ref/font-pools/font-pool-{display,body}-A{1,2,3}-mapping.json` | Curé manuellement | Pas de fonts datées dans le pool (gate "préventif" sur le pool lui-même) |
| `{brand}-penseur-c{N}.md` (display longlist) | Penseur typo display | Format : 12-15 fonts, justifications spécifiques, pas de phrases génériques |
| `{brand}-penseur-body-c{N}.md` (body longlist) | Penseur typo body | Format : 10 fonts, justifications spécifiques |
| `{brand}-descriptions-c{N}.md` (interaction 1 designer) | Designer visuel interaction 1 | Vérifier qu'aucun nom de font n'a leaké (anti-biais — la gate par fichier existe déjà) |
| `{brand}-pitch-c{N}.md` (interaction 3) | Designer visuel + pitch | Vérifier qu'aucune font datée n'est mentionnée dans le pitch final |
| `{brand}-font-backups.md` | Designer visuel interaction 2 | Format + cohérence inter-concepts |

### 4.5 Ce que tu dois faire (à toi de cadrer)

À toi de proposer à Charles :
- L'audit complet des prompts 3B-1/3B-2 (penseur display, penseur body, designer visuel)
- L'audit du pool de fonts lui-même (les fichiers JSON dans `ref/font-pools/`)
- Le mapping N1/N2/N3 spécifique aux fonts
- L'architecture proposée (un gate sur quel artefact ? étendre `phase3b-css-gate.py` ou créer un gate dédié `phase3b-fonts-anti-slop.py` ?)
- L'implémentation
- Les tests sur cas réel (cf. sessions Camille pour comparaison ancien/nouveau)
- Les patches post-test si besoin

**Important** : applique la même méthode que pour les chantiers précédents (cf. section 2). Charles est rigoureux et préfère qu'on prenne un carrefour à la fois, qu'on teste, qu'on valide, qu'on commit, avant de passer au suivant.

---

## 5. Références exhaustives

### 5.1 Fichiers BIG à lire d'abord

| Fichier | Pourquoi |
|---|---|
| `ref/passation-anti-slop-pour-3b.md` | **Le grand frère de ce document** — contexte Vague 2 sur Phase 4, architecture détaillée, leçons. Lecture OBLIGATOIRE en complément |
| `ref/anti-slop-formulation-guide.md` | **CRITIQUE** — convention 3 niveaux N1/N2/N3 + clause anti-cousin. À ne JAMAIS oublier |
| `ref/extraction-vague2-2026-04-26.md` | Extraction des 182 règles audit-slop avec destination proposée (TIER_1 / GATE_PYTHON / CRITIQUE_TIER_2) |
| `SKILL.md` | Pipeline complet. Zones pertinentes : 3B-1 (l. ~1187-1500 environ), 3B-2 (interactions designer visuel), 3B-3 (palette, l. 1561+), 3B-bis (validation visuelle) |
| `phases/phase-3b-penseur.md` | Prompt penseur display |
| `phases/phase-3b-penseur-body.md` | Prompt penseur body |
| `phases/phase-3b-design.md` | Prompt designer pitch (Interaction 3 — l'endroit où les noms de fonts apparaissent en clair) |
| `ref/font-matching-rules.md` | Règles de matching font × concept (lu par penseurs et designer visuel) |

### 5.2 Fichiers BIG du chantier 1 (routeur) — pour référence d'architecture

| Fichier | Rôle |
|---|---|
| `phases/phase-3b-gamut-router.md` | Prompt routeur avec règles anti-slop intégrées |
| `scripts/phase3b-gamut-router-anti-slop.py` | Gate Python ~600 lignes, 9 checks, mode `--json-output`, tag `[SLOP_RISQUE]` cumulable |
| `lib/gamut-visual.mjs` | Adapté pour rendre badges multiples |
| `SKILL.md` zone 3B-0a (l. ~982-1066) | Orchestration : trace disque → gate → patch ou resume → planche visuelle |

### 5.3 Fichiers BIG du chantier 2 (palette) — pour référence d'architecture

| Fichier | Rôle |
|---|---|
| `phases/phase-3b-palette.md` | Prompt palette avec 5 règles anti-slop intégrées |
| `scripts/phase3b-palette-anti-slop.py` | Gate Python ~700 lignes, 10 checks, conversion OKLCH/WCAG standalone, mode `--json-output` |
| `SKILL.md` zone 3B-3 Vague 2bis | GATE ANTI-SLOP ajoutée APRÈS le GATE CHROMATIQUE existant |

### 5.4 Skill `audit-slop` (matière originelle du chantier)

| Chemin | Rôle |
|---|---|
| `.claude/skills/audit-slop/SKILL.md` | Orchestrateur audit-slop (5 grilles, 4 agents + synthétiseur) |
| `.claude/skills/audit-slop/agents/craft-moderne.md` | Agent Craft Moderne (Impeccable + Taste + GStack) |
| `.claude/skills/audit-slop/agents/vercel-technique.md` | Agent Vercel Technique (`vercel-command.md`) |
| `.claude/skills/audit-slop/agents/big-pipeline.md` | Agent BIG Pipeline (lance les 2 gates Python) |
| `.claude/skills/audit-slop/agents/perplexity-temporel.md` | Agent Perplexity Temporel |
| `.claude/skills/audit-slop/agents/synthetiseur.md` | Synthétiseur arbitre |
| `.claude/skills/audit-slop/sources/impeccable/SKILL.md` | Source Impeccable principale |
| `.claude/skills/audit-slop/sources/impeccable/reference/typography.md` | **CRITIQUE pour fonts** — règles typographiques détaillées Impeccable |
| `.claude/skills/audit-slop/sources/taste-skill/taste-skill.md` | Source Taste Skill principale (3 dials, AI Tells section 7) |
| `.claude/skills/audit-slop/sources/taste-skill/soft-skill.md` | "Awwwards-tier" / Beautiful UI — règles fonts premium |
| `.claude/skills/audit-slop/sources/taste-skill/minimalist-skill.md` | Banned Elements section |
| `.claude/skills/audit-slop/sources/taste-skill/brutalist-skill.md` | Banned universels (extraire seulement) |
| `.claude/skills/audit-slop/sources/taste-skill/redesign-skill.md` | Audit granulaire par catégorie |
| `.claude/skills/audit-slop/sources/taste-skill/images-taste-skill.md` | Section 26 ANTI-AI-SLOP RULES |
| `.claude/skills/audit-slop/sources/taste-skill/stitch-skill.md` | Section 9 Anti-Patterns AI Tells |
| `.claude/skills/audit-slop/sources/gstack/design-review.md` | Checklist 10 catégories / ~80 items |
| `.claude/skills/audit-slop/sources/gstack/plan-design-review.md` | Design Hard Rules + AI Slop blacklist 11 items |
| `.claude/skills/audit-slop/sources/vercel-command.md` | Vercel Web Interface Guidelines (typographie section incluse) |

### 5.5 Documents de référence Perplexity

| Fichier | Rôle |
|---|---|
| `ref/perplexity-styles-datés-vs-actuels-2026.md` | Classification 85 styles + marqueurs slop datés (incluant fonts datées par registre) — **à scanner spécifiquement pour les pairings typographiques datés** |
| `ref/perplexity-composition-patterns-report.md` | 12 patterns datés × 12 actuels (composition, partiellement liée aux fonts) |
| `ref/perplexity-composition-detail-report.md` | Détail composition |

### 5.6 Documents de référence BIG sur les fonts

| Fichier | Rôle |
|---|---|
| `ref/font-matching-rules.md` | 5 règles de matching font × concept (densité, registre sensoriel, justification spécifique, pas de mots-clés isolés, feeling global) — lu par penseurs et designer |
| `ref/font-pools/font-pool-display-A{1,2,3}-mapping.json` | Pool de fonts display indexé par curseur A |
| `ref/font-pools/font-pool-body-A{1,2,3}-mapping.json` | Pool body |
| `ref/font-selection-rex.md` | REX sur les choix de fonts passés (à lire pour comprendre les pièges historiques) |
| `ref/font-selection-next-session.md` | Notes pour next session sur fonts |
| `ref/styles-bibliotheque.md` Partie A | 34 styles avec champ "Signatures à incarner" qui inclut souvent des recommandations typographiques |

### 5.7 Plans Vague 2 (architecture historique)

| Fichier | Rôle |
|---|---|
| `ref/plan-vague2-point1-regles-negatives-externes.md` | Plan d'intégration des règles négatives externes |
| `ref/plan-vague2-point2-regles-positives.md` | Plan des règles positives |
| `ref/plan-integration-anti-slop.md` | Plan historique du chantier Vague 1 |

### 5.8 Sessions de test pour comparaison ancien/nouveau

| Session | Brand | Notes |
|---|---|---|
| `outputs/test-camille-test-20260415-1733/` | Camille | **Ancienne session avant règles anti-slop palette** — utilisée pour comparaison v0 vs v2 du chantier palette. Contient `{brand}-penseur-c{N}.md`, `{brand}-pitch-c{N}.md`. Bonne base pour comparer ancien/nouveau sur fonts |
| `outputs/test-camille-test-20260427-1545/` | Camille | Session originale post-routeur anti-slop (validée par Charles) |
| `outputs/test-camille-test-20260427-3b3-anti-slop-v2/` | Camille | Test palette v2 (avec patches) — peut servir d'input pour test E2E fonts |
| `outputs/test-voltapilot-vague2.5-20260427-*/` | VoltaPilot | Sessions Phase 4 récentes |

### 5.9 Outils de génération pour les fonts

| Fichier | Rôle |
|---|---|
| `lib/font-pool-contact-sheet.mjs` | Génère les planches duos PNG (pour designer visuel) |
| `lib/font-palette-specimen.mjs` | Génère le specimen PNG de validation visuelle (3B-bis) |
| `lib/font-recap-all.mjs` | Récap des fonts choisies par concept |

---

## 6. Comment travailler — méthodologie reproductible

1. **Lire ce document + `ref/passation-anti-slop-pour-3b.md` + `ref/anti-slop-formulation-guide.md`** (3 lectures clés en début de session)
2. **Lire le prompt actuel** des sub-agents 3B-1 et 3B-2 (`phase-3b-penseur.md`, `phase-3b-penseur-body.md`, et la zone 3B-2 du SKILL.md)
3. **Lire les fichiers du pool** de fonts (`ref/font-pools/*.json`) pour vérifier que le pool est sain
4. **Lire `ref/font-matching-rules.md`** + `ref/styles-bibliotheque.md` (Partie A — pour comprendre les pairings recommandés par style)
5. **Lire `ref/perplexity-styles-datés-vs-actuels-2026.md`** + `audit-slop/sources/impeccable/reference/typography.md` (matière fondamentale fonts)
6. **Faire l'audit + cartographie + proposition d'architecture** à Charles
7. **Implémenter** après validation
8. **Tester** sur sessions existantes
9. **Patcher** si besoin
10. **Committer** quand tout est validé
11. **Mettre à jour ce document** avec les leçons apprises du chantier 3 (pour la passation suivante chantier 4 = style)

---

## 7. État commit / git

À la date du **2026-04-28** :
- **Chantier 1 routeur** : commit `ecc3d11` "chore: import preexisting Phase 3B work + style refs + session passations" (27 avril 15:20)
- **Chantier 2 palette + patches** : **PAS ENCORE COMMITÉ** (Charles le fera dans son flow normal). Modifications en cours sur `phase-3b-palette.md`, `scripts/phase3b-palette-anti-slop.py` (créé), `SKILL.md` zone 3B-3.

Vérifier avec `git status` au démarrage. Si le chantier 2 n'est pas commité, demander à Charles si on commit avant de toucher 3B-1/3B-2 ou si on continue.

---

## 8. Questions de cadrage à poser à Charles avant démarrage

Charles préfère un carrefour à la fois. Pose ces questions au début de la session :

1. **Périmètre 3B-1/3B-2** : on couvre les 2 sub-agents en un seul chantier (penseur + designer) ou on les sépare (3a = penseur, 3b = designer visuel) ?
2. **Pool de fonts** : on audite et corrige le pool lui-même si nécessaire, ou on considère que le pool est intouchable et on travaille uniquement sur les sub-agents qui choisissent dedans ?
3. **Articulation gate existant** : on étend `phase3b-css-gate.py` (qui couvre le pitch en mode "ZÉRO CSS") pour ajouter un check fonts datées, ou on crée un gate dédié `phase3b-fonts-anti-slop.py` ?
4. **Test E2E** : sur `test-camille-test-20260427-1545` (depuis 3B-1), ou sur un autre brief ? Cloner et nettoyer comme pour palette ?
5. **Décisions de seuil** : Charles arbitre les cas limites observés au test (calque sur palette : observer puis proposer un patch).

---

## Dernière mise à jour

2026-04-28 — Rédaction par la session qui a terminé les chantiers 1 (routeur) et 2 (palette + patches). Bonne chance pour le chantier 3.
