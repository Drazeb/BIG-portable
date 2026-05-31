#!/usr/bin/env python3
"""
project_buckets.py — Projette la grille du routeur chromatique v2 (territoire × aptitude)
en 3 BUCKETS d'aptitude consommables par le composeur de palette v2.

Pourquoi : le composeur ne doit PAS voir les territoires (anti-contamination — règle
volontaire de BIG : le choix chromatique vient du concept, pas des territoires). Mais il
DOIT voir l'aptitude (base/dominante/accent) pour piocher par rôle, ET les tags
[SECTORIEL]/[SLOP_RISQUE] pour le cap B=2 et la vigilance slop.

Ce que fait ce script :
- parse la grille (réutilise gate_v2.parse_grid)
- dédup sur la FAMILLE catalogue (via match_hexes) — une même famille vue sous 2 territoires
  avec 2 reformulations = 1 seule entrée
- résout l'aptitude quand elle diverge selon territoire : INTENSITÉ MAX GAGNE
  (accent > dominante > base) — on préserve le potentiel énergétique (philosophie router)
- RETIRE l'axe territoire + le mot-clé-servi (anti-contamination)
- CONSERVE les tags [SECTORIEL]/[SLOP_RISQUE], posés MÉCANIQUEMENT par tags.py (ils ne sont
  PAS fiables dans le texte des lignes validées de la grille → on les réapplique)

Usage :
  python3 project_buckets.py --grid <01-grid.md> --output <01-buckets.md>
                             [--catalogue <p>] [--ventre-mou <p>]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_v2 as gv       # noqa: E402  (parse_grid)
import match_hexes as mh   # noqa: E402
import tags as tg          # noqa: E402

APT_RANK = {'base': 1, 'dominante': 2, 'accent': 3}
RANK_APT = {1: 'base', 2: 'dominante', 3: 'accent'}
# Seuils de richesse minimale (sous lesquels on émet un WARN, pas un FAIL)
MIN_BUCKET = {'dominante': 2, 'accent': 3, 'base': 3}


def _norm(s: str) -> str:
    return re.sub(r'\s+', ' ', s.strip().lower())


def _apt(raw: str) -> str:
    """Normalise l'aptitude déclarée dans la grille → base|dominante|accent."""
    r = (raw or '').strip().lower()
    if r.startswith('accent'):
        return 'accent'
    if r.startswith('domin'):
        return 'dominante'
    return 'base'


def build_buckets(parsed, catalogue, slop_set, sectoral):
    """Renvoie {'dominante': [...], 'accent': [...], 'base': [...]}.
    Chaque entrée : {'name', 'tags' (list), 'also' (set d'autres aptitudes vues)}."""
    # clé de dédup = famille catalogue matchée (robuste aux reformulations) ; repli = nom normalisé
    groups = {}  # key -> {'best_rank', 'name', 'apts': set}
    for t in parsed['territories']:
        for r in t['rows']:
            name = r['gamut']
            apt = _apt(r.get('aptitude', ''))
            rank = APT_RANK[apt]
            _, _, matched = mh.match(name, catalogue)
            key = _norm(matched) if matched else _norm(name)
            g = groups.get(key)
            if g is None:
                groups[key] = {'best_rank': rank, 'name': name, 'apts': {apt}, 'family': matched or ''}
            else:
                g['apts'].add(apt)
                if rank > g['best_rank']:
                    g['best_rank'] = rank
                    g['name'] = name  # le nom de l'occurrence à l'aptitude gagnante

    buckets = {'dominante': [], 'accent': [], 'base': []}
    for g in groups.values():
        winning = RANK_APT[g['best_rank']]
        others = sorted(a for a in g['apts'] if a != winning)
        buckets[winning].append({
            'name': g['name'],
            'family': g['family'],
            'tags': tg.tags_for(g['name'], catalogue, slop_set, sectoral),
            'also': others,
        })
    return buckets


def render_markdown(buckets) -> str:
    head = {
        'dominante': '### Bucket DOMINANTE (→ Primary, Secondary)',
        'accent': '### Bucket ACCENT (→ Accent ; reste LIBRE — toute gamme si le concept le justifie)',
        'base': '### Bucket BASE (→ Bg dark, Bg light, Text primary, Text secondary — orientation, hex teinté librement)',
    }
    lines = ['## Buckets chromatiques (projetés depuis la grille routeur v2)', '',
             'Territoire retiré (anti-contamination). Tags conservés. Une gamme = un seul bucket '
             '(aptitude la plus intense vue sur la grille).', '']
    for b in ('dominante', 'accent', 'base'):
        lines.append(head[b])
        lines.append('')
        if not buckets[b]:
            lines.append('- (aucune)')
        for e in buckets[b]:
            suffix = (' ' + ' '.join(e['tags'])) if e['tags'] else ''
            also = f"  _(aussi vue en {', '.join(e['also'])})_" if e['also'] else ''
            lines.append(f"- {e['name']}{suffix}{also}")
        lines.append('')
    lines.append('**Tags** : `[SECTORIEL]` = convention secteur (cap B=2 : max 1 dominante sectorielle) · '
                 '`[SLOP_RISQUE]` = zone training-defaults, choisir en bord de gamme.')
    lines.append('')
    return '\n'.join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--grid', required=True)
    ap.add_argument('--output', required=True)
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

    buckets = build_buckets(parsed, catalogue, slop_set, sectoral)
    Path(args.output).write_text(render_markdown(buckets), encoding='utf-8')

    counts = {b: len(buckets[b]) for b in buckets}
    nsect = sum(1 for b in buckets.values() for e in b if '[SECTORIEL]' in e['tags'])
    nslop = sum(1 for b in buckets.values() for e in b if '[SLOP_RISQUE]' in e['tags'])
    print(f"[OK] buckets écrits : {args.output}")
    print(f"     dominante: {counts['dominante']} · accent: {counts['accent']} · base: {counts['base']} "
          f"· [SECTORIEL]: {nsect} · [SLOP_RISQUE]: {nslop}")
    for b, mn in MIN_BUCKET.items():
        if counts[b] < mn:
            print(f"  ⚠ bucket {b} pauvre ({counts[b]} < {mn}) — re-router conseillé ou accepter avec ⚠", file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
