# REX — Curseur B, Ventre Mou et Anti-territoire (audit avril 2026)

Rapport d'audit exhaustif sur le fonctionnement réel du curseur B, du Ventre Mou et de l'anti-territoire dans le pipeline BIG. Destiné à être lu par une session vierge qui prend le relais.

---

## CONTEXTE — Pourquoi cet audit

### Le système BIG utilise 2 curseurs

Le pipeline Brand Identity Generator (BIG) produit des identités de marque en 7 phases. L'utilisateur choisit 2 curseurs en Phase 2 :

- **Curseur A (Audace de composition)** : contrôle la forme — comment les éléments sont disposés, proportionnés, animés. Valeurs 1 (Prudent), 2 (Décalé), 3 (Rupture).
- **Curseur B (Différenciation concurrentielle / ZAG)** : contrôle le positionnement — à quel point la marque s'éloigne des codes visuels de son secteur. Valeurs 1 (Mimétisme), 2 (Distinction), 3 (Contre-pied total).

Les deux sont indépendants : A=3 B=1 (composition radicale dans les codes du secteur) est une combinaison valide.

### Le problème identifié

Un audit complet du pipeline a révélé que le curseur A est bien instrumenté (~80% opérationnel : pools de fonts, type-scale, exemples, checklists, gates). Le curseur B est quasi-inerte (~5% opérationnel). L'audit a aussi révélé que le Ventre Mou (l'inventaire sectoriel) fonctionne bien, mais que l'anti-territoire (le filtre conceptuel dérivé du Ventre Mou + curseur B) est un output mort.

### Ce qui a été fait dans cette session (vague 1)

Un nettoyage des prescriptions dirigistes du curseur A a été commité (`79d8da3`) : toutes les prescriptions qui liaient une technique CSS à un niveau de curseur A ont été remplacées par des sensations. Le gate mécanique a été unifié. Ce nettoyage est FAIT et ne concerne pas ce rapport.

Ce rapport concerne le **chantier suivant** : que faire du curseur B et de l'anti-territoire ?

---

## PARTIE 1 — Le curseur B dans le pipeline : audit exhaustif

### Définition officielle (bible-design-strategie.md)

| B | Label | Palette | Imagerie | Ton |
|---|-------|---------|----------|-----|
| 1 | Mimétisme | Codes couleur attendus du secteur, palette "safe" | Imagerie conventionnelle du marché, stock prévisible | Vocabulaire corporate, réassurance maximale |
| 2 | Distinction | Pivot chromatique sur 1 couleur inattendue, reste cohérent avec le secteur | Mix d'imagerie sectorielle + DA originale | Voix distinctive sur 1 axe (humour, poésie, franchise) |
| 3 | ZAG (Contre-pied) | Palette en opposition radicale aux leaders | DA en rupture totale (illustration là où tous font de la photo) | Voix radicalement différente |

Le principe : "Identification de la tendance dominante du marché pour proposer un contre-pied proportionnel au score du Curseur B." Le test diagnostique : "Un concurrent pourrait-il utiliser ce design ? Si oui → B doit monter d'au moins 1 point."

### Parcours de B phase par phase

#### Phase 2 — Scoping : B est COLLECTÉ

L'utilisateur voit la description des 3 niveaux et choisit une valeur. Elle est stockée dans `{cursor_b}`. Le Ventre Mou sectoriel est produit dans cette même phase — c'est le matériau sur lequel B est censé agir. Mais le scoping produit le Ventre Mou indépendamment de B (le même Ventre Mou pour B=1 et B=3).

**Fichier** : `SKILL.md` lignes 596-607.

#### Phase 3A — Concepts narratifs : B est TRANSMIS mais INERTE

B apparaît 5 fois dans `phase-3a-concepts.md`, toutes en mode label :
- `A={cursor_a} × B={cursor_b}` (contexte, ligne 26)
- "Génère 1 concept calibré sur A×B" (instruction, ligne 40)
- Le heading du concept porte `Calibrage A=X × B=Y` (ligne 51)
- "consulte persona-and-rules.md et bible-design-strategie.md pour comprendre ce que ces valeurs impliquent" (ligne 88)

Aucune instruction conditionnelle du type "si B=3, pousse le ZAG plus fort". La section "Position ZAG" (ligne 83) mentionne le Ventre Mou mais n'est pas calibrée sur la valeur de B.

Les fichiers annexes de Phase 3A (`phase-3a-explore.md`, `phase-3a-evaluate.md`, `phase-3a-decontamination.md`) ne mentionnent AUCUNE occurrence de B, ZAG, différenciation ou Ventre Mou.

**Verdict** : B est passif. Le subagent reçoit la valeur mais rien ne l'oblige à agir différemment selon B=1 ou B=3.

#### Phase 3B — Design dérivé : B a UN SEUL point d'action, implicite

B apparaît 4 fois dans `phase-3b-design.md`. 3 en mode label (`A={cursor_a} × B={cursor_b}`) et **1 seul point semi-actionné** :

> **Ligne 156** — Carte d'Inspiration, section Anti-territoire :
> "Ce dont le concept s'éloigne EXPLICITEMENT. **Déduis-le du Ventre Mou (Phase 2) et du curseur B.** Nomme les clusters esthétiques et/ou secteurs visuels que les choix ÉVITENT."

C'est la **seule ligne de tout le pipeline** où B est invoqué comme source d'une décision. Mais le mécanisme est implicite : le subagent doit "déduire" sans règle concrète (B=1 → quoi ? B=3 → quoi ?).

Les autres subagents de Phase 3B :
- **Routeur chromatique** (`phase-3b-gamut-router.md`) : zéro occurrence de B. Les gammes viennent des territoires.
- **Penseur typographique** (`phase-3b-penseur.md`) : B en label uniquement. Pool indexé sur A.
- **Palette** (`phase-3b-palette.md`) : B en label uniquement.
- **Penseur visuel** (`phase-3b-penseur-visuel.md`) : B en label uniquement.

**Verdict** : micro-influence via l'anti-territoire (1 ligne), sans vérification ni calibrage.

#### Phase 4 — Style-tile : B est COSMÉTIQUE

B apparaît 1 fois dans `phase-4-styletile.md` (ligne 40 : label). Tout le calibrage est indexé sur A.

Le gate "Cursor Coherence" (ligne 370) dit vérifier A×B mais **ne vérifie que A** : "Si A=2, vérifier qu'il y a au moins une asymétrie..." Aucune vérification de B.

Même constat pour `phase-4-artefact.md` (1 label, zéro logique B) et `phase-4bis-da-check.md` (zéro occurrence).

**Verdict** : B est cosmétique en Phase 4.

#### Orchestrateur (SKILL.md) : B est TRANSPORTÉ partout, ACTIONNÉ nulle part

~25 occurrences dans le SKILL.md, réparties :

| Type d'usage | Nb | Effet réel |
|---|---|---|
| TRANSMISSION (`{cursor_b}` passé au subagent) | ~10 | Variable transportée sans exploitation |
| LABEL (affiché "A×B") | ~8 | Cosmétique |
| DESCRIPTION (définition présentée à l'utilisateur) | ~3 | Collecte |
| LOGIQUE CONDITIONNELLE sur B | **0** | Rien |

Pour comparaison, le curseur A a des logiques conditionnelles sur : le choix du fichier exemple (ligne 2365), le pool de fonts (ligne 1125), le type-scale ratio, le seuil du gate (ligne 2493), le répertoire standard/rupture (ligne 330).

### Tableau récapitulatif B

| Phase | B est... | Effet réel |
|---|---|---|
| Phase 2 (Scoping) | Collecté | L'utilisateur choisit. Le Ventre Mou est produit indépendamment de B. |
| Phase 3A (Concepts) | Transmis + label | Aucune instruction conditionnelle. |
| Phase 3B (Design) | **1 micro-action** | L'anti-territoire est "déduit du curseur B". Implicite, non vérifié. |
| Phase 3B (Palette) | Label | Le routeur chromatique ignore B. |
| Phase 3B (Typo) | Label | Pool indexé sur A uniquement. |
| Phase 4 (Style-tile) | Cosmétique | Zéro logique conditionnelle. |
| Phase 4 (Gate) | Absent | Le gate "Cursor Coherence" ne vérifie que A. |
| Batches 2-3 | Label | Transmis mais non actionné. |

### Conclusion B

B est un placebo à ~95%. Son seul point d'influence (ligne 156 de phase-3b-design.md) est implicite, non calibré, et non vérifié. Si on passait B de 1 à 3 sans changer A, le pipeline produirait des pitchs potentiellement différents (si le DA le prend en compte) mais aucun mécanisme ne garantit que le HTML final traduit ce changement.

---

## PARTIE 2 — Le Ventre Mou : audit exhaustif

### Qu'est-ce que c'est

Le Ventre Mou est un inventaire sectoriel produit en Phase 2 (scoping). Il répond à : "que font TOUS les concurrents de ce secteur ?". Il existe en 2 variantes :

**Ventre Mou Visuel** (codes design des concurrents) — exemple pour un composteur urbain :
- Vert dominant monotone (vert forêt ou vert sauge omniprésent)
- Typo ronde/amicale type Nunito, Poppins
- Imagerie "mains dans la terre" en stock photo
- Illustration flat style "corporate green"
- Pictogrammes de feuilles, de recyclage, de planète

**Ventre Mou Narratif** (clichés de communication) — même brief :
- Discours culpabilisant ("sauvez la planète")
- Vocabulaire militant-associatif ("engagez-vous", "ensemble")
- Ton pédagogique condescendant ("le saviez-vous ?")
- Promesse floue sur l'impact ("chaque geste compte")

### Circuit de transmission mécanique

Le Ventre Mou a un circuit complet et fonctionnel :

```
Phase 2A (scoping) produit le Ventre Mou dans {brand}-scoping.md
        │
        ▼
Orchestrateur extrait la section "Les constantes transverses (le vrai Ventre Mou)"
        │
        ├──► Phase 3A : {ventre_mou} narratif décontaminé
        │    → section "VENTRE MOU SECTORIEL (ce contre quoi zagguer)"
        │    → instruction : positionner le concept par rapport au Ventre Mou
        │    → VERDICT : ACTIONNÉ (directionnel, pas binaire)
        │
        ├──► Phase 3B design : lecture directe du scoping
        │    → instruction : "Pour chaque choix design, VÉRIFIE qu'il ne tombe pas
        │      dans un code identifié comme Ventre Mou. Si c'est le cas → trouve
        │      une alternative."
        │    → VERDICT : ACTIONNÉ (filtre binaire sur CHAQUE choix)
        │
        ├──► Phase 3B palette : lecture directe du scoping
        │    → instruction : "VÉRIFIE que tes choix de palette ne tombent pas dans
        │      un code identifié comme Ventre Mou."
        │    → VERDICT : ACTIONNÉ (filtre binaire)
        │
        ├──► Phase 3B penseur visuel : {ventre_mou_visuel}
        │    → section dédiée "VENTRE MOU SECTORIEL (visuels à éviter)"
        │    → VERDICT : ACTIONNÉ (évitement)
        │
        ├──► Phase 3B routeur chromatique : ABSENT
        │    → VERDICT : TROU (rattrapé par la palette en aval)
        │
        ├──► Phase 4 style-tile : {ventre_mou}
        │    → section "## VENTRE MOU SECTORIEL — ÉLÉMENTS INTERDITS"
        │    → "Ces codes visuels sont le Ventre Mou du secteur. NE PAS les
        │      reproduire, même inconsciemment :"
        │    → VERDICT : ACTIONNÉ (filtre binaire "INTERDITS")
        │
        └──► Phase 4 artefact : {ventre_mou}
             → même section "ÉLÉMENTS INTERDITS"
             → VERDICT : ACTIONNÉ (filtre binaire "INTERDITS")
```

### Point technique important

La variable `{ventre_mou}` porte **deux contenus différents** selon la phase :
- En Phase 3A : ventre mou **narratif** décontaminé (clichés de communication, sans noms de marque ni termes sectoriels)
- En Phase 4 : constantes **visuelles** (éléments design interdits — couleurs, typos, imagerie)

Même nom de variable, contenu différent. Fragile mais pas cassé.

### Conclusion Ventre Mou

Le Ventre Mou **fonctionne bien**. Il est injecté mécaniquement à chaque phase pertinente, avec une formulation binaire claire ("INTERDITS", "NE PAS reproduire"). Il est identique pour les 3 concepts et ne dépend pas de B.

---

## PARTIE 3 — L'anti-territoire : audit exhaustif

### Qu'est-ce que c'est

L'anti-territoire est un output du DA Phase 3B, produit dans la Carte d'Inspiration (section c). C'est la réponse à : "de quel UNIVERS ESTHÉTIQUE ce concept s'éloigne-t-il ?".

**Définition dans `phase-3b-design.md` ligne 156** :
> "Anti-territoire : Ce dont le concept s'éloigne EXPLICITEMENT. Déduis-le du Ventre Mou (Phase 2) et du curseur B. Nomme les clusters esthétiques et/ou secteurs visuels que les choix ÉVITENT (ex: 'On s'éloigne du corporate utilities et du militant associatif lo-fi')."

### Différence avec le Ventre Mou

| | Ventre Mou | Anti-territoire |
|---|---|---|
| **Granularité** | Éléments concrets (une couleur, une typo, un type d'image) | Clusters esthétiques abstraits (un univers, un registre) |
| **Produit quand** | Phase 2, AVANT les concepts | Phase 3B, APRÈS que le concept existe |
| **Produit par qui** | Subagent scoping (analyse sectorielle) | DA design (classification de ses choix) |
| **Commun aux 3 concepts** | Oui — le même pour les 3 | Non — chaque concept a le sien |
| **Exemple concret** | "Pas de vert sauge, pas de Nunito" | "On s'éloigne du corporate utilities et du militant lo-fi" |
| **Mécanisme d'injection** | Variable `{ventre_mou}` → section titrée "INTERDITS" en Phase 4 | Noyé dans le pitch `{concept_details}`, pas isolé |
| **Formulation** | "NE PAS reproduire" (binaire) | "Ce dont le concept s'éloigne" (directionnel) |
| **Calibré sur B** | Non (identique quel que soit B) | Censé l'être (ligne 156) mais sans règle concrète |
| **Gate de vérification** | Non (mais formulation "INTERDITS" est forte) | Non |

### Circuit de transmission de l'anti-territoire

```
Phase 3B : le DA écrit l'anti-territoire dans le pitch
        │
        ▼
Le pitch est écrit dans {brand}-pitch-c{N}.md
        │
        ▼
L'orchestrateur extrait {concept_details} du pitch pour Phase 4
        │
        ▼
{concept_details} = blob de ~3000 mots (intention créative + direction visuelle +
palette + typo + surface + interaction + données métier + philosophie hover +
prescriptions d'exécution + registre atmosphérique + Carte d'Inspiration +
visuels recommandés + graine logo + bénéfices business + avis DA)
        │
        ▼
Le codeur Phase 4 reçoit ce blob. L'anti-territoire est NOYÉ
dans la Carte d'Inspiration, elle-même une des 8+ sections.
Jamais isolé comme contrainte.
```

### Conclusion anti-territoire

L'anti-territoire est un output qui meurt dans le pitch. Il n'est pas injecté comme variable dédiée. Il n'est pas dans une section titrée "INTERDITS". Il est noyé dans un blob de texte. Son influence réelle sur le code HTML est indéterminée (dépend de combien le LLM le remarque parmi ~3000 mots de pitch).

---

## PARTIE 4 — La logique du système : pourquoi 2 filtres distincts ?

### La théorie (pertinente)

Le Ventre Mou et l'anti-territoire répondent à deux questions différentes :

1. **Ventre Mou** : "Que font les concurrents ?" → inventaire factuel, sectoriel, partagé entre les 3 concepts. C'est un INPUT du processus créatif (on le produit AVANT de créer).

2. **Anti-territoire** : "De quoi ce CONCEPT SPÉCIFIQUE s'éloigne-t-il ?" → déclaration positionnelle, conceptuelle, propre à chaque concept. C'est un OUTPUT du processus créatif (on le produit APRÈS avoir choisi).

La distinction a du sens : un concept "Symbiose Vivante" (organique, fluide) s'éloigne du corporate utilities. Un concept "Précision Brute" (mécanique, angulaire) s'éloigne peut-être de l'artisanal craft. Même si les deux évitent le même Ventre Mou sectoriel (vert sauge, Nunito), leurs anti-territoires divergent.

### La pratique (cassée)

En pratique, l'anti-territoire a 3 problèmes :

1. **Il n'est pas isolé comme contrainte en Phase 4.** Il est noyé dans le pitch. Le codeur Phase 4 ne le voit pas comme une interdiction.

2. **Il est redondant avec le Ventre Mou dans la majorité des cas.** "On s'éloigne du corporate utilities" est une reformulation abstraite de "pas de fonds blancs, pas de pictos flat, pas de ton institutionnel" — qui est déjà dans le Ventre Mou en plus concret et plus actionnable.

3. **C'est le seul point d'ancrage de B, et il ne fait pas le job.** L'instruction dit "déduis l'anti-territoire du Ventre Mou ET du curseur B", mais sans règle concrète sur comment B gradue l'anti-territoire.

### Ce qui manque dans le système

Le Ventre Mou dit **"ne fais pas ça"** (binaire, quel que soit B). Mais rien ne dit :
- **"Fais le CONTRAIRE de ça"** → ce que B=3 devrait produire
- **"Reste proche tout en évitant le pire"** → ce que B=1 devrait produire

Le curseur B est censé graduer cette distance au Ventre Mou, mais le seul mécanisme de distance (l'anti-territoire) meurt dans le blob du pitch.

---

## PARTIE 5 — Résolution choisie (implémentée — D45, avril 2026)

**Option A retenue** (VM visuel gradué par B) avec 2 ajustements par rapport à la proposition initiale :
1. **Gradation corrigée** : B=1 = permissif (tu PEUX utiliser les codes), B=2 = statu quo (INTERDIT), B=3 = contre-pied actif. La proposition initiale mettait B=1=avertissement, mais la logique du curseur (Mimétisme→ZAG) implique que B=1 autorise les codes sectoriels.
2. **VM narratif retiré de Phase 3A** : l'analyse des outputs réels a montré que les 3 concepts zaggent mécaniquement contre les 7 mêmes items du VM narratif → zéro différenciation, zéro valeur ajoutée. Le VM narratif listait des défauts (ton culpabilisant, discours mou), pas des codes neutres graduables.
3. **Anti-territoire** : gardé comme exercice de réflexion pour le DA en Phase 3B, mais la mention du curseur B retirée (B est géré par le VM gradué).

Les options B, C, D ci-dessous sont archivées comme historique de réflexion.

### Option A — Instrumenter B via le Ventre Mou gradué

Modifier la transmission du Ventre Mou en Phase 4 pour qu'il soit **gradué selon B** :

- **B=1** : le Ventre Mou est transmis comme une liste d'**AVERTISSEMENTS** ("attention, ces codes sont sectoriels — vous pouvez les utiliser si le concept le justifie"). Le filtre est non-bloquant.
- **B=2** : le Ventre Mou est transmis comme aujourd'hui — INTERDICTIONS binaires ("NE PAS reproduire").
- **B=3** : le Ventre Mou est transmis avec une directive de CONTRE-PIED ("pour chaque élément du Ventre Mou, montrer que le concept fait le CONTRAIRE — ex: si le secteur fait du vert sauge → la palette ne contient PAS de vert").

Avantage : réutilise un mécanisme qui fonctionne déjà (la variable `{ventre_mou}` et la section "INTERDITS").
Risque : B=1 qui autorise les codes sectoriels peut produire un résultat générique.

### Option B — Renforcer l'anti-territoire avec un circuit dédié

Donner à l'anti-territoire le même circuit que le Ventre Mou :
- Variable dédiée `{anti_territoire}` extraite du pitch par l'orchestrateur
- Section titrée "ANTI-TERRITOIRE — CE CONCEPT S'ÉLOIGNE DE" en Phase 4
- Formulé en clusters esthétiques (pas en éléments concrets — c'est le complément du Ventre Mou, pas un doublon)

Avantage : l'anti-territoire devient actionnable en Phase 4.
Risque : doublon partiel avec le Ventre Mou, augmente le volume du prompt Phase 4.

### Option C — Fusionner anti-territoire dans le Ventre Mou et graduer par B

Supprimer l'anti-territoire comme concept séparé. Le Ventre Mou gradué par B fait tout le travail :
- B=1 : Ventre Mou = avertissements
- B=2 : Ventre Mou = interdictions
- B=3 : Ventre Mou = interdictions + directive de contre-pied

Avantage : un seul concept, un seul circuit, clarifie l'architecture.
Risque : on perd la spécificité par concept (le Ventre Mou est le même pour les 3 concepts, l'anti-territoire était propre à chaque concept).

### Option D — Assumer B comme conceptuel pur

Accepter que B agit uniquement via le pitch 3B, sans mécanique. Renommer le gate "Cursor Coherence" en "Composition Coherence" (ne vérifie que A). Documenter : "B est un curseur stratégique qui influence la posture du DA, pas un paramètre technique."

Avantage : honnêteté, zéro complexité ajoutée.
Risque : l'utilisateur qui met B=3 s'attend à un résultat visuellement en rupture avec le secteur — et rien ne le garantit.

---

## PARTIE 6 — Le rapport initial de contexte (session précédente)

Le REX de la session 9-13 avril (`ref/rex-visual-upgrade-session-2026-04-09-13.md`) documente le contexte plus large de l'optimisation des style-tiles. Les points pertinents pour le curseur B :

### Découvertes fondamentales sur la qualité des style-tiles

1. **Pitch > Exemples > Principes** : la qualité du style-tile dépend à ~80% du pitch 3B. Les blacklists et gates relèvent le plancher mais ne poussent pas le plafond. Le plafond vient de la spécificité et de la richesse sensorielle du pitch. → Si B ne module pas le pitch efficacement, B ne module pas le résultat.

2. **Code > Rules** : le LLM suit ce qu'il VOIT dans les exemples HTML plus que ce qu'on lui écrit en règles. → Même si on ajoute des règles B, elles seront moins efficaces qu'un mécanisme qui change ce que le LLM voit (exemples, variables injectées dans des sections titrées).

3. **La blacklist relève le plancher, pas le plafond** : elle élimine le daté mais ne pousse pas vers l'élite. → Un B=3 instrumenté par des interdictions (Ventre Mou renforcé) ne fera que le minimum. Pour pousser vers le contre-pied, il faut une directive positive, pas juste une interdiction.

### Ce qui a été fait dans la session 9-13 avril

- 3ème couche graphique décorative ajoutée (grain, overlays, formes)
- Artefact refactoré (subagent dédié, structure semi-standardisée)
- Gate visuel Puppeteer ajouté (crops ciblés)
- Grain calibré (tuilé 150px, soft-light, 0.35-0.45)
- Brand watermark et clip-path sur halos interdits

### Chantiers ouverts identifiés (pertinents pour B)

1. **Audit mapping A1/A2/A3** → FAIT dans la session actuelle (vague 1 commitée)
2. **Gate visuel en crops ciblés** → implémenté mais pas encore validé empiriquement
3. **Grain** → monté à 0.35-0.45, pas encore testé
4. **Formes à contour net** → découragées mais le subagent continue d'en produire
5. **Incohérence nommage étalons** → toujours pas corrigé

---

## PARTIE 7 — État actuel du système après la vague 1

### Ce qui a été nettoyé (commit `79d8da3`)

Toutes les prescriptions qui liaient une technique CSS à un niveau de curseur A ont été remplacées par des sensations :

| Fichier | Modification |
|---------|-------------|
| `phase-4-styletile.md` | Calibrage image : split/clip-path/overflow → zones distinctes/interaction/entrelacement |
| `html-showroom-spec.md` | Tableau §8 : supprimé colonne "Adapté pour" et "split DÉCONSEILLÉ pour A=3" |
| `SKILL.md` | Calibrage Batch 3 : retiré @property, clip-path, @starting-style, subgrid par niveau |
| `phase-3b-design.md` | Checklist A=3 : retiré z-index, blend modes, masques. Calibrage surface A=1/2/3 reformulé |
| `phase-4-artefact.md` | Calibrage A=3 aligné |
| `phase4-finishing-gate.py` | check_clip_or_mask : WARN uniforme pour tous les A |
| `SKILL.md` | Prompt contrôleur : retiré "clip-path absent pour A=1" |

### Ce qui reste à faire (vague 2 — pas encore commencée)

Catégories 3 + 6 : le fichier prescripteur `interface-design-lens.md` expose des techniques CSS au DA, et les formulations hybrides sensation/technique dans Phase 4 doivent être nettoyées. Le plan existe dans `ref/plan-nettoyage-curseurs-A-B.md` (Plan 2).

### Ce qui reste à décider

- **Catégorie 4** : les 3 pools de fonts et type-scale séparés par curseur A — garder ou unifier ?
- **Catégorie 5** : les exemples HTML ségrégués standard/rupture par curseur A — garder ou pool unique ?
- **Catégorie 7** : le curseur B — instrumenter (options A/B/C) ou assumer comme conceptuel (option D) ?

---

## FICHIERS DE RÉFÉRENCE

| Fichier | Contenu | Pertinence |
|---------|---------|------------|
| `ref/plan-nettoyage-curseurs-A-B.md` | Plan complet des 7 catégories d'incohérences identifiées | Plan d'action détaillé |
| `ref/rex-visual-upgrade-session-2026-04-09-13.md` | REX session 9-13 avril (3ème couche, artefact, grain, gate visuel) | Contexte qualité style-tiles |
| `ref/rex-visual-upgrade-session-2026-04-04-08.md` | REX session 4-8 avril (blacklists CSS/composition, gates, exemples) | Contexte blacklists et patterns |
| `ref/rapport-gap-visual-elite.md` | 8 leviers d'optimisation, audit 88 sites Awards | Contexte niveau cible |
| `ref/bible-design-strategie.md` | Définition des curseurs A et B | Source de vérité curseurs |
| `phases/phase-2a-scoping.md` | Production du Ventre Mou | Source du filtre sectoriel |
| `phases/phase-3b-design.md` | Production de l'anti-territoire (ligne 156) | Seul point d'action de B |
| `phases/phase-4-styletile.md` | Injection du Ventre Mou ("ÉLÉMENTS INTERDITS") | Filtre binaire en Phase 4 |
| `DECISIONS.md` | Historique des décisions d'architecture | Contexte des choix passés |

## Dernière mise à jour : 2026-04-14
