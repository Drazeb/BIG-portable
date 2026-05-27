# Design Principles — Phase 4 Style-Tile Generation

10 principes opérationnels. Le subagent DOIT les appliquer lors de la génération HTML/CSS.
Ces principes s'appliquent au triptyque Voice Block + Artefact Témoin + Atmosphere Block.

---

## 1. Contraste Interactif

**Rule** : Chaque CTA/bouton DOIT contraster avec son fond immédiat. JAMAIS même couleur.

**Measurable** : Le bouton doit être identifiable en 0.5s sur un screenshot flouté (squint test).

**Anti-patterns** :
- CTA `--color-accent` sur gradient qui finit en `--color-accent`
- CTA `--color-primary` sur fond `--color-primary-dark` (trop proche)
- Bouton blanc sur fond `--color-surface` (invisible)

## 2. Cohérence Tonale

**Rule** : Sections adjacentes partagent la même température de couleur. Max 1 transition warm↔cool entre les 3 sections.

**Measurable** : Voice Block↔Artefact et Artefact↔Atmosphere = même famille (warm→warm OU cool→cool). 1 transition autorisée.

**Anti-patterns** :
- Voice Block chaud (terracotta) → Artefact froid (gris bleuté) → Atmosphere chaude = 2 transitions = trop
- Transition brutale dark→light sans gradient intermédiaire entre sections

## 3. Hiérarchie Visuelle

**Rule** : 1 point focal par section. Ordre de dominance : Taille > Poids > Couleur > Position.

**Measurable** : En floutant la section, un seul élément reste lisible : Voice Block = H1, Artefact = titre du composant, Atmosphere = quote ou manifesto.

**Anti-patterns** :
- 2 éléments de même taille en compétition (double heading)
- Tout en gras = rien en gras
- Point focal en bas à droite (contre le F-pattern naturel)

## 4. Whitespace & Rythme

**Rule** : Les 3 sections du triptyque DOIVENT avoir des padding-block DIFFÉRENTS. Alterner sections denses et aérées.

**Measurable** : Aucune paire de sections ne partage le même padding-block. Le Voice Block est le plus immersif (min-block-size: 100vh ou padding généreux).

**Anti-patterns** :
- 3× `var(--space-2xl)` sur les 3 sections
- Voice Block et Artefact avec le même espacement → monotonie

## 5. Palette & Usage Couleur

**Rule** : 4 rôles max dans le CSS : primary (identité), accent (action), surface (fond), depth (fond sombre). Chaque couleur = 1 seul job sémantique.

**Measurable** : Chaque couleur du `:root` est utilisée pour un seul rôle. Pas de `--color-primary` à la fois comme fond ET texte ET bouton dans la même section.

**Anti-patterns** :
- `--color-accent` sur plus de 3 éléments par viewport
- Couleurs hardcodées hors palette (hex au lieu de `var(--color-*)`)
- Même couleur pour deux rôles différents

## 6. Typographie & Échelle

**Rule** : 2 familles max (display + body). Weight = hiérarchie (700 titres, 400 body). Overlines : uppercase + letter-spacing 0.12-0.15em.

**Measurable** : L'échelle typographique utilise les variables `--text-*` du `:root`. Pas de `font-size` hardcodé.

**Anti-patterns** :
- 3+ familles de polices
- Body text en font-weight 600+ (fatigue visuelle)
- Overlines sans letter-spacing (pas d'air)

## 7. Accessibilité Contraste

**Rule** : Texte normal ≥ 4.5:1. Grand texte (≥18px bold ou ≥24px) ≥ 3:1. WCAG AA minimum.

**Measurable** : `--color-text-secondary` sur fond coloré passe le ratio 4.5:1.

**Anti-patterns** :
- Texte gris clair sur fond blanc (#999 sur #fff = 2.8:1)
- Texte `--color-text-on-depth` sur fond `--color-primary` sans vérification ratio
- Placeholder text à peine visible

## 8. Voice Block Impact

**Rule** : Le Voice Block est autonome et lisible sans scroll. Le H1 et au moins 1 CTA sont visibles sur un viewport 1440×900.

**Measurable** : min-block-size: 100vh (ou équivalent). Le contenu principal ne déborde pas sous le fold.

**Anti-patterns** :
- Voice Block trop haut → CTA invisible sans scroll
- Padding excessif qui pousse le H1 trop bas
- Image ou forme décorative qui prend tout l'espace au détriment du texte

## 9. Data Visualisation (conditionnel — si l'artefact contient des données)

**Rule** : Data-ink ratio maximal (Tufte). Pas de chartjunk. Couleurs `--color-dataviz-*` dédiées.

**Measurable** : Chaque pixel d'encre porte de l'information. Pas de gradient décoratif sur les barres/métriques.

**Anti-patterns** :
- Ombres portées sur les barres de progression
- Couleurs primary/accent réutilisées pour la dataviz (collision sémantique)
- 3D effect sur des métriques plates

## 10. Affordance Cognitive

**Rule** : L'apparence prédit l'interaction. Boutons = pressables (shadow, border-radius, couleur accent). Liens = soulignement ou couleur. Cards avec hover = cursor:pointer + feedback visuel.

**Measurable** : Un utilisateur novice identifie les éléments cliquables sans hésiter.

**Anti-patterns** :
- Texte qui ressemble à un lien mais n'est pas cliquable
- Card sans hover state (pas de feedback d'interaction)
- Bouton flat sans distinction du texte environnant
