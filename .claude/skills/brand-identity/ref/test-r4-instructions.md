# Instructions Test E2E — Validation Vague 2.5 (4 patches structurels)

> **À lire intégralement avant de commencer.** Ce test valide 4 patches appliqués au pipeline BIG Phase 4 le 2026-04-27 pour corriger une régression observée la veille (audit-slop 6.0/10, BIG Pipeline 3.0/10 sur VoltaPilot c2).

---

## Contexte (à lire en début de session vierge)

> Le pipeline BIG Phase 4 vient d'être patché (Vague 2.5 corrective) avec 4 patches structurels :
>
> - **P3** : Anti-régression rollback Designer correction étendu à la sous-étape 4.5 (en plus de 4.9 et 4.12 qui l'avaient déjà)
> - **P3-bis** : Fix d'un bug latent (`total_fails` → `fail_count`) qui empêchait le rollback de fonctionner en 4.6/4.9/4.13 — donc le rollback est maintenant ACTIF partout
> - **P4** : Standardisation des conventions de nommage des backups HTML (4 conventions chaotiques → 4 noms cohérents auto-explicatifs). Fixe le bug `.bakiter0` qui faisait skipper l'iter1.
> - **P7** : 3 pauses utilisateur insérées (4.1bis, 4.7bis, 4.12bis) pour reprendre le contrôle aux moments clés du pipeline
> - **P8** : Forcer les 4 Critiques en VRAI parallèle (directive "même message orchestrateur" + détection wall-clock du shortcut)
>
> Ce test valide :
> - Que toutes les sous-étapes (4.1 → 4.15 + 3 bis) s'exécutent dans l'ordre
> - Que les 3 pauses utilisateur déclenchent l'attente
> - Que les 4 Critiques tournent en parallèle (wall-clock < 8 min entre 1er et dernier)
> - Que le rollback Designer correction se déclenche si nécessaire
> - Que le score audit-slop remonte à ≥ 7.5/10 (cible 8.0+) et BIG Pipeline ≥ 7/10
>
> **Brief de test** : VoltaPilot c2 ("Le Pouls Profond"), Cabinet de Praticien Nocturne, Curseur A=3 × B=2.
> **Run partial** : c2 uniquement (la détection dynamique va calculer `CONCEPTS=[2]` automatiquement).

---

## Étape 1 — Cloner la session de référence

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M)
SOURCE="/Users/charlesbezard/Library/CloudStorage/GoogleDrive-charles.bezard@gmail.com/Mon Drive/Claude Code/Brand Identity Generator/.claude/skills/brand-identity/outputs/test-voltapilot-test-20260426-1841"
TARGET="/Users/charlesbezard/Library/CloudStorage/GoogleDrive-charles.bezard@gmail.com/Mon Drive/Claude Code/Brand Identity Generator/.claude/skills/brand-identity/outputs/test-voltapilot-vague2.5-${TIMESTAMP}"
cp -r "$SOURCE" "$TARGET"
echo "✓ Session clonée : $(basename $TARGET)"
echo "Path complet : $TARGET"
```

**📌 NOTE** le nom exact du dossier (`test-voltapilot-vague2.5-{TIMESTAMP}`) — tu en auras besoin à l'étape 4.

---

## Étape 2 — Nettoyer les artefacts Phase 4 du clone

```bash
cd "$TARGET" && rm -f \
  .finishing-gate-c*.pass \
  .finishing-gate-c*-corrections.json \
  .finishing-gate-c*-art-corrections.json \
  .gates-c*-iter*.json \
  .gates-c*-art.json \
  .gates-c*-v*.json \
  .gates-finishing-c*-*.json \
  .gates-blacklist-c*-*.json \
  .gates-blacklist-c*-*.stdout \
  .critique-c*-iter*.json \
  .critique-c*-a11y-iter*.json \
  .critique-c*-composition-iter*.json \
  .critique-c*-typo-copy-iter*.json \
  .critique-c*-craft-iter*.json \
  .fix-loop-c*.log \
  .pipeline-audit-c*.json \
  .phase4-concepts.txt \
  .tmp-*.txt \
  voltapilot-style-tile-concept-*.html \
  voltapilot-style-tile-concept-*.html.bak* \
  audit-slop-c*-*.md \
  .tmp-* \
  .tmp-gv-c*-*.png

echo "✓ Phase 4 nettoyée. Reste : artefacts Phase 3 (pitch, palette, specimen, visuels, style-choice)"
ls -1 | head -25
```

**Fichiers qui doivent rester** (Phase 3 amont) :
- `voltapilot-pitch-c2.md`
- `voltapilot-palette-c2.md`
- `voltapilot-specimen-c2.html`
- `voltapilot-style-choice-c2.md` (format final)
- `voltapilot-visual-c2-1.png` + `.b64`
- `voltapilot-visual-c2-2.png` + `.b64`
- `voltapilot-visual-direction-c2.md`
- `voltapilot-visual-analysis.md`, `voltapilot-visual-brief.md`

---

## Étape 3 — Pré-test : vérifier la détection dynamique des concepts

Avant de lancer, valider rapidement que la détection dynamique fonctionne :

```bash
sd="$TARGET"
CONCEPTS=""
for n in 1 2 3; do
  if [ -f "$sd/voltapilot-pitch-c${n}.md" ]; then
    CONCEPTS="$CONCEPTS $n"
  fi
done
CONCEPTS=$(echo $CONCEPTS | xargs)
echo "Concepts détectés : [$CONCEPTS]"
echo "Nombre : $(echo $CONCEPTS | wc -w | tr -d ' ')"
```

**Attendu** : `Concepts détectés : [2]` et `Nombre : 1`.

Si tu vois autre chose (vide, ou `1 2 3`), arrête et signale.

---

## Étape 4 — Ouvrir une nouvelle session Claude Code vierge et lancer /test-big

**Dans une nouvelle fenêtre/session Claude Code vierge**, tape :

```
/test-big test-voltapilot-vague2.5-<TIMESTAMP>
```

Exemple si timestamp = `20260427-1100` :
```
/test-big test-voltapilot-vague2.5-20260427-1100
```

**Quand le test demande quelle phase reprendre, choisis : `Phase 4 (style-tile)`**.

### ⚠️ IMPORTANT — 3 pauses utilisateur attendues pendant le run

À 3 moments clés, le pipeline va s'arrêter et te demander une réponse :

#### Pause 1 — Étape 4.1bis : après création HTML v0 (avant toute correction)

Tu verras dans le chat :

> **Pause 4.1bis — Validation HTML v0**
>
> Les style-tiles v0 sont prêts (avant toute correction Designer). C'est le moment d'arrêter tôt si la direction visuelle ne te convient pas.
>
> **Options :**
> 1. **OK** — Valider et continuer (gates Python + corrections en aval)
> 2. **RELANCER 4.1** — Modifier le brief / les inputs et relancer la création
> 3. **STOP** — Arrêter le pipeline ici

→ Le HTML v0 est ouvert dans ton navigateur. Tu inspectes visuellement, puis tu réponds dans le chat : `OK` / `RELANCER 4.1` / `STOP`.

#### Pause 2 — Étape 4.7bis : après intégration de l'artefact

Tu verras :

> **Pause 4.7bis — Validation artefact**
>
> Les artefacts (UI mini-app) ont été générés et intégrés aux style-tiles. C'est le moment de vérifier qu'ils ne sont pas trop chargés ou hors-sujet.
>
> **Options :**
> 1. **OK** — Valider et continuer
> 2. **RELANCER 4.7** — Régénérer l'artefact avec contraintes différentes
> 3. **STOP** — Arrêter le pipeline ici

→ HTML avec artefact ouvert dans navigateur. Réponse : `OK` / `RELANCER 4.7` / `STOP`.

#### Pause 3 — Étape 4.12bis : avant la boucle iter1 (si applicable)

Tu verras :

> **Pause 4.12bis — Validation finale avant boucle iter1**
>
> Les corrections issues du Critique 4-parallèle ont été appliquées. C'est le moment de décider si on déclenche une 2e itération de polish (iter1) ou si l'état actuel est suffisant.
>
> **Options :**
> 1. **OK** — Continuer vers 4.13 (boucle iter1 si violations résiduelles, sinon audit final)
> 2. **RELANCER 4.12** — Ajustement manuel des corrections puis relancer Designer mode CORRECTION
> 3. **STOP** — Livrer en l'état (passer directement à 4.14 audit final, skip iter1)

→ HTML post-correction iter0 ouvert dans navigateur. Réponse : `OK` / `RELANCER 4.12` / `STOP`.

> **Note** : si la sous-étape 4.12 est skippée (aucune correction iter0 nécessaire), 4.12bis l'est aussi — pas de pause dans ce cas.

### Durée estimée

**~75-90 minutes** (vs 120 min hier) grâce au parallélisme P8 sur les 4 Critiques + skip conditionnel des sous-étapes de correction.

---

## Étape 5 — Validation à la fin du run

Reviens dans n'importe quel terminal et lance ce bloc bash :

```bash
TARGET="/Users/charlesbezard/Library/CloudStorage/GoogleDrive-charles.bezard@gmail.com/Mon Drive/Claude Code/Brand Identity Generator/.claude/skills/brand-identity/outputs/test-voltapilot-vague2.5-<TIMESTAMP>"
SD="$TARGET"
N=2  # concept Pouls Profond

echo "=== TEST E2E — VALIDATION VAGUE 2.5 ==="
echo ""
echo "--- 0. Détection dynamique ---"
if [ -f "$SD/.phase4-concepts.txt" ]; then
  CONCEPTS=$(cat "$SD/.phase4-concepts.txt")
  echo "  ✓ .phase4-concepts.txt présent — concepts traités : [$CONCEPTS]"
else
  echo "  ⚠ .phase4-concepts.txt absent (peut être normal si nettoyé en fin de Phase)"
fi

echo ""
echo "--- 1. Artefacts attendus présents ---"
ARTEFACTS=(
  "voltapilot-style-tile-concept-${N}.html"
  ".gates-finishing-c${N}-v0.json"
  ".finishing-gate-c${N}-v0.pass"
  ".finishing-gate-c${N}-v0-corrections.json"
  ".gates-finishing-c${N}-art.json"
  ".finishing-gate-c${N}-art.pass"
  ".finishing-gate-c${N}-art-corrections.json"
  ".critique-c${N}-a11y-iter0.json"
  ".critique-c${N}-composition-iter0.json"
  ".critique-c${N}-typo-copy-iter0.json"
  ".critique-c${N}-craft-iter0.json"
  ".critique-c${N}-iter0.json"
  ".pipeline-audit-c${N}.json"
)
MISSING=0
for art in "${ARTEFACTS[@]}"; do
  if [ -f "$SD/$art" ]; then echo "  ✓ $art"; else echo "  ❌ $art MANQUANT"; MISSING=$((MISSING+1)); fi
done

echo ""
echo "--- 2. P4 — Convention nommage backups respectée ---"
echo -n "  Anciens noms (doit être 0) : "
ls "$SD"/.bakv0 "$SD"/.bakart "$SD"/.bakiter0 2>/dev/null | wc -l | tr -d ' '
echo "  Nouveaux backups présents :"
ls "$SD"/*.html.bak-* 2>/dev/null | head -5

echo ""
echo "--- 3. P3 + P3-bis — Anti-régression rollback (logs .fix-loop) ---"
if [ -f "$SD/.fix-loop-c${N}.log" ]; then
  echo "  Contenu .fix-loop-c${N}.log :"
  cat "$SD/.fix-loop-c${N}.log" | sed 's/^/    /'
  ROLLBACK_COUNT=$(grep -c "P3 ROLLBACK" "$SD/.fix-loop-c${N}.log" 2>/dev/null || echo "0")
  echo "  → P3 ROLLBACK déclenchés : $ROLLBACK_COUNT (peut être 0 si corrections OK)"
else
  echo "  ⚠ Pas de .fix-loop-c${N}.log"
fi

echo ""
echo "--- 4. P8 — Parallélisme 4 Critiques (wall-clock) ---"
if [ -f "$SD/.critique-c${N}-a11y-iter0.json" ] && [ -f "$SD/.critique-c${N}-craft-iter0.json" ]; then
  t_a=$(stat -f %B "$SD/.critique-c${N}-a11y-iter0.json")
  t_co=$(stat -f %B "$SD/.critique-c${N}-composition-iter0.json")
  t_tc=$(stat -f %B "$SD/.critique-c${N}-typo-copy-iter0.json")
  t_cr=$(stat -f %B "$SD/.critique-c${N}-craft-iter0.json")
  t_min=$t_a
  t_max=$t_a
  for t in $t_co $t_tc $t_cr; do
    [ "$t" -lt "$t_min" ] && t_min=$t
    [ "$t" -gt "$t_max" ] && t_max=$t
  done
  delta=$((t_max - t_min))
  echo "  Wall-clock entre 1er et dernier critique : ${delta}s"
  if [ "$delta" -lt 480 ]; then
    echo "  ✓ Parallélisme effectif (< 8 min)"
  else
    echo "  ❌ Parallélisme suspect (> 8 min) — voir log P8 WARN"
  fi
fi

echo ""
echo "--- 5. P3 Synthétiseur signature ---"
grep -q '"synthesizer_subagent_signature"' "$SD/.critique-c${N}-iter0.json" 2>/dev/null && echo "  ✓ Signature présente" || { echo "  ❌ Synthétiseur shortcut détecté"; MISSING=$((MISSING+1)); }

echo ""
echo "--- 6. P5 vague2 dans gates JSON ---"
if grep -q '"vague2"' "$SD/.gates-finishing-c${N}-v0.json" 2>/dev/null; then
  COUNT=$(python3 -c "import json; d=json.load(open('$SD/.gates-finishing-c${N}-v0.json')); print(d.get('vague2',{}).get('total_warnings','?'))" 2>/dev/null)
  echo "  ✓ vague2 présent — $COUNT warnings remontés"
else
  echo "  ❌ Section vague2 absente"; MISSING=$((MISSING+1))
fi

echo ""
echo "--- 7. verdict_critiques (Patch A + P1) ---"
VERDICT=$(python3 -c "import json; d=json.load(open('$SD/.pipeline-audit-c${N}.json')); print(d.get('verdict_critiques','MISSING'))" 2>/dev/null)
echo "  verdict_critiques : $VERDICT"
echo "$VERDICT" | grep -qE "OK|FALLBACK_VAGUE1" && echo "  ✓ Verdict acceptable" || { echo "  ❌ Shortcut détecté"; MISSING=$((MISSING+1)); }

echo ""
echo "--- 8. Pas d'artefacts c1/c3 parasites ---"
PARASITE=0
for n in 1 3; do
  for art in "voltapilot-style-tile-concept-${n}.html" ".gates-finishing-c${n}-v0.json" ".pipeline-audit-c${n}.json"; do
    [ -f "$SD/$art" ] && { echo "  ⚠ Parasite c${n}: $art"; PARASITE=$((PARASITE+1)); }
  done
done
[ "$PARASITE" -eq 0 ] && echo "  ✓ Aucun artefact c1/c3 (run partial respecté)"

echo ""
echo "=== RÉSUMÉ ==="
[ "$MISSING" -eq 0 ] && echo "✅ TOUS LES CHECKS OK — vague 2.5 validée sur c${N}" || echo "❌ $MISSING check(s) échoué(s)"
```

---

## Étape 6 — Mesure du score audit-slop

```
/audit-slop --session test-voltapilot-vague2.5-<TIMESTAMP> --concept 2
```

Note le score final.

---

## Critères de succès

| Critère | Cible | Source |
|---|---|---|
| Détection dynamique | `.phase4-concepts.txt` contient `2` | étape 5.0 |
| Artefacts c2 présents | 13/13 | étape 5.1 |
| **3 pauses utilisateur déclenchées** | **OUI** (4.1bis, 4.7bis, 4.12bis affichent le prompt) | observation directe pendant le run |
| Convention nommage backup | `.bak-v0-pre-correction`, `.bak-art-pre-correction`, etc. | étape 5.2 |
| **P3 rollback effectif** | log `P3 ROLLBACK` si correction empire (peut être 0 si tout OK) | étape 5.3 |
| **P8 parallélisme 4 Critiques** | **wall-clock < 8 min** entre 1er et dernier critique | étape 5.4 |
| Signature Synthétiseur | OUI | étape 5.5 |
| Section `vague2` visible | OUI + warnings remontés | étape 5.6 |
| `verdict_critiques` | `OK` ou `FALLBACK_VAGUE1` | étape 5.7 |
| Pas d'artefacts c1/c3 parasites | 0 | étape 5.8 |
| **Score audit-slop final** | **≥ 7.5/10** (cible 8.0+) | étape 6 |
| **BIG Pipeline gate Python** | **≥ 7/10** (vs 3 hier) | étape 6 |

---

## Que m'envoyer en retour pour analyse

Copie-colle dans la session principale :
1. **Le résultat complet du bloc bash de l'étape 5** (avec ✓/❌)
2. **Le contenu du `.fix-loop-c2.log`** (pour voir si P3 ROLLBACK ou P8 WARN ont été déclenchés)
3. **Le score audit-slop final** (capture d'écran ou texte)
4. **Le chemin exact du dossier**

---

## Si problème pendant le test

| Symptôme | Cause probable | Action |
|---|---|---|
| Pause 4.1bis ne se déclenche pas | P7 mal interprété par l'orchestrateur | Note l'étape qui a sauté, signale |
| 4 Critiques séquentiels (wall-clock > 8 min) | P8 directive ignorée | Le warning sera dans `.fix-loop` — pas bloquant |
| Test plante avec "Aucun pitch concept trouvé" | Détection dynamique non active | Vérifier zone Étape 4 SKILL.md |
| Test plante avec un nom de backup non trouvé | P4 incomplet | Note l'erreur exacte, signale |
| Score régresse vs 6.5/10 | Hypothèse rollback ne marche pas | On diagnostique |
| `vague2` toujours absent | P4+P5 régressé | À vérifier |

---

## Rollback rapide si la Vague 2.5 casse tout

```bash
cd "/Users/charlesbezard/Library/CloudStorage/GoogleDrive-charles.bezard@gmail.com/Mon Drive/Claude Code/Brand Identity Generator/.claude/skills/brand-identity"
ls -1 SKILL.md.bak-pre-* | head -10  # liste les backups disponibles
# Pour revenir à l'état pré-Vague 2.5 (juste avant les 4 patches du 27 avril) :
cp SKILL.md.bak-pre-P4-20260427-101536 SKILL.md
echo "✓ SKILL.md restauré état pré-P4 (avant Vague 2.5)"
```

Backups disponibles (ordre chronologique) :
- `SKILL.md.bak-pre-refactor-r3-20260426-204751` — pré-refactor R3
- `SKILL.md.bak-pre-dynamic-concepts-20260426-1900` — pré-détection dynamique
- `SKILL.md.bak-pre-P4-20260427-101536` — pré-P4 rename backups (= état pré-Vague 2.5)
- `SKILL.md.bak-pre-P3-20260427-101828` — pré-P3 anti-régression
- `SKILL.md.bak-pre-P8-20260427-102305` — pré-P8 parallélisme
- `SKILL.md.bak-pre-P7-20260427-102704` — pré-P7 pauses utilisateur

---

## Dernière mise à jour

2026-04-27 — Test E2E préparé après application des 4 patches Vague 2.5 (P3, P3-bis, P4, P7, P8). Run estimé ~75-90 min avec 3 pauses utilisateur.
