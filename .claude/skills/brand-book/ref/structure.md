# Structure du Brand Book — 8 sections + intro Identity Card + cover + closing

Ce document décrit **précisément** ce que doit contenir chaque section, **où** trouver l'information dans le pack BIG, **quel mode chromatique** appliquer et **quel mode de présentation** (immersif / grille documentaire / éditorial minimaliste / fullbleed).

**SANCTUARISÉ 27 mai 2026** : section Voice & Tone retirée (focus brand identité visuelle, pas verbale) ; intro "Identity Card / Le pack en une vue" ajoutée entre sommaire et Big Idea ; renumérotation 07→06 / 08→07 / 09→08 ; sommaire passé en 2 colonnes ; Big Idea + Concept passés en 2 colonnes éditoriales.

---

## Vue d'ensemble du flux

```
[COVER fullbleed]             ← peinture pivot + wordmark centré
[SOMMAIRE]                    ← 2 colonnes CSS multicol, non-sticky, juste après cover
[INTRO IDENTITY CARD]         ← bento 7 cards "Le pack en une vue" · positif
01 BIG IDEA                   éditorial 2-cols · positif
02 CONCEPT                    éditorial 2-cols · positif
03 IDENTITÉ                   grille · positif
04 PALETTE                    immersif (1 page composée) · positif
05 TYPOGRAPHIE                immersif (1 page composée) · positif
06 SYSTÈME                    positif wrapper + îlots dark
   · 06a Iconographie         titre canonique "Une grammaire iconique tenue."
   · 06b Composants UI
   · 06c Data viz
   · 06d Composition
07 APPLICATIONS               positif wrapper
   · 07a Web                  PNG sur fond gradient palette
   · 07b Pitch Deck           spread asymétrique 2×3
   · 07c Réseaux sociaux      diptyque LinkedIn + X
08 PHOTO & ILLUSTRATION       Dark Cinema natif · grille de cadrages
[CLOSING fullbleed]           macro-halo + statement final · Dark Cinema
```

> **Préfixes CSS sanctuarisés** : `.bv4-*` pour Identity Card v4 (intro), `.s08b-*` pour Pitch Deck, `.s08c-*` pour Réseaux sociaux. Les préfixes `s08b` / `s08c` sont conservés (pas renommés en `s07b` / `s07c`) pour ne pas casser les feuilles existantes — seuls les eyebrows affichés sont renumérotés. Le préfixe `.bb-*` (Identity Card v3) est obsolète depuis le 27 mai 2026.

---

## COVER (fullbleed)

- **Contenu** : peinture pivot pleine page (hero) en background, wordmark `{brand}.` centré (point final en couleur d'accent), petit caption en bas ("Brand Book v{N}" + année).
- **Source** : `visual-final/{brand}-c{N}-{paletteID}-hero-*.png` (le plus large disponible, idéalement painterly atmospheric).
- **Mode chromatique** : **Dark Cinema natif** — pas de wrapper clair, le fond Nuit d'Indigo de la marque englobe tout.
- **Mode de présentation** : fullbleed `100vw × 100vh` (ou min-height 720px si écran petit).
- **Hauteur** : ~100vh (full viewport).
- **Règles** :
  - Wordmark en `--brand-display`, taille très grande (clamp ~72-120px), tracking légèrement réduit
  - Le point final du wordmark dans `--brand-color-accent` (graine typographique)
  - Pas de menu, pas de navigation : c'est une couverture de livre
  - Overlay sombre subtil si nécessaire pour la lisibilité (mais favoriser une image native sombre)

---

## SOMMAIRE

- **Contenu** : liste des sections (Identity Card en intro + 8 sections numérotées de 01 BIG IDEA à 08 PHOTO & ILLUSTRATION), 1 ligne par entrée.
- **Source** : statique (fait partie du squelette).
- **Mode chromatique** : positif (fond Brume de Plan).
- **Mode de présentation** : **CSS multicol 2 colonnes** (`column-count: 2`, `column-gap: clamp(40px, 5vw, 80px)`, `column-fill: balance`, `break-inside: avoid` sur chaque `.toc__item`). Liste max-width 1200px, ordre top→bottom col1 puis col2 (lecture naturelle). Non-sticky, lieu de transition entre cover et corps.
- **Hauteur** : ~520-640px.
- **Règles** :
  - Sub-title H2 court au-dessus de la liste (ex: "Le pack, chapitre par chapitre.")
  - Numéros en `--brand-body` mono petit (clamp 13-15px), couleur accent, letter-spacing 0.1em, min-width 3em
  - Titres section en `--brand-display` taille moyenne (clamp ~22-32px), letter-spacing -0.01em
  - Première entrée = intro Identity Card avec numéro `—` (tiret cadratin, pas de numéro chiffré)
  - Ligne fine `1px solid` couleur accent sous chaque entrée (sauf dernière)
  - Pas de page numbers (c'est du long-scroll, pas du PDF)

---

## 00 IDENTITÉ CONDENSÉE — "Le pack en une vue" (intro bento) — **SANCTUARISÉ 27 mai 2026 (v4)**

Bento d'ouverture inséré entre le sommaire et la section 01 BIG IDEA. Donne en une page composée l'image-pack de la marque : cover hero + wordmark enrichi + manifesto + iconographie mini + typo mini + dataviz + palette 6 couleurs. Structure **v4 figée** après itérations Charles : v3 (3×3 × 240px) → v4 (3×6 × 120px) avec icônes en taille naturelle 32px (au lieu de zoomées) + palette enrichie de 3 → 6 couleurs + wordmark passé d'un texte simple à un wordmark enrichi (overline + wordmark + signature mono), sans tagline (sanctuarisé sans tagline — redondant avec concept).

- **Contenu (7 cards en bento 3 cols × 6 rows, 120px par row = 720px total)** :
  - **Cover** (col 1, rows 1-4 — 480px) : visual hero pivot avec gradient overlay bas + label "Cover · atmosphère hero"
  - **Wordmark enrichi** (col 1, rows 5-6 — 240px) : overline mono ("Brand ID · LL-{année}") + wordmark `{brand}.` en display 54px (point final en accent) + signature mono 2 lignes (typiquement coordonnées géographiques + cadence/rythme propre à la marque, tirées du pitch). **Pas de tagline** (sanctuarisé : redondant avec le concept et alourdit la card).
  - **Manifesto** (col 2-3, rows 1-2 — 240px) : 2 lignes display (chacune terminée par un point en accent) + 1 ligne explicative mono · label "Manifesto"
  - **Iconographie mini — bande horizontale 4×** (col 2, row 3 — 120px) : fond accent (Foyer), 4 SVG icônes signature inline en ligne, **taille naturelle 32px** (PAS zoomées comme en v3 — c'était trop massif). Extraits de batch2.
  - **Typo specimen Aa+Aa** (col 2, row 4 — 120px) : grid 2 cols égales, baseline align — "Aa" display gauche (50px) + "Aa" mono droite (22px) + caption mono avec nom de la fonte
  - **Dataviz signature** (col 2, rows 5-6 — 240px) : bar chart 6 barres dont 1 active en accent (composé depuis batch2), label mono "Cadence · {valeur}" ou équivalent
  - **Palette 6 couleurs** (col 3, rows 3-6 — 480px) : grille interne 2 cols × 3 rows, 6 blocs au lieu de 3, chacun avec rôle + nom (display) + code HEX (mono). Rôles canoniques côté Camille : Fond profond (Nuit) · Fond surface (Nuit Claire) · Détail froid (Marine) · Surface claire (Brume) · Accent signal (Foyer) · Accent chaud (Foyer Chaud). Le skill adapte les noms par marque mais conserve les 6 rôles.
- **Source** : composition manuelle par le skill — cf. SKILL.md Étape 2e "Identity Card".
- **Mode chromatique** : positif wrapper, blocs individuels alternant Nuit / Marine / Brume / Foyer selon position dans le bento.
- **Mode de présentation** : bento 7 cards · 3 cols × 6 rows · `grid-template-rows: repeat(6, 120px)` · gap 14px.
- **Préfixe CSS** : `.bv4-*` (bento v4) pour éviter toute collision avec le reste du brand book et avec la v3 archivée.
- **Effet "grain"** : overlay SVG `feTurbulence` (.grain / .grain--dark) sur chaque card pour matière texturée.
- **Hauteur** : 720px stricts (6 rows × 120px) + title + padding ≈ 820px.
- **Variables Mustache nécessaires** : `{{IDENTITY_CARD_TITLE}}`, `{{COVER_VISUAL}}`, `{{BRAND}}` (wordmark), `{{WORDMARK_OVERLINE}}` (ex: "Brand ID · LL-2026"), `{{BRAND_SIGNATURE_COORDS}}` + `{{BRAND_SIGNATURE_CADENCE}}` (2 lignes mono tirées du pitch), `{{MANIFESTO_LINE1}}`, `{{MANIFESTO_LINE2}}`, `{{MANIFESTO_SUB}}`, `{{ICONGRID_LABEL}}`, `{{IDENTITY_CARD_ICONS_4}}` (composé — 4 cells `<div class="bv4-icongrid__cell">` avec SVG 32px), `{{FONT_DISPLAY_NAME}}`, `{{FONT_MONO_NAME}}`, `{{DATAVIZ_LABEL}}`, `{{DATAVIZ_SIGNATURE_SVG}}` (composé — `<svg>` bar chart 6 barres), et 6 fois `{{COLOR_N_ROLE/NAME/HEX}}` pour N de 1 à 6. Variables :root alias attendues dans la marque : `--color-foyer`, `--color-foyer-warm`, `--color-mist`, `--color-mist-cool`, `--color-marine-cliff`, `--color-night-clear` (optionnel, fallback `#142133`), `--brand-color-dark-bg`, `--font-display`, `--font-mono`, `--radius`.

---

## 01 BIG IDEA

- **Contenu** : le grand énoncé conceptuel de la marque, en mode éditorial minimaliste (PAS un statement-poster gigantesque, PAS de méta-fields en grille).
- **Source** : `{brand}-pitch.md` section "Big Idea" + `{brand}-design-specs.md` §01.2 "Intention Créative".
- **Mode chromatique** : **positif** (Brume de Plan ou équivalent clair de la palette).
- **Mode de présentation** : **éditorial 2-cols magazine** (voir `editorial-patterns.md`) :
  - Titre `01 — BIG IDEA` en eyebrow petit caps
  - H1 simple en `--brand-display` (3-4 mots maximum, jamais une phrase entière)
  - Sous-titre italique en accent (couleur Foyer du Phare ou équivalent) — facultatif
  - **Corps en `.editorial-column` 2 colonnes CSS multicol** : `column-count: 2`, `column-gap: clamp(40px, 5vw, 80px)`, `column-fill: balance`, `max-width: 1100px`, `break-inside: avoid` sur chaque `<p>`. Fallback 1 col + max-width 55ch sous 768px.
  - 4-5 paragraphes courants de 2-4 lignes
- **Hauteur** : ~720-820px.
- **Règles** :
  - Beaucoup d'air en haut et en bas (padding vertical ≥ 120px)
  - Pas d'illustration, pas d'image, pas de décoratif — c'est un texte qui respire
  - Si le pitch a une formule-signature (ex: "Voltage Zen"), elle peut servir de sous-titre italique

---

## 02 CONCEPT

- **Contenu** : développement du concept en 3-5 paragraphes, optionnel : manifesto split (2 colonnes) pour citer le manifesto ou des piliers.
- **Source** : `{brand}-pitch.md` sections "Concept", "Manifesto", "Pilliers" + `{brand}-design-specs.md` §01.3 "Territoire Sémantique".
- **Mode chromatique** : **positif**.
- **Mode de présentation** : **éditorial 2-cols magazine** (même règle qu'01) :
  - Titre `02 — CONCEPT`
  - H2 simple en display
  - **Corps en `.editorial-column` 2 colonnes CSS multicol** (cf. 01 BIG IDEA pour la spec exacte)
  - **Optionnel** : si la marque a un manifesto fort (3-5 lignes capitalisées), le placer en split 2-colonnes (manifesto à gauche en gros, glose à droite en plus petit)
- **Hauteur** : ~720-900px.
- **Règles** :
  - Mêmes règles d'air que 01
  - Si manifesto split : aligner sur la grille single-column max-width pour ne pas casser le rythme

---

## 03 IDENTITÉ

- **Contenu** :
  - 4 lockups (horizontal, vertical, symbol-only, wordmark-only)
  - Clear space (zone d'exclusion) avec mesure dérivée du symbole
  - Variantes de contexte (sur fond clair, sombre, accent, photo)
- **Source** : `{brand}-batch2.html` (extraire la section §05 Logotype) + `{brand}-design-specs.md` §05 LOGOTYPE (§05.2 lockups, §05.3 clear space, §05.4 contextes).
- **Mode chromatique** : **positif** (la section).
- **Mode de présentation** : **grille documentaire**.
  - Une ligne pour les 4 lockups (grid 2×2 ou 4×1 selon largeur)
  - Une ligne pour le clear space avec annotation des marges
  - Une ligne pour les variantes de contexte (4 vignettes carrées : sur clair / sombre / accent / photo)
- **Hauteur** : ~860-1020px.
- **Règles** :
  - Chaque lockup dans une vignette à fond neutre (pas un fond accent qui distrait)
  - Légende sous chaque lockup en eyebrow petit caps : `HORIZONTAL`, `VERTICAL`, etc.
  - Le clear space avec hachures ou pointillés discrets pour montrer la zone d'exclusion

---

## 04 PALETTE — MODE IMMERSIF (1 page composée)

- **Contenu** : la palette canonique de la marque, **TOUTES les couleurs sur 1 SEULE page composée**, format Solara/Agenie/MachineX (grands rectangles immersifs côte à côte, pas 1 couleur = 1 page).
- **Source** : `{brand}-design-specs.md` §02 COLOR SYSTEM (§02.1 primary, §02.2 secondary/accent, §02.3 neutrals, §02.4 semantic). Au minimum 9 couleurs.
- **Mode chromatique** : **positif** (wrapper clair) ; les rectangles de couleur OCCUPENT la page dans une grille immersive.
- **Mode de présentation** : **MODE IMMERSIF COMPOSÉ — 1 page entière dédiée à la palette**, en grille élégante (style Solara : 4 grands blocs 2×2 / style Agenie : bandes verticales / style MachineX : 11 colonnes côte à côte).
  - Grille recommandée : 3×3 ou asymétrique 4 grands + 5 secondaires + sémantiques en bandeau bas
  - Chaque rectangle suffisamment grand pour "ressentir" la couleur (min 220×180px, idéalement 300×260px)
  - Chaque rectangle contient en superposition : nom de la couleur en `--brand-display`, codes HEX et oklch en monospaced petit, rôle en eyebrow caps
  - Si la couleur est foncée, texte en clair ; si claire, en sombre
  - Title de section "04 — PALETTE" + intro courte 1-2 phrases en haut
- **Hauteur** : **~720-900px (1 slide)**.
- **Règles** :
  - Pas de mini-swatches ronds (cliché Photoshop preset)
  - Pas de 9 pages successives (sur-immersion qui casse le slide rythm — c'était mon erreur d'interprétation des benchmarks)
  - Les vrais brand books (Solara, Agenie, MachineX) font TOUS "toute la palette sur 1 page composée"

---

## 05 TYPOGRAPHIE — MODE IMMERSIF (1 page composée)

- **Contenu** : grands spécimens Display + Body + Pairing + Type Scale **composés sur 1 SEULE page**, format Solara (composition immersive, pas 4 pages successives).
- **Source** : `{brand}-design-specs.md` §03 TYPOGRAPHIE (§03.1 pairing, §03.2 type scale, §03.3 rôles, §03.4 lisibilité) + le style-tile pour les Google Fonts effectivement importés.
- **Mode chromatique** : **positif**.
- **Mode de présentation** : **MODE IMMERSIF COMPOSÉ — 1 page entière dédiée à la typo**, layout composé :
  - Bloc gauche : grand "Aa" Display (~clamp 200-320px) + nom de la police en eyebrow + 1 mot brand-signature en grand
  - Bloc droite : grand "Aa" Body (~clamp 160-240px) + nom + 1 phrase courante
  - Bandeau bas : Type Scale H1/H2/H3/Body/Caption en liste verticale compacte (5 lignes max)
  - Optionnel : un sous-bloc Pairing en bas-droite (titre + chapô + 2 lignes corps) pour montrer le couple en action
- **Hauteur** : **~720-900px (1 slide)**.
- **Règles** :
  - Les 2 spécimens "Aa" Display + Body côte à côte (pas un par page)
  - Type scale en liste simple, jamais en tableau complexe
  - Alphabet complet PEUT être omis si l'espace manque — préférer un mot brand-signature qui montre la "couleur" de la police

---

<!-- Section 06 VOICE & TONE retirée (SANCTUARISÉ 27 mai 2026) — focus
     brand identité visuelle, pas verbale. Renumérotation : ex-07 SYSTEM
     devient 06, ex-08 APPLICATIONS devient 07, ex-09 PHOTO devient 08.
     Préfixes CSS s08b- / s08c- conservés. -->

## 06 SYSTÈME (positif wrapper + îlots dark canoniques) — 4 SLIDES SÉPARÉES

**Chaque sous-bloc est sa propre slide ~720-900px**, pas un long bloc cumulé. Total = 4 slides successives.

- **Mode chromatique global** : **positif** pour le wrapper (titres, intros), **îlots dark canoniques** pour les composants production (les composants sont rendus dans leur état réel, qui est généralement Dark Cinema).
- **Mode de présentation** : **GRILLE DOCUMENTAIRE** dans chaque slide.

### 06a Iconographie — **SANCTUARISÉ 27 mai 2026**

- **Titre canonique** : **"Une grammaire iconique tenue."**
- **Subtitle canonique** : **"Outline canonique · Solid pour le CTA · Duotone pour l'état actif."**
- **Règle stricte** : **NE PAS mentionner un nombre d'icônes** (écarté explicitement par Charles le 27 mai 2026 — le nombre de grammaires peut varier par marque, on parle de la grammaire, pas du compte).
- **Contenu** :
  - Icônes canoniques de la marque (les "must-haves" identifiés en batch 2 — laisser le nombre s'adapter par marque)
  - Grammaires affichées (généralement 3 : outline / filled / duotone — ou les grammaires définies par la marque)
  - Échelle (du plus petit usage 16px au plus large 64px)
- **Source** : `{brand}-batch2.html` (section iconographie) + `{brand}-design-specs.md` §06 ICONOGRAPHIE.
- **Hauteur** : ~620-720px.

### 06b Composants UI

- **Contenu** : boutons (primary/secondary/ghost), inputs (default/focus/error), badges, cards, nav, tabs, etc.
- **Source** : `{brand}-batch2.html` (section UI components).
- **Mode** : chaque composant dans un îlot dark (fond Nuit d'Indigo) car c'est leur état production.
- **Hauteur** : ~720-920px.

### 06c Data viz

- **Contenu** : 3 charts SVG canoniques (line, bar, donut) — exemples avec données fictives sobres.
- **Source** : `{brand}-batch2.html` (section data viz) + `{brand}-design-specs.md` §07 DATA VIZ.
- **Hauteur** : ~520-620px.

### 06d Composition

- **Contenu** : 3 grilles canoniques (ex: editorial 12-col, dashboard 8-col, hero asymétrique) avec annotations des breakpoints.
- **Source** : `{brand}-design-specs.md` §09 SYSTÈME DE COMPOSITION.
- **Hauteur** : ~520-620px.

---

## 07 APPLICATIONS (positif wrapper)

La section 07 est **éclatée en 3 sous-blocs**, chacun en sa propre slide (sauf 07a Web qui est l'exception longue assumée).

**Préfixes CSS sanctuarisés** : `.s08b-*` pour Pitch Deck et `.s08c-*` pour Réseaux sociaux. Les préfixes restent en `s08b/c` (pas renommés en `s07b/c`) pour ne pas casser les feuilles existantes — seuls les eyebrows affichés sont renumérotés 07b / 07c.

### 07a WEB (positif wrapper) — EXCEPTION longue assumée ~1200-1600px **FULLBLEED sanctuarisé 27 mai 2026**

- **Contenu** : capture PNG full-page du style-tile, présentée comme un "écran de référence" — pas une iframe.
- **Source** : `{brand}-landing-fullpage.png` (généré par `scripts/capture-style-tile.py`).
- **Mode chromatique** : **positif** (wrapper clair).
- **Mode de présentation FULLBLEED** :
  - Titre de section en haut ("07a — Web" + h2 title) — reste contenu dans `.section__inner` (max-width 1320px)
  - **Stage FULLBLEED** : le `<div class="web__stage">` est enfant DIRECT de `<section>` (PAS dans `.section__inner`) pour toucher les bords gauche/droit du viewport
  - Fond du stage : **radial-gradient palette** asymétrique (accent + accent-2 + positive-bg) — gradient occupe TOUTE la largeur viewport
  - Image insérée comme `<img>` à `max-width: 900px`, centrée dans le stage
  - Drop-shadow direction (jamais 0 0) pour donner de la matérialité
  - Caption discret sous l'image : "Style-tile principal · viewport 1280 px · capture full-page"
  - **PAS de border-radius sur le stage** (`border-radius: 0`) — fullbleed strict sans cadre

- **Structure HTML sanctuarisée** :
  ```html
  <section class="section section--positive web" id="web">
    <div class="section__inner">  <!-- header contenu -->
      <p class="section__eyebrow">07a — Web</p>
      <h2 class="section__title">{{WEB_TITLE}}</h2>
    </div>
    <div class="web__stage">  <!-- FULLBLEED hors inner -->
      <img src="{{BRAND}}-landing-fullpage.png" />
      <p class="web__caption">{{WEB_CAPTION}}</p>
    </div>
  </section>
  ```

- **Hauteur** : ~1200-2000px (la capture est longue, c'est l'exception qui casse le rythme)
- **Règles** :
  - JAMAIS d'iframe
  - JAMAIS de scroll horizontal dans l'image
  - Le PNG doit être généré en headless Chromium à viewport 1280×800 avec `full_page=True`
  - Le stage DOIT toucher les bords gauche/droit du viewport (fullbleed) — pas de cadre carte autour du gradient (sanctuarisé après remarque Charles 27/05/26 : "le cadre qui entoure le style tile pas heureux, il faut que ça touche les bords")

---

### 07b PITCH DECK — pattern SPREAD ASYMÉTRIQUE 2×3 (figé, à brancher)

> **NOTE numérotation** : eyebrow affiché "07b" (après retrait Voice & Tone). Préfixe CSS conservé `.s08b-*` (sanctuarisé pour ne pas casser les feuilles existantes).

- **Contenu** : 6 slides 16:9 (1280×720 natives) générées par le sous-skill `generate-mini-deck` (qui invoque SPG Phase 0 mode mini), présentées dans un **spread asymétrique horizontal sur 2 lignes × 3 slides**.
- **Source** : sous-skill `/Slide Presentation Generator/.claude/skills/generate-mini-deck/` invoqué via sub-agent Task. Mapping figé : Cover (#1) · Case Study (#12) · Data Viz (#9) · Dashboard KPI (#10) · Process/Timeline (#7) · Icon Grid (#19).
- **Mode chromatique** : positif wrapper (fond Brume de Plan ou équivalent palette brand). Slides individuelles en alternance Dark/Light pilotée par Sub0-B SPG selon VISUAL-ANALYSIS.md §7.
- **Mode de présentation** — SPREAD ASYMÉTRIQUE :

```
Ligne 1 :  [Slide pos 1 · 75% visible]──[COVER · 100%]──[Slide pos 3 · 25%]
           ↑ coupée à gauche (overflow)                   ↑ coupée à droite (overflow)

Ligne 2 :  [Slide pos 4 · 25%]──[DATA VIZ · 100%]──[Slide pos 6 · 75%]
           ↑ coupée à gauche                              ↑ coupée à droite
```

  - Cover en position 2 (centre row top, 100% visible) — signature d'ouverture
  - Data Viz/Dashboard en position 5 (centre row bottom, 100% visible) — signature numérique
  - Positions 1, 3, 4, 6 : autres slides en alternance Dark/Light (déterminée par Sub0-B)
  - **PAS d'overlay hachuré** sur les slides aux extrémités (les 6 slides sont toutes des vraies slides, le débordement = juste l'overflow viewport)

- **CSS validé** :

```css
.spread {
  --slide-w: calc((100vw - 2 * var(--slide-gap)) / 2);  /* ≈ 48vw */
  --slide-gap: 28px;
  overflow-x: hidden;
}
.spread__row { display: flex; gap: var(--slide-gap); width: max-content; }
.spread__row--top    { transform: translateX(calc(-0.25 * var(--slide-w))); }
.spread__row--bottom { transform: translateX(calc(-0.75 * var(--slide-w))); }
.slide-card {
  flex: 0 0 var(--slide-w);
  aspect-ratio: 16 / 9;
  box-shadow: 0 8px 24px -4px rgba(13,22,35,0.18), 0 2px 6px rgba(13,22,35,0.08);
}
```

- **Hauteur** : ~1200-1400px (exception au slide rythm 720-900px car spread = 2 lignes de slides 16:9). Assumée.
- **Référence visuelle** : capture Guardbase montrant le pattern original.
- **Statut** : **PATTERN FIGÉ** — sub-skill `generate-mini-deck` v4 (6 archétypes) implémenté côté SPG. Reste à brancher dans `brand-book/SKILL.md` Étape 4bis et générer brand book Camille v3 avec section 07b active.

---

### 07c RÉSEAUX SOCIAUX — diptyque LinkedIn + X sur 2 fonds palette **SANCTUARISÉ 27 mai 2026**

> **NOTE numérotation** : eyebrow affiché "07c" (après retrait Voice & Tone). Préfixe CSS conservé `.s08c-*` (sanctuarisé pour ne pas casser les feuilles existantes).

Section calibrée sur référence Khairallah AL-Awady (X officiel) + LinkedIn entreprise réel. **Ne pas dévier de cette spec** — les ratios et tailles ont été validés en 6+ itérations avec Charles. Seuls les champs marqués `{{...}}` varient par marque.

- **Contenu** : 2 mockups de profil entreprise (LinkedIn + X) présentés côte à côte en **diptyque fullbleed sur 2 fonds palette différents**.
- **Source** :
  - LinkedIn capturé via `scripts/capture-linkedin-mockup.py` depuis `ref/linkedin-profile-mockup.html`
  - X capturé via `scripts/capture-x-mockup.py` depuis `ref/x-profile-mockup.html`
  - Customisation marque : UNIQUEMENT cover image (depuis visual-final/) + avatar (mode wordmark brand) + champs textuels meta. Tout le UI plateforme reste strict (couleurs natives, typo system, boutons Follow/Souscrire en couleur officielle).

- **Mode chromatique — RÈGLE FONDAMENTALE** :
  - La section `.s08c-section` a un fond **transparent** (pas de fond global).
  - Cellule LinkedIn : fond **beige clair chaud DISTINCT** du fond Brume bleu-froid du body — exemple Camille `oklch(0.92 0.025 78)`. À adapter par marque mais doit être visuellement distinct du `--brand-color-positive-bg` (sinon la cellule se confond avec le fond de la page).
  - Cellule X : fond **Nuit profonde** = `var(--brand-color-dark-bg)` (l'absolu noir-bleuté de la palette marque).
  - Les 2 cellules **touchent strictement les bords gauche/droit** de l'écran (fullbleed) — pas de `max-width` ni `padding-inline` sur `.s08c-diptych`.

- **Mode de présentation** — DIPTYQUE FULLBLEED :

```
├──────────────────────────────────┼──────────────────────────────────┤
│  [FOND BEIGE CLAIR CHAUD]        │  [FOND NUIT PROFONDE]            │
│  fullbleed bord gauche → milieu  │  fullbleed milieu → bord droit   │
│                                  │                                  │
│      ┌─────────────────┐         │      ┌─────────────────┐         │
│      │  LinkedIn card  │         │      │   X profile     │         │
│      │  (profile +     │         │      │   (cover +      │         │
│      │   about empilées│         │      │    zone profil  │         │
│      │   flottantes)   │         │      │    1000×1000)   │         │
│      └─────────────────┘         │      └─────────────────┘         │
│       PROFIL ENTREPRISE          │       PROFIL ENTREPRISE          │
│           LinkedIn               │              X                   │
└──────────────────────────────────┴──────────────────────────────────┘
```

  - Grid 2 cols égales, `gap: 0` (les fonds collent)
  - Chaque cellule : `min-height: 720px`, padding `clamp(56px, 7vh, 96px) clamp(32px, 4vw, 80px)`, contenu centré
  - Mockup max-width 720px dans la cellule (image affichée en `width: 100%; height: auto`)
  - Légende sous chaque mockup : eyebrow "PROFIL ENTREPRISE" (uppercase letter-spaced) + nom plateforme en typo display (LinkedIn / X)

- **Format des mockups — ASYMÉTRIE ASSUMÉE (LinkedIn paysage / X carré)** :
  - **X** : viewport 1000×1000 — mockup carré (header 70 + cover 360 + actions 160 + identité ~410). Capture du viewport entier.
  - **LinkedIn** : viewport 1000×1000 mais **capture ciblée sur `.li-profile-card` via locator** → PNG paysage ~1000×563 (ratio 1.78:1). Pas de About card sous la profile card — Charles a explicitement écarté cette option (27 mai 2026).
  - Captures retina `device_scale_factor=2`
  - **LinkedIn `omit_background=True`** → fond transparent → la card flotte directement sur le beige de la cellule
  - **X sans omit_background** → fond blanc du mode light X intrinsèque

- **Équilibrage visuel dans le brand book — RÈGLE CLÉ** :
  - LinkedIn PNG (ratio 1000:563) et X PNG (ratio 1:1) ont des formats DIFFÉRENTS.
  - Pour avoir la même HAUTEUR visuelle dans le diptyque, X est réduit en largeur :
    - `.s08c-cell--linkedin .s08c-mockup { max-width: 720px; }` → affiché à 720×405
    - `.s08c-cell--x .s08c-mockup { max-width: calc(720px * 0.563); }` → affiché à 405×405
  - Les 2 mockups ont la **même hauteur visuelle** (~405px) → diptyque équilibré.
  - Charles a explicitement demandé cette approche (27 mai 2026) : "diminue l'image X pour qu'elle soit équilibrée avec LinkedIn". L'approche inverse (ajouter une About card sous LinkedIn pour étirer en carré) a été testée et rejetée comme alourdissant inutilement.

- **Wrapper mockup dans le brand book** :
  - `.s08c-mockup` : background blanc + box-shadow + border-radius (pour X)
  - `.s08c-cell--linkedin .s08c-mockup` : neutralisé (`background: transparent; box-shadow: none; border-radius: 0; overflow: visible`) — la card LinkedIn porte ses propres styles natifs
  - `.s08c-cell--x .s08c-mockup` : max-width réduit à `calc(720px * 0.563)` ≈ 405px

- **Spec interne mockup X (calé sur Khairallah AL-Awady)** :
  - Topbar 70px, padding 0 24px, contient back arrow (40px) + nom display (30px) + posts (17px) + **UNE SEULE icône loupe** (26px) à droite (PAS d'icône mute)
  - Cover 360px (ratio ~2.78:1 sur 1000px)
  - Avatar rond 290px (29% largeur), top -145px sur la cover (déborde de 50%), bordure 6px blanc
  - Nom 46px bold, verified 34px, handle 22px, bio 25px (line-height 34, max-width 880), méta 23px (svg 26)
  - Stats 21px, followed-by 20px (mini-avatars 28px)
  - Bouton Souscrire : font 26px, height 68px, padding 0 34px, rose #bc3afb (X Premium)
  - Icon-btn actions (More, Message, Notify, Add) : 64×64px, svg 30px

- **Spec interne mockup LinkedIn** :
  - Card profile (max-width 920px) **seule** : cover ratio 4:1, avatar carré 160px overlay -80px, nom 28-34px clamp, tagline 16-18px, meta 13-14px, boutons Follow/Visit website/More (font 18px, padding 10×24, border-radius 24)
  - Pas de About card sous la profile card (cf. note précédente — écarté par Charles)
  - Card background blanc + border subtile + box-shadow légère
  - Capture via `page.locator(".li-profile-card").screenshot()` → PNG paysage ~1000×563

- **Variables Mustache LinkedIn** : `{{BRAND_NAME}}`, `{{BRAND_DISPLAY}}`, `{{BRAND_BODY}}`, `{{BRAND_ACCENT_COLOR}}`, `{{BRAND_DARK_BG}}`, `{{BRAND_PRIMARY_FONT_URL}}`, `{{COVER_IMAGE_URL}}`, `{{WORDMARK_OVERLAY_HTML}}`, `{{PROFILE_AVATAR_HTML}}`, `{{TAGLINE}}`, `{{META_SECTOR}}`, `{{META_CITY}}`, `{{META_FOLLOWERS}}`, `{{META_EMPLOYEES}}`.

- **Variables Mustache X** : `{{BRAND_NAME}}`, `{{BRAND_DISPLAY}}`, `{{BRAND_BODY}}`, `{{BRAND_DARK_BG}}`, `{{BRAND_PRIMARY_FONT_URL}}`, `{{COVER_IMAGE_URL}}`, `{{COVER_OVERLAY_HTML}}`, `{{AVATAR_HTML}}`, `{{HANDLE}}`, `{{POSTS_COUNT}}`, `{{BIO}}`, `{{META_CATEGORY}}`, `{{META_LOCATION}}`, `{{META_URL}}`, `{{META_BIRTHDAY}}`, `{{META_JOINED}}`, `{{STATS_FOLLOWING}}`, `{{STATS_FOLLOWERS}}`, `{{FOLLOWED_BY}}`.

- **Hauteur section** : header (titre + eyebrow + subtitle dans un wrapper `max-width: 1320px`) + diptyque min 720px = ~1000-1200px total
- **Référence visuelle de validation** : `outputs/camille-test-v2/camille-brand-book.html` section `#social` — sanctuarisée le 27 mai 2026 après 6+ itérations Charles. Captures de référence : `outputs/Captures/Captures diverses/Capture d'écran 2026-05-27 à 00.38.22.png` (Khairallah X) + `outputs/Captures/Captures diverses/Capture d'écran 2026-05-27 à 09.25.04.png` (cible diptyque Charles).
- **Statut** : **SANCTUARISÉ** — squelettes mockups, dimensions internes, scénographie diptyque fixés. Reste à brancher dans `brand-book/SKILL.md` Étape 4bis pour générer automatiquement.

---

### 07d BENTO GRID — slide ~720-900px (à implémenter)

- **Contenu** : vitrine condensée de la personnalité brand en grille bento (asymétrique, 4-6 tuiles de tailles variables) : slogan signature en grand + logo lockup + 1 atome iconique + 1 couleur en aplat + 1 mini-mockup + 1 visuel brand.
- **Source** : composition d'atomes brand existants.
- **Mode chromatique** : positif wrapper, tuiles individuelles dans les couleurs brand.
- **Mode de présentation** : grille bento `display: grid` avec `grid-template-columns: repeat(6, 1fr)` et tuiles en `grid-column` / `grid-row` variables (1×1, 2×1, 1×2, 2×2).
- **Hauteur** : ~720-900px (1 slide).
- **Statut** : **PAS encore implémenté** — chantier à venir.

---

## 08 PHOTO & ILLUSTRATION (Dark Cinema natif)

- **Contenu** :
  - **4 cadrages canoniques** (ex: macro produit / portrait éditorial / paysage halo / nature morte atmosphérique — selon les cadrages définis par la marque)
  - **Signature de prompting MJ** (formule récurrente que la marque utilise pour générer ses visuels)
  - **Galerie** : 4-8 visuels finaux issus de `visual-final/`
- **Source** : `{brand}-batch3.html` + `{brand}-design-specs.md` §08 DIRECTION PHOTOGRAPHIQUE (§08.1 style, §08.2 traitement, §08.3 scénographie, §08.4 signature prompting) + §10 ILLUSTRATION (si applicable) + dossier `visual-final/`.
- **Mode chromatique** : **Dark Cinema natif** (la section entière est en fond Nuit d'Indigo, pas un wrapper clair).
- **Mode de présentation** :
  - Titre `08 — PHOTO & ILLUSTRATION` en blanc/clair
  - 4 cadrages canoniques en grille 2×2 ou 4×1, chacun avec titre + description courte
  - Signature de prompting MJ en bloc encadré (background légèrement plus clair que le fond, format code)
  - Galerie en grille 2-col ou 3-col selon nombre de visuels
- **Hauteur** : ~1200-1600px.
- **Règles** :
  - Tout en clair sur fond sombre
  - Légendes des visuels en eyebrow caps petites
  - Si la marque a une illustration narrative (§10 du design-specs), l'inclure dans cette section avec son propre sous-bloc

---

## CLOSING (fullbleed)

- **Contenu** : macro-halo + statement final (1 phrase signature, pas le pull-quote de la section 06 — quelque chose de plus court, plus définitif).
- **Source** : `visual-final/{brand}-c{N}-{paletteID}-halo-*.png` (le visuel halo le plus atmosphérique disponible) + statement extrait du pitch ou du design-specs §01.5 "Ancre de Posture".
- **Mode chromatique** : **Dark Cinema natif** (symétrie avec la cover).
- **Mode de présentation** : fullbleed `100vw × ~720-880px`, statement centré en display moyen.
- **Hauteur** : ~720-880px.
- **Règles** :
  - Pas de bouton, pas de CTA — c'est un livre, pas une landing
  - Optionnel : crédit discret en bas ("{brand} — Brand Identity, {année}")
  - Le halo en background occupe TOUTE la zone (pas un cadre étriqué)

---

## Récapitulatif hauteurs

| Section | Hauteur | Cumul |
|---------|---------|-------|
| COVER | ~100vh (~900px) | 900 |
| Sommaire (2 cols) | ~580px | 1480 |
| 00 IDENTITY CARD (bento intro) | ~820px | 2300 |
| 01 BIG IDEA (2 cols) | ~770px | 3070 |
| 02 CONCEPT (2 cols) | ~810px | 3880 |
| 03 IDENTITÉ | ~940px | 4820 |
| 04 PALETTE (1 page composée) | ~820px | 5640 |
| 05 TYPOGRAPHIE (1 page composée) | ~820px | 6460 |
| 06a Iconographie | ~720px | 7180 |
| 06b Composants UI | ~820px | 8000 |
| 06c Data viz | ~720px | 8720 |
| 06d Composition | ~720px | 9440 |
| 07a WEB | ~1600px | 11040 |
| 07b PITCH DECK (spread 2×3) | ~1300px | 12340 |
| 07c RÉSEAUX SOCIAUX (diptyque) | ~1100px | 13440 |
| 08 PHOTO | ~820px | 14260 |
| CLOSING | ~800px | 15060 |

**Total estimé** : ~14500-15500px (~15-16 écrans). Vrai brand book en slide rythm : chaque section est une "page" éditoriale de hauteur prédictible.

**Exceptions au slide rythm** (assumées) :
- 07a WEB : la capture PNG du style-tile est longue par nature (~1200-1600px), c'est la respiration du document
- 07b PITCH DECK : spread 2 lignes × 3 slides 16:9 (~1200-1400px)
- 07c RÉSEAUX SOCIAUX : diptyque fullbleed LinkedIn + X (~1000-1200px)
- 06 SYSTÈME : éclaté en 4 slides successives (06a/b/c/d) plutôt qu'une longue section

**Le mode immersif veut dire "composition pleine page avec présence visuelle forte", PAS "1 atome = 1 page"**. Les benchmarks Solara/Agenie/MachineX font tous "toute la palette en 1 page composée". Idem typo.
