# Bug Report — Lockup secondaire : texte tronqué

## Le problème

Le texte "ATELIER VERMEIL" dans le lockup horizontal était tronqué — il affichait "LES ALCHIMIST" (il manquait "ES" à la fin).

## Cause racine

Le script Python qui génère le lockup secondaire **estime la largeur du texte** avec une formule :

```
text_width_est = nb_caractères × font_size × 0.62
```

Soit : `15 × 24 × 0.62 = 223px`

Cette estimation était **trop basse** pour Fraunces 700, qui est une police relativement large en graisse 700. En plus, le `letter-spacing: 2.5` (14 gaps × 2.5 = 35px supplémentaires) n'était pas suffisamment pris en compte.

Résultat : le viewBox calculé faisait `350` de large (`112 + 223 + 15` de padding), alors que le texte réel débordait au-delà.

## La correction

Élargissement du viewBox de `"0 0 350 80"` à `"0 0 450 80"` — +100px de marge, ce qui laisse assez de place pour le texte complet.

## Recommandation pour le système

Le coefficient `0.62` dans la formule d'estimation est trop optimiste pour les polices larges/grasses. Deux pistes :

1. **Augmenter le coefficient** : passer de `0.62` à `0.70-0.75` pour les polices weight 700+, surtout les serifs display comme Fraunces. Ajouter explicitement le letter-spacing au calcul : `text_width = nb_chars × font_size × coeff + (nb_chars - 1) × letter_spacing`

2. **Ajouter une marge de sécurité** : après calcul, multiplier par 1.15-1.20 pour absorber les variations entre familles de polices. Un viewBox trop large ne pose aucun problème visuel (l'espace vide à droite est invisible), alors qu'un viewBox trop étroit tronque le texte.

Le problème ne se pose que pour le lockup **horizontal** (secondaire) — le lockup vertical centre le texte sous le mark, donc un viewBox un peu large ne cause pas de troncature.

---

*Session : Atelier Vermeil a2-b2, concept Solstice Fertile — Feb 2026*
