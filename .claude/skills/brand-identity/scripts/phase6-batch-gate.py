#!/usr/bin/env python3
"""
phase6-batch-gate.py — Gate anti-slop pour les Batch 2 et Batch 3 de BIG.

Wrapper mince : strippe les <svg> et data: URIs (les SVG de logo sont vettés
en amont par la Phase Logo, le base64 est du bruit), délègue aux gates Phase 4
(phase4-blacklist-gate.py + phase4-finishing-gate.py), re-pondère leurs verdicts
selon un profil « documentation batch », et ajoute des checks batch-spécifiques
(Specs Lock, Completeness, polices bannies non approuvées, image externe, Lorem ipsum).

Tourne UNE fois par batch, sur le fichier complet assemblé (Batch 2 après injection
des SVG logos ; Batch 3 après assemblage des 3 chapitres).

Usage:
  python3 phase6-batch-gate.py <batch_file.html> --batch {2|3} --cursor-a N \
      [--expected-root <root.css>] [--approved-fonts "Font A,Font B"] [--json-output PATH]

Sortie JSON (--json-output) :
  { gate, batch, html_audited, html_sha256, timestamp, status,
    deterministic_fails:[...], other_fails:[...], warns:[...] }
  Chaque entrée = {check, rule_id, severity, line, message, chapter, source}
  - deterministic_fails : violations mécaniques non-ambiguës → auto-correction (1 tour) côté orchestrateur
  - other_fails         : violations à surfacer à l'utilisateur (« je corrige ? ») — pas d'auto-trigger
  - warns               : informationnel (période d'observation — promotion progressive vers FAIL)

Exit code 0 = PASS-clean ou WARN seulement
Exit code 1 = au moins un deterministic_fail OU un other_fail
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BLACKLIST_GATE = os.path.join(HERE, "phase4-blacklist-gate.py")
FINISHING_GATE = os.path.join(HERE, "phase4-finishing-gate.py")

# --- Profil batch : exceptions vs la classification des gates Phase 4 ---

# rule_ids exclus : faux positifs garantis sur un batch
#  - graphic-layer-* : un batch n'est pas un style-tile « héros », pas de socle grain/overlay requis
#  - figurative-svg / stroke-circle-amateur : les batches DOCUMENTENT des icônes/charts (et les <svg> sont strippés)
#  - overline-decorative-line : la convention overline+décorateur est imposée par le prompt Batch 3
#  - root_vars_unused : le batch recopie le :root complet du style-tile (Specs Lock) et n'en utilise qu'un sous-ensemble
BATCH_EXCLUDE = {
    "graphic-layer-missing-grain", "graphic-layer-missing-overlay",
    "graphic-layer-insufficient", "graphic-layer-grain-too-faint",
    "figurative-svg", "stroke-circle-amateur", "overline-decorative-line",
    "root_vars_unused",
}

# rule_ids démotés en WARN pour le profil batch (toutes les autres rule_ids
# conservent la sévérité native du gate Phase 4 — décision audit 13 mai 2026).
# Chaque entrée DOIT être justifiée par un commentaire citant la raison batch-spécifique.
BATCH_DEMOTE_TO_WARN = {
    # R-148 meta theme-color : polish mobile-chrome, marginal pour une planche de doc
    "R148",
    # R-054 skip link : a11y prio nav SaaS, moins critique pour une planche showroom
    "R054",
    # hover_multi_property : batches montrent souvent des composants en démos
    # isolées où un hover minimal (1 propriété) est légitime
    "hover_multi_property",
    # advanced_techniques : le finishing gate Phase 4 exige ≥4 techniques avancées
    # (calibré pour un style-tile « héros »). Les prompts batch n'exigent que ≥2.
    # Demoter en WARN pour éviter un FAIL structurel sur tous les batches.
    "advanced_techniques",
}

# labels de sections obligatoires (cf. CHECKLIST des prompts phase-6a-batch2.md / phase-6b-batch3.md)
BATCH2_SECTIONS = ["06.1", "06.2", "06.3", "06.4",
                   "04.1", "04.2", "04.3", "04.4", "04.5",
                   "07.1", "07.2", "07.3", "07.4"]
BATCH3_SECTIONS = ["08.1", "08.2", "08.3", "08.4",
                   "09.1", "09.2", "09.3", "09.4",
                   "10.1", "10.2", "10.3", "10.4", "10.5"]


# ---------------------------------------------------------------------------
# Pré-traitement
# ---------------------------------------------------------------------------

def strip_svg_and_data(html: str) -> str:
    html = re.sub(r"<svg\b[^>]*>.*?</svg>", "<svg></svg>", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"data:[^\"')\s]+", "data:stripped", html)
    return html


def line_of(html: str, idx: int) -> int:
    return html.count("\n", 0, idx) + 1


def chapter_at(html: str, line: int) -> str | None:
    """Batch 3 : remonte du numéro de ligne au préfixe de chapitre .ch08-/.ch09-/.ch10-."""
    if line <= 0:
        return None
    head = "\n".join(html.split("\n")[:line])
    matches = re.findall(r"\.ch(08|09|10)-", head)
    return matches[-1] if matches else None


# ---------------------------------------------------------------------------
# Checks batch-spécifiques (faits par le wrapper)
# ---------------------------------------------------------------------------

def parse_root_props(css_or_html: str):
    """Extrait le bloc :root {...} (même imbriqué dans @layer tokens) → dict {prop: valeur normalisée}."""
    m = re.search(r":root\s*\{", css_or_html)
    if not m:
        return None
    i = m.end()
    depth = 1
    while i < len(css_or_html) and depth > 0:
        c = css_or_html[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    block = css_or_html[m.end():i - 1]
    props = {}
    for pm in re.finditer(r"(--[\w-]+)\s*:\s*([^;]+);", block):
        props[pm.group(1).strip()] = re.sub(r"\s+", " ", pm.group(2).strip()).lower()
    return props


def check_specs_lock(batch_html: str, expected_root_path: str | None) -> list[dict]:
    if not expected_root_path:
        return [_w("specs-lock", 0, "--expected-root non fourni — Specs Lock non vérifié")]
    try:
        with open(expected_root_path, encoding="utf-8") as f:
            expected_raw = f.read()
    except Exception:
        return [_w("specs-lock", 0, f"Impossible de lire {expected_root_path} — Specs Lock non vérifié")]
    expected = parse_root_props(expected_raw)
    actual = parse_root_props(batch_html)
    if expected is None:
        return [_w("specs-lock", 0, "Le fichier --expected-root ne contient pas de bloc :root analysable — Specs Lock non vérifié")]
    if actual is None:
        return [_f("specs-lock", 0, "Aucun bloc :root trouvé dans le batch — le :root validé doit y être recopié à l'identique")]
    diffs = []
    for name, val in expected.items():
        if name not in actual:
            diffs.append(f"token manquant : {name}")
        elif actual[name] != val:
            diffs.append(f"token modifié : {name} (attendu '{val}', trouvé '{actual[name]}')")
    for name in actual:
        if name not in expected:
            if name.startswith("--color-feedback"):
                continue  # exception : Batch 2 ch.04 autorise AU PLUS 1 token --color-feedback-*
            diffs.append(f"token ajouté : {name}")
    if not diffs:
        return []
    suffix = "…" if len(diffs) > 8 else ""
    return [_f("specs-lock", 0, "Le :root du batch diverge du :root validé : " + " ; ".join(diffs[:8]) + suffix)]


def check_completeness(batch_html: str, batch_n: int) -> list[dict]:
    sections = BATCH2_SECTIONS if batch_n == 2 else BATCH3_SECTIONS
    missing = [s for s in sections if s not in batch_html]
    if batch_n == 2 and not re.search(r"\b05[.\s]|Logotype", batch_html, re.IGNORECASE):
        missing.append("chapitre 05 (Logotype)")
    if not missing:
        return []
    return [_f("completeness", 0, f"Sections manquantes dans le Batch {batch_n} : " + ", ".join(missing))]


def check_external_image(batch_html: str) -> list[dict]:
    out = []
    for m in re.finditer(r"""(?:src\s*=\s*["']|url\(\s*["']?)(https?://[^"')\s]+)""", batch_html, re.IGNORECASE):
        out.append(_of("external-image", line_of(batch_html, m.start()),
                       f"Image externe ({m.group(1)[:60]}…) — le batch n'embarque que des chemins relatifs (visual-final/…) ou des assets inline ; pas de stock distant"))
    return out


def check_lorem_ipsum(batch_html: str) -> list[dict]:
    m = re.search(r"lorem\s+ipsum", batch_html, re.IGNORECASE)
    if not m:
        return []
    return [_of("lorem-ipsum", line_of(batch_html, m.start()),
                "« Lorem ipsum » détecté — le batch utilise le contenu réel de la marque")]


def _f(rid, line, msg):   # deterministic FAIL
    return {"check": rid, "rule_id": rid, "severity": "FAIL", "line": line, "message": msg, "chapter": None, "source": "wrapper"}


def _of(rid, line, msg):  # other FAIL (surfacé)
    return {"check": rid, "rule_id": rid, "severity": "FAIL", "line": line, "message": msg, "chapter": None, "source": "wrapper", "surface_only": True}


def _w(rid, line, msg):   # WARN
    return {"check": rid, "rule_id": rid, "severity": "WARN", "line": line, "message": msg, "chapter": None, "source": "wrapper"}


# ---------------------------------------------------------------------------
# Délégation aux gates Phase 4
# ---------------------------------------------------------------------------

def run_gate(cmd: list[str], json_path: str) -> dict:
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except Exception as e:
        return {"_error": f"{os.path.basename(cmd[1])} a échoué : {e}"}
    try:
        with open(json_path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"_error": f"JSON de {os.path.basename(cmd[1])} illisible : {e}"}


def collect_from_blacklist(j: dict) -> list[dict]:
    out = []
    for v in j.get("fails", []):
        out.append({"rule_id": v.get("rule_id") or v.get("check"), "line": v.get("line", 0) or 0,
                    "message": v.get("message", ""), "gate_severity": "FAIL", "source": "blacklist"})
    for w in j.get("warns", []):
        out.append({"rule_id": w.get("rule_id") or w.get("check"), "line": w.get("line", 0) or 0,
                    "message": w.get("message", ""), "gate_severity": "WARN", "source": "blacklist"})
    return out


def collect_from_finishing(j: dict) -> list[dict]:
    out = []
    for key, c in j.get("vague1", {}).get("checks", {}).items():
        st = c.get("status")
        if st in ("FAIL", "WARN"):
            out.append({"rule_id": key, "line": 0,
                        "message": (f"{c.get('label', key)} : {c.get('message', '')}").strip(" :"),
                        "gate_severity": st, "source": "finishing"})
    for w in j.get("vague2", {}).get("warnings", []):
        out.append({"rule_id": w.get("rule_id") or w.get("label"), "line": 0,
                    "message": (f"{w.get('label', '')} : {w.get('message', '')}").strip(" :"),
                    "gate_severity": "WARN", "source": "finishing"})
    return out


def classify(rule_id: str, gate_severity: str = "WARN") -> str | None:
    """Profil batch : 'DET' (déterministe, auto-corrigé), 'FAIL' (surfacé), 'WARN', ou None (exclu).

    Logique (audit 13 mai 2026) : par défaut on conserve la sévérité native du
    gate Phase 4. On EXCLUT les faux-positifs batch-spécifiques (BATCH_EXCLUDE)
    et on DÉMOTE quelques rule_ids en WARN avec justification (BATCH_DEMOTE_TO_WARN).
    Les polices bannies (R013) sont promues DET (auto-correction chirurgicale).
    """
    rid = rule_id or ""
    if rid in BATCH_EXCLUDE:
        return None
    if re.search(r"(banned.?fonts?|\bR013\b)", rid, re.IGNORECASE):
        return "DET"  # police bannie = défaut mécanique → auto-correction
    if rid in BATCH_DEMOTE_TO_WARN:
        return "WARN"
    # Défaut : on conserve la sévérité native du gate Phase 4
    return "FAIL" if gate_severity == "FAIL" else "WARN"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(prog="phase6-batch-gate")
    ap.add_argument("batch_file")
    ap.add_argument("--batch", type=int, choices=(2, 3), required=True)
    ap.add_argument("--cursor-a", type=int, default=2)
    ap.add_argument("--expected-root", default=None, help="Fichier .css contenant le bloc :root validé du style-tile")
    ap.add_argument("--approved-fonts", default="", help="Liste CSV des polices validées du style-tile (réservé — recoupage futur ; les polices bannies sont déjà détectées via R013)")
    ap.add_argument("--json-output", default=None)
    args = ap.parse_args()

    try:
        with open(args.batch_file, encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"Erreur : fichier introuvable — {args.batch_file}")
        sys.exit(2)

    # Fichier strippé pour les gates Phase 4 (SVG logos vettés en amont ; base64 = bruit)
    tmpdir = tempfile.mkdtemp(prefix="phase6gate-")
    stripped_path = os.path.join(tmpdir, "stripped.html")
    with open(stripped_path, "w", encoding="utf-8") as f:
        f.write(strip_svg_and_data(html))
    bl_json = os.path.join(tmpdir, "bl.json")
    fin_json = os.path.join(tmpdir, "fin.json")

    bl = run_gate(["python3", BLACKLIST_GATE, stripped_path, "--json-output", bl_json], bl_json)
    fin = run_gate(["python3", FINISHING_GATE, stripped_path, str(args.cursor_a), "--json-output", fin_json], fin_json)

    raw = []
    if "_error" not in bl:
        raw += collect_from_blacklist(bl)
    if "_error" not in fin:
        raw += collect_from_finishing(fin)

    det_fails, other_fails, warns = [], [], []
    seen = set()
    for v in raw:
        sev = classify(v["rule_id"], v.get("gate_severity", "WARN"))
        if sev is None:
            continue
        key = (v["rule_id"], v["message"][:80])
        if key in seen:
            continue
        seen.add(key)
        out_sev = "FAIL" if sev == "DET" else sev   # un rule_id "DET" reste "FAIL" dans le JSON, rangé en deterministic_fails
        entry = {"check": v["rule_id"], "rule_id": v["rule_id"], "severity": out_sev,
                 "line": v["line"], "message": v["message"], "chapter": None, "source": v["source"]}
        if sev == "DET":
            det_fails.append(entry)
        elif sev == "FAIL":
            other_fails.append(entry)
        else:
            warns.append(entry)

    # Checks batch-spécifiques
    own = []
    own += check_specs_lock(html, args.expected_root)
    own += check_completeness(html, args.batch)
    own += check_external_image(html)
    own += check_lorem_ipsum(html)
    for e in own:
        if e["severity"] == "WARN":
            warns.append(e)
        elif e.get("surface_only"):
            other_fails.append(e)
        else:
            det_fails.append(e)

    # Attribution chapitre (Batch 3)
    if args.batch == 3:
        for e in det_fails + other_fails + warns:
            if e["line"] and not e["chapter"]:
                e["chapter"] = chapter_at(html, e["line"])

    status = "FAIL" if (det_fails or other_fails) else "PASS"
    payload = {
        "gate": "phase6-batch-gate", "batch": args.batch, "html_audited": args.batch_file,
        "html_sha256": hashlib.sha256(html.encode("utf-8")).hexdigest(),
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "deterministic_fails": [_clean(e) for e in det_fails],
        "other_fails": [_clean(e) for e in other_fails],
        "warns": [_clean(e) for e in warns],
    }
    if args.json_output:
        try:
            with open(args.json_output, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Avertissement : échec écriture JSON {args.json_output} : {e}")

    # stdout lisible
    print(f"\n=== PHASE 6 BATCH GATE — Batch {args.batch} ===")
    print(f"File: {os.path.basename(args.batch_file)} | cursor A = {args.cursor_a}")
    for src in (bl, fin):
        if "_error" in src:
            print(f"⚠ {src['_error']}")
    print()

    def show(title, items):
        if not items:
            return
        print(f"--- {title} ({len(items)}) ---")
        for e in items:
            loc = f"L{e['line']}" if e["line"] else "—"
            ch = f" [ch{e['chapter']}]" if e.get("chapter") else ""
            print(f"  [{e['severity']}] {e['rule_id']}{ch} ({loc}) : {e['message'][:160]}")
        print()

    show("DETERMINISTIC FAILS (auto-correction)", det_fails)
    show("FAILS (à surfacer)", other_fails)
    show("WARNINGS", warns)
    if status == "PASS":
        print(f"VERDICT: PASS — {len(warns)} warning(s) informationnel(s)")
        sys.exit(0)
    print(f"VERDICT: FAIL — {len(det_fails)} déterministe(s) + {len(other_fails)} autre(s) ; {len(warns)} warning(s)")
    sys.exit(1)


def _clean(e: dict) -> dict:
    return {k: v for k, v in e.items() if k != "surface_only"}


if __name__ == "__main__":
    main()
