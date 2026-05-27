# Rapport — Bug de corruption HTML par `extract-trace.py` (Phase 4)

**Date** : 2026-05-11
**Auteur** : session de test (test-big — Camille, concept 3, Phase 4)
**Destinataire** : session d'optimisation système
**Statut** : **Levier 1 APPLIQUÉ 2026-05-11** (commit à venir) — la checklist de correction ne va plus dans le HTML (réponse texte du sous-agent uniquement), les 4 appels à `extract-trace.py` sont retirés du SKILL.md, `scripts/extract-trace.py` est supprimé. La cause racine ET l'effet de bord (faux-positifs gates) sont éliminés. **Levier 2 (garde-fou validation post-transformation in-place) + bug connexe `pipefail` (§5) : NON FAITS — à traiter dans un chantier de suivi, avec test soigné (risque de faux positifs / rollback à tort).**

---

## 0. TL;DR

Le script `scripts/extract-trace.py`, appelé plusieurs fois pendant la state-machine de la Phase 4 (étapes 4.5 / 4.6 / 4.12, garde-fous "P15") pour **retirer du HTML les commentaires `<!-- TRACE PASSE … -->`** avant de relancer les gates Python, a **dévoré deux balises `<section>` complètes** (`<section class="artifact-witness">` et `<section class="atmosphere-block">`, ouvrantes ET fermantes) lors d'un run. Le HTML est devenu structurellement cassé (1 seule `<section>` sur 3, zéro `</section>`), tout en restant "plausible" (le CSS et le contenu de l'artefact étaient toujours là, juste plus enveloppés dans leurs sections). Le bug est passé inaperçu sur le moment ; détecté ensuite via un `grep` de contrôle ; réparé en faisant réécrire le HTML par un sous-agent à partir d'un backup propre. **Coût : ~20 min + risque qu'un run automatique non surveillé continue sur un HTML invalide.**

---

## 1. Le problème — description précise

### 1.1 Ce que fait `extract-trace.py` et pourquoi il existe

- **Contexte** : les sous-agents de correction chirurgicale Phase 4 (`phases/phase-4-styletile-correction.md`, mécanisme "P14") sont tenus d'insérer dans le HTML qu'ils produisent un commentaire de checklist juste après `<head>` :
  ```html
  <!-- TRACE PASSE 1/1 severity=all
  V-001: APPLIED  (...)
  V-002: SKIPPED  raison="..."
  ... -->
  ```
- **Problème que ça crée** : ces commentaires contiennent des mots-clés (`letter-spacing`, `box-shadow`, `translateY`, `infinite`, `clip-path`, etc.) qui font **faux-positifver** les gates `scripts/phase4-blacklist-gate.py` et `scripts/phase4-finishing-gate.py` (qui scannent le HTML brut, commentaires inclus).
- **Solution actuelle (= la cause du bug)** : avant de relancer les gates dans les garde-fous "P15" (étapes 4.5, 4.6, 4.12 du SKILL.md), l'orchestrateur appelle :
  ```bash
  python3 "{skill_dir}/scripts/extract-trace.py" "$html" "$sd/.trace-c${n}-…txt"
  ```
  Ce script est censé : (a) extraire les blocs `<!-- TRACE PASSE … -->` du HTML vers un fichier `.trace-….txt`, et (b) **réécrire le HTML in-place sans ces commentaires**. C'est l'étape (b) qui a corrompu le fichier.

### 1.2 Le bug observé

Sur le run du 2026-05-11 (Camille c3) :
- Le HTML était à **61 654 octets / 1429 lignes** juste avant l'appel à `extract-trace.py` (état post-correction 4.9, valide, 3 sections, gates OK).
- Après l'appel : **48 039 octets / 1235 lignes**. Perte de ~13,6 ko.
- `grep -c '<section'` → **1** (au lieu de 3) ; `grep -c '</section>'` → **0** (au lieu de 3) ; `grep -c 'class="artifact-witness"'` → **0** ; `grep -c 'class="atmosphere-block"'` → **0**. En revanche `class="voice-block"` → 1 (intacte), `class="artifact-witness__inner"` → 3 (le `<div>` interne de l'artefact toujours là), tout le CSS des sections artifact-witness/atmosphere toujours là, le `<script>` du phare et le `<svg>` toujours là.
- Conclusion : extract-trace a **supprimé du markup `<body>` tout un segment** allant à peu près de la fin du hero (`<header class="voice-block__header">` … `<style>`) et un autre segment (`<header class="quart-ledger">` … `<script>`), englobant les balises `<section>` ouvrantes/fermantes de la zone médiane et de l'atmosphère. Cohérent avec une **regex de découpe trop gourmande** : au lieu de matcher uniquement les blocs `<!-- TRACE PASSE … -->`, elle a probablement matché du `<!--` à `-->` de façon greedy (ou DOTALL non borné), et **un agent de correction avait reformulé/mentionné des `<!--`/`-->` ou inséré d'autres commentaires HTML ailleurs** dans le fichier — ce qui a déplacé les bornes du match et fait sauter tout ce qu'il y avait entre.

### 1.3 Pourquoi c'est dangereux

- **Silencieux** : le HTML reste "ouvrable" (le navigateur tolère des `<section>` non fermées), les `<style>`/`<script>` sont intacts, donc à l'œil le rendu peut sembler proche. Les gates Python tournent quand même (et passent, parce qu'ils voient moins de contenu).
- **Contamination aval** : un run automatique non surveillé continuerait vers les critiques, l'audit, le packaging avec un HTML invalide. Les critiques noteraient peut-être l'anomalie de structure, mais ce n'est pas garanti.
- **Récurrent** : tant que (a) les sous-agents insèrent des commentaires `<!-- TRACE … -->` dans le HTML et (b) un script in-place les retire avec une regex fragile, ça peut se reproduire à chaque run où un agent met `<!--`/`-->` dans une description ou ajoute un commentaire.

---

## 2. Ce que j'envisage (les pistes)

Trois leviers, qui peuvent se combiner :

**Levier 1 — Supprimer le besoin** : ne plus mettre la checklist de correction DANS le HTML. Le commentaire `<!-- TRACE PASSE … -->` a une faible valeur d'audit (l'orchestrateur a déjà la réponse texte du sous-agent, qu'il peut logger dans `.fix-loop-c{N}.log`). Si la checklist ne va que dans la réponse texte du sous-agent → plus de commentaire à retirer → plus d'appel à `extract-trace.py` → vecteur supprimé. Bonus : les gates ne voient plus jamais de mots-clés parasites, donc le problème de faux-positifs disparaît aussi.

**Levier 2 — Garde-fou de validation après toute transformation in-place du HTML** : tout script/sed/regex qui réécrit le HTML Phase 4 in-place doit être suivi d'un check de structure ; en cas d'échec, restaurer le backup et `exit 1`. Filet de sécurité général, indépendant de ce bug précis (protège aussi contre les futurs `sed`/`python -c` destructifs des agents ou de l'orchestrateur).

**Levier 3 — Durcir `extract-trace.py`** : si on garde le mécanisme, rendre la regex stricte (ne matcher que les blocs dont le contenu commence par `TRACE PASSE`, non-greedy), et faire échouer le script si l'output a un nombre de `<`/`>` différent de l'input ou ne contient plus `</html>` ou a perdu une des 3 classes de section.

---

## 3. Ce que je propose (recommandation)

**Faire Levier 1 + Levier 2 ensemble.** (Levier 3 devient redondant si Levier 1 est fait, mais ne coûte presque rien si on veut une ceinture de plus.)

- **Levier 1** est la vraie correction : il élimine la cause racine ET un effet de bord (faux-positifs des gates sur les commentaires). Petit chantier : 1 prompt + retrait d'appels dans le SKILL.md.
- **Levier 2** est à faire de toute façon : c'est une bonne hygiène pour une state-machine qui fait beaucoup de transformations in-place du HTML. Petit chantier : un bloc bash réutilisable.

Priorité : Levier 2 d'abord (le moins risqué, protège immédiatement), puis Levier 1.

---

## 4. Solution concrète imaginée (pointeurs d'implémentation)

### 4.1 Levier 1 — supprimer les commentaires TRACE du HTML

Fichiers concernés :
- `phases/phase-4-styletile-correction.md` — la section "⛔ CHECKLIST TRACE — obligatoire avant d'écrire le HTML" (vers la fin du prompt) demande actuellement d'insérer `<!-- TRACE PASSE {pass_index}/{pass_total_passes} severity={pass_severity} … -->` juste après `<head>`. → **Remplacer par** : "Liste explicitement chaque correction par son `rule_id`/`id` avec son statut (APPLIED / SKIPPED + raison) **dans ta réponse texte uniquement** (PAS dans le HTML). N'insère AUCUN commentaire dans le HTML." Conserver les règles sur le ratio APPLIED ≥ 70% etc.
- `SKILL.md` — étapes **4.5**, **4.6**, **4.12** (et toute autre étape qui appelle `extract-trace.py` ; chercher `extract-trace.py` dans le fichier — il apparaît dans les garde-fous "P15"). → **Retirer les appels** `python3 "{skill_dir}/scripts/extract-trace.py" "$html" "$sd/.trace-c${n}-….txt"`. Comme les commentaires TRACE n'existent plus, les gates n'ont plus de faux-positifs ; les `grep -oE "❌ [a-z-]+"` sur les stdout blacklist et les lectures de `vague1.checks[*].status == FAIL` restent valides.
- Optionnel : faire logger à l'orchestrateur, juste après le retour du sous-agent de correction, la checklist (extraite de la réponse texte du sous-agent) dans `.fix-loop-c{N}.log` — pour garder une trace d'audit hors-HTML.
- `scripts/extract-trace.py` — peut être laissé en place (mort) ou supprimé. Si on le supprime, vérifier qu'aucune autre étape ne l'utilise.

### 4.2 Levier 2 — garde-fou de validation post-transformation in-place

Ajouter dans le SKILL.md, à utiliser **après chaque transformation in-place du HTML Phase 4** (post-correction 4.5/4.6/4.9/4.12, post-insertion artefact 4.7, post-swap 4.15…), idéalement encapsulé comme un bloc bash réutilisable. Un backup horodaté doit avoir été pris **juste avant** la transformation (c'est déjà le cas pour les corrections : `.bak-v0-pre-correction`, `.bak-art-pre-correction`, `.bak-iter0-pre-correction`).

Pseudocode du check (pour un fichier `$html` et son backup `$bak`) :
```bash
ok=1
[ "$(grep -c '<section' "$html")" -eq "$(grep -c '</section>' "$html")" ] || { ok=0; echo "❌ sections déséquilibrées"; }
[ "$(grep -cE 'class="(voice-block|artifact-witness|atmosphere-block)"' "$html")" -eq 3 ] || { ok=0; echo "❌ pas 3 classes de section"; }
grep -q '</html>' "$html" || { ok=0; echo "❌ </html> absent"; }
[ "$(grep -c '<!-- ARTEFACT_PLACEHOLDER -->' "$html")" -le 1 ] || { ok=0; echo "❌ placeholder dupliqué"; }
# (avant artefact: == 1 ; après artefact: == 0 — adapter selon l'étape)
sz_new=$(wc -c < "$html"); sz_old=$(wc -c < "$bak")
[ "$sz_new" -ge $(( sz_old * 80 / 100 )) ] || { ok=0; echo "❌ taille chutée de >20% ($sz_old → $sz_new)"; }
grep -q 'data-visual=' "$html" || true   # n'invalide pas si le concept n'a pas d'image — adapter
if [ "$ok" -eq 0 ]; then
  cp "$bak" "$html"
  echo "P-VALIDATE ROLLBACK c${n} | transformation in-place a cassé le HTML — restauré depuis $bak" >> "$sd/.fix-loop-c${n}.log"
  exit 1   # ou : RELANCER la transformation
fi
```
Seuils à calibrer : le `-20%` peut être resserré à `-12%` une fois le Levier 1 fait (plus de commentaires TRACE = plus de variations de taille légitimes). Le check `== 3` sur les classes de section suppose que les sous-agents gardent les noms de classe exacts `voice-block` / `artifact-witness` / `atmosphere-block` — c'est déjà une consigne forte dans tous les prompts de correction, donc OK.

### 4.3 Levier 3 (optionnel, si on garde `extract-trace.py`)

Dans `scripts/extract-trace.py` :
- Regex stricte : `re.compile(r'<!--\s*TRACE PASSE\b.*?-->', re.DOTALL)` (non-greedy, ancrée sur le préfixe `TRACE PASSE`). Ne JAMAIS faire un `<!--.*?-->` global.
- Avant d'écrire l'output : si `output.count('<')` != `input.count('<') - retirés` (ou plus simplement si `'</html>' not in output` ou si l'une des 3 classes de section a disparu) → ne pas écrire, retourner un code d'erreur.

---

## 5. Annexes — éléments du run où le bug est apparu

- Dossier de session : `.claude/skills/brand-identity/outputs/test-camille-test-20260511-1330/`
- Backup du fichier corrompu (pour analyse post-mortem si besoin) : `camille-style-tile-concept-3.html.bak-CORRUPTED-by-extract-trace` dans ce dossier.
- Backup propre utilisé pour la réparation : `camille-style-tile-concept-3.html.bak-art-pre-correction` (59 151 octets, état post-insertion artefact, pré-correction 4.9).
- Tailles : 61 654 o (pré-extract-trace) → 48 039 o (post-extract-trace, corrompu) → réparé à ~56,5–56,8 ko (réécriture sans les commentaires TRACE).
- Le `.pipeline-audit-c3.json` du run mentionne l'incident dans sa clé `"incident"`.
- Note connexe (hors-périmètre de ce bug, mais relevée le même run) : un garde-fou "P12/P17" des étapes 4.5/4.6 a une fois déclenché un **ROLLBACK à tort** (le HTML était valide, taille 32 ko, 3 sections — pourtant rollback). Cause non confirmée ; piste : `set -o pipefail` hérité du profil shell + un `grep -v '^$'` qui exit 1 dans une sous-substitution `$(... | grep | wc -l)` cassant un `&&`-chain de l'orchestrateur. À vérifier : les blocs bash des garde-fous P12/P17 devraient être robustes à `pipefail` (préfixer par `set +o pipefail` ou éviter les `grep` qui peuvent exit non-zéro dans des command substitutions chaînées par `&&`).
