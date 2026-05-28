# Brand Identity Generator (BIG)

> Pipeline Claude Code de génération d'identités de marque de classe mondiale, du brief stratégique aux livrables visuels.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

BIG est un système de skills Claude Code qui guide la création complète d'une identité de marque : stratégie, direction artistique, style-tiles HTML immersifs, système de signes, photographie, illustration, brand book éditorial. Deux modes au choix : **création** complète depuis un brief marketing, ou **aspiration** d'une marque existante depuis son site web.

## Quick start

```bash
# 1. Clone ce repo où tu veux (n'importe quel dossier)
git clone https://github.com/Drazeb/BIG-portable.git ~/Documents/Claude\ Code/BIG-portable

# 2. Lance le script d'install (il clone les 2 repos compagnons côte à côte)
cd ~/Documents/Claude\ Code/BIG-portable
./install.sh

# 3. Ouvre Claude Code dans ce dossier et tape /brand-identity
```

Le script `install.sh` clone automatiquement `SPG-portable` et `nano-banana-edit-portable` côte à côte avec BIG-portable. Tu n'as **rien d'autre à configurer pour démarrer**.

À l'invocation, une **Phase 0 Preflight Check** vérifie ton environnement et démarre le pipeline. **Les dépendances optionnelles (clé Gemini, vtracer, abonnements MJ/Recraft/Perplexity) sont demandées au moment où elles sont nécessaires**, pas au démarrage. Tu peux explorer la Phase 1 à 5 (analyse brief → style-tile) **sans configurer aucune clé API**.

## Prerequisites

Seules ces 5 dépendances sont nécessaires pour démarrer. Tout le reste est demandé en cours de pipeline.

| Dépendance | Comment installer |
|---|---|
| **macOS** | (déjà là) |
| **[Claude Code](https://claude.ai/code)** | Via l'app Claude |
| **Git** | `brew install git` |
| **Node.js ≥ 18** | `brew install node` |
| **Python 3** | `brew install python` |

**Dépendances optionnelles** (demandées juste-à-temps, quand tu arrives à la phase qui en a besoin) :

- **vtracer** (Phase Logo) — installation rapide via `pip3 install vtracer` au moment de la Phase Logo
- **Clé API Gemini** (Phase 3B-7c visuel hero + variantes d'atmosphère) — obtenir une clé gratuite sur [Google AI Studio](https://aistudio.google.com/app/apikey), je te guide quand tu en as besoin
- **Abos payants** : [MidJourney](https://www.midjourney.com) (visuels), [Recraft](https://www.recraft.ai) (illustrations flat), [Perplexity Pro](https://www.perplexity.ai/pro) (image-pivot)
- **SPG-portable** (brand book final) — déjà cloné automatiquement par `install.sh`

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
| **visual-prompt** | `/visual-prompt` | Workflow itératif MidJourney → Nano Banana 2 → Recraft pour produire des visuels IA de niveau Awards. **2 modes** : (1) hero principal depuis un rapport Perplexity, (2) variantes (atmosphere/closeup/macro/pov) dérivées d'un hero existant, en s'appuyant sur le framework librairie atmosphère du nb-prompting-guide. Invoqué en Phase 3B-7c et 3B-7e de BIG. **Dépend de [nano-banana-edit-portable](https://github.com/Drazeb/nano-banana-edit-portable) (repo séparé, à cloner côte à côte) pour les corrections NB2.** |
| **brand-book** | `/brand-book` | Génère un brand book HTML éditorial à partir d'un pack BIG (cover + intro Identity Card + 8 sections + closing). Invoqué automatiquement en Phase 8 de BIG, ou seul. |
| **test-big** | `/test-big` | Test runner pour reprendre le pipeline BIG à partir d'une phase spécifique (utile en debug ou si le pipeline a planté) |

L'écosystème complet inclut aussi `/audit-elite`, `/audit-slop` (audits qualité) et `/landing-page` (génération de landing pages) — disponibles dans des repos séparés ou versions futures.

## Reprendre un pipeline à mi-parcours

Si un pipeline a planté ou si tu veux reprendre à une phase précise sur la base d'une session existante (par exemple, recommencer le style-tile en Phase 4 sans refaire le brief et le scoping), lance `/test-big` au lieu de `/brand-identity`. Il te demandera quelle session reprendre et à quelle phase démarrer, et il copiera les artefacts nécessaires dans un nouveau dossier de session.

## Brand book final (Phase 8)

La dernière étape du pipeline produit un brand book HTML éditorial via le skill `/brand-book`. La section "Pitch Deck" de ce brand book nécessite le skill `generate-mini-deck` qui vit dans un repo séparé : `SPG-portable` (Slide Presentation Generator).

Si tu veux générer le brand book complet :

```bash
git clone https://github.com/Drazeb/SPG-portable.git ~/repos/SPG-portable
```

La Phase 8 fonctionne aussi sans SPG-portable : la section Pitch Deck du brand book est simplement omise.

## Mises à jour

Le projet évolue activement. Pour récupérer les dernières améliorations sur les 3 repos d'un coup :

```bash
cd ~/Documents/Claude\ Code/BIG-portable
./update.sh
```

Le script `update.sh` lance `git pull` dans BIG-portable + SPG-portable + nano-banana-edit-portable et te donne un récap. Tes sessions de travail (`outputs/`) et ton fichier `.env` (avec ta clé Gemini) restent intacts — ils sont gitignorés et locaux à ta machine.

**Mécanismes complémentaires** :

1. **GitHub Watch** — Clique sur "Watch" en haut du repo GitHub → tu reçois un email à chaque push
2. **GitHub Releases** — Les versions majeures sont taggées avec un changelog narratif
3. **Check auto in-skill** — La Phase 0 Preflight vérifie si ton repo local a du retard sur GitHub et te prévient au démarrage de chaque session

## Contributing

Voir [`CONTRIBUTING.md`](CONTRIBUTING.md). Pour signaler un bug ou proposer une amélioration, ouvre une [issue GitHub](../../issues) d'abord — on en discute avant de coder.

## License

[MIT](LICENSE) — utilisez, modifiez, distribuez librement, en gardant le copyright.

## Maintainer

Created and maintained by [Charles Bezard](https://github.com/Drazeb).
Built with [Claude Code](https://claude.ai/code).
