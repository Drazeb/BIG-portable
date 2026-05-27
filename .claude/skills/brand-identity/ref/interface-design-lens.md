# Interface Design Lens — Pour le prescripteur (Phase 3B)

Ce fichier donne au DA prescripteur les réflexes d'un designer d'interface élite, SANS entrer dans le code. Chaque principe impacte directement un choix du pitch.

---

## 4 PRINCIPES OPÉRATIONNELS

### 1. Contraste Interactif
Chaque bouton/CTA DOIT contraster avec son fond immédiat. Test : le bouton est identifiable en 0.5s sur un screenshot flouté.
**Impact pitch** : quand tu prescris palette + registre atmosphérique, vérifie que l'accent se détache du fond prévu. Si ton atmosphere block est sombre ET ta couleur accent est sombre → collision.

### 2. Cohérence Tonale Inter-Sections
Les 3 sections (Voice Block → Artefact → Atmosphere) partagent une température de couleur. Max 1 transition warm↔cool sur les 3 sections.
**Impact pitch** : ne prescris pas un Voice Block chaud (terracotta), un Artefact froid (gris bleuté), puis un Atmosphere chaud → 2 transitions = incohérent. La palette doit FONCTIONNER sur les 3 sections, pas seulement en nuancier.

### 3. Rythme Spatial Différencié
Les 3 sections ont des densités DIFFÉRENTES. Le Voice Block est immersif (100vh), l'Artefact est resserré (contenu dense, utile), l'Atmosphere est compact (impression finale).
**Impact pitch** : quand tu prescris surface + rythme, pense en 3 RESPIRATIONS distinctes — pas un rythme uniforme.

### 4. Impact Above-Fold
Le Voice Block est autonome sans scroll. Le H1 display + au moins 1 CTA sont visibles sur un viewport standard (1440×900).
**Impact pitch** : si tu prescris une composition "Superposition" avec beaucoup de couches, ou un "Full-bleed typographique" avec du texte géant, vérifie que le contenu essentiel n'est pas poussé hors écran par la mise en scène.

---

## VOCABULAIRE DES COMPOSITIONS — Ce que chaque type IMPLIQUE visuellement

### Voice Block (8 types)

| Type | Ce que ça implique concrètement |
|------|-------------------------------|
| **Centré** | Symétrie, typographie seule comme levier, radial-gradient subtil en fond, impact par la taille du H1 |
| **Split** | Grille 55/45, mask-image pour liaison texte↔visuel, asymétrie contrôlée, CTA aligné à gauche |
| **Full-bleed typo** | Fond sombre, H1 en 8-10vw, blend-mode difference, CTA en outline (bordure) — tout repose sur la font display |
| **Superposition** | Couches transparentes empilées (z-index), backdrop-filter blur, bordures semi-transparentes, apparition animée |
| **Grille éditoriale** | Layout magazine en grid nommé, overline uppercase + letter-spacing, séparateur horizontal, container query pour responsive |
| **Diagonale / clip-path** | Découpe polygonale sur le visuel (polygon 15%), gradient diagonal, CTA lui-même découpé — tout est angulaire |
| **Scroll-reveal** | Apparition progressive au scroll (animation-timeline: view()), blur→net, scale 0.92→1 — dynamique temporelle |
| **Minimaliste radical** | Blanc dominant, H1 géant quasi-noir, CTA réduit à un lien souligné, interaction au hover sur le titre entier (lightness qui change) |

### Atmosphere Block (4 registres)

| Registre | Ce que ça implique concrètement |
|----------|-------------------------------|
| **Sombre** | Fond depth, radial-gradients colorés subtils en overlay, texte clair, accent en lumière — nécessite une palette avec assez de contraste clair |
| **Clair** | Continuation du surface, ombre inset en haut pour profondeur, border-top subtile — doux, pas de rupture |
| **Coloré** | Gradient diagonal primary→accent, overlay animé (hue-drift), text-shadow pour lisibilité, saturé et vivant |
| **Texturé** | SVG feTurbulence en overlay (grain/noise), gradient masqué en radial, sensation de matière physique (papier, pierre, tissu) |

---

## ANTI-PATTERNS DE PRESCRIPTION

Ce que le DA prescripteur doit ÉVITER de recommander :

- **Atmosphere sombre + accent sombre** → le CTA disparaît
- **3 sections même température + même densité** → monotonie, pas de voyage visuel
- **Full-bleed typo avec une body font en display** → tout repose sur la display, si elle n'est pas spectaculaire c'est plat
- **Scroll-reveal pour A=1** → le client veut du conventionnel, l'animation est un signal A≥2
- **Superposition pour un concept minimaliste** → contradiction — superposition = accumulation de couches
- **Split sans image/forme côté visuel** → le split a un panneau vide, la composition est bancale
