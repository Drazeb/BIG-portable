# Prompt — Polissage de Style-Tiles en Exemples Canoniques

> **Usage** : Copie ce document entier comme premier message dans une session Claude Code vierge.
> **Prérequis** : Avoir 3-5 style-tiles HTML générés par le pipeline BIG, ouverts dans le navigateur, et avoir identifié les 3 plus réussis ET structurellement différents.

---

## CONTEXTE — Pourquoi ce travail existe

Je travaille sur le **Brand Identity Generator (BIG)**, un système qui génère des identités de marque via un pipeline orchestré par Claude Code. Le pipeline est dans `.claude/skills/brand-identity/`.

Le pipeline génère des **style-tiles HTML** (fichiers self-contained avec CSS inline) pour présenter des concepts de marque. Le problème identifié : **les style-tiles générés se ressemblent structurellement** (~65-70% d'ADN commun) parce que le subagent qui les génère lit UN exemple de référence et en reproduit inconsciemment la structure (layout des cards, type de hero, pattern de shadows, architecture des composants).

**Ta mission** : transformer 3 vrais style-tiles (outputs réels du pipeline) en **exemples canoniques** de qualité elite. Ces exemples serviront de référence qualité pour les futures générations. Ils doivent être **maximalement différents structurellement** pour casser le biais de mimétisme.

---

## FICHIERS DE RÉFÉRENCE À LIRE EN PREMIER

Lis ces fichiers AVANT de commencer le travail :

1. **Spec technique HTML** : `.claude/skills/brand-identity/ref/html-showroom-spec.md`
   - Particulièrement la **section 6 — Vocabulaire CSS Moderne** (catalogue de techniques 2023-2026)
   - Et la **section 4 — Structure des 3 sections** (triptyque : Voice Block + Artefact + Atmosphere)

2. **Bible design** : `.claude/skills/brand-identity/ref/bible-design-strategie.md`
   - Les curseurs A (Audace) et B (Différenciation) et leur influence sur le design

3. **Exemples actuels** (pour comprendre le standard existant) :
   - `.claude/skills/brand-identity/examples/standard/style-tile-example-A.html` (Clarity Analytics, A=1)
   - `.claude/skills/brand-identity/examples/standard/style-tile-example-B.html` (Maison Solène, A=2)
   - `.claude/skills/brand-identity/examples/rupture/style-tile-example-C.html` (NØRD Studio, A=3)

---

## LES 3 STYLE-TILES À POLIR

> **[INSÈRE ICI les chemins des 3 fichiers HTML sélectionnés]**
>
> Style-tile 1 : `outputs/.../.html` — Brief: ..., Curseurs A=... B=...
> Style-tile 2 : `outputs/.../.html` — Brief: ..., Curseurs A=... B=...
> Style-tile 3 : `outputs/.../.html` — Brief: ..., Curseurs A=... B=...

---

## PROCESSUS DE POLISSAGE (3 passes)

### PASSE 1 — Audit structurel (lecture seule, AUCUNE modification)

Pour chaque style-tile, lis le fichier entier et documente :

**A. Inventaire structurel :**
- Composition du Voice Block : quel type ? (centré, split, full-bleed typo, superposition, grille éditoriale, diagonale, minimaliste, autre)
- Architecture de l'Artefact : quel composant ? (cards grid, timeline, formulaire, tableau, player, liste, layout libre, autre)
- Approche Atmosphere : quel registre ? (sombre classique, clair inversé, gradient immersif, texturé, coloré saturé, autre)
- Techniques CSS utilisées : liste exhaustive (grid, flexbox, gradients, animations, filters, clip-path, etc.)

**B. Score CSS moderne :**
- oklch() : oui/non + nombre d'occurrences
- @layer : oui/non
- @property : oui/non + quelles propriétés
- text-wrap balance/pretty : oui/non
- color-mix() : oui/non
- clip-path / mask-image : oui/non
- container queries : oui/non
- logical properties : oui/non
- Autres techniques modernes : lesquelles

**C. Matrice de diversité (CRITIQUE) :**

Remplis ce tableau pour les 3 style-tiles :

| Dimension | Style-tile 1 | Style-tile 2 | Style-tile 3 |
|-----------|-------------|-------------|-------------|
| Composition Voice Block | | | |
| Architecture Artefact | | | |
| Approche Atmosphere | | | |
| Palette (harmonie) | | | |
| Typo (serif/sans/mono) | | | |
| Registre (clair/sombre/mixte) | | | |
| Densité (aéré/dense/mixte) | | | |
| Technique CSS signature | | | |

**Chaque ligne DOIT avoir 3 valeurs DIFFÉRENTES.** Si 2 style-tiles partagent une valeur sur une ligne, signale-le — c'est un problème à résoudre en Passe 2.

**Présente-moi cet audit AVANT de passer à la Passe 2.** J'arbitrerai les conflits de diversité.

---

### PASSE 2 — Modernisation CSS + différenciation structurelle

Pour chaque style-tile, applique les modifications suivantes :

**A. CSS Moderne obligatoire (minimum 6 techniques par fichier) :**

1. **oklch()** : Convertir TOUTE la palette `:root` de HEX vers oklch. Les couleurs DOIVENT rester visuellement identiques.
   - Outil de conversion : les valeurs oklch approximatives suffisent si elles sont perceptuellement fidèles
   - Les rgba() deviennent `oklch(L C H / alpha)`
   - Supprimer les variables `-rgb` (plus nécessaires avec oklch)

2. **@layer** : Organiser le CSS en couches explicites :
   ```css
   @layer reset, tokens, components, utilities;
   @layer reset { /* reset */ }
   @layer tokens { :root { /* variables */ } }
   @layer components { /* tout le reste */ }
   ```
   Note : `@property` et la déclaration `@layer` d'ordre restent HORS des layers.

3. **@property** : Déclarer au moins 1 custom property typée et animable. Choisir en fonction du concept :
   - Concept organique/vivant → `--gradient-angle` (type `<angle>`)
   - Concept tech/données → `--accent-hue` (type `<number>`)
   - Concept chaleureux → `--glow-intensity` (type `<number>`)

4. **text-wrap** : `balance` sur tous les h1/h2, `pretty` sur tous les paragraphes

5. **color-mix()** : Remplacer les couleurs hover hardcodées par `color-mix(in oklch, var(--color-xxx) 85%, black)`

6. **Logical properties** : Remplacer `margin-top/bottom` → `margin-block`, `padding-left/right` → `padding-inline`, etc.

7. **Au choix selon le concept (minimum 1)** :
   - `clip-path` pour une transition de section non-rectangulaire
   - `mask-image` pour un fondu atmosphérique
   - `@container` pour un artefact adaptatif
   - `animation-timeline: view()` pour un reveal au scroll
   - `subgrid` pour des alignements dans l'artefact
   - `backdrop-filter` avancé (blur + saturate)

**B. Résolution des conflits de diversité (identifiés en Passe 1) :**

Si 2 style-tiles partagent la même structure sur une dimension :
- **Voice Block identiques** → Transformer l'un des deux. Options : centré → full-bleed typo, split → grille éditoriale, etc. Le changement doit rester COHÉRENT avec le concept/brief du style-tile.
- **Artefacts identiques** → Changer le type de composant de l'un. Un dashboard de cards peut devenir une timeline, un pricing table, un formulaire multi-étapes.
- **Atmospheres identiques** → Inverser le registre de l'un. Sombre → clair texturé, gradient → flat coloré.

**C. Nettoyage qualité :**
- Zero dead code : chaque `@keyframes` utilisé, chaque custom property référencée
- Supprimer les commentaires techniques/debug
- Vérifier WCAG AA sur les contrastes texte
- `font-feature-settings` sur les données numériques
- `letter-spacing` sur les overlines et caps
- Transitions sur TOUS les éléments interactifs

---

### PASSE 3 — Validation finale

Pour chaque fichier poli, vérifie ces gates :

**Gates obligatoires :**
- [ ] **Screenshot Test** : ZÉRO donnée technique visible (pas de HEX, pas de noms de fonts, pas de px dans le texte)
- [ ] **Mason's Rule** : ZÉRO scaffolding (pas de "Section 02", pas de labels)
- [ ] **Zero Dead Code** : chaque @keyframes et custom property utilisés
- [ ] **CSS Moderne** : minimum 6 techniques de la section 6 de html-showroom-spec.md
- [ ] **Couverture :root** : les 7 catégories présentes (palette, typo, type-scale, spacing, radius, shadows, transitions)
- [ ] **Self-contained** : tout le CSS dans `<style>`, Google Fonts via `<link>` avec preconnect
- [ ] **Diversité structurelle** : la matrice de diversité a 3 valeurs DIFFÉRENTES sur chaque ligne

**Gate qualité elite :**
- [ ] Le fichier est visuellement impressionnant dans un navigateur
- [ ] Chaque section a de la profondeur visuelle (pas de backgrounds plats)
- [ ] Les animations sont subtiles et significatives (pas gratuites)
- [ ] La typographie est soignée (balance, kerning, leading, feature-settings)

---

## RÈGLES STRICTES

### NE PAS modifier :
- Les class names des 3 sections : `voice-block`, `artifact-witness` OU `artifact-section`, `atmosphere-block` — le pipeline en dépend
- Le concept/brief sous-jacent (palette, fonts, contenu narratif)
- La structure HTML globale (3 sections, pas plus, pas moins)

### NE PAS introduire :
- Des images SVG "faites maison" (illustrations, logos)
- Des dépendances externes (CDN, frameworks, JS)
- Du contenu technique visible (nuanciers, noms de fonts, specs)

### TOUJOURS :
- Garder le fichier self-contained
- Garder les Google Fonts identiques
- Garder le contenu textuel intact (ou l'améliorer si clairement bancal)
- Tester dans Chrome ou Safari dernière version

---

## SORTIE ATTENDUE

Pour chaque style-tile poli :
1. Le fichier HTML écrit dans `examples/` avec un nom descriptif :
   - `examples/example-A-{composition}.html` (ex: `example-A-centered-typo.html`)
   - `examples/example-B-{composition}.html` (ex: `example-B-editorial-grid.html`)
   - `examples/example-C-{composition}.html` (ex: `example-C-asymmetric-layers.html`)
2. Un résumé des modifications effectuées
3. La matrice de diversité finale (preuve que les 3 sont différents)

---

## ANTI-PATTERNS — Ce qui a échoué par le passé

Ces patterns ont été identifiés sur les vrais outputs du pipeline. NE PAS les reproduire :

1. **Le "look SaaS 2019"** : cards avec border-radius 16px, shadow-md identiques, grille 3 colonnes, hero split systématique. C'est le pattern par défaut du LLM — l'éviter activement.

2. **L'atmosphère sombre par défaut** : le LLM a un biais vers le dark mode pour les sections "Atmosphere". Au moins 1 des 3 exemples DOIT avoir une atmosphère claire, texturée, ou colorée.

3. **Le même hover effect partout** : `transform: translateY(-4px)` + shadow-lg sur les cards. Varier : scale, background-color, border, clip-path, filter, opacity.

4. **Les gradients linéaires plats** : `linear-gradient(to bottom, ...)`. Varier : radial, conic, mesh (via superposition de radials), oklch gradients.

5. **Aucune technique CSS post-2021** : pas de oklch, pas de @layer, pas de text-wrap, pas de container queries. Les exemples DOIVENT montrer du CSS 2024-2026.

6. **3 Voice Blocks hero-split** : la composition la plus "safe" du LLM. Maximum 1 hero-split sur les 3 exemples.
