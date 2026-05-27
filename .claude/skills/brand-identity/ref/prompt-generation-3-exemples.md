# Prompt — Génération de 3 Exemples Style-Tile Structurellement Différents

> **Usage** : Copie ce document entier comme premier message dans une session Claude Code vierge.
> **Durée estimée** : Long — 3 fichiers HTML de ~800 lignes chacun, générés séquentiellement.

---

## CONTEXTE

Tu travailles sur le **Brand Identity Generator (BIG)**, un système dans `.claude/skills/brand-identity/`.

Le pipeline génère des **style-tiles HTML** (fichiers self-contained). Le problème : le subagent qui génère les style-tiles lit un UNIQUE exemple et en reproduit inconsciemment la structure (layout des cards, type de hero, pattern de shadows, architecture des composants). Résultat : ~65-70% d'ADN structurel identique entre les outputs.

**Ta mission** : Générer **3 exemples HTML de référence** de qualité elite, pour 3 briefs fictifs différents, avec des **structures radicalement opposées**. Ces 3 exemples remplaceront les exemples actuels et serviront de standard qualité pour les futures générations.

---

## FICHIERS À LIRE AVANT DE COMMENCER

Lis ces fichiers DANS CET ORDRE (c'est critique pour comprendre le système) :

1. `.claude/skills/brand-identity/ref/html-showroom-spec.md` — **la spec technique complète**, surtout :
   - Section 2 : structure du `:root` (7 catégories obligatoires)
   - Section 4 : triptyque Voice Block + Artefact + Atmosphere
   - Section 6 : **catalogue CSS moderne** (techniques 2023-2026)
2. `.claude/skills/brand-identity/ref/master-style-guide.md` — le guide de style
3. `.claude/skills/brand-identity/ref/bible-design-strategie.md` — la bible design (curseurs A×B)
4. `.claude/skills/brand-identity/ref/output-framework-zone1.md` — les règles du showroom
5. **Exemples ACTUELS** (lis les 3 pour comprendre le niveau de qualité, puis **OUBLIE leur structure** — tes nouveaux exemples doivent être radicalement différents) :
   - `.claude/skills/brand-identity/examples/standard/style-tile-example-A.html` (Clarity Analytics, A=1)
   - `.claude/skills/brand-identity/examples/standard/style-tile-example-B.html` (Maison Solène, A=2)
   - `.claude/skills/brand-identity/examples/rupture/style-tile-example-C.html` (NØRD Studio, A=3)

---

## LES 3 EXEMPLES À GÉNÉRER

### EXEMPLE A — "Clarity Analytics" (A=1, B=2 — Prudent/Décalé)
**Brief fictif** : SaaS B2B d'analytics pour PME. Cible : CFOs et ops managers. Promesse : "la clarté dans vos données". Secteur : fintech/data.

**CONTRAINTES STRUCTURELLES OBLIGATOIRES :**

| Dimension | Contrainte |
|-----------|------------|
| **Voice Block** | **Centré pur typographique** — flex center, PAS de split, PAS de grid. Le titre et un CTA, c'est tout. Fond clair. Impact par la TAILLE de la typo et l'espace négatif. |
| **Artefact** | **Tableau de données / data dashboard** — PAS de cards, PAS de steps/process. Un VRAI tableau avec lignes, colonnes, badges de statut, sparklines en CSS. Penser : spreadsheet premium. |
| **Atmosphere** | **Claire et texturée** — PAS de fond sombre. Fond clair avec texture SVG noise subtile. Accent coloré en typographie. Minimaliste. |
| **Radius** | **0px partout** — philosophie sharp, chirurgicale |
| **Shadows** | **Aucune shadow portée** — élévation par bordures fines et backgrounds contrastés |
| **Hover** | **border-color shift + background-color** — INTERDIT translateY, INTERDIT scale |
| **CSS moderne min.** | oklch, @layer, @property (animer une custom property couleur), text-wrap, color-mix, `mask-image` (fondu sur le tableau) |
| **Fonts (pool A=1)** | Choisir dans le pool A=1 de html-showroom-spec.md §3. NE PAS utiliser Fraunces, Inter, Cormorant, Barlow, Crimson Pro, Gloock, Epilogue, Instrument Sans. |

---

### EXEMPLE B — "Maison Solène" (A=2, B=3 — Décalé/Contre-pied)
**Brief fictif** : Maison d'édition indépendante spécialisée en essais et littérature contemporaine. Cible : lecteurs exigeants 30-55 ans. Promesse : "chaque livre est une position". Secteur : édition/culture.

**CONTRAINTES STRUCTURELLES OBLIGATOIRES :**

| Dimension | Contrainte |
|-----------|------------|
| **Voice Block** | **Diagonale / clip-path** — la section est coupée en diagonal via `clip-path: polygon()`. Le texte est positionné de manière asymétrique. Fond avec gradient radial. |
| **Artefact** | **Timeline verticale** — PAS de cards, PAS de grille. Une VRAIE timeline avec ligne centrale, points, contenu alternant gauche/droite. Penser : chronologie éditoriale (livres publiés). |
| **Atmosphere** | **Gradient immersif chaud** — gradient multi-stops (3+ couleurs), PAS de fond sombre uni. Texte en overlay avec blend-mode. |
| **Radius** | **Mixte : 0px sur les conteneurs, full-round sur les accents** (badges, dots) |
| **Shadows** | **Ombres colorées teintées** — pas de rgba noir, utiliser oklch de la couleur primaire avec alpha |
| **Hover** | **scale(1.02) + filter brightness** — INTERDIT translateY |
| **CSS moderne min.** | oklch, @layer, @property, text-wrap, color-mix, `clip-path` (section transition), `@container` (timeline items adaptatifs) |
| **Fonts (pool A=2)** | Choisir dans le pool A=2. NE PAS utiliser les fonts listées ci-dessus pour l'Exemple A. NE PAS utiliser Fraunces, Space Grotesk, Young Serif, DM Sans, Source Sans 3. |

---

### EXEMPLE C — "NØRD Studio" (A=3, B=3 — Rupture/Contre-pied)
**Brief fictif** : Studio de design digital spécialisé en branding pour startups tech. Cible : fondateurs tech et CTOs. Promesse : "ton brand n'est pas un logo, c'est un système". Secteur : agence créative/tech.

**CONTRAINTES STRUCTURELLES OBLIGATOIRES :**

| Dimension | Contrainte |
|-----------|------------|
| **Voice Block** | **Full-bleed superposition de layers** — texte GÉANT (clamp 8vw+), background sombre, éléments en position absolute qui se chevauchent. Lignes de grille visibles en fond (pseudo-elements). PAS de hero split. |
| **Artefact** | **Formulaire / configurateur interactif** — PAS de cards, PAS de process steps, PAS de timeline. Un FAUX formulaire (inputs désactivés) de type "configurateur de brand" avec des champs, des toggles CSS, des range indicators. |
| **Atmosphere** | **Split bicolore** — moitié gauche et moitié droite de couleurs différentes via grid 2 colonnes ou clip-path. PAS un fond uni. |
| **Radius** | **0px** — brutaliste, sharp absolu |
| **Shadows** | **Inset shadows ou glow** — PAS de drop shadows classiques. `box-shadow: inset ...` ou `0 0 Npx color` |
| **Hover** | **clip-path morph + background-color** — INTERDIT translateY, INTERDIT scale |
| **CSS moderne min.** | oklch, @layer, @property (animer --hue), text-wrap, color-mix, `clip-path` (hover + section), `animation-timeline: view()` (scroll-reveal), `@starting-style` (entry animations), SVG noise |
| **Fonts (pool A=3)** | Choisir dans le pool A=3. NE PAS utiliser Instrument Serif, IBM Plex Mono, Syne, Bricolage Grotesque, ni aucune font des Exemples A et B. |

---

## PROCESSUS DE GÉNÉRATION

### Ordre obligatoire : A → B → C

Génère les exemples **séquentiellement**, pas en parallèle :

1. **Génère l'Exemple A** → écris le fichier → vérifie les gates
2. **Génère l'Exemple B** → AVANT de coder, relis l'Exemple A et vérifie que ta structure est RADICALEMENT différente (différent layout, différent composant, différent hover, différente atmosphere). Puis écris le fichier → vérifie les gates.
3. **Génère l'Exemple C** → AVANT de coder, relis les Exemples A ET B et vérifie que ta structure n'a RIEN en commun avec eux. Puis écris le fichier → vérifie les gates.

### Pour chaque exemple :

**Étape 1 — Brief & tokens**
- Invente un brief réaliste (3-4 phrases) pour la marque fictive
- Définis la palette en oklch (min 8 couleurs), les fonts, le type-scale ratio
- Définis les radius, shadows, spacing, transitions

**Étape 2 — Génération HTML**
- Fichier HTML self-contained (tout le CSS dans `<style>`)
- Google Fonts via `<link>` avec preconnect
- CSS organisé en `@layer reset, tokens, components, utilities`
- Palette en `oklch()` exclusivement dans le `:root`
- Le fichier doit être visuellement IMPRESSIONNANT dans un navigateur Chrome/Safari
- Contenu fictif RÉALISTE et aligné avec le brief

**Étape 3 — Vérification gates**
Vérifie CHAQUE gate avant de passer à l'exemple suivant :
- [ ] **Screenshot Test** : zéro donnée technique visible (pas de HEX, pas de noms de fonts en texte)
- [ ] **Mason's Rule** : zéro scaffolding ("Section 02", labels techniques)
- [ ] **Zero Dead Code** : chaque @keyframes utilisé, chaque custom property référencée
- [ ] **CSS Moderne** : min 6 techniques de la section 6 de html-showroom-spec.md
- [ ] **Contrainte structurelle** : CHAQUE contrainte du tableau est respectée
- [ ] **Anti-card** : AUCUN élément ne ressemble à une "card SaaS" (box + radius + shadow + hover translateY)
- [ ] **Anti-pattern hover** : AUCUN `transform: translateY()` dans le fichier
- [ ] **Couverture :root** : les 7 catégories (palette, typo, type-scale, spacing, radius, shadows, transitions)
- [ ] **Self-contained** : tout dans `<style>`, Google Fonts via `<link>`
- [ ] **Diversité inter-exemples** : si Exemple B ou C, la structure est RADICALEMENT différente des précédents

---

## ANTI-PATTERNS — INTERDIT DANS LES 3 EXEMPLES

Ces patterns ont été identifiés comme les biais par défaut du LLM. Ils sont **INTERDITS** :

1. **La "card SaaS"** : box avec padding + border-radius 8-16px + shadow-md + hover translateY(-Npx). C'EST LE PATTERN LE PLUS INTERDIT. Si tu te retrouves à coder ça, ARRÊTE et repense ton composant.

2. **`transform: translateY(-Npx)`** au hover. Interdit dans les 3 exemples. Utilise : border-color, background-color, filter, scale, clip-path, opacity, ou toute autre approche.

3. **Grille 3 colonnes de cards identiques** pour l'artefact. Chaque artefact a un TYPE de composant différent (tableau, timeline, formulaire) et une FORME différente.

4. **Atmosphere block = fond sombre uni**. Maximum 1 des 3 exemples peut avoir un fond sombre. Les 2 autres DOIVENT être différents (clair texturé, gradient, split bicolore).

5. **Hero split** (texte à gauche, espace/image à droite). Maximum 0 des 3 exemples — aucun n'utilise ce layout pour le voice-block.

6. **Process steps / journey steps** comme artefact. Maximum 1 des 3 exemples — les 2 autres doivent être un TYPE DE COMPOSANT fondamentalement différent.

7. **CSS sans clip-path ni mask-image**. Au moins 2 des 3 exemples DOIVENT utiliser clip-path ou mask-image.

---

## FICHIERS DE SORTIE

Écris chaque fichier dans :
```
.claude/skills/brand-identity/examples/standard/style-tile-example-A.html
.claude/skills/brand-identity/examples/standard/style-tile-example-B.html
.claude/skills/brand-identity/examples/rupture/style-tile-example-C.html
```

(A et B dans `standard/` car A=1 et A=2, C dans `rupture/` car A=3)

Après avoir généré les 3, **ouvre-les dans le navigateur** :
```bash
open .claude/skills/brand-identity/examples/standard/style-tile-example-A.html
open .claude/skills/brand-identity/examples/standard/style-tile-example-B.html
open .claude/skills/brand-identity/examples/rupture/style-tile-example-C.html
```

Puis **présente-moi la matrice de diversité** pour que je valide :

| Dimension | Exemple A | Exemple B | Exemple C |
|-----------|-----------|-----------|-----------|
| Voice Block | centré typo | diagonale clip-path | full-bleed layers |
| Artefact | tableau data | timeline verticale | formulaire/config |
| Atmosphere | claire texturée | gradient immersif | split bicolore |
| Radius | 0px sharp | mixte (0 + full) | 0px brutaliste |
| Shadows | aucune (bordures) | colorées teintées | inset / glow |
| Hover | border-color | scale + filter | clip-path morph |
| Palette | froide (bleu/gris) | chaude (ambre/terre) | saturée (contrastes forts) |
| Fonts | serif classique + sans | serif éditoriale + sans | display expérimental + mono |
| CSS signature | mask-image | clip-path + @container | animation-timeline + @starting-style |
