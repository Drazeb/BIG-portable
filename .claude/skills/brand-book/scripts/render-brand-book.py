#!/usr/bin/env python3
"""
render-brand-book.py
====================

Substitution Mustache mécanique du `template-base.html` du skill brand-book.

Pourquoi
--------
Avant ce script, le sub-agent brand-book écrivait DIRECTEMENT le HTML final du
brand book. Conséquence : il pouvait réécrire / simplifier / inventer le markup
de sections pourtant figées par le template (ex: section 07b Pitch Deck — bug
Vermeil 30/05/2026 : pattern spread asymétrique 2×3 remplacé par 6 figures
à plat ; section Identity Card bento v4 — "pétouille" mentionnée par Charles ;
etc.).

Avec ce script, **le sub-agent ne touche plus au HTML**. Il produit un
`template-vars.json` contenant uniquement les **valeurs** des slots Mustache
`{{VAR}}` du template (titres, captions, couleurs, manifesto, etc.). Le script
fait la substitution mécanique. Le markup figé est **verrouillé par construction**.

Cas spécial : les 8 slots `{{BATCH2_INVENTORY_*}}` ne sont PAS fournis dans le
JSON. Le script lit automatiquement `batch2-inventory.html` (produit par
`extract-batch2-inventory.py` en Étape 2.5) et y injecte les `<article
data-component="…">…</article>` de la catégorie correspondante — y compris les
commentaires `BEGIN_BLOCK md5=… / END_BLOCK` qui font passer le quality gate
MD5 (Étape 5) par construction.

Usage
-----
    python3 render-brand-book.py <template.html> <vars.json> <output.html> \
            [--batch2-inventory <inventory.html>] [--strict] [--verbose]

Arguments
---------
    template.html           Le template-base.html (point de départ)
    vars.json               Le template-vars.json produit par le sub-agent
    output.html             Le brand book final à produire
    --batch2-inventory      Path vers batch2-inventory.html. Si fourni, les 8
                            slots BATCH2_INVENTORY_* sont substitués automatiquement.
                            Si absent, ils sont remplacés par une string vide.
    --strict                Si un slot du template n'a PAS de valeur dans vars.json,
                            erreur fatale (exit 1). Sinon (défaut), placeholder
                            visible "[MISSING:VAR_NAME]".
    --verbose               Log détaillé.

Exit codes
----------
    0  OK
    1  erreur fatale (input manquant, JSON invalide, slot manquant en --strict)
    2  mauvais usage CLI

Format vars.json
----------------
Objet JSON {clé → valeur} où chaque clé correspond au nom d'un slot du template
SANS les `{{}}`. Exemple :

    {
      "BRAND": "les-vermeil",
      "BRAND_THEME_COLOR": "#1a2a18",
      "PITCH_DECK_TITLE": "Le relevé, en six planches.",
      "PITCH_DECK_SUBTITLE": "Deck commercial · 6 slides · ratio 16:9",
      "COLOR_1_ROLE": "Fond profond", "COLOR_1_NAME": "Bocage", "COLOR_1_HEX": "#1a2a18",
      ...
    }

Mapping BATCH2_INVENTORY_*
---------------------------
| Slot                                       | Catégorie(s) inventory injectées |
|--------------------------------------------|----------------------------------|
| {{BATCH2_INVENTORY_ICONS}}                 | icons                            |
| {{BATCH2_INVENTORY_BUTTONS}}               | buttons                          |
| {{BATCH2_INVENTORY_INPUTS}}                | inputs                           |
| {{BATCH2_INVENTORY_BADGES}}                | badges                           |
| {{BATCH2_INVENTORY_TOGGLES_CHECKBOXES}}    | toggles + checkboxes             |
| {{BATCH2_INVENTORY_CARDS}}                 | cards                            |
| {{BATCH2_INVENTORY_MISC_UI}}               | tabs + alerts + progress         |
| {{BATCH2_INVENTORY_CHARTS}}                | charts                           |
"""

import argparse
import json
import re
import sys
from pathlib import Path


SLOT_PATTERN = re.compile(r"\{\{([A-Z0-9_]+)\}\}")

BATCH2_SLOT_MAPPING = {
    "BATCH2_INVENTORY_ICONS": ["icons"],
    "BATCH2_INVENTORY_BUTTONS": ["buttons"],
    "BATCH2_INVENTORY_INPUTS": ["inputs"],
    "BATCH2_INVENTORY_BADGES": ["badges"],
    "BATCH2_INVENTORY_TOGGLES_CHECKBOXES": ["toggles", "checkboxes"],
    "BATCH2_INVENTORY_CARDS": ["cards"],
    "BATCH2_INVENTORY_MISC_UI": ["tabs", "alerts", "progress"],
    "BATCH2_INVENTORY_CHARTS": ["charts"],
}


def list_slots(template_html: str) -> set:
    """Retourne l'ensemble unique des slots {{VAR}} présents dans le template."""
    return set(SLOT_PATTERN.findall(template_html))


def find_balanced_block(html: str, start: int, tag_name: str):
    """
    À partir de `start` (pos pointant sur `<{tag_name}`), trouve la fin du
    bloc équilibré en gérant les imbrications du MÊME tag. Retourne
    (start, end_exclusif) ou None.
    """
    open_re = re.compile(
        rf"<{re.escape(tag_name)}\b[^>]*?(/?)>",
        re.DOTALL | re.IGNORECASE,
    )
    open_match = open_re.match(html, start)
    if not open_match:
        return None
    if open_match.group(1) == "/":
        return (start, open_match.end())
    nested_re = re.compile(
        rf"<(/?){re.escape(tag_name)}\b[^>]*?(/?)>",
        re.DOTALL | re.IGNORECASE,
    )
    depth = 1
    pos = open_match.end()
    while True:
        m = nested_re.search(html, pos)
        if not m:
            return None
        is_close = m.group(1) == "/"
        is_self_close = m.group(2) == "/"
        if is_close:
            depth -= 1
            if depth == 0:
                return (start, m.end())
        elif not is_self_close:
            depth += 1
        pos = m.end()


def extract_articles_by_category(inventory_html: str) -> dict:
    """
    Parse `batch2-inventory.html` et retourne dict {category → list[article_html]}.
    Chaque article inclut ses bornes <!-- BEGIN_BLOCK / END_BLOCK -->.

    Utilise un balanced parser sur <section> ET sur <article> pour gérer les
    imbrications (ex: Vermeil a des <article class="card"> verbatim DANS
    les <article data-component="cards"> wrappers de l'inventory — un regex
    non-greedy couperait au mauvais </article>).
    """
    by_cat = {}
    section_open_re = re.compile(
        r'<section\s+data-inv="([^"]+)"[^>]*>',
        re.IGNORECASE,
    )
    article_open_re = re.compile(r'<article\b', re.IGNORECASE)

    for section_match in section_open_re.finditer(inventory_html):
        category = section_match.group(1)
        section_block = find_balanced_block(inventory_html, section_match.start(), "section")
        if section_block is None:
            continue
        section_content = inventory_html[section_match.end():section_block[1] - len("</section>")]
        articles = []
        # Itérer en avançant la position pour ne pas re-capturer les <article>
        # imbriqués (ex: Vermeil met un <article class="card"> verbatim
        # DANS le <article data-component="cards"> wrapper inventory).
        # On ne garde QUE les wrappers de premier niveau (ceux avec data-component=).
        pos = 0
        while pos < len(section_content):
            article_match = article_open_re.search(section_content, pos)
            if not article_match:
                break
            article_block = find_balanced_block(section_content, article_match.start(), "article")
            if article_block is None:
                pos = article_match.end()
                continue
            block_html = section_content[article_block[0]:article_block[1]]
            # Filtre : on ne garde que les wrappers de premier niveau, identifiables
            # par la présence de `data-component=` dans l'ouvrant.
            opening_tag = block_html[:block_html.find(">") + 1]
            if "data-component=" in opening_tag:
                articles.append(block_html)
            pos = article_block[1]
        by_cat[category] = articles
    return by_cat


def build_batch2_substitutions(inventory_html: str) -> dict:
    """
    Construit dict {slot_name → html_concaténé} pour les 8 slots BATCH2_INVENTORY_*.
    """
    by_cat = extract_articles_by_category(inventory_html)
    substitutions = {}
    for slot_name, categories in BATCH2_SLOT_MAPPING.items():
        articles = []
        for cat in categories:
            articles.extend(by_cat.get(cat, []))
        substitutions[slot_name] = "\n".join(articles)
    return substitutions


def substitute_slots(
    template_html: str,
    vars_dict: dict,
    strict: bool,
    verbose: bool,
) -> tuple:
    """
    Substitue tous les `{{VAR}}` du template par leur valeur dans vars_dict.
    Retourne (output_html, missing_slots, substituted_count).
    """
    missing = []
    substituted = 0
    used_slots = set()

    def replacer(match):
        nonlocal substituted
        slot = match.group(1)
        used_slots.add(slot)
        if slot in vars_dict:
            substituted += 1
            value = vars_dict[slot]
            # Convertir les non-string en string proprement.
            if value is None:
                return ""
            return str(value)
        else:
            missing.append(slot)
            if strict:
                return match.group(0)  # garde le {{VAR}} pour debug
            return f"[MISSING:{slot}]"

    output = SLOT_PATTERN.sub(replacer, template_html)

    if verbose:
        unused_vars = set(vars_dict.keys()) - used_slots
        if unused_vars:
            print(f"[INFO] {len(unused_vars)} variable(s) fournie(s) mais non utilisée(s) par le template :")
            for v in sorted(unused_vars):
                print(f"         · {v}")

    return output, sorted(set(missing)), substituted


def main():
    parser = argparse.ArgumentParser(
        description="Render brand book HTML by Mustache substitution.",
    )
    parser.add_argument("template_path", type=str, help="Path to template-base.html")
    parser.add_argument("vars_json_path", type=str, help="Path to template-vars.json")
    parser.add_argument("output_path", type=str, help="Path to write the rendered HTML")
    parser.add_argument(
        "--batch2-inventory", type=str, default=None,
        help="Optional path to batch2-inventory.html for auto-injection of BATCH2_INVENTORY_* slots",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Fail (exit 1) if any template slot has no value in vars.json",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    template_path = Path(args.template_path).resolve()
    vars_path = Path(args.vars_json_path).resolve()
    output_path = Path(args.output_path).resolve()
    inventory_path = Path(args.batch2_inventory).resolve() if args.batch2_inventory else None

    if not template_path.exists():
        print(f"[ERROR] Template introuvable : {template_path}")
        sys.exit(1)
    if not vars_path.exists():
        print(f"[ERROR] vars.json introuvable : {vars_path}")
        sys.exit(1)
    if inventory_path and not inventory_path.exists():
        print(f"[ERROR] batch2-inventory.html introuvable : {inventory_path}")
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Template    : {template_path}")
    print(f"[INFO] Vars JSON   : {vars_path}")
    print(f"[INFO] Output      : {output_path}")
    if inventory_path:
        print(f"[INFO] Inventory   : {inventory_path}")
    print(f"[INFO] Strict mode : {args.strict}")

    template_html = template_path.read_text(encoding="utf-8")
    template_slots = list_slots(template_html)
    print(f"[INFO] Slots dans template : {len(template_slots)} uniques")

    try:
        vars_dict = json.loads(vars_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON invalide dans {vars_path} : {e}")
        sys.exit(1)
    if not isinstance(vars_dict, dict):
        print(f"[ERROR] vars.json doit être un objet JSON {{clé → valeur}}, pas {type(vars_dict).__name__}")
        sys.exit(1)
    print(f"[INFO] Variables fournies  : {len(vars_dict)}")

    # Injection automatique des 8 slots BATCH2_INVENTORY_*.
    if inventory_path:
        inventory_html = inventory_path.read_text(encoding="utf-8")
        batch2_subs = build_batch2_substitutions(inventory_html)
        # Les vars du JSON priment sur les substitutions auto (pour permettre override manuel).
        for slot_name, html_block in batch2_subs.items():
            if slot_name not in vars_dict:
                vars_dict[slot_name] = html_block
        counts_str = " · ".join(
            f"{slot.split('_')[-1].lower()}={len(SLOT_PATTERN.sub('', batch2_subs[slot]).split('<article'))-1}"
            for slot in batch2_subs
        )
        print(f"[INFO] Injection auto batch2-inventory : 8 slots remplis")

    # Substitution.
    output_html, missing, substituted = substitute_slots(
        template_html, vars_dict, args.strict, args.verbose,
    )

    print(f"[OK]   Substitutions   : {substituted}")
    if missing:
        print(f"[WARN] {len(missing)} slot(s) du template sans valeur dans vars.json :")
        for m in missing:
            print(f"         · {{{{{m}}}}}")
        if args.strict:
            print(f"[FAIL] Mode --strict : {len(missing)} slot(s) manquant(s), pas d'écriture.")
            sys.exit(1)
        else:
            print(f"[INFO] Mode non-strict : remplacés par '[MISSING:VAR]' dans le brand book.")

    # Garde-fou : aucun {{VAR}} ne doit subsister dans l'output (même en non-strict
    # on les a remplacés par [MISSING:VAR]).
    residual = SLOT_PATTERN.findall(output_html)
    if residual:
        print(f"[FAIL] Slots résiduels non substitués dans l'output : {len(residual)}")
        for r in set(residual):
            print(f"         · {{{{{r}}}}}")
        sys.exit(1)

    output_path.write_text(output_html, encoding="utf-8")
    size_kb = output_path.stat().st_size / 1024
    print(f"[OK]   Brand book écrit : {output_path} ({size_kb:,.1f} Ko, {len(output_html.splitlines()):,} lignes)")

    sys.exit(0)


if __name__ == "__main__":
    main()
