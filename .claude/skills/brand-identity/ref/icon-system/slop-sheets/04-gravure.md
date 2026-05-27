# 04 — Gravure / linocut — Fiche slop / anti-slop

**Famille** : `04-gravure` · **Dernière revue** : 2026-05-27 · **Prochaine revue** : 2026-08-27

**Sources scannées (positions datées)** :
- Aesop website (sept 2025), Mucho Studio archive (2023-2025), Loewe Foundation Craft Prize (2024-2025)
- *Linocut Renaissance in Digital Editorial Design* — Eye on Design AIGA, avril 2024
- Brand New chronique Aesop Online 2.0 (février 2025), Pentagram Books portfolio (2024)
- *Crafting Marks in 2025* — Velvet Spectrum interview Type 01, juin 2025
- The Atlantic Daily newsletter (2025 — Helga Cocco illustrations)

---

## À BANNIR — 8 anti-patterns datés

### `[ANTI-01]` Hachures parallèles régulières strictement à 45°
- **Description** : pattern SVG `lines 45°` figé sur toute l'illustration, espacement uniforme, zéro variation
- **Preuve d'âge** : preset Photoshop "Engraving Lines 45°" — Adobe Stock + Envato Elements 2015-2022, vu 10 000 fois
- **Signature slop** : la régularité parfaite TUE l'esthétique gravure (un graveur ne tient pas le burin parfaitement à 45° sur 10cm)
- **Contre-exemple pro** : Aesop pictogrammes 2025 — hachures rotation 8-15° suivant le volume signifié

### `[ANTI-02]` Aplat noir 100% K sans aucune hachure
- **Description** : silhouette pleine noire sans nuance, équivalent à un "icon-solid" déguisé en gravure
- **Preuve d'âge** : confusion fréquente "gravure = noir et blanc plein" — vu dans templates Behance "engraving icon set" 2018-2023
- **Signature slop** : c'est de la SILHOUETTE, pas de la gravure. La gravure JOUE entre l'aplat ET l'absence ET les hachures intermédiaires
- **Contre-exemple pro** : Loewe Craft Prize 2024 — chaque pictogramme contient au moins 3 niveaux de gris (aplat / hachure dense / hachure clairsemée)

### `[ANTI-03]` Filter `feTurbulence` baseFrequency > 0.1 (texture organique surjouée)
- **Description** : la texture devient un bruit numérique sale plutôt qu'un grain crédible de bois/lino
- **Preuve d'âge** : tutoriels "SVG grunge texture" Codrops 2019-2021
- **Signature slop** : le bruit est visiblement procédural — un graveur ne fait pas du noise random
- **Contre-exemple pro** : The Atlantic Daily 2025 (Helga Cocco) — texture appliquée uniquement sur les aplats noirs, baseFrequency 0.03-0.05 max

### `[ANTI-04]` Drop-shadow sur les éléments gravure
- **Description** : ombre portée CSS / SVG sur l'icône (`filter: drop-shadow(...)`)
- **Preuve d'âge** : automatisme UI moderne appliqué à tort sur du contenu illustratif
- **Signature slop** : tueur immédiat — la gravure n'a JAMAIS d'ombre portée. C'est un médium plat sur papier
- **Contre-exemple pro** : 100% des références Aesop/Hermès/Loewe — zéro shadow

### `[ANTI-05]` Tracé Bézier trop lisse, parfaitement vectoriel
- **Description** : courbes Bézier "Photoshop pen tool perfection", angles parfaitement adoucis
- **Preuve d'âge** : esthétique vectorielle générique Adobe Illustrator 2010+
- **Signature slop** : la gravure a des **irrégularités de trait** (le burin glisse, dérape, change de pression)
- **Contre-exemple pro** : Mucho Studio "Edicions del Periscopi" (2023) — tracés délibérément irréguliers, ruptures de pression visibles

### `[ANTI-06]` Palette > 2 couleurs
- **Description** : tentative de gravure colorée avec 3+ couleurs distinctes (verts, bleus, rouges, etc.)
- **Preuve d'âge** : confusion gravure ↔ illustration vintage colorée, vu dans templates "vintage icon pack" 2017-2022
- **Signature slop** : la gravure historique est monochrome ou bichrome (noir + 1 accent), point. Au-delà → illustration vintage, pas gravure
- **Contre-exemple pro** : Aesop, Hermès Heritage, Loewe — strictement monochrome ou bichrome (noir + un terreux)

### `[ANTI-07]` Frame décorative ornementale englobante (cadre filigrane "vintage")
- **Description** : icône entourée d'un cadre ornemental art nouveau / blason
- **Preuve d'âge** : confusion gravure ↔ ornemental, esthétique "vintage badge" Etsy 2014-2021
- **Signature slop** : c'est de l'ornemental DÉGUISÉ en gravure. La gravure éditoriale moderne n'a pas de frame décorative
- **Contre-exemple pro** : The Atlantic, Mubi Notebook — icône respire dans son espace sans cadre

### `[ANTI-08]` Gradient (linéaire ou radial) en lieu et place des hachures
- **Description** : utilisation d'un dégradé pour simuler l'ombre/profondeur
- **Preuve d'âge** : automatisme SVG moderne mal calibré sur la famille gravure
- **Signature slop** : tueur intrinsèque — la gravure est par définition aplat/hachure. Tout gradient = pas gravure
- **Contre-exemple pro** : 100% des refs pro — zéro `linearGradient` / `radialGradient` SVG

---

## SIGNATURES PRO 2024-2026 — 5 patterns à reproduire

### `[SIG-01]` Hachures à rotation variable selon volume signifié
- **Description** : hachures à 5-15° pour zone d'ombre légère, 30-45° pour ombre moyenne, croisillons (crosshatch) pour ombre dense
- **Source** : Aesop website pictogrammes (sept 2025), Loewe Craft Prize illustrations (2024)
- **Implémentation** : 2-3 patterns SVG distincts dans `<defs>`, appliqués sur des paths différents selon le niveau d'ombre

### `[SIG-02]` Trait variable (`stroke-width`) sur le même path
- **Description** : épaisseur du trait varie le long du même contour (simulation pression burin)
- **Source** : Mucho Studio Edicions del Periscopi (2023), Helga Cocco illustrations (2024-2025)
- **Implémentation** : superposer 2-3 `<path>` identiques avec stroke-width différents, ou décomposer l'icône en segments avec stroke variable

### `[SIG-03]` Combinaison aplat + hachure + vide dans le MÊME pictogramme
- **Description** : un objet gravé montre au moins 3 traitements : une zone aplat noir, une zone hachurée intermédiaire, une zone laissée vide (lumière)
- **Source** : 100% des pictogrammes pro gravure observés (Aesop, Hermès, Loewe, Mucho)
- **Implémentation** : décomposer chaque icône en 3 zones avec fills différents (`black`, `url(#hatch)`, `none`)

### `[SIG-04]` Bichromie noire + accent terreux RARE
- **Description** : noir + 1 seule couleur de soutien (rouge sang #8B2424, ocre #C5772E, bleu d'encre #1F3A5F), utilisée seulement sur 1-2 détails (pas en aplat large)
- **Source** : Hermès Heritage 2024, Margiela cards (2024-2025)
- **Implémentation** : 95% des fills en `#1a1a1a`, 5% en accent terreux ponctuel

### `[SIG-05]` Centrage solennel ou décentrement asymétrique éditorial
- **Description** : composition soit parfaitement centrée (gravité classique), soit décentrée d'un cran (1/3 vs 2/3) — refus du centrage "icon UI" tiède
- **Source** : The Atlantic Daily (Helga Cocco 2024-2025), Mubi Notebook (2024-2026)
- **Implémentation** : `viewBox` calé délibérément (centrage parfait OU asymétrie franche), pas de marge molle

---

## CHECKS MÉCANIQUES — 2 vérifications

### `[CHK-01]` Au moins 1 `<pattern>` SVG défini ET utilisé
- **Règle** : Le SVG doit contenir au moins un `<pattern id="...">` dans `<defs>`, ET au moins un `fill="url(#pattern_id)"` qui l'utilise
- **Vérification** : `grep` du HTML — présence d'un `<pattern` ET d'un `fill="url(#` correspondant
- **Si fail** : c'est qu'il n'y a pas de hachures du tout — pas une gravure

### `[CHK-02]` Aucun `linearGradient` ni `radialGradient` ni `filter: drop-shadow`
- **Règle** : tueurs intrinsèques de la famille
- **Vérification** : `grep -c 'linearGradient\|radialGradient\|drop-shadow'` doit retourner 0

### `[CHK-03]` INCARNATION VISIBLE — ≥30% des icônes du set 06.1 utilisent vraiment les hachures (pas juste une démo unique)
- **Règle** : `[SIG-01]` hachures rotation variable + `[SIG-03]` aplat + hachure + vide DOIVENT être incarnés sur ≥30% du set, pas juste sur 1 icône démo. Au moins 6 icônes sur ~20 doivent contenir un `fill="url(#pattern_xxx)"` qui pointe vers un `<pattern>` de hachures défini dans `<defs>`
- **Vérification** : (a) compter les `<pattern id="..."` dans les `<defs>` du HTML → au moins 1 pattern existe ; (b) pour chaque SVG icône du set 06.1, vérifier la présence d'au moins 1 `fill="url(#pattern_id)"` qui pointe vers un de ces patterns ; (c) ratio (icônes hachurées / total) doit être ≥30%
- **Si fail (<30%)** : la signature gravure n'est pas incarnée — c'est de la déclaration verbale ("4 hachures SVG distinctes 0°, 15°, 45°, crosshatch 30°" en légende texte) sans application visuelle sur les icônes. C'EST EXACTEMENT LE BUG OBSERVÉ SUR CAMILLE 0527. Re-dispatch designer : "Au moins 6 icônes du set 06.1 DOIVENT contenir une zone hachurée visible (`fill="url(#hatch)"`). Ne pas se contenter de mentionner les hachures dans la légende — APPLIQUER les patterns sur les vraies icônes UI."
- **Si fail** : la famille n'est pas respectée, c'est du flat illustré ou du pictogramme géo déguisé
