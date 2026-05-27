# Catalogue des 8 familles d'icônes — Index

**Pool décontaminé** : 8 familles graphiques cohérentes avec un pipeline d'identité de marque, **toutes faisables en SVG/CSS pur en stack Claude Code**.

**Disqualifiées du pool** (raisons techniques) :
- Glyphe typographique custom (nécessite une fonte commandée)
- Hand-drawn / sketchy (nécessite Rough.js ou assets dessinés à la main — `feTurbulence` SVG est un cache-misère, pas du vrai hand-drawn)

---

## Tableau récapitulatif

| ID | Famille | Époque/Origine | Grain naturel | Cas d'usage typique | Tons |
|---|---|---|---|---|---|
| `01-pictogramme-geo` | Pictogramme géométrique propre | 2010s, Heroicons/Phosphor/Lucide | UI dense, doc technique | SaaS, dashboards, design systems neutres | Sérieux fonctionnel |
| `02-isometrique` | Isométrique / 3D | 2010s revival, Stripe-like + Streamline 3D | Hero éditorial, conceptuel | Marques "système", "infrastructure", "construction" | Sérieux, parfois ludique |
| `03-pixel` | Pixel art | 1980s revival, jeu vidéo + dev tools | UI dense, micro-icônes, signature | Marques tech-retro, gaming, dev outils, contre-culture | Brut, geek, retro |
| `04-gravure` | Gravure / linocut | 19e siècle revival, illustration éditoriale | Hero, illustration éditoriale | Marques artisanales, éditoriales, savoir-faire, patrimoine | Sérieux, premium, ancré |
| `05-ornemental` | Ornemental (art déco / nouveau / blason) | 1920-1930s revival, Pentagram, COLLINS | Hero, héritage, cérémonial | Marques luxe, héritage, hôtellerie, spiritueux | Cérémonial, premium |
| `06-flat-illustre` | Flat illustré coloré | 2014-2024 mainstream, Notion/Slack/Stripe | Hero, spot illustration | Marques SaaS chaleureuses, B2C friendly, fintech | Chaleureux, accessible |
| `07-sticker` | Sticker / cut-out | 2018+ contemporary, Linear/Vercel/Substack | Micro-récompenses, badges | Marques fun, communauté, lifestyle, gaming | Ludique, communautaire |
| `08-brutaliste` | Brutaliste / ASCII | 2020+ counter-trend, Mike Mai/Bobby Berry | Signature graphique forte | Marques tech-pointues, contre-culture, indie | Brut, anti-corporate |

---

## Format des fiches catalogue

Chaque fiche `0X-{famille}.md` suit la **même structure H2** pour permettre comparaison côte-à-côte par le router :

1. **Nom canonique + alias** (comment les designers l'appellent)
2. **Époque d'origine et revivals**
3. **Traits formels** (stroke, fill, géométrie, texture)
4. **Marques contemporaines** (3-5, avec date 2024-2026)
5. **Couleurs natives**
6. **Formats natifs en stack Claude Code** (SVG plat / multicouche / CSS+pseudo / image)
7. **Grain naturel** (où la famille brille naturellement)
8. **Compatibilités concept** (tons : sérieux/ludique/lux/brut)
9. **Incompatibilités évidentes**
10. **Sources datées**

---

## État de remplissage

| ID | Statut |
|---|---|
| `01-pictogramme-geo` | Rempli (Sprint 2) |
| `02-isometrique` | Rempli (Sprint 2) |
| `03-pixel` | Rempli (Sprint 2) |
| `04-gravure` | Rempli (Sprint 1) |
| `05-ornemental` | Rempli (Sprint 2) |
| `06-flat-illustre` | Rempli (Sprint 1) |
| `07-sticker` | Rempli (Sprint 2) |
| `08-brutaliste` | Rempli (Sprint 2) |

**Pool complet** : les 8 familles sont documentées (catalogue + slop sheet + 2-3 spécimens). Le router peut désormais opérer sur le pool complet randomisé.
