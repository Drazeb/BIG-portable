# 06 — Flat illustré coloré — Fiche slop / anti-slop

**Famille** : `06-flat-illustre` · **Dernière revue** : 2026-05-27 · **Prochaine revue** : 2026-08-27

**Sources scannées (positions datées)** :
- Linear / Pitch / Arc / Substack / Mubi Notebook (juillet 2025)
- *The Death of Corporate Memphis* — Eye on Design AIGA, mai 2024
- *Why Big Tech Logos All Look the Same* — It's Nice That, juin 2023
- *Three Internet Aesthetics* — Toby Shorin, 2020 (taxonomie slop genres)
- COLLINS — Robinhood rebrand 2023, Pentagram Pitch case study 2024
- Order Design (Jesse Reed) — Mailchimp Illustration System v2 (2023)

---

## À BANNIR — 8 anti-patterns datés

### `[ANTI-01]` "Corporate Memphis" — figures humaines stylisées au cou-girafe
- **Description** : personnages au tronc allongé, membres simplifiés en formes pâteuses, têtes minuscules sur grands corps
- **Preuve d'âge** : style dominant 2017-2022 (Facebook, Slack, Headspace, Mailchimp v1), littéralement appelé "Corporate Memphis" — appellation péjorative documentée par Eye on Design AIGA 2024 ("The Death of Corporate Memphis")
- **Signature slop** : indissociable de l'ère pré-2023 — utiliser ce style EN 2026 signe une marque qui copie 5 ans en retard
- **Contre-exemple pro** : Linear 2025 — figures humaines réalistes avec proportions normales, ou abstraction non-figurative

### `[ANTI-02]` Palette pastel anémique (Headspace pâle, "Notion soft")
- **Description** : tons pastel délavés (lavande pâle, pêche pâle, sauge pâle, beige rosé), aucune couleur ne pop, palette qui ressemble à une bouillie de chambres d'enfant
- **Preuve d'âge** : signature 2018-2022 mainstream B2C SaaS ; *The Death of Corporate Memphis* AIGA 2024 cite cette palette comme co-tueur
- **Signature slop** : illisible, oubliable, interchangeable entre 50 marques
- **Contre-exemple pro** : Mubi Notebook 2024-2026 — fond profond + accents saturés qui pop ; Pitch 2024 — palette éditoriale contrastée

### `[ANTI-03]` Gradient lisse multi-couleurs (sunset gradient, mesh gradient)
- **Description** : dégradés tonal continu (lavande → pêche → corail), souvent en background ou fill principal
- **Preuve d'âge** : signature Instagram/Stripe 2017-2020, "mesh gradient" pic 2020-2022
- **Signature slop** : le flat illustré moderne fonctionne par JUXTAPOSITION d'aplats, pas par gradient lisse
- **Contre-exemple pro** : Order Design Mailchimp v2 (2023) — 100% aplats sans gradient continu

### `[ANTI-04]` Drop-shadow soft pastel généralisé sur tous les éléments
- **Description** : ombre portée diffuse (souvent colorée pastel) sur tous les objets de l'illustration, donnant un effet "tout flotte sur fond uni"
- **Preuve d'âge** : signature Dribbble 2016-2021, Material Design v2 spot illu
- **Signature slop** : produit l'effet "sticker enfantin" anti-pro
- **Contre-exemple pro** : Substack writers illustrations 2025 — zéro shadow, profondeur par superposition de plans

### `[ANTI-05]` Géométrie "blob" arrondie infantilisée
- **Description** : tous les objets ont des coins ultra-arrondis (radius 50%+), formes "haricot", silhouettes molles
- **Preuve d'âge** : signature 2018-2021 mainstream ("friendly UI" surjouée), critiquée comme "blanding" par The Verge 2022
- **Signature slop** : tueur d'autorité visuelle, infantilise toute marque sérieuse
- **Contre-exemple pro** : Linear marketing 2025 — angles francs, silhouettes assumées

### `[ANTI-06]` Mascotte / personnage récurrent qui parle au public
- **Description** : petite mascotte (renard, robot, blob coloré) qui apparaît dans toutes les illustrations
- **Preuve d'âge** : tendance B2C 2014-2020 (Duolingo, Mailchimp Freddie, etc.) — fonctionne UNIQUEMENT si la marque a effectivement une mascotte cœur
- **Signature slop** : inventer une mascotte uniquement pour habiller des illustrations = slop éhonté
- **Contre-exemple pro** : Mubi, Linear, Pitch — illustrations narratives sans personnage récurrent imposé

### `[ANTI-07]` Tous les objets cernés d'un stroke noir 2px uniforme
- **Description** : chaque forme aplat est entourée d'un trait noir 2px, comme un coloriage enfant
- **Preuve d'âge** : style "flat outline" générique 2016-2020 (vu dans Freepik / templates Envato gratuits)
- **Signature slop** : la combinaison "aplat + outline noir épais uniforme" est l'esthétique livre-de-coloriage, pas l'illustration éditoriale pro
- **Contre-exemple pro** : si stroke utilisé, il est dans une couleur de la palette (pas du noir par défaut) et son épaisseur varie par fonction

### `[ANTI-08]` Symbole de "fonctionnalité tech" en arrière-plan (graphes, % de croissance, engrenages)
- **Description** : l'illustration contient des symboles "tech-startup générique" — courbes ascendantes, pourcentages, engrenages, écran avec graphes
- **Preuve d'âge** : automatisme B2B SaaS 2015-2022 ("nous sommes une boîte tech, mettons des graphes")
- **Signature slop** : le flat illustré pro raconte une scène, pas un dashboard
- **Contre-exemple pro** : Pitch 2024 — illustrations qui montrent l'usage humain, pas l'interface du produit

---

## SIGNATURES PRO 2024-2026 — 5 patterns à reproduire

### `[SIG-01]` Palette charpentée 3-4 couleurs avec UN accent qui pop
- **Description** : palette restreinte (un fond, deux neutres, un accent saturé), souvent un ton chaud (laiton, ocre, terracotta) ou froid (cobalt, indigo) qui structure la lecture
- **Source** : Mubi Notebook 2024-2026, Pitch 2024, Linear 2025
- **Implémentation** : limiter explicitement à 4 couleurs hexadécimales distinctes dans le SVG ; UN accent occupe ≤15% de la surface

### `[SIG-02]` Profondeur par superposition de plans aplats
- **Description** : effet "papier découpé" — 2-4 plans aplats superposés avec un léger décalage, créant une profondeur sans gradient
- **Source** : Substack writers illustrations 2025, Arc Browser 2024
- **Implémentation** : 2-4 `<path>` ou `<polygon>` avec fills différents, légèrement décalés en `transform: translate()`

### `[SIG-03]` Grain noise overlay subtil (signature 2024-2026)
- **Description** : texture grain photoshop discrète sur les aplats, casse le côté "trop vectoriel propre"
- **Source** : Pitch 2024, Mubi Notebook 2025, COLLINS projets récents (2024-2025)
- **Implémentation** : filter SVG `<feTurbulence baseFrequency="0.6"/>` + `<feColorMatrix>` opacity 0.05-0.1 sur les aplats principaux

### `[SIG-04]` Composition narrative : scène complète, pas symbole isolé
- **Description** : l'illustration raconte un moment d'usage (un humain en action, un objet métier en contexte, un environnement situé) — pas juste un symbole flottant
- **Source** : 100% des refs pro flat illustré moderne ; Order Design Mailchimp v2 (2023) — chaque illu = mini-scène
- **Implémentation** : chaque icône métier en `06.4` doit contenir ≥2 éléments narrativement liés (un objet ET un contexte)

### `[SIG-05]` Variante mode sombre cinéma (clair-obscur)
- **Description** : fond profond (charbon, indigo nuit, bordeaux), accents lumineux qui pop (laiton, ivoire, ocre chaud) — registre "flat illustré cinéma"
- **Source** : Mubi Notebook 2024-2026, Pitch 2024, Arc dark mode 2025
- **Implémentation** : si la palette de la marque est nocturne / dark mode, basculer en mode cinéma — fond `oklch(0.15 ...)`, accents `oklch(0.7 0.15 70)` chaleureux

---

## CHECKS MÉCANIQUES — 2 vérifications

### `[CHK-01]` Compte des couleurs distinctes par illustration : entre 3 et 6
- **Règle** : chaque illustration `06.4` doit contenir entre 3 et 6 valeurs `fill` ou `stroke` distinctes
- **Vérification** : extraire les valeurs `fill="#..."` et `stroke="#..."` du SVG, compter les uniques
- **Si fail** :
  - `<3` : illustration trop monochrome (probablement déguisée en pictogramme géo)
  - `>6` : palette débordée (probablement slop pastel)

### `[CHK-02]` Aucun `linearGradient` ni `radialGradient` lisse multi-couleurs
- **Règle** : pas de dégradé tonal continu (le flat moderne fonctionne par juxtaposition d'aplats)
- **Vérification** : `<linearGradient>` ou `<radialGradient>` avec ≥3 `<stop>` de teintes différentes = fail. Bichrome aplat assumé (2 stops) = OK
- **Si fail** : la famille bascule vers gradient mesh années 2020, signal slop fort

### `[CHK-03]` INCARNATION VISIBLE — ≥30% des icônes du set 06.1 ont ≥3 plans aplats superposés
- **Règle** : `[SIG-02]` profondeur par superposition de plans aplats DOIT être incarnée. Au moins 6 icônes sur ~20 doivent contenir ≥3 paths/polygones avec fills de couleurs DIFFÉRENTES (pas la même couleur répétée)
- **Vérification** : pour chaque SVG du set, extraire tous les `fill="..."` (sauf `fill="none"`), compter les valeurs distinctes. Si ≥3 distinctes → l'icône compte. Ratio ≥30%
- **Si fail (<30%)** : les icônes sont mono-aplat (juste une silhouette + 1 accent), pas vraiment "flat illustré" mais "flat plat". La profondeur par plans n'est pas incarnée. Re-dispatch designer : "Au moins 6 icônes du set DOIVENT contenir 3+ plans aplats superposés (par exemple : fond + objet principal + détail + accent — 4 couleurs distinctes). Pas juste 1 silhouette + 1 accent ocre."
