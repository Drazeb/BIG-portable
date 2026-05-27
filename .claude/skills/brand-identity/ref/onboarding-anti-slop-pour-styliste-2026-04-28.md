# Onboarding — chantier anti-slop : ce que la session styliste (3B-7a) doit savoir

> **Pour la session qui travaille sur le sub-agent styliste (`phase-3b-styliste.md`)**.
> Tu connais bien ton sub-agent. Mais il existe un **gros chantier anti-slop transversal** dans BIG dont tu n'as probablement pas le contexte. Ce document te le donne, pointe les failles repérées sur le styliste depuis ce point de vue, et te laisse décider quoi en faire.

---

## 1. Le chantier anti-slop dans BIG — vue d'ensemble

### 1.1 Le problème de fond

Les LLM produisent par défaut des outputs avec des **marqueurs slop AI** : patterns visuels datés, fonts surutilisées, hex Tailwind par défaut, justifications creuses, format chaotique. Sans intervention, le pipeline BIG hérite de ces biais à chaque sub-agent.

**Exemples concrets de slop chromatique** : pure noir/blanc sur surfaces principales, AI purple/blue gradient (`#6366f1` style indigo), aurora 3 blobs génériques, accent plus terne que la dominante.

**Exemples concrets de slop typographique** : Inter / Roboto / Open Sans (les "invisibles"), Times New Roman / Georgia sans justification, single font sans variation de poids, ou 2 fonts en compétition sans contraste structurel.

**Exemples concrets de slop compositionnel** : 50/50 hero rigide, grids 3 cards identiques, 3 features icon+title+desc, footer 4 colonnes.

### 1.2 La grille audit-slop (référentiel canonique)

Il existe un skill `/audit-slop` (`.claude/skills/audit-slop/`) qui audite un style-tile HTML produit par BIG sur **4 grilles indépendantes** + 1 synthétiseur :

| Agent auditeur | Sources |
|---|---|
| Craft Moderne | Impeccable + Taste Skill (7 variantes) + GStack — 19 fichiers, ~130 règles |
| Vercel Technique | `vercel-command.md` — ~60 règles |
| BIG Pipeline | 10 fichiers BIG + 2 gates Python — ~80 règles |
| Perplexity Temporel | Rapport classification 85 styles + marqueurs datés |

Total : **~212 règles brutes**, **~158 universelles** (HTML vanilla), **~54 contextuelles** (React/Framer/Stitch).

### 1.3 La Vague 2 (déjà faite — sur Phase 4)

Avant le chantier 3B en cours, une grosse Vague 2 anti-slop a importé **~120 règles dans BIG en amont (Phase 4)**. Architecture stratifiée :

- **TIER 1** : ~28 règles structurantes injectées dans le prompt du Designer Phase 4 (limite empirique : pas plus de ~25-30, sinon sur-engineering observé)
- **Gates Python déterministes** (`scripts/phase4-blacklist-gate.py`, `phase4-finishing-gate.py`) : checks regex mécaniques sur le HTML produit
- **Critiques sémantiques** : 4 subagents spécialisés (a11y, composition, typo-copy, craft) + 1 Synthétiseur, pour ~80 règles non-grep-ables

Détail dans `ref/passation-anti-slop-pour-3b.md` (le grand frère de ce document — **à lire si tu veux le contexte complet**).

### 1.4 Le chantier 3B en cours

La Vague 2 a traité **Phase 4**. Mais la 3B FIXE des choix consommés par Phase 4 (palette, fonts, style, pitch). Donc le slop peut être **introduit en amont** (palette qui contient `#000000`, font datée choisie, style mal-cadré) puis se propager. Solution : équiper aussi les sous-étapes 3B.

**Ordre d'attaque chronologique du pipeline** :

| Sous-étape | Carrefour | Statut |
|---|---|---|
| 3B-0a | Routeur chromatique | ✅ Fait (commit `ecc3d11`) |
| 3B-3 | Palette (variantes A/B/C) | ✅ Fait (à committer) |
| 3B-1 / 3B-2 | Fonts (penseurs typo + designer visuel) | ⏳ En cours (autre session) |
| **3B-7a** | **Styliste** | **⏳ Toi** |
| 3B-5 | Direction visuelle (penseur visuel) | À faire |
| 3B Interaction 3 | Pitch designer complet | À faire |

---

## 2. La méthodologie validée (à connaître)

### 2.1 Convention de formulation 3 niveaux

Référence canonique : `ref/anti-slop-formulation-guide.md` (à lire absolument avant toute modif de prompt).

| Niveau | Forme | Risque LLM | Verdict |
|---|---|---|---|
| **N1** Principe abstrait | `Do NOT center everything symmetrically` | Aucun | ✅ OK prompt |
| **N2** Pattern nommé non-substituable | `Do NOT use neumorphism` | Aucun | ✅ OK prompt |
| **N3** Énumération précise (fonts/hex/syntax) | `Do NOT use #6366f1`, `Do NOT use Inter` | **CONTAMINATION CRÉATIVE PROUVÉE** | ❌ JAMAIS prompt — gate Python uniquement |

**Le risque N3 est prouvé empiriquement** : `Do NOT use #6366f1` lit le LLM comme "cette teinte est cool, je peux jouer autour". Bannir Inter → choisit Roboto. Documenté sur 17 tests consécutifs.

**Stratégie 3 (amont + aval) validée** : N1/N2 dans le prompt + N3 dans gate Python. Ne pas relâcher l'un au profit de l'autre.

### 2.2 Pattern d'intégration en 5 étapes

1. **Audit du prompt actuel** : ce qui existe, ce qui manque
2. **Mapping N1/N2/N3** : pour chaque règle audit-slop applicable, décider amont (prompt) ou aval (gate)
3. **Modifications prompt** : ajouter un bloc "## RÈGLES ANTI-SLOP (universelles)" AVANT le format de sortie
4. **Création gate Python** : `scripts/phase3b-{carrefour}-anti-slop.py` — ~5-10 checks, mode `--json-output`, exit codes 0=PASS / 1=FAIL / 2=ERREUR
5. **Modification SKILL.md** : invocation du gate après production sub-agent, AVANT checkpoint utilisateur. FAIL → resume sub-agent (Task fresh, prompt relu disque) avec violations en feedback. Max 2 itérations.

### 2.3 Patches post-test (anticipés)

Très probable qu'après le premier test, certains checks soient trop stricts. Pattern observé sur palette :
- WCAG 4.5:1 sur les 2 fonds simultanément interdisait des Bg dark presque-noirs profonds → patch "mode-aware"
- Accent_distinct mesurait seulement la saturation → patch "distance LCH complète" pour reconnaître les oppositions chaud/froid

À toi d'observer après le premier test, identifier les faux positifs, et patcher proprement.

---

## 3. Ce qui a déjà été fait (chantiers 1+2 — pour info architecturale)

### Chantier 1 — Routeur chromatique (3B-0a)

- Prompt enrichi : 4 règles N1/N2 (zone violet/indigo qualifiée, neutres orientés, spécificité, pas de doublons)
- Gate Python : 9 checks, mode `--json-output`
- **Innovation : tag `[SLOP_RISQUE]` cumulable** (calque de `[SECTORIEL]` existant) — permet d'autoriser une gamme à risque MAIS la signaler en aval. Pattern propagé : la palette en aval reçoit le tag et applique une vigilance accrue sur les hex choisis dans cette gamme.
- Pattern PASS_WITH_PATCH : si l'oubli est trivial (tag absent mais qualification OK), l'orchestrateur patche silencieusement sans déranger le sub-agent.

### Chantier 2 — Palette (3B-3)

- Prompt enrichi : 5 règles N1/N2
- Gate Python : 10 checks (format strict, hex valides, rôles inventés, pur noir/blanc, hex AI Tailwind, neutres tintés, saturation aux extrêmes, WCAG mode-aware, accent distinct par distance LCH, justifications)
- Conversion OKLCH/WCAG standalone (sans dépendance externe)
- 2 patches post-test : WCAG mode-aware + distance LCH pour accent

### Métriques validation chantier 2

Sur 9 palettes Camille équivalentes (3 concepts × 3 variantes A/B/C) :
- Avant règles : 51 violations totales, 0/9 PASS
- Après règles + patches : 0 violations, 9/9 PASS clean au premier coup
- Drama chromatique préservé (Bg dark presque-noirs profonds OK)

Réduction du slop ~98%.

---

## 4. Failles que je repère sur le styliste — à challenger

> Ces points sont **mes observations** depuis l'extérieur du chantier styliste. Je ne connais pas tous les arbitrages que tu as faits. À toi de challenger : confirmer / infirmer / nuancer.

### 4.1 Ce qui existe déjà dans `phase-3b-styliste.md` (et qui est bien)

- Interdiction Partie B du catalogue (10 styles datés/cycliques en déclin)
- Interdiction "matière BIG" inventée (anciens registres bricolés type "Editorial Photographique Monographique")
- Mix max 2 styles
- Scan exhaustif 01-34 obligatoire (binaire COMPATIBLE/INCOMPATIBLE)
- Longlist 6-8 + test de spécificité auto-évalué
- Étape 5 "Vérification anti-slop finale" + bloc "Garde-fous anti-slop activés"
- Anti-confabulation
- Calibrage par curseur A

C'est probablement **le prompt le plus mature de tout le pipeline** sur le plan textuel.

### 4.2 Failles repérées (textuellement présent ≠ mécaniquement vérifié)

| # | Faille | Pourquoi c'est problématique | Suggestion |
|---|---|---|---|
| 1 | **Le scan 01-34 n'est jamais vérifié mécaniquement** | Le LLM peut bâcler et n'en scanner que 5-6 qui lui paraissent évidents. Un compte des numéros présents dans la sortie révèle le pot aux roses. | Gate Python qui compte 34 numéros (01 à 34) présents dans la section "Scan exhaustif" |
| 2 | **Le style retenu n'est pas vérifié contre la liste exacte du catalogue** | Si le styliste écrit "Editorial Premium" alors que le catalogue contient "Editorial Grid #66", c'est une "matière BIG inventée" qu'on n'attrape pas | Extraction des 34 noms officiels depuis `ref/styles-bibliotheque.md` Partie A + grep dans la fiche produite |
| 3 | **Le mix max 2 n'est pas compté mécaniquement** | "mix Editorial × Brutalism × Anti-AI Crafting" (3 styles) — interdit mais pas vérifié | Compter "×" ou "modulateur" dans la section Arbitrage final |
| 4 | **Le bloc "Garde-fous anti-slop activés" n'est pas vérifié présent + ≥3 puces** | Section sautée ou bâclée à 1 puce vide. Or c'est précisément ce qui se transmet au pitch designer en aval — la **clé de la propagation** | Parser markdown : compter puces dans la section, vérifier non-générique |
| 5 | **Marqueurs Partie C dans les "Signatures à incarner"** | Le catalogue documente une Partie C (marqueurs slop transverses qui peuvent contaminer N'IMPORTE QUEL style légitime : purple/indigo, aurora 3 blobs génériques, Inter mono-font, glow shadow, translateY au hover). Le styliste peut copier des signatures du catalogue qui en contiennent | Grep blacklist sur la section "Signatures à incarner" |
| 6 | **Justifications longlist génériques** | "Ce style est moderne et épuré" / "convient bien" / "dans l'air du temps" — patterns identiques à ceux qu'on attrape déjà en palette/routeur. Le test de spécificité auto-évalué par le sub-agent n'est pas fiable | Grep réutilisable des patterns existants dans `phase3b-palette-anti-slop.py` ou `phase3b-gamut-router-anti-slop.py` |
| 7 | **Avis du DA bâclable** | "Force majeure : OK / Risque : aucun / ZAG : bon" en 3 lignes vides | Vérification longueur min + non-générique sur les 3 axes |

### 4.3 Une faille architecturale potentielle (à challenger plus profondément)

Le styliste tourne **APRÈS** la palette + les fonts validées. Il doit en théorie vérifier la **cohérence système** (style + palette + fonts = même univers sensoriel). C'est dans le prompt (règle 6 du matching), mais auto-évalué.

**Faille** : si la palette ressort bordeaux mat + ocre saturé + crème (univers craft chaud), et le styliste retient "Cyberpunk UI" (univers tech froid néon), c'est une dissonance. L'auto-évaluation peut louper. Mais c'est sémantique et pas trivial à coder.

**Idée pour aller plus loin** : récupérer le diagnostic de température du routeur chromatique (qui fait son raisonnement interne sur chaud/froid à partir des territoires) et vérifier que le **registre** du style retenu est compatible. Mais c'est un check fragile — à toi de juger si ça vaut le coup ou si ça crée des faux positifs.

### 4.4 Pattern utile à connaître : `[SLOP_RISQUE]` cumulable

Inventé pour le routeur chromatique : un **tag** dans une cellule de tableau, cumulable avec d'autres tags (`TERRITOIRE [SLOP_RISQUE]`, `[SECTORIEL] [SLOP_RISQUE]`).

**Idée transposable au styliste** : si le styliste retient un style officiel mais que ce style touche une **zone à risque** (ex: Aurora UI #10 qui est légitime mais frôle la zone purple/indigo générique, ou Glassmorphism #3 qui frôle le glassmorphism décoratif daté), il pourrait le tagger `[SLOP_RISQUE]` dans son arbitrage final. Le pitch designer en aval verrait le tag et serait extra-vigilant sur les prescriptions concrètes.

À challenger : est-ce utile ? Est-ce que ça fait doublon avec le bloc "Garde-fous anti-slop activés" qui existe déjà ?

---

## 5. Références clés (où aller chercher la matière)

### À lire en priorité (~30 min)

| Fichier | Pourquoi |
|---|---|
| `ref/anti-slop-formulation-guide.md` | Convention 3 niveaux N1/N2/N3 — règle d'or anti-contamination |
| `ref/passation-anti-slop-pour-3b.md` | Contexte Vague 2 (Phase 4) + leçons architecturales |
| `ref/analyse-anti-slop-3b-style-visual-pitch-2026-04-28.md` | Analyse re-challengée des 3 carrefours restants — section dédiée styliste |
| `ref/extraction-vague2-2026-04-26.md` | Extraction des 182 règles audit-slop avec destination proposée |

### Fichiers de référence du chantier styliste

| Fichier | Rôle |
|---|---|
| `phases/phase-3b-styliste.md` | Prompt actuel du styliste |
| `ref/styles-bibliotheque.md` | Catalogue 34 styles Partie A + 10 Partie B + marqueurs Partie C |
| `ref/style-matching-rules.md` | 5 règles matching + 2 règles pairing |
| `ref/styles-matching-protocol.md` | Protocole 5 étapes + format fiche |
| `phases/phase-3b-specimen-stylise.md` | Comment le style se transmet en aval (3B-7b) |

### Patterns d'architecture (chantiers 1+2 — pour copier la méthode)

| Fichier | Rôle |
|---|---|
| `scripts/phase3b-gamut-router-anti-slop.py` | Pattern référence (9 checks, tag cumulable, mode `--json-output`) |
| `scripts/phase3b-palette-anti-slop.py` | Pattern référence (10 checks, conversions OKLCH/WCAG standalone) |
| `phases/phase-3b-gamut-router.md` (modifié) | Exemple bloc "RÈGLES ANTI-SLOP" en N1/N2 |
| `phases/phase-3b-palette.md` (modifié) | Idem |
| `SKILL.md` zone 3B-0a et zone 3B-3 (Vague 2bis) | Patterns d'intégration gate dans le pipeline |

### Skill audit-slop (matière originelle)

`.claude/skills/audit-slop/` — toute l'architecture d'audit. Regarder en particulier :
- `audit-slop/sources/impeccable/reference/typography.md` (typo)
- `audit-slop/sources/taste-skill/*.md` (7 variantes incluant règles fonts/styles)
- `audit-slop/sources/gstack/design-review.md` (checklist 10 catégories)

---

## 6. Ce que je propose comme prochaines actions (à challenger)

1. **Lire les 4 fichiers prioritaires** (cf. section 5)
2. **Re-challenger mes 7 failles** (section 4.2) — confirmer / infirmer / nuancer chacune
3. **Décider de l'architecture** : un gate Python `phase3b-style-anti-slop.py` (calque palette/routeur) ou intégration au styliste autrement ?
4. **Implémenter** si validé par Charles
5. **Tester** sur fiches `{brand}-style-choice-c{N}-{a,b,c}.md` existantes (sessions Camille récentes)
6. **Patcher** les checks trop stricts (anticipé : test de spécificité, vérif Avis du DA substantiel)

Tu peux tout à fait me re-challenger sur les priorités, l'architecture, ou ne rien implémenter si tu juges que les failles ne sont pas critiques. Tu connais ton sub-agent mieux que moi.

---

## 7. Questions ouvertes (auxquelles je n'ai pas la réponse)

1. **Le styliste tourne en variantes A/B/C** (calque palette). Faut-il un gate par variante ou un gate global ? Probablement par variante (cf. palette).
2. **Le bloc "Garde-fous anti-slop activés" est censé propager au pitch designer** : est-ce que cette propagation fonctionne aujourd'hui ? Ou bien est-ce que le pitch designer ignore ce bloc en pratique ?
3. **La Partie C du catalogue** est-elle à jour avec tous les marqueurs slop documentés ailleurs (perplexity-styles-datés, anti-slop-blacklist-core) ? Si non, doublon possible.
4. **Le tag `[SLOP_RISQUE]` transposé au styliste** — pertinent ou usine à gaz ?

---

## Dernière mise à jour

2026-04-28 — Rédigé par la session ayant complété les chantiers 1 (routeur) et 2 (palette + patches). Source de l'analyse re-challengée : `ref/analyse-anti-slop-3b-style-visual-pitch-2026-04-28.md`.
