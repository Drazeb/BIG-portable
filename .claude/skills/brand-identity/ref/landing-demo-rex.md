# REX Landing Demo (Phase 6C) — Rapport d'incohérences (Feb 2026)

## Contexte

Ce rapport documente les **5 incohérences majeures** observées entre la landing page générée en Phase 6C et les 3 batches précédents (style-tile, batch 2, batch 3) pour la marque Atelier Vermeil, session a2-b3, concept Sol Radieux.

L'objectif est de permettre à la session d'optimisation de comprendre **précisément** chaque problème, de le **vérifier visuellement** dans les fichiers, et d'implémenter les **correctifs structurels** dans le prompt 6C du SKILL.md.

---

## Fichiers à examiner

Tous dans le dossier :
```
.claude/skills/brand-identity/outputs/les-vermeil-a2-b3/
```

| Fichier | Rôle | Taille |
|---------|------|--------|
| `les-vermeil-style-tile-concept-1.html` | Batch 1 — Triptyque (Voice + Artefact + Atmosphere) | 4.5 MB |
| `les-vermeil-batch2-sol-radieux.html` | Batch 2 — Logotype + Iconographie + Data Viz | ~1 MB |
| `les-vermeil-batch3-sol-radieux.html` | Batch 3 — Direction Photo + Composition + Illustration | ~90 KB |
| `les-vermeil-landing-sol-radieux.html` | **Landing Demo — le fichier problématique** | ~90 KB |

Pour les logos SVG (problème #2) :
```
les-vermeil-logo-sol-radieux.svg              (104 613 octets)
les-vermeil-logo-sol-radieux-lockup-secondaire.svg  (104 984 octets)
```

---

## Problème #1 — Atmosphère générale inversée (sombre au lieu de clair)

### Le problème

Les 3 batches ont une atmosphère **lumineuse, chaude, crème**. Le fond dominant est `--color-surface: #FEF9EF` (beige clair chaud). Le sombre (`--color-depth: #1C1917`) est utilisé uniquement pour quelques sections d'accent.

La landing fait **l'inverse** : les sections majeures (Hero, Process, Data/Impact, Manifesto, Footer) sont toutes sur fond `--color-depth` (#1C1917 noir). Le crème n'apparaît que dans les sections secondaires.

### Où observer le problème

**Style-tile** (ligne 79) :
```css
body {
    background: var(--color-surface);  /* #FEF9EF — crème chaud */
}
```
Le style-tile est entièrement sur fond crème. Les 3 blocs (Voice, Artefact, Atmosphere) vivent sur ce fond clair.

**Batch 3** — comptage des occurrences :
- `background: var(--color-surface)` → **~19 occurrences**
- `background: var(--color-depth)` → **~7 occurrences** (sections accent uniquement)
- Ratio 3:1 en faveur du clair.

**Landing** (fichier problématique) — lignes CSS à examiner :
```
Ligne 213:  .hero { background: var(--color-depth); }
Ligne 398:  .trust-bar { background: var(--color-depth); }
Ligne 563:  .process { background: var(--color-depth); }
Ligne 668:  .impact { background: var(--color-depth); }
Ligne 820:  .manifesto { background: var(--color-depth); }
Ligne 1144: .footer { background: var(--color-depth); }
```
→ **8 sections majeures sur fond sombre** vs 7 sections sur fond clair.

**L'exemple landing** (`examples/landing-demo-example.html`) est aussi sur fond clair :
```css
body { background: var(--color-surface); }
```

### Pourquoi c'est arrivé

**Cause 1 — Biais "landing page" du LLM** : Les landing pages modernes dans les données d'entraînement utilisent massivement des hero sombres et des alternances dark/light. Sans directive explicite, le LLM gravite vers ce pattern.

**Cause 2 — Anti-contamination mal calibrée** : Le prompt dit "NE COPIE PAS les choix formels de l'exemple". L'exemple est clair → le subagent a interprété ça comme un signal pour aller vers le sombre. L'anti-contamination visait les layouts/animations, mais le subagent l'a appliquée à l'atmosphère aussi.

**Cause 3 — Instruction manquante** : Le prompt transmet les tokens atomiques (`:root` identique) et les patterns de layout, mais **JAMAIS le registre atmosphérique dominant**. Le `:root` contient à la fois `--color-surface` et `--color-depth` — sans guidance sur leur proportion d'usage, le subagent choisit librement. Le champ sémantique du brief ("ombres chaudes", "strates géologiques", "sol fertile") a pu pousser vers le sombre.

### Correctif proposé

Ajouter au prompt 6C une section `## REGISTRE ATMOSPHÉRIQUE` :
```
## REGISTRE ATMOSPHÉRIQUE — OBLIGATOIRE

L'atmosphère dominante de cette identité est CLAIRE.
Le fond principal est var(--color-surface) (#FEF9EF — crème chaud).

Règles :
- body { background: var(--color-surface) } — OBLIGATOIRE
- MAXIMUM 2 sections sur 9 peuvent utiliser --color-depth comme fond (typiquement : Manifesto + Footer)
- Les 7 autres sections vivent sur --color-surface ou --color-surface-alt
- Le Hero est sur fond CLAIR avec le texte en --color-depth (pas l'inverse)

Ce registre est extrait des 3 batches précédents qui sont tous surface-dominant.
L'anti-contamination ne s'applique PAS au registre atmosphérique — il doit être COHÉRENT avec les batches.
```

L'orchestrateur devrait aussi extraire automatiquement le ratio surface/depth des batches et le passer explicitement.

---

## Problème #2 — Logo non embedé (substitut simplifié)

### Le problème

Le Batch 2 (section 05) contient le **vrai logo** de la marque : un lettermark A en 4 strates colorées (or #D97706, noir #1C1917, terracotta #B45309, crème #FEF9EF), vectorisé via vtracer avec des paths fidèles au PNG Midjourney original.

La landing affiche un **logo de substitution** : un triangle simplifié de 36×36px qui ne ressemble pas au vrai logo. On le voit dans la Nav (ligne 1304) et le Footer (ligne 1834).

### Où observer le problème

**Le vrai logo** (SVG 104 KB) :
- Fichier : `les-vermeil-logo-sol-radieux.svg`
- Structure : 6 `<path>` avec des milliers de coordonnées de courbes de Bézier
- ViewBox : `250 140 1550 1760`
- Produit par vtracer (auto-trace bitmap → SVG)

**Le logo de substitution dans la landing** (lignes 1304-1312) :
```html
<!-- Logo simplifie — A stylise alchimiste -->
<svg width="36" height="36" viewBox="0 0 100 100" fill="none">
    <!-- Triangle basique, ~10 points de coordonnées -->
</svg>
```
→ Rien à voir avec le vrai logo.

### Pourquoi c'est arrivé

**Cause — Limitation de l'outil Read** : Les SVG vtracer font 104 KB (~47 000 tokens chacun). L'outil Read a une limite de 25 000 tokens par fichier. Quand le subagent a tenté de lire les fichiers SVG, il a reçu l'erreur `File content exceeds maximum allowed tokens`. Il n'a eu aucun accès au contenu réel du logo et a dû improviser un substitut.

Ce n'est pas un raccourci du subagent — c'est une **impossibilité technique**. L'outil ne peut pas lire ces fichiers.

### Correctif proposé

Adopter le **même pattern que pour les images base64** — injection en post-processing :

1. Le subagent insère un placeholder : `<!-- PLACEHOLDER:LOGO_NAV -->` et `<!-- PLACEHOLDER:LOGO_FOOTER -->`
2. L'orchestrateur lit le SVG (il n'a pas la même limite de tokens) et l'injecte via Python :
   ```python
   with open('logo.svg') as f: logo = f.read()
   html = html.replace('<!-- PLACEHOLDER:LOGO_NAV -->', logo)
   ```

Alternative : l'orchestrateur pré-génère une version optimisée du logo (supprimer les points redondants dans les paths via un simplificateur SVG) pour passer sous la limite de 25K tokens.

---

## Problème #3 — Images base64 non détectées et non propagées

### Le problème

Le style-tile contient **2 images photographiques** en base64 (c'est ce qui explique sa taille de 4.5 MB). Ces images ont été fournies par l'utilisateur en Phase 3B (références visuelles) et intégrées dans le style-tile en Phase 4 avec des overlays CSS.

La landing n'utilise **aucune image** — que des gradients CSS. Les zones Hero et Manifesto, qui devraient montrer la direction photographique en contexte réel, sont vides de contenu photographique.

### Où observer le problème

**Les images dans le style-tile** :
- Ligne 1171 : image dans `.voice-block__image-col` — c'est l'image du Voice Block (Hero Split)
- Ligne 1402 : image dans `.atmosphere-block__bg` — c'est l'image de fond de l'Atmosphere Block

Pour vérifier :
```bash
grep -n "data:image/png\|data:image/jpeg" les-vermeil-style-tile-concept-1.html
```
→ Retourne les lignes 1171 et 1402.

**La landing** — aucun match :
```bash
grep -n "data:image/png\|data:image/jpeg" les-vermeil-landing-sol-radieux.html
```
→ 0 résultat.

**La taille du fichier confirme** : 4 567 352 octets pour le style-tile vs ~90 000 octets pour la landing.

### Pourquoi c'est arrivé

**Cause — Erreur de détection par l'orchestrateur** : L'orchestrateur (moi) a exécuté un `Grep` en mode `count` pour chercher `data:image/` dans le style-tile. Le résultat affiché était :
```
3
Found 0 total occurrences across 0 files.
```
L'output était **ambigu** (le "3" et le "Found 0" semblent contradictoires). J'ai interprété ça comme 0 images et j'ai envoyé `{images_present}` = false au subagent. En réalité il y avait 2 images.

**Erreur d'orchestration complémentaire** : Le fichier fait 4.5 MB. Un check de taille (`wc -c`) aurait immédiatement révélé la présence d'images (un HTML sans images fait rarement plus de 200 KB). Cette vérification de bon sens n'a pas été faite.

### Correctif proposé

Fiabiliser la détection des images dans le protocole 6C-A :

1. **Check primaire par taille** : Si le fichier > 200 KB → `{images_present}` = true (sans même chercher dans le contenu).
2. **Check secondaire par Grep en mode content** (pas count) : Grep `data:image/(png|jpeg)` en mode `content` avec `-B 3` pour identifier les classes parentes.
3. **Ajouter ces 2 checks en séquence** dans le SKILL.md, section "Étape 6C-A".

---

## Problème #4 — Icônes recréées au lieu d'être copiées

### Le problème

Le Batch 2 (section 06.4) contient **8 icônes métier SVG** soigneusement dessinées avec le bon angle du sillon (~15-25°), les bons stroke-weights (1.5/2/2.5px), les bons radius mixtes (sharp 4px + soft 16px), et la bonne palette.

La landing contient 8+ icônes SVG, mais elles sont **recréées from scratch** par le subagent. Elles ne correspondent pas aux icônes du Batch 2 — ni en forme, ni en proportions, ni en détails.

### Où observer le problème

**Les icônes du Batch 2** — section 06.4, lignes ~960-1100 :
- 8 icônes métier en cards : Collecte, Compostage, Traçabilité, Lavage, Logistique, Insertion, Impact, Circuit court
- Chaque icône est un SVG inline avec des paths spécifiques
- Style cohérent : angle du sillon hérité du logo, stroke 2px, caps arrondis

**Les icônes de la landing** — sections Services (lignes ~1473-1510) et Process (lignes ~1546-1640) :
- SVGs génériques de 28×28px créés par le subagent
- Formes différentes, proportions différentes, angles différents
- Pas d'héritage du sillon du logo

Pour comparer : ouvrir le Batch 2 et la landing côte à côte dans le navigateur, section icônes.

### Pourquoi c'est arrivé

**Cause — Gap dans le protocole d'extraction 6C-A** : Le protocole d'extraction passe des **descriptions textuelles** des icônes au subagent, pas le code SVG réel :

> "Style: Three registers — Outline (2px stroke, caps arrondis), Solid (fill primaire)..."

Le subagent n'a jamais vu le SVG réel des icônes du Batch 2. Il a recréé des icônes à partir de la description textuelle — ce qui produit inévitablement des résultats différents.

### Correctif proposé

Modifier le protocole 6C-A pour extraire le **code SVG complet** des 8 icônes du Batch 2 :

1. Grep `06.4` ou `DA Illustrative` dans le Batch 2 → trouver la section
2. Read de cette section → extraire chaque bloc `<svg>...</svg>` des 8 icônes
3. Passer ces 8 SVGs VERBATIM au subagent dans la variable `{icon_svgs}`
4. Le subagent EMBED ces SVGs tels quels au lieu d'en créer de nouveaux

Les icônes font quelques centaines d'octets chacune — aucun problème de taille.

---

## Problème #5 — Composants CSS non cohérents (cards, sections)

### Le problème

Au-delà des tokens atomiques (`:root`), les batches utilisent des patterns de composants CSS spécifiques : styles de cards, arrondis de sections, traitements de bordures, patterns de hover. La landing a ses propres styles de composants qui ne correspondent pas.

### Où observer le problème

**Batch 2** — cards icônes (section 06.4) : chercher les classes `.icon-style-card`, `.da-card` dans le Batch 2. Observer le padding, le border-radius, le background, le box-shadow.

**Batch 3** — cards composition (section 09.3) : chercher `.pattern-card`, `.mood-card`. Observer les traitements.

**Landing** — comparer les `.bento-card` (ligne 527+) :
```css
.bento-card {
    border-radius: var(--radius-sharp);  /* 4px */
    /* ... */
}
```

Les batches peuvent utiliser des combinaisons différentes (sharp en haut, soft en bas, ou l'inverse). Les hover states, les transitions, les pseudo-éléments décoratifs sont aussi différents.

### Pourquoi c'est arrivé

**Cause — Seuls les tokens atomiques sont partagés, pas les composants** : Le protocole 6C-A extrait le bloc `:root` (palette, fonts, radius, shadows) et le passe au subagent. Mais il n'extrait pas les **styles de composants** des batches. Le subagent crée donc ses propres composants CSS à partir des tokens — cohérents en tokens mais pas en patterns de composition.

### Correctif proposé

Ajouter au protocole 6C-A l'extraction de **3-4 patterns de composants clés** :

1. **Card standard** : border-radius, padding, shadow, background du type `.card` le plus fréquent dans les batches
2. **Section sombre** : le traitement exact des sections sur fond `--color-depth` (gradient meshes, pseudo-éléments)
3. **Hover state** : le pattern de hover commun (transition, transform, shadow change)
4. **Séparateur** : le gradient-separator utilisé entre les sections

Ces patterns font quelques lignes CSS chacun — aucun coût en tokens.

---

## Synthèse

| # | Problème | Type | Cause racine | Difficulté du fix |
|---|----------|------|-------------|-------------------|
| 1 | Atmosphère sombre au lieu de claire | **Gap de spécification** | Aucune consigne sur le registre atmosphérique dans le prompt | Facile — ajouter une section au prompt |
| 2 | Logo de substitution (36px triangle) | **Limitation outil** | SVG 104KB > limite Read 25K tokens | Moyen — ajouter étape post-processing |
| 3 | Images non détectées / non propagées | **Erreur orchestrateur** | Grep count mode ambigu + pas de check taille | Facile — fiabiliser la détection |
| 4 | Icônes recréées au lieu de copiées | **Gap protocole extraction** | Descriptions textuelles au lieu de code SVG | Facile — extraire les SVGs verbatim |
| 5 | Composants CSS incohérents | **Gap protocole extraction** | Tokens partagés mais pas les patterns composants | Moyen — extraire 3-4 patterns CSS |

**Aucun de ces problèmes n'est lié à un manque de performance ou à un raccourci du subagent.** Le subagent a produit 1 915 lignes de code HTML/CSS avec 16 radial-gradients, 24 pseudo-éléments et 2 animations SVG. L'effort technique est là. Les lacunes viennent exclusivement de **données manquantes en entrée** (images non détectées, logo illisible, icônes non transmises) et d'un **manque de consignes** (registre atmosphérique, patterns composants).

---

*Document créé le 16 Feb 2026 — Session Atelier Vermeil a2-b3, concept Sol Radieux.*
