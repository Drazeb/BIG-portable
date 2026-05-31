#!/usr/bin/env python3
"""
render_directive.py — Génère la directive Ventre Mou chromatique pour le composeur de
palette ({vm_palette_directive}), selon le curseur B. Clone fidèle de la logique BIG
(SKILL.md L1409-1425) — INCHANGÉE par le passage aux buckets.

- B=1 (Mimétisme)   : les gammes [SECTORIEL] sont libres pour n'importe quel rôle.
- B=2 (Distinction) : CAP — max 1 dominante (Primary OU Secondary) en gamme [SECTORIEL].
- B=3 (ZAG)         : sectoriel déjà exclu en amont ; éloignement actif.

Usage :
  python3 render_directive.py --cursor-b {1|2|3} --out <vm-palette-directive.md>
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

B1 = """## GAMMES SECTORIELLES (information)
Certaines gammes des buckets sont taguées [SECTORIEL] — ce sont les conventions chromatiques du secteur. Tu peux librement les utiliser pour n'importe quel rôle. Aucune contrainte d'évitement."""

B2 = """## CONTRAINTE SECTORIELLE — 1 DOMINANTE MAX
Certaines gammes du bucket DOMINANTE sont taguées [SECTORIEL]. Règle : tu peux placer AU MAXIMUM 1 dominante (Primary OU Secondary) dans une gamme [SECTORIEL]. L'autre dominante DOIT être dans une gamme non-sectorielle. L'accent est libre."""

B3 = """## CONTRE-PIED CHROMATIQUE — ÉLOIGNEMENT ACTIF
Les gammes sectorielles ont été exclues par le routeur chromatique (absentes des buckets). En complément, oriente ACTIVEMENT tes choix vers des familles chromatiquement opposées aux conventions du secteur. L'objectif n'est pas juste d'éviter — c'est de démontrer le contre-pied."""

TEMPLATES = {1: B1, 2: B2, 3: B3}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--cursor-b', type=int, choices=[1, 2, 3], required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    Path(args.out).write_text(TEMPLATES[args.cursor_b] + '\n', encoding='utf-8')
    print(f"[OK] directive palette B={args.cursor_b} écrite : {args.out}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
