# REX — Injection SVG dans les Batches HTML (Post-traitement logo)

**Date** : 2026-02-23
**Contexte** : Phase 6A (Batch 2 — Système de Signes), session `camille-2-2-v8`, concept "La Partition"

---

## Problème 1 — SVG injectés invisibles (zone vide à la place du logo)

### Description
Après injection des SVG logos via le script Python de post-traitement (remplacement des `<!-- PLACEHOLDER:LOGO_* -->`), les logos sont bien présents dans le HTML (vérifiable avec `grep "<svg"`) mais **ne s'affichent pas visuellement** dans le navigateur. L'espace réservé au logo est vide — on voit le conteneur (fond, texte narratif en dessous) mais pas le SVG.

Sections impactées : **toutes** celles contenant un logo injecté (05.1 Concept & Symbolique, 05.2 Lockups, 05.3 Zone d'exclusion, 05.4 Variantes de contexte).

### Cause racine : 2 problèmes combinés

#### Cause A — Pas de dimensions explicites sur le SVG

Les fichiers SVG produits par vtracer (vectorisation logo) ont un `viewBox` mais **pas d'attributs `width`/`height`** :

```html
<svg xmlns="http://www.w3.org/2000/svg" viewBox="529 319 1014 1423">
  <!-- pas de width ni height -->
```

Quand ce SVG est injecté dans un conteneur **flex** (`display: flex; align-items: center; justify-content: center;`), le navigateur ne sait pas quelle taille intrinsèque donner au SVG. Résultat : le SVG se collapse à 0×0 ou prend une taille par défaut (300×150) qui ne correspond pas au viewBox, et le contenu déborde invisiblement.

**Règle CSS/SVG** : Un SVG sans `width`/`height` dans un conteneur flex n'a pas de taille intrinsèque. Le navigateur utilise le "replaced element" sizing algorithm qui peut produire des résultats imprévisibles selon le contexte de layout.

#### Cause B — Déclaration `<?xml?>` inline dans le HTML

Le script d'injection copie le contenu brut des fichiers `.svg`, qui commencent par :

```
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" ...>
```

La déclaration `<?xml?>` est valide dans un fichier SVG autonome, mais **invalide quand le SVG est injecté inline dans du HTML5**. Certains navigateurs (Safari notamment) traitent cette déclaration comme un nœud de commentaire ou de processing instruction, ce qui peut casser le parsing du SVG qui suit.

### Impact

- **100% des logos injectés** étaient invisibles dans le Batch 2
- Le problème est **silencieux** : aucune erreur console, le HTML est valide, le SVG est bien dans le DOM — il ne s'affiche simplement pas
- Affecte toutes les phases qui utilisent l'injection SVG post-traitement : **6A (Batch 2)**, potentiellement **6B (Batch 3)** et **6C (Batch 4)**

---

## Solution retenue

### Fix A — Ajouter des règles CSS de dimensionnement SVG dans le prompt subagent

Le prompt Batch 2 (et Batch 3) doit **exiger** que le subagent ajoute des règles CSS explicites pour dimensionner les SVG injectés. Les conteneurs qui reçoivent des logos via placeholder doivent inclure :

```css
/* Exemple pour le showcase principal */
.logo-showcase__mark svg {
    width: 140px;   /* ajuster selon le contexte */
    height: auto;
}

/* Lockups */
.lockup-horizontal svg,
.lockup-stacked svg,
.lockup-icon svg {
    width: 60px;
    height: auto;
}

/* Variantes de contexte */
.variant-card svg {
    width: 100px;
    height: auto;
}

/* Safe area */
.safe-area-box svg {
    width: 100px;
    height: auto;
}
```

**Règle générale** : tout conteneur qui reçoit un `<!-- PLACEHOLDER:LOGO_* -->` DOIT avoir une règle CSS `{container} svg { width: Xpx; height: auto; }`.

### Fix B — Nettoyer les déclarations `<?xml?>` dans le script d'injection Python

Le script Python de post-traitement (dans SKILL.md, section Phase 6A) doit supprimer les déclarations XML avant injection :

```python
# Après lecture du SVG
svg = f.read().strip()
# Supprimer la déclaration XML (invalide en inline HTML5)
svg = svg.replace('<?xml version="1.0" encoding="UTF-8"?>', '').strip()
```

---

## Pourquoi ça marche

1. **`width` + `height: auto`** donne au SVG une taille intrinsèque explicite. Le `height: auto` préserve le ratio du viewBox. Le navigateur peut alors dimensionner le SVG correctement dans le conteneur flex.

2. **Suppression de `<?xml?>`** : en HTML5, le parser traite `<?...?>` comme un commentaire bogus (spec HTML5 §13.2.6.43). En le supprimant, le SVG est parsé comme du SVG inline standard, ce qui est le comportement attendu.

---

## Où corriger dans le système

| Fichier | Section | Action |
|---------|---------|--------|
| `SKILL.md` | Prompt subagent Phase 6A (Batch 2) | Ajouter une instruction : "tout conteneur recevant un PLACEHOLDER:LOGO_* DOIT avoir une règle CSS `{container} svg { width: Xpx; height: auto; }`" |
| `SKILL.md` | Prompt subagent Phase 6B (Batch 3) | Idem si des logos sont injectés |
| `SKILL.md` | Script Python post-traitement (Phase 6A) | Ajouter `svg = svg.replace('<?xml version="1.0" encoding="UTF-8"?>', '').strip()` après la lecture du fichier SVG |
| `SKILL.md` | Script Python post-traitement (Phase 6B) | Idem si un script d'injection existe |

---

## Checklist de vérification post-fix

Après correction du système, vérifier sur un test :

- [ ] Les logos sont visibles dans 05.1 (showcase principal, fond sombre)
- [ ] Les logos sont visibles dans 05.2 (lockups, 3 variantes côte à côte)
- [ ] Le logo est visible dans 05.3 (safe area, avec la zone d'exclusion en pointillés)
- [ ] Les 4 variantes sont visibles dans 05.4 (fond clair, fond sombre, monochrome, OLED)
- [ ] Aucun `<?xml` n'apparaît dans le HTML final (`grep "<?xml" fichier.html` retourne 0)
- [ ] Le logo conserve ses proportions (pas écrasé/étiré)
