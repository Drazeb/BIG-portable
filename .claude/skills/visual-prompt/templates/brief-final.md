# Brief image — {NOM_IMAGE}

**Concept** : {NOM_CONCEPT} — {DESCRIPTION_COURTE_CONCEPT}
**Marque** : {NOM_MARQUE}
**Image source** : {CHEMIN_FICHIER_IMAGE}
**Date de validation** : {DATE_AAAA-MM-JJ}

---

## 1. Description visuelle

{Narration spatiale et lumineuse de l'image en 1-2 paragraphes. Décrire :
- Le sujet et son positionnement dans le cadre (diagonale, centré, excentré)
- La direction et la nature de la lumière (rasante, frontale, contre-jour, réfléchie/émissive)
- Les zones d'ombre et leur rapport à l'image (% de couverture)
- Les éléments graphiques secondaires (ombres portées, reflets, effets de matière)}

---

## 2. Palette exacte par zone

| Zone | Couleur | Hex | Rôle |
|------|---------|-----|------|
| {Zone 1 — ex: Fond} | {Description tonale} | `{HEX}` | {Rôle dans la composition} |
| {Zone 2} | {...} | `{HEX}` | {...} |
| {Zone 3} | {...} | `{HEX}` | {...} |
| {Zone 4} | {...} | `{HEX}` | {...} |

Tension chromatique centrale : **{TON_CHAUD #HEX}** contre **{TON_FROID #HEX}** (ou tout autre rapport — analogique, complémentaire, monochrome).

---

## 3. Texture et grain

- {Type de grain : argentique 35mm pull-processed / moyen format / numérique discret / etc.}
- {Visible dans les ombres ? les hautes lumières ? les deux ?}
- {Texture des matières principales : mate / brillante / spéculaire / micro-relief}
- {Anti-pattern à éviter : pas de bruit numérique uniforme, pas de rendu 3D lisse}

---

## 4. Ratios et composition

- **Format** : {ex: 3:4 portrait éditorial}
- **Occupation du sujet** : {ex: ~55-60% du cadre}
- **Espace négatif** : {ex: ~40-45% de fond pur en bas-droite et haut-droite}
- **Ligne de force dominante** : {ex: diagonale haut-gauche → bas-droite}
- **Point focal** : {ex: zone cuivre au centre-bas}

---

## 5. Intention créative

**Concept incarné** : {Phrase d'1-2 lignes — qu'est-ce que cette image dit du concept de marque ?}

**Registre** : {ex: Editorial Grid × Dark Mode Cinema. Pas de la photographie produit — de la photographie éditoriale de presse spécialisée.}

**Ton** : {ex: contemplatif, premium, technique-poétique. Ni clinique, ni spectaculaire.}

---

## 6. Usages possibles dans un livrable design

L'image peut être utilisée :
- **Hero pleine largeur** : {oui/non, conditions — ex: avec overlay sombre si du texte passe dessus}
- **Bloc éditorial** : {oui/non, position recommandée — droite ou gauche du texte}
- **Détail / Accent** : {oui/non, crop suggéré — ex: crop serré sur la zone cuivre}
- **Fond watermark** : {oui/non, opacité recommandée — ex: 40-60%}

---

## 7. Ce que cette image n'est PAS

- {Anti-pattern 1 — ex: pas une image produit ou packshot studio}
- {Anti-pattern 2 — ex: pas une image "danger / attention" (pas d'orange sécurité, pas de jaune d'avertissement)}
- {Anti-pattern 3 — ex: pas un rendu 3D ou une illustration — c'est de la photographie argentique}
- {Anti-pattern 4 — ex: pas de science-fiction (pas de lumière émissive, pas d'arcs électriques)}

---

## 8. Références d'ambiance

- {Référence 1 — photographe / film / magazine — ex: Photographie de Peter Lippmann (still life macro éditorial)}
- {Référence 2 — ex: Covers de revues d'ingénierie haut de gamme (Scientific American, Wired print)}
- {Référence 3 — ex: Palettes cinéma Blade Runner 2049 (bleu-nuit + ambre)}

---

## 9. Métadonnées techniques

- **Approche MJ retenue** : {Option A (sref seul) / Option B (composition + style) / Option C (from scratch)}
- **Prompt MJ final** :
```
{PROMPT_MJ_TEXTE_INTÉGRAL}
```
- **Corrections NB2 appliquées** (dans l'ordre) :
  1. {Correction 1 — ex: Fond bleu-nuit → #1A2231}
  2. {Correction 2 — ex: Grain argentique 35mm pull-processed}
  3. {Correction 3 — ex: Réchauffement tons cuivrés vers #C89A6E}
  4. {Correction N}
- **Ancre stylistique verrouillée** : voir `01-anchor.md`
- **Nombre total d'itérations** : {N batchs MJ + N corrections NB2}
- **Gate élite passée le** : {DATE_AAAA-MM-JJ}
