# Anti-Slop Blacklist — Core

Rédaction Niveau 1-2 selon `anti-slop-formulation-guide.md`. Listes nominatives (fonts, hex, filler words, fake names, syntax CSS précise) = gates Python uniquement, pas dans ce fichier.

**Portée** : interdictions UNIVERSELLES — s'appliquent quel que soit le curseur A, le registre atmosphérique, le concept narratif. Importé par Phase 4 (styletile + artefact), Batch 2, Batch 3.

---

## §1 — Anti-patterns datés

Ces patterns étaient courants en 2015-2020. Aujourd'hui ce sont des marqueurs de CSS générique — ne les utilise jamais, même si un exemple en contient.

### Hovers datés
- Do NOT lift on hover — no translateY, no scale > 1.02, no translate on child elements
- Do NOT use underline reveal on hover — hierarchy comes from weight, size, color
- Do NOT shift letter-spacing on hover — 2017 premium footer cliché

### Animations infinies décoratives
- Do NOT use infinite decorative animations — no pulsing, breathing, drift, flicker
- Do NOT use infinite rotation or angle shifts on gradients — decorative debt
- Do NOT animate grain or noise — grain is a texture, not motion
- Do NOT use neon flicker, frequency bars, particle drift as decoration — revolved aesthetics

Alternative : `@starting-style` for entries, `animation-timeline: view()` for scroll. No infinite decorative loops.

### Séparateurs entre sections
- Do NOT use wave/zigzag dividers — WordPress template marker
- Do NOT use diagonal clip-path as section transition — section edges are straight
- Do NOT use decorative gradient lines between sections

Alternative : background change or spacing shift marks the transition.

### Effets visuels datés
- Do NOT use glow shadows without directional offset — shadows have offset and direction
- Do NOT use text-shadow glow on titles — emphasis comes from size and weight
- Do NOT use scan lines or CRT overlays — retro-futurism era
- Do NOT use heavy neumorphism (symmetric inset/outset double shadow) — and its cousins (soft-UI 2020 era, skeuomorphic plastic surfaces)
- Do NOT use outer glow / neon halo as decoration — large blurred coloured shadow detached from the element. Cousins : cyberpunk décoratif, néon 2010s. Préférer inner border, ombre tintée subtile, ou contraste de fond.
- Do NOT use heavy backdrop-filter blur — 16px+ is dated glassmorphism; keep to ≤12px and punctual
- Do NOT use glassmorphism (blur background + translucence) as a default decorative effect — acceptable uniquement comme intention forte assumée, jamais comme texture par défaut sur cartes ou panneaux
- Do NOT use thick colored borders as importance markers — container distinction comes from background or typography
- Do NOT use decorative strokes before/after/under overlines or titles — hierarchy is size, weight, color
- Do NOT use H1 oversize as the only hierarchy lever — combine weight, color, space, position. La taille seule produit un titre qui crie sans rien organiser.

NOTE : the typographic-strokes rule bans TYPOGRAPHIC strokes (lines on overlines, labels, titles). Compositional pseudo-elements for graphic accents (shapes, positioned geometric accents) remain valid — see §2.

NOTE brutaliste : pure black, neon saturé, CRT scanlines sont à éviter SAUF comme intention esthétique brutaliste totale assumée et cohérente sur l'ensemble. Pas comme accent ponctuel sur un design par ailleurs sage.

### Animations d'entrée datées
- Do NOT use manual staggered fade-up — 2017 landing page signature, use `@starting-style` instead
- Do NOT use clip-path reveal animations — 2019 technique, feels dated today

### Compositions datées
S'appliquent à TOUTES les sections (Voice Block, Artefact, Atmosphere, chapitres Batch).

- Do NOT use rigid 50/50 hero split as default layout — web's most generic composition
- Do NOT use grids of N identical containers — vary proportions, hierarchize by size
- Do NOT use repetitive alternating text/image left-right across sections — predictable skeleton
- Do NOT use pricing columns with central option highlighted — copied everywhere
- Do NOT use "process steps" as numbered icon blocks — generic landing pattern
- Do NOT use exhaustive link-column footers — footer is a conclusion, not a sitemap
- Do NOT use product screenshots in device frames (laptop, phone) — show product through components
- Do NOT use carousels as content containers — content is visible, not hidden behind arrows
- Do NOT use feature sections as uniform icon+title+description containers — web's most copied pattern

### Cartes et conteneurs
- Do NOT containerize content systematically — la carte (rectangle arrondi + ombre douce + padding) n'est pas l'unité par défaut. Préférer espace + alignement pour structurer.
- Do NOT nest cards inside cards — chaque niveau d'imbrication dilue la hiérarchie et signale un défaut de design.
- Do NOT use generic rounded-rect + drop-shadow card as default container — et ses cousins (templates SaaS 2020-2023, dashboard kits Figma génériques). Si une carte est nécessaire, justifier sa présence par une intention (séparation forte, élévation sémantique).
- Do NOT use modals for actions that could be inline — le modal est une solution paresseuse, il interrompt le flux. Réserver aux confirmations critiques ou aux contextes vraiment isolés.
- Do NOT use decorative sparklines without real data — les mini-courbes décoratives sans signification simulent une dataviz, c'est du faux signal.

---

## §2 — Couche graphique décorative — interdictions

Complète les règles positives de la couche graphique documentées dans `phase-4-styletile.md` (catégories admises, socle obligatoire, seuils de visibilité).

- Do NOT include brand name as oversize semi-transparent watermark — ultra-rare in elite sites, always mediocre
- Do NOT use circles with stroke as decoration — no concentric rings, no target/dial patterns
- Do NOT use figurative SVG paths — recognizable objects (gear, leaf, star, sun, ...) are illustrations, not graphic elements
- Do NOT use large closed geometric contours with visible border — border > 1px or opacity > 6% on shapes covering > 30% of a section creates an empty frame that floats

Alternative au contour : un `radial-gradient` diffus qui crée l'IMPRESSION de la forme sans bord net, ou une masse remplie semi-transparente. Exception : border très fin (1px) ET très transparent (opacity ≤ 6%) devient une texture atmosphérique et reste autorisé.

---

## §3 — Typographie et fonts (listes en gate Python)

Procédure de sélection : `font-matching-rules.md` (8 règles de matching font × concept) et `font-pools/` (pools autorisés par registre). Les rex `font-selection-rex.md` et `font-selection-next-session.md` documentent les choix passés.

Les training-data defaults (geometric sans-serifs des années 2010, serifs classiques vus partout) sont détectés et bloqués par `scripts/phase4-blacklist-gate.py` `check_banned_fonts` au runtime. La liste nominative n'apparaît jamais ici pour éviter la contamination.

**Clause anti-cousin** : quand tu évites une famille, évite aussi ses cousins visuels. Si ton choix final ressemble à ce que tu aurais pris en réflexe, reprendre la procédure.

*Section à enrichir à l'Étape 3 avec les règles sémantiques transverses (one font family multiple weights, weight spectrum, etc.) si pertinent.*

---

## §4 — Couleurs et palette (listes en gate Python)

Les règles positives (OKLCH, palette structurée, 60-30-10, teinte des neutres) sont dans `phase-3b-palette.md` et gardées par `scripts/phase3b-css-gate.py`.

Les training-data defaults de palette (pur noir, pur blanc, accent indigo, AI purple/blue gradient, defaults non-teintés) sont détectés et bloqués par `scripts/phase4-blacklist-gate.py` et `scripts/phase3b-css-gate.py` au runtime.

*Section à enrichir à l'Étape 3 avec les règles sémantiques transverses (mixing warm/cool grays, oversaturated accents, decision fatigue multiple accents, etc.).*

---

## §5bis — Robustesse, performance, choix techniques

Patterns à éviter au niveau implémentation. Pas des valeurs nominatives — des choix de mécanique CSS qui produisent du slop ou de la fragilité.

- Do NOT use flexbox + calc() math to fake a grid — préférer CSS Grid quand le layout est bidimensionnel. Le flex avec calculs complexes signale un mauvais choix de modèle.
- Do NOT apply grain / noise filters on scrollable containers — coût performance catastrophique. Réserver le grain à un pseudo-element en position fixed avec pointer-events:none, jamais sur un conteneur qui scroll.
- Do NOT design text containers as if content was always short — anticiper le débordement (truncation, line-clamp, break-words selon contexte). Un layout qui casse au premier titre long est un layout fragile.
- Do NOT forget min-width:0 on flex children that contain truncatable text — sans cette propriété, la troncation ne fonctionne pas et le contenu force la largeur du parent. Règle de robustesse, pas d'esthétique.

---

## §5 — Copy et placeholders (listes en gate Python)

Les générateurs placés automatiquement ont des training-defaults bien documentés : placeholder names (Jane/John Doe, Acme, Nexus, SmartFlow style), fake round percentages, marketing filler words (Elevate/Seamless/Unleash style), Lorem Ipsum, avatars par défaut (Lucide/Feather user icons).

Ces énumérations vivent dans `scripts/phase4-blacklist-gate.py` (`check_fake_names`, `check_filler_words`, `check_lorem_ipsum`, `check_avatar_placeholders`) et sont bloquées au runtime.

Dans le prompt, la règle générique suffit : utilise des noms contextuels réalistes, des chiffres organiques, des verbes concrets, du draft copy aligné avec le brief.

*Section à enrichir à l'Étape 3 avec les règles sémantiques transverses (empty state pattern, error message 3-part formula, active voice, etc.).*

---

## Source et traçabilité

**Factorisation** : ce fichier remplace les sections redondantes dans :
- `phases/phase-4-styletile.md` (sections "ANTI-PATTERNS DATÉS — BLACKLIST" L302-349 et interdictions de "COUCHE GRAPHIQUE DÉCORATIVE" L218-270)
- `phases/phase-4-artefact.md` (section "ANTI-PATTERNS DATÉS" L144-151)
- `phases/phase-6a-batch2.md` (section "ANTI-PATTERNS DATÉS" L108-137)
- `phases/phase-6b-batch3.md` (section "ANTI-PATTERNS DATÉS" L86-114)

Les 4 phases importeront ce fichier via l'orchestrateur (pattern BIG : orchestrateur lit + injecte, subagent ne lit pas les refs directement).

**Règles reformulées** pendant la factorisation pour respect du guide (Niveau 3 → Niveau 2) :
- `Rotation/drift de gradient (--angle: 0deg → 360deg infinite)` → `Do NOT use infinite rotation or angle shifts on gradients`
- `Soulignement au hover (scaleX(0) → scaleX(1) sur ::before)` → `Do NOT use underline reveal on hover`

## Dernière mise à jour

2026-04-24 — Création par factorisation des 4 phases. Étape 1 du plan d'intégration anti-slop.
