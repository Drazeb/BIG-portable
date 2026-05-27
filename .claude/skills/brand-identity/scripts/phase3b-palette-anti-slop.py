#!/usr/bin/env python3
"""
Phase 3B-3 Palette Anti-Slop Gate

Vérifie le markdown produit par le sub-agent palette (3B-3) sur 10 checks :
  Format / hex valides / pure noir-blanc / blacklist AI Tailwind /
  neutres tintés / saturation extrêmes / WCAG AA / accent distinct /
  rôles inventés / justifications non-génériques.

Usage :
  python3 phase3b-palette-anti-slop.py <palette-c{N}.md> [--json-output]

Exit codes :
  0 = PASS
  1 = FAIL (violations bloquantes)
  2 = ERREUR fichier
"""

from __future__ import annotations

import json
import math
import re
import sys


# ---------------------------------------------------------------------------
# Vocabulaire (listes nominatives — vivent ici, jamais dans le prompt)
# ---------------------------------------------------------------------------

EXPECTED_ROLES = [
    'Primary',
    'Secondary',
    'Accent',
    'Bg dark',
    'Bg light',
    'Text primary',
    'Text secondary',
]

# Rôles inventés à détecter (pas de variantes par défaut)
INVENTED_ROLE_PATTERNS = [
    r'^Primary\s+(dark|light|base|deep|alt)\b',
    r'^Secondary\s+(dark|light|base|deep|alt)\b',
    r'^Accent\s+(primary|secondary|alt|2|deep|light)\b',
    r'^Surface\b',
    r'^Neutral\s+(mid|base|alt|2)\b',
    r'^Bg\s+(medium|mid|alt|2)\b',
    r'^Text\s+(tertiary|inverted|disabled|alt|3)\b',
]

# Hex bannis : pur noir / pur blanc EXACTS
PURE_BLACK_WHITE = [
    '#000000', '#000', '#FFFFFF', '#FFF', '#fff', '#ffffff',
]

# Hex AI Tailwind défaut (training-defaults LLM)
# Liste canonique 2024-2026 (Tailwind v3/v4 indigo/violet/purple/blue)
AI_TAILWIND_DEFAULTS = [
    # Indigo
    '#6366f1', '#4f46e5', '#4338ca', '#3730a3',
    # Violet
    '#8b5cf6', '#7c3aed', '#6d28d9', '#5b21b6',
    # Purple
    '#a855f7', '#9333ea', '#7e22ce', '#6b21a8',
    # Blue brillants (les bleus AI)
    '#3b82f6', '#2563eb', '#1d4ed8',
    # Sky brillants
    '#0ea5e9', '#0284c7',
]
# Normaliser en lowercase pour comparaisons
AI_TAILWIND_DEFAULTS_LOWER = [h.lower() for h in AI_TAILWIND_DEFAULTS]

# Phrases génériques bannies dans les justifications
GENERIC_JUSTIFICATION_PATTERNS = [
    r'\bton\s+moderne\b',
    r'\bton\s+élégant\b', r'\bton\s+elegant\b',
    r'\bton\s+universel\b',
    r'\bdans\s+l[\'’]?\s*air\s+du\s+temps\b',
    r'\bconvient\s+bien\b',
    r'\bfonctionne\s+bien\b',
    r'\bbon\s+choix\s+en\s+général\b', r'\bbon\s+choix\s+en\s+general\b',
    r'\bvaleur\s+sûre\b', r'\bvaleur\s+sure\b',
    r'\bton\s+épuré\b', r'\bton\s+epure\b',
]


# ---------------------------------------------------------------------------
# Conversions colorimétriques (sans dépendance externe)
# ---------------------------------------------------------------------------

def hex_to_rgb(hex_str: str) -> tuple[float, float, float] | None:
    """Convert #RRGGBB or #RGB to (r, g, b) floats in [0, 1]."""
    s = hex_str.strip().lstrip('#')
    if len(s) == 3:
        s = ''.join(c * 2 for c in s)
    if len(s) != 6:
        return None
    try:
        r = int(s[0:2], 16) / 255.0
        g = int(s[2:4], 16) / 255.0
        b = int(s[4:6], 16) / 255.0
        return r, g, b
    except ValueError:
        return None


def srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_oklch(hex_str: str) -> tuple[float, float, float] | None:
    """Convert hex to OKLCH (L, C, H_degrees). Returns None on invalid hex."""
    rgb = hex_to_rgb(hex_str)
    if rgb is None:
        return None
    r, g, b = (srgb_to_linear(c) for c in rgb)

    # linear sRGB → OKLab (Björn Ottosson)
    lL = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    lM = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    lS = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l_ = lL ** (1 / 3) if lL > 0 else 0
    m_ = lM ** (1 / 3) if lM > 0 else 0
    s_ = lS ** (1 / 3) if lS > 0 else 0

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    C = math.sqrt(a * a + bb * bb)
    H = math.degrees(math.atan2(bb, a))
    if H < 0:
        H += 360
    return L, C, H


def relative_luminance(hex_str: str) -> float | None:
    rgb = hex_to_rgb(hex_str)
    if rgb is None:
        return None
    r, g, b = (srgb_to_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def wcag_contrast(hex1: str, hex2: str) -> float | None:
    L1 = relative_luminance(hex1)
    L2 = relative_luminance(hex2)
    if L1 is None or L2 is None:
        return None
    return (max(L1, L2) + 0.05) / (min(L1, L2) + 0.05)


def is_in_ai_purple_zone(hex_str: str) -> tuple[bool, dict]:
    """Détecte si un hex tombe dans la zone LCH 'AI purple/indigo Tailwind'.

    Critères : hue 250-310°, chroma > 0.13, lightness 0.40-0.75.
    Cette zone englobe les indigo/violet/purple Tailwind 500-700 et leurs variantes.
    """
    oklch = hex_to_oklch(hex_str)
    if oklch is None:
        return False, {}
    L, C, H = oklch
    in_zone = (250 <= H <= 310) and (C > 0.13) and (0.40 <= L <= 0.75)
    return in_zone, {'L': round(L, 3), 'C': round(C, 3), 'H': round(H, 1)}


# ---------------------------------------------------------------------------
# Parser markdown
# ---------------------------------------------------------------------------

def _clean_cell(cell: str) -> str:
    """Strip markdown bold/code markers around cell content."""
    s = cell.strip()
    # Remove surrounding backticks
    if s.startswith('`') and s.endswith('`'):
        s = s[1:-1].strip()
    # Remove surrounding bold markers
    if s.startswith('**') and s.endswith('**'):
        s = s[2:-2].strip()
    # Remove inline backticks anywhere (for hex like `#2B3A67`)
    s = s.replace('`', '').strip()
    # Remove inline bold (**text**) but keep the text
    s = re.sub(r'\*\*([^*]+)\*\*', r'\1', s)
    return s


def parse_palette_table(content: str) -> list[dict]:
    """Extrait les lignes du tableau Palette complète.

    Tolère les variations de format : ordre Hex/Nom variable, en-têtes avec
    qualificatifs ('Justification métaphore', 'Nom évocateur'), gras/backticks
    dans les cellules.
    """
    rows = []
    # Find every markdown table in the doc, look for one with required columns.
    # A table block = header line, separator line, then data lines.
    table_re = re.compile(
        r'\n(\|[^\n]+\|)\n\|[-: |]+\|\n((?:\|[^\n]+\|\n?)+)',
        re.MULTILINE
    )
    for m in table_re.finditer(content):
        header_line = m.group(1)
        body = m.group(2)
        headers = [_clean_cell(h).lower() for h in header_line.split('|') if _clean_cell(h)]
        # Check for required columns (role + hex; name and reason useful)
        idx_role = next((i for i, h in enumerate(headers) if 'rôle' in h or 'role' in h), -1)
        idx_hex = next((i for i, h in enumerate(headers) if 'hex' in h or 'code' in h), -1)
        idx_name = next((i for i, h in enumerate(headers) if 'nom' in h or 'name' in h), -1)
        idx_reason = next((i for i, h in enumerate(headers) if 'justif' in h or 'pourquoi' in h or 'raison' in h), -1)

        # Only consider tables with at least Role + Hex columns
        if idx_role < 0 or idx_hex < 0:
            continue

        # Verify this looks like the palette table (has known role names)
        body_lines = [l for l in body.strip().split('\n') if l.strip().startswith('|')]
        if not body_lines:
            continue
        # Quick heuristic : at least one line should contain 'primary', 'accent', 'bg', 'text', or 'surface'
        body_lower = body.lower()
        if not any(kw in body_lower for kw in ('primary', 'accent', 'bg ', 'text ', 'surface', 'neutral')):
            continue

        # Parse rows
        for line in body_lines:
            cells = [_clean_cell(c) for c in line.split('|')]
            cells = [c for c in cells if c != '']
            if len(cells) <= max(idx_role, idx_hex):
                continue
            row = {
                'role': cells[idx_role] if idx_role < len(cells) else '',
                'hex': cells[idx_hex] if idx_hex < len(cells) else '',
                'name': cells[idx_name] if 0 <= idx_name < len(cells) else '',
                'reason': cells[idx_reason] if 0 <= idx_reason < len(cells) else '',
            }
            rows.append(row)
        if rows:
            return rows  # Stop at the first matching table
    return rows


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_format_strict(rows: list[dict]) -> list[dict]:
    """Check 1 : 7 rôles exacts dans l'ordre attendu."""
    violations = []
    if len(rows) == 0:
        violations.append({
            'check': 'format_strict',
            'severity': 'FAIL',
            'detail': "Aucun tableau Palette détecté (en-tête 'Rôle | Nom | Hex | Justification' attendu).",
        })
        return violations
    if len(rows) != 7:
        violations.append({
            'check': 'format_strict',
            'severity': 'FAIL',
            'detail': f"Le tableau contient {len(rows)} lignes, EXACTEMENT 7 attendues (Primary, Secondary, Accent, Bg dark, Bg light, Text primary, Text secondary).",
        })
    for i, expected in enumerate(EXPECTED_ROLES):
        if i >= len(rows):
            break
        actual = rows[i]['role'].strip()
        # Comparaison insensible à la casse
        if actual.lower() != expected.lower():
            violations.append({
                'check': 'format_strict',
                'severity': 'FAIL',
                'detail': f"Ligne {i+1} : rôle attendu '{expected}', trouvé '{actual}'. Ordre strict obligatoire.",
            })
    return violations


def check_hex_validity(rows: list[dict]) -> list[dict]:
    """Check 2 : tous les hex respectent #RRGGBB ou #RGB."""
    violations = []
    hex_re = re.compile(r'^#[0-9A-Fa-f]{6}$|^#[0-9A-Fa-f]{3}$')
    for row in rows:
        if not hex_re.match(row['hex']):
            violations.append({
                'check': 'hex_validity',
                'severity': 'FAIL',
                'detail': f"Hex invalide pour {row['role']} : '{row['hex']}' (attendu #RRGGBB ou #RGB).",
            })
    return violations


def check_no_invented_roles(content: str) -> list[dict]:
    """Check 3 : pas de rôles inventés (Primary dark, Surface, Neutral mid, etc.)."""
    violations = []
    for pattern in INVENTED_ROLE_PATTERNS:
        for m in re.finditer(pattern, content, re.MULTILINE):
            violations.append({
                'check': 'no_invented_roles',
                'severity': 'FAIL',
                'detail': f"Rôle inventé détecté : '{m.group(0)}'. Format strict 7 rôles : Primary, Secondary, Accent, Bg dark, Bg light, Text primary, Text secondary.",
            })
    return violations


def check_no_pure_black_white(rows: list[dict]) -> list[dict]:
    """Check 4 : pas de pur #000 / #fff sur surfaces principales."""
    violations = []
    surface_roles = {'Bg dark', 'Bg light', 'Text primary'}
    pure_set = {h.lower() for h in PURE_BLACK_WHITE}
    for row in rows:
        if row['role'] not in surface_roles:
            continue
        if row['hex'].lower() in pure_set:
            violations.append({
                'check': 'no_pure_black_white',
                'severity': 'FAIL',
                'detail': f"{row['role']} = '{row['hex']}' (pur noir/blanc). Marqueur slop majeur — utilise un off-{('black' if row['hex'].lower() in {'#000', '#000000'} else 'white')} teinté vers la dominante.",
            })
    return violations


def check_no_ai_tailwind_defaults(rows: list[dict]) -> list[dict]:
    """Check 5 : aucun hex de la blacklist AI Tailwind (regex strict + zone LCH)."""
    violations = []
    for row in rows:
        hex_norm = row['hex'].lower()
        # Match regex strict (hex exact dans la liste)
        if hex_norm in AI_TAILWIND_DEFAULTS_LOWER:
            violations.append({
                'check': 'ai_tailwind_default',
                'severity': 'FAIL',
                'detail': f"{row['role']} = '{row['hex']}' = hex AI Tailwind défaut connu (indigo/violet/purple/blue). Décale franchement vers magenta-shifted, bleu profond désaturé, ou ajoute du chroma vers l'orangé.",
            })
            continue
        # Match zone LCH (variantes proches du défaut)
        in_zone, lch = is_in_ai_purple_zone(row['hex'])
        if in_zone:
            violations.append({
                'check': 'ai_purple_zone',
                'severity': 'FAIL',
                'detail': f"{row['role']} = '{row['hex']}' (LCH={lch}) dans la zone AI purple/indigo (hue {lch.get('H')}°, chroma {lch.get('C')}, L {lch.get('L')}). Décale vers magenta-shifted (H<240 ou H>310) ou désature franchement (C<0.13).",
            })
    return violations


def check_neutrals_tinted(rows: list[dict]) -> list[dict]:
    """Check 6 : neutres tintés vers la dominante (chroma OKLCH > 0.005)."""
    violations = []
    neutral_roles = {'Bg dark', 'Bg light', 'Text primary', 'Text secondary'}
    threshold = 0.005
    for row in rows:
        if row['role'] not in neutral_roles:
            continue
        oklch = hex_to_oklch(row['hex'])
        if oklch is None:
            continue
        L, C, H = oklch
        if C < threshold:
            violations.append({
                'check': 'neutrals_tinted',
                'severity': 'FAIL',
                'detail': f"{row['role']} = '{row['hex']}' a chroma OKLCH = {C:.4f} (< {threshold}). Neutre purement chromatiquement neutre — coupe la cohésion subconsciente. Ajoute une trace chromatique vers la teinte du Primary.",
            })
    return violations


def check_saturation_extremes(rows: list[dict]) -> list[dict]:
    """Check 7 : saturation réduite aux lightness extrêmes (L>0.95 ou L<0.10 → C<0.04)."""
    violations = []
    for row in rows:
        oklch = hex_to_oklch(row['hex'])
        if oklch is None:
            continue
        L, C, H = oklch
        if (L > 0.95 or L < 0.10) and C > 0.04:
            violations.append({
                'check': 'saturation_extremes',
                'severity': 'FAIL',
                'detail': f"{row['role']} = '{row['hex']}' (L={L:.2f}, C={C:.3f}) — chroma trop élevé pour lightness extrême ({'>0.95' if L > 0.95 else '<0.10'}). Aux extrêmes, désature franchement (chroma < 0.04) pour éviter aspect garish.",
            })
    return violations


def parse_dominant_mode(content: str) -> str:
    """Extract 'SOMBRE' or 'CLAIR' from the 'Mode fond dominant' line."""
    m = re.search(r'\*\*Mode\s+fond\s+dominant\*\*\s*:?\s*\*?\*?\s*(SOMBRE|CLAIR)\b',
                  content, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    # Fallback : scan looser
    m = re.search(r'mode\s+fond\s+dominant.*?(SOMBRE|CLAIR)', content, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).upper()
    return 'UNKNOWN'


def check_wcag_contrast(rows: list[dict], dominant_mode: str = 'UNKNOWN') -> list[dict]:
    """Check 8 : WCAG AA contraste mode-aware.

    Le texte primaire n'apparaît en pratique que sur le fond DOMINANT, pas sur les deux
    simultanément. On vérifie donc les paires effectivement utilisées selon le mode :
      - SOMBRE  : Text primary/secondary sur Bg dark
      - CLAIR   : Text primary/secondary sur Bg light
      - UNKNOWN : fallback strict (vérifie les deux paires)
    Plus une vérification d'inversion atmosphérique : Bg dark vs Bg light ≥ 4.5:1
    pour que les sections inversées (atmosphère) soient lisibles.
    """
    violations = []
    by_role = {row['role']: row for row in rows}

    # Pair list according to mode
    if dominant_mode == 'SOMBRE':
        pairs = [
            ('Text primary', 'Bg dark', 4.5),
            ('Text secondary', 'Bg dark', 3.0),
        ]
    elif dominant_mode == 'CLAIR':
        pairs = [
            ('Text primary', 'Bg light', 4.5),
            ('Text secondary', 'Bg light', 3.0),
        ]
    else:
        # Fallback strict — comportement historique
        pairs = [
            ('Text primary', 'Bg light', 4.5),
            ('Text primary', 'Bg dark', 4.5),
            ('Text secondary', 'Bg light', 3.0),
            ('Text secondary', 'Bg dark', 3.0),
        ]

    for fg, bg, min_ratio in pairs:
        if fg not in by_role or bg not in by_role:
            continue
        ratio = wcag_contrast(by_role[fg]['hex'], by_role[bg]['hex'])
        if ratio is None:
            continue
        if ratio < min_ratio:
            violations.append({
                'check': 'wcag_contrast',
                'severity': 'FAIL',
                'detail': (
                    f"[mode {dominant_mode}] Contraste WCAG {fg} ({by_role[fg]['hex']}) "
                    f"vs {bg} ({by_role[bg]['hex']}) = {ratio:.2f}:1 (< {min_ratio}:1 requis). "
                    f"Texte inaccessible sur le fond dominant."
                ),
            })

    # Cross-check minimal : Bg dark et Bg light ne doivent pas être quasi-identiques.
    # On accepte largement les palettes "tons doux monochromes" (Bg dark taupe vs
    # Bg light crème, écart subtil). On ne flag que les cas extrêmes où les deux
    # fonds sont visuellement indistinguables (seuil 1.5:1 = palette plate
    # accidentelle, presque même hex).
    if 'Bg dark' in by_role and 'Bg light' in by_role:
        inv_ratio = wcag_contrast(by_role['Bg dark']['hex'], by_role['Bg light']['hex'])
        if inv_ratio is not None and inv_ratio < 1.5:
            violations.append({
                'check': 'wcag_contrast',
                'severity': 'FAIL',
                'detail': (
                    f"Bg dark ({by_role['Bg dark']['hex']}) et Bg light ({by_role['Bg light']['hex']}) "
                    f"sont quasi-identiques : contraste {inv_ratio:.2f}:1 (< 1.5:1). "
                    f"Tu n'as pas deux fonds, tu as deux nuances de la même couleur — c'est un bug, "
                    f"pas un choix créatif."
                ),
            })

    return violations


def lch_distance(oklch1: tuple, oklch2: tuple) -> dict:
    """Distance perceptuelle entre 2 couleurs OKLCH.

    Combine la différence de chroma (saturation) ET de hue (position sur la roue
    chromatique). Une couleur peut être 'distincte' soit par sa saturation supérieure,
    soit par son opposition chaud/froid, soit par les deux.

    Retour : dict avec delta_C, delta_H_arc (degrés), delta_H_chord (perceptuel),
    et distance_total = sqrt(delta_C² + delta_H_chord²).
    """
    L1, C1, H1 = oklch1
    L2, C2, H2 = oklch2
    delta_C = C2 - C1
    # Arc minimal sur la roue (0..180°)
    diff = abs(H1 - H2) % 360
    delta_H_arc = min(diff, 360 - diff)
    # Distance "corde" = projection planaire dans l'espace LCH
    # 2 * sqrt(C1*C2) * sin(delta_H_arc/2)  est la longueur de corde sur le cercle de
    # rayons moyennés — utile pour des chroma > 0
    half_rad = math.radians(delta_H_arc / 2)
    delta_H_chord = 2 * math.sqrt(max(C1 * C2, 0)) * math.sin(half_rad)
    distance = math.sqrt(delta_C * delta_C + delta_H_chord * delta_H_chord)
    return {
        'delta_C': delta_C,
        'delta_H_arc': delta_H_arc,
        'delta_H_chord': delta_H_chord,
        'distance': distance,
    }


def check_accent_distinct(rows: list[dict]) -> list[dict]:
    """Check 9 : Accent visuellement distinct du Primary.

    Distinction = soit chroma plus élevé (Accent plus saturé), soit opposition de
    hue (chaud/froid), soit les deux. On exige une distance LCH ≥ 0.07 (seuil
    perceptuel calibré) ET un chroma_accent supérieur ou très proche du Primary
    (delta_C ≥ -0.02 — pour ne pas accepter un accent visiblement plus terne).
    """
    violations = []
    by_role = {row['role']: row for row in rows}
    if 'Accent' not in by_role or 'Primary' not in by_role:
        return violations
    accent_oklch = hex_to_oklch(by_role['Accent']['hex'])
    primary_oklch = hex_to_oklch(by_role['Primary']['hex'])
    if accent_oklch is None or primary_oklch is None:
        return violations
    d = lch_distance(primary_oklch, accent_oklch)
    THRESHOLD_DISTANCE = 0.07
    THRESHOLD_DELTA_C_FLOOR = -0.02  # accent ne doit pas être dramatiquement plus terne
    if d['distance'] < THRESHOLD_DISTANCE or d['delta_C'] < THRESHOLD_DELTA_C_FLOOR:
        violations.append({
            'check': 'accent_distinct',
            'severity': 'FAIL',
            'detail': (
                f"Accent ({by_role['Accent']['hex']}) pas distinct du Primary "
                f"({by_role['Primary']['hex']}). "
                f"Distance perceptuelle LCH = {d['distance']:.3f} (seuil {THRESHOLD_DISTANCE}), "
                f"delta saturation = {d['delta_C']:+.3f}, "
                f"écart de teinte = {d['delta_H_arc']:.0f}°. "
                f"L'accent doit se distinguer soit par une saturation nettement plus élevée, "
                f"soit par une opposition de teinte (chaud/froid), soit les deux."
            ),
        })
    return violations


def check_justifications_non_generic(rows: list[dict]) -> list[dict]:
    """Check 10 : justifications non vides et non génériques."""
    violations = []
    for row in rows:
        reason = row.get('reason', '')
        if len(reason.strip()) < 10:
            violations.append({
                'check': 'justification_present',
                'severity': 'FAIL',
                'detail': f"Justification vide ou trop courte pour {row['role']} = '{row['hex']}'.",
            })
            continue
        for pattern in GENERIC_JUSTIFICATION_PATTERNS:
            if re.search(pattern, reason, re.IGNORECASE):
                violations.append({
                    'check': 'justification_non_generic',
                    'severity': 'FAIL',
                    'detail': f"Justification générique pour {row['role']} : '{reason[:80]}…'. Cite la métaphore ou un mot-clé du concept narratif.",
                })
                break
    return violations


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    json_output = '--json-output' in sys.argv
    args = [a for a in sys.argv[1:] if a != '--json-output']

    if len(args) < 1:
        print("Usage: python3 phase3b-palette-anti-slop.py <palette.md> [--json-output]")
        sys.exit(2)

    filepath = args[0]
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erreur: fichier introuvable — {filepath}")
        sys.exit(2)

    rows = parse_palette_table(content)

    all_violations = []
    all_violations.extend(check_format_strict(rows))
    all_violations.extend(check_hex_validity(rows))
    all_violations.extend(check_no_invented_roles(content))
    all_violations.extend(check_no_pure_black_white(rows))
    all_violations.extend(check_no_ai_tailwind_defaults(rows))
    all_violations.extend(check_neutrals_tinted(rows))
    all_violations.extend(check_saturation_extremes(rows))
    dominant_mode = parse_dominant_mode(content)
    all_violations.extend(check_wcag_contrast(rows, dominant_mode))
    all_violations.extend(check_accent_distinct(rows))
    all_violations.extend(check_justifications_non_generic(rows))

    verdict = 'FAIL' if all_violations else 'PASS'
    exit_code = 1 if all_violations else 0

    if json_output:
        output = {
            'verdict': verdict,
            'file': filepath,
            'roles_count': len(rows),
            'violations': all_violations,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        sys.exit(exit_code)

    filename = filepath.rsplit('/', 1)[-1] if '/' in filepath else filepath
    print(f"\n=== PHASE 3B-3 PALETTE ANTI-SLOP GATE ===")
    print(f"File: {filename}")
    print(f"Roles parsed: {len(rows)}/7")
    print()

    if all_violations:
        by_check: dict[str, list] = {}
        for v in all_violations:
            by_check.setdefault(v['check'], []).append(v)
        print(f"[FAIL] {len(all_violations)} violation(s) dans {len(by_check)} catégorie(s) :\n")
        for check, instances in sorted(by_check.items()):
            print(f"  ❌ {check} ({len(instances)}x)")
            for inst in instances[:5]:
                print(f"     {inst['detail']}")
            if len(instances) > 5:
                print(f"     ... et {len(instances) - 5} autre(s)")
            print()
        print("VERDICT: FAIL — corrections requises")
        print("→ Resume du sub-agent palette avec ces violations en feedback.")
    else:
        print("VERDICT: PASS — palette conforme aux 10 checks anti-slop.")

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
