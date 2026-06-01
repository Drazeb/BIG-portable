# REX — Le checkpoint de sélection typo (planche récap + swap) a été sauté

**Date** : 2026-05-29
**Session source** : `les-vermeil-premium-militant` (mode concept unique via Sélectif)
**Remonté par** : Charles, en Phase 3B — "il ne m'a pas montré les palettes de typos avec les typos choisis et les backups pour que je choisisse".
**Statut** : erreur d'orchestration confirmée, avec une faille systémique permissive dans le SKILL.
**Sévérité** : élevée. Une décision créative qui APPARTIENT à l'utilisateur (le choix final de la typo) a été prise à sa place sans qu'il puisse trancher ni swapper.

---

## TL;DR

En Phase 3B (typographie), l'orchestrateur est passé directement de **"le designer choisit le pairing"** au **"spécimen rendu"**, en SAUTANT le **checkpoint de sélection utilisateur** : la planche récap unifiée (`font-recap-all.mjs`) qui montre display + body retenus **et leurs backups**, avec le tableau de validation où l'utilisateur valide OU swappe (ex: "C1 display → backup 1").

Résultat : l'utilisateur a vu un spécimen d'UN pairing déjà décidé, au lieu de CHOISIR parmi les candidats + backups. Le choix lui a été retiré.

---

## Pourquoi ça a été sauté — analyse honnête de la cause racine

### Cause 1 (la mienne — orchestration) : j'ai bundlé deux choses séparables et n'en ai gardé qu'une mauvaise moitié

La Phase 3B-Vague2 contient en réalité DEUX dispositifs distincts qui ont des finalités différentes :

1. **Le mécanisme blind-planche / duos** (Vague 2ter, designer visuel en 2 interactions sur planches duos anonymisées) → c'est un **dispositif anti-biais INTERNE** : il empêche le LLM d'halluciner les propriétés des fonts ET empêche les 3 concepts de converger vers la même font.
2. **Le checkpoint de sélection utilisateur** (section "Checkpoint — Traduction, backups, planches récap, validation utilisateur") → c'est une **GATE DÉCISIONNELLE UTILISATEUR** : `font-recap-all.mjs` génère la planche récap (choix ★ + backups), l'orchestrateur ouvre le HTML et présente le tableau "OK pour lancer les pitchs, ou swap ?".

J'ai raisonné : "concept unique → le risque de convergence inter-concepts disparaît → je peux streamliner le mécanisme blind-planche". **Ce raisonnement est juste pour le dispositif (1).** Mais j'ai étendu à tort le "streamline" au dispositif (2) — alors que la validation utilisateur n'a RIEN à voir avec la convergence : elle est nécessaire qu'il y ait 1 ou 3 concepts. J'ai jeté la gate utilisateur en même temps que le dispositif anti-biais.

### Cause 2 (la mienne) : j'ai rationalisé que le spécimen ferait office de validation

Je me suis dit "le spécimen (Vague 3) a déjà une validation utilisateur, donc le choix sera validé là". Faux : le spécimen valide **UN pairing déjà arrêté**, il ne présente PAS les candidats + backups côte à côte pour un CHOIX. La validation "tu valides ou tu swappes" suppose de VOIR les alternatives — ce que seule la planche récap fait. Le spécimen est un "valide/ajuste sur un choix fait", pas un "choisis parmi".

### Cause 3 (systémique — le SKILL le permet) : la gate utilisateur n'est pas marquée non-skippable, et l'adaptation concept-unique n'est pas spécifiée

- Le checkpoint palette (Vague 1-choix) porte un marqueur fort : **"⚠ OBLIGATOIRE — NE PAS SAUTER CETTE ÉTAPE. La planche HTML comparative DOIT être générée et ouverte AVANT de demander le choix… Ne PAS présenter un résumé texte à la place."** Le checkpoint de sélection TYPO **n'a PAS ce marqueur équivalent.** Il est décrit comme une suite d'actions ("Avant de lancer les pitchs, l'orchestrateur prépare tout et demande validation") sans interdiction explicite de le sauter.
- La Phase 3B est écrite pour **3 concepts en parallèle**. Contrairement à la Phase 4 (qui a une "Détection dynamique des concepts disponibles" et itère sur `$CONCEPTS`), la Phase 3B **ne spécifie aucune adaptation pour un concept unique** (cas produit par le mode Sélectif quand l'utilisateur ne retient qu'un mot). L'orchestrateur est donc laissé à **improviser** l'adaptation single-concept — et l'improvisation a supprimé une gate utilisateur.

C'est le même patron que les 2 REX précédents : quand le SKILL laisse une latitude non bornée, l'orchestrateur prend un raccourci qui dégrade silencieusement (ici, retire un choix à l'utilisateur).

---

## Où regarder

Base skill : `/Users/charlesbezard/claude-code-tests/test-big-portable/BIG-portable/.claude/skills/brand-identity/`

| Élément | Rôle |
|---|---|
| `SKILL.md` — Vague 2ter "Designer visuel" | Le mécanisme blind-planche (dispositif anti-biais interne) |
| `SKILL.md` — section "Checkpoint — Traduction, backups, planches récap, validation utilisateur" | **La gate utilisateur sautée.** Points 3-4-5 : génération `font-recap-all.mjs`, ouverture navigateur, tableau de validation + swap |
| `lib/font-recap-all.mjs` | Génère la planche récap unifiée (choix ★ + backups) — JAMAIS appelé dans cette session |
| `lib/font-pool-contact-sheet.mjs` | Génère les planches duos + récap individuelles `font-selection-c{N}.png` — non appelé |
| `SKILL.md` — Vague 1-choix (palette) | **Le bon modèle** : marqueur "⚠ OBLIGATOIRE — NE PAS SAUTER" à répliquer sur la typo |
| `SKILL.md` — Phase 4 "Détection dynamique des concepts" | **Le bon modèle** d'adaptation N-concepts à répliquer en Phase 3B |

Trace de la session (ce qui a été produit vs sauté) : `outputs/les-vermeil-premium-militant/`
- Produit : `les-vermeil-penseur-c1.md`, `…-penseur-body-c1.md`, `…-font-backups.md`, `…-specimen-c1.{html,png}`
- **Jamais produit (preuve du saut)** : `les-vermeil-font-recap-all.html`, `font-pool-font-selection-c1.png`

---

## Recommandations systémiques (pour la session d'optimisation)

1. **Marquer le checkpoint de sélection typo comme NON-SKIPPABLE**, avec le même marqueur fort que le checkpoint palette : "⚠ OBLIGATOIRE — NE PAS SAUTER. La planche récap (`font-recap-all.mjs`) DOIT être générée et ouverte AVANT de demander le choix. Ne PAS présenter un spécimen à la place — le spécimen valide un choix déjà fait, il ne permet pas de choisir parmi les candidats + backups."

2. **Décrire explicitement dans le SKILL la séparation des deux dispositifs** : (a) blind-planche duos = anti-biais interne, adaptable/allégeable si concept unique ; (b) checkpoint récap + validation utilisateur = gate décisionnelle, JAMAIS allégeable quel que soit le nombre de concepts. Aujourd'hui ils sont présentés en continuité, ce qui invite à les traiter en bloc.

3. **Ajouter une section "Adaptation concept unique / run partiel" à la Phase 3B**, calquée sur la "Détection dynamique des concepts disponibles" de la Phase 4. Préciser ce qui s'allège (les duos parallèles, le shuffle anti-convergence) et ce qui NE s'allège PAS (les gates anti-slop, le checkpoint de sélection utilisateur). Sans ça, chaque orchestrateur réimprovise l'adaptation single-concept différemment.

4. **Garde-fou anti-skip générique** : tout point du SKILL qui retire un CHOIX à l'utilisateur (sélection parmi alternatives) doit être taggé d'un marqueur visuel uniforme (ex: `🚦 GATE UTILISATEUR — NON-SKIPPABLE`) et listé dans un index en tête de SKILL.md. Un orchestrateur qui "streamline" doit pouvoir distinguer en un coup d'œil ce qui est un dispositif interne (allégeable) d'une gate utilisateur (intouchable).

## Leçon transférable

"Streamliner pour un cas particulier (concept unique)" est légitime pour les **dispositifs internes** (anti-biais, anti-convergence) mais JAMAIS pour les **gates décisionnelles utilisateur**. La règle : un raccourci d'orchestration peut réduire le COÛT interne, jamais retirer un CHOIX à l'utilisateur. Quand les deux sont décrits en continuité dans le SKILL, le risque de les confondre est élevé — d'où la nécessité de les marquer distinctement.
