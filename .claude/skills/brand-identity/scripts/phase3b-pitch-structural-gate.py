#!/usr/bin/env python3
"""
Phase 3B Pitch Structural Gate — Anti-prescription HTML

Détecte les patterns STRUCTURELS de débordement dans le pitch :
1. Valeurs numériques hors palette (ratios chiffrés, pixels, pourcentages, fourchettes)
2. Sous-sections inventées hors format autorisé
3. Longueurs excessives sur sections cadrées

Approche : patterns formels (regex numériques, headers, mots), AUCUNE liste
de mots créatifs (drop-cap, masthead, etc.) pour éviter la contamination.

Usage:
  python3 phase3b-pitch-structural-gate.py <path/to/pitch.md> [--json-output]

Exit code 0 = PASS
Exit code 1 = FAIL (violations détectées)
Exit code 2 = ERR (fichier introuvable, argument manquant)
"""

import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# CHECK 1 — Valeurs numériques hors palette
# ---------------------------------------------------------------------------

# Patterns problématiques (chiffres précis qui prescrivent du HTML)
NUMERIC_PATTERNS = [
    # Ratios type-scale chiffrés
    (
        r'\b\d+\.\d{2,}\b',
        'ratio chiffré',
        'Le pitch ne prescrit pas de ratio numérique. Phase 4 calibre selon le curseur A.',
    ),
    # Pixels prescriptifs
    (
        r'\b\d+\s*px\b',
        'valeur en pixels',
        'Le pitch décrit la sensation, pas les valeurs en pixels. Phase 4 décide.',
    ),
    # Pourcentages de surface/cadre
    (
        r'\b\d{1,3}\s*%\b(?!\s*(d\'opacité|opacité|de fiabilité|de confiance))',
        'pourcentage de surface',
        'Le pitch dit "vide dominant" / "sujet contenu", pas un pourcentage exact.',
    ),
    # Fourchettes de pourcentages (25-30%, 70-75%)
    (
        r'\b\d{1,3}\s*[-–à]\s*\d{1,3}\s*%',
        'fourchette de pourcentage',
        'Pas de fourchette numérique de cadre. "Vide dominant" / "sujet contenu".',
    ),
    # Fourchettes de nombres (1-3 points, 3-7 traits, 5-7 brins)
    # Exclut les contextes légitimes : "1-2 phrases", "3-5 lignes" qui sont dans le META du pitch
    (
        r'\b(?<![Cc]oncept )(?<!règles )\d+\s*[-–à]\s*\d+\s+(?:points|traits|brins|filaments|halos|capillaires|éléments|signes|conducteurs|ornements|sections|colonnes)\b',
        'fourchette de nombre d\'éléments',
        'Pas de quantité numérique (1-3, 3-7) sur les éléments visuels. "Ponctuels", "rares", "discrets".',
    ),
    # Position spatiale en colonnes
    (
        r'colonnes?\s+\d+\s*[-–]\s*\d+',
        'position en colonnes (X-Y)',
        'Le pitch ne dit pas "colonnes 7-8/12". Phase 4 décide du grid.',
    ),
    # Débordement en X%
    (
        r'(?:déborde|débordement|déborder).{0,30}\d+\s*%',
        'débordement chiffré',
        'Le pitch dit "déborde du cadre", pas "déborde de 20-30%".',
    ),
]

# Skip patterns — sections où certaines valeurs numériques sont légitimes
# Format : (section_name, line_pattern_to_skip)
SKIP_LINE_PATTERNS = [
    # Pastilles couleur HTML inline (légitimes)
    r'<span\s+style=',
    # Calibrage A=1/2/3 du curseur
    r'^\s*Calibrage\s+A=',
    r'^\s*A\s*=\s*[123]',
    # Ligne du heading concept
    r'^##\s+CONCEPT\s+\d+',
    # Spec de format dans les META du prompt (ex: "1-2 phrases MAX")
    r'\d+\s*-\s*\d+\s+(?:phrases?|mots?|lignes?|puces?)',
    # Fonts variables (ex: "axe wght 540")
    r'(?:wght|weight|axe|font-variation)\s*\d+',
    # Multi-vue d'image (4:5, 3:4, 16:9)
    r'\b\d+:\d+\b',
]

# Sections où les chiffres sont attendus (placeholders métier)
# On lit la zone "Données métier clés" jusqu'à la section suivante
SKIP_SECTION_PATTERNS = [
    (r'^\*\*Données\s+métier\s+clés\*\*', r'^\*\*[^*]+\*\*\s*\n', 'Données métier clés'),
    (r'^###\s+\d+\.\s*Ancrage\s+Brief', r'^###?\s+\d+\.', 'Ancrage Brief'),
    (r'^###\s+\d+\.\s*Pont\s+Brief', r'^###?\s+', 'Pont Brief'),
]


# ---------------------------------------------------------------------------
# CHECK 2 — Sous-sections inventées
# ---------------------------------------------------------------------------

# Liste exhaustive des headers autorisés (insensible à la casse)
ALLOWED_HEADERS = [
    # Niveau 2 — sections principales
    'concept',
    'style officiel retenu',
    'ancrage brief',
    'tension résolue',
    'pont brief → créa',
    'pont brief → crea',
    'pont brief',
    'icp ciblé',
    'icp cible',
    'intention créative',
    'intention creative',
    'direction visuelle',
    'carte d\'inspiration',
    'visuels recommandés',
    'graine logo',
    'bénéfices business',
    'benefices business',
    'avis du da',
    # Niveau 3 — sous-sections de Direction visuelle
    'typographie',
    'palette',
    'surface',
    'atmosphère',
    'atmosphere',
    'type-scale',
    'composition voice block',
    'données métier clés',
    'donnees metier cles',
    'philosophie d\'interaction',
    'philosophie d interaction',
    'prescriptions d\'exécution visuelle',
    'prescriptions d execution visuelle',
    'prescriptions d\'execution visuelle',
    'registre de surface',
    'géométrie des formes',
    'geometrie des formes',
    'relief et profondeur',
    'traitement des conteneurs',
    'rythme spatial',
    'registre atmosphérique',
    'registre atmospherique',
    # Niveau 3 — sous-sections de Carte d'Inspiration
    'territoire visuel',
    'secteurs visuellement proches',
    'anti-territoire',
    'anti territoire',
    'voisinage de marques',
    # Niveau 3 — sous-sections de Avis du DA
    'force majeure',
    'risque potentiel',
    'position zag',
    # Niveau 3 — sous-sections de Bénéfices business
    'différenciation',
    'differenciation',
    'icp',
    'zag',
    'scalabilité',
    'scalabilite',
    # Display / Body (sous-typographie)
    'display',
    'body',
    'display — epilogue',
    'body — funnel sans',
    # Conclusion atmosphérique
    'conclusion atmosphérique',
    'conclusion atmospherique',
    'affirmation finale',
    'affirmation de marque',
    # Récapitulatif optionnel
    'récapitulatif comparatif',
    'recapitulatif comparatif',
    'synthèse',
    'synthese',
    'recommandation da',
    # Sous-titres légitimes du Pont Brief → Créa
    'palette',
    'typographie',
    'univers',
    'univers visuel',
    # Numérotation des risques dans Avis du DA (Risque 1, Risque 2, etc.)
    # → traités via SKIP_HEADER_PATTERNS ci-dessous
]


# Patterns de headers à SKIP (légitimes mais variables)
SKIP_HEADER_PATTERNS = [
    r'^\s*\*\*Risque\s+\d+\s*[—–-]',          # **Risque 1 — Nom**
    r'^\s*\*\*\d+\.\s',                        # **1. Nom** (numérotation)
    r'^\s*\*\*\[[^\]]+\]\*\*\s*[:—–]',        # **[Différenciation]** : (Bénéfices business)
]


def normalize_header(text):
    """Normalise un header pour comparaison (lowercase, strip, retire markdown)."""
    text = text.strip()
    # Retirer markdown bold/italic
    text = re.sub(r'^\*+|\*+$', '', text)
    text = re.sub(r'^#+\s*', '', text)
    # Retirer le numéro de section (ex: "1. ")
    text = re.sub(r'^\d+\.\s*', '', text)
    # Retirer le tiret de liste (ex: "a) " ou "- ")
    text = re.sub(r'^[a-z]\)\s*', '', text)
    text = re.sub(r'^-\s*', '', text)
    # Lowercase
    text = text.lower()
    # Retirer les accents pour matching plus robuste
    return text


# ---------------------------------------------------------------------------
# CHECK 3 — Caps de longueur par section
# ---------------------------------------------------------------------------

# Caps de longueur (en mots)
SECTION_CAPS = {
    'composition voice block': 30,
    'type-scale': 60,
    'philosophie d\'interaction': 50,
    'registre atmosphérique': 80,
    'registre atmospherique': 80,
    'registre de surface': 40,
    'géométrie des formes': 40,
    'geometrie des formes': 40,
    'relief et profondeur': 40,
    'traitement des conteneurs': 40,
    'rythme spatial': 40,
    'force majeure': 100,
    'risque potentiel': 200,  # peut lister 1-3 risques avec garde-fous
    'position zag': 100,
}


def count_words(text):
    """Compte le nombre de mots dans un texte (mots = séquences de chars non-espace)."""
    # Retirer les blocs de code inline et les span HTML
    text = re.sub(r'`[^`]*`', ' ', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    # Retirer les puces de liste markdown
    text = re.sub(r'^\s*[-*]\s+', '', text, flags=re.MULTILINE)
    # Retirer markdown bold/italic
    text = re.sub(r'\*+', '', text)
    # Compter les mots
    words = re.findall(r'\S+', text)
    return len(words)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def should_skip_line(line):
    """True si la ligne doit être ignorée par les checks numériques."""
    for pattern in SKIP_LINE_PATTERNS:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False


def find_section_zones(lines, section_start_pattern, section_end_pattern):
    """Retourne les indices (start, end) des zones où chiffres sont autorisés."""
    zones = []
    in_zone = False
    zone_start = None
    for i, line in enumerate(lines):
        if not in_zone and re.search(section_start_pattern, line, re.IGNORECASE):
            in_zone = True
            zone_start = i
        elif in_zone and re.search(section_end_pattern, line, re.IGNORECASE) and i > zone_start + 1:
            zones.append((zone_start, i))
            in_zone = False
    if in_zone:
        zones.append((zone_start, len(lines)))
    return zones


def is_in_skip_zone(line_idx, skip_zones):
    """True si la ligne est dans une zone où les chiffres sont autorisés."""
    for start, end in skip_zones:
        if start <= line_idx < end:
            return True
    return False


# ---------------------------------------------------------------------------
# Checks principaux
# ---------------------------------------------------------------------------


def check_numeric_violations(content):
    """Détecte les valeurs numériques hors palette."""
    violations = []
    lines = content.split('\n')

    # Construire les zones où chiffres sont autorisés (ex: Données métier)
    skip_zones = []
    for start_pat, end_pat, _ in SKIP_SECTION_PATTERNS:
        skip_zones.extend(find_section_zones(lines, start_pat, end_pat))

    for i, line in enumerate(lines):
        if should_skip_line(line):
            continue
        if is_in_skip_zone(i, skip_zones):
            continue

        for pattern, label, hint in NUMERIC_PATTERNS:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                violations.append({
                    'check': 'numeric',
                    'line': i + 1,
                    'pattern': label,
                    'matched': match.group(0).strip(),
                    'context': line.strip()[:120],
                    'hint': hint,
                })

    return violations


def check_invented_subsections(content):
    """Détecte les sous-sections (headers) qui ne sont pas dans la liste autorisée."""
    violations = []
    lines = content.split('\n')

    # Headers à détecter : ## XXX, ### XXX, **XXX** seul sur sa ligne, **XXX** :
    header_patterns = [
        re.compile(r'^##+\s+(.+?)$'),                       # ## ou ### markdown
        re.compile(r'^\*\*([^*]+)\*\*\s*$'),                # **XXX** seul sur sa ligne
        re.compile(r'^\s*\*\*([^*:]+?)\*\*\s*[:—–]'),       # **XXX** : ou **XXX** —
    ]

    allowed_normalized = set(allowed.lower().strip() for allowed in ALLOWED_HEADERS)
    skip_header_compiled = [re.compile(p, re.IGNORECASE) for p in SKIP_HEADER_PATTERNS]

    for i, line in enumerate(lines):
        # Skip les patterns de headers légitimes mais variables (numérotation des risques, etc.)
        if any(p.match(line) for p in skip_header_compiled):
            continue

        for pattern in header_patterns:
            match = pattern.match(line)
            if not match:
                continue
            header_raw = match.group(1)
            header_normalized = normalize_header(header_raw)

            # Vérifier dans la liste autorisée (avec match approximatif)
            is_allowed = False
            for allowed in allowed_normalized:
                # Match exact ou allowed est inclus dans header
                if allowed == header_normalized or allowed in header_normalized:
                    is_allowed = True
                    break

            if not is_allowed:
                # Skip les variations légitimes courtes (ex: "**Display**", "**Body**")
                if len(header_normalized) < 3:
                    continue
                violations.append({
                    'check': 'subsection',
                    'line': i + 1,
                    'header': header_raw.strip(),
                    'context': line.strip()[:120],
                    'hint': 'Sous-section inventée hors format autorisé. Le pitch ne crée pas de nouvelles sections — toute info qui ne rentre pas dans une section existante appartient à Phase 4.',
                })
                break

    return violations


def check_section_lengths(content):
    """Détecte les sections cadrées qui dépassent leur cap de longueur."""
    violations = []
    lines = content.split('\n')

    # Trouver chaque section avec cap et mesurer
    for i, line in enumerate(lines):
        # Détecter les headers de sections cadrées
        for header_key, cap in SECTION_CAPS.items():
            # Match approximatif sur la ligne
            line_normalized = normalize_header(line)
            if header_key not in line_normalized:
                continue
            # Vérifier que c'est bien un header (pas du texte courant)
            if not re.match(r'^\s*(##+|\*\*|-)\s', line):
                continue

            # Lire le contenu jusqu'à la prochaine section
            content_lines = []
            for j in range(i + 1, len(lines)):
                next_line = lines[j]
                # Stop si nouveau header markdown ## ou ###
                if re.match(r'^##+\s', next_line):
                    break
                # Stop si **Mot** seul sur sa ligne
                if re.match(r'^\*\*[^*]+\*\*\s*$', next_line):
                    break
                # Stop si **Mot** : ou **Mot** — au début de ligne (avec ou sans espaces)
                if re.match(r'^\s*\*\*[^*:]+?\*\*\s*[:—–]', next_line):
                    break
                # Stop si - **Mot** : ou - **Mot** — (puce avec sous-section)
                if re.match(r'^\s*[-*]\s+\*\*[^*:]+?\*\*\s*[:—–]', next_line):
                    break
                # Stop si séparateur
                if re.match(r'^---+$', next_line):
                    break
                content_lines.append(next_line)

            section_text = ' '.join(content_lines)
            word_count = count_words(section_text)

            if word_count > cap:
                violations.append({
                    'check': 'length',
                    'line': i + 1,
                    'section': header_key,
                    'word_count': word_count,
                    'cap': cap,
                    'overflow': word_count - cap,
                    'hint': f'Section "{header_key}" : {word_count} mots vs cap {cap}. Resserre — la prose libre après le format strict est un débordement structurel.',
                })
            break  # Match trouvé, passer à la ligne suivante

    return violations


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def scan_pitch(content):
    """Scan complet — retourne la liste de toutes les violations."""
    violations = []
    violations.extend(check_numeric_violations(content))
    violations.extend(check_invented_subsections(content))
    violations.extend(check_section_lengths(content))
    return violations


def format_human(violations, filepath):
    """Output human-readable pour la console."""
    filename = filepath.split('/')[-1] if '/' in filepath else filepath
    print(f"\n=== PHASE 3B PITCH STRUCTURAL GATE ===")
    print(f"File: {filename}")
    print()

    if not violations:
        print("VERDICT: PASS — aucun débordement structurel détecté")
        print("Le pitch reste dans les sensations et intentions, pas dans la prescription HTML.")
        return

    by_check = {}
    for v in violations:
        by_check.setdefault(v['check'], []).append(v)

    print(f"[FAIL] {len(violations)} violation(s) structurelle(s) détectée(s) :\n")

    if 'numeric' in by_check:
        print(f"❌ Valeurs numériques hors palette ({len(by_check['numeric'])}x)")
        for v in by_check['numeric'][:5]:
            print(f"   Ligne {v['line']} [{v['pattern']}]: {v['matched']}")
            print(f"      Contexte : {v['context']}")
            print(f"      → {v['hint']}")
        if len(by_check['numeric']) > 5:
            print(f"   ... et {len(by_check['numeric']) - 5} autre(s)")
        print()

    if 'subsection' in by_check:
        print(f"❌ Sous-sections inventées ({len(by_check['subsection'])}x)")
        for v in by_check['subsection'][:5]:
            print(f"   Ligne {v['line']} : « {v['header']} »")
            print(f"      → {v['hint']}")
        if len(by_check['subsection']) > 5:
            print(f"   ... et {len(by_check['subsection']) - 5} autre(s)")
        print()

    if 'length' in by_check:
        print(f"❌ Sections trop longues ({len(by_check['length'])}x)")
        for v in by_check['length']:
            print(f"   Section « {v['section']} » : {v['word_count']} mots vs cap {v['cap']} (overflow +{v['overflow']})")
            print(f"      → {v['hint']}")
        print()

    print("VERDICT: FAIL — corrections requises")
    print("Resserre les sections en débordement. Toute info qui ne rentre pas dans le format")
    print("imposé appartient à Phase 4 (qui a la fiche styliste, palette, fonts en input direct).")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 phase3b-pitch-structural-gate.py <path/to/pitch.md> [--json-output]", file=sys.stderr)
        sys.exit(2)

    filepath = sys.argv[1]
    json_output = '--json-output' in sys.argv

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erreur: fichier introuvable — {filepath}", file=sys.stderr)
        sys.exit(2)

    violations = scan_pitch(content)

    if json_output:
        result = {
            'file': filepath,
            'status': 'PASS' if not violations else 'FAIL',
            'violation_count': len(violations),
            'violations': violations,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        format_human(violations, filepath)

    sys.exit(0 if not violations else 1)


if __name__ == '__main__':
    main()
