<!--
  AUTO-GÉNÉRÉ — ne pas modifier ce fichier manuellement.
  Source de vérité : ref/pipeline-overview.md (version interne avec "sous le capot")
  Script de build : scripts/build-public-pipeline-overview.py
  Régénération auto au pre-commit (.githooks/pre-commit).
-->

# Brand Identity Generator — Guide du Pipeline

```
   ╔════════════════════════════════════╗
   ║  ██████╗ ██╗ ██████╗               ║
   ║  ██╔══██╗██║██╔════╝  Brand        ║
   ║  ██████╔╝██║██║  ███╗ Identity     ║
   ║  ██╔══██╗██║██║   ██║ Generator    ║
   ║  ██████╔╝██║╚██████╔╝              ║
   ║  ╚═════╝ ╚═╝ ╚═════╝               ║
   ╚════════════════════════════════════╝
```

Bienvenue ! Je suis ton Directeur de Création. Ensemble, on va construire une identité de marque de classe mondiale — de la stratégie jusqu'aux livrables visuels.

---

## /brand-identity

Cet outil génère une identité de marque complète : direction artistique, style-tiles visuels, système de signes, et documentation technique.
Le processus est guidé étape par étape — je te demanderai tes inputs et validations au fur et à mesure.

---

## Écosystème de skills

`/brand-identity` est le pipeline principal de création d'identité. D'autres skills le complètent ou peuvent être invoqués indépendamment :

- **`/test-big`** — Test runner pour reprendre le pipeline BIG à partir d'une phase spécifique sur la base d'une session existante. Utile si tu veux itérer sur la Phase 4 sans refaire le brief et le scoping, ou si le pipeline a planté en cours et que tu veux reprendre là où il s'est arrêté.
- **`/brand-book`** — Génère un brand book HTML éditorial à partir d'un pack BIG complet : cover painterly + intro Identity Card bento + 8 sections documentaires (Big Idea, Concept, Identité, Palette, Typographie, Système, Applications, Photo & Illustration) + closing. Invoqué automatiquement en Phase 8 de BIG, mais peut aussi être lancé seul sur un pack existant.
- **`/landing-page`** — Génère des landing pages HTML auto-portées depuis un brief, un design system, ou directement depuis un pack BIG. *(disponible dans un repo séparé, à venir)*
- **`/visual-prompt`** — Workflow itératif MidJourney → Nano Banana 2 → animation Recraft pour produire des visuels IA niveau Awards. **2 modes** : (1) mode **principal** — génération d'un visuel hero à partir d'un rapport Perplexity ; (2) mode **variantes** — dérivation d'atmosphere/closeup/macro/pov à partir d'un hero existant, en exploitant le framework librairie atmosphère (`nb-prompting-guide.md §11` — 7 types × 4 niveaux d'intensité). Invoqué en Phase 3B-7c.7 (hero) puis Phase 3B-7c.10 + 3B-7e (variantes). Dépend de `/nano-banana-edit` pour les corrections NB2.
- **`/nano-banana-edit`** — Primitive d'édition d'image via l'API Gemini (alias Nano Banana / NB2). Invoqué par `/visual-prompt` pour toutes les corrections atomiques (couleur de fond, grain, tons, clair-obscur, retouche ciblée). Skill **workspace partagé** — disponible dans un repo séparé `nano-banana-edit-portable`, nécessite une clé API Gemini configurée dans `.env`.
- **`/audit-elite`** — Juge **relatif** : compare un style-tile BIG aux étalons Awards et prescrit les corrections pour atteindre le niveau élite. *(disponible dans un repo séparé, à venir)*
- **`/audit-slop`** — Juge **absolu** : évalue un style-tile contre 4 grilles de règles universelles (Craft Moderne / Vercel / BIG Pipeline / Perplexity Temporel) et produit un verdict consolidé. Complémentaire à `/audit-elite`. *(disponible dans un repo séparé, à venir)*

---

## Phase 0 — Preflight Check

Avant la collecte du brief, je lance une **vérification automatique simplifiée** :

- Ce qui est **bloquant** (Node, Python, git — sans ça le pipeline ne tourne pas) et ce qui te manque éventuellement, avec la commande d'install pour chaque
- Un **statut informatif** des dépendances optionnelles (SPG-portable, nano-banana-edit, clé Gemini) — **je ne te demande PAS de les configurer maintenant**. Je te le demanderai au moment où chaque dep sera nécessaire dans le pipeline (juste-à-temps).
- L'**état du repo** vs GitHub (combien de commits de retard si tu n'as pas pull récemment, et un rappel de lancer `./update.sh` si applicable)

Tu peux explorer la Phase 1 à 5 (analyse brief → style-tile) **sans configurer aucune clé API**. Tape juste "continue" ou directement A/B/C/D pour ton mode de brief.

**Gates juste-à-temps en aval** (la dep est demandée seulement quand tu en as besoin) :
- **Phase Logo** → check vtracer (3 options : install rapide / skip)
- **Phase 3B-7c visuel hero** → check nano-banana-edit + clé Gemini (3 options : setup complet via `install.sh` / mode dégradé web NB Pro / skip visuel)
- **Phase 8 Brand Book** → check SPG-portable (3 options : git clone / Phase 8 dégradée sans Pitch Deck / skip)

*Skip pour le mainteneur : la variable d'environnement `BIG_SKIP_PREFLIGHT=1` saute la Phase 0 — utile en dev pour itérer rapidement sans repasser par la checklist.*
→ Ton input : **"continue"** ou liste des phases à skipper

---

*Note UX : à chaque entrée d'étape importante, tu verras un encadré de cadrage (Quoi / Pourquoi / Tu vas / En sortira) — pas besoin de relire ce guide en cours de route.*

## Les 12 étapes du pipeline

*Les durées indiquées sont des **fourchettes empiriques** calculées sur ~50 sessions historiques. Elles incluent le temps machine ET ton temps de lecture / décision / itération. Une session complète médiane fait ~3-5h tout compris (linéaire) à ~10h (avec beaucoup d'itérations). Les étapes optionnelles peuvent être skippées.*

**1. Collecte du brief** *(~2-5 min)*
Au lancement, un **label de session** est demandé pour isoler les fichiers de cette exécution. Tous les outputs sont regroupés dans `outputs/{brand}-{label}/`. Un fichier `.session-id` est créé dans ce dossier pour vérifier l'identité de la session avant chaque phase. Cela permet de lancer plusieurs sessions en parallèle sur la même marque sans collision de fichiers.

Pour démarrer de zéro, il faut un brief d'entreprise au bon format BIG. Je te propose 4 options selon où tu en es :
  · **A. Tu as déjà un brief au bon format BIG** — donne-moi le fichier ou colle le contenu
  · **B. Tu veux un guide à emporter** — je te fournis un template complet avec explications, tu le remplis à ton rythme et tu reviens
  · **C. Tu préfères qu'on construise ensemble** — on passe les 14 points en mode conversationnel
  · **D. Tu as une brand existante à aspirer** — je capture l'identité depuis ton site web (aspiration de brand)
→ Ton input : **choix A, B, C ou D** + brief si option A, URLs si option D

---

**2. Analyse du brief** *(~7-14 min)*
J'analyse les 14 points du brief (+ Point 15 optionnel : Aversions client — couleurs à éviter en description libre + registres visuels à éviter via Q/R adaptatif), identifie les lacunes, et te pose des questions ciblées si certains points manquent de précision.
→ Tes inputs : **réponses aux questions** si lacunes détectées

---

**3. Scoping — Tension & Curseurs** *(~10-24 min)*
Je définis la Tension de Marque (le paradoxe créatif qui rend ton identité unique), je dérive un diagnostic de température (chaud/froid/neutre) depuis le brief et les aversions client, puis je te demande de calibrer 2 curseurs stratégiques.
→ Tes inputs : **validation de la Tension** + **validation de la température recommandée** + **choix des curseurs A et B** (1 à 3 chacun)

---

**4. Pitch stratégique — 3 concepts** *(~2h45 - 4h — la phase la plus longue)*
C'est l'étape la plus dense du pipeline : elle construit les 3 directions narratives ET leur traduction visuelle complète. Elle se déroule en 4 sous-étapes :

**4a. Territoires créatifs.** J'extrais 15-20 mots-clés de ton brief (selon 4 axes : métier, valeurs, marché, aspirations), je les clusterise en 4-5 territoires. Tu attribues un rôle à chacun (Principal / Secondaire / Tertiaire) — ce mix donne le ton dominant des concepts à venir.

**4b. 3 concepts narratifs.** Tu choisis entre 2 modes :
  · **Génératif** (par défaut) — je génère 3 concepts séquentiellement, chacun voit les précédents et doit diverger
  · **Sélectif par registre** — tu choisis un registre culturel dans le catalogue (28 registres : signalisation maritime, artisanat normand, magazine éditorial 70s…). Je tire un pool de ~210 mots, je dédoublonne et sélectionne 100, je les passe à 10 évaluateurs parallèles. Tu choisis jusqu'à 3 mots qui deviennent les noms-piliers des concepts.

**4c. Direction visuelle.** Pour chaque concept, je dérive 4 éléments — avec un checkpoint utilisateur sur les 3 principaux :
  · **Palette** — je te propose 3 palettes par concept (rendues sur un specimen visuel), tu en choisis 1
  · **Typographies** — je te propose 1 pairing (titre + texte) chargé via Google Fonts et capturé en screenshot pour validation visuelle, tu valides ou demandes un remplacement
  · **Style HTML** — je te présente 4 spécimens stylisés par concept (combinant palette + typo + style), tu en choisis 1
  · **Image-pivot** (pour 1 seul concept) — tu choisis quel concept va recevoir une image de référence générée via Perplexity ; les 2 autres concepts restent en HTML classique

**4d. Pitch écrit.** Je te présente le pitch éditorial complet pour les 3 concepts, ancré sur tous les choix précédents (et sur la description multimodale de l'image-pivot pour le concept concerné). Tu valides ou demandes des ajustements.

Avant de te présenter le pitch final, je vérifie visuellement que les fonts, palettes et styles choisis correspondent bien à l'intention — si un rendu ne colle pas, je corrige avant que tu ne voies le résultat.
→ Tes inputs : **choix du mode (Génératif ou Sélectif)** + (si Sélectif : choix du registre + des finalistes) + **attribution des rôles aux territoires** (Principal/Secondaire/Tertiaire) + **validation des directions narratives** + **choix de palette** (avec alerte aversion si applicable) + **choix de style** (avec alerte aversion si applicable) + **validation du pitch complet**

---

**5. Visuels de référence** *(optionnel — ~30-60 min si activé, dont du temps de génération côté outils externes)*
Si certains concepts recommandent de la photo ou de l'illustration, je te propose de générer des visuels de référence pour enrichir les Style-Tiles. Cette étape s'exécute dans le skill séparé `/visual-prompt` (workflow itératif MidJourney → Nano Banana 2 → Recraft) : je génère les prompts adaptés au registre de chaque concept, tu lances les générations dans ces outils externes et tu rapportes les images, je les analyse pour préparer leur intégration en Phase 6 (Style-Tiles). Deux modes disponibles : **principal** (génération d'un visuel hero) et **variantes** (dérivation atmosphere / closeup / macro / pov depuis un hero existant).
→ Tes inputs : **Oui/Non** + **images** si tu choisis d'en fournir (chemins de fichiers)

---

**6. Style-Tiles — 3 showrooms visuels** *(~60-120 min — variable selon le nombre d'itérations)*
Je génère 3 fichiers HTML immersifs (un par concept) : Voice Block, Artefact Témoin, Atmosphere Block. Chaque fichier s'ouvre dans une fenêtre de navigateur distincte pour comparaison côte à côte.

Chaque style-tile passe par 3 niveaux de contrôle qualité avant de t'être présenté :
  · **Gates structurels** — vérifient automatiquement que palette, typo et layout choisis sont appliqués sans déviation
  · **Gates anti-slop** — détectent et bloquent les clichés AI visuels datés (accent-bars systématiques, hover-translateY générique, glow-shadow gratuit, animations infinies décoratives, emojis dans l'UI, polices "AI-slop" comme Inter par défaut…). Le système re-itère jusqu'à 2 tours de polish pour corriger
  · **Audit "4 critiques"** — 4 sub-agents évaluent chacun le style-tile sous un angle différent (signal sectoriel, fidélité au pitch, modernité, originalité) et proposent des corrections ciblées avant de te livrer

*Note : si des style-tiles existent déjà (itération de concepts), ils sont archivés dans `_archive-st-{N}/` avant régénération. De même, les fichiers de design (pitches, penseurs, specimens, font backups) sont archivés dans `_archive-pass-{N}/` avant chaque relance de Phase 3B.*
→ Automatique (génération) puis **comparaison visuelle**

---

**6bis. Audit DA** *(optionnel — ~7-14 min)*
Avant de te présenter les résultats, je te propose un audit qualité : je capture des screenshots des 3 Style-Tiles et je les compare au pitch pour vérifier que le rendu est fidèle (fonts, palette, atmosphère, artefacts). Si des écarts sont détectés, je te présente les corrections à valider.
→ Tes inputs : **Oui/Non** pour lancer l'audit + **validation des corrections** si écarts détectés

---

**7. Itération & Choix final** *(~10-30 min)*
Tu compares les 3 Style-Tiles, tu demandes des ajustements si besoin, et tu choisis ton concept final.
→ Tes inputs : **ajustements** (optionnel) + **choix du concept** (A, B ou C)

---

**7bis. Animation du style-tile** *(optionnel — ~15-35 min)*
Je te propose d'ajouter une couche d'animation moderne au style-tile retenu (parallaxe au scroll, apparitions des sections quand tu les atteins, typo cinétique à l'arrivée…). C'est calibré pour rester sobre et anti-slop : scroll natif (pas de smooth-scroll « pâteux »), librairies standard. J'analyse ton style-tile, je te propose un **preset adapté** dans un fichier que tu peux ajuster, puis je produis **2-3 variantes de dosage** (subtil / médian / prononcé) que tu compares dans le navigateur. Tu en choisis une et on itère si besoin.
→ Tes inputs : **Oui/Non** + si oui : **ajustement du preset** + **choix de la variante** (+ itérations éventuelles)

---

**8. Logo — Concept & Génération** *(optionnel — ~40-65 min, incluant ~20 min côté MidJourney)*
Je te propose de créer un logo professionnel avec Midjourney. Si tu acceptes : je conçois le concept créatif + 3 prompts MJ, tu génères dans Midjourney, je vectorise en SVG propre et crée 6 déclinaisons (bicolore, négatif, monochromes, lockups).
→ Tes inputs : **Oui/Non** + si oui : **choix du résultat MJ** + **validation des 6 déclinaisons SVG**

---

**9. Enrichissement — Batches 2 & 3** *(~25-50 min — Batch 2 et Batch 3 cumulés)*
Je génère 2 fichiers HTML supplémentaires, visuellement cohérents avec ton choix :
  · **Batch 2 — Signes** : Logotype, Iconographie (refondue D59), UI Components, Data Visualization
  · **Batch 3 — Narration** : Direction Photo, Composition, Illustration
→ Tes inputs : **choix de la famille d'icônes** (validation du choix du routeur Phase 6A-0 ou override sur les 8 options) puis **validation** de chaque batch (ou demande d'ajustements)

---

**10. Documentation Markdown (Phase 7 — Zone 2)** *(~7-16 min)*
Je génère les Design Specs (45 sections en Markdown).
→ Validation user, puis Phase 8 ou directement Packaging selon ta réponse

---

**11. Brand Book éditorial (Phase 8 — optionnel — ~10-15 min)**
Je te demande si tu veux que je génère un brand book HTML éditorial : cover painterly + intro Identity Card bento + 8 sections documentaires (Big Idea, Concept, Identité, Palette, Typographie, Système, Applications avec Web/Pitch Deck/Réseaux Sociaux, Photo & Illustration) + closing.
→ Ta réponse : **(a) Oui — générer** OU **(b) Non — passer direct au Packaging**

---

**12. Packaging final** *(~1-3 min — automatique)*
Je package tous les livrables dans un dossier dédié prêt à être partagé.
→ Automatique — le dossier s'ouvre dans le Finder + déploiement Vercel

---

---

## Mode D — Aspiration de Brand

Si tu choisis l'option **D**, le pipeline est différent : au lieu de créer une identité ex nihilo, je capture celle de ta brand existante depuis son site web.

**D1. Collecte**
Je te demande les URLs de ton site (2-5 pages), ton logo (optionnel), et le nom de la marque. Ensuite je capture automatiquement les screenshots, le HTML et le CSS.
→ Tes inputs : **URLs** + **logo** (optionnel) + **nom de la marque**

---

**D2. Extraction du Brand DNA**
J'analyse le CSS, le HTML, les screenshots et le contenu textuel pour extraire tous les design tokens de ta brand : palette, typo, radius, ombres, espacements, transitions. J'analyse aussi le ton de voix, le style visuel et je propose un positionnement.
→ Automatique (extraction)

---

**D3. Validation**
Je te présente une synthèse de ce que j'ai extrait : palette, typo, style, curseurs estimés. Tu valides, corriges ou ajustes.
→ Tes inputs : **validation/corrections** de la Brand DNA + **curseurs A×B**

---

**D4. Style-Tile**
Je génère un Style-Tile (triptyque Voice + Artefact + Atmosphere) fidèle à 100% aux tokens extraits. Le layout est un showroom créatif, mais les couleurs, typos et dimensions sont exactement les tiennes.
→ Automatique (génération) puis **validation visuelle**

---

**D5. Validation fidélité**
Le style-tile s'ouvre dans ton navigateur. Tu vérifies que tout correspond à ta brand. Si quelque chose ne va pas, on ajuste.
→ Tes inputs : **validation** ou **corrections**

---

**Ensuite → Convergence avec le pipeline créatif**
Les étapes suivantes sont identiques aux options A/B/C :
  · Batch 2 — Signes (Logotype, Iconographie, Data Viz)
  · Batch 3 — Narration (Photo, Composition, Illustration)
  · Documentation & Packaging

---

## Récap — ce qu'il faut préparer

**Option A — Tu as déjà un brief :**
  · 1 fichier brief (.md ou texte) — c'est tout

**Option B — Tu veux un guide à emporter :**
  · Rien maintenant — je te fournis le template, tu reviens quand c'est rempli

**Option C — Mode conversationnel :**
  · Rien à préparer — on construit ensemble, question par question

**Option D — Aspiration de brand :**
  · 2-5 URLs de ton site (homepage obligatoire + pages représentatives)
  · Ton logo en SVG ou PNG (optionnel mais recommandé)
  · Le nom de ta marque

---

*Ferme ce fichier et retourne dans le chat pour commencer !*
