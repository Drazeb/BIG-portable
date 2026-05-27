# A11y et Fondamentaux — TIER 1 (non-négociable)

Ces règles ne sont PAS optionnelles, ne dépendent PAS du concept, ne se patchent PAS proprement après coup. Le Designer DOIT les appliquer dès la conception, sans exception.

**Portée** : importé par Phase 4 (styletile + artefact), Batch 2, Batch 3.

---

## A11y — accessibilité (non-négociable légal)

- **`:focus-visible` sur TOUS les interactifs** (`<a>`, `<button>`, `<input>`, éléments avec `cursor: pointer`). Outline cohérent avec `--color-accent` du `:root` (couleur ou color-mix), `outline-offset: 2px` minimum, `border-radius: inherit` si l'élément a un radius. JAMAIS `outline: none` sans `:focus-visible` de remplacement.
- **`prefers-reduced-motion` honoré** si animations actives (durée > 200ms ou `infinite`). Bloc obligatoire :
  ```
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
    }
  }
  ```
- **Touch targets ≥ 44px** sur tous les interactifs (boutons, liens cliquables, toggles). Si l'élément visible est < 44px, étendre la zone tactile via `padding` ou `::before` invisible.
- **Body text en `rem`** (pas `px`), avec `font-size` racine ≥ 16px. Permet le respect du zoom utilisateur navigateur (a11y zoom).
- **Semantic HTML obligatoire** : `<button>` pour actions, `<a href>` pour navigation, `<label>` (avec `for` ou wrapping) pour `<input>`. JAMAIS `<div onClick>` ou `<span onClick>`.
- **WCAG AA contraste** : 4.5:1 sur body text, 3:1 sur large text (≥ 24px) / UI components / icons. Vérifier les paires fond/texte au design (notamment sur sections semi-transparentes).

## Viewport et mobile (structurel)

- **`min-block-size: 100dvh`** (dynamic viewport height) au lieu de `100vh` sur sections full-bleed. Évite le viewport jump iOS Safari.

---

## Pourquoi ces règles sont en TIER 1 et pas dans le Critique

Ces 7 règles sont des **fondamentaux structurels** qui demandent une connaissance globale du design system du concept (palette accent pour focus-visible, hiérarchie typo pour rem, structure HTML sémantique pour les actions). Si elles sont manquées à la création, les corriger en patch chirurgical risque de :
- Ajouter un `:focus-visible` générique qui jure avec la palette accent
- Refactoriser la structure `<div onClick>` → `<button>` (lourd et risque de casser le CSS)
- Modifier le `:root` pour mettre body en `rem` (touche tout le type-scale)

Mieux vaut que le Designer les applique nativement dès la première version, avec son cerveau CSS et sa connaissance du design system.

---

## Source et traçabilité

**TIER 1** créé le 2026-04-25 suite au constat que le mode CORRECTION improvisé manquait systématiquement les corrections a11y critiques (cf. test `test-voltapilot-test-20260425-1457` — `:focus-visible` et `prefers-reduced-motion` absents du HTML résultant malgré FAIL détectés par les contrôleurs).

Règles extraites de `anti-slop-blacklist-core.md` §3-§5 (placeholder TIER 2+3 — promues TIER 1) et de `vercel-command.md` (sources audit-slop).
