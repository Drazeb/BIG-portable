# Framework d'Output — Zone 2 : Le Lab

> **SCOPE V2** — Ce fichier définit les protocoles pour la Zone 2 (Lab), qui sera implémentée en V2 du skill. La structure est préservée pour garantir la cohérence future.

---

## 1. CONCEPT FONDAMENTAL

La Zone 2 est la **documentation technique exhaustive** de l'identité de marque. Là où la Zone 1 vend de l'émotion, la Zone 2 fournit la **spécification complète**.

Format : **2 fichiers**
- Fichier 1 : `{brand}_manifesto.md` (Le Cerveau — stratégie narrative)
- Fichier 2 : `{brand}_design_specs.html` (Le Corps — spécifications techniques)

---

## 2. PROTOCOLE NO-DIGEST (Token Override)

En Zone 2, le biais naturel de synthèse est l'ENNEMI.

### Règles
- Objectif : traiter **100%** des points de la liste, même si cela demande 5000 lignes
- **Ne jamais compresser** le code pour qu'il rentre dans une seule réponse
- Si le fichier coupe au milieu : c'est une victoire (preuve d'exhaustivité)
- Il vaut mieux un fichier coupé mais dense qu'un fichier complet mais résumé

### La Règle des 40 Divs (Atomic Check)
- Compter les sous-points du Master Style Guide
- Le fichier HTML doit contenir une `<div class="spec-section">` par sous-point
- INTERDICTION de grouper des points (ex: "02.1 & 02.2")
- INTERDICTION de faire des listes à puces en lieu et place de blocs visuels codés

---

## 3. FICHIER 1 — MANIFESTE STRATÉGIQUE (.md)

Points à couvrir :
- [01] Fondations Stratégiques (5 sous-points)
- [05] Logotype — Partie Conceptuelle (1 sous-point)
- [08] Direction Narrative — Partie Intention (1 sous-point)
- [10] Illustration — Partie Narrative (2 sous-points)

---

## 4. FICHIER 2 — DESIGN SYSTEM (.html)

Points à couvrir (exhaustif, 1 section par sous-point) :
- [02] Color System (6 sous-points)
- [03] Typographie (4 sous-points)
- [04] Code Civil Atomique — Tokens (5 sous-points texte dans design-specs) + Composants UI (5 sous-points visuels dans batch2 HTML : Buttons, Form Elements, Badges, Cards, Feedback & Navigation)
- [05] Logotype — Partie Visuelle (3 sous-points)
- [06] Iconographie (4 sous-points)
- [07] Data Visualization (4 sous-points)
- [08] Direction Photo — Partie Moodboard (3 sous-points)
- [09] Système de Composition (4 sous-points)
- [10] Illustration — Partie Visuelle (3 sous-points)

---

## 5. IMPLÉMENTATION V2

Ce fichier sera activé lorsque les Phases 5-6 seront implémentées dans le skill. Les subagents correspondants liront ce document pour générer la Zone 2 complète.
