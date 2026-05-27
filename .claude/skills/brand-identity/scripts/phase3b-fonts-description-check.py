#!/usr/bin/env python3
"""
Phase 3B-2 Designer Interaction 1 — Description Visual Check

Cross-check les descriptions visuelles produites par le designer Interaction 1
contre les axes structurels réels des fontes (via font-axes-tags.json).

Détecte les hallucinations LLM vision où une fonte est mal identifiée
(ex: Sporting Grotesque taggée 'sans' décrite comme 'sérif Didone-light').

Usage :
  python3 phase3b-fonts-description-check.py \\
      --descriptions path/to/{brand}-descriptions-c{N}.md \\
      --session-dir path/to/{session_dir} \\
      [--concept N] \\
      [--json-output]

Flow :
  1. Parse le fichier descriptions par bloc (Planche X, Font YZ)
  2. Pour chaque bloc : lit le mapping JSON de la planche (font-pool-duo-{display,body}-c{N}-X-mapping.json)
     → résout (planche, position) → nom de fonte
  3. Lit ref/font-axes-tags.json → structure réelle (sans/serif/slab/monospace/etc.)
  4. Détecte la structure suggérée par la description (mots-clés)
  5. Si conflit → FAIL avec liste précise

Exit codes :
  0 = PASS (pas d'incohérence détectée)
  1 = FAIL (≥1 hallucination détectée)
  2 = ERREUR fichier ou paramètre
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys


# ---------------------------------------------------------------------------
# Vocabulaire — keywords par structure
# ---------------------------------------------------------------------------

# Patterns ordonnés par priorité de détection.
# CRITIQUE : "sans-serif" / "sans serif" doit être détecté AVANT "serif" seul,
# sinon on classerait à tort un sans-serif comme serif.

PATTERNS_SANS_COMPOSED = [
    r'\bsans[\s\-]+serifs?\b',
    r'\bsans[\s\-]+s[ée]rifs?\b',
    r'\bsans[\s\-]?serifs?\b',
]

PATTERNS_SERIF_BARE = [
    r'\bs[ée]rifs?\b',
    r'\bdidone\b',
    r'\btransitional\b',
    r'\bold[\s\-]?style\b',
    r'\bgaralde\b',
    r'\baldine\b',
    r'\bvenetian\b',
    r'\bgaramondesque\b',
    r'\bbaskerville\b',
    r'\bcaslon\b',
]

PATTERNS_SANS = [
    r'\bgrotesque?s?\b',  # grotesk / grotesque
    r'\bgrotesks?\b',
    r'\bneo[\s\-]grotesque?\b',
    r'\bhumanist[e]?\s+sans\b',
    r'\bgeometric\s+sans\b',
    r'\bgeometric\s+humaniste?\b',
    r'\bsans\s+humaniste?\b',
]

PATTERNS_SLAB = [
    r'\bslabs?\b',
    r'\bclarendon\b',
    r'\begyptien(ne)?\b',
    r'\begyptian\b',
]

PATTERNS_MONO = [
    r'\bmonospaced?\b',
    r'\bmono\b',
    r'\bfixed[\s\-]?widths?\b',
    r'\blargeur[\s\-]+fixe\b',
    r'\bchasse[\s\-]+fixe\b',
]

PATTERNS_BLACKLETTER = [
    r'\bblackletters?\b',
    r'\bgothic\b',
    r'\btextura\b',
    r'\bfrakturs?\b',
    r'\bgothique\b',
]


def detect_structure(text):
    """
    Détecte la(les) structure(s) suggérée(s) par le texte de description.
    Renvoie un set : {'sans', 'serif', 'slab', 'monospace', 'blackletter'}.
    Vide si aucune structure n'est détectable (description vague).

    Algorithme :
    1. Détecte d'abord 'sans' composé (sans-serif, sans serif) → sans
    2. Détecte 'serif' bare (sérif, didone, transitional, ...) → serif
       MAIS seulement si pas déjà détecté 'sans' (anti-faux-positif "sans serif")
    3. Détecte autres patterns indépendants : sans bare, slab, mono, blackletter
    """
    text_lower = text.lower()
    detected = set()

    # 1. "sans-serif" / "sans serif" (composé) → sans (priorité)
    has_sans_composed = any(re.search(p, text_lower) for p in PATTERNS_SANS_COMPOSED)
    if has_sans_composed:
        detected.add('sans')

    # 2. "serif" bare → serif (uniquement si pas de "sans-serif" composé)
    if not has_sans_composed:
        if any(re.search(p, text_lower) for p in PATTERNS_SERIF_BARE):
            detected.add('serif')

    # 3. Autres patterns sans (grotesk, humaniste sans, geometric sans)
    if any(re.search(p, text_lower) for p in PATTERNS_SANS):
        detected.add('sans')

    # 4. Slab
    if any(re.search(p, text_lower) for p in PATTERNS_SLAB):
        detected.add('slab')

    # 5. Monospace
    if any(re.search(p, text_lower) for p in PATTERNS_MONO):
        detected.add('monospace')

    # 6. Blackletter
    if any(re.search(p, text_lower) for p in PATTERNS_BLACKLETTER):
        detected.add('blackletter')

    return detected


# Conflits explicites : (description_dit, axe_réel) → message
CONFLICT_PAIRS = [
    ('serif', 'sans'),
    ('serif', 'monospace'),
    ('sans', 'serif'),
    ('sans', 'slab'),
    ('slab', 'sans'),
    ('slab', 'monospace'),
    ('monospace', 'sans'),
    ('monospace', 'serif'),
    ('monospace', 'slab'),
    ('blackletter', 'sans'),
    ('blackletter', 'serif'),
    ('blackletter', 'monospace'),
]


def is_conflict(detected_structures, real_structure):
    """
    Renvoie True si une des structures détectées dans la description entre en
    conflit explicite avec la structure réelle (du tag axe).
    """
    if not detected_structures:
        return False  # description trop vague, pas de check possible
    if real_structure in detected_structures:
        return False  # match au moins partiel → OK
    for detected in detected_structures:
        if (detected, real_structure) in CONFLICT_PAIRS:
            return True
    # Cas spécial : 'display' et 'experimental' (du tags JSON) sont des catégories
    # transversales qui peuvent contenir n'importe quelle structure visuelle.
    # On ne flagge pas de conflit pour ces axes flous.
    return False


# ---------------------------------------------------------------------------
# Parser markdown
# ---------------------------------------------------------------------------

def parse_descriptions(content):
    """
    Parse le fichier descriptions par bloc Planche × Font.

    Format attendu :
        ### Planche display 4 (font-pool-duo-display-c2-4)
        **Font 01**
        - ...descriptions...

        **Font 02**
        - ...descriptions...

    Renvoie : list[dict] = [{plate_type, plate_num, font_pos, description}, ...]
    """
    blocks = []

    # Trouver les sections "### Planche {display|body} N (font-pool-duo-...)"
    plate_re = re.compile(
        r'###\s+Planche\s+(display|body)\s+(\d+)[^\n]*\n(.*?)(?=^###\s+Planche|\Z)',
        re.MULTILINE | re.DOTALL | re.IGNORECASE
    )

    for plate_match in plate_re.finditer(content):
        plate_type = plate_match.group(1).lower()
        plate_num = int(plate_match.group(2))
        plate_content = plate_match.group(3)

        # Trouver les blocs **Font 01** / **Font 02** dans la planche
        font_re = re.compile(
            r'\*\*Font\s+(\d+)\*\*\s*\n(.*?)(?=\n\*\*Font\s+\d+\*\*|\Z)',
            re.DOTALL | re.IGNORECASE
        )
        for font_match in font_re.finditer(plate_content):
            font_pos = font_match.group(1).zfill(2)  # "01" / "02"
            description = font_match.group(2).strip()
            blocks.append({
                'plate_type': plate_type,
                'plate_num': plate_num,
                'font_pos': font_pos,
                'description': description,
            })

    return blocks


def load_plate_mapping(session_dir, plate_type, plate_num, concept_num):
    """Charge le mapping JSON d'une planche duo (numéro→nom de fonte)."""
    pattern = f'font-pool-duo-{plate_type}-c{concept_num}-{plate_num}-mapping.json'
    path = os.path.join(session_dir, pattern)
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def load_axes_tags(skill_dir):
    """Charge ref/font-axes-tags.json (mapping fonte → 3 axes)."""
    path = os.path.join(skill_dir, 'ref', 'font-axes-tags.json')
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if not k.startswith('_')}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Designer Interaction 1 description ↔ axes check')
    parser.add_argument('--descriptions', required=True,
                        help='Path to {brand}-descriptions-c{N}.md')
    parser.add_argument('--session-dir', required=True,
                        help='Path to {session_dir} (où sont les *-mapping.json)')
    parser.add_argument('--concept', type=int, required=True, help='Numéro de concept (1, 2, 3)')
    parser.add_argument('--json-output', action='store_true', help='Output JSON structuré')
    parser.add_argument('--skill-dir', help='Path to skill root (auto-detect par défaut)')
    args = parser.parse_args()

    skill_dir = args.skill_dir or os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )

    if not os.path.exists(args.descriptions):
        print(f"❌ Fichier descriptions introuvable : {args.descriptions}", file=sys.stderr)
        sys.exit(2)
    if not os.path.isdir(args.session_dir):
        print(f"❌ Session dir introuvable : {args.session_dir}", file=sys.stderr)
        sys.exit(2)

    with open(args.descriptions, encoding='utf-8') as f:
        content = f.read()

    blocks = parse_descriptions(content)
    if not blocks:
        result = {
            'verdict': 'FAIL',
            'detail': 'Aucun bloc Planche×Font détecté dans le fichier descriptions',
            'violations': [],
        }
        if args.json_output:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ {result['detail']}")
        sys.exit(1)

    axes_db = load_axes_tags(skill_dir)
    if not axes_db:
        print(f"⚠ ref/font-axes-tags.json non trouvé — check impossible", file=sys.stderr)
        sys.exit(2)

    violations = []
    checked_count = 0
    for block in blocks:
        mapping = load_plate_mapping(args.session_dir, block['plate_type'],
                                      block['plate_num'], args.concept)
        if not mapping:
            violations.append({
                'check': 'mapping_missing',
                'severity': 'WARN',
                'detail': f"Planche {block['plate_type']} {block['plate_num']} : "
                          f"mapping JSON introuvable",
            })
            continue

        font_name = mapping.get(block['font_pos'])
        if not font_name:
            violations.append({
                'check': 'font_pos_unknown',
                'severity': 'WARN',
                'detail': f"Planche {block['plate_type']} {block['plate_num']} "
                          f"position {block['font_pos']} : pas de fonte dans le mapping",
            })
            continue

        if font_name not in axes_db:
            violations.append({
                'check': 'axes_unknown',
                'severity': 'WARN',
                'detail': f"Fonte '{font_name}' absente de font-axes-tags.json — "
                          f"check d'axe impossible pour Planche {block['plate_type']} "
                          f"{block['plate_num']} F{block['font_pos']}",
            })
            continue

        real_structure = axes_db[font_name].get('structure')
        detected = detect_structure(block['description'])
        checked_count += 1

        if is_conflict(detected, real_structure):
            violations.append({
                'check': 'description_axis_conflict',
                'severity': 'FAIL',
                'detail': f"Planche {block['plate_type']} {block['plate_num']} "
                          f"F{block['font_pos']} = '{font_name}' (structure réelle : "
                          f"'{real_structure}') mais description suggère "
                          f"'{'/'.join(sorted(detected))}'",
                'plate_type': block['plate_type'],
                'plate_num': block['plate_num'],
                'font_pos': block['font_pos'],
                'font_name': font_name,
                'real_structure': real_structure,
                'detected_structures': sorted(detected),
                'description_excerpt': block['description'][:200].replace('\n', ' '),
                'suggestion': f"Re-décrire la fonte '{font_name}' en respectant "
                              f"sa structure réelle ({real_structure}). "
                              f"Hallucination LLM probable sur fonte à caractère unique.",
            })

    fail_violations = [v for v in violations if v['severity'] == 'FAIL']
    verdict = 'FAIL' if fail_violations else 'PASS'
    exit_code = 1 if fail_violations else 0

    if args.json_output:
        output = {
            'verdict': verdict,
            'concept': args.concept,
            'descriptions_file': args.descriptions,
            'blocks_detected': len(blocks),
            'blocks_checked': checked_count,
            'fail_count': len(fail_violations),
            'warn_count': len([v for v in violations if v['severity'] == 'WARN']),
            'violations': violations,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'=' * 60}")
        print(f"Designer Interaction 1 — Description Check — "
              f"Concept {args.concept} — Verdict : {verdict}")
        print(f"{'=' * 60}")
        print(f"Blocs détectés : {len(blocks)}")
        print(f"Blocs checkés (mapping + axes connus) : {checked_count}")
        print()
        if not violations:
            print("✅ Pas d'incohérence description↔axe détectée")
        else:
            for v in violations:
                icon = '❌' if v['severity'] == 'FAIL' else '⚠'
                print(f"  {icon} [{v['check']}] {v['detail']}")
                if v.get('description_excerpt'):
                    print(f"      Description : {v['description_excerpt']}")
                if v.get('suggestion'):
                    print(f"      → {v['suggestion']}")
                print()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
