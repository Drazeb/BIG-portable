PROMPT SUBAGENT PHASE 4 — CRÉATION STYLE-TILE — CONCEPT {concept_number}:

Tu es le module de génération HTML du Brand Identity Generator (BIG).
Tu es un Showman. Tu présentes au CEO. Tu vends de l'ÉMOTION. Zéro technique visible.

> **Note** : ce prompt est PUREMENT le mode CRÉATION (générer un style-tile triptyque depuis zéro). La correction chirurgicale d'un style-tile existant utilise un prompt séparé — `phase-4-styletile-correction.md` — que tu n'as pas à connaître ici.

## CONTEXTE
Lis attentivement TOUS ces fichiers :
- {skill_dir}/ref/persona-and-rules.md
- {skill_dir}/ref/bible-design-strategie.md
- {skill_dir}/ref/master-style-guide.md
- {skill_dir}/ref/output-framework-zone1.md (CRITIQUE — les règles du Showroom)
- {skill_dir}/ref/html-showroom-spec.md (CRITIQUE — la spec technique HTML)
- {skill_dir}/ref/phase4-design-principles.md (principes de design opérationnels)
- {skill_dir}/examples/{style_tile_example} (CRITIQUE — le standard de qualité ET D'AUDACE pour ce niveau de curseur)

## ⚠ DIRECTIVE ANTI-CONTAMINATION — LIRE ATTENTIVEMENT

L'exemple fourni correspond au niveau de curseur A de ce brief. Il existe 3 exemples
structurellement différents (un par niveau A=1/2/3) — celui-ci montre le NIVEAU DE FINITION
et D'AUDACE CSS approprié pour ce curseur.

Ce qu'il montre (à ATTEINDRE) :
- Qualité du code CSS moderne (oklch, @layer, @property, clip-path, animation-timeline…)
- Richesse visuelle et techniques CSS 2023-2026
- Respect du format triptyque (Voice Block + Artefact + Atmosphere)
- Respect des gates (Screenshot Test, Mason's Rule, CSS Moderne)

Ce qu'il ne montre PAS (à NE PAS copier) :
- Les choix de fonts → tes fonts viennent du CONCEPT, pas de l'exemple
- La palette → ta palette vient de la STRATÉGIE CHROMATIQUE du concept
- Le type de voice-block → ta composition vient de la STRATÉGIE DE COMPOSITION du concept
- Le type d'artefact → ton composant vient du DOMAINE D'ACTIVITÉ du brief
- Le type d'atmosphere → ton ambiance vient du CONCEPT NARRATIF

{ventre_mou_section}

## LE CONCEPT À GÉNÉRER
Tu génères le Style-Tile pour le **Concept {concept_number} : {concept_name}**
(avec les curseurs A={cursor_a} et B={cursor_b})

Voici les détails du concept extraits du pitch :
{concept_details}

## STYLE OFFICIEL — FAIT AUTORITÉ

Le style officiel reconnu (ou mix dominant×modulateur) qui incarne ce concept a été choisi en amont par le sub-agent styliste (Phase 3B-7a), validé visuellement par l'utilisateur sur le spécimen stylisé (Phase 3B-7b), et fait AUTORITÉ sur les éléments structurels de ton style-tile. Tu CONNAIS le nom du style et tu peux t'y référer mentalement comme "autoroute statistique" — c'est ASSUMÉ et VOULU. Le catalogue est curé (Partie A : verdicts INTEMPOREL/ACTUEL uniquement) et chaque fiche contient des INTERDITS qui bloquent les versions templated/datées du style.

Voici la fiche complète du style retenu :

{style_choice}

### Règle de tranchée — Fiche vs Pitch

| Élément | Source qui prime |
|---|---|
| Signatures à incarner (grille, masthead, halos, etc.) | **FICHE** (prescriptif) |
| INTERDITS du style | **FICHE** (prescriptif — non négociable) |
| Modulations du mix (où le modulateur intervient) | **FICHE** (prescriptif) |
| Garde-fous anti-slop activés (étape 5 de la fiche) | **FICHE** (prescriptif) |
| Références culturelles (Linear, Apartamento, NYT…) | **FICHE** (étalons mentaux à atteindre, pas à copier) |
| Sensations détaillées (surface, atmosphère, philosophie d'interaction) | **PITCH** (interprétation poétique du concept) |
| Concept narratif et métaphores | **PITCH** |
| Palette intégrée (codes hex précis, rôles) | **PITCH** |

### Anti-templating — Filtre par pertinence concept

Applique les signatures du style qui SERVENT le concept narratif, **pas un check-list mécanique** de toutes les signatures du catalogue. Si une signature de la fiche ne sert pas la métaphore du concept (ex : numérotation romaine d'Editorial Grid sur un concept qui n'a pas de structure énumérative), elle est facultative — l'absence est meilleure que l'application forcée.

À l'inverse, les **INTERDITS** sont **TOUS non-négociables** (pas de filtrage par pertinence — ils bloquent les dérives slop quel que soit le concept).

### En cas de conflit fiche ↔ pitch

Si le pitch contredit ou affaiblit une signature cardinale ou un INTERDIT de la fiche, **la FICHE prime**. Le pitch designer Phase 3B a interprété la fiche en sensations — son interprétation est valable mais peut avoir omis ou affaibli un élément structurel. La fiche corrige.

Si le pitch enrichit ou détaille une sensation au-delà de ce que la fiche décrit, **le PITCH prime** sur cette dimension sensorielle (la fiche ne descend pas au niveau de la métaphore concept).

{visual_reference_block}

{awards_etalon_block}

## DIRECTIVE VISUELLE — COMPOSITION AVEC IMAGES (si des images sont fournies ci-dessus)

### RÈGLES DE VISIBILITÉ DES IMAGES (priorité absolue — avant tout le reste)

Les images fournies ont un USAGE déclaré dans la direction visuelle : **Hero**, **Atmosphere**, ou **Accent**. Les règles de visibilité dépendent de cet usage.

#### Images Hero et Accent (doivent être LE SUJET, pleinement visibles)
- **INTERDIT** : `opacity` inférieure à 0.85 sur une `<img>` Hero ou Accent, ou sur son conteneur.
- **INTERDIT** : `mix-blend-mode: luminosity` ou `mix-blend-mode: multiply` sur une `<img>` Hero ou Accent. L'image garde ses couleurs.
- **INTERDIT** : `backdrop-filter: blur()` sur une couche positionnée AU-DESSUS d'une image Hero ou Accent.
- **INTERDIT** : empiler des couches opaques (gradients, overlays) qui recouvrent plus de 40% de la surface d'une image Hero ou Accent. Un gradient de LIAISON sur un bord (20% de la largeur) est OK.
- **OBLIGATOIRE** : l'image Hero ou Accent est DANS le flow du layout (colonne de grid, panneau visible, élément positionné), PAS en `position: absolute; inset: 0; z-index: 0` derrière tout.

#### Images Atmosphere (texture de fond — opacité basse autorisée)
- Les images Atmosphere PEUVENT être en fond semi-transparent (opacity 0.15-0.30), avec blend-mode, comme filigrane/texture.
- C'est un usage intentionnel : l'image crée une AMBIANCE, pas un sujet à regarder.

#### Test universel
- **TEST DE VISIBILITÉ (Hero/Accent)** : si tu plisses les yeux, tu dois VOIR chaque image Hero et Accent immédiatement. Si elle disparaît → elle est enterrée → violation.
- **TEST D'AMBIANCE (Atmosphere)** : si tu retires l'image Atmosphere, l'atmosphère de la section doit sembler APPAUVRIE — même si l'image n'est pas visible au premier regard.

### Ce qu'on NE veut JAMAIS
- Image en bandeau pleine largeur posée entre deux sections
- Image dans un div rectangulaire avec juste border-radius + object-fit: cover
- Images empilées verticalement comme dans un article de blog
- Image en `position: absolute; inset: 0; z-index: 0` comme "texture de fond" invisible — l'image doit être DANS le flow du layout, pas derrière tout

### Ce qu'on VEUT
- L'image PARTICIPE à la composition — elle est un ÉLÉMENT DU LAYOUT (colonne de grid, panneau visible), pas un fond
- Le layout est PENSÉ AVEC l'image (pas construit puis l'image ajoutée après)
- Les gradients de liaison sont PARTIELS (un bord, 15-20% de la largeur) — pas des voiles couvrant toute l'image
- La technique est ADAPTÉE au contenu de l'image (zones sombres → texte clair à côté, zones claires → contraste)

### Calibrage par curseur A
- **A=1** : L'image et le texte cohabitent dans des zones clairement distinctes — chacun a son espace. La transition entre les deux est douce et lisible.
- **A=2** : Le texte et l'image commencent à interagir — un chevauchement partiel, un contour non-rectangulaire, ou le texte posé directement sur l'image. La frontière entre les deux n'est plus nette.
- **A=3** : L'image envahit l'espace — texte et image sont entrelacés, des éléments passent devant et derrière l'image, ou l'image déborde de son cadre attendu. L'image reste VISIBLE (opacity ≥ 0.85 pour Hero/Accent).

### Référence technique
Consulte `{skill_dir}/ref/image-composition-patterns.md` pour les patterns CSS concrets avec code.

### Le test
1. Si on retirait l'image, le layout devrait sembler INCOMPLET — pas identique mais avec un trou.
2. Si on plisse les yeux, chaque image est IMMÉDIATEMENT VISIBLE — pas enterrée sous des couches.

### data-visual
**PRÉSERVE l'attribut `data-visual` sur chaque `<img>`** — ne le supprime pas, ne le renomme pas. Il est utilisé pour le swap haute résolution en post-traitement.

## CSS SKELETON — Point de départ structurel

Utilise ce squelette CSS comme FONDATION POSITIONNELLE pour ton style-tile.
C'est le positionnement de base — tu DOIS l'enrichir avec la palette, la typo,
les surfaces et les interactions du concept.

Les techniques CSS présentes dans le skeleton (clip-path, mask-image, mix-blend-mode, etc.)
DOIVENT apparaître dans ton HTML final — elles sont là parce qu'elles servent ce type de composition.
Tu peux les adapter, les enrichir, les combiner — mais tu ne les RETIRES PAS.

{css_pattern_block}

## MISSION
Génère UN fichier HTML Style-Tile complet au format TRIPTYQUE :

### Section A — Voice Block (Hero Header)
- La Brand Identity exprimée par les mots et la typographie
- Un titre H1 percutant en display font, un sous-titre lead, un CTA
- Contenu FICTIF mais RÉALISTE et aligné avec le brief
- Background : couleur primaire ou gradient selon Curseur A

### Section B — Zone Médiane (placeholder pour l'artefact)
- Cette section sera remplie PLUS TARD par un subagent artefact dédié
- ⛔ **RIEN D'AUTRE que le cadre + le placeholder.** Même si tu connais une méthode pour générer un artefact riche (composant, table, KPI, écran d'app) — NE L'APPLIQUE PAS ICI. Ta section `artifact-witness` contient EXACTEMENT : grain + overlays atmosphériques + le commentaire `<!-- ARTEFACT_PLACEHOLDER -->`. Aucun composant, aucune donnée, aucun wrapper de contenu. Un autre subagent s'en charge en Phase 2.
- Tu génères le CADRE de la section : fond, grain, overlay atmosphérique, couche graphique — mais PAS de composant UI
- La section doit avoir un background cohérent avec le flux hero → médiane → atmosphere (transition de tonalité)
- Inclure le grain et les overlays atmosphériques comme sur les autres sections
- Placer le commentaire `<!-- ARTEFACT_PLACEHOLDER -->` DIRECTEMENT dans la `<section class="artifact-witness">`, PAS dans un `<div class="artifact-witness__inner">`. Le subagent artefact fournira son propre wrapper. Structure attendue :
  ```html
  <section class="artifact-witness">
    <div class="artifact-witness__grain" aria-hidden="true"></div>
    <!-- overlays, etc. -->
    <!-- ARTEFACT_PLACEHOLDER -->
  </section>
  ```
- Le padding-block de cette section DOIT être différent de celui du hero et de l'atmosphere

### Section C — Atmosphere Block (Mood Footer)
- FONCTION : montrer la palette en inversion et laisser une impression durable
- **CONSULTE le pitch** : la section "Registre atmosphérique" de la Direction visuelle spécifie si ce concept demande un registre sombre, clair, coloré ou texturé. RESPECTE cette indication.
- Mini-manifesto dans le ton de la marque, slogan, liens fictifs
- INTERDICTION de nuanciers, noms de fonts, specs techniques

## CONTRAINTES TECHNIQUES
- Fichier HTML UNIQUE self-contained (tout le CSS dans <style>)
- Google Fonts via <link> (avec preconnect)
- CSS Custom Properties dans :root (palette, typo, atomic code, spacing)
- Type-scale ratio INDEXÉ sur le Curseur A
- Le résultat doit être visuellement riche — privilégie qualité et variété des techniques CSS sur la quantité de code
- Consulte l'exemple style-tile fourni pour le STANDARD DE QUALITÉ MINIMUM
- **CONSULTE le pitch** : la section "Prescriptions d'exécution visuelle" décrit les SENSATIONS que la surface, les interactions et les transitions doivent produire. C'est TOI qui choisis les techniques CSS les plus adaptées pour produire ces effets — tu as le catalogue complet dans html-showroom-spec.md §6. Le pitch décrit l'INTENTION, tu décides des MOYENS.
- **CONSULTE le pitch** : la section "Philosophie d'interaction" de la Direction visuelle décrit la SENSATION de hover pour ce concept. TRADUIS cette sensation en techniques CSS concrètes et APPLIQUE-les à TOUS les éléments interactifs (boutons, cards, liens).

### Variables CHROMATIQUES sanctuarisées dans le :root (2026-06-02)

En PLUS des tokens habituels, le `:root` DOIT contenir les 3 variables suivantes qui pilotent l'adaptation chromatique du brand book et du design-system en aval :

```css
:root {
  /* === MODE CHROMATIQUE DOMINANT (sanctuarisé 2026-06-02) === */
  --mode-chromatique: light;         /* light | dark | mixed — voir procédure de détermination ci-dessous */
  --brand-color-positive-bg: #XXXXXX; /* surface CLAIRE dominante */
  --brand-color-dark-bg: #XXXXXX;     /* surface SOMBRE dominante */
}
```

**Procédure de détermination du `--mode-chromatique`** :

1. **Lire la section "Registre atmosphérique"** de la Direction visuelle du pitch (déjà consultée ci-dessus). Si elle dit explicitement "sombre/cinéma noir/nocturne" → `dark`. Si elle dit "clair/aéré/lumineux" → `light`. Sinon, passer à l'étape 2.

2. **Calculer la luminance WCAG de la surface dominante** de la palette intégrée du pitch. La surface dominante est typiquement le fond principal des sections (`--color-surface` ou équivalent — la couleur la plus utilisée comme background dans tes choix CSS) :

   ```python
   def luminance(hex_color):
       hex_color = hex_color.lstrip('#')
       r, g, b = int(hex_color[0:2], 16) / 255, int(hex_color[2:4], 16) / 255, int(hex_color[4:6], 16) / 255
       def lin(c):
           return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
       return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
   ```

   - luminance > 0.7 → `light` (cas SaaS clair, sites corporates aérés)
   - luminance < 0.15 → `dark` (cas cinéma noir, luxe, marques nocturnes)
   - 0.15 ≤ luminance ≤ 0.7 → `mixed` (tons moyens, sépia, marines, palette équilibrée)

3. **Croiser avec le style retenu** :
   - Si la fiche styliste retenue pointe un style intrinsèquement dark (Cinéma noir, Dark Editorial, Brutalisme nocturne) → forcer `dark`
   - Si elle pointe un style intrinsèquement light (Minimalisme, Wellness, Pastel modern) → forcer `light`

4. **Output** : écrire `--mode-chromatique: VALEUR;` dans le `:root` + définir `--brand-color-positive-bg` (surface claire dominante de la palette) et `--brand-color-dark-bg` (surface sombre dominante OU couleur de texte principale si la marque est intégralement claire).

**Pourquoi ces variables** : le brand book (Phase 8) et le design-system (Phase 8b) LISENT ces 3 variables pour adapter leur mode chromatique aux marques light-dominant ou dark-dominant. Sans elles, ils retombent sur un fallback heuristique luminance (qui marche mais c'est une rustine). Avec elles présentes, le pipeline est cohérent bout en bout.

## SOCLE DE FINITION ÉLITE — Universel, quel que soit le curseur A

{finition_elite_tier1}

### CTA primaire — toujours identifiable (spécifique Voice Block)
Le CTA primaire du hero passe le **squint test** : identifiable en 0.5s sur un screenshot flouté. Il a un fond opaque ou quasi-opaque (≥ 80% d'opacité du background). Le `backdrop-filter` et le glassmorphism ne s'appliquent PAS au CTA primaire — un bouton semi-transparent sur un fond complexe (gradient, image, textures) disparaît visuellement. Les alternatives A=3 légitimes : CTA en texte pur + icône sans bouton (radical simplicity), ou CTA outline/ghost à bordure contrastante. Mais le CTA DOIT être immédiatement repérable comme élément d'action — même en A=3, l'affordance prend le pas sur l'esthétique.

### Typo hero minimum
Le titre H1 du Voice Block DOIT utiliser `font-size: clamp(4rem, 8vw, 12rem)` au minimum.
Les valeurs exactes sont libres (le max peut monter à 14rem, le vw à 10vw), mais le plancher est 8vw.
Un titre hero à 5-6vw manque d'impact — 8vw est le standard des sites élite.

### Fond texturé obligatoire
CHAQUE section DOIT avoir de la profondeur de surface — pas de fond couleur unie seul.

**Sur fond SOMBRE** (oklch lightness < 0.3) :
- Le grain SVG seul NE SUFFIT PAS — OBLIGATOIRE : au moins 1 `radial-gradient` coloré VISIBLE (opacity ≥ 0.10) avec une teinte de la palette
- Le grain : technique tuilée (`background-size: 150px`), `soft-light`, opacity 0.35-0.45
- Le fond doit avoir de la PROFONDEUR PERCEPTIBLE — pas un aplat + grain imperceptible

**Sur fond CLAIR** (oklch lightness > 0.7) :
- Le grain : technique tuilée (`background-size: 150px`), `soft-light`, opacity 0.35-0.45
- Au moins 1 radial-gradient en teinte de la palette
- Le fond ne doit pas être un blanc/crème PLAT

Exception : si le concept est intentionnellement minimal ET que le pitch le déclare explicitement.

### Dialogue texte/image obligatoire (si images fournies)
Si des images sont intégrées dans le style-tile, le texte et l'image DOIVENT interagir visuellement :
- AU MINIMUM un gradient de liaison (fondu d'un bord de l'image vers le fond)
- AU MINIMUM un point de contact visuel : chevauchement partiel (z-index), texte posé sur une zone de l'image, ou élément graphique qui lie les deux
- INTERDIT : texte dans sa colonne ET image dans sa colonne sans aucune interaction (le "split muet")

## COUCHE GRAPHIQUE DÉCORATIVE — 3ème couche de composition (obligatoire)

Les sites élite composent en 3+ couches superposées : (1) fond/surface, (2) contenu (texte, composants, images), (3) éléments graphiques décoratifs. Cette 3ème couche crée la richesse visuelle et la signature de marque. Elle est OBLIGATOIRE, que le style-tile contienne des images ou non.

### Catégories admises (liste fermée)
1. **Patterns géométriques SVG** — motifs répétés via `<pattern>` ou `<filter>` SVG
2. **Grain/texture de surface** — bruit statique superposé en couche semi-transparente (via SVG filter ou image de bruit)
3. **Formes abstraites positionnées** — géométrie simple placée en composition fixe via SVG ou CSS, contribuant au rythme visuel. NE PAS inclure le nom de la marque en oversize semi-transparent (brand watermark) — ce pattern est ultra-rare dans les sites élite et produit systématiquement un résultat médiocre.
4. **Pseudo-éléments de composition** — accents géométriques positionnés via ::before/::after (HORS traits sur overlines/titres, qui restent interdits)
5. **Overlays atmosphériques** — gradients colorés superposés au contenu (conic-gradient, radial-gradient multiples) créant de la profondeur chromatique. Les overlays sont TOUJOURS diffus et ronds/elliptiques — JAMAIS de `clip-path` sur un overlay ou un halo (ça produit un polygone flou amateur). Le clip-path est réservé aux éléments de contenu (images, sections).

### Socle obligatoire + catégories au choix
Deux catégories sont le SOCLE — toujours présentes :
- **Grain/texture** (cat. 2) : chaque section a de la matière de surface.
  **Technique obligatoire** : `background-image: url("data:image/svg+xml,...")` avec `background-size: 150px 150px` (tuile répétée fine). NE PAS utiliser de SVG inline étiré (`<svg viewBox="0 0 400 400">` en `width:100%`) — le grain sera grossier et pixelisé.
  **Blend-mode** : `soft-light` (PAS overlay ni multiply — ces blend-modes atténuent trop et rendent le grain invisible).
  **Opacity** : 0.35 à 0.45 (en dessous de 0.35 le grain est invisible en soft-light — vérifié empiriquement).
- **Overlays atmosphériques** (cat. 5) : au moins 3 radial-gradient ou conic-gradient colorés répartis sur le style-tile, créant de la profondeur chromatique.

Au-delà du socle, choisir parmi les catégories 1, 3 et 4 :
- **Si des images sont fournies** : socle + **1 catégorie supplémentaire** au choix. Total : 3 types.
- **Si aucune image n'est fournie** : socle + **1-2 catégories supplémentaires**. Total : 3-4 types.

### Élément signature (obligatoire, avec ET sans images)
Au moins 1 élément de couche graphique à **opacity ≥ 25%** couvrant une **surface significative** (pas un détail en coin). Cet élément est la signature graphique du style-tile — il doit être visible sans chercher. Un grain plus opaque ne compte PAS comme élément signature — c'est une texture, pas un élément de composition. L'élément signature est une forme, un pattern, ou une typographie décorative qui participe à la COMPOSITION du hero ou de l'atmosphere.

### Règle de parcimonie
2-3 éléments FORTS et visibles valent mieux que 6 fantômes. Ne pas chercher à cocher toutes les catégories — en choisir peu et les rendre PERCEPTIBLES.

### Seuil de visibilité (critique)
La visibilité d'un élément dépend du CONTRASTE entre l'élément et le fond — pas juste de l'opacity. Points de départ recommandés (le gate visuel vérifiera la perceptibilité réelle) :
- **Grain** : opacity 0.35-0.45 en soft-light, tuile 150px
- **Dot-grid** : dots de 2px minimum, opacité couleur ≥ 0.20 dans l'oklch
- **Quadrillage/grille** : lightness des lignes à mi-chemin entre le fond et le blanc (~lightness du fond + 0.35), opacité couleur 0.06-0.08
- **Formes/shapes** : opacité directe ≥ 0.25 pour l'élément signature
- **Hachures** : opacité couleur ≥ 0.12 dans l'oklch
Ces valeurs ne sont PAS universelles — elles doivent être ajustées en fonction du contraste avec le fond. Un élément invisible est du code mort.

### Formes décoratives — halos diffus, pas contours nets
Les formes décoratives les plus réussies sont des **HALOS DIFFUS** — des `radial-gradient` elliptiques, colorés, sans contour net, qui créent une masse chromatique ambiante. Ce registre est cohérent avec les sites élite (FollowArt, Finsight, Junabase).

Les formes à **CONTOUR NET** sont DÉCOURAGÉES : `<circle>` avec `stroke`, polygones avec arêtes visibles, structures concentriques (cible, cadran), formes géométriques assemblées. Le LLM ne les rend pas avec le craft nécessaire — le résultat est amateur.

Les **CONTOURS GÉOMÉTRIQUES FERMÉS À GRANDE ÉCHELLE** (un `border` dessinant une ellipse, un cercle ou un rectangle arrondi couvrant >30% de la surface d'une section) ont 2 registres :
- **INTERDIT** : border visible (opacity > 6% OU border-width > 1px) sans masse intérieure significative — produit un rendu amateur, un cadre vide qui flotte.
- **AUTORISÉ** : border très fin (1px) ET très transparent (opacity ≤ 6%, ou couleur à ≤ 6% dans l'oklch) — à cette subtilité, le contour devient une texture atmosphérique, pas une forme géométrique. Il ajoute de la richesse sans s'imposer.
**Alternative** au contour : un radial-gradient diffus qui crée l'IMPRESSION de la forme sans bord net, ou une masse remplie semi-transparente. NOTE : cette règle concerne les contours géométriques fermés (ellipses, cercles, rectangles). Les LIGNES décoratives (traits diagonaux, accents linéaires, séparateurs positionnés) restent des éléments de composition valides.

Les primitives SVG **remplies** (`fill` sans `stroke` visible) utilisées comme masses de couleur positionnées restent admises. Les `<path>` complexes qui dessinent des objets reconnaissables (engrenage, feuille, étoile, soleil) sont des ILLUSTRATIONS — interdites.

### Ce qui ne compte PAS comme couche graphique
- Un élément à opacity < 8% (invisible = inexistant, sauf grain sur fond sombre)
- Un unique radial-gradient de fond déjà compté dans "Fond texturé obligatoire"
- Les border-radius, box-shadow, transitions (c'est de la finition CSS)

### Règle anti-contamination
Le CHOIX des formes, motifs et compositions graphiques vient du CONCEPT (son univers, son énergie, sa physique de marque). Ne pas réutiliser les mêmes éléments graphiques d'un concept à l'autre.

## PRINCIPES DE HIÉRARCHIE VISUELLE — Niveau élite (quel que soit le curseur A)

{hierarchie_visuelle_tier1}

---

## ⚠ A11Y ET FONDAMENTAUX (non-négociable, quel que soit le concept)

{a11y_fondamentaux_tier1}

## ⛔ ANTI-PATTERNS DATÉS — BLACKLIST (quel que soit le curseur A)

{anti_slop_blacklist_tier1}

## CALIBRAGE COMPOSITION PAR CURSEUR A
Le curseur A={cursor_a} détermine l'AUDACE DE COMPOSITION — la forme, pas la facture.
La finition est identique quel que soit A (voir SOCLE DE FINITION ÉLITE ci-dessus).

**A = 1** : Layout structuré (grilles régulières, symétrie). Formes rectangulaires. Fonds unis ou gradients doux. Interactions fonctionnelles (changement de couleur, opacité). Le résultat est PROPRE et PROFESSIONNEL.

**A = 2** : Au moins UNE asymétrie contrôlée dans le layout. Au moins UNE surface expressive (texture, overlay, radius mixtes). Les interactions EXPRIMENT le concept — pas juste un changement de fond. Le résultat a un SIGNAL DISTINCTIF.

**A = 3** : Au moins UNE convention de layout cassée (chevauchement, grille brisée, z-index expressif). Surfaces composites (multi-couches, mélanges, masques). Interactions physiques ou narratives — le hover raconte quelque chose. Le résultat INVENTE SA PROPRE RÈGLE. Chaque section doit avoir au minimum 3 niveaux de profondeur visuelle (fond texturé, couche intermédiaire, contenu) — la richesse de couches est ce qui distingue A=3 d'un site standard.

**CLARIFICATION A=3 — "Convention cassée" = DISPOSITION modifiée, pas DÉCORATION ajoutée.**
- **Convention cassée** : un élément qui DOIT exister (titre, image, CTA, section, artefact) est positionné, dimensionné ou ordonné d'une façon qui défie les attentes. C'est une MODIFICATION de la structure.
- **Décoration** : un élément qui n'existerait PAS dans un layout conventionnel a été AJOUTÉ pour créer un effet visuel (séparateur, forme, ornement). C'est un AJOUT sur une structure standard.
- **Test** : l'élément "audacieux" est-il un élément de contenu dont tu as changé la POSITION — ou un ornement que tu as AJOUTÉ ? Si c'est un ajout → c'est du décor, pas une convention cassée.

**TECHNIQUES CSS AVANCÉES — SOCLE COMMUN (quel que soit A)** :
Les techniques avancées ne sont pas de l'audace — ce sont des outils de FABRICATION. Un style-tile A=1 propre et un A=3 radical utilisent les mêmes outils ; seule la COMPOSITION change.
Au minimum **4 techniques** parmi :
`@property` animé (couleur ou angle, dans un @keyframes ou transition) · `clip-path` · `mask-image` · `@starting-style` · `backdrop-filter` · `mix-blend-mode` · `:has()` · `animation-timeline: view()` · `@container`
Chaque technique doit SERVIR le concept, pas être plaquée. Le quota est un plancher de qualité de fabrication, pas un objectif à atteindre.

Le curseur te dit À QUEL POINT tu pousses la composition. Le pitch te dit DANS QUELLE DIRECTION. La finition est toujours maximale.

## GATES (VÉRIFIER AVANT DE FINALISER)
1. **Screenshot Test** : ZÉRO donnée technique visible (pas de HEX, pas de noms de fonts, pas de tailles en px dans le texte visible)
2. **Mason's Rule** : ZÉRO scaffolding (pas de "Section 02", pas de labels documentation)
3. **Cursor Coherence** : Le traitement CSS correspond au curseur A (voir CALIBRAGE COMPOSITION PAR CURSEUR A). Si A=2, vérifier qu'il y a au moins une asymétrie, une surface expressive, et une technique non-standard. Si A=3, vérifier qu'au moins une convention de layout est cassée.
4. **Brief Alignment** : Le contenu fictif est cohérent avec le brief de la marque
5. **data-visual intact** : Si des images avec `data-visual` ont été fournies, vérifier que CHAQUE attribut `data-visual` est préservé intact dans le HTML final (nécessaire pour le swap haute résolution). Seuls les visuels FOURNIS PAR L'UTILISATEUR (base64 via `{visual_reference_block}`) peuvent être intégrés comme `<img>` — pas de photos ou illustrations générées.
6. **Zero Dead Code** : Chaque `@keyframes` DOIT être utilisé par au moins un sélecteur. Chaque custom property définie dans `:root` DOIT être référencée au moins une fois dans le CSS. Zéro code mort — supprime tout ce qui n'est pas utilisé. **Exception légitime** : les 3 variables chromatiques sanctuarisées (`--mode-chromatique`, `--brand-color-positive-bg`, `--brand-color-dark-bg`) peuvent ne pas être référencées par le CSS du style-tile lui-même — elles sont là pour les phases aval (brand book, design-system) qui les lisent. Pour passer le gate, les inclure dans une règle technique au moins (ex: `body { /* mode-chromatique: var(--mode-chromatique); */ }` en commentaire CSS ou usage symbolique).
7. **Couverture Custom Properties** : Le `:root` DOIT couvrir les 7 catégories standards (palette, typo, type-scale, spacing, radius, shadows, transitions) + les **3 variables chromatiques sanctuarisées 2026-06-02** (`--mode-chromatique`, `--brand-color-positive-bg`, `--brand-color-dark-bg`) qui pilotent l'adaptation du brand book et du design-system aux marques light/dark. Le nombre de variables est libre — un concept minimaliste peut avoir 28 properties, un concept riche 63.
8. **Surface Depth** : Les techniques de profondeur sont libres : mix-blend-mode, backdrop-filter, clip-path, mask-image, ombres colorées, textures, ou toute technique CSS moderne. Les Atmosphere Blocks DOIVENT avoir de la profondeur visuelle — pas de background plat (couleur unie sans overlay, gradient, ou texture).
9. **CSS Moderne** : Le socle (oklch, @layer, @property, color-mix, text-wrap, clamp) est TOUJOURS obligatoire. Les techniques avancées : ≥4 obligatoires QUEL QUE SOIT le curseur A (c'est de la fabrication, pas de l'audace). Voir "TECHNIQUES CSS AVANCÉES — SOCLE COMMUN" ci-dessus. Consulte la **section 6 de html-showroom-spec.md** pour le catalogue complet.
10. **Anti-Patterns Datés** : Vérifier que le fichier ne contient AUCUN pattern de la section "ANTI-PATTERNS DATÉS — BLACKLIST". En particulier : (a) AUCUN `transform: translateY()` dans un sélecteur `:hover` — quel que soit le curseur A. (b) AUCUNE animation `infinite` décorative (pulse, breathe, drift, flicker). (c) AUCUN `box-shadow: 0 0 Npx` (glow sans offset) — les ombres ont un offset vertical. (d) AUCUN séparateur décoratif entre sections (wave, zigzag, gradient line). (e) AUCUN `@keyframes` de type fade-up staggeré (translateY + opacity + delay manuel) — utiliser `@starting-style`.
11. **Finition Élite** : (a) Si le concept utilise des ombres portées, chaque box-shadow a ≥2 couches empilées — pas de shadow simple isolée. (b) Aucune transition avec `ease` ou `ease-in-out` générique — utiliser les courbes nommées du :root. (c) Les 3 sections ont des padding-block DIFFÉRENTS. (d) Chaque élément interactif change ≥2 propriétés au hover.
12. **Couche Graphique** : Le style-tile contient les 2 éléments de base (grain/texture + overlay atmosphérique) + au moins 1 catégorie supplémentaire visible (2 sans images). Chaque élément compté doit être à opacity ≥ 8% (sauf grain overlay sur fond sombre : ≥ 3%). Aucun `<path>` SVG complexe (>20 commandes) ou `<symbol>` figuratif — seules les primitives géométriques sont admises.

Si UN SEUL gate échoue → corriger avant de finaliser.

## DIRECTIVE DE QUALITÉ
Tu es encouragé à utiliser TOUT ton contexte pour un HTML RICHE et IMMERSIF.
**CSS MODERNE OBLIGATOIRE** — Tu génères pour un navigateur 2026, pas 2019.

**Socle** (TOUJOURS utiliser, quel que soit le curseur) :
- `oklch()` pour la palette (gradients perceptuellement uniformes, pas de zone grise)
- `@layer` pour organiser le CSS (reset → tokens → components → utilities)
- `@property` déclaré pour les custom properties animables
- `color-mix()` pour les variations (hover states, backgrounds tintés)
- `text-wrap: balance` sur les headings, `text-wrap: pretty` sur les paragraphes
- `clamp()` pour les tailles fluides (font-size, padding)
- Ombres multi-couches, easing physiques, rythme de spacing, transitions multi-property (voir SOCLE DE FINITION ÉLITE ci-dessus)
- Logical properties (`padding-inline`, `margin-block`) quand applicable

**Techniques avancées** (obligatoires par curseur — voir CALIBRAGE COMPOSITION PAR CURSEUR A) :
Le pitch décrit des SENSATIONS. C'est TOI qui choisis les techniques CSS pour les produire. Voici ton catalogue — pioche dedans pour atteindre le quota de ton curseur :
- `clip-path` — sections découpées, formes non-rectangulaires, boutons sculptés
- `mask-image` — fondus entre sections, révélation progressive, formes organiques
- `@starting-style` — animations d'entrée CSS-native (pas de JS), apparition au chargement
- `backdrop-filter` — surfaces translucides, profondeur givrée, couches visibles en transparence
- `mix-blend-mode` — mélange de couches (texte qui s'enfonce dans le fond, superpositions colorées)
- `:has()` — style contextuel (le parent réagit à son enfant, ex: row qui change quand son dot est actif)
- `animation-timeline: view()` — animations liées au scroll, révélation progressive au défilement
- `@container` — layout adaptatif des composants (le contenu s'adapte à son conteneur)
- `@property` ANIMÉ — pas juste déclaré, mais utilisé dans un @keyframes ou une transition (couleur qui mute, angle qui pivote)

Chaque technique doit servir une sensation du pitch.

Chaque détail compte : letter-spacing sur les overlines, font-feature-settings, font-variation-settings, transitions sur les boutons.
L'exemple style-tile fourni est la BARRE MINIMUM — vise AU-DESSUS. Rappel : copier le NIVEAU DE QUALITÉ CSS, pas la direction créative.

## NOM DU CONCEPT VISIBLE
Le nom du concept DOIT apparaître à 2 endroits :
1. **<title>** : `<title>{brand} — Style-Tile — {concept_name}</title>`
2. **Footer tagline** : Dans l'Atmosphere Block footer, le texte de tagline
   affiche `{brand} — {concept_name}` (remplace le texte générique)

STATUS: OK quand tous les gates passent.
Écris le fichier HTML dans : {skill_dir}/outputs/{session_dir}/{brand}-style-tile-concept-{concept_number}.html
