#!/usr/bin/env python3
"""
capture-x-mockup.py
===================

Capture viewport PNG d'un mockup X (Twitter) HTML via Playwright (headless Chromium).

Usage
-----
    python3 capture-x-mockup.py <input_html_path> <output_png_path>

Exemples
--------
    python3 .claude/skills/brand-book/scripts/capture-x-mockup.py \\
        .claude/skills/brand-book/outputs/camille-test-v2/camille-x-mockup.html \\
        .claude/skills/brand-book/outputs/camille-test-v2/camille-x-mockup.png

Dépendances
-----------
    pip install playwright
    playwright install chromium

Différences avec capture-linkedin-mockup.py
-------------------------------------------
- Viewport 1000x1000 : format quasi-carré pour s'intégrer dans le diptyque
  social 08c du brand book à côté du LinkedIn (lui aussi en 1000x1000).
  Tailles internes du mockup recalibrées en conséquence (avatar 200px,
  nom 30px, bio 20px, méta 18px, etc.) pour rester fidèle à la proportion
  de la zone profil X desktop (cf. référence Khairallah AL-Awady).
- device_scale_factor=2 (retina) : identique à LinkedIn — capture haute résolution
  pour rendu net au zoom dans le brand book.
- full_page=False : on capture le viewport.

Notes d'implémentation
----------------------
- Attente : networkidle + 2s pour laisser charger Google Fonts (FOUT puis FOIT)
  et l'image cover (visual-final/*.jpg).
- Mode LIGHT X — le X officiel ne change jamais son UI. Le fond blanc est
  intrinsèque au template, pas besoin de l'imposer via le navigateur.
"""

import sys
from pathlib import Path

# Viewport quasi-carré 1000x1000 — format aligné sur LinkedIn pour le diptyque
# social 08c du brand book.
VIEWPORT_WIDTH = 1000
VIEWPORT_HEIGHT = 1000

# Retina x2 — le mockup sera affiché à taille réduite dans le brand book.
DEVICE_SCALE_FACTOR = 2

# Attente supplémentaire après networkidle pour Google Fonts + image cover.
EXTRA_WAIT_MS = 2000


def print_usage():
    """Affiche l'usage et quitte."""
    print(__doc__)
    print("\nUsage: python3 capture-x-mockup.py <input_html_path> <output_png_path>\n")
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

    print(f"[INFO] Source HTML       : {input_html_path}")
    print(f"[INFO] Output PNG        : {output_png_path}")
    print(f"[INFO] Viewport          : {VIEWPORT_WIDTH}x{VIEWPORT_HEIGHT}")
    print(f"[INFO] Device scale (DPR): {DEVICE_SCALE_FACTOR}x (retina)")
    print(f"[INFO] Lancement de headless Chromium…")

    # Conversion en file:// URI pour résolution des chemins relatifs (visual-final/, etc.).
    file_url = input_html_path.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            context = browser.new_context(
                viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
                device_scale_factor=DEVICE_SCALE_FACTOR,
            )
            page = context.new_page()

            # Navigation avec attente networkidle (toutes les requêtes réseau terminées).
            page.goto(file_url, wait_until="networkidle", timeout=30000)

            # Attente explicite que document.fonts soit ready (Google Fonts chargées).
            try:
                page.evaluate("document.fonts.ready")
            except Exception:
                # Pas bloquant — networkidle a déjà attendu, on continue.
                pass

            # Buffer supplémentaire pour le rendering final (FOIT → FOUT swap).
            page.wait_for_timeout(EXTRA_WAIT_MS)

            # Capture du viewport uniquement (pas full_page).
            page.screenshot(
                path=str(output_png_path),
                full_page=False,
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
    width, height = _read_png_dimensions(output_png_path)

    print(f"[OK]   Capture réussie.")
    print(f"[OK]   Fichier      : {output_png_path}")
    print(f"[OK]   Taille       : {size_mb:.2f} Mo ({size_bytes:,} octets)")
    if width and height:
        print(f"[OK]   Dimensions   : {width} x {height} px (logique : {width // DEVICE_SCALE_FACTOR} x {height // DEVICE_SCALE_FACTOR})")


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
