# REX — Session d'optimisation visuels BIG (30 mars - 1er avril 2026)

Session marathon de 2 jours. 3 axes identifiés, 1 axe traité en profondeur, 2 axes restants à implémenter.

---

## Contexte : l'audit initial

88 sites Awards (startups primées) analysés par 4 subagents parallèles. Résultats dans `outputs/pattern-demo/` (audit-heroes.html, groupements.html, pedagogie.html).

### Stats clés Awards vs BIG

| Métrique | Sites Awards | BIG (avant session) |
|---|---|---|
| Layout Stacked | 27% | ~0% |
| Layout Full-bleed overlay | 23% | ~0% |
| Layout Split | 19% | **71%** (surreprésenté x3.7) |
| Images Hero visibles | ~70% | Images enterrées en fond invisible |
| Texte aligné gauche | 60% | **96%** |
| Typo hero taille | 8-12vw | 5-6vw |

---

## AXE 1 — Qualité des visuels (TRAITÉ)

### Ce qui a été fait

1. **Skill `/visual-brief` isolé** (D43) — Phase 3C extraite en session séparée avec contexte frais
2. **Penseur visuel** (D44) — Nouveau subagent Phase 3B (Vague 2quater) entre spécimens et pitch final
   - Flux en 2 passes : choix du registre → demande d'étalons → prescriptions calibrées
   - Taxonomie de types visuels (familles A-G, 34 types)
   - Ancre stylistique 6 dimensions (dont registre de réalité)
   - Gate qualité universelle : "chaque élément justifie sa présence" (pas de règles dures par registre)
3. **Skill `/visual-brief` enrichi** :
   - Double prompt systématique MJ + Recraft (l'utilisateur teste les deux)
   - 3 gates : conformité technique, anti-stock, anti-slop IA
   - Params Recraft externes (palette, dimensions, modèle)
   - Demande d'images de NIVEAU en début de session (benchmark craft)
   - Gate de résolution minimum (plus de downscale à 1200px)
   - Bonnes pratiques anti-dérive MJ (références éditoriales, --no anti-fiction, vocabulaire contemporain)
4. **Règles de visibilité des images** dans Phase 4 :
   - Conditionnelles selon usage (Hero/Accent = visible, Atmosphere = fond OK)
   - INTERDIT : opacity < 0.85 sur Hero/Accent, blend-mode destructeur, couches opaques par-dessus
   - TEST : plisse les yeux → chaque image Hero doit être immédiatement visible
5. **Pitch final modifié** (phase-3b-design.md) — REPREND la direction visuelle au lieu de DÉRIVER

### Ce qui a marché

- Le penseur visuel élimine le stock (plus de "mains sur clavier")
- La direction technique est suffisamment précise pour que le skill ne devine plus
- Le registre de réalité empêche les dérives fiction/steampunk de MJ
- Les double prompts MJ+Recraft donnent plus de marge
- Les étalons visuels en début de session calibrent le niveau d'exigence

### Ce qui reste limité

- **Plafond Recraft** : ~7-7.5/10 en registre photo macro. Les outils génératifs ne produisent pas le niveau ICOMAT/POUCH sans retouche manuelle.
- **Anti-dérive MJ** : pas de règle abstraite fiable. Le double prompt est le seul filet.
- **Les critères élite doivent être dérivés des étalons** (pas codés en dur) — sinon ils ne sont valides que pour un registre.

### Biais identifié et corrigé

Les 5 critères élite initiaux étaient ADDITIFS ("ajoute du grain, de la fumée, de la texture"). Les sites Awards élite sont SOUSTRACTIFS ("un sujet, une lumière, rien d'autre"). Corrigé : critère universel "chaque élément justifie sa présence" + règles dérivées des étalons fournis.

### Fichiers modifiés/créés (axe 1)

| Fichier | Action |
|---|---|
| `.claude/skills/visual-brief/SKILL.md` | Réécrit (étape 1 exécute au lieu de raisonner, 3 gates, double prompt, params Recraft, benchmark niveau, résolution) |
| `.claude/skills/brand-identity/phases/phase-3b-penseur-visuel.md` | CRÉÉ (prompt complet 2 passes) |
| `.claude/skills/brand-identity/phases/phase-3b-design.md` | Modifié (visuels recommandés = REPRENDRE pas DÉRIVER) |
| `.claude/skills/brand-identity/phases/phase-4-styletile.md` | Modifié (règles visibilité images conditionnelles) |
| `.claude/skills/brand-identity/SKILL.md` | Modifié (Vague 2quater + Phase 3C lit visual-direction) |
| `.claude/skills/brand-identity/ref/visual-direction-guide.md` | CRÉÉ (guide DA, modifié section 7) |
| `.claude/skills/brand-identity/ref/visual-prompting-rex.md` | CRÉÉ par la session de test (workflow Recraft Remix) |
| `.claude/skills/test-big/SKILL.md` | Modifié (phases 3B-3 à 3B-5 + 3C) |

---

## AXE 2 — Techniques CSS (À FAIRE)

### Ce que l'audit a identifié

1. **Dialogue texte/image (layering)** — CRITIQUE
   - Les sites Awards font du z-index layering (texte qui traverse l'image, éléments devant/derrière)
   - BIG ne le fait JAMAIS
   - Les règles existent dans le catalogue CSS mais les EXEMPLES ne le montrent pas → pattern "Code > Rules"

2. **3ème couche graphique** — IMPORTANT
   - Éléments de liaison entre texte et image (lignes, formes, particules SVG)
   - Un seul cas BIG (Camille C3, lignes de convergence) — et c'est le hero le mieux noté
   - À systématiser

3. **Surfaces enrichies** — MODÉRÉ
   - feTurbulence/noise SVG existe dans le catalogue mais n'est pas utilisé par défaut
   - Les fonds sont des aplats unis
   - Proposition : rendre la texture obligatoire (grain subtil 2-3% sur chaque fond)

### Recommandation d'implémentation

**Le levier le plus efficace : modifier les EXEMPLES de référence** (pas les règles). Le pattern "Code > Rules" est documenté : le LLM reproduit ce qu'il VOIT dans les exemples. Si les 6 exemples HTML ont du layering, de la 3ème couche, et du grain → le LLM le fera.

Fichiers à modifier :
- `examples/standard/style-tile-example-A.html` (A=1)
- `examples/standard/style-tile-example-B.html` (A=2)
- `examples/rupture/style-tile-example-C.html` (A=3)
- (et les 3 autres E, F, D)

Page pédagogique avec exemples Awards concrets : `outputs/pattern-demo/pedagogie.html`

---

## AXE 3 — Layout et taille du visuel (À FAIRE)

### Ce que l'audit a identifié

1. **Variété des layouts** — CRITIQUE
   - BIG fait du split 71% du temps (avec images)
   - Les Awards font stacked (27%) + full-bleed (23%) + split (19%)
   - Les 2 meilleurs heroes BIG (Alch C1, CP C3) étaient en full-bleed — corrélation claire

2. **Taille du visuel** — IMPORTANT
   - Dans les splits BIG, le visuel occupe 15-20% du hero
   - Awards : 40%+ minimum

3. **Taille typographique** — MODÉRÉ
   - BIG : ~5-6vw pour les headlines
   - Awards : 8-12vw

### Recommandation d'implémentation

1. **Non-répétition layout** : les 3 subagents Phase 4 ne peuvent pas utiliser le même layout. Même mécanisme que Phase 3A pour la divergence.
2. **Exemples de référence** : ajouter 2 exemples HTML avec stacked et full-bleed overlay (les plus courants aux Awards et les plus absents chez BIG).
3. **Taille minimum visuel** : règle dans Phase 4 — dans un split, le visuel occupe ≥ 40% du hero.
4. **Taille typo** : augmenter la baseline dans les exemples à 8-10vw.

---

## Démo et audit dans outputs/pattern-demo/

| Fichier | Contenu |
|---|---|
| `index.html` | 8 patterns de layout avec démo visuelle, ordonnés par fréquence Awards |
| `audit-heroes.html` | Tableau des 88 sites Awards avec classifications (layout, visuel, style, impression, A BIG, B) |
| `groupements.html` | Groupements par layout, type visuel, style, curseur A BIG |
| `pedagogie.html` | Explications layering, 3ème couche, surfaces — avec exemples Awards illustrés |
| `plan-amelioration-visuels.md` | Plan complet des 3 axes avec 11 actions à cocher |

---

## Memories mises à jour

- `project_visual_audit_2026_03.md` — stats Awards, gaps identifiés, recommandations
- `MEMORY.md` — liens vers l'audit et le skill `/visual-brief`

---

## Prochaines étapes (nouvelle session)

1. **AXE 2 — CSS** : Modifier les exemples HTML de référence pour y intégrer du layering, de la 3ème couche graphique, et du grain SVG. C'est le levier le plus efficace (pattern "Code > Rules").
2. **AXE 3 — Layout** : Ajouter 2 exemples HTML (stacked + full-bleed). Ajouter la contrainte de non-répétition layout entre les 3 concepts. Augmenter la taille typo et la taille minimum du visuel.
3. **Tester** : Relancer un cycle complet VoltaPilot ou Vermeil avec les 3 axes implémentés et comparer au style-tile actuel.

## Dernière mise à jour : 2026-04-01
