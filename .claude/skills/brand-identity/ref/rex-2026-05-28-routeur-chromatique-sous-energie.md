# REX — Le routeur chromatique sous-livre l'énergie quand le brief la demande

**Date** : 2026-05-28
**Session source** : `les-vermeil-premium-militant`
**Auteur** : remonté par Charles en cours de pipeline (Phase 3B-0), confirmé par auto-critique du routeur.
**Statut** : problème systémique confirmé — à corriger dans les prompts/gates, pas seulement dans cette session.
**Sévérité** : élevée. Produit des identités à côté du brief sur l'axe le plus visible (la couleur).

---

## TL;DR

Pour une marque dont le brief demande explicitement **chaleur, vie, optimisme** (territoire SECONDAIRE "Chaleur Vivante" : Vivant, Chaleureux, Optimiste, Entraînant), le **routeur chromatique (Phase 3B-0)** a produit un set de 15 gammes autorisées dont **0 dominante à vraie énergie chaude** — tout en "désaturé / éteint / poudré / mat / vieilli". Résultat : un univers **sépia "vieux grimoire / herbier"** qui lit *patine et sobriété*, l'exact opposé de l'énergie attendue. Le territoire SECONDAIRE entier était trahi.

Cause racine : **la désaturation a été utilisée comme anti-cliché paresseux.** Pour fuir le "pop criard" et l'"écolo niais", le routeur a tout éteint — jetant l'énergie avec le risque. Le contre-pied B=3 ("ailleurs que le secteur") a été confondu avec "sourd".

Deuxième défaut, lié : **exclusion en bloc d'une famille entière (les verts) sur la teinte au lieu de la valeur.** Le cliché écolo est dans la **luminosité haute + la fraîcheur** (vert-feuille/pousse/menthe), PAS dans le pigment vert. Un olive sombre très désaturé échappe au cliché et serait même un contre-pied fort — il a pourtant été exclu avec tous les autres verts.

---

## Où regarder (chemins absolus — session source)

Base session : `/Users/charlesbezard/claude-code-tests/test-big-portable/BIG-portable/.claude/skills/brand-identity/outputs/les-vermeil-premium-militant/`

| Fichier | Rôle dans la chaîne |
|---|---|
| `les-vermeil-brief.md` | Brief enrichi — voir §10 Tone of Voice (Enthousiaste/Proche/Fiable, anti-froid) + §15 Aversions (les 2 ventre-mous) |
| `les-vermeil-brief-analysis.md` | Analyse Phase 1 — tension premium-serviciel × militant, verdict "Confiance teintée d'enthousiasme" |
| `les-vermeil-scoping.md` | Phase 2 — Diagnostic de température = CHAUD, et le Ventre Mou sectoriel (froid industriel + écolo niais) |
| `les-vermeil-validated-temperature.md` | Température validée par l'utilisateur = chaud |
| `les-vermeil-context-clean.md` | Mix de territoires décontaminé (input du routeur) — **SECONDAIRE "Chaleur Vivante" : Vivant, Chaleureux, Optimiste, Entraînant, Texturé, Habité** |
| `les-vermeil-chromatic-gamuts.md` | **Output du routeur** — c'est le fichier digéré en aval par le sub-agent palette (Phase 3B-1). Contient maintenant la version révisée + une RÈGLE DE COMPOSITION ajoutée. |
| `.tmp-gamut-visual-config.json` + `les-vermeil-gamuts-visual.html` | Planche visuelle des gammes |

### Artefacts système concernés (le code/les prompts à corriger)

Base skill : `/Users/charlesbezard/claude-code-tests/test-big-portable/BIG-portable/.claude/skills/brand-identity/`

| Fichier | Pourquoi il est dans la boucle |
|---|---|
| `phases/phase-3b-gamut-router.md` | **Prompt du routeur — épicentre du problème.** Les règles anti-slop §1-4 poussent à qualifier/écarter, mais RIEN n'impose un quota minimal d'énergie/saturation quand le brief le demande. La désaturation n'est jamais contre-balancée. |
| `ref/chromatic-spectrum-catalog.md` | Le catalogue scanné. Les sous-gammes "vives/saturées" sont décrites comme "pop/criard" → biais qui pousse le routeur à les classer non-applicables par réflexe. |
| `scripts/phase3b-gamut-router-anti-slop.py` | Le gate. Il attrape les mots-température et le slop, mais **ne mesure pas le sous-dosage d'énergie** (un set tout-désaturé passe le gate sans alerte). |
| `phases/phase-3b-palette.md` | Sub-agent palette aval — consomme `chromatic-gamuts.md`. Si l'input est tout-désaturé, l'output le sera aussi. Le problème naît en amont mais se matérialise ici. |

---

## Ce qui s'est passé, étape par étape

1. Brief + scoping + température convergent sur **CHAUD, énergique, vivant** (premium serviciel chaleureux, anti-froid, "Confiance teintée d'enthousiasme"). Curseur B=3 (contre-pied total vs 2 ventre-mous : froid industriel + écolo niais).
2. Le routeur reçoit le mix décontaminé (où "Vivant/Chaleureux/Optimiste/Entraînant" sont explicites) + la directive d'exclusion sectorielle B=3.
3. Le routeur produit 15 autorisées : 4 neutres, 2 métaux mats, 4 terreux sourds, 5 "couleurs" mais **toutes qualifiées désaturé/poudré/éteint/moutarde/bordeaux**. Aucune dominante franche et lumineuse.
4. Il exclut **les 4 verts en bloc** (cliché écolo), sur la teinte.
5. Gate anti-slop : **PASS** (aucune règle ne détecte le sous-dosage d'énergie).
6. L'utilisateur (DC expérimenté) ressent immédiatement le décalage : *"je ne ressens pas l'énergie ni la chaleur ; on a quelque chose censé être énergique et on se retrouve avec des palettes de vieux grimoire — c'est la cata."*

## Justifications de l'auto-critique du routeur (verbatim condensé)

Renvoyé au routeur sous forme d'auto-critique honnête, il a confirmé :

> **Objection 1 (trop sage) : "fondée, largement."** Sur 15 autorisées, 0 dominante à vraie énergie. *"On ne peut pas être Optimiste et Entraînant en sourdine."* Le mot désaturé/éteint/poudré/mat apparaît sur la quasi-totalité des entrées qui auraient pu chanter. **"La désaturation a servi d'anti-cliché paresseux — elle a tué l'énergie en même temps que le risque."** Le contre-pied B=3 ne veut pas dire "éteint", il veut dire "ailleurs que le secteur" — on peut être franc/chaud sans être pop.

> **Objection 2 (tous les verts cliché ?) : "non, un vert échappe."** Le cliché écolo est dans la **luminosité haute + la fraîcheur** (vert-feuille/pousse/menthe), pas dans le pigment. Le routeur a **exclu la teinte au lieu de la valeur**. Un olive **sombre + très désaturé** (kaki militaire/céramique/terre d'ombre) ne lit PAS "responsable" — il lit *matière, terre, gravité*, colle au concept "Bocage" (Texturé/Habité), et devient distinctif *parce que* le secteur n'utilise que le vert clair. Contre-pied B=3 valide, en rôle d'accent (jamais éclairci).

## Correctif appliqué dans cette session (palliatif local)

Dans `les-vermeil-chromatic-gamuts.md` :
- **+ Terre cuite franche** (saturation moyenne-haute) comme dominante chaude de marque.
- **Safran/moutarde → Safran vif** (curcuma/ocre solaire, saturation haute).
- **Rouge poudré → Rouge-brique charnel** (saturation moyenne-haute).
- **Verts olive sombres très désaturés** : exclu → autorisé (accent/soutien, condition stricte sombre+désaturé).
- **Règle de composition ajoutée** : au moins une chaude saturée en aplat dominant lumineux ; anti-pattern "sépia vieux grimoire" explicitement proscrit.

## Recommandations système (le vrai sujet — pour les sessions d'optimisation)

1. **`phase-3b-gamut-router.md` — ajouter une règle d'ÉNERGIE symétrique aux règles anti-slop.** Si les territoires contiennent des mots d'énergie/chaleur (Vivant, Optimiste, Entraînant, Chaleureux, Audacieux…) ET/OU température chaude validée, le routeur DOIT autoriser **au moins 2-3 gammes franches et saturées** (pas seulement désaturées) et désigner explicitement au moins **1 dominante saturée candidate**. Interdire que 100% des autorisées portent un qualificatif d'extinction (désaturé/éteint/poudré/mat/sourd).

2. **Découpler anti-cliché et désaturation.** Documenter dans le prompt que le contre-pied (B=3) = *changer de territoire chromatique*, PAS *baisser la saturation*. La désaturation systématique est un faux-ami anti-slop.

3. **Exclure sur la VALEUR, pas sur la TEINTE.** Quand une famille est un cliché sectoriel, le routeur doit identifier la **zone précise du cliché** (ex: "vert = cliché en luminosité haute + fraîcheur") et ne exclure QUE cette zone, en gardant les versions sombres/désaturées/inattendues de la même teinte comme contre-pied potentiel.

4. **`phase3b-gamut-router-anti-slop.py` — ajouter un check "sous-dosage d'énergie".** Heuristique : si N mots d'énergie/chaleur dans les territoires (ou température chaude) ET 0 gamme autorisée sans qualificatif d'extinction → WARN (ou FAIL tag-or-fail) "set potentiellement sous-énergétique pour un brief qui demande de la chaleur". C'est exactement le type de problème que le gate aurait dû lever ici.

5. **`chromatic-spectrum-catalog.md` — neutraliser le biais de description.** Les sous-gammes saturées sont étiquetées "pop/criard" → le routeur les fuit par réflexe. Reformuler pour distinguer "saturé criard pop" (à éviter) de "saturé franc/charnel/solaire" (légitime et souvent nécessaire).

## Addendum (même session, Phase 3B-Vague2bis) — bug de substring dans le gate fonts anti-slop

Deuxième occurrence du même thème, sur un autre gate : `scripts/phase3b-fonts-anti-slop.py`.

**Symptôme** : le gate a classé le brief Atelier Vermeil (éditorial/premium B2B : site corporate, decks, LinkedIn, ancre Patagonia/Biocoop) comme **dashboard/SaaS UI**, et a déclenché `dashboard_display_serif` + `dashboard_body_serif` FAIL — exigeant de bannir les sérifs et de passer en sans+sans. Or sans+sans générique est précisément le **ventre-mou "froid industriel"** que le client a explicitement rejeté. Le penseur avait fait le BON choix (serif éditorial, R-display-3).

**Cause racine** : `detect_brief_register()` fait un matching **par sous-chaîne sans frontière de mot** : `if tok.lower() in lower`. Le token `'cli'` (command-line interface) matche dans "**cli**ent", "**cli**ché", "**cli**c"… présents 10× dans le brief-analysis. → faux positif "dashboard" garanti sur tout brief B2B qui parle de ses *clients*.

**Fix** (1 ligne) : matcher sur frontière de mot (regex `\bcli\b`) au lieu de `in`. Idéalement retirer `'cli'` de la liste ou le remplacer par `'cli tool'`/`'command line'` (déjà présents). Tokens à risque similaire : `'monitoring'`, `'terminal'` (peut matcher dans d'autres contextes).

**Impact** : sur n'importe quel brief mentionnant "client(s)" (= quasi tous les briefs B2B), le gate fonts force un pairing sans+sans et bannit le serif — exactement le contraire de ce qu'un brief premium/éditorial demande. À corriger en priorité, c'est un faux positif systématique.

**Verdict de cette session** : les 2 FAILs dashboard sont overridés (faux positifs documentés) ; le serif éditorial est conservé. Le FAIL `format_body` (12 au lieu de 10) est réel et trivial (longlist tronquée au top 10 en aval).

## Leçon transférable

Les gates et règles anti-slop du pipeline sont **asymétriques** : ils protègent contre l'excès (criard, slop, training-defaults) mais **pas contre le défaut** (sous-énergie, sur-sobriété). Sur un brief qui demande de l'audace ou de la chaleur, cette asymétrie produit mécaniquement un résultat en-deçà du brief, et **le gate le valide silencieusement**. Tout sous-système anti-slop devrait avoir un garde-fou symétrique "anti-fadeur" piloté par les signaux du brief.
