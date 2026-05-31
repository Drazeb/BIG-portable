#!/usr/bin/env python3
"""
derive_aptitude.py — Dérive l'aptitude fonctionnelle (base / dominante / accent)
d'une gamme chromatique à partir de son intensité (saturation + luminosité).

Logique HYBRIDE (cf. plan ok-tr-s-bien-on-compressed-dragon.md) :

  1. ABSOLU — séparer les NEUTRES (base) des COULEURS.
     Un fond/texte doit rester lisible → seuil absolu de désaturation/contraste.
     base si  S <= S_BASE_MAX  OU  L >= L_BASE_HIGH  OU  L <= L_BASE_LOW.
     Garde-fou sémantique : descripteur du catalogue prime (« désaturé/poudré/pâle »
     pousse vers base ; « vif/saturé/pop » interdit base).

  2. RELATIF — parmi les COULEURS d'un même terrain, classer par rang d'intensité :
     la/les plus intense(s) -> accent ; le reste -> dominante.
     => l'accent existe dès qu'il y a >=1 couleur, quelle que soit sa saturation
        absolue (auto-régulation : douce si brief calme, vive si brief énergique).

Rôle dans le gate : le signal DUR et gateable est la frontière base<->couleur
(absolue, fiable). La frontière accent<->dominante est relative/molle -> advisory.
Le bug « grimoire » = déclarer une couleur saturée comme base ; c'est ce que le
cross-check base/couleur attrape.

Modes CLI :
  --calibrate <catalogue.md>   : classe les ~33 sous-gammes du catalogue, affiche
                                 S/L/intensité + conflits descripteur (calibration).
  --json <terrain.json>        : terrain = [{"name":..., "hexes":[...]}, ...]
                                 -> imprime le classement (base/dominante/accent).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Seuils (calibrés sur le catalogue — cf. --calibrate)
# ---------------------------------------------------------------------------

S_BASE_MAX = 0.22     # saturation <= -> candidat base (désaturé)
L_BASE_HIGH = 0.85    # luminosité >= -> candidat base (très clair = fond clair)
L_BASE_LOW = 0.12     # luminosité <= -> candidat base (très sombre = fond sombre)

# Tier accent : une couleur est apte-accent si son intensité >= ACCENT_TIER * max_intensité
# du terrain (et au moins la plus intense l'est toujours).
ACCENT_TIER = 0.72

# Seuil d'intensité absolue sous lequel un « accent » est jugé désaturé (advisory
# energy_survival du gate — pas une frontière de classement).
ACCENT_WEAK_INTENSITY = 0.30

# Filet « contre-température minimal » (mode --temp-filter minimal) : seuil d'intensité
# au-dessus duquel une gamme à contre-brief est jugée FRANCHEMENT VIVE (cyan fintech,
# bleu AI, orange pop) et donc retirée des dominante/accent. En dessous, c'est un
# désaturé/profond utilisable (bleu de plan, marine sombre, terracotta éteint) qu'on
# conserve. Calibré pour laisser passer S~0,30-0,45 et rattraper S~0,8.
CONTRA_TEMP_VIVID_INTENSITY = 0.55

# Descripteurs sémantiques (le nom du catalogue / la reformulation du routeur)
DESATURATED_WORDS = [
    'désaturé', 'desature', 'désaturée', 'desaturee', 'désaturés', 'désaturées',
    'éteint', 'eteint', 'éteinte', 'eteinte', 'éteints', 'éteintes',
    'poudré', 'poudre', 'poudrée', 'poudreuse', 'poudrés', 'poudrées',
    'pâle', 'pale', 'pâles', 'pales', 'pastel',
    'sourd', 'sourds', 'sourde', 'sourdes',
    'craie', 'chalk', 'crémeux', 'cremeux', 'off-white', 'off-black',
]
# NB : « mat/mate » décrivent le FINI, pas la chroma — un or mat reste saturé.
# Donc PAS dans DESATURATED_WORDS (sinon les métalliques basculeraient à tort en base).
SATURATED_WORDS = [
    'vif', 'vifs', 'vive', 'vives',
    'saturé', 'sature', 'saturée', 'saturees', 'saturés', 'saturées',
    'pop', 'solaire', 'acidulé', 'acidule', 'acidulés', 'fluo', 'néon', 'neon',
    'électrique', 'electrique', 'franc', 'franche', 'charnel', 'charnelle',
]
# Familles explicitement neutres dans le catalogue
NEUTRAL_WORDS = [
    'off-white', 'off-black', 'gris', 'beige', 'sable', 'ivoire', 'crème', 'creme',
    'taupe', 'ardoise', 'anthracite', 'graphite', 'blanc', 'noir',
]


def _norm(s: str) -> str:
    return s.lower().strip()


# Classe « lettre » incluant les accents FR : sert de frontière de mot.
# Évite que 'saturé' matche 'dé-saturé-s' ou 'gris' matche 'vert-de-gris'.
_LETTER = "a-zàâäéèêëïîôöùûüçœæ"


def _contains(text: str, words: list[str]) -> bool:
    t = _norm(text)
    for w in words:
        # un trait d'union compte comme frontière (ex: 'off-white', 'vert-de-gris')
        pat = rf"(?<![{_LETTER}]){re.escape(_norm(w))}(?![{_LETTER}])"
        if re.search(pat, t):
            return True
    return False


# ---------------------------------------------------------------------------
# Couleur : hex -> HSL
# ---------------------------------------------------------------------------

def hex_to_hsl(hexstr: str) -> tuple[float, float, float]:
    h = hexstr.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r = int(h[0:2], 16) / 255.0
    g = int(h[2:4], 16) / 255.0
    b = int(h[4:6], 16) / 255.0
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2.0
    if mx == mn:
        return 0.0, 0.0, l  # achromatique
    d = mx - mn
    s = d / (2.0 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        hue = (g - b) / d + (6 if g < b else 0)
    elif mx == g:
        hue = (b - r) / d + 2
    else:
        hue = (r - g) / d + 4
    return hue / 6.0, s, l


def avg_sl(hexes: list[str]) -> tuple[float, float]:
    """Saturation + luminosité moyennes sur les hex d'une gamme."""
    valid = [h for h in hexes if re.match(r'^#?[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$', h.strip())]
    if not valid:
        return 0.0, 0.5
    sls = [hex_to_hsl(h) for h in valid]
    s = sum(x[1] for x in sls) / len(sls)
    l = sum(x[2] for x in sls) / len(sls)
    return s, l


def intensity(s: float, l: float) -> float:
    """Intensité perçue : saturation pondérée par la proximité d'une luminosité
    médiane (un saturé très clair ou très sombre claque moins qu'un saturé moyen)."""
    return s * (1.0 - abs(l - 0.5))


def warmth(hexes: list[str]) -> str:
    """'warm' | 'cold' | 'neutral' pour une gamme (vote sur ses hex).
    Froid = teinte cyan→bleu→indigo (165-285°) avec saturation lisible.
    Chaud = teinte rouge/orange/jaune (<70° ou >300°). Le reste (verts, près-neutres) = neutral."""
    valid = [h for h in hexes if re.match(r'^#?[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$', h.strip())]
    if not valid:
        return 'neutral'
    warm = cold = 0
    for h in valid:
        hue6, s, _ = hex_to_hsl(h)
        if s < 0.15:
            continue  # quasi-neutre : pas de température franche
        deg = hue6 * 360.0
        if 165.0 <= deg <= 285.0:
            cold += 1
        elif deg < 70.0 or deg > 300.0:
            warm += 1
    if cold > warm:
        return 'cold'
    if warm > cold:
        return 'warm'
    return 'neutral'


# ---------------------------------------------------------------------------
# Classement absolu : base vs couleur
# ---------------------------------------------------------------------------

def is_base(name: str, s: float, l: float) -> bool:
    """True si la gamme est un NEUTRE (apte base) — seuil absolu + sémantique."""
    # Sémantique : famille explicitement neutre -> base
    if _contains(name, NEUTRAL_WORDS):
        return True
    # Sémantique : « vif/saturé/franc » interdit la base, même si numériquement bas
    if _contains(name, SATURATED_WORDS):
        return False
    # Numérique
    if s <= S_BASE_MAX or l >= L_BASE_HIGH or l <= L_BASE_LOW:
        return True
    # Sémantique désaturé + luminosité non médiane -> base
    if _contains(name, DESATURATED_WORDS) and (l >= 0.70 or l <= 0.30):
        return True
    return False


# ---------------------------------------------------------------------------
# Classement relatif : accent vs dominante (sur un terrain)
# ---------------------------------------------------------------------------

def rank_aptitudes(terrain: list[dict]) -> list[dict]:
    """terrain = [{"name":..., "hexes":[...]}, ...]
    Retourne la même liste enrichie de {s, l, intensity, aptitude, weak_accent}."""
    enriched = []
    for g in terrain:
        s, l = avg_sl(g.get('hexes', []))
        enriched.append({
            **g, 's': round(s, 3), 'l': round(l, 3),
            'intensity': round(intensity(s, l), 3),
            'is_base': is_base(g['name'], s, l),
        })

    colors = [g for g in enriched if not g['is_base']]
    if colors:
        max_i = max(g['intensity'] for g in colors)
        threshold = ACCENT_TIER * max_i if max_i > 0 else 0
        for g in colors:
            g['aptitude'] = 'accent' if g['intensity'] >= threshold and max_i > 0 else 'dominante'
        # Garantir dominante non-vide : s'il y a >=2 couleurs mais toutes en accent,
        # rétrograder la moins intense en dominante.
        accents = [g for g in colors if g['aptitude'] == 'accent']
        doms = [g for g in colors if g['aptitude'] == 'dominante']
        if len(colors) >= 2 and not doms:
            least = min(accents, key=lambda g: g['intensity'])
            least['aptitude'] = 'dominante'
        # Marquer un accent faible (advisory energy_survival)
        for g in colors:
            if g['aptitude'] == 'accent':
                g['weak_accent'] = g['intensity'] < ACCENT_WEAK_INTENSITY
    for g in enriched:
        if g['is_base']:
            g['aptitude'] = 'base'
            g['weak_accent'] = False
        g.setdefault('weak_accent', False)
    return enriched


# ---------------------------------------------------------------------------
# Mode calibration : lire le catalogue, classer chaque sous-gamme
# ---------------------------------------------------------------------------

def parse_catalogue(md: str) -> list[dict]:
    """Extrait (nom, hexes) de chaque ligne `- **Nom** — desc (ex: `#xxxxxx`, `#yyyyyy`)`."""
    out = []
    for line in md.splitlines():
        m = re.match(r'\s*-\s+\*\*(.+?)\*\*\s*(.*)', line)
        if not m:
            continue
        name = m.group(1).strip()
        rest = m.group(2)
        hexes = re.findall(r'#[0-9a-fA-F]{6}', rest)
        if not hexes:
            continue  # ignore les puces d'intro / sans échantillon (bruit de parsing)
        # nom + reste pour la détection sémantique
        out.append({'name': f"{name} {rest}", 'short': name, 'hexes': hexes})
    return out


def run_calibrate(catalogue_path: Path) -> int:
    entries = parse_catalogue(catalogue_path.read_text(encoding='utf-8'))
    if not entries:
        print("Aucune sous-gamme parsée — vérifier le format du catalogue.", file=sys.stderr)
        return 2
    print(f"\n=== CALIBRATION derive_aptitude — {len(entries)} sous-gammes ===\n")
    print(f"{'sous-gamme':<52} {'S':>5} {'L':>5} {'int':>5}  {'base?':<6} {'sémantique':<12} conflit")
    print("-" * 110)
    conflicts = 0
    for e in entries:
        s, l = avg_sl(e['hexes'])
        i = intensity(s, l)
        base = is_base(e['name'], s, l)
        # Attendu sémantique d'après le descripteur
        if _contains(e['name'], SATURATED_WORDS):
            sem = 'saturé'
        elif _contains(e['name'], DESATURATED_WORDS) or _contains(e['name'], NEUTRAL_WORDS):
            sem = 'désat/neutre'
        else:
            sem = '—'
        # Conflit : sémantique saturé mais classé base, ou sémantique désat mais couleur très intense
        conflict = ''
        if sem == 'saturé' and base:
            conflict = '⚠ saturé→base'
            conflicts += 1
        # Seuil 0.50 : une terre moyenne (ocre/terracotta ~S0.40) nommée « désaturée »
        # est une dominante légitime, pas un conflit. On ne flague qu'un « désaturé »
        # réellement vif (contradiction franche).
        if sem == 'désat/neutre' and not base and i > 0.50:
            conflict = '⚠ désat→couleur intense'
            conflicts += 1
        label = (e['short'][:50])
        nhex = len(e['hexes'])
        flag = f"{nhex}hex" if nhex else "0hex!"
        print(f"{label:<52} {s:>5.2f} {l:>5.2f} {i:>5.2f}  {('BASE' if base else 'coul'):<6} {sem:<12} {conflict}  {flag}")
    print("-" * 110)
    print(f"\n{conflicts} conflit(s) sémantique/numérique. Cible : 0 (ajuster seuils si >2).\n")
    return 0


def run_json(terrain_path: Path) -> int:
    terrain = json.loads(terrain_path.read_text(encoding='utf-8'))
    result = rank_aptitudes(terrain)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--calibrate', help='Chemin du catalogue .md à calibrer')
    ap.add_argument('--json', dest='json_terrain', help='Chemin d\'un terrain JSON [{name,hexes}]')
    args = ap.parse_args()
    if args.calibrate:
        return run_calibrate(Path(args.calibrate))
    if args.json_terrain:
        return run_json(Path(args.json_terrain))
    ap.print_help()
    return 2


if __name__ == '__main__':
    sys.exit(main())
