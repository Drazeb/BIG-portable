# Guide — Workflow itératif MidJourney + NB2 vers le niveau élite

> **Registres cibles** : Dark mode cinéma, macro éditorial, still life chiaroscuro
> **Session de référence** : VoltaPilot "Le Pouls Profond" — 2026-04-30
> **Guides techniques complémentaires** : `midjourney-prompting-guide.md` (params MJ) · `nano-banana-prompting-guide.md` (params NB2)
> **Niveau atteint** : Awards / 9-10 via 3 passes

---

## §0 — Philosophie : la logique des 3 passes

L'erreur commune est de chercher l'image parfaite en une génération. Le bon modèle mental :

| Passe | Outil | Rôle | Ce qu'on ne touche PAS encore |
|-------|-------|------|-------------------------------|
| **Passe 1** | MidJourney (×4) | Trouver la bonne direction : composition + ambiance + lumière | Tout — on évalue, on ne corrige pas encore |
| **Passe 2** | MJ Vary Subtle (×4) | Affiner dans la direction validée | La direction — on raffine, on ne change pas |
| **Passe 3** | NB2 (sessions séquentielles) | Corrections chirurgicales : couleur fond, grain, tons cuivrés | La composition, la lumière, le cadrage |

**Règle d'or** : chaque outil fait ce qu'il fait bien. Ne jamais demander à NB2 de corriger la lumière — c'est MJ qui la génère. Ne jamais recadrer dans NB2 — c'est MJ Editor/Zoom Out.

---

## §1 — Sélection et usage des images de référence

### Les deux slots MidJourney

| Slot | Paramètre | Ce qu'il transfère | Ce qu'il ne transfère PAS |
|------|-----------|-------------------|--------------------------|
| **Image Prompt** | (image uploadée en slot 1, pas de paramètre) + `--iw N` | Composition + sujet + style global | Rien — tout passe en bloc |
| **Style Reference** | `--sref [URL]` + `--sw N` | Palette · grain · mood · traitement | **Direction lumière** · composition · sujet |

**`--sw` recommandé** : 60-80. En dessous de 50, l'effet est trop faible. Au-dessus de 90, la palette du prompt se perd.

### Approche A — Style Reference seul (une image)

```
[prompt text complet] --sref [URL cosmos image] --sw 70 --style raw --ar 3:4
```

- L'image de référence transfère : ambiance froide/chaude, grain, palette générale
- La composition est entièrement décrite dans le prompt texte
- **C'est l'approche qui a produit le meilleur résultat dans cette session**
- Avantage : contrôle total sur la composition via le prompt

**Quand utiliser** : quand on a une image de référence qui a le bon "traitement" (grain, palette, mood) mais qu'on veut une composition différente.

### Approche B — Deux images (composition + style)

```
[image composition en Image Prompt slot] [prompt text] --iw 1.5 --sref [URL style] --sw 60 --style raw --ar 3:4
```

- L'Image Prompt transfère la composition et la structure de la scène
- Le Style Reference transfère le traitement visuel
- **Attention** : `--iw` est ignoré silencieusement si l'Image Prompt slot est vide (REX §6)
- Avantage : si on a une image de composition parfaite qu'on ne peut pas décrire en texte

**Quand utiliser** : quand on a deux images complémentaires — l'une pour la structure, l'autre pour le traitement — et qu'on veut fusionner les deux.

### Approche C — Prompt from scratch (sans référence)

```
[prompt text complet] --style raw --ar 3:4 --s 250
```

- Aucune image de référence — tout est dans le texte
- Plus de liberté, moins de précision sur le traitement
- À utiliser quand on n'a pas d'image de référence pertinente

### Sélection d'une image cosmos comme Style Reference

Critères de sélection en ordre de priorité :
1. **Palette** — les tons froids/chauds correspondent au brief
2. **Traitement** — grain, contraste, qualité de lumière proche de l'intention
3. **Mood** — le registre émotionnel correspond (cinématique ≠ éditorial ≠ studio)
4. **Ratio et composition** — secondaire si on use l'image en style reference seulement

**Important** : `--sref` n'importe PAS la direction lumière de l'image de référence. La lumière doit être décrite dans le prompt texte.

---

## §2 — Génération MidJourney : paramètres et structure du prompt

### Paramètres non-négociables pour le dark mode cinéma

| Paramètre | Valeur | Pourquoi |
|-----------|--------|----------|
| `--style raw` | toujours | Supprime le filtre esthétique MJ. Sans ça : éclairage dramatisé, profondeur artificielle |
| `--ar` | 3:4 ou 4:5 | Portrait éditorial — BIG utilise le 3:4 |
| `--sw` | 60-80 | Si style reference utilisée |
| `--s` | 200-350 | Stylize modéré — assez pour la finesse, pas assez pour perdre le sujet |
| `--no` | Voir ci-dessous | Critique pour éviter les dérives |

### Structure du prompt (registre P2 macro + P4 still life)

```
[type de photographie] of [sujet + état précis], [angle caméra + position],
[description composition : axe, profondeur, bokeh],
[source lumière unique : direction + nature RÉFLÉCHIE],
[highlights métalliques si relevant],
[fond + couleur hex],
[contraste + couverture ombre %],
[focus + profondeur de champ],
[grain film],
[mood éditorial] --sw N --style raw --ar 3:4 --no [négatifs]
```

**Règle de poids** : les premiers mots pèsent le plus. Mettre le sujet en premier, les descripteurs techniques en dernier.

### Lumière — vocabulaire critique

La distinction lumière réfléchie / lumière émissive est la plus importante du registre macro cuivre sur fond sombre.

| Ce qu'on veut | Ce qu'on écrit | Ce qu'on évite |
|---------------|----------------|----------------|
| Lumière réfléchie rasante | `single raking warm ocre light source low lateral left out of frame grazing across copper wire surfaces` | "glowing wire ends", "light coming from the wire" |
| Highlights métalliques | `specular metallic highlights on individual copper wire strands, reflected warm light on bare copper metal` | "luminous", "emanating", "emissive" |
| Pas d'effets spéciaux | `--no glowing wire ends, emissive light, fiber optic effect, sparks` | — |

**REX** : si le prompt parle de "light catching the wire ends" sans préciser "reflected", MJ génère parfois de la lumière émissive. Être explicite sur la nature réfléchie.

### Négatifs recommandés pour le registre dark macro éditorial

```
--no white background, studio lighting, CGI render, multiple separate cables,
colored insulation wires, glassmorphism, text, watermark, glowing wire ends,
emissive light, fiber optic effect, sparks, neon, rainbow gradient
```

### Piège : l'ordre des descripteurs techniques

Un descripteur très spécifique placé en premier peut provoquer une régression.

**Exemple** : "35-degree oblique bevel angle" en première position → MJ a généré des tubes creux au lieu de fils de cuivre. Le descripteur de précision géométrique a écrasé le descripteur de sujet.

**Solution** : les descripteurs techniques très précis vont en milieu ou fin de prompt, après le sujet principal.

---

## §3 — Vary Subtle et Zoom Out : itération dans MJ

### Vary Subtle — toujours avant NB2

Après avoir sélectionné la meilleure des 4 générations initiales :
1. **Vary Subtle** sur l'image retenue → 4 nouvelles variations légèrement différentes
2. Évaluer les 4 : grain, lumière, composition, tons
3. Retenir la meilleure → c'est la base pour NB2

**Pourquoi Vary Subtle avant NB2** : Vary Subtle reste dans MJ, exploite l'espace latent de l'image. Moins destructif que de partir directement en NB2.

### Quand utiliser Zoom Out (pas NB2) pour le recadrage

Si l'image est trop serrée et que l'objectif est d'étendre le fond sombre autour du sujet :

| Outil | Ce qu'il fait | Quand l'utiliser |
|-------|---------------|------------------|
| **MJ Zoom Out 1.5×** | Étend le cadre, génère du contenu cohérent (fond noir, bokeh) | Extension modérée du fond |
| **MJ Zoom Out 2×** | Extension plus agressive | Passer de 60% à ~30% du cadre occupé par le sujet |
| **MJ Editor — Image Scale** | Réduction du sujet dans le cadre, fond étendu | Contrôle fin du placement |

**NB2 ne peut PAS faire du recadrage** (REX §6) — il tente mais soit ne change rien, soit passe en 16:9 sans préserver le ratio.

---

## §4 — NB2 : post-processing chirurgical

### Principe fondamental

NB2 traite une image existante. C'est un éditeur, pas un générateur. Sa force : multi-turn avec formule `"Keep the same image exactly as is — same [X], same [Y]. Only change [Z]."`.

**Règle absolue** : une correction par session NB2. Pas de batch.

### Routing par type de correction

| Correction | Outil | Pourquoi |
|-----------|-------|----------|
| Couleur du fond | **NB2** | Excellente isolation. Formule : "Replace only the background color — [hex actuel] → [hex cible]" |
| Grain argentique | **NB2** | Ajout organique, grade film. Formule : "Add analog film grain as if shot on 35mm" |
| Tons cuivrés (chaleur) | **NB2** | Réchauffer ou désaturer la couleur métal. Formule : "Only warm up / desaturate the copper tone on the wire surfaces" |
| Direction lumière | **MJ reprompt** | NB2 génère de la lumière émissive au lieu de réfléchie (REX critique) |
| Clair-obscur | **NB2 possible** | Assombrir les ombres. Formule : "Darken the shadow areas — sharper transition light/shadow" |
| Recadrage / zoom | **MJ Zoom Out ou Editor** | NB2 échoue sur le recadrage géométrique (REX §6) |
| Angle de prise de vue | **MJ reprompt + --iw** | Changement structurel → regénérer |
| Imperfection organique | **MJ regénération** | Modifier la structure du sujet = generation, pas édition |

### Formule NB2 universelle

```
Keep the same image exactly as is — same [composition], same [background], same [grain].

[Instruction de correction en 2-3 phrases, très précis sur la zone cible.]

Do not change the [X]. Do not change the [Y]. Only [Z].
```

### REX critique : lumière réfléchie vs émissive dans NB2

**Problème** : quand on demande à NB2 d'ajouter de la lumière sur des fils de cuivre, il génère systématiquement de la lumière émissive (halo orange, effet fibre optique, étincelles).

**Mécanisme** : NB2 associe "light on wire tips" à "wire tips emit light" — pas à "wire tips reflect external light".

**Solutions par ordre de préférence** :
1. **Ne pas demander à NB2** — décrire la lumière rasante dans le prompt MJ de génération
2. Si NB2 est inévitable : `"Important: do NOT add any glowing, sparkling, or emissive effects to the wire ends. The copper wire tips should show small metallic specular highlights — the kind you see when bare metal reflects a single off-camera light source. Think still life product photography with one key light."`
3. Ajouter en négatif : `"no sparks, no glow, no fiber optic, no emissive light"`

### Ordre recommandé des sessions NB2

Pour le registre dark mode cinéma :
1. **Fond** → corriger la couleur de fond (souvent teal/vert → bleu-nuit hex)
2. **Grain** → ajouter le grain argentique
3. **Tons** → ajuster la chaleur cuivrée si nécessaire
4. **Ombres** → renforcer le clair-obscur si nécessaire

**Attendre** entre chaque session NB2 — valider le résultat avant de passer à la suivante.

---

## §5 — Critères de validation : quand s'arrêter

### Gate "niveau élite" (à appliquer sur l'image finale)

Comparer à une image de référence Awards (pas au batch précédent — erreur de dérive du référentiel, voir REX `visual-prompting-rex.md` §biais de notation).

| Critère | Standard élite | Signal de non-conformité |
|---------|----------------|--------------------------|
| **Palette** | Hex fidèle, aucune dérive | Trop vert, trop orange, fond gris |
| **Lumière** | Réfléchie, rasante, directionnelle | Lumière émissive, halo, backlit global |
| **Grain** | Organique, argentique, dans les ombres | Bruit numérique uniforme, trop fin |
| **Contraste** | Chiaroscuro — 85-90% ombre, 10-15% lumière | Image trop plate, trop de zones claires |
| **Composition** | Sujet ancré, pas flottant | Sujet centré et isolé comme du packshot |
| **Registre** | Editorial, non-studio | Peut être vendu sur Unsplash → non conforme |

### Gate anti-Unsplash

Avant de valider : "Cette image pourrait-elle figurer dans un stock photo premium (Unsplash/Getty) ?"

- **Oui** → traitement trop sage. Pousser le grain, le contraste, le clair-obscur.
- **Non** → conforme.

---

## §6 — REX consolidé (session 2026-04-30)

### REX 1 — `--iw` silencieusement ignoré sans Image Prompt

**Problème** : ajout de `--iw 2` dans un prompt Approach A (sans image dans l'Image Prompt slot). MJ n'a pas généré d'erreur — il a juste ignoré le paramètre.

**Solution** : `--iw` ne fonctionne QUE si l'Image Prompt slot contient une image uploadée. Vérifier avant d'écrire le paramètre.

---

### REX 2 — Lumière émissive NB2 (voir §4 pour le détail)

**Problème** : NB2 a produit un halo orange + effet fibre optique au lieu d'une lumière rasante réfléchie.

**Solution** : décrire la lumière dans le prompt MJ de génération, pas dans NB2.

---

### REX 3 — MJ Retexture pour le grain = désastre

**Problème** : tentative d'utiliser MJ Retexture pour ajouter du grain argentique → résultat : texture de carrosserie de voiture (alu brossé).

**Solution** : grain argentique → NB2 exclusivement. MJ Retexture change des textures de SURFACE, pas du traitement photographique.

---

### REX 4 — Descripteur technique en première position

**Problème** : "35-degree oblique bevel angle" en début de prompt → MJ a généré des tubes creux (le descripteur géométrique a écrasé le sujet "copper wire strands").

**Solution** : descripteurs de précision géométrique en milieu ou fin de prompt, après avoir établi le sujet.

---

### REX 5 — NB2 ne recadre pas

**Problème** : demande de recadrage à NB2 (passer de 60% à 30% de surface câble) → soit aucun changement, soit passage en 16:9.

**Solution** : recadrage → MJ Zoom Out 1.5× ou 2×. MJ Editor → Image Scale pour contrôle fin.

---

### REX 6 — --sref transfère la palette, pas la lumière

**Confirmation** : même avec une image cosmos ayant une lumière rasante parfaite en style reference, MJ n'a pas reproduit cette direction lumière. La lumière doit être décrite en texte.

**Conséquence** : pour toute direction lumière non conventionnelle (rasante, contre-jour, key light latéral très précis), décrire en texte + exclusions --no. Le --sref fait le reste (grain, palette, mood).

---

### REX 7 — Séquentiel > parallèle pour les approches de référence

**Problème** : tendance à lancer les approches A et B en parallèle pour "gagner du temps".

**Solution** : tester Approche A en premier. Observer le résultat. Si conforme → aller en Passe 2 directement. Si non conforme → analyser pourquoi AVANT de lancer l'Approche B. Le parallèle empêche d'apprendre de chaque tentative.

---

## Dernière mise à jour : 2026-04-30
