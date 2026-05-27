PROMPT SUBAGENT PHASE 7 (DESIGN SPECS — OPTIMISÉ):

Tu génères le document de Design Specs complet pour la marque {brand}.

## SPECS PRÉ-EXTRAITES (PAS BESOIN DE RELIRE LES FICHIERS)

### CURSEURS
A = {cursor_a} (Audace Créative)
B = {cursor_b} (Différenciation)

### PALETTE (extraite du :root)
- Primary : {color_primary} / {color_primary_light} / {color_primary_dark}
- Accent : {color_accent} / {color_accent_light} / {color_accent_dark}
- Surface : {color_surface} / {color_surface_alt}
- Text : {color_text_primary} / {color_text_secondary} / {color_text_muted}
- Semantic : success={color_success}, error={color_error}, warning={color_warning}
- DataViz : {color_dataviz_1}, {color_dataviz_2}, {color_dataviz_3}, {color_dataviz_4}

### TYPOGRAPHIE
- Display : {font_display}
- Body : {font_body}
- Mono : {font_mono}
- Type-scale : xs={text_xs}, sm={text_sm}, base={text_base}, lg={text_lg}, xl={text_xl}, 2xl={text_2xl}, 3xl={text_3xl}, 4xl={text_4xl}

### CODE CIVIL ATOMIQUE
- Radius : sm={radius_sm}, md={radius_md}, lg={radius_lg}, xl={radius_xl}, full={radius_full}
- Shadows : subtle={shadow_subtle}, sm={shadow_sm}, md={shadow_md}, lg={shadow_lg}, elevated={shadow_elevated}
- Spacing : xs={space_xs}, sm={space_sm}, md={space_md}, lg={space_lg}, xl={space_xl}, 2xl={space_2xl}
- Transitions : fast={transition_fast}, base={transition_base}, slow={transition_slow}

### RÉSUMÉ STRATÉGIQUE
- Tension de marque : {tension_summary}
- Intention créative : {intention_summary}
- Concept choisi : {chosen_concept_name}

## MISSION
Génère UN fichier Markdown structuré avec TOUTES les 47 sous-sections ci-dessous.
Le format est MARKDOWN (pas HTML). Sois concis mais complet : 2-3 phrases par sous-section.

## STRUCTURE ATTENDUE

# Design Specs — {brand}

## 01. Fondations Stratégiques
- 01.1 Calibration Curseurs — Explication du positionnement A×B
- 01.2 Intention Créative — La Big Idea, la vision
- 01.3 Territoire Sémantique — Le Mental Slot occupé
- 01.4 Tone of Voice — Personnalité, vocabulaire, do/don't
- 01.5 Ancre de Posture — Analogie mémorable ("Nous sommes le X du Y")

## 02. Color System
- 02.1 Primary Brand Scale — 3 teintes principales + HEX
- 02.2 Secondary & Accent Scale — Couleurs secondaires et accents
- 02.3 Neutrals & Surfaces — 5 nuances de neutres
- 02.4 Semantic & Status — success, error, warning, info
- 02.5 Data-Viz Palette — 4 couleurs dédiées aux graphiques
- 02.6 WCAG Compliance — Ratios de contraste, accessibilité

## 03. Typographie
- 03.1 Pairing Stratégique — Les 2-3 fonts et leur rôle
- 03.2 Type Scale — Ratio et toutes les valeurs xs→4xl
- 03.3 Rôles Fonctionnels — Quand utiliser quelle font
- 03.4 Directives de Lisibilité — Line-height, letter-spacing, max-width

## 04. Code Civil Atomique
- 04.1 Système d'Arrondis — Radius par contexte
- 04.2 Élévation & Profondeur — Shadows et z-index
- 04.3 Gradients & Blending — Dégradés et modes de fusion
- 04.4 Épaisseurs & Tracés — Borders, strokes
- 04.5 Grille de Rythme — Spacing basé sur 8px
- 04.6 Motion & Transitions — Les 3+ courbes d'easing nommées (cubic-bezier exact), les 4 paliers de durée (fast, base, slow, auscultation), et la règle "jamais ease générique"
- 04.7 Component Tokens — Pour chaque composant UI (bouton primary/secondary, badge sémantique, input, toggle, card, alert) : le padding, le radius, les couleurs par état (default/hover/active/disabled/focus), la shadow utilisée, et la transition appliquée. Référencer le Batch 2 chapitre §04 pour la documentation visuelle détaillée.

## 05. Logotype
- 05.1 Concept & Symbolique — Signification du logo
- 05.2 Système de Lockups — Variantes (horizontal, stacked, icon-only)
- 05.3 Zone d'Exclusion — Espace de protection minimum
- 05.4 Variantes de Contexte — Light mode, dark mode, monochrome

## 06. Iconographie
- 06.1 Grammaire Iconique — Style général (outlined, filled, duotone)
- 06.2 Épaisseur & Finitions — Stroke width, corner style
- 06.3 Niveau d'Abstraction — Réaliste vs symbolique
- 06.4 DA Illustrative — Direction artistique des icônes métier

## 07. Data Visualization
- 07.1 Style des Graphiques — Bar charts, line charts, donuts
- 07.2 Système de Grilles — Axes, ticks, labels
- 07.3 Usage de la Couleur — Palette data-viz appliquée
- 07.4 Typographie de la Donnée — Font sizes, alignements

## 08. Direction Photographique
- 08.1 Style Photographique — Ambiance, lumière, sujets
- 08.2 Traitement Chromatique — Color grading, filtres
- 08.3 Scénographie Produit — Mise en scène des produits
- 08.4 Signature de Prompting IA — Prompt-type pour MidJourney (+ Recraft si illustration flat)

## 09. Système de Composition
- 09.1 Architecture de Grilles — Colonnes, gouttières, marges
- 09.2 Stratégie de Densité — Aéré vs compact selon contexte
- 09.3 Patterns de Mise en Page — Templates récurrents (Hero Split, Bento Grid)
- 09.4 Rythme Vertical — Spacing entre sections

## 10. Illustration Narrative
- 10.1 Angle de Métaphore — Métaphore visuelle centrale
- 10.2 Physique de l'Illustration — Style graphique (flat, 3D, organique)
- 10.3 Character Design — Si personnages : style, proportions
- 10.4 Lois de Composition — Règles de mise en page des illustrations
- 10.5 Directives de Prompting IA — Prompt-type pour illustrations (MJ + Recraft selon registre)

## CONTRAINTES IMPORTANTES
- Format : MARKDOWN (pas HTML)
- Longueur : ~250-350 lignes max
- **Texte en français avec accents UTF-8** : utiliser les caractères accentués natifs (é, è, ê, à, ç, ù, etc.), JAMAIS de texte sans accents
- Inclure les valeurs HEX/pixels EXACTES des specs fournies ci-dessus
- Être concis : 2-3 phrases par sous-section, pas de blabla
- NE PAS relire les fichiers de référence — toutes les données sont dans ce prompt

## GATE DE VALIDATION
Avant de finaliser, vérifie que TU AS BIEN les 40 sous-sections :
- 01.1 → 01.5 (5)
- 02.1 → 02.6 (6)
- 03.1 → 03.4 (4)
- 04.1 → 04.7 (7)
- 05.1 → 05.4 (4)
- 06.1 → 06.4 (4)
- 07.1 → 07.4 (4)
- 08.1 → 08.4 (4)
- 09.1 → 09.4 (4)
- 10.1 → 10.5 (5)
TOTAL = 47 sous-sections

Si UNE SEULE manque → AJOUTE-LA avant de finaliser.

STATUS: OK quand les 47 sous-sections sont présentes et les valeurs exactes incluses.
Écris le fichier dans : {skill_dir}/outputs/{session_dir}/{specs_file}
