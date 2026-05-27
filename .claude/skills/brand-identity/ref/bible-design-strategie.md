# Bible Design & Stratégie — BIG System

Ce document est le **référentiel d'excellence**. Aucune proposition ne doit déroger à ces standards.

---

## 1. LES 5 PRINCIPES DU BRANDING MODERNE (FILTRE D'AUDIT)

Toute proposition doit être auditée selon ces 5 filtres :

| # | Principe | Description | Test |
|---|----------|-------------|------|
| 1 | **Différenciation** | Capacité à se détacher du "Ventre Mou" du secteur | "Est-ce qu'un concurrent pourrait utiliser ce design ?" → Si oui, rejet |
| 2 | **Scalabilité** | Efficacité du 16px (favicon) au 1920px (billboard) | "Est-ce lisible en petit ET impactant en grand ?" |
| 3 | **Clarté Cognitive** | Hiérarchie de l'information immédiate (Gestalt) | "En 3 secondes, l'utilisateur comprend-il la hiérarchie ?" |
| 4 | **Résonance Émotionnelle** | Alignement psychologique entre visuel et cible (ICP) | "Est-ce que l'ICP se sent compris en regardant ?" |
| 5 | **Intégrité Système** | Cohérence totale entre tous les points de contact | "Est-ce que chaque élément parle la même langue ?" |

---

## 2. FRAMEWORKS AVANCÉS

### 2.1 La Loi de la Gestalt
Utilisation de la **Proximité**, **Similitude** et **Continuité** pour guider l'œil. Chaque composition doit créer un chemin de lecture naturel, pas un labyrinthe.

### 2.2 Le Framework ZAG (Neumeier)
Identification de la **tendance dominante** du marché pour proposer un **contre-pied** proportionnel au score du Curseur B.
- Quand tout le monde zig, tu zag
- Le Zag n'est pas gratuit : il doit être fondé sur la **conviction** du brief (point 08)

### 2.3 Affordance Cognitive
Les éléments de design (boutons, cartes, composants) doivent **suggérer leur fonction par leur forme**. Zéro ambiguïté sur l'interactivité.

---

## 3. SYSTÈME DOUBLE CURSEUR (DÉCOUPLÉS)

Chaque variante (VAR) est calibrée sur **deux axes indépendants** (score de 1 à 3).
Les axes sont **découplés** : A=3 + B=1 est une combinaison valide.

### AXE A — AUDACE CRÉATIVE (Structure & Forme)

Les valeurs ci-dessous sont des **GUIDES D'INTENSITÉ**, pas des recettes. Le concept narratif détermine QUELS paramètres sont poussés et COMMENT.

| Score | Label | Typographie | Layout | Surface |
|-------|-------|-------------|--------|---------|
| **1** | Prudent | Type-scale ≤ 1.200, pairings classiques, hiérarchie lisible | Grille structurée, alignement clair, espacement généreux | Radius et ombres cohérents, gradients simples |
| **2** | Décalé | Type-scale 1.250–1.333, un display à caractère fort, contrastes marqués | Asymétries contrôlées, ruptures de rythme intentionnelles | Surface expressive — le concept choisit les techniques |
| **3** | Rupture | Type-scale ≥ 1.414, display expérimental ou variable font, hiérarchie non-conventionnelle | Layout expérimental, negative space radical, grilles libres | Surface radicale — toute technique CSS est légitime |

**Note** : Un concept A=1 peut avoir des radius à 0px s'il est chirurgical. Un concept A=3 peut avoir des ombres subtiles s'il joue sur d'autres axes de rupture. La cohérence vient du CONCEPT, pas du tableau.

### AXE B — DIFFÉRENCIATION CONCURRENTIELLE (ZAG)

| Score | Label | Palette | Imagerie | Ton |
|-------|-------|---------|----------|-----|
| **1** | Mimétisme | Codes couleur attendus du secteur, palette "safe" | Imagerie conventionnelle du marché, stock prévisible | Vocabulaire corporate, réassurance maximale |
| **2** | Distinction | Pivot chromatique sur 1 couleur inattendue, reste cohérent avec le secteur | Mix d'imagerie sectorielle et de direction artistique originale | Voix distinctive sur 1 axe (ex: humour, ou poésie, ou franchise) |
| **3** | ZAG (Contre-pied) | Palette en opposition radicale aux leaders du secteur | Direction artistique en rupture totale (ex: illustration là où tous font de la photo) | Voix radicalement différente, rupture assumée avec les conventions |

### Flow des curseurs
1. **L'utilisateur choisit UNE SEULE combinaison A×B** (ex: A=2, B=3) après avoir validé la Tension de Marque en Phase 2
2. **BIG génère 3 interprétations créatives** en Phase 3, toutes calibrées sur cette MÊME combinaison A×B
3. Les 3 interprétations sont visuellement distinctes (palettes différentes, typographies différentes, atmosphères différentes) mais partagent le **même niveau d'audace** (A) et le **même niveau de différenciation** (B)

**Exemple** : Si l'utilisateur choisit A=2 × B=3, les 3 concepts proposeront tous une audace "Décalée" (type-scale 1.250–1.333, asymétries contrôlées) et une différenciation "Contre-pied" (palette en rupture avec le secteur, imagerie non-conventionnelle) — mais avec des univers visuels distincts

---

## 4. LA TENSION DE MARQUE

La Tension est le **cœur créatif** de l'identité. C'est l'union de deux attributs apparemment contradictoires qui crée une identité **impossible à copier**.

### Protocole de synthèse
1. Extraire du brief les deux pôles (point 09)
2. Formuler la tension sous la forme : **"[Attribut A]" + "[Attribut B]"**
3. Vérifier que la tension est **résoluble visuellement** (chaque pôle peut s'exprimer dans le design)
4. La tension alimente **directement** les 3 concepts de la Phase 3

### Test de qualité
- Si la tension est évidente (ex: "Modernité + Innovation") → **REJET** — c'est du Ventre Mou
- Si la tension est irrésoluble (ex: "Invisible + Explosif") → **REJET** — c'est un paradoxe stérile
- Si la tension crée une **synthèse visuelle inattendue** → **VALIDÉ**

---

## 5. LE VENTRE MOU (ANTI-PATTERN)

Le "Ventre Mou" est l'ennemi n°1. C'est le design que **tout le monde fait** dans un secteur donné.

### Comment l'identifier
- Analyser les 3-5 concurrents principaux
- Lister leurs codes communs (couleurs, typos, imagerie, ton)
- Ces codes communs = le Ventre Mou

### Comment l'éviter
- Chaque proposition doit passer le test : "Un concurrent pourrait-il utiliser exactement ce design ?"
- Si oui → le Curseur B doit monter d'au moins 1 point
- Le degré d'éloignement est **proportionnel** au score B choisi
