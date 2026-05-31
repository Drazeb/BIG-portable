#!/usr/bin/env python3
"""
extract-batch2-inventory.py
===========================

Extrait verbatim les composants UI / icônes / charts depuis un fichier
`{brand}-batch2.html` produit par le pipeline BIG, et produit deux artefacts :

1. `batch2-inventory.html` — document HTML autonome organisé par catégorie
   (`<section data-inv="icons">`, `<section data-inv="buttons">`, etc.) où
   chaque bloc est borné par `<!-- BEGIN_BLOCK md5=… --> … <!-- END_BLOCK -->`.
2. `batch2-inventory.json` (optionnel) — manifest des hashes MD5 par catégorie,
   consommé par le quality gate Étape 5 du skill `brand-book`.

Pourquoi ?
----------
La Phase 8 du pipeline BIG délègue à un sub-agent la composition du brand
book. Sur Atelier Vermeil (test 30/05/2026), le sub-agent a redessiné les
composants UI au lieu de les copier verbatim depuis batch2 (28 SVG
hachurés 64×64 → 20 SVG plats 32×32, 4 badges/toggles oubliés, etc.). Les
règles déclaratives du SKILL.md ne suffisent pas — le sub-agent les voit
mais les contourne.

Solution : retirer le sub-agent de la boucle de copie. Le script extrait
les composants en HTML brut, le sub-agent INJECTE ces blocs dans les
slots `{{BATCH2_INVENTORY_*}}` du template. Quality gate par hash MD5
strict (Étape 5).

Usage
-----
    python3 extract-batch2-inventory.py <batch2_html_path> <output_html_path> \
            [--json-output <report.json>] [--verbose]

Exemples
--------
    python3 .claude/skills/brand-book/scripts/extract-batch2-inventory.py \\
        outputs/test-camille-phase8-20260527/camille-batch2-le-phare-de-ralliement.html \\
        /tmp/camille-inventory.html \\
        --json-output /tmp/camille-inventory.json --verbose

Exit codes
----------
    0  OK
    1  erreur fatale (input introuvable, 0 élément extrait toutes catégories)
    2  mauvais usage CLI

Conventions
-----------
- Stdlib seule (regex + pathlib + argparse + json + hashlib + sys + datetime).
- Read-only sur la source. Écriture d'un nouveau fichier (jamais in-place —
  leçon `extract-trace.py` corrupted HTML).
- Polymorphisme conventions batch2 : listes alternatives de classes wrappers
  en constantes en tête de fichier + fallback "SVG nu" si aucun wrapper.
- Injection inline des `<defs>` référencés via `url(#xxx)` directement dans
  chaque SVG → chaque bloc est autonome et idempotent.
"""

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ============================================================================
# CONSTANTES
# ============================================================================

# Classes wrappers reconnues comme icônes (toutes les conventions BIG observées).
# Polymorphisme batch2 : Vermeil utilise .glyph, Camille utilise .icon-card,
# .stroke-step, .abstraction-step, .business-icon (spécimens grammaire icône).
# Le matching est exact OU par préfixe BEM (`target--variant`).
ICON_WRAPPER_CLASSES = [
    "glyph", "icon-card", "icon-cell", "icon-tile", "icon-spec",
    "stroke-step", "abstraction-step", "business-icon",
]

# Boutons : tous les <button class="btn..."> SAUF les tabs (catégorie séparée).
BUTTON_CLASSES = ["btn"]  # match "btn" exact ou "btn--*"

# Tabs : wrapper parent. Les <button class="tab"> individuels sont extraits
# UNE FOIS via leur wrapper (déduplication automatique).
TAB_WRAPPER_CLASSES = ["tabs", "segmented-control", "seg", "tablist", "tab-bar"]
# Pour exclure les <button class="tab"> au moment de l'extraction des buttons.
TAB_BUTTON_CLASSES = ["tab"]

# Composants UI atomiques.
BADGE_CLASSES = ["badge"]
TOGGLE_CLASSES = ["toggle"]
CHECKBOX_CLASSES = ["check", "checkbox"]

# Cards UI / KPI tiles (whitelist stricte — on évite les .card génériques qui
# foisonnent partout dans le document, ex: header cards, chapter cards).
CARD_CLASSES = [
    "kpi-card", "stat-card", "metric-card", "ui-card", "data-card",
    "card--kpi", "card--depth", "tile",
]

# Alertes / toasts.
ALERT_CLASSES = ["alert", "toast"]

# Progress / meter bars.
PROGRESS_CLASSES = ["progress", "meter"]

# Inputs wrappers (.field, .form-field, .input-wrap, .input-group) et tags input/select/textarea.
INPUT_WRAPPER_CLASSES = ["field", "form-field", "input-wrap", "input-group", "input", "select"]

# Charts dataviz : SVG avec viewBox suffisamment grand pour ne pas être une icône
# (heuristique : largeur OU hauteur >= 150 dans viewBox).
CHART_MIN_VIEWBOX_DIM = 150

# Catégories dans l'ordre d'extraction (priorité aux conteneurs avant les
# éléments atomiques → déduplication par positions consommées).
CATEGORIES = [
    "icons", "buttons", "inputs", "badges", "toggles", "checkboxes",
    "cards", "tabs", "alerts", "progress", "charts",
]


# ============================================================================
# DATACLASS
# ============================================================================

@dataclass
class Component:
    """Un bloc HTML extrait verbatim depuis batch2."""
    category: str
    source_line: int
    source_wrapper_class: str  # classe principale du wrapper (.glyph, .btn--primary, etc.)
    source_viewbox: str  # "64 64" pour SVG, "" sinon
    block_html: str  # le bloc verbatim (après injection defs si SVG)
    md5: str  # hashlib.md5(block_html.encode("utf-8")).hexdigest()
    label: str  # aria-label / texte court / "" sinon
    source_pos_start: int = 0  # position byte dans le source (pour dédup)
    source_pos_end: int = 0


# ============================================================================
# HELPERS GÉNÉRIQUES
# ============================================================================

def line_at_pos(html: str, pos: int) -> int:
    """Numéro de ligne (1-indexed) pour la position byte."""
    return html.count("\n", 0, pos) + 1


def compute_md5(block_html: str) -> str:
    """MD5 sur le bloc normalisé (strip whitespace de bord)."""
    return hashlib.md5(block_html.strip().encode("utf-8")).hexdigest()


def find_balanced_block(html: str, start: int, tag_name: str) -> Optional[tuple]:
    """
    À partir de `start` (position pointant sur `<{tag_name}`), trouve la fin
    du bloc équilibré. Retourne (start, end_exclusif) ou None.

    Gère les tags self-closing (`<input/>`) en détectant `/>` à la fin de
    l'opening tag. Gère les imbrications du MÊME tag via un compteur de
    profondeur.

    Ne gère PAS les commentaires HTML imbriqués qui contiendraient des tags
    factices — cas non observé dans les batch2 BIG.
    """
    open_re = re.compile(
        rf"<{re.escape(tag_name)}\b[^>]*?(/?)>",
        re.DOTALL | re.IGNORECASE,
    )
    open_match = open_re.match(html, start)
    if not open_match:
        return None
    # Self-closing.
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


def extract_viewbox(svg_block: str) -> str:
    """Extrait `width height` depuis viewBox=\"0 0 W H\". Retourne \"\" si absent."""
    m = re.search(r'viewBox\s*=\s*"\s*\d+\s+\d+\s+(\d+)\s+(\d+)\s*"', svg_block)
    if not m:
        return ""
    return f"{m.group(1)} {m.group(2)}"


def extract_label(block: str) -> str:
    """Tire un label depuis aria-label, data-name ou un span/div .__name/.__label."""
    for pattern in (
        r'aria-label\s*=\s*"([^"]+)"',
        r'data-name\s*=\s*"([^"]+)"',
        r'data-label\s*=\s*"([^"]+)"',
        r'class="[^"]*__label[^"]*"[^>]*>([^<]+)<',
        r'class="[^"]*__name[^"]*"[^>]*>([^<]+)<',
    ):
        m = re.search(pattern, block)
        if m:
            return m.group(1).strip()[:80]
    return ""


def extract_primary_class(block: str, target_classes: list) -> str:
    """Extrait la classe principale du wrapper : premier match exact ou BEM dans target_classes."""
    m = re.search(r'class\s*=\s*"([^"]+)"', block)
    if not m:
        return ""
    classes_in_attr = m.group(1).split()
    for cls in classes_in_attr:
        for target in target_classes:
            if cls == target or cls.startswith(target + "--"):
                return cls
    return classes_in_attr[0] if classes_in_attr else ""


# ============================================================================
# DEFS INDEX (gère url(#xxx) référencés via <defs> centralisés)
# ============================================================================

def extract_inline_css(html: str) -> str:
    """
    Extrait le contenu CONCATÉNÉ de tous les <style>...</style> du document batch2.

    Pourquoi : sans ce CSS, les composants UI/icônes/charts injectés verbatim
    dans le brand book s'affichent en HTML brut (classes `.glyph`, `.btn--*`,
    `.toggle__track`, `.badge--*`, etc. non définies) → rendu cassé / invisible.

    Bug observé Vermeil test E2E 31/05/2026 : section Composants UI quasi
    vide, section Dataviz vide alors que les hashes MD5 disaient 46/46 OK.

    Le CSS extrait est inclus dans `batch2-inventory.html` sous une section
    `<section data-inv="_css" hidden>` et réinjecté dans le brand book final
    par `render-brand-book.py`.
    """
    blocks = re.findall(r"<style\b[^>]*>(.*?)</style>", html, re.DOTALL | re.IGNORECASE)
    return "\n".join(blocks)


def build_defs_index(html: str) -> dict:
    """
    Scanne TOUS les <defs>...</defs> du document (qu'ils soient dans un SVG
    visible ou dans un SVG width="0" invisible servant de catalogue). Tag par
    `id="xxx"` chaque enfant direct.

    Retourne dict {id → element_html} pour injection inline ultérieure.
    """
    defs_index = {}
    defs_pattern = re.compile(r"<defs\b[^>]*>(.*?)</defs>", re.DOTALL | re.IGNORECASE)
    for defs_match in defs_pattern.finditer(html):
        defs_content = defs_match.group(1)
        # Pour chaque tag avec id="xxx" dans le defs, capturer l'élément complet.
        # On utilise find_balanced_block sur les positions absolues dans le contenu.
        pos = 0
        while True:
            child_match = re.search(
                r'<(\w+)\b[^>]*\bid\s*=\s*"([^"]+)"',
                defs_content[pos:],
            )
            if not child_match:
                break
            tag_name = child_match.group(1)
            element_id = child_match.group(2)
            child_start = pos + child_match.start()
            balanced = find_balanced_block(defs_content, child_start, tag_name)
            if balanced is None:
                pos = pos + child_match.end()
                continue
            block = defs_content[balanced[0]:balanced[1]]
            defs_index[element_id] = block
            pos = balanced[1]
    return defs_index


def inject_defs_inline(svg_block: str, defs_index: dict, warnings: list) -> str:
    """
    Pour un bloc SVG donné, scanne `url(#xxx)` et injecte les <defs> nécessaires
    juste après la balise <svg> ouvrante. Si le SVG a déjà un <defs> interne,
    fusionne dedans. Garantit que le SVG devient autonome (rendable hors contexte).
    """
    refs = set(re.findall(r"url\(#([a-zA-Z0-9_\-]+)\)", svg_block))
    if not refs:
        return svg_block

    # Defs nécessaires (présents dans l'index).
    needed = []
    for ref in refs:
        if ref in defs_index:
            needed.append(defs_index[ref])
        else:
            warnings.append(f"SVG référence url(#{ref}) introuvable dans defs_index")

    if not needed:
        return svg_block

    inject_html = "<defs>" + "".join(needed) + "</defs>"

    # Si le SVG a déjà un <defs> interne, fusionner dedans.
    existing_defs = re.search(r"<defs\b[^>]*>", svg_block)
    if existing_defs:
        return (
            svg_block[: existing_defs.end()]
            + "".join(needed)
            + svg_block[existing_defs.end():]
        )

    # Sinon, injecter juste après le <svg ...>.
    svg_open = re.match(r"<svg\b[^>]*>", svg_block)
    if not svg_open:
        return svg_block
    return svg_block[: svg_open.end()] + inject_html + svg_block[svg_open.end():]


# ============================================================================
# EXTRACTEURS PAR CATÉGORIE
# ============================================================================

def _class_matches_any(classes_in_attr: list, target_classes: list) -> bool:
    """
    Match si AU MOINS une classe de l'attribut correspond à un target :
    - match exact (classe == target)
    - match BEM par préfixe (classe.startswith(target + "--"))
    """
    for cls in classes_in_attr:
        for target in target_classes:
            if cls == target or cls.startswith(target + "--"):
                return True
    return False


def _find_wrappers_by_classes(html: str, tag_names: list, target_classes: list) -> list:
    """
    Trouve toutes les balises ouvrantes `<tag>` dont au moins UNE des classes
    matche (exact ou BEM préfixe) UN des target_classes.
    Retourne liste triée de (tag_name, position_start).
    """
    found = []
    for tag_name in tag_names:
        pattern = re.compile(
            rf'<{re.escape(tag_name)}\b[^>]*\bclass\s*=\s*"([^"]+)"',
            re.IGNORECASE,
        )
        for m in pattern.finditer(html):
            classes_in_attr = m.group(1).split()
            if _class_matches_any(classes_in_attr, target_classes):
                found.append((tag_name, m.start()))
    found.sort(key=lambda x: x[1])
    return found


def extract_icons(html: str, defs_index: dict, consumed: set, warnings: list) -> list:
    """
    Extraction icônes :
    1. Cherche tous les wrappers <div class="{ICON_WRAPPER_CLASSES}">.
    2. Pour chaque wrapper trouvé, extrait le bloc équilibré et injecte les defs
       inline dans les SVG internes.
    """
    components = []
    found = _find_wrappers_by_classes(html, ["div"], ICON_WRAPPER_CLASSES)
    for tag_name, start in found:
        if start in consumed:
            continue
        balanced = find_balanced_block(html, start, tag_name)
        if balanced is None:
            continue
        block = html[balanced[0]:balanced[1]]
        # Injecter defs dans tous les SVG du bloc.
        block_with_defs = re.sub(
            r"<svg\b.*?</svg>",
            lambda m: inject_defs_inline(m.group(0), defs_index, warnings),
            block,
            flags=re.DOTALL,
        )
        viewbox = extract_viewbox(block_with_defs)
        label = extract_label(block)
        wrapper_class = extract_primary_class(block, ICON_WRAPPER_CLASSES)
        components.append(Component(
            category="icons",
            source_line=line_at_pos(html, start),
            source_wrapper_class=wrapper_class,
            source_viewbox=viewbox,
            block_html=block_with_defs,
            md5=compute_md5(block_with_defs),
            label=label,
            source_pos_start=balanced[0],
            source_pos_end=balanced[1],
        ))
        # Marquer toutes les positions à l'intérieur du bloc comme consommées.
        for p in range(balanced[0], balanced[1]):
            consumed.add(p)

    return components


def extract_charts(html: str, defs_index: dict, consumed: set, warnings: list) -> list:
    """
    Extraction charts dataviz : SVG avec viewBox > CHART_MIN_VIEWBOX_DIM dans
    AU MOINS UNE dimension. Inclut son wrapper s'il y en a un (.viz, .chart-card).
    """
    components = []
    svg_pattern = re.compile(r"<svg\b", re.IGNORECASE)
    for m in svg_pattern.finditer(html):
        if m.start() in consumed:
            continue
        balanced = find_balanced_block(html, m.start(), "svg")
        if balanced is None:
            continue
        svg_block = html[balanced[0]:balanced[1]]
        viewbox = extract_viewbox(svg_block)
        if not viewbox:
            continue
        try:
            w, h = (int(x) for x in viewbox.split())
        except ValueError:
            continue
        if max(w, h) < CHART_MIN_VIEWBOX_DIM:
            continue
        # Exclure les SVG width="0" (defs invisibles).
        if 'width="0"' in svg_block[:200] and 'height="0"' in svg_block[:200]:
            continue

        block_with_defs = inject_defs_inline(svg_block, defs_index, warnings)
        components.append(Component(
            category="charts",
            source_line=line_at_pos(html, m.start()),
            source_wrapper_class="",
            source_viewbox=viewbox,
            block_html=block_with_defs,
            md5=compute_md5(block_with_defs),
            label=extract_label(svg_block),
            source_pos_start=balanced[0],
            source_pos_end=balanced[1],
        ))
        for p in range(balanced[0], balanced[1]):
            consumed.add(p)
    return components


def extract_tabs(html: str, consumed: set) -> list:
    """Extraction tabs : wrappers <div class="tabs|segmented-control|seg|tablist">."""
    components = []
    found = _find_wrappers_by_classes(html, ["div", "nav"], TAB_WRAPPER_CLASSES)
    for tag_name, start in found:
        if start in consumed:
            continue
        balanced = find_balanced_block(html, start, tag_name)
        if balanced is None:
            continue
        block = html[balanced[0]:balanced[1]]
        components.append(Component(
            category="tabs",
            source_line=line_at_pos(html, start),
            source_wrapper_class=extract_primary_class(block, TAB_WRAPPER_CLASSES),
            source_viewbox="",
            block_html=block,
            md5=compute_md5(block),
            label=extract_label(block),
            source_pos_start=balanced[0],
            source_pos_end=balanced[1],
        ))
        for p in range(balanced[0], balanced[1]):
            consumed.add(p)
    return components


def extract_buttons(html: str, consumed: set) -> list:
    """
    Extraction boutons : <button> dont la classe match `btn` (exact ou BEM).
    SKIP les <button class="tab"> (déjà extraits comme tabs) et les boutons
    déjà consommés (à l'intérieur d'un wrapper de tabs par exemple).
    """
    components = []
    pattern = re.compile(
        r'<button\b[^>]*\bclass\s*=\s*"([^"]+)"',
        re.IGNORECASE,
    )
    for m in pattern.finditer(html):
        if m.start() in consumed:
            continue
        classes_in_attr = m.group(1).split()
        # Exclure les tabs.
        if _class_matches_any(classes_in_attr, TAB_BUTTON_CLASSES):
            continue
        if not _class_matches_any(classes_in_attr, BUTTON_CLASSES):
            continue
        balanced = find_balanced_block(html, m.start(), "button")
        if balanced is None:
            continue
        block = html[balanced[0]:balanced[1]]
        # Tirer la classe principale (premier match dans BUTTON_CLASSES).
        primary_class = next(
            (c for c in classes_in_attr if c in BUTTON_CLASSES
             or any(c.startswith(t + "--") for t in BUTTON_CLASSES)),
            classes_in_attr[0],
        )
        components.append(Component(
            category="buttons",
            source_line=line_at_pos(html, m.start()),
            source_wrapper_class=primary_class,
            source_viewbox="",
            block_html=block,
            md5=compute_md5(block),
            label=re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", block)).strip()[:60],
            source_pos_start=balanced[0],
            source_pos_end=balanced[1],
        ))
        for p in range(balanced[0], balanced[1]):
            consumed.add(p)
    return components


def extract_inputs(html: str, consumed: set) -> list:
    """
    Extraction inputs : wrappers <div|label class="field|form-field|input|select|...">
    qui contiennent un <input>, <select> ou <textarea>. + inputs nus restants.
    """
    components = []
    found = _find_wrappers_by_classes(html, ["div", "label"], INPUT_WRAPPER_CLASSES)
    for tag_name, start in found:
        if start in consumed:
            continue
        balanced = find_balanced_block(html, start, tag_name)
        if balanced is None:
            continue
        block = html[balanced[0]:balanced[1]]
        # On ne garde que les wrappers qui contiennent un <input>, <select> ou <textarea>.
        if not re.search(r"<(input|select|textarea)\b", block, re.IGNORECASE):
            continue
        components.append(Component(
            category="inputs",
            source_line=line_at_pos(html, start),
            source_wrapper_class=extract_primary_class(block, INPUT_WRAPPER_CLASSES),
            source_viewbox="",
            block_html=block,
            md5=compute_md5(block),
            label=extract_label(block),
            source_pos_start=balanced[0],
            source_pos_end=balanced[1],
        ))
        for p in range(balanced[0], balanced[1]):
            consumed.add(p)
    # Pas de fallback "input nu" : les <input> orphelins à l'intérieur de toggles
    # ou checkboxes sont déjà captés via leur wrapper de catégorie respective.
    return components


def _extract_simple_wrappers(
    html: str,
    consumed: set,
    category: str,
    tag_names: list,
    target_classes: list,
) -> list:
    """Helper générique pour badges, toggles, checkboxes, alerts, progress, cards."""
    components = []
    found = _find_wrappers_by_classes(html, tag_names, target_classes)
    for tag_name, start in found:
        if start in consumed:
            continue
        balanced = find_balanced_block(html, start, tag_name)
        if balanced is None:
            continue
        block = html[balanced[0]:balanced[1]]
        components.append(Component(
            category=category,
            source_line=line_at_pos(html, start),
            source_wrapper_class=extract_primary_class(block, target_classes),
            source_viewbox="",
            block_html=block,
            md5=compute_md5(block),
            label=extract_label(block) or re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", block)).strip()[:60],
            source_pos_start=balanced[0],
            source_pos_end=balanced[1],
        ))
        for p in range(balanced[0], balanced[1]):
            consumed.add(p)
    return components


def extract_badges(html: str, consumed: set) -> list:
    return _extract_simple_wrappers(html, consumed, "badges", ["span", "div"], BADGE_CLASSES)


def extract_toggles(html: str, consumed: set) -> list:
    return _extract_simple_wrappers(html, consumed, "toggles", ["label", "div", "button"], TOGGLE_CLASSES)


def extract_checkboxes(html: str, consumed: set) -> list:
    return _extract_simple_wrappers(html, consumed, "checkboxes", ["label", "div"], CHECKBOX_CLASSES)


def extract_alerts(html: str, consumed: set) -> list:
    return _extract_simple_wrappers(html, consumed, "alerts", ["div", "aside"], ALERT_CLASSES)


def extract_progress(html: str, consumed: set) -> list:
    return _extract_simple_wrappers(html, consumed, "progress", ["div", "progress"], PROGRESS_CLASSES)


def extract_cards(html: str, consumed: set) -> list:
    """
    Cards UI : on accepte
    - <article class="card[ --variant]"> : convention Vermeil (cards éditoriales documentées)
    - <div|article class="kpi-card|stat-card|metric-card|...">: whitelist stricte
    On évite les <div class="card"> seul (chapter headers génériques foisonnent).
    """
    article_classes = ["card"] + CARD_CLASSES
    found = _find_wrappers_by_classes(html, ["article"], article_classes)
    found += _find_wrappers_by_classes(html, ["div"], CARD_CLASSES)
    found.sort(key=lambda x: x[1])
    components = []
    for tag_name, start in found:
        if start in consumed:
            continue
        balanced = find_balanced_block(html, start, tag_name)
        if balanced is None:
            continue
        block = html[balanced[0]:balanced[1]]
        components.append(Component(
            category="cards",
            source_line=line_at_pos(html, start),
            source_wrapper_class=extract_primary_class(block, article_classes),
            source_viewbox="",
            block_html=block,
            md5=compute_md5(block),
            label=extract_label(block) or re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", block)).strip()[:60],
            source_pos_start=balanced[0],
            source_pos_end=balanced[1],
        ))
        for p in range(balanced[0], balanced[1]):
            consumed.add(p)
    return components


# ============================================================================
# RENDER : HTML + JSON
# ============================================================================

INVENTORY_HTML_TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Batch2 Inventory — {brand}</title>
<style>
  body {{ font: 14px/1.5 system-ui, sans-serif; margin: 24px; background: #f7f8fa; color: #14181f; }}
  header {{ margin-bottom: 32px; padding-bottom: 16px; border-bottom: 1px solid #d0d4dc; }}
  h1 {{ margin: 0 0 8px; font-size: 22px; }}
  .meta {{ color: #57606a; font-size: 12px; font-family: ui-monospace, monospace; }}
  section[data-inv] {{ background: #fff; border: 1px solid #d0d4dc; border-radius: 8px; padding: 20px; margin-bottom: 24px; }}
  section[data-inv] > h2 {{ margin: 0 0 16px; font-size: 16px; color: #14181f; }}
  article {{ display: inline-block; margin: 8px; padding: 12px; border: 1px dashed #d0d4dc; border-radius: 6px; vertical-align: top; background: #fff; }}
  article > .article-meta {{ display: block; font: 11px ui-monospace, monospace; color: #57606a; margin-bottom: 8px; }}
</style>
</head>
<body>
<header>
  <h1>Batch2 Inventory — {brand}</h1>
  <p class="meta">Source: {source_path}<br>{total_count} composants extraits · généré le {generated_at}</p>
</header>
{sections_html}
</body>
</html>
"""


def _slug_brand_from_path(source_path: Path) -> str:
    """Tire un slug brand depuis le nom de fichier (ex: camille-batch2-le-phare-...)."""
    stem = source_path.stem
    if "-batch2" in stem:
        return stem.split("-batch2")[0]
    return stem


def render_inventory_html(
    components_by_category: dict,
    source_path: Path,
    brand: str,
    total_count: int,
    batch2_css: str = "",
) -> str:
    sections_html = []
    # Section _css cachée : CSS batch2 verbatim, sera réinjecté par render-brand-book.py
    # dans le brand book final pour styliser les composants extraits.
    if batch2_css:
        sections_html.append(
            f'<section data-inv="_css" hidden aria-hidden="true">\n'
            f'  <!-- CSS verbatim extrait de batch2.html — réinjecté dans le brand book\n'
            f'       par render-brand-book.py pour styliser les composants UI/icônes/charts. -->\n'
            f'  <style data-source="batch2-inventory">{batch2_css}</style>\n'
            f'</section>'
        )
    for cat in CATEGORIES:
        items = components_by_category.get(cat, [])
        if not items:
            sections_html.append(
                f'<section data-inv="{cat}" data-count="0">\n'
                f'  <h2>{cat.capitalize()} (0)</h2>\n'
                f'  <p style="color:#999;font-style:italic">Aucun composant extrait pour cette catégorie.</p>\n'
                f'</section>'
            )
            continue
        articles = []
        for c in items:
            meta = (
                f'data-component="{c.category}" data-md5="{c.md5}" '
                f'data-source-line="{c.source_line}" '
                f'data-source-wrapper="{c.source_wrapper_class}" '
                f'data-source-viewbox="{c.source_viewbox}" '
                f'data-label="{c.label}"'
            )
            articles.append(
                f'  <article {meta}>\n'
                f'    <span class="article-meta">md5={c.md5[:12]}… · line={c.source_line} · {c.label or "—"}</span>\n'
                f'    <!-- BEGIN_BLOCK md5={c.md5} -->\n'
                f'    {c.block_html}\n'
                f'    <!-- END_BLOCK -->\n'
                f'  </article>'
            )
        sections_html.append(
            f'<section data-inv="{cat}" data-count="{len(items)}">\n'
            f'  <h2>{cat.capitalize()} ({len(items)})</h2>\n'
            + "\n".join(articles) + "\n"
            f'</section>'
        )
    return INVENTORY_HTML_TEMPLATE.format(
        brand=brand,
        source_path=str(source_path),
        total_count=total_count,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        sections_html="\n".join(sections_html),
    )


def render_json_manifest(
    components_by_category: dict,
    source_path: Path,
    brand: str,
) -> dict:
    categories_data = {}
    total = 0
    for cat in CATEGORIES:
        items = components_by_category.get(cat, [])
        total += len(items)
        categories_data[cat] = {
            "count": len(items),
            "items": [
                {
                    "md5": c.md5,
                    "label": c.label,
                    "source_line": c.source_line,
                    "source_viewbox": c.source_viewbox,
                    "source_wrapper": c.source_wrapper_class,
                }
                for c in items
            ],
        }
    return {
        "brand": brand,
        "source_path": str(source_path),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "categories": categories_data,
        "totals": {"all": total},
    }


# ============================================================================
# POST-CHECKS
# ============================================================================

def post_checks(components_by_category: dict, warnings: list) -> tuple:
    """Vérifications post-extraction. Retourne (deterministic_fails, soft_warns)."""
    fails = []
    warns = list(warnings)

    # MD5 reproductible : pour chaque composant, recalculer le hash et comparer.
    for cat, items in components_by_category.items():
        for c in items:
            recomputed = compute_md5(c.block_html)
            if recomputed != c.md5:
                fails.append(f"MD5 non reproductible pour {cat} ligne {c.source_line}")

    # Doublons par MD5 dans une même catégorie.
    for cat, items in components_by_category.items():
        seen = {}
        for c in items:
            if c.md5 in seen:
                warns.append(
                    f"Doublon MD5 dans {cat} (lignes {seen[c.md5]} et {c.source_line})"
                )
            else:
                seen[c.md5] = c.source_line

    return fails, warns


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Extract verbatim UI components from a batch2.html into an inventory.",
    )
    parser.add_argument("batch2_html_path", type=str, help="Path to {brand}-batch2.html")
    parser.add_argument("output_html_path", type=str, help="Path to write the inventory HTML")
    parser.add_argument("--json-output", type=str, default=None, help="Optional JSON manifest path")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    src = Path(args.batch2_html_path).resolve()
    dst_html = Path(args.output_html_path).resolve()
    dst_json = Path(args.json_output).resolve() if args.json_output else None

    if not src.exists():
        print(f"[ERROR] Le fichier source n'existe pas : {src}")
        sys.exit(1)
    if not src.is_file():
        print(f"[ERROR] Le chemin source n'est pas un fichier : {src}")
        sys.exit(1)

    dst_html.parent.mkdir(parents=True, exist_ok=True)
    if dst_json:
        dst_json.parent.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Source     : {src}")
    print(f"[INFO] Output HTML: {dst_html}")
    if dst_json:
        print(f"[INFO] Output JSON: {dst_json}")

    html = src.read_text(encoding="utf-8")
    brand = _slug_brand_from_path(src)
    print(f"[INFO] Brand slug : {brand}")
    print(f"[INFO] Source size: {len(html):,} octets ({len(html.splitlines()):,} lignes)")

    # Index des defs.
    defs_index = build_defs_index(html)
    print(f"[INFO] Defs index : {len(defs_index)} éléments indexés ({', '.join(sorted(defs_index)[:8])}{'…' if len(defs_index) > 8 else ''})")

    # Extraction du CSS batch2 (pour réinjection dans le brand book final).
    batch2_css = extract_inline_css(html)
    print(f"[INFO] CSS batch2 : {len(batch2_css):,} caractères extraits ({len(batch2_css.splitlines()):,} lignes)")

    # Extraction par catégorie. Ordre : conteneurs (icons/charts/tabs/cards) AVANT
    # composants à input interne (toggles/checkboxes) AVANT inputs (qui ne prend
    # que les wrappers .field/.input/.select, pas les inputs nus à l'intérieur
    # d'un toggle ou checkbox) AVANT atomes simples (badges/buttons).
    warnings = []
    consumed = set()

    components_by_category = {}
    components_by_category["icons"] = extract_icons(html, defs_index, consumed, warnings)
    components_by_category["charts"] = extract_charts(html, defs_index, consumed, warnings)
    components_by_category["tabs"] = extract_tabs(html, consumed)
    components_by_category["cards"] = extract_cards(html, consumed)
    components_by_category["toggles"] = extract_toggles(html, consumed)
    components_by_category["checkboxes"] = extract_checkboxes(html, consumed)
    components_by_category["inputs"] = extract_inputs(html, consumed)
    components_by_category["alerts"] = extract_alerts(html, consumed)
    components_by_category["progress"] = extract_progress(html, consumed)
    components_by_category["badges"] = extract_badges(html, consumed)
    components_by_category["buttons"] = extract_buttons(html, consumed)

    # Post-checks.
    fails, warns = post_checks(components_by_category, warnings)

    # Reporting.
    total = sum(len(v) for v in components_by_category.values())
    print(f"[OK]   Total extrait : {total} composants")
    for cat in CATEGORIES:
        n = len(components_by_category.get(cat, []))
        print(f"         {cat:11s}: {n:3d}")

    if args.verbose:
        for cat, items in components_by_category.items():
            for c in items[:5]:
                print(f"         [{cat}] line={c.source_line} md5={c.md5[:8]} label='{c.label}' viewbox='{c.source_viewbox}'")

    for w in warns:
        print(f"[WARN] {w}")
    for f in fails:
        print(f"[FAIL] {f}")

    if total == 0:
        print("[ERROR] 0 composant extrait toutes catégories. Vérifier le format de batch2.")
        sys.exit(1)

    # Render.
    inventory_html = render_inventory_html(components_by_category, src, brand, total, batch2_css=batch2_css)
    dst_html.write_text(inventory_html, encoding="utf-8")
    print(f"[OK]   Inventory HTML écrit : {dst_html} ({dst_html.stat().st_size:,} octets)")

    if dst_json:
        manifest = render_json_manifest(components_by_category, src, brand)
        dst_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK]   Manifest JSON écrit  : {dst_json} ({dst_json.stat().st_size:,} octets)")

    if fails:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
