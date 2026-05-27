# REX — Session d'optimisation BIG (2-4 avril 2026)

Session 3 sur le chantier visuels/style-tiles. Suite directe des sessions 30 mars - 1er avril (Axes 1-3 visuels) et 1-2 avril (CSS/composition/layout).

---

## CONTEXTE DE DÉPART

Score estimé avant session : ~7.5-8/10. Cible : 9-10/10 (niveau Awards).

### Ce qui avait été fait (sessions précédentes)
- Axe 1 (qualité visuels) : penseur visuel, skill `/visual-brief`, règles visibilité images
- Axe 2 (CSS/composition) : prompt Phase 4 renforcé (typo ≥8vw, fonds texturés, dialogue texte/image)
- Axe 3 (layout/taille) : 2 nouveaux squelettes CSS (VB-9 Stacked, VB-10 Full-bleed overlay), 6 exemples HTML refaits avec images
- Orchestration : swap 3C↔3B-5 (visuels AVANT pitch), Awards étalons injectables
- Outils : skill `/audit-elite` créé
- Audit de 88 sites Awards avec stats de layout

---

## CE QUI A ÉTÉ FAIT DANS CETTE SESSION

### 1. Prescriptions de sensation Phase 3B (radius, relief, conteneurs)

**Problème identifié** : Le même pitch ("Le Pouls Profond", A=3) produisait des radius de 2px dans un run et de 999px (pills) dans un autre. Cause : le pitch ne prescrivait rien sur le radius, les ombres, ni le traitement des conteneurs. Phase 4 improvisait.

**Solution** : Ajout de 5 sous-sections obligatoires dans la section "Prescriptions d'exécution visuelle" du prompt Phase 3B design (`phases/phase-3b-design.md`). Le designer produit maintenant des paragraphes titrés pour :
- Registre de surface (existait déjà)
- Géométrie des formes (NOUVEAU → radius)
- Relief et profondeur (NOUVEAU → shadows)
- Traitement des conteneurs (NOUVEAU → cards/containers)
- Rythme spatial (existait déjà)

**Format** : sensation + micro-justification concept/territoire. Pas de CSS, pas de menu d'options (risque de contamination/biais de primauté). Le designer dérive librement du concept.

**Résultat testé** : le pitch produit maintenant "Radius : minimaux tendant vers zéro — la précision de l'instrument chirurgical" et "Élévation : quasi-plate avec des émergences ponctuelles". Les deux runs convergent.

**Commit** : `ada0f22`

### 2. Test sans exemples HTML

**Hypothèse** : les exemples HTML en Phase 4 sont peut-être devenus inutiles vu qu'on a enrichi le prompt, les CSS skeletons, les étalons Awards, etc.

**Test** : suppression temporaire de toutes les références aux exemples dans Phase 4 (`phase-4-styletile.md` + `SKILL.md`). Run A=3 VoltaPilot.

**Résultat** : ~7/10 sans exemples vs ~8/10 avec. Delta de ~1 point en richesse technique :
- Moins de @property animées (1 vs 3)
- Pas de :has() (0 vs 2)
- Pas de @container (0 vs 1)
- Mais animation-timeline: view() trouvé autonomement (3 instances)
- Un radius-touch: 20px qui dépassait la prescription du pitch

**Analyse contamination avec exemples** : la contamination créative est quasi-nulle (fonts, palette, layout, artefact type → tout suit le pitch). La contamination technique est faible (easing curves identiques, pattern CTA ::before copié). Les prescriptions de sensation ajoutées (radius, relief) tiennent bien face à l'exemple.

**Décision** : rollback → on garde les exemples pour le +1 point de richesse technique. La contamination créative est suffisamment contrôlée.

**Commits** : `c6f8e1b` (suppression) → `9c0900f` (rollback)

### 3. Transmission stricte des préférences esthétiques

**Problème** : l'orchestrateur passait les noms d'inspirations esthétiques ("Blueprint", "Futuristic Surrealism") en texte libre dans le prompt des subagents, même quand l'utilisateur avait dit "aucune inspiration". Résultat : 2/3 concepts contaminés par Blueprint.

**Solution** : ajout de la "RÈGLE DE TRANSMISSION STRICTE" — l'orchestrateur ne transmet QUE la variable `{preference_concept_N}`, jamais de texte libre ajouté. Appliqué au designer Phase 3B et au penseur visuel Phase 3B-5.

**Commit** : `64cb960`

### 4. Divergence séquentielle pour les directions visuelles (Phase 3B-5)

**Nouveau système** : même pattern que les palettes (Vague 2bis). Pour chaque concept, 3 vagues A→B→C produisent 3 directions visuelles divergentes :
- Vague A : libre (dérivation la plus directe)
- Vague B : diverge sur la **famille visuelle** (type × registre)
- Vague C : diverge sur l'**univers de sujets** (les objets/scènes/matières)

L'utilisateur choisit 1 direction par concept. Les variantes sont archivées (pas supprimées) pour permettre un switch après feedback Recraft.

**Axes de divergence** : 2 axes forts, pas 3 faibles. L'ancre stylistique (lumière, grain) n'est PAS un axe de divergence (trop faible visuellement).

**Ancrage concept obligatoire** : les directives B et C incluent une règle "ANCRAGE CONCEPT OBLIGATOIRE" — les sujets divergent mais restent dans la métaphore du concept. Ajouté après un test où C3 dérivait vers des coupes géologiques sans rapport avec le concept de précipitation chimique.

**Enchaînement automatique** : les 3 vagues s'enchaînent SANS pause ni confirmation entre elles (feedback utilisateur — il voyait une pause entre A et B qui n'avait pas de sens).

**Injection dans les spécimens** : les 3 directions visuelles sont injectées dans le HTML du spécimen (panneau fixe à droite) AVANT de demander le choix à l'utilisateur, pour qu'il puisse comparer visuellement.

**Archivage des variantes palettes** : le même principe a été appliqué aux palettes — les variantes `-a.md`, `-b.md`, `-c.md` ne sont plus supprimées après le choix.

**Commits** : `8748d6b`, `3394f83`, `6d96588`, `75592d2`, `5e81c71`

### 5. Intention créative dans les HTML de choix

**Ajout** : l'intention créative (2-3 phrases condensées) est maintenant affichée dans les 3 documents HTML de choix :
- **Spécimen** : encart en haut à gauche (largeur limitée pour ne pas chevaucher le panneau de directions visuelles)
- **Palette comparison** : encart au-dessus de chaque concept-row (avant les 3 palettes)
- **Font recap** : encart en haut de chaque colonne concept

Permet à l'utilisateur de reconnecter ses choix visuels avec le concept narratif.

Le champ `intentionCreative` est optionnel dans les configs JSON — rétrocompatible.

**Commit** : `c88cfc6`

### 6. Option "Fond CSS/SVG seul" (pas de visuel généré)

**Problème** : depuis la dissociation du penseur visuel du designer Phase 3B, l'option "aucun visuel" avait disparu. Le penseur visuel, en tant que subagent dédié aux visuels, proposait toujours une image.

**Solution** : clarification des options à l'étape 1 du penseur visuel. Le fond CSS/SVG est TOUJOURS présent (socle). La question est : "faut-il une image PAR-DESSUS ?" L'option "Fond CSS/SVG seul" est maintenant présentée comme un choix créatif fort pour les concepts fondés sur le silence, la soustraction, le vide intentionnel.

**Commit** : `1dcd166`, `6e1b843`

### 7. Mode fond dominant ≠ exclusif

**Problème** : le pitch designer interprétait "Mode fond dominant : CLAIR" comme "tout doit être clair". Résultat : style-tiles entièrement clairs sans aucune section sombre, zéro contraste.

**Solution** : ajout de la "RÈGLE DE CONTRASTE INTRA-CONCEPT" dans `phase-3b-design.md`. "Dominant CLAIR" signifie majorité claire, mais l'Atmosphere Block PEUT (et pour A≥2, DEVRAIT) utiliser une inversion sombre.

**Commit** : `0405227`

---

## DÉCOUVERTES ET LEÇONS APPRISES

### Découverte 1 — Les prescriptions de sensation convergent, le CSS libre diverge
Quand le pitch prescrit une sensation ("radius minimaux, précision chirurgicale"), Phase 4 converge entre les runs. Quand le pitch ne dit rien, Phase 4 improvise différemment à chaque run. C'est prouvé par le test radius (2px vs 999px → 0-3px stable après prescription).

### Découverte 2 — Les exemples ajoutent ~1 point mais ne contaminent plus créativement
Les prescriptions de sensation (radius, relief, conteneurs) ont rendu le pitch suffisamment fort pour que Phase 4 suive le pitch sur ces dimensions, pas l'exemple. La contamination résiduelle est technique (easing curves, pattern CTA) et invisible visuellement.

### Découverte 3 — Le curseur A ne doit PAS prescrire de layout
Le calibrage par curseur A (A=1/A=2/A=3) ne devrait influencer que l'INTENSITÉ du traitement (composition, audace). Le layout (split, stacked, full-bleed) vient du pitch. Quand on force A=2 sur un pitch A=3, le subagent ne devrait PAS changer le layout — mais il le fait parfois par réflexe. Constaté lors du test A=2 forcé sur VoltaPilot.

### Découverte 4 — L'orchestrateur ajoute du texte libre malgré les règles
Le LLM orchestrateur a un biais d'helpfulness : même quand la règle dit "transmets UNIQUEMENT la variable", il ajoute des notes contextuelles ("le client a mentionné Blueprint mais ne veut pas l'utiliser"). La solution est de rendre la règle STRUCTURELLE, pas juste comportementale.

### Découverte 5 — Un subagent dédié ne propose jamais de s'annuler
Le penseur visuel, en tant que subagent dont la mission EST de prescrire des visuels, ne proposera jamais "pas de visuel". Pour qu'il le fasse, l'option doit être explicitement listée à parité avec les autres.

### Découverte 6 — "Dominant" est interprété comme "exclusif"
Le mot "dominant" dans "Mode fond dominant : CLAIR" est interprété littéralement par le LLM comme "tout est clair". Il faut expliciter que dominant ≠ exclusif.

---

## PROBLÈME MAJEUR IDENTIFIÉ : PATTERNS CSS DATÉS

### Le problème

Le LLM génère des patterns CSS qui étaient créatifs en 2015-2020 mais sont considérés datés/cheap en 2024-2026. Exemples constatés :
- **Dents de scie / wave dividers** entre les sections (clip-path polygon jagged)
- **Card hover lift** (`:hover { transform: translateY(-2px) }`)
- **Neon glow** sur les boutons et textes (box-shadow multicolore type synthwave)
- **Pulsing infini** sur les indicateurs de statut

### Audit des exemples HTML

**4 exemples sur 6 contiennent des `:hover translateY`** — le pattern le plus interdit par nos propres règles (Gate 10 du prompt Phase 4 l'interdit explicitement pour A≥2). Le système est INCOHÉRENT : les règles disent non, les exemples montrent oui. Le pattern "Code > Rules" fait que le subagent suit l'exemple.

| Exemple | Problème | Risque |
|---------|---------|-------|
| A (A=1) | `:hover translateY(-2px)` CTA | CRITIQUE |
| F (A=1) | `:hover translateY(-1px) scale(1.01)` | CRITIQUE |
| C (A=3) | `:hover translateY(-3px) scale(1.02)` | CRITIQUE |
| D (A=3) | `:hover translateY(-2px)` + glow néon | CRITIQUE |
| D (A=3) | Waveform divider (vague SVG entre sections) | MODÉRÉ |
| D (A=3) | Esthétique néon/glow omniprésente (variables `--shadow-glow-*`) | MODÉRÉ |
| A/B | `live-pulse` animation infinie sur indicateurs | FAIBLE |

**Ce qui est PROPRE** : les CSS skeletons (`css-patterns-phase4.md`), les techniques modernes (oklch, @property, :has(), mask-image, @starting-style), les prompts Phase 4 et Phase 3B (règles correctes).

### Cause racine

Le LLM est entraîné sur du web 2015-2024. Ses réflexes CSS "créatifs" sont biaisés vers les patterns les plus fréquents dans ses données, qui sont souvent ceux de 2016-2020 (leur volume domine). Il confond "j'ai vu ça souvent" avec "c'est moderne".

### Capacité du LLM à distinguer daté vs moderne

**Peut identifier les patterns DATÉS** : oui, parce que le consensus critique existe dans ses données d'entraînement (articles "stop using X in 2023", etc.)

**Ne peut PAS identifier ce qui est cutting-edge 2025-2026** : son biais statistique pousse vers les patterns les plus fréquents, pas les plus récents. Risque de considérer comme "moderne" des trucs qui datent déjà.

**Méthode fiable pour cartographier** :
1. **Blacklist (ce qui est daté)** : le LLM peut la construire (consensus critique dans ses données). Sources : observations utilisateur + audit Awards + connaissances LLM.
2. **Whitelist (ce qui est moderne)** : nécessite des données fraîches. Sources : captures de sites Awards récents + observations utilisateur. Le LLM seul ne suffit pas.

---

## MISSION POUR LA PROCHAINE SESSION

### Priorité 1 : Décontamination des 6 exemples HTML

Nettoyer les 4 fichiers contaminés :
- Remplacer TOUS les `:hover translateY` par des alternatives modernes (changement de couleur + ombre + opacité)
- Exemple D : retirer le waveform divider, modérer l'esthétique néon/glow
- Exemples A/B : remplacer le pulsing infini par un indicateur statique

**Approche recommandée** : même méthodologie que la session 1-2 avril — faire recoder les heroes par des subagents Phase 4 qui produisent du CSS cohérent d'un seul tenant (ne PAS modifier par regex, ça dégrade systématiquement).

### Priorité 2 : Construire la blacklist de patterns datés

Ajouter dans le prompt Phase 4 une section "ANTI-PATTERNS DATÉS" avec 8-10 patterns concrets :
- Wave/zigzag section dividers
- Card/button hover translateY lift
- Neon glow text/button effects (synthwave aesthetic)
- Infinite pulsing animations
- Parallax scroll backgrounds
- Diagonal clip-path section transitions
- Bouncing/rotating elements on hover
- Over-engineered hamburger animations

### Priorité 3 : Recadrer A=3 "convention cassée"

Le calibrage A=3 dit "au moins une convention de layout cassée". Le subagent interprète ça comme "ajouter du décor non-conventionnel" (wave dividers, clip-path décoratifs). Il faut recadrer : convention cassée = la STRUCTURE est non-conventionnelle (chevauchement, overflow, hiérarchie inversée), pas le DÉCOR (dividers fantaisie, bordures, effets).

### Priorité 4 (si temps) : Whitelist de patterns modernes

Idéalement, fournir 5-10 captures de sites Awards récents (2024-2025) et en extraire les patterns CSS actuels. C'est la source la plus fiable pour la whitelist, plus que les connaissances du LLM.

---

## FICHIERS MODIFIÉS (exhaustif)

| Fichier | Modification | Commit |
|---------|-------------|--------|
| `phases/phase-3b-design.md` | +5 sous-sections prescriptions sensation + règle contraste intra-concept | `ada0f22`, `0405227` |
| `phases/phase-3b-penseur-visuel.md` | +placeholder divergence + option "fond CSS/SVG seul" | `8748d6b`, `6e1b843` |
| `phases/phase-4-styletile.md` | Test suppression exemples (rollback) | `c6f8e1b` → `9c0900f` |
| `SKILL.md` | Divergence séquentielle visuels A→B→C + transmission stricte esthétique + injection spécimen + archivage variantes palettes + intention créative dans configs | `64cb960`, `8748d6b`, `3394f83`, `6d96588`, `75592d2`, `5e81c71`, `c88cfc6` |
| `lib/font-palette-specimen.mjs` | +bloc intentionCreative conditionnel | `c88cfc6` |
| `lib/palette-comparison.mjs` | +bloc intentionCreative par concept-row | `c88cfc6` |

---

## ÉTAT DU SYSTÈME APRÈS CETTE SESSION

- **Phase 3B design** : prescriptions de sensation complètes (radius, relief, conteneurs), mode fond dominant clarifié
- **Phase 3B-5 penseur visuel** : divergence séquentielle A→B→C, option "sans visuel", ancrage concept obligatoire
- **Phase 4** : inchangée (les règles sont correctes, le problème est dans les exemples)
- **Exemples HTML** : CONTAMINÉS — à nettoyer en priorité (prochaine session)
- **HTML de choix** : intention créative ajoutée dans spécimen, palette comparison, font recap
- **Palettes** : variantes archivées au lieu d'être supprimées

## Dernière mise à jour : 2026-04-04
