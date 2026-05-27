# Anti-Slop Blacklist — TIER 1 (structurantes)

Ce fichier contient les **interdictions structurantes** qui doivent guider le Designer Phase 4 dès la conception. Pour les détails et anti-patterns détectables (TIER 2 + TIER 3), voir `anti-slop-blacklist-core.md` — lus uniquement par le Critique en aval.

**Portée** : importé par Phase 4 (styletile + artefact), Batch 2, Batch 3.

---

## Compositions à éviter dès la composition initiale

Ces patterns macro sont les marqueurs les plus reconnaissables de slop. Les éviter dès la conception, pas en correction.

- Do NOT use rigid 50/50 hero split as default layout — web's most generic composition
- Do NOT use grids of N identical containers — vary proportions, hierarchize by size
- Do NOT use feature sections as uniform icon+title+description containers — web's most copied pattern
- Do NOT use exhaustive link-column footers — footer is a conclusion, not a sitemap
- Do NOT use carousels as content containers — content is visible, not hidden behind arrows
- Do NOT use product screenshots in device frames (laptop, phone) — show product through components

Avoid these and their visual cousins (variations of the same generic landing-page templates from 2015-2020).

---

## Source et traçabilité

**TIER 1** extrait de `anti-slop-blacklist-core.md §1 Compositions datées` — règles à plus haut impact compositionnel.

**TIER 2 + TIER 3** (hovers datés, animations infinies, séparateurs, effets visuels datés, animations d'entrée datées, autres compositions datées spécifiques, couche graphique interdictions) restent dans `anti-slop-blacklist-core.md` et sont gérés par le subagent Critique en aval (`phase-4check.md`).

## Dernière mise à jour

2026-04-25 — Création TIER 1 lors du pivot architectural Designer + Critique.
