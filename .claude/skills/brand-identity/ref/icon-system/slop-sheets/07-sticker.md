# 07 — Sticker / cut-out — Fiche slop / anti-slop

**Famille** : `07-sticker` · **Dernière revue** : 2026-05-27 · **Prochaine revue** : 2026-08-27

**Sources scannées** : Vercel Conf (2024-2025), Linear releases (2024), Substack featured badges (2025), Discord Nitro (2024-2026), GitHub Achievements (2024-2025), *The Sticker Aesthetic: From Physical to Digital* — It's Nice That (juin 2024).

---

## À BANNIR — 8 anti-patterns datés

### `[ANTI-01]` Drop-shadow flou sans contour blanc préalable
- **Description** : ombre portée seule sans le contour blanc qui simule la découpe
- **Preuve d'âge** : oubli technique fréquent
- **Signature slop** : c'est juste une icône avec ombre, pas un sticker
- **Contre-exemple pro** : Vercel stickers 2024 — DOUBLE drop-shadow (blanc 3px + flou sombre)

### `[ANTI-02]` Forme géométrique pure sans personnalité (cercle, carré, hexagone)
- **Description** : sticker réduit à une forme géométrique sans figure / objet / symbole identifiable
- **Preuve d'âge** : badges génériques templates 2018-2020
- **Signature slop** : interchangeable, oubliable
- **Contre-exemple pro** : Discord Nitro stickers 2024 — chaque sticker = silhouette identifiable

### `[ANTI-03]` Palette pastel anémique (Headspace-like)
- **Description** : sticker en couleur pastel délavée
- **Preuve d'âge** : Corporate Memphis 2018-2021
- **Signature slop** : tue l'éclat qui FAIT le sticker
- **Contre-exemple pro** : refs 2024 — couleurs saturées qui pop sur fond

### `[ANTI-04]` Rotation 0° figée (orthogonal parfait)
- **Description** : sticker parfaitement aligné aux axes
- **Preuve d'âge** : oubli de la signature physique "collé à la main"
- **Signature slop** : trop digital, perd l'authenticité du collage
- **Contre-exemple pro** : Substack badges 2025 — rotation -3° à +5° calculée

### `[ANTI-05]` Sticker sans accent / détail intérieur
- **Description** : silhouette pleine sans aucun détail à l'intérieur
- **Preuve d'âge** : confusion sticker / silhouette plate
- **Signature slop** : c'est un blob, pas un sticker
- **Contre-exemple pro** : GitHub Achievements 2024 — chaque sticker a un détail icon central

### `[ANTI-06]` Contour blanc TROP fin (≤2px)
- **Description** : contour de découpe trop discret pour signifier la coupe physique
- **Preuve d'âge** : erreur d'implémentation
- **Signature slop** : la découpe doit être ÉVIDENTE
- **Contre-exemple pro** : Linear releases 2024 — contour blanc 4-8px obligatoire

### `[ANTI-07]` Mascot forcé dans chaque sticker
- **Description** : la mascotte de la marque apparaît dans tous les stickers
- **Preuve d'âge** : tendance Duolingo / Mailchimp 2016-2020
- **Signature slop** : forcé, perd la variété naturelle du sticker
- **Contre-exemple pro** : Vercel stickers 2024 — variété de motifs sans mascot omniprésente

### `[ANTI-08]` "Sticker" en aplat sans drop-shadow du tout
- **Description** : juste une silhouette colorée sans aucun effet de "sticker"
- **Preuve d'âge** : confusion sticker / flat illustration
- **Signature slop** : sans drop-shadow, c'est juste de l'illustration plate
- **Contre-exemple pro** : 100% des refs pro — drop-shadow signature obligatoire

---

## SIGNATURES PRO 2024-2026 — 5 patterns à reproduire

### `[SIG-01]` Double drop-shadow (blanc épais + flou sombre)
- **Description** : `drop-shadow(0 3px 0 white) drop-shadow(0 4px 4px rgba(0,0,0,0.18))`
- **Source** : Vercel stickers 2024, Linear releases 2024
- **Implémentation** : CSS exact, pas approximation

### `[SIG-02]` Rotation aléatoire 3-8° (effet "collé à la main")
- **Description** : transform rotate signature
- **Source** : Substack badges 2025, GitHub Achievements 2024
- **Implémentation** : CSS `transform: rotate(-5deg)` etc., randomisé par sticker

### `[SIG-03]` Couleur saturée vive (jamais pastel)
- **Description** : 1 couleur par sticker, saturation forte
- **Source** : Discord Nitro 2024, Vercel 2024
- **Implémentation** : `oklch` chroma 0.15+ pour les accents

### `[SIG-04]` Silhouette identifiable + détail central
- **Description** : forme reconnaissable globale + 1 petit détail icon à l'intérieur
- **Source** : GitHub Achievements 2024, Substack badges 2025
- **Implémentation** : 2 layers — silhouette + détail central white/contrasté

### `[SIG-05]` Conteneur transparent (le sticker est posé sur autre chose)
- **Description** : aucun fond, le sticker doit pouvoir vivre sur n'importe quel background
- **Source** : 100% des refs pro
- **Implémentation** : SVG `background: transparent`, viewBox calée sur le sticker

---

## CHECKS MÉCANIQUES — 2 vérifications

### `[CHK-01]` Au moins 1 drop-shadow avec offset 0 et couleur white
- **Règle** : signature "découpe sticker" obligatoire
- **Vérification** : grep `drop-shadow(0 \d+px 0 white)` ou équivalent CSS

### `[CHK-02]` Présence d'au moins 1 `transform: rotate(...)` avec angle ≠ 0
- **Règle** : signature "collé à la main"
- **Vérification** : grep `transform: rotate(-?[1-9]` (exclut 0deg)

### `[CHK-03]` INCARNATION VISIBLE — ≥80% des icônes du set 06.1 ont la signature sticker complète (drop-shadow double + rotation)
- **Règle** : la famille sticker est DÉFINIE par ses 2 signatures intrinsèques (`[SIG-01]` double drop-shadow blanc+sombre + `[SIG-02]` rotation 3-8°). Sans ces 2 signatures, ce n'est PAS un sticker — c'est une icône plate. Au moins 16 icônes sur ~20 doivent les avoir TOUTES LES DEUX
- **Vérification** : pour chaque icône du set, détecter (a) `filter: drop-shadow(0 \d+px 0 white)` (ou équivalent inline) ET (b) `transform: rotate(-?[1-9]` (angle ≠ 0). Ratio ≥80%
- **Si fail (<80%)** : la signature sticker n'est pas portée par le set — quelques icônes "stickers" plus la plupart sans drop-shadow ou sans rotation. Re-dispatch designer : "AU MOINS 16 icônes du set DOIVENT avoir la signature sticker complète : DOUBLE drop-shadow (blanc 3-4px puis flou sombre) + rotation -3° à +5°. Pas de sticker sans ces 2 signatures intrinsèques."
