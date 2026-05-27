# REX — Intégration des visuels dans les Style-Tiles (Phase 4)

Date : 2026-03-04
Session : test-camille-test-20260303-2234
Observé par : Charles + Claude

---

## Problème

Les images générées en Phase 3C (Recraft/MidJourney) ne sont pas intégrées de manière cohérente dans les style-tiles HTML de la Phase 4. Le résultat donne une impression de "cadre photo posé sur un mur" plutôt que de "mur conçu autour du tableau". L'image est plaquée dans un conteneur CSS avec `object-fit: cover`, mais la composition globale (layout, overlays, padding, masques, blend-modes) n'a pas été pensée EN FONCTION du contenu visuel réel de l'image.

Le rendu est propre techniquement, mais l'intégration manque de dialogue entre l'image et le design.

---

## Cause racine : le subagent Phase 4 ne voit jamais les images

### Chaîne d'événements réelle (session Camille)

1. **Phase 3C** : L'orchestrateur génère les prompts visuels → l'utilisateur génère les images sur Recraft/MJ → l'utilisateur fournit les fichiers → l'orchestrateur les copie, les redimensionne (1200px), et les encode en base64.

2. **Calcul de la taille base64** : Les fichiers encodés font entre 325K et 3.9M de caractères, soit **~80K à ~990K tokens par image**. Pour le concept 2 (L'Observatoire) avec 3 images, le total base64 dépassait **1.8M tokens** — soit largement plus que la fenêtre de contexte d'un subagent.

3. **Décision de l'orchestrateur** : Utiliser le **protocole placeholder** (`<!-- PLACEHOLDER:visual-cX-Y -->`). Le subagent génère le HTML avec des commentaires marqueurs, puis l'orchestrateur injecte les images en post-traitement via un script Python.

4. **Conséquence** : Le subagent Phase 4 a reçu :
   - La **description textuelle** de chaque image (sujet, dimensions, palette)
   - L'**instruction** que des images seraient injectées aux endroits marqués
   - Les **règles CSS** d'intégration (object-fit, overlay, blend-mode)

   Mais il n'a **jamais vu un seul pixel**. Il a donc conçu un layout avec des zones réservées, sans pouvoir adapter :
   - Le cadrage CSS (clip-path, mask) au contenu réel de l'image
   - Les overlays/gradients aux zones claires/sombres de l'image
   - Le positionnement des éléments textuels par rapport à la composition de l'image
   - Les blend-modes au contraste et à la palette effective (pas seulement théorique)

### Pourquoi le protocole placeholder a été choisi

Le `{visual_reference_block}` dans SKILL.md (lignes 1080-1103) prévoit d'insérer les images base64 DIRECTEMENT dans le prompt du subagent. Mais :

| Image | Taille base64 | ~Tokens |
|-------|---------------|---------|
| c1-1 (clivage) | 325 KB | ~81K |
| c1-2 (réseau) | 1.4 MB | ~356K |
| c2-1 (observatoire) | 1.3 MB | ~318K |
| c2-2 (coupole) | 3.9 MB | ~991K |
| c2-3 (instrument) | 2.1 MB | ~522K |

Un subagent reçoit déjà ~30-50K tokens de contexte (ref files + pitch + exemple + prompt). Ajouter 400K-1.8M de tokens base64 dépasse la capacité.

Le SKILL.md mentionne le protocole placeholder (ligne 1102) mais le traite comme un cas normal — il ne prévoit pas que l'injection post-traitement CASSE le dialogue image/composition.

---

## Ce qu'on a essayé (et pourquoi ça ne résout pas tout)

### Approche actuelle : placeholder + injection post-traitement
- **Résultat** : Layout structurellement correct (les images sont aux bons endroits) mais intégration visuelle générique
- **Pourquoi insuffisant** : Le subagent ne peut pas adapter la composition au contenu réel de l'image. Il met un `object-fit: cover` dans un conteneur, point.

### Alternative théorique : passer les images en base64 au subagent
- **Bloquée par** : la taille des base64 (80K à 990K tokens par image). Même une seule image de taille moyenne consommerait plus de contexte que tout le reste du prompt combiné.

---

## Solutions proposées

### Solution A — Redimensionnement agressif pour prompt (recommandée, impact moyen)

**Idée** : Créer une version très compressée de chaque image (~400px de large, JPEG qualité 60) spécifiquement pour le prompt du subagent. L'image haute résolution reste pour l'injection finale.

**Chaîne modifiée** :
1. Image originale → copie dans session dir (existant)
2. Version web 1200px pour injection finale (existant)
3. **NOUVEAU** : Version prompt ~400px JPEG basse qualité pour le subagent
4. Le subagent reçoit les images basse résolution DANS son prompt → il VOIT le contenu
5. Il génère le HTML avec les images basse résolution intégrées
6. Post-traitement : remplacer les images basse résolution par les versions haute résolution

**Estimation de taille** (400px wide, JPEG q60) :
- Image 1024×1024 → ~400×400 → ~15-25 KB → ~20-33K caractères b64 → **~5-8K tokens**
- Image 1536×1024 → ~400×267 → ~10-20 KB → ~13-27K caractères b64 → **~3-7K tokens**
- 2-3 images par concept → **~10-20K tokens supplémentaires** (gérable)

**Implémentation** :
```bash
# Étape 3e bis — Version prompt (basse résolution)
sips --resampleWidth 400 "{image}" --out "{session_dir}/.tmp-prompt-{n}.png"
# Convertir en JPEG basse qualité pour réduire encore
sips -s format jpeg -s formatOptions 60 "{session_dir}/.tmp-prompt-{n}.png" --out "{session_dir}/.tmp-prompt-{n}.jpg"
base64 -i "{session_dir}/.tmp-prompt-{n}.jpg" -o "{session_dir}/.tmp-prompt-{n}.jpg.b64"
```

**Avantage** : Le subagent voit RÉELLEMENT les images (composition, zones claires/sombres, bords). Même à 400px, c'est suffisant pour adapter un layout CSS.

**Risque** : ~10-20K tokens supplémentaires par subagent. Acceptable si le reste du prompt est optimisé.

**Modification SKILL.md** : Ajouter une étape 3e-bis de génération des versions prompt. Modifier le `{visual_reference_block}` pour utiliser les versions basse résolution dans le prompt et les versions haute résolution pour l'injection post-traitement.

### Solution B — Passe de raffinement post-injection (alternative, impact léger)

**Idée** : Après injection des images haute résolution, relancer le subagent avec le HTML complet (il peut voir les images intégrées) pour affiner uniquement l'intégration visuelle.

**Chaîne modifiée** :
1. Phase 4 actuelle (subagent sans images) → HTML avec placeholders
2. Injection base64 (existant)
3. **NOUVEAU** : Relancer le subagent avec instruction ciblée : "Voici le HTML avec les images injectées. Ajuste UNIQUEMENT l'intégration visuelle (overlays, masks, blend-modes, padding, clip-path). Ne touche pas au contenu ni à la structure générale."

**Problème** : Le subagent devrait lire un fichier HTML de 500K-4M lignes (à cause du base64 inline). La lecture du HTML par Read tool tronque à 2000 lignes. Le subagent ne verrait que le début du fichier.

**Variante** : Le subagent reçoit seulement le CSS + la structure HTML (sans le base64), plus les images en version basse résolution. Il modifie le CSS d'intégration, et l'orchestrateur réinjecte.

**Avantage** : Ne change pas le flow existant, s'ajoute en option.
**Inconvénient** : Double le coût en tokens de la Phase 4. Le raffinement est moins bon qu'une conception intégrée dès le départ.

### Solution C — Description visuelle structurée (fallback, impact faible)

**Idée** : L'orchestrateur (qui est multimodal et VOIT les images) génère une description structurée très détaillée de chaque image, orientée composition CSS.

**Format enrichi** (en plus de la palette/mood existants) :
```markdown
### Image c2-1 — Observatoire stratégique
- **Palette** : #1B2838 (65%), #C8956C (15%), #E8DDD0 (20%)
- **Zone focale** : tiers supérieur-gauche (coupole cuivre)
- **Zones sombres** : bas + coins (ciel nuit), utilisables comme fond de texte
- **Zones claires** : centre-droite (murs crème), contraste suffisant pour overlay sombre
- **Bords** : transition douce vers sombre en bas → bon pour gradient-to-background
- **Composition interne** : verticale dominante (tour), lignes de fuite vers le haut
- **Recommandation CSS** : placer dans la partie supérieure du voice-block, gradient linéaire vers le bas pour fondre dans le texte. mix-blend-mode: multiply possible sur les zones cuivre.
```

**Avantage** : Zéro coût token supplémentaire par rapport à l'existant (la description remplace simplement la description actuelle par une version plus riche).
**Inconvénient** : Le subagent travaille toujours à l'aveugle — même une bonne description ne remplace pas la vision directe. Mieux que rien, nettement moins bon que Solution A.

---

## Recommandation

**Solution A (prompt basse résolution)** comme changement principal :
- Coût token maîtrisé (~10-20K par subagent)
- Le subagent voit les images → peut adapter la composition
- Transparent pour l'utilisateur (même flow)
- L'injection haute résolution reste en post-traitement

**Solution C (description structurée)** en complément systématique :
- Même si le subagent voit l'image basse résolution, la description enrichie oriente les choix CSS
- Utile aussi comme fallback si une image est trop grande même en basse résolution

**Solution B (raffinement)** en dernier recours :
- Pour les cas où Solution A ne suffit pas (image très spécifique nécessitant un ajustement fin)
- Ou comme passe optionnelle de polish

---

## Modifications SKILL.md à prévoir

### 1. Étape 3e — Ajouter la génération des versions prompt

Après le redimensionnement web (1200px), ajouter :

```
3e-bis. Créer une version prompt basse résolution :
   sips --resampleWidth 400 "{image}" --out "{session_dir}/.tmp-prompt-{n}.png"
   sips -s format jpeg -s formatOptions 60 ".tmp-prompt-{n}.png" --out ".tmp-prompt-{n}.jpg"
   base64 -i ".tmp-prompt-{n}.jpg" -o ".tmp-prompt-{n}.jpg.b64"
```

### 2. Étape 3f — Enrichir le `{visual_reference_block}`

Modifier le bloc pour inclure :
- Les images **basse résolution** (base64 de la version 400px JPEG) DANS le prompt
- La description structurée enrichie (zones focales, bords, recommandations CSS)
- L'instruction que les images haute résolution seront injectées en post-traitement aux mêmes emplacements

### 3. Phase 4 — Modifier le protocole placeholder

Le subagent n'utilise plus de placeholders. Il intègre directement les images basse résolution (qui sont assez petites pour tenir dans le prompt). Le post-traitement remplace ensuite les `src="data:image/jpeg;base64,{basse_res}"` par `src="data:image/png;base64,{haute_res}"`.

Pattern de remplacement post-traitement :
```python
# Remplacer chaque image basse résolution par sa version haute résolution
for key in images:
    low_res_b64 = read(f'.tmp-prompt-{key}.jpg.b64')
    high_res_b64 = read(f'{brand}-visual-{key}-web.png.b64')
    html = html.replace(low_res_b64, high_res_b64)
```

### 4. Phase 4 — Garder le protocole placeholder en fallback

Si la taille totale des images basse résolution dépasse un seuil (~50K tokens pour un concept), revenir au protocole placeholder actuel + Solution C (description structurée enrichie).

---

## Pourquoi ça marchera

La Solution A fonctionne parce que :
1. **Le subagent est multimodal** — il peut interpréter une image dans son prompt, même basse résolution
2. **400px suffit pour la composition** — les choix de layout CSS (placement, overlay, mask, blend-mode) dépendent de la structure de l'image (zones claires/sombres, composition), pas de la résolution
3. **Le coût est contenu** — ~5-8K tokens par image, soit ~15-24K pour 3 images, largement dans le budget d'un subagent
4. **Le post-traitement est simple** — remplacer un base64 par un autre dans le HTML est une opération déterministe

Le résultat attendu : le subagent conçoit un layout qui **dialogue** avec l'image réelle — gradients adaptés aux zones sombres, texte positionné sur les zones lisibles, masques CSS qui suivent la composition de l'image — puis l'orchestrateur swape la basse résolution pour la haute résolution sans toucher au CSS.

---

## Solution retenue (implémentée 2026-03-04)

**Solution A (prompt basse résolution) + Solution C (description enrichie)** combinées.

### Mécanisme

1. **Étape 3e** : l'image est copiée/redimensionnée à 1200px (haute résolution) + nommage `{brand}-visual-c{concept}-{n}.{ext}` (associe explicitement l'image à son concept)
2. **Étape 3e-bis** : version 400px JPEG q60 créée dans `.tmp-prompt-c{concept}-{n}.jpg` (~5-8K tokens)
3. **Analyse enrichie** (3e, step 4) : palette + zone focale + zones sombres/claires + bords + composition + recommandation CSS
4. **`{visual_reference_block}`** : fiche visuelle enrichie + images basse résolution avec `data-visual="c{concept}-{n}"`
5. **Subagent Phase 4** : VOIT les images (basse résolution), compose en fonction, préserve `data-visual`
6. **Étape 4A-bis** : script Python scanne les `{brand}-visual-c*-*.*.b64`, matche les `data-visual` dans le HTML, swap `src` vers haute résolution
7. **Étape 5B** : re-swap après itération subagent (le subagent travaille toujours en basse résolution)

### Budget tokens

| Élément | Tokens |
|---------|--------|
| Image basse résolution (400px JPEG q60) | ~5-8K |
| Fiche visuelle enrichie | ~0.2K |
| Total pour 2 images × 1 concept | ~10-16K |
| Total pour 3 images × 1 concept | ~15-24K |
| Contexte subagent existant (ref + pitch + exemple) | ~30-50K |

Acceptable : le surcoût images (~15-24K) reste < 50% du contexte subagent.

### Nommage

| Fichier | Pattern |
|---------|---------|
| Haute résolution | `{brand}-visual-c{concept}-{n}.{ext}` |
| Base64 haute résolution | `{brand}-visual-c{concept}-{n}.{ext}.b64` |
| Basse résolution prompt | `.tmp-prompt-c{concept}-{n}.jpg` |
| Base64 basse résolution | `.tmp-prompt-c{concept}-{n}.jpg.b64` |
| Attribut HTML | `data-visual="c{concept}-{n}"` |

### Zones vérifiées (pas de régression)

- **Batch allègement** (SKILL.md) : regex `data:image/[^"]+` fonctionne post-swap
- **Packaging extraction** (SKILL.md) : regex d'extraction fonctionne post-swap
- **Étape 3G archive** : globs étendus couvrent tous les formats + `.tmp-prompt-c*`
- **Mode Brand Existante (D)** : pas de Phase 3C, pas impacté
- **Phase Logo** : placeholders SVG, pas impacté
