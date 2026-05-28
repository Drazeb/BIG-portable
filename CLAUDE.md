# Brand Identity Generator (BIG) — Instructions Claude Code

## Projet

Système de génération d'identités de marque de classe mondiale, en pipeline Claude Code. Deux modes : création complète à partir d'un brief marketing, ou aspiration d'une marque existante depuis son site web. Produit des style-tiles HTML, systèmes de signes, brand book éditorial, et documentation technique.

Le skill principal s'invoque avec `/brand-identity`. Pour reprendre un pipeline à mi-parcours : `/test-big`.

## Structure du repo

```
BIG-portable/
├── README.md                 ← Onboarding et installation
├── LICENSE                   ← MIT
├── CONTRIBUTING.md           ← Comment signaler bug / proposer
├── CLAUDE.md                 ← Ce fichier (instructions pour Claude Code)
├── docs/
│   ├── ARCHITECTURE.md       ← Carte technique vivante du pipeline
│   └── internal/             ← Lore optionnel (DECISIONS, BUILD-LOG)
├── guides/                   ← Guides pratiques (brief-guide, prompt-perplexity-logo)
└── .claude/skills/
    ├── brand-identity/       ← Pipeline principal (~2200 lignes SKILL.md)
    │   ├── SKILL.md          ← Orchestrateur
    │   ├── phases/           ← Prompts subagents externalisés
    │   ├── ref/              ← Fichiers de référence (bible, specs, REX)
    │   ├── examples/         ← Exemples de qualité (standard/ + rupture/)
    │   ├── scripts/          ← Gates Python (anti-slop, blacklist, finishing)
    │   └── lib/              ← Libs Node (puppeteer, font specimens, palette)
    ├── visual-prompt/        ← Workflow itératif MJ→NB2→Recraft
    ├── brand-book/           ← Phase 8 — brand book HTML éditorial
    └── test-big/             ← Reprise du pipeline à mi-parcours
```

## Patterns techniques critiques

À respecter dans toute modification du pipeline :

- **`:root` sacré** : 40-60 CSS custom properties, 7 catégories (palette, typo, type-scale, spacing, radius, shadows, transitions). Jamais modifié après validation Phase 5.
- **Session isolation** : `outputs/{brand}-{session}/` + fichier `.session-id`. Vérifié avant chaque subagent.
- **Anti-contamination** : Les exemples montrent la QUALITÉ attendue, pas la direction créative. Le prompt liste explicitement ce qu'il est interdit de copier.
- **Subagent pattern** : 1 subagent (Task tool, general-purpose) par phase, resumable via agentId pour itération.
- **Anti-`/tmp/`** : JAMAIS utiliser `/tmp/`. Toujours `{session_dir}/.tmp-*` pour isoler la session.
- **Placeholder protocol** : `<!-- PLACEHOLDER:X -->` pour assets > 25K tokens, injection Python post-traitement.
- **Mason's Rule** : Zéro scaffolding visible (pas de "Section 02", labels, nuanciers décoratifs). Le showroom = vrai site de marque, pas documentation.
- **Screenshot Test** : "Cet élément serait-il visible sur un screenshot du site en production ?" Filtre les données techniques hors des HTML showroom.

## Conventions de code

- **Commit messages** : Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, `perf:`, `test:`)
- **Langue** : prompts subagents en français, commentaires de code en français OK, mais les noms de variables et identifiants en anglais
- **`SKILL.md`** : reste concis — externaliser dans `phases/` ou `ref/` si une section dépasse ~50 lignes
- **Pas de nouvelles dépendances externes payantes** sans discussion préalable

## Documentation à maintenir

À chaque modification structurelle du pipeline :

- **`docs/ARCHITECTURE.md`** : carte technique vivante. À mettre à jour si une brique change de squelette ou de mécanique (pas pour un bug fix interne).
- **`.claude/skills/brand-identity/ref/pipeline-overview-public.md`** : vue d'ensemble user-facing. Régénérée automatiquement au pre-commit depuis la version interne du sandbox (voir système de pre-commit hook côté maintainer).
- **`docs/internal/DECISIONS.md`** : log des décisions structurantes (D1, D2, ...) avec dates et "pourquoi". Le "pourquoi" protège contre la défaite involontaire d'un choix passé.

## Outils externes du pipeline

Le pipeline invoque (à différentes phases) :

- **MidJourney** (web) — génération d'images photoréalistes, illustrations, logos. Workflow copy-paste : Claude Code génère le prompt, l'utilisateur lance dans MJ, télécharge l'image, et revient
- **Recraft V4** (web) — illustrations flat, line art, infographiques. Idem MJ.
- **Nano Banana 2** (web) — édition d'images, retouches localisées
- **Perplexity Pro** (web) — recherche stylistique pour image-pivot (Phase 3B-7c)
- **vtracer** (CLI Python) — vectorisation PNG → SVG pour logos
- **Puppeteer** (auto-installé) — screenshots de validation visuelle

Tous les outils web sont en workflow manuel (copy-paste de prompt → user lance dans le service → revient avec le résultat). Pas d'API call automatisé.

## Permissions Claude Code recommandées

Pour fluidifier l'exécution, autoriser ces patterns dans les permissions de Claude Code :

- Bash : `git`, `python3`, `node`, `npm`, `npx`, `open`, `mkdir`, `cp`, `rsync`, `pip3`
- Read/Write/Edit : tout le repo

## Setup initial pour un nouveau user

Lorsque tu invoques le skill `/brand-identity` pour la première fois, la **Phase 0 Preflight Check** affiche une checklist cochable des dépendances installées sur la machine. Suis ses instructions — elle te dit ce qui manque, comment l'installer, et à quelles phases du pipeline chaque dep sert. Tu peux choisir de tout installer, ou de skipper certaines phases si tu n'as pas besoin (ex: pas de logo → pas besoin de vtracer).

Pour un démarrage rapide complet, voir [`README.md`](README.md).
