# Prompt — Génération Exemple Style-Tile C : "NØRD Studio"

> **Usage** : Copie ce document entier comme premier message dans une session Claude Code vierge.

---

## CONTEXTE

Tu travailles sur le **Brand Identity Generator (BIG)**, un système dans `.claude/skills/brand-identity/`.

Le pipeline génère des **style-tiles HTML** (fichiers self-contained avec CSS inline). Tu dois générer UN exemple de référence de qualité elite qui servira de standard pour les futures générations.

**IMPORTANT** : Cet exemple sera lu par des subagents LLM qui reproduiront inconsciemment sa structure. Chaque choix formel que tu fais ici sera amplifié. C'est pourquoi les contraintes structurelles ci-dessous sont NON-NÉGOCIABLES.

Cet exemple est le **C** d'une série de 3 — le plus audacieux (A=3, Rupture). Il doit repousser les limites du CSS moderne tout en restant fonctionnel.

---

## FICHIERS À LIRE AVANT DE COMMENCER

Lis ces fichiers dans cet ordre :

1. `.claude/skills/brand-identity/ref/html-showroom-spec.md` — **spec technique complète**, surtout :
   - Section 2 : structure du `:root` (7 catégories obligatoires)
   - Section 4 : triptyque Voice Block + Artefact + Atmosphere
   - Section 6 : **catalogue CSS moderne 2023-2026** (CRITIQUE — tu DOIS utiliser ces techniques)
2. `.claude/skills/brand-identity/ref/master-style-guide.md`
3. `.claude/skills/brand-identity/ref/bible-design-strategie.md` (curseurs A×B)
4. `.claude/skills/brand-identity/ref/output-framework-zone1.md`

NE PAS lire les exemples existants — tu pars de zéro.

---

## BRIEF FICTIF

**Marque** : NØRD Studio
**Secteur** : Studio de design digital — branding & design systems pour startups tech
**Cible** : Fondateurs tech, CTOs, VP Product de startups Series A-C
**Promesse** : "Ton brand n'est pas un logo — c'est un système. On construit l'infrastructure visuelle de ta croissance."
**Ton** : Direct, technique, confiant. Parle le langage des ingénieurs. Zéro bullshit créatif. Le design comme discipline d'ingénierie.
**Curseurs** : A=3 (Rupture) × B=3 (Contre-pied total)
**Tension de marque** : Radicalité créative × Rigueur d'ingénierie — l'audace d'un collectif d'artistes dans la méthode d'un cabinet de consulting

---

## CONTRAINTES STRUCTURELLES (NON-NÉGOCIABLES)

### Voice Block — Full-bleed superposition de layers
- Background SOMBRE (couleur depth)
- Texte GÉANT : le titre en `font-size: clamp(4rem, 10vw, 10rem)` — il doit dominer l'écran
- Éléments superposés en `position: absolute` :
  - Des lignes de grille en arrière-plan (pseudo-elements, `repeating-linear-gradient`, opacité très basse ~5%)
  - Un mot ou fragment en très grande taille, en arrière du titre principal, couleur très subtile (3-5% opacité)
- PAS de hero split, PAS de flex center simple, PAS de grid éditoriale propre
- L'effet visuel doit être BRUT, DENSE, SUPERPOSÉ — pas clean et aéré
- SVG noise filter en overlay pour la texture

### Artefact — Formulaire / Configurateur
- **PAS de cards** (zéro)
- **PAS de process steps / timeline / journey**
- **PAS de tableau de données**
- Un FAUX formulaire interactif : "Brand System Configurator"
  - Des champs inputs (désactivés visuellement mais réalistes) : nom de marque, secteur, positionnement
  - Des toggles CSS purs (checkbox cachée + label stylisé) : "Dark mode", "Variable fonts", "Motion system"
  - Des range/slider indicators en CSS pur (barres avec position) : "Brand Maturity", "Visual Density"
  - Des radio buttons stylisés pour choisir un "tier" : Starter / Growth / Enterprise
  - Un bouton submit "Generate System" en style accent
- Le tout dans un layout structuré (pas une seule colonne — utilise grid pour organiser les groupes de champs)
- Fond légèrement contrasté par rapport au surface principal

### Atmosphere Block — Split bicolore
- **PAS de fond uni** (ni sombre, ni clair)
- Layout en **2 colonnes** (grid ou flexbox) :
  - Colonne gauche : couleur primaire (ou depth), texte manifesto en couleur claire
  - Colonne droite : couleur accent ou surface contrastée, infos pratiques (contact, liens)
- OU : `clip-path` diagonal séparant les 2 zones de couleur
- Le contraste entre les 2 moitiés doit être FORT (pas 2 nuances proches)

### Radius
- **0px partout** — brutalisme, angles vifs
- Les inputs du formulaire aussi : sharp
- Les toggles : exception autorisée (`border-radius: 9999px` sur les pills/toggles uniquement)

### Shadows
- **PAS de drop shadows classiques** (`0 Npx Npx rgba(...)`)
- Utilise UNIQUEMENT :
  - `box-shadow: inset ...` (ombres internes, effet embossé/debossed)
  - `box-shadow: 0 0 Npx color` (glow, halo)
  - Ou AUCUNE shadow (flat brutal)

### Hover & interactions
- **INTERDIT : `transform: translateY()`**
- **INTERDIT : `transform: scale()`**
- Hover sur les toggles/radios : `background-color` change
- Hover sur le bouton submit : `clip-path` morph (ex: `clip-path: inset(2px)` → `clip-path: inset(0)`) OU `box-shadow: inset` change
- Hover sur les liens atmosphere : `color` + `letter-spacing` change (micro-expansion)

### CSS Moderne (minimum 8 techniques — c'est le niveau Rupture)
- [ ] `oklch()` : TOUTE la palette en oklch, zéro hex
- [ ] `@layer reset, tokens, components, utilities`
- [ ] `@property` : au moins 2 custom properties typées — ex: `--hue` (type `<number>`, animée dans un keyframe pour un shift chromatique subtil) + `--grid-opacity` (type `<number>`)
- [ ] `text-wrap: balance` sur les titres, `text-wrap: pretty` sur les paragraphes
- [ ] `color-mix(in oklch, ...)` pour les variantes
- [ ] `clip-path` : sur l'atmosphere block (split) ET/OU sur les hover states
- [ ] `animation-timeline: view()` : scroll-reveal sur les éléments du formulaire (apparition progressive au scroll)
- [ ] `@starting-style` : état initial pour les transitions d'entrée
- [ ] SVG noise filter (`feTurbulence`) pour le grain

### Fonts
- Choisis dans le **pool A=3** de html-showroom-spec.md §3
- **INTERDIT** : Instrument Serif, IBM Plex Mono, Syne, Bricolage Grotesque, Fraunces, Space Grotesk, Young Serif, Inter, DM Sans, et TOUTES les fonts des exemples A et B (Cormorant, Barlow, Crimson Pro, Instrument Sans, Gloock, Epilogue — ou quelles que soient les fonts choisies dans A et B, ne les réutilise pas)
- Pour le body : une font MONO est recommandée (cohérent avec le positionnement "ingénierie du design")
- Cherche un display EXPÉRIMENTAL — le pool A=3 contient des options radicales

---

## GATES DE VALIDATION

Vérifie CHAQUE gate avant de finaliser :

- [ ] **Screenshot Test** : zéro donnée technique visible en texte
- [ ] **Mason's Rule** : zéro scaffolding
- [ ] **Zero Dead Code** : chaque @keyframes et custom property utilisés
- [ ] **CSS Moderne** : min 8 techniques cochées ci-dessus
- [ ] **Anti-card** : AUCUN élément type card
- [ ] **Anti-translateY** : `translateY` n'apparaît NULLE PART
- [ ] **Anti-scale** : `scale` n'apparaît NULLE PART en hover
- [ ] **Anti-drop-shadow** : aucune shadow de type `0 Npx Npx rgba(0,0,0,...)` — uniquement inset ou glow
- [ ] **Couverture :root** : 7 catégories oklch
- [ ] **Self-contained** : tout dans `<style>`
- [ ] **Full-bleed hero** : le voice-block a un texte géant et des éléments superposés en absolute
- [ ] **Formulaire** : l'artefact est un faux configurateur avec inputs, toggles, sliders, radios
- [ ] **Split atmosphere** : l'atmosphere a 2 zones de couleur distinctes
- [ ] **animation-timeline** : au moins une animation scroll-driven
- [ ] **@starting-style** : au moins un usage
- [ ] **SVG noise** : filtre grain présent
- [ ] **Qualité elite** : visuellement impressionnant et RADICAL dans Chrome

---

## FICHIER DE SORTIE

Écris le fichier dans :
```
.claude/skills/brand-identity/examples/rupture/style-tile-example-C.html
```

Puis ouvre-le :
```bash
open .claude/skills/brand-identity/examples/rupture/style-tile-example-C.html
```

Présente-moi un résumé : fonts choisies, palette, techniques CSS utilisées, et si tous les gates passent.
