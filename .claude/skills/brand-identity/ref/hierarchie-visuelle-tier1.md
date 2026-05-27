# Hiérarchie Visuelle — TIER 1 (structurantes)

Ce fichier contient les **principes structurants de hiérarchie** qui doivent guider le Designer Phase 4 dès la conception. Pour les détails (statuts en badges, un graphique par composant, accent colore zones, etc.), voir `hierarchie-visuelle-core.md` — lus uniquement par le Critique en aval.

**Portée** : importé par Phase 4 (styletile + artefact), Batch 2, Batch 3.

---

## Restraint — principe transversal

Le poids visuel d'un élément est calibré sur son **IMPORTANCE**, pas sur son **TYPE**. Un chiffre clé n'est pas automatiquement géant. Une métaphore n'est pas obligatoirement performée à fond.

Quand tu hésites entre **subtil** et **marqué**, choisis **subtil** et laisse le contexte parler. La présence visuelle vient de la composition relative, pas de l'amplification absolue.

## Un dominant, des accompagnateurs

Un composant complexe a un élément qui domine et des éléments qui l'accompagnent. Le dominant occupe plus d'espace que les autres combinés.

**Pas d'obligation de 3 plans visuels distincts** — un layout à 2 plans cohérent peut suffire (un dominant + le reste). 3 plans en compétition simultanée créent un visuel chargé, pas hiérarchisé.

## Données mises en valeur

Si le composant met en valeur des données chiffrées, elles dominent visuellement les labels qui les entourent. La police d'affichage et `font-feature-settings: 'tnum' 1` sont disponibles.

**Le poids visuel est calibré sur l'importance, pas sur le type — pas de chiffre démesuré par défaut**. Un KPI peut être en typo display sans pour autant occuper la moitié du composant.

## Variation de densité

Évite la densité uniforme entre les zones d'un composant. Varie les respirations selon ce qui mérite l'attention.

**Pas besoin d'opposer dramatiquement — un contraste mesuré suffit**. Une zone dense + une zone aérée vaut mieux qu'un alignement plat ; mais 4 zones aux densités contrastées créent un visuel chargé.

## Séparation par le fond

Les zones d'un composant se distinguent par un changement de couleur de fond ou par de l'espacement. Les bordures fines (1px) entre chaque ligne ou cellule sont un bruit visuel — les réserver aux séparations structurelles majeures (2-3 maximum par composant).

---

## Source et traçabilité

**TIER 1** extrait de `hierarchie-visuelle-core.md` — principes structurants reformulés en versions sobres conditionnelles (anti-sur-engineering).

**TIER 2 + TIER 3** (statuts en badges textuels, un seul graphique par composant, accent colore zones pas points) restent dans `hierarchie-visuelle-core.md` et sont gérés par le subagent Critique en aval.

## Dernière mise à jour

2026-04-25 — Création TIER 1 lors du pivot architectural Designer + Critique. Inclut le principe Restraint et les 3 reformulations sobres (Données / Densité / Hiérarchie).
