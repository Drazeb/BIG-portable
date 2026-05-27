#!/usr/bin/env python3
"""
randomize_pool.py — Génère un ordre aléatoire Fisher-Yates des 8 familles d'icônes.

Usage:
    python3 randomize_pool.py --run-dir <RUN_DIR> [--seed <INT>]

Effets:
    - Lit catalogue/_index.md (ou liste hardcodée si index absent)
    - Applique Fisher-Yates seedé
    - Anti-autoroute : si 01-pictogramme-geo tire la position 1, re-shuffle
    - Écrit RUN_DIR/pool-randomise.md avec la seed loggée
"""

from __future__ import annotations

import argparse
import random
import sys
from datetime import datetime
from pathlib import Path

# Pool fermé des 8 familles (ID stable + label affiché)
POOL = [
    ("01-pictogramme-geo", "Pictogramme géométrique propre (Heroicons-like)"),
    ("02-isometrique", "Isométrique / 3D"),
    ("03-pixel", "Pixel art"),
    ("04-gravure", "Gravure / linocut"),
    ("05-ornemental", "Ornemental (art déco / nouveau / blason)"),
    ("06-flat-illustre", "Flat illustré coloré (variante cinéma sombre disponible)"),
    ("07-sticker", "Sticker / cut-out"),
    ("08-brutaliste", "Brutaliste / ASCII"),
]


def fisher_yates(items: list, seed: int, anti_autoroute_id: str = "01-pictogramme-geo", max_attempts: int = 50) -> tuple[list, int]:
    """
    Mélange Fisher-Yates seedé.
    Anti-autoroute : si anti_autoroute_id atterrit en position 0, re-mélange avec seed+1.
    Renvoie (liste_melangee, seed_utilisee).
    """
    for attempt in range(max_attempts):
        current_seed = seed + attempt
        rng = random.Random(current_seed)
        shuffled = list(items)
        # Fisher-Yates classique
        for i in range(len(shuffled) - 1, 0, -1):
            j = rng.randint(0, i)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        # Anti-autoroute : refuser si anti_autoroute_id en position 0
        if shuffled[0][0] != anti_autoroute_id:
            return shuffled, current_seed
    # Fallback : tant pis, on accepte (improbable avec 8 entrées)
    return shuffled, current_seed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Chemin absolu du fichier de sortie (ex: {session_dir}/.tmp-icon-pool-randomise.md)")
    parser.add_argument("--seed", type=int, default=None, help="Seed Fisher-Yates (défaut: epoch timestamp)")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    seed = args.seed if args.seed is not None else int(datetime.now().timestamp())
    shuffled, used_seed = fisher_yates(POOL, seed)

    # Écriture
    lines = [
        f"# Pool randomisé des 8 familles",
        f"",
        f"**Seed Fisher-Yates** : `{used_seed}`",
        f"**Date génération** : {datetime.now().isoformat()}",
        f"**Anti-autoroute appliquée** : `01-pictogramme-geo` ne peut pas être en position 1 (re-shuffle si tiré)",
        f"",
        f"## Ordre du pool (à présenter au Router dans cet ordre exact)",
        f"",
    ]
    for i, (family_id, family_label) in enumerate(shuffled, start=1):
        lines.append(f"{i}. **{family_id}** — {family_label}")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] Pool randomisé écrit : {output_path}")
    print(f"     Seed utilisée : {used_seed}")
    print(f"     Position 1 : {shuffled[0][0]}")


if __name__ == "__main__":
    main()
