# REX — Problème "Tell don't Show" dans les Batch 2/3

**Date** : 2026-02-23
**Contexte** : Test Camille A2×B2, concept "La Partition", session test-camille-2-2-v12
**Sévérité** : Haute — affecte la qualité perçue du showroom

---

## Le problème

Dans un showroom d'identité de marque, certaines sections **décrivent en texte** un traitement visuel au lieu de le **démontrer visuellement en CSS**. Le visiteur lit "Bleu-ardoise" sur fond blanc au lieu de **voir** du bleu-ardoise.

## Cas déclencheur

**Section 08.2 — Traitement Chromatique**, cartes "Ombres / Tons Moyens / Hautes Lumières" :
- Les 3 cartes ont un fond identique (transparent + bordure légère)
- Le texte décrit le traitement ("Bleu-ardoise", "Désaturés froids", "Parchemin + cuivre")
- **Aucun background-color, gradient ou filtre** ne matérialise visuellement ce qui est décrit
- Le CSS est minimal : `border: 1px solid var(--color-border-light)` + hover subtil

## Audit complet — Sections affectées

| Section | Sévérité | Ce qui manque |
|---------|----------|---------------|
| **08.2 — Filter Specs cards** | **HAUTE** | Les 3 cartes devraient avoir un fond/gradient incarnant la zone tonale décrite (ardoise, froid, parchemin) |
| **09.2 — Stratégie de Densité** | **HAUTE** | Les 2 cartes "Aéré" vs "Compact" ont les **mêmes paddings/densités** — zéro différence visuelle entre les deux modes |
| **10.3 — Éléments Récurrents** | **MOYENNE** | Les SVGs montrent les formes isolées mais pas en contexte d'usage (la portée devrait être en arrière-plan avec du texte posé dessus) |

Les autres sections (08.1 Moodboard, 08.3 Devices, 09.1 Grilles, 09.3 Patterns, 10.1 Métaphore, 10.2 Physique, 10.4 Composition) sont **correctement expressives**.

## Cause racine

Le problème vient des **prompts subagents dans SKILL.md** (Phase 6B, lignes 2358-2484). Certaines sections ont le tag `Surface EXPRESSIVE` dans leur description, d'autres non :

| Section | Instruction prompt | Tag EXPRESSIVE | Résultat |
|---------|-------------------|----------------|----------|
| 08.1 Style Photo | "Moodboard avec descriptions d'ambiances. **Surface EXPRESSIVE**" | Oui | Riche |
| 08.2 Chromatique | "Démonstration du color grading. Utilise mix-blend-mode ou filter CSS" | Non (dit juste "utilise") | Le before/after est OK, mais les specs cards sont plates |
| 09.2 Densité | "Comparaison aéré vs compact. Deux versions côte à côte du même contenu" | Non | Identiques visuellement |
| 09.3 Patterns | "Surface EXPRESSIVE — utilise les techniques CSS du curseur A" | Oui | Riche |
| 10.2 Physique | "Surface EXPRESSIVE — utilise les techniques CSS du curseur A" | Oui | Riche |
| 10.3 Character | "montrer les éléments récurrents du langage illustratif" | Non | Formes isolées, pas en contexte |

**Pattern clair** : quand le prompt dit "Surface EXPRESSIVE", le résultat est visuellement riche. Quand il ne le dit pas, le LLM produit du texte descriptif sur fond neutre.

C'est la variante prompt du learning déjà documenté : **"Code > Rules — le LLM adopte ce qu'il VOIT, pas ce qu'il lit."** Ici : **le LLM fait ce qui est explicitement demandé, pas ce qui est implicitement attendu.**

## Recommandation — Fix systémique

### Fix 1 (prioritaire) — Règle globale dans `{batch3_shared_context}`

Ajouter dans le bloc de contexte commun aux 3 subagents (SKILL.md, lignes 2292-2356) :

```
## RÈGLE SHOW > TELL
Chaque carte, bloc ou zone qui DÉCRIT un traitement visuel DOIT l'INCARNER en CSS.
- Si une carte dit "bleu-ardoise" → son background DOIT être bleu-ardoise
- Si deux cartes comparent "aéré" vs "compact" → les paddings et densités DOIVENT différer visiblement
- Si un élément illustratif est montré → le montrer EN CONTEXTE D'USAGE, pas isolé sur fond vide
- Zéro carte "texte descriptif sur fond neutre" pour un concept visuel
```

### Fix 2 (quick win) — Renforcer les prompts des sections faibles

- **08.2** : ajouter *"Les 3 specs cards (ombres/tons/highlights) doivent avoir un background-color qui INCARNE la zone tonale décrite"*
- **09.2** : ajouter *"La carte aérée doit avoir 3× plus de padding et moins de contenu. La carte compacte doit être dense, serrée. La DIFFÉRENCE doit être immédiate visuellement."*
- **10.3** : ajouter *"Montrer chaque élément EN CONTEXTE : la portée comme arrière-plan avec du texte dessus, la note comme marqueur dans un paragraphe, la barre comme séparateur entre sections."*

### Fix 3 (ceinture + bretelles) — Nouvelle gate de validation

Ajouter dans la section GATES DE VALIDATION des subagents :

```
6. **Show > Tell** : Chaque texte qui décrit un traitement visuel est-il INCARNÉ par le CSS de son conteneur ?
```

## Applicabilité

- **Batch 3** : directement concerné (3 sections identifiées)
- **Batch 2** : potentiellement concerné (à auditer — les sections Iconographie et Data Viz peuvent avoir le même pattern)
- **Phase 4 (Style-Tiles)** : moins concerné car le prompt est plus directif, mais vérifier les sections Voice et Atmosphere

## Fichiers de référence

- `SKILL.md` Phase 6B : lignes 2203-2533 (prompts subagents Batch 3)
- `SKILL.md` Phase 6B shared context : lignes 2292-2356 (bloc commun)
- Fichier généré de test : `outputs/test-camille-2-2-v12/camille-batch3-narration-espace.html`
- Exemple standard : `examples/standard/batch3-example.html`
