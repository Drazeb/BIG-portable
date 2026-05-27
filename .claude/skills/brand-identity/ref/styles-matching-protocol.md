# Protocole de matching style — Phase 3B-7a

> **Rôle** : protocole en 5 étapes que le sub-agent styliste suit STRICTEMENT pour choisir UN style officiel reconnu (ou mix dominant×modulateur max) parmi les 34 styles de la Partie A du catalogue `ref/styles-bibliotheque.md`.
>
> **Pattern source** : matching naturel sémantique calqué sur `phases/phase-3b-penseur.md` (penseur typographique). Pas de shuffle, pas de divergence forcée. Scan exhaustif + ranking par pertinence sémantique + justification spécifique.
>
> **Règles appliquées** : `ref/style-matching-rules.md` (5 règles + 2 pairing).

---

## Inputs requis (substitués dans le prompt par l'orchestrateur)

| Variable | Source | Rôle dans le matching |
|---|---|---|
| `{concept_narrative}` | `{brand}-concepts-narratifs.md` | Source PRINCIPALE du matching (registre sensoriel, métaphore, mots-clés) |
| `{territory_mix}` | `{brand}-context-clean.md` (Mix de Territoires décontaminé) | Source COMPLÉMENTAIRE (mots-clés territoriaux) |
| `{cursor_a}` × `{cursor_b}` | `{brand}-scoping.md` | Calibrage intensité/différenciation |
| `{ventre_mou_section}` | `{brand}-scoping.md` | Codes visuels toxiques du secteur — à éviter activement |
| `{palette_summary}` | `{brand}-palette-c{N}.md` | Ingrédient figé (palette validée) — vérification cohérence règle 6 |
| `{display_font}` + `{body_font}` | `{brand}-font-backups.md` | Ingrédients figés (typo validée) — vérification cohérence règles 6-7 |

---

## Étape 1 — Déclaration du TYPE de style recherché (avant tout scan)

**AVANT** de scanner le catalogue, le styliste DÉCLARE le type de style recherché en croisant le concept narratif et les territoires. Cette déclaration ANCRE le matching et empêche le styliste de tomber sur le premier style "qui sonne bien".

Le styliste produit une déclaration structurée :

```markdown
## TYPE de style recherché

**Registre cible** : {Éditorial / Brutaliste / Minimaliste / Cinétique / Organique / Cinématographique / Tech / Crafty} — ou hybride 2 registres si le concept l'appelle clairement.

**Densité visuelle** : {dense / structuré / modéré / épuré / extrême-épuré} — basée sur la règle 1 du matching (densité = poids métaphorique).

**Température** : {chaude / neutre / froide / contrastée chaud-froid} — cohérente avec la palette validée.

**Justification (3-5 phrases)** : pourquoi ce registre + cette densité + cette température, en CITANT explicitement :
- Au moins 1 mot-clé du concept narratif
- Au moins 1 mot-clé du territoire principal
- Le curseur A (intensité du traitement)
- Le curseur B (différenciation vs ventre mou)
```

**Exemple ancré** (concept "rack focus cinématographique" + territoires "précision instrumentale + chaleur analogique" + curseur A=2 + B=2) :

> **Registre cible** : Cinématographique × Éditorial (hybride)
> **Densité visuelle** : modéré (rythme magazine + halos cinematic)
> **Température** : chaude (validée par la palette)
> **Justification** : Le concept "rack focus" évoque un univers de cinéma argentique (registre cinématographique), mais le territoire "précision instrumentale" demande une rigueur de composition (registre éditorial). Le curseur A=2 demande une asymétrie contrôlée (pas du Brutalism A=3, pas du Minimalism Swiss A=1). Le curseur B=2 demande 1 axe de différenciation par rapport au ventre mou consulting (qui tire vers le Tech bleu froid) → s'éloigner via la chaleur analogique.

Cette déclaration est OBLIGATOIRE. Sans elle, le scan exhaustif tombe en bâclage.

---

## Étape 2 — Scan exhaustif `01-N` du catalogue

Le styliste lit `ref/styles-bibliotheque.md` Partie A intégralement (les 34 styles), et pour CHAQUE style, déclare :

```markdown
## Scan exhaustif des 34 styles

01. {Nom du style} — COMPATIBLE / INCOMPATIBLE — {raison courte 1 ligne}
02. {Nom du style} — COMPATIBLE / INCOMPATIBLE — {raison courte 1 ligne}
...
34. {Nom du style} — COMPATIBLE / INCOMPATIBLE — {raison courte 1 ligne}
```

**Règles du scan** :
- **Format binaire strict** : COMPATIBLE ou INCOMPATIBLE. Pas de "peut-être", "à vérifier", "selon le contexte". Si tu hésites → INCOMPATIBLE (le styliste doit prendre position).
- **Raison courte obligatoire** pour chaque INCOMPATIBLE. Pas de silence — la raison doit citer une règle de matching violée (densité, registre sensoriel, palette/fonts incompatibles, etc.) ou un INTERDIT de la fiche du style.
- **Pas de shortlisting prématuré** : tu DOIS scanner les 34 styles, pas t'arrêter après les 6-7 premiers compatibles.
- **Numérotation 01-34** : chiffres explicites, rend tout manquement visible.

Sortie attendue : ~10-15 COMPATIBLES + ~19-24 INCOMPATIBLES avec raisons.

**Anti-bâclage** : si tu sors plus de 25 COMPATIBLES, tu es trop permissif (probablement réflexe sectoriel). Re-scanner avec la règle 3 (justification spécifique).

---

## Étape 3 — Application des 5 règles + longlist ordonnée 6-8

Sur les COMPATIBLES de l'étape 2, le styliste applique les **5 règles de matching** de `ref/style-matching-rules.md` :
1. Densité visuelle = poids métaphorique
2. Registre sensoriel = univers du concept
3. Justification SPÉCIFIQUE (test : s'applique à 5+ autres styles ? → REJET)
4. Pas de matching par mot-clé isolé
5. Feeling global > checklist d'attributs

Et les **2 règles de pairing** :
6. Cohérence système (style + typo + palette = même univers sensoriel)
7. Contraste structurel (style et typo se distinguent sur ≥1 axe)

Le styliste produit une **longlist ordonnée de 6-8 candidats** (rang 1 = meilleur match) :

```markdown
## Longlist ordonnée (6-8 candidats)

1. **{Nom du style retenu}** — {justification spécifique passant les 5 règles, 2-3 phrases}
2. **{Nom du style}** — {justification, 2-3 phrases}
3. **{Nom du style}** — {justification, 2-3 phrases}
...
6 (à 8). **{Nom du style}** — {justification, 2-3 phrases}
```

**Règle de spécificité** (rappel règle 3) : pour chaque candidat, le test "ta justification s'applique à 5+ autres styles ?" doit être négatif. Sinon REJET du candidat (descend en bas du ranking ou disparaît).

**Règle de feeling global** (règle 5) : si 2 candidats ont des justifications proches, départager par l'IMPRESSION GLOBALE (lequel SENT le plus comme le concept).

---

## Étape 4 — Arbitrage final : style pur ou mix dominant × modulateur

Le styliste arbitre entre 2 options à partir de sa longlist :

### Option A — Style pur (1 style retenu)

Le rang 1 de la longlist est nettement meilleur que le rang 2. Critère :
- Le rang 1 incarne PLEINEMENT le concept (toutes les signatures sont au service du concept)
- Le rang 2 et suivants sont des "approximations" — ils captent une partie mais pas tout

**Verdict** : style pur retenu = rang 1.

### Option B — Mix dominant × modulateur (2 styles retenus, max)

Le rang 1 et le rang 2 sont équivalents sur deux dimensions complémentaires (l'un fort sur composition, l'autre fort sur surface ; l'un fort sur ambiance, l'autre fort sur atmosphère ; etc.).

**Conditions strictes** :
- **Compatibilité sémantique** : le rang 1 (dominant) et le rang 2 (modulateur) doivent venir d'un MÊME univers sensoriel (règle 6 — cohérence système) ET se distinguer sur au moins un axe structurel (règle 7 — contraste structurel). Si les deux sont sémantiquement dissonants (registres incompatibles, ex: Cyberpunk UI × Warmth Minimalism) → REJET du mix, retomber sur style pur.
- **Maximum 2 styles** : pas de mix à 3+. Le mix doit être dominant (~70% du rendu) × modulateur (~30%).
- **Le dominant DIRIGE** : composition globale, palette dominante, atmosphère générale.
- **Le modulateur INCRUSTE** : 1-2 signatures secondaires (ex: Vintage Analog modulateur sur Editorial Grid dominant = la grille éditoriale + la matière papier vintage, pas une fusion 50/50).

**Verdict** : mix retenu = rang 1 (dominant) + rang 2 (modulateur).

### Test post-arbitrage

Le styliste répond à la question : *"Si je devais expliquer ce choix à un designer pro qui connaît le catalogue Perplexity, est-ce que je peux nommer le ou les styles SANS hésitation, et est-ce qu'il acquiescerait au lien concept ↔ style ?"*

Si oui → arbitrage validé.
Si non → revenir à l'étape 3, élargir la longlist, ou reconsidérer l'étape 1.

---

## Étape 5 — Vérification anti-slop finale

Avant de finaliser la fiche de style, le styliste vérifie que ses prescriptions concrètes (signatures à incarner) ne contiennent aucun marqueur de la Partie C du catalogue :

- Couleurs/Gradients : pas d'indigo générique, pas d'aurora générique 3 blobs centrés
- Typographie : pas d'Inter mono-font, pas de Roboto/Arial fallback
- Layout : pas de 3-features grid icon+title+desc, pas de mega-footer sitemap, pas de carousel pour du contenu visible
- Effets visuels : pas de glassmorphism `backdrop-blur 20px+ + violet`, pas de subtle shadow `0.1 opacity` systématique, pas de glow shadow `0 0 Npx`
- Comportements : pas de translate Y au hover, pas d'animation infinite décorative, pas de wave/zigzag dividers

Si la fiche du style retenu contient un INTERDIT qui matche un marqueur slop (ex: Editorial Grid avec subtle shadows 0.1 opacity systématique), le styliste DOIT formuler la prescription pour l'EXCLURE explicitement dans son output.

Le résultat de cette vérification est un bloc final dans la fiche de style intitulé **"Garde-fous anti-slop activés"** (3-5 puces de directives spécifiques formulées par le styliste pour le pitch designer en aval).

---

## Format de sortie : la FICHE DE STYLE

Output du styliste = fichier `{brand}-style-choice-c{N}.md` structuré ainsi :

```markdown
# Fiche de style — Concept {N} "{Nom du concept}"

## TYPE de style recherché (étape 1)
{déclaration registre cible + densité + température + justification 3-5 phrases citant concept/territoire/curseur}

## Scan exhaustif (étape 2)
{34 lignes : "01. {Style} — COMPATIBLE/INCOMPATIBLE — raison"}

## Longlist ordonnée (étape 3)
{6-8 candidats avec justification spécifique passant les 5 règles}

## Arbitrage final (étape 4)
**Type** : Style pur OU Mix dominant × modulateur
**Style {pur OU dominant}** : {Nom officiel} (Source : Perplexity #{N} ou Partie 2 lettre {X})
**Style modulateur** (si MIX) : {Nom officiel} (Source : ...)

## Justification stratégique (3-4 phrases)
{Pourquoi ce choix résout la tension du brief, sert le concept, et marque l'éloignement (ou le respect) du ventre mou sectoriel}

## Signatures à incarner (issues du catalogue, copiées intégralement)
{Liste à puces — du champ "Signatures visuelles à incarner" du style retenu}

## Modulations dues au mix (si applicable)
{Liste à puces — 1-2 signatures du modulateur intégrées + DOMAINE concerné : "uniquement dans l'atmosphere block", "uniquement sur la typo display", etc.}

## INTERDITS actifs
{Liste à puces — du champ "INTERDITS" du style retenu (et du modulateur si MIX)}

## Garde-fous anti-slop activés (étape 5)
{Liste à puces — vérifications de l'étape 5 explicitement formulées comme directives pour le pitch designer}

## Cohérence système (vérification règles 6-7)
- **Pairing typo + style** : {1-2 phrases sur la cohérence sensorielle des 3 ingrédients}
- **Contraste structurel** : {axe de distinction style ↔ typo}

## Références culturelles
{3-5 références — utilisées comme étalons mentaux par le pitch designer et la phase 4}

## Avis du DA (auto-critique obligatoire)
- **Force majeure** : ce qui est indiscutablement réussi dans ce choix de style pour ce concept
- **Risque potentiel** : ce qui pourrait poser problème (cohérence tendue avec les ingrédients, niche sectorielle, etc.)
- **Position ZAG** : suffisamment différenciant vs Ventre Mou sectoriel ?
```

---

## Règles cardinales de validité

Pour qu'une fiche de style soit valide, elle DOIT :

1. **Avoir scanné les 34 styles** (étape 2 complète, pas tronquée)
2. **Avoir une justification spécifique** sur le choix final (pas "ce style est moderne" ; règle 3)
3. **Citer le brief / concept / curseur / ventre mou** dans la justification (pas de "c'est un bon choix en général")
4. **Si MIX, modulateur compatible** documenté dans le catalogue (gate 2 orchestrateur)
5. **Style retenu existe dans la Partie A** du catalogue (gate 1 orchestrateur — pas d'invention)
6. **Avis du DA rendu** (auto-critique 3 axes)

Si une de ces 6 règles est violée → l'orchestrateur resume le sub-agent styliste avec feedback ciblé. Max 2 itérations par règle violée.
