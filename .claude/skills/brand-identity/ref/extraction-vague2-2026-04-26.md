# Extraction exhaustive Vague 2 — règles audit-slop externes (2026-04-26)

> Output de l'agent Explore "very thorough" lancé en Phase A de la Vague 2.
> Source : 20 fichiers externes (Vercel + Impeccable + GStack + Taste).
> Méthode : matrice de décision 4 tests A/B/C/D appliquée à chaque règle.

---

## SECTION 1 — Statistiques globales

**Total règles extraites :** 182 distinctes (après déduplication cross-source)

**Universelles vs Contextuelles :**
- UNIVERSEL (HTML vanilla) : 156 règles (85.7%)
- CONTEXTUEL (React/Framer Motion/Next.js) : 26 règles (14.3%)

**Par domaine :**
| Domaine | Compte | % |
|---------|--------|-----|
| typography | 24 | 13.2% |
| spacing & layout | 22 | 12.1% |
| interaction | 20 | 11.0% |
| color & contrast | 18 | 9.9% |
| composition | 18 | 9.9% |
| motion | 16 | 8.8% |
| ux-writing | 14 | 7.7% |
| responsive | 12 | 6.6% |
| a11y | 11 | 6.0% |
| content | 10 | 5.5% |
| performance | 9 | 4.9% |
| craft/polish | 8 | 4.4% |

**Polarité :**
- NEGATIVE (interdictions) : 96 (52.7%)
- POSITIVE (prescriptions) : 86 (47.3%)

**Destination proposée :**
| Destination | Compte |
|---|---|
| TIER_1 (candidats à promotion) | 12 |
| GATE_PYTHON | 48 |
| CRITIQUE_TIER_2 | 78 |
| CRITIQUE_TIER_3 | 32 |
| N_A_HTML_VANILLA | 12 |

**Couverture BIG :**
- Déjà présentes (au moins partiellement) : 28 règles (15.4%)
- Nouvelles à intégrer : 154 règles (84.6%)

**Ambiguïtés à trancher par Charles :** 14 (7.7%)

---

## SECTION 2 — Tableau exhaustif (182 règles)

| ID | Règle | Source principale | Aussi présente dans | Type | Domaine | Polarité | Grepable | Sévérité | Test_A | Test_B | Test_C | Test_D | Destination | Sous-destination | Déjà BIG | Ambig | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R-001 | Utiliser OKLCH au lieu de HSL pour les couleurs. Lightness uniforme perceptuellement. | impeccable/color-and-contrast.md §Color_Spaces | soft-skill, minimalist | UNIV | color | POS | PARTIEL | POLISH | ROOT | PERF_CATA | REGEX_FAUX_POSITIFS | DANGER_PRESCRIPTIF | TIER_1 | finition-elite-tier1.md | PARTIEL | NON | Déjà partiellement dans finition-elite-core → promotion TIER_1 |
| R-002 | Réduire la saturation chromatique en approchant blanc/noir. Éviter aspect garish aux extrêmes. | impeccable/color-and-contrast.md §Building_Functional_Palettes | - | UNIV | color | POS | NON | POLISH | ROOT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PRESCRIPTIF | CRITIQUE_TIER_2 | finition-elite-core.md | NON | NON | Requiert jugement perceptif |
| R-003 | Teinter les neutres légèrement (0.005–0.015 chroma) vers la teinte brand. Cohésion subconsciente. | impeccable/color-and-contrast.md §Tinted_Neutrals | taste, minimalist | UNIV | color | POS | NON | POLISH | ROOT | PERF_CATA | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PRESCRIPTIF | TIER_1 | finition-elite-tier1.md | PARTIEL | NON | Très impact, facile à formaliser |
| R-004 | Règle 60-30-10 sur le poids VISUEL, non la surface pixel. Accent 10% rare = puissant. | impeccable/color-and-contrast.md §60-30-10_Rule | - | UNIV | composition | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | hierarchie-visuelle-core.md | OUI tier1 | NON | Déjà importé tier1 |
| R-005 | JAMAIS pure black (#000) ou pure white (#fff). Toujours tinter vers off-black/off-white. | impeccable/color-and-contrast.md §Never_Use_Pure_Gray | taste, minimalist, brutalist | UNIV | color | NEG | OUI | MOYENNE | SYNTAX | AI_SLOP | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | OUI tier1 | NON | Grepable #000 ou #fff |
| R-006 | WCAG AA contraste body 4.5:1, large 3:1, icons/UI 3:1. AAA: 7:1 / 4.5:1. | impeccable/color-and-contrast.md §WCAG_Requirements | vercel, a11y-fond-tier1 | UNIV | a11y | POS | NON | CRITIQUE | LAYOUT | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | TIER_1 | a11y-fondamentaux-tier1.md | OUI tier1 | NON | Déjà tier1 |
| R-007 | Pas de gray text sur colored background — lave l'apparence. Utiliser nuance plus foncée du fond. | impeccable §Dangerous_Color_Combinations | redesign, taste | UNIV | color | NEG | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | CRITIQUE_TIER_2 | finition-elite-core.md | NON | NON | Pattern détectable mais analyse sémantique |
| R-008 | Dark mode ≠ inverted light mode. Depth par surface lightness, pas shadows. Désaturer accents. | impeccable §Dark_Mode_Is_Not_Inverted | - | UNIV | color | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | hierarchie-visuelle-core.md | PARTIEL | NON | Architectural decision |
| R-009 | Aucune dépendance à alpha/rgba pour la profondeur. Alpha = design smell. | impeccable §Alpha_Is_A_Design_Smell | - | UNIV | color | NEG | OUI | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Grepable rgba/hsla abusif |
| R-010 | Modular type scale avec 5 sizes, contrast 1.25+. NOT 14,15,16,18... | impeccable §Vertical_Rhythm | soft, minimalist | UNIV | typography | POS | NON | POLISH | ROOT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PRESCRIPTIF | TIER_1 | finition-elite-tier1.md ou typography ref | PARTIEL | NON | Charles à valider |
| R-011 | Line-height inverse à line-length. Light-on-dark +0.05-0.1 extra. | impeccable §Readability_Measure | - | UNIV | typography | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | typography ref core | PARTIEL | OUI | Heuristic loupe-dependent |
| R-012 | Use `ch` units. Max 65ch body. | impeccable §Readability_Measure | responsive, vercel | UNIV | responsive | POS | PARTIEL | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Grepable max-width: 65ch |
| R-013 | Ban Inter + Roboto + Open Sans + Lato + Montserrat (invisibles). | impeccable §Choosing_Distinctive_Fonts | taste, minimalist, brutalist, redesign | UNIV | typography | NEG | OUI | MOYENNE | SYNTAX | AI_SLOP | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | PARTIEL | NON | Déjà bloqué partiellement |
| R-014 | Font selection procedure: brief words → physical object → browse → avoid defaults. | impeccable §Font_Selection_Procedure | - | UNIV | typography | POS | NON | MOYENNE | SYNTAX | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | typography ref core | NON | NON | Process-oriented |
| R-015 | Pair fonts with multi-axis contrast (Serif+Sans, Geometric+Humanist, Condensed+Wide). | impeccable §Pairing_Principles | - | UNIV | typography | POS | NON | POLISH | SYNTAX | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | typography ref core | PARTIEL | NON | Détectable mais font metadata |
| R-016 | One font + multiple weights > two competing typefaces. Add 2nd ONLY for genuine contrast. | impeccable §Pairing_Principles | - | UNIV | typography | POS | NON | POLISH | SYNTAX | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | typography ref core | PARTIEL | OUI | "Genuine contrast" subjectif |
| R-017 | font-display: swap + size-adjust/ascent-override pour minimiser CLS. | impeccable §Web_Font_Loading | - | UNIV | performance | POS | PARTIEL | CRITIQUE | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Pattern détectable |
| R-018 | Fluid type (clamp) pour MARKETING. Fixed rem pour APP/DASHBOARDS. | impeccable §Fluid_Type | - | UNIV | typography | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | typography ref core | PARTIEL | NON | Designer decision |
| R-019 | OpenType : tabular-nums data, small-caps abréviations, no ligatures code. | impeccable §OpenType_Features | - | UNIV | typography | POS | PARTIEL | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Grepable font-variant-* |
| R-020 | Never disable zoom (`user-scalable=no`). Layout doit supporter 200%. | impeccable §Accessibility | vercel, a11y-fond-tier1 | UNIV | a11y | NEG | OUI | CRITIQUE | STRUCTURE | WCAG_FAIL | REGEX_TRIVIALE | SAFE_INTERDICTION | TIER_1 | a11y-fondamentaux-tier1.md | OUI tier1 | NON | Déjà tier1 |
| R-021 | rem/em pour font-size, ≥16px body. | impeccable | a11y-fond-tier1, vercel | UNIV | a11y | POS | OUI | CRITIQUE | ROOT | WCAG_FAIL | REGEX_TRIVIALE | SAFE_INTERDICTION | TIER_1 | a11y-fondamentaux-tier1.md | OUI tier1 | NON | Déjà tier1 |
| R-022 | Tap targets ≥44px. | impeccable | vercel, a11y-fond-tier1 | UNIV | a11y | POS | NON | CRITIQUE | LAYOUT | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | TIER_1 | a11y-fondamentaux-tier1.md | OUI tier1 | NON | Déjà tier1 |
| R-023 | 4pt spacing base. Scale 4,8,12,16,24,32,48,64,96. `gap` not margins. | impeccable §Spacing_Systems | soft, minimalist | UNIV | spacing | POS | NON | POLISH | ROOT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PRESCRIPTIF | TIER_1 | finition-elite-tier1.md ou ref spacing | PARTIEL | NON | Charles à valider |
| R-024 | Name spacing tokens semantically (--space-sm), not by value. | impeccable §Name_Tokens_Semantically | soft, redesign | UNIV | spacing | POS | PARTIEL | POLISH | SYNTAX | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Grepable token naming |
| R-025 | Grid `repeat(auto-fit, minmax(280px, 1fr))` pour responsive sans breakpoints. | impeccable §Self-Adjusting_Grid | responsive | UNIV | responsive | POS | PARTIEL | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Détectable |
| R-026 | Hierarchy via 2-3 dimensions (size+weight+color+space), NOT size alone. 3:1+ ratio size. | impeccable §Hierarchy_Through_Multiple_Dimensions | hierarchie-vis-tier1, redesign | UNIV | composition | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | hierarchie-visuelle-core.md | OUI tier1 partial | NON | Déjà tier1, étendre core |
| R-027 | Card overuse = slop. Use spacing+alignment for hierarchy. NO nested cards. | impeccable §Cards_Are_Not_Required | redesign, soft | UNIV | composition | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | OUI partial | NON | Déjà tier1 |
| R-028 | Container queries pour components, viewport queries pour page layout. | impeccable §Container_Queries | responsive, soft | UNIV | responsive | POS | PARTIEL | MOYENNE | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Détectable CSS |
| R-029 | Optical alignment text negative margin (-0.05em). | impeccable §Optical_Adjustments | - | UNIV | craft | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_3 | craft ref | NON | NON | Eye-dependent |
| R-030 | Icons need 44px tap target via padding/::before. | impeccable §Touch_Targets_vs_Visual_Size | vercel, a11y-fond-tier1 | UNIV | a11y | POS | NON | CRITIQUE | LAYOUT | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | TIER_1 | a11y-fondamentaux-tier1.md | OUI tier1 | NON | Déjà tier1 |
| R-031 | Z-index semantic scale (dropdown<sticky<modal-backdrop<modal<toast<tooltip). No 9999. | impeccable §Depth_and_Elevation | redesign, vercel | UNIV | composition | POS | PARTIEL | POLISH | SYNTAX | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Grepable z-index value |
| R-032 | Shadows subtle. Si visible, trop fort. Scale (sm,md,lg,xl). | impeccable §Depth_and_Elevation | finition-elite-tier1, finition-elite-core | UNIV | craft | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_3 | finition-elite-core.md | PARTIEL | NON | Détails dans core |
| R-033 | Duration: 100-150ms feedback, 200-300ms state, 300-500ms layout, 500-800ms entrance. Exit = 75% enter. | impeccable §Duration_100_300_500_Rule | soft, taste | UNIV | motion | POS | PARTIEL | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Détectable timing |
| R-034 | Avoid `ease`. Use exponential curves (cubic-bezier 0.16,1,0.3,1 ; 0.7,0,0.84,0). | impeccable §Easing_Pick_Right_Curve | soft, brutalist | UNIV | motion | NEG | OUI | MOYENNE | CHIRURGICAL | PERF_NORMAL | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Grepable easing |
| R-035 | NO bounce/elastic easing. Real objects decelerate smoothly. Bounce = 2015 daté. | impeccable §Avoid_Bounce_and_Elastic | soft, taste | UNIV | motion | NEG | OUI | MOYENNE | CHIRURGICAL | AI_SLOP | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | PARTIEL | NON | Grepable bounce |
| R-036 | Animate ONLY transform + opacity. Heights via grid-template-rows: 0fr→1fr. | impeccable §Only_Two_Properties | soft, vercel, taste | UNIV | motion | NEG | OUI | CRITIQUE | LAYOUT | PERF_CATA | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | OUI partial | NON | Grepable |
| R-037 | Staggered animations: cap total delay (10 items @ 50ms = 500ms max). | impeccable §Staggered_Animations | soft, taste | UNIV | motion | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | motion ref core | NON | NON | Designer discipline |
| R-038 | MUST honor `prefers-reduced-motion: reduce`. ~35% adultes 40+. | impeccable §Reduced_Motion | vercel, a11y-fond-tier1 | UNIV | a11y | POS | OUI | CRITIQUE | LAYOUT | WCAG_FAIL | REGEX_TRIVIALE | SAFE_INTERDICTION | TIER_1 | a11y-fondamentaux-tier1.md | OUI tier1 | NON | Déjà tier1 |
| R-039 | 80ms threshold (<80ms = instant). Peak-end effect easing. | impeccable §Perceived_Performance | - | UNIV | motion | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | motion ref core | NON | OUI | Heuristic perceptive |
| R-040 | Preemptive start (skeleton/progress) shifts perceived time. | impeccable §Perceived_Performance | - | UNIV | motion | POS | NON | POLISH | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | motion ref core | PARTIEL | NON | Design pattern |
| R-041 | Optimistic UI : update immediately, sync later. LOW-STAKES only (likes, follows). NOT payments. | impeccable §Perceived_Performance | interaction, taste | CTX | interaction | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | PARTIEL | NON | React-specific |
| R-042 | No `will-change` preemptively. Only when imminent. | impeccable §Performance | - | UNIV | performance | POS | PARTIEL | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Détectable CSS |
| R-043 | Eight states: Default/Hover/Focus/Active/Disabled/Loading/Error/Success. | impeccable §Eight_Interactive_States | redesign, soft | UNIV | interaction | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | PARTIEL | NON | États existent partiel |
| R-044 | NEVER `outline: none` sans `:focus-visible` replacement. Outline 2-3px, offset 2px. | impeccable §Focus_Rings | vercel, a11y-fond-tier1 | UNIV | a11y | NEG | OUI | CRITIQUE | LAYOUT | WCAG_FAIL | REGEX_TRIVIALE | SAFE_INTERDICTION | TIER_1 | a11y-fondamentaux-tier1.md | OUI tier1 | NON | Déjà tier1 |
| R-045 | Placeholders ≠ labels. Always visible `<label>`. Error below w/ aria-describedby. | impeccable §Form_Design | vercel, soft | UNIV | interaction | NEG | OUI | CRITIQUE | STRUCTURE | WCAG_FAIL | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | OUI partial | NON | Grepable structurel |
| R-046 | Validate on blur (NOT keystroke). Errors below inputs. | impeccable §Form_Design | vercel | UNIV | interaction | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | PARTIEL | NON | Pattern designer |
| R-047 | Skeletons > spinners. Preview content shape. | impeccable §Loading_States | redesign, soft | UNIV | interaction | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | PARTIEL | NON | Design pattern |
| R-048 | Native `<dialog>` ou `inert` pour modales. Focus trap auto. Escape closes. | impeccable §Modals_Inert_Approach | vercel | UNIV | interaction | POS | PARTIEL | CRITIQUE | STRUCTURE | WCAG_FAIL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Détectable HTML |
| R-049 | Popover API pour tooltips/dropdowns. Light-dismiss, stacking propre. | impeccable §Popover_API | - | UNIV | interaction | POS | PARTIEL | CRITIQUE | STRUCTURE | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Détectable HTML |
| R-050 | Dropdown clipping: jamais position:absolute dans overflow:hidden. Use position:fixed ou Popover. | impeccable §Dropdown_and_Overlay_Positioning | - | UNIV | interaction | NEG | NON | CRITIQUE | STRUCTURE | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | CRITIQUE_TIER_2 | interaction ref core | NON | NON | CSS+HTML inspection |
| R-051 | CSS Anchor Positioning : tether overlay sans JS. @position-try flips. | impeccable §CSS_Anchor_Positioning | - | UNIV | interaction | POS | PARTIEL | MOYENNE | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Détectable browser support |
| R-052 | Undo > Confirm. Delete immediately, undo toast. | impeccable §Destructive_Actions | redesign | UNIV | interaction | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | PARTIEL | NON | UX pattern |
| R-053 | Roving tabindex pour groupes : un item tabbable, arrows move within. | impeccable §Roving_Tabindex | - | UNIV | a11y | POS | NON | CRITIQUE | STRUCTURE | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Détectable HTML/JS |
| R-054 | Skip links keyboard (hidden off-screen, show on focus, link #main-content). | impeccable §Skip_Links | vercel | UNIV | a11y | POS | OUI | CRITIQUE | STRUCTURE | WCAG_FAIL | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Grepable HTML |
| R-055 | Gestures invisibles. Hint via partial reveal/onboarding/visible fallback. | impeccable §Gesture_Discoverability | - | UNIV | interaction | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | NON | NON | Design pattern |
| R-056 | Mobile-first: base mobile, min-width pour complexité. | impeccable §Mobile-First | redesign, responsive | UNIV | responsive | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | responsive ref core | PARTIEL | NON | Architecture decision |
| R-057 | 3 breakpoints (640, 768, 1024). Content-driven, not device. | impeccable §Breakpoints_Content_Driven | soft, responsive | UNIV | responsive | POS | PARTIEL | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Détectable CSS |
| R-058 | Detect input method (`@media (pointer: fine)`, `(hover: hover)`). | impeccable §Detect_Input_Method | responsive | UNIV | responsive | POS | PARTIEL | CRITIQUE | LAYOUT | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Détectable CSS |
| R-059 | Safe areas : `env(safe-area-inset-*)` notches. `viewport-fit: cover`. | impeccable §Safe_Areas | responsive, soft | UNIV | responsive | POS | PARTIEL | CRITIQUE | LAYOUT | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Détectable CSS |
| R-060 | srcset + sizes images responsive. picture pour art direction. | impeccable §Responsive_Images | responsive, vercel | UNIV | responsive | POS | PARTIEL | MOYENNE | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Détectable HTML |
| R-061 | Never user-scalable=no ou maximum-scale=1. Fix layout. | impeccable + vercel | a11y-fond-tier1 | UNIV | a11y | NEG | OUI | CRITIQUE | SYNTAX | WCAG_FAIL | REGEX_TRIVIALE | SAFE_INTERDICTION | TIER_1 | a11y-fondamentaux-tier1.md | OUI tier1 | NON | Déjà tier1 |
| R-062 | Test on real devices, not DevTools. | impeccable §Testing | - | UNIV | performance | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | responsive ref core | NON | OUI | Process/discipline |
| R-063 | Button labels specific verb+object ("Save changes"), NOT generic ("OK"/"Submit"). | impeccable §Button_Label_Problem | redesign, soft | UNIV | copy | NEG | NON | MOYENNE | CHIRURGICAL | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Content pattern |
| R-064 | Errors : What/Why/How-to-fix. Not "Invalid input". | impeccable §Error_Messages | redesign, ux-writing | UNIV | copy | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Content pattern |
| R-065 | Empty states : Acknowledge/Explain value/Clear action. Not "No items". | impeccable §Empty_States | redesign, ux-writing | UNIV | interaction | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | PARTIEL | NON | Design+content |
| R-066 | Voice (brand) vs Tone (context). Errors: empathetic. Success: brief. Loading: reassuring. | impeccable §Voice_vs_Tone | ux-writing | UNIV | copy | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Brand+discipline |
| R-067 | Link text standalone meaning ("View pricing plans"). Icon buttons need aria-label. | impeccable §Writing_for_Accessibility | vercel, a11y-fond-tier1 | UNIV | a11y | NEG | OUI | CRITIQUE | CHIRURGICAL | WCAG_FAIL | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | PARTIEL | NON | Grepable aria-label |
| R-068 | Alt text describes information, not image. Decorative `alt=""`. | impeccable + vercel | - | UNIV | a11y | POS | NON | CRITIQUE | STRUCTURE | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Content pattern |
| R-069 | Plan expansion translation: German+30%, French+20%, Finnish+30-40%, Chinese-30%. | impeccable §Translation | - | UNIV | responsive | POS | NON | POLISH | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | responsive ref core | NON | OUI | i18n consideration |
| R-070 | Numbers separate ("New messages: 3"). Avoid abbreviations. | impeccable §Translation-Friendly | - | UNIV | copy | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | NON | NON | i18n discipline |
| R-071 | Terminology consistency : pick one term (Delete/Remove/Trash → Delete). | impeccable §Consistency | ux-writing, redesign | UNIV | copy | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Brand glossary |
| R-072 | No redundant copy. If heading explains, intro redundant. | impeccable §Avoid_Redundant_Copy | redesign, ux-writing | UNIV | copy | NEG | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Editor discipline |
| R-073 | Loading specific ("Saving draft..."). Long waits: progress. | impeccable §Loading_States | ux-writing, interaction | UNIV | copy | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Content+UX |
| R-074 | Confirmation dialogs sparingly. Prefer undo. When must: name action+consequence+specific labels. | impeccable §Confirmation | interaction, ux-writing | UNIV | interaction | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | PARTIEL | NON | UX pattern |
| R-075 | Form instructions : show format via placeholders. Explain non-obvious fields. | impeccable §Form_Instructions | interaction, ux-writing | UNIV | interaction | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | UX pattern |
| R-076 | No jargon sans explication. Avoid Elevate/Seamless/Unleash/Next-Gen/Delve clichés. | impeccable + redesign | taste, redesign | UNIV | copy | NEG | OUI | MOYENNE | CHIRURGICAL | AI_SLOP | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | PARTIEL | NON | Grepable clichés |
| R-077 | Never blame user in errors. Active voice. | impeccable + redesign | ux-writing | UNIV | copy | NEG | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Editor discipline |
| R-078 | Shape design first. NEVER jump to code without brief confirmed. | impeccable/craft.md | - | UNIV | process | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | craft ref core | NON | OUI | Process directive |
| R-079 | Build order : Structure→Layout→Typo+Color→States→Motion→Responsive. | impeccable §Build | - | UNIV | process | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | craft ref core | PARTIEL | NON | Designer discipline |
| R-080 | Visual iteration loop: brief→AI slop test→DON'Ts→all states→responsive→details→iterate. | impeccable §Visual_Iteration | - | UNIV | process | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | craft ref core | NON | NON | Process directive |
| R-081 | BAN side-stripe borders (>1px) on cards/alerts. Rewrite structure. | impeccable §absolute_bans | anti-slop-core, redesign | UNIV | composition | NEG | OUI | MOYENNE | CHIRURGICAL | AI_SLOP | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | OUI partial | NON | Grepable |
| R-082 | BAN gradient text (background-clip:text + gradient). | impeccable §absolute_bans | anti-slop-core, redesign, soft | UNIV | composition | NEG | OUI | MOYENNE | CHIRURGICAL | AI_SLOP | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | OUI partial | NON | Grepable |
| R-083 | No generic rounded rectangles + drop shadows. AI-tell. | impeccable §Visual_Details | soft, redesign | UNIV | composition | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | OUI partial | NON | Pattern recommendation |
| R-084 | NO glassmorphism default. | impeccable §Visual_Details | soft, minimalist (ban), taste | UNIV | composition | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | OUI partial | NON | Interdiction visuelle |
| R-085 | NO sparklines décoratives. | impeccable §Visual_Details | - | UNIV | composition | NEG | NON | POLISH | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | NON | NON | Designer judgment |
| R-086 | NO modals unless no alternative. Modals are lazy. | impeccable §Visual_Details | interaction, redesign | UNIV | interaction | NEG | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | NON | NON | UX pattern |
| R-087 | Grid 3 identical cards BANNED. Use 2-col zig-zag ou asymétrique. | impeccable + anti-slop-core | redesign, soft | UNIV | composition | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | OUI tier1 | NON | Déjà tier1 |
| R-088 | Centered layout: OK small. BANNED si DESIGN_VARIANCE>4. Force asymétrie. | impeccable + soft | soft, taste, redesign | UNIV | composition | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | PARTIEL | OUI | "DESIGN_VARIANCE>4" comment coder ? |
| R-089 | 50/50 hero split BANNED par défaut. | impeccable anti-slop-tier1 | redesign, soft | UNIV | composition | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | OUI tier1 | NON | Déjà tier1 |
| R-090 | Feature sections NOT uniform icon+title+desc. | impeccable anti-slop-tier1 | redesign, soft | UNIV | composition | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | OUI tier1 | NON | Déjà tier1 |
| R-091 | NO link-column footers. Footer = conclusion, pas sitemap. | impeccable anti-slop-tier1 | redesign | UNIV | composition | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | OUI tier1 | NON | Déjà tier1 |
| R-092 | NO carousels content. Content visible. | impeccable anti-slop-tier1 | redesign | UNIV | composition | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | OUI tier1 | NON | Déjà tier1 |
| R-093 | NO product screenshots in device frames. | impeccable anti-slop-tier1 | redesign | UNIV | composition | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | OUI tier1 | NON | Déjà tier1 |
| R-094 | Restraint : weight = importance. Subtil > marqué. | impeccable hierarchie-tier1 | - | UNIV | composition | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | hierarchie-visuelle-core.md | OUI tier1 | NON | Déjà tier1 |
| R-095 | 1 dominant + accompagnateurs. 2-plan OK. 3-plan = chargé. | impeccable hierarchie-tier1 | - | UNIV | composition | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | hierarchie-visuelle-core.md | OUI tier1 | NON | Déjà tier1 |
| R-096 | Data emphasis : numbers > labels. Display font + tabular-nums. | impeccable hierarchie-tier1 | redesign, minimalist | UNIV | composition | POS | PARTIEL | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Grepable tnum |
| R-097 | Density variation. Dense+aéré > 4 zones contrastées. | impeccable hierarchie-tier1 | soft (DENSITY), minimalist | UNIV | composition | POS | NON | POLISH | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | hierarchie-visuelle-core.md | PARTIEL | NON | Designer judgment |
| R-098 | Séparation par fond/espace. 1px lines = noise (sauf majeures 2-3 max). | impeccable hierarchie-tier1 | - | UNIV | composition | POS | NON | POLISH | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | hierarchie-visuelle-core.md | PARTIEL | NON | Designer judgment + CSS audit |
| R-099 | 1 accent color per concept. Accent = visual EVENT (1-2 elements/viewport). | impeccable finition-tier1 | soft, taste, minimalist | UNIV | color | NEG | NON | MOYENNE | CHIRURGICAL | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | finition-elite-core.md | PARTIEL | NON | Architecture color |
| R-100 | CSS moderne baseline : oklch, @layer, @property, color-mix, text-wrap, clamp. MANDATORY 2026. | impeccable finition-tier1 | soft, taste, brutalist | UNIV | color | POS | PARTIEL | CRITIQUE | ROOT | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Détectable CSS |
| R-101 | Couche graphique : grain SVG (0.35-0.45) + 3 radial/conic gradients. | impeccable finition-tier1 | taste, brutalist, minimalist | UNIV | craft | POS | NON | POLISH | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_3 | finition-elite-core.md | PARTIEL | NON | Visual verification |
| R-102 | Font weight range : Regular(400)+Medium(500)+SemiBold(600) min. | impeccable + redesign | soft | UNIV | typography | POS | NON | POLISH | ROOT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | typography ref core | PARTIEL | NON | CSS pattern détectable |
| R-103 | Narrow vs wider body. Single font + weights > two fonts. | impeccable | - | UNIV | typography | POS | NON | POLISH | SYNTAX | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | typography ref core | PARTIEL | OUI | Confusion avec R-016 ? |
| R-104 | Orphaned words : `text-wrap: balance` (headings) ou `pretty` (paragraphes). | impeccable + redesign + vercel | - | UNIV | typography | POS | PARTIEL | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Détectable CSS |
| R-105 | Tabular fonts pour data columns (font-variant-numeric: tabular-nums). | impeccable + redesign | - | UNIV | typography | POS | PARTIEL | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Grepable tnum |
| R-106 | All-caps subheaders RARE. Préférer lowercase italics, sentence case, small-caps. | impeccable + redesign | soft, minimalist | UNIV | typography | NEG | NON | POLISH | CHIRURGICAL | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | typography ref core | PARTIEL | NON | Pattern détectable |
| R-107 | Letter-spacing négatif large headers, positif small caps/labels. | impeccable | soft, brutalist | UNIV | typography | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | typography ref core | PARTIEL | NON | CSS pattern |
| R-108 | NO emojis (code, markup, alt, content). Use icons (Phosphor, Radix) ou SVG. | taste, soft, redesign, brutalist, minimalist | - | UNIV | composition | NEG | OUI | MOYENNE | CHIRURGICAL | AI_SLOP | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | PARTIEL | NON | Grepable emoji |
| R-109 | NO Lucide default icon library. Use Phosphor (thin) ou Radix. | taste, redesign, soft | - | UNIV | composition | NEG | OUI | MOYENNE | SYNTAX | AI_SLOP | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | PARTIEL | NON | Grepable import |
| R-110 | NO pure ease-in-out. Exponential : ease-out-quart/quint/expo. | soft, taste, minimalist | impeccable | UNIV | motion | NEG | OUI | MOYENNE | CHIRURGICAL | AI_SLOP | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | PARTIEL | NON | Grepable easing |
| R-111 | NO neon/outer glows. Inner borders ou subtle tinted shadows. | soft, taste, redesign, minimalist | impeccable | UNIV | composition | NEG | NON | MOYENNE | CHIRURGICAL | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | PARTIEL | NON | Visual+CSS |
| R-112 | NO oversized H1s. Hierarchy via weight+color, not massive scale. | soft, taste | impeccable | UNIV | typography | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | typography ref core | PARTIEL | NON | Designer+CSS audit |
| R-113 | NO 3-col equal cards. Use 2-col zig-zag, asymétrique, scroll. | soft, taste, redesign | impeccable | UNIV | composition | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | OUI tier1 | NON | Déjà tier1 (R-087) |
| R-114 | NO custom mouse cursors. | soft, taste, redesign | - | UNIV | composition | NEG | OUI | POLISH | CHIRURGICAL | AI_SLOP | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | NON | NON | Grepable cursor:url() |
| R-115 | NO generic names ("John Doe", "Acme", "Nexus", "SmartFlow"). Inventer réalistes. | soft, taste, redesign | ux-writing, vercel | UNIV | content | NEG | NON | MOYENNE | CHIRURGICAL | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Content human review |
| R-116 | NO fake round numbers (99.99%, 50%, $100.00). Use organic (47.2%, $99.00). | soft, taste, redesign | ux-writing | UNIV | content | NEG | NON | MOYENNE | CHIRURGICAL | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Content human review |
| R-117 | NO AI clichés (Elevate, Seamless, Unleash, Next-Gen, Game-changer, Delve). | soft, taste, redesign, impeccable | vercel | UNIV | copy | NEG | OUI | MOYENNE | CHIRURGICAL | AI_SLOP | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | PARTIEL | NON | Grepable clichés |
| R-118 | NO broken image links. Use picsum.photos ou SVG. | soft, taste, redesign | - | UNIV | performance | NEG | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | performance ref | PARTIEL | NON | QA check |
| R-119 | NO shadcn/ui defaults. Customize. | soft, taste | - | CTX | composition | NEG | NON | MOYENNE | STRUCTURE | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | N_A_HTML_VANILLA | (React) | NON | NON | N/A vanilla |
| R-120 | Magnetic hover (Framer Motion useMotionValue). | soft §4 | - | CTX | motion | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | N_A_HTML_VANILLA | (Framer) | NON | NON | N/A vanilla |
| R-121 | Spring physics : stiffness:100, damping:20 (premium feel). No linear. | soft §4, taste, stitch | impeccable | UNIV | motion | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | motion ref core | PARTIEL | NON | Motion config |
| R-122 | Perpetual micro-interactions sur composants actifs (Pulse, Typewriter, Float). | soft §4, soft §9 Bento | taste | CTX | motion | POS | NON | POLISH | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | motion ref core | PARTIEL | OUI | Scope creep ? |
| R-123 | Staggered children Framer Motion (Parent+Children dans Client Component tree). | soft §4 | - | CTX | motion | POS | NON | MOYENNE | STRUCTURE | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | N_A_HTML_VANILLA | (Framer) | NON | NON | N/A vanilla |
| R-124 | Never mix GSAP+Framer ou ThreeJS+Framer same tree. | soft §8 | - | CTX | motion | NEG | NON | CRITIQUE | STRUCTURE | PERF_CATA | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | N_A_HTML_VANILLA | (React) | NON | NON | N/A vanilla |
| R-125 | Avoid `h-screen`. ALWAYS `min-h-[100dvh]` (iOS Safari jump). | soft, taste, minimalist, brutalist | impeccable, a11y-fond-tier1 | UNIV | responsive | NEG | OUI | CRITIQUE | LAYOUT | PERF_CATA | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | OUI tier1 | NON | Déjà tier1 |
| R-126 | No complex flexbox math. Use CSS Grid. | soft (Grid > Flex-Math), taste | - | UNIV | layout | NEG | NON | MOYENNE | STRUCTURE | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | layout ref core | PARTIEL | NON | CSS pattern |
| R-127 | Never animate top/left/width/height. ONLY transform+opacity. | soft, taste, redesign, impeccable | vercel | UNIV | motion | NEG | OUI | CRITIQUE | LAYOUT | PERF_CATA | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | OUI partial | NON | Grepable |
| R-128 | Grain/noise filters ONLY fixed pseudo-elements (pointer-events-none). | soft §5, taste, minimalist | impeccable | UNIV | composition | NEG | NON | CRITIQUE | LAYOUT | PERF_CATA | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | CRITIQUE_TIER_2 | craft ref core | NON | NON | CSS pattern |
| R-129 | Semantic HTML mandatory (button/a/label, JAMAIS div onClick). | soft, redesign, vercel | a11y-fond-tier1 | UNIV | a11y | NEG | NON | CRITIQUE | STRUCTURE | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | GATE_PYTHON | phase4-finishing-gate.py | OUI tier1 | NON | Déjà tier1 |
| R-130 | Responsive images : srcset+sizes, picture art direction. | impeccable, vercel, soft | - | UNIV | responsive | POS | PARTIEL | CRITIQUE | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Détectable HTML |
| R-131 | Image width+height (CLS). Below-fold loading=lazy. Above-fold priority. | impeccable + vercel + redesign | - | UNIV | performance | POS | OUI | CRITIQUE | CHIRURGICAL | PERF_NORMAL | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Détectable HTML |
| R-132 | NO `transition: all`. List properties. | vercel, redesign | soft, impeccable | UNIV | motion | NEG | OUI | CRITIQUE | CHIRURGICAL | PERF_NORMAL | REGEX_TRIVIALE | SAFE_INTERDICTION | GATE_PYTHON | phase4-blacklist-gate.py | OUI partial | NON | Grepable |
| R-133 | Large lists (>50) : virtualize ou content-visibility:auto. | vercel §Performance | - | UNIV | performance | POS | PARTIEL | CRITIQUE | CHIRURGICAL | PERF_CATA | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Détectable CSS |
| R-134 | NO layout reads in render (getBoundingClientRect, offsetHeight). | vercel | - | CTX | performance | NEG | NON | CRITIQUE | STRUCTURE | PERF_CATA | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | CRITIQUE_TIER_2 | performance ref | NON | OUI | React-specific ? |
| R-135 | URL reflète state (filters, tabs, pagination en query params). | vercel | interaction, soft | CTX | interaction | POS | NON | CRITIQUE | STRUCTURE | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | PARTIEL | NON | React Router/nuqs |
| R-136 | touch-action: manipulation prevents double-tap zoom delay. | vercel | - | UNIV | responsive | POS | OUI | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_TRIVIALE | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | OUI tier1 | NON | Déjà tier1 |
| R-137 | -webkit-tap-highlight-color set intentionally. | vercel | - | UNIV | interaction | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | NON | NON | CSS minor polish |
| R-138 | overscroll-behavior: contain dans modals/drawers. | vercel | - | UNIV | responsive | POS | OUI | MOYENNE | CHIRURGICAL | PERF_NORMAL | REGEX_TRIVIALE | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Grepable CSS |
| R-139 | Intl.DateTimeFormat / NumberFormat (no static formats). | vercel §Locale_and_i18n | - | CTX | performance | POS | PARTIEL | MOYENNE | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | CRITIQUE_TIER_2 | i18n ref | NON | NON | React/JS |
| R-140 | Brand names : `translate="no"` pour éviter auto-translate. | vercel §Locale | - | UNIV | composition | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | content ref | NON | NON | i18n discipline |
| R-141 | Inputs avec value need onChange. Uncontrolled : defaultValue. Hydration. | vercel §Hydration | - | CTX | interaction | NEG | NON | CRITIQUE | STRUCTURE | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | N_A_HTML_VANILLA | (React) | NON | NON | N/A vanilla |
| R-142 | Icon buttons need aria-label. Icon-only links distinct text. | vercel + ux-writing | a11y-fond-tier1 | UNIV | a11y | NEG | NON | CRITIQUE | CHIRURGICAL | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | GATE_PYTHON | phase4-finishing-gate.py | OUI partial | NON | Grepable aria-label |
| R-143 | Active voice : "Install the CLI" not "The CLI will be installed". | vercel §Content_and_Copy | ux-writing | UNIV | copy | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Copy discipline |
| R-144 | Title Case (Chicago) headings/buttons. Numerals "8 deployments" not "eight". | vercel §Content_and_Copy | ux-writing | UNIV | copy | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Copy discipline |
| R-145 | Specific button labels ("Save API Key" not "Continue"). | vercel | ux-writing R-063 | UNIV | copy | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Doublon R-063 |
| R-146 | Errors : fix/next step, compassionate tone. | vercel | ux-writing R-064 | UNIV | copy | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | PARTIEL | NON | Doublon R-064 |
| R-147 | color-scheme: dark sur <html> dark themes. Fixes scrollbar/inputs. | vercel §Dark_Mode | impeccable | UNIV | color | POS | OUI | MOYENNE | CHIRURGICAL | PERF_NORMAL | REGEX_TRIVIALE | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Grepable CSS |
| R-148 | <meta name="theme-color"> matches page background. | vercel §Dark_Mode | - | UNIV | color | POS | OUI | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_TRIVIALE | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Grepable HTML meta |
| R-149 | No onPaste preventDefault. Let users paste. | vercel | interaction | UNIV | interaction | NEG | NON | CRITIQUE | STRUCTURE | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | CRITIQUE_TIER_2 | interaction ref core | NON | NON | UX anti-pattern |
| R-150 | Autocomplete on inputs (autocomplete="email"). | vercel | - | UNIV | interaction | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | NON | NON | HTML pattern |
| R-151 | Correct input types (email, tel, url, number) avec inputmode. | vercel | - | UNIV | interaction | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | NON | NON | HTML pattern |
| R-152 | Disable spellcheck emails/codes/usernames (spellCheck=false). | vercel | - | UNIV | interaction | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | NON | NON | HTML attribute |
| R-153 | Checkboxes/radios : label+control single hit target ≥44px. | vercel | interaction | UNIV | interaction | POS | NON | CRITIQUE | LAYOUT | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | HTML pattern |
| R-154 | Submit button enabled until request, spinner during. | vercel | interaction R-047 | UNIV | interaction | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | PARTIEL | NON | UX pattern |
| R-155 | Placeholders end with `…` + show example pattern. | vercel | ux-writing | UNIV | copy | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | NON | NON | Content polish |
| R-156 | autocomplete="off" non-auth fields (avoid password manager). | vercel | - | UNIV | interaction | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | NON | NON | HTML attribute |
| R-157 | Warn before navigation unsaved (beforeunload ou router guard). | vercel | interaction | CTX | interaction | POS | NON | MOYENNE | STRUCTURE | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | NON | NON | React Router |
| R-158 | Ellipsis `…` not `...`. Curly quotes. Non-breaking spaces (10&nbsp;MB). | vercel §Typography | redesign, ux-writing | UNIV | copy | POS | PARTIEL | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Grepable text |
| R-159 | No straight quotes html/JSON. Always entities/unicode. | (R-158) | - | UNIV | copy | POS | PARTIEL | POLISH | CHIRURGICAL | PERF_NORMAL | REGEX_FAUX_POSITIFS | SAFE_PRINCIPE | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Grepable mais context |
| R-160 | Text containers handle long content (truncate, line-clamp, break-words). | vercel §Content_Handling | redesign | UNIV | layout | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | layout ref core | PARTIEL | NON | CSS pattern |
| R-161 | Flex children need min-w-0 (text truncation). | vercel | - | UNIV | layout | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | layout ref core | NON | NON | CSS pattern |
| R-162 | Handle empty states (no broken UI for empty strings/arrays). | vercel | interaction R-047, redesign | UNIV | interaction | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | PARTIEL | NON | Code inspection |
| R-163 | Anticipate content range (short, average, very long). | vercel | - | UNIV | layout | POS | NON | MOYENNE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | layout ref core | NON | NON | Designer discipline |
| R-164 | preconnect CDN/asset domains. preload as=font + font-display:swap. | vercel §Performance | impeccable R-017 | UNIV | performance | POS | NON | CRITIQUE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | performance ref | PARTIEL | NON | HTML meta + font strategy |
| R-165 | Use uncontrolled inputs ; if controlled, must be cheap per keystroke. | vercel | - | CTX | performance | POS | NON | CRITIQUE | STRUCTURE | PERF_CATA | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | performance ref | NON | NON | React pattern |
| R-166 | Headings hierarchical h1-h6. Skip link main content. | vercel | interaction | UNIV | a11y | POS | NON | CRITIQUE | STRUCTURE | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Grepable HTML |
| R-167 | scroll-margin-top heading anchors (sticky nav overlap). | vercel | - | UNIV | responsive | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | responsive ref core | NON | NON | CSS pattern |
| R-168 | Inputs need name + meaningful autocomplete. | vercel | - | UNIV | interaction | POS | NON | MOYENNE | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | PARTIEL | NON | HTML pattern |
| R-169 | Async updates aria-live="polite". | vercel | - | UNIV | a11y | POS | NON | CRITIQUE | STRUCTURE | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | GATE_PYTHON | phase4-finishing-gate.py | NON | NON | Grepable HTML |
| R-170 | Never rely on hover for functionality (touch users). | impeccable + vercel | - | UNIV | interaction | NEG | NON | CRITIQUE | LAYOUT | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | CRITIQUE_TIER_2 | interaction ref core | NON | NON | UX cross-device |
| R-171 | Buttons/links ALWAYS have hover: state. | vercel | redesign, soft | UNIV | interaction | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | interaction ref core | PARTIEL | NON | CSS pattern |
| R-172 | Interactive states increase contrast (hover/active/focus > rest). | vercel | redesign, interaction | UNIV | interaction | POS | NON | CRITIQUE | LAYOUT | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | GATE_PYTHON | phase4-finishing-gate.py | PARTIEL | NON | Détectable contrast |
| R-173 | Second person ("you can install") not first ("we recommend"). | vercel | ux-writing | UNIV | copy | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | NON | NON | Copy discipline |
| R-174 | Use & over "and" space-constrained. | vercel | - | UNIV | copy | POS | NON | POLISH | CHIRURGICAL | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | ux-writing ref core | NON | NON | Copy discipline |
| R-175 | Design Variance Rule : vary section rhythm/layout/spacing/image ratio. No repetitive. | soft §1+§9, taste, images-taste | - | UNIV | composition | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | composition ref core | NON | OUI | Designer discipline soft ? |
| R-176 | Motion Intensity Scale (1-10) : 1-3 static, 4-7 fluid CSS, 8-10 cinematic. Calibrate to brief. | soft §6, taste | - | UNIV | motion | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | motion ref core | NON | NON | Brief decision |
| R-177 | Visual Density Scale (1-10) : 1-3 airy, 4-7 daily, 8-10 cockpit. | soft §6, taste | - | UNIV | composition | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | composition ref core | NON | NON | Brief decision |
| R-178 | Brutalist : no pure #000, no neon, no CRT scanlines unless THAT is the aesthetic. | brutalist-skill | - | UNIV | composition | NEG | NON | MOYENNE | LAYOUT | AI_SLOP | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | anti-slop-blacklist-core.md | PARTIEL | NON | Aesthetic-specific |
| R-179 | Image-first workflow : generate images BEFORE code. Code = translation. | images-taste-skill | - | UNIV | process | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | craft ref core | NON | NON | BIG-specific process |
| R-180 | Stitch DESIGN.md : encodes atmosphere/color/typo/components/motion/anti-patterns. | stitch-skill | - | CTX | process | POS | NON | CRITIQUE | STRUCTURE | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | N_A_HTML_VANILLA | (Stitch) | NON | NON | N/A |
| R-181 | Redesign audit 10-step priority order : fonts→colors→hover/active→layout→loading/empty/error→polish. | redesign-skill §Fix_Priority | - | UNIV | process | POS | NON | CRITIQUE | LAYOUT | PERF_NORMAL | SEMANTIQUE_VUE_ENSEMBLE | DANGER_PERFORM | CRITIQUE_TIER_2 | redesign ref core | PARTIEL | OUI | Redesign-specific |
| R-182 | Vercel Guidelines compliance : check all categories (a11y/forms/animation/typo/responsive/perf). | vercel | impeccable | UNIV | process | POS | NON | CRITIQUE | LAYOUT | WCAG_FAIL | SEMANTIQUE_VUE_ENSEMBLE | SAFE_INTERDICTION | CRITIQUE_TIER_2 | QA ref | PARTIEL | NON | Audit checklist |

---

## SECTION 3 — Candidates TIER 1 (12 candidats, max 9 promotions)

| Priorité | ID | Règle | Justification | Risque | Recommandation agent |
|---|---|---|---|---|---|
| 1 | R-003 | Teinter neutres légèrement vers brand hue | Foundation palette ; high impact ; low friction | NONE | **PROMOTE** |
| 2 | R-023 | 4pt spacing base ; scale 4,8,12,16... gap not margins | Root layer ; affects all layout | NONE | **PROMOTE** |
| 3 | R-010 | Modular 5-size type scale ; contrast 1.25+ | Déjà partiellement | risque inflexibilité — clause "ou contextual" | **PROMOTE avec clause** |
| 4 | R-100 | CSS moderne : oklch, @layer, @property, color-mix, clamp | Mandatory 2026 baseline | NONE | **PROMOTE** (déjà tier1, à formaliser) |
| 5 | R-004 | 60-30-10 visual weight | Déjà tier1 | DUPE | SKIP |
| 6 | R-096 | Data emphasis : numbers > labels. Tabular nums. | High-leverage dashboards | NONE | **PROMOTE** |
| 7 | R-094 | Restraint principle | Déjà tier1 | DUPE | SKIP |
| 8 | R-026 | Hierarchy 2-3 dimensions, NOT size alone | Déjà tier1 partiel | étendre core | SKIP (étendre core) |
| 9 | R-101 | Couche graphique : grain SVG + 3 radial gradients | Premium aesthetic | risque prescription lourde — clause "ou subtilement" | **PROMOTE avec clause** |
| 10 | R-099 | 1 accent color per concept max | Déjà finition-elite-core | NONE | **PROMOTE** (formaliser depuis core) |
| 11 | R-038 | prefers-reduced-motion | Déjà tier1 | DUPE | SKIP |
| 12 | R-002 | Réduire saturation extrêmes | Part of OKLCH workflow | "gradually" subjectif — heuristique 0.08-0.15 | **PROMOTE avec heuristique** |

**Résumé promotion TIER 1 :** 6-7 candidats viables, 4 doublons à skip. Total post-promotion : 22-23 (sous limite 25). ✅

---

## SECTION 4 — Ambiguïtés à trancher (14 règles)

| ID | Règle | Ambiguïté | Conseil agent |
|---|---|---|---|
| R-011 | Line-height inverse à line-length, +0.05-0.1 light-on-dark | Heuristic loupe-dependent | Reformuler : "Light-on-dark : +0.05-0.1 MIN, mesurer empiriquement" |
| R-016 | Single font + weights vs 2 fonts | "Genuine contrast" subjectif | Définir : "different structural category (serif/sans, width, era)" |
| R-039 | 80ms threshold = instant | Perceptual heuristic | Reclassifier PRINCIPLE → motion ref core (pas grepable) |
| R-041 | Optimistic UI low-stakes | "Low-stakes" non défini | Définir : "user can undo, cost of error <10s recovery" |
| R-062 | Test on real devices | Process pas codable | Reclassifier QA discipline → testing ref |
| R-069 | Plan expansion translation | i18n consideration pas design rule | Move i18n ref, INFORMATIONAL pas gated |
| R-078 | Shape design first, never jump to code | Process philosophical | Reclassifier PROCESS → craft ref |
| R-088 | Centered banned si DESIGN_VARIANCE>4 | "DESIGN_VARIANCE>4" comment coder ? | Option A : "DESIGN_VARIANCE>5" strict / Option B : "Asymmetric quand variance intended" soft |
| R-103 | Single font + weights > 2 fonts | Confusion R-016 | Splitter : R-016 = "when to pair", R-103 = "width/weight variety" |
| R-122 | Perpetual micro-interactions composants actifs | "Every active component" scope creep ? | Clarifier : "DATA-HEAVY components ONLY (dashboards, grids)" |
| R-134 | NO layout reads in render | React-specific ? | Move REACT_PERFORMANCE ref, mark N_A_HTML_VANILLA |
| R-175 | Design Variance Rule : vary rhythm | Discipline pas codable | Reclassifier PRINCIPLE + GUIDELINE → composition ref |
| R-181 | Redesign audit 10-step priority order | Redesign-specific méthodologie | Move redesign procedure (pas extraction main) |

---

## SECTION 5 — Déjà couvertes dans BIG (28 règles, à NE PAS ré-importer)

| ID | Règle | Présence BIG |
|---|---|---|
| R-004 | 60-30-10 visual weight | hierarchie-visuelle-tier1.md |
| R-005 | NO #000/#fff | finition-elite-tier1.md |
| R-006 | WCAG AA contraste | a11y-fondamentaux-tier1.md |
| R-020, R-061 | user-scalable=no | a11y-fondamentaux-tier1.md |
| R-021 | rem ≥16px body | a11y-fondamentaux-tier1.md |
| R-022, R-030 | Tap targets 44px | a11y-fondamentaux-tier1.md |
| R-036 | Animate transform+opacity only | finition-elite-core.md (motion) |
| R-038 | prefers-reduced-motion | a11y-fondamentaux-tier1.md |
| R-044 | outline:none + focus-visible | a11y-fondamentaux-tier1.md |
| R-081 | side-stripe borders | anti-slop-blacklist-tier1.md |
| R-082 | gradient text | anti-slop-blacklist-tier1.md |
| R-087, R-113 | 3-col equal cards (doublon) | anti-slop-blacklist-tier1.md |
| R-089 | 50/50 hero split | anti-slop-blacklist-tier1.md |
| R-090 | uniform icon+title+desc | anti-slop-blacklist-tier1.md |
| R-091 | link-column footers | anti-slop-blacklist-tier1.md |
| R-092 | carousels content | anti-slop-blacklist-tier1.md |
| R-093 | device frames | anti-slop-blacklist-tier1.md |
| R-094 | Restraint | hierarchie-visuelle-tier1.md |
| R-095 | 1 dominant + accompagnateurs | hierarchie-visuelle-tier1.md |
| R-099 | 1 accent color | finition-elite-core.md (à formaliser) |
| R-100 | CSS moderne | finition-elite-tier1.md |
| R-112 | NO oversized H1s | hierarchie-visuelle-tier1.md (implicite) |
| R-125 | min-h: 100dvh | a11y-fondamentaux-tier1.md |
| R-129 | Semantic HTML | a11y-fondamentaux-tier1.md |
| R-136 | touch-action: manipulation | a11y-fondamentaux-tier1.md |
| R-026 | Hierarchy 2-3 dimensions | hierarchie-visuelle-tier1.md (partiel) |
| R-027 | Card overuse | anti-slop-blacklist-tier1.md (partiel) |

---

## SECTION 6 — Synthèse et prochaines étapes

**Métriques :**
- 182 règles distinctes extraites
- 154 nouvelles à intégrer (84.6%)
- 28 déjà couvertes (15.4%)
- 14 ambiguïtés (7.7%)

**Destinations post-arbitrage :**
- TIER_1 : 6-7 promotions + 16 existants = 22-23 total (limite 25 ✅)
- GATE_PYTHON : ~48 règles regex-detectable
- CRITIQUE : ~78-82 règles sémantiques
- N_A_HTML_VANILLA : 12 règles React/Framer/Stitch only

**Prochaines étapes (Phase B) :**
1. Charles arbitre les 14 ambiguïtés
2. Charles valide les 6-7 promotions TIER 1 (1 par 1)
3. Charles confirme classification par lots de domaine
4. Implémentation Phase C

---

**Fin du livrable extraction.**
