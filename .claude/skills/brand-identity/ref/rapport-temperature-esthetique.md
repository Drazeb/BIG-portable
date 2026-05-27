# Rapport — Problème de température froide sur les style-tiles Camille (batch test 19 mars 2026)

## Contexte

Session de test du pipeline BIG sur la marque Camille (studio pitch deck & positionnement stratégique).
6 concepts narratifs testés en 2 batches, les 3 premiers poussés jusqu'aux style-tiles HTML.

### Fichiers concernés

- **Style-tiles** :
  - `/Users/charlesbezard/Library/CloudStorage/GoogleDrive-charles.bezard@gmail.com/Mon Drive/Claude Code/Brand Identity Generator/.claude/skills/brand-identity/outputs/test-camille-test-20260319-13383/camille-style-tile-concept-1.html` (La Chambre Sourde)
  - `/Users/charlesbezard/Library/CloudStorage/GoogleDrive-charles.bezard@gmail.com/Mon Drive/Claude Code/Brand Identity Generator/.claude/skills/brand-identity/outputs/test-camille-test-20260319-13383/camille-style-tile-concept-2.html` (Le Collimateur)
  - `/Users/charlesbezard/Library/CloudStorage/GoogleDrive-charles.bezard@gmail.com/Mon Drive/Claude Code/Brand Identity Generator/.claude/skills/brand-identity/outputs/test-camille-test-20260319-13383/camille-style-tile-concept-3.html` (Le Chromatogramme)

- **Dossier session** : `.claude/skills/brand-identity/outputs/test-camille-test-20260319-13383/`

- **Pitchs (qui ont dicté la direction visuelle)** :
  - `camille-pitch-c1.md`, `camille-pitch-c2.md`, `camille-pitch-c3.md` dans le même dossier

- **Profil esthétique (qui n'a PAS été transmis comme contrainte)** :
  - `camille-aesthetic-profile.md` dans le même dossier

---

## Le problème

Les 3 style-tiles sont sombres et froids :

| Concept | Température déclarée | Atmosphère | Palette dominante |
|---------|---------------------|------------|-------------------|
| C1 — La Chambre Sourde | Froide-neutre | Sombre | Noir #1C1C1E + gris + teal |
| C2 — Le Collimateur | Froide | Sombre | Noir #0A0A0F + blanc bleuté + cyan-menthe |
| C3 — Le Chromatogramme | Froide | Coloré mais froid | Bleu encre #1B2D45 + cyan + rouge signal |

Or, le brief et le scoping de Camille contenaient des signaux clairs de **température chaude** :

1. **Scoping, section Ventre Mou** : "n'importe quelle direction chaude, artisanale ou texturée sera immédiatement différenciante" — le DA recommande explicitement le chaud comme levier de ZAG contre le bleu-gris dominant du secteur.

2. **Scoping, section Diagnostic de Compatibilité Esthétique** : "Température chaude : cuivre, terre, vert botanique, crème — pas de bleu tech."

3. **Brief analysis** : "La DA devra incarner cette dualité : chaleur du nom propre + rigueur du service."

4. **Profil esthétique** : Les DEUX préférences (Blueprint et Futuristic Surrealism) déclarent une température chaude :
   - Blueprint : "chaud (cuivre, terre, crème)"
   - Futuristic Surrealism : "tend vers chaud via les matières instrumentales — cuivre, laiton, optique"

---

## Pourquoi c'est arrivé

### La mécanique exacte

À la Phase 3B-0 (sélection de la préférence esthétique par concept), l'utilisateur a dit : **"sans préférence stylistique"** pour les 3 concepts. C'est un choix légitime — il ne voulait pas orienter les concepts vers le Blueprint ou le Futuristic Surrealism.

Le système a alors fait ce qu'il est programmé à faire : il a mis la variable `{aesthetic_constraint_or_omit}` à vide dans le prompt des subagents pitch (phase-3b-design.md). Les subagents n'ont reçu **aucune consigne esthétique explicite**.

### Ce que les subagents ont reçu vs. ce qu'ils auraient dû percevoir

**Fichiers lus par les subagents pitch** :

| Fichier | Contient des signaux de chaleur ? | Les subagents les ont-ils utilisés ? |
|---------|----------------------------------|--------------------------------------|
| `camille-scoping.md` | **Oui** — section Ventre Mou ("direction chaude différenciante") + section 4 profil esthétique ("température chaude") | **Non** — traité comme contexte informatif, pas comme contrainte |
| `camille-brief-analysis.md` | **Oui** — "chaleur du nom propre" | **Non** — noyé dans 200 lignes d'analyse |
| `camille-context-clean.md` | **Non** — aucune mention de chaleur | N/A |
| `ref/bible-design-strategie.md` | **Non** | N/A |
| `ref/master-style-guide.md` | **Non** | N/A |
| `phases/phase-3b-design.md` | Variable `{aesthetic_constraint_or_omit}` = **vide** | Les subagents ont lu la section "CADRE DE COMPATIBILITÉ ESTHÉTIQUE" et vu qu'elle était vide → pas de contrainte |

### Le biais LLM sous-jacent

Sans contrainte de température explicite, les concepts à registre technique/scientifique convergent naturellement vers le froid/sombre :
- Chambre sourde → noir (silence = absence de lumière)
- Collimateur → noir (chambre optique = obscurité)
- Chromatogramme → bleu froid (laboratoire = froid analytique)

C'est un biais statistique du LLM : dans ses données d'entraînement, les univers "labo", "optique", "acoustique" sont massivement associés à des palettes froides. Sans garde-fou explicite, il va vers son association la plus forte.

---

## La cause racine : confusion entre "inspirations" et "guidelines"

Le problème n'est pas que l'utilisateur a dit "pas de préférence". Le problème est que le système traite le profil esthétique comme un bloc monolithique : soit on le passe en entier (les 2 inspirations + le transversal), soit on ne passe rien.

Or, le profil esthétique contient **deux types d'informations fondamentalement différentes** :

### Type 1 — Les inspirations esthétiques (optionnelles)
Ce sont les registres visuels spécifiques que le client aime :
- "Blueprint" (tracés techniques, cotes, annotations)
- "Futuristic Surrealism" (instruments impossibles, observatoires)

Ce sont des **sources d'inspiration créative**. Les activer oriente le concept vers un registre visuel spécifique. Ne PAS les activer est un choix créatif légitime — on veut que le concept trouve son propre registre visuel.

### Type 2 — Les guidelines transversales (toujours actives)
Ce sont les contraintes qui s'appliquent QUEL QUE SOIT le registre choisi :
- Température chaude (cuivre, terre, crème)
- Ce que le client veut éviter (bleu tech, rouge vif, flat générique, etc.)
- Signaux transversaux du scoping (direction chaude = ZAG vs. le ventre mou froid du secteur)

Ces guidelines ne sont PAS optionnelles. Elles viennent du brief et du client. Dire "pas d'inspiration Blueprint" ne signifie pas "ok pour du bleu froid".

### Situation actuelle vs. situation souhaitée

**Aujourd'hui** : Le fichier `aesthetic-profile.md` contient les deux types mélangés. La section "Ce que le client veut éviter" est transversale, mais la température chaude est enfouie dans chaque préférence individuelle. Quand on dit "aucune préférence", on perd TOUT — y compris les guidelines transversales.

**Ce qu'il faudrait** : Séparer clairement les deux types dans le fichier ET dans la mécanique de transmission aux subagents :

```
# Profil Esthétique — {brand}

## Guidelines transversales (TOUJOURS transmises)
### Température
- Chaud (cuivre, terre, crème) — pas de bleu tech
### Ce que le client veut
- Chaleur du nom propre + rigueur du service
- Direction chaude = différenciante dans ce secteur (ZAG vs. ventre mou froid)
### Ce que le client veut éviter
- Bleu tech/corporate
- Rouge vif (anti-référence)
- Flat générique, stock photos
- etc.

## Inspirations esthétiques (sélectionnables par concept)
### Inspiration 1 — "Blueprint"
[...]
### Inspiration 2 — "Futuristic Surrealism"
[...]
```

---

## Propositions

### 1. Restructurer le fichier `aesthetic-profile.md`

Séparer en deux sections clairement distinctes :
- **Guidelines transversales** : température, ce que le client veut/ne veut pas, signaux de chaleur du brief. Toujours transmises aux subagents, même si aucune inspiration n'est sélectionnée.
- **Inspirations esthétiques** : les registres visuels spécifiques (Blueprint, Futuristic Surrealism, etc.). Sélectionnables individuellement par concept.

### 2. Modifier la variable de transmission dans le prompt phase-3b-design.md

Au lieu d'une seule variable `{aesthetic_constraint_or_omit}`, utiliser **deux variables** :
- `{aesthetic_guidelines}` : **toujours remplie** si le profil esthétique existe (contient les guidelines transversales)
- `{aesthetic_inspiration_or_omit}` : remplie avec l'inspiration choisie, ou vide si "aucune inspiration"

### 3. Modifier la Phase 3B-0

Le choix utilisateur à la Phase 3B-0 porterait uniquement sur les **inspirations**, pas sur les guidelines :

> "Pour chaque concept, quelle **inspiration** activer ?"
> - Concept 1 : Blueprint / Futuristic Surrealism / **aucune inspiration**
> - Concept 2 : ...

Et les guidelines transversales seraient transmises automatiquement, sans question.

### 4. Enrichir la section transversale

La section "Ce que le client veut éviter" existe déjà dans le profil. Il faut y ajouter une section symétrique **"Ce que le client veut"** qui capture :
- La température souhaitée
- Les signaux de chaleur/humanité du brief
- Les qualités sensorielles transversales (artisanal, craft visible, etc.)

---

## Impact sur cette session

Pour les 3 style-tiles existants, deux options :
1. **Relancer les pitchs** avec les guidelines transversales injectées (température chaude, pas de bleu tech) → nouveaux style-tiles
2. **Ajuster les palettes directement** sur les style-tiles existants (remplacer les noirs/bleus froids par des teintes chaudes) — plus rapide mais moins profond (la composition et l'atmosphère resteraient "froides" dans leur structure)

L'option 1 est plus propre. L'option 2 est un patch.
