# Editorial Patterns — Rédaction des sections textuelles (01, 02, 06)

Patterns rédactionnels et formels pour les sections **01 BIG IDEA**, **02 CONCEPT** et **06 VOICE & TONE**. Pour la structure générale, voir `structure.md`. Pour les règles formelles transverses, voir `style-guide.md`.

---

## 1. Principe directeur — Éditorial minimaliste

Ces sections sont **textuelles**. Le brand book n'est pas un poster Behance, c'est un **livre éditorial**. Le but : un texte qui respire, où chaque mot porte.

### Ce qu'on ne fait PAS
- **PAS de statement-poster gigantesque** : titre H1 à 200px qui occupe l'écran et noie le contenu.
- **PAS de méta-fields en grille** style "Type / Date / Client / Studio" en haut de page (c'est un format style-frame d'agence, pas un brand book).
- **PAS de bullet points** : les bullets fragmentent la pensée. On veut du texte courant qui se lit comme un essai.
- **PAS de boîtes décoratives** autour du texte (cards, encadrés colorés, fond accent en aplat sur tout le bloc).
- **PAS de divider lines décoratives** entre paragraphes.

### Ce qu'on fait
- Texte courant aligné à gauche, en **colonne 55ch**.
- Hiérarchie typo claire (eyebrow → H1 → sous-titre italique → corps).
- Beaucoup d'air en haut, en bas, à gauche et à droite.
- Les paragraphes courts (2-4 lignes), espacés par un `margin-block: 1.2em`.

---

## 2. La colonne 55ch — Largeur de lecture confortable

```css
.editorial-column {
  max-width: 55ch;
  margin-inline: auto;          /* ou margin-left: 0 si on veut un alignement à gauche fort */
  font-family: var(--brand-body);
  font-size: clamp(17px, 1.4vw, 20px);
  line-height: 1.55;
}
```

**Pourquoi 55ch ?**
- En dessous de ~45ch : le texte est haché, l'œil rebondit toutes les 5 mots, fatigant.
- Au-delà de ~75ch : le texte est trop large, le lecteur perd la ligne quand il revient à la marge.
- **55ch** = largeur canonique des livres bien typographiés (~10-11 mots par ligne).

**Variantes acceptables** :
- `60ch` si le corps est en sans-serif compact (gain de confort marginal)
- `50ch` si le corps est en serif large (gain de respiration)
- Jamais au-delà de `65ch` ni en dessous de `48ch`.

---

## 3. Hiérarchie typographique — Big Idea & Concept

### Eyebrow (section label)
- Format : `01 — BIG IDEA` (numéro + tiret cadratin + nom de section en caps).
- Taille : `clamp(11px, 0.9vw, 13px)`.
- Couleur : `var(--brand-color-accent)` (la couleur d'accent de la marque, ex: Foyer du Phare pour Camille).
- Letter-spacing : `0.12em` à `0.18em` (caps petites espacées).
- Font : `var(--brand-body)` en `font-weight: 500` ou `var(--brand-display)` en taille petite — au choix selon la marque.
- Marge sous l'eyebrow avant le H1 : `clamp(24px, 3vh, 48px)`.

### H1 — Titre concept (3-4 mots maximum)
- Taille : `clamp(48px, 6vw, 96px)`.
- Font : `var(--brand-display)`.
- **JAMAIS une phrase entière** : le H1 est une formule-clé, pas une description.
- Couleur : `var(--brand-color-positive-text)` (le texte principal sur fond clair).
- Line-height : `1.05` à `1.1` (compact, le H1 occupe peu de lignes).
- Tracking : légèrement négatif (`letter-spacing: -0.02em`) si la display l'autorise.

**Exemples concrets** :
- Camille (Le Phare de Ralliement) → H1 : **"Le phare immobile"** (3 mots).
- Camille alt → H1 : **"Repère codifié"** (Concept).

### Sous-titre italique (optionnel)
- Format : 1 phrase de 4-12 mots, en italique, en `var(--brand-display)` ou `var(--brand-body)`.
- Taille : `clamp(20px, 1.8vw, 28px)`.
- Couleur : `var(--brand-color-accent)` ou un dérivé proche (ex: Foyer du Phare adouci).
- Rôle : porter la **formule-signature** de la marque (ce qu'on retient à l'oral).
- Marge entre H1 et sous-titre : `clamp(16px, 2vh, 32px)`.

**Exemple Camille** :
- H1 : "Le phare immobile"
- Sous-titre italique : *"dans la matière qui tourbillonne."*

### Corps — 3-5 paragraphes courants
- Taille : `clamp(17px, 1.4vw, 20px)`.
- Font : `var(--brand-body)`.
- Line-height : `1.55` à `1.65`.
- Espacement entre paragraphes : `margin-block: 1.2em`.
- **2-4 lignes par paragraphe** en moyenne. Un paragraphe = une idée.
- Marge entre sous-titre et premier paragraphe : `clamp(48px, 6vh, 80px)`.

---

## 4. Pattern spécifique — 01 BIG IDEA (exemple Camille)

```
01 — BIG IDEA                                        (eyebrow accent caps)

Le phare immobile                                    (H1 display, 3 mots)
dans la matière qui tourbillonne.                    (sous-titre italique accent)

Camille n'invente pas un repère. Il en formalise     (corps, ~55ch, 4 paragraphes)
un qui existait déjà — silencieux, partagé, jamais
nommé. C'est le geste codifié d'une posture qui
attendait sa syntaxe.

[Paragraphe 2 — pourquoi cette idée maintenant]

[Paragraphe 3 — comment elle se traduit en design]

[Paragraphe 4 — qui elle rallie]
```

**Notes** :
- 4 paragraphes max. Si on dépasse, c'est que la Big Idea n'est pas claire.
- Le dernier paragraphe peut se terminer sur une phrase-écho qui prolonge le sous-titre italique.

---

## 5. Pattern spécifique — 02 CONCEPT (exemple Camille)

```
02 — CONCEPT                                         (eyebrow)

Repère codifié                                       (H2 display, 2 mots)

[Corps en colonne 55ch — 4-5 paragraphes qui développent
la métaphore du phare maritime : le faisceau qui ne
tourne pas mais qui éclaire ; le code lumineux propre
à chaque phare ; la matière (granit, fonte) qui dure ;
la fonction d'orientation collective.]
```

### Option : manifesto split (2-cols asymétriques)

Si la marque a un **manifesto fort** (3-5 lignes capitalisées qui font signature, type "Nous croyons que…"), on peut le présenter en split 2-cols asymétriques sous le corps principal :

```
┌─────────────────────────┬───────────────────────────────────┐
│ MANIFESTO               │ Glose courte qui contextualise    │
│                         │ le manifesto en 2-3 lignes        │
│ Nous ne décrivons       │ courantes. Sert de transition     │
│ pas la mer.             │ vers la suite.                    │
│ Nous calons             │                                   │
│ le foyer.               │                                   │
│                         │                                   │
│ 35%                     │ 65%                               │
└─────────────────────────┴───────────────────────────────────┘
```

- Colonne manifesto : 35% de la largeur, texte en `var(--brand-display)` taille moyenne (~clamp 28-44px), capitalisé optionnel, line-height très serrée (1.05-1.1).
- Colonne glose : 65% de la largeur, texte en `var(--brand-body)` taille corps standard, line-height 1.55.
- Aligner les deux colonnes sur la même grille de baseline (top aligned).
- **N'utiliser le split que si le manifesto existe et tient en 3-5 lignes capitalisées**. Sinon, le concept reste en single-column.

---

## 6. Pattern spécifique — 06 VOICE & TONE

### 6.1 Pull-quote géante (mode immersif)

La voix de la marque se ressent. **Une citation signature** occupe une page pleine, en très grand display.

```
                  Nous ne décrivons pas la mer.                  (pull-quote display, ~72-96px,
                  Nous calons le foyer.                          centrée ou aligned-left selon
                                                                  registre, italique optionnel)

                              — voix Camille                     (attribution discrète bas-droite,
                                                                  eyebrow caps petites)
```

**Règles** :
- Taille : `clamp(56px, 6vw, 96px)`.
- Font : `var(--brand-display)`.
- Italique optionnel (selon la display — Gloock italique fonctionne bien, Inter italique non).
- Line-height : `1.05` à `1.15`.
- **PAS de guillemets ouvrants gigantesques** style Pinterest ("« en 200px en couleur fluo"). Sobriété absolue : pas de guillemets décoratifs, juste le texte.
- Si l'on veut des guillemets, utiliser les guillemets français `«` et `»` en taille normale, intégrés au texte.
- Attribution en bas-droite ou bas-gauche en eyebrow caps petites (`— voix {brand}` ou `— {brand} brand voice`).

### 6.2 Tone descriptors

3 à 5 adjectifs principaux qui résument la voix, chacun avec **1 ligne d'explication concrète** (pas un dictionnaire).

Format en **grille horizontale** (1 colonne par descriptor) :

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ POSÉ         │ CODIFIÉ      │ FRATERNEL    │ SANS GRAS    │
│              │              │              │              │
│ Parle bas,   │ Choisit des  │ Inclut sans  │ Énonce sans  │
│ pas vite.    │ mots qui     │ supplier.    │ jamais       │
│              │ tiennent     │              │ exhorter.    │
│              │ dans le      │              │              │
│              │ temps.       │              │              │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

- Eyebrow caps pour le descriptor : `var(--brand-color-accent)`, taille `clamp(13px, 1vw, 16px)`, letter-spacing `0.14em`.
- Glose en `var(--brand-body)` taille normale (`clamp(15px, 1.2vw, 17px)`), `line-height: 1.5`.
- Si 5 descriptors et écran étroit : passer en grille 2-3 colonnes avec retour à la ligne automatique.

### 6.3 Do / Don't

4 à 6 paires d'exemples concrets. Le but : **donner à voir** le tone en action.

```
┌──────────────────────────────────────┬──────────────────────────────────────┐
│ DO                                   │ DON'T                                │
│ (accent — Foyer du Phare ou équiv.)  │ (gris neutre, PAS rouge)             │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ « Le foyer reste, la matière tourne. │ « Révolutionnez votre relation à la  │
│   Trouvez votre point d'appui. »     │   permanence avec notre solution     │
│                                      │   disruptive ! »                     │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ « Un code, deux faisceaux, mille     │ « Le leader incontournable de la     │
│   marins. »                          │   nouvelle ère des repères. »        │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

**Règles** :
- 4 à 6 paires. Au-delà, c'est de la redondance.
- **Do en couleur d'accent positive** (Foyer du Phare, ou équivalent — pas vert pomme générique).
- **Don't en gris neutre** ou en `var(--brand-color-positive-text)` un peu atténué. **JAMAIS en rouge agressif** (c'est une convention web, pas un brand book).
- Texte des exemples en `var(--brand-body)`, italique optionnel pour marquer la citation.
- Label `DO` / `DON'T` en eyebrow caps en haut de colonne.
- Ligne `1px solid` discrète entre paires (couleur très atténuée), pas de cards.

---

## 7. Anti-patterns rédactionnels — Liste fermée

| Anti-pattern | Pourquoi c'est slop | À la place |
|--------------|---------------------|------------|
| Jargon brand-strategist : "nous incarnons un mindset de…", "ADN", "ownership", "purpose-driven" | Vide de sens, recyclé à l'infini | Mots concrets, verbes d'action |
| Superlatifs vides : "la première marque à…", "le seul acteur qui…" | Inflation publicitaire | Affirmation simple, factuelle |
| Tagline en H1 : "Recharger autrement.", "Innover. Réinventer." | Une tagline est de la pub, pas un titre éditorial | H1 = formule-clé conceptuelle |
| Phrases nominales pompeuses : "Innover. Réinventer. Transcender." | Slop poster typique | Phrases complètes, sujet + verbe |
| Empilement d'adjectifs : "audacieuse, créative, humaine, durable, responsable" | 5 adjectifs = 0 adjectif | 1-2 adjectifs précis qui tranchent |
| Métaphore filée jusqu'à l'absurde : "comme un phare qui éclaire la nuit du voyageur perdu sur la mer agitée de…" | Cliché poétique | Métaphore mesurée, posée une fois |
| Citation pseudo-philosophique pour le pull-quote : "L'essence se cache dans le détail." | Tumblr 2014 | Citation signature spécifique à la marque |
| "Notre mission est de…" en ouverture | Format pitch deck startup | Entrer directement dans le concept |
| Bullet points pour articuler le concept | Fragmente la pensée | Paragraphes courants |
| Citation centrée sur fond gradient arc-en-ciel | Slop AI-générique | Citation aligned-left sur fond uni positif |

---

## 8. Récapitulatif — Checklist avant de valider une section textuelle

- [ ] Eyebrow en caps + accent color ?
- [ ] H1 fait 3-4 mots maximum ?
- [ ] Sous-titre italique en accent si la marque a une formule-signature ?
- [ ] Corps en colonne 55ch, paragraphes de 2-4 lignes ?
- [ ] Pas de bullet, pas de méta-fields, pas de divider décoratif ?
- [ ] Padding vertical généreux (≥ 120px haut et bas) ?
- [ ] Aucun mot de jargon brand-strategist ?
- [ ] Aucun superlatif vide ?
- [ ] Le H1 n'est pas une tagline ?
- [ ] Le pull-quote n'a pas de guillemets gigantesques décoratifs ?
- [ ] Do en accent positive, Don't en gris neutre (PAS rouge) ?
