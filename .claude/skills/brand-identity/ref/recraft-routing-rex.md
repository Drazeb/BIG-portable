# REX — Routage MJ vs Recraft V4 pour les registres illustratifs

## Problème

Le système BIG routait TOUS les visuels sauf I1/I2/I7 vers MidJourney. Sur le brief Camille (conseil stratégique premium, registre illustratif "sketch + surréalisme architectural", A=2 × B=3), les 9 images MJ produisaient systématiquement un rendu cinématique/photoréaliste au lieu d'illustratif :

- **A1 (Strates organiques, T2)** : MJ produit du marble stock photoréaliste. Le prompt demandait "painterly strata" → résultat = photo de roche.
- **A2 (Instruments, I5)** : MJ produit du steampunk cinématique avec éclairage dramatique. Le prompt demandait "stylized illustration" → résultat = photo de prop.
- **B2 (Observatoire, F4)** : MJ produit des grottes gothiques type concept art jeu vidéo. Trop sombre, trop cinématique pour du conseil stratégique premium.

**Diagnostic** : MJ a un biais fondamental vers le photoréalisme. Même avec `--style raw` et des mots-clés illustratifs, le modèle "tire" vers de la photo. Ce n'est pas un problème de prompting — c'est une limite du modèle pour les registres illustratifs.

## Ce qu'on a essayé (et pourquoi ça n'a pas marché)

- **Mots-clés illustratifs** (painterly, organic brushstrokes, hand-painted) → MJ les interprète comme filtres sur une base photoréaliste, pas comme un changement de registre
- **`--style raw`** → réduit l'esthétique "cinéma" mais ne passe pas en illustration
- **`--stylize` bas (50-150)** → résultat plus brut mais toujours photoréaliste

## Solution retenue

Routage 3-tier basé sur le registre du prompt :

| Tier | Registres | Outil | Raison |
|------|-----------|-------|--------|
| **Recraft systématique** | I1, I2, I4, I7, T2 | Recraft V4 Vector/Pro | Illustratif natif, pas de biais photoréaliste |
| **Dual (choix user)** | I3, I5, T3, F4 | Question à l'user | Dépend du rendu souhaité (illustratif vs cinématique) |
| **MJ systématique** | P1-P6, I6, T1, F1-F3 | MidJourney | Photo, personnages, seamless = forces MJ |

**Fichiers modifiés** :
- `SKILL.md` Phase 3C : table de routage + mécanisme question dual
- `ref/recraft-prompting-guide.md` : §1 élargi (5 Recraft + 4 Dual), nouveaux §5 pour I4/T2/Dual
- `ref/midjourney-prompting-guide.md` : marqueurs ⚠️ (Recraft par défaut) et 🔀 (Dual) dans l'arbre

**Mécanisme dual** : À l'écriture du prompt, l'orchestrateur pose la question :
> Image N — {description} (registre {code}, dual MJ/Recraft)
> A. Recraft — Rendu illustratif/stylisé
> B. MidJourney — Rendu cinématique/photoréaliste

## Pourquoi ça marche

Recraft V4 Pro a un "design taste" interne qui produit naturellement des rendus illustratifs/artisanaux — pas de biais photoréaliste. Sur les 3 comparaisons directes (A1/A2/A3 MJ vs Recraft) :

- **A1r** : strates organiques painterly → exactement le registre artisanal demandé
- **A2r** : instruments stylisés → illustration claire, pas du steampunk photo
- **A3r** : lignes analytiques + flux organiques → alignement parfait avec le brief "schéma de pensée"

Score Recraft 3-0 sur les registres illustratifs. MJ reste imbattable pour la photo et le cinématique.

## Données de test

Session Camille, mars 2026 :
- 9 prompts MJ (3 concepts × 3 images)
- 3 prompts Recraft V4 Pro (concept A uniquement, 3 images)
- Comparaison directe A vs A : Recraft systématiquement supérieur pour les registres I4/I5/T2
- L'écart est le plus flagrant sur T2 (texture abstraite) : MJ → marble stock, Recraft → strates painterly artisanales

---

## Addendum — Phase Logo : Recraft par défaut (mars 2026)

### Problème
Le routage initial classait L1-L6 (tous les registres logo) en "MJ systématique", basé sur un REX lettermark bicolore. Ce REX était correct pour les lettermarks complexes (split, negative space) mais a été sur-généralisé à TOUS les types de logos.

### Ce qu'on a observé (test Camille, mars 2026)
Sur 3 concepts F1 Soft Geometric (Point Focal, Corridor, Galets) testés en parallèle Recraft + MJ :

| Concept | Recraft | MJ | Gagnant |
|---------|---------|-----|---------|
| Point Focal (arcs) | Moyen (risque wifi) | FAIL (wifi/rainbow) | Recraft |
| Corridor (squircles) | BON (nets, géométriques) | DATÉ (blobs organiques 2015) | Recraft net |
| Galets (ellipses) | Correct (propres) | DATÉ (blobs amorphes friendly-startup) | Recraft |

**Diagnostic MJ** : MJ a un biais "organic blob" sur les formes abstraites. `--style raw` + `--no sharp corners` pousse les formes vers du mou/amorphe au lieu de doux/structuré. Le résultat ressemble au "friendly blob era" 2013-2018 (Slack, Asana, apps wellbeing) — pas au F1 Soft Geometric 2025 qui exige de la tension dans la douceur.

**Diagnostic Recraft** : V4 Vector maintient la rigueur géométrique. Un squircle reste un squircle (pas un coquillage). Les aplats sont nets, les proportions précises.

### Solution retenue
- **Phase Logo → Recraft V4 Vector par défaut**
- MJ disponible sur demande explicite de l'utilisateur
- L1-L6 retirés du tier "MJ systématique"
- Le prompt subagent Phase L1 lit maintenant le guide Recraft en priorité

### Apprentissage critique : framework = qualité
Le facteur n°1 de qualité des prompts logo (Recraft OU MJ) est le **respect strict du framework de prompting** :
- Recraft : les 7 couches (§4) doivent TOUTES être présentes. Un prompt sans Style ou sans Medium produit des résultats nettement inférieurs.
- MJ : les paramètres --v, --style, --s, --no doivent TOUS être spécifiés selon le registre.
- Gate d'auto-vérification ajoutée dans phase-logo-l1.md pour attraper les oublis.

*Dernière mise à jour : mars 2026*
