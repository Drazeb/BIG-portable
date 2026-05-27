# REX — Session modernisation CSS + composition BIG (4-8 avril 2026)

Session de 4 jours sur la modernisation des style-tiles générés par BIG. Objectif : éliminer les patterns datés (2015-2020) et pousser vers un niveau élite (Awards 2024-2026).

---

## LE PROBLÈME DE DÉPART

Les style-tiles générés par Phase 4 de BIG utilisaient des patterns CSS et de composition datés :
- Hover `translateY(-2px)` sur les boutons (cliché SaaS 2017)
- Animations infinies décoratives (pulse, breathe, drift)
- Glow shadows (`box-shadow: 0 0 Npx` sans offset)
- Wave/zigzag dividers entre les sections
- Staggered fade-up (`@keyframes` translateY + opacity + delays échelonnés)
- Artefacts en grilles uniformes (`repeat(N, 1fr)` avec N cards identiques)
- CTA avec flèche → systématique

**Cause racine identifiée** : pattern "Code > Rules" — le LLM suit ce qu'il VOIT dans les exemples HTML plus que les règles textuelles du prompt. Les exemples contenaient tous ces patterns datés.

---

## CE QUI A ÉTÉ FAIT (tout commité sur main)

### 1. Blacklist CSS dans Phase 4 (FAIT)
**Fichier** : `phases/phase-4-styletile.md`, section "ANTI-PATTERNS DATÉS — BLACKLIST"
- 6 familles, ~25 patterns techniques interdits
- Hovers datés (translateY, scale > 1.02, arrow slide, underline scaleX, letter-spacing)
- Animations infinies décoratives
- Séparateurs fantaisie (waves, zigzag, gradient lines)
- Effets visuels datés (glow shadows, text-shadow glow, scan lines, neumorphism, glassmorphism lourd)
- Staggered fade-up manuels → remplacés par @starting-style
- Transversal : s'applique à TOUS les curseurs A (A=1, A=2, A=3)

### 2. Blacklist composition dans Phase 4 (FAIT)
**Fichier** : `phases/phase-4-styletile.md`, section "Compositions datées"
9 items non-ambigus (confirmés par 3 sources : connaissance native + Perplexity + benchmark 21 sites Awards) :
1. Hero split 50/50 rigide par défaut
2. Grille de N conteneurs identiques (même taille, même structure)
3. Alternance zigzag texte/image
4. Pricing en colonnes middle highlighted
5. "How it works" 3 étapes avec icônes
6. Mega-footer sitemap
7. Device mockup dans le hero
8. Carousel/slider
9. Cards icône ronde + titre + description

### 3. 8 principes de hiérarchie visuelle dans Phase 4 (FAIT)
**Fichier** : `phases/phase-4-styletile.md`, section "PRINCIPES DE HIÉRARCHIE VISUELLE"
1. Données clés en typographie display (pas en body text)
2. Taille proportionnelle à l'importance (un élément domine)
3. Séparation par changement de fond, pas par bordures 1px
4. Statuts en badges textuels, pas en jauges/barres
5. Variation dramatique de densité (zones aérées + zones compactes)
6. Hiérarchie 3 couches (dominant > support > détails)
7. Max 1 graphique par composant
8. Accent couleur sur des zones entières, pas dispersé

### 4. Gate mécanique CSS (FAIT)
**Fichier** : `scripts/phase4-blacklist-gate.py` (342 lignes, 11 checks)
- Détecte mécaniquement : translateY hover, arrow slide, scale excessive, animations infinies, glow shadows, text-shadow glow, zigzag clip-path (>6 points), staggered fadeup, backdrop-blur excessif, letter-spacing hover, underline scaleX
- Intégré dans l'étape 4A-ter du SKILL.md (les subagents contrôleurs lancent ce script + le finishing gate)
- Si FAIL → renvoi au subagent Phase 4 pour correction (max 2 itérations)

### 5. Clarification A=3 dans Phase 4 ET Phase 3B (FAIT)
"Convention cassée" = DISPOSITION modifiée (un élément existant repositionné), pas DÉCORATION ajoutée (un ornement plaqué sur un layout standard).

### 6. Corrections squelettes CSS (FAIT)
**Fichier** : `ref/css-patterns-phase4.md`
- VB-3 : glow → shadow offset
- VB-4 : glow → shadow offset, blur 40→12px
- VB-8 : letter-spacing hover retiré
- VB-10 : glow → shadow offset
- AT-3 : animation infinite retirée, ease-in-out corrigé

### 7. 6 exemples HTML décontaminés CSS (FAIT)
Tous les patterns CSS datés retirés des 6 exemples (A, B, C, D, E, F). Remplacés par @starting-style, hover multi-property, ombres offset. 2 passes de nettoyage (la 1ère avait laissé des résidus que le gate a attrapés).

### 8. 6 exemples artefacts refondus (FAIT)
Les artefacts tables/grilles uniformes remplacés par des composants exotiques avec hiérarchie 3 couches :
- A : Fiche diagnostic IoT (score 87/100 dominant + 4 capteurs + maintenance)
- B : Carnet de dégustation (note 94 dominant + profil sensoriel + provenance)
- C : Journal de chantier (73% dominant + métriques terrain + annotation)
- D : Fiche de résidence artistique (J-14 dominant + artiste + note curateur)
- E : Bulletin météo (18.4°C dominant + 4 relevés + meta station)
- F : Fiche analyse de sol (7.2 dominant + paramètres + recommandation)

### 9. Flèches CTA retirées des exemples (FAIT)
4/6 exemples avaient des → dans les CTA hero. Retiré pour éviter la contamination systématique.

### 10. 7 contradictions internes corrigées (FAIT)
Identifiées par un audit de cohérence (10 checks par paire de fichiers) :
- 3 squelettes CSS avec patterns blacklistés (AT-3, VB-8, VB-10)
- html-showroom-spec avec blur(20px) → corrigé en blur(10px)
- Example D gradient divider résiduel → retiré
- Phase 3B translateY "toléré pour A=1" → aligné "interdit pour tous"
- Phase 4 résidu "Pour A=3, au moins 4" → retiré (doublon)

### 11. Règles Phase 3B ajoutées (FAIT)
- Radius polarisé (en sensation : "prend parti, angulaire OU arrondi, pas de milieu uniforme")
- Prescription artefact renforcée ("décrire les éléments structurels et leur hiérarchie, pas juste le type")
- Statement typographique final ("l'atmosphere se conclut par une affirmation de marque")
- Ombres ponctuelles (reformulé de "systématique" à "1-2 éléments clés")
- Palette restreinte (accent = événement rare, 1-2 éléments par viewport)

---

## RECHERCHE EFFECTUÉE (données disponibles)

### Audit de 24 style-tiles BIG
**Résultat** : 21% daté, 50% correct, 29% moderne/élite
**Découverte clé** : les 3 élites (VoltaPilot monitoring, Vermeil almanach, Vermeil fiche parcelle) avaient un pitch Phase 3B très spécifique structurellement. Les datés avaient un pitch générique ("timeline", "dashboard").
**Captures** : `outputs/audit-artifacts-20260405/` (24 captures hero + full + artifact)

### Benchmark 21 sites Awards
**Captures** : `outputs/benchmark-awards-20260407/` (hero + full de 21 sites)
**Analyses** : 3 agents macro (layout, structure) + 3 agents micro (ombres, radius, bordures, surfaces, cards, typo, densité, couleur) + 1 agent CSS (grain, shadows dans le code source)
**Résultats macro** : full-bleed hero dominant, alternance tonale sombre/clair, typo display comme architecture, statement final, 3ème couche atmosphérique, whitespace radical
**Résultats micro** : ombres ponctuelles (pas systématiques), radius polarisé (sharp OU pilule), séparation par fond (pas bordures), grain présent mais subtil (4/19 confirmé par CSS — image webp, pas feTurbulence), palette 2-3 couleurs max

### 2 rapports Perplexity
**Fichiers** : `ref/perplexity-composition-patterns-report.md` + `ref/perplexity-composition-detail-report.md`
**Contenu** : patterns datés vs actuels (heroes, composants, sections, footers, interactions), détail opérationnel (hovers, footers, composants UI, transitions, spacing)
**Conflit identifié** : Perplexity dit translateY 2-4px sur cards = encore OK. Notre blacklist l'interdit. Le benchmark Awards confirme notre blacklist (0/21 sites utilisent translateY hover).

### Blacklist composition draft
**Fichier** : `ref/composition-blacklist-draft.md`
13 items initiaux, réduits à 9 après croisement Awards. Les 9 validés sont implémentés. Les 4 retirés : logo wall gris (encore utilisé), CTA flèche (encore utilisé mais retiré des exemples par précaution), guillemets géants (données insuffisantes), illustrations isométriques (pas pertinent pour les style-tiles).

---

## OÙ ON EN EST — LE PROBLÈME RESTANT

### Le problème
Malgré toutes les règles (blacklists + principes + exemples refondus + gate mécanique), les artefacts générés retombent sur des grilles `repeat(5, 1fr)` avec bordures. Le dernier test Camille (20260408-0011) montre : hero moderne ✅, atmosphere moderne ✅, artefact daté ❌.

### La cause racine identifiée
**Pitch > Exemples > Principes.** Quand le pitch Phase 3B dit "5 étapes de dosage", le subagent Phase 4 fait 5 colonnes identiques — même si l'exemple montre une hiérarchie, même si les principes disent "un élément dominant". Le contenu concret du pitch écrase tout.

### Ce qui manque — L'ACTION SUIVANTE
**Phase 3B ne connaît pas les blacklists ni les principes de hiérarchie de Phase 4.**

Le designer 3B prescrit la composition du hero, de l'artefact et de l'atmosphere SANS savoir que :
- "Grille de N conteneurs identiques" est blacklisté en Phase 4
- "Hiérarchie 3 couches avec un élément dominant" est prescrit en Phase 4
- "Séparation par fond, pas par bordures" est prescrit en Phase 4

Résultat : le pitch pousse Phase 4 vers exactement ce qu'on lui interdit.

**La solution** : injecter dans `phases/phase-3b-design.md` une version SENSATION (pas CSS) de :
1. La blacklist composition (en langage 3B — pas de termes CSS, pas d'exemples concrets contaminants)
2. Les principes de hiérarchie (en langage 3B — "un élément dominant, pas N éléments de même importance")

C'est ~10-12 lignes à ajouter dans la section "STRATÉGIE D'ARTEFACT" et éventuellement "STRATÉGIE DE COMPOSITION" de Phase 3B. Le gate CSS `phase3b-css-gate.py` ne bloquera pas ça (c'est du langage sensation).

---

## FICHIERS CLÉS À LIRE

| Fichier | Pourquoi le lire |
|---------|-----------------|
| `phases/phase-3b-design.md` | Le prompt du designer — c'est LÀ qu'il faut ajouter les règles |
| `phases/phase-4-styletile.md` | Le prompt du codeur — contient les blacklists + principes que 3B doit connaître |
| `ref/css-patterns-phase4.md` | Les squelettes CSS — déjà nettoyés |
| `scripts/phase4-blacklist-gate.py` | Le gate mécanique — déjà en place |
| `examples/*/style-tile-example-*.html` | Les 6 exemples refondus — déjà nettoyés |

### Fichiers de recherche (consultation)
| Fichier | Contenu |
|---------|---------|
| `ref/perplexity-composition-patterns-report.md` | Rapport 1 : patterns datés vs actuels |
| `ref/perplexity-composition-detail-report.md` | Rapport 2 : détail opérationnel |
| `ref/composition-blacklist-draft.md` | Draft blacklist composition (13 items, 9 validés) |
| `outputs/benchmark-awards-20260407/` | Captures Puppeteer de 21 sites Awards |
| `outputs/audit-artifacts-20260405/` | Captures des 24 style-tiles BIG analysés |
| `outputs/audit-examples-refonte-20260407/` | Captures des 6 exemples après refonte |

### Mémoire projet
| Fichier | Contenu |
|---------|---------|
| Mémoire projet `project_css_composition_modernization_plan.md` | Plan complet avec tout l'historique |

---

## DÉCOUVERTES FONDAMENTALES DE CETTE SESSION

1. **Code > Rules** : le LLM suit les exemples plus que les règles textuelles. Pour changer le comportement → changer les exemples.
2. **Pitch > Exemples > Principes** : quand le pitch dit "5 étapes", le subagent fait 5 colonnes même si l'exemple montre une hiérarchie. Le contenu concret prime.
3. **Le LLM invente mieux quand il n'a pas de template** : les artefacts les plus élites venaient de pitchs avec des noms spécifiques ("almanach de récolte") pour lesquels le LLM n'avait pas de template par défaut.
4. **Les agents sur-classifient** : dans les analyses (Awards, artefacts BIG), les agents confondent "spécifique au domaine" avec "moderne". Un stepper qui s'appelle "Descente au sol" reste un stepper. Toujours recalibrer.
5. **Les captures Puppeteer ne montrent pas les détails subtils** : le grain à 3-5% d'opacité est invisible sur screenshot. L'inspection CSS est nécessaire pour confirmer.
6. **Les contradictions internes diluent le signal** : les squelettes CSS contenaient des patterns blacklistés (glow, letter-spacing hover, animation infinite). Le subagent recevait des signaux contradictoires.
7. **La blacklist relève le plancher, pas le plafond** : elle élimine le daté mais ne pousse pas vers l'élite. Le plafond vient de la qualité du pitch.
8. **Les patterns micro (ombres, grain, radius) sont contextuels** : pas blacklistables en binaire. Les ombres ne sont pas "mortes" — elles sont ponctuelles (1-2 éléments), pas systématiques.

---

## TESTS RÉALISÉS

| Test | Dossier | Résultat | Ce qu'on a appris |
|------|---------|---------|-------------------|
| Camille Phase 4 (avant blacklists) | test-camille-test-20260404-2149 | Zigzag divider + CTA flèche + 5 cards grid | Contamination exemples |
| Camille Phase 4 (après blacklist CSS) | test-camille-test-20260405-phase4-run2 | Zigzag persistant + CTA flèche | Gate ne détectait pas les zigzags en enfant |
| Camille Phase 4 (gate amélioré) | test-camille-test-20260405-1352 | Pas de zigzag ✅, CTA flèche persiste, 5 cards grid | Gate CSS OK, composition pas encore traitée |
| Camille 3B7→4 (blacklist compo + principes) | test-camille-test-20260407-1538 | Hero moderne ✅, artefact = dashboard avec hiérarchie MAIS bordures | Mieux mais pas élite |
| Camille Phase 4 (principes hiérarchie) | test-camille-test-20260407-1732 | 5 cards grid `repeat(5,1fr)` malgré les principes | Les principes ne suffisent pas — le pitch domine |
| Camille Phase 4 (exemples refondus + tout) | test-camille-test-20260408-0011 | Hero ✅ atmosphere ✅ artefact = encore 5 cards grid | Pitch > Exemples > Principes confirmé |

---

### 12. Accent bar blacklisté (FAIT)
Trait vertical/horizontal coloré épais (2px+) plaqué sur le bord d'un conteneur. Pattern Material Design/Bootstrap 2016-2020. Vérifié absent des 21 sites Awards. Ajouté à la blacklist CSS Phase 4.

### 13. Injection principes composition dans Phase 3B (FAIT — par Charles en session séparée)
Bloc "PRINCIPES DE COMPOSITION" ajouté dans `phase-3b-design.md` entre "ZÉRO CSS" et "DIVERGENCE VISUELLE" :
- 9 items INTERDITS (blacklist composition traduite en sensation)
- 6 items PRESCRITS (hiérarchie, séparation, densité, masse chromatique, parcimonie, données clés)
- Correction anti-contamination lexicale : listes entre parenthèses retirées des prescriptions d'exécution

### Test Camille 20260408-1137 — Résultats
- **Pitch** : EXCELLENT — 9/9 blacklist composition respectés, 6/6 principes positifs respectés, artefact prescrit avec hiérarchie 3 couches
- **Style-tile (sans visuels)** : artefact asymétrique 3 zones (1fr / 1.8fr / 1.2fr), chiffre dominant en display, séparation par fond ✅. MAIS : 3 cards "01 02 03" dans l'atmosphere (steps numérotés = blacklisté), accent bars latéraux (blacklisté après ce test)

### 14. Gate mécanique renforcé — 13 checks (FAIT)
- Ajout `check_accent_bar` : détecte `border-inline-start`/`border-left` ≥ 2px avec couleur
- Ajout `check_overline_decorative_line` : détecte `::before`/`::after` sur les overlines qui dessinent un trait
- Total : 13 checks mécaniques dans `scripts/phase4-blacklist-gate.py`

### 15. Blacklist élargie — traits décoratifs (FAIT)
- Overlines : trait `::before`/`::after` devant les overlines retiré des exemples C, D, E + blacklisté
- Titres : `border-block-end` coloré sous les titres ajouté à la blacklist (0/10 Awards l'utilisent)
- Compositions datées : la blacklist s'applique maintenant explicitement à "TOUTES les sections — Voice Block, Artefact ET Atmosphere"
- Formulation unifiée : "la hiérarchie typographique se crée par la taille, le poids et la couleur, pas par une ligne dessinée"

### 16. Fix prompt trop gros — images lues depuis le disque (FAIT)
- Le prompt Phase 4 devenait trop gros (~380 lignes + pitch ~140 lignes + images base64 ~80K caractères)
- Fix dans SKILL.md : au lieu d'injecter les base64 dans le prompt, passer les chemins des fichiers. Le subagent Phase 4 lit les images depuis le disque via Read tool
- Appliqué aux visuels de référence ET aux étalons Awards

### 17. Frequency visualizer retiré de l'exemple D (FAIT)
- 30 `freq-bar` statiques dans l'atmosphere de l'exemple D contaminaient les outputs
- Le test Camille run3 avait produit des "sediment strata" = copie directe du pattern freq-bar
- CSS + HTML retirés de `examples/rupture/style-tile-example-D.html`

### Tests supplémentaires

| Test | Dossier | Résultat |
|------|---------|---------|
| Camille Phase 4 (pitch avec principes 3B) | test-camille-test-20260408-1137 | Pitch excellent (9/9 blacklist + 6/6 principes). Style-tile sans image : artefact asymétrique ✅ mais 3 cards "01 02 03" dans l'atmosphere + accent bars |
| Camille Phase 4 run2 (avec images) | test-camille-test-20260408-phase4-run2 | Hero avec image en layering ✅, artefact 3 zones asymétriques ✅, atmosphere manifesto ✅. Résiduels : accent bar (maintenant gaté), trait sous titre (maintenant blacklisté) |
| Camille Phase 4 run3 | test-camille-test-20260408-phase4-run3 | Hero + artefact bons. Atmosphere : sediment strata (barres) = contamination par les freq-bar de l'exemple D (maintenant retiré) |

### Incohérence de nommage étalons (NON CORRIGÉ — noté)
- Phase 3B-5 stocke les étalons sous `{brand}-etalon-niveau-{n}.{ext}` (ligne 1869 du SKILL.md)
- Phase 4 les cherche sous `etalon-*.png` (ligne 2465 du SKILL.md)
- Risque : Phase 4 ne trouve pas les étalons. À corriger dans une session d'orchestration.

---

## ÉTAT FINAL DU SYSTÈME (après cette session)

### Fichiers modifiés (commits sur main)
| Fichier | Modifications cumulées |
|---------|----------------------|
| `phases/phase-4-styletile.md` | Blacklist CSS (~25 patterns) + blacklist composition (9 items, TOUTES sections) + 8 principes hiérarchie + ombres ponctuelles + palette restreinte + accent bar + traits décoratifs |
| `phases/phase-3b-design.md` | Clarification A=3 + radius polarisé + prescription artefact renforcée + statement final + translateY aligné + principes composition (9 interdits + 6 prescrits) |
| `ref/css-patterns-phase4.md` | 6 corrections squelettes (VB-3, VB-4, VB-8, VB-10, AT-3) |
| `ref/html-showroom-spec.md` | blur(20px) → blur(10px) |
| `scripts/phase4-blacklist-gate.py` | 13 checks mécaniques (11 originaux + accent-bar + overline-decorative-line) |
| `SKILL.md` | Gate intégré en 4A-ter + fix injection base64 |
| `examples/*.html` (6 fichiers) | CSS décontaminé + artefacts refondus (composants exotiques avec hiérarchie) + flèches CTA retirées + traits overline retirés + freq-bars retirées |

### Ce qui fonctionne
- Les heroes sont modernes (full-bleed, layering, typo massive, pas de split 50/50)
- Les atmospheres sont modernes (manifesto assertif, pas de cards numérotées, pas de mega-footer)
- Les artefacts ont de la hiérarchie (3 zones, chiffre dominant, densité variable) quand le pitch le prescrit bien
- Le gate mécanique attrape 13 patterns CSS datés
- Phase 3B connaît les blacklists et les principes de Phase 4

### Ce qui reste problématique
- Le LLM retombe ENCORE sur des réflexes d'entraînement (accent bars, traits décoratifs) malgré les blacklists textuelles. Le gate mécanique est le seul filet fiable.
- L'artefact dépend fortement de la qualité du pitch 3B. Un pitch qui dit "5 étapes" → repeat(5, 1fr). Un pitch qui dit "score dominant + données secondaires" → hiérarchie.
- Les étalons Awards ont une incohérence de nommage entre 3B-5 et Phase 4

### Prochaines actions recommandées
1. Tester avec d'autres briefs (pas seulement Camille) pour vérifier la généralisation
2. Corriger l'incohérence de nommage des étalons dans le SKILL.md
3. Continuer à identifier et retirer les contaminants résiduels dans les exemples au fil des tests

## Dernière mise à jour : 2026-04-09
