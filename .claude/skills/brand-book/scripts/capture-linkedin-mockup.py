#!/usr/bin/env python3
"""
capture-linkedin-mockup.py
==========================

Capture viewport PNG d'un mockup LinkedIn HTML via Playwright (headless Chromium).

Usage
-----
    python3 capture-linkedin-mockup.py <input_html_path> <output_png_path>

Exemples
--------
    python3 .claude/skills/brand-book/scripts/capture-linkedin-mockup.py \\
        .claude/skills/brand-book/outputs/camille-test-v2/camille-linkedin-mockup.html \\
        .claude/skills/brand-book/outputs/camille-test-v2/camille-linkedin-mockup.png

Dépendances
-----------
    pip install playwright
    playwright install chromium

Différences avec capture-style-tile.py
--------------------------------------
- Viewport 1000x1000 (format quasi-carré aligné sur capture-x-mockup.py)
  pour le diptyque social 08c du brand book. La card LinkedIn (max-width 920px)
  est centrée dans le viewport, avec marges Brume LinkedIn sur les côtés.
- device_scale_factor=2 (retina) : le mockup sera affiché à taille réduite dans
  le brand book (max-width ~560px), donc on capture en haute résolution pour
  garder un rendu net au zoom et éviter la pixellisation des polices/icônes.
- full_page=False : on capture le viewport, pas la page complète.

Notes d'implémentation
----------------------
- Attente : networkidle + 2s pour laisser charger Google Fonts (FOUT puis FOIT)
  et l'image cover (visual-final/*.jpg).
- Le PNG retina pèse plus lourd (~1-3 Mo) mais reste raisonnable pour un
  brand book HTML.
"""

import sys
from pathlib import Path

# Viewport quasi-carré 1000x1000 — format aligné sur X mockup pour le diptyque
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
    print("\nUsage: python3 capture-linkedin-mockup.py <input_html_path> <output_png_path>\n")
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

    # Conversion en file:// URI pour que les ressources relatives
    # (Google Fonts via réseau, visual-final/ en chemin local) soient résolues.
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

            # Wait additionnel pour laisser charger les Google Fonts (FOUT puis FOIT)
            # et l'image cover si elle est lourde.
            page.wait_for_timeout(EXTRA_WAIT_MS)

            # Capture ciblée sur la card profile uniquement (locator) avec fond
            # transparent (omit_background=True). Le PNG résultant a la taille
            # naturelle de la card (paysage ~1000×500) — pas de viewport carré
            # avec marges transparentes. Quand intégrée dans le diptyque social
            # du brand book, la card flotte directement sur le fond beige.
            page.locator(".li-profile-card").screenshot(
                path=str(output_png_path),
                type="png",
                omit_background=True,
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
