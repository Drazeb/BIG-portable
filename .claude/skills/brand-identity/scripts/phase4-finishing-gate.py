#!/usr/bin/env python3
"""
Phase 4 Finishing Gate — BIG Style-Tile CSS Quality Verifier

Mechanically verifies 7 CSS finishing quality checks on a style-tile HTML file.
Usage: python3 phase4-finishing-gate.py path/to/style-tile.html <cursor_a> [--json-output PATH]

Exit code 0 = all PASS (WARNs are OK), exit code 1 = at least one FAIL.

Si --json-output est fourni, écrit en plus du stdout un JSON structuré complet
contenant Vague 1 (checks bloquants) + Vague 2 (warnings informationnels), pour
que l'orchestrateur BIG puisse passer les WARN Vague 2 aux Critiques sémantiques
sans shortcut du résumé stdout (cf. SKILL.md zone Étape 4A-loop).
"""

import argparse
import datetime
import hashlib
import json
import re
import sys
from typing import NamedTuple


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_css_comments(css: str) -> str:
    """Remove /* ... */ comments from CSS, preserving line numbers (replace with spaces)."""
    def replace_with_newlines(match):
        return re.sub(r'[^\n]', ' ', match.group(0))
    return re.sub(r'/\*.*?\*/', replace_with_newlines, css, flags=re.DOTALL)


def extract_css(html: str) -> str:
    """Extract all CSS between <style> tags, concatenated."""
    blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
    return '\n'.join(blocks)


def line_number_at(text: str, pos: int) -> int:
    """Return 1-based line number for a character position in text."""
    return text[:pos].count('\n') + 1


def split_top_level(value: str, sep: str = ',') -> list[str]:
    """Split a CSS value by sep, but only at top-level (not inside parentheses)."""
    parts = []
    depth = 0
    current = []
    for ch in value:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth = max(0, depth - 1)
        if ch == sep and depth == 0:
            parts.append(''.join(current).strip())
            current = []
        else:
            current.append(ch)
    tail = ''.join(current).strip()
    if tail:
        parts.append(tail)
    return parts


# ---------------------------------------------------------------------------
# Result tracking
# ---------------------------------------------------------------------------

class CheckResult(NamedTuple):
    status: str   # "PASS", "FAIL", "WARN"
    label: str
    summary: str
    details: list[str]


# ---------------------------------------------------------------------------
# Check 1: Hover multi-property
# ---------------------------------------------------------------------------

def check_hover_multi_property(css: str) -> CheckResult:
    """Every :hover block must set >= 2 distinct CSS properties."""
    label = "Hover multi-property"
    # Match :hover { ... } blocks (handles nested braces simply via non-greedy on first })
    # We look for selector:hover ... { ... }
    pattern = re.compile(r':hover\s*\{([^}]*)\}', re.DOTALL)
    failures = []
    total = 0

    for m in pattern.finditer(css):
        total += 1
        block = m.group(1)
        # Extract property names (lines like "  property: value;")
        props = re.findall(r'([\w-]+)\s*:', block)
        # Deduplicate
        unique_props = set(props)
        if len(unique_props) < 2:
            ln = line_number_at(css, m.start())
            single = ', '.join(unique_props) if unique_props else '(vide)'
            failures.append(f"Ligne {ln}: :hover ne définit que {single}")

    if total == 0:
        return CheckResult("PASS", label, "aucune règle :hover trouvée", [])
    if failures:
        return CheckResult("FAIL", label, f"{len(failures)}/{total} règle(s) avec < 2 propriétés", failures)
    return CheckResult("PASS", label, f"{total}/{total} rules OK", [])


# ---------------------------------------------------------------------------
# Check 2: clip-path OR mask-image present
# ---------------------------------------------------------------------------

def check_clip_or_mask(css: str, cursor_a: int) -> CheckResult:
    """Check clip-path or mask-image is present in the CSS."""
    label = "clip-path ou mask-image"
    found_clip = bool(re.search(r'clip-path\s*:', css))
    found_mask = bool(re.search(r'mask-image\s*:', css))

    if found_clip or found_mask:
        which = []
        if found_clip:
            which.append("clip-path")
        if found_mask:
            which.append("mask-image")
        return CheckResult("PASS", label, f"trouvé: {', '.join(which)}", [])

    # WARN pour tous les niveaux — le socle technique est identique quel que soit A.
    # Le quota de 4 techniques avancées (check_advanced_techniques) couvre déjà ce cas.
    return CheckResult(
        "WARN", label,
        f"absent (cursor A={cursor_a} — informatif)",
        ["clip-path / mask-image absent — le quota de techniques avancées reste le filet de sécurité"],
    )


# ---------------------------------------------------------------------------
# Check 3: No generic ease
# ---------------------------------------------------------------------------

def check_no_generic_ease(css: str) -> CheckResult:
    """No standalone 'ease' or 'ease-in-out' in transition/animation properties."""
    label = "Easing physiques"
    # Find transition: and animation: declarations with their values
    # We match property: value up to ; or }
    pattern = re.compile(
        r'(transition|animation)\s*:\s*([^;{}]+)',
        re.IGNORECASE,
    )
    failures = []

    for m in pattern.finditer(css):
        value = m.group(2).strip()
        # Skip if value is just a var() reference
        if re.match(r'^var\(', value.strip()):
            continue
        # Check for standalone ease or ease-in-out
        # Must not be inside cubic-bezier() or var(--)
        # Strategy: remove cubic-bezier(...) and var(...) occurrences, then check
        cleaned = re.sub(r'cubic-bezier\([^)]*\)', '', value)
        cleaned = re.sub(r'var\([^)]*\)', '', cleaned)
        # Now look for standalone ease or ease-in-out as whole words
        if re.search(r'\bease-in-out\b', cleaned) or re.search(r'\bease\b(?!-)', cleaned):
            ln = line_number_at(css, m.start())
            full_decl = f"{m.group(1)}: {value}"
            failures.append(f"Ligne {ln}: {full_decl}")

    if failures:
        return CheckResult("FAIL", label, f"{len(failures)} generic ease trouvé(s)", failures)
    return CheckResult("PASS", label, "0 generic ease found", [])


# ---------------------------------------------------------------------------
# Check 4: Box-shadow multi-layer
# ---------------------------------------------------------------------------

def check_box_shadow_layers(css: str) -> CheckResult:
    """Every box-shadow (non-none) must have >= 2 comma-separated layers."""
    label = "Box-shadow multi-layer"
    pattern = re.compile(r'box-shadow\s*:\s*([^;{}]+)', re.IGNORECASE)
    failures = []
    total = 0

    for m in pattern.finditer(css):
        value = m.group(1).strip()
        # Skip none or var() references
        if value.lower() == 'none' or value.startswith('var('):
            continue
        # Skip inset-only (single inset keyword, no real shadow values beyond that)
        if value.strip().lower() == 'inset':
            continue
        total += 1
        layers = split_top_level(value, ',')
        if len(layers) < 2:
            ln = line_number_at(css, m.start())
            failures.append(f"Ligne {ln}: box-shadow: {value} — ajouter ≥1 couche")

    if failures:
        return CheckResult("FAIL", label, f"{len(failures)} shadow(s) simple(s) found", failures)
    summary = f"{total}/{total} OK" if total else "aucun box-shadow trouvé"
    return CheckResult("PASS", label, summary, [])


# ---------------------------------------------------------------------------
# Check 5: Padding-block varied across 3 main sections
# ---------------------------------------------------------------------------

def check_padding_block_varied(css: str) -> CheckResult:
    """The 3 main sections (voice, artifact/witness, atmosphere) must have different padding-block."""
    label = "Padding-block varié"
    # Map section keywords to regex patterns for class selectors
    sections = {
        'voice': re.compile(r'\.\w*voice\w*', re.IGNORECASE),
        'artifact': re.compile(r'\.\w*(?:artifact|artefact|witness)\w*', re.IGNORECASE),
        'atmosphere': re.compile(r'\.\w*atmosphere\w*', re.IGNORECASE),
    }

    # Build a map: section -> list of padding-block values found
    section_paddings: dict[str, list[str]] = {k: [] for k in sections}

    # Find all rule blocks: selector { ... }
    # We iterate through the CSS finding selectors and their blocks
    # Use a simple brace-matching approach
    rule_pattern = re.compile(r'([^{}]+?)\{([^{}]*)\}', re.DOTALL)

    for m in rule_pattern.finditer(css):
        selector = m.group(1).strip()
        block = m.group(2)
        for section_name, sec_pattern in sections.items():
            if sec_pattern.search(selector):
                # Look for padding-block in this block
                pb_match = re.search(r'padding-block\s*:\s*([^;]+)', block)
                if pb_match:
                    section_paddings[section_name].append(pb_match.group(1).strip())

    # Check we found values for at least 2 sections
    found = {k: v for k, v in section_paddings.items() if v}
    if len(found) < 2:
        return CheckResult(
            "PASS", label,
            f"seulement {len(found)} section(s) trouvée(s) — check non applicable",
            [],
        )

    # Check for duplicates among the first value of each found section
    value_to_sections: dict[str, list[str]] = {}
    for section_name, values in found.items():
        val = values[0]  # take first padding-block found for this section
        value_to_sections.setdefault(val, []).append(section_name)

    duplicates = {v: secs for v, secs in value_to_sections.items() if len(secs) > 1}
    if duplicates:
        details = []
        for val, secs in duplicates.items():
            details.append(f"{', '.join(secs)} partagent padding-block: {val}")
        return CheckResult("FAIL", label, "valeurs identiques détectées", details)

    return CheckResult("PASS", label, f"{len(found)} valeurs distinctes", [])


# ---------------------------------------------------------------------------
# Check 6: @keyframes referenced
# ---------------------------------------------------------------------------

def check_keyframes_referenced(css: str) -> CheckResult:
    """Every @keyframes name must be referenced in an animation property."""
    label = "@keyframes référencés"
    # Find all @keyframes declarations
    kf_names = re.findall(r'@keyframes\s+([\w-]+)', css)
    if not kf_names:
        return CheckResult("PASS", label, "aucun @keyframes déclaré", [])

    orphans = []
    for name in kf_names:
        # Check for animation-name: <name> or animation: ... <name>
        # Look for the name as a word boundary match in animation properties
        ref_pattern = re.compile(
            r'animation(?:-name)?\s*:[^;{}]*\b' + re.escape(name) + r'\b',
            re.IGNORECASE,
        )
        if not ref_pattern.search(css):
            orphans.append(name)

    if orphans:
        return CheckResult(
            "FAIL", label,
            f"{len(orphans)}/{len(kf_names)} non référencé(s)",
            [f"@keyframes {n} — déclaré mais jamais utilisé" for n in orphans],
        )
    return CheckResult("PASS", label, f"{len(kf_names)}/{len(kf_names)} OK", [])


# ---------------------------------------------------------------------------
# Check 7: :root variables used
# ---------------------------------------------------------------------------

def check_root_variables_used(css: str) -> CheckResult:
    """Every --var declared in :root must appear as var(--var) somewhere outside :root."""
    label = ":root variables"
    # Extract the :root block(s)
    # Handle :root { ... } possibly inside @layer
    root_pattern = re.compile(r':root\s*\{([^}]*)\}', re.DOTALL)
    root_blocks = []
    root_spans = []
    for m in root_pattern.finditer(css):
        root_blocks.append(m.group(1))
        root_spans.append((m.start(), m.end()))

    if not root_blocks:
        return CheckResult("PASS", label, "aucun :root trouvé", [])

    # Collect all variable declarations in :root
    declared_vars = set()
    for block in root_blocks:
        for var_match in re.finditer(r'--([\w-]+)\s*:', block):
            declared_vars.add(var_match.group(1))

    if not declared_vars:
        return CheckResult("PASS", label, "aucune variable dans :root", [])

    # Build CSS without :root blocks to search for references
    css_without_root = css
    # Remove root blocks from the search (replace with spaces to preserve positions)
    for start, end in reversed(root_spans):
        css_without_root = css_without_root[:start] + ' ' * (end - start) + css_without_root[end:]

    unused = []
    for var_name in sorted(declared_vars):
        # Check for var(--var_name) outside :root
        pattern = re.compile(r'var\(\s*--' + re.escape(var_name) + r'[\s,)]')
        if not pattern.search(css_without_root):
            unused.append(f"--{var_name}")

    if unused:
        status = "WARN"
        details = [f"{v} (déclarée mais jamais référencée)" for v in unused]
        return CheckResult(status, label, f"{len(unused)} non utilisée(s)", details)

    return CheckResult("PASS", label, f"{len(declared_vars)}/{len(declared_vars)} OK", [])


# ---------------------------------------------------------------------------
# Check 8: Advanced CSS techniques quota by cursor A
# ---------------------------------------------------------------------------

ADVANCED_TECHNIQUES = [
    (r'@property\s', '@property animé', lambda css: bool(
        re.search(r'@property\s', css) and
        # Check it's actually used in a @keyframes or transition, not just declared
        (re.search(r'@keyframes\s+\w+\s*\{[^}]*--', css) or
         re.search(r'transition\s*:[^;]*--', css))
    )),
    (r'clip-path\s*:', 'clip-path', None),
    (r'mask-image\s*:', 'mask-image', None),
    (r'@starting-style', '@starting-style', None),
    (r'backdrop-filter\s*:', 'backdrop-filter', None),
    (r'mix-blend-mode\s*:', 'mix-blend-mode', None),
    (r':has\(', ':has()', None),
    (r'animation-timeline\s*:', 'animation-timeline: view()', None),
    (r'container-type\s*:', '@container', None),
]

# Minimum required — same for all cursor A values (fabrication quality, not audacity)
TECHNIQUE_QUOTA = {1: 4, 2: 4, 3: 4}


def check_advanced_techniques(css: str, cursor_a: int) -> CheckResult:
    """Check that enough advanced CSS techniques are used for the cursor A level."""
    label = "Techniques CSS avancées"
    quota = TECHNIQUE_QUOTA.get(cursor_a, 0)

    if quota == 0:
        return CheckResult("PASS", label, f"cursor A={cursor_a} — pas de quota", [])

    found = []
    missing = []

    for pattern, name, custom_check in ADVANCED_TECHNIQUES:
        if custom_check:
            present = custom_check(css)
        else:
            present = bool(re.search(pattern, css))

        if present:
            found.append(name)
        else:
            missing.append(name)

    if len(found) >= quota:
        return CheckResult(
            "PASS", label,
            f"{len(found)}/{quota} requis — trouvé: {', '.join(found)}",
            [],
        )
    else:
        details = [
            f"Trouvé ({len(found)}): {', '.join(found) if found else 'aucune'}",
            f"Manquantes: {', '.join(missing)}",
            f"Ajouter au moins {quota - len(found)} technique(s) parmi les manquantes",
        ]
        return CheckResult(
            "FAIL", label,
            f"{len(found)}/{quota} requis (cursor A={cursor_a})",
            details,
        )


# ===========================================================================
# Vague 2 anti-slop — Checks supplémentaires (mode WARN par défaut)
#
# Ces checks démarrent en WARN : ils loguent mais ne bloquent pas la livraison.
# À promouvoir en FAIL après 5 runs sans faux positif.
# Source : ref/plan-vague2-point1-regles-negatives-externes.md
# ===========================================================================


# ---- Bloc Couleur ---------------------------------------------------------

def check_R005_no_pure_black_white(css: str, html: str) -> CheckResult:
    """R-005 | NO pure black/white sur surfaces principales."""
    label = "R-005 NO pure black/white"
    findings = []
    # Extract :root block(s)
    root_blocks = re.findall(r':root\s*\{([^}]*)\}', css, re.DOTALL)
    root_text = '\n'.join(root_blocks)
    # Look for pure black/white in :root color/background tokens
    for line_num, line in enumerate(css.split('\n'), 1):
        # Only check lines with color-ish properties or token names
        if re.search(r'(background|color|--color|--bg|--surface|--text|--ink)', line, re.IGNORECASE):
            if (re.search(r'(?<![\w-])#000(?![0-9a-fA-F])', line) or
                re.search(r'(?<![\w-])#fff(?![0-9a-fA-F])', line, re.IGNORECASE) or
                re.search(r'rgb\s*\(\s*0\s*,\s*0\s*,\s*0\s*\)', line) or
                re.search(r'rgb\s*\(\s*255\s*,\s*255\s*,\s*255\s*\)', line)):
                findings.append(f"Ligne {line_num}: {line.strip()[:80]}")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} occurrence(s) de noir/blanc pur",
                          findings[:5])
    return CheckResult("PASS", label, "aucun noir/blanc pur sur surfaces", [])


def check_R009_alpha_excess(css: str) -> CheckResult:
    """R-009 | Alpha abusif (>8 occurrences rgba/hsla)."""
    label = "R-009 alpha-channel abuse"
    rgba_count = len(re.findall(r'rgba\s*\(', css))
    hsla_count = len(re.findall(r'hsla\s*\(', css))
    total = rgba_count + hsla_count
    if total > 8:
        return CheckResult("WARN", label, f"{total} occurrences (max recommandé 8)",
                          [f"rgba: {rgba_count}, hsla: {hsla_count} — préférer oklch() ou color-mix()"])
    return CheckResult("PASS", label, f"{total} occurrence(s)", [])


def check_R001_oklch_preferred(css: str) -> CheckResult:
    """R-001 | OKLCH préféré, alerter HSL/RGB sur tokens majeurs."""
    label = "R-001 OKLCH preferred"
    # Look in :root or --color-* declarations
    root_blocks = re.findall(r':root\s*\{([^}]*)\}', css, re.DOTALL)
    findings = []
    for block in root_blocks:
        for line in block.split('\n'):
            # Token line with hsl/rgb (not oklch)
            if re.search(r'--(color|bg|surface|ink|text|accent|brand)[\w-]*\s*:', line, re.IGNORECASE):
                if (re.search(r'\bhsl\s*\(', line) or
                    re.search(r'\brgb\s*\(', line)) and not re.search(r'oklch', line):
                    findings.append(line.strip()[:90])
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} token(s) en HSL/RGB",
                          findings[:5] + ["Préférer oklch() pour la cohérence perceptuelle"])
    return CheckResult("PASS", label, "tokens en oklch() ou aucun token couleur HSL/RGB", [])


def check_R147_color_scheme_dark(css: str) -> CheckResult:
    """R-147 | color-scheme: dark sur html si thème sombre."""
    label = "R-147 color-scheme dark"
    # Detect dark theme via :root background or body background
    is_dark = False
    # Look for background in :root with low lightness
    root_blocks = re.findall(r':root\s*\{([^}]*)\}', css, re.DOTALL)
    for block in root_blocks:
        # oklch with L < 0.3 or hex starting with 0/1/2
        if re.search(r'(--bg|--background|--surface|--canvas)[\w-]*\s*:\s*oklch\s*\(\s*0?\.[012]', block):
            is_dark = True
            break
        if re.search(r'(--bg|--background|--surface|--canvas)[\w-]*\s*:\s*#[0-2][0-9a-fA-F]{2}\b', block):
            is_dark = True
            break
    if not is_dark:
        return CheckResult("PASS", label, "thème non-dark — check non applicable", [])
    has_color_scheme = bool(re.search(r'color-scheme\s*:\s*[^;]*\bdark\b', css))
    if not has_color_scheme:
        return CheckResult("WARN", label, "thème sombre détecté sans color-scheme",
                          ["Ajouter `color-scheme: dark` (ou `dark light`) sur html pour le rendu UA natif"])
    return CheckResult("PASS", label, "color-scheme déclaré", [])


def check_R148_meta_theme_color(html: str) -> CheckResult:
    """R-148 | meta theme-color présent."""
    label = "R-148 meta theme-color"
    if re.search(r'<meta\s+[^>]*name\s*=\s*["\']theme-color["\']', html, re.IGNORECASE):
        return CheckResult("PASS", label, "meta theme-color présent", [])
    return CheckResult("WARN", label, "<meta name=\"theme-color\"> absent",
                      ["Ajouter <meta name=\"theme-color\" content=\"...\"> pour la barre browser mobile"])


# ---- Bloc Typo / Fonts ---------------------------------------------------

BANNED_FONTS = [
    'Inter', 'Roboto', 'Open Sans', 'Lato', 'Montserrat',
    'Poppins', 'Source Sans', 'Nunito', 'Raleway', 'Ubuntu',
]


def check_R013_banned_fonts(html: str, css: str) -> CheckResult:
    """R-013 | Fonts bannies (Inter, Roboto, Open Sans, Lato, Montserrat, ...)."""
    label = "R-013 banned fonts"
    findings = []
    combined = html + '\n' + css
    for font in BANNED_FONTS:
        # Match in font-family, @import, Google Fonts URLs
        # Use word boundary; case-insensitive
        pattern = re.compile(
            r'(?:font-family\s*:[^;{}]*|@import[^;]*|fonts\.googleapis\.com[^"\']*|family=)[^"\';{}]*\b'
            + re.escape(font).replace(r'\ ', r'[\s+]') + r'\b',
            re.IGNORECASE,
        )
        if pattern.search(combined):
            findings.append(font)
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} font(s) bannie(s) détectée(s)",
                          [f"{f} — préférer une font éditoriale plus distinctive" for f in findings])
    return CheckResult("PASS", label, "aucune font bannie", [])


def check_R017_font_display_swap(css: str, html: str) -> CheckResult:
    """R-017 | font-display: swap pour minimiser CLS au chargement de fonte."""
    label = "R-017 font-display: swap"
    combined = css + '\n' + html
    has_external_fonts = bool(re.search(
        r'@font-face|fonts\.googleapis\.com|fonts\.gstatic\.com|<link[^>]*preload[^>]*font',
        combined,
        re.IGNORECASE,
    ))
    if not has_external_fonts:
        return CheckResult("PASS", label, "pas de fonte externe", [])
    has_swap = bool(re.search(
        r'font-display\s*:\s*swap|display=swap',
        combined,
        re.IGNORECASE,
    ))
    if has_swap:
        return CheckResult("PASS", label, "font-display: swap détecté", [])
    return CheckResult(
        "WARN", label, "fontes externes sans font-display: swap",
        ["Ajouter `font-display: swap;` dans @font-face ou `&display=swap` "
         "dans les URL Google Fonts (sinon FOIT — page blanche pendant le "
         "chargement de fonte)"],
    )


def check_R104_text_wrap(css: str) -> CheckResult:
    """R-104 | text-wrap: balance/pretty sur titres/paragraphes."""
    label = "R-104 text-wrap balance/pretty"
    has_wrap = bool(re.search(r'text-wrap\s*:\s*(balance|pretty)', css))
    if has_wrap:
        return CheckResult("PASS", label, "text-wrap balance/pretty présent", [])
    # Detect headings/paragraphs declarations
    has_heading_rules = bool(re.search(r'(?:^|\s)h[1-6]\s*[,{]', css, re.MULTILINE))
    if has_heading_rules:
        return CheckResult("WARN", label, "text-wrap absent sur titres/paragraphes",
                          ["Ajouter `text-wrap: balance` aux titres et `text-wrap: pretty` aux paragraphes"])
    return CheckResult("PASS", label, "pas de règles titres détectées", [])


def check_R105_tabular_nums(html: str, css: str) -> CheckResult:
    """R-105 | tabular-nums sur colonnes chiffrées."""
    label = "R-105 tabular-nums"
    # Detect <td> or <th> with digits
    has_numeric_table = False
    for m in re.finditer(r'<t[dh][^>]*>([^<]*)</t[dh]>', html, re.IGNORECASE):
        if re.search(r'\d', m.group(1)):
            has_numeric_table = True
            break
    if not has_numeric_table:
        return CheckResult("PASS", label, "aucun tableau numérique — check non applicable", [])
    has_tabular = bool(re.search(r'font-variant-numeric\s*:\s*[^;]*tabular-nums', css))
    if not has_tabular:
        return CheckResult("WARN", label, "tableau numérique sans tabular-nums",
                          ["Ajouter `font-variant-numeric: tabular-nums` sur les colonnes chiffrées"])
    return CheckResult("PASS", label, "tabular-nums présent", [])


# ---- Bloc Animations / Motion --------------------------------------------

def check_R035_bounce_elastic(css: str) -> CheckResult:
    """R-035 | NO bounce/elastic easing."""
    label = "R-035 bounce/elastic easing"
    findings = []
    # cubic-bezier with overshoot (>1.0 or <0.0 in y values)
    for m in re.finditer(r'cubic-bezier\s*\(\s*([\d.\-]+)\s*,\s*([\d.\-]+)\s*,\s*([\d.\-]+)\s*,\s*([\d.\-]+)\s*\)', css):
        try:
            y1 = float(m.group(2))
            y2 = float(m.group(4))
            if y1 > 1.0 or y1 < 0.0 or y2 > 1.0 or y2 < 0.0:
                ln = line_number_at(css, m.start())
                findings.append(f"Ligne {ln}: cubic-bezier overshoot ({m.group(0)})")
        except ValueError:
            pass
    # Keyword bounce/elastic
    for m in re.finditer(r'\b(bounce|elastic)\b', css, re.IGNORECASE):
        ln = line_number_at(css, m.start())
        # Skip if it's inside a name like "bounce-in" used as a class identifier
        context = css[max(0, m.start()-20):m.end()+20]
        if re.search(r'animation[^;]*\b(bounce|elastic)\b', context, re.IGNORECASE):
            findings.append(f"Ligne {ln}: keyword {m.group(1)} dans animation")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} easing avec overshoot/bounce",
                          findings[:5] + ["Préférer des courbes physiques sans overshoot"])
    return CheckResult("PASS", label, "aucun bounce/elastic", [])


def check_R036_animate_transform_opacity_only(css: str) -> CheckResult:
    """R-036 / R-127 | Animer ONLY transform/opacity (pas top/left/width/height/margin/padding)."""
    label = "R-036/R-127 animate transform/opacity only"
    findings = []
    # transition: <prop> ...
    for m in re.finditer(r'transition\s*:\s*([^;{}]+)', css):
        value = m.group(1).strip()
        if value.startswith('var('):
            continue
        # Check if the property part contains forbidden ones
        # Forbidden: top, left, right, bottom, width, height, margin, padding (not max-*)
        forbidden = re.findall(
            r'(?<![\w-])(top|left|right|bottom|width|height|margin|padding)(?!-w|-h)\b',
            value
        )
        # But allow max-width/max-height, min-width/min-height
        for f in forbidden:
            # check if preceded by "max-" or "min-"
            pass
        # Simpler: re-scan with stricter regex
        bad = re.findall(
            r'(?<![\w-])(?<!max-)(?<!min-)\b(top|left|right|bottom|width|height|margin|padding)\b',
            value
        )
        if bad:
            ln = line_number_at(css, m.start())
            findings.append(f"Ligne {ln}: transition: {value[:60]} — anime {', '.join(set(bad))}")
    # @keyframes that animate forbidden properties
    for m in re.finditer(r'@keyframes\s+([\w-]+)\s*\{([^@]*?)\n\s*\}', css, re.DOTALL):
        block = m.group(2)
        bad = re.findall(
            r'(?:^|\s)(?<!max-)(?<!min-)(top|left|right|bottom|width|height|margin|padding)\s*:',
            block, re.MULTILINE
        )
        if bad:
            ln = line_number_at(css, m.start())
            findings.append(f"Ligne {ln}: @keyframes {m.group(1)} anime {', '.join(set(bad))}")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} animation(s) hors transform/opacity",
                          findings[:5] + ["Animer uniquement transform et opacity pour la perf"])
    return CheckResult("PASS", label, "animations limitées à transform/opacity", [])


def check_R132_no_transition_all(css: str) -> CheckResult:
    """R-132 | NO transition: all."""
    label = "R-132 no transition: all"
    findings = []
    for m in re.finditer(r'transition\s*:\s*all\b', css):
        ln = line_number_at(css, m.start())
        findings.append(f"Ligne {ln}: transition: all — lister les propriétés explicitement")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} transition: all",
                          findings[:5])
    return CheckResult("PASS", label, "aucun transition: all", [])


def check_R042_will_change_excess(css: str) -> CheckResult:
    """R-042 | NO will-change preemptive (>3 occurrences)."""
    label = "R-042 will-change excess"
    count = len(re.findall(r'will-change\s*:', css))
    if count > 3:
        return CheckResult("WARN", label, f"{count} will-change (max recommandé 3)",
                          ["will-change preemptif coûte de la mémoire — réserver aux animations critiques"])
    return CheckResult("PASS", label, f"{count} occurrence(s)", [])


# ---- Bloc Layout / Responsive --------------------------------------------

def check_R024_spacing_tokens_semantic(css: str) -> CheckResult:
    """R-024 | Spacing tokens naming sémantique (pas --spacing-8)."""
    label = "R-024 spacing tokens naming"
    findings = []
    for m in re.finditer(r'--(spacing|space)-(\d+)\s*:', css):
        ln = line_number_at(css, m.start())
        findings.append(f"Ligne {ln}: --{m.group(1)}-{m.group(2)} — préférer --space-xs/sm/md/lg/xl")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} token(s) spacing numérique",
                          findings[:5])
    return CheckResult("PASS", label, "naming sémantique ou aucun token spacing numérique", [])


def check_R025_grid_minmax_responsive(css: str) -> CheckResult:
    """R-025 | Auto-fit minmax responsive grid."""
    label = "R-025 grid auto-fit minmax"
    has_grid = bool(re.search(r'display\s*:\s*grid', css))
    if not has_grid:
        return CheckResult("PASS", label, "pas de grid — check non applicable", [])
    has_auto = bool(re.search(r'repeat\s*\(\s*auto-(fit|fill)\s*,\s*minmax', css))
    if not has_auto:
        return CheckResult("WARN", label, "grid sans repeat(auto-fit, minmax(...))",
                          ["Préférer `repeat(auto-fit, minmax(Npx, 1fr))` pour une grille responsive sans media-queries"])
    return CheckResult("PASS", label, "grid auto-fit présente", [])


def check_R028_container_queries(css: str) -> CheckResult:
    """R-028 | Container queries presence (informationnel)."""
    label = "R-028 container queries"
    has_container = bool(re.search(r'@container\b', css))
    if has_container:
        return CheckResult("PASS", label, "@container présent", [])
    return CheckResult("WARN", label, "aucun @container",
                      ["Container queries (`@container`) recommandées pour composants modulaires"])


def check_R031_no_arbitrary_zindex(css: str) -> CheckResult:
    """R-031 | Z-index scale, no arbitrary 9999."""
    label = "R-031 z-index arbitraire"
    findings = []
    for m in re.finditer(r'z-index\s*:\s*(\d+)', css):
        try:
            val = int(m.group(1))
            if val >= 9000:
                ln = line_number_at(css, m.start())
                findings.append(f"Ligne {ln}: z-index: {val}")
        except ValueError:
            pass
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} z-index ≥ 9000",
                          findings[:5] + ["Définir une échelle de z-index sémantique (--z-modal, --z-toast...)"])
    return CheckResult("PASS", label, "pas de z-index arbitraire", [])


def check_R057_breakpoints_count(css: str) -> CheckResult:
    """R-057 | 3 breakpoints (info, alerter si >5)."""
    label = "R-057 breakpoints count"
    count = len(re.findall(r'@media\s*\([^)]*min-width', css))
    if count > 5:
        return CheckResult("WARN", label, f"{count} breakpoints (max recommandé 5)",
                          ["Trop de breakpoints = over-engineering. Préférer du fluid sizing (clamp)."])
    return CheckResult("PASS", label, f"{count} breakpoint(s)", [])


def check_R058_input_method_query(css: str) -> CheckResult:
    """R-058 | Input method detection (informationnel)."""
    label = "R-058 input method query"
    if re.search(r'@media\s*\([^)]*\b(pointer|hover)\s*:', css):
        return CheckResult("PASS", label, "@media pointer/hover présent", [])
    return CheckResult("WARN", label, "aucun @media pointer/hover",
                      ["Utiliser @media (pointer: fine/coarse) pour adapter aux écrans tactiles"])


def check_R059_safe_area_inset(html: str, css: str) -> CheckResult:
    """R-059 | Safe-area-inset usage sur sections full-bleed."""
    label = "R-059 safe-area-inset"
    has_full_bleed = bool(re.search(r'(100vw|100dvw|full-bleed|fullscreen)', css, re.IGNORECASE))
    if not has_full_bleed:
        return CheckResult("PASS", label, "pas de full-bleed détecté", [])
    if re.search(r'env\s*\(\s*safe-area-inset', css):
        return CheckResult("PASS", label, "safe-area-inset utilisé", [])
    return CheckResult("WARN", label, "full-bleed sans safe-area-inset",
                      ["Ajouter `padding: env(safe-area-inset-top) env(safe-area-inset-right) ...` sur sections full-bleed"])


def check_R138_overscroll_behavior(html: str, css: str) -> CheckResult:
    """R-138 | overscroll-behavior: contain sur modals."""
    label = "R-138 overscroll-behavior contain"
    has_modal = bool(re.search(r'(role\s*=\s*["\']dialog["\']|<dialog\b|\.modal\b)', html, re.IGNORECASE))
    if not has_modal:
        return CheckResult("PASS", label, "pas de modal — check non applicable", [])
    if re.search(r'overscroll-behavior\s*:\s*contain', css):
        return CheckResult("PASS", label, "overscroll-behavior: contain présent", [])
    return CheckResult("WARN", label, "modal sans overscroll-behavior: contain",
                      ["Ajouter `overscroll-behavior: contain` sur le modal pour éviter le scroll-chaining"])


# ---- Bloc A11y / Forms ---------------------------------------------------

def check_R045_inputs_labelled(html: str) -> CheckResult:
    """R-045 | Inputs avec label associé."""
    label = "R-045 input labels"
    findings = []
    inputs = re.findall(r'<input\b[^>]*>', html, re.IGNORECASE)
    for inp in inputs:
        # Skip hidden, submit, button
        type_m = re.search(r'type\s*=\s*["\']?(hidden|submit|button|reset)\b', inp, re.IGNORECASE)
        if type_m:
            continue
        # Check id linked to a label for=
        id_m = re.search(r'id\s*=\s*["\']([^"\']+)', inp)
        has_aria_label = bool(re.search(r'aria-label\s*=', inp, re.IGNORECASE))
        if has_aria_label:
            continue
        if id_m:
            input_id = id_m.group(1)
            if not re.search(r'<label[^>]+for\s*=\s*["\']' + re.escape(input_id) + r'["\']', html, re.IGNORECASE):
                findings.append(f"<input id=\"{input_id}\"> sans <label for=...>")
        else:
            findings.append(f"<input> sans id ni aria-label: {inp[:60]}")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} input(s) sans label",
                          findings[:5])
    return CheckResult("PASS", label, "tous les inputs ont un label", [])


def check_R048_native_dialog(html: str) -> CheckResult:
    """R-048 | Native <dialog> usage."""
    label = "R-048 native dialog"
    has_role_dialog = bool(re.search(r'role\s*=\s*["\']dialog["\']', html, re.IGNORECASE))
    has_native = bool(re.search(r'<dialog\b', html, re.IGNORECASE))
    if has_role_dialog and not has_native:
        return CheckResult("WARN", label, "role=\"dialog\" sans <dialog> natif",
                          ["Préférer l'élément natif <dialog> à role=\"dialog\""])
    return CheckResult("PASS", label, "native dialog ou pas de modal", [])


def check_R049_popover_api(html: str) -> CheckResult:
    """R-049 | Popover API usage (info)."""
    label = "R-049 popover API"
    if re.search(r'\bpopover\s*=', html, re.IGNORECASE):
        return CheckResult("PASS", label, "Popover API utilisée", [])
    return CheckResult("WARN", label, "Popover API absente (informationnel)", [])


def check_R051_anchor_positioning(css: str) -> CheckResult:
    """R-051 | CSS Anchor positioning (info)."""
    label = "R-051 CSS Anchor positioning"
    if re.search(r'(anchor-name|position-anchor)\s*:', css):
        return CheckResult("PASS", label, "Anchor positioning utilisé", [])
    return CheckResult("WARN", label, "Anchor positioning absent (informationnel)", [])


def check_R053_roving_tabindex(html: str) -> CheckResult:
    """R-053 | Roving tabindex pattern (info)."""
    label = "R-053 roving tabindex"
    has_tabindex = bool(re.search(r'tabindex\s*=\s*["\']-?[01]["\']', html))
    if has_tabindex:
        return CheckResult("PASS", label, "tabindex présent", [])
    return CheckResult("WARN", label, "aucun tabindex (informationnel — vérifier patterns clavier)", [])


def check_R054_skip_link(html: str) -> CheckResult:
    """R-054 | Skip link presence."""
    label = "R-054 skip link"
    has_skip = bool(re.search(
        r'<a\s+[^>]*(?:href\s*=\s*["\']#main|class\s*=\s*["\'][^"\']*\bskip\b)',
        html, re.IGNORECASE
    ))
    if has_skip:
        return CheckResult("PASS", label, "skip link présent", [])
    return CheckResult("WARN", label, "skip link absent",
                      ["Ajouter <a href=\"#main\" class=\"skip-link\">Aller au contenu</a> en début de body"])


def check_R067_R142_icon_buttons_aria_label(html: str) -> CheckResult:
    """R-067 + R-142 | Icon buttons doivent avoir aria-label (FUSION DOUBLON)."""
    label = "R-067/R-142 icon button aria-label"
    findings = []
    for m in re.finditer(r'<button\b([^>]*)>(.*?)</button>', html, re.DOTALL | re.IGNORECASE):
        attrs = m.group(1)
        inner = m.group(2).strip()
        # Strip svg
        text_only = re.sub(r'<svg\b.*?</svg>', '', inner, flags=re.DOTALL | re.IGNORECASE)
        text_only = re.sub(r'<[^>]+>', '', text_only).strip()
        has_text = bool(text_only)
        has_svg_or_icon = bool(re.search(r'<svg\b|class\s*=\s*["\'][^"\']*icon', inner, re.IGNORECASE))
        has_aria_label = bool(re.search(r'aria-label\s*=', attrs, re.IGNORECASE))
        if has_svg_or_icon and not has_text and not has_aria_label:
            findings.append(f"<button> icon-only sans aria-label: {m.group(0)[:80]}")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} bouton(s) icon-only sans aria-label",
                          findings[:5])
    return CheckResult("PASS", label, "tous les boutons icon-only sont labélisés", [])


def check_R068_alt_text(html: str) -> CheckResult:
    """R-068 | Alt text non vide pour images non-décoratives."""
    label = "R-068 image alt text"
    findings = []
    for m in re.finditer(r'<img\b([^>]*)>', html, re.IGNORECASE):
        attrs = m.group(1)
        alt_m = re.search(r'\balt\s*=\s*["\']([^"\']*)["\']', attrs, re.IGNORECASE)
        is_decorative = bool(re.search(r'class\s*=\s*["\'][^"\']*\b(decorative|decoration)\b', attrs, re.IGNORECASE))
        is_aria_hidden = bool(re.search(r'aria-hidden\s*=\s*["\']true["\']', attrs, re.IGNORECASE))
        if not alt_m:
            findings.append(f"<img> sans attribut alt: {m.group(0)[:80]}")
        elif alt_m.group(1).strip() == '' and not is_decorative and not is_aria_hidden:
            findings.append(f"<img> alt vide (non décoratif): {m.group(0)[:80]}")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} image(s) sans alt valide",
                          findings[:5])
    return CheckResult("PASS", label, "alt text OK sur toutes les images", [])


def check_R166_headings_hierarchy(html: str) -> CheckResult:
    """R-166 | Headings h1-h6 hiérarchiques."""
    label = "R-166 headings hierarchy"
    headings = re.findall(r'<h([1-6])\b', html, re.IGNORECASE)
    if not headings:
        return CheckResult("PASS", label, "aucun heading", [])
    levels = [int(h) for h in headings]
    skips = []
    prev = levels[0]
    for i, lvl in enumerate(levels[1:], 1):
        if lvl > prev + 1:
            skips.append(f"h{prev} → h{lvl} (saut de niveau)")
        prev = lvl
    if skips:
        return CheckResult("WARN", label, f"{len(skips)} saut(s) de niveau",
                          skips[:5])
    return CheckResult("PASS", label, f"{len(headings)} headings hiérarchiques", [])


def check_R169_aria_live(html: str) -> CheckResult:
    """R-169 | aria-live polite sur async updates."""
    label = "R-169 aria-live"
    has_async = bool(re.search(r'\b(toast|notification|alert|status|live-region)\b', html, re.IGNORECASE))
    if not has_async:
        return CheckResult("PASS", label, "pas de zone async — check non applicable", [])
    if re.search(r'aria-live\s*=\s*["\'](polite|assertive)["\']', html, re.IGNORECASE):
        return CheckResult("PASS", label, "aria-live présent", [])
    return CheckResult("WARN", label, "zone async sans aria-live",
                      ["Ajouter aria-live=\"polite\" sur les zones de notification/toast"])


def check_R172_interactive_states(css: str) -> CheckResult:
    """R-172 | Interactive states contrast (présence :hover/:focus/:active)."""
    label = "R-172 interactive states"
    hover_count = len(re.findall(r':hover\b', css))
    focus_count = len(re.findall(r':focus\b', css))
    active_count = len(re.findall(r':active\b', css))
    missing = []
    if hover_count == 0:
        missing.append(":hover")
    if focus_count == 0:
        missing.append(":focus / :focus-visible")
    if active_count == 0:
        missing.append(":active")
    if missing:
        return CheckResult("WARN", label, f"{len(missing)} état(s) manquant(s)",
                          [f"Aucun {m} dans le CSS" for m in missing])
    return CheckResult("PASS", label, f"hover={hover_count} focus={focus_count} active={active_count}", [])


# ---- Bloc Performance ----------------------------------------------------

def check_R060_srcset_sizes(html: str) -> CheckResult:
    """R-060 | srcset+sizes sur images >400px."""
    label = "R-060 srcset+sizes"
    findings = []
    for m in re.finditer(r'<img\b([^>]*)>', html, re.IGNORECASE):
        attrs = m.group(1)
        w_m = re.search(r'\bwidth\s*=\s*["\']?(\d+)', attrs)
        if w_m and int(w_m.group(1)) > 400:
            has_srcset = bool(re.search(r'\bsrcset\s*=', attrs, re.IGNORECASE))
            has_sizes = bool(re.search(r'\bsizes\s*=', attrs, re.IGNORECASE))
            if not (has_srcset and has_sizes):
                findings.append(f"<img width={w_m.group(1)}> sans srcset+sizes")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} image(s) >400px sans srcset",
                          findings[:5])
    return CheckResult("PASS", label, "srcset/sizes OK ou pas d'images >400px", [])


def check_R130_picture_art_direction(html: str) -> CheckResult:
    """R-130 | Picture art direction (info)."""
    label = "R-130 picture art direction"
    if re.search(r'<picture\b', html, re.IGNORECASE):
        return CheckResult("PASS", label, "<picture> utilisé", [])
    img_count = len(re.findall(r'<img\b', html, re.IGNORECASE))
    if img_count > 3:
        return CheckResult("WARN", label, f"{img_count} <img> sans <picture>",
                          ["<picture> recommandé pour art direction (crop différent par viewport)"])
    return CheckResult("PASS", label, "peu d'images — check non applicable", [])


def check_R131_image_dimensions_lazy(html: str) -> CheckResult:
    """R-131 | Image width+height + loading=lazy."""
    label = "R-131 image dimensions + lazy"
    findings = []
    for m in re.finditer(r'<img\b([^>]*)>', html, re.IGNORECASE):
        attrs = m.group(1)
        has_w = bool(re.search(r'\bwidth\s*=', attrs, re.IGNORECASE))
        has_h = bool(re.search(r'\bheight\s*=', attrs, re.IGNORECASE))
        has_lazy = bool(re.search(r'loading\s*=\s*["\']lazy["\']', attrs, re.IGNORECASE))
        if not (has_w and has_h):
            findings.append(f"<img> sans width/height: {m.group(0)[:60]}")
        elif not has_lazy:
            findings.append(f"<img> sans loading=\"lazy\": {m.group(0)[:60]}")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} image(s) sans dim/lazy",
                          findings[:5])
    return CheckResult("PASS", label, "toutes les images ont width/height + lazy", [])


def check_R133_large_lists_virtualize(html: str, css: str) -> CheckResult:
    """R-133 | Large lists virtualize (content-visibility: auto)."""
    label = "R-133 large lists virtualize"
    # Rough heuristic: count <li> in any single list
    list_blocks = re.findall(r'<(ul|ol)\b[^>]*>(.*?)</\1>', html, re.DOTALL | re.IGNORECASE)
    has_large = False
    for tag, inner in list_blocks:
        li_count = len(re.findall(r'<li\b', inner, re.IGNORECASE))
        if li_count > 50:
            has_large = True
            break
    if not has_large:
        return CheckResult("PASS", label, "pas de grande liste — check non applicable", [])
    if re.search(r'content-visibility\s*:\s*auto', css):
        return CheckResult("PASS", label, "content-visibility: auto présent", [])
    return CheckResult("WARN", label, "grande liste sans content-visibility",
                      ["Ajouter `content-visibility: auto` aux items de longues listes"])


# ---- Bloc Compositions interdites (visuelles) ----------------------------

def check_R081_side_stripe_borders(css: str) -> CheckResult:
    """R-081 | Side-stripe borders >1px sur cartes."""
    label = "R-081 side-stripe borders"
    findings = []
    for m in re.finditer(
        r'border-(?:left|right|inline-start|inline-end)\s*:\s*([2-9]|[1-9]\d+)px\s+solid',
        css
    ):
        ln = line_number_at(css, m.start())
        findings.append(f"Ligne {ln}: border latérale {m.group(1)}px")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} side-stripe border(s)",
                          findings[:5] + ["Préférer un fond contrasté à un trait latéral épais"])
    return CheckResult("PASS", label, "pas de side-stripe border", [])


def check_R082_gradient_text(css: str) -> CheckResult:
    """R-082 | Gradient text (background-clip: text)."""
    label = "R-082 gradient text"
    findings = []
    # background-clip: text combiné avec gradient sur le même selecteur (heuristique simple)
    # Iterate rule blocks
    for m in re.finditer(r'\{([^{}]*)\}', css):
        block = m.group(1)
        has_clip_text = bool(re.search(r'background-clip\s*:\s*text|-webkit-background-clip\s*:\s*text', block))
        has_gradient = bool(re.search(r'(linear|conic|radial)-gradient', block))
        if has_clip_text and has_gradient:
            ln = line_number_at(css, m.start())
            findings.append(f"Ligne {ln}: background-clip:text + gradient")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} gradient text",
                          findings[:5] + ["Préférer une couleur unie ou un effet typo plus original"])
    return CheckResult("PASS", label, "pas de gradient text", [])


def check_R108_no_emojis(html: str, css: str) -> CheckResult:
    """R-108 | NO emojis in code/markup."""
    label = "R-108 no emojis"
    # Strip <svg>...</svg> first
    cleaned = re.sub(r'<svg\b.*?</svg>', '', html + '\n' + css, flags=re.DOTALL | re.IGNORECASE)
    # Match common emoji ranges
    emoji_pattern = re.compile(
        r'[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F600-\U0001F64F]'
    )
    matches = emoji_pattern.findall(cleaned)
    if matches:
        unique = list(set(matches))[:10]
        return CheckResult("WARN", label, f"{len(matches)} emoji(s) trouvé(s)",
                          [f"Emojis: {' '.join(unique)}", "Préférer des SVG ou icônes maîtrisés"])
    return CheckResult("PASS", label, "aucun emoji", [])


def check_R109_no_lucide_default(html: str, css: str) -> CheckResult:
    """R-109 | NO Lucide icon library default."""
    label = "R-109 no Lucide default"
    combined = html + '\n' + css
    if re.search(r'(from\s+["\']lucide|<i\s+[^>]*class[^>]*lucide|lucide-icon)', combined, re.IGNORECASE):
        return CheckResult("WARN", label, "Lucide détecté",
                          ["Lucide est devenue cliché — préférer des icônes custom ou Phosphor/Iconoir"])
    return CheckResult("PASS", label, "pas de Lucide", [])


def check_R114_custom_cursors(css: str) -> CheckResult:
    """R-114 | NO custom mouse cursors."""
    label = "R-114 no custom cursor"
    findings = []
    for m in re.finditer(r'cursor\s*:\s*url\(', css):
        ln = line_number_at(css, m.start())
        findings.append(f"Ligne {ln}: cursor: url(...)")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} custom cursor(s)",
                          findings[:5] + ["Les curseurs custom dégradent l'UX"])
    return CheckResult("PASS", label, "pas de custom cursor", [])


# ---- Bloc Copy / Content -------------------------------------------------

AI_CLICHES = [
    'elevate', 'seamless', 'unleash', 'next-gen', 'next gen',
    'game-changer', 'game-changing', 'gamechanger', 'gamechanging',
    'delve', 'leverage', 'empowering', 'cutting-edge', 'cutting edge',
    'revolutionize', 'revolutionizing', 'disrupt', 'disruptive',
    'paradigm', 'synergy', 'synergize',
]


def check_R076_R117_ai_cliches(html: str) -> CheckResult:
    """R-076 + R-117 | AI clichés (FUSION DOUBLON)."""
    label = "R-076/R-117 AI clichés"
    # Strip script/style
    text = re.sub(r'<(script|style)\b.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    findings = []
    for cliche in AI_CLICHES:
        pattern = re.compile(r'\b' + re.escape(cliche).replace(r'\ ', r'[\s-]?') + r'\b', re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            findings.append(f"\"{cliche}\" ({len(matches)}x)")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} cliché(s) AI détecté(s)",
                          findings[:8] + ["Reformuler avec un vocabulaire spécifique au métier"])
    return CheckResult("PASS", label, "aucun cliché AI", [])


GENERIC_NAMES = [
    r'John Doe', r'Jane Doe', r'Acme(?:\s+Corp)?', r'Nexus',
    r'SmartFlow', r'Lorem ipsum', r'TechCorp', r'FinanceFirst',
]


def check_R115_generic_names(html: str) -> CheckResult:
    """R-115 | Generic names placeholder."""
    label = "R-115 generic names"
    text = re.sub(r'<(script|style)\b.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    findings = []
    for name in GENERIC_NAMES:
        pattern = re.compile(r'\b' + name + r'\b', re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            findings.append(f"\"{matches[0]}\" ({len(matches)}x)")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} nom(s) générique(s)",
                          findings[:5] + ["Utiliser des noms spécifiques au persona/secteur"])
    return CheckResult("PASS", label, "aucun nom générique", [])


def check_R116_fake_round_numbers(html: str) -> CheckResult:
    """R-116 | Fake round numbers (99.99%, 100%, 50% faster)."""
    label = "R-116 fake round numbers"
    text = re.sub(r'<(script|style)\b.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    findings = []
    patterns = [
        (r'\b99\.99\s*%', '99.99%'),
        (r'\b100\.00\s*%', '100.00%'),
        (r'\$100\.00\b', '$100.00'),
        (r'\b50\s*%\s+(faster|cheaper|better|stronger|smarter)\b', '50% faster/cheaper/better'),
        (r'\b10x\s+(faster|cheaper|better|productivity)\b', '10x faster/...'),
    ]
    for pat, label_p in patterns:
        if re.search(pat, text, re.IGNORECASE):
            findings.append(label_p)
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} chiffre(s) suspect(s)",
                          findings[:5] + ["Préférer des données spécifiques et crédibles"])
    return CheckResult("PASS", label, "pas de chiffres clichés", [])


def check_R118_broken_image_links(html: str) -> CheckResult:
    """R-118 | Broken image links (URLs externes non placeholder)."""
    label = "R-118 broken image links"
    findings = []
    for m in re.finditer(r'<img\b[^>]*\bsrc\s*=\s*["\'](https?://[^"\']+)', html, re.IGNORECASE):
        url = m.group(1)
        if not re.search(r'(picsum|placeholder|placehold|unsplash\.com/photos|images\.unsplash)', url, re.IGNORECASE):
            findings.append(url[:80])
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} URL(s) image suspecte(s)",
                          findings[:5] + ["Vérifier que les URLs résolvent — préférer placeholders connus"])
    return CheckResult("PASS", label, "aucun lien image suspect", [])


def check_R158_R159_typography(html: str) -> CheckResult:
    """R-158 + R-159 | Curly quotes / ellipsis / nbsp (FUSION DOUBLON)."""
    label = "R-158/R-159 typo française"
    # Extract visible text (strip tags + style/script)
    text = re.sub(r'<(script|style)\b.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    findings = []
    # Straight apostrophe in middle of word (l'on, c'est)
    if re.search(r"\b\w+'\w+\b", text):
        findings.append("apostrophe droite (') dans des mots — utiliser ’")
    # Straight double quotes around words
    if re.search(r'"\w[^"]*\w"', text):
        findings.append("guillemets droits (\") — utiliser « … »")
    # ... instead of …
    if re.search(r'\.\.\.', text):
        findings.append("\"...\" — utiliser …")
    # Space before : ! ? ; without nbsp (rough heuristic — looks for raw space)
    # Note: HTML entities like &nbsp; or &#160; are already substituted out by tag-strip,
    # so we rely on the source `html` for entity check
    if re.search(r'[a-zàéèêôûîç]\s[!?:;»](?!\w)', text):
        findings.append("espace simple avant : ! ? ; » — utiliser &nbsp; ou &#8239;")
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} problème(s) typo",
                          findings[:5])
    return CheckResult("PASS", label, "typo française correcte", [])


# ---- Bloc Misc -----------------------------------------------------------

def check_R019_opentype_features(css: str) -> CheckResult:
    """R-019 | OpenType features (info)."""
    label = "R-019 OpenType features"
    has_features = bool(re.search(
        r'font-variant-(numeric|caps|ligatures|alternates|east-asian)\s*:|font-feature-settings\s*:',
        css
    ))
    if has_features:
        return CheckResult("PASS", label, "OpenType features utilisées", [])
    return CheckResult("WARN", label, "aucune OpenType feature",
                      ["Activer font-variant-* pour fignoler la typographie"])


def check_R033_durations_standard(css: str) -> CheckResult:
    """R-033 | Durations standard (alerter >800ms ou <50ms)."""
    label = "R-033 durations"
    findings = []
    for m in re.finditer(r'(transition-duration|animation-duration|transition\s*:|animation\s*:)\s*([^;{}]+)', css):
        value = m.group(2)
        for dur_m in re.finditer(r'(\d+(?:\.\d+)?)\s*(ms|s)\b', value):
            num = float(dur_m.group(1))
            unit = dur_m.group(2)
            ms = num * 1000 if unit == 's' else num
            if ms > 800 or (ms < 50 and ms > 0):
                ln = line_number_at(css, m.start())
                findings.append(f"Ligne {ln}: {dur_m.group(0)} (hors plage 50-800ms)")
                break
    if findings:
        return CheckResult("WARN", label, f"{len(findings)} duration(s) hors plage",
                          findings[:5] + ["Plage recommandée : 150-400ms (UI), max 800ms"])
    return CheckResult("PASS", label, "durations dans la plage", [])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

VAGUE2_CHECKS = [
    # Couleur
    ('R005', lambda css, html, ca: check_R005_no_pure_black_white(css, html)),
    ('R009', lambda css, html, ca: check_R009_alpha_excess(css)),
    ('R001', lambda css, html, ca: check_R001_oklch_preferred(css)),
    ('R147', lambda css, html, ca: check_R147_color_scheme_dark(css)),
    ('R148', lambda css, html, ca: check_R148_meta_theme_color(html)),
    # Typo
    ('R013', lambda css, html, ca: check_R013_banned_fonts(html, css)),
    ('R017', lambda css, html, ca: check_R017_font_display_swap(css, html)),
    ('R104', lambda css, html, ca: check_R104_text_wrap(css)),
    ('R105', lambda css, html, ca: check_R105_tabular_nums(html, css)),
    # Animations
    ('R035', lambda css, html, ca: check_R035_bounce_elastic(css)),
    ('R036', lambda css, html, ca: check_R036_animate_transform_opacity_only(css)),
    ('R132', lambda css, html, ca: check_R132_no_transition_all(css)),
    ('R042', lambda css, html, ca: check_R042_will_change_excess(css)),
    # Layout
    ('R024', lambda css, html, ca: check_R024_spacing_tokens_semantic(css)),
    ('R025', lambda css, html, ca: check_R025_grid_minmax_responsive(css)),
    ('R028', lambda css, html, ca: check_R028_container_queries(css)),
    ('R031', lambda css, html, ca: check_R031_no_arbitrary_zindex(css)),
    ('R057', lambda css, html, ca: check_R057_breakpoints_count(css)),
    ('R058', lambda css, html, ca: check_R058_input_method_query(css)),
    ('R059', lambda css, html, ca: check_R059_safe_area_inset(html, css)),
    ('R138', lambda css, html, ca: check_R138_overscroll_behavior(html, css)),
    # A11y
    ('R045', lambda css, html, ca: check_R045_inputs_labelled(html)),
    ('R048', lambda css, html, ca: check_R048_native_dialog(html)),
    ('R049', lambda css, html, ca: check_R049_popover_api(html)),
    ('R051', lambda css, html, ca: check_R051_anchor_positioning(css)),
    ('R053', lambda css, html, ca: check_R053_roving_tabindex(html)),
    ('R054', lambda css, html, ca: check_R054_skip_link(html)),
    ('R067', lambda css, html, ca: check_R067_R142_icon_buttons_aria_label(html)),
    ('R068', lambda css, html, ca: check_R068_alt_text(html)),
    ('R166', lambda css, html, ca: check_R166_headings_hierarchy(html)),
    ('R169', lambda css, html, ca: check_R169_aria_live(html)),
    ('R172', lambda css, html, ca: check_R172_interactive_states(css)),
    # Performance
    ('R060', lambda css, html, ca: check_R060_srcset_sizes(html)),
    ('R130', lambda css, html, ca: check_R130_picture_art_direction(html)),
    ('R131', lambda css, html, ca: check_R131_image_dimensions_lazy(html)),
    ('R133', lambda css, html, ca: check_R133_large_lists_virtualize(html, css)),
    # Compositions
    ('R081', lambda css, html, ca: check_R081_side_stripe_borders(css)),
    # R-082, R-108, R-109, R-114 — hébergés dans phase4-blacklist-gate.py (interdictions binaires)
    # Copy
    ('R076', lambda css, html, ca: check_R076_R117_ai_cliches(html)),
    ('R115', lambda css, html, ca: check_R115_generic_names(html)),
    ('R116', lambda css, html, ca: check_R116_fake_round_numbers(html)),
    ('R118', lambda css, html, ca: check_R118_broken_image_links(html)),
    ('R158', lambda css, html, ca: check_R158_R159_typography(html)),
    # Misc
    ('R019', lambda css, html, ca: check_R019_opentype_features(css)),
    ('R033', lambda css, html, ca: check_R033_durations_standard(css)),
]


# ---------------------------------------------------------------------------
# Vague 1 check identifiers — clé stable pour le JSON output (P4)
# Ordre = ordre d'exécution des checks dans main(). Sert au mapping
# results[i] → vague1.checks[VAGUE1_CHECK_KEYS[i]] sans toucher l'output stdout.
# ---------------------------------------------------------------------------

VAGUE1_CHECK_KEYS = [
    "hover_multi_property",
    "clip_or_mask",
    "no_generic_ease",
    "box_shadow_layers",
    "padding_block_varied",
    "keyframes_referenced",
    "root_vars_unused",
    "advanced_techniques",
]


def main():
    parser = argparse.ArgumentParser(
        prog="phase4-finishing-gate",
        description=(
            "Phase 4 Finishing Gate — vérifie 8 checks Vague 1 (bloquants) + "
            "checks Vague 2 anti-slop (informationnels) sur un style-tile HTML."
        ),
    )
    parser.add_argument("html_path", help="Chemin vers le style-tile HTML à auditer")
    parser.add_argument(
        "cursor_a",
        type=int,
        help="Cursor A (1-5) issu du scoping — détermine le quota de techniques avancées",
    )
    parser.add_argument(
        "--json-output",
        default=None,
        metavar="PATH",
        help=(
            "Si fourni, écrit un JSON structuré complet (Vague 1 + Vague 2) "
            "à ce chemin EN PLUS du stdout actuel (compat ascendante préservée)."
        ),
    )
    args = parser.parse_args()

    filepath = args.html_path
    cursor_a = args.cursor_a
    json_output_path = args.json_output

    # Read file
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        print(f"Erreur: fichier introuvable — {filepath}")
        sys.exit(2)

    # Extract and clean CSS
    raw_css = extract_css(html)
    if not raw_css.strip():
        print(f"Erreur: aucun CSS trouvé dans {filepath}")
        sys.exit(2)

    css = strip_css_comments(raw_css)

    # Run all 8 Vague 1 checks
    results = [
        check_hover_multi_property(css),
        check_clip_or_mask(css, cursor_a),
        check_no_generic_ease(css),
        check_box_shadow_layers(css),
        check_padding_block_varied(css),
        check_keyframes_referenced(css),
        check_root_variables_used(css),
        check_advanced_techniques(css, cursor_a),
    ]

    # Run Vague 2 checks (WARN by default)
    # On garde la rule_id alignée avec chaque résultat pour le JSON output.
    vague2_results: list[tuple[str, CheckResult]] = []
    for rule_id, check_fn in VAGUE2_CHECKS:
        try:
            vague2_results.append((rule_id, check_fn(css, html, cursor_a)))
        except Exception as e:
            vague2_results.append((
                rule_id,
                CheckResult(
                    "WARN", f"{rule_id} (erreur)",
                    f"check a échoué: {type(e).__name__}", [str(e)[:120]]
                ),
            ))

    # Output
    filename = filepath.rsplit('/', 1)[-1] if '/' in filepath else filepath
    print(f"\n=== PHASE 4 FINISHING GATE ===")
    print(f"File: {filename}")
    print(f"Cursor A: {cursor_a}")
    print()

    fail_count = 0
    warn_count = 0

    for r in results:
        tag = f"[{r.status}]"
        print(f"{tag} {r.label}: {r.summary}")
        if r.status == "FAIL":
            fail_count += 1
        elif r.status == "WARN":
            warn_count += 1
        for detail in r.details:
            print(f"  → {detail}")

    # Vague 2 anti-slop section (informationnel, ne bloque pas)
    print()
    print("--- VAGUE 2 ANTI-SLOP (WARN seulement, informationnel) ---")
    v2_warn = 0
    v2_pass = 0
    for rule_id, r in vague2_results:
        tag = f"[{r.status}]"
        if r.status == "PASS":
            v2_pass += 1
            # Skip PASS in output to keep noise low
            continue
        if r.status == "WARN":
            v2_warn += 1
        print(f"{tag} {r.label}: {r.summary}")
        for detail in r.details[:3]:
            print(f"  → {detail}")
    print(f"Vague 2: {v2_pass} PASS / {v2_warn} WARN sur {len(vague2_results)} checks")

    print()
    parts = []
    if fail_count:
        parts.append(f"{fail_count} FAIL")
    if warn_count:
        parts.append(f"{warn_count} WARN")
    vague1_verdict = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")
    if not parts:
        print("VERDICT: ALL PASS")
        verdict_summary = "ALL PASS"
    else:
        verdict = ', '.join(parts)
        suffix = " — corrections requises" if fail_count else ""
        print(f"VERDICT: {verdict}{suffix}")
        verdict_summary = f"{verdict}{suffix}"

    # ----------------------------------------------------------------------
    # P4 — JSON output structuré (optionnel, compat ascendante)
    # ----------------------------------------------------------------------
    if json_output_path:
        try:
            html_sha256 = hashlib.sha256(html.encode('utf-8')).hexdigest()
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )

            # Vague 1 — checks alignés avec VAGUE1_CHECK_KEYS
            vague1_checks: dict = {}
            for key, r in zip(VAGUE1_CHECK_KEYS, results):
                vague1_checks[key] = {
                    "status": r.status,
                    "label": r.label,
                    "message": r.summary,
                    "details": list(r.details),
                }

            # Vague 2 — sortir UNIQUEMENT les warnings (les PASS ne servent pas
            # aux Critiques sémantiques en aval ; on garde un compte pour audit).
            vague2_warnings = []
            v2_warn_count = 0
            v2_pass_count = 0
            for rule_id, r in vague2_results:
                if r.status == "PASS":
                    v2_pass_count += 1
                    continue
                v2_warn_count += 1
                vague2_warnings.append({
                    "rule_id": rule_id,
                    "label": r.label,
                    "status": r.status,
                    "message": r.summary,
                    "details": list(r.details),
                })

            verdict_global = vague1_verdict if vague1_verdict == "FAIL" else (
                "WARN" if (vague1_verdict == "WARN" or v2_warn_count > 0) else "PASS"
            )

            gate_results = {
                "gate": "phase4-finishing-gate",
                "html_audited": filepath,
                "html_sha256": html_sha256,
                "cursor_a": cursor_a,
                "timestamp": timestamp,
                "vague1": {
                    "verdict": vague1_verdict,
                    "checks": vague1_checks,
                    "warn_count": warn_count,
                    "fail_count": fail_count,
                },
                "vague2": {
                    "warnings": vague2_warnings,
                    "total_warnings": v2_warn_count,
                    "checks_pass_count": v2_pass_count,
                    "checks_total": len(vague2_results),
                },
                "verdict_global": verdict_global,
                "summary": (
                    f"Vague 1: {verdict_summary} | "
                    f"Vague 2: {v2_warn_count} WARN sur {len(vague2_results)} checks"
                ),
            }

            with open(json_output_path, 'w', encoding='utf-8') as fh:
                json.dump(gate_results, fh, ensure_ascii=False, indent=2)
        except Exception as e:
            # Ne jamais faire planter le gate à cause du JSON — log stderr et continuer.
            print(
                f"[finishing-gate] WARN: échec écriture JSON {json_output_path} : "
                f"{type(e).__name__}: {e}",
                file=sys.stderr,
            )

    sys.exit(1 if fail_count > 0 else 0)


if __name__ == '__main__':
    main()
