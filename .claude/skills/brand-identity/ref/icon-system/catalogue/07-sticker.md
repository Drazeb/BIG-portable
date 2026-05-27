# 07 — Sticker / cut-out

## Nom canonique et alias
- **Nom canonique** : Sticker / cut-out
- **Alias usuels** : badge, peel-off sticker, paper-cut, drop-shadow sticker, achievement badge, swag pin
- **ID stable** : `07-sticker`

## Époque d'origine et revivals
- **Origine** : stickers physiques (skate, punk, dev conferences) → adaptation digitale fin 2010s
- **Pic mainstream** : 2020-2024 (Vercel, Linear, Substack badges, Discord nitro stickers)
- **Codes contemporains** : silhouette pleine + halo blanc + ombre douce derrière, look "découpé" assumé

## Traits formels
- **Stroke** : pas de stroke conventionnel, MAIS un contour blanc épais (4-8px) qui simule la coupe physique
- **Fill** : silhouette pleine d'une seule couleur saturée (rarement 2 couleurs)
- **Géométrie** : forme arrondie organique ou silhouette d'objet/animal/symbole simplifiée
- **Texture** : ombre portée diffuse derrière (signature)
- **Composition** : rotation légère (3-8°) pour casser l'orthogonalité (effet "collé à la main")

## Marques contemporaines qui l'emploient (2024-2026)
1. **Vercel** — achievements, conference swag (2024-2025)
2. **Linear** — release stickers, community badges (2024)
3. **Substack** — featured writer badges (2024-2025)
4. **Discord Nitro** — sticker packs (2024-2026)
5. **GitHub Achievements** — badges (2024-2025)

## Couleurs natives
- **Palette principale** : 1 couleur vive saturée par sticker (chaque sticker = sa propre couleur)
- **Contour blanc obligatoire** : signature physique du sticker découpé
- **Fond** : transparent (les stickers sont posés sur autre chose)
- **Mode sombre** : fonctionne mais sticker reste éclatant (ne s'adapte pas vraiment au dark)

## Formats natifs en stack Claude Code
- **SVG inline avec filter drop-shadow** : DOUBLE drop-shadow (blanc pour la découpe + flou sombre pour l'ombre portée)
- **Silhouette simple** : 1 path principal en aplat coloré
- **`filter: drop-shadow(0 3px 0 white) drop-shadow(0 4px 4px rgba(0,0,0,0.18))`** : recette signature
- **`transform: rotate(-3deg)` ou `rotate(5deg)`** : signature "collé à la main"

## Grain naturel (où la famille brille)
- Récompenses / achievements / accomplishments
- Marques avec une dimension communautaire forte (Discord, Twitch, GitHub)
- Marques de conférences / events / dev culture
- Badges de fonctionnalités, releases, milestones
- Marques fun / lifestyle / gaming / culture geek mainstream

## Compatibilités concept (tons)
- **Ludique** : excellent (signature native)
- **Communautaire** : excellent
- **Gaming / dev culture** : excellent
- **Récompense / accomplissement** : excellent
- **Tech-friendly accessible** : très bon
- **Casual / fun** : très bon
- **Sérieux / corporate** : faible (trop "fun")
- **Méthodique / rigoureux** : faible
- **Premium / luxe** : très faible (sticker = anti-luxe)
- **Patrimoine** : très faible
- **Cinématographique sombre** : faible (le sticker reste éclatant)

## Incompatibilités évidentes
- Marques B2B très sérieuses → trop léger
- Marques luxe → contradiction de codes
- Marques institutionnelles → trop "communautaire"
- Hero éditorial sombre → le sticker reste hors registre

## Sources datées
- Vercel Conf 2024 — swag et stickers digitaux
- Linear releases (2024-2025) — release stickers communautaires
- GitHub Achievements (2024-2025) — github.com/achievements
- Discord Sticker packs (2024-2026)
- Substack featured badges 2025
- *The Sticker Aesthetic: From Physical to Digital* — It's Nice That, juin 2024
