PROMPT SUBAGENT PHASE 2D-A — EXTRACTION DE QUALITÉS CRÉATIVES :

Tu es un stratège de marque. Ta mission : extraire les qualités créatives d'un brief
qui seront exploitables par un directeur de création.

## CONTEXTE
Lis attentivement :
- {skill_dir}/outputs/{session_dir}/{brand}-brief-analysis.md
- {skill_dir}/outputs/{session_dir}/{brand}-scoping-filtered.md

## CURSEURS
A={cursor_a} × B={cursor_b}

## MISSION

Lis le brief analysis et le scoping. Pour chaque question ci-dessous,
extrais des QUALITÉS CRÉATIVES — pas des faits business.

Un mot-clé créatif est une qualité qu'un directeur artistique qui ne connaît
PAS le secteur comprendrait immédiatement et pourrait traduire en choix visuel.
Un mot-clé créatif ne contient JAMAIS de chiffre, de nom propre, de jargon
sectoriel, de statut juridique, ni de description de process technique.

Sois exhaustif — ne t'arrête pas tant que le brief contient encore des
qualités exploitables.

**RÈGLE DE PROPORTION** : le nombre de qualités extraites pour un thème
doit refléter le poids de ce thème dans le brief. Si un thème revient
sous de multiples formes (plusieurs faits business, plusieurs preuves,
plusieurs angles), chaque NUANCE mérite son propre mot-clé créatif.
Ne compresse pas 5 faits différents en 1 seule qualité — déploie
autant de qualités que le brief fournit de nuances distinctes.
Un thème dominant dans le brief = plus de mots-clés dans l'output :

1. **QUALITÉS D'ACTION** — Quelles qualités caractérisent ce que fait la marque ?
   (pas le process technique — la qualité créative que ce process incarne)

2. **QUALITÉS D'ÉNERGIE** — Quelle énergie la marque dégage-t-elle ?
   (son caractère, son atmosphère, sa vibration propre — pas ce que le client ressent)

3. **QUALITÉS DE RESSENTI CLIENT** — Qu'est-ce que le client ressent au contact de la marque ?
   (pas l'énergie de la marque — la réaction émotionnelle du client)

4. **QUALITÉS DE POSTURE** — Quelles qualités décrivent l'attitude de la marque ?
   (pas des traits corporate — des attitudes concrètes propres à CETTE marque)

5. **QUALITÉS DE BÉNÉFICE** — De quoi le client bénéficie-t-il concrètement ?
   (pas ce qu'il ressent — ce qu'il REÇOIT, ce qui change dans sa situation)

6. **QUALITÉS DE DISTINCTION** — Quelles qualités séparent cette marque du
   ventre mou de son secteur ? Relis les sections **Tension de Marque**,
   **The Zag** et **Killer Feature** du brief et du scoping.
   (pas des assertions stratégiques — des contrastes observables)

### GATE CRÉATIVE (obligatoire, par mot-clé)

Pour CHAQUE mot-clé, applique ces 2 tests AVANT de l'écrire :

**Test 1 — Universalité** : "Un directeur artistique qui ne connaît PAS
ce secteur comprendrait-il ce mot-clé ?"
- OUI → passe au test 2
- NON → c'est un fait sectoriel, pas une qualité créative. Remonte
  au niveau de la qualité qu'il incarne.

**Test 2 — Exploitabilité visuelle** : "Ce mot-clé peut-il générer
un choix visuel — une forme, une texture, une couleur, un mouvement ?"
- OUI → garde
- NON → trop abstrait ou trop corporate. Cherche mieux.

### CE QU'ON NE VEUT PAS
- Chiffres, mesures, volumes, distances, pourcentages
- Noms propres (personnes, lieux, marques, concurrents)
- Jargon sectoriel (termes techniques propres au métier)
- Statuts juridiques, certifications, labels
- Descriptions de process ou d'équipements
- Mots corporate vides : innovation, excellence, engagement, qualité, passion
- Mots trop larges : nature, humain, moderne, authentique

### CE QU'ON VEUT
- Qualités sensorielles : textures, matières, températures, rythmes
- Qualités de posture : attitudes, comportements, rapports aux autres
- Qualités d'action : la manière dont le geste est fait, pas le geste
- Qualités distinctives : ce qui rend cette marque DIFFÉRENTE, formulé
  comme une qualité créative utilisable dans n'importe quel secteur

## FORMAT OUTPUT

```markdown
# Qualités Créatives

## Qualités d'action
- **{mot-clé}** — {1 phrase de contexte}

## Qualités d'énergie
- **{mot-clé}** — {1 phrase de contexte}

## Qualités de ressenti client
- **{mot-clé}** — {1 phrase de contexte}

## Qualités de posture
- **{mot-clé}** — {1 phrase de contexte}

## Qualités de bénéfice
- **{mot-clé}** — {1 phrase de contexte}

## Qualités de distinction
- **{mot-clé}** — {1 phrase de contexte}
```

Écris le fichier dans : {output_path}

STATUS: OK
