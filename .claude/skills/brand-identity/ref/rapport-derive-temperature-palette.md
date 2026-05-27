# Rapport — Dérive température palette en Phase 3B

## Problème identifié

Les pitchs de Phase 3B produisent systématiquement des palettes **froides/sombres** (noir, gris, cyan, bleu marine) alors que le brief et les préférences esthétiques demandent explicitement du **chaud** (cuivre, terre, vert botanique, crème). La dérive est invisible étape par étape (chaque étape est cohérente avec la précédente) mais massive quand on compare le point de départ (brief) et le point d'arrivée (style-tile).

## Données de référence

### Brief et scoping (source de vérité)
- Brief analysis : `.claude/skills/brand-identity/outputs/test-camille-test-20260319-13383/camille-brief-analysis.md`
- Scoping : `.claude/skills/brand-identity/outputs/test-camille-test-20260319-13383/camille-scoping.md`

### Directives de température du brief
Extraites du scoping et des préférences esthétiques validées :
- **« Température chaude : cuivre, terre, vert botanique, crème — PAS de bleu tech »**
- **« Qualité artisanale visible : craft, trace de main humaine »**
- **« Double registre : Blueprint (plan technique, tracés précis) + Surréalisme architectural (observatoires, instruments, mécanismes) »**
- **« Registre = stratège-artisan — rigueur intellectuelle + sens du récit »**
- Ventre mou explicite : « Pas de bleu primaire (électrique, marine, cyan) »

### Pitchs produits (résultat observé)
Session : `test-camille-test-20260319-13383`

| Concept | Palette | Température réelle | Conforme brief ? |
|---------|---------|-------------------|-----------------|
| Chambre Sourde | `#1C1C1E` noir + `#6B6B6F` gris + `#F4F3F0` crème + `#2A6B5E` teal | FROID | ❌ |
| Collimateur | `#0A0A0F` noir + `#E0E8F0` blanc bleuté + `#00D4AA` cyan-menthe + `#3A3A4A` gris | FROID | ❌ |
| Chromatogramme | `#1B2D45` bleu marine + `#00B4D8` cyan + `#E63946` rouge + `#F1FAEE` blanc verdâtre | FROID + BLEU | ❌❌ (violation ventre mou) |

### Style-tiles générés
Dans le même dossier `test-camille-test-20260319-13383/` :
- `camille-style-tile-c1.html` (Chambre Sourde)
- `camille-style-tile-c2.html` (Collimateur)
- `camille-style-tile-c3.html` (Chromatogramme)

### Concepts narratifs (pour comparaison)
- `camille-concepts-narratifs.md` dans le même dossier
- Les concepts sont : La Chambre Sourde (acoustique), Le Collimateur (optique), Le Chromatogramme (chimie analytique)

## Analyse : où ça décroche

### Les concepts narratifs NE SONT PAS le problème

Les 3 concepts (Chambre Sourde, Collimateur, Chromatogramme) sont des métaphores scientifiques/instrumentales. Mais ils ne dictent PAS une palette froide :

- **Chambre Sourde** = « espace où le bruit est absorbé ». Une chambre anéchoïque peut être en bois, feutre naturel, matériaux absorbants chaleureux. Le concept parle de SOUSTRACTION, pas de NOIR.
- **Collimateur** = « aligner la lumière en faisceau ». Un collimateur peut être un instrument en laiton poli sur un banc optique en bois (science victorienne = CHAUD). Le concept parle d'ALIGNEMENT, pas de FROIDEUR.
- **Chromatogramme** = « séparer en bandes lisibles ». La chromatographie sur papier produit des bandes aquarellées (carnet de labo = CHAUD). Le concept parle de SÉPARATION, pas de BLEU MARINE.

L'avis du DA dans le concept narratif de la Chambre Sourde contient même un WARNING explicite : « Le registre du silence/vide peut basculer dans l'austérité repoussante si l'exécution design ne trouve pas le bon dosage entre negative space radical et **chaleur humaine** ».

### Le décrochage est en Phase 3B (Design Dérivé)

Le designer reçoit :
1. Le concept narratif (neutre sur la température — ne dicte pas froid)
2. Le warning du DA (« attention à la froideur »)
3. Les préférences esthétiques (« chaud, craft, blueprint ») — si transmises via 3B-0
4. Les territoires créatifs (Principal « Dévoilement Stratégique » = chirurgicale, lucide / Tertiaire « Autorité Sans Costume » = artisanale-premium)

Et produit : noir mat, gris anthracite, teal/cyan, achromatique. Registre « studio d'enregistrement professionnel » / « laboratoire optique » / « laboratoire de chimie ».

### Le mécanisme de la dérive

Le LLM associe les NOMS des concepts à des univers visuels de son training :
- « Chambre anéchoïque » → noir, mousse acoustique, studio pro, technique
- « Collimateur » → noir optique, laser, laboratoire, instrument froid
- « Chromatogramme » → bleu nuit, cyan, labo chimie, écran de mesure

Ces associations sont plus fortes que les directives explicites du brief (« température chaude, craft visible, blueprint »). Le designer dérive du CONCEPT (associations LLM) au lieu de dériver du BRIEF (directive chaude + craft).

C'est le même pattern que le biais typographique Instrument Serif : **le LLM suit ses associations internes (training) plus fort que les contraintes explicites (prompt)**.

## Ce qui fonctionne vs ce qui ne fonctionne pas

| Aspect | Statut |
|--------|--------|
| Cohérence concept → design | ✅ Chaque choix design est traçable au concept |
| Cohérence intra-pitch | ✅ Palette/typo/surface forment un système cohérent |
| Registre sensoriel des fonts | ✅ Les fonts matchent les concepts |
| Émotion « Évidence » | ✅ Bien incarnée |
| Ancrage ICP investisseurs | ✅ Le premium est lisible |
| Température brief → palette | ❌ INVERSION (chaud → froid) |
| Double registre Blueprint + Surréalisme | ❌ ABSENT (remplacé par « instrument scientifique ») |
| Craft visible / artisanal | ❌ ABSENT (remplacé par « technique/industriel ») |
| Ventre mou « pas de bleu » | ❌ VIOLÉ par le Chromatogramme |
| Registre « stratège-artisan » | ❌ Glissé vers « ingénieur-scientifique » |

## Piste de correction

Le cadre de compatibilité esthétique est actuellement un **filtre a posteriori** dans le prompt `phase-3b-design.md` (section « CADRE DE COMPATIBILITÉ ESTHÉTIQUE ») :
> « Le cadre esthétique DÉLIMITE le terrain de jeu de tes choix design — il ne les DICTE pas. »
> « Hiérarchie : Territoires + Concept narratif GÉNÈRENT → Cadre esthétique FILTRE. »

Le problème est structurel : le cadre esthétique FILTRE mais ne GÉNÈRE pas. Le concept génère, et il génère froid (associations LLM). Le filtre est trop faible pour corriger la direction une fois qu'elle est prise.

**L'hypothèse de correction** : remonter les contraintes de température et de registre esthétique au niveau de la GÉNÉRATION (pas du filtrage). Le designer devrait recevoir la température comme une ENTRÉE au même titre que le concept, pas comme un check à faire après avoir déjà choisi.

Concrètement dans le prompt `phase-3b-design.md`, la section « Éléments qui CROISENT les deux sources » (ligne 67+) décrit comment la température de palette est dérivée :
> « Étape 1 : les territoires orientent la zone macro (chaud/froid/neutre). Étape 2 : le concept narratif INFLEXE la température. »

Le problème est que l'étape 2 (concept → inflexion) ÉCRASE l'étape 1 (territoires → direction macro) au lieu de l'infléchir. Le concept « Chambre Sourde » tire tellement fort vers le froid que la direction macro « chaud » (venant des territoires et du brief) est complètement écrasée.

## Fichiers du pipeline à examiner pour la correction
- `phases/phase-3b-design.md` — le prompt du designer, section « CADRE DE COMPATIBILITÉ ESTHÉTIQUE » (ligne ~214+) et section « Éléments qui CROISENT les deux sources » (ligne ~67+)
- `SKILL.md` — section 3B-0 (ligne ~958+) où les préférences esthétiques sont assignées par concept
- `ref/font-matching-rules.md` — les règles de matching (registre sensoriel) qui pourraient aussi intégrer une contrainte de température
