# 08 — Brutaliste / ASCII — Fiche slop / anti-slop

**Famille** : `08-brutaliste` · **Dernière revue** : 2026-05-27 · **Prochaine revue** : 2026-08-27

**Sources scannées** : Mike Mai (2023-2025), Bobby Berry (2024), Dia Browser (2025), Sentry docs (2024-2025), Are.na "Brutalist Web Design" channel (2024-2026), *Web Brutalism in 2026* — Eye on Design AIGA (mars 2026), *The Return of Terminal Aesthetic* — It's Nice That (mai 2025).

---

## À BANNIR — 8 anti-patterns datés

### `[ANTI-01]` Police monospace pas vraiment monospace (substitution fallback)
- **Description** : `font-family: monospace` sans web font, fallback approximatif
- **Preuve d'âge** : erreur d'implémentation classique
- **Signature slop** : casse la grille caractère qui FAIT le médium
- **Contre-exemple pro** : Mike Mai 2024 — IBM Plex Mono ou JetBrains Mono chargés explicitement

### `[ANTI-02]` Couleurs colorées (>2 couleurs)
- **Description** : essayer de rendre le brutaliste "cool" avec une palette colorée
- **Preuve d'âge** : tentatives de "brutalism friendly" 2020-2022
- **Signature slop** : trahit la contrainte qui FAIT le médium
- **Contre-exemple pro** : refs 2024 — noir/blanc strict, ou +1 accent unique vert phosphore / orange terminal

### `[ANTI-03]` Anti-aliasing sur les caractères Unicode graphiques
- **Description** : utiliser `█▓░` avec rendering smooth, perdant la grille
- **Preuve d'âge** : erreur d'implémentation
- **Signature slop** : flou = pas brutaliste
- **Contre-exemple pro** : Mike Mai 2024 — `font-smooth: never` ou CSS équivalent

### `[ANTI-04]` Composition centrée symétrique propre
- **Description** : appliquer les codes de mise en page UI moderne à du brutaliste
- **Preuve d'âge** : confusion brutalism / minimalism propre
- **Signature slop** : casse l'asymétrie assumée du raw web
- **Contre-exemple pro** : Are.na Brutalist channel — asymétries franches, alignements décalés

### `[ANTI-05]` Ombre portée / glow / effets décoratifs
- **Description** : appliquer des filtres CSS sur du brutaliste
- **Preuve d'âge** : automatisme UI moderne
- **Signature slop** : annule la pureté du médium
- **Contre-exemple pro** : refs 2024 — zéro filter CSS, propreté ASCII pure

### `[ANTI-06]` Icônes "brutalist friendly" infantilisées (formes pâteuses)
- **Description** : silhouettes arrondies présentées comme "brutalist"
- **Preuve d'âge** : confusion brutalism / chunky design
- **Signature slop** : ce n'est pas du brutalism, c'est du chunky illustration
- **Contre-exemple pro** : Mike Mai — angles francs, blocs purs

### `[ANTI-07]` Caractères Unicode décoratifs (étoiles, fleurs, emojis)
- **Description** : utilisation de Unicode "fun" au lieu des caractères structurels
- **Preuve d'âge** : confusion ASCII art "fun" vs brutalism structural
- **Signature slop** : trahit la rigueur du médium
- **Contre-exemple pro** : refs 2024 — Unicode structurels (`█▓░│─┃╋╳╱╲┌┐└┘├┤┬┴┼`)

### `[ANTI-08]` Faux brutalism "designé" (graphisme léché qui se déguise)
- **Description** : icônes propres présentées comme brutalist
- **Preuve d'âge** : tendance "brutalist aesthetic" sans le médium
- **Signature slop** : esbroufe, pas authentique
- **Contre-exemple pro** : Mike Mai — vraiment brutalist dans l'implémentation, pas juste l'esthétique

---

## SIGNATURES PRO 2024-2026 — 5 patterns à reproduire

### `[SIG-01]` Police monospace web font chargée (IBM Plex Mono / JetBrains Mono / GT Pressura Mono)
- **Description** : police monospace pro avec contrôle de la grille
- **Source** : 100% des refs pro 2024
- **Implémentation** : `@import` Google Fonts ou self-hosted

### `[SIG-02]` Caractères Unicode structurels graphiques (`█▓░│─┃╋╳╱╲`)
- **Description** : utiliser Unicode pour DESSINER, pas juste pour décorer
- **Source** : Are.na Brutalist channel, Mike Mai 2024
- **Implémentation** : `<pre>` avec lignes de caractères structurels

### `[SIG-03]` Palette bichrome stricte (noir/blanc ou +1 accent terminal)
- **Description** : contrainte qui définit le médium
- **Source** : Game Boy palette, terminal Unix
- **Implémentation** : 2 couleurs hex hardcodées, max

### `[SIG-04]` Asymétrie assumée (refus de la propreté UI)
- **Description** : alignements décalés volontaires, refus du grid moderne propre
- **Source** : Are.na Brutalist, Mike Mai, Dia Browser sections brutalist
- **Implémentation** : `margin-left: 17px` etc. — refus du grid 4px / 8px UI

### `[SIG-05]` SVG `<rect>` sur grille stricte (si SVG, pas `<pre>`)
- **Description** : alternative SVG avec `shape-rendering="crispEdges"`
- **Source** : signature brutalist-pixel hybrid
- **Implémentation** : viewBox petite + rect crispEdges + 2 couleurs

---

## CHECKS MÉCANIQUES — 2 vérifications

### `[CHK-01]` Police monospace explicitement chargée (pas fallback)
- **Règle** : signature technique obligatoire
- **Vérification** : grep `font-family.*Mono|font-family.*Pressura|fonts.googleapis.*Mono`

### `[CHK-02]` Palette ≤ 2 couleurs distinctes (+ neutre fond)
- **Règle** : contrainte définissant le médium
- **Vérification** : extraire fills/strokes, ≤3 valeurs uniques

### `[CHK-03]` INCARNATION VISIBLE — 100% des icônes du set 06.1 utilisent vraiment le médium brutaliste (monospace+Unicode OU SVG rect crispEdges strict)
- **Règle** : la famille brutaliste est définie par son médium intrinsèque. Toutes les icônes du set DOIVENT être SOIT (a) en `<pre>` monospace avec caractères Unicode structurels (`█▓░│─┃╋╳╱╲┌┐└┘├┤┬┴┼`) SOIT (b) en SVG `<rect>` avec `shape-rendering="crispEdges"` strict. Pas de mix avec d'autres familles, pas de Bézier courbe
- **Vérification** : pour chaque icône du set, détecter SOIT (a) `<pre>` avec font monospace + caractères Unicode structurels SOIT (b) SVG uniquement `<rect>` (zéro `<path>` Bézier) avec `shape-rendering="crispEdges"`. 100% doit passer
- **Si fail (<100%)** : la famille n'est pas respectée — quelques icônes utilisent du Bézier "normal" ou des courbes lisses. Re-dispatch designer : "TOUTES les icônes du set DOIVENT être en médium brutaliste strict : soit `<pre>` monospace avec Unicode structurels, soit SVG rect crispEdges. Pas de courbes Bézier, pas de mix."
