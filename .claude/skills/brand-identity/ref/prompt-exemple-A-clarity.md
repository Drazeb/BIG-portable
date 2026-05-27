# Prompt — Génération Exemple Style-Tile A : "Clarity Analytics"

> **Usage** : Copie ce document entier comme premier message dans une session Claude Code vierge.

---

## CONTEXTE

Tu travailles sur le **Brand Identity Generator (BIG)**, un système dans `.claude/skills/brand-identity/`.

Le pipeline génère des **style-tiles HTML** (fichiers self-contained avec CSS inline). Tu dois générer UN exemple de référence de qualité elite qui servira de standard pour les futures générations.

**IMPORTANT** : Cet exemple sera lu par des subagents LLM qui reproduiront inconsciemment sa structure. Chaque choix formel que tu fais ici sera amplifié. C'est pourquoi les contraintes structurelles ci-dessous sont NON-NÉGOCIABLES.

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

**Marque** : Clarity Analytics
**Secteur** : SaaS B2B — plateforme d'analytics financiers pour PME
**Cible** : CFOs, directeurs financiers, ops managers de PME 50-500 employés
**Promesse** : "La clarté dans vos données — chaque décision financière, éclairée"
**Ton** : Professionnel, sobre, précis. Pas froid — confiant et rassurant. Zéro jargon tech.
**Curseurs** : A=1 (Prudent) × B=2 (Positionnement décalé)
**Tension de marque** : Rigueur × Accessibilité — la puissance d'un outil enterprise dans la simplicité d'un produit consumer

---

## CONTRAINTES STRUCTURELLES (NON-NÉGOCIABLES)

### Voice Block — Centré pur typographique
- Layout : `display: flex; flex-direction: column; align-items: center; justify-content: center`
- PAS de split (gauche/droite), PAS de grid multi-colonnes, PAS d'image
- Le titre H1 en display font, centré, taille généreuse (clamp)
- Un sous-titre d'une ligne, un CTA
- Fond CLAIR (la couleur surface principale)
- L'impact vient de la TAILLE de la typo et de l'ESPACE NÉGATIF autour
- Éléments décoratifs subtils autorisés (lignes fines, formes géométriques en pseudo-elements)

### Artefact — Tableau de données / Data dashboard
- **PAS de cards** (zéro élément box + padding + radius + shadow + hover translateY)
- **PAS de "process steps"** ou "journey"
- Un VRAI tableau de données financières : lignes, colonnes, headers, cellules avec données numériques
- Badges de statut inline (positif/négatif/neutre)
- Sparklines en CSS pur (petites barres ou lignes de tendance via gradient ou pseudo-elements)
- Des KPI en en-tête (chiffres gros, labels petits)
- Penser : spreadsheet premium, pas dashboard SaaS générique
- Utilise `mask-image` pour un fondu progressif en bas du tableau (illusion de continuité)

### Atmosphere Block — Claire et texturée
- **PAS de fond sombre** — fond clair (crème, blanc cassé, ou surface-alt)
- Texture via SVG noise filter (`feTurbulence`) en très basse opacité (~2-3%)
- Accent de couleur uniquement en typographie (le manifesto en couleur primaire ou accent)
- Minimaliste : peu d'éléments, beaucoup d'espace
- Footer sobre avec liens fictifs

### Radius
- **0px partout** — philosophie chirurgicale, zéro arrondi
- Les tableaux, les conteneurs, les badges : tous sharp

### Shadows
- **Aucune shadow portée** (`box-shadow: none` ou absent)
- Élévation exprimée uniquement par : bordures fines (1px), backgrounds contrastés, ou espacement
- Philosophie "flat premium" — la hiérarchie vient de la couleur et de la typo, pas de la profondeur

### Hover & interactions
- **INTERDIT : `transform: translateY()`** — nulle part dans le fichier
- **INTERDIT : `transform: scale()`**
- Hover sur les lignes du tableau : `background-color` change (highlight subtil)
- Hover sur le CTA : `border-color` shift + `color` change
- Transitions fluides (300ms ease)

### CSS Moderne (minimum 7 techniques)
- [ ] `oklch()` : TOUTE la palette en oklch, zéro hex
- [ ] `@layer reset, tokens, components, utilities`
- [ ] `@property` : au moins 1 custom property typée et animée (ex: `--accent-lightness` type `<number>`)
- [ ] `text-wrap: balance` sur les titres, `text-wrap: pretty` sur les paragraphes
- [ ] `color-mix(in oklch, ...)` pour les variantes hover
- [ ] `mask-image` : fondu en bas du tableau
- [ ] Logical properties : `margin-block`, `padding-inline`, `max-inline-size`

### Fonts
- Choisis dans le **pool A=1** de html-showroom-spec.md §3
- **INTERDIT** : Fraunces, Inter, Cormorant, Barlow, Crimson Pro, Instrument Sans, Gloock, Epilogue, Lora, DM Sans, Playfair Display, Montserrat, Poppins
- Cherche des pairings INHABITUELS mais lisibles — le pool A=1 a 50+ options

---

## GATES DE VALIDATION

Vérifie CHAQUE gate avant de finaliser :

- [ ] **Screenshot Test** : zéro donnée technique visible (pas de HEX, pas de noms de fonts en texte)
- [ ] **Mason's Rule** : zéro scaffolding ("Section 02", labels techniques)
- [ ] **Zero Dead Code** : chaque @keyframes utilisé, chaque custom property référencée
- [ ] **CSS Moderne** : min 7 techniques cochées ci-dessus
- [ ] **Anti-card** : AUCUN élément type card (box + padding + radius + shadow + hover translateY)
- [ ] **Anti-translateY** : `translateY` n'apparaît NULLE PART dans le fichier
- [ ] **Couverture :root** : 7 catégories (palette oklch, typo, type-scale, spacing, radius, shadows, transitions)
- [ ] **Self-contained** : tout dans `<style>`, Google Fonts via `<link>` avec preconnect
- [ ] **Atmosphere claire** : le fond de l'atmosphere block N'EST PAS sombre
- [ ] **Masque sur tableau** : `mask-image` est utilisé sur la section artefact
- [ ] **Qualité elite** : le résultat est visuellement impressionnant dans Chrome

---

## FICHIER DE SORTIE

Écris le fichier dans :
```
.claude/skills/brand-identity/examples/standard/style-tile-example-A.html
```

Puis ouvre-le :
```bash
open .claude/skills/brand-identity/examples/standard/style-tile-example-A.html
```

Présente-moi un résumé : fonts choisies, palette, techniques CSS utilisées, et si tous les gates passent.
