# Hiérarchie Visuelle — Core

Principes universels de hiérarchie visuelle. S'appliquent à TOUTES les sections, TOUS les composants, QUEL QUE SOIT le curseur A. Ils ne dictent pas de layout — ils dictent comment l'information est hiérarchisée visuellement.

**Portée** : importé par Phase 4 (styletile + artefact), Batch 2, Batch 3.

---

## Données clés mises en valeur

Si le composant met en valeur des données chiffrées, elles dominent visuellement les labels qui les entourent. La police d'affichage et `font-feature-settings: 'tnum' 1` sont disponibles. **Le poids visuel est calibré sur l'importance, pas sur le type — pas de chiffre démesuré par défaut**. Un KPI peut être en typo display sans pour autant occuper la moitié du composant.

## Taille proportionnelle à l'importance

L'élément principal occupe visuellement plus d'espace que les éléments secondaires. La hiérarchie se lit au premier regard : un élément DOMINE, les autres l'accompagnent. Pas de grille où tout est au même poids visuel.

## Hiérarchie multi-dimensionnelle

La hiérarchie ne se construit pas sur la taille seule — elle combine plusieurs dimensions : taille, poids typographique, couleur, position, espace autour. Un titre n'a pas besoin d'être énorme s'il est isolé par l'espace et porté par un poids fort. **Sans empiler tous les marqueurs sur le même élément** : la combinaison reste lisible, pas saturée. Le ratio de taille entre niveaux hiérarchiques doit rester perceptible — un écart trop faible aplatit la hiérarchie.

## Pondération 60-30-10 — répartition de poids visuel

Quand on parle de 60-30-10 (dominant / secondaire / accent), il s'agit du POIDS VISUEL perçu, pas de la surface en pixels. Une zone peut occuper 60% de la surface tout en pesant 30% visuellement (fond neutre, peu de contraste). L'accent (10%) doit rester rare pour conserver sa puissance — une couleur accent qui apparaît partout cesse d'être un accent.

## Séparation par le fond, pas par des lignes

Les zones d'un composant se distinguent par un changement de couleur de fond (teinte, luminosité) ou par de l'espacement. Les bordures fines (1px) entre chaque ligne sont un bruit visuel — les réserver aux séparations structurelles majeures (2-3 maximum par composant).

## Statuts et catégories en badges textuels

Les statuts (actif, en attente, terminé) et les catégories sont des badges textuels (fond teinté + texte + éventuellement un point coloré). Les barres de progression et les jauges sont réservées aux données qui ÉVOLUENT dans le temps — pas aux statuts binaires.

## Variation de densité

Évite la densité uniforme entre les zones d'un composant. Varie les respirations selon ce qui mérite l'attention. **Pas besoin d'opposer dramatiquement — un contraste mesuré suffit**. Une zone dense + une zone aérée vaut mieux qu'un alignement plat ; mais 4 zones aux densités contrastées créent un visuel chargé.

## Hiérarchie : un dominant, des accompagnateurs

Un composant complexe a un élément qui domine et des éléments qui l'accompagnent. Le dominant occupe plus d'espace que les autres combinés. Les accompagnateurs s'alignent dans la logique du dominant (même axe, même rythme, même registre de poids). **Pas d'obligation de 3 plans visuels distincts** — un layout à 2 plans cohérent peut suffire (un dominant + le reste). 3 plans en compétition simultanée créent un visuel chargé, pas hiérarchisé.

## Restraint — l'importance se signale par le poids, pas par l'accumulation

Le poids visuel signale l'importance ; le type ou le nombre de marqueurs ne le signale pas. Un titre n'a pas besoin d'être à la fois plus gros, plus gras, plus coloré, souligné et précédé d'une icône. Un choix subtil bien placé porte plus loin qu'une accumulation de marqueurs. Laisser le contexte (espace, position, alignement) faire une partie du travail — ne pas tout dire avec la typographie.

## Un seul graphique par composant

Si le composant contient de la dataviz (courbe, barres, donut), il n'en contient qu'UN. Le reste des données est en typographie brute (chiffres + labels) ou en badges. Plusieurs graphiques dans un même composant diluent l'impact de chacun.

## La couleur accent colore des zones, pas des points

Quand la couleur accent est utilisée, elle colore une ZONE entière (fond de panneau, bande latérale) plutôt que des petits éléments dispersés (un chiffre ici, un dot là). La masse chromatique a plus d'impact que le saupoudrage.

## Anticiper la variabilité du contenu

Designer la résilience visuelle, pas un état figé. Pour chaque zone qui reçoit du contenu, anticiper trois cas : court, moyen, très long. Un titre court doit tenir sans paraître orphelin ; un titre long doit pouvoir respirer sur deux lignes sans casser le layout. Les composants qui ne fonctionnent qu'avec un seul cas de longueur sont fragiles.

## Variance — varier le rythme de la page

Principe guideline : une page n'est pas une succession de blocs identiques. Varier le rythme entre sections (densités différentes, ratios d'image différents, layouts différents). Une section dense suivie d'une section aérée crée un battement qui guide la lecture. Trois sections de même densité d'affilée écrasent la hiérarchie globale.

## Échelles de calibration — motion et densité

Deux échelles 1-10 pour calibrer l'intensité visuelle au brief, pas par défaut :

- **Motion intensity** : 1-3 = static (transitions discrètes, hover minimal) / 4-7 = fluid CSS (mouvement utile, scroll-driven discret) / 8-10 = cinematic (mouvement comme matière, transitions narratives). La marque dicte le niveau, pas le réflexe technique.
- **Visual density** : 1-3 = airy (espace dominant, peu d'éléments par écran) / 4-7 = daily app (densité normale d'interface productive) / 8-10 = cockpit (densité maximale assumée, beaucoup d'information par unité de surface). Le brief et le contexte d'usage déterminent où se placer.

## Marques et codes techniques — translate="no"

Les noms de marque, codes techniques, tokens, identifiants doivent être protégés de la traduction automatique avec l'attribut `translate="no"` sur leur conteneur. Un nom de marque traduit automatiquement par le navigateur détruit l'identité. Règle informationnelle, pas esthétique.

---

## Source et traçabilité

**Factorisation** : ce fichier remplace les sections redondantes dans :
- `phases/phase-4-styletile.md` (section "PRINCIPES DE HIÉRARCHIE VISUELLE" L272-298)
- `phases/phase-4-artefact.md` (section L133-142)
- `phases/phase-6a-batch2.md` (section L63-89)
- `phases/phase-6b-batch3.md` (section L60-67)

Les 4 phases importeront ce fichier via l'orchestrateur.

## Dernière mise à jour

2026-04-24 — Création par factorisation des 4 phases. Étape 1 du plan d'intégration anti-slop.
