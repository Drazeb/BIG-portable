# Patterns de composition web actuels — Détail opérationnel (2024–2026)

> Rapport de recherche approfondie. Destiné à un système de génération automatique d'identités de marque produisant des style-tiles HTML en 3 sections : Hero, Composant UI témoin, Section Atmosphère. Toutes les règles sont transversales sauf mention explicite.

***

## Partie 1 — Hovers et interactions : ce qui est actuel concrètement

### 1.1 Philosophie générale : le hover comme "confirmation systématique"

En 2024–2026, le hover n'est plus un ornement ni une révélation : c'est une **confirmation non bloquante**. Toute information essentielle doit déjà être visible ; le hover amplifie ou confirme sans transformer. Ce changement de philosophie est documenté par plusieurs praticiens : les micro-interactions "sont là pour guider, rassurer et ravir — sans être intrusives". La cohérence avec le design system est désormais une contrainte forte : un même vocabulaire d'effets (amplitudes, timings, easings) doit s'appliquer à tous les composants.[^1][^2][^3]

Ce qui distingue fondamentalement le hover 2025 du hover 2020 :

| Dimension | Hover 2020 | Hover 2025 |
|-----------|-----------|-----------|
| Rôle | Décoratif ou révélateur d'info cachée | Confirmation d'état, signal non bloquant |
| Amplitude | Large (gros zooms, rotations, glows) | Subtile (≤ 4 px déplacement, ≤ 1.05 scale) |
| Cohérence | Variable selon composant | Systématique, piloté par design system |
| Accessibilité | Ignorée (hover desktop-only accepté) | Requise : media query `hover: hover` + `prefers-reduced-motion` |
| Info cachée | Fréquente (tooltips critiques, texte caché) | Interdite pour contenu essentiel |

Sources :[^2][^3][^4][^1]

***

### 1.2 Catalogue des hovers par type d'élément

#### Boutons (primaires et secondaires)

- **Changement de fond** : variation de luminosité ou saturation dans la même teinte (bleu → bleu légèrement plus sombre ou plus clair). Jamais de changement de teinte complet sauf cas de branding très fort.[^5]
- **Variation de profondeur** : soit augmentation légère de l'ombre (élévation +1 niveau) pour un effet "lift", soit au contraire compression (ombre réduite + translation Y +1–2 px) pour simuler un "press".[^5]
- **Variation de bordure** : apparition ou accentuation d'un très fin outline (1 px), surtout sur les boutons ghost ou secondary.[^2][^5]
- **Durée typique** : 120–180 ms, easing ease-out ou cubic-bezier "standard matériel".[^6][^1]

**Règle de génération** : `button:hover = même teinte ± luminosité + shadow ± 1 niveau + border-color accentuée. Duration : 150ms ease-out. Aucun changement de taille de texte ni de layout.`

#### Cards

- **Scale très léger** : 1.00 → 1.02–1.03. Ne doit jamais déborder de la grille ni déclencher de reflow des éléments voisins.[^7][^2]
- **Lift** : combinaison shadow augmentée (level +1 ou +2) + translation Y de –2 à –4 px.[^8][^6]
- **Accentuation de bordure** : si la card a un outline, il gagne en contraste (ex. `rgba(0,0,0,0.08)` → `rgba(0,0,0,0.15)`).[^2]
- **Révélation de CTA secondaire** : l'action secondaire (lien "voir plus", icône de navigation) passe de semi-transparent (opacity 0.5) à visible (opacity 1). Elle **existe déjà dans le DOM** — elle n'est pas cachée.[^3][^6]
- **Image de fond ou de couverture** : léger zoom (scale 1.0 → 1.05 sur l'image seule, pas sur la card entière).[^9]

**Règle de génération** : `card:hover = scale 1.02 + shadow +1 + translateY(-3px) + border-opacity + 15%. CTA secondaire : opacity 0.5 → 1. Image interne : scale 1.05. Duration : 200ms ease-out. Aucun reflow du layout parent.`

#### Liens de navigation et liens textuels

- **Soulignement animé** : le plus courant en 2024–2025. Le soulignement apparaît au hover, souvent "tiré de gauche à droite" ou "du centre vers les bords".[^3][^7]
- **Offset du underline** : 2–4 px sous le texte, pas collé à la baseline (perception plus propre).[^3]
- **Changement de couleur texte** : nuance légère (ex. 80% opacité → 100%, ou teinte légèrement différente).[^2]
- **Dans les menus principaux** : fond léger derrière l'item hover (rectangle de fond très pâle), sans décalage des autres items.[^10]

**Règle de génération** : `nav-item:hover = underline slide-in (left→right) + text-color +opacity. Background pill optionnel. Duration : 150ms. Aucun déplacement d'items voisins.`

#### Lignes de tableau et listes interactives

- **Highlight de ligne** : fond légèrement teinté sur toute la largeur de la ligne (ex. `rgba(brand-color, 0.04)` ou `#F5F5F5` en thème clair).[^2]
- **Révélation d'actions** : icônes d'actions (éditer, supprimer, plus) passent de `opacity: 0` à `opacity: 1`, **sans changer de position**.[^2]
- **Curseur** : passage à `cursor: pointer` pour les lignes cliquables, `cursor: default` pour les lignes non actionnables.[^3]

**Règle de génération** : `table-row:hover = background-tint (brand/04) + action-icons opacity 0→1 (in-place). Duration : 100ms.`

***

### 1.3 Hover contextuel (élément A affecte un élément B distant)

Le hover contextuel — où le survol d'un élément modifie l'état d'un autre élément distant — est un pattern **légitime et bien représenté dans les collections Awwwards 2024–2025**, à condition de respecter des contraintes précises.[^11]

**Exemples documentés sur Codrops 2025 :**
- Grille d'images interactive où chaque card scale selon sa distance au curseur (plus proche = plus grande, effet de "lentille" sur la grille).[^12]
- Grid to preview : hover sur une card produit déplace les cards voisines vers l'intérieur et révèle un panneau de preview via clip-path animé.[^13]
- Portfolio avec flip 3D de cards au scroll + hover, avec media query `hover: hover` pour cibler seulement les appareils souris.[^4]

**Conditions de validité :**
- L'élément affecté (B) doit être **spatialement proche** de A (dans la même section, idéalement dans le même groupe visuel).[^12][^3]
- L'état "au repos" de B doit être **compréhensible sans hover** (information accessible par défaut).[^3]
- Ce pattern est adapté aux **galeries, grilles de produits, listes de projets** — pas aux composants fonctionnels (formulaires, dashboards).[^13][^3]

**Règle de génération** : `hover-contextuel = autoriser dans hero galleries et grilles de composants témoins de type "projets/produits". Interdire dans les formulaires, tables de données, dashboards.`

***

### 1.4 Curseurs dynamiques et custom cursors

Les curseurs dynamiques (cursor qui change de forme ou de taille selon le contexte) sont documentés comme trend 2025. Leur usage dans les sites Award est réel mais sectoriellement situé :[^14][^15]

- **Légitimé pour** : portfolios d'agences créatives, sites de luxe, expériences éditoriales, collections Awwwards "Hovers, Cursors and Cute Interactions" (466 items).[^11]
- **À éviter pour** : SaaS B2B, dashboards fonctionnels, sites de santé, e-commerce transactionnel.
- **Patterns courants** : cursor qui grossit au hover sur images (grow), cursor qui change de couleur selon la section, cursor custom qui remplace l'arrow par un cercle ou une forme de marque.[^15][^14]

**Règle de génération** : `custom-cursor = activer uniquement pour secteurs créatifs/luxe/culturels. Désactiver pour SaaS B2B, santé, industrie.`

***

### 1.5 Amplitudes et timings : le consensus pro

D'après les sources praticiens (Nacar Design, Stan Vision, Appnova, JustinMind) :[^1][^7][^6][^3]

| Type d'interaction | Durée recommandée | Scale max | Translation max |
|---|---|---|---|
| Hover bouton | 120–180 ms | — | 2 px |
| Hover card | 180–220 ms | 1.03 | 4 px |
| Hover lien | 120–160 ms | — | — |
| Hover ligne tableau | 80–120 ms | — | — |
| Transition de section | 200–350 ms | — | — |
| Hover contextuel (grid) | 200–300 ms | 1.08–1.15 (card individuelle) | — |

**Règle absolue** : aucune interaction directe (hover, press) ne doit dépasser 300 ms. Au-delà, la réponse est perçue comme latente, pas comme une intention.[^6][^1]

***

## Partie 2 — Footers et sections de conclusion

### 2.1 Anatomie du footer actuel (2024–2026)

Les pratiques documentées sur Awwwards, pages.report, Eleken et Muffin Group convergent vers une structure en **deux zones distinctes** : un pré-footer éditorial et un footer structurel.[^16][^17][^18][^19]

```
┌──────────────────────────────────────────────┐
│  PRÉ-FOOTER                                  │
│  (section autonome avant le footer réel)     │
│  → CTA fort, ou manifeste, ou evidence       │
│  → Fond contrasté, viewport partiel (50-80%) │
└──────────────────────────────────────────────┘
┌──────────────────────────────────────────────┐
│  FOOTER STRUCTUREL                           │
│  → 2-3 colonnes de liens                    │
│  → 1 bloc brand/editorial                   │
│  → Légal minifié                             │
└──────────────────────────────────────────────┘
```

***

### 2.2 Patterns de pré-footer (spécifiquement 2024+)

**Pattern A — Pré-footer CTA fort**

- Un bloc occupant 50–80% de hauteur viewport, fond contrasté (couleur de marque pleine, très foncé ou très clair par rapport à la section précédente).[^17][^18][^19]
- Composition : heading grand (H2 ou H1 contextuel), sous-titre ou phrase courte (max 1–2 lignes), 1 CTA principal dominant (bouton ou lien large).[^18][^17]
- Principe : "les utilisateurs qui n'ont pas encore décidé arrivent en bas de page — c'est le deuxième moment de conversion".[^17]
- Exemple observé : **Karma** place un second CTA identique en footer sur chaque page ; **pages.report** déploie un CTA "See all 368+ landing pages" juste au-dessus du footer structurel.[^18][^17]

**Règle de génération pour section Atmosphère** : `pré-footer = 1 heading fort (H2, 40–72px) + 1 phrase (max 2 lignes) + 1 CTA. Fond contrasté vs section précédente. Hauteur min 40vh.`

**Pattern B — Pré-footer manifeste / signature**

- Bloc plein ou demi-écran avec une phrase manifeste (ton assertif, présent, premier ou deuxième personne).[^20][^21]
- Quelques exemples typiques : "Let's build something meaningful.", "Every brand deserves clarity.", "Designed for what comes next."
- Accompagné éventuellement d'une signature (nom de marque en grand, ville, date de fondation).[^20]
- Footer structurel réduit à quelques lignes sous ce bloc.[^20]

**Pattern C — Pré-footer evidence + invitation**

- Bloc rassemblant des preuves sociales (logos, chiffres, métriques) + un CTA d'invitation (démo, contact, newsletter).[^18][^20]
- Composition en grille 2 colonnes ou bento : à gauche les preuves, à droite l'invitation.[^20]

***

### 2.3 Compositions de footer structurel actuelles

**Pattern 1 — "Typographic grid" (2024+)**

Documenté comme footer excellence dans les exemples de référence 2024 : 4 colonnes avec titre de section + liens, hiérarchie typographique claire (titre colonne 16–18 px, liens 13–14 px), grille visible (séparateurs horizontaux fins).[^16][^20]

**Pattern 2 — Footer minimaliste fonctionnel**

- 3 éléments max : (1) bloc brand (logo + baseline ou email), (2) liens essentiels (5–8), (3) légal (copyright, terms, 10–11 px).[^22][^17]
- Fond foncé ou fond de marque, contraste avec le reste de la page.[^23][^22]

**Pattern 3 — Footer modulaire en grille avec bordures**

- Grille alignée sur le système global, avec bordures fines (1 px) qui découpent les modules.[^24][^20]
- Cohérence visuelle forte avec le reste du layout (même grid, même bordures).[^24]

***

### 2.4 Ce qui est spécifiquement 2024+ vs intemporel

| Élément | Intemporel | Spécifiquement 2024+ |
|---|---|---|
| Liens de navigation en footer | ✓ | — |
| Contact/légal | ✓ | — |
| Pré-footer comme section autonome | — | ✓ |
| Footer avec grilles visibles/bordures | — | ✓ |
| Micro-interactions sur liens footer | — | ✓ |
| Manifeste/signature comme conclusion | — | ✓ |
| Grande typographie dans le pré-footer | — | ✓ |
| Mega-footer sitemap complet | ❌ daté | — |

***

## Partie 3 — Composants UI : ce qui "sent" 2025

### 3.1 Principes transversaux de hiérarchie interne

Un composant UI "sent" 2025 quand sa hiérarchie interne est **lisible sans effort en 3 secondes**. Le Nielsen Norman Group documente la règle des 3 niveaux hiérarchiques avec des variations maximales de 3 tailles et 3 niveaux de contraste :[^25]

```
Niveau 1 — Header du composant (15–20 % hauteur)
  → Titre principal + méta (statut, période, filtre actif)
  → Plus grand, plus contrasté
  → Fond légèrement teinté ou séparé

Niveau 2 — Contenu principal (60–70 % hauteur)
  → Données, graphique, liste, tableau
  → Zone dominante

Niveau 3 — Actions/détails (10–20 % hauteur)
  → Boutons, liens secondaires, contrôles
  → Plus petits, alignés à droite ou en bas
```

Sources :[^26][^27][^25]

**Règle de génération** : `composant.layout = 3 niveaux. Ratio vertical approximatif : 15% / 65% / 20%. Niveau 1 : contraste max. Niveau 3 : contraste min.`

***

### 3.2 Proportions et asymétrie interne

Les composants "datés" ont des proportions uniformes (colonnes égales, cellules identiques, espacements uniformes partout). Les composants actuels introduisent une **asymétrie intentionnelle** :

- **Taille ∝ importance** : le champ ou la métrique principale occupe plus d'espace que les secondaires. Pas de grille 3×3 de KPI identiques.[^27][^26]
- **Colonne principale dominante** : dans un composant à colonnes (ex. : fiche, formulaire), la colonne de l'info principale fait 55–70% de la largeur ; les colonnes secondaires, 30–45%.[^26]
- **Hiérarchie de graisse typographique** : au minimum 3 niveaux distincts (ex. : 700 / 500 / 400) — mais jamais plus de 3 dans un même composant.[^28][^25]

**Règle de génération** : `composant.colonnes = asymétrique (60/40 ou 70/30) pour composants narratifs. Symétrique (50/50 ou 33/33/33) uniquement pour comparaisons explicites.`

***

### 3.3 Densité d'information : le bon niveau

La tension entre minimalisme et densité est documentée et résolue par la littérature récente : **la densité est acceptable si la structure est maîtrisée**.[^29][^30][^31]

Le système AWS Cloudscape (documentation référence) propose deux modes explicites :[^31]
- **Comfortable** : hauteur de ligne 40–52 px, padding généreux, pour lecture et navigation.
- **Compact** : hauteur de ligne 28–36 px, spacing réduit, pour données intensives.

La Master CAWEB synthétise le consensus NNG :[^29]
> "Minimalism earns attention. Density earns confidence and speed. The strongest UX designs achieve both by aligning structure, culture and intent."

Pour les **composants UI témoins** dans un style-tile :
- Choisir le mode "comfortable" pour les composants narratifs (timelines, fiches, formulaires).
- Choisir "compact" pour les composants de données denses (dashboards, tableaux).
- Dans les deux cas : **padding minimum 8–12 px autour de chaque unité textuelle**.[^32][^33]

**Règle de génération** : `composant.densité = comfortable pour composants narratifs (timeline, fiche, stepper). Compact pour dashboards et tableaux. Padding min 8px autour de toute unité textuelle. Max 2 niveaux d'info côte à côte sans séparation.`

***

### 3.4 Data visuelle dans les composants

Le pattern 2024–2025 est clairement documenté : **typographie brute + badges pour les données simples, graphiques simples pour les tendances**.[^34][^27][^26]

**Ce qui "sent" 2025 :**
- Statuts et catégories → **badges textuels** (fond teinté léger + texte + éventuellement point/icône). Pas de jauges ou d'indicateurs complexes pour des statuts.[^27][^26]
- Métriques principales → **grandes valeurs typographiques** (chiffre en bold/semibold, label en small/regular dessous). Pattern dit "stat block".[^26]
- Tendances → **sparklines inline** (graphique miniature intégré dans la ligne ou dans le stat block), 40–80 px de large, sans axes ni labels.[^27]
- Alertes/priorités → **couleur codée parcimonieusement** : une seule couleur "alerte" (rouge ou ambre), une seule couleur "positive" (vert), tout le reste neutre.[^25][^26]
- Données complexes → **1 graphique max par composant**, type simple (barres, lignes, donut minimal sans légende externe).[^27]

**Ce qui "sent" daté :**
- Jauges circulaires / gauges pour des pourcentages simples (pattern très 2016–2020).
- Gros graphiques avec axes, légendes, tooltips partout dans un composant témoin.
- Indicateurs colorés partout sans hiérarchie (chaque ligne a sa couleur).

**Règle de génération** : `composant.data = badge textuel pour statuts. Stat block (big number + label) pour métriques. Sparkline pour tendances. Max 1 graphe. Couleur alerte = 1 max.`

***

### 3.5 Bordures et séparations internes

Les patterns observés sur les sites et design systems de référence 2024–2025 :[^31][^24][^26]

**Ce qui est actuel :**
- **Ligne fine fonctionnelle** : 1 px, gris très clair (`#E5E5E5` en thème clair), uniquement entre zones fonctionnellement distinctes (header vs contenu, colonne actions vs contenu).[^24][^26]
- **Fond différencié** : header du composant sur fond légèrement teinté (`gray-50` ou `brand-50`), corps sur fond blanc/neutre. Crée une séparation sans ligne.[^26][^24]
- **Espacement comme séparateur** : la proximité/distance remplace avantageusement les lignes dans les groupes d'items liés.[^32][^25]
- **Contour externe discret** : ombre légère (level 1 ou 2) ou bordure fine pour délimiter le composant dans la page.[^35]

**Ce qui est daté :**
- Lignes de séparation entre chaque ligne d'une liste (trop de bruit visuel).
- Nombreuses bordures à différentes opacités sans système.
- Fond de composant très coloré/gradient.

**Règle de génération** : `composant.bordures = max 2 types de séparation interne (soit fond teinté, soit ligne 1px). Contour externe = ombre level-1 ou bordure 1px. Interdire séparateur entre chaque ligne d'une liste à moins de 5 items.`

***

### 3.6 Récapitulatif — Les 5 marqueurs d'un composant "2025"

| Marqueur | Description | Source |
|---|---|---|
| Hiérarchie en 3 couches | Header distinct / contenu dominant / actions retirées | [^25][^26] |
| Asymétrie proportionnelle | Taille des éléments proportionnelle à leur importance | [^27][^26] |
| Data brute en typographie | Stat blocks + badges + sparklines, pas de jauges | [^27][^34] |
| Densité intentionnelle | Comfortable ou Compact selon contexte, jamais par défaut | [^29][^31] |
| Séparations fonctionnelles | Fond teinté + ligne fine, jamais décoratifs | [^24][^26] |

***

## Partie 4 — Transitions entre sections

### 4.1 Les 3 patterns de transition valides en 2025

**Pattern 1 — Bord droit + changement de fond**

Le plus répandu dans les sites de référence et le plus "sûr" pour un générateur automatique.[^36][^24]

- Sections séparées par un simple changement de `background-color`.
- Palette typique : blanc → gris très léger (`#F8F9FA`), ou blanc → fond de marque très pâle.
- Espacement vertical généreux (padding top/bottom 80–120 px).[^37][^24]
- Peut être renforcé par une ligne horizontale fine (1 px) en bordure de section.

**Règle de génération** : `section-transition.clean = background-change + padding-vertical 80-120px. Optionnel : border-top 1px.`

***

**Pattern 2 — Overlap modéré (layered depth)**

Documenté comme trend fort 2025 par Appnova : "websites are moving away from flat, grid-locked layouts. Layered depth uses overlapping images, text and backgrounds to create a sense of dimension".[^38]

Variants :
- **Card qui déborde** : un composant (card, cluster) dépasse de 24–64 px dans la section suivante, créant une continuité visuelle.[^38][^36]
- **Sticky image + scroll texte** : image fixée à gauche pendant que du texte défile à droite (pattern "sticky panels"). Fréquent sur les sites de produit.[^39][^40]
- **Z-index layering** : section suivante passe "par-dessus" la précédente grâce à une ombre et un z-index supérieur.[^38]

**Contraintes d'usage** :
- L'overlap doit rester **cadré par la grille** (alignement latéral conservé).[^38]
- Maximum 1–2 overlaps par page (risque de chaos visuel si multiplié).[^38]
- Tester impérativement la version mobile (les overlaps peuvent devenir des bugs visuels).[^38]

**Règle de génération** : `section-transition.overlap = 1 composant max déborde de 24-64px. Conserver l'alignement de grille. Utiliser pour hero→section1 uniquement dans les style-tiles.`

***

**Pattern 3 — Continuité + variation de structure**

Même couleur de fond sur plusieurs sections consécutives, séparation par :
- Variation du layout (1 colonne → 2 colonnes → bento).[^24]
- Variation typographique forte (heading size, weight).[^41][^42]
- Ligne horizontale fine ou espace vertical augmenté.[^43][^24]

Ce pattern est particulièrement adapté aux pages de contenu éditorial où la rupture de fond viderait la fluidité narrative.[^36][^43]

***

### 4.2 Patterns de transition datés à bannir

| Pattern | Problème | Période dominante |
|---|---|---|
| Vagues SVG / clip-path diagonales génériques | Détachées de l'identité, associées aux templates bas de gamme | 2016–2020 |
| Scroll-jacking forcé (chaque scroll = une slide) | Frustrant, inaccessible, problèmes performance | 2014–2019 |
| Parallax lourd (vitesses différentes partout) | Nausée, accessibilité, performance mobile | 2014–2019 |
| Zigzags décoratifs / bordures en angle | Gimmick, pas de lien avec le contenu | 2015–2021 |

Sources :[^44][^45][^24]

***

### 4.3 Le pattern "Awwwards-grade" : transitions de page entière

Pour les sites visuellement ambitieux (agences créatives, portfolios), Awwwards recense 366 exemples de transitions entre pages ou états, dont les plus courants en 2024–2025 :[^46]

- **Mask reveal** : une forme masque la transition (fade via SVG clip-path).[^47][^46]
- **Scale + fade** : la page courante scale-down légèrement et fade, la suivante scale-up.[^46]
- **View Transitions API** : la nouvelle API CSS native pour les transitions entre documents, documentée par Smashing Magazine comme "bonne alternative aux SPA basées sur du JS lourd".[^48]

**Pour un générateur automatique** : ces transitions sont appropriées pour les style-tiles de secteurs créatifs/culture/luxe uniquement. Pour SaaS/industrie/santé, privilégier les transitions de section simples (Pattern 1).

***

## Partie 5 — Espace négatif et densité : les proportions actuelles

### 5.1 Heroes : le ratio vide/contenu en 2024–2026

Deux études convergentes documentent les proportions actuelles des heroes :[^49][^50][^37]

**Contentsquare (2026 trends)** nomme explicitement l'"Emphasizing Negative Space" comme l'un des 6 plus grands trends de 2025–2026, avec l'argument : "When you surround website elements with white space, it's clear to users where you're trying to draw their attention".[^49]

**Hero section composition study (2026)** donne des ratios concrets :[^37]
- Contenu principal : 40–60% de la largeur desktop.
- Image/visuel : soit grand (50–60% de la zone hero) soit minimal (30–40%). **Éviter le "milieu" à 45%** qui semble cramped.
- Padding vertical autour du contenu : minimum 60 px, optimal 80–120 px.
- Règle empirique : "Si ça semble spacieux, c'est probablement juste. Si vous craignez de gaspiller l'espace, vous êtes sur la bonne voie."[^37]

Sam Anthony (2025 trends) synthétise : "Minimalist, spacious designs and greatly optimised interactive elements ensure that websites remain lightweight while engaging users".[^50]

**Règle de génération (Hero)** :
```
hero.width-content = max 8 colonnes sur 12
hero.padding-vertical = 96px min (120px optimal)
hero.image-size = soit 50-60% soit 30-40% — interdire 40-50%
hero.vide = au moins 1 colonne de marge visible des deux côtés
```

***

### 5.2 Composants UI : densité comme signal sectoriel

La distinction actuelle est **contextuellement signifiante** : un composant dense communique la maîtrise et la sophistication professionnelle, un composant aéré communique la clarté et la facilité d'accès.[^30][^29]

La thèse de Master CAWEB / NNG synthétise ce consensus :[^29]
- **Outils expert et dashboards** → densité accrue post-shift AI, mais très structurée (grouping, hierarchy, borders fonctionnels).
- **Landing pages et marketing** → minimalisme spacieux persistant voire intensifié.
- **Produits mixtes** → hiérarchie claire entre "overview" spacieux et "detail/data" dense.

Pour un **système de génération automatique**, cela se traduit en 3 profils de composant :

| Profil | Padding vertical lignes | Secteurs typiques |
|---|---|---|
| Spacious | 20–28 px | Luxe, culture, créatif |
| Comfortable | 12–16 px | SaaS, produit, santé |
| Compact | 6–10 px | Analytics, dashboards B2B, fintech |

Sources :[^30][^31][^29]

***

### 5.3 Le vide intentionnel vs le remplissage systématique

Le principe de Gestalt appliqué au web reste la référence établie : le vide n'est pas une absence mais un **acteur de la composition** — il crée la hiérarchie, signale les groupes, guide l'œil.[^51]

Ce qui distingue le **vide intentionnel 2025** du "remplissage évité par défaut" :
- Le vide est **aligné sur le grid** : les marges sont multiples du système de spacing (4 px base, 8 px base ou tokens).[^33][^32]
- Le vide est **asymétrique quand c'est voulu** : une section peut avoir plus de padding en haut qu'en bas pour diriger la lecture vers la suivante.[^51][^26]
- Le vide est **cohérent** : les mêmes valeurs de padding reviennent à travers les sections (pas d'espacements arbitraires).[^33][^32]

**Règle de génération** :
```
spacing-system = base 8px (ou 4px pour dense)
section.padding = multiple de 8px (ex: 96px = 12×8)
composant.padding-interne = multiple de 4px (ex: 16px, 20px, 24px)
interdire les valeurs "à la main" (ex: 37px, 93px) sauf contrainte typographique
```

***

## Partie 6 — Application aux 3 sections du style-tile

### 6.1 Section Hero

| Paramètre | Valeur recommandée | Source |
|---|---|---|
| Largeur du bloc de contenu | 6–8 colonnes sur 12 | [^37][^24] |
| Padding vertical | 96–140 px | [^37] |
| Padding de marges latérales | 80–160 px (desktop) | [^37] |
| Hover sur CTA | fade couleur + shadow +1 + 150ms | [^5][^2] |
| Hover sur liens nav | underline slide + text-opacity | [^3][^7] |
| Transition vers section suivante | Pattern 1 (fond change) ou Pattern 2 (overlap léger) | [^24][^38] |
| Curseur custom | Secteurs créatifs/luxe uniquement | [^14][^11] |

### 6.2 Section Composant UI Témoin

| Paramètre | Valeur recommandée | Source |
|---|---|---|
| Hiérarchie | 3 niveaux : header / contenu / actions | [^25][^26] |
| Densité par défaut | Comfortable (12–16 px line height bonus) | [^31][^29] |
| Séparations internes | Fond teinté + ligne fine max, pas décoratif | [^24][^26] |
| Data | Badge + stat block + sparkline. Max 1 graphe | [^27][^34] |
| Hover rows/cards | highlight fond + actions reveal | [^2][^3] |
| Asymétrie | Colonne principale 55–70% si composant à colonnes | [^26] |

### 6.3 Section Atmosphère / Conclusion

| Paramètre | Valeur recommandée | Source |
|---|---|---|
| Structure | Pré-footer (heading fort + CTA ou manifeste) + footer structurel | [^18][^17][^19] |
| Hauteur pré-footer | 40–80% viewport | [^16][^19] |
| Fond pré-footer | Contrasté vs section précédente | [^18][^17] |
| Heading pré-footer | 40–72 px, assertif, max 8 mots | [^41][^16] |
| Footer structurel | Max 3 colonnes + bloc brand | [^16][^22] |
| Mega-footer sitemap | ❌ Interdit | [^45][^17] |

***

## Sources principales

- **Nacar Design** — "How to Create Powerful Microinteractions" (2025) :[^1]
- **JustinMind** — "Best web micro-interaction examples and guidelines for 2025" :[^3]
- **Appnova** — "The 10 Most Important UI Design Trends for 2025" et "Top 20 Web Design Trends 2025" :[^2][^38]
- **ShapeBootstrap** — "Hover Effects for Buttons: Modern Techniques 2025" :[^5]
- **YouTube / Web Design Pro** — "Website Footer Design Inspiration (Best practices in 2024)" :[^16]
- **Awwwards** — Collections "Footer Design Best Practices", "Hovers, Cursors and Cute Interactions", "Transitions" :[^21][^46][^11][^20]
- **IT-Dimension** — "UX/UI Trends 2025: How Design Adapts to New Realities" :[^26]
- **UX Planet** — "Principles of Spacing in UI Design: 4-Point Spacing System" :[^32]
- **Stan Vision** — "Micro interactions in web design: how subtle details shape UX" (2026) :[^7]
- **Contentsquare** — "6 modern web design trends for 2026" :[^49]
- **Codrops** — Tutorials 2025 (Interactive Image Grid, Animated Product Grid Preview, Portfolio Animations) :[^52][^4][^12][^13]
- **Pages.report** — "7 Best Web Page Footer Examples 2025" :[^18]
- **Eleken** — "10 modern footer UX patterns for 2026" :[^19]
- **Master CAWEB / Unistra** — "Minimalism vs Density in UI and UX" (2026) :[^29]
- **Nielsen Norman Group** — "Visual Hierarchy in UX: Definition" et "Whitespace" :[^53][^25]
- **AWS Cloudscape Design System** — "Content Density Guidelines" :[^31]
- **ConvertFlowes / Hero Section Composition** (2026) :[^37]
- **GraphicMama** — "Graphic Design Trends 2024" (grids and visible borders) :[^24]
- **Smashing Magazine** — "New Front-End Features For Designers in 2025" (View Transitions, scroll behavior, fluid type) :[^48]
- **Utsubo** — "Award-Winning Web Design: Judging Criteria Decoded" (2026) :[^54]
- **Sam Anthony** — "Web Design Trends (2025)" :[^50]
- **Pixelmatters** — "8 UI design trends we're seeing in 2025" :[^35]

---

## References

1. [How to Create Powerful Microinteractions - Nacar Design](https://nacardesign.com/2025/03/12/how-to-create-powerful-micro-interactions-from-basics-to-better-ux/) - This guide explores how to create effective microinteractions—from core concepts to practical implem...

2. [The 10 Most Important UI Design Trends for 2025 - Appnova](https://www.appnova.com/ui-design-trends/) - 2025 is set to be a landmark year for UI design, with digital experiences getting more immersive, in...

3. [Best web micro-interaction examples and guidelines for 2025](https://www.justinmind.com/web-design/micro-interactions) - In this post, we'll look at some great examples of what micro-interactions can achieve when done rig...

4. [Built to Move: A Closer Look at the Animations Behind Eduard ...](https://tympanus.net/codrops/2025/07/29/built-to-move-a-closer-look-at-the-animations-behind-eduard-bodaks-portfolio/) - In this breakdown, I'll walk you through three of the core GSAP animations on my site: flipping 3D c...

5. [Hover Effects for Buttons: Modern Techniques in Web ...](https://shapebootstrap.net/hover-effects-for-buttons-modern-techniques-in-web-design-2025/) - Buttons remain one of the most critical elements in web design. They guide users through interfaces,...

6. [UX/UI Trends for 2025: VUI, Emotional Design, and Microinteractions](https://www.awesomic.com/blog/ux-ui-trends-to-watch-in-2025-voice-interfaces-emotional-design-and-microinteractions) - Best Practices to implement microinteractions. Effective micro-interactions create moments of deligh...

7. [Micro interactions in web design: how subtle details shape ...](https://www.stan.vision/journal/micro-interactions-2025-in-web-design) - Learn how micro interactions in web design use subtle UI feedback, animations, and states to improve...

8. [5 Micro-interactions That Improve UX | 2026 | Ripplix Blog](https://www.ripplix.com/blog/ui-design-tips-micro-interactions-before-after) - Learn 5 proven UI design tips using micro-interactions to improve UX, boost clarity, and increase en...

9. [Building a card layout with a “hover reveal” effect](https://developer.wordpress.org/news/2024/07/building-a-card-layout-with-a-hover-reveal-effect/) - Learn to use the Grid block and Cover block to create cards with a hover reveal effect.

10. [Homepage & Navigation UX Best Practices 2025 - Baymard](https://baymard.com/blog/ecommerce-navigation-best-practice) - Discover 11 Homepage & Category Navigation UX best practices to follow, backed by our 2025 UX benchm...

11. [Hovers, Cursors and Cute Interactions - Awwwards](https://www.awwwards.com/awwwards/collections/hovers-cursors-and-cute-interactions/) - Hovers, Cursors, Animations, Interactions,RollOvers 466 items. ELEMENT Mouse Interaction video 3D Cu...

12. [Building an Interactive Image Grid with Three.js - Codrops](https://tympanus.net/codrops/2025/03/18/building-an-interactive-image-grid-with-three-js/) - In this tutorial, we'll create an interactive image grid using Three.js, covering setup, animations,...

13. [Animated Product Grid Preview with GSAP & Clip-Path - Codrops](https://tympanus.net/codrops/2025/05/27/animated-product-grid-preview-with-gsap-clip-path/) - We'll explore a “grid to preview” hover interaction that transforms product cards into a full previe...

14. [Key Website Design Trends for 2025 - Globe Runner](https://globerunner.com/key-website-design-trends-for-2025/) - Explore the key website design trends expected to shape 2025. From AI integration to micro animation...

15. [I've been testing out interactions with custom cursors on my design ...](https://www.instagram.com/reel/DAtrOkmSGG3/) - I've been testing out interactions with custom cursors on my design portfolio. There are two cursor ...

16. [Website Footer Design Inspiration (Best practices in 2024) - YouTube](https://www.youtube.com/watch?v=Dt04HR1lN5Y) - ... examples and best practices to show you what footer excellence looks like in 2024. Learn to desi...

17. [Website footer examples that should inspire you - Muffin Group](https://muffingroup.com/blog/website-footer/) - Explore website footer design examples with layout patterns, typography standards, mobile adaptation...

18. [7 Best Web Page Footer Examples to Inspire You in 2025](https://www.pages.report/blog/web-page-footer-examples) - Discover the best web page footer examples for 2025. Get actionable insights on layout, copy, and co...

19. [10 modern footer UX patterns for 2026 [with pro tips] - Eleken](https://www.eleken.co/blog-posts/footer-ux) - Start designing footers that users actually use. See 10 modern UX patterns with practical tips for m...

20. [Footer Design Best Practices - Awwwards](https://www.awwwards.com/awwwards/collections/website-footer-design-best-practices/) - The bottom of a web page, which contains general and legal info about the company, as well as a site...

21. [Best Footer Design in Websites | Web Design Inspiration - Awwwards](https://www.awwwards.com/websites/footer-design/) - Beautiful Footers in Website Designs for Inspiration. Selection of Awwwards winning footer design in...

22. [Website Footer Design Best Practices [+Tools and Examples]](https://curator.io/blog/website-footer-design) - We've rounded up some tried-and-true best practices and footer design basics to help you design a fo...

23. [26 Best HTML & Bootstrap Footer Templates 2026 - Colorlib](https://colorlib.com/wp/html-footer-templates/) - Free HTML footer templates and Bootstrap footer designs. Responsive, dark mode, mega footers with so...

24. [Graphic Design Trends 2024 - The Great Reset - GraphicMama](https://graphicmama.com/blog/graphic-design-trends-2024/) - Using grids in your designs will improve the hierarchy and structure of the design. The bigger the e...

25. [Visual Hierarchy in UX: Definition - NN/G](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/) - A clear visual hierarchy guides the eye to the most important elements on the page. It can be create...

26. [UX/UI Trends 2025: How Design Adapts to New Realities](https://it-dimension.com/blog/ux-ui-trends-2025-how-design-adapts-to-new-realities/) - Standardized spacing. A consistent spacing system creates visual rhythm and improves readability by ...

27. [BI Dashboard Design: 2025 UX Best Practices](https://ukdataservices.co.uk/blog/articles/business-intelligence-dashboard-design.php) - How to design effective business intelligence dashboards that turn complex data into clear decisions...

28. [Mastering Advanced Typography and Visual Hierarchy in UI Design](https://www.linkedin.com/pulse/mastering-advanced-typography-visual-hierarchy-ui-design-karimeh-txbbf) - Typographic Hierarchy in UI Components ... Modular Layouts: Grid-based systems allow consistent spac...

29. [Minimalism Versus Density in UI and UX - Master CAWEB](https://mastercaweb.unistra.fr/en/actualites/ux-ui-design-en/minimalism-versus-density-in-ui-and-ux/) - Minimalism earns attention. Density earns confidence and speed. The strongest UX designs achieve bot...

30. [Ultimate Guide to Flat Design: Best Practices and Examples](https://www.mockplus.com/blog/post/flat-design-guide) - Research from the Norman Nielsen Group highlights that flat design can reduce usability, as users ma...

31. [General guidelines](https://cloudscape.design/foundation/visual-foundation/content-density/) - Content density is defined by the ratio of information visible compared to the space available in th...

32. [Principles of Spacing in UI Design: A Beginner's Guide to the 4-Point ...](https://uxplanet.org/principles-of-spacing-in-ui-design-a-beginners-guide-to-the-4-point-spacing-system-6e88233b527a) - In this article, we'll explore the principles of spacing in UI design and provide a step-by-step gui...

33. [Top Website Design Best Practices for 2025](https://altitudedesign.co.uk/blog/website-design-best-practices) - Discover essential website design best practices to enhance user experience in 2025. Learn tips to o...

34. [Top 10 UX/UI Design Trends for 2025 - Touch4IT](https://www.touch4it.com/blog/top-10-uxui-design-trends-2025) - As we approach 2025, UX/UI design will change quickly due to new technologies and higher user expect...

35. [8 UI design trends we're seeing in 2025 - Pixelmatters](https://www.pixelmatters.com/insights/8-ui-design-trends-2025) - Discover some of our favorite UI design trends for 2025, from dynamic minimalism to functional AI an...

36. [55 Best Website Design Ideas & Inspiration (2025) - The Web Factory](https://www.thewebfactory.us/blogs/55-best-website-design-ideas-and-web-design-examples/) - Looking for website design ideas? Browse 55 cutting-edge web design examples and trends shaping 2025...

37. [Hero Section Composition: What Actually Captures Attention](https://convertflowes.com/landing-page-design-malaysia/hero-section-composition/) - Explore the core elements that make hero sections work. Headline placement, imagery strategy, and wh...

38. [Top 20 Web Design Trends to Watch in 2025 - Appnova](https://www.appnova.com/top-web-design-trends/) - From bold visuals to smarter features, this blog highlights 20 biggest website design trends that ca...

39. [Create STUNNING Seamless Scroll Transitions in Divi (Overlaps ...](https://www.youtube.com/watch?v=cawZ83SP8RE) - Divi's visual drag-and-drop page builder and professional website templates make it super easy for a...

40. [Long SCROLL Item with Overlapping Section Transition Effect For ...](https://www.youtube.com/watch?v=665L57vDJ_c) - ... STICKY Images and Long Item Scroll with Overlapping Effects for FREE and also i will show you ho...

41. [Top 7 UI Design Trends Shaping 2025 - LinkedIn](https://www.linkedin.com/pulse/top-7-ui-design-trends-shaping-2025-hassam-shabbir-zhbhf) - UI design in 2025 is moving in two directions at once: toward cleaner, more focused layouts and towa...

42. [Modern Typography: Trends and Inspirations for 2025](https://graphicdesignjunction.com/2025/04/modern-typography-trends-2025/) - Modern digital typography is reshaping digital and print media, and in 2025, modern typography will ...

43. [Rethinking “Pixel Perfect” Web Design - Smashing Magazine](https://www.smashingmagazine.com/2026/01/rethinking-pixel-perfect-web-design/) - Amit Sheen takes a hard look at the “Pixel Perfect” legacy concept, explaining why it's failing us a...

44. [Scrolling Designs: 8 Patterns and When to Use Each (2026) | Lovable](https://lovable.dev/guides/scrolling-designs-patterns-when-to-use) - 1. Parallax Scrolling: Multi-Layered Depth · 2. Infinite Scroll: Continuous Content Discovery · 3. H...

45. [Looking Back at the Top Web Design Trends (2018-2019)](https://kinsta.com/blog/web-design-trends/) - How is the world of web design evolving? An in-depth look and analysis of the latest trends in web d...

46. [Transitions - Awwwards](https://www.awwwards.com/awwwards/collections/transitions/) - Transitions are the animated changes between two pages, states or views to provide visual continuity...

47. [Tutorials - Codrops](https://tympanus.net/codrops/category/tutorials/) - In this tutorial, we'll create four scroll-driven transitions that reveal fullscreen images using SV...

48. [New Front-End Features For Designers In 2025 - Smashing Magazine](https://www.smashingmagazine.com/2024/12/new-front-end-features-for-designers-in-2025/) - This post is a journey through new front-end features and what they are capable of. Component-specif...

49. [6 modern web design trends to inspire you in 2026 - Contentsquare](https://contentsquare.com/guides/web-design/trends/) - Need to design a fresh and modern website? We’re uncovering the most innovative web design trends fo...

50. [Web Design Trends (2025) | Sam Anthony](https://samanthony.design/blog/trends-2025) - Fast-loading websites are non-negotiable in 2025. Minimalist, spacious designs and greatly optimised...

51. [How To Use Spaces In Web Design With Gestalt Principles](https://www.smashingmagazine.com/2019/04/spaces-web-design-gestalt-principles/) - In this article, we covered the Gestalt principles in relation to positive and negative spaces in we...

52. [2025: A Very Special Year in Review - Codrops](https://tympanus.net/codrops/2025/12/29/2025-a-very-special-year-in-review/) - A look back at the ideas, experiments, and people that shaped a remarkable year at Codrops.

53. [What is Whitespace? (Video) - Nielsen Norman Group](https://www.nngroup.com/videos/whitespace/) - Whitespace is an effective principle to achieve a balanced design, making it easier for your users t...

54. [Award-Winning Web Design: Judging Criteria Decoded - Utsubo](https://www.utsubo.com/blog/award-winning-website-design-guide) - Custom interaction design is the single biggest differentiator — template-based and AI-generated sit...

