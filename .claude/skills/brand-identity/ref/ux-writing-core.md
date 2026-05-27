# UX-writing & copy — Core (Critique TIER 2/3)

Règles sémantiques universelles d'UX-writing et de micro-copy. Lues par les Critiques spécialisés (audit-slop, audit-elite) lors de la phase de jugement, **pas** par le Designer en mode CRÉATION. Les listes nominatives (filler words, fake names, Lorem Ipsum, avatars génériques) vivent dans les gates Python — pas dans ce fichier.

**Portée** : critères d'audit transverses sur la copy des style-tiles HTML, artefacts, batchs. S'applique quel que soit le curseur A, le registre atmosphérique, le concept narratif. Importé par les Critiques de Phase 4 (styletile + artefact), Batch 2, Batch 3.

---

## §1 — Boutons et actions

### Verbe + objet, pas de générique
Les libellés de boutons combinent **un verbe d'action et son objet** (la chose sur laquelle l'action porte). Les libellés génériques sont à proscrire — ils cachent l'action derrière une formule passe-partout. Un bouton bien rédigé permet de comprendre ce qui va se passer sans relire le contexte autour.

### Voix active sur les actions
Les libellés sont en **voix active** ("Installer le CLI"), jamais en voix passive ("Le CLI sera installé") ni en formulation impersonnelle. La voix active responsabilise l'action et raccourcit le libellé.

---

## §2 — Erreurs et feedback

### Formule en trois temps
Un message d'erreur répond à trois questions dans cet ordre : **Quoi s'est passé ? Pourquoi ? Comment corriger ?** Un message qui ne donne que l'un des trois est un message dégradé. Un message générique sans cause ni action est un échec produit.

### Ton compatissant, jamais accusatoire
L'utilisateur n'est **jamais blâmé** dans le message d'erreur. Reformuler du côté du système ou de la contrainte ("Ce champ est requis") plutôt que du côté de l'utilisateur ("Vous avez fait une erreur"). Le ton est compatissant et factuel, pas culpabilisant.

---

## §3 — États vides et états de chargement

### États vides en trois temps
Un état vide se compose de trois éléments : **reconnaître l'absence, expliquer la valeur attendue à venir, proposer une action claire**. Un état vide qui ne fait que constater l'absence ("Aucun élément") est un échec d'onboarding et de pédagogie.

### Chargement spécifique au contexte
Le libellé de chargement est **spécifique à l'opération en cours** ("Sauvegarde en cours…", "Préparation de l'export…") plutôt que générique. Sur les attentes longues : ajouter un indicateur de progression ou une contextualisation de ce qui se passe. Un loader générique sans contexte fait douter l'utilisateur du bon fonctionnement.

---

## §4 — Voix et ton

### Voice constant, Tone adaptatif
La **Voice** est la personnalité de marque — elle reste constante d'une surface à l'autre. Le **Tone** s'adapte au contexte : empathique sur les erreurs, bref sur le succès, rassurant sur les attentes longues, factuel sur les confirmations. Mélanger voice et tone produit une marque qui sonne tantôt corporate tantôt désinvolte sans cohérence.

### Deuxième personne
Adresse à l'utilisateur en **deuxième personne** ("vous pouvez installer", "votre projet"). Préférable à la première personne plurielle ("nous recommandons d'installer") qui crée une distance corporate, et au passif neutre qui efface la relation.

### Casse Title Case sur titres et boutons
Les titres et libellés de boutons suivent une **convention de casse cohérente** sur l'ensemble du produit (Title Case ou sentence case selon le ton de la marque, mais une seule convention par marque). L'incohérence de casse entre sections est un marqueur de produit non finalisé.

---

## §5 — Cohérence terminologique

### Un terme par concept
Choisir **un terme par concept** et l'imposer partout. Alterner entre Supprimer / Effacer / Mettre à la corbeille pour la même action est un marqueur de produit sans glossaire de marque. La cohérence terminologique est un marqueur élite — l'incohérence est un signal de finition absente.

### Pas de redondance
Pas de répétition entre niveaux d'information. **Si le titre explique, l'intro est redondante. Si le bouton est clair, ne pas le réexpliquer en sous-texte.** La redondance dilue la hiérarchie et alourdit la lecture.

### Chiffres séparés du texte
Séparer les chiffres du texte ("Nouveaux messages : 3") plutôt que de les insérer dans une phrase ("Vous avez 3 nouveaux messages"). Les abréviations chiffrées sont à éviter pour des raisons d'internationalisation et de robustesse.

---

## §6 — Forms et inputs (copy)

### Placeholders comme exemple, pas comme label
Les placeholders **terminent par un caractère de suite** et montrent un pattern d'exemple — ils ne remplacent jamais le label. Un placeholder qui sert de label disparaît dès que l'utilisateur clique et casse l'accessibilité.

### Types d'input et inputmode appropriés
Les types d'input (`email`, `tel`, `url`, `number`) et l'attribut `inputmode` sont choisis selon la nature de la donnée attendue. Un champ téléphone en type `text` est un défaut de finition mobile.

### Autocomplete bien renseigné
L'attribut `autocomplete` est renseigné avec la valeur sémantique correcte sur tous les inputs concernés (email, name, address, etc.). Sur les champs hors authentification où le password manager parasite l'expérience : l'attribut est désactivé explicitement.

### Spellcheck désactivé sur identifiants techniques
Le spellcheck est désactivé sur les emails, codes, usernames, identifiants techniques. Sans cela, le navigateur souligne les valeurs valides comme des fautes — défaut de finition immédiatement visible.

---

## Règles SKIP (déjà couvertes ailleurs)

- **R-070 (chiffres séparés du texte)** : conservée mais reformulée sans énumération nominative — la version source contenait un exemple précis qui sortait du périmètre N1/N2.
- **R-174 (& over and en espace contraint)** : SKIPPÉE. Règle micro-typographique de niveau substituable trop précise (équivalent N3 implicite par exemple unique). Si elle remonte par audit, à intégrer comme principe plus large de typographie économe en espace contraint.
- **Filler words, fake names, Lorem Ipsum, avatars par défaut** : déjà couverts par `anti-slop-blacklist-core.md §5` et le gate Python `phase4-blacklist-gate.py`. Pas de duplication ici.

---

## Source et traçabilité

**Origine** : règles sémantiques extraites du skill `audit-slop` (R-063+R-145, R-064+R-146, R-065, R-066, R-070, R-071, R-072, R-073, R-077, R-143, R-144, R-150, R-151, R-152, R-155, R-156, R-173), reformulées en Niveau 1-2 selon `anti-slop-formulation-guide.md`. Fusions opérées : R-063+R-145 (specific button labels) et R-064+R-146 (errors what/why/how) — règles équivalentes dans la source.

**Lecteurs prévus** : Critiques TIER 2/3 (audit-slop, audit-elite). Le Designer en mode CRÉATION ne lit PAS ce fichier — il reçoit les principes via les phases 4 et batchs sous forme synthétisée.

## Dernière mise à jour

2026-04-26 — Création. Étape 3 du plan d'intégration anti-slop (Vague 2).
