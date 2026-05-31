#!/usr/bin/env python3
"""
divergence_gate.py — Garde-fou MÉCANIQUE d'unicité inter-variantes (le « finisseur »).

POURQUOI : la consigne de divergence (render_divergence.py) dégrossit massivement, mais
elle a un plancher — un LLM qui raisonne en concepts recopie parfois un hex à l'identique
malgré l'instruction « ne pas reproduire » (observé : Secondary #2C5340 dupliqué V3=V5).
Aucune consigne ne garantit l'unicité ; seul un gate qui MESURE le rendu le peut.

Ce gate compare la variante courante à TOUTES les précédentes, sur les 3 rôles porteurs
d'identité (Primary, Secondary, Accent), en distance perceptuelle ΔE (Lab). Si un rôle
est trop proche du même rôle d'une variante précédente → FAIL (re-dispatch).

Seuil bas par design : on ne flague que les VRAIS jumeaux (copie / quasi-copie), pas la
proximité légitime d'un terrain étroit. Défaut ΔE < 10. (ΔE 0 = hex identique ; ~2-3 =
imperceptible ; ~10 = différence faible mais visible côte à côte.)

Usage :
  python3 divergence_gate.py <variante_courante.md> --prev <V1.md> [<V2.md> …] \
      [--threshold 10] [--json-output]
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROLES = ['Primary', 'Secondary', 'Accent']


def parse_role_hex(content: str, role: str) -> str:
    m = re.search(r'\|\s*' + re.escape(role) + r'\s*\|[^|]*\|\s*`?(#[0-9a-fA-F]{6})`?', content, re.I)
    return m.group(1) if m else ''


def _srgb_lin(c: float) -> float:
    c /= 255
    return ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92


def _lab(hex_str: str):
    h = hex_str.lstrip('#')
    rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (_srgb_lin(x) for x in rgb)
    X = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047
    Y = r * 0.2126 + g * 0.7152 + b * 0.0722
    Z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(X), f(Y), f(Z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e(h1: str, h2: str) -> float:
    a, b = _lab(h1), _lab(h2)
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('palette')
    ap.add_argument('--prev', nargs='*', default=[], help='Variantes précédentes (V1, V2, …)')
    ap.add_argument('--threshold', type=float, default=10.0, help='ΔE en dessous duquel deux rôles sont jumeaux')
    ap.add_argument('--json-output', action='store_true')
    args = ap.parse_args()

    cur = Path(args.palette)
    if not cur.exists():
        print(f"Introuvable : {cur}", file=sys.stderr)
        return 2
    cur_content = cur.read_text(encoding='utf-8')
    cur_hex = {r: parse_role_hex(cur_content, r) for r in ROLES}

    violations = []
    for idx, p in enumerate(args.prev, start=1):
        pp = Path(p)
        if not pp.exists():
            continue
        prev_hex = {r: parse_role_hex(pp.read_text(encoding='utf-8'), r) for r in ROLES}
        for r in ROLES:
            if cur_hex[r] and prev_hex.get(r):
                d = delta_e(cur_hex[r], prev_hex[r])
                if d < args.threshold:
                    violations.append({
                        'check': 'role_duplicate',
                        'severity': 'FAIL',
                        'role': r,
                        'detail': (f"{r} {cur_hex[r]} ≈ {r} {prev_hex[r]} de la variante V{idx} "
                                   f"(ΔE {d:.1f} < {args.threshold:g}). Jumeau perceptuel — choisis un hex "
                                   f"nettement distinct pour ce rôle.")
                    })

    verdict = 'FAIL' if violations else 'PASS'
    result = {'verdict': verdict, 'file': str(cur), 'threshold': args.threshold, 'violations': violations}
    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== DIVERGENCE GATE — {cur.name} === {verdict}")
        for v in violations:
            print(f"  [FAIL] {v['role']}: {v['detail']}")
    return 1 if violations else 0


if __name__ == '__main__':
    sys.exit(main())
