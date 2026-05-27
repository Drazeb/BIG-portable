# REX Lockup SVG — Technique mark + texte (Feb 2026)

## Contexte

Ce document décrit la méthode fiable pour générer des lockups SVG (logo mark + nom de marque en texte) à partir d'un SVG vectorisé via vtracer. Il complète `logo-vectorization-rex.md` (vectorisation PNG → SVG) avec l'étape suivante : l'assemblage mark + texte dans des compositions lockup.

---

## Problème 1 — Scale transforms sur paths vtracer (TOUJOURS ÉCHOUE)

### Le piège

Les paths générés par vtracer ont cette structure :

```xml
<path d="M0 0 C..." fill="#D97706" transform="translate(884.9, 396.8)"/>
<path d="M0 0 C..." fill="#1C1917" transform="translate(947, 674)"/>
```

Chaque path commence à `M0 0` dans son espace local, puis est positionné via `translate(x, y)` dans l'espace global 2048×2048.

L'approche **naïve** pour créer un lockup est d'envelopper les paths dans un `<g transform="scale(...)">` :

```xml
<!-- ❌ NE PAS FAIRE ÇA -->
<svg viewBox="0 0 500 430">
  <g transform="scale(0.283)">
    <path ... transform="translate(884.9, 396.8)"/>
    <!-- etc. -->
  </g>
  <text>ATELIER VERMEIL</text>
</svg>
```

### Pourquoi ça échoue

Le `scale()` s'applique à TOUT dans le `<g>`, y compris les `translate()` des paths. Donc :

- `translate(884.9, 396.8)` avec `scale(0.283)` → position effective `(250.4, 112.3)`
- Mais le scale affecte aussi les coordonnées du `d=""` → les paths sont compressés ET déplacés
- Le résultat est imprévisible : le mark se retrouve dans un coin, trop gros ou trop petit, décalé par rapport au texte

### Résultats observés (3 tentatives)

| Tentative | Transform | Résultat |
|-----------|-----------|----------|
| `scale(0.283)` | Lockup primaire | Mark massif, déborde, texte écrasé sous le mark |
| `scale(0.075)` | Lockup secondaire | Mark minuscule à gauche, texte disproportionné |
| `translate(-5,0) scale(0.283)` | Ajustement manuel | Légèrement mieux mais proportions fausses |

**Conclusion : NE JAMAIS utiliser `<g transform="scale(...)">` sur des paths vtracer avec des `translate()` embarqués.**

---

## Problème 2 — ViewBox trop large (padding invisible)

### Le piège

Le SVG vectorisé a un viewBox calculé avec ~5-10% de padding autour des paths :

```xml
<svg viewBox="250 140 1550 1760">  <!-- viewBox du SVG original -->
```

Mais les paths n'occupent pas tout cet espace. En calculant les bornes réelles des paths (via parsing des coordonnées `d=""` + `translate()`), on découvre :

```
ViewBox:          x:[250, 1800]  y:[140, 1900]  → 1550 × 1760
Contenu réel:     x:[445, 1601]  y:[397, 1661]  → 1156 × 1264
Taux de remplissage: 75% en X, 72% en Y
```

Conséquence : quand on alloue une boîte de 70×80px au mark dans un lockup, le mark visible ne fait en réalité que **50×57px** (72% de l'espace). Le texte à côté paraît disproportionnément grand.

---

## La solution qui fonctionne : `<svg>` imbriqué + viewBox serré

### Principe

Au lieu d'appliquer des transforms aux paths, on les encapsule dans un **`<svg>` imbriqué** avec son propre `viewBox`. Le SVG imbriqué gère automatiquement le mapping de coordonnées — aucun calcul de scale/translate nécessaire.

```xml
<!-- ✅ MÉTHODE CORRECTE -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 410">
  <svg x="111" y="25" width="238" height="260" viewBox="410 359 1225 1340">
    <!-- Les paths vtracer tels quels, sans modification -->
    <path d="M0 0 C..." fill="#D97706" transform="translate(884.9, 396.8)"/>
    <path d="M0 0 C..." fill="#1C1917" transform="translate(947, 674)"/>
    <!-- etc. -->
  </svg>
  <text x="230" y="358" text-anchor="middle" ...>ATELIER VERMEIL</text>
</svg>
```

### Pourquoi ça marche

1. Le `<svg>` imbriqué a son propre `viewBox` qui définit le système de coordonnées interne
2. Les attributs `x`, `y`, `width`, `height` du SVG imbriqué définissent la **boîte de destination** dans le SVG parent
3. Le navigateur mappe automatiquement le viewBox interne vers la boîte de destination
4. Les paths + leurs `translate()` restent INTACTS — aucune modification
5. Le `<text>` vit dans le SVG parent, à côté du SVG imbriqué, avec des coordonnées simples

### Les 2 étapes obligatoires

#### Étape 1 — Calculer le viewBox serré (tight viewBox)

Le viewBox du SVG imbriqué ne doit PAS être celui du SVG original (trop de padding). Il faut calculer les bornes réelles des paths :

```python
import re

with open('logo.svg', 'r') as f:
    content = f.read()

# Extraire les paths avec leurs translate
path_data = re.findall(
    r'<path d="([^"]+)"[^>]*transform="translate\(([^)]+)\)"', content
)

all_x, all_y = [], []

for d, translate in path_data:
    tx, ty = [float(v) for v in translate.split(',')]

    # Parser les coordonnées du d=""
    tokens = re.findall(
        r'[MLCQSTAZmlcqstaz]|[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', d
    )

    i, x, y, cmd = 0, 0, 0, 'M'
    while i < len(tokens):
        if tokens[i].isalpha():
            cmd = tokens[i]
            i += 1
            continue
        try:
            if cmd in ('M', 'L'):
                x, y = float(tokens[i]), float(tokens[i+1])
                all_x.append(tx + x); all_y.append(ty + y)
                i += 2
                if cmd == 'M': cmd = 'L'
            elif cmd == 'C':
                for j in range(3):
                    cx = float(tokens[i + j*2])
                    cy = float(tokens[i + j*2 + 1])
                    all_x.append(tx + cx); all_y.append(ty + cy)
                x, y = float(tokens[i+4]), float(tokens[i+5])
                i += 6
            elif cmd in ('Z', 'z'):
                break
            else:
                i += 1
        except (IndexError, ValueError):
            break

min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)

# Ajouter 3% de padding
pad_x = (max_x - min_x) * 0.03
pad_y = (max_y - min_y) * 0.03

tight_viewbox = (
    f"{min_x - pad_x:.0f} {min_y - pad_y:.0f} "
    f"{max_x - min_x + 2*pad_x:.0f} {max_y - min_y + 2*pad_y:.0f}"
)
aspect_ratio = (max_x - min_x) / (max_y - min_y)

print(f"Tight viewBox: {tight_viewbox}")
print(f"Aspect ratio: {aspect_ratio:.3f}")
```

Ce script produit un viewBox comme `"410 359 1225 1340"` au lieu de `"250 140 1550 1760"` — le mark remplit maintenant ~97% de la boîte au lieu de ~72%.

#### Étape 2 — Construire le lockup avec le SVG imbriqué

Script Python complet pour générer les 2 lockups :

```python
import re

with open('logo.svg', 'r') as f:
    original = f.read()

# Extraire les <path .../> tels quels
paths = re.findall(r'<path [^>]+/>', original)
paths_str = '\n'.join(paths)

# ┌─────────────────────────────────────────────────┐
# │ VARIABLES À ADAPTER PAR SESSION                  │
# ├─────────────────────────────────────────────────┤
tight_vb = "410 359 1225 1340"  # ← calculé à l'étape 1
aspect = 1225 / 1340            # ← largeur / hauteur du tight_vb
brand_name = "ATELIER VERMEIL"  # ← en capitales
font_family = "'Fraunces', Georgia, serif"
font_import = "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&amp;display=swap"
fill_color = "#1C1917"          # ← --color-depth du :root
# └─────────────────────────────────────────────────┘

# === LOCKUP PRIMAIRE (vertical : mark au-dessus, texte en-dessous) ===
#
# Proportions recommandées :
#   - Mark : ~60-65% de la hauteur totale
#   - Gap mark→texte : ~10-12% de la hauteur totale
#   - Texte : ~8% de la hauteur totale (font-size)
#   - Padding bottom : ~15%
#
mark_h_v = 260                            # hauteur du mark
mark_w_v = round(mark_h_v * aspect)       # largeur (proportionnelle)
vb_w_v = max(mark_w_v + 100, 400)         # largeur viewBox (mark + marges)
vb_h_v = 410                              # hauteur viewBox totale
mark_x_v = round((vb_w_v - mark_w_v) / 2) # centrage horizontal
mark_y_v = 25                             # padding top
gap_v = 45                                # espace mark → texte
text_y_v = mark_y_v + mark_h_v + gap_v + 28  # baseline texte

lockup_v = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w_v} {vb_h_v}">
<defs><style>@import url('{font_import}');</style></defs>
<title>{brand_name} — Lockup Primaire</title>
<svg x="{mark_x_v}" y="{mark_y_v}" width="{mark_w_v}" height="{mark_h_v}" viewBox="{tight_vb}">
{paths_str}
</svg>
<text x="{vb_w_v // 2}" y="{text_y_v}" text-anchor="middle" font-family="{font_family}" font-weight="700" font-size="36" fill="{fill_color}" letter-spacing="4">{brand_name}</text>
</svg>'''

# === LOCKUP SECONDAIRE (horizontal : mark à gauche, texte à droite) ===
#
# Proportions recommandées :
#   - Mark : ~90% de la hauteur du viewBox
#   - Texte font-size : ~30% de la hauteur du viewBox (≈ 1/3 du mark)
#   - Gap mark→texte : ~18-20% de la largeur du mark
#   - Baseline texte : alignée à ~72% de la hauteur du mark
#
# ATTENTION Fraunces 700 :
#   - Cap-height très élevée (~75% du font-size vs ~70% standard)
#   - Visuellement les capitales paraissent plus grandes qu'attendu
#   - Compenser en réduisant le font-size à ~30% du viewBox height
#     (au lieu de 35-40% pour une police standard)
#
vb_h_h = 80                               # hauteur viewBox
mark_h_h = 72                             # mark = 90% de la hauteur
mark_w_h = round(mark_h_h * aspect)       # largeur proportionnelle
mark_x_h = 8                              # padding gauche
mark_y_h = round((vb_h_h - mark_h_h) / 2)  # centrage vertical
text_x_h = mark_x_h + mark_w_h + 14      # gap mark → texte
text_y_h = mark_y_h + round(mark_h_h * 0.72)  # baseline à 72%
font_size_h = round(vb_h_h * 0.30)        # 30% de la hauteur = 24

# Estimer la largeur du texte
# Coefficient 0.72 (polices weight 700+ / serifs display) + letter-spacing explicite + marge sécurité 15%
letter_spacing = 2.5
text_width_est = len(brand_name) * font_size_h * 0.72 + (len(brand_name) - 1) * letter_spacing
vb_w_h = round((text_x_h + text_width_est + 15) * 1.15)  # marge sécurité 15% — un viewBox trop large est invisible, trop étroit tronque

lockup_h = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w_h} {vb_h_h}">
<defs><style>@import url('{font_import}');</style></defs>
<title>{brand_name} — Lockup Secondaire</title>
<svg x="{mark_x_h}" y="{mark_y_h}" width="{mark_w_h}" height="{mark_h_h}" viewBox="{tight_vb}">
{paths_str}
</svg>
<text x="{text_x_h}" y="{text_y_h}" font-family="{font_family}" font-weight="700" font-size="{font_size_h}" fill="{fill_color}" letter-spacing="2.5">{brand_name}</text>
</svg>'''

# Écriture
with open('lockup-primaire.svg', 'w') as f:
    f.write(lockup_v)
with open('lockup-secondaire.svg', 'w') as f:
    f.write(lockup_h)
```

---

## Paramètres de proportion — Guide par type de police

Le ratio mark/texte dépend fortement de la police utilisée. Fraunces 700 (serif variable, optical-size) a des capitales particulièrement hautes.

### Ratio mark height / font-size par police

| Police | Cap-height ratio | font-size recommandé (% viewBox height) | Résultat visuel |
|--------|-----------------|----------------------------------------|-----------------|
| Fraunces 700 | ~75% | 30% | Mark ≈ 2.5× caps |
| Source Sans 3 | ~70% | 33% | Mark ≈ 2.5× caps |
| Inter 700 | ~73% | 31% | Mark ≈ 2.5× caps |
| Playfair Display | ~68% | 34% | Mark ≈ 2.5× caps |

**Règle générale** : viser font-size = `viewBox_height × 0.30` pour le lockup horizontal. Coefficient largeur texte : `0.72 × font-size` par caractère + letter-spacing, × 1.15 marge de sécurité. Ajuster ±2-3% selon la police.

### Alignement baseline dans le lockup horizontal

La baseline du texte doit être à **72% de la hauteur du mark** (depuis le top). Cela aligne visuellement le centre optique des capitales avec le centre de gravité du mark :

```
Mark top ──────────── y = mark_y
    │
    │   72% ─────── ← baseline texte (text_y = mark_y + mark_h × 0.72)
    │
Mark bottom ───────── y = mark_y + mark_h
```

Si le mark a un centre de gravité plus bas (ex: lettre A avec la barre transversale basse), descendre à 74-76%.
Si le mark a un centre de gravité haut (ex: lettre T), monter à 68-70%.

---

## Checklist pour la génération de lockups

Avant de considérer un lockup comme terminé, vérifier :

- [ ] **Nested SVG** : Les paths sont dans un `<svg>` imbriqué, PAS dans un `<g transform="scale()">`
- [ ] **Tight viewBox** : Le viewBox du SVG imbriqué est calculé depuis les bornes réelles des paths (script Python ci-dessus), PAS copié du SVG original
- [ ] **Fill ratio** : Le mark remplit >95% de sa boîte (si <80%, le tight viewBox est mal calculé)
- [ ] **Font import** : Le `<defs><style>@import url(...)</style></defs>` est présent pour Google Fonts
- [ ] **Proportions primaire** : Le mark occupe ~60-65% de la hauteur totale, le texte ~8%
- [ ] **Proportions secondaire** : Le mark occupe ~90% de la hauteur, font-size = ~30% de la hauteur
- [ ] **Baseline** : Le texte est aligné à 72% de la hauteur du mark (lockup horizontal)
- [ ] **Centrage** : Le mark est centré horizontalement (lockup vertical) via `x = (viewBox_w - mark_w) / 2`
- [ ] **Test navigateur** : Ouvert dans Chrome, comparé visuellement

---

## Erreurs courantes à éviter

| Erreur | Conséquence | Correction |
|--------|-------------|------------|
| `<g transform="scale(0.28)">` sur paths vtracer | Mark déformé, mal positionné | Utiliser `<svg>` imbriqué |
| ViewBox du SVG original comme viewBox du nested SVG | Mark ne remplit que ~72% de sa boîte | Calculer le tight viewBox |
| `font-size="32"` avec Fraunces 700 dans un viewBox de 80px de haut | Texte visuellement aussi grand que le mark | Réduire à `font-size="24"` (30% de 80) |
| Baseline texte à 50% du mark | Texte trop haut, déséquilibre visuel | Baseline à 72% du mark |
| Oublier `@import` Google Fonts | Fallback serif générique, métriques différentes | Toujours inclure dans `<defs><style>` |
| Estimer les proportions sans calcul | Ratio mark/texte approximatif | Utiliser le script Python avec les formules |

---

## Récapitulatif du workflow complet

```
SVG vectorisé (via vtracer, post-processed)
        │
        ▼
   ÉTAPE 1 — Calculer le tight viewBox
   (script Python : parse d="" + translate → bornes réelles + 3% padding)
        │
        ▼
   ÉTAPE 2 — Extraire les <path .../> du SVG original
   (regex: re.findall(r'<path [^>]+/>', svg_content))
        │
        ▼
   ÉTAPE 3 — Construire les lockups avec <svg> imbriqué
   ├── Lockup primaire (vertical)
   │   viewBox: "0 0 {w} {h}"
   │   <svg x=centered y=25 width=W height=H viewBox="{tight_vb}">
   │     {paths}
   │   </svg>
   │   <text x=center y=below_mark text-anchor=middle>
   │
   └── Lockup secondaire (horizontal)
       viewBox: "0 0 {w} 80"
       <svg x=8 y=4 width=W height=72 viewBox="{tight_vb}">
         {paths}
       </svg>
       <text x=after_mark y=72%_of_mark font-size=30%_of_height>
        │
        ▼
   ÉTAPE 4 — Valider dans Chrome
   open -a "Google Chrome" lockup.svg
```

---

*Document créé le 15 Feb 2026 — Testé avec succès sur le logo "Sol Radieux" (Atelier Vermeil, session a2-b3). 4 itérations nécessaires pour converger (3 échecs scale transform, 1 succès nested SVG + tight viewBox).*
