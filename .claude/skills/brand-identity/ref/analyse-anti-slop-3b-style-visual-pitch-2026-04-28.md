# Analyse anti-slop — carrefours 3B restants après fonts (2026-04-28)

> Analyse re-challengée par la session qui a complété les chantiers 1 (routeur)
> et 2 (palette + patches) du chantier anti-slop 3B. À utiliser quand on
> attaquera les carrefours suivants. **Ne couvre PAS les fonts** (chantier 3
> en cours dans une autre session — voir `ref/plan-master-chantier-3-fonts-2026-04-28.md`).

> **Carrefours analysés ici** : direction visuelle (3B-5), styles (3B-7a),
> pitch designer (3B Interaction 3). Cette analyse est destinée à servir de
> base à 3 chantiers ultérieurs.

---

## Méthodologie partagée

Pour chaque carrefour, on applique la même méthode validée sur les chantiers 1+2 :

1. **Audit du prompt actuel** : ce qui existe déjà, ce qui manque
2. **Mapping N1/N2/N3** : N1/N2 dans prompt (principes/patterns), N3 dans gate Python (listes nominales)
3. **Architecture** : prompt enrichi + gate Python + intégration SKILL.md (FAIL → resume sub-agent, max 2 itérations)
4. **Tests sur sortie existante** + comparaison avant/après
5. **Patches post-test** (anticipés — cf. patches WCAG mode-aware + LCH distance sur palette)

---

## Carrefour 1 — Direction visuelle (3B-5)

### Ce que cette étape fait

Le sub-agent "penseur visuel" reçoit le concept narratif validé + la palette + les fonts. Il prescrit pour 3 images-clés de la marque : type de visuel (photo macro, illustration painterly, 3D, abstrait…), sujet, cadrage, lumière, matière, ancre stylistique commune. Output : `{brand}-visual-direction-c{N}.md`. C'est le brief créatif des images de la marque.

### Ce qui existe déjà

- Principe **soustractif** (1 sujet, 1 source de lumière, rien d'autre)
- Test **anti-stock** dans la gate qualité par défaut
- **Densité matière vs espace négatif** intentionnel (interdit le "vide subi")
- **Ancre stylistique** (cohérence inter-images : registre, lumière, grain, abstraction, bords)
- **Concrétude** des prescriptions (format prompt MJ/Recraft, pas narration abstraite)

### Lacunes (ce qui laisse passer du slop aujourd'hui)

| Lacune | Pourquoi c'est problématique |
|---|---|
| **Aucun gate Python** sur la sortie | L'auto-évaluation ✓/✗ est faite par le sub-agent lui-même. Vu en palette : les sub-agents trichent sans le savoir |
| **Aucune blacklist de sujets stock explicite** | "Mains sur clavier", "équipe diverse souriante en réunion", "personne en costume regardant un tableau", "lampe Edison filaments", "cybertunnel grid" — sujets slop AI 2018-2024 reconnaissables. Test anti-stock subjectif laisse passer s'ils sont déguisés |
| **Aucune blacklist de matières clichées** | "Marbre veiné" (luxe SaaS), "béton rugueux" (architecte 2020), "velours froissé" (premium 2019), "liquid metal chrome" (Y2K return), "alcohol ink fluide" (boudoir 2022) — tells AI |
| **Aucune blacklist de signatures temporelles datées** | "Aurora gradient mesh 3 blobs" (cliché AI 2023), "light shaft / rayons divins" (cinéma 2015-2020), "filament bokeh chaud orangé" (stock 2010s), "3D clay/blob plastic" (Aurora UI 2022) |
| **Pas de check de diversité inter-images** | Le prompt dit "sujets différents", pas vérifié. Le sub-agent peut prescrire 3 variations du même sujet (3 lignes lumineuses, 3 textures similaires) — faux drama |
| **Pas de check de cohérence avec la palette validée** | Le prompt dit "2-3 hex de la palette doivent dominer", pas vérifié. Le penseur peut prescrire un visuel qui demande des couleurs hors palette |
| **Pas de propagation tag `[SLOP_RISQUE]`** | Si la palette utilise une gamme `[SLOP_RISQUE]`, le visuel qui dominerait cette gamme amplifie le risque. Le penseur visuel ne le sait pas |

### Architecture proposée

| Niveau | Quoi | Où |
|---|---|---|
| **N1** (déjà présent) | Principe soustractif (1 sujet, 1 lumière) | Prompt OK |
| **N2** (à ajouter) | "Pas de Aurora 3 blobs", "Pas de Y2K chrome", "Pas de mains sur clavier" — patterns nommés | Prompt à enrichir |
| **N3** | Liste nominale sujets stock + matières clichées + signatures datées | Gate Python |
| **Calcul** | Diversité inter-images, cohérence palette validée | Gate Python |

**Gate Python `phase3b-visual-anti-slop.py`** — vérifications :
- Sujets bannis (regex blacklist)
- Matières clichées (regex blacklist)
- Signatures datées (regex blacklist)
- Diversité inter-images (heuristique mots clés sujets)
- Présence des dimensions ancre stylistique
- Cohérence palette (hex prescrits ⊂ palette validée)

### Priorité re-challengée

Mon audit initial : 5e (optionnel). **Re-challenge : 3e (impact slop élevé)**.
Raison : le visuel est le slop le plus VISIBLE pour l'utilisateur final (image hero "mains sur clavier" = marque cheap). Le code est simple (grep listes). Trou de couverture le plus large car auto-évaluation actuelle.

---

## Carrefour 2 — Styles (3B-7a)

### Ce que cette étape fait

Le sub-agent "styliste" reçoit le concept narratif validé + palette + fonts. Il choisit UN style officiel (ou mix de 2 max) parmi un catalogue de 34 styles documentés (`ref/styles-bibliotheque.md`). Output : `{brand}-style-choice-c{N}.md` avec scan exhaustif 01-34, longlist 6-8, arbitrage final, signatures à incarner, INTERDITS actifs, garde-fous anti-slop activés, Avis du DA. C'est l'étape qui dit "on va faire du Editorial Grid avec une touche de Anti-AI Crafting".

### Ce qui existe déjà

Le prompt du styliste est **probablement le plus mature** du pipeline :
- Interdiction Partie B (10 styles datés/cycliques en déclin)
- Interdiction "matière BIG" inventée (anciens registres BIG type "Editorial Photographique Monographique")
- Mix max 2 styles (pas 3+)
- Scan exhaustif 01-34 obligatoire (binaire COMPATIBLE/INCOMPATIBLE)
- Longlist 6-8 + test de spécificité
- Étape 5 "Vérification anti-slop finale" + bloc "Garde-fous anti-slop activés"
- Anti-confabulation
- Calibrage par curseur A

### Lacunes

| Lacune | Pourquoi c'est problématique |
|---|---|
| **Scan 01-34 pas vérifié mécaniquement** | Le LLM peut bâcler et n'en scanner que 5-6. Compter les numéros présents révèle le pot aux roses |
| **Style retenu pas vérifié contre liste exacte** | Si le styliste écrit "Editorial Premium" alors que catalogue contient "Editorial Grid #66", c'est une "matière BIG" inventée pas attrapée |
| **Mix max 2 pas compté mécaniquement** | "Editorial × Brutalism × Anti-AI Crafting" = 3 styles, interdit mais pas vérifié |
| **Bloc "Garde-fous anti-slop activés" pas vérifié présent + ≥3 puces** | Si bâclé "Pas de slop" en 1 ligne, ça passe. Or c'est la propagation des garde-fous spécifiques au pitch designer en aval |
| **Marqueurs Partie C dans Signatures à incarner** | Le catalogue documente une Partie C (marqueurs slop transverses : purple/indigo, aurora 3 blobs, Inter mono-font, glow shadow, translateY hover). Le styliste peut copier des signatures qui en contiennent |
| **Justifications longlist génériques** | "Ce style est moderne et épuré" / "convient bien" / "dans l'air du temps" — mêmes patterns qu'en palette |
| **Avis du DA substantiel** | Possible bâclage "Force majeure : OK / Risque : aucun" en 3 lignes vides |

### Architecture proposée

| Niveau | Quoi | Où |
|---|---|---|
| **N1/N2** (déjà présents) | Principes anti-confabulation, anti-générique | Prompt OK |
| **Format** | Scan 01-34 complet, format strict, mix max 2 | Gate Python |
| **N3** | Liste matière BIG inventée, marqueurs Partie C, génériques | Gate Python |

**Gate Python `phase3b-style-anti-slop.py`** — vérifications :
- Scan 01-34 complet (compte numéros)
- Style retenu dans liste catalogue (extraction des 34 noms officiels)
- Mix max 2 styles (compte modulateurs / "×")
- Bloc "Garde-fous anti-slop activés" présent + ≥3 puces non génériques
- Grep "matière BIG" inventée (blacklist anciens registres)
- Grep marqueurs Partie C dans Signatures (purple/indigo, etc.)
- Section "Avis du DA" présente avec 3 axes (Force majeure / Risque / ZAG) substantiels
- Justifications longlist non génériques (réutiliser pattern routeur/palette)

### Priorité re-challengée

Mon audit initial : 3e (mature donc plus simple). **Re-challenge : 4e (mature mais à formaliser)**.
Raison : la maturité textuelle ne suffit pas. On l'a vu en palette où le format strict 7 rôles était dans le prompt mais violé 7/9 fois sans gate. Sans gate Python, les sub-agents bâclent. ~6-8 checks structurels possibles.

---

## Carrefour 3 — Pitch designer complet (3B Interaction 3)

### Ce que cette étape fait

Le pitch est **le document final de la phase 3** qui condense tout : concept narratif + palette validée + fonts validées + style validé + direction visuelle + philosophie d'interaction + données métier + bénéfices business. Output : `{brand}-pitch-c{N}.md`. C'est ce qui est donné au designer Phase 4 pour fabriquer le HTML final.

C'est le **point de convergence** de toutes les décisions amont. Si le slop arrive jusqu'ici, il contamine le HTML produit en Phase 4.

8 sections obligatoires (Ancrage Brief, Intention créative, Direction visuelle, Carte d'Inspiration, Visuels recommandés, Graine Logo, Bénéfices business, Avis du DA).

### Ce qui existe déjà

Le pitch a déjà BEAUCOUP de protections explicites :
- **Règle Cardinale ZÉRO CSS** (gate Python existant `phase3b-css-gate.py` mécanique)
- 9 compositions interdites explicites (50/50 hero, grid 3 cards identiques, 3 features icon+title+desc, footer 4 colonnes, carousels, pricing centré highlighté, process steps numérotés, device frames, alternance texte/image)
- Anti-hover qui monte (interdit "carte se soulève au survol", quel que soit le curseur)
- Diversité atmosphérique inter-concepts (≥1/3 non-sombre)
- Données métier liées au DOMAINE (pas KPI SaaS pour artisan)
- Anti-confabulation Carte d'Inspiration
- Calibrage par curseur A détaillé
- Voisinage marques : avertissement "usual suspects" Aesop / Apple / Bloomberg / Dieter Rams

### Lacunes

| Lacune | Pourquoi c'est problématique |
|---|---|
| **Aucun gate filler words AI** | "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve", "Revolutionize" — mots clichés AI les plus reconnaissables. Sub-agent les utilise sans s'en rendre compte. Grep trivial |
| **Aucun gate fake names** | "John Doe", "Jane Doe", "Acme", "Nexus", "SmartFlow", "Flowbit", "Quantumly", "NovaCore" — placeholders LLM par défaut. Grep trivial |
| **Compositions interdites prescrites en Voice Block / Artefact** | Le prompt liste 9 compositions interdites, rien ne vérifie que le sub-agent ne les prescrit pas. "Voice Block = grid 3 cards identiques" passe sans flag |
| **"Cards" prescrites comme artefact** | Mémoire utilisateur explicite : "artefacts exotiques uniquement (data table, schedule grid), JAMAIS KPI cards / stat grids". Le pitch peut prescrire artefact = card |
| **Voisinage marques surfait** | Aesop / Apple / Bloomberg / Dieter Rams = usual suspects à éviter (mémoire utilisateur). Grep blacklist |
| **Cohérence avec carrefours amont** | Le pitch peut citer hex hors palette validée, fonts hors `font-backups`, style ≠ style choisi en 3B-7a. Aucune vérif. Dérive amont/aval qui casse le système |
| **Diversité atmosphérique inter-concepts** | Règle "≥1/3 non-sombre" sur 3 pitchs. Si tous SOMBRE, pas attrapé. Vérification possible en parsant les 3 pitchs ensemble |
| **Justifications génériques Pont Brief→Créa** | Mêmes patterns que palette/styliste. "On utilise du vert parce que c'est organique" sans citer brief. Grep réutilisable |
| **Avis du DA substantiel** | Bâclage "Force majeure : OK / Risque : aucun" en 2 lignes. Vérif longueur min + non-générique |
| **Anti-hover qui monte vocabulairement** | La règle ZÉRO CSS empêche les termes techniques, mais "la carte se soulève légèrement au survol" en français passe. Grep sémantique sur "se soulève", "monte au survol", "lift on hover", "remonte au passage" |
| **Données métier ≥ 3 chiffres concrets** | Si pitch en a 0 ou 1, le designer Phase 4 ne peut pas remplir l'artefact témoin. Comptage trivial |

### Architecture proposée

Le pitch est **le carrefour le plus RICHE** en règles applicables. Tous types de slop convergent : verbal, compositionnel, sectoriel, diversité, confabulation, voisinage, cohérence amont, justification.

**Gate Python `phase3b-pitch-anti-slop.py`** (~12-15 checks, complémente `phase3b-css-gate.py` existant) :
- Filler words AI (R-117)
- Fake names (R-115)
- Compositions interdites prescrites en Voice Block / Artefact
- Cards comme artefact (mémoire utilisateur)
- Voisinage marques surfait (usual suspects)
- Cohérence amont : hex de la palette validée, fonts du `font-backups`, style du `style-choice`
- Diversité atmosphérique inter-concepts (sur les 3 pitchs combinés)
- Justifications génériques dans Pont Brief→Créa
- Avis du DA substantiel
- Anti-hover qui monte (vocabulaire)
- Format strict (8 sections présentes)
- Données métier ≥ 3 chiffres concrets

### Priorité re-challengée

Mon audit initial : 4e (gros volume). **Re-challenge : 5e (gros volume + point de convergence)**.
Raison : ~12-15 checks (vs 9-10 palette). Mais traiter en dernier parce que le pitch consomme les sorties des autres carrefours — bénéficie de la propagation des garde-fous amont (style, visuel) qui auront été nettoyés avant.

---

## Ordre recommandé révisé pour la suite

| # | Carrefour | Statut |
|---|---|---|
| 1 | Routeur chromatique (3B-0a) | ✅ FAIT (commit `ecc3d11`) |
| 2 | Palette (3B-3) | ✅ FAIT + patches (à committer) |
| 3 | **Fonts (3B-1/3B-2)** | ⏳ EN COURS (autre session) |
| 4 | **Styles (3B-7a)** | À FAIRE — gate Python ciblé sur vérifications structurelles |
| 5 | **Direction visuelle (3B-5)** | À FAIRE — impact slop élevé, code simple (grep listes) |
| 6 | **Pitch designer (3B Interaction 3)** | À FAIRE — point de convergence, plus gros volume |

Cet ordre place les "petits gates structurels" (styles, direction visuelle) avant le "gros gate de convergence" (pitch). Quand on attaquera le pitch, les sorties des carrefours amont seront déjà nettoyées, donc le check de cohérence amont sera plus simple.

---

## Références sources pour ces 3 carrefours

### Pour direction visuelle (3B-5)
- `phases/phase-3b-penseur-visuel.md` — prompt actuel
- `ref/visual-direction-guide.md` — principes de composition, registres émotionnels, usage→prompting
- `ref/perplexity-styles-datés-vs-actuels-2026.md` — marqueurs visuels datés (Aurora 3 blobs, Y2K chrome, etc.)
- `audit-slop/sources/taste-skill/images-taste-skill.md` — section 26 ANTI-AI-SLOP RULES sur images
- Sessions de test : `outputs/test-camille-test-20260415-1733/` (anciennes), `outputs/test-camille-test-20260427-1545/` (récente)

### Pour styles (3B-7a)
- `phases/phase-3b-styliste.md` — prompt actuel
- `ref/styles-bibliotheque.md` — catalogue 34 styles (Partie A) + 10 datés (Partie B) + marqueurs slop transverses (Partie C)
- `ref/style-matching-rules.md` — 5 règles matching + 2 règles pairing
- `ref/styles-matching-protocol.md` — protocole 5 étapes + format fiche
- `phases/phase-3b-specimen-stylise.md` — pour comprendre comment le style se transmet en aval (3B-7b)

### Pour pitch designer (3B Interaction 3)
- `phases/phase-3b-design.md` — prompt actuel
- `scripts/phase3b-css-gate.py` — gate existant ZÉRO CSS (pattern à imiter / complémenter)
- `ref/persona-and-rules.md` — persona DA + règles
- `ref/bible-design-strategie.md` — bible
- `ref/master-style-guide.md` — guide style principal
- `ref/exclusion-metaphores-rex.md` — REX métaphores hors-sujet
- `ref/output-framework-zone1.md`, `zone2.md` — frameworks output
- Mémoire utilisateur : feedbacks (no_copyable_cards, etc.)

### Architecture déjà validée (chantiers 1+2)
- `ref/passation-anti-slop-pour-3b.md` — passation Vague 2 sur Phase 4
- `ref/passation-anti-slop-fonts-2026-04-28.md` — passation chantier 3 fonts (méthodologie consolidée applicable)
- `ref/anti-slop-formulation-guide.md` — convention 3 niveaux N1/N2/N3
- `scripts/phase3b-gamut-router-anti-slop.py` — pattern référence (9 checks, mode --json-output, tag cumulable)
- `scripts/phase3b-palette-anti-slop.py` — pattern référence (10 checks, conversions OKLCH/WCAG standalone, patches mode-aware/distance LCH)

---

## Dernière mise à jour

2026-04-28 — Rédaction par la session ayant complété les chantiers 1 (routeur) et 2 (palette). Ce document constitue la **base de cadrage pour les 3 chantiers suivants** après les fonts.
