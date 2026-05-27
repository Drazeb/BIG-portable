# Propositions d'Amélioration Créative du Pipeline BIG

> **Contexte** : Ces 5 pistes ont été identifiées lors d'une analyse de la nature de la génération créative par LLM (concept-first vs design-first). Le constat : un LLM co-génère concept et design en un seul flux statistique, ce qui tend à produire des "clusters moyens" plutôt que des idées véritablement distinctives. Ces propositions visent à forcer une créativité plus authentique.
>
> **Statut** : Pistes 1 (Two-Pass) et 2 (Domaines de métaphore) implémentées — Février 2026. Pistes 3, 4, 5 archivées pour implémentation future.
>
> **Date** : Février 2026

---

## Piste 1 — Two-Pass : Concept PUIS Design (la plus structurante)

Aujourd'hui Phase 3 = 1 prompt qui génère concept + design en un seul flux. Le modèle co-génère tout.

**Alternative** :
- **Pass A** (subagent 1) : Génère UNIQUEMENT le concept narratif — nom, résolution de tension, métaphore centrale, intention créative. **Zéro couleur, zéro font, zéro spec visuelle.**
- **Pass B** (subagent 2) : Reçoit le concept narratif en input (+ brief + curseurs) et **dérive** les choix de design à partir du concept.

Le subagent B n'a jamais vu le "cluster statistique habituel" — il doit DÉRIVER depuis le texte conceptuel. Ça force un vrai flow concept→design.

**Coût** : +1 subagent par concept (×3 = 6 au lieu de 1). Mais les passes A sont courtes.

**Gain créatif** : Élevé. Le concept peut aller dans des directions inattendues sans être "tiré vers le centre" par les associations palette/typo habituelles.

---

## Piste 2 — Diversité forcée par domaines de métaphore (facile à implémenter)

Actuellement les 3 concepts sont libres → ils tombent souvent dans des clusters proches (nature, lumière, terre pour un brief écolo par exemple).

**Alternative** : Imposer des **contraintes structurelles** sur les domaines de métaphore :
- Concept 1 : métaphore du monde **naturel/physique** (saisons, écosystèmes, matériaux...)
- Concept 2 : métaphore du monde **humain/culturel** (artisanat, voyages, rituels...)
- Concept 3 : métaphore du monde **abstrait/systémique** (mathématique, musical, géométrique...)

Le modèle DOIT explorer des territoires différents au lieu de rester dans le cluster le plus probable.

**Coût** : Quasi nul (3 lignes de prompt en plus).

**Gain créatif** : Moyen-élevé. Ça ne change pas le mécanisme, mais ça diversifie les outputs mécaniquement.

---

## Piste 3 — Validation adversariale (la plus élégante)

Après génération d'un concept complet, un **validateur** lit UNIQUEMENT les specs design (palette, typo, surface) SANS le narratif, et essaie de **reconstruire le concept**.

- S'il devine correctement → le design EST distinctif et porteur du concept
- S'il ne peut pas deviner → le design est trop générique (il pourrait servir n'importe quel concept)
- S'il reconstruit un concept DIFFÉRENT → il y a un problème de cohérence

C'est comme demander à quelqu'un de regarder un moodboard sans légende et de deviner l'intention créative.

**Coût** : +1 subagent par concept pour la validation.

**Gain créatif** : Pas directement — mais ça détecte les concepts "creux" où le narratif est séduisant mais le design est interchangeable.

---

## Piste 4 — Stimulus aléatoire / SCAMPER (la plus audacieuse)

Au lieu de laisser le modèle partir de sa distribution statistique, injecter un **stimulus créatif externe** :

- 3 mots aléatoires tirés d'un dictionnaire → "forge + origami + marée" → le modèle doit trouver le lien avec le brief
- Ou une analogie forcée : "Si cette marque était un bâtiment, lequel serait-ce et pourquoi ?" → puis dériver le design de l'analogie
- Ou SCAMPER : prendre le concept le plus évident du secteur et appliquer Substitute / Combine / Adapt / Modify / Put to other use / Eliminate / Reverse

C'est exactement ce que font les DA humains dans les workshops de brainstorming — des exercices de pensée latérale.

**Coût** : Complexité de prompt, résultats moins prévisibles.

**Gain créatif** : Très élevé — ça casse fondamentalement les patterns statistiques.

---

## Piste 5 — Anti-répétition par mémoire cross-sessions

Maintenir une bibliothèque des concepts déjà générés (par secteur, par brief-type) et dire au modèle : "Ces métaphores/palettes/territoires ont déjà été proposés dans des sessions précédentes → propose autre chose."

**Coût** : Infrastructure (fichier JSON de mémoire dans le skill).

**Gain créatif** : Progressif — plus le système est utilisé, plus il est forcé d'explorer des territoires nouveaux.

---

## Récap impact/effort

| Piste | Effort | Gain créatif | Faisabilité |
|-------|--------|-------------|-------------|
| **2. Domaines de métaphore** | Très faible | Moyen-élevé | Immédiate |
| **1. Two-pass concept/design** | Moyen | Élevé | Quelques heures |
| **3. Validation adversariale** | Moyen | Détection qualité | Quelques heures |
| **5. Mémoire cross-sessions** | Moyen | Progressif | Demi-journée |
| **4. Stimulus aléatoire** | Élevé | Très élevé | Expérimental |

La piste 2 est un "quick win" qui ne coûte rien. La piste 1 est le changement le plus structurant pour garantir un vrai flow concept→design. Les deux sont complémentaires.
