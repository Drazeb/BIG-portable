# CSS Patterns — Phase 4 Style-Tile

Squelettes CSS pour Voice Block (8 types) et Atmosphere Block (4 registres).
L'orchestrateur injecte le pattern correspondant au type choisi dans le pitch via `{css_pattern_block}`.

Le subagent DOIT :
- Utiliser ce squelette comme FONDATION POSITIONNELLE
- ENRICHIR avec la palette, la typo, les surfaces et les interactions du concept
- CONSERVER les techniques CSS embarquées (clip-path, mask-image, etc.) dans le HTML final

---

## VOICE BLOCK PATTERNS

### VB-1 : Centré

```css
.voice-block {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-block-size: 100vh;
    padding-block: var(--space-4xl) var(--space-3xl);
    padding-inline: var(--space-lg);
    background: radial-gradient(ellipse at 50% 40%,
        color-mix(in oklch, var(--color-primary) 8%, var(--color-surface)),
        var(--color-surface));
    text-align: center;
    position: relative;
    overflow: hidden;
}
.voice-block__title {
    font-family: var(--font-display);
    font-size: clamp(var(--text-3xl), 7vw, var(--text-5xl));
    font-weight: 700;
    color: var(--color-text-primary);
    text-wrap: balance;
    max-inline-size: 18ch;
    line-height: 1.05;
    margin-block-end: var(--space-md);
}
.voice-block__lead {
    font-family: var(--font-body);
    font-size: var(--text-lg);
    color: var(--color-text-secondary);
    text-wrap: pretty;
    max-inline-size: 48ch;
    margin-block-end: var(--space-xl);
}
.voice-block__cta {
    font-family: var(--font-body);
    font-size: var(--text-base);
    font-weight: 600;
    padding: var(--space-sm) var(--space-xl);
    background: var(--color-primary);
    color: var(--color-text-on-primary);
    border: 2px solid transparent;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: background var(--transition-base), border-color var(--transition-fast), box-shadow var(--transition-base);
}
.voice-block__cta:hover {
    background: color-mix(in oklch, var(--color-primary) 85%, black);
    border-color: var(--color-accent);
    box-shadow: var(--shadow-lg);
}
```

### VB-2 : Split

```css
.voice-block {
    display: grid;
    grid-template-columns: 55fr 45fr;
    min-block-size: 100vh;
    overflow: hidden;
}
.voice-block__content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-block: var(--space-3xl);
    padding-inline: var(--space-2xl) var(--space-xl);
}
.voice-block__title {
    font-family: var(--font-display);
    font-size: clamp(var(--text-2xl), 5vw, var(--text-4xl));
    font-weight: 700;
    color: var(--color-text-primary);
    text-wrap: balance;
    line-height: 1.1;
    margin-block-end: var(--space-md);
}
.voice-block__lead {
    font-family: var(--font-body);
    font-size: var(--text-lg);
    color: var(--color-text-secondary);
    text-wrap: pretty;
    max-inline-size: 42ch;
    margin-block-end: var(--space-xl);
}
.voice-block__visual {
    position: relative;
    background: var(--color-primary);
    mask-image: linear-gradient(to right, transparent, black 15%);
    -webkit-mask-image: linear-gradient(to right, transparent, black 15%);
}
.voice-block__visual::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom,
        color-mix(in oklch, var(--color-primary) 90%, transparent),
        color-mix(in oklch, var(--color-accent) 40%, transparent));
    mix-blend-mode: overlay;
}
.voice-block__cta {
    font-family: var(--font-body);
    font-weight: 600;
    padding: var(--space-sm) var(--space-xl);
    background: var(--color-accent);
    color: var(--color-text-on-primary);
    border: 2px solid transparent;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: background var(--transition-base), border-color var(--transition-fast), box-shadow var(--transition-base);
    align-self: flex-start;
}
.voice-block__cta:hover {
    background: color-mix(in oklch, var(--color-accent) 80%, black);
    border-color: var(--color-primary);
    box-shadow: var(--shadow-md);
}
```

### VB-3 : Full-bleed typographique

```css
@property --hero-hue {
    syntax: '<number>';
    initial-value: 0;
    inherits: false;
}
.voice-block {
    min-block-size: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-block: var(--space-3xl);
    padding-inline: var(--space-xl);
    background: var(--color-depth);
    color: var(--color-text-on-depth);
    position: relative;
    overflow: hidden;
}
.voice-block::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 30% 60%,
        color-mix(in oklch, var(--color-primary) 20%, transparent),
        transparent 70%);
    mix-blend-mode: soft-light;
}
.voice-block__title {
    position: relative;
    font-family: var(--font-display);
    font-size: clamp(var(--text-4xl), 10vw, 8rem);
    font-weight: 900;
    line-height: 0.95;
    text-wrap: balance;
    color: var(--color-text-on-depth);
    mix-blend-mode: difference;
    margin-block-end: var(--space-lg);
}
.voice-block__lead {
    position: relative;
    font-family: var(--font-body);
    font-size: var(--text-lg);
    color: color-mix(in oklch, var(--color-text-on-depth) 70%, transparent);
    max-inline-size: 36ch;
    text-wrap: pretty;
    margin-block-end: var(--space-xl);
}
.voice-block__cta {
    position: relative;
    font-family: var(--font-body);
    font-weight: 600;
    padding: var(--space-sm) var(--space-xl);
    background: transparent;
    color: var(--color-accent);
    border: 2px solid var(--color-accent);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: background var(--transition-base), color var(--transition-fast), box-shadow var(--transition-base);
    align-self: flex-start;
}
.voice-block__cta:hover {
    background: var(--color-accent);
    color: var(--color-depth);
    box-shadow: 0 4px 16px color-mix(in oklch, var(--color-accent) 15%, transparent), 0 12px 40px color-mix(in oklch, var(--color-accent) 8%, transparent);
}
```

### VB-4 : Superposition

```css
@starting-style {
    .voice-block__title { opacity: 0; translate: 0 1rem; }
    .voice-block__lead { opacity: 0; translate: 0 1.5rem; }
}
.voice-block {
    min-block-size: 100vh;
    display: grid;
    grid-template-rows: 1fr;
    position: relative;
    overflow: hidden;
    background: var(--color-depth);
}
.voice-block__layer-bg {
    position: absolute;
    inset: 0;
    background: conic-gradient(from 45deg at 30% 70%,
        var(--color-primary),
        color-mix(in oklch, var(--color-secondary) 60%, var(--color-primary)),
        var(--color-primary));
    opacity: 0.15;
    mix-blend-mode: screen;
}
.voice-block__layer-mid {
    position: absolute;
    inset: 10% 5%;
    border: 1px solid color-mix(in oklch, var(--color-accent) 15%, transparent);
    border-radius: var(--radius-lg);
    backdrop-filter: blur(12px) saturate(1.1);
}
.voice-block__content {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: var(--space-3xl) var(--space-2xl);
}
.voice-block__title {
    font-family: var(--font-display);
    font-size: clamp(var(--text-3xl), 6vw, var(--text-5xl));
    font-weight: 700;
    color: var(--color-text-on-depth);
    text-wrap: balance;
    line-height: 1.05;
    margin-block-end: var(--space-md);
    opacity: 1; translate: 0 0;
    transition: opacity 0.8s var(--ease-out-expo), translate 0.8s var(--ease-out-expo);
}
.voice-block__lead {
    font-family: var(--font-body);
    font-size: var(--text-lg);
    color: color-mix(in oklch, var(--color-text-on-depth) 75%, transparent);
    text-wrap: pretty;
    max-inline-size: 44ch;
    margin-block-end: var(--space-xl);
    opacity: 1; translate: 0 0;
    transition: opacity 1s var(--ease-out-expo) 0.15s, translate 1s var(--ease-out-expo) 0.15s;
}
.voice-block__cta {
    font-family: var(--font-body);
    font-weight: 600;
    padding: var(--space-sm) var(--space-xl);
    background: color-mix(in oklch, var(--color-accent) 15%, transparent);
    color: var(--color-accent);
    border: 1px solid color-mix(in oklch, var(--color-accent) 30%, transparent);
    border-radius: var(--radius-md);
    backdrop-filter: blur(8px);
    cursor: pointer;
    transition: background var(--transition-base), border-color var(--transition-fast), box-shadow var(--transition-base);
    align-self: flex-start;
}
.voice-block__cta:hover {
    background: color-mix(in oklch, var(--color-accent) 25%, transparent);
    border-color: var(--color-accent);
    box-shadow: 0 4px 16px color-mix(in oklch, var(--color-accent) 12%, transparent), 0 12px 36px color-mix(in oklch, var(--color-accent) 6%, transparent);
}
```

### VB-5 : Grille éditoriale

```css
.voice-block {
    min-block-size: 100vh;
    display: grid;
    grid-template-columns: var(--space-2xl) 1fr 1fr var(--space-2xl);
    grid-template-rows: var(--space-3xl) auto auto 1fr var(--space-2xl);
    grid-template-areas:
        ". . . ."
        ". overline overline ."
        ". title title ."
        ". lead cta ."
        ". . . .";
    background: var(--color-surface);
    position: relative;
    container-type: inline-size;
    container-name: voice;
}
.voice-block__overline {
    grid-area: overline;
    font-family: var(--font-body);
    font-size: var(--text-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--color-accent);
    margin-block-end: var(--space-sm);
}
.voice-block__title {
    grid-area: title;
    font-family: var(--font-display);
    font-size: clamp(var(--text-3xl), 5vw, var(--text-5xl));
    font-weight: 700;
    color: var(--color-text-primary);
    text-wrap: balance;
    line-height: 1.05;
    margin-block-end: var(--space-lg);
    border-block-end: 2px solid var(--color-primary);
    padding-block-end: var(--space-lg);
}
.voice-block__lead {
    grid-area: lead;
    font-family: var(--font-body);
    font-size: var(--text-base);
    color: var(--color-text-secondary);
    text-wrap: pretty;
    line-height: 1.7;
    align-self: start;
}
.voice-block__cta-area {
    grid-area: cta;
    display: flex;
    align-items: start;
    justify-content: flex-end;
    padding-block-start: var(--space-sm);
}
@container voice (max-width: 700px) {
    .voice-block {
        grid-template-columns: var(--space-lg) 1fr var(--space-lg);
        grid-template-areas:
            ". . ."
            ". overline ."
            ". title ."
            ". lead ."
            ". cta .";
    }
}
```

### VB-6 : Diagonale / clip-path

```css
@property --diag-angle {
    syntax: '<angle>';
    initial-value: 3deg;
    inherits: false;
}
.voice-block {
    min-block-size: 100vh;
    display: grid;
    grid-template-columns: 1fr 1fr;
    position: relative;
    overflow: hidden;
}
.voice-block__content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: var(--space-3xl) var(--space-2xl);
    position: relative;
    z-index: 2;
}
.voice-block__visual {
    position: relative;
    background: var(--color-primary);
    clip-path: polygon(15% 0, 100% 0, 100% 100%, 0% 100%);
}
.voice-block__visual::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(
        var(--diag-angle),
        color-mix(in oklch, var(--color-accent) 40%, transparent),
        transparent 60%);
    mask-image: linear-gradient(to bottom, black, transparent 90%);
    -webkit-mask-image: linear-gradient(to bottom, black, transparent 90%);
}
.voice-block__title {
    font-family: var(--font-display);
    font-size: clamp(var(--text-3xl), 6vw, var(--text-5xl));
    font-weight: 700;
    color: var(--color-text-primary);
    text-wrap: balance;
    line-height: 1.05;
    margin-block-end: var(--space-md);
}
.voice-block__lead {
    font-family: var(--font-body);
    font-size: var(--text-lg);
    color: var(--color-text-secondary);
    text-wrap: pretty;
    max-inline-size: 38ch;
    margin-block-end: var(--space-xl);
}
.voice-block__cta {
    font-family: var(--font-body);
    font-weight: 600;
    padding: var(--space-sm) var(--space-xl);
    background: var(--color-primary);
    color: var(--color-text-on-primary);
    border: none;
    border-radius: var(--radius-md);
    clip-path: polygon(0 0, 100% 0, 95% 100%, 0% 100%);
    cursor: pointer;
    transition: background var(--transition-base), clip-path var(--transition-slow), box-shadow var(--transition-base);
    align-self: flex-start;
}
.voice-block__cta:hover {
    background: color-mix(in oklch, var(--color-primary) 85%, black);
    clip-path: polygon(0 0, 100% 0, 100% 100%, 5% 100%);
    box-shadow: var(--shadow-lg);
}
```

### VB-7 : Scroll-reveal

```css
@starting-style {
    .voice-block__title { opacity: 0; scale: 0.95; }
    .voice-block__lead { opacity: 0; translate: 0 2rem; }
    .voice-block__cta { opacity: 0; translate: 0 2rem; }
}
.voice-block {
    min-block-size: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-block: var(--space-4xl);
    padding-inline: var(--space-xl);
    background: var(--color-surface);
    text-align: center;
}
.voice-block__title {
    font-family: var(--font-display);
    font-size: clamp(var(--text-3xl), 7vw, var(--text-5xl));
    font-weight: 700;
    color: var(--color-text-primary);
    text-wrap: balance;
    max-inline-size: 16ch;
    line-height: 1.05;
    margin-block-end: var(--space-lg);
    opacity: 1; scale: 1;
    transition: opacity 0.8s var(--ease-out-expo), scale 0.6s var(--ease-out-back);
    animation: reveal-title linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 40%;
}
@keyframes reveal-title {
    from { opacity: 0; scale: 0.92; filter: blur(4px); }
    to { opacity: 1; scale: 1; filter: blur(0); }
}
.voice-block__lead {
    font-family: var(--font-body);
    font-size: var(--text-lg);
    color: var(--color-text-secondary);
    text-wrap: pretty;
    max-inline-size: 48ch;
    margin-block-end: var(--space-xl);
    opacity: 1; translate: 0 0;
    transition: opacity 1s var(--ease-out-expo) 0.2s, translate 1s var(--ease-out-expo) 0.2s;
}
.voice-block__cta {
    font-family: var(--font-body);
    font-weight: 600;
    padding: var(--space-sm) var(--space-xl);
    background: var(--color-primary);
    color: var(--color-text-on-primary);
    border: 2px solid transparent;
    border-radius: var(--radius-md);
    cursor: pointer;
    opacity: 1; translate: 0 0;
    transition: opacity 1s var(--ease-out-expo) 0.35s, translate 1s var(--ease-out-expo) 0.35s, background var(--transition-base), border-color var(--transition-fast), box-shadow var(--transition-base);
}
.voice-block__cta:hover {
    background: color-mix(in oklch, var(--color-primary) 85%, black);
    border-color: var(--color-accent);
    box-shadow: var(--shadow-lg);
}
```

### VB-8 : Minimaliste radical

```css
@property --title-l {
    syntax: '<number>';
    initial-value: 0.25;
    inherits: false;
}
.voice-block {
    min-block-size: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-block: var(--space-4xl);
    padding-inline: var(--space-2xl);
    background: var(--color-surface);
}
.voice-block__title {
    font-family: var(--font-display);
    font-size: clamp(var(--text-4xl), 8vw, 7rem);
    font-weight: 800;
    color: oklch(var(--title-l) 0.02 var(--hue-primary));
    line-height: 0.95;
    letter-spacing: -0.03em;
    text-wrap: balance;
    margin-block-end: var(--space-xl);
    transition: --title-l 0.6s var(--ease-out-expo), letter-spacing 0.6s var(--ease-out-expo);
}
.voice-block:hover .voice-block__title {
    --title-l: 0.45;
    letter-spacing: -0.01em;
}
.voice-block__lead {
    font-family: var(--font-body);
    font-size: var(--text-base);
    color: var(--color-text-secondary);
    max-inline-size: 40ch;
    text-wrap: pretty;
    margin-block-end: var(--space-lg);
}
.voice-block__cta {
    font-family: var(--font-body);
    font-weight: 500;
    font-size: var(--text-sm);
    padding: var(--space-xs) 0;
    background: none;
    color: var(--color-text-primary);
    border: none;
    border-block-end: 1px solid var(--color-text-primary);
    cursor: pointer;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    transition: border-color var(--transition-base), color var(--transition-base);
    align-self: flex-start;
}
.voice-block__cta:hover {
    border-color: var(--color-accent);
    color: var(--color-accent);
}
```

---

### VB-9 : Stacked

```css
@property --reveal-y {
    syntax: '<length>';
    initial-value: 40px;
    inherits: false;
}
.voice-block {
    min-block-size: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding-block-start: clamp(var(--space-2xl), 15vh, var(--space-3xl));
    padding-inline: var(--space-xl);
    background: var(--color-surface);
    color: var(--color-text-primary);
    position: relative;
    overflow: hidden;
}
.voice-block__content {
    position: relative;
    z-index: 2;
    text-align: center;
    max-inline-size: 800px;
    margin-block-end: var(--space-xl);
}
.voice-block__title {
    font-family: var(--font-display);
    font-size: clamp(var(--text-3xl), 9vw, 10rem);
    font-weight: 700;
    line-height: 0.95;
    text-wrap: balance;
    color: var(--color-text-primary);
    margin-block-end: var(--space-md);
}
.voice-block__lead {
    font-family: var(--font-body);
    font-size: var(--text-lg);
    color: var(--color-text-secondary);
    text-wrap: pretty;
    max-inline-size: 48ch;
    margin-inline: auto;
    margin-block-end: var(--space-lg);
}
.voice-block__cta {
    font-family: var(--font-body);
    font-weight: 600;
    padding: var(--space-sm) var(--space-xl);
    background: var(--color-primary);
    color: var(--color-text-on-primary);
    border: 2px solid transparent;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: background var(--transition-base), box-shadow var(--transition-base);
}
.voice-block__cta:hover {
    background: color-mix(in oklch, var(--color-primary) 85%, black);
    box-shadow: var(--shadow-md);
}
/* Image en dessous — émerge dans le viewport */
.voice-block__visual {
    position: relative;
    inline-size: min(100%, 1200px);
    margin-inline: auto;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
    mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
}
.voice-block__visual img {
    display: block;
    inline-size: 100%;
    block-size: auto;
    object-fit: cover;
}
/* Entrée animée — @starting-style */
@starting-style {
    .voice-block__content {
        opacity: 0;
        translate: 0 var(--reveal-y);
    }
    .voice-block__visual {
        opacity: 0;
        scale: 0.96;
    }
}
.voice-block__content {
    transition: opacity 0.8s var(--ease-out-expo), translate 0.8s var(--ease-out-expo);
}
.voice-block__visual {
    transition: opacity 1s var(--ease-out-expo) 0.2s, scale 1s var(--ease-out-expo) 0.2s;
}
```

---

### VB-10 : Full-bleed overlay

```css
@property --overlay-opacity {
    syntax: '<number>';
    initial-value: 0.55;
    inherits: false;
}
.voice-block {
    position: relative;
    min-block-size: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding-block: var(--space-3xl) var(--space-2xl);
    padding-inline: var(--space-2xl);
    overflow: hidden;
    color: var(--color-text-on-depth);
}
/* Image fond — absolute, couvre tout */
.voice-block__bg {
    position: absolute;
    inset: 0;
    z-index: 0;
}
.voice-block__bg img {
    display: block;
    inline-size: 100%;
    block-size: 100%;
    object-fit: cover;
}
/* Gradient de lisibilité directionnel */
.voice-block__bg::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to top,
        color-mix(in oklch, var(--color-depth) 90%, transparent) 0%,
        color-mix(in oklch, var(--color-depth) 50%, transparent) 30%,
        color-mix(in oklch, var(--color-depth) 15%, transparent) 55%,
        transparent 80%
    );
    mix-blend-mode: multiply;
    pointer-events: none;
}
/* Overlay coloré teinté — harmonise l'image avec la palette */
.voice-block::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(
        ellipse at 30% 70%,
        color-mix(in oklch, var(--color-primary) 15%, transparent),
        transparent 65%
    );
    z-index: 1;
    pointer-events: none;
}
.voice-block__content {
    position: relative;
    z-index: 2;
    max-inline-size: 680px;
}
.voice-block__title {
    font-family: var(--font-display);
    font-size: clamp(var(--text-4xl), 10vw, 10rem);
    font-weight: 700;
    line-height: 0.95;
    text-wrap: balance;
    margin-block-end: var(--space-md);
    text-shadow: 0 2px 30px color-mix(in oklch, var(--color-depth) 40%, transparent);
}
.voice-block__lead {
    font-family: var(--font-body);
    font-size: var(--text-lg);
    color: color-mix(in oklch, var(--color-text-on-depth) 80%, transparent);
    max-inline-size: 42ch;
    text-wrap: pretty;
    margin-block-end: var(--space-xl);
}
.voice-block__cta {
    font-family: var(--font-body);
    font-weight: 600;
    padding: var(--space-sm) var(--space-xl);
    background: color-mix(in oklch, var(--color-surface) 15%, transparent);
    color: var(--color-text-on-depth);
    border: 1.5px solid color-mix(in oklch, var(--color-surface) 30%, transparent);
    border-radius: var(--radius-md);
    cursor: pointer;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    transition: background var(--transition-base), border-color var(--transition-fast), box-shadow var(--transition-base);
    align-self: flex-start;
}
.voice-block__cta:hover {
    background: color-mix(in oklch, var(--color-surface) 25%, transparent);
    border-color: color-mix(in oklch, var(--color-surface) 50%, transparent);
    box-shadow: 0 4px 16px color-mix(in oklch, var(--color-surface) 12%, transparent), 0 12px 40px color-mix(in oklch, var(--color-surface) 6%, transparent);
}
/* Entrée animée */
@starting-style {
    .voice-block__content {
        opacity: 0;
        translate: 0 30px;
    }
}
.voice-block__content {
    transition: opacity 0.8s var(--ease-out-expo), translate 0.8s var(--ease-out-expo);
}
```

---

## ATMOSPHERE BLOCK PATTERNS

### AT-1 : Sombre (inversion)

```css
.atmosphere-block {
    padding-block: var(--space-2xl) var(--space-xl);
    background: var(--color-depth);
    color: var(--color-text-on-depth);
    position: relative;
    overflow: hidden;
}
.atmosphere-block::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse at 20% 80%,
            color-mix(in oklch, var(--color-primary) 12%, transparent),
            transparent 50%),
        radial-gradient(ellipse at 80% 20%,
            color-mix(in oklch, var(--color-accent) 8%, transparent),
            transparent 50%);
}
.atmosphere-block__content {
    position: relative;
    z-index: 1;
    max-inline-size: 720px;
    margin-inline: auto;
    padding-inline: var(--space-lg);
    text-align: center;
}
.atmosphere-block__quote {
    font-family: var(--font-display);
    font-size: var(--text-2xl);
    font-weight: 400;
    font-style: italic;
    line-height: 1.5;
    color: var(--color-text-on-depth);
    margin-block-end: var(--space-lg);
    text-wrap: balance;
}
.atmosphere-block__tagline {
    font-family: var(--font-body);
    font-size: var(--text-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: color-mix(in oklch, var(--color-accent) 70%, var(--color-text-on-depth));
}
.atmosphere-block a {
    color: var(--color-accent);
    text-decoration: none;
    border-block-end: 1px solid color-mix(in oklch, var(--color-accent) 30%, transparent);
    transition: border-color var(--transition-fast), color var(--transition-fast);
}
.atmosphere-block a:hover {
    color: color-mix(in oklch, var(--color-accent) 80%, white);
    border-color: var(--color-accent);
}
```

### AT-2 : Clair (continuation)

```css
.atmosphere-block {
    padding-block: var(--space-xl) var(--space-lg);
    background: color-mix(in oklch, var(--color-surface) 95%, var(--color-primary));
    color: var(--color-text-primary);
    position: relative;
    border-block-start: 1px solid color-mix(in oklch, var(--color-primary) 10%, transparent);
}
.atmosphere-block::before {
    content: '';
    position: absolute;
    inset: 0;
    box-shadow: inset 0 20px 40px color-mix(in oklch, var(--color-primary) 4%, transparent);
    pointer-events: none;
}
.atmosphere-block__content {
    position: relative;
    max-inline-size: 680px;
    margin-inline: auto;
    padding-inline: var(--space-lg);
    text-align: center;
}
.atmosphere-block__quote {
    font-family: var(--font-display);
    font-size: var(--text-xl);
    font-weight: 400;
    line-height: 1.6;
    color: var(--color-text-primary);
    margin-block-end: var(--space-md);
    text-wrap: balance;
}
.atmosphere-block__tagline {
    font-family: var(--font-body);
    font-size: var(--text-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--color-text-secondary);
}
.atmosphere-block a {
    color: var(--color-primary);
    text-decoration: none;
    border-block-end: 1px solid color-mix(in oklch, var(--color-primary) 25%, transparent);
    transition: border-color var(--transition-fast), color var(--transition-fast);
}
.atmosphere-block a:hover {
    color: color-mix(in oklch, var(--color-primary) 80%, black);
    border-color: var(--color-primary);
}
```

### AT-3 : Coloré (saturation)

```css
@property --atmo-hue {
    syntax: '<number>';
    initial-value: 0;
    inherits: false;
}
.atmosphere-block {
    padding-block: var(--space-2xl) var(--space-xl);
    background: linear-gradient(135deg,
        var(--color-primary),
        color-mix(in oklch, var(--color-secondary) 60%, var(--color-accent)));
    color: var(--color-text-on-primary);
    position: relative;
    overflow: hidden;
}
.atmosphere-block::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 70% 30%,
        color-mix(in oklch, var(--color-accent) 30%, transparent),
        transparent 60%);
    mix-blend-mode: overlay;
    opacity: 0.7;
}
.atmosphere-block__content {
    position: relative;
    z-index: 1;
    max-inline-size: 720px;
    margin-inline: auto;
    padding-inline: var(--space-lg);
    text-align: center;
}
.atmosphere-block__quote {
    font-family: var(--font-display);
    font-size: var(--text-2xl);
    font-weight: 500;
    line-height: 1.5;
    text-wrap: balance;
    margin-block-end: var(--space-lg);
    text-shadow: 0 2px 20px color-mix(in oklch, var(--color-depth) 30%, transparent);
}
.atmosphere-block__tagline {
    font-family: var(--font-body);
    font-size: var(--text-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: color-mix(in oklch, var(--color-text-on-primary) 80%, transparent);
}
.atmosphere-block a {
    color: inherit;
    text-decoration: none;
    border-block-end: 1px solid color-mix(in oklch, currentColor 40%, transparent);
    transition: border-color var(--transition-fast), opacity var(--transition-fast);
}
.atmosphere-block a:hover {
    opacity: 0.85;
    border-color: currentColor;
}
```

### AT-4 : Texturé (matière)

```css
.atmosphere-block {
    padding-block: var(--space-2xl) var(--space-xl);
    background: var(--color-surface);
    color: var(--color-text-primary);
    position: relative;
    overflow: hidden;
}
.atmosphere-block__noise {
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: 0.4;
}
.atmosphere-block__noise svg {
    width: 100%;
    height: 100%;
}
/* In HTML: <div class="atmosphere-block__noise"><svg><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#noise)"/></svg></div> */
.atmosphere-block::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom,
        color-mix(in oklch, var(--color-primary) 6%, transparent),
        color-mix(in oklch, var(--color-secondary) 4%, transparent));
    background-blend-mode: multiply;
    mask-image: radial-gradient(ellipse at 50% 50%, black, transparent 80%);
    -webkit-mask-image: radial-gradient(ellipse at 50% 50%, black, transparent 80%);
}
.atmosphere-block__content {
    position: relative;
    z-index: 1;
    max-inline-size: 680px;
    margin-inline: auto;
    padding-inline: var(--space-lg);
    text-align: center;
}
.atmosphere-block__quote {
    font-family: var(--font-display);
    font-size: var(--text-xl);
    font-weight: 400;
    line-height: 1.6;
    margin-block-end: var(--space-md);
    text-wrap: balance;
}
.atmosphere-block__tagline {
    font-family: var(--font-body);
    font-size: var(--text-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--color-text-secondary);
}
.atmosphere-block a {
    color: var(--color-primary);
    text-decoration: none;
    border-block-end: 1px solid color-mix(in oklch, var(--color-primary) 20%, transparent);
    transition: border-color var(--transition-fast), color var(--transition-fast);
}
.atmosphere-block a:hover {
    color: color-mix(in oklch, var(--color-primary) 75%, black);
    border-color: var(--color-primary);
}
```
