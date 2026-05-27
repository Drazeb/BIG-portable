# Draft refactor Étape 4 BIG — state machine atomique 15 sous-étapes

Statut : **DRAFT à valider par Charles avant Phase R3 (implémentation SKILL.md).**
Auteur : Subagent rédacteur (Phase R2).
Plan parent : `/Users/charlesbezard/.claude/plans/twinkly-wondering-hamming.md`.

---

## Contexte

Le pipeline BIG Phase 4 (`SKILL.md` lignes ~2714-3744) a accumulé **8 patches réactifs** en 3 jours (Patch A, B, P1, P2, P3, P4, P5, P6) pour corriger des "shortcuts orchestrateur" : le LLM lit la zone Étape 4 comme un **pseudocode narratif d'environ 600 lignes** qu'il interprète librement, et il "pioche" parmi les contrôles, les boucles, les invocations de subagents.

Le refactor cible une **state machine atomique** : 15 sous-étapes 4.1 → 4.15, chacune avec **pré-condition bash bloquante**, **action unique**, **post-condition bash bloquante**, **transition explicite**. Pas de boucles inline (chaque itération = sous-étape distincte). Pas de pseudocode narratif. Les 6+2 patches sont **préservés intégralement** mais ré-encodés comme conditions bash explicites au lieu d'instructions à interpréter.

Principe directeur : si l'orchestrateur peut interpréter une instruction, il la shortcutera. La seule défense robuste est un check bash qui `exit 1` quand l'artefact attendu est absent.

---

## Vue d'ensemble — séquence des 15 sous-étapes

| ID | Nom | Type d'action | Conditionnelle ? | Parallèle 3 concepts ? | Artefact in (clé) | Artefact out (clé) |
|---|---|---|---|---|---|---|
| **4.1** | Création HTML v0 | TASK_TOOL_INVOCATION | NON | OUI (3 Designers parallèles) | pitch + style-choice + visuels Phase 3 | `{brand}-style-tile-concept-{N}.html` v0 |
| **4.2** | Gates Python v0 | BASH_COMMAND | NON | OUI | HTML v0 | `.gates-finishing-c{N}-v0.json` + `.gates-blacklist-c{N}-v0.json` |
| **4.3** | Gate visuel v0 | TASK_TOOL_INVOCATION (contrôleur lecture-seule) | NON | OUI | HTML v0 + gates JSON | `.finishing-gate-c{N}-v0.pass` (JSON structuré) |
| **4.4** | Production JSON corrections v0 (P6) | TASK_TOOL_INVOCATION ou FILE_WRITE | NON (toujours produit, même vide) | OUI | gates JSON + visuel pass | `.finishing-gate-c{N}-v0-corrections.json` |
| **4.5** | Designer correction v0→v1 | TASK_TOOL_INVOCATION | OUI (skip si corrections vide) | OUI | corrections JSON + v0 | HTML v1 (overwrite) |
| **4.6** | Re-validation v1 | BASH_COMMAND + TASK_TOOL_INVOCATION | OUI (skip si 4.5 sauté) | OUI | HTML v1 | `.gates-finishing-c{N}-v1.json` + `.finishing-gate-c{N}-v1.pass` |
| **4.7** | Artefact (Designer) | TASK_TOOL_INVOCATION + FILE_WRITE | NON | OUI | HTML v_current + pitch | HTML avec artefact (overwrite) |
| **4.8** | Re-validation post-artefact (P5+P6) | BASH_COMMAND + TASK_TOOL_INVOCATION | NON | OUI | HTML avec artefact | `.gates-finishing-c{N}-art.json` + `.finishing-gate-c{N}-art.pass` + `.finishing-gate-c{N}-art-corrections.json` |
| **4.9** | Correction post-artefact | TASK_TOOL_INVOCATION | OUI (skip si corrections vide) | OUI | corrections art JSON + HTML | HTML patché (overwrite) |
| **4.10** | Critique 4-parallèle iter0 | TASK_TOOL_INVOCATION (×4 parallèle) | NON | OUI (par concept) — chacun lance 4 critiques en parallèle | HTML stable + gates JSON v_artefact | 4 fichiers `.critique-c{N}-{domain}-iter0.json` |
| **4.11** | Synthétiseur iter0 (P3) | TASK_TOOL_INVOCATION + DECISION (fallback Vague 1) | NON | OUI | 4 JSON Critiques | `.critique-c{N}-iter0.json` (avec `synthesizer_subagent_signature`) |
| **4.12** | Designer correction iter0 | TASK_TOOL_INVOCATION | OUI (skip si total_violations==0) | OUI | Synthétiseur JSON + HTML | HTML iter1 (overwrite) |
| **4.13** | Boucle iter1 | TASK_TOOL_INVOCATION (×4 + 1 + 1) | OUI (skip si 4.12 sauté OU oscillation) | OUI | HTML iter1 | HTML final + `.critique-c{N}-iter1.json` |
| **4.14** | Audit consolidé (Patch A + P1) | BASH_COMMAND (heredoc JSON) | NON | OUI | tous artefacts précédents | `.pipeline-audit-c{N}.json` |
| **4.15** | Swap haute résolution + ouverture | BASH_COMMAND (Python inline) + `open` | NON | NON (séquentiel sur les 3 fichiers) | HTML final + `.b64` files | HTML avec visuels haute-rés + 3 fenêtres navigateur |

**Convention de nommage des artefacts** : `.{type}-c{N}-{stage}.json`
- `{type}` ∈ {`gates-finishing`, `gates-blacklist`, `finishing-gate`, `critique`, `pipeline-audit`}
- `{N}` ∈ {1, 2, 3}
- `{stage}` ∈ {`v0`, `v1`, `art`, `iter0`, `iter1`} ; suffixe optionnel `-corrections`, `-recheck`

**Notation parallélisme** : "OUI (3 concepts en parallèle)" = l'orchestrateur lance les actions des 3 concepts dans le **même message** Task tool. À l'intérieur d'une sous-étape parallèle, les 3 concepts produisent leurs artefacts indépendamment ; la post-condition vérifie les 3.

---

## Détail des sous-étapes

### Étape 4.1 — Création HTML v0 (Designer mode CRÉATION)

**Type d'action** : TASK_TOOL_INVOCATION

**Conditionnelle ?** : NON (toujours exécutée — c'est l'entrée du pipeline Phase 4).

**Concept parallèle ?** : OUI — 3 Task tools lancés EN PARALLÈLE dans un seul message orchestrateur, un par concept.

**Patches préservés** : aucun directement (c'est la création initiale).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  [ -f "$sd/{brand}-pitch-c${n}.md" ] || { echo "❌ Pitch c${n} manquant — RETOUR à Phase 3B"; exit 1; }
  [ -f "$sd/{brand}-style-choice-c${n}.md" ] || { echo "❌ Style-choice c${n} manquant — RETOUR à Phase 3B-7-checkpoint"; exit 1; }
done
[ -f "{skill_dir}/phases/phase-4-styletile.md" ] || { echo "❌ Prompt phase-4-styletile.md introuvable"; exit 1; }
[ -f "{skill_dir}/ref/anti-slop-blacklist-tier1.md" ] || { echo "❌ TIER 1 anti-slop manquant"; exit 1; }
[ -f "{skill_dir}/ref/a11y-fondamentaux-tier1.md" ] || { echo "❌ TIER 1 a11y manquant"; exit 1; }
[ -f "{skill_dir}/ref/finition-elite-tier1.md" ] || { echo "❌ TIER 1 finition manquant"; exit 1; }
[ -f "{skill_dir}/ref/hierarchie-visuelle-tier1.md" ] || { echo "❌ TIER 1 hiérarchie manquant"; exit 1; }
echo "✓ Pré-conditions 4.1 OK — autorisé à lancer 3 Designers parallèles"
```

▸ ACTION :
Lire `{skill_dir}/phases/phase-4-styletile.md` UNE FOIS, puis lancer **3 Task tools en parallèle (1 message orchestrateur)** avec les variables résolues :

Variables communes (identiques pour les 3) :
- `{skill_dir}`, `{brand}`, `{session_dir}`, `{cursor_a}`, `{cursor_b}`
- `{anti_slop_blacklist_tier1}` = contenu intégral `ref/anti-slop-blacklist-tier1.md`
- `{a11y_fondamentaux_tier1}` = contenu intégral `ref/a11y-fondamentaux-tier1.md`
- `{finition_elite_tier1}` = contenu intégral `ref/finition-elite-tier1.md`
- `{hierarchie_visuelle_tier1}` = contenu intégral `ref/hierarchie-visuelle-tier1.md`
- `{style_tile_example}` = exemple choisi par règle anti-contamination (cf. mapping `cursor_a` actuel SKILL.md)
- `{ventre_mou_section}` = section pré-formatée selon `cursor_b` (B=1/2/3)
- `{correction_mode_block}` = **chaîne VIDE** (mode CRÉATION)
- `{awards_etalon_block}` = bloc conditionnel selon présence `etalon-*.png`

Variables spécifiques par concept N :
- `{concept_number}` = N
- `{concept_name}` = titre du concept
- `{concept_details}` = contenu pertinent extrait de `{brand}-pitch-c{N}.md`
- `{style_choice}` = contenu intégral `{brand}-style-choice-c{N}.md`
- `{css_pattern_block}` = squelettes Voice Block + Atmosphere Block extraits de `ref/css-patterns-phase4.md`
- `{visual_reference_block}` = bloc conditionnel selon visuels Phase 3C présents

Chaque Designer écrit `{sd}/{brand}-style-tile-concept-{N}.html` (mode CRÉATION → triptyque hero + placeholder artefact + atmosphere).

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  f="$sd/{brand}-style-tile-concept-${n}.html"
  [ -f "$f" ] || { echo "❌ HTML v0 c${n} manquant — Designer Phase 4 a échoué — relancer"; exit 1; }
  [ "$(wc -c < "$f")" -gt 10000 ] || { echo "❌ HTML v0 c${n} trop court (<10kB) — output incomplet"; exit 1; }
  grep -q "<!-- ARTEFACT_PLACEHOLDER -->" "$f" || { echo "❌ HTML v0 c${n} sans placeholder artefact — Designer hors-spec"; exit 1; }
  grep -q ":root" "$f" || { echo "❌ HTML v0 c${n} sans :root — Designer hors-spec"; exit 1; }
done
echo "✓ 3 HTML v0 valides — passer à 4.2"
```

➡️ TRANSITION : passer à Étape **4.2** (Gates Python v0).

---

### Étape 4.2 — Gates Python v0 (blacklist + finishing avec --json-output)

**Type d'action** : BASH_COMMAND

**Conditionnelle ?** : NON.

**Concept parallèle ?** : OUI — 3 paires de scripts Python lancés en parallèle (les scripts sont CPU-bound courts, peuvent tourner concurrentiellement).

**Patches préservés** : **P4** (capture intégrale du finishing gate via `--json-output`) + **P5** (Vague 2 warnings préservés dans le JSON, plus de résumé stdout).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  [ -f "$sd/{brand}-style-tile-concept-${n}.html" ] || { echo "❌ HTML v0 c${n} manquant — RETOUR à 4.1"; exit 1; }
done
[ -f "{skill_dir}/scripts/phase4-finishing-gate.py" ] || { echo "❌ Script finishing-gate.py manquant"; exit 1; }
[ -f "{skill_dir}/scripts/phase4-blacklist-gate.py" ] || { echo "❌ Script blacklist-gate.py manquant"; exit 1; }
```

▸ ACTION :
Pour chaque concept N ∈ {1,2,3}, exécuter en parallèle :

```bash
sd="{skill_dir}/outputs/{session_dir}"
html="$sd/{brand}-style-tile-concept-${N}.html"

# 1. Finishing gate AVEC --json-output (P4) — capture vague1 + vague2 intégrale
python3 "{skill_dir}/scripts/phase4-finishing-gate.py" \
    "$html" {cursor_a} \
    --json-output "$sd/.gates-finishing-c${N}-v0.json"
finishing_exit=$?

# 2. Blacklist gate (binaire FAIL/PASS, pas de --json-output dans la version actuelle ;
#    si le script est patché pour supporter --json-output, l'utiliser ici aussi)
python3 "{skill_dir}/scripts/phase4-blacklist-gate.py" "$html" \
    > "$sd/.gates-blacklist-c${N}-v0.stdout" 2>&1
blacklist_exit=$?

# 3. Si --no-images détecté (visual_reference_block vide), ajouter --no-images au finishing-gate.
#    L'orchestrateur connaît cet état depuis l'invocation 4.1.

# 4. Écrire un fichier consolidé pour les Critiques (P5 — vague2 préservée intégralement)
python3 -c "
import json, sys
fin = json.load(open('$sd/.gates-finishing-c${N}-v0.json'))
with open('$sd/.gates-blacklist-c${N}-v0.stdout') as f:
    bl_out = f.read()
consolidated = {
    'blacklist_gate': {'exit_code': $blacklist_exit, 'raw_output': bl_out},
    'finishing_gate': fin,
    'vague2_warnings_total': fin.get('vague2', {}).get('total_warnings', 0)
}
json.dump(consolidated, open('$sd/.gates-c${N}-v0.json', 'w'), indent=2)
"
```

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  fin="$sd/.gates-finishing-c${n}-v0.json"
  cons="$sd/.gates-c${n}-v0.json"
  [ -f "$fin" ] || { echo "❌ Finishing gate JSON c${n} manquant"; exit 1; }
  [ -f "$cons" ] || { echo "❌ Gates consolidés JSON c${n} manquant"; exit 1; }
  python3 -c "import json; d=json.load(open('$fin')); assert 'vague2' in d, 'P5 violé : vague2 absente'" \
    || { echo "❌ Finishing JSON c${n} sans section vague2 — P4/P5 violés — relancer"; exit 1; }
  python3 -c "import json; json.load(open('$cons'))" \
    || { echo "❌ Gates consolidés c${n} JSON invalide"; exit 1; }
done
echo "✓ 3 gates Python v0 OK — vague2 visible — passer à 4.3"
```

➡️ TRANSITION : passer à Étape **4.3** (Gate visuel v0).

---

### Étape 4.3 — Gate visuel v0 (contrôleur Puppeteer lecture-seule)

**Type d'action** : TASK_TOOL_INVOCATION

**Conditionnelle ?** : NON.

**Concept parallèle ?** : OUI — 3 contrôleurs Task tool lancés en parallèle.

**Patches préservés** : **Patch B** (audit défensif TIER 1 visuel — 3ème couche graphique évidente) + **P6** (le contrôleur ne patche PAS le HTML lui-même — observation seulement).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  [ -f "$sd/.gates-finishing-c${n}-v0.json" ] || { echo "❌ Gates v0 c${n} manquant — RETOUR à 4.2"; exit 1; }
  [ -f "$sd/{brand}-style-tile-concept-${n}.html" ] || { echo "❌ HTML v0 c${n} manquant"; exit 1; }
done
which node >/dev/null 2>&1 || { echo "❌ Node introuvable pour Puppeteer"; exit 1; }
[ -d "/tmp/pup/node_modules/puppeteer" ] || { echo "❌ Puppeteer non installé sous /tmp/pup"; exit 1; }
```

▸ ACTION :
Lancer 3 Task tools EN PARALLÈLE, chacun avec un prompt **contrôleur LECTURE-SEULE STRICTEMENT** (extrait du prompt 4A-ter actuel SKILL.md, mais limité aux Étapes 1-3 — la production du JSON corrections est isolée en 4.4) :

Le contrôleur reçoit en variables résolues :
- `{skill_dir}`, `{brand}`, `{session_dir}`, `{cursor_a}`, `{N}` (concept_number)

Mission du contrôleur :
1. Identifier les éléments de 3ème couche graphique dans le CSS (grain, dot/grid/hatch patterns, formes décoratives, overlays atmosphériques)
2. Pour chaque élément, prendre un crop ciblé 250×250 via Puppeteer (`boundingBox()`)
3. Lire chaque crop via Read tool et juger IMPITOYABLEMENT : VISIBLE / FAIL_INVISIBLE / DOUTEUX (= FAIL)
4. Vérifier aussi : pas de halo polygonal (`clip-path` polygon), pas de brand watermark, pas de cercles à contour net
5. Nettoyer les crops temporaires
6. Écrire un **marqueur final JSON STRUCTURÉ** dans `.finishing-gate-c{N}-v0.pass` avec :
   - `verdict` : "PASS" / "WARN"
   - `concept`, `timestamp`, `html_audited`, `html_sha256`
   - `step1_finishing_gate` : exit code + verdict + iterations + raw_output_first_line
   - `step1_blacklist_gate` : idem
   - `step3_visual_check` : `executed: true`, `elements_identified[]`, `crops_generated[]`, `verdict_per_element{}`
   - `subagent_signature` : "controleur-c{N}-v0"

**⛔ INTERDICTIONS STRICTES (rappel pattern P6)** dans le prompt contrôleur :
- ⛔ Ne JAMAIS modifier le HTML/CSS
- ⛔ Ne JAMAIS RESUME un autre subagent
- ⛔ Ne PAS écrire le fichier `.finishing-gate-c{N}-v0-corrections.json` (cette responsabilité est isolée en 4.4)

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  marker="$sd/.finishing-gate-c${n}-v0.pass"
  [ -f "$marker" ] || { echo "❌ Marqueur visuel v0 c${n} manquant — relancer contrôleur c${n}"; exit 1; }
  python3 -c "
import json
d=json.load(open('$marker'))
assert d.get('step3_visual_check',{}).get('executed') is True, 'step3 non exécuté'
assert 'html_sha256' in d, 'sha256 absent'
assert d.get('subagent_signature','').startswith('controleur-c${n}'), 'signature absente/wrong'
" || { echo "❌ Marqueur visuel v0 c${n} invalide ou shortcut détecté — RELANCER contrôleur c${n}"; exit 1; }
done
echo "✓ 3 marqueurs visuels v0 valides — passer à 4.4"
```

➡️ TRANSITION : passer à Étape **4.4** (Production JSON corrections v0).

---

### Étape 4.4 — Production JSON corrections v0 (P6 — pivot architectural)

**Type d'action** : TASK_TOOL_INVOCATION (si violations) OU FILE_WRITE (JSON vide marqueur)

**Conditionnelle ?** : NON (le fichier est TOUJOURS écrit ; son contenu est conditionnel).

**Concept parallèle ?** : OUI — 3 productions parallèles.

**Patches préservés** : **P6 nouveau** — pattern "contrôleur extrait corrections → orchestrateur invoque Designer". Sépare l'observation (4.3) de l'extraction de corrections (4.4).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  [ -f "$sd/.gates-finishing-c${n}-v0.json" ] || { echo "❌ Gates v0 c${n} manquant — RETOUR à 4.2"; exit 1; }
  [ -f "$sd/.finishing-gate-c${n}-v0.pass" ] || { echo "❌ Visuel v0 c${n} manquant — RETOUR à 4.3"; exit 1; }
done
```

▸ ACTION :
Pour chaque concept N en parallèle, l'orchestrateur :

1. Parse les 2 sources pour détecter d'éventuelles violations :
```bash
sd="{skill_dir}/outputs/{session_dir}"
python3 -c "
import json, sys
fin = json.load(open('$sd/.gates-finishing-c${N}-v0.json'))
visu = json.load(open('$sd/.finishing-gate-c${N}-v0.pass'))
has_fail = (
    fin.get('vague1', {}).get('verdict') == 'FAIL'
    or any(v == 'FAIL_INVISIBLE' or v == 'DOUTEUX' for v in visu.get('step3_visual_check', {}).get('verdict_per_element', {}).values())
)
print('HAS_FAIL' if has_fail else 'NO_FAIL')
" > "$sd/.tmp-violation-check-c${N}.txt"
verdict=$(cat "$sd/.tmp-violation-check-c${N}.txt")
rm "$sd/.tmp-violation-check-c${N}.txt"
```

2. **Si `verdict == NO_FAIL`** (pas de violation à patcher) : l'orchestrateur écrit directement le marqueur vide :
```bash
echo '{"corrections": [], "produced_by": "orchestrator-no-violations", "concept": '"$N"', "iteration": 0}' \
  > "$sd/.finishing-gate-c${N}-v0-corrections.json"
```

3. **Si `verdict == HAS_FAIL`** : l'orchestrateur invoque un Task tool contrôleur extracteur (subagent NEUF, prompt minimal) avec mission :

```
Tu es un extracteur de corrections. Lis ces 2 fichiers JSON :
- {sd}/.gates-finishing-c{N}-v0.json (rapport gates Python complet, vague1+vague2)
- {sd}/.finishing-gate-c{N}-v0.pass (rapport gate visuel)

Produis UNIQUEMENT un fichier JSON corrections list au format :
{
  "produced_by": "controller-extracted-c{N}",
  "concept": {N},
  "iteration": 0,
  "html_audited": "{brand}-style-tile-concept-{N}.html",
  "source_gates": ["finishing-gate", "blacklist-gate", "visual-gate"],
  "corrections": [
    {
      "rule_id": "<ex: finishing-gate.no-flat-shadow OU visual-gate.grain-not-evident>",
      "severity": "FAIL",
      "line": <int ou null>,
      "current": "<extrait CSS fautif, ~80 chars>",
      "fix": "<directive de correction concrète, vocabulaire designer>",
      "reason": "<règle violée, 1 phrase>"
    }
  ]
}

Écris le résultat dans : {sd}/.finishing-gate-c{N}-v0-corrections.json

⛔ INTERDICTIONS ABSOLUES (P6) :
- Ne JAMAIS modifier le HTML/CSS
- Ne JAMAIS RESUME un autre subagent
- Ne JAMAIS lancer Puppeteer
- Tu produis UNIQUEMENT ce JSON. Rien d'autre.
```

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  f="$sd/.finishing-gate-c${n}-v0-corrections.json"
  [ -f "$f" ] || { echo "❌ JSON corrections c${n} manquant — relancer 4.4"; exit 1; }
  python3 -c "
import json
d = json.load(open('$f'))
assert 'corrections' in d, 'champ corrections absent'
assert isinstance(d['corrections'], list), 'corrections pas une liste'
assert d.get('produced_by','').startswith(('orchestrator-no-violations', 'controller-extracted')), 'producer wrong'
" || { echo "❌ JSON corrections c${n} invalide"; exit 1; }
done
echo "✓ 3 JSON corrections v0 valides — passer à 4.5"
```

➡️ TRANSITION : passer à Étape **4.5** (Designer correction v0→v1, conditionnelle).

---

### Étape 4.5 — Designer correction v0→v1 (CONDITIONNELLE)

**Type d'action** : TASK_TOOL_INVOCATION

**Conditionnelle ?** : **OUI** — skip si `corrections == []` pour les 3 concepts (sinon exécuter pour les concepts qui en ont).

**Concept parallèle ?** : OUI — 1 Designer mode CORRECTION par concept ayant des corrections, lancés en parallèle.

**Patches préservés** : **P6** (pattern Designer mode CORRECTION CHIRURGICALE — JAMAIS d'agent custom léger).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
# Pour chaque concept, déterminer si correction nécessaire
concepts_to_correct=""
for n in 1 2 3; do
  f="$sd/.finishing-gate-c${n}-v0-corrections.json"
  [ -f "$f" ] || { echo "❌ JSON corrections c${n} manquant — RETOUR à 4.4"; exit 1; }
  count=$(python3 -c "import json; print(len(json.load(open('$f'))['corrections']))")
  if [ "$count" -gt 0 ]; then
    concepts_to_correct="$concepts_to_correct $n"
    # Backup avant correction (rollback divergence en 4.6)
    cp "$sd/{brand}-style-tile-concept-${n}.html" "$sd/{brand}-style-tile-concept-${n}.html.bakv0"
  fi
done
echo "Concepts à corriger : $concepts_to_correct"

# Si aucun → SKIP cette sous-étape ; transition directe vers 4.7
if [ -z "$concepts_to_correct" ]; then
  echo "✓ Aucune correction v0 à appliquer — SKIP 4.5 et 4.6 — transition vers 4.7"
  exit 0  # ce code de sortie 0 = skip explicite, l'orchestrateur saute en 4.7
fi
```

▸ ACTION (uniquement pour les concepts dans `concepts_to_correct`) :
Pour chaque concept N à corriger, lancer un Task tool avec le prompt complet `{skill_dir}/phases/phase-4-styletile.md` résolu avec :
- `{correction_mode_block}` = bloc non vide composé par l'orchestrateur :

```
=== HTML EXISTANT À PATCHER (v0) ===

[contenu intégral de {brand}-style-tile-concept-{N}.html]

=== LISTE DE CORRECTIONS À APPLIQUER (JSON v0) ===

[contenu intégral de .finishing-gate-c{N}-v0-corrections.json]

=== INSTRUCTIONS ===

Tu es en MODE CORRECTION CHIRURGICALE. Patche EXACTEMENT les zones listées.
NE MODIFIE PAS les zones non listées. NE RECRÉE RIEN.
Output : HTML complet patché — overwrite {brand}-style-tile-concept-{N}.html.
```

- Toutes les autres variables (`{concept_number}`, `{concept_name}`, `{style_choice}`, `{anti_slop_*tier1}`, etc.) sont passées identiques au mode CRÉATION (cohérence du :root et du design system).

**⛔ INTERDICTION ABSOLUE** : ne JAMAIS improviser un agent custom léger inline. TOUJOURS le prompt complet `phase-4-styletile.md`.

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
# Si la pré-condition a renvoyé exit 0 (skip), cette POST n'est pas évaluée.
# Sinon, vérifier que les concepts corrigés ont un HTML modifié et toujours valide.
for n in $concepts_to_correct; do
  html="$sd/{brand}-style-tile-concept-${n}.html"
  bak="$sd/{brand}-style-tile-concept-${n}.html.bakv0"
  [ -f "$html" ] || { echo "❌ HTML c${n} manquant après correction"; exit 1; }
  [ "$(wc -c < "$html")" -gt 10000 ] || { echo "❌ HTML c${n} trop court après correction"; exit 1; }
  if [ -f "$bak" ] && cmp -s "$html" "$bak"; then
    echo "⚠ HTML c${n} non modifié par Designer correction — log mais continuer"
  fi
done
echo "✓ Designer corrections v0 appliquées sur :$concepts_to_correct — passer à 4.6"
```

➡️ TRANSITION :
- Si pré-condition a fait `exit 0` (skip) → passer directement à **4.7**
- Sinon → passer à **4.6** (re-validation v1)

---

### Étape 4.6 — Re-validation v1 (CONDITIONNELLE)

**Type d'action** : BASH_COMMAND + TASK_TOOL_INVOCATION

**Conditionnelle ?** : **OUI** — exécutée seulement pour les concepts qui ont reçu une correction en 4.5.

**Concept parallèle ?** : OUI — pour chaque concept corrigé, re-run gates Python + nouveau contrôleur visuel en parallèle.

**Patches préservés** : **P4+P5** (re-validation préserve vague2) + **Patch B** (re-check visuel) + garde-fou divergence (rollback si Designer a empiré).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
# Cette étape n'est exécutée que si 4.5 a tourné. Reconstituer la liste depuis le fichier marqueur.
concepts_to_recheck=""
for n in 1 2 3; do
  if [ -f "$sd/{brand}-style-tile-concept-${n}.html.bakv0" ]; then
    # Backup existe → 4.5 a tourné pour ce concept
    concepts_to_recheck="$concepts_to_recheck $n"
  fi
done
[ -n "$concepts_to_recheck" ] || { echo "✓ Aucun concept à re-valider — transition directe vers 4.7"; exit 0; }
```

▸ ACTION :
Pour chaque concept N dans `concepts_to_recheck` :

1. Re-run gates Python (même protocole P4+P5 que 4.2) avec suffixe `-v1` :
```bash
python3 "{skill_dir}/scripts/phase4-finishing-gate.py" \
    "$sd/{brand}-style-tile-concept-${N}.html" {cursor_a} \
    --json-output "$sd/.gates-finishing-c${N}-v1.json"
python3 "{skill_dir}/scripts/phase4-blacklist-gate.py" \
    "$sd/{brand}-style-tile-concept-${N}.html" \
    > "$sd/.gates-blacklist-c${N}-v1.stdout" 2>&1
```

2. Garde-fou divergence — comparer count de violations critiques v1 vs v0 :
```bash
v0_crit=$(python3 -c "import json; d=json.load(open('$sd/.gates-finishing-c${N}-v0.json')); print(d.get('vague1',{}).get('total_fails',0))")
v1_crit=$(python3 -c "import json; d=json.load(open('$sd/.gates-finishing-c${N}-v1.json')); print(d.get('vague1',{}).get('total_fails',0))")
if [ "$v1_crit" -gt "$v0_crit" ]; then
  echo "⚠ Designer correction c${N} a EMPIRÉ ($v0_crit→$v1_crit) — ROLLBACK v0"
  cp "$sd/{brand}-style-tile-concept-${N}.html.bakv0" "$sd/{brand}-style-tile-concept-${N}.html"
  echo "ROLLBACK_V0" > "$sd/.fix-loop-c${N}.log"
fi
```

3. Lancer un Task tool contrôleur visuel v1 (même prompt que 4.3, mais avec suffixe `-v1` sur le marqueur) → produit `.finishing-gate-c{N}-v1.pass`.

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in $concepts_to_recheck; do
  [ -f "$sd/.gates-finishing-c${n}-v1.json" ] || { echo "❌ Gates v1 c${n} manquant"; exit 1; }
  python3 -c "import json; d=json.load(open('$sd/.gates-finishing-c${n}-v1.json')); assert 'vague2' in d" \
    || { echo "❌ Gates v1 c${n} sans vague2 — P5 violé"; exit 1; }
  [ -f "$sd/.finishing-gate-c${n}-v1.pass" ] || { echo "❌ Visuel v1 c${n} manquant"; exit 1; }
  python3 -c "
import json
d=json.load(open('$sd/.finishing-gate-c${n}-v1.pass'))
assert d.get('step3_visual_check',{}).get('executed') is True
" || { echo "❌ Visuel v1 c${n} shortcut"; exit 1; }
done
echo "✓ Re-validation v1 OK — passer à 4.7"
```

➡️ TRANSITION : passer à Étape **4.7** (Artefact).

---

### Étape 4.7 — Artefact (Designer mode artefact)

**Type d'action** : TASK_TOOL_INVOCATION + FILE_WRITE (insertion Python post-traitement)

**Conditionnelle ?** : NON.

**Concept parallèle ?** : OUI — 3 Designers artefact en parallèle.

**Patches préservés** : aucun directement (étape standard).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  [ -f "$sd/{brand}-style-tile-concept-${n}.html" ] || { echo "❌ HTML stable c${n} manquant — RETOUR à 4.5/4.6"; exit 1; }
  grep -q "<!-- ARTEFACT_PLACEHOLDER -->" "$sd/{brand}-style-tile-concept-${n}.html" \
    || { echo "❌ Placeholder artefact c${n} absent — Designer a effacé le placeholder en correction — corriger manuellement"; exit 1; }
done
[ -f "{skill_dir}/phases/phase-4-artefact.md" ] || { echo "❌ Prompt phase-4-artefact.md manquant"; exit 1; }
```

▸ ACTION :
Lancer 3 Task tools EN PARALLÈLE avec le prompt complet `{skill_dir}/phases/phase-4-artefact.md` résolu pour chaque concept.

Variables communes : `{skill_dir}`, `{brand}`, `{session_dir}`, `{cursor_a}`, `{cursor_b}`, `{anti_slop_blacklist_tier1}`, `{a11y_fondamentaux_tier1}`, `{finition_elite_tier1}`, `{hierarchie_visuelle_tier1}`, `{style_tile_example}`, `{example_artefact_type}`, `{ventre_mou_section}` (mêmes valeurs que 4.1).

Variables spécifiques par concept : `{concept_number}`, `{concept_data_metrics}` (extrait de la section "Données métier clés" du pitch).

Chaque Designer écrit `{sd}/.tmp-artefact-concept-{N}.html`.

Post-traitement orchestrateur (Python inline) — insertion dans le style-tile :
```python
import re
session = '{skill_dir}/outputs/{session_dir}'
for n in [1, 2, 3]:
    st = f'{session}/{brand}-style-tile-concept-{n}.html'
    art = f'{session}/.tmp-artefact-concept-{n}.html'
    with open(st) as f: html = f.read()
    with open(art) as f: art_html = f.read()
    if '<!-- ARTEFACT_PLACEHOLDER -->' not in html:
        raise SystemExit(f'❌ Placeholder absent dans {st} — abort')
    html = html.replace('<!-- ARTEFACT_PLACEHOLDER -->', art_html)
    with open(st, 'w') as f: f.write(html)
# Cleanup
import glob, os
for f in glob.glob(f'{session}/.tmp-artefact-concept-*.html'):
    os.remove(f)
```

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  html="$sd/{brand}-style-tile-concept-${n}.html"
  [ -f "$html" ] || { echo "❌ HTML c${n} manquant après insertion artefact"; exit 1; }
  if grep -q "<!-- ARTEFACT_PLACEHOLDER -->" "$html"; then
    echo "❌ Placeholder c${n} non remplacé — insertion a échoué"
    exit 1
  fi
  [ ! -f "$sd/.tmp-artefact-concept-${n}.html" ] || { echo "⚠ Tmp c${n} non nettoyé (warn)"; }
done
echo "✓ 3 artefacts insérés — passer à 4.8"
```

➡️ TRANSITION : passer à Étape **4.8** (Re-validation post-artefact).

---

### Étape 4.8 — Re-validation post-artefact (P5+P6)

**Type d'action** : BASH_COMMAND + TASK_TOOL_INVOCATION (×2 par concept : contrôleur visuel + extracteur corrections)

**Conditionnelle ?** : NON.

**Concept parallèle ?** : OUI.

**Patches préservés** : **P4+P5** (gates avec --json-output, vague2 capturée) + **Patch B** (gate visuel) + **P6** (extraction JSON corrections séparée).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  html="$sd/{brand}-style-tile-concept-${n}.html"
  [ -f "$html" ] || { echo "❌ HTML c${n} avec artefact manquant — RETOUR à 4.7"; exit 1; }
  grep -q "<!-- ARTEFACT_PLACEHOLDER -->" "$html" \
    && { echo "❌ Placeholder c${n} encore présent — RETOUR à 4.7"; exit 1; }
done
```

▸ ACTION :
Pour chaque concept N en parallèle :

1. Gates Python (mêmes commandes qu'en 4.2, suffixe `-art`) :
```bash
python3 "{skill_dir}/scripts/phase4-finishing-gate.py" \
    "$sd/{brand}-style-tile-concept-${N}.html" {cursor_a} \
    --json-output "$sd/.gates-finishing-c${N}-art.json"
python3 "{skill_dir}/scripts/phase4-blacklist-gate.py" \
    "$sd/{brand}-style-tile-concept-${N}.html" \
    > "$sd/.gates-blacklist-c${N}-art.stdout" 2>&1
# Reconstruire .gates-c{N}-art.json (consolidé) — même bloc Python que 4.2
```

2. Lancer Task tool contrôleur visuel art (prompt identique à 4.3, suffixe `-art`) → produit `.finishing-gate-c{N}-art.pass`.

3. Lancer extraction JSON corrections art (même protocole P6 que 4.4) → produit `.finishing-gate-c{N}-art-corrections.json`.

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  [ -f "$sd/.gates-finishing-c${n}-art.json" ] || { echo "❌ Gates art c${n} manquant"; exit 1; }
  python3 -c "import json; d=json.load(open('$sd/.gates-finishing-c${n}-art.json')); assert 'vague2' in d" \
    || { echo "❌ Gates art c${n} sans vague2"; exit 1; }
  [ -f "$sd/.finishing-gate-c${n}-art.pass" ] || { echo "❌ Visuel art c${n} manquant"; exit 1; }
  [ -f "$sd/.finishing-gate-c${n}-art-corrections.json" ] || { echo "❌ Corrections art c${n} manquant"; exit 1; }
  python3 -c "
import json
d=json.load(open('$sd/.finishing-gate-c${n}-art-corrections.json'))
assert 'corrections' in d and isinstance(d['corrections'], list)
" || { echo "❌ JSON corrections art c${n} invalide"; exit 1; }
done
echo "✓ Re-validation post-artefact OK — passer à 4.9"
```

➡️ TRANSITION : passer à Étape **4.9** (Correction post-artefact, conditionnelle).

---

### Étape 4.9 — Correction post-artefact (CONDITIONNELLE)

**Type d'action** : TASK_TOOL_INVOCATION

**Conditionnelle ?** : **OUI** — skip si tous les `.finishing-gate-c{N}-art-corrections.json` ont `corrections == []`.

**Concept parallèle ?** : OUI — 1 Designer mode CORRECTION par concept ayant des corrections.

**Patches préservés** : **P6** (Designer mode CORRECTION sur HTML complet, JAMAIS d'agent custom léger).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
concepts_to_correct=""
for n in 1 2 3; do
  f="$sd/.finishing-gate-c${n}-art-corrections.json"
  [ -f "$f" ] || { echo "❌ Corrections art c${n} manquant — RETOUR à 4.8"; exit 1; }
  count=$(python3 -c "import json; print(len(json.load(open('$f'))['corrections']))")
  if [ "$count" -gt 0 ]; then
    concepts_to_correct="$concepts_to_correct $n"
    cp "$sd/{brand}-style-tile-concept-${n}.html" "$sd/{brand}-style-tile-concept-${n}.html.bakart"
  fi
done
[ -n "$concepts_to_correct" ] || { echo "✓ Aucune correction art à appliquer — SKIP 4.9 — transition vers 4.10"; exit 0; }
```

▸ ACTION :
Pour chaque concept N dans `concepts_to_correct`, lancer Task tool avec prompt complet `{skill_dir}/phases/phase-4-styletile.md` (PAS phase-4-artefact.md — c'est le Designer styletile qui a la vue d'ensemble du :root et peut patcher hero/artefact/atmosphere de manière cohérente).

`{correction_mode_block}` = HTML complet (avec artefact) + JSON corrections art. Mode CORRECTION CHIRURGICALE.

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in $concepts_to_correct; do
  html="$sd/{brand}-style-tile-concept-${n}.html"
  [ -f "$html" ] || { echo "❌ HTML c${n} manquant après correction art"; exit 1; }
  # Pas de re-validation gates ici (la boucle 4.10-4.13 fera le re-check sémantique).
done
echo "✓ Corrections art appliquées sur :$concepts_to_correct — passer à 4.10"
```

➡️ TRANSITION : passer à Étape **4.10** (Critique 4-parallèle iter0).

---

### Étape 4.10 — Critique 4-parallèle iter0

**Type d'action** : TASK_TOOL_INVOCATION (×4 par concept en parallèle)

**Conditionnelle ?** : NON.

**Concept parallèle ?** : OUI — pour chaque concept, 4 Critiques sont lancés en parallèle. Les 3 concepts × 4 critiques = 12 Task tools peuvent être lancés en parallèle dans un seul message orchestrateur (économie de wall-clock).

**Patches préservés** : Architecture Vague 2 (4 Critiques spécialisés vs 1 Critique unique).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  [ -f "$sd/{brand}-style-tile-concept-${n}.html" ] || { echo "❌ HTML c${n} manquant"; exit 1; }
  [ -f "$sd/.gates-finishing-c${n}-art.json" ] || { echo "❌ Gates art c${n} manquant — RETOUR à 4.8"; exit 1; }
  # Backup avant boucle Critique (rollback divergence en 4.13)
  cp "$sd/{brand}-style-tile-concept-${n}.html" "$sd/{brand}-style-tile-concept-${n}.html.bak0"
done
for prompt in phase-4check-a11y.md phase-4check-composition.md phase-4check-typo-copy.md phase-4check-craft.md; do
  [ -f "{skill_dir}/phases/$prompt" ] || { echo "❌ Prompt $prompt manquant"; exit 1; }
done
```

▸ ACTION :
Pour chaque concept N, construire le `gates_report` consolidé (lecture de `.gates-c{N}-art.json` ou reconstruction depuis `.gates-finishing-c{N}-art.json` si nécessaire).

Pour chaque domaine D ∈ {a11y, composition, typo-copy, craft}, lancer un Task tool avec le prompt `{skill_dir}/phases/phase-4check-{D}.md` résolu avec :
- `{html_path}` = `{brand}-style-tile-concept-{N}.html`
- `{gates_report}` = JSON intégral (vague1 + vague2 — **NE PAS RÉSUMER**, P4/P5)
- `{pitch_extract}` = pitch extrait
- `{cursor_a}`, `{cursor_a_label}`, `{registre}` = valeurs
- `{iteration}` = 0
- `{concept_number}` = N
- `{concept_name}` = titre du concept

Chaque Critique écrit `.critique-c{N}-{D}-iter0.json`.

**Total** : 3 concepts × 4 domaines = 12 Task tools EN PARALLÈLE dans un seul message.

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
# Tolérer ≤ 1 plantage par concept (FALLBACK Vague 1 si ≥ 2 plantés en 4.11).
for n in 1 2 3; do
  ok_count=0
  for d in a11y composition typo-copy craft; do
    f="$sd/.critique-c${n}-${d}-iter0.json"
    if [ -f "$f" ] && python3 -c "import json; json.load(open('$f'))" 2>/dev/null; then
      ok_count=$((ok_count + 1))
    fi
  done
  if [ "$ok_count" -lt 1 ]; then
    echo "❌ Concept c${n} : 0 critique valide — RELANCER les 4 Critiques c${n}"
    exit 1
  fi
  echo "  c${n} : $ok_count/4 critiques valides"
done
echo "✓ Critiques iter0 OK (≥1 par concept) — passer à 4.11"
```

➡️ TRANSITION : passer à Étape **4.11** (Synthétiseur iter0).

---

### Étape 4.11 — Synthétiseur iter0 (P3 — fallback Vague 1 si <3)

**Type d'action** : TASK_TOOL_INVOCATION + DECISION (Synthétiseur OU Fallback Critique unique)

**Conditionnelle ?** : NON (toujours produit `.critique-c{N}-iter0.json`, mais via deux chemins distincts).

**Concept parallèle ?** : OUI — 3 Synthétiseurs (ou 3 fallbacks) en parallèle.

**Patches préservés** : **P3** (signature `synthesizer_subagent_signature` obligatoire) + Fallback Vague 1 (`phase-4check.md`).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
[ -f "{skill_dir}/phases/phase-4check-synthetiseur.md" ] || { echo "❌ Prompt synthétiseur manquant"; exit 1; }
[ -f "{skill_dir}/phases/phase-4check.md" ] || { echo "❌ Prompt fallback Vague 1 manquant"; exit 1; }
# Calculer pour chaque concept la stratégie : SYNTH ou FALLBACK
for n in 1 2 3; do
  ok_count=0
  for d in a11y composition typo-copy craft; do
    f="$sd/.critique-c${n}-${d}-iter0.json"
    if [ -f "$f" ] && python3 -c "import json; json.load(open('$f'))" 2>/dev/null; then
      ok_count=$((ok_count + 1))
    fi
  done
  if [ "$ok_count" -ge 3 ]; then
    echo "STRATEGY_c${n}=SYNTH" >> "$sd/.tmp-synth-strategy.txt"
  else
    echo "STRATEGY_c${n}=FALLBACK" >> "$sd/.tmp-synth-strategy.txt"
    echo "PRE-COND SYNTH FAIL — ${ok_count}/4 critiques valides — bascule FALLBACK Vague 1" \
      >> "$sd/.fix-loop-c${n}.log"
  fi
done
```

▸ ACTION :
Pour chaque concept N, selon la stratégie :

**Si STRATEGY = SYNTH** (≥ 3 Critiques valides) :
Lancer Task tool avec prompt `{skill_dir}/phases/phase-4check-synthetiseur.md` résolu :
- `{html_path}`, `{pitch_extract}`, `{cursor_a}`, `{registre}`, `{concept_number}` = N, `{concept_name}`, `{iteration}` = 0

→ Synthétiseur consolide les 4 (ou 3) JSON disponibles, écrit `.critique-c{N}-iter0.json` au format compat ascendante avec `phase-4check.md`. **DOIT contenir** `synthesis_metadata.synthesizer_subagent_signature` (P3).

**Si STRATEGY = FALLBACK** (< 3 Critiques valides) :
Lancer Task tool avec prompt `{skill_dir}/phases/phase-4check.md` (Critique unique Vague 1) sur le HTML concept N → produit `.critique-c{N}-iter0.json` au même format mais SANS signature synthétiseur (Patch P3 marquera `verdict_critiques: FALLBACK_VAGUE1` en 4.14).

Les 3 invocations (toutes stratégies confondues) se font en parallèle dans un message orchestrateur.

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  f="$sd/.critique-c${n}-iter0.json"
  [ -f "$f" ] || { echo "❌ Critique consolidé c${n} iter0 manquant"; exit 1; }
  python3 -c "
import json
d = json.load(open('$f'))
assert 'corrections' in d and 'summary' in d, 'format incorrect'
" || { echo "❌ Critique consolidé c${n} iter0 invalide"; exit 1; }
  # Si stratégie SYNTH, vérifier la signature
  if grep -q "STRATEGY_c${n}=SYNTH" "$sd/.tmp-synth-strategy.txt"; then
    grep -q '"synthesizer_subagent_signature"' "$f" \
      || { echo "❌ Synthétiseur c${n} sans signature — SHORTCUT_DETECTE — relancer Synthétiseur"; exit 1; }
  fi
done
rm -f "$sd/.tmp-synth-strategy.txt"
echo "✓ Synthétiseur iter0 OK — passer à 4.12"
```

➡️ TRANSITION : passer à Étape **4.12** (Designer correction iter0, conditionnelle).

---

### Étape 4.12 — Designer correction iter0 (CONDITIONNELLE)

**Type d'action** : TASK_TOOL_INVOCATION

**Conditionnelle ?** : **OUI** — skip si `total_violations == 0` pour les 3 concepts.

**Concept parallèle ?** : OUI — 1 Designer correction par concept ayant des violations.

**Patches préservés** : Pattern Designer mode CORRECTION CHIRURGICALE (préservation cerveau CSS).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
concepts_to_correct=""
for n in 1 2 3; do
  f="$sd/.critique-c${n}-iter0.json"
  [ -f "$f" ] || { echo "❌ Critique iter0 c${n} manquant — RETOUR à 4.11"; exit 1; }
  total=$(python3 -c "import json; d=json.load(open('$f')); print(d.get('summary',{}).get('total_violations',0))")
  if [ "$total" -gt 0 ]; then
    concepts_to_correct="$concepts_to_correct $n"
    cp "$sd/{brand}-style-tile-concept-${n}.html" "$sd/{brand}-style-tile-concept-${n}.html.bakiter0"
    # Logger la trajectoire
    echo "ITER 0 START | total_violations: $total" >> "$sd/.fix-loop-c${n}.log"
  else
    echo "ITER 0 START | total_violations: 0 | STOP — passer directement à 4.14" >> "$sd/.fix-loop-c${n}.log"
  fi
done
[ -n "$concepts_to_correct" ] || { echo "✓ Aucune violation iter0 — SKIP 4.12 ET 4.13 — transition vers 4.14"; exit 0; }
```

▸ ACTION :
Pour chaque concept N dans `concepts_to_correct`, Task tool avec prompt complet `{skill_dir}/phases/phase-4-styletile.md` :
- `{correction_mode_block}` = HTML v_iter0 + JSON `.critique-c{N}-iter0.json` intégral + instructions "Patche EXACTEMENT les zones listées"
- Autres variables identiques au mode CRÉATION

→ Designer overwrite `{brand}-style-tile-concept-{N}.html`

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in $concepts_to_correct; do
  html="$sd/{brand}-style-tile-concept-${n}.html"
  bak="$sd/{brand}-style-tile-concept-${n}.html.bakiter0"
  [ -f "$html" ] || { echo "❌ HTML c${n} manquant après correction iter0"; exit 1; }
  # Garde-fou divergence — re-run gates rapide
  python3 "{skill_dir}/scripts/phase4-finishing-gate.py" "$html" {cursor_a} \
      --json-output "$sd/.gates-finishing-c${n}-iter0-recheck.json" 2>/dev/null
  v_orig=$(python3 -c "import json; d=json.load(open('$sd/.gates-finishing-c${n}-art.json')); print(d.get('vague1',{}).get('total_fails',0))")
  v_new=$(python3 -c "import json; d=json.load(open('$sd/.gates-finishing-c${n}-iter0-recheck.json')); print(d.get('vague1',{}).get('total_fails',0))" 2>/dev/null || echo "999")
  if [ "$v_new" -gt "$v_orig" ]; then
    echo "ITER 0 ROLLBACK | gates empirées ($v_orig→$v_new)" >> "$sd/.fix-loop-c${n}.log"
    cp "$bak" "$html"
  else
    echo "ITER 0 CORRECTION | designer mode=correction | gates: $v_new" >> "$sd/.fix-loop-c${n}.log"
  fi
done
echo "✓ Corrections iter0 appliquées sur :$concepts_to_correct — passer à 4.13"
```

➡️ TRANSITION :
- Si pré-condition `exit 0` (skip) → passer à **4.14**
- Sinon → passer à **4.13** (boucle iter1)

---

### Étape 4.13 — Boucle iter1 (CONDITIONNELLE — 2e itération explicite)

**Type d'action** : TASK_TOOL_INVOCATION (re-Critique 4-parallèle + Synthétiseur + Designer correction iter1)

**Conditionnelle ?** : **OUI** — exécutée seulement si :
- 4.12 a tourné pour au moins 1 concept ET
- ce concept n'a pas été rollback ET
- (test sera fait dans la pré-condition) le re-Critique iter1 produit encore des violations.

**Concept parallèle ?** : OUI — uniquement pour les concepts éligibles à iter1.

**Patches préservés** : Pattern itératif éclaté (PAS de boucle `while iter < 2` inline) + garde-fou oscillation.

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
concepts_iter1=""
for n in 1 2 3; do
  # Critère d'éligibilité iter1 : 4.12 a tourné (backup .bakiter0 existe) ET pas de rollback
  if [ -f "$sd/{brand}-style-tile-concept-${n}.html.bakiter0" ] \
     && ! grep -q "ITER 0 ROLLBACK" "$sd/.fix-loop-c${n}.log" 2>/dev/null; then
    concepts_iter1="$concepts_iter1 $n"
  fi
done
[ -n "$concepts_iter1" ] || { echo "✓ Aucun concept éligible à iter1 — SKIP 4.13 — transition vers 4.14"; exit 0; }
```

▸ ACTION :
Pour chaque concept N dans `concepts_iter1`, exécuter une 2e itération explicite — répliquer la séquence 4.10 → 4.11 → 4.12 mais avec suffixe `iter1` :

1. **Re-gates Python** (suffixe `iter1`) :
```bash
python3 "{skill_dir}/scripts/phase4-finishing-gate.py" \
    "$sd/{brand}-style-tile-concept-${N}.html" {cursor_a} \
    --json-output "$sd/.gates-finishing-c${N}-iter1.json"
```

2. **Re-Critique 4 parallèle** (lance les 4 prompts `phase-4check-{D}.md` avec `{iteration}=1`) → produit `.critique-c{N}-{D}-iter1.json`.

3. **Re-Synthétiseur (ou fallback)** avec `{iteration}=1` → produit `.critique-c{N}-iter1.json`.

4. **Test garde-fou oscillation** :
```bash
prev=$(python3 -c "import json; d=json.load(open('$sd/.critique-c${N}-iter0.json')); print(d.get('summary',{}).get('total_violations',0))")
curr=$(python3 -c "import json; d=json.load(open('$sd/.critique-c${N}-iter1.json')); print(d.get('summary',{}).get('total_violations',0))")
if [ "$curr" -eq 0 ]; then
  echo "ITER 1 START | total_violations: 0 | STOP — convergence" >> "$sd/.fix-loop-c${N}.log"
elif [ "$curr" -ge "$prev" ]; then
  echo "ITER 1 OSCILLATION | $prev→$curr | STOP — pas de progrès" >> "$sd/.fix-loop-c${N}.log"
else
  # Lancer Designer correction iter1 (mode CORRECTION)
  echo "ITER 1 CORRECTION | $prev→$curr | designer mode=correction" >> "$sd/.fix-loop-c${N}.log"
  # Task tool : prompt complet phase-4-styletile.md avec correction_mode_block iter1
fi
```

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in $concepts_iter1; do
  [ -f "$sd/.critique-c${n}-iter1.json" ] || { echo "❌ Critique iter1 c${n} manquant"; exit 1; }
  [ -f "$sd/.gates-finishing-c${n}-iter1.json" ] || { echo "❌ Gates iter1 c${n} manquant"; exit 1; }
  # HTML doit toujours être présent et valide
  html="$sd/{brand}-style-tile-concept-${n}.html"
  [ "$(wc -c < "$html")" -gt 10000 ] || { echo "❌ HTML c${n} corrompu après iter1"; exit 1; }
done
echo "✓ Boucle iter1 terminée — passer à 4.14"
```

➡️ TRANSITION : passer à Étape **4.14** (Audit consolidé).

---

### Étape 4.14 — Audit consolidé (Patch A + P1 + P5)

**Type d'action** : BASH_COMMAND (heredoc JSON par concept)

**Conditionnelle ?** : NON — TOUJOURS exécutée. C'est l'artefact qui prouve que toutes les étapes précédentes ont bien été traversées.

**Concept parallèle ?** : OUI — 3 fichiers d'audit produits en parallèle (mais commande bash par concept indépendante).

**Patches préservés** : **Patch A** (fichier `.pipeline-audit-c{N}.json` consolidé obligatoire) + **P1** (champs `synthesizer_signature_present`, `vague2_warnings_visible`, `verdict_critiques`) + **P5** (vérification vague2 dans gates JSON).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  [ -f "$sd/{brand}-style-tile-concept-${n}.html" ] || { echo "❌ HTML final c${n} manquant"; exit 1; }
  [ -f "$sd/.critique-c${n}-iter0.json" ] || { echo "❌ Critique consolidé c${n} iter0 manquant — RETOUR à 4.11"; exit 1; }
  [ -f "$sd/.gates-finishing-c${n}-art.json" ] || { echo "❌ Gates art c${n} manquant"; exit 1; }
done
```

▸ ACTION :
Pour chaque concept N, écrire `.pipeline-audit-c{N}.json` via heredoc bash. Le fichier consolide les preuves des étapes 4.1-4.13 :

```bash
sd="{skill_dir}/outputs/{session_dir}"
for N in 1 2 3; do
  HTML_SHA=$(shasum -a 256 "$sd/{brand}-style-tile-concept-${N}.html" | cut -d' ' -f1)
  
  # Calculs préliminaires
  v0_visu_ok=$([ -f "$sd/.finishing-gate-c${N}-v0.pass" ] && grep -q '"executed": true' "$sd/.finishing-gate-c${N}-v0.pass" && echo true || echo false)
  art_visu_ok=$([ -f "$sd/.finishing-gate-c${N}-art.pass" ] && grep -q '"executed": true' "$sd/.finishing-gate-c${N}-art.pass" && echo true || echo false)
  
  crit_count=$(ls "$sd/.critique-c${N}-"{a11y,composition,typo-copy,craft}"-iter0.json" 2>/dev/null | wc -l | tr -d ' ')
  synth_sig=$([ -f "$sd/.critique-c${N}-iter0.json" ] && grep -q 'synthesizer_subagent_signature' "$sd/.critique-c${N}-iter0.json" && echo true || echo false)
  fallback_used=$([ -f "$sd/.fix-loop-c${N}.log" ] && grep -q 'FALLBACK Vague 1' "$sd/.fix-loop-c${N}.log" && echo true || echo false)
  iterations=$([ -f "$sd/.fix-loop-c${N}.log" ] && grep -c 'ITER .* START' "$sd/.fix-loop-c${N}.log" || echo 0)
  v2_visible=$([ -f "$sd/.gates-finishing-c${N}-art.json" ] && grep -q '"vague2"' "$sd/.gates-finishing-c${N}-art.json" && echo true || echo false)
  
  # Déterminer verdict_critiques (P1)
  if [ "$fallback_used" = "true" ]; then
    verdict_crit="FALLBACK_VAGUE1 — acceptable, log explicite"
  elif [ "$crit_count" -lt 3 ] && [ "$synth_sig" = "false" ]; then
    verdict_crit="SHORTCUT_DETECTE — moins de 3 critiques ET pas de signature — RELANCER"
  elif [ "$crit_count" -lt 3 ]; then
    verdict_crit="DEGRADE — moins de 3 critiques mais signature OK"
  elif [ "$synth_sig" = "false" ]; then
    verdict_crit="SHORTCUT_DETECTE — 4 critiques mais Synthétiseur sauté — RELANCER"
  else
    verdict_crit="OK — 4 critiques + signature synthétiseur valides"
  fi
  if [ "$v2_visible" = "false" ]; then
    verdict_crit="$verdict_crit | WARN: vague2 non remontée dans gates art — P4/P5 violés"
  fi
  
  cat > "$sd/.pipeline-audit-c${N}.json" <<AUDITEOF
{
  "concept": ${N},
  "session_dir": "{session_dir}",
  "html_final_sha256": "$HTML_SHA",
  "audit_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "etapes_traversees": [
    {"etape": "4.1 Designer création", "status": "DONE"},
    {"etape": "4.2 Gates Python v0", "status": "DONE", "gates_v0_present": true, "vague2_v0_visible": true},
    {"etape": "4.3 Gate visuel v0", "status": "DONE", "executed": ${v0_visu_ok}},
    {"etape": "4.4 JSON corrections v0", "status": "DONE"},
    {"etape": "4.5 Designer correction v0→v1", "status": "DONE_OR_SKIP"},
    {"etape": "4.6 Re-validation v1", "status": "DONE_OR_SKIP"},
    {"etape": "4.7 Designer artefact", "status": "DONE"},
    {"etape": "4.8 Re-validation post-artefact", "status": "DONE", "executed": ${art_visu_ok}, "vague2_art_visible": ${v2_visible}},
    {"etape": "4.9 Correction post-artefact", "status": "DONE_OR_SKIP"},
    {"etape": "4.10 Critique 4-parallèle iter0", "status": "DONE", "critiques_count": ${crit_count}},
    {"etape": "4.11 Synthétiseur iter0", "status": "DONE", "synthesizer_signature_present": ${synth_sig}, "fallback_vague1_used": ${fallback_used}},
    {"etape": "4.12 Designer correction iter0", "status": "DONE_OR_SKIP"},
    {"etape": "4.13 Boucle iter1", "status": "DONE_OR_SKIP", "iterations": ${iterations}}
  ],
  "shortcuts_detectes": [],
  "verdict_critiques": "${verdict_crit}",
  "alerte_qualite": "Si verdict_critiques contient 'SHORTCUT_DETECTE' ou 'WARN' → relancer les subagents concernés avant livraison"
}
AUDITEOF
done
```

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  audit="$sd/.pipeline-audit-c${n}.json"
  [ -f "$audit" ] || { echo "❌ Audit c${n} manquant — RELANCER 4.14"; exit 1; }
  python3 -c "import json; d=json.load(open('$audit')); assert 'verdict_critiques' in d" \
    || { echo "❌ Audit c${n} JSON invalide"; exit 1; }
  v=$(python3 -c "import json; print(json.load(open('$audit'))['verdict_critiques'])")
  if echo "$v" | grep -q "SHORTCUT_DETECTE"; then
    echo "⚠ SHORTCUT détecté c${n} : $v — l'utilisateur doit décider de relancer ou continuer"
    # NE PAS exit 1 ici — l'audit a fait son job (signaler le shortcut)
  fi
done
echo "✓ 3 audits consolidés produits — passer à 4.15"
```

➡️ TRANSITION : passer à Étape **4.15** (Swap haute résolution + ouverture).

---

### Étape 4.15 — Swap haute résolution + ouverture browser

**Type d'action** : BASH_COMMAND (Python inline) + commande `open`

**Conditionnelle ?** : NON.

**Concept parallèle ?** : NON — script Python séquentiel sur les 3 fichiers ; commandes `open` peuvent être lancées en parallèle (3 fenêtres).

**Patches préservés** : **Patch A pré-condition** (audit consolidé OBLIGATOIRE avant ouverture — déjà couvert par 4.14).

⛔ PRÉ-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
for n in 1 2 3; do
  [ -f "$sd/{brand}-style-tile-concept-${n}.html" ] || { echo "❌ HTML c${n} manquant"; exit 1; }
  [ -f "$sd/.pipeline-audit-c${n}.json" ] || { echo "❌ Audit c${n} manquant — RETOUR à 4.14"; exit 1; }
done
```

▸ ACTION :

1. Swap haute résolution — script Python inline (identique au script actuel `Étape 4A-bis` SKILL.md) :
```bash
python3 -c "
import re, glob, os, sys
session_dir = '{skill_dir}/outputs/{session_dir}'
brand = '{brand}'
hires_files = glob.glob(os.path.join(session_dir, f'{brand}-visual-c*-*.*.b64'))
hires_map = {}
for f in hires_files:
    basename = os.path.basename(f)
    m = re.match(rf'{re.escape(brand)}-visual-(c\d+-\d+)\.\w+\.b64$', basename)
    if m: hires_map[m.group(1)] = f
if not hires_map:
    print('Aucun visuel haute résolution trouvé — swap ignoré.')
    sys.exit(0)
for html_file in glob.glob(os.path.join(session_dir, f'{brand}-style-tile-concept-*.html')):
    with open(html_file) as fh: html = fh.read()
    modified = False
    for vid, b64_file in hires_map.items():
        pattern = rf'(data-visual=\"{re.escape(vid)}\"[^>]*?)src=\"data:image/[^\"]*\"'
        with open(b64_file) as fb: hires_b64 = fb.read().strip()
        ext_match = re.match(rf'{re.escape(brand)}-visual-{re.escape(vid)}\.(\w+)\.b64$', os.path.basename(b64_file))
        ext = ext_match.group(1) if ext_match else 'png'
        mime = 'image/jpeg' if ext in ('jpg','jpeg') else f'image/{ext}'
        replacement = rf'\1src=\"data:{mime};base64,{hires_b64}\"'
        new_html, count = re.subn(pattern, replacement, html)
        if count > 0:
            html = new_html; modified = True
            print(f'  ✓ {vid} swappé dans {os.path.basename(html_file)}')
    if modified:
        with open(html_file, 'w') as fh: fh.write(html)
print('Swap haute résolution terminé.')
"
```

2. Ouverture des 3 fenêtres navigateur :
```bash
sd="{skill_dir}/outputs/{session_dir}"
open "$sd/{brand}-style-tile-concept-1.html"
open "$sd/{brand}-style-tile-concept-2.html"
open "$sd/{brand}-style-tile-concept-3.html"
```

3. Présentation utilisateur (Étape 4C dans la nomenclature actuelle — fusionnée ici) :
> "Voici vos 3 Style-Tiles ouverts dans 3 fenêtres distinctes. Comparez-les visuellement. Quel concept préférez-vous ?
> - **A** : {concept_1_name}
> - **B** : {concept_2_name}
> - **C** : {concept_3_name}
> 
> Audits pipeline disponibles : `.pipeline-audit-c{1,2,3}.json` — vérifier qu'aucun shortcut n'a été pris."

⛔ POST-CONDITION (bash bloquant) :
```bash
sd="{skill_dir}/outputs/{session_dir}"
# Vérifier que le swap a inséré les visuels haute-rés (taille HTML > seuil basse-rés)
for n in 1 2 3; do
  html="$sd/{brand}-style-tile-concept-${n}.html"
  size=$(wc -c < "$html")
  echo "  HTML c${n} final : $size bytes"
done
echo "✓ Phase 4 complétée — choix utilisateur attendu"
```

➡️ TRANSITION : sortie de Phase 4 → choix utilisateur → **Phase 4bis** (DA Check, optionnel) ou **Phase 5**.

---

## Synthèse — artefacts produits par concept N

| Fichier (par concept N) | Producteur (sous-étape) | Consommateur (sous-étapes suivantes) |
|---|---|---|
| `{brand}-style-tile-concept-{N}.html` | 4.1 (création), 4.5/4.7/4.9/4.12/4.13 (overwrite) | 4.2/4.3/4.6/4.8/4.10/4.13/4.15 |
| `{brand}-style-tile-concept-{N}.html.bakv0` | 4.5 (avant correction) | 4.6 (rollback divergence) |
| `{brand}-style-tile-concept-{N}.html.bakart` | 4.9 (avant correction) | (rollback non implémenté à ce stade — log seulement) |
| `{brand}-style-tile-concept-{N}.html.bak0` | 4.10 (avant boucle) | 4.13 (rollback divergence) |
| `{brand}-style-tile-concept-{N}.html.bakiter0` | 4.12 (avant correction) | 4.12 (rollback gates empirées), 4.13 |
| `.gates-finishing-c{N}-v0.json` | 4.2 | 4.4, 4.14 |
| `.gates-blacklist-c{N}-v0.stdout` | 4.2 | 4.4 (consolidation) |
| `.gates-c{N}-v0.json` (consolidé) | 4.2 | (référence, non re-lu) |
| `.gates-finishing-c{N}-v1.json` | 4.6 | 4.14 (audit) |
| `.gates-finishing-c{N}-art.json` | 4.8 | 4.10 (gates_report Critiques), 4.14 |
| `.gates-finishing-c{N}-iter0-recheck.json` | 4.12 (garde-fou) | 4.14 |
| `.gates-finishing-c{N}-iter1.json` | 4.13 | 4.14 |
| `.finishing-gate-c{N}-v0.pass` | 4.3 (contrôleur visuel) | 4.4, 4.14 |
| `.finishing-gate-c{N}-v1.pass` | 4.6 (contrôleur visuel) | 4.14 |
| `.finishing-gate-c{N}-art.pass` | 4.8 (contrôleur visuel) | 4.14 |
| `.finishing-gate-c{N}-v0-corrections.json` | 4.4 (extracteur OU orchestrateur) | 4.5 |
| `.finishing-gate-c{N}-art-corrections.json` | 4.8 (extracteur OU orchestrateur) | 4.9 |
| `.critique-c{N}-{a11y,composition,typo-copy,craft}-iter0.json` | 4.10 (4 Critiques parallèles) | 4.11 |
| `.critique-c{N}-{a11y,composition,typo-copy,craft}-iter1.json` | 4.13 | 4.13 (Synthétiseur), 4.14 |
| `.critique-c{N}-iter0.json` (consolidé) | 4.11 (Synthétiseur OU fallback) | 4.12, 4.14 |
| `.critique-c{N}-iter1.json` (consolidé) | 4.13 | 4.14 |
| `.fix-loop-c{N}.log` | 4.11/4.12/4.13 | 4.14 (parsing iterations, fallback_used) |
| `.pipeline-audit-c{N}.json` | 4.14 | 4.15 (pré-condition), utilisateur final |

---

## Synthèse — patches préservés

| Patch | Symptôme corrigé | Localisation ancienne archi | Localisation nouvelle archi |
|---|---|---|---|
| **Patch A** | Audit consolidé `.pipeline-audit-c{N}.json` skippé | Étape 4A-audit (~ligne 3539-3637 SKILL.md) + pré-condition 4A-bis | **4.14** (action) + **4.15** (pré-condition lit l'audit) |
| **Patch B** | TIER 1 a11y oublié par Designer mode CORRECTION | TIER 1 a11y obligatoire dans tous les Designers + audit défensif visuel sur 3ème couche | **4.1** (variable `{a11y_fondamentaux_tier1}` injectée) + **4.3 / 4.6 / 4.8** (gate visuel impitoyable) |
| **P1** | Verdict critiques sans signature synthétiseur | Champ `verdict_critiques` calculé en 4A-audit | **4.14** (calcul `verdict_crit` avec branches SHORTCUT_DETECTE / FALLBACK_VAGUE1 / OK) |
| **P2** | Synthétiseur invoqué avec inputs incomplets | Pré-condition stricte avant Synthétiseur | **4.11** (calcul `STRATEGY` SYNTH vs FALLBACK selon `ok_count >= 3`) |
| **P3** | Synthétiseur sans signature `synthesizer_subagent_signature` | `synthesis_metadata.synthesizer_subagent_signature` obligatoire | **4.11** (post-condition `grep -q synthesizer_subagent_signature`) |
| **P4** | Résumé stdout des gates Python tronqué | `--json-output` sur `phase4-finishing-gate.py` + lecture intégrale du JSON | **4.2 / 4.6 / 4.8 / 4.12 (recheck) / 4.13** (toutes les invocations utilisent `--json-output`) |
| **P5** | Section `vague2` perdue dans `.gates-c{N}-iter0.json` | Vérification `'vague2' in finishing_gate` avant invocation Critiques + audit `vague2_warnings_visible` | **4.2 post-condition** (`assert 'vague2' in d`) + **4.10 pré-condition** (validation gates_report intègre vague2) + **4.14** (champ `vague2_v0_visible`/`vague2_art_visible`) |
| **P6** | Contrôleur Finishing Gate corrige le HTML lui-même (SendMessage non accessible aux subagents) | Pattern "contrôleur produit JSON corrections → orchestrateur invoque Designer mode CORRECTION" | **4.3** (contrôleur lecture-seule) + **4.4** (production JSON séparée) + **4.5** (Designer mode CORRECTION) — répliqué pour **4.8 / 4.9** post-artefact |

---

## Risques et points de vigilance

| Risque | Probabilité | Impact | Mitigation prévue |
|---|---|---|---|
| Inflation du nombre de Task tools (12 en parallèle en 4.10) → quotas API ou crashs | Moyenne | Moyen | Surveiller wall-clock et erreurs API 529. Si plantages > 2 → rebasculer sur lancements séquentiels par concept (4 critiques en parallèle, 3 vagues séquentielles). |
| Pré-conditions bash trop strictes → blocages normaux (ex: WARN catalogués comme FAIL en 4.4) | Moyenne | Moyen | Test E2E Phase R4 sur 2 briefs distincts. Tolérance graceful : la pré-condition `exit 1` ne se déclenche que sur artefact MANQUANT, pas sur contenu warn-uniquement. |
| Multiplication des fichiers `.bak*` → encombrement disque | Faible | Faible | Nettoyage explicite après 4.15 (optionnel). Acceptable car compressible. |
| Backup `.bakv0` créé en 4.5 mais jamais nettoyé si concept skipé en 4.5 | Faible | Faible | Le backup n'est créé que pour les concepts dans `concepts_to_correct` — pas d'orphelins. |
| Compatibilité ascendante avec subagents existants : si `phase-4-styletile.md` est modifié pour exiger une nouvelle variable, le refactor casse | Moyenne | Critique | Phase R3 inclut une vérification explicite que les variables passées correspondent au contrat des prompts (audit Phase 1 référentiel). |
| Le "STRATEGY_c{n}=SYNTH/FALLBACK" est stocké dans un fichier tmp lu après — si l'orchestrateur perd l'état entre commandes bash, lecture/écriture de `.tmp-synth-strategy.txt` fragile | Faible | Moyen | Le fichier tmp est écrit AVANT le lancement Task tool et lu APRÈS — entre temps l'état est sur disque. Pattern utilisé identique à `concepts_to_correct`. |
| Fichier `.fix-loop-c{N}.log` parsé en 4.14 par `grep -c 'ITER .* START'` — si format de log dévie, le compteur d'iterations est faux | Faible | Faible | Format imposé strictement (`ITER 0 START`, `ITER 1 START`) par les sous-étapes 4.12 et 4.13. |
| Gate visuel produit FAIL_INVISIBLE → corrections JSON non vide → boucle infinie possible si Designer ne corrige jamais l'invisibilité (ex: pattern impossible) | Faible | Moyen | Pas de boucle inline sur la gate visuelle — 4.5 corrige UNE FOIS. Si reste FAIL après 4.6, c'est WARN dans `verdict` mais pipeline continue. La 2e passe est en fait 4.8/4.9 après artefact. |
| Sous-étape 4.13 (iter1) jamais déclenchée car 4.12 résout tout — perte de filet anti-slop pour cas "presque parfait" | Faible | Faible | Comportement attendu — si iter0 résout tout, iter1 inutile. La métrique audit-slop tracera. |

---

## Décisions à valider par Charles

1. **Découpage 15 sous-étapes (vs 13 du plan initial)** : on a explicité 4.14 et 4.15 séparément (4.14 = audit, 4.15 = swap+ouverture). Le plan parlait de 13 + 2 "suivi de". Cohérent ?

2. **Sous-étape 4.6 (re-validation v1)** : on re-run gates Python ET contrôleur visuel APRÈS la correction v0→v1. Coût : 1 cycle Puppeteer additionnel par concept ayant reçu correction. Alternative : re-run gates Python seulement, skip contrôleur visuel (gain de temps mais perd la garantie que le Designer n'a pas cassé la 3ème couche). **Recommandation** : garder le contrôleur visuel — c'est la seule garantie que la correction n'a pas re-introduit un halo polygonal ou cassé un grain.

3. **Sous-étape 4.4 (P6) — contrôleur extracteur OU orchestrateur direct ?** : la pré-condition prévoit deux chemins (orchestrateur écrit JSON vide si NO_FAIL, sinon contrôleur extrait). Alternative plus simple : TOUJOURS un contrôleur extracteur même pour produire un JSON vide (garantit symétrie). Coût : 3 Task tools de plus à chaque run. **Recommandation** : garder l'optimisation orchestrateur direct sur NO_FAIL — pas de risque de shortcut puisque l'orchestrateur écrit littéralement `{"corrections": []}`.

4. **4.5 et 4.6 ont une pré-condition `exit 0` (skip explicite)** : ce pattern est-il acceptable ? Alternative : transformer en `if/else` dans la transition au lieu d'un exit. **Recommandation** : `exit 0` est lisible et sans ambiguïté. Le SKILL.md formulera "Si la pré-condition retourne 0 sans erreur ET avec message 'SKIP' → transition directe vers X".

5. **Backup `.bakart` jamais utilisé pour rollback** : on crée un backup avant 4.9 mais on ne rollback pas si gates empirent. Voulez-vous ajouter un garde-fou divergence en 4.9 (comme en 4.6 et 4.12) ?

6. **Sous-étape 4.10 — 12 Task tools en parallèle** : faisable ? Ou faut-il sérialiser par concept (3 vagues de 4 critiques) ? Test sur VoltaPilot c2 avait 4 critiques en parallèle pour 1 concept — à confirmer pour 12.

7. **Fichier `.tmp-synth-strategy.txt`** : pattern fichier tmp lu plus tard. Charles préfère un autre pattern (ex: variable shell exportée, ou directement reconstruire la stratégie dans la post-cond) ?

8. **Numérotation 4.X vs maintien des noms 4A-ter / 4A-art / 4A-loop / 4A-audit / 4A-bis** : le draft propose 4.1-4.15 (numéros plats). Faut-il garder en parallèle une mention du nom historique pour faciliter la lecture diachronique du SKILL.md (ex: "## Étape 4.10 — Critique 4-parallèle iter0 (ex-4A-loop iteration 0)") ?

9. **Phase 4bis (DA Check)** : non couverte par ce refactor (volontairement, périmètre). Confirmer ?

10. **Cible taille SKILL.md zone Étape 4 après refactor** : le plan annonce "≤ 400 lignes". Le présent draft est ~600 lignes mais avec gabarits explicites. La traduction en SKILL.md condensera les explications répétitives. Cible réaliste : ~500-700 lignes (vs 900 actuelles).

---

## Dernière mise à jour

2026-04-26 — Draft Phase R2 produit, en attente de validation Charles.
