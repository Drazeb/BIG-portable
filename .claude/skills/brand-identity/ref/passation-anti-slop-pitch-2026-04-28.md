# Passation — Chantier anti-slop Phase 3B, carrefour 6 : pitch designer (3B Interaction 3)

> **Lecture obligatoire avant tout travail sur le pitch designer.** Ce document
> contient le contexte complet du chantier anti-slop appliqué à BIG, ce qui a
> été fait sur les carrefours précédents, les méthodes validées, les pièges, et
> toutes les références sources.
>
> Le pitch est **le carrefour le plus RICHE en règles applicables** —
> tous les types de slop convergent ici. C'est aussi le **point de convergence**
> des sorties amont (palette / fonts / style / direction visuelle) — donc
> traiter en dernier permet de bénéficier des nettoyages amont.

---

## 0. TL;DR

- BIG produit des identités de marque. Vague 2 a équipé la Phase 4 (style-tiles HTML) avec ~120 règles anti-slop. Cf. `ref/passation-anti-slop-pour-3b.md`.
- En avril 2026, on étend l'architecture aux étapes **3B** (qui FIXENT les choix consommés par Phase 4 : palette, fonts, style, pitch).
- **Carrefours déjà traités** : routeur chromatique (chantier 1, commit `ecc3d11`), palette (chantier 2, à committer).
- **Carrefours en cours / à venir** : fonts (chantier 3, autre session), styliste (chantier 4, document d'onboarding `ref/onboarding-anti-slop-pour-styliste-2026-04-28.md`), direction visuelle (chantier 5), **pitch (chantier 6 — TOI)**.
- Méthodologie validée : stratégie 3-niveaux N1/N2/N3 + pattern "amont prompt + aval gate Python" + tests sur cas réels + patches post-test.
- Le pitch est **le plus riche en checks possibles** (~12-15) parce qu'il condense tout. **C'est aussi le dernier maillon avant Phase 4** — ce qui passe ici contamine le HTML final.

---

## 1. Contexte global du chantier anti-slop dans BIG

### 1.1 Le problème

Les LLM produisent par défaut des outputs avec des **marqueurs slop AI** : patterns visuels datés, fonts surutilisées, hex Tailwind par défaut, justifications creuses, format chaotique. Sans intervention, le pipeline BIG hérite de ces biais à chaque sub-agent.

### 1.2 La grille audit-slop (référentiel canonique)

Skill `/audit-slop` (`.claude/skills/audit-slop/`) audite un style-tile HTML sur **4 grilles indépendantes** + synthétiseur :
- **Craft Moderne** : Impeccable + Taste Skill (7 variantes) + GStack — 19 fichiers, ~130 règles
- **Vercel Technique** : `vercel-command.md` — ~60 règles
- **BIG Pipeline** : 10 fichiers BIG + 2 gates Python — ~80 règles
- **Perplexity Temporel** : rapport classification 85 styles + marqueurs datés

Total ~212 règles brutes, ~158 universelles.

### 1.3 Vague 2 sur Phase 4 (déjà fait — référentiel d'architecture)

Cf. `ref/passation-anti-slop-pour-3b.md`. Architecture stratifiée :
- **TIER 1** : ~28 règles structurantes injectées dans le prompt Designer (limite empirique : ~25-30 max, sinon sur-engineering)
- **Gates Python déterministes** : checks regex mécaniques sur le HTML
- **Critiques sémantiques** : 4 subagents spécialisés (a11y, composition, typo-copy, craft) + 1 Synthétiseur, ~80 règles non-grep-ables

### 1.4 Convention de formulation 3 niveaux (CRITIQUE)

Référence : `ref/anti-slop-formulation-guide.md`. **À lire absolument avant toute modif de prompt.**

| Niveau | Forme | Risque | Verdict |
|---|---|---|---|
| **N1** Principe abstrait | `Do NOT center everything symmetrically` | Aucun | ✅ OK prompt |
| **N2** Pattern nommé non-substituable | `Do NOT use neumorphism` | Aucun | ✅ OK prompt |
| **N3** Énumération précise (fonts/hex/syntax) | `Do NOT use Inter`, `Do NOT use #6366f1` | **CONTAMINATION CRÉATIVE PROUVÉE** | ❌ JAMAIS prompt — gate Python uniquement |

**Stratégie 3 (amont + aval)** : N1/N2 dans prompt + N3 dans gate Python. Validée sur les 2 chantiers déjà faits.

### 1.5 Phase 3B — où on en est

| Sous-étape | Carrefour | Statut |
|---|---|---|
| 3B-0a | Routeur chromatique | ✅ Fait (commit `ecc3d11`) |
| 3B-0b | Sélection inspiration esthétique | (touché incidemment) |
| 3B-1 | Penseurs typographiques | ⏳ Chantier 3 (autre session) |
| 3B-2 | Designer visuel (planches duos) | ⏳ Chantier 3 (autre session) |
| 3B-3 | Palette (variantes A/B/C) | ✅ Fait (à committer) |
| 3B-5 | Penseur visuel (direction iconographique) | À faire (chantier 5) |
| 3B-7a | Styliste | À faire (chantier 4 — onboarding fait) |
| 3B-7b | Spécimen stylisé | (carrefour ultérieur) |
| **3B Interaction 3** | **Pitch designer complet** | **⏳ TOI (chantier 6)** |

L'ordre chronologique du pipeline pose le pitch **en dernier** — bénéficie de la propagation des nettoyages amont.

---

## 2. Méthodologie consolidée (à reproduire pour le pitch)

### 2.1 Pattern d'intégration en 5 étapes

1. **Audit du prompt actuel** (`phase-3b-design.md`) : ce qui existe déjà comme règles, ce qui manque
2. **Mapping N1/N2/N3** : pour chaque règle audit-slop applicable, décider si elle va dans le prompt (N1/N2) ou dans le gate Python (N3)
3. **Modifications prompt** : ajouter un bloc "## RÈGLES ANTI-SLOP (universelles)" dans le prompt pitch designer, AVANT le format de sortie
4. **Création gate Python** : `scripts/phase3b-pitch-anti-slop.py` avec ~12-15 checks (le pitch est le plus riche), mode `--json-output`, exit codes 0/1/2
5. **Modification SKILL.md** : ajouter l'invocation du gate après la production du pitch (Interaction 3 du designer), avant l'assemblage final `{brand}-pitch.md`. Pattern : si FAIL → resume du designer (Task fresh, anti-dégradation, prompt relu disque) avec violations en feedback. Max 2 itérations.

### 2.2 Gate existant à articuler

**`scripts/phase3b-css-gate.py`** existe déjà — il vérifie "ZÉRO CSS dans le pitch" (la Règle Cardinale du prompt). C'est une mission unique et claire.

**Recommandation** (à challenger) : créer un gate dédié `phase3b-pitch-anti-slop.py` qui complémente le CSS gate. Les deux s'enchaînent dans le pipeline. Cohérent avec l'architecture "un gate par carrefour, un gate = une responsabilité".

Alternative : étendre le CSS gate. Mais ça brouille les responsabilités (CSS gate fait du grep simple, pitch anti-slop fera des checks plus complexes).

### 2.3 Tests obligatoires

- **Test sur pitch existant** : trouver un `{brand}-pitch-c{N}.md` réel (cf. sessions Camille / VoltaPilot récentes), lancer le gate dessus, vérifier qu'il détecte des violations cohérentes
- **Test E2E** : cloner une session de test qui a déjà tous les amont validés (palette, fonts, style choisi), lancer le pipeline depuis l'Interaction 3 du designer
- **Comparaison avant/après** : compter les violations sur l'ancien (sans règles) vs nouveau (avec règles) — quantifier le gain

### 2.4 Patches post-test (anticipés)

Sur les 2 chantiers précédents, on a observé que les premiers checks sont souvent trop stricts. Pattern de réaction validé :
- Identifier le faux positif (cas légitime que le gate refuse à tort)
- Comprendre la cause structurelle
- Patcher : assouplir le seuil, ajouter une dépendance contextuelle (ex: lire un mode dominant), passer à une métrique plus riche
- Re-tester pour vérifier qu'on garde le gain anti-slop

Exemples de patches sur palette :
- WCAG mode-aware (lit le mode dominant pour ne vérifier que les paires utilisées)
- Distance LCH complète pour accent (chroma + hue, pas juste chroma)

À anticiper sur le pitch : peut-être un seuil "longueur min de l'Avis du DA" trop strict, ou une blacklist filler words trop large.

---

## 3. Ce qui a été fait avant toi (chantiers 1+2 en synthèse)

### Chantier 1 — Routeur chromatique (3B-0a)

- Prompt enrichi : 4 règles N1/N2 (zone violet/indigo qualifiée, neutres orientés, spécificité, pas de doublons)
- Gate Python : 9 checks, mode `--json-output`
- **Innovation : tag `[SLOP_RISQUE]` cumulable** (calque de `[SECTORIEL]` existant) — autorise une gamme à risque MAIS la signale en aval. Pattern de propagation : la palette en aval reçoit le tag et applique une vigilance accrue
- Pattern PASS_WITH_PATCH : si l'oubli est trivial (tag absent mais qualification OK), l'orchestrateur patche silencieusement

Fichiers : `phases/phase-3b-gamut-router.md`, `scripts/phase3b-gamut-router-anti-slop.py`, `lib/gamut-visual.mjs` (badges cumulables), `SKILL.md` zone 3B-0a.

### Chantier 2 — Palette (3B-3)

- Prompt enrichi : 5 règles N1/N2
- Gate Python : 10 checks (format strict, hex valides, rôles inventés, pur noir/blanc, hex AI Tailwind + zone LCH, neutres tintés, saturation aux extrêmes, WCAG mode-aware, accent distinct par distance LCH, justifications)
- Conversion OKLCH/WCAG standalone (sans dépendance externe Python)
- 2 patches post-test : WCAG mode-aware + distance LCH pour accent

### Métriques validation chantier 2 (Camille)

Sur 9 palettes équivalentes (3 concepts × 3 variantes A/B/C) :
- Avant règles : 51 violations totales, 0/9 PASS
- Après règles + patches : 0 violations, 9/9 PASS clean au premier coup
- Drama chromatique préservé (Bg dark presque-noirs profonds OK)

Réduction du slop ~98%.

### Limites reconnues (à connaître)

1. **Trou de couverture "accent dans gamme exclue"** : si le routeur exclut une gamme (ex: cyans turquoise pour Camille, ventre mou tech/wellness) mais la palette met cet accent quand même (règle "accent libre"), pas de flag. Cas observé sur Foyer Parabolique C avec Accent cyan.
2. **Bug pipeline température** : la prescription "Température chaude" du scoping (Phase 2A) n'est pas remontée au routeur. Charles a décidé "vivre avec".
3. **Divergence A/B/C plus subtile qu'avant** : en forçant le respect des règles, on élimine les anciennes "divergences à coup de slop". Pour récupérer plus de divergence, enrichir le prompt de divergence B/C lui-même, pas relâcher le gate.

Ces 3 limites NE concernent PAS directement le pitch. À noter pour culture.

---

## 4. Le carrefour pitch — ce que tu dois faire

### 4.1 Ce que le pitch fait

Le pitch est **le document final de la phase 3** qui condense TOUT :
- Concept narratif (Phase 3A)
- Palette validée (3B-3)
- Fonts validées (3B-1/3B-2)
- Style officiel validé (3B-7a)
- Direction visuelle (3B-5)
- Philosophie d'interaction
- Données métier
- Bénéfices business

Output : `{brand}-pitch-c{N}.md` (par concept N=1,2,3) + assemblage final `{brand}-pitch.md`. C'est ce qui est donné au designer Phase 4 pour fabriquer le HTML final.

**Format** : 8 sections obligatoires
1. Ancrage Brief (Tension résolue + Pont Brief→Créa + ICP)
2. Intention créative
3. Direction visuelle (typo, palette, surface, atmosphère, type-scale, données métier, philosophie d'interaction, prescriptions d'exécution visuelle, registre atmosphérique)
4. Carte d'Inspiration (territoire visuel, secteurs proches, anti-territoire, voisinage marques)
5. Visuels recommandés (résumé du penseur visuel)
6. Graine Logo
7. Bénéfices business
8. Avis du DA (Force majeure / Risque potentiel / Position ZAG)

### 4.2 Ce qui existe déjà comme protections (et qui marche)

- **Règle Cardinale ZÉRO CSS** : interdit les termes techniques (clip-path, backdrop-filter, cubic-bezier, hex précis…). Gate Python existant `phase3b-css-gate.py` qui vérifie mécaniquement
- **9 compositions interdites** explicites (50/50 hero rigide, grid 3 cards identiques, 3 features icon+title+desc, footer 4 colonnes, carousels, pricing centré highlighté, process steps numérotés, device frames, alternance texte/image)
- **Anti-hover qui monte** : interdit la "carte qui se soulève au survol", quel que soit le curseur
- **Diversité atmosphérique inter-concepts** : sur 3 pitchs, au moins 1 doit être non-sombre
- **Données métier liées au DOMAINE** : pas KPI SaaS génériques pour un artisan
- **Anti-confabulation Carte d'Inspiration** : ne pas inventer "wabi-sabi japonais" si choix n'ont rien de wabi-sabi
- **Calibrage par curseur A** détaillé
- **Voisinage de marques** : avertissement à ne pas surreprésenter Aesop / Apple / Bloomberg / Dieter Rams (les "usual suspects")
- **Format strict** des 8 sections

C'est le prompt **avec le plus de protections textuelles explicites** du pipeline. Mais textuel ne signifie pas mécaniquement vérifié.

### 4.3 Mes impressions sur les failles potentielles (à re-challenger)

> **Important** : ces points sont mes observations depuis l'extérieur. Charles m'a explicitement demandé de **ne pas dégrossir le travail d'analyse** — il veut que tu re-challenges ça avec un esprit frais. Donc considère ce qui suit comme **un référentiel de zones suspectes**, pas comme un plan d'attaque. Tu peux infirmer / nuancer / ajouter.

Failles potentielles que j'ai pré-identifiées (sans approfondir) :

| Zone suspecte | Pourquoi je la flag |
|---|---|
| Filler words AI | "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve", "Revolutionize" — clichés AI les plus reconnaissables. Aucun gate aujourd'hui. Grep trivial à coder |
| Fake names | "John Doe", "Jane Doe", "Acme", "Nexus", "SmartFlow", "Flowbit", "Quantumly", "NovaCore" — placeholders LLM par défaut. Aucun gate. Grep trivial |
| Compositions interdites prescrites | Le prompt liste 9 compositions interdites mais ne vérifie pas que le sub-agent ne les prescrit pas dans Voice Block ou Artefact. "Voice Block = grid 3 cards identiques" passe sans flag |
| "Cards" prescrites comme artefact | Mémoire utilisateur explicite : "artefacts exotiques uniquement (data table, schedule grid), JAMAIS KPI cards / stat grids". Le pitch peut prescrire "artefact = card avec 3 KPI" |
| Voisinage marques surfait | Aesop / Apple / Bloomberg / Dieter Rams = usual suspects à éviter (mémoire utilisateur). Grep blacklist |
| Cohérence avec carrefours amont | Le pitch peut citer hex hors palette validée, fonts hors `font-backups`, style ≠ choix 3B-7a. Aucune vérif. **Dérive amont/aval qui peut casser tout le système** |
| Diversité atmosphérique inter-concepts | Règle "≥1/3 non-sombre" sur 3 pitchs. Si tous sombre, pas attrapé. Vérif possible en parsant les 3 pitchs ensemble |
| Justifications génériques Pont Brief→Créa | Mêmes patterns que palette/styliste. "On utilise du vert parce que c'est organique" sans citer brief. Pattern réutilisable |
| Avis du DA bâclable | "Force majeure : OK / Risque : aucun" en 2 lignes. Vérif longueur min + non-générique |
| Anti-hover qui monte vocabulairement | Règle ZÉRO CSS empêche les termes techniques, mais "la carte se soulève légèrement au survol" en français passe. Grep sémantique sur "se soulève", "monte au survol", "lift on hover", "remonte au passage" |
| Données métier ≥ 3 chiffres | Le prompt dit "3-5 chiffres / métriques / statuts". Si le pitch en a 0 ou 1, le designer Phase 4 ne peut pas remplir l'artefact témoin. Comptage trivial |

**Ce que je n'ai pas approfondi (et que tu peux explorer)** :

- L'articulation **précise** entre `phase3b-css-gate.py` existant et un futur `phase3b-pitch-anti-slop.py` (étendre vs séparer)
- La **propagation des garde-fous spécifiques au style** (le bloc "Garde-fous anti-slop activés" produit par le styliste — est-ce que le pitch les respecte vraiment ? comment le vérifier ?)
- La **propagation du tag `[SLOP_RISQUE]`** des palettes vers le pitch (s'il existe, quels checks supplémentaires ?)
- Les **règles spécifiques aux sections du pitch** que je n'ai pas catégorisées
- Le **format du pitch assemblé final** (`{brand}-pitch.md` qui concatène les 3 pitchs c1+c2+c3) — vérifier sur l'assemblage ou sur chaque pitch individuel ?
- Les **REX historiques** sur le pitch que j'ai juste survolés (`exclusion-metaphores-rex.md` — métaphores hors-sujet)
- Les **règles sectorielles** (Ventre Mou) qui doivent être respectées dans le pitch — comment le vérifier ?

---

## 5. Références exhaustives

### À lire en priorité (~1h)

| Fichier | Pourquoi |
|---|---|
| `ref/passation-anti-slop-pour-3b.md` | Contexte Vague 2 sur Phase 4 — leçons d'architecture détaillées |
| `ref/anti-slop-formulation-guide.md` | **CRITIQUE** — convention 3 niveaux N1/N2/N3 |
| `ref/extraction-vague2-2026-04-26.md` | Extraction des 182 règles audit-slop avec destination |
| `ref/analyse-anti-slop-3b-style-visual-pitch-2026-04-28.md` | Analyse re-challengée des 3 carrefours restants — section dédiée pitch (la plus complète) |
| `ref/passation-anti-slop-fonts-2026-04-28.md` | Passation du chantier fonts — pattern méthodologique reproduit ici |

### Fichiers du carrefour pitch

| Fichier | Rôle |
|---|---|
| `phases/phase-3b-design.md` | **Le prompt actuel du pitch designer** — long, ~370 lignes |
| `scripts/phase3b-css-gate.py` | Gate existant ZÉRO CSS (pattern à imiter / complémenter) |
| `SKILL.md` zone 3B (Interaction 3) | Orchestration actuelle du pitch |
| `SKILL.md` Étape 3B-bis | Validation visuelle typo + palette via specimen PNG |
| `ref/persona-and-rules.md` | Persona DA + 4 règles d'or |
| `ref/bible-design-strategie.md` | Bible design (5 principes branding + ZAG + Tension + Ventre Mou + double curseur A×B) |
| `ref/master-style-guide.md` | Guide style principal |
| `ref/output-framework-zone1.md` | Framework output Zone 1 (core identity) |
| `ref/output-framework-zone2.md` | Framework output Zone 2 (extensions) |
| `ref/exclusion-metaphores-rex.md` | REX métaphores hors-sujet |
| `ref/interface-design-lens.md` | Vocabulaire compositions et atmosphères |

### Patterns architecturaux (chantiers 1+2 — pour copier la méthode)

| Fichier | Rôle |
|---|---|
| `scripts/phase3b-gamut-router-anti-slop.py` | Pattern gate (9 checks, tag cumulable, JSON output) |
| `scripts/phase3b-palette-anti-slop.py` | Pattern gate (10 checks, OKLCH/WCAG standalone, patches mode-aware) |
| `phases/phase-3b-gamut-router.md` (modifié) | Bloc "RÈGLES ANTI-SLOP" en N1/N2 — exemple |
| `phases/phase-3b-palette.md` (modifié) | Bloc "RÈGLES ANTI-SLOP" en N1/N2 — exemple |
| `SKILL.md` zone 3B-0a + zone 3B-3 (Vague 2bis) | Patterns d'intégration gate |

### Skill audit-slop (matière originelle)

| Chemin | Rôle |
|---|---|
| `audit-slop/SKILL.md` | Architecture (4 grilles + synthétiseur) |
| `audit-slop/agents/big-pipeline.md` | Agent BIG (qui audite les style-tiles vs le pipeline complet — INSTRUCTIF) |
| `audit-slop/sources/impeccable/reference/ux-writing.md` | **CRITIQUE pour pitch** — règles UX writing applicables au pitch (errors, voice/tone, button labels, etc.) |
| `audit-slop/sources/taste-skill/redesign-skill.md` | Audit granulaire par catégorie incluant content/copy |
| `audit-slop/sources/taste-skill/taste-skill.md` | Section 7 AI Tells (filler words, fake names, generic avatars) |
| `audit-slop/sources/gstack/design-review.md` | Checklist 10 catégories incluant Content + AI Slop |
| `audit-slop/sources/gstack/plan-design-review.md` | Hard Rules + AI Slop blacklist 11 items |
| `audit-slop/sources/vercel-command.md` | Section "Content & Copy" |

### Documents BIG anti-slop existants (pour cohérence)

| Fichier | Rôle |
|---|---|
| `ref/anti-slop-blacklist-tier1.md` | TIER 1 anti-slop Phase 4 — compositions à éviter |
| `ref/anti-slop-blacklist-core.md` | Anti-patterns sémantiques (composition, hovers datés, animations infinies, glow shadows…) |
| `ref/finition-elite-tier1.md` | Palette + CSS moderne + neutres tintés + type scale + spacing scale |
| `ref/hierarchie-visuelle-tier1.md` | Restraint + 1 dominant + données/labels + variation densité |
| `ref/typography-core.md` | Pairing fonts, weights, letter-spacing, line-height, OpenType features |
| `ref/ux-writing-core.md` | Boutons, errors, empty states, voice/tone, Title Case |

### Sessions de test pour comparaison

| Session | Brand | Notes |
|---|---|---|
| `outputs/test-camille-test-20260415-1733/` | Camille | Anciennes pitches `{brand}-pitch-c{N}.md` (pré-anti-slop) |
| `outputs/test-camille-test-20260424-1907/` | Camille | Pitches `{brand}-pitch.md` assemblés (récent, partiellement nettoyé) |
| `outputs/test-voltapilot-vague2.5-20260427-*/` | VoltaPilot | Pitches Phase 4 récents |

### Mémoire utilisateur pertinente

Lire `MEMORY.md` index. Particulièrement :
- `feedback_no_copyable_cards_in_examples.md` — artefacts exotiques uniquement, jamais KPI cards/stat grids
- `feedback_no_undiscussed_changes.md` — ne pas ajouter de règles hors périmètre sans validation
- `feedback_step_by_step_testing.md` — une seule modification par test

---

## 6. Méthodologie pas-à-pas

1. **Lire ce document** + `ref/anti-slop-formulation-guide.md` + `ref/passation-anti-slop-pour-3b.md`
2. **Lire le prompt actuel** `phase-3b-design.md` (long mais incontournable)
3. **Lire la section pitch** dans `ref/analyse-anti-slop-3b-style-visual-pitch-2026-04-28.md`
4. **Lire les règles UX writing** : `audit-slop/sources/impeccable/reference/ux-writing.md`
5. **Faire ton propre audit** + cartographie + proposition d'architecture à Charles
6. **Présenter le plan** et les 5 questions de cadrage (cf. section 8) AVANT d'implémenter
7. **Implémenter** après validation
8. **Tester** sur pitch existant (Camille 15 avril) + comparer avant/après
9. **Patcher** si besoin (anticiper : seuils, faux positifs sur sections optionnelles)
10. **Committer** quand tout est validé

---

## 7. État commit / git au 2026-04-28

- **Chantier 1 routeur** : commit `ecc3d11`
- **Chantier 2 palette + patches** : à committer (vérifier avec `git status`)
- **Chantier 3 fonts** : en cours (autre session) — voir `ref/plan-master-chantier-3-fonts-2026-04-28.md`
- **Chantier 4 styliste** : onboarding fait — voir `ref/onboarding-anti-slop-pour-styliste-2026-04-28.md`
- **Chantier 5 direction visuelle** : non démarré — analyse pré-faite dans `ref/analyse-anti-slop-3b-style-visual-pitch-2026-04-28.md`
- **Chantier 6 pitch** : **TOI**

---

## 8. Questions de cadrage à poser à Charles avant démarrage

Charles préfère un carrefour à la fois et le challenge plutôt que la complaisance. Pose ces questions au début :

1. **Articulation `phase3b-css-gate.py` existant et nouveau gate pitch** : étendre le CSS gate ou créer un gate dédié ?
2. **Test E2E** : sur quel pitch existant (Camille 24 avril ou VoltaPilot récent) ? Cloner et nettoyer comme pour palette ?
3. **Périmètre** : on couvre les 3 pitchs séparément (par concept) ET l'assemblage final, ou seulement par concept ?
4. **Cohérence amont** : on vérifie que les hex / fonts / style cités dans le pitch correspondent aux validations amont, ou on considère que c'est au designer Phase 4 de gérer ?
5. **Décisions de seuil** : Charles arbitre les cas limites observés au test (calque sur palette : observer puis proposer un patch).

---

## 9. Note importante — re-challenge attendu

Charles m'a explicitement dit de ne PAS trop dégrossir l'analyse pour toi. Donc :
- La section 4.3 ci-dessus liste des **zones suspectes** que j'ai repérées
- Mais **tu dois faire ton propre audit avec un esprit frais**
- Tu peux infirmer mes points, ajouter des points que je n'ai pas vus, ou prioriser différemment
- L'idéal est que tu présentes ton propre audit à Charles AVANT d'implémenter, comme on a fait sur les chantiers 1+2

C'est précisément parce que le pitch est le carrefour le plus riche que Charles veut un regard frais.

---

## Dernière mise à jour

2026-04-28 — Rédigé par la session ayant complété les chantiers 1 (routeur) et 2 (palette + patches). Bonne chance pour le chantier 6.
