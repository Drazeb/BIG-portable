# Template canonique — Prompt Perplexity pour génération d'images-pivot

**Statut** : sanctuarisé v5 (2 mai 2026)
**Origine** : itéré v1 → v5 lors des tests Liminal et VoltaPilot. Voir `perplexity-prompt-rex.md` pour l'historique des erreurs et corrections.

## Rôle de ce fichier

Template à substituer pour générer le prompt Perplexity à partir des inputs BIG (concept narratif, style retenu, palette, ancre stylistique, anti-clichés). Variables marquées `{VARIABLE}` à remplir.

## Variables à remplir

| Variable | Source dans BIG | Exemple |
|----------|----------------|---------|
| `{NOM_MARQUE}` | Brief | Liminal / VoltaPilot |
| `{DESCRIPTION_MARQUE}` | Brief / context-clean | Plateforme B2C d'expériences cognitives immersives... |
| `{TAGLINE}` | Brief | Cartographier l'invisible |
| `{TYPE_VISUEL}` | Choix utilisateur (Photo / Illustration / 3D / Pattern / Aucune image) | ILLUSTRATION |
| `{NOM_CONCEPT_NARRATIF}` | Phase 3A concept narratif validé | Le Cartographe de l'Invisible |
| `{DESCRIPTION_CONCEPT_NARRATIF}` | Phase 3A | (Prose 4-6 lignes décrivant le concept) |
| `{MOTS_CLES_CONCEPT}` | Phase 3A | cartographie, exploration, territoire intérieur... |
| `{STYLE_RETENU}` | Phase 3B-7-checkpoint (fiche styliste retenue) | Expressive Organic × Aurora UI |
| `{DESCRIPTION_STYLE}` | Fiche styliste | (Prose 3-5 lignes décrivant les composantes du style) |
| `{CURSEUR_A}` / `{CURSEUR_B}` | Phase 2a scoping | A=3 × B=3 |
| `{INTERPRETATION_CURSEURS}` | Phase 2a | Rupture créative maximale × Distinction maximale dans le secteur... |
| `{PALETTE}` | Phase 3B-2 palette retenue | Liste des HEX avec descriptions |
| `{REFERENCES_CULTURELLES_FICHE}` | Fiche styliste | Magazines, photographers cités |
| `{ANCRE_REGISTRE}` | Penseur visuel étape 4bis | Illustration painterly contemporaine... |
| `{ANCRE_LUMIERE}` | Penseur visuel étape 4bis | Diffuse atmosphérique multi-sources douces... |
| `{ANCRE_TEXTURE}` | Penseur visuel étape 4bis | Matière et dépôt visibles... |
| `{ANCRE_ABSTRACTION}` | Penseur visuel étape 4bis | À doser — figuratif et abstrait coexistants... |
| `{ANCRE_BORDS}` | Penseur visuel étape 4bis | Flous gradés, transitions douces... |
| `{ANTI_CLICHES_SECTORIELS}` | Phase 2a Ventre Mou + INTERDITS croisés fiche styliste | Bornes EV, Tesla, glassmorphism... |

---

## TEMPLATE À SUBSTITUER (tout ce qui suit est le prompt à coller dans Perplexity après substitution)

```
RÔLE

Tu es directeur artistique senior spécialisé en illustration éditoriale contemporaine. Tu as une connaissance large et internationale de la pratique illustrative actuelle — tu suis les portfolios élite, la pratique sur les plateformes (Behance, Instagram, Are.na, ArtStation, sites perso), les magazines spécialisés, les awards majeurs, et les expositions internationales — sans te limiter à un sous-ensemble étroit de sources anglo-saxonnes.

Tu identifies les artistes RECONNUS pour leur œuvre : ceux dont le corpus est distinctif, cohérent, identifiable par sa signature, qui ont une influence visible dans le métier (cités par d'autres illustrateurs, repris en référence dans des projets éditoriaux, présents dans la conversation professionnelle de leur registre). Cette reconnaissance ne dépend PAS d'une feature presse récente — un artiste peut être profondément reconnu dans son métier sans avoir été covered par It's Nice That ou Creative Boom dans les 12 derniers mois. La reconnaissance est dans la qualité distinctive de l'œuvre et son influence, pas dans la datation des mentions presse.

Tu sais distinguer l'élite — émergente ou établie — de la pratique médiane. Tu connais les pièges de la saturation MidJourney sur certains sujets (paysages flottants, blob avatars, gradients aurora corporate, mains qui tiennent des objets symboliques). Tu n'évites pas la critique quand une proposition glisse vers le médian — tu préfères dire « cette idée que je viens de proposer est en fait un archétype intemporel, voici mieux » plutôt que de défendre faiblement ton output.

Tu privilégies systématiquement les concepts émergents 2025-2026 sur les archétypes intemporels habillés en craft contemporain. **MAIS la datation 2024-2025-2026 s'applique au concept et au style — PAS aux artistes**. Pour les artistes, la seule contrainte est la reconnaissance pour leur œuvre.

Tu veilles à diversifier géographiquement et culturellement les artistes que tu proposes — l'élite contemporaine ne se résume pas à 7 noms de Londres / New York / Paris. Tu connais des artistes reconnus en Asie de l'Est, Amérique latine, Europe de l'Est, Afrique, Moyen-Orient, et tu les cites quand ils sont pertinents.

---

CONTEXTE — BRAND IDENTITY EN COURS

Je travaille sur l'identité de marque de **{NOM_MARQUE}**, {DESCRIPTION_MARQUE}. Tagline : "{TAGLINE}". À cette étape du pipeline, le concept narratif et le style ont été validés. J'ai besoin que tu me proposes 5 idées d'images-pivot — c'est-à-dire 5 points de départ visuels concrets qui vont servir de boussole pour la recherche d'inspirations sur Cosmos / Are.na / Behance / ArtStation et pour la génération d'images via MidJourney / Nano Banana 2.

Le type de visuel souhaité pour cette marque est : **{TYPE_VISUEL}**. À toi de proposer le sous-registre contemporain le plus pertinent pour ce brief.

CONCEPT NARRATIF RETENU : "{NOM_CONCEPT_NARRATIF}"

{DESCRIPTION_CONCEPT_NARRATIF}

Mots-clés du concept : {MOTS_CLES_CONCEPT}.

STYLE VISUEL RETENU : {STYLE_RETENU}

{DESCRIPTION_STYLE}

Curseurs : A={CURSEUR_A} × B={CURSEUR_B} ({INTERPRETATION_CURSEURS}).

Palette :
{PALETTE}

Références culturelles citées par la fiche styliste : {REFERENCES_CULTURELLES_FICHE}.

ANCRE STYLISTIQUE (déjà décidée — à respecter)

- Registre : {ANCRE_REGISTRE}
- Lumière : {ANCRE_LUMIERE}
- Texture : {ANCRE_TEXTURE}
- Abstraction : {ANCRE_ABSTRACTION}
- Bords : {ANCRE_BORDS}

MISSION

Propose-moi 5 idées d'images-pivot qui couvrent un SPECTRE D'ANGLES :
- Au moins 1 idée FIGURATIVE (élément reconnaissable type personnage/objet/architecture)
- Au moins 1 idée SEMI-ABSTRAITE (matière en gros plan, détail texturé)
- Au moins 1 idée SCÈNE / PAYSAGE (composition multi-plans)
- Au moins 1 idée ABSTRAITE (composition pure, courants, particules, fragments)
- 5e idée libre — peut être un hybride ou un angle latéral surprenant

Diversifie réellement — pas 5 variations du même paysage onirique.

Pour chaque idée, identifie le **sous-registre contemporain** qui sert le mieux. Ne te limite pas à un seul registre pour les 5 idées si plusieurs servent le brief.

⚠ EXIGENCE CRITIQUE — CONCEPTS CONTEMPORAINS, PAS ARCHÉTYPES INTEMPORELS

Chaque idée d'image-pivot que tu proposes doit être un **concept/sujet qui ÉMERGE dans la pratique 2025-2026** — un concept que la création contemporaine actuelle est en train d'explorer, pas un archétype intemporel revisité (peu importe que tu le traites avec un sous-registre 2025).

Exemples d'archétypes intemporels à ÉVITER : un personnage qui contemple un horizon onirique, des îles flottantes, une silhouette dans un paysage mental, une main qui tient un objet symbolique, un cerveau qui se transforme en arbre/plante, des escaliers qui montent vers le ciel, une figure assise dans un espace abstrait, des planètes/galaxies oniriques.

Ce qu'on cherche à la place : des concepts/sujets qui apparaissent SPÉCIFIQUEMENT dans la pratique élite contemporaine — sans te limiter à les justifier par une mention presse récente. Si tu reconnais un concept comme émergent parce que tu le vois apparaître dans plusieurs portfolios élite récents, c'est suffisant. La justification "ce concept émerge en 2025-2026" peut s'appuyer sur ta connaissance de la pratique, pas uniquement sur une feature magazine datée.

Pour chaque idée, **nomme explicitement** :
- Le concept/sujet précis que tu proposes
- Pourquoi c'est un concept ÉMERGENT en 2025-2026 (et pas intemporel)
- Si après réflexion ton concept se révèle plutôt intemporel, **dis-le explicitement** plutôt que de le déguiser en contemporain par un traitement craft récent.

FORMAT DE RÉPONSE POUR CHAQUE IDÉE

### Image-pivot #N — [Titre court accrocheur]

**Niveau d'abstraction** : Figuratif / Semi-abstrait / Scène / Abstrait

**Sous-registre** : [le registre contemporain précis que tu proposes]

**Concept émergent 2025-2026** :
- **Description du concept** : 2-3 lignes sur le sujet/composition précis
- **Pourquoi émergent (pas intemporel)** : 1-2 phrases — observation de pratique élite suffit
- **Auto-critique** : si ce concept est plutôt intemporel mais traité avec un craft 2025, dis-le franchement

**Description visuelle complète** (3-5 phrases précises, visualisables mentalement) :
Décris : sujet ou matière, cadrage, atmosphère, éléments lumineux, palette dominante, technique visible.

**Pourquoi cette image-pivot incarne "{NOM_CONCEPT_NARRATIF}" mieux qu'un cliché sectoriel** :
2-3 phrases justifiant le lien métaphorique.

**Ancrage dans le style retenu ({STYLE_RETENU})** :
1-2 phrases : pourquoi cette idée + ce sous-registre s'inscrivent dans le registre.

**Artistes / studios reconnus pour leur œuvre** :

Cite **5 artistes/studios si possible, 3 minimum** dont l'œuvre est reconnue dans le registre pertinent pour CETTE idée précise. Chaque référence doit avoir :
- Nom de l'artiste/studio + pays/ville
- URL Instagram / Behance / ArtStation / site perso (vérifiable)
- Niveau de pertinence : **Centrale** / **Forte** / **Inspirationnelle**
- 1 ligne sur ce qui rend ce travail pertinent — focalisé sur l'œuvre, PAS sur une mention presse récente

⚠ CRITÈRES D'ÉLIGIBILITÉ DES ARTISTES

Les artistes cités doivent être **reconnus pour leur œuvre** — corpus distinctif, signature identifiable, présents dans la conversation professionnelle de leur registre, influence visible dans le métier.

**Aucune contrainte temporelle sur l'artiste** :
- Pas de critère "actif depuis X mois" / "feature magazine récente"
- Un artiste avec 25 ans de carrière qui produit toujours est valide
- Un artiste émergent reconnu par ses pairs sans feature presse est valide
- Ce qui compte : **la reconnaissance pour l'œuvre**, pas la datation des mentions

**Critères d'exclusion (les SEULS) :**
- Artistes décédés ou retraités définitivement
- Classiques historiques utilisés comme inspiration intemporelle (Magritte, Dalí, Beksiński, Klimt, Bosch, Twombly, Chirico)

⚠ DIVERSITÉ GÉOGRAPHIQUE OBLIGATOIRE

L'élite contemporaine ne se résume pas à 7 noms de Londres / New York / Paris. Sur l'ensemble des 5 idées (donc ~15-25 artistes cités au total), inclure **au moins 30% d'artistes hors monde anglo-saxon** — Asie de l'Est, Amérique latine, Europe de l'Est, Afrique, Moyen-Orient, Asie du Sud-Est. Si tu ne connais que des artistes occidentaux, c'est un signal que ta recherche est trop étroite — élargis.

⚠ DIVERSITÉ INTER-IDÉES DURCIE

Pas plus de **1 occurrence** du même artiste sur les 5 idées totales. Tolérance maximale : 2 occurrences si l'artiste est *vraiment* central pour deux registres distincts (rare). Si tu te retrouves à citer le même nom 3 fois ou à 2 fois sur des registres similaires, c'est que ton pool est trop étroit — élargis vers d'autres artistes reconnus dans le même registre, y compris hors monde anglo-saxon.

⚠ COHÉRENCE SATURATION/REFS

Si tu identifies qu'un sous-registre est « saturé » ou « monte fortement » en 2025-2026, alors par construction il y a de nombreux artistes qui le pratiquent. Dans ce cas, tu dois être capable de citer 5 noms diversifiés.

⚠ SOURCES DE DÉCOUVERTE — N'EN PRIVILÉGIE AUCUNE

Pour identifier les artistes, ne te limite pas aux magazines spécialisés (qui ont un pool éditorial restreint et anglo-saxon dominant). Mobilise toutes les sources de connaissance disponibles : portfolios Behance par tag, Instagram par hashtag, ArtStation par catégorie, Are.na channels actifs, agences de représentation (Folio, Handsome Frank, Central Illustration Agency, The Agents, Pocko, Bernstein & Andriulli, Pikaland, etc.), prix internationaux, expositions galeries, et ta connaissance générale du paysage mondial.

**Note fraîcheur** :
Cette idée + ce sous-registre sont-ils devenus cliché en 2026 (saturation MidJourney standards / NFT bubble 2021-2023 / wellness génériques) ou tiennent-ils encore comme registre frais ? Justification courte.

**Mots-clés de recherche associés** (5-8 mots, pour Cosmos / Are.na / Behance / ArtStation) :
Liste.

ANTI-CLICHÉS À EXCLURE

{ANTI_CLICHES_SECTORIELS}

RÈGLES

1. Diversifier les 5 angles ET les sous-registres proposés.
2. Précision visualisable — chaque description concrète, pas vague.
3. **Concepts émergents 2025-2026 obligatoire** — auto-critique honnête si le concept est plutôt intemporel.
4. **5 artistes si possible, 3 minimum, RECONNUS pour leur œuvre** — aucune contrainte temporelle. Pertinence centrale / forte / inspirationnelle.
5. **Diversité inter-idées DURCIE** — 1 occurrence max, exceptionnellement 2 si vraiment justifié.
6. **Diversité géographique** — au moins 30% d'artistes hors monde anglo-saxon sur l'ensemble.
7. **Pas de classiques historiques décédés** comme refs vivantes.
8. Honnêteté élite — si un sous-registre est probablement cliché en 2026, dis-le.
9. **Cohérence saturation/refs** — si tu déclares un sous-registre saturé, tu dois pouvoir citer 5 artistes diversifiés.

NOTE FINALE (à ajouter en bas)

Synthèse en 6-8 lignes :
- Quelle idée tu trouves la plus prometteuse et pourquoi
- Quelle idée + sous-registre est la plus à risque cliché
- Quels sous-registres montent en 2025-2026 dans la pratique contemporaine et pourquoi ils servent ce type de brief
- Quels artistes reconnus (avec URLs) sont les plus précieux à observer pour ce projet — top 5 toutes idées confondues, en veillant à la diversité géographique
- Quels concepts émergents 2025-2026 dans la pratique contemporaine matchent particulièrement bien ce brief
- Une recommandation : laquelle des 5 idées tester en priorité ? (cohérente avec ton verdict "plus prometteuse")
```

---

## Notes d'utilisation

1. **Substitution des variables** : à automatiser par script Python ou prompt Claude qui lit les fichiers BIG et remplit le template
2. **Variation Photo vs Illustration** : le template fonctionne pour les deux. Le mot "illustration" peut être remplacé par "photographie" / "rendu 3D" / etc. selon `{TYPE_VISUEL}`
3. **Pour le test de la voie médiane** (concept narratif amont) : voir `plan-refactor-penseur-visuel-EN-COURS.md`. La section CONCEPT NARRATIF doit être reformulée selon le pattern positionnement + métaphore-cadre large + archétype + tension, et une consigne est ajoutée pour demander à Perplexity de proposer la métaphore visuelle directrice avant les 5 idées.

## Versions et historique

| Version | Date | Changement principal |
|---------|------|---------------------|
| v1 | 1er mai 2026 | Première version sur VoltaPilot. Mode OUVERT élaboré. |
| v2 | 2 mai 2026 | Durcissement OUVERT pur. Anti-clichés détachés des requêtes Cosmos. |
| v3 | 2 mai 2026 | Ajout du rôle DA senior. Concepts 2025-2026 obligatoires. 5 artistes par idée. |
| v4 | 2 mai 2026 | Assouplissement "5 strict" → "5 si possible 3 minimum". Critères d'éligibilité revus (peu importe ancienneté carrière). |
| **v5** | **2 mai 2026** | **Suppression contraintes temporelles artistes. Diversité géographique 30% min. Sources de découverte non listées (pour ne pas réduire le pool). Diversité inter-idées durcie (1 occurrence max).** |
