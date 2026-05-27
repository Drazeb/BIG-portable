# Brand Identity Generator (BIG)

> Pipeline Claude Code de génération d'identités de marque de classe mondiale, du brief stratégique aux livrables visuels.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

BIG est un système de skills Claude Code qui guide la création complète d'une identité de marque : stratégie, direction artistique, style-tiles HTML immersifs, système de signes, photographie, illustration, brand book éditorial. Deux modes au choix : **création** complète depuis un brief marketing, ou **aspiration** d'une marque existante depuis son site web.

## Quick start

```bash
# 1. Clone le repo (hors Google Drive recommandé)
git clone https://github.com/charlesbezard/BIG-portable.git ~/repos/BIG-portable

# 2. Ouvre Claude Code dans le dossier
cd ~/repos/BIG-portable
claude

# 3. Invoque le skill
/brand-identity
```

À l'invocation, une **Phase 0 Preflight Check** s'affiche : checklist cochable des dépendances installées sur ta machine + ce qui te manque (avec commande d'install pour chacune) + à quelles phases du pipeline elles servent. Tu peux choisir d'installer tout ou de skipper certaines phases.

## Prerequisites

### Indispensables (sinon le pipeline ne tourne pas du tout)

| Dépendance | Comment installer | Pourquoi |
|---|---|---|
| **macOS** | (déjà là) | Le système utilise `open`, `open -a Chrome` pour ouvrir les artefacts à valider |
| **[Claude Code](https://claude.ai/code)** | Via l'app Claude | Le skill tourne dedans |
| **Git** | `brew install git` | Pour cloner + recevoir les mises à jour (`git pull`) |
| **Node.js ≥ 18** | `brew install node` | Phase 3B-bis (specimens typo) + Phase 4 (screenshots Puppeteer) |
| **Python 3** | `brew install python` | Gates anti-slop mécaniques (Phase 4, Phase 6) |

### Optionnelles (chaque dep ne bloque qu'une partie du pipeline)

| Dépendance | Phases concernées | Skip si | Comment installer |
|---|---|---|---|
| **vtracer** (pip) | Phase Logo (vectorisation PNG → SVG) | Tu ne génères pas de logo | `pip3 install vtracer` |
| **Abo MidJourney** | Phase 3C visuels, Phase Logo | Tu n'utilises pas de visuels IA | [midjourney.com](https://www.midjourney.com) |
| **Abo Recraft** | Phase 3C illustrations flat | Tu restes en registre photo only | [recraft.ai](https://www.recraft.ai) |
| **Abo Perplexity Pro** | Phase 3B-7c (image-pivot stylistique) | Tu acceptes un pipeline sans image-pivot | [perplexity.ai/pro](https://www.perplexity.ai/pro) |
| **Abo Nano Banana 2** | Étapes d'édition d'images (Phase 3C, brand book) | Tu n'éditer pas les visuels post-MJ | [nanobanana.ai](https://nanobanana.ai) |
| **SPG-portable** (repo séparé) | Phase 8 — section pitch deck du brand book | Tu ne veux pas le brand book final | `git clone https://github.com/charlesbezard/SPG-portable.git ~/repos/SPG-portable` *(pas encore disponible — à venir)* |

La Phase 0 Preflight au lancement du skill détecte automatiquement ce qui est installé et te dit ce qui manque pour les phases que tu veux faire.

## Pipeline overview

Pour le détail des étapes (objectif, inputs, outputs, ce qu'on te demande), consulte [`pipeline-overview-public.md`](.claude/skills/brand-identity/ref/pipeline-overview-public.md). Ce fichier s'ouvre automatiquement à l'invocation du skill.

En résumé, le pipeline en mode création passe par 12 étapes :

1. Collecte du brief (4 options : brief existant, template, conversationnel, aspiration)
2. Analyse du brief + aversions client
3. Scoping — Tension de marque + curseurs A×B
4. Réconciliation de la tension
5. Pitch stratégique — 3 concepts narratifs (Génératif ou Sélectif par registre)
6. Design dérivé — palette, typographie, style officiel, penseur visuel, pitch complet
7. Visuels de référence (MidJourney / Recraft / Nano Banana 2)
8. Style-tiles HTML — 3 concepts en parallèle, 11 quality gates
9. Choix + itération + animation optionnelle
10. Logo (optionnel)
11. Système de signes — Batch 2 (logotype, iconographie, dataviz) + Batch 3 (photo, composition, illustration)
12. Packaging final + brand book éditorial (Phase 8)

## Architecture

La carte technique vivante du pipeline est dans [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — chaque brique est documentée à deux niveaux : vue rapide (input / output / règles) et "sous le capot" (exécution réelle, fichiers lus, mécanismes, pièges).

Pour le **pourquoi** des décisions structurantes, voir [`docs/internal/`](docs/internal/) (lore optionnel, exposé pour transparence).

## Skills inclus dans ce repo

| Skill | Invocation | Rôle |
|---|---|---|
| **brand-identity** | `/brand-identity` | Le pipeline principal de création d'identité (mode création 7 phases ou aspiration 5 phases) |
| **visual-brief** | `/visual-brief` | Génère les prompts visuels (MidJourney / Recraft / Nano Banana 2), analyse les images, prépare leur intégration. Invoqué en Phase 3C de BIG, ou seul. |
| **visual-prompt** | `/visual-prompt` | Workflow itératif MidJourney → Nano Banana 2 → Recraft pour produire des visuels IA de niveau Awards |
| **brand-book** | `/brand-book` | Génère un brand book HTML éditorial à partir d'un pack BIG (cover + intro Identity Card + 8 sections + closing). Invoqué automatiquement en Phase 8 de BIG, ou seul. |
| **test-big** | `/test-big` | Test runner pour reprendre le pipeline BIG à partir d'une phase spécifique (utile en debug ou si le pipeline a planté) |

L'écosystème complet inclut aussi `/audit-elite`, `/audit-slop` (audits qualité) et `/landing-page` (génération de landing pages) — disponibles dans des repos séparés ou versions futures.

## Reprendre un pipeline à mi-parcours

Si un pipeline a planté ou si tu veux reprendre à une phase précise sur la base d'une session existante (par exemple, recommencer le style-tile en Phase 4 sans refaire le brief et le scoping), lance `/test-big` au lieu de `/brand-identity`. Il te demandera quelle session reprendre et à quelle phase démarrer, et il copiera les artefacts nécessaires dans un nouveau dossier de session.

## Brand book final (Phase 8)

La dernière étape du pipeline produit un brand book HTML éditorial via le skill `/brand-book`. La section "Pitch Deck" de ce brand book nécessite le skill `generate-mini-deck` qui vit dans un repo séparé : `SPG-portable` (Slide Presentation Generator).

Si tu veux générer le brand book complet :

```bash
git clone https://github.com/charlesbezard/SPG-portable.git ~/repos/SPG-portable
```

*(SPG-portable n'est pas encore publié — il sera mis à disposition prochainement. La Phase 8 fonctionne sans : la section Pitch Deck est simplement omise.)*

## Mises à jour

Le projet évolue activement. Trois mécanismes pour rester à jour :

1. **GitHub Watch** — Clique sur "Watch" en haut du repo GitHub → tu reçois un email à chaque push significatif
2. **GitHub Releases** — Les versions majeures sont taggées comme releases avec un changelog narratif. Watcher les releases (option "Releases only") filtre les notifications
3. **Check auto in-skill** — La Phase 0 Preflight Check vérifie si ton repo local a du retard sur `origin/main`. Si oui, elle te demande de lancer `git pull` avant de continuer

Pour mettre à jour manuellement :

```bash
cd ~/repos/BIG-portable
git pull
```

Tes sessions de travail (dossier `.claude/skills/brand-identity/outputs/`) restent intactes — elles sont gitignorées et locales à ta machine.

## Contributing

Voir [`CONTRIBUTING.md`](CONTRIBUTING.md). Le projet est principalement maintenu par [Charles Bezard](https://github.com/charlesbezard). Pour signaler un bug ou proposer une amélioration, ouvre une [issue GitHub](../../issues) d'abord — on en discute avant de coder.

## License

[MIT](LICENSE) — utilisez, modifiez, distribuez librement, en gardant le copyright.
