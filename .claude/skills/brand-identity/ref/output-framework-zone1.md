# Framework d'Output — Zone 1 : Le Showroom

Ce document définit les règles absolues pour la génération du **Style-Tile HTML** en Zone 1 (Showroom).

---

## 1. CONCEPT FONDAMENTAL

La Zone 1 est un fichier **HTML unique** qui présente l'identité de marque comme une **expérience immersive** (Diegetic UI). C'est une vitrine émotionnelle, pas une documentation technique.

**Métaphore** : Tu présentes au CEO. Tu vends de l'émotion. Zéro technique visible.

---

## 2. LE SCREENSHOT TEST (Règle d'Étanchéité)

Pour savoir si un élément a le droit d'exister en Zone 1, pose cette question binaire :

> "Si je fais une capture d'écran du site final en production, est-ce que cet élément est visible par le client ?"

| Réponse | Action | Exemples |
|---------|--------|----------|
| **OUI** (c'est du contenu) | AUTORISÉ en Zone 1 | Titre, photo, bouton, dégradé de fond, illustration, slogan |
| **NON** (c'est de la méta-donnée) | BANNISSEMENT vers Zone 2 | Code HEX, nom de police, règle CSS, grille visible, nuancier |

**Note sur les photos et illustrations** : Les visuels de référence fournis par l'utilisateur (photos, illustrations) sont du **contenu autorisé** en Zone 1. Intégrés en base64, ils sont invisibles en tant que données techniques — l'utilisateur voit l'image, pas l'encodage. Ils passent le Screenshot Test car ils sont exactement ce qu'on verrait sur le site final en production.

---

## 3. LA RÈGLE DU MAÇON (No Scaffolding Left Behind)

Quand tu construis la Zone 1 (la Maison), tu ne laisses pas les échafaudages.

### Interdictions formelles
- **INTERDIT** : Numéros de section du guide (ex: "01.", "05.", "10.") dans le texte visible
- **INTERDIT** : Specs techniques (Hex codes, noms de fonts, tailles de pixels, stroke-width) dans le texte visible
- **INTERDIT** : Nuanciers abstraits (carrés de couleur isolés) ou noms de police affichés ("Inter", "Agikile")
- **INTERDIT** : Tout label qui ressemble à une documentation

### Transformation sémantique obligatoire
Avant d'écrire une ligne de code, traduis le concept technique en concept marketing :

| Concept technique | Devient en Zone 1 |
|-------------------|--------------------|
| Color System (02) | L'ambiance visuelle du site |
| Iconography (06) | La section Features / Services |
| Data Viz (07) | La section Preuve de Performance |
| Typography (03) | Le rythme éditorial incarné |

### Le Test Final
> "Si ça ressemble à une documentation, supprime-le."

---

## 4. FORMAT TRIPTYQUE OBLIGATOIRE

Le Style-Tile HTML est structuré en **3 blocs** obligatoires :

### A. Le Voice Block (Hero Header)

La Brand Identity exprimée par les **mots et la typographie**.

- **Fonction** : Montrer le Tone of Voice, la hiérarchie typographique, les couleurs primaires en contexte
- **Contenu** : Un titre percutant (H1), un sous-titre (H2 ou lead), un call-to-action — tout en contenu fictif mais réaliste et aligné avec le brief
- **Inputs piliers** : Typographie (03) + Tone of Voice (01) + Couleurs (02)
- **Interdit** : Tout texte qui ressemble à "Ceci est notre titre Display en 48px"

### B. L'Artefact Témoin (Component Witness)

Un **composant UI complexe** incarnant la "physique" de la marque.

- **Fonction** : Montrer les radius, ombres, espacements, micro-interactions en contexte réel
- **Contenu** : Une carte, un dashboard widget, un pricing block, ou un composant métier — en contenu fictif réaliste lié au brief
- **Inputs piliers** : Code Civil (04) + Couleurs (02) + Grille de rythme (04)
- **Le meilleur test** : "Est-ce que ce composant pourrait exister dans le vrai produit ?"

### C. L'Atmosphere Block (Mood Footer)

Une section immersive qui utilise les codes graphiques **sans jamais les expliquer**.

- **Fonction** : Créer une ambiance de clôture, un "mood" global — footer, manifesto, ou section "vision"
- **Contenu** : Du contenu fictif réaliste (slogan, copyright, statut serveur, citation de manifesto)
- **Inputs piliers** : Couleurs (02) + Grille (04) + Atmosphère générale
- **Règle Diegetic UI** : Tout doit ressembler à un vrai site — pas à un moodboard

---

## 4bis. BRIEF VISUEL (livrable optionnel, entre Phase 3 et Phase 4)

Si l'utilisateur choisit de fournir des visuels de référence après validation des 3 concepts, l'orchestrateur génère un **Brief Visuel** par concept sélectionné. Ce brief contient : description libre du registre attendu, prompts IA prêts à copier-coller (avec `--no` exhaustif intégrant tous les négatifs directionnels), et palette cible. C'est un livrable intermédiaire qui guide l'utilisateur dans la sélection ou la génération de visuels cohérents avec le concept.

Les visuels fournis sont ensuite intégrés comme éléments structurants dans le Style-Tile (voir html-showroom-spec.md §8).

---

## 5. LOIS D'EXCELLENCE

1. **Loi d'Excellence** : Un design "moyen" est un échec
2. **Loi d'Intensité** : Calibrer l'audace selon les Curseurs A & B
3. **Fichier Unique** : Ne jamais créer de v2 — toujours mettre à jour le même fichier
4. **Verrouillage Génétique** : Une fois validés, les styles deviennent des constantes immuables
5. **Cohérence Curseurs** : Le HTML doit incarner visuellement les scores A×B du concept choisi

---

## 6. PROTOCOLE D'AUTO-CONTRÔLE (Zone 1)

Avant chaque export, vérifier mentalement :

- [ ] **Single File** : Ai-je réutilisé le même filepath ?
- [ ] **Diegetic UI** : L'Atmosphere Block ressemble à un vrai site (footer, manifesto) et NON à un nuancier ?
- [ ] **Screenshot Test** : Aucune méta-donnée visible (HEX, noms de fonts, tailles) ?
- [ ] **Mason's Rule** : Aucun label de documentation visible ("01.", "Section Color") ?
- [ ] **Cursor Coherence** : Le niveau d'audace visuel correspond aux scores A×B ?
- [ ] **Brief Alignment** : Le contenu fictif est cohérent avec le brief de la marque ?
