PROMPT SUBAGENT PHASE 3A — MODE SÉLECTIF / COUVREUR DE REGISTRE :

Tu vas produire 100 mots qui couvrent le registre **"{registre}"**.

⚠ Tu reçois UNIQUEMENT le nom du registre. Tu n'as **aucune information sur la marque** ni sur les territoires créatifs. C'est volontaire : ce pool sera ensuite évalué en aval par d'autres subagents qui, eux, connaîtront le brief. Ton job est de produire la matière première la plus large et la mieux dispersée possible.

## Consignes de couverture

- Va dans les recoins, pas seulement les évidences statistiques du registre
- Inclus les mots techniques ET les mots poétiques ET les mots du quotidien lié à ce registre
- Inclus des éléments de plusieurs natures : objets, phénomènes, processus, expériences sensorielles, métiers, instruments, lieux, gestes, sensations, concepts abstraits, références culturelles
- Pas de doublons sémantiques (si tu mets "étoile", ne mets pas aussi "astre" qui dit la même chose)

## Angles à inclure explicitement (couvrir les angles culturels)

En plus des évidences techniques, inclus systématiquement :
- Noms propres emblématiques (figures du domaine, instruments célèbres, missions, œuvres)
- Lieux mythiques associés au registre
- Concepts philosophiques ou abstraits associés
- Références culturelles ou artistiques évoquant le registre (œuvres, films, livres, mythologie)
- Mots issus de cultures non-occidentales liées au registre, si pertinent
- Le vocabulaire du loisir/amateur lié au registre (gestes, instants, expériences)

## Consigne de dispersion

Vise un mélange équilibré :
- ~40 mots immédiatement reconnaissables par n'importe qui (fondamentaux)
- ~40 mots un peu connus (qu'un amateur du registre aurait)
- ~20 mots obscurs mais évocateurs (qui ouvrent un angle inattendu)

## Format de sortie

Liste numérotée de 1 à 100, un mot ou expression courte par ligne. Pas de catégorisation, pas de regroupement, pas d'explication.

Ordre : pioche dans l'ordre que tu veux (pas forcément par fréquence ni par catégorie). L'ordre n'est pas signifiant — il sera randomisé en aval.

## Output

Écris le résultat dans : `{output_path}`

Format exact attendu :

```
# Pool de 100 mots — Registre "{registre}"

1. {mot}
2. {mot}
...
100. {mot}
```

STATUS: OK quand le fichier est écrit avec exactement 100 mots distincts.
