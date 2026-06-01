# REX — Phase 8 Brand Book : la section Pitch Deck échoue par dépassement du nesting de sous-agents

**Date** : 2026-05-30
**Session** : les-vermeil / premium-militant (Bocage)
**Gravité** : systémique — touche TOUTE session BIG qui exécute la Phase 8 (brand book) via le pipeline.

## Symptôme

Le brand book sort avec **11 sections sur 12** : la section **07b Pitch Deck** est dégradée (bloc `.deck-pending` avec placeholders), alors que les 7 autres sont complètes. Le sous-agent brand-book signale honnêtement : *« pas de Task tool disponible pour lancer le sous-sub-agent isolé »*.

## Cause racine — un seul niveau de délégation

Dans Claude Code, **l'outil `Task` (lancer un sous-agent) n'est disponible que pour l'agent principal**. Un sous-agent lancé par le principal ne reçoit PAS `Task` → il ne peut pas lancer un sous-agent à son tour. **Règle : un seul niveau de délégation.**

La Phase 8 du SKILL (Étape 8-2) demande à l'orchestrateur de lancer le brand-book **comme un sous-agent**. Or le skill brand-book (Étape 2d) doit lui-même lancer SPG `generate-mini-deck`, qui lui-même lance Sub0-A + Sub0-B + content-mapper. La chaîne demandée est donc :

| Niveau | Acteur | `Task` ? |
|---|---|---|
| 0 | Orchestrateur BIG | ✅ |
| 1 | sous-agent brand-book | ❌ |
| 2 | SPG generate-mini-deck | jamais atteint |
| 3 | Sub0-A / Sub0-B / content-mapper | — |

→ SPG est demandé à **niveau 2**, refusé.

## Pourquoi « ça marchait en local »

En lançant `/brand-book` **directement** dans la session principale, le brand-book s'exécute au niveau 0 → SPG est à niveau 1 → autorisé. Le pipeline BIG **ajoute une couche** (brand-book en sous-agent) qui pousse tout d'un cran trop profond. Ce n'est pas un bug du skill brand-book ni de SPG — c'est l'**orchestration Phase 8 qui empile une couche de trop**.

## Contournement appliqué (manuel, cette session)

L'orchestrateur (niveau 0) a **exécuté lui-même les étapes de SPG generate-mini-deck**, en lançant Sub0-A, Sub0-B et content-mapper comme SES propres sous-agents (niveau 1, autorisés) :
1. Prep dossier identity SPG (copie pack en noms canoniques).
2. Sub0-A (analyse visuelle) → VISUAL-ANALYSIS.md.
3. Sub0-B mode mini → design-language.md + slide-examples-mini.html (6 archétypes, alternance dark/light, validate-pptx OK).
4. content-mapper avec voice **réelle de la marque** (pas la voice "Camille" bakée dans le prompt SPG — à overrider explicitement).
5. Capture 6 PNG (Playwright) → `brand-book/pitch-deck-mini/`.
6. Patch du HTML brand book : remplacement du bloc `.deck-pending` par une vraie grille de slides + nettoyage de la CSS dégradée orpheline.
7. Bonus : masquer le bouton `.export-btn` (`position:fixed`) du template SPG AVANT capture, sinon il pollue le coin de la slide 1.

## Correctif SKILL recommandé

Deux options pour la session qui corrigera le SKILL :

1. **Ne PAS wrapper brand-book dans un sous-agent en Phase 8.** L'orchestrateur exécute le workflow brand-book directement (niveau 0), ce qui rend SPG accessible à niveau 1. C'est l'option la plus fidèle à l'usage `/brand-book` standalone.
2. **Découper la Phase 8** : l'orchestrateur lance d'abord SPG generate-mini-deck (ses 4 sous-étapes au niveau 1), PUIS lance le sous-agent brand-book avec les 6 PNG déjà présentes (skip intelligent de la section 07b → simple intégration des images existantes).

Dans les deux cas, le gate juste-à-temps SPG-portable reste valable. Penser aussi à : (a) overrider la voice "Camille Le Phare" du content-mapper par la voice réelle de la marque, (b) masquer `.export-btn` avant capture.

## Thème transverse

Tout skill qui « invoque un sous-skill qui invoque un sous-agent » est incompatible avec une exécution en sous-agent. À chaque branchement de skill-dans-skill dans BIG, vérifier la profondeur de délégation requise.
