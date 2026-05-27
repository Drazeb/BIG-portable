# Guide Recraft V4 — Prompting pour BIG

> **Source unique** pour les prompts Recraft dans le pipeline BIG.
> Utilisé en Phase 3C (visuels de référence) pour les registres Recraft et Dual.

---

## §0 — Règle de fraîcheur

**AVANT de générer des prompts Recraft**, vérifier la version courante via WebSearch :
```
Recherche : "recraft V4 latest update 2026"
```
Si une mise à jour post-février 2026 change les modèles ou les capacités → adapter les recommandations ci-dessous. Ne JAMAIS générer de prompts Recraft avec des paramètres obsolètes.

---

## §1 — Quand utiliser Recraft (routage)

Recraft V4 est l'outil recommandé ou disponible pour **5 registres Recraft + 4 registres Dual**. Le routage se fait dans SKILL.md Phase 3C — ce guide ne décide PAS de l'outil, il fournit les instructions de prompting une fois Recraft choisi.

### Registres Recraft (systématique)

| Registre BIG | Nom | Pourquoi Recraft | Modèle |
|-------------|-----|-----------------|--------|
| **I1** | Flat / Corporate | SVG natif, lignes nettes, couleurs maîtrisées, aplats parfaits | V4 Vector |
| **I2** | Line Art | Linework propre et cohérent, traits réguliers | V4 Vector |
| **I4** | Aquarelle / Painterly | Registre illustratif/artisanal — MJ pousse vers le photoréalisme, Recraft reste en illustration | V4 Pro |
| **I7** | Infographique | Précision géométrique, aplats, données visuelles | V4 Vector / V4 Pro Vector |
| **T2** | Texture abstraite / Painterly | Textures illustratives organiques — MJ fait du marble stock, Recraft fait du painterly artisanal | V4 Pro |

### Registres Dual (choix utilisateur en Phase 3C)

| Registre BIG | Nom | Recraft si... | MJ si... | Modèle Recraft |
|-------------|-----|--------------|---------|----------------|
| **I3** | Isométrique | Illustratif, technique, schéma | Cinématique, 3D réaliste | V4 Pro |
| **I5** | Rétro / Vintage / 3D stylisé | Illustratif, stylisé, artisanal | Cinématique, photoréaliste | V4 Pro |
| **T3** | Pattern géométrique | Aplats précis, tessellation nette | Patterns texturés avec matière | V4 Vector |
| **F4** | Fond 3D / surréaliste | Illustratif, onirique, stylisé | Cinématique, photoréaliste | V4 Pro |

### Registres MidJourney exclusif

**P1-P6** (Photos), **I6** (Character), **T1** (Seamless), **F1-F3** (Food/Mockup/UI) → MidJourney. Voir `midjourney-prompting-guide.md`.

### Phase Logo — Recraft par défaut

**Recraft V4 Vector** est l'outil par défaut pour la Phase Logo. Sur les registres géométriques (L1 Geometric Abstract, L2 Lettermark simple), Recraft produit des formes plus nettes, plus contemporaines et plus géométriquement précises que MJ (qui a un biais "organic blob" sur les formes abstraites). L'utilisateur peut demander MJ à la place — dans ce cas, suivre `midjourney-prompting-guide.md` registres L1-L6.

**Règle critique** : quel que soit l'outil, le prompt DOIT respecter TOUTES les couches/paramètres du framework correspondant (7 couches Recraft §4, ou paramètres MJ §5). Un prompt incomplet = résultats dégradés.

---

## §2 — Les 4 variantes V4

| Modèle | Résolution | Vitesse | Usage BIG recommandé |
|--------|-----------|---------|---------------------|
| **V4** | 1024×1024 | ~10s | Itération rapide, exploration de directions |
| **V4 Vector** | Standard | ~15s | **Usage principal BIG** — illustrations flat/vector, icônes |
| **V4 Pro** | 2048×2048 | ~28s | Rendu final haute résolution (si nécessaire) |
| **V4 Pro Vector** | Haute résolution | ~45s | SVG haute fidélité pour branding/packaging |

**Recommandation BIG** :
- **Exploration** → V4 (rapide, 10s)
- **Rendu final registre I1/I2** → V4 Vector (SVG natif)
- **Rendu final registre I4/T2** → V4 Pro (painterly haute résolution)
- **Rendu final registre I7** → V4 Vector ou V4 Pro Vector (précision géométrique)
- **Rendu final registres Dual (I3/I5/T3/F4)** → V4 Pro (illustratif) ou V4 Vector (technique/plat)

---

## §3 — Principes fondamentaux

Recraft fonctionne différemment de MidJourney. Le prompt est plus court, plus naturel, et le modèle prend des décisions esthétiques autonomes ("design taste").

### 3.1 Clarté
Écrire comme on décrirait une scène à une personne. Langage conversationnel, pas de keyword stuffing.
- **Bon** : *"A mountain lake at sunrise, surrounded by pine trees and soft mist."*
- **Mauvais** : *"lake mountains mist sunrise pines ethereal dreamy 4K"*

L'ordre des mots compte : sujet principal en premier, puis environnement, puis ambiance.

### 3.2 Structure
Regrouper les concepts liés : sujet, puis composition, puis style. Pas d'instructions éparpillées.

### 3.3 Précision
Chaque détail inclus guide le modèle. Plus de spécificité ≠ toujours mieux — l'enjeu est de savoir **quels détails comptent** et lesquels laisser au modèle.

### 3.4 Différence clé avec MJ
| Aspect | MidJourney | Recraft V4 |
|--------|-----------|-----------|
| Prompt optimal | Long, détaillé, paramétré | Court à moyen, naturel |
| Paramètres techniques | `--style`, `--stylize`, `--ar`, `--no` | Aucun paramètre inline — tout dans le prompt |
| Negative prompt | `--no` dans le prompt | **Pas de négation** — décrire ce qu'on veut uniquement |
| Style | Via `--style` + `--sref` | Via le choix du modèle (Vector, Pro) + prompt |
| Palette | HEX intégrés dans le prompt | HEX intégrés dans le prompt (identique) |

---

## §4 — Template universel : 7 couches visuelles

```
[SUJET + ACTION], [COMPOSITION], [CONTEXTE], [MEDIUM], [STYLE], [VIBE], [ATTRIBUTS]
```

### Les 3 couches fondamentales (obligatoires)

| Couche | Rôle | Exemple |
|--------|------|---------|
| **Sujet** | Ce qui est représenté + action/position | *"Geometric network of interconnected nodes"* |
| **Composition** | Cadrage, angle, placement | *"Centered in frame"*, *"isometric view"*, *"rule of thirds"* |
| **Contexte** | Environnement / arrière-plan | *"Clean white background"*, *"soft gradient backdrop"* |

### Les 4 couches artistiques (optionnelles mais recommandées)

| Couche | Rôle | Exemple |
|--------|------|---------|
| **Medium** | Technique de rendu | *"Flat vector illustration"*, *"line art drawing"* |
| **Style** | Esthétique visuelle | *"Modern corporate"*, *"Japanese minimalist"* |
| **Vibe** | Émotion / atmosphère | *"Professional and trustworthy"*, *"playful and energetic"* |
| **Attributs** | Couleurs, éclairage, textures | *"Muted blue and warm gray palette"*, *"clean outlines"* |

---

## §5 — Prompting par type BIG

### I1 — Illustration Flat / Corporate

**Modèle recommandé** : V4 Vector

**Mots-clés efficaces** : *flat vector illustration*, *simple geometric shapes*, *clean lines*, *solid colors*, *bold outlines*, *modern graphic style*, *minimal design*.

**3 niveaux de détail** :

| Niveau | Quand | Prompt type |
|--------|-------|-------------|
| Minimal | Exploration | *"Flat vector illustration of [sujet], simple geometric shapes, [palette], clean lines, minimal design"* |
| Descriptif | Direction confirmée | *"Flat vector illustration of [sujet] with [éléments], geometric [formes], bold outlines, modern graphic style, [palette]"* |
| Détaillé | Rendu final | *"Detailed flat vector illustration of [sujet], [composition], [éléments détaillés], contemporary poster design, [palette complète avec HEX]"* |

**Palette BIG** : Toujours intégrer 2-3 couleurs HEX du :root du concept dans le prompt.
Exemple : *"rich color palette with deep navy #1A1A2E, warm terracotta #E2725B, and soft cream #F5F0EB"*

### I2 — Line Art

**Modèle recommandé** : V4 Vector

**Mots-clés efficaces** : *line art*, *bold line work*, *consistent stroke width*, *monoline style*, *clean outlines*, *pen and ink technique*.

**Template** :
```
Line art illustration of [sujet], [composition], bold line work with consistent stroke width,
[fond : white/colored], monoline style, [palette si nécessaire], clean and minimal
```

**Point d'attention** : Pour le line art monochromatique, spécifier explicitement *"single color [HEX] on white background"* — sinon V4 ajoutera des couleurs.

### I7 — Infographique

**Modèle recommandé** : V4 Vector ou V4 Pro Vector

**Mots-clés efficaces** : *infographic*, *data visualization*, *clean layout*, *geometric shapes*, *organized grid*, *professional chart*, *structured information design*.

**Template** :
```
[Type d'infographie : timeline / process / comparison / stats] infographic,
[sujet et données], structured layout with [composition],
flat vector style, [palette HEX], clean professional design
```

**Point d'attention** : Recraft V4 comprend la typographie comme élément structurel — les chiffres et labels seront intégrés proprement dans la composition (pas plaqués en overlay).

### I4 — Aquarelle / Painterly

**Modèle recommandé** : V4 Pro

**Mots-clés efficaces** : *painterly illustration*, *watercolor style*, *organic flowing forms*, *soft washes*, *artistic brushstrokes*, *hand-painted aesthetic*, *layered translucent colors*.

**Template** :
```
Painterly illustration of [sujet], [composition], soft organic brushstrokes,
[palette HEX intégrée], [ambiance/vibe], warm artistic quality,
layered translucent washes on [fond]
```

**Point d'attention** : Recraft V4 Pro produit un registre illustratif/artisanal naturellement — PAS de photoréalisme. C'est l'avantage principal sur MJ pour ce registre. Ne pas forcer le réalisme : laisser le "design taste" de V4 travailler. Décrire l'ambiance et la palette, pas les techniques de peinture.

**Piège à éviter** : "watercolor painting" peut pousser vers un rendu trop classique. Préférer "painterly illustration" pour un résultat plus contemporain.

### T2 — Texture Abstraite / Painterly

**Modèle recommandé** : V4 Pro

**Mots-clés efficaces** : *abstract organic forms*, *flowing geological strata*, *layered texture*, *fluid composition*, *artistic abstract*, *painterly surface*, *natural formations*.

**Template** :
```
Abstract painterly composition of [sujet/forme], [palette HEX intégrée],
[composition : flowing/layered/fragmented], organic texture,
artistic quality, [fond]
```

**Point d'attention** : V4 Pro excelle à produire des textures qui restent illustratives (artisanales, organiques) là où MJ glisse vers du marble stock photoréaliste. Pour des textures chaleureuses et artisanales, Recraft est systématiquement supérieur.

### Registres Dual — I3, I5, T3, F4

Ces registres sont routés vers Recraft quand l'utilisateur choisit le rendu illustratif/stylisé (voir Phase 3C SKILL.md).

**Modèle recommandé** : V4 Pro (illustratif) ou V4 Vector (technique/plat)

**Principes communs** :
- Utiliser le même template 7 couches (§4) — sujet, composition, contexte, medium, style, vibe, attributs
- Palette HEX toujours intégrée
- Décrire le RÉSULTAT visuel, pas la technique de construction
- Le medium doit être explicite : *"stylized illustration"*, *"technical illustration"*, *"artistic render"*

**Par registre** :
- **I3 Isométrique** : *"stylized isometric illustration"*, *"technical diagram style"*, *"clean architectural drawing"*. V4 Pro pour le stylisé, V4 Vector pour le technique pur.
- **I5 Rétro/3D stylisé** : *"stylized artistic render"*, *"illustrated object"*, *"hand-crafted aesthetic"*. Toujours V4 Pro.
- **T3 Pattern géométrique** : *"precise geometric pattern"*, *"tessellation"*, *"mathematical grid"*. V4 Vector recommandé (précision des aplats).
- **F4 Fond surréaliste** : *"illustrated dreamscape"*, *"surreal landscape illustration"*, *"impossible architecture"*. Toujours V4 Pro.

---

## §6 — Limitations V4 et stratégies de compensation

| Limitation | Impact | Compensation |
|-----------|--------|-------------|
| **Pas de negative prompt** | Impossible d'exclure des éléments | Décrire précisément ce qu'on veut — ne pas mentionner ce qu'on ne veut pas |
| **Pas de `--style` / `--stylize`** | Pas de contrôle de fidélité | Ajuster la spécificité du prompt |
| **Pas de styles custom** | Pas de réutilisation cross-session | Répéter les éléments de style dans chaque prompt |
| **Pas de negative prompt** | Un élément indésirable persiste | Ne JAMAIS écrire "no X" ou "without Y" — reformuler positivement |

### Arbre de décision : élément indésirable

1. **Reformuler** : décrire uniquement ce qu'on veut, sans mentionner l'élément
2. **Préciser** : ajouter plus de détail sur la composition et le contexte
3. **Fallback MJ** : si le problème persiste → basculer sur MidJourney avec `--no`

---

## §7 — Checklist avant génération (prompt Recraft BIG)

Avant de finaliser un prompt Recraft pour le brief visuel, vérifier :

- [ ] **Sujet** décrit clairement avec position/action
- [ ] **Composition** spécifiée (cadrage, angle, placement)
- [ ] **Medium** déclaré (*"flat vector illustration"*, *"line art"*, etc.)
- [ ] **Palette HEX** du concept intégrée (2-3 couleurs dominantes)
- [ ] **Modèle V4** spécifié (V4 / V4 Vector / V4 Pro / V4 Pro Vector)
- [ ] **Zéro négation** — pas de "no", "without", "not" dans le prompt
- [ ] **Nombres précis** plutôt que des pluriels vagues (*"three icons"* pas *"icons"*)
- [ ] **Phrases naturelles** — pas de keyword stuffing
- [ ] **Vibe/ambiance** si l'émotion est un enjeu
- [ ] **Taille de prompt** : court à moyen (V4 comprend mieux les prompts concis)

---

## §8 — Erreurs courantes

| Erreur | Pourquoi ça échoue | Solution |
|--------|-------------------|----------|
| Négation ("no X", "without Y") | V4 interprète le mot-clé, pas la négation | Ne pas mentionner l'élément du tout |
| Keyword stuffing | Le modèle s'embrouille avec trop de mots isolés | Écrire des phrases naturelles complètes |
| Prompt trop long et directif | V4 fonctionne mieux avec des prompts concis | Laisser le "design taste" de V4 travailler |
| Ambiguïté des noms | "Bat" = chauve-souris ou batte ? | Ajouter du contexte : *"a flying bat in the night sky"* |
| Style redéfini dans chaque prompt | Incohérence entre les visuels d'un même concept | Garder les mêmes éléments de style pour tous les prompts d'un concept |
| Pluriel vague | "des formes" — combien ? | Spécifier le nombre : *"five geometric shapes"* |
| Mélange sujet + construction géométrique | "Un triangle fait de rectangles empilés" | Décrire ce qu'on VOIT, pas comment c'est construit |

---

## §9 — Format de prompt dans le brief visuel BIG

Quand un prompt Recraft est inclus dans `{brand}-visual-brief.md`, il suit ce format :

```
**Image N — {description courte}**
Registre : {code} {nom} · Outil : Recraft · Modèle : {V4 Vector / V4 Pro Vector}

```
[prompt complet en langage naturel, palette HEX intégrée, composition et medium spécifiés]
```
```

Pas de paramètres techniques à la fin (contrairement à MJ qui a `--ar`, `--style`, etc.). Le prompt est autonome.

---

*Dernière mise à jour : mars 2026*
*Source : documentation officielle Recraft (guide prompt engineering, nov 2025 / mise à jour fév 2026), retours praticiens Reddit, analyses Imagine.Art et Freepik.*
