#!/usr/bin/env python3
"""
gate_v2.py — Gate du routeur chromatique v2 (exhaustif binaire : territoire × aptitude / exclu).

Checks FAIL stricts :
  format_strict          — header, keywords, ≥3 sections territoire, section exclues, accent libre
  exhaustive_coverage    — les ~45 sous-gammes du catalogue sont TOUTES classées (validé ∪ exclu)
  anti_amputation        — chaque territoire ≥3 gammes
  functional_completeness— chacune des 3 aptitudes (base/dominante/accent) ≥1 gamme validée
  aptitude_validity      — l'aptitude déclarée ne contredit pas l'intensité calculée (≥30% de contradictions DURES = FAIL)
  no_temperature_words   — pas de chaud/froid/neutre dans les noms
  min_specificity        — nom ≥3 mots OU qualificatif
  justification_present  — « Mot-clé servi » non vide et non générique
  no_duplicate_gamuts    — pas de doublon INTRA-territoire
Advisory (WARN) :
  energy_survival        — un territoire énergique a-t-il un accent qui claque ?

NB : les tags [SLOP_RISQUE]/[SECTORIEL] sont posés MÉCANIQUEMENT en aval (tags.py) —
le gate ne les vérifie plus.

Usage : python3 gate_v2.py <grid.md> [--catalogue <path>] [--json-output]
Exit : 0 PASS / 1 FAIL / 2 erreur fichier
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import derive_aptitude as da  # noqa: E402
import match_hexes as mh      # noqa: E402
import tags as tg             # noqa: E402

BANNED_TEMPERATURE_WORDS = [
    'chaud', 'chauds', 'chaude', 'chaudes', 'froid', 'froids', 'froide', 'froides',
    'neutre', 'neutres', 'température', 'temperature', 'tiède', 'tiedes', 'tiede', 'warm', 'cool',
]
GENERIC_JUSTIF = [
    r'\bton\s+moderne\b', r'\bton\s+élégant\b', r'\bton\s+universel\b',
    r'\bconvient\s+bien\b', r'\bfonctionne\s+bien\b', r'\bvaleur\s+sûre\b',
]
SPECIFICITY_QUALIFIERS = [
    'saturé', 'saturée', 'saturés', 'saturées', 'désaturé', 'désaturée', 'profond', 'profonds',
    'profonde', 'profondes', 'clair', 'claire', 'clairs', 'sombre', 'sombres', 'éteint', 'éteinte',
    'lumineux', 'lumineuse', 'poudré', 'poudrée', 'pâle', 'pâles', 'vif', 'vifs', 'vive', 'vives',
    'doux', 'sourd', 'mat', 'mate', 'crémeux', 'forêt', 'marine', 'minéral', 'tirant', 'shifted',
    'magenta-', 'encre', "d'encre", 'olive', 'bordeaux', 'safran', 'terracotta', 'ocre',
]
ENERGETIC_KEYWORDS = [
    'vivant', 'vivante', 'optimiste', 'entraînant', 'entrainant', 'énergique', 'energique',
    'audacieux', 'audacieuse', 'pop', 'éclatant', 'joyeux', 'joyeuse', 'solaire', 'vif',
]
VALID_APTITUDES = {'base', 'dominante', 'accent'}


def normalize(s: str) -> str:
    return s.lower().strip()


def contains_any(text: str, needles: list[str]) -> bool:
    t = normalize(text)
    return any(normalize(n) in t for n in needles)


def jaccard(a: str, b: str) -> float:
    sa, sb = set(re.findall(r'\w+', normalize(a))), set(re.findall(r'\w+', normalize(b)))
    return len(sa & sb) / len(sa | sb) if sa and sb else 0.0


# ── Parser ──

def parse_rows(block: str, ncols: int) -> list[dict]:
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|') if c.strip() != '']
        if not cells:
            continue
        if normalize(cells[0]) in ('gamme', 'gammes') or set(cells[0]) <= set('-: '):
            continue
        if ncols == 3 and len(cells) >= 3:
            rows.append({'gamut': cells[0], 'aptitude': normalize(cells[1]), 'keyword': cells[2]})
        elif ncols == 2 and len(cells) >= 2:
            rows.append({'gamut': cells[0], 'reason': cells[1]})
    return rows


def parse_grid(content: str) -> dict:
    res = {
        'has_main_header': bool(re.search(r'##\s+Grille\s+chromatique', content, re.I)),
        'has_keywords': bool(re.search(r'\*\*Mots-clés\s+dominants\s+analysés\*\*', content, re.I)),
        'has_excluded': bool(re.search(r'###\s+Gammes\s+exclues', content, re.I)),
        'has_accent_libre': bool(re.search(r'\*\*Accent\s+libre\*\*', content, re.I)),
        'territories': [], 'excluded_rows': [],
    }
    for sec in re.split(r'\n(?=###\s+)', content):
        head = re.match(r'###\s+(.+)', sec)
        if not head:
            continue
        title = head.group(1).strip()
        if normalize(title).startswith('gammes exclues'):
            res['excluded_rows'] = parse_rows(sec, 2)
        else:
            rows = parse_rows(sec, 3)
            if rows:
                res['territories'].append({'name': title, 'rows': rows})
    return res


def all_validated(parsed: dict) -> list[dict]:
    return [{**r, '_territory': t['name']} for t in parsed['territories'] for r in t['rows']]


# ── Checks ──

def check_format(parsed):
    miss = []
    if not parsed['has_main_header']: miss.append('## Grille chromatique (routeur v2)')
    if not parsed['has_keywords']: miss.append('**Mots-clés dominants analysés**')
    if len(parsed['territories']) < 3: miss.append(f"3 sections territoire (trouvé {len(parsed['territories'])})")
    if not parsed['has_excluded']: miss.append('### Gammes exclues')
    if not parsed['has_accent_libre']: miss.append('**Accent libre**')
    return [{'check': 'format_strict', 'severity': 'FAIL', 'detail': 'Manquant : ' + ', '.join(miss)}] if miss else []


def check_no_temperature(parsed):
    # Validé uniquement : c'est ce qui descend à la palette (anti-biais température).
    # Sur une exclue, « froid » est juste descriptif du motif d'exclusion — toléré.
    v = []
    for r in all_validated(parsed):
        words = re.findall(r"[\wÀ-ÿ']+", normalize(r['gamut']))
        for b in BANNED_TEMPERATURE_WORDS:
            if normalize(b) in words:
                v.append({'check': 'no_temperature_words', 'severity': 'FAIL',
                          'detail': f"Mot-température '{b}' dans : '{r['gamut']}'"})
                break
    return v


def check_min_specificity(parsed):
    # S'applique au VALIDÉ uniquement (ce qui nourrit la palette) ; un exclu n'a besoin
    # que d'une raison, pas d'un nom reformulé riche (cas des entrées annexe : « Néons »).
    v = []
    for r in all_validated(parsed):
        n = r['gamut']
        if len(re.findall(r"[\wÀ-ÿ']+", n)) >= 3 or contains_any(n, SPECIFICITY_QUALIFIERS):
            continue
        v.append({'check': 'min_specificity', 'severity': 'FAIL', 'detail': f"Nom trop court : '{n}'"})
    return v


def check_justification(parsed):
    v = []
    for r in all_validated(parsed):
        kw = r.get('keyword', '')
        if not kw or len(kw.strip()) < 3:
            v.append({'check': 'justification_present', 'severity': 'FAIL',
                      'detail': f"Mot-clé servi vide : '{r['gamut']}'"})
        elif any(re.search(p, kw, re.I) for p in GENERIC_JUSTIF):
            v.append({'check': 'justification_present', 'severity': 'FAIL',
                      'detail': f"Mot-clé générique pour '{r['gamut']}' : '{kw}'"})
    return v


def check_no_duplicates_intra(parsed):
    v = []
    for t in parsed['territories']:
        rows = t['rows']
        for i in range(len(rows)):
            for j in range(i):
                if jaccard(rows[i]['gamut'], rows[j]['gamut']) > 0.6:
                    v.append({'check': 'no_duplicate_gamuts', 'severity': 'FAIL',
                              'detail': f"Doublon intra-'{t['name'][:30]}': '{rows[i]['gamut']}' ~ '{rows[j]['gamut']}'"})
                    break
    return v


def check_anti_amputation(parsed):
    return [{'check': 'anti_amputation', 'severity': 'FAIL',
             'detail': f"Territoire '{t['name'][:40]}' amputé : {len(t['rows'])} gamme(s) (min 3)"}
            for t in parsed['territories'] if len(t['rows']) < 3]


def check_functional_completeness(parsed):
    apts = {r['aptitude'] for r in all_validated(parsed)}
    return [{'check': 'functional_completeness', 'severity': 'FAIL',
             'detail': f"Aptitude '{a}' non pourvue"} for a in ('base', 'dominante', 'accent') if a not in apts]


def check_min_accents(parsed):
    """Au moins 2 gammes apte-accent (sinon palette difficilement exploitable)."""
    n = sum(1 for r in all_validated(parsed) if r['aptitude'] == 'accent')
    if n < 2:
        return [{'check': 'min_accents', 'severity': 'FAIL',
                 'detail': f"{n} accent(s) — minimum 2 requis (les 2+ gammes les plus intenses du terrain)."}]
    return []


def check_sectoral_conflict(parsed, sectoral_shorts, catalogue):
    """PRIMAUTÉ DURE : une gamme de la liste sectorielle (B=3) ne peut PAS être validée.
    Filtre déterministe — prime sur toute justification par-territoire (anti blueprint-blue)."""
    if not sectoral_shorts:
        return []
    sect_tok = [mh.tokenize(s) for s in sectoral_shorts]
    v = []
    for r in all_validated(parsed):
        _, _, matched = mh.match(r['gamut'], catalogue)
        if not matched:
            continue
        mtoks = mh.tokenize(matched)
        if matched in sectoral_shorts or any(st and st <= mtoks for st in sect_tok):
            v.append({'check': 'sectoral_conflict', 'severity': 'FAIL',
                      'detail': f"Gamme SECTORIELLE validée ({r['_territory'][:25]}) : '{r['gamut']}' "
                                f"→ famille '{matched}' exclue par B=3. La directive sectorielle PRIME : "
                                f"déplace-la en exclu (accent libre seulement)."})
    return v


def check_sectoral_inclusion(parsed, sectoral, catalogue):
    """B=1 (Mimétisme) : INCLUSION OBLIGATOIRE — chaque famille sectorielle DOIT
    apparaître dans le validé (elle s'ajoute aux territoires). Famille absente → FAIL."""
    if not sectoral:
        return []
    validated = [r['gamut'] for r in all_validated(parsed)]
    val_tok = [mh.tokenize(n) for n in validated]
    val_shorts = set()
    for n in validated:
        _, _, m = mh.match(n, catalogue)
        if m:
            val_shorts.add(m)
    missing = [fam for fam in sectoral
               if fam not in val_shorts and not any(mh.tokenize(fam) and mh.tokenize(fam) <= vt for vt in val_tok)]
    if missing:
        return [{'check': 'sectoral_inclusion', 'severity': 'FAIL',
                 'detail': f"B=1 inclusion obligatoire : {len(missing)} famille(s) sectorielle(s) absente(s) "
                           f"du validé : " + ', '.join(missing[:8]) + (' …' if len(missing) > 8 else '')
                           + " — tu DOIS les valider (même hors analyse territoires)."}]
    return []


def check_temperature_coherence(parsed, temperature, catalogue, cursor_b=3, sectoral=None, mode='on'):
    """PRIMAUTÉ DURE : une gamme validée à contre-température → FAIL.
    EXCEPTION B=1 : les familles sectorielles sont EXEMPTÉES (mimétisme = on garde les
    codes secteur même froids ; l'inclusion prime sur la température).
    mode='minimal' : ne FAIL que les gammes à contre-brief FRANCHEMENT VIVES en
    dominante/accent (cohérent avec enforce --temp-filter minimal)."""
    temp = (temperature or '').strip().lower()
    if temp not in ('chaud', 'froid'):
        return []
    opp = 'cold' if temp == 'chaud' else 'warm'
    sect_tok = [mh.tokenize(s) for s in (sectoral or [])]
    v = []
    for r in all_validated(parsed):
        hexes, _, matched = mh.match(r['gamut'], catalogue)
        if not hexes:
            continue
        is_sect = bool(matched) and (matched in (sectoral or []) or any(st and st <= mh.tokenize(matched) for st in sect_tok))
        if cursor_b == 1 and is_sect:
            continue  # B=1 : sectoriel exempté de la température
        if da.warmth(hexes) != opp:
            continue
        if mode == 'minimal':
            if r['aptitude'] not in ('dominante', 'accent'):
                continue
            s, l = da.avg_sl(hexes)
            if da.intensity(s, l) < da.CONTRA_TEMP_VIVID_INTENSITY:
                continue
        v.append({'check': 'temperature_coherence', 'severity': 'FAIL',
                  'detail': f"'{r['gamut']}' ({r['aptitude']}) est {opp} alors que température validée = {temp}. "
                            f"La température PRIME → exclu pour Primary/Secondary."})
    return v


def check_exhaustive(parsed, families):
    """Chaque famille du catalogue (les ~45) doit être validée OU exclue.
    Couverture par le matcher IDF (robuste aux reformulations) + repli token-subset."""
    named = [r['gamut'] for r in all_validated(parsed)] + [r['gamut'] for r in parsed['excluded_rows']]
    named_tok = [mh.tokenize(n) for n in named]
    # covered via le matcher IDF : chaque nom reformulé pointe vers sa famille catalogue
    covered = set()
    for n in named:
        _, _, matched = mh.match(n, families)
        if matched:
            covered.add(matched)
    missing = []
    for e in families:
        if e['short'] in covered:
            continue
        etoks = mh.tokenize(e['short'])
        if any(etoks and etoks <= nt for nt in named_tok):
            continue
        if any(jaccard(e['short'], n) >= 0.45 for n in named):
            continue
        missing.append(e['short'])
    if missing:
        return [{'check': 'exhaustive_coverage', 'severity': 'FAIL',
                 'detail': f"{len(missing)} famille(s) catalogue NON classée(s) (ni validée ni exclue) : "
                           + ', '.join(missing[:12]) + ('…' if len(missing) > 12 else '')}]
    return []


def check_aptitude_validity(parsed, catalogue):
    v, warnings = [], []
    verifiable, hard = 0, 0
    for r in all_validated(parsed):
        apt = r['aptitude']
        if apt not in VALID_APTITUDES:
            v.append({'check': 'aptitude_validity', 'severity': 'FAIL',
                      'detail': f"Aptitude invalide '{apt}' pour '{r['gamut']}'"})
            continue
        hexes, _, _ = mh.match(r['gamut'], catalogue)
        if not hexes:
            warnings.append({'check': 'aptitude_validity', 'severity': 'WARN',
                             'detail': f"Aptitude non-vérifiable (pas de match) : '{r['gamut']}'"})
            continue
        verifiable += 1
        s, l = da.avg_sl(hexes)
        inten = da.intensity(s, l)
        if apt == 'base' and not da.is_base(r['gamut'], s, l) and inten > 0.45:
            hard += 1
            warnings.append({'check': 'aptitude_validity', 'severity': 'WARN',
                             'detail': f"'{r['gamut']}' déclaré base mais vif (S={s:.2f} L={l:.2f} int={inten:.2f})"})
        elif apt == 'accent' and da.is_base(r['gamut'], s, l):
            warnings.append({'check': 'aptitude_validity', 'severity': 'WARN',
                             'detail': f"'{r['gamut']}' déclaré accent mais calculé neutre (S={s:.2f} L={l:.2f})"})
    rate = (hard / verifiable) if verifiable else 0.0
    if rate >= 0.30:
        v.append({'check': 'aptitude_validity', 'severity': 'FAIL',
                  'detail': f"{hard}/{verifiable} 'base' contredites par l'intensité ({rate:.0%} ≥ 30%) — aptitudes inventées ?"})
    return v, warnings, round(rate, 2)


def check_energy_survival(parsed, catalogue):
    warnings = []
    for t in parsed['territories']:
        energetic = contains_any(t['name'], ENERGETIC_KEYWORDS) or \
            any(contains_any(r.get('keyword', ''), ENERGETIC_KEYWORDS) for r in t['rows'])
        if not energetic:
            continue
        strong = False
        for r in t['rows']:
            if r['aptitude'] != 'accent':
                continue
            hexes, _, _ = mh.match(r['gamut'], catalogue)
            if hexes:
                s, l = da.avg_sl(hexes)
                if da.intensity(s, l) >= da.ACCENT_WEAK_INTENSITY:
                    strong = True
        if not strong:
            warnings.append({'check': 'energy_survival', 'severity': 'WARN',
                             'detail': f"Territoire énergique '{t['name'][:40]}' sans accent qui claque"})
    return warnings


def _opt(name):
    for i, a in enumerate(sys.argv):
        if a == name and i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return None


def main() -> int:
    json_out = '--json-output' in sys.argv
    cat_arg, vm_arg, temp_arg, cb_arg = _opt('--catalogue'), _opt('--ventre-mou'), _opt('--temperature'), _opt('--cursor-b')
    temp_filter = (_opt('--temp-filter') or 'minimal')  # DÉFAUT sanctuarisé : minimal (filet froid/chaud vif sur dominante/accent) · on=legacy · off=aucun
    cursor_b = int(cb_arg) if cb_arg else 3
    consumed = {cat_arg, vm_arg, temp_arg, cb_arg, _opt('--temp-filter')}
    args = [a for a in sys.argv[1:] if not a.startswith('--') and a not in consumed]
    if not args:
        print('Usage: gate_v2.py <grid.md> [--catalogue <p>] [--ventre-mou <p>] [--temperature chaud|froid] [--json-output]')
        return 2
    grid_path = Path(args[0])
    if not grid_path.exists():
        print(f'Introuvable : {grid_path}')
        return 2
    cat_path = Path(cat_arg) if cat_arg else Path(__file__).resolve().parent.parent / 'ref' / 'chromatic-spectrum-catalog.md'
    catalogue = mh.load_catalogue(cat_path) if cat_path.exists() else []
    families = mh.load_catalogue(cat_path, families_only=True) if cat_path.exists() else []
    sectoral = []
    if vm_arg and Path(vm_arg).exists():
        sectoral = tg.load_sectoral_families(Path(vm_arg).read_text(encoding='utf-8'))

    parsed = parse_grid(grid_path.read_text(encoding='utf-8'))

    violations, warnings = [], []
    for fn in (check_format, check_no_temperature, check_min_specificity, check_justification,
               check_no_duplicates_intra, check_anti_amputation, check_functional_completeness,
               check_min_accents):
        violations += fn(parsed)
    violations += check_exhaustive(parsed, families)
    # Curseur B (sectoriel) : B=3 exclusion → conflit si validé ; B=1 inclusion oblig. → manque si absent ; B=2 ni l'un ni l'autre
    if cursor_b == 3:
        violations += check_sectoral_conflict(parsed, sectoral, catalogue)
    elif cursor_b == 1:
        violations += check_sectoral_inclusion(parsed, sectoral, catalogue)
    if temp_filter != 'off':
        violations += check_temperature_coherence(parsed, temp_arg, catalogue, cursor_b, sectoral, mode=temp_filter)
    av_v, av_w, mismatch = check_aptitude_validity(parsed, catalogue)
    violations += av_v
    warnings += av_w + check_energy_survival(parsed, catalogue)

    verdict, code = ('FAIL', 1) if violations else ('PASS', 0)

    per_territory = {t['name'][:40]: len(t['rows']) for t in parsed['territories']}
    apt_counts = {}
    for r in all_validated(parsed):
        apt_counts[r['aptitude']] = apt_counts.get(r['aptitude'], 0) + 1
    classified = len(all_validated(parsed)) + len(parsed['excluded_rows'])

    if json_out:
        print(json.dumps({'verdict': verdict, 'file': str(grid_path), 'violations': violations,
                          'warnings': warnings, 'per_territory_counts': per_territory,
                          'aptitude_counts': apt_counts, 'aptitude_mismatch_rate': mismatch,
                          'validated': len(all_validated(parsed)), 'excluded': len(parsed['excluded_rows']),
                          'families_target': len(families)}, ensure_ascii=False, indent=2))
        return code

    print(f"\n=== GATE v2 (exhaustif binaire) — {grid_path.name} ===")
    print(f"Territoires : {per_territory}")
    print(f"Validées : {len(all_validated(parsed))} · Exclues : {len(parsed['excluded_rows'])} · "
          f"Cible familles : {len(families)}")
    print(f"Aptitudes : {apt_counts} · mismatch : {mismatch:.0%}\n")
    if violations:
        by = {}
        for v in violations:
            by.setdefault(v['check'], []).append(v)
        print(f"[FAIL] {len(violations)} violation(s) :\n")
        for c, items in sorted(by.items()):
            print(f"  ❌ {c} ({len(items)}x)")
            for it in items[:6]:
                print(f"     {it['detail']}")
            print()
    if warnings:
        print(f"[WARN] {len(warnings)} (advisory) :")
        for w in warnings[:10]:
            print(f"  ⚠ {w['check']}: {w['detail']}")
        print()
    print(f"VERDICT: {verdict}")
    return code


if __name__ == '__main__':
    sys.exit(main())
