# Rapport — Exploration d'une orientation de registre pour les concepts narratifs (Phase 3A)

> **Destinataire** : session dédiée à l'exploration de cette fonctionnalité
> **Auteur** : session de travail du 12 mars 2026 (décontamination + batches Phase 3A)
> **Statut** : exploration à mener — rien n'est implémenté

---

## 1. Ce que Charles veut explorer

Quand on génère des concepts narratifs (par batch de 3), chaque concept atterrit naturellement dans un **registre** différent (ex: médico-légal, chimie/alchimie, cartographie, gravure, géologie, acoustique…). C'est un comportement émergent du LLM — aucune instruction ne dit "change de registre".

Sur 20+ concepts générés, la diversité de registres est intéressante. Mais Charles aimerait pouvoir **orienter** : "explore plutôt le domaine de la photographie" ou "reste dans les registres abstraits" — sans casser le territory-first.

**La question fondamentale** : peut-on ajouter une orientation de registre optionnelle au système actuel, en mode hybride ?

---

## 2. Pourquoi ça n'a JAMAIS marché avant (historique critique)

### L'ancien système (D25 → D33, toutes révisées par D34)

Le pipeline Phase 3A a connu **9 décisions successives** (D25 à D33) qui tentaient toutes de faire fonctionner des **catégories métaphoriques** (appelées "domaines de métaphore" : Naturel/Organique, Spatial/Architectural, Artisanal/Culturel, Abstrait/Conceptuel, etc.).

Le flow était : **brief → domaines de métaphore → métaphores → concepts**.

**Problème central** : le LLM faisait systématiquement du **domain-first**. Il prenait l'autoroute statistique du domaine (ex: "Naturel" → racine, croissance, saison, cycle, graine…) et connectait artificiellement le brief après coup. Le brief devenait un habillage, pas la source.

### Ce qui a été tenté et pourquoi ça a échoué

| Décision | Approche | Résultat |
|----------|----------|----------|
| **D25** | Brief-first directive ("pars de 5 facettes du brief, puis cherche dans le domaine") | Le LLM ignorait la directive — le domaine restait l'autoroute principale |
| **D26** | Redistribution des slots (1 métaphore par facette par domaine) | Améliorait l'alignement facette×domaine mais le domain-first persistait |
| **D27** | Format structural + verbes d'action | Cosmétique — le fond ne changeait pas |
| **D28** (devenu D29) | Profondeur métaphorique (3 niveaux d'exploration) + dédup inter-versions | Réduisait la convergence mais le domain-first restait le problème de fond |
| **D30** | Concept de réconciliation (1 trait unique au lieu de 2 pôles) | Réduisait la complexité d'entrée mais les domaines dominaient toujours |
| **D31** | Pipeline 3 agents isolés (chaque agent ne voit qu'1 pôle) | Architecture trop complexe, résultats pas meilleurs |
| **D32** | Agents parallèles par domaine + brief-first unifié | Meilleur mais toujours domain-first au fond |
| **D33** | Enrichissement exemples métaphoriques | Marginal |

**Diagnostic rétrospectif** : le problème n'était pas la formulation de la directive brief-first. C'est que **la structure même du prompt** (brief + domaine métaphorique) créait une compétition que le domaine gagnait toujours. Le LLM suit la contrainte la plus structurellement concrète (le domaine est un mot clair et activateur), pas l'instruction abstraite ("pars du brief").

C'est ce qu'on appelle le **pattern fondamental LLM** (documenté en MEMORY) : pour changer le comportement, changer la **structure** — pas renforcer l'instruction.

### Pourquoi D34 a tout changé

La décision D34 a **supprimé les domaines de métaphore** du pipeline. Plus de catégories. Plus de "Naturel", "Architectural", "Abstrait". À la place :

1. **Phase 2D-A** : extraction de qualités créatives du brief (6 catégories : Action, Énergie, Ressenti client, Posture, Bénéfice, Distinction)
2. **Phase 2D-B** : clustering de ces qualités en territoires créatifs (labels émergents, pas de catégories pré-définies)
3. **Phase 2E** : l'utilisateur compose son mix (Principal / Secondaire / Tertiaire)
4. **Phase 3A** : le subagent reçoit UNIQUEMENT le mix de territoires décontaminé + ventre mou → génère le concept

Le registre (médico-légal, chimie, cartographie…) **émerge** du croisement entre les mots-clés des territoires et l'interprétation du LLM. Il n'est plus prescrit.

---

## 3. Ce qui marche MAINTENANT — le système territory-first

### Architecture actuelle (à bien comprendre avant de toucher quoi que ce soit)

```
Brief
  ↓
Phase 2D-A : Extraction qualités créatives (6 catégories)
  → {brand}-qualites-v{N}.md
  ↓
Phase 2D-B : Clustering en territoires
  → {brand}-territoires-v{N}.md
  ↓
Phase 2E : User compose le mix (Principal / Secondaire / Tertiaire)
  → mix stocké dans {brand}-scoping.md
  ↓
Subagent décontamination : nettoie 3 blocs (territories + aesthetic + ventre mou)
  → {brand}-context-clean.md
  ↓
Phase 3A : 3 subagents séquentiels, reçoivent UNIQUEMENT :
  - territory_mix (décontaminé, anonymisé, sans direction)
  - ventre_mou (décontaminé)
  - aesthetic_profile (décontaminé, optionnel)
  - previous_concepts (anonymisés ou résumés pour cross-batch)
  - curseurs A×B
  + lisent 3 fichiers GÉNÉRIQUES : persona, bible, exemple
  → concept-{N}-v{version}.md (chemin anonyme, renommé après)
```

### Les 5 couches de protection anti-contamination

1. **Extraction 2D-A** : gate créative à 2 tests (universalité + exploitabilité visuelle) — filtre le jargon sectoriel dès l'extraction
2. **Clustering 2D-B** : ne reçoit QUE les qualités créatives, jamais le brief → pas de contamination sectorielle dans les regroupements
3. **Pré-filtrage scoping** : le subagent 2D lit `{brand}-scoping-filtered.md` (Tension + Ventre Mou + Réconciliation seulement), pas le scoping complet. Les sections Avis du DA / Diagnostic esthétique / Position ZAG contenaient des pré-décisions design qui contaminaient.
4. **Subagent décontamination 3A** : 3 tests sur chaque mot-clé (nom propre, jargon sectoriel, redondance) + anonymisation + retrait des directions
5. **Anonymisation totale 3A** : chemins de fichiers anonymes (`concept-{N}-v{version}.md`, pas `{brand}-concept-...`), nom de marque absent de toutes les variables, concepts précédents anonymisés, résumés de divergence pour cross-batch

### Résultats validés

- **Vermeil** (test 11 mars, post-anonymisation) : 3/3 territory-first. Zéro terme compost/déchet/terre dans les concepts.
- **Camille** (test 11 mars) : 3/3 territory-first, qualité near-perfect. 9 concepts sur 3 batches, tous territory-first, légère baisse de qualité en batch 3 mais acceptable.

### Mécanisme de divergence actuel

La divergence entre concepts au sein d'un batch est pilotée par :
- `{divergence_instruction}` : "STRUCTURELLEMENT DIFFÉRENT : métaphore différente, résolution de tension différente, monde visuel différent"
- `{previous_concepts}` : texte complet anonymisé (intra-batch) ou résumés ~50-80 tokens (cross-batch)

Aucune mention de registre, domaine, ou catégorie. Le LLM interprète spontanément "structurellement différent" comme "changer d'univers de référence" — d'où les sauts de registre observés.

---

## 4. Le piège à éviter absolument

### Le scénario catastrophe

Si on ajoute une orientation de registre dans le prompt Phase 3A (ex: `{registre_orientation}` = "Explore le domaine de la photographie"), on recrée **exactement** la situation D25-D33 :

- Le LLM reçoit des mots-clés de territoires (abstraits, secs) + un registre (concret, activateur)
- Le registre est **structurellement plus concret** que les mots-clés → il devient l'autoroute principale
- Le concept devient registre-first avec habillage territorial

C'est le pattern fondamental LLM : la contrainte la plus concrète gagne.

### Pourquoi "cette fois c'est différent" pourrait être vrai (ou pas)

L'argument pour l'approche hybride : les territoires décontaminés sont **plus riches** que l'ancien brief brut. On a 10-15 mots-clés créatifs soigneusement extraits et filtrés vs un brief de 2000 mots. Le ratio signal/bruit est meilleur.

Le contre-argument : le registre reste un mot unique ultra-activateur ("photographie", "typographie", "géologie") qui pèse plus lourd dans l'attention du LLM qu'une liste de 10 mots-clés abstraits. Le LLM a des milliers d'associations pré-entraînées pour "photographie" → chambre noire, argentique, révélateur, négatif, surexposition… C'est une autoroute à 8 voies vs des sentiers forestiers.

---

## 5. Pistes d'exploration (à tester, pas à implémenter)

### Piste A — Registre comme FILTRE POST-GÉNÉRATION (pas d'input)

Ne pas injecter le registre dans le prompt. Générer 6-9 concepts normalement (2-3 batches), puis proposer un filtre :

> "Parmi les 9 concepts générés, voici ceux qui explorent un registre proche de la photographie : 2A La Chambre Noire, 3B Le Cadrage…"

**Avantage** : zéro risque de contamination — le registre n'entre jamais dans le prompt.
**Limite** : on ne peut pas FORCER un registre qui n'émerge pas naturellement.

### Piste B — Registre comme CONTRAINTE DE DIVERGENCE (pas d'ancrage)

Au lieu de `{divergence_instruction}` = "structurellement différent", dire :

> "Structurellement différent. Pour ce concept, explore un registre créatif dans le champ de la photographie — mais le concept DOIT émerger des mots-clés de territoires, PAS du registre. Le registre colore l'interprétation, il ne la génère pas."

**Avantage** : oriente le registre tout en maintenant l'ancrage territorial.
**Risque** : le pattern LLM (contrainte concrète > instruction abstraite) pourrait faire du registre-first malgré la directive. À TESTER empiriquement.

### Piste C — Registre intégré au CLUSTERING (Phase 2D-B)

Intervenir plus tôt : au moment du clustering, proposer des regroupements orientés par registre. Ex: au lieu de laisser le clustering libre, dire "regroupe ces qualités en territoires, en privilégiant les regroupements qui évoquent le champ de la photographie".

**Avantage** : le registre influence les territoires eux-mêmes, pas les concepts directement.
**Risque** : contamination en amont — les territoires deviennent registre-first.

### Piste D — Vocabulaire de registre dans les MOTS-CLÉS de territoires

Au lieu de nommer le registre, enrichir les mots-clés des territoires avec du vocabulaire issu du registre voulu. Ex: si l'utilisateur veut "photographie", ajouter aux mots-clés existants des termes comme "révélation progressive", "cadrage", "netteté sélective" — qui sont à la fois des qualités créatives universelles ET des termes de photographie.

**Avantage** : les mots-clés restent le point de départ — territory-first préservé.
**Risque** : injection manuelle, lourd, et les mots-clés ajoutés pourraient ne pas être cohérents avec le brief.

### Piste E — Registre comme 2e PASS sur un concept existant

Garder la génération normale (territory-first, pas de registre). Quand l'utilisateur voit un concept intéressant mais veut le "transposer" dans un autre registre :

> "Reprends le concept 2A 'Le Scalpel Blanc' mais transpose-le dans le registre de la photographie. Les mots-clés de territoires restent les mêmes — seul l'univers de référence change."

**Avantage** : le concept est DÉJÀ territory-first — on ne fait que changer la surface.
**Risque** : la transposition peut dénaturer le concept si le registre est incompatible.

---

## 6. Recommandation de la session précédente

**Commencer par tester la Piste B** (registre comme contrainte de divergence). C'est le test le plus direct de l'hypothèse "est-ce que territory-first + registre orientation peut coexister ?".

**Protocole de test suggéré** :
1. Prendre le brief Camille (bien connu, résultats de référence disponibles)
2. Générer un batch de 3 concepts SANS orientation (baseline, déjà fait : 20+ concepts disponibles)
3. Générer un batch de 3 concepts AVEC orientation registre (ex: "photographie")
4. Comparer : les concepts orientés sont-ils territory-first (auto-test : chaque choix traçable à un mot-clé) ou registre-first (les choix viennent de l'univers "photographie" et les territoires sont habillés après) ?

**Critère de succès** : dans la section "Ancrage Territoires" du concept, les choix créatifs doivent être traçables à des mots-clés de territoires. Le registre "photographie" doit colorer le vocabulaire et l'imaginaire, PAS générer les choix créatifs.

**Critère d'échec** : si la section "Ancrage Territoires" contient des justifications du type "le mot-clé 'Révélatrice' évoque la chambre noire en photographie" → c'est du registre-first habillé de territorial. L'association "Révélatrice → chambre noire" vient du registre, pas du territoire.

---

## 7. Fichiers à lire avant de commencer

| Fichier | Pourquoi |
|---------|----------|
| `phases/phase-3a-concepts.md` | Le prompt actuel du subagent concept — c'est LUI qui serait modifié |
| `phases/phase-3a-decontamination.md` | Le filtre en amont — comprendre ce que le subagent reçoit |
| `phases/phase-2d-extraction.md` | Comment les qualités sont extraites du brief |
| `phases/phase-2d-clustering.md` | Comment les qualités deviennent des territoires |
| `SKILL.md` lignes ~695-870 | L'orchestration Phase 3A (variables, flow séquentiel, batches) |
| `ref/exclusion-metaphores-rex.md` | REX sur la redécouverte de métaphores (ancien système, mais le problème de fond est pertinent) |
| `DECISIONS.md` D25-D34 | L'historique complet des tentatives échouées avec les domaines de métaphore |
| `MEMORY.md` | Les patterns fondamentaux LLM documentés |

### Fichiers de test disponibles (résultats de référence)

| Session | Contenu |
|---------|---------|
| `outputs/test-camille-test-20260311-1557/` | 3 concepts territory-first (baseline sans orientation) |
| `outputs/test-camille-test-20260311-2310/` | 9 concepts sur 3 batches (test multi-batch) |
| `outputs/test-vermeil-test-20260311-1557/` | 3 concepts territory-first (2e marque de test) |

---

## 8. Résumé en 1 phrase

L'ancien système (brief + domaine de métaphore → domain-first) a échoué 9 fois. Le nouveau (brief → qualités → territoires décontaminés → concepts territory-first) marche. La question est : peut-on réintroduire une orientation de registre SANS recréer le piège domain-first, maintenant que la base est solide ?
