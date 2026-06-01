#!/usr/bin/env python3
"""
render_divergence.py — Génère MÉCANIQUEMENT la directive de divergence pour la
variante en cours, à partir des palettes déjà produites + du bucket. AUCUN texte
libre esthétique, AUCUNE suggestion de teinte/mode (pas de « bascule sombre »).

POURQUOI : avant ce script, la directive était rédigée à la main → l'orchestrateur
soufflait des réponses (familles, mode) et contaminait le test. L'app doit refléter
le système autonome de BIG.

La divergence est rendue CONCRÈTE (pas seulement « ≥N leviers », auto-jugé sur des
labels) par 3 leviers mécaniques :
  1. Familles de bucket encore INEXPLOITÉES → à privilégier pour Primary/Secondary
     (empêche de repiquer la même famille pendant que d'autres dorment).
  2. Accents déjà pris (hex listés) → le nouvel accent doit s'en démarquer
     VISIBLEMENT (zone de teinte ≠ OU saturation franchement ≠), pas par un renommage.
  3. Clause terrain épuisé → si toutes les familles dominantes sont prises, interdit
     de répéter à l'identique : diverger fort sur mode/saturation/harmonie/accent.

Règle dégressive (cf. ORCHESTRATION) : seuil = max(1, 6 - position). V2 ≥4 … V5 ≥1.

Usage :
  python3 render_divergence.py --prev <V1.md> [<V2.md> …] --buckets <01-buckets.md> --output <div.md>
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROLES = ['Primary', 'Secondary', 'Accent', 'Bg dark', 'Bg light', 'Text primary', 'Text secondary']

# noyaux de familles du catalogue (pour matcher bucket <-> gammes déclarées)
CORES = [
    'bleus marine', 'bleus profonds désaturés', 'bleus pétrole', 'bleus ciels', 'bleus ai',
    'cyans saturés', 'cyans désaturés', 'verts vifs', 'verts forêts', 'verts olives', 'verts mousse',
    'rouges saturés vifs', 'rouges profonds bordeaux', 'rouges désaturés',
    'oranges saturés vifs', 'oranges désaturés', 'oranges brûlés',
    'jaunes vifs', 'jaunes profonds safran', 'jaunes pâles',
    'bruns encre', 'ocres terreux', 'terracotta', 'brun-rouille',
    'beiges sables', 'cuivres', 'or vieilli', 'argent',
]


def core(name: str) -> str | None:
    n = name.lower()
    for c in CORES:
        if c in n:
            return c
    return None


def extract_params(content: str) -> str:
    m = re.search(r'\*\*PARAM[ÈE]TRES\*\*\s*:?\s*(.+)', content, re.I)
    return m.group(1).strip() if m else '(paramètres non déclarés)'


def extract_mode(content: str) -> str | None:
    m = re.search(r'Mode\s+fond\s+dominant[\s:*]*(SOMBRE|CLAIR)', content, re.I)
    return m.group(1).upper() if m else None


def extract_role(content: str, role: str):
    m = re.search(r'\|\s*' + re.escape(role) + r'\s*\|\s*([^|]+?)\s*\|\s*`?(#[0-9a-fA-F]{6})`?', content, re.I)
    return (m.group(1).strip(), m.group(2)) if m else (None, None)


def extract_hexes_line(content: str) -> str:
    out = []
    for role in ROLES:
        nm, hx = extract_role(content, role)
        if hx:
            out.append(f"{role} {hx}")
    return ' · '.join(out)


def declared_dominante_cores(content: str) -> set[str]:
    """Familles (noyaux) utilisées en Primary/Secondary par une palette, via la ligne « Dominantes »."""
    m = re.search(r'\*\*Dominantes[^\n]*\*\*\s*:?(.+?)(?:\n\s*\*\*|\n\s*##|\n\s*\n)', content, re.S | re.I)
    found = set()
    if m:
        seg = m.group(1).split('\n')[0]
        for part in re.split(r'\s*[×+·]\s*|\s+et\s+', seg):
            c = core(part)
            if c:
                found.add(c)
    # filet : si la ligne déclare mal, on retombe sur les noms de rôle Primary/Secondary
    if not found:
        for r in ('Primary', 'Secondary'):
            nm, _ = extract_role(content, r)
            if nm:
                c = core(nm)
                if c:
                    found.add(c)
    return found


HARD_EXCL_KW = ['contredit', 'contradiction', 'contre-tempér', 'contre-temp', 'alarmiste',
                'déplacé auto', 'marqueur slop', 'ai-tell', 'slop', 'clinquant', 'opposé']


def hard_excluded_labels(grid_path) -> list[str]:
    """Noms de gammes exclues par le routeur pour raison DURE (contradiction/slop/contre-température).
    L'accent, bien que libre, ne doit PAS y piocher (≠ exclusions « non évoqué »)."""
    if not grid_path or not Path(grid_path).exists():
        return []
    c = Path(grid_path).read_text(encoding='utf-8')
    m = re.search(r'###\s+Gammes\s+exclues(.+?)(?:\n\*\*|\n##\s|\Z)', c, re.S | re.I)
    out = []
    if not m:
        return out
    for line in m.group(1).splitlines():
        s = line.strip()
        if not s.startswith('|'):
            continue
        cells = [x.strip() for x in s.strip('|').split('|')]
        if len(cells) < 2 or cells[0].lower().startswith('gamme') or set(cells[0]) <= set('- '):
            continue
        if any(k in cells[1].lower() for k in HARD_EXCL_KW):
            out.append(cells[0])
    return out


def bucket_families(buckets_path: Path):
    """{'DOMINANTE':[(label, core)], 'ACCENT':[(label, core)], 'BASE':[(label, core)]}"""
    c = buckets_path.read_text(encoding='utf-8')
    out = {'DOMINANTE': [], 'ACCENT': [], 'BASE': []}
    for sec in ('DOMINANTE', 'ACCENT', 'BASE'):
        m = re.search(r'### Bucket ' + sec + r'.*?\n(.*?)(?:\n### |\Z)', c, re.S)
        if not m:
            continue
        for line in m.group(1).splitlines():
            mm = re.match(r'\s*-\s*(.+?)\s*(?:—|\[|$)', line)
            if mm:
                label = mm.group(1).strip()
                out[sec].append((label, core(label)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--prev', nargs='+', required=True, help='Palettes précédentes, dans l\'ordre (V1, V2, …)')
    ap.add_argument('--buckets', required=True, help='Chemin du 01-buckets.md du run')
    ap.add_argument('--grid', default=None,
                    help='Chemin du 01-grid.md du routeur (pour interdire à l\'accent les exclusions dures)')
    ap.add_argument('--total', type=int, default=5,
                    help='Nombre total de variantes prévues (pour garantir l\'étalement du mode clair/sombre)')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    prev_files = [Path(p) for p in args.prev]
    for p in prev_files:
        if not p.exists():
            print(f"Introuvable : {p}", file=sys.stderr)
            return 2
    bpath = Path(args.buckets)
    if not bpath.exists():
        print(f"Bucket introuvable : {bpath}", file=sys.stderr)
        return 2

    position = len(prev_files) + 1
    threshold = max(1, 6 - position)

    buckets = bucket_families(bpath)
    dom_fams = buckets['DOMINANTE']

    # comptage d'usage par famille dominante (combien de variantes l'ont prise en Primary/Secondary)
    fam_count: Counter = Counter()
    prev_contents = []
    for p in prev_files:
        c = p.read_text(encoding='utf-8')
        prev_contents.append(c)
        for cr in declared_dominante_cores(c):
            fam_count[cr] += 1
    unused = [(label, cr) for (label, cr) in dom_fams if cr and fam_count.get(cr, 0) == 0]
    overused = [(label, cr) for (label, cr) in dom_fams if cr and fam_count.get(cr, 0) >= 2]

    # étalement du mode : garantir ≥1 CLAIR ET ≥1 SOMBRE sur l'ensemble du set.
    # On ne force RIEN tant que c'est rattrapable ; on n'impose le mode manquant qu'à la
    # DERNIÈRE variante qui peut encore le sauver (intervention minimale, zéro orientation
    # esthétique sur les variantes antérieures).
    seen_modes = {m for m in (extract_mode(c) for c in prev_contents) if m}
    missing_modes = {'CLAIR', 'SOMBRE'} - seen_modes
    slots_incl_current = max(1, args.total - len(prev_files))
    forced_mode = sorted(missing_modes)[0] if (missing_modes and slots_incl_current <= len(missing_modes)) else None

    # accents déjà pris
    prev_accents = []
    for i, c in enumerate(prev_contents, start=1):
        nm, hx = extract_role(c, 'Accent')
        if hx:
            prev_accents.append((i, nm or '', hx))

    L = []
    L.append(f"## DIRECTIVE DE DIVERGENCE — Variante {position} (générée mécaniquement)")
    L.append("")
    L.append(f"Tu produis la **variante {position}** d'une série pour CE MÊME concept. "
             f"{len(prev_files)} variante(s) précédente(s) existe(nt) (paramètres + hex ci-dessous). "
             "Tu composes librement, fidèle au concept et aux buckets (Primary/Secondary ∈ bucket DOMINANTE ; "
             "contrainte sectorielle selon le curseur déjà fournie).")
    L.append("")
    L.append("### Les 5 leviers de divergence")
    L.append("1. **famille** (teinte d'identité) · 2. **mode** (clair / sombre) · "
             "3. **saturation** (vif / éteint) · 4. **harmonie** · 5. **accent**.")
    L.append("")
    L.append("### Exigence (dégressive)")
    if forced_mode:
        L.append(f"**Diffère sur AU MOINS {threshold} des 5 leviers** par rapport à CHACUNE des variantes précédentes.")
    else:
        L.append(f"**Diffère sur AU MOINS {threshold} des 5 leviers** par rapport à CHACUNE des variantes précédentes. "
                 "**Aucun levier n'est imposé ni privilégié** : le mode (clair/sombre) en particulier n'est PAS orienté — "
                 "choisis-le selon ce que le concept appelle, pas pour diverger à tout prix.")
    L.append("")
    # Section étalement du mode
    if forced_mode:
        L.append("### ⚠ MODE IMPOSÉ (étalement du set)")
        L.append(f"Le mode **{forced_mode}** n'est encore apparu dans AUCUNE variante précédente, et c'est la "
                 f"**dernière variante** qui peut encore l'introduire. Pour que le jeu d'options ne soit pas mono-mode, "
                 f"**cette variante DOIT être en mode {forced_mode}** (fond dominant {forced_mode.lower()}). "
                 "Trouve la lecture du concept qui justifie ce mode — elle existe presque toujours "
                 "(un même univers a une face claire et une face sombre). Adapte texte/contraste en conséquence (WCAG).")
        L.append("")
    elif missing_modes:
        miss = sorted(missing_modes)[0]
        L.append("### Mode (info étalement)")
        L.append(f"Le mode **{miss}** n'est pas encore apparu sur le set. Il n'est pas imposé ici (encore rattrapable "
                 "sur une variante ultérieure), mais si le concept s'y prête naturellement, c'est le bon moment de le poser.")
        L.append("")
    L.append("⚠ **« Différent » se juge sur le RENDU, pas sur le label.** Renommer une teinte (« vert forêt » → "
             "« vert clinique ») sans changer l'hex ne compte PAS comme une divergence de famille. Deux variantes "
             "ne doivent pas se ressembler une fois posées côte à côte.")
    L.append("")
    # Levier 1 — familles inexploitées + cap d'usage (Primary ET Secondary distincts et neufs)
    L.append("### Familles dominantes : règle d'usage (Primary ET Secondary)")
    L.append("⚠ **Primary et Secondary doivent venir de DEUX familles différentes**, et **chacune** doit être "
             "choisie en privilégiant les familles encore inexploitées — pas seulement le Primary.")
    if unused:
        L.append("")
        L.append("**Familles INEXPLOITÉES (count 0) — à privilégier pour Primary ET Secondary** :")
        for label, _ in unused:
            L.append(f"- {label}")
    if overused:
        L.append("")
        L.append("**Familles DÉJÀ PRISES 2 fois ou plus — INTERDIT de les reprendre** "
                 "(elles sont saturées, en piocher une 3e fois = répétition) :")
        for label, cr in overused:
            L.append(f"- {label} (déjà {fam_count[cr]}×)")
    L.append("")
    if unused:
        L.append("Règle : sers-toi d'abord dans les inexploitées. Tu ne peux reprendre une famille déjà utilisée "
                 "**qu'une seule fois** (jamais une famille déjà prise 2× — voir interdites), et seulement si aucune "
                 "inexploitée ne sert le rôle. Aucune famille ne doit dépasser 2 usages sur l'ensemble de la série.")
    else:
        L.append("⚠ **Terrain épuisé** (toutes les familles ont déjà servi). NE répète pas une combinaison à "
                 "l'identique et **ne dépasse jamais 2 usages d'une même famille** : prends la famille la MOINS "
                 "utilisée, et diverge FORT sur les autres leviers (mode, saturation, harmonie, accent) + l'hex précis "
                 "(bord de gamme différent).")
    L.append("")
    # Levier 5 — accents déjà pris
    if prev_accents:
        L.append("### Accents déjà utilisés — ton accent doit s'en démarquer VISIBLEMENT")
        for i, nm, hx in prev_accents:
            L.append(f"- V{i} : {hx}" + (f" ({nm})" if nm else ""))
        L.append("Ton accent doit être dans une **zone de teinte différente** OU à **saturation franchement "
                 "différente** de TOUS ceux ci-dessus — pas une variation imperceptible de la même teinte "
                 "(deux accents ne doivent pas être des jumeaux).")
        L.append("")
    # Levier fond/neutres — varier la FAMILLE de base (le fond ne doit pas être identique partout)
    base_fams = [label for (label, _) in buckets.get('BASE', [])]
    prev_bg = []
    for i, c in enumerate(prev_contents, start=1):
        m = extract_mode(c) or '?'
        nm_l, hx_l = extract_role(c, 'Bg light')
        nm_d, hx_d = extract_role(c, 'Bg dark')
        hero = (hx_l, 'Bg light', nm_l) if m == 'CLAIR' else (hx_d, 'Bg dark', nm_d)
        if hero[0]:
            prev_bg.append((i, m, hero[1], hero[0], hero[2] or ''))
    if base_fams:
        L.append("### Fond / neutres — varie la FAMILLE de base (levier de variété)")
        L.append("Le fond (la plus grande surface) ne doit PAS être quasi identique d'une variante à l'autre. "
                 "Pour ton fond dominant (Bg light si mode clair, Bg dark si sombre), choisis une **famille du "
                 "bucket BASE DIFFÉRENTE** de celles déjà prises, PUIS re-teinte-la vers TA dominante (l'écho "
                 "fond↔identité reste). Familles BASE disponibles :")
        for f in base_fams:
            L.append(f"- {f}")
        if prev_bg:
            L.append("")
            L.append("Fonds dominants déjà utilisés (NE les répète pas — prends une autre direction de neutre) :")
            for i, m, role, hx, nm in prev_bg:
                L.append(f"- V{i} [{m}] {role} {hx}" + (f" ({nm})" if nm else ""))
        L.append("")
    # Accent : exclusions DURES interdites (même si l'accent est libre)
    hard_labels = hard_excluded_labels(args.grid)
    if hard_labels:
        L.append("### Accent — gammes INTERDITES même en accent")
        L.append("L'accent est libre, MAIS il ne peut PAS réintroduire une gamme que le routeur a exclue pour une "
                 "raison **DURE** (contradiction franche avec la marque, slop/AI-tell, contre-température). "
                 "Tu peux piocher librement dans les gammes simplement « non évoquées », **jamais** dans celles-ci :")
        for lbl in hard_labels:
            L.append(f"- {lbl}")
        L.append("")
    # Paramètres complets précédents
    L.append("### Paramètres complets des variantes précédentes (à ne pas reproduire)")
    for i, c in enumerate(prev_contents, start=1):
        L.append(f"- **Variante {i}** — {extract_params(c)}")
        hexes = extract_hexes_line(c)
        if hexes:
            L.append(f"  - hex : {hexes}")
    L.append("")
    L.append("### En fin de sortie")
    L.append("Déclare la ligne de traçabilité : "
             "`**PARAMÈTRES** : famille=… · mode=… · saturation=… · harmonie=… · accent=…`")
    L.append("")

    Path(args.output).write_text('\n'.join(L), encoding='utf-8')
    nb_unused = len(unused)
    mode_note = f" — MODE IMPOSÉ : {forced_mode}" if forced_mode else (
        f" — mode manquant (info) : {sorted(missing_modes)[0]}" if missing_modes else " — modes déjà étalés")
    print(f"[OK] divergence V{position} (seuil ≥{threshold}) écrite : {args.output} "
          f"— familles dominantes inexploitées restantes : {nb_unused}{mode_note}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
