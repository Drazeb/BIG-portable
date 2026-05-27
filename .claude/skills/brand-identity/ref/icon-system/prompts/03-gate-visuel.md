GATE VISUEL — Procédure pour Claude Code en session (mini-app icon-system, étape 6)

Ce template **n'est PAS un prompt subagent**. C'est une procédure que Claude Code en session principale exécute, parce qu'elle nécessite l'accès multimodal (Read sur des images PNG) que les Task subagents ne portent pas de façon fiable.

## CE QUE TU FAIS (Claude Code en session)

Tu charges 4 éléments :
1. Le PNG capturé du chapitre 06 généré par le designer : `{run_dir}/03-chapter06.png`
2. Les 2-3 références canoniques de la famille : `tools/icon-system/references/{famille_id}/spec-*.png`
3. La slop sheet de la famille : `tools/icon-system/slop-sheets/{famille_id}.md`
4. Le concept narratif décontaminé + territoires : `{run_dir}/00-inputs/{brand}-concepts-narratifs.md` + `{brand}-territoires-v*.md`

Puis tu émets un verdict structuré en 4 checks (a/b/c/d), suivi d'un VERDICT final, dans le fichier `{run_dir}/04-gate-verdict.md`.

## CHECKS — Détails

### (a) Appartenance famille

**Question** : Le PNG du chapitre 06 généré ressemble-t-il visuellement à la famille graphique assignée ?

**Méthode** :
1. Regarder le PNG `03-chapter06.png`
2. Le comparer aux 2-3 spécimens de référence
3. Identifier les traits formels partagés vs divergents

**Sortie** : OUI / NON binaire + 2 phrases de justification visuelle citant des traits concrets observés (pas "ça ressemble", mais "les hachures rotation 15° sont présentes sur 5 des 6 icônes métier, les aplats noirs francs sont là, les contours stroke variable aussi").

### (b) Anti-patterns slop

**Question** : Aucun des 8 `[ANTI-N°]` de la slop sheet n'est présent ?

**Méthode** :
1. Lire la slop sheet de la famille assignée
2. Pour chacun des 8 `[ANTI-N°]`, examiner le PNG et statuer :
   - **OK** : l'anti-pattern n'est pas présent
   - **VIOLATION** : l'anti-pattern est visible — citer l'icône précise où il apparaît

**Sortie** : tableau structuré, 8 lignes, statut OK/VIOLATION + (si VIOLATION) icône concernée + 1 ligne de description.

### (c) Sujets vs territoires créatifs

**Question** : Les 6-8 icônes métier (sous-section 06.4) dérivent-elles des TERRITOIRES créatifs ou du métier littéral du brief ?

**Méthode** :
1. Lire les territoires créatifs (liste des mots-clés et clusters)
2. Pour chaque icône métier visible dans le PNG, identifier le sujet représenté
3. Statuer : le sujet appartient-il sémantiquement à un territoire créatif (= OUI) ou est-il une représentation littérale du métier (= NON) ?

**Exemple** : pour Camille (concept "Le Phare de Ralliement", territoires = "désencombrement chirurgical / cartographie / cap long terme") :
- Icône "loupe sur document" → NON (littéral, c'est "diagnostic" déguisé)
- Icône "scalpel net" → OUI (territoire "chirurgical / désencombrement")
- Icône "carte avec point cardinal" → OUI (territoire "cartographie")
- Icône "horloge" → NON (littéral)
- Icône "phare avec halo" → OUI (concept narratif central)

**Sortie** : tableau des 6-8 icônes, statut OUI/NON par icône, + pourcentage final (= % OUI). **Seuil attendu : ≥80%.**

### (d) Proximité visuelle vs références

**Question** : Quelle est la proximité visuelle entre le résultat et chaque référence canonique de la famille ?

**Méthode** :
1. Pour chaque spécimen de référence (3 PNG), noter 1-5 la proximité visuelle avec le résultat :
   - 5 : indissociable, mêmes signatures, même rendu
   - 4 : très proche, signatures partagées, micro-écarts
   - 3 : reconnaissable de la même famille, mais traitement différent
   - 2 : famille flottante, hésitation
   - 1 : famille différente, slop

2. Calculer la moyenne

**Sortie** : tableau des 3 références, note 1-5 + 1 ligne de justification par référence + moyenne calculée.

## VERDICT FINAL

Le verdict est calculé mécaniquement à partir des 4 checks :

- **PASS** :
  - (a) = OUI
  - (b) 0 violation
  - (c) ≥80%
  - (d) moyenne ≥3.5

- **SOFT_FAIL** : un OU deux des éléments ci-dessous :
  - (b) exactement 1 violation
  - (c) entre 60% et 80%
  - (d) moyenne entre 2.5 et 3.5

  → Le run est gardé tel quel, le verdict est consigné comme avertissement.

- **HARD_FAIL** :
  - (a) = NON
  - OU (b) ≥2 violations
  - OU (c) <60%

  → **Loop back vers étape 4 (Designer)** avec consignes correctives. Max 2 itérations. Au-delà, le run final est consigné comme SOFT_FAIL gardé.

## FORMAT DE SORTIE — `04-gate-verdict.md`

```markdown
# Gate visuel — Verdict

**Date** : {ISO_DATETIME}
**Run** : {run_dir_relative}
**Famille assignée** : {famille_id} — {famille_label}
**Itération** : {N}/3

## (a) Appartenance famille

**Statut** : OUI / NON

{2 phrases de justification visuelle citant des traits concrets}

## (b) Anti-patterns slop — 8 checks

| Anti-pattern | Statut | Icône concernée | Description |
|---|---|---|---|
| [ANTI-01] {nom} | OK / VIOLATION | ... | ... |
| [ANTI-02] {nom} | OK / VIOLATION | ... | ... |
| ... | ... | ... | ... |

Violations totales : **{N}**

## (c) Sujets vs territoires créatifs

| # | Icône (sujet) | Territoire OUI/NON | Justif |
|---|---|---|---|
| 1 | {nom} | OUI/NON | {1 ligne} |
| ... | ... | ... | ... |

Score : **{X}/{Y} = {%}**

## (d) Proximité visuelle vs références

| Référence | Note 1-5 | Justification |
|---|---|---|
| spec-01-{nom} | X | {1 ligne} |
| spec-02-{nom} | X | {1 ligne} |
| spec-03-{nom} | X | {1 ligne} |

Moyenne : **{X.X}**

## VERDICT : PASS / SOFT_FAIL / HARD_FAIL

{Si HARD_FAIL ou SOFT_FAIL : consignes correctives concrètes pour le Designer en cas de re-dispatch — citer les violations précises et les icônes à corriger}
```

## SORTIE

Écris le verdict dans `{run_dir}/04-gate-verdict.md`. Puis si HARD_FAIL, prépare les consignes correctives pour le re-dispatch du Designer.
