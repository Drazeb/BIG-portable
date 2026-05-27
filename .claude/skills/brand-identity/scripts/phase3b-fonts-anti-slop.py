#!/usr/bin/env python3
"""
Phase 3B-1 Fonts Anti-Slop Gate

Vérifie les longlists produites par les penseurs typographiques (display + body)
sur 7 checks anti-slop :
  1. Format strict longlist (12-15 display / 10 body, rang ordonné)
  2. Aucune fonte hard-banned (filet de sécurité après pool curé)
  3. Justifications spécifiques (pas génériques "moderne", "convient", "tasteful")
  4. Top 3 sans SLOP_RISK_EMERGING non justifié
  5. Pairing structural contrast (display rang 1 × body rang 1, ≥1 axe différent)
  6. Pairing pas dans closed-ban list (Playfair+Lato, Cormorant+Montserrat, etc.)
  7. Dashboard/SaaS UI = serif banni

Usage :
  python3 phase3b-fonts-anti-slop.py \\
      --display path/to/{brand}-penseur-c{N}.md \\
      --body    path/to/{brand}-penseur-body-c{N}.md \\
      [--brief  path/to/{brand}-brief-analysis.md] \\
      [--concept N] \\
      [--json-output]

Exit codes :
  0 = PASS (pas de violations)
  1 = FAIL (≥1 violation bloquante)
  2 = ERREUR fichier ou paramètre
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys


# ---------------------------------------------------------------------------
# Vocabulaire (listes nominatives — vivent ici, jamais dans le prompt)
# ---------------------------------------------------------------------------

# Hard banned : fontes invisibles + generic serifs + tasteful reflex traps.
# Ces fontes ont été retirées du pool. Le check est un FILET DE SÉCURITÉ
# qui flagge si une fonte bannie ressort malgré tout (bug pool ou autre).
HARD_BANNED = {
    # Invisibles SaaS defaults
    'Inter', 'Inter Tight', 'Roboto', 'Roboto Flex',
    'Open Sans', 'Lato', 'Montserrat', 'Poppins',
    'Helvetica', 'Arial',
    'Source Sans 3', 'Source Sans Pro',
    'Public Sans', 'Nunito Sans',
    'IBM Plex Sans', 'IBM Plex Sans Condensed',
    'DM Sans', 'Plus Jakarta Sans',
    # Generic serifs
    'Times New Roman', 'Georgia', 'Garamond', 'Palatino',
    'Book Antiqua', 'Bookman', 'Cambria',
    # Tasteful reflex traps
    'Fraunces', 'Cormorant', 'Cormorant Garamond',
    'Cormorant Infant', 'Cormorant Upright',
    'Playfair Display', 'DM Serif Display', 'DM Serif Text',
    'EB Garamond',
    # Slop documenté
    'Quicksand', 'Roboto Slab',
}

# Fontes à risque de slop émergent — autorisées dans le pool mais nécessitent
# une justification spécifique si placées en top 3 de la longlist.
SLOP_RISK_EMERGING = {
    'Outfit', 'Switzer', 'Cabinet Grotesk', 'Manrope',
    'Anton', 'Oswald', 'Space Mono', 'Space Grotesk',
    'Bricolage Grotesque', 'Syne', 'General Sans', 'Clash Display',
}

# Pairings explicitement bannis (tuple display × body, casse-insensitive)
CLOSED_BANNED_PAIRINGS = [
    ('Playfair Display', 'Lato'),
    ('Cormorant', 'Montserrat'),
    ('Cormorant Garamond', 'Montserrat'),
    ('Poppins', 'Open Sans'),
    ('Inter', 'Inter Mono'),
    ('Georgia', 'Verdana'),
    ('Lato', 'Roboto'),
]

# Patterns de justification générique à rejeter
GENERIC_JUSTIFICATION_PATTERNS = [
    r'\btasteful\b',
    r'\bton\s+moderne\b',
    r'\btr[èe]s\s+[ée]l[ée]gant(e)?\b',
    r'\bton\s+universel\b',
    r'\bconvient\s+bien\b', r'\bsied\s+bien\b',
    r'\bdans\s+l[\'’]?\s*air\s+du\s+temps\b',
    r'\btendance\s+actuelle\b',
    r'\bcontemporain(e)?\s+et\s+(moderne|distinctive)\b',
    r'\bclassique\s+intemporel(le)?\b',
    r'\bsobre\s+et\s+raffin[ée]e?\b',
    r'\bidentit[ée]\s+forte\b',
    r'\bpolyvalent(e)?\b',
]

# Tokens qui indiquent un brief dashboard / data-dense / SaaS UI
DASHBOARD_TOKENS = [
    'dashboard', 'data-dense', 'data dense', 'saas ui',
    'admin panel', 'admin tool', 'cockpit',
    'data viz', 'data visualization', 'data visualisation',
    'cli', 'terminal', 'command line', 'developer tool',
    'analytics platform', 'monitoring',
]

# Tokens qui indiquent un brief editorial / creative
EDITORIAL_TOKENS = [
    'editorial', 'magazine', 'long-form', 'longform',
    'storytelling', 'cultural institution', 'museum',
    'hospitality', 'fashion', 'luxury',
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fail(check, severity, detail, suggestion=None):
    return {
        'check': check,
        'severity': severity,
        'detail': detail,
        'suggestion': suggestion or '',
    }


def load_axes_tags(skill_dir):
    """Charge ref/font-axes-tags.json (mapping fonte → 3 axes)."""
    path = os.path.join(skill_dir, 'ref', 'font-axes-tags.json')
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    # Filtrer les clés meta (commençant par _)
    return {k: v for k, v in data.items() if not k.startswith('_')}


def parse_longlist(content, expected_count_min, expected_count_max):
    """
    Parse le markdown d'un penseur pour extraire (rang, nom, justification).

    2 formats supportés :
      Format A (prompt actuel) :
          ## Longlist ordonnée (12-15 candidates)
          1. [Nom] — [justification spécifique...]
          2. ...
      Format B (Camille 0415, h3 + multi-line) :
          ## Longlist ordonnée (12 candidates)
          ### 1. Nom (notes)
          Justification multi-line...
          ### 2. Nom
          ...

    Renvoie : list[dict] = [{rang, name, justification}, ...]
    """
    # Priorité 1 : "## Longlist ordonnée" (format canonique)
    # Priorité 2 : "## Longlist Display" / "## Longlist Body"
    # On prend la PLUS LONGUE section trouvée (l'autre est probablement un header vide).
    candidates = []
    for m in re.finditer(
        r'##\s*(?:\d+\.\s*)?Longlist\s+(ordonn[ée]e?|display|body)[^\n]*\n(.*?)(?=\n##\s|\Z)',
        content, re.DOTALL | re.IGNORECASE
    ):
        candidates.append(m.group(2))
    if not candidates:
        return []
    # Sélectionner la section avec le plus de contenu (probablement la longlist réelle)
    section = max(candidates, key=len)

    entries = []

    # Format B : ### N. Nom OU ### Rang N — Nom OU ### Rang N - Nom \n justification multi-line
    h3_re = re.compile(
        r'^###\s+(?:Rang\s+)?(\d{1,2})[\.\s\-—:]+\s*(.+?)$\n+(.*?)(?=^###\s+|\Z)',
        re.MULTILINE | re.DOTALL | re.IGNORECASE
    )
    for m in h3_re.finditer(section):
        rang = int(m.group(1))
        name_raw = m.group(2).strip()
        # Nettoyer "(poids 800-900)" ou similaires en parenthèses
        name = re.sub(r'\s*\([^)]+\)\s*$', '', name_raw).strip()
        # Nettoyer markdown emphasis
        name = re.sub(r'^\*+|\*+$', '', name).strip()
        justification = m.group(3).strip()
        entries.append({'rang': rang, 'name': name, 'justification': justification})

    # Format A si format B n'a rien matché : "1. Nom — justification" sur 1 ligne
    if not entries:
        line_re = re.compile(
            r'^\s*(\d{1,2})\.\s*\**([^\n*—\-:]+?)\**\s*[—\-:]\s*(.+?)$',
            re.MULTILINE
        )
        for m in line_re.finditer(section):
            rang = int(m.group(1))
            name = m.group(2).strip()
            justification = m.group(3).strip()
            entries.append({'rang': rang, 'name': name, 'justification': justification})

    entries.sort(key=lambda e: e['rang'])
    return entries


def detect_brief_register(brief_content):
    """Renvoie un set de tokens registre détectés dans le brief."""
    if not brief_content:
        return set()
    lower = brief_content.lower()
    detected = set()
    for tok in DASHBOARD_TOKENS:
        if tok.lower() in lower:
            detected.add('dashboard')
            break
    for tok in EDITORIAL_TOKENS:
        if tok.lower() in lower:
            detected.add('editorial')
            break
    return detected


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_format_strict(entries, expected_min, expected_max, label):
    """Vérifie format strict : N entries entre min et max, rang continu 1..N."""
    violations = []
    if not entries:
        violations.append(fail(
            f'format_{label}',
            'FAIL',
            f'Aucune longlist détectée pour {label}',
            'Vérifier que le penseur a bien produit la section "## Longlist ordonnée"',
        ))
        return violations
    if len(entries) < expected_min or len(entries) > expected_max:
        violations.append(fail(
            f'format_{label}',
            'FAIL',
            f'Longlist {label} = {len(entries)} fontes (attendu {expected_min}-{expected_max})',
            f'Le penseur doit produire entre {expected_min} et {expected_max} candidates ordonnées',
        ))
    expected_ranks = list(range(1, len(entries) + 1))
    actual_ranks = [e['rang'] for e in entries]
    if actual_ranks != expected_ranks:
        violations.append(fail(
            f'format_{label}_ranks',
            'FAIL',
            f'Rangs {label} non continus : {actual_ranks}',
            'Le penseur doit numéroter ses candidates 1, 2, 3... sans saut',
        ))
    return violations


def check_no_hard_banned(entries, label):
    """Filet de sécurité : aucune fonte HARD_BANNED ne doit ressortir."""
    violations = []
    for e in entries:
        if e['name'] in HARD_BANNED:
            violations.append(fail(
                f'hard_banned_{label}',
                'FAIL',
                f"{label} rang {e['rang']} = '{e['name']}' (banned absolute)",
                'Pool sale ou penseur a halluciné. Vérifier le pool et le filtrer.',
            ))
    return violations


def check_justifications_specific(entries, label):
    """Détecte les justifications génériques."""
    violations = []
    for e in entries:
        for pattern in GENERIC_JUSTIFICATION_PATTERNS:
            if re.search(pattern, e['justification'], re.IGNORECASE):
                violations.append(fail(
                    f'generic_justification_{label}',
                    'FAIL',
                    f"{label} rang {e['rang']} '{e['name']}' : justification générique "
                    f"(pattern '{pattern}'). Texte : {e['justification'][:120]}",
                    'Reformuler avec une caractéristique visuelle UNIQUE de cette fonte qui '
                    'sert CE concept (test : la justification ne devrait pas s\'appliquer à '
                    '5 autres fontes de la même catégorie).',
                ))
                break  # Un seul pattern matché suffit pour la fonte
    return violations


def check_top3_slop_risk_justified(entries, label):
    """Si SLOP_RISK_EMERGING dans top 3, exiger justification spécifique (≥150 chars)."""
    violations = []
    for e in entries[:3]:
        if e['name'] in SLOP_RISK_EMERGING:
            justif_len = len(e['justification'])
            if justif_len < 150:
                violations.append(fail(
                    f'slop_risk_unjustified_{label}',
                    'FAIL',
                    f"{label} rang {e['rang']} '{e['name']}' : SLOP_RISK_EMERGING en top 3 "
                    f"avec justification trop courte ({justif_len} chars, min 150). "
                    f"Texte : {e['justification']}",
                    f"'{e['name']}' est largement utilisée et glisse vers le slop. "
                    f"Justifier explicitement pourquoi cette fonte vs alternative distinctive.",
                ))
    return violations


def check_pairing_structural_contrast(display_entries, body_entries, axes_db):
    """Display rang 1 × body rang 1 : au moins 1 axe différent."""
    violations = []
    if not display_entries or not body_entries:
        return violations
    d1 = display_entries[0]['name']
    b1 = body_entries[0]['name']
    if d1 == b1:
        # Mono-fonte assumée — OK selon R-body-3 (pas violation)
        return violations
    if d1 not in axes_db:
        violations.append(fail(
            'pairing_axes_unknown',
            'WARN',
            f"Display rang 1 '{d1}' absent de font-axes-tags.json — check pairing impossible",
            'Ajouter les tags axes structurels pour cette fonte dans ref/font-axes-tags.json',
        ))
        return violations
    if b1 not in axes_db:
        violations.append(fail(
            'pairing_axes_unknown',
            'WARN',
            f"Body rang 1 '{b1}' absent de font-axes-tags.json — check pairing impossible",
            'Ajouter les tags axes structurels pour cette fonte dans ref/font-axes-tags.json',
        ))
        return violations
    d_axes = axes_db[d1]
    b_axes = axes_db[b1]
    diffs = sum(1 for axis in ('structure', 'construction', 'proportion')
                if d_axes.get(axis) != b_axes.get(axis))
    if diffs == 0:
        violations.append(fail(
            'pairing_no_contrast',
            'FAIL',
            f"Pairing display × body sans contraste structurel : "
            f"'{d1}' et '{b1}' partagent les 3 axes "
            f"({d_axes.get('structure')}/{d_axes.get('construction')}/{d_axes.get('proportion')})",
            'Trouver une fonte body qui diverge sur au moins 1 axe (structure/construction/proportion). '
            'Ou assumer mono-fonte explicitement (display = body).',
        ))
    return violations


def check_pairing_not_closed_banned(display_entries, body_entries):
    """Pairing display rang 1 × body rang 1 ne doit pas être dans la liste fermée."""
    violations = []
    if not display_entries or not body_entries:
        return violations
    d1 = display_entries[0]['name']
    b1 = body_entries[0]['name']
    for (banned_d, banned_b) in CLOSED_BANNED_PAIRINGS:
        if d1.lower() == banned_d.lower() and b1.lower() == banned_b.lower():
            violations.append(fail(
                'pairing_closed_ban',
                'FAIL',
                f"Pairing '{d1}' × '{b1}' est explicitement banni (cliché slop daté)",
                'Choisir un pairing différent — chacune des fontes peut rester si pairing change.',
            ))
    return violations


def check_dashboard_no_serif(display_entries, body_entries, register, axes_db):
    """Si brief = dashboard, display rang 1 et body rang 1 ne doivent pas être serif/slab."""
    violations = []
    if 'dashboard' not in register:
        return violations
    for label, entries in [('display', display_entries), ('body', body_entries)]:
        if not entries:
            continue
        n1 = entries[0]['name']
        if n1 not in axes_db:
            continue
        struct = axes_db[n1].get('structure')
        if struct in ('serif', 'slab', 'blackletter'):
            violations.append(fail(
                f'dashboard_{label}_serif',
                'FAIL',
                f"Brief dashboard/SaaS UI mais {label} rang 1 = '{n1}' (structure '{struct}')",
                'Pour dashboard/data-dense : pairing sans+sans (idéalement sans + mono pour data). '
                'Sérif strictement banni en interface technique.',
            ))
    return violations


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Phase 3B-1 Fonts Anti-Slop Gate')
    parser.add_argument('--display', required=True, help='Path to {brand}-penseur-c{N}.md')
    parser.add_argument('--body', required=True, help='Path to {brand}-penseur-body-c{N}.md')
    parser.add_argument('--brief', help='Path to {brand}-brief-analysis.md (optionnel)')
    parser.add_argument('--concept', type=int, default=0, help='Numéro de concept (1, 2, 3)')
    parser.add_argument('--json-output', action='store_true', help='Output JSON structuré')
    parser.add_argument('--skill-dir', help='Path to skill root (auto-detect par défaut)')
    args = parser.parse_args()

    # Auto-detect skill_dir : ce script est dans scripts/, parent = skill root
    skill_dir = args.skill_dir or os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )

    # Lire les 3 fichiers
    if not os.path.exists(args.display):
        print(f"❌ Fichier display introuvable : {args.display}", file=sys.stderr)
        sys.exit(2)
    if not os.path.exists(args.body):
        print(f"❌ Fichier body introuvable : {args.body}", file=sys.stderr)
        sys.exit(2)
    with open(args.display, encoding='utf-8') as f:
        display_content = f.read()
    with open(args.body, encoding='utf-8') as f:
        body_content = f.read()
    brief_content = ''
    if args.brief and os.path.exists(args.brief):
        with open(args.brief, encoding='utf-8') as f:
            brief_content = f.read()

    # Parser
    display_entries = parse_longlist(display_content, 12, 15)
    body_entries = parse_longlist(body_content, 10, 10)
    register = detect_brief_register(brief_content)
    axes_db = load_axes_tags(skill_dir)

    # Lancer les checks
    all_violations = []
    all_violations += check_format_strict(display_entries, 12, 15, 'display')
    all_violations += check_format_strict(body_entries, 10, 10, 'body')
    all_violations += check_no_hard_banned(display_entries, 'display')
    all_violations += check_no_hard_banned(body_entries, 'body')
    all_violations += check_justifications_specific(display_entries, 'display')
    all_violations += check_justifications_specific(body_entries, 'body')
    all_violations += check_top3_slop_risk_justified(display_entries, 'display')
    all_violations += check_top3_slop_risk_justified(body_entries, 'body')
    all_violations += check_pairing_structural_contrast(display_entries, body_entries, axes_db)
    all_violations += check_pairing_not_closed_banned(display_entries, body_entries)
    all_violations += check_dashboard_no_serif(display_entries, body_entries, register, axes_db)

    # Filtrer FAIL strict (les WARN sont informationnels)
    fail_violations = [v for v in all_violations if v['severity'] == 'FAIL']
    verdict = 'FAIL' if fail_violations else 'PASS'
    exit_code = 1 if fail_violations else 0

    if args.json_output:
        output = {
            'verdict': verdict,
            'concept': args.concept,
            'display_file': args.display,
            'body_file': args.body,
            'display_count': len(display_entries),
            'body_count': len(body_entries),
            'register_detected': sorted(register),
            'axes_db_loaded': len(axes_db),
            'violations': all_violations,
            'fail_count': len(fail_violations),
            'warn_count': len([v for v in all_violations if v['severity'] == 'WARN']),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'=' * 60}")
        print(f"Phase 3B-1 Fonts Anti-Slop — Concept {args.concept} — Verdict : {verdict}")
        print(f"{'=' * 60}")
        print(f"Display : {len(display_entries)} fontes — {os.path.basename(args.display)}")
        print(f"Body    : {len(body_entries)} fontes — {os.path.basename(args.body)}")
        print(f"Register détecté : {sorted(register) or '∅'}")
        print(f"Axes DB : {len(axes_db)} fontes")
        print()
        if not all_violations:
            print("✅ 7/7 checks OK — pas de violations détectées")
        else:
            print(f"⚠ {len(fail_violations)} FAIL + "
                  f"{len([v for v in all_violations if v['severity'] == 'WARN'])} WARN détectés :\n")
            for v in all_violations:
                icon = '❌' if v['severity'] == 'FAIL' else '⚠'
                print(f"  {icon} [{v['check']}] {v['detail']}")
                if v.get('suggestion'):
                    print(f"      → {v['suggestion']}")

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
