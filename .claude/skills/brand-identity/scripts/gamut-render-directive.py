#!/usr/bin/env python3
"""
render_directive.py — Génère DÉTERMINISTIQUEMENT la directive sectorielle du routeur
chromatique selon le curseur B, en clonant les 3 templates de BIG (SKILL.md
{ventre_mou_chromatique_section}). Plus de rédaction à la main = plus de règle oubliée.

Le curseur B → quelle directive (le QUOI). La liste des familles sectorielles → le QUI
(propriété du brief/secteur). On ne fait que combiner les deux.

Usage :
  python3 render_directive.py --cursor-b {1|2|3} --familles "Fam A ; Fam B ; ..." [--out <path>]
  (ou --familles-file <path> contenant une ligne « Familles catalogue concernées : ... »)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Templates CLONÉS de BIG SKILL.md (routeur chromatique 3B-0a). Ne pas paraphraser.
TEMPLATES = {
    1: """## GAMMES CHROMATIQUES SECTORIELLES — INCLUSION OBLIGATOIRE (curseur B=1, Mimétisme)
Ces gammes chromatiques sont les conventions du secteur. Tu DOIS les inclure dans les gammes validées, même si ton analyse des territoires ne les aurait pas retenues. (Le sectoriel s'AJOUTE aux territoires — il ne remplace pas : tu gardes aussi tes gammes non-sectorielles.) Tagge-les [SECTORIEL].

Familles catalogue concernées : {familles}""",
    2: """## GAMMES CHROMATIQUES SECTORIELLES — INCLUSION PAR DÉFAUT (curseur B=2, Distinction)
Ces gammes chromatiques sont les conventions du secteur. Tu DOIS les inclure dans les gammes validées SAUF si ton analyse des territoires les trouve ACTIVEMENT CONTRADICTOIRES avec l'univers évoqué (pas juste « pas idéal » — il faut une contradiction franche et explicite ; une température opposée compte comme contradiction franche). En cas de doute, INCLURE. Tagge-les [SECTORIEL].

Familles catalogue concernées : {familles}""",
    3: """## GAMMES CHROMATIQUES SECTORIELLES — EXCLUSION OBLIGATOIRE (curseur B=3, ZAG)
Ces gammes chromatiques sont le Ventre Mou du secteur. Tu DOIS les exclure des gammes validées, même si ton analyse des territoires les aurait retenues. Le contre-pied B=3 = « aller AILLEURS que le secteur », PAS « éteindre les couleurs ».

Familles catalogue concernées : {familles}""",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--cursor-b', type=int, required=True, choices=[1, 2, 3])
    ap.add_argument('--familles', help='Familles séparées par « ; »')
    ap.add_argument('--familles-file', help='Fichier contenant « Familles catalogue concernées : ... »')
    ap.add_argument('--out')
    args = ap.parse_args()

    familles = args.familles
    if not familles and args.familles_file and Path(args.familles_file).exists():
        m = re.search(r'Familles\s+catalogue\s+concernées\s*:?\s*(.+)', Path(args.familles_file).read_text(encoding='utf-8'), re.I)
        familles = m.group(1).strip() if m else ''
    if not familles:
        print('[ERROR] fournir --familles ou --familles-file', file=sys.stderr)
        return 1

    out_text = TEMPLATES[args.cursor_b].format(familles=familles)
    if args.out:
        Path(args.out).write_text(out_text + '\n', encoding='utf-8')
        print(f"[OK] directive B={args.cursor_b} écrite : {args.out}")
    else:
        print(out_text)
    return 0


if __name__ == '__main__':
    sys.exit(main())
