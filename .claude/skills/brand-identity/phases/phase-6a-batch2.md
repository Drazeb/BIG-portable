PROMPT SUBAGENT PHASE 6A (BATCH 2 — FICHIER SÉPARÉ):

Tu génères le Batch 2 (Système de Signes) pour la marque {brand}.
Ce fichier est SÉPARÉ du Batch 1 (triptyque) mais VISUELLEMENT COHÉRENT grâce aux specs partagées.

## SPECS ARRÊTÉES (À RESPECTER EXACTEMENT)

### CSS Custom Properties (extraites du Batch 1)
{extracted_css_variables}

### Polices Google Fonts
{extracted_fonts}

## CONTEXTE
Lis ces fichiers de référence :
- {skill_dir}/ref/persona-and-rules.md
- {skill_dir}/ref/bible-design-strategie.md
- {skill_dir}/ref/master-style-guide.md (sections 05, 06, 07)
- {skill_dir}/examples/{example_level}/batch2-example.html (standard de qualité pour le Batch 2)
- {skill_dir}/ref/icon-system/catalogue/{icon_family_id}.md (fiche catalogue de la famille d'icônes assignée par Phase 6A-0)
- {skill_dir}/ref/icon-system/slop-sheets/{icon_family_id}.md (fiche slop/anti-slop spécifique à la famille — à respecter strictement pour le chapitre 06)

Et le style-tile source (pour comprendre l'univers visuel) :
- {style_tile_read_path}

### Cohérence dataviz — Référence artefact
Le style-tile contient un artefact témoin (section `.artifact-witness`) avec des composants de données : chart cards, KPI display, sparklines, grilles de données. Ton **chapitre 07 (Data Visualization)** DOIT partager le même design language que cet artefact :
- Mêmes radius et shadows sur les chart cards
- Même traitement typographique des KPI (font-display, tnum, même gamme de tailles)
- Mêmes courbes de hover (easing, scale, propriétés)
- Même logique de séparation (fond, pas bordures)
Tu ne copies pas le layout de l'artefact — tu t'alignes sur son **vocabulaire visuel** pour les composants de données.

## CONCEPT CHOISI (extrait du pitch)
{pitch_extract}

## CALIBRAGE CSS PAR CURSEUR A — {cursor_a_label}

Le style-tile source a été généré avec le curseur A = {cursor_a}. Le Batch DOIT maintenir le MÊME niveau d'ambition CSS.

**Socle de finition (TOUJOURS, quel que soit A)** :

{finition_elite_tier1}

## PRINCIPES DE HIÉRARCHIE VISUELLE — Niveau élite

{hierarchie_visuelle_tier1}

### A = 1 (Prudent) — Le traitement est RECONNAISSABLE
- Layout : grilles régulières, symétrie, alignements standards
- Surfaces : fonds unis ou gradients basiques, radius constants
- Interactions : changement de fond, opacité — avec easing physiques et multi-property

### A = 2 (Décalé) — Le traitement a UN SIGNAL DISTINCTIF
- Layout : au moins une asymétrie ou irrégularité contrôlée (ratio 60/40, grille non-standard)
- Surfaces : au moins une surface expressive (texture, overlay, ombre colorée)
- Interactions : le hover EXPRIME le concept (pas juste un changement de fond)
- Techniques CSS : au moins une technique non-standard (@property animé, color-mix avancé, clip-path, animation-timeline)

### A = 3 (Rupture) — Le traitement INVENTE SA PROPRE RÈGLE
- Layout : au moins une convention cassée (chevauchement, grille brisée, négatif margins)
- Surfaces : surfaces composites (blend modes, masques, formes non-rectangulaires)
- Interactions : interactions physiques ou narratives
- Techniques CSS : au moins une technique de pointe (@starting-style, scroll-driven, subgrid, clip-path compositionnel)

## ⚠ A11Y ET FONDAMENTAUX (non-négociable, quel que soit le concept)

{a11y_fondamentaux_tier1}

## ⛔ ANTI-PATTERNS DATÉS — BLACKLIST (quel que soit le curseur A)

{anti_slop_blacklist_tier1}

## CATALOGUE CSS MODERNE (extrait de html-showroom-spec.md, section 6)
{css_moderne_catalogue}

## ⚠ DIRECTIVE ANTI-CONTAMINATION — LIRE ATTENTIVEMENT

L'exemple Batch 2 montre le NIVEAU DE FINITION à atteindre :
- Qualité du code CSS (custom properties, animations, transitions)
- Structure des sections (05→07) et complétude des sous-sections
- Richesse visuelle des démonstrations (icons, data-viz, lockups)
- Respect des gates (Screenshot Test, Cursor Coherence, CSS Moderne)

Il ne montre PAS la direction créative à suivre.
Tes choix de style iconique, de traitement logotype, de style data-viz doivent découler
du CONCEPT du style-tile source, PAS de l'exemple.

La SEULE chose à copier de l'exemple est le NIVEAU DE QUALITÉ et la COMPLÉTUDE, pas les choix formels.

Concrètement :
- Si l'exemple utilise un logo radial/organique → ton concept peut demander un wordmark géométrique, un monogramme, ou un symbole abstrait
- Si l'exemple montre des icônes duotone → ton concept peut utiliser des icônes outline, solid, ou hand-drawn
- Si l'exemple fait de la data-viz avec 4 couleurs → tu peux en utiliser 2 ou 6 selon la palette

{ventre_mou_section}

{logo_block}

## MISSION
Génère un fichier HTML AUTONOME contenant les 4 chapitres du Batch 2, ouvert par un en-tête éditorial SOBRE (pas de cover band image — supprimée le 2026-05-14, cf. amendement D54). Format strictement aligné sur l'ouverture du Batch 3 : skip-link → `<main>` → kicker de volume discret → chapitre 05.

### ENTRÉE ÉDITORIALE (obligatoire, sobre)

Le `<body>` s'ouvre **exactement** dans cet ordre :

1. `<a href="#main" class="skip-link">Aller au contenu</a>` (a11y).
2. `<main id="main">` (le `id="main"` vit sur `<main>`, **pas** sur la première section — cohérent avec Batch 3).
3. **Kicker de volume** discret, type overline éditorial, avant le chapitre 05. Format suggéré :
   ```html
   <div class="batch2-volume-marker" aria-hidden="true">
     <span class="batch2-volume-marker__line"></span>
     Volume II · Système de Signes
   </div>
   ```
   CSS minimaliste — réutilise les tokens `:root` partagés (pas de nouvelles variables) :
   - `font-family: var(--font-body)`, `font-size: var(--fs-overline)` (ou un `--text-xs`/`clamp` équivalent), `font-weight: 500`, `letter-spacing: 0.28em`/`0.32em`, `text-transform: uppercase`.
   - `color: var(--color-accent)` (ou l'équivalent kicker du style-tile retenu).
   - `padding: clamp(var(--space-lg), 6vh, var(--space-2xl)) clamp(var(--space-lg), 5vw, var(--space-2xl))`.
   - Une fine ligne 1px à gauche (`__line`) en `background: currentColor` ou `var(--color-accent)`, largeur ~`clamp(32px, 5vw, 64px)`, hauteur `1px`.
   - Pas de fond image, pas de gradient, pas d'overlay — c'est un kicker éditorial sobre.
4. Directement enchaîner sur le chapitre 05 (cf. ci-dessous). **Aucune** `<section class="batch2-cover">`, **aucune** image en `background-image` ouvrante, **aucun** wordmark géant en hero.

**Pourquoi** : la cover band image (D54 du 12 mai) a été retirée le 2026-05-14 — un header habillé à l'image en ouverture n'apporte rien d'éditorial sur cette planche de documentation et entre en conflit avec le hero du style-tile/Batch 1. La mention du volume dans le `<title>` + le kicker sobre + le footer existant suffisent. Les chapitres du Batch 2 (05/06/04/07) s'ouvrent normalement à la suite.

### CHAPITRE 05 — LOGOTYPE & MORPHOLOGIE DU SIGNE
{logo_chapter_instructions}

### CHAPITRE 06 — ICONOGRAPHIE (REFONTE 2026-05-27, D59)

**Famille d'icônes assignée par Phase 6A-0 : `{icon_family_id}` — {icon_family_label}**

Tu DOIS produire un VRAI SET D'ICÔNES UI UTILISABLES dans le style de la famille assignée, **PAS des illustrations narratives**. Distinction critique :

| Ce que tu NE DOIS PAS faire | Ce que tu DOIS faire |
|---|---|
| Dessiner des illustrations narratives liées au concept (un phare, un sextant, une scène d'auscultation) | Dessiner des icônes UI fonctionnelles (search, settings, user, save, calendar) dans le STYLE de la famille assignée |
| Représenter le SUJET du concept narratif | Faire VIVRE le concept dans la FORME, l'épaisseur, la matière, la palette des icônes utiles |
| Une icône = une scène complète avec atmosphère | Une icône = un pictogramme lisible à 24×24 |

**Le concept narratif donne le TON (palette, matière, épaisseur), pas le SUJET.** Une icône `search` doit RESPIRER l'univers de la marque via sa forme, pas être un dessin du concept narratif.

**Fiche catalogue + fiche slop/anti-slop de la famille assignée** (déjà chargées en contexte via `{skill_dir}/ref/icon-system/`) — tu DOIS les respecter strictement :
- Catalogue : `ref/icon-system/catalogue/{icon_family_id}.md` (traits formels, traitements natifs, couleurs natives)
- Slop sheet : `ref/icon-system/slop-sheets/{icon_family_id}.md` (8 anti-patterns à BANNIR + 5 signatures pro 2024-2026 à incarner + 2 checks mécaniques)

**Justification du choix de famille** (transmise par le router) :
{router_justification}

#### 06.1 — Le set d'icônes (la VRAIE livraison)

**18-22 icônes** présentées en grille dense (4-6 colonnes), labels courts en dessous, **dans LE traitement principal natif de la famille** (= état normal).

**Composition du set** (cible 18-22) :
- **10-12 UI primaire** (les indispensables, universels) :
  `search`, `menu`, `close`, `back`, `home`, `settings`, `user`, `notification`, `calendar`, `mail`, `edit`, `trash`, `save`, `share`, `filter`, `add` — pioche 10-12 dans cette liste
- **4-6 UI métier spécifiques à la marque** : dérivés du brief et du concept (ex pour une agence de positionnement startup : `pitch-deck`, `brief`, `workshop`, `roadmap`, `client`, `review`. Ex pour une boîte de recharge VE : `station`, `vehicle`, `charge`, `battery`, `grid`)
- **4 statuts sémantiques** : `success`, `warning`, `error`, `info`

**Règles d'exécution** :
- Toutes les icônes appartiennent à la **MÊME famille graphique** assignée
- Toutes incarnent au moins 3 des 5 `[SIG-N°]` de la slop sheet (techniques natives de la famille)
- Aucun des 8 `[ANTI-N°]` de la slop sheet n'est présent
- Composition simple, lisible, pas de scène
- **Labels** : 1-2 mots fonctionnels EN MINUSCULES (`search`, `settings`, `user-add`), pas des phrases poétiques

**Règle d'incarnation visuelle (CRITIQUE — point dur observé sur Camille 0527)** :
- **≥50% des icônes du set (soit ≥10 sur 20) DOIVENT INCARNER VISIBLEMENT au moins 2 des 5 `[SIG-N°]` de TA fiche slop — pas seulement les déclarer en commentaire CSS ou dans une légende texte.** Si la fiche slop dit "hachures rotation variable (SIG-01)" pour la gravure, on doit VOIR les hachures sur l'icône rendue — pas juste lire "<!-- hachures appliquées -->" dans le SVG. Si la fiche dit "superposition de plans aplats (SIG-02)" pour le flat illustré, on doit VOIR au moins 3 plans empilés — pas un seul aplat avec annotation. Etc. pour les 8 familles.
- **Vérification par le check `[CHK-N°]` de la slop sheet (au niveau du gate post-batch)** : chaque famille a un check d'incarnation famille-spécifique qui compte le nombre d'icônes du set qui utilisent VRAIMENT la technique signature. Si <50% → FAIL, re-dispatch designer avec consigne corrective ciblée.

**Règle d'affichage du set principal (CRITIQUE pour la visibilité de la signature)** :
- **Afficher les icônes à 64×64 minimum dans la grille 06.1**, pas 24×24. Le designer rend les SVG en `width: 64px; height: 64px;` (ou `clamp(48px, 5vw, 80px)` pour responsive). Une note en bas du set indique : *"Affichage à 64×64 ci-dessus pour rendre visible la signature `{icon_family_label}`. Rendu cible UI : 24-32px (les hachures / plans / textures restent calibrés pour rester lisibles à toutes les tailles)."*
- **Pourquoi** : à 24×24, les signatures matérielles (hachures gravure, plans superposés flat illustré, grain noise, etc.) s'évaporent. Le designer sous-produit la matière par crainte de l'illisibilité. Afficher plus grand DÉBLOQUE l'incarnation visuelle, ET force le designer à oser la signature.
- Le set 06.2 traitements alternatifs et 06.3 mockup usage en contexte gardent les tailles UI réalistes (24-32px) — c'est dans 06.1 SEULEMENT que le set principal est exposé en 64×64.

#### 06.2 — Traitements alternatifs (1-2 traitements pour cas d'usage business)

Présenter **1 ou 2 traitements alternatifs** au traitement principal de 06.1, MONTRÉS sur 4-6 icônes types prises du set principal.

**Chaque traitement alternatif DOIT être étiqueté avec son CAS D'USAGE BUSINESS EXPLICITE**, pas juste un nom technique. Exemple :

| Traitement | Cas d'usage business | Quand l'utiliser concrètement |
|---|---|---|
| **Principal** (montré en 06.1) | État normal | Sidebar inactive, toolbar standard, listes |
| **État actif/sélectionné** | Highlight | Onglet en cours, favori coché, item sélectionné |
| **Variante dense/mini** (optionnel) | UI dense | Tableaux serrés, breadcrumb, micro-icônes 16px |

Pour les traitements natifs de TA famille assignée, lis la fiche catalogue (`ref/icon-system/catalogue/{icon_family_id}.md`) section "Formats natifs en stack Claude Code" et "Couleurs natives". Adapte les noms des traitements à la famille (PAS "Outline / Solid / Duotone" par défaut — c'est l'ancienne logique qu'on remplace).

**Règle** : **2 traitements max** (1 principal + 1 alternatif), 3 si la famille en a vraiment 3 natifs distincts. PAS plus.

#### 06.3 — Usage en contexte (1 mini-mockup, pas 5)

**Une SEULE composition** qui montre 4-6 icônes du set EN CONDITION RÉELLE d'usage.

**Squelette imposé — pioche UN type parmi cette liste, pas d'autre** :
- Sidebar verticale (logo + 5-7 items navigation + footer user)
- Mini-table avec toolbar (4 colonnes, 5 lignes, toolbar avec icônes search/filter/add)
- Toolbar horizontale isolée (8-10 icônes groupées par fonction)
- Breadcrumb + status indicators inline
- List items verticaux (5-7 items avec icône + label + status)
- Navigation principale (tabs ou segmented control)

**Interdit (déjà couvert chapitre 04)** : pas de card produit complexe, pas de form avec inputs/toggles/checkboxes, pas de bouton primary/secondary isolé, pas d'alert/notification.
**Autorisé** : avatar simple en initiales si pertinent, badge statut inline (usage contextuel d'une icône statut du set, pas une démo isolée).

**Règles** :
- Doit utiliser le STYLE de la marque (palette, typo, espacements depuis `:root`)
- Doit montrer le CONTRASTE entre traitement principal (icônes inactives) et traitement actif (icône en cours)
- Pas de Lorem ipsum — labels métier crédibles dérivés du brief
- Taille raisonnable, pas de hero monumentale

### CHAPITRE 04 — CODE CIVIL ATOMIQUE : COMPOSANTS UI

Ce chapitre documente visuellement TOUS les composants UI du design system, **isolés et avec leurs variantes d'état**.

**Source de vérité prioritaire** : la section `.artifact-witness` du style-tile source contient l'inventaire de composants posés en Phase 4. Cet inventaire est **variable selon la grammaire choisie par le designer** (les 5 catégories fonctionnelles avec quotas minimum produisent un nombre et un format d'atomes qui dépendent de l'archétype retenu — pas une liste fixe). Lis l'artefact source pour identifier les composants présents et **extraire leurs specs exactes** (padding, radius, couleur, transition) — ce sont les références canoniques.

**Composants à générer (absents de l'artefact source)** : tu génères dans ce chapitre les composants attendus par la checklist obligatoire ci-dessous mais qui n'apparaissent pas dans l'artefact source. Tu les **génères en respectant strictement le design language du `:root` partagé** (mêmes radius, shadows, easing, family de couleurs que les composants extraits) ET la grammaire posée par l'artefact source (signatures structurelles repérables dans la composition Phase 4). C'est ce chapitre qui pose ces atomes pour la suite du process (LPG, design system).

**Règle chromatique pour les sévérités feedback** : pour signifier success / warning / error / info, tu RÉUTILISES en priorité la palette de base validée du :root (par variation de valeur, opacité, ou fond teinté de l'accent existant). Tu peux introduire AU PLUS 1 token sémantique supplémentaire (`--color-feedback-*`) si la palette de base ne suffit absolument pas à signifier les sévérités. **Pas de nouvelles familles chromatiques inventées** (pas de teintes hors gamme du :root).

Chaque composant est documenté ISOLÉMENT — pas de remix layout, juste le composant + ses variantes + ses specs visuelles.

Affiche chaque composant isolé avec ses variantes et specs visibles :
- 04.1 **Buttons** : Primary (fond plein + hover) et Secondary (outline/ghost + hover) côte à côte, avec états default/hover/active/disabled. Specs visibles : padding, radius, font-size, transition.
- 04.2 **Form Elements** : Input (avec placeholder + focus state), Toggle (on/off), Checkbox (checked/unchecked), Select (avec chevron). Chacun dans son état default + actif.
- 04.3 **Badges & Statuts** : Les 4 variantes sémantiques (success/warning/error/info) alignées, avec fond teinté + texte. Montrer aussi 2-3 tailles si pertinent.
- 04.4 **Cards & Containment** : Montrer 2-3 cards avec radius, shadow multi-layer, fond distinct. Hover state visible. Montrer aussi la logique de séparation (fond vs bordure).
- 04.5 **Feedback & Navigation** : Alert/notification (au moins 1 variante), Progress indicator (bar ou ring), Tab bar ou segmented control (active/inactive), Avatar (initiales).

### CHAPITRE 07 — DATA VISUALIZATION & EVIDENCE
Affiche visuellement :
- 07.1 **Style des Graphiques** : exemples de line charts, bar charts, donuts
- 07.2 **Système de Grilles & Axes** : démonstration des gridlines et baseline
- 07.3 **Usage de la Couleur** : palette data-viz appliquée sur graphiques
- 07.4 **Typographie de la Donnée** : labels, légendes, KPI en style mono

## CHECKLIST OBLIGATOIRE — VÉRIFIER AVANT DE FINALISER
Tu DOIS inclure TOUTES ces sections dans le fichier. Coche mentalement chaque item :
{logo_chapter_checklist}
[ ] 06.1 Iconographie — Le set d'icônes UI (famille `{icon_family_id}`, 18-22 icônes : 10-12 UI primaire + 4-6 UI métier + 4 statuts sémantiques)
[ ] 06.2 Iconographie — Traitements alternatifs (1-2 max, chacun étiqueté avec son cas d'usage business explicite, MONTRÉS sur 4-6 icônes types du set)
[ ] 06.3 Iconographie — Usage en contexte (1 mini-mockup, squelette imposé : sidebar / table+toolbar / toolbar / breadcrumb / list / nav — pas de composants chapitre 04)
[ ] 04.1 UI Components — Buttons (Primary + Secondary, 4 états)
[ ] 04.2 UI Components — Form Elements (Input, Toggle, Checkbox, Select)
[ ] 04.3 UI Components — Badges & Statuts (4 variantes sémantiques)
[ ] 04.4 UI Components — Cards & Containment (radius, shadow, hover)
[ ] 04.5 UI Components — Feedback & Navigation (Alert, Progress, Tabs, Avatar)
[ ] 07.1 Data Viz — Style des Graphiques
[ ] 07.2 Data Viz — Système de Grilles & Axes
[ ] 07.3 Data Viz — Usage de la Couleur
[ ] 07.4 Data Viz — Typographie de la Donnée

SI UNE SEULE SECTION MANQUE → AJOUTE-LA AVANT DE FINALISER.

## RÈGLE CRITIQUE — COHÉRENCE ABSOLUE
Le bloc `:root { ... }` du fichier généré DOIT être IDENTIQUE aux specs fournies.
- Mêmes codes HEX
- Mêmes noms de fonts
- Mêmes valeurs de radius, shadows, spacing
- Aucune variation créative sur les specs atomiques

## CONTRAINTES TECHNIQUES
- HTML self-contained (CSS dans `<style>`). Plus de référence externe à `visual-final/` côté Batch 2 depuis le retrait de la cover band (2026-05-14) — le batch redevient strictement self-contained.
- Google Fonts via <link> (avec preconnect)
- Le résultat doit être visuellement riche — privilégie qualité et variété des techniques CSS sur la quantité de code
- **CSS Moderne** : socle de finition obligatoire (oklch, @layer, @property, color-mix, text-wrap, clamp) + **≥2 techniques avancées** parmi : `@property` animé, `clip-path`, `mask-image`, `@starting-style`, `backdrop-filter`, `mix-blend-mode`, `:has()`, `animation-timeline: view()`, `@container`. Chaque technique doit SERVIR le design
- **Techniques concept-driven** : le CONCEPT CHOISI (extrait du pitch) peut spécifier des techniques CSS prioritaires — si présentes, les intégrer EN PRIORITÉ
- **Vocabulaire d'interaction** : si le CONCEPT CHOISI spécifie une philosophie d'interaction, l'APPLIQUER à tous les éléments interactifs (cards, icônes, graphiques)
- Respecte les GATES

## PROGRESS LOG
Écris une ligne dans le fichier `{skill_dir}/outputs/{session_dir}/.progress-batch2.log` à chaque étape clé (écris le fichier complet à chaque fois avec les lignes précédentes + la nouvelle) :
- Après lecture des fichiers de référence : `REFS_LOADED | {n} fichiers lus`
- Avant de commencer à écrire le HTML : `GEN_START | {n} sections à générer`
- Après chaque chapitre terminé : `CHAPTER_DONE | {numéro} {nom}`
- En fin de génération : `COMPLETE | {filename} | {n} lignes`
- En cas d'erreur ou blocage : `ERROR | {description}`

Ce log est lu par l'orchestrateur pour détecter les blocages. Il doit rester SOBRE (1 ligne par étape).

## GATES DE VALIDATION
1. **Specs Lock** : Les CSS Custom Properties sont-elles IDENTIQUES aux specs fournies ?
2. **Completeness** : Les 11 sous-sections (05.1→05.4 + 06.1→06.3 + 04.1→04.5 + 07.1→07.4) sont-elles TOUTES présentes ? (Le chapitre 06 a été refondu D59 — 3 sections au lieu de 4 : set / traitements alternatifs / usage en contexte.)
3. **Screenshot Test** : Zéro donnée technique brute visible dans le rendu (pas de HEX, pas de noms de fonts en clair dans le texte courant) — les labels de section (05.1, 06.2) sont LÉGITIMES ici (c'est de la documentation).
4. **Brief Alignment** : Le contenu est-il cohérent avec le brief ?
5. **Cursor Coherence** : Le traitement CSS correspond au curseur A (voir CALIBRAGE CSS ci-dessus). Si A=2, vérifier ≥1 asymétrie de layout et ≥1 surface expressive. Si A=3, vérifier ≥1 convention cassée.
6. **Zero Dead Code** : Chaque `@keyframes` DOIT être utilisé. Chaque `@property` déclarée DOIT être animée. Zéro code mort.
7. **CSS Moderne** : Socle de finition obligatoire (oklch, @layer, @property, color-mix, text-wrap, clamp) + bonus contextuel si pertinent. Chaque technique doit SERVIR le design, pas être décorative.
8. **Interaction Coherence** : Si curseur A ≥ 2, AUCUN `:hover` ne doit contenir `transform: translateY()`. Alternatives : `background-color`, `border-color`, `opacity`, `filter`, `box-shadow`, `scale`, `clip-path`.
9. **Anti-Patterns Datés** : Vérifier qu'AUCUN pattern de la section "ANTI-PATTERNS DATÉS — BLACKLIST" n'est présent. En particulier : (a) aucun `transform: translateY()` dans un `:hover`, (b) aucune animation `infinite` décorative, (c) aucun `box-shadow: 0 0 Npx` (glow sans offset), (d) aucun `@keyframes` de type fade-up staggeré.
10. **Finition Élite** : (a) Si des ombres portées sont utilisées, chaque `box-shadow` a ≥2 couches empilées. (b) Aucune transition avec `ease` ou `ease-in-out` générique — utiliser les courbes nommées du `:root`. (c) Les 3 chapitres ont des padding-block DIFFÉRENTS. (d) Chaque élément interactif change ≥2 propriétés au hover.

## ⚠ AUDIT ANTI-SLOP DE FIN DE BATCH (avant STATUS: OK)
Regarde le fichier dans son ensemble — pas section par section — et vérifie :
1. Squint test : yeux mi-clos, la hiérarchie de chaque chapitre reste lisible (un titre domine, pas une bouillie de gris de même poids) ?
2. Une idée par sous-section : chaque 05.x / 06.x / 04.x / 07.x porte UN propos, pas deux empilés ?
3. Les cards justifient leur existence : élévation/containment servent une vraie séparation, jamais de la décoration — rien n'est mis en card « parce que c'est joli » ?
4. Rythme non répétitif : les 4 chapitres ont des poids et des densités visiblement différents (pas 4 blocs jumeaux qui se suivent) ?
5. Data-ink défendable (surtout ch.07) : aucun élément graphique qui n'ajoute rien — ombres gratuites, gradients qui ne signifient rien, conteneurs vides ?
6. Show > Tell : chaque carte qui DÉCRIT un traitement (style iconique, finition, grading) l'INCARNE en CSS ; les démos d'icônes/composants sont en contexte d'usage.
7. Entrée éditoriale sobre : kicker « Volume II · Système de Signes » discret avant le chapitre 05 ; PAS de cover band image, PAS de hero wordmark géant en ouverture (cf. amendement D54 du 2026-05-14).
8. **Icônes UI, PAS illustrations narratives (D59)** : aucune des icônes du chapitre 06 ne représente le SUJET du concept narratif (pas de phare, sextant, scène d'auscultation, câble sectionné, etc.). Toutes les icônes sont des fonctions UI réelles (`search`, `user`, `calendar`, `settings`…) ou des objets métier du brief, dans le STYLE de la famille assignée. Si tu trouves une "illustration" qui raconte une scène au lieu d'un pictogramme lisible à 24×24, c'est un anti-pattern racine — corrige.
9. **Squelette mockup 06.3 respecté (D59)** : le mockup 06.3 est UN seul, et son format appartient à la liste autorisée (sidebar / table+toolbar / toolbar / breadcrumb / list / nav). Aucun composant chapitre 04 dupliqué (pas de boutons primary/secondary, forms, cards d'action, alerts isolés).
Si tu détectes 2+ écarts → corrige avant de finaliser. Si 4+ → la structure est à reprendre, pas juste à retoucher.

## NOM DU CONCEPT VISIBLE
1. **<title>** : `<title>{brand} — Système de Signes — {chosen_concept_name}</title>` (la famille d'icônes `{icon_family_label}` n'apparaît pas dans le `<title>` — elle est documentée en intro du chapitre 06 dans le rendu).
2. **Footer subtitle** : `.batch-footer__sub` ou équivalent affiche
   `Système de Signes — {chosen_concept_name}`
En mode D (pas de concept) : omettre le nom du concept — le brand name suffit.

STATUS: OK quand tous les gates passent ET que l'audit anti-slop de fin de batch ne révèle aucun écart majeur.
Écris le fichier HTML dans : {skill_dir}/outputs/{session_dir}/{batch2_file}
