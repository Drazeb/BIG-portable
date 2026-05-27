# Styles bibliothèque BIG — Catalogue curé 2026

> **Rôle** : Catalogue curé des styles officiels reconnus, utilisé par le sub-agent styliste (Phase 3B-7a) pour choisir UN style (ou mix dominant×modulateur max) qui incarne le concept narratif d'un brief.
>
> **Source** : Référentiel Perplexity 2026 (`ref/perplexity-styles-datés-vs-actuels-2026.md`) + 7 styles manquants documentés Partie 2 du même rapport. Tous les verdicts (INTEMPOREL / ACTUEL / CYCLIQUE / DATÉ) sont CITATIONNELS — ils viennent du rapport, pas de jugement personnel.
>
> **Mise à jour** : à chaque nouveau rapport Perplexity. La structure (Partie A / B / C, format de fiche) est stable.

---

## Mode d'emploi

Le styliste lit la **Partie A** intégralement (les 34 styles à utiliser : 27 du référentiel actionnable Perplexity + 7 styles manquants Partie 2), suit le protocole de matching de `ref/styles-matching-protocol.md`, applique les 5 règles de `ref/style-matching-rules.md`, et produit une fiche de style structurée en sortie.

La **Partie B** liste les styles à éviter (DATÉS + CYCLIQUES en déclin) avec leur raison d'exclusion. Le styliste NE LES CHOISIT JAMAIS.

La **Partie C** documente les marqueurs AI slop transverses qui peuvent contaminer N'IMPORTE QUEL style légitime. Chaque fiche de Partie A référence ces marqueurs dans son champ "Marqueurs anti-slop".

> ⚠ **Pas de champ "Secteurs ✅ / Secteurs ❌"** dans les fiches — décision actée le 25 avril 2026. Cristalliser une association `secteur ↔ style` est un piège à Ventre Mou structurel : le styliste serait orienté vers les codes visuels SECTORIELS (= ce qu'on cherche à FUIR avec le curseur B). Le matching se fait sur **concept narratif** (source PRINCIPALE) + **curseurs A×B** (calibrage) + **Ventre Mou du scoping** (codes à éviter selon B). Le secteur de la marque est une donnée de contexte, pas un critère de matching.

> ⚠ **Pas de champ "Compatibilités MIX (dominant) / (modulateur)"** dans les fiches — décision actée le 26 avril 2026. Cristalliser une association `style A ↔ styles B/C/D mixables` est le MÊME piège à Ventre Mou que les Secteurs, en version "style ↔ style" : le styliste tend à choisir parmi les mix les plus listés → convergence vers les usual mix. La validation d'un mix repose désormais sur les **règles 6 (cohérence système — même univers sensoriel)** et **7 (contraste structurel)** du fichier `ref/style-matching-rules.md`, vérifiées sémantiquement par le styliste lui-même + l'Avis du DA (auto-critique 3 axes). Un mix `Cyberpunk UI × Warmth Minimalism` ne passe pas la règle 6 (univers opposés) → le styliste DOIT le rejeter par cette règle.

---

## Structure des fiches Partie A

```markdown
### {N°}. {Nom officiel}

| Champ | Valeur |
|---|---|
| Verdict | INTEMPOREL / ACTUEL / CYCLIQUE |
| Source catalogue | Perplexity #{N} ou Partie 2 lettre {X} |
| Registre | Éditorial / Brutaliste / Minimaliste / Cinétique / Organique / Cinématographique / Tech / Crafty |

**Description officielle** : 3-4 phrases reprises du rapport Perplexity.

**Signatures visuelles à incarner** :
- 5-8 puces concrètes (typographie, surface, couleur, layout, micro-interactions, atmosphère)

**Marqueurs anti-slop** :
- 4-6 puces — ce qui distingue le style authentique de la version générée par LLM moyen.

**INTERDITS** :
- 4-6 puces — ce qui transforme le style en cliché ou bascule en slop.

**Références culturelles** :
- 3-5 marques/sites/designers vérifiables.

```

**Registre** (8 valeurs possibles) : pré-classification haut-niveau utilisée par l'étape 1 du protocole de matching (déclaration du TYPE de style recherché par croisement concept narratif × territoires) :
- **Éditorial** : héritage magazine/presse, multi-cols, hiérarchie typographique forte (Editorial Grid, Hypertypography, Swiss Modernism 2.0…)
- **Brutaliste** : bordures dures, anti-friendly, couleurs primaires bloquées (Brutalism, Neubrutalism, Vibrant Block-based…)
- **Minimaliste** : épure, espace blanc actif, parcimonie (Minimalism Swiss, Exaggerated Minimalism, Warmth Minimalism…)
- **Cinétique** : animation et interaction comme matière première (Motion-Driven, Kinetic Typography, Parallax Storytelling…)
- **Organique** : formes courbes, nature-inspired, anti-grille (Organic Biophilic, Biomimetic Organic 2.0, Expressive Organic…)
- **Cinématographique** : tension lumineuse, narrative scrollée, ambiance immersive (Dark Mode Cinema, Storytelling-Driven, Immersive Scroll…)
- **Tech** : SaaS premium, dashboards, interfaces denses (Bento Grid, Aurora UI, Glassmorphism…)
- **Crafty** : signal anti-AI, imperfections assumées, gestes humains (Naïve Design, Anti-AI Crafting, Anti-Polish Raw…)

---

# Partie A — Styles à utiliser


### 1. Minimalism & Swiss Style

| Champ | Valeur |
|---|---|
| Verdict | INTEMPOREL |
| Source catalogue | Perplexity #1 |
| Registre | Minimaliste |

**Description officielle** : Fondation du design web depuis les années 50. Présent en continu sur SiteInspire et Awwwards quel que soit le cycle de tendances. Jamais en déclin car il s'adapte à chaque époque sans perdre sa pertinence. Référence : Linear.app, Stripe (redesigns successifs).

**Signatures visuelles à incarner** :
- Grille 12 colonnes stricte, alignements parfaits
- Typographie expressive choisie à dessein (PAS Inter par défaut)
- Espace blanc abondant et structuré
- Hiérarchie typographique forte (sauts de taille marqués)
- Hairlines 1px comme séparateurs structurels
- Aucune ombre décorative — les blocs sont définis par le fond ou la grille

**Marqueurs anti-slop** :
- Pas d'Inter en mono-font (signal AI direct)
- Pas de "centered hero + 3 features cards" — c'est un template, pas du Swiss
- Pas de grille 12 colonnes invisible (grille doit être PERCEPTIBLE par les alignements même si les hairlines sont absentes)
- Une font de caractère assumée (Helvetica Neue / Söhne / Inter Display / GT America custom)

**INTERDITS** :
- Indigo / purple gradient en accent (AI slop)
- Cards uniformes 3×3 ou 4×3 sans hiérarchie (mur de cards)
- Footer 4 colonnes égales de liens (sitemap déguisé)
- Subtle shadow systématique 0 1px 3px rgba(0,0,0,0.1)

**Références culturelles** :
- Linear.app · Stripe · Müller-Brockmann (héritage) · Vercel (sobriété)


### 50. Swiss Modernism 2.0

| Champ | Valeur |
|---|---|
| Verdict | INTEMPOREL |
| Source catalogue | Perplexity #50 |
| Registre | Éditorial |

**Description officielle** : Évolution directe du style Swiss original : grille rigoureuse, typographie expressive, espace blanc intentionnel. Présent dans chaque génération de winners Awwwards sans exception. La version 2.0 intègre des typographies variables et un accent couleur unique assumé. Référence : Awwwards winner "Exat Typeface" (Mars 2026).

**Signatures visuelles à incarner** :
- Grille 12 colonnes STRICTE et VISIBLE (hairlines verticales possibles)
- Typographie Bodoni / Didone exploitée comme display expressif (italique + droit dialoguent)
- Espace blanc intentionnel et structuré (pas vide, il compose)
- UN seul accent couleur assumé (1-2 fois max par vue)
- Compositions asymétriques contrôlées (alignements parfaits mais non-symétriques)
- Numérotation technique visible (sections 01/02/03, micro-labels, chiffres tabulaires)
- Hairlines 1px comme séparateurs structurels (horizontaux et verticaux)

**Marqueurs anti-slop** :
- Italique Bodoni sur un MOT du titre (signature 2.0 vs Swiss 1.0)
- Folio + rubrique + numéro de section visibles (vocabulaire éditorial)
- Pas d'ornement décoratif (anti-pattern Swiss 1.0)
- Une seule couleur active par vue (parcimonie chromatique)

**INTERDITS** :
- Multi-color décoratif (Swiss = 1 accent, point)
- Shadows lourdes ou gradients chromatiques
- Formes courbes non-fonctionnelles
- Vignettage ou texture lourde
- Border-radius rond (Swiss = angles droits)

**Références culturelles** :
- Pentagram · Studio Size · Awwwards "Exat Typeface" (Mars 2026) · Base Design · Bureau Mirko Borsche


### 66. Editorial Grid / Magazine

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #66 |
| Registre | Éditorial |

**Description officielle** : SiteInspire a 458 sites dans la catégorie "Editorial, Grid Layout". Multi-column, mix headlines/images = standard pour culture/média/portfolio. ColibriWP documente +30% session duration avec ce pattern. Référence : Awwwards winner "Composites.archi" (Sparkk, Mars 2026).

**Signatures visuelles à incarner** :
- Multi-colonnes justifiées (2-3 cols avec hyphens auto)
- Lettrine drop-cap au début des articles
- Pull quote en italique avec filet d'accent latéral
- Masthead à 3 parties (folio gauche / titre central / numéro/édition droite)
- Numérotation romaine de sections (I, II, III)
- Hairlines 1px comme séparateurs entre blocs éditoriaux
- Hierarchie typographique éditoriale forte (display × body × caption)

**Marqueurs anti-slop** :
- Multi-column layout intentionnel (pas "magazine template" Pinterest)
- Mix hierarchy types (headline + body + quote, pas que des headlines)
- Folio + édition + numéro visibles (références éditoriales)
- Pull quote attribué (avec — Auteur)

**INTERDITS** :
- Hero centré titre + sous-titre + CTA (= template SaaS, pas editorial)
- 3-features grid avec icônes
- Cards uniformes sans hiérarchie
- Border-radius rond systématique

**Références culturelles** :
- Apartamento · Kinfolk · The Gentlewoman · NYT Magazine · Awwwards "Composites.archi" (Sparkk Mars 2026)


### 39. Bento Box Grid

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #39 (= #53 doublon CSV) |
| Registre | Tech / Minimaliste |

**Description officielle** : 67% des top 100 SaaS ProductHunt l'utilisent sur homepage. Apple a popularisé le pattern en 2023, depuis adopté massivement. +47% dwell time, +38% CTR selon senorit.de. Risque de banalisation croissant en 2026. Référence : Apple product pages, Notion, Framer.

**Signatures visuelles à incarner** :
- Tuiles de tailles VARIÉES (pas grille uniforme 3×3)
- Hiérarchie visuelle FORTE dans la tuile dominante
- Coins arrondis cohérents (12-24px) sur toutes les tuiles
- Fond légèrement teinté ou textured pour distinguer chaque tuile
- Chaque tuile a un rôle précis (USP, social proof, product shot, CTA secondaire)
- Mix de contenus dans les tuiles (texte, image, métrique, illustration)

**Marqueurs anti-slop** :
- Tuile dominante 2-3× plus grande que les autres (pas grille uniforme)
- Contenus DIFFÉRENTS dans chaque tuile (pas répétition icône+titre+texte)
- Densité contrôlée (chaque tuile respire, pas tassée)

**INTERDITS** :
- Grille 3×3 uniforme (= card sprawl Pinterest, anti-bento)
- Toutes les tuiles avec le même type de contenu (mur de cards déguisé)
- Border-radius incohérent entre tuiles
- Gradient violet dans une tuile (AI slop)

**Références culturelles** :
- Apple product pages · Notion · Framer · Linear (sections features)


### 47. Exaggerated Minimalism

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #47 |
| Registre | Minimaliste |

**Description officielle** : Espace blanc extrême, typographie unique hypertrophiée, palette réduite à 1-2 couleurs. Signature des agences premium (Instrument, Fantasy). Différent du minimalisme "propre et simple". Référence : Awwwards winner "Bleibtgleich'25" (Portfolios Mars 2026).

**Signatures visuelles à incarner** :
- UN seul élément fort par bloc (titre, sample typo, ou disque coloré)
- Paddings massifs (18-24vh par bloc)
- Typographie display hypertrophiée (clamp 12vw-22vw)
- Palette réduite visuellement à 2-3 couleurs actives par vue
- Pas de grille visible, asymétries tendues
- Accent couleur parcimonieux (1 par bloc)

**Marqueurs anti-slop** :
- Espace blanc ACTIF (composé), pas vide subi
- Typographie display CHOISIE pour ses détails (italique Bodoni, GT Sectra display)
- Asymétries INTENTIONNELLES (pas centered Bootstrap)
- Tension par la PROPORTION (texte petit + énorme)

**INTERDITS** :
- Hero centré "titre + sous-titre + CTA" (= Bootstrap, pas minimaliste élite)
- Inter / Helvetica par défaut
- Stock photography (anti-luxe)
- Manifesto poétique (pollution narrative)

**Références culturelles** :
- Instrument · Fantasy Interactive · Pentagram (sites produit) · Awwwards "Bleibtgleich'25"


### Hypertypography

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Partie 2 lettre E |
| Registre | Éditorial / Minimaliste |

**Description officielle** : La typographie comme unique élément de composition — pas d'images, pas d'illustrations, uniquement du texte à différentes échelles, poids, styles. Grandes masses de caractères en fond, overlapping type, typographies variables qui "bougent". Awwwards a une catégorie Typography Honors qui prime quasi mensuellement en 2025-2026. Référence : Awwwards winner "Bleibtgleich'25", "Exat Typeface" Studio Size.

**Signatures visuelles à incarner** :
- 1 typographie display forte (PAS Inter), exploitée comme matériau principal
- Couleurs réduites à 1-2 (texte vs fond, accent rare)
- Espace blanc actif autour des masses typographiques
- Variations dramatiques de taille (du caps 200vw aux body 16px)
- Overlap typographique intentionnel (titres qui débordent, se superposent)
- Animation typographique kinétique optionnelle (variable fonts)

**Marqueurs anti-slop** :
- Variable fonts si possible (axes weight, slant, optical size animés)
- Typographie CHOISIE (Cormorant, GT Sectra, Söhne Display, PP Editorial Old)
- Composition NON centrée (asymétries typographiques)
- Texte = MATIÈRE (pas information)

**INTERDITS** :
- Inter / Roboto / Helvetica par défaut
- Texte centré symétrique avec sous-titre + CTA
- Photos ou illustrations (= autre style)
- Glow / shadow / gradient sur le texte (anti-typographique)

**Références culturelles** :
- Awwwards Typography Honors (Sept 2025+) · Studio Size "Exat Typeface" · Pangram Pangram · Maksym Ponomarenko


### 3. Glassmorphism (raffiné)

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL (évolué) |
| Source catalogue | Perplexity #3 |
| Registre | Tech / Cinétique |

**Description officielle** : Validé à l'échelle de l'OS par Apple Liquid Glass (iOS 26, juin 2025). En 2026, la technologie GPU rattrape l'ambition esthétique. Le glassmorphism brutal/saturé de 2021 est daté ; la version raffinée avec backdrop-blur 10-20px reste premium. Référence : Awwwards HM "Glassmorphism with Dark & Light Theme" (Juin 2025).

**Signatures visuelles à incarner** :
- Backdrop-blur 10-15px max (PAS 20px+ qui rend le texte illisible)
- Fond chromatique propre à la marque (pas violet générique)
- Couches de profondeur multiples (élément flotté > arrière-plan > fond)
- Bordure subtile semi-transparente sur les surfaces glass
- Contraste texte vérifié ≥ 4.5:1 (accessibilité)
- Refraction ou distortion légère sur les bords (signature 2.0)

**Marqueurs anti-slop** :
- Backdrop-blur MODÉRÉ (10-15px max)
- Fond CHROMATIQUE intentionnel (pas gradient violet par défaut)
- Texte LISIBLE sur la surface glass (test contraste)
- Glass utilisé pour HIÉRARCHISER (pas partout)

**INTERDITS** :
- Backdrop-blur 20px+ + fond violet + texte blanc (= AI slop direct)
- Glass sur le CTA primaire (disparaît visuellement)
- Glass sur fond uni (perd l'effet de profondeur)
- Glass partout (= cosmétique sans sens)

**Références culturelles** :
- Apple iOS 26 Liquid Glass · Stripe Dashboard · Linear (modales) · Awwwards HM Juin 2025


### 4. Brutalism

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #4 |
| Registre | Brutaliste |

**Description officielle** : Présent en continu sur Awwwards dans la catégorie portfolios/editorial. Le Brutalism pur reste une déclaration de positionnement anti-corporate. Référence : Toggl.com.

**Signatures visuelles à incarner** :
- 0 border-radius (angles droits stricts)
- 0 transitions douces (changements d'état nets)
- Polices système ou display fortes (Helvetica brute, Times brute, system-ui)
- Couleurs primaires pures bloquées en aplats
- Compositions désordonnées maîtrisées (anti-grille perceptible)
- Bordures épaisses noires (3-6px solid) comme structure
- Espace blanc minimal (densité brute)

**Marqueurs anti-slop** :
- Bordures noires ÉPAISSES (3-6px) comme grille
- Aucun border-radius (anti-friendly)
- Couleurs PRIMAIRES PURES (rouge #FF0000, jaune #FFFF00, bleu #0000FF) ou très saturées
- Polices système ou DISPLAY brutes (pas Inter / Roboto)

**INTERDITS** :
- Border-radius (rompt l'esthétique brutaliste)
- Glassmorphism (style opposé)
- Transitions douces / easing physique
- Couleurs pastel ou sourdes
- Stock photography lisse

**Références culturelles** :
- Toggl.com · Bloomberg Businessweek · awsmd.com · Pawel Nolbert


### 14. Liquid Glass

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL (émergent) |
| Source catalogue | Perplexity #14 |
| Registre | Cinétique / Tech |

**Description officielle** : Lancé par Apple WWDC 2025 sur iOS 26. Translucide + réfraction lumière. Se propage vers le web via SwiftUI aesthetic. Très jeune (juin 2025) donc non banalisé. Expertise requise pour l'implémenter correctement. Référence : Apple iOS 26.

**Signatures visuelles à incarner** :
- Translucide + réfraction lumière (pas juste blur)
- Surfaces qui réagissent aux gestes/scroll (transitions liées à l'interaction)
- Profondeur multi-couches perceptible
- Reflet subtil sur les bords (signature liquid)
- Couleurs qui filtrent à travers la surface
- Fond chromatique riche derrière le glass

**Marqueurs anti-slop** :
- Refraction VRAIE (pas juste backdrop-blur)
- Transitions liées aux GESTES (scroll, hover, click)
- Profondeur HIÉRARCHISÉE (3+ niveaux distincts)
- Contraste préservé (lisibilité ≥ AA)

**INTERDITS** :
- Glassmorphism statique (= Glassmorphism, autre style)
- Fond pauvre en contraste derrière le glass
- Glass sur le CTA primaire
- Stack technique cheap (test mobile obligatoire)

**Références culturelles** :
- Apple iOS 26 Liquid Glass · WWDC25 demos · Raw.studio analysis


### 38. Neubrutalism

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #38 |
| Registre | Brutaliste |

**Description officielle** : "A très fort momentum en 2025" selon Clovertechnology. Bejamas le documente comme anti-template, léger, accessible. Dominant creator economy et Gen Z. SVGator confirme que "ses éléments distinctifs sont encore prévalents en 2026". Référence : Toggl, Linear History, Pika.art.

**Signatures visuelles à incarner** :
- Bordures épaisses noires (2-4px solid) sur les blocs clés
- Shadow offset NET sans blur (4-8px 4-8px 0 couleur)
- Couleurs primaires vives non-standard (pas rouge basique, plutôt #FF6B6B chaud, #FFDC00 jaune saturé, etc.)
- Border-radius modéré (4-12px max — ni 0 brutalist pur, ni 24px+ friendly)
- Typographie BOLD ou expressive (pas elegant)
- Fond blanc cassé ou crème (pas pur blanc)

**Marqueurs anti-slop** :
- Shadow offset NETTE 0 blur (pas shadow douce)
- Border NOIRE épaisse (pas border subtile)
- Couleurs primaires DISTINCTIVES (pas Tailwind defaults)
- Typographie bold ASSUMÉE

**INTERDITS** :
- Shadow douce blur 12px+ (anti-neubrutalism)
- Border-radius 16px+ (perd l'esthétique brute)
- Glassmorphism simultané (incompatibilité documentée)
- Inter / Roboto par défaut

**Références culturelles** :
- Toggl · Linear History page · Pika.art · Pawel Nolbert · Gumroad


### 65. Gradient Mesh / Aurora Evolved

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #65 |
| Registre | Tech / Cinétique |

**Description officielle** : Évolution du gradient aurora : mesh gradient, formes irrégulières, blur + distortion. Awwwards documente des multicoloured gradients avec "irregular shapes with blur and distortion effects". Actif mais risque de banalisation (CYCLIQUE dans 12-18 mois). Référence : Stripe, Vercel.

**Signatures visuelles à incarner** :
- Mesh gradient asymétrique (pas 3 blobs centrés)
- 2-3 couleurs MAX bien choisies (pas 5+)
- Couleurs NON-violet/indigo (teal+amber, crimson+sage, etc.)
- Blur + distortion sur les formes (irrégularité organique)
- Composition off-center (axe diagonal ou décalage assumé)
- Texte LISIBLE sur le mesh (pas texte directement sur gradient saturé)

**Marqueurs anti-slop** :
- Palette NON-générique (éviter purple/blue Stripe par défaut)
- Composition ASYMÉTRIQUE (pas 3 blobs symétriques)
- 2-3 couleurs (pas rainbow)
- Mesh organique (pas circles parfaits)

**INTERDITS** :
- Aurora générique 3 blobs symétriques violet+rose+bleu (= AI slop signature)
- Texte blanc sur gradient saturé (illisibilité)
- Mesh sur tout l'écran (perd l'effet de focal)

**Références culturelles** :
- Stripe · Vercel · Resend · Linear (sections hero)


### 19. Soft UI Evolution

| Champ | Valeur |
|---|---|
| Verdict | CYCLIQUE |
| Source catalogue | Perplexity #19 |
| Registre | Organique / Minimaliste |

**Description officielle** : Version évoluée du neumorphism classique — utilisé stratégiquement pour health/wellness/fintech boutique. DesignRush documente des cas où le Soft UI + WCAG = performant. Pas de site élite en showcase systématique — usage NICHE.

**Signatures visuelles à incarner** :
- Pastels NON-génériques (pas pastel Memphis)
- Surfaces relief subtil (différent du neumorphism dur)
- Border-radius généreux (16-24px)
- Ombres douces multi-couches (pas la combinaison shadow-gris standard)
- Couleurs apaisantes mais pas timides
- Hiérarchie par taille/poids (compense le manque de contraste)

**Marqueurs anti-slop** :
- Pastels CHOISIS (pas sortis d'une palette générique)
- Relief SUBTIL (pas neumorphism complet)
- Contraste WCAG vérifié (Soft UI peut casser l'accessibilité)
- Hiérarchie EXPLICITE (compense le manque de contraste)

**INTERDITS** :
- Neumorphism complet (style daté, voir Partie B)
- Pastels Memphis Design (= autre style)
- Tout au même niveau visuel (rompt la hiérarchie)
- Fonds gris clair systématique

**Références culturelles** :
- Calm · Headspace · apps wellness premium


### Anti-AI Crafting / Craft-Core

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL (montant fort) |
| Source catalogue | Partie 2 lettre B |
| Registre | Crafty / Cinématographique |

**Description officielle** : Graham Sykes (Global ECD Landor) : "Designers are putting their hands back on the work — literally. When algorithms flood the world with flawless flatness, the marks of the maker become signal". Trend n°1 identifié par Creative Boom pour 2026. Différent de Naïve Design : utilise de vrais matériaux physiques photographiés (≠ simulation digitale d'imperfection).

**Signatures visuelles à incarner** :
- Photographie 35mm grain argentique (pas filtre numérique)
- Textures analogiques RÉELLES (tissu, argile, liège, bactéries cultivées)
- Lumière naturelle physique (pas lighting parfait studio)
- Imperfections visibles du matériau
- Surfaces palpables (sensation de matière dans l'image)
- Compositions qui montrent le geste humain

**Marqueurs anti-slop** :
- Texture VRAIE photographiée (pas simulée)
- Lumière NATURELLE (pas studio perfect lighting AI)
- Imperfections ASSUMÉES (pas effacées)
- Différencier de Naïve Design (Craft = matériaux RÉELS, Naïve = imperfection DIGITALE)

**INTERDITS** :
- Studio perfect lighting AI
- Texture digitale simulée (perd le signal)
- Stock photography "diverse hands"
- Filtre Instagram vintage (pas authentique)

**Références culturelles** :
- Burberry Cross-Stitch Knight Life campaign · Madalena Studio pour Crucible (bacteria cork logo) · OpenAI ChatGPT 2025



### 7. Dark Mode (OLED) / Dark Mode Cinema

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #7 |
| Registre | Tech / Cinématographique |

**Description officielle** : 82% des utilisateurs mobile préfèrent le dark mode en 2025. OLED = économie batterie 39-47%. Premium tech, crypto, creative tools. Risque : "generic dark premium SaaS" = AI slop zone. Référence : Linear, Vercel, Resend.

**Signatures visuelles à incarner** :
- Fond sombre dominant `#0F0F0F` minimum (PAS pur noir `#000`)
- Palette chromatique précise (pas indigo générique)
- Texte crème `#F2F2F2` ou similaire (PAS blanc pur `#FFF`)
- Halos lumineux chauds en accents (radial-gradients diffus)
- Typographie cinematic (tailles généreuses, letter-spacing serré display)
- Tension lumière (zones très claires vs très sombres)

**Marqueurs anti-slop** :
- Fond `#0F0F0F` ou plus sombre TEINTÉ (pas pur noir)
- Accent CHAUD (terracotta, ambre) ou CHROMATIQUE précis (pas indigo générique)
- Texte CRÈME (pas blanc pur violent)
- Halos LUMINEUX intentionnels (création de profondeur)

**INTERDITS** :
- Fond pur noir `#000000` + Inter + indigo (= AI slop direct)
- Texte blanc pur `#FFF` (contraste violent amateur)
- Glow shadows `box-shadow: 0 0 Npx` sans offset
- Generic dark premium SaaS sans personnalité

**Références culturelles** :
- Linear · Vercel · Resend · SpaceX · Apple Pro Display


### 10. Aurora UI

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #10 |
| Registre | Tech / Cinétique |

**Description officielle** : Gradient mesh animé = standard des hero sections SaaS premium. Stripe, Linear, Vercel l'utilisent. Awwwards confirme la tendance multicolore avec blur et distortion. Risque de banalisation dans 12-18 mois (CYCLIQUE émergent). Référence : Stripe, Linear, Vercel.

**Signatures visuelles à incarner** :
- Blobs en composition ASYMÉTRIQUE (pas 3 blobs centrés)
- Palette NON-violette (teal+amber, crimson+sage, terracotta+vert forêt…)
- Animation lente et subtile (pas auto-play tape-à-l'œil)
- Texte TOUJOURS lisible sur le mesh
- Composition off-center
- 2-3 couleurs MAX bien choisies

**Marqueurs anti-slop** :
- Palette CHOISIE non-générique (pas violet+rose+bleu)
- Composition ASYMÉTRIQUE (pas 3 blobs symétriques)
- Texte lisible (contraste vérifié)
- Mesh ZONE focale (pas tout l'écran)

**INTERDITS** :
- 3 blobs animés centrés violet+rose+bleu (= AI slop signature)
- Mesh sur tout l'écran (perd l'effet hero)
- Texte directement sur zone saturée
- Animation rapide tape-à-l'œil

**Références culturelles** :
- Stripe · Linear · Vercel · Resend (sections hero)


### 42. Organic Biophilic

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #42 |
| Registre | Organique |

**Description officielle** : Earthy tones (terracotta, olive, clay), formes organiques, textures naturelles. Seahawk Media documente des sites en 2026. Pantone Mocha Mousse 2025 ancre la tendance chromatique. Différent de la "nature générique" IA. Référence : Patagonia, Airbnb.

**Signatures visuelles à incarner** :
- Earthy palette PRÉCISE (terracotta, sage, clay, mocha mousse, ocre)
- Formes organiques vectorielles vraiment non-géométriques (pas blobs simples)
- Textures naturelles (papier, lin, bois, pierre)
- Typographie humaniste ou serif chaleureux
- Compositions fluides (anti-grille rigide)
- Couleurs SOURDES (pas saturées)

**Marqueurs anti-slop** :
- Palette earthy PRÉCISE (pas "earth tones" génériques)
- Formes ORGANIQUES vectorielles (pas blobs simples)
- Typographie HUMANISTE / serif chaleureux
- Couleurs SOURDES authentiques

**INTERDITS** :
- "Earth tones" génériques AI (palette terne sans intention)
- Blobs simples (= autre style)
- Typographie froide (Inter, Roboto)
- Stock photography "nature lifestyle"

**Références culturelles** :
- Patagonia · Airbnb · Aesop · Pantone Mocha Mousse 2025


### 58. Biomimetic Organic 2.0

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #58 |
| Registre | Organique |

**Description officielle** : Version avancée de l'organique : textures qui imitent le vivant, formes fractales, animations qui "respirent". Au-delà des formes "blob" génériques. Branding différenciateur pour wellness, food, cosmétiques. Référence : Madalena Studio pour Crucible (bacteria cork logo).

**Signatures visuelles à incarner** :
- Textures inspirées du vivant RÉEL (grain de bois, veine de feuille, peau, mycélium)
- Mouvements "respirant" (animations subtiles cycliques)
- Formes fractales ou organiques avancées (pas blobs simples)
- Palette dérivée de la nature (avec subtilité)
- Photographie macro vivante (pas stock)

**Marqueurs anti-slop** :
- Textures VRAIES photographiées (pas Photoshop)
- Mouvement RESPIRANT (pas animation décorative random)
- Différenciation des "organic" génériques
- Détails biologiques précis

**INTERDITS** :
- Blobs simples (= Organic Biophilic basique)
- "Nature stock" génériques
- Animations infinies décoratives sans intention
- Filtres "wellness" prêts-à-l'emploi

**Références culturelles** :
- Madalena Studio (Crucible) · Aesop (cosmétiques avancées) · Patagonia avancée


### Warmth Minimalism / Quiet Luxury Digital

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Partie 2 lettre D |
| Registre | Minimaliste / Organique |

**Description officielle** : Minimalisme avec chaleur émotionnelle — teintes chaudes (crème, miel, caramel, terracotta), typographies serif expressives, espace blanc "respirant", photographie naturaliste non-stylisée. S'oppose au minimalisme froid "startup générique". Pantone Mocha Mousse Couleur de l'Année 2025.

**Signatures visuelles à incarner** :
- Palette chaude PRÉCISE (Mocha Mousse, terracotta, crème ivoire, miel)
- Serif expressif (Cormorant, Söhne Serif, GT Sectra)
- Espace blanc "respirant" (paddings massifs sans être vides)
- Photographie naturaliste non-stylisée (lumière naturelle)
- Grain analogique léger (pas dominant)
- Compositions centrées ou ancrées à gauche (pas multi-cols denses)

**Marqueurs anti-slop** :
- Palette PRÉCISE chaude (pas "earth tones" génériques)
- Serif EXPRESSIF (pas Times)
- Photographie LUMIÈRE NATURELLE (pas studio perfect)
- Espace ACTIF (pas vide subi)

**INTERDITS** :
- Inter / Roboto par défaut
- Flat cold white
- Indigo/purple gradient
- Stock photography "diverse lifestyle"
- Layout multi-cols denses (= Editorial Grid)

**Références culturelles** :
- Aesop · The Row · Le Labo · Apartamento · Kinfolk


### Naïve Design / Handmade Digital

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL (émergent fort) |
| Source catalogue | Partie 2 lettre A |
| Registre | Crafty |

**Description officielle** : Formes asymétriques, lignes tremblantes, typographie "crayonnée", couleurs vives sans dégradés, personnages illustrés à la main, textures papier/crayon/peinture. Intentionnellement imparfait mais parfaitement calculé dans son imperfection. DesignRush : "la tendance graphique qui redéfinit le branding en 2026". Différent de Craft-Core (Naïve = imperfection DIGITALE simulée, Craft = matériaux RÉELS).

**Signatures visuelles à incarner** :
- Lignes intentionnellement tremblantes (pas droites parfaites)
- Couleurs vives sans gradient (aplats saturés)
- Typographie "crayonnée" vraie (Karla Display, Nikkei, Bracket)
- Formes asymétriques irrégulières
- Textures papier/crayon/peinture (digitales mais authentiques)
- Personnages illustrés à la main

**Marqueurs anti-slop** :
- Imperfection CALCULÉE (pas chaos random)
- Typographie HAND-DRAWN vraie (pas filtre crayon Illustrator)
- Couleurs ASSUMÉES (pas pastels Memphis)
- Geste humain perceptible

**INTERDITS** :
- Memphis Design (formes pastel + zigzags)
- Filtre crayon générique sur typo Inter
- Stock illustrations "diverse hands"
- Border-radius rond systématique

**Références culturelles** :
- Acne Studios × Michael McGregor · Gail's Bakeries (Christopher Brown printmaking) · OpenAI ChatGPT 35mm


### 6. Vibrant & Block-based

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #6 |
| Registre | Brutaliste / Cinétique |

**Description officielle** : Couleurs primaires bloquées, typographie XXL, hiérarchie hard. Très présent dans les landing pages SaaS 2025, mais risque de saturation imminente. Fonctionne encore fort pour le branding B2C/culture.

**Signatures visuelles à incarner** :
- Couleurs primaires bloquées en aplats grands (#FF6B6B, #FFDC00, #4D96FF)
- Typographie XXL à dessein (clamp 8vw-14vw sur titres)
- Hiérarchie hard par contraste de taille
- Compositions block (rectangles colorés franches)
- Pas de dégradé chromatique (aplats purs)

**Marqueurs anti-slop** :
- Couleurs primaires NON-génériques (pas l'indigo classique Tailwind)
- Typographie XXL ASSUMÉE
- Aplats ENTIERS (pas accent timide)
- Hiérarchie BRUTE (sauts de taille marqués)

**INTERDITS** :
- Indigo / purple gradient (AI slop)
- Couleurs Tailwind par défaut sans réflexion
- Border-radius 16px+ (perd le côté block)
- Stock photography

**Références culturelles** :
- Gumroad · Mailchimp · Stripe Press · Notion (sections marketing)


### 5. 3D & Hyperrealism

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #5 |
| Registre | Cinétique / Tech |

**Description officielle** : Three.js catégorie Awwwards = winner quasi-hebdomadaire en 2025-2026. Spline démocratise la 3D accessible. Les sites B2B premium intègrent 3D scènes pour produits physiques. Coût élevé = signal de craft. Référence : Lacoste Members Experience (Merci-Michel), Boucheron Quatre 20th.

**Signatures visuelles à incarner** :
- Three.js / Spline / R3F (vraie 3D, pas illustration 3D)
- Shaders custom (pas presets génériques)
- Mobile performance testée (pas 3D "cheap")
- Lumière physique (pas studio AI)
- Interaction 3D (drag, hover, scroll)

**Marqueurs anti-slop** : 3D VRAIE (pas mockup PNG) · Shaders CUSTOM · Performance mobile vérifiée · Coût visible (signal craft).

**INTERDITS** : 3D "cheap" Spline preset · 3D sans interaction · Mobile cassé · Mockups produit dans cadre device.

**Références culturelles** : Lacoste Members Experience · Boucheron Quatre 20th · Apple AR · SpaceX.



### 15. Motion-Driven

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #15 |
| Registre | Cinétique |

**Description officielle** : School of Motion documente des sites avec "choreographed transitions" et "scroll-triggered animations" qui définissent les winners 2026. GSAP = tech dominante. Référence : SpaceX.com, Wodwo (Digital Silk).

**Signatures visuelles à incarner** :
- GSAP choreography (chaque animation raconte quelque chose)
- Scroll-triggered animations CONTRÔLÉES
- Easing physique nommés (cubic-bezier custom)
- Transitions multi-properties simultanées
- Pacing intentionnel (pauses + accélérations)

**Marqueurs anti-slop** : Animations CHORÉGRAPHIÉES (pas random CSS) · GSAP ou animation-timeline CSS native · Pacing INTENTIONNEL · Chaque animation a un sens.

**INTERDITS** : Animations infinies décoratives · Staggered fade-up générique · Translate Y au hover · Animation random sans intention.

**Références culturelles** : SpaceX · Wodwo · Awwwards Motion winners 2025-2026.



### 16. Micro-interactions

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL (transversal) |
| Source catalogue | Perplexity #16 |
| Registre | Cinétique (transversal) |

**Description officielle** : 30% du score Awwwards repose sur l'Usability dont les micro-interactions font partie. Hover states, cursor behaviors, transitions = critères de jugement explicites. Référence : Made With GSAP (Awwwards HM Mars 2026).

**Signatures visuelles à incarner** :
- Hover states intentionnels (pas translate Y générique)
- Cursor behaviors (magnetic hover, follower)
- Transition timing 200-400ms cohérent dans tout le système
- Easing nommés réutilisables (`--ease-out-expo`, `--ease-out-back`)
- Multi-property transitions (background + border simultané)

**Marqueurs anti-slop** : Cohérence du système (timing identique partout) · Transitions multi-property · Easing custom nommés · Aucun translate Y au hover.

**INTERDITS** : Translate Y au hover · `transition: all` · Easing par défaut `ease`/`ease-in-out` · Glow shadow au hover.

**Références culturelles** : Made With GSAP · Awwwards Honors 2025-2026 · Linear (transitions raffinées).


### 27. Storytelling-Driven

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #27 |
| Registre | Cinétique / Cinématographique |

**Description officielle** : Scroll storytelling + cinematic experiences = trend identifié dans plusieurs rapports 2025-2026. Parallax + audio = multi-sensoriel. Les narratives Awwwards winners 2025 sont quasi-systématiquement storytelling-first. Référence : The Goonies by Joseph Berry, Blue Desert (Adoratorio).

**Signatures visuelles à incarner** :
- Scroll narrative avec PACING intentionnel (pas transitions "scroll → opacity" basiques)
- Sections qui se RÉVÈLENT progressivement (animation-timeline view())
- Audio optionnel (sound design discret)
- Camera-like transitions entre sections
- Narrative structurée (arc dramatique perceptible)

**Marqueurs anti-slop** : Pacing INTENTIONNEL (variations rythme) · Narrative STRUCTURÉE (pas random reveals) · Transitions CINEMATIC · Multi-sensoriel discret.

**INTERDITS** : Scroll → opacity basique · Animations random au scroll · Manifestos poétiques omniprésents · Audio intrusif.

**Références culturelles** : The Goonies (Joseph Berry) · Blue Desert (Adoratorio) · SpaceX · Awwwards Storytelling winners.



### 46. Dimensional Layering

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #46 |
| Registre | Cinétique |

**Description officielle** : Profondeur sans 3D réelle : scroll parallax, z-index intentionnel, overlapping elements. Proche du Motion-Driven mais avec une logique spatiale spécifique. Fréquent dans les winners Awwwards 2025-2026.

**Signatures visuelles à incarner** :
- Z-index INTENTIONNEL (couches perceptibles)
- Overlapping elements qui créent la profondeur
- Mask-image pour fondus entre couches
- Scroll parallax SUBTIL (multi-vitesse maîtrisé)
- Pas de Three.js (profondeur CSS pure)

**Marqueurs anti-slop** : Profondeur SANS 3D · Z-index PERCEPTIBLE (pas accidentel) · Overlapping CONTRÔLÉ · Multi-speed parallax intentionnel.

**INTERDITS** : Parallax basique scroll → opacity · Z-index random · Overlapping qui casse l'accessibilité.

**Références culturelles** : Awwwards portfolios 2025 · Adoratorio Blue Desert.



### 48. Kinetic Typography

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #48 |
| Registre | Cinétique / Éditorial |

**Description officielle** : Typography animée = "lettres vivantes". Spotify Wrapped = cas d'école. Fontfabric documente les variable fonts kinétiques en 2025. Awwwards a une catégorie dédiée Typography Honors. Référence : Awwwards Typography Honors Sep 2025.

**Signatures visuelles à incarner** :
- Variable fonts animées (axes weight/slant/optical animés)
- Animation liée à l'INTERACTION (pas auto-play systématique)
- Typographie comme MATIÈRE (pas information)
- Transitions typographiques fluides (pas saccadées)
- 1 typographie display CHOISIE pour ses axes variables

**Marqueurs anti-slop** : Variable fonts si possible · Animation INTERACTIVE · Transitions FLUIDES · Typo CHOISIE pour ses axes.

**INTERDITS** : Auto-play tape-à-l'œil · Inter / Roboto par défaut · Animations infinies décoratives · Typo statique sans animation (= autre style).

**Références culturelles** : Spotify Wrapped · Awwwards Typography Honors · Pangram Pangram · Variable fonts museum.



### 49. Parallax Storytelling

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #49 |
| Registre | Cinétique / Cinématographique |

**Description officielle** : Parallax = catégorie Awwwards avec winners continus jusqu'en Oct 2025. SpaceX utilise full-bleed photography + scroll-triggered parallax. Technique mature mais toujours récompensée si bien exécutée. Référence : SpaceX, The Goonies, Lacoste.

**Signatures visuelles à incarner** :
- Multi-speed layers INTENTIONNELS (pas tous à la même vitesse)
- Testé MOBILE (pas seulement desktop)
- Scroll-triggered avec pacing
- Full-bleed photography ou visuels grand format
- Couches Z avec profondeur perceptible

**Marqueurs anti-slop** : Multi-speed CALIBRÉ · Mobile testé · Pacing intentionnel (pas continu uniforme) · Full-bleed visuels.

**INTERDITS** : Parallax uniforme tous éléments même vitesse · Cassé en mobile · Scroll-jacking lourd (bloque le scroll naturel).

**Références culturelles** : SpaceX · The Goonies (Joseph Berry) · Lacoste · Awwwards Parallax winners.



### 62. Interactive Cursor

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #62 |
| Registre | Cinétique |

**Description officielle** : Dynamic cursor = cité comme trend 2026 par WP Creative. Magnetic cursors, follower cursors = marqueur d'artisanat. Présent dans les portfolios Awwwards comme signal de craft.

**Signatures visuelles à incarner** :
- Cursor follower avec PHYSICS (spring) — pas linéaire
- Magnetic hover sur les éléments interactifs
- Cursor change de forme/taille selon contexte
- Pas désactivable (mais a fallback mobile)
- Non-gimmicky (sert l'expérience, pas décoratif)

**Marqueurs anti-slop** : Physics SPRING (pas linéaire saccadé) · Magnetic CONTRÔLÉ · Cursor change INTENTIONNELLE · Fallback mobile.

**INTERDITS** : Cursor follower lent saccadé · Cursor décoratif sans utilité · Mobile sans fallback.

**Références culturelles** : Awwwards portfolios 2025-2026 · Studio Mémoire · Arnaud Beelen.


### 64. 3D Product Preview

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Perplexity #64 |
| Registre | Tech / Cinétique |

**Description officielle** : AR/3D product pages = trend e-commerce fort 2025-2026. Android XR + Apple Vision Pro accélèrent l'adoption. Model element HTML maintenant supporté nativement sur Safari visionOS. Référence : Sites e-commerce premium.

**Signatures visuelles à incarner** :
- Spline pour assets simples
- Three.js / R3F pour interactions complexes
- Toujours fallback image (loading + browsers older)
- Drag/rotate intuitif
- Lumière physique réaliste

**Marqueurs anti-slop** : 3D VRAIE interactive · Fallback image présent · Performance mobile vérifiée · Lumière réaliste.

**INTERDITS** : 3D mockup PNG (pas vraie 3D) · Pas de fallback · Cassé en mobile · 3D décorative sans utilité produit.

**Références culturelles** : Sites e-commerce premium · Apple AR · Boucheron Quatre 20th.



### Adaptive Motion Identity / Living Brand Systems

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Partie 2 lettre C |
| Registre | Cinétique |

**Description officielle** : Logos et systèmes visuels fluides — logos "fondants", palettes de couleurs flexibles qui évoluent selon le contexte, motion design intégré à l'identité de marque. The Branding Journal identifie comme trend central 2026 : "Visual identities: from fixed systems to lived sensations".

**Signatures visuelles à incarner** :
- Logo system qui "vit" (SVG animé natif)
- Palette flexible par contexte (chaud/froid selon section)
- Motion design intégré à l'identité (pas overlay)
- Texture + mouvement + son intégrés à la marque
- Identité ADAPTATIVE selon platform/screen/contexte

**Marqueurs anti-slop** : SVG animé NATIF (pas Lottie générique) · Palette CONTEXTUELLE · Motion intégré à l'identité (pas décoratif).

**INTERDITS** : Logo statique animé en wrapper Lottie · Palette fixe rigide · Motion décoratif déconnecté de l'identité.

**Références culturelles** : Studio Dumbar · Interbrand 2026 work · The Branding Journal trends 2026.



### Immersive Scroll Narrative / Cinematic Scrolling

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Partie 2 lettre G |
| Registre | Cinétique / Cinématographique |

**Description officielle** : Sites où le scroll est une chorégraphie narrative complète — entrance animations, section reveals, pace variable, sound design optionnel, camera-like transitions entre sections. School of Motion documente les sites épics 2026. Distinct du simple parallax : ici, le scroll définit une narrative structurée.

**Signatures visuelles à incarner** :
- GSAP ScrollTrigger choreography
- Narrative STRUCTURÉE (pas animations random au scroll)
- Pace VARIABLE (alternance lent/rapide)
- Camera-like transitions (zooms, pans)
- Sound design optionnel discret

**Marqueurs anti-slop** : Narrative STRUCTURÉE · Pace VARIABLE · GSAP ScrollTrigger · Camera-like.

**INTERDITS** : Animations random au scroll · Pace uniforme · Sound intrusif · Scroll-jacking violent.

**Références culturelles** : Blue Desert (Adoratorio, Three.js + GSAP) · SpaceX · School of Motion sites 2026.




### 57. Gen Z Chaos / Maximalism

| Champ | Valeur |
|---|---|
| Verdict | CYCLIQUE (pic 2024-2025) |
| Source catalogue | Perplexity #57 |
| Registre | Crafty / Cinétique |

**Description officielle** : Layouts fluides, anti-grille, maximalisme expressif. Très fort pour creator economy et Gen Z. Risque de saturation si mal exécuté.

**Signatures visuelles à incarner** :
- Layouts intentionnellement anti-grille
- Typographies clashantes CHOISIES (pas générées aléatoirement)
- Couleurs saturées multi-accents
- Compositions denses chargées
- Stickers, GIFs, glitch ponctuels
- Voix maximaliste (pas minimaliste premium)

**Marqueurs anti-slop** : Chaos CALCULÉ (pas random) · Typographies clashantes CHOISIES · Détails Gen Z authentiques · Voix vraie.

**INTERDITS** : Chaos aléatoire généré · Stock photography · Voice corporate · Manifestos polis.

**Références culturelles** : MSCHF · Bottega Veneta web · Glossier (premières années) · sites musique indie.



### 59. Anti-Polish / Raw Aesthetic

| Champ | Valeur |
|---|---|
| Verdict | CYCLIQUE (montant fort) |
| Source catalogue | Perplexity #59 |
| Registre | Crafty / Brutaliste |

**Description officielle** : "Anti-AI Crafting" = "tendance qui définira 2026" selon Landor/Graham Sykes. Imperfection intentionnelle, surfaces texturées, marques du geste humain. Très fort momentum.

**Signatures visuelles à incarner** :
- Textures genuinement artisanales (pas filtres AI)
- Typographies "vraies à la main" (pas filtres crayon)
- Imperfections ASSUMÉES (lignes pas droites, espacements irréguliers)
- Photographie analogique brute
- Compositions désordonnées maîtrisées
- Anti-finition (signal d'authenticité)

**Marqueurs anti-slop** : Textures VRAIES · Typographies VRAIES hand-drawn · Imperfections AUTHENTIQUES · Photographie analogique brute.

**INTERDITS** : Filtres "raw" prêts-à-l'emploi · Stock photography vintage · Inter avec filtre crayon · Manifesto poétique sur "authenticité".

**Références culturelles** : Burberry Cross-Stitch · Madalena Studio · OpenAI campagne 2025 anti-AI · brands indépendants Berlin.



### Expressive Organic / Anti-Grid Flow

| Champ | Valeur |
|---|---|
| Verdict | ACTUEL |
| Source catalogue | Partie 2 lettre F |
| Registre | Organique / Cinétique |

**Description officielle** : Layouts fluides sans grille rigide — formes organiques qui coulent, éléments qui s'enroulent autour du contenu, scroll qui "respire", transitions en morphing. Opposé du bento grid structuré. YouTube "Top 2026 Web Design Trends" : "organic web layouts and the anti-grid design trend are replacing rigid structures".

**Signatures visuelles à incarner** :
- Layout sans grille rigide (formes organiques dictent l'espace)
- Morphing shapes (animations de formes qui se transforment)
- Palette biomorphique
- Texte qui s'enroule autour des formes (text-wrap shape)
- Scroll qui "respire" (pas saccadé)
- Pas de hairlines droites (anti-rigide)

**Marqueurs anti-slop** : Formes ORGANIQUES vraies · Morphing INTENTIONNEL · Palette biomorphique · Text-wrap autour des formes.

**INTERDITS** : Bento grid · Grille rigide visible · Blobs centrés statiques · Couleurs Tailwind par défaut.

**Références culturelles** : Sites culture, arts, food artisanal · DevInterface 2026 trends.



---

# Partie B — Styles à ÉVITER (DATÉS + CYCLIQUES en déclin)

> **Le styliste NE LES CHOISIT JAMAIS**. Ils sont listés ici pour être ÉLIMINÉS du scan dès l'étape 1 du protocole de matching.

### 2. Neumorphism (pur)

**Verdict** : DATÉ.
**Source catalogue** : Perplexity #2.
**Pourquoi éviter** : "Pure neumorphism 2020 — strict, low-contrast, monochromatic — is unequivocally a dated trend". Problèmes d'accessibilité (WCAG AAA impossible), visuellement "boring" selon le créateur lui-même Michał Malewicz. Survit uniquement dans une version hybride (Soft UI Evolution #19, voir Partie A).
**Alternative singulière** : Soft UI Evolution (#19, Partie A) si secteur wellness/santé non-critique.

### 13. Skeuomorphism (classique)

**Verdict** : DATÉ / Revival niche.
**Source catalogue** : Perplexity #13.
**Pourquoi éviter** : Le skeuomorphism "traditionnel" (boutons réalistes, cuir, ombres épaisses) reste associé à iOS 6 pre-Jony Ive. Un "Light Skeuomorphism" raffiné revient timidement en 2025-2026 mais sans présence dans les sites primés. Réservé aux niches (apps musicales, retro gaming).
**Alternative singulière** : Liquid Glass (#14, Partie A) pour la profondeur premium.

### 18. Zero Interface

**Verdict** : DATÉ.
**Source catalogue** : Perplexity #18.
**Pourquoi éviter** : Concept "invisible UI" de 2017-2020 porté par des apps vocal-first. La réalité de 2025 : les interfaces hybrides ont remplacé ce concept théorique.
**Alternative singulière** : aucune nécessaire — concept obsolète.

### 9. Claymorphism

**Verdict** : CYCLIQUE (déclin).
**Source catalogue** : Perplexity #9.
**Pourquoi éviter** : Populaire 2021-2023, maintenant associé au "Corporate Memphis 3D". LogRocket note qu'il "n'est pas à la pointe" en 2024. Encore utilisé pour les app icons (iMessage, Facebook Messenger) mais pas pour les sites primés.
**Alternative singulière** : Soft UI Evolution (#19, Partie A) si besoin tactile, ou 3D & Hyperrealism (#5, Partie A) si vraie 3D.

### 11. Retro-Futurism

**Verdict** : CYCLIQUE (pic 2024-2025).
**Source catalogue** : Perplexity #11.
**Pourquoi éviter** : Neon grids, chrome, glitch retro = peak en 2024-2025. Vaporwave revival 2025 lui est lié. Risque de déclin si trop généralisé.
**Alternative singulière** : Chromatic Aberration (#67, Partie A) si signal "tech imprévisible" voulu.

### 40. Y2K Aesthetic

**Verdict** : CYCLIQUE (déclin).
**Source catalogue** : Perplexity #40.
**Pourquoi éviter** : Peak en 2023-2024. Awwwards l'a récompensé (fa-So-La Akihabara, Sept 2023). La tendance Vaporwave 2025 le prolonge mais le Y2K "pur" commence à saturer.
**Alternative singulière** : Vibrant Block-based (#6, Partie A) si signal "digital expressif" voulu.

### 41. Cyberpunk UI

**Verdict** : CYCLIQUE (déclin hors gaming).
**Source catalogue** : Perplexity #41.
**Pourquoi éviter** : Fort en 2020-2022 (Cyberpunk 2077 effect). Encore présent en gaming/crypto. Absent des sites non-entertainment primés en 2025-2026.
**Alternative singulière** : Dark Mode Cinema (#7, Partie A) + Chromatic Aberration (#67, Partie A) si tech premium.

### 44. Memphis Design

**Verdict** : CYCLIQUE (déclin).
**Source catalogue** : Perplexity #44.
**Pourquoi éviter** : Revival 2022-2024 documenté. En 2026, le mouvement Naïve Design absorbe une partie de son énergie. Risque de saturation rapide.
**Alternative singulière** : Naïve Design (Partie A) — le successeur naturel.

### 45. Vaporwave

**Verdict** : CYCLIQUE (pic 2025).
**Source catalogue** : Perplexity #45.
**Pourquoi éviter** : "Retour en force en 2025" selon Alibaba — fatigue digitale + nostalgie 2000s. Attention : trop niche pour un usage transversal. Saturation imminente.
**Alternative singulière** : Vintage Analog (#68, Partie A) pour signal nostalgique authentique.

### Pixel Art (mainstream)

**Verdict** : DATÉ (mainstream) / ACTUEL (niche gaming).
**Source catalogue** : Perplexity #52.
**Pourquoi éviter** : En tant qu'esthétique transversale de site : daté. En tant que choix intentionnel pour gaming/culture/indie brands : actuel. Sur le web grand public : signal de niche, pas de professionnalisme.
**Alternative singulière** : Vintage Analog (#68, Partie A) pour signal nostalgique premium.

---

# Partie C — Marqueurs AI slop transverses

> Ces patterns peuvent contaminer N'IMPORTE QUEL style légitime. Le styliste DOIT les éviter dans ses prescriptions, et chaque fiche de Partie A référence ces marqueurs dans son champ "INTERDITS".

## C.1 — Couleurs & Gradients

- **Purple/indigo accent** : `#6366f1`, `bg-indigo-500`, palette Tailwind par défaut sans réflexion. Documenté comme AI slop signature (Adam Wathan, août 2025).
- **Gradient violet → bleu sur fond blanc/gris clair** : signature des AI-generated SaaS landings.
- **Aurora gradient générique** : 3 blobs animés centrés, toujours violet+rose+bleu — le marqueur AI slop le plus visible.
- **Palettes "timides" équilibrées** : 3 couleurs pastel + gris. Manque de tension chromatique.

## C.2 — Typographie

- **Inter en corps de texte ET en headline** (mono-font Inter) : signal AI direct. Inter en body OK, mais avec un display CHOISI.
- **Roboto / Arial fallback systématique** : signal de "design par défaut", pas de choix typographique.
- **Space Grotesk dès qu'on veut "faire moderne"** : sur-utilisé en 2025. Si Space Grotesk choisi, justifier précisément.
- **Hiérarchie limitée à "titre gros = header"** : pas de variations de poids/style/échelle. Hiérarchie pauvre.

## C.3 — Layout & Composants

- **Hero centré "grand titre + sous-titre + bouton CTA seul"** : pattern Bootstrap générique. Aucune signature de marque.
- **Trois features en boxes (icône + titre + texte) systématiquement horizontales** : artefact CTA pages 2018-2020.
- **Cards avec `border-radius: 8-12px` + ombre `0.1 opacity` sur fond blanc** : combo générique AI default.
- **Section "How it works" en 3 steps numérotés avec icônes** : structure SaaS template.
- **Footer avec 4 colonnes égales de liens** : sitemap déguisé sans personnalité.

## C.4 — Effets visuels

- **Glassmorphism avec backdrop-blur 20px+ générique + fond violet** : combo AI slop documenté.
- **Subtle shadows "exactement 0.1 opacity"** : signature CSS par défaut.
- **Dark mode = fond `#0a0a0a` + texte `#ffffff` + accent indigo** : combo AI slop dark.

## C.5 — Marqueurs comportementaux

- **Translate Y au hover** : pattern le plus générique du web.
- **`transform: scale()` > 1.02 au hover** : effet "jouet".
- **Icône/arrow qui slide au hover** : cliché SaaS 2017.
- **Soulignement qui grandit au hover** : cliché navbar 2018.
- **Letter-spacing qui augmente au hover** : cliché footer premium 2017.
- **Pulsing/breathing animations infinies décoratives** : indicateur daté.
- **Glow shadows `box-shadow: 0 0 Npx`** sans offset : les ombres ont un offset directionnel.
- **Wave/zigzag dividers entre sections** : marqueur de template WordPress.
- **Staggered fade-up `@keyframes` manuels** : signature des landing pages 2017.

## C.6 — Source de vérité

Cette liste est issue de :
- Adam Wathan (Tailwind) — "AI Purple apology + AI slop documentation" (août 2025)
- Jack Pearce — "Purple gradient origins analysis" (février 2026)
- Kristian Valtersen / Dawn Studio — "AI slop fix video" (Dec 2025)
- Rapport Perplexity 2026 Partie 3 (`ref/perplexity-styles-datés-vs-actuels-2026.md` lignes 205-247)
- Blacklist Phase 4 BIG (`phases/phase-4-styletile.md`)

À mettre à jour à chaque nouveau rapport Perplexity ou détection empirique.

