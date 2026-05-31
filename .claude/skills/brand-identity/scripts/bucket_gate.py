#!/usr/bin/env python3
"""
bucket_gate.py — Gate déterministe propre au composeur v2 (complète palette_gate.py).

Vérifie ce que le composeur peut violer silencieusement, en reliant les hex de la palette
aux familles du catalogue (nearest family) puis aux buckets reconstruits depuis la grille :

  - dominantes_in_bucket : Primary ET Secondary doivent appartenir à une famille du
    bucket DOMINANTE (mapping rôle→bucket du régime hybride). FAIL sinon.
  - sectoral_cap_b2 : si cursor_b==2, max 1 dominante (Primary/Secondary) en famille
    [SECTORIEL]. FAIL si >1. (B=1 libre → skip ; B=3 sectoriel exclu en amont → skip.)
  - cap_unsatisfiable (WARN) : en B=2, si le bucket dominante est 100% [SECTORIEL]
    (cap mécaniquement impossible — brief trop sectoriel).

Le cap B=2 devient ainsi VÉRIFIÉ (avant : jugement manuel du composeur).

Usage :
  python3 bucket_gate.py <palette.md> --grid <01-grid.md> --ventre-mou <p> --cursor-b N
                         [--catalogue <p>] [--json-output]
Exit : 0 PASS · 1 FAIL · 2 erreur fichier
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_v2 as gv          # noqa: E402  (parse_grid)
import match_hexes as mh      # noqa: E402
import tags as tg             # noqa: E402
import project_buckets as pb  # noqa: E402  (build_buckets)


def hex_to_rgb(h: str):
    s = h.strip().lstrip('#')
    if len(s) == 3:
        s = ''.join(c * 2 for c in s)
    if len(s) != 6:
        return None
    try:
        return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    except ValueError:
        return None


def nearest_family(hexstr: str, entries) -> str:
    """Famille catalogue ('short') dont un hex indicatif est le plus proche (distance RGB²)."""
    rgb = hex_to_rgb(hexstr)
    if rgb is None:
        return ''
    best, best_d = '', 1e18
    for e in entries:
        for hx in e['hexes']:
            c = hex_to_rgb(hx)
            if not c:
                continue
            d = (rgb[0] - c[0]) ** 2 + (rgb[1] - c[1]) ** 2 + (rgb[2] - c[2]) ** 2
            if d < best_d:
                best_d, best = d, e['short']
    return best


def parse_role_hex(content: str, role: str) -> str:
    """Extrait le hex d'un rôle exact dans la table palette (ancré sur | role |)."""
    m = re.search(r'\|\s*' + re.escape(role) + r'\s*\|[^|]*\|\s*`?(#[0-9a-fA-F]{3,6})`?', content, re.I)
    return m.group(1) if m else ''


def parse_declared_dominantes(content: str) -> list[str]:
    """Gammes DÉCLARÉES en dominante par le composeur (section « Dominantes (Primary,
    Secondary) »). On lit la déclaration plutôt que le hex : en terrain chromatiquement
    homogène (B=3 tout-chaud), le matching hex→famille confond les familles voisines
    (orange brûlé ≈ cuivre ≈ terracotta) → faux positifs. Le nom déclaré pointe la
    bonne famille du bucket sans ambiguïté.

    Robuste à DEUX formats (le composeur n'utilise pas toujours les backticks, et le
    template de sortie n'en impose pas sur cette ligne) :
      1. avec backticks : … `Gamme A` … `Gamme B`
      2. texte nu       : Gamme A (Primary) × Gamme B (Secondary). <prose éventuelle>
    Sans cette robustesse, le format nu retombe sur le repli hex (faux positifs)."""
    m = re.search(r'\*\*Dominantes[^\n]*\*\*\s*:?(.+?)(?:\n\s*\*\*|\n\s*##|\n\s*\n)', content, re.S | re.I)
    if not m:
        return []
    seg = m.group(1).strip()
    # Format 1 : noms entre backticks (prioritaire, sans ambiguïté)
    backticked = re.findall(r'`([^`]+)`', seg)
    if backticked:
        return [n.strip() for n in backticked][:2]
    # Format 2 : texte nu. On coupe sur les séparateurs de DOMINANTES (× + ·, « et »),
    # jamais sur « / » ni « , » qui appartiennent aux noms de gammes
    # (« Verts olives désaturés / kaki éteint »).
    names = []
    for p in re.split(r'\s*[×+·]\s*|\s+et\s+', seg.split('\n')[0]):
        p = p.split('.')[0]                                  # coupe la prose qui suit (les noms n'ont pas de point)
        p = re.sub(r'\b(?:Primary|Secondary)\s*=\s*', '', p, flags=re.I)
        p = re.sub(r'\([^)]*\)', '', p)                      # annotations de rôle entre parenthèses
        p = re.sub(r'\[[^\]]*\]', '', p)                     # tags [SECTORIEL] / [SLOP_RISQUE]
        p = re.sub(r'\s*—.*$', '', p)                        # « — bucket… », « — toutes deux… »
        p = p.strip(' .:—-')
        if p:
            names.append(p)
    return names[:2]


# Raisons d'exclusion DURES : l'accent libre ne peut PAS réintroduire ces gammes
# (par opposition aux exclusions « non évoqué / redondant », elles, accessibles à l'accent).
HARD_EXCL_KW = ['contredit', 'contradiction', 'contre-tempér', 'contre-temp', 'alarmiste',
                'déplacé auto', 'marqueur slop', 'ai-tell', 'slop', 'clinquant', 'opposé']


def load_hard_excluded(grid_content: str, catalogue) -> set:
    """Familles exclues par le routeur pour une raison DURE (contradiction franche, slop,
    contre-température, clinquant opposé). Retourne un set de familles normalisées."""
    m = re.search(r'###\s+Gammes\s+exclues(.+?)(?:\n\*\*|\n##\s|\Z)', grid_content, re.S | re.I)
    hard = set()
    if not m:
        return hard
    for line in m.group(1).splitlines():
        s = line.strip()
        if not s.startswith('|'):
            continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if len(cells) < 2 or cells[0].lower().startswith('gamme') or set(cells[0]) <= set('- '):
            continue
        if any(k in cells[1].lower() for k in HARD_EXCL_KW):
            _, _, fam = mh.match(cells[0], catalogue)
            if fam:
                hard.add(pb._norm(fam))
    return hard


def parse_declared_accent(content: str) -> str:
    """Nom de gamme déclaré pour l'Accent (ligne « **Accent** : … »), nettoyé."""
    m = re.search(r'\*\*Accent\*\*\s*:?(.+)', content, re.I)
    if not m:
        return ''
    seg = m.group(1).split('\n')[0]
    seg = re.sub(r'\([^)]*\)', '', seg)
    seg = re.sub(r'\blibre\b\s*[:—-]*', '', seg, flags=re.I)
    seg = re.sub(r'`', '', seg)
    return seg.strip(' .:—-')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('palette')
    ap.add_argument('--grid', required=True)
    ap.add_argument('--ventre-mou', default=None)
    ap.add_argument('--cursor-b', type=int, default=2)
    ap.add_argument('--catalogue', default=str(Path(__file__).resolve().parent.parent / 'ref' / 'chromatic-spectrum-catalog.md'))
    ap.add_argument('--json-output', action='store_true')
    args = ap.parse_args()

    pal_path = Path(args.palette)
    if not pal_path.exists():
        print(f"Introuvable : {pal_path}", file=sys.stderr)
        return 2
    content = pal_path.read_text(encoding='utf-8')
    catalogue = mh.load_catalogue(Path(args.catalogue))
    slop_set = tg.load_slop_risk(Path(args.catalogue))
    sectoral = []
    if args.ventre_mou and Path(args.ventre_mou).exists():
        sectoral = tg.load_sectoral_families(Path(args.ventre_mou).read_text(encoding='utf-8'))

    parsed = gv.parse_grid(Path(args.grid).read_text(encoding='utf-8'))
    buckets = pb.build_buckets(parsed, catalogue, slop_set, sectoral)
    dom_families = {pb._norm(e['family']) for e in buckets['dominante'] if e['family']}
    dom_all_sectoral = bool(buckets['dominante']) and all('[SECTORIEL]' in e['tags'] for e in buckets['dominante'])

    violations, warnings = [], []
    dominantes = {}  # libellé -> {family, hex, sectoral, source}

    def fam_is_sectoral(fam):
        return bool(fam) and '[SECTORIEL]' in tg.tags_for(fam, catalogue, slop_set, sectoral)

    declared = parse_declared_dominantes(content)
    if declared:
        # MÉTHODE ROBUSTE : on juge sur la gamme DÉCLARÉE (nom → famille catalogue)
        for name in declared:
            _, _, fam = mh.match(name, catalogue)
            dominantes[name] = {'family': fam, 'hex': None, 'sectoral': fam_is_sectoral(fam), 'source': 'déclarée'}
            if not fam:
                warnings.append({'check': 'dominantes_in_bucket', 'severity': 'WARN',
                                 'detail': f"Dominante déclarée « {name[:40]} » : famille catalogue non identifiable."})
            elif pb._norm(fam) not in dom_families:
                violations.append({'check': 'dominantes_in_bucket', 'severity': 'FAIL',
                                   'detail': f"Dominante déclarée « {name[:40]} » → famille « {fam} » absente du bucket DOMINANTE."})
    else:
        # REPLI : pas de section « Dominantes » parsable → vérif par hex (moins fiable en terrain chaud)
        warnings.append({'check': 'dominantes_source', 'severity': 'WARN',
                         'detail': "Section « Dominantes » non parsable → vérification par hex (peut produire des faux positifs en terrain chromatique homogène)."})
        for role in ('Primary', 'Secondary'):
            hx = parse_role_hex(content, role)
            fam = nearest_family(hx, catalogue) if hx else ''
            dominantes[role] = {'family': fam, 'hex': hx, 'sectoral': fam_is_sectoral(fam), 'source': 'hex'}
            if fam and pb._norm(fam) not in dom_families:
                violations.append({'check': 'dominantes_in_bucket', 'severity': 'FAIL',
                                   'detail': f"{role} {hx} → famille « {fam} » absente du bucket DOMINANTE (par hex)."})

    # cap sectoriel B=2 (sur les dominantes retenues)
    if args.cursor_b == 2:
        sect_count = sum(1 for d in dominantes.values() if d['sectoral'])
        if sect_count > 1:
            violations.append({'check': 'sectoral_cap_b2', 'severity': 'FAIL',
                               'detail': f"{sect_count} dominantes [SECTORIEL] (cap B=2 = max 1)."})
        if dom_all_sectoral:
            warnings.append({'check': 'cap_unsatisfiable', 'severity': 'WARN',
                             'detail': "Bucket DOMINANTE 100% [SECTORIEL] : cap B=2 mécaniquement impossible (brief trop sectoriel)."})

    # accent : la liberté de l'accent NE permet PAS de réintroduire une gamme exclue pour
    # raison DURE (contradiction franche / slop / contre-température). Seules les exclusions
    # « non évoqué / redondant » restent accessibles à l'accent.
    hard_excl = load_hard_excluded(Path(args.grid).read_text(encoding='utf-8'), catalogue)
    acc_name = parse_declared_accent(content)
    acc_hex = parse_role_hex(content, 'Accent')
    acc_fam = ''
    if acc_name:
        _, _, acc_fam = mh.match(acc_name, catalogue)
    if not acc_fam and acc_hex:
        acc_fam = nearest_family(acc_hex, catalogue)
    if acc_fam and pb._norm(acc_fam) in hard_excl:
        violations.append({'check': 'accent_hard_excluded', 'severity': 'FAIL',
                           'detail': f"Accent → famille « {acc_fam} » exclue par le routeur pour raison DURE "
                                     "(contradiction franche / slop / contre-température). L'accent libre ne peut "
                                     "réintroduire qu'une gamme exclue « non évoquée », pas une exclusion dure."})

    verdict = 'FAIL' if violations else 'PASS'
    result = {'verdict': verdict, 'file': str(pal_path), 'cursor_b': args.cursor_b,
              'dominantes': dominantes, 'violations': violations, 'warnings': warnings}
    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== BUCKET GATE — {pal_path.name} === {verdict}")
        for v in violations:
            print(f"  [FAIL] {v['check']}: {v['detail']}")
        for w in warnings:
            print(f"  [WARN] {w['check']}: {w['detail']}")
    return 1 if violations else 0


if __name__ == '__main__':
    sys.exit(main())
