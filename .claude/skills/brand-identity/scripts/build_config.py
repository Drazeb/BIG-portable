#!/usr/bin/env python3
"""
build_config.py — Assemble le .tmp-grid-visual-config.json pour grid-visual.mjs.

Modèle binaire exhaustif : validé (par territoire × aptitude) + exclu. Pas de réserve.
- Swatches peuplés via match_hexes.
- Tags [SLOP_RISQUE] / [SECTORIEL] posés MÉCANIQUEMENT (tags.py), sur validé ET exclu.

Usage :
  python3 build_config.py --grid <01-grid.md> --output <json> --brand "<Nom>"
                          [--cursor-b N] [--catalogue <path>] [--ventre-mou <path>]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_v2 as gv       # noqa: E402  (parse_grid)
import match_hexes as mh   # noqa: E402
import tags as tg          # noqa: E402

ROLE_ORDER = ['Principal', 'Secondaire', 'Tertiaire']
CURSOR_LABELS = {1: 'Mimétisme', 2: 'Distinction', 3: 'ZAG'}


def parse_territory_title(title: str):
    role_m = re.match(r'\s*(principal|secondaire|tertiaire)', title, re.I)
    role = role_m.group(1).capitalize() if role_m else title.split()[0].capitalize()
    name_m = re.search(r'[«"“]([^»"”]+)[»"”]', title)
    name = name_m.group(1).strip() if name_m else title
    kw_m = re.search(r'\(([^)]*)\)\s*$', title)
    kws = [k.strip() for k in kw_m.group(1).split(',')] if kw_m else []
    return role, name, kws


def extract_keywords_line(content: str):
    m = re.search(r'\*\*Mots-clés\s+dominants\s+analysés\*\*\s*:?\s*(.+)', content, re.I)
    return [k.strip() for k in re.split(r'[,;]', m.group(1)) if k.strip()] if m else []


def source_str(base: str, tags_list: list[str]) -> str:
    return (base + ' ' + ' '.join(tags_list)).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--grid', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--brand', required=True)
    ap.add_argument('--cursor-b', type=int, default=2)
    ap.add_argument('--catalogue', default=str(Path(__file__).resolve().parent.parent / 'ref' / 'chromatic-spectrum-catalog.md'))
    ap.add_argument('--ventre-mou', default=None)
    args = ap.parse_args()

    content = Path(args.grid).read_text(encoding='utf-8')
    parsed = gv.parse_grid(content)
    catalogue = mh.load_catalogue(Path(args.catalogue))

    slop_set = tg.load_slop_risk(Path(args.catalogue))
    sectoral = []
    if args.ventre_mou and Path(args.ventre_mou).exists():
        sectoral = tg.load_sectoral_families(Path(args.ventre_mou).read_text(encoding='utf-8'))

    def tags_for(name):
        return tg.tags_for(name, catalogue, slop_set, sectoral)

    territories_header, grid = {}, []
    for i, t in enumerate(parsed['territories']):
        role, name, kws = parse_territory_title(t['name'])
        key = role.lower()
        if key in ('principal', 'secondaire', 'tertiaire'):
            territories_header[key] = {'name': name, 'keywords': kws}
        gammes = []
        for r in t['rows']:
            hexes, _, _ = mh.match(r['gamut'], catalogue)
            gammes.append({'gamut': r['gamut'], 'aptitude': r['aptitude'],
                           'keyword': r.get('keyword', ''),
                           'source': source_str('TERRITOIRE', tags_for(r['gamut'])),
                           'swatches': hexes})
        grid.append({'role': role if role in ROLE_ORDER else (ROLE_ORDER[i] if i < 3 else role),
                     'name': name, 'gammes': gammes})

    excluded = []
    for r in parsed['excluded_rows']:
        hexes, _, _ = mh.match(r['gamut'], catalogue)
        excluded.append({'gamut': r['gamut'], 'reason': r.get('reason', ''),
                         'source': source_str('', tags_for(r['gamut'])), 'swatches': hexes})

    config = {
        'brandName': args.brand, 'cursorB': args.cursor_b,
        'cursorBLabel': CURSOR_LABELS.get(args.cursor_b, '?'),
        'territories': territories_header, 'ventreMouChromatique': [],
        'analyzedKeywords': extract_keywords_line(content),
        'grid': grid, 'excluded': excluded,
    }
    Path(args.output).write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8')
    nslop = sum(1 for g in grid for ga in g['gammes'] if '[SLOP_RISQUE]' in ga['source']) + \
        sum(1 for e in excluded if '[SLOP_RISQUE]' in e['source'])
    nsect = sum(1 for e in excluded if '[SECTORIEL]' in e['source'])
    print(f"[OK] config écrit : {args.output}")
    print(f"     validées: {sum(len(g['gammes']) for g in grid)} · exclues: {len(excluded)}")
    print(f"     tags posés mécaniquement — [SLOP_RISQUE]: {nslop} · [SECTORIEL]: {nsect}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
