# Catalogue chromatique macro — spectre exhaustif pour le routeur 3B-0a

## À quoi sert ce catalogue

Le routeur chromatique (Phase 3B-0a) reçoit ce catalogue en input et DOIT scanner CHAQUE sous-gamme listée pour la classer dans une de 3 catégories au regard des territoires créatifs du brief :

- **Autorisée** — cohérente avec l'univers évoqué par les territoires
- **Exclue** — en contradiction franche avec les territoires (interdite pour Primary/Secondary)
- **Non applicable** — étrangère au brief, ni clairement compatible ni clairement contradictoire

Le but est de fermer l'angle mort du mode sélectif précédent (le routeur générait ad hoc ~10-15 gammes en oubliant des familles entières du spectre). Avec ce catalogue, aucune famille de teinte n'est silencieusement absente du tri.

## Règles d'usage par le routeur

1. **Scan obligatoire** : passer en revue les 14 familles, ne sauter aucune sous-gamme.
2. **Reformulation des noms** : les noms du catalogue sont des CATÉGORIES génériques (ex: "Bruns / encre profonds"). Le routeur DOIT reformuler chaque sous-gamme retenue (autorisée OU exclue) avec une formule contextualisée au brief (ex: "Bruns encre profonds — sépia foncé, brou de noix, encre du cartographe"). Les "non applicables" peuvent garder un nom court.
3. **Justifications** : autorisées = lien explicite avec un mot-clé du territoire ; exclues = contradiction nommée ; non-applicables = 1 ligne suffit.
4. **Tags Source** : `TERRITOIRE`, `[SECTORIEL]`, `[SLOP_RISQUE]` selon les règles habituelles du prompt routeur.
5. **Inflation interdite** : le total des autorisées ne doit PAS dépasser ~22 sous-gammes. Au-delà, le routeur est complaisant — il faut resserrer.

---

## Catalogue (14 familles · ~33 sous-gammes)

### 1. Rouges

- **Rouges saturés vifs** — cherry, vermillon, écarlate (ex: `#d62828`, `#e63946`)
- **Rouges profonds bordeaux** — bordeaux, sang séché, sceau notarial (ex: `#5a0e1f`, `#6b1a25`)
- **Rouges désaturés / poudrés** — rouge briqueté éteint, rouge ancien (ex: `#a06060`, `#8e5a55`)

### 2. Oranges

- **Oranges saturés vifs** — orange pop, mandarine, vermillon-orangé (ex: `#e8581f`, `#f06820`)
- **Oranges désaturés / abricot poudré** — abricot terne, orange brûlé éteint (ex: `#c89070`, `#b88060`)
- **Oranges brûlés profonds** — terre cuite saturée foncée, brun-orangé (ex: `#8b3a1a`, `#7a3015`)

### 3. Jaunes

- **Jaunes vifs saturés** — jaune pop, citron, soleil (ex: `#f1c40f`, `#ffd23f`)
- **Jaunes profonds safran / moutarde** — ocre jaune saturé, moutarde dense (ex: `#b8902a`, `#c8a040`)
- **Jaunes pâles pastel** — jaune crème, paille, beurre clair (ex: `#f5e8a8`, `#efd998`)

### 4. Verts

- **Verts vifs lumineux / acidulés** — citron vert, néon-vert, menthe vif (ex: `#5fe5b8`, `#c8e040`)
- **Verts forêts profonds saturés** — vert empire, vert sapin, conifère (ex: `#1b3a2a`, `#0f3a23`)
- **Verts olives désaturés / kaki éteint** — sauge profonde, kaki militaire (ex: `#5a5e3a`, `#6e7050`)
- **Verts mousse / lichen poudrés** — mousse claire, lichen, vert poussiéreux (ex: `#6a7a4a`, `#828e60`)

### 5. Bleus

- **Bleus marine saturés classiques** — marine plein, navy, bleu roi profond (ex: `#1a2952`, `#0a1840`)
- **Bleus profonds désaturés type encre** — bleu de plan, bleu de Prusse éteint (ex: `#28384a`, `#1a2838`) ⚠ ZONE TRAINING-DEFAULTS
- **Bleus pétrole / canard désaturés** — bleu canard profond, bleu sarcelle (ex: `#1f4754`, `#2d6378`)
- **Bleus ciels / poudrés clairs** — bleu pastel, bleu poudré, ciel matinal (ex: `#a8c8e0`, `#b8d0e8`)
- **Bleus AI brillants / SaaS générique** — blue-500 Tailwind, AI-tell ⚠ SLOP — distinct des bleus encre, à exclure systématiquement (ex: `#3b82f6`, `#2563eb`)

### 6. Cyans / turquoises

- **Cyans saturés brillants / fintech** — cyan vif, turquoise saturé (ex: `#28d8d0`, `#06b6d4`)
- **Cyans désaturés / vintage** — cyan éteint, vert-de-gris bleuté (ex: `#5a8a8a`, `#6b9090`)

### 7. Violets / Indigos ⚠ ZONE SLOP_RISQUE OBLIGATOIRE

Si une variante est retenue (autorisée OU exclue avec qualification), elle DOIT être taggée `[SLOP_RISQUE]` et qualifiée par un écart explicite (cf. règles anti-slop §1 du prompt routeur).

- **Indigos profonds zone SaaS / purple monoline** — purple-500/violet-600 Tailwind par défaut ⚠ AI-TELL #1 (ex: `#4a3aa8`, `#5040b8`)
- **Violets profonds saturés** — violet d'encre, prune profonde (ex: `#5a2a90`, `#7035a8`)
- **Violets magenta-shifted profonds** — pourpre cardinalice, violet vers magenta (ex: `#7a2a5a`, `#8a3a6a`) — moins SLOP que indigo SaaS, mais qualification toujours requise
- **Lavandes claires / violets pastel** — lavande pâle, mauve poudré (ex: `#d8c8f0`, `#b8a0e8`)

### 8. Magentas / roses

- **Magentas saturés / fuchsias** — fuchsia électrique, magenta pop (ex: `#e02890`, `#d020a0`)
- **Roses saturés vifs** — cerise, framboise, rose hot (ex: `#d63365`, `#e84878`)
- **Roses pastel poudrés** — rose poudré, dragée, blush (ex: `#f5c8d0`, `#e8a8b8`)

### 9. Bruns / Ocres / Terracotta (terre profonde)

- **Bruns encre profonds** — sépia foncé, brou de noix, brun-noir (ex: `#3d2914`, `#2a1810`)
- **Ocres terreux désaturés** — terre de Sienne éteinte, ambre poudré, pigments anciens (ex: `#a17a4a`, `#c89860`)
- **Terracotta éteints** — briques poudrées, rouge-brique désaturé (ex: `#a8624c`, `#b87358`)
- **Brun-rouille / brun bois clair** — bois de chêne, brun rouille moyen (ex: `#8a5a3a`, `#9a6a4a`)

### 10. Beiges / sables (terre claire)

- **Beiges sables clairs** — sable du désert, lin écru, beige doux (ex: `#d8c8a8`, `#e0d2b3`)
- **Off-whites crémeux orientés ivoire** — papier vélin, parchemin clair, crème (ex: `#f4ecd8`, `#fdf6e3`)

### 11. Off-whites orientés

- **Off-whites bleutés** — blanc cassé froid, blanc nuage, blanc-cyan léger (ex: `#eef2f6`, `#e8edf3`)
- **Off-whites rosés / ivoires chauds** — blanc poudré, blanc-rosé subtil (ex: `#f7eeea`, `#f5ebe6`)
- **Off-whites verdâtres / chalk** — blanc craie, blanc-vert subtil, papier ancien (ex: `#eff0e8`, `#ebede0`)

### 12. Off-blacks orientés

- **Off-blacks tirant vers le brun-encre** — noir d'iroko, noir sépia, noir-encre (ex: `#1f1810`, `#15100a`)
- **Off-blacks tirant vers le bleu-nuit** — noir d'astronomie, noir-marine, noir d'encre bleue (ex: `#0f1418`, `#0a0f15`)
- **Off-blacks anthracites profonds** — noir charbon, anthracite très profond, sans orientation chromatique (ex: `#181818`, `#1a1a1a`) ⚠ marqueur slop si retenu sans qualification

### 13. Gris orientés

- **Gris taupes profonds** — taupe vers brun-encre, gris-chair (ex: `#544a40`, `#665a4f`)
- **Gris ardoises bleutés profonds** — ardoise, gris-bleu profond (ex: `#4a5560`, `#5a6470`)
- **Gris anthracites / graphite** — graphite profond, gris-noir industriel (ex: `#2a2e34`, `#383c42`)

### 14. Métalliques

- **Or vieilli mat / dorés patinés** — dorure de manuscrit ancien, or mat (PAS or brillant clinquant) (ex: `#b8941f`, `#a07a18`)
- **Cuivres / bronzes mats patinés** — métal d'atelier, bronze travaillé (ex: `#8b5a2b`, `#b87333`)
- **Argent / chrome brillant** — métal brillant industriel, chrome (ex: `#c8c8d0`, `#d0d0d8`)

---

## Hors-catalogue (à exclure systématiquement, sauf cas exotique très explicite)

Cette annexe regroupe des familles qui sont des marqueurs slop universels — leur exclusion est tacite mais le routeur peut les expliciter en exclues si le brief touche à un univers qui flirte avec ces zones (ex: rave, kids, fintech-flashy).

- **Néons / fluorescents** (vert lime fluo, rose hot fluo, jaune néon, cyan fluo) — `#d8ff10`, `#ff0a8a`, `#0aff8a`
- **Gradients arc-en-ciel multi-stops** — pas une "gamme" mais un anti-pattern souvent slop
- **Gradients AI/SaaS purple→pink standards** — purple-500 → pink-500 Tailwind (ex: `#a855f7` → `#ec4899`)

---

## Note sur la couverture

Ce catalogue couvre ~33 sous-gammes du spectre macro. Il n'est PAS exhaustif au niveau des nuances Pantone ou RAL — c'est une grille de scan pour le routeur, pas un nuancier complet. Les sous-gammes sont définies au grain "familial" (la finesse du nuancier final est l'affaire du subagent palette en aval).

## Maintenance

À mettre à jour si :
- Une nouvelle famille macro émerge dans la culture visuelle (peu probable à court terme)
- Un test E2E révèle qu'une sous-gamme manque (rare — c'est le filet de sécurité d'avoir l'option Charles d'ajouter manuellement au checkpoint user)
- Une sous-gamme se révèle redondante (ex: deux variantes qui ne se distinguent jamais en pratique → fusionner)

## Dernière mise à jour : 2026-05-05
