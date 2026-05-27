# Typographie — Core (Critique TIER 2/3)

Règles sémantiques universelles de typographie. Lues par les Critiques spécialisés (audit-slop, audit-elite) lors de la phase de jugement, **pas** par le Designer en mode CRÉATION. Les listes nominatives (fonts à éviter, hex de couleur typo, valeurs précises de letter-spacing/line-height) vivent dans les gates Python — pas dans ce fichier.

**Portée** : critères d'audit transverses — s'appliquent quel que soit le curseur A, le registre atmosphérique, le concept narratif. Importé par les Critiques de Phase 4 (styletile + artefact), Batch 2, Batch 3.

---

## §1 — Sélection des fontes

### Procédure de choix
La sélection part des mots-clés du brief, identifie l'objet ou le caractère physique évoqué (matière, époque, tempérament), puis explore au-delà des défauts de rendu IA. **Le but est l'unicité au service du concept, pas la familiarité rassurante**. Une fonte qui sonne immédiatement "déjà-vu" est un signal d'alarme — la procédure doit être reprise.

**Clause anti-cousin** : éviter une famille suspecte ne suffit pas. Ses cousins visuels (même époque, mêmes proportions, même rendu géométrique ou humaniste) sont à éviter aussi. Un choix final qui ressemble au réflexe initial = procédure non aboutie.

### Single font + weights par défaut
Par défaut, **une seule famille typographique** exploitée sur plusieurs weights. L'ajout d'une seconde famille n'est légitime que pour produire un contraste structurel intentionnel — pas pour "varier". Une famille bien exploitée porte presque toujours plus loin qu'un duo timide.

### Variété intra-famille avant pairing
Avant d'introduire une seconde famille, exploiter la variété disponible dans la première : weights, widths, italics, optical sizes. Le pairing à deux familles n'est pertinent que quand la première a montré ses limites — pas en réflexe initial. Cette règle est complémentaire à "single font par défaut" : elle dicte la séquence d'exploration.

---

## §2 — Pairing et hiérarchie typographique

### Contraste multi-axes en cas de pairing
Si pairing assumé : contraste sur **plusieurs axes structurels simultanément** — sans-serif vs serif, géométrique vs humaniste, condensée vs large, époque historique différente. Deux sans-serif aux proportions proches ne forment pas un pairing — c'est une collision. Le contraste doit être lisible au premier coup d'œil.

### Étalage de weights minimum
La hiérarchie typographique exige un étalage minimum de **trois niveaux de weight** distincts (ex. Regular + Medium + SemiBold ou équivalent). Sans cette amplitude, la hiérarchie est plate : titres et corps se ressemblent, et l'œil ne sait pas où regarder.

### All-caps : usage rare et intentionnel
L'all-caps est un outil d'emphase rare, pas un default pour les sous-titres ou les labels. Préférer **lowercase italic, sentence case ou small-caps** selon le ton. L'all-caps systématique sur les overlines ou les sections est un marqueur de template — il vide la hiérarchie de son intention.

---

## §3 — Réglages typographiques fins

### Type fluide vs type fixe selon surface
**Type fluide (`clamp()`)** : acceptable et souvent souhaitable sur les surfaces marketing et éditoriales — il accompagne le viewport. **Type fixe (`rem`)** : préférable sur les interfaces app/dashboard où la stabilité de la grille et la prévisibilité priment sur la fluidité visuelle. Le bon choix dépend de la nature de la surface, pas d'un dogme.

### Letter-spacing inverse au corps
**Letter-spacing négatif** sur les larges headers — sans cela ils paraissent visuellement aérés et perdent en densité. **Letter-spacing positif** sur les small caps, labels et overlines petits — sans cela la lisibilité chute. Le sens du tracking est inverse à la taille du corps.

### Line-height inverse à la longueur de ligne
Le line-height est proportionnel **inverse** à la longueur de ligne : ligne courte → interligne resserré, ligne longue → interligne ample. Sur du texte light-on-dark, ajouter un complément d'aération minimum à mesurer empiriquement — la lecture sur fond sombre exige plus d'air. Une valeur unique d'interligne pour toute la page est un signal de réglage absent.

### Features OpenType pertinentes activées
Les features OpenType ne sont pas automatiques : elles s'activent là où elles servent. **Tabular numerals (`tnum`)** sur les colonnes de chiffres et données financières — sinon les colonnes vibrent. **Small-caps** pour les abréviations dans le corps de texte — les majuscules normales déséquilibrent la grise typographique. **Ligatures désactivées** sur le code et le monospace — elles parasitent la lecture technique.

---

## Règles SKIP (déjà couvertes ailleurs)

Aucune règle n'a été skippée à la création. Les règles touchant aux fontes nominatives (training-data defaults, geometric sans-serifs des années 2010) restent dans `anti-slop-blacklist-core.md §3` et le gate Python `phase4-blacklist-gate.py`.

---

## Source et traçabilité

**Origine** : règles sémantiques extraites du skill `audit-slop` (R-014, R-015, R-016, R-018, R-019, R-102, R-103, R-106, R-107, R-011), reformulées en Niveau 1-2 selon `anti-slop-formulation-guide.md`.

**Lecteurs prévus** : Critiques TIER 2/3 (audit-slop, audit-elite). Le Designer en mode CRÉATION ne lit PAS ce fichier — il reçoit les principes via les phases 3B/4 et la procédure de matching font.

## Dernière mise à jour

2026-04-26 — Création. Étape 3 du plan d'intégration anti-slop (Vague 2).
