# 04 — Gravure / linocut

## Nom canonique et alias
- **Nom canonique** : Gravure / linocut
- **Alias usuels** : woodcut, engraving, linogravure, scratchboard, étching, hand-printed mark
- **ID stable** : `04-gravure`

## Époque d'origine et revivals
- **Origine** : techniques de gravure sur bois (woodcut, 15e siècle), linogravure (début 20e), gravure sur métal (eau-forte, 17e+)
- **Revivals modernes** :
  - 1990s-2000s : illustration éditoriale presse (New York Times Op-Ed, The Guardian Long Reads, The Atlantic)
  - 2018-2026 : renouveau "brand maison" — Hermès digital, Aesop digital, Margiela cards, Loewe Foundation
  - Période actuelle : pic de présence dans les marques artisanales premium et l'édition indépendante

## Traits formels
- **Stroke** : trait épais haut-contraste (0.5pt très fin pour les détails, 2-4pt pour les contours principaux), rythme variable
- **Fill** : aplats noirs francs ou hachures parallèles (`pattern` SVG), souvent contre-tailles (croisillons) pour les zones d'ombre intermédiaires
- **Géométrie** : irrégularités contrôlées, asymétries, refus de la perfection vectorielle Bézier
- **Texture** : grain visible — la matérialité du burin/gouge/pointe-sèche est SIGNATURE, pas du bruit
- **Composition** : centrage solennel ou décentrement asymétrique éditorial

## Marques contemporaines qui l'emploient (2024-2026)
1. **Aesop** — pictogrammes catégorie produit sur site (gravure trait, observé sept 2025) — [aesop.com](https://www.aesop.com)
2. **Hermès Heritage** — sections savoir-faire (gravures façon Émile Hermès, 2024)
3. **Loewe Foundation** — programme Crafts Prize, illustrations gravure (2024-2025)
4. **The Atlantic Daily** — illustrations en-tête newsletter (linogravure, 2025)
5. **Editions du Seuil — collection Fiction** — pictogrammes collection (gravure contemporaine, 2024)

## Couleurs natives
- **Palette principale** : monochrome noir profond sur fond crème/papier (le contraste IS le médium)
- **Bichromie tolérée** : noir + 1 accent terreux (rouge sang, ocre, bleu d'encre) — JAMAIS plus de 2 couleurs
- **Inversion** : crème/blanc sur fond sombre fonctionne bien (signature éditoriale moderne)
- **Pas de gradients** — la gravure est par essence aplat/hachure, pas continuum tonal

## Formats natifs en stack Claude Code
- **SVG inline avec `<pattern>` hachures** : pattern `lines 45°` ou `crosshatch`, rotation 5-15° suivant le volume signifié
- **Combine fills aplats + hachures dans la même icône** : signature linocut (un détail aplat, une zone hachurée pour l'ombre, une zone vide pour la lumière)
- **Filter `feTurbulence` léger** : optionnel pour donner une micro-texture organique au trait (à doser, max baseFrequency 0.05)
- **Path strokes variable-width** : utiliser plusieurs `<path>` superposés avec stroke-width différents pour simuler la pression variable du burin
- **Pas de gradient SVG, pas de drop-shadow** : tueurs immédiats de l'esthétique gravure

## Grain naturel (où la famille brille)
- Hero éditorial avec narration ancienne
- Illustration de chapitre / éditorial long-form
- Pictogrammes catégorie produit en mode artisanal
- Marques premium qui revendiquent un héritage / savoir-faire / patrimoine
- Documents print transposables 1:1 du print au digital

## Compatibilités concept (tons)
- **Sérieux** : excellent (gravité naturelle du médium)
- **Premium / luxe** : excellent (signature heritage)
- **Artisanal / savoir-faire** : excellent (matérialité revendiquée)
- **Méthodique / rigoureux** : très bon (précision du burin)
- **Patrimoine / héritage** : excellent
- **Cinématographique / nocturne** : très bon (palette monochrome + textures)
- **Brut / contre-culture** : moyen (peut basculer si trop éditorial)
- **Ludique / accessible** : faible (médium intrinsèquement formel)
- **Tech-startup neutre** : faible (mauvais matching de codes)

## Incompatibilités évidentes
- Marques B2C SaaS friendly mainstream → faux match, illisible pour la cible
- Marques fintech / banque digitale → trop éditorial, manque la "modernité" attendue
- Marques produits enfants → registre trop formel
- Concepts qui demandent multicolore vif → la famille n'a pas cette palette
- Hero animés avec micro-interactions ludiques → la gravure est statique par nature

## Sources datées
- Aesop — site site catégorie produit, observé septembre 2025
- The Atlantic — newsletter Daily, mars 2025 (illustrations Helga Cocco)
- Loewe Foundation Craft Prize 2024 — site événementiel
- *Linocut Renaissance in Digital Editorial Design* — Eye on Design, AIGA, avril 2024
- Brand New — chronique Aesop Online 2.0, février 2025
- Mucho Studio — projet "Edicions del Periscopi" (2023), références gravure contemporaine
- *Crafting Marks in 2025* — Velvet Spectrum (Maxime Goyet), interview Type 01 magazine, juin 2025
