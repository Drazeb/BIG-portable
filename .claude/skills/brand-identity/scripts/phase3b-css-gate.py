#!/usr/bin/env python3
"""
Phase 3B CSS Gate — Pitch Quality Verifier

Scans a pitch markdown file for CSS technical prescriptions that should
be expressed as sensations/intentions instead.

Usage: python3 phase3b-css-gate.py path/to/pitch.md

Exit code 0 = PASS (no CSS prescriptions found)
Exit code 1 = FAIL (CSS prescriptions detected)

The gate checks two things:
1. BLOCK: CSS property/function names that should never appear in a pitch
2. WARN: Technical vocabulary that might be acceptable but warrants review
"""

import re
import sys


# ---------------------------------------------------------------------------
# CSS terms that should NEVER appear in a pitch
# ---------------------------------------------------------------------------

BLOCKED_TERMS = [
    # CSS properties
    (r'\bclip-path\b', 'clip-path'),
    (r'\bmask-image\b', 'mask-image'),
    (r'\bbackdrop-filter\b', 'backdrop-filter'),
    (r'\bmix-blend-mode\b', 'mix-blend-mode'),
    (r'\bbackground-blend-mode\b', 'background-blend-mode'),
    (r'\bbox-shadow\s*:', 'box-shadow (valeur)'),
    (r'\btext-shadow\s*:', 'text-shadow (valeur)'),
    (r'\btransform\s*:', 'transform (valeur)'),
    (r'\bfilter\s*:', 'filter (valeur)'),
    (r'\bz-index\b', 'z-index'),
    (r'\bnegative?\s*margins?\b', 'negative margin'),
    (r'\bgrid-template(?:-columns|-rows)?\s*:', 'grid-template (valeur)'),
    (r'\bflex-direction\b', 'flex-direction'),
    (r'\bborder-radius\s*:\s*\d', 'border-radius (valeur exacte)'),
    (r'\bletter-spacing\s*:\s*[\d.]', 'letter-spacing (valeur exacte)'),
    (r'\bpadding(?:-block|-inline)?\s*:\s*\d', 'padding (valeur exacte)'),
    (r'\bmargin(?:-block|-inline)?\s*:\s*-?\d', 'margin (valeur exacte)'),

    # CSS functions
    (r'\bcubic-bezier\s*\(', 'cubic-bezier()'),
    (r'\bcolor-mix\s*\(', 'color-mix()'),
    (r'\bconic-gradient\s*\(', 'conic-gradient()'),
    (r'\bradial-gradient\s*\(', 'radial-gradient()'),
    (r'\blinear-gradient\s*\(', 'linear-gradient()'),
    (r'\boklch\s*\(', 'oklch()'),
    (r'\btranslateY?\s*\(', 'translate()'),
    (r'\bscale\s*\(\s*[\d.]', 'scale() avec valeur'),
    (r'\brotate\s*\(\s*[\d.]', 'rotate() avec valeur'),

    # CSS at-rules / features
    (r'@property\b', '@property'),
    (r'@keyframes\b', '@keyframes'),
    (r'@starting-style\b', '@starting-style'),
    (r'\banimation-timeline\b', 'animation-timeline'),

    # SVG filter specifics
    (r'\bfeTurbulence\b', 'feTurbulence'),
    (r'\bbaseFrequency\b', 'baseFrequency'),
    (r'\bnumOctaves\b', 'numOctaves'),

    # Exact values (numbers with CSS units in technical context)
    (r'\b\d+ms\b', 'durée en ms'),
    (r'\b\d+vw\b(?!\s*[,)])', 'valeur en vw'),
]

# Sections to SKIP (these legitimately contain technical terms)
# Palette hex codes, font names, etc.
SKIP_PATTERNS = [
    r'<span\s+style=',  # inline pastilles HTML (OK)
    r'Calibrage\s+A=',  # calibrage header
    r'\*\*Composition\s+Voice\s+Block\*\*\s*:', # composition type declaration
    r'Voice\s+Block\*?\*?\s*:\s*\*?\*?(?:Centré|Split|Full-bleed|Superposition|Grille|Diagonale|Scroll|Minimaliste)',  # composition type line
]


def should_skip_line(line: str) -> bool:
    """Check if a line should be excluded from scanning."""
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, line):
            return True
    return False


def scan_pitch(content: str) -> list[dict]:
    """Scan pitch content for CSS prescriptions. Returns list of violations."""
    violations = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        if should_skip_line(line):
            continue

        for pattern, label in BLOCKED_TERMS:
            matches = list(re.finditer(pattern, line, re.IGNORECASE))
            for match in matches:
                # Extract context (surrounding words)
                start = max(0, match.start() - 30)
                end = min(len(line), match.end() + 30)
                context = line[start:end].strip()
                if start > 0:
                    context = '...' + context
                if end < len(line):
                    context = context + '...'

                violations.append({
                    'line': line_num,
                    'term': label,
                    'context': context,
                })

    return violations


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 phase3b-css-gate.py <path/to/pitch.md>")
        sys.exit(2)

    filepath = sys.argv[1]

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erreur: fichier introuvable — {filepath}")
        sys.exit(2)

    violations = scan_pitch(content)

    # Output
    filename = filepath.rsplit('/', 1)[-1] if '/' in filepath else filepath
    print(f"\n=== PHASE 3B CSS GATE ===")
    print(f"File: {filename}")
    print()

    if not violations:
        print("VERDICT: PASS — aucune prescription CSS détectée")
        print("Le pitch décrit des sensations et intentions, pas des techniques.")
        sys.exit(0)

    # Group by term
    by_term: dict[str, list] = {}
    for v in violations:
        by_term.setdefault(v['term'], []).append(v)

    print(f"[FAIL] {len(violations)} prescription(s) CSS détectée(s) dans {len(by_term)} catégorie(s) :\n")

    for term, instances in sorted(by_term.items()):
        print(f"  ❌ {term} ({len(instances)}x)")
        for inst in instances[:3]:  # max 3 examples per term
            print(f"     Ligne {inst['line']}: {inst['context']}")
        if len(instances) > 3:
            print(f"     ... et {len(instances) - 3} autre(s)")
        print()

    print("VERDICT: FAIL — corrections requises")
    print("Chaque prescription CSS doit être reformulée en SENSATION ou EFFET VISUEL.")
    print("Exemples : 'clip-path' → 'sections découpées en diagonale'")
    print("           'backdrop-filter blur' → 'profondeur givrée, arrière-plan flou'")
    print("           'cubic-bezier + 350ms' → 'rebond élastique, mouvement vif'")

    sys.exit(1)


if __name__ == '__main__':
    main()
