# Guide Nano Banana 2 — Prompting pour BIG

> **Version NB2** : Nano Banana 2 (Gemini 3.1 Flash Image) + Nano Banana Pro (Gemini 3 Pro Image)
> **Dernière vérification** : 2026-04-17
> **Règle de fraîcheur** : Avant de générer des prompts NB2, le subagent DOIT faire un `WebSearch("nano banana latest version 2026")`. Si une version post-avril 2026 change les modèles ou capacités → alerter l'utilisateur et adapter les recommandations.

---

## §0 — Pourquoi Nano Banana 2 dans BIG

**Positionnement vs MidJourney et Recraft** :

| Critère | Nano Banana 2 | MidJourney v7 | Recraft V4 |
|---------|---------------|---------------|-----------|
| Prompt adherence (composition, layout strict) | **Excellente** — le modèle planifie la composition avant rendu | Moyenne — dérive esthétique fréquente | Bonne — mais limitée en photoréalisme |
| Photoréalisme éditorial (Kinfolk, still life) | **Excellente** — registre natif | Excellente avec bon prompt | Limitée |
| Cohérence multi-images (brand kit) | **Excellente** (95%+ via refs role-scopées) | Moyenne | Bonne |
| Multi-turn editing (iterer sur l'image) | **Killer feature** — "same image, change X only" | Vary Region seulement | Remix seulement |
| Illustrations flat/vector | Faible | Faible | **Excellente** |
| Logos complexes / lettermarks | Faible | Excellente | Bonne |

**Usages BIG où NB2 est recommandé en premier** :
- Photos éditoriales macro/still life/abstrait fluide (P1, P2, F1)
- Heroes avec composition contrainte (negative space pour titre, focal side strict)
- Mockups produit (F2), UI sur device (F3)
- Quand plusieurs assets doivent partager une signature visuelle précise (brand kit)

**Usages où MJ ou Recraft restent préférés** :
- Illustrations vectorielles (I1-I7) → Recraft
- Logos (L1-L6) → MidJourney (REX validé)
- Patterns seamless (T1) → MidJourney (`--tile`)
- Portraits (P3) → MidJourney (--style raw + grain filmique reste supérieur)

---

## §1 — Modèles : Flash vs Pro

| Modèle | Nom API | Contexte input | Résolutions | Vitesse | Usage BIG |
|--------|---------|----------------|-------------|---------|-----------|
| **Nano Banana 2** (Flash) | Gemini 3.1 Flash Image | 131K tokens | 0.5K / 1K / 2K / 4K | ~8s | **Itération rapide, drafts, exploration** |
| **Nano Banana Pro** | Gemini 3 Pro Image | 65K tokens | 1K / 2K / 4K | ~25s | **Rendu final, précision maximale** |

**Règle BIG** :
- Explorer en Flash (quick, 20-50 variations pour trouver la bonne direction)
- Valider la composition en Flash
- **Basculer Pro pour la version finale 4K** avant upscale

**Accès** : Gemini AI Pro ($19.99/mois) = 100 gén/jour Pro. Suffisant pour BIG. AI Ultra ($249/mois) seulement pour volume intensif.

**Aspect ratios supportés** :
- Pro et Flash : 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
- Flash uniquement : ratios extrêmes 1:4, 4:1, 1:8, 8:1

---

## §2 — Principes fondamentaux (non négociables)

### 2.1 Prose dense narrative, JAMAIS JSON

**Vérité validée (avril 2026)** : Google Cloud officiel (mars 2026) + Pillitteri A/B test + Charlie Hills + nanobananaprompt.org = **100% prose narrative**. Zéro JSON.

Les chiffres "JSON = 89% vs prose = 72% adherence" circulant sur X sont **folklore non vérifié**. Aucun benchmark reproductible.

**Test Pillitteri (2026)** : *"Le prompt narratif a produit une image cohérente. Le prompt en liste/JSON a produit un mélange déconnecté d'éléments, avec un éclairage qui ne dialoguait pas avec l'environnement."*

**Mantra Google répété 3× dans les docs** : *"Describe the scene, don't just list keywords."*

### 2.2 Zéro négation (formulation positive)

Google déconseille explicitement les négations.

❌ `"no cars"` → ✅ `"empty street"`
❌ `"not too dark"` → ✅ `"soft ambient lighting, clearly visible"`
❌ `"no text visible"` → ✅ `"pure abstract surface, organic forms only"`

Pour la lisibilité future (overlay CSS), éviter activement le texte via formulation positive : *"unbroken surface texture, typographically neutral composition"*.

### 2.3 Terminologie photographique précise

NB2 a été entraîné sur des corpus éditoriaux massifs. Il reconnaît et respecte :
- **Caméras réelles** : Hasselblad H6D-100c, Phase One XF IQ4, Leica M11, Canon EOS R5
- **Focales précises** : 24mm / 35mm / 50mm / 85mm / 100mm macro / 120mm macro / 180mm macro
- **Apertures** : f/1.4, f/2.8, f/4, f/8 (avec conséquence sur profondeur de champ)
- **Films** : Kodak Portra 400, Fujifilm Classic Chrome, Cinestill 800T, Ektachrome
- **Lumière** : key light / fill light / rim light / back light + direction (camera-left, top-right, overhead)

### 2.4 Conversational editing (multi-turn)

**La force killer de NB2** : tu peux itérer sur l'image existante avec des phrases naturelles.

✅ `"Same image. Change key light to golden hour, warmer temperature"`
✅ `"Same image. Make material more matte, less glossy specular"`
✅ `"Keep composition exactly. Move focal point 20% left to open headline space"`

**Limite critique** : **3-4 turns max** avant dégradation visible (skin smearing, color drift, texture bleed). Mécanisme : chaque turn édite la sortie précédente, pas l'original → accumulation type JPEG.

**Workaround pro** : investir dans UN prompt initial très bien construit plutôt que 10 turns chaînés.

### 2.5 Deep reasoning = prompts riches acceptés

NB2 planifie la composition AVANT de rendre (deep reasoning). Il accepte donc des prompts longs avec contraintes imbriquées (palette + lens + lighting + composition + mood) que MJ dilue. **Pas de plafond à 6 lignes comme MJ** — tu peux aller jusqu'à 200-300 mots de prose dense et le modèle restera fidèle.

---

## §3 — Formule universelle (Google officiel)

```
[SUJET + ACTION + ÉTAT] + [COMPOSITION + CADRAGE + NEGATIVE SPACE]
+ [LOCATION/CONTEXTE/ARRIÈRE-PLAN]
+ [LIGHTING : source, direction, qualité, température]
+ [CAMERA : marque/modèle, lens mm, aperture]
+ [COLOR PALETTE : hex codes intégrés + rôles]
+ [STYLE : référence éditoriale, film stock, grading]
+ [ASPECT RATIO + RÉSOLUTION]
```

Le prompt est UNE PHRASE LONGUE (ou 3-4 phrases), pas une liste. Les virgules et les points scandent les groupes conceptuels.

---

## §4 — Structure de prompt type (template détaillé)

### Template prose pure (recommandé défaut)

```
[Camera + lens + aperture] [shot type] of [subject in precise action/state],
[composition description with focal position and negative space side].
[Lighting description: source, direction, quality, color temperature].
[Material / texture / surface details].
[Palette with HEX codes in narrative form, muted/saturated adjectives, film stock reference].
[Aspect ratio] format.
```

### Exemple (pour notre cas Camille C1 hero) :

```
Ultra-macro editorial photograph captured on a Hasselblad H6D-100c with
a 120mm macro lens at f/4, extreme close-up of deep burgundy ink #6B2D3E
slowly diffusing into still distilled water, caught mid-bloom. The ink
mass occupies the center-right of the frame at 35% coverage, spiraling
inward with feathered translucent edges, leaving generous negative space
in the upper-left quadrant for editorial typography. Single cold
directional key light from camera-left through a large softbox, subtle
rim from behind creating backlit translucency in the peripheral ink
tendrils, no specular reflections from studio equipment. Deep navy
#1E2D42 undertones thread through the core like fracture veins, while
delicate terracotta #C4654A filaments suspend at the bloom boundary.
Gradient backdrop transitions from near-black #1A1F2A at right edge to
warm cream #F2EDE6 in upper-left. Editorial still life aesthetic of
Kinfolk and Cereal magazine, shot on Kodak Portra 400 color science,
muted contrast, subtle film grain, razor-sharp focus on the core with
soft depth-of-field falloff on the tendrils. 16:9 format at 4K resolution.
```

### Option "tagged prose" (Joulyan format — pour use cases où la discipline "une variable à la fois" est critique)

C'est un **hybride lisible** (ni JSON, ni prose pure). À utiliser quand tu veux itérer proprement sur une variable à la fois lors du multi-turn.

```
GOAL: Hero editorial macro, 16:9, 4K
SUBJECT: [description dense du sujet en prose]
COMPOSITION: [focal position, negative space side, frame occupation %]
LIGHTING: [key + fill + rim + color temp]
CAMERA: [brand model], [lens mm], [aperture], [shot type]
MATERIAL: [texture, surface qualities, translucency]
PALETTE: [hex codes + rôles, film stock reference]
STYLE: [reference aesthetic, magazine, grading]
ASPECT: 16:9
```

**⚠ Cette option est SECONDAIRE.** Le défaut reste la prose narrative pure. Les tagged prose est utile uniquement quand tu sais d'avance que tu vas itérer systématiquement sur une variable spécifique.

---

## §5 — Références role-scopées

### 5.1 Règles fondamentales

- **Max technique** : 14 images (official Google)
- **Haute fidélité** : 6 premières images (folklore largement confirmé)
- **Sweet spot pro** : **3-4 références role-scopées**
- **Règle d'or** : **1 référence = 1 job** (jamais "cette image pour le lighting ET la composition")

### 5.2 Rôles possibles

| Rôle | Ce que la réf apporte | Exemple dans le prompt |
|------|----------------------|-----------------------|
| **Lighting** | Direction, qualité, température de lumière | *"Use Image A strictly for lighting direction and tonal register"* |
| **Material** | Texture, fini, matérialité | *"Use Image B for material behavior and translucency only"* |
| **Composition** | Framing, placement, negative space | *"Use Image C for framing and negative space balance only"* |
| **Atmosphere / Palette** | Mood général, grading couleur | *"Use Image D for color palette and atmospheric mood only"* |
| **Character / Face** | Identité d'un personnage (strict lock) | *"Preserve the face from Image E exactly, 100% accuracy"* |

### 5.3 Formulation type dans le prompt

Ajouter à la fin du prompt prose :

```
Reference A (lighting): [upload filename]
Reference B (material/texture): [upload filename]
Reference C (composition): [upload filename]

Use Reference A strictly for lighting direction and tonal register.
Use Reference B for physical material behavior and translucency.
Use Reference C for framing and negative space balance.
```

### 5.4 Upload order

**Critique** : les 6 premières slots sont en haute fidélité. Uploader les refs **dans l'ordre où elles sont nommées** dans le prompt, **par priorité décroissante**.

Exemple : si lighting est la contrainte la plus critique → Image A (lighting) en slot 1. Si palette est secondaire → en slot 3.

### 5.5 Anti-patterns

❌ **Réfs Pinterest / Unsplash** : NB2 les a massivement vues, dilue le signal
❌ **Réfs AI-generated** : slop in → slop out
❌ **Réfs avec UI visible (screenshots de sites)** : NB2 les interprète comme instructions UI
❌ **Plus de 6 réfs** : diminishing returns, quality degradation
❌ **Même réf pour 2+ jobs** : signal contradictoire

✅ **Sources recommandées** : Cosmos.so (clustering visuel, auto-blurs AI), Savee.it (éditorial human-curated), Are.na (channels conceptuels pro), photos éditoriales magazine (Kinfolk, Cereal, Openhouse)

---

## §6 — Terminologie photographique (vocabulaire qui marche)

### 6.1 Caméras (anchors puissants)

| Caméra | Ce qu'elle évoque | Usage BIG |
|--------|-------------------|-----------|
| **Hasselblad H6D-100c** | Medium format, luxe, éditorial mode/still life | P1, P2, P4 éditoriaux |
| **Phase One XF IQ4** | Medium format, precision, commercial haut de gamme | P4, P5 architecture |
| **Leica M11** | Street/documentaire, contraste élevé, grain argentique | P1 lifestyle authentique |
| **Canon EOS R5** | Polyvalent, contemporain | P1-P6 généraliste |
| **Arri Alexa 35** | Cinéma, motion picture look | P1 cinématique |
| **DJI Mavic 4 Pro** | Aérien, drone | P6 paysage |

### 6.2 Lens (focale = caractère)

| Focale | Effet | Usage |
|--------|-------|-------|
| **24mm tilt-shift** | Lignes droites, architecture | P5 intérieur/extérieur |
| **35mm** | Reportage, champ large naturel | P1 documentaire |
| **50mm** | Neutre, "vision humaine" | Usage général |
| **85mm f/1.4** | Portrait, isolation sujet, bokeh crémeux | P3 portrait |
| **100mm macro f/2.8** | Macro standard, détail serré | P2 texture |
| **120mm macro f/4** | Macro éditorial, profondeur contrôlée | P2 still life premium |
| **180mm macro f/2.8** | Macro extrême, compression de plan | P2 insect-scale |

### 6.3 Apertures (profondeur)

- **f/1.4 – f/2** : Bokeh extrême, focal plane très fin, isolation agressive
- **f/2.8 – f/4** : Profondeur sélective, standard éditorial
- **f/5.6 – f/8** : Net partout, commercial/produit
- **f/11+** : Hyperfocal, paysage

### 6.4 Lighting vocabulary

**Sources** : key light (principale), fill light (remplissage), rim light (contour), back light (contre-jour), practical light (intégrée à la scène), natural light

**Qualité** : soft (diffusée, softbox), hard (directe, nue), diffused, directional, rasante, sculptural

**Température** : warm (2800-3500K, tungsten), neutral (5000-5500K, daylight), cool (6500-7500K, overcast, fluorescent)

**Setups classiques** : three-point (key + fill + rim), Rembrandt (45° haut), split (90°), butterfly (overhead), clamshell, window light (natural), golden hour (contre-jour chaud)

### 6.5 Film stock (grading couleur)

| Film | Palette | Usage |
|------|---------|-------|
| **Kodak Portra 400** | Chair fidèle, tons chauds, grain fin | Portrait, lifestyle éditorial |
| **Fujifilm Classic Chrome** | Saturation contrôlée, verts/bleus éditoriaux | Street, documentaire |
| **Cinestill 800T** | Tungsten daylight, halation, cyberpunk | Néon, nocturne |
| **Kodak Ektachrome** | Slides, bleus saturés, blancs chauds | Éditorial voyage |
| **Ilford HP5** | N&B, grain moyen, contraste modéré | N&B reportage |

### 6.6 Références éditoriales magazine

Mentionner un magazine LITTÉRALEMENT dans le prompt ancre puissamment le registre :

- **Kinfolk** : still life minimaliste, tons crème, lumière douce, composition zen
- **Cereal** : voyage, architecture, palettes désaturées, large format
- **Monocle** : documentaire éditorial, reportage international
- **Openhouse** : intérieur, architecture, naturel et texture
- **The Gentlewoman** : portrait mode, lumière naturelle, féminité éditoriale
- **Hodinkee** : macro watches, éclairage produit luxe, textures métalliques
- **Another Magazine** : mode avant-garde, expérimental
- **i-D** : street, fashion contemporaine

---

## §7 — Prompting par registre BIG

NB2 couvre efficacement : **P1-P6, F1-F3** (tous les registres photo) + **T2** (textures photo, painterly nuancé) + **F2 mockup** + **F4 3D photoréaliste**.

Pour les autres (illustrations, logos, patterns vector) → MJ ou Recraft restent préférés.

### P1 — Éditorial / Lifestyle

**Patterns qui marchent** :
- *"Editorial photograph shot on [Hasselblad/Leica]"* + 85mm ou 35mm + f/1.4-2.8
- Moment capture : "candid", "unposed", "caught mid-action", "frozen instant"
- Référence magazine (Kinfolk, Cereal, Monocle)
- Film stock Kodak Portra 400 ou Fuji Classic Chrome

### P2 — Macro / Texture / Matière

**Patterns qui marchent** :
- Focale macro précise (100mm / 120mm / 180mm)
- f/2.8-f/4 pour DOF sélective, f/8 pour net partout
- Verbes-moment pour fluides : "frozen mid-bloom", "tendrils suspended", "caught diffusing", "long-exposure flow"
- Matière précise : *"viscous India ink"* plutôt que "ink", *"burnished walnut grain"* plutôt que "wood"
- Lumière rasante (45°) pour révéler relief
- Référence Hodinkee pour luxe, Kinfolk pour éditorial

### P3 — Portrait Environnemental

**Patterns qui marchent** :
- 85mm f/1.4 ou 50mm f/1.8
- *"Environmental portrait"* (pas juste "portrait")
- Skin texture explicite : *"visible pores, natural skin texture, subtle imperfections"*
- Expression précise : *"slight knowing smile"* (pas "happy")
- Mains à cacher si possible (encore imparfaites)

### P4 — Produit / Still Life

**Patterns qui marchent** :
- Phase One ou Hasselblad + 80mm-120mm + f/4-8
- Setup éclairage explicite : *"three-point softbox setup"* ou *"single overhead diffused light"*
- Surface nommée : *"polished walnut"*, *"brushed aluminum"*, *"matte ceramic"*
- Backdrop spécifié : *"seamless cream paper"*, *"black velvet"*, *"tonal gradient backdrop"*
- Référence : Hodinkee, product commercial photography

### P5 — Architecture / Intérieur

**Patterns qui marchent** :
- 24mm tilt-shift (corrige verticales)
- Matériaux explicites : *"polished concrete, raw timber, brushed steel"*
- *"Symmetrical composition, straight vertical lines"*
- Architecte cité : *"Zaha Hadid-inspired"*, *"Tadao Ando aesthetic"*
- Référence : Openhouse, Dezeen, Cereal

### P6 — Paysage / Aérien

**Patterns qui marchent** :
- *"Drone shot"* (proximité) vs *"aerial view"* (abstrait)
- DJI Mavic 4 Pro + 24mm wide
- Plans explicites : foreground / midground / background
- Atmospheric perspective : *"layers of fog"*, *"hazy distance"*
- Golden hour ou blue hour pour drama
- Référence : National Geographic, Cereal

### F1 — Food

**Patterns qui marchent** :
- *"Food photography"* + angle explicite (overhead 90°, 45°, eye-level)
- Éclairage : *"soft top light"* ou *"window light from camera-left"*
- Verbes sensoriels : *"glistening", "steam rising", "freshly plated"*
- Référence : Bon Appétit, Apartamento

### F2 — Mockup

**Patterns qui marchent** :
- *"Floating [device] mockup"* ou *"packaging mockup"*
- Setup : *"seamless backdrop, subtle drop shadow"*
- Angle : *"eye-level perspective"* ou *"slightly tilted 3/4 view"*

### F3 — UI sur device

**Patterns qui marchent** :
- Device + contexte : *"MacBook Pro on marble desk with morning light"*
- *"Realistic screen reflection"* pour crédibilité
- ⚠ L'UI lui-même : NB2 peut générer un UI abstrait crédible mais PAS ton UI précis. Pour l'UI réel → screenshot overlay en post.

### T2 — Texture abstraite photo

**Patterns qui marchent** :
- Proche P2 macro mais rempli bord-à-bord
- *"Fills entire frame edge-to-edge, continuous texture extending beyond all four edges"*
- *"Homogeneous distribution of detail, no single focal point"*
- Référence : papier photographique, encre, surface minérale

### F4 — 3D / Fond surréaliste photoréaliste

**Patterns qui marchent** :
- *"3D render, octane-rendered quality"*
- Matériaux PBR : *"glass material with caustics"*, *"brushed metal with fingerprint details"*
- HDRI lighting : *"studio HDRI environment"*
- ⚠ Pour 3D stylisé/illustratif → Recraft V4 Pro préféré

---

## §8 — Multi-turn iteration (templates)

### 8.1 Règles multi-turn

1. **Limite** : 3-4 turns max avant dégradation visible
2. **Pattern** : commencer par *"Same image."* ou *"Keep X exactly."* pour préserver l'état
3. **Une variable à la fois** : ne pas changer lighting ET composition ET palette en un turn — le modèle dilue
4. **Si >4 turns nécessaires** → retour au prompt initial, réécrire

### 8.2 Templates par variable

**Lighting** :
- `"Same image. Change key light to golden hour, warmer temperature"`
- `"Same image. Stronger chiaroscuro, darker shadows, preserved highlights"`
- `"Same image. Soften the key light, remove harsh shadows"`
- `"Same image. Add subtle rim light from behind, cool blue temperature"`

**Material / Texture** :
- `"Same image. Make material more matte, less glossy specular"`
- `"Same image. Reveal more translucency in the peripheral zones"`
- `"Same image. Add subtle film grain, Kodak Portra 400 aesthetic"`
- `"Same image. Increase micro-detail on the focal surface"`

**Composition** :
- `"Keep lighting and material exactly. Move focal point 20% to the left to open right side for headline"`
- `"Keep lighting exactly. Expand negative space in upper third"`
- `"Same image. Slight asymmetry, less centered composition"`
- `"Same image. Tighter crop, subject at 50% frame coverage"`

**Color / Palette** :
- `"Same image. Deeper burgundy saturation, less pink dilution"`
- `"Same image. Reduce the terracotta tones by 40%, enhance navy undertones"`
- `"Same image. Warmer color grading, Kodak Portra 400"`
- `"Same image. Cooler temperature, editorial desaturation"`

**Background** :
- `"Same subject exactly. Replace background with seamless cream gradient #F2EDE6"`
- `"Same subject. Pure black velvet backdrop, zero reflection"`

### 8.3 Ordre d'itération recommandé

Si v1 a ~70% de ce qu'on veut, itérer dans cet ordre :
1. **Composition** (focal, negative space) — c'est ce qui conditionne tout le reste
2. **Lighting** (direction, qualité, température)
3. **Material / texture**
4. **Color / palette / grading**
5. **Background** en dernier

---

## §9 — Aspect ratios et résolutions

### 9.1 Aspect ratios supportés

| Ratio | Flash (NB2) | Pro | Usage BIG |
|-------|-------------|-----|-----------|
| 1:1 | ✅ | ✅ | Accent, clip-path |
| 16:9 | ✅ | ✅ | Hero full-bleed desktop |
| 21:9 | ✅ | ✅ | Hero ultra-wide, cinematic |
| 3:2 | ✅ | ✅ | Éditorial standard |
| 4:5 | ✅ | ✅ | Portrait, mobile |
| 9:16 | ✅ | ✅ | Mobile vertical, story |
| 3:4, 2:3, 4:3, 5:4 | ✅ | ✅ | Formats variés |
| 1:4, 4:1, 1:8, 8:1 | ✅ | ❌ | Bannières extrêmes |

### 9.2 Résolutions

- **Flash** : 0.5K (512px), 1K, 2K, 4K
- **Pro** : 1K, 2K, 4K

**Règle BIG** : toujours demander 4K dans le prompt (*"rendered at 4K resolution"*) ET le sélectionner dans le dropdown UI.

---

## §10 — "Negative prompts" en formulation positive

NB2 déconseille les négations explicites. Pour exclure un élément, utiliser la formulation positive :

| À éviter | ❌ Négation | ✅ Positive |
|----------|------------|-------------|
| Texte dans l'image | "no text" | "pure abstract surface, typographically neutral" |
| Logos | "no logos" | "unbranded, abstract composition" |
| Personnes | "no people" | "empty unpopulated scene" |
| UI visible | "no UI" | "raw photography, no graphic overlay" |
| Reflets studio | "no studio equipment reflections" | "clean specular highlights, absorbed background" |
| Grain excessif | "no grain" | "smooth film transfer, minimal texture" |
| Flou accidentel | "not blurry" | "razor-sharp focus, tack-sharp on subject" |

**⚠ Exception limitée** : certains termes restent acceptables en fin de prompt comme "safety net" de baseline : *"Avoid: watermark, signature, caption, text overlay"* — NB2 les interprète mais moins fiablement que la formulation positive.

---

## §11 — Quand utiliser JSON (exceptions étroites)

**JSON est justifié UNIQUEMENT dans ces cas** (démonstrations concrètes documentées) :

| Use case | Raison |
|----------|--------|
| **Édition ciblée** d'une image existante (changer 1 couleur sans toucher au reste) | JSON force l'isolation de la variable |
| **Multi-subject avec couleurs distinctes** (anti-attribute-bleeding) | JSON empêche les contaminations croisées |
| **Infographics / layouts data-driven** | Structure tabulaire native |
| **Character/face consistency stricte** (100% face lock) | Contrainte forte sur attribut critique |
| **Batch / automation API** (brand kit de 10+ assets) | Swap programmatique du champ `subject` |

**Pour BIG** : tous les cas hero éditoriaux macro/still life/abstract = **prose dense, pas JSON**.

Le JSON peut être envisagé pour :
- Générer 10+ variations d'un même hero (brand kit) une fois la direction validée
- Éditer une image existante pour la Phase 4 sans régénérer

**Format JSON si vraiment nécessaire** (canonical 11 fields) :
```json
{
  "intent": "...",
  "subject": "...",
  "composition": "...",
  "environment": "...",
  "lighting": "...",
  "camera": "...",
  "color_palette": "...",
  "style": "...",
  "reference_roles": {...},
  "aspect_ratio": "16:9",
  "resolution": "4K"
}
```

---

## §12 — Erreurs courantes

| Erreur | Pourquoi ça échoue | Solution |
|--------|-------------------|----------|
| Prompt en liste de keywords | NB2 est entraîné sur prose éditoriale | Phrases complètes, langage naturel |
| Négation directe ("no X") | Le modèle interprète le mot-clé | Formulation positive |
| Plus de 6 références | Fidélité dégradée au-delà | Max 3-4 role-scopées |
| Une réf pour 2 jobs | Signal contradictoire | 1 réf = 1 job strict |
| Mix de JSON et prose | Modèle confus | Choisir un format et s'y tenir |
| Multi-turn >4 turns | Dégradation accumulée | Retour au prompt initial |
| "Beautiful", "stunning", "amazing" | Adjectifs génériques ignorés | Terminologie photographique précise |
| Lens sans aperture | Caractère photographique incomplet | Toujours spécifier les deux |
| Référence sans rôle scoped | Le modèle devine le job | Toujours nommer le rôle |
| Palette hors du prompt | Les HEX dans le color picker seul → ignorés | HEX intégrés DANS la prose |
| Magazine non nommé | Registre vague | Citer Kinfolk/Cereal/Hodinkee littéralement |

---

## §13 — Checklist avant génération

Avant de finaliser un prompt NB2 pour le brief visuel, vérifier :

- [ ] **Sujet** décrit avec précision (action, état, matière)
- [ ] **Composition** : focal position + occupation % + negative space side
- [ ] **Lighting** : source + direction + qualité + température
- [ ] **Camera** : marque/modèle + lens mm + aperture
- [ ] **Palette HEX** intégrée dans la prose (2-4 couleurs avec rôles)
- [ ] **Style/référence** : magazine + film stock nommés
- [ ] **Aspect ratio** spécifié dans le prompt (même si défini dans l'UI)
- [ ] **Résolution 4K** mentionnée dans le prompt
- [ ] **Zéro négation** — tout en formulation positive
- [ ] **Références role-scopées** nommées avec `"Use Image X for Y only"`
- [ ] **Pas de JSON** (sauf exception §11)
- [ ] **Ancre stylistique** BIG intégrée verbatim

---

## §14 — Format dans le brief visuel BIG

Quand un prompt NB2 est inclus dans `{brand}-visual-brief.md`, il suit ce format :

```
**Image c{concept}-{n} — {description courte}**
Usage prévu : {Voice Block hero / Atmosphere block / Accent}

**Version Nano Banana 2** :
Modèle : {Pro / Flash}
Aspect ratio : {16:9 / 1:1 / etc.}
Résolution : 4K

\```
[prompt prose dense complet, palette HEX intégrée, vocabulaire photographique,
aspect ratio et résolution mentionnés dans le texte]

Reference A (lighting): [nom du fichier]
Reference B (material): [nom du fichier]
Reference C (composition): [nom du fichier]

Use Reference A strictly for [job].
Use Reference B for [job] only.
Use Reference C for [job] only.
\```

Multi-turn recommandé si v1 ≥ 70% :
- `[template multi-turn adapté à ce prompt]`
- `[template multi-turn alternatif]`
```

Pas de paramètres techniques à la fin (contrairement à MJ). Le prompt est autonome, tout s'écrit en langue naturelle.

---

## §15 — Tableau récapitulatif

| # | Registre | Modèle | Lens/Aperture | Aspect | Références recommandées | Notes |
|---|----------|--------|---------------|--------|------------------------|-------|
| P1 | Éditorial | Pro | 35mm f/2 ou 85mm f/1.4 | 3:2, 4:5 | 1 lighting + 1 mood | Kinfolk/Cereal |
| P2 | Macro | Pro | 100-180mm macro f/2.8-4 | 1:1, 4:5, 16:9 | 1 material + 1 composition | Hodinkee pour luxe |
| P3 | Portrait | Pro | 85mm f/1.4 | 2:3, 4:5 | 1 face + 1 lighting | Natural skin texture |
| P4 | Produit | Pro | 80-120mm f/4-8 | 1:1, 4:5 | 1 material + 1 setup | Phase One aesthetic |
| P5 | Architecture | Pro | 24mm tilt-shift f/8 | 16:9, 21:9 | 1 composition + 1 mood | Openhouse, Dezeen |
| P6 | Paysage | Flash | 24mm wide f/8 | 16:9, 21:9 | 1 mood + 1 composition | National Geographic |
| F1 | Food | Pro | 50-100mm macro f/4 | 4:5, 3:2 | 1 lighting + 1 material | Bon Appétit |
| F2 | Mockup | Pro | 50-85mm f/4 | 16:9, 3:2 | 1 composition + 1 material | Apple commercial |
| F3 | UI/Device | Pro | 50mm f/4 | 16:9 | 1 setup + 1 device | UI overlay en post |
| T2 | Texture | Pro | 100mm macro f/4 | 16:9 | 1 material + 1 mood | Fills edge-to-edge |
| F4 | 3D photoreal | Pro | — (3D render) | 16:9 | 1 material + 1 lighting | PBR materials |

---

*Dernière mise à jour : 17 avril 2026*
*Sources primaires : Google Cloud Ultimate Prompting Guide for Nano Banana (mars 2026), Google DeepMind prompt guide, Pasquale Pillitteri A/B test analysis (avril 2026), Charlie Hills Substack, Joulyan tagged prose format, Perplexity Deep Research synthesis avril 2026.*
