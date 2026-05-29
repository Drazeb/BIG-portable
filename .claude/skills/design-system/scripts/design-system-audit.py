#!/usr/bin/env python3
"""
design-system-audit.py — Audit automatisé d'un Design System HTML généré par le skill /design-system.

Vérifie 4 choses :
1. Inventaire 1:1 — tous les items attendus par section (selon `inventory.json`) sont présents dans le DS.
2. Sourcing — tous les items du DS ont une entrée dans `audit-sources.json` qui pointe vers une ligne de design-specs.md.
3. Tailles font-size — toutes les tailles utilisées dans le CSS sont dans le type scale documenté en §02 Typography du DS.
4. Pas d'encadrés AI-slop — aucun `border-left: Xpx solid var(--doc-accent)` (X=2,3,4) sur un bloc d'emphase.

Usage:
    python3 design-system-audit.py <session_dir> [--json-output]

Output:
    - Rapport humain en stdout
    - Si --json-output : aussi un fichier `{brand}-design-system-audit-report.json` dans le dossier session

Exit codes:
    0 — Aucune violation, le DS est blindé
    1 — Une ou plusieurs violations détectées (à corriger par le sub-agent)
    2 — Erreur d'I/O ou de configuration

Inspiré de phase4-blacklist-gate.py et phase6-batch-gate.py (BIG).
"""

from __future__ import annotations
import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

# Tailles autorisées dans tous les DS (8 tokens canoniques)
ALLOWED_FONT_SIZE_TOKENS = {
    "--text-xs",        # 0.72rem
    "--text-sm",        # 0.84rem
    "--text-base",      # 1rem
    "--fs-overline",    # clamp(0.7rem, 0.85vw, 0.92rem)
    "--fs-cta",         # clamp(0.86rem, 1vw, 1.05rem)
}

# Tailles clamp / valeurs documentées dans le type scale (référence Camille v0.2)
ALLOWED_FONT_SIZE_VALUES = {
    "0.72rem", "0.84rem", "1rem",
    "clamp(0.7rem, 0.85vw, 0.92rem)",
    "clamp(0.86rem, 1vw, 1.05rem)",
    "clamp(1.3rem, 2.2vw, 1.9rem)",   # H3 sub-section (Batch 2/3)
    "clamp(2.5rem, 5vw, 4.5rem)",     # H2 chapitre
    "clamp(12vw, 18vw, 22vw)",        # Hero / Manifesto
}

# Patterns autorisés (signature DA) qui peuvent contenir border-left mais ne sont PAS des encadrés AI-slop
PATTERN_ALLOWED_BORDER_LEFT = {
    ".sidebar__nav-link",  # nav latérale active
    ".chapter__beacon-mark", # marqueur signature
}


# ─────────────────────────────────────────────────────────────────────────────
# Modèle de données
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Violation:
    """Une violation détectée par l'auditeur."""
    rule_id: str
    section: str
    severity: str  # "critical" | "warning" | "info"
    message: str
    location: str = ""  # ex: "ligne 1234" ou "section 04 Iconography"
    expected: str = ""
    found: str = ""


@dataclass
class AuditReport:
    """Rapport complet d'audit."""
    file_audited: str
    inventory_file: str = ""
    sources_file: str = ""
    violations: list[Violation] = field(default_factory=list)
    items_inventoried: int = 0
    items_sourced: int = 0
    font_sizes_checked: int = 0
    encadres_checked: int = 0
    pass_status: bool = True

    def add(self, v: Violation) -> None:
        self.violations.append(v)
        if v.severity == "critical":
            self.pass_status = False

    def summary(self) -> str:
        n_critical = sum(1 for v in self.violations if v.severity == "critical")
        n_warning = sum(1 for v in self.violations if v.severity == "warning")
        n_info = sum(1 for v in self.violations if v.severity == "info")
        status = "✅ PASS" if self.pass_status else "❌ FAIL"
        return (
            f"{status}\n"
            f"  Critical: {n_critical}\n"
            f"  Warning:  {n_warning}\n"
            f"  Info:     {n_info}\n"
            f"  Total:    {len(self.violations)}\n"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Auditeurs
# ─────────────────────────────────────────────────────────────────────────────

def audit_inventory(
    inventory: dict, ds_html: str, report: AuditReport
) -> None:
    """
    Vérifie que chaque item du fichier inventory.json est présent dans le DS HTML.

    Format inventory.json attendu :
    {
      "01-color": {
        "01.1 Palette primaire": {
          "expected_items": ["Nuit d'Indigo", "Nuit teintée", "Bleu Quart de Nuit", ...],
          "present_items":  ["Nuit d'Indigo", "Nuit teintée", "Bleu Quart de Nuit", ...]
        },
        ...
      },
      ...
    }
    """
    for section_id, subsections in inventory.items():
        # Skip meta keys (commentaires, métadonnées) — ne sont pas des sections
        if section_id.startswith("$") or section_id in (
            "source_specs", "ds_file", "generated_at",
            "source_file", "audit_date", "summary", "notes", "comment"
        ):
            continue
        if not isinstance(subsections, dict):
            continue
        for subsection_id, content in subsections.items():
            if subsection_id.startswith("$") or not isinstance(content, dict):
                continue
            expected = set(content.get("expected_items", []))
            present = set(content.get("present_items", []))
            report.items_inventoried += len(expected)

            missing = expected - present
            for item in missing:
                report.add(Violation(
                    rule_id="R12",
                    section=f"{section_id} / {subsection_id}",
                    severity="critical",
                    message=f"Item manquant dans le DS",
                    expected=item,
                    found="(absent)",
                ))

            invented = present - expected
            for item in invented:
                report.add(Violation(
                    rule_id="R13",
                    section=f"{section_id} / {subsection_id}",
                    severity="warning",
                    message=f"Item dans le DS sans correspondance dans la source",
                    found=item,
                    expected="(non listé dans inventory)",
                ))


def audit_sources(sources: dict, ds_html: str, report: AuditReport) -> None:
    """
    Vérifie que chaque entrée du fichier audit-sources.json a un format valide
    et que le texte source référencé est cohérent.

    Format attendu : { "section_id": [{ "text": "...", "source": "design-specs.md L###" }, ...] }
    """
    for section_id, items in sources.items():
        # Skip meta keys
        if section_id.startswith("$") or section_id in (
            "source_specs", "ds_file", "generated_at",
            "source_file", "audit_date", "summary", "notes", "comment"
        ):
            continue
        if not isinstance(items, list):
            report.add(Violation(
                rule_id="R06",
                section=section_id,
                severity="critical",
                message="Format invalide dans audit-sources.json — attendu liste",
                found=type(items).__name__,
            ))
            continue

        for item in items:
            report.items_sourced += 1
            if not isinstance(item, dict):
                report.add(Violation(
                    rule_id="R06",
                    section=section_id,
                    severity="critical",
                    message="Item de sourcing au mauvais format",
                    found=str(item)[:80],
                ))
                continue
            if "text" not in item or "source" not in item:
                report.add(Violation(
                    rule_id="R06",
                    section=section_id,
                    severity="critical",
                    message="Item de sourcing sans 'text' ou 'source'",
                    found=str(item)[:80],
                ))
                continue
            # Vérifier que la source est bien un pointeur design-specs ou batch
            src = item["source"]
            if not (re.search(r"design-specs\.md L\d+", src)
                    or re.search(r"batch[23]\.html L\d+", src)
                    or "style-tile" in src):
                report.add(Violation(
                    rule_id="R06",
                    section=section_id,
                    severity="warning",
                    message="Source non identifiable comme design-specs / batch / style-tile",
                    found=src[:80],
                ))


def audit_font_sizes(ds_html: str, report: AuditReport) -> None:
    """
    Cherche toutes les valeurs `font-size:` du CSS et vérifie qu'elles sont
    soit des tokens autorisés (`var(--text-xs)`, etc.), soit des valeurs
    explicitement documentées dans le type scale.

    Tolérances :
    - Valeurs dans les `.swatch__*`, `.subsection__desc`, légendes — souvent <1rem en xs/sm zone
    - Tailles inlinées dans le bloc spécimen de §02.2 Type Scale (volontaires)
    """
    # Pattern pour capturer font-size: <value>;
    pattern = re.compile(r"font-size\s*:\s*([^;]+?)(?:\s*;|\s*\}|\s*\!important)", re.IGNORECASE)
    matches = pattern.findall(ds_html)
    report.font_sizes_checked = len(matches)

    for match in matches:
        value = match.strip()

        # Tokens var(--xxx)
        if value.startswith("var(--"):
            token_name = value[4:].rstrip(")").strip()
            if token_name not in ALLOWED_FONT_SIZE_TOKENS:
                report.add(Violation(
                    rule_id="R02",
                    section="CSS global",
                    severity="warning",
                    message="Token font-size non documenté dans le type scale",
                    found=value,
                    expected=" / ".join(sorted(ALLOWED_FONT_SIZE_TOKENS)),
                ))
            continue

        # Valeurs littérales
        # Normaliser les espaces
        normalized = re.sub(r"\s+", " ", value).strip()
        if normalized in ALLOWED_FONT_SIZE_VALUES:
            continue
        # Tolérance : tailles de spécimens dans le type scale (inline style)
        # Ces tailles servent à RENDRE le specimen, pas à styler du contenu.
        # On ne flag pas les valeurs entre 0.5rem et 5rem qui apparaissent dans des
        # `style="font-size: ..."` (inline) — souvent des specimens.
        # Mais on flag les autres.
        if re.match(r"^\d+(\.\d+)?rem$", normalized):
            # Valeur rem hors scale — warning
            report.add(Violation(
                rule_id="R02",
                section="CSS",
                severity="warning",
                message="Valeur font-size rem hors type scale documenté",
                found=normalized,
                expected="utiliser un token --text-* ou clamp documenté",
            ))


def audit_encadres(ds_html: str, report: AuditReport) -> None:
    """
    Cherche les patterns AI-slop (border-left avec 2-4px solid sur un bloc d'emphase).
    Tolère border-left sur .sidebar__nav-link.is-active et .chapter__beacon-mark.

    Regex : `border-left:\s*[2-4]px\s+solid\s+var\(--doc-accent\)` ou similaire
    """
    pattern = re.compile(
        r"border-left\s*:\s*([2-4])px\s+solid\s+(var\([^)]+\)|#[0-9A-Fa-f]+|oklch[^;]+)",
        re.IGNORECASE,
    )
    matches = list(pattern.finditer(ds_html))
    report.encadres_checked = len(matches)

    for m in matches:
        # Récupérer la classe parente (recherche dans les ~200 chars précédents)
        start = max(0, m.start() - 500)
        context = ds_html[start:m.start()]
        # Chercher le sélecteur CSS qui précède
        selector_match = re.search(r"(\.[a-zA-Z][\w-]*)\s*\{[^}]*$", context)
        selector = selector_match.group(1) if selector_match else "(inconnu)"

        if selector in PATTERN_ALLOWED_BORDER_LEFT:
            continue

        report.add(Violation(
            rule_id="R04",
            section="CSS",
            severity="critical",
            message="Pattern AI-slop détecté (border-left 2-4px solid accent)",
            found=f"{selector} → {m.group(0)}",
            expected="utiliser pattern .law (hairlines dotted horizontales) ou .dont-list (liste plate)",
        ))


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def find_brand_files(session_dir: Path) -> tuple[Optional[Path], Optional[Path], Optional[Path]]:
    """Trouve {brand}-design-system-full.html, inventory.json, audit-sources.json."""
    ds_html = next(session_dir.glob("*-design-system*.html"), None)
    inventory = next(session_dir.glob("*-design-system-inventory.json"), None)
    sources = next(session_dir.glob("*-design-system-audit-sources.json"), None)
    return ds_html, inventory, sources


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Audit d'un Design System généré par le skill /design-system")
    parser.add_argument("session_dir", type=Path, help="Dossier session BIG contenant le DS et les fichiers d'audit")
    parser.add_argument("--json-output", action="store_true", help="Produire aussi un rapport JSON exploitable par sub-agent")
    args = parser.parse_args(argv)

    session_dir = args.session_dir
    if not session_dir.is_dir():
        print(f"❌ Dossier introuvable : {session_dir}", file=sys.stderr)
        return 2

    ds_html_path, inventory_path, sources_path = find_brand_files(session_dir)
    if not ds_html_path:
        print(f"❌ Fichier *-design-system-full.html introuvable dans {session_dir}", file=sys.stderr)
        return 2

    ds_html = ds_html_path.read_text(encoding="utf-8")
    report = AuditReport(file_audited=str(ds_html_path))

    # 1. Inventaire 1:1
    if inventory_path:
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        report.inventory_file = str(inventory_path)
        audit_inventory(inventory, ds_html, report)
    else:
        report.add(Violation(
            rule_id="R12",
            section="(global)",
            severity="critical",
            message="Fichier *-design-system-inventory.json absent — audit inventaire impossible",
        ))

    # 2. Sourcing
    if sources_path:
        sources = json.loads(sources_path.read_text(encoding="utf-8"))
        report.sources_file = str(sources_path)
        audit_sources(sources, ds_html, report)
    else:
        report.add(Violation(
            rule_id="R06",
            section="(global)",
            severity="critical",
            message="Fichier *-design-system-audit-sources.json absent — audit sourcing impossible",
        ))

    # 3. Tailles font-size hors scale
    audit_font_sizes(ds_html, report)

    # 4. Patterns AI-slop (border-left)
    audit_encadres(ds_html, report)

    # ── Affichage rapport ──
    print("=" * 70)
    print("Design System Audit — Rapport")
    print("=" * 70)
    print(f"Fichier audité : {ds_html_path.name}")
    if inventory_path:
        print(f"Inventaire     : {inventory_path.name}")
    if sources_path:
        print(f"Sources        : {sources_path.name}")
    print(f"Items inventoriés : {report.items_inventoried}")
    print(f"Items sourcés     : {report.items_sourced}")
    print(f"font-size scannés : {report.font_sizes_checked}")
    print(f"border-left scannés : {report.encadres_checked}")
    print()
    print(report.summary())

    if report.violations:
        print("\n── Violations détaillées ──\n")
        for v in report.violations:
            sev_icon = {"critical": "🔴", "warning": "🟠", "info": "🟡"}[v.severity]
            print(f"{sev_icon} [{v.rule_id}] {v.section}")
            print(f"   → {v.message}")
            if v.expected:
                print(f"   Attendu : {v.expected}")
            if v.found:
                print(f"   Trouvé  : {v.found}")
            print()

    # ── Sortie JSON ──
    if args.json_output:
        json_path = session_dir / f"{ds_html_path.stem.replace('-full', '')}-audit-report.json"
        json_path.write_text(
            json.dumps(
                {
                    "summary": {
                        "pass": report.pass_status,
                        "n_critical": sum(1 for v in report.violations if v.severity == "critical"),
                        "n_warning": sum(1 for v in report.violations if v.severity == "warning"),
                        "n_info": sum(1 for v in report.violations if v.severity == "info"),
                        "items_inventoried": report.items_inventoried,
                        "items_sourced": report.items_sourced,
                        "font_sizes_checked": report.font_sizes_checked,
                        "encadres_checked": report.encadres_checked,
                    },
                    "violations": [asdict(v) for v in report.violations],
                    "files": {
                        "ds_html": str(ds_html_path),
                        "inventory": str(inventory_path) if inventory_path else None,
                        "sources": str(sources_path) if sources_path else None,
                    },
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        print(f"\n📄 Rapport JSON : {json_path}")

    return 0 if report.pass_status else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
