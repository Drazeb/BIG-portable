# 05 — Ornemental — Fiche slop / anti-slop

**Famille** : `05-ornemental` · **Dernière revue** : 2026-05-27 · **Prochaine revue** : 2026-08-27

**Sources scannées** : Cunard rebrand Pentagram (2024), Cartier digital identity (2024-2025), Spotify Wrapped 2024-2025 (COLLINS), Mast Brothers (2018-2026), Aesop Athens/Tokyo collections (2025), *Art Deco Returns to Branding* — It's Nice That (février 2025), Mucho Studio Bauhaus revival.

---

## À BANNIR — 8 anti-patterns datés

### `[ANTI-01]` Or jaune vif saturé (`#FFD700`-like)
- **Description** : utilisation du jaune vif comme accent "noble"
- **Preuve d'âge** : signature templates "vintage badge" Etsy 2014-2021
- **Signature slop** : kitsch immédiat, anti-luxe
- **Contre-exemple pro** : Cunard 2024 — cuivre patiné `oklch(0.65 0.10 60)` ou bronze sourd

### `[ANTI-02]` Cadre filigrane "vintage badge" surchargé
- **Description** : entourer chaque pictogramme d'un cadre ornemental complexe avec rubans, étoiles, lauriers
- **Preuve d'âge** : tendance "hipster badge" 2012-2016, mort depuis
- **Signature slop** : barbe + bûcheron + Brooklyn 2014
- **Contre-exemple pro** : Cartier 2024-2025 — géométrie rigoureuse sans cadre décoratif

### `[ANTI-03]` Lettering ornemental script italique cursif
- **Description** : police "script cursif" type calligraphique mariage 2010s
- **Preuve d'âge** : Wedding industry 2008-2018, contaminé l'ornemental brand
- **Signature slop** : kitsch, anti-pro
- **Contre-exemple pro** : Cunard 2024 — lettering géométrique propre art déco

### `[ANTI-04]` Symboles ésotériques génériques (œil, triangle, lune)
- **Description** : utilisation d'iconographie pseudo-mystique sans rapport avec la marque
- **Preuve d'âge** : tendance "mystic brand" 2018-2022 (skincare, wellness)
- **Signature slop** : New Age générique
- **Contre-exemple pro** : Aesop collections 2025 — symboles dérivés du lieu / produit spécifique

### `[ANTI-05]` Couleurs vives multicolores (>2 couleurs)
- **Description** : palette ornementale colorée vive (turquoise + corail + jaune + rose)
- **Preuve d'âge** : Cinco de Mayo 2014, Wes Anderson lite 2018
- **Signature slop** : confusion avec illustration vintage colorée
- **Contre-exemple pro** : 100% des refs pro — bichromie max (noir + 1 accent noble)

### `[ANTI-06]` Symétrie radiale parfaite figée
- **Description** : tout symétrique 360°, refus de tout casser la symétrie
- **Preuve d'âge** : signature "mandala templates" 2015-2020
- **Signature slop** : monotonie ornementale
- **Contre-exemple pro** : Mucho 2023 — symétrie axiale + asymétries calculées

### `[ANTI-07]` Texture "vieux papier" (sépia, taches, plis)
- **Description** : overlay "aged paper" pour simuler l'ancienneté
- **Preuve d'âge** : templates "vintage badge" 2014-2020
- **Signature slop** : faux-vintage cliché
- **Contre-exemple pro** : Cunard 2024 — propreté digitale, héritage par géométrie pas par texture

### `[ANTI-08]` Drop-shadow / depth effects sur l'ornemental
- **Description** : ombre portée sur les motifs ornementaux
- **Preuve d'âge** : confusion UI moderne / ornemental
- **Signature slop** : l'ornemental est par essence plat sur papier
- **Contre-exemple pro** : refs pro — aucun drop-shadow

---

## SIGNATURES PRO 2024-2026 — 5 patterns à reproduire

### `[SIG-01]` Géométrie sacrée stricte (cercles, triangles, hexagones imbriqués)
- **Description** : composition basée sur des formes géométriques pures empilées
- **Source** : Mucho Bauhaus revival (2023-2025), Cartier 2024
- **Implémentation** : SVG avec formes pures Bézier rigoureuses, symétries calculées

### `[SIG-02]` Symétries axiales fines + accents asymétriques calculés
- **Description** : symétrie principale + 1-2 éléments qui la cassent volontairement
- **Source** : Cunard rebrand 2024, Mast Brothers
- **Implémentation** : groupe symétrique + élément hors-axe

### `[SIG-03]` Bichromie noir + cuivre patiné (jamais or vif)
- **Description** : palette noble retenue, cuivre/bronze/laiton patiné comme unique accent
- **Source** : Cunard 2024, Hermès Heritage 2024
- **Implémentation** : 2 couleurs max, accent en `oklch(0.65 0.10 50-70)` cuivre

### `[SIG-04]` Lettering ornemental géométrique (pas cursif)
- **Description** : si lettrage, art déco géométrique (à la Cassandre), pas calligraphique
- **Source** : Cunard 2024, Spotify Wrapped 2024-2025
- **Implémentation** : police comme Major Mono Display, Big Shoulders, ou custom géométrique

### `[SIG-05]` Coins coupés (chamfered) signature art déco
- **Description** : refus du corner radius arrondi UI moderne, coins coupés à 45°
- **Source** : Cunard 2024, Cartier digital frames 2025
- **Implémentation** : `<polygon>` SVG avec coupes 45°, pas `<rect rx>`

---

## CHECKS MÉCANIQUES — 2 vérifications

### `[CHK-01]` Palette maximum 2 couleurs (+ neutre fond)
- **Règle** : ornemental pro = bichromie stricte
- **Vérification** : extraire fills/strokes, ≤3 valeurs uniques

### `[CHK-02]` Symétrie détectable (au moins 1 axe)
- **Règle** : ornemental contemporain repose sur symétries calculées
- **Vérification** : présence de `transform="scale(-1, 1)"` ou structure miroir évidente

### `[CHK-03]` INCARNATION VISIBLE — ≥30% des icônes du set 06.1 sont visiblement ornementales (symétrie axiale OU coins coupés chamfered OU lettering géométrique)
- **Règle** : `[SIG-01]` géométrie sacrée + `[SIG-02]` symétries axiales + `[SIG-05]` coins coupés chamfered DOIVENT être incarnés. Au moins 6 icônes sur ~20 doivent avoir au moins l'une des 3 signatures : (a) symétrie axiale visible (`transform="scale(-1, 1)"` ou structure miroir), (b) coins coupés à 45° au lieu de corner-radius arrondi (`<polygon>` au lieu de `<rect rx>`), (c) imbrication géométrique stricte (cercle + polygone régulier imbriqués)
- **Vérification** : pour chaque SVG du set, détecter (a) `transform="scale(-1` OU (b) `<polygon>` avec 8 points ou plus (chamfered) OU (c) ≥2 `<circle>` ou `<polygon>` concentriques. Ratio ≥30%
- **Si fail (<30%)** : les icônes sont génériques modernes (arrondies, asymétriques). La signature ornementale art déco n'est pas incarnée. Re-dispatch designer : "Au moins 6 icônes du set DOIVENT être visiblement ornementales : symétrie axiale franche, ou coins coupés 45° (chamfered), ou géométrie imbriquée concentrique. Refuser les coins arrondis 4-8px par défaut."
