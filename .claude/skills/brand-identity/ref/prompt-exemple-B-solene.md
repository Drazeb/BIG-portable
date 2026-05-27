# Prompt — Génération Exemple Style-Tile B : "Maison Solène"

> **Usage** : Copie ce document entier comme premier message dans une session Claude Code vierge.

---

## CONTEXTE

Tu travailles sur le **Brand Identity Generator (BIG)**, un système dans `.claude/skills/brand-identity/`.

Le pipeline génère des **style-tiles HTML** (fichiers self-contained avec CSS inline). Tu dois générer UN exemple de référence de qualité elite qui servira de standard pour les futures générations.

**IMPORTANT** : Cet exemple sera lu par des subagents LLM qui reproduiront inconsciemment sa structure. Chaque choix formel que tu fais ici sera amplifié. C'est pourquoi les contraintes structurelles ci-dessous sont NON-NÉGOCIABLES.

Cet exemple est le **B** d'une série de 3 exemples radicalement différents. Les contraintes ci-dessous garantissent qu'il n'a RIEN en commun structurellement avec les exemples A et C.

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

**Marque** : Maison Solène
**Secteur** : Édition indépendante — essais, littérature contemporaine, poésie
**Cible** : Lecteurs exigeants 30-55 ans, littéraires, intellectuels curieux, libraires indépendants
**Promesse** : "Chaque livre est une position — pas un produit, un acte éditorial"
**Ton** : Cultivé, affirmé, chaleureux sans être familier. L'érudition sans le pédantisme.
**Curseurs** : A=2 (Décalé) × B=3 (Contre-pied total)
**Tension de marque** : Exigence intellectuelle × Chaleur humaine — la rigueur d'un éditeur académique dans la sensibilité d'un artisan du livre

---

## CONTRAINTES STRUCTURELLES (NON-NÉGOCIABLES)

### Voice Block — Diagonale / clip-path
- La section utilise `clip-path: polygon()` pour créer une coupe diagonale en bas (ex: `polygon(0 0, 100% 0, 100% 85%, 0 100%)`)
- Le texte est positionné de manière ASYMÉTRIQUE (pas centré, pas en grille symétrique) — utilise padding-inline-start plus grand que padding-inline-end, ou position le contenu à gauche avec le côté droit vide
- Background : gradient radial (pas linéaire simple) — au moins 2 couleurs avec une zone de lumière décentrée
- Le titre H1 en display font, grande taille, avec une ligne en italique pour la chaleur
- PAS de hero split classique, PAS de flex center

### Artefact — Timeline verticale
- **PAS de cards** (zéro élément box + padding + radius + shadow + hover translateY)
- **PAS de grille** (ni 2 colonnes, ni 3 colonnes)
- **PAS de "process steps"** linéaires
- Une VRAIE timeline verticale avec :
  - Une ligne centrale (pseudo-element, 1-2px, couleur accent)
  - Des points/dots sur la ligne (border-radius: 50%)
  - Du contenu alternant gauche/droite le long de la timeline
  - Contenu = livres publiés fictifs (titre, auteur, court extrait, année)
  - La timeline doit raconter une histoire éditoriale (2018 → 2026)
- Utilise `@container` : chaque item de timeline est un container, et le layout interne s'adapte

### Atmosphere Block — Gradient immersif chaud
- **PAS de fond sombre uni** — background gradient multi-stops (min 3 couleurs chaudes)
- Le texte en overlay avec `mix-blend-mode` (difference, overlay, ou soft-light — ce qui est lisible)
- Manifesto poétique — dans le ton d'un éditeur passionné
- Peut avoir un léger noise/grain SVG en overlay sur le gradient

### Radius
- **Mixte** : 0px sur les conteneurs/sections, `border-radius: 50%` ou `9999px` sur les accents (dots timeline, badges)
- Pas de 8px/16px générique

### Shadows
- **Ombres colorées teintées** — pas de `rgba(0,0,0,...)`, utilise `oklch(primary / alpha)` pour les ombres
- Nombre de niveaux libre (2-3 suffisent)
- Les ombres doivent avoir une TEINTE visible, pas juste du noir transparent

### Hover & interactions
- **INTERDIT : `transform: translateY()`** — nulle part dans le fichier
- Hover sur les items timeline : `transform: scale(1.02)` + `filter: brightness(1.05)`
- Hover sur le CTA : background-color change avec transition
- Les dots de la timeline : scale au hover

### CSS Moderne (minimum 7 techniques)
- [ ] `oklch()` : TOUTE la palette en oklch, zéro hex
- [ ] `@layer reset, tokens, components, utilities`
- [ ] `@property` : au moins 1 custom property typée et animée (ex: `--glow-hue` type `<angle>` pour un glow animé)
- [ ] `text-wrap: balance` sur les titres, `text-wrap: pretty` sur les paragraphes
- [ ] `color-mix(in oklch, ...)` pour les variantes hover et les ombres
- [ ] `clip-path` : coupe diagonale du voice-block
- [ ] `@container` : items de timeline adaptatifs

### Fonts
- Choisis dans le **pool A=2** de html-showroom-spec.md §3
- **INTERDIT** : Fraunces, Space Grotesk, Young Serif, DM Sans, Source Sans 3, Inter, Cormorant, Barlow, Crimson Pro, Instrument Sans, Gloock, Epilogue, Playfair Display
- Cherche un pairing avec PERSONNALITÉ — un display qui a du caractère éditorial

---

## GATES DE VALIDATION

Vérifie CHAQUE gate avant de finaliser :

- [ ] **Screenshot Test** : zéro donnée technique visible
- [ ] **Mason's Rule** : zéro scaffolding
- [ ] **Zero Dead Code** : chaque @keyframes et custom property utilisés
- [ ] **CSS Moderne** : min 7 techniques cochées ci-dessus
- [ ] **Anti-card** : AUCUN élément type card
- [ ] **Anti-translateY** : `translateY` n'apparaît NULLE PART dans le fichier
- [ ] **Couverture :root** : 7 catégories oklch
- [ ] **Self-contained** : tout dans `<style>`
- [ ] **clip-path** : le voice-block a une coupe diagonale via clip-path
- [ ] **Timeline** : l'artefact est une timeline verticale avec ligne centrale et contenu alternant
- [ ] **@container** : utilisé sur les items de timeline
- [ ] **Gradient atmosphere** : le fond de l'atmosphere est un gradient multi-stops, PAS un fond uni
- [ ] **Ombres teintées** : les shadows ont une teinte visible (pas du noir pur)
- [ ] **Qualité elite** : visuellement impressionnant dans Chrome

---

## FICHIER DE SORTIE

Écris le fichier dans :
```
.claude/skills/brand-identity/examples/standard/style-tile-example-B.html
```

Puis ouvre-le :
```bash
open .claude/skills/brand-identity/examples/standard/style-tile-example-B.html
```

Présente-moi un résumé : fonts choisies, palette, techniques CSS utilisées, et si tous les gates passent.
