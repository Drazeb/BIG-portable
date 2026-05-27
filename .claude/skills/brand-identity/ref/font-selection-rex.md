# REX — Sélection typographique visuelle (Phase 3B)

## Session du 17-18 mars 2026

---

## Problème initial

Le système de sélection typographique par planches visuelles (D43) souffrait de plusieurs biais :
1. **Biais de primauté** : Bodoni Moda (#01) choisie 5/12 fois, y compris pour un concept agraire incompatible
2. **Hallucination de noms** : le subagent écrivait des noms de fonts malgré l'anonymisation (ex: "#21 = Cormorant" alors que #21 = Chivo)
3. **Rationalisation post-hoc** : le scoring 7/7 justifiait n'importe quel choix après coup

## Ce qu'on a essayé (et les résultats)

### Architecture : 1 subagent monolithique → 3 subagents parallèles
- **Résultat** : amélioration de la qualité par concept (plus d'attention), mais n'a pas résolu le biais typo
- **Statut** : implémenté, fonctionne bien

### Fusion Passe 1 + 2 (contexte complet + planches dès le départ)
- **Hypothèse** : le biais venait de l'absence de cerveau DA en Passe 1
- **Résultat** : diversité des catégories améliorée (serif + sans au lieu de 3 serifs), mais biais de primauté persistant
- **Statut** : implémenté, partiellement efficace

### Shortlisteur + Designer (2 subagents)
- **Hypothèse** : séparer exploration et choix final
- **Résultat** : le shortlisteur mettait #01 dans toutes ses shortlists, le designer la choisissait
- **Statut** : implémenté, pas suffisant seul

### Gate numéros uniquement
- **Hypothèse** : empêcher l'hallucination de noms
- **Résultat** : les shortlists sont en numéros, les pitchs écrivent encore des noms. Gate souvent sautée par l'orchestrateur
- **Statut** : implémenté, compliance partielle

### Scoring des 7 candidates
- **Hypothèse** : forcer la comparaison
- **Résultat** : le scoring est du post-hoc — le subagent met 7/7 à son choix préféré et rationalise
- **Statut** : implémenté, efficacité douteuse

### Planches de différentes tailles
Tests empiriques de catégorisation (même pool, tailles différentes) :

| Format | Score catégorisation | Biais primauté | Round-robin | Perception DECO |
|---|---|---|---|---|
| 50 fonts, 1 planche | ~10% | Très fort | Non | Très mauvaise |
| 25 fonts, 1 planche | ~20% | Fort | Non | Mauvaise |
| 10 fonts, 5 planches | ~85% correct (personnalité) | Faible | Non | Erreurs sur DECO (#33, #42) |
| 3 fonts, 17 planches | ~84% correct | Faible | **OUI (round-robin)** | Bonne |
| 2 fonts, 25 planches | ~92% correct | Aucun | Non testé en shortlist | Bonne |
| 1 font, 25 images | ~92% correct | Aucun | N/A | Bonne |

### Tags de catégorie sur les planches
- Tags SERIF/SANS/DECO/PIXEL → élimine les confusions serif↔sans
- Tags enrichis DECO-3D/DECO-OUTLINE/DECO-GLITCH → aide mais ne suffit pas, le subagent shortliste quand même des DECO en croyant voir des slabs
- Tags MONO/PROP pour les body → résout la confusion mono↔proportionnel (vérifié : le LLM ne peut PAS distinguer visuellement mono de prop)

### Consigne anti-round-robin
- "Choisis les 7 meilleures GLOBALEMENT — pas une par planche"
- **Résultat** : ignorée. Le round-robin est structurel avec les planches séquentielles
- **Statut** : inefficace

### Inventaire préalable (catégorisation des 50 avant shortlist)
- **Résultat** : élimine le biais Bodoni (0/3 au lieu de 5/12) mais les catégorisations sont massivement fausses → les choix qui en découlent sont basés sur des perceptions erronées
- **Statut** : abandonné

## Découvertes clés

### 1. Le LLM ne fait pas de vraie comparaison visuelle
Sur une planche de N fonts, il trouve la première acceptable et s'arrête. Il ne compare jamais les N entre elles. Le scoring est de la rationalisation post-hoc.

### 2. La résolution est critique
- 50 fonts sur 1 image : illisible (empattements à 1-2 pixels)
- 10 fonts sur 1 image : lisible pour la personnalité, mais les effets subtils (3D, outline) ne sont pas vus
- 3 fonts sur 1 image : tout est vu, mais crée le biais round-robin

### 3. Mono vs proportionnel est invisible visuellement
Sur 30 monospaces testées, le LLM n'en identifie que 3-5 visuellement. La chasse fixe est un détail trop subtil. Tags MONO/PROP obligatoires.

### 4. Le jugement de personnalité fonctionne
Vérifié par l'utilisateur : les descriptions de style/personnalité/poids/énergie sont correctes et pertinentes, même sur des planches de 10. Le problème n'est pas dans la perception de la personnalité — c'est dans le croisement personnalité × concept.

### 5. Le biais de primauté n'est PAS toujours un biais
Test avec concept festival électronique (A=3 × B=3) : Bodoni #01 n'est PAS shortlistée. Le LLM discrimine correctement quand le concept est clairement incompatible. Bodoni sort pour les concepts Camille parce que les territoires ("chirurgicale", "précision") créent un lien réel avec le haut contraste didone.

### 6. Le round-robin est structurel avec des planches séquentielles
Quand le LLM voit les planches une par une, il traite chaque planche comme un mini-choix local. La consigne "choisis globalement" ne change pas ce comportement.

## Meilleur compromis trouvé

**Planches de 10 avec tags enrichis + consigne anti-round-robin** :
- Pas de round-robin (distribution irrégulière confirmée)
- Pas de Bodoni automatique (0/1 sur le test Sillon)
- Erreurs résiduelles sur DECO (#33, #37 shortlistées malgré tags) → le designer sur mini-planche les écartera
- Ratio qualité/tokens optimal (5 planches au lieu de 17 ou 25)

## Problème non résolu

Le subagent fait des choix **corrects mais pas optimaux**. Sur 7 shortlistées : 1 très bon, 3 bons, 1 moyen, 2 discutables. Le meilleur choix du pool (#02 Abril Fatface pour le Sillon) n'est JAMAIS shortlisté dans aucun test.

**Hypothèse** : le subagent manque de la capacité de croisement fin entre personnalité visuelle et registre conceptuel. Il voit les fonts correctement, il comprend le concept, mais le matching est approximatif.

**Pistes à explorer (prochaine session)** :
1. **Approche par élimination** : au lieu de "shortliste 7", demander "élimine les incompatibles". Force un jugement binaire par font.
2. **Anti-patterns typographiques** : formaliser des règles de croisement concept × font (ex: "concept terreux → pas de didone capillaire, chercher slab/bold/dense")
3. **Feedback loop simulé** : montrer des exemples de bons et mauvais matchs concept × font avant la sélection

## Fichiers de test produits (dans outputs/test-camille-test-20260317-2218/)

- `test-shortlist-sillon.md` — planches de 3, sans tags (ancien système)
- `test-shortlist-chromatogramme.md` — idem
- `test-shortlist-route.md` — idem
- `test-shortlist-sillon-split.md` — planches de 2 (split)
- `test-shortlist-festival.md` — concept anti-Bodoni, planches de 10
- `test-shortlist-sillon-ten.md` — planches de 10, tags simples
- `test-shortlist-sillon-trio.md` — planches de 3, tags simples (round-robin détecté)
- `test-shortlist-sillon-2pass.md` — planches de 3, 2 passes (round-robin persistant)
- `test-shortlist-sillon-ten-v2.md` — planches de 10, tags enrichis (meilleur résultat)
