#!/usr/bin/env python3
"""
capture-style-tile.py
=====================

Capture full-page PNG d'un style-tile HTML via Playwright (headless Chromium).

Usage
-----
    python3 capture-style-tile.py <input_html_path> <output_png_path>

Exemples
--------
    python3 .claude/skills/brand-book/scripts/capture-style-tile.py \\
        outputs/camille-test-20260511/camille-style-tile-concept-3.html \\
        .claude/skills/brand-book/outputs/camille-test-v1/camille-landing-fullpage.png

Dépendances
-----------
    pip install playwright
    playwright install chromium

Pourquoi un PNG plutôt qu'une iframe ?
--------------------------------------
Les iframes posent des problèmes insolubles de scaling et de scroll horizontal
quand on intègre un style-tile dans un brand book. Une capture PNG full-page
rendue en headless Chromium à viewport 1280×800 (taille canonique du style-tile)
capture fidèlement le rendu, et on l'insère ensuite comme <img> dans le brand
book — sur fond gradient palette + drop-shadow directionnel pour la matérialité.

Notes d'implémentation
----------------------
- Viewport canonique : 1280×800 (largeur du style-tile BIG).
- Capture full_page=True : Playwright capture toute la hauteur de la page,
  pas seulement le viewport.
- Attente : networkidle + 2s de stabilisation supplémentaire — laisse le
  temps aux Google Fonts de charger et aux éventuelles images distantes
  (visual-final/) de s'afficher.
- Le PNG est sauvegardé en device-scale-factor 1 (pas de retina ×2) pour
  éviter des PNG de 8-15 Mo qui ralentiraient le brand book.
"""

import sys
from pathlib import Path

# Viewport canonique du style-tile BIG.
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 800

# Attente supplémentaire après networkidle pour laisser charger les Google Fonts.
EXTRA_WAIT_MS = 2000


def print_usage():
    """Affiche l'usage et quitte."""
    print(__doc__)
    print("\nUsage: python3 capture-style-tile.py <input_html_path> <output_png_path>\n")
    sys.exit(2)


def main():
    if len(sys.argv) != 3:
        print_usage()

    input_html_path = Path(sys.argv[1]).resolve()
    output_png_path = Path(sys.argv[2]).resolve()

    # Validation de l'input.
    if not input_html_path.exists():
        print(f"[ERROR] Le fichier HTML source n'existe pas : {input_html_path}")
        sys.exit(1)
    if not input_html_path.is_file():
        print(f"[ERROR] Le chemin source n'est pas un fichier : {input_html_path}")
        sys.exit(1)

    # Création du dossier output si nécessaire.
    output_png_path.parent.mkdir(parents=True, exist_ok=True)

    # Import Playwright en garde-fou — message clair si non installé.
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[ERROR] Playwright n'est pas installé.")
        print()
        print("Installer avec :")
        print("    pip install playwright")
        print("    playwright install chromium")
        print()
        sys.exit(1)

    print(f"[INFO] Source HTML  : {input_html_path}")
    print(f"[INFO] Output PNG   : {output_png_path}")
    print(f"[INFO] Viewport     : {VIEWPORT_WIDTH}x{VIEWPORT_HEIGHT}")
    print(f"[INFO] Lancement de headless Chromium…")

    # Conversion en file:// URI pour que les ressources relatives (Google Fonts,
    # visual-final/) soient résolues correctement.
    file_url = input_html_path.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            context = browser.new_context(
                viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
                device_scale_factor=1,  # pas de retina x2 — fichier plus léger
            )
            page = context.new_page()

            # Navigation avec attente networkidle (toutes les requêtes réseau terminées).
            page.goto(file_url, wait_until="networkidle", timeout=30000)

            # Wait additionnel pour laisser charger les Google Fonts (FOUT puis FOIT).
            page.wait_for_timeout(EXTRA_WAIT_MS)

            # Capture full-page (toute la hauteur du document, pas seulement le viewport).
            page.screenshot(
                path=str(output_png_path),
                full_page=True,
                type="png",
            )
        finally:
            browser.close()

    # Vérification post-capture et reporting.
    if not output_png_path.exists():
        print(f"[ERROR] La capture a échoué : {output_png_path} n'existe pas.")
        sys.exit(1)

    size_bytes = output_png_path.stat().st_size
    size_mb = size_bytes / (1024 * 1024)

    # Lire les dimensions de la PNG sans dépendance externe.
    # Format PNG : signature 8 octets + chunk IHDR avec largeur (4 octets) et hauteur (4 octets)
    # à partir de l'octet 16.
    width, height = _read_png_dimensions(output_png_path)

    print(f"[OK]   Capture réussie.")
    print(f"[OK]   Fichier      : {output_png_path}")
    print(f"[OK]   Taille       : {size_mb:.2f} Mo ({size_bytes:,} octets)")
    if width and height:
        print(f"[OK]   Dimensions   : {width} x {height} px")


def _read_png_dimensions(png_path: Path):
    """Lit les dimensions d'une PNG sans dépendance externe (parsing du chunk IHDR)."""
    try:
        with open(png_path, "rb") as f:
            header = f.read(24)
        if len(header) < 24:
            return (None, None)
        # Vérifier signature PNG.
        if header[:8] != b"\x89PNG\r\n\x1a\n":
            return (None, None)
        # Largeur = octets 16-19, hauteur = octets 20-23 (big-endian).
        width = int.from_bytes(header[16:20], byteorder="big")
        height = int.from_bytes(header[20:24], byteorder="big")
        return (width, height)
    except Exception:
        return (None, None)


if __name__ == "__main__":
    main()
