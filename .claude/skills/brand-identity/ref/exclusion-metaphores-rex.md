# REX — Bloc d'exclusion Phase 3A : candidats explorés non transmis

## Problème

Quand l'utilisateur demande plusieurs versions de concepts narratifs (v1, v2, v3…) sur les **mêmes domaines de métaphore**, le subagent "redécouvre" des métaphores qui avaient déjà été explorées (mais non retenues) dans une version précédente.

**Exemple concret** :
- v1, domaine Artisanal/Culturel : le subagent explore 5 candidats dont **Palimpseste** (score 10/15, non retenu — "La Trame" gagne avec 13/15)
- v3, même domaine Artisanal/Culturel : le subagent explore à nouveau Palimpseste, le sélectionne cette fois comme gagnant, et développe le concept complet
- L'utilisateur qui a lu la v1 voit que la v3 recycle une idée qu'il connaît déjà

**Cause racine** : le bloc `{exclusion_block}` construit par l'orchestrateur (Étape 3A, lignes ~787-808 du SKILL.md) ne transmet que les **métaphores gagnantes** (titre + métaphore centrale des concepts développés). Les 5 candidats explorés par domaine dans le tableau d'évaluation ne sont pas transmis aux versions suivantes.

## Ce qu'on a essayé (et pourquoi ça n'a pas marché)

- Approche actuelle : exclusion par titre + métaphore centrale des concepts retenus uniquement → le subagent n'a aucune visibilité sur les candidats non retenus des versions précédentes → redécouverte inévitable quand le même domaine est réassigné.

## Solution proposée

Enrichir le bloc `{exclusion_block}` pour inclure **tous les candidats explorés** (pas seulement les gagnants) quand le même domaine de métaphore revient dans une nouvelle version.

### Mécanisme d'extraction

Pour chaque fichier `{brand}-concepts-narratifs-v*.md` existant, extraire EN PLUS des titres/métaphores gagnantes :
- Les tableaux d'exploration métaphorique (lignes `| # | Métaphore | Prof. | ...`)
- Pour chaque ligne du tableau : le nom de la métaphore + le domaine associé

### Format du bloc d'exclusion enrichi

```
## CONCEPTS DÉJÀ GÉNÉRÉS — À NE PAS REPRODUIRE

Les concepts suivants ont déjà été produits :
- 1A — "La Trame" : tissage stratégique...
- 1B — "La Ligne de Fuite" : architecte de perspective...
- 1C — "Le Gradient" : mise au point progressive...

## MÉTAPHORES DÉJÀ EXPLORÉES PAR DOMAINE

Les métaphores suivantes ont déjà été évaluées dans des versions précédentes. INTERDIT de les reproposer, même reformulées.

**Artisanal / Culturel** (v1) : Alchimie, Fermentation, Palimpseste, Trame et chaîne, Patine
**Spatial / Architectural** (v1) : Fondation, Ligne de fuite, Belvédère, Cour intérieure, Voûte
**Abstrait / Conceptuel** (v1) : Catalyse, Gradient, Seuil critique, Résonance, Polarité
```

### Conditions d'application

- Ce bloc supplémentaire n'est injecté **que pour les domaines qui ont déjà été explorés** dans une version précédente. Si la v3 utilise un domaine jamais exploré avant, pas besoin d'exclusion de candidats pour ce domaine.
- Format compact : **nom de la métaphore uniquement** (pas la description complète), groupé par domaine. Coût token minimal (~1 ligne par domaine par version).

### Impact estimé

- **Tokens** : +1-3 lignes par domaine réutilisé par version. Négligeable.
- **Créativité** : positive — force le LLM à sortir des associations les plus évidentes du domaine.
- **Limite** : au-delà de 5 versions sur le même domaine (~25 métaphores exclues), le domaine commence à s'assécher. Prévoir un warning si >20 exclusions sur un même domaine.

## Où modifier

- **Fichier** : `.claude/skills/brand-identity/SKILL.md`
- **Section** : `### Étape 3A — Concepts Narratifs (Pass A)`, bloc "Versionnage (orchestrateur, AVANT le subagent)" (actuellement lignes ~783-808)
- **Ce qui change** : la logique de construction de `{exclusion_block}` doit parser les tableaux d'exploration des versions précédentes en plus des titres de concepts
