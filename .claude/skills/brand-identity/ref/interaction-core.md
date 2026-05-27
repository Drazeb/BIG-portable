# Interaction — règles sémantiques (Critique TIER 2/3)

Règles universelles de comportement interactif. S'appliquent quel que soit le curseur A, le registre atmosphérique, le concept narratif. Elles ne dictent pas un look — elles dictent comment l'interface répond aux gestes de l'utilisateur.

**Portée** : importé par Phase 4 (styletile + artefact), Batch 2, Batch 3.

---

## États interactifs

## Designer les huit états

Chaque élément interactif a HUIT états à designer, pas un seul : Default, Hover, Focus, Active, Disabled, Loading, Error, Success. Livrer uniquement le default produit une interface qui paraît morte au contact. Les états ne sont pas optionnels — ils sont l'infrastructure invisible qui distingue un produit pro d'un mockup.

## Hover toujours visible

Boutons, liens, contrôles cliquables : toujours un état hover visuellement distinct du default. Sans changement perceptible au survol, l'élément paraît mort et l'utilisateur doute qu'il soit cliquable. Le hover ne doit pas reposer sur un seul indice (un seul changement de couleur léger), il combine plusieurs propriétés (voir `finition-elite-core.md` — Transitions multi-property).

## Hover seul interdit

Ne jamais conditionner une fonctionnalité au hover uniquement. Les utilisateurs touch n'ont pas de hover — un menu, une révélation, une action qui n'apparaît qu'au survol disparaît pour eux. Toujours offrir une alternative tactile équivalente (tap, bouton visible, geste découvrable).

## Skeletons plutôt que spinners

Préférer les skeletons (preview de la forme du contenu à venir) aux spinners. Le skeleton donne une attente cadrée — l'utilisateur voit la structure qui se prépare et patiente mieux. Le spinner ne donne aucune information sur le contenu, il ne fait que dire "ça charge". Les spinners restent acceptables pour les actions très courtes ou les chargements ponctuels (bouton submit), pas pour les zones de contenu.

## Optimistic UI à enjeu faible

L'optimistic UI (mise à jour immédiate avant retour serveur) est acceptable uniquement quand l'utilisateur peut annuler facilement et que le coût d'une erreur est faible (toggle d'un like, ajout à une liste, édition d'un nom). Interdit sur les actions à enjeu (paiements, suppressions définitives, confirmations légales) — l'utilisateur doit voir le serveur confirmer avant de croire que c'est fait.

---

## Forms et inputs

## Validation au blur

Valider un champ à la SORTIE du champ (blur), pas à chaque frappe. Valider à chaque frappe inonde l'utilisateur d'erreurs prématurées avant qu'il ait fini de taper. Erreurs affichées sous l'input concerné, jamais en haut de formulaire — l'utilisateur doit voir ce qui ne va pas là où il regarde.

## Placeholders donnent l'exemple

Les instructions de format passent par les placeholders (qui montrent un exemple concret du format attendu), pas par des labels longs ou des helpers verbeux. Expliquer un champ avec une note d'aide uniquement s'il n'est pas évident — un champ "Email" ou "Mot de passe" n'a pas besoin d'explication.

## Coller jamais bloqué

Ne jamais bloquer le coller (`onPaste preventDefault`) sur les inputs. Les utilisateurs collent des emails, des codes, des mots de passe, des numéros — c'est un comportement légitime et fréquent. Bloquer le paste signale du mauvais design défensif et frustre les utilisateurs réels pour rien.

## Submit actif puis spinner

Le bouton submit reste ACTIF jusqu'au début de la requête, puis affiche un spinner pendant la requête (et redevient actif ou affiche un état success ensuite). Ne jamais le griser en permanence en attendant que tous les champs soient parfaits — l'utilisateur veut voir que son geste a été pris en compte. Le grisage permanent est passif-agressif.

## États vides assumés

Gérer les états vides au niveau composant : `empty string`, `array vide`, `null` doivent rendre une UI cohérente, pas casser ou afficher du vide béant. Chaque liste, chaque tableau, chaque section dynamique a son empty state designé (illustration ou message + action principale). Un composant qui ne gère que le cas plein est un composant fragile.

---

## Modales, dropdowns, overlays

## Dropdowns hors du parent clippé

Anti-pattern : `position: absolute` sur un dropdown à l'intérieur d'un parent en `overflow: hidden` — le dropdown se fait couper. Utiliser `position: fixed` avec calcul de position, ou la Popover API moderne, pour que les overlays sortent toujours de leur conteneur. Vaut aussi pour les tooltips, menus contextuels, autocomplete.

## Undo plutôt que confirm

Préférer "supprimer immédiatement avec toast d'annulation" plutôt que dialogue de confirmation systématique. La confirmation est paresseuse et casse le flux pour 99% des cas où l'utilisateur sait ce qu'il fait. Le pattern undo respecte la vitesse de l'utilisateur. La confirmation reste réservée aux actions destructives DÉFINITIVES (suppression de compte, paiement, changement irréversible) — pas aux suppressions banales.

## Gestes découvrables

Les gestes (swipe, pinch, long-press) sont invisibles par nature — un utilisateur ne devine pas qu'il faut swiper. Toujours offrir une découvrabilité : révélation partielle au repos (le bouton swipe dépasse à 10%), onboarding court à la première utilisation, ou alternative tactile visible (un bouton classique qui fait la même action). Les gestes sont un raccourci pour les power users, pas la seule porte d'entrée.

---

## Touch et responsive

## Mobile-first par défaut

Architecture CSS mobile-first : styles de base écrits pour mobile, media queries `min-width` qui ajoutent de la complexité au desktop. C'est l'inverse de la pratique 2010s (desktop d'abord, on dégrade sur mobile). Le mobile-first force à hiérarchiser le contenu (qu'est-ce qui est essentiel ?) et à designer pour la contrainte la plus forte. Le desktop hérite ensuite des respirations supplémentaires.

## Tap-highlight intentionnel

Définir intentionnellement `-webkit-tap-highlight-color` sur les éléments tactiles — soit transparent (si le hover fait le travail), soit une couleur de marque cohérente. Laisser le défaut bleu/gris du navigateur signale un design qui n'a pas pensé au tactile. C'est un détail qu'on ne voit pas individuellement, mais qui distingue un produit fini d'un produit non fini.

## Scroll-margin sous nav sticky

Quand la page a une nav sticky, prévoir `scroll-margin-top` sur les ancres de heading pour qu'elles ne soient pas masquées par la nav lors d'un scroll-to-anchor. Sinon, cliquer sur un lien d'ancre fait disparaître le titre cible derrière la nav — l'utilisateur arrive sur le bon endroit mais ne le voit pas. Règle de robustesse, pas d'esthétique.

## Tester sur appareils réels

Discipline : tester sur appareils réels, pas seulement DevTools. Inclure un Android d'entrée de gamme dans la liste de test — les performances et le rendu varient drastiquement (animations qui ramènent, fonts qui rendent différemment, viewport qui se comporte autrement). Le simulateur ment sur la performance, jamais sur le rendu pixel. La vraie expérience se mesure sur le vrai matériel.

---

## Source et traçabilité

**Création** : ce fichier rassemble les règles sémantiques d'interaction (états, forms, overlays, touch) extraites du skill audit-slop. Les listes nominatives (cubic-bezier values, durées en ms, tailles de tap targets) vivent dans les gates Python associés, pas ici.

**Importé par** : Phase 4 (styletile + artefact), Batch 2, Batch 3 — via l'orchestrateur (pattern BIG : orchestrateur lit + injecte, subagent ne lit pas les refs directement).

## Dernière mise à jour

2026-04-26 — Création (~17 règles N1/N2 issues du skill audit-slop). Étape de l'intégration anti-slop côté interaction.
