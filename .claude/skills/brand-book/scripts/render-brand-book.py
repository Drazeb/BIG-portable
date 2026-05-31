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
    "BATCH2_INVENTORY_LOCKUPS": ["lockups"],
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


def compose_palette_pages(vars_dict: dict) -> str:
    """
    Auto-compose la section Palette (6 pages couleur) à partir des slots
    COLOR_N_ROLE / COLOR_N_NAME / COLOR_N_HEX (N de 1 à 6) déjà fournis par
    le sub-agent dans template-vars.json.

    Une page par couleur : grand bloc swatch + meta (rôle / nom / hex / texte
    contrasté).
    """
    pages = []
    for n in range(1, 7):
        role = vars_dict.get(f"COLOR_{n}_ROLE", "").strip()
        name = vars_dict.get(f"COLOR_{n}_NAME", "").strip()
        hex_value = vars_dict.get(f"COLOR_{n}_HEX", "").strip()
        if not hex_value:
            continue
        # Texte sur le swatch : noir/blanc selon luminosité (heuristique simple via hex).
        text_color = "#fff"
        if hex_value.startswith("#") and len(hex_value) == 7:
            try:
                r, g, b = int(hex_value[1:3], 16), int(hex_value[3:5], 16), int(hex_value[5:7], 16)
                luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                text_color = "#0a0a0a" if luminance > 0.6 else "#fafafa"
            except ValueError:
                pass
        pages.append(
            f'  <article class="bk-palette-page" style="background:{hex_value};color:{text_color}">\n'
            f'    <div class="bk-palette-page__meta">\n'
            f'      <p class="bk-palette-page__index">{n:02d} / 06</p>\n'
            f'      <p class="bk-palette-page__role">{role}</p>\n'
            f'      <h3 class="bk-palette-page__name">{name}</h3>\n'
            f'    </div>\n'
            f'    <p class="bk-palette-page__hex"><span class="bk-mono">{hex_value.upper()}</span></p>\n'
            f'  </article>'
        )
    if not pages:
        return ""
    return '<div class="bk-palette-pages">\n' + "\n".join(pages) + '\n</div>'


def compose_typo_specimens(vars_dict: dict) -> str:
    """
    Auto-compose la section Typographie à partir des slots FONT_DISPLAY_NAME /
    FONT_DISPLAY / FONT_BODY / FONT_MONO_NAME / FONT_MONO déjà dans le JSON.

    3 specimens : Display (grand Aa + tagline) + Body (paragraphe sample) +
    Mono (specimen technique).
    """
    display_name = vars_dict.get("FONT_DISPLAY_NAME", "").strip()
    display_stack = vars_dict.get("FONT_DISPLAY", "").strip()
    body_stack = vars_dict.get("FONT_BODY", "").strip() or display_stack
    mono_name = vars_dict.get("FONT_MONO_NAME", "").strip()
    mono_stack = vars_dict.get("FONT_MONO", "").strip()

    if not display_name and not mono_name:
        return ""

    specimens = []
    if display_stack and display_name:
        specimens.append(
            f'  <article class="bk-typo-specimen bk-typo-specimen--display">\n'
            f'    <div class="bk-typo-specimen__aa" style="font-family:{display_stack}">Aa</div>\n'
            f'    <div class="bk-typo-specimen__meta">\n'
            f'      <p class="bk-typo-specimen__role">Display</p>\n'
            f'      <h3 class="bk-typo-specimen__name">{display_name}</h3>\n'
            f'      <p class="bk-typo-specimen__sample" style="font-family:{display_stack};font-size:32px;line-height:1.1;margin-top:16px">'
            f'Le repère du métier, posé large.</p>\n'
            f'    </div>\n'
            f'  </article>'
        )
    if body_stack:
        specimens.append(
            f'  <article class="bk-typo-specimen bk-typo-specimen--body">\n'
            f'    <div class="bk-typo-specimen__aa" style="font-family:{body_stack}">Aa</div>\n'
            f'    <div class="bk-typo-specimen__meta">\n'
            f'      <p class="bk-typo-specimen__role">Body</p>\n'
            f'      <h3 class="bk-typo-specimen__name">{body_stack.split(",")[0].strip().strip(chr(39)).strip(chr(34))}</h3>\n'
            f'      <p class="bk-typo-specimen__sample" style="font-family:{body_stack};font-size:16px;line-height:1.6;margin-top:16px">'
            f'Lorem ipsum dolor sit amet — la marque parle clair, '
            f'pose les mots à hauteur d\'usage, sans détours. Le texte courant porte la voix éditoriale.</p>\n'
            f'    </div>\n'
            f'  </article>'
        )
    if mono_stack and mono_name:
        specimens.append(
            f'  <article class="bk-typo-specimen bk-typo-specimen--mono">\n'
            f'    <div class="bk-typo-specimen__aa" style="font-family:{mono_stack}">Aa</div>\n'
            f'    <div class="bk-typo-specimen__meta">\n'
            f'      <p class="bk-typo-specimen__role">Mono</p>\n'
            f'      <h3 class="bk-typo-specimen__name">{mono_name}</h3>\n'
            f'      <p class="bk-typo-specimen__sample" style="font-family:{mono_stack};font-size:14px;line-height:1.5;margin-top:16px">'
            f'46.84°N · 1.43°W<br>Cadence — 5 000 t/an<br>build · v1.0 · 2026</p>\n'
            f'    </div>\n'
            f'  </article>'
        )
    if not specimens:
        return ""
    return '<div class="bk-typo-specimens">\n' + "\n".join(specimens) + '\n</div>'


def compose_photo_gallery(visual_final_dir: Path, brand: str = "") -> str:
    """
    Auto-compose la section Photo gallery en listant les PNG du dossier
    visual-final/. Filtre : seuls les fichiers .png pertinents (hero,
    atmosphere, halo, macro, pov, closeup).
    """
    if not visual_final_dir.exists() or not visual_final_dir.is_dir():
        return ""
    pngs = sorted(visual_final_dir.glob("*.png"))
    if not pngs:
        return ""
    items = []
    for p in pngs:
        rel = f"visual-final/{p.name}"
        # Inférer un label depuis le filename (suffixe après le slug brand).
        stem = p.stem
        label_parts = stem.split("-")
        label = label_parts[-1] if len(label_parts) > 1 else stem
        label_human = label.replace("_", " ").capitalize()
        items.append(
            f'  <figure class="bk-photo-gallery__item">\n'
            f'    <img src="{rel}" alt="{label_human} — {brand}" loading="lazy" />\n'
            f'    <figcaption class="bk-photo-gallery__caption">'
            f'<span class="bk-mono">{label_human}</span></figcaption>\n'
            f'  </figure>'
        )
    return '<div class="bk-photo-gallery">\n' + "\n".join(items) + '\n</div>'


def extract_batch2_css(inventory_html: str) -> str:
    """
    Récupère le CSS batch2 depuis la section <section data-inv="_css"> de
    l'inventory (déposée par extract-batch2-inventory.py). Retourne "" si
    absent (cas legacy inventory sans CSS).
    """
    m = re.search(
        r'<section\s+data-inv="_css"[^>]*>\s*(?:<!--.*?-->\s*)?<style\b[^>]*>(.*?)</style>',
        inventory_html,
        re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return ""
    return m.group(1)


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

    # Auto-composition des sections SOURCE-DRIVEN (Palette / Typo / Photo) à
    # partir des valeurs déjà fournies par le sub-agent + des fichiers visuels
    # disponibles. Permet au sub-agent de ne PAS fournir ces slots HTML — il les
    # composerait souvent mal (option B vs A : on évite les bugs récurrents de
    # "sub-agent réinvente le markup").
    if "PALETTE_PAGES_HTML" not in vars_dict:
        vars_dict["PALETTE_PAGES_HTML"] = compose_palette_pages(vars_dict)
        print(f"[INFO] Auto-composition Palette : {len(vars_dict['PALETTE_PAGES_HTML']):,} chars")
    if "TYPO_SPECIMEN_HTML" not in vars_dict:
        vars_dict["TYPO_SPECIMEN_HTML"] = compose_typo_specimens(vars_dict)
        print(f"[INFO] Auto-composition Typographie : {len(vars_dict['TYPO_SPECIMEN_HTML']):,} chars")
    if "PHOTO_GALLERY_HTML" not in vars_dict:
        visual_final_dir = output_path.parent / "visual-final"
        brand = vars_dict.get("BRAND", "")
        vars_dict["PHOTO_GALLERY_HTML"] = compose_photo_gallery(visual_final_dir, brand=brand)
        print(f"[INFO] Auto-composition Photo gallery : {len(vars_dict['PHOTO_GALLERY_HTML']):,} chars")

    # Injection automatique des 9 slots BATCH2_INVENTORY_* + récupération CSS batch2.
    batch2_css = ""
    if inventory_path:
        inventory_html = inventory_path.read_text(encoding="utf-8")
        batch2_subs = build_batch2_substitutions(inventory_html)
        # Les vars du JSON priment sur les substitutions auto (pour permettre override manuel).
        for slot_name, html_block in batch2_subs.items():
            if slot_name not in vars_dict:
                vars_dict[slot_name] = html_block
        print(f"[INFO] Injection auto batch2-inventory : 8 slots remplis")
        # Récupération du CSS batch2 pour réinjection dans le brand book final.
        # Sans ce CSS, les composants extraits (classes .glyph, .btn, .badge, .toggle,
        # .alert, .card--depth, etc.) s'affichent en HTML brut sans style → bug
        # observé Vermeil test E2E 31/05/2026.
        batch2_css = extract_batch2_css(inventory_html)
        if batch2_css:
            print(f"[INFO] CSS batch2 récupéré : {len(batch2_css):,} caractères ({len(batch2_css.splitlines()):,} lignes)")
        else:
            print(f"[WARN] Pas de CSS batch2 trouvé dans l'inventory (inventory legacy ?). Composants extraits seront non-stylés.")

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

    # Injection du CSS batch2 juste avant </head> (cascade : après le CSS template,
    # donc le CSS batch2 prend précédence pour les classes communes — souhaité car
    # les composants extraits utilisent les classes batch2).
    if batch2_css:
        css_block = (
            '\n<style data-source="batch2-inventory">\n'
            '/* CSS extrait de batch2.html via extract-batch2-inventory.py, '
            'réinjecté ici par render-brand-book.py pour styliser les composants '
            'UI / icônes / charts injectés verbatim dans le brand book. */\n'
            + batch2_css
            + '\n</style>\n'
        )
        # Insérer juste avant </head> (case-insensitive, premier match).
        m = re.search(r"</head>", output_html, re.IGNORECASE)
        if m:
            output_html = output_html[:m.start()] + css_block + output_html[m.start():]
            print(f"[OK]   CSS batch2 injecté dans le brand book ({len(batch2_css):,} chars)")
        else:
            print(f"[WARN] Pas de </head> trouvé dans le template : CSS batch2 NON injecté.")

    output_path.write_text(output_html, encoding="utf-8")
    size_kb = output_path.stat().st_size / 1024
    print(f"[OK]   Brand book écrit : {output_path} ({size_kb:,.1f} Ko, {len(output_html.splitlines()):,} lignes)")

    sys.exit(0)


if __name__ == "__main__":
    main()
