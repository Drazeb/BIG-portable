---
name: design-system
description: |
  Design System Generator (DSG) — Génère un design system HTML technique sobre
  à partir d'un pack BIG (design-specs + style-tile + batch 2 + batch 3 + brand book).
  Format type Carbon / Atlassian : sidebar navigation, foundations exhaustives,
  tokens prêts à copier. Sobre, dev-grade, opposable. Complète le brand book.

  Invoquer avec /design-system depuis un dossier session BIG, ou en passant le
  chemin du dossier en argument.

  STATUT : ACTIF — branché dans le pipeline BIG en Phase 8b (post Brand Book, pré
  Packaging) depuis le 29 mai 2026 (D62). Peut aussi être lancé en autonome sur
  un pack existant.
---

# Design System Generator (DSG)

> Skill ACTIF, branché dans le pipeline BIG en Phase 8b depuis 2026-05-29 (D62).
> Produit un DS technique sobre type Carbon/Atlassian, qui respecte la DA de la
> marque sans tomber dans le brand book. Blindé par 14 règles sanctuarisées + ~120
> items de checklist + script Python d'audit anti-régression.

## Quand l'utiliser

- Après le Brand Book (Phase 8 BIG), avant le Packaging (Phase 9 BIG).
- En autonome sur un dossier session BIG existant pour tester / itérer.

## Inputs requis

Dans le dossier session passé en argument (ou détecté automatiquement) :

| Fichier | Rôle | Obligatoire |
|---------|------|-------------|
| `{brand}-design-specs.md` | Source de vérité textuelle (12 sections : Identité, Color, Typo, Iconographie, Logo, Dataviz, Photo, Composition, Illustration, Motion, Tokens, Don'ts) | ✅ |
| `{brand}-style-tile.html` (ou `concept-N.html`) | Bloc `:root` de référence + composants atomiques + grammaire visuelle CSS | ✅ |
| `{brand}-batch2.html` (ou `batch2-{concept}.html`) | Wordmark, Iconographie, Composants UI, Data viz — patterns CSS hérités | ✅ |
| `{brand}-batch3.html` (ou `batch3-{concept}.html`) | Photo, Composition, Illustration — patterns CSS hérités | ✅ |
| `{brand}-pitch-c{N}.md` | Ton de voix, ICP, tension (lu pour comprendre l'esprit, pas pour copier) | recommandé |
| `visual-final/` | Visuels finaux dérivés (rarement utilisés par le DS, sauf en illustration des sections Photo/Illustration) | optionnel |

## Output

Un fichier unique : `{brand}-design-system.html` dans le dossier session.
Page scrollable avec sidebar navigation + 10 à 12 sections + footer.

## Règles de génération sanctuarisées

Lire **OBLIGATOIREMENT** `ref/design-system-generation-rules.md` avant toute génération.
Ces règles sont issues d'un cycle d'itération validé sur Camille (mai 2026) et
prévalent sur toute autre interprétation. Toute violation rend le DS rejetable.

Les 10 règles, en synthèse (détails dans le fichier ref) :

1. **Fond clair de la palette** (équivalent `--color-chart-mist` du brand). Jamais varié, jamais d'image hero, jamais de gradient mesh.
2. **Type scale documenté = type scale appliqué**. Auditer le doc final : toute taille utilisée doit être listée dans la section Typography. Le H3 sub-section (clamp 1.3-1.9rem, Gloock 400, hérité Batch 2/3) est légitime même si absent du design-specs §03.2.
3. **Grammaire visuelle Batch 2/3 reprise** : hairline verticale 1px gradient Foyer à gauche de la zone main + beacon mark 12px en tête + overlines `barre courte 1px Foyer + texte mono uppercase letter-spacing 0.30em` + dotted underlines sur sub-section heads + numérotation sub-section en Mono Foyer letter-spacing 0.20em.
4. **Pas d'encadrés génériques** type "barre verticale 2-4px Foyer + box surface + bordure". Les blocs spéciaux (loi, don't) sont structurés en hairlines horizontales dotted + overline label + statement + liste plate avec marker mono. **Anti-AI-slop.**
5. **Ton dev/factuel partout**. Phrases courtes, énumérations, usage explicite. **Exceptions sacrées** : (a) les **noms de tokens** (`Foyer du Phare`, `Nuit d'Indigo`…) restent intacts, (b) les **règles formelles** type `99/1`, `1.5px canonique` peuvent être emphased en Gloock italic H3.
6. **Sourcing strict des don'ts**. Tout item de section "Don't" DOIT être présent dans `design-specs.md §12` ou dans une règle explicite des sous-sections (ex: "Pas de troisième fonte" §03.1). **Pas d'extrapolation, pas de dérivation, pas d'invention**.
7. **Sidebar nav numérotée standard Carbon-like** : groupes "Foundations" / "Identity" / "Assets" / "Patterns" / "Resources" selon découpage. Liens numérotés `01 / 02 / 03…`. Indicateur d'état actif via border-left Foyer.
8. **Bloc `:root` final** dans une section "Tokens" en fin de doc, en `<code>` complet avec syntax highlighting passif (couleurs token + valeur). Prêt à copier-coller.
9. **Mention explicite des choix d'architecture** : si la marque utilise des tokens flat (cas Camille — pas de hiérarchie primitive/semantic/component), le mentionner dans une mini-section "Token architecture" pour qu'un dev sache à quoi s'attendre.
10. **Mini-section "Voice" optionnelle** issue de design-specs §01.4 (Tone of Voice), si présente. Pas le reste de §01 (Calibration, Tension, Posture, ICP — c'est du brand book).

## Périmètre standard — 10 sections

Sauf indication contraire dans les inputs, générer ces 10 sections dans cet ordre :

| N° | Section | Source design-specs | Source batches |
|----|---------|---------------------|----------------|
| 01 | Color | §02 (palette + sémantique + WCAG + dataviz tokens) | style-tile :root |
| 02 | Typography | §03 (pairing + scale + lisibilité + lettrage signature) | style-tile + Batch 2 |
| 03 | Spacing & Density | §08.2/08.4 + §11 | style-tile :root |
| 04 | Grid / Layout | §08.1 (3 grilles canoniques) + §08.3 (patterns) | Batch 2 ch04 layout |
| 05 | Iconography | §04 (grammaire + strokes + abstraction + vocabulaire) | Batch 2 ch06 |
| 06 | Logo / Wordmark | §05 (lockups + zone exclusion + variantes) | Batch 2 ch05 |
| 07 | Data visualization | §06 (familles + grilles + chromatique + typo data) | Batch 2 ch07 |
| 08 | Photography | §07 (style + traitement + cadrages + prompting) | Batch 3 ch08 |
| 09 | Illustration | §09 (pivot + physique + lois cohabitation + interdits) | Batch 3 ch10 |
| 10 | Motion | §10 (easings + durées + patterns hover + reduced motion) | style-tile transitions |

Section optionnelle finale : **11 — Tokens** (le `:root` complet prêt à copier).

**NE PAS générer de section Voice** — le tone of voice (§01.4 du design specs) appartient au brand book, pas au DS technique. Décision tranchée mai 2026.

## Tableau inventaire-type — CHECKLIST OBLIGATOIRE par section

Pour chaque section, AVANT de finaliser, faire l'inventaire exhaustif des items de la source et vérifier présence 1:1 dans le DS. **SI UN SEUL ITEM MANQUE → AJOUTE-LE AVANT DE FINALISER.**

| Section DS | Source design-specs | Items à compter / lister (inventaire exhaustif) |
|------------|--------------------|-----------------------------------------------|
| 01 Color | §02.1 + §02.3 + §02.4 + §02.5 + §12.1 | **Palette** : 9 rôles (Nuit d'Indigo, Nuit teintée, Bleu Quart de Nuit / Bleu marine de carte, Foyer du Phare, Foyer Clair, Brume de Plan, Encre de Veille **Bleutée**, Lueur de Compas, Sextant Atténué) — noms EXACTS · **Sémantique** : 4 rôles (Success, Warning, Error, Info) · **Dataviz palette** : 4 tons · **WCAG** : 4 ratios (recopier "sous AA" tel quel pour Sextant, NE PAS inventer un chiffre) · **Don'ts** : 5 items §12.1 |
| 02 Typography | §03.1 + §03.2 + §03.3 + §03.4 + §03.5 + §12.4 | **Pairing** : 2 fontes + justifications **complètes** (recopier toute la dimension stratégique : gravité éditoriale, registre instrumental, etc.) · **Type scale** : 7 tailles source + H3 sub-section (8e taille issue Batch 2/3) · **Rôles fonctionnels** : sous-section dédiée · **Lisibilité** : 3 directives · **Lettrage signature** : point final chaud comme graine · **Don'ts** : 3 items §12.4 + 1 item §03.1 |
| 03 Spacing | §08.2 + §08.4 + §11 | **Échelle** : 8 tokens · **Densité binaire** : 2 modes · **Cadence d'éclats** (formule rhétorique) · **Don'ts** : 1 item explicite §08.2 |
| 04 Iconography | §04.1 + §04.2 + §04.3 + §04.4 | **Grammaire** : 3 variantes (Outline 80% / Solid 10% / Duotone 10%) · **Strokes** : 4 (1.0 / 1.5 canonique / 2.0 / 3.0) + linecap round · **Abstraction** : 5 positions · **Vocabulaire** : 6 icônes avec **descriptions formelles source** (Cap = boussole abstraite, Portée = cercles concentriques, etc.) — **PAS de business-speak** · **Don'ts** : 4 items §04.4 |
| 05 Logo | §05.1 + §05.2 + §05.3 + §05.4 | **Concept** : mode wordmark + point final chaud · **Lockups** : 4 variantes (Primaire / Secondaire / Icon-only / Horizontale) — **PAS d'ajout "point Foyer obligatoire"** · **Zone exclusion** : 3 valeurs (1× cap-height / 64px / 18mm) · **Variantes contexte** : 4 (Négatif / Positif / Mono / OLED) |
| 06 Data viz | §06.1 + §06.2 + §06.3 + §06.4 + §02.4 | **Familles** : 3 (Line / Bar / Donut) sur **fond dark** · **Grilles & axes** : 6 éléments · **Usage chromatique** : 4 tons + règle 1 série Foyer · **Typo donnée** : 5 rôles · **Don'ts** : 3 items §06.3 |
| 07 Photography | §07.1 + §07.2 + §07.3 + §07.4 + §12.5 | **Style** : références incluant Linear / A24 · **Traitement chromatique** : 4 principes + échelle tonale L13→L72 · **Cadrages** : 4 typologies avec **vrais visuels** issus de `visual-final/` · **Prompt MidJourney sanctuarisé §07.4** (chaîne complète à recopier) · **Anti-territoires** : 6 items |
| 08 Composition | §08.1 + §08.3 + §12.2 | **Grilles** : 3 canoniques · **Patterns** : 3 · **Maxime "Cadence d'éclats"** §08.4 · **Don'ts** : 4 items §12.2 + §12.3 (Glow shadow + Subtle shadow systématique) |
| 09 Illustration | §09.1 + §09.2 + §09.3 + §09.4 + §09.5 | **Angle métaphore** : peinture huile post-impressionniste · **Physique** : 3 plans avec **visuels dérivés visual-final/** · **Pas de character design** : 4 éléments récurrents · **Lois cohabitation** : 4 lois · **Anti-territoires** : 12 items (compresser OK, mais tous les territoires couverts) |
| 10 Motion | §10.1 + §10.2 + §10.3 + §10.4 + §12.6 | **Philosophie** : citation « Le survol n'élève rien » · **Easings** : 3 (ease-out-expo / ease-sharp / slow décrochage) · **Durées** : 2 (320ms / 520ms) · **Patterns hover** : 5 règles **strictement sourcées** (PAS de pulse 0.85→1 inventé) · **Reduced motion** · **Don'ts** : 3 items §12.6 |
| 11 Tokens | §11 | **Bloc `:root` complet** identique au style-tile + bilan « 9 couleurs · 2 fontes · 5 type-scale · 1 radius · 3 shadows · 8 spacing · 4 transitions » (recopier exactement) · **Pas de §11.1 Token architecture** — décision tranchée mai 2026, retiré pour rester en strict catalogage |

**Action obligatoire pour le sub-agent générateur** :

1. À la fin de chaque section, faire l'inventaire selon ce tableau.
2. Si un item manque → l'ajouter immédiatement, ne pas finaliser sans.
3. Produire `{brand}-design-system-inventory.json` avec, pour chaque section, items attendus vs items présents.
4. Produire `{brand}-design-system-audit-sources.json` complet (pas juste les don'ts — TOUT) qui mappe chaque item du DS à sa ligne source.

**Don'ts du §12 doivent être DISTRIBUÉS dans les sections concernées** (pas une section Don'ts globale) :
- §12.1 Chromatie (5) → section 01 Color
- §12.2 Composition (4) → section 08 Composition
- §12.3 Effets/shadows (3) → distribués : 1 dans Motion (translate Y), 2 dans Composition (glow shadow + subtle shadow systématique)
- §12.4 Typographie (3) → section 02 Typography
- §12.5 Imagerie (5) → distribués entre 04 Icono, 07 Photo, 09 Illustration
- §12.6 Motion (3) → section 10 Motion

## Pipeline d'exécution

### Étape 1 — Détection du dossier session

Si argument passé à `/design-system`, l'utiliser comme `{session_dir}`.
Sinon, demander à l'utilisateur quel dossier session BIG il veut utiliser
(`outputs/test-{brand}-...`) ou détecter le plus récent.

Vérifier la présence des inputs obligatoires (table ci-dessus). Si l'un manque,
**signaler à l'utilisateur et stopper** — ne pas tenter de générer sans les sources.

### Étape 2 — Sub-agent générateur (Task tool, general-purpose)

Lancer **un seul sub-agent** avec :

- Le contenu intégral de `{brand}-design-specs.md`
- Le bloc `:root { ... }` extrait du style-tile
- Les patterns CSS atomiques extraits du Batch 2 (chapter shell, hairline, beacon mark, overlines, subsection heads)
- Le contenu de `ref/design-system-generation-rules.md` (les 10 règles)
- Le template HTML de référence : `ref/design-system-template.html` (gabarit Camille validé)
- Instruction : générer les 10 sections en respectant strictement les règles, en sourçant chaque don't, en appliquant le type scale documenté

Output du sub-agent : `{session_dir}/{brand}-design-system.html`

### Étape 3 — Audit auto-régression

Lancer le script `scripts/design-system-audit.py` qui vérifie :

- Toutes les tailles `font-size` du fichier sont dans le type scale documenté en §02 du DS
- Aucun `border-left: Xpx solid var(--color-beacon)` sur un bloc non-décoratif (anti-encadré générique)
- Tous les items des sections `Don't` sont sourcés (le sub-agent doit avoir produit un fichier `.audit-sources.json` qui mappe chaque don't à sa source design-specs)
- Le bloc `:root` final est strictement identique au style-tile source (cohérence absolue)

Si violation → reporter à l'utilisateur, ne pas finaliser.

### Étape 4 — Validation visuelle

Capture headless Chrome (3 hauteurs : 1400px / 3000px / 6000px) dans `{session_dir}/.tmp-dsg-shots/`.
Présenter à l'utilisateur. Itération possible via `/design-system --iter "corrige X"`.

### Étape 5 — Output final

`open {brand}-design-system.html` dans le navigateur par défaut.

## Anti-patterns connus (ne PAS faire)

Issus de l'itération Camille mai 2026 :

- ❌ Titre poétique style "Le manuel technique du repère" → utiliser **"Design System"** point.
- ❌ Lede manifesto ("Sobre, exhaustif, opposable. Il complète le brand book — qui pose la conviction…") → utiliser un lede factuel : "Spécifications visuelles pour les équipes design et engineering : tokens, composants atomiques, règles d'usage."
- ❌ Encadré "barre verticale Foyer 2-4px + box surface + bordure" → utiliser le pattern signature Camille (hairlines dotted horizontales + overline label + statement).
- ❌ Don't dérivé ou inventé ("Multiplier les valeurs hors tokens", "Régler l'inter-section au pifomètre") → ne mettre QUE ce qui est explicitement listé dans `design-specs §12`.
- ❌ Justifs typo poétiques ("Gravité éditoriale brûlante. Pleins/déliés contrastés qui dialoguent avec les coups de brosse de l'image-pivot") → factuel : "Sérif display, empattements affirmés, mono-weight. **Usage** : titres hero, manifesto, wordmark, pull-quotes."
- ❌ Tailles `font-size` hors scale (ex: `1.8rem` fixe quand le scale documente `clamp(2.5rem, 5vw, 4.5rem)`) → toute taille doit être dans le scale.
- ❌ Cards superflues autour de chaque don't / chaque règle → liste plate verticale avec marker mono.

## Branchement BIG (futur, post-validation)

Quand le skill sera validé :

1. Ajouter une nouvelle phase au pipeline BIG entre Brand Book (Phase 8) et Packaging :
   - Phase 8 = Brand Book (existant)
   - **Phase 8b ou 9 = Design System (nouveau)**
   - Phase 9 ou 10 = Packaging (décalé)
2. Mettre à jour :
   - `.claude/skills/brand-identity/SKILL.md` (orchestration de la nouvelle phase)
   - `ARCHITECTURE.md` (nouvelle brique)
   - `ref/pipeline-overview.md` (PS écosystème + section pipeline)
   - `.claude/skills/test-big/SKILL.md` (3 tables : prérequis, outputs, mapping)
3. Question utilisateur post-Brand Book : "Voulez-vous générer le design system ?" (oui par défaut).
4. Output inclus dans le pack final centralisé par Packaging + déploiement Vercel.

## Fichiers de référence

| Fichier | Contenu |
|---------|---------|
| `ref/design-system-generation-rules.md` | Les 10 règles sanctuarisées en détail, avec exemples et anti-exemples |
| `ref/design-system-template.html` | Gabarit HTML Camille validé (Color + Typography + Spacing) à utiliser comme référence structurelle par le sub-agent |
| `scripts/design-system-audit.py` | Script d'audit anti-régression (type scale, encadrés, don't sourcing, :root cohérence) — à créer en étape 2 du chantier |

## Versions

- v0.1 — 28 mai 2026 — Skill DRAFT, gabarit Color + Typography + Spacing validé sur Camille. Pas encore branché à BIG.
- v0.2 — 28 mai 2026 — Industrialisation : 14 règles sanctuarisées (R12 inventaire 1:1, R13 catalogage strict, R14 checklist par section), tableau inventaire-type d'~120 items, script Python d'audit anti-régression (`design-system-audit.py`). Patch DS Camille validé (10 inventions corrigées, 5 manquants ajoutés, audit Python PASS, 203/203 items présents, 0 critical).
- v1.0 — 29 mai 2026 — **ACTIF, branché dans le pipeline BIG en Phase 8b** (post Phase 8 Brand Book, pré Étape Finale Packaging) via D62. Pattern de branchement cloné de Phase 8 Brand Book (commit `fb18acf`). Mise à jour `brand-identity/SKILL.md` + `pipeline-overview.md` + `test-big/SKILL.md` (5 zones) + `CLAUDE.md` projet + `ARCHITECTURE.md` + `CHANGELOG.md` + `DECISIONS.md`. Portage public via `SKILLS_TO_PORT` de BIG-portable.
