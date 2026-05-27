#!/usr/bin/env python3
"""
Phase 3B-0a Gamut Router Anti-Slop Gate

Vérifie le markdown produit par le routeur chromatique (3B-0a) sur 9 checks :
  7 FAIL stricts (erreurs structurelles ou règles déjà imposées au prompt)
  2 TAG-or-FAIL (zone violet/indigo, neutres pas orientés)
    - Si gamme qualifiée + tag [SLOP_RISQUE] présent → PASS
    - Si gamme qualifiée mais tag absent       → PASS_WITH_PATCH (l'orchestrateur injecte le tag)
    - Si gamme NON qualifiée                   → FAIL (resume du routeur)

Usage :
  python3 phase3b-gamut-router-anti-slop.py <chromatic-gamuts.md> [--json-output]

Exit codes :
  0 = PASS (aucune violation, aucun patch requis)
  0 = PASS_WITH_PATCH si le seul problème est l'oubli d'un tag (l'orchestrateur patche)
  1 = FAIL (violations structurelles, resume du routeur nécessaire)
  2 = ERREUR fichier
"""

import json
import re
import sys


# ---------------------------------------------------------------------------
# Vocabulaire (listes nominatives — vivent ici, jamais dans le prompt)
# ---------------------------------------------------------------------------

# Mots-clés zone violet/indigo (training-defaults LLM)
PURPLE_INDIGO_TRIGGERS = [
    'violet', 'violets', 'violette', 'violettes',
    'indigo', 'indigos',
    'purple', 'purples',
    'lavande', 'lavandes',
    'mauve', 'mauves',
    'parme',
    'aubergine',
    'lilas',
]

# Qualificatifs anti-cousin acceptables pour la zone violet/indigo
PURPLE_INDIGO_QUALIFIERS = [
    'shifted',
    'désaturé', 'desature', 'desaturé',
    'magenta-', 'magenta shifted',
    'pas indigo', 'non indigo',
    'pas saas', 'non saas',
    'pas tailwind', 'non tailwind',
    'pas ai', 'non ai',
    'pas générique', 'non générique', 'pas generique',
    'profond', 'profonds', 'profonde', 'profondes',
    'éteint', 'eteint', 'éteinte', 'éteintes',
    'sourd', 'sourds', 'sourde', 'sourdes',
    'encre', 'd\'encre',
]

# Mots-clés neutres non orientés (forme "pure")
UNQUALIFIED_NEUTRAL_PATTERNS = [
    r'\bgris\s+neutres?\b',
    r'\bblancs?\s+purs?\b',
    r'\bnoirs?\s+purs?\b',
    r'\bpure\s+white\b',
    r'\bpure\s+black\b',
    r'#000(000)?\b',
    r'#fff(fff)?\b',
    r'#FFF(FFF)?\b',
]

# Qualificatifs d'orientation acceptables pour les neutres
NEUTRAL_ORIENTATION_QUALIFIERS = [
    'crémeux', 'cremeux',
    'ardoise',
    'bleu nuit',
    'tirant vers',
    'légèrement teinté', 'legerement teinte',
    'off-white', 'off-black',
    'ocre', 'ocrés',
    'sable',
    'ivoire',
    'craie',
    'graphite',
    'anthracite',
    'pierre',
    'cendré', 'cendre',
    'taupe',
    'teinté', 'teinte',
    'chaud', 'froid',  # autorisé dans neutres orientés (≠ températures bannies dans le NOM de gamme)
]

# Mots de température bannis dans les noms de gammes (règle déjà au prompt)
BANNED_TEMPERATURE_WORDS_IN_NAMES = [
    'chaud', 'chauds', 'chaude', 'chaudes',
    'froid', 'froids', 'froide', 'froides',
    'neutre', 'neutres',  # le mot exact "neutre" en isolation = banni
    'température', 'temperature',
    'tiède', 'tiedes', 'tiede',
    'warm',
    'cool',
]

# Mots de restriction de rôle interdits
ROLE_RESTRICTION_PATTERNS = [
    r'\baccent\s+uniquement\b',
    r'\bsecondaire\s+uniquement\b',
    r'\bdominante\s+uniquement\b',
    r'\bprimaire\s+uniquement\b',
    r'\bonly\s+for\s+accent\b',
]

# Phrases génériques bannies dans les justifications
GENERIC_JUSTIFICATION_PATTERNS = [
    r'\bton\s+moderne\b',
    r'\bton\s+élégant\b', r'\bton\s+elegant\b',
    r'\bton\s+universel\b',
    r'\bdans\s+l[\'’]?\s*air\s+du\s+temps\b',
    r'\bconvient\s+bien\b',
    r'\bfonctionne\s+bien\b',
    r'\bbon\s+choix\s+en\s+général\b', r'\bbon\s+choix\s+en\s+general\b',
    r'\bvaleur\s+sûre\b', r'\bvaleur\s+sure\b',
    r'\bton\s+épuré\b', r'\bton\s+epure\b',
]

# Qualificatifs de spécificité (au moins un attendu si nom < 3 mots)
SPECIFICITY_QUALIFIERS = [
    'saturé', 'saturée', 'saturés', 'saturées', 'sature',
    'désaturé', 'desature', 'désaturée', 'desaturee',
    'profond', 'profonds', 'profonde', 'profondes',
    'clair', 'claire', 'clairs', 'claires',
    'sombre', 'sombres',
    'éteint', 'eteint', 'éteinte', 'eteinte',
    'lumineux', 'lumineuse', 'lumineuses',
    'poudré', 'poudre', 'poudrée', 'poudreuse',
    'pâle', 'pale', 'pâles', 'pales',
    'vif', 'vifs', 'vive', 'vives',
    'doux', 'douce', 'douces',
    'sourd', 'sourds', 'sourde', 'sourdes',
    'mat', 'mate', 'mats', 'mates',
    'crémeux', 'cremeux',
    'forêt', 'foret',
    'marine',
    'minéral', 'mineral', 'minérale', 'minerale',
    'organique',
    'tirant',
    'shifted',
    'magenta-',
    'd\'encre', 'encre',
    'velouté', 'veloute',
]


# ---------------------------------------------------------------------------
# Parser markdown
# ---------------------------------------------------------------------------

def parse_markdown(content: str) -> dict:
    """Extrait les sections clés du markdown du routeur."""
    result = {
        'has_main_header': bool(re.search(r'##\s+Gammes\s+chromatiques', content, re.IGNORECASE)),
        'has_keywords_section': bool(re.search(r'\*\*Mots-clés\s+dominants\s+analysés\*\*', content, re.IGNORECASE)),
        'has_authorized_section': bool(re.search(r'\*\*Gammes\s+autorisées\*\*', content, re.IGNORECASE)),
        'has_excluded_section': bool(re.search(r'\*\*Gammes\s+exclues\*\*', content, re.IGNORECASE)),
        'has_non_applicable_section': bool(re.search(r'\*\*Gammes\s+non\s+applicables\*\*', content, re.IGNORECASE)),
        'has_accent_mention': bool(re.search(r'\*\*Accent\*\*\s*:\s*libre', content, re.IGNORECASE)),
        'authorized_rows': [],
        'excluded_rows': [],
        'non_applicable_rows': [],
    }

    # Extraction du tableau "Gammes autorisées"
    auth_match = re.search(
        r'\*\*Gammes\s+autorisées\*\*\s*:?.*?\n\s*\|.*?\|.*?\n\s*\|[-: |]+\|.*?\n((?:\s*\|.*?\|.*?\n)+)',
        content, re.IGNORECASE | re.DOTALL
    )
    if auth_match:
        result['authorized_rows'] = parse_table_rows(auth_match.group(1), expected_cols=3)

    # Extraction du tableau "Gammes exclues"
    excl_match = re.search(
        r'\*\*Gammes\s+exclues\*\*\s*:?.*?\n\s*\|.*?\|.*?\n\s*\|[-: |]+\|.*?\n((?:\s*\|.*?\|.*?\n)+)',
        content, re.IGNORECASE | re.DOTALL
    )
    if excl_match:
        result['excluded_rows'] = parse_table_rows(excl_match.group(1), expected_cols=2)

    # Extraction du tableau "Gammes non applicables" (mode exhaustif)
    na_match = re.search(
        r'\*\*Gammes\s+non\s+applicables\*\*\s*:?.*?\n\s*\|.*?\|.*?\n\s*\|[-: |]+\|.*?\n((?:\s*\|.*?\|.*?\n)+)',
        content, re.IGNORECASE | re.DOTALL
    )
    if na_match:
        result['non_applicable_rows'] = parse_table_rows(na_match.group(1), expected_cols=2)

    # Détection des colonnes hors format (Usage, Rôle, etc.)
    extra_col_match = re.search(
        r'\|\s*Gamme\s*\|\s*Raison\s*\|\s*Source\s*\|\s*([A-Za-zÀ-ÿ]+)',
        content, re.IGNORECASE
    )
    result['has_extra_column'] = bool(extra_col_match)

    return result


def parse_table_rows(table_block: str, expected_cols: int) -> list[dict]:
    """Parse les lignes d'un tableau markdown.

    expected_cols=3 : Gamme | Raison | Source (autorisées)
    expected_cols=2 : Gamme | Raison (exclues)
    """
    rows = []
    for line_num, line in enumerate(table_block.strip().split('\n'), 1):
        line = line.strip()
        if not line.startswith('|'):
            continue
        # Splitter et nettoyer
        cells = [c.strip() for c in line.split('|')]
        # Enlever les cellules vides aux extrémités (artefacts de | début/fin)
        cells = [c for c in cells if c != '']
        if len(cells) < 2:
            continue
        if expected_cols == 3 and len(cells) >= 3:
            rows.append({
                'line_in_table': line_num,
                'gamut': cells[0],
                'reason': cells[1],
                'source': cells[2],
            })
        elif expected_cols == 2 and len(cells) >= 2:
            rows.append({
                'line_in_table': line_num,
                'gamut': cells[0],
                'reason': cells[1],
            })
    return rows


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize(s: str) -> str:
    """Lowercase + remove accents-light + strip."""
    s = s.lower().strip()
    return s


def contains_any(text: str, needles: list[str]) -> tuple[bool, str]:
    """Vrai si text contient au moins un des needles (insensible à la casse). Retourne le needle trouvé."""
    text_norm = normalize(text)
    for needle in needles:
        if normalize(needle) in text_norm:
            return True, needle
    return False, ''


def jaccard_similarity(a: str, b: str) -> float:
    """Similarité Jaccard entre deux strings au niveau des tokens."""
    set_a = set(re.findall(r'\w+', normalize(a)))
    set_b = set(re.findall(r'\w+', normalize(b)))
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


# ---------------------------------------------------------------------------
# Checks (FAIL strict)
# ---------------------------------------------------------------------------

def check_format_strict(parsed: dict) -> list[dict]:
    """Check 1 : sections obligatoires présentes (mode exhaustif : 3 sections + accent)."""
    violations = []
    missing = []
    if not parsed['has_main_header']:
        missing.append('## Gammes chromatiques (routeur)')
    if not parsed['has_keywords_section']:
        missing.append('**Mots-clés dominants analysés**')
    if not parsed['has_authorized_section']:
        missing.append('**Gammes autorisées**')
    if not parsed['has_excluded_section']:
        missing.append('**Gammes exclues**')
    if not parsed['has_non_applicable_section']:
        missing.append('**Gammes non applicables**')
    if not parsed['has_accent_mention']:
        missing.append('**Accent** : libre')
    if missing:
        violations.append({
            'check': 'format_strict',
            'severity': 'FAIL',
            'detail': f"Sections obligatoires manquantes : {', '.join(missing)}",
        })
    if parsed.get('has_extra_column'):
        violations.append({
            'check': 'format_strict',
            'severity': 'FAIL',
            'detail': "Colonne supplémentaire détectée après 'Source' (Usage / Rôle / etc.). Format strict : 3 colonnes seulement (Gamme | Raison | Source).",
        })
    return violations


def check_no_temperature_words_in_names(parsed: dict) -> list[dict]:
    """Check 2 : pas de mots-températures dans les noms de gammes."""
    violations = []
    all_rows = parsed['authorized_rows'] + parsed['excluded_rows']
    for row in all_rows:
        gamut_name = row['gamut']
        gamut_norm = normalize(gamut_name)
        # On regarde mot par mot pour éviter les faux positifs (ex: "fraîcheur" contient "frai")
        words = re.findall(r"[\wÀ-ÿ']+", gamut_norm)
        for banned in BANNED_TEMPERATURE_WORDS_IN_NAMES:
            if normalize(banned) in words:
                violations.append({
                    'check': 'no_temperature_words',
                    'severity': 'FAIL',
                    'detail': f"Mot-température '{banned}' dans le nom de gamme : '{gamut_name}'. Règle : ne JAMAIS transmettre 'chaud/froid/neutre/température' dans l'output.",
                })
                break  # un seul flag par gamme
    return violations


def check_min_specificity(parsed: dict) -> list[dict]:
    """Check 5 : nom de gamme < 3 mots ET sans qualificatif → FAIL."""
    violations = []
    for row in parsed['authorized_rows'] + parsed['excluded_rows']:
        name = row['gamut']
        # Compter les mots
        words = re.findall(r"[\wÀ-ÿ']+", name)
        if len(words) >= 3:
            continue
        # Vérifier si un qualificatif est présent
        has_qualifier, _ = contains_any(name, SPECIFICITY_QUALIFIERS)
        if not has_qualifier:
            violations.append({
                'check': 'min_specificity',
                'severity': 'FAIL',
                'detail': f"Nom de gamme insuffisamment spécifique : '{name}'. Au moins 3 mots OU un qualificatif (saturé/désaturé/profond/clair/sombre/lumineux/etc.).",
            })
    return violations


def check_no_role_restrictions(parsed: dict, content: str) -> list[dict]:
    """Check 6 : pas de mentions 'accent uniquement', 'secondaire uniquement', etc."""
    violations = []
    for pattern in ROLE_RESTRICTION_PATTERNS:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for m in matches:
            line_num = content[:m.start()].count('\n') + 1
            violations.append({
                'check': 'no_role_restrictions',
                'severity': 'FAIL',
                'detail': f"Restriction de rôle détectée ligne {line_num} : '{m.group(0)}'. Toute gamme autorisée est utilisable pour TOUT rôle — c'est le designer qui décide.",
            })
    return violations


def check_no_duplicate_gamuts(parsed: dict) -> list[dict]:
    """Check 7 : doublons déguisés (Jaccard > 0.5 entre noms de gammes)."""
    violations = []
    auth_rows = parsed['authorized_rows']
    seen = []
    for i, row in enumerate(auth_rows):
        for j in range(i):
            sim = jaccard_similarity(row['gamut'], auth_rows[j]['gamut'])
            if sim > 0.5:
                violations.append({
                    'check': 'no_duplicate_gamuts',
                    'severity': 'FAIL',
                    'detail': f"Doublon déguisé probable : '{row['gamut']}' ressemble à '{auth_rows[j]['gamut']}' (similarité {sim:.0%}). Fusionne en une seule gamme bien décrite.",
                })
                break
    return violations


def check_justification_present(parsed: dict) -> list[dict]:
    """Check 9 : raison non vide pour chaque ligne."""
    violations = []
    for row in parsed['authorized_rows'] + parsed['excluded_rows']:
        if not row.get('reason') or len(row['reason'].strip()) < 5:
            violations.append({
                'check': 'justification_present',
                'severity': 'FAIL',
                'detail': f"Raison vide ou trop courte pour la gamme '{row['gamut']}'.",
            })
    return violations


def check_no_inflation(parsed: dict) -> list[dict]:
    """Check 10 (mode exhaustif) : pas plus de 18 autorisées (anti-complaisance).

    Le mode exhaustif force le routeur à classer toutes les sous-gammes du catalogue.
    Risque de complaisance : mettre "autorisée" par défaut sur les marginales / cousines.
    Si > 18 autorisées (incluant [SECTORIEL]), le routeur doit reclasser les moins
    pertinentes en non applicables — elles serviront de réserve d'arbitrage utilisateur.
    """
    violations = []
    auth_count = len(parsed['authorized_rows'])
    if auth_count > 18:
        violations.append({
            'check': 'no_inflation',
            'severity': 'FAIL',
            'detail': (
                f"Inflation des autorisées : {auth_count} sous-gammes (max 18). "
                f"Le routeur a classé trop de cousines / marginales en autorisées par complaisance. "
                f"Reclasse les moins essentielles en non applicables (cible : 10-15) — "
                f"elles serviront de réserve d'arbitrage à l'utilisateur."
            ),
        })
    return violations


def check_min_coverage(parsed: dict) -> list[dict]:
    """Check 11 (mode exhaustif) : couverture minimale du spectre.

    Garantit que le routeur a vraiment scanné le catalogue exhaustivement.
    Le catalogue contient ~45 sous-gammes ; on tolère des fusions et regroupements
    mais on exige au minimum 30 sous-gammes catégorisées au total.
    """
    violations = []
    total = len(parsed['authorized_rows']) + len(parsed['excluded_rows']) + len(parsed['non_applicable_rows'])
    if total < 30:
        violations.append({
            'check': 'min_coverage',
            'severity': 'FAIL',
            'detail': (
                f"Couverture insuffisante du spectre : {total} sous-gammes catégorisées au total "
                f"(autorisées + exclues + non applicables). Minimum attendu : 30. "
                f"Le routeur a probablement sauté des entrées du catalogue — re-scanne ligne par ligne."
            ),
        })
    return violations


def check_justification_non_generic(parsed: dict) -> list[dict]:
    """Check 8 : justifications génériques bannies."""
    violations = []
    for row in parsed['authorized_rows'] + parsed['excluded_rows']:
        reason = row.get('reason', '')
        for pattern in GENERIC_JUSTIFICATION_PATTERNS:
            if re.search(pattern, reason, re.IGNORECASE):
                violations.append({
                    'check': 'justification_non_generic',
                    'severity': 'FAIL',
                    'detail': f"Justification générique pour '{row['gamut']}' : '{reason}'. Cite un mot-clé territoire spécifique au lieu de phrases passe-partout.",
                })
                break
    return violations


# ---------------------------------------------------------------------------
# Checks (TAG-or-FAIL : zone violet/indigo + neutres non orientés)
# ---------------------------------------------------------------------------

def check_purple_indigo_handling(parsed: dict) -> tuple[list[dict], list[dict]]:
    """Check 3 : zone violet/indigo qualifiée + tag [SLOP_RISQUE].

    Retourne (violations_FAIL, patches_à_appliquer).
    - Si gamme contient violet/indigo/purple ET non qualifiée → FAIL
    - Si qualifiée mais tag [SLOP_RISQUE] absent → patch (l'orchestrateur ajoute le tag)
    - Si qualifiée et taggée → PASS
    """
    violations = []
    patches = []
    for row in parsed['authorized_rows']:
        name = row['gamut']
        source = row.get('source', '')
        # Détecte si la gamme touche la zone violet/indigo
        triggered, trigger_word = contains_any(name, PURPLE_INDIGO_TRIGGERS)
        if not triggered:
            continue
        # La gamme touche la zone — vérifier qualification
        has_qualifier, _ = contains_any(name, PURPLE_INDIGO_QUALIFIERS)
        has_slop_tag = '[SLOP_RISQUE]' in source

        if not has_qualifier:
            violations.append({
                'check': 'purple_indigo_handling',
                'severity': 'FAIL',
                'detail': (
                    f"Gamme '{name}' touche la zone violet/indigo (mot-clé '{trigger_word}') "
                    f"mais n'est PAS qualifiée. Ajoute une contrainte d'écart explicite "
                    f"(ex: 'magenta-shifted', 'profond désaturé', 'pas indigo SaaS') ET "
                    f"le tag [SLOP_RISQUE] dans la colonne Source."
                ),
            })
        elif not has_slop_tag:
            patches.append({
                'gamut': name,
                'current_source': source,
                'patched_source': source.strip() + ' [SLOP_RISQUE]',
                'reason': f"Zone violet/indigo qualifiée mais tag [SLOP_RISQUE] manquant",
            })
    return violations, patches


def check_unqualified_neutrals(parsed: dict) -> tuple[list[dict], list[dict]]:
    """Check 4 : neutres orientés, jamais purs.

    Retourne (violations_FAIL, patches_à_appliquer).
    """
    violations = []
    patches = []
    for row in parsed['authorized_rows']:
        name = row['gamut']
        source = row.get('source', '')
        name_norm = normalize(name)
        triggered = False
        trigger_match = ''
        for pattern in UNQUALIFIED_NEUTRAL_PATTERNS:
            m = re.search(pattern, name_norm, re.IGNORECASE)
            if m:
                triggered = True
                trigger_match = m.group(0)
                break
        if not triggered:
            continue
        # La gamme touche la zone neutre pure — vérifier orientation
        has_orientation, _ = contains_any(name, NEUTRAL_ORIENTATION_QUALIFIERS)
        has_slop_tag = '[SLOP_RISQUE]' in source

        if not has_orientation:
            violations.append({
                'check': 'unqualified_neutrals',
                'severity': 'FAIL',
                'detail': (
                    f"Gamme neutre '{name}' (déclencheur : '{trigger_match}') sans orientation chromatique. "
                    f"Précise la direction (ex: 'gris tirant vers l'ardoise', 'off-whites légèrement crémeux', "
                    f"'off-blacks tirant vers le bleu nuit') ET ajoute [SLOP_RISQUE] dans la colonne Source. "
                    f"Pas de pure black/white/gray."
                ),
            })
        elif not has_slop_tag:
            patches.append({
                'gamut': name,
                'current_source': source,
                'patched_source': source.strip() + ' [SLOP_RISQUE]',
                'reason': f"Neutre orienté mais tag [SLOP_RISQUE] manquant",
            })
    return violations, patches


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

ALL_FAIL_CHECKS = [
    ('format_strict', check_format_strict, False),       # (name, fn, needs_content_param)
    ('no_temperature_words', check_no_temperature_words_in_names, False),
    ('min_specificity', check_min_specificity, False),
    ('no_role_restrictions', check_no_role_restrictions, True),
    ('no_duplicate_gamuts', check_no_duplicate_gamuts, False),
    ('justification_present', check_justification_present, False),
    ('justification_non_generic', check_justification_non_generic, False),
    ('no_inflation', check_no_inflation, False),         # mode exhaustif
    ('min_coverage', check_min_coverage, False),         # mode exhaustif
]


def main():
    json_output = '--json-output' in sys.argv
    args = [a for a in sys.argv[1:] if a != '--json-output']

    if len(args) < 1:
        print("Usage: python3 phase3b-gamut-router-anti-slop.py <chromatic-gamuts.md> [--json-output]")
        sys.exit(2)

    filepath = args[0]
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erreur: fichier introuvable — {filepath}")
        sys.exit(2)

    parsed = parse_markdown(content)

    # Collecter toutes les violations
    all_violations = []
    for name, fn, needs_content in ALL_FAIL_CHECKS:
        if needs_content:
            all_violations.extend(fn(parsed, content))
        else:
            all_violations.extend(fn(parsed))

    # Checks tag-or-fail
    purple_violations, purple_patches = check_purple_indigo_handling(parsed)
    neutral_violations, neutral_patches = check_unqualified_neutrals(parsed)
    all_violations.extend(purple_violations)
    all_violations.extend(neutral_violations)
    all_patches = purple_patches + neutral_patches

    # Verdict
    if all_violations:
        verdict = 'FAIL'
        exit_code = 1
    elif all_patches:
        verdict = 'PASS_WITH_PATCH'
        exit_code = 0
    else:
        verdict = 'PASS'
        exit_code = 0

    # Output
    if json_output:
        output = {
            'verdict': verdict,
            'file': filepath,
            'violations': all_violations,
            'patches': all_patches,
            'authorized_count': len(parsed['authorized_rows']),
            'excluded_count': len(parsed['excluded_rows']),
            'non_applicable_count': len(parsed['non_applicable_rows']),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        sys.exit(exit_code)

    # Sortie human-readable
    filename = filepath.rsplit('/', 1)[-1] if '/' in filepath else filepath
    print(f"\n=== PHASE 3B-0a GAMUT ROUTER ANTI-SLOP GATE ===")
    print(f"File: {filename}")
    print(f"Authorized: {len(parsed['authorized_rows'])}  |  Excluded: {len(parsed['excluded_rows'])}  |  Non-applicable: {len(parsed['non_applicable_rows'])}")
    print()

    if all_violations:
        # Grouper par check
        by_check: dict[str, list] = {}
        for v in all_violations:
            by_check.setdefault(v['check'], []).append(v)

        print(f"[FAIL] {len(all_violations)} violation(s) dans {len(by_check)} catégorie(s) :\n")
        for check, instances in sorted(by_check.items()):
            print(f"  ❌ {check} ({len(instances)}x)")
            for inst in instances[:5]:
                print(f"     {inst['detail']}")
            if len(instances) > 5:
                print(f"     ... et {len(instances) - 5} autre(s)")
            print()

    if all_patches:
        print(f"[PATCH] {len(all_patches)} tag(s) [SLOP_RISQUE] à injecter (omission triviale, l'orchestrateur patche) :\n")
        for p in all_patches:
            print(f"  🟡 Gamme : {p['gamut']}")
            print(f"     Raison : {p['reason']}")
            print(f"     Source actuelle : '{p['current_source']}'")
            print(f"     Source patchée  : '{p['patched_source']}'")
            print()

    print(f"VERDICT: {verdict}")
    if verdict == 'FAIL':
        print("→ Resume du routeur avec ces violations en feedback.")
    elif verdict == 'PASS_WITH_PATCH':
        print("→ L'orchestrateur peut patcher silencieusement, pas de resume nécessaire.")
    else:
        print("→ Sortie du routeur conforme aux 9 checks anti-slop.")

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
