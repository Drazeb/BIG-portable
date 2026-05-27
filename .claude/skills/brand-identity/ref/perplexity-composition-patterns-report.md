<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# \# Recherche — Patterns de composition web : datés vs actuels (2024-2026)

## Contexte

Je travaille sur un système de génération automatique d'identités de marque qui produit des style-tiles HTML (des pages web showcase en 3 sections : hero, composant UI témoin, section atmosphère/manifeste). Le système génère pour TOUS les secteurs
(tech, luxe, industrie, food, culture, santé, etc.).

Mon problème : le système produit parfois des compositions qui "sentent" 2018-2020 — des layouts, structures et patterns visuels qui étaient à la mode il y a quelques années mais qui ne le sont plus. Je veux identifier précisément :

1. Quels patterns de composition web sont aujourd'hui considérés comme datés/clichés
2. Quels patterns de composition sont actuellement utilisés par les meilleurs sites (2024-2025-2026)

Je ne parle PAS de techniques CSS (j'ai déjà traité ça). Je parle de COMPOSITION : comment les éléments sont disposés, structurés, proportionnés sur la page. Ça inclut les layouts de hero/header, les structures de composants UI, les sections de
contenu, les footers/atmosphères.

## Ce que je cherche

### Partie 1 — Patterns de composition DATÉS

Pour chaque pattern identifié :

- Description précise du pattern (layout, structure, proportions)
- Période où il était dominant (ex: 2016-2020)
- Pourquoi il est considéré daté aujourd'hui (qu'est-ce qui a changé)
- Sources qui documentent ce consensus (articles, experts, discussions)

Sois exhaustif — je préfère avoir trop d'items et couper ensuite.

Inclure au minimum ces catégories :

- Layouts de hero/header (compositions du haut de page)
- Structures de composants (cards, grilles, tableaux, dashboards, timelines, steppers)
- Patterns de sections de contenu (comment les sections s'enchaînent)
- Patterns de footer/conclusion
- Éléments décoratifs de page (séparateurs, formes, ornements)
- Patterns d'interaction visuelle (hover, animations, transitions — en termes de composition, pas de technique CSS)


### Partie 2 — Patterns de composition ACTUELS (2024-2025-2026)

Mêmes catégories. Pour chaque pattern :

- Description précise
- Depuis quand il est dominant
- Pourquoi il fonctionne (qu'est-ce qui le rend actuel)
- Exemples de sites Awards ou de marques qui l'utilisent
- Sources


### Partie 3 — Synthèse croisée

Un tableau qui croise : pattern daté → son remplacement actuel → pourquoi le remplacement est meilleur.

## Exigences de qualité

### Sources fiables UNIQUEMENT

- Agences de design reconnues (Pentagram, Fantasy, Huge, Instrument, BASIC/DEPT, Ramotion, Tubik)
- Experts publiés et reconnus (Vitaly Friedman/Smashing Magazine, critères Awwwards, Codrops, designmodo)
- Conférences de référence (An Event Apart, Config/Figma, CSS Day)
- Forums de practitioners (si crédibles et argumentés)
- NE PAS utiliser : listicles SEO ("10 web design trends 2025"), blogs marketing généralistes, articles sans argumentation


### Précision temporelle

- "Actuel" = 2024, 2025, 2026. Pas 2022.
- "Daté" = patterns qui étaient dominants AVANT 2024 et qui ne le sont plus.
- Si un pattern est ancien (ex: pre-2020) mais TOUJOURS utilisé par les meilleurs sites en 2025 → il n'est PAS daté. Le signaler explicitement.


### Transversal vs sectoriel

- Concentre-toi PRINCIPALEMENT sur les patterns TRANSVERSAUX — ceux qui sont datés ou actuels QUEL QUE SOIT le secteur. C'est ma priorité.
- Si tu identifies des patterns spécifiques à certains secteurs (tech, luxe, etc.), note-les en complément, mais n'y passe pas trop de temps. Les transversaux sont ce qui m'intéresse le plus.


### Argumentation

- Pour chaque pattern (daté ou actuel), expliquer POURQUOI. Pas juste "c'est une tendance" mais la raison de fond (changement d'usage, évolution des devices, shift culturel, etc.)


## Format de sortie

Un rapport structuré en markdown avec :

1. Partie 1 : Patterns datés (par catégorie)
2. Partie 2 : Patterns actuels (par catégorie)
3. Partie 3 : Tableau croisé daté → actuel
4. Sources utilisées (avec URLs)

Sois le plus exhaustif et détaillé possible. Je préfère un rapport long et complet qu'un résumé superficiel.

Voici une grille de travail pour “désenterrer” ton moteur : je me concentre sur les patterns réellement discutés par des praticiens et observables sur les sites primés, pas sur des listicles SEO.

***

## 1. Patterns de composition datés (par catégorie)

### 1.1 Hero / Header

#### 1.1.1 Hero “SaaS 2018” ultra-rigide

- **Description**
    - Layout 2 colonnes strictes 50/50 : à gauche H1 + paragraphe + 1 ou 2 boutons, à droite un “full screenshot” de l’app dans un frame d’ordi ou de mobile.
    - Tout est contenu dans un bloc centré, avec large padding top/bottom, background uni, souvent gradient linéaire.
    - Proportions : H1 très dominant, visuel d’app scellé dans un rectangle unique, très peu de layering ou d’éléments flottants.
- Période dominante
    - En gros 2016–2021, porté par la vague SaaS marketing “clean + flat + screenshot produit”.[^1][^2]
- Pourquoi daté
    - Les designers constatent que l’utilisateur “glisse” ce type de hero sans le regarder : trop générique, pas assez spécifique au produit ou à la marque.[^3]
    - La narration par un seul screenshot ne tient plus : produits modulaires, multiproduits, features complexes → besoin de montrer des “morceaux” plutôt qu’un écran complet.[^3]
    - Les sites primés Awwwards / portfolios récents montrent plutôt des compositions fragmentées (bento, composants isolés, layers flottants) et des transitions liées au scroll.[^4][^3]
- Sources / signaux
    - DesignerUp explique que la plupart des headers récents se détachent du “simple header lockup avec screenshot plein” pour aller vers des heros plus créatifs (isolated component, bento, tied-to-scroll).[^5][^3]


#### 1.1.2 Hero “template Bootstrap” centré

- **Description**
    - H1 centré, petit paragraphe centré, deux boutons côte à côte centrés, éventuellement une illustration SVG générique en dessous.
    - Largeur de texte ~600–800px, tout pile au centre de l’écran, sans rupture de grille, sans asymétrie.
- Période dominante
    - Très répandu sur 2015–2020, via les templates Bootstrap / ThemeForest.[^2][^1]
- Pourquoi daté
    - L’absence de tension visuelle (tout centré, tout symétrique) est perçue comme peu premium et peu “brandé” par rapport aux heros actuels qui jouent sur asymétries, clusters de contenu, layering.[^6][^3]
    - Les collections “Layout” d’Awwwards montrent très peu de homepages primées avec ce motif ultra-centre, au profit de compositions plus fragmentées ou éditoriales.[^7][^4]


#### 1.1.3 Split-screen 50/50 très littéral

- **Description**
    - Split vertical 50/50 : texte à gauche, image pleine hauteur à droite (photo ou visuel produit), sans interaction entre les deux côtés, séparation nette.[^8]
- Période dominante
    - Trend fort 2016–2019 (mis en avant dans de nombreux guides de layout “split-screen pattern”).[^1][^8]
- Pourquoi daté
    - Sur desktop, ce pattern rigidifie la hiérarchie : un côté est visuellement “perdu” si l’utilisateur scrolle vite.
    - Sur mobile, il se réduit à un simple “texte puis visuel” empilé, sans valeur ajoutée vs. un layout plus adaptatif.
    - Les split actuels (sur sites primés) sont plus dynamiques : ratios non 50/50, chevauchements, cards qui débordent, interaction avec le scroll.[^9][^4]

***

### 1.2 Structures de composants (cards, grilles, dashboards…)

#### 1.2.1 Mur de cards uniformes “Pinterest SaaS”

- **Description**
    - Grille uniforme de cards de même largeur, même hauteur, même padding, avec : icône + titre + 2 lignes de texte + CTA ou chevron.
    - Disposition en 3–4 colonnes sur desktop, 1 colonne sur mobile, sans variations de proportions, sans hiérarchie entre cards.[^8]
- Période dominante
    - 2015–2022, héritage du card-layout popularisé par Material Design et les feeds sociaux.[^2][^1]
- Pourquoi daté
    - Perçu comme “card sprawl” : tout est mis au même niveau, rendant la scannabilité plus difficile qu’un layout hiérarchisé.[^10]
    - Les critiques actuelles pointent :
        - Cards partout → perte d’impact, clutter.
        - Longueurs de contenu inégales → lignes brisées et trous visuels.
        - Actions dispersées sur chaque card → charge cognitive.[^10]
    - Les dashboards/landing récents privilégient des grilles avec modules de tailles différentes, “hero card” dominante, regroupement des actions, ou retour au tableau pour l’info dense.[^11][^10]


#### 1.2.2 Dashboard “widget zoo” sans hiérarchie

- **Description**
    - Home analytics avec 8–12 widgets de taille similaire, disposés en grille 3×3 ou 4×3, tous au même poids visuel (graphique, KPI, card).[^8]
- Période dominante
    - 2014–2020, dans les templates de dashboards BI / admin.[^1]
- Pourquoi daté
    - La littérature récente sur BI dashboard préconise une hiérarchie explicite : top-row pour 2–3 KPI critiques, ensuite détails, avec une grille 12 colonnes flexible et versions mobiles simplifiées.[^11]
    - Les designers data parlent de “decision first, then detail”, incompatibles avec la matrice plate de widgets.[^11]


#### 1.2.3 Timelines ultra-linéaires

- **Description**
    - Timeline verticale ou horizontale avec points régulièrement espacés, texte de même taille, même importance, souvent avec une ligne centrale, sans variations de blocs ou de regroupements.[^8]
- Période dominante
    - Très en vogue dans les années 2010 (about pages, “Our history”).[^1]
- Pourquoi daté
    - Les timelines actuelles se transforment plutôt en “story sections” séquencées, avec blocs de contenu différents, visuels par étape et micro-interactions, plutôt que la ligne uniforme.[^4][^9]
    - Sur mobile, la timeline linéaire classique est peu lisible; les designers préfèrent des sections empilées avec repères temporels clairs à chaque bloc.[^12]

***

### 1.3 Patterns de sections de contenu

#### 1.3.1 Alternance “image gauche / texte droite” parfaitement répétitive

- **Description**
    - Section 1 : image left, texte right. Section 2 : image right, texte left. Et ce motif se répète 4–6 fois.
    - Proportions 50/50, même hauteur de section, même padding, même style de visuel.
- Période dominante
    - 2013–2020, devenu “le” motif de landing pages de produits et services.[^2][^1]
- Pourquoi daté
    - Pattern trop prévisible, quasi-squelettique, qui donne une impression de template.
    - Les contenus éditoriaux récents (Smashing, Awwwards) mettent davantage en avant des séquences avec variations : full-bleed sections, clusters, bento, hero-cards, etc.[^7][^6][^4]
    - Sur mobile, l’alternance gauche/droite perd sa signification (tout s’empile) → autant concevoir directement des blocs à valeur éditoriale, pas ce gimmick.[^13]


#### 1.3.2 Homepages “one scroll, 6 blocs génériques”

- **Description**
    - Enchaînement : Hero → “Features” en 3 cards → “How it works” en 3 steps → “Testimonials” en 3 cards → “Pricing” en 3 colonnes → “FAQ” en accordéon.
    - Chaque section est une boîte très autonome, sans continuité visuelle ni storytelling.
- Période dominante
    - 2016–2022, génération SaaS template-driven.[^2][^1]
- Pourquoi daté
    - Les critiques de designers UI récents pointent la “homogénéisation” : les sites finissent tous par raconter la même histoire dans le même ordre.[^14]
    - Les sites plus contemporains travaillent davantage la continuité entre sections (transitions, re-usage de motifs, anchors éditoriaux), et adaptent l’ordre des sections à la proposition de valeur.[^9][^4]

***

### 1.4 Footers / conclusions

#### 1.4.1 Mega-footer “site map déguisée”

- **Description**
    - Bas de page en 3–5 colonnes de liens texte, tous de même poids, plus un bloc newsletter, plus les icônes sociales.
    - Fetish du “tout mettre en bas”, même sur de petites marques.
- Période dominante
    - 2012–2020 (héritage corporate / CMS).[^1]
- Pourquoi daté
    - Contraste avec les footers plus éditoriaux ou compressés des sites récompensés, qui sélectionnent quelques liens clés + un motif de marque fort (baseline, mini-manifeste, contact clair).[^4][^7]
    - En mobile, ces mega-footers deviennent des scrolls inutiles; les pratiques récentes préconisent des footers plus tactiques (CTA, support, locales) et des menus persistants pour le reste.[^12]

***

### 1.5 Éléments décoratifs de page

#### 1.5.1 Separators en vagues, diagonales clip-path génériques

- **Description**
    - Sections séparées par des bords en “vague”, diagonales CSS, zigzags, souvent appliqués partout.
- Période dominante
    - 2016–2020 (souvent dans les générateurs de templates).[^2][^1]
- Pourquoi daté
    - Sur-utilisation dans le bas/moyen de gamme et absence de lien avec le contenu.
    - Les tendances actuelles préféreront des séparations plus nettes (grid visible, bordures fines, jeux de spacing) ou des motifs typographiques/illustratifs spécifiques à la marque.[^14][^6]


#### 1.5.2 Gradients “Instagram 2018” full-bleed

- **Description**
    - Large gradient multicolore en arrière-plan du hero ou de sections entières, souvent violet/rose/bleu très saturé.[^2]
- Période dominante
    - 2017–2020, identifiés comme “la” réponse à la lassitude du flat.[^1][^2]
- Pourquoi daté
    - Les gradients n’ont pas disparu, mais la version full-bleed ultra-saturée est associée à l’esthétique de cette période.
    - Les grilles et bordures visibles, couleurs plus contrôlées et palettes réduites dominent aujourd’hui la typologie “pro / système”.[^6][^14]

***

### 1.6 Patterns d’interaction visuelle (au niveau composition)

#### 1.6.1 Parallax lourd et scroll-jacking

- **Description**
    - Sections qui se déplacent à des vitesses différentes au scroll, parfois couplées à un scroll-jacking (le scroll déclenche des “slides” fixes).
- Période dominante
    - Très présent dans les sites “créatifs” 2014–2019.[^15][^1]
- Pourquoi daté
    - Fatigue utilisateur, problèmes d’accessibilité et de performance.
    - Les discussions récentes privilégient des micro-interactions douces et des transitions qui soutiennent la lisibilité plutôt que des effets spectaculaires qui prennent le dessus.[^13][^12]


#### 1.6.2 Hovers critiques pour la compréhension (desktop-only)

- **Description**
    - Information essentielle qui n’apparaît qu’au hover sur les cards, images, éléments de navigation.
- Période dominante
    - Courant dans les patterns desktop des années 2010.[^8][^1]
- Pourquoi daté
    - Non-fonctionnel sur mobile, dark patterns potentiels, et contraire aux recommandations d’accessibilité récentes.[^12][^13]

***

## 2. Patterns de composition actuels (2024–2026)

### 2.1 Heros / headers

#### 2.1.1 Hero “composants isolés” (Isolated Component Hero)

- **Description**
    - Au lieu d’un screenshot complet, le hero présente une composition de fragments d’UI : cards de stats, header de table, modal, snippet de chat, etc. disposés en cluster.[^5][^3]
    - Le texte de valeur (H1 + pitch) occupe une colonne principale; les composants flottent dans une zone adjacente, souvent en layout libre mais sous-jacent à une grille.
    - Les composants sont parfois partiellement masqués ou cropped pour suggérer richesse et profondeur.
- Depuis quand dominant
    - Popularisé 2022–2023, fortement mis en avant dans les “hero trends 2024” de DesignerUp et dans de nombreux sites SaaS récents.[^3][^5][^14]
- Pourquoi ça fonctionne
    - Permet de raconter une histoire fonctionnelle : chaque fragment d’UI illustre un bénéfice, sans dépendre d’un écran complet figé.[^3]
    - Décliné naturellement en responsive : les fragments se réorganisent (stack, carrousel, clusters) plutôt que de se réduire à un screenshot illisible.[^5][^13]
- Exemples / sources
    - DesignerUp – 5 hero layouts 2024 (Isolated Component Hero).[^5][^3]
    - Observables dans de nombreux sites de produits en analytics/ops référencés sur Awwwards.[^7][^4]


#### 2.1.2 Hero “Bento grid”

- **Description**
    - Hero structuré en grilles de tuiles de tailles variées (bento boxes), sur 2–3 rangées : une tuile dominante (message principal), plusieurs tuiles secondaires (features, preuves sociales, visuels).[^14][^3]
    - Grille explicite : bordures visibles ou blocs bien séparés, alignés sur un grid système.[^6]
- Depuis quand dominant
    - Terme “bento” associé au web/UI à partir de 2021 (Microsoft/Apple), mais explosion dans le monde produit vers 2023–2024.[^14][^3]
- Pourquoi ça fonctionne
    - Permet de densifier l’info sans card-sprawl : chaque tuile a un rôle précis (social proof, USP, product shot, CTA secondaire).[^6][^14]
    - S’adapte très bien aux breakpoints : les tuiles peuvent se reconfigurer en 2 colonnes ou en stack vertical, tout en gardant une hiérarchie lisible.[^13]
- Exemples / sources
    - Apple (sections bento sur plusieurs pages produit), cité comme référence bento par Sam Anthony.[^14]
    - DesignerUp – Bento grid hero.[^3][^5]


#### 2.1.3 Hero “lava layout / layered”

- **Description**
    - Layout avec grands blocs organiques ou “pools” de contenu qui se chevauchent légèrement, cartes/visuels flottants au-dessus du fond, parfois ombres douces.[^9][^5]
    - Composition asymétrique, mais adossée à une grille; un bloc texte principal et des “îlots” de contenu autour (avatars, chiffres, logos clients).
- Depuis quand dominant
    - Montée en puissance 2023–2025, visible dans plusieurs inspirations Stripe-like, portfolios.[^4][^9]
- Pourquoi ça fonctionne
    - Donne un sentiment de profondeur et de mouvement sans recourir à des animations lourdes.[^9]
    - Reste compatible avec une grille, ce qui facilite le design system et le responsive.[^13][^6]


#### 2.1.4 Hero “tied to scroll” / narrative scroll

- **Description**
    - Le hero s’étend sur plusieurs “écrans” : en scrollant, le texte évolue, les fragments d’UI se réarrangent ou se révèlent progressivement, souvent avec un côté fixe (texte ou visuel) et un côté qui défile.[^5][^3]
- Depuis quand dominant
    - Popularité croissante depuis ~2021, mais présenté comme pattern clé pour 2024 dans les contenus pro de DesignerUp.[^3][^5]
- Pourquoi ça fonctionne
    - Transforme le hero en mini-storytelling interactif, permettant de montrer la progression (avant/après, étapes clés) sans saturer un seul écran.[^3]
    - Si bien implémenté, reste accessible (scroll standard) tout en donnant une expérience “awwwards-like”.[^12][^4]

***

### 2.2 Composants / grilles / dashboards

#### 2.2.1 Grilles hiérarchisées avec “hero card”

- **Description**
    - Grilles de cards où une ou deux cards sont plus grandes (hero card), les autres plus petites; la taille communique l’importance.[^6]
    - Layouts combinant 1×2 + 2×1, etc., plutôt qu’un strict 3×3 uniforme.
- Depuis quand dominant
    - Noté comme pattern fort dans les tendances 2024 de “grids and visible borders”, et largement présent dans les bento/grids modernes.[^14][^6]
- Pourquoi ça fonctionne
    - Capte l’attention sur l’élément clé tout en permettant une liste d’options secondaires.
    - Répond aux critiques des grilles uniformes (manque de hiérarchie).[^10][^6]


#### 2.2.2 Card UI intentionnelle (moins, mais mieux)

- **Description**
    - Utilisation de cards pour des unités d’info cohérentes, avec hiérarchie interne claire: titre fort, contenu concis, actions regroupées au même endroit.[^10]
    - Cards espacées, rarement plus de 3–4 par ligne, décor limité, parfois encadrées par des bordures fines.[^10][^6]
- Depuis quand dominant
    - Consolidation 2023–2025, en réaction au “card sprawl” des années précédentes.[^10]
- Pourquoi ça fonctionne
    - Meilleure lisibilité et scannabilité, réduit la charge cognitive.[^10]
    - Les bordures visibles et grilles nettes donnent un aspect maîtrisé et premium.[^6]


#### 2.2.3 Dashboards centrés sur “jobs to be done”

- **Description**
    - Layout dashboard où la partie supérieure est réservée à 1–3 blocs critiques (KPI, tâche principale), sous lesquels se trouvent des modules détaillés.[^11]
    - Grille 12 colonnes, responsive : sur mobile, seuls les blocs essentiels sont visibles sur le premier écran.[^11]
- Depuis quand dominant
    - Documenté comme best practice 2024–2025 dans la littérature BI UX.[^11]
- Pourquoi ça fonctionne
    - Aligné avec les recommandations UX modernes (decision-first), plus faciles à traduire en direction pour un moteur de génération.[^12][^11]

***

### 2.3 Sections de contenu

#### 2.3.1 Séquences éditoriales variées

- **Description**
    - Plutôt qu’une simple alternance image/texte, la page est structurée en “chapitres” visuels distincts : un bloc de narration, un cluster de preuves, un bloc use-cases, etc., chacun avec un layout spécifique (hero card, bento, full-bleed, etc.).[^7][^4]
- Depuis quand dominant
    - Visible sur les sites primés 2022–2025 (portfolios, produits, culture).[^4][^7]
- Pourquoi ça fonctionne
    - Donne une sensation de voyage, renforce le récit tout en évitant l’ennui.
    - Permet d’utiliser des patterns de composition plus riches (bento, grids hiérarchisées, carrousels, story blocks).[^9][^6]


#### 2.3.2 Sections “evidence clusters”

- **Description**
    - Sections où multiples preuves sont rassemblées dans un cadre cohérent : logos clients, métriques, citations, awards, groupés dans une grille/cluster plutôt que éparpillés sur la page.[^9][^14]
- Depuis quand dominant
    - Tendance 2023–2025 dans les pages produit performantes.[^14][^9]
- Pourquoi ça fonctionne
    - Augmente la crédibilité en un bloc compact, facile à réutiliser dans différents templates.
    - S’intègre bien aux bento/grilles, et se décline facilement en mobile.[^13][^6]

***

### 2.4 Footers / conclusions

#### 2.4.1 Footers tactiques et éditoriaux

- **Description**
    - Footers plus courts, organisés autour de : CTA principal (demo, contact), contact/support, liens essentiels, et une micro-section de marque (baseline, manifeste, mini-bio).[^7][^4]
- Depuis quand dominant
    - Très visible dans les sites primés Awwwards récents (portfolios, studios, produits).[^4][^7]
- Pourquoi ça fonctionne
    - Renforce la personnalité de marque jusqu’en bas de page, tout en gardant l’info structurée.
    - Réduit le bruit sur mobile, où le footer est souvent la “fin de l’histoire” et le moment clé pour un CTA.[^12]


#### 2.4.2 Footers modulaires (grid)

- **Description**
    - Composition en quelques modules clairement séparés (contact, navigation, légal, social), alignés sur la grille globale du site, parfois avec des bordures visibles.[^6]
- Depuis quand dominant
    - Aligné avec le retour aux grilles visibles 2023–2025.[^6]
- Pourquoi ça fonctionne
    - Cohérence visuelle avec le reste du layout, lisibilité accrue, facile à combiner avec thème clair/sombre.

***

### 2.5 Éléments décoratifs

#### 2.5.1 Grilles visibles et bordures fines

- **Description**
    - Sections structurées par des bordures fines, lignes de séparation explicites, colonnes apparentes, parfois guides de grid visibles à très faible opacité.[^6]
- Depuis quand dominant
    - Explicitement identifié comme trend 2024 (“Grids and Visible Borders”).[^6]
- Pourquoi ça fonctionne
    - Renforce la hiérarchie et la lisibilité, surtout dans des UIs denses.[^6]
    - Permet des compositions complexes (bento, clusters) sans perdre la structure.


#### 2.5.2 Décor lié à l’identité (au lieu de générique)

- **Description**
    - Motifs illustrés, formes, textures ou micro-patterns directement dérivés de l’identité (logo, typographie, iconographie), intégrés dans les marges, inter-sections, backgrounds partiels.[^7][^4]
- Depuis quand dominant
    - Plus marqué depuis 2022, avec la montée des “brand systems” digitaux.[^14][^6]
- Pourquoi ça fonctionne
    - Permet de conserver un style distinctif sans retomber dans les gimmicks 2016 (waves, diagonales génériques).
    - Systémisable dans un générateur : slots décoratifs alimentés par un “brand motif”.

***

### 2.6 Interaction visuelle (composition)

#### 2.6.1 Micro-interactions ponctuelles alignées à la grille

- **Description**
    - Hovers simples (légers déplacements, soulignement des bordures, changement d’ombre), transitions entre states dans un cadre défini (same place, same size).[^13][^10]
- Depuis quand dominant
    - Consolidé 2022–2025 au fur et à mesure que CSS moderne facilite les transitions sans JS lourd.[^16][^13]
- Pourquoi ça fonctionne
    - Renforce les affordances, améliore la compréhension des composants, sans casser le scroll naturel.[^12][^13]


#### 2.6.2 Scrollytelling modéré

- **Description**
    - Utilisation du scroll comme déclencheur de transitions logiques (changement d’état, révélation d’éléments) dans un cadre limité : hero étendu, section produit clé.[^9][^3]
- Depuis quand dominant
    - Apparait comme compromis entre sites “expérientiels” et besoins de performance/UX (2022–2025).[^12][^9]
- Pourquoi ça fonctionne
    - Offre une allure premium Awwwards-compatible tout en restant utilisable sur mobile et accessible.[^4][^7]

***

## 3. Tableau croisé – pattern daté → pattern actuel

### Évolutions de composition (vue synthétique)

| Pattern daté (avant 2024) | Pattern actuel (2024–2026) | Pourquoi le nouveau est meilleur |
| :-- | :-- | :-- |
| Hero 2 colonnes “titre + paragraphe + 2 CTA” + screenshot plein d’app [^3][^1] | Hero de composants isolés (fragments d’UI en cluster) [^3][^5] | Raconte plusieurs bénéfices à la fois, s’adapte mieux aux produits complexes, plus différenciant visuellement, responsive plus riche. [^3][^5] |
| Hero centré “template Bootstrap” (tout aligné centre, illustration générique) [^1][^2] | Hero bento avec tuiles de tailles variées (message, preuves, visuels) [^3][^14][^6] | Introduit une hiérarchie claire et une densité d’info contrôlée, tout en gardant une structure forte, facile à adapter aux breakpoints. [^14][^6] |
| Split-screen 50/50 rigide texte/image [^8][^1] | Layouts asymétriques avec blocs superposés ou “lava layout” [^5][^9] | Crée une tension visuelle plus forte, permet de superposer contenu contextuel, meilleure adaptation aux petits écrans. [^9][^6] |
| Mur de cards uniformes (3×3, 4×3) [^8][^1] | Grilles hiérarchisées avec hero card + cards secondaires [^6][^10] | Introduit rang d’importance; réduit la fatigue visuelle et le “card sprawl”; améliore la découverte de contenu clé. [^6][^10] |
| Dashboard en matrice de widgets de même taille [^8][^1] | Dashboard centré sur décision (top KPI dominant, modules secondaires) [^11] | Aligné sur les tâches critiques (decision-first), meilleure lisibilité cross-device, conforme aux bonnes pratiques data UX modernes. [^11] |
| Sections en alternance image gauche/texte droite répétées [^1][^2] | Séquences éditoriales variées (chapitres avec layout propre) [^4][^7][^9] | Crée un récit distinctif, moins de monotonie, permet d’adapter la composition à chaque message plutôt qu’à un schéma figé. [^9] |
| Homepage “Hero → Features 3 cards → Steps 3 → Testimonials 3 → Pricing 3” copier-collé de template [^1] | Pages structurées par blocs narratifs (value, evidence cluster, flows, social proof modulaires) [^14][^9] | Meilleure adéquation au produit et à la marque, plus grande flexibilité pour différents secteurs; perçu comme moins générique. [^14][^9] |
| Mega-footer sitemap (4–5 colonnes de liens) [^1] | Footer tactique + éditorial (CTA, contact, mini-manifeste) [^4][^7] | Focalise sur actions clés et renforce la marque; réduit le bruit, surtout sur mobile. [^4][^12] |
| Separators en vagues, diagonales clip-path génériques [^1][^2] | Grilles visibles, bordures fines et motifs de marque spécifiques [^6][^14] | Évite les gimmicks; structure clairement le contenu; motifs directement liés à l’identité plutôt qu’à un effet de mode. [^6][^14] |
| Gradients full-bleed très saturés “Instagram 2018” [^2][^1] | Palettes maîtrisées, fonds neutres + accents colorés, parfois gradient discret dans un composant [^6][^14] | Maintient une apparence contemporaine, facilite la lisibilité des composants, plus durable esthétiquement. [^6][^14] |
| Parallax lourd + scroll-jacking [^1][^15] | Scrollytelling modéré sur quelques sections clés [^3][^9] | Conserve la fluidité du scroll, améliore accessibilité et performance, tout en ajoutant de la richesse narrative. [^9][^12] |
| Hovers indispensables à la compréhension (desktop-only) [^1][^8] | Micro-interactions non bloquantes, états visibles par défaut, transitions douces [^12][^13][^10] | Fonctionne sur mobile et desktop, réduit risque de contenu “caché”, améliore l’accessibilité et la robustesse UX. [^12][^13] |


***

## 4. Sources (sélection avec URLs)

- Awwwards – Layout collections / sites primés (pour observation des compositions récentes)[^17][^7][^4]
    - https://www.awwwards.com
    - https://www.awwwards.com/awwwards/collections/layout/
- Smashing Magazine – design patterns, CSS moderne, critique du “pixel perfect” (structure adaptative)[^18][^13][^12]
    - https://www.smashingmagazine.com
    - https://www.smashingmagazine.com/categories/design-patterns/
    - https://www.smashingmagazine.com/2026/01/rethinking-pixel-perfect-web-design/
- DesignerUp – “2024 Design Trends | 5 Must Try Hero Layouts” (Isolated Components, Bento, Lava, Callout, Tied-to-scroll) [^3][^5]
    - https://designerup.co/blog/2024-design-trends-5-must-try-hero-layouts/
    - https://www.youtube.com/watch?v=TjLxhLSrmGw
- Sam Anthony – “Web \& UI Design Trends (2024)” (bento box layouts, shift away from simple flat UI)[^14]
    - https://samanthony.design/blog/trends-2024
- GraphicMama – “Graphic Design Trends 2024 – Grids and Visible Borders” (grilles visibles, hiérarchie, structure)[^6]
    - https://graphicmama.com/blog/graphic-design-trends-2024/
- Kinsta / Elementor – rétrospectives des tendances 2018–2020 (flat, gradients, broken grid)[^1][^2]
    - https://kinsta.com/blog/web-design-trends/
    - https://elementor.com/blog/past-web-design-trends-2020/
- BI / dashboards UX – “BI Dashboard Design: 2025 UX Best Practices”[^11]
    - https://ukdataservices.co.uk/blog/articles/business-intelligence-dashboard-design.php
- BridxLabs – “Card UI Design Examples That Actually Work in 2025” (critiques du card sprawl)[^10]
    - https://bricxlabs.com/blogs/card-ui-design-examples
- Google Design – “Config – Takeaways from Figma’s 2024 Conference” (focus sur systèmes, variables, cohérence)[^19]
    - https://design.google/library/config-2024

Si tu veux, on peut faire un deuxième tour uniquement orienté “règles pour ton générateur” : par exemple, quels patterns bannir/limiter, quels paramétrages de grille / ratios imposer pour garder un “sentiment 2024+” quel que soit le secteur.
<span style="display:none">[^20][^21][^22][^23][^24][^25][^26][^27][^28][^29]</span>

<div align="center">⁂</div>

[^1]: https://kinsta.com/blog/web-design-trends/

[^2]: https://elementor.com/blog/past-web-design-trends-2020/

[^3]: https://designerup.co/blog/2024-design-trends-5-must-try-hero-layouts/

[^4]: https://www.awwwards.com/awwwards/collections/layout/

[^5]: https://www.youtube.com/watch?v=TjLxhLSrmGw

[^6]: https://graphicmama.com/blog/graphic-design-trends-2024/

[^7]: https://www.awwwards.com/inspiration/smashing-magazine

[^8]: https://www.hashbuilds.com/patterns

[^9]: https://www.thewebfactory.us/blogs/55-best-website-design-ideas-and-web-design-examples/

[^10]: https://bricxlabs.com/blogs/card-ui-design-examples

[^11]: https://ukdataservices.co.uk/blog/articles/business-intelligence-dashboard-design.php

[^12]: https://www.smashingmagazine.com/categories/design-patterns/

[^13]: https://www.smashingmagazine.com/2026/01/rethinking-pixel-perfect-web-design/

[^14]: https://samanthony.design/blog/trends-2024

[^15]: https://www.linkedin.com/pulse/12-colossal-website-designing-patterns-2018-siyaram-ray

[^16]: https://www.smashingmagazine.com/2024/12/new-front-end-features-for-designers-in-2025/

[^17]: https://www.awwwards.com

[^18]: https://www.smashingmagazine.com

[^19]: https://design.google/library/config-2024

[^20]: https://www.freshpies.co.uk/web-design-trends-in-2024-a-mid-year-review/

[^21]: https://www.en.sitew.com/How-to-design-a-website/web-design-trends

[^22]: https://www.bootstrapdash.com/blog/9-responsive-design-trends-in-dashboard-templates

[^23]: https://dsragland.com/top-web-design-trends-for-2024/

[^24]: https://www.reddit.com/r/web_design/comments/763z9j/what_are_some_web_design_patterns_that_need_to/

[^25]: https://www.youtube.com/watch?v=OSihRRirLVk

[^26]: https://www.youtube.com/watch?v=eMgywhSUD48

[^27]: https://www.luklagroup.com/en/change-adopt-en/config-2024-figma-reinvents-collaborative-design-with-outstanding-features/

[^28]: https://www.youtube.com/watch?v=5K-GMHdvyM4

[^29]: https://www.smashingmagazine.com/the-smashing-newsletter/smashing-newsletter-issue-540/

