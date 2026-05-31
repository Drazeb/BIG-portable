#!/usr/bin/env python3
"""
enforce_filters.py — Applique DÉTERMINISTIQUEMENT les filtres durs sur la grille du routeur.

Le routeur (LLM) rationalise parfois une gamme sectorielle ou à contre-température en
validé (ex: bleu sectoriel rebaptisé « encre de plan »). Ce script ne lui fait pas
confiance : il DÉPLACE mécaniquement vers les exclues toute gamme validée qui est
  - sectorielle (B=3, listée dans la directive Ventre Mou), OU
  - à contre-température en dominante/accent (froide quand chaud, et inversement).
Puis re-sérialise la grille. La primauté sectoriel/température n'est plus négociable.

Usage :
  python3 enforce_filters.py --grid <01-grid.md> --catalogue <p> --ventre-mou <p> --temperature chaud|froid
  (écrit la grille nettoyée en place ; --out <p> pour écrire ailleurs)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_v2 as gv
import match_hexes as mh
import tags as tg
import derive_aptitude as da

ACCENT_FREE = "**Accent libre** : toute gamme, y compris exclue, reste mobilisable en accent si le concept le justifie."


def violators(parsed, sectoral, catalogue, temperature, cursor_b=3, temp_filter='on'):
    """Filtres durs déterministes, curseur-aware.
    Volet sectoriel (toujours actif) :
    - B=3 : retire le sectoriel (directive). B=1/B=2 : pas de retrait sectoriel dur.

    Volet température, selon `temp_filter` :
    - 'on'      : legacy — retire TOUTE gamme à contre-brief, quelle que soit l'aptitude
                  ou l'intensité (amputait les territoires calmes-bleus).
    - 'off'     : n'applique plus aucun filtre température (le jugement par territoire +
                  le curseur secteur portent la direction chromatique).
    - 'minimal' : filet — retire UNIQUEMENT les gammes à contre-brief qui sont (a) en
                  dominante/accent ET (b) franchement vives (intensité ≥ seuil). Les bases
                  froides et les bleus désaturés (encre, pétrole, ardoise) sont conservés.
    B=1 mimétisme : le sectoriel reste exempté du volet température dans tous les modes."""
    sect_tok = [mh.tokenize(s) for s in sectoral]
    temp = (temperature or '').strip().lower()
    opp = 'cold' if temp == 'chaud' else ('warm' if temp == 'froid' else None)
    out = {}  # id(row) -> reason
    for t in parsed['territories']:
        for r in t['rows']:
            hexes, _, matched = mh.match(r['gamut'], catalogue)
            is_sect = bool(matched) and (matched in sectoral or any(st and st <= mh.tokenize(matched) for st in sect_tok))
            reasons = []
            if cursor_b == 3 and is_sect:
                reasons.append('sectoriel B=3 (directive)')
            if temp_filter != 'off' and opp and hexes and da.warmth(hexes) == opp:
                contra = True
                if temp_filter == 'minimal':
                    # seul un contre-brief FRANCHEMENT VIF en dominante/accent est retiré
                    if r['aptitude'] not in ('dominante', 'accent'):
                        contra = False
                    else:
                        s, l = da.avg_sl(hexes)
                        contra = da.intensity(s, l) >= da.CONTRA_TEMP_VIVID_INTENSITY
                if contra:
                    if cursor_b == 1 and is_sect:
                        pass  # B=1 mimétisme : sectoriel exempté de la température (inclusion prime)
                    else:
                        label = 'contre-température vive' if temp_filter == 'minimal' else 'contre-température'
                        reasons.append(f'{label} ({opp} vs {temp})')
            if reasons:
                out[id(r)] = ' + '.join(reasons)
    return out


def serialize(parsed, content, moved):
    kw = re.search(r'(\*\*Mots-clés\s+dominants\s+analysés\*\*[^\n]*)', content)
    lines = ["## Grille chromatique (routeur v2)", "", kw.group(1) if kw else "**Mots-clés dominants analysés** : —", ""]
    for t in parsed['territories']:
        lines += [f"### {t['name']}", "", "| Gamme | Aptitude | Mot-clé servi |", "|-------|----------|---------------|"]
        for r in t['rows']:
            if id(r) in moved:
                continue
            lines.append(f"| {r['gamut']} | {r['aptitude']} | {r.get('keyword','')} |")
        lines.append("")
    lines += ["### Gammes exclues", "", "| Gamme | Raison |", "|-------|--------|"]
    for r in parsed['excluded_rows']:
        lines.append(f"| {r['gamut']} | {r.get('reason','')} |")
    for gamut, reason in moved.values():
        lines.append(f"| {gamut} | DÉPLACÉ AUTO — {reason} (la primauté prime sur la justification par-territoire) |")
    lines += ["", ACCENT_FREE, ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--grid', required=True)
    ap.add_argument('--catalogue', default=str(Path(__file__).resolve().parent.parent / 'ref' / 'chromatic-spectrum-catalog.md'))
    ap.add_argument('--ventre-mou')
    ap.add_argument('--temperature')
    ap.add_argument('--cursor-b', type=int, default=3)
    ap.add_argument('--temp-filter', choices=['on', 'off', 'minimal'], default='minimal',
                    help="minimal=DÉFAUT sanctuarisé (dominante/accent vifs uniquement) · "
                         "on=legacy (toutes aptitudes, amputait les territoires calmes) · "
                         "off=aucun filtre température")
    ap.add_argument('--out')
    args = ap.parse_args()

    content = Path(args.grid).read_text(encoding='utf-8')
    parsed = gv.parse_grid(content)
    catalogue = mh.load_catalogue(Path(args.catalogue))
    sectoral = tg.load_sectoral_families(Path(args.ventre_mou).read_text(encoding='utf-8')) \
        if args.ventre_mou and Path(args.ventre_mou).exists() else []

    vio = violators(parsed, sectoral, catalogue, args.temperature, args.cursor_b,
                    temp_filter=args.temp_filter)
    moved = {}  # id -> (gamut, reason)  (dédup par nom de gamme côté exclu)
    for t in parsed['territories']:
        for r in t['rows']:
            if id(r) in vio:
                moved[id(r)] = (r['gamut'], vio[id(r)])

    new_content = serialize(parsed, content, moved)
    out = Path(args.out) if args.out else Path(args.grid)
    out.write_text(new_content, encoding='utf-8')

    if moved:
        print(f"[ENFORCE] {len(moved)} gamme(s) validée(s) déplacée(s) vers exclues :")
        for gamut, reason in moved.values():
            print(f"  → {gamut[:50]} ({reason})")
    else:
        print("[ENFORCE] aucune violation — grille déjà conforme.")
    # garde-fous post-déplacement
    for t in parsed['territories']:
        remaining = sum(1 for r in t['rows'] if id(r) not in moved)
        if remaining < 3:
            print(f"  ⚠ '{t['name'][:30]}' tombe à {remaining} gammes (<3) après déplacement — re-dispatch conseillé.")
    acc = sum(1 for t in parsed['territories'] for r in t['rows'] if r['aptitude'] == 'accent' and id(r) not in moved)
    if acc < 2:
        print(f"  ⚠ {acc} accent(s) restant(s) (<2) après déplacement.")
    print(f"[OK] grille écrite : {out}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
