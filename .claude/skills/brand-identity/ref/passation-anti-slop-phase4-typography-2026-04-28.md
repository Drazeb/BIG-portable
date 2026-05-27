# Passation — Compléments anti-slop typographique pour Phase 4

> **Lecture obligatoire avant tout travail.** Ce document est rédigé par la session 2026-04-28 qui mène le chantier anti-slop fonts sur la **Phase 3B** (sélection). Lors de la cartographie audit-slop, 3 lacunes ont été identifiées **côté Phase 4** (utilisation des fontes dans les style-tiles HTML). Hors scope du chantier 3B, mais à intégrer en Phase 4 par une session dédiée. Ce document briefe cette session.

> **Statut chantier (2026-04-28 12:30)** :
> - ✅ **Lacune 3 (R-017 font-display: swap) — DONE** par session Phase 4 (commit `e1c0b26`). Check intégré dans `scripts/phase4-finishing-gate.py` en WARN, validé sur run réel `outputs/test-voltapilot-test-20260427-2046` (PASS si `&display=swap` présent, WARN si absent).
> - ⏸ **Lacune 1 (Dashboard = serif banni)** — NON RETENUE après test A/B sur VoltaPilot c2. La variante "strict no-serif" (Recursive partout) a été générée et comparée à l'original (Cormorant Garamond sur display + KPIs). Verdict utilisateur : la variante est moins bonne. La règle telle que formulée (binaire "serif banni partout en dashboard") casserait le meilleur résultat actuel. À reformuler en règle nuancée (serif autorisé sur display/KPI uniquement, banni sur body/UI/labels) si re-tentée plus tard.
> - ⏸ **Lacune 2 (Editorial = serif+sans par défaut)** — NON RETENUE pour cette itération. Devrait remonter en Phase 3B (sélection des fontes) plutôt qu'en Critique Phase 4 (flag tardif sur choix déjà fait). À coordonner avec le chantier 3B fonts.

---

## 0. TL;DR pour démarrer rapidement

- BIG produit des style-tiles HTML en Phase 4. La typographie en Phase 4 est déjà bien couverte par la Vague 2 (cf. `ref/passation-vague2-2026-04-26.md`, `ref/passation-anti-slop-pour-3b.md`).
- Les fichiers `ref/typography-core.md` (Critique typo-copy) et `ref/finition-elite-tier1.md` (Designer) couvrent déjà : single font + weights, pairing multi-axes, étalage 3 weights minimum, all-caps usage rare, letter-spacing inverse, line-height inverse, OpenType features, text-wrap, clamp, échelle modulaire.
- Le gate Python `phase4-finishing-gate.py` ligne 509-523 implémente déjà la blacklist Inter/Roboto/Open Sans/Lato/Montserrat (R-013).
- **3 lacunes restent à combler**, détaillées ci-dessous.

---

## 1. Contexte — pourquoi ces lacunes existent

Les sources audit-slop (Impeccable typography, Taste Skill stitch-skill, Taste Skill taste-skill, Vercel) contiennent des règles **contextuelles selon le type de surface** (dashboard vs marketing vs editorial). La Vague 2 a importé les règles **universelles** (qui s'appliquent partout), mais a laissé de côté les règles **conditionnelles**. Ces règles sont opérationnelles (le Designer/Critique peut les appliquer) mais nécessitent que le sub-agent connaisse le **registre de la surface** qu'il génère.

Les 3 lacunes :

1. **Dashboard / data-dense → serif strictement banni en headers ET body**
2. **Editorial / creative → privilégier serif header + sans body** (ou inverse) comme pairing par défaut
3. **`font-display: swap` non vérifié** dans le gate finishing (impact perf : layout shift au chargement de fonte)

---

## 2. Lacune 1 — Dashboard = serif banni

### Source

- `audit-slop/sources/taste-skill/taste-skill.md:41` : *"TECHNICAL UI RULE: Serif fonts are strictly BANNED for Dashboard/Software UIs. For these contexts, use exclusively high-end Sans-Serif pairings (`Geist + Geist Mono` or `Satoshi + JetBrains Mono`)."*
- `audit-slop/sources/taste-skill/stitch-skill.md:51-52` : *"Serif is always BANNED in dashboards or software UIs. Dashboard Constraint: Use Sans-Serif pairings exclusively."*

### Pourquoi c'est important

Un dashboard est conçu pour la **lecture rapide de données denses**. Les sérifs (avec empattements) ralentissent la lecture sur des écrans à haute densité d'information (chiffres, KPIs, labels courts). Les utilisateurs de dashboards ne lisent pas — ils scannent. La règle est universellement reconnue dans la communauté UI/UX (Linear, Vercel, Stripe Dashboard, Notion, Resend, tous sont en sans+sans). Un dashboard avec serif = signal slop immédiat (associé aux templates "premium dashboard" 2017-2020).

### Comment l'intégrer

**Approche recommandée** : règle sémantique dans `ref/typography-core.md` (lue par Critique typo-copy + Critique craft).

**Formulation N1/N2 proposée** (à adapter en cohérence avec le ton du fichier existant) :

```markdown
### Pairing contextuel selon la surface

Le pairing dépend du **registre de la surface** :

- **Dashboard / interface data-dense / SaaS UI** : sérifs bannis, en headers comme en body. Le pairing vit dans la famille sans-serif uniquement, idéalement avec contraste sans + mono pour les labels/données. Justification : la lecture en mode "scan rapide" est dégradée par les empattements ; le sérif sur dashboard est un marqueur de template daté (2017-2020).
- **Editorial / creative / marketing storytelling** : pairing privilégié sérif display + sans body (ou inverse), avec contraste structurel multi-axes. Le sérif y trouve son rôle naturel — densité de lecture longue, hiérarchie expressive.
- **Mixed / brand showcase** : laisser la latitude au Designer, vérifier seulement la cohérence concept × pairing.
```

**Détection de la surface** : la Phase 4 produit deux types d'artefact :
- `phase-4-styletile.md` → showroom de marque (registre brand showcase, mixed)
- `phase-4-artefact.md` → mockup d'app/dashboard (registre dashboard quasi-systématique)

Donc le Critique peut détecter mécaniquement : si l'artefact contient `data-table`, `KPI`, `metric-card`, `dashboard`, ou si c'est l'output `phase-4-artefact.md`, → registre dashboard → check serif.

**Variante gate Python** : un check supplémentaire dans `phase4-finishing-gate.py` qui flag (WARN ou FAIL selon arbitrage) la présence de `font-family: ... serif` dans un artefact détecté comme dashboard. Détection : recherche de tokens markup `<table>` dense, classes `.kpi`, `.dashboard`, ou meta tag de registre injecté par le pipeline.

### Cible des modifications

- **Ajout** : `ref/typography-core.md` §2 — paragraphe "Pairing contextuel selon la surface"
- **Vérifier** : que la règle remonte au Critique typo-copy (`phases/phase-4check-typo-copy.md`) qui lit déjà ce fichier
- **Optionnel** : ajout d'un check dans `scripts/phase4-finishing-gate.py` pour artefacts dashboard

---

## 3. Lacune 2 — Editorial = pairing serif + sans (ou inverse) par défaut

### Source

- `audit-slop/sources/taste-skill/redesign-skill.md:22` : *"For editorial/creative projects, pair a serif header with a sans-serif body."*
- `audit-slop/sources/impeccable/reference/typography.md:54-63` : pairing multi-axes — "Serif + Sans (structure contrast)" est le premier pairing recommandé.

### Pourquoi c'est important

Pour les briefs editorial/creative/marketing storytelling, le **pairing par défaut** dans la communauté design est : sérif (display ou body) + sans (l'autre). C'est le pattern qu'utilisent Vercel marketing, Stripe content, The Verge, Pitchfork, Awwwards editorial sites. **Quand un editorial brief produit un pairing sans+sans, le résultat sent immédiatement le SaaS générique**, même avec des bonnes fontes.

La règle n'est pas absolue (mono+sans ou serif+serif italics peuvent être justifiés contextuellement) mais elle est un **point de référence par défaut** — une dérogation devrait être justifiée par le concept narratif, pas par défaut.

### Comment l'intégrer

**Approche recommandée** : règle complémentaire au paragraphe "Pairing contextuel" ci-dessus dans `typography-core.md`. Le paragraphe couvrirait à la fois la lacune 1 (dashboard=sans) et la lacune 2 (editorial=mixed).

**Note sur l'articulation avec 3B** : la sélection des fontes se fait en 3B. La règle "editorial = serif+sans par défaut" devrait remonter en 3B-1 (penseurs typographiques) pour orienter le choix dès la longlist. Mais c'est aussi un check Critique en Phase 4 qui peut flag un mismatch si le concept est editorial mais le pairing est sans+sans.

→ **Coordination utile avec le chantier 3B fonts** (en cours — cf. `ref/passation-anti-slop-fonts-2026-04-28.md`).

### Cible des modifications

Idem lacune 1 : `ref/typography-core.md` §2.

---

## 4. Lacune 3 — `font-display: swap` non vérifié dans le gate finishing

### Source

- `audit-slop/sources/impeccable/reference/typography.md:65-90` : section complète "Web Font Loading" qui prescrit `font-display: swap` + `size-adjust` / `ascent-override` pour minimiser CLS (Cumulative Layout Shift).
- `audit-slop/sources/vercel-command.md` : règles de performance web — typographie performance.

### Pourquoi c'est important

Sans `font-display: swap`, le navigateur attend que la fonte soit chargée avant d'afficher le texte (FOIT — Flash Of Invisible Text). Le visiteur voit une page vide pendant 100-500 ms. Avec `swap`, le texte s'affiche immédiatement en fallback puis bascule sur la fonte chargée (FOUT — Flash Of Unstyled Text). Le compromis FOUT est universellement préféré à FOIT.

C'est une règle technique simple, **détectable mécaniquement** par grep CSS, et **systématiquement attendue** sur les style-tiles HTML production-grade.

### État actuel BIG

Le gate `phase4-finishing-gate.py` couvre la blacklist fontes (R-013) mais **ne vérifie pas la présence de `font-display: swap`** dans les `@font-face` ni dans les import URL Google Fonts. Vérification manuelle des style-tiles produits : la directive `&display=swap` est parfois présente dans les URL Google Fonts (héritage de templates) mais inconstante.

### Comment l'intégrer

**Approche recommandée** : ajouter un check dans `scripts/phase4-finishing-gate.py`.

**Logique** :
1. Si le HTML utilise des fontes externes (recherche `@font-face`, `fonts.googleapis.com`, `fonts.gstatic.com`, `<link rel="preload"...font...`) :
   - Vérifier qu'au moins une de ces 3 conditions est satisfaite : URL Google Fonts contient `&display=swap`, OU `@font-face` contient `font-display: swap`, OU les deux.
2. Si fonte externe sans `font-display: swap` détecté → WARN (ou FAIL selon arbitrage — Vercel le traite en FAIL pour leurs marketing pages).

**Format du check** (conforme aux conventions existantes du gate) :

```python
def check_R017_font_display_swap(css: str, html: str) -> CheckResult:
    """R-017 | font-display: swap pour minimiser CLS au chargement de fonte."""
    label = "R-017 font-display: swap"
    # Détecter usage de fontes externes
    has_external_fonts = bool(re.search(
        r'@font-face|fonts\.googleapis\.com|fonts\.gstatic\.com|<link[^>]*preload[^>]*font',
        css + html
    ))
    if not has_external_fonts:
        return CheckResult("PASS", label, "Pas de fonte externe", [])
    # Vérifier présence font-display: swap
    has_swap = bool(re.search(
        r'font-display\s*:\s*swap|display=swap',
        css + html
    ))
    if has_swap:
        return CheckResult("PASS", label, "font-display: swap détecté", [])
    return CheckResult("WARN", label, "Fontes externes sans font-display: swap",
                      ["Ajouter `font-display: swap;` dans les @font-face ou `&display=swap` dans les URL Google Fonts"])
```

### Cible des modifications

- **Ajout** : `scripts/phase4-finishing-gate.py` — fonction `check_R017_font_display_swap`, enregistrement dans la table de checks vague2.
- **Optionnel** : compléter la formulation N1 dans `ref/finition-elite-tier1.md` ("CSS moderne — socle obligatoire") pour ajouter `font-display: swap` au socle obligatoire — utile pour orienter le Designer en amont.

---

## 5. Méthode reproductible — comment exécuter ce chantier

1. **Lire** ce document + `ref/anti-slop-formulation-guide.md` (convention N1/N2/N3) + `ref/passation-vague2-2026-04-26.md` (architecture Vague 2).
2. **Lire** les fichiers cibles : `ref/typography-core.md`, `ref/finition-elite-tier1.md`, `scripts/phase4-finishing-gate.py`.
3. **Patcher** dans cet ordre :
   - Lacune 3 (gate Python) en premier : techniquement isolé, déterministe, gain immédiat.
   - Lacune 1 + 2 (typography-core.md §2) ensemble : une seule modification cohérente "Pairing contextuel selon la surface".
4. **Tester** sur 1 session récente :
   - Test gate R-017 : lancer sur `outputs/test-voltapilot-vague2.5-*` pour vérifier qu'il PASS si `&display=swap` présent, WARN sinon.
   - Test typo-copy : relancer le Critique typo-copy sur un style-tile dashboard récent et vérifier qu'il flag un usage de serif (créer artificiellement le cas si nécessaire).
5. **Committer** avec message dédié `feat: complete anti-slop typographique Phase 4 (P4 editorial pairing + P5 dashboard sans serif + R-017 font-display swap)`.
6. **Mettre à jour** `ref/passation-vague2-2026-04-26.md` avec la mention de ces 3 patches.

---

## 6. Estimation effort

- Lacune 3 (gate R-017) : ~30 min (code + 1 test)
- Lacune 1 + 2 (typography-core.md) : ~45 min (rédaction propre cohérente avec le ton existant + relecture par 1 cas)
- Tests E2E : ~30 min
- **Total** : ~2 h pour les 3 patches.

---

## 7. Articulation avec le chantier 3B (en cours)

Le chantier 3B (fonts en sélection — penseurs + designer visuel) est mené dans la session 2026-04-28. Il **ne touche pas** Phase 4. Mais ces 3 patches Phase 4 sont **complémentaires et non-redondants** : 3B oriente le choix amont des fontes, Phase 4 applique les règles d'usage des fontes choisies.

→ Tu peux exécuter ce chantier Phase 4 **en parallèle** ou **après** le chantier 3B. Pas de blocage croisé.

---

## Dernière mise à jour

2026-04-28 — Rédaction par la session menant le chantier 3B fonts. Les 3 lacunes ont été identifiées lors de la cartographie audit-slop sur la typographie. Bonne chance.
