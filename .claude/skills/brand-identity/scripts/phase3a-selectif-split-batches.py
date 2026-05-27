#!/usr/bin/env python3
"""Phase 3A — Mode Sélectif : splitte le pool de 100 mots en 10 batchs de 10.

Lit le fichier 100-mots-selection.md produit par phase3a-selectif-build-pool.py,
randomise l'ordre (seed fixe = 2026 par défaut), et écrit 2 fichiers :
- batches.json (input des 10 sub-agents évaluateurs)
- batches-preview.md (audit lisible)

Usage :
    python3 phase3a-selectif-split-batches.py \\
        --session-dir <path absolu vers outputs/{session}/> \\
        --version <int> \\
        --registre <nom du registre> \\
        [--seed 2026]

Convention de chemins :
    Input  : {session_dir}/.tmp-selectif-v{version}/100-mots-selection.md
    Output : {session_dir}/.tmp-selectif-v{version}/batches.json
             {session_dir}/.tmp-selectif-v{version}/batches-preview.md
"""

import argparse
import json
import random
import re
import sys
from pathlib import Path


def parse_words(md_path: Path) -> list[str]:
    """Extrait tous les mots en gras du markdown de sélection."""
    words = []
    for line in md_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^- \*\*(.+?)\*\*", line)
        if m:
            words.append(m.group(1))
    return words


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--session-dir", required=True, type=Path)
    p.add_argument("--version", required=True, type=int)
    p.add_argument("--registre", required=True)
    p.add_argument("--seed", type=int, default=2026)
    args = p.parse_args()

    tmp_dir = args.session_dir / f".tmp-selectif-v{args.version}"
    src = tmp_dir / "100-mots-selection.md"
    if not src.is_file():
        sys.exit(f"Erreur : {src} introuvable. Lance phase3a-selectif-build-pool.py d'abord.")

    dst_json = tmp_dir / "batches.json"
    dst_md = tmp_dir / "batches-preview.md"

    words = parse_words(src)
    if len(words) != 100:
        sys.exit(f"Erreur : attendu 100 mots, trouvé {len(words)} dans {src}")

    random.seed(args.seed)
    shuffled = words.copy()
    random.shuffle(shuffled)

    batches = [shuffled[i*10:(i+1)*10] for i in range(10)]

    with dst_json.open("w", encoding="utf-8") as f:
        json.dump(
            {"registre": args.registre, "version": args.version, "seed": args.seed, "batches": batches},
            f, ensure_ascii=False, indent=2,
        )

    registre_title = args.registre.replace('-', ' ').title()
    with dst_md.open("w", encoding="utf-8") as f:
        f.write(f"# {registre_title} — 10 batchs (seed={args.seed})\n\n")
        for i, batch in enumerate(batches, 1):
            f.write(f"## Batch {i}\n\n")
            for w in batch:
                f.write(f"- {w}\n")
            f.write("\n")

    print(f"10 batchs écrits :")
    print(f"  - {dst_json}")
    print(f"  - {dst_md}\n")
    for i, batch in enumerate(batches, 1):
        print(f"  Batch {i}: {', '.join(batch[:3])}…")


if __name__ == "__main__":
    main()
