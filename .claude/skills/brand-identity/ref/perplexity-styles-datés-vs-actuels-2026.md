# Styles UI : Datés vs Actuels 2026
## Référentiel pour Générateur de Brand Identity
> **Usage** : Ce rapport classe les 85 styles du CSV UX/UI Pro Max + identifie les styles manquants + documente les marqueurs AI slop. Conçu pour alimenter un système de génération automatique de brand identity (style-tiles HTML, landing pages, design systems) opérant sur tous secteurs.

***
## Partie 1 — Classification des styles UX/UI Pro Max
### Méthodologie d'évaluation
Les verdicts s'appuient sur : Awwwards SOTD/FWA winners 2025-2026, analyses de Codrops/Webzibition (2 200+ sites curés en 2025), Smashing Magazine, Creative Boom, The Branding Journal, et la documentation des patterns qui font gagner aux award platforms. Un style "ACTUEL" = présent régulièrement dans les SOTD et winners 2025-2026. Un style "DATÉ" = massivement critiqué post-2022 et quasi-absent des sites primés récents.[^1][^2]

***
### Styles Généraux (nos 1–68)
#### ✅ INTEMPORELS — Fondations qui ne vieillissent pas

| # | Style | Verdict | Raison (2-3 lignes) | Source | Exemple site récent |
|---|-------|---------|---------------------|--------|---------------------|
| 1 | **Minimalism & Swiss Style** | INTEMPOREL | Fondation du design web depuis les années 50. Présent en continu sur SiteInspire et Awwwards, quel que soit le cycle de tendances. Jamais en déclin car il s'adapte à chaque époque sans perdre sa pertinence. | [^2][^3] | Linear.app, Stripe (redesigns successifs) |
| 8 | **Accessible & Ethical Design** | INTEMPOREL | Pas un style esthétique mais une contrainte de base. WCAG 2.2 et AA/AAA sont des exigences légales en UE (EAA 2025). Ne sera jamais "daté" car c'est un impératif fonctionnel et légal. | [^2] | Tous les sites primés post-2024 |
| 12 | **Flat Design** | INTEMPOREL (évolué) | Le flat "pur" de 2013 est daté. Mais le flat modernisé — avec hiérarchie, micro-relief et typographie forte — reste la base de 90% des UI actuelles. À distinguer du "flat générique" AI slop. | [^4][^5] | Notion, Figma, Framer |
| 17 | **Inclusive Design** | INTEMPOREL | Principe transversal, non un style. Concerne l'accessibilité, le langage, la représentation. Aucun site élite 2025-2026 ne peut l'ignorer sans perdre en score Awwwards (30% du score = Usability). | [^2] | — (principe, pas un look) |
| 50 | **Swiss Modernism 2.0** | INTEMPOREL | Évolution directe du style Swiss original : grille rigoureuse, typographie expressive, espace blanc intentionnel. Présent dans chaque génération de winners Awwwards sans exception. | [^2][^3] | Awwwards winner "Exat Typeface" (Mars 2026) |
| 69 | **Bauhaus** | INTEMPOREL | Fonctionnalisme formel né en 1919, utilisé cycliquement. La version 2025-2026 intègre des typographies variables et des couleurs saturées primaires avec la même logique constructiviste. | [^6] | Portfolios design agencies Berlin |

***

#### 🟢 ACTUELS — Présents régulièrement sur Awwwards/SiteInspire/Codrops 2025-2026

| # | Style | Verdict | Raison (2-3 lignes) | Source | Exemple site récent |
|---|-------|---------|---------------------|--------|---------------------|
| 3 | **Glassmorphism** | ACTUEL (évolué) | Validé à l'échelle de l'OS par Apple Liquid Glass (iOS 26, juin 2025) — redesign le plus significatif depuis iOS 7 selon Apple[^7]. En 2026, la technologie GPU rattrape l'ambition esthétique. Le glassmorphism brutal/saturé de 2021 est daté ; la version raffinée avec backdrop-blur 10-20px reste premium. | [^8][^7][^9] | Awwwards HM "Glassmorphism with Dark & Light Theme" (Juin 2025) |
| 4 | **Brutalism** | ACTUEL | Présent en continu sur Awwwards dans la catégorie portfolios/editorial. Toggl a utilisé un design brutalist avec mini-games, cité par des practitioners[^10]. Le Brutalism pur reste une déclaration de positionnement anti-corporate. | [^11][^10] | Toggl.com |
| 5 | **3D & Hyperrealism** | ACTUEL | Three.js catégorie Awwwards = winner quasi-hebdomadaire en 2025-2026[^12]. Spline démocratise la 3D accessible. Les sites B2B premium intègrent 3D scènes pour produits physiques. Coût élevé = signal de craft. | [^13][^14][^15] | Lacoste Members Experience (Merci-Michel), Boucheron Quatre 20th (Merci-Michel) |
| 6 | **Vibrant & Block-based** | ACTUEL | Couleurs primaires bloquées, typographie XXL, hiérarchie hard. Très présent dans les landing pages SaaS 2025, mais risque de saturation imminente. Fonctionne encore fort pour le branding B2C/culture. | [^16][^17] | — |
| 7 | **Dark Mode (OLED)** | ACTUEL | 82% des utilisateurs mobile préfèrent le dark mode en 2025[^18]. OLED = économie batterie 39-47%[^19]. Premium tech, crypto, creative tools. Risque : "generic dark premium SaaS" = AI slop zone. | [^20][^21][^18] | Linear, Vercel, Resend |
| 10 | **Aurora UI** | ACTUEL | Gradient mesh animé = standard des hero sections SaaS premium. Stripe, Linear, Vercel l'utilisent[^22]. Awwwards confirme la tendance multicolore avec blur et distortion[^23]. Risque de banalisation dans 12-18 mois. | [^22][^24][^23] | Stripe, Linear, Vercel |
| 14 | **Liquid Glass** | ACTUEL (émergent) | Lancé par Apple WWDC 2025 sur iOS 26[^7]. Translucide + réfraction lumière. Se propage vers le web via swiftUI aesthetic. Très jeune (juin 2025) donc non banalisé. Expertise requise pour l'implémenter correctement. | [^25][^9][^7] | Apple iOS 26 |
| 15 | **Motion-Driven** | ACTUEL | School of Motion documente des sites avec "choreographed transitions" et "scroll-triggered animations" qui définissent les winners 2026[^26]. GSAP = tech dominante. Parallax Awwwards = winners en continu 2025[^27]. | [^28][^27][^26] | SpaceX.com, Wodwo (Digital Silk) |
| 16 | **Micro-interactions** | ACTUEL | 30% du score Awwwards repose sur l'Usability[^2] dont les micro-interactions font partie. Hover states, cursor behaviors, transitions = critères de jugement explicites. | [^2] | Made With GSAP (Awwwards HM Mars 2026) |
| 23 | **Minimal & Direct** (Landing Page) | ACTUEL | Version landing page du Minimalism. Copy-first, CTA immédiat, espace blanc généreux. Pattern dominant pour les SaaS à conversion élevée. | [^2] | Linear, Resend, Planetscale |
| 27 | **Storytelling-Driven** | ACTUEL | Scroll storytelling + cinematic experiences = trend identifié dans plusieurs rapports 2025-2026[^29][^30]. Parallax + audio = multi-sensoriel. Les narratives Awwwards winners 2025 sont quasi-systématiquement storytelling-first. | [^28][^30][^26] | The Goonies by Joseph Berry, Blue Desert (Adoratorio) |
| 38 | **Neubrutalism** | ACTUEL | "A très fort momentum en 2025" selon Clovertechnology[^11]. Bejamas le documente comme anti-template, léger, accessible[^31]. Dominant creator economy et Gen Z. SVGator confirme que "ses éléments distinctifs sont encore prévalents en 2026"[^32]. | [^11][^31][^32][^33] | Awwwards: Toggl, Linear History, Pika.art |
| 39 | **Bento Box Grid** | ACTUEL | 67% des top 100 SaaS ProductHunt l'utilisent sur homepage[^34]. Apple a popularisé le pattern en 2023, depuis adopté massivement. +47% dwell time, +38% CTR selon senorit.de[^35]. Risque de banalisation croissant en 2026. | [^36][^35][^34] | Apple product pages, Notion, Framer |
| 42 | **Organic Biophilic** | ACTUEL | Earthy tones (terracotta, olive, clay), formes organiques, textures naturelles. Seahawk Media documente des sites en 2026[^37]. Pantone Mocha Mousse 2025 ancre la tendance chromatique. Différent de la "nature générique" IA. | [^37][^38] | Patagonia, Airbnb |
| 46 | **Dimensional Layering** | ACTUEL | Profondeur sans 3D réelle : scroll parallax, z-index intentionnel, overlapping elements. Proche du Motion-Driven mais avec une logique spatiale spécifique. Fréquent dans les winners Awwwards 2025-2026. | [^27][^2] | — |
| 47 | **Exaggerated Minimalism** | ACTUEL | Espace blanc extrême, typographie unique hypertrophiée, palette réduite à 1-2 couleurs. Signature des agences premium (Instrument, Fantasy). Différent du minimalisme "propre et simple". | [^2][^3] | Awwwards winner "Bleibtgleich'25" (Portfolios Mars 2026) |
| 48 | **Kinetic Typography** | ACTUEL | Typography animée = "lettres vivantes"[^39]. Spotify Wrapped = cas d'école. Fontfabric documente les variable fonts kinétiques en 2025[^40]. Awwwards a une catégorie dédiée Typography Honors. | [^40][^39][^41][^42] | Awwwards Typography Honors Sep 2025 |
| 49 | **Parallax Storytelling** | ACTUEL | Parallax = catégorie Awwwards avec winners continus jusqu'en Oct 2025[^27]. SpaceX utilise full-bleed photography + scroll-triggered parallax[^28]. Technique mature mais toujours récompensée si bien exécutée. | [^28][^27][^43] | SpaceX, The Goonies, Lacoste |
| 53 | **Bento Grids** | ACTUEL | Identique au #39 (doublon dans le CSV). Même verdict. | [^35][^34] | — |
| 58 | **Biomimetic / Organic 2.0** | ACTUEL | Version avancée de l'organique : textures qui imitent le vivant, formes fractales, animations qui "respirent". Au-delà des formes "blob" génériques. Branding différenciateur pour wellness, food, cosmétiques. | [^37] | Madalena Studio pour Crucible (bacteria cork logo) |
| 62 | **Interactive Cursor Design** | ACTUEL | Dynamic cursor = cité comme trend 2026 par WP Creative[^16]. Magnetic cursors, follower cursors = marqueur d'artisanat. Présent dans les portfolios Awwwards comme signal de craft. | [^16][^2] | Awwwards portfolios 2025-2026 |
| 64 | **3D Product Preview** | ACTUEL | AR/3D product pages = trend e-commerce fort 2025-2026[^44]. Android XR + Apple Vision Pro accélèrent l'adoption[^44]. Model element HTML maintenant supporté nativement sur Safari visionOS[^45]. | [^13][^44][^15] | Sites e-commerce premium |
| 65 | **Gradient Mesh / Aurora Evolved** | ACTUEL | Évolution du gradient aurora : mesh gradient, formes irrégulières, blur + distortion. Awwwards documente des multicoloured gradients avec "irregular shapes with blur and distortion effects"[^23]. Actif mais risque de banalisation (→ CYCLIQUE dans 12-18 mois). | [^22][^24][^23] | Stripe, Vercel |
| 66 | **Editorial Grid / Magazine** | ACTUEL | SiteInspire a 458 sites dans la catégorie "Editorial, Grid Layout"[^46]. Multi-column, mix headlines/images = standard pour culture/média/portfolio. ColibriWP documente +30% session duration[^47]. | [^48][^47][^46] | Awwwards winner "Composites.archi" (Sparkk, Mars 2026) |
| 67 | **Chromatic Aberration / RGB Split** | ACTUEL (niche) | Glitch esthétique pour IT/gaming/entertainment. Weblium le documente en 2026 comme signal de "technologie imprévisible"[^49]. Très niche — pas transversal. À éviter pour corporate, finance, santé. | [^49][^50] | Sites gaming, festivals IT |
| 68 | **Vintage Analog / Retro Film** | ACTUEL | "35mm film aesthetic" utilisé par OpenAI pour ChatGPT campagne 2025 (anti-AI crafting)[^51]. Grain, textures argentiques, tonalités désaturées. Signal fort d'authenticité humaine. Trend en montée 2025-2026. | [^51][^52][^53] | OpenAI ChatGPT campaign 2025 |

***

#### 🟡 CYCLIQUES — En vogue mais à surveiller (bascule possible dans 12-18 mois)

| # | Style | Verdict | Raison | Source |
|---|-------|---------|--------|--------|
| 9 | **Claymorphism** | CYCLIQUE (déclin) | Populaire 2021-2023, maintenant associé au "Corporate Memphis 3D". LogRocket note qu'il "n'est pas à la pointe" en 2024[^54]. Encore utilisé pour les app icons (iMessage, Facebook Messenger)[^54] mais pas pour les sites primés. | [^55][^56][^54] |
| 11 | **Retro-Futurism** | CYCLIQUE (pic 2024-2025) | Neon grids, chrome, glitch retro = peak en 2024-2025. Figma le cite comme trend portfolio/entertainment[^57]. Vaporwave revival 2025 lui est lié[^58]. Risque de déclin si trop généralisé. | [^58][^57][^50] |
| 19 | **Soft UI Evolution** | CYCLIQUE | Version évoluée du neumorphism classique — utilisé stratégiquement pour health/wellness/fintech boutique[^59]. DesignRush documente des cas où le Soft UI + WCAG = performant. Pas de site élite en showcase systématique. | [^59][^60][^61] |
| 40 | **Y2K Aesthetic** | CYCLIQUE (déclin) | Peak en 2023-2024. Awwwards l'a récompensé (fa-So-La Akihabara, Sept 2023)[^62]. La tendance Vaporwave 2025 le prolonge[^58] mais le Y2K "pur" commence à saturer. | [^63][^62][^58][^64] |
| 41 | **Cyberpunk UI** | CYCLIQUE (déclin) | Fort en 2020-2022 (Cyberpunk 2077 effect). Encore présent en gaming/crypto. Absent des sites non-entertainment primés en 2025-2026. | [^65][^66] |
| 43 | **AI-Native UI** | CYCLIQUE (montant) | Chat interfaces, streaming responses, loading states "pensants". Très neuf donc pas encore saturé. Vitaly Friedman documente les "Design Patterns For AI Interfaces" en 2026[^67][^68]. | [^67][^69][^70] |
| 44 | **Memphis Design** | CYCLIQUE (déclin) | Revival 2022-2024 documenté[^71][^72]. Neo-Memphis = retour mainstream avec retailers[^71]. En 2026, le mouvement Naïve Design absorbe une partie de son énergie. Risque de saturation rapide. | [^71][^72] |
| 45 | **Vaporwave** | CYCLIQUE (pic 2025) | "Retour en force en 2025" selon Alibaba[^58] — fatigue digitale + nostalgie 2000s. Dribbble reste le hub principal. Attention : trop niche pour un usage transversal. | [^58][^73] |
| 51 | **HUD / Sci-Fi FUI** | CYCLIQUE (niche stable) | Présent en continu dans gaming/défense/data viz. Absent hors de ces niches dans les winners 2025-2026. À utiliser uniquement pour des secteurs où ce référentiel est attendu. | [^66] |
| 55 | **Spatial UI (VisionOS)** | CYCLIQUE (montant) | Non-niche selon DesignFest : "plus une niche avec Apple Vision Pro et Meta Quest 3"[^74]. Apple WWDC 2025 spatial web features[^45]. Mais adopté principalement dans des contexts premium/R&D. | [^45][^74][^70] |
| 57 | **Gen Z Chaos / Maximalism** | CYCLIQUE (pic 2024-2025) | Layouts fluides, anti-grille, maximalisme expressif. Très fort pour creator economy et Gen Z[^33][^10]. Risque de saturation si mal exécuté. | [^33][^10][^75] |
| 59 | **Anti-Polish / Raw Aesthetic** | CYCLIQUE (montant fort) | "Anti-AI Crafting" = "tendance qui définira 2026" selon Landor/Graham Sykes[^51]. Imperfection intentionnelle, surfaces texturées, marques du geste humain. Très fort momentum. | [^76][^51][^52] |
| 60 | **Tactile Digital / Deformable UI** | CYCLIQUE (émergent) | Interfaces qui réagissent physiquement aux gestes (GSAP + Three.js). Rare sur le web en 2025-2026 = signal de craft différenciateur. | [^15][^2] |
| 61 | **Nature Distilled** | CYCLIQUE | Version abstraite de l'organique biophilique : couleurs nature distillées (sage, clay, moss) sans references visuelles explicites. Lié aux earthy palettes 2025-2026. | [^16][^77] |

***

#### 🔴 DATÉS — À éviter pour des designs "élite 2026"

| # | Style | Verdict | Raison précise | Source |
|---|-------|---------|----------------|--------|
| 2 | **Neumorphism (pur)** | DATÉ | "Pure neumorphism 2020 — strict, low-contrast, monochromatic — is unequivocally a dated trend"[^78]. Problèmes d'accessibilité (WCAG AAA impossible), visuellement "boring" selon le créateur lui-même Michał Malewicz[^56]. Survit uniquement dans une version hybride (Soft UI Evolution). | [^78][^56] |
| 13 | **Skeuomorphism (classique)** | DATÉ / Revival niche | Le skeuomorphism "traditionnel" (boutons réalistes, cuir, ombres épaisses) reste associé à iOS 6 pre-Jony Ive[^79]. Un "Light Skeuomorphism" raffiné revient timidement en 2025-2026[^80] mais sans présence dans les sites primés. Réservé aux niches (apps musicales, retro gaming). | [^81][^79][^82][^83] |
| 52 | **Pixel Art** | DATÉ (mainstream) / ACTUEL (niche) | En tant qu'esthétique transversale de site : daté. En tant que choix intentionnel pour gaming/culture/indie brands : actuel. Indie pixel-art games = $400M en 2024[^84]. Sur le web grand public : signal de niche, pas de professionnalisme. | [^85][^86][^84][^87] |
| 18 | **Zero Interface** | DATÉ | Concept "invisible UI" de 2017-2020 porté par des apps vocal-first. La réalité de 2025 : les interfaces hybrides ont remplacé ce concept théorique. Voice-First (#63) est la version actuelle. | — |

***

#### ⚫ SPÉCIALISÉS — Styles landing pages (nos 20-27) et Dashboard (nos 28-37)

Ces styles sont des **patterns de conversion**, pas des esthétiques globales. Leur verdict s'analyse différemment.

| # | Style | Verdict | Note |
|---|-------|---------|------|
| 20 | Hero-Centric Design | INTEMPOREL | Structure fondamentale. Toujours pertinente si le hero est visuellement fort. |
| 21 | Conversion-Optimized | INTEMPOREL | Principe UX universel. Non daté. |
| 22 | Feature-Rich Showcase | ACTUEL | Bento grid = version 2025 de ce pattern. |
| 24 | Social Proof-Focused | INTEMPOREL | Logos clients, testimonials = standard de conversion. |
| 25 | Interactive Product Demo | ACTUEL | Motion + 3D product preview = peak 2025-2026. |
| 26 | Trust & Authority | INTEMPOREL | Applicable à tout secteur. |
| 28-37 | Dashboards (8 sous-styles) | ACTUEL | Dark mode dominant, dense data viz. Linear + vercel aesthetic est le standard 2025-2026. |

***

#### Styles Mobile (nos 69-85)

| # | Style | Verdict | Note |
|---|-------|---------|------|
| 69 | Bauhaus Mobile | INTEMPOREL | Constructivisme adapté mobile. |
| 70 | Minimalist Monochrome | INTEMPOREL | N&B ou monochrome = fondation intemporelle. |
| 71 | Modern Dark Cinema Mobile | ACTUEL | OLED + cinematic = premium mobile 2025. |
| 72 | SaaS Mobile High-Tech Boutique | ACTUEL | Linear/Vercel aesthetic sur mobile. |
| 73 | Terminal CLI Mobile | CYCLIQUE (niche) | Dev tools, crypto. Très niche. |
| 74 | Kinetic Brutalism Mobile | ACTUEL | Neubrutalism adapté mobile avec animation. |
| 75 | Flat Design Mobile Touch-First | INTEMPOREL | Base universelle. |
| 76 | Material You (MD3) | ACTUEL | Google recommandation officielle 2025. Dynamic color system. |
| 77 | Neo Brutalism Mobile | ACTUEL | Même verdict que #38 Neubrutalism. |
| 78 | Bold Typography Mobile Poster | ACTUEL | Typography-as-hero sur mobile = fort en 2025-2026. |
| 79 | Academia Scholarly | CYCLIQUE | Serif élégant, vieux livres. Niche mais cohérent pour éducation/culture. |
| 80 | Cyberpunk Mobile HUD | CYCLIQUE (déclin) | Gaming niche uniquement. |
| 81 | Bitcoin DeFi Mobile | CYCLIQUE | Crypto secteur uniquement. |
| 82 | Claymorphism Mobile | CYCLIQUE (déclin) | App icons OK, pas les sites. |
| 83 | Enterprise SaaS Mobile | ACTUEL | Clean, dense, accessible = standard B2B. |
| 84 | Sketch Hand-Drawn Mobile | ACTUEL (montant) | Lié au Naïve Design trend 2026. |
| 85 | Neumorphism Mobile | DATÉ | Même verdict que #2 pur. |

***
## Partie 2 — Styles actuels 2025-2026 manquants dans UX/UI Pro Max
Ces styles sont documentés par des sources élites (Awwwards, Codrops, Creative Boom, The Branding Journal) comme dominants en 2025-2026 mais absents des 85 entrées du CSV.

***
### A. Naïve Design / Handmade Digital
**Description visuelle** : Formes asymétriques, lignes tremblantes, typographie "crayonnée", couleurs vives sans dégradés, personnages illustrés à la main, textures papier/crayon/peinture. Intentionnellement imparfait mais parfaitement calculé dans son imperfection.

**Pourquoi actuel** : DesignRush documente que c'est "la tendance graphique qui redéfinit le branding en 2026". Kittl's 2026 Design Trend Report identifie le "handmade digital" comme shift central. Adobe confirme une hausse de 30% des recherches pour les éléments hand-drawn. Réponse directe au flooding d'outputs AI hyperpolished.[^52][^53][^88]

**Exemples** : Acne Studios × Michael McGregor, Gail's Bakeries (Christopher Brown printmaking), campagne ChatGPT OpenAI sur 35mm film.[^51][^53][^89]

**Sources** :[^53][^90][^89][^88][^52]

***
### B. Anti-AI Crafting / Craft-Core
**Description visuelle** : Photographie 35mm grain argentique, sets construits à la main, textures analogiques (tissu, argile, liège, bactéries cultivées), lumière naturelle physique, imperfections visibles du matériau. Opposé du studio perfect lighting AI.

**Pourquoi actuel** : Graham Sykes (Global ECD Landor) : "Designers are putting their hands back on the work — literally. When algorithms flood the world with flawless flatness, the marks of the maker become signal". Trend n°1 identifié par Creative Boom pour 2026.[^51]

**Marqueurs distinctifs vs Naïve Design** : Le Craft-Core utilise de vrais matériaux physiques photographiés (≠ simulation digitale d'imperfection du Naïve Design).

**Exemples** : Burberry Cross-Stitch Knight Life campaign, Madalena Studio pour Crucible (bacteria cork logo).[^51]

**Sources** :[^52][^53][^51]

***
### C. Adaptive Motion Identity / Living Brand Systems
**Description visuelle** : Logos et systèmes visuels fluides — logos "fondants", palettes de couleurs flexibles qui évoluent selon le contexte, motion design intégré à l'identité de marque, non plus des assets statiques. "Identités vivantes".

**Pourquoi actuel** : The Branding Journal identifie comme trend central 2026 : "Visual identities: from fixed systems to lived sensations. Logos and identity systems are designed to adapt across platforms, screens, and contexts". Texture + mouvement + son intégrés à la marque.[^91]

**Exemples** : Identités de marques qui "bougent" nativement (Studio Dumbar, Interbrand 2026 work).[^92][^91]

**Sources** :[^2][^91]

***
### D. Warmth Minimalism / Quiet Luxury Digital
**Description visuelle** : Minimalisme avec chaleur émotionnelle — teintes chaudes (crème, miel, caramel, terracotta), typographies serif expressives, espace blanc "respirant", photographie naturaliste non-stylisée, grain analogique léger. S'oppose au minimalisme froid "startup generique".

**Pourquoi actuel** : Pantone Mocha Mousse Couleur de l'Année 2025. WP Creative documente le shift "natural, muted tones, soft pastels, smooth gradients, moving away from bright neon". La "Quiet Luxury" du fashion entre dans le digital.[^16]

**Exemples** : Brands wellness premium, cosmétiques naturels, food artisanal 2025-2026.

**Sources** :[^37][^77][^16]

***
### E. Hypertypography / Text-First Architecture
**Description visuelle** : La typographie comme unique élément de composition — pas d'images, pas d'illustrations, uniquement du texte à différentes échelles, poids, styles. Grandes masses de caractères en fond, overlapping type, typographies variables qui "bougent". Palettes minimalistes 1-2 couleurs.

**Pourquoi actuel** : Awwwards a une catégorie Typography Honors spécifique qui prime quasi mensuellement en 2025-2026. "Exat Typeface" par Studio Size (Awwwards Honor Award Mars 2026). UXpilot documente "Bold typography and kinetic text" comme "fondation du design moderne".[^93][^94]

**Exemples** : Awwwards winner "Bleibtgleich'25" par Maksym Ponomarenko (portfolio dominant type), Awwwards HM "Exat Typeface" Studio Size.[^93]

**Sources** :[^40][^94][^3][^93]

***
### F. Expressive Organic / Anti-Grid Flow
**Description visuelle** : Layouts fluides sans grille rigide — formes organiques qui coulent, éléments qui s'enroulent autour du contenu, scroll qui "respire", transitions en morphing. Opposé du bento grid structuré. Souvent associé aux couleurs naturelles ou aux gradients organiques.

**Pourquoi actuel** : YouTube "Top 2026 Web Design Trends" : "organic web layouts and the anti-grid design trend are replacing rigid structures, creating more fluid, expressive interfaces". DevInterface confirme que "asymmetric artwork" et "organic shapes" comptent parmi les trends dominants 2026.[^95][^96][^29]

**Exemples** : Sites culture, arts, food artisanal.

**Sources** :[^29][^95]

***
### G. Immersive Scroll Narrative / Cinematic Scrolling
**Description visuelle** : Sites où le scroll est une chorégraphie narrative complète — entrance animations, section reveals, pace variable, sound design optionnel, camera-like transitions entre sections. L'expérience entière est une histoire en mouvement.

**Pourquoi actuel** : School of Motion documente les sites épics 2026 avec "carefully choreographed transitions, images that slide in from unexpected angles, text reveals with precise timing". Parallax Awwwards = winners en continu Oct 2025. Distinct du simple parallax : ici, le scroll définit une narrative structurée.[^27][^26]

**Exemples** : Blue Desert (Adoratorio, Three.js + GSAP), SpaceX.[^28][^14]

**Sources** :[^26][^28][^27]

***
## Partie 3 — Styles qui sentent l'IA (AI slop)
### Le diagnostic documenté
En août 2025, Adam Wathan (créateur Tailwind) s'est excusé publiquement pour avoir popularisé `bg-indigo-500` dans Tailwind UI : "I apologized for making every button in Tailwind UI use bg-indigo-500 five years ago, which caused every AI-generated interface on Earth to turn purple." Ce post a généré plus d'1 million de vues et a formalisé le terme "AI slop aesthetic".[^97]

Jack Pearce (février 2026) documente que "purple gradients dominated 'modern' web design in 2015-2020 (Instagram rebrand, Stripe/Twitch-style branding). LLMs were trained on that era's tutorials, CodePen demos, and SaaS landing pages, so they treat purple gradients as the default 'innovative' look".[^98]

***
### Marqueurs visuels du AI slop (liste complète)
**Couleurs & Gradients :**
- Purple/indigo accent (`#6366f1`, `bg-indigo-500`)
- Gradient violet → bleu sur fond blanc ou gris clair
- Aurora gradient générique sans intention (3 blobs animés centrés, toujours)
- Palettes "timides" équilibrées (3 couleurs pastel + gris)

**Typographie :**
- Inter en corps de texte ET en headline (mono-font)
- Roboto ou Arial comme fallback systématique
- Space Grotesk dès qu'on veut "faire moderne" (sur-utilisé en 2025)[^97]
- Hiérarchie limitée à "titre gros = header"

**Layout & Composants :**
- Hero centré : grand titre + sous-titre + bouton CTA seul
- Trois features en boxes (icône + titre + texte), systématiquement horizontales
- Cards avec `border-radius: 8-12px` + ombre `0.1 opacity` sur fond blanc
- Section "How it works" en 3 steps numérotés avec icônes
- Footer avec 4 colonnes égales

**Effets visuels :**
- Glassmorphism avec backdrop-blur générique (20px) + fond violet
- Subtle shadows "exactement 0.1 opacity"
- Dark mode = fond `#0a0a0a` + texte `#ffffff` + accent indigo

***
### Styles qui amplifient le slop AI (éviter en output système)
| Style | Pourquoi il produit du slop | Alternative singulière |
|-------|----------------------------|------------------------|
| **Aurora UI générique** | Les LLMs reproduisent le pattern "3 blobs animés + fond sombre + texte blanc" sans comprendre la composition d'origine (Stripe, Linear). Résultat : Aurora mal composé, couleurs incorrectes, bloom sans contrôle. | Gradient mesh custom avec palette non-standard (terracotta + sage + off-white), positions de blobs asymétriques et intentionnelles |
| **Generic Dark Premium SaaS** | `#0a0a0a` + Inter + indigo = pile de training data 2019-2022. Aucun caractère de marque. | Dark cinematic avec palette chromatique forte (Linear utilise des teintes slate/violet précises, pas du noir pur) |
| **Glassmorphism basique** | LLMs reproduisent le combo `backdrop-filter: blur(20px)` + `rgba(255,255,255,0.1)` + fond violet sans comprendre la hiérarchie de profondeur. | Glassmorphism avec fond chromatique propre à la marque, profondeur multi-couche intentionnelle, refraction Apple Liquid Glass |
| **3-Feature Grid** | Artefact de CTA pages 2018-2020 : 3 icônes en ligne = "standard SaaS". LLMs croient que c'est la structure universelle. | Bento grid asymétrique avec features de tailles différentes, ou feature-cards en scroll horizontal narrative |
| **Neumorphism générique** | LLMs génèrent systématiquement la combinaison `box-shadow: -5px -5px 15px` + fond gris clair + boutons ronds = neumorphism 2020 sans créativité. | Soft UI avec intention sectorielle (wellness → teintes organiques, fintech → gris bleuté précis) |

**Sources** :[^97][^99][^98][^100][^101]

***
## Partie 4 — Référentiel actionnable (37 styles recommandés)
Ce tableau consolide les styles optimaux pour un générateur de brand identity. Critères de sélection : ACTUEL ou INTEMPOREL, transversal (utilisable hors niche unique), différenciant (non AI slop), implémentable en HTML/CSS/JS.

| # | Style | Verdict | Utiliser pour | À éviter pour | Marqueurs anti-slop |
|---|-------|---------|---------------|---------------|---------------------|
| 1 | **Minimalism & Swiss Style** | INTEMPOREL | Enterprise, B2B SaaS, tech, finance, documentation | Entertainment, culture créative, food playful | Grille 12 colonnes stricte, 0 shadow, typographie à dessein (pas Inter par défaut) |
| 3 | **Glassmorphism (raffiné)** | ACTUEL | Fintech premium, SaaS modern, dashboards | Accessibilité critique, fond sombre peu contrasté | Backdrop-blur 10-15px max, fond chromatique propre à la marque, ≥ 4.5:1 contrast check |
| 4 | **Brutalism** | ACTUEL | Portfolios, tech blogs, counter-culture brands, agences créatives | Corporate conservateur, santé, finance traditionnelle | 0 border-radius, 0 transitions, polices système ou display fortes, couleurs primaires pures |
| 5 | **3D & Hyperrealism** | ACTUEL | Luxe, produits physiques (fashion, automotive, cosmétiques), gaming | Budgets limités, mobile-first bas de gamme | Three.js / Spline / R3F, shaders custom, mobile performance testé, pas de 3D "cheap" |
| 6 | **Vibrant & Block-based** | ACTUEL | B2C fort, culture, sport, food, startups Gen Z | Finance traditionnelle, santé, B2B corporate | Couleurs primaires non-génériques (pas l'indigo), typographie XXL à dessein |
| 7 | **Dark Mode Cinema** | ACTUEL | Tech premium, SaaS developer tools, crypto, gaming, logiciels créatifs | Santé, e-commerce généraliste, finance accessible | Fond `#0f0f0f` minimum (pas pur noir), palette chromatique précise (pas indigo générique) |
| 10 | **Aurora UI (maîtrisé)** | ACTUEL | SaaS hero, fintech, AI products | Secteurs "chaleureux" (food, santé wellness, luxe fashion) | Blobs en composition asymétrique, palette non-violet (teal+amber, crimson+sage...), texte toujours lisible |
| 14 | **Liquid Glass** | ACTUEL | Premium digital, luxury, Apple-ecosystem products | Accessibility-critical contexts | Backdrop + refraction combinés, transitions liées aux gestes, jamais sur fond pauvre en contraste |
| 15 | **Motion-Driven** | ACTUEL | Portfolios créatifs, entertainment, luxury, tech storytelling | Documents statiques, landing pages de conversion pure | GSAP choreography, pas de CSS aléatoire — chaque animation raconte quelque chose |
| 16 | **Micro-interactions** | ACTUEL | Tous secteurs (layer transversal, pas un style autonome) | — | Hover states intentionnels, cursor behaviors, transition timing 200-400ms cohérent |
| 19 | **Soft UI Evolution** | CYCLIQUE | Wellness, santé non-critique, apps de méditation, fintech boutique | Applications critiques (urgences, finance grand public) | Pastels non-génériques, pas la combinaison shadow-gris standard |
| 27 | **Storytelling-Driven** | ACTUEL | Luxury, culture, impact brands, portfolios créatifs | E-commerce conversion-only, landing pages directes | Scroll narrative avec pacing intentionnel, pas des transitions "scroll → opacity" basiques |
| 38 | **Neubrutalism** | ACTUEL | Creator economy, Gen Z brands, tech indé, SaaS disruptif, culture | Finance traditionnelle, santé, luxe classique | Thick black outlines, shadows offset, couleurs primaires vives non-standard, NO glassmorphism simultané |
| 39 | **Bento Box Grid** | ACTUEL | SaaS features, landing pages tech, portfolios produits, B2B | Longform editorial, storytelling linear | Blocs de tailles variées (pas uniform cards), hierarchy visuelle forte dans le plus grand bloc |
| 42 | **Organic Biophilic** | ACTUEL | Wellness, food, cosmétiques naturels, mode durable, immobilier premium | SaaS tech, finance, gaming | Earthy palette précise (pas les earth tones AI génériques), formes organiques vectorielles vraiment non-géométriques |
| 46 | **Dimensional Layering** | ACTUEL | Portfolios créatifs, luxury, cultural brands | Documents, dashboards, contenu dense | Z-index intentionnel, overlapping elements qui créent de la profondeur sans Three.js |
| 47 | **Exaggerated Minimalism** | ACTUEL | Luxury, mode, architecture, agencies premium | SMB généraliste, e-commerce produits nombreux | Une seule typographie display hypertrophiée, espace blanc "actif" pas vide, palette 1-2 couleurs max |
| 48 | **Kinetic Typography** | ACTUEL | Entertainment, culture, événements, portfolios, agences créatives | Documentation, dashboards, B2B enterprise | Variable fonts si possible, animation liée à l'interaction (pas auto-play systématique) |
| 49 | **Parallax Storytelling** | ACTUEL | Luxury, culture, grands récits de marque | Landing pages de conversion directe, mobile-first strict | Multi-speed layers intentionnels (pas tous à la même vitesse), testé mobile |
| 50 | **Swiss Modernism 2.0** | INTEMPOREL | Corporate premium, architecture, éditorial, culture institutionnelle | Brands "fun", food, gaming | Grille stricte MAIS typographie expressive forte, accent couleur unique assumé |
| 53 | **Bento Grids** | ACTUEL | Idem #39 | Idem #39 | Idem #39 |
| 57 | **Gen Z Chaos / Maximalism** | CYCLIQUE | Gen Z brands, beauty, musique, mode streetwear | Corporate, B2B, finance, santé | Layouts intentionnellement anti-grille, typographies clashantes choisies (pas générées aléatoirement) |
| 58 | **Biomimetic Organic 2.0** | ACTUEL | Cosmétiques bio, food artisanal, wellness avancé, impact | SaaS tech, finance, B2B corporate | Textures inspirées du vivant réel (grain de bois, veine de feuille), mouvements "respirant" |
| 59 | **Anti-Polish / Raw** | CYCLIQUE | Artisans, brands indé, culture, résistance corporate | Entreprises qui vendent de la fiabilité/conformité | Textures genuinement artisanales (pas des filtres AI), typographies "vraies" à la main |
| 62 | **Interactive Cursor** | ACTUEL | Layer transversal pour portfolios, luxury, gaming, agences | Mobile-only, SaaS corporate dense | Cursor follower avec physics (spring), magnetic hover, non-gimmicky |
| 64 | **3D Product Preview** | ACTUEL | E-commerce produits physiques, automotive, luxe, B2B industriel | Services purs, B2B software abstrait | Spline pour assets simples, Three.js pour interactions complexes, toujours fallback image |
| 65 | **Gradient Mesh Aurora** | ACTUEL | SaaS hero (palette non-violette), fintech, AI products | Food organique, wellness nature, luxury classique | Couleurs non-génériques, composition mesh asymétrique, 2-3 couleurs max bien choisies |
| 66 | **Editorial Grid** | ACTUEL | Culture, médias, publishing, portfolios agencies, marques culturelles | E-commerce produits, SaaS dashboards | Multi-column layout intentionnel, mix hierarchy types (headline + body + quote), pas de "magazine template" |
| **N/A** | **Naïve Design** | ACTUEL (émergent fort) | Brands artisanales, culture, youth, beauty indie, food créatif | Finance, tech enterprise, santé, legal | Lignes intentionnellement tremblantes, couleurs vives non-gradient, typographie "crayonnée" vraie |
| **N/A** | **Craft-Core / Anti-AI** | ACTUEL (montant) | Luxury "handmade", food artisanal premium, culture, mode | Contexts qui requièrent précision technique | Texture physique réelle photographiée, jamais simulée ; grain argentique, surfaces palpables |
| **N/A** | **Warmth Minimalism** | ACTUEL | Wellness, cosmétiques, food premium, mode durable, immobilier | B2B tech, gaming, fintech agressif | Palette chaude précise (Mocha Mousse, terracotta, crème ivoire), serif expressif, NO flat cold white |
| **N/A** | **Hypertypography** | ACTUEL | Agences créatives, culture, mode, portfolios | E-commerce image-heavy, SaaS feature-riche | 1 typographie display forte (pas Inter), couleurs réduites à 1-2, espace blanc actif |
| **N/A** | **Expressive Organic** | ACTUEL | Culture, food, wellness, portfolios créatifs | B2B corporate, dashboards, documentations | Layout sans grille rigide, morphing shapes, palette biomorphique |
| **N/A** | **Immersive Scroll Narrative** | ACTUEL | Luxury, entertainment, cultural brands, grands lancements | Landing pages de conversion directe | GSAP ScrollTrigger choreography, narrative structurée (pas juste des animations random au scroll) |
| **N/A** | **Adaptive Motion Identity** | ACTUEL | Brands digitales native, tech consumer, entertainment | Institutions, B2B conservative | Logo system qui "vit" (SVG animé natif), palette flexible par contexte |
| 1 | **Minimalism & Swiss Style** | INTEMPOREL | (rappel ligne en tête) | | |
| 50 | **Swiss Modernism 2.0** | INTEMPOREL | (rappel ligne en tête) | | |

***
## Sources utilisées (triées par crédibilité)
### Plateformes de référence awards / élites
- [Awwwards — Winning websites patterns 2025-2026](https://www.utsubo.com/blog/award-winning-website-design-guide)[^2]
- [Awwwards SOTD parallax winners](https://www.awwwards.com/websites/parallax/)[^27]
- [Awwwards Three.js winners (SOTD & DEV weekly)](https://www.awwwards.com/websites/three-js/)[^12]
- [Awwwards March 2026 Honor Awards](https://fr.linkedin.com/company/awwwards)[^93]
- [Codrops 2025 Year in Review — Webzibition 2,200+ sites](https://tympanus.net/codrops/2025/12/29/2025-a-very-special-year-in-review/)[^1]
- [SiteInspire Editorial Grid Layout category](https://www.siteinspire.com/websites/categories/editorial/grid-layout)[^46]
### Apple — Liquid Glass (source primaire officielle)
- [Apple Newsroom — Liquid Glass design announcement](https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/)[^7]
- [Apple WWDC25 — Meet Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/)[^102]
- [Raw.studio — Liquid Glass analysis](https://raw.studio/blog/liquid-glass-apples-subtle-masterstroke-toward-a-spatial-digital-future/)[^9]
### Experts & agences reconnues
- [Adam Wathan (Tailwind) — AI Purple apology + AI slop documentation](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website)[^97]
- [Graham Sykes / Landor — Anti-AI Crafting trend 2026](https://www.creativebloq.com/design/graphic-design/texture-warmth-and-tactile-rebellion-the-big-graphic-design-trends-for-2026)[^51]
- [Jack Pearce — Purple gradient origins analysis](https://www.jackpearce.co.uk/notes/purple-gradient-ai-aesthetics/)[^98]
- [Kristian Valtersen / Dawn Studio — AI slop fix video Dec 2025](https://www.youtube.com/watch?v=NRE4kv8RS68)[^99]
- [The Branding Journal — Visual identities 2026 shift](https://www.thebrandingjournal.com/2026/01/top-branding-design-trends-2026/)[^91]
- [DesignRush — Naive Design 2026](https://www.designrush.com/best-designs/print/trends/naive-design-trend-2026)[^53]
- [Kittl — 10 graphic design trends 2026](https://www.kittl.com/blogs/graphic-design-trends-2026/)[^88]
- [School of Motion — 10 websites with great animation 2026](https://www.schoolofmotion.com/blog/10-websites-with-great-animation-in-2026)[^26]
### Analyses sectorielles fiables
- [Lindsay Marsh Substack — Design Trends 2026: Imperfection & Rebellion](https://lindsaymarsh.substack.com/p/design-trends-2026-imperfection-rebellion)[^103]
- [Refuel Creative — Top 4 web design trends 2026](https://www.refuelcreative.com.au/blog/top-4-website-design-and-user-experience-trends-to-look-out-for-in-2026)[^33]
- [Gezar.dk — 11 web design trends 2026 (avec démos live)](https://gezar.dk/en/blog/web-design-trends-2026)[^22]
- [Bejamas — Neubrutalism web design trend](https://bejamas.com/blog/neubrutalism-web-design-trend)[^31]
- [LogRocket — Claymorphism in web design](https://blog.logrocket.com/ux-design/what-is-claymorphism-web-design/)[^54]
- [Seahawk Media — Biophilic website design 2026](https://seahawkmedia.com/design/biophilic-website-design-examples/)[^37]
- [Clovertechnology — Neo-Brutalism 2025 takeover](https://www.clovertechnology.co/insights/how-neo-brutalism-took-over-digital-design-in-2025)[^11]
- [Withlore — Best 3D website examples 2026](https://www.withlore.co/blog/best-3d-website-examples/)[^15]
- [orpetron.com — 10 award-winning Three.js websites](https://orpetron.com/blog/10-award-winning-websites-pushing-boundaries-with-three-js/)[^14]

---

## References

1. [2025: A Very Special Year in Review - Codrops](https://tympanus.net/codrops/2025/12/29/2025-a-very-special-year-in-review/) - A look back at the ideas, experiments, and people that shaped a remarkable year at Codrops.

2. [Award-Winning Web Design: Judging Criteria Decoded - Utsubo](https://www.utsubo.com/blog/award-winning-website-design-guide) - 4 award platforms scored and compared. Awwwards, FWA, Webby, CSSDA criteria breakdowns, 8–24 week ti...

3. [assets.awwwards.com/awards/element/2026/03 ...](https://latest.gallery/ref/capture-assets-awwwards-com-awards-element-2026-03-69a41553e35500030-1775162787984) - Design reference: assets.awwwards.com/awards/element/2026/03/69a41553e3550003056970.mp4

4. [Why choose Material Design over Flat? - Fingent](https://www.fingent.com/blog/why-choose-material-design-over-flat/) - Ever since its release, material design has been much talked about. After all, what is it all about?...

5. [Flat Design vs. Material Design: what’s your flavor?](https://uxplanet.org/flat-design-vs-material-design-whats-your-flavor-43a27c295f62?gi=0d97d54b8015) - Flat design vs material design — what’s best? We take a dive into material design as well as another...

6. [Claymorphism: Will It Stick Around? : r/web_design - Reddit](https://www.reddit.com/r/web_design/comments/tgwss1/claymorphism_will_it_stick_around/) - Overview of claymorphism in web design. Top web design trends for 2024. Best tools for responsive we...

7. [Apple introduces a delightful and elegant new software design](https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/) - Apple previewed a new software design, crafted with Liquid Glass, that makes apps and system experie...

8. [Glassmorphism: What It Is and How to Use It in 2026](https://invernessdesignstudio.com/glassmorphism-what-it-is-and-how-to-use-it-in-2026) - Discover what glassmorphism is and how to implement this frosted-glass UI trend in 2026. Learn core ...

9. [Liquid Glass: Apple's Subtle Masterstroke Toward a Spatial Digital ...](https://raw.studio/blog/liquid-glass-apples-subtle-masterstroke-toward-a-spatial-digital-future/) - Liquid Glass is a training ground. Apple is building a bridge between flat screens and 3D environmen...

10. [10 Website Design Trends 2026: Build Modern Sites Without Code](https://lovable.dev/guides/website-design-trends-2026) - Discover the top website design trends for 2026 including AI personalization, kinetic typography, an...

11. [How Neo-Brutalism Took Over Digital Design in 2025](https://www.clovertechnology.co/insights/how-neo-brutalism-took-over-digital-design-in-2025) - A few years ago, Brutalism in web design was still considered niche. But today, what we're really se...

12. [Best Three.js Websites | Web Design Inspiration - Awwwards](https://www.awwwards.com/websites/three-js/) - Three.js is a widely-used JavaScript library for creating 3D graphics and animations in web browsers...

13. [The Best Web Design Trends for 2026 - Fireart Studio](https://fireart.studio/blog/the-best-web-design-trends/) - 3D Illustrations and Hyperrealism. Three-dimensional images, illustrations, and effects are everywhe...

14. [10 Award-Winning Websites Pushing Boundaries with Three.js](https://orpetron.com/blog/10-award-winning-websites-pushing-boundaries-with-three-js/) - Three.js has revolutionized the way developers bring 3D experiences to the web, enabling interactive...

15. [Best 3D Website Examples in 2026: What Makes Them Work](https://www.withlore.co/blog/best-3d-website-examples/) - Spline for simple 3D elements you can add to existing pages. Three.js/React Three Fiber for custom i...

16. [Top 20 Web Design Trends [2026] - WP Creative](https://wpcreative.com.au/web-design-trends/) - In 2026, sustainable web design focuses on creating websites that are faster, more efficient, and en...

17. [Ranking: the best web design trends in 2025](https://www.elias.studio/en/blog/post/les-meilleures-tendances-de-webdesign-en-2025) - Discover the web design trends of 2025: neo-brutalism, sensory maximalism, AI and dark fashion. Tran...

18. [Dark Mode Design Trends for 2025: Should Your Startup Adopt It?](https://altersquare.io/dark-mode-design-trends-for-2025-should-your-startup-adopt-it/) - Explore the pros and cons of adopting dark mode for your startup, focusing on user preferences, read...

19. [Why Dark Mode Design Converts Better: 2026 Guide For CEOs](https://www.digitalsilk.com/digital-trends/dark-mode-design-guide/) - Learn why dark mode design increases conversions in 2026. Discover its impact and why businesses sho...

20. [Why Light Mode Refuses To...](https://ciellumiere.com/web-design-blog/dark-mode-vs-light-mode-which-one-will-dominate-in-2025) - Dark mode or light mode? Explore their pros, cons, and what users prefer in websites . Dark mode sav...

21. [Dark Mode vs Light Mode: The Complete UX Guide for 2025](https://altersquare.io/dark-mode-vs-light-mode-the-complete-ux-guide-for-2025/) - Explore the crucial differences between dark and light mode, their impact on user experience, and ho...

22. [11 Web Design Trends in 2026 (With Live Demos) | Gezar](https://gezar.dk/en/blog/web-design-trends-2026) - See the 11 web design trends dominating 2026 - with interactive demos you can try right in your brow...

23. [Trendy Gradients in Web Design](https://www.awwwards.com/gradients-in-web-design-elements.html) - This year we have seen various multicoloured gradients with vibrant color palettes and irregular sha...

24. [Gradient design trend: Color shades play - Kittl Blog](https://www.kittl.com/blogs/gradient-design-trend-stl/) - Follow stunning gradient design trends with Kittl. Discover tips, tools, and inspiration to add smoo...

25. [“Liquid Glass” is the term Apple uses to define its design concept](https://newsroundtheclock.com/liquid-glass-is-the-term-apple-uses-to-define-its-design-concept/) - Apple unveiled its "Liquid Glass" design at WWDC 2025, paving the way for future products including ...

26. [10 Websites with Great Animation in 2026 - School of Motion](https://www.schoolofmotion.com/blog/10-websites-with-great-animation-in-2026) - Great web animation guides users, tells stories, and creates memorable experiences. Here are 10 webs...

27. [Best Parallax Websites | Web Design Inspiration - Awwwards](https://www.awwwards.com/websites/parallax/) - Awesome Parallax Website Designs for Inspiration. Selection of Awwwards winning parallax websites or...

28. [21 Best Parallax Scrolling Websites 2026 - Colorlib](https://colorlib.com/wp/parallax-scrolling-websites/) - Get inspired by this collection of stunning parallax scrolling websites. Learn from the best, copy a...

29. [Vertical Photographs & Mobile...](https://www.theedigital.com/blog/web-design-trends) - Is your website working for or against you? Learn about the top web design trends for 2026, and how ...

30. [14 of the Best Parallax Scroll Examples for 2025 - Memberstack](https://www.memberstack.com/blog/14-of-the-best-parallax-scroll-examples-for-2025) - This post will teach you how to implement parallax scrolling effects, why parallax can enhance user ...

31. [Neubrutalism - UI Design Trend That Wins The Web - Bejamas](https://bejamas.com/blog/neubrutalism-web-design-trend) - Neubrutalism is a trend in web design focusing on creating structures and layouts that are simple bu...

32. [What Is The Neubrutalism Web Design Trend? A Visual Guide](https://www.svgator.com/blog/what-is-neubrutalism/) - Neubrutalism is a web design trend that has been gaining traction in recent years, with its distinct...

33. [Top 4 website design and user experience trends to look out for in ...](https://www.refuelcreative.com.au/blog/top-4-website-design-and-user-experience-trends-to-look-out-for-in-2026) - Discover the definitive website trends of 2026. From Liquid Glass and Neo-Brutalism to Agentic UX, l...

34. [Bento Grid Design: How to Create Modern Modular Layouts in 2026](https://landdding.com/blog/blog-bento-grid-design-guide) - Learn how to design stunning bento grid layouts that organize content beautifully. Step-by-step guid...

35. [Bento Grid Design: The Hottest UI Trend of 2026](https://senorit.de/en/blog/bento-grid-design-trend-2025) - Bento Grid Design is a widely adopted UI pattern in 2026, inspired by Japanese bento boxes. The modu...

36. [The Bento Box Effect: Why Modular Grids Dominate 2025 Design](https://onecodesoft.com/blogs/the-bento-box-effect-why-modular-grids-dominate-2025-design) - Dec 08, 2025 - Discover why Bento Grids are taking over web design in 2025. Learn how these modular ...

37. [Best Biophilic Website Design Examples in 2026: Top Picks](https://seahawkmedia.com/design/biophilic-website-design-examples/) - Biophilic website design brings that experience to life by blending natural elements with digital in...

38. [Biophilic Design 2025 | Nature-Inspired Home for Modern Interiors](https://designjadugar.com/biophilic-design-2-0-nature-inspired-homes-in-2025/) - In Biophilic Design 2025, designers focus on deeper integration—using real textures, organic shapes,...

39. [Typography Trends 2025: The 5 Biggest Styles Shaping Design](https://www.designity.com/blog/typography-trends) - Discover the biggest typography trends shaping 2025. See how design is evolving to capture attention...

40. [Top 10 Typography Trends for 2025 - Fontfabric™](https://www.fontfabric.com/blog/top-typography-trends-2025/) - Discover the 2025's top type trends—from variable fonts to playful serifs. Stay ahead in design with...

41. [7 Kinetic Typography Trends 2025: AI Revolution + Examples](https://www.upskillist.com/blog/top-7-kinetic-typography-trends-2025/) - Explore the top trends in kinetic typography for 2026, including AI tools, 3D effects, and user-resp...

42. [Kinetic Typography in 2026: Examples, Patterns & UX Risk](https://www.digitalsilk.com/digital-trends/kinetic-typography/) - Explore 10 kinetic typography examples, key patterns and when animated text improves clarity or crea...

43. [Best Parallax Effects Website Designs of 2026 - DesignRush](https://www.designrush.com/best-designs/websites/parallax-effects) - Looking for innovative visual storytelling? Find a collection of the top parallax effects website de...

44. [Web design trends 2026: How AR and 3D are shaping the future of ...](https://www.pausarstudio.de/pausar-news/web-design-trends-2026-how-ar-and-3d-are-shaping-the-future-of-websites/) - By combining their websites product-pages with 3D and augmented reality, they create a customer expe...

45. [What’s new for the spatial web - WWDC25 - Videos](https://developer.apple.com/videos/play/wwdc2025/237/) - Discover the latest spatial features for the web on visionOS 26. We'll cover how to display inline 3...

46. [The Best Editorial, Grid Layout Websites | Siteinspire](https://www.siteinspire.com/websites/categories/editorial/grid-layout) - Discover Editorial, Grid Layout websites A showcase of the web’s finest design + talent

47. [10 Inspiring Web Layouts to Elevate Your Site in 2025 - Embark Studio](https://embark-studio.com/blog/10-inspiring-web-layouts-to-elevate-your-site-in-2025) - 10 Inspiring Web Layouts to Elevate Your Site in 2025 | Discover 10 innovative web layouts set to el...

48. [Magazine Website Redesign: Strategy, UX & Layout Ideas for 2026](https://flip180media.com/tips-for-periodical-publishers/magazine-website-redesign-strategy-ux-layout-ideas-for-2026/) - Revamp your magazine website with proven strategies for design and user engagement. Discover actiona...

49. [Top 10 Web Design Trends for 2026 - Weblium Blog](https://weblium.com/blog/best-web-design-trends/) - It is also worth using chromatic aberration — an effect in which colors (red, blue, green) “flare” a...

50. [6 Graphic & Web Design Trends for 2026 - Lange Creative Lab](https://langecreativelab.au/6-graphic-web-design-trends-for-2026/) - In 2026 it is about taking nostalgic cues and pairing them with modern digital techniques. Think neo...

51. [Texture, warmth and tactile rebellion: the big graphic design trends ...](https://www.creativebloq.com/design/graphic-design/texture-warmth-and-tactile-rebellion-the-big-graphic-design-trends-for-2026) - "In 2025, we gave AI a visual identity with bold 3D forms and unapologetically digital aesthetics do...

52. [Why naive design leads the anti-perfection design trend of 2026 - Kittl](https://www.kittl.com/blogs/naive-design-trend-stl/) - Trend forecasts for 2026 point to a return of “handmade digital” aesthetics. Naive Design feels appr...

53. [Naive Design Trend 2026: Why Imperfection Is Winning in Branding](https://www.designrush.com/best-designs/print/trends/naive-design-trend-2026) - Naive design is redefining branding in 2026 with hand-drawn visuals, imperfect typography, and human...

54. [What is claymorphism in web design? - LogRocket Blog](https://blog.logrocket.com/ux-design/what-is-claymorphism-web-design/) - Claymorphism is still applicable for apps that are considering phasing out the very popular flat des...

55. [Claymorphism | Aesthetics Wiki - Fandom](https://aesthetics.fandom.com/wiki/Claymorphism) - Claymorphism is a user interface design trend that focuses on 3D visuals mimicking the texture of cl...

56. [Claymorphism in User Interfaces | SquarePlanet - HYPE4.Academy](https://hype4.academy/articles/design/claymorphism-in-user-interfaces) - Claymorphism in User Interfaces. How we crave for an illusion of depth on our flat screens. Let's ta...

57. [Top Web Design Trends for 2026 - Figmawww.figma.com › resource-library › web-design-trends](https://www.figma.com/resource-library/web-design-trends/) - Want to stay ahead of the curve? Learn about the latest Web design trends and how to apply them in F...

58. [Why Did Vaporwave Aesthetics Make A Comeback In 2025 Digital ...](https://www.alibaba.com/product-insights/why-did-vaporwave-aesthetics-make-a-comeback-in-2025-digital-nostalgia-trends.html) - Explore why vaporwave aesthetics surged back in 2025 as digital nostalgia trends reshaped internet c...

59. [Is Neumorphism Still Relevant in Web Design? 2025 Agency Guide](https://www.designrush.com/best-designs/websites/trends/neumorphism-website) - Learn how top agencies use neumorphism in 2025 to boost traffic, brand engagement, and UX—when appli...

60. [Neumorphism vs Skeuomorphism in 2025 - Netstager Blog](https://blog.netstager.com/neumorphism-vs-skeuomorphism-ui-trends-2025/) - Neumorphism is a newer design trend that started becoming popular around 2020. It takes the idea of ...

61. [Neumorphism vs. Glassmorphism: What's Winning in 2025 Web ...](https://www.opendesignsin.com/blog/neumorphism-vs-glassmorphism-whats-winning-in-2025-web-design/) - The digital design world sees Neumorphism and Glassmorphism emerge as dominant styles that transform...

62. [Y2K AESTHETICS - Awwwards](https://www.awwwards.com/inspiration/y2k-aesthetics-fa-so-la-akihabara) - Y2K AESTHETICS from Fa-So-La AKIHABARA · Desktop · Mobile · Intro · KAWAII TRANSITION · CURIOUS FOOT...

63. [Y2K aesthetic for web design projects: Everything you need to know](https://webflow.com/blog/y2k-aesthetic) - The history of Y2K era aesthetics, how it has influenced web design, and how to use it in your proje...

64. [Y2K Web Design: Modernizing the Retro-Futuristic Trend](https://www.sivadesigner.in/blog/y2k-retro-futuristic-design-guide/) - Master the Y2K web design trend without sacrificing UX. Learn how to use glitch effects, chrome text...

65. [UI trends for 2077 | SquarePlanet - HYPE4.Academy](https://hype4.academy/articles/design/ui-trends-for-2077) - Cyberpunk 2077 has inspired me to take a look at the interfaces in the year 2077, and what I think w...

66. [25 Web Design Trends to Watch in 2025 - DEV Community](https://dev.to/watzon/25-web-design-trends-to-watch-in-2025-e83) - 6. Futuristic, Sci-Fi Gaming UI Aesthetics. Interfaces inspired by games and sci-fi films are on the...

67. [Designing For Complex UIs, 2026 Edition - SmashingConf Amsterdam](https://smashingconf.com/freiburg-2026/workshops/vitaly-friedman-complex-uis/) - Complex UIs don't have to be complicated. In this in-person workshop with Vitaly Friedman, UX consul...

68. [Smashing Magazine — For Web Designers And Developers](https://www.smashingmagazine.com) - Brought to you by Design Patterns For AI Interfaces, friendly video courses on UX and design pattern...

69. [State of AI UX For Designers in 2026 with Vitaly Friedman - YouTube](https://www.youtube.com/watch?v=qWaYYDTLTgM) - State of AI UX For Designers in 2026 with Vitaly Friedman — November, 2025. 1.6K views · 4 months ag...

70. [18 Predictions for 2026 - UX Tigers](https://www.uxtigers.com/post/2026-predictions) - Summary: Accelerating AI capabilities will shift focus from raw intelligence to autonomous agents an...

71. [Memphis Trend 2025: Bold Revival in Modern Design & Interiors](https://www.accio.com/business/memphis_trend) - Consistent Narrative: All sources consistently point to a revival of Memphis design as a counter-tre...

72. [Memphis Design - Aesthetics Wiki - Fandom](https://aesthetics.fandom.com/wiki/Memphis_Design) - Due to the clear lineage between pure Memphis Design and Memphis Lite, they are often conflated in r...

73. [25 ESSENTIAL DESIGN TRENDS FOR 2025!! #design ... - Instagram](https://www.instagram.com/reel/DMbmwd_MKOz/) - DESIGN STYLES THAT WILL TREND IN 2026 CRAFTCORE DESIGN SWISS BRUTALISM VAPORWAVE UI MEMPHIS REVIVAL ...

74. [Top 10 UX UI Design Trends That Will Dominate 2026 | Designfest](https://designfest.framer.media/blogs/top-uxui-design-trends-will-dominate) - Designing for "Spatial Continuity". With the widespread adoption of devices like the Apple Vision Pr...

75. [Top 2026 Web Design Trends](https://www.youtube.com/watch?v=DQOCFw_23FI) - Web Design Trends 2026 worth knowing as a web designer or developer. While AI is popular for graphic...

76. [The Rise of Anti-Design in 2025: Embracing Imperfection in Web ...](https://rent-a-website.hashnode.dev/the-rise-of-anti-design-in-2025-embracing-imperfection-in-web-design) - This bold approach to design breaks the rules, embraces imperfection, and prioritises human connecti...

77. [Biophilic Design in 2026: Why Nature-Inspired Interiors Are Your ...](https://www.homeplannerapp.com/post/biophilic-design-in-2026-why-nature-inspired-interiors-are-your-home-s-new-heartbeat) - At its core, biophilic design is about mimicking nature's essence indoors to nurture our well-being....

78. [Neumorphism in 2026: Is It Here to Stay? - Digital Kulture - Webbb.ai](https://www.webbb.ai/blog/neumorphism-in-2026-is-it-here-to-stay) - Learn about Neumorphism in 2026: Is It Here to Stay? and discover how visuals, videos, UI, and UX sh...

79. [Flat Design vs. Material Design - Are They So Similar?](https://www.motocms.com/blog/en/flat-design-vs-material-design/) - A Few Years ago Flat beat Skeuomorphism. Today we can see another battle: Flat Design vs. Material D...

80. [Trends for 2026 Series: Web Design Web design is entering a new ...](https://www.instagram.com/p/DSbMp9lk1RR/) - ... Skeuomorphism A refined revival of real-world cues: soft textures, gentle embossing, and tactile...

81. [Revival of Skeuomorphism: A Modern Twist on a Classic Trend - Arde](https://ardeint.com/revival-of-skeuomorphism-a-modern-twist-on-a-classic-trend/) - We have come to an understanding that skeuomorphism is indeed making a comeback in web design, albei...

82. [Skeuomorphism: The Return of Realistic Design](https://www.responsivedzn.com/post/skeuomorphism-the-return-of-realistic-design-in-2024) - The return of skeuomorphism suggests a broader trend towards more personalized and visually rich dig...

83. [Skeuomorphisme : un retour inattendu en 2025 - Kryzalid](https://kryzalid.net/blogue-marketing-web/skeuomorphisme-un-retour-inattendu-en-2025/) - Le skeuomorphisme, ce style de design qui cherche à imiter des objets réels dans le monde numérique,...

84. [The Resurgence of Pixel Art: More Than Just Nostalgia?](https://logicsimplified.com/newgames/the-resurgence-of-pixel-art-more-than-just-nostalgia/) - Indie pixel-art games pulled in over $400 million in 2024. Interest in pixel logo design has increas...

85. [Pixel Art Trends 2025: The Future of Digital Creativity - Pixeliowall](https://pixeliowall.com/blogs/pixel-art-trends-2025-future-of-digital-creativity/) - Discover the top pixel art trends in 2025, including AI-assisted creation, 3D pixel fusion, neon cyb...

86. [Pixel Art Trend 2025: What's New in Digital Creativity? - Accio](https://www.accio.com/business/pixel-art-trend-2025) - The design landscape for 2025 is characterized by a blend of nostalgia, technological advancement, a...

87. [Modern Pixel Art Design Trends and Tools for 2025](https://stanislav-kondrashov.ghost.io/pixel-art-digital-design-2025/) - Explore pixel art's evolution, key features, tools, and future trends shaping modern design in 2025 ...

88. [Steal the start: 10 graphic design trends 2026 by Kittl - Kittl Blog](https://www.kittl.com/blogs/graphic-design-trends-2026/) - Get ahead with Kittl's exclusive preview of the top 10 graphic design trends 2026! Discover emerging...

89. [Six surprising illustration trends for 2026 | Creative Boom](https://www.creativeboom.com/inspiration/six-surprising-illustration-trends-for-2026/) - We asked a selection of artists and their representatives to cast their minds ahead and visualise wh...

90. [Naive Design: The Quirky Design Trend Taking Over 2026](https://designerly.com/naive-design-the-quirky-design-trend-taking-over-2026/) - Naive design utilizes bright colors and wobbly lines to provide an authentic alternative to AI-gener...

91. [Top Branding & Design Trends For 2026 - The Branding Journal](https://www.thebrandingjournal.com/2026/01/top-branding-design-trends-2026/) - Top Branding & Design Trends For 2026 · 1. Strategic Branding: AI Agents, Human Connection, and Felt...

92. [The Best Brand Design Agencies in 2026 (Reviewed by Experts)](https://www.awesomic.com/blog/brand-design-agencies) - Discover the best brand design agencies in 2026 with expert reviews to help you pick the perfect tea...

93. [awwwards. | LinkedIn](https://fr.linkedin.com/company/awwwards) - awwwards. | 264,846 followers on LinkedIn. The awards that recognize the talent and effort of the be...

94. [4. Minimalism And Maximalism](https://uxpilot.ai/blogs/web-design-trends-2026) - <p>Stay ahead with the latest web design trends in 2026, from minimalism to AI-driven layouts, shapi...

95. [2026 Web Design Trends You Need to Know - YouTube](https://www.youtube.com/watch?v=rFyOIWMwRdg) - I 100% agree with the human-made, i think it will be a major if not the biggest selling point in 202...

96. [Web design trends in 2026 - DevInterface](https://www.devinterface.com/en/blog/web-design-trends-in-2026) - Web design 2026: trends, examples and practical advice for choosing the right style based on your pr...

97. [Why Your AI Keeps Building the Same Purple Gradient Website](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website) - There's now a documented phenomenon called “AI slop” where AI-generated designs are instantly recogn...

98. [Where does that purple gradient come from? - Jack Pearce](https://www.jackpearce.co.uk/notes/purple-gradient-ai-aesthetics/) - Exploring why AI-generated designs often default to purple gradients and what this reveals about tra...

99. [Why Most AI Design Looks Like "AI Slop" (And How to Fix It)](https://www.youtube.com/watch?v=NRE4kv8RS68) - I discovered why every AI landing page looks the same and found a ridiculously simple fix... 

Artic...

100. [AI Purple Problem: Make Your UI Unmistakable - DEV Community](https://dev.to/jaainil/ai-purple-problem-make-your-ui-unmistakable-3ono) - This is the AI Purple Problem AI tools and template-driven stacks nudging teams toward the same indi...

101. [aiGradientSlop : r/ProgrammerHumor - Reddit](https://www.reddit.com/r/ProgrammerHumor/comments/1mrffif/aigradientslop/) - Discuss purple gradient aesthetics in AI art. Most relatable programmer struggles. Best programming ...

102. [Meet Liquid Glass - WWDC25 - Videos - Apple Developer](https://developer.apple.com/videos/play/wwdc2025/219/) - Liquid Glass unifies Apple platform design language while providing a more dynamic and expressive us...

103. [Design Trends 2026! Imperfection, Rebellion, and the Return of ...](https://lindsaymarsh.substack.com/p/design-trends-2026-imperfection-rebellion) - I can see Glassmorphism evolving with this trend to produce distortion through see-through textures.

