#!/usr/bin/env python3
"""Phase 3A — Mode Sélectif : construit le pool final propre + sélectionne 100 mots.

Lit les 5 fichiers pool-run*.md produits par les 5 sub-agents "couvreur de registre"
dans le dossier intermédiaire de la session, déduplique morphologiquement, applique
la sélection stratifiée (5/5 + 4/5 gardés intégralement + sample uniforme du reste),
et écrit 2 fichiers :
- pool-final.md (audit complet, toutes les fréquences)
- 100-mots-selection.md (sélection finale prête à splitter en batchs)

Usage :
    python3 phase3a-selectif-build-pool.py \\
        --session-dir <path absolu vers outputs/{session}/> \\
        --version <int> \\
        --registre <nom du registre>

Convention de chemins :
    Input  : {session_dir}/.tmp-selectif-v{version}/pool-run{1..5}.md
    Output : {session_dir}/.tmp-selectif-v{version}/pool-final.md
             {session_dir}/.tmp-selectif-v{version}/100-mots-selection.md
"""

import argparse
import random
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


def normalize(word: str) -> str:
    """Lowercase + strip accents + collapse spaces. Pour comparer 'Doppler' et 'doppler'."""
    w = word.strip().lower()
    w = unicodedata.normalize("NFD", w)
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    w = re.sub(r"\s+", " ", w)
    return w


def parse_pool(path: Path) -> list[str]:
    """Extrait les mots numérotés '1. mot' d'un fichier markdown."""
    words = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*\d+\.\s+(.+?)\s*$", line)
        if m:
            words.append(m.group(1))
    return words


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--session-dir", required=True, type=Path)
    p.add_argument("--version", required=True, type=int)
    p.add_argument("--registre", required=True)
    args = p.parse_args()

    tmp_dir = args.session_dir / f".tmp-selectif-v{args.version}"
    if not tmp_dir.is_dir():
        sys.exit(f"Erreur : dossier {tmp_dir} introuvable")

    paths = sorted(tmp_dir.glob("pool-run*.md"))
    if not paths:
        sys.exit(f"Erreur : aucun fichier pool-run*.md trouvé dans {tmp_dir}")

    raw_pools = [parse_pool(p) for p in paths]
    norm_to_display: dict[str, str] = {}
    word_count: Counter = Counter()

    for pool in raw_pools:
        seen_in_pool = set()
        for w in pool:
            n = normalize(w)
            if n in seen_in_pool:
                continue
            seen_in_pool.add(n)
            if n not in norm_to_display:
                norm_to_display[n] = w
            word_count[n] += 1

    strates: dict[int, list[str]] = defaultdict(list)
    for n, c in word_count.items():
        strates[c].append(n)

    n_runs = len(raw_pools)
    full_pool_size = sum(len(v) for v in strates.values())

    print(f"=== POOL {args.registre} ({n_runs} runs) ===")
    print(f"  Total après dédup : {full_pool_size} mots distincts")
    for k in range(n_runs, 0, -1):
        print(f"  {k}/{n_runs} runs : {len(strates[k])} mots")

    # Sélection stratifiée : tout le 5/5 + tout le 4/5 + sample uniforme du reste
    kept = []
    for k in (n_runs, n_runs - 1):
        kept.extend(sorted(strates[k]))

    samplable = []
    for k in range(1, n_runs - 1):
        samplable.extend(strates[k])

    n_to_sample = 100 - len(kept)
    if n_to_sample < 0:
        sys.exit(f"Erreur : noyau {len(kept)} > 100 mots demandés.")
    if n_to_sample > len(samplable):
        sys.exit(f"Erreur : besoin de {n_to_sample} mots à sampler mais seulement {len(samplable)} disponibles.")

    random.seed(42)
    sampled = random.sample(samplable, n_to_sample)

    print(f"\n=== SÉLECTION ===")
    print(f"  Noyau (5/5 + 4/5) gardé : {len(kept)} mots")
    print(f"  Variance samplée : {n_to_sample}/{len(samplable)}")
    print(f"  TOTAL : {len(kept) + n_to_sample} mots")

    pool_md = tmp_dir / "pool-final.md"
    sample_md = tmp_dir / "100-mots-selection.md"
    registre_title = args.registre.replace('-', ' ').title()

    with pool_md.open("w", encoding="utf-8") as f:
        f.write(f"# Pool complet — {registre_title} ({n_runs} runs, dédupliqué)\n\n")
        f.write(f"**Total : {full_pool_size} mots distincts.**\n\n")
        for k in range(n_runs, 0, -1):
            if not strates[k]:
                continue
            f.write(f"\n## Présents dans {k}/{n_runs} runs ({len(strates[k])} mots)\n\n")
            for n in sorted(strates[k]):
                f.write(f"- **{norm_to_display.get(n, n)}**\n")

    with sample_md.open("w", encoding="utf-8") as f:
        f.write(f"# Sélection finale — 100 mots {registre_title}\n\n")
        f.write("Méthode : tout le 5/5 + tout le 4/5 + sample uniforme du reste (seed=42).\n\n")
        f.write(f"## Noyau dur — {n_runs}/{n_runs} ({len(strates[n_runs])} mots)\n\n")
        for n in sorted(strates[n_runs]):
            f.write(f"- **{norm_to_display.get(n, n)}**\n")
        f.write(f"\n## Quasi-noyau — {n_runs-1}/{n_runs} ({len(strates[n_runs-1])} mots)\n\n")
        for n in sorted(strates[n_runs - 1]):
            f.write(f"- **{norm_to_display.get(n, n)}**\n")
        f.write(f"\n## Tirage de dispersion — {n_to_sample} mots\n\n")
        for n in sorted(sampled):
            f.write(f"- **{norm_to_display.get(n, n)}** _(présent dans {word_count[n]}/{n_runs} runs)_\n")

    print(f"\nFichiers écrits :")
    print(f"  - {pool_md}")
    print(f"  - {sample_md}")


if __name__ == "__main__":
    main()
