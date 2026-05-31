#!/usr/bin/env python3
"""
tags.py — Tags FIXES, posés MÉCANIQUEMENT (le routeur ne les interprète pas).

- [SLOP_RISQUE] : propriété fixe de zones du catalogue (violet/indigo, neutres non
  orientés, bleus AI-tell…). Dérivée des marqueurs ⚠ du catalogue. Universelle.
- [SECTORIEL]   : défini en amont par la directive Ventre Mou (liste explicite de
  familles catalogue). Brief-spécifique mais NON inventé par le routeur.

On attache ces tags en aval, sur les gammes validées ET exclues, par matching du nom
reformulé vers l'entrée catalogue.
"""

from __future__ import annotations

import re
from pathlib import Path

import match_hexes as mh

# Marqueurs ⚠ d'une LIGNE de sous-gamme qui en font une zone slop-risk
_SLOP_LINE_MARKERS = ['slop', 'ai-tell', 'training-defaults', 'marqueur slop']
# Un en-tête de famille contenant ce marqueur => toute la famille est slop-risk
_SLOP_FAMILY_MARKER = 'slop_risque'


def load_slop_risk(catalogue_path: Path) -> set[str]:
    """Ensemble des noms-courts de sous-gammes en zone slop-risk (déterministe)."""
    slop: set[str] = set()
    family_is_slop = False
    for line in Path(catalogue_path).read_text(encoding='utf-8').splitlines():
        h = re.match(r'###\s+\d+\.\s+(.+)', line)
        if h:
            family_is_slop = _SLOP_FAMILY_MARKER in line.lower()
            continue
        m = re.match(r'\s*-\s+\*\*(.+?)\*\*\s*(.*)', line)
        if not m:
            continue
        name, rest = m.group(1).strip(), m.group(2)
        low = (name + ' ' + rest).lower()
        if family_is_slop or any(mk in low for mk in _SLOP_LINE_MARKERS):
            slop.add(name)
    return slop


def load_sectoral_families(directive_text: str) -> list[str]:
    """Liste des familles catalogue marquées sectorielles dans la directive Ventre Mou.
    Cherche une ligne « Familles catalogue concernées : a ; b ; c »."""
    m = re.search(r'Familles\s+catalogue\s+concernées\s*:?\s*(.+)', directive_text, re.I)
    if not m:
        return []
    return [x.strip() for x in re.split(r'[;,]', m.group(1)) if x.strip()]


def tags_for(gamut_name: str, catalogue: list[dict], slop_set: set[str],
             sectoral_shorts: list[str]) -> list[str]:
    """Tags fixes d'une gamme (nom reformulé) : matche le catalogue puis applique."""
    _, _, matched = mh.match(gamut_name, catalogue)
    out = []
    if matched and matched in slop_set:
        out.append('[SLOP_RISQUE]')
    # sectoriel : le nom-noyau d'une famille sectorielle apparaît dans la gamme
    if matched:
        sect_tokens = [mh.tokenize(s) for s in sectoral_shorts]
        mtoks = mh.tokenize(matched)
        if any(st and st <= mtoks for st in sect_tokens) or matched in sectoral_shorts:
            out.append('[SECTORIEL]')
    return out
