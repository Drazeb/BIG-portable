#!/usr/bin/env python3
"""
Phase 3B-7a Style Anti-Slop Gate

Vérifie qu'un sub-agent styliste (3B-7a) n'a pas recopié de marqueurs slop
transverses (Partie C de `ref/styles-bibliotheque.md`) dans ses prescriptions
positives — c'est-à-dire dans les sections où le styliste prescrit ce que
le pitch designer en aval doit INCARNER.

Pourquoi : certaines fiches Partie A du catalogue contiennent, dans leur champ
"Signatures visuelles à incarner", des éléments qui peuvent toucher des
marqueurs Partie C (ex : Aurora UI listant "3 radial-gradients" qui frôle
"aurora 3 blobs centrés"). Si le styliste recopie sans précaution, le slop
est introduit en input du pipeline depuis le catalogue lui-même.

Sections scannées (prescriptions positives uniquement) :
  - ## Signatures à incarner
  - ## Modulations dues au mix (si applicable)

Sections NON scannées (prescriptions négatives — où nommer le slop est OK) :
  - ## INTERDITS actifs
  - ## Garde-fous anti-slop activés
  - ## Avis du DA

Usage :
  python3 phase3b-style-anti-slop.py <style-choice-c{N}-{variant}.md> [--json-output]

Exit codes :
  0 = PASS
  1 = FAIL (violations bloquantes)
  2 = ERREUR fichier
"""

from __future__ import annotations

import json
import re
import sys


# ---------------------------------------------------------------------------
# Marqueurs slop transverses — calque sur Partie C de styles-bibliotheque.md
# Chaque marqueur a un id stable (PARTC-X.Y), un nom, des regex patterns,
# et une raison courte affichée en feedback.
# ---------------------------------------------------------------------------

PARTC_MARKERS = [
    # ===== C.1 — Couleurs & Gradients =====
    {
        'id': 'PARTC-1.1',
        'name': 'Hex Tailwind purple/indigo générique',
        'patterns': [
            r'#6366f1\b', r'#4f46e5\b', r'#4338ca\b',
            r'#8b5cf6\b', r'#7c3aed\b', r'#6d28d9\b',
            r'#a855f7\b', r'#9333ea\b',
            r'\bbg-indigo-(400|500|600|700)\b',
            r'\bbg-violet-(400|500|600|700)\b',
            r'\bbg-purple-(400|500|600|700)\b',
        ],
        'reason': 'Hex Tailwind par défaut (indigo/violet/purple). Marqueur AI slop documenté.',
    },
    {
        'id': 'PARTC-1.2',
        'name': 'Aurora gradient générique 3 blobs',
        'patterns': [
            r'\baurora\s+(gradient|3\s+blobs|blobs)\b',
            r'\b3\s+blobs\s+(centr[ée]s|anim[ée]s|violet)',
            r'\bgradient\s+mesh\s+g[ée]n[ée]rique\b',
        ],
        'reason': 'Aurora 3 blobs centrés violet+rose+bleu = marqueur AI slop le plus visible.',
    },
    {
        'id': 'PARTC-1.3',
        'name': 'Gradient violet→bleu sur fond clair',
        'patterns': [
            r'\bgradient\s+violet\s*[→/-]\s*bleu\b',
            r'\bgradient\s+(purple|violet|indigo)\s+to\s+(blue|cyan)\b',
            r'\bdégradé\s+violet[\s-]bleu\b',
        ],
        'reason': 'Signature des AI-generated SaaS landings.',
    },

    # ===== C.2 — Typographie =====
    {
        'id': 'PARTC-2.1',
        'name': 'Inter en mono-font (display + body)',
        'patterns': [
            r'\bInter\s+(en\s+)?(mono[\s-]?font|seul|seule)\b',
            r'\bInter\s+en\s+(headline|display)\s+et\s+en\s+(body|corps)',
            r'\bInter\s+partout\b',
        ],
        'reason': 'Inter en mono-font (display ET body) = signal AI direct. Inter body OK avec un display CHOISI.',
    },
    {
        'id': 'PARTC-2.2',
        'name': 'Roboto/Arial fallback systématique',
        'patterns': [
            r'\bRoboto\s+fallback\s+syst[ée]matique\b',
            r'\bArial\s+fallback\s+syst[ée]matique\b',
            r'\bRoboto\s*/\s*Arial\b',
        ],
        'reason': 'Fallback Roboto/Arial = signal de "design par défaut", pas de choix typo.',
    },

    # ===== C.3 — Layout & Composants =====
    {
        'id': 'PARTC-3.1',
        'name': 'Hero centré titre + sous-titre + CTA seul',
        'patterns': [
            r'\bhero\s+centr[ée]\s+(avec\s+)?(grand\s+)?titre\s*\+\s*(sous[\s-]?titre|sub)\s*\+\s*(bouton\s+)?CTA\s+seul\b',
            r'\bcentered\s+hero\s+(with\s+)?title\s*\+\s*subtitle\s*\+\s*CTA\b',
            r'\bpattern\s+Bootstrap\s+(hero\s+)?centr[ée]\b',
        ],
        'reason': 'Hero centré titre+sous-titre+CTA = pattern Bootstrap générique sans signature de marque.',
    },
    {
        'id': 'PARTC-3.2',
        'name': '3 features en boxes (icône + titre + texte)',
        'patterns': [
            r'\b3\s+features?\s+en\s+box(es)?\b',
            r'\btrois\s+features\s+(horizontales|en\s+grid)\b',
            r'\b3\s+features?\s+(grid|cards?)\s+(ic[ôo]ne?\s*\+\s*titre\s*\+\s*texte|icon\s*\+\s*title\s*\+\s*desc)',
            r'\bgrid\s+3\s+cards?\s+identiques\b',
        ],
        'reason': '3 features en boxes (icône+titre+texte) horizontales = artefact CTA pages 2018-2020.',
    },
    {
        'id': 'PARTC-3.3',
        'name': 'Cards radius 8-12px + shadow 0.1 opacity sur fond blanc',
        'patterns': [
            r'\bcards?\s+(avec\s+)?border[\s-]?radius\s*:?\s*(8|10|12)px\s*\+\s*ombre',
            r'\bcards?\s+8[\s-]12px\s*\+\s*shadow\s+0\.1',
            r'\bsubtle\s+shadow\s+0\.1\s+opacity\s+syst[ée]matique\b',
        ],
        'reason': 'Combo générique AI default : cards radius 8-12px + ombre 0.1 opacity.',
    },
    {
        'id': 'PARTC-3.4',
        'name': 'Section "How it works" 3 steps numérotés avec icônes',
        'patterns': [
            r'\bhow\s+it\s+works\s+(en\s+)?3\s+steps?\s+num[ée]rot[ée]s?\s+avec\s+ic[ôo]nes?\b',
            r'\b3\s+[ée]tapes\s+num[ée]rot[ée]es\s+avec\s+ic[ôo]nes?\b',
        ],
        'reason': 'Section "How it works" en 3 steps numérotés = structure SaaS template.',
    },
    {
        'id': 'PARTC-3.5',
        'name': 'Footer 4 colonnes égales de liens',
        'patterns': [
            r'\bfooter\s+(avec\s+)?4\s+colonnes?\s+[ée]gales?\s+de\s+liens?\b',
            r'\bfooter\s+(4|four)\s+(cols?|columns?)\s+sitemap\b',
        ],
        'reason': 'Footer 4 colonnes égales = sitemap déguisé sans personnalité.',
    },

    # ===== C.4 — Effets visuels =====
    {
        'id': 'PARTC-4.1',
        'name': 'Glassmorphism backdrop-blur 20px+ violet',
        'patterns': [
            r'\bglassmorphism\s+(avec\s+)?backdrop[\s-]?(filter|blur)\s*:?\s*\d{2,}px\s*\+?\s*(fond\s+)?violet',
            r'\bbackdrop[\s-]?blur\s+20px\+?\s+(g[ée]n[ée]rique|violet)\b',
        ],
        'reason': 'Glassmorphism backdrop-blur 20px+ + fond violet = combo AI slop documenté.',
    },
    {
        'id': 'PARTC-4.2',
        'name': 'Dark mode générique (#0a0a0a + #fff + indigo)',
        'patterns': [
            r'\bdark\s+mode\s+(=\s+)?fond\s+#?0a0a0a\s*\+\s*texte\s+#?ffffff?\s*\+\s*accent\s+indigo\b',
            r'\bcombo\s+#?0a0a0a\s*\+\s*#?fff\s*\+\s*indigo\b',
        ],
        'reason': 'Dark mode fond #0a0a0a + texte #ffffff + accent indigo = combo AI slop dark.',
    },

    # ===== C.5 — Marqueurs comportementaux =====
    {
        'id': 'PARTC-5.1',
        'name': 'Translate Y au hover',
        'patterns': [
            # On cible le combo "translate Y" + "hover/survol" — pas translateY isolé
            r'\btranslate(?:Y|\s+Y|\s+vertical)\s+au\s+hover\b',
            r'\btranslate[\s-]?Y\s+(at|on)\s+hover\b',
            r'\bhover\s*:[^.]*\btranslate[\s-]?Y\b',
            r'\b(carte|card)\s+(qui\s+)?(se\s+)?soul[èe]ve\s+au\s+(survol|hover)\b',
            r'\b(carte|card)\s+qui\s+monte\s+au\s+(survol|hover)\b',
            r'\btransform:\s*translateY\([^)]+\)\s*[;,]?\s*(au|on)\s+hover\b',
        ],
        'reason': 'Translate Y au hover (carte qui se soulève) = pattern le plus générique du web.',
    },
    {
        'id': 'PARTC-5.2',
        'name': 'Transform scale > 1.02 au hover',
        'patterns': [
            r'\btransform[:\s]+scale\([1-9]\.\d+\)\s*(au|on)\s+hover\b',
            r'\bscale\s*>\s*1\.02\s+au\s+hover\b',
            r'\bscale\s+\d\.\d+\s+effet\s+jouet\b',
        ],
        'reason': 'transform: scale() > 1.02 au hover = effet "jouet".',
    },
    {
        'id': 'PARTC-5.3',
        'name': 'Icône/arrow qui slide au hover',
        'patterns': [
            r'\b(ic[ôo]ne|arrow|fl[èe]che)\s+qui\s+slide\s+au\s+(survol|hover)\b',
            r'\barrow\s+slide\s+(at|on)\s+hover\b',
            r'\btranslateX\s+sur\s+enfant\s+CTA\b',
        ],
        'reason': 'Icône/arrow qui slide au hover = cliché SaaS 2017.',
    },
    {
        'id': 'PARTC-5.4',
        'name': 'Soulignement qui grandit au hover',
        'patterns': [
            r'\bsoulignement\s+qui\s+grandit\s+au\s+(survol|hover)\b',
            r'\bunderline\s+qui\s+(grandit|grows)\s+(at|on)\s+hover\b',
            r'\bscaleX\s*\(\s*0\s*\)\s*[→-]+\s*scaleX\s*\(\s*1\s*\)',
        ],
        'reason': 'Soulignement qui grandit au hover (scaleX 0→1) = cliché navbar 2018.',
    },
    {
        'id': 'PARTC-5.5',
        'name': 'Letter-spacing qui augmente au hover',
        'patterns': [
            r'\bletter[\s-]?spacing\s+qui\s+augmente\s+au\s+(survol|hover)\b',
            r'\bletter[\s-]?spacing\s+(at|on)\s+hover\b',
        ],
        'reason': 'Letter-spacing qui augmente au hover = cliché footer premium 2017.',
    },
    {
        'id': 'PARTC-5.6',
        'name': 'Pulsing/breathing animation infinity décorative',
        'patterns': [
            r'\bpulsing\s+(breathing\s+)?animation\b',
            r'\bbreathing\s+animation\s+infini(e|ty)?\b',
            r'\banimation[:\s-]+infinite\s+d[ée]corative?\b',
            r'\b(opacity|box[\s-]?shadow)\s+qui\s+oscille\s+en\s+boucle\b',
        ],
        'reason': 'Pulsing/breathing animations infinies décoratives = indicateur daté.',
    },
    {
        'id': 'PARTC-5.7',
        'name': 'Glow shadow box-shadow 0 0 sans offset',
        'patterns': [
            r'\bglow\s+shadows?\b',
            r'\bbox[\s-]?shadow:\s*0\s+0\s+\d+px\b',
            r'\btext[\s-]?shadow\s+glow\s+sur\s+(les\s+)?titres?\b',
        ],
        'reason': 'Glow shadows / box-shadow 0 0 Npx sans offset = ombre non-directionnelle.',
    },
    {
        'id': 'PARTC-5.8',
        'name': 'Wave/zigzag dividers entre sections',
        'patterns': [
            r'\bwave\s+dividers?\s+entre\s+sections?\b',
            r'\bzigzag\s+dividers?\b',
            r'\b(SVG|clip[\s-]?path)\s+(d[ée]coratif|wave|zigzag)\s+entre\s+sections?\b',
        ],
        'reason': 'Wave/zigzag dividers entre sections = marqueur de template WordPress.',
    },
    {
        'id': 'PARTC-5.9',
        'name': 'Staggered fade-up @keyframes manuels',
        'patterns': [
            r'\bstaggered\s+fade[\s-]?up\s+(manuels?|@keyframes?)\b',
            r'\b@keyframes\s+(avec\s+)?translateY\s*\+\s*opacity\s*\+\s*delays?\s+manuels?\b',
        ],
        'reason': 'Staggered fade-up @keyframes manuels = signature des landing pages 2017. Préférer @starting-style.',
    },
]


# ---------------------------------------------------------------------------
# Sections du markdown — extraction
# ---------------------------------------------------------------------------

# Sections que le gate scanne (prescriptions POSITIVES — où nommer un marqueur
# slop signifie le faire INCARNER par le pitch designer aval).
SCANNED_SECTIONS = [
    'Signatures à incarner',
    'Modulations dues au mix',
]

# Sections que le gate IGNORE (prescriptions NÉGATIVES — où nommer un marqueur
# slop signifie le BANNIR, ce qui est l'objectif de ces sections).
IGNORED_SECTIONS = [
    'INTERDITS actifs',
    'Garde-fous anti-slop activés',
    'Avis du DA',
    'Scan exhaustif',  # contient les 34 raisons d'INCOMPATIBLE qui peuvent nommer du slop
    'Longlist ordonnée',  # justifications qui peuvent citer des risques
]


def extract_section(content: str, section_title: str) -> str | None:
    """
    Extrait le contenu textuel d'une section markdown identifiée par son titre
    (sans les ##). Retourne le texte de la section jusqu'au prochain titre `##`
    de même niveau ou supérieur (#), ou jusqu'à la fin du document.
    Retourne None si la section n'existe pas.
    """
    # On capture les titres de niveau 2 (## Foo) ou 3 (### Foo) tolérant des
    # variations (## Signatures à incarner (...), ## Signatures à incarner)
    # Match du début de section :
    pattern = re.compile(
        r'^#{2,3}\s+' + re.escape(section_title) + r'\b[^\n]*\n',
        re.MULTILINE,
    )
    match = pattern.search(content)
    if not match:
        return None
    start = match.end()
    # Fin = prochain titre de niveau ≤ 3 (## ou #) après start, ou EOF
    end_pattern = re.compile(r'^#{1,3}\s+\S', re.MULTILINE)
    end_match = end_pattern.search(content, pos=start)
    end = end_match.start() if end_match else len(content)
    return content[start:end].strip()


# ---------------------------------------------------------------------------
# Check principal — scan des marqueurs Partie C dans les sections positives
# ---------------------------------------------------------------------------

def check_partc_markers(content: str) -> list[dict]:
    """
    Pour chaque section scannée, parcourt les marqueurs Partie C et retourne
    la liste des violations détectées.
    """
    violations = []

    for section_title in SCANNED_SECTIONS:
        section_text = extract_section(content, section_title)
        if section_text is None:
            # Section absente — pas une violation en soi (Modulations est
            # optionnelle ; Signatures est obligatoire mais sa présence est
            # vérifiée ailleurs si besoin).
            continue
        if not section_text:
            # Section vide
            continue

        for marker in PARTC_MARKERS:
            for pattern in marker['patterns']:
                match = re.search(pattern, section_text, re.IGNORECASE)
                if match:
                    # Extraire un extrait contextuel (~80 caractères autour
                    # de la correspondance).
                    s = max(0, match.start() - 30)
                    e = min(len(section_text), match.end() + 50)
                    excerpt = section_text[s:e].strip().replace('\n', ' ')
                    violations.append({
                        'check': 'partc_marker_in_prescription',
                        'severity': 'FAIL',
                        'marker_id': marker['id'],
                        'marker_name': marker['name'],
                        'section': section_title,
                        'excerpt': excerpt,
                        'detail': (
                            f"Section « {section_title} » contient « {marker['name']} » "
                            f"({marker['id']}) — {marker['reason']} "
                            f"Reformule pour préciser ce qui distingue cette signature "
                            f"du marqueur slop, ou retire-la."
                        ),
                    })
                    # Un seul match par marqueur par section (pas la peine
                    # de spammer si la même formulation apparaît 2 fois).
                    break

    return violations


# ---------------------------------------------------------------------------
# Vérification structurelle — la section "Signatures à incarner" existe
# ---------------------------------------------------------------------------

def check_signatures_section_present(content: str) -> list[dict]:
    """La fiche DOIT contenir une section "Signatures à incarner" non vide."""
    section = extract_section(content, 'Signatures à incarner')
    if section is None:
        return [{
            'check': 'signatures_section_missing',
            'severity': 'FAIL',
            'detail': "Section « Signatures à incarner » absente — obligatoire pour "
                      "que le pitch designer aval ait des prescriptions à incarner.",
        }]
    if not section.strip():
        return [{
            'check': 'signatures_section_empty',
            'severity': 'FAIL',
            'detail': "Section « Signatures à incarner » présente mais vide.",
        }]
    return []


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    json_output = '--json-output' in sys.argv
    args = [a for a in sys.argv[1:] if a != '--json-output']

    if len(args) < 1:
        print("Usage: python3 phase3b-style-anti-slop.py <style-choice.md> [--json-output]")
        sys.exit(2)

    filepath = args[0]
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erreur: fichier introuvable — {filepath}")
        sys.exit(2)

    all_violations = []
    all_violations.extend(check_signatures_section_present(content))
    all_violations.extend(check_partc_markers(content))

    verdict = 'FAIL' if all_violations else 'PASS'
    exit_code = 1 if all_violations else 0

    if json_output:
        output = {
            'verdict': verdict,
            'file': filepath,
            'sections_scanned': SCANNED_SECTIONS,
            'sections_ignored': IGNORED_SECTIONS,
            'markers_count': len(PARTC_MARKERS),
            'violations': all_violations,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        sys.exit(exit_code)

    filename = filepath.rsplit('/', 1)[-1] if '/' in filepath else filepath
    print(f"\n=== PHASE 3B-7a STYLE ANTI-SLOP GATE ===")
    print(f"File: {filename}")
    print(f"Sections scannées: {', '.join(SCANNED_SECTIONS)}")
    print(f"Marqueurs Partie C surveillés: {len(PARTC_MARKERS)}")
    print()

    if all_violations:
        by_check: dict[str, list] = {}
        for v in all_violations:
            by_check.setdefault(v['check'], []).append(v)
        print(f"[FAIL] {len(all_violations)} violation(s) :\n")
        for check, instances in sorted(by_check.items()):
            print(f"  ❌ {check} ({len(instances)}x)")
            for inst in instances[:5]:
                print(f"     {inst['detail']}")
                if 'excerpt' in inst:
                    print(f"     Extrait: « ...{inst['excerpt']}... »")
            if len(instances) > 5:
                print(f"     ... et {len(instances) - 5} autre(s)")
            print()
        print("VERDICT: FAIL — corrections requises")
        print("→ Resume du sub-agent styliste avec ces violations en feedback.")
    else:
        print(f"VERDICT: PASS — aucun marqueur Partie C dans les prescriptions positives.")

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
