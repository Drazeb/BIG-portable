# Guide d'Implémentation — Couche d'Animation du Style-Tile (Étape 5D)

> **Lu par** : le sous-agent animateur (`phases/phase-5d-animation.md`).
> **Stack** : GSAP 3.13+ (`gsap`, `ScrollTrigger`, `SplitText`) via CDN + CSS natif. **Pas** de Lenis/ScrollSmoother (scroll natif). **Pas** de WebGL/3D/vidéo. **Pas** de framework JS.
> **Catalogue des options** : `ref/animation-catalogue.md` (les codes B1, C1, D2… ci-dessous y renvoient).
> **Dernière vérification** : 2026-05-12. *Avant de générer, faire un `WebSearch("gsap latest version")` ; si la version courante n'est plus 3.13.x, alerter l'utilisateur avant de figer les URLs CDN.*

---

## §1 — Setup technique (squelette commun à toute variante animée)

Toute variante animée = **le HTML source, inchangé, + une couche additive** composée de 4 morceaux :

**1a. Dans `<head>`, juste après le `<link>` Google Fonts** — un micro-script + un `<style>` scopé :

```html
<!-- ▸ COUCHE ANIMATION (Étape 5D) — état initial masqué UNIQUEMENT si JS actif -->
<script>document.documentElement.classList.add('gsap-anim');</script>
<style>
  /* on neutralise la transition CSS du bloc de contenu hero pour que le scrub GSAP soit net */
  html.gsap-anim .{hero-content-selector} { transition: none !important; }
  /* (UNIQUEMENT si une option d'entrée hero B1-B7 est active) masquer les éléments avant l'anim : */
  /* html.gsap-anim .{hero-content-selector} > * { opacity: 0; } */
  @media (prefers-reduced-motion: reduce) {
    html.gsap-anim .{hero-content-selector} > * { opacity: 1 !important; }
  }
</style>
```

Règles :
- N'ajouter la règle `.{hero-content-selector} > * { opacity: 0 }` **que si** une option B1-B7 est active. Si B0 (aucune entrée hero), ne rien masquer → pas de risque de « pop » blanc si le JS rate.
- Ne **jamais** mettre `opacity: 1 !important` sur le conteneur lui-même : GSAP doit pouvoir piloter son opacité (pour le fade-out C3).
- Le `<style>` scopé est le **seul** ajout CSS autorisé. Il ne touche aucun sélecteur existant du style-tile.

**1b. Avant `</body>`, après les éventuels `<script>` déjà présents** — les libs CDN (versions épinglées) :

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/ScrollTrigger.min.js"></script>
<!-- SplitText UNIQUEMENT si une option B2/B3/B4 est active : -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.13.0/SplitText.min.js"></script>
```

**1c. Juste après** — UN bloc `<script>` d'init, **toujours encapsulé** dans une IIFE avec garde-fou :

```html
<script>
(function () {
  // élements du hero qu'une option d'entrée masque (vide si B0)
  var heroKids = document.querySelectorAll('.{hero-content-selector} > *');
  function revealAll() {
    heroKids.forEach(function (el) { el.style.opacity = '1'; el.style.transform = 'none'; el.style.filter = 'none'; });
  }
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // garde-fou : si l'utilisateur réduit les anims, OU si un CDN n'a pas chargé → tout afficher, statique.
  if (reduceMotion || !window.gsap || !window.ScrollTrigger) { revealAll(); return; }
  gsap.registerPlugin(ScrollTrigger);
  if (window.SplitText) gsap.registerPlugin(SplitText);

  /* ---- ici : les blocs d'animation des options retenues ---- */

  // recalage des positions une fois les fonts chargées (clamp + text-wrap:balance peuvent décaler le layout)
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { ScrollTrigger.refresh(); });
  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
</script>
```

**1d. Optionnel** — quelques attributs `data-` sur des éléments existants, **uniquement si nécessaire** pour cibler proprement (préférer les sélecteurs CSS déjà présents). Ne jamais ajouter de classe qui pourrait entrer en collision avec le CSS du tile ; préfixer toute classe ajoutée par `vb-` ou `anim-`.

---

## §2 — Non-régression (RÈGLE ABSOLUE)

Le sous-agent **n'a le droit d'ajouter que** : les 4 morceaux du §1 (le `<script>` + `<style>` du 1a, les `<script src>` du 1b, le `<script>` d'init du 1c, éventuellement des `data-` du 1d).

Il ne **modifie ni ne supprime jamais** :
- le bloc `:root` / `@layer tokens` (les 40-60 custom properties — palette, typo, type-scale, spacing, radius, shadows, transitions) → **doit rester byte-identique** entre le HTML source et la variante animée ;
- aucune autre règle CSS existante (layers `reset`, `base`, `layer-graphic`, `components`, `sections`, `utilities`…) ;
- les `<script>` déjà présents (ex : une animation SVG sur-mesure type faisceau de phare, un `requestAnimationFrame` maison) → laissés tels quels, on ne les touche pas ;
- le HTML structurel (sections, contenu, alt, etc.) — sauf l'ajout d'attributs `data-` neutres du 1d.

**Vérification avant d'écrire chaque variante** : comparer le bloc `@layer tokens { :root { … } }` du source et de la sortie ; si différent, c'est un bug, corriger.

---

## §3 — Mode sûr « hero » (overlay calé sur l'image)

L'orchestrateur transmet `hero_safe_mode = true` quand le hero contient un overlay positionné dont la géométrie dépend du cadrage exact de l'image (ex : un `<svg>` en `position: absolute; inset: 0` avec des coordonnées en pixels durs — le faisceau du phare de Camille). **Le sous-agent re-vérifie lui-même** et bascule en mode sûr au moindre doute.

En mode sûr :
- **INTERDIT** : toute `transform` (scale, translate, yPercent…) sur l'image de fond du hero, sur l'élément overlay, ou sur leur conteneur commun. Pas de Ken Burns (C5), pas de pin avec zoom (C4), pas de parallaxe multi-couches (C2). L'image et l'overlay doivent rester **exactement** comme dans le style-tile.
- **AUTORISÉ** : animer le **bloc de texte** du hero (`yPercent` + `opacity`, scrubés au scroll → C1 + C3) ; les reveals des sections du bas (axe D) ; le header condensé (C6) ; l'entrée hero au chargement (axe B) — car celle-ci ne touche que le texte, pas l'image.

Sans overlay calé, le mode sûr ne s'applique pas et C2/C4/C5 redeviennent possibles si le preset les inclut.

---

## §4 — Recettes par option

Snippets canoniques, à insérer dans le bloc d'init du §1c. Affiner les amplitudes/durées selon la variante de dosage (§6). `{hero-section}` = le sélecteur de la section hero (souvent `.voice-block`), `{hero-content}` = le bloc de texte centré du hero, `{lower-sections}` = la liste des conteneurs des sections sous le hero.

### Axe B — Entrée du hero (timeline une-fois, `delay` ~0.15-0.2s)

**B1 · Fondu montant (staggered fade-up)**
```js
gsap.set('.{hero-content} > *', { opacity: 0 }); // déjà fait par le CSS du 1a, ok de doubler
gsap.timeline({ defaults: { ease: 'expo.out' }, delay: 0.18 })
  .fromTo('.{hero-content} > *', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.8, stagger: 0.1 });
```

**B2 · Typo par lignes (split-text line reveal)** — montée + fondu **sans clip dur** (sécurise les jambages) :
```js
var titleLines = null;
if (window.SplitText) { try { titleLines = new SplitText('.{hero-title}', { type: 'lines', linesClass: 'vb-line' }).lines; gsap.set('.{hero-title}', { opacity: 1 }); } catch (e) {} }
var intro = gsap.timeline({ defaults: { ease: 'expo.out' }, delay: 0.2 });
intro.fromTo('.{hero-overline}', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.8 }, 0);
if (titleLines && titleLines.length) intro.fromTo(titleLines, { opacity: 0, yPercent: 100, filter: 'blur(8px)' }, { opacity: 1, yPercent: 0, filter: 'blur(0px)', duration: 1.15, stagger: 0.14 }, 0.18);
else intro.fromTo('.{hero-title}', { opacity: 0, y: 24, filter: 'blur(8px)' }, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 1.15 }, 0.18);
intro.fromTo('.{hero-lead}', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.8 }, 0.62)
     .fromTo('.{hero-cta-row}', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.75 }, 0.9);
// si un bloc enfant du hero contient lui-même des enfants animés (ex: liste de chiffres), set le parent à opacity 1.
```
*B3 (mots) / B4 (lettres)* : idem mais `type: 'words'` / `'chars'`, stagger plus court (0.04-0.08), à réserver aux titres courts.

**B5 · Volet (clip-path reveal)** sur un bloc :
```js
gsap.fromTo('.{block}', { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)', duration: 1, ease: 'expo.out', delay: 0.3 });
```

**B6 · Mise au net (blur-in)** : ajouter `filter: 'blur(10px)' → 'blur(0px)'` à un `fromTo` d'entrée. Bref (≤ 0.8s), un seul élément.

**B7 · Compteurs** : voir D8 (même technique, déclenché au chargement au lieu d'au scroll).

### Axe C — Hero au scroll

**C1 + C3 · Parallaxe 1 couche + fondu de sortie** *(recette de référence, compatible mode sûr)* :
```js
gsap.timeline({
  scrollTrigger: { trigger: '.{hero-section}', start: 'top top', end: '+=70%', scrub: true, invalidateOnRefresh: true }
}).to('.{hero-content}', { yPercent: -24, opacity: 0, ease: 'none' });
```
*Variante « parallaxe seule » (C1 sans C3)* : retirer `opacity: 0`, baisser `yPercent` (~ -12). *Variante « différentielle »* (hors mode sûr) : ajouter une 2e `.to('.{hero-bg}', { yPercent: -8 }, 0)` après avoir donné de la marge (`scale: 1.15-1.2` sur le bg).

**C2 · Parallaxe multi-couches** *(interdit en mode sûr)* : `gsap.set('.{hero-bg}', { scale: 1.18 })` puis dans la timeline scrubée `.to('.{hero-bg}', { yPercent: -8 }, 0)` + `.to('.{hero-mid}', { yPercent: -16 }, 0)` + `.to('.{hero-content}', { yPercent: -32, opacity: 0 }, 0)`.

**C4 · Épinglage + scrub** *(interdit en mode sûr)* — pin court :
```js
gsap.timeline({ scrollTrigger: { trigger: '.{hero-section}', start: 'top top', end: '+=70%', pin: true, scrub: true, anticipatePin: 1, invalidateOnRefresh: true } })
  .to('.{hero-bg}', { scale: 1.12, ease: 'none' }, 0)            // léger
  .to('.{hero-content}', { yPercent: -16, opacity: 0.1, ease: 'none' }, 0);
```

**C5 · Ken Burns** *(interdit en mode sûr)* : `gsap.set('.{hero-bg}', { scale: 1.05 })` + scrub `.to('.{hero-bg}', { scale: 1.18, yPercent: 4, ease: 'none' })`. Toujours laisser de la marge (`overflow: hidden` sur le conteneur ; scale ≥ 1.05).

**C6 · Header condensé** : passer le header en `position: fixed` (via le `<style>` scopé, attention si le header était `position: absolute` dans le tile — vérifier que rien ne casse), puis :
```js
ScrollTrigger.create({ trigger: 'body', start: '80px top', toggleClass: { targets: '.{header}', className: 'is-condensed' } });
```
+ une règle `.{header}.is-condensed { /* fond, ombre, padding réduit, blur */ }` dans le `<style>` scopé. Transition CSS sur le header pour adoucir.

### Axe D — Reveals des sections du bas

**D1 · Apparition par le bas (fade-up on scroll)** *(recette de référence)* :
```js
['.{lower-section-1}', '.{lower-section-2}', /* … */].forEach(function (sel) {
  var root = document.querySelector(sel); if (!root) return;
  gsap.utils.toArray(root.children).forEach(function (el, i) {
    if (el.tagName === 'STYLE' || el.tagName === 'SCRIPT' || el.classList.contains('grain')) return;
    gsap.set(el, { opacity: 0, y: 36 });
    ScrollTrigger.create({ trigger: el, start: 'top 85%', once: true,
      onEnter: function () { gsap.to(el, { opacity: 1, y: 0, duration: 0.95, ease: 'expo.out', delay: (i % 3) * 0.05 }); } });
  });
});
```
**D2 · Cascade (staggered reveal)** : variante de D1 — au lieu d'un ScrollTrigger par enfant, un seul par section avec `onEnter: () => gsap.to(kids, { opacity:1, y:0, stagger: 0.12, ... })`.

**D3 · Volet (clip-path wipe)** : `gsap.set(el, { clipPath:'inset(0 0 100% 0)' })` + `onEnter → gsap.to(el, { clipPath:'inset(0 0 0% 0)', duration: 0.9 })`.

**D4 · Apparition zoomée (scale-in)** : `gsap.set(el, { opacity:0, scale: 0.94 })` + `onEnter → gsap.to(el, { opacity:1, scale:1, duration: 0.8, ease:'expo.out' })`. Pas de `back`/`elastic`.

**D5 · Entrée latérale (slide-in)** : `gsap.set(el, { opacity:0, x: 40 })` + `onEnter → gsap.to(el, { opacity:1, x:0, ... })`. Alterner le sens avec parcimonie ; jamais sur plus de 2-3 blocs.

**D6 · Tracé de trait (SVG path / `stroke-dashoffset`)** : pour un `<svg><path>` (ou un faux trait via un `<span>` avec bordure), `gsap.set(path, { strokeDasharray: len, strokeDashoffset: len })` + `onEnter → gsap.to(path, { strokeDashoffset: 0, duration: 1.2, ease:'power2.inOut' })`. Pour une hairline CSS : animer une pseudo-largeur via `scaleX` de 0 → 1 avec `transform-origin: left`.

**D7 · Dévoilé d'image** : `gsap.fromTo(img, { clipPath:'inset(0 0 100% 0)', scale: 1.06 }, { clipPath:'inset(0 0 0% 0)', scale: 1, duration: 1.1, ease:'expo.out', scrollTrigger: { trigger: img, start:'top 80%' } })`.

**D8 · Compteurs (number counter)** :
```js
gsap.utils.toArray('.{counter}').forEach(function (el) {
  var end = parseFloat(el.getAttribute('data-count') || el.textContent.replace(/[^\d.]/g, '')) || 0;
  var prefix = el.getAttribute('data-prefix') || '', suffix = el.getAttribute('data-suffix') || '';
  var obj = { v: 0 };
  ScrollTrigger.create({ trigger: el, start: 'top 85%', once: true, onEnter: function () {
    gsap.to(obj, { v: end, duration: 1.4, ease: 'power2.out', onUpdate: function () { el.textContent = prefix + Math.round(obj.v).toLocaleString('fr-FR') + suffix; } });
  }});
});
```
Le `data-count`/`data-prefix`/`data-suffix` sont des attributs `data-` ajoutés (1d) ; ne pas casser un nombre déjà formaté (« €340 M » → `data-count="340" data-prefix="€" data-suffix=" M"`, texte initial conservé en fallback statique).

**D9 · Parallaxe intra-page** : `gsap.to('.{element}', { yPercent: -10, ease:'none', scrollTrigger: { trigger: '.{element-parent}', start:'top bottom', end:'bottom top', scrub: true } })`. Léger, jamais sur un bloc avec overlay calé.

### Axe E — Micro-interactions

**E1 · États hover riches** : ne PAS ajouter de JS — enrichir via le `<style>` scopé (`transition`, `box-shadow`, `transform: translateY(-2px)`, flèche `::after { transform: translateX(4px) }` au hover). À ne faire que si le tile en manque visiblement.

**E2 · Bouton magnétique** :
```js
gsap.utils.toArray('.{magnetic}').forEach(function (btn) {
  var bounds; btn.addEventListener('mouseenter', function () { bounds = btn.getBoundingClientRect(); });
  btn.addEventListener('mousemove', function (e) {
    var x = e.clientX - bounds.left - bounds.width/2, y = e.clientY - bounds.top - bounds.height/2;
    gsap.to(btn, { x: x*0.25, y: y*0.25, duration: 0.4, ease: 'power3.out' });
  });
  btn.addEventListener('mouseleave', function () { gsap.to(btn, { x: 0, y: 0, duration: 0.5, ease: 'elastic.out(1, 0.4)' }); });
});
```
1-2 boutons max. Pas sur mobile (`if (matchMedia('(pointer:fine)').matches)`).

**E3 · Curseur custom** — **opt-in seulement** ; un `<div class="anim-cursor">` ajouté en fin de `<body>` + CSS scopé + `gsap.quickTo` sur `mousemove`. Toujours `pointer-events: none`, `mix-blend-mode: difference` ou similaire. Désactiver si `(pointer: coarse)`.

**E4 · Inclinaison 3D** : sur une carte/visuel, `mousemove` → `gsap.to(card, { rotateY: x*8, rotateX: -y*8, transformPerspective: 800, duration: 0.4 })` ; `mouseleave` → retour à 0. Un seul élément.

**E5 · Marquee** — CSS pur préférable : dupliquer le contenu du bandeau, `display: flex`, `animation: marquee 20s linear infinite` + `@keyframes marquee { to { transform: translateX(-50%) } }`. Pause au hover (`animation-play-state: paused`).

**E6 · Image au survol** : sur des liens de liste, un `<img>` en `position: fixed; opacity: 0; pointer-events: none` qui suit le curseur et `opacity: 1` au hover du lien (`gsap.quickTo` pour la position).

### Axe F — Fond / ambiance

**F1 · Dégradé animé** — CSS pur + `@property`, cycle long :
```css
@property --g { syntax: '<angle>'; inherits: false; initial-value: 0deg; }
.{ambient} { background: conic-gradient(from var(--g) at 50% 50%, /* couleurs de la palette */); animation: gspin 28s linear infinite; }
@keyframes gspin { to { --g: 360deg; } }
```
Couleurs : **uniquement des tokens existants** (`var(--color-…)`) ou des `color-mix()` dessus. Cycle ≥ 20s. Jamais sur un fond clair (effet halo douteux).

**F2 · Grain animé** : si le tile a déjà une couche `.grain` (data-URI SVG `feTurbulence`), animer très légèrement `background-position` (`animation: grainshift 8s steps(8) infinite` avec quelques positions). Sinon, ne pas en ajouter.

**F3 (aurora/mesh) / F4 (particules)** : **ne pas implémenter** sauf demande explicite et insistante de l'utilisateur — ce sont des marqueurs d'AI-slop. Si vraiment imposé : ultra-subtil, sur fond sombre uniquement, et le signaler dans `{brand}-animation-spec.md`.

**F5 · SVG/canvas sur-mesure** : **le sous-agent ne crée jamais** une telle animation. S'il y en a déjà une dans le tile (faisceau de phare, etc.), il la **laisse intacte** et travaille autour (mode sûr probable).

**F6 · Vidéo/shader** : hors v1 — ne pas implémenter.

---

## §5 — Anti-slop animation (règles fermes)

- **Pas** de mesh/aurora/blob WebGL en fond (F3), pas de particules (F4) — marqueurs d'AI-slop 2023-2024.
- **Pas** de smooth-scroll par défaut (A2 opt-in seulement) : la sensation « lourde » est exactement ce qu'on évite.
- **Pas** de pin long sur un style-tile (≤ 70-80vh de scroll si C4 est utilisé) — vite vu sur un document qu'on parcourt en quelques secondes.
- **Easings** : `expo.out` / `power2-3.out` / `'none'` (pour les scrubs) / `power2.inOut` (pour les tracés). **Pas** de `back.out`, `elastic`, `bounce` agressifs (sauf un `elastic.out(1, 0.4)` discret pour le retour d'un bouton magnétique).
- **Durées** : entrées/reveals 0.6-1.2s ; scrubs → `scrub: true` (verrouillé au scroll, pas de lag) ou `scrub: 0.5-1` au plus si on veut un soupçon de catch-up ; rien au-delà.
- **Amplitudes** : translations d'entrée 12-40px / 12-24 `yPercent` ; scales 0.94-1.0 (entrée) ou 1.0-1.18 (Ken Burns) ; blurs ≤ 10px et brefs.
- **Pas** de curseur custom (E3) ni de tilt (E4) dans un preset par défaut.
- **`prefers-reduced-motion`** : toujours respecté via le garde-fou du §1c. Aucune exception.
- **Performance** : n'animer que `transform`, `opacity`, `filter`, `clip-path` ; pas d'animation de `width`/`height`/`top`/`left`/`box-shadow` en boucle ; `will-change` parcimonieux.
- **Console propre** : aucune erreur JS au chargement (tester avec et sans réseau).

---

## §6 — Stratégie des 2-3 variantes de dosage

Le sous-agent produit **2-3 variantes** (`-animated-v1.html`, `-v2.html`, `-v3.html`) qui implémentent **la même liste d'options**, en faisant varier **le dosage uniquement** :

| Variante | Dosage |
|---|---|
| **v1 · Subtil** | Amplitudes basses, durées courtes (entrées 0.6-0.7s, `yPercent` -12 à -16 pour le parallaxe, scales proches de 1, pas de blur ou très léger). « On le sent à peine. » |
| **v2 · Médian** | Réglages de référence des recettes du §4 (entrées ~0.8-1s, parallaxe -24, blur 8px sur la typo si B2). Le « bon défaut ». |
| **v3 · Prononcé** | Amplitudes plus marquées (parallaxe -28 à -34, durées 1-1.2s, blur plus présent) **+ éventuellement une option bonus compatible** non demandée mais cohérente (ex : ajouter B2 typo au load si le preset ne l'avait pas, ou D6 line drawing sur les hairlines). « Ça envoie. » |

Ne **jamais** changer la liste d'options entre v1 et v2 (seul le dosage bouge) ; v3 peut ajouter **une seule** option bonus, signalée dans la présentation à l'utilisateur. Lors d'une itération (resume avec feedback), partir de la variante que l'utilisateur a désignée et appliquer le feedback dessus.

À la fin (l'utilisateur a choisi), l'orchestrateur promeut la variante retenue en `{brand}-style-tile-concept-{n}-animated.html` et archive les autres — le sous-agent n'a pas à gérer ça.
