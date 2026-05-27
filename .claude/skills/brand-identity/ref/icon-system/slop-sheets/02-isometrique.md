# 02 — Isométrique / 3D — Fiche slop / anti-slop

**Famille** : `02-isometrique` · **Dernière revue** : 2026-05-27 · **Prochaine revue** : 2026-08-27

**Sources scannées** : Cloudflare illustrations (2024-2025), Vercel Conf (2024), Streamline 3D (2022-2025), Iconscout 3D (2024), Framer marketing (2024), *The Return of Isometric Design (Without the Pastel)* — Eye on Design AIGA (août 2024).

---

## À BANNIR — 8 anti-patterns datés

### `[ANTI-01]` Palette pastel iso Stripe-era (2017-2020)
- **Description** : violet/lavande/pêche pâle, gradient cyan→magenta sur les volumes
- **Preuve d'âge** : Stripe website 2018-2021, Slack iso 2017-2020
- **Signature slop** : signature "tech startup friendly" devenue cliché total
- **Contre-exemple pro** : Cloudflare 2024 — palette contrastée, mode sombre dominant

### `[ANTI-02]` Personnages iso au cou-girafe (= Corporate Memphis iso)
- **Description** : version iso du Corporate Memphis, figures simplifiées allongées en projection 30°
- **Preuve d'âge** : ère 2018-2022, Slack/Mailchimp v1/Facebook
- **Signature slop** : double slop — Memphis + iso
- **Contre-exemple pro** : Vercel iso 2024 — objets uniquement, pas de figures humaines stylisées cliché

### `[ANTI-03]` Gradient lisse sur les faces (mesh gradient)
- **Description** : faces iso avec dégradé lisse au lieu d'aplat de couleur nuancée
- **Preuve d'âge** : tendance "iso gradient" 2019-2021
- **Signature slop** : tueur du caractère "construit" de l'iso
- **Contre-exemple pro** : Streamline 3D 2024 — uniquement aplats nuancés, jamais gradient

### `[ANTI-04]` Ombre portée diffuse sous chaque objet
- **Description** : drop-shadow soft sous tous les objets, leur donnant un effet "flottant cute"
- **Preuve d'âge** : Material Design iso 2018-2021
- **Signature slop** : tueur de la solidité construite
- **Contre-exemple pro** : Cloudflare 2024 — ombres calculées par face, pas drop-shadow CSS

### `[ANTI-05]` Détails "tech" génériques (engrenages, % de croissance, courbes)
- **Description** : meubles iso recouverts de symboles tech génériques
- **Preuve d'âge** : automatisme B2B SaaS 2017-2022
- **Signature slop** : "nous sommes une boîte tech, mettons des graphes"
- **Contre-exemple pro** : Vercel iso 2024 — objets métier spécifiques (serveurs, edges, requests)

### `[ANTI-06]` Projection inconsistante (mix iso 30° + cabinet 45° dans le même set)
- **Description** : oubli des règles de projection, angles approximatifs
- **Preuve d'âge** : signature "iso fait à la main rapidement" 2019-2022
- **Signature slop** : casse la rigueur géométrique qui fait la valeur de la famille
- **Contre-exemple pro** : 100% des biblios pro 2024 — projection rigoureuse constante

### `[ANTI-07]` Cubes vides empilés sans objet métier identifiable
- **Description** : illustrations iso composées uniquement de cubes / parallélépipèdes abstraits
- **Preuve d'âge** : illustrations "infrastructure générique" 2018-2021
- **Signature slop** : interchangeable, oubliable
- **Contre-exemple pro** : Cloudflare 2024 — objets reconnaissables (rack serveur, routeur, requête HTTP)

### `[ANTI-08]` Iso "isométrique pur" sans variation cabinet/cavalière
- **Description** : exclusivement iso 30° strict, jamais d'angle alternatif pour le rythme
- **Preuve d'âge** : signature "iso facile" templates Envato 2019-2022
- **Signature slop** : monotonie visuelle d'un set complet
- **Contre-exemple pro** : Iconscout 3D 2024 — mix iso pour les volumes + cabinet pour les actions, rythme

---

## SIGNATURES PRO 2024-2026 — 5 patterns à reproduire

### `[SIG-01]` Mode sombre + accents lumineux saturés (palette Cloudflare-like)
- **Description** : fond charbon / nuit, objets iso avec aplats sombres + UN accent lumineux ponctuel (orange, vert électrique, cyan)
- **Source** : Cloudflare 2024-2025, Vercel Conf 2024
- **Implémentation** : palette restreinte 3-4 couleurs, contraste fort

### `[SIG-02]` Wireframe iso (uniquement stroke, sans fills)
- **Description** : variante "wire" qui montre la structure sans les surfaces
- **Source** : Streamline 3D wireframe (2024), Iconscout 3D wire (2024)
- **Implémentation** : tous les paths en `fill: none; stroke: ...`, stroke 1px

### `[SIG-03]` Objets métier reconnaissables (pas cubes abstraits)
- **Description** : chaque illustration iso représente un objet du domaine de la marque
- **Source** : Cloudflare 2024 (serveurs/edges), Vercel 2024 (pages/builds)
- **Implémentation** : dériver les sujets des territoires créatifs, pas du métier littéral

### `[SIG-04]` Grain noise overlay subtil (signature 2024)
- **Description** : texture grain photoshop discrète sur les volumes
- **Source** : Cloudflare 2024, Framer 2024
- **Implémentation** : filter SVG feTurbulence opacity 0.05-0.08 sur les volumes principaux

### `[SIG-05]` Composition asymétrique éditoriale (vs centrée symétrique)
- **Description** : refus du centrage iso parfait, asymétrie 1/3 vs 2/3 ou décentrement narratif
- **Source** : Cloudflare hero illustrations 2024, Vercel Conf 2024
- **Implémentation** : viewBox décalée, objet principal hors centre

---

## CHECKS MÉCANIQUES — 2 vérifications

### `[CHK-01]` Pas de `linearGradient` ni `radialGradient` lisse multi-stops
- **Règle** : profondeur par aplats nuancés, pas par dégradé
- **Vérification** : grep — `<linearGradient>` avec ≥3 stops = fail

### `[CHK-02]` Au moins 3 polygones distincts par objet (top + 2 côtés)
- **Règle** : assure la projection iso correcte, pas un simple rectangle "déguisé"
- **Vérification** : compter les `<polygon>` ou `<path>` par groupe d'icône, doit être ≥3

### `[CHK-03]` INCARNATION VISIBLE — ≥30% des icônes du set 06.1 ont une vraie projection iso (3 polygones face + fills nuancés OU wireframe iso)
- **Règle** : `[SIG-02]` wireframe iso OU `[SIG-03]` objets métier en projection 30° doivent être incarnés. Au moins 6 icônes sur ~20 doivent avoir soit (a) ≥3 polygones distincts avec fills de couleurs DIFFÉRENTES (face top + 2 côtés iso) soit (b) être en mode wireframe iso pur (`fill="none"` + stroke 1px)
- **Vérification** : pour chaque SVG du set, compter polygones avec fills distincts (≥3 distincts = OK) ou détecter wireframe (toutes les formes en `fill="none"`). Ratio ≥30%
- **Si fail (<30%)** : la signature iso n'est pas incarnée. Les icônes sont plates ou en 2D pure. Re-dispatch designer : "Au moins 6 icônes du set DOIVENT être en projection isométrique 30° visible (face top + 2 côtés en aplats nuancés OU wireframe iso complet)."
