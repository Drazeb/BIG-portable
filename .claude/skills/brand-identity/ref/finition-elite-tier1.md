# Finition Élite — TIER 1 (structurantes)

Ce fichier contient les **règles de finition structurantes** qui doivent guider le Designer Phase 4 dès la conception. Pour les détails (ombres ≥2 niveaux, easing nommés, multi-property hover, rythme spacing, retenue hovers, techniques avancées quota), voir `finition-elite-core.md` — lus uniquement par le Critique en aval.

**Portée** : importé par Phase 4 (styletile + artefact), Batch 2, Batch 3.

---

## Palette et couleur

- 1 seul accent couleur par concept — l'accent est un ÉVÉNEMENT visuel (1-2 éléments par viewport maximum). Le reste vit dans la famille de la couleur dominante.
- Pas de pur noir (`#000000`) ni pur blanc (`#ffffff`) sur les surfaces principales — utiliser off-black/off-white avec teinte subtile.
- **Neutres tintés** : les neutres (gris, fonds, texte secondaire) sont légèrement teintés vers la teinte dominante du concept, jamais purement chromatiquement neutres. Cette parenté crée la cohésion subconsciente entre accent et neutre, sans verrouiller leur identité visuelle.

## Système typographique

L'identité typographique repose sur une **échelle modulaire courte** (autour de 5 niveaux distincts, pas une succession serrée) avec un **ratio de contraste franc entre niveaux** — la hiérarchie doit se lire au premier coup d'œil. Multiplier les tailles intermédiaires dilue la lecture et trahit l'absence de système.

## Système d'espacement

L'espacement repose sur une **grille modulaire à pas constant** avec **nommage sémantique** (`--space-sm`, `--space-md`, `--space-lg`, etc.), pas une succession de valeurs ad hoc.

L'espacement entre éléments fraternels passe par `gap` (sur le conteneur), pas par `margin-top`/`margin-bottom` sur chaque enfant — la cohérence du rythme appartient au parent, pas aux enfants.

## CSS moderne — socle obligatoire

Quel que soit le curseur, le `:root` et le code utilisent :
- `oklch()` pour la palette (pas de HSL)
- `@layer` pour organiser le CSS
- `@property` pour les custom properties animables
- `color-mix()` pour les variations
- `text-wrap: balance` sur headings, `text-wrap: pretty` sur paragraphes
- `clamp()` pour les tailles fluides

Ce socle n'est pas de l'audace — c'est le standard de fabrication 2026.

## Couche graphique constitutive

CHAQUE section a de la profondeur de surface :
- Grain SVG tuilé (background-size: 150px, blend-mode soft-light, opacity 0.35-0.45)
- Au moins 3 radial-gradient ou conic-gradient colorés répartis (overlays atmosphériques)

Pas de fond plat sans matière de surface.

---

## Source et traçabilité

**TIER 1** extrait de `finition-elite-core.md` — règles structurantes pour la palette/CSS moderne/couche graphique.

**TIER 2 + TIER 3** (ombres ≥2 niveaux, easing physiques nommés, rythme spacing variable entre sections, transitions multi-property au hover, retenue hovers scale 1.01-1.02, techniques avancées CSS ≥4 parmi 9) restent dans `finition-elite-core.md` et sont gérés par le subagent Critique en aval.

## Dernière mise à jour

2026-04-25 — Création TIER 1 lors du pivot architectural Designer + Critique.
2026-04-26 — Vague 2 anti-slop : 3 promotions TIER 1 (R-003 Neutres tintés, R-010 Système typographique modulaire, R-023 Système d'espacement nommé). Total TIER 1 : 19 règles (sous plafond 25).
