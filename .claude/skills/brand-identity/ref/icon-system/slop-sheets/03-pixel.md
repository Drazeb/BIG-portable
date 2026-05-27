# 03 — Pixel art — Fiche slop / anti-slop

**Famille** : `03-pixel` · **Dernière revue** : 2026-05-27 · **Prochaine revue** : 2026-08-27

**Sources scannées** : GitHub Pixels initiative (2024), Cassette Tape (2024), Pico-8 community (2024-2026), itch.io interface (2024-2026), DB16/DB32 DawnBringer palettes, *Pixel Art's Quiet Renaissance in Branding* — It's Nice That (novembre 2024).

---

## À BANNIR — 8 anti-patterns datés

### `[ANTI-01]` Anti-aliasing implicite (rendering par défaut)
- **Description** : oubli de `shape-rendering: crispEdges`, les pixels deviennent flous
- **Preuve d'âge** : erreur débutant, toujours observable dans templates pixel rapides
- **Signature slop** : tueur intrinsèque — du pixel art flou n'est plus du pixel art
- **Contre-exemple pro** : 100% des refs pro utilisent `crispEdges`

### `[ANTI-02]` Palette > 8 couleurs par icône
- **Description** : palette débordée, "pixel art photo-réaliste"
- **Preuve d'âge** : tendance "pixel art HD" 2010s, mort fin 2010s
- **Signature slop** : trahit la contrainte historique qui FAIT le médium
- **Contre-exemple pro** : Pico-8 16 couleurs total dans la palette globale, 4-8 par sprite

### `[ANTI-03]` Grille déformée (pixels rectangulaires au lieu de carrés)
- **Description** : viewBox non carrée appliquée à des "pixels" qui s'étirent
- **Preuve d'âge** : erreur d'implémentation classique
- **Signature slop** : casse le rendu pixel-perfect
- **Contre-exemple pro** : grille carrée stricte, viewBox 12 12 / 16 16

### `[ANTI-04]` Pixel art "haute résolution" (256×256 +)
- **Description** : pixel art tellement dense qu'on perd la lisibilité de la grille
- **Preuve d'âge** : 2010s "pixel art réaliste", abandonné
- **Signature slop** : si la grille n'est plus visible, c'est de l'illustration, pas du pixel art
- **Contre-exemple pro** : refs 2024 — grilles 16×16 ou 24×24 max

### `[ANTI-05]` Gradient pixel (transitions douces simulées en pixels)
- **Description** : utilisation de nuances de couleur pour simuler un dégradé sur un pixel
- **Preuve d'âge** : tendance "pixel art moderne" 2015-2020
- **Signature slop** : trahit la contrainte palette stricte
- **Contre-exemple pro** : Pico-8 community 2024 — aplats nets de 1 couleur par zone

### `[ANTI-06]` Outline noir 1px autour de chaque sprite
- **Description** : ligne noire de contour systématique
- **Preuve d'âge** : signature pixel art "cartoon" 2000s, daté
- **Signature slop** : enferme dans un seul style historique
- **Contre-exemple pro** : DB16 palette assume sans contour systématique

### `[ANTI-07]` Mascot pixel art forcé dans toutes les illustrations
- **Description** : un personnage récurrent pixelisé apparaît partout
- **Preuve d'âge** : tendance B2C 2014-2020 transposée à tort en pixel art
- **Signature slop** : forcé, inventé pour habiller, pas crédible
- **Contre-exemple pro** : itch.io — pas de mascot omniprésent, l'interface vit par elle-même

### `[ANTI-08]` Effets "post-production" sur le pixel (glow, blur, drop-shadow)
- **Description** : appliquer des filtres CSS sur du pixel art
- **Preuve d'âge** : confusion conceptuelle des designers non-pixel
- **Signature slop** : annule la pureté du médium
- **Contre-exemple pro** : refs 2024 — zéro filter CSS sur le pixel

---

## SIGNATURES PRO 2024-2026 — 5 patterns à reproduire

### `[SIG-01]` `shape-rendering="crispEdges"` SVG sur tous les rect
- **Description** : signature technique obligatoire
- **Source** : 100% des refs pro pixel art SVG 2024
- **Implémentation** : attribut sur le `<svg>` racine ou sur chaque `<rect>`

### `[SIG-02]` Palette restreinte 4-8 couleurs (référence DB16 ou Pico-8)
- **Description** : palette nommée, sourçable, historiquement crédible
- **Source** : DB16 DawnBringer (2009, toujours utilisé 2024), Pico-8 (2014)
- **Implémentation** : 4-8 couleurs hex hardcodées dans le SVG, pas plus

### `[SIG-03]` Grille petite (12-24 unités max)
- **Description** : viewBox petite, pixels visibles
- **Source** : itch.io interface 2024, GitHub Pixels 2024
- **Implémentation** : viewBox 12 12, 16 16, 24 24 max

### `[SIG-04]` Variante 1-bit (n/b strict) signature
- **Description** : version monochrome pure pour les éléments dense / micro-icônes
- **Source** : Game Boy palette historique, refs 2024 brutalist-pixel
- **Implémentation** : 2 couleurs seulement (fond + signature)

### `[SIG-05]` Animation frame-by-frame possible (signature pixel)
- **Description** : si animation, frame-by-frame en `@keyframes steps()`, pas easing lisse
- **Source** : refs jeu vidéo, repris en web pixel 2024
- **Implémentation** : CSS `animation-timing-function: steps(N)`

---

## CHECKS MÉCANIQUES — 2 vérifications

### `[CHK-01]` `shape-rendering="crispEdges"` présent
- **Règle** : tueur intrinsèque si absent
- **Vérification** : grep `shape-rendering="crispEdges"` → ≥1 occurrence

### `[CHK-02]` Compte des `<rect>` distincts ≤ 200 par icône (pas du pixel HD)
- **Règle** : si trop de rect, c'est de l'illustration pixelisée, pas du pixel art
- **Vérification** : compter `<rect` par groupe d'icône, doit être 10-150 range

### `[CHK-03]` INCARNATION VISIBLE — 100% des icônes du set 06.1 sont en grille pixel stricte
- **Règle** : `[SIG-03]` grille petite + `[SIG-01]` crispEdges sont la SIGNATURE intrinsèque du pixel art — pas un détail décoratif. Toutes les icônes du set doivent avoir viewBox petite (≤24×24) ET utiliser uniquement `<rect>` (pas de path Bézier courbe) ET avoir `shape-rendering="crispEdges"` (sur le SVG racine ou sur chaque rect)
- **Vérification** : pour chaque SVG du set : viewBox ≤ 24×24 ET zéro `<path>` Bézier (uniquement `<rect>`) ET `shape-rendering="crispEdges"` présent. 100% du set doit passer
- **Si fail (<100%)** : la famille n'est pas respectée — quelques icônes utilisent du Bézier ou de la grille trop grande. Re-dispatch designer : "TOUTES les icônes du set DOIVENT être en pixel art strict : viewBox 12-24, rectangles uniquement, shape-rendering crispEdges, palette ≤8 couleurs."
