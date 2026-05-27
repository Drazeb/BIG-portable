# Audit de catégorisation typographique — Rapport complet

Date : 2026-03-18

Méthodologie : chaque font est vérifiée contre sa nature réelle (famille typographique connue). Les critères d'erreur sont :
- **GRAVE** (retirer) : confondre serif/sans-serif, confondre mono/proportionnel
- **Modérée** (garder) : confondre display-decorative et standard
- **Mineure** (garder) : erreur de sous-catégorie (grotesque vs humaniste, didone vs transitionnelle, etc.)

---

## 1. Display A1

| # | Font réelle | LLM dit | Correct ? | Nature de l'erreur |
|---|---|---|---|---|
| #01 | Brygada 1918 | Serif didone | ❌ | Mineure — Brygada 1918 est une serif old-style/transitionnelle, pas didone |
| #02 | Labrada | Sans-serif grotesque | ❌ | **GRAVE** — Labrada est une serif (cubaine, style éditorial avec empattements), catégorisée sans-serif |
| #03 | Gilda Display | Serif transitionnel | ✅ | Correct (didone/transitionnel acceptable) |
| #04 | Marcellus | Serif old-style | ❌ | Mineure — Marcellus est plutôt une serif inscriptionnelle/classique, pas vraiment old-style au sens Garamond, mais reste serif → acceptable |
| #05 | Faustina | Sans-serif grotesque | ❌ | **GRAVE** — Faustina est une serif transitionnelle, catégorisée sans-serif |
| #06 | Aleo | Slab serif | ✅ | Correct |
| #07 | Neuton | Serif didone | ❌ | Mineure — Neuton est plutôt transitionnelle/old-style, pas didone |
| #08 | Frank Ruhl Libre | Sans-serif géométrique | ❌ | **GRAVE** — Frank Ruhl Libre est une serif didone, catégorisée sans-serif |
| #09 | Libre Caslon Display | Serif mécane | ❌ | Mineure — Libre Caslon Display est une serif transitionnelle (Caslon), pas mécane |
| #10 | Noto Serif Display | Serif transitionnel | ✅ | Correct |
| #11 | Petrona | Sans-serif humaniste | ❌ | **GRAVE** — Petrona est une serif, catégorisée sans-serif |
| #12 | Signika | Slab serif | ❌ | **GRAVE** — Signika est une sans-serif (signage), catégorisée slab serif |
| #13 | Tinos | Serif transitionnel | ✅ | Correct (compatible Times-like) |
| #14 | Zilla Slab | Sans-serif grotesque | ❌ | **GRAVE** — Zilla Slab est une slab serif, catégorisée sans-serif |
| #15 | Gelasio | Serif didone | ❌ | Mineure — Gelasio est une serif transitionnelle (Georgia-like), pas didone |
| #16 | Domine | Sans-serif néo-grotesque | ❌ | **GRAVE** — Domine est une serif transitionnelle, catégorisée sans-serif |
| #17 | Encode Sans | Serif old-style | ❌ | **GRAVE** — Encode Sans est une sans-serif, catégorisée serif |
| #18 | Cabin | Sans-serif géométrique | ❌ | Mineure — Cabin est plutôt humaniste que géométrique, mais reste sans-serif |
| #19 | Barlow | Serif didone | ❌ | **GRAVE** — Barlow est une sans-serif grotesque, catégorisée serif |
| #20 | Vollkorn | Sans-serif grotesque | ❌ | **GRAVE** — Vollkorn est une serif, catégorisée sans-serif |
| #21 | Cardo | Serif transitionnel | ✅ | Correct (old-style/transitionnel acceptable) |
| #22 | Bitter | Sans-serif humaniste | ❌ | **GRAVE** — Bitter est une slab serif, catégorisée sans-serif |
| #23 | Spectral | Slab serif | ❌ | **GRAVE** — Spectral est une serif transitionnelle, catégorisée slab serif (confusion serif→slab) — erreur modérée plutôt que grave car reste serif |
| #24 | Alegreya | Serif didone | ❌ | Mineure — Alegreya est old-style/humaniste, pas didone |
| #25 | Noto Sans Display | Sans-serif grotesque | ✅ | Correct (néo-grotesque/grotesque acceptable) |
| #26 | Ubuntu | Serif transitionnel | ❌ | **GRAVE** — Ubuntu est une sans-serif humaniste, catégorisée serif |
| #27 | Arimo | Serif didone | ❌ | **GRAVE** — Arimo est une sans-serif néo-grotesque (Arial-like), catégorisée serif |
| #28 | Chivo | Sans-serif géométrique | ❌ | Mineure — Chivo est plutôt grotesque que géométrique, mais reste sans-serif |
| #29 | Libre Franklin | Serif old-style | ❌ | **GRAVE** — Libre Franklin est une sans-serif (Franklin Gothic-like), catégorisée serif |
| #30 | Roboto Serif | Sans-serif néo-grotesque | ❌ | **GRAVE** — Roboto Serif est une serif, catégorisée sans-serif |
| #31 | IBM Plex Serif | Serif transitionnel | ✅ | Correct |
| #32 | Roboto Slab | Sans-serif grotesque | ❌ | **GRAVE** — Roboto Slab est une slab serif, catégorisée sans-serif |
| #33 | Quicksand | Serif didone | ❌ | **GRAVE** — Quicksand est une sans-serif géométrique arrondie, catégorisée serif |
| #34 | Comfortaa | Sans-serif humaniste | ❌ | Mineure — Comfortaa est plutôt géométrique/arrondie que humaniste, mais reste sans-serif |
| #35 | Josefin Sans | Slab serif | ❌ | **GRAVE** — Josefin Sans est une sans-serif géométrique, catégorisée slab serif |
| #36 | Outfit | Serif transitionnel | ❌ | **GRAVE** — Outfit est une sans-serif géométrique, catégorisée serif |
| #37 | Nunito | Sans-serif grotesque | ❌ | Mineure — Nunito est plutôt géométrique arrondie que grotesque, mais reste sans-serif |
| #38 | Cormorant Garamond | Serif old-style | ✅ | Correct |
| #39 | EB Garamond | Sans-serif géométrique | ❌ | **GRAVE** — EB Garamond est une serif old-style, catégorisée sans-serif |
| #40 | PT Serif | Serif didone | ❌ | Mineure — PT Serif est transitionnelle, pas didone |
| #41 | Crimson Text | Sans-serif néo-grotesque | ❌ | **GRAVE** — Crimson Text est une serif old-style, catégorisée sans-serif |
| #42 | Noto Serif | Serif transitionnel | ✅ | Correct |
| #43 | Source Serif 4 | Sans-serif grotesque | ❌ | **GRAVE** — Source Serif 4 est une serif transitionnelle, catégorisée sans-serif |
| #44 | Libre Baskerville | Serif old-style | ❌ | Mineure — Libre Baskerville est transitionnelle (Baskerville), pas old-style, mais reste serif |
| #45 | Merriweather | Sans-serif humaniste | ❌ | **GRAVE** — Merriweather est une serif slab/transitionnelle, catégorisée sans-serif |
| #46 | Lora | Sans-serif géométrique | ❌ | **GRAVE** — Lora est une serif contemporaine/transitionnelle, catégorisée sans-serif |
| #47 | Raleway | Sans-serif grotesque | ❌ | Mineure — Raleway est plutôt géométrique/élégante que grotesque, mais reste sans-serif |
| #48 | Montserrat | Serif didone | ❌ | **GRAVE** — Montserrat est une sans-serif géométrique, catégorisée serif |
| #49 | Poppins | Serif didone | ❌ | **GRAVE** — Poppins est une sans-serif géométrique, catégorisée serif |
| #50 | Playfair Display | Serif old-style | ❌ | Mineure — Playfair Display est didone/high-contrast, pas old-style, mais reste serif |

**Score : 10/50** (seulement 10 catégorisations correctes ou avec erreur mineure acceptable)

Corrections : en comptant les mineures comme "acceptables" : ~18/50

**Erreurs GRAVES (serif/sans-serif confondues) — fonts a retirer :**
- #02 Labrada (serif → dit sans-serif)
- #05 Faustina (serif → dit sans-serif)
- #08 Frank Ruhl Libre (serif → dit sans-serif)
- #11 Petrona (serif → dit sans-serif)
- #12 Signika (sans-serif → dit slab serif)
- #14 Zilla Slab (slab serif → dit sans-serif)
- #16 Domine (serif → dit sans-serif)
- #17 Encode Sans (sans-serif → dit serif)
- #19 Barlow (sans-serif → dit serif)
- #20 Vollkorn (serif → dit sans-serif)
- #22 Bitter (slab serif → dit sans-serif)
- #26 Ubuntu (sans-serif → dit serif)
- #27 Arimo (sans-serif → dit serif)
- #29 Libre Franklin (sans-serif → dit serif)
- #30 Roboto Serif (serif → dit sans-serif)
- #32 Roboto Slab (slab serif → dit sans-serif)
- #33 Quicksand (sans-serif → dit serif)
- #35 Josefin Sans (sans-serif → dit slab serif)
- #36 Outfit (sans-serif → dit serif)
- #39 EB Garamond (serif → dit sans-serif)
- #41 Crimson Text (serif → dit sans-serif)
- #43 Source Serif 4 (serif → dit sans-serif)
- #45 Merriweather (serif → dit sans-serif)
- #46 Lora (serif → dit sans-serif)
- #48 Montserrat (sans-serif → dit serif)
- #49 Poppins (sans-serif → dit serif)

**26 fonts a retirer sur 50** — pool inutilisable.

---

## 2. Display A2

| # | Font réelle | LLM dit | Correct ? | Nature de l'erreur |
|---|---|---|---|---|
| #01 | Bricolage Grotesque | Sans-serif géométrique | ❌ | Mineure — Bricolage est grotesque, pas géométrique, mais reste sans-serif |
| #02 | Gabarito | Sans-serif grotesque | ❌ | **GRAVE** — Gabarito est une serif/slab-serif arrondie, catégorisée sans-serif |
| #03 | Calistoga | Sans-serif grotesque | ❌ | **GRAVE** — Calistoga est une serif display (empattements), catégorisée sans-serif |
| #04 | Manuale | Serif didone | ❌ | Mineure — Manuale est une serif transitionnelle, pas didone |
| #05 | Tenor Sans | Sans-serif humaniste | ✅ | Correct |
| #06 | Epilogue | Sans-serif grotesque | ❌ | Mineure — Epilogue est plutôt néo-grotesque/géométrique, mais reste sans-serif |
| #07 | Brygada 1918 | Sans-serif géométrique | ❌ | **GRAVE** — Brygada 1918 est une serif, catégorisée sans-serif |
| #08 | Labrada | Sans-serif grotesque | ❌ | **GRAVE** — Labrada est une serif, catégorisée sans-serif |
| #09 | Sansita | Serif mécane (slab) | ❌ | **GRAVE** — Sansita est une sans-serif arrondie (le nom dit "Sans"), catégorisée serif |
| #10 | Prata | Serif transitionnelle | ❌ | Mineure — Prata est didone, pas transitionnelle, mais reste serif |
| #11 | Anybody | Sans-serif grotesque | ✅ | Correct (variable width grotesque) |
| #12 | Commissioner | Serif didone | ❌ | **GRAVE** — Commissioner est une sans-serif humaniste, catégorisée serif |
| #13 | Geologica | Sans-serif néo-grotesque | ✅ | Correct |
| #14 | Onest | Sans-serif grotesque | ❌ | Mineure — Onest est plutôt géométrique/arrondie, mais reste sans-serif |
| #15 | Ancizar Serif | Sans-serif géométrique | ❌ | **GRAVE** — Ancizar Serif est une serif (le nom le dit), catégorisée sans-serif |
| #16 | Wix Madefor Display | Serif humaniste | ❌ | **GRAVE** — Wix Madefor Display est une sans-serif, catégorisée serif |
| #17 | Gloock | Sans-serif grotesque | ❌ | **GRAVE** — Gloock est une serif didone display, catégorisée sans-serif |
| #18 | Jost | Sans-serif néo-grotesque | ❌ | Mineure — Jost est plutôt géométrique (Futura-like), mais reste sans-serif |
| #19 | Crimson Pro | Serif didone | ❌ | Mineure — Crimson Pro est old-style/transitionnelle, pas didone |
| #20 | Frank Ruhl Libre | Serif transitionnelle | ❌ | Mineure — Frank Ruhl Libre est didone, pas transitionnelle |
| #21 | Cormorant | Sans-serif grotesque | ❌ | **GRAVE** — Cormorant est une serif Garamond-like, catégorisée sans-serif |
| #22 | Zalando Sans | Sans-serif humaniste | ✅ | Correct |
| #23 | Noto Serif Display | Sans-serif grotesque | ❌ | **GRAVE** — Noto Serif Display est une serif (le nom le dit), catégorisée sans-serif |
| #24 | Roboto Serif | Sans-serif grotesque | ❌ | **GRAVE** — Roboto Serif est une serif (le nom le dit), catégorisée sans-serif |
| #25 | Libre Caslon Display | Sans-serif néo-grotesque | ❌ | **GRAVE** — Libre Caslon Display est une serif (Caslon), catégorisée sans-serif |
| #26 | Red Hat Display | Sans-serif grotesque | ❌ | Mineure — Red Hat Display est plutôt géométrique/humaniste, mais reste sans-serif |
| #27 | Albert Sans | Sans-serif grotesque | ❌ | Mineure — Albert Sans est plutôt géométrique, mais reste sans-serif |
| #28 | Figtree | Sans-serif géométrique | ✅ | Correct (géométrique arrondie) |
| #29 | Urbanist | Sans-serif humaniste | ❌ | Mineure — Urbanist est plutôt géométrique, mais reste sans-serif |
| #30 | Instrument Sans | Sans-serif grotesque | ❌ | Mineure — Instrument Sans est plutôt néo-grotesque, mais reste sans-serif |
| #31 | Lexend | Sans-serif géométrique | ❌ | Mineure — Lexend est plutôt humaniste (conçue pour la lisibilité), mais reste sans-serif |
| #32 | Josefin Sans | Sans-serif néo-grotesque | ❌ | Mineure — Josefin Sans est géométrique (inspirée Futura), mais reste sans-serif |
| #33 | Sora | Sans-serif grotesque | ❌ | Mineure — Sora est plutôt géométrique, mais reste sans-serif |
| #34 | Overpass | Sans-serif humaniste | ❌ | Mineure — Overpass est plutôt grotesque (Highway Gothic-like), mais reste sans-serif |
| #35 | Libre Franklin | Sans-serif grotesque | ✅ | Correct |
| #36 | Archivo | Serif didone | ❌ | **GRAVE** — Archivo est une sans-serif grotesque, catégorisée serif |
| #37 | Literata | Sans-serif géométrique | ❌ | **GRAVE** — Literata est une serif contemporaine, catégorisée sans-serif |
| #38 | Hanken Grotesk | Sans-serif grotesque | ✅ | Correct |
| #39 | Be Vietnam Pro | Sans-serif grotesque | ❌ | Mineure — Be Vietnam Pro est plutôt géométrique/humaniste, mais reste sans-serif |
| #40 | Schibsted Grotesk | Sans-serif néo-grotesque | ✅ | Correct (grotesque/néo-grotesque) |
| #41 | Outfit | Sans-serif grotesque | ❌ | Mineure — Outfit est plutôt géométrique, mais reste sans-serif |
| #42 | Maven Pro | Sans-serif grotesque | ❌ | Mineure — Maven Pro est plutôt géométrique, mais reste sans-serif |
| #43 | IBM Plex Serif | Serif transitionnelle | ✅ | Correct |
| #44 | Newsreader | Sans-serif grotesque | ❌ | **GRAVE** — Newsreader est une serif transitionnelle, catégorisée sans-serif |
| #45 | Poppins | Sans-serif grotesque | ❌ | Mineure — Poppins est géométrique, pas grotesque, mais reste sans-serif |
| #46 | DM Serif Display | Serif didone | ❌ | Mineure — DM Serif Display est transitionnelle, pas didone, mais reste serif |
| #47 | Playfair Display | Serif transitionnelle | ❌ | Mineure — Playfair Display est didone, pas transitionnelle, mais reste serif |
| #48 | Young Serif | Sans-serif grotesque | ❌ | **GRAVE** — Young Serif est une serif (le nom le dit), catégorisée sans-serif |
| #49 | Fraunces | Serif didone | ❌ | Mineure — Fraunces est old-style variable, pas didone, mais reste serif |
| #50 | Space Grotesk | Sans-serif grotesque | ✅ | Correct |

**Score : 10/50**

Corrections avec mineures acceptables : ~24/50

**Erreurs GRAVES — fonts a retirer :**
- #02 Gabarito (serif → dit sans-serif)
- #03 Calistoga (serif → dit sans-serif)
- #07 Brygada 1918 (serif → dit sans-serif)
- #08 Labrada (serif → dit sans-serif)
- #09 Sansita (sans-serif → dit serif)
- #12 Commissioner (sans-serif → dit serif)
- #15 Ancizar Serif (serif → dit sans-serif)
- #16 Wix Madefor Display (sans-serif → dit serif)
- #17 Gloock (serif → dit sans-serif)
- #21 Cormorant (serif → dit sans-serif)
- #23 Noto Serif Display (serif → dit sans-serif)
- #24 Roboto Serif (serif → dit sans-serif)
- #25 Libre Caslon Display (serif → dit sans-serif)
- #36 Archivo (sans-serif → dit serif)
- #37 Literata (serif → dit sans-serif)
- #44 Newsreader (serif → dit sans-serif)
- #48 Young Serif (serif → dit sans-serif)

**17 fonts a retirer sur 50.**

---

## 3. Display A3

| # | Font réelle | LLM dit | Correct ? | Nature de l'erreur |
|---|---|---|---|---|
| #01 | Bodoni Moda | Serif display didone | ✅ | Correct |
| #02 | Abril Fatface | Serif display slab bold | ❌ | Mineure — Abril Fatface est didone/fatface, pas slab. Reste serif display |
| #03 | Cormorant Garamond | Serif display transitionnelle | ❌ | Mineure — Cormorant Garamond est old-style, pas transitionnelle. Reste serif |
| #04 | DM Serif Display | Sans-serif display grotesque | ❌ | **GRAVE** — DM Serif Display est une serif (le nom le dit), catégorisée sans-serif |
| #05 | Gloock | Serif display didone | ✅ | Correct |
| #06 | Eczar | Slab serif display | ❌ | Mineure — Eczar est plutôt une serif humaniste épaisse, pas slab. Reste serif |
| #07 | Young Serif | Serif display didone | ❌ | Mineure — Young Serif est transitionnelle, pas didone. Reste serif |
| #08 | Fraunces | Sans-serif display géométrique | ❌ | **GRAVE** — Fraunces est une serif old-style variable, catégorisée sans-serif |
| #09 | Kalnia Glaze | Serif display décorative | ✅ | Correct (display décorative avec effets) |
| #10 | Instrument Serif | Sans-serif display grotesque | ❌ | **GRAVE** — Instrument Serif est une serif (le nom le dit), catégorisée sans-serif |
| #11 | Calistoga | Sans-serif display condensée | ❌ | **GRAVE** — Calistoga est une serif display, catégorisée sans-serif |
| #12 | Darker Grotesque | Serif display slab | ❌ | **GRAVE** — Darker Grotesque est une sans-serif (le nom dit Grotesque), catégorisée serif |
| #13 | Bebas Neue | Sans-serif display condensée | ✅ | Correct |
| #14 | Big Shoulders Inline | Sans-serif display géométrique | ❌ | Mineure — Big Shoulders Inline est plutôt condensée display, pas géométrique. Reste sans-serif |
| #15 | Funnel Display | Sans-serif display grotesque | ✅ | Correct |
| #16 | Genos | Sans-serif display ronde | ❌ | Mineure — Genos est plutôt géométrique/futuriste que ronde. Reste sans-serif |
| #17 | Tourney | Sans-serif display slab inline | ❌ | Mineure — Tourney est variable display, la description "slab inline" n'est pas tout a fait juste. Mais c'est display |
| #18 | Bungee | Sans-serif display grotesque | ✅ | Correct |
| #19 | Familjen Grotesk | Sans-serif display géométrique humaniste | ❌ | Mineure — Familjen Grotesk est grotesque (le nom le dit), pas géométrique |
| #20 | Schibsted Grotesk | Sans-serif display grotesque | ✅ | Correct |
| #21 | Chivo | Sans-serif display géométrique | ❌ | Mineure — Chivo est grotesque, pas géométrique. Reste sans-serif |
| #22 | Rethink Sans | Sans-serif display géométrique medium | ❌ | Mineure — Rethink Sans est humaniste, pas géométrique. Reste sans-serif |
| #23 | Bricolage Grotesque | Slab serif display arrondie | ❌ | **GRAVE** — Bricolage Grotesque est une sans-serif (le nom le dit), catégorisée slab serif |
| #24 | Special Gothic Expanded One | Sans-serif grotesque italique | ✅ | Correct |
| #25 | Gabarito | Sans-serif display humaniste | ❌ | **GRAVE** — Gabarito a des empattements (serif/slab-like), catégorisée sans-serif |
| #26 | Righteous | Sans-serif display géométrique light | ❌ | Mineure — Righteous est plutôt display arrondie, pas géométrique light. Reste sans-serif |
| #27 | Syne | Sans-serif display géométrique | ❌ | Mineure — Syne est plutôt grotesque expressive, pas géométrique. Reste sans-serif |
| #28 | Unbounded | Sans-serif display humaniste | ❌ | Mineure — Unbounded est plutôt géométrique/arrondie display. Reste sans-serif |
| #29 | Audiowide | Sans-serif display géométrique futuriste | ✅ | Correct |
| #30 | Tektur | Sans-serif display géométrique square | ✅ | Correct |
| #31 | Rubik Mono One | Display décorative | ❌ | Mineure — Rubik Mono One est plutôt sans-serif ultra-bold display que "décorative". Acceptable |
| #32 | Tilt Neon | Sans-serif display transitionnelle | ❌ | Mineure — Tilt Neon est plutôt variable display arrondie, pas "transitionnelle". Reste sans-serif display |
| #33 | Tilt Prism | Display décorative outline | ✅ | Correct (3D/prismatique = décorative) |
| #34 | Foldit | Script display | ❌ | Modérée — Foldit est une display décorative géométrique pliable, pas script |
| #35 | Nabla | Display décorative 3D | ✅ | Correct |
| #36 | Rampart One | Display décorative | ✅ | Correct |
| #37 | Rubik Glitch | Display décorative | ✅ | Correct |
| #38 | Rubik Spray Paint | Display décorative | ✅ | Correct |
| #39 | Rubik Wet Paint | Display décorative | ✅ | Correct |
| #40 | Honk | Display décorative chromée | ✅ | Correct |
| #41 | Moirai One | Script display cursive | ❌ | Modérée — Moirai One est une display décorative (motifs en vagues), pas vraiment script cursive |
| #42 | Monoton | Display décorative slab | ❌ | Mineure — Monoton est plutôt display outline/inline, pas slab unicase. Reste décorative |
| #43 | Bagel Fat One | Sans-serif display semi-bold | ❌ | Mineure — Bagel Fat One est plutôt display arrondie/blob, pas "semi-bold clean". Mais sans-serif |
| #44 | Cairo Play | Display variable bicolore | ✅ | Correct (Cairo Play est une variable color font) |
| #45 | Climate Crisis | Display décorative | ✅ | Correct |
| #46 | Sixtyfour | Pixel display | ✅ | Correct |
| #47 | Pixelify Sans | Pixel display | ✅ | Correct |
| #48 | Handjet | Pixel display | ✅ | Correct |
| #49 | Silkscreen | Pixel display bold | ✅ | Correct |
| #50 | Press Start 2P | Pixel display serif bitmap | ✅ | Correct |

**Score : 27/50**

Avec mineures acceptables : ~38/50

**Erreurs GRAVES — fonts a retirer :**
- #04 DM Serif Display (serif → dit sans-serif)
- #08 Fraunces (serif → dit sans-serif)
- #10 Instrument Serif (serif → dit sans-serif)
- #11 Calistoga (serif → dit sans-serif)
- #12 Darker Grotesque (sans-serif → dit serif)
- #23 Bricolage Grotesque (sans-serif → dit slab serif)
- #25 Gabarito (serif-like → dit sans-serif)

**7 fonts a retirer sur 50.**

---

## 4. Body A1

| # | Font réelle | LLM dit | Correct ? | Nature de l'erreur |
|---|---|---|---|---|
| #01 | Geist | Sans-serif grotesque | ❌ | Mineure — Geist est plutôt néo-grotesque/géométrique. Reste sans-serif |
| #02 | Schibsted Grotesk | Sans-serif grotesque | ✅ | Correct |
| #03 | Catamaran | Sans-serif humaniste | ✅ | Correct |
| #04 | Sarabun | Sans-serif néo-grotesque | ❌ | Mineure — Sarabun est plutôt humaniste (Thai-Latin), mais reste sans-serif |
| #05 | Cantarell | Sans-serif grotesque | ❌ | Mineure — Cantarell est plutôt humaniste (GNOME). Reste sans-serif |
| #06 | Maven Pro | Sans-serif géométrique | ❌ | Mineure — Maven Pro est plutôt géométrique arrondie, acceptable |
| #07 | Hanken Grotesk | Sans-serif humaniste | ❌ | Mineure — Hanken Grotesk est grotesque (le nom le dit). Reste sans-serif |
| #08 | Encode Sans | Sans-serif néo-grotesque | ✅ | Correct |
| #09 | Overpass | Sans-serif grotesque | ✅ | Correct |
| #10 | Hind | Sans-serif néo-grotesque | ❌ | Mineure — Hind est plutôt humaniste. Reste sans-serif |
| #11 | Archivo | Sans-serif humaniste | ❌ | Mineure — Archivo est grotesque. Reste sans-serif |
| #12 | Wix Madefor Text | Sans-serif grotesque | ❌ | Mineure — Wix Madefor Text est humaniste. Reste sans-serif |
| #13 | Atkinson Hyperlegible | Sans-serif néo-grotesque | ❌ | Mineure — Atkinson est humaniste (conçue pour hyperlégiblité). Reste sans-serif |
| #14 | Red Hat Text | Sans-serif géométrique | ❌ | Mineure — Red Hat Text est plutôt humaniste. Reste sans-serif |
| #15 | Instrument Sans | Sans-serif humaniste | ❌ | Mineure — Instrument Sans est plutôt néo-grotesque. Reste sans-serif |
| #16 | Lexend | Sans-serif néo-grotesque | ❌ | Mineure — Lexend est plutôt humaniste. Reste sans-serif |
| #17 | Be Vietnam Pro | Sans-serif grotesque | ❌ | Mineure — Be Vietnam Pro est plutôt géométrique. Reste sans-serif |
| #18 | Albert Sans | Sans-serif humaniste | ❌ | Mineure — Albert Sans est plutôt géométrique. Reste sans-serif |
| #19 | Figtree | Sans-serif géométrique | ✅ | Correct |
| #20 | Urbanist | Sans-serif humaniste | ❌ | Mineure — Urbanist est plutôt géométrique. Reste sans-serif |
| #21 | Outfit | Sans-serif néo-grotesque | ❌ | Mineure — Outfit est plutôt géométrique. Reste sans-serif |
| #22 | Karla | Sans-serif grotesque | ❌ | Mineure — Karla est plutôt grotesque, acceptable |
| #23 | Rubik | Sans-serif humaniste | ❌ | Mineure — Rubik est plutôt géométrique arrondie. Reste sans-serif |
| #24 | Plus Jakarta Sans | Sans-serif néo-grotesque | ❌ | Mineure — Plus Jakarta Sans est plutôt géométrique. Reste sans-serif |
| #25 | Manrope | Sans-serif grotesque | ❌ | Mineure — Manrope est plutôt géométrique. Reste sans-serif |
| #26 | Public Sans | Sans-serif humaniste | ❌ | Mineure — Public Sans est plutôt néo-grotesque. Reste sans-serif |
| #27 | Nunito Sans | Sans-serif néo-grotesque | ❌ | Mineure — Nunito Sans est plutôt géométrique arrondie. Reste sans-serif |
| #28 | Work Sans | Serif transitionnel | ❌ | **GRAVE** — Work Sans est une sans-serif grotesque, catégorisée serif |
| #29 | Mulish | Sans-serif grotesque | ❌ | Mineure — Mulish est plutôt géométrique. Reste sans-serif |
| #30 | Noto Sans | Sans-serif néo-grotesque | ✅ | Correct |
| #31 | Fira Sans | Sans-serif humaniste | ✅ | Correct |
| #32 | Ubuntu | Sans-serif grotesque | ❌ | Mineure — Ubuntu est plutôt humaniste. Reste sans-serif |
| #33 | Lato | Sans-serif néo-grotesque | ❌ | Mineure — Lato est plutôt humaniste/géométrique hybride. Reste sans-serif |
| #34 | Roboto | Sans-serif humaniste | ❌ | Mineure — Roboto est plutôt néo-grotesque/géométrique. Reste sans-serif |
| #35 | Open Sans | Sans-serif grotesque | ❌ | Mineure — Open Sans est plutôt humaniste. Reste sans-serif |
| #36 | Literata | Sans-serif néo-grotesque | ❌ | **GRAVE** — Literata est une serif contemporaine, catégorisée sans-serif |
| #37 | Newsreader | Serif contemporain | ✅ | Correct (serif, description "contemporain" acceptable pour "transitionnelle") |
| #38 | Roboto Serif | Sans-serif humaniste | ❌ | **GRAVE** — Roboto Serif est une serif (le nom le dit), catégorisée sans-serif |
| #39 | Crimson Text | Sans-serif grotesque | ❌ | **GRAVE** — Crimson Text est une serif old-style, catégorisée sans-serif |
| #40 | Noto Serif | Serif didone | ❌ | Mineure — Noto Serif est transitionnelle, pas didone. Reste serif |
| #41 | Merriweather | Sans-serif néo-grotesque | ❌ | **GRAVE** — Merriweather est une serif, catégorisée sans-serif |
| #42 | Lora | Sans-serif grotesque | ❌ | **GRAVE** — Lora est une serif, catégorisée sans-serif |
| #43 | Source Serif 4 | Sans-serif humaniste | ❌ | **GRAVE** — Source Serif 4 est une serif (le nom le dit), catégorisée sans-serif |
| #44 | PT Sans | Sans-serif néo-grotesque | ✅ | Correct (humaniste/néo-grotesque acceptable) |
| #45 | Libre Franklin | Sans-serif grotesque | ✅ | Correct |
| #46 | Chivo | Sans-serif humaniste | ❌ | Mineure — Chivo est grotesque. Reste sans-serif |
| #47 | IBM Plex Sans | Sans-serif néo-grotesque | ✅ | Correct |
| #48 | DM Sans | Sans-serif grotesque | ❌ | Mineure — DM Sans est plutôt géométrique. Reste sans-serif |
| #49 | Source Sans 3 | Sans-serif humaniste | ❌ | Mineure — Source Sans 3 est plutôt humaniste, acceptable |
| #50 | Inter | Sans-serif grotesque | ❌ | Mineure — Inter est plutôt néo-grotesque/humaniste. Reste sans-serif |

**Score : 11/50** (strictement correct)

Avec mineures acceptables : ~43/50

**Erreurs GRAVES — fonts a retirer :**
- #28 Work Sans (sans-serif → dit serif)
- #36 Literata (serif → dit sans-serif)
- #38 Roboto Serif (serif → dit sans-serif)
- #39 Crimson Text (serif → dit sans-serif)
- #41 Merriweather (serif → dit sans-serif)
- #42 Lora (serif → dit sans-serif)
- #43 Source Serif 4 (serif → dit sans-serif)

**7 fonts a retirer sur 50.**

---

## 5. Body A2

| # | Font réelle | LLM dit | Correct ? | Nature de l'erreur |
|---|---|---|---|---|
| #01 | Rethink Sans | Sans-serif humaniste | ✅ | Correct |
| #02 | Geist | Sans-serif grotesque | ❌ | Mineure — Geist est plutôt néo-grotesque. Reste sans-serif |
| #03 | Alegreya Sans | Sans-serif néo-grotesque | ❌ | Mineure — Alegreya Sans est humaniste. Reste sans-serif |
| #04 | Spectral | Sans-serif humaniste | ❌ | **GRAVE** — Spectral est une serif, catégorisée sans-serif |
| #05 | Crimson Pro | Sans-serif néo-grotesque | ❌ | **GRAVE** — Crimson Pro est une serif, catégorisée sans-serif |
| #06 | Encode Sans | Sans-serif grotesque | ❌ | Mineure — Encode Sans est néo-grotesque. Reste sans-serif |
| #07 | Commissioner | Sans-serif humaniste | ✅ | Correct (humaniste variable) |
| #08 | Onest | Sans-serif néo-grotesque | ❌ | Mineure — Onest est plutôt géométrique. Reste sans-serif |
| #09 | Epilogue | Sans-serif grotesque | ❌ | Mineure — Epilogue est plutôt néo-grotesque. Reste sans-serif |
| #10 | Instrument Sans | Sans-serif humaniste | ❌ | Mineure — Instrument Sans est plutôt néo-grotesque. Reste sans-serif |
| #11 | Barlow | Sans-serif géométrique | ❌ | Mineure — Barlow est grotesque. Reste sans-serif |
| #12 | Cabin | Sans-serif grotesque | ❌ | Mineure — Cabin est humaniste. Reste sans-serif |
| #13 | Noto Sans | Sans-serif humaniste | ❌ | Mineure — Noto Sans est néo-grotesque. Reste sans-serif |
| #14 | Urbanist | Sans-serif néo-grotesque | ❌ | Mineure — Urbanist est géométrique. Reste sans-serif |
| #15 | Outfit | Sans-serif grotesque | ❌ | Mineure — Outfit est géométrique. Reste sans-serif |
| #16 | Wix Madefor Text | Sans-serif humaniste | ✅ | Correct |
| #17 | Atkinson Hyperlegible | Sans-serif géométrique | ❌ | Mineure — Atkinson est humaniste. Reste sans-serif |
| #18 | Be Vietnam Pro | Sans-serif grotesque | ❌ | Mineure — Be Vietnam Pro est géométrique. Reste sans-serif |
| #19 | Lexend | Slab-serif humaniste | ❌ | **GRAVE** — Lexend est une sans-serif, catégorisée slab-serif |
| #20 | Figtree | Sans-serif néo-grotesque | ❌ | Mineure — Figtree est géométrique. Reste sans-serif |
| #21 | Albert Sans | Sans-serif grotesque | ❌ | Mineure — Albert Sans est géométrique. Reste sans-serif |
| #22 | Red Hat Text | Sans-serif humaniste | ✅ | Correct |
| #23 | Overpass | Sans-serif géométrique | ❌ | Mineure — Overpass est grotesque. Reste sans-serif |
| #24 | Hind | Sans-serif néo-grotesque | ❌ | Mineure — Hind est humaniste. Reste sans-serif |
| #25 | Mulish | Sans-serif humaniste | ❌ | Mineure — Mulish est géométrique. Reste sans-serif |
| #26 | Karla | Sans-serif grotesque | ✅ | Correct (grotesque acceptable) |
| #27 | Plus Jakarta Sans | Sans-serif néo-grotesque | ❌ | Mineure — Plus Jakarta Sans est géométrique. Reste sans-serif |
| #28 | Manrope | Sans-serif humaniste | ❌ | Mineure — Manrope est géométrique. Reste sans-serif |
| #29 | Public Sans | Sans-serif géométrique | ❌ | Mineure — Public Sans est néo-grotesque. Reste sans-serif |
| #30 | Nunito Sans | Sans-serif grotesque | ❌ | Mineure — Nunito Sans est géométrique arrondie. Reste sans-serif |
| #31 | Work Sans | Sans-serif humaniste | ❌ | Mineure — Work Sans est grotesque. Reste sans-serif |
| #32 | Lora | Sans-serif néo-grotesque | ❌ | **GRAVE** — Lora est une serif, catégorisée sans-serif |
| #33 | Source Serif 4 | Sans-serif grotesque | ❌ | **GRAVE** — Source Serif 4 est une serif (le nom le dit), catégorisée sans-serif |
| #34 | Literata | Sans-serif humaniste | ❌ | **GRAVE** — Literata est une serif, catégorisée sans-serif |
| #35 | Newsreader | Sans-serif géométrique | ❌ | **GRAVE** — Newsreader est une serif, catégorisée sans-serif |
| #36 | Noto Serif | Sans-serif grotesque | ❌ | **GRAVE** — Noto Serif est une serif (le nom le dit), catégorisée sans-serif |
| #37 | Schibsted Grotesk | Sans-serif humaniste | ❌ | Mineure — Schibsted Grotesk est grotesque. Reste sans-serif |
| #38 | Hanken Grotesk | Sans-serif néo-grotesque | ✅ | Correct (grotesque/néo-grotesque) |
| #39 | Ubuntu | Sans-serif grotesque | ❌ | Mineure — Ubuntu est humaniste. Reste sans-serif |
| #40 | PT Sans | Sans-serif humaniste | ✅ | Correct |
| #41 | Fira Sans | Sans-serif géométrique | ❌ | Mineure — Fira Sans est humaniste. Reste sans-serif |
| #42 | Libre Franklin | Sans-serif grotesque | ✅ | Correct |
| #43 | Roboto | Sans-serif humaniste | ❌ | Mineure — Roboto est néo-grotesque. Reste sans-serif |
| #44 | Lato | Sans-serif néo-grotesque | ❌ | Mineure — Lato est humaniste. Reste sans-serif |
| #45 | Chivo | Sans-serif grotesque | ✅ | Correct |
| #46 | Open Sans | Sans-serif humaniste | ✅ | Correct |
| #47 | IBM Plex Sans | Sans-serif néo-grotesque | ✅ | Correct |
| #48 | Source Sans 3 | Sans-serif grotesque | ❌ | Mineure — Source Sans 3 est humaniste. Reste sans-serif |
| #49 | DM Sans | Sans-serif humaniste | ❌ | Mineure — DM Sans est géométrique. Reste sans-serif |
| #50 | Inter | Sans-serif géométrique | ❌ | Mineure — Inter est néo-grotesque. Reste sans-serif |

**Score : 11/50** (strictement correct)

Avec mineures acceptables : ~42/50

**Erreurs GRAVES — fonts a retirer :**
- #04 Spectral (serif → dit sans-serif)
- #05 Crimson Pro (serif → dit sans-serif)
- #19 Lexend (sans-serif → dit slab-serif)
- #32 Lora (serif → dit sans-serif)
- #33 Source Serif 4 (serif → dit sans-serif)
- #34 Literata (serif → dit sans-serif)
- #35 Newsreader (serif → dit sans-serif)
- #36 Noto Serif (serif → dit sans-serif)

**8 fonts a retirer sur 50.**

---

## 6. Body A3

| # | Font réelle | LLM dit | Correct ? | Nature de l'erreur |
|---|---|---|---|---|
| #01 | Inclusive Sans | Sans-serif grotesque | ❌ | Mineure — Inclusive Sans est humaniste. Reste sans-serif |
| #02 | Rethink Sans | Sans-serif néo-grotesque | ❌ | Mineure — Rethink Sans est humaniste. Reste sans-serif |
| #03 | Atkinson Hyperlegible | Sans-serif grotesque | ❌ | Mineure — Atkinson est humaniste. Reste sans-serif |
| #04 | Be Vietnam Pro | Sans-serif humaniste | ❌ | Mineure — Be Vietnam Pro est géométrique. Reste sans-serif |
| #05 | Lexend | Sans-serif néo-grotesque | ❌ | Mineure — Lexend est humaniste. Reste sans-serif |
| #06 | Outfit | Sans-serif grotesque | ❌ | Mineure — Outfit est géométrique. Reste sans-serif |
| #07 | Encode Sans | Sans-serif humaniste | ❌ | Mineure — Encode Sans est néo-grotesque. Reste sans-serif |
| #08 | Sono | Sans-serif géométrique | ❌ | Mineure — Sono est plutôt arrondie/monospace-like. Reste sans-serif |
| #09 | Shantell Sans | Sans-serif arrondie | ❌ | Mineure — Shantell Sans est plutôt manuscrite/handwriting. Catégorie discutable mais pas grave |
| #10 | Familjen Grotesk | Sans-serif néo-grotesque | ✅ | Correct (grotesque/néo-grotesque) |
| #11 | Schibsted Grotesk | Sans-serif géométrique | ❌ | Mineure — Schibsted Grotesk est grotesque. Reste sans-serif |
| #12 | Reddit Sans | Sans-serif humaniste | ✅ | Correct |
| #13 | Funnel Sans | Sans-serif néo-grotesque | ✅ | Correct |
| #14 | Darker Grotesque | Sans-serif grotesque | ✅ | Correct |
| #15 | IBM Plex Sans | Sans-serif humaniste | ❌ | Mineure — IBM Plex Sans est néo-grotesque. Reste sans-serif |
| #16 | Source Sans 3 | Sans-serif grotesque | ❌ | Mineure — Source Sans 3 est humaniste. Reste sans-serif |
| #17 | Inter | Sans-serif néo-grotesque | ✅ | Correct |
| #18 | Space Grotesk | Sans-serif grotesque | ✅ | Correct |
| #19 | Geologica | Sans-serif géométrique | ❌ | Mineure — Geologica est néo-grotesque. Reste sans-serif |
| #20 | Recursive | Sans-serif grotesque | ❌ | Mineure — Recursive est variable mono/sans, plutôt humaniste. Reste sans-serif |
| #21 | Geist Mono | Sans-serif néo-grotesque | ❌ | **GRAVE** — Geist Mono est une monospace, catégorisée comme proportionnelle néo-grotesque |
| #22 | Martian Mono | Sans-serif humaniste | ❌ | **GRAVE** — Martian Mono est une monospace, catégorisée comme proportionnelle humaniste |
| #23 | Azeret Mono | Sans-serif grotesque | ❌ | **GRAVE** — Azeret Mono est une monospace, catégorisée comme proportionnelle grotesque |
| #24 | Red Hat Mono | Sans-serif néo-grotesque | ❌ | **GRAVE** — Red Hat Mono est une monospace, catégorisée comme proportionnelle |
| #25 | DM Mono | Sans-serif humaniste | ❌ | **GRAVE** — DM Mono est une monospace, catégorisée comme proportionnelle |
| #26 | Fragment Mono | Sans-serif grotesque | ❌ | **GRAVE** — Fragment Mono est une monospace, catégorisée comme proportionnelle |
| #27 | Victor Mono | Sans-serif néo-grotesque | ❌ | **GRAVE** — Victor Mono est une monospace, catégorisée comme proportionnelle |
| #28 | Kode Mono | Slab-serif géométrique | ❌ | Modérée — Kode Mono est une monospace. Le LLM a vu les empattements (slab) mais a raté le mono |
| #29 | Fira Code | Sans-serif humaniste | ❌ | **GRAVE** — Fira Code est une monospace avec ligatures, catégorisée proportionnelle |
| #30 | JetBrains Mono | Sans-serif grotesque | ❌ | **GRAVE** — JetBrains Mono est une monospace, catégorisée proportionnelle |
| #31 | Source Code Pro | Sans-serif humaniste | ❌ | **GRAVE** — Source Code Pro est une monospace, catégorisée proportionnelle |
| #32 | Roboto Mono | Sans-serif grotesque | ❌ | **GRAVE** — Roboto Mono est une monospace, catégorisée proportionnelle |
| #33 | IBM Plex Mono | Sans-serif néo-grotesque | ❌ | **GRAVE** — IBM Plex Mono est une monospace, catégorisée proportionnelle |
| #34 | Inconsolata | Sans-serif humaniste | ❌ | **GRAVE** — Inconsolata est une monospace, catégorisée proportionnelle |
| #35 | Ubuntu Mono | Sans-serif grotesque | ❌ | **GRAVE** — Ubuntu Mono est une monospace, catégorisée proportionnelle |
| #36 | Noto Sans Mono | Sans-serif géométrique | ❌ | **GRAVE** — Noto Sans Mono est une monospace, catégorisée proportionnelle |
| #37 | Syne Mono | Slab-serif humaniste | ❌ | **GRAVE** — Syne Mono est une monospace, catégorisée proportionnelle slab-serif |
| #38 | B612 Mono | Sans-serif grotesque | ❌ | **GRAVE** — B612 Mono est une monospace, catégorisée proportionnelle |
| #39 | Atkinson Hyperlegible Mono | Sans-serif humaniste | ❌ | **GRAVE** — monospace catégorisée proportionnelle |
| #40 | Chivo Mono | Sans-serif grotesque | ❌ | **GRAVE** — Chivo Mono est une monospace, catégorisée proportionnelle |
| #41 | Reddit Mono | Sans-serif humaniste | ❌ | **GRAVE** — Reddit Mono est une monospace, catégorisée proportionnelle |
| #42 | Space Mono | Sans-serif grotesque | ❌ | **GRAVE** — Space Mono est une monospace, catégorisée proportionnelle |
| #43 | Anonymous Pro | Sans-serif néo-grotesque | ❌ | **GRAVE** — Anonymous Pro est une monospace, catégorisée proportionnelle |
| #44 | Spline Sans Mono | Sans-serif grotesque | ❌ | **GRAVE** — monospace catégorisée proportionnelle |
| #45 | Share Tech Mono | Sans-serif humaniste | ❌ | **GRAVE** — monospace catégorisée proportionnelle |
| #46 | Xanh Mono | Slab-serif géométrique | ❌ | **GRAVE** — Xanh Mono est une monospace serif, catégorisée slab-serif proportionnelle |
| #47 | Nova Mono | Slab-serif grotesque | ❌ | **GRAVE** — Nova Mono est une monospace, catégorisée proportionnelle |
| #48 | Cutive Mono | Serif transitionnel | ❌ | **GRAVE** — Cutive Mono est une monospace slab serif, catégorisée comme serif transitionnel proportionnel |
| #49 | Overpass Mono | Slab-serif monospace | ❌ | Modérée — Overpass Mono est une sans-serif monospace, pas slab-serif. Mais le LLM a au moins identifié le monospace |
| #50 | Courier Prime | Slab-serif monospace | ✅ | Correct (slab serif monospace) |

**Score : 7/50** (strictement correct)

Avec mineures acceptables : ~20/50

**Erreurs GRAVES — fonts a retirer (mono catégorisées proportionnelles) :**
- #21 Geist Mono
- #22 Martian Mono
- #23 Azeret Mono
- #24 Red Hat Mono
- #25 DM Mono
- #26 Fragment Mono
- #27 Victor Mono
- #29 Fira Code
- #30 JetBrains Mono
- #31 Source Code Pro
- #32 Roboto Mono
- #33 IBM Plex Mono
- #34 Inconsolata
- #35 Ubuntu Mono
- #36 Noto Sans Mono
- #37 Syne Mono
- #38 B612 Mono
- #39 Atkinson Hyperlegible Mono
- #40 Chivo Mono
- #41 Reddit Mono
- #42 Space Mono
- #43 Anonymous Pro
- #44 Spline Sans Mono
- #45 Share Tech Mono
- #46 Xanh Mono
- #47 Nova Mono
- #48 Cutive Mono

**27 fonts a retirer sur 50** — pool inutilisable (toutes les monospaces ont été catégorisées comme proportionnelles).

---

## Synthese globale

| Pool | Score strict | Score (mineures OK) | Fonts a retirer | Verdict |
|---|---|---|---|---|
| **Display A1** | 10/50 | 18/50 | 26 | INUTILISABLE — le LLM ne sait pas du tout quelles fonts sont serif vs sans-serif dans ce pool |
| **Display A2** | 10/50 | 24/50 | 17 | INUTILISABLE — meme probleme serif/sans-serif |
| **Display A3** | 27/50 | 38/50 | 7 | UTILISABLE avec retrait — le bas du pool (decoratives, pixels) est bien catégorisé, le haut (serifs classiques) pose probleme |
| **Body A1** | 11/50 | 43/50 | 7 | UTILISABLE avec retrait — les sous-catégories sont fausses mais serif/sans-serif est globalement correct sauf 7 fonts |
| **Body A2** | 11/50 | 42/50 | 8 | UTILISABLE avec retrait — meme profil que Body A1 |
| **Body A3** | 7/50 | 20/50 | 27 | INUTILISABLE — le LLM n'a identifié AUCUNE des 30 monospaces du pool |

### Diagnostic principal

1. **Le LLM ne voit pas les fonts.** Il travaille a l'aveugle sur des numeros. Sans pouvoir inspecter les glyphes, il produit des catégorisations aléatoires pour la distinction serif/sans-serif.

2. **Les sous-catégories (grotesque vs humaniste vs géométrique) sont quasi-aléatoires** dans tous les pools. Le LLM semble distribuer les sous-catégories pour avoir une variété, pas parce qu'il identifie réellement des caractéristiques.

3. **Les monospaces sont systématiquement invisibles.** Body A3 contient 30 monospaces et le LLM n'en a identifié que 2 (#49, #50). C'est la preuve définitive que le LLM invente les catégorisations.

4. **Les pools Display A1 et A2 sont les plus contaminés** car ils melangent serif et sans-serif de facon équilibrée, maximisant les chances d'erreur grave.

### Recommandation

La catégorisation par un LLM aveugle (sans accès aux specimens visuels) est **fondamentalement non fiable** pour la distinction serif/sans-serif et mono/proportionnel. Ces catégorisations ne peuvent pas servir de base pour un choix typographique pertinent.

Options :
- **A** : Remplacer la catégorisation LLM par une table de vérité humaine (mapping font → catégorie + description)
- **B** : Fournir les noms réels des fonts au LLM (il connait les fonts Google Fonts par leur nom et pourrait les catégoriser correctement)
- **C** : Utiliser les metadata Google Fonts API (category, variant) comme source de vérité
