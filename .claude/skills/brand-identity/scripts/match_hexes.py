#!/usr/bin/env python3
"""
match_hexes.py — Mappe un nom de gamme reformulé (par le routeur) sur les hex
indicatifs de la sous-gamme correspondante du catalogue, par similarité Jaccard.

Le routeur reformule (« Safran vif — curcuma, ocre solaire ») ; le catalogue a le
nom générique (« Jaunes profonds safran / moutarde ») + 2-3 hex indicatifs. On
retrouve la meilleure entrée par recouvrement de tokens.

Pas de match au-dessus du seuil (gamme [SECTORIEL] hors-catalogue) -> [] (jamais une
erreur ; le gate marque alors l'aptitude « non-vérifiable » et le rendu n'affiche
pas de swatch).

CLI :
  --catalogue <path> --name "<nom gamme>"          -> imprime les hex (JSON)
  --catalogue <path> --names-json <terrain.json>   -> [{name, hexes}] enrichi de hexes
Importable : load_catalogue(path), match(name, entries) -> (hexes, score, matched_name)
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

THRESHOLD = 0.25

# Tokens vides à ignorer dans la comparaison
STOPWORDS = {
    'et', 'ou', 'vers', 'type', 'le', 'la', 'les', 'de', 'des', 'du', 'en', 'à',
    'un', 'une', 'pas', 'plus', 'comme', 'ex', 'sat', 'haute', 'basse', 'moyenne',
    'luminosité', 'saturation', 'profonde', 'foncé',
}


def tokenize(s: str) -> set[str]:
    s = s.lower()
    # retirer les parenthèses d'exemples hex et le contenu après « (ex: »
    s = re.sub(r'#[0-9a-fA-F]{3,6}', ' ', s)
    toks = re.findall(r"[a-zàâäéèêëïîôöùûüçœæ]{3,}", s)
    return {t for t in toks if t not in STOPWORDS}


def load_catalogue(path: Path, families_only: bool = False) -> list[dict]:
    """[{short, tokens, hexes, annex}] pour chaque sous-gamme du catalogue ayant des hex.
    Calcule aussi l'IDF de chaque token (rareté inter-entrées) pour pondérer le match.
    families_only=True : ignore l'annexe « Hors-catalogue » (néons, gradients)."""
    out = []
    in_annex = False
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if re.match(r'##\s+Hors-catalogue', line, re.I):
            in_annex = True
        if families_only and in_annex:
            continue
        m = re.match(r'\s*-\s+\*\*(.+?)\*\*\s*(.*)', line)
        if not m:
            continue
        name, rest = m.group(1).strip(), m.group(2)
        hexes = re.findall(r'#[0-9a-fA-F]{6}', rest)
        if not hexes:
            continue
        out.append({'short': name, 'tokens': tokenize(name + ' ' + rest), 'hexes': hexes, 'annex': in_annex})
    # IDF : un token présent dans peu d'entrées est distinctif (safran, terracotta…)
    n = len(out) or 1
    df: dict[str, int] = {}
    for e in out:
        for t in e['tokens']:
            df[t] = df.get(t, 0) + 1
    idf = {t: math.log(1 + n / c) for t, c in df.items()}
    for e in out:
        e['idf_total'] = sum(idf.get(t, 0.0) for t in e['tokens']) or 1.0
    # attacher l'idf global aux entrées (référence partagée)
    for e in out:
        e['_idf'] = idf
    return out


def match(name: str, entries: list[dict]) -> tuple[list[str], float, str]:
    """Retourne (hexes, score, nom_catalogue) de la meilleure entrée, ou ([],0,'').
    Score = recouvrement des tokens du catalogue pondéré par leur rareté (IDF)."""
    q = tokenize(name)
    if not entries:
        return [], 0.0, ''
    idf = entries[0]['_idf']
    best, best_score = None, 0.0
    for e in entries:
        shared = q & e['tokens']
        if not shared:
            continue
        # part de l'« information » du nom catalogue couverte par la requête
        score = sum(idf.get(t, 0.0) for t in shared) / e['idf_total']
        if score > best_score:
            best, best_score = e, score
    if best and best_score >= THRESHOLD:
        return best['hexes'], round(best_score, 2), best['short']
    return [], round(best_score, 2), ''


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--catalogue', required=True)
    ap.add_argument('--name')
    ap.add_argument('--names-json', help='terrain JSON [{name,...}] -> enrichi de hexes')
    args = ap.parse_args()

    entries = load_catalogue(Path(args.catalogue))
    if not entries:
        print('Catalogue vide / non parsé', file=sys.stderr)
        return 2

    if args.name:
        hexes, score, matched = match(args.name, entries)
        print(json.dumps({'name': args.name, 'hexes': hexes, 'score': score,
                          'matched_catalogue_entry': matched}, ensure_ascii=False, indent=2))
        return 0

    if args.names_json:
        terrain = json.loads(Path(args.names_json).read_text(encoding='utf-8'))
        for g in terrain:
            hexes, score, matched = match(g.get('name', ''), entries)
            g['hexes'] = hexes
            g['_match_score'] = score
            g['_matched_entry'] = matched
        print(json.dumps(terrain, ensure_ascii=False, indent=2))
        return 0

    ap.print_help()
    return 2


if __name__ == '__main__':
    sys.exit(main())
