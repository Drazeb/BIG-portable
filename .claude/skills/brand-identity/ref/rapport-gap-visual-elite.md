# Rapport — Gap visuel BIG vs Elite Awards (avril 2026)

## Contexte

Audit de 88 sites Awards (startups primées, meilleurs sites de l'année) comparé aux outputs BIG.
Score actuel estimé : **~7.5/10**. Cible élite : **9-10/10**. Gap : ~1.5-2.5 points.

10 heroes Awards analysés en détail : ICOMAT (macro carbone), POUCH (3D liquide), GlyphicBio (sphères protéiques), MOAK (bouclier 3D), LiquidSolar (sphère ambre), MindJoin (ville futuriste), Anima (tronc fleuri), Nivora/"DESIGN FOR EVERYONE" (portrait full-bleed) + 2 complémentaires.

Le **Déficit 1** (~1 point) concerne la qualité intrinsèque des visuels générés (limite des outils MJ/Recraft) — partiellement hors de notre contrôle, traité dans l'Axe 1 de la session précédente.

Le **Déficit 2** (~1-1.5 points) concerne l'intégration et la composition du visuel dans le style-tile — c'est notre terrain d'action. C'est l'objet de ce rapport.

---

## Constat : ce que fait BIG aujourd'hui

Le hero type BIG est un **split** (texte à gauche ~55%, image à droite ~45%) :
- Le texte et l'image sont chacun dans leur zone, séparés par un gradient de liaison
- Le fond est une couleur unie (navy, crème, etc.) sans texture
- La typo du titre fait ~5-7vw
- L'image est le support du texte, pas le sujet principal
- Il n'y a aucun élément entre le texte et l'image (pas de forme, pas de ligne, pas de décor)
- L'espace est rempli : titre, sous-titre, body, bouton, tout est là

Le résultat est propre, professionnel, bien codé (CSS moderne, oklch, @layer, @property). Mais il manque le "wow" — la tension visuelle, l'audace compositionnelle, la profondeur qui distinguent un site élite d'un site bien fait.

---

## Les 8 leviers d'optimisation

### Levier 1 — Composition / Layout

**Ce que c'est** : la disposition des éléments dans l'espace du hero. Comment le texte et l'image sont positionnés l'un par rapport à l'autre.

**Le problème** : BIG utilise le split (texte à gauche, image à droite) dans ~71% des cas. Les sites Awards utilisent le split dans seulement 19% des cas. Les layouts dominants chez les Awards sont :
- **Full-bleed** (23%) : l'image occupe 100% de l'écran, le texte est posé par-dessus
- **Stacked** (27%) : le texte est en haut, l'image en dessous (ou l'inverse), en pleine largeur
- Full-bleed centré (10%), typo pure (9%), grid overlap/poster (6%)

**Ce qu'on veut** : que BIG produise des heroes en full-bleed et en stacked, pas seulement en split. Que les exemples HTML de référence montrent ces layouts pour que le LLM les reproduise (pattern "Code > Rules" : le LLM imite ce qu'il voit dans les exemples, pas ce qu'on lui dit en texte).

**Pourquoi ça marchera** : le pattern "Code > Rules" est documenté et vérifié dans le projet. Si les exemples HTML montrent du full-bleed et du stacked, le LLM les produira. S'ils ne montrent que du split, il fera du split — quel que soit le texte du prompt.

**Exemples Awards de référence** :
- ICOMAT : full-bleed, l'image de carbone EST tout le fond, le texte est en bas-gauche
- Nivora : full-bleed, portrait en fond, typo massive par-dessus
- GlyphicBio : stacked en haut (titre + baseline), visuel en dessous qui monte dans le texte

---

### Levier 2 — Layering texte/image

**Ce que c'est** : le fait que le texte et l'image s'entrelacent — des morceaux de l'image passent DEVANT le texte, ou le texte est positionné DANS l'image. C'est une question d'organisation des couches (z-index en CSS : quel élément est devant, lequel est derrière).

Ce n'est PAS du post-traitement sur l'image (levier 3). C'est de la composition spatiale : qui est devant qui.

**Le problème** : BIG ne fait JAMAIS d'interpénétration texte/image. Le texte est dans sa zone, l'image dans la sienne, les deux ne se touchent pas. 5/10 des heroes Awards analysés font du layering.

**Ce qu'on veut** : que des éléments visuels passent devant le texte (ou que le texte soit posé sur l'image), créant un entrelacement qui donne de la profondeur.

**Pourquoi ça marchera** : le layering se fait avec du CSS basique (z-index, position). C'est une technique que le LLM maîtrise parfaitement — il ne la fait pas parce que les exemples ne la montrent pas, pas parce qu'il ne sait pas.

**Exemples Awards de référence** :
- Anima : le tronc fleuri passe DEVANT certaines lettres de "Growing nature-inspired companies". Le texte est pris en sandwich dans l'image.
- MindJoin : les bâtiments de la ville futuriste passent devant et derrière les lettres géantes "MINDJOIN"
- Nivora : le texte "DESIGN FOR EVERYONE" est posé directement sur le visage, pas à côté
- LiquidSolar : "Fuel molecules from sun and air" est écrit DIRECTEMENT sur la sphère ambre

---

### Levier 3 — Post-traitement visuel (habillage CSS de l'image)

**Ce que c'est** : des effets CSS empilés PAR-DESSUS l'image pour la magnifier — sans modifier le fichier image lui-même. Le PNG MidJourney/Recraft reste tel quel, mais à l'écran il rend mieux grâce aux couches CSS superposées. C'est comme poser des calques par-dessus une photo imprimée.

Ce n'est PAS du layering (levier 2). Ici on ne parle pas de la position relative du texte et de l'image, mais de techniques visuelles appliquées à l'image pour améliorer son rendu.

**Les techniques concrètes** :

| Technique | Ce que ça fait | Effet visuel |
|-----------|---------------|-------------|
| Grain SVG (feTurbulence) | Ajoute un léger bruit de pellicule photo sur toute la surface | Enlève le côté "rendu numérique lisse" des images IA, donne un feeling plus organique, plus craft |
| Gradient overlay | Un dégradé de couleur semi-transparent posé par-dessus l'image | Fond l'image dans la palette de la marque, crée une liaison visuelle avec le texte et le fond |
| mix-blend-mode | Mélange mathématiquement les couleurs de l'image avec une couche colorée | Donne un traitement couleur distinctif (comme un filtre Instagram, mais en CSS — l'image prend la teinte de la marque) |
| mask-image | Un masque qui fait apparaître/disparaître des zones de l'image progressivement | Fondus doux, formes non-rectangulaires — l'image "sort" de sa boîte rectangulaire |
| backdrop-filter | Flou ou saturation appliqué à une zone au-dessus de l'image | Zones de texte lisibles sur l'image sans cacher l'image (comme un verre dépoli posé sur une partie) |
| clip-path | Découpe l'image ou des éléments dans des formes géométriques | Sortir du rectangle, créer des angles, des découpes expressives |

**Le problème** : ces techniques existent dans le catalogue CSS de BIG (html-showroom-spec.md §6), mais les exemples HTML de référence ne les utilisent pas sur les images. Le LLM ne les applique donc pas.

**Pourquoi ça marchera** : un visuel MJ "7.5/10" peut passer à ~8.5/10 visuellement grâce à l'habillage CSS. Le grain enlève le côté lisse IA, le blend-mode harmonise avec la palette, le mask-image l'intègre dans la composition. Les Awards font ça systématiquement : le visuel brut n'est jamais montré tel quel, il est toujours composé dans des couches CSS qui le magnifient.

---

### Levier 4 — 3ème couche graphique

**Ce que c'est** : des éléments visuels qui ne sont NI du texte utile NI l'image principale. Des éléments décoratifs "entre les deux" qui créent de la richesse et de la profondeur.

Analogie : dans un restaurant gastronomique, il y a le plat (le contenu/texte) et l'assiette (le fond). La 3ème couche, c'est la sauce décorative tracée sur l'assiette, le brin d'herbe posé dessus — des éléments qui ne sont ni le plat ni l'assiette mais qui font passer le tout de "bon" à "gastronomique".

**Le problème** : BIG compose en 2 couches (fond → texte ou fond → image). Les Awards composent en 3-4 couches (fond → image → éléments graphiques → texte). Un seul hero BIG a une 3ème couche (Camille C3, lignes de convergence) — et c'est le hero BIG le mieux noté.

**Types d'éléments de 3ème couche vus dans les Awards** :
- Nom de marque en oversize semi-transparent (POUCH : "POUCH" vertical géant à gauche)
- Annotations/labels flottants (GlyphicBio : "LKYCHLLV", "SS", "TGY" comme des labels de labo)
- Lignes, formes géométriques, grilles en arrière-plan
- Particules, éléments SVG décoratifs

**Pourquoi ça marchera** : ce sont des éléments HTML/CSS simples (un `<span>` avec une grosse font-size, opacity 0.1, position absolute). Le LLM sait les coder. Il faut juste les montrer dans les exemples.

---

### Levier 5 — Espace négatif

**Ce que c'est** : le vide intentionnel. Les zones du hero où il n'y a rien — ni texte, ni image, ni bouton. Juste du fond.

Analogie : une vitrine Apple (un iPhone seul sur 3m² de table blanche = luxe) vs une vitrine bazar (50 produits entassés = cheap). Le vide autour d'un objet le rend plus important et plus précieux.

**Le problème** : BIG remplit l'espace. Titre, sous-titre, overline, body text, bouton — tout est là, bien tassé. L'image remplit sa colonne. Pas de vide. Le résultat est informatif et complet mais il n'y a aucune tension, aucune respiration qui dit "ce truc est important, REGARDE".

**Ce qu'on veut** : des heroes où le visuel + texte n'occupent que 40-60% de la surface, le reste étant du vide intentionnel. Moins d'éléments textuels (pas forcément overline + titre + sous-titre + body + bouton à chaque fois).

**Exemples Awards de référence** :
- MOAK : bouclier 3D rouge au centre, ~60% de l'écran est du noir vide. Le texte est petit, en dessous. L'impact est maximum.
- ICOMAT : l'image carbone occupe 80% du hero, le texte "Engineer Without Limits" est petit en bas-gauche. Le vide entre le logo en haut et le texte en bas crée de la tension.

**Pourquoi ça marchera** : c'est un choix de composition, pas une technique CSS complexe. Il suffit de montrer dans les exemples des heroes avec moins d'éléments et plus de vide.

---

### Levier 6 — Typo plus grande

**Ce que c'est** : augmenter la taille des headlines hero de ~5-7vw (BIG actuel) à 8-10vw minimum (standard Awards). vw = pourcentage de la largeur de l'écran, donc 10vw = le titre occupe ~10% de la largeur par caractère.

**Le problème** : les titres BIG sont lisibles et bien composés, mais ils manquent d'impact. Dans les Awards, le titre est souvent l'élément LE PLUS visible du hero — il occupe un tiers de l'écran.

**Exemples Awards de référence** :
- Nivora : "DESIGN FOR EVERYONE" en ~12vw, les lettres font la hauteur d'un tiers de l'écran
- MindJoin : "MINDJOIN" en ~15vw, occupe tout le haut du hero
- POUCH : "POUCH" vertical en ~20vw (!)

**Pourquoi ça marchera** : c'est une valeur CSS (font-size). Si les exemples de référence montrent des titres en 8-10vw, le LLM produira des titres en 8-10vw. C'est le levier le plus simple et le plus mécanique.

---

### Levier 7 — Inversion de hiérarchie image/texte

**Ce que c'est** : une option où l'image est la STAR du hero (70-100% de la surface) et le texte est secondaire — posé dedans, discret. C'est l'inverse de BIG aujourd'hui, où le texte est la star et l'image illustre.

**Le problème** : BIG traite systématiquement l'image comme un accompagnement du texte. Le texte occupe la majorité de l'attention, l'image est dans une colonne à côté. Dans les Awards, c'est souvent l'inverse : l'image crée l'émotion, le texte la nomme.

**Exemples Awards de référence** :
- ICOMAT : l'image de carbone occupe 100% du hero. Le texte "Engineer Without Limits" est petit en bas-gauche — il nomme l'émotion créée par l'image, il ne la crée pas.
- MOAK : le bouclier 3D est LE sujet. Le texte est une ligne en dessous.
- POUCH : le liquide bleu est partout. "Fuel Your Ambition" est petit en bas.

**Pourquoi ça marchera** : c'est un choix de composition (levier 1) combiné avec les proportions. Si un exemple HTML montre un hero où l'image fait 100% et le texte est petit, le LLM peut reproduire ce ratio. Ce n'est pas garanti à chaque run, mais c'est une option dans le répertoire.

**Lien avec d'autres leviers** : c'est une combinaison de Layout (#1) + Espace négatif (#5) + Typo (#6 inversé — ici la typo peut être plus petite parce que c'est l'image qui parle).

---

### Levier 8 — Nom de marque comme élément graphique

**Ce que c'est** : utiliser le nom de la marque (ou un mot-clé du concept) en taille oversize, semi-transparent, comme élément décoratif — pas comme texte à lire. C'est un sous-cas spécifique de la 3ème couche (levier 4).

**Exemple Awards de référence** :
- POUCH : le mot "POUCH" est écrit en énorme à la verticale sur le bord gauche du hero, en semi-transparent. On ne le "lit" pas — on le perçoit comme un élément graphique qui affirme l'identité de marque.

**Pourquoi c'est un levier séparé** : c'est le pattern de 3ème couche le plus reproductible et le moins risqué. Pas besoin de créer des formes ou des SVG complexes — c'est juste du texte CSS avec une grosse font-size et une faible opacité. C'est facile à coder pour le LLM et le résultat est immédiatement "élite".

**Priorité** : plus basse que les autres car c'est un cas particulier du levier 4.

---

## Stratégie d'implémentation

**Le levier principal** : modifier les exemples HTML de référence. Le pattern "Code > Rules" est le fondement de notre approche — le LLM reproduit ce qu'il VOIT dans les exemples, pas ce qu'on lui écrit dans les règles. Si les 6 exemples de style-tiles montrent du layering, de la 3ème couche, du grain, du full-bleed, le LLM le fera.

**Fichiers à modifier** :
- `examples/standard/style-tile-example-A.html` (curseur A=1)
- `examples/standard/style-tile-example-B.html` (curseur A=2)
- `examples/rupture/style-tile-example-C.html` (curseur A=3)
- `examples/standard/style-tile-example-E.html`
- `examples/standard/style-tile-example-F.html`
- `examples/rupture/style-tile-example-D.html`

**Fichiers à créer** :
- 1-2 exemples supplémentaires avec layouts stacked et full-bleed (pour diversifier au-delà du split)

**Fichiers à ajuster** :
- `phases/phase-4-styletile.md` — prompt du subagent Phase 4 (typo minimum, espace négatif)
- `ref/image-composition-patterns.md` — catalogue de patterns CSS (layering, post-traitement)

**Règle de travail** : une modification à la fois, test entre chaque, comparaison avant/après.

---

## Références visuelles

Les heroes Awards analysés sont archivés dans :
- `.claude/skills/brand-identity/outputs/Exemples Awards macro-abstract/` — 10 captures (ICOMAT, POUCH, GlyphicBio, MOAK, LiquidSolar, MindJoin, Anima, Nivora)
- `outputs/pattern-demo/` — audit des 88 sites, pages pédagogiques, démos de patterns

---

## Dernière mise à jour : 2026-04-01
