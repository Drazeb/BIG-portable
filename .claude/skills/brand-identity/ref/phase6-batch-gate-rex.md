# REX — Script `phase6-batch-gate.py`

REX du script anti-slop déterministe qui valide les Batch 2 / Batch 3 en sortie de Phase 6A / 6B. Un REX par sujet : tous les apprentissages liés à ce script sont regroupés ici.

---

## Régression 06.4 — désynchronisation avec refactor D59 (juin 2026)

### Problème
Le test BIG a planté pendant la génération Batch 2 avec l'erreur : *« Le gate exige une section 06.4 qui n'existe plus depuis le refactor D59 (ch.06 = 3 sections). »*

### Cause racine
La constante `BATCH2_SECTIONS` du script listait explicitement la section `"06.4"` comme requise :

```python
BATCH2_SECTIONS = ["06.1", "06.2", "06.3", "06.4", ...]
```

Or le **refactor D59 (27 mai 2026)** a transformé le chapitre 06 du Batch 2 :
- **Avant D59** : 4 sections (06.1 Outline / 06.2 Solid / 06.3 Duotone / 06.4 Usage en contexte)
- **Depuis D59** : 3 sections orientées USAGE (06.1 Set d'icônes UI utilisables / 06.2 Traitements alternatifs / 06.3 Usage en contexte)

Le script gate a été oublié dans la liste de fichiers à synchroniser à l'occasion du refactor — le prompt `phase-6a-batch2.md`, les ressources `ref/icon-system/`, le CLAUDE.md ont été mis à jour, **mais pas le gate déterministe en aval** qui validait encore la grammaire pré-D59.

### Solution retenue
Retirer `"06.4"` de la liste `BATCH2_SECTIONS` dans `scripts/phase6-batch-gate.py` (ligne ~77). Ajouter un commentaire au-dessus de la constante qui rappelle l'historique D59 pour éviter que quelqu'un re-ajoute `06.4` plus tard sans contexte.

```python
# Chapitre 06 : 3 sections orientées USAGE depuis refactor D59 (27 mai 2026)
# — auparavant 4 sections (06.1 Outline / 06.2 Solid / 06.3 Duotone /
# 06.4 Usage en contexte). La nouvelle structure est 06.1 Set d'icônes UI
# utilisables / 06.2 Traitements alternatifs / 06.3 Usage en contexte.
BATCH2_SECTIONS = ["06.1", "06.2", "06.3",
                   "04.1", "04.2", "04.3", "04.4", "04.5",
                   "07.1", "07.2", "07.3", "07.4"]
```

### Pourquoi ça marche
La completeness check du gate (`check_completeness` dans le script) parcourt les sections listées dans `BATCH2_SECTIONS` et FAIL le batch si une section est absente. En retirant `06.4` de la liste, le check ne la cherche plus → pas de fail pour une section qui n'a légitimement plus lieu d'exister.

### Leçon transférable
**Tout refactor de prompt qui ajoute/supprime/renomme une section structurelle du livrable DOIT vérifier les scripts gates en aval qui valident cette structure.** Le gate est un binding déclaratif sur la grammaire du prompt — pas un check sémantique souple. Si la grammaire change, le gate doit suivre dans le MÊME commit, sinon régression silencieuse jusqu'au prochain run.

Liste des "couples" à synchroniser pour le chapitre 06 du Batch 2 :
- `.claude/skills/brand-identity/phases/phase-6a-batch2.md` (prompt subagent — grammaire à produire)
- `.claude/skills/brand-identity/scripts/phase6-batch-gate.py` (gate déterministe — grammaire à valider)
- `.claude/skills/brand-identity/ref/icon-system/` (slop-sheets et catalogue — ressources)
- `.claude/skills/brand-identity/SKILL.md` Phase 6A (orchestration)
- `.claude/skills/brand-identity/CLAUDE.md` (vue d'ensemble Phase 6A si présente)

À étendre quand un futur refactor touche un autre chapitre (04, 07, ou Batch 3 08/09/10).
