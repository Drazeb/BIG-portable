# Guide MidJourney — Prompting par registre visuel

> **Version MJ** : v7 + Niji 7
> **Dernière vérification** : 2026-02-27
> **Règle de fraîcheur** : Avant de générer des prompts MJ, le subagent DOIT faire un `WebSearch("midjourney latest version 2026")`. Si la version courante ≠ v7, alerter l'utilisateur : "Le guide MJ est calibré pour v7, mais vX semble disponible. Voulez-vous que je mette à jour le guide avant de générer les prompts ?"

---

## §1. Arbre de décision — Quel registre choisir ?

Le subagent qui génère des prompts MJ utilise cet arbre pour router le brief vers le bon registre. Lire de haut en bas, premier match gagne.

### Étape 1 — Famille

| Mots-clés dans le brief | Famille |
|---|---|
| photo, réaliste, shot on, lens, bokeh, macro, portrait, paysage, food, produit, architecture, lifestyle, éditorial | **PHOTO** |
| illustration, vector, flat, watercolor, line art, isometric, vintage, affiche, mascot, character, infographie | **ILLUSTRATION** |
| logo, brand mark, emblem, symbol, monogram, badge, pictogram, mark | **LOGO** |
| pattern, motif, seamless, texture, background, tile, grain, fond | **PATTERN/TEXTURE** |
| mockup, device, packaging, smartphone, écran | **F2 Mockup** |
| UI, dashboard, app, wireframe, interface, material design | **F3 UI/UX** |
| 3D render, clay, glass, metallic, octane, HDRI, PBR | **F4 3D Render** 🔀 **Dual** (illustratif/onirique → Recraft, cinématique/photoréaliste → MJ) |

### Étape 2 — Registre dans la famille

**PHOTO** :

| Signal | Registre |
|---|---|
| lifestyle, ambiance, scène de vie, candid, editorial | **P1** Éditoriale |
| macro, close-up, surface, détail, bois, métal, tissu, pierre, matière | **P2** Macro/Texture |
| portrait, personne, fondateur, équipe, visage | **P3** Portrait |
| produit, packshot, objet, still life, studio | **P4** Produit |
| architecture, intérieur, espace, bâtiment, showroom, lieu | **P5** Architecture |
| paysage, drone, aérien, panorama, nature, montagne, vue | **P6** Paysage |
| food, cuisine, plat, gastronomie, recette | **F1** Food |

**ILLUSTRATION** :

| Signal | Registre |
|---|---|
| flat, vector, corporate, Notion, editorial 2D, aplat, solid colors | **I1** Flat/Corporate |
| line art, trait, encre, monoline, croquis propre, fineliner | **I2** Line Art |
| isometric, isométrique, axonometric, vue 30° | **I3** Isométrique 🔀 **Dual** (illustratif → Recraft, cinématique → MJ) |
| aquarelle, watercolor, peinture, brush, lavis | **I4** Aquarelle ⚠️ **→ Recraft par défaut** (voir routage Phase 3C) |
| rétro, vintage, art déco, mid-century, affiche, poster | **I5** Rétro/Vintage 🔀 **Dual** (illustratif → Recraft, cinématique → MJ) |
| character, mascotte, personnage, avatar, chibi | **I6** Character/Mascotte |
| infographic, schéma, diagramme, process, flowchart, data-viz | **I7** Infographique |

**LOGO** :

| Signal | Registre |
|---|---|
| géométrique, abstrait, minimal, formes pures, symbole pur | **L1** Géométrique abstrait |
| figuratif, pictorial, objet reconnaissable, animal, silhouette | **L2** Figuratif |
| monoline, single weight, wireframe, outline only, trait unique | **L3** Monoline |
| badge, emblème, shield, circular, bannière, contenu dans une forme | **L4** Badge/Emblème |
| mascotte, character, personnage expressif | **L5** Mascotte |
| vintage, craft, texturé, distressed, artisanal, letterpress | **L6** Texturé/Craft |

**PATTERN/TEXTURE** :

| Signal | Registre |
|---|---|
| seamless, répétitif, tile, textile, papier peint | **T1** Seamless |
| abstrait, fond, grain, gradient, organique, fluid | **T2** Abstraite ⚠️ **→ Recraft par défaut** (voir routage Phase 3C) |
| géométrique, tessellation, grille, mosaïque, hexagonal | **T3** Géométrique 🔀 **Dual** (aplats précis → Recraft, texturés/matière → MJ) |

### Étape 3 — Résolution d'ambiguïtés

| Cas ambigu | Règle |
|---|---|
| "texture aquarelle" + sujet concret (fleurs, village) | → **I4** (illustration) |
| "texture aquarelle" sans sujet (fond, background) | → **T2** (texture abstraite) |
| "illustration 3D" + vue isométrique | → **I3** (isométrique) |
| "illustration 3D" + render/octane/clay | → **F4** (3D render) |
| "logo mascotte" | → **L5** (toujours logo, pas I6) |
| "pattern illustration" | → **T1** avec style keywords illustration |
| "illustration de process" | → **I7** si schéma, **I3** si vue spatiale, **I1** si flat |

---

## §2. Fondations universelles

### Paramètres communs

| Paramètre | Ce que ça fait | Défaut | Piège |
|---|---|---|---|
| `--stylize N` (0-1000) | Liberté créative de MJ. Bas = littéral. Haut = MJ impose son esthétique. | 100 | >500 : MJ ignore le prompt. <20 : résultat brouillon sauf logos. |
| `--style raw` | Supprime le filtre esthétique MJ (éclairage drama, profondeur ciné). Plus plat, plus fidèle. | off | Ne PAS utiliser pour paysages et aquarelles (le filtre est un atout). |
| `--niji 7` | Mode illustration/anime. Linework propre, couleurs plates, cohérence personnage. | off | Biais manga/anime. Pas de personnalisation (`--p` inactif). |
| `--no X` | Exclusion de termes. Pas 100% fiable — toujours renforcer dans le prompt aussi. | — | Ne pas mettre plus de 10-12 termes. Au-delà, MJ perd en cohérence. |
| `--tile` | Génère une tuile répétable (seamless). | off | Ne PAS upscaler les tiles (casse le seamless sauf upscalers récents). |
| `--ar W:H` | Aspect ratio. | 1:1 | Pas de ratio > 3:1 ni < 1:3. |
| `--draft` | Qualité réduite, coût réduit. | off | Suffisant pour exploration (logos, patterns). Insuffisant pour macro/archi/portraits finaux. |

### Structure de prompt optimale (v7)

V7 comprend mieux les phrases naturelles que les listes de tags. Structure recommandée :

```
[SUJET + ACTION + CONTEXTE], [STYLE / MEDIUM], [ÉCLAIRAGE / AMBIANCE],
[DÉTAILS TECHNIQUES : objectif, film stock], [COULEURS HEX si pertinent],
[FOND] --[mode] --ar X:Y --s N --style raw --no [négatifs]
```

**Règles universelles** :
1. Les premiers mots du prompt ont le plus de poids — y mettre le sujet
2. Prompt ≤ 6 lignes — au-delà, MJ perd le fil
3. Un seul medium par prompt ("watercolor" OU "ink", pas les deux sauf "ink and watercolor")
4. Couleurs HEX intégrées dans le texte du prompt quand la palette est importante
5. `--no` contient TOUS les négatifs (techniques + sectoriels + directionnels) — pas de bloc séparé
6. "8K, ultra HD, hyper-realistic" n'améliorent PAS la qualité en v7 — dilution inutile

---

## §3. Photos

### P1 — Éditoriale / Lifestyle

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 250-500 | raw optionnel | 16:9, 3:2, 4:5 | stock photo, generic, posed |

**Mots-clés efficaces** : `editorial photo`, `cinematic still`, `candid moment`, `documentary style`, `authentic`, `unposed`. Objectif : `85mm f/1.4`, `35mm lens`, `shot on Canon R5`. Film stock : `Kodak Portra 400`, `Fujifilm Classic Chrome`.

**Pièges** : "beautiful woman/handsome man" → rendu pub générique. "stock photo" dans le prompt → MJ l'interprète littéralement. Trop de détails techniques simultanés → MJ se perd.

**Prompt exemple** :
```
editorial photo, woman in her 40s reading at a sunlit café terrace, candid moment,
85mm f/1.8, shallow depth of field, golden hour, Kodak Portra 400 film grain,
warm earth tones --v 7 --ar 3:2 --s 350
```

**--sref** : `3861771670` (Cinematic Moody Nostalgia), `871420533` (Dreamy)

---

### P2 — Macro / Texture Matière

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 200-400 | raw | 1:1, 4:5, 3:4 | product shot, studio, human |

**Mots-clés efficaces** : `ultra-magnified macro image`, `extreme close-up`, `Canon R ISO100 f/2.8`, `180mm macro lens`, `rim lighting`, `backlit`, `dramatic side lighting`. Textures : `scales, feathers, fur, iridescent, glistening`.

**Pièges** : "product shot" → transforme en packshot studio. Omettre le fond → MJ ajoute un contexte narratif. Un seul sujet par prompt (deux → MJ ne sait plus quoi focuser).

**Prompt exemple** :
```
ultra-magnified macro image of weathered oak wood grain, deep fissures and aged patina,
Canon R ISO100 f/2.8, 180mm macro lens, dramatic side lighting,
dark mood background --v 7 --style raw --ar 4:5 --s 350
```

---

### P3 — Portrait Environnemental

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 100-250 | **raw obligatoire** | 2:3, 4:5, 3:4 | plastic skin, glossy, smooth skin, airbrushed |

**Raw OBLIGATOIRE** — c'est LE paramètre anti-uncanny valley. Sans raw, MJ lisse les visages.

**Mots-clés efficaces** : `natural skin texture`, `pores`, `realistic imperfections`, `freckles`, `laugh lines`, `candid`, `environmental portrait`, `soft natural light`, `85mm f/1.4`.

**Pièges** : "perfect skin/flawless" → garantie uncanny valley. Mains visibles → encore problématique en v7 (cacher dans les poches, derrière le dos). Expressions vagues ("happy person") → sourire forcé, préférer "slight knowing smile".

**Prompt exemple** :
```
environmental portrait of a ceramist in her workshop, mid-30s, clay-stained apron,
natural skin texture with pores, focused expression, soft window light,
shallow depth of field, 85mm f/1.4, cluttered shelves in background
--v 7 --style raw --ar 2:3 --s 150
```

---

### P4 — Produit / Still Life

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 100-300 | raw | 1:1, 4:5, 3:4 | people, face, messy background |

**Mots-clés efficaces** : `product photography`, `commercial photography`, `three-point lighting`, `soft diffused lighting`, `polished marble surface`, `clean backdrop`. Structure modulaire : [produit] + [surface] + [éclairage] + [mood].

**Pièges** : `--no background` ne supprime pas toujours le fond → spécifier "white background" explicitement. Ne pas mélanger éclairage studio et naturel. Rester concis sur l'objet, détaillé sur le setup.

**Prompt exemple** :
```
commercial photography of a matte black ceramic mug on polished walnut surface,
soft diffused side lighting, subtle steam rising, warm neutral tones,
shallow depth of field, clean minimal background
--v 7 --style raw --ar 4:5 --s 200
```

---

### P5 — Architecture / Intérieur

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 200-400 | raw si lignes droites critiques | 16:9, 21:9, 3:2 | fisheye, distortion, people |

**Mots-clés efficaces** : `architectural photography`, `24mm tilt-shift lens` (corrige les perspectives), `straight vertical lines`, `symmetrical composition`. Référencer des architectes (Mies van der Rohe, Zaha Hadid) fonctionne bien. Spécifier les matériaux (`polished concrete, raw timber, brushed steel`).

**Pièges** : MJ courbe les lignes verticales → antidote : `tilt-shift`, `straight vertical lines`. "wide angle" seul → résultat variable, préférer `24mm architectural lens`. "cozy" seul → MJ ajoute bougies, plaids aléatoires.

**Prompt exemple** :
```
architectural interior photography of a minimalist Japanese teahouse,
polished concrete floors, raw timber beams, floor-to-ceiling windows,
natural diffused light, 24mm tilt-shift lens, symmetrical composition,
bright airy atmosphere --v 7 --style raw --ar 16:9 --s 300
```

---

### P6 — Paysage / Aérien

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 300-500 | **standard (PAS raw)** | 16:9, 21:9, 2.39:1 | people, text, watermark |

**PAS raw** — le filtre esthétique de MJ (lumière dramatique, profondeur atmosphérique) est un atout pour les paysages. Raw les rend plats.

**Mots-clés efficaces** : `drone shot`, `atmospheric perspective`, `layers of fog`, `foreground interest`, `golden hour`, `DJI Mavic 24mm`. Décrire les plans (foreground/midground/background). Inclure un élément d'échelle (`tiny figure on ridge`).

**Pièges** : "beautiful landscape" → poster calendar. Ratio carré → tue l'immensité. "aerial view" = abstrait, "drone shot" = plus de proximité.

**Prompt exemple** :
```
extreme long drone shot of volcanic highlands at blue hour, layers of fog between
black lava ridges, Iceland, atmospheric perspective, DJI Mavic 24mm,
dramatic sky, foreground moss-covered rocks --v 7 --ar 21:9 --s 450
```

---

### F1 — Food Photography

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 150-300 | raw | 4:5, 3:2, 16:9 | human, hands (si non voulues), messy background |

**Mots-clés efficaces** : `food photography`, `studio food styling`, `soft top light`, `macro detail`, `glistening`, `steam`, `overhead shot`, `45-degree angle`.

**Pièges** : "delicious" → MJ surcharge les couleurs. Omettre l'angle → rendu incohérent. Fond non spécifié → MJ improvise.

---

## §4. Illustrations

### I1 — Flat / Corporate 2D

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 0-100 | **raw** | selon usage | ink, hand-drawn, paper texture, photograph, shadow, 3d, gradient |

**Stylize TRÈS BAS (20-75)** — crucial. Le défaut (100) ajoute déjà trop de détails pour du flat.

**Mots-clés efficaces** : `Simple flat vector illustration of [sujet], isolated on a white background`, `flat design`, `minimal`, `geometric shapes`, `solid colors`, `clean lines`, `minimalistic`, `no gradients`.

**⚠ PIÈGES CRITIQUES** :
- **"ink"** → PHOTO d'un dessin à l'encre sur papier, PAS une illustration digitale
- **"hand-drawn"** → PHOTO de croquis physique sur table
- **"paper" / "paper texture"** → texture de papier réaliste sous l'illustration
- **"illustration"** seul (sans "flat" ou "vector") → illustration détaillée/painterly
- **Stylize > 200** → MJ ajoute ombres portées et casse le flat

**Pour le style Notion spécifiquement** : `notion style minimalist illustration, black line art on white background, simple facial features, exaggerated proportions, clean precise outlines, flat design, playful whimsical style`. Utiliser `--niji 7 --s 50` au lieu de `--v 7` (linework plus propre, rendu plus plat natif). Si le résultat est trop manga, fallback sur `--v 7 --style raw --s 50`.

**Prompt exemple** :
```
Simple flat vector illustration of a young woman sitting at her desk with a laptop,
solid colors, geometric shapes, clean outlines, minimalistic,
isolated on a plain white background --v 7 --style raw --ar 3:2 --s 50
```

**--sref** : `27179547` (Minimalist Vector), `1758293170` (Minimalist Line Art)

---

### I2 — Line Art / Trait

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| **`--niji 7` (premier choix)** ou `--v 7 + raw` | 50-200 | standard (niji) ou raw (v7) | selon usage | color, fill, shading, gradient, photograph |

**Niji 7 premier choix** — la linework est sa force majeure. Les lignes ne se "collapsent" plus dans les zones denses. V7 produit des traits plus "painterly".

**Mots-clés efficaces** : `line art`, `monoline illustration`, `single line drawing`, `pen and ink`, `clean linework`, `white background`. Contrôle épaisseur : `thin delicate lines` vs `bold thick outlines` (MJ n'a pas de paramètre d'épaisseur, utiliser des adjectifs).

**Pièges** : "sketch" → croquis brouillon. Ajouter des couleurs dans un prompt line art → MJ remplit les zones.

**Prompt exemple** :
```
monoline illustration of a botanical branch with leaves, delicate linework,
single weight line, no fill, black ink on white background,
editorial style, minimalist --niji 7 --ar 2:3 --s 100
```

**--sref** : `19797` (Pen and Ink), `3550719318` (Organic Line Art)

---

### I3 — Isométrique

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 100-300 | standard | 1:1, 3:4 | perspective, vanishing point, photorealistic |

**Mots-clés efficaces** : `Isometric illustration of [sujet], highly detailed, vibrant colors, clean lines, minimalistic design, white background`, `isometric view`, `30-degree angle`, `cutaway view`.

**Pièges** : MJ ne respecte pas toujours le 30° (isométrie approximative). "3D render" → rendu Blender réaliste. Scènes trop complexes → MJ perd l'angle. Toujours spécifier "white background".

**Prompt exemple** :
```
Isometric illustration of a modern coworking space, highly detailed, vibrant colors,
clean lines, minimalistic design, cutaway view showing interior furniture
and people working, white background --v 7 --ar 1:1 --s 200
```

---

### I4 — Aquarelle / Peinture

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 250-500 | **standard (PAS raw)** | 3:2, 2:3, 4:5 | photorealistic, sharp, digital, vector |

**PAS raw** — le filtre esthétique renforce le rendu organique et painterly. Raw = rendu trop sec.

**Mots-clés efficaces** : `watercolor painting`, `soft washes`, `wet-on-wet technique`, `loose brushstrokes`, `paint bleeding`, `transparent layers`, `rough watercolor paper`. Artistes : `Winslow Homer`, `John Singer Sargent`. Dosage : "watercolor illustration" = contrôlé, "watercolor painting" = libre.

**Pièges** : "hyper-realistic watercolor" → oxymore. "digital art" → annule l'effet aquarelle. Trop de détails → MJ surcharge (l'aquarelle est un medium de suggestion).

**Prompt exemple** :
```
watercolor painting of a misty coastal village at dawn, soft washes of pastel blues
and warm ochres, loose brushstrokes, wet-on-wet technique, paint bleeding at edges,
rough watercolor paper texture, inspired by Winslow Homer --v 7 --ar 3:2 --s 400
```

**--sref** : `2234126148` (Watercolor expressif)

---

### I5 — Rétro / Vintage

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 200-500 | standard | 2:3, 3:4, 1:1 | modern, digital, clean, minimalist |

**Par période** :
- **Art Déco (1920-40)** : `art deco, bold geometric shapes, gold accents, 1930s poster`
- **Mid-Century (1950-60)** : `mid-century modern, 1960s aesthetic, pastel palette, Saul Bass style`
- **Rétro-futurisme** : `retro-futurism, atomic age, googie architecture`
- **Vintage print** : `aged paper, distressed texture, letterpress, sepia-toned`
- **Affiche** : `vintage travel poster, bold typography, WPA style`

**Pièges** : "vintage" seul → trop vague, MJ mélange les époques. Toujours spécifier la décennie ou le mouvement. "old/ancient" → MJ interprète comme dégradé, pas comme style.

**--sref** : `1410777217` (Art Deco Vector), `3986612298` (Retro Color-Block)

---

### I6 — Character / Mascotte

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| **`--niji 7` (premier choix)** | 100-250 | standard | 1:1, 2:3 | photorealistic, complex background |

**Niji 7** — cohérence de personnage bien supérieure à v7. Les traits faciaux restent stables entre les générations.

**Mots-clés efficaces** : `cute mascot [animal], chibi proportions, clean outline, flat colors`, `character design`, `turnaround sheet`. Utiliser `--cref` pour verrouiller l'identité visuelle entre variantes.

**Stratégie de cohérence** :
1. Créer un portrait de référence avec tous les traits fixes
2. Utiliser cette image en `--cref` pour toutes les variantes
3. Ne modifier que pose, décor, expression — jamais la description du personnage

**Pièges** : V7 change le visage à chaque génération. "logo mascot" → MJ interprète comme badge contenant une mascotte.

---

### I7 — Infographique / Technique

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 50-150 | raw | 2:1, 16:9, 1:1 | photograph, realistic, complex texture |

**Raw + stylize bas** — la précision géométrique exige un contrôle maximal.

**Mots-clés efficaces** : `flat material vector design`, `2D`, `data visualization`, `infographic style`, `clean geometric shapes`, `structured layout`, `high contrast`, `bold colors`.

**Pièges** : **MJ ne sait PAS écrire du texte fiable** — générer le visuel, ajouter le texte en post-prod. "infographic" seul → poster artistique. "data/chart" → MJ invente des données incohérentes.

---

## §5. Logos

### Règles universelles logos

1. **`--ar 1:1` obligatoire** — sans exception
2. **`--no text, letters, words, signature, watermark`** — toujours (MJ ajoute du texte sinon)
3. **`--style raw`** — toujours (sauf L5 en niji)
4. **MJ ne garantit JAMAIS la symétrie** — retouche post-prod obligatoire
5. **MJ ne sait PAS faire de typographie** — ne jamais compter sur MJ pour le lettrage
6. Décrire ce qu'on VOIT, pas comment c'est construit
7. Post-prod systématique : upscale Subtle → export PNG → vectorisation (vtracer ou Illustrator)

### L1 — Symbole Géométrique Abstrait

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | **0-30** | raw | 1:1 | text, letters, words, signature, watermark, background, shadow, gradient, depth, 3d, shading, photorealistic, detailed texture, noise |

**Stylize quasi-zéro** — toute "créativité" de MJ casse la symétrie.

**Mots-clés efficaces** : `abstract geometric symbol`, `negative space`, `pure shapes`, `monoline`, `brand mark`, `symmetrical design`, `black and white`, `isolated on pure white`.

**Pièges** : "minimalist" peut ne pas suffire → ajouter `single element, no ornamentation`. Fond coloré persistant malgré --no → insister avec `isolated on pure white` dans le prompt.

**Prompt exemple** :
```
abstract geometric mountain peak symbol, hexagon frame, monoline, single line art,
negative space, modern logo, black and white, symmetrical design,
isolated on pure white background --v 7 --style raw --ar 1:1 --s 20
--no text, letters, words, signature, watermark, background, shadow, gradient
```

---

### L2 — Symbole Figuratif

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | **20-60** | raw | 1:1 | text, letters, background, shadow, gradient, 3d, photorealistic |

**Stylize légèrement plus haut** — MJ a besoin d'un peu de liberté pour simplifier un objet reconnaissable en symbole.

**Mots-clés efficaces** : `simplified`, `iconic`, `flat design`, `bold silhouette`, `pictorial mark`, `negative space`, `geometric abstraction of [sujet]`.

**Pièges** : "realistic fox" → renard détaillé, pas un symbole. Utiliser `simplified, iconic, geometric`. "logo of a [animal]" → trop détaillé, préférer `[animal] symbol, simplified to geometric shapes`.

---

### L3 — Monoline / Single-Weight

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | **10-40** | raw | 1:1 | fill, shading, color, gradient, 3d, shadow, text, letters |

**Zéro remplissage** — `--no fill, shading, color` ET `no fill, outline only` dans le prompt (les deux nécessaires).

**Mots-clés efficaces** : `monoline`, `single weight line`, `uniform stroke`, `wireframe style`, `no fill`, `outline only`, `continuous line`.

**Pièges** : MJ ajoute TOUJOURS du remplissage si on n'est pas explicite. "line art" seul → épaisseur variable, spécifier `single weight, uniform stroke`.

---

### L4 — Badge / Emblème

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | **30-80** | raw | 1:1 | photorealistic, 3d, depth, noise |

**Stylize plus haut** — les badges ont des détails internes qui bénéficient d'un peu d'interprétation.

**Mots-clés efficaces** : `badge logo`, `emblem style`, `circular frame`, `shield shape`, `ornate frame`, `detailed linework`, `vintage badge`, `hand-engraved look`.

**Pièges** : MJ surcharge les badges de détails illisibles à petite taille → spécifier `clean at small size, simplified details`. Texte dans le badge → toujours en post-prod.

---

### L5 — Mascotte (logo)

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| **`--niji 7`** ou `--v 7 + raw` | 50-150 | standard (niji) ou raw (v7) | 1:1 | background, photorealistic, complex texture, text |

**Niji 7 premier choix** — contours plus nets, couleurs plus plates, exactement ce qu'il faut pour un logo mascotte vectorisable.

**Mots-clés efficaces** : `mascot logo`, `cartoon character`, `friendly`, `bold outlines`, `flat colors`, `limited palette`, `simple shapes`.

**Pièges** : V7 sans raw → trop de détails réalistes. "mascot" seul → MJ peut faire un patch sportif.

---

### L6 — Texturé / Craft / Vintage

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | **100-300** | raw | 1:1 | modern, clean, digital, gradient, photorealistic |

**INVERSE des autres logos** — ici les textures sont VOULUES. Stylize plus haut pour que MJ génère de l'usure et de la patine.

**Mots-clés efficaces** : `distressed`, `weathered`, `letterpress`, `hand-stamped`, `woodcut`, `linocut`, `halftone dots`, `ink splatter`.

**Pièges** : "clean/minimal" → tue les textures voulues. Un seul medium par prompt ("distressed" OU "letterpress", pas les deux).

---

## §6. Patterns & Textures

### T1 — Pattern Seamless

| Mode | --stylize | --style | --ar | --tile | --no |
|---|---|---|---|---|---|
| `--v 7` | 200-500 | standard | **1:1** | **obligatoire** | text, watermark, border |

**`--tile` obligatoire** — crée la tuile répétable. Ajouter aussi "seamless" dans le texte du prompt.

**Mots-clés efficaces** : `seamless repeating pattern of [sujet]`, spécifier la couleur de fond, `high detail`, `intricate`.

**Pièges** : Ne PAS upscaler les tiles. Ratio non-carré complique le tiling. `--chaos` trop élevé casse le seamless.

---

### T2 — Texture Abstraite

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 300-600 | standard (fluide) ou raw (brut) | 1:1, 16:9 | text, face, person, object |

**Stylize élevé** — les textures profitent de la créativité de MJ. Raw pour du brut/industriel, standard pour du fluide/organique.

**Mots-clés efficaces** : `cracked ink`, `halftone dots`, `brushed metal`, `marble veins`, `fluid abstract`, `organic grain`. Un seul matériau par prompt.

**Pièges** : "texture" seul → collage conceptuel. Trop de matériaux mélangés → frankenstein.

**--sref** : `2098178002` (Gradients abstraits), `2361091909` (Monochrome Grainy)

---

### T3 — Pattern Géométrique

| Mode | --stylize | --style | --ar | --tile | --no |
|---|---|---|---|---|---|
| `--v 7` | 100-250 | raw | **1:1** | **recommandé** | organic, natural, photograph, realistic |

**Raw** — empêche MJ d'arrondir les angles ou d'ajouter des effets "artistiques".

**Mots-clés efficaces** : `geometric tessellation`, `tiling pattern`, `grid pattern`, `mosaic`, `sharp angles`, `mathematical precision`. Références : `M.C. Escher`, `Islamic tessellation`, `Art Deco pattern`.

**Pièges** : MJ ne fait PAS de géométrie parfaite. "complex tessellation" → chaos visuel. "fractal" → impressionnant mais rarement utilisable comme pattern.

---

## §7. Registres spécialisés

### F2 — Mockup (device, packaging)

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 100-250 | raw | 3:2, 16:9 | text, logo (si overlay prévu), people |

**Mots-clés efficaces** : `minimal product mockup`, `floating smartphone`, `packaging mockup`, `studio lighting`, `clean perspective`.

---

### F3 — UI/UX Design Elements

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 0-80 | raw | 16:9, 3:2 | realistic, 3d |

**Mots-clés efficaces** : `flat UI kit`, `dashboard wireframe`, `minimal interface`, `material design`, `Figma-style`.

---

### F4 — 3D Render (clay, glass, metallic)

| Mode | --stylize | --style | --ar | --no |
|---|---|---|---|---|
| `--v 7` | 200-500 | standard | 16:9, 3:2 | sketch, flat, watercolor |

**Mots-clés efficaces** : `3D render`, `octane render`, `clay render`, `glass material`, `HDRI lighting`, `PBR materials`.

---

## §8. Paramètres avancés

### --personalize / --p

Applique un profil esthétique appris via feedback. Activé par défaut si un profil existe.

| Famille | Recommandation |
|---|---|
| Logos (L1-L6), flat (I1), line art (I2), infographie (I7), UI (F3) | **Désactiver --p** — contrôle strict requis |
| Photos (P1-P6, F1/F2) | `--p` ok si profil orienté photo |
| Illustrations stylisées (I4, I5, I6, F4) | `--p` optionnel |

`--style raw` n'annule PAS l'effet de `--p`.

### --cref + --cw (character reference + weight)

`--cref` = image de référence personnage. `--cw` = poids 0-100 (100 = copie rigide, 40-60 = bon mix).

| Usage | --cw |
|---|---|
| I6 mascotte — fiche personnage | 60-80 |
| I6 mascotte — variations de scènes | 40-60 |
| L5 logo mascotte — garder silhouette | 30-50 |

`--cw` n'a d'effet que s'il y a `--cref`.

### --sref + --sw (style reference + weight)

`--sref` = code de style. `--sw` = poids 0-1000 (0 = inspiration légère, 1000 = copie du style).

| Famille | --sw |
|---|---|
| Photos (P1-P6) | 100-400 |
| Illustrations (I1-I7) | 200-600 |
| Logos (L1-L6) | 50-200 (prudence) |
| Patterns/Textures (T1-T3) | 300-700 |

**Bibliothèques --sref** : srefcodes.com (4800+ codes v7), sref-midjourney.com (5600+ codes), midlibrary.io (5500+ styles). Les codes v6 ne produisent pas le même résultat en v7.

### --iw (image weight) avec image prompt

Image ref = copie composition/contenu. `--sref` = copie esthétique/style.

| Famille | --iw |
|---|---|
| Photos (P1-P6) | 0.8-1.2 |
| Illustrations flat/iso/infog (I1/I3/I7) | 0.5-0.8 |
| Illustrations painterly (I4/I5) | 1.0-1.5 |
| Mascottes (I6/L5) | 0.8-1.2 (avec --cref) |
| Logos (L1-L4) | 0.5-0.8 |
| Patterns/Textures (T1-T3) | 1.0-2.0 |

### Prompt weighting (::)

`mot::2` = poids double. `mot::-0.5` = importance négative. V7 pondère déjà les premiers mots fortement.

| Usage | Pattern |
|---|---|
| Photos | `subject::2 background::0.5` |
| Logos | `flat::2`, `monoline::2`, `symbol::2` |
| Patterns | `motif principal::2 background::0.5` |

Pièges : sur-pondération (>3), trop de termes pondérés, negative weights extrêmes.

### Upscaling

| Type | Upscaler MJ |
|---|---|
| Logos, flat, line art, patterns, UI, photos propres | **Subtle** |
| Paysages, éditorial, aquarelle, rétro, concept art | **Creative** |
| Macro, textures détaillées | MJ Subtle → **Topaz/Magnific** externe |
| Logos pour vectorisation | Parfois mieux SANS upscale MJ → vectorisation directe |

**Workflow logo** : choisir variation → upscale Subtle → export PNG → vectorisation (vtracer).

### --repeat / --r

Exploration (logos, patterns, illustrations) : `--r 4-8`. Production (photos, visuels finaux) : `--r 1-2`.

### --draft

Suffisant pour : exploration logos, patterns, textures, styles illustratifs. Insuffisant pour : macro fine, architecture, portraits de prod.

**Workflow** : draft + repeat → sélection seed → relance full quality avec seed fixé + réglages fins.

### Vary Region (inpainting)

Cas d'usage : mains/yeux en portraits, détails de courbe en logos, zones problématiques de patterns, détails archi.

Limites : peut casser le seamless sur patterns. Pour logos précis, corriger en vectoriel. Garde l'influence de `--p`, `--sref`, `--cref` du job d'origine.

---

## §9. Tableau récapitulatif

| # | Registre | Mode | --s | --style | --ar | --tile | --no clé |
|---|---|---|---|---|---|---|---|
| P1 | Éditorial | --v 7 | 250-500 | raw opt. | 16:9 | — | stock, generic, posed |
| P2 | Macro | --v 7 | 200-400 | raw | 1:1 | — | product shot, human |
| P3 | Portrait | --v 7 | 100-250 | **raw** | 2:3 | — | plastic skin, airbrushed |
| P4 | Produit | --v 7 | 100-300 | raw | 1:1 | — | people, messy background |
| P5 | Architecture | --v 7 | 200-400 | raw si lignes | 16:9 | — | fisheye, distortion |
| P6 | Paysage | --v 7 | 300-500 | **standard** | 21:9 | — | people, text |
| F1 | Food | --v 7 | 150-300 | raw | 4:5 | — | human, messy background |
| I1 | Flat 2D | --v 7 | 0-100 | **raw** | — | — | ink, hand-drawn, paper, shadow, 3d |
| I2 | Line Art | **--niji 7** | 50-200 | standard | — | — | color, fill, shading |
| I3 | Isométrique | --v 7 | 100-300 | standard | 1:1 | — | perspective, photorealistic |
| I4 | Aquarelle | --v 7 | 250-500 | **standard** | 3:2 | — | photorealistic, digital |
| I5 | Rétro | --v 7 | 200-500 | standard | 2:3 | — | modern, digital, clean |
| I6 | Character | **--niji 7** | 100-250 | standard | 1:1 | — | photorealistic |
| I7 | Infographique | --v 7 | 50-150 | **raw** | 16:9 | — | photograph, realistic |
| L1 | Logo géométrique | --v 7 | **0-30** | **raw** | 1:1 | — | text, shadow, gradient, 3d |
| L2 | Logo figuratif | --v 7 | **20-60** | **raw** | 1:1 | — | text, shadow, gradient |
| L3 | Logo monoline | --v 7 | **10-40** | **raw** | 1:1 | — | fill, shading, color |
| L4 | Logo badge | --v 7 | **30-80** | **raw** | 1:1 | — | photorealistic, 3d |
| L5 | Logo mascotte | **--niji 7** | 50-150 | standard | 1:1 | — | photorealistic, text |
| L6 | Logo vintage | --v 7 | **100-300** | **raw** | 1:1 | — | modern, clean, digital |
| T1 | Pattern seamless | --v 7 | 200-500 | standard | 1:1 | **--tile** | text, watermark |
| T2 | Texture abstraite | --v 7 | 300-600 | selon rendu | 16:9 | — | text, face, object |
| T3 | Pattern géom. | --v 7 | 100-250 | **raw** | 1:1 | **--tile** | organic, natural |
| F2 | Mockup | --v 7 | 100-250 | raw | 3:2 | — | text, people |
| F3 | UI/UX | --v 7 | 0-80 | **raw** | 16:9 | — | realistic, 3d |
| F4 | 3D Render | --v 7 | 200-500 | standard | 16:9 | — | sketch, flat |
