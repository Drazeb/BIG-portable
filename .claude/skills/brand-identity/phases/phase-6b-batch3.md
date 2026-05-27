# Batch 3 — Prompts subagents (3 chapitres)

## Bloc de contexte partagé (injecté dans {batch3_shared_context})

## SPECS ARRÊTÉES (À RESPECTER EXACTEMENT)
### CSS Custom Properties
{extracted_css_variables}
### Polices Google Fonts
{extracted_fonts}

## CONTEXTE
Lis ces fichiers :
- {skill_dir}/ref/persona-and-rules.md
- {skill_dir}/ref/bible-design-strategie.md
- {skill_dir}/ref/master-style-guide.md (sections du chapitre concerné uniquement)
- {skill_dir}/examples/{example_level}/batch3-example.html (standard de qualité pour le Batch 3)

Et le style-tile source (pour comprendre l'univers visuel) :
- {style_tile_read_path}

## CONCEPT CHOISI (extrait du pitch)
{pitch_extract}

## RÉSUMÉ BATCH 2 (choix de design à maintenir pour la cohérence)
{batch2_design_summary}

## DIRECTION VISUELLE VALIDÉE
{visual_direction_extract}

## PROMPTS VISUELS EXISTANTS
{visual_brief_prompts}

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

{ventre_mou_section}

## CONTRAINTES TECHNIQUES
- Génère UNIQUEMENT le contenu HTML de ton chapitre (PAS de doctype, head, body, ou style global)
- Encapsule ton CSS dans un bloc `<style>` au début de ta sortie
- **Visuels finaux** : si une section "VISUELS FINAUX DISPONIBLES" t'est fournie, les images sont référencées par chemin relatif `visual-final/…` (JAMAIS en base64), les animations `.html` via `<iframe>`. Le fichier Batch 3 n'est alors plus 100 % self-contained — le dossier `visual-final/` est livré avec.
- Le résultat doit être visuellement riche — privilégie qualité et variété des techniques CSS
- **CSS Moderne** : socle de finition (oklch, @layer, @property, color-mix, text-wrap, clamp) + ≥2 techniques avancées parmi : `@property` animé, `clip-path`, `mask-image`, `@starting-style`, `backdrop-filter`, `mix-blend-mode`, `:has()`, `animation-timeline: view()`, `@container` — chaque technique doit SERVIR le design
- Qualité visuelle Showroom — digne d'un CEO

## RÈGLE SHOW > TELL
Chaque carte, bloc ou zone qui DÉCRIT un traitement visuel DOIT l'INCARNER en CSS.
- Si une carte dit "bleu-ardoise" → son background DOIT être bleu-ardoise
- Si deux cartes comparent "aéré" vs "compact" → les paddings et densités DOIVENT différer visiblement
- Si un élément illustratif est montré → le montrer EN CONTEXTE D'USAGE (posé sur un fond, à côté de texte, comme séparateur entre blocs), pas isolé sur fond vide
- Zéro carte "texte descriptif sur fond neutre" pour un concept visuel

## RÈGLES DE COHÉRENCE INTER-CHAPITRES
Les 3 chapitres sont générés séparément mais DOIVENT paraître issus du même designer. Respecte ces conventions :
- **Texte en français avec accents UTF-8** : utiliser les caractères accentués natifs (é, è, ê, à, ç, etc.), JAMAIS d'entités HTML (&eacute;), JAMAIS de texte sans accents
- **Overline de chapitre** : toujours en `color: var(--color-accent)` avec décorateurs linéaires `background: var(--color-accent)`
- **Nommage CSS** : préfixer toutes les classes avec `ch{numero}-` (ex: `.ch08-section`, `.ch09-section`). Convention BEM pour les éléments : `__label`, `__title`, `__desc`
- **Propriétés CSS** : utiliser les propriétés physiques standard (width, height, margin, padding) — PAS de propriétés logiques (inline-size, block-size)
- **Screenshot Test strict** : aucun terme technique CSS (oklch, rem, px) visible dans le texte rendu. Les labels de section (08.1, 09.3) sont légitimes.

## GATES DE VALIDATION
1. **Specs Lock** : Les CSS Custom Properties référencées sont-elles celles du :root fourni ?
2. **Completeness** : TOUTES les sous-sections du chapitre sont-elles présentes ?
3. **Screenshot Test** : Zéro donnée technique brute visible dans le rendu (pas de oklch, HEX, noms de fonts en texte courant) ?
4. **Cursor Coherence** : Le traitement CSS correspond au curseur A ?
5. **Zero Dead Code** : Chaque `@keyframes` déclaré DOIT être référencé dans une `animation`. Chaque `@property` déclaré DOIT être lu avec `var()` ET animé ou transitionné. Sinon = dead code = FAIL.
6. **Show > Tell** : Chaque texte qui décrit un traitement visuel est-il INCARNÉ par le CSS de son conteneur ? Zéro carte descriptive sur fond neutre.
7. **Anti-Patterns Datés** : Aucun pattern de la blacklist n'est présent ?
8. **Finition Élite** : Shadows ≥2 couches si utilisées, pas de `ease` générique, padding-block différenciés entre chapitres, hover ≥2 propriétés ?

## ⚠ AUTO-AUDIT ANTI-SLOP DE TON CHAPITRE (avant de finaliser)
Regarde TES sections dans leur ensemble et vérifie :
1. Squint test sur tes sections : la hiérarchie reste lisible yeux mi-clos ?
2. Une idée par sous-section (08.x / 09.x / 10.x) : pas deux propos empilés ?
3. Tes cards justifient leur existence : containment = vraie séparation, pas déco ?
4. Tes N sections ne sont pas N jumelles : poids/densités différenciés ?
5. Data-ink défendable : aucun élément graphique gratuit ?
6. Show > Tell : tout ce qui DÉCRIT un traitement l'INCARNE en CSS ; tout élément illustratif est montré EN CONTEXTE D'USAGE, jamais isolé sur fond vide.
7. Si une librairie « VISUELS FINAUX DISPONIBLES » t'est fournie : tu affiches les vraies images (chemin relatif), elles remplacent toute carte qui ne ferait que « décrire » une ambiance.
2+ écarts → corrige avant de rendre. (La cohérence des poids ENTRE chapitres est vérifiée par le gate — ne t'en occupe pas ici.)

---

## Chapitre 08 — Direction Photo

PROMPT SUBAGENT BATCH 3 — CHAPITRE 08 (DIRECTION NARRATIVE & PHOTOGRAPHIQUE):

Tu génères le CHAPITRE 08 du Batch 3 pour la marque {brand}.
Ce chapitre fait partie d'un fichier HTML plus large — tu génères UNIQUEMENT le contenu de ce chapitre.

{batch3_shared_context}

{visual_library_ch08}

## MISSION — CHAPITRE 08

**Garde-fou cohérence visuelle** : Si une direction visuelle a été validée (section DIRECTION VISUELLE ci-dessus), tu DOCUMENTES cette direction — tu ne la réinventes pas. Le moodboard (08.1), le color grading (08.2) et la scénographie (08.3) doivent refléter les choix déjà faits. **Si une section "VISUELS FINAUX DISPONIBLES" est présente ci-dessus, ces images sont la matière première du chapitre : tu les affiches réellement (`<img>`/`<iframe>` en chemin relatif), elles remplacent toute carte qui ne ferait que "décrire" une ambiance.** Si ni direction visuelle ni librairie ne sont fournies, tu en proposes une cohérente avec le concept et le style-tile.

Génère le HTML pour les 4 sections suivantes :

### 08.1 — Style Photographique
Moodboard. **Si des visuels `atmosphere` / `closeup` / `macro` sont fournis (section VISUELS FINAUX DISPONIBLES) → affiche-les ici en vrai (`<img src="visual-final/…">`) : c'est ÇA le moodboard, légendé par l'ambiance qu'il incarne.** Sinon : descriptions d'ambiances, angles, éclairages, incarnés en surfaces CSS. Surface EXPRESSIVE — utilise les techniques CSS du curseur A.

### 08.2 — Traitement Chromatique
Démonstration du color grading. **Si plusieurs niveaux d'intensité `atmosphere` sont fournis (uniforme → parchemin → doux → dramatique) → ils SONT la démonstration : affiche-les en série, du plus calme au plus contrasté, chacun légendé par son usage (sections content / CTA / vision…).** Sinon : avant/après, filtres (mix-blend-mode ou filter CSS). Les specs cards (ombres / tons moyens / hautes lumières) DOIVENT avoir un background-color ou gradient qui INCARNE la zone tonale décrite — pas de carte sur fond neutre.

### 08.3 — Scénographie Produit
Mockups de devices, mise en situation produit. **Si des visuels `hero` / `pov` ou une `animation` (.html) sont fournis → affiche-les ici en situation (l'animation dans un `<iframe src="visual-final/…animation.html" loading="lazy">` au ratio adapté, sans la modifier).**

### 08.4 — Signature de Prompting IA
Si des prompts visuels existent (section PROMPTS VISUELS EXISTANTS ci-dessus), reprends-les tels quels dans un code block stylé. Ajoute le label de l'outil recommandé (MidJourney ou Recraft).
Si aucun prompt n'est fourni, génère des prompts cohérents avec la direction visuelle du concept. Si le concept utilise de l'illustration flat/vector, ajouter un prompt Recraft en plus du prompt MJ (registres I1/I2/I7 → Recraft V4 Vector).

## CHECKLIST
[ ] 08.1 Style Photographique (moodboard)
[ ] 08.2 Traitement Chromatique (color grading)
[ ] 08.3 Scénographie Produit (mockups)
[ ] 08.4 Signature de Prompting IA

## FORMAT DE SORTIE
Écris le résultat dans : {skill_dir}/outputs/{session_dir}/.tmp-batch3-ch08.html
Le fichier contient : un bloc <style> avec le CSS du chapitre, puis le HTML des 4 sections.
Pas de doctype, pas de head, pas de body.

---

## Chapitre 09 — Composition

PROMPT SUBAGENT BATCH 3 — CHAPITRE 09 (SYSTÈME DE COMPOSITION & RYTHME):

Tu génères le CHAPITRE 09 du Batch 3 pour la marque {brand}.
Ce chapitre fait partie d'un fichier HTML plus large — tu génères UNIQUEMENT le contenu de ce chapitre.

{batch3_shared_context}

## MISSION — CHAPITRE 09
Génère le HTML pour les 4 sections suivantes :

### 09.1 — Architecture de Grilles
Visualisation des colonnes, gouttières, marges. Démonstration visuelle des grid-template-columns.

### 09.2 — Stratégie de Densité
Comparaison aéré vs compact. Deux versions côte à côte du même contenu.
La carte "aéré" DOIT avoir 3× plus de padding et moins de contenu. La carte "compact" DOIT être dense, serrée, avec des interlignes réduits. La DIFFÉRENCE doit être immédiate visuellement.

### 09.3 — Patterns de Mise en Page
Exemples Hero Split, Bento Grid, Feature Grid. Surface EXPRESSIVE — utilise les techniques CSS du curseur A.

### 09.4 — Rythme Vertical
Démonstration de l'espacement vertical (8px unit), des marges entre sections.

## CHECKLIST
[ ] 09.1 Architecture de Grilles
[ ] 09.2 Stratégie de Densité
[ ] 09.3 Patterns de Mise en Page
[ ] 09.4 Rythme Vertical

## FORMAT DE SORTIE
Écris le résultat dans : {skill_dir}/outputs/{session_dir}/.tmp-batch3-ch09.html
Le fichier contient : un bloc <style> avec le CSS du chapitre, puis le HTML des 4 sections.
Pas de doctype, pas de head, pas de body.

---

## Chapitre 10 — Illustration

PROMPT SUBAGENT BATCH 3 — CHAPITRE 10 (SYSTÈME D'ILLUSTRATION NARRATIVE):

Tu génères le CHAPITRE 10 du Batch 3 pour la marque {brand}.
Ce chapitre fait partie d'un fichier HTML plus large — tu génères UNIQUEMENT le contenu de ce chapitre.

{batch3_shared_context}

{visual_library_ch10}

## MISSION — CHAPITRE 10

**Garde-fou cohérence visuelle** : Si une direction visuelle a été validée et qu'elle inclut un registre illustratif (section DIRECTION VISUELLE ci-dessus), tu DOCUMENTES ce registre — tu ne le réinventes pas. **Si une section "VISUELS FINAUX DISPONIBLES" (schémas) est présente ci-dessus, affiche ces schémas EN CONTEXTE D'USAGE dans les sections pertinentes (10.2 Physique de l'illustration, 10.4 Lois de composition) — posés sur un fond, à côté de texte, comme illustration d'un propos ; jamais isolés sur fond vide.** Si aucune direction visuelle n'est fournie, tu en proposes une cohérente avec le concept et le style-tile.

Génère le HTML pour les 5 sections suivantes :

### 10.1 — Angle de Métaphore
La métaphore visuelle centrale expliquée visuellement.

### 10.2 — Physique de l'Illustration
Contours, remplissages, textures démontrés. Surface EXPRESSIVE — utilise les techniques CSS du curseur A.

### 10.3 — Character Design
Si personnages, style et proportions. Sinon, montrer les éléments récurrents du langage illustratif.
Chaque élément doit être montré EN CONTEXTE D'USAGE : la forme récurrente posée sur un fond texturé ou comme arrière-plan derrière du texte, l'élément décoratif comme séparateur entre blocs — pas d'éléments flottants isolés sur fond vide.

### 10.4 — Lois de Composition
Cohabitation illustration/texte/CTA — démonstration de placement.

### 10.5 — Directives de Prompting IA
Si des prompts visuels existent pour l'illustration (section PROMPTS VISUELS EXISTANTS ci-dessus), reprends-les tels quels dans un code block stylé. Ajoute le label de l'outil recommandé (MidJourney ou Recraft).
Si aucun prompt n'est fourni, génère des prompts cohérents avec le style illustratif du concept. Inclure un prompt MJ ET un prompt Recraft si le style est flat/vector (registres I1/I2/I7 → Recraft V4 Vector). Préciser l'outil recommandé pour chaque type de visuel.

### Footer (colophon)
Après la dernière section, ajoute un footer/colophon sobre affichant :
`Narration & Espace — {chosen_concept_name}`
Style cohérent avec le reste du fichier (même palette, même typographie).

## CHECKLIST
[ ] 10.1 Angle de Métaphore
[ ] 10.2 Physique de l'Illustration
[ ] 10.3 Character Design
[ ] 10.4 Lois de Composition
[ ] 10.5 Directives de Prompting IA
[ ] Footer / colophon

## FORMAT DE SORTIE
Écris le résultat dans : {skill_dir}/outputs/{session_dir}/.tmp-batch3-ch10.html
Le fichier contient : un bloc <style> avec le CSS du chapitre, puis le HTML des 5 sections.
Pas de doctype, pas de head, pas de body.
