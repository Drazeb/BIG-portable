# Plan Master — Chantier 3 anti-slop fonts (3B-1 + 3B-2)

> **Document de sanctuarisation des décisions.** Ce plan est mis à jour au fil des sessions. Il sert de référence stable pour ne pas perdre le fil pendant l'exécution. Toute décision prise ou amendée doit être reflétée ici dans la même session.

**Session démarrée** : 2026-04-28
**Session terminée** : 2026-04-29
**Statut global** : ✅ COMPLETED — Phases 0, 1, 1bis, 2, 3, 4, 5, 6 toutes terminées. Test E2E Camille validé (6 violations détectées sur 3 concepts = régression check OK).

## Résumé final du chantier

**Pool final** : 110 fontes uniques (Google Fonts + Fontshare + local self-host)
- Display A1 : 43 / Display A2 : 73 / Display A3 : 49
- Body A1 : 50 / Body A2 : 70 / Body A3 : 30 (limite structurelle marché free)

**Livrables techniques** :
- `lib/font-pool-contact-sheet.mjs` refactor multi-source + check strict chargement
- `lib/fonts/` (Sporting Grotesque + Departure Mono self-host)
- `lib/regenerate_pools.sh` (script reproductible)
- `ref/font-source-map.json` (110 fontes → CDN)
- `ref/font-axes-tags.json` (110 fontes × 3 axes structurels)
- `ref/font-pools/font-pool-{display,body}-A{1,2,3}-mapping.json` (6 mappings)
- 11 planches PNG régénérées
- `scripts/phase3b-fonts-anti-slop.py` (340 lignes, 7 checks, mode --json-output)
- `phases/phase-3b-penseur.md` + `phase-3b-penseur-body.md` (bloc N1/N2 anti-slop)
- `SKILL.md` sous-section "Vague 1bis — GATE ANTI-SLOP FONTS" (~50 lignes)

**Validation E2E** : gate testé sur 3 concepts Camille → 6 violations détectées (Fraunces × 3, IBM Plex Sans × 2, DM Serif Display × 1). Comportement attendu confirmé.

**Hors scope reporté** :
- Lacunes Phase 4 typo 1+2 (dashboard sans serif, editorial pairing) : non retenues par session Phase 4 après tests
- Refactor pool unifié + tags audace : dette technique notée
- Body A3 boutique payante : limite marché free assumée
- Chantier 4 anti-slop style (3B-7a styliste) : passation à rédiger en début prochaine session



---

## 0. Contexte

Le chantier 3 du programme anti-slop BIG (cf. `ref/passation-anti-slop-fonts-2026-04-28.md`) couvre la sélection typographique en Phase 3B (penseurs typographiques 3B-1 + designer visuel 3B-2). Ce chantier suit les chantiers 1 (routeur chromatique) et 2 (palette) qui sont déjà committed.

Méthode reproduite des chantiers précédents : N1/N2 dans le prompt + N3 dans gate Python + tests sur cas réels + patches post-test.

---

## 1. Décisions arrêtées (à ne pas re-débattre)

### 1.1 Cartographie des règles fonts en 6 familles
6 familles distinctes (cf. conversation 2026-04-28) :
- **F1 — Sélection** (quel nom de fonte) : pool en amont + gate sur la longlist
- **F2 — Pairing** (mariage display × body) : gate sémantique sur le couple
- **F3 — Poids/Weights** : Phase 4 only — vérification préventive sur le pool (≥4 weights disponibles)
- **F4 — Mise en œuvre** (CSS letter-spacing, line-height, all-caps) : Phase 4 only — déjà couvert par `typography-core.md`
- **F5 — Technique web** (font-display, OpenType, fluid type) : Phase 4 only — partiellement couvert, `font-display: swap` à ajouter (cf. passation Phase 4)
- **F6 — Process/mentalité** : largement couvert par `font-matching-rules.md`, ajouts marginaux non retenus

### 1.2 Périmètre du chantier 3
**In scope** :
- Pool des fontes (curation, ban, ajout, équilibre par registre)
- Prompts penseurs `phase-3b-penseur.md` + `phase-3b-penseur-body.md`
- Mécanisme designer visuel 3B-2 si nécessaire
- Gate Python `phase3b-fonts-anti-slop.py` (à créer)

**Hors scope (renvoyé en Phase 4 dans une passation dédiée)** :
- Cf. `ref/passation-anti-slop-phase4-typography-2026-04-28.md`
- Lacune Phase 4 #1 : dashboard = serif banni
- Lacune Phase 4 #2 : editorial = pairing serif+sans par défaut
- Lacune Phase 4 #3 : `font-display: swap` non vérifié dans gate finishing

### 1.3 Stratégie ban absolu (validée 2026-04-28)
**Pas de règles contextuelles** (Fraunces autorisé sauf si brief warm = trop complexe). À la place : **ban absolu** des 3 listes consolidées.

**Liste 1 — Invisibles (ban absolu)** :
Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Helvetica, Arial, Source Sans 3, Public Sans, Nunito Sans, IBM Plex Sans, DM Sans

**Liste 2 — Generic serifs (ban absolu)** :
Times New Roman, Georgia, Garamond, Palatino, Book Antiqua, Bookman

**Liste 3 — Tasteful reflex traps (ban absolu — décision 2026-04-28)** :
Fraunces, Cormorant, Cormorant Garamond, Cormorant Infant, Playfair Display, DM Serif Display, DM Serif Text, EB Garamond (borderline)

**Anti-cousin clause** : pour chaque famille bannie, éviter aussi les cousins visuels — fonts de la même époque, mêmes proportions, mêmes constructions géométriques/humanistes qui seraient le second favori du LLM.

### 1.4 Règle anti-réflexe Impeccable — REJETÉE
Pas pertinente après ban absolu (redondante). Garde-la dans la poche pour le jour où on bascule vers un système ouvert.

### 1.5 Règles de pairing à intégrer (validées)
- **P1** — Au moins 1 axe de contraste structurel entre display et body (serif/sans, geometric/humanist, condensed/wide). Implémentation : tags axes sur chaque fonte du pool + check Python binaire vectoriel.
- **P2** — Pairing 2 fontes "similaires mais non identiques" interdit (sous-cas de P1, captée par même check)
- **P3** — Mono-fonte (display = body) acceptable quand contraste structurel non requis (N1 dans prompt penseur body)
- **Liste fermée pairings bannis** : Playfair+Lato, Cormorant+Montserrat, Poppins+Open Sans, Inter+Inter Mono mono-stack — devient redondante après ban absolu mais conservée comme filet

### 1.6 Process/mentalité — pas de patch
Couverture actuelle de `font-matching-rules.md` (5 règles) jugée suffisante après croisement avec process Impeccable. Pas de patch dans le chantier 3.

### 1.7 Stratification A1/A2/A3 — préservée
Modèle 3 niveaux d'audace conservé. Cohérent avec curseur A de BIG. Pas de remise en cause structurelle. **Mais** : recomposition complète des 3 pools nécessaire (constats ci-dessous).

---

## 2. Constats d'audit du pool actuel (2026-04-28)

### 2.1 Trois problèmes structurels détectés
1. **Fontes datées concentrées en fin de pool** (rangs 33-50 = popularité Google Fonts). Curation par popularité, pas par qualité.
2. **Geist absente du DISPLAY** (présente seulement en body A1 #01, body A2 #02). Lacune majeure — Geist est la fonte signal anti-slop par excellence en 2025-2026.
3. **Couverture inégale par registre** :
   - A1 : sur-représenté en sérifs classiques, sous-représenté en tech distinctif + industrial
   - A2 : mix correct mais contient les fontes datées
   - A3 : trop lourd en déco gimmick (~18-20 fontes "à effet visuel uniquement"), warm artisanal sous-représenté, tech distinctif premium absent

### 2.2 Volume cible des pools
- 50 display × 3 niveaux audace = 150 slots display
- 50 body × 3 niveaux audace = 150 slots body
- **Total : ~300 slots à remplir**
- **Overlaps inter-niveaux acceptés** (une fonte peut être en A1 ET en A2). Avec ~50% d'overlap A1↔A2 et A2↔A3, besoin réel ~150-200 fontes uniques.

### 2.3 Estimation slots libérés par ban absolu
Pool body actuel A1+A2+A3 contient ~12-15 fontes des Listes 1+2+3. Pool display A1+A2+A3 en contient ~8-10. **Total ~20-25 slots à libérer + autant de remplaçants à trouver** (compte tenu des overlaps).

Plus : **élagage déco gimmick A3** (~8-10 slots à libérer en display A3).

→ **~30-40 nouveaux slots à pourvoir avec des fontes premium 2025-2026 non-slop**.

---

## 3. Étapes d'exécution (séquence master)

### Phase 0 — Préparation + recherche typeface inventory (✅ CLOSE)
- [x] Lecture passation 2026-04-28 et contexte global
- [x] Cartographie audit-slop des règles fonts (6 familles)
- [x] Vérification couverture Phase 4 actuelle
- [x] Audit du pool actuel (constats 2.1)
- [x] Rédaction passation Phase 4 (`ref/passation-anti-slop-phase4-typography-2026-04-28.md`)
- [x] Rédaction prompt Perplexity v1 (`ref/perplexity-prompt-fonts-premium-2026-04-28.md`)
- [x] Run Perplexity v1 (50 fontes, 75% boutique → insuffisant)
- [x] Décision : Google Fonts + Fontshare uniquement (pas de boutique payante)
- [x] Rédaction prompt Perplexity v2 GF+Fontshare (`ref/perplexity-prompt-fonts-premium-v2-google-fontshare-2026-04-28.md`)
- [x] Run Perplexity v2 → 108 unique fontes, 12 registres ≥10
- [x] Audit critique v2 → 6 faiblesses identifiées (SLOP_RISK manquants, ITF filler, gaps, sur-représentation ITF, borderlines, weak proofs)
- [x] Rédaction prompt Perplexity v3 adversarial review (`ref/perplexity-prompt-fonts-premium-v3-affinage-adversarial-2026-04-28.md`)
- [x] Run Perplexity v3 → rapport adversarial 116 unique fontes, défenses + concessions
- [x] Audit final v3 → adoption canonique validée par Charles

### État actuel post-v3 (2026-04-28 après-midi) — sanctuarisation décisions

**Pool canonique adopté** : v3 inventory (rapport `~/Downloads/V2 Adversarial Review — Typography Inventory v3 Corrections.md`, 116 unique fontes).

**Retraits actés (9)** :
- 8 WEAK_PROOF retirés (manque preuve d'usage réel) : Sentient (Reg 2), Pally (Reg 6), Pilcrow Rounded (Reg 6), Synonym (Reg 3), Tabular (Reg 3), Boska (Reg 1 + cross Reg 8), Bespoke Slab (Reg 8), Bespoke Stencil (Reg 12)
- Roboto Slab retiré (association Roboto = signal mixte, pas net)

**Ajouts de complément actés (4 nouvelles + cross-listings) pour combler sub-minimum** :
- Eczar (Reg 2 Modern serif + cross Reg 8 Slab) — Rosetta foundry GF, humanist serif distinctive
- Trench Slab Fontshare (Reg 8 Slab) — réintégration de v2 (absente du tableau v3 final)
- Sansita (Reg 8 Slab) — Google Fonts slab playful single-style
- Cross-listings explicites : Geist Mono → Reg 3 + Reg 10 ; Recursive → Reg 3 + Reg 10 ; Newsreader → Reg 1 + Reg 6 ; Spectral → Reg 2 + Reg 6

**Pool final** : **~111 fontes uniques**, 12 registres tous ≥10.

**SLOP_RISK_EMERGING tags consolidés (12)** : Switzer ⚠️, Cabinet Grotesk ⚠️, Clash Display ⚠️, General Sans ⚠️, Space Grotesk ⚠️, Bricolage Grotesque ⚠️, Syne ⚠️, Manrope ⚠️ (nouveau v3), Outfit ⚠️ (nouveau v3), Anton ⚠️ (nouveau v3), Oswald ⚠️ (nouveau v3), Space Mono ⚠️ (nouveau v3).

**Quicksand REMOVED ENTIRELY** (upgrade v3 — Pimp My Type "Goodbye Quicksand" 2024).

**Borderlines tranchés** :
- Alegreya INCLUDE Reg 2+6 (école Aldine ≠ Garald, ATypI Letter2)
- Hanken Grotesk INCLUDE Reg 4 (Awwwards HMs 2024-2025)
- Roboto Slab REMOVED (décision Charles)
- Plus Jakarta Sans EXCLUDE confirmé
- Inclusive Sans INCLUDE Reg 5 (Penguin Books, Olivia King — strongest proof)
- Sono INCLUDE Reg 10 (Tyler Finck, variable MONO axis)
- Atkinson Hyperlegible classic EXCLUDE (Next supersedes)
- Big Shoulders Stencil INCLUDE Reg 12

**Allocation contraintes** :
- Lora restreinte aux pools A1 + A2 uniquement (pas A3 — manque distinctiveness pour audace haute)
- 6 fontes en surveillance personnelle Claude (à monitorer post-déploiement) : Bodoni Moda, Lora, Manrope, Space Mono, Calistoga, General Sans

**Méthode composition pool (séquence A/B/C/D)** :
- Phase A : Subagents recherche doc enrichie sur ~40 fontes Fontshare/ITF/Velvetyne/independants moins connus de Claude (lance prochainement, ~15 min background)
- Phase B : Allocation A1/A2/A3 + tags axes structurels (structure : serif/sans/slab — construction : geometric/humanist/transitional — proportion : condensed/normal/wide) sur les ~111 fontes. Confiance haute sur ~70 fontes connues, confiance moyenne sur ~40 fontes ITF avec doc enrichie.
- Phase C : Validation visuelle multimodale par Claude sur cas douteux uniquement (génération mini-planches PNG ciblées)
- Phase D : Validation logique par Charles (audace cohérente avec concept ? registre clair ? overlap A1↔A2 sain ?). PAS de validation visuelle par Charles (non-designer).

### Phase 1 — Recomposition des pools
- [ ] Liste finale fontes à retirer (ban absolu Listes 1+2+3 + déco gimmick A3)
- [ ] Liste finale fontes à ajouter (depuis Perplexity v1 + v2)
- [ ] Tags axes structurels sur chaque fonte (structure: serif/sans/slab — construction: geometric/humanist/transitional — proportion: condensed/normal/wide)
- [ ] Allocation par audace A1/A2/A3 (avec overlaps acceptés)
- [ ] Allocation par registre (chaque registre → ≥8-10 fontes utilisables par pool)
- [ ] Validation par Charles avant régénération
- [ ] Régénération mappings JSON (`font-pool-display-A{1,2,3}-mapping.json` + body)
- [ ] Régénération planches PNG (`lib/font-pool-contact-sheet.mjs`)

### Phase 2 — Patches prompts penseur (3B-1)
- [ ] Ajout bloc "RÈGLES ANTI-SLOP" dans `phase-3b-penseur.md` (display) — N1/N2 uniquement
- [ ] Ajout bloc "RÈGLES ANTI-SLOP" dans `phase-3b-penseur-body.md` — N1/N2 + règle P3 (mono-fonte acceptable)
- [ ] Pas de patch sur `font-matching-rules.md` (couverture jugée suffisante)

### Phase 3 — Création gate Python `phase3b-fonts-anti-slop.py`
- [ ] Format strict longlist (12-15 display / 10 body, ordonnée, scan binaire)
- [ ] Justifications spécifiques (pas de phrases génériques applicables à 5 autres fontes)
- [ ] Pairing : check vectoriel sur 3 axes structurels (FAIL si 0 axe différent)
- [ ] Liste fermée pairings bannis (filet de sécurité après ban absolu)
- [ ] Format `--json-output` (convention SKILL.md state machine)
- [ ] Exit codes 0=PASS / 1=FAIL / 2=ERREUR

### Phase 4 — Intégration SKILL.md (orchestration)
- [ ] Sous-section "GATE ANTI-SLOP FONTS" dans la zone 3B-1
- [ ] Pattern resume penseur si FAIL (max 2 itérations, anti-dégradation, prompt relu disque)
- [ ] Pattern PASS_WITH_PATCH si omission triviale

### Phase 5 — Tests E2E
- [ ] Test 1 : run sur `outputs/test-camille-test-20260415-1733/` (ancienne session, comparaison ancien/nouveau)
- [ ] Test 2 : run depuis 3B-1 sur Camille avec nouveaux pools — comparaison ancien vs nouveau (compter violations)
- [ ] Test 3 : brief Pool A=3 (audace haute) pour stresser le système
- [ ] Patches post-test si nécessaire

### Phase 6 — Commit + mise à jour mémoire
- [ ] Commit dédié
- [ ] Mise à jour `MEMORY.md` index
- [ ] Mise à jour de ce plan avec leçons apprises
- [ ] Rédaction passation pour le chantier 4 (style — étape 3B-7a styliste)

---

## 4. Question ouverte en cours d'arbitrage : Google Fonts only vs hybride

### 4.1 Position initiale (2026-04-28 décision préliminaire)
Option 1 (Google Fonts curé seul) — chantier immédiat. Option 2 (hybride boutique premium) — plus tard, séparé.

### 4.2 Constat sur Perplexity v1
Le rapport remonte 57 fontes : ~15 Google Fonts + ~40 boutique paid. Sur les 40 boutique, la qualité moyenne est nettement supérieure aux GF (Söhne, GT Sectra, Canela, Domaine, GT America, etc.).

**Implication** : le marché premium 2025-2026 est majoritairement boutique. Si on reste strictement GF, on plafonne notre qualité. Mais si on bascule hybride, on impose au client final l'achat de licences (~50-300€/fonte/web licence).

### 4.3 Options à arbitrer
1. **GF only — relancer Perplexity v2 GF-focused** : prompt v2 spécifique "give me 60-80 Google Fonts that elite designers use in 2025-2026 production work". Risque : raclage de fond — il y a peut-être seulement 30-40 GF vraiment non-slop disponibles.
2. **Hybride — accepter le mix actuel** : 15 GF (rang prioritaire pour licensing client) + 40 boutique (rang ambitieux pour briefs premium qui peuvent payer). Reformuler la stratification A1/A2/A3 en intégrant la dimension licensing.
3. **Combinaison — Perplexity v2 GF-focused PLUS rapport v1 utilisé pour tier boutique** : run un v2 pour avoir un pool GF complet, garde v1 comme pool boutique optionnel. Stratification possible : pools "free" (GF only, pour MVP/clients budget) + pools "elite" (avec boutique, pour briefs premium).

**Décision attendue** : Charles arbitre.

---

## 5. Fichiers de référence du chantier

| Fichier | Rôle | Statut |
|---|---|---|
| `ref/passation-anti-slop-fonts-2026-04-28.md` | Passation entrante (rédigée par session précédente) | Lu |
| `ref/passation-anti-slop-phase4-typography-2026-04-28.md` | Passation sortante vers Phase 4 (3 lacunes) | Créé |
| `ref/perplexity-prompt-fonts-premium-2026-04-28.md` | Prompt Perplexity v1 | Créé, exécuté |
| `~/Downloads/Premium Typeface Inventory 2025–2026 Non-Slop Pool for Brand Identity Generators.md` | Rapport Perplexity v1 (57 fontes) | Reçu, en cours d'évaluation |
| `ref/plan-master-chantier-3-fonts-2026-04-28.md` | **CE FICHIER** | Vivant |
| `ref/font-matching-rules.md` | Règles matching font×concept (5 règles + 3 pairing) | Inchangé (pas de patch décidé) |
| `ref/font-selection-rex.md` | REX historique sélection visuelle | Lu, à respecter |
| `ref/font-selection-next-session.md` | Notes next session de mars | Lu |
| `ref/font-pools/font-pool-{display,body}-A{1,2,3}-mapping.json` | Mappings pool (numéro→nom) | À recomposer |
| `phases/phase-3b-penseur.md` | Prompt penseur display | À patcher (N1/N2 anti-slop) |
| `phases/phase-3b-penseur-body.md` | Prompt penseur body | À patcher (N1/N2 anti-slop + P3 mono-fonte) |
| `scripts/phase3b-fonts-anti-slop.py` | Gate Python | À créer |
| `lib/font-pool-contact-sheet.mjs` | Génération planches PNG | À relancer après recomposition pools |

---

## 6. Risques identifiés et contre-mesures

| Risque | Probabilité | Contre-mesure |
|---|---|---|
| Pool recomposé trop boutique → coût licence client | Moyenne | Stratification "free vs elite" tier |
| Perplexity v2 GF-focused remonte trop peu de fontes (< 40) | Élevée | Combiner GF + sélectivement boutique pour combler |
| Régression qualité visuelle sur briefs déjà testés | Moyenne | Test E2E sur Camille avant commit |
| Sur-engineering du gate (ex: classification axes structurels trop subtile) | Faible | Garder check binaire vectoriel simple, élargir si test révèle besoin |
| Charles sature sur le volume de chantiers parallèles (3B fonts + Phase 4 typo + chantier 4 style) | Moyenne | Séquentialiser strictement : finir 3B fonts avant d'ouvrir chantier 4 |

---

## 7. Notes de session

### 2026-04-28 (session courante)
- Découverte : Geist absente des 3 pools display alors qu'omniprésente en body. Lacune majeure non documentée précédemment.
- Découverte : pools curés par popularité Google Fonts, pas par qualité — d'où la concentration de fontes datées en fin de pool.
- Décision : ban absolu des 3 listes (pas de contextuel). Dérogation refusée pour Fraunces malgré sa contradiction inter-sources.
- Décision : règle anti-réflexe Impeccable rejetée (redondante après ban absolu).
- Création passation Phase 4 et prompt Perplexity. Reste à évaluer Perplexity v1 et trancher sur GF only vs hybride.

---

## Dernière mise à jour
2026-04-28 — Création initiale par session 3B fonts.
