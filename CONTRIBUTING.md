# Contributing

Merci de l'intérêt que vous portez à ce projet.

## Statut du projet

Ce projet est principalement maintenu par [Charles Bezard](https://github.com/Drazeb). Il évolue activement et la roadmap est dirigée par les usages internes.

Les pull requests externes sont les bienvenues, mais merci d'ouvrir une issue de discussion **avant** d'investir du temps sur un changement non trivial — pour éviter les efforts perdus sur des directions qui ne s'aligneraient pas avec la trajectoire du projet.

## Signaler un bug

Ouvrez une [issue GitHub](../../issues) avec :

- Une description du comportement observé vs attendu
- La phase du pipeline concernée (ex: "Phase 3B-7c — penseur visuel")
- Le nom de marque et le label de session si applicable (`outputs/{brand}-{session}/`)
- Le contenu pertinent du fichier `.session-id` ou des logs `.progress-*.log`
- Votre environnement : macOS version, version de Claude Code, dépendances installées (résultat de la Phase 0 Preflight Check)

## Proposer une amélioration

1. Ouvrez d'abord une issue **"discussion"** décrivant l'idée et le problème qu'elle résout
2. Attendez un retour avant de coder — ça évite de réinventer ce qui existe déjà sous un autre nom, ou de partir dans une direction non alignée
3. Une fois validé, ouvrez la PR contre `main` avec :
   - Un commit message au format Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, etc.)
   - Une description claire du **pourquoi** plus que du **quoi**
   - Si la PR touche au pipeline (`SKILL.md`, `phases/`, `scripts/gates`), mettre à jour `docs/ARCHITECTURE.md` en conséquence
   - Si la PR ajoute une nouvelle décision structurante, en parler dans `docs/internal/DECISIONS.md`

## Style

- Code commenté en français OK, prompts subagents en français (c'est la langue du système)
- Les `SKILL.md` doivent rester concis — externaliser dans `phases/` ou `ref/` si > ~50 lignes par section
- Pas d'ajout de dépendances externes payantes sans discussion (MidJourney/Recraft/Perplexity sont déjà des points de friction)
- Respecter les patterns critiques du projet (`:root` sacré, session isolation, anti-contamination, placeholder protocol, screenshot test, Mason's Rule)

## Tests

Le projet n'a pas (encore) de suite de tests automatisés. Validation manuelle via le skill `/test-big` qui permet de relancer une phase précise sur une session existante. Avant de proposer une PR, faire tourner le pipeline complet sur au moins un brief de test (ex: utiliser un brief minimaliste type "marque de café artisanal").

## Convention d'anonymisation (mainteneur uniquement)

Ce repo public est synchronisé depuis un sandbox interne où les tests réels utilisent des marques clientes réelles. Pour ne jamais exposer ces clients, le script `scripts/export-to-portable.sh` applique une **anonymisation systématique** au moment du portage : toute marque cliente listée dans `CLIENT_ANONYMIZATIONS` (en tête du script) est remplacée par un pseudonyme dans tous les fichiers texte exposés.

Les pseudonymes actuellement utilisés (à titre indicatif pour comprendre les exemples dans la doc) :

| Pseudonyme | Registre / Contexte |
|---|---|
| **Atelier Vermeil** | Marque artisanale, atelier de transformation |
| **Camille** | Wordmark mono-mot, registre identitaire personnel |
| **VoltaPilot** | Mobilité électrique, B2B/B2C tech |

Si tu ajoutes un nouveau cas d'étude basé sur un client réel, ajoute le mapping dans `CLIENT_ANONYMIZATIONS` du script. Le script applique automatiquement 3 variantes de casse par mapping (Title Case, lowercase, UPPERCASE).

## Questions

Pour toute question qui ne rentre pas dans une issue, vous pouvez contacter le maintainer via le profil GitHub.
