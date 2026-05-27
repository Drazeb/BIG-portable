# Guide de formulation anti-slop

Comment rédiger une règle anti-slop sans contaminer la génération créative du LLM.

## Le problème

Quand une règle est formulée avec un exemple concret (hex précis, font nommée, syntaxe CSS complète, variable custom), le LLM peut l'utiliser comme inspiration créative au lieu de l'éviter. Pattern anti-contamination documenté dans D4 pour les exemples visuels — étendu ici à la **rédaction des règles elles-mêmes**.

Exemple : `Do NOT use purple/blue gradient #6366f1 → #a855f7` peut être lu par le LLM comme "ces teintes existent, je peux jouer autour".

## Les 3 niveaux

### Niveau 1 — Principe abstrait (prompt OK)
Formulation qui ne peut pas servir de template visuel.
- OK : `Do NOT center everything symmetrically`
- OK : `Do NOT use infinite decorative animations`
- OK : `Sections should have varying vertical rhythm`

### Niveau 2 — Pattern nommé non-substituable (prompt OK)
Nomme un pattern reconnu — pas de valeur ni syntaxe exploitable.
- OK : `Do NOT use wave/zigzag dividers`
- OK : `Do NOT use manual staggered fade-up entries`
- OK : `Do NOT use neumorphism`
- OK : `Do NOT use glow shadows without directional offset`

### Niveau 3 — Énumération précise (gate Python UNIQUEMENT)
Fonts par nom, hex précis, syntax CSS complète, custom properties nommées. **Ne vit QUE dans le code Python**.
- Non prompt : `Do NOT use Inter, Roboto, Open Sans`
- Oui code : `scripts/phase4-blacklist-gate.py` `check_banned_fonts()` regex
- Non prompt : `Do NOT use --angle: 0deg → 360deg infinite`
- Oui reformuler Niveau 2 : `Do NOT use infinite rotation on gradients`

## Cas spécial — Listes nominatives nécessaires

Quand le LLM doit être orienté hors d'une famille précise (fonts training-defaults, icon libs par défaut, placeholder sources), deux outils :

1. **Gate Python** (Niveau 3) — détecte au runtime, bloque avant livraison.
2. **Procédure dans le prompt** (Niveau 1) — oriente vers la découverte, sans énumérer.

Exemple pour les fonts : le prompt renvoie vers `font-matching-rules.md` (méthode de matching) et `font-pools/` (pools autorisés par registre). La liste des fonts bannies vit uniquement dans le gate Python.

Le prompt montre le PROCESSUS, pas la liste. La liste vit dans le code.

## Clause "anti-cousin"

Pour les règles à risque de substitution proche (LLM banni d'Inter → choisit Roboto, banni de hero centré → choisit hero symétrique), ajouter :
```
Avoid X and its visual cousins (Y-style elements from the Z era monoculture).
```
Exemple : `Avoid centered hero CTA-only and its cousins (startup landing page templates 2015-2020).`

## Check avant d'ajouter une règle

1. La règle peut-elle se lire comme un exemple à suivre ? Si oui → reformuler Niveau 1.
2. Contient-elle une valeur exploitable (hex, px, font, class, custom property nommée) ? Si oui → déplacer au gate Python.
3. A-t-elle un cousin évident de substitution ? Si oui → ajouter clause "anti-cousin".

Règle d'or : si tu hésites entre Niveau 2 et Niveau 3 → Niveau 3 (gate Python). Le prompt reste propre.

## Dernière mise à jour

2026-04-24 — Création. Validé avec Charles suite à l'audit contamination sur les sources Vercel, Impeccable, GStack, Taste Skill.
