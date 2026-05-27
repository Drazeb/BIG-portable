# Internal — logs de construction du projet

Ce dossier contient les **logs de construction** du projet BIG, exposés pour transparence.

**Vous n'avez pas besoin de lire ces fichiers pour utiliser le système.**

Ils sont utiles seulement si vous voulez :

- Comprendre **pourquoi** une décision d'architecture a été prise (et pas son alternative)
- Voir l'évolution du système session par session
- Reprendre un chantier passé ou éviter de refaire une erreur déjà identifiée

## Fichiers

| Fichier | Contenu |
|---|---|
| [`DECISIONS.md`](./DECISIONS.md) | Décisions structurantes chronologiques (D1, D2, ..., D57+) — chaque décision avec date, choix retenu, et le **pourquoi**. Le "pourquoi" est ce qui protège les choix passés contre une remise en question non informée. |
| [`BUILD-LOG.md`](./BUILD-LOG.md) | Historique narratif des sessions de travail, en français, regroupant les commits par thématique cohérente (plus lisible qu'un `git log`). |

## Format

Ces fichiers suivent un format **interne** plutôt qu'un standard public (pas de semver release notes type Keep-a-Changelog, pas de format ADR codifié type MADR). C'est volontaire : ils sont d'abord des outils de mémoire pour le mainteneur, et secondairement une ressource pédagogique pour les curieux.

Si vous voulez la version "user-facing" du projet, lisez plutôt :

- [`/README.md`](../../README.md) — Onboarding utilisateur
- [`/docs/ARCHITECTURE.md`](../ARCHITECTURE.md) — Carte technique vivante du pipeline
- [`/.claude/skills/brand-identity/ref/pipeline-overview.md`](../../.claude/skills/brand-identity/ref/pipeline-overview.md) — Vue d'ensemble du pipeline côté utilisateur (ouverte automatiquement à l'invocation du skill)
