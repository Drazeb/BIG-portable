# Règles de génération — Design System Generator

> Règles sanctuarisées issues de l'itération validée sur Camille (mai 2026).
> Ces règles prévalent sur toute autre interprétation. Toute violation rend le DS rejetable.

---

## Règle 01 — Fond clair pour la doc, dark contextuel pour les éléments natifs dark

**Quoi.** Le fond global du document est l'équivalent `--color-chart-mist` (ou nom équivalent) de la marque — le clair de la palette. Pour Camille : `#E6ECF1`. Pour une marque où ce token n'existe pas : prendre la couleur la plus claire de la palette qui ne soit ni blanc pur ni gris technique.

**Exception majeure** : pour les sections où les éléments **vivent natively sur fond dark** (data visualization, photography, illustration pour une marque dark mode comme Camille), utiliser des **conteneurs locaux dark** qui montrent les éléments en condition réelle d'usage. Le fond global de la page reste clair — seuls les conteneurs spécifiques basculent en dark.

**Pourquoi.** Le DS est un document technique consulté en mode "manuel de référence" sur un grand écran, parfois imprimé. Le fond clair garantit lisibilité maximale du texte, neutralité, et n'épuise pas l'œil sur des longues sessions de consultation. MAIS : présenter un dataviz Camille sur fond clair quand il est calibré pour du dark (axes en 20% opacité texte clair, foyer chaud qui signale dans le noir) le dénature complètement — la grille devient invisible, le contraste s'écrase. Le DS doit montrer les éléments en **condition réelle d'usage**, sinon c'est une trahison du système.

**Comment.**
- Background global : un seul fond clair (`--color-chart-mist` ou équivalent), sans gradient, sans image, sans variation entre sections.
- Surfaces cards / tables / swatches : blanc légèrement teinté froid (`oklch(0.985 0.004 240)`) pour le micro-contraste.
- **Conteneurs dark contextuels** (uniquement pour Photo / Data viz / Illustration / Motion si la marque est dark) :
  - Fond `var(--color-night)` ou `var(--color-abyss)` selon densité
  - Padding généreux pour respirer
  - Radius conforme à la marque (`--radius-xs`)
  - Tout le contenu interne en couleurs dark mode natives
  - Label discret au-dessus pour signaler "vu en condition réelle" (overline mono, optionnel)

**Anti-exemple.** Hero painterly comme dans le brand book. Background qui varie entre sections (les "chapters" du Batch 2). Gradient mesh. Mini-graphique dataviz Camille sur fond clair (la grille en 20% opacité texte clair devient invisible).

---

## Règle 02 — Type scale documenté = type scale appliqué

**Quoi.** Toute taille `font-size` utilisée dans le doc DOIT être présente dans la section Typography du DS. Pas de valeur ad hoc.

**Pourquoi.** Un DS qui prêche un type scale mais utilise des tailles libres est auto-incohérent et perd toute crédibilité auprès d'un dev qui ouvre le fichier. C'est la première chose qu'un designer junior va vérifier.

**Comment.**
- Auditer le type scale présent dans `design-specs §03.2`.
- Compléter avec le **H3 sub-section** (`clamp(1.3rem, 2.2vw, 1.9rem)` Gloock 400) qui est présent dans Batch 2/3 (`.subsection__name`) mais souvent absent du design-specs.md. **Le mentionner explicitement dans le DS** avec note "sourcé Batch 2/3".
- Mapper rigoureusement :
  - H1 page title → H2 chapitre
  - H2 section title → H2 chapitre (même token — distinction par le numéro 01/02/03 à gauche)
  - H3 sub-section title → H3 sub-section (nouveau token)
  - Body → `--text-base`
  - Captions, eyebrows, labels → `--text-sm` / `--fs-overline` / `--text-xs`
  - Nom de token (ex "Nuit d'Indigo") → `--text-base` Gloock
  - Logo wordmark sidebar → taille libre (c'est un logo, pas du texte)

**Anti-exemple.** `font-size: 1.8rem` fixe pour les section titles quand le scale documente `clamp(2.5rem, 5vw, 4.5rem)`. `font-size: 1.05rem` pour les noms de token quand `--text-base: 1rem` existe.

**Test auto.** Le script `design-system-audit.py` doit grep toutes les valeurs `font-size:` du fichier et vérifier qu'elles correspondent à une entrée du type scale.

---

## Règle 03 — Grammaire visuelle Batch 2/3 reprise

**Quoi.** Le DS reprend les signatures visuelles atomiques du Batch 2/3 pour rester reconnaissable comme document de la marque, sans tomber dans le brand book.

**Pourquoi.** Sans ces signatures, le doc est un Carbon générique anonyme. Avec, il devient "le DS de cette marque". L'équilibre est subtil : reprendre les signatures *structurelles* (hairlines, marks, overlines), pas les signatures *atmosphériques* (gradients chapter, image hero, overlays radiaux).

**Comment — éléments à reprendre obligatoirement :**

1. **Hairline verticale diagonale** : 1px gradient Foyer à gauche de la zone main, traverse toute la hauteur. Atténuer la couleur pour qu'elle tienne sur fond clair (opacity 0.10-0.55 selon position).
2. **Beacon mark** : cercle 12px radial-gradient Foyer + box-shadow chaleureux, en tête de la hairline.
3. **Overlines** : texte mono uppercase letter-spacing 0.30em, précédé d'une barre horizontale 28-56px de 1px Foyer.
4. **Dotted underlines** sur les sub-section heads (`border-block-end: 1px dotted oklch(0.27 0.045 248 / 0.10)` adapté au fond clair).
5. **Numérotation sub-section** en Mono Foyer letter-spacing 0.20em (`01.1`, `01.2`…).
6. **Radius unique** : utiliser le radius unique de la marque (Camille = 2px).

**Comment — éléments à NE PAS reprendre :**

- Backgrounds chapter colorés (chaque chapitre Batch 2 a son fond Abyss ou Night) → un seul fond clair.
- Overlays radiaux atmosphériques (les `.chapter::before` du Batch 2) → aucun overlay.
- Grain SVG tuilé → aucun grain (le doc est un fichier technique pur).
- Hero image / cover band → aucune image décorative.
- Chapter shells avec padding-block variable → padding uniforme entre sections.

---

## Règle 04 — Pas d'encadrés génériques (anti-AI-slop)

**Quoi.** Aucun bloc d'emphase ne doit ressembler à un encadré générique d'AI assistant : pas de "barre verticale colorée 2-4px à gauche d'une box avec border + padding + radius".

**Pourquoi.** C'est LA signature visuelle de l'AI-slop. Tout designer qui voit ça pense "ChatGPT a écrit le doc". Le DS d'une marque premium doit signaler par d'autres mécanismes.

**Comment — pour les blocs spéciaux (loi, don't, banner test, etc.) :**

- Pas de `border-left: Xpx solid var(--accent)`.
- Pas de `background: var(--surface) + border: 1px + border-radius: var(--radius-xs)` en pattern systématique.
- À la place :
  - **Loi/règle** : zone séparée par 2 hairlines dotted horizontales (`border-block-start` + `border-block-end`), à l'intérieur : overline avec barre courte Foyer + statement Gloock italic H3 + liste de règles avec dashes.
  - **Don't** : liste verticale plate, chaque item en grid 2 colonnes (marker mono `01 / 02 / 03…` avec préfixe `× ` Foyer + texte du don't), hairlines dotted entre items.
  - **Banner test** : kicker overline en haut de page, hairline dotted en bas, pas de cadre.

**Anti-exemple — ne JAMAIS générer :**

```css
.color-law {
  background: var(--doc-surface);
  border: 1px solid var(--doc-border);
  border-left: 2px solid var(--doc-accent);
  border-radius: 2px;
  padding: 24px;
}
```

**Pattern à utiliser à la place :**

```css
.law {
  padding: var(--space-xl) 0 var(--space-lg) 0;
  border-block-start: 1px dotted oklch(0.27 0.045 248 / 0.20);
  border-block-end:   1px dotted oklch(0.27 0.045 248 / 0.20);
  /* pas de fond, pas de bordure cadre, pas de border-left */
}
```

---

## Règle 05 — Ton dev/factuel partout

**Quoi.** Toutes les phrases (intros section, intros sub-section, descriptions, justifs) sont écrites en ton dev : phrases courtes, énumérations, usage explicite. Pas de prose poétique style brand book.

**Pourquoi.** Le public est un dev / un designer junior qui doit utiliser le doc pour produire du code. Il ne veut pas qu'on lui raconte une histoire, il veut savoir où mettre quoi. Le brand book joue déjà le rôle de séduction — le DS doit jouer le rôle de manuel opérationnel.

**Comment — barème.**

| À écrire (✓) | À éviter (✗) |
|--------------|--------------|
| « 9 couleurs en 4 rôles. Système binaire 99/1. » | « La palette Nuit d'Indigo organise neuf couleurs en quatre rôles : matière dominante, signal ponctuel, registre clair documentaire, échelle de texte. » |
| « Sérif display, empattements affirmés, mono-weight. **Usage** : titres hero, manifesto, ouvertures de chapitre. » | « Sérif patrimonial à empattements affirmés. Gravité éditoriale brûlante. Pleins/déliés contrastés qui dialoguent avec les coups de brosse de l'image-pivot. » |
| « Pas de valeur intermédiaire entre aéré et compact. » | « La modération molle est l'erreur. » |
| « Toute valeur d'espacement utilise un de ces 8 tokens. Pas d'interpolation. » | « Cadence d'éclats : un éclat, beaucoup de silence, un éclat. » |

**Exceptions sacrées (à NE PAS dé-poétiser) :**

1. **Les noms de tokens** : `Foyer du Phare`, `Nuit d'Indigo`, `Encre de Veille Bleutée`, etc. **Intouchables.** C'est l'identité.
2. **Les règles formelles courtes** : `99 / 1`, `1.5 px canonique`, `Échelle 8px Fibonacci`. Peuvent être emphased en Gloock italic H3 dans une zone `.law`.
3. **La numérotation et les overlines** : `01 / 02 / 03`, `01.1 / 01.2`, `RÈGLE 99/1` — ce sont des conventions structurelles, pas du contenu.

**Mots-marqueurs à débusquer** (souvent symptôme de prose poétique) :
- « matière », « instrumental », « cadence », « éclats », « monumental », « patrimonial », « portant », « repère », « signal » (au sens littéraire, pas UX), « bordée », « cadence », « éphéméride »…

À chaque occurrence, vérifier : est-ce un nom de token (intouchable) ? une règle (OK) ? ou de la prose à dé-poétiser ?

---

## Règle 06 — Sourcing strict des don'ts

**Quoi.** Tout item d'une section "Don't" DOIT être présent textuellement (ou en reformulation directe) dans :
- `design-specs.md §12 Don'ts — Anti-direction` (source principale)
- OU dans une règle explicite d'une sous-section (ex: §03.1 "Pas de troisième fonte")

**Aucune extrapolation, aucune dérivation logique, aucune invention.**

**Pourquoi.** Un don't non sourcé n'est pas opposable. Si un dev demande "où est-ce écrit qu'on ne peut pas faire X ?", il faut pouvoir pointer la source. Sinon c'est l'opinion du générateur, pas la règle de la marque.

**Comment.** Le sub-agent générateur doit produire un fichier `.audit-sources.json` qui mappe chaque don't à sa ligne source :

```json
{
  "color_donts": [
    { "text": "Pur noir #000000 comme fond...", "source": "design-specs.md L461" },
    { "text": "Pur blanc #FFFFFF comme texte...", "source": "design-specs.md L462" }
  ],
  "typo_donts": [
    { "text": "Inter / Helvetica par défaut...", "source": "design-specs.md L482" },
    { "text": "Troisième fonte...", "source": "design-specs.md L103" }
  ]
}
```

Le script d'audit vérifie que chaque don't a un mapping valide.

**Anti-exemple — ne JAMAIS générer comme don't :**
- « Multiplier les valeurs hors tokens — toute valeur en pixel libre est interdite » (déduction)
- « Régler l'inter-section au pifomètre » (invention)
- « Compacter une zone aérée pour gagner du scroll » (dérivation)

**Si une section a 0 ou 1 seul don't sourcé** : c'est OK. La section don't peut être minimale (1 item) ou même omise si la source n'en a pas. **Mieux vaut 1 don't sourcé que 4 inventés.**

---

## Règle 07 — Sidebar nav numérotée standard Carbon-like

**Quoi.** Sidebar fixe à gauche (260px), avec :
- Logo wordmark de la marque en haut
- Sous-titre `Design System · v0.1` (ou version courante)
- Groupes de navigation labélisés `Foundations` / `Identity` / `Assets` / `Patterns` (selon découpage)
- Liens numérotés `01 / 02 / 03…` en Mono
- Indicateur d'état actif via `border-left: 2px solid var(--accent)`
- Métadonnées de marque en bas (concept, calibrage, style officiel)

**Pourquoi.** C'est la convention universelle. Un dev qui ouvre Carbon, Atlassian, Polaris, Material trouve la même structure. Ne pas la respecter = forcer l'utilisateur à apprendre une UX spécifique.

**Comment.**
- Sidebar position `sticky`, top 0, full-height scrollable indépendamment.
- Liens à venir (futures sections) : `opacity: 0.4; pointer-events: none` (visible mais désactivés).
- Pas de logo agrandi, pas d'icône, pas de search bar (overkill pour un doc statique).

---

## Règle 08 — Bloc `:root` final prêt à copier

**Quoi.** À la fin du doc (avant le footer), une section "Tokens" affiche le bloc CSS `:root { ... }` complet, dans un `<pre><code>` sélectionnable, copiable d'un clic. Affichage avec syntax highlighting passif (couleurs CSS rendues visuellement à côté des valeurs).

**Pourquoi.** C'est le livrable utilitaire numéro 1 du DS. Un dev qui veut commencer à coder ouvre le DS, va à la section Tokens, copie-colle le `:root` dans son projet, et est prêt. Sans cette section, le DS reste un document descriptif et oblige le dev à reconstruire les tokens à la main.

**Comment.**
- Bloc strictement identique au style-tile source (cohérence absolue — vérifié par audit).
- Ajouter un bouton "Copier" en haut à droite du bloc (optionnel, JS minimal).
- Commenter par catégorie : `/* === PALETTE === */`, `/* === TYPOGRAPHIE === */`, etc.

---

## Règle 09 — Mention explicite des choix d'architecture

**Quoi.** Si la marque utilise des **tokens flat** (pas de hiérarchie primitive / semantic / component), le mentionner dans une mini-section "Token architecture" en début de la section Tokens.

**Pourquoi.** Un dev qui prend en main un DS s'attend par défaut à une hiérarchie 3 niveaux (c'est ce que font Material, Carbon, Polaris). Si on est flat, il faut le dire pour qu'il ne cherche pas la hiérarchie. C'est un choix conscient à expliquer, pas une lacune à cacher.

**Comment.** Court paragraphe :

> « Ce design system utilise des tokens à 1 niveau (semantic uniquement). Pas de couche primitive en amont (les valeurs sont nommées directement par leur rôle, ex: `--color-beacon` plutôt que `--orange-500`), pas de couche component en aval (les composants utilisent les tokens semantic directement, ex: `var(--color-beacon)` dans `.cta-primary` plutôt qu'un `--button-primary-bg` dédié). Ce choix est cohérent avec une marque mono-thème mono-brand. Pour theming dark/light ou multi-brand, il faudrait introduire la couche primitive. »

Si la marque a une hiérarchie complète, mentionner les 3 niveaux et leur convention de nommage.

---

## Règle 10bis — Utilisation OBLIGATOIRE de visual-final/

**Quoi.** Si le dossier session contient `visual-final/` avec des visuels de la marque, le sub-agent générateur DOIT les utiliser dans :

- **Section Photography** : 1 visuel par cadrage canonique documenté (ex pour Camille : `hero` pour Surplomb aérien 3:4, `atmosphere-*` pour Plein-plan latéral 16:10, `macro-halo` pour Macro foyer 1:1, `pov-depuis-phare` pour POV 4:5). Les visuels sont présentés dans des conteneurs dark contextuels (cf R01).
- **Section Illustration** : 3-6 visuels qui montrent la **physique de l'illustration** documentée (brushwork directionnel + plans atmosphériques + foyer ponctuel pour Camille). Présentés en grille dans un grand conteneur dark.
- **Section Color (optionnel)** : un visuel hero peut illustrer "Foyer du Phare en condition réelle" dans une mini-démonstration.

**Pourquoi.** Le DS n'est pas un document théorique — c'est un manuel d'usage. Un designer qui consulte la section Photography doit voir **immédiatement** ce à quoi ressemble un cadrage Surplomb aérien Camille, pas lire une description textuelle. Pareil pour la physique d'illustration. Les visuels existent, sont validés, sont la référence canonique — les ignorer est une faute professionnelle.

**Comment.**
- Copier les visuels nécessaires depuis `{session}/visual-final/` vers `{output_dir}/visual-final/` (chemin relatif simple `visual-final/...` depuis le HTML).
- Ne pas embarquer en base64 (les fichiers font 2-3 MB chacun, ça exploserait le HTML).
- Utiliser `<img loading="lazy" decoding="async">` pour ne pas plomber le chargement initial.
- Légender chaque visuel sobrement : nom du cadrage / type / palette + mini-caption technique.
- Crop responsive : `object-fit: cover` avec aspect-ratio respectant le cadrage canonique (3:4, 16:10, 1:1, 4:5).

**Anti-exemple.** Générer un mockup SVG simple pour symboliser un cadrage quand un vrai visuel Camille de ce cadrage existe dans `visual-final/`. Décrire textuellement "brushwork visible partout" quand 9 PNG le démontrent.

**Si `visual-final/` est absent ou vide** : fallback sur des mockups SVG sobres OU placeholder textuel "[Visuel non généré — voir le pack final]". Ne pas inventer un visuel.

---

## Règle 11 — Mini-section "Voice" optionnelle

**Quoi.** Une dernière section courte (1 écran max) reprenant le `Tone of Voice` du design-specs §01.4 : vocabulaire signature, à faire, à ne pas faire.

**Pourquoi.** C'est la seule partie de §01 (Identité de marque) qui est actionable pour un dev / un PM / un copywriter. Le reste de §01 (Calibration A×B, Tension, Posture, ICP) appartient au brand book et ne sert pas à coder ou à rédiger les contenus produit.

**Comment.** Section "12 — Voice" en fin de doc, structure :
- Vocabulaire signature (liste de 10-15 mots issus de §01.4)
- À faire (3-5 puces)
- À ne pas faire (3-5 puces)

Si §01.4 est absent ou vide → omettre la section.

---

## Règle 12 — Inventaire 1:1 obligatoire (clone brand-book §8quater)

**Quoi.** AVANT de finaliser chaque sous-section du DS, le sub-agent générateur DOIT faire un inventaire de la sous-section source correspondante (compter les items, lister leurs noms exacts) et vérifier la présence **1:1** dans le DS. Si écart → ajouter les items manquants AVANT de finaliser.

**Pourquoi.** Sans inventaire forcé, le LLM générateur tend à produire « quelques exemples représentatifs » et à appauvrir la matière. C'est exactement ce qui s'est passé pour Camille v3 brand book (composants UI : 3 boutons au lieu de 8, pas de toggle) — d'où la sanctuarisation de cette règle côté brand-book le 27 mai 2026. Le DS doit appliquer la même règle.

**Comment — protocole pour le sub-agent générateur, à exécuter à la fin de chaque sous-section :**

1. Identifier la sous-section source correspondante dans `design-specs.md` (ex: §02.1 pour Color/Palette primaire).
2. Faire la liste exhaustive de ses items distincts (compter les lignes de table, les puces, les sous-titres).
3. Pour chaque item, vérifier sa présence dans le DS généré.
4. Si un item manque → l'ajouter immédiatement.
5. Si un item est dans le DS mais PAS dans la source → vérifier R13 (catalogage strict). S'il est inventé, le retirer.

**Anti-pattern interdit** : « j'ai mis quelques exemples représentatifs » → NON. Le DS doit refléter la **vraie densité** du système Camille (ou autre marque). Sous-représenter = trahir la valeur du pack identité.

**Trace obligatoire** : le sub-agent génère un fichier `{brand}-design-system-inventory.json` qui liste pour chaque sous-section les items attendus (source) vs présents (DS). Le script d'audit utilisera ce fichier pour vérification automatique.

Voir le **tableau inventaire-type** dans `SKILL.md` qui liste pour chaque section ce qu'il faut compter.

---

## Règle 13 — Catalogage strict, pas réinterprétation (élargissement de R06)

**Quoi.** Le DS ne PARAPHRASE pas, ne REFORMULE pas en "business-speak", ne DÉRIVE pas de conclusions logiques absentes de la source. Il RECOPIE ou compresse factuellement. Cette règle s'applique à TOUT le contenu, pas seulement aux don'ts.

**Pourquoi.** L'audit Camille v0.2 a montré 11 inventions sémantiques dont 6 captions d'icônes ré-écrites en business-speak (« Direction long terme — point fixe de référence pour la trajectoire » au lieu de « boussole abstraite » que dit la source). Le LLM générateur est tenté de "rendre actionable" en interprétant. C'est exactement ce qu'il NE DOIT PAS faire. Le DS est un catalogage, pas une explication.

**Comment — pour chaque type de contenu :**

| Type de contenu | Règle stricte |
|-----------------|---------------|
| **Captions / descriptions d'éléments visuels** (icônes, lockups, cadrages…) | RECOPIER la description formelle de la source. Si la source dit « boussole abstraite » → écrire « Boussole abstraite ». PAS « Direction long terme ». PAS « Point fixe de référence ». |
| **Usages de tokens / éléments** (palette, fontes, espacement…) | RECOPIER la colonne "Usage" du tableau source. Reformulation acceptable : enlever un adjectif décoratif. Reformulation INTERDITE : ajouter un critère, changer un mot-clé sémantique (ex: « micro-pulse » → « état actif »). |
| **Règles** (« 1 seul accent par vue », « stroke 1.5px canonique »…) | RECOPIER la règle exactement. Une règle n'est pas une indication, c'est une obligation. |
| **Don'ts** (déjà couvert par R06) | Source uniquement (§12 ou règle explicite d'une sous-section). |
| **Spécifications numériques** (ratios WCAG, tailles, durées…) | RECOPIER exactement. Pas d'arrondi, pas d'extrapolation. Si la source ne donne pas la valeur précise (ex: « sous le seuil AA »), NE PAS inventer un chiffre. |
| **Vocabulaire et nommage** (« Encre de Veille Bleutée », « Bleu marine de carte »…) | RECOPIER les noms EXACTS, qualificatifs inclus. Pas de simplification ("Encre de Veille" sans "Bleutée"). Pas de reformulation ("Modulation marine" au lieu de "Bleu marine de carte"). |

**Test à appliquer** : pour chaque phrase du DS, le sub-agent doit pouvoir pointer la ligne source qui la justifie. Si la phrase exprime quelque chose que la source ne dit pas explicitement → la retirer.

**Anti-pattern interdit — exemples concrets vus sur Camille v0.2 :**

- ❌ « Direction long terme — point fixe de référence pour la trajectoire » (caption icône Cap inventée)
- ✅ « Boussole abstraite » (description source)

- ❌ « Le foyer chaud peut pulse en opacité (0.85 → 1) sur --transition-slow » (règle motion extrapolée)
- ✅ « Fade-in d'opacité du halo » (formulation source)

- ❌ « Ratio Sextant Atténué : 3.1 : 1 » (chiffre inventé)
- ✅ « Sextant Atténué : sous le seuil AA — réservé aux usages décoratifs » (formulation source)

---

## Règle 14 — Checklist obligatoire par section (clone Batch 2)

**Quoi.** Le prompt du sub-agent générateur DOIT inclure, pour chaque section, une checklist explicite des items à inclure. À la fin de chaque section, le sub-agent coche mentalement et complète si nécessaire AVANT de passer à la suivante.

**Pourquoi.** Sans checklist explicite, le LLM oublie des items, surtout sur les sections riches (§04 Iconographie, §07 Photography, §10 Motion qui ont 5+ sous-sections chacune). Batch 2 utilise ce mécanisme depuis P15 (avril 2026), brand-book depuis §8quater (mai 2026). Le DS doit l'utiliser aussi.

**Comment.** La checklist exhaustive vit dans le **tableau inventaire-type** du `SKILL.md` (voir section "Périmètre standard — 10 sections" enrichie). Le prompt sub-agent doit lui rappeler avant de finaliser :

> « Pour chaque section, applique la checklist du tableau inventaire-type. Coche mentalement chaque item. **SI UN SEUL ITEM MANQUE → AJOUTE-LE AVANT DE FINALISER.** »

**Trace obligatoire** : le `.audit-sources.json` mappe chaque item de chaque section à sa source. Le script d'audit vérifie que la couverture est 100%.

---

## Checklist anti-régression

À vérifier sur tout DS généré avant de le présenter à l'utilisateur :

- [ ] **R01** Fond unique (= clair de la palette), aucun gradient, aucune image. Conteneurs dark contextuels OK pour data viz / photo / illustration
- [ ] **R02** Toute taille `font-size` du fichier est dans le type scale documenté en §02
- [ ] **R02bis** Le H3 sub-section est documenté dans le type scale
- [ ] **R03** Hairline verticale + beacon mark présents et visibles
- [ ] **R03bis** Overlines = barre courte 1px + texte mono uppercase letter-spacing 0.30em
- [ ] **R03ter** Sub-section heads avec dotted underline + numéro Mono Foyer 0.20em
- [ ] **R04** Aucun `border-left: Xpx solid var(--accent)` sur un bloc d'emphase
- [ ] **R04bis** Lois / don'ts construits avec hairlines dotted + overline + statement (pattern Camille validé)
- [ ] **R05** Lecture rapide du doc final : aucune phrase ne ressemble à du brand book (pas de "matière", "cadence", "instrumental"… hors noms de tokens et règles formelles)
- [ ] **R06** Chaque don't a une entrée dans `.audit-sources.json` qui pointe vers une ligne de design-specs.md
- [ ] **R07** Sidebar 260px avec nav numérotée + groupes + métadonnées marque
- [ ] **R08** Section Tokens en fin de doc avec `:root` complet, identique au style-tile source
- [ ] **R09** Token architecture documentée OU pas, selon décision
- [ ] **R10bis** Visuels de `visual-final/` utilisés pour Photography et Illustration si disponibles
- [ ] **R12** Inventaire 1:1 — pour chaque sous-section source, vérifier présence dans le DS via le fichier `{brand}-design-system-inventory.json`
- [ ] **R13** Catalogage strict — aucune phrase n'invente ou ne réinterprète. Captions d'icônes = description formelle source uniquement. Aucun chiffre WCAG inventé. Aucune règle motion extrapolée.
- [ ] **R14** Checklist exhaustive du tableau inventaire-type du SKILL.md respectée pour chaque section
- [ ] **PAS DE Voice** — section 12 Voice ne doit PAS être générée (décision tranchée mai 2026)

---

## Versions

- v0.1 — 28 mai 2026 — Règles initiales sanctuarisées après itération Camille (Color + Typography + Spacing validés). Auditeur Python à créer en étape 2.
