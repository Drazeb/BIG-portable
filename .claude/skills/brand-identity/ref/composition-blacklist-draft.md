# Blacklist Composition — DRAFT (non validé)

**Statut** : BROUILLON. Cette liste est basée sur le consensus critique dans les données d'entraînement du LLM. Elle n'est PAS encore croisée avec des données positives (analyse de sites Awards 2024-2025). Certains items pourraient être de faux négatifs (critiqués par la communauté mais toujours utilisés par les meilleurs sites).

**Prochaine étape** : croiser avec un benchmark positif de sites Awards. Ce qui est dans cette liste ET absent des Awards = blacklist validée. Ce qui est dans cette liste MAIS présent dans les Awards = retirer de la blacklist.

---

## Items à consensus fort (à valider par croisement Awards)

### Hero (Voice Block)

| # | Pattern | Consensus critique | Risque de faux négatif |
|---|---------|-------------------|----------------------|
| 1 | **Hero split 50/50 par défaut** (texte gauche, image droite, séparés) | Rapport de gap BIG (71% vs 19% Awards) + critique community | FAIBLE — données chiffrées |
| 2 | **Device mockup comme hero** (laptop/phone avec screenshot produit) | Critique massive "stop putting your app in a laptop" | **ÉLEVÉ — vu dans des sites Awards récents** |
| 3 | **Formes géométriques flottantes** comme décoration (cercles, triangles, blobs abstraits sans signification) | Critique forte "the SaaS decoration problem" | MOYEN — à vérifier |

### Artefact

| # | Pattern | Consensus critique | Risque de faux négatif |
|---|---------|-------------------|----------------------|
| 4 | **Cards icône ronde + titre + description** (le "features section" générique) | Le pattern le plus massivement critiqué du web. Chaque template l'utilise | FAIBLE |
| 5 | **3 colonnes pricing "middle highlighted"** (3 plans côte à côte, milieu proéminent) | Copie de Stripe 2016 | MOYEN — pricing 3 colonnes existe encore, c'est le "middle highlighted" qui est cliché |
| 6 | **"How it works" en 3 étapes** avec icônes numérotées (step 1 → step 2 → step 3) | Critique large du template par défaut | MOYEN — les processus en étapes existent encore, c'est la présentation iconique qui est cliché |
| 7 | **Sections alternées zigzag** (texte gauche/image droite, puis inversé, en boucle) | Critique documentée "zigzag layout" = remplissage par défaut | FAIBLE |
| 8 | **KPI row** (3-4 gros chiffres alignés) comme artefact seul | Critique modérée-forte : chiffres sans contexte = remplissage | MOYEN — les KPI existent encore dans des dashboards, c'est le "row isolée" qui est cliché |
| 9 | **Carousel/slider** pour du contenu | Consensus très fort (Nielsen Norman Group, Baymard Institute) : "carousel blindness" | FAIBLE |

### Atmosphere Block

| # | Pattern | Consensus critique | Risque de faux négatif |
|---|---------|-------------------|----------------------|
| 10 | **Guillemets géants** décoratifs sur citations (le gros " avant le texte testimonial) | Critique forte — cliché n°1 des sections témoignages | MOYEN — à vérifier sur Awards |
| 11 | **Signup newsletter** dans le footer comme seul contenu | Critique comme "remplissage par défaut" | MOYEN |

### Transversal

| # | Pattern | Consensus critique | Risque de faux négatif |
|---|---------|-------------------|----------------------|
| 12 | **Illustrations isométriques** (style "2.5D" avec personnages/objets en perspective iso) | Tendance 2018-2020 massivement identifiée comme révolue | FAIBLE |
| 13 | **Logo wall en niveaux de gris** ("Ils nous font confiance" + rangée de logos grisés) | Critique modérée-forte | **ÉLEVÉ — très courant sur les sites B2B Awards** |

---

## Items retirés (pas de consensus assez fort)

| Item | Raison du retrait |
|---|---|
| Empilement vertical strict | Fondamental du layout, pas un cliché. Contextuel |
| CTA avec flèche (→) | Overused mais pas mort (Vercel, Linear l'utilisent) |
| Numérotation 01. 02. 03. | Choix esthétique, pas de consensus critique |
| Citation centrée | Pattern classique intemporel |
| Overline avec petite ligne | Overused mais fonctionnel |
| Fond sombre par défaut | Biais LLM, pas un pattern de composition |

---

## Méthode de validation

Pour chaque item, analyser 15-20 sites Awards 2024-2025 (tous secteurs) et noter :
- Présent dans combien de sites Awards ?
- Si présent, sous quelle forme (identique au cliché ou variante moderne) ?

Décision :
- 0-1 sites Awards → blacklist validée
- 2-3 sites Awards → examiner les variantes. Si c'est la même forme → retirer de la blacklist. Si c'est une variante modernisée → garder en blacklist avec nuance.
- 4+ sites Awards → retirer de la blacklist

## Dernière mise à jour : 2026-04-05
