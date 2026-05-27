# Benchmark Notes — 9 case studies de référence

Synthèse compacte des 9 case studies analysés pour calibrer la forme du brand book BIG. À consulter en cas de doute sur la forme d'une section. Ne pas refaire l'analyse à chaque marque.

---

## Tableau récapitulatif

Pour chaque case study : présence des éléments clés et archétype dominant.

Légende : **O** = présent / **—** = absent / **(o)** = présent mais minoritaire ou très accessoire.

| Case study | Archétype | Composants UI doc. | Dataviz | Mockup web | Mockup mobile | Palette immersive | Typo spécimen géant | Voice & Tone | Photo | Lifestyle photo | Mascot | Sidebar TOC sticky | Stats outcome | Quote testimonial | Bento grid | OOH | Papeterie | Particularité notable |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Matrix**     | Brand World classique     | —   | —   | O   | O   | O   | O   | (o) | O   | O   | —   | —   | —   | —   | (o) | O   | O   | Couverture-affiche peinture pivot, lourde papeterie corporate |
| **Solara**     | Brand World classique     | —   | —   | O   | O   | O   | O   | (o) | O   | (o) | —   | —   | —   | —   | —   | O   | O   | Palette immersive 1 couleur = 1 page (référence forte) |
| **Tags**       | Brand World classique     | (o) | —   | O   | O   | O   | O   | (o) | O   | O   | —   | —   | —   | —   | O   | O   | O   | Système de tags graphiques transverse cohérent |
| **Kurio**      | Digital Product Brand     | O   | O   | O   | O   | O   | O   | O   | (o) | —   | (o) | —   | O   | —   | O   | —   | —   | Documentation UI exhaustive (state matrix complet) |
| **HAXON**      | Digital Product Brand     | O   | O   | O   | (o) | O   | O   | O   | (o) | —   | —   | —   | O   | —   | O   | —   | —   | Dashboard data-heavy + ton très technique |
| **Agenie**     | Digital Product Brand     | O   | O   | O   | O   | O   | O   | O   | (o) | —   | —   | —   | O   | —   | O   | —   | —   | Palette immersive Solara-like adaptée au produit |
| **Guardbase**  | Digital Product Brand     | O   | O   | O   | O   | O   | O   | O   | —   | —   | —   | —   | O   | (o) | O   | —   | —   | Iconographie sécurité très typée, état dark canonique |
| **Yazio**      | Editorial Case Study Koto | (o) | (o) | O   | O   | O   | O   | O   | (o) | O   | O   | O   | O   | O   | (o) | —   | —   | Sidebar TOC sticky + character mascot + storytelling fort |
| **MachineX**   | Editorial Case Study Koto | (o) | (o) | O   | (o) | O   | O   | O   | O   | (o) | O   | O   | O   | O   | (o) | —   | —   | Long-scroll narratif Koto, character mascot, voice forte |

---

## Lecture par archétype

### 1. Brand World classique (Matrix · Solara · Tags)
- Focus : **mockup physique** (papeterie, OOH, packaging), **photographie produit** soignée.
- Cover : peinture pivot pleine page, statement-poster fort.
- Faible documentation UI (pas un produit digital, ou produit secondaire).
- Voice & Tone : présent mais accessoire — pas le cœur.
- Pertinent pour : marques B2C lifestyle, produits physiques, hospitality.

### 2. Digital Product Brand (Kurio · HAXON · Agenie · Guardbase)
- Focus : **dashboard mockup web**, **composants UI documentés** (state matrix complet : default/hover/focus/disabled/error), **dataviz canonique**.
- Stats outcome systématiquement présentes (chiffres business du redesign).
- Mockup mobile fréquent mais pas systématique (dépend de l'ICP).
- Mascot, lifestyle photo, OOH, papeterie : généralement absents.
- Voice & Tone : présent mais accessoire.
- Pertinent pour : SaaS, fintech, dev-tools, produits B2B digitaux.

### 3. Editorial Case Study Koto (Yazio · MachineX)
- Focus : **storytelling éditorial long-scroll**, **sidebar TOC sticky**, **character mascot** (illustration narrative), **voice & tone forte**, **quote testimonial**.
- Stats outcome présentes (mais traitées en éditorial, pas en dashboard).
- Documentation UI minoritaire (présente mais pas exhaustive).
- Voice & Tone très développée (descriptors + Do/Don't + tone-shifts par contexte).
- Pertinent pour : marques avec un récit fort (food, wellbeing, edtech, media).

---

## 3 conclusions actionnables pour le brand book BIG

### Conclusion 1 — On vise un mix "Digital Product Brand + touches Koto"
Le brand book BIG cible **majoritairement Digital Product Brand** (composants UI documentés, dataviz canonique, mockup web via capture style-tile) **avec des touches Editorial Case Study Koto** (Big Idea / Concept éditorial minimaliste, Voice & Tone développée avec pull-quote + descriptors + Do/Don't, cover peinture pivot painterly).

C'est la combinaison qui correspond aux marques que BIG produit aujourd'hui : majorité SaaS / produit digital, avec un récit BIG suffisamment fort pour mériter un éditorial.

### Conclusion 2 — Mockup mobile = optionnel
Le mockup mobile n'est inclus **que si l'ICP de la marque est explicitement une app mobile** (ex: app B2C). Pour tous les autres cas (B2B SaaS, dashboard, web app desktop), on **skip le mockup mobile**.

Raison : un mockup mobile générique sur fond gradient = cliché Dribbble. Mieux vaut pas de mockup mobile qu'un mockup mobile générique.

### Conclusion 3 — Skip systématique : stats outcome, lifestyle photo, mascot, sidebar TOC sticky
- **Stats outcome** : BIG ne dispose pas de données réelles post-redesign (le brand book est généré au moment de la création de la marque). Skip.
- **Lifestyle photo** : nécessite un shooting photo réel ou une banque d'images dédiée. Hors capacité BIG. Skip.
- **Character mascot** : nécessite un travail d'illustration narrative dédié, hors pipeline. Skip sauf si la marque a explicitement défini une mascotte en Phase 3B/3C.
- **Sidebar TOC sticky** : ajoute une complexité de layout (gestion du scroll, responsive) qui n'apporte pas grand-chose sur un document de ~21000px. Le sommaire en haut (non sticky) suffit pour la v1. À reconsidérer en v2 si feedback utilisateur.

---

## Quand consulter ce benchmark ?

- **Doute sur la forme d'une section** : "Est-ce que je mets un mockup mobile pour VoltaPilot ?" → relire conclusion 2.
- **Doute sur la profondeur de documentation UI** : "Est-ce que je fais une state matrix complète ?" → archétype Digital Product Brand = oui (Kurio en référence).
- **Doute sur l'éditorial** : "Est-ce que la pull-quote section 06 doit être très grande ?" → archétype Koto = oui (MachineX en référence).
- **Doute sur la cover** : "Statement-poster ou peinture pivot ?" → toujours peinture pivot (Brand World + Koto convergent là-dessus). Pas de statement-poster.
