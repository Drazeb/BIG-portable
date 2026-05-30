#!/usr/bin/env python3
"""
verify-md5-fidelity.py
======================

Vérifie que TOUS les blocs verbatim attendus (manifest JSON produit par
`extract-batch2-inventory.py`) sont présents et **non altérés** dans un brand
book HTML final.

Mécanique
---------
Le brand book final contient des sections avec des blocs bornés par :

    <!-- BEGIN_BLOCK md5=<hash> -->
    <html du composant>
    <!-- END_BLOCK -->

Le script :
1. Lit `batch2-inventory.json` (manifest des hashes attendus).
2. Lit le brand book HTML final.
3. Pour chaque hash attendu, vérifie qu'il existe un bloc `BEGIN_BLOCK md5=<hash>`
   ET que le HTML interne re-hashé (MD5 sur le bloc normalisé) match le hash
   annoncé. Détecte ainsi les cas où le sub-agent aurait copié le commentaire
   `md5=xxx` sans le contenu correspondant, ou aurait altéré le contenu.

Usage
-----
    python3 verify-md5-fidelity.py <inventory.json> <brand-book.html>

Exit codes
----------
    0  Tous les hashes attendus présents + contenu fidèle (1:1 verbatim).
    1  FAIL : au moins un hash manque ou un contenu a été altéré.
    2  Mauvais usage CLI.
"""

import hashlib
import json
import re
import sys
from pathlib import Path


def compute_md5(block_html: str) -> str:
    """Identique à extract-batch2-inventory.py : MD5 sur strip whitespace."""
    return hashlib.md5(block_html.strip().encode("utf-8")).hexdigest()


def extract_blocks(brand_book_html: str) -> dict:
    """Retourne dict {hash_annonce → contenu_interne} pour chaque BEGIN/END."""
    pattern = re.compile(
        r"<!--\s*BEGIN_BLOCK\s+md5=([a-f0-9]{32})\s*-->(.*?)<!--\s*END_BLOCK\s*-->",
        re.DOTALL | re.IGNORECASE,
    )
    return {m.group(1): m.group(2) for m in pattern.finditer(brand_book_html)}


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)

    inventory_path = Path(sys.argv[1]).resolve()
    brand_book_path = Path(sys.argv[2]).resolve()

    if not inventory_path.exists():
        print(f"[ERROR] Manifest JSON introuvable : {inventory_path}")
        sys.exit(1)
    if not brand_book_path.exists():
        print(f"[ERROR] Brand book HTML introuvable : {brand_book_path}")
        sys.exit(1)

    manifest = json.loads(inventory_path.read_text(encoding="utf-8"))
    brand_book_html = brand_book_path.read_text(encoding="utf-8")

    expected_by_cat = {
        cat: [item["md5"] for item in data["items"]]
        for cat, data in manifest["categories"].items()
    }
    all_expected = {
        item["md5"]
        for data in manifest["categories"].values()
        for item in data["items"]
    }
    found_blocks = extract_blocks(brand_book_html)

    missing = sorted(all_expected - set(found_blocks))
    altered = []
    for hsh, content in found_blocks.items():
        if hsh in all_expected:
            recomputed = compute_md5(content)
            if recomputed != hsh:
                altered.append((hsh, recomputed))

    extra = sorted(set(found_blocks) - all_expected)

    total_expected = len(all_expected)
    total_found = len(found_blocks)
    print(f"[INFO] Manifest    : {inventory_path}")
    print(f"[INFO] Brand book  : {brand_book_path}")
    print(f"[INFO] Attendus    : {total_expected} blocs sur {len(manifest['categories'])} catégories")
    print(f"[INFO] Trouvés     : {total_found} blocs dans le brand book")

    if not missing and not altered and not extra:
        print(f"[OK]   Fidélité 1:1 verbatim vérifiée — {total_expected} blocs présents et intacts.")
        sys.exit(0)

    if missing:
        print(f"[FAIL] {len(missing)} bloc(s) ATTENDU(S) absent(s) du brand book :")
        for hsh in missing[:20]:
            cat = next(
                (c for c, hashes in expected_by_cat.items() if hsh in hashes),
                "?",
            )
            print(f"         · {hsh}  ({cat})")
        if len(missing) > 20:
            print(f"         · … et {len(missing) - 20} autre(s)")

    if altered:
        print(f"[FAIL] {len(altered)} bloc(s) ALTÉRÉ(S) (hash annoncé ≠ hash recalculé) :")
        for annoucned, recomputed in altered[:20]:
            print(f"         · annoncé={annoucned}  recalculé={recomputed}")

    if extra:
        print(f"[WARN] {len(extra)} bloc(s) PRÉSENT(S) dans le brand book mais ABSENT(S) du manifest :")
        for hsh in extra[:10]:
            print(f"         · {hsh}")

    sys.exit(1)


if __name__ == "__main__":
    main()
