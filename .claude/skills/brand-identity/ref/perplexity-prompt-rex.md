# REX — Prompt Perplexity pour images-pivot

**Statut** : sanctuarisé après itération v1 → v5 (2 mai 2026)
**Lien** : `perplexity-prompt-template.md` (template canonique sanctuarisé)

## Genèse

Pendant les sessions du 30 avril → 2 mai 2026, on a construit puis itéré un prompt Perplexity destiné à remplacer la prescription d'images concrètes que faisait le penseur visuel BIG (Phase 3B-7c, étape 5 actuelle). Constat empirique fondateur : Claude seul (= LLM sans accès web) produit des images-pivot **médianes / cliché** parce que son training textuel converge vers les associations les plus fréquentes. Perplexity, grâce à son accès web temps réel, peut citer des artistes contemporains nommés et proposer des concepts émergents — à condition que le prompt soit bien construit.

Cinq versions ont été nécessaires pour stabiliser le prompt. Ce REX documente les pièges identifiés à NE PLUS REPRODUIRE.

## Itération v1 → v5

### v1 — Mode OUVERT élaboré (cas VoltaPilot)

**Approche** : laisser Perplexity proposer les sujets librement à partir d'un brief enrichi (concept narratif + style retenu + ancre stylistique + curseurs). Distinction OUVERT (sujet émerge) vs FERMÉ (sujet imposé).

**Problème observé** : slippage du sujet — en mode OUVERT, Perplexity injectait quand même des sujets concrets dans les requêtes Cosmos ("hand stethoscope", "open book") au lieu de rester sur le champ métaphorique abstrait. Tractabilité humaine du tri Cosmos = **médiocre** (Charles l'a senti immédiatement : "j'obtiens des photos d'appartements dans la pénombre, mais je ne sais pas quoi choisir").

**Conclusion** : le mode OUVERT pur n'est pas tractable cognitivement pour l'humain — il faut un point de départ visuel concret. C'est ce qui a fait basculer toute la démarche vers la notion d'**image-pivot**.

### v2 — Durcissement OUVERT (test, abandonné)

**Approche** : durcir l'interdiction d'injecter du sujet concret dans les requêtes Cosmos en mode OUVERT.

**Problème** : marche en lettre, mais devient inutilisable en pratique — l'humain n'a pas d'étalon de tri.

**Conclusion** : abandonné comme stratégie principale. Le mode OUVERT pur est une impasse pratique, on bascule sur l'idée que l'image-pivot est nécessaire en amont.

### v3 — Ajout du rôle DA senior + concepts 2025-2026 (cas Liminal)

**Changements** :
- Ajout d'un bloc **RÔLE** en tête (DA senior, sources nommées, posture critique)
- Ajout d'une **exigence concepts émergents 2025-2026** (pas archétypes intemporels)
- Passage à **5 artistes par idée** (vs 1-3)
- **Diversité inter-idées max 2 occurrences**

**Effet** : le rôle a cassé l'autoroute statistique main+objet. Concepts plus distinctifs (Anatomie du conducteur, Cavité thoracique pour VoltaPilot ; corps-méridien, strate primaire, delta d'écriture pour Liminal). Mais persistance de patterns figuratifs proches du slop (main+instrument).

**Problème observé** : Perplexity n'arrive pas à citer 5 artistes pertinents par idée — déclare "honnêtement non comblé" alors qu'il déclare en parallèle que le sous-registre est saturé. **Contradiction logique**.

### v4 — Assouplissement "5 strict" + critères d'éligibilité revus

**Changements** :
- Assouplissement : "5 si possible, 3 minimum" (au lieu de 5 strict)
- Critères d'éligibilité revus : "actifs aujourd'hui (portfolio mis à jour ces 18 derniers mois), peu importe quand la carrière a commencé"
- Niveaux de pertinence (centrale / forte / inspirationnelle)
- Bloc "Non-contradiction saturation/refs"

**Effet** : la calibration honnête fonctionne (Perplexity admet quand il n'a que 3 ou 4 refs). Mais nouveau problème observé : **répétition d'artistes** entre les idées. Sur Liminal v4, 3 artistes (Markos Kay, Nadiia Pliamko, Chris Hoffmann) apparaissent ensemble sur Image 2 ET Image 4, alors que ce sont deux registres distincts.

**Diagnostic** : Perplexity restait contraint par les **sources** qu'il consulte. Il privilégiait les artistes ayant une mention presse récente (Creative Boom, It's Nice That, Creative Bloq, Pocko) — un pool éditorial étroit. Auto-censure sur les artistes établis depuis longtemps qui n'ont pas eu de feature récente.

### v5 — Suppression contraintes temporelles artistes + diversité géographique forcée + sources de découverte non listées (VERSION SANCTUARISÉE)

**Changements** :
- **Suppression de la contrainte d'activité ≤18 mois** sur les artistes
- Reformulation : "artistes RECONNUS pour leur œuvre — corpus distinctif, signature identifiable, influence dans le métier" — pas de contrainte temporelle
- **Suppression des listes de magazines/awards** dans le rôle (qui réduisaient le pool de découvrabilité)
- **Bloc "Sources de découverte — n'en privilégie aucune"** : élargissement explicite (Behance par tag, Instagram par hashtag, agences de représentation, etc.)
- **Diversité géographique 30% minimum** hors monde anglo-saxon
- **Diversité inter-idées durcie** : 1 occurrence max (vs 2 max au v4)

**Résultat** :
- ~70% d'artistes hors monde anglo-saxon (au lieu de ~95% UK/US/Europe occidentale au v4)
- ~24 noms uniques sur 25 emplacements (au lieu de ~16 au v4)
- Justifications portent sur l'œuvre, pas sur les mentions presse
- Concepts plus distinctifs et plus singuliers (notation isobarique, section drawing organique, surréalisme opérationnel)

## Pièges à NE PLUS REPRODUIRE

| Piège | Raison | Symptôme | Correction sanctuarisée |
|-------|--------|----------|-------------------------|
| **Lister les magazines/awards comme sources prioritaires** | Réduit le pool de découvrabilité au pipeline éditorial anglo-saxon | Les mêmes 7-10 artistes reviennent en boucle | Bloc "Sources de découverte — n'en privilégie aucune" + diversité géographique |
| **Imposer une contrainte temporelle sur l'activité de l'artiste** | Auto-censure sur les artistes établis depuis longtemps qui pratiquent toujours | Perplexity dit "non comblé" alors que le sous-registre est saturé | Critère = reconnaissance pour l'œuvre, peu importe la date |
| **Blacklister des archétypes intemporels (main+objet, paysage flottant, etc.)** | Liste infinie, pas la bonne approche structurelle | Charles l'a explicitement refusée — risque d'"enfer infini" | Garde-fou par rôle + exigence concepts émergents + auto-critique honnête |
| **Imposer "EXACTEMENT 5" artistes sans souplesse** | Force l'auto-censure ou le comblement par artistes hors-sujet | Réfs périphériques ajoutées artificiellement OU "non comblé" sec | "5 si possible, 3 minimum" + niveaux de pertinence + calibration honnête |
| **Demander des "preuves" datées pour chaque idée et chaque artiste** | Force Perplexity à citer des mentions presse, biaise vers les artistes covered | Justifications saturées de "cité par X en 2025" | Justification ancrée dans l'œuvre suffit, pas besoin de mention presse |
| **Mode OUVERT pur (sans sujet concret)** | Pas tractable cognitivement pour le tri humain Cosmos | Charles : "je ne sais pas quoi choisir" | Image-pivot concrète indispensable comme étalon de tri |

## Comment évaluer un rapport Perplexity (grille d'audit)

À chaque rapport généré, vérifier :

| Critère | Comment le mesurer | Seuil acceptable |
|---------|--------------------|--------|
| **Diversité géographique** | Compter les pays/régions des artistes cités | ≥30% hors monde anglo-saxon |
| **Diversité noms artistes** | Compter les noms uniques sur l'ensemble | ≥80% des emplacements ont un nom unique (~20+ noms uniques sur 25 emplacements) |
| **Justifications artistes** | Lire les justifications | Centrées sur l'œuvre, pas sur les mentions presse |
| **Concepts émergents** | Vérifier l'auto-critique sur chaque idée | Honnête — déclare quand un concept est plutôt intemporel |
| **Cohérence saturation/refs** | Si un sous-registre est dit "saturé", il y a 5 refs ? | Oui sinon contradiction logique |
| **Cohérence verdict/recommandation** | L'idée recommandée est-elle l'idée déclarée "plus prometteuse" ? | Doit coïncider |
| **Diversité des sous-registres** | Les 5 idées ont-elles des sous-registres distincts ? | ≥4 sous-registres distincts sur 5 idées |
| **Présence d'auto-critique honnête** | Idées à risque cliché signalées ? | Au moins 1 sur 5 explicitement signalée |

## À surveiller dans les prochaines sessions

- **Reproductibilité** : si on relance le même prompt 3 fois, les 5 idées sont-elles différentes ou Perplexity converge-t-il ? Pas testé sur le v5.
- **Adaptation aux médiums autres qu'illustration et photo** : le template n'a été testé que sur photo (VoltaPilot) et illustration (Liminal). Pour 3D, pattern, mixed-media, vérifier que le prompt tient.
- **Voie médiane sur le concept narratif** (test à faire — voir `plan-refactor-penseur-visuel-EN-COURS.md`) : Claude prescrit positionnement + métaphore-cadre large SANS métaphore visuelle directrice, Perplexity propose la métaphore visuelle. À comparer au v5 actuel pour évaluer si la métaphore Perplexity est plus fertile que celle de Claude.

## Dernière mise à jour : 2 mai 2026
