#!/usr/bin/env python3
"""
Phase 4 Blacklist Gate — Style-Tile Anti-Pattern Verifier

Scans a generated style-tile HTML file for dated CSS patterns (2015-2020)
that should not appear in modern outputs.

Usage: python3 phase4-blacklist-gate.py path/to/style-tile.html [--no-images] [--json-output PATH]

Exit code 0 = PASS (no dated patterns found)
Exit code 1 = FAIL (dated patterns detected — list violations)

--json-output PATH : écrit en plus du stdout un JSON structuré
  {gate, html_audited, html_sha256, timestamp, verdict, fails:[...], warns:[...]}
  La sortie stdout reste inchangée (compat ascendante — parsée par la boucle 4A de Phase 4).
"""

import datetime
import hashlib
import json
import re
import sys


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_hover_blocks(css: str) -> list[tuple[int, str]]:
    """Extract all :hover rule blocks with their starting line numbers."""
    blocks = []
    lines = css.split('\n')
    i = 0
    while i < len(lines):
        if ':hover' in lines[i]:
            start = i
            brace_count = 0
            block_lines = []
            for j in range(i, len(lines)):
                block_lines.append(lines[j])
                brace_count += lines[j].count('{') - lines[j].count('}')
                if brace_count <= 0 and '{' in ''.join(block_lines):
                    break
            blocks.append((start + 1, '\n'.join(block_lines)))
            i = j + 1 if 'j' in dir() else i + 1
        else:
            i += 1
    return blocks


def extract_keyframes(css: str) -> list[tuple[int, str, str]]:
    """Extract @keyframes blocks: (line_num, name, content)."""
    results = []
    lines = css.split('\n')
    i = 0
    while i < len(lines):
        m = re.search(r'@keyframes\s+([\w-]+)', lines[i])
        if m:
            name = m.group(1)
            start = i
            brace_count = 0
            block_lines = []
            for j in range(i, len(lines)):
                block_lines.append(lines[j])
                brace_count += lines[j].count('{') - lines[j].count('}')
                if brace_count <= 0 and len(block_lines) > 1:
                    break
            results.append((start + 1, name, '\n'.join(block_lines)))
            i = j + 1 if 'j' in dir() else i + 1
        else:
            i += 1
    return results


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_hover_translateY(css: str) -> list[dict]:
    """No translateY in any :hover rule."""
    violations = []
    for line_num, block in extract_hover_blocks(css):
        if re.search(r'translateY\s*\(', block):
            violations.append({
                'line': line_num,
                'rule': 'hover-translateY',
                'detail': 'translateY() dans un :hover — remplacer par changement de background/shadow/border',
            })
    return violations


def check_hover_translateX(css: str) -> list[dict]:
    """No translateX on child elements in :hover (arrow slide pattern)."""
    violations = []
    for line_num, block in extract_hover_blocks(css):
        if re.search(r'translate[X]?\s*\(', block) or re.search(r'translate\s*:\s*\d', block):
            # Allow translateX on non-arrow/icon elements (rare, but check context)
            if re.search(r'arrow|icon|svg|chevron', block, re.IGNORECASE) or \
               re.search(r'translate\s*:\s*\d+px\s+0', block):
                violations.append({
                    'line': line_num,
                    'rule': 'hover-arrow-slide',
                    'detail': 'Arrow/icon qui slide au hover (translateX) — remplacer par changement de couleur/opacité',
                })
    return violations


def check_hover_scale_excessive(css: str) -> list[dict]:
    """No scale > 1.02 in :hover."""
    violations = []
    for line_num, block in extract_hover_blocks(css):
        scales = re.findall(r'scale\s*\(\s*([\d.]+)', block)
        scales += re.findall(r'scale\s*:\s*([\d.]+)', block)
        for s in scales:
            try:
                if float(s) > 1.02:
                    violations.append({
                        'line': line_num,
                        'rule': 'hover-scale-excessive',
                        'detail': f'scale({s}) > 1.02 au hover — max 1.02',
                    })
            except ValueError:
                pass
    return violations


def check_infinite_animations(css: str) -> list[dict]:
    """No decorative infinite animations."""
    violations = []
    lines = css.split('\n')
    for i, line in enumerate(lines, 1):
        if re.search(r'animation\s*:.*\binfinite\b', line) or \
           re.search(r'animation-iteration-count\s*:\s*infinite', line):
            violations.append({
                'line': i,
                'rule': 'animation-infinite',
                'detail': 'Animation infinite décorative — utiliser @starting-style ou animation-timeline: view()',
            })
    return violations


def check_glow_shadows(css: str) -> list[dict]:
    """No box-shadow without vertical offset (0 0 Npx = glow)."""
    violations = []
    lines = css.split('\n')
    for i, line in enumerate(lines, 1):
        # Match box-shadow: 0 0 Npx (glow pattern — no offset)
        # But allow 0 0 0 Npx (outline/ring pattern with spread)
        if re.search(r'box-shadow\s*:', line) or re.search(r'--shadow.*:', line):
            # Find 0 0 Npx patterns (2 zeros then a non-zero blur)
            glows = re.findall(r'(?<!\d)\b0\s+0\s+(\d+)px\b', line)
            for g in glows:
                if int(g) > 0:
                    # Check it's not a ring (0 0 0 Npx = spread only)
                    if not re.search(r'\b0\s+0\s+0\s+\d+px\b', line):
                        violations.append({
                            'line': i,
                            'rule': 'glow-shadow',
                            'detail': f'box-shadow: 0 0 {g}px (glow sans offset) — ajouter un offset vertical',
                        })
                        break  # one per line
    return violations


def check_text_shadow_glow(css: str) -> list[dict]:
    """No text-shadow glow (0 0 Npx)."""
    violations = []
    lines = css.split('\n')
    for i, line in enumerate(lines, 1):
        if re.search(r'text-shadow\s*:.*\b0\s+0\s+\d+px\b', line):
            violations.append({
                'line': i,
                'rule': 'text-shadow-glow',
                'detail': 'text-shadow glow (0 0 Npx) — supprimer ou utiliser un offset',
            })
    return violations


def check_section_clip_path(content: str) -> list[dict]:
    """No zigzag/wave clip-path dividers between sections."""
    violations = []
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if re.search(r'clip-path\s*:\s*polygon\s*\(', line):
            # Collect the full polygon value (may span multiple lines)
            poly_lines = [line]
            j = i
            while j < len(lines) and ')' not in ''.join(poly_lines):
                j += 1
                if j <= len(lines):
                    poly_lines.append(lines[j - 1])
            poly_str = ' '.join(poly_lines)

            # Count coordinate pairs in the polygon
            coords = re.findall(r'[\d.]+%', poly_str)
            num_points = len(coords) // 2  # each point = x% y%

            # A polygon with >6 points is likely a zigzag/wave divider
            # Legitimate clip-paths (angular cuts, simple shapes) have 3-6 points
            if num_points > 6:
                violations.append({
                    'line': i,
                    'rule': 'zigzag-clip-path',
                    'detail': f'clip-path polygon avec {num_points} points (zigzag/wave divider) — les bords de section sont droits',
                })
            else:
                # For simple polygons (≤6 points), check if it's on a section element
                context = '\n'.join(lines[max(0, i-10):i])
                if re.search(r'\.(artifact|atmosphere|voice-block)\b(?!.*img)(?!.*image)(?!.*visual)(?!.*bg)', context):
                    violations.append({
                        'line': i,
                        'rule': 'section-clip-path',
                        'detail': 'clip-path sur une section (séparateur fantaisie) — les bords de section sont droits',
                    })
    return violations


def check_staggered_fadeup(css: str) -> list[dict]:
    """No @keyframes with translateY + opacity (staggered fade-up pattern)."""
    violations = []
    for line_num, name, block in extract_keyframes(css):
        has_translate = bool(re.search(r'translateY|translate\s*\(.*,', block))
        has_opacity = bool(re.search(r'opacity', block))
        if has_translate and has_opacity:
            violations.append({
                'line': line_num,
                'rule': 'staggered-fadeup',
                'detail': f'@keyframes {name} (translateY + opacity) — utiliser @starting-style à la place',
            })
    return violations


def check_backdrop_blur_excessive(css: str) -> list[dict]:
    """No backdrop-filter blur > 16px."""
    violations = []
    lines = css.split('\n')
    for i, line in enumerate(lines, 1):
        m = re.search(r'backdrop-filter\s*:.*blur\s*\(\s*(\d+)', line)
        if m and int(m.group(1)) > 16:
            violations.append({
                'line': i,
                'rule': 'backdrop-blur-excessive',
                'detail': f'backdrop-filter: blur({m.group(1)}px) > 16px — max 12px recommandé',
            })
    return violations


def check_letter_spacing_hover(css: str) -> list[dict]:
    """No letter-spacing transition in :hover."""
    violations = []
    for line_num, block in extract_hover_blocks(css):
        if re.search(r'letter-spacing', block):
            violations.append({
                'line': line_num,
                'rule': 'hover-letter-spacing',
                'detail': 'letter-spacing au hover — cliché footer 2017, remplacer par changement de couleur',
            })
    return violations


def check_underline_scalex(css: str) -> list[dict]:
    """No scaleX(0) → scaleX(1) underline reveal pattern."""
    violations = []
    lines = css.split('\n')
    for i, line in enumerate(lines, 1):
        if re.search(r'scaleX\s*\(\s*0\s*\)', line):
            violations.append({
                'line': i,
                'rule': 'underline-scaleX',
                'detail': 'scaleX(0) underline reveal — remplacer par border-color transition',
            })
    return violations


def check_accent_bar(css: str) -> list[dict]:
    """No thick colored border on card edge as importance marker.

    Also detects pseudo-element accent bars (::before/::after with narrow
    width + tall height + solid background color), and the box-shadow inset
    workaround explicitly named by Impeccable BAN 1.

    Sources:
      - Impeccable sources/impeccable/SKILL.md L207-213 (« Side-stripe borders…
        REWRITE: … Do not just swap to box-shadow inset. »)
      - GStack sources/gstack/design-review.md L1477, L1715 (« Colored
        left-border on cards `border-left: 3px solid <accent>` »)
    """
    violations = []
    lines = css.split('\n')
    for i, line in enumerate(lines, 1):
        # Pattern 1: border-inline-start or border-left >= 2px solid color
        m = re.search(r'border-(?:inline-start|left)\s*:\s*([2-9]\d*|[1-9]\d+)px\s+solid\s+(?!transparent|inherit)', line)
        if m:
            violations.append({
                'line': i,
                'rule': 'accent-bar',
                'detail': f'Bordure latérale colorée {m.group(1)}px (accent bar) — la distinction vient du fond, pas d\'un trait sur le bord',
            })

    # Pattern 2: pseudo-element accent bars
    # Detect ::before/::after with narrow width (<=5px) + tall height (% or large px) + background color
    for i, line in enumerate(lines, 1):
        if re.search(r'::(?:before|after)', line):
            context = '\n'.join(lines[i-1:min(i+12, len(lines))])
            narrow = re.search(r'(?:inline-size|width)\s*:\s*([1-5])px', context)
            tall = re.search(r'(?:block-size|height)\s*:\s*\d+%', context)
            has_bg = re.search(r'background\s*:\s*(?:var\(--color|oklch|hsl|rgb|#)', context)
            has_position = re.search(r'position\s*:\s*absolute', context)
            if narrow and tall and has_bg and has_position:
                violations.append({
                    'line': i,
                    'rule': 'accent-bar',
                    'detail': f'Pseudo-élément accent bar ({narrow.group(1)}px × height%) — la distinction vient du fond, pas d\'un trait sur le bord',
                })

    # Pattern 3: box-shadow inset Npx 0 0 <color> — contournement explicitement
    # cité par Impeccable BAN 1 (« Do not just swap to box-shadow inset »).
    # N=1..5 (gauche, N>0) ou N=-1..-5 (droite, N<0). Couleur non transparent/inherit/none.
    # Scan multi-ligne (DOTALL) car la valeur box-shadow peut s'étaler sur plusieurs lignes.
    for m in re.finditer(
        r'box-shadow\s*:\s*[^;]*?\binset\s+(-?[1-5])px\s+0(?:px)?\s+0(?:px)?\s+(?!transparent|inherit|none)',
        css, re.IGNORECASE | re.DOTALL
    ):
        n = int(m.group(1))
        side = 'gauche' if n > 0 else 'droite'
        line_num = css[:m.start()].count('\n') + 1
        violations.append({
            'line': line_num,
            'rule': 'accent-bar',
            'detail': f'box-shadow inset {n}px 0 0 (accent bar {side} via box-shadow) — Impeccable BAN 1 cite explicitement ce contournement',
        })

    return violations


def check_outline_focus_visible_pairing(css: str) -> list[dict]:
    """Toute règle outline:none/0 doit être compensée par un :focus-visible qui
    restaure un outline visible. Sinon = focus invisible au clavier (faille a11y).

    Sources:
      - Vercel Web Interface Guidelines (Focus States): « Never remove the
        focus outline without providing an equivalent visual indicator. »
      - GStack design-review item 5 (Interaction): « focus-visible ring present ».
    """
    violations = []
    # 1. Trouver les positions des occurrences outline: none / outline: 0
    none_occurrences = []
    for m in re.finditer(r'outline\s*:\s*(?:none|0)\b', css, re.IGNORECASE):
        line_num = css[:m.start()].count('\n') + 1
        none_occurrences.append(line_num)
    if not none_occurrences:
        return []
    # 2. Chercher au moins un bloc :focus-visible qui restaure un outline visible
    #    (width ≥ 1px, style solid/dashed/dotted/double, couleur non-transparent).
    has_restore = bool(re.search(
        r':focus-visible[^{}]*\{[^{}]*outline\s*:\s*[1-9]\d*px\s+(?:solid|dashed|dotted|double)\s+(?!transparent)',
        css, re.IGNORECASE | re.DOTALL
    ))
    if has_restore:
        return []  # appairage OK
    # 3. Sinon : violation a11y sur chaque outline: none/0
    for line in none_occurrences:
        violations.append({
            'line': line,
            'rule': 'outline-none-no-focus-visible',
            'detail': "outline: none/0 sans :focus-visible qui restaure un outline visible — focus invisible au clavier (faille a11y, Vercel Focus States + GStack)",
        })
    return violations


def check_overline_decorative_line(css: str) -> list[dict]:
    """No decorative ::before/::after line next to overlines."""
    violations = []
    lines = css.split('\n')
    for i, line in enumerate(lines, 1):
        if re.search(r'overline.*::(?:before|after)', line, re.IGNORECASE):
            # Look forward for a line pattern (inline-size/width + block-size/height 1-3px)
            context = '\n'.join(lines[i-1:min(i+8, len(lines))])
            has_line = (re.search(r'(?:inline-size|width)\s*:\s*\d+px', context) and
                       re.search(r'(?:block-size|height)\s*:\s*[1-3]px', context))
            if has_line:
                violations.append({
                    'line': i,
                    'rule': 'overline-decorative-line',
                    'detail': 'Trait décoratif ::before/::after sur overline — l\'overline se distingue par sa typographie seule',
                })
    return violations


def check_stroke_circles(content: str) -> list[dict]:
    """Detect SVG circles/ellipses with visible stroke and no fill.

    These produce thin-line amateur shapes (targets, dials, concentric rings).
    Elite sites use diffuse halos (radial-gradient) not stroked outlines.
    Exception: functional artifact elements (gauges, charts, sparklines).
    """
    violations = []
    # Find <circle> or <ellipse> with stroke and fill="none"
    for m in re.finditer(r'<(?:circle|ellipse)\b[^>]*>', content):
        tag = m.group(0)
        has_stroke = bool(re.search(r'stroke\s*=\s*"(?!none)', tag))
        has_no_fill = bool(re.search(r'fill\s*=\s*"none"', tag))
        if has_stroke and has_no_fill:
            # Skip functional artifact elements (NOT dial — stroked dial circles are amateur)
            start = max(0, m.start() - 400)
            context_before = content[start:m.start()]
            if re.search(r'gauge|chart|monitor|pulse|graph|spark|artifact-witness__inner|donut|progress',
                         context_before, re.IGNORECASE):
                continue
            violations.append({
                'line': 0,
                'rule': 'stroke-circle-amateur',
                'detail': (
                    'Cercle/ellipse SVG avec stroke sans fill (contour net) — '
                    'les formes décoratives élite sont des halos diffus '
                    '(radial-gradient), pas des contours fins. '
                    'Remplacer par un radial-gradient elliptique ou supprimer.'
                ),
            })
    return violations


def check_blend_mode_difference_on_text(content: str) -> list[dict]:
    """Detect mix-blend-mode: difference applied to text elements.

    difference on text over a dark gradient produces accidental outline/hollow
    letters or color clashes (cyan on warm gradient). The technique is valid
    on non-text layers but produces amateur results on titles/headings.
    """
    violations = []
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if re.search(r'mix-blend-mode\s*:\s*difference', line):
            # Look at surrounding context for text indicators
            context = '\n'.join(lines[max(0, i - 8):min(i + 5, len(lines))])
            is_text = bool(re.search(
                r'font-(?:family|size|weight)|text-transform|letter-spacing|line-height|\.title|\.quote|\.display|\.heading|h[1-6]|__title|__quote|__display|__manifesto',
                context, re.IGNORECASE
            ))
            if is_text:
                violations.append({
                    'line': i,
                    'rule': 'blend-mode-difference-text',
                    'detail': (
                        'mix-blend-mode: difference sur un élément textuel — '
                        'produit des lettres en contour/outline ou un clash chromatique '
                        '(cyan sur fond chaud). Retirer le blend-mode ou utiliser '
                        'soft-light/overlay à la place.'
                    ),
                })
    return violations


def check_figurative_svg(content: str) -> list[dict]:
    """Detect figurative SVG illustrations.

    Two detection strategies:
    1. Complex <path> with >20 SVG commands (drawing recognizable objects)
    2. <symbol> with >12 child elements (assembled illustrations from primitives)

    Allowed: simple decorative shapes (1-3 primitives per group).
    Exception: functional artifact elements (gauges, charts, monitors).
    """
    violations = []

    # Find all <symbol> blocks
    symbol_blocks = re.finditer(
        r'<symbol\s+id="([^"]*)"[^>]*>(.*?)</symbol>',
        content, re.DOTALL
    )
    for m in symbol_blocks:
        symbol_id = m.group(1)
        symbol_content = m.group(2)
        # Skip functional artifact elements
        if re.search(r'gauge|chart|monitor|pulse|dial|graph', symbol_id, re.IGNORECASE):
            continue

        # Strategy 1: complex <path>
        paths = re.findall(r'd="([^"]*)"', symbol_content)
        for path_d in paths:
            cmd_count = len(re.findall(r'[A-Za-z]', path_d))
            if cmd_count > 20:
                violations.append({
                    'line': 0,
                    'rule': 'figurative-svg',
                    'detail': (
                        f'SVG figuratif <symbol id="{symbol_id}"> contient un <path> '
                        f'avec {cmd_count} commandes (max 20). Les formes SVG '
                        f'décoratives doivent être des primitives géométriques simples.'
                    ),
                })
                break

        # Strategy 2: too many child elements = assembled illustration
        child_count = len(re.findall(
            r'<(?:circle|rect|ellipse|polygon|line|path|polyline)\b',
            symbol_content
        ))
        if child_count > 12:
            violations.append({
                'line': 0,
                'rule': 'figurative-svg',
                'detail': (
                    f'SVG figuratif <symbol id="{symbol_id}"> contient {child_count} '
                    f'éléments enfants (max 12). Un assemblage de primitives qui dessine '
                    f'un objet reconnaissable est une illustration, pas une forme abstraite.'
                ),
            })

    # Find standalone decorative <path> elements (not in artifact/defs context)
    standalone_paths = re.finditer(r'<path\s+[^>]*d="([^"]*)"', content)
    for m in standalone_paths:
        path_d = m.group(1)
        cmd_count = len(re.findall(r'[A-Za-z]', path_d))
        if cmd_count > 20:
            start = max(0, m.start() - 500)
            context_before = content[start:m.start()]
            if re.search(r'gauge|chart|monitor|pulse|dial|graph|svg-filters|defs|artifact|artefact',
                         context_before, re.IGNORECASE):
                continue
            violations.append({
                'line': 0,
                'rule': 'figurative-svg',
                'detail': (
                    f'<path> SVG complexe ({cmd_count} commandes, max 20) hors '
                    f'contexte fonctionnel — utiliser des primitives géométriques simples.'
                ),
            })

    return violations


def check_graphic_layer_presence(content: str, no_images: bool = False) -> list[dict]:
    """Check that the style-tile has the required decorative graphic layer.

    Mandatory base (always required):
      - Grain/texture (feTurbulence or noise)
      - Overlay atmosphérique (>=3 radial/conic-gradient)

    Additional categories (chosen by concept):
      1. SVG patterns/filters (<pattern>, <filter>)
      2. Pseudo-elements (::before/::after decorative, NOT on overlines)
      3. Shapes (circle, rect, polygon, decorative clip-path)

    With images: base + 1 additional = 3 total
    Without images: base + 1-2 additional = 3-4 total
    """
    violations = []
    lines = content.split('\n')

    # --- MANDATORY BASE ---

    # Base 1: Grain/texture with sufficient opacity
    has_grain = False
    grain_max_opacity = 0.0
    for i, line in enumerate(lines):
        if re.search(r'feTurbulence|grain|noise', line, re.IGNORECASE):
            context = '\n'.join(lines[max(0, i - 3):min(i + 8, len(lines))])
            # Check direct opacity AND @property initial-value
            opacity_m = re.search(r'(?:opacity|initial-value)\s*:\s*(0?\.\d+)', context)
            if opacity_m:
                val = float(opacity_m.group(1))
                grain_max_opacity = max(grain_max_opacity, val)
                if val >= 0.20:
                    has_grain = True
    if not has_grain:
        if grain_max_opacity > 0:
            violations.append({
                'line': 0,
                'rule': 'graphic-layer-grain-too-faint',
                'detail': (
                    f'Grain/texture présent mais opacity max = {grain_max_opacity:.0%} '
                    f'(minimum 20%). '
                    f'En dessous de 20%, le grain est invisible sur les rendus — augmenter l\'opacity.'
                ),
            })
        else:
            violations.append({
                'line': 0,
                'rule': 'graphic-layer-missing-grain',
                'detail': 'Grain/texture de surface ABSENT — obligatoire sur chaque style-tile.',
            })

    # Base 2: Overlay atmosphérique (>=3 radial/conic-gradient)
    gradient_count = len(re.findall(r'(?:radial|conic)-gradient\s*\(', content))
    has_overlay = gradient_count >= 3
    if not has_overlay:
        violations.append({
            'line': 0,
            'rule': 'graphic-layer-missing-overlay',
            'detail': (
                f'Overlay atmosphérique insuffisant — {gradient_count} radial/conic-gradient '
                f'détectés, minimum 3 requis pour la profondeur chromatique.'
            ),
        })

    # --- ADDITIONAL CATEGORIES ---
    additional_found = set()

    # Cat 1: SVG patterns/filters
    if (re.search(r'<pattern[\s>]', content) or
            re.search(r'<filter[\s>]', content)):
        additional_found.add('svg-pattern-filter')

    # Cat 2: Decorative pseudo-elements (not on overlines/labels/titles)
    for i, line in enumerate(lines):
        if re.search(r'::(?:before|after)', line):
            context = '\n'.join(lines[max(0, i - 5):min(i + 10, len(lines))])
            has_position = bool(re.search(r'position\s*:\s*absolute', context))
            has_content = bool(re.search(r'content\s*:', context))
            is_overline = bool(re.search(
                r'overline|\.label|\.tag|h[1-6]', context, re.IGNORECASE
            ))
            # Check opacity >= 8% (ignore elements below threshold)
            opacity_match = re.search(r'opacity\s*:\s*(0?\.\d+)', context)
            visible = True
            if opacity_match:
                val = float(opacity_match.group(1))
                if val < 0.08:
                    visible = False
            if has_position and has_content and not is_overline and visible:
                additional_found.add('pseudo-element-composition')
                break

    # Cat 3: SVG shapes or CSS decorative clip-path (opacity >= 8%)
    # Check SVG shapes
    shape_tags = re.finditer(r'<(?:circle|rect|polygon|ellipse)[\s>]', content)
    for m in shape_tags:
        context = content[max(0, m.start() - 200):min(m.end() + 200, len(content))]
        # Skip functional artifact elements
        if re.search(r'gauge|chart|monitor|pulse|dial|graph', context, re.IGNORECASE):
            continue
        # Check opacity
        opacity_m = re.search(r'opacity[=:]\s*["\']?(0?\.\d+)', context)
        if opacity_m and float(opacity_m.group(1)) < 0.08:
            continue
        additional_found.add('shapes')
        break
    # Also check CSS clip-path
    if 'shapes' not in additional_found:
        for i, line in enumerate(lines):
            if re.search(r'clip-path\s*:\s*(?:circle|ellipse|polygon|inset)', line):
                context = '\n'.join(lines[max(0, i - 5):i + 1])
                if not re.search(r'\b(?:voice|artifact|atmosphere|section)\b', context,
                                 re.IGNORECASE):
                    additional_found.add('shapes')
                    break

    additional_needed = 2 if no_images else 1
    additional_count = len(additional_found)

    if additional_count < additional_needed:
        mode = 'sans images' if no_images else 'avec images'
        found = ', '.join(sorted(additional_found)) if additional_found else 'aucune'
        violations.append({
            'line': 0,
            'rule': 'graphic-layer-insufficient',
            'detail': (
                f'Couche graphique supplémentaire insuffisante ({mode}) : '
                f'{additional_count}/{additional_needed} catégories additionnelles '
                f'détectées ({found}). Au-delà du socle (grain + overlay), '
                f'minimum {additional_needed} catégories parmi : svg-pattern-filter, '
                f'pseudo-element-composition, shapes.'
            ),
        })

    return violations


# ===========================================================================
# Vague 2 anti-slop — Checks d'interdictions visuelles (mode WARN)
#
# Ces checks détectent des anti-patterns binaires mais démarrent en WARN
# (informationnel) pour permettre une période d'observation. À promouvoir en
# FAIL (déplacer dans ALL_CHECKS) après 5 runs sans faux positif.
# Source : ref/plan-vague2-point1-regles-negatives-externes.md
# ===========================================================================


def warn_R082_gradient_text(content: str) -> list[dict]:
    """R-082 | Gradient text (background-clip:text + gradient)."""
    warnings = []
    # Find rule blocks combining background-clip:text and a gradient
    for m in re.finditer(r'\{([^{}]*)\}', content):
        block = m.group(1)
        has_clip = bool(re.search(r'background-clip\s*:\s*text|-webkit-background-clip\s*:\s*text', block))
        has_grad = bool(re.search(r'(linear|conic|radial)-gradient', block))
        if has_clip and has_grad:
            line_num = content[:m.start()].count('\n') + 1
            warnings.append({
                'line': line_num,
                'rule': 'R-082-gradient-text',
                'detail': 'background-clip:text + gradient — préférer une couleur unie',
            })
    return warnings


def warn_R108_emojis(content: str) -> list[dict]:
    """R-108 | NO emojis dans markup/code (hors <svg>)."""
    warnings = []
    cleaned = re.sub(r'<svg\b.*?</svg>', '', content, flags=re.DOTALL | re.IGNORECASE)
    emoji_pattern = re.compile(
        r'[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F600-\U0001F64F]'
    )
    matches = list(emoji_pattern.finditer(cleaned))
    if matches:
        # Use line of first occurrence
        first = matches[0]
        line_num = cleaned[:first.start()].count('\n') + 1
        unique = sorted({m.group(0) for m in matches})
        warnings.append({
            'line': line_num,
            'rule': 'R-108-emojis',
            'detail': f'{len(matches)} emoji(s) détecté(s) ({" ".join(unique[:8])}) — préférer SVG/icônes maîtrisés',
        })
    return warnings


def warn_R109_lucide_default(content: str) -> list[dict]:
    """R-109 | NO Lucide icon library default."""
    warnings = []
    if re.search(r'(from\s+["\']lucide|<i\s+[^>]*class[^>]*lucide|lucide-icon)', content, re.IGNORECASE):
        warnings.append({
            'line': 0,
            'rule': 'R-109-lucide-default',
            'detail': 'Lucide détecté — devenu cliché, préférer icônes custom ou Phosphor/Iconoir',
        })
    return warnings


def warn_R114_custom_cursors(content: str) -> list[dict]:
    """R-114 | NO custom mouse cursors."""
    warnings = []
    for m in re.finditer(r'cursor\s*:\s*url\(', content):
        line_num = content[:m.start()].count('\n') + 1
        warnings.append({
            'line': line_num,
            'rule': 'R-114-custom-cursor',
            'detail': 'cursor: url(...) — les curseurs custom dégradent l\'UX',
        })
    return warnings


WARN_CHECKS_VAGUE2 = [
    warn_R082_gradient_text,
    warn_R108_emojis,
    warn_R109_lucide_default,
    warn_R114_custom_cursors,
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

ALL_CHECKS = [
    check_hover_translateY,
    check_hover_translateX,
    check_hover_scale_excessive,
    check_infinite_animations,
    check_glow_shadows,
    check_text_shadow_glow,
    check_section_clip_path,
    check_staggered_fadeup,
    check_backdrop_blur_excessive,
    check_letter_spacing_hover,
    check_underline_scalex,
    check_accent_bar,
    check_outline_focus_visible_pairing,
    check_overline_decorative_line,
    check_stroke_circles,
    check_blend_mode_difference_on_text,
    check_figurative_svg,
]


def main():
    # Parse arguments
    no_images = False
    json_output = None
    args = sys.argv[1:]
    if '--no-images' in args:
        no_images = True
        args.remove('--no-images')
    if '--json-output' in args:
        idx = args.index('--json-output')
        if idx + 1 >= len(args):
            print("Erreur: --json-output requiert un chemin")
            sys.exit(2)
        json_output = args[idx + 1]
        del args[idx:idx + 2]

    if len(args) < 1:
        print("Usage: python3 phase4-blacklist-gate.py <path/to/style-tile.html> [--no-images] [--json-output PATH]")
        sys.exit(2)

    filepath = args[0]

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erreur: fichier introuvable — {filepath}")
        sys.exit(2)

    # Run all blacklist checks (negative — detect what must NOT be there)
    all_violations = []
    for check_fn in ALL_CHECKS:
        all_violations.extend(check_fn(content))

    # Run graphic layer check (positive — detect what MUST be there)
    graphic_violations = check_graphic_layer_presence(content, no_images=no_images)
    all_violations.extend(graphic_violations)

    # Run Vague 2 WARN checks (informationnel, ne bloque pas)
    all_warnings = []
    for warn_fn in WARN_CHECKS_VAGUE2:
        try:
            all_warnings.extend(warn_fn(content))
        except Exception as e:
            all_warnings.append({
                'line': 0,
                'rule': f'{warn_fn.__name__}-error',
                'detail': f'Check a échoué: {type(e).__name__}: {str(e)[:100]}',
            })

    # Sort by line number
    all_violations.sort(key=lambda v: v['line'])
    all_warnings.sort(key=lambda v: v['line'])

    # Optional JSON output (compat ascendante : le stdout ci-dessous reste inchangé)
    if json_output:
        verdict = "PASS" if not all_violations else "FAIL"
        html_sha256 = hashlib.sha256(content.encode('utf-8')).hexdigest()
        payload = {
            "gate": "phase4-blacklist-gate",
            "html_audited": filepath,
            "html_sha256": html_sha256,
            "timestamp": datetime.datetime.now().isoformat(timespec='seconds'),
            "verdict": verdict,
            "fails": [
                {"check": v["rule"], "rule_id": v["rule"], "line": v["line"],
                 "snippet": "", "message": v["detail"]}
                for v in all_violations
            ],
            "warns": [
                {"check": w["rule"], "rule_id": w["rule"], "line": w["line"],
                 "snippet": "", "message": w["detail"]}
                for w in all_warnings
            ],
        }
        try:
            with open(json_output, 'w', encoding='utf-8') as jf:
                json.dump(payload, jf, indent=2, ensure_ascii=False)
        except Exception as exc:
            print(f"Avertissement: échec écriture JSON {json_output}: {exc}")

    # Output
    filename = filepath.rsplit('/', 1)[-1] if '/' in filepath else filepath
    print(f"\n=== PHASE 4 BLACKLIST GATE ===")
    print(f"File: {filename}")
    if no_images:
        print(f"Mode: --no-images (seuil couche graphique = 4)")
    print()

    # Print Vague 2 warnings (informationnel, ne change pas le verdict)
    def print_warnings_section():
        if not all_warnings:
            return
        warn_by_rule: dict[str, list] = {}
        for w in all_warnings:
            warn_by_rule.setdefault(w['rule'], []).append(w)
        print(f"--- VAGUE 2 ANTI-SLOP (WARN, informationnel) ---")
        for rule, instances in sorted(warn_by_rule.items()):
            print(f"  [WARN] {rule} ({len(instances)}x)")
            for inst in instances[:3]:
                line_info = f"Ligne {inst['line']}: " if inst['line'] > 0 else ""
                print(f"     {line_info}{inst['detail']}")
            if len(instances) > 3:
                print(f"     ... et {len(instances) - 3} autre(s)")
        print()

    if not all_violations:
        print_warnings_section()
        print("VERDICT: PASS — aucun anti-pattern daté détecté")
        print("Le style-tile utilise des techniques CSS modernes.")
        if all_warnings:
            print(f"({len(all_warnings)} warning(s) Vague 2 informationnel(s) — voir ci-dessus)")
        sys.exit(0)

    # Group by rule
    by_rule: dict[str, list] = {}
    for v in all_violations:
        by_rule.setdefault(v['rule'], []).append(v)

    print(f"[FAIL] {len(all_violations)} violation(s) dans {len(by_rule)} catégorie(s) :\n")

    for rule, instances in sorted(by_rule.items()):
        print(f"  ❌ {rule} ({len(instances)}x)")
        for inst in instances[:3]:
            line_info = f"Ligne {inst['line']}: " if inst['line'] > 0 else ""
            print(f"     {line_info}{inst['detail']}")
        if len(instances) > 3:
            print(f"     ... et {len(instances) - 3} autre(s)")
        print()

    print_warnings_section()

    print("VERDICT: FAIL — corrections requises avant livraison")
    print("Le subagent Phase 4 doit corriger chaque violation listée ci-dessus.")
    if all_warnings:
        print(f"({len(all_warnings)} warning(s) Vague 2 additionnel(s) — informationnel)")

    sys.exit(1)


if __name__ == '__main__':
    main()
